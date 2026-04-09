"""Model architectures for aether property derivation."""

import torch
import torch.nn as nn
import torch.nn.functional as F
from experiment_config import AetherConfig

class BaseAetherModel(nn.Module):
    """Base model for aether property derivation."""
    
    def __init__(self, config: AetherConfig):
        """
        Initialize the base aether model.
        
        Args:
            config: Configuration object with hyperparameters
        """
        super().__init__()
        
        # Learnable physics parameters
        self.raw_params = nn.Parameter(torch.zeros(config.num_physics_params))
        # Initialize with physically motivated priors
        with torch.no_grad():
            self.raw_params.copy_(config.get_param_init())
        
        # Physics encoder network: [B, 6] -> [B, 128]
        self.physics_encoder = nn.Sequential(
            nn.Linear(6, config.hidden_dim),
            nn.ReLU(),
            nn.Linear(config.hidden_dim, config.hidden_dim),
            nn.ReLU(),
            nn.Linear(config.hidden_dim, 128)
        )
        
        # Property prediction head: [B, 136] -> [B, 4]
        self.property_head = nn.Sequential(
            nn.Linear(128 + config.num_physics_params, 64),
            nn.ReLU(),
            nn.Linear(64, 4)
        )
    
    def forward(self, obs: torch.Tensor) -> torch.Tensor:
        """
        Forward pass to derive aether properties from observations.
        
        Args:
            obs: Observation tensor of shape [B, 6]
            
        Returns:
            Properties tensor of shape [B, 4] with [density, elasticity, viscosity, permittivity]
        """
        # Encode physics observations
        encoded = self.physics_encoder(obs)  # [B, 128]
        
        # Expand parameters for batch
        params_expanded = self.raw_params.expand(obs.shape[0], -1)  # [B, 8]
        
        # Combine encoded features with parameters
        combined = torch.cat([encoded, params_expanded], dim=1)  # [B, 136]
        
        # Predict properties
        properties = self.property_head(combined)  # [B, 4]
        
        # Apply physical constraints
        properties = self.apply_physical_constraints(properties)
        
        return properties
    
    def apply_physical_constraints(self, props: torch.Tensor) -> torch.Tensor:
        """
        Apply physical constraints to ensure valid property values.
        
        Args:
            props: Raw property predictions [B, 4]
            
        Returns:
            Constrained properties [B, 4]
        """
        # Ensure positive density
        density = F.softplus(props[:, 0:1])
        
        # Ensure positive elasticity
        elasticity = F.softplus(props[:, 1:2])
        
        # Ensure positive viscosity
        viscosity = F.softplus(props[:, 2:3])
        
        # Permittivity near vacuum value with small variations
        permittivity = 8.854e-12 + torch.tanh(props[:, 3:4]) * 1e-13
        
        return torch.cat([density, elasticity, viscosity, permittivity], dim=1)
    
    def compute_physics_loss(
        self, 
        predictions: torch.Tensor, 
        targets: torch.Tensor, 
        errors: torch.Tensor
    ) -> torch.Tensor:
        """
        Compute chi-squared physics loss.
        
        Args:
            predictions: Model predictions [B, 4]
            targets: Target values [B, 4]
            errors: Measurement errors [B, 4]
            
        Returns:
            Scalar loss tensor
        """
        chi_squared = ((predictions - targets) ** 2 / (errors ** 2 + 1e-8)).mean()
        return chi_squared

