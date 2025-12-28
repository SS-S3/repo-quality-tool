# Code Quality Report

## Overall Score: 31.191515151515148 (Poor)

## Metrics Summary

| Metric | Value | Grade |
|--------|-------|-------|
| Maintainability | 91.54545454545453 | Excellent |
| Security | 85.0 | Good |
| Structure | 76.66666666666666 | Fair |
| Testing Quality | null | N/A | Reason: No test files detected in the codebase.
| Code Coverage | null | N/A | Reason: No coverage reports found in the repository.
| Documentation | 45.4 | Poor | 
| CI/CD | null | N/A | Reason: No CI/CD configuration files detected in the repository.
| Compliance | 50.0 | Poor |
| API Quality | null | N/A | Reason: No API endpoints or specifications detected.
| Monitoring | null | N/A | Reason: No logging or monitoring integrations detected.

## Detailed Metrics

### Complexity
| Metric | Value | Grade |
|--------|-------|-------|
| Average Cyclomatic Complexity | 2.8 | Good |
| Max Cyclomatic Complexity | 5 | - |
| % Functions CCN > 10 | 0.0% | - |

### Duplication
| Metric | Value | Grade |
|--------|-------|-------|
| Code Duplication % | 0.0% | Excellent |

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
| pyproject.toml | ❌ |
| Pipfile | ❌ |
| poetry.lock | ❌ |
| pylint Config | ❌ |
| pytest Config | ❌ |
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
- **Documentation**: Add comprehensive docstrings and improve README.
- **Compliance**: Fix linting issues and adhere to coding standards.

## Complexity & Risky Functions

- **Average Cyclomatic Complexity**: 2.8181818181818183
- **Max Cyclomatic Complexity**: 5
- **% Functions CCN > 10**: 0.0%

### Halstead Metrics for Main Files

| File | Vocabulary | Length | Volume | Difficulty | Effort |
|------|------------|--------|--------|------------|--------|
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpxgg3xmqv/server/app.py | 51 | 51 | 289.29 | 3.0 | 867.88 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpxgg3xmqv/client/src/index.js | None | None | None | None | None |

| Function | CCN | Params |
|----------|-----|--------|
| translate_text@66-85@/var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpxgg3xmqv/server/app.py | 5 | 3 |
| translate_text@18-33@/var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpxgg3xmqv/server/translator.py | 5 | 3 |
| health@89-99@/var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpxgg3xmqv/server/app.py | 4 | 0 |

## Final Summary

This codebase is in poor health. Major improvements are needed in maintainability, security, testing, and documentation.
Code Coverage: No coverage reports found in the repository.
Testing Quality: No test files detected in the codebase.
CI/CD: No CI/CD configuration files detected in the repository.
API Quality: No API endpoints or specifications detected.
Monitoring: No logging or monitoring integrations detected.
## Security & Static Analysis Findings (Semgrep)

**Total Security Findings:** 2

- Critical: 0
- Error: 0
- Warning: 2
- Info: 0

| Severity | File | Line | Rule | Message |
|----------|------|------|------|---------|
| WARNING | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpxgg3xmqv/server/app.py | 138 | python.flask.security.audit.app-run-param-config.avoid_app_run_with_bad_host | Running flask app with host 0.0.0.0 could expose the server publicly. |
| WARNING | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpxgg3xmqv/server/translator.py | 78 | python.flask.security.audit.app-run-param-config.avoid_app_run_with_bad_host | Running flask app with host 0.0.0.0 could expose the server publicly. |

## Custom Static Analysis Findings


### AI-Generated/Placeholder Code (17 instances)

