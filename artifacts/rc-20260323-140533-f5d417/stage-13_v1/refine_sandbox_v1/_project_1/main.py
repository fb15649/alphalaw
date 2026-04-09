"""Main experiment orchestration for aether property derivation."""

import torch
import numpy as np
from typing import Dict, List, Any, Type
import time

from experiment_config import AetherConfig
from data import get_dataloaders
from models import (
    BaseAetherModel,
    LorentzEtherModel,
    DiracAetherModel,
    MaxwellBaseline,
    SuperfluidVacuumModel,
    LinearizedAetherModel,
    NoViscosityAetherModel
)
from training import Trainer
from experiment_harness import ExperimentHarness

# Define experiment conditions - baseline models
BASELINE_MODELS: Dict[str, Type[torch.nn.Module]] = {
    'Proving_baseline_1': MaxwellBaseline,
    'Proving_baseline_2': LinearizedAetherModel,
}

# Define proposed methods
PROPOSED_MODELS: Dict[str, Type[torch.nn.Module]] = {
    'Proving_proposed': LorentzEtherModel,
    'Proving_variant': DiracAetherModel,
}

# Define ablation models
ABLATION_MODELS: Dict[str, Type[torch.nn.Module]] = {
    'without_key_component': NoViscosityAetherModel,
    'simplified_version': SuperfluidVacuumModel,
}

def run_single_experiment(
    config: AetherConfig,
    model_class: Type[torch.nn.Module],
    model_name: str,
    seed: int,
    harness: ExperimentHarness
) -> Dict[str, float]:
    """
    Run a single experiment with given configuration.
    
    Args:
        config: Configuration object
        model_class: Model class to instantiate
        model_name: Name of the model for logging
        seed: Random seed for reproducibility
        harness: Experiment harness for time budget management
        
    Returns:
        Dictionary with evaluation metrics
    """
    # Set random seeds for reproducibility
    torch.manual_seed(seed)
    np.random.seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    
    # Check time budget before starting
    if harness.should_stop():
        return {
            'loss': float('nan'),
            'primary_metric': float('nan'),
            'secondary_metric': float('nan')
        }
    
    # Create model
    model = model_class(config)
    
    # Get dataloaders - use model name as condition type for data generation
    train_loader, val_loader, test_loader = get_dataloaders(config, model_name)
    
    # Create trainer
    trainer = Trainer(model, config)
    
    # Train the model
    train_results = trainer.fit(train_loader, val_loader)
    
    # Check time budget after training
    if harness.should_stop():
        return {
            'loss': float('nan'),
            'primary_metric': float('nan'),
            'secondary_metric': float('nan')
        }
    
    # Evaluate on test set
    eval_results = trainer.evaluate(test_loader)
    
    # Report metrics to harness
    for metric_name, value in eval_results.items():
        if harness.check_value(value, f"{model_name}_{metric_name}"):
            harness.report_metric(f"{model_name}_{metric_name}", value)
    
    return eval_results

