"""
THREE FREQUENCIES OF A TORUS (bond)
====================================

Every torus (bond) has:
  ω₁ ∝ E₁ = σ-frequency (single bond energy)
  ω₂ ∝ Δ₂ = E₂ - E₁ = π-frequency (what double bond ADDS)
  ω₃ = |ω₁ - ω₂| = beat frequency

What can we learn from all three?
"""
import sys, math
import numpy as np
sys.path.insert(0, '/Volumes/Backup/Python_projects/alphalaw')
from alphalaw.data import BONDS

MUSIC = [
    (1,1,'1:1'), (9,8,'9:8'), (8,7,'8:7'), (7,6,'7:6'),
    (6,5,'6:5'), (5,4,'5:4'), (4,3,'4:3'), (7,5,'7:5'),
    (3,2,'3:2'), (8,5,'8:5'), (5,3,'5:3'), (7,4,'7:4'),
    (2,1,'2:1'), (3,1,'3:1'),
]

def nearest_music(ratio):
    best = min(MUSIC, key=lambda m: abs(ratio - m[0]/m[1]))
    r = best[0]/best[1]
    pct = abs(ratio - r)/r * 100
    return best[2], r, pct


print("=" * 70)
print("  ТРИ ЧАСТОТЫ ТОРА: σ, π, БИЕНИЯ")
print("=" * 70)
print()

# ============================================================
# Extract three frequencies for all bonds with ≥2 bond orders
# ============================================================
data = []

print(f"{'Bond':>8} {'E₁(σ)':>6} {'Δ₂(π)':>6} {'Beat':>6} {'σ/π':>6} {'Интервал':>8} {'Δ%':>5} {'α':>6}")
print(f"{'─'*58}")

for b in sorted(BONDS, key=lambda x: x.alpha if x.alpha else 0):
    if b.alpha is None: continue
    orders = sorted(b.energies.keys())
    if len(orders) < 2: continue

    E1 = b.energies[orders[0]]
    E2 = b.energies[orders[1]]

    sigma = E1           # σ-frequency
    pi = E2 - E1         # π-frequency
    beat = abs(sigma - pi)  # beat frequency

    if pi <= 0: continue

    ratio = sigma / pi   # σ/π ratio
    name, val, pct = nearest_music(ratio)

    marker = "★" if pct < 1 else ("♪" if pct < 3 else "·" if pct < 5 else " ")

    print(f"{b.bond:>8} {sigma:>6.0f} {pi:>6.0f} {beat:>6.0f} {ratio:>6.3f} {name:>8} {pct:>4.1f}% {b.alpha:>6.3f} {marker}")

    data.append({
        'bond': b.bond, 'sigma': sigma, 'pi': pi, 'beat': beat,
        'ratio': ratio, 'alpha': b.alpha, 'period': b.period,
        'interval': name, 'interval_err': pct,
    })

    # Also compute Δ₃ if triple bond exists
    if len(orders) >= 3:
        E3 = b.energies[orders[2]]
        delta3 = E3 - E2
        r2 = pi / delta3 if delta3 > 0 else 0
        name2, val2, pct2 = nearest_music(r2) if r2 > 0 else ('?', 0, 0)
        # print(f"         Δ₃={delta3:>4.0f}  π/Δ₃={r2:.3f} ≈ {name2} ({pct2:.1f}%)")


# ============================================================
# Statistics
# ============================================================
print(f"\n{'='*70}")
print(f"  СТАТИСТИКА")
print(f"{'='*70}\n")

ratios = [d['ratio'] for d in data]
beats = [d['beat'] for d in data]
alphas_arr = [d['alpha'] for d in data]
sigmas = [d['sigma'] for d in data]
pis = [d['pi'] for d in data]

# How many σ/π ratios hit musical intervals?
hits = {1:0, 3:0, 5:0}
for d in data:
    for t in hits:
        if d['interval_err'] < t: hits[t] += 1

n = len(data)
print(f"  σ/π попадает в муз. интервал (из {n} связей):")
print(f"    < 1%: {hits[1]}/{n} = {hits[1]/n*100:.0f}%")
print(f"    < 3%: {hits[3]}/{n} = {hits[3]/n*100:.0f}%")
print(f"    < 5%: {hits[5]}/{n} = {hits[5]/n*100:.0f}%")

# Random comparison
np.random.seed(42)
rand_ratios = np.random.uniform(0.3, 3.0, 10000)
r_hits = {1:0, 3:0, 5:0}
for rr in rand_ratios:
    _, _, pct = nearest_music(rr)
    for t in r_hits:
        if pct < t: r_hits[t] += 1

nr = len(rand_ratios)
print(f"\n  Случайное (uniform [0.3, 3.0]):")
print(f"    < 1%: {r_hits[1]/nr*100:.0f}%")
print(f"    < 3%: {r_hits[3]/nr*100:.0f}%")
print(f"    < 5%: {r_hits[5]/nr*100:.0f}%")

# P-value
from math import comb
def binom_p(k, n, p):
    return sum(comb(n, i) * p**i * (1-p)**(n-i) for i in range(k, n+1))

p3 = binom_p(hits[3], n, r_hits[3]/nr)
p1 = binom_p(hits[1], n, r_hits[1]/nr)
print(f"\n  P-values:")
print(f"    < 3%: p = {p3:.6f} {'★ ЗНАЧИМО' if p3 < 0.05 else ''}")
print(f"    < 1%: p = {p1:.6f} {'★ ЗНАЧИМО' if p1 < 0.05 else ''}")


