"""
Euler-Cauchy ODE analysis of α-law.

Insight from DeepMind PINN methodology: E(n) = E₁·n^α is the self-similar
ansatz for the Euler-Cauchy ODE:

    n²·E'' + p·n·E' + q·E = 0

Power-law solutions E = n^α exist when:
    α² + (p-1)·α + q = 0  (characteristic equation)

This means:
    α = [(1-p) ± √((p-1)² - 4q)] / 2

Questions:
1. Can we recover (p, q) for each bond from its energy data?
2. Do (p, q) follow patterns across bonds?
3. Does this explain WHY π/σ predicts α?
4. For 2-param model E = E₁·n^(α+β·ln(n)): what ODE does THAT solve?

The β≠0 case corresponds to DEGENERATE Euler-Cauchy (repeated root),
which has solutions n^α·ln(n) — exactly our 2-param model!
"""
import sys
import os
import math

import numpy as np
from scipy.optimize import minimize
from scipy.stats import pearsonr

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alphalaw.data import BONDS

EN = {
    "H": 2.20, "B": 2.04, "C": 2.55, "N": 3.04, "O": 3.44, "F": 3.98,
    "Al": 1.61, "Si": 1.90, "P": 2.19, "S": 2.58, "Cl": 3.16,
    "Ge": 2.01, "As": 2.18, "Se": 2.55, "Sn": 1.96, "Te": 2.10,
}


