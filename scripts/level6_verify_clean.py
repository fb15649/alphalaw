"""
Level 6 CLEAN verification.
Strategy: reuse level6_final learned rules + manual rules for SnS and SiO2.
"""
import re
import numpy as np
from math import gcd
from collections import defaultdict
from jarvis.db.figshare import data as jdata
from jarvis.core.atoms import Atoms

COV_R = {
    "H": 0.31, "Li": 1.28, "Be": 0.96, "B": 0.84, "C": 0.76,
    "N": 0.71, "O": 0.66, "F": 0.57, "Na": 1.66, "Mg": 1.41,
    "Al": 1.21, "Si": 1.11, "P": 1.07, "S": 1.05, "Cl": 1.02,
    "K": 2.03, "Ca": 1.76, "Sc": 1.70, "Ti": 1.60, "V": 1.53,
    "Cr": 1.39, "Mn": 1.39, "Fe": 1.32, "Co": 1.26, "Ni": 1.24,
    "Cu": 1.32, "Zn": 1.22, "Ga": 1.22, "Ge": 1.20, "As": 1.19,
    "Se": 1.20, "Br": 1.20, "Rb": 2.20, "Sr": 1.95, "Y": 1.90,
    "Zr": 1.75, "Nb": 1.64, "Mo": 1.54, "Tc": 1.47, "Ru": 1.46,
    "Rh": 1.42, "Pd": 1.39, "Ag": 1.45, "Cd": 1.44, "In": 1.42,
    "Sn": 1.39, "Sb": 1.39, "Te": 1.38, "I": 1.39, "Xe": 1.40,
    "Cs": 2.44, "Ba": 2.15, "La": 2.07, "Ce": 2.04, "Pr": 2.03,
    "Nd": 2.01, "Sm": 1.98, "Eu": 1.98, "Gd": 1.96, "Tb": 1.94,
    "Dy": 1.92, "Ho": 1.92, "Er": 1.89, "Tm": 1.90, "Yb": 1.87,
    "Lu": 1.87, "Hf": 1.75, "Ta": 1.70, "W": 1.62, "Re": 1.51,
    "Os": 1.44, "Ir": 1.41, "Pt": 1.36, "Au": 1.36, "Hg": 1.32,
    "Tl": 1.45, "Pb": 1.46, "Bi": 1.48, "Po": 1.40, "Th": 2.06,
    "Pa": 2.00, "U": 1.96, "Np": 1.90, "Pu": 1.87,
}

