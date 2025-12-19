"""
Archive Manager for KALDRA v2.9 Apps.
Moves app-specific files to _ARCHIVE directories.
"""
import os
import shutil
from pathlib import Path

ROOT_DIR = Path("/Users/niki/Desktop/kaldra_core")
APPS_DIR = ROOT_DIR / "src/apps"

# Files to archive by app
ARCHIVE_MAP = {
    "alpha": [
        "analyzer.py",
        "earnings_analyzer.py",
        "earnings_ingest.py",
        "earnings_pipeline.py",
        "ingest.py"
    ],
    "geo": [
        "geo_analyzer.py",
        "geo_ingest.py",
        "geo_risk_engine.py",
        "geo_signals.py"
    ],
    "product": [
        "product_analyzer.py",
        "product_ingest.py",
        "product_kindra_mapping.py"
    ],
    "safeguard": [
        "bias_monitor.py",
        "narrative_guard.py",
        "toxicity_detector.py"
    ]
}

def create_archive_readme(app_name: str, archive_dir: Path):
    """Create README in archive directory."""
    readme_content = f"""# KALDRA {app_name.title()} App - Archive

**Status:** Archived (v2.9 Freeze)  
**Date:** November 30, 2025

## Purpose

This directory contains the **{app_name.title()} App** implementation from KALDRA v2.x line.

These files represent:
- Early prototypes of app-specific logic
- Vision for domain-specific KALDRA applications
- Reference implementations for v3.0 Unification Layer

## Status

**NOT ACTIVE** - These files are not integrated into the main KALDRA pipeline.

They are preserved for:
1. Historical reference
2. Potential reuse in v3.0 Apps layer
3. Documentation of design patterns

## v3.0 Migration

The v3.0 Unification Layer will:
- Redesign the Apps architecture
- May reuse concepts from these files
- Will NOT directly depend on this code

## Files

"""
    
    files = ARCHIVE_MAP.get(app_name, [])
    for f in files:
        readme_content += f"- `{f}`\n"
    
    readme_content += "\n## See Also\n\n"
    readme_content += "- `docs/core/DEAD_CODE_TRIAGE_V2.9.md`\n"
    readme_content += "- `docs/core/KALDRA_V2.9_FREEZE_NOTE.md`\n"
    
    readme_path = archive_dir / "README_ARCHIVE.md"
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"Created: {readme_path}")

def archive_app_files():
    """Archive app files to _ARCHIVE directories."""
    print("Starting App Archival Process...")
    
    for app_name, files in ARCHIVE_MAP.items():
        app_dir = APPS_DIR / app_name
        archive_dir = APPS_DIR / "_ARCHIVE" / app_name
        
        # Create archive directory
        os.makedirs(archive_dir, exist_ok=True)
        print(f"\nCreated archive directory: {archive_dir}")
        
        # Move files
        for filename in files:
            src = app_dir / filename
            dst = archive_dir / filename
            
            if src.exists():
                shutil.move(str(src), str(dst))
                print(f"  Moved: {filename}")
            else:
                print(f"  Skipped (not found): {filename}")
        
        # Create README
        create_archive_readme(app_name, archive_dir)
    
    print("\nApp Archival Complete.")

if __name__ == "__main__":
    archive_app_files()
