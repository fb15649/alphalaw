# Bond Order Scaling Rule: A Classification of Chemical Bonds by Power-Law Exponent

**Yuri Kazin**

Independent researcher

Correspondence: yuri@kazin.ru

---

## Abstract

We fit E(n) = E_1 × n^alpha to bond dissociation energies at multiple bond orders for 37 element pairs and find two independent results. First, three rules predict whether alpha > 1 (cooperative strengthening) or alpha < 1 (diminishing returns) with 100% accuracy (37/37): (A) homonuclear Group 15 through Period 5, (B) O-O, and (C) heteronuclear {C, N} + Group 16. Second, the ratio R = E_max/E_single exhibits an empty gap: for 15 heteronuclear compounds, all gases have R >= 1.97 and all framework solids have R <= 1.63 — no compound falls in [1.63, 1.97]. For 23 elements, R combined with coordination number correctly classifies all as molecular gas or framework solid (23/23). Note that alpha and R are related but not equivalent: C-N has alpha < 1 yet R > 1.8 because its triple bond (R = 2.92) compensates sublinear scaling. The gap originates from the abrupt drop in pi/sigma overlap at the Period 2–3 transition. As a machine learning feature, alpha adds +0.032 R^2 to formula-based models of formation energy on 38,074 JARVIS-DFT materials, encoding information not captured by electronegativity or lone pair count alone. An open-source calculator is available.

**Keywords:** bond dissociation energy, bond order, power law, pi-bonding, materials classification

---

## 1. Introduction

Bond dissociation energies are among the most fundamental quantities in chemistry, yet a simple question remains underexplored: how does bond energy scale with bond order for a given element pair? A carbon-carbon double bond (614 kJ/mol) is not twice a single bond (346 kJ/mol), while a nitrogen-nitrogen triple bond (945 kJ/mol) is nearly six times the single bond (160 kJ/mol). This difference — diminishing returns for carbon, cooperative strengthening for nitrogen — determines whether an element forms extended frameworks (diamond) or small molecules (N_2).

We parameterize this scaling as E(n) = E_1 × n^alpha, where alpha is a dimensionless exponent. This functional form was used by Johnston and Parr [1] in the BEBO model for activation energies but was never systematically studied as a descriptor of bond character. We compute alpha for 45 element pairs using bond energies from the CRC Handbook [2] and Cotton & Murillo [3], classify bonds by the ratio R = E_max/E_single, and discover an empty gap in R that cleanly separates molecular compounds from framework solids.

---

## 2. Methods

### 2.1 Data

Bond dissociation energies at two or more bond orders were compiled from the CRC Handbook (97th ed.) [2], Cotton & Murillo [3] for transition metal multiple bonds, and cross-checked against wiredchemist.com and Chemistry LibreTexts tables. The final dataset comprises 37 unique bond types: 20 s/p-block heteronuclear, 13 s/p-block homonuclear, and 4 d-block homonuclear bonds. Results were cross-checked against alternative sources (wiredchemist.com, Chemistry LibreTexts) to verify robustness.

### 2.2 Computation of alpha

For bond types with exactly two bond orders (n_1, n_2):

    alpha = log(E_2/E_1) / log(n_2/n_1)

For bond types with three or more bond orders, alpha was determined by ordinary least squares regression of log(E_n/E_1) on log(n/n_1), forced through the origin (no intercept). This ensures E(n_1) = E_1 by construction.

For improved prediction accuracy, a two-parameter model was also fitted:

    E(n) = E_1 × n^(alpha + beta × ln(n))

where beta captures acceleration (beta > 0) or deceleration (beta < 0) of scaling with bond order.

### 2.3 Machine learning

Formation energies of 38,074 materials from JARVIS-DFT [4] were predicted using gradient boosting regression (300 estimators, max depth 6, 5-fold cross-validation). Three feature sets were compared: 12 formula-derived features (electronegativity, atomic radius, period, mass), 5 alpha-derived features (avg_alpha, max_alpha, min_alpha, has_synergy, avg_R), and 5 lone pair features (max_LP, min_LP, mean_LP, has_LP, has_d_block). Feature importance was assessed by permutation importance.

---

## 3. Results

### 3.1 Classification rule: alpha > 1 vs alpha < 1

We find that alpha > 1 (cooperative strengthening, where each additional bond order adds more than the previous) occurs in exactly three cases:

**(A)** Homonuclear Group 15 bonds through Period 5: N-N (alpha = 1.55), P-P (1.28), As-As (1.39), Sb-Sb (1.31). Exception: Bi-Bi (alpha = 0.89, Period 6).

**(B)** O-O (alpha = 1.77).

**(C)** Heteronuclear bonds between {C, N} and a Group 16 element: C-O (1.02), C-S (1.08), C-Se (1.07), N-O (1.60), N-S (1.55).

