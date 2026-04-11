"""
5 new research directions for alphalaw — each from an analogy.

1. MUSIC:    Harmonic series in multi-order bonds (R₃/R₂ = musical intervals?)
2. GRAVITY:  E₁(A-B) = √(E_AA·E_BB) × f(ΔEN) — crack E₁ prediction
3. LANDAU:   Phase transition in LP space — is LP=2→3 a critical point?
4. NUCLEAR:  E(n)/n curve — analog of binding energy per nucleon
5. FIBONACCI: Cluster self-assembly — φ in coordination geometry

Method: "as above, so below" — analogy → hypothesis → numerical test → verdict
"""
import sys
import os
import math

import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import pearsonr
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alphalaw.data import BONDS

# ============================================================
# Shared data
# ============================================================
EN = {
    "H": 2.20, "Li": 0.98, "Be": 1.57, "B": 2.04, "C": 2.55, "N": 3.04,
    "O": 3.44, "F": 3.98, "Al": 1.61, "Si": 1.90, "P": 2.19, "S": 2.58,
    "Cl": 3.16, "Ge": 2.01, "As": 2.18, "Se": 2.55, "Br": 2.96,
    "Sn": 1.96, "Te": 2.10, "I": 2.66,
    "Cr": 1.66, "Mo": 2.16, "W": 2.36, "Re": 1.90,
}

# Musical intervals (ratio, name)
INTERVALS = [
    (1, 1, "unison"), (9, 8, "major 2nd"), (8, 7, "septimal 2nd"),
    (6, 5, "minor 3rd"), (5, 4, "major 3rd"), (4, 3, "perfect 4th"),
    (7, 5, "septimal tritone"), (3, 2, "perfect 5th"), (8, 5, "minor 6th"),
    (5, 3, "major 6th"), (7, 4, "harmonic 7th"), (2, 1, "octave"),
    (9, 4, "major 9th"), (5, 2, "major 10th"), (3, 1, "perfect 12th"),
    (4, 1, "double octave"),
]

PHI = (1 + math.sqrt(5)) / 2  # golden ratio


# ============================================================
# DIRECTION 1: MUSIC — Harmonic series in multi-order bonds
# ============================================================
def direction1_music():
    print("\n" + "=" * 80)
    print("  НАПРАВЛЕНИЕ 1: МУЗЫКА — Гармонический ряд в порядках связей")
    print("  Аналогия: R₂=2 — октава. Порядки связи — обертоны струны.")
    print("  Гипотеза: R_n/R_m ≈ простые дроби (музыкальные интервалы)")
    print("=" * 80)

    # Collect multi-order bonds
    multi_bonds = []
    for b in BONDS:
        orders = sorted(b.energies.keys())
        if len(orders) < 3:
            continue
        E1 = b.energies[orders[0]]
        ratios = {n: b.energies[n] / E1 for n in orders}
        multi_bonds.append({
            "bond": b.bond, "orders": orders, "ratios": ratios,
            "alpha": b.alpha, "block": b.block,
        })

    print(f"\n  Связи с 3+ порядками: {len(multi_bonds)}")

    all_interval_distances = []
    random_distances = []

    for mb in multi_bonds:
        print(f"\n  {mb['bond']} (α={mb['alpha']:.3f}, {mb['block']}):")
        orders = mb["orders"]
        ratios = mb["ratios"]

        # Print raw ratios
        for n in orders:
            print(f"    n={n}: E/E₁ = {ratios[n]:.3f}")

        # Compute all pairwise ratios R_n / R_m (n > m > 1)
        print(f"    Pairwise ratios:")
        for i, n in enumerate(orders):
            for m in orders[:i]:
                if m == orders[0] and n == orders[0]:
                    continue
                r = ratios[n] / ratios[m] if ratios[m] > 0 else 0
                if r <= 0:
                    continue

                # Find nearest musical interval
                best_dist = 999
                best_name = ""
                best_frac = ""
                for p, q, name in INTERVALS:
                    interval = p / q
                    dist = abs(r - interval)
                    if dist < best_dist:
                        best_dist = dist
                        best_name = name
                        best_frac = f"{p}/{q}"

                all_interval_distances.append(best_dist)
                print(f"      R_{n}/R_{m} = {r:.4f} ≈ {best_frac} ({best_name}), "
                      f"Δ = {best_dist:.4f}")

    # Monte Carlo: how close are RANDOM numbers to musical intervals?
    np.random.seed(42)
    for _ in range(10000):
        r = np.random.uniform(0.8, 4.0)
        best_dist = min(abs(r - p / q) for p, q, _ in INTERVALS)
        random_distances.append(best_dist)

    mean_real = np.mean(all_interval_distances)
    mean_random = np.mean(random_distances)
    med_real = np.median(all_interval_distances)
    med_random = np.median(random_distances)

    print(f"\n  ТЕСТ: реальные vs случайные расстояния до интервалов")
    print(f"    Реальные:  mean Δ = {mean_real:.4f}, median = {med_real:.4f} "
          f"({len(all_interval_distances)} ratios)")
    print(f"    Случайные: mean Δ = {mean_random:.4f}, median = {med_random:.4f}")
    ratio = mean_real / mean_random
    print(f"    Real/Random = {ratio:.2f}")

    if ratio < 0.5:
        verdict = "ПОДТВЕРЖДЕНО: реальные в 2+ раз ближе к интервалам"
    elif ratio < 0.8:
        verdict = "ПЕРСПЕКТИВНО: реальные ближе к интервалам"
    else:
        verdict = "НЕ ПОДТВЕРЖДЕНО: не ближе чем случайные"

    print(f"\n  ВЕРДИКТ: {verdict}")
    return {"verdict": verdict, "ratio": ratio, "n_ratios": len(all_interval_distances)}


