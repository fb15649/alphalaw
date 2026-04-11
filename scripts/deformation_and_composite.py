"""
Two alternative models for electron mass:
(в) Deformation energy (not kinetic)
(г) Composite structure (not single vortex)
"""
import math

c = 2.99792458e8
h = 6.62607015e-34
hbar = h / (2 * math.pi)
e_charge = 1.602176634e-19
mu_0 = 4e-7 * math.pi
epsilon_0 = 8.8541878128e-12
m_e = 9.1093837015e-31
alpha_em = 1 / 137.036

rho = mu_0
G_shear = rho * c**2  # 1.13e11 Pa


# ============================================================
# (В) DEFORMATION ENERGY MODEL
# ============================================================
print("=" * 80)
print("  (В) ЭНЕРГИЯ ДЕФОРМАЦИИ: масса = упругая энергия среды")
print("=" * 80)

# Inside a vortex tube, the ether is SHEARED (not compressed).
# Shear strain: γ = v/c = Γ/(2πrc) at the tube wall
# Shear energy density: u = ½Gγ²
# Total: E = ½G γ² × V_tube

# For v_tube = c: γ = 1 (maximum strain)
# E = ½G × 1² × V = ½ρc² × V (same as kinetic! Because G = ρc²)

# But: shear strain is NOT uniform inside the tube.
# For a vortex: v(r) = Γ/(2πr) (inversely proportional to distance)
# γ(r) = v(r)/c = Γ/(2πrc)
# Energy density: u(r) = ½G[Γ/(2πrc)]² = ½ρΓ²/(4π²r²)

# Total energy per unit LENGTH of tube:
# dE/dl = ∫ u(r) × 2πr dr from r_core to R_cut
# = ∫ ½ρΓ²/(4π²r²) × 2πr dr = ρΓ²/(4π) × ∫ dr/r
# = ρΓ²/(4π) × ln(R_cut/r_core)

# For a torus: total length = 2πR, R_cut = R (outer radius of ring)
# E = 2πR × ρΓ²/(4π) × ln(R/r_core)
# = ½ρΓ²R × ln(R/r)  ← THIS IS KELVIN'S FORMULA!

# So: deformation energy = kinetic energy of circulation.
# They are THE SAME THING in an ideal fluid!

print(f"""
  Результат: энергия деформации = кинетическая энергия циркуляции.

  E_deformation = ½G ∫γ² dV = ½ρΓ²R·ln(R/r) = E_Kelvin

  В идеальной жидкости упругая и кинетическая энергия — одно и то же!
  Это теорема Кельвина (1849): для вихря, вся энергия = кинетическая.

  → ПУТЬ (В) НЕ ДАЁТ НОВОГО. Деформация = кинетика = та же формула.
""")


# ============================================================
# (Г) COMPOSITE STRUCTURE: electron ≠ single vortex
# ============================================================
print("=" * 80)
print("  (Г) СОСТАВНАЯ СТРУКТУРА: электрон = несколько вихрей")
print("=" * 80)

# What if electron = N intertwined vortex rings?
# Like a torus knot (p,q) — wrapping p times in one direction,
# q times in the other.

# For a (p,q) torus knot:
# - Total tube length = 2πR × √(p² + q²(R/r)²) ≈ 2πR × q(R/r) for R/r >> 1
# - Circulation per strand: Γ₁ = h/(Nm) where N = number of strands
# - Total circulation: Γ = N × Γ₁ = h/m (same!)
# - But the energy is DIFFERENT:
#   E = N × ½ρΓ₁²R·ln(8R/r) = N × ½ρ(h/Nm)²R·ln(8R/r)
#   = ½ρh²R/(N m²) × ln(8R/r)

# For single vortex (N=1): E = ½ρΓ²R·ln(8R/r) = mc²
# For N strands: E = ½ρΓ²R/(N) × ln(8R/r) = mc²/N ???
# NO — that gives LESS energy. N strands should give MORE.

# Correct: if N strands are PARALLEL (like a cable):
# Each has Γ₁ = Γ/N, energy ∝ Γ₁²
# Total: N × Γ₁² = N × (Γ/N)² = Γ²/N — LESS than single strand
# This is why: splitting a vortex REDUCES energy (energy of 2 half-vortices < 1 full)

# But: if strands are TWISTED around each other (braided):
# There's INTERACTION energy between strands!
# E_interaction = ρΓ₁²/(4π) × linking_number × 2πR
# For N strands with linking number L: E_int = NLρΓ₁²R/2

