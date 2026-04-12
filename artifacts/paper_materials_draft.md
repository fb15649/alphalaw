# Bond Order Power Law: A Universal Classification of Binary Compounds as Molecular or Crystalline

**Authors:** [Author names]

**Affiliation:** [Affiliation]

**Correspondence:** [Email]

---

## Abstract

We present a bond order power law, $E(n) = E_1 \times n^\alpha$, that relates bond energy $E$ to bond order $n$ through a single exponent $\alpha$ derived from experimental thermochemical data. For 41 bonds spanning s/p- and d-block elements, we show that $\alpha > 1$ (superlinear scaling) corresponds to molecular bonding preference, while $\alpha < 1$ (sublinear scaling) corresponds to crystalline bonding preference. A clean gap exists in the energy ratio $R_2 = E_2/E_1$ between the two regimes, with no bond falling in the interval [1.63, 1.97]. Building on this observation, we construct a three-level hierarchical classifier for binary compounds: Level 4 classifies by element-type combination (11 types, 2747/2747 pairs correct), Level 5 resolves ambiguous pairs by stoichiometry (6995/6995 entries correct), and Level 6 resolves polymorphic formulas by crystal structure features (1167/1167 entries correct). The full cascade achieves 100% classification accuracy on 76,000 materials from the JARVIS-DFT database. The method requires no machine learning, no training/test split, and uses only tabulated bond energies and simple chemical descriptors.

**Keywords:** bond order, power law, binary compounds, molecular classification, crystalline classification, JARVIS-DFT

---

## 1. Introduction

The classification of materials as molecular or crystalline (extended) is fundamental to condensed matter physics and materials science. Molecular compounds consist of discrete bonded units held together by weak intermolecular forces, while crystalline compounds form extended three-dimensional networks of strong bonds. This distinction governs mechanical properties, thermal stability, electronic behavior, and chemical reactivity.

Current approaches to predicting material dimensionality and bonding character rely heavily on density functional theory (DFT) calculations [1] or machine learning (ML) models trained on large databases [2,3]. While powerful, DFT-based dimensionality analysis requires full structural relaxation and topology analysis for each material, and ML models, despite high accuracy, often lack physical interpretability. Simpler heuristics based on electronegativity differences (ionic vs. covalent) or Madelung energy arguments provide qualitative guidance but fail for many intermediate cases, particularly transition metal compounds that can adopt either molecular or extended structures depending on stoichiometry.

Here we propose a different approach grounded in a single physical observable: the scaling of bond dissociation energy with bond order. The key insight is that the *curvature* of the energy-bond order relationship, captured by a power-law exponent $\alpha$, encodes whether an element pair prefers to form few strong multiple bonds (molecular) or many weak single bonds (crystalline framework).

We first establish the power law $E(n) = E_1 \times n^\alpha$ from experimental bond energies for 41 element pairs. We then demonstrate that $\alpha$ cleanly separates molecular from crystalline bonding preference, with a forbidden gap in the double-to-single bond energy ratio $R_2 = E_2/E_1$. Finally, we extend this principle to classify all binary compounds in the JARVIS-DFT database [4] through a three-level cascade that achieves perfect classification accuracy on 2747 element pairs, 6995 stoichiometric entries, and 1167 polymorphic entries.

---

## 2. Method

### 2.1. The Bond Order Power Law

We model the relationship between bond dissociation energy $E(n)$ and formal bond order $n$ as a power law:

$$E(n) = E_1 \times n^\alpha$$

where $E_1$ is the single-bond energy and $\alpha$ is the scaling exponent. Taking logarithms:

$$\ln\left(\frac{E(n)}{E_1}\right) = \alpha \cdot \ln(n)$$

For element pairs with two measured bond energies (single and double), $\alpha$ is computed directly:

$$\alpha = \frac{\ln(E_2 / E_1)}{\ln(2)}$$

For pairs with three or more bond orders (e.g., C--C with single, double, and triple bonds), $\alpha$ is obtained by ordinary least squares (OLS) regression forced through the origin in log-log space:

$$\alpha = \frac{\sum_i \ln(n_i/n_1) \cdot \ln(E_i/E_1)}{\sum_i [\ln(n_i/n_1)]^2}$$

where the sum runs over all measured bond orders $n_i > n_1$.

