"""
Predictive model: π/σ = f(period, LP_sum, ΔEN, r_max)

If we can predict π/σ from atomic properties alone,
we can predict α for ANY element pair without measuring E₁ and E₂.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alphalaw.data import BONDS, ELEMENTS

EN = {
    "H": 2.20, "B": 2.04, "C": 2.55, "N": 3.04, "O": 3.44, "F": 3.98,
    "Al": 1.61, "Si": 1.90, "P": 2.19, "S": 2.58, "Cl": 3.16,
    "Ge": 2.01, "As": 2.18, "Se": 2.55, "Sn": 1.96, "Te": 2.10,
}

RADII = {
    "B": 84, "C": 76, "N": 71, "O": 66, "F": 57, "Al": 121, "Si": 111,
    "P": 107, "S": 105, "Cl": 102, "Ge": 120, "As": 119, "Se": 120,
    "Te": 138, "Sn": 139,
}


def build_dataset():
    """Build feature matrix for s/p bonds with 2+ orders."""
    rows = []
    for b in BONDS:
        if b.alpha is None or b.block == "d":
            continue
        if 1 not in b.energies or 2 not in b.energies:
            continue
        pi_sigma = (b.energies[2] - b.energies[1]) / b.energies[1]
        dEN = abs(EN.get(b.elem_A, 0) - EN.get(b.elem_B, 0))
        r_max = max(RADII.get(b.elem_A, 999), RADII.get(b.elem_B, 999))
        lp_sum = (b.LP_A + b.LP_B) if b.LP_A >= 0 and b.LP_B >= 0 else 0
        lp_max = max(b.LP_A, b.LP_B) if b.LP_A >= 0 and b.LP_B >= 0 else 0

        rows.append({
            "bond": b.bond, "alpha": b.alpha, "pi_sigma": pi_sigma,
            "period": b.period, "lp_sum": lp_sum, "lp_max": lp_max,
            "dEN": dEN, "r_max": r_max,
        })
    return rows


def linear_regression(X, y):
    """Simple OLS: y = X @ beta. Returns beta."""
    # X: list of lists, y: list
    import numpy as np
    X = np.array(X, dtype=float)
    y = np.array(y, dtype=float)
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    y_pred = X @ beta
    residuals = y - y_pred
    ss_res = sum(r**2 for r in residuals)
    ss_tot = sum((yi - sum(y)/len(y))**2 for yi in y)
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return beta, r_squared, y_pred


def leave_one_out(rows, feature_names, target="pi_sigma"):
    """LOO cross-validation."""
    errors = []
    classifications = []

    for i in range(len(rows)):
        train = [r for j, r in enumerate(rows) if j != i]
        test = rows[i]

        X_train = [[r[f] for f in feature_names] + [1] for r in train]
        y_train = [r[target] for r in train]
        X_test = [test[f] for f in feature_names] + [1]

        beta, _, _ = linear_regression(X_train, y_train)
        y_pred = sum(b * x for b, x in zip(beta, X_test))

        actual_alpha = test["alpha"]
        actual_mol = actual_alpha > 1
        pred_mol = y_pred > 1  # predict molecule if π/σ > 1

        errors.append(abs(y_pred - test[target]))
        classifications.append(pred_mol == actual_mol)

    mae = sum(errors) / len(errors)
    accuracy = sum(classifications) / len(classifications)
    return mae, accuracy


def main():
    rows = build_dataset()
    n = len(rows)
    print("=" * 80)
    print(f"МОДЕЛЬ ПРЕДСКАЗАНИЯ π/σ ({n} связей s/p-блока)")
    print("=" * 80)

    # Try different feature combinations
    feature_sets = [
        ("period", ["period"]),
        ("lp_sum", ["lp_sum"]),
        ("dEN", ["dEN"]),
        ("r_max", ["r_max"]),
        ("period + lp_sum", ["period", "lp_sum"]),
        ("period + lp_sum + dEN", ["period", "lp_sum", "dEN"]),
        ("r_max + lp_sum + dEN", ["r_max", "lp_sum", "dEN"]),
        ("r_max + lp_max + dEN", ["r_max", "lp_max", "dEN"]),
        ("period + lp_sum + dEN + r_max", ["period", "lp_sum", "dEN", "r_max"]),
    ]

    print(f"\n{'Признаки':<35} {'R²':>6} {'MAE':>6} {'LOO точн.':>10}")
    print("-" * 65)

    best_accuracy = 0
    best_features = None

    for name, features in feature_sets:
        X = [[r[f] for f in features] + [1] for r in rows]
        y = [r["pi_sigma"] for r in rows]
        beta, r2, y_pred = linear_regression(X, y)
        mae, loo_acc = leave_one_out(rows, features)

        print(f"{name:<35} {r2:>6.3f} {mae:>6.3f} {loo_acc:>9.1%}")

        if loo_acc > best_accuracy:
            best_accuracy = loo_acc
            best_features = (name, features, beta)

    # Best model details
    name, features, beta = best_features
    print(f"\n{'='*80}")
    print(f"ЛУЧШАЯ МОДЕЛЬ: {name}")
    print(f"{'='*80}")

    print(f"\n  π/σ = ", end="")
    terms = []
    for i, f in enumerate(features):
        terms.append(f"{beta[i]:+.4f}·{f}")
    terms.append(f"{beta[-1]:+.4f}")
    print(" ".join(terms))

    # Show predictions
    X = [[r[f] for f in features] + [1] for r in rows]
    y = [r["pi_sigma"] for r in rows]
    _, _, y_pred = linear_regression(X, y)

    print(f"\n  {'Связь':<8} {'π/σ факт':>9} {'π/σ пред':>9} {'α':>6} "
          f"{'Факт':>6} {'Пред':>6} {'OK?':>4}")
    print(f"  {'-'*55}")

    correct = 0
    for i, r in enumerate(rows):
        actual_type = "МОЛ" if r["alpha"] > 1 else "КРИСТ"
        pred_type = "МОЛ" if y_pred[i] > 1 else "КРИСТ"
        ok = "✓" if actual_type == pred_type else "✗"
        if actual_type == pred_type:
            correct += 1
        print(f"  {r['bond']:<8} {r['pi_sigma']:>9.3f} {y_pred[i]:>9.3f} "
              f"{r['alpha']:>6.3f} {actual_type:>6} {pred_type:>6} {ok:>4}")

    print(f"\n  Точность классификации: {correct}/{n} = {100*correct/n:.1f}%")

    # Now: predict for NEW pairs
    print(f"\n{'='*80}")
    print("ПРЕДСКАЗАНИЯ ДЛЯ НОВЫХ ПАР (нет экспериментальных E₁, E₂)")
    print(f"{'='*80}")

    new_pairs = [
        # Pairs we don't have in dataset
        ("H", "H"), ("H", "O"), ("H", "N"), ("H", "C"), ("H", "F"),
        ("C", "F"), ("C", "Cl"), ("N", "F"), ("N", "Cl"),
        ("Si", "S"), ("Si", "C"), ("Si", "P"),
        ("Ge", "N"), ("Ge", "S"),
        ("As", "O"), ("As", "S"), ("As", "N"),
        ("Se", "O"), ("Se", "S"),
        ("Sn", "O"), ("Sn", "S"),
        ("Te", "O"),
        ("P", "N"),
        ("B", "S"), ("B", "F"),
        ("Al", "N"), ("Al", "S"),
    ]

    print(f"\n  {'Пара':<8} {'π/σ пред':>9} {'Предсказание':<14} {'Причина'}")
    print(f"  {'-'*65}")

    for e1, e2 in new_pairs:
        if e1 not in ELEMENTS or e2 not in ELEMENTS:
            continue
        p1, g1, blk1, v1, lp1 = ELEMENTS[e1]
        p2, g2, blk2, v2, lp2 = ELEMENTS[e2]

        period = max(p1, p2)
        lp_sum = (lp1 + lp2) if lp1 >= 0 and lp2 >= 0 else 0
        lp_max = max(lp1, lp2) if lp1 >= 0 and lp2 >= 0 else 0
        dEN = abs(EN.get(e1, 2.0) - EN.get(e2, 2.0))
        r_max = max(RADII.get(e1, 100), RADII.get(e2, 100))

        x = [{"period": period, "lp_sum": lp_sum, "lp_max": lp_max,
              "dEN": dEN, "r_max": r_max}[f] for f in features] + [1]
        ps_pred = sum(b * xi for b, xi in zip(beta, x))

        pred = "МОЛЕКУЛА" if ps_pred > 1 else "КРИСТАЛЛ"
        reason = ""
        if ps_pred > 1.5:
            reason = "сильный бок"
        elif ps_pred > 1:
            reason = "бок > ось"
        elif ps_pred > 0.8:
            reason = "пограничный"
        elif dEN > 1.0:
            reason = f"ионный (ΔEN={dEN:.1f})"
        elif r_max > 120:
            reason = "большой тороид"
        else:
            reason = "ось > бок"

        print(f"  {e1}-{e2:<5} {ps_pred:>9.3f} {pred:<14} {reason}")


if __name__ == "__main__":
    main()
