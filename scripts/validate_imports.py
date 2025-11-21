"""
Validate that main KALDRA CORE modules can be imported.
"""
from __future__ import annotations


def main() -> None:
    import importlib

    modules = [
        "kaldra_core.core.tw369",
        "kaldra_core.core.kindras",
        "kaldra_core.core.bias",
        "kaldra_core.core.meta",
        "kaldra_core.core.delta144",
        "kaldra_core.kaldra_engine",
    ]

    for m in modules:
        importlib.import_module(m)

    print("✅ Import validation: OK")
    print(f"   Validated {len(modules)} modules")


if __name__ == "__main__":
    main()
