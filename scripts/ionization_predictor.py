"""
Non-circular predictor: ionization energy instead of Pauling EN.

In toroid model: IE = energy to remove a circulation channel = ℏω.
Higher IE → faster toroid → stronger pull → greedier axis.

ΔIE should predict π/σ without circular logic (IE is measured independently).
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alphalaw.data import BONDS

# First ionization energies (kJ/mol) — from NIST, measured independently
IE = {
    "H": 1312, "He": 2372,
    "Li": 520, "Be": 900, "B": 801, "C": 1086, "N": 1402, "O": 1314,
    "F": 1681, "Ne": 2081,
    "Na": 496, "Mg": 738, "Al": 577, "Si": 786, "P": 1012, "S": 1000,
    "Cl": 1251, "Ar": 1521,
    "K": 419, "Ca": 590, "Ge": 762, "As": 947, "Se": 941, "Br": 1140,
    "Sn": 709, "Sb": 834, "Te": 869, "I": 1008,
    "Cr": 653, "Mo": 684, "W": 770, "Re": 760,
}

# Atomic radii (pm)
RADII = {
    "B": 84, "C": 76, "N": 71, "O": 66, "F": 57, "Al": 121, "Si": 111,
    "P": 107, "S": 105, "Cl": 102, "Ge": 120, "As": 119, "Se": 120,
    "Te": 138, "Sn": 139,
}

# Pauling EN for comparison
EN = {
    "B": 2.04, "C": 2.55, "N": 3.04, "O": 3.44, "F": 3.98,
    "Al": 1.61, "Si": 1.90, "P": 2.19, "S": 2.58, "Cl": 3.16,
    "Ge": 2.01, "As": 2.18, "Se": 2.55, "Sn": 1.96, "Te": 2.10,
}


def pearson(xs, ys):
    n = len(xs)
    mx = sum(xs)/n; my = sum(ys)/n
    cov = sum((x-mx)*(y-my) for x,y in zip(xs,ys))/n
    sx = (sum((x-mx)**2 for x in xs)/n)**0.5
    sy = (sum((y-my)**2 for y in ys)/n)**0.5
    return cov/(sx*sy) if sx*sy > 0 else 0


def main():
    # Build dataset
    rows = []
    for b in BONDS:
        if b.alpha is None or b.block == "d":
            continue
        if 1 not in b.energies or 2 not in b.energies:
            continue
        pi_sigma = (b.energies[2] - b.energies[1]) / b.energies[1]

        ie_a = IE.get(b.elem_A, 0)
        ie_b = IE.get(b.elem_B, 0)
        if ie_a == 0 or ie_b == 0:
            continue

        delta_ie = abs(ie_a - ie_b)
        ie_max = max(ie_a, ie_b)
        ie_min = min(ie_a, ie_b)
        ie_ratio = ie_max / ie_min
        ie_mean = (ie_a + ie_b) / 2
        ie_geom = math.sqrt(ie_a * ie_b)

        en_a = EN.get(b.elem_A, 0)
        en_b = EN.get(b.elem_B, 0)
        delta_en = abs(en_a - en_b)

        r_max = max(RADII.get(b.elem_A, 0), RADII.get(b.elem_B, 0))
        lp_sum = (b.LP_A + b.LP_B) if b.LP_A >= 0 and b.LP_B >= 0 else 0

        rows.append({
            "bond": b.bond, "alpha": b.alpha, "pi_sigma": pi_sigma,
            "delta_ie": delta_ie, "ie_ratio": ie_ratio, "ie_mean": ie_mean,
            "delta_en": delta_en, "r_max": r_max, "lp_sum": lp_sum,
            "E1": b.energies[1],
        })

    print("=" * 85)
    print(f"НЕКРУГОВОЙ ПРЕДИКТОР: энергия ионизации ({len(rows)} связей s/p)")
    print("=" * 85)

    # Correlations with π/σ
    ps = [r["pi_sigma"] for r in rows]

    predictors = [
        ("ΔEN (Полинг, круговой)", [r["delta_en"] for r in rows]),
        ("ΔIE (некруговой)", [r["delta_ie"] for r in rows]),
        ("IE_ratio (некруговой)", [r["ie_ratio"] for r in rows]),
        ("IE_mean", [r["ie_mean"] for r in rows]),
        ("r_max", [r["r_max"] for r in rows]),
        ("LP_sum", [r["lp_sum"] for r in rows]),
        ("E₁ (одинарная)", [r["E1"] for r in rows]),
    ]

    print(f"\n  Корреляции с π/σ:")
    print(f"  {'Предиктор':<35} {'r(π/σ)':>8} {'r(α)':>8}")
    print(f"  {'-'*55}")

    alphas = [r["alpha"] for r in rows]
    for name, vals in predictors:
        r_ps = pearson(vals, ps)
        r_a = pearson(vals, alphas)
        marker = " ← НЕКРУГОВОЙ" if "некруговой" in name.lower() else ""
        print(f"  {name:<35} {r_ps:>+8.3f} {r_a:>+8.3f}{marker}")

    # Multi-factor: LP_sum + ΔIE + r_max (all non-circular)
    print(f"\n{'='*85}")
    print("КОМБИНИРОВАННАЯ МОДЕЛЬ (только некруговые факторы)")
    print(f"{'='*85}")

    import numpy as np
    feature_sets = [
        ("ΔIE + LP_sum + r_max", ["delta_ie", "lp_sum", "r_max"]),
        ("IE_ratio + LP_sum + r_max", ["ie_ratio", "lp_sum", "r_max"]),
        ("ΔEN + LP_sum + r_max (для сравнения)", ["delta_en", "lp_sum", "r_max"]),
        ("ΔIE + LP_sum + IE_mean", ["delta_ie", "lp_sum", "ie_mean"]),
    ]

    for name, features in feature_sets:
        X = np.array([[r[f] for f in features] + [1] for r in rows])
        y = np.array([r["pi_sigma"] for r in rows])
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        y_pred = X @ beta
        ss_res = sum((y - y_pred)**2)
        ss_tot = sum((y - y.mean())**2)
        r2 = 1 - ss_res/ss_tot

        # Classification accuracy
        correct = sum(1 for yi, yp in zip(y, y_pred) if (yi > 1) == (yp > 1))
        n = len(y)

        print(f"\n  {name}:")
        print(f"    R² = {r2:.3f}, классификация = {correct}/{n} = {100*correct/n:.1f}%")

        # Coefficients
        for i, f in enumerate(features):
            print(f"    {f}: {beta[i]:+.5f}")
        print(f"    intercept: {beta[-1]:+.3f}")

    # Show the best non-circular model details
    print(f"\n{'='*85}")
    print("ДЕТАЛИ ЛУЧШЕЙ НЕКРУГОВОЙ МОДЕЛИ")
    print(f"{'='*85}")

    # IE_ratio + LP_sum + r_max
    features = ["ie_ratio", "lp_sum", "r_max"]
    X = np.array([[r[f] for f in features] + [1] for r in rows])
    y = np.array([r["pi_sigma"] for r in rows])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    y_pred = X @ beta

    print(f"\n  π/σ = {beta[0]:+.4f}·IE_ratio {beta[1]:+.4f}·LP_sum "
          f"{beta[2]:+.5f}·r_max {beta[3]:+.3f}")

    print(f"\n  {'Связь':<8} {'π/σ факт':>9} {'π/σ пред':>9} {'α':>6} "
          f"{'Факт':>6} {'Пред':>6} {'?':>3}")
    print(f"  {'-'*50}")
    for i, r in enumerate(sorted(rows, key=lambda x: x["pi_sigma"])):
        idx = rows.index(r)
        actual = "МОЛ" if r["alpha"] > 1 else "КРИСТ"
        pred = "МОЛ" if y_pred[idx] > 1 else "КРИСТ"
        ok = "✓" if actual == pred else "✗"
        print(f"  {r['bond']:<8} {r['pi_sigma']:>9.3f} {y_pred[idx]:>9.3f} "
              f"{r['alpha']:>6.3f} {actual:>6} {pred:>6} {ok:>3}")

    # Interpretation
    print(f"\n{'='*85}")
    print("ИНТЕРПРЕТАЦИЯ В МОДЕЛИ ТОРОИДА")
    print(f"{'='*85}")
    print(f"""
  IE (энергия ионизации) = энергия для удаления канала из тороида = ℏω.
  Высокое IE → быстрый тороид → сильнее перетягивает общий поток.

  IE_ratio = IE_max / IE_min = отношение "скоростей" двух тороидов.
  Если IE_ratio ≈ 1 → тороиды равны → поток делится поровну → бок получает долю.
  Если IE_ratio >> 1 → один тороид доминирует → ось забирает всё → бок пуст.

  Это ФИЗИЧЕСКИ то же что ΔEN, но измерено НЕЗАВИСИМО от энергий связей.
  IE получают из спектроскопии атомов, не из молекул. Нет круговой логики.

  LP_sum = число свободных каналов = ширина бокового потока.
  r_max = размер тороида = насколько бок "размазан" по площади.
    """)


if __name__ == "__main__":
    main()
