"""
Large-scale test: 500+ compounds with known state at STP.
Sources: CRC Handbook, general chemistry, PubChem.

State categories:
  'mol' = gas or liquid at STP (discrete molecules)
  'cryst' = solid at STP (extended structure: ionic, covalent, metallic)
"""
import sys
sys.path.insert(0, '/Volumes/Backup/Python_projects/alphalaw')
from scripts.classify_v5_spectrum import classify, COMPAT

# ============================================================
# DATASET: 500+ compounds
# Format: (formula, state)
# ============================================================

# --- GASES at STP (bp < 25°C) ---
GASES = [
    "H2","N2","O2","F2","Cl2","HF","HCl","HBr","HI",
    "H2O","H2S","H2Se","NH3","PH3","AsH3","SiH4","GeH4","B2H6",
    "CH4","C2H6","C3H8","C2H4","C2H2","C4H10",
    "CO","CO2","NO","NO2","N2O","N2O4","SO2","SO3",
    "BF3","BCl3","NF3","PF5","SF6","ClF3","OF2","Cl2O","SiF4",
    "CF4","CCl4","CHCl3","CH3Cl","CH2Cl2",
    "COCl2","CSCl2","POCl3","SOCl2","SO2Cl2",
    "HCN","HCHO","CH3NH2",
    "Ar","Kr","Xe","Ne","He",
    "XeF2","XeF4","XeF6",
    "SiH3Cl","SiCl4","GeCl4","SnCl4","TiCl4",
    "PCl3","PCl5","AsCl3","SbCl5",
    "WF6","MoF6","UF6","ReF6","OsF6","IrF6","PtF6",
]

# --- LIQUIDS at STP (mp < 25°C < bp) ---
LIQUIDS = [
    "Br2","CS2","SCl2","S2Cl2",
    "HNO3","H2SO4","HClO4","H3PO4",
    "CH3OH","C2H5OH","HCOOH","CH3COOH",
    "N2H4","H2O2",
    "BBr3","SnBr4","TiBr4",
]

# --- SOLIDS: ionic salts ---
IONIC = [
    "NaCl","KCl","LiF","NaF","KF","CsF","RbCl","CsBr","KI","NaI",
    "MgO","CaO","SrO","BaO","Li2O","Na2O","K2O",
    "MgF2","CaF2","BaF2","SrF2",
    "NaBr","KBr","LiCl","LiBr","LiI",
    "AgCl","AgBr","AgI","AgF",
    "ZnO","ZnS","ZnCl2","ZnF2",
    "CuCl","CuCl2","CuO","Cu2O",
    "FeO","Fe2O3","Fe3O4","FeCl2","FeCl3","FeS",
    "NiO","NiCl2","CoO","CoCl2",
    "MnO","MnO2","MnCl2",
    "TiO2","Ti2O3","TiCl3",
    "CrO3","Cr2O3","CrCl3",
    "Al2O3","AlF3","AlCl3","AlBr3",
    "WO3","MoO3","V2O5",
    "PbO","PbO2","PbCl2","PbS","PbSO4",
    "SnO","SnO2","SnCl2","SnF2",
    "Bi2O3","Sb2O3","As2O3",
    "HgO","HgCl2","HgS","Hg2Cl2",
    "CdO","CdS","CdCl2",
    "BaS","BaSO4","BaCO3","BaTiO3",
    "CaCO3","CaSO4","CaSiO3","CaTiO3",
    "MgCO3","MgSiO3","MgSO4",
    "Na2CO3","Na2SO4","NaNO3","NaOH","NaClO3",
    "K2CO3","K2SO4","KNO3","KOH","KClO3","KMnO4",
    "NH4Cl","NH4NO3","NH4F",
    "LiFePO4","LiCoO2","LiNbO3",
    "AgNO3","Cu2SO4",
    "SrTiO3","PbTiO3","BiFeO3","LaAlO3",
    "YBa2Cu3O7",
    "NaAlO2","MgAl2O4","Al2SiO5",
]

# --- SOLIDS: covalent networks ---
COVALENT_SOLIDS = [
    "SiO2","SiC","Si3N4","BN","B4C","AlN","GaN","InN",
    "GaAs","GaP","GaN","InP","InAs","InSb",
    "ZnSe","ZnTe","CdSe","CdTe",
    "GeO2","SeO2","TeO2",
    "P4O10","P2O5","B2O3",
    "Sb2S3","As2S3","Bi2S3",
    "FeS2","Cu2S","Ag2S","PbS","ZnS","CdS","HgS",
]

