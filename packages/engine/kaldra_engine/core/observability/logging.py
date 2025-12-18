"""
Structured Logging for KALDRA v2.9.
"""
import logging
import json
import time
from typing import Any, Dict

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        
    def log(self, level: str, event: str, request_id: str, details: Dict[str, Any] = None):
        payload = {
            "timestamp": time.time(),
            "level": level,
            "event": event,
            "request_id": request_id,
            "details": details or {}
        }
        self.logger.log(getattr(logging, level), json.dumps(payload))

    def info(self, event: str, request_id: str, details: Dict[str, Any] = None):
        self.log("INFO", event, request_id, details)

    def error(self, event: str, request_id: str, details: Dict[str, Any] = None):
        self.log("ERROR", event, request_id, details)

    def warn(self, event: str, request_id: str, details: Dict[str, Any] = None):
        self.log("WARNING", event, request_id, details)
