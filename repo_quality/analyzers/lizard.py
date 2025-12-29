import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List
import re
import logging

logger = logging.getLogger(__name__)


def analyze_lizard(repo_path: Path) -> Dict[str, Any]:
    """Analyze code using Lizard and return metrics.

    Args:
        repo_path: Path to the repository.

    Returns:
        Dictionary with lizard metrics. Returns null for unavailable metrics.
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
        
        # Return null metrics if no code files found
        if not code_files:
            return {
                'avg_ccn': None,
                'max_ccn': None,
                'pct_ccn_gt_10': None,
                'functions_gt_7_params': None,
                'duplication_pct': None,
                'risky_functions': None
            }
        
        # Limit to prevent timeout on massive repos
        if len(code_files) > 200:
            code_files = code_files[:200]
            logger.warning(f"Limited analysis to first 200 files (found {len(code_files)} total)")
        
        # Run lizard with language specification
        lizard_cmd = ['lizard', '-l', 'python,javascript'] + [str(f) for f in code_files]
        result = subprocess.run(
            lizard_cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        # Lizard returns 0 for success, 1 for analysis complete with findings (both valid)
        if result.returncode not in (0, 1):
            logger.error(f"Lizard failed with return code {result.returncode}: {result.stderr}")
            return {
                'avg_ccn': None,
                'max_ccn': None,
                'pct_ccn_gt_10': None,
                'functions_gt_7_params': None,
                'duplication_pct': None,
                'risky_functions': None
            }

        output = result.stdout
        if not output.strip():
            output = result.stderr
        
        # Parse lizard output
        functions = _parse_lizard_output(output)
        
        # If no functions parsed, return null metrics
        if not functions:
            logger.warning("No functions parsed from Lizard output")
            return {
                'avg_ccn': None,
                'max_ccn': None,
                'pct_ccn_gt_10': None,
                'functions_gt_7_params': None,
                'duplication_pct': None,
                'risky_functions': None
            }

        # Calculate metrics from parsed functions
        ccn_values = [f['cyclomatic_complexity'] for f in functions]
        avg_ccn = round(sum(ccn_values) / len(ccn_values), 2) if ccn_values else None
        max_ccn = max(ccn_values) if ccn_values else None
        pct_ccn_gt_10 = round(sum(1 for c in ccn_values if c > 10) / len(ccn_values) * 100, 1) if ccn_values else None
        functions_gt_7_params = sum(1 for f in functions if f['parameter_count'] > 7)

        # Calculate duplication percentage
        duplication_pct = _analyze_duplication(code_files, len(functions))

        # Extract risky functions (top 3 by CCN and parameter count)
        risky_functions = sorted(
            functions, 
            key=lambda f: (f['cyclomatic_complexity'], f['parameter_count']), 
            reverse=True
        )[:3]

        return {
            'avg_ccn': avg_ccn,
            'max_ccn': max_ccn,
            'pct_ccn_gt_10': pct_ccn_gt_10,
            'functions_gt_7_params': functions_gt_7_params,
            'duplication_pct': duplication_pct,
            'risky_functions': risky_functions if risky_functions else None
        }
    
    except subprocess.TimeoutExpired:
        logger.error("Lizard analysis timed out")
        return {
            'avg_ccn': None,
            'max_ccn': None,
            'pct_ccn_gt_10': None,
            'functions_gt_7_params': None,
            'duplication_pct': None,
            'risky_functions': None
        }
    except Exception as e:
        logger.error(f"Lizard analysis failed: {e}")
        raise Exception(f"Failed to analyze with Lizard: {e}")


def _parse_lizard_output(output: str) -> List[Dict[str, Any]]:
    """Parse Lizard output and extract function metrics.
    
    Args:
        output: Raw output from lizard command.
        
    Returns:
        List of function dictionaries with metrics.
    """
    functions = []
    lines = output.split('\n')
    parsing = False
    header_found = False
    
    for line in lines:
        # Look for header line with NLOC and CCN
        if 'NLOC' in line and 'CCN' in line and 'token' in line.lower():
            parsing = True
            header_found = True
            continue
        
        # Skip non-parsing mode
        if not parsing:
            continue
        
        # Skip separator lines and summary lines
        if not line.strip():
            continue
        if line.startswith('-') or line.startswith('='):
            continue
        if 'Total' in line or 'analyzed' in line or 'file' in line.lower():
            continue
        
        # Parse function metrics
        parts = re.split(r'\s+', line.strip())
        if len(parts) >= 6:
            try:
                nloc = int(parts[0])
                ccn = int(parts[1])
                token_count = int(parts[2])
                param_count = int(parts[3])
                location = ' '.join(parts[5:])
                
                # Validate metrics are reasonable
                if ccn > 0 and param_count >= 0 and nloc > 0:
                    functions.append({
                        'cyclomatic_complexity': ccn,
                        'parameter_count': param_count,
                        'location': location,
                        'nloc': nloc,
                        'token_count': token_count
                    })
            except (ValueError, IndexError) as e:
                # Skip malformed lines
                continue
    
    return functions


def _analyze_duplication(code_files: List[Path], total_functions: int) -> Optional[float]:
    """Analyze code duplication using Lizard.
    
    Args:
        code_files: List of code files to analyze.
        total_functions: Total number of functions for percentage calculation.
        
    Returns:
        Duplication percentage or None if unavailable.
    """
    if total_functions == 0:
        return None
    
    try:
        # Limit files for duplication analysis
        files_to_check = code_files[:50] if len(code_files) > 50 else code_files
        
        dup_cmd = ['lizard', '--duplicate'] + [str(f) for f in files_to_check]
        dup_result = subprocess.run(
            dup_cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if dup_result.returncode not in (0, 1):
            logger.warning("Duplication analysis failed")
            return None
        
        dup_output = dup_result.stdout if dup_result.stdout else dup_result.stderr
        
        # Count duplicate blocks
        dup_lines = len([
            line for line in dup_output.split('\n') 
            if line.strip() and not line.startswith(' ') and len(line) > 10
        ])
        
        duplication_pct = min((dup_lines / total_functions) * 10, 100) if total_functions > 0 else None
        return round(duplication_pct, 1) if duplication_pct is not None else None
        
    except Exception as e:
        logger.warning(f"Could not analyze duplication: {e}")
        return None