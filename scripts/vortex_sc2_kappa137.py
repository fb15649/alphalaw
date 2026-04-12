"""
ВИХРЬ В СВЕРХПРОВОДНИКЕ II ТИПА С κ = 1/α = 137
==================================================

Не выводим α. Принимаем: κ_ГЛ = 1/α = 137.036.
Смотрим что СЛЕДУЕТ для вихря.
"""
import math

pi = math.pi
hbar = 1.05457e-34
c = 2.998e8
h = 2 * pi * hbar
mu_0 = 4e-7 * pi
eps_0 = 1 / (mu_0 * c**2)
e = 1.602e-19
m_e = 9.109e-31
alpha = 1 / 137.036
kappa = 1 / alpha  # GL parameter

# Derived lengths
lambda_C = hbar / (m_e * c)   # reduced Compton wavelength
r_e = alpha * lambda_C         # classical electron radius
Phi_0 = h / (2 * e)           # magnetic flux quantum
Z_0 = mu_0 * c


print("=" * 76)
print("  ВИХРЬ АБРИКОСОВА С κ = 1/α = 137")
print("=" * 76)

print(f"""
  ДАНО: κ = λ_L/ξ = 1/α = {kappa:.2f}

  В ЛЮБОМ сверхпроводнике II типа с параметром κ:
    λ_L = глубина проникновения магнитного поля
    ξ   = длина когерентности (размер ядра вихря)
    κ   = λ_L/ξ — определяет ВСЕ свойства вихрей

  Отождествление:
    λ_L = ƛ_e = ℏ/(m_e c) = {lambda_C:.4e} м
    ξ   = r_e = α·ƛ_e      = {r_e:.4e} м
    κ   = ƛ_e/r_e = 1/α    = {kappa:.2f} ✓
""")


# ==========================================================
# 1. Energy of one vortex (per unit length)
# ==========================================================
print("=" * 76)
print("  1. ЭНЕРГИЯ ОДНОГО ВИХРЯ")
print("=" * 76)

# Standard GL formula:
# ε₁ = (Φ₀/(4πλ_L))² × ln(κ)  (energy per unit length)
eps_1 = (Phi_0 / (4 * pi * lambda_C))**2 / mu_0 * math.log(kappa)

print(f"""
  Энергия на единицу длины (формула ГЛ):
    ε₁ = (Φ₀/(4πλ_L))² / μ₀ × ln(κ)

  Φ₀ = {Phi_0:.4e} Вб
  λ_L = ƛ_e = {lambda_C:.4e} м
  ln(κ) = ln(1/α) = {math.log(kappa):.4f}

  ε₁ = {eps_1:.4e} Дж/м
""")

# For a RING of circumference 2πR:
# E_ring = ε₁ × 2πR
# What R gives E = m_e c²?
E_target = m_e * c**2
R_for_me = E_target / (eps_1 * 2 * pi)

print(f"  Для E_ring = m_e c² = {E_target:.4e} Дж:")
print(f"  R = m_e c²/(2πε₁) = {R_for_me:.4e} м")
print(f"  R/ƛ_e = {R_for_me/lambda_C:.4f}")
print(f"  R/r_e = {R_for_me/r_e:.2f}")

# N = R/ξ for this ring:
N_ring = R_for_me / r_e
print(f"\n  N = R/ξ = R/r_e = {N_ring:.2f}")


# ==========================================================
# 2. Magnetic flux through the ring
# ==========================================================
print(f"\n{'='*76}")
print(f"  2. МАГНИТНЫЙ ПОТОК ЧЕРЕЗ КОЛЬЦО")
print(f"{'='*76}")

# Self-inductance of a torus:
# L = μ₀ R [ln(8R/a) − 2]  (for R >> a)
# Current in vortex: I = Φ₀/(μ₀ λ_L)  (per unit length) ...
# Actually for Abrikosov: the current flows in a shell of thickness λ_L

# More directly:
# The vortex carries exactly 1 flux quantum Φ₀ ALONG its core.
# The flux THROUGH the ring (self-induced) is different.

# For a superconducting ring with current I:
# Φ_through = L × I = n Φ₀ (fluxoid quantization)

# Current in vortex ring ≈ Φ₀/(μ₀ λ_L²) × (2πa) × (1/(2π)) = Φ₀ a/(μ₀ λ_L²)
# Wait, let me be more careful.

# In Abrikosov vortex: the supercurrent density at distance r from core:
# j(r) = Φ₀/(2πμ₀λ_L²) × K₁(r/λ_L)/r  (for r >> ξ)
# Total current (integrated): I = Φ₀/(μ₀λ_L) approximately

I_vortex = Phi_0 / (mu_0 * lambda_C)
print(f"\n  Ток вихря: I ≈ Φ₀/(μ₀λ_L) = {I_vortex:.4e} А")

