"""
α-Law Web Calculator — Streamlit app.
Run: streamlit run alphalaw/web.py
"""
import streamlit as st
import math

st.set_page_config(
    page_title="α-Law Calculator",
    page_icon="⚛️",
    layout="wide",
)

# ── i18n ────────────────────────────────────────────────────────────────

T = {
    "title": {"en": "⚛️ α-Law Calculator", "ru": "⚛️ Калькулятор α-закона"},
    "subtitle": {
        "en": "**Reserve Law of Chemical Bonding**: $E(n) = E_1 \\times n^\\alpha$\n\n"
              "Where $\\alpha > 1$ means synergy (each bond strengthens the next) "
              "and $\\alpha < 1$ means diminishing returns.",
        "ru": "**Закон Резерва химической связи**: $E(n) = E_1 \\times n^\\alpha$\n\n"
              "Где $\\alpha > 1$ — синергия (каждая связь усиливает следующую), "
              "а $\\alpha < 1$ — убывающая отдача.",
    },
    "select": {"en": "Select elements", "ru": "Выберите элементы"},
    "elem1": {"en": "Element 1", "ru": "Элемент 1"},
    "elem2": {"en": "Element 2", "ru": "Элемент 2"},
    "no_data": {"en": "No data for", "ru": "Нет данных для"},
    "regime": {"en": "Regime", "ru": "Режим"},
    "synergy": {"en": "Synergy", "ru": "Синергия"},
    "diminishing": {"en": "Diminishing returns", "ru": "Убывающая отдача"},
    "lp0": {
        "en": "**LP = 0** — No recruitable reserve. All electrons in bonds → each additional bond order weaker.",
        "ru": "**LP = 0** — Нет рекрутируемого резерва. Все электроны в связях → каждый следующий порядок слабее.",
    },
    "lp1": {
        "en": "**LP = {lp}** — Has reserve! Lone pairs available for π-bonding → synergy.",
        "ru": "**LP = {lp}** — Есть резерв! Неподелённые пары доступны для π-связей → синергия.",
    },
    "dblock": {
        "en": "**d-block** — d-electrons form δ-bonds with poor overlap → always diminishing returns.",
        "ru": "**d-блок** — d-электроны формируют δ-связи с плохим перекрыванием → всегда убывающая отдача.",
    },
    "source": {"en": "Source", "ru": "Источник"},
    "scaling": {"en": "Bond energy scaling", "ru": "Масштабирование энергии связи"},
    "energies": {"en": "Energies (kJ/mol)", "ru": "Энергии (кДж/моль)"},
    "bond_order": {"en": "Bond order", "ru": "Порядок связи"},
    "e_actual": {"en": "E actual", "ru": "E факт"},
    "e_predicted": {"en": "E predicted", "ru": "E расчёт"},
    "error_pct": {"en": "Error %", "ru": "Ошибка %"},
    "full_table": {"en": "📊 Full bond table (38 bonds)", "ru": "📊 Полная таблица связей (38)"},
    "bond": {"en": "Bond", "ru": "Связь"},
    "block": {"en": "Block", "ru": "Блок"},
    "reserve": {"en": "Reserve", "ru": "Резерв"},
    "yes": {"en": "YES", "ru": "ДА"},
    "no": {"en": "NO", "ru": "НЕТ"},
    "stats": {
        "en": "**Statistics:**\n- LP=0 → α<1: 93% (13/14)\n- LP≥1 → α>1: 80% (4/5)\n- d-block → α<1: 100% (4/4)",
        "ru": "**Статистика:**\n- LP=0 → α<1: 93% (13/14)\n- LP≥1 → α>1: 80% (4/5)\n- d-блок → α<1: 100% (4/4)",
    },
    "estimated_tag": {"en": "ESTIMATED", "ru": "ОЦЕНКА"},
    "confidence": {"en": "Confidence", "ru": "Уверенность"},
    "est_note": {
        "en": "No measured data — prediction based on LP + period heuristic",
        "ru": "Нет измеренных данных — предсказание по LP + период",
    },
    "about_title": {"en": "About", "ru": "О проекте"},
    "about": {
        "en": "The **Reserve Law** states that systems with recruitable reserve show cooperative scaling (α > 1), "
              "while systems without reserve show diminishing returns (α < 1).\n\n"
              "- **Paper**: Reserve Law of Chemical Bonding (Y. Kazin, 2026)\n"
              "- **Code**: `pip install alphalaw`\n"
              "- **Contact**: yuri@kazin.ru",
        "ru": "**Закон Резерва** гласит: системы с рекрутируемым резервом показывают синергию (α > 1), "
              "а без резерва — убывающую отдачу (α < 1).\n\n"
              "- **Статья**: Закон Резерва химической связи (Ю. Казин, 2026)\n"
              "- **Код**: `pip install alphalaw`\n"
              "- **Контакт**: yuri@kazin.ru",
    },
}

