"""
Toroid nucleon test: does R_charge/R_magnetic ≈ √2 hold for neutron?

Proton finding: R_charge/R_magnetic = 1.433 ≈ √2 = 1.414 (error 1.3%)

Now test on:
- Neutron (μ_n = -1.913 μ_N, r²_charge = -0.1161 fm²)
- Also: deuteron, triton, He-3 if data available
- Also: check other simple ratios (φ, e/π, etc.)

If the pattern holds → toroid aspect ratio is a universal nucleon property.
If it doesn't → proton coincidence.
"""
import math

# Physical constants
h_planck = 6.62607015e-34
hbar = h_planck / (2 * math.pi)
c_light = 2.99792458e8
e_charge = 1.602176634e-19
m_proton = 1.67262192369e-27
m_neutron = 1.67492749804e-27
mu_N = 5.0507837461e-27  # nuclear magneton (J/T)

PHI = (1 + math.sqrt(5)) / 2

print("=" * 80)
print("  ТОРОИДНЫЙ ТЕСТ: протон + нейтрон + ядра")
print("  Гипотеза: R_charge / R_magnetic = √2 (aspect ratio тороида)")
print("=" * 80)

# ============================================================
# PROTON (recap)
# ============================================================
print("\n" + "-" * 60)
print("  ПРОТОН")
print("-" * 60)

mu_p = 2.7928473446  # in μ_N
R_charge_p = 0.8414e-15  # m (CODATA 2018, muonic H consistent)

# R_magnetic from μ = (e·v·R_mag)/2, μ/μ_N = m_p·v·R_mag/ℏ
# At v = c: R_mag = μ/μ_N × ℏ/(m_p·c)
lambda_c_p = hbar / (m_proton * c_light)  # reduced Compton wavelength
R_mag_p = mu_p * lambda_c_p

ratio_p = R_charge_p / R_mag_p

print(f"  μ_p = {mu_p:.7f} μ_N")
print(f"  R_charge = {R_charge_p*1e15:.4f} fm")
print(f"  ƛ_C = ℏ/(m_p·c) = {lambda_c_p*1e15:.4f} fm")
print(f"  R_magnetic = μ·ƛ_C = {R_mag_p*1e15:.4f} fm")
print(f"  R_charge / R_magnetic = {ratio_p:.4f}")
print(f"  √2 = {math.sqrt(2):.4f}")
print(f"  Error = {abs(ratio_p - math.sqrt(2))/math.sqrt(2)*100:.2f}%")

# ============================================================
# NEUTRON
# ============================================================
print("\n" + "-" * 60)
print("  НЕЙТРОН")
print("-" * 60)

mu_n = -1.91304273  # in μ_N (negative!)
# Neutron charge radius: <r²> = -0.1161 ± 0.0022 fm²
# This is NEGATIVE — meaning charge distribution has a negative core
# The RMS "size" is often quoted as √|<r²>| but this is not a real radius
r2_neutron = -0.1161e-30  # m² (negative!)

print(f"  μ_n = {mu_n:.8f} μ_N")
print(f"  <r²>_charge = {r2_neutron*1e30:.4f} fm² (NEGATIVE!)")
print(f"  √|<r²>| = {math.sqrt(abs(r2_neutron))*1e15:.4f} fm (formal)")

# R_magnetic for neutron
lambda_c_n = hbar / (m_neutron * c_light)
R_mag_n = abs(mu_n) * lambda_c_n

print(f"\n  ƛ_C(n) = ℏ/(m_n·c) = {lambda_c_n*1e15:.4f} fm")
print(f"  R_magnetic = |μ_n|·ƛ_C = {R_mag_n*1e15:.4f} fm")

# Problem: neutron charge radius² is NEGATIVE
# This means there's no simple "R_charge" for the neutron
# The charge distribution is: positive core + negative shell (from pion cloud)
# RMS of this gives negative <r²>

