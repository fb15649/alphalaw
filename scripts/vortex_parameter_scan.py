"""
Scan R/r (aspect ratio) from 1 to 10000.
For each R/r, compute ALL vortex properties.
Find which R/r gives the best match to KNOWN experimental values.

Fixed: ρ = μ₀ = 4π×10⁻⁷ kg/m³
Variable: R/r (aspect ratio of toroid)
Derived: everything else
"""
import math
import numpy as np

# ============================================================
# CONSTANTS
# ============================================================
c = 2.99792458e8
h = 6.62607015e-34
hbar = h / (2 * math.pi)
e = 1.602176634e-19
mu_0 = 4e-7 * math.pi
epsilon_0 = 8.8541878128e-12
alpha_exp = 1 / 137.035999166

# Experimental targets
m_e_exp = 9.1093837015e-31
mu_e_exp = 9.2740100783e-24  # electron magnetic moment (J/T)
mu_bohr = e * hbar / (2 * m_e_exp)  # Bohr magneton
g_factor_exp = 2.00231930436256  # electron g-factor
spin_exp = hbar / 2  # ½ℏ

# Ether
rho = mu_0  # 1.2566e-6 kg/m³

print("=" * 90)
print("  СКАН R/r: поиск aspect ratio тороида электрона")
print(f"  ρ = μ₀ = {rho:.4e} кг/м³, c = {c:.3e} м/с")
print("=" * 90)

# ============================================================
# For a vortex ring with major radius R and minor radius r:
#
# Volume:        V = 2π²Rr²
# Energy (thin):  E = ½ρΓ²R[ln(8R/r) - 7/4]  (Kelvin, valid for R >> r)
# Energy (thick): E ≈ ½ρc²V = ½ρc² × 2π²Rr² (for v_tube ≈ c)
# Angular momentum: L = ρΓπR²  (impulse of vortex ring)
# Circulation:   Γ = h/m (quantized)
# Velocity in tube: v_tube = Γ/(2πr)
# Velocity of ring: v_ring = Γ/(4πR)[ln(8R/r) - 1/4]
#
# We want v_tube ≈ c (relativistic rotation inside tube)
# This gives: r = Γ/(2πc) = h/(2πmc) = ƛ_C (Compton wavelength!)
#
# So r is FIXED by the condition v_tube = c:
#   r = h/(2πmc) = ƛ_C
#
# And R = r × (R/r) — varies with aspect ratio
#
# Mass from energy:
#   If v_tube = c: E_kinetic = ½ρc² × V = ½ρc² × 2π²Rr² = π²ρc²Rr²
#   Set = mc²: m = π²ρRr²
#   With r = ƛ_C = ℏ/(mc): r depends on m!
#
# Self-consistent:
#   m = π²ρR(ℏ/(mc))²
#   m³ = π²ρRℏ²/c²
#   R = m³c²/(π²ρℏ²)
#
# And r = ℏ/(mc), R/r = m³c²/(π²ρℏ²) × mc/ℏ = m⁴c³/(π²ρℏ³)
#
# So R/r is determined by m! (and vice versa)
# R/r = m⁴c³/(π²ρℏ³)
# ============================================================

print("\n  Самосогласованное решение:")
print("  Условие: v_tube = Γ/(2πr) = c → r = ƛ_C = ℏ/(mc)")
print("  Энергия: E = π²ρc²Rr² = mc² → R = m/(π²ρr²) = m³c²/(π²ρℏ²)")
print("  R/r = m⁴c³/(π²ρℏ³)")

# Compute for electron
r_e = hbar / (m_e_exp * c)  # Compton wavelength
R_e = m_e_exp**3 * c**2 / (math.pi**2 * rho * hbar**2)
Rr_e = R_e / r_e

print(f"\n  Электрон:")
print(f"    r = ƛ_C = {r_e:.4e} м = {r_e*1e15:.1f} фм")
print(f"    R = m³c²/(π²ρℏ²) = {R_e:.4e} м = {R_e*1e15:.1f} фм")
print(f"    R/r = {Rr_e:.4f}")

# What does α = (r/R)² give?
alpha_from_Rr = (r_e / R_e)**2
print(f"\n    α = (r/R)² = {alpha_from_Rr:.6e}")
print(f"    1/α = {1/alpha_from_Rr:.1f}")
print(f"    Факт: 1/α = 137.036")
print(f"    Совпадает? {'ДА!!!' if abs(1/alpha_from_Rr - 137.036) < 1 else 'НЕТ'}")

# Angular momentum
Gamma_e = h / m_e_exp
L_e = rho * Gamma_e * math.pi * R_e**2
print(f"\n    Γ = h/m = {Gamma_e:.4e} м²/с")
print(f"    L = ρΓπR² = {L_e:.4e} Дж·с")
print(f"    ½ℏ = {spin_exp:.4e} Дж·с")
print(f"    L / (½ℏ) = {L_e / spin_exp:.4f}")

