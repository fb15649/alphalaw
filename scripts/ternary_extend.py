"""
Ternary extension of alphalaw.

Strategy: a ternary compound ABC is classified by the
WEAKEST LINK — the pair with the lowest α determines
whether the compound is molecular or crystalline.

Reasoning: a chain is as strong as its weakest link.
If ONE pair prefers single bonds (α < 1), the compound
forms a 3D framework. All pairs must be synergistic (α > 1)
for the compound to be a molecule.

Test on JARVIS-DFT ternary materials.
"""
import sys
import math
from collections import Counter

sys.path.insert(0, '/Volumes/Backup/Python_projects/alphalaw')
from alphalaw.data import get_bond_data, estimate_alpha, ELEMENTS

# Try to import JARVIS
try:
    from jarvis.db.figshare import data as jdata
    HAS_JARVIS = True
except ImportError:
    HAS_JARVIS = False
    print("WARNING: jarvis-tools not installed. Using built-in test set.")


def get_alpha_for_pair(e1, e2):
    """Get α for element pair — from data or estimate."""
    bond = get_bond_data(e1, e2)
    if bond and bond.alpha is not None:
        return bond.alpha, "data"
    est = estimate_alpha(e1, e2)
    if est:
        return est["alpha_est"], "estimated"
    return None, "unknown"


def get_unique_pairs(elements):
    """Get all unique element pairs from a list of elements."""
    pairs = set()
    for i, e1 in enumerate(elements):
        for e2 in elements[i+1:]:
            pair = tuple(sorted([e1, e2]))
            pairs.add(pair)
        # Also include same-element pairs if element appears multiple times
    return pairs


def parse_formula(formula):
    """Parse chemical formula into element list.
    E.g., 'Ca1Ti1O3' → ['Ca', 'Ti', 'O']
    """
    import re
    elements = set()
    for match in re.finditer(r'([A-Z][a-z]?)\d*', formula):
        elem = match.group(1)
        if elem in ELEMENTS:
            elements.add(elem)
    return sorted(elements)


def classify_compound(elements):
    """Classify compound by weakest-link rule.
    Returns: 'mol', 'cryst', or 'unknown' with details.
    """
    if len(elements) < 2:
        return "unknown", {}

    pairs = get_unique_pairs(elements)
    alphas = {}
    for e1, e2 in pairs:
        a, src = get_alpha_for_pair(e1, e2)
        if a is not None:
            alphas[f"{e1}-{e2}"] = (a, src)

    if not alphas:
        return "unknown", {}

    # Weakest link = minimum α
    min_pair = min(alphas, key=lambda k: alphas[k][0])
    min_alpha = alphas[min_pair][0]

    # Classification
    classification = "mol" if min_alpha > 1.0 else "cryst"

    return classification, {
        "min_pair": min_pair,
        "min_alpha": min_alpha,
        "all_alphas": alphas,
        "rule": "weakest-link (min α determines classification)",
    }


# ============================================================
# Built-in test set (known ternary compounds)
# ============================================================
TERNARY_TEST = [
    # (formula, elements, known_type)
    # Crystals (frameworks)
    ("CaTiO3",    ["Ca", "Ti", "O"],   "cryst"),   # perovskite
    ("BaTiO3",    ["Ba", "Ti", "O"],   "cryst"),   # perovskite
    ("SrTiO3",    ["Sr", "Ti", "O"],   "cryst"),   # perovskite
    ("LiNbO3",    ["Li", "Nb", "O"],   "cryst"),   # lithium niobate
    ("MgAl2O4",   ["Mg", "Al", "O"],   "cryst"),   # spinel
    ("CaCO3",     ["Ca", "C",  "O"],   "cryst"),   # calcite
    ("NaAlSi3O8", ["Na", "Al", "Si", "O"], "cryst"),  # albite (feldspar)
    ("KAlSi3O8",  ["K",  "Al", "Si", "O"], "cryst"),  # orthoclase
    ("LiFePO4",   ["Li", "Fe", "P", "O"],  "cryst"),  # battery cathode
    ("YBa2Cu3O7", ["Y",  "Ba", "Cu", "O"], "cryst"),  # YBCO superconductor
    ("ZnSiO3",    ["Zn", "Si", "O"],  "cryst"),   # zinc silicate
    ("FeTiO3",    ["Fe", "Ti", "O"],   "cryst"),   # ilmenite
    ("Al2SiO5",   ["Al", "Si", "O"],   "cryst"),   # kyanite/sillimanite
    ("CaSiO3",    ["Ca", "Si", "O"],   "cryst"),   # wollastonite
    ("MgSiO3",    ["Mg", "Si", "O"],   "cryst"),   # enstatite
    ("NaClO3",    ["Na", "Cl", "O"],   "cryst"),   # sodium chlorate
    ("KMnO4",     ["K",  "Mn", "O"],   "cryst"),   # potassium permanganate
    ("Bi2Te3",    ["Bi", "Te"],        "cryst"),   # bismuth telluride (binary check)
    ("GaAs",      ["Ga", "As"],        "cryst"),   # gallium arsenide (binary check)

    # Molecules (gases/liquids at STP)
    ("HCN",       ["H", "C", "N"],     "mol"),     # hydrogen cyanide
    ("H2SO4",     ["H", "S", "O"],     "mol"),     # sulfuric acid (liquid)
    ("HNO3",      ["H", "N", "O"],     "mol"),     # nitric acid
    ("CH3OH",     ["C", "H", "O"],     "mol"),     # methanol
    ("NH4Cl",     ["N", "H", "Cl"],    "mol"),     # ammonium chloride — actually cryst!
    ("POCl3",     ["P", "O", "Cl"],    "mol"),     # phosphoryl chloride
    ("SOCl2",     ["S", "O", "Cl"],    "mol"),     # thionyl chloride
    ("NOCl",      ["N", "O", "Cl"],    "mol"),     # nitrosyl chloride
    ("COCl2",     ["C", "O", "Cl"],    "mol"),     # phosgene
    ("BF3",       ["B", "F"],          "mol"),     # boron trifluoride (binary check)
]

