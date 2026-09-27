STEP F028 R3 — BOOK ROUND 2, RESOLVE R-1076 AND REGISTER R-1077, RECORD D3, REPAIR R-1077, AND LAND THE SECOND HALF OF T002: the shortfall seed's three answers, its labels as a mapping of sentences, and the budget extension from the answer through the fold to the running job

GOAL
Round 2 passed. Book its gate entry, R-1076's resolution and R-1077's registration, and record
DECISION F028 D3. Repair R-1077. Then land the shortfall seed's answers: `drop` ends a shortfall
draft, `shrink_task` derives a new draft one band smaller, and `extend_budget` derives a
confirmable draft that carries a raised cost limit, which the confirmation copies, the fold
applies to the job's budgets, and `run_job` re-reads so the next safe point uses it.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests against S1 to S5. Read DECISIONS F028 D1, D2 and D3 in
`.agent/decisions.md` (D3 arrives with C2) and R-1077 in `.agent/live_review.md` first.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f028-r3-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f028-r3/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f028-r1-sim/`, `.remedy-wt/f028-r2-sim/`, `.remedy-wt/f028-r3-sim/`  The reviewer's
                                  simulation trees; do not touch them.
  `.remedy-wt/f028-review/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f028-r3-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f028-task-injection`, and `git log --oneline -1` must read `bdb65916`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f028-r3/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f028-r3-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 31 | 1168 | 4d3ce761c647b0ac8989aacc2de00aa082b6d203c18c47b7bc6046dd414b012e |
| records.diff | 67 | 12751 | 8c900898eb62dacdfcc3fb1915f91324bfd62f6a677f8fb205fc16cb031ae5d2 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `bdb65916`. It appends round 2's gate entry,
R-1076's `Done:` paragraph and R-1077's registration to `.agent/live_review.md`, and DECISION
F028 D3 to `.agent/decisions.md`.

THE SPECIFICATION — in `packages/orchestration/task_injection.py` unless named otherwise.
S1 R-1077. `confirmed_injections` raises `TaskInjectionError` for a record lacking, or holding
   with the wrong type, any of: `draft_id` (non-empty `str`), `task` (`dict`), `placement`
   (`dict` whose `rationale` and `basis` are `str`), `task_rationale`, `text`, `actor` and
   `confirmed_at` (each `str`), and `budget_extend_to_usd` when present (None, or an `int` or
   `float` above zero that is not a `bool`). `apply_injection_to_job` computes every value first
   and changes `job` only in its last statements, so any exception in it leaves `job` untouched.
S2 THE LABELS. `shortfall_decision_seed` answers `question` = `"Adding this task would go over
   the job's cost limit. What should happen?"` and `option_labels` as a `dict` keyed by option:
   `extend_budget` → `f"Raise the job's cost limit to ${extend_to_usd:.2f} and add the task."`;
   `shrink_task` → `f"Draft the task again one size smaller, as size {shrink_band}, and check
   the cost again."`, or `"The task is already the smallest size, so it cannot shrink."` when
   `shrink_band` is None; `drop` → `"Drop this task and add nothing to the job."`. Every other
   key is unchanged.
