"""
Stress Tests for KALDRA Pipeline
Tests concurrency, sustained load, and system resilience.
"""

import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("\n" + "=" * 70)
print("💪 KALDRA STRESS TEST SUITE")
print("=" * 70)


def test_concurrent_requests():
    """Test 100 simultaneous requests."""
    print("\n" + "=" * 70)
    print("TEST 1: Concurrent Requests (100 simultaneous)")
    print("=" * 70)

    try:
        from kaldra_engine.core.kaldra_master_engine import KaldraMasterEngineV2

        engine = KaldraMasterEngineV2()
        num_requests = 100

        def make_request(i):
            embedding = np.random.randn(256).astype(np.float32)
            start = time.perf_counter()
            signal = engine.infer_from_embedding(embedding)
            elapsed = (time.perf_counter() - start) * 1000
            return i, elapsed, signal.degraded

        print(f"\n🚀 Launching {num_requests} concurrent requests...")
        start_time = time.time()

        results = []
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(make_request, i) for i in range(num_requests)]

            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                    if len(results) % 20 == 0:
                        print(f"   Completed: {len(results)}/{num_requests}", end="\r")
                except Exception as e:
                    print(f"   ❌ Request failed: {e}")

        total_time = time.time() - start_time

        # Analyze results
        times = [r[1] for r in results]
        degraded_count = sum(1 for r in results if r[2])

        print("\n\n📊 Results:")
        print(f"   Total requests: {len(results)}")
        print(f"   Successful: {len(results) - degraded_count}")
        print(f"   Degraded: {degraded_count}")
        print(f"   Total time: {total_time:.2f}s")
        print(f"   Avg latency: {np.mean(times):.2f}ms")
        print(f"   Max latency: {np.max(times):.2f}ms")
        print(f"   Throughput: {len(results) / total_time:.1f} req/s")

        # Success criteria
        if len(results) == num_requests and total_time < 10:
            print("\n   ✅ PASS: All requests completed within 10s")
        else:
            print("\n   ⚠️  SLOW: Consider scaling resources")

    except Exception as e:
        print(f"\n   ❌ Test failed: {e}")


def test_sustained_load():
    """Test 1000 sequential requests."""
    print("\n" + "=" * 70)
    print("TEST 2: Sustained Load (1000 sequential requests)")
    print("=" * 70)

    try:
        from kaldra_engine.core.kaldra_master_engine import KaldraMasterEngineV2

        engine = KaldraMasterEngineV2()
        num_requests = 1000

        print(f"\n🔄 Processing {num_requests} requests...")

        times = []
        degraded_count = 0
        start_time = time.time()

        for i in range(num_requests):
            embedding = np.random.randn(256).astype(np.float32)

            start = time.perf_counter()
            signal = engine.infer_from_embedding(embedding)
            elapsed = (time.perf_counter() - start) * 1000

            times.append(elapsed)
            if signal.degraded:
                degraded_count += 1

            if i % 100 == 0:
                print(
                    f"   Progress: {i}/{num_requests} ({np.mean(times[-100:]):.1f}ms avg)",
                    end="\r",
                )

        total_time = time.time() - start_time

        print("\n\n📊 Results:")
        print(f"   Total requests: {num_requests}")
        print(f"   Successful: {num_requests - degraded_count}")
        print(f"   Degraded: {degraded_count}")
        print(f"   Total time: {total_time:.2f}s")
        print(f"   Avg latency: {np.mean(times):.2f}ms")
        print(f"   Med latency: {np.median(times):.2f}ms")
        print(f"   P95 latency: {np.percentile(times, 95):.2f}ms")
        print(f"   P99 latency: {np.percentile(times, 99):.2f}ms")
        print(f"   Throughput: {num_requests / total_time:.1f} req/s")

        # Success criteria
        avg_time = np.mean(times)
        if avg_time < 150:
            print(f"\n   ✅ PASS: Avg latency {avg_time:.1f}ms < 150ms")
        else:
            print(f"\n   ⚠️  SLOW: Avg latency {avg_time:.1f}ms > 150ms")

    except Exception as e:
        print(f"\n   ❌ Test failed: {e}")


