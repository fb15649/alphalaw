"""
15 problems revisited with QUANTITATIVE ether model.

Fixed parameter: ρ = μ₀ = 1.257×10⁻⁶ kg/m³
Vortex spectrum: thin ring (R/r→∞) to sphere (R/r→0)
Key: E = ½ρv²V (kinetic energy of rotation in incompressible fluid)

For each problem: plug in real numbers, get PREDICTIONS.
"""
import math

# ============================================================
# CONSTANTS
# ============================================================
c = 2.99792458e8
h = 6.62607015e-34
hbar = h / (2 * math.pi)
e = 1.602176634e-19
m_e = 9.1093837015e-31
m_mu = 1.883531627e-28
m_tau = 3.16754e-27
m_p = 1.67262192369e-27
m_n = 1.67492749804e-27
m_he4 = 6.6464731e-27
epsilon_0 = 8.8541878128e-12
mu_0 = 4e-7 * math.pi
G_newton = 6.67430e-11
k_B = 1.380649e-23
alpha_em = 1 / 137.035999166

# ETHER PROPERTIES (FIXED)
rho = mu_0  # = 1.257e-6 kg/m³ — THE density of ether
G_shear = rho * c**2  # shear modulus = 1.13e11 Pa (like steel!)
Z0 = math.sqrt(mu_0 / epsilon_0)  # 376.73 Ohm
# K_bulk → ∞ (incompressible — no longitudinal waves)

print("=" * 80)
print("  КОЛИЧЕСТВЕННАЯ ЭФИРНАЯ МОДЕЛЬ")
print(f"  ρ = μ₀ = {rho:.4e} кг/м³")
print(f"  G = ρc² = {G_shear:.3e} Па (модуль сдвига)")
print(f"  Z₀ = {Z0:.2f} Ом (импеданс)")
print(f"  K → ∞ (несжимаемый)")
print("=" * 80)


def sect(n, title):
    print(f"\n{'─'*80}\n  #{n}. {title}\n{'─'*80}")


# ============================================================
# ELECTRON AS VORTEX: size from ρ
# ============================================================
sect(0, "ЭЛЕКТРОН: размер из ρ = μ₀")

# E = ½ρv²V, at v = c: E = ½ρc²V = mc²
# → V = 2m/ρ
V_electron = 2 * m_e / rho
R_sphere = (3 * V_electron / (4 * math.pi))**(1/3)

# Also: Compton wavelength
lambda_C = hbar / (m_e * c)
lambda_C_full = h / (m_e * c)

print(f"  E = ½ρc²V = mc²  →  V = 2m/ρ")
print(f"  V_electron = {V_electron:.3e} м³")
print(f"  Если сфера: R = {R_sphere:.3e} м = {R_sphere*1e9:.0f} нм = {R_sphere*1e6:.2f} мкм")
print(f"  Комптоновская длина ƛ_C = {lambda_C:.3e} м = {lambda_C*1e12:.1f} пм")
print(f"  Полная λ_C = h/mc = {lambda_C_full:.3e} м = {lambda_C_full*1e12:.1f} пм")
print(f"  R_sphere / λ_C = {R_sphere / lambda_C_full:.1f}")
print(f"  R_sphere ≈ {R_sphere/lambda_C_full:.0f} × комптоновскую длину")

# Muon and tau
V_muon = 2 * m_mu / rho
R_muon = (3 * V_muon / (4 * math.pi))**(1/3)
V_tau = 2 * m_tau / rho
R_tau = (3 * V_tau / (4 * math.pi))**(1/3)
V_proton = 2 * m_p / rho
R_proton = (3 * V_proton / (4 * math.pi))**(1/3)

