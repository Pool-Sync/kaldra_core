"""
KALDRA News APIs - Validation Script
Tests all configured external news APIs to ensure they're working correctly.
"""
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from kaldra_data.ingestion.news.mediastack_client import MediaStackClient
from kaldra_data.ingestion.news.gnews_client import GNewsClient

def test_mediastack():
    """Test MediaStack API"""
    print("\n🔍 Testing MediaStack API...")
    
    api_key = os.getenv("MEDIASTACK_API_KEY")
    if not api_key or api_key.startswith("COLE_"):
        print("❌ MEDIASTACK_API_KEY not configured in .env.local")
        return False
    
    try:
        client = MediaStackClient()
        articles = client.fetch_latest("AI", limit=5)
        
        if articles:
            print(f"✅ MediaStack: Fetched {len(articles)} articles")
            print(f"   Sample: {articles[0].get('title', 'N/A')[:60]}...")
            return True
        else:
            print("⚠️  MediaStack: No articles returned (check API quota)")
            return False
    except Exception as e:
        print(f"❌ MediaStack error: {e}")
        return False

def test_gnews():
    """Test GNews API"""
    print("\n🔍 Testing GNews API...")
    
    api_key = os.getenv("GNEWS_API_KEY")
    if not api_key or api_key.startswith("COLE_"):
        print("❌ GNEWS_API_KEY not configured in .env.local")
        return False
    
    try:
        client = GNewsClient()
        articles = client.fetch_latest("AI", limit=5)
        
        if articles:
            print(f"✅ GNews: Fetched {len(articles)} articles")
            print(f"   Sample: {articles[0].get('title', 'N/A')[:60]}...")
            return True
        else:
            print("⚠️  GNews: No articles returned (check API quota)")
            return False
    except Exception as e:
        print(f"❌ GNews error: {e}")
        return False

def main():
    print("=" * 60)
    print("KALDRA News APIs - Validation Test")
    print("=" * 60)
    
    # Check if .env.local exists
    env_file = project_root / ".env.local"
    if not env_file.exists():
        print("\n❌ .env.local not found!")
        print("   Please create it from .env.example and add your API keys")
        return
    
    print(f"\n✅ Found .env.local at: {env_file}")
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file)
        print("✅ Loaded environment variables")
    except ImportError:
        print("⚠️  python-dotenv not installed, using system environment")
    
    # Run tests
    results = {
        "MediaStack": test_mediastack(),
        "GNews": test_gnews(),
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    for api, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{api:20} {status}")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\nTotal: {passed}/{total} APIs working")
    
    if passed == total:
        print("\n🎉 All APIs are configured correctly!")
    elif passed > 0:
        print("\n⚠️  Some APIs are working, check the failures above")
    else:
        print("\n❌ No APIs are working, please check your .env.local configuration")

if __name__ == "__main__":
    main()
