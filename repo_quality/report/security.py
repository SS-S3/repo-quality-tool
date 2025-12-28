from typing import Dict, Any, List


def generate_semgrep_findings(metrics: Dict[str, Any]) -> str:
    """Generate Semgrep security findings section."""
    findings = metrics.get('semgrep_findings', []) if isinstance(metrics.get('semgrep_findings', []), list) else []

    report = "\n## Security & Static Analysis Findings (Semgrep)\n\n"
    if findings:
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
        report += "No issues detected.\n"

    return report


def generate_custom_findings(metrics: Dict[str, Any]) -> str:
    """Generate custom static analysis findings section."""
    custom_findings = metrics.get('custom_static_findings', []) if isinstance(metrics.get('custom_static_findings', []), list) else []

    report = "\n## Custom Static Analysis Findings\n\n"
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

    return report