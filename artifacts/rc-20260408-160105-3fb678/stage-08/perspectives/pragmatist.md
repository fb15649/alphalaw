# Feasible Hypotheses from Vortex Geometry–Property Synthesis

---

## Hypothesis 1: Frustration Index of Space Group Lattices Predicts Magnetic Ordering Type and Curie Temperature

### Concrete, Testable Claim

For each of the 230 crystallographic space groups, compute a geometric frustration index *F* from the symmetry operations relating nearest-neighbor magnetic sites. Then:

- **Claim A**: Space groups with *F* > threshold τ₁ will have >80% of their known crystalline compounds classified as ferromagnetic.
- **Claim B**: Within ferromagnetic elements, *F* correlates positively with Curie temperature *T*c (Pearson r > 0.6).
- **Claim C**: Space groups with *F* ≈ 0 (maximally frustrated) will have >80% of compounds classified as paramagnetic or spin-glass.

**Methodology**:

1. **Data acquisition**: Pull crystal structures and magnetic properties from the Materials Project API (~150,000 entries) and the MAGNDAS magnetic structure database (~1,500 ordered magnetic structures). Supplement with elemental data from CRC Handbook (Tc for Fe, Co, Ni, Gd, etc.).

2. **Frustration index computation**: For each space group, identify the magnetic sublattice (Wyckoff positions occupied by magnetic ions). For each triangle of nearest-neighbor sites (i, j, k), assign a sign to each coupling K_ij based on whether the space group symmetry operation relating sites i and j preserves (+1) or reverses (−1) a common polar axis. Then:
   
   *F* = |Σ sgn(K_ij · K_jk · K_ki)| / N_triangles

   where N_triangles counts all unique nearest-neighbor triangles on the magnetic sublattice.

3. **Classification test**: Bin all materials into F > 0.7 (unfrustrated), 0.3 < F < 0.7 (partially frustrated), F < 0.3 (highly frustrated). Compute the fraction of ferromagnetic, antiferromagnetic, paramagnetic, and diamagnetic materials in each bin. Test with χ² contingency table.

4. **Tc correlation test**: For all ferromagnetic elemental metals and simple compounds with measured Tc, plot Tc vs. F and compute Pearson/Spearman correlation.

### Why Achievable with Limited Compute

- The frustration index is a **combinatorial calculation** on small graphs (unit cell typically has 1–20 magnetic sites). No molecular dynamics, no DFT, no simulation. Each space group takes seconds on a laptop.
- Materials Project has a free API with programmatic access. MAGNDAS is publicly available.
- Total compute: ~230 space groups × ~seconds each = **under 1 CPU-hour** for the core calculation. Database queries are the bottleneck (hours, not GPU-hours).

### Rationale Based on Proven Techniques

- Geometric frustration is a mature concept in condensed matter physics (Binder & Young, *Rev. Mod. Phys.* 1988). The frustration index is standard in spin glass theory.
- López-Cabrelles et al. (2021) already showed that crystal symmetry determines magnetic ordering type in 2D MOFs. This hypothesis generalizes that finding using a single numerical index.
- Thiel et al. (2020) showed geometric distortion modulates magnetic anisotropy—the frustration index captures this quantitatively.
- The Edwards-Anderson order parameter is the standard measure in frustrated magnetism literature.

### Measurable Prediction and Failure Condition

| Prediction | Success Criterion | Failure Criterion |
|---|---|---|
| Ferromagnetic materials cluster in low-frustration space groups | ≥75% of ferromagnets have F > 0.5 | <50% of ferromagnets have F > 0.5 |
| Tc correlates with F across ferromagnetic elements | r > 0.5, p < 0.05 | r < 0.3 or p > 0.1 |
| High-frustration groups are predominantly paramagnetic | ≥70% of F < 0.3 materials are paramagnetic/diamagnetic | No enrichment (random distribution) |
| Transition metals in BCC (Im3̄m) have higher F than FCC (Fm3̄m) | Confirmed for Fe-BCC vs. Cu-FCC class | No systematic difference |

