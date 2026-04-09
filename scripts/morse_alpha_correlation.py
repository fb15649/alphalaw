#!/usr/bin/env python3
"""
Direction 3: Correlate Morse anharmonicity x_e with α-law exponent.
Hypothesis: high x_e → α < 1 (shallow well → diminishing returns).
"""
import math
import numpy as np
from scipy import stats

# Spectroscopic constants from Huber & Herzberg (1979) / NIST
# ω_e (cm⁻¹), ω_eχ_e (cm⁻¹) for homonuclear diatomics
# x_e = ω_eχ_e / ω_e (dimensionless anharmonicity)
# α from E(n) = E₁ × n^α (our α-law)
# 3β_Morse = 6×x_e (anharmonicity parameter from two-level model)

# (element, omega_e, omega_e_xe, x_e, alpha, LP_min, period)
DATA = [
    # s/p block homonuclear (x_e from diatomic, α from bond orders 1,2,3)
    ("C-C",   1854.7, 13.34, None,  0.770, 0, 2),
    ("N-N",   2358.6, 14.32, None,  2.012, 1, 2),
    ("O-O",   1580.2, 12.07, None,  1.770, 2, 2),
    ("Si-Si",  510.9,  2.02, None,  0.485, 0, 3),
    ("P-P",    780.8,  2.84, None,  1.283, 1, 3),
    ("S-S",    725.7,  2.84, None,  0.676, 2, 3),
    ("Ge-Ge",  286.0,  0.96, None,  0.407, 0, 4),
    ("Sn-Sn",  186.2,  0.26, None,  0.330, 0, 5),
]

# Compute x_e
for i, (name, we, wexe, _, alpha, lp, per) in enumerate(DATA):
    DATA[i] = (name, we, wexe, wexe / we, alpha, lp, per)

def analyze():
    print("=" * 70)
    print("MORSE ANHARMONICITY x_e vs α-LAW EXPONENT")
    print("=" * 70)

    print(f"\n{'Bond':>6} {'ω_e':>8} {'ω_eχ_e':>8} {'x_e':>8} {'3β':>6} "
          f"{'α':>6} {'LP':>3} {'Per':>3}")
    print("-" * 60)

    for name, we, wexe, xe, alpha, lp, per in DATA:
        beta3 = 6 * xe
        print(f"{name:>6} {we:8.1f} {wexe:8.2f} {xe:8.5f} {beta3:6.3f} "
              f"{alpha:6.3f} {lp:>3} {per:>3}")

    # Extract arrays
    xe_vals = [d[3] for d in DATA]
    alpha_vals = [d[4] for d in DATA]
    lp_vals = [d[5] for d in DATA]
    per_vals = [d[6] for d in DATA]
    beta3_vals = [6 * d[3] for d in DATA]

    # Correlation tests
    print("\n" + "=" * 50)
    print("CORRELATIONS")
    print("=" * 50)

    rho, p = stats.spearmanr(xe_vals, alpha_vals)
    print(f"Spearman(x_e, α): ρ = {rho:.3f}, p = {p:.4f}")

    r, p_r = stats.pearsonr(xe_vals, alpha_vals)
    print(f"Pearson(x_e, α):  r = {r:.3f}, p = {p_r:.4f}")

    rho2, p2 = stats.spearmanr(beta3_vals, alpha_vals)
    print(f"Spearman(3β, α):  ρ = {rho2:.3f}, p = {p2:.4f}")

    # Two-level model: separate LP=0 and LP>0
    print("\n" + "=" * 50)
    print("TWO-LEVEL MODEL: α = f(LP) + g(3β)")
    print("=" * 50)

    lp0 = [(d[3], d[4]) for d in DATA if d[5] == 0]
    lp1plus = [(d[3], d[4]) for d in DATA if d[5] >= 1]

    if len(lp0) >= 2:
        xe0, a0 = zip(*lp0)
        beta3_0 = [6*x for x in xe0]
        if len(lp0) >= 3:
            slope, intercept, r, p, se = stats.linregress(beta3_0, a0)
            print(f"\nLP=0: α = {intercept:.3f} + {slope:.3f} × 3β")
            print(f"  r = {r:.3f}, p = {p:.4f}, R² = {r**2:.3f}")
            print(f"  Points: {', '.join(f'{d[0]}' for d in DATA if d[5]==0)}")
        else:
            print(f"\nLP=0: only {len(lp0)} points, need ≥3 for regression")

    if len(lp1plus) >= 2:
        xe1, a1 = zip(*lp1plus)
        beta3_1 = [6*x for x in xe1]
        if len(lp1plus) >= 3:
            slope, intercept, r, p, se = stats.linregress(beta3_1, a1)
            print(f"\nLP≥1: α = {intercept:.3f} + {slope:.3f} × 3β")
            print(f"  r = {r:.3f}, p = {p:.4f}, R² = {r**2:.3f}")
            print(f"  Points: {', '.join(f'{d[0]}' for d in DATA if d[5]>=1)}")
        else:
            print(f"\nLP≥1: only {len(lp1plus)} points, need ≥3 for regression")

    # Overall two-level model fit
    print("\n" + "=" * 50)
    print("COMBINED MODEL: α = a + b×LP + c×3β + d×LP×3β")
    print("=" * 50)

    X = np.column_stack([
        np.ones(len(DATA)),
        [d[5] for d in DATA],  # LP
        beta3_vals,             # 3β
        [d[5] * 6 * d[3] for d in DATA],  # LP × 3β interaction
    ])
    y = np.array(alpha_vals)

    if len(DATA) > 4:
        # OLS fit
        coeffs, residuals, rank, sv = np.linalg.lstsq(X, y, rcond=None)
        y_pred = X @ coeffs
        ss_res = np.sum((y - y_pred)**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        r2 = 1 - ss_res / ss_tot

        print(f"α = {coeffs[0]:.3f} + {coeffs[1]:.3f}×LP + "
              f"{coeffs[2]:.3f}×3β + {coeffs[3]:.3f}×LP×3β")
        print(f"R² = {r2:.3f}")

        # Predict vs actual
        print(f"\n{'Bond':>6} {'α_actual':>8} {'α_pred':>8} {'Δ':>8}")
        for i, d in enumerate(DATA):
            print(f"{d[0]:>6} {d[4]:8.3f} {y_pred[i]:8.3f} "
                  f"{y_pred[i]-d[4]:+8.3f}")

    # Physical interpretation
    print("\n" + "=" * 50)
    print("PHYSICAL INTERPRETATION")
    print("=" * 50)
    print("""
x_e = ω_eχ_e / ω_e = anharmonicity parameter
  - High x_e → shallow potential well → bonds weaken quickly → α < 1
  - Low x_e → deep, nearly harmonic well → bonds retain strength → α ≥ 1

3β = 6×x_e = Morse anharmonicity = "soil quality" in Seed Law
  - LP = "seed presence" (has reserve or not)
  - 3β = "soil fertility" (how well the reserve converts to bond strength)

Two-level model: LP determines IF there's synergy, 3β determines HOW MUCH.
""")


if __name__ == "__main__":
    analyze()
