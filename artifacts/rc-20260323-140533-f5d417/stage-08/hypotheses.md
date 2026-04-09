# Final Research Proposal: Decisive Aether Hypotheses

## Synthesis Rationale

After weighing all perspectives, I reject the "complementary frameworks" narrative. The contrarian correctly identifies that viscosity contradictions between superfluid (η = 0) and Einstein-Aether (η ≠ 0) frameworks are **mutually exclusive physical claims**, not parametric variations. Rather than flattening this conflict, we exploit it: any experiment constraining aether viscosity eliminates at least one major framework regardless of outcome.

The strongest hypotheses are those that:
1. Make **genuinely novel predictions** absent from standard GR/QFT
2. Directly probe the **framework exclusivity problem**
3. Use **existing data** with feasible computation

---

## Hypothesis 1: **Gravitational Wave Frequency-Dependent Arrival Dispersion**

### Rationale
This hypothesis exploits the viscosity contradiction directly. Superfluid vacuum demands η = 0 (no dispersion); Einstein-Aether permits η ≠ 0 (dispersion proportional to f²). Standard GR predicts no dispersion. A single LIGO analysis eliminates at least two of these three possibilities.

The innovator's seismic analogy is sound: viscoelastic media universally exhibit frequency-dependent phase velocity. If spacetime has shear structure, this signature should appear.

### Measurable Prediction
For aether viscosity η_aether ≈ 10⁻³⁶ Pa·s:

**Arrival time delay between frequency components:**
$$\Delta t_{arrival} = \frac{\eta_{aether} \cdot L \cdot \omega^2}{2\rho_{aether} \cdot c^4}$$

**Specific prediction:** For GW150914 (L = 410 Mpc, f_peak = 250 Hz), high-frequency components arrive **0.1-1 ms later** than low-frequency components, producing chirp smearing visible in time-frequency decomposition.

**Analysis pipeline:**
1. Download LIGO strain data for 10+ BBH mergers from GWOSC
2. Apply continuous wavelet transform (CWT) to extract time-frequency structure
3. Measure arrival time vs. frequency for peak amplitude across 50-500 Hz band
4. Fit: t(f) = t₀ + β·f²

### Failure Condition
|β| < 10⁻⁸ s/Hz² at 3σ confidence → **Viscous aether rejected; aether either superfluid (η = 0) or nonexistent**

This bound corresponds to η < 10⁻⁴⁰ Pa·s—effectively proving superfluid behavior if satisfied.

### Feasibility Notes
- Computation: ~15 minutes on single GPU for 10 events
- Data: Public LIGO HDF5 files (~1GB)
- Systematic risk: LIGO calibration drift could mimic dispersion; mitigated by analyzing multiple events with different sky locations

---

## Hypothesis 2: **Cross-Framework Impedance Equivalence Test**

### Rationale
The contrarian's fragmentation hypothesis claims Einstein-Aether and superfluid vacuum are mathematically incompatible. This hypothesis directly tests that claim by attempting to map parameters between frameworks.

If successful (impedances match), frameworks describe the same physics in different coordinates. If unsuccessful (no consistent mapping exists), the contrarian is correct: "aether" is a homonym covering incompatible theories.

### Measurable Prediction
**Einstein-Aether impedance:**
$$Z_{EA} = \frac{c_\sigma^2}{8\pi G \cdot c^2}$$
where c_σ is the shear coupling constant

**Superfluid vacuum impedance:**
$$Z_{SV} = \rho_{sv} \cdot c \cdot \xi$$
where ξ is coherence length, ρ_sv is condensate density

**Prediction:** If frameworks are equivalent, Z_EA ≈ Z_SV within factor of 2 when both are constrained by identical cosmological parameters (H₀, Ω_Λ, σ₈).

### Failure Condition
|Z_EA - Z_SV| / Z_EA > 10 (order-of-magnitude mismatch) → **Framework unification falsified; Einstein-Aether and superfluid vacuum describe different physics**

