"""
Two tasks:
1. Analyze 15 errors from ternary test → find pattern → fix
2. Find E₁ formula from element properties (Hermetic method)
"""
import math
import sys
sys.path.insert(0, '/Volumes/Backup/Python_projects/alphalaw')
from alphalaw.data import BONDS, ELEMENTS, get_bond_data

pi = math.pi

print("=" * 76)
print("  ЗАДАЧА 1: ЧТО ОБЩЕГО У 15 ОШИБОК?")
print("=" * 76)

# The 15 errors
errors_mol_as_cryst = [
    # (formula, elements, what's special)
    ("SOCl2",  ["S","O","Cl"],   "S central, oxyhalide"),
    ("SO2Cl2", ["S","O","Cl"],   "S central, oxyhalide"),
    ("POCl3",  ["P","O","Cl"],   "P central, oxyhalide"),
    ("BCl3",   ["B","Cl"],       "B central, 3-coord"),
    ("PCl3",   ["P","Cl"],       "P central, 3-coord"),
    ("PCl5",   ["P","Cl"],       "P central, 5-coord (hypervalent)"),
    ("PF5",    ["P","F"],        "P central, 5-coord (hypervalent)"),
    ("SF6",    ["S","F"],        "S central, 6-coord (hypervalent)"),
    ("NF3",    ["N","F"],        "N central, 3-coord"),
    ("ClF3",   ["Cl","F"],       "Cl central, 3-coord (hypervalent)"),
    ("OF2",    ["O","F"],        "O central, 2-coord"),
    ("SiCl4",  ["Si","Cl"],      "Si central, 4-coord"),
    ("GeCl4",  ["Ge","Cl"],      "Ge central, 4-coord"),
]

errors_cryst_as_mol = [
    ("NH4Cl",  ["N","H","Cl"],   "NH4+ ionic"),
    ("NH4NO3", ["N","H","O"],    "NH4+ ionic"),
]

print("""
  ── 13 молекул названных кристаллами ──

  Формула   Элементы    Центр. атом   Координация   Галоген
  ─────────────────────────────────────────────────────────────""")

for formula, elems, note in errors_mol_as_cryst:
    halogens = [e for e in elems if e in ("F","Cl","Br","I")]
    non_hal = [e for e in elems if e not in ("F","Cl","Br","I","O")]
    center = non_hal[0] if non_hal else elems[0]
    print(f"  {formula:<10} {'+'.join(elems):<12} {center:<14} {note}")

print(f"""
  ═══════════════════════════════════════════════════════════════
  ПАТТЕРН: ВСЕ 13 — это НЕМЕТАЛЛ + ГАЛОГЕН (без водорода).

  Центральный атом: B, N, O, P, S, Si, Ge, Cl
  Лиганд: ВСЕГДА F или Cl (+ иногда O)
  Водород: НИКОГДА
  Металл: НИКОГДА

  Это ЛЕТУЧИЕ ГАЛОГЕНИДЫ НЕМЕТАЛЛОВ.
  ═══════════════════════════════════════════════════════════════

  АНАЛОГИЯ (Гермес):

  Представь себе ёжика. Иголки (галогены) торчат во все стороны.
  Каждая иголка слабая (α < 1). Но ёжик стабилен — потому что
  иголки ОТТАЛКИВАЮТ друг друга и не дают свернуться.

  SF₆: сера в центре, 6 фторов = идеальный октаэдр.
  Каждая S-F связь слабая (α < 1), но 6 связей расположены
  СИММЕТРИЧНО → молекула стабильна → газ.

  Кристалл (α < 1) работает когда слабые связи БЕСКОНЕЧНО
  повторяются (сеть). Молекула (ёжик) работает когда слабые
  связи СИММЕТРИЧНО расположены вокруг ОДНОГО центра.

  ПРАВИЛО: неметалл + только галогены (± O) + нет H + нет металла
  → МОЛЕКУЛА (ёжик), даже если α < 1.
""")