class LorentzEtherModel(BaseAetherModel):
    """Full Lorentz ether theory with complete physical properties."""
    
    def __init__(self, config: AetherConfig):
        super().__init__(config)
        # Lorentz-specific velocity encoder
        self.velocity_encoder = nn.Sequential(
            nn.Linear(6, 32),
            nn.Tanh(),
            nn.Linear(32, 1)
        )
    
    def forward(self, obs: torch.Tensor) -> torch.Tensor:
        """
        Forward pass with Lorentz contraction effects.
        
        Args:
            obs: Observation tensor [B, 6]
            
        Returns:
            Properties tensor [B, 4]
        """
        # Encode physics observations
        encoded = self.physics_encoder(obs)  # [B, 128]
        
        # Compute Lorentz factor from velocity embedding
        v_squared = torch.sigmoid(self.velocity_encoder(obs))  # [B, 1]
        lorentz_factor = 1.0 / torch.sqrt(1.0 - v_squared + 1e-8)  # [B, 1]
        
        # Expand and correct parameters with Lorentz contraction
        params_expanded = self.raw_params.expand(obs.shape[0], -1)
        params_corrected = params_expanded * lorentz_factor
        
        # Combine and predict
        combined = torch.cat([encoded, params_corrected], dim=1)
        properties = self.property_head(combined)
        
        # Apply Lorentz-specific constraints
        properties = self.apply_lorentz_constraints(properties, lorentz_factor)
        
        return properties
    
    def apply_lorentz_constraints(
        self, 
        props: torch.Tensor, 
        gamma: torch.Tensor
    ) -> torch.Tensor:
        """
        Apply Lorentz transformation constraints to properties.
        
        Args:
            props: Raw properties [B, 4]
            gamma: Lorentz factor [B, 1]
            
        Returns:
            Constrained properties [B, 4]
        """
        # Density increases with motion (relativistic mass increase)
        density = F.softplus(props[:, 0:1]) * gamma
        
        # Elasticity transforms inversely (length contraction effect)
        elasticity = F.softplus(props[:, 1:2]) / gamma
        
        # Viscosity is frame-independent in Lorentz ether theory
        viscosity = F.softplus(props[:, 2:3])
        
        # Permittivity with small variations around vacuum value
        permittivity = 8.854e-12 + torch.tanh(props[:, 3:4]) * 1e-13
        
        return torch.cat([density, elasticity, viscosity, permittivity], dim=1)
    
    def compute_physics_loss(
        self, 
        predictions: torch.Tensor, 
        targets: torch.Tensor, 
        errors: torch.Tensor
    ) -> torch.Tensor:
        """
        Compute physics loss with Lorentz regularization.
        """
        chi_squared = ((predictions - targets) ** 2 / (errors ** 2 + 1e-8)).mean()
        lorentz_reg = (self.raw_params ** 2).mean()
        return chi_squared + 0.1 * lorentz_reg

class DiracAetherModel(BaseAetherModel):
    """Dirac 1951 aether model with quantum vacuum properties."""
    
    def __init__(self, config: AetherConfig):
        """
        Initialize Dirac aether model with quantum encoder.
        
        Args:
            config: Configuration object
        """
        super().__init__(config)
        
        # Quantum feature encoder for vacuum fluctuations
        self.quantum_encoder = nn.Sequential(
            nn.Linear(6, 64),
            nn.Tanh(),
            nn.Linear(64, 32)
        )
        
        # Vacuum coupling parameter - controls classical/quantum feature mixing
        self.vacuum_coupling = nn.Parameter(torch.tensor(0.5))
        
        # Separate property head for Dirac model
        self.dirac_property_head = nn.Sequential(
            nn.Linear(160, 64),
            nn.Tanh(),
            nn.Linear(64, 4)
        )
    
    def forward(self, obs: torch.Tensor) -> torch.Tensor:
        """
        Forward pass with quantum-classical feature mixing.
        
        Args:
            obs: Observation tensor [B, 6]
            
        Returns:
            Properties tensor [B, 4]
        """
        # Classical encoding from base model
        classical_encoded = self.physics_encoder(obs)  # [B, 128]
        
        # Quantum vacuum features
        quantum_features = self.quantum_encoder(obs)  # [B, 32]
        
        # Interpolate between classical and quantum features
        vacuum_factor = torch.sigmoid(self.vacuum_coupling)
        
        # Combine classical and quantum features
        combined_features = torch.cat([classical_encoded, quantum_features], dim=1)  # [B, 160]
        
        # Combine with learnable physics parameters
        params_expanded = self.raw_params.expand(obs.shape[0], -1)
        
        # Predict using Dirac-specific head
        properties = self.dirac_property_head(combined_features)
        properties = self.apply_dirac_quantization(properties)
        
        return properties
    
    def apply_dirac_quantization(self, props: torch.Tensor) -> torch.Tensor:
        """
        Apply Dirac quantization to properties.
        """
        # Reduced Planck constant for quantization
        h_bar = 1.054571817e-34
        
        # Quantized density - scaled by Planck constant
        density = F.softplus(props[:, 0:1]) * h_bar
        
        # Standard elasticity (macroscopic property)
        elasticity = F.softplus(props[:, 1:2])
        
        # Quantized viscosity - quantum vacuum fluctuations
        viscosity = F.softplus(props[:, 2:3]) * h_bar
        
        # Permittivity with small relative variations around vacuum value
        permittivity = 8.854e-12 * (1 + torch.tanh(props[:, 3:4]) * 0.01)
        
        return torch.cat([density, elasticity, viscosity, permittivity], dim=1)
    
    def compute_physics_loss(
        self, 
        predictions: torch.Tensor, 
        targets: torch.Tensor, 
        errors: torch.Tensor
    ) -> torch.Tensor:
        """
        Compute physics loss with quantization regularization.
        """
        chi_squared = ((predictions - targets) ** 2 / (errors ** 2 + 1e-8)).mean()
        quantization_reg = torch.abs(self.vacuum_coupling - 0.5)
        return chi_squared + 0.05 * quantization_reg

