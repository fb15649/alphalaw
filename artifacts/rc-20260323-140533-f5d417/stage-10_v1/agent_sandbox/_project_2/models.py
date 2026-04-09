"""
All aether model implementations with different theoretical frameworks.

Models predict aether physical properties [rho, K, eta, eps] from
electromagnetic and gravitational measurements.
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Any
import config


class BaseAetherModel(nn.Module):
    """
    Base model for aether property derivation.
    
    Input: [B, 12] EM/gravity features
    Output: [B, 4] aether properties [rho, K, eta, eps]
    """
    
    def __init__(self, cfg: config.Config):
        super().__init__()
        self.cfg = cfg
        self.input_dim = cfg.input_dim
        self.output_dim = cfg.aether_property_dim
        self.hidden_dim = cfg.hidden_dim
        
        # Encoder network
        self.encoder = nn.Sequential(
            nn.Linear(self.input_dim, self.hidden_dim),
            nn.LayerNorm(self.hidden_dim),
            nn.GELU(),
            nn.Linear(self.hidden_dim, self.hidden_dim),
            nn.LayerNorm(self.hidden_dim),
            nn.GELU(),
            nn.Linear(self.hidden_dim, self.hidden_dim // 2),
            nn.LayerNorm(self.hidden_dim // 2),
            nn.GELU()
        )
        
        # Property prediction head
        self.property_head = nn.Linear(self.hidden_dim // 2, self.output_dim)
        
        # Store features for physics loss
        self.last_features = None
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass.
        
        Args:
            x: [B, 12] input features
            
        Returns:
            [B, 4] predicted aether properties [rho, K, eta, eps]
        """
        h = self.encoder(x)  # [B, hidden_dim // 2]
        self.last_features = h.detach()
        raw_properties = self.property_head(h)  # [B, 4]
        # Ensure positive values
        properties = F.softplus(raw_properties)
        return properties
    
    def compute_loss(
        self, 
        pred: torch.Tensor, 
        target: torch.Tensor, 
        x: torch.Tensor
    ) -> torch.Tensor:
        """
        Compute physics-constrained loss.
        
        Args:
            pred: [B, 4] predicted properties
            target: [B, 4] target properties
            x: [B, 12] input features (for physics constraints)
            
        Returns:
            Scalar loss value
        """
        # Base MSE loss
        mse_loss = F.mse_loss(pred, target)
        
        # Physics consistency: c = sqrt(K/rho)
        rho = pred[:, 0:1]
        K = pred[:, 1:2]
        
        predicted_c = torch.sqrt(K / (rho + self.cfg.eps))
        # Measured c is in feature index 2 (normalized)
        measured_c = x[:, 2:3]
        
        physics_reg = F.mse_loss(predicted_c, measured_c)
        
        total_loss = mse_loss + 0.1 * physics_reg
        return total_loss
    
    def get_model_name(self) -> str:
        return "BaseAetherModel"
    
    def get_model_info(self) -> Dict[str, Any]:
        return {
            'name': self.get_model_name(),
            'parameters': sum(p.numel() for p in self.parameters()),
            'trainable': sum(p.numel() for p in self.parameters() if p.requires_grad)
        }


