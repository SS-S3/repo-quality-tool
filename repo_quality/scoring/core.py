from typing import Dict, Any, Optional
from .utils import find_metric, numeric


def compute_core_scores(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Compute core scores: CCN, duplication, maintainability, security, structure."""
    scores = {}

    # Extract metrics
    avg_ccn = find_metric(metrics, ['avg_ccn', 'average_ccn'])
    pct_ccn_gt_10 = find_metric(metrics, ['pct_ccn_gt_10', 'pct_ccn_over_10'])
    duplication_pct = find_metric(metrics, ['duplication_pct', 'duplication_percentage'])
    functions_gt_7_params = find_metric(metrics, ['functions_gt_7_params', 'functions_gt_7'])
    security_critical = find_metric(metrics, ['security_critical']) or 0
    security_high = find_metric(metrics, ['security_high']) or 0
    security_medium = find_metric(metrics, ['security_medium']) or 0

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

    # CCN and duplication scoring
    avg_ccn_n = numeric(avg_ccn)
    pct_ccn_gt_10_n = numeric(pct_ccn_gt_10)
    duplication_pct_n = numeric(duplication_pct)

    if avg_ccn_n is not None and pct_ccn_gt_10_n is not None and avg_ccn_n > 0:
        scores['ccn_score'] = max(0.0, 100.0 - (avg_ccn_n * 5.0 + pct_ccn_gt_10_n))
    if duplication_pct_n is not None:
        scores['dup_score'] = max(0.0, 100.0 - duplication_pct_n)

    # Maintainability score
    if scores.get('ccn_score') is not None and scores.get('dup_score') is not None:
        scores['maint_score'] = 0.6 * scores['ccn_score'] + 0.4 * scores['dup_score']

    # Security score
    semgrep_penalty = security_critical * 20 + security_high * 10 + security_medium * 2
    custom_penalty = min(dangerous_findings * 5, 30)  # Cap at 30 points
    scores['sec_score'] = max(0, 100 - semgrep_penalty - custom_penalty + (security_config_score * 0.1))

    # Structure score
    fg7 = numeric(functions_gt_7_params)
    if fg7 is not None:
        struct_penalty = fg7 * 10.0
        scores['struct_score'] = max(0.0, (config_score * 0.7 + max(0.0, 100.0 - struct_penalty) * 0.3))

    return scores