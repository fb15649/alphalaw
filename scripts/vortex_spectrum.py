"""
Vortex spectrum: mass as function of ring size R.

Given: ρ = μ₀, ℏ, c
Free parameter: R (major radius of toroid)

For each known particle: find R, r, R/r, L, v_tube
Check: what determines WHICH R are "allowed"?
"""
import math
import numpy as np

c = 2.99792458e8
h = 6.62607015e-34
hbar = h / (2 * math.pi)
e_charge = 1.602176634e-19
mu_0 = 4e-7 * math.pi
epsilon_0 = 8.8541878128e-12
alpha_em = 1 / 137.036

rho = mu_0

print("=" * 85)
print("  СПЕКТР ВИХРЕЙ: m(R), r(R), L(R), R/r(R)")
print(f"  ρ = μ₀ = {rho:.4e} кг/м³")
print("=" * 85)

# ============================================================
# FORMULAS (from v_tube = c, E = mc²)
#
# r = ℏ/(mc)           — tube radius (Compton wavelength)
# m³ = π²ρRℏ²/c²      — mass from energy
# R = m³c²/(π²ρℏ²)     — ring radius from mass
# Γ = h/m              — circulation
# L = ρΓπR²            — angular momentum
# R/r = m⁴c³/(π²ρℏ³)  — aspect ratio
# v_tube = Γ/(2πr) = c  (by construction)
# v_ring = Γ/(4πR)×[ln(8R/r)-¼] — self-propulsion speed
# ============================================================

def particle_properties(name, mass):
    """Compute all vortex properties for a particle of given mass."""
    m = mass
    r = hbar / (m * c)          # tube radius
    R = m**3 * c**2 / (math.pi**2 * rho * hbar**2)  # ring radius
    Gamma = h / m               # circulation
    L = rho * Gamma * math.pi * R**2  # angular momentum
    Rr = R / r if r > 0 else 0  # aspect ratio
    alpha_geom = (r/R)**2 if R > 0 else 0  # geometric coupling
    V = 2 * math.pi**2 * R * r**2  # volume

    # Self-propulsion speed (thin ring formula, valid for R >> r)
    if Rr > 2:
        ln_factor = math.log(8 * Rr) - 0.25
        v_ring = Gamma / (4 * math.pi * R) * ln_factor
    else:
        v_ring = 0  # formula invalid

    # Spin in units of ℏ
    L_hbar = L / hbar

    return {
        "name": name, "m": m, "R": R, "r": r, "Rr": Rr,
        "Gamma": Gamma, "L": L, "L_hbar": L_hbar,
        "alpha_geom": alpha_geom, "V": V, "v_ring": v_ring,
    }


# Known particles
particles = [
    ("нейтрино (ν_e)", 0.04 * 1.783e-36),   # ~0.04 эВ (from oscillations, rough)
    ("нейтрино (ν_μ)", 0.05 * 1.783e-36),    # ~0.05 эВ
    ("электрон (e)", 9.1093837015e-31),
    ("мюон (μ)", 1.883531627e-28),
    ("пион (π±)", 2.488e-28),
    ("каон (K±)", 8.800e-28),
    ("протон (p)", 1.67262192369e-27),
    ("нейтрон (n)", 1.67492749804e-27),
    ("тау (τ)", 3.16754e-27),
    ("W-бозон", 1.433e-25),
    ("Z-бозон", 1.625e-25),
    ("Хиггс (H)", 2.228e-25),
]

print(f"\n  {'Частица':<16s} {'m (кг)':<11s} {'R (м)':<11s} {'r (м)':<11s} "
      f"{'R/r':<12s} {'L/ℏ':<12s} {'α=(r/R)²'}")
print("  " + "─" * 90)

results = []
for name, mass in particles:
    p = particle_properties(name, mass)
    results.append(p)

    # Format R and r nicely
    if p["R"] < 1e-15:
        R_str = f"{p['R']*1e18:.1f} ам"
    elif p["R"] < 1e-12:
        R_str = f"{p['R']*1e15:.1f} фм"
    elif p["R"] < 1e-9:
        R_str = f"{p['R']*1e12:.1f} пм"
    elif p["R"] < 1e-6:
        R_str = f"{p['R']*1e9:.1f} нм"
    elif p["R"] < 1e-3:
        R_str = f"{p['R']*1e6:.1f} мкм"
    else:
        R_str = f"{p['R']*1e3:.1f} мм"

    if p["r"] < 1e-15:
        r_str = f"{p['r']*1e18:.1f} ам"
    elif p["r"] < 1e-12:
        r_str = f"{p['r']*1e15:.1f} фм"
    else:
        r_str = f"{p['r']*1e12:.2f} пм"

    print(f"  {name:<16s} {mass:<11.3e} {R_str:<11s} {r_str:<11s} "
          f"{p['Rr']:<12.2e} {p['L_hbar']:<12.2e} {p['alpha_geom']:.2e}")

