"""
KAN (Kolmogorov-Arnold Network) to discover E₁ = f(toroid properties).

KAN advantage: learns interpretable univariate functions on edges.
Even on small data, if the true function is simple, KAN can find it.

Features (non-circular, from toroid model):
- IE_A, IE_B: ionization energies (= ℏω, toroid frequency)
- r_A, r_B: covalent radii (toroid size)
- LP_A, LP_B: lone pairs (free lateral channels)
"""
import sys, os, math
import numpy as np
import torch
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alphalaw.data import BONDS, ELEMENTS

# Ionization energies (kJ/mol)
IE = {
    "H": 1312, "B": 801, "C": 1086, "N": 1402, "O": 1314,
    "F": 1681, "Al": 577, "Si": 786, "P": 1012, "S": 1000,
    "Cl": 1251, "Ge": 762, "As": 947, "Se": 941, "Br": 1140,
    "Sn": 709, "Te": 869, "I": 1008,
    "Cr": 653, "Mo": 684, "W": 770, "Re": 760,
}

# Covalent radii (pm)
RADII = {
    "H": 31, "B": 84, "C": 76, "N": 71, "O": 66, "F": 57,
    "Al": 121, "Si": 111, "P": 107, "S": 105, "Cl": 102,
    "Ge": 120, "As": 119, "Se": 120, "Br": 120,
    "Sn": 139, "Te": 138, "I": 139,
    "Cr": 139, "Mo": 154, "W": 162, "Re": 151,
}


def build_dataset():
    """Build (features, target) for E₁ prediction."""
    X = []
    y = []
    bonds = []

    for b in BONDS:
        if 1 not in b.energies:
            continue
        ie_a = IE.get(b.elem_A)
        ie_b = IE.get(b.elem_B)
        r_a = RADII.get(b.elem_A)
        r_b = RADII.get(b.elem_B)
        if ie_a is None or ie_b is None or r_a is None or r_b is None:
            continue

        lp_a = b.LP_A if b.LP_A >= 0 else 0
        lp_b = b.LP_B if b.LP_B >= 0 else 0

        # Symmetric features (order-independent)
        ie_mean = (ie_a + ie_b) / 2
        ie_diff = abs(ie_a - ie_b)
        ie_prod = math.sqrt(ie_a * ie_b)
        r_mean = (r_a + r_b) / 2
        r_max = max(r_a, r_b)
        lp_sum = lp_a + lp_b
        lp_max = max(lp_a, lp_b)

        E1 = b.energies[1]

        X.append([ie_mean, ie_diff, r_mean, lp_sum])
        y.append(E1)
        bonds.append(b.bond)

    return np.array(X), np.array(y), bonds


def try_symbolic_first(X, y, bonds):
    """Before KAN, try simple symbolic forms."""
    print("=" * 80)
    print("СИМВОЛЬНЫЙ ПОИСК: простые формулы для E₁")
    print("=" * 80)

    ie_mean = X[:, 0]
    ie_diff = X[:, 1]
    r_mean = X[:, 2]
    lp_sum = X[:, 3]
    n = len(y)

    # Try various forms
    candidates = [
        ("IE_mean / r_mean", ie_mean / r_mean),
        ("IE_mean / r_mean²", ie_mean / r_mean**2 * 1000),
        ("IE_mean² / r_mean", ie_mean**2 / r_mean / 1000),
        ("√(IE_mean) / r_mean", np.sqrt(ie_mean) / r_mean * 100),
        ("IE_prod / r_sum (Morse-like)", ie_mean / r_mean),
        ("(IE_mean - k·LP) / r", (ie_mean - 100*lp_sum) / r_mean),
        ("IE_mean·exp(-r/100)", ie_mean * np.exp(-r_mean/100)),
        ("IE_mean / (r + 10·LP)", ie_mean / (r_mean + 10*lp_sum + 1)),
        ("IE_mean² / (r · (1+LP))", ie_mean**2 / (r_mean * (1 + lp_sum)) / 1000),
    ]

    print(f"\n  {'Формула':<35} {'R²':>6} {'масштаб':>10}")
    print(f"  {'-'*55}")

    best_r2 = -999
    best_name = ""

    for name, x_cand in candidates:
        # Linear fit: E1 = a*x + b
        A = np.column_stack([x_cand, np.ones(n)])
        beta = np.linalg.lstsq(A, y, rcond=None)[0]
        y_pred = A @ beta
        ss_res = np.sum((y - y_pred)**2)
        ss_tot = np.sum((y - y.mean())**2)
        r2 = 1 - ss_res / ss_tot
        print(f"  {name:<35} {r2:>6.3f} {beta[0]:>10.4f}")
        if r2 > best_r2:
            best_r2 = r2
            best_name = name
            best_beta = beta
            best_pred = y_pred
            best_x = x_cand

    print(f"\n  Лучшая: {best_name}, R² = {best_r2:.3f}")

    # Multi-feature linear
    print(f"\n  Многофакторная линейная:")
    A = np.column_stack([X, np.ones(n)])
    beta = np.linalg.lstsq(A, y, rcond=None)[0]
    y_pred = A @ beta
    r2 = 1 - np.sum((y - y_pred)**2) / np.sum((y - y.mean())**2)
    print(f"  E₁ = {beta[0]:.3f}·IE_mean + {beta[1]:.3f}·ΔIE + {beta[2]:.3f}·r_mean + {beta[3]:.1f}·LP + {beta[4]:.1f}")
    print(f"  R² = {r2:.3f}")

    # Non-linear combos
    print(f"\n  Нелинейные комбинации:")
    combos = [
        ("IE/r + ΔIE + LP", np.column_stack([ie_mean/r_mean, ie_diff, lp_sum])),
        ("IE²/r + LP", np.column_stack([ie_mean**2/r_mean/1000, lp_sum])),
        ("IE/r + IE·LP/r²", np.column_stack([ie_mean/r_mean, ie_mean*lp_sum/r_mean**2])),
        ("√IE·√IE/r + LP/r", np.column_stack([np.sqrt(ie_mean)/r_mean*100, lp_sum/r_mean*100])),
        ("IE_mean/r + ΔIE/r + LP/r²",
         np.column_stack([ie_mean/r_mean, ie_diff/r_mean, lp_sum/r_mean**2*10000])),
    ]

    for name, Xc in combos:
        A = np.column_stack([Xc, np.ones(n)])
        beta = np.linalg.lstsq(A, y, rcond=None)[0]
        yp = A @ beta
        r2 = 1 - np.sum((y - yp)**2) / np.sum((y - y.mean())**2)
        print(f"  {name:<35} R² = {r2:.3f}")

    return best_r2


