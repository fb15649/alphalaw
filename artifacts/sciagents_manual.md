# SciAgents: Ручной проход по методологии

## Этап 1: Граф знаний

### Узлы (наши открытия)

```
[α-law]──────── E(n) = E₁ × n^α, 48 bonds, 100%
    ├── [α > 1] = molecule (synergy)
    ├── [α < 1] = crystal (diminishing returns)
    ├── [Empty Gap] [1.63, 1.97] — forbidden zone
    └── [π/σ ratio] r = 0.989 with α

[π-formulas]──── 8 EM constants through π
    ├── [m_p/m_e] = 6π⁵ (0.01 ppm)
    ├── [1/α] = π(4π²+π+1) (0.001 ppm)
    ├── [μ_p] = (8/9)π μ_N
    ├── [Δm] = (10/7)√π m_e
    ├── [m_d/m_p] = 2 − (17/9)π²α²
    ├── [μ_d] = 15/π^(5/2) μ_N
    ├── [R_p] = 4ƛ_C
    └── [g-2] = QED(our α) → 10 digits

[vortex model]── particles = vortices in superfluid ether
    ├── [electron] = 1 vortex ring
    ├── [proton] = 3 linked rings
    ├── [neutrino] = phonon (longitudinal wave)
    ├── [photon] = transverse wave
    ├── [3 generations] = 3 torus modes, Koide Q=2/3
    ├── [muon] = excited electron, m_μ/m_e ≈ 3/(2α)
    └── [pion] = vortex-antivortex pair

[ether properties]── medium parameters
    ├── [ρ] ≈ μ₀ = 1.26×10⁻⁶ (from impedance + independent vacuum analysis)
    ├── [G] = ρc² = 1/ε₀ = 1.13×10¹¹ Pa
    ├── [κ_GL] = 1/α = 137 (type-II SC)
    ├── [η] = 0 (superfluid)
    └── [K] → ∞ (incompressible)

[independent vacuum analysis]── macroscopic ether effects
    ├── [ρ_ether] = 10⁻⁶ kg/m³ (from Shapiro delay)
    ├── [β] = 2.1×10⁻⁴ (acoustoelastic coupling)
    ├── [σ_cav] = 4.2×10⁻⁵ N/m
    ├── [asymmetry] = 0.0032% (solar limb, testable)
    └── [Γ ∝ L^0.847] across 29 orders of magnitude
```

### Рёбра (связи между узлами)

```
[α-law] ←→ [π/σ ratio]: r = 0.989 (empirical)
[π/σ ratio] ←→ [vortex model]: π-bond = lateral flow, σ = axial
[1/α] ←→ [κ_GL]: κ = ƛ_e/r_e = 1/α (identity)
[ρ] ←→ [ρ_ether]: μ₀ ≈ 10⁻⁶ (independent estimates)
[G] ←→ [G_independent vacuum analysis]: 1/ε₀ = ρc² (exact)
[neutrino] ←→ [Δm² ratio]: π³ ≈ 31.0 (5% from exp)
[3 generations] ←→ [Koide]: Q = 2/3 (0.001%)
[electron] ←→ [London moment]: rotation → charge
[N_opt] ←→ [variational]: e³/8 ≈ 2.51 (NOT π)
```

## Этап 2: Поиск незамеченных связей

### Связь 1: α_scaling (0.847) ↔ α_bond (0.5-1.8)

independent vacuum analysis нашёл: Γ ∝ L^0.847 на 29 порядках масштаба.
alphalaw нашёл: E(n) = E₁ × n^α, где α варьируется.

**Вопрос:** α_bond для СРЕДНЕЙ связи ≈ 0.85?

Проверим: средний α по 48 bonds = ???

### Связь 2: Empty Gap [1.63, 1.97] ↔ κ_GL = 137

Gap в R₂ = E₂/E₁. Нижняя граница ≈ φ = 1.618.
κ = 1/α = 137. α = 1/κ.

**Вопрос:** есть ли связь между φ и α?
φ² = φ + 1 → φ = (1+√5)/2.
α ≈ φ²/π⁴ × (some integer)?

### Связь 3: σ_cav (macro) ↔ bond energy (micro)

independent vacuum analysis: σ_cav = 4.2×10⁻⁵ N/m (macroscopic surface tension).
alphalaw: E₁ (single bond energy) = 100-900 kJ/mol.

**Вопрос:** если σ scales as Γ ∝ L^0.847, what σ at atomic scale?

### Связь 4: N_opt = e³/8 ↔ Koide δ = 132.7°

N_opt = e³/8 = 2.511.
Koide δ = 2.317 rad.
δ/N_opt = 2.317/2.511 = 0.923 ≈ ???

### Связь 5: 3/(2α) ↔ 6π⁵

m_μ/m_e = 3/(2α) ≈ 206.
m_p/m_e = 6π⁵ ≈ 1836.
Ratio: 6π⁵/(3/(2α)) = 4π⁵α ≈ 8.90.
4π⁵α = 4 × 306.02 × 0.00730 = 8.935.
≈ 9? 3²? π²? Not clean.

## Этап 3: Гипотезы для проверки

### H1: Среднее α_bond ≈ α_scaling

Если средний α по всем 48 bonds ≈ 0.847, это связывает
материаловедение (Слой 1) с космологическим скейлингом (independent vacuum analysis).

### H2: Gap boundaries = function of κ_GL

Если φ и 2 (границы Gap) выводятся из κ = 137, это замыкает
связь между EM-константой и материаловедением.

### H3: σ_cav × (L_macro/L_micro)^0.847 ≈ bond energy

Если поверхностное натяжение масштабируется по тому же закону
что и циркуляция, то макро-σ из independent vacuum analysis предсказывает
микро-энергии связей из alphalaw.

## Этап 4: Проверка (выполняется в скрипте)

→ см. scripts/sciagents_hypotheses.py
