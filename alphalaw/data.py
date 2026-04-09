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
        orders = sorted(self.energies.keys())
        if len(orders) < 2:
            return None
        E1 = self.energies[orders[0]]
        if E1 <= 0:
            return None
        if len(orders) == 2:
            n1, n2 = orders
            E_n1, E_n2 = self.energies[n1], self.energies[n2]
            if E_n1 <= 0 or E_n2 <= 0:
                return None
            return math.log(E_n2 / E_n1) / math.log(n2 / n1)
        from scipy import stats
        log_n = [math.log(n / orders[0]) for n in orders[1:]]
        log_ratio = [math.log(self.energies[n] / E1) for n in orders[1:]]
        slope, _, _, _, _ = stats.linregress(log_n, log_ratio)
        return slope

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


def get_bond_data(elem1: str, elem2: str) -> Optional[BondData]:
    e1 = elem1.capitalize()
    e2 = elem2.capitalize()
    return _BOND_INDEX.get((e1, e2))


def list_all_bonds() -> list[BondData]:
    return list(BONDS)
