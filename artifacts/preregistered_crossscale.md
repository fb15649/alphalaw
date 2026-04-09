# Pre-Registered Protocol: Cross-Scale Alpha-Law Hypothesis Test

**Registration date: 2026-04-10**
**Status: PREDICTIONS LOCKED (data search NOT yet performed)**

---

## 1. Hypothesis

> The Reserve Law exponent alpha, defined by E(n) = E_1 * n^alpha, is a universal
> scaling constant determined by the presence or absence of "recruitable reserve"
> in the system. Specifically:
>
> - Systems WITH recruitable reserve exhibit alpha > 1 (superlinear scaling)
> - Systems WITHOUT recruitable reserve exhibit alpha < 1 (sublinear scaling)
> - The NUMERIC VALUE of alpha matches one of the known atomic bond exponents
>   within 10% tolerance

This protocol tests the hypothesis in **3 new domains** not previously examined,
with predictions specified BEFORE any data search.

---

## 2. Already Confirmed (Post-Hoc) -- Acknowledged Bias

In prior analysis (2026-04-09), we identified 12 cross-scale matches across
7 domains with corrected p = 0.0003:

| # | Domain       | System                  | alpha | Atom  | alpha_atom | Delta% |
|---|-------------|-------------------------|-------|-------|------------|--------|
| 1 | Neuroscience | Habituation             | 0.83  | C-C   | 0.80       | 3.7    |
| 2 | Neuroscience | LTP + dopamine          | 1.26  | P-P   | 1.28       | 1.6    |
| 3 | Networks     | Metcalfe (Facebook)     | 2.00  | N-N   | 2.01       | 0.5    |
| 4 | Cities       | Patents vs city size    | 1.27  | P-P   | 1.28       | 0.8    |
| 5 | Biology      | Kleiber's law           | 0.75  | C-C   | 0.77       | 2.6    |
| 6 | Pharmacology | Nicotinic receptor n_H  | 1.80  | N-N   | 1.83       | 1.6    |
| 7 | Pharmacology | mu-opioid receptor n_H  | 1.30  | P-P   | 1.28       | 1.6    |
| 8 | Learning     | Choice RT (Seibel)      | 0.48  | Si-Si | 0.48       | 0.0    |
| 9 | Learning     | Text editing (Card)     | 0.80  | C-C   | 0.80       | 0.0    |
| 10| Learning     | Mental arithmetic       | 0.65  | S-S   | 0.68       | 4.4    |
| 11| Economics    | Durable goods RTS       | 1.27  | P-P   | 1.28       | 0.8    |
| 12| Networks     | Telephone (historical)  | 0.50  | Si-Si | 0.48       | 4.2    |

**Reserve rule: 10/12 = 83% (100% for unambiguous cases)**

**Known limitation**: All 12 matches were found POST HOC. Selection bias is
present despite statistical correction. This protocol aims to provide genuinely
predictive evidence.

---

## 3. New Predictions (3 Domains Not Yet Searched)

### Reference: Known Atomic alpha Values

| Bond  | LP | alpha | Reserve? |
|-------|-----|-------|----------|
| C-C   | 0   | 0.770 | NO       |
| Si-Si | 0   | 0.485 | NO       |
| Ge-Ge | 0   | 0.407 | NO       |
| Sn-Sn | 0   | 0.330 | NO       |
| N-N   | 1   | 2.012 | YES      |
| P-P   | 1   | 1.283 | YES      |
| O-O   | 2   | 1.770 | YES      |
| S-S   | 2   | 0.676 | anomaly  |

---

### Domain A: Muscle Physiology -- Force-Frequency Relationship

**Background**: Skeletal muscle force scales as a power law with stimulation
frequency: F(f) ~ f^alpha. The exponent depends on the muscle's energy state.

**Reserve definition**: Glycogen stores and rested cross-bridge cycling capacity
constitute the muscle's "recruitable reserve." When glycogen is depleted or the
muscle is fatigued, reserve is absent.

**Predictions**:

| Condition                        | Reserve? | Predicted alpha | Matching atom | Tolerance |
|----------------------------------|----------|-----------------|---------------|-----------|
| Rested, glycogen-loaded muscle   | YES      | 1.28 +/- 0.13   | P-P (1.283)   | 10%       |
| Fatigued, glycogen-depleted      | NO       | 0.49 +/- 0.05   | Si-Si (0.485) | 10%       |

