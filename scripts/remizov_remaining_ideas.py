"""
RemizovNet × alphalaw: Remaining 3 ideas from the original brainstorm.

Idea A: π/σ as 2D surface π/σ(LP_sum, period) → find PDE via ADI splitting
Idea B: E₁ matrix Z_A × Z_B → 2D grid → find PDE
Idea C: Kernel smoothing to bridge discrete→continuous gap

Previous result: direct 1D application = denoising artifact (R²=0.985 but no physics).
Now testing whether 2D/alternative approaches find real structure.
"""
import sys
import os

import numpy as np
import torch
from scipy.interpolate import griddata, RBFInterpolator
from scipy.stats import pearsonr

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alphalaw.data import BONDS
from remizov_net import EquationDiscoverer, ODECoefficients, ChernoffStep

# ============================================================
# Shared data
# ============================================================
EN = {
    "H": 2.20, "Li": 0.98, "Be": 1.57, "B": 2.04, "C": 2.55, "N": 3.04,
    "O": 3.44, "F": 3.98, "Na": 0.93, "Mg": 1.31, "Al": 1.61, "Si": 1.90,
    "P": 2.19, "S": 2.58, "Cl": 3.16, "Ge": 2.01, "As": 2.18,
    "Se": 2.55, "Br": 2.96, "Sn": 1.96, "Te": 2.10, "I": 2.66,
}

RADII = {
    "H": 31, "B": 84, "C": 76, "N": 71, "O": 66, "F": 57,
    "Al": 121, "Si": 111, "P": 107, "S": 105, "Cl": 102,
    "Ge": 120, "As": 119, "Se": 120, "Te": 138, "Sn": 139,
}

Z_MAP = {
    "H": 1, "Li": 3, "Be": 4, "B": 5, "C": 6, "N": 7, "O": 8, "F": 9,
    "Na": 11, "Mg": 12, "Al": 13, "Si": 14, "P": 15, "S": 16, "Cl": 17,
    "Ge": 32, "As": 33, "Se": 34, "Br": 35, "Sn": 50, "Te": 52, "I": 53,
}


def get_sp_bonds():
    """All s/p bonds with E₁, E₂, π/σ, α."""
    result = []
    for b in BONDS:
        if b.alpha is None or b.block == "d":
            continue
        if 1 not in b.energies or 2 not in b.energies:
            continue
        E1, E2 = b.energies[1], b.energies[2]
        en_a, en_b = EN.get(b.elem_A, 0), EN.get(b.elem_B, 0)
        lp_sum = b.LP_A + b.LP_B if b.LP_A >= 0 and b.LP_B >= 0 else 0
        r_max = max(RADII.get(b.elem_A, 100), RADII.get(b.elem_B, 100))
        z_a = Z_MAP.get(b.elem_A, 0)
        z_b = Z_MAP.get(b.elem_B, 0)
        result.append({
            "bond": b.bond, "alpha": b.alpha,
            "pi_sigma": (E2 - E1) / E1,
            "E1": E1, "E2": E2,
            "delta_en": abs(en_a - en_b),
            "r_max": r_max, "period": b.period, "lp_sum": lp_sum,
            "Z_A": min(z_a, z_b), "Z_B": max(z_a, z_b),
            "elem_A": b.elem_A, "elem_B": b.elem_B,
        })
    return result


def discover_1d(x_grid, y_grid, grid_size=64, epochs=2000, verbose=False):
    """1D ODE discovery. Returns dict with a, b, c, V, r2."""
    dx = (x_grid[-1] - x_grid[0]) / (len(x_grid) - 1)
    y_norm = y_grid / (np.max(np.abs(y_grid)) + 1e-10)

    g_data = np.zeros((30, grid_size))
    y_data = np.zeros((30, grid_size))
    for i in range(30):
        g_data[i] = y_norm + np.random.randn(grid_size) * 0.05
        y_data[i] = y_norm

    g_t = torch.tensor(g_data, dtype=torch.float32)
    y_t = torch.tensor(y_data, dtype=torch.float32)

    disc = EquationDiscoverer(
        grid_size=grid_size, n_steps=20, total_time=1.0,
        lr=1e-3, dx=float(dx),
    )
    result = disc.fit(g_t, y_t, epochs=epochs, tol=1e-8,
                      verbose=verbose, print_every=500)

    with torch.no_grad():
        y_pred = disc.model(g_t).numpy()
    mse = float(np.mean((y_pred - y_data) ** 2))
    r2 = 1 - mse / np.var(y_data) if np.var(y_data) > 0 else 0

    a = result.a.numpy()
    b_coef = result.b.numpy()
    c = result.c.numpy()
    V = c - b_coef**2 / (4 * a)

    return {"a": a, "b": b_coef, "c": c, "V": V, "r2": r2, "mse": mse,
            "equation": result.equation}


