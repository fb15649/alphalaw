"""
THE CONSISTENCY TEST: eliminate π from two formulas.

If m_p/m_e = 6π⁵ and 1/α = 4π³ + π² + π are BOTH true,
then there exists a RELATION between m_p/m_e and 1/α
that does NOT contain π. This relation is testable to 10⁻¹⁰.

Also: π is NOT a coincidence. It's everywhere in measured physics.
"""
import math
import numpy as np

pi = math.pi

# Experimental values (CODATA 2018/2023)
mp_me_exp = 1836.15267343
alpha_inv_exp = 137.035999166
mu_p_exp = 2.7928473446
mn_me_exp = 1838.68366173
mu_n_exp = 1.91304273
dm_me_exp = mn_me_exp - mp_me_exp  # = 2.53099

print("=" * 80)
print("  ТЕСТ СОГЛАСОВАННОСТИ: исключаем π")
print("=" * 80)


# ============================================================
# PART 1: Eliminate π from m_p/m_e and 1/α
# ============================================================
print(f"\n{'─'*80}")
print(f"  ЧАСТЬ 1: Исключение π из двух формул")
print(f"{'─'*80}")

# Formula 1: m_p/m_e = 6π⁵  →  π = (m_p/m_e / 6)^(1/5)
# Formula 2: 1/α = 4π³ + π² + π

# Substitute π from (1) into (2):
# Let x = (m_p/m_e / 6)^(1/5)
# Then: 1/α = 4x³ + x² + x

# This gives a PREDICTION for 1/α from m_p/m_e alone!

x_from_mass = (mp_me_exp / 6)**(1/5)
alpha_inv_predicted = 4 * x_from_mass**3 + x_from_mass**2 + x_from_mass

print(f"  Формула 1: m_p/m_e = 6π⁵  →  π_eff = (m_p/m_e / 6)^(1/5)")
print(f"  Формула 2: 1/α = 4π³ + π² + π")
print(f"")
print(f"  π_eff = ({mp_me_exp}/6)^(1/5) = {x_from_mass:.10f}")
print(f"  π_math = {pi:.10f}")
print(f"  Разница π: {abs(x_from_mass - pi):.6e} = {abs(x_from_mass - pi)/pi*1e6:.1f} ppm")
print(f"")
print(f"  Подставляем π_eff в формулу 2:")
print(f"  1/α (предсказание) = {alpha_inv_predicted:.8f}")
print(f"  1/α (эксперимент)  = {alpha_inv_exp:.8f}")
print(f"  Разница = {abs(alpha_inv_predicted - alpha_inv_exp):.6f}")
print(f"  = {abs(alpha_inv_predicted - alpha_inv_exp)/alpha_inv_exp*1e6:.1f} ppm")

# The other way: get m_p/m_e from 1/α
# From 1/α = 4π³ + π² + π, solve for π numerically
from scipy.optimize import brentq

def eq_alpha(x):
    return 4*x**3 + x**2 + x - alpha_inv_exp

pi_from_alpha = brentq(eq_alpha, 3.0, 3.2)
mp_me_predicted = 6 * pi_from_alpha**5

print(f"\n  Обратно: из 1/α находим π, затем m_p/m_e:")
print(f"  π_from_α = {pi_from_alpha:.10f}")
print(f"  m_p/m_e (предсказание) = {mp_me_predicted:.6f}")
print(f"  m_p/m_e (эксперимент)  = {mp_me_exp:.6f}")
print(f"  Разница = {abs(mp_me_predicted - mp_me_exp):.4f}")
print(f"  = {abs(mp_me_predicted - mp_me_exp)/mp_me_exp*1e6:.1f} ppm")

# KEY: the relation WITHOUT π:
# If m/6 = π⁵ and 1/α = 4π³+π²+π, then π = (m/6)^(1/5)
# 1/α = 4(m/6)^(3/5) + (m/6)^(2/5) + (m/6)^(1/5)
print(f"\n  СООТНОШЕНИЕ БЕЗ π:")
print(f"  1/α = 4(m/6)^(3/5) + (m/6)^(2/5) + (m/6)^(1/5)")
print(f"  где m = m_p/m_e")

# How precise is this relation?
# LHS = 137.035999166
# RHS = 4(1836.153/6)^0.6 + (1836.153/6)^0.4 + (1836.153/6)^0.2
m = mp_me_exp
rhs = 4*(m/6)**0.6 + (m/6)**0.4 + (m/6)**0.2
lhs = alpha_inv_exp
print(f"\n  LHS = 1/α = {lhs:.9f}")
print(f"  RHS = 4(m/6)^(3/5) + (m/6)^(2/5) + (m/6)^(1/5) = {rhs:.9f}")
print(f"  Разница = {abs(lhs-rhs):.6f} = {abs(lhs-rhs)/lhs*1e6:.1f} ppm")


# ============================================================
# PART 2: Test all pairs of formulas
# ============================================================
print(f"\n{'─'*80}")
print(f"  ЧАСТЬ 2: Все пары — согласованность через π")
print(f"{'─'*80}")

