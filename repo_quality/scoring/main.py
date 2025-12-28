from typing import Dict, Any, Optional
from .core import compute_core_scores
from .analyzers import compute_analyzer_scores
from .fallbacks import compute_fallbacks
from .utils import get_grade


def compute_scores(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Compute weighted scores from metrics.

    Args:
        metrics: Dictionary of raw metrics.

    Returns:
        Dictionary of scores and grades.
    """
    # Compute core scores
    core_scores = compute_core_scores(metrics)

    # Compute analyzer scores
    analyzer_scores = compute_analyzer_scores(metrics)

    # Apply fallbacks if needed
    maint_score = core_scores.get('maint_score')
    if maint_score is None:
        fallbacks = compute_fallbacks(metrics)
        core_scores.update(fallbacks)
        # Recalculate maint_score if fallbacks provided ccn and dup
        if fallbacks.get('ccn_score') is not None and fallbacks.get('dup_score') is not None:
            core_scores['maint_score'] = 0.6 * fallbacks['ccn_score'] + 0.4 * fallbacks['dup_score']

    # Combine all scores
    scores = {**core_scores, **analyzer_scores}

    # Compute overall score
    overall_score = _compute_overall_score(scores)

    # Add grades
    grades = _compute_grades(scores, overall_score)

    return {
        **scores,
        'overall_score': overall_score,
        **grades,
        'metrics': metrics
    }


def _compute_overall_score(scores: Dict[str, Any]) -> Optional[float]:
    """Compute the overall weighted score."""
    maint_score = scores.get('maint_score')
    sec_score = scores.get('sec_score')
    struct_score = scores.get('struct_score')
    # Build core with presence-aware weighting (normalize when some are missing)
    core_components = [
        (0.5, maint_score),
        (0.3, sec_score),
        (0.2, struct_score),
    ]
    present_core = [(w, v) for (w, v) in core_components if v is not None]
    core_score = None
    if present_core:
        total_core_weight = sum(w for w, _ in present_core)
        # weighted average of present core components
        core_score = sum(w * v for w, v in present_core) / total_core_weight

    # Compose overall score using the previous weights but only for present components
    components = [
        (0.25, core_score),
        (0.15, scores.get('testing_score')),
        (0.10, scores.get('coverage_score')),
        (0.10, scores.get('docs_score')),
        (0.10, scores.get('ci_cd_score')),
        (0.10, scores.get('compliance_score')),
        (0.10, scores.get('api_score')),
        (0.10, scores.get('monitoring_score')),
    ]

    present = [(w, v) for (w, v) in components if v is not None]
    if not present:
        return None

    total_weight = sum(w for w, _ in present)
    overall = sum(w * v for w, v in present) / total_weight
    return overall


def _compute_grades(scores: Dict[str, Any], overall_score: Optional[float]) -> Dict[str, str]:
    """Compute grades for all scores."""
    score_keys = [
        'ccn_score', 'dup_score', 'maint_score', 'sec_score', 'struct_score',
        'coverage_score', 'testing_score', 'docs_score', 'ci_cd_score',
        'compliance_score', 'api_score', 'monitoring_score'
    ]

    grades = {}
    for key in score_keys:
        grades[f"{key.replace('_score', '')}_grade"] = get_grade(scores.get(key))

    grades['overall_grade'] = get_grade(overall_score)
    return grades