# Code Quality Report

## Overall Score: 27.04583333333333 (Poor)

## Metrics Summary

| Metric | Value | Grade |
|--------|-------|-------|
| Maintainability | 91.7 | Excellent |
| Security | 70.0 | Fair |
| Structure | 76.66666666666666 | Fair |
| Testing Quality | null | N/A | Reason: No test files detected in the codebase.
| Code Coverage | null | N/A | Reason: No coverage reports found in the repository.
| Documentation | 25.0 | Poor | 
| CI/CD | null | N/A | Reason: No CI/CD configuration files detected in the repository.
| Compliance | 40.0 | Poor |
| API Quality | null | N/A | Reason: No API endpoints or specifications detected.
| Monitoring | null | N/A | Reason: No logging or monitoring integrations detected.

## Detailed Metrics

### Complexity
| Metric | Value | Grade |
|--------|-------|-------|
| Average Cyclomatic Complexity | 2.8 | Good |
| Max Cyclomatic Complexity | 8 | - |
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
| package.json | ❌ |
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

- **Average Cyclomatic Complexity**: 2.7666666666666666
- **Max Cyclomatic Complexity**: 8
- **% Functions CCN > 10**: 0.0%

### Halstead Metrics for Main Files

| File | Vocabulary | Length | Volume | Difficulty | Effort |
|------|------------|--------|--------|------------|--------|
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpt5850h_i/server/server.js | 78 | 288 | 1810.2 | 18.03 | 32644.89 |

| Function | CCN | Params |
|----------|-----|--------|
| clerkWebhooks@5-59@/var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpt5850h_i/server/controllers/clerkWebhooks.js | 8 | 0 |
| handleUserCreated@62-90@/var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpt5850h_i/server/controllers/clerkWebhooks.js | 7 | 0 |
| handleUserUpdated@93-116@/var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpt5850h_i/server/controllers/clerkWebhooks.js | 7 | 0 |

## Final Summary

This codebase is in poor health. Major improvements are needed in maintainability, security, testing, and documentation.
Code Coverage: No coverage reports found in the repository.
Testing Quality: No test files detected in the codebase.
CI/CD: No CI/CD configuration files detected in the repository.
API Quality: No API endpoints or specifications detected.
Monitoring: No logging or monitoring integrations detected.
## Security & Static Analysis Findings (Semgrep)

**Total Security Findings:** 180

- Critical: 0
- Error: 1
- Warning: 178
- Info: 1

