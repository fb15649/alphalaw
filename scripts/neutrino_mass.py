"""
#1: NEUTRINO MASS from vortex model.

What we know:
- Electron = 1 vortex, charge -e, spin ½, N_e ≈ 4255
- Proton = 3 vortices, charge +e, spin ½
- Neutrino = ??? vortex, charge 0, spin ½

Key question: what makes neutrino DIFFERENT from electron?
Both are spin-½ fermions. But neutrino has NO CHARGE.

In vortex model: charge = circulation direction.
No charge = no NET circulation? Or: two opposite circulations cancel?

Approach: use our formulas + what's measured about neutrinos.
"""
import math

pi = math.pi
alpha = 1 / 137.035999166
c = 2.998e8
h = 6.626e-34
hbar = h / (2*pi)
mu_0 = 4e-7 * pi
rho = mu_0
m_e = 9.109e-31
eV = 1.602e-19  # 1 eV in Joules

print("=" * 80)
print("  #1: МАССА НЕЙТРИНО ИЗ ВИХРЕВОЙ МОДЕЛИ")
print("=" * 80)


# ============================================================
# What's measured
# ============================================================
print("""
------------------------------------------------------------------------
  ЧТО ИЗМЕРЕНО
------------------------------------------------------------------------

  Нейтрино ИМЕЕТ массу (осцилляции):
    Δm²₂₁ = 7.53 × 10⁻⁵ эВ²    (солнечные)
    |Δm²₃₂| = 2.453 × 10⁻³ эВ² (атмосферные)

  → m₂ ≥ √(Δm²₂₁) ≈ 0.0087 эВ
  → m₃ ≥ √(|Δm²₃₂|) ≈ 0.050 эВ

  Верхняя граница (прямое измерение):
    m(ν_e) < 0.8 эВ              (KATRIN 2022)
    m(ν_e) < 0.45 эВ             (KATRIN 2024, предварительно)

  Космологическая граница:
    Σm_ν < 0.12 эВ               (Planck 2018)
    → m_i < 0.04 эВ (если все 3 ≈ равны)

  ДИАПАЗОН: 0.009 эВ < m₂ < 0.04 эВ
            0.05 эВ < m₃ < 0.04-0.12 эВ (зависит от иерархии)
""")

dm21_sq = 7.53e-5  # eV²
dm32_sq = 2.453e-3  # eV²
m2_min = math.sqrt(dm21_sq)
m3_min = math.sqrt(dm32_sq)

print(f"  m₂ ≥ {m2_min*1000:.1f} мэВ")
print(f"  m₃ ≥ {m3_min*1000:.1f} мэВ")


# ============================================================
# Approach 1: Neutrino = simplest vortex (N = 1)
# ============================================================
print("""
------------------------------------------------------------------------
  ПОДХОД 1: Нейтрино = простейший вихрь (N = 1)
------------------------------------------------------------------------
""")

# m = [π²ρNℏ³/c²]^(1/4)
# At N = 1:
m_N1 = (pi**2 * rho * 1 * hbar**3 / c**2)**(0.25)
m_N1_eV = m_N1 * c**2 / eV

print(f"  m(N=1) = [π²ρℏ³/c²]^(1/4) = {m_N1:.3e} кг = {m_N1_eV:.4f} эВ")
print(f"  = {m_N1_eV*1000:.2f} мэВ")

# Compare
print(f"\n  Сравнение:")
print(f"    m(N=1) = {m_N1_eV*1000:.1f} мэВ")
print(f"    m₂(exp) ≥ {m2_min*1000:.1f} мэВ")
print(f"    m₃(exp) ≥ {m3_min*1000:.1f} мэВ")
print(f"    Σm < 120 мэВ (космология)")

# N=1 gives ~ 63 keV — WAY too heavy!
if m_N1_eV > 1:
    print(f"\n    N=1: {m_N1_eV:.0f} эВ — СЛИШКОМ ТЯЖЁЛ (> KATRIN limit)")


