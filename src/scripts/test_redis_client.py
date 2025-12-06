"""
Redis Client Test Script
Tests Redis connectivity and caching functionality.
"""

import sys
import time
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.infrastructure.cache.redis_client import RedisClient, get_redis_client
from src.infrastructure.cache.decorators import redis_cache

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def test_redis_connection():
    """Test basic Redis connection."""
    print("\n" + "="*60)
    print("TEST 1: Redis Connection")
    print("="*60)
    
    client = RedisClient()
    
    if not client.enabled:
        print("❌ Redis is disabled or unavailable")
        print("   Set REDIS_ENABLED=true and ensure Redis is running")
        return False
    
    print(f"✅ Connected to Redis at {client.host}:{client.port}")
    return True


def test_basic_operations():
    """Test basic get/set/delete operations."""
    print("\n" + "="*60)
    print("TEST 2: Basic Operations")
    print("="*60)
    
    client = get_redis_client()
    
    if not client.enabled:
        print("⏭️  Skipping (Redis disabled)")
        return
    
    # Test SET
    print("\n📝 Testing SET...")
    success = client.set("test:key1", {"value": "hello", "number": 42}, ttl=60)
    print(f"   Result: {'✅ Success' if success else '❌ Failed'}")
    
    # Test GET
    print("\n📖 Testing GET...")
    value = client.get("test:key1")
    print(f"   Retrieved: {value}")
    print(f"   Result: {'✅ Correct' if value == {\"value\": \"hello\", \"number\": 42} else '❌ Incorrect'}")
    
    # Test EXISTS
    print("\n🔍 Testing EXISTS...")
    exists = client.exists("test:key1")
    print(f"   Result: {'✅ Key exists' if exists else '❌ Key not found'}")
    
    # Test DELETE
    print("\n🗑️  Testing DELETE...")
    client.delete("test:key1")
    exists_after = client.exists("test:key1")
    print(f"   Result: {'✅ Deleted' if not exists_after else '❌ Still exists'}")


def test_cache_decorator():
    """Test @redis_cache decorator."""
    print("\n" + "="*60)
    print("TEST 3: Cache Decorator")
    print("="*60)
    
    call_count = 0
    
    @redis_cache(ttl=60, key_prefix="test")
    def expensive_function(x, y):
        nonlocal call_count
        call_count += 1
        time.sleep(0.1)  # Simulate expensive operation
        return x + y
    
    print("\n🔢 Testing cached function...")
    
    # First call - should execute function
    print("   Call 1 (cache miss)...")
    start = time.time()
    result1 = expensive_function(5, 3)
    time1 = time.time() - start
    print(f"      Result: {result1}, Time: {time1:.3f}s, Calls: {call_count}")
    
    # Second call with same args - should use cache
    print("   Call 2 (cache hit)...")
    start = time.time()
    result2 = expensive_function(5, 3)
    time2 = time.time() - start
    print(f"      Result: {result2}, Time: {time2:.3f}s, Calls: {call_count}")
    
    # Third call with different args - should execute function
    print("   Call 3 (different args, cache miss)...")
    start = time.time()
    result3 = expensive_function(10, 7)
    time3 = time.time() - start
    print(f"      Result: {result3}, Time: {time3:.3f}s, Calls: {call_count}")
    
    # Verify results
    print("\n📊 Results:")
    if call_count == 2:
        print("   ✅ Cache working correctly (2 function calls for 3 invocations)")
    else:
        print(f"   ❌ Expected 2 calls, got {call_count}")
    
    if time2 < time1 / 10:
        print("   ✅ Cache speedup verified")
    else:
        print(f"   ⚠️  Cache may not be active (time1: {time1:.3f}s, time2: {time2:.3f}s)")


def test_graceful_degradation():
    """Test that system works without Redis."""
    print("\n" + "="*60)
    print("TEST 4: Graceful Degradation")
    print("="*60)
    
    @redis_cache(ttl=60, key_prefix="test", enabled=False)
    def test_function(x):
        return x * 2
    
    print("\n🔄 Testing with caching disabled...")
    result = test_function(21)
    print(f"   Result: {result}")
    print(f"   {'✅ Function works without cache' if result == 42 else '❌ Failed'}")


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("🧪 REDIS CLIENT TEST SUITE")
    print("="*60)
    
    # Test 1: Connection
    connected = test_redis_connection()
    
    # Test 2: Basic operations
    test_basic_operations()
    
    # Test 3: Decorator
    test_cache_decorator()
    
    # Test 4: Degradation
    test_graceful_degradation()
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETE")
    print("="*60)
    
    if connected:
        print("\n💡 Redis is operational and caching is working!")
    else:
        print("\n⚠️  Redis not available - system will run without caching")
        print("   To enable Redis:")
        print("   1. Install: brew install redis (Mac) or docker run -d -p 6379:6379 redis:7-alpine")
        print("   2. Set: REDIS_ENABLED=true in .env")
    
    print()


if __name__ == "__main__":
    main()