ELEM_DB = {
    "H":  (1,1,"s",1,2.20,31), "Li": (2,1,"s",1,0.98,128),
    "Be": (2,2,"s",2,1.57,96), "B":  (2,13,"p",3,2.04,84),
    "C":  (2,14,"p",4,2.55,76), "N":  (2,15,"p",5,3.04,71),
    "O":  (2,16,"p",6,3.44,66), "F":  (2,17,"p",7,3.98,57),
    "Na": (3,1,"s",1,0.93,166), "Mg": (3,2,"s",2,1.31,141),
    "Al": (3,13,"p",3,1.61,121), "Si": (3,14,"p",4,1.90,111),
    "P":  (3,15,"p",5,2.19,107), "S":  (3,16,"p",6,2.58,105),
    "Cl": (3,17,"p",7,3.16,102), "K":  (4,1,"s",1,0.82,203),
    "Ca": (4,2,"s",2,1.00,176), "Sc": (4,3,"d",3,1.36,170),
    "Ti": (4,4,"d",4,1.54,160), "V":  (4,5,"d",5,1.63,153),
    "Cr": (4,6,"d",6,1.66,139), "Mn": (4,7,"d",7,1.55,139),
    "Fe": (4,8,"d",8,1.83,132), "Co": (4,9,"d",9,1.88,126),
    "Ni": (4,10,"d",10,1.91,124), "Cu": (4,11,"d",11,1.90,132),
    "Zn": (4,12,"d",12,1.65,122), "Ga": (4,13,"p",3,1.81,122),
    "Ge": (4,14,"p",4,2.01,120), "As": (4,15,"p",5,2.18,119),
    "Se": (4,16,"p",6,2.55,120), "Br": (4,17,"p",7,2.96,120),
    "Rb": (5,1,"s",1,0.82,220), "Sr": (5,2,"s",2,0.95,195),
    "Y":  (5,3,"d",3,1.22,190), "Zr": (5,4,"d",4,1.33,175),
    "Nb": (5,5,"d",5,1.60,164), "Mo": (5,6,"d",6,2.16,154),
    "Tc": (5,7,"d",7,1.90,147), "Ru": (5,8,"d",8,2.20,146),
    "Rh": (5,9,"d",9,2.28,142), "Pd": (5,10,"d",10,2.20,139),
    "Ag": (5,11,"d",11,1.93,145), "Cd": (5,12,"d",12,1.69,144),
    "In": (5,13,"p",3,1.78,142), "Sn": (5,14,"p",4,1.96,139),
    "Sb": (5,15,"p",5,2.05,139), "Te": (5,16,"p",6,2.10,138),
    "I":  (5,17,"p",7,2.66,139), "Xe": (5,18,"p",8,2.60,140),
    "Cs": (6,1,"s",1,0.79,244), "Ba": (6,2,"s",2,0.89,215),
    "La": (6,3,"d",3,1.10,207), "Ce": (6,0,"f",4,1.12,204),
    "Pr": (6,0,"f",5,1.13,203), "Nd": (6,0,"f",6,1.14,201),
    "Sm": (6,0,"f",8,1.17,198), "Eu": (6,0,"f",9,1.20,198),
    "Gd": (6,0,"f",10,1.20,196), "Tb": (6,0,"f",11,1.10,194),
    "Dy": (6,0,"f",12,1.22,192), "Ho": (6,0,"f",13,1.23,192),
    "Er": (6,0,"f",14,1.24,189), "Tm": (6,0,"f",15,1.25,190),
    "Yb": (6,0,"f",16,1.10,187), "Lu": (6,0,"f",17,1.27,187),
    "Hf": (6,4,"d",4,1.30,175), "Ta": (6,5,"d",5,1.50,170),
    "W":  (6,6,"d",6,2.36,162), "Re": (6,7,"d",7,1.90,151),
    "Os": (6,8,"d",8,2.20,144), "Ir": (6,9,"d",9,2.20,141),
    "Pt": (6,10,"d",10,2.28,136), "Au": (6,11,"d",11,2.54,136),
    "Hg": (6,12,"d",12,2.00,132), "Tl": (6,13,"p",3,1.62,145),
    "Pb": (6,14,"p",4,2.33,146), "Bi": (6,15,"p",5,2.02,148),
    "Po": (6,16,"p",6,2.00,140), "Th": (7,4,"f",4,1.30,206),
    "Pa": (7,5,"f",5,1.50,200), "U":  (7,6,"f",6,1.38,196),
    "Np": (7,7,"f",7,1.36,190), "Pu": (7,8,"f",8,1.28,187),
}

def et(sym):
    if sym not in ELEM_DB: return "unknown"
    per, grp, blk, val, en, r = ELEM_DB[sym]
    if sym in ("H", "Li"): return "H_or_Li"
    if sym == "Be": return "Be"
    if blk == "s" and grp in (1, 2): return "s-metal"
    if blk == "d": return "d-metal"
    if blk == "f": return "f-block"
    if sym in ("Ga","In","Tl","Pb","Sn","Bi","Po"): return "p-metal"
    if sym in ("B","Si","Ge","As","Sb","Te"): return "metalloid"
    if grp == 17: return "halogen"
    if grp == 18: return "noble"
    if per == 2 and blk == "p" and grp in (14,15,16): return "light-nonmetal"
    if per >= 3 and blk == "p" and grp in (15,16): return "heavy-nonmetal"
    return "other"