# ============================================================
# ANALYSIS: what patterns?
# ============================================================
print(f"\n{'='*85}")
print("  АНАЛИЗ: есть ли закономерность?")
print("=" * 85)

# L/ℏ for fermions — should be close to ½
fermions = [r for r in results if r["name"] in
            ["электрон (e)", "мюон (μ)", "тау (τ)", "протон (p)", "нейтрон (n)"]]

print(f"\n  Угловой момент фермионов (должен быть ½ℏ):")
for p in fermions:
    ratio_to_half = p["L_hbar"] / 0.5
    print(f"    {p['name']:<16s}: L = {p['L_hbar']:.3e} ℏ "
          f"(L/½ℏ = {ratio_to_half:.3e})")

# R scaling: R ∝ m³ → log(R) = 3·log(m) + const
print(f"\n  Масштабирование R ∝ m³:")
for p in results:
    if p["m"] > 0:
        log_ratio = math.log10(p["R"]) - 3 * math.log10(p["m"])
        print(f"    {p['name']:<16s}: log₁₀(R) - 3·log₁₀(m) = {log_ratio:.2f}")

# R/r scaling: R/r ∝ m⁴
print(f"\n  R/r ∝ m⁴ (aspect ratio):")
print(f"    {'Частица':<16s} {'R/r':<14s} {'m/m_e':<12s} {'(m/m_e)⁴':<14s} {'ratio'}")
for p in results:
    m_ratio = p["m"] / 9.1094e-31
    m4 = m_ratio**4
    if p["Rr"] > 0 and fermions[0]["Rr"] > 0:
        scale = p["Rr"] / fermions[0]["Rr"] if fermions[0]["Rr"] > 0 else 0
        print(f"    {p['name']:<16s} {p['Rr']:<14.2e} {m_ratio:<12.2e} {m4:<14.2e} "
              f"{scale/m4 if m4 > 0 else 0:.3f}")

# ============================================================
# KEY QUESTION: what determines which R are "allowed"?
# ============================================================
print(f"\n{'='*85}")
print("  КЛЮЧЕВОЙ ВОПРОС: что определяет разрешённые R?")
print("=" * 85)

# Hypothesis 1: L = n × ½ℏ (quantized angular momentum)
# L = ρΓπR² = ρ(h/m)πR²
# From m³ = π²ρRℏ²/c²: R = m³c²/(π²ρℏ²)
# L = ρ(h/m)π[m³c²/(π²ρℏ²)]²
# = ρ(h/m)π × m⁶c⁴/(π⁴ρ²ℏ⁴)
# = hm⁵c⁴/(π³ρℏ⁴)
# = 2πℏ × m⁵c⁴/(π³ρℏ⁴)
# = 2m⁵c⁴/(π²ρℏ³)

print(f"\n  L = 2m⁵c⁴/(π²ρℏ³)")
print(f"  Для L = ½ℏ: m⁵ = π²ρℏ⁴/(4c⁴)")

m_half_spin = (math.pi**2 * rho * hbar**4 / (4 * c**4))**(0.2)
print(f"  m(L=½ℏ) = {m_half_spin:.4e} кг = {m_half_spin*c**2/1.602e-19:.3e} эВ")

# For L = n × ½ℏ:
print(f"\n  Спектр масс при L = n × ½ℏ:")
print(f"  {'n':<5s} {'L/ℏ':<8s} {'m (кг)':<12s} {'m (эВ)':<12s} {'Ближайшая':<20s} {'m_part/m'}")
print("  " + "─" * 75)

known_masses = {
    "нейтрино": 0.04 * 1.783e-36,
    "электрон": 9.1094e-31,
    "мюон": 1.8835e-28,
    "пион": 2.488e-28,
    "каон": 8.800e-28,
    "протон": 1.6726e-27,
    "тау": 3.1675e-27,
    "W-бозон": 1.433e-25,
    "Хиггс": 2.228e-25,
}

for n in [1, 2, 3, 4, 5, 6, 7, 8, 10, 15, 20, 50, 100, 200, 500, 1000,
          5000, 10000, 50000, 100000, 500000, 1000000]:
    L_n = n * hbar / 2
    m_n = (L_n * math.pi**2 * rho * hbar**3 / (2 * c**4))**(1/5)
    eV_n = m_n * c**2 / 1.602e-19

    # Find closest known particle
    closest = min(known_masses.items(), key=lambda x: abs(x[1] - m_n))
    ratio = closest[1] / m_n

    marker = ""
    if 0.5 < ratio < 2:
        marker = " ★"
    if 0.9 < ratio < 1.1:
        marker = " ★★★"

    if n <= 20 or marker or n in [50, 100, 500, 1000, 10000, 100000, 1000000]:
        print(f"  {n:<5d} {n/2:<8.1f} {m_n:<12.3e} {eV_n:<12.3e} "
              f"{closest[0]:<20s} {ratio:<.3f}{marker}")

