"""
Expand the dataset by combining:
1. E₁ (single bond energy) from CRC/WiredChemist — known for ~40 pairs
2. D₀ (diatomic dissociation energy) from spectroscopy — known for ~65 diatomics
3. Bond order of the diatomic ground state — from MO theory

If we know E₁ and D₀, and D₀ = E_n for known n, then:
  R_n = D₀ / E₁
  π/σ = R₂ - 1  (for double bonds)
  α can be estimated

This gives us NEW data points for pairs not in our original 31.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alphalaw.data import BONDS

# Single bond energies (kJ/mol) from CRC/WiredChemist
# These are AVERAGE bond energies in polyatomic molecules
E_SINGLE = {
    # Already in our dataset
    "C-C": 346, "Si-Si": 310, "Ge-Ge": 264, "Sn-Sn": 187,
    "N-N": 160, "P-P": 201, "O-O": 146, "S-S": 266,
    "As-As": 146, "Se-Se": 172, "Te-Te": 138,
    "C-N": 305, "C-O": 358, "N-O": 201, "B-N": 389, "B-O": 536,
    "Si-O": 452, "Si-N": 355, "Al-O": 502, "C-S": 272, "C-P": 264,
    "Ge-O": 401, "B-C": 372, "N-S": 159, "P-O": 335, "S-O": 265, "P-S": 230,
    # NEW — from WiredChemist, not in original dataset
    "B-B": 293, "H-H": 432, "F-F": 155, "Cl-Cl": 240, "Br-Br": 190, "I-I": 148,
    "H-C": 411, "H-N": 386, "H-O": 459, "H-S": 363, "H-F": 565,
    "H-Cl": 428, "H-Br": 362, "H-I": 295, "H-Si": 318, "H-P": 322,
    "H-B": 389, "H-Ge": 288, "H-Sn": 251, "H-Se": 276, "H-Te": 238,
    "C-F": 485, "C-Cl": 327, "C-Br": 285, "C-I": 213,
    "C-Si": 318, "C-Ge": 238, "C-Sn": 192,
    "N-F": 283, "N-Cl": 313,
    "Si-S": 293, "Si-F": 565, "Si-Cl": 381,
    "Ge-N": 257, "Ge-F": 470, "Ge-Cl": 349,
    "P-F": 490, "P-Cl": 326,
    "As-O": 301, "As-F": 484, "As-Cl": 322,
    "S-F": 284, "S-Cl": 255,
    "Sb-Sb": 121,
    "Al-N": 297,  # estimated from Al₂O₃ analogy
    "B-F": 613, "B-Cl": 456,
}

# Diatomic D₀ (kJ/mol) + ground state bond order
# D₀ = total bond energy of the diatomic = E(n_ground)
# Bond order from MO theory / spectroscopy
DIATOMIC = {
    # (D₀ kJ/mol, bond_order, source)
    # Homonuclear
    "H-H":   (432, 1, "σ only"),
    "B-B":   (290, 1, "weak, σ + partial π"),  # B₂ has BO≈1
    "C-C":   (602, 2, "C₂ in gas phase, BO=2"),  # NOT diamond, gas C₂
    "N-N":   (945, 3, "triple"),
    "O-O":   (498, 2, "double"),
    "F-F":   (159, 1, "σ only, weak"),
    "Si-Si": (316, 2, "Si₂ diatomic"),
    "P-P":   (489, 3, "P₂ triple, like N₂"),  # P₂ has triple bond!
    "S-S":   (425, 2, "S₂ double"),
    "Cl-Cl": (243, 1, "σ only"),
    "Ge-Ge": (264, 1, "weak"),  # Ge₂ is essentially single bond
    "As-As": (382, 3, "As₂ triple"),  # As₂ has triple bond like N₂/P₂
    "Se-Se": (332, 2, "Se₂ double"),
    "Br-Br": (194, 1, "σ only"),
    "Te-Te": (258, 2, "Te₂ double"),  # Te₂ like O₂/S₂/Se₂
    "I-I":   (153, 1, "σ only"),
    "Sn-Sn": (187, 1, "weak"),
    "Sb-Sb": (299, 3, "Sb₂ triple"),  # like N₂/P₂/As₂

    # Heteronuclear
    "C-O":  (1077, 3, "CO triple"),
    "C-N":  (749, 3, "CN radical, ~triple"),
    "C-S":  (714, 3, "CS triple"),
    "N-O":  (631, 2.5, "NO, 2.5 bond order"),  # BO = 2.5
    "B-O":  (806, 2, "BO double/triple"),
    "B-N":  (385, 3, "BN triple"),
    "Si-O": (799, 2, "SiO double in gas"),
    "Al-O": (502, 1.5, "AlO, partially ionic"),
    "P-O":  (596, 2, "PO double"),
    "N-S":  (467, 2, "NS double"),
    "S-O":  (522, 2, "SO double"),
    "P-S":  (442, 2, "PS double"),
    "Ge-O": (660, 2, "GeO double"),
    "Si-N": (470, 2, "SiN double"),
    "P-N":  (617, 3, "PN triple"),
    "Si-S": (617, 2, "SiS double"),
    "Si-C": (452, 2, "SiC double"),
    "As-O": (484, 2, "AsO double"),
    "Se-O": (429, 2, "SeO double"),
    "Te-O": (373, 2, "TeO double"),
    "Sn-O": (528, 2, "SnO double"),
    "B-F":  (732, 1.5, "BF, partially ionic"),
    "C-F":  (552, 1, "CF radical, σ"),
    "N-F":  (340, 1, "NF, σ"),
    "B-S":  (577, 2, "BS double"),
    "B-C":  (448, 2, "BC double in gas"),  # gas phase BC ≠ B₄C crystal
    "Al-N": (368, 1.5, "AlN partially ionic"),
}


def normalize_bond(a, b):
    """Alphabetical order for consistent lookup."""
    return f"{min(a,b)}-{max(a,b)}" if a != b else f"{a}-{b}"


def main():
    print("=" * 85)
    print("РАСШИРЕНИЕ ДАТАСЕТА: D₀ + E₁ → π/σ для новых пар")
    print("=" * 85)

    # For each diatomic, if we know E₁ and D₀ with bond order n:
    # R_n = D₀ / E₁
    # For n=2: π/σ = R₂ - 1 = D₀/E₁ - 1
    # For n=3: need to decompose further

    new_pairs = []
    existing = {b.bond for b in BONDS if b.alpha is not None}

    print(f"\n  Существующие пары с α: {len(existing)}")

    for bond, (d0, bo, note) in DIATOMIC.items():
        e1 = E_SINGLE.get(bond)
        if e1 is None:
            continue

        R = d0 / e1
        is_new = bond not in existing

        if bo == 2:
            # D₀ = E₂, so R₂ = D₀/E₁, π/σ = R₂ - 1
            pi_sigma = R - 1
            alpha_est = math.log(R) / math.log(2)  # from E₂ = E₁ · 2^α
        elif bo == 3:
            # D₀ = E₃, R₃ = D₀/E₁
            # α from 2 points: E(1)=E₁, E(3)=D₀ → α = ln(D₀/E₁)/ln(3)
            alpha_est = math.log(R) / math.log(3)
            # For π/σ we need E₂ which we don't have
            # Estimate: E₂ ≈ E₁ · 2^α
            E2_est = e1 * 2**alpha_est
            pi_sigma = (E2_est - e1) / e1  # estimated
        elif bo == 1:
            # D₀ ≈ E₁, not useful for π/σ
            pi_sigma = 0  # no double bond
            alpha_est = None
            continue  # skip single-bond diatomics
        elif bo == 2.5:
            # NO: bond order 2.5
            # Estimate α from E(1) and E(2.5)
            alpha_est = math.log(R) / math.log(2.5)
            E2_est = e1 * 2**alpha_est
            pi_sigma = (E2_est - e1) / e1
        elif bo == 1.5:
            alpha_est = math.log(R) / math.log(1.5)
            E2_est = e1 * 2**alpha_est if alpha_est else None
            pi_sigma = (E2_est - e1) / e1 if E2_est else 0
        else:
            continue

        pred = "МОЛ" if pi_sigma > 1 else "КРИСТ"
        new_pairs.append((bond, e1, d0, bo, R, pi_sigma, alpha_est, pred, is_new))

    # Sort by π/σ
    new_pairs.sort(key=lambda x: x[5])

    print(f"  Новых пар (не в исходных 31): {sum(1 for p in new_pairs if p[8])}")
    print(f"  Всего пар с π/σ: {len(new_pairs)}")

    print(f"\n  {'Связь':<8} {'E₁':>5} {'D₀':>5} {'n':>4} {'R_n':>6} {'π/σ':>6} "
          f"{'α_ест':>6} {'Пред':<6} {'Новая?':<6}")
    print(f"  {'-'*65}")

    new_count = 0
    for bond, e1, d0, bo, R, ps, alpha, pred, is_new in new_pairs:
        a_str = f"{alpha:.3f}" if alpha else "  —  "
        new_str = "★ ДА" if is_new else ""
        print(f"  {bond:<8} {e1:>5} {d0:>5} {bo:>4.1f} {R:>6.3f} {ps:>6.3f} "
              f"{a_str:>6} {pred:<6} {new_str}")
        if is_new:
            new_count += 1

    # Cross-validate: for pairs IN our dataset, compare estimated vs actual α
    print(f"\n{'='*85}")
    print("ПЕРЕКРЁСТНАЯ ПРОВЕРКА: оценка α из D₀ vs фактический α")
    print(f"{'='*85}")

    bond_alpha = {b.bond: b.alpha for b in BONDS if b.alpha is not None}

    print(f"\n  {'Связь':<8} {'α факт':>7} {'α оценка':>8} {'Ошибка':>8} {'OK?':>4}")
    print(f"  {'-'*40}")

    errors = []
    class_ok = 0
    class_total = 0
    for bond, e1, d0, bo, R, ps, alpha_est, pred, is_new in new_pairs:
        if bond in bond_alpha and alpha_est is not None:
            actual = bond_alpha[bond]
            err = alpha_est - actual
            ok = "✓" if (actual > 1) == (alpha_est > 1) else "✗"
            print(f"  {bond:<8} {actual:>7.3f} {alpha_est:>8.3f} {err:>+8.3f} {ok:>4}")
            errors.append(abs(err))
            class_total += 1
            if ok == "✓":
                class_ok += 1

    if errors:
        print(f"\n  MAE = {sum(errors)/len(errors):.3f}")
        print(f"  Классификация: {class_ok}/{class_total} = {100*class_ok/class_total:.1f}%")

    # Summary: all NEW pairs
    print(f"\n{'='*85}")
    print(f"ИТОГО: {new_count} НОВЫХ ПАР")
    print(f"{'='*85}")
    for bond, e1, d0, bo, R, ps, alpha, pred, is_new in new_pairs:
        if is_new and alpha is not None:
            print(f"  {bond:<8} π/σ={ps:.3f} α≈{alpha:.3f} → {pred}")


if __name__ == "__main__":
    main()
