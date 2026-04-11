"""
Can we PREDICT digits of m_p/m_e that haven't been measured yet?

Current experimental precision: m_p/m_e = 1836.152 673 43 (11)
That's 11 significant digits. Uncertainty in last 2 digits.

Our formula: 6π⁵ = ?
π is known to trillions of digits → formula gives UNLIMITED precision.
If formula is exact → we predict digits 12, 13, 14...
If formula is approximate → we predict nothing.

Let's see WHERE our formula deviates from experiment.
"""
import math
from decimal import Decimal, getcontext

# Set high precision
getcontext().prec = 50

print("=" * 80)
print("  ТЕСТ ПРЕДСКАЗАНИЯ: m_p/m_e vs 6π⁵")
print("=" * 80)

# ============================================================
# HIGH-PRECISION COMPARISON
# ============================================================

# π to 50 digits (known)
pi_str = "3.14159265358979323846264338327950288419716939937510"
pi_dec = Decimal(pi_str)

# 6π⁵ to 50 digits
six_pi5 = 6 * pi_dec**5

# Experimental m_p/m_e (CODATA 2018)
# 1836.152 673 43 (11) — last two digits uncertain
mp_me_codata = "1836.15267343"
mp_me_unc = 11  # uncertainty in last 2 digits = ±0.00000011

print(f"\n  6π⁵ (50 цифр):")
print(f"    {six_pi5}")
print(f"\n  m_p/m_e (CODATA 2018):")
print(f"    {mp_me_codata} ± {mp_me_unc} (в последних 2 цифрах)")

# Difference
diff = Decimal(mp_me_codata) - six_pi5
print(f"\n  Разница:")
print(f"    m_p/m_e - 6π⁵ = {diff}")
print(f"    = {float(diff):.10e}")

# In units of experimental uncertainty
diff_in_sigma = float(abs(diff)) / (mp_me_unc * 1e-11)
print(f"    = {diff_in_sigma:.0f}σ от экспериментальной погрешности")

# Compare digit by digit
print(f"\n  Поцифровое сравнение:")
s1 = str(six_pi5)[:20]
s2 = mp_me_codata
print(f"    6π⁵:     {s1}")
print(f"    CODATA:  {s2}")
print(f"    Совпад.: ", end="")
for i in range(min(len(s1), len(s2))):
    if i < len(s2) and s1[i] == s2[i]:
        print(s1[i], end="")
    else:
        print(f"← расхождение на позиции {i+1}")
        break

# ============================================================
# WHAT IF FORMULA HAS A CORRECTION?
# ============================================================
print(f"\n\n{'─'*80}")
print(f"  А ЕСЛИ ФОРМУЛА С ПОПРАВКОЙ?")
print(f"{'─'*80}")

# m_p/m_e = 6π⁵ × (1 + ε)
# ε = (m_exp - 6π⁵) / 6π⁵
eps = float(Decimal(mp_me_codata) - six_pi5) / float(six_pi5)
print(f"\n  ε = (m_exp - 6π⁵) / 6π⁵ = {eps:.10e}")
print(f"  = {eps*1e6:.2f} ppm")

# What is ε in terms of known constants?
alpha = 1/137.035999166
print(f"\n  ε в единицах α:")
print(f"    ε/α = {eps/alpha:.6f}")
print(f"    ε/α² = {eps/alpha**2:.4f}")
print(f"    ε/(α/π) = {eps/(alpha/math.pi):.6f}")
print(f"    ε/(α²/π) = {eps/(alpha**2/math.pi):.4f}")

# Is ε = simple fraction × α^n × π^m?
print(f"\n  Поиск: ε = (a/b) × α^n × π^m")
best_err = 999
best_formula = ""
for a in range(1, 20):
    for b in range(1, 20):
        for n in range(0, 4):
            for m_pow in range(-3, 4):
                val = (a/b) * alpha**n * math.pi**m_pow
                if abs(val) < 1e-10:
                    continue
                err = abs(val - eps) / abs(eps) * 100
                if err < best_err:
                    best_err = err
                    best_formula = f"({a}/{b})×α^{n}×π^{m_pow}"

print(f"  Лучшее: ε ≈ {best_formula} (err {best_err:.2f}%)")