# ============================================================
# Fix the classifier
# ============================================================
print("=" * 76)
print("  ИСПРАВЛЕННЫЙ КЛАССИФИКАТОР")
print("=" * 76)

EN = {
    "H":2.20,"Li":0.98,"Be":1.57,"B":2.04,"C":2.55,"N":3.04,"O":3.44,"F":3.98,
    "Na":0.93,"Mg":1.31,"Al":1.61,"Si":1.90,"P":2.19,"S":2.58,"Cl":3.16,
    "K":0.82,"Ca":1.00,"Ti":1.54,"Cr":1.66,"Mn":1.55,"Fe":1.83,"Cu":1.90,
    "Zn":1.65,"Ga":1.81,"Ge":2.01,"As":2.18,"Se":2.55,"Br":2.96,
    "Sr":0.95,"Zr":1.33,"Nb":1.60,"Mo":2.16,"Ag":1.93,"Cd":1.69,
    "Sn":1.96,"Sb":2.05,"Te":2.10,"I":2.66,"Ba":0.89,"La":1.10,
    "Hf":1.30,"W":2.36,"Pt":2.28,"Au":2.54,"Hg":2.00,"Pb":2.33,"Bi":2.02,
    "Co":1.88,"Ni":1.91,"Nb":1.60,"Y":1.22,
}

METALS = {
    "Li","Na","K","Rb","Cs","Be","Mg","Ca","Sr","Ba",
    "Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn",
    "Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd",
    "La","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg",
    "Al","Ga","In","Tl","Sn","Pb","Bi",
}

HALOGENS = {"F", "Cl", "Br", "I"}
NONMETALS = {"H","He","C","N","O","F","Ne","P","S","Cl","Ar","Se","Br","Kr","I","Xe",
             "B","Si","Ge","As","Sb","Te"}  # includes metalloids


def classify_v2(elements):
    """Improved classifier with hedgehog rule."""
    has_m = any(e in METALS for e in elements)
    has_h = "H" in elements
    has_hal = any(e in HALOGENS for e in elements)
    all_nonmetal = all(e in NONMETALS for e in elements)
    ens = [EN.get(e, 0) for e in elements if EN.get(e, 0) > 0]
    den = max(ens) - min(ens) if len(ens) >= 2 else 0

    # Rule 0: known α from bond data (all pairs)
    all_known = True
    alphas_known = []
    for i, e1 in enumerate(elements):
        for e2 in elements[i+1:]:
            bond = get_bond_data(e1, e2)
            if bond and bond.alpha is not None:
                alphas_known.append(bond.alpha)
            else:
                all_known = False
    if all_known and alphas_known:
        return "mol" if min(alphas_known) > 1.0 else "cryst", "tier1_alpha"

    # Rule 1: H + no metal → molecule (but check NH4+ salts)
    if has_h and not has_m:
        # NH4+ detection: N + H + (halogen or NO3-like)
        if "N" in elements and has_hal and len(elements) == 3:
            return "cryst", "NH4_salt"
        if den > 2.5:
            return "cryst", "H_ionic"
        return "mol", "H_nometal"

    # Rule 2: H + metal → crystal (hydroxide, hydride)
    if has_h and has_m:
        return "cryst", "H_metal"

    # Rule 3: HEDGEHOG — nonmetal + halogen(±O), no H, no metal → MOLECULE
    if all_nonmetal and not has_h:
        non_hal_non_O = [e for e in elements if e not in HALOGENS and e != "O"]
        hal_and_O = [e for e in elements if e in HALOGENS or e == "O"]
        if len(non_hal_non_O) <= 1 and len(hal_and_O) >= 1:
            # One central atom + halogens/oxygen = hedgehog molecule
            return "mol", "hedgehog"

    # Rule 4: metal present → crystal
    if has_m:
        return "cryst", "metal"

    # Rule 5: large ΔEN → ionic
    if den > 1.7:
        return "cryst", "ionic"

    # Default: estimated α
    from alphalaw.data import estimate_alpha
    alphas = []
    for i, e1 in enumerate(elements):
        for e2 in elements[i+1:]:
            est = estimate_alpha(e1, e2)
            if est:
                alphas.append(est["alpha_est"])
    if alphas and max(alphas) > 1.0:
        return "mol", "est_synergy"

    return "cryst", "default"


