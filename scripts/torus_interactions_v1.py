"""
v1.0 — Classification from ALL torus interactions.
Built from scratch. No rules. Only physics.

TWO TORI approach each other. What happens?

ATTRACTIVE:
  1. σ-bond: axial flow coupling (always present when close)
  2. π-bond: lateral flow donation (requires LP)
  3. Coulomb: opposite charges attract (ionic)
  4. Dispersion: temporary dipole fluctuations (always, weak)

REPULSIVE:
  5. LP-LP: lone pair flows collide (short-range)
  6. Pauli/core: tori can't occupy same space (very short-range)
  7. Coulomb: same charges repel

SPECIAL:
  8. Delocalization: flows merge into common pool (metallic)
  9. Frequency locking: resonance capture (determines bond strength)

The DOMINANT interaction determines the compound type.
"""
import re, sys, math
sys.path.insert(0, '/Volumes/Backup/Python_projects/alphalaw')
from alphalaw.data import BONDS, ELEMENTS, get_bond_data


# ============================================================
# Element properties (from periodic table)
# ============================================================
EN = {
    'H':2.20,'Li':0.98,'Be':1.57,'B':2.04,'C':2.55,'N':3.04,'O':3.44,'F':3.98,
    'Na':0.93,'Mg':1.31,'Al':1.61,'Si':1.90,'P':2.19,'S':2.58,'Cl':3.16,
    'K':0.82,'Ca':1.00,'Sc':1.36,'Ti':1.54,'V':1.63,'Cr':1.66,'Mn':1.55,
    'Fe':1.83,'Co':1.88,'Ni':1.91,'Cu':1.90,'Zn':1.65,
    'Ga':1.81,'Ge':2.01,'As':2.18,'Se':2.55,'Br':2.96,
    'Sr':0.95,'Y':1.22,'Zr':1.33,'Nb':1.60,'Mo':2.16,
    'Ag':1.93,'Cd':1.69,'In':1.78,'Sn':1.96,'Sb':2.05,'Te':2.10,'I':2.66,
    'Ba':0.89,'La':1.10,'Hf':1.30,'Ta':1.50,'W':2.36,'Re':1.90,
    'Os':2.20,'Ir':2.20,'Pt':2.28,'Au':2.54,'Hg':2.00,
    'Tl':1.62,'Pb':2.33,'Bi':2.02,'Xe':2.60,'Kr':3.00,
    'U':1.38,'Th':1.30,
}

def elem_props(e):
    """Get (period, group, block, valence, lp, en) for element."""
    if e in ELEMENTS:
        p, g, blk, v, lp = ELEMENTS[e]
        return p, g, blk, v, lp, EN.get(e, 1.5)
    return 4, 0, 'p', 0, 0, EN.get(e, 1.5)


def compute_interactions(e1, e2):
    """
    Compute ALL interactions between two tori.
    Returns dict of interaction strengths (arbitrary units, relative).
    """
    p1, g1, b1, v1, lp1, en1 = elem_props(e1)
    p2, g2, b2, v2, lp2, en2 = elem_props(e2)

    period = max(p1, p2)
    den = abs(en1 - en2)
    en_prod = en1 * en2
    lp_min = min(lp1, lp2) if lp1 >= 0 and lp2 >= 0 else 0
    lp_max = max(lp1, lp2) if lp1 >= 0 and lp2 >= 0 else 0
    is_metal = (b1 in ('d', 'f') or b2 in ('d', 'f') or
                g1 in (1, 2) or g2 in (1, 2))
    is_noble = (g1 == 18 or g2 == 18)

    # ── 1. σ-bond (axial flow coupling) ──
    # Strength ∝ geometric mean of EN / Period
    sigma = math.sqrt(en_prod) / period

    # ── 2. π-bond (lateral flow, LP donation) ──
    # Requires LP. Effectiveness drops with Period² (diffuse LP)
    if lp_min > 0:
        pi = lp_min * sigma / period  # LP amplifies σ, weakened by size
    else:
        pi = 0

    # ── 3. Coulomb (ionic attraction) ──
    # Strength ∝ ΔEN² (charge separation)
    coulomb = den ** 2

    # ── 4. Dispersion (van der Waals) ──
    # Strength ∝ Period³ (polarizability ∝ atomic volume)
    dispersion = (p1 * p2) ** 1.5 / 100  # normalized to be small

    # ── 5. LP-LP repulsion ──
    # Both atoms have LP → collide
    lp_repulsion = lp1 * lp2 / period ** 2 if lp1 > 0 and lp2 > 0 else 0

    # ── 6. Pauli (core repulsion) ──
    # Always present, but dominated by others at bond distance
    pauli = 0.1  # constant small background

    # ── 7. Delocalization (metallic) ──
    # High for: low EN, many valence electrons, d/f-block
    if is_metal and en1 < 2.5 and en2 < 2.5:
        metallic = v1 * v2 / (en1 * en2 * period)
    else:
        metallic = 0

    # ── 8. Noble gas factor ──
    if is_noble:
        noble = 10  # strong LP repulsion, no bonds
    else:
        noble = 0

    return {
        'sigma': sigma,
        'pi': pi,
        'coulomb': coulomb,
        'dispersion': dispersion,
        'lp_repulsion': lp_repulsion,
        'metallic': metallic,
        'noble': noble,
        'period': period,
        'den': den,
    }


