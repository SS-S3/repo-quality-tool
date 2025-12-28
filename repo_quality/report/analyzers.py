from typing import Dict, Any
from .utils import coerce_section


def generate_coverage_section(metrics: Dict[str, Any]) -> str:
    """Generate code coverage analysis section."""
    coverage_data = coerce_section(metrics, 'coverage_analysis')
    if not coverage_data:
        return ""

    report = "\n## Code Coverage Analysis\n\n"
    report += f"- **Coverage Percentage**: {coverage_data.get('line_coverage_pct', 0):.1f}%\n"
    report += f"- **Lines Covered**: {coverage_data.get('total_lines', 0) - coverage_data.get('uncovered_lines', 0)}\n"
    report += f"- **Total Lines**: {coverage_data.get('total_lines', 0)}\n"
    report += f"- **Coverage Grade**: {coverage_data.get('coverage_quality', 'N/A')}\n\n"

    recommendations = coverage_data.get('recommendations', [])
    if recommendations:
        report += "**Recommendations**:\n"
        for rec in recommendations:
            report += f"- {rec}\n"
        report += "\n"

    return report


def generate_testing_section(metrics: Dict[str, Any]) -> str:
    """Generate testing quality assessment section."""
    testing_data = coerce_section(metrics, 'testing_quality')
    if not testing_data:
        return ""

    report = "\n## Testing Quality Assessment\n\n"
    report += f"- **Test-to-Code Ratio**: {testing_data.get('test_to_code_ratio', 0):.2f}\n"
    report += f"- **Test Coverage**: {testing_data.get('assertion_density', 0):.1f}%\n"
    report += f"- **Test Quality Score**: {testing_data.get('test_quality_score', 0):.1f}/100\n"
    report += f"- **Testing Grade**: {testing_data.get('test_quality', 'N/A')}\n\n"

    anti_patterns = testing_data.get('anti_patterns', [])
    if anti_patterns:
        report += "**Anti-Patterns Detected**:\n"
        for pattern in anti_patterns[:10]:
            report += f"- {pattern}\n"
        if len(anti_patterns) > 10:
            report += f"\n*... and {len(anti_patterns) - 10} more*\n"
        report += "\n"

    recommendations = testing_data.get('recommendations', [])
    if recommendations:
        report += "**Recommendations**:\n"
        for rec in recommendations:
            report += f"- {rec}\n"
        report += "\n"

    return report


def generate_documentation_section(metrics: Dict[str, Any]) -> str:
    """Generate documentation quality assessment section."""
    docs_data = coerce_section(metrics, 'documentation_quality')
    if not docs_data:
        return ""

    report = "\n## Documentation Quality Assessment\n\n"
    report += f"- **Documentation Coverage**: {docs_data.get('docstring_quality_score', 0):.1f}%\n"
    report += f"- **README Quality Score**: {docs_data.get('readme_quality', 'N/A')}\n"
    report += f"- **Documentation Score**: {docs_data.get('overall_docs_score', 0):.1f}/100\n"
    report += f"- **Documentation Grade**: {docs_data.get('documentation_quality', 'N/A')}\n\n"

    missing_docs = docs_data.get('undocumented_functions', [])
    if missing_docs:
        report += "**Undocumented Functions**:\n"
        for func in missing_docs[:10]:
            report += f"- {func}\n"
        if len(missing_docs) > 10:
            report += f"\n*... and {len(missing_docs) - 10} more*\n"
        report += "\n"

    gaps = docs_data.get('documentation_gaps', [])
    if gaps:
        report += "**Documentation Gaps**:\n"
        for gap in gaps:
            report += f"- {gap}\n"
        report += "\n"

    return report