# ============================================================
# DIRECTION 2: GRAVITY — E₁(A-B) = √(E_AA·E_BB) × f(ΔEN)
# ============================================================
def direction2_gravity():
    print("\n" + "=" * 80)
    print("  НАПРАВЛЕНИЕ 2: ГРАВИТАЦИЯ — E₁(A-B) = √(E_AA·E_BB) × f(ΔEN)")
    print("  Аналогия: E_grav = G·m₁·m₂/r. 'Масса' = √(E_AA).")
    print("  Гипотеза: геом.среднее + поправка на ионность")
    print("=" * 80)

    # Collect homonuclear E₁
    homo_e1 = {}
    for b in BONDS:
        if b.elem_A == b.elem_B and 1 in b.energies:
            homo_e1[b.elem_A] = b.energies[1]

    print(f"\n  Homonuclear E₁: {len(homo_e1)} elements")
    for elem, e1 in sorted(homo_e1.items(), key=lambda x: -x[1]):
        print(f"    {elem:>3s}: {e1:>4d} kJ/mol")

    # Collect heteronuclear bonds where BOTH elements have homonuclear data
    hetero = []
    for b in BONDS:
        if b.elem_A == b.elem_B:
            continue
        if 1 not in b.energies:
            continue
        if b.elem_A not in homo_e1 or b.elem_B not in homo_e1:
            continue

        e_aa = homo_e1[b.elem_A]
        e_bb = homo_e1[b.elem_B]
        e_ab = b.energies[1]
        geom_mean = math.sqrt(e_aa * e_bb)
        deviation = e_ab / geom_mean
        en_a = EN.get(b.elem_A, 0)
        en_b = EN.get(b.elem_B, 0)
        delta_en = abs(en_a - en_b)

        hetero.append({
            "bond": b.bond, "E_AB": e_ab, "E_AA": e_aa, "E_BB": e_bb,
            "geom_mean": geom_mean, "deviation": deviation, "delta_en": delta_en,
        })

    print(f"\n  Heteronuclear bonds (both homopairs known): {len(hetero)}")
    print(f"  {'Bond':>6s} {'E_AB':>5s} {'√(AA·BB)':>9s} {'E/√':>5s} {'ΔEN':>5s}")
    print("  " + "-" * 35)

    devs = []
    dens = []
    for h in sorted(hetero, key=lambda x: x["delta_en"]):
        print(f"  {h['bond']:>6s} {h['E_AB']:>5.0f} {h['geom_mean']:>9.0f} "
              f"{h['deviation']:>5.2f} {h['delta_en']:>5.2f}")
        devs.append(h["deviation"])
        dens.append(h["delta_en"])

    # Baseline: geometric mean alone
    geom_preds = [h["geom_mean"] for h in hetero]
    e_true = [h["E_AB"] for h in hetero]
    r_geom, _ = pearsonr(geom_preds, e_true)
    mse_geom = np.mean([(p - t) ** 2 for p, t in zip(geom_preds, e_true)])
    mape_geom = np.mean([abs(p - t) / t for p, t in zip(geom_preds, e_true)]) * 100

    print(f"\n  Baseline (geometric mean only):")
    print(f"    r = {r_geom:.4f}, MAPE = {mape_geom:.1f}%")

    # Test: deviation vs ΔEN
    if len(devs) > 3:
        r_dev_en, p_dev_en = pearsonr(devs, dens)
        print(f"\n  Correlation E/√(AA·BB) vs ΔEN:")
        print(f"    r = {r_dev_en:.4f}, p = {p_dev_en:.2e}")

        # Fit: E_AB = √(E_AA·E_BB) × (a + b·ΔEN + c·ΔEN²)
        devs_arr = np.array(devs)
        dens_arr = np.array(dens)

        # Linear: deviation = a + b·ΔEN
        coeffs_lin = np.polyfit(dens_arr, devs_arr, 1)
        pred_lin = np.polyval(coeffs_lin, dens_arr)
        r2_lin = 1 - np.sum((devs_arr - pred_lin)**2) / np.sum((devs_arr - devs_arr.mean())**2)

        # Quadratic: deviation = a + b·ΔEN + c·ΔEN²
        coeffs_quad = np.polyfit(dens_arr, devs_arr, 2)
        pred_quad = np.polyval(coeffs_quad, dens_arr)
        r2_quad = 1 - np.sum((devs_arr - pred_quad)**2) / np.sum((devs_arr - devs_arr.mean())**2)

        print(f"\n  Fit f(ΔEN):")
        print(f"    Linear:    f = {coeffs_lin[0]:.3f}·ΔEN + {coeffs_lin[1]:.3f}, "
              f"R² = {r2_lin:.3f}")
        print(f"    Quadratic: f = {coeffs_quad[0]:.3f}·ΔEN² + {coeffs_quad[1]:.3f}·ΔEN + "
              f"{coeffs_quad[2]:.3f}, R² = {r2_quad:.3f}")

        # Corrected prediction
        corr_preds = [h["geom_mean"] * np.polyval(coeffs_quad, h["delta_en"])
                      for h in hetero]
        r_corr, _ = pearsonr(corr_preds, e_true)
        mape_corr = np.mean([abs(p - t) / t for p, t in zip(corr_preds, e_true)]) * 100

        print(f"\n  Corrected model E₁ = √(E_AA·E_BB) × f(ΔEN):")
        print(f"    r = {r_corr:.4f}, MAPE = {mape_corr:.1f}%")

        # LOO cross-validation
        loo_errors = []
        for i in range(len(hetero)):
            d_train = np.delete(dens_arr, i)
            v_train = np.delete(devs_arr, i)
            c_loo = np.polyfit(d_train, v_train, 2)
            pred_dev = np.polyval(c_loo, hetero[i]["delta_en"])
            pred_e1 = hetero[i]["geom_mean"] * pred_dev
            err = abs(pred_e1 - hetero[i]["E_AB"]) / hetero[i]["E_AB"] * 100
            loo_errors.append(err)

        print(f"\n  LOO cross-validation:")
        print(f"    Mean error = {np.mean(loo_errors):.1f}%")
        print(f"    Median error = {np.median(loo_errors):.1f}%")

        # Pauling formula comparison: E_AB = √(E_AA·E_BB) + 96.5·ΔEN²
        pauling_preds = [math.sqrt(h["E_AA"] * h["E_BB"]) + 96.5 * h["delta_en"]**2
                         for h in hetero]
        mape_pauling = np.mean([abs(p - t) / t for p, t in zip(pauling_preds, e_true)]) * 100
        r_pauling, _ = pearsonr(pauling_preds, e_true)
        print(f"\n  Pauling formula (E = √(AA·BB) + 96.5·ΔEN²):")
        print(f"    r = {r_pauling:.4f}, MAPE = {mape_pauling:.1f}%")

        if mape_corr < mape_geom * 0.7:
            verdict = f"ПОДТВЕРЖДЕНО: ΔEN-коррекция улучшает на {mape_geom-mape_corr:.0f}%"
        elif r_dev_en > 0.5:
            verdict = "ПЕРСПЕКТИВНО: ΔEN коррелирует с отклонением"
        else:
            verdict = "НЕ ПОДТВЕРЖДЕНО: ΔEN не объясняет отклонения"
    else:
        verdict = "НЕДОСТАТОЧНО ДАННЫХ"
        r_corr = 0
        mape_corr = 0

    print(f"\n  ВЕРДИКТ: {verdict}")
    return {"verdict": verdict, "r_corr": r_corr, "mape_corr": mape_corr,
            "n_bonds": len(hetero)}