# NH4Cl is ionic crystal despite being made of molecular ions — edge case
# Let's mark it correctly
TERNARY_TEST[23] = ("NH4Cl", ["N", "H", "Cl"], "cryst")


# ============================================================
# Run tests
# ============================================================
print("=" * 76)
print("  TERNARY EXTENSION: WEAKEST-LINK CLASSIFICATION")
print("=" * 76)
print()

correct = 0
wrong = 0
unknown = 0
results = []

for formula, elements, known in TERNARY_TEST:
    pred, details = classify_compound(elements)
    status = "✓" if pred == known else ("?" if pred == "unknown" else "✗")

    if pred == known:
        correct += 1
    elif pred == "unknown":
        unknown += 1
    else:
        wrong += 1

    results.append((formula, elements, known, pred, status, details))

# Print results
print(f"{'Formula':<14} {'Elements':<22} {'Known':<7} {'Pred':<7} {'':>3} Min pair (α)")
print("─" * 76)
for formula, elements, known, pred, status, details in results:
    elem_str = "+".join(elements)
    min_info = ""
    if details:
        min_info = f"{details['min_pair']} ({details['min_alpha']:.3f})"
    print(f"{formula:<14} {elem_str:<22} {known:<7} {pred:<7} {status:>3} {min_info}")

# Summary
total = correct + wrong + unknown
print(f"""
{'='*76}
  РЕЗУЛЬТАТ
{'='*76}

  Всего:     {total}
  Правильно: {correct} ({correct/total*100:.1f}%)
  Неверно:   {wrong} ({wrong/total*100:.1f}%)
  Неизвестно:{unknown}
""")

# Show wrong ones in detail
if wrong > 0:
    print("  ОШИБКИ:")
    for formula, elements, known, pred, status, details in results:
        if status == "✗":
            print(f"    {formula}: known={known}, pred={pred}")
            if details:
                for pair, (a, src) in details["all_alphas"].items():
                    marker = " ← min" if pair == details["min_pair"] else ""
                    print(f"      {pair}: α={a:.3f} ({src}){marker}")
            print()


# ============================================================
# Alternative model: average α
# ============================================================
print("=" * 76)
print("  АЛЬТЕРНАТИВА: СРЕДНИЙ α")
print("=" * 76)
print()

correct2 = 0
for formula, elements, known, _, _, details in results:
    if not details or not details.get("all_alphas"):
        continue
    alphas = [a for a, _ in details["all_alphas"].values()]
    avg = sum(alphas) / len(alphas)
    pred2 = "mol" if avg > 1.0 else "cryst"
    if pred2 == known:
        correct2 += 1

total_with_data = sum(1 for _, _, _, _, _, d in results if d and d.get("all_alphas"))
print(f"  Средний α: {correct2}/{total_with_data} = {correct2/total_with_data*100:.1f}%")
print(f"  Мин. α:    {correct}/{total} = {correct/total*100:.1f}%")
print()

# Which is better?
print(f"  {'Мин. α лучше' if correct > correct2 else 'Средний α лучше' if correct2 > correct else 'Одинаково'}")
