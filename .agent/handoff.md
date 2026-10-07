# Handoff — F295 session 3, round 12: book round 11, resolve R-1148, land DECISION F295 D11's `extend` (R-1146 part one)

## Session

SESSION 3 of feature F295 · rounds 10 to 12 · rounds so far 12

Context self-assessment: "The reviewer's context is comfortable after three rounds; the session
continues."

Fortschritt: ~75 % (T001 and T002 landed · T003's stdin proof, R-1147's resume guard and R-1148
landed · R-1146's extend landed, review pending · abandon, R-1147's providers, the hunk decision
and T004 open; then the hardening stage and the closure) — Schätzung

## Range

Review of `6aec8d959`..`05eb87a5d`, plus this handback commit.

## Commits

### 87d0dab37 F295 R12 C1: book round 11, resolve R-1148, DECISION F295 D11, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f295-r12.md` | 187/0 (new) | byte copy of the round 12 block |
| `.agent/live_review.md` | 4/0 | append round 11's gate entry (PASS) and the resolution of R-1148, exactly as the reviewer prepared it |
| `.agent/decisions.md` | 10/0 | append DECISION F295 D11 |
| `.agent/plan.md` | 5/6 | rewrite to round 12's current step |

### 62e622d24 F295 R12 C2: the budget decision's answer and its readers (R-1146)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/budget_decision.py` | 185/0 (new) | DECISION F295 D11 (2) to (5): `answer_budget_decision(job, decision_id, option, answers, *, now)` — checks the decision id, whether it is already answered, the reason, that an answer was given, the unraisable floor, that every `--answer` parses, that the stop's own limit is among the answered ones (unless it names none), and that every answered limit strictly raises the job's current value; on success mutates `job.budgets` and `job.metadata["budget_decision_answers"]` without saving |
| `packages/orchestration/budget_resolution.py` | 26/0 | `parse_budget_limit(name, raw)`, built on the existing `_pos_int`/`_pos_float`/`_parse_deadline`, raising `BudgetConfigError` for any name outside the five D11 (1) limits |
| `packages/orchestration/decision_queue.py` | 59/1 | `budget_stop_answer(job)` and `open_budget_decision_id(job)` (DECISION F295 D11 (4)); `list_decisions` skips its budget decision while `budget_stop_answer` finds a record |
| `tests/orchestration/import_reachability_allowlist.txt` | 1/0 | the new module's line, in sorted place (reachable via `apps.cli.commands.decision`'s lazy import, itself reachable via `apps.cli.commands.__init__.collect_all_handlers`) |

### 5289f4303 F295 R12 C3: decision resolve answers a budget decision, and resume reads the answer (R-1146)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/decision.py` | 69/4 | `_is_budget_decision_id` helper; the `--answer` admission at the top of `_cmd_decision_resolve` also admits a budget decision id; one new `elif` branch beside `veto:`, calling `answer_budget_decision` with `now` the current UTC time, mapping each of the six refusal codes to one literal `fail(...)` call, saving the job with `save_job_plan` on success, and answering with D11 (3)'s JSON keys |
| `apps/cli/command_catalog.py` | 2/1 | `_ANSWER_OPT`'s help text names both uses: a bundled clarification and a raised budget limit |
| `apps/cli/commands/job.py` | 8/7 | `_resume_preview` and `_cmd_job_resume`'s `budget_stopped` branch now call `open_budget_decision_id(job)` instead of comparing `stop_source` |
| `packages/orchestration/checkpoints.py` | 8/7 | `decide_checkpoint_resume`'s fourth guard calls `open_budget_decision_id(job)`; its docstring and `_resume_preview`'s say an answered stop no longer holds the job |
| `tests/cli/test_decision_cmd.py` | 3/1 | `_PINNED_TOKENS` gains `invalid_budget`, `budget_limit_not_raised` and `budget_limit_not_raisable` |

### ba7ae7739 F295 R12 C4: unit tests of the budget answer, its readers and the resume guard (R-1146)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_budget_decision.py` | 256/0 (new) | 17 tests: extend records the answer and raises the limit; a later stop reopens the same decision id; `list_decisions` leaves an answered stop out and relists it after a later stop; 12 parametrized refusal cases, one per D11 (2) token, each asserting `job.budgets` and `job.metadata` are unchanged; a stop reason naming no limit accepts any raise; `parse_budget_limit` parses each of the five limits and refuses any other name |
| `tests/orchestration/test_resume_cli.py` | 52/0 | two tests appended to `TestBudgetStop`: an answered budget stop hands the job to the stub executor once; its dry-run preview reports `budget_stop` empty and `would_run` true |

### 05eb87a5d F295 R12 C5: a client answers a budget decision with extend and runs the job to its end (R-1146)

| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_decision_cmd.py` | 121/0 | `TestABudgetDecisionAnsweredThroughTheCommandLine`, in-process through `apps.cli.grouped.main` in a temporary git repository, with the same tripwires and `OllamaBuilder` stand-in as `tests.orchestration.test_resume_cli`'s command-line test: `remedy do ... --plan-only` then `remedy job run ... --deadline 2000-01-01T00:00:00+00:00` stops the job; `decision resolve ... --reason extend --answer deadline=<...>` answers `ok` true, `outcome` `extended`, and the next `job run ... --json` completes the job; a second test answers `max_cost_usd=2` for the same deadline stop and gets `budget_limit_not_raised`, exit 1, the decision still listed |

### F295 R12 C6: handback (self-reference exception — committed by this same write)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file, rewritten in full per `docs/agents/handback_template.md` |

## External actions

None during the round before C6. After C6: `git push origin feature/f295-machine-client-contract-v1`;
its outcome is in the worker's final reply (write-once rule). No PR opened, no other `gh` command,
beyond the Open PR Gate check: `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
returned `[]` — no open PR for this branch.

## Verification

Gates ran once each, after C5 and before C6.

1. `git -C /home/decodeux/Repos/remedy status --porcelain` → empty output. Byte comparison of
   every file C1 wrote (`git show 87d0dab37:<path>`) against its prepared file, four of four equal
   (`.agent/authored/f295-r12.md` vs `block.md`, `.agent/live_review.md` vs `dry-live_review.md`,
   `.agent/decisions.md` vs `dry-decisions.md`, `.agent/plan.md` vs `dry-plan.md`).
2. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r12/run.py /home/decodeux/Repos/remedy 5
   python3 -m ruff check` followed by every Python file C2 to C5 touched (`apps/cli/command_catalog.py
   apps/cli/commands/decision.py apps/cli/commands/job.py packages/orchestration/budget_decision.py
   packages/orchestration/budget_resolution.py packages/orchestration/checkpoints.py
   packages/orchestration/decision_queue.py tests/cli/test_decision_cmd.py
   tests/orchestration/test_budget_decision.py tests/orchestration/test_resume_cli.py`):
   ```
   exit 0
   All checks passed!
   ```
3. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r12/run_selection.py /home/decodeux/Repos/remedy`
   ```
   exit 0
   SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
   SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
   SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
   5401 passed, 3 skipped in 127.09s (0:02:07)
   ```
   No FAILED, ERROR or `process(es) behind` line.
4. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r12/run.py /home/decodeux/Repos/remedy 3
   python3 -m apps.cli.main integrity check --json`
   ```
   exit 1
   {"check_count": 6, "checks": [{"message": "handlers=174", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "1 open blocker/high: R-1147", "name": "high_blockers_open", "status": "fail"}], "error": "integrity_failed", "fail_count": 1, "message": "integrity gate failed with 1 failing check(s)", "ok": false, "passed": false, "schema_version": 1, "version": 1}
   ```
   `fail_count` 1, the one failing check `high_blockers_open` reading `1 open blocker/high: R-1147`;
   R-1147 was booked before this round and stays open after this round by design (its provider half
   is still open).
5. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r12/run.py /home/decodeux/Repos/remedy 3
   python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
   ```
   exit 0
   ['R-1138', 'R-1139', 'R-1143', 'R-1146', 'R-1147', 'R-1149']
   ```
   R-1148 is resolved by this round's C1; R-1146 stays open until `abandon` lands (next round).

## Authored-text proofs

- `block.md` → `.agent/authored/f295-r12.md`: 187 lines / 187 lines, sha256
  `380042de0bfdd5a21155e89731634c34b8f87110ece26f61d6b438f02b35b576` / same, byte comparison equal.
- Every prepared file copied over its target (`dry-live_review.md`, `dry-decisions.md`,
  `dry-plan.md`): byte comparison equal, before the commit and again from the committed bytes in
  gate 1.
- Append proofs: `git show 6aec8d959:.agent/live_review.md` plus the bytes of
  `append-live_review.txt` equals the new file: `True`; the same for `.agent/decisions.md` with
  `append-decisions.txt`: `True`.
- Every prepared file's sha256 was read with Python before use and matched the block's value
  (`dry-live_review.md`, `dry-decisions.md`, `dry-plan.md`, `append-live_review.txt`,
  `append-decisions.txt`, and `block.md` itself, 187 lines, verified before any read of its text).
- `git diff --cached --numstat` before the C1 commit matched the block's cells: `187 0` (the
  authored copy), `10 0` (decisions), `4 0` (the ledger), `5 6` (the plan).

## Deviations & assumptions

- Attribution line: every commit of this round closes with
  `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`, the model this worker runs on.
- Helper scripts (`verify_block.py`, `verify_prepared.py`, `verify_c1.py`, `gate1_c1_compare.py`,
  `sanity_import_c2.py`, `sanity_answer_budget.py`, `sanity_list_decisions.py`,
  `sanity_cmd_decision.py`) under `.remedy-wt/f295-r12-worker/` did the digest checks, byte
  comparisons and the pre-commit functional sanity runs the block's sandbox rules require. They
  are not committed.
- Before staging C2, this worker ran `python3 -m ruff check` on the three touched modules directly
  (not through the block's `run.py` wrapper) and a functional sanity script exercising
  `parse_budget_limit`, `budget_stop_answer`, `open_budget_decision_id` and `answer_budget_decision`
  end-to-end, as pre-commit sanity checks only.
- Before staging C3, this worker ran `python3 -m ruff check` on the five touched files directly,
  plus the full existing `tests/orchestration/test_resume_cli.py` (45 passed) and
  `tests/cli/test_decision_cmd.py` (18 passed) to confirm the guard rewire broke nothing already
  landed, and an in-process sanity script driving `_cmd_decision_resolve`'s new branch directly
  (extend success, then a second call correctly refusing `decision_already_answered`).
- Before staging C4, this worker ran the new `tests/orchestration/test_budget_decision.py` alone
  (17 passed) and the whole of `tests/orchestration/test_resume_cli.py` (47 passed) directly, plus
  `ruff check` on both files.
- Before staging C5, this worker ran the new
  `TestABudgetDecisionAnsweredThroughTheCommandLine` class alone (2 passed), then the whole of
  `tests/cli/test_decision_cmd.py` (20 passed), plus `ruff check` on the file.
  These are additional to, not instead of, the five numbered gates above, each of which ran
  exactly once, in order, after C5 and before C6. No two test commands ran at once, no mutation
  red-proof was run, the full suite was never run via a second command (gate 3 is the one full
  selection run), and `REMEDY_TEST_MAX_WORKERS` was never set.
- C2 touched exactly the four paths the block named, no other module. The disk-floor limit
  (`min_free_disk_bytes`) is refused as `budget_limit_not_raisable` by checking the STOP REASON's
  own limit, independent of what `--answer` raises — a job stopped by the disk floor is refused
  even when the caller's `--answer` would otherwise validly raise some other limit, since D11 (2)
  states the disk floor is never raised per job at all.
- `--reason` for the budget branch is read as `str(reason or "")` exactly as the `veto:` branch
  reads its own `--reason`; an absent `--reason` therefore reads as the empty string and is
  refused `invalid_argument` (must be `extend`), never as a silent default.
- No other departure from the block's ordered commit sequence (C1 to C6, gates, push) or its
  constraints.

## Round verdicts

Rounds 1 to 5 and 7 to 11 PASS and round 6 FAIL, booked in the ledger (round 11 by this round's
C1). Round 12's verdict is the reviewer's to give and book in the next round's first commit.

## For the operator, in plain sentences

When a job stops because it ran out of budget, a person or a program can now give it more budget
with one command, `remedy decision resolve`, naming the limit to raise and its new value. Remedy
writes the new limit to the job, notes the answer, and the job can then be run on to its end.
Giving such a job up is the next round's work. Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): not present during this round; if it appears, finish the commit
   in hand, write the handoff and stop.
2. Phase 1 rule 2: the Open PR Gate; no pull request is open for this branch yet.
3. Phase 1 rule 4: the reviewer reviews round 12 and books its verdict in the next round's first
   commit.
4. R-1146, second part: the budget decision answered `abandon`.

Operator questions open: 0.
Open findings: 6 (R-1147 High and R-1146 Medium, owned by F295; R-1138, R-1139, R-1143 and R-1149
Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 (block copy, three record copies, append proofs, numstat) | done | `87d0dab37` |
| C2 (`budget_decision.py`, D11 (2) to (5)) | done | `62e622d24` |
| C3 (`decision resolve`'s budget branch, resume guard rewire, pinned tokens) | done | `5289f4303` |
| C4 (unit tests of the answer, its readers and the resume guard) | done | `ba7ae7739` |
| C5 (client end-to-end test: extend, then run to completion) | done | `05eb87a5d` |
| Gate 1 (status and byte comparisons) | done | porcelain empty, four of four equal |
| Gate 2 (ruff) | done | `All checks passed!` |
| Gate 3 (selection) | done | `5401 passed, 3 skipped`, exit 0 |
| Gate 4 (integrity check) | done | exit 1, `fail_count` 1, `high_blockers_open`: `1 open blocker/high: R-1147` |
| Gate 5 (open finding ids) | done | `['R-1138', 'R-1139', 'R-1143', 'R-1146', 'R-1147', 'R-1149']` |
| C6 handback commit | done | this file |
| Push after C6 | pending | runs right after this commit, reported in the worker's final reply |
