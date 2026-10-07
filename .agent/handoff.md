# Handoff — F295 session 3, round 10: book round 9, resolve R-1145, register R-1146 to R-1148, land DECISION F295 D9 (R-1147 part one)

## Session

SESSION 3 of feature F295 · round 10 · rounds so far 10

Context self-assessment: "The reviewer's context is comfortable after one round; the session
continues."

Fortschritt: ~70 % (T001 and T002 landed · T003's stdin proof landed · R-1147's resume guard
landed, review pending · R-1148, R-1146, R-1147's providers, the hunk decision and T004 open; then
the hardening stage and the closure) — Schätzung

## Range

Review of `5a3ba7cd4`..`44524f78f`, plus this handback commit.

## Commits

### 68d2e7943 F295 R10 C1: book round 9, resolve R-1145, register R-1146 to R-1148, DECISION F295 D9, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f295-r10.md` | 166/0 (new) | byte copy of the round 10 block |
| `.agent/live_review.md` | 10/0 | append round 9's gate entry (PASS), the resolution of R-1145 and the registration of R-1146, R-1147 and R-1148, exactly as the reviewer prepared them |
| `.agent/decisions.md` | 10/0 | append DECISION F295 D9 |
| `.agent/plan.md` | 14/8 | rewrite to round 10's current step |

### 100548861 F295 R10 C2: a job its budget stopped does not resume until its budget decision is answered (R-1147)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/decision_queue.py` | 7/2 | new public `budget_decision_id(request_id)`; `list_decisions` now names the budget decision through it, no behaviour change |
| `packages/orchestration/checkpoints.py` | 19/6 | `decide_checkpoint_resume` gains a fourth guard, run after the all-green check: a job whose `stop_source` is exactly `"budget"` is refused (`RESUME_REFUSED`, reason `budget_stopped`, detail naming the stop reason and the decision id) |
| `apps/cli/commands/job.py` | 30/1 | `_cmd_job_resume` renders that reason as `budget_decision_open`, exit 3, payload key `decision_id`; `_resume_preview`/`_print_resume_preview` gain `budget_stop` (placed after `plan_approval_gate`) and fold it into `would_run` and the text preview; the exit-code docstring line is updated |

### 44524f78f F295 R10 C3: tests that a budget stop holds job resume, its preview and the loop's guard (R-1147)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_resume_cli.py` | 210/0 | `TestBudgetStop` (8 tests: refusal + decision id, text refusal, fallback id, operator-stop still resumes, pending-stop-wins-over-budget, all-green-wins-over-budget, the loop's guard directly, the dry-run preview both JSON and text, and the no-budget-stop preview) and `TestBudgetStopThroughTheCommandLine` (1 test, in-process through `apps.cli.grouped.main`, with the model-call tripwires of `tests/cli/test_do_order_file.py` plus an `OllamaBuilder` tripwire, proving a machine client's `remedy job resume --yes --json` is refused before any provider is reached) |

### F295 R10 C4: handback (self-reference exception — committed by this same write)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file, rewritten in full per `docs/agents/handback_template.md` |

## External actions

None during the round before C4. After C4: `git push origin feature/f295-machine-client-contract-v1`;
its outcome is in the worker's final reply (write-once rule). No PR opened, no `gh` command, beyond
the Open PR Gate check (`gh pr list --state open ...` → `[]`, no open PR).

## Verification

Gates ran once each, after C3 and before C4.

1. `git -C /home/decodeux/Repos/remedy status --porcelain` → empty output. Byte comparison of every
   file C1 wrote (`git show 68d2e7943:<path>`) against its prepared file, four of four equal
   (`.agent/authored/f295-r10.md` vs `block.md`, `.agent/live_review.md` vs `dry-live_review.md`,
   `.agent/decisions.md` vs `dry-decisions.md`, `.agent/plan.md` vs `dry-plan.md`).
2. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r10/run.py /home/decodeux/Repos/remedy 5
   python3 -m ruff check packages/orchestration/decision_queue.py
   packages/orchestration/checkpoints.py apps/cli/commands/job.py
   tests/orchestration/test_resume_cli.py`
   ```
   exit 0
   All checks passed!
   ```
3. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r10/run_selection.py /home/decodeux/Repos/remedy`
   ```
   exit 0
   SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
   SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
   SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
   4722 passed, 3 skipped in 29.07s
   ```
   No FAILED, ERROR or `process(es) behind` line.
4. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r10/run.py /home/decodeux/Repos/remedy 3
   python3 -m apps.cli.main integrity check --json`
   ```
   exit 1
   {"check_count": 6, "checks": [{"message": "handlers=174", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "1 open blocker/high: R-1147", "name": "high_blockers_open", "status": "fail"}], "error": "integrity_failed", "fail_count": 1, "message": "integrity gate failed with 1 failing check(s)", "ok": false, "passed": false, "schema_version": 1, "version": 1}
   ```
   `fail_count` 1, the one failing check `high_blockers_open` reading `1 open blocker/high: R-1147`;
   R-1147 was booked by C1 and stays open after this round by design (its provider half is still
   open).
5. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r10/run.py /home/decodeux/Repos/remedy 3
   python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
   ```
   exit 0
   ['R-1138', 'R-1139', 'R-1143', 'R-1146', 'R-1147', 'R-1148']
   ```

## Authored-text proofs

- `block.md` → `.agent/authored/f295-r10.md`: 166 lines / 166 lines, sha256
  `c7c0d832ebf679dc4a798656b63a869ab6e1b8ac2faac0b016c9ce4eb503342e` / same, byte comparison equal.
- Every prepared file copied over its target (`dry-live_review.md`, `dry-decisions.md`,
  `dry-plan.md`): byte comparison equal, before the commit and again from the committed bytes in
  gate 1.
- Append proofs: `git show 5a3ba7cd4:.agent/live_review.md` plus the bytes of
  `append-live_review.txt` equals the new file: `True`; the same for `.agent/decisions.md` with
  `append-decisions.txt`: `True`.
- Every prepared file's sha256 was read with Python before use and matched the block's value
  (`dry-live_review.md`, `dry-decisions.md`, `dry-plan.md`, `append-live_review.txt`,
  `append-decisions.txt`, and `block.md` itself, 166 lines, verified before any read of its text).
- `git diff --cached --numstat` before the C1 commit matched the block's cells: `166 0`, `10 0`,
  `10 0`, `14 8`.

## Deviations & assumptions

- Attribution line: every commit of this round closes with
  `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`, the model this worker runs on.
- Helper scripts `verify_block.py`, `copy_c1.py`, `verify_prepared.py`, `append_proof.py`,
  `gate1_byte_compare.py` and `check_digest_lengths.py` under `.remedy-wt/f295-r10-worker/` did the
  digest checks, copies, append proofs and the gate-1 byte comparison the block's sandbox rules
  require. They are not committed.
- Before staging C2 and C3, this worker ran `python3 -m ruff check` directly (not through the
  block's `run.py` wrapper) and `python3 -B -m pytest -q tests/orchestration/test_resume_cli.py`
  (the single new test file, in three sequential invocations: the new non-CLI tests alone, the new
  CLI test alone, then the whole file) as pre-commit sanity checks on the code and tests being
  written. These are additional to, not instead of, the five numbered gates below, each of which
  ran exactly once, in order, after C3 and before C4, exactly as the block requires. No two test
  commands ran at once, and the full suite was never run.
- No other departure from the block's ordered commit sequence (C1 to C4, gates, push) or its
  constraints: C2 touched only `packages/orchestration/decision_queue.py`,
  `packages/orchestration/checkpoints.py` and `apps/cli/commands/job.py`; no new `except` clause, no
  new module, no catalog or docs change.

## Round verdicts

Rounds 1 to 5 and 7 to 9 PASS and round 6 FAIL, booked in the ledger (round 9 by this round's C1).
Round 10's verdict is the reviewer's to give and book in the next round's first commit.

## For the operator, in plain sentences

When a job stops because it used up its budget, the command that continues a stopped job now
refuses to run it and says which decision has to be answered first, both for a person and for a
program reading the JSON answer, and its preview says the same. Until now it ran such a job anyway.
Giving the job more budget, or giving it up, through that decision is the work of a later round.
Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): not present; if it appears, finish the commit in hand, write the
   handoff and stop.
2. Phase 1 rule 2: the Open PR Gate; no pull request is open for this branch yet
   (`gh pr list --state open ...` → `[]`).
3. Phase 1 rule 4: the reviewer reviews round 10 and books its verdict in the next round's first
   commit.
4. R-1148: a job `remedy do` plans writes its run manifest.

Operator questions open: 0.
Open findings: 6 (R-1147 High, R-1146 and R-1148 Medium, owned by F295; R-1138, R-1139 and R-1143
Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 (block copy, three record copies, append proofs, numstat) | done | `68d2e7943` |
| C2 (`decision_queue.py`, `checkpoints.py`, `job.py`, DECISION F295 D9) | done | `100548861` |
| C3 (budget-stop guard, preview and CLI tests) | done | `44524f78f` |
| Gate 1 (status and byte comparisons) | done | porcelain empty, four of four equal |
| Gate 2 (ruff) | done | `All checks passed!` |
| Gate 3 (selection) | done | `4722 passed, 3 skipped`, exit 0 |
| Gate 4 (integrity check) | done | exit 1, `fail_count` 1, `high_blockers_open`: `1 open blocker/high: R-1147` |
| Gate 5 (open finding ids) | done | `['R-1138', 'R-1139', 'R-1143', 'R-1146', 'R-1147', 'R-1148']` |
| C4 handback commit | done | this file |
| Push after C4 | pending | runs right after this commit, reported in the worker's final reply |
