# Handoff — F287 session 1, round 6: tests-only proof that a relaunch on claude-cli resumes the parked session in the job's worktree and falls back once in copy mode — all gates GREEN

## Session

SESSION 1 of feature F287 · round 6 · rounds so far 6

Context self-assessment: The reviewer's context is still workable but long after seven delegated
rounds in this session, one for F295 and six for F287; the session ends after this round, inside
the six-to-eight target, so that the next session starts T003 fresh.

Fortschritt: ~60 % (claim · T001 complete · T002 landed, review pending · T003, the hardening
stage and closure open) — Schätzung

## Range

Review of `9213a3c76`..HEAD (HEAD is C3 below, the commit that carries this handback).

## Commits

### 7e336e273 F287 R6 C1: book round 5, register R-1162, DECISION F287 D5, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f287-r6.md` | 132/0 (new) | byte copy of this round's block |
| `.agent/live_review.md` | 4/0 | append the F287 R5 gate entry (PASS) and R-1162's OPEN line, exactly as prepared |
| `.agent/decisions.md` | 10/0 | append DECISION F287 D5, exactly as prepared |
| `.agent/plan.md` | 8/9 | rewrite to round 6's current step |

### da57fef69 F287 R6 C2: a relaunch on claude-cli resumes the parked session in the job's worktree and falls back once in copy mode (T002, DECISION F287 D5)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_relaunch_session_resume.py` | 219/0 | new class `TestAParkedClaudeCliTaskResumesOnRelaunch`, with its own `_make_stand_in` replacement for `pingpong_provider._guarded_cli_run` shared by the parked run and its relaunch: it tracks the directory each session id was minted in, refuses a `--resume` naming a session from another directory (`returncode=1`, `stderr="No conversation found with session ID: <id>"`), and a successful builder call appends one line under `docs/README.md` in its own cwd so the task has a real change. `ClaudeCliProvider._get_claude_path`/`._resolve_version` are patched at the class level, matching the reviewer's probe scripts. Three tests, every one calling `run_job(..., builder_name="claude-cli", reviewer_name="claude-cli", builder_model="claude-sonnet-4-6", reviewer_model="claude-sonnet-4-6", repair_rounds=0)` for both the interrupted run and the relaunch: a git-target pause and a git-target stop each relaunch into the parked worktree, carry `--resume` with the parked builder session, and complete with `resume_used` true and the matching `resume_session_ref`; a copy-mode pause relaunches into a new directory, is refused, falls back once (two builder calls that round) and completes with `resume_fallback` true, `resume_used` false. No existing test changed; no production file touched. |

### F287 R6 C3: handback (self-reference exception — the handoff is committed by this same commit)

Measured before the handoff joined it (`git diff --cached --numstat`):

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file, rewritten in full per `docs/agents/handback_template.md` |

## External actions

- `git push origin feature/f287-provider-session-continuity` after C3: outcome reported in the worker's final reply (write-once rule; not known when this file is written).
- No merge, no `git checkout` or `git switch`, no branch moved or deleted, no force-push, no pull, no `gh` command, no pull request.

## Verification

