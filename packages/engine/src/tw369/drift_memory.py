"""
DriftMemory - In-memory storage for TW369 drift history.

Maintains a sliding window of recent DriftState snapshots
with optional persistence to file.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional
from collections import deque

from .drift_state import DriftState


class DriftMemory:
    """
    Manages a sliding window of drift states.
    
    Provides in-memory storage with optional file persistence.
    """
    
    def __init__(self, window_size: int = 10):
        """
        Initialize drift memory.
        
        Args:
            window_size: Maximum number of states to keep in memory
        """
        self.window_size = window_size
        self._history: deque[DriftState] = deque(maxlen=window_size)
    
    def append(self, state: DriftState) -> None:
        """
        Add a new state to the history.
        
        Args:
            state: DriftState to add
        """
        self._history.append(state)
    
    def get_history(self) -> List[DriftState]:
        """
        Get all states in the history window.
        
        Returns:
            List of DriftState objects (oldest to newest)
        """
        return list(self._history)
    
    def get_latest(self) -> Optional[DriftState]:
        """
        Get the most recent state.
        
        Returns:
            Latest DriftState or None if empty
        """
        return self._history[-1] if self._history else None
    
    def clear(self) -> None:
        """Clear all history."""
        self._history.clear()
    
    def save(self, path: Path) -> None:
        """
        Save history to JSON file.
        
        Args:
            path: Path to save file
        """
        data = {
            "window_size": self.window_size,
            "history": [state.to_dict() for state in self._history]
        }
        
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    
    def load(self, path: Path) -> None:
        """
        Load history from JSON file.
        
        Args:
            path: Path to load file
        """
        with open(path, "r") as f:
            data = json.load(f)
        
        self.window_size = data.get("window_size", 10)
        self._history = deque(
            [DriftState.from_dict(state_dict) for state_dict in data.get("history", [])],
            maxlen=self.window_size
        )
    
    def compute_volatility(self) -> float:
        """
        Compute drift volatility from recent history.
        
        Returns:
            Volatility measure (std dev of drift_metric)
        """
        if len(self._history) < 2:
            return 0.0
        
        drift_values = [state.drift_metric for state in self._history]
        
        # Simple standard deviation
        mean = sum(drift_values) / len(drift_values)
        variance = sum((x - mean) ** 2 for x in drift_values) / len(drift_values)
        
        return variance ** 0.5
