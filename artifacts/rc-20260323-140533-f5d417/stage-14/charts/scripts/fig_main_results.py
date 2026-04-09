
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Academic styling
try:
    plt.style.use(['science', 'ieee'])
except Exception:
    try:
        plt.style.use(['seaborn-v0_8-whitegrid'])
    except Exception:
        pass  # Use default matplotlib style

# Colorblind-safe palette
COLORS = ['#4477AA', '#EE6677', '#228833', '#CCBB44', '#66CCEE', '#AA3377', '#BBBBBB']
LINE_STYLES = ['-', '--', '-.', ':']
MARKERS = ['o', 's', '^', 'D', 'v', 'P', '*', 'X']

# Publication settings
plt.rcParams.update({
    "font.size": 8,
    "axes.titlesize": 9,
    "axes.labelsize": 8,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "legend.fontsize": 7,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.15,
})

# Data
conditions = ['Proving_baseline_1', 'Proving_baseline_2', 'Proving_proposed']
values = [1.0, 0.040004, 0.050826]
ci_low = [1.0, 0.040004, 0.050826]
ci_high = [1.0, 0.040004, 0.050826]

# Plot
fig, ax = plt.subplots(figsize=(3.5, 3.0), constrained_layout=True)
x = np.arange(len(conditions))
bar_colors = [COLORS[i % len(COLORS)] for i in range(len(conditions))]

yerr_lo = [max(0, v - lo) for v, lo in zip(values, ci_low)]
yerr_hi = [max(0, hi - v) for v, hi in zip(values, ci_high)]

bars = ax.bar(x, values, color=bar_colors, alpha=0.85, edgecolor="white", linewidth=0.5)
ax.errorbar(x, values, yerr=[yerr_lo, yerr_hi],
            fmt="none", ecolor="#333", capsize=4, capthick=1.2, linewidth=1.2)

# Value labels
offset = max(yerr_hi) * 0.08 if yerr_hi and max(yerr_hi) > 0 else max(values) * 0.02
for i, v in enumerate(values):
    ax.text(i, v + offset, f"{v:.4f}", ha="center", va="bottom", fontweight="bold")

ax.set_xlabel("Method")
ax.set_ylabel("Primary Metric")
ax.set_title("Method Comparison")
ax.set_xticks(x)
ax.set_xticklabels([c.replace("_", " ") for c in conditions], rotation=25, ha="right")
ax.grid(True, axis="y", alpha=0.3)
ax.set_axisbelow(True)
fig.savefig("/workspace/output/fig_main_results.png")
plt.close(fig)
print(f"Saved: /workspace/output/fig_main_results.png")