# ── Data ────────────────────────────────────────────────────────────────

BONDS = {
    # Format: (α, β, LP_min, block, energies, source)
    # Model: E = E₁ × n^(α + β·ln(n));  β=0 for 2-point bonds
    ("C", "C"):   (0.864, -0.052, 0, "s/p", {1:346, 2:614, 3:839}, "CRC Handbook"),
    ("Si", "Si"): (0.485, 0, 0, "s/p", {1:310, 2:434}, "CRC"),
    ("Ge", "Ge"): (0.407, 0, 0, "s/p", {1:264, 2:350}, "CRC"),
    ("Sn", "Sn"): (0.330, 0, 0, "s/p", {1:187, 2:235}, "CRC"),
    ("N", "N"):   (0.990, 0.570, 1, "s/p", {1:160, 2:418, 3:945}, "CRC"),
    ("P", "P"):   (1.283, 0, 1, "s/p", {1:201, 2:489}, "CRC"),
    ("O", "O"):   (1.770, 0, 2, "s/p", {1:146, 2:498}, "CRC"),
    ("S", "S"):   (0.676, 0, 2, "s/p", {1:266, 2:425}, "CRC"),
    ("C", "N"):   (1.073, -0.089, 0, "s/p", {1:305, 2:615, 3:891}, "CRC"),
    ("C", "O"):   (1.151, -0.135, 0, "s/p", {1:358, 2:745, 3:1077}, "CRC"),
    ("N", "O"):   (1.595, 0, 1, "s/p", {1:201, 2:607}, "CRC"),
    ("B", "N"):   (0.707, 0, 0, "s/p", {1:389, 2:635}, "CRC"),
    ("B", "O"):   (0.589, 0, 0, "s/p", {1:536, 2:806}, "CRC"),
    ("Si", "O"):  (0.502, 0, 0, "s/p", {1:452, 2:640}, "CRC"),
    ("Si", "N"):  (0.405, 0, 0, "s/p", {1:355, 2:470}, "CRC"),
    ("Al", "O"):  (0.560, 0, 0, "s/p", {1:502, 2:740}, "CRC"),
    ("C", "S"):   (1.075, 0, 0, "s/p", {1:272, 2:573}, "CRC"),
    ("C", "P"):   (0.958, 0, 0, "s/p", {1:264, 2:513}, "CRC"),
    ("Ge", "O"):  (0.520, 0, 0, "s/p", {1:401, 2:575}, "CRC"),
    ("As", "As"): (1.388, 0, 1, "s/p", {1:146, 2:382}, "CRC"),
    ("Se", "Se"): (0.661, 0, 2, "s/p", {1:172, 2:272}, "CRC"),
    ("Te", "Te"): (0.686, 0, 2, "s/p", {1:138, 2:222}, "CRC"),
    ("B", "C"):   (0.665, 0, 0, "s/p", {1:372, 2:590}, "CRC"),
    ("N", "S"):   (1.554, 0, 1, "s/p", {1:159, 2:467}, "CRC"),
    ("P", "O"):   (0.699, 0, 1, "s/p", {1:335, 2:544}, "CRC"),
    ("S", "O"):   (0.978, 0, 2, "s/p", {1:265, 2:522}, "CRC"),
    ("P", "S"):   (0.543, 0, 1, "s/p", {1:230, 2:335}, "CRC"),
    ("F", "F"):   (None, 0, 3, "s/p", {1:158}, "CRC"),
    ("Cl", "Cl"): (None, 0, 3, "s/p", {1:242}, "CRC"),
    ("Br", "Br"): (None, 0, 3, "s/p", {1:193}, "CRC"),
    ("I", "I"):   (None, 0, 3, "s/p", {1:151}, "CRC"),
    ("Ti", "O"):  (None, 0, -1, "d", {1:672}, "CRC"),
    ("Fe", "C"):  (None, 0, -1, "d", {1:394}, "CRC; Brugh & Morse"),
    ("W", "C"):   (None, 0, -1, "d", {1:639}, "CRC"),
    ("Cr", "Cr"): (0.559, 0, -1, "d", {1:70, 4:152}, "Cotton; CRC"),
    ("Mo", "Mo"): (1.076, -0.242, -1, "d", {1:140, 2:250, 3:350, 4:405, 5:420, 6:435}, "Cotton & Murillo 2005"),
    ("W", "W"):   (1.394, -0.336, -1, "d", {1:160, 3:500, 4:570, 6:666}, "CRC; Cotton"),
    ("Re", "Re"): (0.924, 0, -1, "d", {1:120, 4:432}, "Bergman 1984; CRC"),
}

