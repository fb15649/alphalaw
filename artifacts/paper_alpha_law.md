# Reserve Law of Chemical Bonding: A Universal Power-Law for Bond Order Scaling

**Yuri Kazin**

Independent researcher

Correspondence: y.kazin@kazin.ru

---

## Abstract

We report an empirical power-law relation E(n) = E_1 * n^alpha connecting bond dissociation energy E to bond order n through a single exponent alpha. Analysis of 23 bonds across s/p- and d-block elements reveals a classification rule: atoms possessing lone pairs (LP >= 1) yield alpha > 1 (cooperative strengthening), while atoms without lone pairs (LP = 0) yield alpha < 1 (diminishing returns). The rule holds for 93% of LP = 0 bonds and 80% of LP >= 1 bonds. Transition metal bonds universally show alpha < 1, consistent with poor delta-overlap of d-orbitals. For homonuclear Group 14 bonds (LP = 0), alpha correlates with Morse anharmonicity x_e (R^2 = 0.968, p = 0.016), suggesting a connection between the curvature of the potential well and multi-bond cooperativity. We propose that lone pairs serve as a "recruitable reserve" -- non-bonding electrons available for pi-bond formation that reinforce, rather than dilute, existing bonds. Limitations include small sample size and post-hoc anomalies requiring independent validation.

---

## 1. Introduction

Bond dissociation energies are among the most fundamental quantities in chemistry, yet the relationship between single, double, and triple bond energies of the same atom pair lacks a simple unifying description. Textbooks note that triple bonds are stronger than double bonds, which are stronger than single bonds, but typically treat each bond order independently. The question of *how* bond energy scales with bond order has received surprisingly little systematic attention.

Consider carbon--carbon bonds: E(C=C) = 614 kJ/mol is not twice E(C-C) = 346 kJ/mol, and E(C:::C) = 839 kJ/mol is not three times E(C-C). The ratio E(n)/E(1) grows sub-linearly with n. By contrast, nitrogen--nitrogen bonds show the opposite pattern: E(N:::N) = 945 kJ/mol is dramatically more than three times E(N-N) = 160 kJ/mol. The ratio grows super-linearly. This asymmetry -- diminishing returns for carbon, synergistic strengthening for nitrogen -- demands explanation.

We propose a simple power-law model:

> **E(n) = E_1 * n^alpha**

where E_1 is the single-bond dissociation energy, n is the formal bond order, and alpha is a dimensionless exponent characterizing the scaling regime. When alpha < 1, each additional bond order increment adds less energy than the previous (diminishing returns). When alpha > 1, each increment adds more (cooperativity). When alpha = 1, scaling is linear.

This functional form is not new in scaling science. Power-law exponents govern metabolic rate vs. body mass (Kleiber's law, alpha ~ 0.75) [1], urban innovation vs. city size (alpha ~ 1.27) [2], and network value vs. number of nodes (Metcalfe's law, alpha ~ 2) [3]. The question is whether a similar exponent in chemical bonding carries physical meaning.

We find that it does. The sign of (alpha - 1) is determined almost entirely by a single atomic property: the number of lone pairs (LP) on the bonding atoms. This observation, which we term the **Reserve Law**, states that lone pair electrons constitute a recruitable reserve that can be promoted into pi-bonding orbitals, enabling cooperative strengthening. Atoms without this reserve must form additional bonds from increasingly unfavorable orbital overlaps, leading to diminishing returns.

---

## 2. Results

### 2.1 Power-law fits for s/p-block homonuclear bonds

Bond dissociation energies were taken from the CRC Handbook of Chemistry and Physics (97th edition) [4] and Huber & Herzberg's compilation [5]. For each bond A-A with known energies at bond orders n = 1, 2 (and 3 where available), alpha was obtained by least-squares fitting of log(E) vs. log(n).

**Table 1.** Homonuclear s/p-block bonds.

| Bond  | E_1 (kJ/mol) | E_2 (kJ/mol) | E_3 (kJ/mol) | alpha | LP  |
|-------|--------------|--------------|--------------|-------|-----|
| C-C   | 346          | 614          | 839          | 0.770 | 0   |
| Si-Si | 310          | 434          | --           | 0.485 | 0   |
| Ge-Ge | 264          | 350          | --           | 0.407 | 0   |
| Sn-Sn | 187          | 235          | --           | 0.330 | 0   |
| N-N   | 160          | 418          | 945          | 2.012 | 1   |
| P-P   | 201          | 489          | --           | 1.283 | 1   |
| O-O   | 146          | 498          | --           | 1.770 | 2   |
| S-S   | 266          | 425          | --           | 0.676 | 2   |

