from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class AuditTrailRecord:
    """
    Single inference-level audit record.
    Intended to be lightweight and serializable.
    """

    timestamp: float
    request_id: str
    context: dict[str, Any]
    summary: dict[str, Any]


@dataclass
class AuditTrail:
    """
    In-memory audit trail with optional JSONL export.
    This is intentionally minimal: storage backend can be swapped in future.
    """

    records: list[AuditTrailRecord] = field(default_factory=list)

    def record_inference(
        self,
        request_id: str,
        context: dict[str, Any],
        summary: dict[str, Any],
        timestamp: float | None = None,
    ) -> None:
        ts = time.time() if timestamp is None else timestamp
        self.records.append(
            AuditTrailRecord(
                timestamp=ts,
                request_id=request_id,
                context=context,
                summary=summary,
            )
        )

    def to_dicts(self) -> list[dict[str, Any]]:
        return [
            {
                "timestamp": r.timestamp,
                "request_id": r.request_id,
                "context": r.context,
                "summary": r.summary,
            }
            for r in self.records
        ]

    def export_jsonl(self, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("w", encoding="utf-8") as f:
            for rec in self.to_dicts():
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