S3 THE ANSWER. `INJECTION_ANSWERS_DIRNAME = "injection_answers"`. `answer_injection_shortfall(job,
   draft_id, option, *, actor, budgets, counters, config, now=None, control_root_path=None) ->
   dict` NEVER raises for a refusal and answers `{"outcome": "refused", "code", "detail"}` from the
   first of: the terminal check (`job_terminal`); `read_injection_draft` refusing (its code); a
   record of another job (`draft_unknown`); a `status` other than `needs_decision`
   (`draft_not_in_shortfall`); `option` not in `SHORTFALL_OPTIONS` (`unknown_option`); an answer
   file already present for the draft (`already_answered`); `shrink_task` when the stored seed's
   `shrink_band` is None (`cannot_shrink`). A refusal writes nothing. Otherwise it mints the
   derived draft id (none for `drop`), publishes ONE create-only answer file in
   `INJECTION_ANSWERS_DIRNAME`, named as a draft file is, holding `injection_answer_v` 1, `job_id`,
   `draft_id`, `option`, `actor` (bounded), `answered_at` and `derived_draft_id`, a lost race
   answering `already_answered`; then: `drop` answers `{"outcome": "dropped", "job_id",
   "draft_id", "answered_at"}`; `shrink_task` publishes a derived draft whose task is the old task
   with `est_tokens_band` the seed's `shrink_band`, its check `injection_budget_check` over the
   caller's `budgets`, `counters` and `config` at that band, a shortfall making it
   `needs_decision` with a fresh seed and no token; `extend_budget` publishes a derived draft at
   the old band, status `confirmable`, carrying `budget_extend_to_usd` equal to the seed's
   `extend_to_usd`, its check computed over `budgets.model_copy(update={"max_cost_usd":
   extend_to_usd})`. A derived draft keeps the old record's task id, `placement`,
   `task_rationale`, `text`, `after` and `fence_conflicts`, takes the new id, the answering actor,
   `drafted_at` `now` and a fresh `expires_at`, and adds `derived_from` (the old id) and `answer`
   (the option); it is published through round 1's draft helper and answered in the shape
   `draft_task_injection` answers, plus those two keys and `budget_extend_to_usd`.
   `draft_task_injection`'s own drafts store and answer `budget_extend_to_usd` None.
S4 THE EXTENSION. `confirm_task_injection` copies the draft's `budget_extend_to_usd` (None when
   absent) into the confirmation. `apply_injection_to_job` then sets
   `job.budgets["max_cost_usd"]` to it when it is not None, `job.budgets` is a dict whose
   `max_cost_usd` is not None, and that current value is lower; it never creates a limit and never
   lowers one; the edit log's `injection` block gains `budget_extend_to_usd` (the record's value).
S5 THE RE-READ, in `packages/orchestration/pingpong_job.py`'s `run_job`: one local function
   `_fold_injections_here() -> bool` using `nonlocal _job_budgets`, defined after `_job_budgets`
   is first bound and before point (a), copies `job.budgets` (a shallow `dict` copy, or None),
   calls `_fold_task_injections(job, _control)` and answers True when it did; when `job.budgets`
   now differs from the copy it re-binds `_job_budgets = JobBudgets.model_validate(job.budgets)`,
   and a pydantic `ValidationError` there sets `JOB_BLOCKED` and
   `job.error = f"corrupt_budget_state: {exc}"`, persists and answers True; otherwise False. The
   four fold points call it instead of `_fold_task_injections`, point (d) keeping its length
   reading around the call.

THE TESTS
In `tests/orchestration/test_task_injection.py`: R-1077's fields, one record lacking each and one
holding each with a wrong type raising `TaskInjectionError`, and `apply_injection_to_job` leaving
`job` equal to a deep copy of itself when it raises; S2's question and three labels as exact
strings, with and without a smaller band — and the one existing assertion reading
`seed["option_labels"][seed["options"].index("shrink_task")]` rewritten to read
`seed["option_labels"]["shrink_task"]`, the only edit this round makes to a test round 1 wrote;
S3's refusal codes with nothing written; `drop`; `shrink_task` from `M` to `S` answering a
confirmable derived draft under the limit of round 1's budget test, and from `L` to `M` still a
shortfall; `extend_budget` answering a confirmable draft whose `budget_extend_to_usd` is 1.22 and
whose check shows no shortfall; a second answer refused `already_answered`; the old draft still
refused `draft_needs_decision` by `confirm_task_injection`; and S4 raising a limit of 1.00 to 1.22,
leaving 2.00 at 2.00, and leaving a job without a limit without one. In
`tests/orchestration/test_task_injection_runner.py`: a job with a cost limit of 1.00 whose
confirmed extended injection, confirmed before the run, reaches every call of
`packages.orchestration.budget_guard.predict_next_task_cost` made from the injected task's
pre-task safe point with `max_cost_usd` 1.22 (a wrapper around the real function records the
limit it receives), the job's record ending with a limit of 1.22; and a confirmed injection file
lacking `text` blocking the job with the `task_injection_control_error:` prefix.

