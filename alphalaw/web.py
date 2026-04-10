"""
α-Law Web Calculator — Streamlit app.
Run: streamlit run alphalaw/web.py
"""
import streamlit as st
import math
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(page_title="α-Law Calculator", page_icon="⚛️", layout="wide")

# ── Import data from canonical source ───────────────────────────────
from alphalaw.data import (
    list_all_bonds, get_bond_data, estimate_alpha, ELEMENTS, BondData
)

ALL_ELEMENTS = sorted(set(
    [b.elem_A for b in list_all_bonds()] +
    [b.elem_B for b in list_all_bonds()] +
    list(ELEMENTS.keys())
))

# ── i18n ────────────────────────────────────────────────────────────
T = {
    "title": {"en": "⚛️ α-Law Calculator", "ru": "⚛️ Калькулятор α-закона"},
    "subtitle": {
        "en": "**Bond Order Scaling Rule**: $E(n) = E_1 \\times n^\\alpha$\n\n"
              "Where $\\alpha > 1$ means synergy (each bond strengthens the next) "
              "and $\\alpha < 1$ means diminishing returns.",
        "ru": "**Правило масштабирования связей**: $E(n) = E_1 \\times n^\\alpha$\n\n"
              "Где $\\alpha > 1$ — синергия (каждая связь усиливает следующую), "
              "а $\\alpha < 1$ — убывающая отдача.",
    },
    "select": {"en": "Select elements", "ru": "Выберите элементы"},
    "elem1": {"en": "Element 1", "ru": "Элемент 1"},
    "elem2": {"en": "Element 2", "ru": "Элемент 2"},
    "no_data": {"en": "Unknown element", "ru": "Неизвестный элемент"},
    "regime": {"en": "Regime", "ru": "Режим"},
    "synergy": {"en": "Synergy", "ru": "Синергия"},
    "diminishing": {"en": "Diminishing returns", "ru": "Убывающая отдача"},
    "lp0": {
        "en": "**LP = 0** — No recruitable reserve → each additional bond order weaker.",
        "ru": "**LP = 0** — Нет рекрутируемого резерва → каждый следующий порядок слабее.",
    },
    "lp1": {
        "en": "**LP = {lp}** — Has reserve! Lone pairs available for π-bonding → synergy.",
        "ru": "**LP = {lp}** — Есть резерв! Неподелённые пары для π-связей → синергия.",
    },
    "lp1_heavy": {
        "en": "**LP = {lp}, Period {per}** — LP exists but poor π-overlap in heavy atoms.",
        "ru": "**LP = {lp}, Период {per}** — LP есть, но плохое π-перекрывание у тяжёлых.",
    },
    "dblock": {
        "en": "**d-block** — d-electrons form δ-bonds with poor overlap → diminishing returns.",
        "ru": "**d-блок** — d-электроны формируют δ-связи с плохим перекрыванием → убывание.",
    },
    "source": {"en": "Source", "ru": "Источник"},
    "scaling": {"en": "Bond energy scaling", "ru": "Масштабирование энергии связи"},
    "energies": {"en": "Energies (kJ/mol)", "ru": "Энергии (кДж/моль)"},
    "bond_order": {"en": "Bond order", "ru": "Порядок связи"},
    "e_actual": {"en": "E actual", "ru": "E факт"},
    "e_predicted": {"en": "E predicted", "ru": "E расчёт"},
    "error_pct": {"en": "Error %", "ru": "Ошибка %"},
    "full_table": {"en": "📊 Full bond table", "ru": "📊 Полная таблица связей"},
    "bond": {"en": "Bond", "ru": "Связь"},
    "block": {"en": "Block", "ru": "Блок"},
    "reserve": {"en": "Reserve", "ru": "Резерв"},
    "yes": {"en": "YES", "ru": "ДА"},
    "no": {"en": "NO", "ru": "НЕТ"},
    "estimated_tag": {"en": "ESTIMATED", "ru": "ОЦЕНКА"},
    "confidence": {"en": "Confidence", "ru": "Уверенность"},
    "est_note": {
        "en": "No measured data — prediction based on LP + period heuristic",
        "ru": "Нет измеренных данных — предсказание по LP + период",
    },
    "about_title": {"en": "About", "ru": "О проекте"},
    "about": {
        "en": "The **Bond Order Scaling Rule** classifies bonds by whether multiple bonds "
              "are stronger (α > 1) or weaker (α < 1) than expected from single bond energy.\n\n"
              "- **Paper**: Bond Order Scaling Rule (Y. Kazin, 2026)\n"
              "- **Code**: [github.com/fb15649/alphalaw](https://github.com/fb15649/alphalaw)\n"
              "- **Contact**: yuri@kazin.ru",
        "ru": "**Правило масштабирования** классифицирует связи: кратные связи сильнее (α > 1) "
              "или слабее (α < 1) чем ожидается из энергии одинарной.\n\n"
              "- **Статья**: Bond Order Scaling Rule (Ю. Казин, 2026)\n"
              "- **Код**: [github.com/fb15649/alphalaw](https://github.com/fb15649/alphalaw)\n"
              "- **Контакт**: yuri@kazin.ru",
    },
}

