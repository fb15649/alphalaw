"""
Training loop with physics-constrained optimization and evaluation metrics.
"""
import torch
import torch.nn.functional as F
import numpy as np
from typing import Dict, Tuple
from torch.utils.data import DataLoader
import config
import models


class AetherTrainer:
    """Trainer for aether property derivation models."""
    
    def __init__(
        self, 
        model: models.BaseAetherModel, 
        cfg: config.Config, 
        device: torch.device
    ):
        self.model = model.to(device)
        self.cfg = cfg
        self.device = device
        
        # Optimizer with weight decay
        self.optimizer = torch.optim.AdamW(
            model.parameters(),
            lr=cfg.lr,
            weight_decay=cfg.weight_decay
        )
        
        # Learning rate scheduler
        self.scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            self.optimizer,
            T_max=cfg.epochs,
            eta_min=cfg.lr * 0.01
        )
        
        self.best_val_loss = float('inf')
        self.best_state = None
        self.history = {
            'train_loss': [], 
            'val_loss': [], 
            'metrics': []
        }
    
    def train_one_epoch(self, train_loader: DataLoader) -> float:
        """Train for one epoch."""
        self.model.train()
        total_loss = 0.0
        num_batches = 0
        
        for x, y in train_loader:
            x = x.to(self.device)
            y = y.to(self.device)
            
            self.optimizer.zero_grad()
            
            pred = self.model(x)
            loss = self.model.compute_loss(pred, y, x)
            
            # Check for NaN
            if torch.isnan(loss):
                print('WARNING: NaN loss detected, skipping batch')
                continue
            
            loss.backward()
            
            # Gradient clipping
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            
            self.optimizer.step()
            
            total_loss += loss.item()
            num_batches += 1
        
        avg_loss = total_loss / max(num_batches, 1)
        return avg_loss
    
    def evaluate(self, val_loader: DataLoader) -> Dict[str, float]:
        """Evaluate model on validation set."""
        self.model.eval()
        total_loss = 0.0
        all_preds = []
        all_targets = []
        all_features = []
        
        with torch.no_grad():
            for x, y in val_loader:
                x = x.to(self.device)
                y = y.to(self.device)
                
                pred = self.model(x)
                loss = self.model.compute_loss(pred, y, x)
                
                if not torch.isnan(loss):
                    total_loss += loss.item()
                    all_preds.append(pred.cpu())
                    all_targets.append(y.cpu())
                    all_features.append(x.cpu())
        
        avg_loss = total_loss / max(len(val_loader), 1)
        
        # Concatenate all predictions
        all_preds = torch.cat(all_preds, dim=0)
        all_targets = torch.cat(all_targets, dim=0)
        all_features = torch.cat(all_features, dim=0)
        
        # Compute metrics
        mse = F.mse_loss(all_preds, all_targets).item()
        mae = torch.mean(torch.abs(all_preds - all_targets)).item()
        
        # Physics consistency: c = sqrt(K/rho)
        rho_pred = all_preds[:, 0]
        K_pred = all_preds[:, 1]
        c_predicted = torch.sqrt(K_pred / (rho_pred + self.cfg.eps))
        c_measured = all_features[:, 2]
        c_consistency = torch.mean(torch.abs(c_predicted - c_measured)).item()
        
        return {
            'loss': avg_loss,
            'mse': mse,
            'mae': mae,
            'c_consistency': c_consistency
        }
    
    def fit(
        self, 
        train_loader: DataLoader, 
        val_loader: DataLoader
    ) -> Dict:
        """Full training loop."""
        for epoch in range(self.cfg.epochs):
            train_loss = self.train_one_epoch(train_loader)
            val_metrics = self.evaluate(val_loader)
            self.scheduler.step()
            
            self.history['train_loss'].append(train_loss)
            self.history['val_loss'].append(val_metrics['loss'])
            self.history['metrics'].append(val_metrics)
            
            # Save best model
            if val_metrics['loss'] < self.best_val_loss:
                self.best_val_loss = val_metrics['loss']
                self.best_state = {
                    k: v.cpu().clone() 
                    for k, v in self.model.state_dict().items()
                }
        
        # Restore best model
        if self.best_state is not None:
            self.model.load_state_dict({
                k: v.to(self.device) 
                for k, v in self.best_state.items()
            })
        
        return self.history


def compute_primary_metric(
    model: models.BaseAetherModel, 
    test_loader: DataLoader, 
    device: torch.device,
    cfg: config.Config
) -> float:
    """
    Compute primary metric: physics consistency score.
    
    Metric: 1 - mean_relative_physics_error
    where physics_error = |c_predicted - c_measured| / |c_measured|
    
    Higher is better (max 1.0).
    """
    model.eval()
    total_physics_error = 0.0
    total_samples = 0
    
    with torch.no_grad():
        for x, y in test_loader:
            x = x.to(device)
            y = y.to(device)
            
            pred = model(x)
            
            # Physics consistency
            rho = pred[:, 0]
            K = pred[:, 1]
            c_pred = torch.sqrt(K / (rho + cfg.eps))
            c_meas = x[:, 2]
            
            # Relative error
            rel_error = torch.abs(c_pred - c_meas) / (torch.abs(c_meas) + cfg.eps)
            
            total_physics_error += rel_error.sum().item()
            total_samples += x.shape[0]
    
    mean_error = total_physics_error / max(total_samples, 1)
    primary_metric = max(0.0, 1.0 - mean_error)
    
    return primary_metric


def compute_secondary_metric(
    model: models.BaseAetherModel, 
    test_loader: DataLoader, 
    device: torch.device,
    cfg: config.Config
) -> float:
    """
    Compute secondary metric: parameter accuracy.
    
    Metric: 1 / (1 + log_MAE)
    where log_MAE = mean(|log10(pred) - log10(target)|)
    
    Higher is better (max 1.0).
    """
    model.eval()
    all_pred_params = []
    all_target_params = []
    
    with torch.no_grad():
        for x, y in test_loader:
            pred = model(x.to(device))
            all_pred_params.append(pred.cpu())
            all_target_params.append(y)
    
    preds = torch.cat(all_pred_params, dim=0)
    targets = torch.cat(all_target_params, dim=0)
    
    # Log-scale MAE (physical parameters span orders of magnitude)
    log_preds = torch.log10(torch.abs(preds) + cfg.eps)
    log_targets = torch.log10(torch.abs(targets) + cfg.eps)
    log_mae = torch.mean(torch.abs(log_preds - log_targets)).item()
    
    # Handle potential NaN/Inf
    if np.isnan(log_mae) or np.isinf(log_mae):
        return 0.0
    
    secondary_metric = 1.0 / (1.0 + log_mae)
    return secondary_metric