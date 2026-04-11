"""
Hunt for π in fundamental physics constants.

Part 1: Verify 6π⁵ specialness (Monte Carlo)
Part 2: Scan ALL measured ratios for π-formulas
Part 3: Analogies — where do powers of π appear in nature?
"""
import math
import numpy as np

pi = math.pi
phi = (1 + math.sqrt(5)) / 2

# ============================================================
# ALL reliably measured dimensionless ratios
# ============================================================
TARGETS = {
    # Mass ratios
    "m_p/m_e": 1836.15267343,
    "m_n/m_e": 1838.68366173,
    "m_n/m_p": 1.00137841931,
    "(m_n-m_p)/m_e": 2.53102,       # = 1.293 MeV / 0.511 MeV

    # Electromagnetic
    "1/α": 137.035999166,
    "μ_p/μ_N": 2.7928473446,        # proton magnetic moment
    "|μ_n/μ_N|": 1.91304273,        # neutron magnetic moment
    "μ_p/|μ_n|": 1.45989805,

    # Koide
    "Koide": 2/3,                    # = 0.66667 (if exact)

    # Geometry
    "R_p/ƛ_C(p)": 0.8414e-15 / (1.0546e-34/(1.6726e-27*2.998e8)),  # R_proton / Compton_p

    # Our vortex model
    "N_e (R/r electron)": 4255,
}

print("=" * 85)
print("  ОХОТА НА π: поиск формул a×π^n в фундаментальных числах")
print("=" * 85)


# ============================================================
# Part 1: SPECIALNESS of 6π⁵
# ============================================================
print(f"\n{'─'*85}")
print(f"  ЧАСТЬ 1: Насколько специальна формула 6π⁵ ≈ 1836.15?")
print(f"{'─'*85}")

target = 1836.15267343
tolerance_pct = 0.01  # 0.01% = 100 ppm

# Count formulas a×π^n with a=1..20, n=1..10 that hit target within tolerance
hits_simple = []
for a in range(1, 21):
    for n in range(1, 11):
        val = a * pi**n
        err = abs(val - target) / target * 100
        if err < tolerance_pct:
            hits_simple.append((a, n, val, err))

print(f"  Target: {target:.5f}")
print(f"  Формулы a×π^n (a=1..20, n=1..10) within {tolerance_pct}%:")
if hits_simple:
    for a, n, val, err in sorted(hits_simple, key=lambda x: x[3]):
        print(f"    {a}×π^{n} = {val:.5f} (err {err:.4f}%)")
else:
    print(f"    Нет попаданий!")

# Total formulas in search space
total_simple = 20 * 10
p_simple = len(hits_simple) / total_simple
print(f"  Total formulas: {total_simple}")
print(f"  Hits: {len(hits_simple)}")
print(f"  P = {p_simple:.2e}")
print(f"  {'SPECIAL' if p_simple < 0.01 else 'NOT special'}")

# Broader: a×π^n + b×π^m (two terms)
hits_two = []
for a in range(-10, 11):
    for n in range(0, 8):
        for b in range(-10, 11):
            for m in range(0, 8):
                if a == 0 and b == 0:
                    continue
                if n == m and a != 0 and b != 0:
                    continue
                val = a * pi**n + b * pi**m
                if val <= 0:
                    continue
                err = abs(val - target) / target * 100
                if err < 0.01:  # 0.01% = 100 ppm
                    hits_two.append((a, n, b, m, val, err))

# Deduplicate by value
seen = set()
unique_two = []
for h in sorted(hits_two, key=lambda x: x[5]):
    key = round(h[4], 6)
    if key not in seen:
        seen.add(key)
        unique_two.append(h)

print(f"\n  Формулы a×π^n + b×π^m (a,b ∈ [-10,10], n,m ∈ [0,7]) within 0.01%:")
for a, n, b, m, val, err in unique_two[:10]:
    print(f"    {a}π^{n} + {b}π^{m} = {val:.5f} (err {err:.4f}%)")
print(f"  Total unique hits: {len(unique_two)}")


# ============================================================
# Part 2: SCAN all targets
# ============================================================
print(f"\n{'─'*85}")
print(f"  ЧАСТЬ 2: Поиск a×π^n для ВСЕХ физических отношений")
print(f"{'─'*85}")

print(f"\n  {'Величина':<25s} {'Значение':>12s} {'Лучшая формула':<20s} {'Err%':>8s}")
print("  " + "─" * 70)

all_results = []

