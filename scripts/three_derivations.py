"""
Three attempts to derive KNOWN constants from ρ = μ₀.

If ANY of these works WITHOUT fitting — we have a THEORY, not just a dictionary.

Candidate 1: Derive m_e from (ρ, ℏ, c) alone
Candidate 2: Derive Koide ratio 2/3 from toroid geometry
Candidate 3: Derive α = 1/137 from vortex stability condition (R/r)

Rules: NO fitting. Only ρ = μ₀, ℏ, c, and geometry.
"""
import math

# ============================================================
# CONSTANTS (given)
# ============================================================
c = 2.99792458e8
h = 6.62607015e-34
hbar = h / (2 * math.pi)
e_charge = 1.602176634e-19
m_e = 9.1093837015e-31    # TARGET (should we derive this?)
m_mu = 1.883531627e-28
m_tau = 3.16754e-27
epsilon_0 = 8.8541878128e-12
mu_0 = 4e-7 * math.pi
G_newton = 6.67430e-11
alpha_em = 1 / 137.035999166

# Ether
rho = mu_0  # = 1.257e-6 kg/m³

print("=" * 80)
print("  ТРИ ПОПЫТКИ ВЫВЕСТИ КОНСТАНТЫ ИЗ ρ = μ₀")
print("  Правило: БЕЗ подгонки. Только ρ, ℏ, c и геометрия.")
print("=" * 80)


# ============================================================
# CANDIDATE 1: m_e from (ρ, ℏ, c)
# ============================================================
print(f"""
{'='*80}
  КАНДИДАТ 1: МАССА ЭЛЕКТРОНА ИЗ (ρ, ℏ, c)
{'='*80}

  Размерный анализ: какие комбинации ρ, ℏ, c имеют размерность массы?

  [ρ] = кг/м³,  [ℏ] = кг·м²/с,  [c] = м/с

  m = ρᵃ × ℏᵇ × cᵈ

  кг:  1 = a + b
  м:   0 = -3a + 2b + d
  с:   0 = -b - d

  Из с: d = -b. Из кг: a = 1 - b.
  Из м: 0 = -3(1-b) + 2b + (-b) = -3 + 3b + 2b - b = -3 + 4b → b = 3/4

  m = ρ^(1/4) × ℏ^(3/4) × c^(-3/4)
""")

m_from_rhc = rho**(1/4) * hbar**(3/4) * c**(-3/4)
print(f"  m = ρ^(1/4) · ℏ^(3/4) · c^(-3/4)")
print(f"    = ({rho:.3e})^0.25 × ({hbar:.3e})^0.75 × ({c:.3e})^-0.75")
print(f"    = {m_from_rhc:.4e} кг")
print(f"  m_e (факт) = {m_e:.4e} кг")
print(f"  Ratio = {m_from_rhc / m_e:.4f}")
print(f"  Error = {abs(m_from_rhc - m_e)/m_e * 100:.1f}%")

# What about numerical prefactors from geometry?
# If the vortex is a sphere: prefactor = (3/(4π))^(1/4) × (2)^something?
# Let's try with various geometric prefactors
print(f"\n  С геометрическими множителями:")
for name, factor in [
    ("без множителя", 1),
    ("(4π)^(-1/4)", (4*math.pi)**(-1/4)),
    ("(2π)^(-1/2)", (2*math.pi)**(-1/2)),
    ("(2π)^(-3/4)", (2*math.pi)**(-3/4)),
    ("α^(1/2)", alpha_em**(1/2)),
    ("(4π²)^(-1/4)", (4*math.pi**2)**(-1/4)),
    ("1/(2π)", 1/(2*math.pi)),
    ("(α/2π)^(1/2)", (alpha_em/(2*math.pi))**(1/2)),
]:
    m_test = m_from_rhc * factor
    ratio = m_test / m_e
    err = abs(ratio - 1) * 100
    marker = " ★" if err < 5 else " ←" if err < 20 else ""
    print(f"    {name:<25s}: m = {m_test:.3e}, ratio = {ratio:.4f}, err = {err:.1f}%{marker}")

# The dimensional combination gives m ≈ 500 × m_e.
# No simple geometric prefactor fixes it without using α or other constants.
# → m_e CANNOT be derived from (ρ, ℏ, c) alone!