# Magnetic moment
# For a current ring: μ = IA = (eω/(2π)) × πR² = eωR²/2
# ω = v_ring/R = Γ/(4πR²) × [ln(8R/r) - 1/4] ... complicated
# Simpler: μ = (e/2m)L (gyromagnetic ratio for orbital motion)
# For spin: μ = g(e/2m)(ℏ/2) where g ≈ 2
mu_orbital = (e / (2 * m_e_exp)) * L_e
print(f"\n    μ_orbital = (e/2m)L = {mu_orbital:.4e} Дж/Тл")
print(f"    μ_Bohr = {mu_bohr:.4e} Дж/Тл")
print(f"    μ_orbital / μ_Bohr = {mu_orbital/mu_bohr:.4f}")

# Self-energy
U_self = e**2 / (8 * math.pi * epsilon_0 * R_e)
print(f"\n    U_self = e²/(8πε₀R) = {U_self:.4e} Дж")
print(f"    U_self / mc² = {U_self/(m_e_exp*c**2):.6f}")
print(f"    α = {alpha_exp:.6f}")
print(f"    Совпадает? {abs(U_self/(m_e_exp*c**2) - alpha_exp)/alpha_exp*100:.2f}% ошибка")

# Velocity of vortex ring (self-propagation speed)
if Rr_e > 1.5:
    ln_factor = math.log(8 * Rr_e) - 0.25
    v_ring = Gamma_e / (4 * math.pi * R_e) * ln_factor
    print(f"\n    v_ring = Γ/(4πR)·[ln(8R/r)-¼] = {v_ring:.2e} м/с = {v_ring/c:.4f}c")
else:
    print(f"\n    R/r = {Rr_e:.2f} < 1.5 → формула тонкого кольца не работает")

# ============================================================
# Now the KEY question: is the self-consistent solution unique?
# ============================================================
print(f"\n{'='*90}")
print("  КЛЮЧЕВОЙ ВОПРОС: единственно ли решение?")
print("=" * 90)

# We have:
# (1) r = ℏ/(mc)              ← Compton wavelength (from v_tube = c)
# (2) m = π²ρRr²             ← energy = mc²
# (3) R/r = m⁴c³/(π²ρℏ³)    ← from (1) and (2)
#
# This gives R/r as function of m. So R/r is NOT free — it's determined by m!
# And m is determined by (ρ, ℏ, c):
#
# From (2): m = π²ρ(R/r)r³ = π²ρ(R/r)(ℏ/(mc))³ = π²ρ(R/r)ℏ³/(m³c³)
# m⁴ = π²ρ(R/r)ℏ³/c³
# But R/r = m⁴c³/(π²ρℏ³) → substituting back:
# m⁴ = π²ρ × m⁴c³/(π²ρℏ³) × ℏ³/c³ = m⁴
# TAUTOLOGY!!! The system is underdetermined.

print(f"""
  Система уравнений:
  (1) r = ℏ/(mc)           ← v_tube = c
  (2) m = π²ρRr²          ← E = mc²
  (3) R/r = m⁴c³/(π²ρℏ³)  ← из (1)+(2)

  Подставляем (3) в (2):
  m = π²ρ × [m⁴c³/(π²ρℏ³)] × [ℏ/(mc)]²
  m = π²ρ × m⁴c³/(π²ρℏ³) × ℏ²/(m²c²)
  m = m⁴c³ × ℏ²/(ℏ³ × m²c²)
  m = m⁴c/(ℏm²)
  m = m²c/ℏ ... НЕТ

  Пересчитаем аккуратно:
  m = π²ρRr²
  R = (R/r) × r = [m⁴c³/(π²ρℏ³)] × [ℏ/(mc)]
  R = m³c²/(π²ρℏ²)

  m = π²ρ × [m³c²/(π²ρℏ²)] × [ℏ/(mc)]²
  m = π²ρ × m³c²/(π²ρℏ²) × ℏ²/(m²c²)
  m = m³c² × ℏ²/(ℏ² × m²c²)  ... π²ρ сокращается!
  m = m³/m² × c²/c² × 1/1
  m = m  ← ТОЖДЕСТВО

  → Система ВЫРОЖДЕНА: m и R/r НЕ определяются!
  → Любая масса m удовлетворяет при соответствующем R/r.
  → Нужно ЧЕТВЁРТОЕ уравнение для фиксации m.
""")

# What could be the 4th equation?
print("  Кандидаты на 4-е уравнение:")
print("  ─────────────────────────────")

# (A) Spin quantization: L = ρΓπR² = ½ℏ
print("\n  (A) L = ½ℏ (спин-½)")
# L = ρ(h/m)πR² = ρh π R²/m
# = ρhπ/(m) × [m³c²/(π²ρℏ²)]²
# = ρhπ/m × m⁶c⁴/(π⁴ρ²ℏ⁴)
# = hm⁵c⁴/(π³ρℏ⁴)
# = (2πℏ)m⁵c⁴/(π³ρℏ⁴) = 2m⁵c⁴/(π²ρℏ³)
# Set = ℏ/2:
# 2m⁵c⁴/(π²ρℏ³) = ℏ/2
# m⁵ = π²ρℏ⁴/(4c⁴)