**Critical failure mode**: If frustration index F shows no correlation with magnetic ordering type, the hypothesis that space group geometry alone (via vortex alignment constraints) determines ferromagnetism is falsified for this formulation.

### Resource Requirements

| Resource | Estimate |
|---|---|
| Personnel | 1 researcher, 3-4 months |
| Compute | Laptop-scale; <10 CPU-hours total |
| Data | Materials Project API (free), MAGNDAS (free), CRC Handbook |
| Software | Python (pymatgen, networkx, scipy), standard libraries |
| Budget | ~$0 (using open databases) |

---

## Hypothesis 2: Kuramoto Critical Coupling on Space Group Graphs Classifies Magnetic Ordering with >80% Accuracy

### Concrete, Testable Claim

Model each magnetic ion in a crystal as a coupled oscillator whose coupling graph topology is determined by the space group. The Kuramoto critical coupling *K*c — computed purely from graph structure — predicts whether the system supports coherent alignment (ferromagnetism), competing alignments (antiferromagnetism), or incoherent disorder (paramagnetism).

- **Claim**: A binary classifier based on K_effective / K_c > 1 (synchronization condition) correctly labels ≥80% of materials as ferromagnetic vs. non-ferromagnetic.

**Methodology**:

1. **Graph construction**: For each space group, build the magnetic coupling graph G_SG:
   - Nodes = Wyckoff positions occupied by magnetic ions
   - Edges = pairs within a nearest-neighbor distance threshold (defined by the ionic radius sum + tolerance)
   - Edge weights: K_ij = +1 if the space group operation relating sites i→j is a proper rotation preserving a unique polar axis; K_ij = −1 if it's an improper operation (mirror, inversion, rotoinversion) that reverses the axis; K_ij = 0 for glide reflections.

2. **Critical coupling computation**: Use the standard Kuramoto result for networks:
   
   *K*c = 2 / [π · g(ω₀)]
   
   where g(ω₀) is the density of natural frequencies at the center. For identical oscillators (same ion type), g(ω₀) → δ-function and Kc → 0, so we use the finite-size correction:
   
   *K*c ≈ λ₂⁻¹ / N
   
   where λ₂ is the algebraic connectivity (second-smallest eigenvalue of the graph Laplacian), computed for the signed coupling matrix.

3. **Effective coupling**: K_eff = Σ|K_ij| / N_edges, reflecting the mean coupling strength from geometry.

4. **Classification**: If K_eff / K_c > 1 → predict ferromagnetic. If K_eff / K_c < 1 with dominant negative couplings → predict antiferromagnetic. If graph is disconnected or K_eff ≈ 0 → predict paramagnetic.

5. **Validation**: Test on Materials Project entries with known magnetic ordering (heuristic labels: ferromagnetic, antiferromagnetic, non-magnetic). Use 70/30 train/test split (train only to tune the distance threshold, not the model). Report accuracy, precision, recall, F1.

6. **Ablation**: Compare against baseline classifiers using (a) space group alone, (b) element alone, (c) space group + element. The Kuramoto-graph model should outperform all baselines.

### Why Achievable with Limited Compute

- Graph construction from space groups is **deterministic and fast**—pymatgen parses space group symmetry operations in milliseconds.
- Eigenvalue computation for graphs of size 1–50 nodes is trivial (numpy.linalg.eigh handles this in microseconds).
- The Materials Project API returns magnetic ordering labels for ~30,000 entries. Query + process = hours, not days.
- **No training of ML models**—this is a physics-based classifier with at most one tunable parameter (the distance threshold). Total compute: <5 CPU-hours.

### Rationale Based on Proven Techniques

- The Kuramoto model is one of the most studied models in nonlinear dynamics with >10,000 citations. Its synchronization criterion is analytically proven for many graph topologies (Acebrón et al., *Rev. Mod. Phys.* 2005).
- López-Cabrelles et al. (2021) showed that symmetry determines magnetic ordering. The Kuramoto framework provides the *mechanism*: symmetry → coupling graph → synchronization condition → ordering type.
- Topp et al. (2021) proved that quantum geometry (not dynamics) governs electromagnetic response. The Kuramoto graph captures this static geometric constraint.
- Couzin et al. (2005) demonstrated that interaction zone geometry alone predicts collective alignment vs. disorder in animal groups—the same principle should apply to vortex micro-pumps in crystals.

