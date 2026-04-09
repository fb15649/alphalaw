"""
Bond data for α-law calculations.
Sources: CRC Handbook 97th ed., Huber & Herzberg (1979), Cotton & Murillo (2005),
Chen & Manz (2019) RSC Advances, Morse (2018) Acc. Chem. Res.
"""
from dataclasses import dataclass, field
from typing import Optional
import math


@dataclass
class BondData:
    bond: str
    block: str               # "s/p" or "d"
    period: int              # period of heavier atom
    elem_A: str
    elem_B: str
    valence_e_A: int
    valence_e_B: int
    LP_A: int                # lone pairs (-1 for d-block)
    LP_B: int
    energies: dict           # {bond_order: energy_kJ_mol}
    source: str
    omega_e: Optional[float] = None      # cm⁻¹
    omega_e_xe: Optional[float] = None   # cm⁻¹

    @property
    def alpha(self) -> Optional[float]:
        """Simple α: OLS forced through origin. Used for CLASSIFICATION.
        E(n) = E₁ × n^α. α>1 = synergy, α<1 = diminishing returns."""
        orders = sorted(self.energies.keys())
        if len(orders) < 2:
            return None
        E1 = self.energies[orders[0]]
        if E1 <= 0:
            return None
        if len(orders) == 2:
            n1, n2 = orders
            if self.energies[n1] <= 0 or self.energies[n2] <= 0:
                return None
            return math.log(self.energies[n2] / self.energies[n1]) / math.log(n2 / n1)
        x = [math.log(n / orders[0]) for n in orders[1:]]
        y = [math.log(self.energies[n] / E1) for n in orders[1:]]
        return sum(xi * yi for xi, yi in zip(x, y)) / sum(xi * xi for xi in x)

    @property
    def alpha_beta(self) -> tuple[Optional[float], float]:
        """(α, β) for 2-param model: E = E₁ × n^(α + β·ln(n)).
        Used for PREDICTION. More accurate than simple α."""
        orders = sorted(self.energies.keys())
        if len(orders) < 2:
            return None, 0.0
        E1 = self.energies[orders[0]]
        if E1 <= 0:
            return None, 0.0
        if len(orders) <= 2:
            return self.alpha, 0.0
        import numpy as np
        x1 = np.array([math.log(n / orders[0]) for n in orders[1:]])
        x2 = x1 ** 2
        y = np.array([math.log(self.energies[n] / E1) for n in orders[1:]])
        X = np.column_stack([x1, x2])
        coeffs = np.linalg.lstsq(X, y, rcond=None)[0]
        return float(coeffs[0]), float(coeffs[1])

    @property
    def beta(self) -> float:
        """β curvature: >0 = accelerating synergy, <0 = decelerating."""
        return self.alpha_beta[1]

    def predict_energy(self, n: float) -> Optional[float]:
        """Predict E(n) using 2-parameter model (high accuracy)."""
        a, b = self.alpha_beta
        if a is None:
            return None
        orders = sorted(self.energies.keys())
        E1 = self.energies[orders[0]]
        ln_n = math.log(n / orders[0]) if n > orders[0] else 0
        return E1 * math.exp(a * ln_n + b * ln_n ** 2)

    @property
    def LP_min(self) -> int:
        if self.LP_A < 0 or self.LP_B < 0:
            return -1
        return min(self.LP_A, self.LP_B)

    @property
    def x_e(self) -> Optional[float]:
        if self.omega_e and self.omega_e_xe:
            return self.omega_e_xe / self.omega_e
        return None

    @property
    def has_reserve(self) -> Optional[bool]:
        if self.block == "d":
            return False  # d-electrons are anti-bonding overhead
        return self.LP_min >= 1


def _b(bond, block, period, eA, eB, vA, vB, lpA, lpB, energies, src,
       we=None, wexe=None):
    return BondData(bond, block, period, eA, eB, vA, vB, lpA, lpB,
                    energies, src, we, wexe)


