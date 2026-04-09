"""Experiment harness for managing experiments with time budgets and validation."""

import time
import math
from typing import Any, Dict, Optional


class ExperimentHarness:
    """Harness for managing experiments with time budgets and metric validation."""
    
    def __init__(self, time_budget: Optional[float] = None):
        """
        Initialize the experiment harness.
        
        Args:
            time_budget: Maximum time in seconds for the experiment (None for no limit)
        """
        self.time_budget = time_budget
        self.start_time = time.time()
        self.metrics: Dict[str, list] = {}
        self._should_stop = False
        # CRITICAL FIX: Initialize elapsed to 0.0 to ensure it's always defined
        # regardless of whether should_stop() is ever called
        self._elapsed = 0.0
    
    def should_stop(self) -> bool:
        """
        Check if the experiment should stop.
        
        Returns:
            True if time budget exceeded or stop signal received
        """
        if self._should_stop:
            return True
        
        if self.time_budget is not None:
            # Compute elapsed time
            self._elapsed = time.time() - self.start_time
            if self._elapsed >= self.time_budget:
                self._should_stop = True
                return True
        
        return False
    
    def check_value(self, value: Any, name: str) -> bool:
        """
        Check if a value is valid (not NaN or Inf).
        
        Args:
            value: The value to check
            name: Name of the metric for error reporting
            
        Returns:
            True if value is valid, False otherwise
        """
        if value is None:
            return False
        
        if isinstance(value, (int, float)):
            if math.isnan(value) or math.isinf(value):
                return False
        
        return True
    
    def report_metric(self, name: str, value: float) -> None:
        """
        Report a metric value.
        
        Args:
            name: Name of the metric
            value: Value of the metric
        """
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(value)
    
    def get_metric_summary(self, name: str) -> Dict[str, float]:
        """
        Get summary statistics for a metric.
        
        Args:
            name: Name of the metric
            
        Returns:
            Dictionary with mean, std, min, max
        """
        if name not in self.metrics or len(self.metrics[name]) == 0:
            return {'mean': float('nan'), 'std': 0.0, 'min': float('nan'), 'max': float('nan')}
        
        values = self.metrics[name]
        n = len(values)
        mean = sum(values) / n
        variance = sum((v - mean) ** 2 for v in values) / n
        std = math.sqrt(variance) if n > 1 else 0.0
        
        return {
            'mean': mean,
            'std': std,
            'min': min(values),
            'max': max(values)
        }
    
    def get_elapsed_time(self) -> float:
        """
        Get the elapsed time since the experiment started.
        
        Returns:
            Elapsed time in seconds
        """
        # Always compute fresh elapsed time directly
        return time.time() - self.start_time
    
    def finalize(self) -> Dict[str, Any]:
        """
        Finalize the experiment and return summary.
        
        Returns:
            Dictionary with experiment summary
        """
        # CRITICAL FIX: Compute elapsed directly here, not from stored variable
        elapsed = time.time() - self.start_time
        
        summary = {
            'elapsed_seconds': elapsed,
            'time_budget': self.time_budget,
            'completed': not self._should_stop or elapsed < (self.time_budget or float('inf')),
            'metrics': {name: self.get_metric_summary(name) for name in self.metrics}
        }
        
        return summary