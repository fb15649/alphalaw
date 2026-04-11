"""
Compressible ether vortex: can finite K fix the electron mass?

Incompressible model: E = ½ρv²V (kinetic only) → m_e doesn't come out.
Compressible model: E = ½ρv²V + ½(Δρ)²c_L²V/ρ (kinetic + compression)

Inside a vortex, the centripetal acceleration creates a pressure DROP
(Bernoulli). If ether is compressible (finite K), this pressure drop
creates a DENSITY CHANGE inside the vortex core:

  Δρ/ρ = -v²/(2c_L²) = -v²ρ/(2K)

This compressed/rarefied core has additional elastic energy:
  E_compression = ½K(Δρ/ρ)²V = ½K(v⁴ρ²/(4K²))V = ρv⁴V/(8K)

Total: E = ½ρv²V + ρv⁴V/(8K) = ½ρv²V × [1 + v²/(4K/ρ)]
     = ½ρv²V × [1 + v²/(4c_L²)]

This changes the mass formula!
"""
import math
import numpy as np

# Constants
c = 2.99792458e8
h = 6.62607015e-34
hbar = h / (2 * math.pi)
e_charge = 1.602176634e-19
mu_0 = 4e-7 * math.pi
epsilon_0 = 8.8541878128e-12
m_e_exp = 9.1093837015e-31
alpha_exp = 1 / 137.035999166

rho = mu_0
G_shear = rho * c**2

print("=" * 80)
print("  СЖИМАЕМЫЙ ЭФИР: E = ½ρv²V × [1 + v²/(4c_L²)]")
print(f"  ρ = {rho:.4e}, c = {c:.3e}, G = {G_shear:.3e}")
print("=" * 80)

# ============================================================
# Model: vortex ring with v_tube = v (variable, not necessarily c)
#
# Energy: E = ½ρv²V × [1 + v²/(4c_L²)]
# Set E = mc²:
#   mc² = ½ρv²V[1 + v²/(4c_L²)]
#
# Volume: V = 2π²Rr² (toroid)
# Circulation: Γ = 2πr × v (velocity × circumference of tube)
# Quantized: Γ = h/m
# → r = Γ/(2πv) = h/(2πmv)
#
# Angular momentum: L = ρΓπR² = ½ℏ (spin ½)
# → R² = ℏ/(2ρΓπ) = ℏm/(2ρhπ) = m/(4π²ρhbar)...
#   Wait: Γ = h/m, so R² = ℏ/(2ρ(h/m)π) = ℏm/(2ρhπ) = m/(4π²ρ)×(ℏ/ℏ)
#   R² = ℏm/(2πρh) = m/(4π²ρ) ... hmm
#
# Let me be more careful:
# L = ρΓπR² = ½ℏ
# Γ = h/m
# R² = ℏ/(2ρΓπ) = ℏ/(2ρπ × h/m) = ℏm/(2πρh) = m/(2πρ × 2π) = m/(4π²ρ)
#
# Actually: ℏ/(2ρΓπ) = ℏ/(2ρπ(h/m)) = ℏm/(2πρh) = m/(2π×2πρ) = m/(4π²ρ)
# since ℏ/h = 1/(2π)
#
# So: R² = m/(4π²ρ)
# R = √(m/(4π²ρ)) = (1/(2π))√(m/ρ)
#
# And: r = h/(2πmv) = ℏ/(mv)
#
# Volume: V = 2π²Rr² = 2π²(1/(2π))√(m/ρ) × ℏ²/(m²v²)
#        = π√(m/ρ) × ℏ²/(m²v²)
#        = πℏ²/(m^(3/2) × v² × ρ^(1/2))
#
# Energy equation:
# mc² = ½ρv² × V × [1 + v²/(4c_L²)]
# mc² = ½ρv² × πℏ²/(m^(3/2)v²ρ^(1/2)) × [1 + v²/(4c_L²)]
# mc² = ½ × ρ^(1/2) × πℏ² / m^(3/2) × [1 + v²/(4c_L²)]
# m^(5/2) c² = ½ π ℏ² ρ^(1/2) × [1 + v²/(4c_L²)]
# m^(5/2) = πℏ²ρ^(1/2) / (2c²) × [1 + v²/(4c_L²)]
# ============================================================

print(f"""
  4 уравнения:
  (1) Γ = h/m                    (квантование циркуляции)
  (2) L = ρΓπR² = ½ℏ            (спин ½)
  (3) v_tube = Γ/(2πr)           (скорость в трубке)
  (4) E = ½ρv²V[1+v²/(4c_L²)] = mc²  (энергия = масса)

  Из (1)+(2): R = √(m/(4π²ρ))
  Из (1)+(3): r = ℏ/(mv)

  Подставляя в (4):
  m^(5/2) = πℏ²√ρ / (2c²) × [1 + v²/(4c_L²)]
""")