# ============================================================
# Approach 2: Find N that gives neutrino mass
# ============================================================
print("""
------------------------------------------------------------------------
  ПОДХОД 2: Какое N даёт m_ν ≈ 0.05 эВ?
------------------------------------------------------------------------
""")

# m = [π²ρNℏ³/c²]^(1/4)
# m⁴ = π²ρNℏ³/c²
# N = m⁴c²/(π²ρℏ³)

for m_target_eV in [0.01, 0.05, 0.1, 0.5, 0.8]:
    m_target = m_target_eV * eV / c**2
    N_target = m_target**4 * c**2 / (pi**2 * rho * hbar**3)
    print(f"  m = {m_target_eV:.2f} эВ → N = {N_target:.3e}")

# N ~ 10⁻²⁵ for neutrinos — absurdly small!
print(f"\n  N << 1 для всех нейтринных масс!")
print(f"  N < 1 означает r > R (трубка больше кольца)")
print(f"  = сферический вихрь (Hill), не тороид")


# ============================================================
# Approach 3: Neutrino = UNCHARGED vortex
# ============================================================
print("""
------------------------------------------------------------------------
  ПОДХОД 3: Нейтрино = незаряженный вихрь
------------------------------------------------------------------------

  В модели: заряд = направление циркуляции.
  Нет заряда → нет НЕТТО-циркуляции.

  Два варианта:
  A) Нейтрино = вихрь + антивихрь (пара, Γ_net = 0)
  B) Нейтрино = вихрь БЕЗ циркуляции (Hill's vortex без Γ?)

  Вариант A: пара вихрь-антивихрь
  Масса = 2 × m_single − E_binding
  Если E_binding ≈ 2 × m_single − m_ν:
  → m_ν << m_e → пара ПОЧТИ аннигилирует, остаётся крошечная масса
""")

# Approach A: neutrino = e + e̅ almost annihilated
# m_ν = 2m_e × (1 - f) where f ≈ 1 − m_ν/(2m_e)
# What is f?
f_binding = 1 - 0.05 * eV / (2 * m_e * c**2)
print(f"  Если ν = e⁺e⁻ связанная:")
print(f"  f = 1 − m_ν/(2m_e) = {f_binding:.15f}")
print(f"  → 99.99999...% энергии уничтожено")
print(f"  → физически невероятно (нужна точность {(2*m_e*c**2/eV)/0.05:.0e})")


# ============================================================
# Approach 4: Neutrino from π-formula
# ============================================================
print("""
------------------------------------------------------------------------
  ПОДХОД 4: m_ν из π-формулы (как m_p/m_e = 6π⁵)
------------------------------------------------------------------------

  У нас: m_p/m_e = 6π⁵ (протон/электрон).
  Есть ли π-формула для m_ν/m_e?
""")

# m_ν/m_e = ???
# m₃ ≈ 0.05 eV, m_e = 511000 eV
# m₃/m_e ≈ 0.05/511000 ≈ 9.8×10⁻⁸

ratio_nu_e = 0.05 / 511000
print(f"  m₃/m_e ≈ {ratio_nu_e:.2e}")
print(f"  1/(m_e/m₃) = 1/{1/ratio_nu_e:.0f}")

# Search: m_e/m_ν = a × π^n ?
target = 1/ratio_nu_e  # ≈ 1.02×10⁷
print(f"\n  Ищу π-формулу для m_e/m_ν ≈ {target:.2e}:")

best_err = 999
best = ""
for a in range(1, 30):
    for b in range(1, 20):
        for n_num in range(1, 20):
            for n_den in range(1, 4):
                n = n_num / n_den
                val = (a/b) * pi**n
                if val <= 0:
                    continue
                err = abs(val - target) / target * 100
                if err < best_err:
                    best_err = err
                    if b == 1 and n_den == 1:
                        best = f"{a}×π^{n_num}"
                    else:
                        best = f"({a}/{b})×π^({n_num}/{n_den})"

