# Code Quality Report

## Overall Score: 68.97624698422159 (Poor)

## Metrics Summary

| Metric | Value | Grade |
|--------|-------|-------|
| Maintainability | 69.78698311164086 | Poor |
| Security | 73.33333333333333 | Fair |
| Structure | 100.0 | Excellent |
| Testing Quality | 60.0 | Poor | 
| Code Coverage | null | N/A | Reason: No coverage reports found in the repository.
| Documentation | 60.6 | Poor | 
| CI/CD | 90.0 | Excellent | 
| Compliance | 50.0 | Poor |
| API Quality | null | N/A | Reason: No API endpoints or specifications detected.
| Monitoring | null | N/A | Reason: No logging or monitoring integrations detected.

## Detailed Metrics

### Complexity
| Metric | Value | Grade |
|--------|-------|-------|
| Average Cyclomatic Complexity | 1.47 | Excellent |
| Max Cyclomatic Complexity | 25 | - |
| % Functions CCN > 10 | 1.3% | - |

### Duplication
| Metric | Value | Grade |
|--------|-------|-------|
| Code Duplication % | N/A% | Poor |

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
- **Testing**: Enhance test suite quality and coverage.
- **Documentation**: Add comprehensive docstrings and improve README.
- **Compliance**: Fix linting issues and adhere to coding standards.


## Configuration & Workflow Files

| File | Present |
|------|---------|
| GitHub Actions Workflow | ✅ |
| GitLab CI | ❌ |
| CircleCI | ❌ |
| package.json | ✅ |
| tsconfig.json | ❌ |
| ESLint Config | ✅ |
| Prettier Config | ✅ |
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
| LICENSE | ✅ |
| CONTRIBUTING.md | ✅ |
| jest.config.js | ❌ |
| vitest.config | ✅ |
| .gitignore | ✅ |


## Complexity & Risky Functions

- **Average Cyclomatic Complexity**: 1.47
- **Max Cyclomatic Complexity**: 25
- **% Functions CCN > 10**: 1.3%

### Halstead Metrics for Main Files

| File | Vocabulary | Length | Volume | Difficulty | Effort |
|------|------------|--------|--------|------------|--------|
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/internal/server/index.js | 222 | 1718 | 13390.81 | 67.9 | 909235.76 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/compiler/phases/3-transform/css/index.js | 194 | 2566 | 19501.38 | 120.02 | 2340542.61 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/reactivity/window/index.js | None | None | None | None | None |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/compiler/phases/3-transform/index.js | 85 | 458 | 2935.5 | 36.46 | 107023.48 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/compiler/index.js | 104 | 596 | 3993.46 | 38.92 | 155433.84 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/events/index.js | 7 | 7 | 19.65 | 2 | 39.3 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/compiler/phases/2-analyze/visitors/shared/a11y/index.js | 376 | 4459 | 38144.91 | 93.18 | 3554329.17 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/benchmarking/compare/index.js | 119 | 589 | 4061.05 | 36.07 | 146471.49 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/eslint.config.js | 101 | 319 | 2123.97 | 16.43 | 34897.62 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/attachments/index.js | 36 | 140 | 723.79 | 15.6 | 11291.12 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/compiler/print/index.js | 274 | 4286 | 34708.17 | 123.88 | 4299638.76 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/svelte.config.js | 9 | 15 | 47.55 | 3 | 142.65 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/server/index.js | 7 | 7 | 19.65 | 2 | 39.3 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/compiler/migrate/index.js | 550 | 11253 | 102439.3 | 220.45 | 22583246.14 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/easing/index.js | 105 | 1147 | 7701.24 | 72.87 | 561153.79 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/benchmarking/benchmarks/ssr/index.js | 13 | 15 | 55.51 | 5.63 | 312.22 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/store/shared/index.js | 97 | 605 | 3992.95 | 58.89 | 235151.32 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/compiler/phases/1-parse/index.js | 156 | 1211 | 8822.62 | 74.39 | 656348.43 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/transition/index.js | 179 | 1421 | 10634.5 | 74.8 | 795422.79 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/internal/index.js | 6 | 6 | 15.51 | 2.5 | 38.77 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/compiler/phases/3-transform/client/transform-template/index.js | 75 | 309 | 1924.7 | 31.31 | 60255.05 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/benchmarking/benchmarks/reactivity/index.js | 50 | 168 | 948.17 | 9.63 | 9126.12 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/compiler/preprocess/index.js | 152 | 1245 | 9023.67 | 76.96 | 694503.15 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/internal/client/index.js | 279 | 757 | 6149.96 | 3.84 | 23586.11 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/internal/flags/index.js | 16 | 55 | 220 | 7.07 | 1555.71 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/motion/index.js | 18 | 27 | 112.59 | 7.86 | 884.62 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/animate/index.js | 87 | 382 | 2461.2 | 40.53 | 99743.55 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/vitest.config.js | 74 | 194 | 1204.63 | 16.01 | 19285.95 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/compiler/phases/2-analyze/index.js | 521 | 6333 | 57156.21 | 102.06 | 5833513.02 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/scripts/process-messages/index.js | 231 | 2061 | 16182.45 | 70.68 | 1143839.63 |