def try_kan(X, y, bonds):
    """Use KAN to find the function."""
    print(f"\n{'='*80}")
    print("KAN: поиск функции E₁ = f(IE_mean, ΔIE, r_mean, LP_sum)")
    print(f"{'='*80}")

    try:
        from efficient_kan import KAN
    except ImportError:
        print("  efficient_kan не установлен")
        return

    # Normalize features
    X_norm = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-8)
    y_norm = (y - y.mean()) / y.std()

    X_t = torch.FloatTensor(X_norm)
    y_t = torch.FloatTensor(y_norm).unsqueeze(1)

    dataset = {
        'train_input': X_t,
        'train_label': y_t,
        'test_input': X_t,  # same (small dataset)
        'test_label': y_t,
    }

    # efficient_kan: KAN(layers_hidden, grid_size, spline_order)
    # 4 inputs → 6 hidden → 1 output
    try:
        model = KAN([4, 6, 1], grid_size=5, spline_order=3)
        optimizer = torch.optim.LBFGS(model.parameters(), lr=0.1)
        loss_fn = torch.nn.MSELoss()

        # Train
        for epoch in range(300):
            def closure():
                optimizer.zero_grad()
                pred = model(X_t)
                loss = loss_fn(pred, y_t)
                loss.backward()
                return loss
            loss = optimizer.step(closure)

            if epoch % 100 == 0:
                with torch.no_grad():
                    pred = model(X_t)
                    mse = loss_fn(pred, y_t).item()
                print(f"  Эпоха {epoch}: MSE = {mse:.4f}")

        # Final predictions
        with torch.no_grad():
            y_pred_norm = model(X_t).numpy().flatten()

        y_pred = y_pred_norm * y.std() + y.mean()

        r2 = 1 - np.sum((y - y_pred)**2) / np.sum((y - y.mean())**2)
        print(f"\n  KAN R² = {r2:.3f}")

        # Show predictions
        print(f"\n  {'Связь':<8} {'E₁ факт':>8} {'E₁ KAN':>8} {'Ошибка':>8}")
        print(f"  {'-'*35}")
        for i, bond in enumerate(bonds):
            err = y[i] - y_pred[i]
            print(f"  {bond:<8} {y[i]:>8.0f} {y_pred[i]:>8.0f} {err:>+8.0f}")

        mae = np.mean(np.abs(y - y_pred))
        print(f"\n  MAE = {mae:.1f} кДж/моль")

        # LOO cross-validation
        print(f"\n  Leave-one-out перекрёстная проверка...")
        loo_errors = []
        for i in range(len(bonds)):
            mask = np.ones(len(bonds), dtype=bool)
            mask[i] = False
            X_tr = torch.FloatTensor((X[mask] - X.mean(0)) / (X.std(0) + 1e-8))
            y_tr = torch.FloatTensor(((y[mask] - y.mean()) / y.std())).unsqueeze(1)
            X_te = torch.FloatTensor(((X[i:i+1] - X.mean(0)) / (X.std(0) + 1e-8)))

            m = KAN([4, 6, 1], grid_size=5, spline_order=3)
            opt = torch.optim.LBFGS(m.parameters(), lr=0.1)
            for _ in range(200):
                def cl():
                    opt.zero_grad()
                    p = m(X_tr)
                    l = loss_fn(p, y_tr)
                    l.backward()
                    return l
                opt.step(cl)
            with torch.no_grad():
                pred = m(X_te).item() * y.std() + y.mean()
            loo_errors.append(abs(pred - y[i]))

        loo_mae = np.mean(loo_errors)
        print(f"  LOO MAE = {loo_mae:.1f} кДж/моль")

        # Classification from LOO
        loo_r2 = 1 - np.sum(np.array(loo_errors)**2) / np.sum((y - y.mean())**2)
        print(f"  LOO R² = {loo_r2:.3f}")

    except Exception as e:
        print(f"  KAN ошибка: {e}")
        import traceback
        traceback.print_exc()


def main():
    X, y, bonds = build_dataset()
    print(f"Датасет: {len(bonds)} связей, {X.shape[1]} признаков")
    print(f"Признаки: IE_mean, ΔIE, r_mean, LP_sum")
    print(f"Цель: E₁ (одинарная связь, кДж/моль)")
    print(f"Диапазон E₁: {y.min():.0f} — {y.max():.0f}")

    best_symbolic = try_symbolic_first(X, y, bonds)

    if best_symbolic < 0.8:
        print(f"\n  Символьный R² = {best_symbolic:.3f} < 0.8. Пробуем KAN...")
        try_kan(X, y, bonds)
    else:
        print(f"\n  Символьный R² = {best_symbolic:.3f} ≥ 0.8. KAN не нужен.")


if __name__ == "__main__":
    main()
