"""
g−2 of the electron from our π-formula for α.

QED prediction: a_e = (g-2)/2 = C₁(α/π) + C₂(α/π)² + C₃(α/π)³ + C₄(α/π)⁴ + ...

Schwinger (1948): C₁ = 1/2
Petermann, Sommerfield (1957): C₂ = -0.328478965...
Laporta, Remiddi (1996): C₃ = 1.181241456...
Kinoshita et al (2012): C₄ = -1.9113(18)
Aoyama et al (2019): C₅ = 6.675(192)

Experimental: a_e = 0.001 159 652 180 73 (28) [Hanneke 2008]

Question: if we use OUR α (from π-formula) instead of experimental α,
how many digits of g-2 do we get right?
"""
import math
from decimal import Decimal, getcontext

getcontext().prec = 40

pi = math.pi

print("=" * 80)
print("  g−2 ЭЛЕКТРОНА ИЗ π-ФОРМУЛЫ ДЛЯ α")
print("=" * 80)

# ============================================================
# Our α formulas
# ============================================================

# Base: 1/α = 4π³+π²+π
alpha_inv_base = 4*pi**3 + pi**2 + pi
alpha_base = 1 / alpha_inv_base

# With correction: 1/α = (4π³+π²+π)(1 - (7/17)α²/π²)
# This is implicit (α on both sides!). Solve iteratively.
alpha_corr = alpha_base  # start
for _ in range(20):
    alpha_inv_corr = alpha_inv_base * (1 - (7/17) * alpha_corr**2 / pi**2)
    alpha_corr = 1 / alpha_inv_corr

# Experimental α
alpha_exp = 1 / 137.035999166

print(f"\n  α values:")
print(f"    α_base (4π³+π²+π)         = 1/{1/alpha_base:.10f} = {alpha_base:.12e}")
print(f"    α_corrected (with α²/π²)  = 1/{1/alpha_corr:.10f} = {alpha_corr:.12e}")
print(f"    α_experimental             = 1/{1/alpha_exp:.10f} = {alpha_exp:.12e}")
print(f"    Δα_base/α = {abs(alpha_base-alpha_exp)/alpha_exp*1e6:.2f} ppm")
print(f"    Δα_corr/α = {abs(alpha_corr-alpha_exp)/alpha_exp*1e6:.3f} ppm")

# ============================================================
# QED coefficients (known analytically or numerically)
# ============================================================

# a_e = Σ Cₙ (α/π)ⁿ for n = 1,2,3,4,5
C1 = 0.5                      # Schwinger 1948 (exact: 1/2)
C2 = -0.328478965579193       # Petermann 1957 (analytic)
C3 = 1.181241456587           # Laporta, Remiddi 1996 (analytic)
C4 = -1.9113                  # Kinoshita 2012 (numerical, ±0.0018)
C5 = 6.675                    # Aoyama 2019 (numerical, ±0.192)

# Also: hadronic and weak corrections
a_hadronic = 1.693e-12        # ≈ 1.69 × 10⁻¹²
a_weak = -0.030e-12           # ≈ -0.03 × 10⁻¹²

# Experimental value
a_exp = 0.00115965218073      # Hanneke et al 2008, ±0.00000000000028

print(f"\n  QED coefficients:")
print(f"    C₁ = {C1}")
print(f"    C₂ = {C2}")
print(f"    C₃ = {C3}")
print(f"    C₄ = {C4}")
print(f"    C₅ = {C5}")

# ============================================================
# Compute a_e with each α
# ============================================================
def compute_ae(alpha, label, terms=5):
    x = alpha / pi
    ae = C1*x + C2*x**2 + C3*x**3 + C4*x**4 + C5*x**5
    ae += a_hadronic + a_weak  # non-QED corrections
    return ae

ae_base = compute_ae(alpha_base, "base")
ae_corr = compute_ae(alpha_corr, "corrected")
ae_exp_calc = compute_ae(alpha_exp, "experimental α")

