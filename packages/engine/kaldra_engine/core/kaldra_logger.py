from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class KALDRALogger:
    """
    Structured logger for KALDRA Core.

    Logs events as JSON strings via the standard logging module.
    Intended for:
      - inference lifecycle events
      - TW369 / Δ144 summaries
      - epistemic decisions
    """

    logger_name: str = "kaldra.core"
    enabled: bool = True
    level: int = logging.INFO
    _logger: logging.Logger = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._logger = logging.getLogger(self.logger_name)
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(message)s")
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
        self._logger.setLevel(self.level)

    def log_event(
        self,
        event_type: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log a structured event as a JSON line.

        event_type: short string describing the event, e.g. "inference_start".
        payload: free-form dictionary with structured data.
        """
        if not self.enabled:
            return

        record = {
            "ts": time.time(),
            "event": event_type,
        }
        if payload:
            record.update(payload)

        try:
            self._logger.info(json.dumps(record, ensure_ascii=False))
        except Exception:
            # Never break the pipeline because of logging
            return


def make_default_logger() -> KALDRALogger:
    """
    Convenience factory for a default KALDRALogger.
    """
    return KALDRALogger()