### Measurable Prediction and Failure Condition

| Prediction | Success Criterion | Failure Condition |
|---|---|---|
| Kuramoto classifier accuracy | ≥80% on held-out test set | <65% (no better than random by space group) |
| Outperforms element-only baseline | ΔF1 > 0.10 vs. element-only | ΔF1 < 0.05 |
| Im3̄m (BCC, Fe) classifies as ferromagnetic | K_eff/K_c > 1 confirmed | K_eff/K_c < 1 |
| Fm3̄m (FCC, Cu) classifies as non-ferromagnetic | K_eff/K_c < 1 confirmed | K_eff/K_c > 1 |
| Algebraic connectivity λ₂ separates FM from AFM | ROC-AUC > 0.75 for λ₂ alone | ROC-AUC < 0.60 |

**Critical failure mode**: If the Kuramoto graph classifier performs no better than a lookup table of (space group → majority ordering type), then the coupling-graph formalism adds no explanatory power and the vortex synchronization mechanism is unsupported.

### Resource Requirements

| Resource | Estimate |
|---|---|
| Personnel | 1 researcher, 2-3 months |
| Compute | <5 CPU-hours total |
| Data | Materials Project API (free), ~30K entries with magnetic labels |
| Software | Python (pymatgen, networkx, numpy, scikit-learn) |
| Budget | ~$0 |

---

## Hypothesis 3: Icosahedral Geometry Minimizes Inter-Vortex Distance Variance, Predicting Quasicrystal Stability

### Concrete, Testable Claim

The five Platonic solids can be ranked by the variance of their vertex-to-vertex distances (the "vortex harmony function" *H*). The dodecahedron (12 vertices, icosahedral symmetry) minimizes *H*, and this geometric optimality explains why quasicrystals with local icosahedral order exhibit anomalous stability and unusual properties.

- **Claim A**: H(dodecahedron) < H(all other Platonic solids) — the dodecahedron has the most uniform inter-vertex distance distribution.
- **Claim B**: Among known quasicrystals, those with higher local icosahedral order (quantified by XRD peak sharpness of icosahedral reflections) have higher thermal stability (higher onset temperature for crystallization).
- **Claim C**: The predicted equilibrium inter-vortex distance from classical vortex ring dynamics (Saffman model), parameterized with superfluid vacuum density ρ = μ₀, reproduces the nearest-neighbor distance in Al-Mn quasicrystals (2.86 Å) within ±15%.

**Methodology**:

1. **Vortex harmony function computation**: For each Platonic solid with N vertices at positions {r_i}:
   
   *H* = (1/N²) Σᵢ Σⱼ |rᵢⱼ − r̄|² / r̄²
   
   where rᵢⱼ = |rᵢ − rⱼ| and r̄ = mean inter-vertex distance. Normalize all solids to unit circumradius. Compute *H* for tetrahedron (N=4), cube (N=8), octahedron (N=6), dodecahedron (N=20), icosahedron (N=12). Rank by *H*.

2. **Quasicrystal stability correlation**: From the literature (Steurer & Deloudi, *Crystallography of Quasicrystals* 2009), compile a dataset of ~20 well-characterized quasicrystals (Al-Mn, Al-Pd-Mn, i-AlCuFe, Zn-Mg-RE, etc.) with:
   - Local icosahedral order parameter (from pair distribution function or XRD)
   - Crystallization onset temperature T_x
   - Nearest-neighbor distance d_NN
   Plot T_x vs. icosahedral order parameter and compute correlation.

3. **Vortex equilibrium distance prediction**: For two coaxial toroidal vortex rings in a superfluid with density ρ = μ₀ = 4π × 10⁻⁷ kg·m⁻¹, circulation quantum Γ = h/m_e (using the Williamson-van der Mark electron mass parameter), and core size a ≈ classical electron radius × geometric factor, compute the equilibrium separation d_eq using the Saffman formula:
   
   *d*_eq ≈ (Γ² / 4π²ρ·R²) · ln(8R/a)
   
   where R is the vortex ring radius (identified with the atomic radius). Compare d_eq with known d_NN for icosahedral quasicrystals.