### Feasibility Notes
- Computation: Algebraic manipulation + parameter grid search (~8 hours on workstation)
- Leverage existing CLASS/Boltzmann solver modules for Einstein-Aether cosmology
- No numerical relativity required for homogeneous case

---

## Hypothesis 3: **Fourth-Order Anisotropy in LIGO Baseline**

### Rationale
This addresses the contrarian's core challenge: *Does any aether framework predict something standard physics cannot explain?*

Second-order Michelson-Morley experiments are saturated at null. But fourth-order (v/c)⁴ effects are unexplored at LIGO sensitivity. A stationary aether predicts periodic strain anisotropy modulated by Earth's orbital velocity—absent in standard physics with no free parameters to hide it.

### Measurable Prediction
**Fourth-order fringe shift:**
$$\frac{\Delta L}{L} = \left(\frac{v}{c}\right)^4 \cdot \sin^2(2\theta) \cdot \cos(\omega_{orbital} t)$$

For LIGO (L = 4km, λ = 1064nm, v_orbital = 30 km/s):
- Predicted effect: ~10⁻¹⁶ strain level
- LIGO sensitivity: ~10⁻²³ strain

**The signal should be 10⁷ times above noise floor**, modulated at Earth's orbital frequency (annual) and sidereal frequency (daily).

### Failure Condition
No periodic anisotropy correlating with orbital velocity above 10⁻¹⁸ strain → **Stationary aether rejected; any existing aether must be locally comoving (Earth-attached) or Lorentz-symmetric**

### Feasibility Notes
- Computation: FFT + demodulation analysis (<48 hours on single GPU)
- Data: 6+ months of LIGO strain data (~500GB)
- Key systematic: Must distinguish from terrestrial seasonal effects (temperature, seismicity); use null-test with detector orientation rotation

---

## Unresolved Disagreements (Preserved)

| Disagreement | Implications |
|--------------|--------------|
| **Viscosity: η = 0 vs. η ≠ 0** | Hypothesis 1 directly resolves this. Until tested, superfluid and Einstein-Aether frameworks make contradictory claims about physical reality. |
| **Circular derivation problem** | The contrarian's challenge stands unanswered: no aether framework derives density without embedding c a priori. Hypothesis 2's impedance mapping may reveal whether parameters are independent or constrained. |
| **Preferred frame detectability** | Lorentz ether says undetectable; Einstein-Aether says detectable. Hypothesis 3 tests this directly—null result supports either Lorentz ether or no aether. |
| **Novel prediction burden** | The contrarian's standard is correct: reproducing SR/GR results proves nothing. Only Hypotheses 1 and 3 attempt genuinely novel predictions; failure of both would severely weaken the aether program. |

---

## Priority Ranking

| Rank | Hypothesis | What It Resolves | Risk |
|------|------------|------------------|------|
| **1** | GW Dispersion | Viscosity contradiction; eliminates ≥1 framework | Medium (LIGO systematics) |
| **2** | Fourth-Order Anisotropy | Preferred frame existence; addresses "novel prediction" challenge | Medium (seasonal systematics) |
| **3** | Cross-Framework Equivalence | Mathematical unification possibility; tests fragmentation hypothesis | Low (theoretical consistency check) |

**Execute in parallel.** Hypotheses 1 and 3 use the same LIGO data with different analysis pipelines. Hypothesis 2 is independent and can proceed simultaneously. Total timeline: 4-6 weeks to completion.

---

## Decisive Outcomes

- **If H1 succeeds + H3 succeeds**: Aether has viscosity (Einstein-Aether valid) AND preferred frame exists → revolutionary
- **If H1 fails + H3 fails**: Aether either superfluid + Lorentz-symmetric, or doesn't exist → aether program severely constrained
- **If H1 succeeds + H3 fails**: Viscous aether but no preferred frame → supports emergent/bounded aether models
- **If H2 fails**: Frameworks are mutually exclusive → field must choose one; "convergence" narrative abandoned

The contrarian's fragmentation hypothesis is correct until H2 succeeds. The innovator's optimism is warranted only if H1 or H3 succeeds. The pragmatist's feasibility constraints are satisfied in all cases.