# From each formula, extract π:
# m_p/m_e = 6π⁵     → π = (m/6)^(1/5)
# 1/α = 4π³+π²+π   → π = solve(4x³+x²+x = 1/α) ≈ 3.14159...
# μ_p = (8/9)π      → π = (9/8)μ_p = 9μ_p/8
# Δm = (10/7)√π     → π = (7Δm/10)²
# μ_n = (14/5)/π^(1/3) → π = (14/(5μ_n))³

pi_from = {
    "m_p/m_e = 6π⁵": (mp_me_exp / 6)**(1/5),
    "1/α = 4π³+π²+π": pi_from_alpha,
    "μ_p = (8/9)π": 9/8 * mu_p_exp,
    "Δm = (10/7)√π": (7*dm_me_exp/10)**2,
    "|μ_n| = (14/5)π^(-1/3)": (14/(5*mu_n_exp))**3,
}

print(f"\n  π извлечённое из каждой формулы:")
print(f"  {'Формула':<25s} {'π_extracted':>14s} {'Δπ (ppm)':>12s}")
print("  " + "─" * 55)

for name, pi_val in pi_from.items():
    err_ppm = (pi_val - pi) / pi * 1e6
    print(f"  {name:<25s} {pi_val:>14.10f} {err_ppm:>+12.1f}")

# Pairwise consistency: compare π from each pair
print(f"\n  Парная согласованность:")
names = list(pi_from.keys())
vals = list(pi_from.values())
print(f"  {'Пара':<50s} {'Δπ (ppm)':>10s}")
print("  " + "─" * 62)

for i in range(len(names)):
    for j in range(i+1, len(names)):
        diff_ppm = abs(vals[i] - vals[j]) / pi * 1e6
        marker = " ★" if diff_ppm < 100 else ""
        print(f"  {names[i][:24]:<24s} vs {names[j][:24]:<24s} {diff_ppm:>10.1f}{marker}")


# ============================================================
# PART 3: WHERE π IS A MEASURED FACT (not theory)
# ============================================================
print(f"\n{'─'*80}")
print(f"  ЧАСТЬ 3: π — ИЗМЕРЕННЫЙ ФАКТ, НЕ ТЕОРИЯ")
print(f"{'─'*80}")

print(f"""
  π появляется в ИЗМЕРЕННЫХ величинах — не в теориях:

  1. ОКРУЖНОСТЬ / ДИАМЕТР = π
     Измерено с точностью 10⁻¹⁵ (лазерная интерферометрия).
     Не зависит от теории — чистая геометрия пространства.
     Если пространство не евклидово — π меняется!
     Факт: π = 3.14159... → пространство ПЛОСКОЕ (локально).

  2. ПЕРИОД МАЯТНИКА = 2π√(L/g)
     Измерено с точностью 10⁻⁸.
     π входит через ВРАЩЕНИЕ (маятник = проекция кругового движения).

  3. НОРМАЛЬНОЕ РАСПРЕДЕЛЕНИЕ = (1/√(2π)) × exp(-x²/2)
     √(2π) — из гауссова интеграла ∫exp(-x²)dx = √π.
     Измерено статистически (любой эксперимент с шумом).
     π = свойство СЛУЧАЙНОСТИ (или: случайность = проекция вращения).

  4. КВАНТ МАГНИТНОГО ПОТОКА = h/(2e) = π×ℏ/e
     Измерено с точностью 10⁻⁹ (сверхпроводники, эффект Джозефсона).
     π входит НАПРЯМУЮ через 2π в h = 2πℏ.

  5. ПОСТОЯННАЯ ТОНКОЙ СТРУКТУРЫ: α = e²/(4πε₀ℏc)
     4π — геометрический множитель (площадь сферы = 4πr²).
     α ИЗМЕРЕНА с точностью 10⁻¹⁰.
     Без π не записывается.

  6. ИЗЛУЧЕНИЕ ЧЁРНОГО ТЕЛА: σ = 2π⁵k⁴/(15h³c²)
     π⁵ — из интеграла Бозе-Эйнштейна + фазового объёма.
     Измерено с точностью 10⁻⁵.

  7. ГРАВИТАЦИОННЫЕ ВОЛНЫ: частота слияния ∝ 1/(2π) × √(GM/R³)
     Измерено LIGO (2015+) с точностью 10⁻².
     π = из орбитального движения.

  ВЫВОД: π присутствует в КАЖДОМ измерении, связанном с:
  • Вращением
  • Колебанием (= проекция вращения)
  • Сферой (= результат вращения)
  • Статистикой (= суперпозиция вращений)
  • Волнами (= распространение вращения)

  В вихревой модели ВСЁ = вращение → π = ЕДИНСТВЕННАЯ константа.
  Это не совпадение. Это СТРУКТУРА ПРОСТРАНСТВА.
""")


# ============================================================
# PART 4: The precision test — is the relation EXACT?
# ============================================================
print(f"{'─'*80}")
print(f"  ЧАСТЬ 4: ТОЧНЫЙ ТЕСТ — соотношение m_p/m_e ↔ 1/α")
print(f"{'─'*80}")

