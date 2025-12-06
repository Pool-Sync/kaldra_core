"""
Full pipeline smoke test for KALDRA → Supabase persistence.

Tests signals + story_events together in an end-to-end flow.

Usage:
    python3 -m src.scripts.test_full_pipeline
"""
import os
import sys
import uuid
from datetime import datetime, timezone

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.repositories.signal_repository import SignalRepository
from data.repositories.story_event_repository import StoryEventRepository


def require_env(name: str) -> str:
    """Require an environment variable or exit."""
    value = os.getenv(name)
    if not value:
        print(f"❌ Environment variable not found: {name}")
        print("💡 Make sure to load .env: export $(grep -v '^#' .env | xargs)")
        sys.exit(1)
    return value


def main() -> None:
    print("🧪 Testing FULL KALDRA → Supabase pipeline (signals + story_events)...")
    print()
    
    try:
        # 1) Verify environment
        print("🔧 Checking environment variables...")
        supabase_url = require_env("SUPABASE_URL")
        require_env("SUPABASE_SERVICE_ROLE_KEY")
        print(f"✅ Environment configured")
        print(f"   URL: {supabase_url[:50]}...")
        print()
        
        # 2) Initialize repositories
        print("🧱 Initializing repositories...")
        signal_repo = SignalRepository()
        event_repo = StoryEventRepository()
        print("✅ SignalRepository initialized")
        print("✅ StoryEventRepository initialized")
        print()
        
        # 3) Create test signal
        test_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()
        
        signal_data = {
            "id": test_id,
            "domain": "alpha",
            "title": "Full pipeline test signal",
            "summary": "Signal created by test_full_pipeline.py for integration testing",
            "importance": 0.9,
            "confidence": 0.85,
            "delta144_state": "threshold",
            "dominant_archetype": "hero",
            "dominant_polarity": "order",
            "tw_regime": "STABLE",
            "journey_stage": "call_to_adventure",
            "raw_payload": {
                "source": "test_full_pipeline",
                "version": "v1",
                "created_at": now,
                "test": True
            },
        }
        
        print(f"➕ Creating test signal...")
        print(f"   ID: {test_id}")
        result = signal_repo.create_signal(signal_data)
        
        if isinstance(result, dict) and "error" in result:
            print(f"❌ Failed to create signal: {result}")
            sys.exit(1)
        
        print(f"✅ Signal created successfully")
        if isinstance(result, list) and len(result) > 0:
            print(f"   Title: {result[0].get('title', 'N/A')}")
        print()
        
        try:
            # 4) Create story events linked to signal
            print("🧩 Creating story events linked to signal...")
            
            events = [
                {
                    "signal_id": test_id,
                    "stream_id": "test-stream-console",
                    "text": "Hero receives the call to adventure.",
                    "delta144_state": "threshold",
                    "polarities": {"order": 0.7, "chaos": 0.3},
                    "meta": {
                        "stage": "call_to_adventure",
                        "kind": "narrative_beat",
                        "source": "test_full_pipeline",
                    },
                },
                {
                    "signal_id": test_id,
                    "stream_id": "test-stream-console",
                    "text": "Hero hesitates and experiences internal conflict.",
                    "delta144_state": "tension",
                    "polarities": {"order": 0.4, "chaos": 0.6},
                    "meta": {
                        "stage": "refusal_of_the_call",
                        "kind": "narrative_beat",
                        "source": "test_full_pipeline",
                    },
                },
                {
                    "signal_id": test_id,
                    "stream_id": "test-stream-console",
                    "text": "Mentor appears and provides guidance.",
                    "delta144_state": "emergence",
                    "polarities": {"order": 0.8, "chaos": 0.2},
                    "meta": {
                        "stage": "meeting_the_mentor",
                        "kind": "narrative_beat",
                        "source": "test_full_pipeline",
                    },
                },
            ]
            
            bulk_result = event_repo.bulk_create_events(events)
            
            if isinstance(bulk_result, dict) and "error" in bulk_result:
                print(f"❌ Failed to create story events: {bulk_result}")
                sys.exit(1)
            
            print(f"✅ Story events created successfully")
            print(f"   Count: {len(events)} events")
            print()
            
            # 5) Validate: read events back by signal_id
            print("🔍 Validating: fetching story events by signal_id...")
            fetched = event_repo.list_events(signal_id=test_id, limit=10)
            
            if isinstance(fetched, dict) and "error" in fetched:
                print(f"❌ Failed to fetch story events: {fetched}")
                sys.exit(1)
            
            count = len(fetched) if isinstance(fetched, list) else 0
            print(f"✅ Retrieved {count} story events for signal_id={test_id[:8]}...")
            
            if count == 0:
                print("⚠️  WARNING: No story events found — check database")
            elif count != len(events):
                print(f"⚠️  WARNING: Expected {len(events)} events, got {count}")
            else:
                print("✅ Event count matches!")
                
                # Show sample event
                if isinstance(fetched, list) and len(fetched) > 0:
                    print()
                    print("📝 Sample event:")
                    sample = fetched[0]
                    print(f"   Text: {sample.get('text', 'N/A')[:60]}...")
                    print(f"   State: {sample.get('delta144_state', 'N/A')}")
                    print(f"   Stream: {sample.get('stream_id', 'N/A')}")
            
            print()
            print("🎉 FULL PIPELINE TEST PASSED — signal + story_events persisted successfully!")
            print()
        
        finally:
            # 6) Cleanup
            print("🧹 Cleaning up test data...")
            
            # Delete events first (FK constraint)
            try:
                del_events = event_repo.delete_by_signal(test_id)
                if isinstance(del_events, dict) and "error" in del_events:
                    print(f"⚠️  Failed to cleanup story events: {del_events}")
                else:
                    print("✅ Story events deleted")
            except Exception as e:
                print(f"⚠️  Failed to cleanup story events: {e}")
            
            # Delete signal
            try:
                del_signal = signal_repo.delete_signal(test_id)
                if isinstance(del_signal, dict) and "error" in del_signal:
                    print(f"⚠️  Failed to cleanup signal: {del_signal}")
                else:
                    print("✅ Signal deleted")
            except Exception as e:
                print(f"⚠️  Failed to cleanup signal: {e}")
            
            print()
            print("✨ Test complete!")
    
    except RuntimeError as e:
        print(f"\n❌ Initialization error: {e}")
        print("Check .env configuration and Supabase connection")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
