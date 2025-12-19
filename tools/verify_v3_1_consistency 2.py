#!/usr/bin/env python3
"""
KALDRA v3.1 Consistency Verification Tool.

Verifies that all v3.1 components are properly installed and configured.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


def check_mark(passed: bool) -> str:
    """Return colored check mark or X."""
    if passed:
        return f"{Colors.GREEN}✓{Colors.END}"
    return f"{Colors.RED}✗{Colors.END}"


def verify_presets():
    """Verify that all presets are valid and loadable."""
    print(f"\n{Colors.BLUE}Checking Presets...{Colors.END}")
    
    try:
        from src.unification.exoskeleton import PresetManager
        
        mgr = PresetManager()
        presets = mgr.list_presets()
        
        required_presets = ["alpha", "geo", "safeguard", "product"]
        
        all_valid = True
        for preset_name in required_presets:
            exists = preset_name in presets
            print(f"  {check_mark(exists)} Preset '{preset_name}' exists")
            if not exists:
                all_valid = False
        
        return all_valid
    
    except Exception as e:
        print(f"  {check_mark(False)} PresetManager failed: {e}")
        return False


def verify_profiles():
    """Verify that ProfileManager is functional."""
    print(f"\n{Colors.BLUE}Checking Profiles...{Colors.END}")
    
    try:
        from src.unification.exoskeleton import ProfileManager
        
        mgr = ProfileManager(storage_dir="test_profiles_verify")
        
        # Create test profile
        try:
            profile = mgr.create_profile("test_user", {"risk_tolerance": 0.5})
            created = profile is not None
            print(f"  {check_mark(created)} ProfileManager can create profiles")
        except Exception as e:
            print(f"  {check_mark(False)} Profile creation failed: {e}")
            return False
        
        # Retrieve test profile
        try:
            retrieved = mgr.get_profile("test_user")
            retrieved_ok = retrieved is not None and retrieved.user_id == "test_user"
            print(f"  {check_mark(retrieved_ok)} ProfileManager can retrieve profiles")
        except Exception as e:
            print(f"  {check_mark(False)} Profile retrieval failed: {e}")
            return False
        
        # Cleanup
        try:
            import shutil
            if os.path.exists("test_profiles_verify"):
                shutil.rmtree("test_profiles_verify")
        except:
            pass
        
        return True
    
    except Exception as e:
        print(f"  {check_mark(False)} ProfileManager failed: {e}")
        return False


def verify_preset_router():
    """Verify PresetRouter functionality."""
    print(f"\n{Colors.BLUE}Checking Preset Router...{Colors.END}")
    
    try:
        from src.unification.exoskeleton import PresetRouter
        
        router = PresetRouter()
        
        # Test basic resolution
        try:
            config = router.resolve_preset("alpha")
            resolved = config is not None and config.name == "alpha"
            print(f"  {check_mark(resolved)} PresetRouter can resolve presets")
        except Exception as e:
            print(f"  {check_mark(False)} Preset resolution failed: {e}")
            return False
        
        # Test default config
        try:
            default = router.get_default_config()
            has_default = default is not None
            print(f"  {check_mark(has_default)} PresetRouter has default config")
        except Exception as e:
            print(f"  {check_mark(False)} Default config failed: {e}")
            return False
        
        return True
    
    except Exception as e:
        print(f"  {check_mark(False)} PresetRouter failed: {e}")
        return False


def verify_signal_adapter():
    """Verify SignalAdapter v3.1 enhancements."""
    print(f"\n{Colors.BLUE}Checking Signal Adapter...{Colors.END}")
    
    try:
        from src.unification.output import SignalAdapter
        
        # Check that SignalAdapter exists
        has_adapter = SignalAdapter is not None
        print(f"  {check_mark(has_adapter)} SignalAdapter importable")
        
        # Check that to_signal method exists
        has_method = hasattr(SignalAdapter, 'to_signal')
        print(f"  {check_mark(has_method)} SignalAdapter.to_signal() exists")
        
        return has_adapter and has_method
    
    except Exception as e:
        print(f"  {check_mark(False)} SignalAdapter failed: {e}")
        return False


def verify_api_routers():
    """Verify API v3.1 routers exist."""
    print(f"\n{Colors.BLUE}Checking API Routers...{Colors.END}")
    
    router_files = [
        "kaldra_api/routers/router_v3_1.py",
        "kaldra_api/routers/v3_1_analyze.py",
        "kaldra_api/routers/v3_1_presets.py",
        "kaldra_api/routers/v3_1_profile.py"
    ]
    
    all_exist = True
    for router_file in router_files:
        path = project_root / router_file
        exists = path.exists()
        print(f"  {check_mark(exists)} {router_file}")
        if not exists:
            all_exist = False
    
    return all_exist


def verify_schemas():
    """Verify API v3.1 schemas exist."""
    print(f"\n{Colors.BLUE}Checking API Schemas...{Colors.END}")
    
    schema_files = [
        "kaldra_api/schemas/v3_1_schemas.py",
        "kaldra_api/schemas/v3_1_responses.py"
    ]
    
    all_exist = True
    for schema_file in schema_files:
        path = project_root / schema_file
        exists = path.exists()
        print(f"  {check_mark(exists)} {schema_file}")
        if not exists:
            all_exist = False
    
    return all_exist


def verify_documentation():
    """Verify documentation exists."""
    print(f"\n{Colors.BLUE}Checking Documentation...{Colors.END}")
    
    doc_files = [
        "docs/api/v3_1_api_reference.md",
        "docs/release_notes/v3.1.0.md",
        "docs/exoskeleton/presets_system.md",
        "docs/exoskeleton/profiles_system.md",
        "docs/exoskeleton/preset_router.md"
    ]
    
    all_exist = True
    for doc_file in doc_files:
        path = project_root / doc_file
        exists = path.exists()
        print(f"  {check_mark(exists)} {doc_file}")
        if not exists:
            all_exist = False
    
    return all_exist


def main():
    """Run all verification checks."""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}KALDRA v3.1 Consistency Verification{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    
    results = {
        "Presets": verify_presets(),
        "Profiles": verify_profiles(),
        "Router": verify_preset_router(),
        "Signal Adapter": verify_signal_adapter(),
        "API Routers": verify_api_routers(),
        "Schemas": verify_schemas(),
        "Documentation": verify_documentation()
    }
    
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}Summary:{Colors.END}")
    
    all_passed = True
    for component, passed in results.items():
        status = f"{Colors.GREEN}PASS{Colors.END}" if passed else f"{Colors.RED}FAIL{Colors.END}"
        print(f"  {component}: {status}")
        if not passed:
            all_passed = False
    
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    if all_passed:
        print(f"{Colors.GREEN}✓ All v3.1 components verified successfully!{Colors.END}\n")
        return 0
    else:
        print(f"{Colors.RED}✗ Some components failed verification.{Colors.END}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
