from typing import Dict, Any


def compute_scores(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Compute weighted scores from metrics.

    Args:
        metrics: Dictionary of raw metrics.

    Returns:
        Dictionary of scores and grades.
    """
    # Extract metrics with defaults
    avg_ccn = metrics.get('avg_ccn', 0)
    max_ccn = metrics.get('max_ccn', 0)
    pct_ccn_gt_10 = metrics.get('pct_ccn_gt_10', 0)
    duplication_pct = metrics.get('duplication_pct', 0)
    functions_gt_7_params = metrics.get('functions_gt_7_params', 0)
    security_critical = metrics.get('security_critical', 0)
    security_high = metrics.get('security_high', 0)
    security_medium = metrics.get('security_medium', 0)
    
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

    # CCN score: lower is better, max 10 is good
    ccn_score = max(0, 100 - (avg_ccn * 5 + pct_ccn_gt_10))

    # Duplication score: lower duplication is better
    dup_score = max(0, 100 - duplication_pct)

    # Maintainability: 60% CCN + 40% duplication
    maint_score = 0.6 * ccn_score + 0.4 * dup_score

    # Security: Semgrep findings + custom dangerous findings + security configs
    semgrep_penalty = security_critical * 20 + security_high * 10 + security_medium * 2
    custom_penalty = min(dangerous_findings * 5, 30)  # Cap at 30 points
    sec_score = max(0, 100 - semgrep_penalty - custom_penalty + (security_config_score * 0.1))

    # Structure: Config completeness + parameter complexity
    struct_penalty = functions_gt_7_params * 10
    struct_score = max(0, (config_score * 0.7 + (100 - struct_penalty) * 0.3))

    # Overall: 50% maint + 30% sec + 20% struct
    overall_score = 0.5 * maint_score + 0.3 * sec_score + 0.2 * struct_score

    def get_grade(score: float) -> str:
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
        'overall_score': overall_score,
        'ccn_grade': get_grade(ccn_score),
        'dup_grade': get_grade(dup_score),
        'maint_grade': get_grade(maint_score),
        'sec_grade': get_grade(sec_score),
        'struct_grade': get_grade(struct_score),
        'overall_grade': get_grade(overall_score),
        'metrics': metrics
    }