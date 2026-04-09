#!/usr/bin/env python3
"""
α-law expansion to d-block metals.
Calculate α from bond dissociation energies at multiple bond orders.
Test RE (Reserve Electrons) → α rule.
"""
import math
import numpy as np
from scipy import stats
from dataclasses import dataclass

@dataclass
class BondData:
    """Bond energy data for one bond type."""
    bond: str           # e.g. "Cr-Cr"
    block: str          # "s/p" or "d" or "f"
    period: int         # period of heavier atom
    valence_e_A: int    # valence electrons atom A
    valence_e_B: int    # valence electrons atom B
    LP_A: int           # lone pairs atom A (for s/p block)
    LP_B: int           # lone pairs atom B
    energies: dict      # {bond_order: energy_kJ_mol}
    source: str         # data source
    # Morse parameters (if available)
    omega_e: float = None     # cm⁻¹
    omega_e_xe: float = None  # cm⁻¹
    r_e: float = None         # Å

    @property
    def alpha(self):
        """Calculate α from E(n) = E₁ × n^α."""
        orders = sorted(self.energies.keys())
        if len(orders) < 2:
            return None
        E1 = self.energies[orders[0]]
        if E1 <= 0:
            return None
        # For 2 points: α = log(E₂/E₁) / log(n₂/n₁)
        if len(orders) == 2:
            n1, n2 = orders
            E_n1, E_n2 = self.energies[n1], self.energies[n2]
            if E_n1 <= 0 or E_n2 <= 0:
                return None
            return math.log(E_n2 / E_n1) / math.log(n2 / n1)
        # For 3+ points: linear regression of log(E_n/E₁) vs log(n)
        log_n = [math.log(n / orders[0]) for n in orders[1:]]
        log_ratio = [math.log(self.energies[n] / E1) for n in orders[1:]]
        slope, _, _, _, _ = stats.linregress(log_n, log_ratio)
        return slope

    @property
    def RE_A(self):
        """Reserve electrons for atom A at bond order 1."""
        return self.valence_e_A - 2

    @property
    def RE_B(self):
        """Reserve electrons for atom B at bond order 1."""
        return self.valence_e_B - 2

    @property
    def RE_min(self):
        """Bottleneck rule: minimum reserve."""
        return min(self.RE_A, self.RE_B)

    @property
    def LP_min(self):
        """Classic LP_min for s/p block."""
        return min(self.LP_A, self.LP_B)

    @property
    def reserve(self):
        """Unified reserve metric: LP for s/p, RE/2 for d-block."""
        if self.block == "d":
            return self.RE_min / 2
        return self.LP_min

    @property
    def x_e(self):
        """Morse anharmonicity parameter."""
        if self.omega_e and self.omega_e_xe:
            return self.omega_e_xe / self.omega_e
        return None


