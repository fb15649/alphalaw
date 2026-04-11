"""
Target 1: Find α²-correction for 1/α = 4π³ + π² + π

For m_p/m_e: correction (10/9)α²/π improved from 19 ppm to 0.01 ppm.
Can we do the same for 1/α?

Method: same as for mass — search for (a/b) × α^n × π^m correction.
"""
import math
from scipy.optimize import brentq

pi = math.pi
alpha = 1 / 137.035999166
alpha_inv = 137.035999166

# Base formula
base = 4*pi**3 + pi**2 + pi
eps_alpha = (alpha_inv - base) / base
print("=" * 80)
print("  МИШЕНЬ 1: поправка для 1/α = 4π³ + π² + π")
print("=" * 80)

print(f"\n  Base: 4π³+π²+π = {base:.10f}")
print(f"  Exp:  1/α     = {alpha_inv:.10f}")
print(f"  ε = (exp - base)/base = {eps_alpha:.6e} = {eps_alpha*1e6:.2f} ppm")
print(f"  Δ = {alpha_inv - base:.6e}")

# ε is NEGATIVE (base > exp)
print(f"\n  ε < 0 → формула ЗАВЫШАЕТ 1/α на {abs(eps_alpha)*1e6:.1f} ppm")

# Search: ε = (a/b) × α^n × π^m
print(f"\n  Поиск: ε = (a/b) × α^n × π^m")
print(f"  {'Формула':<35s} {'Значение':>12s} {'ε_pred':>12s} {'err%':>8s}")
print("  " + "─" * 70)

best_err = 999
best_formula = ""
best_val = 0
results = []

for a in range(-20, 21):
    for b in range(1, 20):
        for n in range(0, 5):
            for m in range(-4, 5):
                if a == 0:
                    continue
                val = (a/b) * alpha**n * pi**m
                err = abs(val - eps_alpha) / abs(eps_alpha) * 100
                if err < 5:
                    formula = f"({a}/{b})×α^{n}×π^{m}"
                    results.append((formula, val, err))
                if err < best_err:
                    best_err = err
                    best_formula = f"({a}/{b})×α^{n}×π^{m}"
                    best_val = val

# Sort by error
results.sort(key=lambda x: x[2])
for formula, val, err in results[:15]:
    marker = " ★★★" if err < 0.1 else " ★★" if err < 1 else " ★"
    corrected = base * (1 + val)
    corr_err_ppm = abs(corrected - alpha_inv) / alpha_inv * 1e6
    print(f"  {formula:<35s} {val:>12.6e} {corr_err_ppm:>8.2f} ppm{marker}")

# Apply best correction
if best_err < 10:
    corrected_best = base * (1 + best_val)
    print(f"\n  Лучшая поправка: {best_formula}")
    print(f"  1/α = (4π³+π²+π) × (1 + {best_formula})")
    print(f"  = {corrected_best:.10f}")
    print(f"  Exp: {alpha_inv:.10f}")
    print(f"  Err: {abs(corrected_best - alpha_inv)/alpha_inv*1e6:.3f} ppm")

    # Compare precision: before and after
    print(f"\n  Улучшение:")
    print(f"    Без поправки: {abs(base - alpha_inv)/alpha_inv*1e6:.2f} ppm")
    print(f"    С поправкой:  {abs(corrected_best - alpha_inv)/alpha_inv*1e6:.3f} ppm")
    print(f"    Улучшение: {abs(base - alpha_inv)/abs(corrected_best - alpha_inv):.0f}×")

# ============================================================
# Try the SAME structure as mass: (a/b) × α² / π
# ============================================================
print(f"\n{'─'*80}")
print(f"  Проверка: та же структура что для массы (α²/π)")
print(f"{'─'*80}")

# For mass: ε_mass = (10/9) × α²/π
# For alpha: ε_alpha = ? × α²/π
coeff_needed = eps_alpha / (alpha**2 / pi)
print(f"\n  ε_α / (α²/π) = {coeff_needed:.4f}")
print(f"  Для массы: коэффициент = 10/9 = {10/9:.4f}")
print(f"  Для α: коэффициент = {coeff_needed:.4f}")

# Is this a simple fraction?
from fractions import Fraction
frac = Fraction(coeff_needed).limit_denominator(20)
print(f"  Ближайшая дробь: {frac} = {float(frac):.6f} (err {abs(float(frac) - coeff_needed)/abs(coeff_needed)*100:.2f}%)")

# Try manually
for a in range(-20, 21):
    for b in range(1, 21):
        val = a/b
        err = abs(val - coeff_needed) / abs(coeff_needed) * 100
        if err < 2:
            corrected = base * (1 + val * alpha**2 / pi)
            corr_ppm = abs(corrected - alpha_inv) / alpha_inv * 1e6
            print(f"    {a}/{b} = {val:.4f} → 1/α = {corrected:.8f} (err {corr_ppm:.2f} ppm)")


# ============================================================
# ALTERNATIVE: additive correction (not multiplicative)
# ============================================================
print(f"\n{'─'*80}")
print(f"  Альтернатива: аддитивная поправка")
print(f"{'─'*80}")

# 1/α = 4π³ + π² + π + δ
# δ = 137.036... - 137.0363... = -0.000304...
delta = alpha_inv - base
print(f"\n  δ = 1/α - (4π³+π²+π) = {delta:.10f}")
print(f"  δ < 0 → нужно ВЫЧЕСТЬ {abs(delta):.6f}")

# Search: δ = (a/b) × π^m × α^n
print(f"\n  Поиск: δ = (a/b) × α^n × π^m")
best_add_err = 999
best_add = ""
for a in range(-20, 21):
    for b in range(1, 20):
        for n in range(0, 5):
            for m in range(-5, 6):
                if a == 0:
                    continue
                val = (a/b) * alpha**n * pi**m
                err = abs(val - delta)
                if err < best_add_err:
                    best_add_err = err
                    best_add = f"({a}/{b})×α^{n}×π^{m}"
                    best_add_val = val

corrected_add = base + best_add_val
print(f"  Лучшая: δ = {best_add} = {best_add_val:.6e}")
print(f"  1/α = 4π³+π²+π + {best_add}")
print(f"  = {corrected_add:.10f}")
print(f"  Exp: {alpha_inv:.10f}")
print(f"  Err: {abs(corrected_add - alpha_inv)/alpha_inv*1e6:.3f} ppm")
print(f"  Улучшение: {abs(base - alpha_inv)/abs(corrected_add - alpha_inv):.0f}×")


# ============================================================
# SUMMARY
# ============================================================
print(f"\n{'='*80}")
print(f"  ИТОГИ: поправка для 1/α")
print(f"{'='*80}")

# Gather all results
print(f"""
  Базовая формула: 1/α = 4π³+π²+π = 137.0363038 (err 2.22 ppm)

  Мультипликативная поправка (как для массы):
  → Нужен коэффициент {coeff_needed:.4f} при α²/π
  → Ближайшая дробь: {frac} (err {abs(float(frac) - coeff_needed)/abs(coeff_needed)*100:.1f}%)

  Лучшая найденная поправка (мультипликативная):
  → {best_formula}
  → Err: {abs(corrected_best - alpha_inv)/alpha_inv*1e6:.3f} ppm

  Лучшая аддитивная поправка:
  → {best_add}
  → Err: {abs(corrected_add - alpha_inv)/alpha_inv*1e6:.3f} ppm

  ДЛЯ СРАВНЕНИЯ:
  Масса протона: 6π⁵(1+10α²/(9π)) → 0.01 ppm (улучшение 2100×)
  1/α: ???
""")


if __name__ == "__main__":
    pass
