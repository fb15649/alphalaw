"""
7 tests of the ether/toroid hypothesis — from testable (#7) to speculative (#1).

#7 Bond lengths: r_bond vs π/σ, LP — can toroid model beat DFT for F anomalies?
#6 Superfluid He: κ = h/m — derivable from toroid?
#5 Fine structure constant α_em ≈ 1/137 — from geometry?
#4 MOND: a₀ ≈ 1.2e-10 m/s² — property of medium?
#3 Casimir: prediction for rotating system
#2 Spin 1/2: topology of twisted toroid
#1 Proton magnetic moment μ_p = 2.793 — from toroid geometry

Each: hypothesis → numerical test → verdict
"""
import sys
import os
import math

import numpy as np
from scipy.stats import pearsonr
from scipy.optimize import curve_fit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from alphalaw.data import BONDS

# Physical constants
h_planck = 6.62607015e-34    # J·s
hbar = h_planck / (2 * math.pi)
c_light = 2.99792458e8       # m/s
e_charge = 1.602176634e-19   # C
m_electron = 9.1093837015e-31  # kg
m_proton = 1.67262192369e-27  # kg
m_he4 = 6.6464731e-27        # kg (He-4 atom mass)
k_boltz = 1.380649e-23       # J/K
epsilon_0 = 8.8541878128e-12  # F/m
mu_0 = 4e-7 * math.pi        # H/m
G_newton = 6.67430e-11       # m³/(kg·s²)
alpha_em = 7.2973525693e-3   # fine structure constant ≈ 1/137.036
mu_N = 5.0507837461e-27      # nuclear magneton (J/T)
mu_proton = 1.41060674333e-26  # proton magnetic moment (J/T)
mu_p_in_mu_N = 2.7928473446  # μ_p / μ_N
PHI = (1 + math.sqrt(5)) / 2

EN = {
    "H": 2.20, "B": 2.04, "C": 2.55, "N": 3.04, "O": 3.44, "F": 3.98,
    "Al": 1.61, "Si": 1.90, "P": 2.19, "S": 2.58, "Cl": 3.16,
    "Ge": 2.01, "As": 2.18, "Se": 2.55, "Br": 2.96, "Sn": 1.96,
    "Te": 2.10, "I": 2.66, "Cr": 1.66, "Mo": 2.16, "W": 2.36, "Re": 1.90,
}


def section(n, title):
    print(f"\n{'=' * 80}")
    print(f"  #{n}. {title}")
    print(f"{'=' * 80}")