# =============================================================================
# EXISTING s/p-block data (from previous research)
# =============================================================================
SP_BLOCK = [
    BondData("C-C", "s/p", 2, 4, 4, 0, 0, {1: 346, 2: 614, 3: 839}, "CRC"),
    BondData("Si-Si", "s/p", 3, 4, 4, 0, 0, {1: 310, 2: 434}, "CRC"),
    BondData("Ge-Ge", "s/p", 4, 4, 4, 0, 0, {1: 264, 2: 350}, "CRC"),
    BondData("Sn-Sn", "s/p", 5, 4, 4, 0, 0, {1: 187, 2: 235}, "CRC"),
    BondData("N-N", "s/p", 2, 5, 5, 1, 1, {1: 160, 2: 418, 3: 945}, "CRC"),
    BondData("P-P", "s/p", 3, 5, 5, 1, 1, {1: 201, 2: 489}, "CRC"),
    BondData("O-O", "s/p", 2, 6, 6, 2, 2, {1: 146, 2: 498}, "CRC"),
    BondData("S-S", "s/p", 3, 6, 6, 2, 2, {1: 266, 2: 425}, "CRC"),
    BondData("C-N", "s/p", 2, 4, 5, 0, 1, {1: 305, 2: 615, 3: 891}, "CRC"),
    BondData("C-O", "s/p", 2, 4, 6, 0, 2, {1: 358, 2: 745, 3: 1077}, "CRC"),
    BondData("N-O", "s/p", 2, 5, 6, 1, 2, {1: 201, 2: 607}, "CRC"),
    BondData("B-N", "s/p", 2, 3, 5, 0, 1, {1: 389, 2: 635}, "CRC"),
    BondData("B-O", "s/p", 2, 3, 6, 0, 2, {1: 536, 2: 806}, "CRC"),
    BondData("Si-O", "s/p", 3, 4, 6, 0, 2, {1: 452, 2: 640}, "CRC"),
    BondData("Si-N", "s/p", 3, 4, 5, 0, 1, {1: 355, 2: 470}, "CRC"),
    BondData("Al-O", "s/p", 3, 3, 6, 0, 2, {1: 502, 2: 740}, "CRC"),
    BondData("C-S", "s/p", 3, 4, 6, 0, 2, {1: 272, 2: 573}, "CRC"),
    BondData("C-P", "s/p", 3, 4, 5, 0, 1, {1: 264, 2: 513}, "CRC"),
    BondData("Ge-O", "s/p", 4, 4, 6, 0, 2, {1: 401, 2: 575}, "CRC"),
]

# =============================================================================
# NEW d-block data (to be filled from web search)
# valence_e for d-metals: Ti=4, V=5, Cr=6, Mn=7, Fe=8, Co=9, Ni=10, Cu=11, Zn=12
# LP set to -1 as placeholder (LP not defined for d-metals)
# =============================================================================
D_BLOCK = [
    # Will be populated after web search results arrive
]