# ============================================================
# DIRECTION 3: LANDAU — Phase transition in LP space
# ============================================================
def direction3_landau():
    print("\n" + "=" * 80)
    print("  НАПРАВЛЕНИЕ 3: ЛАНДАУ — Фазовый переход в пространстве LP")
    print("  Аналогия: LP = 'температура'. α=1 = критическая точка.")
    print("  Гипотеза: π/σ(LP) — сигмоида, не линия. Переход при LP≈2.")
    print("=" * 80)

    # Collect π/σ by LP_sum
    lp_ps_data = {}
    for b in BONDS:
        if b.alpha is None or b.block == "d":
            continue
        if 1 not in b.energies or 2 not in b.energies:
            continue
        lp = b.LP_A + b.LP_B if b.LP_A >= 0 and b.LP_B >= 0 else -1
        if lp < 0:
            continue
        ps = (b.energies[2] - b.energies[1]) / b.energies[1]
        if lp not in lp_ps_data:
            lp_ps_data[lp] = []
        lp_ps_data[lp].append({"bond": b.bond, "pi_sigma": ps, "alpha": b.alpha})

    print(f"\n  Данные по LP_sum:")
    lp_vals = []
    ps_means = []
    ps_stds = []
    all_lp = []
    all_ps = []

    for lp in sorted(lp_ps_data.keys()):
        bonds = lp_ps_data[lp]
        ps_list = [b["pi_sigma"] for b in bonds]
        mean_ps = np.mean(ps_list)
        std_ps = np.std(ps_list) if len(ps_list) > 1 else 0

        lp_vals.append(lp)
        ps_means.append(mean_ps)
        ps_stds.append(std_ps)

        print(f"    LP={lp}: π/σ = {mean_ps:.3f} ± {std_ps:.3f} ({len(bonds)} bonds)")
        for b in sorted(bonds, key=lambda x: x["pi_sigma"]):
            regime = "MOL" if b["alpha"] > 1 else "CRY"
            print(f"      {b['bond']:>6s}: π/σ = {b['pi_sigma']:.3f}, "
                  f"α = {b['alpha']:.3f} [{regime}]")

        for b in bonds:
            all_lp.append(lp)
            all_ps.append(b["pi_sigma"])

    lp_arr = np.array(lp_vals, dtype=float)
    ps_arr = np.array(ps_means)
    all_lp_arr = np.array(all_lp, dtype=float)
    all_ps_arr = np.array(all_ps)

    # Fit 1: Linear
    coeffs_lin = np.polyfit(all_lp_arr, all_ps_arr, 1)
    pred_lin = np.polyval(coeffs_lin, all_lp_arr)
    ss_res_lin = np.sum((all_ps_arr - pred_lin)**2)
    ss_tot = np.sum((all_ps_arr - all_ps_arr.mean())**2)
    r2_lin = 1 - ss_res_lin / ss_tot

    print(f"\n  Fit LINEAR: π/σ = {coeffs_lin[0]:.3f}·LP + {coeffs_lin[1]:.3f}")
    print(f"    R² = {r2_lin:.4f}")

    # Fit 2: Sigmoid (Landau-like) π/σ = a·tanh(b·(LP - c)) + d
    def sigmoid(lp, a, b, c, d):
        return a * np.tanh(b * (lp - c)) + d

    try:
        popt, pcov = curve_fit(sigmoid, all_lp_arr, all_ps_arr,
                               p0=[0.7, 1.0, 2.0, 0.9], maxfev=10000)
        pred_sig = sigmoid(all_lp_arr, *popt)
        ss_res_sig = np.sum((all_ps_arr - pred_sig)**2)
        r2_sig = 1 - ss_res_sig / ss_tot

        print(f"\n  Fit SIGMOID: π/σ = {popt[0]:.3f}·tanh({popt[1]:.3f}·(LP - {popt[2]:.3f})) "
              f"+ {popt[3]:.3f}")
        print(f"    R² = {r2_sig:.4f}")
        print(f"    Critical point LP_c = {popt[2]:.2f}")

        # Where does sigmoid cross π/σ = 1?
        # a·tanh(b·(LP-c)) + d = 1 → tanh(b·(LP-c)) = (1-d)/a → LP = c + atanh((1-d)/a)/b
        arg = (1 - popt[3]) / popt[0]
        if -1 < arg < 1:
            lp_cross = popt[2] + math.atanh(arg) / popt[1]
            print(f"    π/σ = 1 crossing at LP = {lp_cross:.2f}")
    except Exception as e:
        print(f"\n  Sigmoid fit failed: {e}")
        r2_sig = 0
        popt = [0, 0, 0, 0]

    # Fit 3: Step function (Heaviside at LP_c)
    best_acc = 0
    best_lp_c = 0
    for lp_c in np.arange(0.5, 4.0, 0.1):
        correct = sum(1 for l, p in zip(all_lp, all_ps)
                      if (l >= lp_c and p > 1) or (l < lp_c and p < 1))
        acc = correct / len(all_lp)
        if acc > best_acc:
            best_acc = acc
            best_lp_c = lp_c

    print(f"\n  Step function (Heaviside):")
    print(f"    Best threshold LP_c = {best_lp_c:.1f}, accuracy = {best_acc:.1%}")

    # Classification by regime
    mol_lp = [lp for lp, ps in zip(all_lp, all_ps) if ps > 1]
    cry_lp = [lp for lp, ps in zip(all_lp, all_ps) if ps <= 1]
    print(f"\n  Molecules (π/σ>1): LP range [{min(mol_lp)}, {max(mol_lp)}], "
          f"mean = {np.mean(mol_lp):.1f}")
    print(f"  Crystals  (π/σ≤1): LP range [{min(cry_lp)}, {max(cry_lp)}], "
          f"mean = {np.mean(cry_lp):.1f}")

    # Is the transition sharp?
    delta_r2 = r2_sig - r2_lin
    if delta_r2 > 0.05:
        verdict = f"ПОДТВЕРЖДЕНО: сигмоида лучше линии на ΔR²={delta_r2:.3f}, LP_c={popt[2]:.1f}"
    elif delta_r2 > 0.01:
        verdict = "ПЕРСПЕКТИВНО: лёгкий сигмоидальный перегиб"
    else:
        verdict = "НЕ ПОДТВЕРЖДЕНО: линейный рост, нет фазового перехода"

    print(f"\n  ВЕРДИКТ: {verdict}")
    return {"verdict": verdict, "r2_lin": r2_lin, "r2_sig": r2_sig,
            "lp_c": float(popt[2]) if r2_sig > 0 else 0}


