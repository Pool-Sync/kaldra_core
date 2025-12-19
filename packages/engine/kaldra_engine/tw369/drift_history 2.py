"""
DriftHistory - In-memory storage for TW369 drift topology.

Maintains a sliding window of drift samples for topological analysis.
Part of KALDRA v3.2 TW369 Topological Deepening.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import datetime
from typing import Deque, List, Optional


@dataclass
class DriftSample:
    """
    A single drift observation snapshot.
    
    Attributes:
        timestamp: When this sample was recorded
        drift_value: The drift metric value
        tracy_widom_severity: Tracy-Widom severity score [0, 1]
        regime: Regime classification at sampling time
    """
    timestamp: datetime
    drift_value: float
    tracy_widom_severity: float
    regime: str


class DriftHistory:
    """
    In-memory drift history for TW369 topological analysis.
    
    Stores the last N drift samples in a deque for efficient
    memory management and temporal analysis.
    
    Pattern follows existing DriftMemory class for consistency.
    """
    
    def __init__(self, max_len: int = 512) -> None:
        """
        Initialize drift history.
        
        Args:
            max_len: Maximum number of samples to retain (default: 512)
        """
        self._max_len = max_len
        self._history: Deque[DriftSample] = deque(maxlen=max_len)
    
    def add_sample(
        self,
        drift_value: float,
        tracy_widom_severity: float,
        regime: str,
        timestamp: Optional[datetime] = None,
    ) -> None:
        """
        Add a new drift sample to the history.
        
        Args:
            drift_value: The drift metric value
            tracy_widom_severity: Tracy-Widom severity score
            regime: Current regime classification
            timestamp: Optional timestamp (defaults to now)
        """
        ts = timestamp or datetime.utcnow()
        self._history.append(
            DriftSample(
                timestamp=ts,
                drift_value=drift_value,
                tracy_widom_severity=tracy_widom_severity,
                regime=regime,
            )
        )
    
    def get_samples(self) -> List[DriftSample]:
        """
        Retrieve all stored samples.
        
        Returns:
            List of DriftSample objects (oldest to newest)
        """
        return list(self._history)
    
    def is_empty(self) -> bool:
        """
        Check if history is empty.
        
        Returns:
            True if no samples stored
        """
        return len(self._history) == 0
    
    def clear(self) -> None:
        """Clear all history."""
        self._history.clear()
    
    def get_latest(self) -> Optional[DriftSample]:
        """
        Get the most recent sample.
        
        Returns:
            Latest DriftSample or None if empty
        """
        return self._history[-1] if self._history else None
