"""
Exploration: Can RemizovNet discover an ODE governing alphalaw data?

4 variants tested:
  1. E₁(Z) — single bond energy as "wave function" along periodic table
  2. α(π/σ) — power-law exponent as function of pi/sigma ratio
  3. E₁(ΔEN) — bond energy vs electronegativity difference
  4. π/σ(PCA₁) — pi/sigma along first principal component of 4 features

RemizovNet solves: a(x)·y'' + b(x)·y' + c(x)·y = g(x)
EquationDiscoverer: given (g, y) pairs, discovers a, b, c.
"""
import sys
import os
import math

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alphalaw.data import BONDS
from remizov_net import EquationDiscoverer

# ============================================================
# Shared data
# ============================================================

# Pauling electronegativity
EN = {
    "H": 2.20, "Li": 0.98, "Be": 1.57, "B": 2.04, "C": 2.55, "N": 3.04,
    "O": 3.44, "F": 3.98, "Na": 0.93, "Mg": 1.31, "Al": 1.61, "Si": 1.90,
    "P": 2.19, "S": 2.58, "Cl": 3.16, "Ge": 2.01, "As": 2.18,
    "Se": 2.55, "Br": 2.96, "Sn": 1.96, "Te": 2.10, "I": 2.66,
    "Cr": 1.66, "Mo": 2.16, "W": 2.36, "Re": 1.90,
}

RADII = {
    "H": 31, "B": 84, "C": 76, "N": 71, "O": 66, "F": 57,
    "Al": 121, "Si": 111, "P": 107, "S": 105, "Cl": 102,
    "Ge": 120, "As": 119, "Se": 120, "Te": 138, "Sn": 139,
}

# Atomic numbers
Z_MAP = {
    "H": 1, "Li": 3, "Be": 4, "B": 5, "C": 6, "N": 7, "O": 8, "F": 9,
    "Na": 11, "Mg": 12, "Al": 13, "Si": 14, "P": 15, "S": 16, "Cl": 17,
    "Ge": 32, "As": 33, "Se": 34, "Br": 35, "Sn": 50, "Te": 52, "I": 53,
    "Cr": 24, "Mo": 42, "W": 74, "Re": 75,
}


def get_sp_bonds_with_pi_sigma():
    """Get s/p bonds that have both E₁ and E₂ (for π/σ)."""
    result = []
    for b in BONDS:
        if b.alpha is None or b.block == "d":
            continue
        if 1 not in b.energies or 2 not in b.energies:
            continue
        E1, E2 = b.energies[1], b.energies[2]
        pi_sigma = (E2 - E1) / E1
        en_a = EN.get(b.elem_A, 0)
        en_b = EN.get(b.elem_B, 0)
        delta_en = abs(en_a - en_b)
        r_max = max(RADII.get(b.elem_A, 100), RADII.get(b.elem_B, 100))
        lp_sum = b.LP_A + b.LP_B if b.LP_A >= 0 and b.LP_B >= 0 else 0
        result.append({
            "bond": b.bond,
            "alpha": b.alpha,
            "pi_sigma": pi_sigma,
            "E1": E1,
            "E2": E2,
            "delta_en": delta_en,
            "r_max": r_max,
            "period": b.period,
            "lp_sum": lp_sum,
            "elem_A": b.elem_A,
            "elem_B": b.elem_B,
        })
    return result


def interpolate_to_grid(x_data, y_data, grid_size=64):
    """Interpolate scattered data onto a uniform grid via cubic spline."""
    from scipy.interpolate import CubicSpline

    # Sort by x
    idx = np.argsort(x_data)
    x_sorted = x_data[idx]
    y_sorted = y_data[idx]

    # Remove duplicates (average y for same x)
    x_unique, indices = np.unique(x_sorted, return_inverse=True)
    y_unique = np.zeros(len(x_unique))
    counts = np.zeros(len(x_unique))
    for i, idx_val in enumerate(indices):
        y_unique[idx_val] += y_sorted[i]
        counts[idx_val] += 1
    y_unique /= counts

    if len(x_unique) < 4:
        # Not enough for cubic spline — use linear
        x_grid = np.linspace(x_unique[0], x_unique[-1], grid_size)
        y_grid = np.interp(x_grid, x_unique, y_unique)
        return x_grid, y_grid

    cs = CubicSpline(x_unique, y_unique, bc_type="natural")
    x_grid = np.linspace(x_unique[0], x_unique[-1], grid_size)
    y_grid = cs(x_grid)
    return x_grid, y_grid