# ── Language ────────────────────────────────────────────────────────
lang = st.sidebar.radio("🌐 Language / Язык", ["English", "Русский"], index=0, horizontal=True)
L = "ru" if lang == "Русский" else "en"

def t(key, **kw):
    txt = T.get(key, {}).get(L, key)
    return txt.format(**kw) if kw else txt

# ── UI ──────────────────────────────────────────────────────────────
st.title(t("title"))
st.markdown(t("subtitle"))

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(t("select"))
    elem1 = st.selectbox(t("elem1"), ALL_ELEMENTS, index=ALL_ELEMENTS.index("C"))
    elem2 = st.selectbox(t("elem2"), ALL_ELEMENTS, index=ALL_ELEMENTS.index("C"))

    bond = get_bond_data(elem1, elem2)
    is_estimated = False
    alpha = None

    if bond is not None:
        alpha = bond.alpha
        beta = bond.beta
        lp_min = bond.LP_min
        block = bond.block
        energies = bond.energies
        source = bond.source
    else:
        est = estimate_alpha(elem1, elem2)
        if est is None:
            st.error(f"{t('no_data')}: {elem1}, {elem2}")
        else:
            alpha = est["alpha_est"]
            beta = 0
            lp_min = est["lp_min"]
            block = est["block"]
            energies = {}
            source = est["reason"]
            is_estimated = True

    if alpha is not None:
        color = "🟢" if alpha > 1 else "🔴"
        regime = t("synergy") if alpha > 1 else t("diminishing")
        tag = f" `[{t('estimated_tag')}]`" if is_estimated else ""
        beta_str = f", β = {beta:+.3f}" if abs(beta) > 0.01 else ""

        st.markdown(f"### {color} {elem1}-{elem2}: α = {alpha:.3f}{beta_str}{tag}\n"
                    f"**{t('regime')}**: {regime}")

        if is_estimated:
            conf = est.get("confidence", "?")
            st.warning(f"📊 {t('est_note')}\n\n**{t('confidence')}**: {conf} | {source}")
        elif block == "s/p":
            period = bond.period if bond else 0
            if lp_min == 0:
                st.info(t("lp0"))
            elif lp_min >= 1 and period == 2:
                st.success(t("lp1", lp=lp_min))
            elif lp_min >= 1:
                st.info(t("lp1_heavy", lp=lp_min, per=period))
        elif block == "d":
            st.warning(t("dblock"))

        if not is_estimated:
            st.caption(f"{t('source')}: {source}")

with col2:
    if alpha is not None and energies and len(energies) >= 2:
        orders = sorted(energies.keys())
        E1 = energies[orders[0]]
        a_pred, b_pred = (bond.alpha_beta if bond else (alpha, 0))

        st.subheader(f"{t('scaling')}: {elem1}-{elem2}")

        n_range = np.linspace(orders[0], max(orders[-1], 3), 50)
        E_pred = [E1 * math.exp(a_pred * math.log(n/orders[0]) + b_pred * math.log(n/orders[0])**2)
                  for n in n_range]

        df_pred = pd.DataFrame({"n": n_range, "E = E₁ × n^α": E_pred})
        df_actual = pd.DataFrame({"n": list(energies.keys()), "E actual": list(energies.values())})

        line = alt.Chart(df_pred).mark_line(color="#4C78A8", strokeWidth=2).encode(
            x=alt.X("n:Q", title=t("bond_order") + " n"),
            y=alt.Y("E = E₁ × n^α:Q", title=t("energies")),
        )
        points = alt.Chart(df_actual).mark_circle(size=120, color="#E45756").encode(
            x="n:Q", y=alt.Y("E actual:Q", title=t("energies")),
            tooltip=["n:Q", "E actual:Q"],
        )
        st.altair_chart((line + points).properties(height=350, width=500), use_container_width=True)

        st.markdown(f"**{t('energies')}**")
        rows = []
        for n in orders:
            E_act = energies[n]
            ln_n = math.log(n/orders[0]) if n > orders[0] else 0
            E_p = E1 * math.exp(a_pred * ln_n + b_pred * ln_n**2)
            rows.append({t("bond_order"): n, t("e_actual"): E_act,
                          t("e_predicted"): round(E_p, 1),
                          t("error_pct"): round(100 * (E_p - E_act) / E_act, 1)})
        st.dataframe(pd.DataFrame(rows), hide_index=True)

# ── Full table ──────────────────────────────────────────────────────
st.markdown("---")
with st.expander(t("full_table")):
    rows = []
    for b in sorted(list_all_bonds(), key=lambda x: x.bond):
        a = b.alpha
        if a is not None:
            regime = t("synergy").lower() if a > 1 else t("diminishing").lower()
            a_str = round(a, 3)
        else:
            regime = "—"
            a_str = "—"
        reserve = t("yes") if b.has_reserve else t("no")
        lp_str = str(b.LP_min) if b.LP_min >= 0 else "d"
        rows.append({t("bond"): b.bond, t("block"): b.block, "α": a_str,
                      "LP": lp_str, t("reserve"): reserve, t("regime"): regime})
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

# ── About ───────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(f"### {t('about_title')}")
st.markdown(t("about"))
