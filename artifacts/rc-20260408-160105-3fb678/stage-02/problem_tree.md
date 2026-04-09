# Research Problem Decomposition: Toroidal Vortex Geometry and Material Properties

---

## Source

**Input framework:** Cross-scale topological correlation between crystalline symmetry and bulk material properties under toroidal vortex atom theory, with Platonic solid subgroup mapping as the central analytical instrument.

**Investigator:** Prof. Chen Wei, Institute for Advanced Study
**Generated:** 2025-07-14
**Project tag:** `my-research`

---

## Sub-questions

### SQ-1: The Platonic Subgroup Mapping — A Complete Classification

**Question:** What is the exhaustive mathematical mapping from the 230 crystallographic space groups into Platonic solid subgroup families (tetrahedral, octahedral/cubic, icosahedral/dodecahedral, prismatic/degenerate), and how are known materials distributed across these families?

**Why this is foundational:** Every subsequent investigation depends on this classification. It converts the vague intuition that "crystal structure reflects vortex topology" into a precise, finite, checkable mathematical object.

**Specific tasks:**

1. Decompose each of the 230 space groups by identifying its point group and maximal Platonic supergroup.
2. Assign each space group to a Platonic family based on whether its point group is a subgroup of T<sub>d</sub> (tetrahedral, order 24), O<sub>h</sub> (octahedral, order 48), or I<sub>h</sub> (icosahedral, order 120).
3. Resolve the **icosahedral exclusion problem**: the crystallographic restriction theorem forbids 5-fold rotational symmetry in periodic crystals, so no space group maps to the icosahedral/dodecahedral family. Formalize how this constraint manifests in the vortex framework — is icosahedral symmetry "frustrated" in periodic matter?
4. Treat the remaining point groups (C<sub>n</sub>, D<sub>n</sub>, S<sub>n</sub> families for n = 1, 2, 3, 4, 6) as "degenerate" or "reduced-symmetry" subgroups of Platonic solids. Determine whether a natural hierarchy exists (e.g., C<sub>3</sub> as a subgroup of both T<sub>d</sub> and O<sub>h</sub> — which Platonic family claims it?).
5. Count the distribution: how many space groups fall into each Platonic family? How many known materials (from Materials Project) fall into each?

**Deliverable:** A lookup table (space group number → Platonic family) with mathematical justification, plus a distribution histogram across N ≥ 50,000 materials.

**Dependencies:** None (foundational).

**Success criterion:** Complete, unambiguous classification with no orphan space groups. The hierarchy is consistent (no space group claimed by two families unless it genuinely sits at their intersection).

---

### SQ-2: The Vortex Alignment Index Ψ — Constructing a Topological Invariant

**Question:** Can a computable topological invariant Ψ ∈ [0, 1] be derived from crystal symmetry operations that quantifies the degree to which a vortex configuration permits coherent uniaxial alignment, and does Ψ alone distinguish ferromagnetic from paramagnetic/diamagnetic ordering?

**Why this is the novel theoretical contribution:** This is the mechanism by which vortex topology is claimed to generate ferromagnetism. If Ψ can be formalized and validated, it constitutes a new topological invariant in materials science — one that does not exist in standard band theory.

**Specific tasks:**

1. **Formalize "vortex pump orientation."** In the toroidal vortex model, each atomic vortex has a preferred axis (the circulation axis of the torus). In a crystal, symmetry operations (rotations, reflections, inversions, translations, glides, screws) constrain the possible orientations of these axes. Define the action of each space group operation on the axial vector field.

2. **Define Ψ mathematically.** Provisional definition: Ψ is the fraction of symmetry operations in the space group that preserve a fixed preferred direction **n̂**. If all operations preserve **n̂** (trivial point group, or only operations parallel to **n̂**), then Ψ = 1 (perfect coherent alignment possible). If operations systematically mix directions, Ψ → 0. Formalize this using representation theory: Ψ = dim(V<sub>trivial</sub>) / dim(V), where V is the representation space of axial vectors under the point group.