All other s/p bonds have alpha < 1, including S-S (0.68), Se-Se (0.66), Te-Te (0.69), and all bonds involving Si, Ge, Sn, Pb, B, or Al. All d-block bonds have alpha < 1: Cr-Cr (0.56), Mo-Mo (0.71), W-W (0.88), Re-Re (0.92).

**Accuracy: 37/37 = 100%.** No exceptions. Cross-checked against alternative data sources (wiredchemist.com, Chemistry LibreTexts) with consistent results.

*Table 1: Alpha values for s/p homonuclear bonds*

| Bond | E_1 (kJ/mol) | E_2 | E_3 | alpha | LP_min | Rule |
|------|-------------|-----|-----|-------|--------|------|
| C-C | 346 | 614 | 839 | 0.812 | 0 | — |
| Si-Si | 310 | 434 | — | 0.485 | 0 | — |
| Ge-Ge | 264 | 350 | — | 0.407 | 0 | — |
| Sn-Sn | 187 | 235 | — | 0.330 | 0 | — |
| N-N | 160 | 418 | 945 | 1.551 | 1 | A |
| P-P | 201 | 489 | — | 1.283 | 1 | A |
| As-As | 146 | 382 | — | 1.388 | 1 | A |
| Sb-Sb | 121 | 299 | — | 1.305 | 1 | A |
| Bi-Bi | 105 | 195 | — | 0.893 | 1 | — |
| O-O | 146 | 498 | — | 1.770 | 2 | B |
| S-S | 266 | 425 | — | 0.676 | 2 | — |
| Se-Se | 172 | 272 | — | 0.661 | 2 | — |
| Te-Te | 138 | 222 | — | 0.686 | 2 | — |

*Table 2: d-block bonds (multiple bond orders from molecular compounds)*

| Bond | Bond orders | Energies (kJ/mol) | alpha | R^2 |
|------|------------|-------------------|-------|-----|
| Cr-Cr | 1, 4 | 70, 152 | 0.559 | — |
| Mo-Mo | 1, 2, 3, 4, 5, 6 | 140, 250, 350, 405, 420, 435 | 0.710 | 0.977 |
| W-W | 1, 3, 4, 6 | 160, 500, 570, 666 | 0.878 | 0.988 |
| Re-Re | 1, 4 | 120, 432 | 0.924 | — |

### 3.2 The gap in R = E_max/E_single

For heteronuclear compounds, R cleanly separates gases from framework solids:

- All molecular gases: R >= 1.97 (minimum: S-O, R = 1.97)
- All framework solids: R <= 1.63 (maximum: B-N, R = 1.63)
- Gap: [1.63, 1.97] — **no compound observed**

For homonuclear elements, the equivalent criterion E_max > CN × E_single correctly classifies all 23 tested elements as molecular gas or framework solid.

Combined accuracy: **38/38 = 100%.**

Note: C-N illustrates the distinction between alpha and R. The rules predict alpha(C-N) = 0.99 < 1 (correct — scaling is slightly sublinear). However, because C-N forms a triple bond, R = 891/305 = 2.92 >> 1.8, making HCN a gas. Sublinear scaling (alpha < 1) does not prevent molecular existence when high bond orders are available — it only means E_3 < 3 × E_1.

*Figure 1 description:* R = E_double/E_single for 15 heteronuclear compounds. Gases (circles) cluster at R >= 1.97, solids (squares) at R <= 1.63. Gap region [1.63, 1.97] is empty.

### 3.3 Physical origin of the gap

R = 1 + E_pi/E_sigma. The gap corresponds to E_pi/E_sigma in [0.63, 0.97]. No element pair produces pi/sigma overlap ratios in this range because:

1. Period 2 atoms (C, N, O) have compact 2p orbitals producing efficient pi overlap: E_pi/E_sigma > 0.97.
2. Period 3+ atoms (Si, P, S, ...) have diffuse np orbitals producing poor pi overlap: E_pi/E_sigma < 0.63.
3. The atomic radius increases ~50% from Period 2 to Period 3, and pi overlap decays approximately exponentially with radius. The discontinuous jump in radius produces a discontinuous jump in pi/sigma, leaving no elements in between.

### 3.4 Machine learning validation

On 38,074 JARVIS-DFT materials (5-fold CV, gradient boosting):

| Model | R^2 |
|-------|-----|
| Formula features (12) | 0.822 ± 0.031 |
| Formula + LP (17) | 0.839 ± 0.027 |
| Formula + alpha (17) | 0.853 ± 0.028 |

Alpha features add +0.032 R^2 compared to +0.017 for raw lone pair features. A redundancy test confirms that even 1000-tree gradient boosting on formula features alone (R^2 = 0.831) cannot match Formula + alpha (R^2 = 0.853), establishing that alpha encodes non-redundant information.

Permutation importance ranks max_alpha as the 5th most important feature (0.143), behind delta_EN (0.302), n_atoms (0.294), std_EN (0.233), and weighted_EN (0.208).

---

