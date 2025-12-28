from typing import Dict, Any


def get_null_reasons(scores: Dict[str, Any]) -> Dict[str, str]:
    """Get explanations for null metric values."""
    null_reasons = {}

    if scores.get('coverage_score') is None:
        null_reasons['Code Coverage'] = 'No coverage reports found in the repository.'
    if scores.get('testing_score') is None:
        null_reasons['Testing Quality'] = 'No test files detected in the codebase.'
    if scores.get('docs_score') is None:
        null_reasons['Documentation'] = 'No README or docstrings found.'
    if scores.get('ci_cd_score') is None:
        null_reasons['CI/CD'] = 'No CI/CD configuration files detected in the repository.'
    if scores.get('api_score') is None:
        null_reasons['API Quality'] = 'No API endpoints or specifications detected.'
    if scores.get('monitoring_score') is None:
        null_reasons['Monitoring'] = 'No logging or monitoring integrations detected.'

    return null_reasons


def generate_summary(scores: Dict[str, Any], null_reasons: Dict[str, str]) -> str:
    """Generate a final summary based on key metrics."""
    parts = []
    # Coerce None to 0 for summary thresholds
    overall_score = scores.get('overall_score') or 0
    if overall_score >= 80:
        parts.append('This codebase is production-ready with strong maintainability, security, and structure.')
    elif overall_score >= 60:
        parts.append('This codebase is generally solid but has some areas for improvement, especially in testing, documentation, or CI/CD.')
    elif overall_score >= 40:
        parts.append('This codebase has significant quality issues. Focus on improving maintainability, test coverage, and documentation.')
    else:
        parts.append('This codebase is in poor health. Major improvements are needed in maintainability, security, testing, and documentation.')

    # Add null metric notes
    for k, v in null_reasons.items():
        parts.append(f"{k}: {v}")

    return '\n'.join(parts)