# ============================================================
# #7 BOND LENGTHS
# ============================================================
def test7_bond_lengths():
    section(7, "BOND LENGTHS: r_bond vs π/σ и LP")

    # Experimental bond lengths (pm) for single bonds — from CRC Handbook
    # These are equilibrium bond lengths of diatomic molecules or avg in polyatomics
    BOND_LENGTH = {
        "H-H": 74.1, "B-B": 159.0, "C-C": 154.0, "N-N": 145.0, "O-O": 148.0,
        "F-F": 141.2, "Si-Si": 235.0, "P-P": 221.0, "S-S": 205.0, "Cl-Cl": 199.0,
        "Ge-Ge": 241.0, "As-As": 243.0, "Se-Se": 232.0, "Br-Br": 228.9,
        "Sn-Sn": 281.0, "Te-Te": 270.0, "I-I": 266.6,
        # Heteronuclear
        "C-N": 147.0, "C-O": 143.0, "C-S": 182.0, "C-F": 135.0, "C-Cl": 177.0,
        "C-Br": 194.0, "C-I": 214.0, "C-Si": 185.0, "C-P": 184.0,
        "N-O": 140.0, "N-F": 136.0, "N-S": 174.0,
        "B-N": 145.0, "B-O": 136.0, "B-F": 130.0, "B-C": 156.0, "B-Cl": 175.0,
        "Si-O": 163.0, "Si-N": 174.0, "Si-F": 156.0, "Si-Cl": 202.0,
        "P-O": 163.0, "P-S": 210.0, "P-F": 157.0, "P-Cl": 204.0,
        "S-O": 148.0, "S-F": 156.0,
        "Al-O": 162.0, "Ge-O": 177.0,
        "H-C": 109.0, "H-N": 101.0, "H-O": 96.0, "H-F": 91.7,
        "H-S": 134.0, "H-Cl": 127.5, "H-Br": 141.4, "H-I": 160.9,
    }

    # DFT bond lengths (B3LYP/6-311G**) for selected problem cases
    DFT_BOND_LENGTH = {
        "F-F": 138.5,   # DFT underestimates by ~2 pm
        "O-O": 145.3,   # DFT underestimates
        "N-N": 142.8,   # close
        "C-C": 152.7,   # close
        "H-F": 92.0,    # good
        "C-F": 136.2,   # slightly over
        "N-F": 137.1,   # slightly over
        "S-F": 158.0,   # over
    }

    # Collect data: for each bond, get r_bond, E₁, π/σ, LP, α
    data = []
    for b in BONDS:
        if b.alpha is None:
            continue
        key = b.bond
        r = BOND_LENGTH.get(key)
        if r is None:
            continue

        lp_sum = (b.LP_A + b.LP_B) if b.LP_A >= 0 and b.LP_B >= 0 else 0
        lp_min = min(b.LP_A, b.LP_B) if b.LP_A >= 0 and b.LP_B >= 0 else 0

        E1 = b.energies.get(1, 0)
        pi_sigma = None
        if 1 in b.energies and 2 in b.energies:
            pi_sigma = (b.energies[2] - b.energies[1]) / b.energies[1]

        data.append({
            "bond": key, "r": r, "E1": E1, "alpha": b.alpha,
            "pi_sigma": pi_sigma, "lp_sum": lp_sum, "lp_min": lp_min,
            "period": b.period, "block": b.block,
        })

    print(f"\n  Bonds with known r_bond: {len(data)}")

    # Test 1: r_bond vs E₁ (known: r ∝ 1/E roughly)
    r_arr = np.array([d["r"] for d in data])
    e1_arr = np.array([d["E1"] for d in data])
    r_re1, p_re1 = pearsonr(r_arr, e1_arr)
    print(f"\n  r(r_bond, E₁) = {r_re1:.3f} (p={p_re1:.2e})")

    # Test 2: r_bond vs π/σ
    ps_data = [d for d in data if d["pi_sigma"] is not None]
    if ps_data:
        r_ps = np.array([d["r"] for d in ps_data])
        ps_arr = np.array([d["pi_sigma"] for d in ps_data])
        r_rps, p_rps = pearsonr(r_ps, ps_arr)
        print(f"  r(r_bond, π/σ) = {r_rps:.3f} (p={p_rps:.2e})")

    # Test 3: r_bond vs LP_sum
    lp_arr = np.array([d["lp_sum"] for d in data])
    r_rlp, p_rlp = pearsonr(r_arr, lp_arr)
    print(f"  r(r_bond, LP_sum) = {r_rlp:.3f} (p={p_rlp:.2e})")

    # Test 4: r_bond vs period
    per_arr = np.array([d["period"] for d in data])
    r_rper, p_rper = pearsonr(r_arr, per_arr)
    print(f"  r(r_bond, period) = {r_rper:.3f} (p={p_rper:.2e})")

    # Build model: r_bond = f(period, LP_sum, E₁)
    X = np.column_stack([per_arr, lp_arr, e1_arr])
    X_aug = np.column_stack([np.ones(len(data)), X])
    coeffs = np.linalg.lstsq(X_aug, r_arr, rcond=None)[0]
    pred_r = X_aug @ coeffs
    ss_res = np.sum((r_arr - pred_r)**2)
    ss_tot = np.sum((r_arr - r_arr.mean())**2)
    r2_model = 1 - ss_res / ss_tot

    print(f"\n  Model: r = {coeffs[0]:.1f} + {coeffs[1]:.1f}·period + "
          f"{coeffs[2]:.1f}·LP + {coeffs[3]:.3f}·E₁")
    print(f"  R² = {r2_model:.3f}")

    # F-F anomaly test
    print(f"\n  F-F anomaly test:")
    ff = next((d for d in data if d["bond"] == "F-F"), None)
    if ff:
        ff_pred = coeffs[0] + coeffs[1]*ff["period"] + coeffs[2]*ff["lp_sum"] + coeffs[3]*ff["E1"]
        ff_dft = DFT_BOND_LENGTH.get("F-F", 0)
        print(f"    Experiment: {ff['r']:.1f} pm")
        print(f"    DFT (B3LYP): {ff_dft:.1f} pm (error = {abs(ff_dft - ff['r']):.1f} pm)")
        print(f"    Our model:   {ff_pred:.1f} pm (error = {abs(ff_pred - ff['r']):.1f} pm)")

    # All DFT comparisons
    print(f"\n  Model vs DFT for problematic bonds:")
    print(f"  {'Bond':>6s} {'Exper':>6s} {'DFT':>6s} {'Model':>6s} {'DFT_err':>8s} {'Mod_err':>8s} {'Winner'}")
    print("  " + "-" * 55)

    model_wins = 0
    total_comp = 0
    for bond, dft_r in DFT_BOND_LENGTH.items():
        d = next((dd for dd in data if dd["bond"] == bond), None)
        if d is None:
            continue
        mod_r = coeffs[0] + coeffs[1]*d["period"] + coeffs[2]*d["lp_sum"] + coeffs[3]*d["E1"]
        dft_err = abs(dft_r - d["r"])
        mod_err = abs(mod_r - d["r"])
        winner = "MODEL" if mod_err < dft_err else "DFT"
        if mod_err < dft_err:
            model_wins += 1
        total_comp += 1
        print(f"  {bond:>6s} {d['r']:>6.1f} {dft_r:>6.1f} {mod_r:>6.1f} "
              f"{dft_err:>8.1f} {mod_err:>8.1f} {winner}")

    verdict = (f"Model R²={r2_model:.3f}, beats DFT in {model_wins}/{total_comp} cases"
               if total_comp > 0 else "insufficient DFT data")
    print(f"\n  ВЕРДИКТ: {verdict}")
    return {"r2": r2_model, "model_wins": model_wins, "total_comp": total_comp}