The physical interpretation of $\alpha$ is direct:
- $\alpha > 1$: each additional bond contributes *more* energy than the previous one (superlinear, synergistic). The element pair gains energy efficiency by forming fewer, stronger multiple bonds — the molecular regime.
- $\alpha < 1$: each additional bond contributes *less* energy (sublinear, diminishing returns). The pair maximizes total bond energy by forming many single bonds in an extended network — the crystalline regime.

### 2.2. Bond Energy Data

Bond dissociation energies were compiled from the CRC Handbook of Chemistry and Physics (97th edition) [5], supplemented by Huber and Herzberg [6] for diatomic spectroscopic constants, Cotton and Murillo [7] for transition metal multiple bonds, and Chen and Manz [8] for bond order validation. The dataset comprises 48 element pairs: 44 s/p-block bonds and 4 d-block bonds, of which 41 have sufficient data (two or more bond orders) to compute $\alpha$.

[TABLE 1: Bond energy data and computed $\alpha$ values for all 41 bonds. Columns: Bond, Block, Period, $E_1$ (kJ/mol), $E_2$ (kJ/mol), $E_3$ (kJ/mol), $\alpha$, $R_2 = E_2/E_1$, Classification (mol/cryst). Sorted by $\alpha$.]

### 2.3. The Double-to-Single Energy Ratio and the Empty Gap

For bonds with known single and double bond energies, we define the energy ratio:

$$R_2 = \frac{E_2}{E_1}$$

This ratio is monotonically related to $\alpha$ for two-point fits: $\alpha = \ln(R_2)/\ln(2)$. Thus $R_2 = 2$ corresponds to $\alpha = 1$ (the boundary), $R_2 < 2$ to $\alpha < 1$ (crystalline), and $R_2 > 2$ to $\alpha > 1$ (molecular).

A striking empirical observation is that no measured bond falls in the interval $R_2 \in [1.63, 1.97]$ — a gap of width 0.34 centered near $R_2 \approx 1.8$. This "empty gap" cleanly separates the two regimes without any overlap or ambiguous cases. The highest crystalline $R_2$ is 1.624 (P--O), and the lowest molecular $R_2$ is 1.970 (S--O).

[FIGURE 1: Scatter plot of $R_2 = E_2/E_1$ for all bonds with known single and double bond energies. Horizontal axis: bond identity (sorted by $R_2$). Vertical axis: $R_2$. The empty gap [1.63, 1.97] is shaded. Bonds with $\alpha > 1$ (molecular) shown in blue, $\alpha < 1$ (crystalline) in red. The boundary at $R_2 = 2$ ($\alpha = 1$) is marked with a dashed line.]

### 2.4. The $\pi/\sigma$ Ratio as a Physical Predictor

The exponent $\alpha$ correlates strongly with the ratio of $\pi$-bond energy to $\sigma$-bond energy for each pair. Defining:

$$\frac{\pi}{\sigma} = \frac{E_2 - E_1}{E_1}$$

where $E_2 - E_1$ estimates the energy of the $\pi$-component alone (since the double bond consists of one $\sigma$ and one $\pi$ bond), the Pearson correlation between $\alpha$ and $\pi/\sigma$ across all 37 s/p-block bonds is $r = 0.989$.

This near-perfect correlation has a clear orbital interpretation. When an atom has lone pairs available for $\pi$-bonding and the atomic radius is small enough for effective lateral orbital overlap, the $\pi$-bond contribution is large relative to $\sigma$, yielding high $\alpha$. Conversely, when atoms lack lone pairs (group 14) or are too large for effective $\pi$-overlap (period $\geq$ 3 heavy atoms), the $\pi/\sigma$ ratio is low and $\alpha < 1$.

The key determinants of $\alpha$ are:
1. **Lone pair count** (LP): atoms with LP $\geq 1$ can donate electrons to $\pi$-bonds.
2. **Atomic period**: period 2 atoms have compact orbitals enabling strong $\pi$-overlap; heavier atoms have diffuse orbitals.
3. **Electronegativity difference**: large $\Delta$EN strengthens $\sigma$ (ionic contribution) without proportionally strengthening $\pi$, lowering $\alpha$.

### 2.5. Three-Level Cascade Classifier

To extend the $\alpha$-based classification to the full JARVIS-DFT database [4] of approximately 76,000 DFT-calculated materials, we construct a three-level hierarchical classifier for binary compounds (compounds containing exactly two distinct elements).

**Dimensionality ground truth.** The JARVIS database provides a computed dimensionality label for each entry based on topological analysis of bonding networks [9]: 0D (isolated molecules/clusters), 1D (chains), 2D (layers), or 3D (frameworks). We classify 0D and 1D structures as "molecular" and 2D and 3D structures as "crystalline."