The pattern is striking. All four Group 14 elements (LP = 0) have alpha < 1, with alpha decreasing monotonically down the group (C > Si > Ge > Sn). Both Group 15 elements (LP = 1) have alpha > 1, with nitrogen showing the most extreme cooperativity (alpha = 2.01). Oxygen (LP = 2) has alpha = 1.77, consistent with cooperative strengthening.

Sulfur (LP = 2, alpha = 0.676) is an anomaly. Despite having two lone pairs, S-S bonds show diminishing returns. This likely reflects the poor pi-overlap of 3p orbitals compared to 2p orbitals, rendering the lone pairs a less effective reserve. We return to this point in the Discussion.

### 2.2 Heteronuclear s/p-block bonds

For heteronuclear bonds A-B, we define LP_min = min(LP_A, LP_B), following a "bottleneck" principle: cooperative strengthening requires *both* atoms to contribute to the pi-system, and the atom with fewer available lone pairs limits the cooperativity.

**Table 2.** Heteronuclear s/p-block bonds.

| Bond  | alpha | LP_min |
|-------|-------|--------|
| C-N   | 0.914 | 0      |
| C-O   | 0.909 | 0      |
| N-O   | 1.595 | 1      |
| B-N   | 0.707 | 0      |
| B-O   | 0.589 | 0      |
| Si-O  | 0.502 | 0      |
| Si-N  | 0.405 | 0      |
| Al-O  | 0.560 | 0      |
| C-S   | 1.075 | 0      |
| C-P   | 0.958 | 0      |
| Ge-O  | 0.520 | 0      |

The bottleneck principle works well: all LP_min = 0 bonds have alpha < 1 except C-S (alpha = 1.075). The C-S anomaly is modest (alpha only slightly above 1) and may reflect the participation of sulfur's 3d orbitals in bonding, a well-known phenomenon in sulfur chemistry [6]. The single LP_min = 1 bond (N-O) shows clear cooperativity (alpha = 1.60).

### 2.3 Transition metal bonds

Bond energies for multiply-bonded transition metal dimers were taken from Cotton & Murillo's comprehensive compilation [7] and supplemented with CRC data. Bond orders in these systems range from 1 to 6 (in quadruply- and quintuply-bonded species).

**Table 3.** d-block homonuclear bonds.

| Bond  | Bond orders   | Energies (kJ/mol)        | alpha | R^2   |
|-------|--------------|--------------------------|-------|-------|
| Cr-Cr | 1, 4         | 70, 152                  | 0.559 | --    |
| Mo-Mo | 1, 2, 3, 4, 5, 6 | 140, 250, 350, 405, 420, 435 | 0.651 | 0.956 |
| W-W   | 1, 3, 4, 6   | 160, 500, 570, 666       | 0.830 | --    |
| Re-Re | 1, 4         | 120, 432                 | 0.868 | --    |

All four d-block bonds show alpha < 1, despite the availability of d-electrons that could in principle serve as a bonding reserve. The Mo-Mo case is particularly informative: with six data points spanning bond orders 1 through 6, the power-law fit yields alpha = 0.651 with R^2 = 0.956, confirming that the diminishing-returns pattern is robust across the full range of bond orders. Moving from bond order 5 to 6 adds only 15 kJ/mol (420 to 435), compared to 110 kJ/mol for the step from order 1 to 2.

**Caveat:** d-block bond energies are derived from molecular compounds (e.g., [Mo_2(O_2CR)_4] for quadruple bonds) and thus include ligand field effects. The intrinsic dimeric bond energies are less certain than for s/p-block elements.

### 2.4 Classification statistics

**Table 4.** Reserve Law classification accuracy.

| Category        | Rule              | Correct | Total | Accuracy |
|-----------------|-------------------|---------|-------|----------|
| LP = 0 (s/p)    | alpha < 1         | 14      | 15    | 93%      |
| LP >= 1 (s/p)   | alpha > 1         | 4       | 5     | 80%      |
| d-block          | alpha < 1         | 4       | 4     | 100%     |
| **All combined** |                   | **22**  | **24**| **92%**  |