0. Before any write: digests of all four reviewer-prepared files (`block.md`, `append-live_review.txt`, `append-decisions.txt`, `dry-plan.md`), computed by a worker-written Python sha256 script, all matched the prompt's sha256 lines exactly (4/4 MATCH). `HEAD` read `9213a3c76`, equal to `origin/feature/f287-provider-session-continuity`, and `git status --porcelain` was empty before any write. `git branch --show-current` read `feature/f287-provider-session-continuity` before every commit.
1. C1 copy/append step: `.agent/authored/f287-r6.md` read `byte_equal=True` against `block.md` (sha256 `f157dc5c9b418bde29e734567a73672c7264c593248af377efe5601770dc1f3f` on both sides; 132 lines by both newline count and `splitlines()`). `.agent/live_review.md`'s append read `byte_equal=True`: base blob (194003 bytes, sha256 `af87f6d0a59b1a49dad4036e634a303df843d9b1a492bdc08bf04d938de6ef33`) + `append-live_review.txt`'s bytes (3971 bytes, sha256 `c6d1e729aafc6bb3c9885e338ed9f6f3716c08a9da099815df26b7d69555f3a5`) hashed to the same sha256 (`b73c97e8ef8e510c4b0c6dd31eb5a3faf0b21e9a780aa05f58ecc27cea84d6de`) as the file after the append. `.agent/decisions.md`'s append read `byte_equal=True` (streamed, never read whole into one string): base blob (2906693 bytes, sha256 `04dad0128baf9e175be424780aee829d9b467fc63008c7d334c93c6014c24409`) + `append-decisions.txt`'s bytes (3081 bytes, sha256 `8319301ae41f8595bc4e66f93674f774877460e006510eb750b8b66fc8a29ab1`) hashed to the same sha256 (`750de30aea00b173c622a753268b77002f0f84955de5b0b79073bce275e04ccf`) as the file after the append. `.agent/plan.md` read `byte_equal=True` against `dry-plan.md` (sha256 `56d2eef01a98580ee5d54722791a12ff9eee02c01ea3973804532be7906ca119` on both sides).
2. `git diff --cached --numstat` (before the C1 commit) read exactly the four paths the block names — `132 0` `.agent/authored/f287-r6.md` (new), `10 0` `.agent/decisions.md`, `4 0` `.agent/live_review.md`, `8 9` `.agent/plan.md`. The full cached diff was read before committing (self-review): the plan rewrite and both appends matched the prepared bytes exactly; no unrelated edit found.
3. Before C2: the full target test file, its imported fixtures (`test_job_stop_integration.py`), `test_claude_cli_resume.py`'s `TestRunPingpongResumesOnClaudeCli` stand-in, `pingpong_job.run_job`'s signature, `pause_control.request_pause`, `safe_points.request_stop`, and the reviewer's `probe_cwd_git.py`/`probe_cwd_stop_model.py` were read whole before editing. `python3 -m ruff check tests/orchestration/test_relaunch_session_resume.py` read `All checks passed!`, exit 0 (run twice: once while writing, once again after the commit for gate 3 — same clean result both times). While writing C2, the file was run alone once (permitted by the block; not gate 2): `15 passed in 5.30s`, exit 0 (12 existing tests + 3 new, none existing changed). `git diff --cached --numstat` before the C2 commit read exactly one path: `219 0 tests/orchestration/test_relaunch_session_resume.py`. The full cached diff was read before committing: one new class, `TestAParkedClaudeCliTaskResumesOnRelaunch`, plus the imports it needs (`json`, `subprocess`, `Path`, `MagicMock`/`patch`, `pingpong_provider`, `JOB_STOPPED`, `request_stop`); no existing test changed, no production file touched.
4. **Gate 1**: `git -C /home/decodeux/Repos/remedy status --porcelain` — empty. C1's byte proofs all `True` (above). `git show --numstat --format=` of `da57fef69` (C2) read exactly `219  0  tests/orchestration/test_relaunch_session_resume.py`. PASS.
5. **Gate 2**: `python3 -m pytest -q -rfEs tests/orchestration/test_relaunch_session_resume.py tests/orchestration/test_claude_cli_resume.py tests/orchestration/test_pause_resume.py tests/orchestration/test_job_stop_integration.py tests/cli/test_golden_path.py`, from the primary checkout, run once: exit 0, last line `131 passed in 53.97s`; no `FAILED`, `ERROR` or `SKIPPED` line anywhere in the captured output (grepped). PASS.
6. **Gate 3**: `python3 -m ruff check tests/orchestration/test_relaunch_session_resume.py` — exit 0, `All checks passed!`. PASS.
7. **Gate 4**: `python3 -m apps.cli.main integrity check --json` — exit 0: `{"check_count": 6, "checks": [{"message": "handlers=175", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}`; all six checks `pass`, `fail_count: 0`. `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"` read `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162']`, exactly as ordered. PASS.
8. **Gate 5** (after the push): reported in the worker's final reply (write-once rule; not known when this file is written).

## Authored-text proofs

- `block.md` → `.agent/authored/f287-r6.md`: 132 / 132 lines, sha256 `f157dc5c9b418bde29e734567a73672c7264c593248af377efe5601770dc1f3f` / same.
- `append-live_review.txt` → `.agent/live_review.md`: append proof `True` (base blob + slice, byte for byte).
- `append-decisions.txt` → `.agent/decisions.md`: append proof `True` (base blob + slice, byte for byte, streamed — never read whole into one string).
- `dry-plan.md` → `.agent/plan.md`: byte-equal, `True`.

## Deviations & assumptions