BUNDLE — the commits are C1 to C7, in this order.
C1 — copy this block and the payloads: `.agent/authored/f028-r3-block.md`,
  `.agent/authored/f028-r3-records.diff`, `.agent/authored/f028-r3-plan.md`, by
  `shutil.copyfile`. Subject: `F028 R3 C1: copy round 3 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 98; STOP rather than commit at 500 or more.
C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F028 R3 C2: book round 2, resolve R-1076, register R-1077, record D3`
  Expected by `git show --numstat`: 45/0 decisions.md, 6/0 live_review.md, 9/9 plan.md.
C3 — S1 to S4: `packages/orchestration/task_injection.py`.
  Subject: `F028 R3 C3: repair R-1077, answer a shortfall three ways, and carry a budget extension into the fold`
C4 — S5: `packages/orchestration/pingpong_job.py`.
  Subject: `F028 R3 C4: re-read the job's budgets after every injection fold`
C5 — THE TESTS: the two test files. Subject: `F028 R3 C5: test the shortfall answers, the extension and R-1077`
C6 — THE TOOL: `.agent/authored/f028-r3-mutations.py`. Subject: `F028 R3 C6: add the round 3 mutation tool`
C7 — THE HANDBACK: `.agent/handoff.md`, rewritten, per `docs/agents/handback_template.md`.
  Subject: `F028 R3 C7: rewrite handoff for round 3`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by `git show --numstat`. MEASURE C3 and C5 before you
   commit them; a commit that would reach 500 is split into parts with their own subjects, each
   part leaving the selection of G4 green, and you say so.
3. The round's whole tracked path set is: the `.agent/authored/f028-r3-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/task_injection.py`, `packages/orchestration/pingpong_job.py`,
   `tests/orchestration/test_task_injection.py`,
   `tests/orchestration/test_task_injection_runner.py`, and `.agent/handoff.md`. Report the list
   `git diff --name-only bdb65916` measures after C7. Touch nothing else.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test THIS round
   wrote that is wrong may be corrected before C7, and the correction is declared. Any other
   existing test that goes red is never edited to pass; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives F028 one full-suite run, at its closure.
