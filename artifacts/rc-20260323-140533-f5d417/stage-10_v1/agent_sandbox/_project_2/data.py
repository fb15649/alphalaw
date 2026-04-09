"""
Dataset generation for electromagnetic, gravitational, and quantum vacuum measurements.
Generates synthetic data based on Maxwell equations with aether terms.
"""
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from typing import Tuple
import config


def generate_synthetic_aether_data(
    n_samples: int, 
    cfg: config.Config, 
    seed: int = None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate synthetic data based on Maxwell equations with aether term.
    
    Physics model:
    - c = 1/sqrt(epsilon_0 * mu_0) where epsilon_0 = epsilon_aether
    - Lorentz contraction: L' = L * sqrt(1 - v^2/c^2)
    - Wave equation with aether drag term
    - Damping from aether viscosity: damping = eta_aether * k^2
    
    Input features [12]:
    0: wavelength (normalized)
    1: frequency (normalized)
    2: measured wave velocity
    3: energy scale
    4: separation distance (for Casimir-like effects)
    5: aether drift anisotropy
    6-8: position coordinates (spacetime)
    9: local aether density variation
    10: temperature proxy (for superfluid effects)
    11: polarization state
    
    Output targets [4]:
    0: rho_aether (density)
    1: K_aether (elasticity/bulk modulus)
    2: eta_aether (viscosity)
    3: eps_aether (permittivity)
    """
    if seed is not None:
        np.random.seed(seed)
    
    features = np.zeros((n_samples, 12), dtype=np.float32)
    targets = np.zeros((n_samples, 4), dtype=np.float32)
    
    for i in range(n_samples):
        # Generate aether velocity vector (small fraction of c)
        v_aether = np.random.uniform(0, 0.01, 3)  # 3D aether drift
        v_aether_norm = np.linalg.norm(v_aether)
        
        # Base aether properties with spatial variation
        spatial_factor = 1.0 + 0.1 * np.sin(i * 0.01)  # Slow spatial variation
        
        rho_aether = cfg.rho_aether_base * spatial_factor * (1 + 0.1 * np.random.randn())
        K_aether = cfg.K_aether_base * spatial_factor * (1 + 0.05 * np.random.randn())
        eta_aether = cfg.eta_aether_base * (1 + 0.2 * np.random.randn())
        eps_aether = cfg.eps_aether_base * (1 + 0.05 * np.random.randn())
        
        # Ensure positive values
        rho_aether = max(rho_aether, 0.1)
        K_aether = max(K_aether, 0.1)
        eta_aether = max(eta_aether, 0.001)
        eps_aether = max(eps_aether, 0.5)
        
        # Compute wave velocity from aether properties
        # c = sqrt(K / rho) for elastic medium
        c_base = np.sqrt(K_aether / rho_aether)
        
        # Aether drift effect on measured velocity (Lorentz-Fitzgerald)
        gamma = 1.0 / np.sqrt(1 - v_aether_norm**2 / cfg.c_normalized**2 + cfg.eps)
        
        # Effective permittivity modified by aether
        eps_eff = eps_aether * (1 + 0.01 * v_aether_norm)  # Small drift coupling
        
        # Wave velocity
        c_measured = c_base / np.sqrt(eps_eff) * gamma
        
        # Wavelength and frequency (related by c = lambda * f)
        wavelength = np.random.uniform(0.1, 10.0)
        frequency = c_measured / wavelength
        
        # Wave number for damping calculation
        k = 2 * np.pi / wavelength
        
        # Damping from aether viscosity
        damping = eta_aether * k**2
        
        # Energy scale (for quantum effects)
        energy_scale = np.random.uniform(0.1, 100.0)
        
        # Separation distance (for Casimir effect)
        separation = np.random.uniform(0.01, 1.0)
        
        # Aether drift anisotropy (direction-dependent c measurement)
        anisotropy = v_aether_norm / cfg.c_normalized
        
        # Position coordinates
        position = np.random.uniform(-1, 1, 3)
        
        # Local aether density variation
        local_density_var = 0.1 * np.random.randn()
        
        # Temperature proxy (for superfluid transition)
        temperature = np.random.uniform(0, 1)
        
        # Polarization state
        polarization = np.random.uniform(-1, 1)
        
        # Build feature vector
        features[i] = [
            wavelength,
            frequency,
            c_measured,
            energy_scale,
            separation,
            anisotropy,
            position[0],
            position[1],
            position[2],
            local_density_var,
            temperature,
            polarization
        ]
        
        # Build target vector
        targets[i] = [rho_aether, K_aether, eta_aether, eps_aether]
    
    # Normalize features to [-1, 1]
    feature_means = np.mean(features, axis=0)
    feature_stds = np.std(features, axis=0) + cfg.eps
    features = (features - feature_means) / feature_stds
    features = np.clip(features, -3, 3) / 3
    
    # Normalize targets (log scale for physical parameters)
    targets_log = np.log10(targets + cfg.eps)
    target_means = np.mean(targets_log, axis=0)
    target_stds = np.std(targets_log, axis=0) + cfg.eps
    targets_normalized = (targets_log - target_means) / target_stds
    
    # Store normalization parameters
    norm_params = {
        'feature_mean': feature_means,
        'feature_std': feature_stds,
        'target_mean': target_means,
        'target_std': target_stds
    }
    
    return features.astype(np.float32), targets_normalized.astype(np.float32), norm_params


class AetherDataset(Dataset):
    """PyTorch Dataset for aether property derivation."""
    
    def __init__(self, features: np.ndarray, targets: np.ndarray):
        self.features = torch.from_numpy(features)
        self.targets = torch.from_numpy(targets)
    
    def __len__(self) -> int:
        return len(self.features)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        return self.features[idx], self.targets[idx]


def get_dataloaders(
    cfg: config.Config, 
    seed: int = 0
) -> Tuple[DataLoader, DataLoader, DataLoader, dict]:
    """
    Create train, validation, and test dataloaders.
    
    Returns:
        train_loader, val_loader, test_loader, norm_params
    """
    # Generate training data
    train_features, train_targets, norm_params = generate_synthetic_aether_data(
        cfg.n_train_samples, cfg, seed=seed
    )
    
    # Generate validation data
    val_features, val_targets, _ = generate_synthetic_aether_data(
        cfg.n_val_samples, cfg, seed=seed + 1000
    )
    
    # Generate test data
    test_features, test_targets, _ = generate_synthetic_aether_data(
        cfg.n_test_samples, cfg, seed=seed + 2000
    )
    
    # Create datasets
    train_dataset = AetherDataset(train_features, train_targets)
    val_dataset = AetherDataset(val_features, val_targets)
    test_dataset = AetherDataset(test_features, test_targets)
    
    # Create dataloaders
    train_loader = DataLoader(
        train_dataset, batch_size=cfg.batch_size, shuffle=True
    )
    val_loader = DataLoader(
        val_dataset, batch_size=cfg.batch_size, shuffle=False
    )
    test_loader = DataLoader(
        test_dataset, batch_size=cfg.batch_size, shuffle=False
    )
    
    return train_loader, val_loader, test_loader, norm_params