### Why Achievable with Limited Compute

- The harmony function *H* is a **closed-form calculation** on 5 Platonic solids. Done by hand or in a spreadsheet in minutes.
- The quasicrystal dataset is small (~20-40 entries) and literature-based. No database mining needed.
- The Saffman equilibrium formula is **analytical**. One formula evaluation per material. No simulation.
- Total compute: effectively zero. This is a pen-and-paper + literature study.

### Rationale Based on Proven Techniques

- Saffman's *Vortex Dynamics* (1992) provides exact results for coaxial vortex ring equilibria. These are standard fluid dynamics, not speculative.
- The Caspar-Klug quasi-equivalence model successfully explained icosahedral viral capsid stability through a closely analogous argument: icosahedral geometry minimizes the strain energy of quasi-equivalent protein interactions.
- Gam et al. (2020) empirically showed that icosahedral superatom assemblies have special stability—the harmony function provides the geometric explanation.
- The variance of inter-particle distances is a standard order parameter in condensed matter (related to the pair distribution function).

### Measurable Prediction and Failure Condition

| Prediction | Success Criterion | Failure Condition |
|---|---|---|
| Dodecahedron minimizes H | H(dodecahedron) < H(all others) by >10% | Any other solid has lower H |
| Quasicrystal stability vs. icosahedral order | r > 0.5 between T_x and icosahedral order parameter | r < 0.2 |
| Vortex equilibrium distance matches d_NN | |d_eq − d_NN| / d_NN < 0.15 | Error > 30% |
| H ranking predicts relative stability of Platonic cluster types | Cluster stability order matches H ranking | No correspondence |

**Critical failure mode**: If the dodecahedron does *not* minimize the harmony function *H*, then the proposed geometric explanation for quasicrystal stability is wrong in this formulation. If the vortex equilibrium distance is off by >30%, the superfluid parameterization (ρ = μ₀) is falsified for this application.

### Resource Requirements

| Resource | Estimate |
|---|---|
| Personnel | 1 researcher, 1-2 months |
| Compute | Negligible (closed-form + literature data) |
| Data | Literature compilation (~20-40 quasicrystals) |
| Software | Python or even spreadsheet for calculations |
| Budget | ~$0 |

---

## Hypothesis 4: Platonic Subgroup Membership Captures >60% of Variance in Material Properties via PCA of Symmetry-Property Matrices

### Concrete, Testable Claim

If the 230 space groups are encoded as binary feature vectors indicating membership in Platonic solid symmetry subgroups (tetrahedral T_d, octahedral O_h, icosahedral I_h, and their subgroups), principal component analysis on the resulting (space groups × properties) matrix will show that the first 3 Platonic-subgroup principal components capture >60% of variance in magnetic susceptibility, electrical conductivity, and hardness.

- **Claim A**: The first 3 PCs of the Platonic-subgroup feature matrix explain >60% of property variance, outperforming the first 3 PCs of conventional crystal system encoding (7 crystal systems).
- **Claim B**: The loadings of PC1, PC2, PC3 correspond to tetrahedral, octahedral, and icosahedral symmetry dominance respectively.

**Methodology**:

1. **Feature encoding**: For each of the 230 space groups, compute a binary feature vector of length ~15:
   - Contains T_d subgroup (yes/no)
   - Contains O_h subgroup (yes/no)
   - Contains D_nd subgroups (n = 2,3,4,6)
   - Contains C_nv subgroups (n = 2,3,4,6)
   - Contains inversion symmetry (yes/no)
   - Contains 5-fold or 10-fold axes (yes/no — rare but critical for quasicrystal-adjacent groups)
   - Point group order, Bravais lattice type (7 types as one-hot)

2. **Property matrix**: For ~5,000-10,000 materials from Materials Project with measured/computed properties:
   - Magnetic susceptibility (or magnetic ordering type as numerical code)
   - Band gap (proxy for conductivity)
   - Bulk modulus (proxy for hardness)
   - Melting temperature (where available)
   - Density