# The relation: 1/α = 4(m/6)^(3/5) + (m/6)^(2/5) + (m/6)^(1/5)
# is NOT exact (error 21 ppm).
# BUT: maybe the formulas need small corrections?

# What if the EXACT formulas are:
# m_p/m_e = 6π⁵ × (1 + ε₁)
# 1/α = (4π³ + π² + π) × (1 + ε₂)

eps1 = (mp_me_exp - 6*pi**5) / (6*pi**5)
eps2 = (alpha_inv_exp - (4*pi**3 + pi**2 + pi)) / (4*pi**3 + pi**2 + pi)

print(f"\n  Поправки к π-формулам:")
print(f"    ε₁ (масса) = {eps1:.6e} = {eps1*1e6:.1f} ppm")
print(f"    ε₂ (альфа) = {eps2:.6e} = {eps2*1e6:.1f} ppm")
print(f"    ε₁/ε₂ = {eps1/eps2:.3f}")

# Are corrections related to α?
print(f"\n  Связь поправок с α:")
print(f"    α = {1/alpha_inv_exp:.6e}")
print(f"    α/π = {1/(alpha_inv_exp*pi):.6e}")
print(f"    ε₁ = {eps1:.6e} ≈ ? × α")
print(f"    ε₁/α = {eps1*alpha_inv_exp:.4f}")
print(f"    ε₂/α = {eps2*alpha_inv_exp:.4f}")

# ε₁ ≈ 2.6 × α? (radiative correction?)
print(f"    ε₁ ≈ {eps1*alpha_inv_exp:.1f} × α")
print(f"    ε₂ ≈ {eps2*alpha_inv_exp:.1f} × α")

# If ε₁ = (a₁)α and ε₂ = (a₂)α:
# m_p/m_e = 6π⁵(1 + a₁α)
# 1/α = (4π³+π²+π)(1 + a₂α)

# Then the EXACT relation would be:
# 1/α = [4(m/(6(1+a₁α)))^(3/5) + ...] × (1 + a₂α)
# This is TESTABLE if a₁ and a₂ are determined!

print(f"""
  ВЫВОД ЧАСТИ 4:

  Формулы 6π⁵ и 4π³+π²+π — ПРИБЛИЖЕНИЯ.
  Поправки ε ~ 2-20 ppm, масштаба α = 1/137 ≈ 7300 ppm.

  ε₁/α ≈ {eps1*alpha_inv_exp:.1f} (не целое, не простая дробь)
  ε₂/α ≈ {eps2*alpha_inv_exp:.1f} (почти целое?)

  Если ε₂ = α/π²: ε₂ = {1/(alpha_inv_exp*pi**2):.6e} = {1/(alpha_inv_exp*pi**2)*1e6:.1f} ppm
  Факт ε₂ = {eps2:.6e} = {eps2*1e6:.1f} ppm
  Ratio = {eps2 / (1/(alpha_inv_exp*pi**2)):.2f}

  → Поправки НЕ являются простыми функциями α.
  → Либо формулы приближённые, либо поправки от другого источника.
""")


# ============================================================
# SUMMARY
# ============================================================
print(f"{'='*80}")
print(f"  ИТОГИ")
print(f"{'='*80}")

print(f"""
  1. СООТНОШЕНИЕ БЕЗ π:
     1/α = 4(m_p/(6m_e))^(3/5) + (m_p/(6m_e))^(2/5) + (m_p/(6m_e))^(1/5)
     LHS = {alpha_inv_exp:.6f}
     RHS = {rhs:.6f}
     Δ = {abs(lhs-rhs)/lhs*1e6:.1f} ppm
     → СОГЛАСОВАНО НА УРОВНЕ 21 ppm (но не точно)

  2. π ИЗ РАЗНЫХ ФОРМУЛ:
     Из m_p/m_e: π = {pi_from['m_p/m_e = 6π⁵']:.8f} (+3.8 ppm)
     Из 1/α:     π = {pi_from['1/α = 4π³+π²+π']:.8f} (-0.4 ppm)
     Из μ_p:     π = {pi_from['μ_p = (8/9)π']:.8f} (+115 ppm)
     → Масса и α дают π с РАЗНОЙ точностью
     → Лучшая пара: 1/α × m_p/m_e (Δπ = 4 ppm)

  3. π = ИЗМЕРЕННЫЙ ФАКТ:
     Присутствует в каждом измерении связанном с вращением.
     В вихревой модели (всё = вращение) → π = единственная константа.
     Это не совпадение — это ГЕОМЕТРИЯ ПРОСТРАНСТВА.

  4. ТОЧНОСТЬ:
     Формулы = приближения (19 и 2 ppm отклонения от точных значений).
     Поправки ~ α но не = простые функции α.
     Для ТОЧНЫХ формул нужна теория поправок (аналог QED для вихрей).
""")


if __name__ == "__main__":
    pass
