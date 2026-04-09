
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
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.15,
})

# Data: conditions x metrics
conditions = ['Proving_baseline_1', 'Proving_baseline_2', 'Proving_proposed']
metric_names = ['Epochs', 'Proving_baseline_1_loss', 'Proving_baseline_1_primary_metric', 'Proving_baseline_1_secondary_metric', 'Proving_baseline_1/42/primary_metric']
# data_matrix[i][j] = value for condition i, metric j
data_matrix = [[0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0]]

# Plot
n_groups = len(conditions)
n_bars = len(metric_names)
fig, ax = plt.subplots(figsize=(7.0, 3.0), constrained_layout=True)
x = np.arange(n_groups)
bar_width = 0.8 / n_bars

for j, metric in enumerate(metric_names):
    offset = (j - n_bars / 2 + 0.5) * bar_width
    vals = [data_matrix[i][j] for i in range(n_groups)]
    ax.bar(x + offset, vals, bar_width, label=metric.replace("_", " "),
           color=COLORS[j % len(COLORS)], alpha=0.85, edgecolor="white", linewidth=0.5)

ax.set_xlabel("Method")
ax.set_ylabel("Score")
ax.set_title("Multi-Metric Comparison")
ax.set_xticks(x)
ax.set_xticklabels([c.replace("_", " ") for c in conditions], rotation=25, ha="right")
ax.legend(loc="upper left", bbox_to_anchor=(0, 1), framealpha=0.9, edgecolor="gray")
ax.grid(True, axis="y", alpha=0.3)
ax.set_axisbelow(True)
fig.savefig("/workspace/output/fig_multi_metric.png")
plt.close(fig)
print(f"Saved: /workspace/output/fig_multi_metric.png")
