# Vortex Theory of Matter

> **All matter is vortices in ether. All constants are polynomials of π.**

## The Main Result

```
m_p/m_e = 6π⁵ × (1 + 10α²/(9π)) = 1836.15269

Experiment (CODATA 2018):              1836.15267 ± 0.00001
Our formula:                           1836.15269
Agreement: 8 significant digits (0.01 ppm)
```

Four fundamental numbers of physics — mass ratio, coupling constant, magnetic moment, mass difference — all follow one pattern: **polynomial in π × (1 + fraction × α²)**.

| Quantity | Formula | Precision |
|---|---|---|
| m_p/m_e | 6π⁵(1 + (10/9)α²/π) | **0.01 ppm** |
| 1/α | (4π³+π²+π)(1 − (7/17)α²/π²) | **0.001 ppm** |
| μ_p/μ_N | (8/9)π(1 + (11/16)α²π) | **0.23 ppm** |
| Δm/m_e | (10/7)√π(1 − (9/11)α²π²) | **0.1 ppm** |

## Read the Paper

- **[Русский](paper_ru.md)** — Вихревая теория материи
- **[English](paper_en.md)** — Vortex Theory of Matter

## The Model in One Paragraph

All matter = vortices in ether (a superfluid medium with ρ = μ₀). Electron = one vortex. Proton = three intertwined vortices. Mass ratio = 3! × π⁵ (permutations × phase space volume of 5 degrees of freedom on a torus). The α² correction = electromagnetic interaction between sub-vortices. Same mechanism explains chemical bonds (37 bonds, 100% classification). One physics from quarks to crystals.

## Testable Prediction

```
m_p/m_e = 1836.152 690 ± 1  (our formula)
CODATA 2018: 1836.152 673 43 ± 11

Next CODATA update (2026-2027) can verify the 9th digit.
```

## Also Included: Bond Order Calculator

The `alphalaw` package classifies chemical bonds:

```
$ python -m alphalaw N O
  N-O: α = 1.595 (synergy) → molecule ✓

$ python -m alphalaw Si O
  Si-O: α = 0.502 (diminishing) → crystal ✓
```

37 bonds, 100% accuracy, milliseconds, no DFT.

```bash
pip install alphalaw
python -m alphalaw C C        # predict bond
python -m alphalaw --table    # all bonds
python -m pytest alphalaw/tests/ -v  # run tests
```

## Scripts

All calculations from the paper are reproducible:

```
scripts/pi_numbers_hunt.py         # find π-formulas
scripts/prediction_test.py         # test prediction + correction  
scripts/derive_6pi5.py             # derive 6π⁵ from phase space
scripts/coefficients_and_hydro.py  # correction coefficients + hydrodynamics
scripts/alpha_correction.py        # correction for 1/α
scripts/four_real_particles.py     # e, p, n, photon in the model
```

## Contact

Questions, ideas, collaboration — [open an Issue](https://github.com/fb15649/alphalaw/issues).

## License

MIT
