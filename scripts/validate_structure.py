"""
Validate expected directory structure for KALDRA CORE.
"""
from __future__ import annotations

from pathlib import Path


EXPECTED_PATHS = [
    "core/tw369",
    "core/kindras",
    "core/bias",
    "core/meta",
    "core/delta144",
    "kaldra_engine",
    "apps",
    "infra",
]


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    missing = []
    for rel in EXPECTED_PATHS:
        p = root / rel
        if not p.exists():
            missing.append(rel)

    if missing:
        raise SystemExit(f"Missing expected paths: {missing}")
    print("✅ Structure validation: OK")
    print(f"   Validated {len(EXPECTED_PATHS)} directories")


if __name__ == "__main__":
    main()
