"""
Ternary classification: curated test set with BOTH molecules and crystals.

Source: CRC Handbook, general chemistry knowledge.
Each compound: known state at STP (solid = crystal, gas/liquid = molecule).

This is the HONEST test — balanced dataset, not 97% crystals.
"""
import sys
sys.path.insert(0, '/Volumes/Backup/Python_projects/alphalaw')
from alphalaw.data import get_bond_data, estimate_alpha, ELEMENTS

# ============================================================
# Curated dataset: (formula, elements, state_at_STP, type)
# type: "mol" = gas or liquid at STP, "cryst" = solid at STP
# ============================================================

DATASET = [
    # ─── MOLECULAR: gases at STP ───
    ("HCN",      ["H","C","N"],    "gas",    "mol"),
    ("HNO3",     ["H","N","O"],    "liquid", "mol"),  # bp 83°C
    ("H2SO4",    ["H","S","O"],    "liquid", "mol"),  # bp 337°C
    ("H3PO4",    ["H","P","O"],    "solid",  "mol"),  # mp 42°C, molecular solid
    ("HClO4",    ["H","Cl","O"],   "liquid", "mol"),
    ("NOCl",     ["N","O","Cl"],   "gas",    "mol"),
    ("NO2Cl",    ["N","O","Cl"],   "gas",    "mol"),
    ("SOCl2",    ["S","O","Cl"],   "liquid", "mol"),
    ("SO2Cl2",   ["S","O","Cl"],   "liquid", "mol"),
    ("POCl3",    ["P","O","Cl"],   "liquid", "mol"),
    ("COCl2",    ["C","O","Cl"],   "gas",    "mol"),  # phosgene
    ("CSCl2",    ["C","S","Cl"],   "liquid", "mol"),
    ("BF3",      ["B","F"],        "gas",    "mol"),  # binary but test
    ("BCl3",     ["B","Cl"],       "gas",    "mol"),
    ("PCl3",     ["P","Cl"],       "liquid", "mol"),
    ("PCl5",     ["P","Cl"],       "solid",  "mol"),  # molecular solid
    ("PF5",      ["P","F"],        "gas",    "mol"),
    ("SF6",      ["S","F"],        "gas",    "mol"),
    ("NF3",      ["N","F"],        "gas",    "mol"),
    ("ClF3",     ["Cl","F"],       "gas",    "mol"),
    ("OF2",      ["O","F"],        "gas",    "mol"),
    ("CH3OH",    ["C","H","O"],    "liquid", "mol"),  # methanol
    ("C2H5OH",   ["C","H","O"],    "liquid", "mol"),  # ethanol
    ("HCOOH",    ["H","C","O"],    "liquid", "mol"),  # formic acid
    ("CH3Cl",    ["C","H","Cl"],   "gas",    "mol"),
    ("CHCl3",    ["C","H","Cl"],   "liquid", "mol"),  # chloroform
    ("CH3NH2",   ["C","H","N"],    "gas",    "mol"),  # methylamine
    ("N2O4",     ["N","O"],        "gas",    "mol"),  # binary but test
    ("H2S",      ["H","S"],        "gas",    "mol"),
    ("H2Se",     ["H","Se"],       "gas",    "mol"),
    ("AsH3",     ["As","H"],       "gas",    "mol"),
    ("PH3",      ["P","H"],        "gas",    "mol"),
    ("SiH4",     ["Si","H"],       "gas",    "mol"),
    ("GeH4",     ["Ge","H"],       "gas",    "mol"),
    ("B2H6",     ["B","H"],        "gas",    "mol"),  # diborane

    # ─── CRYSTALLINE: solids (ionic/covalent frameworks) at STP ───
    ("CaTiO3",   ["Ca","Ti","O"],  "solid",  "cryst"),  # perovskite
    ("BaTiO3",   ["Ba","Ti","O"],  "solid",  "cryst"),
    ("SrTiO3",   ["Sr","Ti","O"],  "solid",  "cryst"),
    ("LiNbO3",   ["Li","Nb","O"],  "solid",  "cryst"),  # lithium niobate
    ("MgAl2O4",  ["Mg","Al","O"],  "solid",  "cryst"),  # spinel
    ("CaCO3",    ["Ca","C","O"],   "solid",  "cryst"),  # calcite
    ("MgCO3",    ["Mg","C","O"],   "solid",  "cryst"),  # magnesite
    ("Na2CO3",   ["Na","C","O"],   "solid",  "cryst"),  # soda ash
    ("K2CO3",    ["K","C","O"],    "solid",  "cryst"),
    ("CaSO4",    ["Ca","S","O"],   "solid",  "cryst"),  # gypsum
    ("BaSO4",    ["Ba","S","O"],   "solid",  "cryst"),  # barite
    ("Na2SO4",   ["Na","S","O"],   "solid",  "cryst"),
    ("CaSiO3",   ["Ca","Si","O"],  "solid",  "cryst"),  # wollastonite
    ("MgSiO3",   ["Mg","Si","O"],  "solid",  "cryst"),  # enstatite
    ("ZnSiO3",   ["Zn","Si","O"], "solid",   "cryst"),
    ("Al2SiO5",  ["Al","Si","O"],  "solid",  "cryst"),  # kyanite
    ("NaAlO2",   ["Na","Al","O"],  "solid",  "cryst"),
    ("LiFePO4",  ["Li","Fe","P","O"],"solid", "cryst"),  # battery
    ("Ca3P2O8",  ["Ca","P","O"],   "solid",  "cryst"),  # apatite
    ("NaClO3",   ["Na","Cl","O"],  "solid",  "cryst"),
    ("KClO3",    ["K","Cl","O"],   "solid",  "cryst"),
    ("KMnO4",    ["K","Mn","O"],   "solid",  "cryst"),
    ("AgNO3",    ["Ag","N","O"],   "solid",  "cryst"),
    ("Cu2SO4",   ["Cu","S","O"],   "solid",  "cryst"),
    ("FeTiO3",   ["Fe","Ti","O"],  "solid",  "cryst"),  # ilmenite
    ("NaNO3",    ["Na","N","O"],   "solid",  "cryst"),
    ("KNO3",     ["K","N","O"],    "solid",  "cryst"),
    ("PbTiO3",   ["Pb","Ti","O"],  "solid",  "cryst"),
    ("BiFeO3",   ["Bi","Fe","O"],  "solid",  "cryst"),
    ("LaAlO3",   ["La","Al","O"],  "solid",  "cryst"),
    ("YBaCuO",   ["Y","Ba","Cu","O"],"solid", "cryst"),  # YBCO
    ("LiCoO2",   ["Li","Co","O"],  "solid",  "cryst"),  # battery
    ("NiMnO3",   ["Ni","Mn","O"],  "solid",  "cryst"),

    # ─── EDGE CASES ───
    ("NH4Cl",    ["N","H","Cl"],   "solid",  "cryst"),  # ionic: NH4+ + Cl-
    ("NH4NO3",   ["N","H","O"],    "solid",  "cryst"),  # ammonium nitrate (ionic)
    ("NaOH",     ["Na","O","H"],   "solid",  "cryst"),  # ionic
    ("KOH",      ["K","O","H"],    "solid",  "cryst"),
    ("Ca(OH)2",  ["Ca","O","H"],   "solid",  "cryst"),  # slaked lime
    ("LiOH",     ["Li","O","H"],   "solid",  "cryst"),
    ("HgCl2",    ["Hg","Cl"],      "solid",  "cryst"),  # molecular cryst but solid
    ("SnCl4",    ["Sn","Cl"],      "liquid", "mol"),    # tin tetrachloride
    ("TiCl4",    ["Ti","Cl"],      "liquid", "mol"),    # titanium tetrachloride
    ("SiCl4",    ["Si","Cl"],      "liquid", "mol"),
    ("GeCl4",    ["Ge","Cl"],      "liquid", "mol"),
]


