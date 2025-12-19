"""
Quick test of KALDRA v3.0 Unified Kernel.
"""
import sys
sys.path.insert(0, '/Users/niki/Desktop/kaldra_core')

from src.unification.kernel import UnifiedKernel

def test_kernel():
    print("Testing KALDRA v3.0 Unified Kernel...")
    
    # Initialize kernel
    kernel = UnifiedKernel()
    print(f"✓ Kernel initialized: {kernel}")
    
    # List loaded modules
    modules = kernel.list_modules()
    print(f"✓ Loaded modules: {modules}")
    
    # Run a simple test
    result = kernel.run("Test input text", mode="full")
    print(f"✓ Kernel run successful")
    print(f"  Request ID: {result.global_ctx.request_id}")
    print(f"  Mode: {result.global_ctx.mode}")
    print(f"  Version: {result.global_ctx.version}")
    
    print("\n✅ All tests passed!")

if __name__ == "__main__":
    test_kernel()
