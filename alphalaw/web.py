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

# ── Data (inline to avoid import issues on deploy) ──────────────────────

BONDS = {
    # s/p block: (α, LP_min, block, energies_dict, source)
    ("C", "C"):   (0.770, 0, "s/p", {1:346, 2:614, 3:839}, "CRC Handbook"),
    ("Si", "Si"): (0.485, 0, "s/p", {1:310, 2:434}, "CRC"),
    ("Ge", "Ge"): (0.407, 0, "s/p", {1:264, 2:350}, "CRC"),
    ("Sn", "Sn"): (0.330, 0, "s/p", {1:187, 2:235}, "CRC"),
    ("N", "N"):   (2.012, 1, "s/p", {1:160, 2:418, 3:945}, "CRC"),
    ("P", "P"):   (1.283, 1, "s/p", {1:201, 2:489}, "CRC"),
    ("O", "O"):   (1.770, 2, "s/p", {1:146, 2:498}, "CRC"),
    ("S", "S"):   (0.676, 2, "s/p", {1:266, 2:425}, "CRC"),
    ("C", "N"):   (0.914, 0, "s/p", {1:305, 2:615, 3:891}, "CRC"),
    ("C", "O"):   (0.909, 0, "s/p", {1:358, 2:745, 3:1077}, "CRC"),
    ("N", "O"):   (1.595, 1, "s/p", {1:201, 2:607}, "CRC"),
    ("B", "N"):   (0.707, 0, "s/p", {1:389, 2:635}, "CRC"),
    ("B", "O"):   (0.589, 0, "s/p", {1:536, 2:806}, "CRC"),
    ("Si", "O"):  (0.502, 0, "s/p", {1:452, 2:640}, "CRC"),
    ("Si", "N"):  (0.405, 0, "s/p", {1:355, 2:470}, "CRC"),
    ("Al", "O"):  (0.560, 0, "s/p", {1:502, 2:740}, "CRC"),
    ("C", "S"):   (1.075, 0, "s/p", {1:272, 2:573}, "CRC"),
    ("C", "P"):   (0.958, 0, "s/p", {1:264, 2:513}, "CRC"),
    ("Ge", "O"):  (0.520, 0, "s/p", {1:401, 2:575}, "CRC"),
    # d-block
    ("Cr", "Cr"): (0.559, -1, "d", {1:70, 4:152}, "Cotton; CRC"),
    ("Mo", "Mo"): (0.651, -1, "d", {1:140, 2:250, 3:350, 4:405, 5:420, 6:435}, "Cotton & Murillo 2005"),
    ("W", "W"):   (0.830, -1, "d", {1:160, 3:500, 4:570, 6:666}, "CRC; Cotton"),
    ("Re", "Re"): (0.868, -1, "d", {1:120, 4:432}, "Bergman 1984; CRC"),
}

def lookup(e1, e2):
    return BONDS.get((e1, e2)) or BONDS.get((e2, e1))

ALL_ELEMENTS = sorted(set(e for pair in BONDS for e in pair))

# ── UI ──────────────────────────────────────────────────────────────────

st.title("⚛️ α-Law Calculator")
st.markdown("""
**Reserve Law of Chemical Bonding**: $E(n) = E_1 \\times n^\\alpha$

Where $\\alpha > 1$ means synergy (each bond strengthens the next) and $\\alpha < 1$ means diminishing returns.
""")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Select elements")
    elem1 = st.selectbox("Element 1", ALL_ELEMENTS, index=ALL_ELEMENTS.index("C"))
    elem2 = st.selectbox("Element 2", ALL_ELEMENTS, index=ALL_ELEMENTS.index("C"))

    data = lookup(elem1, elem2)

    if data is None:
        st.error(f"No data for {elem1}-{elem2}")
    else:
        alpha, lp_min, block, energies, source = data

        # Result card
        if alpha > 1:
            color = "🟢"
            regime = "Synergy"
        else:
            color = "🔴"
            regime = "Diminishing returns"

        st.markdown(f"""
### {color} {elem1}-{elem2}: α = {alpha:.3f}
**Regime**: {regime}
""")

        if block == "s/p":
            if lp_min == 0:
                st.info("**LP = 0** — No recruitable reserve. All electrons in bonds → each additional bond order weaker.")
            elif lp_min >= 1:
                st.success(f"**LP = {lp_min}** — Has reserve! Lone pairs available for π-bonding → synergy.")
        else:
            st.warning("**d-block** — d-electrons form δ-bonds with poor overlap → always diminishing returns.")

        st.caption(f"Source: {source}")