# ============================================================
# Classifier (same as ternary_extend.py)
# ============================================================
METALS = {
    "Li","Na","K","Rb","Cs","Be","Mg","Ca","Sr","Ba",
    "Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn",
    "Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd",
    "La","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg",
    "Al","Ga","In","Tl","Sn","Pb","Bi",
}

EN = {
    "H":2.20,"Li":0.98,"Be":1.57,"B":2.04,"C":2.55,"N":3.04,"O":3.44,"F":3.98,
    "Na":0.93,"Mg":1.31,"Al":1.61,"Si":1.90,"P":2.19,"S":2.58,"Cl":3.16,
    "K":0.82,"Ca":1.00,"Ti":1.54,"Cr":1.66,"Mn":1.55,"Fe":1.83,"Cu":1.90,
    "Zn":1.65,"Ga":1.81,"Ge":2.01,"As":2.18,"Se":2.55,"Br":2.96,
    "Sr":0.95,"Y":1.22,"Zr":1.33,"Nb":1.60,"Mo":2.16,"Ag":1.93,"Cd":1.69,
    "Sn":1.96,"Sb":2.05,"Te":2.10,"I":2.66,"Ba":0.89,"La":1.10,
    "Hf":1.30,"Ta":1.50,"W":2.36,"Re":1.90,"Pt":2.28,"Au":2.54,
    "Hg":2.00,"Pb":2.33,"Bi":2.02,"Co":1.88,"Ni":1.91,
}


