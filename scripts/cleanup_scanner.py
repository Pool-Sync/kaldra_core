"""
Cleanup Scanner for KALDRA v2.9.
Scans the repository for redundant, obsolete, and legacy files.
"""
import os
import re
import json
import hashlib
from pathlib import Path
from typing import List, Set, Dict

ROOT_DIR = Path("/Users/niki/Desktop/kaldra_core")
SRC_DIR = ROOT_DIR / "src"
DOCS_DIR = ROOT_DIR / "docs"
SCHEMA_DIR = ROOT_DIR / "schema"

def get_all_files(directory: Path, extensions: Set[str] = None) -> List[Path]:
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if extensions and Path(filename).suffix not in extensions:
                continue
            files.append(Path(root) / filename)
    return files

def find_duplicate_schemas() -> Dict[str, List[Path]]:
    schema_files = get_all_files(SCHEMA_DIR, {".json"})
    content_hashes = {}
    duplicates = {}
    
    for file_path in schema_files:
        try:
            with open(file_path, "rb") as f:
                content = f.read()
                file_hash = hashlib.md5(content).hexdigest()
                
            if file_hash in content_hashes:
                if file_hash not in duplicates:
                    duplicates[file_hash] = [content_hashes[file_hash]]
                duplicates[file_hash].append(file_path)
            else:
                content_hashes[file_hash] = file_path
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            
    return duplicates

def find_unused_schemas() -> List[Path]:
    schema_files = get_all_files(SCHEMA_DIR, {".json"})
    code_files = get_all_files(SRC_DIR, {".py"})
    
    used_schemas = set()
    for code_file in code_files:
        try:
            with open(code_file, "r") as f:
                content = f.read()
                for schema_file in schema_files:
                    if schema_file.name in content:
                        used_schemas.add(schema_file)
        except Exception:
            pass
            
    return [s for s in schema_files if s not in used_schemas]

def find_legacy_docs() -> List[Path]:
    doc_files = get_all_files(DOCS_DIR, {".md"})
    legacy_patterns = [r"v1", r"v2\.0", r"v2\.1", r"v2\.2", r"legacy", r"old"]
    legacy_files = []
    
    for doc_file in doc_files:
        if any(re.search(p, doc_file.name, re.IGNORECASE) for p in legacy_patterns):
            legacy_files.append(doc_file)
            
    return legacy_files

def find_simulation_code() -> List[Path]:
    code_files = get_all_files(SRC_DIR, {".py"})
    simulation_files = []
    
    for code_file in code_files:
        try:
            with open(code_file, "r") as f:
                content = f.read()
                if "simulation stub" in content.lower() or "legacy simulation" in content.lower():
                    simulation_files.append(code_file)
        except Exception:
            pass
            
    return simulation_files

def find_dead_notebooks() -> List[Path]:
    return get_all_files(ROOT_DIR, {".ipynb"})

def generate_report():
    report_lines = ["# KALDRA Cleanup Report v2.9", "", f"Generated on: {os.popen('date').read().strip()}", ""]
    
    # 1. Duplicate Schemas
    duplicates = find_duplicate_schemas()
    report_lines.append("## 1. Duplicate Schemas")
    if duplicates:
        for hash_val, files in duplicates.items():
            report_lines.append(f"- Hash {hash_val[:8]}:")
            for f in files:
                report_lines.append(f"  - {f.relative_to(ROOT_DIR)}")
    else:
        report_lines.append("None found.")
    report_lines.append("")

    # 2. Unused Schemas
    unused = find_unused_schemas()
    report_lines.append("## 2. Potentially Unused Schemas")
    if unused:
        for f in unused:
            report_lines.append(f"- {f.relative_to(ROOT_DIR)}")
    else:
        report_lines.append("None found.")
    report_lines.append("")

    # 3. Legacy Docs
    legacy_docs = find_legacy_docs()
    report_lines.append("## 3. Legacy Documentation (Pre-v2.3)")
    if legacy_docs:
        for f in legacy_docs:
            report_lines.append(f"- {f.relative_to(ROOT_DIR)}")
    else:
        report_lines.append("None found.")
    report_lines.append("")
    
    # 4. Simulation Code
    sim_code = find_simulation_code()
    report_lines.append("## 4. Simulation/Legacy Code")
    if sim_code:
        for f in sim_code:
            report_lines.append(f"- {f.relative_to(ROOT_DIR)}")
    else:
        report_lines.append("None found.")
    report_lines.append("")

    # 5. Dead Notebooks
    notebooks = find_dead_notebooks()
    report_lines.append("## 5. Dead Notebooks")
    if notebooks:
        for f in notebooks:
            report_lines.append(f"- {f.relative_to(ROOT_DIR)}")
    else:
        report_lines.append("None found.")
    report_lines.append("")

    report_content = "\n".join(report_lines)
    
    output_path = DOCS_DIR / "core" / "CLEANUP_REPORT_V2.9.md"
    os.makedirs(output_path.parent, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(report_content)
    
    print(f"Report generated at: {output_path}")

if __name__ == "__main__":
    generate_report()
