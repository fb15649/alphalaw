"""
v1 GEARS MODEL — from torus physics, not chemistry rules.

Each torus has:
  ω₁, ω₂, ω₃ — three frequencies
  N_channels   — number of outgoing flow channels ("teeth")
  N_blocked    — channels where flow returns to self (can't reach neighbor)
  N_active     — channels available for coupling = N_channels - N_blocked

Terminal torus: N_active = 1 (bonds once, done)
Bridging torus: N_active ≥ 2 (can couple to multiple neighbors → network)

Molecule = all tori are either central or terminal. No bridges → closed.
Crystal = at least one bridging torus → network extends indefinitely.

The STRENGTH of each coupling = R₂ = 2^α (frequency resonance).
"""
import re, sys, math
sys.path.insert(0, '/Volumes/Backup/Python_projects/alphalaw')
from alphalaw.data import BONDS, ELEMENTS, get_bond_data

EN = {
    'H':2.20,'Li':0.98,'Be':1.57,'B':2.04,'C':2.55,'N':3.04,'O':3.44,'F':3.98,
    'Na':0.93,'Mg':1.31,'Al':1.61,'Si':1.90,'P':2.19,'S':2.58,'Cl':3.16,
    'K':0.82,'Ca':1.00,'Sc':1.36,'Ti':1.54,'V':1.63,'Cr':1.66,'Mn':1.55,
    'Fe':1.83,'Co':1.88,'Ni':1.91,'Cu':1.90,'Zn':1.65,
    'Ga':1.81,'Ge':2.01,'As':2.18,'Se':2.55,'Br':2.96,
    'Sr':0.95,'Y':1.22,'Zr':1.33,'Mo':2.16,'Ag':1.93,'Cd':1.69,
    'Sn':1.96,'Sb':2.05,'Te':2.10,'I':2.66,'Ba':0.89,'La':1.10,
    'Hf':1.30,'W':2.36,'Re':1.90,'Pt':2.28,'Au':2.54,'Hg':2.00,
    'Pb':2.33,'Bi':2.02,'Xe':2.60,'Kr':3.00,'U':1.38,
    'Os':2.20,'Ir':2.20,'Nb':1.60,'Ta':1.50,'Tl':1.62,
}


def torus_channels(elem):
    """
    How many flow channels does this torus have?
    Active = can couple with neighbor.
    Blocked = flow returns to self.

    Derived from: group number and block.
    In torus terms: number of distinct flow exit directions.
    """
    if elem not in ELEMENTS:
        return 1, 0  # unknown → assume terminal

    period, group, block, valence, lp = ELEMENTS[elem]
    lp_eff = max(0, lp)

    # Noble gases: all channels blocked
    if group == 18 or elem in ('He', 'Ne', 'Ar', 'Kr', 'Xe', 'Rn'):
        return 0, lp_eff  # no active channels (but Xe CAN bond to F)

    # Halogens: 1 active (the rest blocked)
    if group == 17:
        return 1, lp_eff

    # Group 16 (O, S, Se, Te): 2 active
    if group == 16:
        return 2, lp_eff

    # Group 15 (N, P, As, Sb, Bi): 3 active
    if group == 15:
        return 3, lp_eff

    # Group 14 (C, Si, Ge, Sn, Pb): 4 active
    if group == 14:
        return 4, 0

    # Group 13 (B, Al, Ga): 3 active
    if group == 13:
        return 3, 0

    # H: 1 active
    if elem == 'H':
        return 1, 0

    # Metals (group 1, 2): 1-2 active, give away electrons
    if group in (1, 2):
        return group, 0

    # d-block: many channels (4-6 typically), no LP
    if block == 'd':
        return min(valence, 6), 0

    # f-block
    if block == 'f':
        return min(valence, 6), 0

    return 2, 0  # default


def is_terminal(elem):
    """Terminal torus: bonds once, then saturated."""
    active, blocked = torus_channels(elem)
    return active <= 1


def is_bridging(elem):
    """Bridging torus: can couple to 2+ neighbors → extends network."""
    active, blocked = torus_channels(elem)
    return active >= 2


def frequency_resonance(e1, e2):
    """R₂ = 2^α from bond data, or estimated from EN ratio."""
    b = get_bond_data(e1, e2)
    if b and b.alpha is not None:
        return 2 ** b.alpha

    en1 = EN.get(e1, 1.5)
    en2 = EN.get(e2, 1.5)
    # Frequency ratio → how well do they resonate
    ratio = max(en1, en2) / min(en1, en2) if min(en1, en2) > 0 else 1
    # Higher ratio → worse resonance → lower R₂
    # R₂ = 2 / ratio (octave / frequency mismatch)
    R2 = 2.0 / ratio
    return max(1.0, min(R2, 3.0))