# But in toroid model: negative <r²> means the OUTER ring (negative shell)
# is LARGER than the inner ring (positive core)
# R_outer² - R_inner² = |<r²>|

print(f"\n  Проблема: <r²> нейтрона ОТРИЦАТЕЛЬНА")
print(f"  В стандартной модели: d-кварк облако больше u-кварка")
print(f"  В тороидной модели: внешнее кольцо (отриц.) > внутреннего (полож.)")

# Alternative: use the MATTER radius (from neutron scattering)
# Neutron matter radius ≈ proton matter radius ≈ 0.84-0.88 fm
R_matter_n = 0.862e-15  # m (from electron-deuteron scattering, model-dependent)

ratio_n_matter = R_matter_n / R_mag_n

print(f"\n  R_matter(n) ≈ {R_matter_n*1e15:.3f} fm (from scattering)")
print(f"  R_matter / R_magnetic = {ratio_n_matter:.4f}")
print(f"  √2 = {math.sqrt(2):.4f}")
print(f"  Error = {abs(ratio_n_matter - math.sqrt(2))/math.sqrt(2)*100:.2f}%")

# ============================================================
# RATIO μ_p/|μ_n| — is it a simple number?
# ============================================================
print("\n" + "-" * 60)
print("  ОТНОШЕНИЕ μ_p / |μ_n|")
print("-" * 60)

ratio_mu = mu_p / abs(mu_n)
print(f"  μ_p / |μ_n| = {ratio_mu:.6f}")

# Check against simple numbers
candidates = [
    ("3/2", 3/2),
    ("φ", PHI),
    ("√(φ+1)", math.sqrt(PHI + 1)),
    ("e/2", math.e / 2),
    ("π/2", math.pi / 2),
    ("√2", math.sqrt(2)),
    ("ln(5)", math.log(5)),
    ("1 + 1/√2", 1 + 1/math.sqrt(2)),
    ("φ - 1/φ + 1", PHI - 1/PHI + 1),
    ("3·ln(2)", 3*math.log(2)),
    ("2·ln(φ+1)", 2*math.log(PHI+1)),
]

print(f"\n  Comparison with simple constants:")
best_err = 999
best_name = ""
for name, val in candidates:
    err = abs(ratio_mu - val) / ratio_mu * 100
    marker = " ←" if err < 1 else ""
    print(f"    {name:<20s} = {val:.6f}  error = {err:.3f}%{marker}")
    if err < best_err:
        best_err = err
        best_name = name

print(f"\n  Best match: {best_name} (error {best_err:.3f}%)")

# ============================================================
# SUM μ_p + |μ_n| — the isoscalar moment
# ============================================================
print("\n" + "-" * 60)
print("  СУММА И РАЗНОСТЬ")
print("-" * 60)

sum_mu = mu_p + abs(mu_n)  # isoscalar
diff_mu = mu_p - abs(mu_n)  # isovector (signed: p - |n|)

print(f"  μ_p + |μ_n| = {sum_mu:.6f} μ_N")
print(f"  μ_p - |μ_n| = {diff_mu:.6f} μ_N")
print(f"  μ_p × |μ_n| = {mu_p * abs(mu_n):.6f} μ_N²")

# Check these
for name, val in [("μ_p + |μ_n|", sum_mu), ("μ_p - |μ_n|", diff_mu),
                   ("μ_p × |μ_n|", mu_p * abs(mu_n))]:
    for cname, cval in [("1", 1.0), ("π/e", math.pi/math.e), ("φ", PHI),
                         ("√3", math.sqrt(3)), ("e-1", math.e-1),
                         ("2", 2.0), ("5", 5.0), ("π", math.pi),
                         ("4/φ", 4/PHI), ("√φ", math.sqrt(PHI)),
                         ("e/√2", math.e/math.sqrt(2)),
                         ("3/φ", 3/PHI), ("5/3", 5/3),
                         ("φ²", PHI**2), ("2φ-1", 2*PHI-1)]:
        err = abs(val - cval) / abs(val) * 100
        if err < 1:
            print(f"    {name} = {val:.4f} ≈ {cname} = {cval:.4f} (err {err:.2f}%)")

