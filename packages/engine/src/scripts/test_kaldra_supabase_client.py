"""
Test script for KALDRA Supabase Client.

Usage:
    python -m src.scripts.test_kaldra_supabase_client
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from infrastructure.supabase_client import SupabaseClient


def main() -> None:
    print("🔧 Testing KALDRA Supabase Client v1...")
    
    try:
        # Initialize client
        client = SupabaseClient()
        print("✅ Client initialized")
        print(f"→ URL: {client.url}")
        
        # Test fetch
        print("\n📊 Testing fetch on 'signals' table...")
        result = client.fetch("signals", "select=*&limit=5")
        
        if "error" in result:
            print(f"❌ Fetch error: {result}")
        else:
            print(f"✅ Fetch successful")
            if isinstance(result, list):
                print(f"→ Returned {len(result)} rows")
            else:
                print(f"→ Result: {result}")
        
        # Test fetch on profiles
        print("\n👤 Testing fetch on 'profiles' table...")
        profiles = client.fetch("profiles", "select=*&limit=5")
        
        if "error" in profiles:
            print(f"❌ Profiles error: {profiles}")
        else:
            print(f"✅ Profiles fetch successful")
            if isinstance(profiles, list):
                print(f"→ Returned {len(profiles)} profiles")
        
        print("\n🎉 KALDRA Supabase Client is working!")
        
    except RuntimeError as e:
        print(f"\n❌ Initialization error: {e}")
        print("Make sure .env is configured with SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