3. **Compute Ψ for all 230 space groups** using representation theory (character tables are tabulated).

4. **Validate against known magnetic materials.** Extract a list of known ferromagnets (Fe, Co, Ni, Fe<sub>3</sub>O<sub>4</sub>, CrO<sub>2</sub>, SmCo<sub>5</sub>, Nd<sub>2</sub>Fe<sub>14</sub>B, etc.) and paramagnets/diamagnets (Al, Cu, Au, Bi, NaCl, etc.) from the Materials Project. Compute Ψ for each. Test whether Ψ > threshold separates ferromagnets from non-ferromagnets.

5. **Control test:** Compare Ψ's predictive power against the known magnetic space group classification (Shubnikov groups, 1651 magnetic space groups). If Ψ recapitulates Shubnikov classification with no additional information, note this explicitly — it still provides a vortex-theoretic *derivation* of a known result, which is valuable.

**Dependencies:** SQ-1 (need the Platonic family assignment to interpret Ψ in the vortex framework).

**Success criteria:**
- Tier 1: Ψ classification accuracy ≥ 75% for ferromagnet vs. non-ferromagnet (vs. ~50% random baseline).
- Tier 2: Ψ predicts a ferromagnetic ordering temperature trend (T<sub>C</sub> correlates with Ψ within ferromagnetic family).
- Tier 3 (null): Ψ is mathematically equivalent to known magnetic symmetry classification — still publishable as a topological derivation.

---

### SQ-3: The Statistical Correlation Study — Empirical Validation

**Question:** Across a dataset of N ≥ 500 materials, is there a statistically significant correlation (Spearman |ρ| > 0.3, p < 0.001) between Platonic subgroup membership / Ψ and measured physical properties (magnetic susceptibility χ, electrical conductivity σ, Vickers hardness H<sub>v</sub>, melting temperature T<sub>m</sub>), after controlling for known crystallographic and electronic-structure predictors?

**Why this is the empirical anchor:** Without statistical validation, the vortex framework remains aesthetic speculation. This sub-question grounds the theory in data.

**Specific tasks:**

1. **Data extraction.** Using the Materials Project API (pymatgen), extract for each material: formula, space group, computed/experimental χ, computed band gap (proxy for σ), computed hardness (if available; otherwise use elastic modulus proxy), computed formation energy (proxy for T<sub>m</sub>). Target N ≥ 500 materials with complete data. Curate: remove entries marked "theoretical only" if experimental data is required.

2. **Feature engineering.** For each material, compute:
   - Platonic family label (categorical, from SQ-1)
   - Ψ (continuous, from SQ-2)
   - Point group order (continuous, control variable)
   - Number of atoms per unit cell (continuous, control variable)
   - Known electronic features: band gap, density of states at Fermi level (control variables)

3. **Primary analysis:** Spearman correlation between Ψ and log|χ|. Report ρ, p-value, 95% CI via bootstrap (N = 10,000 resamples).

4. **Secondary analysis:** ANOVA/Kruskal-Wallis test — do Platonic families differ significantly in mean χ, σ, H<sub>v</sub>, T<sub>m</sub>?

5. **Control analysis (critical):** Fit a standard regression model predicting χ from known electronic features (band gap, DOS at E<sub>F</sub>). Then add Ψ as a feature. Does Ψ improve prediction (ΔR², AIC comparison)? If Ψ adds predictive power *beyond* standard features, this is the "Keplerian signal in the residuals."

6. **Robustness checks:** Stratified analysis by chemistry (transition metals vs. main group vs. oxides), by structure type (metallic vs. covalent vs. ionic), by sample size quantile.

**Dependencies:** SQ-1 and SQ-2 must be complete.

