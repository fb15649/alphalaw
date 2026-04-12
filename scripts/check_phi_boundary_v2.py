"""
Critical test v2: is the Empty Gap boundary exactly φ?

R₂ = E(2) / E(1) — ratio of double to single bond energy.
This is the fair comparison: same bond order increase (1→2) for all bonds.
The original gap [1.63, 1.97] was found on this ratio.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alphalaw.data import BONDS

PHI = (1 + math.sqrt(5)) / 2  # 1.6180339887...

def main():
    print("=" * 85)
    print(f"Empty Gap v2: R₂ = E(2)/E(1) — is the boundary φ = {PHI:.10f}?")
    print("=" * 85)

    rows = []
    for b in BONDS:
        if 1 not in b.energies or 2 not in b.energies:
            continue
        E1 = b.energies[1]
        E2 = b.energies[2]
        R2 = E2 / E1
        alpha = b.alpha
        rows.append((b.bond, alpha, R2, E1, E2, b.block))

    rows.sort(key=lambda r: r[2])

    print(f"\n{'Bond':<8} {'α':>6} {'R₂=E₂/E₁':>10} {'E₁':>6} {'E₂':>6} {'Type':<6} {'R₂ - φ':>10}")
    print("-" * 75)

    crystals_R = []
    molecules_R = []

    for bond, alpha, R2, E1, E2, block in rows:
        typ = "MOL" if alpha > 1 else "CRYST"
        diff = R2 - PHI
        marker = ""
        if abs(diff) < 0.08:
            marker = " ★"
        print(f"{bond:<8} {alpha:>6.3f} {R2:>10.6f} {E1:>6} {E2:>6} {typ:<6} {diff:>+10.6f}{marker}")

        if alpha > 1:
            molecules_R.append((R2, bond))
        else:
            crystals_R.append((R2, bond))

    print("\n" + "=" * 85)
    print("GAP ANALYSIS")
    print("=" * 85)

    cryst_Rs = sorted([r for r, _ in crystals_R])
    mol_Rs = sorted([r for r, _ in molecules_R])

    max_cryst = max(crystals_R, key=lambda x: x[0])
    min_mol = min(molecules_R, key=lambda x: x[0])

    print(f"\n  Highest crystal R₂:  {max_cryst[0]:.6f}  ({max_cryst[1]})")
    print(f"  Lowest molecule R₂:  {min_mol[0]:.6f}  ({min_mol[1]})")
    print(f"\n  GAP = [{max_cryst[0]:.6f}, {min_mol[0]:.6f}]")
    print(f"  Gap width: {min_mol[0] - max_cryst[0]:.6f}")

    gap_exists = min_mol[0] > max_cryst[0]
    print(f"  Gap exists: {'YES ✓' if gap_exists else 'NO — overlap'}")

    if gap_exists:
        print(f"\n  --- Boundary analysis ---")
        print(f"  Lower boundary (max crystal R₂): {max_cryst[0]:.10f}")
        print(f"  φ =                               {PHI:.10f}")
        print(f"  Difference:                       {max_cryst[0] - PHI:+.10f}")
        print(f"  Is lower boundary < φ?            {'YES ✓' if max_cryst[0] < PHI else 'NO'}")
        print(f"  Is lower boundary > φ?            {'YES' if max_cryst[0] > PHI else 'NO'}")
        print()
        print(f"  Upper boundary (min mol R₂):      {min_mol[0]:.10f}")
        print(f"  2.0 =                             2.0000000000")
        print(f"  Difference:                       {min_mol[0] - 2:+.10f}")

    # Crystals near/above φ
    print("\n" + "=" * 85)
    print("CRYSTALS NEAR φ (closest to boundary)")
    print("=" * 85)
    for R2, bond in sorted(crystals_R, key=lambda x: -x[0])[:8]:
        diff = R2 - PHI
        print(f"  {bond:<8} R₂ = {R2:.6f}  (R₂ - φ = {diff:+.6f})")

    # Molecules near 2
    print("\n" + "=" * 85)
    print("MOLECULES NEAR 2 (closest to boundary)")
    print("=" * 85)
    for R2, bond in sorted(molecules_R, key=lambda x: x[0])[:8]:
        diff = R2 - 2
        print(f"  {bond:<8} R₂ = {R2:.6f}  (R₂ - 2 = {diff:+.6f})")

    # Best-fit boundary
    print("\n" + "=" * 85)
    print("CANDIDATE BOUNDARIES (lower)")
    print("=" * 85)

    if gap_exists:
        candidates = [
            ("φ = (1+√5)/2", PHI),
            ("8/5 (Fib ratio)", 1.6),
            ("1.63 (empirical)", 1.63),
            ("ln(5)", math.log(5)),
            ("√e", math.sqrt(math.e)),
            ("5/3", 5/3),
            ("π/2", math.pi / 2),
            ("e/φ", math.e / PHI),
            ("2/√(φ+1)", 2 / math.sqrt(PHI + 1)),
        ]
        print(f"\n  max crystal R₂ = {max_cryst[0]:.6f}")
        print(f"  min molecule R₂ = {min_mol[0]:.6f}")
        print()
        for name, val in candidates:
            in_gap = max_cryst[0] < val < min_mol[0]
            dist_to_cryst = val - max_cryst[0]
            print(f"  {name:<22} = {val:.6f}  in gap: {'YES' if in_gap else 'no '}  dist from max_cryst: {dist_to_cryst:+.6f}")


if __name__ == "__main__":
    main()
