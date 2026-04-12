"""
Ternary classification on JARVIS-DFT (42,867 ternary materials).

Three-tier classifier:
  Tier 1: α from bond data (known pairs with multiple bond orders)
  Tier 2: Proxy features (electronegativity, metal/nonmetal) when α undefined
  Tier 3: Ionicity criterion (ΔEN > 1.7 → ionic crystal)

Best practice: when data is missing, DON'T extrapolate α.
Use proxy features and mark confidence honestly.
"""
import re
import sys
import math
from collections import Counter

sys.path.insert(0, '/Volumes/Backup/Python_projects/alphalaw')
from alphalaw.data import get_bond_data, estimate_alpha, ELEMENTS

from jarvis.db.figshare import data as jdata


# ============================================================
# Element properties
# ============================================================
# Electronegativity (Pauling scale)
EN = {
    "H": 2.20, "Li": 0.98, "Be": 1.57, "B": 2.04, "C": 2.55,
    "N": 3.04, "O": 3.44, "F": 3.98, "Na": 0.93, "Mg": 1.31,
    "Al": 1.61, "Si": 1.90, "P": 2.19, "S": 2.58, "Cl": 3.16,
    "K": 0.82, "Ca": 1.00, "Sc": 1.36, "Ti": 1.54, "V": 1.63,
    "Cr": 1.66, "Mn": 1.55, "Fe": 1.83, "Co": 1.88, "Ni": 1.91,
    "Cu": 1.90, "Zn": 1.65, "Ga": 1.81, "Ge": 2.01, "As": 2.18,
    "Se": 2.55, "Br": 2.96, "Rb": 0.82, "Sr": 0.95, "Y": 1.22,
    "Zr": 1.33, "Nb": 1.60, "Mo": 2.16, "Ru": 2.20, "Rh": 2.28,
    "Pd": 2.20, "Ag": 1.93, "Cd": 1.69, "In": 1.78, "Sn": 1.96,
    "Sb": 2.05, "Te": 2.10, "I": 2.66, "Cs": 0.79, "Ba": 0.89,
    "La": 1.10, "Hf": 1.30, "Ta": 1.50, "W": 2.36, "Re": 1.90,
    "Os": 2.20, "Ir": 2.20, "Pt": 2.28, "Au": 2.54, "Hg": 2.00,
    "Tl": 1.62, "Pb": 2.33, "Bi": 2.02,
}

METALS = {
    "Li", "Na", "K", "Rb", "Cs",  # alkali
    "Be", "Mg", "Ca", "Sr", "Ba",  # alkaline earth
    "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",  # 3d
    "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd",  # 4d
    "La", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg",  # 5d
    "Al", "Ga", "In", "Tl", "Sn", "Pb", "Bi",  # p-metals
    "Ce", "Pr", "Nd", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er",
    "Tm", "Yb", "Lu", "Th", "U", "Np", "Pu",  # f-block
}

# Elements that only form single bonds (no α computable)
SINGLE_BOND_ONLY = {"H", "F", "Cl", "Br", "I", "He", "Ne", "Ar", "Kr", "Xe"}


def parse_elements(formula):
    """Extract unique elements from formula."""
    return sorted(set(re.findall(r'[A-Z][a-z]?', formula)))


def max_delta_en(elements):
    """Maximum electronegativity difference among all pairs."""
    ens = [EN.get(e, 0) for e in elements if EN.get(e, 0) > 0]
    if len(ens) < 2:
        return 0
    return max(ens) - min(ens)


def has_metal(elements):
    return any(e in METALS for e in elements)


def has_H(elements):
    return "H" in elements


def all_alpha_known(elements):
    """Check if ALL pairs have α from actual bond data (not estimated)."""
    for i, e1 in enumerate(elements):
        for e2 in elements[i+1:]:
            bond = get_bond_data(e1, e2)
            if bond is None or bond.alpha is None:
                return False
    return True


def min_alpha(elements):
    """Get minimum α across all pairs (data or estimated)."""
    alphas = []
    for i, e1 in enumerate(elements):
        for e2 in elements[i+1:]:
            bond = get_bond_data(e1, e2)
            if bond and bond.alpha is not None:
                alphas.append(bond.alpha)
            else:
                est = estimate_alpha(e1, e2)
                if est:
                    alphas.append(est["alpha_est"])
    return min(alphas) if alphas else None