# ============================================================
# #6 SUPERFLUID He — κ = h/m
# ============================================================
def test6_superfluid():
    section(6, "СВЕРХТЕКУЧЕСТЬ He-II: κ = h/m из тороида?")

    kappa_exp = h_planck / m_he4  # 9.97e-8 m²/s
    print(f"\n  Квант циркуляции (эксперимент):")
    print(f"    κ = h/m_He = {kappa_exp:.3e} m²/s")

    # Toroid model: circulation = angular momentum / (mass × radius)
    # For a toroid with major radius R and minor radius r:
    # Circulation Γ = ∮ v·dl = 2π·R·v_θ
    # Quantization: Γ = n·h/m (de Broglie for circular orbit)

    # The question: does h/m follow from toroid geometry alone?
    # h/m = v × λ_dB / m × m = v × λ_dB
    # For He at T → 0: λ_dB = h/√(2mE) → ∞

    # Toroid approach: model He atom as toroid with
    # R = Bohr radius for He ≈ 31 pm, v = orbital velocity
    r_he = 31e-12  # m (He atomic radius)
    v_orbital = hbar / (m_he4 * r_he)  # rough estimate

    print(f"\n  Тороидная оценка:")
    print(f"    r_He = {r_he*1e12:.0f} pm")
    print(f"    v_orbital = ℏ/(m·r) = {v_orbital:.1f} m/s")

    kappa_toroid = 2 * math.pi * r_he * v_orbital
    print(f"    κ_toroid = 2π·r·v = {kappa_toroid:.3e} m²/s")
    print(f"    κ_exact  = h/m    = {kappa_exp:.3e} m²/s")
    print(f"    Ratio: {kappa_toroid / kappa_exp:.4f}")

    # Actually, κ = 2π·r·v = 2π·r·(ℏ/mr) = 2π·ℏ/m = h/m
    # This is EXACTLY κ = h/m. Not a prediction — it's a TAUTOLOGY!
    # The toroid just gives circular motion → de Broglie → same formula

    print(f"\n  АНАЛИЗ:")
    print(f"  κ_toroid = 2π·r·(ℏ/mr) = 2πℏ/m = h/m — ТОЖДЕСТВО")
    print(f"  Тороид даёт κ = h/m потому что это просто круговое движение + де Бройль.")
    print(f"  Это НЕ предсказание — любая модель с квантованием углового момента даст то же.")

    # BUT: what about the CRITICAL VELOCITY?
    # In superfluid He, there's a critical velocity v_c below which superflow is maintained
    # Landau criterion: v_c = min(ε(p)/p) where ε(p) is dispersion relation
    # Experimentally v_c ~ 58 m/s (from roton minimum)
    v_c_exp = 58  # m/s (Landau critical velocity from roton minimum)

    # Toroid prediction: v_c = ℏ/(m·R) where R = inter-atomic distance in liquid He
    r_interatomic = 3.6e-10  # m (avg He-He distance in liquid)
    v_c_toroid = hbar / (m_he4 * r_interatomic)
    print(f"\n  Критическая скорость (Ландау):")
    print(f"    v_c (exp, roton) = {v_c_exp} m/s")
    print(f"    v_c (toroid) = ℏ/(m·d) = {v_c_toroid:.1f} m/s")
    print(f"    d = {r_interatomic*1e10:.1f} Å (inter-He distance)")
    print(f"    Ratio: {v_c_toroid / v_c_exp:.2f}")

    verdict = "ТАВТОЛОГИЯ: κ=h/m следует из любой модели с квантованием L. Но v_c — интересно."
    print(f"\n  ВЕРДИКТ: {verdict}")
    return {"kappa_ratio": kappa_toroid / kappa_exp, "vc_ratio": v_c_toroid / v_c_exp}


