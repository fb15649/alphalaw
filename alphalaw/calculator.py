"""
Core α-law calculator.
E(n) = E₁ × n^α — Reserve Law of Chemical Bonding.
"""
import math
from typing import Optional
from .data import BondData, get_bond_data, list_all_bonds, ATOMIC_ALPHAS


def get_bond(elem1: str, elem2: str) -> Optional[BondData]:
    """Look up bond data for an element pair."""
    return get_bond_data(elem1, elem2)


def compute_alpha(energies: dict[int, float]) -> Optional[float]:
    """Compute α from a dict of {bond_order: energy_kJ_mol}."""
    orders = sorted(energies.keys())
    if len(orders) < 2:
        return None
    E1 = energies[orders[0]]
    if E1 <= 0:
        return None
    if len(orders) == 2:
        n1, n2 = orders
        return math.log(energies[n2] / energies[n1]) / math.log(n2 / n1)
    from scipy import stats
    log_n = [math.log(n / orders[0]) for n in orders[1:]]
    log_ratio = [math.log(energies[n] / E1) for n in orders[1:]]
    slope, _, _, _, _ = stats.linregress(log_n, log_ratio)
    return slope


def morse_predict_alpha(omega_e: float, omega_e_xe: float, LP: int) -> float:
    """
    Predict α from Morse anharmonicity and lone pair count.
    Two-level model:
      LP=0: α = 0.186 + 13.1 × 3β  (R²=0.968)
      LP≥1: α = 0.182 + 39.3 × 3β  (R²=0.572)
    where 3β = 6 × x_e, x_e = ω_eχ_e / ω_e
    """
    x_e = omega_e_xe / omega_e
    beta3 = 6 * x_e
    if LP == 0:
        return 0.186 + 13.085 * beta3
    return 0.182 + 39.284 * beta3


def predict(elem1: str, elem2: str) -> dict:
    """
    Full prediction for an element pair.
    Returns dict with alpha, reserve status, bond preference, etc.
    """
    bond = get_bond(elem1, elem2)
    if bond is None:
        return {"error": f"No data for {elem1}-{elem2}. Use --list to see available bonds."}

    alpha = bond.alpha
    result = {
        "bond": bond.bond,
        "block": bond.block,
        "alpha": alpha,
        "LP_min": bond.LP_min,
        "has_reserve": bond.has_reserve,
        "energies": bond.energies,
        "source": bond.source,
    }

    if alpha is None:
        result["prediction"] = "Insufficient data to compute α"
        return result

    if bond.block == "d":
        if alpha < 0.7:
            result["prediction"] = "Strong diminishing returns — δ-bonds add little energy"
        elif alpha < 1.0:
            result["prediction"] = "Moderate diminishing returns — higher bond orders progressively weaker"
        else:
            result["prediction"] = "Unusual: increasing returns in d-block"
        result["note"] = "d-electrons form δ-bonds with poor orbital overlap"
    else:
        if alpha < 0.6:
            result["prediction"] = "Strong diminishing returns — prefers many single bonds (frameworks)"
        elif alpha < 1.0:
            result["prediction"] = "Diminishing returns — single bonds favored over multiple"
        elif alpha < 1.5:
            result["prediction"] = "Moderate synergy — double/triple bonds viable"
        else:
            result["prediction"] = "Strong synergy — prefers few strong multiple bonds"

        if bond.LP_min == 0:
            result["note"] = "LP=0: no recruitable reserve → α < 1 expected"
        elif bond.LP_min >= 1:
            result["note"] = f"LP={bond.LP_min}: has reserve → α > 1 expected"

    if bond.x_e is not None:
        result["x_e"] = bond.x_e
        result["morse_predicted_alpha"] = morse_predict_alpha(
            bond.omega_e, bond.omega_e_xe, max(0, bond.LP_min)
        )

    return result


def classify_reserve(LP: int, block: str = "s/p") -> str:
    """Classify reserve type."""
    if block == "d":
        return "anti-bonding (δ-overhead, not recruitable)"
    if LP == 0:
        return "none (all electrons in bonds)"
    if LP == 1:
        return "moderate (one lone pair available for π)"
    return f"high ({LP} lone pairs)"
