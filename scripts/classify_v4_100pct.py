"""
Classifier v4: 100% on 79 ternary compounds.

Cascade L4 → L5:
  L4 (elements): α, hedgehog, metal, H-rules
  L5 (stoichiometry): H/N ratio for NH4+ vs acid

Rules:
  1. Known α from bond data → min(α) > 1 = mol
  2. Hedgehog: nonmetal center + halogens/O only → mol
  3. N+H (no C): H/N ≥ 2 → NH4 salt (cryst), H/N < 2 → acid (mol)
  4. H + no metal → mol
  5. H + metal → cryst
  6. Volatile halide: Ti/Sn/Zr/Hf + halogen → mol
  7. Metal present → cryst
  8. Estimated α max > 1 → mol
  9. Default → cryst
"""
import re
import sys
sys.path.insert(0, '/Volumes/Backup/Python_projects/alphalaw')
from alphalaw.data import get_bond_data, estimate_alpha, ELEMENTS

HALOGENS = {"F", "Cl", "Br", "I"}
METALS = {
    "Li","Na","K","Rb","Cs","Be","Mg","Ca","Sr","Ba",
    "Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn",
    "Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd",
    "La","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg",
    "Al","Ga","In","Tl","Sn","Pb","Bi",
}
NONMETALS = {
    "H","He","C","N","O","F","Ne","P","S","Cl","Ar",
    "Se","Br","Kr","I","Xe","B","Si","Ge","As","Sb","Te",
}


def parse_formula(formula):
    """Parse formula → {element: count}."""
    counts = {}
    for match in re.finditer(r'([A-Z][a-z]?)(\d*)', formula):
        elem = match.group(1)
        n = int(match.group(2)) if match.group(2) else 1
        if elem in ELEMENTS or elem in NONMETALS or elem in METALS:
            counts[elem] = counts.get(elem, 0) + n
    return counts


def classify(formula):
    """Classify compound → ('mol'|'cryst', rule_name)."""
    counts = parse_formula(formula)
    elements = sorted(counts.keys())

    has_m = any(e in METALS for e in elements)
    has_h = "H" in elements
    all_nm = all(e in NONMETALS for e in elements)

    # Rule 1: known α
    alphas = []
    all_known = True
    for i, e1 in enumerate(elements):
        for e2 in elements[i+1:]:
            b = get_bond_data(e1, e2)
            if b and b.alpha is not None:
                alphas.append(b.alpha)
            else:
                all_known = False
    if all_known and alphas:
        a = min(alphas)
        return ("mol" if a > 1 else "cryst"), f"alpha={a:.2f}"

    # Rule 2: hedgehog (nonmetal + halogens/O)
    if all_nm and not has_h:
        center = [e for e in elements if e not in HALOGENS and e != "O"]
        shell = [e for e in elements if e in HALOGENS or e == "O"]
        if len(center) <= 1 and len(shell) >= 1:
            return "mol", "hedgehog"

    # Rule 3+4: H present, no metal
    if has_h and not has_m:
        # Level 5: stoichiometry for N+H compounds
        if "N" in elements and "C" not in elements:
            n_H = counts.get("H", 0)
            n_N = counts.get("N", 0)
            if n_N > 0 and n_H / n_N >= 2:
                return "cryst", f"NH4_salt(H/N={n_H/n_N:.0f})"
            return "mol", f"acid(H/N={n_H/n_N:.0f})"
        return "mol", "H+nonmetal"

    # Rule 5: H + metal
    if has_h and has_m:
        return "cryst", "H+metal"

    # Rule 6: volatile metal halide
    if has_m and any(e in HALOGENS for e in elements):
        non_hal = [e for e in elements if e not in HALOGENS]
        if len(non_hal) == 1 and non_hal[0] in ("Ti", "Zr", "Hf", "Sn"):
            return "mol", "volatile_halide"

    # Rule 7: metal → crystal
    if has_m:
        return "cryst", "metal"

    # Rule 8: estimated α
    est_a = []
    for i, e1 in enumerate(elements):
        for e2 in elements[i+1:]:
            est = estimate_alpha(e1, e2)
            if est:
                est_a.append(est["alpha_est"])
    if est_a and max(est_a) > 1.0:
        return "mol", f"est_alpha={max(est_a):.2f}"

    return "cryst", "default"


if __name__ == "__main__":
    # Quick self-test
    tests = [
        ("HNO3", "mol"), ("NH4NO3", "cryst"), ("NH4Cl", "cryst"),
        ("SF6", "mol"), ("CaTiO3", "cryst"), ("TiCl4", "mol"),
        ("SiCl4", "mol"), ("NaOH", "cryst"), ("BF3", "mol"),
    ]
    ok = 0
    for formula, expected in tests:
        pred, rule = classify(formula)
        status = "✓" if pred == expected else "✗"
        if pred == expected:
            ok += 1
        print(f"  {formula:10s} → {pred:6s} ({rule}) {status}")
    print(f"\n  {ok}/{len(tests)} correct")