for name, target_val in TARGETS.items():
    if target_val <= 0:
        continue

    best_err = 999
    best_formula = ""
    best_val = 0

    # Single term: a×π^n
    for a_num in range(1, 30):
        for a_den in range(1, 10):
            a = a_num / a_den
            for n_num in range(-10, 11):
                for n_den in range(1, 4):
                    n = n_num / n_den
                    if n == 0 and a == 1:
                        continue
                    try:
                        val = a * pi**n
                    except:
                        continue
                    if val <= 0:
                        continue
                    err = abs(val - target_val) / target_val * 100
                    if err < best_err:
                        best_err = err
                        if a_den == 1:
                            best_formula = f"{a_num}×π^{n_num}" if n_den == 1 else f"{a_num}×π^({n_num}/{n_den})"
                        else:
                            best_formula = f"({a_num}/{a_den})×π^{n_num}" if n_den == 1 else f"({a_num}/{a_den})×π^({n_num}/{n_den})"
                        best_val = val

    marker = " ★★★" if best_err < 0.01 else " ★★" if best_err < 0.1 else " ★" if best_err < 1 else ""
    print(f"  {name:<25s} {target_val:>12.6f} {best_formula:<20s} {best_err:>7.4f}%{marker}")

    all_results.append((name, target_val, best_formula, best_err))


# ============================================================
# Part 3: ANALOGIES — where do powers of π appear?
# ============================================================
print(f"\n{'─'*85}")
print(f"  ЧАСТЬ 3: ГДЕ В ПРИРОДЕ СТЕПЕНИ π ОПРЕДЕЛЯЮТ ПРОПОРЦИИ?")
print(f"{'─'*85}")

print(f"""
  Степени π в математике/физике:

  π¹: Окружность/диаметр. Период колебаний. Нормальное распределение.
  π²: ζ(2) = π²/6 (сумма обратных квадратов). Площадь круга = πr².
      Ускорение g ≈ π² м/с² (не случайность: метр = длина секундного маятника!)
  π³: Объём гиперсферы. Теплоёмкость Дебая (Cv ∝ π⁴T³/15).
  π⁴: Закон Стефана-Больцмана: σ = 2π⁵k⁴/(15h³c²) содержит π⁵.
  π⁵: Стефан-Больцман! σ ∝ π⁵/15.

  Стефан-Больцман:
    σ = (2π⁵k⁴)/(15h³c²)
    → π⁵ появляется в ТЕПЛОВОМ ИЗЛУЧЕНИИ.

  Наше 6π⁵ и Стефан-Больцман:
    σ содержит 2π⁵/15.
    Наше: m_p/m_e ≈ 6π⁵ = 6×π⁵ = (2π⁵/15)×45.

  Совпадение? Или связь между МАССОЙ и ТЕПЛОВЫМ ИЗЛУЧЕНИЕМ?
""")

# Stefan-Boltzmann
k_B = 1.380649e-23
sigma_SB = 2 * pi**5 * k_B**4 / (15 * (6.626e-34)**3 * (2.998e8)**2)
print(f"  σ_SB = 2π⁵k⁴/(15h³c²) = {sigma_SB:.4e} Вт/(м²·К⁴)")
print(f"  2π⁵/15 = {2*pi**5/15:.4f}")
print(f"  6π⁵ / (2π⁵/15) = {6*pi**5 / (2*pi**5/15):.1f} = 45")
print(f"  6 × 15/2 = 45. Или: 6π⁵ = 45 × (2π⁵/15)")

# Where else does π⁵ appear?
print(f"""
  Где ещё π⁵:
  • Ramanujan: 1/π = (2√2/9801) × Σ (4n)!(1103+26390n)/((n!)⁴ × 396⁴ⁿ)
  • ζ(10) = π¹⁰/93555 (содержит π¹⁰ = (π⁵)²)
  • Объём 10-мерной единичной сферы: V₁₀ = π⁵/120
  • 6π⁵ = 6! × V₁₀ / 6 = 720 × π⁵/(120×6) = π⁵

  Подожди: 6π⁵ = 720 × V₁₀ = 6! × V₁₀?
  V₁₀ = π⁵/120 = π⁵/5!
  6! × V₁₀ = 720 × π⁵/120 = 6π⁵ ✓

  m_p/m_e ≈ 6! × V(10-сферы единичного радиуса) / 1

  Или: m_p/m_e ≈ 6!/5! × π⁵ = 6 × π⁵

  Или проще: m_p/m_e ≈ (6!/5!) × π^(5)
""")

# This is the SAME as 6π⁵ but with a "derivation":
# 6 = 6!/5! = 3! = number of permutations of 3 objects
# π⁵ = V(S¹⁰) × 5! = volume of 10-sphere × 120
# m_p/m_e = 3! × π⁵ ???

# Or: 6 = 2×3 = number of faces of a cube / ... no clear meaning

# ============================================================
# Part 4: TRY TO PREDICT A THIRD NUMBER
# ============================================================
print(f"\n{'─'*85}")
print(f"  ЧАСТЬ 4: ПРЕДСКАЗАНИЕ ТРЕТЬЕГО ЧИСЛА ИЗ π")
print(f"{'─'*85}")

# Pattern: 1/α = 4π³+π²+π, m_p/m_e = 6π⁵
# The polynomial coefficients: ..., 0, 6, 0, 4, 1, 1, 0
# For π⁰=1, π¹, π², π³, π⁴, π⁵
# Coefficients: 0, 1, 1, 4, 0, 6

