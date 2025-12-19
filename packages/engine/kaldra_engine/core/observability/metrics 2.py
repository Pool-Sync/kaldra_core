"""
Metrics Collection for KALDRA v2.9.
"""
from typing import Dict, Any

class MetricsCollector:
    def __init__(self):
        self.counters = {}
        self.gauges = {}
        self.histograms = {}

    def increment(self, metric: str, value: int = 1):
        self.counters[metric] = self.counters.get(metric, 0) + value

    def gauge(self, metric: str, value: float):
        self.gauges[metric] = value

    def observe(self, metric: str, value: float):
        if metric not in self.histograms:
            self.histograms[metric] = []
        self.histograms[metric].append(value)

# Global instance
metrics = MetricsCollector()
