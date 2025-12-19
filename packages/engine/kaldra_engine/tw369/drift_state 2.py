"""
DriftState - Persistent state for TW369 drift tracking.

Represents a snapshot of the TW369 system state at a point in time,
including plane values, drift metrics, and historical context.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional
from pathlib import Path


@dataclass
class DriftState:
    """
    Represents the state of TW369 drift at a point in time.
    
    Attributes:
        timestamp: Unix timestamp of state capture
        plane_values: Values for planes 3, 6, 9
        drift_metric: Overall drift measure
        painleve_coherence: Painlevé filter coherence score
        history_window: List of recent state snapshots
        regime: Current archetypal regime (e.g., "A07_RULER")
    """
    
    timestamp: float = field(default_factory=time.time)
    plane_values: Dict[str, float] = field(default_factory=lambda: {"3": 0.0, "6": 0.0, "9": 0.0})
    drift_metric: float = 0.0
    painleve_coherence: float = 0.0
    history_window: List[Dict[str, Any]] = field(default_factory=list)
    regime: str = "UNKNOWN"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DriftState:
        """Create from dictionary."""
        return cls(**data)
    
    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> DriftState:
        """Deserialize from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def save(self, path: Path) -> None:
        """Save to JSON file."""
        with open(path, "w") as f:
            f.write(self.to_json())
    
    @classmethod
    def load(cls, path: Path) -> DriftState:
        """Load from JSON file."""
        with open(path, "r") as f:
            return cls.from_json(f.read())
