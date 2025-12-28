# Repo Quality Assessment Tool(SQM-Project)

A Python CLI tool that analyzes code repositories to generate comprehensive quality reports. Evaluates complexity, security vulnerabilities, code duplication, dependencies, and adherence to best practices.

## Installation

Clone this repository and install dependencies:

```bash
git clone <your-repo-url>
cd repo-quality
pip install -e .
```

### System Requirements

- Python 3.8 or higher
- Git (for cloning remote repositories)
- 500MB free disk space (for temporary analysis files)

### External Dependencies

The tool automatically installs these analyzers:

- **Lizard** - Cyclomatic complexity measurement
- **Semgrep** - Security vulnerability detection
- **Rich** - Terminal output formatting
- **Node.js + Esprima** - Halstead metrics for JavaScript/TypeScript files

> **Note:** Node.js and the `esprima` npm package are required for Halstead metrics on JS/TS files. The tool will use a subprocess to invoke Node.js for these files.

## Usage

### Basic Commands

Analyze a remote GitHub repository:

```bash
repo-quality https://github.com/torvalds/linux
```

Analyze your current working directory:

```bash
cd /path/to/your/project
repo-quality .
```

Analyze a specific local directory:

```bash
repo-quality /home/user/projects/myapp
```

### Command Options

**Custom output file:**

```bash
repo-quality . --output quality-report.md
```

**CI/CD integration with score threshold:**

```bash
repo-quality . --fail-under 75
# Exit code 1 if score < 75, exit code 0 otherwise
```

**Combined options:**

```bash
repo-quality https://github.com/user/repo --output report.md --fail-under 80
```

## What Gets Analyzed

### Supported File Types

- Python: `.py`
- JavaScript: `.js`, `.jsx`
- TypeScript: `.ts`, `.tsx`

### Metrics Collected

**Code Complexity:**

- Average cyclomatic complexity per function
- Maximum cyclomatic complexity found
- Percentage of functions with complexity > 10
- Count of functions with > 7 parameters
- Total lines of code (excluding comments/blanks)
- **Halstead metrics (per main file, Python & JS/TS):**
  - Vocabulary, Length, Volume, Difficulty, Effort

**Security Issues:**

- Critical vulnerabilities (e.g., SQL injection, XSS)
- High-severity warnings (e.g., hardcoded secrets)
- Medium-severity issues (e.g., weak cryptography)
- Low-severity suggestions
- Detection of dangerous functions: `eval()`, `exec()`, `innerHTML`
- Hardcoded credentials and API keys
- Insecure network protocols (HTTP instead of HTTPS)
- **Numerical summary:**
  - Total findings and counts by severity (Critical, Error, Warning, Info)
- **Limited display:**
  - Only the top 10 security findings are shown in the report for clarity

**Code Quality:**

- Duplicate code blocks
- Missing "use strict" directives in JavaScript
- AI-generated placeholder code patterns
- TODO/FIXME comments requiring attention
- **Numerical summary:**
  - Total and per-type counts for AI code, code quality issues, and secrets

**Dependencies:**

- Unused npm packages in package.json
- Unused Python packages in requirements.txt or pyproject.toml
- Percentage of declared dependencies actually imported

**Project Structure:**

- Presence of GitHub Actions workflows
- Linting configuration (ESLint, Pylint)
- Code formatting tools (Prettier, Black)
- Testing framework setup (pytest, Jest)
- Documentation files (README, CONTRIBUTING)
- Environment configuration (.env.example)
- License file

## Report Structure

The generated Markdown report contains these sections:

### 1. Executive Summary

- Overall quality score (0-100)
- Letter grade (A+ to F)
- Individual scores for maintainability, security, structure
- Quick verdict on code health

### 2. Code Metrics Table

- Tabular breakdown of all measured values with corresponding grades

### 3. Detailed Numerical Summaries

- Security findings: total and per-severity counts
- AI code, code quality, and secret issues: total and per-type counts

### 4. Halstead Metrics (per main file)

- Vocabulary, Length, Volume, Difficulty, Effort for each main Python/JS/TS file

### 5. Security Findings (Limited)

- Top 10 findings by severity, file, line, rule, and message
- If more than 10, a note on additional findings

### 6. Static Analysis Results

- Dangerous pattern detections
- Best practice violations
- Counts and affected file locations

### 7. AI Code Detection

- Placeholder function patterns
- Stub implementations
- Generated code markers

### 8. Dependency Audit

