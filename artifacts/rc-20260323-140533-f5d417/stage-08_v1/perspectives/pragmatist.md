# Feasible Hypotheses for Aether Property Derivation and Testing

## Hypothesis 1: Fourth-Order Aether Wind Detection in LIGO Data

### Concrete, Testable Claim
A stationary aether produces measurable (v/c)⁴ fringe shifts in interferometer arms at Earth's orbital velocity (~30 km/s), predicted to yield ~10⁻¹⁸ strain modulation at Earth's orbital frequency (annual period). LIGO's ~10⁻²³ strain sensitivity is sufficient to detect this effect if it exists.

**Methodology:**
1. Extract 5+ years of continuous LIGO Hanford-Livingston correlated strain data (public GWOSC archive)
2. Construct matched filter for annual-period amplitude modulation with (v/c)⁴ scaling: expected signal ~ (3×10⁴/3×10⁸)⁴ ≈ 10⁻¹⁶ relative modulation
3. Perform coherent stacking across years to improve SNR
4. Compare detected (or upper limit) modulation to aether wind prediction vs. SR null prediction

### Why Achievable with Limited Compute
- **Data already exists**: GWOSC provides pre-processed strain data at 4096 Hz
- **Standard signal processing**: Matched filtering, FFT-based spectral analysis—well-established in GW community
- **No simulation required**: Pure data analysis on ~10 TB of existing data
- **Compute estimate**: Single GPU workstation, ~48-72 hours for full analysis pipeline

### Rationale Based on Proven Techniques
Stávek (2023) explicitly proposes this test. The (v/c)⁴ scaling is a standard prediction of stationary-aether interferometry—first-order (v/c) effects cancel in symmetric interferometers, second-order (v/c)² effects are the basis of MMX, but fourth-order effects remain detectable with sufficient sensitivity. LIGO is ~10¹⁰ times more sensitive than MMX apparatus.

### Measurable Prediction and Failure Condition

| Outcome | Interpretation |
|---------|----------------|
| **Positive**: Detect annual-modulated strain at (v/c)⁴ level, amplitude consistent with ~30 km/s aether wind | Evidence for preferred-frame physics; aether velocity measurable |
| **Negative**: Upper bound <10% of predicted signal | Stationary aether with Earth-relative velocity excluded; Earth-attached or superfluid aether models required |
| **Null with systematic**: Detection of modulation at wrong frequency/amplitude | Instrumental systematic; no aether inference possible |

### Resource Requirements
| Resource | Estimate |
|----------|----------|
| Compute | 1× GPU (RTX 4090 or equivalent), 72 hours |
| Storage | 2 TB for LIGO data download + intermediate products |
| Software | PyCBC or gwpy (standard GW libraries), custom filter code ~500 lines |
| Personnel | 1 researcher with GW data analysis experience |

---

## Hypothesis 2: Inverse Derivation of Aether Elasticity from EM Constants

### Concrete, Testable Claim
Given that ε₀ = 8.85×10⁻¹² F/m and μ₀ = 4π×10⁻⁷ H/m are precisely known, the superfluid vacuum framework (Ilie 2025) permits inversion to derive aether elastic modulus E_aether and density ρ_aether with discrete, testable values. These derived values should then predict Z₀ = 376.73 Ω independently and yield aether sound speed c_s = c.

**Methodology:**
1. Implement Ilie's elastic medium model: ε₀ = f₁(E, ρ, geometry), μ₀ = f₂(E, ρ, geometry)
2. Use constrained nonlinear optimization (scipy.optimize or JAX) to solve inverse problem:
   - Inputs: ε₀, μ₀, c (known to 10+ significant figures)
   - Unknowns: E_aether, ρ_aether, geometric factor
   - Constraints: c² = 1/(ε₀μ₀) = E/ρ (wave propagation in elastic medium)
3. Validate: Derived parameters must reproduce Z₀ = √(μ₀/ε₀) without being fit to it
4. Cross-check: Compare derived ρ_aether to cosmological vacuum energy density ρ_vac ≈ 10⁻²⁶ kg/m³

### Why Achievable with Limited Compute
- **Tiny parameter space**: 2-4 unknowns, well-constrained by 3 known constants
- **Deterministic optimization**: Gradient-based methods converge in seconds
- **No large simulation**: Analytic expressions from Ilie (2025) framework
- **Compute estimate**: Laptop-grade CPU, minutes per optimization run

### Rationale Based on Proven Techniques
The wave equation in elastic media is textbook physics: wave speed c = √(E/ρ) for a medium with elastic modulus E and density ρ. Electromagnetic wave propagation c = 1/√(ε₀μ₀) is mathematically identical to mechanical wave propagation. Ilie (2025) and Johansson (2020) both derive this correspondence—this hypothesis simply inverts it numerically.

