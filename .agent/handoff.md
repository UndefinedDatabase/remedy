# Handoff — F295 session 2, round 9: book round 8, repair R-1145, prove an unattended run never reads stdin (T003, DECISION F295 D8)

## Session

SESSION 2 of feature F295 · rounds 7 to 9 · rounds so far 9

Context self-assessment: "The reviewer's context is comfortable after three rounds; the session
continues."

Fortschritt: ~72 % (T001 and T002 landed · T003's stdin proof landed, review pending · T003's decision kinds and T004 open; then the hardening stage and the closure) — Schätzung

## Range

Review of `977e6e5e5`..`7d24833c8`, plus this handback commit.

## Commits

### af749f212 F295 R9 C1: book round 8, resolve R-1144, register R-1145, DECISION F295 D8, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f295-r9.md` | 122/0 (new) | byte copy of the round 9 block |
| `.agent/live_review.md` | 6/0 | append round 8's gate entry (PASS), the resolution of R-1144 and the registration of R-1145 as the reviewer prepared them |
| `.agent/decisions.md` | 10/0 | append DECISION F295 D8 |
| `.agent/plan.md` | 7/8 | rewrite to round 9's current step |

### 927d233d3 F295 R9 C2: a provider child reads end-of-file, never the caller's stdin (R-1145)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/exec_guard.py` | 3/0 | byte copy of the prepared file: the guarded spawn gives the child end-of-file as stdin |
| `packages/orchestration/stream_evidence.py` | 2/0 | byte copy of the prepared file: the streamed spawn gives the child end-of-file as stdin |

### ce552b87a F295 R9 C3: tests that both provider spawns ignore an open stdin pipe (R-1145)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_exec_guard.py` | 39/0 | byte copy of the prepared test file |
| `tests/orchestration/test_stream_evidence.py` | 39/0 | byte copy of the prepared test file |

### 7d24833c8 F295 R9 C4: an unattended run and the cost confirmation never read an open stdin pipe (T003)

| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_cost_preview_confirm.py` | 46/0 | byte copy of the prepared test file |
| `tests/cli/test_do_flags.py` | 38/0 | byte copy of the prepared test file |

### F295 R9 C5: handback (self-reference exception — committed by this same write)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file, rewritten in full per `docs/agents/handback_template.md` |

## External actions

None during the round before C5. After C5: `git push origin feature/f295-machine-client-contract-v1`;
its outcome is in the worker's final reply (write-once rule). No PR opened, no `gh` command.

## Verification

Gates ran once each, after C4 and before C5.

1. `git -C /home/decodeux/Repos/remedy status --porcelain` → empty output. Byte comparison of
   every file each of C1 to C4 wrote (`git show <commit>:<path>`) against its prepared file,
   ten of ten equal.
2. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r9/run.py /home/decodeux/Repos/remedy 5
   python3 -m ruff check packages/orchestration/exec_guard.py
   packages/orchestration/stream_evidence.py tests/orchestration/test_exec_guard.py
   tests/orchestration/test_stream_evidence.py tests/cli/test_cost_preview_confirm.py
   tests/cli/test_do_flags.py`
   ```
   exit 0
   All checks passed!
   ```
3. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r9/run_selection.py /home/decodeux/Repos/remedy`
   ```
   exit 0
   SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
   SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
   SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
   4134 passed, 3 skipped in 36.67s
   ```
   No FAILED, ERROR or `process(es) behind` line.
4. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r9/run.py /home/decodeux/Repos/remedy 3
   python3 -m apps.cli.main integrity check --json`
   ```
   exit 0
   {"check_count": 6, "checks": [{"message": "handlers=174", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
   ```
5. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r9/run.py /home/decodeux/Repos/remedy 3
   python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
   ```
   exit 0
   ['R-1138', 'R-1139', 'R-1143', 'R-1145']
   ```

## Authored-text proofs

- `block.md` → `.agent/authored/f295-r9.md`: 122 lines / 122 lines, sha256
  `ef8b6111cdd9fd810703c6bb3a9efc1eef239f8f8aebab8de4c3b5b7c26bdc2e` / same, byte comparison equal.
- Every prepared file copied over its target (`dry-live_review.md`, `dry-decisions.md`,
  `dry-plan.md`, `dry-exec_guard.py`, `dry-stream_evidence.py`, `dry-test_exec_guard.py`,
  `dry-test_stream_evidence.py`, `dry-test_cost_preview_confirm.py`, `dry-test_do_flags.py`):
  byte comparison equal, before the commit and again from the committed bytes in gate 1.
- Append proofs: `git show 977e6e5e5:.agent/live_review.md` plus the bytes of
  `append-live_review.txt` equals the new file: `True`; the same for `.agent/decisions.md` with
  `append-decisions.txt`: `True`.
- Every prepared file's sha256 was read with Python before use and matched the block's value.
- `git diff --cached --numstat` before each commit matched the block's cells: C1 `122 0`, `10 0`,
  `6 0`, `7 8`; C2 `3 0`, `2 0`; C3 `39 0`, `39 0`; C4 `46 0`, `38 0`.

## Round verdicts

Rounds 1 to 5, 7 and 8 PASS and round 6 FAIL, booked in the ledger (round 8 by this round's C1).
Round 9's verdict is the reviewer's to give and book in the next round's first commit.

## For the operator, in plain sentences

A program that starts Remedy and leaves its input channel open, without ever writing to it, can no
longer make Remedy wait. Remedy itself never asks a question in that case, and four new tests prove
it by starting real processes with such an open channel. The reviewer found that the processes
Remedy starts for the AI builder and reviewer used to inherit that channel and could have waited on
it until their time limit; they now get an empty input instead. Nothing waits for the operator.

## Deviations & assumptions

- Attribution line: every commit of this round closes with
  `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`, the model this worker runs on.
- Helper scripts `verify.py`, `stage.py` and `gate1.py` under `.remedy-wt/f295-r9-worker/` did the
  digest checks, copies, proofs and staging, as the block's sandbox rules require. They are not
  committed.
- No other departure from the block's commit sequence (C1 to C5, gates, push) or its constraints.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if present, write the handoff and stop.
2. Phase 1 rule 2: the Open PR Gate; no pull request is open for this branch yet.
3. Phase 1 rule 4: the reviewer reviews round 9 and books its verdict and the resolution of R-1145
   in the next round's first commit.
4. T003, second part: which command answers each decision kind under `--json`, the budget raise and
   the hunk decision first.

Operator questions open: 0.
Open findings: 4 (R-1145 Medium, owned by F295, repaired by this round; R-1138, R-1139 and R-1143 Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 (block copy, three record copies, append proofs, numstat) | done | `af749f212` |
| C2 (`exec_guard.py`, `stream_evidence.py`, R-1145 repair) | done | `927d233d3` |
| C3 (two spawn test files) | done | `ce552b87a` |
| C4 (two stdin-proof test files, T003) | done | `7d24833c8` |
| Gate 1 (status and byte comparisons) | done | porcelain empty, ten of ten equal |
| Gate 2 (ruff) | done | `All checks passed!` |
| Gate 3 (selection) | done | `4134 passed, 3 skipped`, exit 0 |
| Gate 4 (integrity check) | done | exit 0, `fail_count` 0 |
| Gate 5 (open finding ids) | done | `['R-1138', 'R-1139', 'R-1143', 'R-1145']` |
| C5 handback commit | done | this file |
| Push after C5 | pending | runs right after this commit, reported in the worker's final reply |