# ============================================================
# s/p-block bonds (19 entries)
# ============================================================
SP_BONDS = [
    _b("C-C",   "s/p", 2, "C",  "C",  4, 4, 0, 0, {1:346, 2:614, 3:839},    "CRC", 1854.7, 13.34),
    _b("Si-Si", "s/p", 3, "Si", "Si", 4, 4, 0, 0, {1:310, 2:434},            "CRC", 510.9, 2.02),
    _b("Ge-Ge", "s/p", 4, "Ge", "Ge", 4, 4, 0, 0, {1:264, 2:350},            "CRC", 286.0, 0.96),
    _b("Sn-Sn", "s/p", 5, "Sn", "Sn", 4, 4, 0, 0, {1:187, 2:235},           "CRC", 186.2, 0.26),
    _b("N-N",   "s/p", 2, "N",  "N",  5, 5, 1, 1, {1:160, 2:418, 3:945},     "CRC", 2358.6, 14.32),
    _b("P-P",   "s/p", 3, "P",  "P",  5, 5, 1, 1, {1:201, 2:489},            "CRC", 780.8, 2.84),
    _b("O-O",   "s/p", 2, "O",  "O",  6, 6, 2, 2, {1:146, 2:498},            "CRC", 1580.2, 12.07),
    _b("S-S",   "s/p", 3, "S",  "S",  6, 6, 2, 2, {1:266, 2:425},            "CRC", 725.7, 2.84),
    _b("C-N",   "s/p", 2, "C",  "N",  4, 5, 0, 1, {1:305, 2:615, 3:891},     "CRC"),
    _b("C-O",   "s/p", 2, "C",  "O",  4, 6, 0, 2, {1:358, 2:745, 3:1077},    "CRC"),
    _b("N-O",   "s/p", 2, "N",  "O",  5, 6, 1, 2, {1:201, 2:607},            "CRC"),
    _b("B-N",   "s/p", 2, "B",  "N",  3, 5, 0, 1, {1:389, 2:635},            "CRC"),
    _b("B-O",   "s/p", 2, "B",  "O",  3, 6, 0, 2, {1:536, 2:806},            "CRC"),
    _b("Si-O",  "s/p", 3, "Si", "O",  4, 6, 0, 2, {1:452, 2:640},            "CRC"),
    _b("Si-N",  "s/p", 3, "Si", "N",  4, 5, 0, 1, {1:355, 2:470},            "CRC"),
    _b("Al-O",  "s/p", 3, "Al", "O",  3, 6, 0, 2, {1:502, 2:740},            "CRC"),
    _b("C-S",   "s/p", 3, "C",  "S",  4, 6, 0, 2, {1:272, 2:573},            "CRC"),
    _b("C-P",   "s/p", 3, "C",  "P",  4, 5, 0, 1, {1:264, 2:513},            "CRC"),
    _b("Ge-O",  "s/p", 4, "Ge", "O",  4, 6, 0, 2, {1:401, 2:575},            "CRC"),
    _b("As-As", "s/p", 4, "As", "As", 5, 5, 1, 1, {1:146, 2:382},            "CRC"),
    _b("Se-Se", "s/p", 4, "Se", "Se", 6, 6, 2, 2, {1:172, 2:272},            "CRC"),
    _b("Te-Te", "s/p", 5, "Te", "Te", 6, 6, 2, 2, {1:138, 2:222},            "CRC"),
    _b("B-C",   "s/p", 2, "B",  "C",  3, 4, 0, 0, {1:372, 2:590},            "CRC"),
    _b("N-S",   "s/p", 3, "N",  "S",  5, 6, 1, 2, {1:159, 2:467},            "CRC"),
    _b("P-O",   "s/p", 3, "P",  "O",  5, 6, 1, 2, {1:335, 2:544},            "CRC"),
    _b("S-O",   "s/p", 3, "S",  "O",  6, 6, 2, 2, {1:265, 2:522},            "CRC"),
    _b("P-S",   "s/p", 3, "P",  "S",  5, 6, 1, 2, {1:230, 2:335},            "CRC"),
    _b("F-F",   "s/p", 2, "F",  "F",  7, 7, 3, 3, {1:158},                   "CRC", 916.6, 11.24),
    _b("Cl-Cl", "s/p", 3, "Cl", "Cl", 7, 7, 3, 3, {1:242},                   "CRC", 559.7, 2.67),
    _b("Br-Br", "s/p", 4, "Br", "Br", 7, 7, 3, 3, {1:193},                   "CRC"),
    _b("I-I",   "s/p", 5, "I",  "I",  7, 7, 3, 3, {1:151},                   "CRC"),
    _b("Ti-O",  "d",   4, "Ti", "O",  4, 6,-1, 2, {1:672},                   "CRC"),
    _b("Fe-C",  "d",   4, "Fe", "C",  8, 4,-1, 0, {1:394},                   "CRC; Brugh & Morse 2002"),
    _b("W-C",   "d",   6, "W",  "C",  6, 4,-1, 0, {1:639},                   "CRC"),
]