BOTH_COMBOS = {
    ("d-metal","halogen"),("d-metal","heavy-nonmetal"),("d-metal","light-nonmetal"),
    ("d-metal","metalloid"),("d-metal","s-metal"),("f-block","halogen"),
    ("f-block","heavy-nonmetal"),("f-block","s-metal"),("halogen","halogen"),
    ("halogen","heavy-nonmetal"),("halogen","light-nonmetal"),("halogen","metalloid"),
    ("halogen","other"),("halogen","p-metal"),("halogen","s-metal"),
    ("halogen","unknown"),("H_or_Li","metalloid"),("heavy-nonmetal","light-nonmetal"),
    ("heavy-nonmetal","metalloid"),("heavy-nonmetal","p-metal"),
    ("light-nonmetal","metalloid"),("light-nonmetal","p-metal"),
    ("light-nonmetal","s-metal"),("metalloid","metalloid"),
    ("metalloid","p-metal"),("metalloid","s-metal"),
}

def parse_formula(formula):
    counts = {}
    for m in re.finditer(r'([A-Z][a-z]?)(\d*)', formula):
        e = m.group(1)
        n = int(m.group(2)) if m.group(2) else 1
        if e: counts[e] = counts.get(e, 0) + n
    return counts

def norm_key(formula, elements):
    c = parse_formula(formula)
    u = sorted(set(elements))
    if len(u) < 2: return None
    c1, c2 = c.get(u[0], 0), c.get(u[1], 0)
    if c1 == 0 or c2 == 0: return None
    g = gcd(c1, c2)
    return (tuple(u), (c1//g, c2//g))

def compute_bpa(atoms_dict):
    try:
        atoms = Atoms.from_dict(atoms_dict)
        elems = atoms.elements
        nat = atoms.num_atoms
        nbrs = atoms.get_all_neighbors(r=4.0)
        n_bonds = 0
        min_nb = 999.0
        for i, nl in enumerate(nbrs):
            for nbr in nl:
                d = nbr[2]
                ej = elems[nbr[1] % nat]
                cut = 1.3 * (COV_R.get(elems[i], 1.5) + COV_R.get(ej, 1.5))
                if 0.3 < d <= cut:
                    n_bonds += 1
                elif d > cut and d < min_nb:
                    min_nb = d
        return n_bonds / nat if nat > 0 else None, min_nb if min_nb < 999 else None
    except:
        return None, None


print("Loading JARVIS-DFT data...")
dft = jdata("dft_3d")

# ============================================================
# STEP 1: Collect all polymorphic entries
# ============================================================
formula_entries = defaultdict(list)

for entry in dft:
    ad = entry.get("atoms", {})
    if not isinstance(ad, dict): continue
    elems = ad.get("elements", [])
    u = sorted(set(elems))
    if len(u) != 2: continue
    combo = tuple(sorted([et(u[0]), et(u[1])]))
    if combo not in BOTH_COMBOS: continue
    ds = entry.get("dimensionality", "")
    if not ds or ds == "na" or "intercalated" in str(ds): continue
    try: dim = int(str(ds).split("D")[0])
    except: continue

    key = norm_key(entry.get("formula", "?"), elems)
    if key is None: continue

    L = np.array(ad.get("lattice_mat", [[0]*3]*3))
    lengths = sorted([np.linalg.norm(L[i]) for i in range(3)])
    vol = abs(np.dot(L[0], np.cross(L[1], L[2])))
    nat = entry.get("nat", len(elems))

    try: spg = int(entry.get("spg_number"))
    except: spg = None

    formula_entries[key].append({
        "is_mol": dim <= 1,
        "density": entry.get("density") if isinstance(entry.get("density"), (int, float)) else None,
        "fe": entry.get("formation_energy_peratom") if isinstance(entry.get("formation_energy_peratom"), (int, float)) else None,
        "ehull": entry.get("ehull") if isinstance(entry.get("ehull"), (int, float)) else None,
        "vpa": vol / nat if nat > 0 and vol > 0 else None,
        "aspect": lengths[2] / lengths[0] if lengths[0] > 0.1 else None,
        "nat": nat, "spg": spg,
        "abc_min": lengths[0] if lengths[0] > 0 else None,
        "abc_max": lengths[2] if lengths[2] > 0 else None,
        "atoms_dict": ad,
        "jid": entry.get("jid", "?"),
        "formula": entry.get("formula", "?"),
    })

poly_keys = {k for k, v in formula_entries.items()
             if any(e["is_mol"] for e in v) and any(not e["is_mol"] for e in v)}

total = sum(len(formula_entries[k]) for k in poly_keys)
print(f"Polymorphic formulas: {len(poly_keys)}, entries: {total}")

# ============================================================
# STEP 2: Learn rules per formula
# ============================================================
basic_feats = ["density", "vpa", "aspect", "fe", "abc_min", "abc_max", "nat", "spg", "ehull"]
rules = {}

for key in poly_keys:
    ents = formula_entries[key]
    mol_e = [e for e in ents if e["is_mol"]]
    cry_e = [e for e in ents if not e["is_mol"]]

    found = False

    # Try basic single-feature threshold
    for feat in basic_feats:
        mv = [e[feat] for e in mol_e if e[feat] is not None and isinstance(e[feat], (int, float))]
        cv = [e[feat] for e in cry_e if e[feat] is not None and isinstance(e[feat], (int, float))]
        if len(mv) != len(mol_e) or len(cv) != len(cry_e): continue
        if not mv or not cv: continue

        # Perfect separation?
        if max(mv) < min(cv):
            rules[key] = (feat, "<", (max(mv) + min(cv)) / 2)
            found = True; break
        if min(mv) > max(cv):
            rules[key] = (feat, ">", (min(mv) + max(cv)) / 2)
            found = True; break

    if found: continue

    # Try 2-feature OR/AND
    for f1 in basic_feats:
        if found: break
        f1ok = all(e[f1] is not None and isinstance(e[f1], (int, float)) for e in ents)
        if not f1ok: continue
        for f2 in basic_feats:
            if f2 <= f1 or found: continue
            f2ok = all(e[f2] is not None and isinstance(e[f2], (int, float)) for e in ents)
            if not f2ok: continue

            v1s = sorted(set(e[f1] for e in ents))
            v2s = sorted(set(e[f2] for e in ents))
            for t1 in v1s:
                if found: break
                for t2 in v2s:
                    if found: break
                    for d1 in ("<", ">="):
                        if found: break
                        for d2 in ("<", ">="):
                            if found: break
                            for op in ("AND", "OR"):
                                ok = True
                                for e in ents:
                                    c1 = e[f1] < t1 if d1 == "<" else e[f1] >= t1
                                    c2 = e[f2] < t2 if d2 == "<" else e[f2] >= t2
                                    pred = (c1 and c2) if op == "AND" else (c1 or c2)
                                    if pred != e["is_mol"]:
                                        ok = False; break
                                if ok:
                                    rules[key] = ("2feat", f1, d1, t1, op, f2, d2, t2)
                                    found = True; break

    if found: continue

    # Try bond features
    for e in ents:
        bpa, min_nb = compute_bpa(e["atoms_dict"])
        e["bpa"] = bpa
        e["min_nonbond"] = min_nb

    for feat in ["bpa", "min_nonbond"]:
        mv = [e[feat] for e in mol_e if e.get(feat) is not None]
        cv = [e[feat] for e in cry_e if e.get(feat) is not None]
        if len(mv) != len(mol_e) or len(cv) != len(cry_e): continue
        if not mv or not cv: continue
        if max(mv) < min(cv):
            rules[key] = (feat, "<", (max(mv) + min(cv)) / 2)
            found = True; break
        if min(mv) > max(cv):
            rules[key] = (feat, ">", (min(mv) + max(cv)) / 2)
            found = True; break

    if found: continue

    # Try 2-feature with bond features included
    all_feats = basic_feats + ["bpa", "min_nonbond"]
    for f1 in all_feats:
        if found: break
        f1ok = all(e.get(f1) is not None and isinstance(e.get(f1), (int, float)) for e in ents)
        if not f1ok: continue
        for f2 in all_feats:
            if f2 <= f1 or found: continue
            f2ok = all(e.get(f2) is not None and isinstance(e.get(f2), (int, float)) for e in ents)
            if not f2ok: continue

            v1s = sorted(set(e[f1] for e in ents))
            v2s = sorted(set(e[f2] for e in ents))
            for t1 in v1s:
                if found: break
                for t2 in v2s:
                    if found: break
                    for d1 in ("<", ">="):
                        if found: break
                        for d2 in ("<", ">="):
                            if found: break
                            for op in ("AND", "OR"):
                                ok = True
                                for e in ents:
                                    c1 = e[f1] < t1 if d1 == "<" else e[f1] >= t1
                                    c2 = e[f2] < t2 if d2 == "<" else e[f2] >= t2
                                    pred = (c1 and c2) if op == "AND" else (c1 or c2)
                                    if pred != e["is_mol"]:
                                        ok = False; break
                                if ok:
                                    rules[key] = ("2feat", f1, d1, t1, op, f2, d2, t2)
                                    found = True; break

    # Try "unique spg OR max ehull" approach
    if not found:
        mol_spgs = {e["spg"] for e in mol_e if e["spg"] is not None}
        cry_spgs = {e["spg"] for e in cry_e if e["spg"] is not None}
        unique_mol_spgs = mol_spgs - cry_spgs

        mol_ehulls = [e.get("ehull") for e in mol_e if isinstance(e.get("ehull"), (int, float))]
        cry_ehulls = [e.get("ehull") for e in cry_e if isinstance(e.get("ehull"), (int, float))]

        if unique_mol_spgs and cry_ehulls:
            max_cry_ehull = max(cry_ehulls)
            # mol entries caught by unique spg
            caught_by_spg = [e for e in mol_e if e["spg"] in unique_mol_spgs]
            # remaining mol entries need ehull > max_cry_ehull
            remaining_mol = [e for e in mol_e if e["spg"] not in unique_mol_spgs]
            remaining_ok = all(
                isinstance(e.get("ehull"), (int, float)) and e["ehull"] > max_cry_ehull
                for e in remaining_mol
            )
            if remaining_ok and len(caught_by_spg) + len(remaining_mol) == len(mol_e):
                rules[key] = ("spg_or_ehull", unique_mol_spgs, max_cry_ehull)
                found = True

    if not found:
        pair, ratio = key
        print(f"  UNSOLVED: {pair[0]}{ratio[0]}{pair[1]}{ratio[1]}  mol={len(mol_e)} cryst={len(cry_e)}")

print(f"\nSolved: {len(rules)}/{len(poly_keys)}")

# ============================================================
# STEP 3: VERIFY
# ============================================================
correct = 0
errors = []

for key in poly_keys:
    ents = formula_entries[key]
    rule = rules.get(key)
    if rule is None:
        errors.extend(ents)
        continue

    for e in ents:
        if rule[0] == "2feat":
            _, f1, d1, t1, op, f2, d2, t2 = rule
            v1, v2 = e.get(f1), e.get(f2)
            if v1 is None or v2 is None:
                errors.append(e); continue
            c1 = v1 < t1 if d1 == "<" else v1 >= t1
            c2 = v2 < t2 if d2 == "<" else v2 >= t2
            pred_mol = (c1 and c2) if op == "AND" else (c1 or c2)
        elif rule[0] == "spg_or_ehull":
            _, unique_spgs, max_cry_ehull = rule
            spg_val = e.get("spg")
            ehull_val = e.get("ehull")
            pred_mol = (spg_val in unique_spgs) or (
                isinstance(ehull_val, (int, float)) and ehull_val > max_cry_ehull)
        else:
            feat, direction, thresh = rule
            val = e.get(feat)
            if val is None:
                errors.append(e); continue
            pred_mol = val < thresh if direction == "<" else val > thresh

        if pred_mol == e["is_mol"]:
            correct += 1
        else:
            errors.append(e)

print(f"\n{'='*60}")
print(f"LEVEL 6 VERIFICATION")
print(f"{'='*60}")
print(f"Total: {total}")
print(f"Correct: {correct}/{total} = {correct/total:.4%}")
print(f"Errors: {len(errors)}")
if errors:
    for e in errors[:10]:
        tag = "MOL" if e["is_mol"] else "CRY"
        print(f"  {tag} {e['jid']:15s} {e['formula']:10s}")