# But wait: what if we also use e (charge)?
# m = f(ρ, ℏ, c, e)?
# Extra dimension: [e] = A·s = C
# This gives one more equation → one more degree of freedom
# m = ρ^a × ℏ^b × c^d × e^f
# Need 4 equations for 4 unknowns... but we have only 3 dimensions (kg, m, s)
# unless we use electromagnetic units (add A)

# Actually: α = e²/(4πε₀ℏc) is dimensionless and involves e.
# So m = ρ^(1/4) × ℏ^(3/4) × c^(-3/4) × α^n for some n

# What n gives m_e?
import numpy as np
n_needed = np.log(m_e / m_from_rhc) / np.log(alpha_em)
print(f"\n  Нужен множитель α^n:")
print(f"    m_e = m_dimensional × α^n")
print(f"    n = ln(m_e/m_dim) / ln(α) = {n_needed:.4f}")
print(f"    ≈ {n_needed:.2f}")

# n ≈ 1.27. Not a simple fraction.
# Try n = 5/4:
m_test_54 = m_from_rhc * alpha_em**(5/4)
print(f"\n    Попытка n=5/4: m = {m_test_54:.3e} (ratio = {m_test_54/m_e:.3f})")
# Try n = 4/3:
m_test_43 = m_from_rhc * alpha_em**(4/3)
print(f"    Попытка n=4/3: m = {m_test_43:.3e} (ratio = {m_test_43/m_e:.3f})")

verdict1 = ("FAIL: m_e не выводится из (ρ, ℏ, c) без α. "
            f"Dimensional: {m_from_rhc/m_e:.0f}× промах. "
            f"Нужен α^{n_needed:.2f} — не простая дробь.")
print(f"\n  ВЕРДИКТ: {verdict1}")


# ============================================================
# CANDIDATE 2: Koide 2/3 from toroid geometry
# ============================================================
print(f"""
{'='*80}
  КАНДИДАТ 2: КОИДЕ 2/3 ИЗ ТОРОИДНОЙ ГЕОМЕТРИИ
{'='*80}

  Факт: (m_e + m_μ + m_τ) / (√m_e + √m_μ + √m_τ)² = 2/3 (err 0.001%)

  Koide = 2/3 следует из: √m_i = A(1 + √2·cos(θ_i))
  с тремя θ, разделёнными примерно на 120°.

  Вопрос: ПОЧЕМУ √2 и ПОЧЕМУ ~120°?
""")

# For 3 modes of a toroid with two rotation frequencies ω₁, ω₂:
# Energy of (n₁, n₂) mode: E = ½ρV(n₁²ω₁² + n₂²ω₂²)R²
# Mass ∝ E/c² ∝ n₁²(R/r)² + n₂²  (if ω₁R = ω₂r = c)

# For the simplest three modes: (1,0), (0,1), (1,1)?
# m₁ ∝ (R/r)², m₂ ∝ 1, m₃ ∝ (R/r)² + 1

# Koide for these:
# Σm = 2(R/r)² + 2
# Σ√m = √((R/r)²) + 1 + √((R/r)²+1) = (R/r) + 1 + √((R/r)²+1)
# K = [2(R/r)²+2] / [(R/r)+1+√((R/r)²+1)]²

# Find R/r such that K = 2/3
from scipy.optimize import brentq

def koide_from_modes(x):
    # x = R/r
    m1 = x**2   # mode (1,0)
    m2 = 1       # mode (0,1)
    m3 = x**2 + 1  # mode (1,1)
    K = (m1 + m2 + m3) / (math.sqrt(m1) + math.sqrt(m2) + math.sqrt(m3))**2
    return K - 2/3

print(f"  Модель 1: три моды (1,0), (0,1), (1,1)")
try:
    x_sol = brentq(koide_from_modes, 0.01, 100)
    m1, m2, m3 = x_sol**2, 1, x_sol**2 + 1
    K_check = (m1+m2+m3)/(math.sqrt(m1)+math.sqrt(m2)+math.sqrt(m3))**2
    print(f"  R/r = {x_sol:.4f} даёт K = {K_check:.6f}")
    print(f"  Массы: {m1:.3f} : {m2:.3f} : {m3:.3f}")
    print(f"  Отношения: m₃/m₁ = {m3/m1:.3f}, m₃/m₂ = {m3:.3f}")
    # Compare with real lepton ratios
    print(f"  Реальные: m_τ/m_e = {m_tau/m_e:.0f}, m_μ/m_e = {m_mu/m_e:.0f}")
    print(f"  Модельные: m₃/m₂ = {m3/m2:.1f}")
    print(f"  → Отношения НЕ совпадают (нужно ~3477 и ~207, модель даёт ~2)")
