from typing import Dict, Any, List
from .utils import format_number


def generate_header(scores: Dict[str, Any]) -> str:
    """Generate the report header."""
    return (
        "# Code Quality Report\n\n"
        f"## Overall Score: {format_number(scores.get('overall_score', None))} ({scores.get('overall_grade', 'N/A')})\n\n"
    )


def generate_metrics_summary(scores: Dict[str, Any], null_reasons: Dict[str, str]) -> str:
    """Generate the metrics summary table."""
    report = "## Metrics Summary\n\n"
    report += "| Metric | Value | Grade |\n"
    report += "|--------|-------|-------|\n"
    report += f"| Maintainability | {format_number(scores.get('maint_score', None))} | {scores.get('maint_grade', 'N/A')} |\n"
    report += f"| Security | {format_number(scores.get('sec_score', None))} | {scores.get('sec_grade', 'N/A')} |\n"
    report += f"| Structure | {format_number(scores.get('struct_score', None))} | {scores.get('struct_grade', 'N/A')} |\n"
    report += f"| Testing Quality | {format_number(scores.get('testing_score', None))} | {scores.get('testing_grade', 'N/A')} | {'Reason: ' + null_reasons['Testing Quality'] if 'Testing Quality' in null_reasons else ''}\n"
    report += f"| Code Coverage | {format_number(scores.get('coverage_score', None))} | {scores.get('coverage_grade', 'N/A')} | {'Reason: ' + null_reasons['Code Coverage'] if 'Code Coverage' in null_reasons else ''}\n"
    report += f"| Documentation | {format_number(scores.get('docs_score', None))} | {scores.get('docs_grade', 'N/A')} | {'Reason: ' + null_reasons['Documentation'] if 'Documentation' in null_reasons else ''}\n"
    report += f"| CI/CD | {format_number(scores.get('ci_cd_score', None))} | {scores.get('ci_cd_grade', 'N/A')} | {'Reason: ' + null_reasons['CI/CD'] if 'CI/CD' in null_reasons else ''}\n"
    report += f"| Compliance | {format_number(scores.get('compliance_score', None))} | {scores.get('compliance_grade', 'N/A')} |\n"
    report += f"| API Quality | {format_number(scores.get('api_score', None))} | {scores.get('api_grade', 'N/A')} | {'Reason: ' + null_reasons['API Quality'] if 'API Quality' in null_reasons else ''}\n"
    report += f"| Monitoring | {format_number(scores.get('monitoring_score', None))} | {scores.get('monitoring_grade', 'N/A')} | {'Reason: ' + null_reasons['Monitoring'] if 'Monitoring' in null_reasons else ''}\n\n"

    return report


def generate_detailed_metrics(metrics: Dict[str, Any], scores: Dict[str, Any]) -> str:
    """Generate detailed metrics sections."""
    report = "## Detailed Metrics\n\n"

    # Complexity
    report += "### Complexity\n"
    report += "| Metric | Value | Grade |\n"
    report += "|--------|-------|-------|\n"
    avg_ccn = metrics.get('avg_ccn')
    max_ccn = metrics.get('max_ccn')
    pct_ccn_gt_10 = metrics.get('pct_ccn_gt_10')
    duplication_pct = metrics.get('duplication_pct')
    report += f"| Average Cyclomatic Complexity | {format_number(avg_ccn)} | {scores.get('ccn_grade', 'N/A')} |\n"
    report += f"| Max Cyclomatic Complexity | {format_number(max_ccn)} | - |\n"
    report += f"| % Functions CCN > 10 | {format_number(pct_ccn_gt_10) if pct_ccn_gt_10 is not None else 'N/A'}% | - |\n\n"

    # Duplication
    report += "### Duplication\n"
    report += "| Metric | Value | Grade |\n"
    report += "|--------|-------|-------|\n"
    report += f"| Code Duplication % | {format_number(duplication_pct) if duplication_pct is not None else 'N/A'}% | {scores.get('dup_grade', 'N/A')} |\n\n"

    # Security
    report += "### Security\n"
    report += "| Severity | Count |\n"
    report += "|----------|-------|\n"
    report += f"| Critical | {metrics.get('security_critical', 0)} |\n"
    report += f"| High | {metrics.get('security_high', 0)} |\n"
    report += f"| Medium | {metrics.get('security_medium', 0)} |\n"
    report += f"| Low | {metrics.get('security_low', 0)} |\n\n"

    # Structure
    report += "### Structure\n"
    report += "| Metric | Value |\n"
    report += "|--------|-------|\n"
    report += f"| Functions with >7 Parameters | {metrics.get('functions_gt_7_params', 0)} |\n\n"

    return report