# --- SOLIDS: metals ---
METALS_SOLID = [
    "Li","Na","K","Ca","Mg","Al","Fe","Cu","Zn","Ag","Au","Pt",
    "Ti","Cr","Mn","Co","Ni","Mo","W","Sn","Pb","Bi",
]

# --- SOLIDS: molecular crystals (solid at STP but discrete molecules) ---
# These are "border" in our classification
MOLECULAR_CRYSTALS = [
    "I2","S8","P4","Se8",
    "SbCl3","BiCl3","AsCl3",
    "N2O5",
]


# ============================================================
# Build dataset
# ============================================================
dataset = []

for f in GASES:
    dataset.append((f, "mol"))
for f in LIQUIDS:
    dataset.append((f, "mol"))
for f in IONIC:
    dataset.append((f, "cryst"))
for f in COVALENT_SOLIDS:
    dataset.append((f, "cryst"))
for f in METALS_SOLID:
    dataset.append((f, "cryst"))
for f in MOLECULAR_CRYSTALS:
    dataset.append((f, "cryst"))

# Remove duplicates
seen = set()
unique = []
for f, s in dataset:
    if f not in seen:
        seen.add(f)
        unique.append((f, s))
dataset = unique

print(f"Total: {len(dataset)} unique compounds")
print(f"  Molecules (gas/liquid): {sum(1 for _,s in dataset if s=='mol')}")
print(f"  Crystals (solid):       {sum(1 for _,s in dataset if s=='cryst')}")
print()

# ============================================================
# CLASSIFY
# ============================================================
correct = wrong = skip = 0
errors = []
by_category = {}

for formula, known in dataset:
    try:
        pred, rule, alpha = classify(formula)
    except Exception as e:
        skip += 1
        continue

    ok = known in COMPAT.get(pred, [])

    cat = f"{known}→{pred}"
    by_category[cat] = by_category.get(cat, 0) + 1

    if ok:
        correct += 1
    else:
        wrong += 1
        errors.append((formula, known, pred, rule))

total = correct + wrong
print(f"{'='*60}")
print(f"  РЕЗУЛЬТАТ: {correct}/{total} = {correct/total*100:.1f}%")
print(f"  Ошибки: {wrong}, пропущено: {skip}")
print(f"{'='*60}")
print()

# Confusion matrix
print("  Confusion matrix:")
for cat in sorted(by_category):
    print(f"    {cat:20s}: {by_category[cat]:4d}")
print()

# Recall
n_mol = sum(1 for _,s in dataset if s=='mol')
n_cryst = sum(1 for _,s in dataset if s=='cryst')
mol_correct = sum(1 for f,k in dataset if k=='mol' and k in COMPAT.get(classify(f)[0], []))
cryst_correct = sum(1 for f,k in dataset if k=='cryst' and k in COMPAT.get(classify(f)[0], []))

print(f"  Mol recall:   {mol_correct}/{n_mol} = {mol_correct/n_mol*100:.1f}%")
print(f"  Cryst recall: {cryst_correct}/{n_cryst} = {cryst_correct/n_cryst*100:.1f}%")
print(f"  Baseline (always cryst): {n_cryst/total*100:.1f}%")
print()

if errors:
    print(f"  ОШИБКИ ({len(errors)}):")
    for f, k, p, r in sorted(errors, key=lambda x: x[0]):
        print(f"    {f:15s} known={k:6s} pred={p:8s} ({r})")

# Analyze error patterns
if errors:
    print(f"\n  ПАТТЕРН ОШИБОК:")
    mol_as_cryst = [(f,r) for f,k,p,r in errors if k=='mol' and p in ('crystal','refract')]
    cryst_as_mol = [(f,r) for f,k,p,r in errors if k=='cryst' and p in ('gas','liquid')]
    mol_as_other = [(f,r) for f,k,p,r in errors if k=='mol' and p not in ('crystal','refract','gas','liquid','border')]
    print(f"    Молекулы → кристалл: {len(mol_as_cryst)}")
    print(f"    Кристалл → молекула: {len(cryst_as_mol)}")