| Function | CCN | Params |
|----------|-----|--------|
| clean_children@8-115@/var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/tests/html_equal.js | 25 | 2 |
| clean_children@8-115@/var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/tests/html_equal.js | 25 | 2 |
| compile_directory@63-164@/var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/tests/helpers.js | 18 | 5 |

## Security & Static Analysis Findings (Semgrep)

**Total Security Findings:** 41

- Critical: 0
- Error: 1
- Warning: 7
- Info: 33

| Severity | File | Line | Rule | Message |
|----------|------|------|------|---------|
| WARNING | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/scripts/check-treeshakeability.js | 90 | javascript.lang.security.audit.unknown-value-with-script-tag.unknown-value-with-script-tag | Cannot determine what 'client_main' is and it is used with a '<script>' tag. This could be susceptible to cross-site scripting (XSS). Ensure 'client_main' is not externally controlled, or sanitize this data. |
| INFO | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/scripts/process-messages/templates/client-warnings.js | 13 | javascript.lang.security.audit.unsafe-formatstring.unsafe-formatstring | Detected string concatenation with a non-literal variable in a util.format / console.log function. If an attacker injects a format specifier in the string, it will forge the log message. Try to use constant values for the format string. |
| INFO | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/scripts/process-messages/templates/server-warnings.js | 13 | javascript.lang.security.audit.unsafe-formatstring.unsafe-formatstring | Detected string concatenation with a non-literal variable in a util.format / console.log function. If an attacker injects a format specifier in the string, it will forge the log message. Try to use constant values for the format string. |
| INFO | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/scripts/process-messages/templates/shared-warnings.js | 13 | javascript.lang.security.audit.unsafe-formatstring.unsafe-formatstring | Detected string concatenation with a non-literal variable in a util.format / console.log function. If an attacker injects a format specifier in the string, it will forge the log message. Try to use constant values for the format string. |
| WARNING | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/compiler/migrate/index.js | 361 | javascript.lang.security.audit.unknown-value-with-script-tag.unknown-value-with-script-tag | Cannot determine what 'parsed' is and it is used with a '<script>' tag. This could be susceptible to cross-site scripting (XSS). Ensure 'parsed' is not externally controlled, or sanitize this data. |
| WARNING | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/compiler/phases/1-parse/acorn.js | 123 | javascript.lang.security.audit.detect-non-literal-regexp.detect-non-literal-regexp | RegExp() called with a `source` function argument, this might allow an attacker to cause a Regular Expression Denial-of-Service (ReDoS) within your application as RegExP blocks the main thread. For this reason, it is recommended to use hardcoded regexes instead. If your regex is run on user-controlled input, consider performing input validation or use a regex checking/sanitization library such as https://www.npmjs.com/package/recheck to verify that the regex does not appear vulnerable to ReDoS. |
| WARNING | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/compiler/phases/1-parse/acorn.js | 123 | javascript.lang.security.audit.detect-non-literal-regexp.detect-non-literal-regexp | RegExp() called with a `start` function argument, this might allow an attacker to cause a Regular Expression Denial-of-Service (ReDoS) within your application as RegExP blocks the main thread. For this reason, it is recommended to use hardcoded regexes instead. If your regex is run on user-controlled input, consider performing input validation or use a regex checking/sanitization library such as https://www.npmjs.com/package/recheck to verify that the regex does not appear vulnerable to ReDoS. |
| INFO | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/internal/client/dev/debug.js | 83 | javascript.lang.security.audit.unsafe-formatstring.unsafe-formatstring | Detected string concatenation with a non-literal variable in a util.format / console.log function. If an attacker injects a format specifier in the string, it will forge the log message. Try to use constant values for the format string. |
| INFO | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/internal/client/dev/debug.js | 143 | javascript.lang.security.audit.unsafe-formatstring.unsafe-formatstring | Detected string concatenation with a non-literal variable in a util.format / console.log function. If an attacker injects a format specifier in the string, it will forge the log message. Try to use constant values for the format string. |
| INFO | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpsvmgk_hr/packages/svelte/src/internal/client/dev/debug.js | 160 | javascript.lang.security.audit.unsafe-formatstring.unsafe-formatstring | Detected string concatenation with a non-literal variable in a util.format / console.log function. If an attacker injects a format specifier in the string, it will forge the log message. Try to use constant values for the format string. |