print(f"  Лучшая: m_e/m_ν ≈ {best} (err {best_err:.2f}%)")

# Also check: m_e/m_ν = (m_p/m_e)^k × something?
# m_p/m_e ≈ 6π⁵ ≈ 1836
# (m_p/m_e)² ≈ 3.37×10⁶
# (m_p/m_e)² × 3 ≈ 10⁷ ← close to m_e/m_ν!
ratio2 = (6*pi**5)**2 * 3
print(f"\n  3 × (6π⁵)² = {ratio2:.2e}")
print(f"  m_e/m_ν = {target:.2e}")
print(f"  Ratio = {ratio2/target:.3f}")
# Not great.

# What about: m_e/m_ν = 6π⁵ / α ?
ratio3 = 6*pi**5 / alpha
print(f"\n  6π⁵/α = {ratio3:.2e}")
print(f"  m_e/m_ν = {target:.2e}")
print(f"  Ratio = {ratio3/target:.3f}")

# Or: m_e/m_ν = (6π⁵)² / (4π³+π²+π)?
ratio4 = (6*pi**5)**2 / (4*pi**3 + pi**2 + pi)
print(f"\n  (6π⁵)²/(4π³+π²+π) = {ratio4:.2e}")
print(f"  m_e/m_ν = {target:.2e}")
print(f"  Ratio = {ratio4/target:.3f}")

# Hmm: (m_p/m_e)² / (1/α) = (6π⁵)² × α
ratio5 = (6*pi**5)**2 * alpha
print(f"\n  (6π⁵)²×α = {ratio5:.2e}")
print(f"  m_e/m_ν = {target:.2e}")
print(f"  Ratio = {ratio5/target:.3f}")

# BINGO? (6π⁵)²×α ≈ 2.46×10⁷, target ≈ 1.02×10⁷
# Ratio 2.4 — not great, but order of magnitude.

# What if m_ν = m_e × α / (6π⁵)?
m_nu_pred = m_e * alpha / (6*pi**5)
m_nu_pred_eV = m_nu_pred * c**2 / eV
print(f"\n  Формула: m_ν = m_e × α/(6π⁵)")
print(f"  = {m_nu_pred_eV:.4f} эВ = {m_nu_pred_eV*1000:.2f} мэВ")
print(f"  Эксперимент: m₃ > 50 мэВ")

# m_e × α²:
m_nu2 = m_e * alpha**2
m_nu2_eV = m_nu2 * c**2 / eV
print(f"\n  m_ν = m_e × α² = {m_nu2_eV:.4f} эВ = {m_nu2_eV*1000:.2f} мэВ")

# m_e × α² = 0.0272 eV ≈ 27 meV
# m₃ > 50 meV → close but too small
# m₂ > 8.7 meV → could be m₂?

# m_e × α² × π:
m_nu3 = m_e * alpha**2 * pi
m_nu3_eV = m_nu3 * c**2 / eV
print(f"  m_ν = m_e × α²π = {m_nu3_eV:.4f} эВ = {m_nu3_eV*1000:.2f} мэВ")

# m_e × α² × π ≈ 85 meV — in the range!
print(f"\n  m₃ > 50 мэВ, Σm < 120 мэВ")
print(f"  m_e × α²π = {m_nu3_eV*1000:.1f} мэВ — В ДИАПАЗОНЕ!")

# Three generations: maybe m_1, m_2, m_3 = m_e × α² × (1, π^(1/3), π^(2/3))?
print(f"\n  Три поколения:")
for k, name in [(0, "ν₁"), (1, "ν₂"), (2, "ν₃")]:
    m_k = m_e * alpha**2 * pi**(k/2)
    m_k_eV = m_k * c**2 / eV
    print(f"    {name}: m_e×α²×π^({k}/2) = {m_k_eV*1000:.2f} мэВ")