def generate_ci_cd_section(metrics: Dict[str, Any]) -> str:
    """Generate CI/CD pipeline analysis section."""
    ci_cd_data = coerce_section(metrics, 'ci_cd_analysis')
    if not ci_cd_data:
        return ""

    report = "\n## CI/CD Pipeline Analysis\n\n"
    report += f"- **CI/CD Score**: {ci_cd_data.get('ci_quality_score', 0):.1f}/100\n"
    report += f"- **Pipeline Completeness**: {ci_cd_data.get('parallel_jobs', 0)}\n"
    report += f"- **Security Practices**: {len(ci_cd_data.get('security_concerns', [])) == 0}\n"
    report += f"- **CI/CD Grade**: {ci_cd_data.get('ci_quality', 'N/A')}\n\n"

    missing_practices = ci_cd_data.get('missing_practices', [])
    if missing_practices:
        report += "**Missing Best Practices**:\n"
        for practice in missing_practices:
            report += f"- {practice}\n"
        report += "\n"

    recommendations = ci_cd_data.get('recommendations', [])
    if recommendations:
        report += "**Recommendations**:\n"
        for rec in recommendations:
            report += f"- {rec}\n"
        report += "\n"

    return report


def generate_compliance_section(metrics: Dict[str, Any]) -> str:
    """Generate compliance and standards analysis section."""
    compliance_data = coerce_section(metrics, 'compliance_analysis')
    if not compliance_data:
        return ""

    report = "\n## Compliance & Standards Analysis\n\n"
    report += f"- **Compliance Score**: {compliance_data.get('compliance_score', 0):.1f}/100\n"
    report += f"- **Linting Issues**: {len(compliance_data.get('code_quality_issues', []))}\n"
    report += f"- **Standards Violations**: {len(compliance_data.get('violations', []))}\n"
    report += f"- **Compliance Grade**: {compliance_data.get('compliance_level', 'N/A')}\n\n"

    violations = compliance_data.get('violations', [])
    if violations:
        report += "**Standards Violations**:\n"
        for violation in violations[:10]:
            report += f"- {violation}\n"
        if len(violations) > 10:
            report += f"\n*... and {len(violations) - 10} more*\n"
        report += "\n"

    recommendations = compliance_data.get('recommendations', [])
    if recommendations:
        report += "**Recommendations**:\n"
        for rec in recommendations:
            report += f"- {rec}\n"
        report += "\n"

    return report


def generate_api_section(metrics: Dict[str, Any]) -> str:
    """Generate API quality assessment section."""
    api_data = coerce_section(metrics, 'api_quality')
    if not api_data:
        return ""

    report = "\n## API Quality Assessment\n\n"
    report += f"- **API Design Score**: {api_data.get('api_score', 0):.1f}/100\n"
    report += f"- **Security Score**: {api_data.get('security_score', 0):.1f}/100\n"
    report += f"- **Documentation Score**: {api_data.get('documentation_score', 0):.1f}/100\n"
    report += f"- **API Quality Grade**: {api_data.get('grade', 'N/A')}\n\n"

    issues = api_data.get('issues', [])
    if issues:
        report += "**API Issues Found**:\n"
        for issue in issues[:10]:
            report += f"- {issue}\n"
        if len(issues) > 10:
            report += f"\n*... and {len(issues) - 10} more*\n"
        report += "\n"

    recommendations = api_data.get('recommendations', [])
    if recommendations:
        report += "**Recommendations**:\n"
        for rec in recommendations:
            report += f"- {rec}\n"
        report += "\n"

    return report


def generate_monitoring_section(metrics: Dict[str, Any]) -> str:
    """Generate monitoring and logging assessment section."""
    monitoring_data = coerce_section(metrics, 'monitoring_analysis')
    if not monitoring_data:
        return ""

    report = "\n## Monitoring & Logging Assessment\n\n"
    report += f"- **Logging Score**: {monitoring_data.get('logging_score', 0):.1f}/100\n"
    report += f"- **Monitoring Score**: {monitoring_data.get('monitoring_score', 0):.1f}/100\n"
    report += f"- **Observability Score**: {monitoring_data.get('observability_score', 0):.1f}/100\n"
    report += f"- **Monitoring Grade**: {monitoring_data.get('grade', 'N/A')}\n\n"

    issues = monitoring_data.get('issues', [])
    if issues:
        report += "**Monitoring Issues**:\n"
        for issue in issues[:10]:
            report += f"- {issue}\n"
        if len(issues) > 10:
            report += f"\n*... and {len(issues) - 10} more*\n"
        report += "\n"

    recommendations = monitoring_data.get('recommendations', [])
    if recommendations:
        report += "**Recommendations**:\n"
        for rec in recommendations:
            report += f"- {rec}\n"
        report += "\n"

    return report