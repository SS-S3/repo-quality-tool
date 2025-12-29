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

### Quick Start

The tool can be invoked either as a command-line utility or as a Python module:

```bash
# Using installed command
repo-quality <repository-path> [OPTIONS]

# Using Python module
python -m repo_quality.cli <repository-path> [OPTIONS]
```

### Basic Commands

Analyze a remote GitHub repository:

```bash
repo-quality https://github.com/torvalds/linux
# Clones the repo to a temp directory, analyzes it, and generates a report
```

Analyze your current working directory:

```bash
cd /path/to/your/project
repo-quality .
# Analyzes the current directory without cloning
```

Analyze a specific local directory:

```bash
repo-quality /home/user/projects/myapp
repo-quality ~/projects/myapp
```

### Command-Line Options

**`--output` / `-o`** - Specify output report file

```bash
repo-quality . --output quality-report.md
# Default: Prints to stdout if not specified
```

**`--fail-under`** - Set minimum score threshold for CI/CD

```bash
repo-quality . --fail-under 75
# Returns exit code 0 if score >= 75
# Returns exit code 1 if score < 75
# Useful for enforcing quality gates
```

**Combined usage:**

```bash
repo-quality https://github.com/user/repo --output report.md --fail-under 80
```

### Practical Examples

**Analyzing multiple repositories:**

```bash
# Analyze different projects and compare
repo-quality https://github.com/{{your-repo}} --output repo1-report.md
repo-quality https://github.com/{{your-other-repo}} --output repo2-report.md
```

**Local development workflow:**

```bash
# Check quality while developing
cd ~/my-project
repo-quality . --output latest-report.md
# Review the report to identify areas for improvement
```

**Enforce quality in scripts:**

```bash
#!/bin/bash
repo-quality . --output quality-report.md --fail-under 75
if [ $? -eq 0 ]; then
    echo "✅ Quality threshold passed!"
else
    echo "❌ Quality threshold failed. Check quality-report.md"
    exit 1
fi
```

**Continuous monitoring:**

