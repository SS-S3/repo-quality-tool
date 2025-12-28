from typing import Dict, Any, Optional
from pathlib import Path
import ast
import re
import math


def compute_fallbacks(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Compute fallback metrics when analyzers fail."""
    repo_root = metrics.get('repo_root')
    if not repo_root:
        return {}

    fallbacks = {}
    try:
        repo_p = Path(repo_root)

        # Python fallbacks
        py_files = list(repo_p.rglob('*.py'))
        if py_files:
            py_fallbacks = _compute_python_fallbacks(py_files)
            fallbacks.update(py_fallbacks)

        # JS/TS fallbacks if Python didn't provide values
        if not fallbacks.get('ccn_score') or not fallbacks.get('dup_score'):
            js_files = list(repo_p.rglob('*.js')) + list(repo_p.rglob('*.ts'))
            if js_files:
                js_fallbacks = _compute_js_fallbacks(js_files)
                fallbacks.update(js_fallbacks)

    except Exception:
        pass

    return fallbacks


def _compute_python_fallbacks(py_files: list) -> Dict[str, Any]:
    """Compute fallback metrics for Python files."""
    fallbacks = {}
    func_ccns = []
    total_lines = 0
    unique_lines = set()
    params_gt_7 = 0
    operators = set()
    operands = set()
    N1 = N2 = 0

    for p in py_files:
        try:
            src = p.read_text(encoding='utf-8', errors='ignore')
            lines = src.splitlines()
            total_lines += len(lines)
            for ln in lines:
                unique_lines.add(ln.strip())

            tree = ast.parse(src)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # cyclomatic approx: 1 + number of decision nodes
                    decisions = sum(1 for n in ast.walk(node) if isinstance(n, (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.BoolOp, ast.ExceptHandler, ast.Assert, ast.comprehension)))
                    func_ccns.append(1 + decisions)
                    if getattr(node.args, 'args', None) and len(node.args.args) > 7:
                        params_gt_7 += 1

                # Halstead: count operators/operands
                if isinstance(node, ast.BinOp):
                    operators.add(type(node.op).__name__)
                    N1 += 1
                if isinstance(node, ast.UnaryOp):
                    operators.add(type(node.op).__name__)
                    N1 += 1
                if isinstance(node, ast.BoolOp):
                    operators.add(type(node.op).__name__)
                    N1 += 1
                if isinstance(node, ast.Compare):
                    operators.add(type(node.ops[0]).__name__)
                    N1 += 1
                if isinstance(node, ast.Call):
                    operands.add(getattr(node.func, 'id', 'call'))
                    N2 += 1
                if isinstance(node, ast.Name):
                    operands.add(node.id)
                    N2 += 1
        except Exception:
            continue

    # CCN metrics
    if func_ccns:
        avg_est = sum(func_ccns) / len(func_ccns)
        pct_gt_10 = sum(1 for v in func_ccns if v > 10) / len(func_ccns) * 100
        if avg_est > 0:
            fallbacks['ccn_score'] = max(0.0, 100.0 - (avg_est * 5.0 + pct_gt_10))
            fallbacks['avg_ccn'] = round(avg_est, 2)
            fallbacks['max_ccn'] = max(func_ccns)
            fallbacks['pct_ccn_gt_10'] = round(pct_gt_10, 2)

    # Duplication
    if total_lines > 0:
        dup_pct_est = max(0.0, (1 - len(unique_lines) / total_lines) * 100)
        fallbacks['dup_score'] = max(0.0, 100.0 - dup_pct_est)

    # Structure
    if params_gt_7 > 0:
        fallbacks['functions_gt_7_params'] = params_gt_7

    # Halstead
    n1 = len(operators)
    n2 = len(operands)
    vocabulary = n1 + n2
    length = N1 + N2
    if vocabulary > 0:
        volume = length * math.log2(vocabulary)
        difficulty = (n1 / 2) * (N2 / n2) if n2 > 0 else 0
        effort = volume * difficulty
        fallbacks['halstead'] = {
            'vocabulary': vocabulary,
            'length': length,
            'volume': round(volume, 2),
            'difficulty': round(difficulty, 2),
            'effort': round(effort, 2)
        }

    return fallbacks


def _compute_js_fallbacks(js_files: list) -> Dict[str, Any]:
    """Compute fallback metrics for JS/TS files."""
    fallbacks = {}
    js_func_count = 0
    js_decisions = 0
    js_params_gt_7 = 0
    js_total_lines = 0
    js_unique_lines = set()

    for p in js_files:
        try:
            txt = p.read_text(encoding='utf-8', errors='ignore')
            lines = txt.splitlines()
            js_total_lines += len(lines)
            for ln in lines:
                js_unique_lines.add(ln.strip())

            # count functions
            funcs = re.findall(r'function\s+\w+\s*\([^)]*\)|\([^)]*\)\s*=>', txt)
            js_func_count += max(1, len(funcs))

            # count decision keywords
            js_decisions += sum(txt.count(k) for k in [' if ', ' for ', ' while ', ' case ', ' switch '])

            # params >7 heuristic
            for m in re.finditer(r'function\s+\w+\s*\(([^)]*)\)', txt):
                params = m.group(1).strip()
                if params:
                    if len([p for p in params.split(',') if p.strip()]) > 7:
                        js_params_gt_7 += 1
        except Exception:
            continue

    if js_func_count > 0:
        avg_est_js = 1 + (js_decisions / js_func_count)
        pct_gt_10_js = 100.0 * (1 if avg_est_js > 10 else 0)
        fallbacks['ccn_score'] = max(0.0, 100.0 - (avg_est_js * 5.0 + pct_gt_10_js))

    if js_total_lines > 0:
        dup_pct_js = max(0.0, (1 - len(js_unique_lines) / js_total_lines) * 100)
        fallbacks['dup_score'] = max(0.0, 100.0 - dup_pct_js)

    if js_params_gt_7 > 0:
        fallbacks['functions_gt_7_params'] = js_params_gt_7

    return fallbacks