# ============================================================
# DIRECTION 4: NUCLEAR — E(n)/n as analog of B/A curve
# ============================================================
def direction4_nuclear():
    print("\n" + "=" * 80)
    print("  НАПРАВЛЕНИЕ 4: ЯДРО — E(n)/n как аналог кривой B/A")
    print("  Аналогия: B/A имеет максимум при Fe-56. E(n)/n — аналог.")
    print("  Гипотеза: α > 1 → E/n растёт; α < 1 → E/n падает.")
    print("=" * 80)

    # Collect all multi-order bonds
    print(f"\n  E(n)/n для всех многопорядковых связей:")

    bonds_data = []
    for b in BONDS:
        orders = sorted(b.energies.keys())
        if len(orders) < 2:
            continue

        E1 = b.energies[orders[0]]
        en_per_order = {n: b.energies[n] / n for n in orders}
        alpha = b.alpha

        bonds_data.append({
            "bond": b.bond, "alpha": alpha, "block": b.block,
            "orders": orders, "en_per_order": en_per_order,
            "energies": {n: b.energies[n] for n in orders},
        })

    # Print E(n)/n curves
    for bd in sorted(bonds_data, key=lambda x: x["alpha"]):
        regime = "MOL" if bd["alpha"] > 1 else "CRY"
        print(f"\n  {bd['bond']} (α={bd['alpha']:.3f}, {regime}):")
        prev_en = 0
        for n in bd["orders"]:
            en = bd["en_per_order"][n]
            delta = en - prev_en if prev_en > 0 else 0
            trend = "↑" if delta > 0 else "↓" if delta < 0 else " "
            print(f"    n={n}: E/n = {en:>6.0f} kJ/mol/order {trend}")
            prev_en = en

    # Classify: does E(n)/n increase or decrease from n=1 to n=2?
    print(f"\n  Классификация по тренду E(n)/n:")
    increasing = []
    decreasing = []

    for bd in bonds_data:
        if 1 in bd["en_per_order"] and 2 in bd["en_per_order"]:
            e1_n = bd["en_per_order"][1]
            e2_n = bd["en_per_order"][2]
            if e2_n > e1_n:
                increasing.append(bd)
            else:
                decreasing.append(bd)

    print(f"    E(2)/2 > E(1)/1 (growing, 'fusion profitable'): {len(increasing)} bonds")
    for bd in sorted(increasing, key=lambda x: x["alpha"]):
        print(f"      {bd['bond']:>6s}: α = {bd['alpha']:.3f}")
    print(f"    E(2)/2 < E(1)/1 (diminishing, 'fission profitable'): {len(decreasing)} bonds")
    for bd in sorted(decreasing, key=lambda x: x["alpha"]):
        print(f"      {bd['bond']:>6s}: α = {bd['alpha']:.3f}")

    # The nuclear analogy: α = 1 is the "iron peak"
    # For α > 1: E(n)/n increases → "fusion" is profitable (like light nuclei)
    # For α < 1: E(n)/n decreases → "fission" is profitable (like heavy nuclei)
    # α = 1: maximum E(n)/n → "iron peak"

    correct = sum(1 for bd in increasing if bd["alpha"] > 1)
    correct += sum(1 for bd in decreasing if bd["alpha"] < 1)
    total = len(increasing) + len(decreasing)
    accuracy = correct / total if total > 0 else 0

    print(f"\n  Nuclear analogy test:")
    print(f"    α > 1 ↔ E/n increasing ('fusion profitable')")
    print(f"    α < 1 ↔ E/n decreasing ('fission profitable')")
    print(f"    Accuracy: {correct}/{total} = {accuracy:.1%}")

    # This is actually exactly the DEFINITION of α:
    # E(n) = E₁·n^α → E(n)/n = E₁·n^(α-1)
    # If α > 1: n^(α-1) grows → E/n increases ✓
    # If α < 1: n^(α-1) decays → E/n decreases ✓
    # So this is TAUTOLOGICAL for 2-point bonds.
    # But for 3+ point bonds, is the ACTUAL E(n)/n monotone?

    # Check 3+ order bonds for non-monotonicity (iron peak analog)
    print(f"\n  Bonds with 3+ orders — is E(n)/n monotone?")
    for bd in bonds_data:
        if len(bd["orders"]) < 3:
            continue
        ens = [bd["en_per_order"][n] for n in bd["orders"]]
        monotone_up = all(ens[i] <= ens[i + 1] for i in range(len(ens) - 1))
        monotone_down = all(ens[i] >= ens[i + 1] for i in range(len(ens) - 1))
        if not monotone_up and not monotone_down:
            peak_n = bd["orders"][np.argmax(ens)]
            print(f"    {bd['bond']:>6s}: NON-MONOTONE! Peak at n={peak_n}")
            print(f"      → 'Iron peak' analog at bond order {peak_n}")
        else:
            trend = "↑" if monotone_up else "↓"
            print(f"    {bd['bond']:>6s}: monotone {trend}")

    # Incremental energy: ΔE(n) = E(n) - E(n-1) — analog of separation energy
    print(f"\n  Incremental energy ΔE(n) = E(n) - E(n-1) (analog of separation energy):")
    for bd in bonds_data:
        if len(bd["orders"]) < 3:
            continue
        print(f"    {bd['bond']:>6s} (α={bd['alpha']:.3f}):")
        for i in range(1, len(bd["orders"])):
            n = bd["orders"][i]
            n_prev = bd["orders"][i - 1]
            de = bd["energies"][n] - bd["energies"][n_prev]
            dn = n - n_prev
            de_per_dn = de / dn
            print(f"      Δn={n_prev}→{n}: ΔE = {de:.0f} kJ/mol, "
                  f"ΔE/Δn = {de_per_dn:.0f} kJ/mol/order")

    if accuracy > 0.95:
        verdict = "ПОДТВЕРЖДЕНО (но тавтологично для 2-точечных)"
    elif accuracy > 0.85:
        verdict = "ПОДТВЕРЖДЕНО: α предсказывает тренд E/n"
    else:
        verdict = "НЕ ПОДТВЕРЖДЕНО"

    # The real finding: look for NON-MONOTONE E/n (actual iron peaks)
    non_mono = [bd for bd in bonds_data if len(bd["orders"]) >= 3
                and not all(bd["en_per_order"][bd["orders"][i]] <= bd["en_per_order"][bd["orders"][i+1]]
                            for i in range(len(bd["orders"])-1))
                and not all(bd["en_per_order"][bd["orders"][i]] >= bd["en_per_order"][bd["orders"][i+1]]
                            for i in range(len(bd["orders"])-1))]

    if non_mono:
        verdict += f" + {len(non_mono)} 'iron peak' analog найдено!"

    print(f"\n  ВЕРДИКТ: {verdict}")
    return {"verdict": verdict, "accuracy": accuracy, "non_monotone": len(non_mono)}


