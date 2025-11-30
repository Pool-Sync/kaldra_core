"""
Archive Manager for KALDRA v2.9.
Moves legacy documentation to _ARCHIVE.
"""
import os
import shutil
from pathlib import Path

ROOT_DIR = Path("/Users/niki/Desktop/kaldra_core")
ARCHIVE_DIR = ROOT_DIR / "docs/core/_ARCHIVE"

# Files to move to archive
FILES_TO_ARCHIVE = [
    "docs/KALDRA_ARCHITECTURE_OVERVIEW.md", # Likely old
    "docs/REPOSITORY_STRUCTURE.md", # Likely old
    "docs/KALDRA_CLOUD_ROADMAP.md", # Check if old
    "docs/KALDRA_V2.3_CLEAN_STRUCTURE_PROPOSAL.md",
    "docs/KALDRA_V2.3_RECONCILIATION_REPORT.md",
    "docs/KALDRA_V2.3_TRUTH_TABLE.md",
    "docs/KALDRA_IDENTITY_VERIFICATION.md", # Seems old
    "docs/KALDRA_FUTURE_STEPS.md", # Likely superseded by roadmap
]

def move_to_archive(path_str):
    src_path = ROOT_DIR / path_str
    if src_path.exists():
        dst_path = ARCHIVE_DIR / src_path.name
        try:
            shutil.move(str(src_path), str(dst_path))
            print(f"Archived: {path_str} -> {dst_path}")
        except Exception as e:
            print(f"Error archiving {path_str}: {e}")
    else:
        print(f"File not found (skipped): {path_str}")

def main():
    print("Starting Archive Process...")
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    
    for f in FILES_TO_ARCHIVE:
        move_to_archive(f)
        
    print("Archive Process Complete.")

if __name__ == "__main__":
    main()