# ============================================================
# IDEA A: π/σ as 2D surface → ADI splitting
# ============================================================
def idea_a_2d_surface():
    print("\n" + "=" * 80)
    print("  ИДЕЯ A: π/σ как 2D поверхность π/σ(LP_sum, period)")
    print("  Метод: ADI splitting — RemizovNet вдоль каждой оси отдельно")
    print("=" * 80)

    bonds = get_sp_bonds()

    # Features: LP_sum (0,1,2,3,4) vs period (2,3,4,5)
    lp_arr = np.array([b["lp_sum"] for b in bonds], dtype=float)
    per_arr = np.array([b["period"] for b in bonds], dtype=float)
    ps_arr = np.array([b["pi_sigma"] for b in bonds])

    # Visualize the 2D scatter
    print(f"\n  Данные: {len(bonds)} связей в пространстве (LP_sum, period)")
    print(f"  LP_sum range: {lp_arr.min():.0f}..{lp_arr.max():.0f} "
          f"(unique: {sorted(set(lp_arr.astype(int)))})")
    print(f"  Period range: {per_arr.min():.0f}..{per_arr.max():.0f} "
          f"(unique: {sorted(set(per_arr.astype(int)))})")

    # Show occupancy of the 2D grid
    print(f"\n  Occupancy (LP_sum × period):")
    print(f"  {'':>10s}", end="")
    for p in [2, 3, 4, 5]:
        print(f" P={p:d} ", end="")
    print()
    for lp in [0, 1, 2, 3, 4]:
        print(f"  LP={lp:<6d}", end="")
        for p in [2, 3, 4, 5]:
            count = sum(1 for b in bonds if b["lp_sum"] == lp and b["period"] == p)
            if count > 0:
                avg_ps = np.mean([b["pi_sigma"] for b in bonds
                                  if b["lp_sum"] == lp and b["period"] == p])
                print(f" {count:d}({avg_ps:.2f})", end="")
            else:
                print(f"   --  ", end="")
        print()

    # Step 1: Interpolate onto regular 2D grid using RBF
    grid_lp = np.linspace(0, 4, 20)
    grid_per = np.linspace(2, 5, 15)
    LP_grid, PER_grid = np.meshgrid(grid_lp, grid_per)

    points = np.column_stack([lp_arr, per_arr])
    # RBF interpolation (handles scattered data well)
    rbf = RBFInterpolator(points, ps_arr, kernel="thin_plate_spline", smoothing=0.1)
    PS_surface = rbf(np.column_stack([LP_grid.ravel(), PER_grid.ravel()]))
    PS_surface = PS_surface.reshape(LP_grid.shape)

    print(f"\n  2D surface interpolated: {PS_surface.shape} = "
          f"{PS_surface.shape[0]} period × {PS_surface.shape[1]} LP")
    print(f"  π/σ range on surface: [{PS_surface.min():.3f}, {PS_surface.max():.3f}]")

    # Step 2: ADI splitting — discover ODE along each axis
    # Axis 1: Fix period, discover ODE along LP_sum
    print(f"\n  --- ODE вдоль оси LP_sum (при фиксированном period) ---")
    ode_lp_results = []
    for j, p_val in enumerate(grid_per[::4]):  # Sample 4 period slices
        row_idx = np.argmin(np.abs(grid_per - p_val))
        y_slice = PS_surface[row_idx, :]
        x_slice = grid_lp

        if len(x_slice) < 4:
            continue

        res = discover_1d(x_slice, y_slice, grid_size=len(x_slice),
                          epochs=1000, verbose=False)
        ode_lp_results.append({
            "period": p_val, "equation": res["equation"],
            "r2": res["r2"], "a": float(res["a"].mean()),
            "b": float(res["b"].mean()), "c": float(res["c"].mean()),
        })
        print(f"    Period≈{p_val:.1f}: {res['equation']}, R²={res['r2']:.3f}")

    # Axis 2: Fix LP_sum, discover ODE along period
    print(f"\n  --- ODE вдоль оси period (при фиксированном LP_sum) ---")
    ode_per_results = []
    for i, lp_val in enumerate(grid_lp[::5]):  # Sample 4 LP slices
        col_idx = np.argmin(np.abs(grid_lp - lp_val))
        y_slice = PS_surface[:, col_idx]
        x_slice = grid_per

        if len(x_slice) < 4:
            continue

        res = discover_1d(x_slice, y_slice, grid_size=len(x_slice),
                          epochs=1000, verbose=False)
        ode_per_results.append({
            "lp_sum": lp_val, "equation": res["equation"],
            "r2": res["r2"], "a": float(res["a"].mean()),
            "b": float(res["b"].mean()), "c": float(res["c"].mean()),
        })
        print(f"    LP≈{lp_val:.1f}: {res['equation']}, R²={res['r2']:.3f}")

    # Step 3: Check if ODE coefficients are stable across slices
    print(f"\n  Стабильность коэффициентов между срезами:")
    if ode_lp_results:
        a_vals = [r["a"] for r in ode_lp_results]
        c_vals = [r["c"] for r in ode_lp_results]
        print(f"    ODE(LP_sum): a = {np.mean(a_vals):.3f}±{np.std(a_vals):.3f}, "
              f"c = {np.mean(c_vals):.3f}±{np.std(c_vals):.3f}")
        cv_a = np.std(a_vals) / (abs(np.mean(a_vals)) + 1e-10)
        print(f"    CV(a) = {cv_a:.2f} ({'stable' if cv_a < 0.3 else 'UNSTABLE'})")

    if ode_per_results:
        a_vals = [r["a"] for r in ode_per_results]
        c_vals = [r["c"] for r in ode_per_results]
        print(f"    ODE(period): a = {np.mean(a_vals):.3f}±{np.std(a_vals):.3f}, "
              f"c = {np.mean(c_vals):.3f}±{np.std(c_vals):.3f}")
        cv_a = np.std(a_vals) / (abs(np.mean(a_vals)) + 1e-10)
        print(f"    CV(a) = {cv_a:.2f} ({'stable' if cv_a < 0.3 else 'UNSTABLE'})")

    # Step 4: Cross-validation — predict held-out points from surface
    print(f"\n  LOO validation на исходных 27 точках через 2D surface:")
    errors = []
    for i, b in enumerate(bonds):
        lp_i, per_i, ps_true = b["lp_sum"], b["period"], b["pi_sigma"]
        ps_pred = float(rbf(np.array([[lp_i, per_i]])))
        err = abs(ps_pred - ps_true) / abs(ps_true) * 100
        errors.append(err)
    print(f"    Mean error: {np.mean(errors):.1f}%")
    print(f"    Median error: {np.median(errors):.1f}%")
    print(f"    Max error: {np.max(errors):.1f}% ({bonds[np.argmax(errors)]['bond']})")

    # True LOO (remove point, refit RBF)
    print(f"\n  True LOO (refit RBF each time):")
    true_loo_errors = []
    for i in range(len(bonds)):
        pts_train = np.delete(points, i, axis=0)
        ps_train = np.delete(ps_arr, i)
        lp_i, per_i = bonds[i]["lp_sum"], bonds[i]["period"]

        rbf_loo = RBFInterpolator(pts_train, ps_train,
                                  kernel="thin_plate_spline", smoothing=0.1)
        ps_pred = float(rbf_loo(np.array([[lp_i, per_i]])))
        err = abs(ps_pred - bonds[i]["pi_sigma"]) / abs(bonds[i]["pi_sigma"]) * 100
        true_loo_errors.append(err)

    print(f"    Mean error: {np.mean(true_loo_errors):.1f}%")
    print(f"    Median error: {np.median(true_loo_errors):.1f}%")

    return {
        "ode_lp": ode_lp_results, "ode_per": ode_per_results,
        "loo_rbf": np.mean(true_loo_errors),
        "surface_shape": PS_surface.shape,
    }