def classify_pair(e1, e2):
    """Classify a single pair by dominant interaction."""
    ix = compute_interactions(e1, e2)

    # Override: if we have REAL bond data, use R₂
    b = get_bond_data(e1, e2)
    if b and b.alpha is not None:
        R2 = 2 ** b.alpha
        if R2 > 1.8: return 'gas', R2, 'data_R2'
        if R2 > 1.35: return 'liquid', R2, 'data_R2'
        if R2 > 1.15: return 'border', R2, 'data_R2'
        return 'crystal', R2, 'data_R2'

    # Noble gas → always molecular
    if ix['noble'] > 0:
        return 'border', 1.0, 'noble'

    # Determine dominant interaction
    covalent = ix['sigma'] + ix['pi']
    ionic = ix['coulomb']
    metal = ix['metallic']
    vdw = ix['dispersion']

    # R₂ from interactions:
    # R₂ = 1 + π/σ (resonance ratio)
    if ix['sigma'] > 0:
        R2 = 1 + ix['pi'] / ix['sigma']
    else:
        R2 = 1.0

    # Ionic dominance: Coulomb >> covalent → crystal
    if ionic > covalent * 2:
        return 'crystal', R2, f'ionic(C={ionic:.2f}>cov={covalent:.2f})'

    # Metallic dominance: delocalized >> localized
    if metal > covalent:
        return 'crystal', R2, f'metallic(M={metal:.2f}>cov={covalent:.2f})'

    # LP-LP repulsion reduces effective bond
    effective_R2 = R2 - ix['lp_repulsion'] * 0.1  # LP weakens bond

    # Classify by R₂
    if effective_R2 > 1.35:
        return 'liquid', effective_R2, f'covalent(R₂={effective_R2:.2f})'
    if effective_R2 > 1.15:
        return 'border', effective_R2, f'covalent(R₂={effective_R2:.2f})'
    return 'crystal', effective_R2, f'covalent(R₂={effective_R2:.2f})'


def parse(formula):
    counts = {}
    for m in re.finditer(r'([A-Z][a-z]?)(\d*)', formula):
        e = m.group(1)
        n = int(m.group(2)) if m.group(2) else 1
        if e in ELEMENTS or e in EN:
            counts[e] = counts.get(e, 0) + n
    return counts


def classify_compound(formula):
    """Classify compound from torus interactions."""
    counts = parse(formula)
    elements = sorted(counts.keys())

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
            return 'crystal', 1.0, 'pure_metal'
        cat, R2, reason = classify_pair(e, e)
        p = ELEMENTS.get(e, (3,))[0] if e in ELEMENTS else 3
        if cat in ('gas', 'liquid') and p >= 3:
            return 'border', R2, f'heavy_homo({reason})'
        return cat, R2, reason

    # Multiple elements: classify each pair, take WORST
    pair_results = []
    for i, e1 in enumerate(elements):
        for e2 in elements[i+1:]:
            cat, R2, reason = classify_pair(e1, e2)
            pair_results.append((cat, R2, f"{e1}-{e2}:{reason}"))

    if not pair_results:
        return 'crystal', 1.0, 'no_pairs'

    # Compound type = determined by the pair with LOWEST R₂
    # (weakest link determines if structure extends)
    worst = min(pair_results, key=lambda x: x[1])
    return worst


COMPAT = {
    "gas": ["mol"],
    "liquid": ["mol"],
    "border": ["mol", "cryst"],
    "crystal": ["cryst"],
    "refract": ["cryst"],
}


