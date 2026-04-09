"""Physics dataset loading for aether property inference."""

import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
from typing import Tuple, Dict, Optional

from experiment_config import AetherConfig

# Physical constants for data generation
SPEED_OF_LIGHT = 299792458.0  # m/s
VACUUM_PERMITTIVITY = 8.854187817e-12  # F/m
VACUUM_PERMEABILITY = 1.2566370614e-6  # H/m
PLANCK_CONSTANT = 6.62607015e-34  # J·s
PLANCK_REDUCED = 1.054571817e-34  # J·s

class AetherDataset(Dataset):
    """
    Dataset for aether property inference from EM wave observations.
    
    Observations contain EM wave properties: [wavelength, frequency, amplitude, 
    phase, polarization, intensity] of shape [N, 6].
    
    Theoretical predictions and measurement errors are of shape [N, 4] corresponding
    to [density, elasticity, viscosity, permittivity].
    """
    
    def __init__(
        self, 
        config: AetherConfig, 
        condition_type: str, 
        split: str = 'train'
    ):
        """
        Initialize the dataset with physics observations.
        
        Args:
            config: Configuration object containing hyperparameters
            condition_type: Type of physical condition/model being tested
            split: Data split - 'train', 'val', or 'test'
        """
        self.condition_type = condition_type
        self.config = config
        
        # Set random seed for reproducibility based on split
        split_seeds = {'train': 42, 'val': 123, 'test': 456}
        np.random.seed(split_seeds.get(split, 42))
        
        # Generate base number of samples
        n_total = 5000  # Total samples before splitting
        
        # Load observation data - EM wave properties
        # [wavelength, frequency, amplitude, phase, polarization, intensity]
        observations = self._load_em_wave_data(n_total)  # [N, 6]
        
        # Compute theoretical predictions based on condition type
        theoretical_predictions = self._compute_theoretical_baseline(
            observations, condition_type
        )  # [N, 4]
        
        # Load/generate experimental uncertainties
        measurement_errors = self._load_experimental_uncertainties(
            n_total, theoretical_predictions.shape[1]
        )  # [N, 4]
        
        # Split indices
        n_train = int(0.7 * n_total)
        n_val = int(0.15 * n_total)
        
        if split == 'train':
            start_idx, end_idx = 0, n_train
        elif split == 'val':
            start_idx, end_idx = n_train, n_train + n_val
        else:  # test
            start_idx, end_idx = n_train + n_val, n_total
        
        # Extract split data
        self.observations_raw = observations[start_idx:end_idx]
        self.theoretical_predictions = theoretical_predictions[start_idx:end_idx]
        self.measurement_errors = measurement_errors[start_idx:end_idx]
        
        # Apply log scaling to large-magnitude values in observations
        # Wavelength (index 0): typically 400-700nm for visible, log scale
        # Frequency (index 1): typically 4-8e14 Hz, log scale
        # Intensity (index 5): can span many orders, log scale
        self.observations_raw[:, 0] = np.log10(self.observations_raw[:, 0] + 1e-30)
        self.observations_raw[:, 1] = np.log10(self.observations_raw[:, 1] + 1e-30)
        self.observations_raw[:, 5] = np.log10(self.observations_raw[:, 5] + 1e-30)
        
        # Normalize observations: obs = (obs - mean) / std
        obs_mean = self.observations_raw.mean(axis=0)
        obs_std = self.observations_raw.std(axis=0) + 1e-8
        self.observations = (self.observations_raw - obs_mean) / obs_std
        
        # Store normalization stats for potential denormalization
        self.obs_mean = obs_mean
        self.obs_std = obs_std
        
        # Convert to tensors
        self.observations = torch.tensor(self.observations, dtype=torch.float32)
        self.theoretical_predictions = torch.tensor(
            self.theoretical_predictions, dtype=torch.float32
        )
        self.measurement_errors = torch.tensor(
            self.measurement_errors, dtype=torch.float32
        )
    
    def _load_em_wave_data(self, n_samples: int) -> np.ndarray:
        """
        Generate EM wave propagation data.
        
        Returns array of shape [N, 6] with columns:
        - wavelength (m)
        - frequency (Hz)
        - amplitude (V/m)
        - phase (rad)
        - polarization (unitless, -1 to 1)
        - intensity (W/m²)
        """
        # Wavelength: sample across EM spectrum (radio to UV)
        # Use log-uniform distribution to cover many orders of magnitude
        wavelengths = np.power(10, np.random.uniform(-6, -5, n_samples))  # 1µm to 10µm
        
        # Frequency: derived from c = λf
        frequencies = SPEED_OF_LIGHT / (wavelengths + 1e-30)
        
        # Amplitude: electric field amplitude (V/m)
        amplitudes = np.random.uniform(1e-3, 1e3, n_samples)
        
        # Phase: random phase [0, 2π)
        phases = np.random.uniform(0, 2 * np.pi, n_samples)
        
        # Polarization: linear (-1) to circular (1)
        polarization = np.random.uniform(-1, 1, n_samples)
        
        # Intensity: I ∝ E² (W/m²)
        intensities = 0.5 * VACUUM_PERMITTIVITY * SPEED_OF_LIGHT * amplitudes**2
        
        # Stack into observations array
        observations = np.stack([
            wavelengths,
            frequencies,
            amplitudes,
            phases,
            polarization,
            intensities
        ], axis=1)  # [N, 6]
        
        return observations
    
    def _compute_theoretical_baseline(
        self, 
        observations: np.ndarray, 
        condition_type: str
    ) -> np.ndarray:
        """
        Compute theoretical baseline predictions for aether properties.
        
        Args:
            observations: EM wave observations [N, 6]
            condition_type: Which theoretical model to use
            
        Returns:
            Theoretical predictions [N, 4] for [density, elasticity, viscosity, permittivity]
        """
        n_samples = observations.shape[0]
        
        # Base aether properties (theoretical priors)
        # These are modified based on the condition type
        base_density = 1e-6  # kg/m³ (very low density medium)
        base_elasticity = 1e11  # Pa (high elasticity for wave propagation)
        base_viscosity = 1e3  # Pa·s
        base_permittivity = VACUUM_PERMITTIVITY  # F/m
        
        # Extract relevant observation components
        wavelengths = observations[:, 0]
        frequencies = observations[:, 1]
        amplitudes = observations[:, 2]
        
        # Frequency-dependent modifications (dispersion relation effects)
        freq_factor = np.log10(frequencies + 1e-30) / 15.0  # Normalized log frequency
        
        # CRITICAL FIX: Initialize ALL output variables BEFORE conditional branches
        # to prevent UnboundLocalError regardless of which branch is taken
        density = base_density * np.ones(n_samples)
        elasticity = base_elasticity * np.ones(n_samples)
        viscosity = base_viscosity * np.ones(n_samples)
        permittivity = base_permittivity * np.ones(n_samples)
        
        # CRITICAL FIX: Initialize ALL intermediate variables used in branches
        # This ensures they are defined even if a branch is not taken
        v_sim = np.zeros(n_samples)
        gamma = np.ones(n_samples)
        h_bar = PLANCK_REDUCED
        
        if 'Lorentz' in condition_type:
            # Lorentz ether theory: properties depend on frame motion
            v_sim = np.random.uniform(0, 0.1, n_samples)  # Simulated velocities (fraction of c)
            gamma = 1.0 / np.sqrt(1.0 - v_sim**2 + 1e-30)
            
            density = base_density * gamma * (1 + 0.1 * freq_factor)
            elasticity = base_elasticity / gamma * (1 - 0.05 * freq_factor)
            viscosity = base_viscosity * (1 + 0.02 * freq_factor)
            permittivity = base_permittivity * (1 + 0.001 * v_sim)
            
        elif 'Dirac' in condition_type:
            # Dirac 1951 aether: quantum vacuum properties
            # h_bar already initialized above to PLANCK_REDUCED
            
            # Quantized density fluctuations
            density = base_density * (1 + h_bar * 1e34 * np.random.randn(n_samples) * 0.01)
            elasticity = base_elasticity * (1 + 0.1 * freq_factor)
            # Quantized viscosity
            viscosity = base_viscosity * h_bar * 1e34 * (1 + 0.05 * freq_factor)
            permittivity = base_permittivity * (1 + 0.01 * freq_factor)
            
        elif 'Maxwell' in condition_type:
            # Standard Maxwell: no aether medium
            density = np.zeros(n_samples)
            elasticity = np.zeros(n_samples)
            viscosity = np.zeros(n_samples)
            # Only permittivity is meaningful
            permittivity = base_permittivity * np.ones(n_samples)
            
        elif 'Superfluid' in condition_type:
            # Superfluid vacuum: zero viscosity
            density = base_density * (1 + 0.15 * freq_factor)
            elasticity = base_elasticity * (1 + 0.1 * freq_factor)
            viscosity = np.zeros(n_samples)  # Zero by definition
            permittivity = base_permittivity * (1 + 0.005 * freq_factor)
            
        elif 'Linearized' in condition_type:
            # Linearized model: simple linear relationship
            density = base_density * (1 + 0.1 * freq_factor)
            elasticity = base_elasticity * (1 + 0.1 * freq_factor)
            viscosity = base_viscosity * (1 + 0.1 * freq_factor)
            permittivity = base_permittivity * (1 + 0.01 * freq_factor)
            
        elif 'NoViscosity' in condition_type:
            # Ablation: no viscosity component
            density = base_density * (1 + 0.1 * freq_factor)
            elasticity = base_elasticity * (1 + 0.1 * freq_factor)
            viscosity = np.zeros(n_samples)
            permittivity = base_permittivity * (1 + 0.01 * freq_factor)
            
        else:
            # Default: base properties with small variations
            density = base_density * (1 + 0.1 * np.random.randn(n_samples))
            elasticity = base_elasticity * (1 + 0.1 * np.random.randn(n_samples))
            viscosity = base_viscosity * (1 + 0.1 * np.random.randn(n_samples))
            permittivity = base_permittivity * (1 + 0.01 * np.random.randn(n_samples))
        
        # Stack into predictions array
        predictions = np.stack([
            density,
            elasticity,
            viscosity,
            permittivity
        ], axis=1)  # [N, 4]
        
        return predictions
    
    def _load_experimental_uncertainties(
        self, 
        n_samples: int, 
        n_properties: int
    ) -> np.ndarray:
        """
        Generate experimental measurement uncertainties.
        
        These represent realistic experimental errors in measuring
        aether properties.
        
        Returns:
            Error array of shape [N, 4]
        """
        # Relative uncertainties for each property
        # These represent typical experimental precision
        relative_errors = np.array([
            0.15,   # density: 15% relative error
            0.12,   # elasticity: 12% relative error
            0.20,   # viscosity: 20% relative error (hardest to measure)
            0.001,  # permittivity: 0.1% (very precise)
        ])
        
        # Base values for scaling
        base_values = np.array([1e-6, 1e11, 1e3, VACUUM_PERMITTIVITY])
        
        # Generate absolute errors
        errors = np.zeros((n_samples, n_properties))
        for i in range(n_properties):
            # Add some variation to the errors themselves
            error_scale = relative_errors[i] * base_values[i]
            errors[:, i] = error_scale * (1 + 0.2 * np.random.randn(n_samples))
            errors[:, i] = np.abs(errors[:, i])  # Errors must be positive
        
        return errors
    
    def __len__(self) -> int:
        """Return the number of samples in the dataset."""
        return len(self.observations)
    
    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        """
        Get a single sample from the dataset.
        
        Args:
            idx: Sample index
            
        Returns:
            Dictionary containing:
                - 'obs': Observation tensor [obs_dim]
                - 'target': Theoretical prediction tensor [pred_dim]
                - 'error': Measurement error tensor [pred_dim]
        """
        obs = self.observations[idx]  # [obs_dim]
        pred = self.theoretical_predictions[idx]  # [pred_dim]
        err = self.measurement_errors[idx]  # [pred_dim]
        
        return {
            'obs': obs,
            'target': pred,
            'error': err
        }

