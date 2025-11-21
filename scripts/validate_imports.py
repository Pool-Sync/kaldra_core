"""
Validate that main KALDRA CORE modules can be imported.
"""
from __future__ import annotations


def main():
    """Validate that core modules can be imported."""
    import importlib

    modules = [
        "core.tw369",
        "core.kindras",
        "core.bias",
        "core.meta",
        "core.delta144",
        "kaldra_engine.kaldra_engine",
    ]

    for m in modules:
        importlib.import_module(m)

    print("✅ Import validation: OK")
    print(f"   Validated {len(modules)} modules")


if __name__ == "__main__":
    main()