**Specific numeric criteria**:
- WITH reserve: alpha in [1.15, 1.41] AND alpha > 1.0
- WITHOUT reserve: alpha in [0.44, 0.54] AND alpha < 1.0

**Search protocol**:
- Database: PubMed, Google Scholar
- Keywords: "force-frequency relationship" AND ("power law" OR "exponent")
  AND ("muscle" OR "skeletal muscle")
- Also: "twitch potentiation" "fatigue" "force-frequency" "exponent"
- Accept: peer-reviewed studies reporting numeric exponents for F(f) fits
- Exclude: smooth muscle, cardiac muscle (different physiology)

---

### Domain B: Epidemiology -- Vaccine Dose-Response (Hill Coefficient)

**Background**: Vaccine dose-response curves are often modeled as
R(d) = R_max * d^n_H / (EC50^n_H + d^n_H), where n_H is the Hill coefficient.
The Hill coefficient captures cooperativity/steepness of the response.

**Reserve definition**: An adjuvant (e.g., alum, MF59) acts as an "immune
amplifier" -- it does not directly produce immunity but recruits and potentiates
the immune response. This is analogous to lone pairs that don't form sigma bonds
but can be recruited into pi bonds.

**Predictions**:

| Condition                     | Reserve? | Predicted n_H | Matching atom    | Tolerance |
|-------------------------------|----------|---------------|------------------|-----------|
| Vaccine WITH adjuvant         | YES      | 1.50 +/- 0.15 | N-N/O-O midpoint | 10%       |
| Vaccine WITHOUT adjuvant      | NO       | 0.77 +/- 0.08 | C-C (0.770)      | 10%       |

**Specific numeric criteria**:
- WITH adjuvant: n_H in [1.35, 1.65] AND n_H > 1.0
- WITHOUT adjuvant: n_H in [0.69, 0.85] AND n_H < 1.0

**Note**: The "with reserve" prediction (1.50) falls between P-P (1.283) and
O-O (1.770). We choose the midpoint because adjuvants vary in potency.
If the actual value matches P-P or O-O individually within 10%, that also counts.

**Search protocol**:
- Database: PubMed
- Keywords: "dose-response" AND "vaccine" AND ("Hill coefficient" OR "Hill slope"
  OR "n_H" OR "cooperativity")
- Also: "adjuvant" "alum" "dose-response curve" "sigmoid" "EC50"
- Accept: clinical or preclinical studies reporting Hill coefficients for
  dose-antibody titer relationships
- Exclude: therapeutic drug dose-response (already covered in pharmacology domain)

---

### Domain C: Materials Fatigue -- Coffin-Manson Exponent

**Background**: The Coffin-Manson relation describes low-cycle fatigue:
Delta_epsilon_p / 2 = epsilon_f' * (2N_f)^c, where c is the fatigue ductility
exponent. Typical values: c in [-0.5, -0.7] for common metals.

**Reserve definition**: Residual compressive stress introduced by shot peening or
surface hardening acts as a "reserve" -- it is not part of the load-bearing
structure but is recruited under tensile loading to oppose crack propagation.
This is analogous to lone pairs recruited into pi bonds.

We predict |c| (absolute value) since the sign convention is reversed in fatigue
(negative exponents indicate degradation, but the magnitude follows alpha-law scaling).

**Predictions**:

| Condition                             | Reserve? | Predicted |c| | Matching atom | Tolerance |
|---------------------------------------|----------|-------------|---------------|-----------|
| Shot-peened / compressive residual     | NO*      | 0.77 +/- 0.08 | C-C (0.770)  | 10%       |
| Untreated (no residual stress)         | NO       | 0.49 +/- 0.05 | Si-Si (0.485) | 10%       |

*Important nuance: Shot peening introduces compressive reserve, but in fatigue
the exponent c describes the DEGRADATION process. The reserve SLOWS degradation,
making |c| LARGER (closer to 1, but still < 1). Both conditions have alpha < 1
because fatigue is inherently a loss process (no true "recruitable reserve" in
the alpha > 1 sense -- the reserve merely reduces the rate of loss).