# ============================================================
# #5 FINE STRUCTURE CONSTANT
# ============================================================
def test5_alpha():
    section(5, "ПОСТОЯННАЯ ТОНКОЙ СТРУКТУРЫ α ≈ 1/137")

    alpha_inv = 1 / alpha_em  # 137.036...
    print(f"\n  α_em = {alpha_em:.10f}")
    print(f"  1/α  = {alpha_inv:.6f}")

    # Known formulas from numerology
    formulas = [
        ("Eddington-like: (16π²/3 - 1/3)⁻¹", 1 / (16*math.pi**2/3 - 1/3)),
        ("Wyler: (9/(16π³))·(π/5!)^(1/4)", (9/(16*math.pi**3)) * (math.pi/120)**(1/4)),
        ("π·e·φ/10", math.pi * math.e * PHI / 10),
        ("(π/2)·e²", (math.pi/2) * math.e**2),
        ("4π³ + π² + π", 4*math.pi**3 + math.pi**2 + math.pi),
        ("e^(π²/2) - e", math.exp(math.pi**2/2) - math.e),
        ("φ² · e^π / 10", PHI**2 * math.exp(math.pi) / 10),
        ("29·cos(π/137) · e^(1/π)", 29 * math.cos(math.pi/137) * math.exp(1/math.pi)),
    ]

    # Toroid-specific: for a toroid with aspect ratio R/r
    # The magnetic field energy ∝ (R/r) × ln(8R/r - 2)
    # If α_em encodes the ratio of EM to total energy of vacuum toroid...
    # Try: α_em = 1/(4π · K) where K = toroid self-inductance factor

    # Self-inductance of toroid: L = μ₀R(ln(8R/r) - 2)
    # For aspect ratio R/r = a: L/μ₀R = ln(8a) - 2
    # Set L/μ₀R = 2π/α_em ??? No physical basis.

    # Let's just try: what aspect ratio gives 137?
    # ln(8a) - 2 = 137 → 8a = e^139 → a = e^139/8 ≈ insane
    # Not useful.

    # More reasonable: 4π²(R/r)² could relate to 137
    # (R/r)² = 137/(4π²) → R/r = √(137/4π²) = √3.47 = 1.86
    # That's a reasonable toroid aspect ratio!

    toroid_ratio = math.sqrt(alpha_inv / (4 * math.pi**2))
    toroid_formulas = [
        ("R/r = √(1/α · 1/4π²)", toroid_ratio, f"R/r = {toroid_ratio:.3f}"),
        ("R/r = (1/α)^(1/3)", alpha_inv**(1/3), f"R/r = {alpha_inv**(1/3):.3f}"),
        ("4π·(R/r)² where R/r=√(e)", 4*math.pi*math.e, ""),
    ]

    print(f"\n  Numerological formulas for 1/α:")
    print(f"  {'Formula':<45s} {'Value':>12s} {'Error':>10s}")
    print("  " + "-" * 70)

    best_err = 999
    best_name = ""
    for name, val in formulas:
        err = abs(val - alpha_inv)
        pct = err / alpha_inv * 100
        marker = " ←" if pct < 0.1 else ""
        print(f"  {name:<45s} {val:>12.6f} {pct:>9.4f}%{marker}")
        if err < best_err:
            best_err = err
            best_name = name

    print(f"\n  Toroid-specific:")
    for name, val, note in toroid_formulas:
        print(f"    {name}: {val:.4f} {note}")

    # Key insight: 137 ≈ 4π² × (aspect ratio)²
    # If the electron IS a toroid, its aspect ratio R/r ≈ 1.86
    # This gives α_em from GEOMETRY alone!
    alpha_from_toroid = 1 / (4 * math.pi**2 * toroid_ratio**2)
    print(f"\n  Toroid hypothesis: α = 1/(4π²·(R/r)²)")
    print(f"    For R/r = {toroid_ratio:.3f}: α = {alpha_from_toroid:.10f}")
    print(f"    Exact:                    α = {alpha_em:.10f}")
    print(f"    This is a TAUTOLOGY (we set R/r to make it work)")

    verdict = (f"Best formula: {best_name} (error {best_err/alpha_inv*100:.4f}%). "
               f"Toroid aspect ratio √(1/4π²α) = {toroid_ratio:.3f} is reasonable but circular.")
    print(f"\n  ВЕРДИКТ: {verdict}")
    return {"best_formula": best_name, "best_error_pct": best_err/alpha_inv*100}