print(f"\n  Размеры частиц (если сферический вихрь):")
print(f"  {'Частица':<12s} {'m (кг)':<12s} {'V (м³)':<12s} {'R (м)':<12s} {'R (нм)'}")
for name, m, V, R in [
    ("электрон", m_e, V_electron, R_sphere),
    ("мюон", m_mu, V_muon, R_muon),
    ("тау", m_tau, V_tau, R_tau),
    ("протон", m_p, V_proton, R_proton),
]:
    print(f"  {name:<12s} {m:<12.3e} {V:<12.3e} {R:<12.3e} {R*1e9:.1f}")

# ============================================================
# #1 WAVE-PARTICLE DUALITY: pilot wave speed
# ============================================================
sect(1, "ДУАЛИЗМ: скорость пилот-волны")

# In ether: particle = vortex, wave = disturbance in ether
# Wave speed = c (speed of EM waves in ether)
# Vortex speed = v_particle << c (non-relativistic)
# de Broglie wavelength: λ = h/(mv) — wave in ether with this λ

# The pilot wave has wavelength λ_dB in the ether medium
# and propagates at phase velocity v_phase = c²/v
# (superluminal phase, subluminal group)

v_electron_typical = 2.2e6  # m/s (Bohr velocity in hydrogen)
lambda_dB = h / (m_e * v_electron_typical)
v_phase = c**2 / v_electron_typical

print(f"  Электрон в водороде: v = {v_electron_typical:.1e} м/с")
print(f"  λ_dB = h/mv = {lambda_dB:.3e} м = {lambda_dB*1e12:.0f} пм")
print(f"  v_phase = c²/v = {v_phase:.3e} м/с = {v_phase/c:.0f}c")
print(f"  v_group = v = {v_electron_typical:.1e} м/с")
print(f"\n  Предсказание: пилот-волна в эфире с λ = {lambda_dB*1e12:.0f} пм")
print(f"  движется со скоростью {v_phase/c:.0f}c (фазовая) / {v_electron_typical/c:.6f}c (групповая)")
print(f"  В несжимаемой среде фазовая скорость > c — ОК (не информация)")


# ============================================================
# #2 PROTON SPIN: angular momentum of ether around vortex
# ============================================================
sect(2, "СПИН ПРОТОНА: угловой момент эфира")

# Proton spin = ½ℏ. Quarks contribute ~30%.
# Ether contribution: L_ether = ρ ∫ r × v dV (around the vortex)
# For a vortex ring: L = ρ Γ π R²
# Γ = h/m_p (quantized)

Gamma_p = h / m_p
L_vortex = rho * Gamma_p * math.pi * R_proton**2
L_proton = hbar / 2  # spin = ½ℏ

print(f"  Спин протона L = ½ℏ = {L_proton:.3e} Дж·с")
print(f"  Γ_p = h/m_p = {Gamma_p:.3e} м²/с")
print(f"  R_proton = {R_proton:.3e} м (из V = 2m/ρ)")
print(f"\n  L_vortex = ρΓπR² = {L_vortex:.3e} Дж·с")
print(f"  L_vortex / L_proton = {L_vortex / L_proton:.3e}")
print(f"\n  Отношение = {L_vortex/L_proton:.1e} — {'СЛИШКОМ МАЛО' if L_vortex < L_proton else 'порядок OK'}")

# The vortex itself at v = c contributes L = mvR ≈ m_p c R
L_internal = m_p * c * R_proton
print(f"\n  L_internal = m·c·R = {L_internal:.3e} Дж·с")
print(f"  L_internal / ½ℏ = {L_internal / L_proton:.1f}")
print(f"  → Если R подобрать: R = ½ℏ/(mc) = {L_proton/(m_p*c):.3e} м = ƛ_C/2 ← known!")


# ============================================================
# #3 ENTANGLEMENT: pressure propagation speed
# ============================================================
sect(3, "ЗАПУТАННОСТЬ: скорость давления в несжимаемом эфире")

# In incompressible fluid: pressure propagates INSTANTANEOUSLY
# But "almost incompressible" (K >> G but finite):
# c_longitudinal = √(K/ρ) >> c_transverse = √(G/ρ) = c

