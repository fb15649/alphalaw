# alphalaw — Простые кубики природы

## Цель
Не опровергать стандартную модель — **опираясь на неё** найти простое объяснение.
Природа строит бесконечное разнообразие из минимума кубиков (ДНК: 4 буквы → жизнь).
Наш кубик: **вихрь в среде + π**.

## Три слоя

### Слой 1: Материаловедение (доказано)
```
E(n) = E₁ × n^α   →   α>1 = молекула, α<1 = кристалл
48 связей, 76K материалов, 100% точность
```

### Слой 2: π-формулы (паттерн найден)
8 EM-констант = m_e + π. Сжатие 8:1. Этап Бальмера (не Бора).

### Слой 3: Вихревая модель (интерпретация)
Частицы = вихри. Фотон = волна. π = геометрия вращения.

## Structure
```
alphalaw/           # Python package
  calculator.py     # α-law: E(n) = E₁ × n^α
  data.py           # 48 bonds, 50+ elements
  cli.py            # python -m alphalaw C C
  tests/            # 22 pytest tests

scripts/            # Research scripts (50+)
artifacts/          # Documents: vision, compression, building_blocks
```

## Commands
```bash
python -m alphalaw N N              # predict bond
python -m alphalaw --table          # all bonds
python -m pytest alphalaw/tests/ -v # run tests (22 tests)
python scripts/level4_final.py      # verify L4 (needs jarvis-tools)
```

## Key documents
```
artifacts/project_vision.md         # Full project vision v3.0
artifacts/parameter_compression.md  # 19→1+π compression table
artifacts/building_blocks.md        # 1 vortex + 3 rules → everything
paper_ru.md / paper_en.md           # Vortex Theory of Matter
```

## GitHub
- Repo: https://github.com/fb15649/alphalaw
- Current: v2.0.0
