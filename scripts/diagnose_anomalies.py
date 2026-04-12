"""
Diagnose WHY some compact Period 2 bonds have α < 1
while others have α > 1.

Hypothesis: it's about the RATIO of π to σ, not just π strength.
If σ is already very strong (ionic character), π adds little RELATIVELY.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alphalaw.data import BONDS

# Pauling electronegativity
EN = {
    "H": 2.20, "Li": 0.98, "Be": 1.57, "B": 2.04, "C": 2.55, "N": 3.04,
    "O": 3.44, "F": 3.98, "Na": 0.93, "Mg": 1.31, "Al": 1.61, "Si": 1.90,
    "P": 2.19, "S": 2.58, "Cl": 3.16, "K": 0.82, "Ca": 1.00, "Sc": 1.36,
    "Ti": 1.54, "V": 1.63, "Cr": 1.66, "Mn": 1.55, "Fe": 1.83, "Co": 1.88,
    "Ni": 1.91, "Cu": 1.90, "Zn": 1.65, "Ga": 1.81, "Ge": 2.01, "As": 2.18,
    "Se": 2.55, "Br": 2.96, "Mo": 2.16, "Sn": 1.96, "Sb": 2.05, "Te": 2.10,
    "I": 2.66, "W": 2.36, "Re": 1.90,
}

# Covalent radii (pm)
RADII = {
    "H": 31, "B": 84, "C": 76, "N": 71, "O": 66, "F": 57,
    "Al": 121, "Si": 111, "P": 107, "S": 105, "Cl": 102,
    "Ge": 120, "As": 119, "Se": 120, "Te": 138, "Sn": 139,
    "Cr": 139, "Mo": 154, "W": 162, "Re": 151,
}


def main():
    print("=" * 90)
    print("ДИАГНОСТИКА: почему α ≠ f(компактность) точно?")
    print("=" * 90)

    rows = []
    for b in BONDS:
        if b.alpha is None or b.block == "d":
            continue
        if 1 not in b.energies or 2 not in b.energies:
            continue

        E1 = b.energies[1]
        E2 = b.energies[2]
        R2 = E2 / E1
        en_a = EN.get(b.elem_A, 0)
        en_b = EN.get(b.elem_B, 0)
        delta_EN = abs(en_a - en_b)
        r_max = max(RADII.get(b.elem_A, 0), RADII.get(b.elem_B, 0))
        lp_max = max(b.LP_A, b.LP_B) if b.LP_A >= 0 and b.LP_B >= 0 else -1
        lp_sum = (b.LP_A + b.LP_B) if b.LP_A >= 0 and b.LP_B >= 0 else -1

        rows.append((b.bond, b.alpha, R2, E1, E2, delta_EN, r_max,
                      b.LP_A, b.LP_B, lp_max, lp_sum, b.period))

    # Sort by alpha
    rows.sort(key=lambda r: r[1])

    print(f"\n{'Связь':<8} {'α':>6} {'R₂':>6} {'E₁':>5} {'E₂':>5} "
          f"{'ΔEN':>5} {'r_max':>5} {'LP_A':>4} {'LP_B':>4} {'LP∑':>4} {'Per':>4}")
    print("-" * 80)

    for (bond, alpha, R2, E1, E2, dEN, r_max,
         lp_a, lp_b, lp_max, lp_sum, period) in rows:
        print(f"{bond:<8} {alpha:>6.3f} {R2:>6.3f} {E1:>5} {E2:>5} "
              f"{dEN:>5.2f} {r_max:>5} {lp_a:>4} {lp_b:>4} {lp_sum:>4} {period:>4}")

    # Key analysis: α vs E1 (single bond strength)
    print("\n" + "=" * 90)
    print("КЛЮЧЕВОЙ ТЕСТ: α vs E₁ (сила одинарной связи)")
    print("=" * 90)

    alphas = [a for _, a, *_ in rows]
    e1s = [E1 for _, _, _, E1, *_ in rows]
    n = len(alphas)
    mean_a = sum(alphas) / n
    mean_e = sum(e1s) / n
    cov = sum((a - mean_a) * (e - mean_e) for a, e in zip(alphas, e1s)) / n
    std_a = (sum((a - mean_a)**2 for a in alphas) / n) ** 0.5
    std_e = (sum((e - mean_e)**2 for e in e1s) / n) ** 0.5
    r_corr = cov / (std_a * std_e) if std_a * std_e > 0 else 0
    print(f"\n  Pearson r(α, E₁) = {r_corr:.3f}")
    if r_corr < -0.3:
        print("  → Чем СИЛЬНЕЕ одинарная связь, тем НИЖЕ α!")

    # α vs ΔEN
    print("\n" + "=" * 90)
    print("α vs ΔEN (разность электроотрицательностей)")
    print("=" * 90)

    dens = [dEN for _, _, _, _, _, dEN, *_ in rows]
    cov2 = sum((a - mean_a) * (d - sum(dens)/n) for a, d in zip(alphas, dens)) / n
    std_d = (sum((d - sum(dens)/n)**2 for d in dens) / n) ** 0.5
    r_corr2 = cov2 / (std_a * std_d) if std_a * std_d > 0 else 0
    print(f"\n  Pearson r(α, ΔEN) = {r_corr2:.3f}")

    # α vs LP_sum
    print("\n" + "=" * 90)
    print("α vs LP_sum (суммарные неспаренные пары)")
    print("=" * 90)

    lps = [lps for _, _, _, _, _, _, _, _, _, _, lps, _ in rows if lps >= 0]
    alphas_lp = [a for (_, a, _, _, _, _, _, _, _, _, lps, _) in rows if lps >= 0]
    mean_lp = sum(lps) / len(lps)
    mean_alp = sum(alphas_lp) / len(alphas_lp)
    cov3 = sum((a - mean_alp) * (l - mean_lp) for a, l in zip(alphas_lp, lps)) / len(lps)
    std_lp = (sum((l - mean_lp)**2 for l in lps) / len(lps)) ** 0.5
    std_alp = (sum((a - mean_alp)**2 for a in alphas_lp) / len(alphas_lp)) ** 0.5
    r_corr3 = cov3 / (std_alp * std_lp) if std_alp * std_lp > 0 else 0
    print(f"\n  Pearson r(α, LP_sum) = {r_corr3:.3f}")

    # Now the key: multivariate — which combination predicts best?
    print("\n" + "=" * 90)
    print("КОМБИНИРОВАННЫЙ АНАЛИЗ: что ТОЧНО определяет α?")
    print("=" * 90)

    # Group by LP_sum and period
    groups = {}
    for (bond, alpha, R2, E1, E2, dEN, r_max,
         lp_a, lp_b, lp_max, lp_sum, period) in rows:
        key = (lp_sum, "Per2" if period == 2 else "Per3+")
        if key not in groups:
            groups[key] = []
        groups[key].append((bond, alpha, E1, dEN))

    for key in sorted(groups.keys()):
        lps, per = key
        items = groups[key]
        avg_a = sum(a for _, a, _, _ in items) / len(items)
        avg_e1 = sum(e for _, _, e, _ in items) / len(items)
        bonds = ", ".join(f"{b}({a:.2f})" for b, a, _, _ in items)
        print(f"\n  LP∑={lps}, {per}: средний α={avg_a:.3f}, средний E₁={avg_e1:.0f}")
        print(f"    {bonds}")

    # The smoking gun: Period 2, LP_sum=2 but different α
    print("\n" + "=" * 90)
    print("РАЗБОР АНОМАЛИЙ: Period 2, LP∑=2 — почему разный α?")
    print("=" * 90)

    for (bond, alpha, R2, E1, E2, dEN, r_max,
         lp_a, lp_b, lp_max, lp_sum, period) in rows:
        if period == 2 and lp_sum == 2:
            E_pi = E2 - E1  # energy of π-bond alone
            pi_ratio = E_pi / E1  # π relative to σ
            print(f"  {bond}: α={alpha:.3f}, E₁(σ)={E1}, E₂−E₁(π)={E_pi}, "
                  f"π/σ={pi_ratio:.3f}, ΔEN={dEN:.2f}")

    print("\n  Аналогично для LP∑=1:")
    for (bond, alpha, R2, E1, E2, dEN, r_max,
         lp_a, lp_b, lp_max, lp_sum, period) in rows:
        if period == 2 and lp_sum == 1:
            E_pi = E2 - E1
            pi_ratio = E_pi / E1
            print(f"  {bond}: α={alpha:.3f}, E₁(σ)={E1}, E₂−E₁(π)={E_pi}, "
                  f"π/σ={pi_ratio:.3f}, ΔEN={dEN:.2f}")

    print("\n  И для LP∑=0:")
    for (bond, alpha, R2, E1, E2, dEN, r_max,
         lp_a, lp_b, lp_max, lp_sum, period) in rows:
        if period == 2 and lp_sum == 0:
            E_pi = E2 - E1
            pi_ratio = E_pi / E1
            print(f"  {bond}: α={alpha:.3f}, E₁(σ)={E1}, E₂−E₁(π)={E_pi}, "
                  f"π/σ={pi_ratio:.3f}, ΔEN={dEN:.2f}")

    # FINAL: α vs π/σ ratio
    print("\n" + "=" * 90)
    print("ИТОГ: α vs π/σ (отношение π-вклада к σ)")
    print("=" * 90)

    pi_ratios = []
    for (bond, alpha, R2, E1, E2, dEN, r_max,
         lp_a, lp_b, lp_max, lp_sum, period) in rows:
        E_pi = E2 - E1
        pi_ratio = E_pi / E1
        pi_ratios.append((bond, alpha, pi_ratio, E1, E_pi, period))

    pi_ratios.sort(key=lambda x: x[2])

    print(f"\n{'Связь':<8} {'α':>6} {'π/σ':>6} {'E₁(σ)':>7} {'E₂-E₁(π)':>9} {'Пер':>4}")
    print("-" * 50)
    for bond, alpha, pr, E1, Epi, period in pi_ratios:
        marker = ""
        if pr >= 1.0:
            marker = " ◄ π≥σ"
        print(f"{bond:<8} {alpha:>6.3f} {pr:>6.3f} {E1:>7} {Epi:>9} {period:>4}{marker}")

    # Correlation
    as2 = [a for _, a, *_ in pi_ratios]
    prs = [pr for _, _, pr, *_ in pi_ratios]
    n2 = len(as2)
    ma = sum(as2)/n2
    mp = sum(prs)/n2
    cov4 = sum((a-ma)*(p-mp) for a,p in zip(as2, prs))/n2
    sa = (sum((a-ma)**2 for a in as2)/n2)**0.5
    sp = (sum((p-mp)**2 for p in prs)/n2)**0.5
    rc = cov4/(sa*sp) if sa*sp > 0 else 0
    print(f"\n  Pearson r(α, π/σ) = {rc:.3f}")


if __name__ == "__main__":
    main()