def generate_recommendations(scores: Dict[str, Any]) -> str:
    """Generate recommendations based on scores."""
    report = "## Recommendations\n\n"

    recommendations = []
    if scores.get('maint_score') is not None and scores.get('maint_score') < 70:
        recommendations.append("- **Maintainability**: Refactor complex functions (CCN > 10) and reduce code duplication.")
    if scores.get('sec_score') is not None and scores.get('sec_score') < 70:
        recommendations.append("- **Security**: Address critical and high-severity vulnerabilities immediately.")
    if scores.get('struct_score') is not None and scores.get('struct_score') < 70:
        recommendations.append("- **Structure**: Simplify functions with too many parameters.")
    if scores.get('coverage_score') is not None and scores.get('coverage_score') < 80:
        recommendations.append("- **Coverage**: Improve test coverage to at least 80%.")
    if scores.get('testing_score') is not None and scores.get('testing_score') < 70:
        recommendations.append("- **Testing**: Enhance test suite quality and coverage.")
    if scores.get('docs_score') is not None and scores.get('docs_score') < 70:
        recommendations.append("- **Documentation**: Add comprehensive docstrings and improve README.")
    if scores.get('ci_cd_score') is not None and scores.get('ci_cd_score') < 70:
        recommendations.append("- **CI/CD**: Implement proper CI/CD pipelines with security scanning.")
    if scores.get('compliance_score') is not None and scores.get('compliance_score') < 70:
        recommendations.append("- **Compliance**: Fix linting issues and adhere to coding standards.")
    if scores.get('api_score') is not None and scores.get('api_score') < 70:
        recommendations.append("- **API Quality**: Improve API design and security practices.")
    if scores.get('monitoring_score') is not None and scores.get('monitoring_score') < 70:
        recommendations.append("- **Monitoring**: Implement proper logging and monitoring.")

    report += '\n'.join(recommendations) + '\n\n'
    return report


def generate_config_section(metrics: Dict[str, Any]) -> str:
    """Generate configuration files section."""
    config_files = metrics.get('config_files', {})
    report = "\n## Configuration & Workflow Files\n\n"
    report += "| File | Present |\n"
    report += "|------|---------|\n"
    for name, present in config_files.items():
        report += f"| {name} | {'✅' if present else '❌'} |\n"
    report += "\n"
    return report


def generate_complexity_section(metrics: Dict[str, Any], halstead_main_files: List[Dict[str, Any]]) -> str:
    """Generate complexity and risky functions section."""
    report = "\n## Complexity & Risky Functions\n\n"

    avg_ccn = metrics.get('avg_ccn', None)
    max_ccn = metrics.get('max_ccn', None)
    pct_ccn_gt_10 = metrics.get('pct_ccn_gt_10', None)
    halstead = metrics.get('halstead', {}) if isinstance(metrics.get('halstead', {}), dict) else {}

    if avg_ccn is not None:
        report += f"- **Average Cyclomatic Complexity**: {avg_ccn}\n"
    if max_ccn is not None:
        report += f"- **Max Cyclomatic Complexity**: {max_ccn}\n"
    if pct_ccn_gt_10 is not None:
        report += f"- **% Functions CCN > 10**: {pct_ccn_gt_10}%\n"
    if halstead:
        report += f"- **Halstead Volume**: {halstead.get('volume', 'N/A')}\n"
        report += f"- **Halstead Difficulty**: {halstead.get('difficulty', 'N/A')}\n"
        report += f"- **Halstead Effort**: {halstead.get('effort', 'N/A')}\n"

    # Per-main-file Halstead metrics
    if halstead_main_files:
        report += "\n### Halstead Metrics for Main Files\n\n"
        report += "| File | Vocabulary | Length | Volume | Difficulty | Effort |\n"
        report += "|------|------------|--------|--------|------------|--------|\n"
        for h in halstead_main_files:
            report += f"| {h.get('file', 'N/A')} | {h.get('vocabulary', 'N/A')} | {h.get('length', 'N/A')} | {h.get('volume', 'N/A')} | {h.get('difficulty', 'N/A')} | {h.get('effort', 'N/A')} |\n"

    risky = metrics.get('risky_functions', []) if isinstance(metrics.get('risky_functions', []), list) else []
    if risky:
        report += "\n| Function | CCN | Params |\n"
        report += "|----------|-----|--------|\n"
        for f in risky:
            report += f"| {f['location']} | {f['cyclomatic_complexity']} | {f['parameter_count']} |\n"
    else:
        report += "\nNo risky functions detected or complexity analysis failed.\n"

    return report