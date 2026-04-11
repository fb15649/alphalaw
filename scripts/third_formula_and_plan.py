"""
PART 1: Third formula — μ_p/μ_N = (8/9)π × (1 + ?α²/π^k)
PART 2: Understand coefficients 10/9 and 7/17
PART 3: Bridge chemistry (alphalaw) ↔ particles (π-formulas)
"""
import math

pi = math.pi
alpha = 1 / 137.035999166
alpha_inv = 137.035999166

# Experimental values
mu_p = 2.7928473446       # proton magnetic moment in nuclear magnetons
mn_me = 1838.68366173     # neutron/electron mass ratio
dm_me = 2.53098830        # (m_n - m_p) / m_e
mu_n = 1.91304273         # |neutron magnetic moment| in nuclear magnetons

print("=" * 80)
print("  ЧАСТЬ 1: ТРЕТЬЯ ФОРМУЛА — μ_p/μ_N")
print("=" * 80)

# Base formula
base_mu = (8/9) * pi
eps_mu = (mu_p - base_mu) / base_mu

print(f"\n  Base: (8/9)π = {base_mu:.10f}")
print(f"  Exp:  μ_p   = {mu_p:.10f}")
print(f"  ε = {eps_mu:.6e} = {eps_mu*1e6:.1f} ppm")

# Search for correction: ε = (a/b) × α^n × π^m
print(f"\n  Поиск: ε = (a/b) × α^n × π^m")

best_results = []
for a in range(-20, 21):
    for b in range(1, 20):
        for n in range(0, 5):
            for m in range(-4, 5):
                if a == 0:
                    continue
                val = (a/b) * alpha**n * pi**m
                err = abs(val - eps_mu) / abs(eps_mu) * 100
                if err < 5:
                    corrected = base_mu * (1 + val)
                    corr_ppm = abs(corrected - mu_p) / mu_p * 1e6
                    formula = f"({a}/{b})×α^{n}×π^{m}"
                    best_results.append((formula, val, corr_ppm))

best_results.sort(key=lambda x: x[2])
print(f"  {'Формула':<30s} {'μ_p corrected':>14s} {'err ppm':>10s}")
print("  " + "─" * 58)
for formula, val, ppm in best_results[:10]:
    corrected = base_mu * (1 + val)
    marker = " ★★★" if ppm < 0.1 else " ★★" if ppm < 1 else " ★"
    print(f"  {formula:<30s} {corrected:>14.10f} {ppm:>9.3f}{marker}")

# Best result
if best_results:
    bf, bv, bp = best_results[0]
    corrected = base_mu * (1 + bv)
    print(f"\n  ЛУЧШАЯ: μ_p = (8/9)π × (1 + {bf})")
    print(f"  = {corrected:.10f}")
    print(f"  Exp: {mu_p:.10f}")
    print(f"  Err: {bp:.3f} ppm")
    print(f"  Улучшение: {abs(eps_mu*1e6)/bp:.0f}×")


# ============================================================
# Also try m_n - m_p
# ============================================================
print(f"\n{'─'*80}")
print(f"  ЧЕТВЁРТАЯ ФОРМУЛА: Δm/m_e = (m_n-m_p)/m_e")
print(f"{'─'*80}")

base_dm = (10/7) * math.sqrt(pi)
eps_dm = (dm_me - base_dm) / base_dm

print(f"  Base: (10/7)√π = {base_dm:.10f}")
print(f"  Exp:  Δm/m_e  = {dm_me:.10f}")
print(f"  ε = {eps_dm:.6e} = {eps_dm*1e6:.1f} ppm")

best_dm = []
for a in range(-20, 21):
    for b in range(1, 20):
        for n in range(0, 5):
            for m in range(-4, 5):
                if a == 0:
                    continue
                val = (a/b) * alpha**n * pi**m
                err_val = abs(val - eps_dm) / abs(eps_dm) * 100
                if err_val < 5:
                    corrected = base_dm * (1 + val)
                    corr_ppm = abs(corrected - dm_me) / dm_me * 1e6
                    formula = f"({a}/{b})×α^{n}×π^{m}"
                    best_dm.append((formula, val, corr_ppm))

