"""
Code Coverage Analyzer for KALDRA v2.9.
Identifies potentially dead/unused Python files.
"""
import os
import ast
from pathlib import Path
from typing import Set, Dict, List

ROOT_DIR = Path("/Users/niki/Desktop/kaldra_core")
SRC_DIR = ROOT_DIR / "src"

def get_all_python_files(directory: Path) -> List[Path]:
    """Get all Python files in directory."""
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.py'):
                files.append(Path(root) / filename)
    return files

def extract_imports(file_path: Path) -> Set[str]:
    """Extract all import statements from a Python file."""
    imports = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=str(file_path))
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split('.')[0])
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
    
    return imports

def build_import_graph() -> Dict[str, Set[str]]:
    """Build a graph of which files import which modules."""
    graph = {}
    all_files = get_all_python_files(SRC_DIR)
    
    for file_path in all_files:
        relative = file_path.relative_to(SRC_DIR)
        module_name = str(relative).replace('/', '.').replace('.py', '')
        imports = extract_imports(file_path)
        graph[str(relative)] = imports
    
    return graph

def find_potentially_dead_files() -> List[Path]:
    """Find Python files that are never imported."""
    all_files = get_all_python_files(SRC_DIR)
    graph = build_import_graph()
    
    # Get all module names
    all_modules = set()
    for file_path in all_files:
        relative = file_path.relative_to(SRC_DIR)
        module_name = str(relative).replace('/', '.').replace('.py', '').replace('.__init__', '')
        all_modules.add(module_name)
    
    # Get all imported modules
    imported = set()
    for imports in graph.values():
        imported.update(imports)
    
    # Files that are never imported (excluding __init__.py and main entry points)
    dead_files = []
    for file_path in all_files:
        relative = file_path.relative_to(SRC_DIR)
        
        # Skip __init__.py and known entry points
        if file_path.name == '__init__.py':
            continue
        if 'main' in file_path.name.lower():
            continue
        if file_path.name in ['config.py', 'constants.py']:
            continue
            
        module_name = str(relative).replace('/', '.').replace('.py', '')
        
        # Check if this module is imported anywhere
        is_imported = False
        for imp in imported:
            if module_name.startswith(imp) or imp.startswith(module_name.split('.')[0]):
                is_imported = True
                break
        
        if not is_imported:
            dead_files.append(file_path)
    
    return dead_files

def generate_coverage_report():
    """Generate coverage report."""
    report_lines = [
        "# KALDRA Code Coverage Report v2.9",
        "",
        f"Generated on: {os.popen('date').read().strip()}",
        "",
        "## Summary",
        "",
        "This report identifies potentially unused Python files in the KALDRA codebase.",
        "",
        "## Methodology",
        "",
        "- Scanned all Python files in `src/`",
        "- Built import dependency graph",
        "- Identified files that are never imported",
        "- Excluded: `__init__.py`, `*main*.py`, `config.py`",
        "",
        "## Potentially Dead Files",
        ""
    ]
    
    dead_files = find_potentially_dead_files()
    
    if dead_files:
        report_lines.append(f"Found {len(dead_files)} potentially unused files:")
        report_lines.append("")
        for f in sorted(dead_files):
            report_lines.append(f"- {f.relative_to(ROOT_DIR)}")
    else:
        report_lines.append("✅ No obviously dead files detected.")
    
    report_lines.extend([
        "",
        "## Recommendations",
        "",
        "1. **Review** each file listed above",
        "2. **Verify** it's truly unused (may be used dynamically or in tests)",
        "3. **Archive or Delete** confirmed dead code",
        "",
        "## Notes",
        "",
        "- This is a heuristic analysis",
        "- Dynamic imports (e.g., `importlib`) are not detected",
        "- Test files may import modules not shown here",
        "- Entry points and scripts may not be imported but are still needed",
        ""
    ])
    
    output_path = ROOT_DIR / "docs/core/COVERAGE_REPORT_V2.9.md"
    with open(output_path, 'w') as f:
        f.write('\n'.join(report_lines))
    
    print(f"Coverage report generated at: {output_path}")
    print(f"Found {len(dead_files)} potentially dead files.")

if __name__ == "__main__":
    generate_coverage_report()
