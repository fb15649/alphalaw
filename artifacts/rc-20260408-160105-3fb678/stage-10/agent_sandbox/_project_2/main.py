"""
Central configuration for the toroidal vortex geometry–material property correlation experiment.
All hyperparameters used across the experiment are defined here.
"""

import numpy as np


class ExperimentConfig:
    """Immutable configuration container for all experiment parameters."""

    def __init__(self):
        # ── Random seeds ──
        self.random_seeds = [0, 1, 2]

        # ── Data dimensions ──
        self.n_materials = 2000
        self.n_crystal_features = 48
        self.n_platonic_classes = 5
        self.n_vortex_features = 64
        self.n_physical_properties = 4
        self.n_magnetic_classes = 3
        self.platonic_embed_dim = 32

        # ── Model architecture ──
        self.hidden_dim = 128
        self.dropout_rate = 0.1

        # ── Training protocol ──
        self.lr = 0.001
        self.batch_size = 64
        self.epochs = 30
        self.patience = 10
        self.l2_reg = 1e-4
        self.max_grad_norm = 1.0

        # ── Data splits ──
        self.train_ratio = 0.70
        self.val_ratio = 0.15
        self.test_ratio = 0.15

        # ── Superfluid vacuum parameters ──
        # ρ = μ₀, G = 1/ε₀, η ≈ 0
        self.superfluid_density_rho = 1.2566370614e-6   # μ₀ in H/m
        self.vacuum_permittivity_eps = 8.854187817e-12   # ε₀ in F/m
        self.gravitational_constant_G = 6.674e-11        # G in m³/(kg·s²)
        self.viscosity_eta_approx = 0.0                   # ideal superfluid

        # ── Platonic solid names ──
        self.platonic_solids = [
            'tetrahedron', 'cube', 'octahedron', 'icosahedron', 'dodecahedron'
        ]

        # ── Magnetic classes ──
        self.magnetic_classes = ['ferromagnetic', 'paramagnetic', 'diamagnetic']

        # ── Crystal families ──
        self.crystal_families = [
            'triclinic', 'monoclinic', 'orthorhombic',
            'tetragonal', 'trigonal', 'hexagonal', 'cubic'
        ]
        self.crystal_family_weights = [0.04, 0.08, 0.15, 0.15, 0.08, 0.15, 0.35]

        # ── Focal loss parameters ──
        self.focal_alpha = np.array([0.5, 0.25, 0.25])
        self.focal_gamma = 2.0

        # ── Quasicrystal fraction ──
        self.quasicrystal_fraction = 0.06