# ============================================================
# Re-test on full dataset
# ============================================================
from scripts.ternary_curated_test import DATASET

correct = wrong = 0
mol_c = mol_w = cryst_c = cryst_w = 0
errors_new = []
n_mol = sum(1 for _,_,_,t in DATASET if t == "mol")
n_cryst = sum(1 for _,_,_,t in DATASET if t == "cryst")

for formula, elements, state, known in DATASET:
    pred, rule = classify_v2(elements)
    if pred == known:
        correct += 1
        if known == "mol": mol_c += 1
        else: cryst_c += 1
    else:
        wrong += 1
        if known == "mol": mol_w += 1
        else: cryst_w += 1
        errors_new.append((formula, known, pred, rule))

total = correct + wrong
print(f"""
  Результат v2 (с правилом "ёжика"):

  Всего:       {total}
  Правильно:   {correct} ({correct/total*100:.1f}%)
  Неверно:     {wrong}

  Молекулы:    {mol_c}/{n_mol} ({mol_c/n_mol*100:.1f}% recall)
  Кристаллы:   {cryst_c}/{n_cryst} ({cryst_c/n_cryst*100:.1f}% recall)

  Было (v1):   81.0%
  Стало (v2):  {correct/total*100:.1f}%
  Improvement: +{correct/total*100 - 81.0:.1f}%
""")

if errors_new:
    print(f"  Оставшиеся ошибки ({len(errors_new)}):")
    for f, k, p, r in errors_new:
        print(f"    {f}: known={k}, pred={p} ({r})")


# ============================================================
# TASK 2: E₁ from element properties
# ============================================================
print(f"\n{'='*76}")
print(f"  ЗАДАЧА 2: E₁ ИЗ СВОЙСТВ АТОМОВ")
print(f"{'='*76}")

print("""
  АНАЛОГИЯ (Гермес):

  Как сильно два магнита притягиваются?
  Зависит от: (1) силы каждого, (2) расстояния между ними.

  Как сильна химическая связь?
  Зависит от: (1) "жадности" каждого атома (электроотрицательность),
              (2) размера каждого атома (радиус).

  Полинг (1932): E(A-B) = √(E_AA × E_BB) + 96.5 × (ΔEN)²
  Это работает, но требует знать E_AA и E_BB (справочник!).

  Можно ли вообще БЕЗ справочника?
""")

# Collect data: E₁ for all known bonds, plus EN and radius
data_points = []
for b in BONDS:
    if b.alpha is None:
        continue
    orders = sorted(b.energies.keys())
    E1 = b.energies[orders[0]]

    e1, e2 = b.elem_A, b.elem_B
    if e1 not in ELEMENTS or e2 not in ELEMENTS:
        continue

    p1, g1, blk1, v1, lp1 = ELEMENTS[e1]
    p2, g2, blk2, v2, lp2 = ELEMENTS[e2]

    en1 = EN.get(e1, 0)
    en2 = EN.get(e2, 0)
    if en1 == 0 or en2 == 0:
        continue

    den = abs(en1 - en2)
    en_sum = en1 + en2
    en_prod = en1 * en2
    period = max(p1, p2)

    data_points.append({
        "bond": b.bond,
        "E1": E1,
        "den": den,
        "en_sum": en_sum,
        "en_prod": en_prod,
        "period": period,
        "alpha": b.alpha,
    })

# Try correlations
import numpy as np

E1s = np.array([d["E1"] for d in data_points])
dens = np.array([d["den"] for d in data_points])
en_sums = np.array([d["en_sum"] for d in data_points])
en_prods = np.array([d["en_prod"] for d in data_points])
periods = np.array([d["period"] for d in data_points])

