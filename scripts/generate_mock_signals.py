"""
Generate mock KALDRA signals for integration testing and frontend development.
"""
from __future__ import annotations

import json
from pathlib import Path

from kaldra_core.kaldra_engine import generate_kaldra_signal


def main() -> None:
    examples = [
        "Texto neutro de teste.",
        "ALERTA MÁXIMO!!! Situação extremamente tensa!!!",
        "Comunicação moderada, com algum grau de ênfase.",
    ]

    signals = [generate_kaldra_signal(t) for t in examples]

    root = Path(__file__).resolve().parent.parent
    out_dir = root / "mock_data"
    out_dir.mkdir(exist_ok=True)

    out_path = out_dir / "sample_signals.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(signals, f, ensure_ascii=False, indent=2)

    print(f"✅ Wrote {len(signals)} signals to {out_path}")


if __name__ == "__main__":
    main()