def run_multi_seed_experiment(
    config: AetherConfig,
    model_class: Type[torch.nn.Module],
    model_name: str,
    harness: ExperimentHarness
) -> Dict[str, Dict[str, float]]:
    """
    Run experiment across multiple seeds and aggregate results with statistics.
    
    Args:
        config: Configuration object
        model_class: Model class to instantiate
        model_name: Name of the model
        harness: Experiment harness for time budget management
        
    Returns:
        Dictionary with mean and std for each metric
    """
    results: Dict[str, List[float]] = {
        'primary_metric': [],
        'secondary_metric': [],
        'loss': []
    }
    
    for seed in config.seeds:
        # CRITICAL FIX: Print per-seed metrics with condition label
        print(f"    Running seed {seed}...")
        
        if harness.should_stop():
            print(f"    Time budget exceeded, stopping multi-seed run")
            break
        
        seed_results = run_single_experiment(
            config, model_class, model_name, seed, harness
        )
        
        # CRITICAL FIX: Print per-seed result with condition label
        primary_val = seed_results.get('primary_metric', float('nan'))
        print(f"    condition={model_name} seed={seed} primary_metric: {primary_val:.6f}")
        
        # Collect results
        for metric_name in results:
            if metric_name in seed_results:
                value = seed_results[metric_name]
                if not np.isnan(value):
                    results[metric_name].append(value)
    
    # Compute mean and std for each metric
    aggregated: Dict[str, Dict[str, float]] = {}
    for metric_name, values in results.items():
        if len(values) > 0:
            values_array = np.array(values)
            aggregated[metric_name] = {
                'mean': float(np.mean(values_array)),
                'std': float(np.std(values_array)) if len(values_array) > 1 else 0.0,
                'min': float(np.min(values_array)),
                'max': float(np.max(values_array)),
                'n_seeds': len(values)
            }
        else:
            aggregated[metric_name] = {
                'mean': float('nan'),
                'std': 0.0,
                'min': float('nan'),
                'max': float('nan'),
                'n_seeds': 0
            }
    
    # CRITICAL FIX: Print aggregated result with condition label
    primary_mean = aggregated.get('primary_metric', {}).get('mean', float('nan'))
    primary_std = aggregated.get('primary_metric', {}).get('std', 0.0)
    print(f"    condition={model_name} primary_metric_mean: {primary_mean:.6f} primary_metric_std: {primary_std:.6f}")
    
    return aggregated

def print_results_table(results: Dict[str, Dict[str, Dict[str, float]]]) -> None:
    """
    Print results in a standardized table format with mean ± std.
    
    Args:
        results: Nested dictionary with model results
    """
    print("\n" + "=" * 90)
    print("EXPERIMENT RESULTS (Mean ± Std over multiple seeds)")
    print("=" * 90)
    print(f"{'Condition':<35} {'Primary Metric':<22} {'Secondary Metric':<22} {'Loss':<20}")
    print("-" * 90)
    
    for model_name, model_results in results.items():
        primary = model_results.get('primary_metric', {'mean': float('nan'), 'std': 0.0})
        secondary = model_results.get('secondary_metric', {'mean': float('nan'), 'std': 0.0})
        loss = model_results.get('loss', {'mean': float('nan'), 'std': 0.0})
        
        primary_str = f"{primary['mean']:.6f} ± {primary['std']:.6f}"
        secondary_str = f"{secondary['mean']:.6f} ± {secondary['std']:.6f}"
        loss_str = f"{loss['mean']:.6f} ± {loss['std']:.6f}"
        
        # Handle NaN values
        if np.isnan(primary['mean']):
            primary_str = "NaN"
        if np.isnan(secondary['mean']):
            secondary_str = "NaN"
        if np.isnan(loss['mean']):
            loss_str = "NaN"
        
        print(f"{model_name:<35} {primary_str:<22} {secondary_str:<22} {loss_str:<20}")
    
    print("=" * 90)

def print_comparison_summary(results: Dict[str, Dict[str, Dict[str, float]]]) -> None:
    """
    Print comparison summary between baselines and proposed methods.
    
    Args:
        results: Nested dictionary with model results
    """
    print("\n" + "=" * 90)
    print("COMPARISON SUMMARY: Proposed vs Baselines")
    print("=" * 90)
    
    # Get proposed method primary metric
    proposed_primary = None
    if 'Proving_proposed' in results:
        proposed_primary = results['Proving_proposed'].get('primary_metric', {}).get('mean', float('nan'))
    
    if proposed_primary is None or np.isnan(proposed_primary):
        print("Warning: Proposed method results not available for comparison")
        return
    
    # Compare against each baseline
    for baseline_name in ['Proving_baseline_1', 'Proving_baseline_2']:
        if baseline_name in results:
            baseline_primary = results[baseline_name].get('primary_metric', {}).get('mean', float('nan'))
            if not np.isnan(baseline_primary) and abs(baseline_primary) > 1e-10:
                improvement = (proposed_primary - baseline_primary) / abs(baseline_primary) * 100
                print(f"Proving_proposed vs {baseline_name}: {improvement:+.2f}% improvement")
            else:
                print(f"Proving_proposed vs {baseline_name}: Unable to compute (baseline=0 or NaN)")
    
    # Compare variant against proposed
    if 'Proving_variant' in results:
        variant_primary = results['Proving_variant'].get('primary_metric', {}).get('mean', float('nan'))
        if not np.isnan(variant_primary) and abs(proposed_primary) > 1e-10:
            improvement = (variant_primary - proposed_primary) / abs(proposed_primary) * 100
            print(f"Proving_variant vs Proving_proposed: {improvement:+.2f}% difference")
    
    print("=" * 90)

