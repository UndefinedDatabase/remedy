## What

F287 — Provider session continuity across relaunch. When a task that a pause or a stop interrupted
runs again on the `claude-cli` provider, its builder and reviewer now continue the sessions they
last used, so the context those sessions already held is not paid for twice. Every other
production provider says in the run record that it did not resume, instead of starting fresh
silently.

- **T001, `claude-cli` resumes.** `build_claude_cli_args` passes `--resume <ref>` only for a
  session reference that fully matches a plain session-id shape, and refuses any other (D2).
  `ClaudeCliProvider` threads the offered session through every call path, records
  `resume_used` and `resume_session_ref` only on a call that succeeded, and answers a failed
  resumed call with `resume_refused:`, which is never transport-retried, so the existing
  fallback-once rule runs on the first failure (D3). `supports_resume` answers true (D4), which
  also turns on F106's repair-round resume and F109's resumed-prompt dedupe for this provider (D6).
- **T002, the relaunch.** No production change was needed (D5): a job on a git target relaunches
  in its own worktree, where the `claude` CLI finds the parked session; a job in copy mode gets a
  new staging directory per run, so its resume is refused and falls back once at full context.
  `tests/orchestration/test_relaunch_session_resume.py` proves both through `run_job`, for a pause
  and for a stop.
- **T003, providers that cannot resume.** `ClaudeProvider` and `OllamaPingPongProvider` say why
  in `resume_unsupported_reason`; a relaunch that offers them a parked session records the role
  and the reason under `resume_declined` in `result.json` and goes on fresh (D7).
  `docs/system/session-resume-v1.md` names which providers resume and the copy-mode limit.
- **The hardening stage (SLOW MODE).** A fresh auditor checked 9 statements of the feature file;
  all 9 had a test that failed under a mutation. Its one gap, no proof through the command line
  (R-1163), is closed by `tests/cli/test_job_run_session_resume.py`, which pauses and relaunches a
  job with `remedy job pause` and `remedy job run` and reads `remedy run show --json`. A repeat
  audit found no gap.
- **A docs repair during the closure (R-1164).** `docs/system/semantic-dedupe-v1.md` and the
  README's F109 entry still said that no production provider resumes; both now say that
  `claude-cli` repair rounds may dedupe and the other two providers never resume.

## Why

Finding R-1055 found that a relaunch after a park never resumed a provider session. F285 built
the record and the hand-over but proved it only through the test provider, because every
production provider answered `supports_resume` with false. So in real use a relaunch still paid
again for the context the parked session held. Token frugality is the operator's first priority.

## Key decisions (in `.agent/decisions.md`)

- D1: three slices in the feature file's order.
- D2: the session reference is validated before it reaches the child's argument list.
- D3: a refused resume answers `resume_refused:` and is never transport-retried.
- D4: `claude-cli` answers `supports_resume` with true.
- D5: the relaunch needs no production change; copy mode always falls back.
- D6: the operator confirmed that F106's repair-round resume and F109's dedupe go live on
  `claude-cli`.
- D7: a declined resume is named with its reason under `resume_declined`.

## How to review / test

- Read `docs/roadmap/features/T3_F287.md`'s Built State first, then
  `docs/system/session-resume-v1.md`'s section "Which providers resume".
- `python3 -m pytest -q tests/orchestration/test_claude_cli_resume.py tests/orchestration/test_relaunch_session_resume.py tests/orchestration/test_session_resume.py tests/cli/test_job_run_session_resume.py tests/cli/test_golden_path.py`
- The closure suite transcript is `.agent/authored/f287-closure-suite.txt`: `21520 passed, 22
  skipped`, exit 0, 1098.51 CPU seconds, 5.7 percent less than F295's closure.

## Changed files (outside `.agent/`, fork point `7c91c3b69` to this branch)

| Path | + | - |
|---|--:|--:|
| `README.md` | 15 | 4 |
| `docs/agents/planner_reviewer_prompt.md` | 7 | 0 |
| `docs/roadmap/STATUS.md` | 1 | 1 |
| `docs/roadmap/features/T3_F287.md` | 59 | 0 |
| `docs/system/semantic-dedupe-v1.md` | 9 | 8 |
| `docs/system/session-resume-v1.md` | 31 | 4 |
| `packages/orchestration/pingpong_loop.py` | 27 | 0 |
| `packages/orchestration/pingpong_provider.py` | 76 | 15 |
| `scripts/self_use_queue.json` | 8 | 0 |
| `tests/cli/test_job_run_session_resume.py` | 131 | 0 |
| `tests/orchestration/test_claude_cli_resume.py` | 535 | 0 |
| `tests/orchestration/test_relaunch_session_resume.py` | 307 | 1 |
| `tests/orchestration/test_session_resume.py` | 5 | 4 |

## Verdict and evidence

- Latest live review verdict: PASS (round 16); F287 accepted PASS_WITH_RISKS, the risks being the
  open findings below.
- Evidence job `f287r16e1001`, package `remedy-review-20261007-150840-READY_FOR_REVIEW.zip`,
  SHA-256 `90554c5598fb14a5804bd34b241802a7d6006473a4006c5b3b502ce5305a781b`, archived at
  `/home/decodeux/Repos/remedy-history/zips`, accepted head `ee90eaa09`. It replaces the package
  `remedy-review-20261007-144203-READY_FOR_REVIEW.zip` of round 14, which round 15's docs repair
  outdated.
- Resolved on this branch: R-1159 (carried from F295), R-1161, R-1163 and R-1164.
- Open findings: 9, all owned by F297, Findings paydown v7. R-1162 (Low) was raised here: a
  `claude-cli` job with no model configured cannot finish a stop. R-1160 (Medium) and R-1138,
  R-1139, R-1143, R-1149, R-1156, R-1157 and R-1158 (Low) were carried from earlier features.

## Runtime actuals

- Rounds: 17, in 3 sessions, all on 2026-10-07. Rounds 2 and 3 failed review and were repaired;
  every other round passed.
- Models: the workers' commit trailers name Claude Opus 5.5 and Claude Sonnet 5; the third
  session's reviewer ran on Claude Opus 5.5. The closure's self-use job SU-046 ran on
  `claude-cli` / `claude-sonnet-4-6`: 2 provider calls, a measured $0.66 against a $6.00 budget,
  completed without a repair round, never applied.
- Tokens and cost of the sessions themselves: not measured.
- Full-suite runs: one, in round 12, green.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
