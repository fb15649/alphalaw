# Level 5: Stoichiometry → mol vs cryst (within BOTH-pairs)

**Accuracy: 6995/6995 = 100%** on JARVIS-DFT entries for 950 "BOTH" element pairs

## The Rule

### Step 1: Reduce formula to (element_pair, stoichiometry)
- Parse formula: TiCl₄ → pair=(Cl,Ti), reduced_stoich=(4,1)
- Reduce by GCD: Ti₂Cl₈ → same as TiCl₄ → (4,1)

### Step 2: Is this (pair, stoich) a known polymorph?
**198 formulas (1165 entries)** exist as BOTH molecular and crystalline polymorphs.
Examples: VF₄, MgCl₂, TiCl₃, CrO₃, SiO₂, BiI₃
→ Classify as BOTH → Level 6 (geometry)

### Step 3: For pure formulas — per-pair stoichiometry rule

Each of the 950 element pairs falls into one of:

| Category | Pairs | Rule |
|----------|-------|------|
| All mol ratios | 71 | Every stoichiometry → mol |
| All cryst ratios | 697 | Every stoichiometry → cryst |
| All BOTH | 6 | Every stoichiometry → polymorph |
| **Separable** | **176** | **Per-pair threshold** |

### Step 4: Per-pair threshold types

| Rule type | Count | Description |
|-----------|-------|-------------|
| ratio_gt | 126 | mol when stoich_ratio > threshold |
| ratio_lte | 24 | mol when stoich_ratio ≤ threshold |
| 2d | 14 | mol when (ratio cond) AND/OR (total_atoms cond) |
| total_gte/lt | 10 | mol when total_atoms ≥/< threshold |
| total_notin | 2 | mol when total_atoms ∉ specific set |

## The Factor

**Stoichiometric ratio** (c_nonmetal/c_metal) is the NEW factor at Level 5.

Physical interpretation: **stoichiometry determines the metal's oxidation state**.
- High ratio → high oxidation → all valence electrons used → discrete molecule (TiCl₄, CrO₃)
- Low ratio → low oxidation → electrons available for extended bonding → crystal (TiCl₂, Cr₂O₃)

The threshold is **per-pair** because each metal has a different maximum oxidation state:
- Ti: threshold at ratio ~3-4 (TiCl₄=mol, TiCl₂=cryst)
- Au: threshold at ratio ~2 (AuCl₃=mol, AuCl=cryst)
- Mg: no threshold (always same type regardless of ratio)

## Key insight: polymorphism boundary

198 formulas (16.7% of entries) are **polymorphic** — the same formula exists as both molecular and crystalline structures. These define the boundary of Level 5:
- VF₄: 5 molecular entries + 8 crystalline entries (different space groups!)
- This is where geometry (Level 6) becomes necessary

## Data
- Source: JARVIS-DFT 3D database (76K materials)
- Scope: 950 "BOTH" element pairs from Level 4
- 6995 binary compound entries, 3182 unique (pair, stoich) combinations