# For a ring: self-inductance
a_core = r_e  # core radius = ξ = r_e
if R_for_me > a_core:
    L_ring = mu_0 * R_for_me * (math.log(8*R_for_me/a_core) - 2)
else:
    L_ring = mu_0 * R_for_me  # rough estimate

Phi_through = L_ring * I_vortex
n_flux = Phi_through / Phi_0

print(f"  Самоиндуктивность кольца: L = {L_ring:.4e} Гн")
print(f"  Поток через кольцо: Φ = LI = {Phi_through:.4e} Вб")
print(f"  Φ/Φ₀ = {n_flux:.2f}")
print(f"  → Кольцо содержит ≈ {n_flux:.0f} квантов потока")


# ==========================================================
# 3. Key numbers table
# ==========================================================
print(f"\n{'='*76}")
print(f"  3. ТАБЛИЦА СВОЙСТВ ВИХРЯ С κ = 137")
print(f"{'='*76}")

# Magnetic field at core:
B_core = Phi_0 / (2 * pi * r_e**2)  # rough: flux through core area
# More accurate: B(0) = Φ₀/(2πξ²) × ln(κ) for κ >> 1
B_core_accurate = Phi_0 / (2 * pi * r_e**2) * math.log(kappa) / kappa
# Actually: B(0) ≈ (Φ₀/(2πλ²)) × ln(κ) for extreme type II
B_center = Phi_0 / (2 * pi * lambda_C**2) * math.log(kappa)

# Lower critical field
H_c1 = Phi_0 / (4 * pi * mu_0 * lambda_C**2) * (math.log(kappa) + 0.5)

# Upper critical field
H_c2 = Phi_0 / (2 * pi * mu_0 * r_e**2)

# Thermodynamic critical field
H_c = math.sqrt(H_c1 * H_c2 * 2 * pi * mu_0 / Phi_0) if H_c1 > 0 else 0
# More accurately: H_c = Φ₀/(2√2 π μ₀ λξ)
H_c_accurate = Phi_0 / (2 * math.sqrt(2) * pi * mu_0 * lambda_C * r_e)

print(f"""
  Параметр                    Формула              Значение
  ──────────────────────────  ──────────────────── ──────────────
  κ (параметр ГЛ)            λ_L/ξ               {kappa:.2f}
  λ_L (глубина проникн.)     ƛ_e = ℏ/(m_e c)     {lambda_C:.3e} м
  ξ (длина когерентности)    r_e = αƛ_e           {r_e:.3e} м
  Φ₀ (квант потока)          h/(2e)               {Phi_0:.3e} Вб
  ε₁ (энергия/длина)         Φ₀²ln(κ)/(4π²μ₀λ²) {eps_1:.3e} Дж/м
  I (ток вихря)              Φ₀/(μ₀λ)            {I_vortex:.3e} А = {I_vortex:.1f} А
  R кольца (для m_e)         m_ec²/(2πε₁)        {R_for_me:.3e} м
  N = R/ξ                    R/r_e                {N_ring:.2f}
  B(центр)                   Φ₀ln(κ)/(2πλ²)      {B_center:.3e} Тл
  H_c1 (нижнее крит.)        Φ₀ln(κ)/(4πμ₀λ²)   {H_c1:.3e} А/м
  H_c2 (верхнее крит.)       Φ₀/(2πμ₀ξ²)         {H_c2:.3e} А/м
""")


# ==========================================================
# 4. Physical interpretation
# ==========================================================
print(f"{'='*76}")
print(f"  4. ФИЗИЧЕСКАЯ ИНТЕРПРЕТАЦИЯ")
print(f"{'='*76}")

print(f"""
  ТОК ВИХРЯ: I = {I_vortex:.1f} А ≈ {I_vortex:.0f} ампер!

  Это ОГРОМНЫЙ ток. Для сравнения:
    Ток в бытовой проводке: ~10 А
    Ток в молнии: ~30 000 А
    Ток вихря электрона: {I_vortex:.0f} А

  Каждый электрон — это контур с током {I_vortex:.0f} А,
  замкнутый в кольцо радиусом {R_for_me:.1e} м.

  Магнитный момент:
    μ = I × πR² = {I_vortex * pi * R_for_me**2:.4e} Дж/Тл
  Магнетон Бора:
    μ_B = eℏ/(2m_e) = {e*hbar/(2*m_e):.4e} Дж/Тл
  Отношение: {I_vortex * pi * R_for_me**2 / (e*hbar/(2*m_e)):.4f}
""")