*... and 31 more findings not shown*

## Custom Static Analysis Findings


### AI-Generated/Placeholder Code (23 instances)

| Type | File | Line | Snippet |
|------|------|------|---------|
| AI/Placeholder Code | packages/svelte/tests/runtime-runes/samples/directives-with-member-access/_config.js | 4 | // that the generated code is valid |
| AI/Placeholder Code | packages/svelte/tests/runtime-legacy/samples/binding-select-null-placeholder/_config.js | 25 | // placeholder option value must be blank string for native required field validation |
| AI/Placeholder Code | packages/svelte/tests/runtime-legacy/samples/store-auto-subscribe-event-callback/_config.js | 6 | <input class="input" placeholder="Type here" type="text"> |
| AI/Placeholder Code | packages/svelte/tests/runtime-legacy/samples/store-auto-subscribe-event-callback/_config.js | 23 | <input class="input" placeholder="Type here" type="text"> |
| AI/Placeholder Code | packages/svelte/src/internal/server/hydratable.js | 62 | // this placeholder is returned synchronously from `uneval`, which includes it in the |
| AI/Placeholder Code | packages/svelte/src/internal/server/hydratable.js | 65 | const placeholder = `"${uid++}"`; |
| AI/Placeholder Code | packages/svelte/src/internal/server/hydratable.js | 68 | entry.serialized = entry.serialized.replace(placeholder, `r(${uneval(v)})`); |
| AI/Placeholder Code | packages/svelte/src/internal/server/hydratable.js | 82 | return placeholder; |
| AI/Placeholder Code | packages/svelte/src/compiler/utils/mapped_code.js | 196 | // is equal to count of generated code lines |
| AI/Placeholder Code | packages/svelte/src/compiler/utils/mapped_code.js | 365 | 'Not implemented. ' + |
| AI/Placeholder Code | packages/svelte/src/compiler/migrate/index.js | 24 | const style_placeholder = '/*$$__STYLE_CONTENT__$$*/'; |
| AI/Placeholder Code | packages/svelte/src/compiler/migrate/index.js | 134 | return start + style_placeholder + end; |
| AI/Placeholder Code | packages/svelte/src/compiler/migrate/index.js | 161 | str.overwrite(content[0], content[0] + style_placeholder.length, content[1]); |
| AI/Placeholder Code | packages/svelte/src/compiler/phases/2-analyze/visitors/shared/a11y/constants.js | 7 | 'activedescendant atomic autocomplete busy checked colcount colindex colspan controls current descri |
| AI/Placeholder Code | packages/svelte/elements.d.ts | 601 | 'aria-placeholder'?: string | undefined | null; |
| AI/Placeholder Code | packages/svelte/elements.d.ts | 776 | placeholder?: string | undefined | null; |
| AI/Placeholder Code | packages/svelte/elements.d.ts | 1126 | placeholder?: string | undefined | null; |
| AI/Placeholder Code | packages/svelte/elements.d.ts | 1417 | placeholder?: string | undefined | null; |
| AI/Placeholder Code | packages/svelte/types/index.d.ts | 964 | /** The generated code */ |
| AI/Placeholder Code | packages/svelte/types/index.d.ts | 971 | /** The generated code */ |

*... and 3 more*

### Security Issues (51 instances)