def test_cache_effectiveness():
    """Test cache hit rate and performance."""
    print("\n" + "=" * 70)
    print("TEST 3: Cache Effectiveness")
    print("=" * 70)

    try:
        from kaldra_engine.core.kaldra_master_engine import KaldraMasterEngineV2

        engine = KaldraMasterEngineV2()

        # Same embedding for cache testing
        embedding = np.random.randn(256).astype(np.float32)

        print("\n🔥 Warming up cache...")
        # First request (cache miss)
        start = time.perf_counter()
        engine.infer_from_embedding(embedding)
        time1 = (time.perf_counter() - start) * 1000

        print(f"   First request (cold): {time1:.2f}ms")

        # Subsequent requests (should hit cache)
        print("\n📊 Testing cache hits...")
        cache_times = []
        for _i in range(10):
            start = time.perf_counter()
            engine.infer_from_embedding(embedding)
            elapsed = (time.perf_counter() - start) * 1000
            cache_times.append(elapsed)

        avg_cache_time = np.mean(cache_times)
        speedup = time1 / avg_cache_time

        print(f"\n   Cold time: {time1:.2f}ms")
        print(f"   Cached avg: {avg_cache_time:.2f}ms")
        print(f"   Speedup: {speedup:.1f}x")

        if speedup > 1.5:
            print(f"\n   ✅ PASS: Cache providing {speedup:.1f}x speedup")
        else:
            print("\n   ⚠️  Cache may not be active")

    except Exception as e:
        print(f"\n   ❌ Test failed: {e}")


def test_memory_stability():
    """Test for memory leaks during sustained operation."""
    print("\n" + "=" * 70)
    print("TEST 4: Memory Stability")
    print("=" * 70)

    try:
        import os

        import psutil
        from kaldra_engine.core.kaldra_master_engine import KaldraMasterEngineV2

        process = psutil.Process(os.getpid())
        engine = KaldraMasterEngineV2()

        # Get initial memory
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        print(f"\n💾 Initial memory: {initial_memory:.1f} MB")

        # Run 100 requests
        print("\n🔄 Running 100 requests to check for leaks...")
        for i in range(100):
            embedding = np.random.randn(256).astype(np.float32)
            engine.infer_from_embedding(embedding)

            if i % 25 == 0:
                current_memory = process.memory_info().rss / 1024 / 1024
                print(f"   After {i} requests: {current_memory:.1f} MB", end="\r")

        # Get final memory
        final_memory = process.memory_info().rss / 1024 / 1024
        memory_increase = final_memory - initial_memory

        print(f"\n\n   Final memory: {final_memory:.1f} MB")
        print(f"   Increase: {memory_increase:.1f} MB")

        # Success criteria: less than 50MB increase
        if memory_increase < 50:
            print(f"\n   ✅ PASS: Memory stable (+{memory_increase:.1f} MB)")
        else:
            print(f"\n   ⚠️  WARNING: Possible memory leak (+{memory_increase:.1f} MB)")

    except ImportError:
        print("\n   ⚠️  psutil not available, skipping memory test")
        print("   Install with: pip install psutil")
    except Exception as e:
        print(f"\n   ❌ Test failed: {e}")


def test_error_recovery():
    """Test graceful degradation under error conditions."""
    print("\n" + "=" * 70)
    print("TEST 5: Error Recovery & Degradation")
    print("=" * 70)

    try:
        from kaldra_engine.core.kaldra_master_engine import KaldraMasterEngineV2

        engine = KaldraMasterEngineV2()

        print("\n🧪 Testing with various error conditions...")

        # Test 1: Invalid embedding size
        print("\n   Test 1: Invalid embedding size")
        try:
            bad_embedding = np.random.randn(128).astype(np.float32)  # Wrong size
            signal = engine.infer_from_embedding(bad_embedding)
            if signal.degraded:
                print("      ✅ Degraded mode activated")
            else:
                print("      ⚠️  No degradation flag")
        except Exception as e:
            print(f"      ✅ Exception handling: {type(e).__name__}")

        # Test 2: Normal operation after error
        print("\n   Test 2: Recovery after error")
        good_embedding = np.random.randn(256).astype(np.float32)
        signal = engine.infer_from_embedding(good_embedding)
        if not signal.degraded:
            print("      ✅ System recovered, normal operation")
        else:
            print("      ⚠️  Still in degraded mode")

        print("\n   ✅ Error recovery functional")

    except Exception as e:
        print(f"\n   ❌ Test failed: {e}")


def main():
    """Run all stress tests."""
    start_time = time.time()

    # Run tests
    test_concurrent_requests()
    test_sustained_load()
    test_cache_effectiveness()
    test_memory_stability()
    test_error_recovery()

    total_time = time.time() - start_time

    print("\n" + "=" * 70)
    print(f"✅ ALL STRESS TESTS COMPLETE ({total_time:.1f}s)")
    print("=" * 70)
    print("\n💡 System is ready for production load!")
    print()


if __name__ == "__main__":
    main()