3. **PCA**: Perform PCA on the feature matrix, then regress properties against the principal components. Report variance explained (R²) for each property.

4. **Baseline comparison**: Compare against:
   - PCA on 7 crystal system features
   - PCA on 14 Bravais lattice features
   - PCA on full 230 space group one-hot encoding
   - Random feature baseline

5. **Interpretation**: Examine PC loadings to determine which symmetry features drive each component. If PC1 loads heavily on tetrahedral subgroup features and PC1 explains most hardness variance, this supports the vortex framework's prediction that tetrahedral vortex configurations produce hard materials (diamond, SiC).

### Why Achievable with Limited Compute

- PCA on a 230 × 15 matrix is instantaneous. Even on the full material-property matrix (10,000 × 15), it takes seconds.
- Materials Project API queries for properties are fast and free.
- No training of neural networks, no hyperparameter tuning. Standard linear algebra.
- Total compute: <1 CPU-hour including all queries and analysis.

### Rationale Based on Proven Techniques

- PCA-based dimensional reduction is the standard approach for testing whether a feature space captures structure-property relationships (Ghiringhelli et al., *Nature Physics* 2015, "Big data of materials science").
- Díaz et al. (*Nature* 2016) used exactly this approach to show that 6 functional traits capture global plant property variance—the same methodology applied here.
- The crystal system → property relationship is established. The question is whether *Platonic subgroup* features capture *more* variance, which is a quantitative, answerable question.
- Cai et al. (2021) articulated cross-scale design principles; PCA tests whether these principles are reducible to a small number of symmetry axes.

### Measurable Prediction and Failure Condition

| Prediction | Success Criterion | Failure Condition |
|---|---|---|
| Platonic PCs explain >60% of property variance | Cumulative R² > 0.60 for first 3 PCs | R² < 0.40 |
| Platonic features outperform crystal system features | ΔR² > 0.10 vs. 7-feature baseline | ΔR² < 0.05 |
| PC loadings map to Platonic symmetry types | Top loadings of PC1-3 are Platonic features, not random | Loadings are diffuse/uninterpretable |
| Tetrahedral PC explains hardness variance | R²(hardness ~ PC_tet) > R²(hardness ~ any other single PC) | No systematic loading-property correspondence |

**Critical failure mode**: If Platonic subgroup features capture no more variance than standard crystal system features, the vortex topology framework provides no additional explanatory power over conventional crystallography for bulk material properties. This would not falsify the vortex model itself but would falsify the claim that Platonic subgroup membership is the *relevant* symmetry descriptor.

### Resource Requirements

| Resource | Estimate |
|---|---|
| Personnel | 1 researcher, 1-2 months |
| Compute | <1 CPU-hour |
| Data | Materials Project API (free), ~10K entries |
| Software | Python (pymatgen, pandas, scikit-learn, matplotlib) |
| Budget | ~$0 |

---

## Summary: Recommended Execution Order

| Priority | Hypothesis | Timeline | Compute | Falsification Power |
|---|---|---|---|---|
| 1 | **H3: Dodecahedral harmony function** | 1-2 months | Negligible | If dodecahedron doesn't minimize H, geometric optimality claim fails |
| 2 | **H1: Frustration index → magnetic ordering** | 3-4 months | <10 CPU-hrs | If no F–ordering correlation, space-group-geometry→magnetism link fails |
| 3 | **H4: Platonic PCA variance capture** | 1-2 months | <1 CPU-hr | If Platonic features don't outperform crystal system, framework adds nothing |
| 4 | **H2: Kuramoto classifier** | 2-3 months | <5 CPU-hrs | If accuracy <65%, synchronization mechanism unsupported |

**Start with H3** (quickest, cheapest, clearest yes/no answer). If the dodecahedron minimizes *H*, proceed to H1 and H4 in parallel. If H1 and H4 both show signal, invest in H2 as the most rigorous test. Total cost for all four hypotheses: **~$0 compute, ~8-12 months of one researcher's time**.