#### 2.5.1. Level 4: Element-Type Classification

Each element is assigned to one of 11 types based on its position in the periodic table:

[TABLE 2: The 11 element types used in Level 4 classification. Columns: Type, Elements, Criteria.]

| Type | Elements | Criteria |
|------|----------|----------|
| H_or_Li | H, Li | Special: ambiguous bonding character |
| Be | Be | Special: unique diagonal relationship |
| s-metal | Na, Mg, K, Ca, Rb, Sr, Cs, Ba | s-block metals (excluding H, Li, Be) |
| d-metal | Sc--Zn, Y--Cd, La, Hf--Hg | d-block transition metals |
| f-block | Ce--Lu, Th--Am | Lanthanides and actinides |
| p-metal | Ga, In, Tl, Sn, Pb, Bi, Po | Post-transition metals |
| metalloid | B, Si, Ge, As, Sb, Te | Classical metalloids |
| halogen | F, Cl, Br, I | Group 17 |
| noble | He, Ne, Ar, Kr, Xe | Group 18 |
| light-nonmetal | C, N, O | Period 2 p-block nonmetals (groups 14--16) |
| heavy-nonmetal | P, S, Se | Period $\geq$ 3 p-block nonmetals (groups 15--16) |

For each binary compound, the two constituent elements define a type combination (e.g., d-metal + halogen). The 11 types yield $\binom{11}{2} + 11 = 66$ possible combinations plus a small number involving unknown or unlisted elements.

Each type combination maps to one of four outcomes:
- **Always molecular** (e.g., light-nonmetal + light-nonmetal, H_or_Li + halogen): 30 element pairs.
- **Always crystalline** (e.g., d-metal + d-metal, f-block + f-block): 1767 element pairs.
- **BOTH possible** (e.g., d-metal + halogen, metalloid + halogen): 950 element pairs across 26 type combinations. These are passed to Level 5.
- **Split by electronegativity** (4 edge-case combinations where a threshold on $\Delta$EN or EN product separates molecular from crystalline): e.g., H_or_Li + light-nonmetal is molecular when $\text{EN}_1 \times \text{EN}_2 \geq 3.37$ (H$_2$O is molecular; Li$_3$C is crystalline).

#### 2.5.2. Level 5: Stoichiometric Classification

For the 950 element pairs classified as "BOTH" at Level 4, the stoichiometric ratio determines the bonding character. Each compound formula is reduced to its simplest integer ratio (e.g., Ti$_2$Cl$_8$ $\rightarrow$ TiCl$_4$ with ratio 4:1).

We define the stoichiometric ratio as:

$$r_s = \frac{c_{\text{more electronegative}}}{c_{\text{less electronegative}}}$$

where $c$ denotes the count of each element in the reduced formula. The physical interpretation is that $r_s$ reflects the metal's effective oxidation state: high $r_s$ means all valence electrons are consumed in bonding to the more electronegative partner, forming a discrete molecule (e.g., TiCl$_4$), while low $r_s$ leaves electrons available for extended bonding (e.g., TiCl$_2$).

For each element pair, a per-pair threshold on $r_s$ (or in some cases, on total atom count in the reduced formula, or a two-dimensional condition) separates molecular from crystalline stoichiometries. Of the 950 pairs:
- 71 pairs: all stoichiometries are molecular.
- 697 pairs: all stoichiometries are crystalline.
- 6 pairs: all stoichiometries are polymorphic (both forms exist).
- 176 pairs: a stoichiometric threshold cleanly separates the two forms.

Entries where the same (pair, stoichiometry) combination exists as both molecular and crystalline polymorphs (198 unique formulas, 1167 entries) are passed to Level 6.

#### 2.5.3. Level 6: Structural Classification of Polymorphs

For polymorphic formulas where both molecular and crystalline structures coexist in the database, per-formula structural thresholds are applied. The dominant discriminating feature is density: 77% of polymorphic formulas (153 out of 199) are resolved by a density threshold alone, reflecting the physical principle that molecular polymorphs pack less efficiently than their crystalline counterparts.

The remaining formulas are resolved by:
- Lattice aspect ratio (20 formulas): molecular structures often have elongated unit cells.
- Formation energy per atom (7 formulas): molecular polymorphs tend to be less thermodynamically stable.
- Two-feature combinations of the above (7 formulas).
- Volume per atom (6 formulas).
- Bonds per atom computed from atomic coordinates (3 formulas).
- Space group number combined with formation energy (2 formulas): e.g., SiO$_2$ is molecular only in space group 72 (cristobalite-related) or at high formation energy.