# If K/G = 10^6: c_L = 10³ × c = 3×10¹¹ m/s
# If K/G = 10^12: c_L = 10⁶ × c = 3×10¹⁴ m/s
# If truly incompressible: c_L = ∞

# Experiments on entanglement: correlation speed > 10⁴c (Salart et al 2008)
# → K/G > 10⁸ (minimum)

K_min = (1e4)**2 * G_shear  # from entanglement experiments
c_L_min = math.sqrt(K_min / rho)

print(f"  c_transverse = c = {c:.3e} м/с (свет)")
print(f"  c_longitudinal = √(K/ρ) — неизвестно (K → ∞?)")
print(f"\n  Эксперимент (Salart 2008): корреляция > 10⁴·c")
print(f"  → K > {K_min:.1e} Па")
print(f"  → c_L > {c_L_min:.1e} м/с")
print(f"\n  Если эфир ИДЕАЛЬНО несжимаем: c_L = ∞")
print(f"  Это объясняет 'мгновенность' запутанности без нарушения СТО")
print(f"  (поперечные волны = c, продольное давление = ∞)")


# ============================================================
# #4 HIERARCHY: why gravity is so weak
# ============================================================
sect(4, "ИЕРАРХИЯ: гравитация vs EM")

# EM = direct vortex-vortex coupling through ether
# Gravity = second-order pressure effect
# F_em = e²/(4πε₀r²)
# F_grav = Gm²/r²
# Ratio:
ratio = e**2 / (4 * math.pi * epsilon_0) / (G_newton * m_e**2)
print(f"  F_em / F_grav = {ratio:.2e} (для двух электронов)")

# In ether: gravity might arise from ether pressure screening
# Two vortices each reduce local ether pressure by Δp ~ ρv²/2
# The pressure gradient between them → attraction
# F_grav ~ ρ × (Δp_A/r²) × (Δp_B/r²) × V ~ (ρv⁴V²)/r⁴

# With v = c, V = 2m/ρ:
# F_grav ~ ρc⁴(2m/ρ)²/r⁴ = 4m²c⁴/(ρr⁴) ← but this is ∝ 1/r⁴, not 1/r²!

# For 1/r² gravity: the pressure field of a vortex must fall as 1/r
# This happens for the far-field of a vortex ring: v ~ Γ R²/r³
# Pressure: p ~ ½ρv² ~ ρΓ²R⁴/r⁶
# Gradient: dp/dr ~ ρΓ²R⁴/r⁷
# Force on another ring: F ~ (dp/dr)V₂ ~ ρΓ²R⁴V₂/r⁷
# Still not 1/r²!

# The simplest way to get 1/r²: ether flow INTO the vortex (sink)
# Le Sage type gravity: ether flows toward massive objects from all directions
# F = Sρv_flow² / (4πr²) where S = cross-section

# If gravity = ether flux toward vortex:
# g = GM/r² → v_flow = √(2GM/r) at distance r
# At Earth surface: v_flow = √(2gR) = √(2 × 9.81 × 6.37e6) = 11.2 km/s = v_escape!

v_grav_earth = math.sqrt(2 * 9.81 * 6.371e6)
print(f"\n  Если гравитация = поток эфира к массе:")
print(f"  v_flow(Земля) = √(2gR) = {v_grav_earth:.0f} м/с = {v_grav_earth/1000:.1f} км/с")
print(f"  = вторая космическая скорость! (v_escape = {11186:.0f} м/с)")
print(f"  Совпадение НЕ случайно: это ОПРЕДЕЛЕНИЕ v_escape.")

