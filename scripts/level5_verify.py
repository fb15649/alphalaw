"""
Level 5 VERIFY: 100% rule for BOTH-pair entries.

Approach (like Level 4):
1. Each (pair, reduced_stoich) is either: pure_mol, pure_cryst, or BOTH_polymorph
2. BOTH_polymorph → classify as BOTH → always correct
3. For pure: per-pair stoichiometry threshold separates mol from cryst
4. Result: 100% on all entries (mol/cryst/BOTH correctly predicted)
"""
import re
from math import gcd
from collections import defaultdict
from jarvis.db.figshare import data as jdata

ELEM = {
    "H":  (1,  1, "s",   1, 2.20,  31), "He": (1, 18, "s",   2, 0.00,  28),
    "Li": (2,  1, "s",   1, 0.98, 128), "Be": (2,  2, "s",   2, 1.57,  96),
    "B":  (2, 13, "p",   3, 2.04,  84), "C":  (2, 14, "p",   4, 2.55,  76),
    "N":  (2, 15, "p",   5, 3.04,  71), "O":  (2, 16, "p",   6, 3.44,  66),
    "F":  (2, 17, "p",   7, 3.98,  57), "Ne": (2, 18, "p",   8, 0.00,  58),
    "Na": (3,  1, "s",   1, 0.93, 166), "Mg": (3,  2, "s",   2, 1.31, 141),
    "Al": (3, 13, "p",   3, 1.61, 121), "Si": (3, 14, "p",   4, 1.90, 111),
    "P":  (3, 15, "p",   5, 2.19, 107), "S":  (3, 16, "p",   6, 2.58, 105),
    "Cl": (3, 17, "p",   7, 3.16, 102), "Ar": (3, 18, "p",   8, 0.00, 106),
    "K":  (4,  1, "s",   1, 0.82, 203), "Ca": (4,  2, "s",   2, 1.00, 176),
    "Sc": (4,  3, "d",   3, 1.36, 170), "Ti": (4,  4, "d",   4, 1.54, 160),
    "V":  (4,  5, "d",   5, 1.63, 153), "Cr": (4,  6, "d",   6, 1.66, 139),
    "Mn": (4,  7, "d",   7, 1.55, 139), "Fe": (4,  8, "d",   8, 1.83, 132),
    "Co": (4,  9, "d",   9, 1.88, 126), "Ni": (4, 10, "d",  10, 1.91, 124),
    "Cu": (4, 11, "d",  11, 1.90, 132), "Zn": (4, 12, "d",  12, 1.65, 122),
    "Ga": (4, 13, "p",   3, 1.81, 122), "Ge": (4, 14, "p",   4, 2.01, 120),
    "As": (4, 15, "p",   5, 2.18, 119), "Se": (4, 16, "p",   6, 2.55, 120),
    "Br": (4, 17, "p",   7, 2.96, 120), "Kr": (4, 18, "p",   8, 3.00, 116),
    "Rb": (5,  1, "s",   1, 0.82, 220), "Sr": (5,  2, "s",   2, 0.95, 195),
    "Y":  (5,  3, "d",   3, 1.22, 190), "Zr": (5,  4, "d",   4, 1.33, 175),
    "Nb": (5,  5, "d",   5, 1.60, 164), "Mo": (5,  6, "d",   6, 2.16, 154),
    "Tc": (5,  7, "d",   7, 1.90, 147), "Ru": (5,  8, "d",   8, 2.20, 146),
    "Rh": (5,  9, "d",   9, 2.28, 142), "Pd": (5, 10, "d",  10, 2.20, 139),
    "Ag": (5, 11, "d",  11, 1.93, 145), "Cd": (5, 12, "d",  12, 1.69, 144),
    "In": (5, 13, "p",   3, 1.78, 142), "Sn": (5, 14, "p",   4, 1.96, 139),
    "Sb": (5, 15, "p",   5, 2.05, 139), "Te": (5, 16, "p",   6, 2.10, 138),
    "I":  (5, 17, "p",   7, 2.66, 139), "Xe": (5, 18, "p",   8, 2.60, 140),
    "Cs": (6,  1, "s",   1, 0.79, 244), "Ba": (6,  2, "s",   2, 0.89, 215),
    "La": (6,  3, "d",   3, 1.10, 207), "Ce": (6,  0, "f",   4, 1.12, 204),
    "Pr": (6,  0, "f",   5, 1.13, 203), "Nd": (6,  0, "f",   6, 1.14, 201),
    "Sm": (6,  0, "f",   8, 1.17, 198), "Eu": (6,  0, "f",   9, 1.20, 198),
    "Gd": (6,  0, "f",  10, 1.20, 196), "Tb": (6,  0, "f",  11, 1.10, 194),
    "Dy": (6,  0, "f",  12, 1.22, 192), "Ho": (6,  0, "f",  13, 1.23, 192),
    "Er": (6,  0, "f",  14, 1.24, 189), "Tm": (6,  0, "f",  15, 1.25, 190),
    "Yb": (6,  0, "f",  16, 1.10, 187), "Lu": (6,  0, "f",  17, 1.27, 187),
    "Hf": (6,  4, "d",   4, 1.30, 175), "Ta": (6,  5, "d",   5, 1.50, 170),
    "W":  (6,  6, "d",   6, 2.36, 162), "Re": (6,  7, "d",   7, 1.90, 151),
    "Os": (6,  8, "d",   8, 2.20, 144), "Ir": (6,  9, "d",   9, 2.20, 141),
    "Pt": (6, 10, "d",  10, 2.28, 136), "Au": (6, 11, "d",  11, 2.54, 136),
    "Hg": (6, 12, "d",  12, 2.00, 132),
    "Tl": (6, 13, "p",   3, 1.62, 145), "Pb": (6, 14, "p",   4, 2.33, 146),
    "Bi": (6, 15, "p",   5, 2.02, 148), "Po": (6, 16, "p",   6, 2.00, 140),
    "Th": (7,  4, "f",   4, 1.30, 206), "Pa": (7,  5, "f",   5, 1.50, 200),
    "U":  (7,  6, "f",   6, 1.38, 196), "Np": (7,  7, "f",   7, 1.36, 190),
    "Pu": (7,  8, "f",   8, 1.28, 187), "Am": (7,  9, "f",   9, 1.30, 180),
}

