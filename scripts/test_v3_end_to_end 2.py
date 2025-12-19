"""
End-to-end test for KALDRA v3.0 Unification Layer.
"""
import sys
import json
sys.path.insert(0, '/Users/niki/Desktop/kaldra_core')

from src.unification.adapters.unified_api import UnifiedKaldra

def test_unified_api():
    print("=" * 60)
    print("KALDRA v3.0 — End-to-End Test")
    print("=" * 60)
    
    # Initialize API
    print("\n1. Initializing UnifiedKaldra API...")
    kaldra = UnifiedKaldra()
    print(f"   ✓ {kaldra}")
    print(f"   ✓ Modules loaded: {kaldra.list_modules()}")
    
    # Test text
    test_text = "The company announced record profits despite market uncertainty."
    
    # Test different modes
    modes = ["signal", "full", "safety-first"]
    
    for mode in modes:
        print(f"\n2. Testing mode: {mode}")
        print(f"   Input: \"{test_text}\"")
        
        result = kaldra.analyze(test_text, mode=mode)
        
        print(f"   ✓ Analysis complete")
        print(f"   - Request ID: {result.get('request_id', 'N/A')}")
        print(f"   - Mode: {result.get('mode', 'N/A')}")
        print(f"   - Degraded: {result.get('summary', {}).get('degraded', 'N/A')}")
        
        if result.get('archetypes'):
            arch = result['archetypes']
            if arch.get('delta144_state'):
                state = arch['delta144_state']
                if state.get('archetype'):
                    print(f"   - Archetype: {state['archetype'].get('label', 'N/A')}")
                if state.get('state'):
                    print(f"   - State: {state['state'].get('label', 'N/A')}")
        
        if result.get('risk'):
            risk = result['risk']
            print(f"   - Risk Level: {risk.get('final_risk', 'N/A')}")
            print(f"   - Risk Score: {risk.get('risk_score', 0.0):.3f}")
    
    # Test batch processing
    print("\n3. Testing batch processing...")
    texts = [
        "Innovation drives progress.",
        "Uncertainty creates opportunity.",
        "Leadership requires vision."
    ]
    
    results = kaldra.analyze_batch(texts, mode="signal")
    print(f"   ✓ Batch analysis complete: {len(results)} results")
    
    for i, result in enumerate(results):
        arch_label = "N/A"
        if result.get('archetypes', {}).get('delta144_state', {}).get('archetype'):
            arch_label = result['archetypes']['delta144_state']['archetype'].get('label', 'N/A')
        print(f"   - Text {i+1}: {arch_label}")
    
    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)
    
    # Print sample output
    print("\n4. Sample output (full mode):")
    sample = kaldra.analyze("Test", mode="full")
    print(json.dumps(sample, indent=2, default=str)[:500] + "...")

if __name__ == "__main__":
    test_unified_api()