| Severity | File | Line | Rule | Message |
|----------|------|------|------|---------|
| WARNING | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpt5850h_i/report/assets/scripts/bundles/codemirror.js | 2 | javascript.lang.security.audit.detect-non-literal-regexp.detect-non-literal-regexp | RegExp() called with a `c` function argument, this might allow an attacker to cause a Regular Expression Denial-of-Service (ReDoS) within your application as RegExP blocks the main thread. For this reason, it is recommended to use hardcoded regexes instead. If your regex is run on user-controlled input, consider performing input validation or use a regex checking/sanitization library such as https://www.npmjs.com/package/recheck to verify that the regex does not appear vulnerable to ReDoS. |
| WARNING | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpt5850h_i/report/assets/scripts/bundles/codemirror.js | 2 | javascript.lang.security.audit.detect-non-literal-regexp.detect-non-literal-regexp | RegExp() called with a `c` function argument, this might allow an attacker to cause a Regular Expression Denial-of-Service (ReDoS) within your application as RegExP blocks the main thread. For this reason, it is recommended to use hardcoded regexes instead. If your regex is run on user-controlled input, consider performing input validation or use a regex checking/sanitization library such as https://www.npmjs.com/package/recheck to verify that the regex does not appear vulnerable to ReDoS. |
| WARNING | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpt5850h_i/report/assets/scripts/bundles/codemirror.js | 3 | javascript.lang.security.audit.detect-non-literal-regexp.detect-non-literal-regexp | RegExp() called with a `b` function argument, this might allow an attacker to cause a Regular Expression Denial-of-Service (ReDoS) within your application as RegExP blocks the main thread. For this reason, it is recommended to use hardcoded regexes instead. If your regex is run on user-controlled input, consider performing input validation or use a regex checking/sanitization library such as https://www.npmjs.com/package/recheck to verify that the regex does not appear vulnerable to ReDoS. |
| WARNING | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpt5850h_i/report/assets/scripts/codemirror.markpopovertext.js | 18 | javascript.lang.security.audit.detect-non-literal-regexp.detect-non-literal-regexp | RegExp() called with a `regex` function argument, this might allow an attacker to cause a Regular Expression Denial-of-Service (ReDoS) within your application as RegExP blocks the main thread. For this reason, it is recommended to use hardcoded regexes instead. If your regex is run on user-controlled input, consider performing input validation or use a regex checking/sanitization library such as https://www.npmjs.com/package/recheck to verify that the regex does not appear vulnerable to ReDoS. |
| ERROR | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpt5850h_i/report/assets/scripts/plato-file.js | 146 | javascript.browser.security.insecure-document-method.insecure-document-method | User controlled data in methods like `innerHTML`, `outerHTML` or `document.write` is an anti-pattern that can lead to XSS vulnerabilities |
| WARNING | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpt5850h_i/report/display.html | 11 | html.security.audit.missing-integrity.missing-integrity | This tag is missing an 'integrity' subresource integrity attribute. The 'integrity' attribute allows for the browser to verify that externally hosted files (for example from a CDN) are delivered without unexpected manipulation. Without this attribute, if an attacker can modify the externally hosted resource, this could lead to XSS and other types of attacks. To prevent this, include the base64-encoded cryptographic hash of the resource (file) you’re telling the browser to fetch in the 'integrity' attribute for all externally hosted files. |
| WARNING | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpt5850h_i/report/files/C__Users_Hp_Desktop_PROJECTS_Hotel_Booking_client_eslint_config_js/index.html | 12 | html.security.audit.missing-integrity.missing-integrity | This tag is missing an 'integrity' subresource integrity attribute. The 'integrity' attribute allows for the browser to verify that externally hosted files (for example from a CDN) are delivered without unexpected manipulation. Without this attribute, if an attacker can modify the externally hosted resource, this could lead to XSS and other types of attacks. To prevent this, include the base64-encoded cryptographic hash of the resource (file) you’re telling the browser to fetch in the 'integrity' attribute for all externally hosted files. |
| WARNING | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpt5850h_i/report/files/C__Users_Hp_Desktop_PROJECTS_Hotel_Booking_client_eslint_config_js/index.html | 28 | html.security.plaintext-http-link.plaintext-http-link | This link points to a plaintext HTTP URL. Prefer an encrypted HTTPS URL if possible. |
| WARNING | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpt5850h_i/report/files/C__Users_Hp_Desktop_PROJECTS_Hotel_Booking_client_eslint_config_js/index.html | 46 | html.security.plaintext-http-link.plaintext-http-link | This link points to a plaintext HTTP URL. Prefer an encrypted HTTPS URL if possible. |
| WARNING | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpt5850h_i/report/files/C__Users_Hp_Desktop_PROJECTS_Hotel_Booking_client_eslint_config_js/index.html | 64 | html.security.plaintext-http-link.plaintext-http-link | This link points to a plaintext HTTP URL. Prefer an encrypted HTTPS URL if possible. |

*... and 170 more findings not shown*

## Custom Static Analysis Findings


### AI-Generated/Placeholder Code (5 instances)