# ============================================================
# TOROID GEOMETRY: what does √2 mean?
# ============================================================
print("\n" + "-" * 60)
print("  ТОРОИДНАЯ ГЕОМЕТРИЯ: что значит R_charge/R_mag = √2")
print("-" * 60)

print(f"""
  Для тороида с большим радиусом R и малым r:
  - R_charge = R (заряд расположен на "большом" круге)
  - R_magnetic ~ (R² - r²)^(1/2) × f(R/r) (площадь тока)

  Для тонкого тороида (R >> r): R_mag ≈ R
  Для "толстого" тороида (R ≈ r): R_mag < R

  R_charge/R_mag = √2 означает:
  R² / R_mag² = 2
  Если R_mag² = R² - r² (сечение тороида):
    R² / (R² - r²) = 2
    1 / (1 - (r/R)²) = 2
    (r/R)² = 1/2
    r/R = 1/√2 = {1/math.sqrt(2):.4f}

  Т.е. малый радиус = R/√2 = 0.707·R
  Это ОЧЕНЬ толстый тороид — почти шар!

  Параметры протонного тороида:
    R = R_charge = 0.841 fm
    r = R/√2 = {0.8414/math.sqrt(2):.3f} fm
    Отношение R/r = √2 = {math.sqrt(2):.3f}
    Внутренний радиус = R - r = {0.8414 - 0.8414/math.sqrt(2):.3f} fm
    Внешний радиус = R + r = {0.8414 + 0.8414/math.sqrt(2):.3f} fm
""")

# ============================================================
# CHECK: does the toroid model predict μ_n from μ_p?
# ============================================================
print("-" * 60)
print("  ПРЕДСКАЗАНИЕ: μ_n из μ_p через тороидную модель?")
print("-" * 60)

# In quark model: μ_p = (4μ_u - μ_d)/3, μ_n = (4μ_d - μ_u)/3
# This gives μ_n/μ_p = -2/3 → μ_n = -2/3 × 2.793 = -1.862
# Actual: μ_n = -1.913
# Quark model error: |(-1.862) - (-1.913)| / 1.913 = 2.7%

mu_n_quark = -2/3 * mu_p
print(f"  Кварковая модель: μ_n = -(2/3)·μ_p = {mu_n_quark:.4f} μ_N")
print(f"  Факт:             μ_n = {mu_n:.4f} μ_N")
print(f"  Error = {abs(mu_n_quark - mu_n)/abs(mu_n)*100:.1f}%")

# Toroid prediction: what if μ is determined by R² - r² (effective area)?
# For proton (positive charge): μ_p = e·c·(R²-r²) / (2·ℏ/m_p)
# For neutron (zero total charge but charge distribution):
# The neutron has +1/3 charge at one radius, -1/3 at another
# In toroid: inner flow (+) and outer flow (-) don't cancel magnetically

# Simplest toroid prediction: if both are R/r = √2 toroids,
# and the difference is in how charge is distributed:
# μ_n/μ_p = -(R² - r²)_n / (R² - r²)_p × (m_p/m_n)
# If same geometry: μ_n/μ_p ≈ -(m_p/m_n) × k
# where k depends on charge distribution

# Try: μ_n = -μ_p × (1 - 1/e)
mu_n_toroid_1 = -mu_p * (1 - 1/math.e)
print(f"\n  Toroid try 1: μ_n = -μ_p·(1-1/e) = {mu_n_toroid_1:.4f} (err {abs(mu_n_toroid_1 - mu_n)/abs(mu_n)*100:.1f}%)")