# ============================================================
# #4 MOND
# ============================================================
def test4_mond():
    section(4, "MOND: a₀ ≈ 1.2×10⁻¹⁰ м/с² как свойство среды")

    a0_mond = 1.2e-10  # m/s² (Milgrom 1983)

    # Known coincidences with a₀
    # a₀ ≈ c·H₀ where H₀ = Hubble constant
    H0 = 70  # km/s/Mpc = 70 * 1000 / (3.086e22) s⁻¹
    H0_si = H0 * 1000 / 3.086e22  # ≈ 2.27e-18 s⁻¹
    a_cH = c_light * H0_si

    # a₀ ≈ c²/(R_universe) where R ≈ Hubble radius
    R_hubble = c_light / H0_si
    a_cR = c_light**2 / R_hubble

    # a₀ ≈ √(Λ·c⁴/(3)) where Λ = cosmological constant
    Lambda_cosm = 1.1056e-52  # m⁻² (Planck 2018)
    a_Lambda = c_light**2 * math.sqrt(Lambda_cosm / 3)

    # Toroid hypothesis: a₀ = characteristic acceleration of ether
    # If ether has "viscosity" η_ether, then a₀ = c²·η/(ρ·L)
    # where L = Hubble radius, ρ = vacuum energy density
    # This gives a₀ ~ c·H₀ again — same coincidence

    # Interesting: a₀ from fundamental constants alone
    # a₀ ≈ (ℏ·c / m_p²)^(1/2) · something?
    a_hc_mp = math.sqrt(hbar * c_light) / m_proton  # not right dimensionally
    # Dimensionally: [a] = m/s². ℏc has units J·m = kg·m³/s²
    # ℏc/m² has units m³/(s²·kg) → not acceleration
    # Try: (ℏ·H₀/m_proton)
    a_hH_mp = hbar * H0_si / m_proton  # dimensionless... no

    # Actually: a₀ ≈ c·H₀/2π
    a_cH_2pi = c_light * H0_si / (2 * math.pi)

    print(f"\n  a₀ (MOND) = {a0_mond:.1e} m/s²")
    print(f"\n  Coincidences with cosmological quantities:")
    print(f"    c·H₀       = {a_cH:.2e} m/s²  (ratio = {a_cH/a0_mond:.2f})")
    print(f"    c²/R_Hubble = {a_cR:.2e} m/s²  (ratio = {a_cR/a0_mond:.2f})")
    print(f"    c²√(Λ/3)   = {a_Lambda:.2e} m/s²  (ratio = {a_Lambda/a0_mond:.2f})")
    print(f"    c·H₀/(2π)  = {a_cH_2pi:.2e} m/s²  (ratio = {a_cH_2pi/a0_mond:.2f})")

    # MOND success: rotation curves
    print(f"\n  MOND vs Dark Matter — scoreboard:")
    print(f"    MOND: 1 parameter (a₀) explains 150+ galaxy rotation curves")
    print(f"    Dark Matter: requires fitting halo mass for EACH galaxy")
    print(f"    MOND predicted rotation curves of low surface brightness galaxies")
    print(f"    BEFORE they were measured (McGaugh 1998) — genuine prediction")

    # Toroid interpretation
    print(f"\n  Toroid/ether interpretation:")
    print(f"    a₀ ≈ c·H₀ suggests: a₀ = property of expanding ether (Hubble flow)")
    print(f"    Below a₀: object is 'carried' by ether (MOND regime)")
    print(f"    Above a₀: object moves through ether (Newtonian regime)")
    print(f"    This is analogous to: subsonic (carried by medium) vs supersonic")

    verdict = ("a₀ ≈ c·H₀ within factor 6 — known coincidence, not new. "
               "MOND's predictive success is real. Ether interpretation adds intuition but not testability.")
    print(f"\n  ВЕРДИКТ: {verdict}")
    return {"a0_ratio_cH": a_cH / a0_mond}