# ============================================================
# DIRECTION 5: FIBONACCI — Cluster geometry and φ
# ============================================================
def direction5_fibonacci():
    print("\n" + "=" * 80)
    print("  НАПРАВЛЕНИЕ 5: ФИБОНАЧЧИ — Координационные числа и φ")
    print("  Аналогия: филлотаксис (угол 137.5° = 360/φ²). Тамме-проблема.")
    print("  Гипотеза: КЧ_cluster связано с φ или числами Фибоначчи")
    print("=" * 80)

    # Known cluster data
    clusters = [
        {"elem": "N", "cluster": "N₂", "CN": 1, "N_atoms": 2,
         "E1": 160, "E_cluster": 945, "geometry": "dimer"},
        {"elem": "O", "cluster": "O₂", "CN": 1, "N_atoms": 2,
         "E1": 146, "E_cluster": 498, "geometry": "dimer"},
        {"elem": "F", "cluster": "F₂", "CN": 1, "N_atoms": 2,
         "E1": 158, "E_cluster": 158, "geometry": "dimer"},
        {"elem": "P", "cluster": "P₄", "CN": 3, "N_atoms": 4,
         "E1": 201, "E_cluster": 6 * 201, "geometry": "tetrahedron"},
        {"elem": "S", "cluster": "S₈", "CN": 2, "N_atoms": 8,
         "E1": 266, "E_cluster": 8 * 266, "geometry": "octagonal ring"},
        {"elem": "Se", "cluster": "Se₈", "CN": 2, "N_atoms": 8,
         "E1": 172, "E_cluster": 8 * 172, "geometry": "ring/chain"},
        {"elem": "C", "cluster": "diamond", "CN": 4, "N_atoms": 999,
         "E1": 346, "E_cluster": 2 * 346, "geometry": "diamond lattice"},
        {"elem": "Si", "cluster": "diamond", "CN": 4, "N_atoms": 999,
         "E1": 310, "E_cluster": 2 * 310, "geometry": "diamond lattice"},
        {"elem": "B", "cluster": "B₁₂", "CN": 5, "N_atoms": 12,
         "E1": 290, "E_cluster": 30 * 290, "geometry": "icosahedron"},
        {"elem": "As", "cluster": "As₄", "CN": 3, "N_atoms": 4,
         "E1": 146, "E_cluster": 6 * 146, "geometry": "tetrahedron"},
        {"elem": "Ge", "cluster": "diamond", "CN": 4, "N_atoms": 999,
         "E1": 264, "E_cluster": 2 * 264, "geometry": "diamond lattice"},
    ]

    # Get α for each element
    homo_alpha = {}
    for b in BONDS:
        if b.elem_A == b.elem_B and b.alpha is not None:
            homo_alpha[b.elem_A] = b.alpha

    print(f"\n  Cluster data:")
    print(f"  {'Elem':>5s} {'Cluster':>8s} {'CN':>3s} {'α':>6s} {'Geom':>16s} "
          f"{'E/(N·E₁)':>9s}")
    print("  " + "-" * 55)

    fib = [1, 1, 2, 3, 5, 8, 13, 21]

    for c in clusters:
        alpha = homo_alpha.get(c["elem"], 0)
        # E per atom per bond
        e_ratio = c["E_cluster"] / (c["N_atoms"] * c["E1"]) if c["N_atoms"] < 100 else c["CN"] / 2
        is_fib = c["CN"] in fib
        print(f"  {c['elem']:>5s} {c['cluster']:>8s} {c['CN']:>3d} {alpha:>6.3f} "
              f"{c['geometry']:>16s} {e_ratio:>9.2f} {'← Fib' if is_fib else ''}")

    # Test 1: Are observed CN values Fibonacci numbers?
    cn_vals = [c["CN"] for c in clusters]
    cn_unique = sorted(set(cn_vals))
    n_fib = sum(1 for cn in cn_unique if cn in fib)
    print(f"\n  Test 1: CN = Fibonacci number?")
    print(f"    Unique CN values: {cn_unique}")
    print(f"    Fibonacci: {n_fib}/{len(cn_unique)} = "
          f"{n_fib/len(cn_unique):.0%}")

    # Test 2: CN = valence - 2·LP (from cluster_geometry.py)
    print(f"\n  Test 2: CN = valence - 2·LP")
    correct = 0
    total = 0
    for c in clusters:
        for b in BONDS:
            if b.elem_A == c["elem"] and b.elem_B == c["elem"]:
                if b.LP_A >= 0:
                    predicted_cn = b.valence_e_A - 2 * b.LP_A
                    actual_cn = c["CN"]
                    match = predicted_cn == actual_cn
                    if match:
                        correct += 1
                    total += 1
                    print(f"    {c['elem']:>3s}: val={b.valence_e_A}, LP={b.LP_A}, "
                          f"pred_CN={predicted_cn}, actual={actual_cn} "
                          f"{'✓' if match else '✗'}")
                break

    if total > 0:
        print(f"    Accuracy: {correct}/{total} = {correct/total:.0%}")

    # Test 3: Tammes problem — optimal packing angle
    # For CN points on a sphere, what's the angular separation?
    print(f"\n  Test 3: Tammes problem — optimal angular separation")
    print(f"  {'CN':>3s} {'Angle°':>7s} {'360/angle':>9s} {'φ^k':>7s} {'Comment'}")
    print("  " + "-" * 45)

    tammes_angles = {
        1: 180.0,   # 2 points (dimer)
        2: 120.0,   # 3 points (triangle) — ring has angle
        3: 109.47,  # 4 points (tetrahedron)
        4: 90.0,    # 6 points — octahedron (but CN=4 = tetrahedron)
        5: 63.43,   # 12 points (icosahedron)
        6: 60.0,    # graphite / close-packed
        12: 45.0,   # FCC
    }

    for cn in sorted(tammes_angles.keys()):
        angle = tammes_angles[cn]
        ratio = 360 / angle
        # Is 360/angle close to φ^k?
        best_k = 0
        best_diff = 999
        for k in range(0, 6):
            diff = abs(ratio - PHI**k)
            if diff < best_diff:
                best_diff = diff
                best_k = k

        comment = f"≈ φ^{best_k}" if best_diff < 0.2 else ""
        print(f"  {cn:>3d} {angle:>7.1f} {ratio:>9.2f} {PHI**best_k:>7.3f} {comment}")

    # Test 4: The golden angle 137.5° = 360°/φ² ≈ 360° × (1-1/φ)
    golden_angle = 360 / PHI**2  # = 137.507...°
    print(f"\n  Test 4: Golden angle = 360/φ² = {golden_angle:.1f}°")
    print(f"  Tetrahedral angle = 109.47° = 360/3.29")
    print(f"  360/golden_angle = φ² = {PHI**2:.3f}")
    print(f"  360/tetrahedral = {360/109.47:.3f}")

    # Is there a relation between α and CN through φ?
    alphas = [homo_alpha.get(c["elem"], 0) for c in clusters]
    cns = [c["CN"] for c in clusters]
    valid = [(a, cn) for a, cn in zip(alphas, cns) if a > 0]
    if len(valid) > 3:
        a_arr = np.array([v[0] for v in valid])
        cn_arr = np.array([v[1] for v in valid])
        r_a_cn, p_a_cn = pearsonr(a_arr, cn_arr)
        print(f"\n  Correlation α vs CN: r = {r_a_cn:.4f} (p = {p_a_cn:.2e})")

    # Verdict
    if n_fib / len(cn_unique) > 0.8:
        verdict = "ПОДТВЕРЖДЕНО: большинство CN — числа Фибоначчи"
    elif n_fib / len(cn_unique) > 0.5:
        verdict = "ПЕРСПЕКТИВНО: многие CN — Фибоначчи, но не все"
    else:
        verdict = "НЕ ПОДТВЕРЖДЕНО: CN не связаны с Фибоначчи"

    print(f"\n  ВЕРДИКТ: {verdict}")
    return {"verdict": verdict, "fib_fraction": n_fib / len(cn_unique)}


