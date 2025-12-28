import os
import re
import ast
import subprocess
from pathlib import Path
from typing import Dict, List, Any


def analyze_compliance_standards(repo_path: str) -> Dict[str, Any]:
    """
    Analyze code compliance with standards and best practices.
    """
    compliance_metrics = {
        'linting_passed': False,
        'style_standard': None,
        'security_standards': [],
        'code_quality_issues': [],
        'compliance_score': 0,
        'violations': [],
        'standards_adhered': []
    }

    repo_path_obj = Path(repo_path)

    # Check for linting tools and run them
    linting_tools = _detect_linting_tools(repo_path_obj)

    if linting_tools:
        compliance_metrics['style_standard'] = list(linting_tools.keys())[0]

        # Run available linters
        for tool, config_file in linting_tools.items():
            try:
                result = _run_linter(tool, repo_path, config_file)
                if result['passed']:
                    compliance_metrics['linting_passed'] = True
                    compliance_metrics['standards_adhered'].append(f"{tool} compliant")
                else:
                    compliance_metrics['violations'].extend(result['issues'])
            except Exception as e:
                compliance_metrics['violations'].append(f"Failed to run {tool}: {str(e)}")

    # Check security standards
    security_standards = _check_security_standards(repo_path_obj)
    compliance_metrics['security_standards'] = security_standards['adhered']
    compliance_metrics['violations'].extend(security_standards['violations'])

    # Check code quality patterns
    quality_issues = _analyze_code_quality_patterns(repo_path_obj)
    compliance_metrics['code_quality_issues'] = quality_issues

    # Calculate compliance score
    score = 0

    # Linting score
    if compliance_metrics['linting_passed']:
        score += 40

    # Security standards score
    security_score = len(compliance_metrics['security_standards']) * 10
    score += min(30, security_score)

    # Code quality score (inverse of issues)
    quality_penalty = len(compliance_metrics['code_quality_issues']) * 5
    score += max(0, 30 - quality_penalty)

    compliance_metrics['compliance_score'] = min(100, score)

    # Overall compliance level
    if score >= 80:
        compliance_level = 'Excellent'
    elif score >= 60:
        compliance_level = 'Good'
    elif score >= 40:
        compliance_level = 'Fair'
    else:
        compliance_level = 'Poor'

    # Generate recommendations
    recommendations = []
    if not compliance_metrics['linting_passed']:
        recommendations.append('Fix linting violations or configure linters properly')
    if len(compliance_metrics['security_standards']) < 3:
        recommendations.append('Implement more security standards (OWASP, etc.)')
    if compliance_metrics['code_quality_issues']:
        recommendations.append('Address code quality anti-patterns')

    return {
        **compliance_metrics,
        'compliance_level': compliance_level,
        'recommendations': recommendations
    }


def _detect_linting_tools(repo_path: Path) -> Dict[str, str]:
    """Detect available linting tools and their config files."""
    linting_tools = {}

    # Python linters
    python_linters = {
        'flake8': ['.flake8', 'setup.cfg', 'tox.ini'],
        'pylint': ['.pylintrc', 'pylint.rc', 'setup.cfg'],
        'black': ['pyproject.toml'],
        'isort': ['.isort.cfg', 'pyproject.toml']
    }

    # JavaScript/TypeScript linters
    js_linters = {
        'eslint': ['.eslintrc.js', '.eslintrc.json', '.eslintrc.yml', 'package.json'],
        'prettier': ['.prettierrc', 'package.json'],
        'tslint': ['tslint.json']  # Legacy, but still used
    }

    # Check for Python files
    python_files = list(repo_path.glob('**/*.py'))
    if python_files:
        for linter, configs in python_linters.items():
            for config in configs:
                if (repo_path / config).exists():
                    linting_tools[linter] = config
                    break

    # Check for JS/TS files
    js_files = list(repo_path.glob('**/*.{js,jsx,ts,tsx}'))
    if js_files:
        for linter, configs in js_linters.items():
            for config in configs:
                if (repo_path / config).exists():
                    linting_tools[linter] = config
                    break

    return linting_tools


def _run_linter(tool: str, repo_path: str, config_file: str) -> Dict[str, Any]:
    """Run a specific linting tool and parse results."""
    try:
        if tool == 'flake8':
            cmd = ['flake8', '--max-line-length=100', '--extend-ignore=E203,W503', repo_path]
        elif tool == 'pylint':
            cmd = ['pylint', '--rcfile', config_file, '--output-format=json', repo_path]
        elif tool == 'black':
            cmd = ['black', '--check', '--diff', repo_path]
        elif tool == 'isort':
            cmd = ['isort', '--check-only', '--diff', repo_path]
        elif tool == 'eslint':
            cmd = ['npx', 'eslint', '--format=json', repo_path]
        elif tool == 'prettier':
            cmd = ['npx', 'prettier', '--check', repo_path]
        else:
            return {'passed': False, 'issues': [f"Unsupported linter: {tool}"]}

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=repo_path, timeout=30)

        if result.returncode == 0:
            return {'passed': True, 'issues': []}
        else:
            # Parse output for issues
            issues = _parse_linter_output(tool, result.stdout + result.stderr)
            return {'passed': False, 'issues': issues[:10]}  # Limit to first 10 issues

    except subprocess.TimeoutExpired:
        return {'passed': False, 'issues': [f"{tool} timed out"]}
    except FileNotFoundError:
        return {'passed': False, 'issues': [f"{tool} not installed"]}
    except Exception as e:
        return {'passed': False, 'issues': [f"Error running {tool}: {str(e)}"]}