# Upper critical field is ENORMOUS
print(f"""
  ВЕРХНЕЕ КРИТИЧЕСКОЕ ПОЛЕ: H_c2 = {H_c2:.2e} А/м
  = {H_c2*mu_0:.2e} Тл = {H_c2*mu_0/1e9:.0f} ГТл

  Для сравнения:
    Поле Земли: ~50 мкТл
    МРТ: ~3 Тл
    Самый сильный лаб. магнит: ~45 Тл
    Нейтронная звезда: ~10⁸ Тл
    Магнетар: ~10¹¹ Тл
    Наш H_c2: {H_c2*mu_0:.0e} Тл

  Эфир остаётся "сверхпроводящим" до полей ≈ {H_c2*mu_0:.0e} Тл.
  Выше H_c2 — сверхпроводимость разрушается → "нормальная фаза".
  Это соответствует условиям внутри тяжёлых ионов на коллайдерах:
  quark-gluon plasma = "нормальная фаза эфира"?
""")

# What is the lower critical field?
print(f"""
  НИЖНЕЕ КРИТИЧЕСКОЕ ПОЛЕ: H_c1 = {H_c1:.2e} А/м
  = {H_c1*mu_0:.2e} Тл = {H_c1*mu_0:.0f} Тл

  При H > H_c1 вихри начинают входить в сверхпроводник.
  При H < H_c1 — полный Мейсснер-эффект (полное выталкивание поля).

  H_c1 = {H_c1*mu_0:.0f} Тл — это ТОЖЕ огромное поле!
  Вихри Абрикосова (= частицы) появляются только
  при полях > {H_c1*mu_0:.0f} Тл.

  Это может объяснить рождение пар e⁺e⁻:
  фотон с E > 2m_ec² → поле > H_c1 → пара вихрь-антивихрь!
""")

E_pair = 2 * m_e * c**2
E_pair_eV = E_pair / 1.602e-19
print(f"  Порог рождения пар: E = 2m_ec² = {E_pair_eV/1e6:.3f} МэВ")
print(f"  Частота: ν = E/h = {E_pair/h:.3e} Гц")
print(f"  Это граница между сверхпроводящей и нормальной фазой эфира.")


# ==========================================================
# 5. Comparison with real superconductors
# ==========================================================
print(f"\n{'='*76}")
print(f"  5. СРАВНЕНИЕ С РЕАЛЬНЫМИ СВЕРХПРОВОДНИКАМИ")
print(f"{'='*76}")

print(f"""
  Материал            κ       λ_L (нм)  ξ (нм)   T_c (K)
  ──────────────────  ──────  ────────  ───────  ────────
  Nb (ниобий)         1.0     39        39       9.3
  NbTi                60      300       5        10
  Nb₃Sn              20      80        4        18
  YBCO                95      150       1.6      93
  BSCCO               150     200       1.3      110
  MgB₂                26      140       5.2      39
  ──────────────────────────────────────────────────────
  ЭФИР                {kappa:.0f}     {lambda_C*1e9:.4f}  {r_e*1e9:.6f}  ???

  Эфир — ЭКСТРЕМАЛЬНЫЙ сверхпроводник II типа:
    κ = 137 — рекорд (BSCCO ≈ 150, близко!)
    λ_L = 0.000386 нм = 0.386 пм (субатомный!)
    ξ = 0.00000282 нм = 2.82 фм (ядерный масштаб!)
    T_c = ??? (наше предсказание: T_c ≈ ∞, т.к. η = 0)

  BSCCO с κ ≈ 150 — ближайший аналог эфира!
  Это высокотемпературный сверхпроводник (купрат).
  Совпадение или подсказка?
""")


# ==========================================================
# 6. Summary
# ==========================================================
print(f"""
{'='*76}
  ИТОГ: ЧТО СЛЕДУЕТ ИЗ κ = 1/α
{'='*76}

  1. Электрон = вихрь Абрикосова с током {I_vortex:.0f} А

  2. Кольцо радиусом R ≈ {R_for_me:.1e} м ≈ {R_for_me/r_e:.0f} × r_e
     (N = R/ξ ≈ {N_ring:.0f} — «толстоватый» вихрь)

  3. Рождение пар e⁺e⁻ = превышение H_c1 ≈ {H_c1*mu_0:.0f} Тл
     (фотон с E > 1.022 МэВ → "вход вихрей" в эфир)

  4. Quark-gluon plasma = превышение H_c2 ≈ {H_c2*mu_0:.0e} Тл
     (разрушение сверхпроводимости = "нормальная фаза")

  5. Ближайший реальный аналог: BSCCO (κ ≈ 150, купрат)

  6. N_ring = {N_ring:.2f} — это ОТЛИЧАЕТСЯ от e³/8 = 2.51
     и от π = 3.14. Нужно понять какое N правильное.

  ЧЕСТНО:
  ✓ Картина физически осмысленна
  ✓ Числа в правильных порядках
  ✗ N_ring ≈ {N_ring:.0f} не совпадает с другими оценками
  ✗ T_c эфира — не определена
  ✗ Почему κ = 1/α — не выведено (принято как факт)
""")