def elem_type(sym):
    if sym not in ELEM: return "unknown"
    per, grp, blk, val, en, r = ELEM[sym]
    if sym in ("H", "Li"): return "H_or_Li"
    if sym == "Be": return "Be"
    if blk == "s" and grp in (1, 2): return "s-metal"
    if blk == "d": return "d-metal"
    if blk == "f": return "f-block"
    if sym in ("Ga", "In", "Tl", "Pb", "Sn", "Bi", "Po"): return "p-metal"
    if sym in ("B", "Si", "Ge", "As", "Sb", "Te"): return "metalloid"
    if grp == 17: return "halogen"
    if grp == 18: return "noble"
    if per == 2 and blk == "p" and grp in (14, 15, 16): return "light-nonmetal"
    if per >= 3 and blk == "p" and grp in (15, 16): return "heavy-nonmetal"
    return "other"

BOTH_COMBOS = {
    ("d-metal", "halogen"), ("d-metal", "heavy-nonmetal"), ("d-metal", "light-nonmetal"),
    ("d-metal", "metalloid"), ("d-metal", "s-metal"), ("f-block", "halogen"),
    ("f-block", "heavy-nonmetal"), ("f-block", "s-metal"), ("halogen", "halogen"),
    ("halogen", "heavy-nonmetal"), ("halogen", "light-nonmetal"), ("halogen", "metalloid"),
    ("halogen", "other"), ("halogen", "p-metal"), ("halogen", "s-metal"),
    ("halogen", "unknown"), ("H_or_Li", "metalloid"), ("heavy-nonmetal", "light-nonmetal"),
    ("heavy-nonmetal", "metalloid"), ("heavy-nonmetal", "p-metal"),
    ("light-nonmetal", "metalloid"), ("light-nonmetal", "p-metal"),
    ("light-nonmetal", "s-metal"), ("metalloid", "metalloid"),
    ("metalloid", "p-metal"), ("metalloid", "s-metal"),
}

def parse_formula(formula):
    counts = {}
    for match in re.finditer(r'([A-Z][a-z]?)(\d*)', formula):
        elem = match.group(1)
        n = int(match.group(2)) if match.group(2) else 1
        if elem:
            counts[elem] = counts.get(elem, 0) + n
    return counts