# ============================================================
# Hypothesis 2: R/r = integer (topological quantization)
# ============================================================
print(f"\n{'='*85}")
print("  ГИПОТЕЗА 2: R/r = целое (топологическое квантование)")
print("=" * 85)

# If R/r = N (integer), then:
# R = N × r = N × ℏ/(mc)
# m³ = π²ρRℏ²/c² = π²ρNℏ³/(mc²)
# m⁴ = π²ρNℏ³/c²
# m = [π²ρNℏ³/c²]^(1/4)

print(f"  m = [π²ρNℏ³/c²]^(1/4), N = R/r (целое)")
print(f"\n  {'N':<6s} {'m (кг)':<12s} {'m (эВ)':<12s} {'Ближайшая':<20s} {'ratio'}")
print("  " + "─" * 65)

for N in [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 137, 144, 233, 377,
          1000, 5000, 10000, 137*137]:
    m_N = (math.pi**2 * rho * N * hbar**3 / c**2)**(0.25)
    eV_N = m_N * c**2 / 1.602e-19
    closest = min(known_masses.items(), key=lambda x: abs(x[1] - m_N))
    ratio = closest[1] / m_N

    marker = ""
    if 0.5 < ratio < 2:
        marker = " ★"
    if 0.9 < ratio < 1.1:
        marker = " ★★★"

    # Special numbers
    special = ""
    fibs = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]
    if N in fibs:
        special = " (Fib)"
    if N == 137:
        special = " (1/α)"
    if N == 137**2:
        special = " (1/α²)"

    print(f"  {N:<6d} {m_N:<12.3e} {eV_N:<12.3e} "
          f"{closest[0]:<20s} {ratio:<.3f}{marker}{special}")

# ============================================================
# DIRECT: for each known particle, what is its N = R/r?
# ============================================================
print(f"\n{'='*85}")
print("  ДЛЯ КАЖДОЙ ЧАСТИЦЫ: N = R/r = ?")
print("=" * 85)

print(f"  {'Частица':<16s} {'m (кг)':<12s} {'N = R/r':<14s} {'√N':<10s} "
      f"{'Ближайшее целое'}")
print("  " + "─" * 65)

for name, mass in particles:
    if mass <= 0:
        continue
    # N = R/r = m⁴c³/(π²ρℏ³)
    # Actually from m = [π²ρNℏ³/c²]^(1/4):
    # N = m⁴c²/(π²ρℏ³)
    N = mass**4 * c**2 / (math.pi**2 * rho * hbar**3)
    sqrtN = math.sqrt(N)
    nearest_int = round(N)

    print(f"  {name:<16s} {mass:<12.3e} {N:<14.3e} {sqrtN:<10.3e} "
          f"{nearest_int}")

# ============================================================
# SUMMARY
# ============================================================
print(f"\n{'='*85}")
print("  ВЫВОДЫ")
print("=" * 85)

print(f"""
  МОДЕЛЬ: m = [π²ρNℏ³/c²]^(1/4), где N = R/r = характеристика вихря.

  При ρ = μ₀:
    N(электрон) = {particles[2][1]**4 * c**2 / (math.pi**2 * rho * hbar**3):.3e}
    N(протон)   = {particles[7][1]**4 * c**2 / (math.pi**2 * rho * hbar**3):.3e}

  N — ОГРОМНЫЕ числа (~10¹² для электрона, ~10²⁴ для протона).
  Это не "простые целые числа" типа 1, 2, 137.

  ЭТО НЕ квантование R/r целыми числами — масштаб не тот.

  НО: формула m ∝ N^(1/4) означает:
  m_p/m_e = (N_p/N_e)^(1/4) = {(particles[7][1]/particles[2][1]):.1f}
  → N_p/N_e = (m_p/m_e)⁴ = {(particles[7][1]/particles[2][1])**4:.3e}

  Отношение масс = ЧЕТВЁРТАЯ степень отношения R/r.
  m_p/m_e = 1836 → N_p/N_e = 1836⁴ = {1836**4:.3e}

  Вопрос остаётся: ЧТО фиксирует конкретные N?
  Варианты:
  • Топологический (узлы на торе — числа перекрутов)
  • Резонансный (устойчивые орбиты на торе)
  • Энергетический (минимум энергии при данном L)
""")


if __name__ == "__main__":
    pass