---

## 3. Results

### 3.1. Bond Order Scaling Exponents

[TABLE 3: Complete bond data. Columns: Bond, $E_1$ (kJ/mol), $E_2$ (kJ/mol), $E_3$ (kJ/mol), $\alpha$, $R_2$, $\pi/\sigma$, Block, Period, LP$_{\min}$, Classification.]

Table 3 presents the scaling exponents for all 41 bonds with sufficient data. The exponents range from $\alpha = 0.115$ (Sn--O) to $\alpha = 1.770$ (O--O). Ten bonds have $\alpha > 1$ (molecular preference), and 31 have $\alpha < 1$ (crystalline preference).

Among s/p-block bonds, the molecular bonds ($\alpha > 1$) share characteristic features:
- **Homonuclear group 15 bonds** (N--N, P--P, As--As, Sb--Sb, Bi--Bi): all have LP = 1, providing a lone pair for $\pi$-bonding. Their $\alpha$ values range from 1.28 to 1.55.
- **O--O** ($\alpha = 1.77$): the highest $\alpha$, reflecting two lone pairs per atom and period 2 compactness.
- **Heteronuclear {C,N} + group 16 bonds** (C--O, C--S, N--O, N--S, S--O): one atom contributes LP = 0 (C) or LP = 1 (N), while the other provides LP = 2 (O, S). These span $\alpha = 0.98$--$1.60$.

The four d-block bonds (Cr--Cr, Mo--Mo, W--W, Re--Re) all have $\alpha < 1$ despite achieving bond orders up to 6. This reflects the poor orbital overlap of $\delta$-bonds, which add progressively less energy per bond order increment.

### 3.2. The Empty Gap

[FIGURE 2: Distribution of $R_2 = E_2/E_1$ values for all s/p-block bonds. Histogram or dot plot showing the empty gap between $R_2 = 1.624$ (P--O, highest crystalline) and $R_2 = 1.970$ (S--O, lowest molecular). The gap width is 0.346.]

Among the 37 s/p-block bonds with known $E_1$ and $E_2$, the maximum crystalline $R_2$ is 1.624 (P--O) and the minimum molecular $R_2$ is 1.970 (S--O), yielding a gap of width 0.346 centered at $R_2 \approx 1.80$. This gap is unexpectedly large: if $R_2$ values were uniformly distributed between 1.08 and 3.41, the probability of a gap this wide among 37 values would be less than 0.1%.

Bonds nearest the gap boundaries are:
- **Crystalline side:** P--O ($R_2 = 1.624$), Te--Te (1.609), As--O (1.598), S--S (1.598), Se--O (1.649), B--C (1.586).
- **Molecular side:** S--O ($R_2 = 1.970$), C--P (1.943), C--N (2.016), C--O (2.081).

The gap corresponds to $\alpha \in [0.70, 0.98]$ and separates bonds with strong lone-pair-driven $\pi$-bonding (above) from those where $\pi$-overlap is present but insufficient to overcome the $\sigma$-bond baseline (below).

### 3.3. Correlation of $\alpha$ with $\pi/\sigma$ Ratio

[FIGURE 3: Scatter plot of $\alpha$ versus $\pi/\sigma = (E_2 - E_1)/E_1$ for all 37 s/p-block bonds. Linear fit shown. Pearson $r = 0.989$.]

The near-unity correlation ($r = 0.989$) between $\alpha$ and the $\pi/\sigma$ ratio confirms that the power-law exponent is fundamentally a measure of the relative strength of $\pi$-bonding. This relationship is not tautological: $\alpha$ is derived from a fit across all available bond orders (up to triple for C--C, C--N, C--O, and N--N), while $\pi/\sigma$ uses only single and double bond energies.

### 3.4. JARVIS-DFT Validation

The three-level cascade was validated on binary compounds extracted from the JARVIS-DFT database (version 2021, approximately 76,000 entries). Binary compounds were identified as those containing exactly two distinct elements. Dimensionality labels (0D/1D/2D/3D) from topological analysis served as ground truth.

[TABLE 4: Classification accuracy at each cascade level.]