# ============================================================
# d-block bonds (4 entries with multiple bond orders)
# ============================================================
D_BONDS = [
    _b("Cr-Cr", "d", 4, "Cr", "Cr", 6, 6, -1, -1,
       {1:70, 4:152}, "Cotton; CRC", 480.6, 14.1),
    _b("Mo-Mo", "d", 5, "Mo", "Mo", 6, 6, -1, -1,
       {1:140, 2:250, 3:350, 4:405, 5:420, 6:435},
       "Cotton & Murillo 2005; Simard 1998", 477.1, 1.5),
    _b("W-W",   "d", 6, "W",  "W",  6, 6, -1, -1,
       {1:160, 3:500, 4:570, 6:666}, "CRC; Cotton", 336.8, 0.85),
    _b("Re-Re", "d", 6, "Re", "Re", 7, 7, -1, -1,
       {1:120, 4:432}, "Bergman 1984; CRC", 337.0, None),
]

BONDS = SP_BONDS + D_BONDS

# Quick lookup: element pair → BondData
_BOND_INDEX: dict[tuple[str, str], BondData] = {}
for b in BONDS:
    _BOND_INDEX[(b.elem_A, b.elem_B)] = b
    _BOND_INDEX[(b.elem_B, b.elem_A)] = b

# Homonuclear α values for quick access
ATOMIC_ALPHAS = {b.bond: b.alpha for b in BONDS if b.alpha is not None}


# ============================================================
# Element properties for predictive mode
# (symbol, period, group, block, valence_e, LP)
# LP = lone pairs for s/p block; -1 for d/f block
# ============================================================
ELEMENTS = {
    "H":  (1,  1, "s",   1, 0),
    "He": (1, 18, "s",   2, 1),
    "Li": (2,  1, "s",   1, 0),
    "Be": (2,  2, "s",   2, 0),
    "B":  (2, 13, "s/p", 3, 0),
    "C":  (2, 14, "s/p", 4, 0),
    "N":  (2, 15, "s/p", 5, 1),
    "O":  (2, 16, "s/p", 6, 2),
    "F":  (2, 17, "s/p", 7, 3),
    "Ne": (2, 18, "s/p", 8, 4),
    "Na": (3,  1, "s",   1, 0),
    "Mg": (3,  2, "s",   2, 0),
    "Al": (3, 13, "s/p", 3, 0),
    "Si": (3, 14, "s/p", 4, 0),
    "P":  (3, 15, "s/p", 5, 1),
    "S":  (3, 16, "s/p", 6, 2),
    "Cl": (3, 17, "s/p", 7, 3),
    "Ar": (3, 18, "s/p", 8, 4),
    "K":  (4,  1, "s",   1, 0),
    "Ca": (4,  2, "s",   2, 0),
    "Sc": (4,  3, "d",   3,-1),
    "Ti": (4,  4, "d",   4,-1),
    "V":  (4,  5, "d",   5,-1),
    "Cr": (4,  6, "d",   6,-1),
    "Mn": (4,  7, "d",   7,-1),
    "Fe": (4,  8, "d",   8,-1),
    "Co": (4,  9, "d",   9,-1),
    "Ni": (4, 10, "d",  10,-1),
    "Cu": (4, 11, "d",  11,-1),
    "Zn": (4, 12, "d",  12,-1),
    "Ga": (4, 13, "s/p", 3, 0),
    "Ge": (4, 14, "s/p", 4, 0),
    "As": (4, 15, "s/p", 5, 1),
    "Se": (4, 16, "s/p", 6, 2),
    "Br": (4, 17, "s/p", 7, 3),
    "Kr": (4, 18, "s/p", 8, 4),
    "Rb": (5,  1, "s",   1, 0),
    "Sr": (5,  2, "s",   2, 0),
    "Y":  (5,  3, "d",   3,-1),
    "Zr": (5,  4, "d",   4,-1),
    "Nb": (5,  5, "d",   5,-1),
    "Mo": (5,  6, "d",   6,-1),
    "Ru": (5,  8, "d",   8,-1),
    "Rh": (5,  9, "d",   9,-1),
    "Pd": (5, 10, "d",  10,-1),
    "Ag": (5, 11, "d",  11,-1),
    "Cd": (5, 12, "d",  12,-1),
    "In": (5, 13, "s/p", 3, 0),
    "Sn": (5, 14, "s/p", 4, 0),
    "Sb": (5, 15, "s/p", 5, 1),
    "Te": (5, 16, "s/p", 6, 2),
    "I":  (5, 17, "s/p", 7, 3),
    "Xe": (5, 18, "s/p", 8, 4),
    "Cs": (6,  1, "s",   1, 0),
    "Ba": (6,  2, "s",   2, 0),
    "La": (6,  3, "d",   3,-1),
    "Hf": (6,  4, "d",   4,-1),
    "Ta": (6,  5, "d",   5,-1),
    "W":  (6,  6, "d",   6,-1),
    "Re": (6,  7, "d",   7,-1),
    "Os": (6,  8, "d",   8,-1),
    "Ir": (6,  9, "d",   9,-1),
    "Pt": (6, 10, "d",  10,-1),
    "Au": (6, 11, "d",  11,-1),
    "Hg": (6, 12, "d",  12,-1),
    "Tl": (6, 13, "s/p", 3, 0),
    "Pb": (6, 14, "s/p", 4, 0),
    "Bi": (6, 15, "s/p", 5, 1),
    "Po": (6, 16, "s/p", 6, 2),
    "U":  (7,  3, "f",   3,-1),
    "Th": (7,  4, "f",   4,-1),
}


