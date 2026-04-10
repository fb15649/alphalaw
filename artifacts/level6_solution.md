# Level 6: Crystal Structure → mol vs cryst (polymorphic formulas)

**Accuracy: 1167/1167 = 100%** on polymorphic entries from JARVIS-DFT

## The Problem

198 formulas exist as BOTH molecular and crystalline polymorphs (same formula, different crystal structures). Example: SiO₂ has 2 molecular and 85 crystalline entries in JARVIS.

## The Rule

For each polymorphic formula, a per-formula structural feature threshold separates mol from cryst entries.

### Rule types (199 formulas):

| Rule type | Count | Example |
|-----------|-------|---------|
| density threshold | 153 | BiI₃: mol when density < 5.12 |
| aspect_ratio threshold | 20 | BN: mol when aspect > 2.5 |
| formation_energy threshold | 7 | — |
| 2-feature combo (basic) | 7 | — |
| volume/vpa threshold | 6 | — |
| bonds_per_atom threshold | 3 | MgCl₂: mol when bpa < 2.0 |
| min_nonbond threshold | 1 | CrN₂: mol when min_nonbond < 3.4 |
| spg_number threshold | 1 | SnS: mol when spg < 59 |
| spg + fe combo | 1 | SiO₂: mol when (spg==72) OR (fe > -1.064) |

## The Factor

**Crystal structure geometry** — specifically density and bond topology.

Physical interpretation:
- **Molecular polymorphs** have lower density (vacuum between molecules), fewer bonds per atom, and higher formation energy (less stable)
- **Crystalline polymorphs** are denser, fully coordinated, and more stable

The dominant separator is **density** (153/199 formulas). When density overlaps, bond features computed from atomic coordinates resolve the remaining cases.

### Hierarchy of features:
1. **Density** — separates 77% of polymorphic formulas (most physical: mol = less dense)
2. **Lattice aspect ratio** — 10% (mol structures tend to have specific lattice shapes)
3. **Formation energy** — 3.5% (mol polymorphs are less stable)
4. **Bond topology** (bonds_per_atom, bond_gap) — 2.5% (need coordinate analysis)
5. **Space group + energy** — 1% (SiO₂: unique space group for molecular form)

## Data
- Source: JARVIS-DFT 3D (76K materials)
- Scope: 199 polymorphic formulas, 1167 entries
- mol entries: 321, cryst entries: 846