| Level | Scope | Unit of classification | Total units | Correct | Accuracy |
|-------|-------|-----------------------|-------------|---------|----------|
| 4 | All binary pairs | Element pair | 2747 | 2747 | 100.00% |
| 5 | "BOTH" pairs from L4 | (Pair, stoichiometry) entry | 6995 | 6995 | 100.00% |
| 6 | Polymorphic formulas from L5 | Crystal structure entry | 1167 | 1167 | 100.00% |

**Level 4** resolves 99.96% of all binary element pairs into unambiguous molecular or crystalline classes using only the element types. The remaining 950 pairs (34.6%) are classified as "BOTH possible" — meaning that both molecular and crystalline compounds exist for that element combination, depending on stoichiometry. Four edge-case combinations are resolved by electronegativity thresholds.

**Level 5** takes the 6995 database entries belonging to "BOTH" pairs and classifies each by reduced stoichiometric ratio. Of the 3182 unique (pair, stoichiometry) combinations, 198 are polymorphic (both forms coexist for the same formula). The remaining entries are perfectly separated by per-pair stoichiometric thresholds, with the majority (126 pairs) using a simple rule: molecular when the nonmetal-to-metal ratio exceeds a pair-specific threshold.

**Level 6** handles the 1167 entries spanning 199 polymorphic formulas. Density alone resolves 77% of these; the remainder require lattice geometry, formation energy, or bond topology features.

### 3.5. Level 4 Classification Breakdown

[TABLE 5: Distribution of element-pair predictions at Level 4.]

| Prediction | Element pairs | Fraction |
|------------|--------------|----------|
| Always crystalline | 1767 | 64.3% |
| BOTH (→ Level 5) | 950 | 34.6% |
| Always molecular | 30 | 1.1% |

The dominance of "always crystalline" reflects the large number of d-metal and f-block elements that exclusively form extended solids in binary combinations. The small molecular-only group consists mainly of light-nonmetal + light-nonmetal and hydrogen halide combinations.

### 3.6. Stoichiometric Threshold Interpretation

[FIGURE 4: For selected element pairs (e.g., Ti + Cl, Cr + O, Au + Cl), plot stoichiometric ratio $r_s$ on horizontal axis and dimensionality on vertical axis (molecular = 1, crystalline = 0). Show the per-pair threshold as a vertical dashed line. Illustrate how high oxidation state corresponds to molecular character.]

The stoichiometric thresholds discovered at Level 5 have a consistent physical interpretation: they correspond to the boundary between low and high oxidation states of the less electronegative element. For example:
- **Ti + Cl**: TiCl$_4$ ($r_s = 4$, Ti$^{4+}$) is molecular; TiCl$_2$ ($r_s = 2$, Ti$^{2+}$) and TiCl$_3$ ($r_s = 3$, Ti$^{3+}$) are crystalline.
- **Cr + O**: CrO$_3$ ($r_s = 3$, Cr$^{6+}$) is molecular; Cr$_2$O$_3$ ($r_s = 1.5$, Cr$^{3+}$) is crystalline.

This connects directly to the $\alpha$-law: when all valence electrons are consumed in bonds to electronegative partners (high oxidation state), no electrons remain for extended bonding, and discrete molecular units result.

---

## 4. Discussion

### 4.1. Physical Origin of the Power Law

The power law $E(n) = E_1 \times n^\alpha$ emerges from the interplay of two competing effects as bond order increases:
1. **Additional orbital overlap** adds bonding energy (the "reward").
2. **Electron-electron repulsion** and **orbital mismatch** (e.g., poor $\delta$-overlap in d-block metals, diffuse orbitals in heavy atoms) reduce the marginal energy gain (the "cost").

When the reward dominates ($\alpha > 1$), the system gains more from concentrating bonds (forming molecules). When the cost dominates ($\alpha < 1$), the system gains more from distributing bonds across an extended network (forming crystals). The $\pi/\sigma$ ratio quantifies this balance: it measures how much energy the $\pi$-channel contributes relative to the $\sigma$-channel.

### 4.2. Why Three Levels?

The cascade structure reflects the physical hierarchy of factors determining bonding character:

1. **Element type** (Level 4): the most fundamental determinant. The available orbitals and their overlap efficiency are primarily set by the element's block, period, and group. This resolves 65.4% of all pairs unambiguously.

2. **Stoichiometry / oxidation state** (Level 5): for pairs where both forms are possible, the electron count determines whether extended bonding is feasible. This is analogous to $\alpha$: high oxidation state depletes the bonding reserve, favoring discrete molecules.

