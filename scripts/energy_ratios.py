"""
Do E₁ ratios between bonds follow geometric patterns?

Analogy: like a string — if half the length → octave higher,
maybe bond energies relate to each other through characteristic ratios.
"""
import sys, os, math
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alphalaw.data import BONDS

PHI = (1 + math.sqrt(5)) / 2

# Characteristic numbers from geometry
CHAR_NUMBERS = {
    "1":       1.000,
    "φ-1":     PHI - 1,   # 0.618
    "1/√2":    1/math.sqrt(2),  # 0.707
    "√2/2":    math.sqrt(2)/2,  # same
    "3/4":     0.750,
    "4/5":     0.800,
    "5/6":     0.833,
    "√3/2":    math.sqrt(3)/2,  # 0.866
    "φ/2":     PHI/2,     # 0.809
    "1/φ":     1/PHI,     # 0.618 = φ-1
    "√2":      math.sqrt(2),  # 1.414
    "φ":       PHI,       # 1.618
    "√3":      math.sqrt(3),  # 1.732
    "2":       2.000,
    "3/2":     1.500,
    "4/3":     1.333,
    "5/4":     1.250,
    "5/3":     1.667,
    "2/φ":     2/PHI,     # 1.236
    "φ²":      PHI**2,    # 2.618
    "e":       math.e,    # 2.718
    "3":       3.000,
    "π":       math.pi,   # 3.14159
    "2φ":      2*PHI,     # 3.236
}


