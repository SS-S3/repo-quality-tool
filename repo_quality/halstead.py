import ast
from pathlib import Path
from typing import Dict, Any
import math


def compute_halstead_for_file(file_path: Path) -> Dict[str, Any]:
    """Compute Halstead metrics for a single Python, JS, or TS file."""
    try:
        if file_path.suffix in ['.js', '.ts']:
            import subprocess, json
            node_path = 'node'  # Assumes node is in PATH
            script_path = str(Path(__file__).parent / 'halstead_js.js')
            result = subprocess.run([node_path, script_path, str(file_path)], capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {'file': str(file_path), 'vocabulary': None, 'length': None, 'volume': None, 'difficulty': None, 'effort': None, 'error': result.stderr}
        else:
            src = file_path.read_text(encoding='utf-8', errors='ignore')
            tree = ast.parse(src)
            operators = set()
            operands = set()
            n1 = n2 = N1 = N2 = 0
            for node in ast.walk(tree):
                if isinstance(node, ast.BinOp):
                    operators.add(type(node.op).__name__)
                    n1 += 1
                if isinstance(node, ast.UnaryOp):
                    operators.add(type(node.op).__name__)
                    n1 += 1
                if isinstance(node, ast.BoolOp):
                    operators.add(type(node.op).__name__)
                    n1 += 1
                if isinstance(node, ast.Compare):
                    operators.add(type(node.ops[0]).__name__)
                    n1 += 1
                if isinstance(node, ast.Call):
                    operands.add(getattr(node.func, 'id', 'call'))
                    N2 += 1
                if isinstance(node, ast.Name):
                    operands.add(node.id)
                    N2 += 1
            n1 = len(operators)
            n2 = len(operands)
            N1 = n1
            N2 = n2
            vocabulary = n1 + n2
            length = N1 + N2
            volume = difficulty = effort = None
            if vocabulary > 0:
                volume = length * math.log2(vocabulary) if vocabulary > 0 else 0
                difficulty = (n1 / 2) * (N2 / n2) if n2 > 0 else 0
                effort = volume * difficulty if volume is not None and difficulty is not None else 0
            return {
                'file': str(file_path),
                'vocabulary': vocabulary,
                'length': length,
                'volume': round(volume, 2) if volume is not None else None,
                'difficulty': round(difficulty, 2) if difficulty is not None else None,
                'effort': round(effort, 2) if effort is not None else None
            }
    except Exception as e:
        return {'file': str(file_path), 'vocabulary': None, 'length': None, 'volume': None, 'difficulty': None, 'effort': None, 'error': str(e)}

def compute_main_files_halstead(repo_root: str) -> list:
    """Compute Halstead metrics for main files in a repo (entry points and top-level modules)."""
    repo_p = Path(repo_root)
    # Heuristic: main files = __main__.py, cli.py, app.py, main.py, server.js, index.js, main.js, app.js, or top-level .py/.js/.ts files in src/ or root
    candidates = set()
    main_names = ['__main__.py', 'cli.py', 'main.py', 'app.py', 'server.js', 'index.js', 'main.js', 'app.js']
    for name in main_names:
        for p in repo_p.rglob(name):
            candidates.add(p)
    for ext in ['*.py', '*.js', '*.ts']:
        for p in repo_p.glob(ext):
            candidates.add(p)
        if (repo_p / 'src').exists():
            for p in (repo_p / 'src').glob(ext):
                candidates.add(p)
    # Remove test files
    main_files = [p for p in candidates if not p.name.startswith('test') and p.is_file()]
    return [compute_halstead_for_file(p) for p in main_files]