# What's the next? π⁶ coefficient?
# Pattern 0,1,1,4,0,6 → differences: 1,0,3,-4,6 → no obvious pattern

# Alternatively: what if each PARTICLE has its own π-formula?
# electron: defined (m_e = m_e)
# proton: m_p/m_e = 6π⁵
# neutron: m_n/m_e = ?

m_n_over_me = 1838.68366173
# Try: 6π⁵ + something
delta = m_n_over_me - 6*pi**5
print(f"  m_n/m_e - 6π⁵ = {delta:.5f}")
print(f"  (m_n-m_p)/m_e = {m_n_over_me - 1836.15267:.5f}")
print(f"  = {(1.67493e-27 - 1.67262e-27)/9.1094e-31:.3f}")

# Is delta expressible in π?
print(f"\n  Δm/m_e = m_n/m_e - m_p/m_e = {m_n_over_me - 1836.15267343:.6f}")
dm_over_me = m_n_over_me - 1836.15267343  # = 2.531

# Search for π-formula for 2.531
print(f"  Ищу π-формулу для Δm/m_e = {dm_over_me:.4f}:")
best_err_dm = 999
best_formula_dm = ""
for a_num in range(1, 20):
    for a_den in range(1, 10):
        a = a_num / a_den
        for n_num in range(-5, 6):
            for n_den in range(1, 4):
                n = n_num / n_den
                try:
                    val = a * pi**n
                except:
                    continue
                err = abs(val - dm_over_me) / dm_over_me * 100
                if err < best_err_dm:
                    best_err_dm = err
                    if a_den == 1 and n_den == 1:
                        best_formula_dm = f"{a_num}×π^{n_num}"
                    else:
                        best_formula_dm = f"({a_num}/{a_den})×π^({n_num}/{n_den})"

print(f"  Лучшая: {best_formula_dm} (err {best_err_dm:.3f}%)")

# Magnetic moment
print(f"\n  μ_p/μ_N = {2.7928473446:.7f}")
best_err_mu = 999
best_formula_mu = ""
for a_num in range(1, 20):
    for a_den in range(1, 10):
        a = a_num / a_den
        for n_num in range(-5, 6):
            for n_den in range(1, 4):
                n = n_num / n_den
                try:
                    val = a * pi**n
                except:
                    continue
                err = abs(val - 2.7928473446) / 2.7928473446 * 100
                if err < best_err_mu:
                    best_err_mu = err
                    if a_den == 1 and n_den == 1:
                        best_formula_mu = f"{a_num}×π^{n_num}"
                    else:
                        best_formula_mu = f"({a_num}/{a_den})×π^({n_num}/{n_den})"

print(f"  Лучшая: {best_formula_mu} (err {best_err_mu:.3f}%)")

# Check: is μ_p/μ_N related to e (Euler's number)?
import math as m
for name, val in [("e/π", m.e/pi), ("π/e", pi/m.e), ("e-1", m.e-1),
                   ("√(e+π)/2", m.sqrt(m.e+pi)/2), ("ln(π²)", m.log(pi**2)),
                   ("π^(1/e)", pi**(1/m.e)), ("e^(1/π)", m.e**(1/pi))]:
    err = abs(val - 2.7928473446) / 2.7928473446 * 100
    if err < 5:
        print(f"    {name} = {val:.6f} (err {err:.3f}%)")


# ============================================================
# SUMMARY
# ============================================================
print(f"\n{'='*85}")
print(f"  ИТОГИ")
print(f"{'='*85}")

# Count how many targets have π-formula within 0.1%
good = [(n, t, f, e) for n, t, f, e in all_results if e < 0.1]
ok = [(n, t, f, e) for n, t, f, e in all_results if 0.1 <= e < 1]

print(f"""
  π-ФОРМУЛЫ (a×π^(p/q)) с точностью < 0.1%:
""")
for n, t, f, e in good:
    print(f"    {n:<25s} ≈ {f:<20s} (err {e:.4f}%)")

print(f"""
  π-ФОРМУЛЫ с точностью 0.1-1%:
""")
for n, t, f, e in ok:
    print(f"    {n:<25s} ≈ {f:<20s} (err {e:.3f}%)")

print(f"""
  СПЕЦИАЛЬНОСТЬ 6π⁵:
    Формул a×π^n (a=1..20, n=1..10) в 0.01% от 1836: {len(hits_simple)}
    P = {p_simple:.2e} → {'SPECIAL' if p_simple < 0.01 else 'NOT SPECIAL'}

  ТРЕТЬЕ ЧИСЛО ИЗ π:
    Δm/m_e ≈ {best_formula_dm} (err {best_err_dm:.3f}%)
    μ_p/μ_N ≈ {best_formula_mu} (err {best_err_mu:.3f}%)
""")


if __name__ == "__main__":
    pass