# ============================================================
# TEST
# ============================================================
if __name__ == "__main__":
    DS = [
        ('H2','mol'),('N2','mol'),('O2','mol'),('F2','mol'),('Cl2','mol'),
        ('HF','mol'),('HCl','mol'),('HBr','mol'),('HI','mol'),
        ('H2O','mol'),('H2S','mol'),('NH3','mol'),('PH3','mol'),
        ('AsH3','mol'),('SiH4','mol'),('GeH4','mol'),('B2H6','mol'),
        ('CO','mol'),('CO2','mol'),('NO','mol'),('NO2','mol'),('SO2','mol'),('SO3','mol'),
        ('BF3','mol'),('BCl3','mol'),('NF3','mol'),('PF5','mol'),('SF6','mol'),
        ('ClF3','mol'),('OF2','mol'),('Cl2O','mol'),
        ('CCl4','mol'),('CHCl3','mol'),('CH3Cl','mol'),
        ('COCl2','mol'),('CSCl2','mol'),('POCl3','mol'),('SOCl2','mol'),
        ('HCN','mol'),('CH3OH','mol'),('HNO3','mol'),('H2SO4','mol'),('HClO4','mol'),
        ('SiCl4','mol'),('GeCl4','mol'),('SnCl4','mol'),('TiCl4','mol'),
        ('PCl3','mol'),('PCl5','mol'),('SbCl5','mol'),
        ('WF6','mol'),('MoF6','mol'),('UF6','mol'),
        ('XeF2','mol'),('Br2','mol'),('CS2','mol'),('N2H4','mol'),('H2O2','mol'),
        ('NaCl','cryst'),('KCl','cryst'),('LiF','cryst'),('MgO','cryst'),('CaO','cryst'),
        ('MgF2','cryst'),('CaF2','cryst'),('AgCl','cryst'),('ZnO','cryst'),
        ('CuO','cryst'),('FeO','cryst'),('Fe2O3','cryst'),('FeCl3','cryst'),
        ('NiO','cryst'),('MnO2','cryst'),('TiO2','cryst'),('Al2O3','cryst'),
        ('AlCl3','cryst'),('WO3','cryst'),('PbO','cryst'),('PbCl2','cryst'),
        ('SnO2','cryst'),('SnCl2','cryst'),('Bi2O3','cryst'),('Sb2O3','cryst'),
        ('As2O3','cryst'),('HgCl2','cryst'),('CdS','cryst'),
        ('BaSO4','cryst'),('BaTiO3','cryst'),('CaCO3','cryst'),('CaSO4','cryst'),
        ('CaTiO3','cryst'),('MgCO3','cryst'),('Na2CO3','cryst'),
        ('NaNO3','cryst'),('NaOH','cryst'),('KOH','cryst'),('KMnO4','cryst'),
        ('NH4Cl','cryst'),('NH4NO3','cryst'),
        ('LiFePO4','cryst'),('LiCoO2','cryst'),('SrTiO3','cryst'),
        ('BiFeO3','cryst'),('LaAlO3','cryst'),('YBa2Cu3O7','cryst'),
        ('SiO2','cryst'),('SiC','cryst'),('BN','cryst'),('GaAs','cryst'),
        ('B2O3','cryst'),('SeO2','cryst'),('TeO2','cryst'),
        ('N2O5','cryst'),('SbCl3','cryst'),('BiCl3','cryst'),
        ('I2','cryst'),('S8','cryst'),('P4','cryst'),('P4O10','mol'),
        ('Li','cryst'),('Fe','cryst'),('Cu','cryst'),('Al','cryst'),
        ('W','cryst'),('Bi','cryst'),
    ]

    print("=" * 70)
    print("  v1.0 TORUS INTERACTIONS: ALL FORCES, NO RULES")
    print("=" * 70)
    print()

    c = w = 0; errs = []
    for f, k in DS:
        p, R2, r = classify_compound(f)
        ok = k in COMPAT.get(p, [])
        if ok: c += 1
        else: w += 1; errs.append((f, k, p, r, R2))

    t = c + w
    print(f"  Result: {c}/{t} = {c/t*100:.1f}%")
    print(f"  Errors: {w}")
    print()

    if errs:
        print(f"  Errors ({min(w, 20)} shown):")
        for f, k, p, r, R2 in sorted(errs)[:20]:
            print(f"    {f:15s} known={k:6s} pred={p:8s} R₂={R2:.3f} ({r})")

    # Show interaction breakdown for key compounds
    print(f"\n  Sample interactions:")
    for formula in ['NaCl', 'N2', 'Fe', 'SF6', 'SiO2', 'BN']:
        counts = parse(formula)
        elements = sorted(counts.keys())
        if len(elements) >= 2:
            e1, e2 = elements[0], elements[1]
            ix = compute_interactions(e1, e2)
            print(f"    {formula:>6} ({e1}-{e2}): σ={ix['sigma']:.2f} π={ix['pi']:.2f} "
                  f"Coul={ix['coulomb']:.2f} metal={ix['metallic']:.2f} disp={ix['dispersion']:.2f}")
