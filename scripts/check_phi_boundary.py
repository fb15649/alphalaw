"""
Critical test: is the Empty Gap boundary exactly φ = (1+√5)/2 = 1.6180339...?

R = E_max / E_single for each bond.
If gap = [φ, 2], then:
  - All crystals (α < 1) should have R ≤ φ
  - All molecules (α > 1) should have R ≥ 2 (approximately)
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alphalaw.data import BONDS

PHI = (1 + math.sqrt(5)) / 2  # 1.6180339887...

def main():
    print("=" * 85)
    print(f"Empty Gap Boundary Test: is R_lower = φ = {PHI:.10f}?")
    print("=" * 85)

    rows = []
    for b in BONDS:
        orders = sorted(b.energies.keys())
        if len(orders) < 2:
            continue
        E_single = b.energies[orders[0]]
        E_max = b.energies[orders[-1]]
        R = E_max / E_single
        n_max = orders[-1]
        alpha = b.alpha
        rows.append((b.bond, alpha, R, n_max, E_single, E_max, b.block))

    rows.sort(key=lambda r: r[2])  # sort by R

    print(f"\n{'Bond':<8} {'α':>6} {'R=Emax/E1':>10} {'n_max':>6} {'E1':>6} {'Emax':>6} {'Type':<6} {'vs φ':>10}")
    print("-" * 85)

    crystals_R = []
    molecules_R = []

    for bond, alpha, R, n_max, E1, Emax, block in rows:
        typ = "MOL" if alpha > 1 else "CRYST"
        diff = R - PHI
        marker = ""
        if abs(diff) < 0.1:
            marker = " ← NEAR φ"
        print(f"{bond:<8} {alpha:>6.3f} {R:>10.4f} {n_max:>6} {E1:>6} {Emax:>6} {typ:<6} {diff:>+10.4f}{marker}")

        if alpha > 1:
            molecules_R.append(R)
        else:
            crystals_R.append(R)

    # Gap analysis
    print("\n" + "=" * 85)
    print("GAP ANALYSIS")
    print("=" * 85)

    max_cryst_R = max(crystals_R)
    min_mol_R = min(molecules_R)

    print(f"\n  Highest crystal R:   {max_cryst_R:.6f}")
    print(f"  Lowest molecule R:   {min_mol_R:.6f}")
    print(f"  Gap:                 [{max_cryst_R:.6f}, {min_mol_R:.6f}]")
    print(f"  Gap width:           {min_mol_R - max_cryst_R:.6f}")

    print(f"\n  φ = {PHI:.10f}")
    print(f"  |max_cryst_R - φ| = {abs(max_cryst_R - PHI):.6f}")
    print(f"  |min_mol_R - 2|   = {abs(min_mol_R - 2):.6f}")

    print(f"\n  Is max_cryst_R ≤ φ?  {'YES ✓' if max_cryst_R <= PHI else 'NO ✗'}  ({max_cryst_R:.6f} vs {PHI:.6f})")
    print(f"  Is min_mol_R  ≥ 2?   {'YES ✓' if min_mol_R >= 2 else 'NO ✗'}  ({min_mol_R:.6f} vs 2.000000)")

    # Check: φ as lower boundary
    print("\n" + "=" * 85)
    print("φ AS EXACT BOUNDARY TEST")
    print("=" * 85)

    cryst_above_phi = [r for r in crystals_R if r > PHI]
    mol_below_2 = [r for r in molecules_R if r < 2]

    print(f"\n  Crystals with R > φ:  {len(cryst_above_phi)} / {len(crystals_R)}")
    if cryst_above_phi:
        for bond, alpha, R, n_max, E1, Emax, block in rows:
            if alpha <= 1 and R > PHI:
                print(f"    {bond}: R = {R:.4f}, α = {alpha:.3f}")

    print(f"\n  Molecules with R < 2: {len(mol_below_2)} / {len(molecules_R)}")
    if mol_below_2:
        for bond, alpha, R, n_max, E1, Emax, block in rows:
            if alpha > 1 and R < 2:
                print(f"    {bond}: R = {R:.4f}, α = {alpha:.3f}")

    # What is the exact midpoint of the gap?
    gap_mid = (max_cryst_R + min_mol_R) / 2
    print(f"\n  Gap midpoint:  {gap_mid:.6f}")
    print(f"  (φ + 2) / 2:  {(PHI + 2) / 2:.6f}")
    print(f"  Difference:    {abs(gap_mid - (PHI + 2) / 2):.6f}")

    # Alternative boundaries to test
    print("\n" + "=" * 85)
    print("ALTERNATIVE BOUNDARY CANDIDATES")
    print("=" * 85)

    candidates = [
        ("φ", PHI),
        ("8/5 (Fibonacci)", 8/5),
        ("√e", math.sqrt(math.e)),
        ("ln(5)", math.log(5)),
        ("5/3", 5/3),
        ("√(φ+1) = √(φ²) = φ", PHI),  # same
        ("π/2", math.pi/2),
        ("3/2", 3/2),
    ]

    print(f"\n  max_cryst_R = {max_cryst_R:.6f}")
    print()
    for name, val in candidates:
        if name == "√(φ+1) = √(φ²) = φ":
            continue
        diff = abs(max_cryst_R - val)
        side = "above" if max_cryst_R > val else "below"
        print(f"  {name:<20} = {val:.6f}  |diff| = {diff:.6f}  (R is {side})")


if __name__ == "__main__":
    main()
