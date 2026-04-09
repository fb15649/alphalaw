#!/usr/bin/env python3
"""
α-law expansion to d-block: using computed bond orders from Chen & Manz (2019).
Approach: For each M₂ with known bond order n and D₀, test whether D₀ scales
as E₁ × n^α across groups/periods.
"""
import math
import numpy as np
from scipy import stats

# Data from Chen & Manz (2019) RSC Advances, Table 1 + Table S2
# Columns: (element, period, group, valence_e, LP_sp, bond_order, D0_eV, re_Å)
# LP_sp: lone pairs in s/p-block sense (-1 for d-metals)
# For d-metals: RE = valence_e - 2*round(bond_order)

DIATOMICS = [
    # s/p block (reference)
    ("H",  1,  1,  1, 0,  0.938, 4.748, 0.741),
    ("Li", 2,  1,  1, 0,  0.925, 1.054, 2.673),
    ("B",  2, 13,  3, 0,  1.808, 3.005, 1.589),
    ("C",  2, 14,  4, 0,  2.727, 6.302, 1.243),
    ("N",  2, 15,  5, 1,  2.917, 9.756, 1.098),
    ("O",  2, 16,  6, 2,  1.962, 5.115, 1.208),
    ("F",  2, 17,  7, 3,  0.982, 1.605, 1.412),
    ("Na", 3,  1,  1, 0,  0.784, 0.732, 3.078),
    ("Al", 3, 13,  3, 0,  1.091, 1.459, 2.701),
    ("Si", 3, 14,  4, 0,  1.745, 3.100, 2.246),
    ("P",  3, 15,  5, 1,  2.555, 5.043, 1.893),
    ("S",  3, 16,  6, 2,  2.094, 4.363, 1.889),
    ("Cl", 3, 17,  7, 3,  1.357, 2.510, 1.988),
    ("Ge", 4, 14,  4, 0,  1.617, 2.535, 2.440),
    ("As", 4, 15,  5, 1,  2.305, 4.022, 2.103),
    ("Se", 4, 16,  6, 2,  1.870, 3.870, 2.166),
    ("Br", 4, 17,  7, 3,  1.264, 1.971, 2.281),
    ("Sn", 5, 14,  4, 0,  1.510, 1.925, 2.808),
    ("Sb", 5, 15,  5, 1,  2.124, 3.630, 2.709),
    ("Te", 5, 16,  6, 2,  1.758, 3.288, 2.747),
    ("I",  5, 17,  7, 3,  1.262, 1.544, 2.666),
    # 3d transition metals
    ("Sc", 4,  3,  3, -1, 2.326, 3.556, 3.572),
    ("Ti", 4,  4,  4, -1, 2.920, 4.693, 2.619),
    ("V",  4,  5,  5, -1, 3.231, 5.305, 2.551),
    ("Cr", 4,  6,  6, -1, 3.858, 4.038, 1.680),
    ("Mn", 4,  7,  7, -1, 0.463, 0.100, 3.400),
    ("Fe", 4,  8,  8, -1, 1.977, 4.281, 2.414),
    ("Co", 4,  9,  9, -1, 1.550, 3.435, 2.506),
    ("Ni", 4, 10, 10, -1, 1.265, 3.197, 2.477),
    ("Cu", 4, 11, 11, -1, 1.050, 2.040, 2.219),
    # 4d transition metals
    ("Y",  5,  3,  3, -1, 2.116, 3.254, 3.722),
    ("Zr", 5,  4,  4, -1, 3.291, 5.628, 3.154),
    ("Nb", 5,  5,  5, -1, 3.517, 5.918, 2.956),
    ("Mo", 5,  6,  6, -1, 4.120, 6.508, 2.088),
    ("Rh", 5,  9,  9, -1, 2.109, 3.725, 2.680),
    ("Pd", 5, 10, 10, -1, 1.571, 1.664, 2.501),
    ("Ag", 5, 11, 11, -1, 0.991, 1.662, 2.531),
    # 5d transition metals
    ("W",  6,  6,  6, -1, 3.194, 6.370, 2.235),
    ("Ir", 6,  9,  9, -1, 2.396, 4.056, 2.524),
    ("Pt", 6, 10, 10, -1, 1.801, 3.653, 2.532),
    ("Au", 6, 11, 11, -1, 1.171, 2.298, 2.472),
]


def compute_reserve(element, period, group, valence_e, LP_sp, bond_order):
    """Compute unified reserve metric."""
    if LP_sp >= 0:
        # s/p block: use classic LP
        return LP_sp
    else:
        # d-block: electrons not used in bonds / 2
        electrons_in_bonds = 2 * bond_order  # each bond uses 2 electrons from this atom
        reserve_e = max(0, valence_e - electrons_in_bonds)
        return reserve_e / 2  # convert to "pair equivalents"