8. No `except Exception` in any production line this round writes.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C7 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table; then compare each `.agent/authored/f028-r3-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f028-r3/block.md`), read back with
 `git show <C1>:<path>`. One reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 317562 | 9551f5ecff40f5ce794ae75d932cb95ef610c0e032e28a723b297c0b31ced52d |
 | .agent/decisions.md | 2259543 | 37251d025f48e5b6410d1005621b43c5a9478d167ce745563ee31d481b0ca045 |
 | .agent/plan.md | 1168 | 4d3ce761c647b0ac8989aacc2de00aa082b6d203c18c47b7bc6046dd414b012e |
 Also `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's text at
 `bdb65916` and at C2 (the reviewer read `['R-1076']` and `['R-1077']`), and `git diff
 --name-only <C1> <C2>`, which must name exactly the paths of the table above.

G3 THE CODE — `python3 -m ruff check packages/orchestration/task_injection.py
 packages/orchestration/pingpong_job.py tests/orchestration/test_task_injection.py
 tests/orchestration/test_task_injection_runner.py` at C6, with its real exit code. Then quote
 from the diff the whole of `answer_injection_shortfall`, `_fold_injections_here` with its four
 call sites and three lines of context each, and the extension lines of `apply_injection_to_job`.

G4 THE TESTS — in the primary checkout at C6, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_task_injection.py tests/orchestration/test_task_injection_runner.py tests/orchestration/test_plan_editing.py tests/orchestration/test_plan_edit_execution.py tests/orchestration/test_task_edit_runtime.py tests/orchestration/test_task_veto.py tests/orchestration/test_task_veto_runner.py tests/orchestration/test_job_task_runner.py tests/orchestration/test_pause_resume.py tests/orchestration/test_pause_manifest.py tests/orchestration/test_job_stop_integration.py tests/orchestration/test_budget_stop_integration.py tests/orchestration/test_worktree_resume_cli.py tests/orchestration/test_job_plan.py tests/orchestration/test_mint_call_sites.py tests/orchestration/test_human_change_one_path.py tests/orchestration/test_pingpong_job_hunk_ledger.py tests/orchestration/test_unified_store_parity.py tests/orchestration/test_run_manifest_strict_boundaries.py tests/orchestration/test_budget_guard.py tests/orchestration/schemas/test_schemas.py tests/orchestration/test_structured_outputs.py tests/orchestration/test_import_reachability.py tests/test_imports.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_data_paths.py tests/test_subprocess_timeouts.py tests/test_no_interactive_guard.py tests/test_path_utils.py tests/regression/test_named_bugs.py tests/orchestration/test_development_artifact_boundary.py tests/test_no_orphan_modules.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection serially in the primary checkout at `bdb65916` and read
 `1593 passed, 7 skipped` at real exit code 0; the seven skips are the F252 quarantines. Report
 every `SKIPPED` line, the node counts of the two edited test files by `--collect-only -q` at
 `bdb65916` and at C6, and account for any difference from 1593 beyond the nodes the round adds.
 Then `python3 -m apps.cli.main integrity check --json`: all six checks `pass`, `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f028-r3-mutations.py` takes a worktree path and,
 for each mutation below, edits the named file INSIDE that worktree (asserting its FROM text
 occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/orchestration/test_task_injection.py tests/orchestration/test_task_injection_runner.py`
 from the worktree's root after purging its `__pycache__` directories, restores the bytes, and
 prints one line per mutation: label, exit code, failed count, failing node ids. An unmutated
 control runs first and last; it ends with `restored byte-identical: True` per file and
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.
  m1 `confirmed_injections` accepts a record lacking `text` (task_injection.py);
  m2 `apply_injection_to_job` lowers a higher limit to the extension (task_injection.py);
  m3 `apply_injection_to_job` creates a limit on a job that has none (task_injection.py);
  m4 `answer_injection_shortfall` skips the `needs_decision` status check (task_injection.py);
  m5 `shrink_task` derives its draft at the old band (task_injection.py);
  m6 `cannot_shrink` is checked only after the answer file is published (task_injection.py);
  m7 the `extend_budget` draft carries `budget_extend_to_usd` None (task_injection.py);
  m8 the `extend_budget` check is computed over the old limit (task_injection.py);
  m9 `confirm_task_injection` drops `budget_extend_to_usd` (task_injection.py);
  m10 the `extend_budget` label names no amount (task_injection.py);
  m11 `_fold_injections_here` never re-binds `_job_budgets` (pingpong_job.py).
 Run it: `git worktree add --detach .remedy-wt/f028-r3-mut <C6>`, then
 `python3 -B .agent/authored/f028-r3-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f028-r3-mut`
 and report its whole output. EVERY mutation must be red; one that stays green is reported as
 green, and you then add the test that catches it in C5 before C7 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f028-r3-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G6 TREE AND PUSH — after C7: `git status --porcelain`, empty; `git log --oneline -n 8`, showing
 C7 back to C1 and `bdb65916` in order (more lines if constraint 2 split a commit);
 `git worktree list | wc -l`, equal to your step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 to C6), every gate's real
output and exit code, the authored-text proofs, the item-status table AGENTS.md requires (one row
per commit, per gate and for R-1077), the deviations, and the next expected action. Name the
commit that lands R-1077's repair; write no `Done:` or `Landed:` line into the ledger. Your Session
section reads SESSION 1 of feature F028, round 3, and says in one sentence how much context you
had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 3, then the run-log event of a folded injection with its readers and `remedy job inject`.
State the open-findings count, 1 (R-1077, its repair awaiting review), and the operator-questions
count, 0.
