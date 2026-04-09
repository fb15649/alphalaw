"""Configuration for aether property derivation experiments."""

import torch
from typing import Dict, Tuple, List

class AetherConfig:
    """Hyperparameter configuration for aether property derivation experiments."""
    
    def __init__(self):
        """Initialize all hyperparameters and validate configuration."""
        # Training hyperparameters
        self.lr = 0.001
        self.batch_size = 64
        self.epochs = 100
        self.hidden_dim = 256
        self.num_physics_params = 8
        self.seeds = [42, 123, 456, 789, 1024]
        self.max_hours = 4
        
        # Device configuration - resolve 'auto' to actual available device
        if torch.cuda.is_available():
            self.device = 'cuda'
        else:
            try:
                if torch.backends.mps.is_available():
                    self.device = 'mps'
                else:
                    self.device = 'cpu'
            except AttributeError:
                # MPS not available in this PyTorch version
                self.device = 'cpu'
        
        # Regularization parameters
        self.weight_decay = 1e-5
        self.aether_constraint_weight = 0.1
        self.viscosity_reg = 0.01
        self.permittivity_reg = 0.01
        
        # Physical priors
        self.density_prior = 1e-6
        self.elasticity_prior = 1e11
        
        # Physical parameter bounds for validation
        self.param_bounds: Dict[str, Tuple[float, float]] = {
            'density': (1e-12, 1e-3),
            'elasticity': (1e8, 1e15),
            'viscosity': (0.0, 1e6),
            'permittivity': (8e-12, 9e-12)
        }
        
        # Validate parameter bounds consistency
        self._validate_bounds()
    
    def _validate_bounds(self) -> None:
        """Validate that all parameter bounds are physically consistent."""
        for param_name, (lower, upper) in self.param_bounds.items():
            if lower >= upper:
                raise ValueError(
                    f"Invalid bounds for {param_name}: lower ({lower}) >= upper ({upper})"
                )
            if lower < 0:
                raise ValueError(
                    f"Negative lower bound for {param_name}: {lower} - physically implausible"
                )
    
    def get_param_init(self) -> torch.Tensor:
        """
        Get initial parameter values with physically motivated priors.
        
        Returns:
            torch.Tensor: Initial parameters of shape [num_physics_params]
                         with log-transformed values for scale-invariant optimization.
        """
        # Physical priors for the 8 parameters:
        # [density, elasticity, viscosity, permittivity, aux1, aux2, aux3, aux4]
        priors = torch.tensor([
            self.density_prior,      # density ~1e-6 kg/m³
            self.elasticity_prior,   # elasticity ~1e11 Pa
            1e3,                     # viscosity ~1e3 Pa·s
            8.854e-12,               # permittivity ~ε₀ (vacuum permittivity)
            0.5, 0.5, 0.5, 0.5,     # auxiliary coupling parameters
        ], dtype=torch.float32)
        
        # Apply log transform for scale-invariant optimization
        # This enables gradient-based optimization to work effectively across
        # parameters that span many orders of magnitude (e.g., 1e-6 to 1e11)
        init_params = torch.log(priors + 1e-30)  # Small epsilon to avoid log(0)
        
        return init_params