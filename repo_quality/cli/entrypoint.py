import sys
import click
from rich.console import Console
from .main import run_analysis

console = Console()

@click.command()
@click.argument('repo_url')
@click.option('--output', '-o', default='report.md', help='Output file for the report')
@click.option('--fail-under', type=int, help='Fail if overall score is below this value')
def assess(repo_url: str, output: str, fail_under: int):
    """Assess code quality of a GitHub repository."""
    try:
        run_analysis(repo_url, output, fail_under, console)
    except SystemExit as e:
        sys.exit(e.code)
    except Exception as e:
        console.print(f"[red]Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    assess()
