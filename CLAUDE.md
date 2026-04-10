# alphalaw — Bond Order Scaling Law

## Project structure
```
alphalaw/           # Python package
  calculator.py     # α-law: E(n) = E₁ × n^α
  data.py           # 37 bonds, 50+ elements, estimate_alpha()
  cli.py            # python -m alphalaw C C
  web.py            # streamlit UI (optional)
  tests/            # 22 pytest tests

scripts/            # JARVIS-DFT verification (76K materials)
  level4_final.py   # Type combo → 2747/2747 = 100%
  level5_verify.py  # Per-pair stoichiometry → 6995/6995 = 100%
  level6_verify_clean.py  # Crystal structure → 1167/1167 = 100%

artifacts/          # Research docs (level4/5/6_solution.md)
```

## Commands
```bash
python -m alphalaw N N          # predict bond
python -m alphalaw --table      # all bonds
python -m pytest alphalaw/tests/ -v  # run tests
python scripts/level4_final.py  # verify L4 (needs jarvis-tools)
```

## Key rules
- α > 1 = synergy (molecules), α < 1 = diminishing returns (crystals)
- Level 4: 11 element types classify binary pairs
- Level 5: per-pair stoichiometry threshold = oxidation state
- Level 6: density/bonds/spg for polymorphic formulas
- Cascade: L4→L5→L6, each either answers or passes "BOTH" to next

## GitHub
- Repo: https://github.com/fb15649/alphalaw
- Current: v2.0.0
