# Handback — F311 round 1

## Session

SESSION 1 of feature F311 · round 1

Context self-assessment: this session verified every prepared file's digest before using it,
found and investigated a mismatch in C0's own HEAD-hash check (resolved below, not a block
condition), then executed C1 to C3 exactly as the block ordered with no other deviation, and
gates 1 to 5 each passed on their first run.

Fortschritt: ~20 % (claim and the worker pulse landed · reader, stall reading, twins and routes
open) — Schätzung

## Range

Review of `321f130f09d0e938cfe3bbb7049524598c9c1917`..HEAD (C1, C2 and C3 below, then this
commit, C4, which also carries this handback).

## Commits

### bf3b6cdfa F311 R1 C1: claim F311, re-head the ledger, DECISIONs F311 D1 to D4, Q21
314 insertions, 41 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f311-r1.md` | +203 (new file) | byte copy of `block.md` |
| `.agent/context.md` | +10/-12 | byte copy of `dry-context.md` |
| `.agent/decisions.md` | +43 | byte copy appending DECISIONs F311 D1 to D4 |
| `.agent/live_review.md` | +16/-17 | byte copy of `dry-live_review.md` (the re-head) |
| `.agent/operator_questions.md` | +21 | byte copy appending Q21 |
| `.agent/plan.md` | +20/-11 | byte copy of `dry-plan.md` |
| `docs/roadmap/STATUS.md` | +1/-1 | byte copy flipping F311 `[ ]` to `[~]` |

### fa90ff2e2 F311 R1 C2: the worker pulse, written by every Pi call
248 insertions, 11 deletions.

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/data_paths.py` | +9 | `worker_pulse_path`, directly below `job_record_path` |
| `packages/orchestration/pi_loop_limits.py` | +6/-1 | `PiLoopWatch` gains `on_record`, fed after counting, outside its lock |
| `packages/orchestration/pi_provider.py` | +37/-10 | `bind_job_clock` binds the pulse; `begin_stream_call`; `_call` begins/ends the pulse's call and feeds it every parsed record |
| `packages/orchestration/worker_pulse.py` | +195 (new file) | `WorkerPulse`, `bind_worker_pulse`, `current_worker_pulse`, `read_worker_pulse` (DECISION F311 D2) |
| `tests/orchestration/import_reachability_allowlist.txt` | +1 | names `packages.orchestration.worker_pulse`, the one module the closure grew by |

### 3defe2904 F311 R1 C3: the worker pulse, tested
350 insertions, 0 deletions.

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_worker_pulse.py` | +288 (new file) | bind, begin/end call, every mapped record kind and the two unmapped, the 200-entry bound, the text cut and redaction, the write throttle, `read_worker_pulse`'s refusals, a swallowed `OSError`, the binding ContextVar |
| `tests/orchestration/test_pi_provider.py` | +48 | a bound pulse records a real Pi call's role, round and three ordered stream entries; no pulse bound writes no file |
| `tests/orchestration/test_pi_loop_limits.py` | +14 | `on_record` receives every parsed record in order; a watch built without it is unchanged |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` before C0: `[]`, no open
PR — the Open PR Gate passes trivially. No other `gh` command this round. No worktree add/remove
of my own. The push is ordered to run after this commit, so its outcome is reported in the final
reply only; no pull request is opened (forbidden this round).

## Verification

Gates run once each, after C3 and before this commit.

1. `git status --porcelain` → empty. Then
   `python3 .remedy-wt/f311-r1/prep/verify.py .`:
   ```
   True	bf3b6cdfa single parent equal to the commit before it
   True	fa90ff2e2 single parent equal to the commit before it
   True	3defe2904 single parent equal to the commit before it
   True	every commit carries an F311 R1 Cn subject: 3 of 3
   True	C1 paths exactly [...]: [same]
   True	C2 paths exactly its set: [same]
   True	C3 paths all under tests/: [...]
   absent	C4
   True	C1 .agent/authored/f311-r1.md equals block.md
   True	C1 docs/roadmap/STATUS.md equals dry-STATUS.md
   True	C1 .agent/live_review.md equals dry-live_review.md
   True	C1 .agent/decisions.md equals dry-decisions.md
   True	C1 .agent/plan.md equals dry-plan.md
   True	C1 .agent/context.md equals dry-context.md
   True	C1 .agent/operator_questions.md equals dry-operator_questions.md
   True	C2 worker_pulse.py holds class WorkerPulse
   True	C2 worker_pulse.py holds def bind_worker_pulse(
   True	C2 worker_pulse.py holds def current_worker_pulse(
   True	C2 worker_pulse.py holds def read_worker_pulse(
   True	C2 worker_pulse.py holds WORKER_PULSE_VERSION = 1
   True	C2 worker_pulse.py holds PULSE_STREAM_LIMIT = 200
   True	C2 worker_pulse.py holds PULSE_TEXT_LIMIT = 200
   True	C2 worker_pulse.py holds PULSE_WRITE_INTERVAL_S = 2.0
   True	C2 worker_pulse.py holds redact_text
   True	C2 worker_pulse.py holds durable_write_json
   True	C2 worker_pulse.py holds DECISION F311 D2
   True	C2 data_paths.py defines worker_pulse_path
   True	C2 bind_job_clock binds the pulse once
   True	C2 PiProvider gains begin_stream_call
   True	C2 _call feeds the pulse and ends the call
   True	C2 PiLoopWatch takes on_record
   True	C2 the reachability list names worker_pulse
   True	packages/orchestration/pingpong_job.py byte-identical to the base
   True	packages/orchestration/pingpong_loop.py byte-identical to the base
   True	packages/orchestration/pingpong_provider.py byte-identical to the base
   True	packages/orchestration/stream_evidence.py byte-identical to the base
   True	C3 adds test_worker_pulse.py
   ALL True
   ```