# ============================================================
# #3 CASIMIR IN ROTATING SYSTEM
# ============================================================
def test3_casimir():
    section(3, "КАЗИМИР: предсказание для вращающейся системы")

    # Standard Casimir force between parallel plates
    # F/A = -π²ℏc/(240·d⁴)
    d = 100e-9  # 100 nm gap
    F_casimir = math.pi**2 * hbar * c_light / (240 * d**4)  # N/m²

    print(f"\n  Standard Casimir (d = {d*1e9:.0f} nm):")
    print(f"    F/A = π²ℏc/(240d⁴) = {F_casimir:.2f} Pa")

    # Rotating system: if ether exists, rotation creates anisotropy
    # The Unruh effect gives: temperature T = ℏa/(2πck_B)
    # For rotation: a = ω²R (centripetal)
    # This gives an effective temperature → modified Casimir force?

    omega = 1000  # rad/s (centrifuge)
    R = 0.1  # m (10 cm radius)
    a_centripetal = omega**2 * R
    T_unruh = hbar * a_centripetal / (2 * math.pi * c_light * k_boltz)

    print(f"\n  Rotating system (ω={omega} rad/s, R={R*100:.0f} cm):")
    print(f"    a_centripetal = {a_centripetal:.0f} m/s²")
    print(f"    T_Unruh = ℏa/(2πck_B) = {T_unruh:.2e} K")
    print(f"    (way too small to measure — T_room ≈ 300 K)")

    # Ether hypothesis: rotation through ether creates drag → modified force
    # v = ω·R relative to ether
    v_ether = omega * R
    beta = v_ether / c_light

    # Relative correction: ΔF/F ~ β² (Lorentz-type)
    correction = beta**2
    delta_F = F_casimir * correction

    print(f"\n  Ether drag hypothesis:")
    print(f"    v = ω·R = {v_ether:.0f} m/s")
    print(f"    β = v/c = {beta:.2e}")
    print(f"    Correction ΔF/F ~ β² = {correction:.2e}")
    print(f"    ΔF = {delta_F:.2e} Pa")
    print(f"    This is {correction:.2e} of the Casimir force — UNMEASURABLE")

    # More promising: Casimir force between rotating disks
    # (Casimir torque, already measured for birefringent materials)
    print(f"\n  Alternative: Casimir TORQUE between anisotropic plates")
    print(f"    Already measured (Somers et al. 2018, Nature)")
    print(f"    Standard QED explains it (birefringent vacuum modes)")
    print(f"    Ether would predict SAME result — no distinguishing test")

    verdict = ("Correction ~β²~10⁻¹³ — unmeasurable. Casimir torque exists but "
               "standard QED explains it. No distinguishing experiment found.")
    print(f"\n  ВЕРДИКТ: {verdict}")
    return {"correction": correction}


# ============================================================
# #2 SPIN 1/2
# ============================================================
def test2_spin():
    section(2, "СПИН 1/2: топология тороида с перекрутом")

    print(f"""
  Стандартная модель: спин 1/2 = спинорное представление SO(3).
  Поворот на 360° → ψ → -ψ. Нужно 720° для возврата.
  Это ПОСТУЛАТ, не выводится из чего-то более простого.

  Тороидная гипотеза: частица = вихревое кольцо (тороид).
  Если тороид имеет ПОЛУЦЕЛЫЙ перекрут (Möbius-like):
  - 0 перекрутов = полный тор → спин 0 (скаляр)
  - 1/2 перекрута = лента Мёбиуса → спин 1/2 (фермион)
  - 1 перекрут = двойное кольцо → спин 1 (бозон)

  Аналогия: лента Мёбиуса — обойди 1 раз → попал на другую сторону.
  Обойди 2 раза → вернулся. Это РОВНО 720° = 2×360°.
""")

    # Can we make this quantitative?
    # For a torus knot (p,q): p windings around tube, q around hole
    # Spin = p/(2q) for simplest cases?
    # Electron: spin 1/2 → p=1, q=1 → trefoil? No, (1,1) = trivial knot

    # Actually: Dirac belt trick demonstrates spin 1/2 geometrically
    # The topology is: SU(2) double-covers SO(3)
    # A toroid with half-twist IS topologically Möbius
    # And its fundamental group requires double traversal

    print(f"  Количественный тест:")
    print(f"  Если спин = (число перекрутов)/2, то:")
    particles = [
        ("Higgs boson", 0, 0, "скаляр"),
        ("Photon", 1, 2, "вектор"),
        ("Electron", 0.5, 1, "фермион"),
        ("Graviton", 2, 4, "тензор"),
        ("W/Z boson", 1, 2, "вектор"),
        ("Gluon", 1, 2, "вектор"),
        ("Quark", 0.5, 1, "фермион"),
        ("Neutrino", 0.5, 1, "фермион"),
    ]

    print(f"\n  {'Particle':<15s} {'Spin':>5s} {'Twists':>6s} {'Type':<10s}")
    print("  " + "-" * 40)
    for name, spin, twists, ptype in particles:
        print(f"  {name:<15s} {spin:>5.1f} {twists:>6d} {ptype:<10s}")

    # The mapping spin = twists/2 is CONSISTENT but is it PREDICTIVE?
    # To be predictive, we need: from toroid topology → predict NEW spin value
    # Problem: all known spins are 0, 1/2, 1, 3/2, 2 — all fit n/2

    print(f"\n  Это СОГЛАСОВАННО (spin = twists/2 для всех), но не ПРЕДСКАЗАТЕЛЬНО.")
    print(f"  Любая частица с spin = n/2 вписывается → нет фальсифицируемости.")
    print(f"")
    print(f"  Что БЫЛО БЫ предсказанием:")
    print(f"  - Невозможность спина > 2 для элементарных частиц")
    print(f"    (тороид не может иметь >4 перекрутов стабильно?)")
    print(f"    Факт: спин >2 для элементарных частиц НЕ наблюдается!")
    print(f"    Но стандартная модель это тоже предсказывает (Weinberg-Witten theorem)")

    verdict = ("Согласовано (spin=twists/2) но не предсказательно. "
               "Ограничение spin≤2 интересно, но объяснимо и без тороида.")
    print(f"\n  ВЕРДИКТ: {verdict}")
    return {}


