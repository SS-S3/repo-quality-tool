from pathlib import Path
from typing import Dict, Any


def detect_config_files(repo_path: Path) -> Dict[str, bool]:
    """Detect presence of important configuration files for both Python and JS/TS projects.
    
    Args:
        repo_path: Path to the repository.
    
    Returns:
        Dictionary mapping config file names to their presence.
    """
    config_checks = {}
    
    # GitHub Actions / CI/CD
    config_checks['GitHub Actions Workflow'] = (repo_path / '.github' / 'workflows').exists()
    config_checks['GitLab CI'] = (repo_path / '.gitlab-ci.yml').exists()
    config_checks['CircleCI'] = (repo_path / '.circleci' / 'config.yml').exists()
    
    # JavaScript/TypeScript configs
    config_checks['package.json'] = (repo_path / 'package.json').exists()
    config_checks['tsconfig.json'] = (repo_path / 'tsconfig.json').exists()
    config_checks['ESLint Config'] = any([
        (repo_path / '.eslintrc.js').exists(),
        (repo_path / '.eslintrc.json').exists(),
        (repo_path / '.eslintrc.yml').exists(),
        (repo_path / 'eslint.config.js').exists()
    ])
    config_checks['Prettier Config'] = any([
        (repo_path / '.prettierrc').exists(),
        (repo_path / '.prettierrc.json').exists(),
        (repo_path / 'prettier.config.js').exists()
    ])
    
    # Python configs
    config_checks['requirements.txt'] = (repo_path / 'requirements.txt').exists()
    config_checks['setup.py'] = (repo_path / 'setup.py').exists()
    config_checks['pyproject.toml'] = (repo_path / 'pyproject.toml').exists()
    config_checks['Pipfile'] = (repo_path / 'Pipfile').exists()
    config_checks['poetry.lock'] = (repo_path / 'poetry.lock').exists()
    config_checks['pylint Config'] = any([
        (repo_path / '.pylintrc').exists(),
        (repo_path / 'pylintrc').exists()
    ])
    config_checks['pytest Config'] = any([
        (repo_path / 'pytest.ini').exists(),
        (repo_path / 'pyproject.toml').exists()
    ])
    
    # Security
    config_checks['.env'] = (repo_path / '.env').exists()
    config_checks['.env.example'] = (repo_path / '.env.example').exists()
    config_checks['Security Policy'] = (repo_path / 'SECURITY.md').exists()
    
    # Docker
    config_checks['Dockerfile'] = (repo_path / 'Dockerfile').exists()
    config_checks['docker-compose.yml'] = (repo_path / 'docker-compose.yml').exists()
    
    # Documentation
    config_checks['README.md'] = (repo_path / 'README.md').exists()
    config_checks['LICENSE'] = any([
        (repo_path / 'LICENSE').exists(),
        (repo_path / 'LICENSE.md').exists(),
        (repo_path / 'LICENSE.txt').exists()
    ])
    config_checks['CONTRIBUTING.md'] = (repo_path / 'CONTRIBUTING.md').exists()
    
    # Testing
    config_checks['jest.config.js'] = (repo_path / 'jest.config.js').exists()
    config_checks['vitest.config'] = any([
        (repo_path / 'vitest.config.js').exists(),
        (repo_path / 'vitest.config.ts').exists()
    ])
    
    # Git
    config_checks['.gitignore'] = (repo_path / '.gitignore').exists()
    
    return config_checks