with col2:
    if data is not None:
        alpha, lp_min, block, energies, source = data
        orders = sorted(energies.keys())
        E1 = energies[orders[0]]

        st.subheader(f"Bond energy scaling: {elem1}-{elem2}")

        # Build chart data
        import numpy as np
        n_range = np.linspace(orders[0], max(orders[-1], 3), 50)
        E_pred = [E1 * (n / orders[0]) ** alpha for n in n_range]

        chart_data = {"Bond order": list(n_range), "E predicted (kJ/mol)": E_pred}

        # Actual data points
        actual_n = list(energies.keys())
        actual_E = list(energies.values())

        # Use st.line_chart for predicted curve
        import pandas as pd
        df_pred = pd.DataFrame({"n": n_range, "E = E₁ × n^α": E_pred})
        df_actual = pd.DataFrame({"n": actual_n, "E actual": actual_E})

        import altair as alt

        line = alt.Chart(df_pred).mark_line(color="#4C78A8", strokeWidth=2).encode(
            x=alt.X("n:Q", title="Bond order n"),
            y=alt.Y("E = E₁ × n^α:Q", title="Bond energy (kJ/mol)"),
        )
        points = alt.Chart(df_actual).mark_circle(size=120, color="#E45756").encode(
            x="n:Q",
            y=alt.Y("E actual:Q", title="Bond energy (kJ/mol)"),
            tooltip=["n:Q", "E actual:Q"],
        )
        st.altair_chart((line + points).properties(height=350, width=500),
                         use_container_width=True)

        # Table
        st.markdown("**Energies (kJ/mol)**")
        rows = []
        for n in orders:
            E_act = energies[n]
            E_p = E1 * (n / orders[0]) ** alpha
            rows.append({"Bond order": n, "E actual": E_act,
                          "E predicted": round(E_p, 1),
                          "Error %": round(100 * (E_p - E_act) / E_act, 1)})
        st.dataframe(pd.DataFrame(rows), hide_index=True)

# ── Full table ──────────────────────────────────────────────────────────

st.markdown("---")
with st.expander("📊 Full bond table (23 bonds)"):
    rows = []
    for (e1, e2), (a, lp, blk, ens, src) in sorted(BONDS.items()):
        reserve = "YES" if (blk == "s/p" and lp >= 1) else "NO"
        lp_str = str(lp) if lp >= 0 else "d"
        regime = "synergy" if a > 1 else "diminishing"
        rows.append({"Bond": f"{e1}-{e2}", "Block": blk, "α": round(a, 3),
                      "LP": lp_str, "Reserve": reserve, "Regime": regime})
    import pandas as pd
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

    st.markdown("""
    **Statistics:**
    - LP=0 → α<1: 93% (13/14)
    - LP≥1 → α>1: 80% (4/5)
    - d-block → α<1: 100% (4/4)
    """)

# ── About ───────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("""
### About

The **Reserve Law** states that systems with recruitable reserve show cooperative scaling (α > 1),
while systems without reserve show diminishing returns (α < 1).

- **Paper**: [Reserve Law of Chemical Bonding](paper_alpha_law.md) (Y. Kazin, 2026)
- **Code**: `pip install alphalaw` — [GitHub](https://github.com/ykazin/alphalaw)
- **Contact**: y.kazin@kazin.ru
""")