def lookup(e1, e2):
    return BONDS.get((e1, e2)) or BONDS.get((e2, e1))

# Estimation for elements not in BONDS
ELEMENTS = {
    "H":(1,1,"s",1,0),"He":(1,18,"s",2,1),"Li":(2,1,"s",1,0),"Be":(2,2,"s",2,0),
    "B":(2,13,"s/p",3,0),"C":(2,14,"s/p",4,0),"N":(2,15,"s/p",5,1),"O":(2,16,"s/p",6,2),
    "F":(2,17,"s/p",7,3),"Na":(3,1,"s",1,0),"Mg":(3,2,"s",2,0),"Al":(3,13,"s/p",3,0),
    "Si":(3,14,"s/p",4,0),"P":(3,15,"s/p",5,1),"S":(3,16,"s/p",6,2),"Cl":(3,17,"s/p",7,3),
    "K":(4,1,"s",1,0),"Ca":(4,2,"s",2,0),"Sc":(4,3,"d",3,-1),"Ti":(4,4,"d",4,-1),
    "V":(4,5,"d",5,-1),"Cr":(4,6,"d",6,-1),"Mn":(4,7,"d",7,-1),"Fe":(4,8,"d",8,-1),
    "Co":(4,9,"d",9,-1),"Ni":(4,10,"d",10,-1),"Cu":(4,11,"d",11,-1),"Zn":(4,12,"d",12,-1),
    "Ga":(4,13,"s/p",3,0),"Ge":(4,14,"s/p",4,0),"As":(4,15,"s/p",5,1),"Se":(4,16,"s/p",6,2),
    "Br":(4,17,"s/p",7,3),"Rb":(5,1,"s",1,0),"Sr":(5,2,"s",2,0),"Y":(5,3,"d",3,-1),
    "Zr":(5,4,"d",4,-1),"Nb":(5,5,"d",5,-1),"Mo":(5,6,"d",6,-1),"Ru":(5,8,"d",8,-1),
    "Rh":(5,9,"d",9,-1),"Pd":(5,10,"d",10,-1),"Ag":(5,11,"d",11,-1),"Cd":(5,12,"d",12,-1),
    "In":(5,13,"s/p",3,0),"Sn":(5,14,"s/p",4,0),"Sb":(5,15,"s/p",5,1),"Te":(5,16,"s/p",6,2),
    "I":(5,17,"s/p",7,3),"Cs":(6,1,"s",1,0),"Ba":(6,2,"s",2,0),"La":(6,3,"d",3,-1),
    "Hf":(6,4,"d",4,-1),"Ta":(6,5,"d",5,-1),"W":(6,6,"d",6,-1),"Re":(6,7,"d",7,-1),
    "Os":(6,8,"d",8,-1),"Ir":(6,9,"d",9,-1),"Pt":(6,10,"d",10,-1),"Au":(6,11,"d",11,-1),
    "Hg":(6,12,"d",12,-1),"Tl":(6,13,"s/p",3,0),"Pb":(6,14,"s/p",4,0),"Bi":(6,15,"s/p",5,1),
    "U":(7,3,"f",3,-1),"Th":(7,4,"f",4,-1),
}