| Type | File | Line | Snippet |
|------|------|------|---------|
| AI/Placeholder Code | report/assets/scripts/vendor/morris.min.js | 1 | (function(){var e,t,n,r,i=[].slice,s={}.hasOwnProperty,o=function(e,t){function r(){this.constructor |
| AI/Placeholder Code | report/assets/scripts/bundles/core-bundle.js | 8 | return m},d.prototype.drawSeries=function(){var a,b,c,d,e,f,g,h,i,j,k,l,m,n;return c=this.width/this |
| AI/Placeholder Code | client/src/components/HotelSearchForm.jsx | 90 | placeholder="Where do you want to go?" |
| AI/Placeholder Code | client/src/components/HotelSearchForm.jsx | 157 | placeholder="1" |
| AI/Placeholder Code | client/src/pages/Booking.jsx | 238 | placeholder="Any special requests or preferences..." |

### Security Issues (33 instances)

| Type | File | Line | Snippet |
|------|------|------|---------|
| SQL Injection Risk | server/server.js | 26 | express.raw({ type: 'application/json' }), |
| Potential Secret | server/controllers/clerkWebhooks.js | 7 | // Get webhook secret from environment |
| Potential Secret | server/controllers/clerkWebhooks.js | 8 | const webhookSecret = process.env.CLERK_WEBHOOK_SECRET; |
| Potential Secret | server/controllers/clerkWebhooks.js | 10 | if (!webhookSecret) { |
| Potential Secret | server/controllers/clerkWebhooks.js | 11 | console.error('CLERK_WEBHOOK_SECRET not found in environment variables'); |
| Potential Secret | server/controllers/clerkWebhooks.js | 12 | return res.status(500).json({ error: 'Webhook secret not configured' }); |
| Hardcoded Credential | server/controllers/clerkWebhooks.js | 12 | return res.status(500).json({ error: 'Webhook secret not configured' }); |
| Potential Secret | server/controllers/clerkWebhooks.js | 24 | const wh = new Webhook(webhookSecret); |
| Potential Secret | report/assets/scripts/vendor/jquery-1.8.3.min.js | 2 | (function(e,t){function _(e){var t=M[e]={};return v.each(e.split(y),function(e,n){t[n]=!0}),t}functi |
| Hardcoded Credential | report/assets/scripts/vendor/jquery-1.8.3.min.js | 2 | (function(e,t){function _(e){var t=M[e]={};return v.each(e.split(y),function(e,n){t[n]=!0}),t}functi |
| Dangerous Function | report/assets/scripts/vendor/jquery-1.8.3.min.js | 2 | (function(e,t){function _(e){var t=M[e]={};return v.each(e.split(y),function(e,n){t[n]=!0}),t}functi |
| Dangerous Function | report/assets/scripts/vendor/lodash.min.js | 11 | }function Q(n,t){this.__chain__=!!t,this.__wrapped__=n}function X(n){function t(){if(r){var n=p(r);b |
| Dangerous Function | report/assets/scripts/vendor/codemirror/codemirror.js | 3618 | var m = tokenSpecialChars.exec(text); |
| Hardcoded Credential | report/assets/scripts/vendor/codemirror/codemirror.js | 3721 | spanStartStyle, pos + tokenText.length == nextChange ? spanEndStyle : ""); |
| Dangerous Function | report/assets/scripts/vendor/codemirror/util/continuelist.js | 10 | var matches = reg.exec(full); |
| Hardcoded Credential | report/assets/scripts/vendor/codemirror/util/pig-hint.js | 25 | token = tprop = {start: cur.ch, end: cur.ch, string: "", state: token.state, |
| Dangerous Function | report/assets/scripts/vendor/codemirror/util/xml-hint.js | 70 | while ((match = regex.exec(text)) != null) { |
| Dangerous Function | report/assets/scripts/vendor/codemirror/util/searchcursor.js | 18 | var line = cm.getLine(pos.line).slice(0, pos.ch), match = query.exec(line), start = 0; |
| Dangerous Function | report/assets/scripts/vendor/codemirror/util/searchcursor.js | 23 | var newmatch = query.exec(line); |
| Dangerous Function | report/assets/scripts/vendor/codemirror/util/searchcursor.js | 30 | var line = cm.getLine(pos.line), match = query.exec(line), |

*... and 13 more*

### Code Quality Issues (113 instances)

| Type | File | Line | Snippet |
|------|------|------|---------|
| Missing Best Practice | server/server.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | server/middleware/authMiddleware.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | server/utils/emailSender.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | server/models/Booking.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | server/models/listing.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | server/models/user.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | server/configs/db.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | server/controllers/bookingController.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | server/controllers/listingController.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | server/controllers/userController.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | server/controllers/clerkWebhooks.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | server/routes/listingRoutes.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | server/routes/bookingRoutes.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | server/routes/userRoutes.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | report/report.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | report/report.history.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | report/files/C__Users_Hp_Desktop_PROJECTS_Hotel_Booking_report_files_C__Users_Hp_Desktop_PROJECTS_Hotel_Booking_client_src_assets_assets_js_report_history_js/report.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | report/files/C__Users_Hp_Desktop_PROJECTS_Hotel_Booking_report_files_C__Users_Hp_Desktop_PROJECTS_Hotel_Booking_client_src_assets_assets_js_report_history_js/report.history.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | report/files/C__Users_Hp_Desktop_PROJECTS_Hotel_Booking_report_files_C__Users_Hp_Desktop_PROJECTS_Hotel_Booking_client_src_hooks_use_outside_click_js_report_history_js/report.js | 1 | Missing "use strict" at top of file |
| Missing Best Practice | report/files/C__Users_Hp_Desktop_PROJECTS_Hotel_Booking_report_files_C__Users_Hp_Desktop_PROJECTS_Hotel_Booking_client_src_hooks_use_outside_click_js_report_history_js/report.history.js | 1 | Missing "use strict" at top of file |

*... and 93 more*
