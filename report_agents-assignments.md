# Code Quality Report

## Overall Score: 41.3448676081584 (Poor)

## Metrics Summary

| Metric | Value | Grade |
|--------|-------|-------|
| Maintainability | 67.07894086526721 | Poor |
| Security | 73.33333333333333 | Fair |
| Structure | 82.0 | Good |
| Testing Quality | 60.0 | Poor | 
| Code Coverage | null | N/A | Reason: No coverage reports found in the repository.
| Documentation | 46.6 | Poor | 
| CI/CD | 57.0 | Poor | 
| Compliance | 40.0 | Poor |
| API Quality | null | N/A | Reason: No API endpoints or specifications detected.
| Monitoring | null | N/A | Reason: No logging or monitoring integrations detected.

## Detailed Metrics

### Complexity
| Metric | Value | Grade |
|--------|-------|-------|
| Average Cyclomatic Complexity | 2.7 | Good |
| Max Cyclomatic Complexity | 33 | - |
| % Functions CCN > 10 | 3.5% | - |

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


## Configuration & Workflow Files

| File | Present |
|------|---------|
| GitHub Actions Workflow | ✅ |
| GitLab CI | ❌ |
| CircleCI | ❌ |
| package.json | ❌ |
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
| LICENSE | ✅ |
| CONTRIBUTING.md | ✅ |
| jest.config.js | ❌ |
| vitest.config | ❌ |
| .gitignore | ✅ |
- **Maintainability**: Refactor complex functions (CCN > 10) and reduce code duplication.
- **Testing**: Enhance test suite quality and coverage.
- **Documentation**: Add comprehensive docstrings and improve README.
- **CI/CD**: Implement proper CI/CD pipelines with security scanning.
- **Compliance**: Fix linting issues and adhere to coding standards.

## Complexity & Risky Functions

- **Average Cyclomatic Complexity**: 2.73
- **Max Cyclomatic Complexity**: 33
- **% Functions CCN > 10**: 3.53%

### Halstead Metrics for Main Files

| File | Vocabulary | Length | Volume | Difficulty | Effort |
|------|------------|--------|--------|------------|--------|
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpfvtufg8z/livekit-agents/livekit/agents/cli/cli.py | 325 | 325 | 2711.9 | 10.0 | 27118.96 |
No risky functions detected or complexity analysis failed.

## Final Summary

This codebase has significant quality issues. Focus on improving maintainability, test coverage, and documentation.
Code Coverage: No coverage reports found in the repository.
API Quality: No API endpoints or specifications detected.
Monitoring: No logging or monitoring integrations detected.
## Security & Static Analysis Findings (Semgrep)

**Total Security Findings:** 13

- Critical: 0
- Error: 7
- Warning: 6
- Info: 0

