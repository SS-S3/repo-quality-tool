from pathlib import Path
from typing import Dict, Any, List
from ..halstead import compute_main_files_halstead
from .summary import get_null_reasons, generate_summary
from .sections import (
    generate_header,
    generate_metrics_summary,
    generate_detailed_metrics,
    generate_recommendations,
    generate_config_section,
    generate_complexity_section
)
from .security import generate_semgrep_findings, generate_custom_findings
from .dependencies import generate_dependency_analysis
from .analyzers import (
    generate_coverage_section,
    generate_testing_section,
    generate_documentation_section,
    generate_ci_cd_section,
    generate_compliance_section,
    generate_api_section,
    generate_monitoring_section
)


def generate_markdown(scores: Dict[str, Any], output_file: str) -> None:
    """Generate a Markdown report from scores.

    Args:
        output_file: Path to the output file.
    """
    metrics = scores['metrics']

    # --- Halstead per-main-file analysis ---
    halstead_main_files = []
    repo_root = metrics.get('repo_root')
    if repo_root:
        try:
            halstead_main_files = compute_main_files_halstead(repo_root)
        except Exception as e:
            halstead_main_files = [{'file': 'ERROR', 'vocabulary': None, 'length': None, 'volume': None, 'difficulty': None, 'effort': None, 'error': str(e)}]

    # Track null reasons for each metric
    null_reasons = get_null_reasons(scores)

    # Compose the report
    report = ""
    report += generate_header(scores)
    report += generate_metrics_summary(scores, null_reasons)
    report += generate_detailed_metrics(metrics, scores)
    report += generate_recommendations(scores)
    report += generate_config_section(metrics)
    report += generate_complexity_section(metrics, halstead_main_files)
    report += generate_semgrep_findings(metrics)
    report += generate_custom_findings(metrics)
    report += generate_dependency_analysis(metrics)
    report += generate_coverage_section(metrics)
    report += generate_testing_section(metrics)
    report += generate_documentation_section(metrics)
    report += generate_ci_cd_section(metrics)
    report += generate_compliance_section(metrics)
    report += generate_api_section(metrics)
    report += generate_monitoring_section(metrics)

    # Add final summary
    report += "\n## Final Summary\n\n"
    report += generate_summary(scores, null_reasons)

    Path(output_file).write_text(report)