def estimate(e1, e2):
    if e1 not in ELEMENTS or e2 not in ELEMENTS:
        return None
    p1,_,blk1,_,lp1 = ELEMENTS[e1]
    p2,_,blk2,_,lp2 = ELEMENTS[e2]
    period = max(p1, p2)
    lp_min = min(lp1, lp2) if lp1 >= 0 and lp2 >= 0 else -1
    is_d = blk1 == "d" or blk2 == "d"
    is_f = blk1 == "f" or blk2 == "f"
    if is_f:
        return 0.5, "low", lp_min, "f", "f-block: rough estimate"
    if is_d:
        a = {4: 0.65, 5: 0.72, 6: 0.85}.get(period, 0.7)
        return a, "medium", lp_min, "d", "d-block: δ-overhead"
    if lp_min == 0:
        a = {2: 0.82, 3: 0.48, 4: 0.41, 5: 0.33, 6: 0.28}.get(period, 0.35)
        return a, "high", lp_min, "s/p", f"LP=0, Period {period}"
    if lp_min >= 1 and period == 2:
        a = {1: 1.55, 2: 1.77}.get(lp_min, 1.6)
        return a, "high", lp_min, "s/p", f"LP={lp_min}, Period 2: synergy"
    if lp_min >= 1 and period == 3:
        a = 1.1 if lp_min == 1 else 0.7
        return a, "medium", lp_min, "s/p", f"LP={lp_min}, Period 3"
    a = 0.65
    return a, "medium", lp_min, "s/p", f"LP={lp_min}, Period {period}"

ALL_ELEMENTS = sorted(set(
    list(e for pair in BONDS for e in pair) + list(ELEMENTS.keys())
))

# ── Language selector ───────────────────────────────────────────────────

lang = st.sidebar.radio("🌐 Language / Язык", ["English", "Русский"],
                        index=0, horizontal=True)
L = "ru" if lang == "Русский" else "en"

def t(key, **kwargs):
    text = T.get(key, {}).get(L, key)
    if kwargs:
        text = text.format(**kwargs)
    return text

# ── UI ──────────────────────────────────────────────────────────────────