| Severity | File | Line | Rule | Message |
|----------|------|------|------|---------|
| ERROR | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpfvtufg8z/.github/workflows/build.yml | 49 | yaml.github-actions.security.run-shell-injection.run-shell-injection | Using variable interpolation `${{...}}` with `github` context data in a `run:` step could allow an attacker to inject their own code into the runner. This would allow them to steal secrets and code. `github` context data can have arbitrary user input and should be treated as untrusted. Instead, use an intermediate environment variable with `env:` to store the data and use the environment variable in the `run:` script. Be sure to use double-quotes the environment variable, like this: "$ENVVAR". |
| WARNING | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpfvtufg8z/livekit-agents/livekit/agents/cli/discover.py | 59 | python.lang.security.audit.non-literal-import.non-literal-import | Untrusted user input in `importlib.import_module()` function allows an attacker to load arbitrary code. Avoid dynamic values in `importlib.import_module()` or use a whitelist to prevent running untrusted code. |
| WARNING | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpfvtufg8z/livekit-agents/livekit/agents/ipc/log_queue.py | 53 | python.lang.security.deserialization.pickle.avoid-pickle | Avoid using `pickle`, which is known to lead to code execution vulnerabilities. When unpickling, the serialized data could be manipulated to run arbitrary code. Instead, consider serializing the relevant data as JSON or a similar text-based serialization format. |
| WARNING | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpfvtufg8z/livekit-agents/livekit/agents/ipc/log_queue.py | 105 | python.lang.security.deserialization.pickle.avoid-pickle | Avoid using `pickle`, which is known to lead to code execution vulnerabilities. When unpickling, the serialized data could be manipulated to run arbitrary code. Instead, consider serializing the relevant data as JSON or a similar text-based serialization format. |
| ERROR | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpfvtufg8z/livekit-agents/livekit/agents/voice/background_audio.py | 9 | python.lang.compatibility.python37.python37-compatibility-importlib2 | Found 'importlib.resources', which is a module only available on Python 3.7+. This does not work in lower versions, and therefore is not backwards compatible. Use importlib_resources instead for older Python versions. |
| WARNING | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpfvtufg8z/livekit-plugins/livekit-blingfire/setup.py | 29 | python.lang.security.audit.exec-detected.exec-detected | Detected the use of exec(). exec() can be dangerous if used to evaluate dynamic content. If this content can be input from outside the program, this may be a code injection vulnerability. Ensure evaluated content is not definable by external sources. |
| ERROR | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpfvtufg8z/livekit-plugins/livekit-plugins-baseten/livekit/plugins/baseten/stt.py | 51 | python.lang.security.unverified-ssl-context.unverified-ssl-context | Unverified SSL context detected. This will permit insecure connections without verifying SSL certificates. Use 'ssl.create_default_context' instead. |
| ERROR | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpfvtufg8z/livekit-plugins/livekit-plugins-browser/livekit/plugins/browser/proc_main.py | 1 | python.lang.compatibility.python37.python37-compatibility-importlib2 | Found 'importlib.resources', which is a module only available on Python 3.7+. This does not work in lower versions, and therefore is not backwards compatible. Use importlib_resources instead for older Python versions. |
| WARNING | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpfvtufg8z/livekit-plugins/livekit-plugins-browser/setup.py | 29 | python.lang.security.audit.exec-detected.exec-detected | Detected the use of exec(). exec() can be dangerous if used to evaluate dynamic content. If this content can be input from outside the program, this may be a code injection vulnerability. Ensure evaluated content is not definable by external sources. |
| WARNING | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmpfvtufg8z/livekit-plugins/livekit-plugins-browser/src/run_browser.py | 45 | python.flask.security.audit.app-run-security-config.avoid_using_app_run_directly | top-level app.run(...) is ignored by flask. Consider putting app.run(...) behind a guard, like inside a function |

*... and 3 more findings not shown*

## Custom Static Analysis Findings


### AI-Generated/Placeholder Code (3114 instances)