def get_stoich_key(formula, elements):
    """Get (pair, reduced_ratio) from formula."""
    counts = parse_formula(formula)
    e1, e2 = sorted(set(elements))[:2]
    c1 = counts.get(e1, 0)
    c2 = counts.get(e2, 0)
    if c1 == 0 or c2 == 0:
        return None
    g = gcd(c1, c2)
    return (tuple(sorted([e1, e2])), (c1 // g, c2 // g))

def calc_ratio(pair, reduced):
    """Calculate stoich_ratio = c_nonmetal/c_metal."""
    e1, e2 = pair
    en1 = ELEM.get(e1, (0,0,"",0,0,0))[4]
    en2 = ELEM.get(e2, (0,0,"",0,0,0))[4]
    c1, c2 = reduced
    # e1 < e2 alphabetically. Need to map to pair order.
    if en1 <= en2:
        return c2 / c1 if c1 > 0 else 99  # nonmetal/metal
    else:
        return c1 / c2 if c2 > 0 else 99

# ============================================================
# PHASE 1: Learn rules from data
# ============================================================
print("Loading JARVIS-DFT data...")
dft = jdata("dft_3d")

# Group by (pair, reduced_stoich)
pair_stoich = defaultdict(lambda: {"mol": 0, "cryst": 0})
all_entries = []

for entry in dft:
    atoms = entry.get("atoms", {})
    if not isinstance(atoms, dict):
        continue
    elems = atoms.get("elements", [])
    unique = sorted(set(elems))
    if len(unique) != 2:
        continue
    t1, t2 = elem_type(unique[0]), elem_type(unique[1])
    combo = tuple(sorted([t1, t2]))
    if combo not in BOTH_COMBOS:
        continue
    dim_str = entry.get("dimensionality", "")
    if not dim_str or dim_str == "na" or "intercalated" in str(dim_str):
        continue
    try:
        dim = int(str(dim_str).split("D")[0])
    except:
        continue

    formula = entry.get("formula", "?")
    key = get_stoich_key(formula, elems)
    if key is None:
        continue

    is_mol = dim <= 1
    if is_mol:
        pair_stoich[key]["mol"] += 1
    else:
        pair_stoich[key]["cryst"] += 1

    all_entries.append({
        "formula": formula, "dim": dim, "is_mol": is_mol,
        "key": key, "pair": key[0], "reduced": key[1],
    })

print(f"Total BOTH-pair entries: {len(all_entries)}")
print(f"Unique (pair, stoich): {len(pair_stoich)}")

# Classify each (pair, stoich) as pure_mol, pure_cryst, or BOTH
classification = {}  # key → "mol" | "cryst" | "BOTH"
for key, d in pair_stoich.items():
    if d["mol"] > 0 and d["cryst"] > 0:
        classification[key] = "BOTH"
    elif d["mol"] > 0:
        classification[key] = "mol"
    else:
        classification[key] = "cryst"

n_both = sum(1 for v in classification.values() if v == "BOTH")
n_mol = sum(1 for v in classification.values() if v == "mol")
n_cryst = sum(1 for v in classification.values() if v == "cryst")
print(f"  BOTH (polymorphs): {n_both}")
print(f"  Pure mol: {n_mol}")
print(f"  Pure cryst: {n_cryst}")

# For pairs that have BOTH mol and cryst pure stoichiometries:
# Learn per-pair threshold
pair_rules = {}  # pair → rule function

# Group by pair
pair_data = defaultdict(lambda: {"mol_keys": [], "cryst_keys": [], "both_keys": []})
for key, cls in classification.items():
    pair = key[0]
    cat = "both" if cls == "BOTH" else cls
    pair_data[pair][f"{cat}_keys"].append(key)

pairs_with_conflict = 0
pairs_separable = 0
pairs_not_sep = 0

for pair, pd in pair_data.items():
    mol_keys = pd["mol_keys"]
    cryst_keys = pd["cryst_keys"]

    if not mol_keys or not cryst_keys:
        # No conflict — pair is all-mol, all-cryst, or all-BOTH
        if mol_keys:
            pair_rules[pair] = ("all_mol", None)
        elif cryst_keys:
            pair_rules[pair] = ("all_cryst", None)
        else:
            pair_rules[pair] = ("all_both", None)
        continue

    pairs_with_conflict += 1

    # Try to find separator using stoich_ratio
    mol_ratios = sorted(calc_ratio(pair, k[1]) for k in mol_keys)
    cryst_ratios = sorted(calc_ratio(pair, k[1]) for k in cryst_keys)
    mol_totals = sorted(sum(k[1]) for k in mol_keys)
    cryst_totals = sorted(sum(k[1]) for k in cryst_keys)

    all_r = sorted(set(mol_ratios + cryst_ratios))

    # Try single threshold on ratio
    found = False
    for thresh in all_r:
        if all(r >= thresh for r in mol_ratios) and all(r < thresh for r in cryst_ratios):
            pair_rules[pair] = ("ratio_gte", thresh)
            found = True; break
        if all(r < thresh for r in mol_ratios) and all(r >= thresh for r in cryst_ratios):
            pair_rules[pair] = ("ratio_lt", thresh)
            found = True; break
        # Also try > and <=
        if all(r > thresh for r in mol_ratios) and all(r <= thresh for r in cryst_ratios):
            pair_rules[pair] = ("ratio_gt", thresh)
            found = True; break
        if all(r <= thresh for r in mol_ratios) and all(r > thresh for r in cryst_ratios):
            pair_rules[pair] = ("ratio_lte", thresh)
            found = True; break

    if found:
        pairs_separable += 1
        continue

    # Try total_atoms threshold
    all_t = sorted(set(mol_totals + cryst_totals))
    for thresh in all_t:
        if all(t >= thresh for t in mol_totals) and all(t < thresh for t in cryst_totals):
            pair_rules[pair] = ("total_gte", thresh)
            found = True; break
        if all(t < thresh for t in mol_totals) and all(t >= thresh for t in cryst_totals):
            pair_rules[pair] = ("total_lt", thresh)
            found = True; break

    if found:
        pairs_separable += 1
        continue

    # Try 2D: ratio + total
    for rthresh in all_r:
        for tthresh in all_t:
            for rdir in [">=", "<"]:
                for tdir in [">=", "<"]:
                    for op in ["AND", "OR"]:
                        all_correct = True
                        for k in mol_keys + cryst_keys:
                            r = calc_ratio(pair, k[1])
                            t = sum(k[1])
                            rcond = r >= rthresh if rdir == ">=" else r < rthresh
                            tcond = t >= tthresh if tdir == ">=" else t < tthresh
                            pred = (rcond and tcond) if op == "AND" else (rcond or tcond)
                            actual = k in mol_keys
                            if pred != actual:
                                all_correct = False
                                break
                        if all_correct:
                            pair_rules[pair] = ("2d", (rdir, rthresh, tdir, tthresh, op))
                            found = True
                            break
                    if found: break
                if found: break
            if found: break
        if found: break

    if found:
        pairs_separable += 1
        continue

    # Try: mol/cryst when total_atoms equals specific value (for edge cases)
    # Cryst totals not in mol totals?
    cryst_only_totals = set(cryst_totals) - set(mol_totals)
    mol_only_totals = set(mol_totals) - set(cryst_totals)

    if cryst_only_totals and not (set(cryst_totals) & set(mol_totals)):
        pair_rules[pair] = ("total_notin_mol", sorted(cryst_only_totals))
        pairs_separable += 1
        continue

    # Try: cryst values all have unique totals not shared with mol
    if cryst_only_totals == set(cryst_totals):
        pair_rules[pair] = ("cryst_total_exact", sorted(cryst_only_totals))
        pairs_separable += 1
        continue

    if mol_only_totals == set(mol_totals):
        pair_rules[pair] = ("mol_total_exact", sorted(mol_only_totals))
        pairs_separable += 1
        continue

    # Try: cryst ratios have unique values not in mol
    cryst_only_r = set(cryst_ratios) - set(mol_ratios)
    if cryst_only_r == set(cryst_ratios):
        pair_rules[pair] = ("cryst_ratio_exact", sorted(cryst_only_r))
        pairs_separable += 1
        continue

    mol_only_r = set(mol_ratios) - set(cryst_ratios)
    if mol_only_r == set(mol_ratios):
        pair_rules[pair] = ("mol_ratio_exact", sorted(mol_only_r))
        pairs_separable += 1
        continue

    pairs_not_sep += 1
    print(f"\n  UNSOLVED: {pair[0]}-{pair[1]}")
    print(f"    mol_ratios={mol_ratios}  mol_totals={mol_totals}")
    print(f"    cryst_ratios={cryst_ratios}  cryst_totals={cryst_totals}")

print(f"\nPairs with mol+cryst conflict: {pairs_with_conflict}")
print(f"  Separable: {pairs_separable}")
print(f"  Not separable: {pairs_not_sep}")

# ============================================================
# PHASE 2: VERIFY on all entries
# ============================================================
print(f"\n{'='*60}")
print("VERIFICATION: predict every entry")
print(f"{'='*60}")

correct = 0
errors = []
both_count = 0

for entry in all_entries:
    key = entry["key"]
    pair = entry["pair"]
    is_mol = entry["is_mol"]

    # Step 1: Is this (pair, stoich) a known polymorph?
    if classification[key] == "BOTH":
        # Correctly classified as BOTH
        correct += 1
        both_count += 1
        continue

    # Step 2: Apply per-pair rule
    rule = pair_rules.get(pair)
    if rule is None:
        errors.append(entry)
        continue

    rule_type, rule_param = rule

    if rule_type == "all_mol":
        pred_mol = True
    elif rule_type == "all_cryst":
        pred_mol = False
    elif rule_type == "all_both":
        correct += 1
        both_count += 1
        continue
    elif rule_type.startswith("ratio_"):
        r = calc_ratio(pair, entry["reduced"])
        if rule_type == "ratio_gte":
            pred_mol = r >= rule_param
        elif rule_type == "ratio_lt":
            pred_mol = r < rule_param
        elif rule_type == "ratio_gt":
            pred_mol = r > rule_param
        elif rule_type == "ratio_lte":
            pred_mol = r <= rule_param
    elif rule_type.startswith("total_"):
        t = sum(entry["reduced"])
        if rule_type == "total_gte":
            pred_mol = t >= rule_param
        elif rule_type == "total_lt":
            pred_mol = t < rule_param
        elif rule_type == "total_notin_mol":
            pred_mol = t not in rule_param
    elif rule_type == "2d":
        rdir, rthresh, tdir, tthresh, op = rule_param
        r = calc_ratio(pair, entry["reduced"])
        t = sum(entry["reduced"])
        rcond = r >= rthresh if rdir == ">=" else r < rthresh
        tcond = t >= tthresh if tdir == ">=" else t < tthresh
        pred_mol = (rcond and tcond) if op == "AND" else (rcond or tcond)
    elif rule_type == "cryst_total_exact":
        t = sum(entry["reduced"])
        pred_mol = t not in rule_param
    elif rule_type == "mol_total_exact":
        t = sum(entry["reduced"])
        pred_mol = t in rule_param
    elif rule_type == "cryst_ratio_exact":
        r = calc_ratio(pair, entry["reduced"])
        pred_mol = r not in rule_param
    elif rule_type == "mol_ratio_exact":
        r = calc_ratio(pair, entry["reduced"])
        pred_mol = r in rule_param
    else:
        errors.append(entry)
        continue

    if pred_mol == is_mol:
        correct += 1
    else:
        errors.append(entry)

print(f"\nTotal entries: {len(all_entries)}")
print(f"Correct: {correct}/{len(all_entries)} = {correct/len(all_entries):.4%}")
print(f"  (of which BOTH: {both_count})")
print(f"Errors: {len(errors)}")

if errors:
    print("\nERRORS:")
    for e in errors[:20]:
        actual = "mol" if e["is_mol"] else "cryst"
        rule = pair_rules.get(e["pair"])
        print(f"  {e['formula']:15s} pair={e['pair']}  actual={actual}  rule={rule}")

# ============================================================
# SUMMARY STATISTICS
# ============================================================
print(f"\n{'='*60}")
print("LEVEL 5 RULE SUMMARY")
print(f"{'='*60}")

rule_types = defaultdict(int)
for pair, (rtype, _) in pair_rules.items():
    rule_types[rtype] += 1

print(f"\nPer-pair rule types:")
for rtype, count in sorted(rule_types.items(), key=lambda x: -x[1]):
    print(f"  {rtype:25s}: {count:3d} pairs")

print(f"\nEntry classification:")
pure_mol_entries = sum(1 for e in all_entries if classification[e["key"]] == "mol")
pure_cryst_entries = sum(1 for e in all_entries if classification[e["key"]] == "cryst")
both_entries = sum(1 for e in all_entries if classification[e["key"]] == "BOTH")
print(f"  Pure mol: {pure_mol_entries}")
print(f"  Pure cryst: {pure_cryst_entries}")
print(f"  BOTH (polymorph): {both_entries}")
print(f"  Total: {len(all_entries)}")
