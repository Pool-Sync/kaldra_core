"""
TW369Topology - Topological analysis for TW369 drift dynamics.

Implements:
- Painlevé II smoothing
- Tracy-Widom severity scoring
- Volatility computation
- Regime classification
- Turning point detection

Part of KALDRA v3.2 TW369 Topological Deepening.
"""

from __future__ import annotations

from typing import List, Optional
import math
import time

from src.tw369.drift_history import DriftHistory, DriftSample
from src.unification.states.unified_state import DriftContext, DriftPoint, TurningPoint




class TW369Topology:
    """
    Implements topological analysis for TW369 drift dynamics.
    
    Provides methods for:
    - Painlevé II-based smoothing of drift series
    - Tracy-Widom severity factor computation
    - Volatility analysis over sliding windows
    - Regime classification (STABLE/VOLATILE/CRITICAL/TRANSITION)
    - Turning point detection between regimes
    """
    
    def __init__(
        self,
        severe_threshold: float = 0.85,
        critical_threshold: float = 0.95,
        volatility_window: int = 32,
    ) -> None:
        """
        Initialize topology analyzer.
        
        Args:
            severe_threshold: Tracy-Widom severity threshold for VOLATILE regime
            critical_threshold: Severity threshold for CRITICAL regime
            volatility_window: Number of recent samples for volatility computation
        """
        self.severe_threshold = severe_threshold
        self.critical_threshold = critical_threshold
        self.volatility_window = volatility_window
    
    def smooth_with_painleve(self, series: List[float]) -> List[float]:
        """
        Apply Painlevé II-based smoothing to a drift series.
        
        TODO: Replace with real Painlevé filter from painleve_filter.py
        Current implementation uses simple moving average as placeholder.
        
        Args:
            series: Time series of drift values
            
        Returns:
            Smoothed drift series
        """
        if not series:
            return series
        
        # Placeholder: Simple moving average with window=3
        # TODO: Integrate real Painlevé II solver from src.tw369.painleve.painleve_filter
        smoothed = []
        window = 3
        
        for i in range(len(series)):
            start = max(0, i - window + 1)
            chunk = series[start : i + 1]
            smoothed.append(sum(chunk) / len(chunk))
        
        return smoothed
    
    def compute_tracy_widom_severity(
        self,
        lambda_max: float,
        mean: float = 0.0,
        std: float = 1.0,
    ) -> float:
        """
        Compute Tracy-Widom severity as tail probability.
        
        Severity represents how extreme lambda_max is relative to
        the Tracy-Widom distribution. Higher severity = more unstable.
        
        TODO: Integrate with real Tracy-Widom CDF from tracy_widom.py
        Current implementation uses logistic approximation as fallback.
        
        Args:
            lambda_max: Maximum eigenvalue or instability index
            mean: Distribution mean (for normalization)
            std: Distribution standard deviation (for normalization)
            
        Returns:
            Severity score in [0, 1]
        """
        if std <= 0:
            return 0.0
        
        # Normalize lambda_max
        z = (lambda_max - mean) / std
        
        # Placeholder: Logistic function mapping z to [0, 1]
        # TODO: Replace with real Tracy-Widom CDF tail probability
        # from src.tw369.tracy_widom.severity_from_index()
        severity = 1.0 / (1.0 + math.exp(-z))
        
        return max(0.0, min(1.0, severity))
    
    def compute_volatility(self, series: List[float]) -> float:
        """
        Compute volatility as standard deviation over a series.
        
        Args:
            series: Time series of drift values
            
        Returns:
            Volatility (standard deviation)
        """
        if len(series) < 2:
            return 0.0
        
        mean = sum(series) / len(series)
        variance = sum((x - mean) ** 2 for x in series) / (len(series) - 1)
        
        return math.sqrt(max(variance, 0.0))
    
    def classify_regime(
        self,
        severity: float,
        volatility: float,
        volatility_threshold: float = 0.1,
    ) -> str:
        """
        Classify regime based on severity and volatility.
        
        Classification logic:
        - CRITICAL: severity >= critical_threshold (regardless of volatility)
        - VOLATILE: severe_threshold <= severity < critical_threshold
        - STABLE: severity < severe_threshold and volatility <= volatility_threshold
        - TRANSITION: severity < severe_threshold but volatility > volatility_threshold
        
        Args:
            severity: Tracy-Widom severity score [0, 1]
            volatility: Drift volatility measure
            volatility_threshold: Threshold for high volatility
            
        Returns:
            Regime string: "STABLE" | "VOLATILE" | "CRITICAL" | "TRANSITION"
        """
        if severity >= self.critical_threshold:
            return "CRITICAL"
        
        if severity >= self.severe_threshold:
            return "VOLATILE"
        
        if volatility <= volatility_threshold:
            return "STABLE"
        
        return "TRANSITION"
    
    def build_drift_context(
        self,
        history: DriftHistory,
        latest_lambda_max: float,
        mean: float = 0.0,
        std: float = 1.0,
    ) -> DriftContext:
        """
        Build complete DriftContext with topological analysis.
        
        Orchestrates:
        1. Painlevé smoothing of drift series
        2. Tracy-Widom severity computation
        3. Volatility analysis
        4. Regime classification
        5. Trajectory construction
        6. Turning point detection
        
        Args:
            history: DriftHistory with accumulated samples
            latest_lambda_max: Most recent eigenvalue/instability index
            mean: Distribution mean for normalization
            std: Distribution standard deviation for normalization
            
        Returns:
            Complete DriftContext with all topological fields
        """
        samples = history.get_samples()
        
        # If no history, return minimal context
        if not samples:
            return DriftContext(
                drift_metric=0.0,
                regime="UNKNOWN",
                volatility=0.0,
                tracy_widom_severity=0.0,
                painleve_smoothed=False,
            )
        
        # Extract drift series from samples
        series = [s.drift_value for s in samples]
        
        # 1. Painlevé smoothing
        smoothed = self.smooth_with_painleve(series)
        painleve_smoothed = bool(smoothed)
        
        # 2. Volatility (last N samples of smoothed series)
        window_series = smoothed[-self.volatility_window :] if smoothed else []
        volatility = self.compute_volatility(window_series)
        
        # 3. Tracy-Widom severity from latest lambda_max
        tracy_severity = self.compute_tracy_widom_severity(
            lambda_max=latest_lambda_max,
            mean=mean,
            std=std,
        )
        
        # 4. Current regime
        regime = self.classify_regime(
            severity=tracy_severity,
            volatility=volatility,
        )
        
        # 5. Build trajectory as DriftPoint list
        trajectory: List[DriftPoint] = []
        for s, v in zip(samples, smoothed or series):
            trajectory.append(
                DriftPoint(
                    timestamp=s.timestamp.timestamp(),  # Convert datetime to float
                    drift_value=v,
                    tracy_widom_severity=s.tracy_widom_severity,
                    regime=s.regime,
                )
            )
        
        # 6. Detect turning points (regime transitions)
        turning_points: List[TurningPoint] = []
        prev_regime: Optional[str] = None
        
        for s in samples:
            if prev_regime is not None and s.regime != prev_regime:
                turning_points.append(
                    TurningPoint(
                        timestamp=s.timestamp.timestamp(),
                        from_regime=prev_regime,
                        to_regime=s.regime,
                        reason="regime_change",
                    )
                )
            prev_regime = s.regime
        
        # 7. Assemble final DriftContext
        latest_drift = smoothed[-1] if smoothed else 0.0
        
        ctx = DriftContext(
            drift_metric=latest_drift,
            regime=regime,
            volatility=volatility,
            tracy_widom_severity=tracy_severity,
            painleve_smoothed=painleve_smoothed,
            trajectory=trajectory,
            turning_points=turning_points,
        )
        
        return ctx