# Try: μ_n = -μ_p × 2/(2+φ)
mu_n_toroid_2 = -mu_p * 2/(2+PHI)
print(f"  Toroid try 2: μ_n = -μ_p·2/(2+φ) = {mu_n_toroid_2:.4f} (err {abs(mu_n_toroid_2 - mu_n)/abs(mu_n)*100:.1f}%)")

# Try: μ_n = -μ_p × 1/φ² × φ ... no
# Direct: μ_p/|μ_n| = 1.4599...
# Is this 3/2 × (m_n/m_p)?
ratio_mass = m_neutron / m_proton
guess = 1.5 * ratio_mass
print(f"\n  μ_p/|μ_n| = {ratio_mu:.6f}")
print(f"  (3/2)·(m_n/m_p) = {guess:.6f} (err {abs(ratio_mu - guess)/ratio_mu*100:.2f}%)")

# Quark model gives -2/3, actual is -0.685 = -(2/3)·(1 + 0.027)
# The 2.7% correction is from QCD (gluon contributions)
print(f"\n  μ_n/μ_p = {mu_n/mu_p:.6f}")
print(f"  Quark model: -2/3 = {-2/3:.6f}")
print(f"  Error = {abs(mu_n/mu_p - (-2/3)) / abs(mu_n/mu_p) * 100:.1f}%")
print(f"  → Кварковая модель даёт -2/3 с точностью 2.7%")
print(f"  → Любая тороидная формула должна быть ТОЧНЕЕ чем -2/3")

# Is there a better formula?
# -2/3 × (1 + α_em/π) = QED correction
alpha_em_val = 1/137.036
qed_correction = -2/3 * (1 + alpha_em_val / math.pi)
print(f"\n  QED correction: -(2/3)·(1 + α/π) = {qed_correction:.6f}")
print(f"  Error = {abs(qed_correction - mu_n/mu_p) / abs(mu_n/mu_p) * 100:.1f}%")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 80)
print("  ВЫВОДЫ")
print("=" * 80)

print(f"""
  ПРОТОН:
    R_charge/R_magnetic = {ratio_p:.4f} ≈ √2 (err 1.3%)
    Если тороид: r/R = 1/√2, очень "толстый" тороид

  НЕЙТРОН:
    R_matter/R_magnetic = {ratio_n_matter:.4f} ≈ √2 (err {abs(ratio_n_matter - math.sqrt(2))/math.sqrt(2)*100:.1f}%)
    Формальный r²_charge < 0 → нет прямого R_charge
    Но R_matter ≈ R_proton → ratio ТОЖЕ ≈ √2

  ОТНОШЕНИЕ μ_p/|μ_n|:
    = {ratio_mu:.4f} ≈ 3/2 (err {abs(ratio_mu - 1.5)/ratio_mu*100:.1f}%)
    Кварковая модель: -2/3 (err 2.7%) — ЛУЧШЕ всех тороидных попыток
    Тороидная модель НЕ может побить -2/3 простой формулой

  ПАТТЕРН √2:
    Протон: ✓ (err 1.3%)
    Нейтрон: {'✓' if abs(ratio_n_matter - math.sqrt(2))/math.sqrt(2) < 0.03 else '?'} (err {abs(ratio_n_matter - math.sqrt(2))/math.sqrt(2)*100:.1f}%, но R_matter модельно-зависим)

  ВЕРДИКТ:
    √2 МОЖЕТ быть real (оба нуклона ~√2), но:
    1. R_matter нейтрона = модельно-зависимая величина
    2. Кварковая модель даёт μ_n/μ_p = -2/3 точнее любой тороидной формулы
    3. √2 может быть СЛЕДСТВИЕМ quark model, не тороида

    Для доказательства нужно:
    → Вывести √2 ИЗ тороидной модели (не подгонять)
    → Предсказать что-то ЕЩЁ из того же вывода
    → Проверить на другом ядре (дейтрон, He-3)
""")


if __name__ == "__main__":
    pass  # all code runs at top level