def _parse_linter_output(tool: str, output: str) -> List[str]:
    """Parse linter output to extract issues."""
    issues = []

    if tool in ['flake8', 'pylint']:
        lines = output.strip().split('\n')
        for line in lines[:10]:  # Limit output
            if line.strip() and not line.startswith('Your code has been rated'):
                issues.append(line.strip())
    elif tool == 'eslint':
        try:
            import json
            data = json.loads(output)
            for file_data in data[:3]:  # Limit files
                file_path = file_data.get('filePath', 'unknown')
                for msg in file_data.get('messages', [])[:3]:  # Limit messages per file
                    rule = msg.get('ruleId', 'unknown')
                    line = msg.get('line', '?')
                    issues.append(f"{file_path}:{line} - {rule}")
        except:
            issues.append("Failed to parse ESLint output")
    else:
        # Generic parsing
        lines = output.strip().split('\n')[:5]
        issues.extend([line.strip() for line in lines if line.strip()])

    return issues


def _check_security_standards(repo_path: Path) -> Dict[str, List[str]]:
    """Check adherence to security standards."""
    adhered = []
    violations = []

    # Check for security-related files
    security_files = [
        '.env.example', 'security.md', 'SECURITY.md',
        'snyk.config', '.snyk', 'safety.txt'
    ]

    has_security_docs = any((repo_path / f).exists() for f in security_files)
    if has_security_docs:
        adhered.append('Security documentation present')
    else:
        violations.append('Missing security documentation')

    # Check for dependency vulnerability scanning setup
    vuln_files = ['requirements.txt', 'package.json', 'Pipfile', 'poetry.lock']
    has_deps = any((repo_path / f).exists() for f in vuln_files)
    if has_deps:
        adhered.append('Dependency management present')
    else:
        violations.append('No dependency files found')

    # Check for secrets in code (basic check)
    secrets_found = []
    code_files = list(repo_path.glob('**/*.{py,js,ts,json,yml,yaml}'))
    for code_file in code_files[:20]:  # Sample check
        try:
            with open(code_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

                # Check for hardcoded secrets
                secret_patterns = [
                    r'password\s*[:=]\s*[\'"][^\'"]*[\'"]',
                    r'secret\s*[:=]\s*[\'"][^\'"]*[\'"]',
                    r'api_key\s*[:=]\s*[\'"][^\'"]*[\'"]',
                    r'token\s*[:=]\s*[\'"][^\'"]*[\'"]'
                ]

                for pattern in secret_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        secrets_found.append(f"Potential secret in {code_file.name}")
                        break

        except:
            continue

    if not secrets_found:
        adhered.append('No hardcoded secrets detected')
    else:
        violations.extend(secrets_found[:3])  # Limit to 3 examples

    return {'adhered': adhered, 'violations': violations}


def _analyze_code_quality_patterns(repo_path: Path) -> List[str]:
    """Analyze code for quality anti-patterns."""
    issues = []

    code_files = list(repo_path.glob('**/*.{py,js,ts}'))
    for code_file in code_files[:15]:  # Sample for efficiency
        try:
            with open(code_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')

                # Check line length (PEP 8 style)
                long_lines = [i+1 for i, line in enumerate(lines) if len(line) > 100]
                if long_lines:
                    issues.append(f"Long lines in {code_file.name}: lines {long_lines[:3]}")

                # Check for TODO/FIXME comments
                todo_count = len(re.findall(r'TODO|FIXME|XXX', content, re.IGNORECASE))
                if todo_count > 5:
                    issues.append(f"High TODO count in {code_file.name}: {todo_count}")

                # Check for print statements in production code
                if code_file.suffix == '.py':
                    print_count = len(re.findall(r'\bprint\s*\(', content))
                    if print_count > 3:
                        issues.append(f"Debug print statements in {code_file.name}: {print_count}")

                # Check for empty catch blocks
                empty_catches = len(re.findall(r'except\s+.*:\s*pass', content))
                if empty_catches > 0:
                    issues.append(f"Empty except blocks in {code_file.name}: {empty_catches}")

        except:
            continue

    return issues