class LorentzEtherTheory(BaseAetherModel):
    """
    Lorentz Ether Theory with Fitzgerald contraction and aether drift.
    
    Key features:
    - Lorentz contraction factor: gamma = 1/sqrt(1 - v^2/c^2)
    - Aether drift velocity as learnable parameter
    - Modified Maxwell equations with aether frame
    """
    
    def __init__(self, cfg: config.Config):
        super().__init__(cfg)
        
        # Learnable aether velocity (3D vector)
        self.v_aether = nn.Parameter(torch.zeros(3))
        
        # Lorentz-modified network
        self.lorentz_net = nn.Sequential(
            nn.Linear(self.hidden_dim // 2 + 3, self.hidden_dim // 2),
            nn.LayerNorm(self.hidden_dim // 2),
            nn.GELU(),
            nn.Linear(self.hidden_dim // 2, self.output_dim)
        )
        
        # Replace property head
        del self.property_head
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass with Lorentz contraction."""
        # Compute Lorentz factor
        v_aether_norm_sq = torch.sum(self.v_aether ** 2)
        c_sq = self.cfg.c_normalized ** 2
        gamma = 1.0 / torch.sqrt(1 - v_aether_norm_sq / c_sq + self.cfg.eps)
        
        # Apply contraction to features
        contracted_features = x * gamma
        
        # Encode
        h = self.encoder(contracted_features)
        self.last_features = h.detach()
        
        # Concatenate with aether velocity
        batch_size = x.shape[0]
        v_expanded = self.v_aether.unsqueeze(0).expand(batch_size, -1)
        h_combined = torch.cat([h, v_expanded], dim=1)
        
        # Predict properties
        raw_properties = self.lorentz_net(h_combined)
        properties = F.softplus(raw_properties)
        
        return properties
    
    def compute_loss(
        self, 
        pred: torch.Tensor, 
        target: torch.Tensor, 
        x: torch.Tensor
    ) -> torch.Tensor:
        """Loss with Lorentz invariance constraints."""
        mse_loss = F.mse_loss(pred, target)
        
        rho = pred[:, 0:1]
        K = pred[:, 1:2]
        
        # Wave speed constraint
        predicted_c = torch.sqrt(K / (rho + self.cfg.eps))
        measured_c = x[:, 2:3]
        physics_reg = F.mse_loss(predicted_c, measured_c)
        
        # Aether drift anisotropy constraint
        v_norm = torch.norm(self.v_aether) + self.cfg.eps
        # Feature 5 contains anisotropy
        expected_anisotropy = x[:, 5:6].mean()
        drift_effect = v_norm / (predicted_c.mean() + self.cfg.eps)
        drift_reg = torch.abs(drift_effect - expected_anisotropy)
        
        total_loss = mse_loss + 0.1 * physics_reg + 0.05 * drift_reg
        return total_loss
    
    def get_model_name(self) -> str:
        return "LorentzEtherTheory"


class DiracAetherModel(BaseAetherModel):
    """
    Dirac 1951 Aether Model with variable density field.
    
    Key features:
    - Timelike velocity 4-vector b_mu
    - Variable aether density field
    - Large numbers hypothesis coupling
    """
    
    def __init__(self, cfg: config.Config):
        super().__init__(cfg)
        
        # Dirac's aether velocity 4-vector (timelike)
        self.b_mu = nn.Parameter(torch.tensor([1.0, 0.0, 0.0, 0.0]))
        
        # Variable density field network
        self.density_field_net = nn.Sequential(
            nn.Linear(self.hidden_dim // 2 + 4, self.hidden_dim // 4),
            nn.LayerNorm(self.hidden_dim // 4),
            nn.GELU(),
            nn.Linear(self.hidden_dim // 4, 1),
            nn.Softplus()
        )
        
        # Quantum coupling (Dirac's large numbers)
        self.quantum_coupling = nn.Parameter(torch.tensor(0.01))
        
        # Modified head
        self.dirac_head = nn.Linear(self.hidden_dim // 2 + 1, self.output_dim)
        del self.property_head
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass with variable density field."""
        h = self.encoder(x)
        self.last_features = h.detach()
        
        batch_size = x.shape[0]
        
        # Extract position features (indices 6-8 are spatial coords)
        position_features = x[:, 6:10]  # Include 4th component for 4-vector
        
        # Compute variable density
        density_input = torch.cat([h, position_features], dim=1)
        variable_density = self.density_field_net(density_input)
        
        # Combine features
        h_with_density = torch.cat([h, variable_density], dim=1)
        
        # Predict properties
        raw_properties = self.dirac_head(h_with_density)
        properties = F.softplus(raw_properties)
        
        # Modulate density by variable field (avoid inplace operation)
        adjusted_density = properties[:, 0:1] * variable_density
        properties = torch.cat([adjusted_density, properties[:, 1:4]], dim=1)
        
        return properties
    
    def compute_loss(
        self, 
        pred: torch.Tensor, 
        target: torch.Tensor, 
        x: torch.Tensor
    ) -> torch.Tensor:
        """Loss with Dirac large numbers constraint."""
        mse_loss = F.mse_loss(pred, target)
        
        rho = pred[:, 0:1]
        K = pred[:, 1:2]
        
        # Wave speed constraint
        predicted_c = torch.sqrt(K / (rho + self.cfg.eps))
        measured_c = x[:, 2:3]
        physics_reg = F.mse_loss(predicted_c, measured_c)
        
        # Large numbers hypothesis: rho_aether ~ 1/G
        # In normalized units, constrain to ~1
        large_number_reg = F.mse_loss(rho.mean(), torch.ones_like(rho.mean()))
        
        # Coupling regularization
        coupling_reg = torch.abs(self.quantum_coupling - 0.01)
        
        total_loss = mse_loss + 0.1 * physics_reg + 0.01 * large_number_reg + 0.001 * coupling_reg
        return total_loss
    
    def get_model_name(self) -> str:
        return "DiracAetherModel"


class SuperfluidVacuumTheory(BaseAetherModel):
    """
    Superfluid Vacuum Theory with phonon-like excitations.
    
    Key features:
    - Superfluid order parameter
    - Phonon propagation network
    - Non-local correlations (attention mechanism)
    - Landau critical velocity
    """
    
    def __init__(self, cfg: config.Config):
        super().__init__(cfg)
        
        # Superfluid order parameter
        self.order_parameter = nn.Parameter(torch.ones(self.hidden_dim // 2))
        
        # Phonon propagation network
        self.phonon_net = nn.Sequential(
            nn.Linear(self.hidden_dim // 2, self.hidden_dim // 2),
            nn.LayerNorm(self.hidden_dim // 2),
            nn.Tanh(),
            nn.Linear(self.hidden_dim // 2, self.hidden_dim // 2)
        )
        
        # Non-local correlation (self-attention)
        self.correlation_net = nn.MultiheadAttention(
            embed_dim=self.hidden_dim // 2,
            num_heads=4,
            batch_first=True
        )
        
        # Critical velocity (Landau criterion)
        self.v_critical = nn.Parameter(torch.tensor(0.5))
        
        # Superfluid head
        self.superfluid_head = nn.Linear(self.hidden_dim // 2, self.output_dim)
        del self.property_head
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass with superfluid properties."""
        h = self.encoder(x)
        self.last_features = h.detach()
        
        # Apply order parameter modulation
        h_ordered = h * self.order_parameter
        
        # Phonon excitations
        phonon_features = self.phonon_net(h_ordered)
        
        # Non-local correlations (self-attention)
        h_unsq = h_ordered.unsqueeze(1)  # [B, 1, hidden_dim // 2]
        correlated, _ = self.correlation_net(h_unsq, h_unsq, h_unsq)
        correlated = correlated.squeeze(1)  # [B, hidden_dim // 2]
        
        # Combine features
        combined = h_ordered + phonon_features + 0.1 * correlated
        
        # Predict properties
        raw_properties = self.superfluid_head(combined)
        properties = F.softplus(raw_properties)
        
        # Superfluid constraint: reduce viscosity below critical velocity
        # Feature 2 contains velocity
        velocity = torch.abs(x[:, 2:3])
        below_critical = (velocity < self.v_critical).float()
        # Reduce viscosity for superfluid state (avoid inplace operation)
        adjusted_viscosity = properties[:, 2:3] * (1 - 0.9 * below_critical)
        properties = torch.cat([
            properties[:, 0:2],
            adjusted_viscosity,
            properties[:, 3:4]
        ], dim=1)
        
        return properties
    
    def compute_loss(
        self, 
        pred: torch.Tensor, 
        target: torch.Tensor, 
        x: torch.Tensor
    ) -> torch.Tensor:
        """Loss with superfluid constraints."""
        mse_loss = F.mse_loss(pred, target)
        
        rho = pred[:, 0:1]
        K = pred[:, 1:2]
        eta = pred[:, 2:3]
        
        # Wave speed constraint
        predicted_c = torch.sqrt(K / (rho + self.cfg.eps))
        measured_c = x[:, 2:3]
        physics_reg = F.mse_loss(predicted_c, measured_c)
        
        # Landau criterion: v_critical should be reasonable
        landau_reg = F.mse_loss(self.v_critical, torch.ones_like(self.v_critical) * 0.5)
        
        # Low viscosity constraint for superfluid
        viscosity_reg = torch.mean(F.relu(eta - 0.5))
        
        total_loss = mse_loss + 0.1 * physics_reg + 0.01 * landau_reg + 0.05 * viscosity_reg
        return total_loss
    
    def get_model_name(self) -> str:
        return "SuperfluidVacuumTheory"


class QuantumVacuumAether(BaseAetherModel):
    """
    Quantum Vacuum as Modern Aether.
    
    Key features:
    - Vacuum expectation value (VEV)
    - Zero-point energy scale
    - Renormalization group flow
    - Vacuum polarization corrections
    """
    
    def __init__(self, cfg: config.Config):
        super().__init__(cfg)
        
        # Vacuum expectation value (Higgs VEV scale, normalized)
        self.vev = nn.Parameter(torch.tensor(1.0))
        
        # Zero-point energy scale
        self.zpe_scale = nn.Parameter(torch.tensor(1.0))
        
        # Renormalization group flow network
        self.rg_flow_net = nn.Sequential(
            nn.Linear(self.hidden_dim // 2 + 2, self.hidden_dim // 4),
            nn.LayerNorm(self.hidden_dim // 4),
            nn.GELU(),
            nn.Linear(self.hidden_dim // 4, 2)  # Running couplings
        )
        
        # Vacuum polarization correction
        self.polarization_net = nn.Sequential(
            nn.Linear(self.hidden_dim // 2, self.hidden_dim // 2),
            nn.LayerNorm(self.hidden_dim // 2),
            nn.GELU()
        )
        
        # QFT head
        self.qft_head = nn.Linear(self.hidden_dim // 2 + 2, self.output_dim)
        del self.property_head
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass with quantum vacuum effects."""
        h = self.encoder(x)
        self.last_features = h.detach()
        
        # Vacuum polarization
        h_polarized = self.polarization_net(h)
        h_combined = h + 0.1 * h_polarized
        
        # Energy scale from features (index 3)
        energy_scale = x[:, 3:4]
        
        # RG flow
        batch_size = x.shape[0]
        zpe_expanded = self.zpe_scale.expand(batch_size, 1)
        rg_input = torch.cat([h_combined, energy_scale, zpe_expanded], dim=1)
        running_couplings = self.rg_flow_net(rg_input)
        
        # Final prediction
        head_input = torch.cat([h_combined, running_couplings], dim=1)
        raw_properties = self.qft_head(head_input)
        properties = F.softplus(raw_properties)
        
        # Vacuum energy contribution to density
        # rho_vacuum ~ (zpe_scale * vev)^4 in natural units (avoid inplace operation)
        vacuum_rho = (self.zpe_scale * self.vev) ** 4
        adjusted_density = properties[:, 0:1] + vacuum_rho.unsqueeze(0)
        properties = torch.cat([adjusted_density, properties[:, 1:4]], dim=1)
        
        return properties
    
    def compute_loss(
        self, 
        pred: torch.Tensor, 
        target: torch.Tensor, 
        x: torch.Tensor
    ) -> torch.Tensor:
        """Loss with Casimir effect constraint."""
        mse_loss = F.mse_loss(pred, target)
        
        rho = pred[:, 0:1]
        K = pred[:, 1:2]
        eps = pred[:, 3:4]
        
        # Wave speed constraint
        predicted_c = torch.sqrt(K / (rho + self.cfg.eps))
        measured_c = x[:, 2:3]
        physics_reg = F.mse_loss(predicted_c, measured_c)
        
        # Casimir effect: vacuum energy ~ 1/d^4
        # Feature 4 is separation distance
        distance = torch.abs(x[:, 4:5]) + self.cfg.eps
        expected_rho_scaling = 1.0 / (distance ** 4 + self.cfg.eps)
        
        # Normalize for comparison
        rho_normalized = rho / (rho.mean() + self.cfg.eps)
        expected_normalized = expected_rho_scaling / (expected_rho_scaling.mean() + self.cfg.eps)
        casimir_reg = F.mse_loss(rho_normalized, expected_normalized)
        
        # Permittivity constraint
        eps_reg = torch.mean(F.relu(-eps + 0.1))
        
        total_loss = mse_loss + 0.1 * physics_reg + 0.05 * casimir_reg + 0.01 * eps_reg
        return total_loss
    
    def get_model_name(self) -> str:
        return "QuantumVacuumAether"


class NoAetherComponent(BaseAetherModel):
    """
    Ablation: No explicit aether component.
    
    Tests necessity of aether assumption by using fixed negligible density.
    """
    
    def __init__(self, cfg: config.Config):
        super().__init__(cfg)
        
        # Fixed (non-learnable) negligible density
        self.register_buffer('fixed_density', torch.tensor([0.001]))
        
        # Modified head: only predict 3 properties [K, eta, eps]
        self.ablation_head = nn.Linear(self.hidden_dim // 2, 3)
        del self.property_head
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass without learnable aether density."""
        h = self.encoder(x)
        self.last_features = h.detach()
        
        # Predict only K, eta, eps
        raw_properties_3 = self.ablation_head(h)
        properties_3 = F.softplus(raw_properties_3)
        
        # Prepend fixed negligible density
        batch_size = x.shape[0]
        fixed_density_expanded = self.fixed_density.expand(batch_size, 1)
        properties = torch.cat([fixed_density_expanded, properties_3], dim=1)
        
        return properties
    
    def compute_loss(
        self, 
        pred: torch.Tensor, 
        target: torch.Tensor, 
        x: torch.Tensor
    ) -> torch.Tensor:
        """Loss computed only on K, eta, eps."""
        # Only compute loss on non-density properties
        pred_3 = pred[:, 1:4]
        target_3 = target[:, 1:4]
        mse_loss = F.mse_loss(pred_3, target_3)
        
        K = pred[:, 1:2]
        
        # With fixed density, c prediction is constrained
        predicted_c = torch.sqrt(K / (self.fixed_density + self.cfg.eps))
        measured_c = x[:, 2:3]
        physics_reg = F.mse_loss(predicted_c, measured_c)
        
        total_loss = mse_loss + 0.1 * physics_reg
        return total_loss
    
    def get_model_name(self) -> str:
        return "NoAetherComponent"


class SimplifiedAether(BaseAetherModel):
    """
    Ablation: Simplified constant aether properties.
    
    Uses global constant properties with only small spatial variations.
    """
    
    def __init__(self, cfg: config.Config):
        super().__init__(cfg)
        
        # Global aether property vector
        self.global_aether = nn.Parameter(torch.ones(4))
        
        # Small variation network
        self.variation_net = nn.Sequential(
            nn.Linear(self.hidden_dim // 2, 32),
            nn.LayerNorm(32),
            nn.GELU(),
            nn.Linear(32, 4)
        )
        
        # Variation scale (small)
        self.variation_scale = nn.Parameter(torch.tensor(0.1))
        
        del self.property_head
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass with nearly constant properties."""
        h = self.encoder(x)
        self.last_features = h.detach()
        
        # Compute small variations
        variations = self.variation_net(h)
        scaled_variations = variations * torch.abs(self.variation_scale)
        
        # Global properties + small variations
        batch_size = x.shape[0]
        global_expanded = self.global_aether.unsqueeze(0).expand(batch_size, -1)
        properties = F.softplus(global_expanded + scaled_variations)
        
        return properties
    
    def compute_loss(
        self, 
        pred: torch.Tensor, 
        target: torch.Tensor, 
        x: torch.Tensor
    ) -> torch.Tensor:
        """Loss with variation penalty."""
        mse_loss = F.mse_loss(pred, target)
        
        rho = pred[:, 0:1]
        K = pred[:, 1:2]
        
        # Physics constraint
        predicted_c = torch.sqrt(K / (rho + self.cfg.eps))
        measured_c = x[:, 2:3]
        physics_reg = F.mse_loss(predicted_c, measured_c)
        
        # Penalize large variations (encourage constant properties)
        global_expanded = self.global_aether.unsqueeze(0).expand(pred.shape[0], -1)
        variations = pred - F.softplus(global_expanded)
        variation_reg = torch.mean(variations ** 2)
        
        total_loss = mse_loss + 0.1 * physics_reg + 0.1 * variation_reg
        return total_loss
    
    def get_model_name(self) -> str:
        return "SimplifiedAether"


def get_model(model_name: str, cfg: config.Config) -> BaseAetherModel:
    """Factory function to create models by name."""
    model_map = {
        'LorentzEtherTheory': LorentzEtherTheory,
        'DiracAetherModel': DiracAetherModel,
        'SuperfluidVacuumTheory': SuperfluidVacuumTheory,
        'QuantumVacuumAether': QuantumVacuumAether,
        'NoAetherComponent': NoAetherComponent,
        'SimplifiedAether': SimplifiedAether,
        'BaseAetherModel': BaseAetherModel
    }
    
    if model_name not in model_map:
        raise ValueError(f"Unknown model: {model_name}. Available: {list(model_map.keys())}")
    
    return model_map[model_name](cfg)