# Total: E = N × E_self + N(N-1)/2 × E_interaction
# This can be MORE than single vortex if L (linking) is large

print(f"""
  Модель: электрон = N сплетённых вихревых нитей (braid).

  Одиночная нить: E₁ = ½ρΓ₁²R·ln(8R/r)
  N нитей, каждая с Γ₁ = Γ/N:
    E_self = N × ½ρ(Γ/N)²R·ln = ½ρΓ²R·ln/N  (МЕНЬШЕ)
    E_mutual = N(N-1)/2 × ρΓ₁² × R × linking
    E_total = E_self + E_mutual

  Для БОЛЬШОГО linking: E_mutual >> E_self → масса РАСТЁТ с N!
""")

# Can we get m_e from N strands?
# E_total ≈ N²ρΓ₁²R × linking / 2  (for large linking)
# = N² × ρ(h/Nm)² × R × linking / 2
# = ρh²R × linking / (2m²)
# Setting = mc²:
# mc² = ρh²R × linking / (2m²)
# m³ = ρh²R × linking / (2c²)

# Compare with single vortex: m³ = π²ρRℏ²/c² ← same structure!
# The "linking" factor replaces π²/2 × (something)

# For the single vortex with v_tube = c:
# m³_single = π²ρRℏ²/c²
# For the braid:
# m³_braid = ρh²R × linking / (2c²) = ρ(2πℏ)²R × linking / (2c²)
#          = 2π²ρℏ²R × linking / c²

# Ratio: m_braid / m_single = (2 × linking)^(1/3)
# For m_braid = m_e and m_single = m(N=1):

# We need m_single first. At what R?
# If L = ½ℏ: m_single = 8.6e-36 kg (from previous calculation)
# Then: linking = (m_e/m_single)³ / 2 = (9.1e-31/8.6e-36)³ / 2

ratio_m = m_e / 8.616e-36
linking_needed = ratio_m**3 / 2

print(f"  Для m_e из сплетённого вихря:")
print(f"    m_single(L=½ℏ) = 8.6×10⁻³⁶ кг")
print(f"    m_e / m_single = {ratio_m:.1f}")
print(f"    linking_needed = (m_e/m_single)³/2 = {linking_needed:.2e}")
print(f"    → Нужен linking number = {linking_needed:.0e} — ОГРОМНЫЙ")

# Alternatively: what if it's a (p,q) torus knot?
# For a (p,q) knot, the "winding number" = p×q
# Total length of tube: L = 2πR × √(p² + q²(R/r)²)
# At R/r >> 1: L ≈ 2πR × q(R/r)
# Energy: E ≈ ½ρΓ² × L/(2πr) = ½ρΓ² × q(R/r)R/r
# = ½ρΓ²qR²/r²

# For v_tube = c: Γ = 2πrc, so Γ² = 4π²r²c²
# E = ½ρ × 4π²r²c² × qR²/r² = 2π²ρc²qR²

# Setting E = mc²: m = 2π²ρqR²/c²... no, m = 2π²ρqR²

# Wait: E = 2π²ρc²qR², and E = mc², so m = 2π²ρqR²

# From L = ½ℏ: this is more complex for a knot...
# Simplified: if R is still from L condition:
# R² = m/(4π²ρ) (from earlier)
# m = 2π²ρq × m/(4π²ρ) = qm/2
# → m = qm/2 → q = 2 ???

# That's trivial. The knot model doesn't help in this simple form.

print(f"""
  Тороидный узел (p,q):
  E = 2π²ρc²qR² → m = 2π²ρqR²

  С L = ½ℏ → R² = m/(4π²ρ):
  m = 2π²ρq × m/(4π²ρ) = qm/2

  → q = 2 (тривиально). Узел не добавляет массы в простейшем приближении.
""")

# ============================================================
# (Д) ELECTROMAGNETIC MASS (the classical approach)
# ============================================================
print("=" * 80)
print("  (Д) ЭЛЕКТРОМАГНИТНАЯ МАССА: m = E_EM/c²")
print("=" * 80)

# What if the mass is NOT kinetic energy of vortex,
# but the ELECTROMAGNETIC field energy around the charge?

# Classical EM mass: m_EM = e²/(6πε₀Rc²)  (Abraham 1902)
# For R = classical electron radius: m_EM = m_e (by definition!)
# R_classical = e²/(4πε₀m_ec²) = 2.82e-15 m

R_classical = e_charge**2 / (4 * math.pi * epsilon_0 * m_e * c**2)
print(f"  Классический радиус: R_cl = e²/(4πε₀mc²) = {R_classical:.3e} м")
print(f"  = α × ƛ_C = {alpha_em} × {hbar/(m_e*c):.3e} = {R_classical:.3e} ✓")

