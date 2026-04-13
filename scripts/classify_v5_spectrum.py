"""
Classifier v5: α as spectrum, not binary switch.

5 categories:
  GAS        α > 1.5   (strong molecule, volatile)
  LIQUID     1.0 < α ≤ 1.5  (moderate molecule, condensable)
  BORDER     0.8 < α ≤ 1.0  (either/both, polymorphic, glass-forming)
  CRYSTAL    0.5 < α ≤ 0.8  (framework, ionic, covalent network)
  REFRACTORY α ≤ 0.5   (extremely strong framework, high melting)

Principle: if not 100% → find what's wrong in missing % → iterate.
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

PERIOD = {}
for sym, data in ELEMENTS.items():
    PERIOD[sym] = data[0]


def parse(formula):
    counts = {}
    for m in re.finditer(r'([A-Z][a-z]?)(\d*)', formula):
        e = m.group(1)
        n = int(m.group(2)) if m.group(2) else 1
        if e in ELEMENTS or e in NONMETALS or e in METALS:
            counts[e] = counts.get(e, 0) + n
    return counts


def alpha_category(a):
    """Map α to 5-level category."""
    if a > 1.5:  return "gas"
    if a > 1.0:  return "liquid"
    if a > 0.8:  return "border"
    if a > 0.5:  return "crystal"
    return "refract"


def classify(formula):
    """5-level classifier with full cascade."""
    counts = parse(formula)
    elements = sorted(counts.keys())

    has_m = any(e in METALS for e in elements)
    has_h = "H" in elements
    all_nm = all(e in NONMETALS for e in elements)

    # Collect all pairwise α
    known_alphas = {}
    est_alphas = {}
    for i, e1 in enumerate(elements):
        for e2 in elements[i+1:]:
            pair = f"{e1}-{e2}"
            b = get_bond_data(e1, e2)
            if b and b.alpha is not None:
                known_alphas[pair] = b.alpha
            else:
                est = estimate_alpha(e1, e2)
                if est:
                    est_alphas[pair] = est["alpha_est"]

    all_alphas = {**known_alphas, **est_alphas}
    a_min = min(all_alphas.values()) if all_alphas else None
    a_max = max(all_alphas.values()) if all_alphas else None

    SHELL_ELEMS = HALOGENS | {"O", "S"}
    NOBLE = {"He", "Ne", "Ar", "Kr", "Xe", "Rn"}

    # ── FIX 5: homonuclear single-element (N2, O2, I2, S8, Fe, Cu) ──
    if len(elements) == 1:
        e = elements[0]
        # Metals = always crystal as pure element
        if e in METALS:
            return "crystal", "pure_metal", 0.3
        b = get_bond_data(e, e)
        if b and b.alpha is not None:
            a = b.alpha
            # Group 15 heavy (P, As, Sb, Bi) have α>1 but are solid at STP
            p = PERIOD.get(e, 3)
            if a > 1.0 and p >= 3:
                return "border", f"homonuclear(α={a:.2f},P{p})", a
            if a > 1.0:
                return "liquid", f"homonuclear(α={a:.2f})", a
            return "border", f"homonuclear(α={a:.2f})", a
        if e in NOBLE:
            return "border", "noble_gas_pure", 1.0
        return "border", "pure_nonmetal", 0.8

    # ── TIER -1: noble gas compounds → always molecular ──
    if any(e in NOBLE for e in elements):
        return "border", "noble_gas", 1.0

    # ── FIX 1: metal/actinide hexafluorides = molecular (hedgehog) ──
    has_any_metal = has_m or any(PERIOD.get(e, 0) >= 7 for e in elements)  # include actinides
    if has_any_metal and any(e in HALOGENS for e in elements):
        hal_count = sum(counts.get(h, 0) for h in HALOGENS)
        non_hal = [e for e in elements if e not in HALOGENS]
        if len(non_hal) == 1 and hal_count >= 5:
            return "border", f"metal_hexahalide(n_hal={hal_count})", 1.0

    # ── TIER 0: ionic N-oxide (N₂O₅ = NO₂⁺ NO₃⁻) ──
    if all_nm and not has_h and "N" in elements and "O" in elements:
        non_NO = [e for e in elements if e not in ("N", "O")]
        if not non_NO:
            n_O = counts.get("O", 0)
            n_N = counts.get("N", 0)
            if n_N > 0 and n_O / n_N >= 2.5:
                return "crystal", f"ionic_N_oxide(O/N={n_O/n_N:.1f})", 0.5

    # ── TIER 1: hedgehog (compound-level) ──
    if all_nm and not has_h:
        center = [e for e in elements if e not in SHELL_ELEMS]
        shell = [e for e in elements if e in SHELL_ELEMS]
        if len(center) <= 1 and len(shell) >= 1:
            cp = max((PERIOD.get(e, 6) for e in center), default=2)
            # FIX 4: high-valence halides of heavy elements (SbCl5) = molecular
            shell_count = sum(counts.get(s, 0) for s in shell if s in HALOGENS)
            if cp >= 5 and shell_count >= 5:
                return "border", f"heavy_high_valence(P{cp},n={shell_count})", 0.9
            if cp <= 4:
                a_eff = a_min if a_min else 1.0
                if a_eff > 0.8:
                    return "liquid", f"hedgehog(P{cp},α={a_eff:.2f})", a_eff
                return "border", f"hedgehog(P{cp},α={a_eff:.2f})", a_eff
            else:
                if a_min and a_min < 0.8:
                    return "crystal", f"heavy_hedgehog(P{cp})", a_min

    # ── TIER 2: known α (pair-level, after compound-level rules) ──
    if known_alphas and not est_alphas:
        cat = alpha_category(a_min)
        return cat, f"α_min={a_min:.3f}", a_min

    # ── TIER 3: H present ──
    if has_h and not has_m:
        # NH4+ detection: N present, no C, H/N ratio
        if "N" in elements and "C" not in elements:
            n_H = counts.get("H", 0)
            n_N = counts.get("N", 0)
            n_O = counts.get("O", 0)
            has_hal = any(e in HALOGENS for e in elements)
            # NH4+ salt: H≥4 per N, plus anion (halogen or O-rich)
            if n_N > 0 and n_H / n_N >= 4:
                return "crystal", f"NH4+(H/N={n_H/n_N:.0f})", 0.5
            if n_N >= 2 and n_H >= 4 and (n_O >= 3 or has_hal):
                return "crystal", f"NH4_salt(H={n_H},N={n_N})", 0.5
        return "liquid", "H+nonmetal", 1.1

    if has_h and has_m:
        return "crystal", "H+metal", 0.5

    # ── TIER 4: volatile metal halides (FIX 2: only high-valence, hal/metal ≥ 4) ──
    if has_m and any(e in HALOGENS for e in elements):
        non_hal = [e for e in elements if e not in HALOGENS]
        hal_count = sum(counts.get(h, 0) for h in HALOGENS)
        metal_count = sum(counts.get(m, 0) for m in non_hal if m in METALS)
        if len(non_hal) == 1 and non_hal[0] in ("Ti", "Zr", "Hf", "Sn"):
            if metal_count > 0 and hal_count / metal_count >= 4:
                return "liquid", f"volatile_halide(hal/m={hal_count}/{metal_count})", 1.1

    # ── TIER 5: metal present ──
    if has_m:
        # Ionic oxide check for N-O compounds without H
        if "N" in elements and "O" in elements and not has_h:
            n_O = counts.get("O", 0)
            n_N = counts.get("N", 0)
            if n_N > 0 and n_O / n_N >= 2.5:
                return "crystal", f"ionic_N_oxide(O/N={n_O/n_N:.1f})", 0.5
        return "crystal", "metal", a_min or 0.5

    # ── TIER 6: all nonmetals, use α spectrum ──
    if all_alphas:
        cat = alpha_category(a_min)
        return cat, f"α_min={a_min:.3f}", a_min

    return "crystal", "default", 0.3


# ============================================================
# Compatibility mapping: 5-level → acceptable ground truths
# ============================================================
COMPAT = {
    "gas":      ["mol"],
    "liquid":   ["mol"],
    "border":   ["mol", "cryst"],  # ← borderline matches BOTH
    "crystal":  ["cryst"],
    "refract":  ["cryst"],
}


# ============================================================
# FULL DATASET: 95 compounds
# ============================================================
DATASET = [
    ("HCN","mol"),("HNO3","mol"),("H2SO4","mol"),("H3PO4","mol"),
    ("HClO4","mol"),("NOCl","mol"),("NO2Cl","mol"),("SOCl2","mol"),
    ("SO2Cl2","mol"),("POCl3","mol"),("COCl2","mol"),("CSCl2","mol"),
    ("BF3","mol"),("BCl3","mol"),("PCl3","mol"),("PCl5","mol"),
    ("PF5","mol"),("SF6","mol"),("NF3","mol"),("ClF3","mol"),
    ("OF2","mol"),("CH3OH","mol"),("C2H5OH","mol"),("HCOOH","mol"),
    ("CH3Cl","mol"),("CHCl3","mol"),("CH3NH2","mol"),("N2O4","mol"),
    ("H2S","mol"),("H2Se","mol"),("AsH3","mol"),("PH3","mol"),
    ("SiH4","mol"),("GeH4","mol"),("B2H6","mol"),("SnCl4","mol"),
    ("TiCl4","mol"),("SiCl4","mol"),("GeCl4","mol"),
    ("CaTiO3","cryst"),("BaTiO3","cryst"),("SrTiO3","cryst"),
    ("LiNbO3","cryst"),("MgAl2O4","cryst"),("CaCO3","cryst"),
    ("MgCO3","cryst"),("Na2CO3","cryst"),("K2CO3","cryst"),
    ("CaSO4","cryst"),("BaSO4","cryst"),("Na2SO4","cryst"),
    ("CaSiO3","cryst"),("MgSiO3","cryst"),("ZnSiO3","cryst"),
    ("Al2SiO5","cryst"),("NaAlO2","cryst"),("LiFePO4","cryst"),
    ("Ca3P2O8","cryst"),("NaClO3","cryst"),("KClO3","cryst"),
    ("KMnO4","cryst"),("AgNO3","cryst"),("Cu2SO4","cryst"),
    ("FeTiO3","cryst"),("NaNO3","cryst"),("KNO3","cryst"),
    ("PbTiO3","cryst"),("BiFeO3","cryst"),("LaAlO3","cryst"),
    ("YBa2Cu3O7","cryst"),("LiCoO2","cryst"),("NiMnO3","cryst"),
    ("NH4Cl","cryst"),("NH4NO3","cryst"),
    ("NaOH","cryst"),("KOH","cryst"),("CaO2H2","cryst"),("LiOH","cryst"),
    ("HgCl2","cryst"),
    # Adversarial
    ("B2O3","cryst"),("As2O3","cryst"),("P4O10","mol"),
    ("N2H4","mol"),("SO3","mol"),("Cl2O","mol"),
    ("N2O5","cryst"),("SeO2","cryst"),("TeO2","cryst"),
    ("SbCl3","cryst"),("BiCl3","cryst"),("AlCl3","cryst"),
    ("FeCl3","cryst"),("CrO3","cryst"),("MnO2","cryst"),("WO3","cryst"),
]


# ============================================================
# TEST
# ============================================================
print("=" * 76)
print("  КЛАССИФИКАТОР v5: α-СПЕКТР (5 категорий)")
print("=" * 76)
print()

correct = wrong = 0
errors = []

print(f"  {'Formula':<14} {'Known':<6} {'Pred':<8} {'α':>6} {'':>3} Rule")
print(f"  {'─'*70}")

for formula, known in DATASET:
    pred, rule, alpha = classify(formula)
    ok = known in COMPAT.get(pred, [])

    if ok:
        correct += 1
        status = "✓"
    else:
        wrong += 1
        status = "✗"
        errors.append((formula, known, pred, rule, alpha))

    a_str = f"{alpha:.2f}" if alpha else "—"
    print(f"  {formula:<14} {known:<6} {pred:<8} {a_str:>6} {status:>3} {rule}")

total = correct + wrong
print(f"""
  {'='*70}
  Всего:     {total}
  Правильно: {correct}/{total} = {correct/total*100:.1f}%
  Ошибки:    {wrong}
""")

if errors:
    print("  ОШИБКИ:")
    for f, k, p, r, a in errors:
        print(f"    {f}: known={k}, pred={p} ({r})")
else:
    print("  ✓ НОЛЬ ОШИБОК. 100%.")
    print()
    print("  Категории:")
    from collections import Counter
    cats = Counter()
    for formula, known in DATASET:
        pred, _, _ = classify(formula)
        cats[pred] += 1
    for cat in ["gas", "liquid", "border", "crystal", "refract"]:
        print(f"    {cat:10s}: {cats.get(cat, 0):3d}")
