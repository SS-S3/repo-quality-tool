import tempfile
from pathlib import Path
from typing import Union

import git


def clone_repo(repo_url: str) -> Path:
    """Clone a GitHub repository to a temporary directory.

    Args:
        repo_url: The URL of the GitHub repository.

    Returns:
        Path to the cloned repository.

    Raises:
        Exception: If cloning fails.
    """
    tmp_dir = Path(tempfile.mkdtemp())
    try:
        git.Repo.clone_from(repo_url, tmp_dir)
        return tmp_dir
    except Exception as e:
        # Clean up on failure
        import shutil
        shutil.rmtree(tmp_dir, ignore_errors=True)
        raise e