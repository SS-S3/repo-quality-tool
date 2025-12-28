from pathlib import Path
from typing import Dict, Any


def generate_markdown(scores: Dict[str, Any], output_file: str) -> None:
    """Generate a Markdown report from scores.

    Args:
        output_file: Path to the output file.
    """
    metrics = scores['metrics']

    # --- Halstead per-main-file analysis ---
    import sys
    from .halstead import compute_main_files_halstead
    repo_root = metrics.get('repo_root')
    halstead_main_files = []
    if repo_root:
        try:
            halstead_main_files = compute_main_files_halstead(repo_root)
        except Exception as e:
            halstead_main_files = [{'file': 'ERROR', 'vocabulary': None, 'length': None, 'volume': None, 'difficulty': None, 'effort': None, 'error': str(e)}]

    def _coerce_section(key: str) -> dict:
        v = metrics.get(key, {})
        return v if isinstance(v, dict) else {}

    def _fmt_num(v, fmt=':.1f'):
        if v is None:
            return 'null'
        try:
            return format(v, fmt)
        except Exception:
            return str(v)

    # Track null reasons for each metric
    null_reasons = {}

    # Check for nulls and add explanations
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

    # Compose a final summary based on key metrics
    def _summary(scores):
        parts = []
        if scores.get('overall_score', 0) >= 80:
            parts.append('This codebase is production-ready with strong maintainability, security, and structure.')
        elif scores.get('overall_score', 0) >= 60:
            parts.append('This codebase is generally solid but has some areas for improvement, especially in testing, documentation, or CI/CD.')
        elif scores.get('overall_score', 0) >= 40:
            parts.append('This codebase has significant quality issues. Focus on improving maintainability, test coverage, and documentation.')
        else:
            parts.append('This codebase is in poor health. Major improvements are needed in maintainability, security, testing, and documentation.')
        # Add null metric notes
        for k, v in null_reasons.items():
            parts.append(f"{k}: {v}")
        return '\n'.join(parts)

    report = (
        f"# Code Quality Report\n\n"
        f"## Overall Score: {_fmt_num(scores.get('overall_score', None))} ({scores.get('overall_grade', 'N/A')})\n\n"
        f"## Metrics Summary\n\n"
        f"| Metric | Value | Grade |\n"
        f"|--------|-------|-------|\n"
        f"| Maintainability | {_fmt_num(scores.get('maint_score', None))} | {scores.get('maint_grade', 'N/A')} |\n"
        f"| Security | {_fmt_num(scores.get('sec_score', None))} | {scores.get('sec_grade', 'N/A')} |\n"
        f"| Structure | {_fmt_num(scores.get('struct_score', None))} | {scores.get('struct_grade', 'N/A')} |\n"
        f"| Testing Quality | {_fmt_num(scores.get('testing_score', None))} | {scores.get('testing_grade', 'N/A')} | {'Reason: ' + null_reasons['Testing Quality'] if 'Testing Quality' in null_reasons else ''}\n"
        f"| Code Coverage | {_fmt_num(scores.get('coverage_score', None))} | {scores.get('coverage_grade', 'N/A')} | {'Reason: ' + null_reasons['Code Coverage'] if 'Code Coverage' in null_reasons else ''}\n"
        f"| Documentation | {_fmt_num(scores.get('docs_score', None))} | {scores.get('docs_grade', 'N/A')} | {'Reason: ' + null_reasons['Documentation'] if 'Documentation' in null_reasons else ''}\n"
        f"| CI/CD | {_fmt_num(scores.get('ci_cd_score', None))} | {scores.get('ci_cd_grade', 'N/A')} | {'Reason: ' + null_reasons['CI/CD'] if 'CI/CD' in null_reasons else ''}\n"
        f"| Compliance | {_fmt_num(scores.get('compliance_score', None))} | {scores.get('compliance_grade', 'N/A')} |\n"
        f"| API Quality | {_fmt_num(scores.get('api_score', None))} | {scores.get('api_grade', 'N/A')} | {'Reason: ' + null_reasons['API Quality'] if 'API Quality' in null_reasons else ''}\n"
        f"| Monitoring | {_fmt_num(scores.get('monitoring_score', None))} | {scores.get('monitoring_grade', 'N/A')} | {'Reason: ' + null_reasons['Monitoring'] if 'Monitoring' in null_reasons else ''}\n\n"
        f"## Detailed Metrics\n\n"
        f"### Complexity\n"
        f"| Metric | Value | Grade |\n"
        f"|--------|-------|-------|\n"
        f"| Average Cyclomatic Complexity | {metrics.get('avg_ccn', 0):.1f} | {scores['ccn_grade']} |\n"
        f"| Max Cyclomatic Complexity | {metrics.get('max_ccn', 0)} | - |\n"
        f"| % Functions CCN > 10 | {metrics.get('pct_ccn_gt_10', 0):.1f}% | - |\n\n"
        f"### Duplication\n"
        f"| Metric | Value | Grade |\n"
        f"|--------|-------|-------|\n"
        f"| Code Duplication % | {metrics.get('duplication_pct', 0):.1f}% | {scores['dup_grade']} |\n\n"
        f"### Security\n"
        f"| Severity | Count |\n"
        f"|----------|-------|\n"
        f"| Critical | {metrics.get('security_critical', 0)} |\n"
        f"| High | {metrics.get('security_high', 0)} |\n"
        f"| Medium | {metrics.get('security_medium', 0)} |\n"
        f"| Low | {metrics.get('security_low', 0)} |\n\n"
        f"### Structure\n"
        f"| Metric | Value |\n"
        f"|--------|-------|\n"
        f"| Functions with >7 Parameters | {metrics.get('functions_gt_7_params', 0)} |\n\n"
        f"## Recommendations\n\n"
    )

    # Add config/workflow file checks dynamically
    config_files = metrics.get('config_files', {})
    report += "\n## Configuration & Workflow Files\n\n"
    report += "| File | Present |\n"
    report += "|------|---------|\n"
    for name, present in config_files.items():
        report += f"| {name} | {'✅' if present else '❌'} |\n"

    # Add recommendations based on scores (only when numeric)
    if scores.get('maint_score') is not None and scores.get('maint_score') < 70:
        report += "- **Maintainability**: Refactor complex functions (CCN > 10) and reduce code duplication.\n"
    if scores.get('sec_score') is not None and scores.get('sec_score') < 70:
        report += "- **Security**: Address critical and high-severity vulnerabilities immediately.\n"
    if scores.get('struct_score') is not None and scores.get('struct_score') < 70:
        report += "- **Structure**: Simplify functions with too many parameters.\n"
    if scores.get('coverage_score') is not None and scores.get('coverage_score') < 80:
        report += "- **Coverage**: Improve test coverage to at least 80%.\n"
    if scores.get('testing_score') is not None and scores.get('testing_score') < 70:
        report += "- **Testing**: Enhance test suite quality and coverage.\n"
    if scores.get('docs_score') is not None and scores.get('docs_score') < 70:
        report += "- **Documentation**: Add comprehensive docstrings and improve README.\n"
    if scores.get('ci_cd_score') is not None and scores.get('ci_cd_score') < 70:
        report += "- **CI/CD**: Implement proper CI/CD pipelines with security scanning.\n"
    if scores.get('compliance_score') is not None and scores.get('compliance_score') < 70:
        report += "- **Compliance**: Fix linting issues and adhere to coding standards.\n"
    if scores.get('api_score') is not None and scores.get('api_score') < 70:
        report += "- **API Quality**: Improve API design and security practices.\n"
    if scores.get('monitoring_score') is not None and scores.get('monitoring_score') < 70:
        report += "- **Monitoring**: Implement proper logging and monitoring.\n"


    # Add top risky functions and complexity breakdown, including Halstead metrics
    risky = metrics.get('risky_functions', []) if isinstance(metrics.get('risky_functions', []), list) else []
    report += "\n## Complexity & Risky Functions\n\n"
    avg_ccn = metrics.get('avg_ccn', None)
    max_ccn = metrics.get('max_ccn', None)
    pct_ccn_gt_10 = metrics.get('pct_ccn_gt_10', None)
    # Halstead metrics (if present)
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

    # --- Per-main-file Halstead metrics ---
    if halstead_main_files:
        report += "\n### Halstead Metrics for Main Files\n\n"
        report += "| File | Vocabulary | Length | Volume | Difficulty | Effort |\n"
        report += "|------|------------|--------|--------|------------|--------|\n"
        for h in halstead_main_files:
            report += f"| {h.get('file', 'N/A')} | {h.get('vocabulary', 'N/A')} | {h.get('length', 'N/A')} | {h.get('volume', 'N/A')} | {h.get('difficulty', 'N/A')} | {h.get('effort', 'N/A')} |\n"

    if risky:
        report += "\n| Function | CCN | Params |\n"
        report += "|----------|-----|--------|\n"
        for f in risky:
            report += f"| {f['location']} | {f['cyclomatic_complexity']} | {f['parameter_count']} |\n"
    else:
        report += "No risky functions detected or complexity analysis failed.\n"

    # Add final summary
    report += "\n## Final Summary\n\n"
    report += _summary(scores)

    # Add Semgrep findings if present, limit to 10
    findings = metrics.get('semgrep_findings', []) if isinstance(metrics.get('semgrep_findings', []), list) else []
    if findings:
        report += "\n## Security & Static Analysis Findings (Semgrep)\n\n"
        report += f"**Total Security Findings:** {len(findings)}\n\n"
        # Count by severity
        severity_counts = {'CRITICAL': 0, 'ERROR': 0, 'WARNING': 0, 'INFO': 0}
        for f in findings:
            sev = f.get('severity', '').upper()
            if sev in severity_counts:
                severity_counts[sev] += 1
            else:
                severity_counts['INFO'] += 1
        report += f"- Critical: {severity_counts['CRITICAL']}\n"
        report += f"- Error: {severity_counts['ERROR']}\n"
        report += f"- Warning: {severity_counts['WARNING']}\n"
        report += f"- Info: {severity_counts['INFO']}\n\n"
        report += "| Severity | File | Line | Rule | Message |\n"
        report += "|----------|------|------|------|---------|\n"
        for f in findings[:10]:
            start_line = f.get('start', {}).get('line', '?')
            report += f"| {f['severity']} | {f['path']} | {start_line} | {f['rule_id']} | {f['message']} |\n"
        if len(findings) > 10:
            report += f"\n*... and {len(findings) - 10} more findings not shown*\n"
    else:
        report += "\n## Security & Static Analysis Findings (Semgrep)\n\nNo issues detected.\n"

    # Add custom static analysis findings
    custom_findings = metrics.get('custom_static_findings', []) if isinstance(metrics.get('custom_static_findings', []), list) else []
    report += "\n## Custom Static Analysis Findings\n\n"
    if custom_findings:
        # Group by type for better readability
        ai_placeholders = [f for f in custom_findings if f['type'] in ['AI/Placeholder Code', 'Potential Placeholder Function']]
        security_issues = [f for f in custom_findings if f['type'] in ['Dangerous Function', 'SQL Injection Risk', 'Hardcoded Credential', 'Insecure Import', 'Potential Secret']]
        quality_issues = [f for f in custom_findings if f['type'] in ['Code Quality Issue', 'Missing Best Practice']]
        
        if ai_placeholders:
            report += f"\n### AI-Generated/Placeholder Code ({len(ai_placeholders)} instances)\n\n"
            report += "| Type | File | Line | Snippet |\n"
            report += "|------|------|------|---------|\n"
            for f in ai_placeholders[:20]:  # Limit to first 20
                report += f"| {f['type']} | {f['file']} | {f['line']} | {f['content']} |\n"
            if len(ai_placeholders) > 20:
                report += f"\n*... and {len(ai_placeholders) - 20} more*\n"
        
        if security_issues:
            report += f"\n### Security Issues ({len(security_issues)} instances)\n\n"
            report += "| Type | File | Line | Snippet |\n"
            report += "|------|------|------|---------|\n"
            for f in security_issues[:20]:
                report += f"| {f['type']} | {f['file']} | {f['line']} | {f['content']} |\n"
            if len(security_issues) > 20:
                report += f"\n*... and {len(security_issues) - 20} more*\n"
        
        if quality_issues:
            report += f"\n### Code Quality Issues ({len(quality_issues)} instances)\n\n"
            report += "| Type | File | Line | Snippet |\n"
            report += "|------|------|------|---------|\n"
            for f in quality_issues[:20]:
                report += f"| {f['type']} | {f['file']} | {f['line']} | {f['content']} |\n"
            if len(quality_issues) > 20:
                report += f"\n*... and {len(quality_issues) - 20} more*\n"
    else:
        report += "No custom static issues detected.\n"
    
    # Add unused dependencies analysis
    js_deps = metrics.get('js_dependencies', {})
    py_deps = metrics.get('python_dependencies', {})
    
    if js_deps.get('has_package_json') or py_deps.get('has_requirements'):
        report += "\n## Dependency Analysis\n\n"
        
        if js_deps.get('has_package_json'):
            unused_deps = js_deps.get('unused_dependencies', [])
            unused_dev = js_deps.get('unused_dev_dependencies', [])
            usage_rate = js_deps.get('dependency_usage_rate', 100)
            
            report += f"### JavaScript/TypeScript Dependencies\n\n"
            report += f"- **Total Dependencies**: {js_deps.get('total_dependencies', 0)}\n"
            report += f"- **Total Dev Dependencies**: {js_deps.get('total_dev_dependencies', 0)}\n"
            report += f"- **Dependency Usage Rate**: {usage_rate:.1f}%\n\n"
            
            if unused_deps:
                report += f"**Unused Dependencies ({len(unused_deps)})**:\n"
                for dep in unused_deps[:10]:
                    report += f"- {dep}\n"
                if len(unused_deps) > 10:
                    report += f"\n*... and {len(unused_deps) - 10} more*\n"
            
            if unused_dev:
                report += f"\n**Unused Dev Dependencies ({len(unused_dev)})**:\n"
                for dep in unused_dev[:10]:
                    report += f"- {dep}\n"
                if len(unused_dev) > 10:
                    report += f"\n*... and {len(unused_dev) - 10} more*\n\n"
        
        if py_deps.get('has_requirements'):
            unused_pkgs = py_deps.get('unused_packages', [])
            usage_rate = py_deps.get('package_usage_rate', 100)
            
            report += f"### Python Dependencies\n\n"
            report += f"- **Total Packages**: {py_deps.get('total_packages', 0)}\n"
            report += f"- **Package Usage Rate**: {usage_rate:.1f}%\n\n"
            
            if unused_pkgs:
                report += f"**Unused Packages ({len(unused_pkgs)})**:\n"
                for pkg in unused_pkgs[:10]:
                    report += f"- {pkg}\n"
                if len(unused_pkgs) > 10:
                    report += f"\n*... and {len(unused_pkgs) - 10} more*\n"

    # Add Coverage Analysis
    coverage_data = _coerce_section('coverage_analysis')
    if coverage_data:
        report += "\n## Code Coverage Analysis\n\n"
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

    # Add Testing Quality Analysis
    testing_data = _coerce_section('testing_quality')
    if testing_data:
        report += "\n## Testing Quality Assessment\n\n"
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

    # Add Documentation Quality Analysis
    docs_data = _coerce_section('documentation_quality')
    if docs_data:
        report += "\n## Documentation Quality Assessment\n\n"
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

    # Add CI/CD Analysis
    ci_cd_data = _coerce_section('ci_cd_analysis')
    if ci_cd_data:
        report += "\n## CI/CD Pipeline Analysis\n\n"
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

    # Add Compliance Analysis
    compliance_data = _coerce_section('compliance_analysis')
    if compliance_data:
        report += "\n## Compliance & Standards Analysis\n\n"
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

    # Add API Quality Analysis
    api_data = _coerce_section('api_quality')
    if api_data:
        report += "\n## API Quality Assessment\n\n"
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

    # Add Monitoring Analysis
    monitoring_data = _coerce_section('monitoring_analysis')
    if monitoring_data:
        report += "\n## Monitoring & Logging Assessment\n\n"
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

    Path(output_file).write_text(report)