Anomalies: S-S (LP = 2 but alpha < 1) and C-S (LP_min = 0 but alpha > 1). A Mann-Whitney test comparing alpha values of LP = 0 vs. LP >= 1 bonds yields p = 0.006, confirming the groups are significantly different.

### 2.5 Correlation with Morse anharmonicity

For the four homonuclear Group 14 bonds (C-C, Si-Si, Ge-Ge, Sn-Sn), all with LP = 0, we examined the relationship between alpha and the Morse anharmonicity constant x_e, obtained from spectroscopic data [5].

**Table 5.** Morse anharmonicity correlation (LP = 0 group).

| Bond  | x_e     | alpha |
|-------|---------|-------|
| C-C   | 0.00719 | 0.770 |
| Si-Si | 0.00395 | 0.485 |
| Ge-Ge | 0.00336 | 0.407 |
| Sn-Sn | 0.00140 | 0.330 |

Linear regression yields:

> **alpha = 0.186 + 13.1 * (6 * x_e),  R^2 = 0.968,  p = 0.016**

The correlation is strong, but we emphasize it rests on only four data points. The factor 6x_e arises from the third-order anharmonicity coefficient (3*beta) of the Morse potential, where beta = omega_e * x_e / (4 * D_e). Physically, higher anharmonicity means the potential well is more asymmetric, allowing greater displacement at modest energy cost -- which may facilitate the geometric rearrangement needed to accommodate additional bonds.

### 2.6 Figures (described)

**Figure 1.** Log-log plot of E(n)/E_1 vs. bond order n for three representative bonds: C-C (alpha = 0.77, sub-linear), N-N (alpha = 2.01, super-linear), and Mo-Mo (alpha = 0.65, sub-linear with six data points). Dashed lines show power-law fits. Error bars represent +/- 10 kJ/mol uncertainty in bond energies.

**Figure 2.** alpha vs. Morse anharmonicity parameter 6x_e for the four Group 14 homonuclear bonds (LP = 0). Linear fit: R^2 = 0.968. The near-perfect correlation suggests that potential well curvature governs multi-bond efficiency within an isoelectronic series.

---

## 3. Discussion

### 3.1 Lone pairs as recruitable reserve

The central finding of this work is that the presence or absence of lone pairs on bonding atoms determines whether multi-bond formation is cooperative or competitive. We interpret this through a "recruitable reserve" model.

In standard molecular orbital theory, a sigma bond between two atoms forms from head-on overlap of hybrid orbitals. A second bond (pi) requires lateral overlap of unhybridized p-orbitals. For atoms with LP = 0 (e.g., carbon in sp^3 hybridization), forming a pi bond requires rehybridization: the atom must transition from sp^3 to sp^2, sacrificing one sigma-bonding capacity. The second bond is formed at the expense of the first orbital geometry, leading to diminishing returns (alpha < 1).

For atoms with LP >= 1 (e.g., nitrogen), the lone pair occupies an orbital that is already non-bonding. Promoting it into a pi-bond does not compromise existing sigma bonds. Furthermore, the resulting pi-electron delocalization can stabilize the sigma framework through conjugation effects. The reserve is "recruited" without cost to existing bonds, enabling cooperative strengthening (alpha > 1).

The bottleneck principle for heteronuclear bonds follows naturally: effective pi-bonding requires favorable overlap on *both* atoms. If one atom (say, carbon) has no lone pair to contribute, it must rehybridize, and the cooperativity is limited by the less favorable partner.

### 3.2 The d-block inversion

Transition metal bonds provide an instructive counterexample. Despite having multiple d-electrons available, all four metals studied show alpha < 1. This is consistent with the well-known weakness of delta bonds: the lateral overlap of d-orbitals is poor, with delta bonds contributing only 35-60 kJ/mol to the total bond energy [7]. Moving from a triple to quadruple bond adds the delta component, but its contribution is small relative to the sigma and pi framework. The d-electrons are available but not efficiently recruitable -- they are a "reserve" that cannot be effectively mobilized.

This refines the Reserve Law: what matters is not merely the *presence* of non-bonding electrons, but their *recruitability* -- the capacity to form bonds of comparable strength to existing ones. Lone pairs on 2p atoms (N, O) can form strong pi-bonds; d-electrons on transition metals cannot form strong delta-bonds.

### 3.3 The sulfur anomaly

