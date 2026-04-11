"""
Final tests: ALL remaining EM numbers that our model hasn't checked.

Only MEASURED, INDEPENDENT, 100% confirmed quantities.

1. m_d/m_p = 1.99900750139  (deuteron/proton mass)
2. μ_d/μ_N = 0.8574382308   (deuteron magnetic moment)
3. R_p = 0.8414 fm          (proton charge radius — model-dependent but measured)
"""
import math

pi = math.pi
alpha = 1 / 137.035999166

print("=" * 80)
print("  ФИНАЛЬНЫЕ ТЕСТЫ: все оставшиеся EM-числа")
print("=" * 80)

def search_pi_formula(target, name, allow_alpha=True):
    """Search for (a/b) × π^(p/q) × α^n closest to target."""
    best_err = 999
    best = ""
    best_val = 0

    for a in range(1, 30):
        for b in range(1, 20):
            for p in range(-10, 11):
                for q in range(1, 4):
                    pw = p / q
                    for n in range(0, 4 if allow_alpha else 1):
                        try:
                            val = (a/b) * pi**pw * alpha**n
                        except:
                            continue
                        if val <= 0:
                            continue
                        err = abs(val - target) / target * 100
                        if err < best_err:
                            best_err = err
                            if b == 1 and q == 1 and n == 0:
                                best = f"{a}×π^{p}"
                            elif n == 0:
                                best = f"({a}/{b})×π^({p}/{q})"
                            elif b == 1 and q == 1:
                                best = f"{a}×π^{p}×α^{n}"
                            else:
                                best = f"({a}/{b})×π^({p}/{q})×α^{n}"
                            best_val = val

    return best, best_val, best_err


# ============================================================
# TEST 1: m_d/m_p = deuteron/proton mass ratio
# ============================================================
print(f"\n{'─'*80}")
print(f"  ТЕСТ 1: m_d/m_p (масса дейтрона / масса протона)")
print(f"{'─'*80}")

md_mp = 1.99900750139  # CODATA 2018, precision 10⁻¹⁰

print(f"\n  m_d/m_p = {md_mp:.11f}")
print(f"  ≈ 2 − 0.001 (дейтрон = почти 2 протона, минус энергия связи)")

# Binding: m_d = m_p + m_n - B/c²
# m_d/m_p = 1 + m_n/m_p - B/(m_p×c²)
# = 1 + 1.001378 - 0.002381 = 1.999007 ✓

# Can we find a π-formula for m_d/m_p?
# m_d/m_p ≈ 2(1 - ε) where ε ≈ 10⁻³
eps_d = 2 - md_mp
print(f"  2 - m_d/m_p = {eps_d:.9f}")
print(f"  ≈ {eps_d:.6f}")

# ε is related to binding energy / proton mass
# B_d = 2.224566 MeV, m_p = 938.272 MeV
# ε = (B_d + (m_n-m_p)c²) / (2m_pc²) ... complex

# Search for π-formula for the WHOLE ratio
f1, v1, e1 = search_pi_formula(md_mp, "m_d/m_p")
print(f"\n  Лучшая π-формула: {f1} = {v1:.11f} (err {e1:.4f}%)")

# Search for ε = 2 - m_d/m_p
f2, v2, e2 = search_pi_formula(eps_d, "ε = 2 - m_d/m_p")
print(f"  Лучшая для ε: {f2} = {v2:.9f} (err {e2:.3f}%)")

# With α² correction
print(f"\n  С α²-поправкой:")
# Base: m_d/m_p = 2(1 - (a/b)π^n × α^m) ???
# Or: m_d/m_p = 2 - f(π, α)
for a in range(1, 20):
    for b in range(1, 20):
        for p in range(-5, 6):
            for q in range(1, 3):
                for n in range(0, 4):
                    val = 2 - (a/b) * pi**(p/q) * alpha**n
                    err = abs(val - md_mp) / md_mp * 100
                    if err < 0.001:
                        pw = f"{p}/{q}" if q > 1 else str(p)
                        print(f"    m_d/m_p = 2 - ({a}/{b})×π^({pw})×α^{n} "
                              f"= {val:.11f} (err {err:.4f}%)")


# ============================================================
# TEST 2: μ_d/μ_N = deuteron magnetic moment
# ============================================================
print(f"\n{'─'*80}")
print(f"  ТЕСТ 2: μ_d/μ_N (магнитный момент дейтрона)")
print(f"{'─'*80}")

mu_d = 0.8574382308  # in nuclear magnetons

print(f"\n  μ_d/μ_N = {mu_d:.10f}")