# Check Δm² ratios
m1 = m_e * alpha**2
m2 = m_e * alpha**2 * pi**(1/2)
m3 = m_e * alpha**2 * pi
m1_eV = m1 * c**2 / eV
m2_eV = m2 * c**2 / eV
m3_eV = m3 * c**2 / eV

dm21_pred = m2_eV**2 - m1_eV**2
dm32_pred = m3_eV**2 - m2_eV**2

print(f"\n  Δm²₂₁ (предсказание) = {dm21_pred:.4e} эВ²")
print(f"  Δm²₂₁ (эксперимент)  = {dm21_sq:.4e} эВ²")
print(f"  Ratio = {dm21_pred/dm21_sq:.2f}")

print(f"\n  Δm²₃₂ (предсказание) = {dm32_pred:.4e} эВ²")
print(f"  Δm²₃₂ (эксперимент)  = {dm32_sq:.4e} эВ²")
print(f"  Ratio = {dm32_pred/dm32_sq:.2f}")

# The RATIO of Δm²:
print(f"\n  Δm²₃₂/Δm²₂₁ (предсказание) = {dm32_pred/dm21_pred:.1f}")
print(f"  Δm²₃₂/Δm²₂₁ (эксперимент)  = {dm32_sq/dm21_sq:.1f}")


# ============================================================
# SUMMARY
# ============================================================
print(f"""
========================================================================
  ИТОГИ: МАССА НЕЙТРИНО
========================================================================

  Лучшая формула: m_νᵢ = m_e × α² × π^(i/2), i = 0,1,2

  Предсказания:
    m₁ = m_e × α² = {m1_eV*1000:.1f} мэВ
    m₂ = m_e × α²√π = {m2_eV*1000:.1f} мэВ
    m₃ = m_e × α²π = {m3_eV*1000:.1f} мэВ
    Σm = {(m1_eV+m2_eV+m3_eV)*1000:.0f} мэВ

  Сравнение:
    m₃ > 50 мэВ (осцилляции)     → наше {m3_eV*1000:.0f} мэВ {'✓' if m3_eV*1000 > 50 else '✗'}
    m₂ > 8.7 мэВ (осцилляции)    → наше {m2_eV*1000:.0f} мэВ {'✓' if m2_eV*1000 > 8.7 else '✗'}
    Σm < 120 мэВ (космология)     → наше {(m1_eV+m2_eV+m3_eV)*1000:.0f} мэВ {'✓' if (m1_eV+m2_eV+m3_eV)*1000 < 120 else '✗'}
    m < 800 мэВ (KATRIN)          → наше {m3_eV*1000:.0f} мэВ ✓

  Отношение Δm²:
    Δm²₃₂/Δm²₂₁ (предсказание) = {dm32_pred/dm21_pred:.1f}
    Δm²₃₂/Δm²₂₁ (эксперимент)  = {dm32_sq/dm21_sq:.1f}
    {'СОВПАДАЕТ!' if abs(dm32_pred/dm21_pred - dm32_sq/dm21_sq)/(dm32_sq/dm21_sq) < 0.3 else 'Расхождение'}

  Физический смысл:
    Нейтрино = электрон, "подавленный" в α² (электромагнитная "тень").
    α² = (1/137)² = "утечка утечки" — вихрь, видимый через 2 порядка EM.
    π^(i/2) = различие поколений (разные моды на торе, шаг √π).

  ПРОВЕРЯЕМО:
    KATRIN (2025+): m < 0.3 эВ → наше {m3_eV*1000:.0f} мэВ ✓
    Project 8: m < 0.04 эВ → наше {m3_eV*1000:.0f} мэВ {'✓' if m3_eV < 0.04 else '✗?'}
    Σm из CMB-S4: < 0.06 эВ → наше {(m1_eV+m2_eV+m3_eV)*1000:.0f} мэВ {'✓' if (m1_eV+m2_eV+m3_eV) < 0.06 else '⚠️'}
""")


if __name__ == "__main__":
    pass