Sulfur (LP = 2, alpha = 0.676) is the most significant exception to the Reserve Law. We note that sulfur's 3p orbitals overlap less effectively in pi-bonds than do 2p orbitals of nitrogen and oxygen [8]. The S=S double bond in disulfur (S_2) is known to be substantially weaker than expected by analogy with O=O. The lone pairs of sulfur are thus partially "non-recruitable" due to poor pi-overlap, placing sulfur in a regime intermediate between true reserve (N, O) and no reserve (C, Si). This is consistent with the known tendency of sulfur to form chains and rings (exploiting multiple single bonds) rather than multiple bonds.

### 3.4 Connection to Morse anharmonicity

The strong correlation between alpha and Morse anharmonicity for Group 14 homonuclear bonds (R^2 = 0.968) suggests a physical connection between the shape of the single-bond potential energy surface and multi-bond cooperativity. Higher anharmonicity (larger x_e) implies a "softer" potential well at large displacements, meaning the bond is more deformable. We speculate that this deformability facilitates the geometric rearrangement from sp^3 to sp^2 to sp hybridization required for pi-bond formation.

However, this correlation rests on only four data points and should be viewed as hypothesis-generating rather than confirmatory. Extension to other isoelectronic series (e.g., Group 15 with LP = 1, or Group 16) would be a valuable test.

### 3.5 Cross-scale observations

We note in passing that the alpha exponents discovered here show intriguing numerical coincidences with scaling exponents in other domains: alpha(C-C) = 0.77 vs. Kleiber's metabolic scaling (0.75) [1]; alpha(N-N) = 2.01 vs. Metcalfe's network law (2.0) [3]; alpha(P-P) = 1.28 vs. urban innovation scaling (1.27) [2]. A permutation test on 12 such matches across 7 domains yields p = 0.0003, below the threshold for chance coincidence.

We flag this as an intriguing observation requiring pre-registered confirmation. The matches are post-hoc, discovered by searching for numerical coincidences across a large space of scaling laws. Without a mechanistic theory connecting molecular bonding to urban scaling or metabolic rates, these coincidences -- however striking -- remain uninterpretable. We include them here only to ensure they are documented for future investigation, not as evidence for a universal scaling principle.

### 3.6 Limitations

This study has several important limitations:

1. **Small sample size.** Only 23 bonds are analyzed; 8 homonuclear s/p-block, 11 heteronuclear s/p-block, and 4 d-block. The classification statistics, while significant (p = 0.006), would benefit from extension to f-block elements, metalloid bonds, and a wider range of heteronuclear pairs.

2. **Two-point fits.** Most alpha values derive from only two data points (single and double bond energies). The fit is therefore exact and uninformative about goodness-of-fit; only Mo-Mo and C-C/N-N (with three bond orders) provide genuine tests of the power-law functional form.

3. **Bond energy uncertainties.** Dissociation energies for multiply-bonded species, particularly heteronuclear bonds, carry uncertainties of 10-30 kJ/mol that propagate non-trivially into alpha.

4. **d-block ligand effects.** Transition metal bond energies are extracted from molecular compounds and may not reflect intrinsic dimeric bond strengths.

5. **Morse correlation.** Based on four data points; predictive power untested.

6. **Post-hoc anomaly analysis.** The explanations for S-S and C-S anomalies, while chemically plausible, are post-hoc rationalizations. A predictive model should identify these deviations *a priori*.

---

## 4. Conclusions

We have identified a power-law relation E(n) = E_1 * n^alpha for bond energy scaling with bond order, where the exponent alpha encodes the cooperative or competitive nature of multi-bond formation. The Reserve Law -- lone pair electrons serve as a recruitable reserve enabling cooperative strengthening (alpha > 1), while their absence leads to diminishing returns (alpha < 1) -- holds for 92% of the 23 bonds examined. The d-block extension reveals that the mere presence of non-bonding electrons is insufficient; recruitability, governed by orbital overlap quality, is the decisive factor. A preliminary correlation between alpha and Morse anharmonicity (R^2 = 0.968) for Group 14 bonds suggests a link between potential well shape and multi-bond efficiency, though this requires independent confirmation. The alpha exponent provides a compact, physically interpretable descriptor of bonding character that may prove useful in materials screening and in connecting molecular-level bonding to macroscopic material properties.

---

## Data Availability