class MaxwellBaseline(BaseAetherModel):
    """Standard Maxwell equations without aether medium."""
    
    def __init__(self, config: AetherConfig):
        """
        Initialize Maxwell baseline with dropout regularization.
        
        Args:
            config: Configuration object
        """
        super().__init__(config)
        
        # Maxwell-specific encoder with dropout for regularization
        self.maxwell_encoder = nn.Sequential(
            nn.Linear(6, config.hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(config.hidden_dim, 128)
        )
        
        # Freeze aether parameters to near-zero (no aether in Maxwell theory)
        with torch.no_grad():
            self.raw_params.fill_(1e-10)
    
    def forward(self, obs: torch.Tensor) -> torch.Tensor:
        """
        Forward pass without aether medium effects.
        
        Args:
            obs: Observation tensor [B, 6]
            
        Returns:
            Properties tensor [B, 4]
        """
        # Use Maxwell encoder instead of physics_encoder
        encoded = self.maxwell_encoder(obs)  # [B, 128]
        
        # Parameters are essentially zero (no aether)
        params_expanded = self.raw_params.expand(obs.shape[0], -1)
        combined = torch.cat([encoded, params_expanded], dim=1)
        
        properties = self.property_head(combined)
        properties = self.apply_maxwell_constraints(properties)
        
        return properties
    
    def apply_maxwell_constraints(self, props: torch.Tensor) -> torch.Tensor:
        """
        Apply Maxwell constraints - no aether properties.
        """
        # No aether density in Maxwell's theory
        density = torch.zeros_like(props[:, 0:1])
        
        # No aether elasticity
        elasticity = torch.zeros_like(props[:, 1:2])
        
        # No aether viscosity
        viscosity = torch.zeros_like(props[:, 2:3])
        
        # Only permittivity is meaningful in Maxwell's equations
        permittivity = 8.854e-12 + torch.tanh(props[:, 3:4]) * 1e-13
        
        return torch.cat([density, elasticity, viscosity, permittivity], dim=1)
    
    def compute_physics_loss(
        self, 
        predictions: torch.Tensor, 
        targets: torch.Tensor, 
        errors: torch.Tensor
    ) -> torch.Tensor:
        """
        Compute loss only on permittivity (other properties are zero).
        """
        # Only compute loss on permittivity (column 3)
        permittivity_pred = predictions[:, 3:4]
        permittivity_target = targets[:, 3:4]
        permittivity_error = errors[:, 3:4]
        
        chi_squared = ((permittivity_pred - permittivity_target) ** 2 / 
                       (permittivity_error ** 2 + 1e-8)).mean()
        
        return chi_squared

class SuperfluidVacuumModel(BaseAetherModel):
    """Superfluid vacuum theory with viscosity-free aether."""
    
    def __init__(self, config: AetherConfig):
        """
        Initialize superfluid vacuum model.
        
        Args:
            config: Configuration object
        """
        super().__init__(config)
        
        # Superfluid encoder with GELU activation for smooth gradients
        self.superfluid_encoder = nn.Sequential(
            nn.Linear(6, config.hidden_dim),
            nn.GELU(),
            nn.Linear(config.hidden_dim, 128)
        )
        
        # Critical velocity parameter for superfluid behavior
        self.critical_velocity = nn.Parameter(torch.tensor(1e-6))
    
    def forward(self, obs: torch.Tensor) -> torch.Tensor:
        """
        Forward pass with superfluid constraints.
        
        Args:
            obs: Observation tensor [B, 6]
            
        Returns:
            Properties tensor [B, 4]
        """
        # Use superfluid encoder
        encoded = self.superfluid_encoder(obs)  # [B, 128]
        
        params_expanded = self.raw_params.expand(obs.shape[0], -1)
        combined = torch.cat([encoded, params_expanded], dim=1)
        
        properties = self.property_head(combined)
        properties = self.apply_superfluid_constraints(properties)
        
        return properties
    
    def apply_superfluid_constraints(self, props: torch.Tensor) -> torch.Tensor:
        """
        Apply superfluid constraints - zero viscosity.
        """
        # Positive density
        density = F.softplus(props[:, 0:1])
        
        # Positive elasticity
        elasticity = F.softplus(props[:, 1:2])
        
        # Zero viscosity - defining property of superfluid!
        viscosity = torch.zeros_like(props[:, 2:3])
        
        # Standard permittivity
        permittivity = 8.854e-12 + torch.tanh(props[:, 3:4]) * 1e-13
        
        return torch.cat([density, elasticity, viscosity, permittivity], dim=1)
    
    def compute_physics_loss(
        self, 
        predictions: torch.Tensor, 
        targets: torch.Tensor, 
        errors: torch.Tensor
    ) -> torch.Tensor:
        """
        Compute physics loss with superfluid regularization.
        """
        chi_squared = ((predictions - targets) ** 2 / (errors ** 2 + 1e-8)).mean()
        # Penalize any non-zero viscosity predictions (column 2)
        superfluid_reg = torch.abs(predictions[:, 2]).mean()
        return chi_squared + 0.1 * superfluid_reg

class LinearizedAetherModel(BaseAetherModel):
    """Simplified linear model for ablation study."""
    
    def __init__(self, config: AetherConfig):
        """
        Initialize linearized model.
        
        Args:
            config: Configuration object
        """
        super().__init__(config)
        
        # Replace physics_encoder with simple linear layer (no non-linearity)
        self.physics_encoder = nn.Linear(6, 128)
        
        # Simpler property head for linearized model
        self.property_head = nn.Sequential(
            nn.Linear(128 + config.num_physics_params, 32),
            nn.ReLU(),
            nn.Linear(32, 4)
        )
    
    def forward(self, obs: torch.Tensor) -> torch.Tensor:
        """
        Forward pass without non-linear encoding.
        
        Args:
            obs: Observation tensor [B, 6]
            
        Returns:
            Properties tensor [B, 4]
        """
        # Linear encoding - no nonlinearity in encoder
        encoded = self.physics_encoder(obs)  # [B, 128]
        
        params_expanded = self.raw_params.expand(obs.shape[0], -1)
        combined = torch.cat([encoded, params_expanded], dim=1)
        
        properties = self.property_head(combined)
        properties = self.apply_physical_constraints(properties)
        
        return properties
    
    def compute_physics_loss(
        self, 
        predictions: torch.Tensor, 
        targets: torch.Tensor, 
        errors: torch.Tensor
    ) -> torch.Tensor:
        """
        Compute basic physics loss without additional regularization.
        """
        chi_squared = ((predictions - targets) ** 2 / (errors ** 2 + 1e-8)).mean()
        return chi_squared

class NoViscosityAetherModel(BaseAetherModel):
    """Aether model without viscosity component (ablation)."""
    
    def __init__(self, config: AetherConfig):
        super().__init__(config)
        # Property head with 3 outputs instead of 4
        self.novisc_property_head = nn.Sequential(
            nn.Linear(128 + config.num_physics_params, 64),
            nn.ReLU(),
            nn.Linear(64, 3)  # Only 3 properties: density, elasticity, permittivity
        )
    
    def forward(self, obs: torch.Tensor) -> torch.Tensor:
        """
        Forward pass with viscosity component ablated.
        
        Args:
            obs: Observation tensor [B, 6]
            
        Returns:
            Properties tensor [B, 4]
        """
        encoded = self.physics_encoder(obs)  # [B, 128]
        
        params_expanded = self.raw_params.expand(obs.shape[0], -1)
        combined = torch.cat([encoded, params_expanded], dim=1)  # [B, 136]
        
        # Predict only 3 properties using ablated head
        properties_3 = self.novisc_property_head(combined)  # [B, 3]
        properties = self.apply_no_viscosity_constraints(properties_3)
        
        return properties
    
    def apply_no_viscosity_constraints(self, props: torch.Tensor) -> torch.Tensor:
        """
        Apply constraints with viscosity ablated.
        
        Args:
            props: Raw properties [B, 3] (density, elasticity, permittivity)
            
        Returns:
            Constrained properties [B, 4]
        """
        # Positive density
        density = F.softplus(props[:, 0:1])
        
        # Positive elasticity
        elasticity = F.softplus(props[:, 1:2])
        
        # No viscosity - ablated component
        viscosity = torch.zeros_like(props[:, 0:1])
        
        # Standard permittivity
        permittivity = 8.854e-12 + torch.tanh(props[:, 2:3]) * 1e-13
        
        return torch.cat([density, elasticity, viscosity, permittivity], dim=1)
    
    def compute_physics_loss(
        self, 
        predictions: torch.Tensor, 
        targets: torch.Tensor, 
        errors: torch.Tensor
    ) -> torch.Tensor:
        """
        Compute physics loss excluding viscosity component.
        
        CRITICAL FIX: Create mask on same device as predictions to avoid
        device mismatch when tensors are on GPU.
        """
        # Only compute loss on non-viscosity properties
        # CRITICAL FIX: Specify device to match predictions/targets/errors
        mask = torch.tensor([1.0, 1.0, 0.0, 1.0], device=predictions.device)
        chi_squared = ((predictions - targets) ** 2 * mask / (errors ** 2 + 1e-8)).mean()
        return chi_squared