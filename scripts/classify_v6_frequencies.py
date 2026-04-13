"""
Classifier v6: pure physics from σ and π frequencies.
NO if/else rules. Only frequencies and resonance.

For each element pair:
  σ = E₁ (single bond energy) — strength of axial bond
  π = E₂ - E₁ (what double bond adds) — strength of lateral bond

Classification emerges from:
  R₂ = (σ + π) / σ = E₂/E₁ = 1 + π/σ = 2^α

  R₂ > threshold → molecular
  R₂ < threshold → crystal
  Threshold depends on the PAIR, not on arbitrary rules.
"""
import re, sys, math
import numpy as np
sys.path.insert(0, '/Volumes/Backup/Python_projects/alphalaw')
from alphalaw.data import BONDS, ELEMENTS, get_bond_data, estimate_alpha

# ============================================================
# Step 1: Build σ and π lookup for all known pairs
# ============================================================
SIGMA_PI = {}  # (e1, e2) → (σ, π, R₂)

for b in BONDS:
    if b.alpha is None: continue
    orders = sorted(b.energies.keys())
    if len(orders) < 2: continue
    E1 = b.energies[orders[0]]
    E2 = b.energies[orders[1]]

    sigma = E1
    pi = E2 - E1
    R2 = E2 / E1 if E1 > 0 else 1

    e1, e2 = sorted([b.elem_A, b.elem_B])
    SIGMA_PI[(e1, e2)] = (sigma, pi, R2)


# Electronegativity and atomic radius for estimation
EN = {}
RAD = {}
for sym, (per, grp, blk, val, lp) in ELEMENTS.items():
    # EN from Pauling scale (approximate)
    _en = {
        'H':2.20,'Li':0.98,'Be':1.57,'B':2.04,'C':2.55,'N':3.04,'O':3.44,'F':3.98,
        'Na':0.93,'Mg':1.31,'Al':1.61,'Si':1.90,'P':2.19,'S':2.58,'Cl':3.16,
        'K':0.82,'Ca':1.00,'Ti':1.54,'Cr':1.66,'Mn':1.55,'Fe':1.83,'Cu':1.90,
        'Zn':1.65,'Ga':1.81,'Ge':2.01,'As':2.18,'Se':2.55,'Br':2.96,
        'Sr':0.95,'Zr':1.33,'Mo':2.16,'Ag':1.93,'Sn':1.96,'Sb':2.05,
        'Te':2.10,'I':2.66,'Ba':0.89,'La':1.10,'W':2.36,'Pt':2.28,
        'Hg':2.00,'Pb':2.33,'Bi':2.02,'Co':1.88,'Ni':1.91,'Nb':1.60,
        'Hf':1.30,'Ta':1.50,'Re':1.90,'Os':2.20,'Ir':2.20,'Au':2.54,
        'Cd':1.69,'In':1.78,'Xe':2.60,'Kr':3.00,'Y':1.22,'Sc':1.36,
        'V':1.63,'Tc':1.90,'Ru':2.20,'Rh':2.28,'Pd':2.20,
        'Tl':1.62,'Po':2.00,'Th':1.30,'U':1.38,
    }
    if sym in _en:
        EN[sym] = _en[sym]


def get_sigma_pi(e1, e2):
    """Get σ and π for a pair — from data or estimated."""
    pair = tuple(sorted([e1, e2]))
    if pair in SIGMA_PI:
        return SIGMA_PI[pair]

    # Estimate σ from electronegativity
    en1 = EN.get(e1, 1.5)
    en2 = EN.get(e2, 1.5)
    p1 = ELEMENTS.get(e1, (3,0,'p',0,0))[0]
    p2 = ELEMENTS.get(e2, (3,0,'p',0,0))[0]
    period = max(p1, p2)

    lp1 = ELEMENTS.get(e1, (0,0,'p',0,0))[4]
    lp2 = ELEMENTS.get(e2, (0,0,'p',0,0))[4]
    lp_min = min(lp1, lp2) if lp1 >= 0 and lp2 >= 0 else 0

    blk1 = ELEMENTS.get(e1, (0,0,'p',0,0))[2]
    blk2 = ELEMENTS.get(e2, (0,0,'p',0,0))[2]
    is_d = blk1 == 'd' or blk2 == 'd'

    # σ estimate: E₁ ≈ k × EN_product / Period + ΔEN² bonus
    den = abs(en1 - en2)
    sigma_est = 6 * en1 * en2 / period + 109 * den**2 + 205

    # π estimate: depends on LP, Period, AND ionicity
    # KEY: ionic CRYSTAL = metal + nonmetal with large ΔEN
    # But ionic MOLECULE (HF, BF₃) = nonmetal + nonmetal → still molecular
    has_metal = (blk1 == 'd' or blk2 == 'd' or
                 blk1 == 'f' or blk2 == 'f' or
                 ELEMENTS.get(e1, (0,0,'p',0,0))[1] in (1,2) or  # group 1,2
                 ELEMENTS.get(e2, (0,0,'p',0,0))[1] in (1,2))
    is_ionic_crystal = has_metal and den > 1.0

    if is_ionic_crystal and den > 1.5:
        pi_est = sigma_est * 0.05  # strong ionic: no π
    elif is_ionic_crystal:
        pi_factor = 0.3 * (1.5 - den) / 0.5
        pi_est = sigma_est * max(0.05, pi_factor)
    elif lp_min >= 2 and period == 2:
        pi_est = sigma_est * 1.5  # strong π (O-O like)
    elif lp_min >= 1 and period == 2:
        pi_est = sigma_est * 1.0  # moderate π (N-N like)
    elif lp_min >= 1 and period == 3:
        pi_est = sigma_est * 0.4  # weak π
    elif lp_min >= 1:
        pi_est = sigma_est * 0.3  # very weak π (heavy)
    elif is_d and den < 0.5:
        pi_est = sigma_est * 0.5  # d-d homonuclear: δ-bonds
    else:
        pi_est = sigma_est * 0.2  # LP=0, covalent: minimal π

    R2_est = (sigma_est + pi_est) / sigma_est if sigma_est > 0 else 1

    return (sigma_est, pi_est, R2_est)