### Measurable Prediction and Failure Condition

| Outcome | Interpretation |
|---------|----------------|
| **Positive**: Unique (E, ρ) solution found; Z₀ predicted correctly (±1%); ρ_aether ~10⁻²⁶ kg/m³ | Strong evidence for elastic aether; density connects to cosmology |
| **Negative**: No physically reasonable solution exists (negative density, E > Planck scale) | Elastic model insufficient; requires additional medium properties |
| **Degenerate**: Multiple solutions with vastly different (E, ρ) | Model underdetermined; needs additional constraint (e.g., viscosity) |

### Resource Requirements
| Resource | Estimate |
|----------|----------|
| Compute | Laptop CPU, <1 hour total |
| Software | Python + scipy/jax, ~200 lines |
| Data | CODATA values for ε₀, μ₀, c (public) |
| Personnel | 1 researcher with optimization background |

---

## Hypothesis 3: Einstein-Aether Parameter Constraints from Multi-Messenger Consistency

### Concrete, Testable Claim
Einstein-Aether theory introduces 4 dimensionless coupling constants (c₁, c₂, c₃, c₄) that modify gravitational propagation. If aether exists with physically meaningful properties, a single (c₁, c₂, c₃, c₄) parameter set must simultaneously satisfy: (1) GW170817 gravitational wave speed constraint |c_GW - c|/c < 10⁻¹⁵, (2) solar system post-Newtonian parameter bounds, and (3) cosmological expansion rate H₀. The hypothesis is that a non-trivial consistent region exists.

**Methodology:**
1. Compile published constraints on (c₁, c₂, c₃, c₄) from:
   - GW speed (GW170817 + EM counterpart): O(10⁻¹⁵) constraint
   - Binary pulsar orbital decay: PPN parameters
   - CMB and large-scale structure: H₀, σ₈
2. Implement MCMC sampler (emcee or similar) to map 4D allowed parameter region
3. Key test: Is allowed region just {c₁=c₂=c₃=c₄=0} (pure GR) or does non-zero aether solution exist?
4. If non-zero: Derive effective aether density ρ_eff = f(c₁, c₂, c₃, c₄) and compare to vacuum energy

### Why Achievable with Limited Compute
- **Likelihoods are cheap**: Each evaluation is analytic (no simulation)
- **MCMC is embarrassingly parallel**: 4D parameter space trivial for modern samplers
- **Constraints already published**: Lit review + numerical integration, not raw data analysis
- **Compute estimate**: 16-core workstation, ~12-24 hours for converged MCMC chains

### Rationale Based on Proven Techniques
Einstein-Aether theory is a well-studied modified gravity framework with 500+ papers. Parameter constraints via MCMC is standard practice in cosmology (Planck analysis, DESI analysis use identical methodology). The innovation here is explicitly testing for non-GR consistency rather than assuming GR is correct.

### Measurable Prediction and Failure Condition

| Outcome | Interpretation |
|---------|----------------|
| **Positive**: Non-zero (c₁, c₂, c₃, c₄) region exists with |c_i| > 0.01, all constraints satisfied | Aether modification viable; predicts deviations testable by LISA |
| **Negative**: Only c_i = 0 satisfies all constraints (within numerical precision) | Einstein-Aether excluded; return to GR or different aether model required |
| **Degenerate**: Large unbounded region | Current observations insufficient; need next-generation constraints |

### Resource Requirements
| Resource | Estimate |
|----------|----------|
| Compute | 16-core workstation, 24 hours |
| Software | Python + emcee + GetDist (standard cosmology tools) |
| Data | Published constraint values from literature (no raw data needed) |
| Personnel | 1 researcher with cosmology/MCMC experience |

---

## Summary Comparison

| Hypothesis | Primary Output | Compute Cost | Falsifiability | Connection to Aether Properties |
|------------|----------------|--------------|----------------|--------------------------------|
| H1: LIGO (v/c)⁴ | Aether wind velocity (or bound) | Medium (48-72 hr GPU) | Direct experimental test | Velocity → density via dynamics |
| H2: Inverse Elasticity | (E_aether, ρ_aether) values | Low (<1 hr CPU) | Cross-validation with Z₀ | Direct derivation of density, elasticity |
| H3: Einstein-Aether MCMC | Allowed (c₁, c₂, c₃, c₄) region | Medium (24 hr CPU) | Consistency test | Couplings → effective density |

**Recommendation**: Execute **H2 first** (lowest cost, clearest output), then **H3** (standard methodology, cosmological relevance), then **H1** (highest cost but direct experimental test). H2 and H3 together establish theoretical predictions that H1 could experimentally confirm.