# ============================================================
# IDEA B: E₁ matrix Z_A × Z_B → 2D PDE
# ============================================================
def idea_b_e1_matrix():
    print("\n" + "=" * 80)
    print("  ИДЕЯ B: E₁ матрица Z_A × Z_B → 2D PDE")
    print("=" * 80)

    # Collect ALL bonds (s/p + d, including single-bond-only)
    bond_data = []
    for b in BONDS:
        if 1 not in b.energies:
            continue
        z_a = Z_MAP.get(b.elem_A, 0)
        z_b = Z_MAP.get(b.elem_B, 0)
        if z_a == 0 or z_b == 0:
            continue
        bond_data.append({
            "bond": b.bond, "Z_A": min(z_a, z_b), "Z_B": max(z_a, z_b),
            "E1": b.energies[1], "block": b.block,
        })

    print(f"\n  Bonds with E₁: {len(bond_data)}")

    # Build sparse matrix
    all_z = sorted(set(
        [d["Z_A"] for d in bond_data] + [d["Z_B"] for d in bond_data]
    ))
    print(f"  Unique Z values: {len(all_z)}: {all_z}")

    z_to_idx = {z: i for i, z in enumerate(all_z)}
    n = len(all_z)
    matrix = np.full((n, n), np.nan)

    for d in bond_data:
        i = z_to_idx[d["Z_A"]]
        j = z_to_idx[d["Z_B"]]
        matrix[i, j] = d["E1"]
        matrix[j, i] = d["E1"]  # symmetric

    # Print matrix
    print(f"\n  E₁ matrix ({n}×{n}):")
    filled = np.sum(~np.isnan(matrix))
    total = n * n
    print(f"  Filled: {filled}/{total} = {filled/total*100:.1f}%")

    header = "      " + "".join(f" {z:>4d}" for z in all_z)
    print(f"\n{header}")
    for i, z_i in enumerate(all_z):
        row = f"  {z_i:>3d}  "
        for j in range(n):
            val = matrix[i, j]
            if np.isnan(val):
                row += "   · "
            else:
                row += f" {val:>4.0f}"
        print(row)

    # Step 1: Analyze row/column patterns via 1D ODE
    print(f"\n  --- ODE analysis: row slices (fixed Z_A, vary Z_B) ---")

    row_results = []
    for i, z_i in enumerate(all_z):
        valid = ~np.isnan(matrix[i, :])
        if valid.sum() < 4:
            continue

        x_vals = np.array(all_z)[valid].astype(float)
        y_vals = matrix[i, valid]

        # Need uniform grid — interpolate
        grid_size = max(20, int(x_vals[-1] - x_vals[0]))
        grid_size = min(grid_size, 64)
        x_grid = np.linspace(x_vals[0], x_vals[-1], grid_size)

        if len(x_vals) < 4:
            y_grid = np.interp(x_grid, x_vals, y_vals)
        else:
            from scipy.interpolate import CubicSpline
            cs = CubicSpline(x_vals, y_vals, bc_type="natural")
            y_grid = cs(x_grid)

        res = discover_1d(x_grid, y_grid, grid_size=grid_size,
                          epochs=1000, verbose=False)

        elem = next((k for k, v in Z_MAP.items() if v == z_i), f"Z={z_i}")
        row_results.append({
            "Z": z_i, "elem": elem,
            "n_bonds": int(valid.sum()),
            "equation": res["equation"], "r2": res["r2"],
            "a": float(res["a"].mean()),
            "c": float(res["c"].mean()),
        })
        print(f"    Z={z_i:2d} ({elem:>3s}, {valid.sum():2d} bonds): "
              f"{res['equation']}, R²={res['r2']:.3f}")

    # Step 2: Check symmetry — E₁(A,B) should equal E₁(B,A)
    print(f"\n  Symmetry check: matrix is symmetric by construction")

    # Step 3: Diagonal (homonuclear) vs off-diagonal analysis
    diag_vals = [matrix[i, i] for i in range(n) if not np.isnan(matrix[i, i])]
    offdiag_vals = [matrix[i, j] for i in range(n) for j in range(n)
                    if i != j and not np.isnan(matrix[i, j])]
    print(f"\n  Diagonal (homonuclear): {len(diag_vals)} bonds, "
          f"mean E₁ = {np.mean(diag_vals):.0f} kJ/mol")
    print(f"  Off-diagonal (hetero):  {len(offdiag_vals)//2} bonds, "
          f"mean E₁ = {np.mean(offdiag_vals):.0f} kJ/mol")

    # Step 4: Predict missing entries using row-wise ODE
    print(f"\n  Предсказание недостающих записей через row ODE:")
    predictions = []
    for i, z_i in enumerate(all_z):
        valid = ~np.isnan(matrix[i, :])
        if valid.sum() < 4:
            continue

        x_vals = np.array(all_z)[valid].astype(float)
        y_vals = matrix[i, valid]

        if len(x_vals) < 4:
            continue

        cs = CubicSpline(x_vals, y_vals, bc_type="natural")

        missing = np.where(np.isnan(matrix[i, :]))[0]
        for j in missing:
            z_j = all_z[j]
            if x_vals[0] <= z_j <= x_vals[-1]:  # interpolation only
                e1_pred = float(cs(z_j))
                elem_i = next((k for k, v in Z_MAP.items() if v == z_i), "?")
                elem_j = next((k for k, v in Z_MAP.items() if v == z_j), "?")
                predictions.append({
                    "bond": f"{elem_i}-{elem_j}",
                    "Z_A": z_i, "Z_B": z_j, "E1_pred": e1_pred,
                })

    if predictions:
        print(f"    {len(predictions)} predictions (interpolation only):")
        for p in predictions[:15]:
            print(f"    {p['bond']:>6s} (Z={p['Z_A']},{p['Z_B']}): "
                  f"E₁ ≈ {p['E1_pred']:.0f} kJ/mol")
        if len(predictions) > 15:
            print(f"    ... и ещё {len(predictions) - 15}")

    return {"matrix_shape": (n, n), "fill_pct": filled/total*100,
            "row_results": row_results, "predictions": predictions}


