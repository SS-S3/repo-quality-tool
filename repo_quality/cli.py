"""
Legacy CLI entrypoint. Use repo_quality/cli/entrypoint.py for the main CLI logic.
This file is kept for backward compatibility and will be removed in future versions.
"""

from .cli.entrypoint import assess

if __name__ == '__main__':
    assess()