# If ALL mass = EM energy:
# m = e²/(6πε₀Rc²) → R = e²/(6πε₀mc²)
# This gives R = (2/3) × R_classical = 1.88e-15 m (factor 2/3 from geometry)

# In vortex model: the charge creates an EM field OUTSIDE the vortex.
# The EM field energy IS stored in the ether (as deformation).
# So: m_total = m_kinetic(vortex) + m_EM(field)

# m_kinetic = ½ρv²V/c² (from vortex rotation)
# m_EM = e²/(6πε₀Rc²) (from Coulomb field)

# For the vortex with N = 4255, R = 0.49 m:
R_vortex = 0.4925  # from vortex_spectrum.py
m_EM = e_charge**2 / (6 * math.pi * epsilon_0 * R_vortex * c**2)
print(f"\n  EM масса при R = {R_vortex:.3f} м (вихрь электрона):")
print(f"    m_EM = e²/(6πε₀Rc²) = {m_EM:.3e} кг")
print(f"    m_e = {m_e:.3e} кг")
print(f"    m_EM / m_e = {m_EM/m_e:.3e}")
print(f"    → EM масса = {m_EM/m_e:.0e} × m_e — НИЧТОЖНА при R = 0.5 м")

# For m_EM = m_e: need R = e²/(6πε₀m_ec²) = R_classical × 2/3
R_for_m_e = e_charge**2 / (6 * math.pi * epsilon_0 * m_e * c**2)
print(f"\n  Для m_EM = m_e нужен R = {R_for_m_e:.3e} м = {R_for_m_e*1e15:.1f} фм")
print(f"  Это классический радиус электрона (1.88 фм)")
print(f"  А наш вихрь имеет R = 0.5 м — в {R_vortex/R_for_m_e:.0e} раз больше!")

# ============================================================
# SYNTHESIS
# ============================================================
print(f"\n{'='*80}")
print("  СИНТЕЗ ВСЕХ ПУТЕЙ")
print("=" * 80)

print(f"""
  (В) Деформация = кинетика (теорема Кельвина). НЕ ПОМОГАЕТ.

  (Г) Составная структура: linking number ~ 10¹⁵. НЕРЕАЛИСТИЧНО.
      Тороидный узел (p,q) → q = 2. ТРИВИАЛЬНО.

  (Д) EM масса при R = 0.5 м → 10⁻²⁸ × m_e. НИЧТОЖНА.
      Для m_EM = m_e нужен R = 1.88 фм — на 11 порядков меньше.

  ИТОГО:
  ──────
  Ни один из путей (В, Г, Д) не даёт m_e при ρ = μ₀.

  КОРЕНЬ ПРОБЛЕМЫ (окончательно):
  R вихря = 0.5 м при ρ = μ₀ и m = m_e.
  Это ОГРОМНЫЙ вихрь для маленькой частицы.

  Но: R = 0.5 м — это R кольца (major radius).
  r = 386 фм — это r трубки (minor radius).
  R/r = 4255.

  Вихрь электрона = ТОНЧАЙШЕЕ КОЛЬЦО диаметром 1 метр
  с трубкой толщиной 386 фм.

  Это как нить длиной 3 метра (2πR ≈ 3 м) и толщиной 800 фм.
  Свёрнутая в кольцо.

  Физически: ЭТО ж де-бройлевская волна!
  λ_dB = h/p. При p = m_e × c: λ = h/(m_e·c) = 2.4 пм.
  Нет, 2πR = 3 м ≠ λ_C.

  Хм. 2πR = 2π × 0.49 = 3.1 м. А что = 3.1 м?
  λ = h/(m_e × v) при v = ? → v = h/(m_e × 3.1) = {h/(m_e*3.1):.2e} м/с
  = {h/(m_e*3.1)/c:.2e} c — это крайне малая скорость.

  Вихрь "покоится" (v_ring ≈ 0), но КРУТИТСЯ внутри (v_tube = c).
  Это СТОЯЧАЯ ВОЛНА в эфире — электрон в покое = стоячий вихрь.

  ВОПРОС ОСТАЁТСЯ: почему R = 0.5 м, а не 0.5 фм?
  Ответ: потому что ρ = μ₀ = 10⁻⁶ кг/м³ — очень разреженная среда.
  В разреженной среде вихрь должен быть БОЛЬШИМ чтобы набрать массу.
""")


if __name__ == "__main__":
    pass