def generate_bootstrap_pairs(y_grid, n_samples=30, noise_level=0.05):
    """Generate (g, y) pairs for EquationDiscoverer via bootstrap.

    Strategy: y is the observed signal. g = y + noise variations.
    The ODE maps g → y, so we create noisy g's that all map to similar y's.

    Actually, we need input-output pairs where the ODE transforms g into y.
    We'll use: g_i = y + ε_i, y_i = y (constant target with noisy inputs).
    This discovers an ODE whose Green's function smooths noise → signal.

    Alternative: use identity pairs g=y, y=y (trivial), plus perturbations.
    """
    grid_size = len(y_grid)
    g_data = np.zeros((n_samples, grid_size))
    y_data = np.zeros((n_samples, grid_size))

    y_norm = y_grid / (np.max(np.abs(y_grid)) + 1e-10)  # normalize

    for i in range(n_samples):
        noise = np.random.randn(grid_size) * noise_level
        g_data[i] = y_norm + noise
        y_data[i] = y_norm

    return (
        torch.tensor(g_data, dtype=torch.float32),
        torch.tensor(y_data, dtype=torch.float32),
    )


def run_discovery(x_grid, y_grid, label, grid_size=64, epochs=2000, n_samples=30):
    """Run EquationDiscoverer and return results."""
    print(f"\n{'='*70}")
    print(f"  VARIANT: {label}")
    print(f"  Data points: {len(y_grid)}, Grid size: {grid_size}")
    print(f"{'='*70}")

    dx = (x_grid[-1] - x_grid[0]) / (len(x_grid) - 1)
    g_data, y_data = generate_bootstrap_pairs(y_grid, n_samples=n_samples)

    discoverer = EquationDiscoverer(
        grid_size=grid_size,
        n_steps=20,
        total_time=1.0,
        lr=1e-3,
        dx=float(dx),
    )

    result = discoverer.fit(
        g_data, y_data,
        epochs=epochs,
        tol=1e-8,
        verbose=True,
        print_every=500,
    )

    # Evaluate reconstruction
    with torch.no_grad():
        y_pred = discoverer.model(g_data).numpy()
    mse = np.mean((y_pred - y_data.numpy()) ** 2)
    y_var = np.var(y_data.numpy())
    r2 = 1 - mse / y_var if y_var > 0 else 0

    # Coefficient analysis
    a_vals = result.a.numpy()
    b_vals = result.b.numpy()
    c_vals = result.c.numpy()

    print(f"\n  Discovered equation: {result.equation}")
    print(f"  Converged: {result.converged}")
    print(f"  Final loss: {result.loss_history[-1]:.2e}")
    print(f"  R² (reconstruction): {r2:.4f}")
    print(f"  MSE: {mse:.2e}")
    print(f"\n  Coefficients (mean ± std):")
    print(f"    a(x): {a_vals.mean():.4f} ± {a_vals.std():.4f}  (diffusion)")
    print(f"    b(x): {b_vals.mean():.4f} ± {b_vals.std():.4f}  (advection)")
    print(f"    c(x): {c_vals.mean():.4f} ± {c_vals.std():.4f}  (reaction)")

    # Physical interpretation
    V = c_vals - b_vals**2 / (4 * a_vals)
    print(f"    V(x): {V.mean():.4f} ± {V.std():.4f}  (potential)")

    is_diffusion_dominant = a_vals.mean() > abs(b_vals.mean())
    is_potential_varying = V.std() / (abs(V.mean()) + 1e-10) > 0.3

    print(f"\n  Interpretation:")
    if is_diffusion_dominant:
        print(f"    → Diffusion-dominated (a >> |b|): smoothing dynamics")
    else:
        print(f"    → Advection/potential-dominated: wave-like or decay dynamics")
    if is_potential_varying:
        print(f"    → Spatially-varying potential: non-trivial structure!")
    else:
        print(f"    → Nearly constant potential: simple exponential behavior")

    return {
        "label": label,
        "equation": result.equation,
        "r2": r2,
        "mse": mse,
        "final_loss": result.loss_history[-1],
        "converged": result.converged,
        "a_mean": float(a_vals.mean()),
        "b_mean": float(b_vals.mean()),
        "c_mean": float(c_vals.mean()),
        "V_mean": float(V.mean()),
        "V_std": float(V.std()),
        "a_vals": a_vals,
        "b_vals": b_vals,
        "c_vals": c_vals,
        "x_grid": x_grid,
        "y_grid": y_grid,
    }


