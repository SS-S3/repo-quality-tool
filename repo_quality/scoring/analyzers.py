from typing import Dict, Any, Optional
from .utils import find_metric, numeric


def compute_analyzer_scores(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Compute scores from various analyzers."""
    scores = {}

    # Coverage score
    coverage_pct = find_metric(metrics, ['line_coverage_pct', 'line_coverage', 'coverage_percentage', 'coverage_percent'])
    coverage_pct_n = numeric(coverage_pct)
    scores['coverage_score'] = coverage_pct_n if coverage_pct_n is not None else None
    if scores['coverage_score'] is not None:
        scores['coverage_score'] = min(100.0, scores['coverage_score'])
    # If coverage analyzer explicitly reports absence, show None
    if metrics.get('coverage_found') is False:
        scores['coverage_score'] = None

    # Testing quality score
    testing_score = find_metric(metrics, ['test_quality_score', 'test_quality', 'test_quality_score'])
    scores['testing_score'] = numeric(testing_score)
    # If no tests found, treat testing score as absent
    if metrics.get('total_test_files', 0) == 0:
        scores['testing_score'] = None

    # Documentation score
    docs_score = find_metric(metrics, ['overall_docs_score', 'doc_coverage_percent', 'doc_coverage_percent'])
    scores['docs_score'] = numeric(docs_score)
    # If documentation analyzer says no README and no docstrings, mark absent
    if metrics.get('readme_present') is False and metrics.get('doc_coverage_percent') is None and docs_score == 0:
        scores['docs_score'] = None

    # CI/CD score
    ci_cd_score = find_metric(metrics, ['ci_quality_score', 'ci_cd_score', 'ci_score'])
    scores['ci_cd_score'] = numeric(ci_cd_score)
    # If no CI/CD config files detected, mark as None
    ci_cd_configs = [
        'GitHub Actions Workflow', 'GitLab CI', 'CircleCI', 'jenkinsfile', 'azure-pipelines.yml',
        '.travis.yml', '.circleci/config.yml', '.github/workflows', '.gitlab-ci.yml', 'bitbucket-pipelines.yml'
    ]
    config_files = metrics.get('config_files', {})
    has_ci_cd = any(config_files.get(f, False) for f in ci_cd_configs)
    if not has_ci_cd:
        scores['ci_cd_score'] = None

    # Compliance score
    compliance_score = find_metric(metrics, ['compliance_score'])
    scores['compliance_score'] = numeric(compliance_score)

    # API quality score
    api_score = find_metric(metrics, ['api_quality_score', 'api_score'])
    scores['api_score'] = numeric(api_score)
    # If API analyzer indicates no API, mark absent
    if metrics.get('has_api') is False or (isinstance(metrics.get('api_quality'), str) and 'No API' in metrics.get('api_quality')):
        scores['api_score'] = None

    # Monitoring score
    monitoring_score = find_metric(metrics, ['logging_quality_score', 'monitoring_score', 'observability_score'])
    scores['monitoring_score'] = numeric(monitoring_score)
    # If monitoring/logging not detected, mark absent
    if metrics.get('has_logging') is False and not metrics.get('monitoring_integrations'):
        scores['monitoring_score'] = None

    return scores