# ============================================================
# WHAT DIGITS CAN WE "PREDICT"?
# ============================================================
print(f"\n{'─'*80}")
print(f"  ЧТО МЫ МОЖЕМ 'ПРЕДСКАЗАТЬ'?")
print(f"{'─'*80}")

# Formula: 6π⁵ = 1836.11810990...
# Experiment: 1836.15267343...
# They DIFFER at the 5th significant digit!

print(f"""
  6π⁵ =     1836.1181099...
  CODATA =  1836.1526734...
                  ^ расхождение начинается ЗДЕСЬ (5-й значащий знак)

  Формула совпадает на 4 значащих цифры: 1836.
  На 5-й цифре: формула даёт 1, эксперимент даёт 5.

  Точность формулы: ~19 ppm = ~4 значащих цифры.
  Точность эксперимента: ~0.06 ppm = ~10 значащих цифр.

  ФОРМУЛА В 300 РАЗ ГРУБЕЕ ЭКСПЕРИМЕНТА.
  → Предсказывать НЕЧЕГО. Эксперимент знает больше чем формула.
""")

# ============================================================
# WHAT ABOUT 1/α?
# ============================================================
print(f"{'─'*80}")
print(f"  А ДЛЯ 1/α?")
print(f"{'─'*80}")

alpha_formula = 4*pi_dec**3 + pi_dec**2 + pi_dec
alpha_exp = Decimal("137.035999166")
diff_alpha = alpha_exp - alpha_formula

print(f"  4π³+π²+π = {str(alpha_formula)[:20]}")
print(f"  CODATA   = {alpha_exp}")
print(f"  Разница  = {float(diff_alpha):.6e}")
print(f"  = {float(abs(diff_alpha))/float(alpha_exp)*1e6:.2f} ppm")

# Digit comparison
s_f = str(alpha_formula)[:18]
s_e = str(alpha_exp)
print(f"\n  4π³+π²+π: {s_f}")
print(f"  CODATA:   {s_e}")
print(f"  Совпад.:  ", end="")
for i in range(min(len(s_f), len(s_e))):
    if i < len(s_e) and s_f[i] == s_e[i]:
        print(s_f[i], end="")
    else:
        print(f" ← расхождение на позиции {i+1}")
        break

print(f"""

  4π³+π²+π = 137.03630...
  CODATA   = 137.03599...
                    ^ расхождение на 6-й значащей цифре

  Точность формулы: ~2 ppm = ~5-6 значащих цифр.
  Точность эксперимента: ~0.11 ppm = ~9 значащих цифр.

  ФОРМУЛА В 20 РАЗ ГРУБЕЕ ЭКСПЕРИМЕНТА.
""")

# ============================================================
# THE HONEST CONCLUSION
# ============================================================
print(f"{'='*80}")
print(f"  ЧЕСТНЫЙ ВЫВОД")
print(f"{'='*80}")

print(f"""
  МОЖЕМ ЛИ МЫ ПРЕДСКАЗАТЬ НОВЫЕ ЦИФРЫ?

  НЕТ. Обе формулы ГРУБЕЕ экспериментов:
  • 6π⁵ даёт 4 верных цифры из 11 измеренных
  • 4π³+π²+π даёт 5 верных цифр из 9 измеренных

  Для предсказания нужна формула ТОЧНЕЕ эксперимента.
  У нас — наоборот.

  ЧТО НУЖНО:
  Формула вида: m_p/m_e = 6π⁵ × (1 + f(α, π))
  где f = поправка, дающая оставшиеся 7 цифр.

  Если f = 0: формула грубая (19 ppm).
  Если f найдена: формула предсказывает всё.

  ε = {eps:.6e} = {eps*1e6:.1f} ppm

  Это МАЛЕНЬКАЯ поправка. 6π⁵ — хорошее приближение.
  Но без точной f — предсказания невозможны.

  АНАЛОГИЯ:
  Кеплер знал что орбиты ≈ эллипсы (хорошее приближение).
  Но для предсказания ТОЧНОГО положения Марса нужна
  поправка на гравитацию Юпитера, Сатурна, и т.д.
  Эллипс = нулевое приближение. Поправки = возмущения.

  Наши 6π⁵ = "эллипс Кеплера" для масс.
  Нужны "возмущения" для предсказания точных цифр.
""")


if __name__ == "__main__":
    pass