**Specific numeric criteria**:
- WITH treatment: |c| in [0.69, 0.85] AND |c| < 1.0
- WITHOUT treatment: |c| in [0.44, 0.54] AND |c| < 1.0
- Both must satisfy alpha < 1 (reserve rule: fatigue = degradation, no true
  superlinear reserve)

**Search protocol**:
- Database: ASM Handbook Vol. 19 (Fatigue and Fracture), Google Scholar
- Keywords: "Coffin-Manson" AND ("fatigue ductility exponent" OR "exponent c")
  AND ("shot peening" OR "residual stress" OR "surface treatment")
- Also: "low-cycle fatigue" "exponent" "power law"
- Accept: experimental studies reporting c values for treated vs. untreated metals
- Exclude: high-cycle fatigue (different mechanism, Basquin equation)

---

## 4. Analysis Protocol

### 4.1 Matching Criteria

**Numeric match**: The measured exponent falls within 10% of the predicted
value. This tolerance is wider than the post-hoc 5% because:
- Predictions are made before data search (no tuning)
- Domain-specific noise may be higher than in atomic data
- 10% still represents a specific, falsifiable prediction

**Reserve rule match**: The sign of (alpha - 1) must match the prediction:
- Reserve present AND alpha > 1 (or |c| closer to 1 for fatigue)
- Reserve absent AND alpha < 1

**Full match** = numeric match AND reserve rule match.

### 4.2 Monte Carlo Null Distribution

For each domain, generate 100,000 simulated "random" exponents:

- Domain A (Muscle): Uniform draw from [0.2, 2.5]
  (physiologically plausible range for force-frequency exponents)
- Domain B (Vaccines): Uniform draw from [0.3, 3.0]
  (Hill coefficient range for biological dose-response)
- Domain C (Fatigue): Uniform draw from [0.3, 0.9]
  (literature range for Coffin-Manson c values)

For each simulation:
1. Draw one value per condition (2 per domain, 6 total)
2. Check if each falls within 10% of predicted atomic alpha
3. Check if reserve rule is satisfied
4. Count domains with full match (both conditions correct)

Report: P(>= k domains match | H_0) for k = 0, 1, 2, 3.

### 4.3 Success and Failure Criteria

| Outcome           | Domains with full match | Interpretation                        |
|-------------------|------------------------|---------------------------------------|
| **Strong support**    | 3 out of 3             | Hypothesis strongly supported         |
| **Support**           | 2 out of 3             | Hypothesis supported (minimum bar)    |
| **Not supported**     | 1 out of 3             | Insufficient evidence                 |
| **Refuted**           | 0 out of 3             | Hypothesis not supported              |

**Pre-committed decision rule**: >= 2 out of 3 domains showing full match
constitutes support for the hypothesis. This threshold was chosen before data search.

### 4.4 Partial Match Rules

If a domain shows:
- Numeric match but NOT reserve rule: scored as "partial, mechanism unclear"
- Reserve rule match but NOT numeric: scored as "directionally correct, not quantitative"
- Neither: scored as "no match"

Partial matches are reported but do NOT count toward the success criterion.

---

## 5. Timeline

| Step | Date | Description |
|------|------|-------------|
| Predictions registered | 2026-04-10 | This document (locked, no modifications after this date) |
| Data search | 2026-04-10 to 2026-04-17 | Literature search in 3 domains |
| Analysis | 2026-04-17 to 2026-04-20 | Monte Carlo, comparison, scoring |
| Results | 2026-04-20 | Published in artifacts/crossscale_results.md |

**Integrity rule**: This document MUST NOT be modified after the registration date.
Any deviations from the protocol (e.g., changed tolerance, added domains) must be
documented and justified in the results file, NOT retroactively edited here.

---

## 6. Limitations

1. **Small sample (N=3 domains)**: Only 3 new domains are tested. Even with
   perfect results, statistical power is limited. This is a pilot pre-registration,
   not a definitive test.

2. **Estimated ranges**: The predicted values (1.28, 0.49, 1.50, 0.77, etc.)
   are matched to atomic alpha values by analogy, not derived from first-principles
   calculations or meta-analyses of each domain. The 10% tolerance partially
   compensates, but the predictions remain heuristic.