| Type | File | Line | Snippet |
|------|------|------|---------|
| Potential Placeholder Function | tests/fake_session.py | 71 | async def run_session(session: AgentSession, agent: Agent, *, drain_delay: float = 1.0) -> float: |
| Potential Placeholder Function | tests/fake_session.py | 102 | def __init__(self) -> None: |
| Potential Placeholder Function | tests/fake_session.py | 174 | def get_user_speeches(self, *, speed_factor: float = 1.0) -> list[FakeUserSpeech]: |
| Potential Placeholder Function | tests/fake_session.py | 177 | def get_llm_responses(self, *, speed_factor: float = 1.0) -> list[FakeLLMResponse]: |
| Potential Placeholder Function | tests/fake_session.py | 180 | def get_tts_responses(self, *, speed_factor: float = 1.0) -> list[FakeTTSResponse]: |
| Potential Placeholder Function | tests/test_schema_gemini.py | 14 | async def test_json_def_replaced(): |
| Potential Placeholder Function | tests/test_schema_gemini.py | 72 | async def test_json_def_replaced_any_of(): |
| Potential Placeholder Function | tests/test_schema_gemini.py | 104 | async def test_json_def_recursive(): |
| Potential Placeholder Function | tests/test_schema_gemini.py | 141 | async def test_json_def_date(): |
| Potential Placeholder Function | tests/test_ipc.py | 33 | def write(self, b: io.BytesIO) -> None: |
| Potential Placeholder Function | tests/test_ipc.py | 39 | def read(self, b: io.BytesIO) -> None: |
| Potential Placeholder Function | tests/test_ipc.py | 52 | def _echo_main(mp_cch): |
| Potential Placeholder Function | tests/test_ipc.py | 53 | async def _pong(): |
| Potential Placeholder Function | tests/test_ipc.py | 66 | async def test_async_channel(): |
| Potential Placeholder Function | tests/test_ipc.py | 89 | def test_sync_channel(): |
| Potential Placeholder Function | tests/test_ipc.py | 110 | def _generate_fake_job() -> job.RunningJobInfo: |
| Potential Placeholder Function | tests/test_ipc.py | 132 | def _new_start_args(mp_ctx: BaseContext) -> _StartArgs: |
| Potential Placeholder Function | tests/test_ipc.py | 144 | def _initialize_proc(proc: JobProcess) -> None: |
| Potential Placeholder Function | tests/test_ipc.py | 157 | async def _job_entrypoint(job_ctx: JobContext) -> None: |
| Potential Placeholder Function | tests/test_ipc.py | 160 | async def _job_shutdown() -> None: |

*... and 3094 more*

### Security Issues (902 instances)

| Type | File | Line | Snippet |
|------|------|------|---------|
| Hardcoded Credential | tests/test_ipc.py | 114 | token="fake_token", |
| Potential Secret | tests/test_tts.py | 122 | "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}", |
| Potential Secret | examples/other/kokoro_tts.py | 52 | api_key="not-needed", |
| Hardcoded Credential | examples/other/kokoro_tts.py | 52 | api_key="not-needed", |
| Potential Secret | examples/drive-thru/order.py | 3 | import secrets |
| Potential Secret | examples/drive-thru/order.py | 13 | return "O_" + "".join(secrets.choice(alphabet) for _ in range(6)) |
| Potential Secret | examples/voice_agents/speaker_id_multi_speaker.py | 14 | # Required: SPEECHMATICS_API_KEY, OPENAI_API_KEY |
| Potential Secret | examples/voice_agents/langfuse_trace.py | 41 | secret_key: str | None = None, |
| Potential Secret | examples/voice_agents/langfuse_trace.py | 47 | secret_key = secret_key or os.getenv("LANGFUSE_SECRET_KEY") |
| Potential Secret | examples/voice_agents/langfuse_trace.py | 50 | if not public_key or not secret_key or not host: |
| Potential Secret | examples/voice_agents/langfuse_trace.py | 51 | raise ValueError("LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, and LANGFUSE_HOST must be set") |
| Potential Secret | examples/voice_agents/langfuse_trace.py | 53 | langfuse_auth = base64.b64encode(f"{public_key}:{secret_key}".encode()).decode() |
| Potential Secret | examples/frontdesk/frontdesk_agent.py | 173 | if cal_api_key := os.getenv("CAL_API_KEY", None): |
| Potential Secret | examples/frontdesk/frontdesk_agent.py | 174 | logger.info("CAL_API_KEY detected, using cal.com calendar") |
| Potential Secret | examples/frontdesk/frontdesk_agent.py | 175 | cal = CalComCalendar(api_key=cal_api_key, timezone=timezone) |
| Potential Secret | examples/frontdesk/frontdesk_agent.py | 178 | "CAL_API_KEY is not set. Falling back to FakeCalendar; set CAL_API_KEY to enable Cal.com integration |
| Potential Secret | examples/frontdesk/calendar_api.py | 100 | def __init__(self, *, api_key: str, timezone: str) -> None: |
| Potential Secret | examples/frontdesk/calendar_api.py | 102 | self._api_key = api_key |
| Potential Secret | examples/frontdesk/calendar_api.py | 204 | h = {"Authorization": f"Bearer {self._api_key}"} |
| Potential Secret | examples/avatar_agents/bithuman/agent_worker.py | 23 | bithuman_api_secret = os.getenv("BITHUMAN_API_SECRET") |