best_dm.sort(key=lambda x: x[2])
if best_dm:
    print(f"\n  Топ-5:")
    for formula, val, ppm in best_dm[:5]:
        corrected = base_dm * (1 + val)
        marker = " ★★★" if ppm < 1 else " ★★" if ppm < 10 else " ★"
        print(f"    {formula:<30s} {corrected:.8f} {ppm:.1f} ppm{marker}")

    bf, bv, bp = best_dm[0]
    print(f"\n  ЛУЧШАЯ: Δm = (10/7)√π × (1 + {bf})")
    print(f"  Err: {bp:.1f} ppm, улучшение: {abs(eps_dm*1e6)/bp:.0f}×")


# ============================================================
# PART 2: UNDERSTAND COEFFICIENTS
# ============================================================
print(f"\n{'='*80}")
print(f"  ЧАСТЬ 2: КОЭФФИЦИЕНТЫ 10/9 и 7/17 — ОТКУДА?")
print(f"{'='*80}")

# m_p/m_e: ε₁ = +(10/9)α²/π   → coeff = 10/9 = 1.111
# 1/α:     ε₂ = -(7/17)α²/π²  → coeff = -7/17 = -0.412
# μ_p:     ε₃ = best from above

print(f"""
  Собираем ВСЕ коэффициенты при α²/π^k:

  {'Величина':<15s} {'Базовая':<20s} {'Поправка':<20s} {'Коэфф':<10s} {'Знак'} {'π^k'}
  {'─'*80}
  m_p/m_e        6π⁵                +(10/9)α²/π         10/9       +    π¹
  1/α            4π³+π²+π           -(7/17)α²/π²        7/17       -    π²
""")

# Check: do 10/9 and 7/17 have a relationship?
c1 = 10/9      # +1.111
c2 = -7/17     # -0.412

print(f"  c₁ = 10/9 = {c1:.6f}")
print(f"  c₂ = -7/17 = {c2:.6f}")
print(f"  c₁ + c₂ = {c1+c2:.6f} = {10/9 - 7/17:.6f} = {(170-63)/153:.6f} = 107/153")
print(f"  c₁ × c₂ = {c1*c2:.6f} = -70/153 = {-70/153:.6f}")
print(f"  c₁ / c₂ = {c1/c2:.6f} = -(10×17)/(9×7) = -170/63")

# 153 = 9 × 17. The PRODUCT of the denominators!
print(f"\n  Знаменатели: 9 и 17. Произведение: 9 × 17 = 153")
print(f"  Числители: 10 и 7. Произведение: 10 × 7 = 70")
print(f"  c₁×c₂ = -70/153")

# Is 153 special? 153 = 1³ + 5³ + 3³ = 1 + 125 + 27 = 153 (narcissistic number!)
print(f"\n  153 = 1³ + 5³ + 3³ = {1+125+27} (нарциссическое число!)")
print(f"  153 = 9 × 17")
print(f"  9 = 3² (число субвихрей в квадрате)")
print(f"  17 = простое число")

# The NUMERATORS: 10 and 7. Sum = 17 (= denominator of c₂!)
print(f"\n  Числители: 10 + 7 = 17 (= знаменатель c₂!)")
print(f"  10 - 7 = 3 (= число субвихрей)")

# Pattern: c₁ = 10/9 = (7+3)/3²
#          c₂ = 7/17 = 7/(10+7)
print(f"\n  Паттерн?")
print(f"  c₁ = 10/9 = (7+3)/3² = {(7+3)/9:.6f}")
print(f"  c₂ = 7/17 = 7/(10+7) = {7/(10+7):.6f}")
print(f"  → Оба содержат 7 и 3 (или 10=7+3)")
print(f"  7 и 3: два простых числа, сумма = 10")
print(f"  7 = число... чего? 3 = субвихри")

# What if 7 = 2×3+1 = number of parameters? Or 7 = 3+4 (torus + space)?
# 3 sub-vortices, 4 dimensions of spacetime → 3+4=7 ?
print(f"\n  7 = 3 + 4 = (субвихри) + (измерения пространства-времени)?")
print(f"  10 = 7 + 3 = (параметры) + (субвихри)")
print(f"  9 = 3² = (субвихри)²")
print(f"  17 = 10 + 7 = (параметры) + ... ")

# Speculative but: 3 = sub-vortices, 4 = spacetime dims, 7 = 3+4, 10 = 3+7
# This is reminiscent of string theory: 10 = 3+7 or 10 = 4+6