def main():
    # Collect E₁ for homonuclear bonds (cleanest comparison)
    homo = []
    for b in BONDS:
        if b.elem_A != b.elem_B or b.block == "d":
            continue
        if 1 not in b.energies:
            continue
        homo.append((b.bond, b.energies[1], b.period, b.LP_min))

    homo.sort(key=lambda x: x[1])

    print("=" * 80)
    print("ГОМОЯДЕРНЫЕ E₁: отношения между ними")
    print("=" * 80)
    print(f"\n  {'Связь':<8} {'E₁':>5} {'Период':>7} {'LP':>3}")
    print(f"  {'-'*30}")
    for bond, e1, per, lp in homo:
        print(f"  {bond:<8} {e1:>5} {per:>7} {lp:>3}")

    # All pairwise ratios (larger/smaller)
    print(f"\n  Все попарные отношения E₁(i)/E₁(j):")
    ratios = []
    for i in range(len(homo)):
        for j in range(i+1, len(homo)):
            b1, e1_1, _, _ = homo[i]
            b2, e1_2, _, _ = homo[j]
            r = e1_2 / e1_1  # larger / smaller (since sorted)
            ratios.append((f"{b2}/{b1}", r))

    ratios.sort(key=lambda x: x[1])

    print(f"\n  {'Пара':<15} {'Отношение':>10} {'Ближайшее число':>20} {'Δ':>8}")
    print(f"  {'-'*60}")

    for pair, ratio in ratios:
        # Find closest characteristic number
        best_name = ""
        best_dist = 999
        for name, val in CHAR_NUMBERS.items():
            d = abs(ratio - val)
            if d < best_dist:
                best_dist = d
                best_name = name
        print(f"  {pair:<15} {ratio:>10.4f} {best_name:>20} {best_dist:>8.4f}")

    # Histogram: how many ratios fall near each characteristic number?
    print(f"\n{'='*80}")
    print("КЛАСТЕРИЗАЦИЯ: сколько отношений рядом с каждым числом?")
    print(f"{'='*80}")

    window = 0.05
    for name, val in sorted(CHAR_NUMBERS.items(), key=lambda x: x[1]):
        near = sum(1 for _, r in ratios if abs(r - val) < window)
        if near > 0:
            which = [p for p, r in ratios if abs(r - val) < window]
            print(f"  {name:<8} = {val:.4f}: {near} отношений {which}")

    # Now: same analysis for HETERONUCLEAR
    print(f"\n{'='*80}")
    print("ГЕТЕРОЯДЕРНЫЕ: E₁ относительно гомоядерных E₁ партнёров")
    print(f"{'='*80}")

    homo_dict = {b.bond.split("-")[0]: b.energies[1]
                 for b in BONDS if b.elem_A == b.elem_B and 1 in b.energies and b.block != "d"}

    print(f"\n  {'Связь':<8} {'E₁(A-B)':>8} {'√(E₁A·E₁B)':>12} {'Отношение':>10} {'Ближ.':>8}")
    print(f"  {'-'*55}")

    for b in BONDS:
        if b.elem_A == b.elem_B or b.block == "d" or 1 not in b.energies:
            continue
        e_ab = b.energies[1]
        e_aa = homo_dict.get(b.elem_A)
        e_bb = homo_dict.get(b.elem_B)
        if e_aa is None or e_bb is None:
            continue
        geom_mean = math.sqrt(e_aa * e_bb)
        ratio = e_ab / geom_mean

        # Find closest
        best_name = ""
        best_dist = 999
        for name, val in CHAR_NUMBERS.items():
            d = abs(ratio - val)
            if d < best_dist:
                best_dist = d
                best_name = name

        print(f"  {b.bond:<8} {e_ab:>8} {geom_mean:>12.1f} {ratio:>10.3f} {best_name:>8} (Δ={best_dist:.3f})")

    # KEY TEST: is E₁(A-B) = geometric_mean(E₁(A-A), E₁(B-B))?
    print(f"\n{'='*80}")
    print("КЛЮЧЕВОЙ ТЕСТ: E₁(A-B) = √(E₁(A-A)·E₁(B-B))?")
    print(f"{'='*80}")

    errors_geom = []
    for b in BONDS:
        if b.elem_A == b.elem_B or b.block == "d" or 1 not in b.energies:
            continue
        e_ab = b.energies[1]
        e_aa = homo_dict.get(b.elem_A)
        e_bb = homo_dict.get(b.elem_B)
        if e_aa is None or e_bb is None:
            continue
        geom_mean = math.sqrt(e_aa * e_bb)
        errors_geom.append((b.bond, e_ab, geom_mean, e_ab/geom_mean))

    if errors_geom:
        ratios_gm = [r for _, _, _, r in errors_geom]
        avg_ratio = sum(ratios_gm) / len(ratios_gm)
        print(f"\n  Среднее E₁(A-B) / √(E₁(A-A)·E₁(B-B)) = {avg_ratio:.3f}")
        print(f"  Если = 1.000 → геометрическое среднее работает идеально")
        print(f"  Если > 1 → гетероядерные СИЛЬНЕЕ чем среднее (ионный вклад)")
        print(f"  Если < 1 → СЛАБЕЕ")

        above = sum(1 for r in ratios_gm if r > 1)
        print(f"\n  Выше 1 (ионное усиление): {above}/{len(ratios_gm)}")
        print(f"  Ниже 1: {len(ratios_gm) - above}/{len(ratios_gm)}")

        # Correlation with ΔEN
        EN = {"B":2.04,"C":2.55,"N":3.04,"O":3.44,"Al":1.61,"Si":1.90,
              "P":2.19,"S":2.58,"Ge":2.01,"As":2.18,"Se":2.55,"Te":2.10,"Sn":1.96}
        print(f"\n  Корреляция отношения с ΔEN:")
        pairs_den = []
        for bond, e_ab, gm, ratio in errors_geom:
            elems = bond.split("-")
            if len(elems) == 2 and elems[0] in EN and elems[1] in EN:
                den = abs(EN[elems[0]] - EN[elems[1]])
                pairs_den.append((bond, ratio, den))
                print(f"    {bond:<8} отношение={ratio:.3f} ΔEN={den:.2f}")

        if len(pairs_den) >= 3:
            rs = [r for _, r, _ in pairs_den]
            ds = [d for _, _, d in pairs_den]
            n = len(rs)
            mr = sum(rs)/n; md = sum(ds)/n
            cov = sum((r-mr)*(d-md) for r,d in zip(rs,ds))/n
            sr = (sum((r-mr)**2 for r in rs)/n)**0.5
            sd = (sum((d-md)**2 for d in ds)/n)**0.5
            corr = cov/(sr*sd) if sr*sd > 0 else 0
            print(f"\n  r(отношение, ΔEN) = {corr:.3f}")


if __name__ == "__main__":
    main()