def classify_ternary(elements):
    """
    Three-tier classifier:
    Tier 1: If all pairs have known α → use min(α)
    Tier 2: If H present and no metal → molecule (proxy)
    Tier 3: If metal present or ΔEN > 1.7 → crystal (ionic)
    Default: use estimated α
    """
    if len(elements) < 2:
        return "unknown", "insufficient", 0

    # Tier 1: all α known from bond data
    if all_alpha_known(elements):
        a = min_alpha(elements)
        if a is not None:
            cls = "mol" if a > 1.0 else "cryst"
            return cls, "tier1_alpha", 1

    # Tier 2: H present, no metal → molecular
    if has_H(elements) and not has_metal(elements):
        # But check ionicity: NH4+ salts etc.
        den = max_delta_en(elements)
        if den > 2.5:
            return "cryst", "tier2_H_ionic", 2
        return "mol", "tier2_H_nometal", 2

    # Tier 3: metal present → crystal (vast majority)
    if has_metal(elements):
        return "cryst", "tier3_metal", 3

    # Tier 3b: large ΔEN → ionic crystal
    den = max_delta_en(elements)
    if den > 1.7:
        return "cryst", "tier3_ionic", 3

    # Default: use estimated min α
    a = min_alpha(elements)
    if a is not None:
        cls = "mol" if a > 1.0 else "cryst"
        return cls, "default_est_alpha", 4

    return "unknown", "no_data", 0


# ============================================================
# Ground truth: dimensionality from JARVIS
# ============================================================
def is_molecular(mat):
    """Determine if material is molecular from JARVIS data.
    Use dimensionality: 0D (molecular) vs 3D (crystal).
    Also: if optb88vdw_bandgap == 0 and large → likely metallic crystal.
    """
    dim = mat.get("dimensionality")
    if dim is not None:
        if isinstance(dim, str):
            dim = dim.strip()
            if dim in ("0", "0D"):
                return True
            if dim in ("3", "3D", "2", "2D", "1", "1D"):
                return False
        elif isinstance(dim, (int, float)):
            return dim == 0
    # Fallback: if no dimensionality, assume crystal (most materials)
    return False


# ============================================================
# Main test
# ============================================================
print("Loading JARVIS-DFT...")
dataset = jdata("dft_3d")
print(f"Total materials: {len(dataset)}")

# Filter to ternary (3 elements)
ternary = []
for mat in dataset:
    formula = mat.get("formula", "")
    elements = parse_elements(formula)
    if len(elements) >= 3:
        ternary.append((formula, elements, mat))

print(f"Ternary+ materials: {len(ternary)}")

# Classify
results = Counter()
tier_counts = Counter()
correct = 0
wrong = 0
unknown_count = 0
total = 0

mol_as_cryst = 0
cryst_as_mol = 0

for formula, elements, mat in ternary:
    known_mol = is_molecular(mat)
    known = "mol" if known_mol else "cryst"

    pred, tier, confidence = classify_ternary(elements)

    if pred == "unknown":
        unknown_count += 1
        continue

    total += 1
    tier_counts[tier] += 1

    if pred == known:
        correct += 1
    else:
        wrong += 1
        if known == "mol" and pred == "cryst":
            mol_as_cryst += 1
        elif known == "cryst" and pred == "mol":
            cryst_as_mol += 1

accuracy = correct / total * 100 if total > 0 else 0

print(f"""
{'='*76}
  РЕЗУЛЬТАТ: ТЕРНАРНЫЕ МАТЕРИАЛЫ НА JARVIS-DFT
{'='*76}

  Материалов проверено: {total} (из {len(ternary)}, {unknown_count} неизвестных)
  Правильно:  {correct} ({accuracy:.1f}%)
  Неверно:    {wrong} ({100-accuracy:.1f}%)
    молекулу назвали кристаллом: {mol_as_cryst}
    кристалл назвали молекулой:  {cryst_as_mol}

  По уровням:
""")
for tier, count in sorted(tier_counts.items()):
    print(f"    {tier:25s}: {count:6d} материалов")

# Also show what fraction are molecular vs crystal in JARVIS
n_mol = sum(1 for _, _, mat in ternary if is_molecular(mat))
n_cryst = len(ternary) - n_mol
print(f"""
  Распределение в JARVIS:
    Кристаллы: {n_cryst} ({n_cryst/len(ternary)*100:.1f}%)
    Молекулы:  {n_mol} ({n_mol/len(ternary)*100:.1f}%)

  Если бы всегда говорили "кристалл":
    Точность = {n_cryst/len(ternary)*100:.1f}% (baseline)

  Наша точность: {accuracy:.1f}% (improvement: +{accuracy - n_cryst/len(ternary)*100:.1f}%)
""")
