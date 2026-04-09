"""
Main experiment entry point for Aether Physical Properties Derivation.

EXPERIMENT DESIGN:
==================
(a) Dataset: Synthetic electromagnetic/gravity measurements generated from
    Maxwell equations with aether terms. Features include wavelength, frequency,
    velocity, energy scale, separation distance, aether drift anisotropy, position
    coordinates, local density variation, temperature proxy, polarization state.
    Loaded via generate_synthetic_aether_data() with seed-controlled randomness.

(b) Data characteristics: 2000 train, 400 val, 400 test samples per seed.
    Normalized features [-1, 1], log-normalized targets for physical parameters.
    Noise level: 2% Gaussian noise added to measurements.

(c) Model architecture: BaseAetherModel with encoder (3 linear layers, LayerNorm,
    GELU) producing hidden_dim//2 features, property head predicting 4 outputs.
    Variants add physics-specific components (Lorentz contraction, variable density,
    phonon networks, RG flow, etc.).

(d) Training protocol: AdamW optimizer (lr=0.001, weight_decay=1e-5),
    CosineAnnealingLR scheduler, 15 epochs, batch_size=64,
    gradient clipping (max_norm=1.0).

(e) Evaluation protocol: 3 seeds [0, 1, 2] per condition, train/val/test split,
    primary_metric = 1 - mean_relative_physics_error (c_consistency),
    secondary_metric = 1/(1 + log_MAE) (parameter accuracy).

CONDITIONS:
===========
1. LorentzEtherTheory: Classical LET with Fitzgerald contraction, aether drift
2. DiracAetherModel: Dirac 1951 model with variable density, large numbers
3. SuperfluidVacuumTheory: Superfluid vacuum with phonon excitations (PROPOSED)
4. QuantumVacuumAether: QFT vacuum with polarization, RG flow
5. NoAetherComponent: Ablation - fixed negligible density (without_key_component)
6. SimplifiedAether: Ablation - constant global properties (simplified_version)
"""
import os
import sys
import time
import json
import random
import numpy as np
import torch
from typing import Dict, List, Any

# Import experiment modules
import config
import data
import models
import training

# Try to import experiment harness
try:
    from experiment_harness import ExperimentHarness
    HAS_HARNESS = True
except ImportError:
    HAS_HARNESS = False
    print("WARNING: experiment_harness not available, using fallback")

# Hyperparameters dictionary (MANDATORY)
HYPERPARAMETERS = {
    'learning_rate': 0.001,
    'batch_size': 64,
    'num_epochs': 15,
    'hidden_dim': 128,
    'weight_decay': 1e-5,
    'seeds': [0, 1, 2],
    'n_train_samples': 2000,
    'n_val_samples': 400,
    'n_test_samples': 400,
    'noise_level': 0.02,
    'input_dim': 12,
    'output_dim': 4,
    'physics_reg_weight': 0.1,
    'gradient_clip_norm': 1.0
}

# Time budget
TIME_BUDGET_SECONDS = 300


