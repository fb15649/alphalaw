"""
Cluster geometry: why N₂ (dimer) but P₄ (tetrahedron) but Si (crystal)?

Hypothesis from toroid model:
- Halbach (α>1): concentrate all bonds on ONE partner → dimer
- Competition (α<1): distribute bonds to MANY partners → cluster/crystal

Cluster CN = how many partners an atom chooses.
Cluster shape = smallest closed figure with that CN.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alphalaw.data import BONDS

# Known molecular forms of elements in standard/common state
# Format: element, cluster_formula, CN_in_cluster, shape, state
ELEMENT_CLUSTERS = [
    # Group 14
    ("C",  "C(diamond)", 4, "бескон. тетраэдр.", "кристалл"),
    ("C",  "C₆₀",       3, "усечённый икосаэдр", "молекула"),
    ("Si", "Si(diamond)",4, "бескон. тетраэдр.", "кристалл"),
    ("Ge", "Ge(diamond)",4, "бескон. тетраэдр.", "кристалл"),
    ("Sn", "Sn(β)",      4, "искаж. тетраэдр.", "кристалл"),

    # Group 15
    ("N",  "N₂",         1, "димер",       "молекула"),
    ("P",  "P₄",         3, "тетраэдр",    "молекула"),
    ("P",  "P(чёрный)",  3, "бескон. слои", "кристалл"),
    ("As", "As₄",        3, "тетраэдр",    "молекула (газ)"),
    ("As", "As(серый)",   3, "бескон. слои", "кристалл"),
    ("Sb", "Sb(серый)",   3, "бескон. слои", "кристалл"),

    # Group 16
    ("O",  "O₂",         1, "димер",       "молекула"),
    ("O",  "O₃",         2, "угловая",     "молекула"),
    ("S",  "S₈",         2, "октагон",     "молекула"),
    ("S",  "S(цепи)",    2, "бескон. цепи", "полимер"),
    ("Se", "Se₈",        2, "октагон",     "молекула"),
    ("Se", "Se(цепи)",   2, "бескон. цепи", "кристалл"),
    ("Te", "Te(цепи)",   2, "бескон. цепи", "кристалл"),

    # Group 17
    ("F",  "F₂",         1, "димер",       "молекула"),
    ("Cl", "Cl₂",        1, "димер",       "молекула"),
    ("Br", "Br₂",        1, "димер",       "молекула"),
    ("I",  "I₂",         1, "димер",       "молекула"),

    # Group 13
    ("B",  "B₁₂",       5, "икосаэдр",    "кристалл"),
]


def main():
    print("=" * 80)
    print("КЛАСТЕРНАЯ ГЕОМЕТРИЯ: какую фигуру выбирает элемент?")
    print("=" * 80)

    # Get alpha for homonuclear bonds
    alphas = {}
    for b in BONDS:
        if b.elem_A == b.elem_B and b.alpha is not None:
            alphas[b.elem_A] = b.alpha

    # Valence and LP
    from alphalaw.data import ELEMENTS
    elem_props = {}
    for sym, (period, group, block, valence, lp) in ELEMENTS.items():
        bonding_cap = valence - 2 * lp if lp >= 0 else valence
        elem_props[sym] = {
            "period": period, "group": group, "valence": valence,
            "lp": lp, "bonding_cap": bonding_cap,
        }

    print(f"\n  {'Элем':<4} {'α':>5} {'Вал':>4} {'LP':>3} {'Связ.':>5} "
          f"{'Кластер':<14} {'КЧ':>3} {'Форма':<20} {'Сост.':<10}")
    print(f"  {'-'*80}")

    for elem, formula, cn, shape, state in ELEMENT_CLUSTERS:
        a = alphas.get(elem, None)
        a_str = f"{a:.3f}" if a else "  —  "
        props = elem_props.get(elem, {})
        val = props.get("valence", "?")
        lp = props.get("lp", "?")
        bc = props.get("bonding_cap", "?")
        print(f"  {elem:<4} {a_str:>5} {val:>4} {lp:>3} {bc:>5} "
              f"{formula:<14} {cn:>3} {shape:<20} {state:<10}")

    # Key pattern
    print(f"\n{'='*80}")
    print("ПАТТЕРН: α → режим → КЧ кластера → форма")
    print(f"{'='*80}")

    print("""
  Хальбах (α > 1): СКОНЦЕНТРИРОВАТЬ все связи на одном партнёре
    → Все электроны связывания → один → высокий порядок → КЧ = 1
    → Димер (N₂, O₂, F₂, Cl₂, Br₂, I₂)

  Конкуренция (α < 1): РАЗДАТЬ связи многим партнёрам
    КЧ зависит от числа доступных связей = валентность − 2·LP:

    Связ. = 2 → КЧ = 2 → кольцо или цепь (S₈, Se₈, Te цепи)
    Связ. = 3 → КЧ = 3 → тетраэдр (P₄, As₄) или слои (As, Sb, графит)
    Связ. = 4 → КЧ = 4 → алмазная решётка (C, Si, Ge, Sn) — бескон. кристалл
    Связ. = 5 → КЧ = 5 → икосаэдр (B₁₂)
    """)

    # Why tetrahedron for CN=3?
    print(f"{'='*80}")
    print("ПОЧЕМУ ТЕТРАЭДР ДЛЯ КЧ=3?")
    print(f"{'='*80}")

    print("""
  КЧ = 1 → единственная замкнутая фигура: пара (2 точки, 1 ребро)
  КЧ = 2 → замкнутая фигура: кольцо (N точек, N рёбер). Минимум: 3 (треугольник)
            Но предпочитают S₈: угол 108° ≈ угол кольца октагона
  КЧ = 3 → замкнутая фигура: ТЕТРАЭДР (4 точки, 6 рёбер)
            Это ЕДИНСТВЕННОЕ Платоново тело с КЧ=3!
  КЧ = 4 → замкнутая фигура: октаэдр или куб. Но для 4 связей
            из каждой вершины проще бесконечная решётка → кристалл
  КЧ = 5 → замкнутая фигура: ИКОСАЭДР (12 точек, 30 рёбер)

  Правило: кластер замыкается в НАИМЕНЬШЕЕ тело с данным КЧ.
  Это Платоновы тела!

  КЧ=3 → Тетраэдр (P₄, As₄)
  КЧ=5 → Икосаэдр (B₁₂)
  КЧ=2 → Кольцо (S₈) — не Платоново, но минимальный замкнутый цикл
  КЧ=1 → Димер (N₂) — вырожденный случай
  КЧ=4 → Не замыкается в малую фигуру → кристалл (Si, Ge)
    """)

    # Verify: bonding_capacity predicts cluster CN?
    print(f"{'='*80}")
    print("ПРОВЕРКА: связ. способность = КЧ кластера?")
    print(f"{'='*80}")

    seen = set()
    correct = 0
    total = 0
    for elem, formula, cn_actual, shape, state in ELEMENT_CLUSTERS:
        if elem in seen:
            continue  # take first (most common) form
        seen.add(elem)
        props = elem_props.get(elem, {})
        bc = props.get("bonding_cap", 0)
        a = alphas.get(elem)

        # Prediction rule:
        # If Halbach (α > 1): CN = 1 (concentrate)
        # If Competition (α < 1): CN = bonding_cap
        # If no α data: CN = bonding_cap (default to competition)
        if a and a > 1:
            cn_pred = 1
        else:
            cn_pred = bc

        ok = "✓" if cn_pred == cn_actual else "✗"
        if cn_pred == cn_actual:
            correct += 1
        total += 1

        a_str = f"{a:.3f}" if a else "  —  "
        regime = "Хальбах" if a and a > 1 else "Конкур."
        print(f"  {elem:<4} α={a_str} связ.={bc} режим={regime:<8} "
              f"КЧ_пред={cn_pred} КЧ_факт={cn_actual} {ok}")

    print(f"\n  Итого: {correct}/{total} = {100*correct/total:.1f}%")

    # The full chain
    print(f"\n{'='*80}")
    print("ПОЛНАЯ ЦЕПОЧКА: тороид → кластер → вещество")
    print(f"{'='*80}")

    print("""
  Атом (тороид)
    │
    ├─ α > 1 (Хальбах) → КЧ = 1 → димер → ГАЗ
    │   N₂, O₂, F₂, Cl₂, Br₂, I₂
    │
    ├─ α < 1 (конкуренция) → КЧ = вал − 2·LP
    │   │
    │   ├─ КЧ = 2 → кольцо/цепь → молек. кристалл или полимер
    │   │   S₈, Se₈ (кольца), Te (цепи)
    │   │
    │   ├─ КЧ = 3 → тетраэдр (молекула) или слои (кристалл)
    │   │   P₄ (молекула), As (слоистый кристалл)
    │   │
    │   ├─ КЧ = 4 → бесконечная решётка → КРИСТАЛЛ
    │   │   Si, Ge, Sn (алмазная структура)
    │   │
    │   └─ КЧ = 5 → икосаэдр → КРИСТАЛЛ (из икосаэдров)
    │       B₁₂ (бор)
    │
    └─ α ≈ 1 (амбиверт) → КЧ = 1-2 → зависит от условий
        C (алмаз КЧ=4, графит КЧ=3, фуллерен КЧ=3)
    """)


if __name__ == "__main__":
    main()
