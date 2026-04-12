"""
Thick toroidal vortex ring: Dyson (1893) / Fraenkel (1972) expansion.

Find optimal aspect ratio N = R/a by minimizing energy under
various physical constraints.

References:
  - Dyson, F.W. (1893) Phil. Trans. Roy. Soc. A 184, 1041-1106
  - Fraenkel, L.E. (1972) J. Fluid Mech. 51, 119-135
  - Saffman, P.G. (1992) Vortex Dynamics, Cambridge UP, Ch. 10
"""

import math
import numpy as np


# =============================================================================
# 1. Dyson energy expansion: E / (½ρΓ²R) = f(N)
# =============================================================================

def dyson_energy_factor(N, C=7/4):
    """
    Dyson (1893) expansion for energy of thick vortex ring.

    f(N) = ln(8N) - C + (3/8)/N² × (ln(8N) + 1/4) + O(N⁻⁴)

    Parameters:
        N: aspect ratio R/a (must be > 1)
        C: core constant (7/4 solid, 2 hollow)

    Returns:
        f(N) = E / (½ρΓ²R)
    """
    ln8N = math.log(8 * N)
    inv_N2 = 1.0 / (N * N)

    f = ln8N - C
    f += (3.0 / 8.0) * inv_N2 * (ln8N + 0.25)       # O(N⁻²)
    f += (9.0 / 128.0) * inv_N2**2 * (ln8N - 0.5)    # O(N⁻⁴)

    return f


def fraenkel_velocity_factor(N):
    """
    Fraenkel (1972) velocity: V × (4πR/Γ) = ln(8N) - 1/4 - ...
    """
    ln8N = math.log(8 * N)
    inv_N2 = 1.0 / (N * N)

    v = ln8N - 0.25
    v -= (3.0 / 8.0) * inv_N2 * (ln8N - 7.0 / 4.0)

    return v


# =============================================================================
# 2. Self-inductance of thick torus
# =============================================================================

def torus_inductance_factor(N):
    """
    Self-inductance: L = μ₀R × h(N)
    h(N) = ln(8N) - 2 + (1/(4N²)) × (ln(8N) + 1/4) + ...
    """
    ln8N = math.log(8 * N)
    inv_N2 = 1.0 / (N * N)

    h = ln8N - 2.0
    h += 0.25 * inv_N2 * (ln8N + 0.25)

    return h


# =============================================================================
# 3. Core models
# =============================================================================

CORE_MODELS = {
    "Solid rotation (Dyson)": {"C": 7.0 / 4.0, "desc": "C = 7/4 = 1.750"},
    "Hollow core":            {"C": 2.0,        "desc": "C = 2.000"},
    "Rankine vortex":         {"C": 15.0 / 8.0, "desc": "C = 15/8 = 1.875"},
    "Burgers vortex":         {"C": 1.558,       "desc": "C ≈ 1.558"},
}


# =============================================================================
# 4. Combined energy functional (the only one with a minimum)
# =============================================================================

def combined_energy(N, C=7/4, lam=1.0, thick=False):
    """
    Two competing energies:
      E_kin = A × N × f(N)       (kinetic: grows with ring size)
      E_mag = B / (N × h(N))     (magnetic: shrinks with ring size)

    G(N) = N × f(N) + λ / (N × h(N)),  where λ = B/A

    Minimum at finite N where dG/dN = 0.
    """
    if thick:
        f = dyson_energy_factor(N, C)
    else:
        f = math.log(8 * N) - C

    h = torus_inductance_factor(N) if thick else (math.log(8 * N) - 2.0)

    if f <= 0 or h <= 0:
        return float('inf')
    return N * f + lam / (N * h)


# =============================================================================
# 5. Numerical optimization
# =============================================================================

def find_minimum(func, N_min=1.01, N_max=50.0, n_points=200000):
    """Find minimum of func(N) by scanning + golden section refinement."""
    N_arr = np.linspace(N_min, N_max, n_points)
    G_arr = np.array([func(n) for n in N_arr])

    valid = np.isfinite(G_arr)
    if not np.any(valid):
        return None, None

    idx = np.argmin(G_arr[valid])
    N_opt = N_arr[valid][idx]

    # Check if on boundary
    if abs(N_opt - N_min) < 0.1 or abs(N_opt - N_max) < 0.1:
        return N_opt, func(N_opt)  # boundary, not interior minimum

    # Refine with golden section
    a, b = max(N_min, N_opt - 0.5), min(N_max, N_opt + 0.5)
    gr = (math.sqrt(5) + 1) / 2
    for _ in range(100):
        c = b - (b - a) / gr
        d = a + (b - a) / gr
        if func(c) < func(d):
            b = d
        else:
            a = c
    N_opt = (a + b) / 2
    return N_opt, func(N_opt)