def parse(formula):
    counts = {}
    for m in re.finditer(r'([A-Z][a-z]?)(\d*)', formula):
        e = m.group(1)
        n = int(m.group(2)) if m.group(2) else 1
        if e in ELEMENTS or e in EN:
            counts[e] = counts.get(e, 0) + n
    return counts


METALS_SET = {
    "Li","Na","K","Rb","Cs","Be","Mg","Ca","Sr","Ba",
    "Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn",
    "Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd",
    "La","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg",
    "Al","Ga","In","Tl","Sn","Pb","Bi",
}


def classify(formula):
    """
    Classify from torus gear physics.

    Three determinations:
    1. Are all atoms SATURATED (all channels used by terminals)?
       → Yes = molecule
    2. Does any atom BRIDGE (channels lead to more non-terminals)?
       → Yes = crystal
    3. How strong is the resonance (R₂)?
       → Determines gas/liquid/border/crystal within each type
    """
    counts = parse(formula)
    elements = sorted(counts.keys())

    # Single element
    if len(elements) == 1:
        e = elements[0]
        if e in METALS_SET:
            return 'crystal', f'metal({e})'
        active, blocked = torus_channels(e)
        if active == 0:
            return 'border', f'noble({e})'
        b = get_bond_data(e, e)
        if b and b.alpha is not None:
            p = ELEMENTS.get(e, (3,))[0] if e in ELEMENTS else 3
            if b.alpha > 1 and p <= 2:
                return 'liquid', f'light_homo(α={b.alpha:.2f})'
            return 'border', f'homo(α={b.alpha:.2f})'
        return 'border', f'pure_nonmetal'

    # Multiple elements
    has_metal = any(e in METALS_SET for e in elements)
    has_bridge = False
    has_terminal_only_neighbor = True  # assume true until proven false
    min_R2 = 10

    # Check each pair
    for i, e1 in enumerate(elements):
        for e2 in elements[i+1:]:
            R2 = frequency_resonance(e1, e2)
            min_R2 = min(min_R2, R2)

    # Determine topology: terminal vs bridging
    # Count channels
    total_channels = 0
    terminal_channels = 0
    for e in elements:
        n_atoms = counts[e]
        active, blocked = torus_channels(e)
        total_channels += active * n_atoms
        if active <= 1:
            terminal_channels += active * n_atoms

    # Ratio of terminal channels to total
    # If mostly terminal → molecule (ёжик by physics)
    # If mostly bridging → crystal (network by physics)
    if total_channels > 0:
        terminal_ratio = terminal_channels / total_channels
    else:
        terminal_ratio = 0

    # Pure metals → all bridging → crystal
    if has_metal and terminal_ratio < 0.3:
        return 'crystal', f'metal_network(term={terminal_ratio:.2f})'

    # Metal + high terminal ratio → could be molecular metal halide
    if has_metal and terminal_ratio > 0.6:
        # If resonance is high → molecular
        if min_R2 > 1.3:
            return 'liquid', f'mol_metal_halide(term={terminal_ratio:.2f},R₂={min_R2:.2f})'
        return 'crystal', f'ionic(term={terminal_ratio:.2f},R₂={min_R2:.2f})'

    # All nonmetals
    if terminal_ratio > 0.5:
        # Majority terminal → molecular (ёжик)
        if min_R2 > 1.35:
            return 'liquid', f'cov_mol(term={terminal_ratio:.2f},R₂={min_R2:.2f})'
        return 'border', f'cov_border(term={terminal_ratio:.2f},R₂={min_R2:.2f})'

    # Majority bridging → network
    if min_R2 > 1.35:
        return 'border', f'cov_network_hi(term={terminal_ratio:.2f},R₂={min_R2:.2f})'
    return 'crystal', f'cov_network(term={terminal_ratio:.2f},R₂={min_R2:.2f})'


COMPAT = {
    "gas": ["mol"], "liquid": ["mol"], "border": ["mol", "cryst"],
    "crystal": ["cryst"], "refract": ["cryst"],
}


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
    print("  v1.0 GEARS MODEL — шестерёнки, каналы, насыщенность")
    print("  Без правил. Только: каналы + резонанс.")
    print("=" * 70)
    print()

    c = w = 0; errs = []
    for f, k in DS:
        p, r = classify(f)
        ok = k in COMPAT.get(p, [])
        if ok: c += 1
        else: w += 1; errs.append((f, k, p, r))

    t = c + w
    print(f"  Result: {c}/{t} = {c/t*100:.1f}%")
    print(f"  Errors: {w}")
    if errs:
        print(f"\n  Errors:")
        for f, k, p, r in sorted(errs)[:25]:
            print(f"    {f:15s} known={k:6s} pred={p:8s} ({r})")
        if len(errs) > 25:
            print(f"    ... +{len(errs)-25} more")
