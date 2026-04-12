"""
Extended bond energy dataset — compiled from multiple sources.

Sources:
  1. CRC Handbook 97th ed. (already in alphalaw/data.py)
  2. WiredChemist.com (comprehensive table, cross-referenced with CRC)
  3. MSU Chemistry (Reusch) — kcal/mol converted to kJ/mol
  4. Chemistry LibreTexts — kJ/mol
  5. Huber & Herzberg 1979 — diatomic spectroscopic data
  6. Active Thermochemical Tables (ATcT) — high-precision D0
  7. NIST WebBook — diatomic dissociation energies

All energies in kJ/mol. Where sources disagree, CRC value preferred.
Conversion: 1 kcal/mol = 4.184 kJ/mol, 1 eV = 96.485 kJ/mol
"""
import math

PHI = (1 + math.sqrt(5)) / 2

# Format: bond, {order: energy_kJ_mol}, source, notes
# Only bonds with 2+ bond orders (needed for R2 and alpha)
EXTENDED_BONDS = [
    # === ALREADY IN alphalaw (37 bonds) — cross-referenced ===

    # s/p homonuclear
    ("C-C",   {1: 346, 2: 614, 3: 839},  "CRC"),
    ("Si-Si", {1: 310, 2: 434},           "CRC"),         # WiredChemist: 222/? — discrepancy, CRC has 310
    ("Ge-Ge", {1: 264, 2: 350},           "CRC"),
    ("Sn-Sn", {1: 187, 2: 235},           "CRC"),
    ("N-N",   {1: 160, 2: 418, 3: 945},   "CRC"),         # LibreTexts: 941; ATcT: 945.33±0.06
    ("P-P",   {1: 201, 2: 489},           "CRC"),         # MSU: 201/489
    ("O-O",   {1: 146, 2: 498},           "CRC"),         # WiredChemist: 142/494; ATcT: 498.36±0.02
    ("S-S",   {1: 266, 2: 425},           "CRC"),         # WiredChemist: 226/425 — single differs!
    ("As-As", {1: 146, 2: 382},           "CRC"),
    ("Se-Se", {1: 172, 2: 272},           "CRC"),
    ("Te-Te", {1: 138, 2: 222},           "CRC"),

    # s/p heteronuclear
    ("C-N",   {1: 305, 2: 615, 3: 891},   "CRC"),
    ("C-O",   {1: 358, 2: 745, 3: 1077},  "CRC"),        # ATcT: D0(CO)=1076.63±0.06
    ("N-O",   {1: 201, 2: 607},           "CRC"),
    ("B-N",   {1: 389, 2: 635},           "CRC"),
    ("B-O",   {1: 536, 2: 806},           "CRC"),
    ("Si-O",  {1: 452, 2: 640},           "CRC"),
    ("Si-N",  {1: 355, 2: 470},           "CRC"),
    ("Al-O",  {1: 502, 2: 740},           "CRC"),
    ("C-S",   {1: 272, 2: 573},           "CRC"),
    ("C-P",   {1: 264, 2: 513},           "CRC"),
    ("Ge-O",  {1: 401, 2: 575},           "CRC"),
    ("B-C",   {1: 372, 2: 590},           "CRC"),
    ("N-S",   {1: 159, 2: 467},           "CRC"),
    ("P-O",   {1: 335, 2: 544},           "CRC"),
    ("S-O",   {1: 265, 2: 522},           "CRC"),
    ("P-S",   {1: 230, 2: 335},           "CRC"),

    # d-block
    ("Cr-Cr", {1: 70, 4: 152},            "Cotton; CRC"),
    ("Mo-Mo", {1: 140, 2: 250, 3: 350, 4: 405, 5: 420, 6: 435}, "Cotton & Murillo 2005"),
    ("W-W",   {1: 160, 3: 500, 4: 570, 6: 666}, "CRC; Cotton"),
    ("Re-Re", {1: 120, 4: 432},           "Bergman 1984; CRC"),

    # === NEW — from WiredChemist, MSU, LibreTexts ===

    # C=S already in CRC as C-S. MSU gives C=S=577 (kcal 138*4.184)
    # WiredChemist: C=S: 573 — consistent with CRC

    # P=S from MSU: 70 kcal/mol * 4.184 = 293 kJ/mol
    # But CRC has P-S single=230, double=335. MSU double differs.
    # WiredChemist: P=S: 335 — matches CRC

    # S=O from MSU: SO2 context: 128 kcal/mol * 4.184 = 536 kJ/mol
    # But CRC has S-O single=265, double=522. MSU value is higher.
    # WiredChemist: S=O: 522 — matches CRC

    # NEW bonds not in original dataset:
    ("Sb-Sb", {1: 121, 2: 195},           "WiredChemist; estimated double from Sb2 D0=3.09eV→298/2≈149?"),
    # Sb-Sb double uncertain, skip for now

    # Diatomic dissociation energies (these are the TOTAL bond, i.e. for the
    # highest bond order in the ground state molecule)
    # Useful for cross-checking our E_max values
]