# =============================================================================
# 6. ASCII plot
# =============================================================================

def ascii_plot(title, curves, N_range=(1.5, 12.0), width=65, height=18):
    """curves: dict of {name: (N_arr, G_arr, symbol)}"""
    print(f"\n{'=' * width}")
    print(f"  {title}")
    print(f"{'=' * width}")

    N_lo, N_hi = N_range
    all_E = []
    for name, (N_arr, G_arr, sym) in curves.items():
        mask = (N_arr >= N_lo) & (N_arr <= N_hi) & np.isfinite(G_arr)
        all_E.extend(G_arr[mask])

    if not all_E:
        print("  No valid data.")
        return

    E_lo = min(all_E) * 0.95
    E_hi = min(max(all_E), min(all_E) * 3.5)

    grid = [[' '] * width for _ in range(height)]

    legend = []
    for name, (N_arr, G_arr, sym) in curves.items():
        legend.append(f"  {sym} = {name}")
        step = max(1, len(N_arr) // 200)
        for n, g in zip(N_arr[::step], G_arr[::step]):
            if not math.isfinite(g) or n < N_lo or n > N_hi:
                continue
            if g > E_hi or g < E_lo:
                continue
            col = int((n - N_lo) / (N_hi - N_lo) * (width - 1))
            row = int((1 - (g - E_lo) / (E_hi - E_lo)) * (height - 1))
            col = max(0, min(width - 1, col))
            row = max(0, min(height - 1, row))
            if grid[row][col] == ' ':
                grid[row][col] = sym

    for row in grid:
        print(''.join(row))
    print(f"  N: {N_lo:.1f}" + " " * (width - 22) + f"{N_hi:.1f}")
    print(f"  G: {E_lo:.4f} (bottom) .. {E_hi:.4f} (top)")
    for line in legend:
        print(line)


# =============================================================================
# 7. Main
# =============================================================================

def main():
    sep = "=" * 72

    print(sep)
    print("  THICK TOROIDAL VORTEX RING")
    print("  Dyson (1893) / Fraenkel (1972) expansion")
    print("  Optimal N = R/a under various constraints")
    print(sep)

    # =========================================================================
    # Part A: Energy and inductance tables
    # =========================================================================
    print("\n--- A. Энергетический фактор Дайсона f(N) = E/(½ρΓ²R) ---")
    print(f"  {'N':>6s}  {'thin(C=7/4)':>11s}  {'thick Dyson':>11s}  {'Δ%':>8s}")
    for N in [1.5, 2.0, 2.5, 3.0, 5.0, 10.0, 20.0]:
        thin = math.log(8 * N) - 7.0 / 4.0
        thick = dyson_energy_factor(N, C=7.0 / 4.0)
        corr = (thick - thin) / abs(thin) * 100
        print(f"  {N:6.1f}  {thin:11.6f}  {thick:11.6f}  {corr:+7.1f}%")

    print("\n--- B. Фактор индуктивности h(N) = L/(μ₀R) ---")
    print(f"  {'N':>6s}  {'thin':>11s}  {'thick':>11s}  {'Δ%':>8s}")
    for N in [1.5, 2.0, 3.0, 5.0, 10.0]:
        thin = math.log(8 * N) - 2.0
        thick = torus_inductance_factor(N)
        corr = (thick - thin) / abs(thin) * 100
        print(f"  {N:6.1f}  {thin:11.6f}  {thick:11.6f}  {corr:+7.1f}%")

    print("\n--- C. Скорость Фраенкеля V×(4πR/Γ) ---")
    for N in [2.0, 3.0, 5.0, 10.0]:
        v = fraenkel_velocity_factor(N)
        print(f"  N = {N:5.1f}:  {v:.6f}")

    # =========================================================================
    # Part D: Why single-constraint optimization has NO minimum
    # =========================================================================
    print(f"\n{sep}")
    print("  ПОЧЕМУ ОДНООГРАНИЧИТЕЛЬНАЯ ЗАДАЧА НЕ ИМЕЕТ МИНИМУМА")
    print(sep)

    print("""
  Вихревое кольцо с фиксированной циркуляцией Γ и ядром a₀:
    E = (½ρΓ²R) × f(N),  N = R/a₀

  f(N) = ln(8N) - C монотонно растёт → E растёт с R.
  Кольцо ВСЕГДА хочет быть как можно меньше.

  При фиксированном объёме V и циркуляции Γ:
    R ~ N^(2/3),  E ~ N^(2/3) × f(N)  → растёт

  При фиксированном импульсе P и объёме V:
    E ~ f(N)/N²  → убывает при N→∞ (f ~ ln N растёт медленнее N²)
    Кольцо хочет быть бесконечно тонким.

  Вывод: НИ ОДНА стандартная задача с одним ограничением
  не даёт минимума E(N) при конечном N > 1.""")

    # Show the monotone behavior
    print(f"\n  {'N':>6s}  {'N^(2/3)f':>10s}  {'f/N²':>10s}  {'Nf':>10s}")
    for N in [1.5, 2.0, 3.0, 5.0, 10.0, 20.0]:
        f = dyson_energy_factor(N)
        print(f"  {N:6.1f}  {N**(2./3)*f:10.4f}  {f/N**2:10.6f}  {N*f:10.4f}")

    # =========================================================================
    # Part E: Combined energy — the ONLY way to get a minimum
    # =========================================================================
    print(f"\n{sep}")
    print("  БАЛАНС ДВУХ ЭНЕРГИЙ — ЕДИНСТВЕННЫЙ ПУТЬ К МИНИМУМУ")
    print(sep)

    print("""
  Если есть ДВА конкурирующих вклада в энергию:
    E_kin = A × N × f(N)    (кинетическая: растёт с N)
    E_mag = B / (N × h(N))  (магнитная/упругая: убывает с N)

  Полная энергия:
    G(N) = N × f(N) + λ/(N × h(N)),   λ = B/A

  G(N) имеет минимум при конечном N.""")

    # Reference constants
    ref_values = {
        "e":    math.e,
        "π":    math.pi,
        "φ":    (1 + math.sqrt(5)) / 2,
        "e³/8": math.exp(3) / 8,
        "2":    2.0,
        "3":    3.0,
    }

    # --- Thin ring ---
    print(f"\n  --- Тонкое приближение (C = 7/4) ---")
    print(f"  {'λ':>8s}  {'N_opt':>8s}  {'G_min':>8s}  "
          f"{'Ближайшая const':>20s}  {'Δ%':>7s}")

    for lam in [0.1, 0.3, 0.5, 1.0, 2.0, 3.0, 5.0, 8.0, 10.0, 15.0, 20.0,
                30.0, 50.0]:
        N_opt, G_opt = find_minimum(
            lambda n, l=lam: combined_energy(n, 7/4, l, thick=False))
        if N_opt is None:
            continue
        closest_name, closest_val = min(
            ref_values.items(), key=lambda kv: abs(kv[1] - N_opt))
        diff = (N_opt - closest_val) / closest_val * 100
        print(f"  {lam:8.1f}  {N_opt:8.4f}  {G_opt:8.4f}  "
              f"{closest_name:>5s}={closest_val:<7.4f}     {diff:+6.1f}%")

    # --- Thick ring (Dyson corrections) ---
    print(f"\n  --- С коррекциями Дайсона (thick) ---")
    print(f"  {'λ':>8s}  {'N_thin':>8s}  {'N_thick':>8s}  {'Δ(N)':>8s}")

    for lam in [0.5, 1.0, 2.0, 5.0, 10.0, 20.0]:
        N_thin, _ = find_minimum(
            lambda n, l=lam: combined_energy(n, 7/4, l, thick=False))
        N_thick, _ = find_minimum(
            lambda n, l=lam: combined_energy(n, 7/4, l, thick=True))
        if N_thin and N_thick:
            print(f"  {lam:8.1f}  {N_thin:8.4f}  {N_thick:8.4f}  "
                  f"{N_thick-N_thin:+8.4f}")

    # --- Different core models ---
    print(f"\n  --- Разные модели ядра (λ = 10) ---")
    for name, params in CORE_MODELS.items():
        C = params["C"]
        N_opt, G_opt = find_minimum(
            lambda n, c=C: combined_energy(n, c, 10.0, thick=True))
        if N_opt:
            closest_name, closest_val = min(
                ref_values.items(), key=lambda kv: abs(kv[1] - N_opt))
            diff = (N_opt - closest_val) / closest_val * 100
            print(f"  {name:30s}: N = {N_opt:.4f}  "
                  f"(~{closest_name}={closest_val:.3f}, {diff:+.1f}%)")

    # =========================================================================
    # ASCII plot of combined energy
    # =========================================================================
    N_scan = np.linspace(1.2, 12.0, 5000)
    plot_curves = {}
    for lam, sym in [(1.0, '*'), (5.0, '+'), (20.0, 'o')]:
        G_arr = np.array([combined_energy(n, 7/4, lam, thick=True)
                          for n in N_scan])
        plot_curves[f"lambda={lam:.0f}"] = (N_scan, G_arr, sym)

    ascii_plot("G(N) = N*f(N) + lambda/(N*h(N)), Dyson thick", plot_curves)

    # =========================================================================
    # What lambda gives N = pi, e, phi?
    # =========================================================================
    print(f"\n{sep}")
    print("  ПРИ КАКОМ λ ПОЛУЧАЕТСЯ N = π, e, φ ?")
    print(sep)

    special_lambdas = {}

    for target_name, target_val in [("π", math.pi), ("e", math.e),
                                     ("φ", (1+math.sqrt(5))/2)]:
        # Binary search for lambda
        lo, hi = 0.001, 200.0
        for _ in range(200):
            mid = math.sqrt(lo * hi)  # geometric mean for log-scale search
            N_opt, _ = find_minimum(
                lambda n, l=mid: combined_energy(n, 7/4, l, thick=True))
            if N_opt is None or N_opt < target_val:
                lo = mid
            else:
                hi = mid

        lam_found = math.sqrt(lo * hi)
        N_check, G_check = find_minimum(
            lambda n, l=lam_found: combined_energy(n, 7/4, l, thick=True))
        special_lambdas[target_name] = lam_found

        print(f"\n  N_opt = {target_name} ≈ {target_val:.6f}:")
        print(f"    λ = {lam_found:.4f}")
        print(f"    Проверка: N_opt = {N_check:.6f}")
        if target_name == "π":
            print(f"    Отношение E_mag/E_kin ≈ {lam_found:.1f}")

    # =========================================================================
    # СВОДНАЯ ТАБЛИЦА
    # =========================================================================
    print(f"\n{sep}")
    print("  СВОДКА РЕЗУЛЬТАТОВ")
    print(sep)

    print("""
  ┌─────────────────────────────────────────────────────────────────┐
  │ Задача оптимизации         │ Результат                        │
  ├─────────────────────────────────────────────────────────────────┤
  │ Фикс. Γ + фикс. V         │ Нет минимума (E монотонна)       │
  │ Фикс. Γ + фикс. a         │ Нет минимума (E монотонна)       │
  │ Фикс. P + фикс. V         │ E→0 при N→∞ (нет минимума)      │
  │ Баланс E_kin + E_mag       │ Минимум ЕСТЬ, но N = N(λ)       │
  │   λ = 1                    │   N ≈ 1.63 (≈ φ)                │
  │   λ = 5                    │   N ≈ 2.30                       │
  │   λ = 10                   │   N ≈ 2.74 (≈ e)                │
  │   λ ≈ {lam_pi:<5.1f}                │   N ≈ π                          │
  └─────────────────────────────────────────────────────────────────┘
  """.format(lam_pi=special_lambdas.get("π", 0)))

    # =========================================================================
    # ЧЕСТНАЯ ПРОВЕРКА
    # =========================================================================
    print(sep)
    print("  ЧЕСТНАЯ ПРОВЕРКА")
    print(sep)

    lam_pi = special_lambdas.get("π", 0)
    lam_e = special_lambdas.get("e", 0)
    lam_phi = special_lambdas.get("φ", 0)

    print(f"""
  1. ФОРМУЛА ДАЙСОНА — корректная классическая гидродинамика.
     Разложение по (a/R)² сходится для N > 2-3.
     Коррекции: +66% при N=1.5, +29% при N=2, +5% при N=4.

  2. КЛЮЧЕВОЙ ФАКТ: стандартная задача (одно ограничение)
     НЕ ДАЁТ минимума энергии по N.
     - E(N) при фикс. Γ — монотонно растёт
     - E(N) при фикс. P — монотонно убывает
     Физика: нет "предпочтительного" соотношения R/a.

  3. МИНИМУМ ВОЗМОЖЕН при двух конкурирующих энергиях:
     G(N) = N×f(N) + λ/(N×h(N))
     Но результат N_opt ЗАВИСИТ от параметра λ:
       λ = {lam_phi:.1f}  →  N ≈ φ = 1.618
       λ = {lam_e:.1f}  →  N ≈ e = 2.718
       λ = {lam_pi:.1f} →  N ≈ π = 3.142

  4. МОЖНО ЛИ ПОЛУЧИТЬ π ИЗ ПЕРВЫХ ПРИНЦИПОВ?
     Нужно показать, что λ = {lam_pi:.2f} следует из
     фундаментальных констант. Без этого N=π — подгонка.

  5. ВЛИЯНИЕ МОДЕЛИ ЯДРА:
     При одном и том же λ, разные модели ядра дают разные N_opt.
     Разброс ~10-20% между solid/hollow/Rankine.

  6. ИТОГ:
     Формулы Дайсона/Фраенкеля — инструмент для вычисления
     энергии при ЗАДАННОМ N, а не для предсказания N.
     Предсказание N требует дополнительной физики:
     какие энергии конкурируют и каково их отношение.
""")


if __name__ == "__main__":
    main()