**Success criteria:**
- Tier 1: Significant correlation between Ψ and log|χ| (ρ > 0.4, p < 0.001) OR Ψ improves prediction of χ beyond electronic features (ΔR² > 0.05).
- Tier 2: The same Ψ correlates with multiple properties (χ, σ, H<sub>v</sub>) — evidence for a universal topological factor.
- Tier 3 (null): No significant correlations. Publish null result as constraint on vortex theory.

---

### SQ-4: The Icosahedral Frustration Principle and Quasicrystal Anomaly

**Question:** Do icosahedral quasicrystals exhibit systematic deviations from density functional theory (DFT) predictions in their physical properties (particularly thermal conductivity, electrical resistivity, and hardness), and are these deviations in the direction predicted by treating the dodecahedron as a "special" vortex configuration with enhanced topological stability?

**Why this is the highest-impact specific prediction:** Quasicrystals are the *only* condensed matter phase where icosahedral symmetry is realized. If the dodecahedron is a special vortex configuration, this is where the signal should be strongest. This sub-question is the most falsifiable.

**Specific tasks:**

1. **Compile quasicrystal property dataset.** From the International Institute for Quasicrystals database (iqc.to.infn.it) and literature (Steurer & Deloudi 2009; Dubois 2012), extract measured properties for known icosahedral quasicrystal phases: Al-Cu-Fe, Al-Pd-Mn, Zn-Mg-RE (RE = Y, Ho, Er), Ti-Zr-Ni, etc. Target: N ≥ 20 distinct compositions with thermal conductivity κ, electrical resistivity ρ, hardness H<sub>v</sub>, and elastic moduli.

2. **Obtain DFT predictions.** For each quasicrystal, find published DFT (or DFT+DMFT) predicted values for the same properties. Where not available, note this as a gap.

3. **Compute residuals.** For each property, compute Δ = measured − DFT_predicted. This is the "anomaly."

4. **Predict the sign of the anomaly from vortex theory.** If the dodecahedron is a "special" (enhanced stability) vortex configuration, what does this predict?
   - Enhanced topological stability → reduced phonon scattering → anomalous thermal conductivity?
   - Or: enhanced topological stability → frustrated phonon modes → *reduced* thermal conductivity?
   - The vortex theory must make a *specific directional prediction* before looking at data.
   - **Formalization task:** From the vortex model, derive whether "special" topology increases or decreases thermal transport, electrical transport, and mechanical hardness relative to DFT predictions.

5. **Statistical test:** One-sample t-test on residuals. If vortex theory predicts Δκ > 0, test whether mean Δκ > 0 with p < 0.05. Compute Cohen's d effect size.

6. **Compare with periodic approximants.** For quasicrystals with known crystalline approximants (e.g., α-AlMnSi approximant to i-AlMnSi), compare properties. The approximant has similar chemistry but lacks icosahedral symmetry. If icosahedral vortex topology is causal, the approximant should *not* show the anomaly.

**Dependencies:** SQ-1 (need to understand icosahedral exclusion from periodic crystals), SQ-4 is partially independent of SQ-2 and SQ-3.