| Type | File | Line | Snippet |
|------|------|------|---------|
| AI/Placeholder Code | client/src/components/TranslationPanel.jsx | 87 | placeholder={sourceLanguage === 'en' ? 'Enter English text...' : 'Ingrese texto en español...'} |
| AI/Placeholder Code | client/src/components/TranslationPanel.jsx | 257 | // //             placeholder="Enter Gemini API Key" |
| AI/Placeholder Code | client/src/components/TranslationPanel.jsx | 297 | // //                 placeholder={sourceLanguage === 'english' ? 'Enter English text...' : 'Ingrese |
| AI/Placeholder Code | client/src/components/TranslationPanel.jsx | 518 | // //             placeholder="Enter Gemini API Key" |
| AI/Placeholder Code | client/src/components/TranslationPanel.jsx | 564 | // //                 placeholder={sourceLanguage === 'english' ? 'Enter English text...' : 'Ingrese |
| AI/Placeholder Code | client/src/components/TranslationPanel.jsx | 761 | //                         placeholder={sourceLanguage === 'english' ? 'Enter English text...' : 'In |
| Potential Placeholder Function | server/app.py | 41 | def get_model(direction): |
| Potential Placeholder Function | server/app.py | 66 | def translate_text(text, source_lang, target_lang): |
| Potential Placeholder Function | server/app.py | 89 | def health(): |
| Potential Placeholder Function | server/app.py | 103 | def translate(): |
| Potential Placeholder Function | server/app.py | 130 | def serve(path): |
| Potential Placeholder Function | server/translator.py | 18 | def translate_text(text, source_lang, target_lang): |
| Potential Placeholder Function | server/translator.py | 36 | def home(): |
| Potential Placeholder Function | server/translator.py | 48 | def health(): |
| Potential Placeholder Function | server/translator.py | 52 | def api_health(): |
| Potential Placeholder Function | server/translator.py | 56 | def translate_legacy(): |
| Potential Placeholder Function | server/translator.py | 61 | def translate(): |

### Security Issues (42 instances)

| Type | File | Line | Snippet |
|------|------|------|---------|
| Potential Secret | client/src/components/TranslationPanel.jsx | 127 | // //   const [apiKey, setApiKey] = useState(''); |
| Potential Secret | client/src/components/TranslationPanel.jsx | 128 | // //   const [savedApiKey, setSavedApiKey] = useState(''); |
| Potential Secret | client/src/components/TranslationPanel.jsx | 136 | // //     const storedApiKey = localStorage.getItem('geminiApiKey'); |
| Potential Secret | client/src/components/TranslationPanel.jsx | 137 | // //     if (storedApiKey) { |
| Potential Secret | client/src/components/TranslationPanel.jsx | 138 | // //       setApiKey(storedApiKey); |
| Potential Secret | client/src/components/TranslationPanel.jsx | 139 | // //       setSavedApiKey(storedApiKey); |
| Potential Secret | client/src/components/TranslationPanel.jsx | 140 | // //       verifyApiKey(storedApiKey); |
| Potential Secret | client/src/components/TranslationPanel.jsx | 146 | // //   const verifyApiKey = async (key) => { |
| Potential Secret | client/src/components/TranslationPanel.jsx | 154 | // //         body: JSON.stringify({ apiKey: key }), |
| Potential Secret | client/src/components/TranslationPanel.jsx | 162 | // //         localStorage.setItem('geminiApiKey', key); |
| Potential Secret | client/src/components/TranslationPanel.jsx | 163 | // //         setSavedApiKey(key); |
| Potential Secret | client/src/components/TranslationPanel.jsx | 177 | // //   const saveApiKey = () => { |
| Potential Secret | client/src/components/TranslationPanel.jsx | 178 | // //     if (apiKey.trim() === '') { |
| Potential Secret | client/src/components/TranslationPanel.jsx | 182 | // //     verifyApiKey(apiKey); |
| Potential Secret | client/src/components/TranslationPanel.jsx | 210 | // //           apiKey: savedApiKey, |
| Potential Secret | client/src/components/TranslationPanel.jsx | 254 | // //             type="password" |
| Hardcoded Credential | client/src/components/TranslationPanel.jsx | 254 | // //             type="password" |
| Potential Secret | client/src/components/TranslationPanel.jsx | 255 | // //             value={apiKey} |
| Potential Secret | client/src/components/TranslationPanel.jsx | 256 | // //             onChange={(e) => setApiKey(e.target.value)} |
| Potential Secret | client/src/components/TranslationPanel.jsx | 259 | // //           <button onClick={saveApiKey} disabled={isLoading}> |

*... and 22 more*

### Code Quality Issues (2 instances)

| Type | File | Line | Snippet |
|------|------|------|---------|
| Missing Best Practice | client/src/reportWebVitals.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | client/src/index.js | 1 | Missing "use strict" at top of file |

## Dependency Analysis

### JavaScript/TypeScript Dependencies

- **Total Dependencies**: 0
- **Total Dev Dependencies**: 2
- **Dependency Usage Rate**: 100.0%


**Unused Dev Dependencies (2)**:
- concurrently
- gh-pages