*... and 882 more*

### Code Quality Issues (20 instances)

| Type | File | Line | Snippet |
|------|------|------|---------|
| Code Quality Issue | tests/test_tts.py | 598 | # TODO: NOT SUPPORTED YET |
| Code Quality Issue | examples/other/translation/multi-user-translator.py | 363 | # TODO: this is test code |
| Code Quality Issue | examples/voice_agents/speedup_output_audio.py | 66 | # TODO: find a streamed way to process the audio |
| Code Quality Issue | livekit-agents/livekit/agents/llm/utils.py | 114 | # TODO: check other content types |
| Code Quality Issue | livekit-agents/livekit/agents/cli/cli.py | 160 | self._output_buf += frame.data  # TODO: optimize |
| Code Quality Issue | livekit-agents/livekit/agents/cli/cli.py | 599 | del self._io_audio_output.audio_buffer[:available_bytes]  # TODO: optimize |
| Code Quality Issue | livekit-agents/livekit/agents/cli/cli.py | 1153 | self._server._job_executor_type = JobExecutorType.THREAD  # TODO: better setter |
| Code Quality Issue | livekit-agents/livekit/agents/cli/cli.py | 1229 | # TODO: wait for a session request the agents console context before showing any of the mode |
| Code Quality Issue | livekit-agents/livekit/agents/voice/agent_activity.py | 1136 | # TODO: for realtime models, the created_at field is off. it should be set to when the user started  |
| Code Quality Issue | livekit-agents/livekit/agents/voice/audio_recognition.py | 58 | # TODO: Move those two functions to EOU ctor (capabilities dataclass) |
| Code Quality Issue | livekit-agents/livekit/agents/voice/audio_recognition.py | 379 | # TODO: this would screw up transcription latency metrics |
| Code Quality Issue | livekit-agents/livekit/agents/voice/avatar/_datastream_io.py | 374 | retry_count = 0  # TODO: use retry logic in rust |
| Code Quality Issue | livekit-plugins/livekit-plugins-sarvam/livekit/plugins/sarvam/stt.py | 119 | ) -> float:  # TODO: Copied from livekit/agents/utils/audio.py, check if it can be reused |
| Code Quality Issue | livekit-plugins/livekit-plugins-sarvam/livekit/plugins/sarvam/stt.py | 527 | ) as e:  # TODO: Check if retry should happen for every Exception type |
| Code Quality Issue | livekit-plugins/livekit-plugins-aws/livekit/plugins/aws/experimental/realtime/realtime_model.py | 956 | # TODO: save this as a field so we're not re-awaiting it every time |
| Code Quality Issue | livekit-plugins/livekit-plugins-aws/livekit/plugins/aws/experimental/realtime/realtime_model.py | 1387 | # TODO: fix this nit |
| Code Quality Issue | livekit-plugins/livekit-plugins-openai/livekit/plugins/openai/realtime/realtime_model_beta.py | 1561 | # TODO: set exception for the response future if it exists |
| Code Quality Issue | livekit-plugins/livekit-plugins-openai/livekit/plugins/openai/realtime/realtime_model.py | 1739 | # TODO: set exception for the response future if it exists |
| Code Quality Issue | livekit-plugins/livekit-plugins-deepgram/livekit/plugins/deepgram/stt.py | 696 | sd.language = alt["languages"][0]  # TODO: handle multiple languages |
| Code Quality Issue | livekit-plugins/livekit-plugins-mistralai/livekit/plugins/mistralai/llm.py | 169 | # TODO: support thinking chunks |