def analyze_all(bonds):
    """Full analysis: compute α, test RE rule, correlations."""
    print("=" * 80)
    print("α-LAW ANALYSIS: s/p-block + d-block")
    print("=" * 80)

    # Compute α for all bonds
    results = []
    for b in bonds:
        a = b.alpha
        if a is not None:
            results.append((b, a))
            orders = sorted(b.energies.keys())
            energies_str = ", ".join(f"E{n}={b.energies[n]}" for n in orders)
            print(f"  {b.bond:8s} α={a:6.3f}  RE_min={b.RE_min:3d}  "
                  f"LP_min={min(b.LP_A, b.LP_B):2d}  [{energies_str}]  ({b.source})")

    if not results:
        print("No bonds with computable α!")
        return

    # Separate by block
    sp_results = [(b, a) for b, a in results if b.block == "s/p"]
    d_results = [(b, a) for b, a in results if b.block == "d"]

    print(f"\nTotal: {len(results)} bonds ({len(sp_results)} s/p + {len(d_results)} d)")

    # Test CLASSIC LP_min rule (s/p block only)
    sp = [(b, a) for b, a in results if b.block == "s/p"]
    if sp:
        print("\n" + "=" * 60)
        print("TEST 1: Classic LP_min rule (s/p block)")
        print("=" * 60)
        lp0_lt1 = sum(1 for b, a in sp if b.LP_min == 0 and a < 1)
        lp0_tot = sum(1 for b, a in sp if b.LP_min == 0)
        lp1_gt1 = sum(1 for b, a in sp if b.LP_min >= 1 and a > 1)
        lp1_tot = sum(1 for b, a in sp if b.LP_min >= 1)
        if lp0_tot:
            print(f"  LP_min=0 → α<1: {lp0_lt1}/{lp0_tot} = {100*lp0_lt1/lp0_tot:.0f}%")
        if lp1_tot:
            print(f"  LP_min≥1 → α>1: {lp1_gt1}/{lp1_tot} = {100*lp1_gt1/lp1_tot:.0f}%")

    # Test d-block RE rule
    db = [(b, a) for b, a in results if b.block == "d"]
    if db:
        print("\n" + "=" * 60)
        print("TEST 2: d-block RE rule")
        print("=" * 60)
        for b, a in db:
            status = "✓" if (b.RE_min > 2 and a > 1) or (b.RE_min <= 2 and a < 1) else "✗"
            print(f"  {b.bond:8s} RE_min={b.RE_min:2d}  α={a:.3f}  {status}")
        re_high_gt1 = sum(1 for b, a in db if b.RE_min > 2 and a > 1)
        re_high_tot = sum(1 for b, a in db if b.RE_min > 2)
        re_low_lt1 = sum(1 for b, a in db if b.RE_min <= 2 and a < 1)
        re_low_tot = sum(1 for b, a in db if b.RE_min <= 2)
        if re_high_tot:
            print(f"  RE_min>2 → α>1: {re_high_gt1}/{re_high_tot} = {100*re_high_gt1/re_high_tot:.0f}%")
        if re_low_tot:
            print(f"  RE_min≤2 → α<1: {re_low_lt1}/{re_low_tot} = {100*re_low_lt1/re_low_tot:.0f}%")

    # Test UNIFIED reserve metric
    print("\n" + "=" * 60)
    print("TEST 3: Unified reserve metric")
    print("=" * 60)
    alpha_vals = [a for b, a in results]
    reserve_vals = [b.reserve for b, a in results]

    res0_lt1 = sum(1 for b, a in results if b.reserve == 0 and a < 1)
    res0_tot = sum(1 for b, a in results if b.reserve == 0)
    res_pos_gt1 = sum(1 for b, a in results if b.reserve > 0 and a > 1)
    res_pos_tot = sum(1 for b, a in results if b.reserve > 0)
    if res0_tot:
        print(f"  reserve=0 → α<1: {res0_lt1}/{res0_tot} = {100*res0_lt1/res0_tot:.0f}%")
    if res_pos_tot:
        print(f"  reserve>0 → α>1: {res_pos_gt1}/{res_pos_tot} = {100*res_pos_gt1/res_pos_tot:.0f}%")

    # Mann-Whitney
    a_no_res = [a for b, a in results if b.reserve == 0]
    a_has_res = [a for b, a in results if b.reserve > 0]
    if len(a_no_res) >= 2 and len(a_has_res) >= 2:
        U, p = stats.mannwhitneyu(a_no_res, a_has_res, alternative='less')
        print(f"  Mann-Whitney (no reserve vs has reserve): U={U:.0f}, p={p:.6f}")

    # Spearman
    rho, p_rho = stats.spearmanr(reserve_vals, alpha_vals)
    print(f"  Spearman(reserve, α): ρ={rho:.3f}, p={p_rho:.6f}")

    res_period = [b.reserve / b.period for b, a in results]
    rho2, p2 = stats.spearmanr(res_period, alpha_vals)
    print(f"  Spearman(reserve/period, α): ρ={rho2:.3f}, p={p2:.6f}")

    # Morse anharmonicity correlation (if available)
    xe_pairs = [(b.x_e, a) for b, a in results if b.x_e is not None]
    if len(xe_pairs) >= 3:
        xe_vals = [x for x, a in xe_pairs]
        a_vals = [a for x, a in xe_pairs]
        rho_xe, p_xe = stats.spearmanr(xe_vals, a_vals)
        print(f"\n  Spearman(x_e, α): ρ={rho_xe:.3f}, p={p_xe:.6f}")
        r_xe, p_r = stats.pearsonr(xe_vals, a_vals)
        print(f"  Pearson(x_e, α): r={r_xe:.3f}, p={p_r:.6f}")

    return results


if __name__ == "__main__":
    # Run with existing s/p data first
    print("\n>>> Phase 1: s/p-block only (existing data)")
    analyze_all(SP_BLOCK)

    if D_BLOCK:
        print("\n\n>>> Phase 2: s/p + d-block (expanded)")
        analyze_all(SP_BLOCK + D_BLOCK)