def main() -> None:
    """Main experiment entry point with full orchestration."""
    print("=" * 90)
    print("AETHER PROPERTY DERIVATION EXPERIMENT")
    print("=" * 90)
    
    # Initialize configuration
    config = AetherConfig()
    print(f"\nConfiguration:")
    print(f"  Device: {config.device}")
    print(f"  Seeds: {config.seeds}")
    print(f"  Epochs: {config.epochs}")
    print(f"  Batch size: {config.batch_size}")
    print(f"  Learning rate: {config.lr}")
    print(f"  Max hours: {config.max_hours}")
    
    # Initialize experiment harness with time budget
    time_budget = config.max_hours * 3600  # Convert hours to seconds
    harness = ExperimentHarness(time_budget=time_budget)
    
    # Collect all models to compare
    all_models: Dict[str, Type[torch.nn.Module]] = {}
    
    # Add baseline models
    print("\n--- BASELINE MODELS ---")
    for model_name, model_class in BASELINE_MODELS.items():
        all_models[model_name] = model_class
        print(f"  {model_name}: {model_class.__name__}")
    
    # Add proposed models
    print("\n--- PROPOSED MODELS ---")
    for model_name, model_class in PROPOSED_MODELS.items():
        all_models[model_name] = model_class
        print(f"  {model_name}: {model_class.__name__}")
    
    # Add ablation models
    print("\n--- ABLATION MODELS ---")
    for model_name, model_class in ABLATION_MODELS.items():
        all_models[model_name] = model_class
        print(f"  {model_name}: {model_class.__name__}")
    
    # Run experiments for all models
    all_results: Dict[str, Dict[str, Dict[str, float]]] = {}
    
    for model_name, model_class in all_models.items():
        if harness.should_stop():
            print(f"\n*** TIME BUDGET EXCEEDED - Stopping experiments ***")
            break
        
        print(f"\n{'=' * 60}")
        print(f"Running experiments for: {model_name}")
        print(f"{'=' * 60}")
        
        start_time = time.time()
        
        results = run_multi_seed_experiment(
            config, model_class, model_name, harness
        )
        all_results[model_name] = results
        
        elapsed = time.time() - start_time
        print(f"  Completed in {elapsed:.1f}s")
        
        # Print intermediate results
        primary = results.get('primary_metric', {'mean': float('nan'), 'std': 0.0})
        n_seeds = results.get('primary_metric', {}).get('n_seeds', 0)
        print(f"  Primary metric: {primary['mean']:.6f} ± {primary['std']:.6f} (n={n_seeds} seeds)")
    
    # Print final results table
    print_results_table(all_results)
    
    # Print comparison summary
    print_comparison_summary(all_results)
    
    # CRITICAL FIX: Print SUMMARY line comparing all conditions
    print("\n" + "=" * 90)
    print("SUMMARY: All Conditions Comparison")
    print("=" * 90)
    for model_name, model_results in all_results.items():
        primary_mean = model_results.get('primary_metric', {}).get('mean', float('nan'))
        primary_std = model_results.get('primary_metric', {}).get('std', 0.0)
        print(f"condition={model_name} primary_metric: {primary_mean:.6f} ± {primary_std:.6f}")
    print("=" * 90)
    
    # Finalize experiment
    summary = harness.finalize()
    print(f"\n{'=' * 90}")
    print("EXPERIMENT SUMMARY")
    print(f"{'=' * 90}")
    print(f"Total experiment time: {summary['elapsed_seconds']:.1f}s ({summary['elapsed_seconds']/3600:.2f}h)")
    print(f"Time budget: {summary['time_budget']}s ({config.max_hours}h)")
    print(f"Experiment completed: {summary['completed']}")
    print(f"Models evaluated: {len(all_results)}/{len(all_models)}")
    print("=" * 90)

if __name__ == "__main__":
    main()