st.title(t("title"))
st.markdown(t("subtitle"))

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(t("select"))
    elem1 = st.selectbox(t("elem1"), ALL_ELEMENTS, index=ALL_ELEMENTS.index("C"))
    elem2 = st.selectbox(t("elem2"), ALL_ELEMENTS, index=ALL_ELEMENTS.index("C"))

    data = lookup(elem1, elem2)
    is_estimated = False

    if data is not None:
        alpha, beta, lp_min, block, energies, source = data
    else:
        est = estimate(elem1, elem2)
        if est is None:
            st.error(f"{t('no_data')} {elem1}-{elem2}")
            alpha = None
        else:
            alpha, conf, lp_min, block, reason = est
            beta, energies, source = 0, {}, reason
            is_estimated = True

    if alpha is not None:
        if alpha > 1:
            color = "🟢"
            regime = t("synergy")
        else:
            color = "🔴"
            regime = t("diminishing")

        tag = f" `[{t('estimated_tag')}]`" if is_estimated else ""
        beta_str = f", β = {beta:+.3f}" if abs(beta) > 0.01 else ""
        st.markdown(f"### {color} {elem1}-{elem2}: α = {alpha:.3f}{beta_str}{tag}\n"
                    f"**{t('regime')}**: {regime}")

        if is_estimated:
            st.warning(f"📊 {t('est_note')}\n\n**{t('confidence')}**: {conf} | {reason}")
        elif block == "s/p":
            if lp_min == 0:
                st.info(t("lp0"))
            elif lp_min >= 1:
                st.success(t("lp1", lp=lp_min))
        else:
            st.warning(t("dblock"))

        if not is_estimated:
            st.caption(f"{t('source')}: {source}")

with col2:
    if alpha is not None and energies and len(energies) >= 2:
        alpha, beta, lp_min, block, energies, source = data
        orders = sorted(energies.keys())
        E1 = energies[orders[0]]

        st.subheader(f"{t('scaling')}: {elem1}-{elem2}")

        import numpy as np
        import pandas as pd
        import altair as alt

        import math as _math
        n_range = np.linspace(orders[0], max(orders[-1], 3), 50)
        E_pred = [E1 * _math.exp(alpha * _math.log(n/orders[0]) + beta * _math.log(n/orders[0])**2)
                  for n in n_range]

        actual_n = list(energies.keys())
        actual_E = list(energies.values())

        df_pred = pd.DataFrame({"n": n_range, "E = E₁ × n^α": E_pred})
        df_actual = pd.DataFrame({"n": actual_n, "E actual": actual_E})

        x_title = t("bond_order") + " n"
        y_title = t("energies")

        line = alt.Chart(df_pred).mark_line(color="#4C78A8", strokeWidth=2).encode(
            x=alt.X("n:Q", title=x_title),
            y=alt.Y("E = E₁ × n^α:Q", title=y_title),
        )
        points = alt.Chart(df_actual).mark_circle(size=120, color="#E45756").encode(
            x="n:Q",
            y=alt.Y("E actual:Q", title=y_title),
            tooltip=["n:Q", "E actual:Q"],
        )
        st.altair_chart((line + points).properties(height=350, width=500),
                         use_container_width=True)

        st.markdown(f"**{t('energies')}**")
        rows = []
        for n in orders:
            E_act = energies[n]
            ln_n = _math.log(n / orders[0]) if n > orders[0] else 0
            E_p = E1 * _math.exp(alpha * ln_n + beta * ln_n**2)
            rows.append({t("bond_order"): n, t("e_actual"): E_act,
                          t("e_predicted"): round(E_p, 1),
                          t("error_pct"): round(100 * (E_p - E_act) / E_act, 1)})
        st.dataframe(pd.DataFrame(rows), hide_index=True)

# ── Full table ──────────────────────────────────────────────────────────

st.markdown("---")
with st.expander(t("full_table")):
    import pandas as pd
    rows = []
    for (e1, e2), (a, b, lp, blk, ens, src) in sorted(BONDS.items()):
        reserve = t("yes") if (blk == "s/p" and lp >= 1) else t("no")
        lp_str = str(lp) if lp >= 0 else "d"
        if a is not None:
            regime = t("synergy").lower() if a > 1 else t("diminishing").lower()
            a_str = round(a, 3)
        else:
            regime = "—"
            a_str = "—"
        b_str = f"{b:+.3f}" if abs(b) > 0.01 else ""
        rows.append({t("bond"): f"{e1}-{e2}", t("block"): blk, "α": a_str,
                      "β": b_str, "LP": lp_str, t("reserve"): reserve, t("regime"): regime})
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
    st.markdown(t("stats"))

# ── About ───────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown(f"### {t('about_title')}")
st.markdown(t("about"))
