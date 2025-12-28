import subprocess
from pathlib import Path
from typing import Dict, Any
import re


def analyze_lizard(repo_path: Path) -> Dict[str, Any]:
    """Analyze code using Lizard and return metrics.

    Args:
        repo_path: Path to the repository.

    Returns:
        Dictionary with lizard metrics.
    """
    try:
        # Analyze Python, JS, TS, JSX, TSX files for broader support
        exts = ["*.py", "*.js", "*.jsx", "*.ts", "*.tsx"]
        code_files = []
        
        # Try common source directories first, then fallback to entire repo
        search_dirs = [repo_path / d for d in ["server", "src", "lib", "app"]]
        search_dirs = [d for d in search_dirs if d.exists()]
        
        if not search_dirs:
            search_dirs = [repo_path]
        
        # Collect code files from search directories
        for search_dir in search_dirs:
            for ext in exts:
                code_files.extend(search_dir.rglob(ext))
        
        # Filter out common non-source directories
        excluded_dirs = {'node_modules', 'venv', '__pycache__', 'dist', 'build', '.git', 'coverage', '.next'}
        code_files = [f for f in code_files if not any(exc in f.parts for exc in excluded_dirs)]
        
        if not code_files:
            return {
                'avg_ccn': 0,
                'max_ccn': 0,
                'pct_ccn_gt_10': 0,
                'functions_gt_7_params': 0,
                'duplication_pct': 0,
                'risky_functions': []
            }
        lizard_cmd = ['lizard'] + [str(f) for f in code_files]
        result = subprocess.run(
            lizard_cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode != 0:
            raise Exception(f"Lizard failed: {result.stderr}")

        output = result.stdout
        lines = output.split('\n')
        functions = []
        parsing = False
        for line in lines:
            if 'NLOC' in line and 'CCN' in line:
                parsing = True
                continue
            if parsing and line.strip() and not line.startswith('-') and not line.startswith('=') and not 'Total' in line and not 'analyzed' in line:
                parts = re.split(r'\s+', line.strip())
                if len(parts) >= 6:
                    try:
                        nloc = int(parts[0])
                        ccn = int(parts[1])
                        param_count = int(parts[3])
                        location = ' '.join(parts[5:])
                        functions.append({'cyclomatic_complexity': ccn, 'parameter_count': param_count, 'location': location})
                    except ValueError:
                        pass

        if not functions:
            return {
                'avg_ccn': 0,
                'max_ccn': 0,
                'pct_ccn_gt_10': 0,
                'functions_gt_7_params': 0,
                'duplication_pct': 0,
                'risky_functions': []
            }

        ccn_values = [f['cyclomatic_complexity'] for f in functions]
        avg_ccn = sum(ccn_values) / len(ccn_values)
        max_ccn = max(ccn_values)
        pct_ccn_gt_10 = sum(1 for c in ccn_values if c > 10) / len(ccn_values) * 100
        functions_gt_7_params = sum(1 for f in functions if f['parameter_count'] > 7)

        # For duplication, run separate command on all code files
        dup_cmd = ['lizard', '--duplicate'] + [str(f) for f in code_files]
        dup_result = subprocess.run(
            dup_cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        duplication_pct = 0
        if dup_result.returncode == 0:
            dup_output = dup_result.stdout
            dup_lines = len([line for line in dup_output.split('\n') if line.strip() and not line.startswith(' ') and len(line) > 10])
            total_functions = len(functions)
            if total_functions > 0:
                duplication_pct = min((dup_lines / total_functions) * 10, 100)

        risky_functions = sorted(functions, key=lambda f: (f['cyclomatic_complexity'], f['parameter_count']), reverse=True)[:3]

        return {
            'avg_ccn': avg_ccn,
            'max_ccn': max_ccn,
            'pct_ccn_gt_10': pct_ccn_gt_10,
            'functions_gt_7_params': functions_gt_7_params,
            'duplication_pct': duplication_pct,
            'risky_functions': risky_functions
        }
    except (subprocess.TimeoutExpired, Exception) as e:
        raise Exception(f"Failed to analyze with Lizard: {e}")