def analyze_euler_cauchy():
    print("=" * 80)
    print("  Euler-Cauchy ODE → α-law: n²E'' + p·nE' + qE = 0")
    print("  Characteristic eq: α² + (p-1)α + q = 0")
    print("  Solution: E(n) = C₁·n^α₁ + C₂·n^α₂  (or C·n^α·(1 + β·ln(n)) if degenerate)")
    print("=" * 80)

    # ============================================================
    # Part 1: Fit (p, q) for each bond
    # ============================================================
    print(f"\n  ЧАСТЬ 1: Fit (p, q) для каждой связи")
    print("  " + "-" * 60)

    results = []
    for b in BONDS:
        if b.alpha is None:
            continue
        orders = sorted(b.energies.keys())
        if len(orders) < 2:
            continue

        E1 = b.energies[orders[0]]
        n_vals = np.array(orders, dtype=float)
        E_vals = np.array([b.energies[n] for n in orders], dtype=float)

        # For Euler-Cauchy: E(n) = E₁ · n^α  (1-param model)
        # α is the root of α² + (p-1)α + q = 0
        alpha = b.alpha

        # From characteristic equation:
        # If we know α, there are infinitely many (p, q) satisfying
        # α² + (p-1)α + q = 0
        # → q = -α² - (p-1)α = -α² - pα + α
        # One free parameter: choose p to minimize residual on ALL data points

        # For 2-param model E = E₁·n^(α + β·ln(n)):
        alpha_2, beta_2 = b.alpha_beta

        # Fit (p, q) by minimizing the ODE residual directly
        # n²E'' + p·nE' + qE should ≈ 0 at each data point
        def ode_residual(params, n_arr, E_arr):
            p, q = params
            total = 0.0
            for i in range(len(n_arr)):
                n = n_arr[i]
                E = E_arr[i]
                # Numerical derivatives (use power-law model for smooth derivatives)
                # E(n) ≈ E₁ · n^α  →  E' = α·E/n,  E'' = α(α-1)·E/n²
                # But for exact fit with data, use the actual α
                if alpha_2 is not None:
                    a, bb = alpha_2, beta_2
                    ln_n = math.log(n / n_arr[0]) if n > n_arr[0] else 0
                    # E = E₁ · exp(a·ln_n + bb·ln_n²)
                    # dE/dn = E · (a + 2bb·ln_n) / n
                    # d²E/dn² = E · [(a+2bb·ln_n)² - (a+2bb·ln_n) + 2bb] / n²
                    coeff1 = a + 2 * bb * ln_n
                    coeff2 = coeff1 ** 2 - coeff1 + 2 * bb
                    res = n**2 * coeff2 * E / n**2 + p * n * coeff1 * E / n + q * E
                    total += res ** 2
                else:
                    # Simple model: E' = α·E/n, E'' = α(α-1)·E/n²
                    res = alpha * (alpha - 1) * E + p * alpha * E + q * E
                    total += res ** 2
            return total

        # Optimize
        res_opt = minimize(ode_residual, [0.0, 0.0], args=(n_vals, E_vals),
                           method="Nelder-Mead")
        p_fit, q_fit = res_opt.x

        # Analytical: for 1-param model (β=0), the exact solution is
        # α² + (p-1)α + q = 0  →  q = -α² + (1-p)α
        # For minimal |p|: set ∂(p² + q²)/∂p = 0  with constraint
        # → p = α, q = -α²  + (1-α)α = α - 2α² ... nah
        # Simpler: set p=0 → q = -α² + α = α(1-α)
        q_simple = alpha * (1 - alpha)
        p_simple = 0.0

        # Alternative: set q=0 → α² + (p-1)α = 0 → p = 1-α
        p_alt = 1 - alpha
        q_alt = 0.0

        # Discriminant of characteristic equation
        D = (p_fit - 1) ** 2 - 4 * q_fit

        # π/σ ratio
        if 1 in b.energies and 2 in b.energies:
            pi_sigma = (b.energies[2] - b.energies[1]) / b.energies[1]
        else:
            pi_sigma = None

        en_a = EN.get(b.elem_A, 0)
        en_b = EN.get(b.elem_B, 0)

        results.append({
            "bond": b.bond, "block": b.block, "alpha": alpha,
            "beta": beta_2 if beta_2 else 0,
            "p_fit": p_fit, "q_fit": q_fit, "D": D,
            "p_simple": p_simple, "q_simple": q_simple,
            "p_alt": p_alt, "q_alt": q_alt,
            "pi_sigma": pi_sigma,
            "n_orders": len(orders), "orders": orders,
            "delta_en": abs(en_a - en_b),
            "E1": b.energies[orders[0]],
        })

    # Print results
    print(f"\n  {'Bond':>6s} {'α':>6s} {'β':>7s} {'p_fit':>7s} {'q_fit':>7s} "
          f"{'D':>7s} {'π/σ':>6s} {'q=α(1-α)':>9s} {'p=1-α':>6s}")
    print("  " + "-" * 75)

    for r in sorted(results, key=lambda x: x["alpha"]):
        ps_str = f"{r['pi_sigma']:.3f}" if r["pi_sigma"] is not None else "  n/a"
        print(f"  {r['bond']:>6s} {r['alpha']:>6.3f} {r['beta']:>7.3f} "
              f"{r['p_fit']:>7.3f} {r['q_fit']:>7.3f} {r['D']:>7.3f} "
              f"{ps_str:>6s} {r['q_simple']:>9.3f} {r['p_alt']:>6.3f}")

    # ============================================================
    # Part 2: Patterns in (p, q)
    # ============================================================
    print(f"\n\n  ЧАСТЬ 2: Паттерны в параметрах (p, q)")
    print("  " + "-" * 60)

    sp_results = [r for r in results if r["block"] == "s/p" and r["pi_sigma"] is not None]

    # Key insight: for 1-param model with p=0
    # q = α(1-α) → q is the ONLY parameter and it's a parabola in α
    # q > 0 when 0 < α < 1 (crystals)
    # q < 0 when α > 1 (molecules)
    # q = 0 at α = 0 or α = 1 (boundary!)

    q_vals = [r["q_simple"] for r in sp_results]
    ps_vals = [r["pi_sigma"] for r in sp_results]
    alpha_vals = [r["alpha"] for r in sp_results]

    r_q_ps, p_q_ps = pearsonr(q_vals, ps_vals)
    r_q_a, p_q_a = pearsonr(q_vals, alpha_vals)

    print(f"\n  Для p=0 (чистый Euler-Cauchy без первой производной):")
    print(f"    q = α(1-α)")
    print(f"    q > 0 → 0 < α < 1 → кристаллы")
    print(f"    q < 0 → α > 1 → молекулы")
    print(f"    q = 0 → α = 1 → ГРАНИЦА")
    print(f"\n    r(q, π/σ) = {r_q_ps:.4f} (p={p_q_ps:.2e})")
    print(f"    r(q, α)   = {r_q_a:.4f} (p={p_q_a:.2e})")

    # Check: is q = α(1-α) related to π/σ?
    # π/σ = 2^α - 1 for power law
    # q = α(1-α) = α - α²
    # Can we express q through π/σ?
    # If α ≈ 0.699·(π/σ) + 0.242 (linear fit), then:
    # q = α - α² = α(1-α)

    print(f"\n  Связь q и π/σ через α:")
    print(f"    α = 0.699·(π/σ) + 0.242")
    print(f"    q = α(1-α) = [0.699·(π/σ) + 0.242]·[1 - 0.699·(π/σ) - 0.242]")
    print(f"    q = [0.699·(π/σ) + 0.242]·[0.758 - 0.699·(π/σ)]")
    print(f"    → q is a DOWNWARD PARABOLA in π/σ with root at π/σ ≈ 1.084")

    # ============================================================
    # Part 3: Why π/σ predicts α — the ODE explanation
    # ============================================================
    print(f"\n\n  ЧАСТЬ 3: ПОЧЕМУ π/σ предсказывает α — объяснение через ODE")
    print("  " + "-" * 60)

    # For E(n) = E₁·n^α:
    # E(2) = E₁·2^α
    # π/σ = (E(2) - E(1)) / E(1) = 2^α - 1
    # So: α = log₂(1 + π/σ)
    # This is EXACT, not approximate!

    print(f"\n  ТОЧНОЕ соотношение (для E(n) = E₁·n^α):")
    print(f"    π/σ = (E₂ - E₁)/E₁ = E₁·2^α/E₁ - 1 = 2^α - 1")
    print(f"    → α = log₂(1 + π/σ)")
    print(f"    → r(α, π/σ) должен быть ~ 1.0 для точной степенной модели")

    # Verify: compute α_exact = log₂(1 + π/σ) vs actual α
    print(f"\n  Проверка: α_exact = log₂(1+π/σ) vs α_measured")
    print(f"  {'Bond':>6s} {'α_meas':>7s} {'α_exact':>7s} {'Δα':>7s} {'π/σ':>6s}")
    print("  " + "-" * 42)

    alpha_exact = []
    alpha_meas = []
    for r in sorted(sp_results, key=lambda x: x["pi_sigma"]):
        a_exact = math.log2(1 + r["pi_sigma"])
        err = r["alpha"] - a_exact
        alpha_exact.append(a_exact)
        alpha_meas.append(r["alpha"])
        print(f"  {r['bond']:>6s} {r['alpha']:>7.3f} {a_exact:>7.3f} "
              f"{err:>+7.3f} {r['pi_sigma']:>6.3f}")

    r_exact, p_exact = pearsonr(alpha_meas, alpha_exact)
    mse_exact = np.mean([(a - b) ** 2 for a, b in zip(alpha_meas, alpha_exact)])
    print(f"\n  r(α_measured, α_exact) = {r_exact:.6f}")
    print(f"  MSE = {mse_exact:.6f}")
    print(f"  RMSE = {math.sqrt(mse_exact):.4f}")

    # Compare with linear fit
    alpha_linear = [0.699 * r["pi_sigma"] + 0.242 for r in sp_results]
    mse_linear = np.mean([(a - b) ** 2 for a, b in zip(alpha_meas, alpha_linear)])
    print(f"\n  Сравнение:")
    print(f"    Exact (log₂):  RMSE = {math.sqrt(mse_exact):.4f}")
    print(f"    Linear (0.699): RMSE = {math.sqrt(mse_linear):.4f}")

    # ============================================================
    # Part 4: 2-param model → degenerate Euler-Cauchy
    # ============================================================
    print(f"\n\n  ЧАСТЬ 4: 2-параметрическая модель → вырожденный Euler-Cauchy")
    print("  " + "-" * 60)

    # E = E₁·n^(α + β·ln(n)) = E₁·n^α · n^(β·ln(n)) = E₁·n^α · exp(β·(ln n)²)
    # This is NOT a solution of Euler-Cauchy.
    # But the standard degenerate case (repeated root α) has:
    # E = (C₁ + C₂·ln(n)) · n^α
    # This looks like our model with β → C₂/C₁ correction.

    # Check: how well does the DEGENERATE solution fit?
    # E_degen(n) = E₁ · n^α · (1 + γ·ln(n))
    # At n=1: E₁ (correct)
    # At n=2: E₁ · 2^α · (1 + γ·ln(2))
    # At n=3: E₁ · 3^α · (1 + γ·ln(3))

    print(f"\n  Вырожденный Euler-Cauchy (repeated root α):")
    print(f"    E(n) = E₁ · n^α · (1 + γ·ln(n))")
    print(f"    ODE: n²E'' + (1-2α)·nE' + α²·E = 0")
    print(f"    (p = 1-2α, q = α²)")

    # For each bond with 3+ orders, fit γ
    print(f"\n  {'Bond':>6s} {'α':>6s} {'β(2-param)':>10s} {'γ(degen)':>9s} "
          f"{'RMSE_2p':>8s} {'RMSE_dg':>8s}")
    print("  " + "-" * 55)

    for r in sorted(results, key=lambda x: x["alpha"]):
        if r["n_orders"] < 3:
            continue

        alpha = r["alpha"]
        b_data = next(b for b in BONDS if b.bond == r["bond"])
        orders = sorted(b_data.energies.keys())
        E1 = b_data.energies[orders[0]]
        n_vals = np.array(orders, dtype=float)
        E_vals = np.array([b_data.energies[n] for n in orders], dtype=float)

        # 2-param model: E = E₁ · exp(α·ln(n) + β·ln(n)²)
        a2, b2 = b_data.alpha_beta
        E_2param = np.array([E1 * math.exp(a2 * math.log(n) + b2 * math.log(n)**2)
                             for n in n_vals])
        rmse_2p = math.sqrt(np.mean((E_2param - E_vals) ** 2))

        # Degenerate: E = E₁ · n^α · (1 + γ·ln(n))
        # Fit γ by least squares
        ln_n = np.log(n_vals)
        n_alpha = n_vals ** alpha
        # E_vals = E1 * n_alpha * (1 + γ*ln_n)
        # E_vals/(E1*n_alpha) = 1 + γ*ln_n
        ratio = E_vals / (E1 * n_alpha)
        # ratio = 1 + γ*ln_n → γ = (ratio - 1) / ln_n (for n > 1)
        mask = n_vals > 1
        if mask.sum() > 0:
            gamma = np.mean((ratio[mask] - 1) / ln_n[mask])
            E_degen = E1 * n_alpha * (1 + gamma * ln_n)
            rmse_dg = math.sqrt(np.mean((E_degen - E_vals) ** 2))
        else:
            gamma = 0
            rmse_dg = rmse_2p

        print(f"  {r['bond']:>6s} {alpha:>6.3f} {b2:>10.4f} {gamma:>9.4f} "
              f"{rmse_2p:>8.1f} {rmse_dg:>8.1f}")

    # ============================================================
    # Part 5: The physics — what does p mean?
    # ============================================================
    print(f"\n\n  ЧАСТЬ 5: Физический смысл параметров ODE")
    print("  " + "-" * 60)

    print(f"""
  Уравнение Эйлера-Коши: n²·E'' + p·n·E' + q·E = 0

  Переписываем в стандартной форме (делим на n²):
    E'' + (p/n)·E' + (q/n²)·E = 0

  Сравним с уравнением Шрёдингера: -ψ'' + V(x)·ψ = E·ψ
    → V(n) = -q/n² — обратноквадратичный потенциал!

  Физическая интерпретация:
  • n = bond order (координата)
  • E(n) = энергия связи (волновая функция)
  • p/n = "трение" (диссипация при увеличении кратности)
  • q/n² = потенциал — ПРИТЯЖЕНИЕ если q > 0 (кристаллы),
                        ОТТАЛКИВАНИЕ если q < 0 (молекулы)

  Для p = 0 (чистый потенциал):
    q = α(1-α)
    α < 1 → q > 0 → притягивающий потенциал → E(n) растёт медленно → кристалл
    α > 1 → q < 0 → отталкивающий потенциал → E(n) растёт быстро → молекула
    α = 1 → q = 0 → свободная частица → ГРАНИЦА молекула/кристалл

  Это объясняет ПОЧЕМУ граница α = 1:
    α = 1 — это точка где потенциал V(n) = 0, т.е.
    электронные облака НЕ создают ни притяжения, ни отталкивания
    при увеличении кратности связи.

  π/σ = 2^α - 1 → π/σ = 1 при α = 1 → q = 0
    Граница π/σ = 1 = граница V = 0 = граница между
    притягивающим и отталкивающим потенциалом в n-пространстве.
""")

    # ============================================================
    # Part 6: Connection to RemizovNet
    # ============================================================
    print(f"  ЧАСТЬ 6: Связь с RemizovNet")
    print("  " + "-" * 60)

    print(f"""
  RemizovNet решает: a(x)·y'' + b(x)·y' + c(x)·y = g(x)

  Euler-Cauchy:       n²·E'' + p·n·E' + q·E = 0
  Замена переменных:  x = ln(n), E(n) = u(x)

  Тогда: E' = u'/n, E'' = (u'' - u')/n²
  → n²·(u'' - u')/n² + p·n·u'/n + q·u = 0
  → u'' + (p-1)·u' + q·u = 0

  Это ODE с ПОСТОЯННЫМИ коэффициентами!
  a = 1, b = (p-1), c = q

  В координатах x = ln(n):
  • x = 0 → n = 1 (одинарная связь)
  • x = ln(2) ≈ 0.693 → n = 2 (двойная)
  • x = ln(3) ≈ 1.099 → n = 3 (тройная)

  RemizovNet МОГ БЫ решить это, НО:
  • Коэффициенты ПОСТОЯННЫЕ → ODE тривиально
  • Всего 2-6 точек на ось → слишком мало
  • RemizovNet не добавляет ценности к аналитическому решению

  ВЫВОД: RemizovNet не нужен для ЭТОЙ задачи.
  Аналитика (Euler-Cauchy) полностью описывает α-law.
""")


def main():
    analyze_euler_cauchy()


if __name__ == "__main__":
    main()