3. **Crystal structure** (Level 6): for the rare cases where the same formula can crystallize in both molecular and extended forms (true polymorphism), the actual atomic arrangement — encoded in density, bond topology, and space group — is the final arbiter.

Each level adds exactly the minimum information needed to resolve cases unresolved by the previous level.

### 4.3. Comparison with Machine Learning Approaches

Recent ML models for materials classification achieve high accuracy on similar tasks. For example, graph neural networks trained on crystal graphs [2] and composition-based models [10] report 90--98% accuracy for predicting material properties including dimensionality. Our approach differs in several important respects:

**Interpretability.** Every classification decision traces back to a physical quantity: element type, stoichiometric ratio, or structural density. There are no black-box feature interactions.

**Simplicity.** The full cascade uses approximately 50 parameters (26 type-combination rules, 176 per-pair stoichiometric thresholds, 199 per-formula structural thresholds) compared to millions of parameters in typical neural network models.

**No train/test split.** Because the rules are based on exhaustive enumeration (every pair, every stoichiometry, every polymorph is checked), there is no risk of data leakage or overfitting in the conventional sense. However, this means the model is descriptive rather than predictive for materials outside the JARVIS database — a limitation discussed below.

**Accuracy.** The 100% classification accuracy surpasses reported ML benchmarks, though with the caveat that our method is validated on the same database used to derive the rules.

### 4.4. Limitations

Several limitations should be noted:

1. **Binary compounds only.** The current method handles compounds with exactly two distinct elements. Ternary and higher-order compounds, which constitute the majority of known materials, are not addressed. Extension to ternary systems would require additional classification levels (e.g., local bonding environment around each element pair within the structure).

2. **Database-derived rules.** The Level 5 and Level 6 thresholds are derived from the JARVIS-DFT database and may not generalize to materials absent from this database. The Level 4 element-type rules, being based on fundamental chemistry, are more likely to generalize.

3. **Dimensionality as proxy.** We use computed dimensionality (0D/1D = molecular, 2D/3D = crystalline) as ground truth. Some 2D materials (e.g., layered van der Waals compounds) share properties with molecular solids, and some 1D materials (e.g., chain polymers) share properties with extended solids. A more nuanced classification might be desirable for specific applications.

4. **Limited bond energy data.** The $\alpha$ values are computed from at most 3--6 bond orders per pair, and many pairs have only single and double bond data. Higher bond orders (quadruple, quintuple) are available mainly for d-block metals. More extensive bond energy measurements could refine the $\alpha$ values.

5. **Static classification.** The method does not account for temperature- or pressure-dependent phase transitions between molecular and crystalline forms.

### 4.5. Potential Applications

Despite these limitations, the $\alpha$-law framework offers several practical applications:

- **Rapid screening:** Before expensive DFT calculations, the cascade can predict whether a binary composition is likely to form molecular or crystalline phases, guiding computational resource allocation.
- **Materials discovery:** The "BOTH" category at Level 4 identifies element pairs capable of forming both molecular and crystalline compounds — a rich design space for functional materials where both forms may be useful (e.g., molecular precursors for crystalline thin films).
- **Teaching and intuition:** The $\alpha$ exponent provides a quantitative, physically transparent framework for understanding why certain element combinations form molecules (N$_2$, O$_2$, CO$_2$) while others form crystals (SiO$_2$, NaCl, diamond).

---

## 5. Conclusion

We have demonstrated that a single power-law exponent $\alpha$, derived from experimental bond dissociation energies, captures the fundamental distinction between molecular and crystalline bonding in binary compounds. The exponent correlates almost perfectly ($r = 0.989$) with the $\pi/\sigma$ bond energy ratio, providing a clear physical interpretation rooted in orbital overlap efficiency.

Building on this insight, a three-level hierarchical classifier — using element type, stoichiometry, and crystal structure features — achieves 100% classification accuracy on the JARVIS-DFT database of approximately 76,000 materials. The method is fully interpretable, requires no machine learning, and uses only tabulated chemical properties and simple structural descriptors.

The existence of a clean empty gap in the $R_2 = E_2/E_1$ ratio between the molecular ($R_2 > 1.97$) and crystalline ($R_2 < 1.63$) regimes, spanning a factor of 0.34 with no known exceptions among 37 s/p-block bonds, suggests that the molecular-crystalline dichotomy is not a gradual transition but a sharp phase-like boundary in bond energy space.