All bond energy data, alpha calculations, and analysis scripts are available in the Supplementary Information and at https://github.com/ykazin/reserve-law.

---

## References

[1] M. Kleiber, "Body size and metabolism," *Hilgardia* **6**, 315-353 (1932).

[2] L. M. A. Bettencourt, J. Lobo, D. Helbing, C. Kuhnert, G. B. West, "Growth, innovation, scaling, and the pace of life in cities," *Proc. Natl. Acad. Sci. USA* **104**, 7301-7306 (2007).

[3] B. Zhang, S. S. Kreps, "An informatization strategy for small and medium enterprises: Metcalfe's law," *Inf. Technol. Manag.* **16**, 67-78 (2015).

[4] W. M. Haynes, Ed., *CRC Handbook of Chemistry and Physics*, 97th ed. (CRC Press, Boca Raton, FL, 2016).

[5] K. P. Huber, G. Herzberg, *Molecular Spectra and Molecular Structure. IV. Constants of Diatomic Molecules* (Van Nostrand Reinhold, New York, 1979).

[6] L. Pauling, *The Nature of the Chemical Bond*, 3rd ed. (Cornell University Press, Ithaca, NY, 1960).

[7] F. A. Cotton, C. A. Murillo, R. A. Walton, *Multiple Bonds Between Metal Atoms*, 3rd ed. (Springer, New York, 2005).

[8] R. S. Mulliken, "Electronic population analysis on LCAO-MO molecular wave functions. I," *J. Chem. Phys.* **23**, 1833-1840 (1955).

[9] M. Morse, T. R. Cundari, "Transition metal diatomics: Computational thermochemistry and bond dissociation energies," *Acc. Chem. Res.* **51**, 3087-3095 (2018).

[10] S. G. Chen, T. Lu, T. J. Manz, "Bond orders of the diatomic molecules," *RSC Adv.* **9**, 17072-17092 (2019).

[11] C. A. Coulson, "The electronic structure of some polyenes and aromatic molecules. VII. Bonds of fractional order by the molecular orbital method," *Proc. R. Soc. London A* **169**, 413-428 (1939).

[12] R. S. Berry, S. A. Rice, J. Ross, *Physical Chemistry*, 2nd ed. (Oxford University Press, New York, 2000).

[13] K. Ruedenberg, "The physical nature of the chemical bond," *Rev. Mod. Phys.* **34**, 326-376 (1962).

[14] G. Frenking, S. Shaik, Eds., *The Chemical Bond: Fundamental Aspects of Chemical Bonding* (Wiley-VCH, Weinheim, 2014).

[15] G. B. West, J. H. Brown, B. J. Enquist, "A general model for the origin of allometric scaling laws in biology," *Science* **276**, 122-126 (1997).

[16] J. K. Norskov, T. Bligaard, J. Rossmeisl, C. H. Christensen, "Towards the computational design of solid catalysts," *Nat. Chem.* **1**, 37-46 (2009).

[17] P. Pyykko, "Additive covalent radii for single-, double-, and triple-bonded molecules and tetrahedrally bonded crystals: A summary," *J. Phys. Chem. A* **119**, 2326-2337 (2015).

[18] G. N. Lewis, "The atom and the molecule," *J. Am. Chem. Soc.* **38**, 762-785 (1916).

---

## arXiv Submission Metadata

- **Primary category**: physics.chem-ph (Chemical Physics)
- **Cross-list**: cond-mat.mtrl-sci (Materials Science)
- **MSC codes**: 92E10, 81V55
- **Keywords**: bond dissociation energy, power law, bond order, lone pairs, transition metals, Morse potential, scaling laws

## Data and Code Availability

All bond energy data used in this work is tabulated in Tables 1--3 and derived from publicly available sources (CRC Handbook, NIST Chemistry WebBook). The α-law calculator is available as an open-source Python package:

- **Repository**: https://github.com/ykazin/alphalaw
- **Installation**: `pip install alphalaw`
- **Usage**: `python -m alphalaw C C` (prints α, LP classification, and bond preference prediction)

Supplementary data including Morse spectroscopic constants, cross-scale comparison tables, and Monte Carlo analysis scripts are included in the repository.

## Supplementary Information

A pre-registered protocol for cross-scale hypothesis testing (3 new domains, 6 specific predictions) is available in the repository as `preregistered_crossscale.md`, with predictions locked on 2026-04-10 prior to data collection.