| Type | File | Line | Snippet |
|------|------|------|---------|
| Dangerous Function | playgrounds/sandbox/scripts/create-test.js | 86 | while ((match = import_regex.exec(content)) !== null) { |
| Dangerous Function | packages/svelte/tests/helpers.js | 219 | const match = last_line && /(at .+) /.exec(last_line); |
| SQL Injection Risk | packages/svelte/tests/validator/samples/class-state-constructor-3/input.svelte.js | 5 | this.count = $state.raw(0); |
| Hardcoded Credential | packages/svelte/tests/compiler-errors/samples/style-unclosed-eof/_config.js | 5 | code: 'expected_token', |
| Hardcoded Credential | packages/svelte/tests/compiler-errors/samples/style-unclosed-eof/_config.js | 6 | message: 'Expected token </style', |
| SQL Injection Risk | packages/svelte/tests/compiler-errors/samples/runes-wrong-state-raw-args/main.svelte.js | 1 | const foo = $state.raw(1, 2, 3); |
| Hardcoded Credential | packages/svelte/tests/compiler-errors/samples/else-if-before-closing/_config.js | 5 | code: 'expected_token', |
| Hardcoded Credential | packages/svelte/tests/compiler-errors/samples/else-if-before-closing/_config.js | 6 | message: 'Expected token {:then ...} or {:catch ...}', |
| Hardcoded Credential | packages/svelte/tests/compiler-errors/samples/else-before-closing-2/_config.js | 5 | code: 'expected_token', |
| Hardcoded Credential | packages/svelte/tests/compiler-errors/samples/else-before-closing-2/_config.js | 6 | message: 'Expected token {:then ...} or {:catch ...}', |
| Hardcoded Credential | packages/svelte/tests/compiler-errors/samples/malformed-snippet-2/_config.js | 5 | code: 'expected_token', |
| Hardcoded Credential | packages/svelte/tests/compiler-errors/samples/malformed-snippet-2/_config.js | 6 | message: 'Expected token )', |
| Hardcoded Credential | packages/svelte/tests/compiler-errors/samples/comment-unclosed/_config.js | 5 | code: 'expected_token', |
| Hardcoded Credential | packages/svelte/tests/compiler-errors/samples/comment-unclosed/_config.js | 6 | message: 'Expected token -->', |
| Hardcoded Credential | packages/svelte/tests/compiler-errors/samples/else-if-without-if/_config.js | 5 | code: 'expected_token', |
| Hardcoded Credential | packages/svelte/tests/compiler-errors/samples/else-if-without-if/_config.js | 6 | message: 'Expected token {:then ...} or {:catch ...}', |
| Hardcoded Credential | packages/svelte/tests/compiler-errors/samples/malformed-snippet/_config.js | 5 | code: 'expected_token', |
| Hardcoded Credential | packages/svelte/tests/compiler-errors/samples/malformed-snippet/_config.js | 6 | message: 'Expected token }', |
| Hardcoded Credential | packages/svelte/tests/compiler-errors/samples/unclosed-attribute-self-close-tag/_config.js | 5 | code: 'expected_token', |
| Hardcoded Credential | packages/svelte/tests/compiler-errors/samples/unclosed-attribute-self-close-tag/_config.js | 6 | message: 'Expected token }', |

*... and 31 more*

### Code Quality Issues (3193 instances)

| Type | File | Line | Snippet |
|------|------|------|---------|
| Missing Best Practice | svelte.config.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | vitest.config.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | eslint.config.js | 1 | Missing "use strict" at top of file |
| Code Quality Issue | eslint.config.js | 61 | // TODO: enable these rules and run `pnpm lint:fix` |
| Missing Best Practice | playgrounds/sandbox/ssr-prod.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | playgrounds/sandbox/svelte.config.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | playgrounds/sandbox/run.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | playgrounds/sandbox/ssr-dev.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | playgrounds/sandbox/vite.config.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | playgrounds/sandbox/ssr-common.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | playgrounds/sandbox/scripts/download.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | playgrounds/sandbox/scripts/create-test.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | playgrounds/sandbox/scripts/create-app-svelte.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | playgrounds/sandbox/scripts/hash.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | packages/svelte/rollup.config.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | packages/svelte/tests/animation-helpers.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | packages/svelte/tests/html_equal.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | packages/svelte/tests/helpers.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | packages/svelte/tests/snapshot/samples/async-each-hoisting/_config.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | packages/svelte/tests/snapshot/samples/async-each-hoisting/_expected/server/index.svelte.js | 1 | Missing "use strict" at top of file |

*... and 3173 more*

## Dependency Analysis

### JavaScript/TypeScript Dependencies

- **Total Dependencies**: 0
- **Total Dev Dependencies**: 18
- **Dependency Usage Rate**: 100.0%


**Unused Dev Dependencies (11)**:
- @changesets/cli
- @svitejs/changesets-changelog-github-compact
- @types/node
- @types/picomatch
- @vitest/coverage-v8
- eslint-plugin-svelte
- jsdom
- playwright
- prettier
- prettier-plugin-svelte

*... and 1 more*


## Final Summary

This codebase is generally solid but has some areas for improvement, especially in testing, documentation, or CI/CD.
Code Coverage: No coverage reports found in the repository.
API Quality: No API endpoints or specifications detected.
Monitoring: No logging or monitoring integrations detected.