- Lists unused packages from:
  - package.json (npm)
  - requirements.txt (pip)
  - pyproject.toml (Poetry/setuptools)

### 9. Configuration Status

- Checklist showing which standard files exist:
  - ✅ Present files
  - ❌ Missing files

### 10. Top Risk Areas

- The 3 functions with highest cyclomatic complexity, including:
  - Function name and location
  - Complexity score
  - Line count

### 11. Actionable Recommendations

- Prioritized list of improvements sorted by impact

## Scoring Algorithm & Null Handling

### Overall Score Calculation

```
Overall = (0.50 × Maintainability) + (0.30 × Security) + (0.20 × Structure)
```

### Component Scores

**Maintainability (50% weight):**

```
Complexity Score = 100 - (avg_ccn × 10 + percent_complex_functions)
Duplication Score = 100 - (duplication_percentage × 2)
Maintainability = (0.60 × Complexity) + (0.40 × Duplication)
```

**Security (30% weight):**

```
Security = 100 - (critical_vulns × 20 + high_vulns × 10 + medium_vulns × 5)
Capped at 0 minimum
```

**Structure (20% weight):**

```
Parameter Penalty = functions_with_many_params × 10
Config Bonus = (present_config_files / total_expected_files) × 100
Structure = 100 - Parameter Penalty + (Config Bonus × 0.2)
```

### Grade Thresholds

- 90-100: Excellent ⭐⭐⭐⭐⭐
- 75-89: Good ⭐⭐⭐⭐
- 60-74: Fair ⭐⭐⭐
- 0-59: Poor ⭐⭐

### Null/Absent Metrics

- If a metric cannot be determined (e.g., no tests, no CI/CD, no coverage), the report will show `null` and a clear reason for its absence in the table and summary.

## Integration Examples

### Pre-commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
repo-quality . --fail-under 70
if [ $? -ne 0 ]; then
    echo "Code quality below threshold. Commit rejected."
    exit 1
fi
```

Make it executable:

```bash
chmod +x .git/hooks/pre-commit
```

### GitHub Actions Workflow

Create `.github/workflows/quality.yml`:

```yaml
name: Code Quality Check
on: [push, pull_request]
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      - name: Install repo-quality
        run: pip install repo-quality
      - name: Run analysis
        run: repo-quality . --fail-under 75 --output quality-report.md
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: quality-report
          path: quality-report.md
```

### GitLab CI/CD

Add to `.gitlab-ci.yml`:

```yaml
code_quality:
  image: python:3.10
  script:
    - pip install repo-quality
    - repo-quality . --fail-under 70 --output quality.md
  artifacts:
    paths:
      - quality.md
    expire_in: 1 week
  only:
    - merge_requests
    - main
```

## Performance Considerations

- **Small repos (<100 files):** 10-30 seconds
- **Medium repos (100-500 files):** 30-90 seconds
- **Large repos (500+ files):** 2-5 minutes
- **Very large repos (1000+ files):** May timeout; consider analyzing subdirectories

Semgrep is the slowest analyzer. For faster results on large codebases, analyze specific directories:

```bash
repo-quality ./src --output src-quality.md
```

## Troubleshooting

### "Command 'lizard' not found"

Reinstall the package:

```bash
pip uninstall lizard
pip install lizard
```

### "Semgrep timed out"

The repository is too large. Analyze a subdirectory or increase timeout in `analyzers/semgrep.py`.

### "No files analyzed"

Check that your repository contains supported file types (.py, .js, .jsx, .ts, .tsx) in the expected locations.

### Score always shows 0.0

The terminal output may show 0.0, but check the generated Markdown report for the actual score. This is a display formatting issue that doesn't affect the report.

## Development

Run tests:

```bash
pytest tests/
```

Install in editable mode:

```bash
pip install -e .
```

Add new analyzers in `repo_quality/analyzers/` and update `cli.py` to integrate them.

## Known Limitations

- Only analyzes Python, JavaScript, and TypeScript
- Semgrep requires internet connection for rule updates
- Does not analyze compiled languages (C, C++, Java, Go, Rust)
- Duplication detection may miss cross-file duplicates in large repos
- AI code detection uses pattern matching, not ML models

## License

MIT License - see LICENSE file for details.

## Contributing

Submit issues and pull requests on GitHub. Before contributing:

1. Run `repo-quality .` on your changes
2. Ensure score is above 75
3. Add tests for new analyzers
4. Update this README if adding features
   Thanks, Soumya Shekhar (SS-S3)