# Diatomic D0 values (ground state dissociation energy)
# These represent the total bond energy of the diatomic molecule
# Source: Huber & Herzberg 1979, ATcT, NIST
# Units: kJ/mol
DIATOMIC_D0 = {
    # Homonuclear
    "H2":  432.07,   # ATcT: 432.068±0.001
    "B2":  290,      # ~3.0 eV
    "C2":  602,      # 6.24 eV — note: C2 has bond order ~2
    "N2":  945.33,   # ATcT: 945.33±0.06
    "O2":  498.36,   # ATcT: 498.36±0.02
    "F2":  158.67,   # ATcT: 158.67±0.05
    "Si2": 316,      # 3.28 eV * 96.485
    "P2":  489,      # ~5.07 eV
    "S2":  425.30,   # 4.41 eV
    "Cl2": 242.60,   # ATcT: 242.60±0.01
    "Ge2": 264,      # 2.74 eV
    "As2": 382,      # 3.96 eV
    "Se2": 332,      # 3.44 eV
    "Br2": 193.86,   # ATcT
    "Te2": 258,      # 2.67 eV
    "I2":  152.55,   # ATcT
    "Sn2": 187,      # 1.94 eV
    "Sb2": 299,      # 3.10 eV
    "Bi2": 204,      # 2.11 eV
    "Pb2": 87,       # 0.90 eV
    # Homonuclear d-block
    "Cr2": 152,      # 1.58 eV — very weak for quadruple bond
    "Mo2": 435,      # 4.51 eV
    "W2":  666,      # 6.90 eV
    "Re2": 432,      # 4.48 eV
    "V2":  269,      # 2.79 eV
    "Ti2": 118,      # 1.22 eV
    "Fe2": 118,      # 1.22 eV
    "Co2": 167,      # 1.73 eV
    "Ni2": 204,      # 2.11 eV
    "Cu2": 201,      # 2.08 eV
    "Ag2": 163,      # 1.69 eV
    "Au2": 226,      # 2.34 eV
    "Mn2": 61,       # 0.63 eV — weakest transition metal dimer

    # Heteronuclear
    "CO":  1076.63,  # ATcT — triple bond
    "NO":  630.57,   # ATcT — 2.5 bond order
    "CN":  749,      # 7.76 eV — ~triple bond
    "CS":  714,      # 7.40 eV — triple bond
    "SO":  522,      # 5.41 eV — double bond
    "SiO": 799,      # 8.28 eV
    "BO":  806,      # 8.35 eV
    "BN":  385,      # 3.99 eV — triple bond  (note: differs from B-N single=389!)
    "AlO": 502,      # 5.27 eV * 96.485 ≈ 508 (CRC: 502)
    "PO":  596,      # 6.18 eV
    "NS":  467,      # 4.84 eV — matches our N-S double
    "PN":  617,      # 6.39 eV — triple bond
    "PS":  442,      # 4.58 eV
    "SiS": 617,      # 6.40 eV
    "SiC": 452,      # 4.69 eV
    "GeO": 660,      # 6.84 eV
    "SnO": 528,      # 5.47 eV
    "PbO": 374,      # 3.87 eV
    "AsO": 484,      # 5.02 eV
    "SeO": 429,      # 4.45 eV
    "TeO": 373,      # 3.87 eV
    "ClO": 269,      # 2.79 eV
    "BrO": 236,      # 2.45 eV
    "IO":  222,      # 2.30 eV
    "NF":  340,      # 3.52 eV
    "OF":  220,      # 2.28 eV
    "SF":  339,      # 3.51 eV
    "CF":  552,      # 5.72 eV
    "CCl": 397,      # 4.11 eV
    "SiN": 470,      # 4.87 eV — matches our Si-N double
}


def compute_R2_alpha():
    """Compute R2 = E2/E1 and alpha for all bonds with 2+ orders."""
    results = []
    for bond, energies, source in EXTENDED_BONDS:
        orders = sorted(energies.keys())
        if len(orders) < 2:
            continue
        E1 = energies[orders[0]]
        E2 = energies[orders[1]]
        R2 = E2 / E1
        n1, n2 = orders[0], orders[1]

        # Alpha (simple)
        if len(orders) == 2:
            alpha = math.log(E2 / E1) / math.log(n2 / n1)
        else:
            x = [math.log(n / orders[0]) for n in orders[1:]]
            y = [math.log(energies[n] / E1) for n in orders[1:]]
            alpha = sum(xi * yi for xi, yi in zip(x, y)) / sum(xi * xi for xi in x)

        results.append((bond, alpha, R2, orders, energies, source))
    return results