print(f"\n  a_e = (g-2)/2 computed from different α:")
print(f"  {'Source':<30s} {'a_e':>22s} {'Δ from exp':>14s} {'ppm':>8s}")
print("  " + "─" * 78)
print(f"  {'Our base (4π³+π²+π)':<30s} {ae_base:>22.15f} "
      f"{ae_base-a_exp:>+14.2e} {abs(ae_base-a_exp)/a_exp*1e6:>8.2f}")
print(f"  {'Our corrected (α²/π²)':<30s} {ae_corr:>22.15f} "
      f"{ae_corr-a_exp:>+14.2e} {abs(ae_corr-a_exp)/a_exp*1e6:>8.2f}")
print(f"  {'Experimental α':<30s} {ae_exp_calc:>22.15f} "
      f"{ae_exp_calc-a_exp:>+14.2e} {abs(ae_exp_calc-a_exp)/a_exp*1e6:>8.2f}")
print(f"  {'Experiment (Hanneke 2008)':<30s} {a_exp:>22.15f} "
      f"{'±0.00000000000028':>14s}")

# ============================================================
# Digit-by-digit comparison
# ============================================================
print(f"\n  Поцифровое сравнение:")

def format_ae(value):
    return f"{value:.15f}"

s_exp = format_ae(a_exp)
s_base = format_ae(ae_base)
s_corr = format_ae(ae_corr)

print(f"    Experiment: {s_exp}")
print(f"    Base α:     {s_base}")
print(f"    Corr α:     {s_corr}")

# Count matching digits
match_base = 0
match_corr = 0
for i in range(len(s_exp)):
    if i < len(s_base) and s_exp[i] == s_base[i]:
        match_base += 1
    else:
        break
for i in range(len(s_exp)):
    if i < len(s_corr) and s_exp[i] == s_corr[i]:
        match_corr += 1
    else:
        break

print(f"\n    Совпадающих цифр (base): {match_base - 2} (не считая '0.')")
print(f"    Совпадающих цифр (corr): {match_corr - 2}")

# ============================================================
# How many digits does our α buy us?
# ============================================================
print(f"\n{'─'*80}")
print(f"  АНАЛИЗ: сколько цифр g−2 определяются α?")
print(f"{'─'*80}")

# Sensitivity: da_e/dα ≈ C₁/π = 1/(2π) at leading order
da_dalpha = C1/pi + 2*C2*alpha_exp/pi**2 + 3*C3*alpha_exp**2/pi**3
print(f"\n  da_e/dα ≈ {da_dalpha:.6e}")
print(f"  Δα = {abs(alpha_corr-alpha_exp):.3e}")
print(f"  → Δa_e ≈ da/dα × Δα = {da_dalpha * abs(alpha_corr-alpha_exp):.3e}")
print(f"  Experimental uncertainty: ±{0.28e-12:.2e}")

# Our α error propagated to a_e:
delta_ae_from_alpha = da_dalpha * abs(alpha_corr - alpha_exp)
print(f"\n  Ошибка в a_e от ошибки в α:")
print(f"    Δa_e (base α) = {da_dalpha * abs(alpha_base-alpha_exp):.2e}")
print(f"    Δa_e (corr α) = {da_dalpha * abs(alpha_corr-alpha_exp):.2e}")
print(f"    Exp uncertainty = {0.28e-12:.2e}")
print(f"\n    base: Δa_e / exp_unc = {da_dalpha * abs(alpha_base-alpha_exp) / 0.28e-12:.0f}×")
print(f"    corr: Δa_e / exp_unc = {da_dalpha * abs(alpha_corr-alpha_exp) / 0.28e-12:.0f}×")

# ============================================================
# THE KEY QUESTION: self-consistency
# ============================================================
print(f"\n{'─'*80}")
print(f"  КЛЮЧЕВОЙ ВОПРОС: самосогласованность")
print(f"{'─'*80}")

# In standard physics: α is MEASURED from a_e (g-2).
# α_exp = value that makes QED(α) = a_exp.
# So: using α_exp in QED gives a_exp EXACTLY (by construction).