def set_seed(seed: int) -> None:
    """Set random seeds for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    if torch.backends.mps.is_available():
        torch.mps.manual_seed(seed)


def get_condition_names() -> List[str]:
    """Return list of all condition names."""
    return [
        'LorentzEtherTheory',      # Baseline 1
        'DiracAetherModel',        # Baseline 2
        'SuperfluidVacuumTheory',  # Proposed
        'QuantumVacuumAether',     # Variant
        'NoAetherComponent',       # Ablation: without_key_component
        'SimplifiedAether'         # Ablation: simplified_version
    ]


def run_single_condition(
    condition_name: str,
    cfg: config.Config,
    seed: int,
    device: torch.device
) -> Dict[str, float]:
    """
    Run a single condition with a single seed.
    
    Returns dict with metrics.
    """
    set_seed(seed)
    
    # Create model
    model = models.get_model(condition_name, cfg)
    model = model.to(device)
    
    # Get data loaders
    train_loader, val_loader, test_loader, _ = data.get_dataloaders(cfg, seed=seed)
    
    # Create trainer
    trainer = training.AetherTrainer(model, cfg, device)
    
    # Train
    history = trainer.fit(train_loader, val_loader)
    
    # Compute metrics
    primary = training.compute_primary_metric(model, test_loader, device, cfg)
    secondary = training.compute_secondary_metric(model, test_loader, device, cfg)
    
    return {
        'primary_metric': primary,
        'secondary_metric': secondary,
        'final_train_loss': history['train_loss'][-1] if history['train_loss'] else 0.0,
        'final_val_loss': history['val_loss'][-1] if history['val_loss'] else 0.0
    }


def verify_ablations_differ(cfg: config.Config, device: torch.device):
    """Verify that ablation models produce different outputs."""
    set_seed(42)
    
    # Create dummy input
    dummy_input = torch.randn(4, cfg.input_dim).to(device)
    
    model_names = get_condition_names()
    outputs = {}
    
    for name in model_names:
        model = models.get_model(name, cfg).to(device)
        model.eval()
        with torch.no_grad():
            out = model(dummy_input)
            outputs[name] = out.cpu().numpy()
    
    # Check that outputs differ
    print("ABLATION_CHECK:")
    for i, name1 in enumerate(model_names):
        for name2 in model_names[i+1:]:
            diff = np.mean(np.abs(outputs[name1] - outputs[name2]))
            differ = diff > 0.001
            print(f"  {name1} vs {name2}: outputs_differ={differ} (mean_diff={diff:.4f})")


def estimate_runtime(cfg: config.Config, device: torch.device) -> float:
    """Estimate total runtime by running a pilot."""
    print("Running pilot to estimate runtime...")
    
    start = time.time()
    
    # Run one condition with one seed
    set_seed(0)
    model = models.get_model('BaseAetherModel', cfg).to(device)
    train_loader, val_loader, test_loader, _ = data.get_dataloaders(cfg, seed=0)
    trainer = training.AetherTrainer(model, cfg, device)
    
    # Run 3 epochs as pilot
    cfg_pilot = config.Config()
    cfg_pilot.epochs = 3
    trainer.cfg = cfg_pilot
    
    for _ in range(3):
        trainer.train_one_epoch(train_loader)
        trainer.evaluate(val_loader)
    
    elapsed = time.time() - start
    
    # Extrapolate: 3 epochs -> 15 epochs, 1 seed -> 3 seeds, 1 condition -> 6 conditions
    estimated_per_run = elapsed / 3 * cfg.epochs  # Full epochs
    estimated_total = estimated_per_run * len(cfg.seeds) * len(get_condition_names())
    
    print(f"Pilot time (3 epochs): {elapsed:.2f}s")
    print(f"Estimated per run: {estimated_per_run:.2f}s")
    print(f"Estimated total: {estimated_total:.2f}s")
    
    return estimated_total


def main():
    """Main entry point."""
    # Print metric definitions
    print("=" * 70)
    print("AETHER PHYSICAL PROPERTIES DERIVATION EXPERIMENT")
    print("=" * 70)
    print()
    print("METRIC_DEF: primary_metric | direction=higher | desc=1 - mean_relative_physics_error")
    print("  Formula: 1 - mean(|c_predicted - c_measured| / |c_measured|)")
    print("  Measures: Physics consistency - how well predicted c matches measured c")
    print()
    print("METRIC_DEF: secondary_metric | direction=higher | desc=1/(1 + log_MAE)")
    print("  Formula: 1 / (1 + mean(|log10(pred) - log10(target)|))")
    print("  Measures: Parameter accuracy in log scale (physical parameters span orders)")
    print()
    
    # Configuration
    cfg = config.Config()
    
    # Override from HYPERPARAMETERS
    cfg.epochs = HYPERPARAMETERS['num_epochs']
    cfg.hidden_dim = HYPERPARAMETERS['hidden_dim']
    cfg.lr = HYPERPARAMETERS['learning_rate']
    cfg.batch_size = HYPERPARAMETERS['batch_size']
    cfg.seeds = HYPERPARAMETERS['seeds']
    
    # Device
    if torch.backends.mps.is_available():
        device = torch.device('mps')
    elif torch.cuda.is_available():
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')
    
    print(f"Device: {device}")
    print(f"Seeds: {cfg.seeds}")
    print(f"Epochs: {cfg.epochs}")
    print(f"Hidden dim: {cfg.hidden_dim}")
    print()
    
    # Register conditions
    conditions = get_condition_names()
    print(f"REGISTERED_CONDITIONS: {', '.join(conditions)}")
    print()
    
    # Verify ablations
    verify_ablations_differ(cfg, device)
    print()
    
    # Estimate runtime
    estimated_time = estimate_runtime(cfg, device)
    print(f"TIME_ESTIMATE: {estimated_time:.1f}s")
    print()
    
    # Initialize harness if available
    if HAS_HARNESS:
        harness = ExperimentHarness(time_budget=TIME_BUDGET_SECONDS)
    else:
        harness = None
    
    # Results storage
    all_results: Dict[str, Dict[str, List[float]]] = {
        cond: {'primary': [], 'secondary': []} 
        for cond in conditions
    }
    
    # Track failures
    failures: Dict[str, List[int]] = {cond: [] for cond in conditions}
    
    # Start timing
    start_time = time.time()
    
    # Run all conditions
    for cond_idx, condition in enumerate(conditions):
        print()
        print("=" * 60)
        print(f"CONDITION: {condition} ({cond_idx + 1}/{len(conditions)})")
        print("=" * 60)
        
        for seed_idx, seed in enumerate(cfg.seeds):
            # Check time budget
            elapsed = time.time() - start_time
            if elapsed > TIME_BUDGET_SECONDS * 0.85:
                print(f"TIME_BUDGET_WARNING: {elapsed/TIME_BUDGET_SECONDS*100:.1f}% used, stopping early")
                break
            
            # Check harness
            if harness and harness.should_stop():
                print("Harness signaled stop")
                break
            
            print(f"  Seed {seed_idx + 1}/{len(cfg.seeds)}: {seed}")
            
            try:
                result = run_single_condition(condition, cfg, seed, device)
                
                # Check for valid values
                primary = result['primary_metric']
                secondary = result['secondary_metric']
                
                if np.isnan(primary) or np.isinf(primary):
                    print(f"    SKIP: Invalid primary_metric")
                    failures[condition].append(seed)
                    continue
                
                if harness and not harness.check_value(primary, 'primary_metric'):
                    print(f"    SKIP: Harness rejected value")
                    failures[condition].append(seed)
                    continue
                
                all_results[condition]['primary'].append(primary)
                all_results[condition]['secondary'].append(secondary)
                
                print(f"    primary_metric: {primary:.6f}")
                print(f"    secondary_metric: {secondary:.6f}")
                print(f"    final_train_loss: {result['final_train_loss']:.6f}")
                print(f"    final_val_loss: {result['final_val_loss']:.6f}")
                
                if harness:
                    harness.report_metric('primary_metric', primary)
                    harness.report_metric('secondary_metric', secondary)
                    
            except Exception as e:
                print(f"    CONDITION_FAILED: {condition} seed={seed} error={str(e)}")
                failures[condition].append(seed)
                continue
        
        # Check time budget after each condition
        if time.time() - start_time > TIME_BUDGET_SECONDS * 0.9:
            print("TIME_BUDGET_EXCEEDED: Stopping after current condition")
            break
    
    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"{'Condition':<25} {'Primary (mean±std)':<25} {'Secondary (mean±std)':<25}")
    print("-" * 75)
    
    for condition in conditions:
        primary_vals = all_results[condition]['primary']
        secondary_vals = all_results[condition]['secondary']
        
        if len(primary_vals) > 0:
            primary_mean = np.mean(primary_vals)
            primary_std = np.std(primary_vals)
            secondary_mean = np.mean(secondary_vals)
            secondary_std = np.std(secondary_vals)
            
            print(f"{condition:<25} {primary_mean:.4f}±{primary_std:.4f}       {secondary_mean:.4f}±{secondary_std:.4f}")
        else:
            print(f"{condition:<25} NO_VALID_RESULTS")
    
    print()
    
    # Print failure summary
    total_failures = sum(len(v) for v in failures.values())
    if total_failures > 0:
        print("FAILURE SUMMARY:")
        for cond, seeds in failures.items():
            if seeds:
                print(f"  {cond}: failed seeds {seeds}")
        print()
    
    # Print summary line for automated parsing
    summary_parts = []
    for condition in conditions:
        vals = all_results[condition]['primary']
        if vals:
            summary_parts.append(f"{condition}={np.mean(vals):.4f}")
        else:
            summary_parts.append(f"{condition}=N/A")
    print(f"SUMMARY: {', '.join(summary_parts)}")
    
    # Compute paired statistics (SuperfluidVacuumTheory vs LorentzEtherTheory)
    proposed = 'SuperfluidVacuumTheory'
    baseline = 'LorentzEtherTheory'
    
    proposed_vals = all_results[proposed]['primary']
    baseline_vals = all_results[baseline]['primary']
    
    if len(proposed_vals) > 0 and len(baseline_vals) > 0 and len(proposed_vals) == len(baseline_vals):
        diffs = [p - b for p, b in zip(proposed_vals, baseline_vals)]
        mean_diff = np.mean(diffs)
        std_diff = np.std(diffs)
        
        # Simple t-statistic
        if std_diff > 0:
            t_stat = mean_diff / (std_diff / np.sqrt(len(diffs)))
        else:
            t_stat = 0.0
        
        print()
        print(f"PAIRED: {proposed} vs {baseline}")
        print(f"  mean_diff: {mean_diff:.4f}")
        print(f"  std_diff: {std_diff:.4f}")
        print(f"  t_stat: {t_stat:.4f}")
    
    # Total time
    total_time = time.time() - start_time
    print()
    print(f"Total time: {total_time:.2f}s ({total_time/60:.2f} minutes)")
    
    # Save results
    results_output = {
        'hyperparameters': HYPERPARAMETERS,
        'metrics': {
            cond: {
                'primary_mean': float(np.mean(vals['primary'])) if vals['primary'] else None,
                'primary_std': float(np.std(vals['primary'])) if vals['primary'] else None,
                'secondary_mean': float(np.mean(vals['secondary'])) if vals['secondary'] else None,
                'secondary_std': float(np.std(vals['secondary'])) if vals['secondary'] else None,
                'primary_values': [float(v) for v in vals['primary']],
                'secondary_values': [float(v) for v in vals['secondary']]
            }
            for cond, vals in all_results.items()
        },
        'failures': failures,
        'total_time_seconds': total_time
    }
    
    with open('results.json', 'w') as f:
        json.dump(results_output, f, indent=2)
    
    print("Results saved to results.json")
    
    # Finalize harness
    if harness:
        harness.finalize()
    
    # Check for degenerate metrics
    all_means = [np.mean(all_results[c]['primary']) for c in conditions if all_results[c]['primary']]
    if len(all_means) > 1 and np.std(all_means) < 0.001:
        print()
        print("WARNING: DEGENERATE_METRICS - all conditions have similar means")
        print("Consider adjusting task difficulty or model capacity")


if __name__ == "__main__":
    main()