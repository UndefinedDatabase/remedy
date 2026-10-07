# F287 claim inventory — provider session resume at `7c91c3b69`

Measured by the planner and reviewer at the F287 claim, 2026-10-07, in the primary checkout on
`main` at `7c91c3b69` (the merge commit of pull request 311), with
`python3 .agent/authored/f287-r1-measure.py` run from the repository root. The script imports the
product, instantiates the four providers without calling them, and reads source text; it starts no
provider process. Its output, verbatim:

```
1. supports_resume per provider (instantiated, never called)
   FakeProvider             name='fake'         supports_resume=False
   ClaudeProvider           name='claude'       supports_resume=False
   ClaudeCliProvider        name='claude-cli'   supports_resume=False
   OllamaPingPongProvider   name='ollama'       supports_resume=False
2. build_claude_cli_args: parameters and the argv of a plain call
   ['claude_path', 'prompt', 'write_mode', 'model', 'stream_evidence', 'json_schema']
   ['claude', '-p', 'PROMPT', '--output-format', 'json']
3. ClaudeCliProvider: which methods take `resume`, and how often the body uses it
   build                      takes_resume=True  body_uses=0
   _build_impl                takes_resume=False  body_uses=0
   review                     takes_resume=True  body_uses=0
   _review_impl               takes_resume=False  body_uses=0
   _call                      takes_resume=False  body_uses=0
   _call_streamed             takes_resume=False  body_uses=0
   _call_reviewer_structured  takes_resume=False  body_uses=0
4. ClaudeCliProvider outputs: is resume_used / resume_session_ref ever set?
   resume_used: 0  resume_session_ref: 0
5. run_pingpong: the R-1055 relaunch hand-over and the fallback-once rule
   'resume_sessions.get("builder")': 1
   'resume_sessions.get("reviewer")': 1
   'builder_out.resume_fallback = True': 1
   'reviewer_out.resume_fallback = True': 1
6. the claude-cli provider's working directory is the run's staging path
   '"cwd": staging_dir' in _create_provider_with_cwd: True
7. tests that construct a resuming claude-cli provider today
   ['tests/orchestration/test_session_resume.py']
```

## What the readings mean

- No production provider resumes today: `claude-cli`, the Anthropic API provider `claude` and
  `ollama` all answer `supports_resume` with false, and so does the test provider by default.
- `claude-cli` accepts `resume` on `build` and `review` and drops it: none of the five methods
  beneath them takes it, the CLI argv has no resume option, and no output field records a resume.
- The relaunch hand-over (R-1055, DECISION F285 D2) and the fallback-once rule (F106 T002c) are
  already in `run_pingpong`, each once per role; F287 does not touch them.
- The provider runs in the run's staging path. The `claude` CLI keeps its sessions per working
  directory, so T002 measures whether a relaunch uses the parked run's directory before it relies
  on a resume.
- `tests/orchestration/test_session_resume.py` pins `ClaudeCliProvider().supports_resume is False`;
  T001 changes that pin on purpose.
