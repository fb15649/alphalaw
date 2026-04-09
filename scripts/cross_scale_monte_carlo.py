#!/usr/bin/env python3
"""
Cross-scale α Monte Carlo analysis.
Tests whether cross-domain α matches are statistically significant.
"""
import numpy as np
from scipy import stats
from dataclasses import dataclass

@dataclass
class CrossScalePair:
    """A pair of α values from different scales."""
    atomic_bond: str
    atomic_alpha: float
    other_domain: str
    other_system: str
    other_alpha: float
    other_alpha_err: float  # error bar if known, else 0
    has_reserve: bool       # does the other system have "reserve"?
    source: str

    @property
    def delta_pct(self):
        """Percent difference."""
        return abs(self.atomic_alpha - self.other_alpha) / self.atomic_alpha * 100


# Known atomic α values (the "targets" to match against)
ATOMIC_ALPHAS = {
    "C-C": 0.770,
    "Si-Si": 0.485,
    "Ge-Ge": 0.407,
    "Sn-Sn": 0.330,
    "N-N": 2.012,
    "P-P": 1.283,
    "O-O": 1.770,
    "S-S": 0.676,
    "C-N": 0.914,
    "C-O": 0.909,
    "N-O": 1.595,
}

# Existing cross-scale pairs (from previous session)
EXISTING_PAIRS = [
    CrossScalePair("C-C", 0.80, "neuroscience", "habituation (no dopamine)",
                   0.83, 0.05, False, "Rankin & Broster 1992"),
    CrossScalePair("P-P", 1.28, "neuroscience", "LTP + dopamine",
                   1.26, 0.08, True, "Lisman et al. 2011"),
]

# NEW pairs from web search
NEW_PAIRS = [
    CrossScalePair("N-N", 2.012, "network", "Metcalfe's law (Facebook/Tencent)",
                   2.0, 0.1, True, "Zhang Liu Xu 2015, J Comp Sci Tech"),
    CrossScalePair("P-P", 1.283, "urban_scaling", "patents vs city size (US MSAs)",
                   1.27, 0.05, True, "Bettencourt et al. 2007, PNAS"),
    CrossScalePair("C-C", 0.770, "allometry", "Kleiber's law (metabolic rate vs mass)",
                   0.75, 0.02, False, "Kleiber 1932; West Brown Enquist 1997"),
]


def monte_carlo_test(pairs, n_simulations=100_000, tolerance_pct=5.0):
    """
    Monte Carlo test: what's the probability that K random exponent pairs
    would ALL match within `tolerance_pct`%?

    For each domain, we sample from a uniform distribution spanning the
    typical range of exponents in that domain.
    """
    # Domain ranges (empirical ranges of exponents in each field)
    DOMAIN_RANGES = {
        "neuroscience": (0.3, 2.5),        # habituation to LTP exponents
        "pharmacology": (0.3, 3.0),        # Hill coefficients
        "learning": (0.1, 1.5),            # power law of practice
        "network": (1.0, 3.0),             # Sarnoff(1) to Reed/cube(3)
        "ecology": (0.05, 0.5),            # species-area z
        "economics": (0.5, 1.5),           # returns to scale
        "fatigue": (0.3, 0.8),             # Coffin-Manson |c|
        "urban_scaling": (0.7, 1.5),       # sub- to superlinear urban exponents
        "allometry": (0.5, 1.0),           # 2/3 to 1.0 range
    }

    atomic_range = (min(ATOMIC_ALPHAS.values()), max(ATOMIC_ALPHAS.values()))

    K = len(pairs)
    if K == 0:
        return 1.0

    count_all_match = 0

    for _ in range(n_simulations):
        all_match = True
        for pair in pairs:
            domain = pair.other_domain
            lo, hi = DOMAIN_RANGES.get(domain, (0.1, 2.5))

            # Random exponent from domain range
            random_other = np.random.uniform(lo, hi)
            # Random atomic α
            random_atomic = np.random.uniform(*atomic_range)

            # Check if they match within tolerance
            if random_atomic != 0:
                delta = abs(random_other - random_atomic) / random_atomic * 100
                if delta > tolerance_pct:
                    all_match = False
                    break

        if all_match:
            count_all_match += 1

    return count_all_match / n_simulations


def fisher_combined_pvalue(p_values):
    """Fisher's method to combine independent p-values."""
    chi2_stat = -2 * sum(np.log(p) for p in p_values if p > 0)
    df = 2 * len(p_values)
    return stats.chi2.sf(chi2_stat, df)


def analyze_pairs(pairs):
    """Full analysis of cross-scale pairs."""
    print("=" * 80)
    print("CROSS-SCALE α ANALYSIS")
    print("=" * 80)

    print(f"\n{'Atomic':10s} {'α_atom':>7s}  {'Domain':15s} {'System':30s} "
          f"{'α_other':>7s} {'Δ%':>5s} {'Reserve':>7s}")
    print("-" * 90)

    for p in pairs:
        res = "YES" if p.has_reserve else "NO"
        match = "✓" if p.delta_pct < 5 else "~" if p.delta_pct < 10 else "✗"
        print(f"{p.atomic_bond:10s} {p.atomic_alpha:7.3f}  {p.other_domain:15s} "
              f"{p.other_system:30s} {p.other_alpha:7.3f} {p.delta_pct:5.1f} "
              f"{res:>7s} {match}")

    # Reserve rule check
    print(f"\nReserve rule check:")
    correct = sum(1 for p in pairs
                  if (p.has_reserve and p.other_alpha > 1) or
                     (not p.has_reserve and p.other_alpha < 1))
    print(f"  Reserve → α>1: {correct}/{len(pairs)} = {100*correct/len(pairs):.0f}%")

    # Tight matches (<5%)
    tight = [p for p in pairs if p.delta_pct < 5]
    print(f"  Tight matches (Δ<5%): {len(tight)}/{len(pairs)}")

    # Monte Carlo
    print(f"\nMonte Carlo test (100K simulations, tolerance=5%):")
    p_mc = monte_carlo_test(pairs)
    print(f"  P(all {len(pairs)} pairs match randomly) = {p_mc:.6f}")
    if p_mc < 0.05:
        print(f"  → SIGNIFICANT at α=0.05")
    if p_mc < 0.001:
        print(f"  → HIGHLY SIGNIFICANT at α=0.001")

    # Individual domain p-values for Fisher's method
    print(f"\nPer-domain p-values:")
    p_values = []
    for p in pairs:
        p_single = monte_carlo_test([p], tolerance_pct=5)
        p_values.append(max(p_single, 1e-6))  # avoid log(0)
        print(f"  {p.other_domain:15s}: p = {p_single:.4f}")

    if len(p_values) >= 2:
        p_fisher = fisher_combined_pvalue(p_values)
        print(f"\nFisher's combined p-value: {p_fisher:.6f}")

    return p_mc


if __name__ == "__main__":
    all_pairs = EXISTING_PAIRS + NEW_PAIRS
    analyze_pairs(all_pairs)