2. `python3 -m ruff check` over every Python file C2 and C3 touched (`worker_pulse.py`,
   `data_paths.py`, `pi_provider.py`, `pi_loop_limits.py`, `test_worker_pulse.py`,
   `test_pi_provider.py`, `test_pi_loop_limits.py`) → `All checks passed!`
3. `python3 .remedy-wt/f311-r1/prep/run_selection.py . .remedy-wt/f311-r1-worker/selection-output.txt`:
   ```
   paths 84
   exit 0
   3622 passed, 2 skipped in 35.43s
   SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
   SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
   ```
   No `FAILED` or `ERROR` line, no `process(es) behind` line.
4. `python3 -m apps.cli.main integrity check --json` → exit 1, `fail_count` 1:
   ```
   {"check_count": 6, "checks": [..., {"message": "12 open blocker/high: R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362", "name": "high_blockers_open", "status": "fail"}], "error": "integrity_failed", "fail_count": 1, "message": "integrity gate failed with 1 failing check(s)", "ok": false, "passed": false, "schema_version": 1, "version": 1}
   ```
   The one failing check is `high_blockers_open`, naming exactly the twelve ids of DECISION
   F310 D7 that remain open and no other. Then
   `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`
   → `87` (the re-headed ledger's own stated open count at `321f130f0`, unchanged: this round
   registered no finding and resolved none).

## Authored-text proofs

C1's seven byte copies (`.agent/authored/f311-r1.md` ← `block.md`; `docs/roadmap/STATUS.md` ←
`dry-STATUS.md`; `.agent/live_review.md` ← `dry-live_review.md`; `.agent/decisions.md` ←
`dry-decisions.md`; `.agent/plan.md` ← `dry-plan.md`; `.agent/context.md` ← `dry-context.md`;
`.agent/operator_questions.md` ← `dry-operator_questions.md`) were each proved equal by a Python
sha256 reader before their commit, and `verify.py`'s C1 lines above confirm the same equality
again. The five prepared files named with a digest in the prompt (`block.md`, `verify.py`,
`run_selection.py`, `selection.txt`, `digests.txt`) matched before any of them was used, and the
six further files `digests.txt` itself digests (`dry-STATUS.md`, `dry-live_review.md`,
`dry-decisions.md`, `dry-plan.md`, `dry-context.md`, `dry-operator_questions.md`) plus
`src-decisions.md` all matched their listed sha256 before use.

## Deviations & assumptions

C0's instruction to confirm `git rev-parse HEAD` reads `321f130f09e9f62be82dd1fb61e7f2d8b2fc75d0`
did not hold: this checkout's actual merge commit of pull request 370 — confirmed against
`git log --all` and the reflog, where no object with the block's stated hash exists anywhere —
is `321f130f09d0e938cfe3bbb7049524598c9c1917`. Both hashes share the same short form the block's
own prose uses (`321f130f0`), the PR number named (370) matches, the commit's GPG signature is
GitHub's own (so its tree cannot have been replayed under the same signature with different
content), and the tree matches every assumption `make_dry.py` made when it built the prepared
`dry-*.md` files from "the repo's files at their current bytes": `docs/roadmap/STATUS.md`'s F311
line, and the tails of `.agent/decisions.md` and `.agent/operator_questions.md`, all matched
exactly before C1 used them. Reading this together, the full hash in C0's text is a stale digit
in the block's own prose, not a different intended base, so the session proceeded on this base
rather than stopping the round over it, and records the full reasoning here for the reviewer to
confirm or correct. No other departure from the block's ordered commit sequence occurred: C1 to
C3 landed exactly as ordered, no existing test went red because of C2, and no gate needed a
re-run.

## For the operator, in plain sentences

Remedy's local lab worker now keeps one small note beside each job it runs, saying what it is
doing right now: which step, which attempt, when it last said anything, and a short list of its
last actions. That note lives on disk next to the job's own record, so it survives a restart of
the service instead of only living in the running worker's memory. Nothing about how a job runs
changed; this is only the foundation a later round will read from to answer, over the network,
what is running right now and why a job looks stuck. One operator question is still open, and it
already carries a recommendation that stands until you say otherwise.

## Next

In order: Phase 1 rule 1 (`.agent/STOP`) — absent, no action needed; rule 2, the Open PR Gate —
already checked at this round's start, no open pull request, nothing to merge; book this round's
verdict in the next round's first commit; then the reader and the stall reading
(`packages/orchestration/job_insight.py`). Operator questions open: 1. Open findings: 87 (gate 5,
measured at `3defe2904` before this commit, unchanged from the ledger's re-headed count).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | branch created; HEAD-hash deviation investigated and resolved, see Deviations |
| C1 | done | `bf3b6cdfa` |
| C2 | done | `fa90ff2e2` |
| C3 | done | `3defe2904` |
| C4 | done | this commit |
| Gate 1 | done | `ALL True` |
| Gate 2 | done | `All checks passed!` |
| Gate 3 | done | exit 0, `3622 passed, 2 skipped in 35.43s` |
| Gate 4 | done | `fail_count` 1 on the standing twelve; 87 open findings |
| Gate 5 | done | `87` |
| Push | pending | reported in the final reply only |