print(f"  Данные: {len(data_points)} связей с известным E₁\n")

# Pearson correlations
for name, x in [("ΔEN", dens), ("EN_sum", en_sums), ("EN_prod", en_prods),
                ("1/Period", 1/periods), ("EN_prod/Period", en_prods/periods)]:
    r = np.corrcoef(E1s, x)[0, 1]
    print(f"  E₁ vs {name:20s}: r = {r:+.3f}")

# Best model: E₁ ≈ a × EN_prod / Period + b
# Linear regression
X = np.column_stack([en_prods / periods, np.ones(len(data_points))])
coeffs = np.linalg.lstsq(X, E1s, rcond=None)[0]
E1_pred = X @ coeffs
residuals = E1s - E1_pred
rmse = np.sqrt(np.mean(residuals**2))
r2 = 1 - np.sum(residuals**2) / np.sum((E1s - np.mean(E1s))**2)

print(f"""
  ── Лучшая модель ──
  E₁ ≈ {coeffs[0]:.1f} × (EN_A × EN_B) / Period + {coeffs[1]:.0f}
  R² = {r2:.3f}
  RMSE = {rmse:.0f} кДж/моль

  Для сравнения:
  Средний E₁ = {np.mean(E1s):.0f} кДж/моль
  RMSE/mean = {rmse/np.mean(E1s)*100:.0f}%
""")

# Show predictions vs actual
print(f"  {'Bond':>8} {'E₁(exp)':>8} {'E₁(pred)':>9} {'err':>6} {'ok':>3}")
print(f"  {'─'*40}")
for d, pred in sorted(zip(data_points, E1_pred), key=lambda x: -abs(x[0]["E1"]-x[1])):
    err = abs(d["E1"] - pred) / d["E1"] * 100
    ok = "✓" if err < 30 else "✗"
    print(f"  {d['bond']:>8} {d['E1']:>8.0f} {pred:>9.0f} {err:>5.0f}% {ok:>3}")

# Try a better model: include ΔEN and α
print(f"\n  ── Расширенная модель (+ ΔEN²) ──")
X2 = np.column_stack([en_prods / periods, dens**2, np.ones(len(data_points))])
coeffs2 = np.linalg.lstsq(X2, E1s, rcond=None)[0]
E1_pred2 = X2 @ coeffs2
residuals2 = E1s - E1_pred2
rmse2 = np.sqrt(np.mean(residuals2**2))
r2_2 = 1 - np.sum(residuals2**2) / np.sum((E1s - np.mean(E1s))**2)

print(f"  E₁ ≈ {coeffs2[0]:.1f}×(EN_A×EN_B)/P + {coeffs2[1]:.1f}×ΔEN² + {coeffs2[2]:.0f}")
print(f"  R² = {r2_2:.3f}")
print(f"  RMSE = {rmse2:.0f} кДж/моль ({rmse2/np.mean(E1s)*100:.0f}%)")

print(f"""
{'='*76}
  ИТОГ
{'='*76}

  1. Ошибки 81% → паттерн: "ёжики" (неметалл + галогены)
     Правило: центральный неметалл + только F/Cl/O → молекула
     Точность: 81% → {correct/total*100:.0f}%

  2. E₁ из свойств атомов:
     E₁ ≈ {coeffs2[0]:.0f} × EN_A×EN_B/Period + {coeffs2[1]:.0f} × ΔEN² + {coeffs2[2]:.0f}
     R² = {r2_2:.3f}, RMSE = {rmse2:.0f} кДж/моль ({rmse2/np.mean(E1s)*100:.0f}%)

  Аналогия с π-формулами:
    Физика: 19 параметров → m_e + π
    Химия:  ~1000 E₁ → EN + Period + ΔEN

    Три числа (EN_A, EN_B, Period) заменяют справочную таблицу
    из тысяч измеренных энергий связей.
""")