# ============================================================
# Variant 1: E₁(Z) along periodic table
# ============================================================
def variant1_e1_along_z():
    """E₁(Z) — single bond energy as wave function along Z."""
    # Collect homonuclear s/p bonds
    z_list, e1_list, labels = [], [], []
    for b in BONDS:
        if b.elem_A != b.elem_B:
            continue
        if 1 not in b.energies:
            continue
        z = Z_MAP.get(b.elem_A)
        if z is None:
            continue
        z_list.append(z)
        e1_list.append(b.energies[1])
        labels.append(b.bond)

    z_arr = np.array(z_list, dtype=float)
    e1_arr = np.array(e1_list, dtype=float)

    print(f"\n  Homonuclear bonds: {len(z_arr)}")
    for z, e1, lab in sorted(zip(z_list, e1_list, labels)):
        print(f"    Z={z:2d} ({lab:5s}): E₁ = {e1} kJ/mol")

    # Interpolate to uniform grid
    grid_size = 64
    x_grid, y_grid = interpolate_to_grid(z_arr, e1_arr, grid_size)

    return run_discovery(x_grid, y_grid, "E₁(Z) — energy along periodic table",
                         grid_size=grid_size)


# ============================================================
# Variant 2: α(π/σ)
# ============================================================
def variant2_alpha_vs_pi_sigma():
    """α as function of π/σ — the known strong correlation."""
    bonds = get_sp_bonds_with_pi_sigma()
    ps_arr = np.array([b["pi_sigma"] for b in bonds])
    alpha_arr = np.array([b["alpha"] for b in bonds])

    print(f"\n  Bonds with π/σ: {len(bonds)}")
    for b in sorted(bonds, key=lambda x: x["pi_sigma"]):
        print(f"    {b['bond']:5s}: π/σ = {b['pi_sigma']:.3f}, α = {b['alpha']:.3f}")

    # Linear regression for reference
    from scipy.stats import pearsonr
    r, p = pearsonr(ps_arr, alpha_arr)
    slope = np.polyfit(ps_arr, alpha_arr, 1)
    print(f"\n  Linear: α = {slope[0]:.3f}·(π/σ) + {slope[1]:.3f}, r = {r:.4f}")

    grid_size = 64
    x_grid, y_grid = interpolate_to_grid(ps_arr, alpha_arr, grid_size)

    return run_discovery(x_grid, y_grid, "α(π/σ) — alpha vs pi/sigma ratio",
                         grid_size=grid_size)


# ============================================================
# Variant 3: E₁(ΔEN)
# ============================================================
def variant3_e1_vs_delta_en():
    """E₁ as function of electronegativity difference."""
    bonds = get_sp_bonds_with_pi_sigma()
    den_arr = np.array([b["delta_en"] for b in bonds])
    e1_arr = np.array([b["E1"] for b in bonds])

    print(f"\n  Bonds: {len(bonds)}")
    for b in sorted(bonds, key=lambda x: x["delta_en"]):
        print(f"    {b['bond']:5s}: ΔEN = {b['delta_en']:.2f}, E₁ = {b['E1']} kJ/mol")

    grid_size = 64
    x_grid, y_grid = interpolate_to_grid(den_arr, e1_arr, grid_size)

    return run_discovery(x_grid, y_grid, "E₁(ΔEN) — energy vs electronegativity diff",
                         grid_size=grid_size)


# ============================================================
# Variant 4: π/σ along PCA₁
# ============================================================
def variant4_pi_sigma_pca():
    """π/σ along first principal component of 4 features."""
    bonds = get_sp_bonds_with_pi_sigma()

    # Build feature matrix: period, LP_sum, ΔEN, r_max
    features = np.array([
        [b["period"], b["lp_sum"], b["delta_en"], b["r_max"]]
        for b in bonds
    ], dtype=float)
    ps_arr = np.array([b["pi_sigma"] for b in bonds])

    # Standardize features
    feat_mean = features.mean(axis=0)
    feat_std = features.std(axis=0) + 1e-10
    feat_norm = (features - feat_mean) / feat_std

    # PCA
    from numpy.linalg import svd
    U, S, Vt = svd(feat_norm, full_matrices=False)
    pc1 = feat_norm @ Vt[0]  # first principal component

    print(f"\n  Bonds: {len(bonds)}")
    print(f"  PCA explained variance ratios: {(S**2 / (S**2).sum())[:3].round(3)}")
    print(f"  PC1 loadings: period={Vt[0,0]:.3f}, LP={Vt[0,1]:.3f}, "
          f"ΔEN={Vt[0,2]:.3f}, r_max={Vt[0,3]:.3f}")

    for b, t in sorted(zip(bonds, pc1), key=lambda x: x[1]):
        print(f"    {b['bond']:5s}: PC1 = {t:.3f}, π/σ = {b['pi_sigma']:.3f}")

    from scipy.stats import pearsonr
    r_pc1, _ = pearsonr(pc1, ps_arr)
    print(f"\n  Correlation π/σ vs PC1: r = {r_pc1:.4f}")

    grid_size = 64
    x_grid, y_grid = interpolate_to_grid(pc1, ps_arr, grid_size)

    return run_discovery(x_grid, y_grid, "π/σ(PC1) — pi/sigma along PCA axis",
                         grid_size=grid_size)