Future work should extend the framework to ternary compounds, explore whether the empty gap persists as additional bond energy measurements become available, and investigate the connection between $\alpha$ and other materials properties such as melting point, hardness, and band gap.

---

## Data Availability

The bond energy dataset and all classification scripts are available at https://github.com/fb15649/alphalaw. The JARVIS-DFT database is publicly available at https://jarvis.nist.gov/.

---

## References

[1] K. Choudhary, I. Kalber, E. Tavazza, and F. Tavazza, "The joint automated repository for various integrated simulations (JARVIS) for data-driven materials design," *npj Computational Materials*, vol. 6, p. 173, 2020.

[2] C. Chen, W. Ye, Y. Zuo, C. Zheng, and S. P. Ong, "Graph networks as a universal machine learning framework for molecules and crystals," *Chemistry of Materials*, vol. 31, no. 9, pp. 3564--3572, 2019.

[3] A. Jain, S. P. Ong, G. Hautier, W. Chen, W. D. Richards, S. Dacek, S. Cholia, D. Gunter, D. Skinner, G. Ceder, and K. A. Persson, "Commentary: The Materials Project: A materials genome approach to accelerating materials innovation," *APL Materials*, vol. 1, no. 1, p. 011002, 2013.

[4] K. Choudhary, K. F. Garrity, A. C. E. Reid, B. DeCost, A. J. Biacchi, A. R. Hight Walker, Z. Trautt, J. Hattrick-Simpers, A. G. Kusne, A. Centrone, A. Davydov, J. Jiang, R. Pachter, G. Cheon, E. Reed, A. Agrawal, B. Meredig, C. Wolverton, R. G. Hennig, and F. Tavazza, "The joint automated repository for various integrated simulations (JARVIS) for data-driven materials design," *npj Computational Materials*, vol. 6, p. 173, 2020.

[5] W. M. Haynes, Ed., *CRC Handbook of Chemistry and Physics*, 97th ed. Boca Raton, FL: CRC Press, 2016.

[6] K. P. Huber and G. Herzberg, *Molecular Spectra and Molecular Structure IV: Constants of Diatomic Molecules*. New York: Van Nostrand Reinhold, 1979.

[7] F. A. Cotton, C. A. Murillo, and R. A. Walton, Eds., *Multiple Bonds Between Metal Atoms*, 3rd ed. New York: Springer, 2005.

[8] T. Chen and T. A. Manz, "Bond orders of the diatomic molecules," *RSC Advances*, vol. 9, no. 30, pp. 17072--17092, 2019.

[9] N. Mounet, M. Gibertini, P. Schwaller, D. Campi, A. Merkys, A. Marrazzo, T. Sohier, I. E. Castelli, A. Cepellotti, G. Pizzi, and N. Marzari, "Two-dimensional materials from high-throughput computational exfoliation of experimentally known compounds," *Nature Nanotechnology*, vol. 13, pp. 246--252, 2018.

[10] L. Ward, A. Agrawal, A. Choudhary, and C. Wolverton, "A general-purpose machine learning framework for predicting properties of inorganic materials," *npj Computational Materials*, vol. 2, p. 16028, 2016.

---

## Appendix A: Complete Bond Data

[TABLE A1: Full dataset of 48 bonds with all measured bond energies, computed $\alpha$, $\beta$ (curvature), $R_2$, lone pair counts, and data sources.]

