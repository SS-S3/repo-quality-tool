import os
import re
import yaml
import json
from pathlib import Path
from typing import Dict, List, Any


def analyze_ci_cd_pipeline(repo_path: str) -> Dict[str, Any]:
    """
    Analyze CI/CD pipeline configurations for best practices.
    """
    ci_metrics = {
        'ci_provider': None,
        'has_ci': False,
        'has_testing': False,
        'has_linting': False,
        'has_security_scanning': False,
        'has_build': False,
        'has_deploy': False,
        'parallel_jobs': 0,
        'environments': [],
        'ci_quality_score': 0,
        'missing_practices': [],
        'security_concerns': [],
        'performance_issues': []
    }

    repo_path_obj = Path(repo_path)

    # Detect CI/CD providers
    ci_files = {
        'github_actions': ['.github/workflows/*.yml', '.github/workflows/*.yaml'],
        'gitlab_ci': ['.gitlab-ci.yml'],
        'jenkins': ['Jenkinsfile', 'jenkins/*'],
        'circle_ci': ['.circleci/config.yml'],
        'travis_ci': ['.travis.yml'],
        'azure_pipelines': ['azure-pipelines.yml', '.azuredevops/**/*.yml'],
        'bitbucket': ['bitbucket-pipelines.yml']
    }

    detected_provider = None
    ci_config_files = []

    for provider, patterns in ci_files.items():
        for pattern in patterns:
            matches = list(repo_path_obj.glob(pattern))
            if matches:
                detected_provider = provider
                ci_config_files.extend(matches)
                break
        if detected_provider:
            break

    if not detected_provider:
        return {
            **ci_metrics,
            'ci_quality': 'No CI/CD detected',
            'recommendations': ['Implement CI/CD pipeline', 'Add automated testing', 'Include security scanning']
        }

    ci_metrics['ci_provider'] = detected_provider
    ci_metrics['has_ci'] = True

    # Analyze CI configuration
    for config_file in ci_config_files:
        try:
            if config_file.suffix in ['.yml', '.yaml']:
                with open(config_file, 'r', encoding='utf-8', errors='ignore') as f:
                    config = yaml.safe_load(f)
                    _analyze_yaml_ci(config, ci_metrics, detected_provider)
            elif config_file.name == 'Jenkinsfile':
                with open(config_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    _analyze_jenkins_ci(content, ci_metrics)
        except Exception as e:
            continue

    # Calculate CI quality score
    score = 20  # Base score for having CI

    if ci_metrics['has_testing']:
        score += 25
    if ci_metrics['has_linting']:
        score += 15
    if ci_metrics['has_security_scanning']:
        score += 20
    if ci_metrics['has_build']:
        score += 10
    if ci_metrics['has_deploy']:
        score += 10

    # Bonus for multiple environments
    score += min(10, len(ci_metrics['environments']) * 2)

    # Bonus for parallel jobs
    score += min(10, ci_metrics['parallel_jobs'] * 2)

    ci_metrics['ci_quality_score'] = min(100, score)

    # Identify missing practices
    missing = []
    if not ci_metrics['has_testing']:
        missing.append('Automated testing')
    if not ci_metrics['has_linting']:
        missing.append('Code linting')
    if not ci_metrics['has_security_scanning']:
        missing.append('Security vulnerability scanning')
    if not ci_metrics['has_build']:
        missing.append('Automated building')
    if not ci_metrics['environments']:
        missing.append('Multiple deployment environments')

    ci_metrics['missing_practices'] = missing

    # Determine overall quality
    if score >= 80:
        quality = 'Excellent'
    elif score >= 60:
        quality = 'Good'
    elif score >= 40:
        quality = 'Fair'
    else:
        quality = 'Poor'

    return {
        **ci_metrics,
        'ci_quality': quality,
        'recommendations': [f"Add {practice}" for practice in missing]
    }


def _analyze_yaml_ci(config: Dict[str, Any], ci_metrics: Dict[str, Any], provider: str):
    """Analyze YAML-based CI configurations (GitHub Actions, GitLab, etc.)."""

    if provider == 'github_actions':
        # GitHub Actions analysis
        if 'jobs' in config:
            jobs = config['jobs']
            ci_metrics['parallel_jobs'] = len(jobs)

            for job_name, job_config in jobs.items():
                steps = job_config.get('steps', [])

                # Check for testing
                test_keywords = ['test', 'pytest', 'jest', 'npm test', 'python -m pytest']
                if any(any(keyword in str(step) for keyword in test_keywords) for step in steps):
                    ci_metrics['has_testing'] = True

                # Check for linting
                lint_keywords = ['lint', 'eslint', 'flake8', 'pylint', 'black']
                if any(any(keyword in str(step) for keyword in lint_keywords) for step in steps):
                    ci_metrics['has_linting'] = True

                # Check for security scanning
                security_keywords = ['security', 'audit', 'scan', 'snyk', 'safety', 'bandit']
                if any(any(keyword in str(step) for keyword in security_keywords) for step in steps):
                    ci_metrics['has_security_scanning'] = True

                # Check for building
                build_keywords = ['build', 'compile', 'webpack', 'setup.py']
                if any(any(keyword in str(step) for keyword in build_keywords) for step in steps):
                    ci_metrics['has_build'] = True

                # Check for deployment
                deploy_keywords = ['deploy', 'publish', 'release', 'docker push']
                if any(any(keyword in str(step) for keyword in deploy_keywords) for step in steps):
                    ci_metrics['has_deploy'] = True

                # Check environments
                if 'environment' in job_config:
                    env = job_config['environment']
                    if isinstance(env, str) and env not in ci_metrics['environments']:
                        ci_metrics['environments'].append(env)

    elif provider == 'gitlab_ci':
        # GitLab CI analysis
        for job_name, job_config in config.items():
            if not isinstance(job_config, dict):
                continue

            script = job_config.get('script', [])
            ci_metrics['parallel_jobs'] += 1

            script_text = ' '.join(script) if isinstance(script, list) else str(script)

            # Similar checks as GitHub Actions
            if any(kw in script_text.lower() for kw in ['test', 'pytest', 'jest']):
                ci_metrics['has_testing'] = True
            if any(kw in script_text.lower() for kw in ['lint', 'eslint', 'flake8']):
                ci_metrics['has_linting'] = True
            if any(kw in script_text.lower() for kw in ['security', 'audit', 'snyk']):
                ci_metrics['has_security_scanning'] = True
            if any(kw in script_text.lower() for kw in ['build', 'compile']):
                ci_metrics['has_build'] = True
            if any(kw in script_text.lower() for kw in ['deploy', 'publish']):
                ci_metrics['has_deploy'] = True

            # Check environments
            if 'environment' in job_config:
                env = job_config['environment']
                if isinstance(env, dict) and 'name' in env:
                    env_name = env['name']
                    if env_name not in ci_metrics['environments']:
                        ci_metrics['environments'].append(env_name)


def _analyze_jenkins_ci(content: str, ci_metrics: Dict[str, Any]):
    """Analyze Jenkins pipeline configuration."""

    # Basic checks for Jenkins pipeline
    if 'pipeline' in content.lower():
        ci_metrics['parallel_jobs'] = len(re.findall(r'stage\s*\(', content, re.IGNORECASE))

        # Check for various practices
        if re.search(r'test|pytest|jest', content, re.IGNORECASE):
            ci_metrics['has_testing'] = True
        if re.search(r'lint|eslint|flake8', content, re.IGNORECASE):
            ci_metrics['has_linting'] = True
        if re.search(r'security|audit|snyk', content, re.IGNORECASE):
            ci_metrics['has_security_scanning'] = True
        if re.search(r'build|compile', content, re.IGNORECASE):
            ci_metrics['has_build'] = True
        if re.search(r'deploy|publish', content, re.IGNORECASE):
            ci_metrics['has_deploy'] = True