# Simple: μ_d ≈ μ_p + μ_n = 2.793 + (-1.913) = 0.880
# But actual = 0.857 — difference from sum = −0.023 (correction for D-state mixing)

f3, v3, e3 = search_pi_formula(mu_d, "μ_d/μ_N")
print(f"  Лучшая π-формула: {f3} = {v3:.10f} (err {e3:.4f}%)")

# Try: μ_d = (μ_p + μ_n) × correction
mu_sum = 2.7928473446 - 1.91304273  # μ_p + μ_n (with sign)
print(f"\n  μ_p + μ_n = {mu_sum:.10f}")
print(f"  μ_d / (μ_p + μ_n) = {mu_d/mu_sum:.6f}")

f4, v4, e4 = search_pi_formula(mu_d/mu_sum, "μ_d/(μ_p+μ_n)")
print(f"  Лучшая для отношения: {f4} = {v4:.6f} (err {e4:.3f}%)")


# ============================================================
# TEST 3: R_p = proton charge radius
# ============================================================
print(f"\n{'─'*80}")
print(f"  ТЕСТ 3: R_p (зарядовый радиус протона)")
print(f"{'─'*80}")

R_p = 0.8414e-15  # meters

# In our model: r_proton (tube radius) = ℏ/(m_p·c) = 0.2103 fm
# R_p ≈ 4 × r_tube? No, R_p/r_tube = 0.8414/0.2103 = 4.001
print(f"\n  R_p = {R_p*1e15:.4f} фм")
hbar = 1.0546e-34
m_p = 1.6726e-27
c = 2.998e8
r_tube_p = hbar / (m_p * c)
print(f"  r_tube(p) = ℏ/(m_p·c) = {r_tube_p*1e15:.4f} фм")
print(f"  R_p / r_tube = {R_p/r_tube_p:.4f}")
print(f"  ≈ 4.001")

# R_p / r_tube = 4! Is this exact?
# 4 = что? 3+1? 2²? Число пространственных измерений + время?
print(f"\n  R_p = 4 × ℏ/(m_p·c) ???")
print(f"  4 × r_tube = {4*r_tube_p*1e15:.4f} фм")
print(f"  R_p exp    = {R_p*1e15:.4f} фм")
print(f"  Err = {abs(4*r_tube_p - R_p)/R_p*100:.2f}%")

# Or: R_p = 4 × r_tube exactly?
# = 4ℏ/(m_p c) = 4ƛ_C(p)
# In terms of α: ƛ_C = r_classical/α
# R_p = 4ƛ_C = 4r_e(proton)/α ... hmm

# Try π:
f5, v5, e5 = search_pi_formula(R_p/r_tube_p, "R_p/r_tube")
print(f"\n  R_p/r_tube ≈ {f5} = {v5:.6f} (err {e5:.3f}%)")


# ============================================================
# SUMMARY
# ============================================================
print(f"\n{'='*80}")
print(f"  ИТОГИ ФИНАЛЬНЫХ ТЕСТОВ")
print(f"{'='*80}")

print(f"""
  ТЕСТ 1: m_d/m_p
    Лучшая формула: {f1} (err {e1:.3f}%)
    ε = 2−m_d/m_p: {f2} (err {e2:.2f}%)
    ВЕРДИКТ: {'✓ РАБОТАЕТ' if e1 < 0.1 else '★ перспективно' if e1 < 1 else '✗ не работает'}

  ТЕСТ 2: μ_d/μ_N
    Лучшая формула: {f3} (err {e3:.3f}%)
    ВЕРДИКТ: {'✓ РАБОТАЕТ' if e3 < 0.1 else '★ перспективно' if e3 < 1 else '✗ не работает'}

  ТЕСТ 3: R_p / r_tube(p)
    R_p / (ℏ/m_pc) = {R_p/r_tube_p:.4f} ≈ 4.000 (err {abs(R_p/r_tube_p - 4)/4*100:.2f}%)
    Лучшая: {f5} (err {e5:.3f}%)
    ВЕРДИКТ: {'✓ СОВПАДАЕТ С 4' if abs(R_p/r_tube_p - 4)/4 < 0.005 else '★ близко'}

  САМОЕ ИНТЕРЕСНОЕ:
  R_p = 4 × ℏ/(m_p·c) с точностью {abs(R_p/r_tube_p - 4)/4*100:.2f}%.
  Зарядовый радиус протона = РОВНО 4 комптоновские длины протона.
  4 = число пространственных измерений?
  4 = 2² = (спин × заряд)?
  Или просто совпадение?
""")


if __name__ == "__main__":
    pass