# ============================================================
# IDEA C: Kernel smoothing → continuous function → ODE
# ============================================================
def idea_c_kernel_smoothing():
    print("\n" + "=" * 80)
    print("  ИДЕЯ C: Kernel smoothing: discrete → continuous → ODE")
    print("  Ключевая идея: вместо интерполяции между точками,")
    print("  строим ПЛОТНОСТЬ в пространстве признаков и ищем ODE для неё.")
    print("=" * 80)

    bonds = get_sp_bonds()

    # Method 1: π/σ as density-weighted function along 1D "chemical distance"
    # Define chemical distance = composite of LP_sum, period, delta_en, r_max
    # weighted by their importance for π/σ

    # Use the known relationship: π/σ ≈ 0.699·α + 0.242 inverted
    # to find what DRIVES π/σ in feature space

    # Feature matrix
    features = np.array([
        [b["lp_sum"], b["period"], b["delta_en"], b["r_max"]]
        for b in bonds
    ], dtype=float)
    ps_arr = np.array([b["pi_sigma"] for b in bonds])

    # Kernel density estimation along each feature axis
    print(f"\n  Step 1: KDE π/σ along each feature axis")
    from scipy.stats import gaussian_kde

    feat_names = ["LP_sum", "period", "ΔEN", "r_max"]
    kde_results = []

    for k, name in enumerate(feat_names):
        x = features[:, k]

        # π/σ-weighted KDE: place Gaussians at each data point with weight=π/σ
        x_eval = np.linspace(x.min() - 0.5, x.max() + 0.5, 100)

        # Nadaraya-Watson: weighted average of π/σ with Gaussian kernel
        bandwidth = (x.max() - x.min()) / 5
        if bandwidth < 0.1:
            bandwidth = 0.1

        pi_sigma_smooth = np.zeros(len(x_eval))
        weights_smooth = np.zeros(len(x_eval))

        for i in range(len(x)):
            kernel = np.exp(-0.5 * ((x_eval - x[i]) / bandwidth) ** 2)
            pi_sigma_smooth += kernel * ps_arr[i]
            weights_smooth += kernel

        pi_sigma_smooth /= (weights_smooth + 1e-10)

        # Correlation of smoothed function with raw data
        ps_interp = np.interp(x, x_eval, pi_sigma_smooth)
        r_val, _ = pearsonr(ps_interp, ps_arr)

        print(f"    {name:>8s}: range [{x.min():.1f}, {x.max():.1f}], "
              f"r(smooth, raw) = {r_val:.3f}")

        kde_results.append({
            "name": name, "x_eval": x_eval, "ps_smooth": pi_sigma_smooth,
            "r": r_val, "bandwidth": bandwidth,
        })

    # Find best 1D feature for kernel-smoothed ODE
    best_kde = max(kde_results, key=lambda r: abs(r["r"]))
    print(f"\n  Best axis for smoothed π/σ: {best_kde['name']} (r = {best_kde['r']:.3f})")

    # Step 2: Discover ODE along best kernel-smoothed axis
    print(f"\n  Step 2: ODE discovery for kernel-smoothed π/σ({best_kde['name']})")
    x_eval = best_kde["x_eval"]
    ps_smooth = best_kde["ps_smooth"]

    # Ensure we have enough points and they're valid
    valid = np.isfinite(ps_smooth)
    x_eval = x_eval[valid]
    ps_smooth = ps_smooth[valid]

    grid_size = min(64, len(x_eval))
    # Subsample to grid_size if needed
    if len(x_eval) > grid_size:
        indices = np.linspace(0, len(x_eval) - 1, grid_size, dtype=int)
        x_eval = x_eval[indices]
        ps_smooth = ps_smooth[indices]

    res = discover_1d(x_eval, ps_smooth, grid_size=len(x_eval),
                      epochs=2000, verbose=True)

    print(f"\n  Discovered: {res['equation']}")
    print(f"  R² = {res['r2']:.4f}")
    V = res["V"]
    print(f"  V(x) std = {V.std():.4f}")

    # Step 3: Physical test — does the ODE predict raw data better than linear?
    print(f"\n  Step 3: Does kernel-smoothed ODE beat linear regression?")

    # Linear baseline
    k_idx = feat_names.index(best_kde["name"])
    x_raw = features[:, k_idx]
    slope, intercept = np.polyfit(x_raw, ps_arr, 1)
    ps_linear = slope * x_raw + intercept
    mse_linear = np.mean((ps_linear - ps_arr) ** 2)

    # ODE-smoothed prediction at raw points
    ps_ode = np.interp(x_raw, x_eval, ps_smooth)
    mse_ode = np.mean((ps_ode - ps_arr) ** 2)

    print(f"    Linear MSE:  {mse_linear:.4f}")
    print(f"    KDE+ODE MSE: {mse_ode:.4f}")
    print(f"    Improvement: {(1 - mse_ode / mse_linear) * 100:.1f}%")

    # Method 2: Multi-dimensional kernel → 1D path
    print(f"\n  Step 4: Optimal 1D path through 4D feature space")

    # Use Isomap-like approach: order bonds by their geodesic distance
    # Simplified: use the Nadaraya-Watson smoothed π/σ along
    # the composite axis t = w₁·LP + w₂·period + w₃·ΔEN + w₄·r_max
    # where w_i optimized for smoothness of π/σ(t)

    # Brute-force: try all single features + all pairs
    best_r2 = 0
    best_axis = None
    best_desc = ""

    for k1 in range(4):
        for k2 in range(k1, 4):
            if k1 == k2:
                # Single axis
                x = features[:, k1]
                desc = feat_names[k1]
            else:
                # Linear combination (try +/-)
                for sign in [1, -1]:
                    x = features[:, k1] + sign * features[:, k2]
                    desc = f"{feat_names[k1]} {'+' if sign > 0 else '-'} {feat_names[k2]}"

                    x_std = (x - x.mean()) / (x.std() + 1e-10)
                    r_val, _ = pearsonr(x_std, ps_arr)

                    if abs(r_val) > best_r2:
                        best_r2 = abs(r_val)
                        best_axis = x_std.copy()
                        best_desc = desc
                continue

            x_std = (x - x.mean()) / (x.std() + 1e-10)
            r_val, _ = pearsonr(x_std, ps_arr)

            if abs(r_val) > best_r2:
                best_r2 = abs(r_val)
                best_axis = x_std.copy()
                best_desc = desc

    # Also try LP_sum - period (physically motivated: LP opposes period)
    custom_axes = [
        ("LP - period/φ", features[:, 0] - features[:, 1] / 1.618),
        ("LP - period/2", features[:, 0] - features[:, 1] / 2),
        ("LP × (3-period)", features[:, 0] * (3 - features[:, 1])),
        ("(LP-ΔEN) / r_max", (features[:, 0] - features[:, 2]) /
         (features[:, 3] / 100)),
    ]

    for desc, x in custom_axes:
        x_std = (x - x.mean()) / (x.std() + 1e-10)
        r_val, _ = pearsonr(x_std, ps_arr)
        if abs(r_val) > best_r2:
            best_r2 = abs(r_val)
            best_axis = x_std.copy()
            best_desc = desc

    print(f"    Best 1D axis: '{best_desc}' with r = {best_r2:.4f}")

    # Kernel-smooth along best axis
    bandwidth = (best_axis.max() - best_axis.min()) / 5
    x_eval2 = np.linspace(best_axis.min() - 0.3, best_axis.max() + 0.3, 64)
    ps_smooth2 = np.zeros(64)
    w_smooth2 = np.zeros(64)
    for i in range(len(best_axis)):
        kernel = np.exp(-0.5 * ((x_eval2 - best_axis[i]) / bandwidth) ** 2)
        ps_smooth2 += kernel * ps_arr[i]
        w_smooth2 += kernel
    ps_smooth2 /= (w_smooth2 + 1e-10)

    res2 = discover_1d(x_eval2, ps_smooth2, grid_size=64, epochs=2000, verbose=False)
    print(f"    ODE for π/σ({best_desc}): {res2['equation']}")
    print(f"    R² = {res2['r2']:.4f}")

    return {
        "best_1d_axis": best_desc, "best_r": best_r2,
        "kde_r2_ode": res["r2"], "best_axis_r2_ode": res2["r2"],
    }


