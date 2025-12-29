# Code Quality Report

## Overall Score: 56.42008584234194 (Poor)

## Metrics Summary

| Metric | Value | Grade |
|--------|-------|-------|
| Maintainability | 27.969847225944793 | Poor |
| Security | 85.0 | Good |
| Structure | null | N/A |
| Testing Quality | null | N/A | Reason: No test files detected in the codebase.
| Code Coverage | null | N/A | Reason: No coverage reports found in the repository.
| Documentation | 80.5 | Good | 
| CI/CD | null | N/A | Reason: No CI/CD configuration files detected in the repository.
| Compliance | 50.0 | Poor |
| API Quality | null | N/A | Reason: No API endpoints or specifications detected.
| Monitoring | null | N/A | Reason: No logging or monitoring integrations detected.

## Detailed Metrics

### Complexity
| Metric | Value | Grade |
|--------|-------|-------|
| Average Cyclomatic Complexity | 0.0 | Poor |
| Max Cyclomatic Complexity | 0 | - |
| % Functions CCN > 10 | 0.0% | - |

### Duplication
| Metric | Value | Grade |
|--------|-------|-------|
| Code Duplication % | 0.0% | Poor |

### Security
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 0 |

### Structure
| Metric | Value |
|--------|-------|
| Functions with >7 Parameters | 0 |

## Recommendations

- **Maintainability**: Refactor complex functions (CCN > 10) and reduce code duplication.
- **Compliance**: Fix linting issues and adhere to coding standards.


## Configuration & Workflow Files

| File | Present |
|------|---------|
| GitHub Actions Workflow | ❌ |
| GitLab CI | ❌ |
| CircleCI | ❌ |
| package.json | ✅ |
| tsconfig.json | ❌ |
| ESLint Config | ❌ |
| Prettier Config | ❌ |
| requirements.txt | ❌ |
| setup.py | ❌ |
| pyproject.toml | ✅ |
| Pipfile | ❌ |
| poetry.lock | ❌ |
| pylint Config | ❌ |
| pytest Config | ✅ |
| .env | ❌ |
| .env.example | ❌ |
| Security Policy | ❌ |
| Dockerfile | ❌ |
| docker-compose.yml | ❌ |
| README.md | ✅ |
| LICENSE | ❌ |
| CONTRIBUTING.md | ❌ |
| jest.config.js | ❌ |
| vitest.config | ❌ |
| .gitignore | ✅ |


## Complexity & Risky Functions


### Halstead Metrics for Main Files

| File | Vocabulary | Length | Volume | Difficulty | Effort |
|------|------------|--------|--------|------------|--------|
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmp2nfqxbs1/repo_quality/cli.py | 3 | 3 | 4.75 | 0.5 | 2.38 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmp2nfqxbs1/repo_quality/cli/__main__.py | 3 | 3 | 4.75 | 0.5 | 2.38 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmp2nfqxbs1/repo_quality/report/main.py | 33 | 33 | 166.47 | 0.0 | 0.0 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmp2nfqxbs1/repo_quality/cli/main.py | 58 | 58 | 339.76 | 2.0 | 679.53 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmp2nfqxbs1/repo_quality/scoring/main.py | 43 | 43 | 233.33 | 3.5 | 816.65 |

No risky functions detected or complexity analysis failed.

## Security & Static Analysis Findings (Semgrep)

**Total Security Findings:** 1

- Critical: 0
- Error: 1
- Warning: 0
- Info: 0

| Severity | File | Line | Rule | Message |
|----------|------|------|------|---------|
| ERROR | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmp2nfqxbs1/repo_quality/analyzers/coverage.py | 50 | python.lang.security.use-defused-xml-parse.use-defused-xml-parse | The native Python `xml` library is vulnerable to XML External Entity (XXE) attacks.  These attacks can leak confidential data and "XML bombs" can cause denial of service. Do not use this library to parse untrusted input. Instead  the Python documentation recommends using `defusedxml`. |

## Custom Static Analysis Findings


### AI-Generated/Placeholder Code (94 instances)