def estimate_alpha(elem1: str, elem2: str) -> Optional[dict]:
    """Predict α for ANY element pair using LP + period heuristic.
    Returns dict with estimated alpha, confidence, and reasoning."""
    e1 = elem1.capitalize()
    e2 = elem2.capitalize()
    if e1 not in ELEMENTS or e2 not in ELEMENTS:
        return None

    p1, g1, blk1, v1, lp1 = ELEMENTS[e1]
    p2, g2, blk2, v2, lp2 = ELEMENTS[e2]

    period = max(p1, p2)
    lp_min = min(lp1, lp2) if lp1 >= 0 and lp2 >= 0 else -1
    is_d = blk1 == "d" or blk2 == "d"
    is_f = blk1 == "f" or blk2 == "f"

    # Heuristic estimation based on validated patterns
    if is_f:
        alpha_est = 0.5
        conf = "low"
        reason = "f-block: very limited data, rough estimate"
    elif is_d:
        if period <= 4:
            alpha_est = 0.65
        elif period <= 5:
            alpha_est = 0.72
        else:
            alpha_est = 0.85
        conf = "medium"
        reason = "d-block: δ-bonds have poor overlap → diminishing returns"
    elif lp_min == 0:
        # LP=0 → α < 1, scaled by period
        alpha_map = {2: 0.82, 3: 0.48, 4: 0.41, 5: 0.33, 6: 0.28}
        alpha_est = alpha_map.get(period, 0.35)
        conf = "high"
        reason = f"LP=0, Period {period}: no reserve → diminishing returns"
    elif lp_min >= 1 and period == 2:
        alpha_map = {1: 1.55, 2: 1.77}
        alpha_est = alpha_map.get(lp_min, 1.6)
        conf = "high"
        reason = f"LP={lp_min}, Period 2: small atoms, good π-overlap → synergy"
    elif lp_min >= 1 and period == 3:
        alpha_est = 1.1 if lp_min == 1 else 0.7
        conf = "medium"
        reason = f"LP={lp_min}, Period 3: moderate π-overlap"
    elif lp_min == 1 and period in (4, 5):
        # Group 15 (As, Sb): retain decent π, like P-P (1.28)
        alpha_est = 1.0 if period == 5 else 0.9
        conf = "medium"
        reason = f"LP=1, Period {period}: Group 15 retains some π-overlap"
    elif lp_min >= 2 and period >= 4:
        alpha_est = 0.65
        conf = "medium"
        reason = f"LP={lp_min}, Period {period}: poor overlap despite LP"
    elif lp_min >= 1 and period >= 6:
        alpha_est = 0.65
        conf = "medium"
        reason = f"LP={lp_min}, Period {period}: very poor overlap"
    else:
        alpha_est = 0.7
        conf = "low"
        reason = "insufficient pattern data"

    return {
        "bond": f"{e1}-{e2}",
        "alpha_est": alpha_est,
        "confidence": conf,
        "reason": reason,
        "lp_min": lp_min,
        "period": period,
        "block": "d" if is_d else ("f" if is_f else "s/p"),
        "source": "estimated (LP + period heuristic)",
    }


def get_bond_data(elem1: str, elem2: str) -> Optional[BondData]:
    e1 = elem1.capitalize()
    e2 = elem2.capitalize()
    return _BOND_INDEX.get((e1, e2))


def list_all_bonds() -> list[BondData]:
    return list(BONDS)
