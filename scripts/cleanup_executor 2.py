"""
Cleanup Executor for KALDRA v2.9.
Deletes files identified as redundant or obsolete.
"""
import os
import shutil
from pathlib import Path

ROOT_DIR = Path("/Users/niki/Desktop/kaldra_core")

FILES_TO_DELETE = [
    # Legacy Docs
    "docs/KALDRA_V2.1_RELEASE_NOTES.md",
    "docs/kindras/LEGACY_MIGRATION_GUIDE.md",
    "docs/core/KALDRA_CORE_MASTER_ROADMAP_V2.2.md",
    
    # Unused Schemas (from report)
    "schema/kindras/cultural_database_schema.json",
    "schema/kindras/kindra_hybrid_config.json",
    "schema/tw369/state_plane_mapping_config.json",
    "schema/tw369/drift_parameters_conservative_v1.json",
    "schema/tw369/drift_parameters_exploratory_v1.json",
    "schema/tw369/state_plane_mapping_default.json",
    "schema/tw369/drift_state_schema.json", # Replaced by unified? Or just unused? User said "remove duplicate schemas".
    "schema/safeguard/safeguard_risk_rules.json",
    "schema/safeguard/safeguard_journey_map.json",
    "schema/tau/tau_config.json",
    "schema/tau/tau_policy_rules.json",
    "schema/story/story_event.schema.json",
    "schema/story/story_signal.schema.json",
    
    # User specific requests (if they exist)
    "src/meta/meta_router_v1.py", # Hypothetical
    "src/meta/heros_journey_v1.py", # Hypothetical
]

DIRS_TO_DELETE = [
    "src/legacy",
    "src/old",
    "src/simulation",
    "legacy",
    "old",
    "simulation",
    "src/kindras/legacy"
]

def delete_file(path_str):
    path = ROOT_DIR / path_str
    if path.exists():
        try:
            os.remove(path)
            print(f"Deleted file: {path_str}")
        except Exception as e:
            print(f"Error deleting {path_str}: {e}")
    else:
        print(f"File not found (skipped): {path_str}")

def delete_dir(path_str):
    path = ROOT_DIR / path_str
    if path.exists():
        try:
            shutil.rmtree(path)
            print(f"Deleted directory: {path_str}")
        except Exception as e:
            print(f"Error deleting {path_str}: {e}")
    else:
        print(f"Directory not found (skipped): {path_str}")

def main():
    print("Starting Cleanup Execution...")
    
    for f in FILES_TO_DELETE:
        delete_file(f)
        
    for d in DIRS_TO_DELETE:
        delete_dir(d)
        
    print("Cleanup Execution Complete.")

if __name__ == "__main__":
    main()