# ============================================================
# Summary
# ============================================================
def print_summary(results):
    print("\n" + "=" * 80)
    print("  ИТОГОВАЯ ТАБЛИЦА: RemizovNet × alphalaw")
    print("=" * 80)
    print(f"  {'Variant':<35s} {'R²':>6s} {'MSE':>10s} {'a_mean':>8s} "
          f"{'b_mean':>8s} {'c_mean':>8s} {'V_std':>8s} {'Verdict'}")
    print("-" * 105)

    for r in results:
        # Determine verdict
        if r["r2"] > 0.95 and r["V_std"] > 0.01:
            verdict = "*** WORKS ***"
        elif r["r2"] > 0.8:
            verdict = "* promising *"
        elif r["r2"] > 0.5:
            verdict = "marginal"
        else:
            verdict = "no fit"

        print(f"  {r['label'][:35]:<35s} {r['r2']:>6.3f} {r['mse']:>10.2e} "
              f"{r['a_mean']:>8.4f} {r['b_mean']:>8.4f} {r['c_mean']:>8.4f} "
              f"{r['V_std']:>8.4f} {verdict}")

    print()
    print("  Key:")
    print("    a = diffusion (smoothing); b = advection (drift); c = reaction (decay)")
    print("    V = c - b²/(4a) = effective potential (Schrodinger-like)")
    print("    V_std > 0.01: spatially-varying potential (non-trivial structure)")
    print("    R² = reconstruction quality of discovered ODE")
    print()

    # Physics interpretation
    print("  ФИЗИЧЕСКАЯ ИНТЕРПРЕТАЦИЯ:")
    print("  " + "-" * 60)
    for r in results:
        print(f"\n  {r['label']}:")
        a, b, c = r["a_mean"], r["b_mean"], r["c_mean"]
        if abs(a) < 0.01 and abs(b) < 0.01:
            print(f"    → Тривиальное ODE: {c:.3f}·y ≈ g  (масштабирование)")
        elif abs(a) > abs(b) and abs(a) > abs(c):
            print(f"    → Диффузионная динамика: y'' доминирует")
            print(f"    → Аналогия: теплопроводность / размытие")
        elif abs(b) > abs(a) and abs(b) > abs(c):
            print(f"    → Адвекционная динамика: y' доминирует")
            print(f"    → Аналогия: перенос / поток")
        else:
            print(f"    → Потенциальная динамика: c·y доминирует")
            print(f"    → Аналогия: стоячие волны / Шредингер")

        if r["V_std"] > 0.1:
            print(f"    → Потенциал V(x) сильно варьирует: V_std = {r['V_std']:.3f}")
            print(f"    → ЭТО ИНТЕРЕСНО: есть скрытая структура!")
        elif r["V_std"] > 0.01:
            print(f"    → Потенциал слабо варьирует: V_std = {r['V_std']:.3f}")
        else:
            print(f"    → Потенциал почти постоянный: V_std = {r['V_std']:.3f}")


def main():
    print("=" * 80)
    print("  RemizovNet × alphalaw: Поиск ODE в данных о химических связях")
    print("  RemizovNet solves: a(x)·y'' + b(x)·y' + c(x)·y = g(x)")
    print("=" * 80)

    np.random.seed(42)
    torch.manual_seed(42)

    results = []

    results.append(variant1_e1_along_z())
    results.append(variant2_alpha_vs_pi_sigma())
    results.append(variant3_e1_vs_delta_en())
    results.append(variant4_pi_sigma_pca())

    print_summary(results)


if __name__ == "__main__":
    main()