# ============================================================
# FINAL SUMMARY
# ============================================================
def final_summary(res_a, res_b, res_c):
    print("\n" + "=" * 80)
    print("  ИТОГОВЫЙ АНАЛИЗ: Оставшиеся 3 идеи")
    print("=" * 80)

    print(f"""
  ИДЕЯ A: π/σ как 2D поверхность (LP_sum × period)
  ─────────────────────────────────────────────────
  Матрица {res_a['surface_shape'][0]}×{res_a['surface_shape'][1]}, LOO RBF error = {res_a['loo_rbf']:.1f}%
  ADI: ODE вдоль LP и period — коэффициенты между срезами
  {"СТАБИЛЬНЫ → единое 2D PDE" if res_a.get("stable") else "НЕСТАБИЛЬНЫ → разные ODE для разных срезов"}

  ИДЕЯ B: E₁ матрица Z_A × Z_B
  ──────────────────────────────
  Матрица {res_b['matrix_shape'][0]}×{res_b['matrix_shape'][1]}, заполнена {res_b['fill_pct']:.0f}%
  Row-wise ODE: R² для элементов с 4+ связями
  {len(res_b['predictions'])} предсказаний для недостающих пар

  ИДЕЯ C: Kernel smoothing → ODE
  ───────────────────────────────
  Best 1D axis: '{res_c['best_1d_axis']}' (r = {res_c['best_r']:.3f})
  ODE along KDE: R² = {res_c['kde_r2_ode']:.3f}
  ODE along best axis: R² = {res_c['best_axis_r2_ode']:.3f}
""")

    print("  ОБЩИЙ ВЕРДИКТ:")
    print("  " + "─" * 60)
    print("""
  Фундаментальная проблема остаётся: RemizovNet решает
  ПРОСТРАНСТВЕННЫЕ ODE (непрерывная функция на сетке),
  а данные alphalaw — ДИСКРЕТНЫЕ точки в многомерном
  пространстве атомных свойств.

  Все попытки навести мост (интерполяция, kernel smoothing,
  ADI splitting) превращают задачу в "сглаживание шума",
  а не в "обнаружение физики".

  ГДЕ REMIZOV МОЖЕТ ПОМОЧЬ (реалистично):
  1. Если получить E₁ через DFT для ~100+ пар → достаточно
     для 2D PDE на сетке Z×Z
  2. Если применить к ДРУГОЙ задаче alphalaw: эволюция E(n)
     как функция bond order n — это 1D ODE с 3-6 точками.
     Мало, но хотя бы это НАСТОЯЩЕЕ ODE (не искусственное).

  ЧТО РАБОТАЕТ ДЛЯ ALPHALAW (без RemizovNet):
  • α = 0.699·(π/σ) + 0.242, r = 0.989 (линейная регрессия)
  • RBF interpolation π/σ(LP, period), LOO ~ {res_a['loo_rbf']:.0f}%
  • Физическая формула: π/σ = f(LP, period, ΔEN) через тороидную модель
""")


def main():
    print("=" * 80)
    print("  RemizovNet × alphalaw: Оставшиеся 3 идеи")
    print("=" * 80)

    np.random.seed(42)
    torch.manual_seed(42)

    res_a = idea_a_2d_surface()
    res_b = idea_b_e1_matrix()
    res_c = idea_c_kernel_smoothing()
    final_summary(res_a, res_b, res_c)


if __name__ == "__main__":
    main()