## 4. Discussion

### 4.1 Relationship to known models

The power-law form E(n) = E_1 × n^alpha was used by Johnston and Parr [1] in the BEBO model for estimating activation energies of H-transfer reactions. BEBO treated alpha as a fitting parameter for individual bond types without seeking a classification rule. The present work identifies three structural rules (A, B, C) that predict alpha > 1 or < 1 with 100% accuracy, and discovers the gap in R that separates molecular from framework compounds.

### 4.2 Why alpha > 1 requires both LP and small atoms

Lone pairs (LP >= 1) are necessary but not sufficient for alpha > 1. Sulfur has LP = 2 but alpha(S-S) = 0.68 < 1; selenium and tellurium similarly. The additional requirement is efficient pi-overlap, which demands small atomic radius (Period 2) or specific orbital geometry (Group 15 through Period 5 for a single pi bond).

Group 15 elements retain alpha > 1 through Period 5 because a single pi bond requires only one good lateral overlap, achievable even with moderately large 4p or 5p orbitals. Group 16 elements (requiring two pi interactions for alpha > 1) lose this ability after Period 2 because two simultaneous pi overlaps demand compact orbitals.

### 4.3 The S-S anomaly is not anomalous

Sulfur was previously considered anomalous (LP = 2 but alpha < 1). In fact, sulfur behaves exactly as expected: its 3p orbitals are too diffuse for effective pi bonding, so it forms S_8 rings of single bonds rather than S_2 dimers. The "anomaly" arose from the incorrect assumption that LP alone determines alpha.

### 4.4 Limitations

1. The dataset (37 bonds) is small. Additional bond types, particularly from Period 4-5 heteronuclear pairs, would strengthen the classification.
2. The two-parameter model (alpha, beta) achieves < 5% prediction error but was validated on 3-point bonds where overfitting risk exists.
3. The ML improvement (+0.032 R^2) is statistically significant but modest. Alpha is a useful supplementary feature, not a replacement for existing descriptors.
4. The gap [1.63, 1.97] is empirical. A first-principles derivation from orbital overlap integrals would strengthen the theoretical foundation.

---

## 5. Conclusions

Two complementary results emerge. First, three rules from the periodic table predict whether the bond order scaling exponent alpha exceeds 1, with 100% accuracy on 37 bond types. Second, the ratio R = E_max/E_single classifies compounds into molecular (R > 1.8) and framework (R < 1.7) types with an empty gap between them (38/38 accuracy). The alpha classification and R criterion are related but distinct: alpha describes scaling character, while R determines structural preference. The gap originates from the discontinuous increase in atomic radius between Period 2 and Period 3. As a machine learning feature, alpha provides non-redundant information about material stability, adding +0.032 R^2 to formula-based models on 38,074 compounds.

---

## Data and Code Availability

Bond energy data is tabulated in Tables 1-2 and derived from publicly available sources. The alpha-law calculator is available as open-source software:

- **Repository**: https://github.com/fb15649/alphalaw
- **Web calculator**: Run locally with `streamlit run alphalaw/web.py`
- **CLI**: `python -m alphalaw C O`

---

## References

[1] H. S. Johnston, C. Parr, "Activation energies from bond energies," *J. Am. Chem. Soc.* **85**, 2544-2551 (1963).

[2] W. M. Haynes, Ed., *CRC Handbook of Chemistry and Physics*, 97th ed. (CRC Press, 2016).

[3] F. A. Cotton, C. A. Murillo, R. A. Walton, *Multiple Bonds Between Metal Atoms*, 3rd ed. (Springer, 2005).

[4] K. Choudhary et al., "The joint automated repository for various integrated simulations (JARVIS) for data-driven materials design," *npj Computational Materials* **6**, 173 (2020).

[5] T. Chen, T. A. Manz, "Bond orders of the diatomic molecules," *RSC Adv.* **9**, 17072-17092 (2019).

[6] K. P. Huber, G. Herzberg, *Molecular Spectra and Molecular Structure IV: Constants of Diatomic Molecules* (Springer, 1979).

[7] M. D. Morse, "Predissociation measurements of bond dissociation energies," *Acc. Chem. Res.* **51**, 141-148 (2018).

[8] L. Pauling, *The Nature of the Chemical Bond*, 3rd ed. (Cornell University Press, 1960).

[9] L. M. A. Bettencourt et al., "Growth, innovation, scaling, and the pace of life in cities," *PNAS* **104**, 7301-7306 (2007).

[10] G. B. West, J. H. Brown, B. J. Enquist, "A general model for the origin of allometric scaling laws in biology," *Science* **276**, 122-126 (1997).

---

## arXiv Submission Metadata

- **Primary category**: physics.chem-ph (Chemical Physics)
- **Cross-list**: cond-mat.mtrl-sci (Materials Science)
- **Keywords**: bond dissociation energy, bond order, power law, pi-bonding, materials classification, forbidden gap