# ============================================================
# #1 PROTON MAGNETIC MOMENT
# ============================================================
def test1_proton():
    section(1, "МАГНИТНЫЙ МОМЕНТ ПРОТОНА μ_p = 2.793 μ_N")

    print(f"\n  Факт: μ_p = {mu_p_in_mu_N:.7f} ядерных магнетонов")
    print(f"  Если бы протон = точечная частица: μ_p = 1.000 μ_N")
    print(f"  Anomalous moment = {mu_p_in_mu_N - 1:.7f} μ_N")
    print(f"  Стандартная модель (lattice QCD): ~2.8 ± 10% (после 40 лет расчётов)")

    # Toroid model: proton = current loop (toroid)
    # Magnetic moment of current loop: μ = I·A = I·π·r²
    # For a toroid with major radius R and minor radius r:
    # μ = (q·v)/(2π·R) · π·R² = q·v·R/2
    # μ_N = eℏ/(2m_p) (nuclear magneton)
    # μ_p/μ_N = (q·v·R/2) / (eℏ/2m_p) = m_p·v·R/ℏ

    # So μ_p/μ_N = m_p·v·R/ℏ = p·R/ℏ where p = m_p·v
    # For de Broglie: p = ℏ/λ_dB → μ/μ_N = R/λ_dB

    # Proton charge radius from experiment: R_p = 0.8414 fm (CODATA 2018)
    R_proton = 0.8414e-15  # m

    # Compton wavelength of proton: λ_C = h/(m_p·c) = 1.321e-15 m
    lambda_compton = h_planck / (m_proton * c_light)

    # Ratio
    ratio_R_lambda = R_proton / (lambda_compton / (2 * math.pi))
    print(f"\n  Тороидная оценка:")
    print(f"    R_proton (charge radius) = {R_proton*1e15:.4f} fm")
    print(f"    ƛ_C (reduced Compton) = ℏ/(m_p·c) = {lambda_compton/(2*math.pi)*1e15:.4f} fm")
    print(f"    μ/μ_N ≈ R_p/ƛ_C = {ratio_R_lambda:.3f}")
    print(f"    Actual μ/μ_N = {mu_p_in_mu_N:.3f}")
    print(f"    Error = {abs(ratio_R_lambda - mu_p_in_mu_N)/mu_p_in_mu_N*100:.1f}%")

    # More sophisticated: toroid with R (major) and r (minor)
    # μ = NIA where N = windings, I = current, A = area
    # For a single-winding toroid: μ = (e·c)/(2π) · (R² - r²)^(1/2) ... complex

    # Try empirical: what R/r gives μ_p/μ_N = 2.793?
    # Simple current ring: μ = I·π·R² = (e·v/(2πR))·πR² = e·v·R/2
    # μ/μ_N = m_p·v·R/ℏ
    # At v = c (relativistic): μ/μ_N = m_p·c·R/ℏ = R/ƛ_C
    # Need R = 2.793 × ƛ_C = 2.793 × 0.2103 fm = 0.587 fm
    R_needed = mu_p_in_mu_N * hbar / (m_proton * c_light)
    print(f"\n  Для μ/μ_N = 2.793 при v = c:")
    print(f"    R_needed = {R_needed*1e15:.3f} fm")
    print(f"    R_proton = {R_proton*1e15:.3f} fm")
    print(f"    R_needed / R_proton = {R_needed/R_proton:.3f}")

    # The charge radius and magnetic radius are DIFFERENT!
    # R_magnetic = 2.793 × ƛ_C = 0.587 fm
    # R_charge = 0.841 fm
    # Ratio: R_charge / R_magnetic = 0.841/0.587 = 1.43 ≈ √2 !!!
    ratio_radii = R_proton / R_needed
    print(f"\n  ИНТЕРЕСНО:")
    print(f"    R_charge / R_magnetic = {ratio_radii:.3f}")
    print(f"    √2 = {math.sqrt(2):.3f}")
    print(f"    Error = {abs(ratio_radii - math.sqrt(2))/math.sqrt(2)*100:.1f}%")

    # If the proton is a toroid:
    # R_charge = major radius R (where charge is)
    # R_magnetic = minor radius relates to current path
    # R/r_eff = √2 → the toroid's aspect ratio!
    print(f"\n  Тороидная интерпретация:")
    print(f"    Если протон = тороид:")
    print(f"    R_charge = R_major = {R_proton*1e15:.3f} fm (где заряд)")
    print(f"    R_magnetic = R_eff = {R_needed*1e15:.3f} fm (магнитная 'площадь')")
    print(f"    Отношение = {ratio_radii:.3f} ≈ √2 = {math.sqrt(2):.3f}")
    print(f"    → Aspect ratio тороида протона ≈ √2")

    close_to_sqrt2 = abs(ratio_radii - math.sqrt(2)) / math.sqrt(2) < 0.02
    verdict = (f"R_charge/R_magnetic = {ratio_radii:.3f} ≈ √2 ({abs(ratio_radii - math.sqrt(2))/math.sqrt(2)*100:.1f}% error). "
               f"{'ИНТЕРЕСНОЕ СОВПАДЕНИЕ' if close_to_sqrt2 else 'Близко к √2 но не точно'}.")
    print(f"\n  ВЕРДИКТ: {verdict}")
    return {"ratio_radii": ratio_radii, "sqrt2_error": abs(ratio_radii - math.sqrt(2))/math.sqrt(2)*100}