3. **Qualitative "reserve" definition**: In atomic bonds, "reserve" = lone pair
   electrons (quantitative, countable). In new domains, "reserve" is defined
   qualitatively:
   - Muscle: glycogen stores (measurable but continuous, not discrete)
   - Vaccines: adjuvant presence (binary, but adjuvant potency varies)
   - Fatigue: residual compressive stress (measurable in MPa, but the threshold
     for "having reserve" is not defined)

4. **Publication bias in source data**: The literature exponents we will find
   may themselves be subject to publication bias (rounding, selective reporting).
   We mitigate by preferring meta-analyses and large datasets over single studies.

5. **Mapping ambiguity**: When multiple atomic alpha values exist in a range,
   choosing which atom to match is partly subjective. We pre-commit the mapping
   above to prevent post-hoc selection. If the measured value matches a DIFFERENT
   atom within 10%, this is noted but scored as a partial match only if the
   reserve rule also holds.

6. **Coffin-Manson sign convention**: Using |c| instead of c introduces an
   interpretation layer. We justify this in section 3C, but it could be seen
   as an additional degree of freedom.

---

## 7. Summary of All Pre-Registered Predictions

| # | Domain   | Condition          | Reserve | Predicted alpha | Atom   | Window [low, high] |
|---|----------|--------------------|---------|-----------------|--------|-------------------|
| 1 | Muscle   | Rested, glycogen+  | YES     | 1.28            | P-P    | [1.15, 1.41]      |
| 2 | Muscle   | Fatigued, depleted | NO      | 0.49            | Si-Si  | [0.44, 0.54]      |
| 3 | Vaccine  | With adjuvant      | YES     | 1.50            | N-N/O-O| [1.35, 1.65]      |
| 4 | Vaccine  | Without adjuvant   | NO      | 0.77            | C-C    | [0.69, 0.85]      |
| 5 | Fatigue  | Shot-peened        | PARTIAL | 0.77            | C-C    | [0.69, 0.85]      |
| 6 | Fatigue  | Untreated          | NO      | 0.49            | Si-Si  | [0.44, 0.54]      |

**Total: 6 numeric predictions, 3 reserve-rule predictions, across 3 domains.**

---

*This document constitutes a pre-registration of predictions. It is timestamped
by git commit and must not be modified after the registration date.*

---

## 8. RESULTS (2026-04-10)

### Domain A: Muscle — INCONCLUSIVE
Literature uses sigmoidal (Hill) fits, NOT power law. No published α values for
direct comparison. Qualitative direction correct (rested > fatigued steepness).
Cannot confirm or refute numeric predictions.

### Domain B: Vaccine — INCONCLUSIVE
Hill coefficients for vaccine dose-response not published as standard practice
(too few dose points in trials). Indirect estimates: without adjuvant ~0.5-0.8,
with adjuvant ~1.0-1.5. Direction consistent. Quantitative verification impossible.

### Domain C: Fatigue — PARTIAL FAIL
- **Untreated |c| ≈ 0.49**: **CONFIRMED** (SAE 1015 steel: 0.47-0.51, within prediction window [0.44, 0.54])
- **Shot-peened |c| ≈ 0.77**: **NOT CONFIRMED**. Literature shows |c| does NOT change with shot peening in LCF regime. Residual compressive stresses relax under cyclic plastic straining. The "reserve = compressive stress" analogy is physically incorrect for this parameter.

### Overall Verdict: **CRITERION NOT MET**
- Required: ≥2/3 domains match
- Achieved: 0 full matches, 2 inconclusive, 1 partial fail
- **Pre-registered test did NOT confirm the cross-scale hypothesis.**

### Lessons Learned
1. **Domain selection was poor**: chose fields where power-law is NOT the standard fitting model
2. **"Reserve" analogy for fatigue was physically wrong**: compressive residual stress relaxes under plastic cycling → not a true "recruitable reserve"
3. **Better domains for future test**: should choose fields where power-law exponents ARE routinely published (e.g., rheology: shear-thinning η~γ̇^(n-1); population ecology: N~t^r; turbulence: E~k^(-5/3) variants)