| Type | File | Line | Snippet |
|------|------|------|---------|
| Potential Placeholder Function | repo_quality/config_detector.py | 5 | def detect_config_files(repo_path: Path) -> Dict[str, bool]: |
| Potential Placeholder Function | repo_quality/halstead.py | 7 | def compute_halstead_for_file(file_path: Path) -> Dict[str, Any]: |
| Potential Placeholder Function | repo_quality/halstead.py | 66 | def compute_main_files_halstead(repo_root: str) -> list: |
| Potential Placeholder Function | repo_quality/clone.py | 8 | def clone_repo(repo_url: str) -> Path: |
| Potential Placeholder Function | repo_quality/analyzers/lizard.py | 7 | def analyze_lizard(repo_path: Path) -> Dict[str, Any]: |
| Potential Placeholder Function | repo_quality/analyzers/documentation.py | 9 | def analyze_documentation_quality(repo_path: str) -> Dict[str, Any]: |
| Potential Placeholder Function | repo_quality/analyzers/documentation.py | 139 | def _assess_readme_quality(readme_path: Path) -> str: |
| Potential Placeholder Function | repo_quality/analyzers/documentation.py | 160 | def _count_python_comments(content: str) -> int: |
| Potential Placeholder Function | repo_quality/analyzers/documentation.py | 173 | def _count_js_comments(content: str) -> int: |
| Potential Placeholder Function | repo_quality/analyzers/documentation.py | 186 | def _analyze_python_docstrings(content: str, file_path: Path) -> Dict[str, Any]: |
| Potential Placeholder Function | repo_quality/analyzers/documentation.py | 234 | def _analyze_js_docstrings(content: str, file_path: Path) -> Dict[str, Any]: |
| Potential Placeholder Function | repo_quality/analyzers/ci_cd.py | 9 | def analyze_ci_cd_pipeline(repo_path: str) -> Dict[str, Any]: |
| Potential Placeholder Function | repo_quality/analyzers/ci_cd.py | 133 | def _analyze_yaml_ci(config: Dict[str, Any], ci_metrics: Dict[str, Any], provider: str): |
| Potential Placeholder Function | repo_quality/analyzers/ci_cd.py | 208 | def _analyze_jenkins_ci(content: str, ci_metrics: Dict[str, Any]): |
| Potential Placeholder Function | repo_quality/analyzers/compliance.py | 9 | def analyze_compliance_standards(repo_path: str) -> Dict[str, Any]: |
| Potential Placeholder Function | repo_quality/analyzers/compliance.py | 95 | def _detect_linting_tools(repo_path: Path) -> Dict[str, str]: |
| Potential Placeholder Function | repo_quality/analyzers/compliance.py | 135 | def _run_linter(tool: str, repo_path: str, config_file: str) -> Dict[str, Any]: |
| Potential Placeholder Function | repo_quality/analyzers/compliance.py | 170 | def _parse_linter_output(tool: str, output: str) -> List[str]: |
| Potential Placeholder Function | repo_quality/analyzers/compliance.py | 199 | def _check_security_standards(repo_path: Path) -> Dict[str, List[str]]: |
| Potential Placeholder Function | repo_quality/analyzers/compliance.py | 256 | def _analyze_code_quality_patterns(repo_path: Path) -> List[str]: |

*... and 74 more*

### Security Issues (22 instances)

| Type | File | Line | Snippet |
|------|------|------|---------|
| Potential Secret | repo_quality/analyzers/compliance.py | 224 | # Check for secrets in code (basic check) |
| Potential Secret | repo_quality/analyzers/compliance.py | 225 | secrets_found = [] |
| Potential Secret | repo_quality/analyzers/compliance.py | 232 | # Check for hardcoded secrets |
| Potential Secret | repo_quality/analyzers/compliance.py | 233 | secret_patterns = [ |
| Potential Secret | repo_quality/analyzers/compliance.py | 234 | r'password\s*[:=]\s*[\'"][^\'"]*[\'"]', |
| Potential Secret | repo_quality/analyzers/compliance.py | 235 | r'secret\s*[:=]\s*[\'"][^\'"]*[\'"]', |
| Potential Secret | repo_quality/analyzers/compliance.py | 236 | r'api_key\s*[:=]\s*[\'"][^\'"]*[\'"]', |
| Potential Secret | repo_quality/analyzers/compliance.py | 240 | for pattern in secret_patterns: |
| Potential Secret | repo_quality/analyzers/compliance.py | 242 | secrets_found.append(f"Potential secret in {code_file.name}") |
| Potential Secret | repo_quality/analyzers/compliance.py | 248 | if not secrets_found: |
| Potential Secret | repo_quality/analyzers/compliance.py | 249 | adhered.append('No hardcoded secrets detected') |
| Potential Secret | repo_quality/analyzers/compliance.py | 251 | violations.extend(secrets_found[:3])  # Limit to 3 examples |
| Potential Secret | repo_quality/analyzers/semgrep.py | 17 | # Custom static checks for secrets, risky patterns, and best practices |
| Potential Secret | repo_quality/analyzers/semgrep.py | 19 | # Scan all files for secrets and risky patterns |
| Potential Secret | repo_quality/analyzers/semgrep.py | 30 | # Secret patterns - more comprehensive |
| Potential Secret | repo_quality/analyzers/semgrep.py | 31 | if any(k in line_lower for k in ['password', 'secret', 'api_key', 'apikey', 'private_key', 'access_t |
| Potential Secret | repo_quality/analyzers/semgrep.py | 33 | 'type': 'Potential Secret', |
| Hardcoded Credential | repo_quality/analyzers/semgrep.py | 33 | 'type': 'Potential Secret', |
| Potential Secret | repo_quality/analyzers/semgrep.py | 40 | if any(k in line_lower for k in ['password', 'secret', 'api_key', 'token', 'apikey']): |
| Dangerous Function | repo_quality/analyzers/semgrep.py | 50 | if any(d in line for d in ['eval(', 'exec(', 'child_process', 'shell=True', 'pickle.loads', 'yaml.lo |

*... and 2 more*

### Code Quality Issues (2 instances)

| Type | File | Line | Snippet |
|------|------|------|---------|
| Missing Best Practice | repo_quality/halstead_js.js | 1 | Missing "use strict" at top of file |
| Code Quality Issue | repo_quality/analyzers/semgrep.py | 78 | if any(tag in line for tag in ['TODO:', 'FIXME:', 'HACK:', 'XXX:', 'BUG:']): |

## Dependency Analysis

### JavaScript/TypeScript Dependencies

- **Total Dependencies**: 1
- **Total Dev Dependencies**: 0
- **Dependency Usage Rate**: 100.0%


## Final Summary

This codebase has significant quality issues. Focus on improving maintainability, test coverage, and documentation.
Code Coverage: No coverage reports found in the repository.
Testing Quality: No test files detected in the codebase.
CI/CD: No CI/CD configuration files detected in the repository.
API Quality: No API endpoints or specifications detected.
Monitoring: No logging or monitoring integrations detected.