def analyze():
    """Test whether D₀ = E₁ × n^α holds across elements, and whether RE predicts α."""
    print("=" * 90)
    print("D₀ vs BOND ORDER ANALYSIS (Chen & Manz 2019 data)")
    print("=" * 90)

    # For elements within the same GROUP, test log(D₀) = log(E₁) + α×log(n)
    # Group elements by their chemical group
    from collections import defaultdict
    groups = defaultdict(list)
    for elem, period, group, val_e, lp, bo, d0, re in DIATOMICS:
        if d0 > 0 and bo > 0.1:  # skip noble gases and Zn₂
            groups[group].append((elem, period, val_e, lp, bo, d0, re))

    # Within each group: regression log(D₀) vs log(n)
    print("\nWithin-group regression: log(D₀) = a + α×log(n)")
    print(f"{'Group':>6} {'Elements':30s} {'α':>7s} {'R²':>7s} {'p':>10s}")
    print("-" * 70)

    group_alphas = []
    for grp in sorted(groups.keys()):
        elems = groups[grp]
        if len(elems) < 3:
            continue
        log_n = [math.log(bo) for _, _, _, _, bo, _, _ in elems]
        log_d0 = [math.log(d0) for _, _, _, _, _, d0, _ in elems]
        slope, intercept, r, p, se = stats.linregress(log_n, log_d0)
        names = ", ".join(e[0] for e in elems)
        print(f"{grp:>6} {names:30s} {slope:7.3f} {r**2:7.3f} {p:10.4f}")
        group_alphas.append((grp, slope, r**2, p))

    # Cross-group: does RE predict bond order preference?
    print("\n" + "=" * 90)
    print("RESERVE ELECTRONS vs BOND ORDER & D₀")
    print("=" * 90)

    all_data = []
    print(f"\n{'Elem':>4} {'Per':>3} {'Grp':>3} {'Val_e':>5} {'BO':>6} {'D₀(eV)':>7} "
          f"{'RE':>5} {'Reserve':>7} {'D₀/BO':>7}")
    print("-" * 65)

    for elem, period, group, val_e, lp, bo, d0, re in DIATOMICS:
        if d0 <= 0 or bo <= 0.1:
            continue
        reserve = compute_reserve(elem, period, group, val_e, lp, bo)
        d0_per_bo = d0 / bo
        is_d = lp < 0
        all_data.append((elem, period, group, val_e, lp, bo, d0, re, reserve, d0_per_bo, is_d))
        marker = "d" if is_d else " "
        print(f"{elem:>4} {period:>3} {group:>3} {val_e:>5} {bo:>6.2f} {d0:>7.3f} "
              f"{val_e - 2*bo:>5.1f} {reserve:>7.2f} {d0_per_bo:>7.3f} {marker}")

    # Key test: do d-metals with high RE have higher D₀/BO (stronger per-bond)?
    d_metals = [(e, p, g, v, lp, bo, d0, re, res, dpbo, is_d)
                for e, p, g, v, lp, bo, d0, re, res, dpbo, is_d in all_data if is_d]

    if d_metals:
        print("\n" + "=" * 90)
        print("D-BLOCK SPECIFIC ANALYSIS")
        print("=" * 90)

        re_vals = [v - 2*bo for _, _, _, v, _, bo, _, _, _, _, _ in d_metals]  # raw RE
        d0_vals = [d0 for _, _, _, _, _, _, d0, _, _, _, _ in d_metals]
        bo_vals = [bo for _, _, _, _, _, bo, _, _, _, _, _ in d_metals]
        dpbo_vals = [dpbo for _, _, _, _, _, _, _, _, _, dpbo, _ in d_metals]
        res_vals = [res for _, _, _, _, _, _, _, _, res, _, _ in d_metals]

        rho1, p1 = stats.spearmanr(res_vals, d0_vals)
        print(f"  Spearman(reserve, D₀): ρ={rho1:.3f}, p={p1:.4f}")
        rho2, p2 = stats.spearmanr(res_vals, dpbo_vals)
        print(f"  Spearman(reserve, D₀/BO): ρ={rho2:.3f}, p={p2:.4f}")
        rho3, p3 = stats.spearmanr(bo_vals, d0_vals)
        print(f"  Spearman(bond_order, D₀): ρ={rho3:.3f}, p={p3:.4f}")

        # Inverted volcano test: early TMs (groups 3-6) have high BO,
        # late TMs (groups 8-11) have low BO. Is this because RE is used for bonds?
        print("\n  Inverted volcano pattern:")
        for e, p, g, v, lp, bo, d0, re, res, dpbo, _ in sorted(d_metals, key=lambda x: x[2]):
            re_raw = v - 2*bo
            print(f"    {e:>3} (group {g:>2}): val_e={v:>2}, BO={bo:.2f}, "
                  f"RE_raw={re_raw:+.1f}, D₀={d0:.3f} eV")

    # Test α-law across periods for same group
    print("\n" + "=" * 90)
    print("α-LAW TEST: SAME GROUP, DIFFERENT PERIODS")
    print("=" * 90)
    print("If D₀ = E₁ × n^α, then for same-group elements with different n:")
    print("α = [log(D₀_heavy/D₀_light)] / [log(n_heavy/n_light)]")

    for grp in sorted(groups.keys()):
        elems = sorted(groups[grp], key=lambda x: x[1])  # sort by period
        if len(elems) < 2:
            continue
        for i in range(len(elems) - 1):
            e1 = elems[i]
            for j in range(i+1, len(elems)):
                e2 = elems[j]
                if e1[4] > 0.1 and e2[4] > 0.1 and e1[5] > 0 and e2[5] > 0:
                    alpha_ij = math.log(e2[5] / e1[5]) / math.log(e2[4] / e1[4])
                    res1 = compute_reserve(e1[0], e1[1], grp, e1[2], e1[3], e1[4])
                    res2 = compute_reserve(e2[0], e2[1], grp, e2[2], e2[3], e2[4])
                    print(f"  {e1[0]:>3}₂ → {e2[0]:>3}₂ (group {grp:>2}): "
                          f"α={alpha_ij:+.3f}  "
                          f"(n: {e1[4]:.2f}→{e2[4]:.2f}, D₀: {e1[5]:.2f}→{e2[5]:.2f}, "
                          f"res: {res1:.1f}→{res2:.1f})")


if __name__ == "__main__":
    analyze()
