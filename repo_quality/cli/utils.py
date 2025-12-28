from pathlib import Path
from typing import List
import os

def filter_code_files(repo_root: Path, search_dirs: List[str]) -> List[str]:
    code_files = []
    for search_dir in search_dirs:
        for root, _, files in os.walk(search_dir):
            for file in files:
                if file.endswith(('.py', '.js', '.ts')):
                    code_files.append(os.path.join(root, file))
    return code_files

def get_search_dirs(repo_root: Path) -> List[str]:
    # Add logic to determine which directories to search for code files
    # For now, just return the repo root
    return [str(repo_root)]