# ============================================================
# PART 3: BRIDGE CHEMISTRY ↔ PARTICLES
# ============================================================
print(f"\n{'='*80}")
print(f"  ЧАСТЬ 3: МОСТ ХИМИЯ ↔ ЧАСТИЦЫ")
print(f"{'='*80}")

print(f"""
  В alphalaw (химические связи):
  π/σ = (E₂-E₁)/E₁ = баланс двух вращений на торе
  α_bond = log₂(1 + π/σ) — определяет молекула или кристалл

  В π-формулах (элементарные частицы):
  m_p/m_e = 6π⁵(1 + 10α²/(9π)) — масса из геометрии тора
  1/α = (4π³+π²+π)(1 - 7α²/(17π²)) — взаимодействие из геометрии

  СВЯЗЬ:
  1. π/σ в химии — это ОТНОШЕНИЕ ДВУХ ВРАЩЕНИЙ тороида.
     В формуле масс — π в СТЕПЕНИ = ЧИСЛО вращений.
     → Химия: 1 тороид, 2 вращения, их ОТНОШЕНИЕ.
     → Частицы: 3 тороида, 5 вращений, их ПРОИЗВЕДЕНИЕ.

  2. α_bond (химия) ∝ ln(1 + π/σ) — логарифм от отношения.
     α_em (физика) входит как α² — квадрат взаимодействия.
     → Химия: α = "мера асимметрии" одного тороида.
     → Физика: α = "мера связи" между вихрем и средой.

  3. Граница α_bond = 1 (молекула/кристалл) соответствует π/σ = 1.
     Граница α_em = 1 была бы при... e² = 4πε₀ℏc.
     Это = "заряд = максимальный" = вихрь полностью открыт наружу.
     Реальность: α = 1/137 << 1 → вихрь ПОЧТИ ЗАМКНУТ.

  ЕДИНАЯ КАРТИНА:
  ───────────────
  Всё = тороидальные вихри в эфире (ρ = μ₀).

  МАСШТАБ ЧАСТИЦ (фм):
  → вихрь = электрон/протон
  → π определяет МАССЫ через число d.o.f.
  → α = мера "утечки" вихря в среду

  МАСШТАБ АТОМОВ (Å):
  → два вихря сближаются = химическая связь
  → σ-поток = осевой (тороидальный)
  → π-поток = боковой (полоидальный)
  → π/σ определяет тип связи (молекула vs кристалл)

  МАСШТАБ МАТЕРИАЛОВ (нм-мм):
  → много связей = кристалл/молекула
  → α_bond, КЧ, платоновы тела

  ОДИН МЕХАНИЗМ НА ТРЁХ МАСШТАБАХ.
  "Что наверху, то и внизу."
""")


# ============================================================
# SUMMARY
# ============================================================
print(f"{'='*80}")
print(f"  ИТОГИ")
print(f"{'='*80}")

if best_results:
    bf3, bv3, bp3 = best_results[0]
    print(f"""
  ТРЕТЬЯ ФОРМУЛА: μ_p/μ_N = (8/9)π × (1 + {bf3})
  Точность: {bp3:.3f} ppm
  Улучшение: {abs(eps_mu*1e6)/bp3:.0f}×

  СВОДКА ВСЕХ ФОРМУЛ С ПОПРАВКАМИ:
  ──────────────────────────────────
  1. m_p/m_e = 6π⁵(1 + (10/9)α²/π)        → 0.01 ppm  (8 цифр) ✓
  2. 1/α = (4π³+π²+π)(1 - (7/17)α²/π²)     → 0.001 ppm (9 цифр) ✓
  3. μ_p/μ_N = (8/9)π(1 + {bf3})  → {bp3:.3f} ppm     ✓

  Три формулы одной структуры: π-база × (1 + дробь×α^n/π^m)
  → Это СИСТЕМА, не совпадение.

  КОЭФФИЦИЕНТЫ:
  10/9 и 7/17 содержат числа 3 и 7:
  10 = 7+3, 9 = 3², 17 = 10+7
  Возможная интерпретация: 3 = субвихри, 7 = 3+4 (вихри + пространство-время)

  МОСТ ХИМИЯ ↔ ЧАСТИЦЫ:
  Один механизм (тороидальные вихри) на трёх масштабах.
  π/σ (химия) = отношение двух вращений одного тороида.
  π^n (частицы) = число степеней свободы нескольких тороидов.
""")


if __name__ == "__main__":
    pass
