from pathlib import Path
from typing import Dict, Any


def generate_markdown(scores: Dict[str, Any], output_file: str) -> None:
    """Generate a Markdown report from scores.

    Args:
        output_file: Path to the output file.
    """
    metrics = scores['metrics']

    report = (
        f"# Code Quality Report\n\n"
        f"## Overall Score: {scores['overall_score']:.1f} ({scores['overall_grade']})\n\n"
        f"## Metrics Summary\n\n"
        f"| Metric | Value | Grade |\n"
        f"|--------|-------|-------|\n"
        f"| Maintainability | {scores['maint_score']:.1f} | {scores['maint_grade']} |\n"
        f"| Security | {scores['sec_score']:.1f} | {scores['sec_grade']} |\n"
        f"| Structure | {scores['struct_score']:.1f} | {scores['struct_grade']} |\n\n"
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

    # Add recommendations based on scores
    if scores['maint_score'] < 70:
        report += "- **Maintainability**: Refactor complex functions (CCN > 10) and reduce code duplication.\n"
    if scores['sec_score'] < 70:
        report += "- **Security**: Address critical and high-severity vulnerabilities immediately.\n"
    if scores['struct_score'] < 70:
        report += "- **Structure**: Simplify functions with too many parameters.\n"

    # Add top risky functions
    risky = metrics.get('risky_functions', [])
    if risky:
        report += "\n## Top Risky Functions\n\n"
        report += "| Function | CCN | Params |\n"
        report += "|----------|-----|--------|\n"
        for f in risky:
            report += f"| {f['location']} | {f['cyclomatic_complexity']} | {f['parameter_count']} |\n"
    else:
        report += "\n## Top Risky Functions\n\nNo functions analyzed.\n"

    # Add Semgrep findings if present
    findings = metrics.get('semgrep_findings', [])
    if findings:
        report += "\n## Security & Static Analysis Findings (Semgrep)\n\n"
        report += "| Severity | File | Line | Rule | Message |\n"
        report += "|----------|------|------|------|---------|\n"
        for f in findings:
            start_line = f.get('start', {}).get('line', '?')
            report += f"| {f['severity']} | {f['path']} | {start_line} | {f['rule_id']} | {f['message']} |\n"
    else:
        report += "\n## Security & Static Analysis Findings (Semgrep)\n\nNo issues detected.\n"

    # Add custom static analysis findings
    custom_findings = metrics.get('custom_static_findings', [])
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

    Path(output_file).write_text(report)