def main():
    print("=" * 90)
    print("EXTENDED DATASET: R₂ = E₂/E₁ and Empty Gap analysis")
    print(f"φ = {PHI:.6f}")
    print("=" * 90)

    results = compute_R2_alpha()
    results.sort(key=lambda r: r[2])  # sort by R2

    print(f"\n{'Связь':<8} {'α':>6} {'R₂':>8} {'E₁':>6} {'E₂':>6} {'Тип':<6} {'R₂−2':>8}")
    print("-" * 60)

    crystals = []
    molecules = []

    for bond, alpha, R2, orders, energies, source in results:
        typ = "МОЛ" if alpha > 1 else "КРИСТ"
        E1 = energies[orders[0]]
        E2 = energies[orders[1]]
        diff2 = R2 - 2
        marker = ""
        if abs(diff2) < 0.1:
            marker = " ◄"
        print(f"{bond:<8} {alpha:>6.3f} {R2:>8.4f} {E1:>6} {E2:>6} {typ:<6} {diff2:>+8.4f}{marker}")
        if alpha > 1:
            molecules.append((bond, alpha, R2))
        else:
            crystals.append((bond, alpha, R2))

    # Gap analysis — s/p block only (d-block has different physics: delta bonds)
    d_block = {"Cr-Cr", "Mo-Mo", "W-W", "Re-Re"}
    crystals_sp = [(b, a, r) for b, a, r in crystals if b not in d_block]
    crystals_d = [(b, a, r) for b, a, r in crystals if b in d_block]

    print("\n" + "=" * 90)
    print("АНАЛИЗ РАЗРЫВА — ТОЛЬКО s/p-блок (d-блок отдельно)")
    print("=" * 90)

    cryst_max = max(crystals_sp, key=lambda x: x[2])
    mol_min = min(molecules, key=lambda x: x[2])

    print(f"\n  Наивысший R₂ кристалла: {cryst_max[2]:.6f}  ({cryst_max[0]}, α={cryst_max[1]:.3f})")
    print(f"  Наименьший R₂ молекулы: {mol_min[2]:.6f}  ({mol_min[0]}, α={mol_min[1]:.3f})")

    gap = mol_min[2] - cryst_max[2]
    print(f"  Разрыв: [{cryst_max[2]:.4f}, {mol_min[2]:.4f}]")
    print(f"  Ширина: {gap:.4f}")
    print(f"  Разрыв существует: {'ДА ✓' if gap > 0 else 'НЕТ — перекрытие'}")

    if gap > 0:
        print(f"\n  Граница ≈ 2.0: |max_cryst − 2| = {abs(cryst_max[2] - 2):.4f}")
        print(f"                  |min_mol − 2|   = {abs(mol_min[2] - 2):.4f}")
        midpoint = (cryst_max[2] + mol_min[2]) / 2
        print(f"  Середина разрыва: {midpoint:.4f}")

    # Statistics
    print(f"\n  Всего связей: {len(results)}")
    print(f"  Кристаллов s/p: {len(crystals_sp)}")
    print(f"  Кристаллов d:   {len(crystals_d)}")
    print(f"  Молекул:        {len(molecules)}")

    if crystals_d:
        print(f"\n  d-блок (исключены из анализа разрыва):")
        for b, a, r in sorted(crystals_d, key=lambda x: x[2]):
            print(f"    {b:<8} R₂={r:.4f} α={a:.3f} — δ-связи, другая физика")

    # R2 near phi
    print("\n" + "=" * 90)
    print(f"СВЯЗИ ВБЛИЗИ φ = {PHI:.4f}")
    print("=" * 90)
    near_phi = [(b, a, r) for b, a, r in crystals + molecules if abs(r - PHI) < 0.1]
    near_phi.sort(key=lambda x: x[2])
    for bond, alpha, R2 in near_phi:
        print(f"  {bond:<8} R₂={R2:.4f}  α={alpha:.3f}  (R₂−φ = {R2-PHI:+.4f})")

    # Molecules near 2
    print("\n" + "=" * 90)
    print("СВЯЗИ ВБЛИЗИ 2.0 (зона границы)")
    print("=" * 90)
    near_2 = [(b, a, r) for b, a, r in crystals + molecules if abs(r - 2) < 0.15]
    near_2.sort(key=lambda x: x[2])
    for bond, alpha, R2 in near_2:
        typ = "МОЛ" if alpha > 1 else "КРИСТ"
        print(f"  {bond:<8} R₂={R2:.4f}  α={alpha:.3f}  {typ}  (R₂−2 = {R2-2:+.4f})")


if __name__ == "__main__":
    main()
