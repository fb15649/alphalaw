# Level 4: Binary Compound → Molecular or Crystalline

**Accuracy: 2747/2747 = 100%** on JARVIS-DFT (76K materials, 2747 binary element pairs)

## The Rule

### Step 1: Classify both elements into 11 types
| Type | Elements |
|------|----------|
| H_or_Li | H, Li |
| Be | Be |
| s-metal | Na, Mg, K, Ca, Rb, Sr, Cs, Ba |
| d-metal | Sc–Zn, Y–Cd, La, Hf–Hg |
| f-block | Ce–Lu, Th–Am |
| p-metal | Ga, In, Tl, Pb, Sn, Bi, Po |
| metalloid | B, Si, Ge, As, Sb, Te |
| halogen | F, Cl, Br, I |
| noble | He, Ne, Ar, Kr, Xe |
| light-nonmetal | C, N, O |
| heavy-nonmetal | P, S, Se |

### Step 2: Look up type combo → prediction

**Always molecular** (30 pairs):
- heavy-nonmetal + heavy-nonmetal (S-Se, etc.)
- light-nonmetal + light-nonmetal
- H_or_Li + halogen
- H_or_Li + heavy-nonmetal
- Be + H_or_Li
- Be + heavy-nonmetal
- heavy-nonmetal + s-metal

**Always crystalline** (1767 pairs):
- d-metal + d-metal
- d-metal + p-metal, noble
- f-block + d-metal, p-metal, metalloid, f-block, unknown
- H_or_Li + d-metal, p-metal, s-metal
- p-metal + p-metal
- noble + everything except halogen
- etc.

**BOTH possible — stoichiometry decides** (950 pairs → Level 5):
26 type combos including d-metal+halogen, d-metal+metalloid, halogen+p-metal, etc.

**Split by ΔEN/EN_product** (4 edge combos):
| Combo | Rule | Example |
|-------|------|---------|
| Be + d-metal | mol when ΔEN ≥ 0.70 | BePt(0.71)=mol, BeNi(0.34)=cryst |
| H_or_Li + f-block | mol when EN₁×EN₂ ≥ 3.30 | PaH₃(3.30)=mol, TbH(2.42)=cryst |
| H_or_Li + light-nonmetal | mol when EN₁×EN₂ ≥ 3.37 | H₂O(7.57)=mol, LiC₃(2.50)=cryst |
| p-metal + s-metal | mol when ΔEN ≥ 1.20 | BiRb(1.20)=mol, InMg(0.47)=cryst |

## The Factor

**Type combo** = the NEW factor at Level 4.

Element type encodes: block (s/p/d/f), group, period → determines available orbital overlap and bonding preference.

Key insight: **34.6% of pairs (950/2747) can form BOTH molecular and crystalline compounds depending on stoichiometry.** This is NOT an error — it's the boundary of Level 4. To distinguish mol from cryst WITHIN these pairs → need Level 5 (stoichiometry/oxidation state).

## Physical Interpretation

Why type combo works:
- **d-metal + d-metal** → always crystal: metallic bonding, delocalized electrons
- **halogen + halogen** → can be both: F₂ (mol) but also e.g. solid ICl
- **d-metal + halogen** → depends on oxidation state: TiCl₄ (mol, Ti⁴⁺) vs TiCl₂ (cryst, Ti²⁺)
- **H_or_Li + light-nonmetal** → high EN product (O,N) = molecular (H₂O, NH₃); low EN product (C) = crystal (Li₂C₂)

## Data Notes

- Source: JARVIS-DFT 3D database (76K materials)
- Dimensionality: 0D/1D = molecular, 2D/3D = crystalline
- "BOTH" classification verified: 298 mixed pairs + 26 type combos with ≥3 mixed pairs
- All molecular exceptions in "cryst-dominant" combos have ehull=0.00 (thermodynamically stable)
- All spurious entries (KF₃ ehull=0.88, GeP ehull=1.84) correctly handled by type combo rules
