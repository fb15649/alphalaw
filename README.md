# Vortex Theory of Matter

> **One building block (vortex). One number (π). Eight constants to ppm.**

The Standard Model uses 19 free parameters — 19 numbers fitted from experiment with no explanation. We show that **8 of them** follow from a single parameter (m_e) and the number π. Compression ratio: **8:1**.

## The Formulas

| # | Quantity | Formula | Precision |
|---|----------|---------|-----------|
| 1 | m_p/m_e | 6π⁵(1 + (10/9)α²/π) | **0.01 ppm** (8 digits) |
| 2 | 1/α | (4π³+π²+π)(1 − (7/17)α²/π²) | **0.001 ppm** (9 digits) |
| 3 | μ_p/μ_N | (8/9)π(1 + (11/16)α²π) | **0.23 ppm** |
| 4 | Δm/m_e | (10/7)√π(1 − (9/11)α²π²) | **0.1 ppm** |
| 5 | m_d/m_p | 2 − (17/9)π²α² | **< 1 ppm** |
| 6 | μ_d/μ_N | 15/π^(5/2) | **0.003%** |
| 7 | R_p | 4ℏ/(m_p c) | **0.02%** |
| 8 | g−2 | QED series with our α | **10 digits** |

All formulas share one structure: **π-polynomial × (1 + fraction × α²)**.

The polynomial Q(x) = 4x²+x+1 from the 1/α formula has roots on |z| = 1/2 **exactly** — the fermion spin. P(all coincidences random) < 10⁻⁹.

## Predictions (testable 2027–2030)

| Prediction | Value | Experiment | When |
|---|---|---|---|
| m_p/m_e 9th digit | 1836.152690 ± 1 | CODATA 2027 | ~2027 |
| Neutrino Σm | 77 meV | CMB-S4 | ~2030 |
| Neutrino m₃ | 63 meV | Project 8 | ~2028 |
| Neutrino hierarchy | Normal | JUNO, DUNE | 2026–2030 |

## Bond Order Calculator

The `alphalaw` package classifies chemical bonds via power law E(n) = E₁ × n^α:

```bash
$ python -m alphalaw N O
  N-O: α = 1.595 (synergy) → molecule ✓

$ python -m alphalaw Si O
  Si-O: α = 0.502 (diminishing) → crystal ✓
```

48 bonds, 76,000 JARVIS-DFT materials, **100% accuracy**.

```bash
pip install alphalaw
python -m alphalaw C C
python -m alphalaw --table
python -m pytest alphalaw/tests/ -v
```

## Read the Paper

- **[English](paper_en.md)** — Vortex Theory of Matter
- **[Русский](paper_ru.md)** — Вихревая теория материи

## License

MIT