# ============================================================
# FINAL SUMMARY
# ============================================================
def final_summary(results):
    print(f"\n{'=' * 80}")
    print(f"  ИТОГО: 7 ТЕСТОВ ЭФИРНОЙ ГИПОТЕЗЫ")
    print(f"{'=' * 80}")

    tests = [
        ("#7 Bond lengths", results[7]),
        ("#6 Сверхтекучесть", results[6]),
        ("#5 α ≈ 1/137", results[5]),
        ("#4 MOND", results[4]),
        ("#3 Казимир", results[3]),
        ("#2 Спин 1/2", results[2]),
        ("#1 μ_p протона", results[1]),
    ]

    print(f"""
  ШКАЛА РЕЗУЛЬТАТОВ:
  ─────────────────
  #7 Bond lengths   — model R²={results[7].get('r2',0):.3f}, beats DFT in {results[7].get('model_wins',0)}/{results[7].get('total_comp',0)}
  #6 Сверхтекучесть — κ=h/m = ТАВТОЛОГИЯ, v_c ratio={results[6].get('vc_ratio',0):.1f}
  #5 α = 1/137      — лучшая формула error={results[5].get('best_error_pct',99):.4f}%
  #4 MOND           — a₀/cH₀ = {results[4].get('a0_ratio_cH',0):.1f} (known coincidence)
  #3 Казимир        — correction ~{results[3].get('correction',0):.0e} (unmeasurable)
  #2 Спин 1/2       — согласовано но не предсказательно
  #1 μ_p протона    — R_charge/R_magnetic = {results[1].get('ratio_radii',0):.3f} ≈ √2 (err {results[1].get('sqrt2_error',99):.1f}%)

  ОБЩИЙ ВЫВОД:
  ────────────
  НИ ОДИН тест не дал ОТЛИЧАЮЩЕГОСЯ предсказания от стандартной модели.

  Тороидная модель:
  • Согласована со всеми фактами (#2, #6)
  • Даёт красивые совпадения (#1: √2, #4: cH₀)
  • Но не предсказывает ничего НОВОГО

  Наиболее перспективный тест:
  • #7 (bond lengths) — единственный где есть шанс ПРЕВЗОЙТИ стандарт
  • #1 (μ_p ≈ √2 × ƛ_C·c·m_p/ℏ) — если совпадение подтвердится
    на нейтроне (μ_n = -1.913 μ_N), это было бы интересно

  Для НАСТОЯЩЕГО теста нужно:
  1. Предсказание тороидной модели, которое ОТЛИЧАЕТСЯ от QFT/QCD
  2. Эксперимент который может различить
  3. Пока такого предсказания НЕТ
""")


def main():
    print("=" * 80)
    print("  7 ТЕСТОВ ЭФИРНОЙ ГИПОТЕЗЫ")
    print("  от тестируемого (#7) к спекулятивному (#1)")
    print("=" * 80)

    results = {}
    results[7] = test7_bond_lengths()
    results[6] = test6_superfluid()
    results[5] = test5_alpha()
    results[4] = test4_mond()
    results[3] = test3_casimir()
    results[2] = test2_spin()
    results[1] = test1_proton()

    final_summary(results)


if __name__ == "__main__":
    main()
