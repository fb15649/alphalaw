"""
Send vortex theory to GLM-5 for independent critical review.
Uses Zhipu AI API (OpenAI-compatible).
"""
import os
from openai import OpenAI

API_KEY = "c22283fedc024498b468b00301a68ca9.PcL2w1KwyhL6ex85"
BASE_URL = "https://api.z.ai/api/coding/paas/v4"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# === REVIEW PROMPT ===
THEORY_TEXT = """
# Вихревая теория материи — краткое изложение для рецензии

## 1. Основная гипотеза
Элементарные частицы = тороидальные вихри в сверхтекучей среде (эфире).
Плотность среды: ρ = μ₀ = 1.257×10⁻⁶ кг/м³ (магнитная проницаемость вакуума).
Циркуляция квантована: Γ = h/m (как в сверхтекучем гелии He-II).

## 2. Восемь π-формул (все проверены численно)

    m_p/m_e = 6π⁵(1 + (10/9)α²/π)           точность 0.01 ppm
    1/α     = (4π³+π²+π)(1 − (7/17)α²/π²)   точность 0.001 ppm
    μ_p/μ_N = (8/9)π(1 + (11/16)α²π)         точность 0.23 ppm
    Δm/m_e  = (10/7)√π(1 − (9/11)α²π²)      точность 0.1 ppm
    m_d/m_p = 2 − (17/9)π²α²                 точность < 1 ppm
    μ_d/μ_N = 15/π^(5/2)                      точность 0.003%
    R_p     = 4ℏ/(m_p·c)                      точность 0.02%
    g−2     = QED(наша α) → 10 совпадающих цифр

## 3. Химические связи (α-law)
E(n) = E₁ × n^α — энергия связи порядка n.
α определяется отношением π-канала к σ-каналу (π/σ).
π/σ > 1 ↔ α > 1 → молекула (самоусиление, Хальбах).
π/σ < 1 ↔ α < 1 → кристалл (конкуренция).
Корреляция π/σ vs α: r = 0.989. Проверено на 37 связях.

## 4. Yang-Mills (массовая щель)
Аргумент: вихри в эфире → группа кос B_N → SU(N).
Зацепление вихрей → helicity H ≠ 0 → E ≥ C|H|^{3/2}/V^{1/2} > 0 (Фридман-Хе 1991).
Дискретность Lk ∈ ℤ → массовая щель Δ > 0.
Статус: физический аргумент (не строгое доказательство).

## 5. Navier-Stokes (регулярность)
Цепочка: Γ = h/m (квантование) + r ≥ ƛ_C (конечное ядро) → ω_max = 2mc²/ℏ →
BKM-интеграл конечен → нет blow-up → глобальная регулярность.
Для h=0 (классический случай): аргумент через пересоединение вихрей.
Лемма о пересоединении (не доказана): при d ≤ Cν/Γ, omega убывает.
Статус: физическое предсказание, математически не доказано.
"""

REVIEW_PROMPT = """Ты — независимый рецензент-физик. Тебе дана краткая теория.
Твоя задача — найти ОШИБКИ и СЛАБЫЕ МЕСТА. Не хвали, а критикуй.

Ответь строго по структуре:

1. ЧИСЛЕННЫЕ ОШИБКИ: проверь каждую из 8 формул. Вычисли левую и правую части.
   Для каждой формулы напиши: LHS = ..., RHS = ..., разница = ... ppm.
   Если ошибка > 1 ppm — отметь.

2. ЛОГИЧЕСКИЕ ОШИБКИ: найди 3 самых слабых звена в цепочке рассуждений.
   Для каждого объясни ПОЧЕМУ это слабое место.

3. ТАВТОЛОГИИ: есть ли утверждения, которые выглядят как результат,
   но на самом деле следуют из определений (круговая логика)?

4. ФИЗИЧЕСКИЕ ПРОБЛЕМЫ: что противоречит экспериментально установленным фактам?
   Конкретно: ρ = μ₀ — откуда? Γ = h/m — почему не h/(2m) или h/(3m)?

5. СРАВНЕНИЕ С СУЩЕСТВУЮЩИМИ РЕЗУЛЬТАТАМИ: есть ли в литературе аналогичные
   формулы? Насколько наши формулы оригинальны vs. давно известны?

Будь максимально критичен. Мне нужна ЧЕСТНАЯ оценка, не комплименты.
"""

print("=" * 80)
print("  ОТПРАВКА ВИХРЕВОЙ ТЕОРИИ НА РЕЦЕНЗИЮ В GLM-5")
print("=" * 80)
print()
print("Отправляю запрос... (может занять 30-60 секунд)")
print()

try:
    response = client.chat.completions.create(
        model="glm-5",
        messages=[
            {"role": "system", "content": "Ты — эксперт по математической физике с 20-летним опытом. Отвечай на русском."},
            {"role": "user", "content": THEORY_TEXT + "\n\n" + REVIEW_PROMPT}
        ],
        temperature=0.3,
        max_tokens=16384,
    )

    msg = response.choices[0].message
    review = msg.content or ""

    # Debug: check for reasoning/thinking content
    if hasattr(msg, 'reasoning_content') and msg.reasoning_content:
        print("[DEBUG] reasoning_content найден, длина:", len(msg.reasoning_content))
    if hasattr(msg, 'tool_calls') and msg.tool_calls:
        print("[DEBUG] tool_calls:", msg.tool_calls)

    # Try to get content from different fields
    if not review:
        # Try raw dict access
        raw = msg.model_dump() if hasattr(msg, 'model_dump') else {}
        print("[DEBUG] Message fields:", list(raw.keys()))
        for k, v in raw.items():
            if v and k != 'role':
                print(f"[DEBUG] {k} = {str(v)[:500]}")
        # Check if content is in reasoning
        if 'reasoning_content' in raw and raw['reasoning_content']:
            review = raw['reasoning_content']

    print("─" * 80)
    print("  РЕЦЕНЗИЯ GLM-5")
    print("─" * 80)
    print()
    print(review if review else "(пустой ответ)")
    print()
    print("─" * 80)
    print(f"  Модель: {response.model}")
    print(f"  Токены: prompt={response.usage.prompt_tokens}, "
          f"completion={response.usage.completion_tokens}")
    print("─" * 80)

except Exception as e:
    print(f"ОШИБКА: {e}")
    print()
    print("Возможные причины:")
    print("  1. API-ключ не имеет доступа к GLM-5 (только glm-4-flash)")
    print("  2. Сетевая ошибка / прокси")
    print("  3. Модель GLM-5 недоступна через этот endpoint")
    print()
    print("Попробую glm-4-plus как fallback...")

    try:
        response = client.chat.completions.create(
            model="glm-5.1",
            messages=[
                {"role": "system", "content": "Ты — эксперт по математической физике с 20-летним опытом. Отвечай на русском."},
                {"role": "user", "content": THEORY_TEXT + "\n\n" + REVIEW_PROMPT}
            ],
            temperature=0.3,
            max_tokens=16384,
        )

        review = response.choices[0].message.content

        print()
        print("─" * 80)
        print(f"  РЕЦЕНЗИЯ {response.model} (fallback)")
        print("─" * 80)
        print()
        print(review)
        print()
        print("─" * 80)
        print(f"  Модель: {response.model}")
        print(f"  Токены: prompt={response.usage.prompt_tokens}, "
              f"completion={response.usage.completion_tokens}")
        print("─" * 80)

    except Exception as e2:
        print(f"Fallback тоже не сработал: {e2}")
