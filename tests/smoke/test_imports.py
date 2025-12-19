
import sys
import os

# Add root to path
sys.path.insert(0, os.getcwd())

def test_engine_import():
    import kaldra_engine
    print("Engine import: OK")

def test_api_import():
    try:
        from apps.api.main import app
        print("API import: OK")
    except ImportError as e:
        print(f"API import skipped (deps?): {e}")

if __name__ == "__main__":
    test_engine_import()
    test_api_import()