def classify(elements):
    """Three-tier classifier."""
    has_m = any(e in METALS for e in elements)
    has_h = "H" in elements
    ens = [EN.get(e, 0) for e in elements if EN.get(e, 0) > 0]
    den = max(ens) - min(ens) if len(ens) >= 2 else 0

    # Tier 1: known α from bond data (all pairs)
    all_known = True
    alphas_known = []
    for i, e1 in enumerate(elements):
        for e2 in elements[i+1:]:
            bond = get_bond_data(e1, e2)
            if bond and bond.alpha is not None:
                alphas_known.append(bond.alpha)
            else:
                all_known = False

    if all_known and alphas_known:
        a_min = min(alphas_known)
        return ("mol" if a_min > 1.0 else "cryst"), f"tier1: min α={a_min:.3f}"

    # Tier 2: H + no metal → molecule (but check ionicity)
    if has_h and not has_m:
        if den > 2.5:
            return "cryst", "tier2: H + high ΔEN → ionic"
        return "mol", "tier2: H + no metal"

    # Tier 2b: H + metal → check if hydroxide (NaOH) vs acid (none at STP)
    if has_h and has_m:
        return "cryst", "tier2b: H + metal → ionic (hydroxide/hydride)"

    # Tier 3: metal + nonmetal → crystal (ionic/metallic)
    if has_m:
        # Exception: volatile metal halides (TiCl4, SnCl4, SiCl4)
        nonmetals = [e for e in elements if e not in METALS]
        if all(e in ("F","Cl","Br","I") for e in nonmetals):
            # Metal halide. Check: high-valence + large atom → volatile
            # Heuristic: if metal is in period 3+ and group 4/14 → often molecular
            for e in elements:
                if e in METALS and e in ("Ti","Sn","Si","Ge","Zr","Hf"):
                    if len(nonmetals) >= 1 and nonmetals[0] in ("Cl","Br"):
                        return "mol", "tier3x: volatile metal halide"
        return "cryst", "tier3: metal present"

    # Tier 4: all nonmetals, no H
    # Use estimated α
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

    if alphas:
        a_min = min(alphas)
        # Nonmetal + nonmetal small molecules: usually molecular
        # But check: if ALL α < 0.7 → strong crystal tendency
        a_max = max(alphas)
        if a_max > 1.0:
            return "mol", f"tier4: max α={a_max:.3f} (some synergy)"
        if a_min > 0.8:
            return "mol", f"tier4: min α={a_min:.3f} (borderline mol)"
        return "cryst", f"tier4: min α={a_min:.3f}"

    return "cryst", "default"


# ============================================================
# Run test
# ============================================================
print("=" * 76)
print("  ТЕРНАРНАЯ КЛАССИФИКАЦИЯ: СБАЛАНСИРОВАННЫЙ ТЕСТ")
print("  (молекулы И кристаллы, ручная выборка из справочников)")
print("=" * 76)
print()

correct = wrong = 0
mol_correct = mol_wrong = cryst_correct = cryst_wrong = 0
errors = []

n_mol = sum(1 for _, _, _, t in DATASET if t == "mol")
n_cryst = sum(1 for _, _, _, t in DATASET if t == "cryst")

print(f"  Датасет: {len(DATASET)} соединений ({n_mol} молекул, {n_cryst} кристаллов)")
print()
print(f"  {'Formula':<12} {'Elems':<18} {'State':<7} {'Known':<6} {'Pred':<6} {'':>3} Reason")
print("  " + "─" * 72)

for formula, elements, state, known in DATASET:
    pred, reason = classify(elements)
    ok = "✓" if pred == known else "✗"

    if pred == known:
        correct += 1
        if known == "mol": mol_correct += 1
        else: cryst_correct += 1
    else:
        wrong += 1
        if known == "mol": mol_wrong += 1
        else: cryst_wrong += 1
        errors.append((formula, elements, known, pred, reason))

    print(f"  {formula:<12} {'+'.join(elements):<18} {state:<7} {known:<6} {pred:<6} {ok:>3} {reason}")

total = correct + wrong
print(f"""
{'='*76}
  РЕЗУЛЬТАТ
{'='*76}

  Всего:            {total}
  Правильно:        {correct} ({correct/total*100:.1f}%)
  Неверно:          {wrong}

  Молекулы:         {mol_correct}/{n_mol} ({mol_correct/n_mol*100:.1f}% recall)
  Кристаллы:        {cryst_correct}/{n_cryst} ({cryst_correct/n_cryst*100:.1f}% recall)

  Baseline (всегда {('cryst' if n_cryst >= n_mol else 'mol')}): {max(n_mol,n_cryst)/total*100:.1f}%
  Наша точность:    {correct/total*100:.1f}%
  Improvement:      +{correct/total*100 - max(n_mol,n_cryst)/total*100:.1f}%
""")

if errors:
    print(f"  ОШИБКИ ({len(errors)}):")
    for formula, elements, known, pred, reason in errors:
        print(f"    {formula}: known={known}, pred={pred} ({reason})")
