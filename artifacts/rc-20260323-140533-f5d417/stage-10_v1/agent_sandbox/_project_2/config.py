"""
Configuration for Aether Physical Properties Derivation Experiments
"""
from dataclasses import dataclass, field
from typing import List

@dataclass
class Config:
    """Hyperparameter configuration for aether property derivation experiments."""
    
    # Training parameters
    lr: float = 0.001
    batch_size: int = 64
    epochs: int = 15  # Reduced for time budget
    hidden_dim: int = 128  # Reduced for speed
    
    # Model architecture
    num_physical_params: int = 8
    aether_property_dim: int = 4
    input_dim: int = 12  # EM/gravity features
    
    # Time budget
    max_time_hours: float = 0.083  # ~5 minutes (300s)
    
    # Random seeds (exactly 3 for time budget)
    seeds: List[int] = field(default_factory=lambda: [0, 1, 2])
    
    # Regularization
    weight_decay: float = 1e-5
    validation_split: float = 0.15
    test_split: float = 0.15
    
    # Physics constraints
    tolerance_threshold: float = 1e-6
    lorentz_contraction_factor: float = 1.0
    eps: float = 1e-8
    
    # Data generation
    n_train_samples: int = 2000
    n_val_samples: int = 400
    n_test_samples: int = 400
    noise_level: float = 0.02
    
    # Aether physical constants (normalized units)
    c_normalized: float = 1.0  # Speed of light
    rho_aether_base: float = 1.0  # Base aether density
    K_aether_base: float = 1.0  # Base elasticity
    eta_aether_base: float = 0.01  # Base viscosity (low for superfluid)
    eps_aether_base: float = 1.0  # Base permittivity


def get_config() -> Config:
    """Return the default configuration."""
    return Config()