# Case 1: Incompressible (K = ∞, c_L = ∞)
m_incomp = (math.pi * hbar**2 * math.sqrt(rho) / (2 * c**2))**(2/5)
print(f"  Случай 1: K = ∞ (несжимаемый)")
print(f"    m = [πℏ²√ρ/(2c²)]^(2/5) = {m_incomp:.4e} кг")
print(f"    m/m_e = {m_incomp/m_e_exp:.6f}")
print(f"    Error = {abs(m_incomp/m_e_exp - 1)*100:.1f}%")

# R/r for this mass
R_incomp = math.sqrt(m_incomp / (4 * math.pi**2 * rho))
r_incomp = hbar / (m_incomp * c)  # if v = c
Rr_incomp = R_incomp / r_incomp if r_incomp > 0 else 0
print(f"    R = {R_incomp:.3e} м, r(v=c) = {r_incomp:.3e} м, R/r = {Rr_incomp:.2f}")

# Case 2: Compressible — scan over c_L and v
print(f"\n  Случай 2: K конечен → ищем (v, c_L) дающие m = m_e")

# m^(5/2) = πℏ²√ρ/(2c²) × [1 + v²/(4c_L²)]
# At m = m_e:
target_lhs = m_e_exp**(5/2)
base_rhs = math.pi * hbar**2 * math.sqrt(rho) / (2 * c**2)

# Required correction factor:
correction_needed = target_lhs / base_rhs
print(f"    m_e^(5/2) = {target_lhs:.4e}")
print(f"    πℏ²√ρ/(2c²) = {base_rhs:.4e}")
print(f"    Нужный множитель: [1 + v²/(4c_L²)] = {correction_needed:.4e}")

# This means: v²/(4c_L²) = correction_needed - 1
corr_minus_1 = correction_needed - 1
print(f"    v²/(4c_L²) = {corr_minus_1:.4e}")

# If v = c: c²/(4c_L²) = correction → c_L² = c²/(4×correction)
if corr_minus_1 > 0:
    cL_needed_v_c = c / (2 * math.sqrt(corr_minus_1))
    K_needed_v_c = cL_needed_v_c**2 * rho
    print(f"\n    При v = c:")
    print(f"      c_L = c/(2√({corr_minus_1:.2e})) = {cL_needed_v_c:.3e} м/с")
    print(f"      c_L/c = {cL_needed_v_c/c:.3e}")
    print(f"      K = ρc_L² = {K_needed_v_c:.3e} Па")
    print(f"      K/G = {K_needed_v_c/G_shear:.3e}")

    # Check: is this c_L reasonable?
    if cL_needed_v_c > c:
        print(f"      c_L > c ✓ (сверхсветовые продольные волны)")
    else:
        print(f"      c_L < c ✗ (медленнее света — не физично)")

# What if v ≠ c? Scan v:
print(f"\n  Скан по v (скорость вращения в трубке):")
print(f"  {'v/c':<8s} {'v²/(4c_L²)':<15s} {'c_L/c':<10s} {'K/G':<10s} {'K (Па)':<12s}")
print("  " + "-" * 60)

for v_over_c in [0.001, 0.01, 0.1, 0.5, 1.0, 10, 100, 1000]:
    v = v_over_c * c
    # m^(5/2) = base × [1 + v²/(4c_L²)]
    # But with v ≠ c, the formula changes because r = ℏ/(mv) not ℏ/(mc)
    # Recalculate:
    # r = ℏ/(mv), R = √(m/(4π²ρ)), V = 2π²Rr² = πℏ²/(m^(3/2)v²ρ^(1/2))
    # E = ½ρv²V[1+v²/(4c_L²)] = mc²
    # ½ρv² × πℏ²/(m^(3/2)v²ρ^(1/2)) × [1+v²/(4c_L²)] = mc²
    # πℏ²ρ^(1/2)/(2m^(3/2)) × [1+v²/(4c_L²)] = mc²
    # Same formula! v cancels out from kinetic term!
    # m^(5/2) = πℏ²√ρ/(2c²) × [1 + v²/(4c_L²)]

    # So the correction depends on v²/c_L².
    # For m = m_e: 1 + v²/(4c_L²) = correction_needed
    # v²/(4c_L²) = correction_needed - 1
    # c_L = v / (2√(correction_needed - 1))

    if corr_minus_1 > 0:
        cL = v / (2 * math.sqrt(corr_minus_1))
        K = cL**2 * rho
        print(f"  {v_over_c:<8.3f} {corr_minus_1:<15.3e} {cL/c:<10.3e} "
              f"{K/G_shear:<10.3e} {K:<12.3e}")

# WAIT — v CANCELS from the kinetic term. The correction [1+v²/(4c_L²)]
# depends on v and c_L independently. So we have TWO unknowns (v and c_L)
# but need correction = constant. This means:
# v = 2c_L × √(correction_needed - 1)
# Any (v, c_L) satisfying this relation gives m = m_e.