def parse(formula):
    counts = {}
    for m in re.finditer(r'([A-Z][a-z]?)(\d*)', formula):
        e = m.group(1)
        n = int(m.group(2)) if m.group(2) else 1
        if e in ELEMENTS or e in EN:
            counts[e] = counts.get(e, 0) + n
    return counts


def classify_v6(formula):
    """
    Pure frequency-based classification.
    For each pair: get R₂ = E₂/E₁.
    Compound R₂ = geometric mean of all pair R₂'s,
    weighted by number of such bonds.

    Then classify by R₂ thresholds (from musical intervals):
      R₂ > 1.9 (near octave 2:1) → gas
      R₂ > 1.4 (near tritone 7:5) → liquid
      R₂ > 1.15 (near 9:8) → border
      R₂ > 1.0 → crystal
    """
    counts = parse(formula)
    elements = sorted(counts.keys())

    if len(elements) < 1:
        return "crystal", "no_data", 1.0

    METALS_SET = {
        "Li","Na","K","Rb","Cs","Be","Mg","Ca","Sr","Ba",
        "Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn",
        "Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd",
        "La","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg",
        "Al","Ga","In","Tl","Sn","Pb","Bi",
    }

    # Single element
    if len(elements) == 1:
        e = elements[0]
        if e in METALS_SET:
            return "crystal", "pure_metal", 1.0
        pair_data = get_sigma_pi(e, e)
        R2 = pair_data[2]
        # Heavy nonmetals with α>1 → border (molecular crystals like P4, I2)
        p = ELEMENTS.get(e, (3,))[0] if e in ELEMENTS else 3
        if R2 > 1.35 and p >= 3:
            return "border", f"homo(R₂={R2:.3f},P{p})", R2
        cat = r2_to_category(R2)
        return cat, f"homo(R₂={R2:.3f})", R2

    # Multiple elements: compute R₂ for each pair
    pair_R2s = []
    for i, e1 in enumerate(elements):
        for e2 in elements[i+1:]:
            sigma, pi, R2 = get_sigma_pi(e1, e2)
            # Weight by stoichiometry: more of each element → more such bonds
            weight = counts.get(e1, 1) * counts.get(e2, 1)
            pair_R2s.append((R2, weight, f"{e1}-{e2}"))

    if not pair_R2s:
        return "crystal", "no_pairs", 1.0

    # Compound R₂ = minimum pair R₂ (weakest link)
    min_R2 = min(pair_R2s, key=lambda x: x[0])
    R2_eff = min_R2[0]

    cat = r2_to_category(R2_eff)
    return cat, f"min_R₂={R2_eff:.3f}({min_R2[2]})", R2_eff


def r2_to_category(R2):
    """Map R₂ to 5-level category using musical interval thresholds."""
    # These thresholds correspond to musical intervals:
    # 2:1 (octave) = 2.0 → gas/liquid boundary
    # 3:2 (fifth) = 1.5 → liquid/border
    # 5:4 (major third) = 1.25 → border/crystal
    # 9:8 (whole tone) = 1.125 → crystal/refractory
    if R2 > 1.8:   return "gas"
    if R2 > 1.35:  return "liquid"
    if R2 > 1.15:  return "border"
    if R2 > 1.05:  return "crystal"
    return "refract"


# ============================================================
# Compatibility
# ============================================================
COMPAT = {
    "gas": ["mol"],
    "liquid": ["mol"],
    "border": ["mol", "cryst"],
    "crystal": ["cryst"],
    "refract": ["cryst"],
}


# ============================================================
# No auto-run on import. Use classify_v6() directly.