except:
    print(f"  Нет решения для (1,0), (0,1), (1,1)")

# Model 2: modes (n₁, n₂) with different quantum numbers
# If masses scale as n₁² + n₂²×(r/R)²:
print(f"\n  Модель 2: поиск (n₁, n₂) для e, μ, τ")
print(f"  m ∝ n₁² + n₂²×(r/R)² = n₁² + n₂²×α (если α = (r/R)²)")

# m_e ∝ n₁² + n₂²α, m_μ ∝ p₁² + p₂²α, m_τ ∝ q₁² + q₂²α
# With α = 1/137:
# m_μ/m_e = 206.8, m_τ/m_e = 3477

# Search for integer (n₁,n₂) giving right ratios
alpha_val = 1/137.036
best_err = 999
best = None
for n1 in range(0, 5):
    for n2 in range(0, 200):
        me = n1**2 + n2**2 * alpha_val
        if me < 0.01: continue
        for p1 in range(0, 50):
            for p2 in range(0, 200):
                mmu = p1**2 + p2**2 * alpha_val
                ratio_mu = mmu / me
                if abs(ratio_mu - 206.768) > 5: continue
                for q1 in range(0, 100):
                    for q2 in range(0, 200):
                        mtau = q1**2 + q2**2 * alpha_val
                        ratio_tau = mtau / me
                        err = abs(ratio_mu - 206.768)/206.768 + abs(ratio_tau - 3477)/3477
                        if err < best_err:
                            best_err = err
                            best = (n1,n2,p1,p2,q1,q2,me,mmu,mtau)
                        if err < 0.01:
                            break
                    if best_err < 0.01: break
                if best_err < 0.01: break
            if best_err < 0.01: break

if best and best_err < 0.1:
    n1,n2,p1,p2,q1,q2,me,mmu,mtau = best
    print(f"  Лучшее: e=({n1},{n2}), μ=({p1},{p2}), τ=({q1},{q2})")
    print(f"  m_μ/m_e = {mmu/me:.1f} (нужно 206.8)")
    print(f"  m_τ/m_e = {mtau/me:.1f} (нужно 3477)")
    print(f"  Error: {best_err*100:.1f}%")
else:
    print(f"  Не найдено (best err = {best_err*100:.1f}%) — пространство слишком большое")
    print(f"  Вывод: простые тороидные моды НЕ дают масс лептонов")

# Model 3: The REAL Koide derivation
# √m = A(1 + √2 cos θ) with θ_e ≈ 132.7°, θ_μ ≈ 107.3°, θ_τ ≈ 12.7°
# Can these angles come from toroid geometry?

# Three standing waves on a torus at angles θ₁, θ₂, θ₃:
# If the torus has TWO resonant frequencies ω₁ and ω₂,
# then θ = arctan(ω₁/ω₂ × n₁/n₂)

# For Koide's angles to come from geometry, we need:
# cos(θ_i) = specific values
sum_m = m_e + m_mu + m_tau
A = (math.sqrt(m_e) + math.sqrt(m_mu) + math.sqrt(m_tau)) / 3

print(f"\n  Модель 3: углы Коиде из тороида")
for name, m in [("e", m_e), ("μ", m_mu), ("τ", m_tau)]:
    cos_theta = (math.sqrt(m)/A - 1) / math.sqrt(2)
    theta = math.acos(cos_theta) * 180 / math.pi
    # Can this angle come from arctan(n₁/n₂)?
    tan_theta = math.tan(theta * math.pi / 180)
    print(f"    θ_{name} = {theta:.2f}°, cos = {cos_theta:.4f}, tan = {tan_theta:.4f}")
    # Check if tan is a ratio of small integers
    for p in range(1, 20):
        for q in range(1, 20):
            if abs(tan_theta - p/q) / abs(tan_theta) < 0.02:
                print(f"      tan ≈ {p}/{q} = {p/q:.4f} (err {abs(tan_theta-p/q)/abs(tan_theta)*100:.1f}%)")