1. No departure from the block's ordered commit sequence: C1 and C2 each landed exactly as ordered, in their own commit, each ending with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`; C3 (this handback) is committed alone and the push follows it once.
2. The block's example for the stand-in's builder-success side effect — "appends to `docs/README.md`" under the call's own working directory — was taken literally: the stand-in itself creates `docs/` if missing and appends one line, in both the job worktree (git mode) and the per-run `/tmp/remedy-pingpong-<run id>` staging directory (copy mode), so every builder call that is not refused leaves a real, detectable change (`_staged_now()`/`_find_staging_changes` see it) rather than relying on `builder_no_changes`'s existing no-op tolerance.
3. The interruption point: the stand-in calls `interrupt()` (either `pc.request_pause` or `safe_points.request_stop`) on the very first builder call it ever sees, before building that call's envelope and returning it — mirroring `PauseTriggerProvider`/`CountingProvider`'s race for `FakeProvider` (trigger fires while the call is in flight, then the call still answers normally). Because the same closure (and its `state["interrupted"]` flag) is shared across both the parked `run_job` call and the relaunch `run_job` call in each test, the interrupt fires exactly once per test, on the parked run, never on the relaunch.
4. Session-id numbering again counts only calls that actually answer success (continuing the round-5 reading of the spec's "answers `session_id` ... in call order" clause): a refused `--resume` attempt is recorded in the test's own `calls` list with an empty `session_id`, consistent with `ClaudeCliProvider` itself never reporting a session on a refused call.
5. Copy mode's "a different directory" property was verified by tracing the production code rather than only asserting it: `_acquire_job_workspace` reuses `job.job_workspace_path` across runs only for bookkeeping, but `workspace_owner` is `"run"` whenever `job_handle is None` (true for every non-git job), so `run_pingpong`'s own `_job_owned` is `False` in copy mode and it creates a fresh `/tmp/remedy-pingpong-<run id>` staging directory every call, matching DECISION F287 D5's measurement. No production file was touched to confirm this — it was read, not changed.
6. All gates read GREEN this round: no gate-driven stop was needed. `.agent/STOP` was not present at any point in the round.
7. Helper scripts under `.remedy-wt/f287-r6-worker/` (gitignored, left untracked) did the digest checks, the copy/append operations, their proofs, and ran the gates; none of them touched any path outside the ones this round's commits name, and none touched `.remedy-wt/f287-r6/`.
8. No other departure.

## Round verdicts

Round 5 PASS is booked by C1 above (carried in the `append-live_review.txt` slice, re-deriving the
F287 R5 gate entry). Round 6's verdict is the next session's reviewer's to give and book in that
session's first commit — this handback reports all five gates GREEN for the reviewer to re-derive,
not a self-granted closure.

## For the operator, in plain sentences

In this session the previous feature was merged after its GitHub tests passed. The new feature now
lets Remedy continue its earlier conversation with the Claude command-line tool when a paused or
stopped job starts again, and in repair rounds. When Remedy works inside its own copy of a git
project the conversation is found again, while for a folder that is not a git project the tool
cannot find it and Remedy starts fresh once, which costs no tokens. While checking this, the
reviewer found that a job on the Claude tool with no model chosen cannot be stopped cleanly, which
is recorded for the next clean-up feature. One question (Q8) is waiting, and its recommendation is
already in effect.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handoff and
   stop. (Not present as of this handback.)
2. Phase 1 rule 2 (the Open PR Gate): check for open pull requests before any new branch.
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Review round 6 (its block is `.agent/authored/f287-r6.md`; the reviewer's scripts are under
   `.remedy-wt/f287-r6/`) and book its verdict in the next round's first commit.
5. T003: the other providers record that they did not resume; the operator guide.

Operator questions open: 2.
Open findings: 9 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158 and
R-1162, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 5, register R-1162, DECISION F287 D5, the plan | done | `7e336e273` |
| C2: a relaunch on claude-cli resumes the parked session in the job's worktree and falls back once in copy mode (T002) | done | `da57fef69` |
| Gate 1 | done | status clean, byte proofs True, C2 numstat exact |
| Gate 2 | done | `131 passed in 53.97s`, exit 0 |
| Gate 3 | done | ruff `All checks passed!`, exit 0 |
| Gate 4 | done | integrity 6/6 pass, `fail_count: 0`; open findings list exact |
| C3 handback commit | done | this file |
| Push, gate 5 | pending | run right after this commit, reported in the worker's final reply |