m_from_spin = (math.pi**2 * rho * hbar**4 / (4 * c**4))**(1/5)
print(f"     m⁵ = π²ρℏ⁴/(4c⁴)")
print(f"     m = [{math.pi**2 * rho * hbar**4 / (4 * c**4):.3e}]^(1/5)")
print(f"     m = {m_from_spin:.4e} кг")
print(f"     m_e = {m_e_exp:.4e} кг")
print(f"     Ratio = {m_from_spin/m_e_exp:.4f}")
print(f"     Error = {abs(m_from_spin - m_e_exp)/m_e_exp * 100:.2f}%")

if abs(m_from_spin/m_e_exp - 1) < 0.01:
    print(f"     ★★★ СОВПАДЕНИЕ ЛУЧШЕ 1%! ★★★")
elif abs(m_from_spin/m_e_exp - 1) < 0.1:
    print(f"     ★★ СОВПАДЕНИЕ ЛУЧШЕ 10% ★★")
elif abs(m_from_spin/m_e_exp - 1) < 0.5:
    print(f"     ★ ПОРЯДОК ВЕРНЫЙ ★")

# Compute R/r for this mass
r_spin = hbar / (m_from_spin * c)
R_spin = m_from_spin**3 * c**2 / (math.pi**2 * rho * hbar**2)
Rr_spin = R_spin / r_spin
alpha_spin = (r_spin / R_spin)**2

print(f"\n     При m = {m_from_spin:.3e}:")
print(f"     R/r = {Rr_spin:.2f}")
print(f"     α = (r/R)² = {alpha_spin:.6f}")
print(f"     1/α = {1/alpha_spin:.2f}")
print(f"     1/α(exp) = 137.036")

# (B) Charge quantization: e = ρΓ × (something geometric)
print("\n  (B) e = функция(ρ, Γ) — заряд из циркуляции")
# If e = ρΓ × 2πr (charge = circulation × circumference × density)
# e = ρ(h/m) × 2π(ℏ/mc) = ρh × 2πℏ/(m²c) = 2πρh × ℏ/(m²c)
# = 4π²ρℏ²/(m²c)
e_from_rho = 4 * math.pi**2 * rho * hbar**2 / (m_e_exp**2 * c)
print(f"     Если e = 4π²ρℏ²/(m²c):")
print(f"     e_calc = {e_from_rho:.4e} Кл")
print(f"     e_exp  = {e:.4e} Кл")
print(f"     Ratio = {e_from_rho/e:.4f}")

# Try e = ρΓr (simplest)
e_simple = rho * Gamma_e * r_e
print(f"\n     Если e = ρΓr:")
print(f"     e_calc = {e_simple:.4e}")
print(f"     e_exp  = {e:.4e}")
print(f"     Ratio = {e_simple/e:.4f}")

# ============================================================
# SUMMARY
# ============================================================
print(f"\n{'='*90}")
print("  ИТОГИ")
print("=" * 90)

print(f"""
  МОДЕЛЬ: Электрон = тороидальный вихрь в эфире (ρ = μ₀)
  Условие: v_tube = c (скорость в трубке = скорость света)

  САМОСОГЛАСОВАННЫЕ ПАРАМЕТРЫ:
  r = ƛ_C = {r_e*1e15:.1f} фм  (малый радиус = комптоновская длина)
  R = {R_e*1e15:.1f} фм  (большой радиус, зависит от m)
  R/r = {Rr_e:.2f}

  ПОПЫТКА ВЫВЕСТИ m_e:
  (A) Из L = ½ℏ: m = {m_from_spin:.3e} кг
      m/m_e = {m_from_spin/m_e_exp:.4f} — ОШИБКА {abs(m_from_spin/m_e_exp-1)*100:.1f}%
      1/α = {1/alpha_spin:.1f} (exp: 137.036)

  ВЕРДИКТ:
""")

err_m = abs(m_from_spin/m_e_exp - 1) * 100
err_alpha = abs(1/alpha_spin - 137.036) / 137.036 * 100

if err_m < 1 and err_alpha < 1:
    print("  ★★★ ТЕОРИЯ: m_e И α выводятся из (ρ, ℏ, c) + v=c + L=½ℏ!")
elif err_m < 10 and err_alpha < 10:
    print("  ★★ ПЕРСПЕКТИВНО: порядок верный, нужна поправка на геометрию")
elif err_m < 50:
    print(f"  ★ ПОРЯДОК ВЕРНЫЙ (m ошибка {err_m:.0f}%, α ошибка {err_alpha:.0f}%)")
    print("    Нужно: точная формула энергии для данного R/r")
else:
    print(f"  FAIL: m ошибка {err_m:.0f}%, α ошибка {err_alpha:.0f}%")


if __name__ == "__main__":
    pass
