from typing import Dict, Any, Iterable, Optional


def find_metric(metrics: Dict[str, Any], keys: Iterable[str]) -> Optional[Any]:
    """Helper to look up metric keys in top-level or analyzer sections."""
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


def numeric(v: Optional[Any]) -> Optional[float]:
    """Convert value to float, return None if not possible."""
    try:
        return float(v)
    except Exception:
        return None


def get_grade(score: Optional[float]) -> str:
    """Convert score to grade."""
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