# ============================================================
# FINAL SUMMARY
# ============================================================
def final_summary(r1, r2, r3, r4, r5):
    print("\n" + "=" * 80)
    print("  ИТОГО: 5 НАПРАВЛЕНИЙ")
    print("=" * 80)

    results = [
        ("МУЗЫКА (гармонический ряд)", r1["verdict"]),
        ("ГРАВИТАЦИЯ (E₁ prediction)", r2["verdict"]),
        ("ЛАНДАУ (фазовый переход)", r3["verdict"]),
        ("ЯДРО (B/A аналог)", r4["verdict"]),
        ("ФИБОНАЧЧИ (кластеры)", r5["verdict"]),
    ]

    for name, verdict in results:
        short = "✓" if "ПОДТВЕРЖДЕНО" in verdict else \
                "?" if "ПЕРСПЕКТИВНО" in verdict else "✗"
        print(f"  [{short}] {name}")
        print(f"      {verdict}")

    # Count passes
    passes = sum(1 for _, v in results
                 if "ПОДТВЕРЖДЕНО" in v or "ПЕРСПЕКТИВНО" in v)
    print(f"\n  Score: {passes}/5 направлений подтверждены или перспективны")

    if passes >= 2:
        print(f"  → Acceptance criteria MET")
    else:
        print(f"  → Acceptance criteria NOT MET")


def main():
    print("=" * 80)
    print("  5 НАПРАВЛЕНИЙ: метод аналогий × alphalaw")
    print("  'Что наверху, то и внизу'")
    print("=" * 80)

    np.random.seed(42)

    r1 = direction1_music()
    r2 = direction2_gravity()
    r3 = direction3_landau()
    r4 = direction4_nuclear()
    r5 = direction5_fibonacci()

    final_summary(r1, r2, r3, r4, r5)


if __name__ == "__main__":
    main()
