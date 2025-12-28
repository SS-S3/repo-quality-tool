from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from ..clone import clone_repo
from ..analyzers.lizard import analyze_lizard
from ..analyzers.semgrep import analyze_semgrep
from ..analyzers.dependency_analyzer import analyze_unused_dependencies, analyze_unused_python_packages
from ..analyzers.coverage import analyze_code_coverage
from ..analyzers.testing_quality import analyze_testing_quality
from ..analyzers.documentation import analyze_documentation_quality
from ..analyzers.ci_cd import analyze_ci_cd_pipeline
from ..analyzers.compliance import analyze_compliance_standards
from ..analyzers.api_quality import analyze_api_quality
from ..analyzers.monitoring import analyze_monitoring_logging
from ..config_detector import detect_config_files
from ..scoring import compute_scores
from ..report import generate_markdown
from .utils import filter_code_files, get_search_dirs


def run_analysis(repo_url: str, output: str, fail_under: Optional[int], console: Console) -> None:
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Cloning repository...", total=None)
        try:
            tmp_dir = clone_repo(repo_url)
            console.print(f"[yellow]Cloned to: {tmp_dir}")
            progress.update(task, description="Repository cloned successfully")
        except Exception as e:
            console.print(f"[red]Failed to clone repository: {e}[/red]")
            raise

        code_files = filter_code_files(tmp_dir, get_search_dirs(tmp_dir))
        num_code_files = len(code_files)
        task = progress.add_task(f"Analyzing {num_code_files} code files with Lizard...", total=None)
        try:
            lizard_metrics = analyze_lizard(tmp_dir)
            progress.update(task, description=f"Lizard analysis complete ({num_code_files} files)")
        except Exception as e:
            console.print(f"[red]Lizard analysis failed: {e}[/red]")
            lizard_metrics = {}

        task = progress.add_task("Analyzing security with Semgrep...", total=None)
        try:
            semgrep_metrics = analyze_semgrep(tmp_dir)
            progress.update(task, description="Semgrep analysis complete")
        except Exception as e:
            console.print(f"[red]Semgrep analysis failed: {e}[/red]")
            semgrep_metrics = {}

        metrics = {**lizard_metrics, **semgrep_metrics}
        metrics['repo_root'] = str(tmp_dir)
        if 'semgrep_findings' in semgrep_metrics:
            metrics['semgrep_findings'] = semgrep_metrics['semgrep_findings']

        task = progress.add_task("Detecting configuration files...", total=None)
        config_files = detect_config_files(tmp_dir)
        metrics['config_files'] = config_files
        progress.update(task, description="Configuration detection complete")

        task = progress.add_task("Analyzing dependencies...", total=None)
        js_deps = analyze_unused_dependencies(tmp_dir)
        py_deps = analyze_unused_python_packages(tmp_dir)
        metrics['js_dependencies'] = js_deps
        metrics['python_dependencies'] = py_deps
        progress.update(task, description="Dependency analysis complete")

        task = progress.add_task("Analyzing code coverage...", total=None)
        coverage_metrics = analyze_code_coverage(tmp_dir)
        metrics.update(coverage_metrics)
        progress.update(task, description="Coverage analysis complete")

        task = progress.add_task("Analyzing testing quality...", total=None)
        testing_metrics = analyze_testing_quality(tmp_dir)
        metrics.update(testing_metrics)
        progress.update(task, description="Testing quality analysis complete")

        task = progress.add_task("Analyzing documentation...", total=None)
        docs_metrics = analyze_documentation_quality(tmp_dir)
        metrics.update(docs_metrics)
        progress.update(task, description="Documentation analysis complete")

        task = progress.add_task("Analyzing CI/CD pipeline...", total=None)
        ci_cd_metrics = analyze_ci_cd_pipeline(tmp_dir)
        metrics.update(ci_cd_metrics)
        progress.update(task, description="CI/CD analysis complete")

        task = progress.add_task("Analyzing compliance...", total=None)
        compliance_metrics = analyze_compliance_standards(tmp_dir)
        metrics.update(compliance_metrics)
        progress.update(task, description="Compliance analysis complete")

        task = progress.add_task("Analyzing API quality...", total=None)
        api_metrics = analyze_api_quality(tmp_dir)
        metrics.update(api_metrics)
        progress.update(task, description="API quality analysis complete")

        task = progress.add_task("Analyzing monitoring...", total=None)
        monitoring_metrics = analyze_monitoring_logging(tmp_dir)
        metrics.update(monitoring_metrics)
        progress.update(task, description="Monitoring analysis complete")

        task = progress.add_task("Computing scores...", total=None)
        scores = compute_scores(metrics)
        progress.update(task, description="Scores computed")

        task = progress.add_task("Generating report...", total=None)
        generate_markdown(scores, output)
        progress.update(task, description=f"Report generated: {output}")

    overall_score = scores.get('overall_score')
    overall_display = overall_score if overall_score is not None else 'null'
    try:
        console.print(f"[green]Overall Score: {overall_display:.1f}[/green]")
    except Exception:
        console.print(f"[green]Overall Score: {overall_display}[/green]")

    if fail_under and overall_score is not None and overall_score < fail_under:
        console.print(f"[red]Score {overall_score:.1f} is below threshold {fail_under}[/red]")
        raise SystemExit(1)
