import sys
import tempfile
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .clone import clone_repo
from .analyzers.lizard import analyze_lizard
from .analyzers.semgrep import analyze_semgrep
from .analyzers.dependency_analyzer import analyze_unused_dependencies, analyze_unused_python_packages
from .config_detector import detect_config_files
from .scoring import compute_scores
from .report import generate_markdown

console = Console()


@click.command()
@click.argument('repo_url')
@click.option('--output', '-o', default='report.md', help='Output file for the report')
@click.option('--fail-under', type=int, help='Fail if overall score is below this value')
def assess(repo_url: str, output: str, fail_under: Optional[int]) -> None:
    """Assess code quality of a GitHub repository."""
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
            sys.exit(1)

        # Count all code files for progress info
        exts = ["*.py", "*.js", "*.jsx", "*.ts", "*.tsx"]
        code_files = []
        
        # Search in common source directories
        search_dirs = [tmp_dir / d for d in ["server", "src", "lib", "app"]]
        search_dirs = [d for d in search_dirs if d.exists()]
        
        if not search_dirs:
            search_dirs = [tmp_dir]
        
        for search_dir in search_dirs:
            for ext in exts:
                code_files.extend(search_dir.rglob(ext))
        
        # Filter out common non-source directories
        excluded_dirs = {'node_modules', 'venv', '__pycache__', 'dist', 'build', '.git', 'coverage', '.next'}
        code_files = [f for f in code_files if not any(exc in f.parts for exc in excluded_dirs)]
        
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
        # Ensure semgrep_findings is present in metrics for report
        if 'semgrep_findings' in semgrep_metrics:
            metrics['semgrep_findings'] = semgrep_metrics['semgrep_findings']
        
        # Detect configuration files
        task = progress.add_task("Detecting configuration files...", total=None)
        config_files = detect_config_files(tmp_dir)
        metrics['config_files'] = config_files
        progress.update(task, description="Configuration detection complete")
        
        # Analyze unused dependencies
        task = progress.add_task("Analyzing dependencies...", total=None)
        js_deps = analyze_unused_dependencies(tmp_dir)
        py_deps = analyze_unused_python_packages(tmp_dir)
        metrics['js_dependencies'] = js_deps
        metrics['python_dependencies'] = py_deps
        progress.update(task, description="Dependency analysis complete")

        task = progress.add_task("Computing scores...", total=None)
        scores = compute_scores(metrics)
        progress.update(task, description="Scores computed")

        task = progress.add_task("Generating report...", total=None)
        generate_markdown(scores, output)
        progress.update(task, description=f"Report generated: {output}")

    overall_score = scores.get('overall', 0)
    console.print(f"[green]Overall Score: {overall_score:.1f}[/green]")

    if fail_under and overall_score < fail_under:
        console.print(f"[red]Score {overall_score:.1f} is below threshold {fail_under}[/red]")
        sys.exit(1)


if __name__ == '__main__':
    assess()