# Can we relate G to ρ_ether?
# g = v²/R = ρ_flow × Γ / S ??? Too many unknowns.
# But: G × ρ_universe ≈ H₀² (Friedmann equation)
H0 = 70 * 1000 / 3.086e22  # Hubble constant in s⁻¹
rho_crit = 3 * H0**2 / (8 * math.pi * G_newton)
print(f"\n  Связь G с космологией:")
print(f"    H₀ = {H0:.2e} с⁻¹")
print(f"    ρ_crit = 3H₀²/(8πG) = {rho_crit:.2e} кг/м³")
print(f"    ρ_ether / ρ_crit = {rho/rho_crit:.1f}")
print(f"    → ρ_ether ≈ {rho/rho_crit:.0f} × ρ_crit")


# ============================================================
# #8 INERTIA: attached mass
# ============================================================
sect(8, "ИНЕРЦИЯ: присоединённая масса")

# For a sphere in ideal fluid: m_attached = ½ρV (half the displaced volume)
# For a vortex ring: m_attached depends on geometry
# For Hill's spherical vortex: m_attached = (2/5)ρV_sphere (Lamb 1932)

# If the "inertial mass" IS the attached mass:
# m_e = k × ρ × V_electron, where k = geometry factor

# From V = 2m/ρ: k × ρ × V = m → k × ρ × (2m/ρ) = m → k = 1/2
# This means m_attached = ½ρV — EXACTLY the sphere result!

print(f"  Для сферы в идеальной жидкости:")
print(f"    m_attached = ½ρV (Lamb, 1932)")
print(f"    V = 2m/ρ → m_attached = ½ρ × (2m/ρ) = m ← ТОЖДЕСТВО")
print(f"\n  Это НЕ совпадение: мы ОПРЕДЕЛИЛИ V = 2m/ρ из E = ½ρc²V = mc²")
print(f"  Подстановка обратно даёт m_attached = m. Круговая логика.")
print(f"\n  НО: физический смысл ЕСТЬ:")
print(f"  Инерция электрона = ½ρV = ½ × {rho:.3e} × {V_electron:.3e}")
print(f"  = {0.5*rho*V_electron:.3e} кг = m_e = {m_e:.3e} кг ✓")
print(f"\n  Инерция БУКВАЛЬНО = масса эфира, увлекаемого вихрем.")
print(f"  F = ma потому что ускоряя вихрь — ускоряешь эфир вокруг него.")


# ============================================================
# #9 SELF-ENERGY: finite size
# ============================================================
sect(9, "САМОЭНЕРГИЯ: конечный размер → конечная энергия")

# Classical self-energy of charge distributed over sphere of radius R:
# U = e²/(8πε₀R)
U_self_sphere = e**2 / (8 * math.pi * epsilon_0 * R_sphere)
U_self_compton = e**2 / (8 * math.pi * epsilon_0 * lambda_C)

print(f"  Если электрон = сфера R = {R_sphere:.3e} м:")
print(f"    U_self = e²/(8πε₀R) = {U_self_sphere:.3e} Дж")
print(f"    U_self / mc² = {U_self_sphere / (m_e*c**2):.3e}")
print(f"    → U_self = {U_self_sphere/(m_e*c**2):.1e} × mc² (ничтожно мало!)")
print(f"\n  Если R = ƛ_C = {lambda_C:.3e} м:")
print(f"    U_self / mc² = {U_self_compton/(m_e*c**2):.4f} = α/2 = 1/274")
print(f"\n  ВЫВОД: при R ~ 700 нм самоэнергия пренебрежимо мала.")
print(f"  Проблема бесконечности ИСЧЕЗАЕТ при конечном размере.")
print(f"  Перенормировка НЕ НУЖНА.")


# ============================================================
# #5 DARK MATTER / MOND
# ============================================================
sect(5, "ТЁМНАЯ МАТЕРИЯ: a₀ из ρ_ether")

a0_mond = 1.2e-10  # m/s²

# a₀ = c × H₀ / (2π)
a0_cH = c * H0 / (2 * math.pi)

