"""
Prediction test: α inversely correlates with coordination number (CN).

Hypothesis (introvert/extravert analogy):
  α > 1 → few strong bonds (CN=1-2), self-sufficient
  α < 1 → many weak bonds (CN=4-12), needs neighbors

Data: CN from crystal structures (CRC Handbook, ICSD)
For molecules: CN = number of bonds in the simplest stable form
For crystals: CN = coordination number in the standard crystal structure
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alphalaw.data import BONDS

# CN data: coordination number in the most common/stable form
# For homonuclear: CN in the element's standard state
# For heteronuclear: CN of the central atom in the simplest binary compound
# Source: CRC Handbook, crystal structure databases
CN_DATA = {
    # Homonuclear s/p-block
    "C-C":   (4, "diamond: tetrahedral"),      # graphite=3, diamond=4
    "Si-Si": (4, "Si: diamond cubic"),
    "Ge-Ge": (4, "Ge: diamond cubic"),
    "Sn-Sn": (4, "β-Sn: distorted, effectively 4+2"),
    "N-N":   (1, "N₂: diatomic molecule"),
    "P-P":   (3, "P₄: tetrahedral cage, each P bonded to 3"),
    "O-O":   (1, "O₂: diatomic molecule"),
    "S-S":   (2, "S₈: ring, each S bonded to 2"),
    "As-As": (3, "As: puckered layers, each As bonded to 3"),
    "Se-Se": (2, "Se: helical chains, each Se bonded to 2"),
    "Te-Te": (2, "Te: helical chains + 4 secondary → effectively 2+4"),
    "F-F":   (1, "F₂: diatomic molecule"),
    "Cl-Cl": (1, "Cl₂: diatomic molecule"),
    "Br-Br": (1, "Br₂: diatomic molecule"),
    "I-I":   (1, "I₂: diatomic molecule"),

    # Heteronuclear s/p-block (CN of central/less electronegative atom)
    "C-N":   (2, "HCN: linear, C bonded to 2"),
    "C-O":   (2, "CO₂: linear, C bonded to 2"),
    "N-O":   (1, "NO: diatomic"),
    "B-N":   (3, "h-BN: planar, each atom bonded to 3"),
    "B-O":   (3, "B₂O₃: trigonal planar BO₃ units"),
    "Si-O":  (4, "SiO₂: tetrahedral SiO₄"),
    "Si-N":  (4, "Si₃N₄: tetrahedral SiN₄"),
    "Al-O":  (6, "Al₂O₃: octahedral AlO₆"),
    "C-S":   (2, "CS₂: linear, C bonded to 2"),
    "C-P":   (1, "CP: diatomic radical"),
    "Ge-O":  (4, "GeO₂: tetrahedral (quartz-type) or 6 (rutile-type)"),
    "B-C":   (6, "B₄C: icosahedral boron clusters"),
    "N-S":   (2, "S₂N₂: ring, alternating S-N"),
    "P-O":   (4, "P₄O₁₀: tetrahedral PO₄ cages"),
    "S-O":   (2, "SO₂: bent, S bonded to 2 O"),
    "P-S":   (3, "P₄S₃: cage, P bonded to 3"),
    "Ti-O":  (6, "TiO₂: octahedral TiO₆"),
    "Fe-C":  (6, "Fe₃C: Fe in trigonal prismatic C₆"),
    "W-C":   (6, "WC: hexagonal, W in trigonal prismatic C₆"),

    # d-block homonuclear
    "Cr-Cr": (8, "Cr: BCC"),
    "Mo-Mo": (8, "Mo: BCC"),
    "W-W":   (8, "W: BCC"),
    "Re-Re": (12, "Re: HCP"),
}


def main():
    print("=" * 80)
    print("α vs Coordination Number (CN): Introvert/Extravert Test")
    print("=" * 80)

    rows = []
    for b in BONDS:
        a = b.alpha
        if a is None:
            continue
        if b.bond not in CN_DATA:
            continue
        cn, desc = CN_DATA[b.bond]
        rows.append((b.bond, a, cn, desc, b.block))

    rows.sort(key=lambda r: r[1])

    print(f"\n{'Bond':<8} {'α':>6} {'CN':>4} {'Description':<45} {'Type':<6}")
    print("-" * 80)

    cn_by_type = {"mol": [], "cryst": []}
    all_alphas = []
    all_cns = []

    for bond, alpha, cn, desc, block in rows:
        typ = "MOL" if alpha > 1 else "CRYST"
        print(f"{bond:<8} {alpha:>6.3f} {cn:>4} {desc:<45} {typ}")
        all_alphas.append(alpha)
        all_cns.append(cn)
        if alpha > 1:
            cn_by_type["mol"].append(cn)
        else:
            cn_by_type["cryst"].append(cn)

    # Statistics
    print("\n" + "=" * 80)
    print("STATISTICS")
    print("=" * 80)

    mol_cn = cn_by_type["mol"]
    cryst_cn = cn_by_type["cryst"]

    if mol_cn:
        print(f"\nMolecules (α > 1):  n={len(mol_cn)}")
        print(f"  CN range: {min(mol_cn)} — {max(mol_cn)}")
        print(f"  CN mean:  {sum(mol_cn)/len(mol_cn):.1f}")

    if cryst_cn:
        print(f"\nCrystals (α < 1):   n={len(cryst_cn)}")
        print(f"  CN range: {min(cryst_cn)} — {max(cryst_cn)}")
        print(f"  CN mean:  {sum(cryst_cn)/len(cryst_cn):.1f}")

    # Correlation
    print("\n" + "=" * 80)
    print("CORRELATION: α vs CN")
    print("=" * 80)

    n = len(all_alphas)
    mean_a = sum(all_alphas) / n
    mean_cn = sum(all_cns) / n
    cov = sum((a - mean_a) * (c - mean_cn) for a, c in zip(all_alphas, all_cns)) / n
    std_a = (sum((a - mean_a)**2 for a in all_alphas) / n) ** 0.5
    std_cn = (sum((c - mean_cn)**2 for c in all_cns) / n) ** 0.5
    r_pearson = cov / (std_a * std_cn) if std_a * std_cn > 0 else 0

    print(f"\n  Pearson r = {r_pearson:.3f}")
    print(f"  r² = {r_pearson**2:.3f}")

    # Spearman
    ranked_a = sorted(range(n), key=lambda i: all_alphas[i])
    ranked_cn = sorted(range(n), key=lambda i: all_cns[i])
    rank_a = [0] * n
    rank_cn = [0] * n
    for rank, idx in enumerate(ranked_a):
        rank_a[idx] = rank
    for rank, idx in enumerate(ranked_cn):
        rank_cn[idx] = rank
    d_sq = sum((rank_a[i] - rank_cn[i])**2 for i in range(n))
    r_spearman = 1 - 6 * d_sq / (n * (n**2 - 1))
    print(f"  Spearman ρ = {r_spearman:.3f}")

    if r_pearson < -0.5:
        print(f"\n  → STRONG negative correlation ✓")
        print(f"  → Higher α = fewer bonds (introvert), lower α = more bonds (extravert)")
    elif r_pearson < -0.3:
        print(f"\n  → Moderate negative correlation")

    # CN distribution by α bins
    print("\n" + "=" * 80)
    print("CN DISTRIBUTION BY α BINS")
    print("=" * 80)

    bins = [
        ("α > 1.5 (strong molecules)", 1.5, 99),
        ("1.0 < α ≤ 1.5 (weak molecules)", 1.0, 1.5),
        ("0.7 < α ≤ 1.0 (weak crystals)", 0.7, 1.0),
        ("α ≤ 0.7 (strong crystals)", 0, 0.7),
    ]

    for label, lo, hi in bins:
        cns = [cn for _, alpha, cn, _, _ in rows if lo < alpha <= hi]
        if cns:
            print(f"\n  {label}:")
            print(f"    CN values: {sorted(cns)}")
            print(f"    CN mean: {sum(cns)/len(cns):.1f}, median: {sorted(cns)[len(cns)//2]}")

    # Perfect classification test
    print("\n" + "=" * 80)
    print("CLASSIFICATION: CN threshold for mol vs cryst")
    print("=" * 80)

    for threshold in [1, 2, 3]:
        correct = sum(
            1 for _, alpha, cn, _, _ in rows
            if (alpha > 1 and cn <= threshold) or (alpha <= 1 and cn > threshold)
        )
        total = len(rows)
        print(f"  CN ≤ {threshold} → mol, CN > {threshold} → cryst: {correct}/{total} = {correct/total*100:.1f}%")


if __name__ == "__main__":
    main()