# Our α is INDEPENDENT — computed from π, not from g-2.
# If our α gives a_e close to experiment — it's NOT a tautology!

# How close?
print(f"""
  В стандартной физике: α ИЗМЕРЕНА из g−2.
  QED(α_exp) = a_exp ← тавтология (α подогнано).

  В нашей модели: α ВЫЧИСЛЕНА из π (независимо от g−2).
  QED(α_our) = ? ← НЕ тавтология!

  Результат:
  QED(α_corrected) = {ae_corr:.15f}
  Experiment        = {a_exp:.15f}
  Δ = {abs(ae_corr - a_exp):.3e}
  = {abs(ae_corr - a_exp)/a_exp * 1e6:.2f} ppm
  = {abs(ae_corr - a_exp) / 0.28e-12:.0f} экспериментальных погрешностей

  Наша α (из π) даёт g−2 с точностью {abs(ae_corr - a_exp)/a_exp * 1e6:.1f} ppm.
  Экспериментальная точность g−2: 0.24 ppb = 0.00024 ppm.

  → Наша α {abs(ae_corr - a_exp)/a_exp * 1e6:.0f} ppm → g−2 в {abs(ae_corr - a_exp)/a_exp * 1e6 / 0.00024:.0f}× хуже эксперимента.
  → Но если α_our отличается от α_exp на {abs(alpha_corr-alpha_exp)/alpha_exp*1e6:.2f} ppm,
     то g−2 АВТОМАТИЧЕСКИ отличается на ~столько же × (da/dα·α/a).
  → Не новая информация: g−2 просто «усиливает» ошибку в α.
""")


# ============================================================
# WHAT IF we REVERSE: compute α from a_exp using QED?
# ============================================================
print(f"{'─'*80}")
print(f"  ОБРАТНАЯ ЗАДАЧА: α из g−2 через нашу π-формулу")
print(f"{'─'*80}")

# Standard: find α such that QED(α) = a_exp.
# Our formula: α = 1/[(4π³+π²+π)(1 - 7α²/(17π²))]

# What if we find α from g−2, and check: is it = our π-formula?
# α from g−2 (Hanneke 2008): 1/α = 137.035 999 084 (51)
alpha_from_g2 = 1 / 137.035999084

# Our formula gives: 1/α = 137.035 999 33
print(f"\n  α из g−2 (Hanneke):  1/α = 137.035999084 ± 51")
print(f"  Наша формула:        1/α = {1/alpha_corr:.9f}")
print(f"  Разница: {abs(1/alpha_corr - 137.035999084):.6f}")
print(f"  = {abs(1/alpha_corr - 137.035999084)/137.036*1e6:.2f} ppm")
print(f"  = {abs(1/alpha_corr - 137.035999084)/0.000000051:.1f} σ (от погрешности g−2)")


# ============================================================
# SUMMARY
# ============================================================
print(f"\n{'='*80}")
print(f"  ИТОГИ: g−2 из π")
print(f"{'='*80}")

digits_corr = match_corr - 2
print(f"""
  1. Наша α (из π): 1/α = {1/alpha_corr:.9f}
     Экспериментальная:  1/α = 137.035999166
     Разница: {abs(1/alpha_corr - 137.035999166)/137.036*1e6:.2f} ppm

  2. g−2 из нашей α: a_e = {ae_corr:.12f}
     Эксперимент:        a_e = {a_exp:.12f}
     Совпадение: {digits_corr} цифр

  3. Ошибка в g−2 = {abs(ae_corr-a_exp)/a_exp*1e6:.1f} ppm
     = прямое следствие ошибки в α ({abs(alpha_corr-alpha_exp)/alpha_exp*1e6:.2f} ppm)
     → g−2 не даёт НОВОЙ информации сверх α

  ВЫВОД: g−2 проверяет α, не добавляя новой физики.
  Наша α с точностью ~0.001 ppm → g−2 с точностью ~0.001 ppm.
  Для лучшего: нужна лучшая α-формула (третья поправка α⁴?).
""")


if __name__ == "__main__":
    pass