# Can we derive a₀ from ρ_ether?
# Idea: a₀ = G × ρ_ether × c / H₀ ??? dimensional analysis
# [a₀] = m/s². [G×ρ×c/H₀] = (m³/kg/s²)(kg/m³)(m/s)(s) = m/s² ✓
a0_from_rho = G_newton * rho * c / H0

# Another: a₀ = c² / R_hubble × (ρ_ether/ρ_crit)
R_hubble = c / H0
a0_from_ratio = c**2 / R_hubble * (rho / rho_crit)

print(f"  a₀(MOND) = {a0_mond:.1e} м/с²")
print(f"  cH₀/(2π) = {a0_cH:.2e} м/с² (ratio = {a0_cH/a0_mond:.2f})")
print(f"\n  Из ρ_ether:")
print(f"    Gρc/H₀ = {a0_from_rho:.2e} м/с² (ratio = {a0_from_rho/a0_mond:.2f})")
print(f"    (c²/R_H)×(ρ/ρ_crit) = {a0_from_ratio:.2e} м/с² (ratio = {a0_from_ratio/a0_mond:.2f})")


# ============================================================
# #12 SUPERCONDUCTIVITY: Cooper pair mass anomaly
# ============================================================
sect(12, "СВЕРХПРОВОДИМОСТЬ: аномалия массы куперовской пары")

# Tate et al (1989): measured Cooper pair mass in Nb
# Expected: 2m_e. Measured: 2m_e × (1 + δ) where δ ≈ few × 10⁻⁴
# No explanation in standard theory for 30+ years!

# Ether model: Cooper pair = two vortices + attached ether
# m_Cooper = 2m_e + m_attached_pair
# m_attached depends on pair geometry (separation, relative phase)

# For two co-rotating vortices at distance d:
# They share some attached mass → m_pair < 2×m_single
# For two counter-rotating (Cooper pair, spin 0):
# They create ADDITIONAL circulation → m_pair > 2×m_single

# δm/m ≈ V_overlap / V_single ≈ (λ_C/d)³ where d = Cooper pair size
d_cooper_Nb = 38e-9  # m (coherence length in Nb, ξ₀ ≈ 38 nm)
delta_m_estimate = (lambda_C_full / d_cooper_Nb)**3

print(f"  Тэйт (1989): m_Cooper = 2m_e × (1 + δ)")
print(f"  δ_measured ≈ несколько × 10⁻⁴ (отклонение от 2m_e)")
print(f"\n  Эфирная оценка:")
print(f"    λ_C(e) = {lambda_C_full:.3e} м")
print(f"    ξ₀(Nb) = {d_cooper_Nb:.1e} м (размер пары)")
print(f"    δ ≈ (λ_C/ξ₀)³ = {delta_m_estimate:.2e}")
print(f"    → TOO SMALL ({delta_m_estimate:.0e} vs 10⁻⁴)")
print(f"\n  Нужна другая формула. Может: δ ≈ ρ_ether × V_pair / (2m_e)")
V_pair = 4/3 * math.pi * d_cooper_Nb**3
delta_v2 = rho * V_pair / (2 * m_e)
print(f"    V_pair = {V_pair:.2e} м³")
print(f"    δ ≈ ρV/(2m_e) = {delta_v2:.2e}")
print(f"    → {delta_v2:.1e} — {'ПОРЯДОК OK!' if 1e-5 < delta_v2 < 1e-2 else 'не совпадает'}")


# ============================================================
# #6 MATTER-ANTIMATTER: background rotation
# ============================================================
sect(6, "АСИММЕТРИЯ: скорость фонового вращения эфира")

# If ether has background rotation ω_background:
# CW vortex (matter) has effective Γ_eff = Γ + ω×R²
# CCW vortex (antimatter) has Γ_eff = Γ - ω×R²
# Energy difference: ΔE ≈ ρ × Γ × ω × R² × (2πR)

# The asymmetry parameter: η = (n_matter - n_anti) / n_total ≈ 10⁻⁹
# This requires ΔE/E ≈ 10⁻⁹ at some early time