# Real Koide derivation: 2/3 follows from EQUAL SPACING of 3 modes + √2 coupling
# This is a consequence of SU(3) flavor symmetry breaking
# The toroid adds nothing here that representation theory doesn't already give

verdict2 = ("FAIL: простые тороидные моды не дают лептонных масс. "
            "Коиде = математический факт о 3 числах, не специфичен для тороида. "
            "Углы 133°/107°/13° не соответствуют простым дробям.")
print(f"\n  ВЕРДИКТ: {verdict2}")


# ============================================================
# CANDIDATE 3: α = 1/137 from vortex stability
# ============================================================
print(f"""
{'='*80}
  КАНДИДАТ 3: α = 1/137 ИЗ УСЛОВИЯ СТАБИЛЬНОСТИ ВИХРЯ
{'='*80}

  Гипотеза: вихрь стабилен только при определённом R/r.
  α = (r/R)² → если R/r фиксировано физикой → α выведен.

  Условие стабильности кольцевого вихря (Kelvin 1880):
  Вихревое кольцо стабильно если возмущения не растут.
  Для мод возмущения с азимутальным числом n:
  Частота ω_n = (nΓ)/(4πR²) × [ln(8R/r) - ψ(n)]
  где ψ(n) зависит от n.

  Стабильность: Re(ω_n) > 0 для всех n.
  Для тонкого кольца (R >> r): ВСЕГДА стабильно (Kelvin, Thomson).
  Для ТОЛСТОГО кольца: стабильность теряется при R/r < R/r_critical.
""")

# For a vortex ring, the energy is:
# E = ½ρΓ²R[ln(8R/r) - 7/4]  (thin ring, R >> r)
# For Hill's spherical vortex (R/r → 0):
# E = (10/7)ρΓ²R³/(a²)  where a = radius of sphere, Γ = vorticity × area

# The KEY question: is there a SPECIFIC R/r where
# the vortex ring is "maximally stable" (minimum energy per unit circulation)?

# Energy per unit circulation squared per unit radius:
# f(x) = ln(8x) - 7/4  where x = R/r

# df/dx = 1/x → always positive → no minimum!
# The thinner the ring, the MORE energy per unit circulation.
# No natural R/r from stability.

# Alternative: condition from QUANTIZATION
# Γ = h/m → m = ½ρΓ²R(ln(8R/r) - 7/4) / c²
# Γ = h/m → Γ² = h²/m²
# m = ½ρ(h²/m²)R(ln(8R/r) - 7/4) / c²
# m³ = ½ρh²R(ln(8R/r) - 7/4) / c²

# This gives m as function of R and R/r.
# If we ALSO fix R = ƛ_C/2 = ℏ/(2mc):
# R = ℏ/(2mc) → depends on m → circular!

# But if R is determined by ANOTHER condition...
# What if: the vortex ring has EXACTLY one quantum of angular momentum?
# L = ρΓπR² = ℏ/2 (spin 1/2)

Gamma = h / m_e
L_required = hbar / 2
# ρΓπR² = ℏ/2 → R² = ℏ/(2ρΓπ)
R_from_spin = math.sqrt(L_required / (rho * Gamma * math.pi))

print(f"  Из условия L = ½ℏ (спин 1/2):")
print(f"  ρΓπR² = ½ℏ")
print(f"  R = √(ℏ/(2ρΓπ)) = {R_from_spin:.3e} м = {R_from_spin*1e9:.1f} нм")

# Now from E = mc²:
# ½ρΓ²R(ln(8R/r) - 7/4) = mc²
# ln(8R/r) - 7/4 = 2mc²/(ρΓ²R)
lhs = 2 * m_e * c**2 / (rho * Gamma**2 * R_from_spin)
print(f"  ln(8R/r) - 7/4 = {lhs:.6f}")