print(f"\n  КЛЮЧЕВОЕ: v сокращается из кинетической энергии!")
print(f"  Единственное условие: v²/(4c_L²) = {corr_minus_1:.3e}")
print(f"  → v/c_L = {2*math.sqrt(corr_minus_1):.3e}")
print(f"  → v = {2*math.sqrt(corr_minus_1):.3e} × c_L")

# Physical constraint: v < c_L (rotation speed < sound speed, otherwise shock)
# If v < c_L: v/c_L < 1 → 2√(corr-1) < 1 → corr < 1.25
# Our correction = {correction_needed} — is it < 1.25?
print(f"\n  Ограничение v < c_L: нужно {2*math.sqrt(corr_minus_1):.3e} < 1")
print(f"  → correction < 1.25")
print(f"  Наше correction = {correction_needed:.3e}")
print(f"  → {'ВЫПОЛНЕНО' if correction_needed < 1.25 else 'НЕ ВЫПОЛНЕНО'}")

# Let's check: what if we DON'T require L = ½ℏ?
# Without spin condition, we lose R equation.
# Instead: what if the vortex chooses v and R/r to MINIMIZE energy
# at fixed Γ and L? This is a variational problem.

print(f"\n{'='*80}")
print(f"  АЛЬТЕРНАТИВА: вариационный принцип")
print(f"{'='*80}")

# For fixed Γ = h/m and fixed spin L = ½ℏ:
# E(v) = ½ρv²V[1 + v²/(4c_L²)] — minimize over v at fixed Γ, L

# V = 2π²Rr² with R = √(m/(4π²ρ)), r = Γ/(2πv) = h/(2πmv)
# V = 2π² × √(m/(4π²ρ)) × (h/(2πmv))²
# V = 2π² × √m/(2πρ^(1/2)) × h²/(4π²m²v²)
# V = h²/(4π²m^(3/2)v²ρ^(1/2)) × ... let me just compute E(v) numerically

# E = πℏ²ρ^(1/2)/(2m^(3/2)) × [1 + v²/(4c_L²)]
# This is INCREASING in v² — so minimum is at v = 0!
# But v = 0 means r = ∞ — no vortex.

# The REAL minimum comes from the full Kelvin energy for finite R/r:
# E = ½ρΓ²R[ln(8R/r) - 7/4] — which has a DIFFERENT structure.

# For compressible case with Kelvin formula:
# E = ½ρΓ²R[ln(8R/r) - 7/4] + compression_energy
# compression_energy depends on pressure distribution inside tube

print(f"""
  Проблема: E ∝ [1 + v²/(4c_L²)] — РАСТЁТ с v.
  Минимум при v = 0 → нет вихря.
  Значит простая формула E = ½ρv²V[1+v²/(4c_L²)] неполна.

  Нужна ПОЛНАЯ энергия Кельвина для сжимаемого вихря.
  Это сложная задача (Saffman, Vortex Dynamics, 1992).

  Но ключевой результат уже получен:
""")

# KEY RESULT: what K is needed?
print(f"  КЛЮЧЕВОЙ РЕЗУЛЬТАТ:")
print(f"  ─────────────────────")
print(f"  Для m = m_e нужен множитель {correction_needed:.3e}")
print(f"  При ρ = μ₀: m_incompressible = {m_incomp:.3e} кг (в {m_e_exp/m_incomp:.0f}× меньше m_e)")
print(f"")
print(f"  correction = (m_e/m_incomp)^(5/2) = {(m_e_exp/m_incomp)**2.5:.3e}")
print(f"")
print(f"  Это {correction_needed:.0e} — ОГРОМНЫЙ множитель.")
print(f"  v²/(4c_L²) ≈ {corr_minus_1:.0e}")
print(f"  → v ≈ {math.sqrt(4*corr_minus_1):.0e} × c_L")
print(f"")
print(f"  Если c_L = 10⁶c (из запутанности): v = {math.sqrt(4*corr_minus_1) * 1e6 * c:.0e} м/с")
print(f"  v/c = {math.sqrt(4*corr_minus_1) * 1e6:.0e}")
print(f"  → v >> c — сверхсветовая скорость вращения!")
print(f"")
print(f"  ВЫВОД: сжимаемость НЕ СПАСАЕТ модель.")
print(f"  Для m_e нужно v >> c в трубке вихря.")
print(f"  Это нефизично в рамках нашей модели (v ≤ c).")
print(f"")
print(f"  КОРНЕВАЯ ПРОБЛЕМА:")
print(f"  ρ = μ₀ = {rho:.2e} кг/м³ — слишком мало.")
print(f"  Для m_e = {m_e_exp:.2e} кг нужно или:")
print(f"    а) ρ >> μ₀ (плотность эфира = другое число)")
print(f"    б) v >> c (сверхсветовое вращение)")
print(f"    в) Энергия связи (не кинетическая!) доминирует")
print(f"    г) Электрон — НЕ один вихрь, а состоящая структура")


if __name__ == "__main__":
    pass
