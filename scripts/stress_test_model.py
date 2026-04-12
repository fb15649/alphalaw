"""
Stress test: trying to BREAK the unified toroid model.

We attack every testable prediction and look for counterexamples.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alphalaw.data import BONDS, ELEMENTS

PHI = (1 + math.sqrt(5)) / 2

# Atomic covalent radii (pm) from CRC Handbook
RADII = {
    "H": 31, "He": 28, "Li": 128, "Be": 96, "B": 84, "C": 76, "N": 71,
    "O": 66, "F": 57, "Ne": 58, "Na": 166, "Mg": 141, "Al": 121, "Si": 111,
    "P": 107, "S": 105, "Cl": 102, "Ar": 106, "K": 203, "Ca": 176,
    "Sc": 170, "Ti": 160, "V": 153, "Cr": 139, "Mn": 139, "Fe": 132,
    "Co": 126, "Ni": 124, "Cu": 132, "Zn": 122, "Ga": 122, "Ge": 120,
    "As": 119, "Se": 120, "Br": 120, "Kr": 116, "Mo": 154, "Sn": 139,
    "Sb": 139, "Te": 138, "I": 139, "W": 162, "Re": 151, "Pb": 146,
}


def get_max_radius(bond_data):
    """Get the larger covalent radius of the two atoms."""
    r_a = RADII.get(bond_data.elem_A, 0)
    r_b = RADII.get(bond_data.elem_B, 0)
    return max(r_a, r_b)


def test_1_compact_toroid():
    """
    ТЕСТ 1: Компактный тороид → α > 1

    Предсказание модели: чем меньше атомный радиус, тем выше α.
    Атаку: найти БОЛЬШИЕ атомы с высоким α или МАЛЕНЬКИЕ с низким.
    """
    print("=" * 80)
    print("ТЕСТ 1: Компактный тороид (малый радиус) → высокий α?")
    print("=" * 80)

    rows = []
    for b in BONDS:
        a = b.alpha
        if a is None:
            continue
        r = get_max_radius(b)
        if r == 0:
            continue
        rows.append((b.bond, a, r, b.period, b.block))

    rows.sort(key=lambda x: x[2])

    print(f"\n{'Связь':<8} {'α':>6} {'r_max(пм)':>10} {'Период':>7} {'Блок':<5}")
    print("-" * 50)
    for bond, alpha, r, period, block in rows:
        marker = ""
        if r <= 85 and alpha < 1:
            marker = " ◄ КОМПАКТНЫЙ, но α<1!"
        if r >= 120 and alpha > 1:
            marker = " ◄ БОЛЬШОЙ, но α>1!"
        print(f"{bond:<8} {alpha:>6.3f} {r:>10} {period:>7} {block:<5}{marker}")

    # Correlation
    alphas = [a for _, a, _, _, _ in rows]
    radii = [r for _, _, r, _, _ in rows]
    n = len(alphas)
    mean_a = sum(alphas) / n
    mean_r = sum(radii) / n
    cov = sum((a - mean_a) * (r - mean_r) for a, r in zip(alphas, radii)) / n
    std_a = (sum((a - mean_a)**2 for a in alphas) / n) ** 0.5
    std_r = (sum((r - mean_r)**2 for r in radii) / n) ** 0.5
    r_corr = cov / (std_a * std_r) if std_a * std_r > 0 else 0

    print(f"\n  Pearson r(α, r_max) = {r_corr:.3f}")

    # Count anomalies
    compact_low = [(b, a, r) for b, a, r, _, _ in rows if r <= 85 and a < 1]
    big_high = [(b, a, r) for b, a, r, _, _ in rows if r >= 120 and a > 1]

    print(f"\n  Аномалии:")
    print(f"    Компактный (r≤85 пм) но α<1: {len(compact_low)}")
    for b, a, r in compact_low:
        print(f"      {b}: r={r} пм, α={a:.3f}")
    print(f"    Большой (r≥120 пм) но α>1: {len(big_high)}")
    for b, a, r in big_high:
        print(f"      {b}: r={r} пм, α={a:.3f}")


def test_2_octave_boundary():
    """
    ТЕСТ 2: Граница октавы R₂ = 2

    Предсказание: для s/p-блока R₂ > 2 → молекула, R₂ < 2 → кристалл.
    Атака: найти кристаллы с R₂ > 2 или молекулы с R₂ < 2 в s/p-блоке.
    """
    print("\n" + "=" * 80)
    print("ТЕСТ 2: Граница октавы R₂ = 2 (s/p-блок)")
    print("=" * 80)

    d_block = {"Cr-Cr", "Mo-Mo", "W-W", "Re-Re", "Ti-O", "Fe-C", "W-C"}

    violations = []
    near_boundary = []

    for b in BONDS:
        if b.bond in d_block:
            continue
        if 1 not in b.energies or 2 not in b.energies:
            continue
        R2 = b.energies[2] / b.energies[1]
        alpha = b.alpha
        if alpha is None:
            continue

        is_mol = alpha > 1
        if is_mol and R2 < 2:
            violations.append((b.bond, alpha, R2, "МОЛЕКУЛА с R₂<2"))
        elif not is_mol and R2 > 2:
            violations.append((b.bond, alpha, R2, "КРИСТАЛЛ с R₂>2"))

        if abs(R2 - 2) < 0.15:
            near_boundary.append((b.bond, alpha, R2))

    print(f"\n  Нарушения (s/p-блок):")
    if violations:
        for bond, alpha, R2, desc in violations:
            print(f"    {bond}: α={alpha:.3f}, R₂={R2:.4f} — {desc}")
    else:
        print(f"    Нет нарушений ✓")

    print(f"\n  Связи вблизи границы (|R₂-2| < 0.15):")
    for bond, alpha, R2 in sorted(near_boundary, key=lambda x: x[2]):
        typ = "МОЛ" if alpha > 1 else "КРИСТ"
        print(f"    {bond}: α={alpha:.3f}, R₂={R2:.4f}, {typ}")


def test_3_period2_rule():
    """
    ТЕСТ 3: Period 2 → α > 1?

    Предсказание: компактные тороиды Period 2 дают α > 1 (если LP > 0).
    Атака: найти связи Period 2 с α < 1.
    """
    print("\n" + "=" * 80)
    print("ТЕСТ 3: Period 2 + неспаренные пары → α > 1?")
    print("=" * 80)

    period2_bonds = []
    for b in BONDS:
        if b.alpha is None:
            continue
        if b.period == 2:
            period2_bonds.append((b.bond, b.alpha, b.LP_min, b.elem_A, b.elem_B))

    period2_bonds.sort(key=lambda x: x[1])

    print(f"\n{'Связь':<8} {'α':>6} {'LP_min':>7} {'Элементы':<10} {'α>1?':<6}")
    print("-" * 45)
    for bond, alpha, lp, ea, eb in period2_bonds:
        result = "ДА" if alpha > 1 else "НЕТ ◄"
        print(f"{bond:<8} {alpha:>6.3f} {lp:>7} {ea}-{eb:<7} {result}")

    p2_below = [(b, a, lp) for b, a, lp, _, _ in period2_bonds if a < 1]
    print(f"\n  Period 2 с α < 1: {len(p2_below)} из {len(period2_bonds)}")
    if p2_below:
        print("  Это НАРУШЕНИЕ модели если LP > 0:")
        for b, a, lp in p2_below:
            marker = "НАРУШЕНИЕ" if lp > 0 else "OK (LP=0, ожидаемо)"
            print(f"    {b}: α={a:.3f}, LP_min={lp} — {marker}")


def test_4_lone_pairs():
    """
    ТЕСТ 4: Без lone pairs → всегда α < 1?

    Предсказание: LP_min=0 означает нет свободных боковых потоков → нет π → α<1.
    Атака: найти LP_min=0 с α > 1 (кроме d-блока).
    """
    print("\n" + "=" * 80)
    print("ТЕСТ 4: LP_min=0 → α < 1? (нет свободных потоков → нет π)")
    print("=" * 80)

    for b in BONDS:
        if b.alpha is None or b.block == "d":
            continue
        if b.LP_min == 0 and b.alpha > 1:
            print(f"  НАРУШЕНИЕ: {b.bond}: α={b.alpha:.3f}, LP_min=0")

    lp0_bonds = [(b.bond, b.alpha) for b in BONDS
                 if b.alpha and b.block != "d" and b.LP_min == 0]
    lp_pos = [(b.bond, b.alpha) for b in BONDS
              if b.alpha and b.block != "d" and b.LP_min > 0]

    if lp0_bonds:
        avg_lp0 = sum(a for _, a in lp0_bonds) / len(lp0_bonds)
        max_lp0 = max(a for _, a in lp0_bonds)
        print(f"\n  LP=0: n={len(lp0_bonds)}, α средний={avg_lp0:.3f}, α макс={max_lp0:.3f}")
    if lp_pos:
        avg_lp = sum(a for _, a in lp_pos) / len(lp_pos)
        min_lp = min(a for _, a in lp_pos)
        print(f"  LP>0: n={len(lp_pos)}, α средний={avg_lp:.3f}, α мин={min_lp:.3f}")

    all_lp0_below = all(a < 1 for _, a in lp0_bonds)
    print(f"\n  Все LP=0 имеют α < 1: {'ДА ✓' if all_lp0_below else 'НЕТ ✗'}")


def test_5_self_consistency():
    """
    ТЕСТ 5: Самосогласованность — предсказания не противоречат друг другу?

    Проверяем: если α определяется компактностью (радиусом), то одинаковые
    атомы в разных связях должны давать ПОХОЖИЙ вклад в α.
    """
    print("\n" + "=" * 80)
    print("ТЕСТ 5: Самосогласованность — один элемент → стабильный вклад?")
    print("=" * 80)

    element_alphas = {}
    for b in BONDS:
        if b.alpha is None:
            continue
        for elem in [b.elem_A, b.elem_B]:
            if elem not in element_alphas:
                element_alphas[elem] = []
            element_alphas[elem].append((b.bond, b.alpha))

    print(f"\n{'Элемент':<6} {'Мин α':>7} {'Макс α':>7} {'Размах':>7} {'n':>3} {'Связи'}")
    print("-" * 70)
    for elem in sorted(element_alphas.keys()):
        vals = element_alphas[elem]
        if len(vals) < 2:
            continue
        alphas = [a for _, a in vals]
        spread = max(alphas) - min(alphas)
        bonds = ", ".join(b for b, _ in vals[:5])
        marker = " ◄ НЕСТАБИЛЬНЫЙ" if spread > 0.8 else ""
        print(f"{elem:<6} {min(alphas):>7.3f} {max(alphas):>7.3f} {spread:>7.3f} {len(vals):>3} {bonds}{marker}")


def test_6_hetero_symmetry():
    """
    ТЕСТ 6: Гетероядерные — модель симметрична?

    Если A-B имеет α, то КАКОЙ тороид определяет результат?
    Модель говорит: больший тороид (max radius) ограничивает π-связь.
    Проверяем: α определяется БОЛЬШИМ атомом?
    """
    print("\n" + "=" * 80)
    print("ТЕСТ 6: В гетероядерных связях α определяет БОЛЬШИЙ атом?")
    print("=" * 80)

    rows = []
    for b in BONDS:
        if b.alpha is None or b.elem_A == b.elem_B or b.block == "d":
            continue
        r_a = RADII.get(b.elem_A, 0)
        r_b = RADII.get(b.elem_B, 0)
        r_max = max(r_a, r_b)
        r_min = min(r_a, r_b)
        bigger = b.elem_A if r_a >= r_b else b.elem_B
        smaller = b.elem_B if r_a >= r_b else b.elem_A
        rows.append((b.bond, b.alpha, r_max, r_min, bigger, smaller, b.period))

    rows.sort(key=lambda x: x[2])

    print(f"\n{'Связь':<8} {'α':>6} {'r_big':>6} {'r_small':>7} {'Больший':<8} {'Период':>7}")
    print("-" * 55)
    for bond, alpha, r_max, r_min, bigger, smaller, period in rows:
        print(f"{bond:<8} {alpha:>6.3f} {r_max:>6} {r_min:>7} {bigger:<8} {period:>7}")


if __name__ == "__main__":
    test_1_compact_toroid()
    test_2_octave_boundary()
    test_3_period2_rule()
    test_4_lone_pairs()
    test_5_self_consistency()
    test_6_hetero_symmetry()

    print("\n" + "=" * 80)
    print("ИТОГО: ВЕРДИКТ")
    print("=" * 80)