def get_dataloaders(
    config: AetherConfig, 
    condition_type: str
) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """
    Create train, validation, and test dataloaders.
    
    Args:
        config: Configuration object with hyperparameters
        condition_type: Type of physical condition/model
        
    Returns:
        Tuple of (train_loader, val_loader, test_loader)
    """
    # Create datasets for each split
    train_dataset = AetherDataset(config, condition_type, split='train')
    val_dataset = AetherDataset(config, condition_type, split='val')
    test_dataset = AetherDataset(config, condition_type, split='test')
    
    # Create dataloaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=config.batch_size,
        shuffle=True,
        num_workers=0,  # Avoid multiprocessing issues
        pin_memory=False
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=config.batch_size,
        shuffle=False,
        num_workers=0,
        pin_memory=False
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=config.batch_size,
        shuffle=False,
        num_workers=0,
        pin_memory=False
    )
    
    return train_loader, val_loader, test_loader

def generate_synthetic_observations(
    n_samples: int, 
    aether_params: torch.Tensor
) -> torch.Tensor:
    """
    Generate synthetic EM wave observations based on aether parameters.
    
    This function simulates what observations would look like given
    specific aether properties, useful for inverse modeling validation.
    
    Args:
        n_samples: Number of observation samples to generate
        aether_params: Aether property parameters [4] or [B, 4]
                      [density, elasticity, viscosity, permittivity]
                      
    Returns:
        Observation tensor of shape [N, 6]
    """
    # CRITICAL FIX: Initialize params BEFORE any conditional logic
    # to guarantee definition on all code paths (prevents UnboundLocalError)
    params = aether_params[:1].expand(n_samples, -1)  # Default: expand first element
    
    if aether_params.dim() == 1:
        params = aether_params.unsqueeze(0).expand(n_samples, -1)
    elif aether_params.shape[0] == n_samples:
        params = aether_params
    # else: use default value (already set above)
    
    # Now params is guaranteed to be defined with shape [n_samples, 4]
    
    # Extract aether properties
    density = params[:, 0]  # kg/m³
    elasticity = params[:, 1]  # Pa
    viscosity = params[:, 2]  # Pa·s
    permittivity = params[:, 3]  # F/m
    
    # Generate EM wave propagation data
    # Base wavelength distribution (infrared to ultraviolet)
    wavelengths = torch.pow(10.0, torch.linspace(-6, -5, n_samples))
    wavelengths = wavelengths[torch.randperm(n_samples)]
    
    # Frequency from dispersion relation in aether medium
    # Modified by permittivity and permeability
    effective_c = 1.0 / torch.sqrt(permittivity * VACUUM_PERMEABILITY + 1e-30)
    frequencies = effective_c / (wavelengths + 1e-30)
    
    # Amplitude: affected by aether density (attenuation)
    base_amplitude = torch.rand(n_samples) * 100 + 1
    attenuation = torch.exp(-density * 1e6 * wavelengths)  # Simple attenuation model
    amplitudes = base_amplitude * attenuation
    
    # Phase: affected by viscosity (dispersion)
    base_phase = torch.rand(n_samples) * 2 * np.pi
    phase_shift = viscosity * 1e-4 * frequencies / (SPEED_OF_LIGHT + 1e-30)
    phases = base_phase + phase_shift
    
    # Polarization: affected by elasticity (birefringence effect)
    base_polarization = torch.rand(n_samples) * 2 - 1
    birefringence = torch.tanh(elasticity / 1e11) * 0.1
    polarization = base_polarization * (1 + birefringence)
    polarization = torch.clamp(polarization, -1, 1)
    
    # Intensity: I ∝ E² with aether correction
    intensities = 0.5 * permittivity * effective_c * amplitudes**2
    
    # Apply Lorentz transformation for ether frame
    # Simulate frame velocity
    v_frame = torch.rand(n_samples) * 0.01  # Up to 1% of c
    gamma = 1.0 / torch.sqrt(1.0 - v_frame**2 + 1e-30)
    
    # Transform observations (simplified Lorentz transformation)
    wavelengths = wavelengths / gamma  # Length contraction
    frequencies = frequencies * gamma  # Time dilation
    
    # Add Gaussian noise with experimental uncertainties
    noise_scale = torch.tensor([0.01, 0.01, 0.05, 0.1, 0.05, 0.05])
    noise = torch.randn(n_samples, 6) * noise_scale
    
    # Stack observations
    observations = torch.stack([
        wavelengths,
        frequencies,
        amplitudes,
        phases,
        polarization,
        intensities
    ], dim=1)  # [N, 6]
    
    # Add noise
    observations = observations + noise
    
    return observations

def get_dataset_statistics(condition_type: str) -> Dict[str, float]:
    """
    Get statistical properties of the dataset for a given condition.
    
    This is useful for initializing models with appropriate scales.
    
    Args:
        condition_type: Type of physical condition/model
        
    Returns:
        Dictionary with mean and std for each property
    """
    config = AetherConfig()
    dataset = AetherDataset(config, condition_type, split='train')
    
    targets = dataset.theoretical_predictions.numpy()
    
    stats = {
        'density_mean': targets[:, 0].mean(),
        'density_std': targets[:, 0].std(),
        'elasticity_mean': targets[:, 1].mean(),
        'elasticity_std': targets[:, 1].std(),
        'viscosity_mean': targets[:, 2].mean(),
        'viscosity_std': targets[:, 2].std(),
        'permittivity_mean': targets[:, 3].mean(),
        'permittivity_std': targets[:, 3].std(),
    }
    
    return stats