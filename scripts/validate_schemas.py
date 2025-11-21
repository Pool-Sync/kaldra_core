"""
Validate that JSON schema/config files load correctly.
"""
from __future__ import annotations

import json
from pathlib import Path


def load_json(path: Path) -> None:
    with path.open("r", encoding="utf-8") as f:
        json.load(f)


def main() -> None:
    root = Path(__file__).resolve().parent.parent

    files = [
        root / "core/tw369/tw369.config.json",
        root / "core/bias/bias_schema.json",
        root / "core/kindras/vectors.json",
        root / "kaldra_engine/schemas/kaldra_signal.schema.json",
    ]

    for fpath in files:
        load_json(fpath)

    print("✅ Schema validation: OK")
    print(f"   Validated {len(files)} JSON files")


if __name__ == "__main__":
    main()
