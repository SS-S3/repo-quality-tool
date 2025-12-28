from typing import Dict, Any, Iterable, Optional
from pathlib import Path
import ast
import re


def compute_scores(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Compute weighted scores from metrics.

    Args:
        metrics: Dictionary of raw metrics.

    Returns:
        Dictionary of scores and grades.
    """
    # Helper to look up metric keys in top-level or analyzer sections
    def _find(keys: Iterable[str]) -> Optional[Any]:
        for k in keys:
            if k in metrics:
                return metrics.get(k)
        # check common analyzer sections
        sections = ['coverage_analysis', 'testing_quality', 'documentation_quality', 'ci_cd_analysis', 'compliance_analysis', 'api_quality', 'monitoring_analysis']
        for s in sections:
            sec = metrics.get(s, {}) if isinstance(metrics.get(s, {}), dict) else {}
            for k in keys:
                if k in sec:
                    return sec.get(k)
        return None

    # Extract metrics (allow None if missing)
    avg_ccn = _find(['avg_ccn', 'average_ccn'])
    max_ccn = _find(['max_ccn', 'maximum_ccn'])
    pct_ccn_gt_10 = _find(['pct_ccn_gt_10', 'pct_ccn_over_10'])
    duplication_pct = _find(['duplication_pct', 'duplication_percentage'])
    functions_gt_7_params = _find(['functions_gt_7_params', 'functions_gt_7'])
    security_critical = _find(['security_critical']) or 0
    security_high = _find(['security_high']) or 0
    security_medium = _find(['security_medium']) or 0
    
    # Config files and custom findings
    config_files = metrics.get('config_files', {})
    custom_findings = metrics.get('custom_static_findings', [])
    
    # Count critical config files
    critical_configs = ['README.md', '.gitignore', 'LICENSE']
    security_configs = ['.env.example', 'Security Policy', 'GitHub Actions Workflow']
    testing_configs = ['jest.config.js', 'pytest Config', 'vitest.config']
    
    config_score = sum(1 for c in critical_configs if config_files.get(c, False)) / len(critical_configs) * 100
    security_config_score = sum(1 for c in security_configs if config_files.get(c, False)) / len(security_configs) * 100
    
    # Count dangerous findings from custom analysis
    dangerous_findings = sum(1 for f in custom_findings if f['type'] in ['Dangerous Function', 'SQL Injection Risk', 'Hardcoded Credential', 'Insecure Import'])

    # CCN and duplication scoring: require numeric inputs; otherwise mark as None
    def _numeric(v: Optional[Any]) -> Optional[float]:
        try:
            return float(v)
        except Exception:
            return None

    avg_ccn_n = _numeric(avg_ccn)
    pct_ccn_gt_10_n = _numeric(pct_ccn_gt_10)
    duplication_pct_n = _numeric(duplication_pct)

    ccn_score = None
    dup_score = None
    maint_score = None
    # Improved fallback: if Lizard fails, estimate complexity using AST for Python and regex for JS/TS
    if avg_ccn_n is not None and pct_ccn_gt_10_n is not None and avg_ccn_n > 0:
        ccn_score = max(0.0, 100.0 - (avg_ccn_n * 5.0 + pct_ccn_gt_10_n))
    if duplication_pct_n is not None:
        dup_score = max(0.0, 100.0 - duplication_pct_n)
    if ccn_score is not None and dup_score is not None:
        maint_score = 0.6 * ccn_score + 0.4 * dup_score
    else:
        # Attempt improved fallback estimations using repo_root if available
        repo_root = metrics.get('repo_root')
        if repo_root:
            try:
                repo_p = Path(repo_root)
                py_files = list(repo_p.rglob('*.py'))
                func_ccns = []
                total_lines = 0
                unique_lines = set()
                params_gt_7 = 0
                # Halstead metrics
                n1 = n2 = N1 = N2 = 0
                operators = set()
                operands = set()
                for p in py_files:
                    try:
                        src = p.read_text(encoding='utf-8', errors='ignore')
                        total_lines += len(src.splitlines())
                        for ln in src.splitlines():
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
                    except Exception:
                        continue

                if func_ccns:
                    avg_est = sum(func_ccns) / len(func_ccns)
                    pct_gt_10 = sum(1 for v in func_ccns if v > 10) / len(func_ccns) * 100
                    if avg_est > 0:
                        ccn_score = max(0.0, 100.0 - (avg_est * 5.0 + pct_gt_10))
                        metrics['avg_ccn'] = round(avg_est, 2)
                        metrics['max_ccn'] = max(func_ccns)
                        metrics['pct_ccn_gt_10'] = round(pct_gt_10, 2)
                if total_lines > 0:
                    dup_pct_est = max(0.0, (1 - len(unique_lines) / total_lines) * 100)
                    dup_score = max(0.0, 100.0 - dup_pct_est)
                if ccn_score is not None and dup_score is not None:
                    maint_score = 0.6 * ccn_score + 0.4 * dup_score
                if functions_gt_7_params is None:
                    functions_gt_7_params = params_gt_7
                if struct_score is None and functions_gt_7_params is not None:
                    fg7 = _numeric(functions_gt_7_params)
                    if fg7 is not None:
                        struct_penalty = fg7 * 10.0
                        struct_score = max(0.0, (config_score * 0.7 + max(0.0, 100.0 - struct_penalty) * 0.3))
                # Halstead metrics calculation
                n1 = len(operators)
                n2 = len(operands)
                N1 = n1
                N2 = n2
                vocabulary = n1 + n2
                length = N1 + N2
                volume = difficulty = effort = None
                if vocabulary > 0:
                    import math
                    volume = length * math.log2(vocabulary) if vocabulary > 0 else 0
                    difficulty = (n1 / 2) * (N2 / n2) if n2 > 0 else 0
                    effort = volume * difficulty if volume is not None and difficulty is not None else 0
                    metrics['halstead'] = {
                        'vocabulary': vocabulary,
                        'length': length,
                        'volume': round(volume, 2) if volume is not None else None,
                        'difficulty': round(difficulty, 2) if difficulty is not None else None,
                        'effort': round(effort, 2) if effort is not None else None
                    }
            except Exception:
                pass
        # If Python fallback didn't yield values, try a JS/TS lightweight fallback
        if (ccn_score is None or dup_score is None) and repo_root:
            try:
                js_files = list(Path(repo_root).rglob('*.js')) + list(Path(repo_root).rglob('*.ts'))
                js_func_count = 0
                js_decisions = 0
                js_params_gt_7 = 0
                js_total_lines = 0
                js_unique_lines = set()
                for p in js_files:
                    try:
                        txt = p.read_text(encoding='utf-8', errors='ignore')
                        js_total_lines += len(txt.splitlines())
                        for ln in txt.splitlines():
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
                    if ccn_score is None:
                        ccn_score = max(0.0, 100.0 - (avg_est_js * 5.0 + pct_gt_10_js))
                if js_total_lines > 0 and dup_score is None:
                    dup_pct_js = max(0.0, (1 - len(js_unique_lines) / js_total_lines) * 100)
                    dup_score = max(0.0, 100.0 - dup_pct_js)
                if ccn_score is not None and dup_score is not None and maint_score is None:
                    maint_score = 0.6 * ccn_score + 0.4 * dup_score
                if functions_gt_7_params is None:
                    functions_gt_7_params = js_params_gt_7
                if struct_score is None and functions_gt_7_params is not None:
                    fg7 = _numeric(functions_gt_7_params)
                    if fg7 is not None:
                        struct_penalty = fg7 * 10.0
                        struct_score = max(0.0, (config_score * 0.7 + max(0.0, 100.0 - struct_penalty) * 0.3))
            except Exception:
                pass

    # Security: Semgrep findings + custom dangerous findings + security configs
    semgrep_penalty = security_critical * 20 + security_high * 10 + security_medium * 2
    custom_penalty = min(dangerous_findings * 5, 30)  # Cap at 30 points
    sec_score = max(0, 100 - semgrep_penalty - custom_penalty + (security_config_score * 0.1))

    # Structure: Config completeness + parameter complexity. Require functions_gt_7_params numeric.
    fg7 = _numeric(functions_gt_7_params)
    struct_score = None
    if fg7 is not None:
        struct_penalty = fg7 * 10.0
        struct_score = max(0.0, (config_score * 0.7 + max(0.0, 100.0 - struct_penalty) * 0.3))

    # New analyzer scores
    # Coverage score (0-100)
    coverage_pct = _find(['line_coverage_pct', 'line_coverage', 'coverage_percentage', 'coverage_percent'])
    coverage_pct_n = _numeric(coverage_pct)
    coverage_score = coverage_pct_n if coverage_pct_n is not None else None
    if coverage_score is not None:
        coverage_score = min(100.0, coverage_score)
    # If coverage analyzer explicitly reports absence, show None
    if metrics.get('coverage_found') is False:
        coverage_score = None

    # Testing quality score (0-100)
    testing_score = _find(['test_quality_score', 'test_quality', 'test_quality_score'])
    testing_score = _numeric(testing_score)
    # If no tests found, treat testing score as absent
    if metrics.get('total_test_files', 0) == 0:
        testing_score = None

    # Documentation score (0-100)
    docs_score = _find(['overall_docs_score', 'doc_coverage_percent', 'doc_coverage_percent'])
    docs_score = _numeric(docs_score)
    # If documentation analyzer says no README and no docstrings, mark absent
    if metrics.get('readme_present') is False and metrics.get('doc_coverage_percent') is None and docs_score == 0:
        docs_score = None

    # CI/CD score (0-100)
    ci_cd_score = _find(['ci_quality_score', 'ci_cd_score', 'ci_score'])
    ci_cd_score = _numeric(ci_cd_score)
    # If no CI/CD config files detected, mark as None
    ci_cd_configs = [
        'GitHub Actions Workflow', 'GitLab CI', 'CircleCI', 'jenkinsfile', 'azure-pipelines.yml',
        '.travis.yml', '.circleci/config.yml', '.github/workflows', '.gitlab-ci.yml', 'bitbucket-pipelines.yml'
    ]
    config_files = metrics.get('config_files', {})
    has_ci_cd = any(config_files.get(f, False) for f in ci_cd_configs)
    if not has_ci_cd:
        ci_cd_score = None

    # Compliance score (0-100)
    compliance_score = _find(['compliance_score'])
    compliance_score = _numeric(compliance_score)

    # API quality score (0-100)
    api_score = _find(['api_quality_score', 'api_score'])
    api_score = _numeric(api_score)
    # If API analyzer indicates no API, mark absent
    if metrics.get('has_api') is False or (isinstance(metrics.get('api_quality'), str) and 'No API' in metrics.get('api_quality')):
        api_score = None

    # Monitoring score (0-100)
    monitoring_score = _find(['logging_quality_score', 'monitoring_score', 'observability_score'])
    monitoring_score = _numeric(monitoring_score)
    # If monitoring/logging not detected, mark absent
    if metrics.get('has_logging') is False and not metrics.get('monitoring_integrations'):
        monitoring_score = None

    # Overall score with all components
    # Weights: 25% Core (maint/sec/struct) + 15% Testing + 10% Coverage + 10% Docs + 10% CI/CD + 10% Compliance + 10% API + 10% Monitoring
    # Compute overall score only when core components are present
    core_score = None
    overall_score = None
    if maint_score is not None and struct_score is not None:
        core_score = 0.5 * maint_score + 0.3 * sec_score + 0.2 * struct_score

    # Compose weighted overall only if at least core_score is present
    if core_score is not None:
        # For optional components, treat missing as 0 contribution but do not fail
        def _or_zero(v: Optional[float]) -> float:
            return float(v) if v is not None else 0.0

        overall_score = (0.25 * core_score +
                        0.15 * _or_zero(testing_score) +
                        0.10 * _or_zero(coverage_score) +
                        0.10 * _or_zero(docs_score) +
                        0.10 * _or_zero(ci_cd_score) +
                        0.10 * _or_zero(compliance_score) +
                        0.10 * _or_zero(api_score) +
                        0.10 * _or_zero(monitoring_score))

    def get_grade(score: Optional[float]) -> str:
        if score is None:
            return 'N/A'
        if score >= 90:
            return 'Excellent'
        elif score >= 80:
            return 'Good'
        elif score >= 70:
            return 'Fair'
        else:
            return 'Poor'

    return {
        'ccn_score': ccn_score,
        'dup_score': dup_score,
        'maint_score': maint_score,
        'sec_score': sec_score,
        'struct_score': struct_score,
        'coverage_score': coverage_score,
        'testing_score': testing_score,
        'docs_score': docs_score,
        'ci_cd_score': ci_cd_score,
        'compliance_score': compliance_score,
        'api_score': api_score,
        'monitoring_score': monitoring_score,
        'overall_score': overall_score if overall_score is not None else 0.0,
        'ccn_grade': get_grade(ccn_score),
        'dup_grade': get_grade(dup_score),
        'maint_grade': get_grade(maint_score),
        'sec_grade': get_grade(sec_score),
        'struct_grade': get_grade(struct_score),
        'coverage_grade': get_grade(coverage_score),
        'testing_grade': get_grade(testing_score),
        'docs_grade': get_grade(docs_score),
        'ci_cd_grade': get_grade(ci_cd_score),
        'compliance_grade': get_grade(compliance_score),
        'api_grade': get_grade(api_score),
        'monitoring_grade': get_grade(monitoring_score),
        'overall_grade': get_grade(overall_score),
        'metrics': metrics
    }