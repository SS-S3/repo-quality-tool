from typing import Dict, Any


def generate_dependency_analysis(metrics: Dict[str, Any]) -> str:
    """Generate dependency analysis section."""
    js_deps = metrics.get('js_dependencies', {})
    py_deps = metrics.get('python_dependencies', {})

    if not (js_deps.get('has_package_json') or py_deps.get('has_requirements')):
        return ""

    report = "\n## Dependency Analysis\n\n"

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

    return report