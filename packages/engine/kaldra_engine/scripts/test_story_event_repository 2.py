"""
Test script for StoryEventRepository.

Usage:
    python3 -m src.scripts.test_story_event_repository
"""
import uuid
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.repositories.story_event_repository import StoryEventRepository


def main() -> None:
    print("🧪 Testing StoryEventRepository v1...")
    
    try:
        repo = StoryEventRepository()
        print("✅ Repository initialized")
        
        # 1) List existing events
        print("\n📊 Listing existing events...")
        result = repo.list_events(limit=5)
        
        if "error" in result:
            print(f"❌ Error listing: {result}")
        elif isinstance(result, list):
            print(f"✅ Found {len(result)} events")
            for event in result[:3]:
                print(f"  • {event.get('text', 'N/A')[:50]}")
        
        # 2) Create test event
        test_id = str(uuid.uuid4())
        test_stream = f"test-stream-{uuid.uuid4().hex[:8]}"
        
        print(f"\n➕ Creating test event (stream: {test_stream})...")
        
        event_data = {
            "id": test_id,
            "signal_id": None,  # Can be null
            "stream_id": test_stream,
            "text": "Test story event from repository script",
            "delta144_state": "test_state",
            "polarities": {"order": 0.6, "chaos": 0.4},
            "meta": {"source": "test_script", "version": "v1"}
        }
        
        create_result = repo.create_event(event_data)
        
        if "error" in create_result:
            print(f"❌ Error creating: {create_result}")
        else:
            print(f"✅ Event created")
            if isinstance(create_result, list) and len(create_result) > 0:
                print(f"  • ID: {create_result[0].get('id', 'N/A')[:8]}...")
                print(f"  • Text: {create_result[0].get('text', 'N/A')}")
        
        # 3) List events for this stream
        print(f"\n🔍 Searching events for stream: {test_stream}...")
        stream_events = repo.list_events(stream_id=test_stream, limit=10)
        
        if "error" in stream_events:
            print(f"❌ Error searching: {stream_events}")
        elif isinstance(stream_events, list):
            print(f"✅ Found {len(stream_events)} events for stream")
        
        # 4) Test bulk create
        print("\n📦 Testing bulk create (3 events)...")
        bulk_events = [
            {
                "stream_id": test_stream,
                "text": f"Bulk event {i}",
                "meta": {"bulk_index": i}
            }
            for i in range(3)
        ]
        
        bulk_result = repo.bulk_create_events(bulk_events)
        
        if "error" in bulk_result:
            print(f"❌ Bulk create error: {bulk_result}")
        else:
            print(f"✅ Bulk create successful")
            if isinstance(bulk_result, list):
                print(f"  • Created {len(bulk_result)} events")
        
        # 5) Delete test event
        print(f"\n🗑️ Deleting test event...")
        delete_result = repo.delete_event(test_id)
        
        if "error" in delete_result:
            print(f"❌ Error deleting: {delete_result}")
        else:
            print(f"✅ Event deleted")
        
        # 6) Delete remaining bulk events by stream
        print(f"\n🗑️ Cleaning up bulk events...")
        # Note: delete_by_signal won't work here, would need delete_by_stream
        # For now, just log
        print("ℹ️ Bulk events cleanup skipped (would need manual deletion or delete_by_stream method)")
        
        print("\n🎉 StoryEventRepository test completed!")
        
    except RuntimeError as e:
        print(f"\n❌ Initialization error: {e}")
        print("Check .env configuration")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