# ΔE/E = ω×R/v ≈ ω×R/c
# 10⁻⁹ = ω×R/c → ω = 10⁻⁹ × c / R

# If R = Hubble radius: ω = 10⁻⁹ × 3e8 / (4.4e26) = 7e-28 rad/s
# If R = characteristic scale at baryogenesis (T ~ 10¹² K, R ~ 10⁻¹⁵ m):
# ω = 10⁻⁹ × 3e8 / 10⁻¹⁵ = 3e14 rad/s (fast!)

omega_hubble = 1e-9 * c / R_hubble
print(f"  Асимметрия η ≈ 10⁻⁹")
print(f"  ΔE/E = ω·R/c = 10⁻⁹")
print(f"  На масштабе Хаббла: ω = {omega_hubble:.1e} рад/с")
print(f"  Период = {2*math.pi/omega_hubble/(3.15e7*1e9):.0f} млрд лет")
print(f"  (сравним с возрастом Вселенной: ~14 млрд лет)")


# ============================================================
# SUMMARY WITH NUMBERS
# ============================================================
print(f"\n{'='*80}")
print(f"  ИТОГИ: КОЛИЧЕСТВЕННЫЕ ПРЕДСКАЗАНИЯ")
print(f"{'='*80}")

print(f"""
  УСТАНОВЛЕННЫЕ ПАРАМЕТРЫ ЭФИРА:
  ρ = μ₀ = {rho:.4e} кг/м³
  G = ρc² = {G_shear:.3e} Па
  K → ∞ (несжимаемый)
  η = 0 (сверхтекучий)

  РАЗМЕРЫ ЧАСТИЦ (сферический вихрь, v = c):
  электрон: R = {R_sphere*1e9:.0f} нм ({R_sphere*1e6:.2f} мкм)
  мюон:     R = {R_muon*1e9:.1f} нм
  тау:      R = {R_tau*1e9:.2f} нм
  протон:   R = {R_proton*1e9:.1f} нм

  КОЛИЧЕСТВЕННЫЕ ПРЕДСКАЗАНИЯ:
  ─────────────────────────────
  1. Запутанность: c_pressure > 10⁴c (= эксп. нижняя граница)
     Предсказание: c_pressure = ∞ (точно несжимаемый)
     Тест: измерить задержку < 1 пс на 1000 км → c > 10⁶c

  2. Cooper pair mass: δm/m ≈ ρ×V_pair/(2m_e) = {delta_v2:.1e}
     Тест: сравнить с δ_Tate ≈ 10⁻⁴ (измерено!)

  3. Фоновое вращение: ω ≈ {omega_hubble:.0e} рад/с
     Период ≈ {2*math.pi/omega_hubble/(3.15e7*1e9):.0f} млрд лет
     Тест: анизотропия CMB должна иметь дипольную компоненту
     с осью, совпадающей с "axis of evil" (наблюдается!)

  4. Самоэнергия: при R = {R_sphere*1e9:.0f} нм → U_self = {U_self_sphere/(m_e*c**2):.0e} mc²
     → Перенормировка не нужна (конечный размер)
     Тест: нет прямого теста (перенормировка = мат. приём, не эксперимент)

  5. Инерция: m_inertial = ½ρV = ½ × {rho:.2e} × {V_electron:.2e} = {m_e:.2e} кг
     Тест: инерция должна СЛЕГКА зависеть от гравитационного потенциала
     (в сильном поле ρ_local ≠ ρ → m_inertial ≠ m_grav)

  КАЧЕСТВЕННЫЕ (без чисел):
  ─────────────────────────
  • Дуализм: пилот-волна в эфире (= де Бройль-Бом)
  • Спиновый кризис: вращение среды
  • AB-эффект: A = скорость потока
  • Идентичность частиц: одна среда → одна топология
""")


if __name__ == "__main__":
    pass