# ============================================================
# Correlations: what does beat frequency predict?
# ============================================================
print(f"\n{'='*70}")
print(f"  КОРРЕЛЯЦИИ: ЧТО ПРЕДСКАЗЫВАЕТ ЧАСТОТА БИЕНИЙ?")
print(f"{'='*70}\n")

beats_arr = np.array(beats)
alphas_np = np.array(alphas_arr)
sigmas_np = np.array(sigmas)
pis_np = np.array(pis)
ratios_np = np.array(ratios)

# Beat vs α
r_beat_alpha = np.corrcoef(beats_arr, alphas_np)[0, 1]
# σ vs α
r_sigma_alpha = np.corrcoef(sigmas_np, alphas_np)[0, 1]
# π vs α
r_pi_alpha = np.corrcoef(pis_np, alphas_np)[0, 1]
# σ/π vs α
r_ratio_alpha = np.corrcoef(ratios_np, alphas_np)[0, 1]
# beat/σ (normalized beat)
beat_norm = beats_arr / sigmas_np
r_bnorm_alpha = np.corrcoef(beat_norm, alphas_np)[0, 1]

print(f"  Корреляция с α:")
print(f"    σ (E₁):           r = {r_sigma_alpha:+.3f}")
print(f"    π (E₂−E₁):       r = {r_pi_alpha:+.3f}")
print(f"    σ/π (отношение):  r = {r_ratio_alpha:+.3f}")
print(f"    beat (|σ−π|):     r = {r_beat_alpha:+.3f}")
print(f"    beat/σ (норм.):   r = {r_bnorm_alpha:+.3f}")

# The KEY: beat/σ = normalized beat
# If beat/σ → 0 → σ ≈ π → unison → border (α ≈ 1)
# If beat/σ → 1 → π → 0 → no π-bond → crystal (α < 1)
# If beat/σ > 1 → π > σ → synergy → molecule (α > 1)

print(f"""
  Физический смысл beat/σ:
    beat/σ → 0: σ ≈ π (унисон, граница, α ≈ 1)
    beat/σ → 1: π → 0 (нет π-связи, кристалл, α < 1)
    beat/σ > 1: π > σ (синергия, молекула, α > 1)
""")


# ============================================================
# Triple bonds: Δ₃ as THIRD frequency
# ============================================================
print(f"{'='*70}")
print(f"  ТРОЙНЫЕ СВЯЗИ: ТРИ ПОЛНЫХ ЧАСТОТЫ")
print(f"{'='*70}\n")

print(f"{'Bond':>8} {'Δ₁(σ)':>6} {'Δ₂(π)':>6} {'Δ₃(δ?)':>6} {'σ/π':>6} {'π/Δ₃':>6} {'σ/Δ₃':>6}")
print(f"{'─'*50}")

for b in BONDS:
    if b.alpha is None: continue
    orders = sorted(b.energies.keys())
    if len(orders) < 3: continue

    E1 = b.energies[orders[0]]
    E2 = b.energies[orders[1]]
    E3 = b.energies[orders[2]]

    d1 = E1
    d2 = E2 - E1
    d3 = E3 - E2

    r_sp = d1/d2 if d2 > 0 else 0
    r_pd = d2/d3 if d3 > 0 else 0
    r_sd = d1/d3 if d3 > 0 else 0

    # Find nearest intervals
    name1, _, pct1 = nearest_music(r_sp) if r_sp > 0 else ('?',0,0)
    name2, _, pct2 = nearest_music(r_pd) if r_pd > 0 else ('?',0,0)
    name3, _, pct3 = nearest_music(r_sd) if r_sd > 0 else ('?',0,0)

    print(f"{b.bond:>8} {d1:>6.0f} {d2:>6.0f} {d3:>6.0f} {r_sp:>6.3f}≈{name1} {r_pd:>6.3f}≈{name2} {r_sd:>6.3f}≈{name3}")

print(f"""
  С тремя частотами получаем ТРИ отношения:
    σ/π: как σ-мода относится к π-моде
    π/Δ₃: как π относится к третьей (δ?) моде
    σ/Δ₃: как σ относится к третьей моде

  Для аккорда (3 ноты) = ТРЕЗВУЧИЕ.
  Мажорное трезвучие: 4:5:6
  Минорное: 10:12:15
  Проверим:
""")

for b in BONDS:
    if b.alpha is None: continue
    orders = sorted(b.energies.keys())
    if len(orders) < 3: continue

    E1 = b.energies[orders[0]]
    E2 = b.energies[orders[1]]
    E3 = b.energies[orders[2]]

    d1 = E1; d2 = E2-E1; d3 = E3-E2

    # Normalize to smallest
    m = min(d1, d2, d3) if min(d1,d2,d3) > 0 else 1
    n1, n2, n3 = d1/m, d2/m, d3/m

    print(f"  {b.bond:>8}: Δ₁:Δ₂:Δ₃ = {n1:.2f} : {n2:.2f} : {n3:.2f}")

    # Check known chords
    for chord_name, a, b_c, c_c in [('мажор',4,5,6),('минор',10,12,15),
                                      ('dim',5,6,7),('aug',4,5,6.3)]:
        # Normalize chord
        cm = min(a,b_c,c_c)
        ca, cb, cc = a/cm, b_c/cm, c_c/cm
        err = (abs(n1-ca)/ca + abs(n2-cb)/cb + abs(n3-cc)/cc) / 3 * 100
        if err < 15:
            print(f"           ≈ {chord_name} ({a}:{b_c}:{c_c}) err={err:.0f}%")
