import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Set
import re


def analyze_unused_dependencies(repo_path: Path) -> Dict[str, Any]:
    """Analyze package.json for unused dependencies in JavaScript/TypeScript projects.
    
    Args:
        repo_path: Path to the repository.
    
    Returns:
        Dictionary with unused dependencies information.
    """
    package_json_path = repo_path / 'package.json'
    
    if not package_json_path.exists():
        return {
            'has_package_json': False,
            'unused_dependencies': [],
            'unused_dev_dependencies': [],
            'total_dependencies': 0,
            'total_dev_dependencies': 0
        }
    
    try:
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)
        
        dependencies = package_data.get('dependencies', {})
        dev_dependencies = package_data.get('devDependencies', {})
        
        # Get all JS/TS files
        code_files = []
        for ext in ['*.js', '*.jsx', '*.ts', '*.tsx']:
            code_files.extend(repo_path.rglob(ext))
        
        # Filter out node_modules
        code_files = [f for f in code_files if 'node_modules' not in f.parts]
        
        # Find all imports/requires in code
        imported_packages = set()
        for file in code_files:
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Match import statements: import ... from 'package'
                    import_matches = re.findall(r"import\s+.*?\s+from\s+['\"]([^'\"]+)['\"]", content)
                    imported_packages.update(import_matches)
                    
                    # Match require statements: require('package')
                    require_matches = re.findall(r"require\(['\"]([^'\"]+)[\"\']", content)
                    imported_packages.update(require_matches)
                    
                    # Match dynamic imports: import('package')
                    dynamic_import_matches = re.findall(r"import\(['\"]([^'\"]+)[\"\']", content)
                    imported_packages.update(dynamic_import_matches)
            except Exception:
                continue
        
        # Extract base package names (remove paths like 'package/subpath')
        base_packages = set()
        for pkg in imported_packages:
            # Handle scoped packages (@scope/package)
            if pkg.startswith('@'):
                parts = pkg.split('/')
                if len(parts) >= 2:
                    base_packages.add(f"{parts[0]}/{parts[1]}")
            else:
                # Regular packages
                base_packages.add(pkg.split('/')[0])
        
        # Find unused dependencies
        unused_deps = []
        for dep in dependencies.keys():
            if dep not in base_packages:
                unused_deps.append(dep)
        
        unused_dev_deps = []
        for dep in dev_dependencies.keys():
            if dep not in base_packages:
                unused_dev_deps.append(dep)
        
        return {
            'has_package_json': True,
            'unused_dependencies': unused_deps,
            'unused_dev_dependencies': unused_dev_deps,
            'total_dependencies': len(dependencies),
            'total_dev_dependencies': len(dev_dependencies),
            'dependency_usage_rate': ((len(dependencies) - len(unused_deps)) / len(dependencies) * 100) if dependencies else 100
        }
    except Exception as e:
        return {
            'has_package_json': True,
            'error': str(e),
            'unused_dependencies': [],
            'unused_dev_dependencies': [],
            'total_dependencies': 0,
            'total_dev_dependencies': 0
        }


def analyze_unused_python_packages(repo_path: Path) -> Dict[str, Any]:
    """Analyze Python requirements for unused packages.
    
    Args:
        repo_path: Path to the repository.
    
    Returns:
        Dictionary with unused package information.
    """
    # Check for requirements files
    req_files = [
        repo_path / 'requirements.txt',
        repo_path / 'requirements-dev.txt',
        repo_path / 'requirements' / 'base.txt'
    ]
    
    req_file = None
    for f in req_files:
        if f.exists():
            req_file = f
            break
    
    if not req_file:
        return {
            'has_requirements': False,
            'unused_packages': [],
            'total_packages': 0
        }
    
    try:
        with open(req_file, 'r') as f:
            requirements = f.readlines()
        
        # Extract package names (ignore version specifiers)
        required_packages = set()
        for line in requirements:
            line = line.strip()
            if line and not line.startswith('#'):
                # Remove version specifiers
                pkg = re.split(r'[<>=!]', line)[0].strip()
                if pkg:
                    required_packages.add(pkg.lower())
        
        # Get all Python files
        py_files = list(repo_path.rglob('*.py'))
        py_files = [f for f in py_files if not any(exc in f.parts for exc in {'venv', 'env', '__pycache__', 'site-packages'})]
        
        # Find all imports
        imported_packages = set()
        for file in py_files:
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Match import statements
                    import_matches = re.findall(r'^import\s+(\w+)', content, re.MULTILINE)
                    imported_packages.update(import_matches)
                    
                    # Match from ... import statements
                    from_matches = re.findall(r'^from\s+(\w+)', content, re.MULTILINE)
                    imported_packages.update(from_matches)
            except Exception:
                continue
        
        # Normalize package names
        imported_packages = {pkg.lower().replace('_', '-') for pkg in imported_packages}
        required_packages = {pkg.lower().replace('_', '-') for pkg in required_packages}
        
        # Find unused packages
        unused = [pkg for pkg in required_packages if pkg not in imported_packages and pkg not in {'pip', 'setuptools', 'wheel'}]
        
        return {
            'has_requirements': True,
            'unused_packages': unused,
            'total_packages': len(required_packages),
            'package_usage_rate': ((len(required_packages) - len(unused)) / len(required_packages) * 100) if required_packages else 100
        }
    except Exception as e:
        return {
            'has_requirements': True,
            'error': str(e),
            'unused_packages': [],
            'total_packages': 0
        }
