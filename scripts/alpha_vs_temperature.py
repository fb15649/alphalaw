"""
Prediction test: α correlates with T_melt / T_boil / T_dissoc.

Hypothesis (vortex model):
  α > 1 (molecules): π-bonds sensitive to T → low T_dissoc (hundreds K)
  α < 1 (crystals):  σ-framework from many weak bonds → high T_melt (thousands K)

Data: CRC Handbook 97th ed., NIST WebBook
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alphalaw.data import BONDS

# ============================================================
# Temperature data (K) from CRC Handbook / NIST
# For homonuclear: T_melt and T_boil of the element
# For heteronuclear: T of the simplest binary compound
# T_dissoc: bond dissociation temp of diatomic (where available)
# ============================================================

# Homonuclear elements: (T_melt_K, T_boil_K, substance)
HOMO_TEMPS = {
    "C-C":   (3823, 4098, "C (diamond/graphite)"),   # graphite sublimes
    "Si-Si": (1687, 3538, "Si"),
    "Ge-Ge": (1211, 3106, "Ge"),
    "Sn-Sn": (505,  2875, "Sn"),
    "N-N":   (63,   77,   "N₂"),        # molecular gas
    "P-P":   (317,  554,  "P₄ (white)"), # molecular solid
    "O-O":   (54,   90,   "O₂"),         # molecular gas
    "S-S":   (388,  718,  "S₈"),         # molecular solid
    "As-As": (1090, 887,  "As (grey, sublimes)"),  # metalloid crystal
    "Se-Se": (494,  958,  "Se"),
    "Te-Te": (723,  1261, "Te"),
    "F-F":   (53,   85,   "F₂"),         # molecular gas
    "Cl-Cl": (172,  239,  "Cl₂"),        # molecular gas/liquid
    "Br-Br": (266,  332,  "Br₂"),        # molecular liquid
    "I-I":   (387,  457,  "I₂"),         # molecular solid
    "Cr-Cr": (2180, 2944, "Cr"),         # crystal metal
    "Mo-Mo": (2896, 4912, "Mo"),         # crystal metal
    "W-W":   (3695, 5828, "W"),          # crystal metal, highest T_melt
    "Re-Re": (3459, 5869, "Re"),         # crystal metal
}

# Heteronuclear: simplest compound
HETERO_TEMPS = {
    "C-N":  (195,  249,  "HCN"),         # molecular
    "C-O":  (195,  195,  "CO₂ (sublimes)"),  # molecular
    "N-O":  (109,  121,  "NO"),          # molecular gas
    "B-N":  (3246, None, "BN (hex, sublimes)"),  # crystal
    "B-O":  (723,  2133, "B₂O₃"),       # glass/crystal
    "Si-O": (1986, 2503, "SiO₂ (quartz)"),  # crystal
    "Si-N": (2173, None, "Si₃N₄ (decomp)"), # crystal
    "Al-O": (2345, 3250, "Al₂O₃"),      # crystal
    "C-S":  (162,  319,  "CS₂"),         # molecular liquid
    "C-P":  (None, None, "CP (rare)"),   # skip
    "Ge-O": (1389, None, "GeO₂"),       # crystal
    "B-C":  (2623, 3773, "B₄C"),        # crystal (superhard)
    "N-S":  (198,  263,  "S₂N₂/S₄N₄"),  # molecular
    "P-O":  (853,  1082, "P₄O₁₀"),      # molecular solid (cage)
    "S-O":  (200,  263,  "SO₂"),         # molecular gas
    "P-S":  (561,  789,  "P₄S₃"),       # molecular solid
    "Ti-O": (2116, 3245, "TiO₂ (rutile)"),  # crystal
    "Fe-C": (1538, None, "Fe₃C (decomp)"),  # crystal/intermetallic
    "W-C":  (3058, None, "WC (decomp)"),     # crystal (superhard)
}


def main():
    print("=" * 80)
    print("α vs Temperature: Testing Vortex Model Prediction")
    print("=" * 80)

    all_temps = {**HOMO_TEMPS, **HETERO_TEMPS}

    # Collect data points
    rows = []
    for b in BONDS:
        a = b.alpha
        if a is None:
            continue
        if b.bond not in all_temps:
            continue
        t_melt, t_boil, substance = all_temps[b.bond]
        if t_melt is None:
            continue
        rows.append((b.bond, a, t_melt, t_boil, substance, b.block))

    # Sort by alpha
    rows.sort(key=lambda r: r[1])

    # Print table
    print(f"\n{'Bond':<8} {'α':>6} {'T_melt(K)':>10} {'T_boil(K)':>10} {'Substance':<30} {'Block':<5}")
    print("-" * 80)

    mol_temps = []
    cryst_temps = []

    for bond, alpha, t_melt, t_boil, substance, block in rows:
        t_b_str = f"{t_boil:>10}" if t_boil else "       N/A"
        marker = "MOL" if alpha > 1 else "CRYST"
        print(f"{bond:<8} {alpha:>6.3f} {t_melt:>10} {t_b_str} {substance:<30} {marker}")

        if alpha > 1:
            mol_temps.append(t_melt)
        else:
            cryst_temps.append(t_melt)

    # Statistics
    print("\n" + "=" * 80)
    print("STATISTICS")
    print("=" * 80)

    if mol_temps:
        avg_mol = sum(mol_temps) / len(mol_temps)
        print(f"\nMolecules (α > 1):  n={len(mol_temps)}")
        print(f"  T_melt range: {min(mol_temps)} — {max(mol_temps)} K")
        print(f"  T_melt mean:  {avg_mol:.0f} K")

    if cryst_temps:
        avg_cryst = sum(cryst_temps) / len(cryst_temps)
        print(f"\nCrystals (α < 1):   n={len(cryst_temps)}")
        print(f"  T_melt range: {min(cryst_temps)} — {max(cryst_temps)} K")
        print(f"  T_melt mean:  {avg_cryst:.0f} K")

    if mol_temps and cryst_temps:
        separation = min(cryst_temps) > max(mol_temps)
        gap = min(cryst_temps) - max(mol_temps)
        print(f"\n  Gap: min(crystal) - max(molecule) = {min(cryst_temps)} - {max(mol_temps)} = {gap} K")
        print(f"  Clean separation: {'YES ✓' if separation else 'NO — overlap exists'}")

    # Correlation
    print("\n" + "=" * 80)
    print("CORRELATION: α vs T_melt")
    print("=" * 80)

    alphas = [r[1] for r in rows]
    temps = [r[2] for r in rows]
    n = len(alphas)

    mean_a = sum(alphas) / n
    mean_t = sum(temps) / n
    cov = sum((a - mean_a) * (t - mean_t) for a, t in zip(alphas, temps)) / n
    std_a = (sum((a - mean_a)**2 for a in alphas) / n) ** 0.5
    std_t = (sum((t - mean_t)**2 for t in temps) / n) ** 0.5
    r_pearson = cov / (std_a * std_t) if std_a * std_t > 0 else 0

    print(f"\n  Pearson r = {r_pearson:.3f}")
    print(f"  r² = {r_pearson**2:.3f}")
    if r_pearson < -0.5:
        print(f"  → STRONG negative correlation: higher α → lower T_melt ✓")
        print(f"  → Vortex model prediction CONFIRMED")
    elif r_pearson < -0.3:
        print(f"  → Moderate negative correlation")
    elif r_pearson < 0.3:
        print(f"  → Weak correlation")
    else:
        print(f"  → Positive correlation (unexpected)")

    # Spearman rank correlation (no scipy needed)
    print("\n  Spearman rank correlation (non-parametric):")
    ranked_a = sorted(range(n), key=lambda i: alphas[i])
    ranked_t = sorted(range(n), key=lambda i: temps[i])
    rank_a = [0] * n
    rank_t = [0] * n
    for rank, idx in enumerate(ranked_a):
        rank_a[idx] = rank
    for rank, idx in enumerate(ranked_t):
        rank_t[idx] = rank
    d_sq = sum((rank_a[i] - rank_t[i])**2 for i in range(n))
    r_spearman = 1 - 6 * d_sq / (n * (n**2 - 1))
    print(f"  Spearman ρ = {r_spearman:.3f}")

    # Check: are ALL molecules below a T threshold, ALL crystals above?
    print("\n" + "=" * 80)
    print("CLASSIFICATION TEST: can T_melt alone classify mol vs cryst?")
    print("=" * 80)

    for threshold in [400, 500, 600, 700, 800, 1000]:
        correct = 0
        total = 0
        for bond, alpha, t_melt, t_boil, substance, block in rows:
            total += 1
            if alpha > 1 and t_melt < threshold:
                correct += 1
            elif alpha <= 1 and t_melt >= threshold:
                correct += 1
        print(f"  T_threshold = {threshold:>5} K → accuracy = {correct}/{total} = {correct/total*100:.1f}%")


if __name__ == "__main__":
    main()