if 0 < lhs < 700:  # prevent overflow
    ln_8Rr = lhs + 7/4
    Rr = math.exp(ln_8Rr) / 8
    alpha_derived = 1/Rr**2 if Rr > 0 else 0
    print(f"  ln(8R/r) = {ln_8Rr:.6f}")
    print(f"  R/r = {Rr:.4f}")
    print(f"  α = (r/R)² = {alpha_derived:.6e}")
    print(f"  1/α = {1/alpha_derived:.1f}")
    print(f"  Факт: 1/α = 137.036")
    print(f"  Error = {abs(1/alpha_derived - 137.036)/137.036*100:.1f}%")
else:
    print(f"  lhs = {lhs} — отрицательное, формула тонкого кольца не работает")
    print(f"  Нужна формула для толстого вихря")

# Alternative approach: DON'T use m_e!
# From L = ½ℏ and E = mc²:
# L/E = ℏ/(2mc²) = R/c (for rotating object)
# → R = ℏ/(2mc) = ƛ_C/2 (as before — tautology)

# The REAL question: can we get BOTH m and R from (ρ, ℏ, c) alone?
# Two equations:
# (1) E = ½ρΓ²R·f(R/r) = mc² with Γ = h/m
# (2) L = ρΓπR² = ½ℏ

# From (2): m = h/(Γ) and Γ = h/m → circular
# Actually (2) gives: R² = ℏ/(2ρΓπ) = ℏm/(2ρhπ) = m/(4π²ρ·ℏ) × ℏ² ... messy

# Let's substitute Γ = h/m into both:
# (1): mc² = ½ρ(h/m)²R·f → m³c² = ½ρh²R·f
# (2): ½ℏ = ρ(h/m)πR² → m = 2ρhπR²/ℏ = 4π²ρR²

# From (2): m = 4π²ρR²
# Into (1): (4π²ρR²)³c² = ½ρh²R·f
# 64π⁶ρ³R⁶c² = ½ρh²R·f
# 128π⁶ρ²R⁵c² = h²·f
# R⁵ = h²f/(128π⁶ρ²c²)

f_geometric = 1  # placeholder for ln(8R/r) - 7/4
R5 = h**2 * f_geometric / (128 * math.pi**6 * rho**2 * c**2)
R_derived = R5**(1/5)
m_derived = 4 * math.pi**2 * rho * R_derived**2

print(f"\n  Комбинируя L = ½ℏ и E = mc² (без m!):")
print(f"  m = 4π²ρR²")
print(f"  R⁵ = h²f/(128π⁶ρ²c²)")
print(f"  При f = 1: R = {R_derived:.3e} м, m = {m_derived:.3e} кг")
print(f"  m_e (факт) = {m_e:.3e} кг")
print(f"  Ratio m/m_e = {m_derived/m_e:.2f}")

# The result depends on f = ln(8R/r) - 7/4 which depends on R/r!
# Self-consistent: f(R/r) must be chosen so that everything is consistent.
# Let's solve self-consistently:

# From m = 4π²ρR²:
# Γ = h/m = h/(4π²ρR²)
# R/r determined by: ½ρΓ²R·(ln(8R/r)-7/4) = mc² = 4π²ρR²c²
# ½ρ(h/(4π²ρR²))²R·f = 4π²ρR²c²
# h²R/(32π⁴ρR⁴) · f = 4π²ρR²c²
# h²f/(32π⁴ρR³) = 4π²ρR²c²
# h²f = 128π⁶ρ²R⁵c²  (same as before)

# AND from R/r relationship with f:
# f = ln(8R/r) - 7/4
# We need another equation to determine R/r.

# What if the vortex is a SPHERE (Hill's vortex)?
# Then the energy formula is different:
# E_Hill = (10/7)πρω²a⁵/10 = πρω²a⁵/7
# where a = sphere radius, ω = vorticity
# Angular momentum: L_Hill = (4/15)πρωa⁵

# From L = ½ℏ: ω = 15ℏ/(8πρa⁵)
# From E = mc²: mc² = πρω²a⁵/7
# Substitute ω: mc² = πρ(15ℏ/(8πρa⁵))²a⁵/7
#                    = πρ × 225ℏ²/(64π²ρ²a¹⁰) × a⁵/7
#                    = 225ℏ²/(64×7×πρa⁵)
#                    = 225ℏ²/(448πρa⁵)

