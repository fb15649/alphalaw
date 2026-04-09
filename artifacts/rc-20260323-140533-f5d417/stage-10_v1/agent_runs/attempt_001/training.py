"""Training utilities for aether property derivation models."""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from typing import Dict, Any, Optional
from config import AetherConfig


class Trainer:
    """Trainer class for aether property models."""
    
    def __init__(self, model: nn.Module, config: AetherConfig):
        """
        Initialize the trainer.
        
        Args:
            model: The model to train
            config: Configuration object with hyperparameters
        """
        self.model = model
        self.config = config
        self.device = config.device
        
        # Move model to device
        self.model = self.model.to(self.device)
        
        # Optimizer with weight decay
        self.optimizer = torch.optim.AdamW(
            self.model.parameters(),
            lr=config.lr,
            weight_decay=config.weight_decay
        )
        
        # Learning rate scheduler
        self.scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer,
            mode='min',
            factor=0.5,
            patience=5,
            verbose=False
        )
        
        self.best_val_loss = float('inf')
        self.final_train_loss = float('inf')
    
    def train_one_epoch(self, train_loader: DataLoader) -> float:
        """
        Train for one epoch.
        
        Args:
            train_loader: Training data loader
            
        Returns:
            Average training loss for the epoch
        """
        self.model.train()
        total_loss = 0.0
        num_batches = 0
        
        for batch in train_loader:
            obs = batch['obs'].to(self.device)
            targets = batch['target'].to(self.device)
            errors = batch['error'].to(self.device)
            
            # Forward pass
            self.optimizer.zero_grad()
            predictions = self.model(obs)
            
            # Compute physics loss
            loss = self.model.compute_physics_loss(predictions, targets, errors)
            
            # Backward pass
            loss.backward()
            
            # Gradient clipping
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            
            self.optimizer.step()
            
            total_loss += loss.item()
            num_batches += 1
        
        avg_loss = total_loss / max(num_batches, 1)
        self.final_train_loss = avg_loss
        return avg_loss
    
    def validate(self, val_loader: DataLoader) -> float:
        """
        Validate the model.
        
        Args:
            val_loader: Validation data loader
            
        Returns:
            Average validation loss
        """
        self.model.eval()
        total_loss = 0.0
        num_batches = 0
        
        with torch.no_grad():
            for batch in val_loader:
                obs = batch['obs'].to(self.device)
                targets = batch['target'].to(self.device)
                errors = batch['error'].to(self.device)
                
                predictions = self.model(obs)
                loss = self.model.compute_physics_loss(predictions, targets, errors)
                
                total_loss += loss.item()
                num_batches += 1
        
        avg_loss = total_loss / max(num_batches, 1)
        return avg_loss
    
    def fit(
        self, 
        train_loader: DataLoader, 
        val_loader: DataLoader
    ) -> Dict[str, Any]:
        """
        Train the model.
        
        Args:
            train_loader: Training data loader
            val_loader: Validation data loader
            
        Returns:
            Dictionary with training results
        """
        for epoch in range(self.config.epochs):
            # Train
            train_loss = self.train_one_epoch(train_loader)
            
            # Validate
            val_loss = self.validate(val_loader)
            
            # Update scheduler
            self.scheduler.step(val_loss)
            
            # Track best validation loss
            if val_loss < self.best_val_loss:
                self.best_val_loss = val_loss
        
        return {
            'final_train_loss': self.final_train_loss,
            'best_val_loss': self.best_val_loss
        }
    
    def evaluate(self, test_loader: DataLoader) -> Dict[str, float]:
        """
        Evaluate the model on test data.
        
        Args:
            test_loader: Test data loader
            
        Returns:
            Dictionary with evaluation metrics
        """
        self.model.eval()
        total_loss = 0.0
        total_chi_sq = 0.0
        num_batches = 0
        
        with torch.no_grad():
            for batch in test_loader:
                obs = batch['obs'].to(self.device)
                targets = batch['target'].to(self.device)
                errors = batch['error'].to(self.device)
                
                predictions = self.model(obs)
                loss = self.model.compute_physics_loss(predictions, targets, errors)
                
                total_loss += loss.item()
                
                # Compute chi-squared (normalized to [0, 1] range)
                chi_sq = ((predictions - targets) ** 2 / (errors ** 2 + 1e-8)).mean().item()
                total_chi_sq += chi_sq
                
                num_batches += 1
        
        avg_loss = total_loss / max(num_batches, 1)
        avg_chi_sq = total_chi_sq / max(num_batches, 1)
        
        # Convert chi-squared to a goodness-of-fit metric in [0, 1]
        # Lower chi-squared = better fit, so we invert and clamp
        primary_metric = max(0.0, min(1.0, 1.0 / (1.0 + avg_chi_sq)))
        
        # Secondary metric: negative loss (higher = better)
        secondary_metric = -avg_loss
        
        return {
            'loss': avg_loss,
            'primary_metric': primary_metric,
            'secondary_metric': secondary_metric
        }