**Success criteria:**
- Tier 1: Systematic anomaly in icosahedral quasicrystals (Cohen's d > 0.8, p < 0.05) in a direction consistent with vortex theory.
- Tier 2: Approximant comparison confirms the anomaly is specific to icosahedral symmetry, not chemistry.
- Tier 3 (null): No significant anomalies. Icosahedral quasicrystals are well-described by DFT. This falsifies the "special dodecahedron" claim.

---

### SQ-5: Cross-Scale Self-Similarity — The "As Above, So Below" Test

**Question:** Are the distributions of Platonic symmetry types at the nuclear scale (Skyrmion polyhedra from the Skyrme model), the atomic/molecular scale (crystal structure from SQ-1), and the cosmic scale (CMB topology constraints) statistically consistent with a universal self-similar topology, or are they independently distributed?

**Why this matters:** This is the most speculative but potentially most profound sub-question. It tests whether the Hermetic principle of correspondence has mathematical content in this context.

**Specific tasks:**

1. **Nuclear scale distribution.** From Battye & Sutcliffe (2002, arXiv:hep-th/0210147) and subsequent Skyrme model calculations, tabulate the predicted Platonic geometry for Skyrmions with baryon numbers B = 1 through ~20+. For each B, what is the predicted polyhedron? (Known results: B = 1 sphere, B = 2 torus, B = 3 tetrahedron, B = 4 cube, B = 7 dodecahedron, etc.) Compile the frequency distribution: how many Skyrmions are tetrahedral, cubic, dodecahedral, etc.?

2. **Atomic/molecular scale distribution.** From SQ-1, compile the distribution of known materials across Platonic families. Normalize to proportions.

3. **Cosmic scale.** From Luminet et al. (Nature 2003) and subsequent Planck CMB analyses, assess the current status of the Poincaré dodecahedral space hypothesis. Is it favored, disfavored, or unconstrained? What is the Bayesian evidence ratio? Compile whatever Platonic symmetry information can be extracted from CMB topology analyses.

4. **Statistical comparison.** Let P<sub>nuclear</sub>, P<sub>crystal</sub>, P<sub>cosmic</sub> be the probability distributions over Platonic symmetry types at each scale. Test:
   - H<sub>0</sub>: P<sub>nuclear</sub> = P<sub>crystal</sub> = P<sub>cosmic</sub> (self-similar)
   - H<sub>1</sub>: Distributions are independent
   - Use Kolmogorov-Smirnov or Fisher's exact test (small N problem).
   - Compute Bayes factor.

5. **Address the Planck constraint head-on.** If the Poincaré dodecahedron is disfavored by Planck data, what does this imply for the cross-scale hypothesis? Can the cosmic scale be represented by other Platonic topologies (e.g., octahedral space, toroidal topology)? Or is this a genuine falsification?

**Dependencies:** SQ-1 (crystal scale distribution). SQ-5 is independent of SQ-2, SQ-3, SQ-4.

**Success criteria:**
- Tier 1: Statistical consistency between nuclear and crystal distributions (K-S test p > 0.05) — evidence for self-similarity across 6+ orders of magnitude.
- Tier 2: All three scales consistent (would require cosmic signal).
- Tier 3 (null): Distributions are statistically distinct across scales. The "as above, so below" principle, in its naive form, is falsified for this topology metric.

---

### SQ-6: The Resolution Problem — Vortex Topology vs. Band Topology

**Question:** Can the topological invariants computed from the vortex alignment framework (Ψ, Platonic family) be expressed as functions of known topological band invariants (Z₂ invariant, Chern number, Berry phase), or does vortex topology capture genuinely orthogonal information?

**Why this is a meta-question worth investigating:** Topological materials science (2017-present) has established that *band structure topology* determines material properties. If vortex topology is mathematically reducible to band topology, it provides an alternative derivation but no new predictions. If it is *irreducible* (captures information band topology misses), this is the strongest possible result.

**Specific tasks:**

1. For a subset of N ≥ 50 materials where both vortex invariants (Ψ, Platonic family from SQ-1/SQ-2) and band topological invariants (Z₂, Chern class from the Topological Materials Database) are available, compute the mutual information I(vortex invariant; band invariant).

2. If I ≈ H(vortex invariant) (where H is entropy), then vortex topology is reducible to band topology — it captures no new information. Still publishable as an alternative derivation.

3. If I << H(vortex invariant), then vortex topology captures orthogonal information. This is the "Keplerian signal" — structure in materials data that standard topology misses.

4. Identify specific materials where vortex and band predictions *disagree*. These are the most informative test cases: which framework matches experiment?

**Dependencies:** SQ-1, SQ-2, SQ-3 (need computed invariants and correlations).

**Success criteria:**
- Tier 1: Quantitative mutual information estimate establishing whether the frameworks are orthogonal or redundant.
- Tier 2: Identification of materials where vortex and band topology make contradictory predictions, with experimental adjudication.

---

## Priority Ranking

| Rank | Sub-question | Rationale | Dependencies | Timeline |
|------|-------------|-----------|--------------|----------|
| **1** | **SQ-1: Platonic Subgroup Mapping** | Foundation for everything. Pure mathematics, no data dependencies, guaranteed completable. Resolves the icosahedral exclusion problem which is central to the framework's coherence. | None | Weeks 1–6 |
| **2** | **SQ-2: Vortex Alignment Index Ψ** | The novel theoretical contribution. If Ψ can be constructed and formalized, it is a publishable result *on its own* as a topological invariant derivation. | SQ-1 | Weeks 4–10 |
| **3** | **SQ-4: Quasicrystal Anomaly** | Most falsifiable specific prediction. Smallest N but highest signal-to-noise if the effect exists. Can proceed in parallel with SQ-3. Independent of Ψ. Addresses the "special dodecahedron" claim directly. | SQ-1 only | Weeks 8–18 |
| **4** | **SQ-3: Statistical Correlation Study** | The bulk empirical validation. Largest dataset, most general claim. Depends on SQ-1 and SQ-2 being complete. | SQ-1, SQ-2 | Weeks 10–14 |
| **5** | **SQ-6: Vortex vs. Band Topology** | Meta-analysis that determines whether the vortex framework is *distinctive* or merely *alternative*. Highest conceptual value but requires all prior results. | SQ-1, SQ-2, SQ-3 | Weeks 15–20 |
| **6** | **SQ-5: Cross-Scale Self-Similarity** | Most speculative, smallest N, hardest to interpret. The Planck constraint on Poincaré dodecahedron is a known headwind. Valuable if positive, manageable if negative. | SQ-1 only | Weeks 18–22 |

**Execution strategy:** SQ-1 and SQ-2 are sequential (do SQ-1 first, then SQ-2). SQ-4 can begin as soon as SQ-1's icosahedral analysis is complete (week ~4). SQ-3 and SQ-5 can proceed once SQ-1 and SQ-2 deliver. SQ-6 is last but conceptually important for the discussion section.

---

## Risks

### Risk Matrix

| Risk | Severity | Probability | Impact on Project | Mitigation |
|------|----------|-------------|-------------------|------------|
| **R1: SQ-1 mapping is trivial.** The 230 → 5 Platonic family mapping may be already implicit in crystallography textbooks (point group → cubic vs. non-cubic is standard). The "mapping" may add nothing beyond known classifications. | Medium | **High** | Undermines novelty of SQ-2 through SQ-6. | *Embrace it:* If the mapping is trivial, publish the triviality explicitly. The value is in making the connection to vortex theory *explicit*, not in discovering new group theory. The real test is whether the vortex *interpretation* of known group theory generates new predictions (SQ-2 onward). |
| **R2: Ψ recapitulates Shubnikov groups.** The vortex alignment index may be mathematically equivalent to the known 1651 magnetic space group classification, providing no new information. | Low-Medium | **Medium-High** | Reduces SQ-2 from "new invariant" to "alternative derivation." Tier 3 outcome. | *Still publishable:* A topological derivation of magnetic space groups from vortex first principles is a contribution. Frame it as "we derive the necessity of magnetic ordering constraints from vortex topology." |
| **R3: No significant statistical correlations (SQ-3).** The data shows ρ < 0.15 for all property–Ψ correlations. Vortex topology has no detectable predictive power for bulk properties. | High | **Medium** | Project's central empirical claim fails. | *Null results are publishable:* Explicitly constraining where vortex topology could be relevant is valuable. Publish as "limits on the predictive power of topological vortex geometry for material properties." Adjust framework. |
| **R4: Quasicrystal anomaly is absent or opposite to prediction (SQ-4).** Icosahedral quasicrystals are well-described by DFT, or deviations exist but are in the wrong direction. | High | **Medium** | Falsifies the "special dodecahedron" claim — the most specific prediction of the framework. | *This is the most valuable negative result:* It directly falsifies a core claim. Publish as a falsification. If dodecahedron is NOT special, the framework needs fundamental revision or abandonment. |
| **R5: Cross-scale comparison is underpowered (SQ-5).** The nuclear Skyrmion dataset has N ~ 20 baryon numbers. The cosmic dataset has N = 1 universe. Statistical comparison across scales is meaningless with these sample sizes. | Medium | **High** | SQ-5 produces inconclusive results rather than positive or negative. | *Acknowledge limitation:* Report distributions qualitatively. Frame SQ-5 as a "pilot study" for cross-scale topology. The formal comparison methodology is the contribution, even if current data is insufficient. |
| **R6: Poincaré dodecahedron is definitively ruled out.** If Planck 2018 data (or future CMB experiments) conclusively exclude the Poincaré dodecahedral space, the cosmic scale of the "as above, so below" hypothesis loses its key prediction. | Medium | **Medium-High** | Weakens SQ-5; the cosmic anchor of the cross-scale comparison is removed. | *Cosmic topology is broader than dodecahedron:* Investigate whether OTHER Platonic cosmic topologies (cubic, toroidal) are viable. The "as above, so below" principle may hold with a different cosmic Platonic solid. |
| **R7: Publication bias / framework rejection.** Journals may reject papers assuming aether/superfluid vacuum as a premise, regardless of mathematical content. | High | **Medium** | Delays or prevents dissemination. | *Strategic framing:* Emphasize the mathematical/topological content (group theory, correlation study) over the interpretive framework. Submit to journals receptive to theoretical speculation (J. Math. Phys., Phys. Lett. A, Found. Phys.). Present results as "if one assumes vortex topology, here are the testable consequences" rather than "vortex topology is true." |
| **R8: Data quality and availability (SQ-3, SQ-4).** Materials Project experimental χ data may be sparse or inconsistent. Quasicrystal property measurements may have large error bars or limited compositions. | Medium | **Medium** | Reduces statistical power; weakens claims. | *Multiple databases:* Cross-validate Materials Project with AFLOW, OQMD, ICSD. For quasicrystals, perform manual literature curation. Report confidence intervals prominently. |

### Go/No-Go Decision Points

| Decision Point | Week | Criterion | Action if Fail |
|----------------|------|-----------|----------------|
| **DP-1:** SQ-1 mapping complete | 6 | All 230 space groups classified with no ambiguities > 5% | Resolve ambiguities before proceeding; if irresolvable, modify framework |
| **DP-2:** Ψ computation yields non-trivial distribution | 10 | Ψ takes ≥ 5 distinct values across 230 space groups (not binary) | If binary, Ψ is too coarse; refine definition or accept limited resolution |
| **DP-3:** Preliminary correlation check | 12 | |ρ| > 0.2 for Ψ vs. log\|χ\| on pilot dataset (N ≥ 100) | If |ρ| < 0.15, reassess whether data curation or Ψ definition is the bottleneck before full analysis |
| **DP-4:** Quasicrystal anomaly direction confirmed | 16 | Anomaly sign matches vortex prediction in ≥ 60% of samples | If sign is random or opposite, falsify "special dodecahedron" claim and refocus paper on SQ-1/SQ-2/SQ-3 |
| **DP-5:** Cross-scale comparison feasible | 20 | Nuclear and crystal distributions have ≥ 4 comparable Platonic categories | If categories are incomparable, redesign comparison metric or reduce SQ-5 to qualitative discussion |

---

*This decomposition yields six sub-questions with clear deliverables, dependencies, and falsification criteria. The project's strength is that every sub-question produces a publishable result — positive, negative, or null. The framework is treated as a hypothesis generator, not a truth claim.*