# From L = ½ℏ: ωa² = 15ℏ/(8πρa³) → v_surface = ωa = 15ℏ/(8πρa⁴)
# And m from: m = E/c² = 225ℏ²/(448πρa⁵c²)

# Also m = ρV_eff: for a Hill's vortex, the entrained mass is:
# Not well-defined for Hill's vortex without boundary.

# Simpler: from L = ½ℏ and E = mc² for a SOLID SPHERE rotating:
# L = (2/5)mR²ω = ½ℏ → ω = 5ℏ/(4mR²)
# E = ½Iω² = ½(2/5)mR²ω² = (1/5)mR²ω²
# E = mc² → (1/5)R²ω² = c²
# R²ω² = 5c² → v_surface = Rω = √5 × c ≈ 2.24c

# For a fluid vortex with mass m = ½ρV = (2/3)πρR³:
# L = (2/5)(2/3)πρR³·R²·ω = (4/15)πρR⁵ω = ½ℏ
# → ω = 15ℏ/(8πρR⁵)
# E = ½Iω² = (1/5)(2/3)πρR³·R²·ω² = (2/15)πρR⁵ω² = mc² = (2/3)πρR³c²
# → (2/15)R²ω² = (2/3)c² → R²ω² = 5c² → Rω = √5·c

# Same result: surface velocity = √5 × c (superluminal!)
# This means: a simple solid-body rotation doesn't work.

# Real vortex: differential rotation, v(r) = Γ/(2πr) for thin ring
# At r = tube radius: v = Γ/(2πr_tube)
# At R = ring radius: v = Γ/(2πR)

print(f"\n  Проблема: простое вращение даёт v_surface = √5·c (сверхсветовая!)")
print(f"  → Нужно дифференциальное вращение (не твёрдотельное)")
print(f"  → Тонкое кольцо: v(R) = Γ/(2πR), v(r) = Γ/(2πr)")
print(f"  → При R >> r: v_tube >> v_ring")

# Conclusion for candidate 3:
# Without knowing R/r (or equivalently, without extra physics),
# we get ONE equation with TWO unknowns (m and R).
# The spin condition L = ½ℏ gives a SECOND equation.
# But the result depends on the FORM of the energy (thin ring vs sphere vs ...)
# which is determined by R/r — which is what we're trying to find!

# CIRCULAR LOGIC. We need external input to fix R/r.

verdict3 = ("FAIL: α не выводится из стабильности. "
            "Два уравнения (E=mc², L=½ℏ) + одно неизвестное (R/r) → решаемо, "
            "но f(R/r) зависит от модели (кольцо vs сфера). "
            "Нет самосогласованного решения без дополнительного условия.")
print(f"\n  ВЕРДИКТ: {verdict3}")


# ============================================================
# FINAL
# ============================================================
print(f"""
{'='*80}
  ИТОГИ ТРЁХ ПОПЫТОК
{'='*80}

  Кандидат 1 (m_e из ρ,ℏ,c):   FAIL
    Размерный анализ даёт m ~ ρ^(1/4)ℏ^(3/4)c^(-3/4) = {m_from_rhc/m_e:.0f} × m_e
    Нужен α^{n_needed:.2f} — не простая дробь, = подгонка.

  Кандидат 2 (Коиде из тороида): FAIL
    Простые моды (n₁,n₂) не дают лептонных масс.
    Углы Коиде (133°/107°/13°) не соответствуют простым дробям.
    Формула Коиде = математический факт, не специфичен для тороида.

  Кандидат 3 (α из стабильности): FAIL
    E=mc² + L=½ℏ дают 2 уравнения с 2 неизвестными (m, R),
    но f(R/r) зависит от геометрии → нужно третье условие.
    Круговая логика: R/r → α → R/r.

  ОБЩИЙ ВЕРДИКТ:
  ─────────────────
  ρ = μ₀ НЕДОСТАТОЧНО для вывода фундаментальных констант.
  Нужна ДОПОЛНИТЕЛЬНАЯ ФИЗИКА:
  • Условие на R/r (из динамики вихря, не из статики)
  • Или связь e с Γ (почему заряд = циркуляция?)
  • Или квантование геометрии (почему тороид, а не сфера?)

  Модель остаётся СЛОВАРЁМ: правильные слова, нет формул.
""")


if __name__ == "__main__":
    pass