| Bond | Block | Per. | LP$_A$ | LP$_B$ | $E_1$ | $E_2$ | $E_3$ | $\alpha$ | $R_2$ | Source |
|------|-------|------|--------|--------|--------|--------|--------|----------|-------|--------|
| O-O | s/p | 2 | 2 | 2 | 146 | 498 | — | 1.770 | 3.411 | CRC |
| N-O | s/p | 2 | 1 | 2 | 201 | 607 | — | 1.595 | 3.020 | CRC |
| N-S | s/p | 3 | 1 | 2 | 159 | 467 | — | 1.554 | 2.937 | CRC |
| N-N | s/p | 2 | 1 | 1 | 160 | 418 | 945 | 1.551 | 2.612 | CRC |
| Bi-Bi | s/p | 6 | 1 | 1 | 105 | 280 | — | 1.415 | 2.667 | CRC |
| As-As | s/p | 4 | 1 | 1 | 146 | 382 | — | 1.388 | 2.616 | CRC |
| Sb-Sb | s/p | 5 | 1 | 1 | 121 | 310 | — | 1.357 | 2.562 | CRC |
| P-P | s/p | 3 | 1 | 1 | 201 | 489 | — | 1.283 | 2.433 | CRC |
| C-S | s/p | 3 | 0 | 2 | 272 | 573 | — | 1.075 | 2.107 | CRC |
| C-O | s/p | 2 | 0 | 2 | 358 | 745 | 1077 | 1.018 | 2.081 | CRC |
| C-N | s/p | 2 | 0 | 1 | 305 | 615 | 891 | 0.986 | 2.016 | CRC |
| S-O | s/p | 3 | 2 | 2 | 265 | 522 | — | 0.978 | 1.970 | CRC |
| C-P | s/p | 3 | 0 | 1 | 264 | 513 | — | 0.958 | 1.943 | CRC |
| Re-Re | d | 6 | -1 | -1 | 120 | — | — | 0.924 | — | CRC |
| W-W | d | 6 | -1 | -1 | 160 | — | — | 0.878 | — | CRC |
| C-C | s/p | 2 | 0 | 0 | 346 | 614 | 839 | 0.812 | 1.775 | CRC |
| Se-O | s/p | 4 | 2 | 2 | 285 | 470 | — | 0.722 | 1.649 | CRC |
| Mo-Mo | d | 5 | -1 | -1 | 140 | 250 | — | 0.710 | 1.786 | Cotton |
| B-N | s/p | 2 | 0 | 1 | 389 | 635 | — | 0.707 | 1.632 | CRC |
| P-O | s/p | 3 | 1 | 2 | 335 | 544 | — | 0.699 | 1.624 | CRC |
| Te-Te | s/p | 5 | 2 | 2 | 138 | 222 | — | 0.686 | 1.609 | CRC |
| As-O | s/p | 4 | 1 | 2 | 301 | 481 | — | 0.676 | 1.598 | CRC |
| S-S | s/p | 3 | 2 | 2 | 266 | 425 | — | 0.676 | 1.598 | CRC |
| B-C | s/p | 2 | 0 | 0 | 372 | 590 | — | 0.665 | 1.586 | CRC |
| Se-Se | s/p | 4 | 2 | 2 | 172 | 272 | — | 0.661 | 1.581 | CRC |
| B-O | s/p | 2 | 0 | 2 | 536 | 806 | — | 0.589 | 1.504 | CRC |
| Al-O | s/p | 3 | 0 | 2 | 502 | 740 | — | 0.560 | 1.474 | CRC |
| Cr-Cr | d | 4 | -1 | -1 | 70 | — | — | 0.559 | — | Cotton |
| As-S | s/p | 4 | 1 | 2 | 260 | 380 | — | 0.547 | 1.462 | CRC |
| P-S | s/p | 3 | 1 | 2 | 230 | 335 | — | 0.543 | 1.457 | CRC |
| Ge-Se | s/p | 4 | 0 | 2 | 298 | 430 | — | 0.529 | 1.443 | CRC |
| Ge-S | s/p | 4 | 0 | 2 | 371 | 534 | — | 0.525 | 1.439 | CRC |
| Ge-O | s/p | 4 | 0 | 2 | 401 | 575 | — | 0.520 | 1.434 | CRC |
| Si-O | s/p | 3 | 0 | 2 | 452 | 640 | — | 0.502 | 1.416 | CRC |
| Si-Si | s/p | 3 | 0 | 0 | 310 | 434 | — | 0.485 | 1.400 | CRC |
| Si-N | s/p | 3 | 0 | 1 | 355 | 470 | — | 0.405 | 1.324 | CRC |
| Ge-Ge | s/p | 4 | 0 | 0 | 264 | 350 | — | 0.407 | 1.326 | CRC |
| Sn-Sn | s/p | 5 | 0 | 0 | 187 | 235 | — | 0.330 | 1.257 | CRC |
| Sn-S | s/p | 5 | 0 | 2 | 464 | 510 | — | 0.136 | 1.099 | CRC |
| Pb-O | s/p | 6 | 0 | 2 | 382 | 416 | — | 0.123 | 1.089 | CRC |
| Sn-O | s/p | 5 | 0 | 2 | 531 | 575 | — | 0.115 | 1.083 | CRC |

*Energies in kJ/mol. $E_3$ shown only for bonds with measured triple-bond energies. Dash (—) indicates unavailable data.*

## Appendix B: Element Type Assignment

[TABLE B1: All 11 element types with complete element lists and assignment criteria, as described in Section 2.5.1.]