```bash
# Generate report and check specific areas
repo-quality https://github.com/user/myrepo --output report.md
grep -A 20 "Security" report.md  # View security section
grep "Critical\|High" report.md   # Find critical issues
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

### 2. Metrics Summary Table

A quick reference table showing:

- Maintainability score with grade
- Security score with grade
- Structure score with grade
- Testing Quality (if available)
- Code Coverage (if available)
- Documentation (if available)
- CI/CD (if available)
- Compliance score with grade
- API Quality (if available)
- Monitoring (if available)

Each metric shows `null` with a reason if data is unavailable.

### 3. Detailed Metrics

Breaking down complexity, duplication, and security findings:

**Complexity metrics:**

- Average Cyclomatic Complexity: Measures function complexity (lower is better, ideal < 10)
- Max Cyclomatic Complexity: Peak complexity in the codebase
- % Functions CCN > 10: Percentage of complex functions (should be < 20%)

**Duplication metrics:**

- Code Duplication %: Percentage of duplicated code blocks (should be < 5%)

**Security findings:**

- Critical vulnerabilities (requires immediate attention)
- High-severity issues (address in next sprint)
- Medium-severity issues (plan for future)
- Low-severity suggestions (nice to have)

### 4. Configuration & Workflow Files

Checklist showing presence of standard files:

- ✅ = File exists and proper configuration detected
- ❌ = File missing or not properly configured

Files checked:

- `.github/workflows/` (GitHub Actions)
- `.gitignore`
- `eslintrc.js` or similar (Linting config)
- `prettier.config.js` or `.prettierrc` (Code formatting)
- `pytest.ini` or `setup.cfg` (Testing)
- `README.md` (Documentation)
- `CONTRIBUTING.md` (Contribution guidelines)
- `.env.example` (Environment configuration)

### 5. Complexity & Risky Functions

Detailed analysis of code complexity:

**Halstead Metrics (for main files):**

- **Vocabulary**: Count of unique operators and operands
- **Length**: Total count of operators and operands
- **Volume**: Program length weighted by vocabulary
- **Difficulty**: Difficulty to understand/write the program
- **Effort**: Time required to understand the program (in basic CPU operations)

**Risky Functions:**
Table of the 3 most complex functions with:

- Function name and file location
- Cyclomatic Complexity (CCN) score
- Number of parameters

### 6. Security Findings (Limited Display)

Top 10 security vulnerabilities from Semgrep analysis:

- File location and line number
- Rule ID and category
- Severity level
- Description of the issue

> Note: Only top 10 are shown for brevity. More findings may exist in the full Semgrep output.

### 7. Dependency Analysis

Lists unused and suspicious dependencies:

- **npm packages** from `package.json`
- **Python packages** from `requirements.txt` or `pyproject.toml`
- Percentage of declared dependencies actually used in code

### 8. Quality Issues

Detected code quality problems:

- TODO/FIXME comments requiring attention
- AI-generated code patterns
- Dangerous functions: `eval()`, `exec()`, `innerHTML`
- Insecure patterns: hardcoded credentials, HTTP URLs

### 9. Actionable Recommendations

Prioritized list of improvements based on current scores:

- Organized by category (Maintainability, Security, Structure, etc.)
- Only shows recommendations for areas scoring below 70
- Actionable steps to improve each area

### 10. Final Summary

Executive overview of findings with:

- Null metrics and reasons for unavailability
- Next steps for improvement
- Areas of strength
- Critical focus areas

## Scoring Algorithm & Null Handling

### Understanding Your Score

**Overall Score Calculation:**

The overall score is a weighted combination of three main dimensions:

```
Overall = (0.50 × Maintainability) + (0.30 × Security) + (0.20 × Structure)
```

This weighting emphasizes that **maintainability is most important** (50%), followed by security (30%), then code structure (20%).

### Component Scores in Detail

**Maintainability (50% weight):**

Measures code complexity and duplication.

```
Complexity Score = 100 - (avg_ccn × 10 + percent_complex_functions)
Duplication Score = 100 - (duplication_percentage × 2)
Maintainability = (0.60 × Complexity) + (0.40 × Duplication)
```

- Affects: How easy is it to understand and modify the code?
- Key metrics: Cyclomatic Complexity (CCN), code duplication
- **Target:** Keep avg CCN < 10, duplication < 5%

**Security (30% weight):**

Measures detected vulnerabilities and dangerous patterns.

```
Security = 100 - (critical × 20 + high × 10 + medium × 5)
Capped at 0 minimum
```

- Affects: How vulnerable is the code to attacks?
- Key metrics: Semgrep findings by severity
- **Target:** Zero critical/high vulnerabilities

**Structure (20% weight):**

Measures code organization and adherence to best practices.

```
Parameter Penalty = functions_with_many_params × 10
Config Bonus = (present_config_files / total_expected_files) × 100
Structure = 100 - Parameter Penalty + (Config Bonus × 0.2)
```

- Affects: Is the code well-organized and following conventions?
- Key metrics: Functions with >7 parameters, presence of config files
- **Target:** <5% functions with >7 parameters, >70% config files present

### Grade Thresholds

| Score  | Grade          | Meaning                                             |
| ------ | -------------- | --------------------------------------------------- |
| 90-100 | A+ (Excellent) | ⭐⭐⭐⭐⭐ Production-ready, best practices         |
| 80-89  | A (Very Good)  | ⭐⭐⭐⭐ Well-maintained, minor improvements needed |
| 70-79  | B (Good)       | ⭐⭐⭐ Acceptable, address key issues               |
| 60-69  | C (Fair)       | ⭐⭐ Significant improvements needed                |
| 50-59  | D (Poor)       | ⭐ Major refactoring required                       |
| <50    | F (Critical)   | 🚨 Immediate attention required                     |

### Understanding Null Metrics

Some metrics may show as `null` instead of a number. This is **expected and correct** - it means:

**When does a metric become `null`?**

1. **No test files found** → Testing Quality = `null`

   - Reason: "No tests detected"

2. **No coverage reports** → Code Coverage = `null`

   - Reason: "No coverage configuration or reports found"

3. **Lizard analysis fails** → Complexity metrics = `null`

   - Reason: "Lizard failed to analyze code files"

4. **No documentation** → Documentation = `null`

   - Reason: "Insufficient documentation files"

5. **No CI/CD configured** → CI/CD = `null`

   - Reason: "No CI/CD workflows detected"

6. **API code not detected** → API Quality = `null`

   - Reason: "No API endpoints detected"

7. **No monitoring setup** → Monitoring = `null`
   - Reason: "No monitoring/observability setup"

**Why use `null` instead of 0?**

- **`0` means:** "This aspect was evaluated and scored zero" (bad)
- **`null` means:** "This aspect doesn't apply to this project" (not applicable)

This distinction helps you understand whether a low score is a real problem (0) or simply not relevant (null).

### Interpreting Specific Metrics

**Cyclomatic Complexity (CCN):**

- **< 5:** Simple, easy to understand
- **5-10:** Moderate, acceptable
- **10-20:** Complex, difficult to test
- **> 20:** Very complex, high maintenance cost

**Code Duplication:**

- **< 5%:** Excellent, minimal duplication
- **5-10%:** Good, some duplication
- **10-20%:** Fair, refactor to reduce
- **> 20%:** Poor, significant duplication

**Security Findings by Severity:**

- **Critical:** Security breaches, data loss risks → Fix immediately
- **High:** Potential for significant damage → Fix in current sprint
- **Medium:** Could be exploited, but barriers exist → Fix soon
- **Low:** Best practice violations → Plan for future

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
