STEP F028 R4 — BOOK ROUND 3 AND RESOLVE R-1077, RECORD D4, AND LAND THE COMMAND LINE: `remedy job inject`, `job inject-confirm` and `job inject-answer`, the `--yes` audit mark, the shared budget and planner helpers, and the extension's amount computed at answer time

GOAL
Round 3 passed. Book its gate entry and R-1077's resolution and record DECISION F028 D4. Then
give the operator the command line: `job inject` drafts a task from their words (and with `--yes`
confirms it at once, marked as unseen), `job inject-confirm` confirms a draft, and `job
inject-answer` answers a shortfall; the command line reads its budget inputs and its planner
through two helpers the browser's command will share, and `extend_budget` computes its amount
again when the operator answers.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests against S1 to S5. Read DECISION F028 D4 in `.agent/decisions.md`
(it arrives with C2), and `apps/cli/commands/job_veto_cmd.py` with `tests/cli/test_job_veto.py`
whole: S4 and its tests copy their shape.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f028-r4-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f028-r4/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f028-r1-sim/` to `.remedy-wt/f028-r4-sim/`  The reviewer's simulation trees.
  `.remedy-wt/f028-review/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f028-r4-worker/`    YOURS for logs and scripts; create it if absent. All are
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
   `feature/f028-task-injection`, and `git log --oneline -1` must read `aa38800a`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f028-r4/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f028-r4-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 30 | 1117 | d0f9fdc2973dd87cf4c30e757eb7b5916db02f459deb776c9bcc0428cc191d49 |
| records.diff | 61 | 9995 | 2d18615311914a367e8ef7eae5e20ddcf75792c73d0071dcbbadf5ae08f9c9ad |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; it appends
round 3's gate entry and R-1077's `Done:` paragraph to `.agent/live_review.md` and DECISION F028
D4 to `.agent/decisions.md`.

THE SPECIFICATION
S1 THE AUDIT, in `packages/orchestration/task_injection.py`: `confirm_task_injection` gains the
   keyword `unseen: bool = False`, stored in the confirmation as `confirmed_unseen`
   (`bool(unseen)`); `_validate_confirmed_record` accepts `confirmed_unseen` absent or a `bool`
   and raises otherwise; `apply_injection_to_job`'s `injection` block carries
   `confirmed_unseen` (`record.get("confirmed_unseen", False)`).
S2 THE HELPERS, in the same module. `injection_budget_inputs(job) -> tuple` answers
   `(budgets, counters, config)`: `budgets` is None when `job.budgets` is None, else
   `JobBudgets.model_validate(job.budgets)`; `counters` is `BudgetCounters()` when
   `job.budget_actuals` is None, else `counters_from_persisted(decode_persisted_budget_actuals(
   job.budget_actuals, first_running_at=job.first_running_at or None))`; `config` is
   `resolve_predictive_budget_config(project_root=job.repo_path or None)`. A pydantic
   `ValidationError`, a `BudgetCounterError`, a `ValueError` or a `TypeError` from the first two
   raises `TaskInjectionRefused("budget_unreadable", ...)`, never a counter that claims nothing
   was spent. `injection_call_fn()` answers `intake.make_structured_call_fn(InjectedTaskDraft)`,
   importing `intake` inside its body.
S3 THE AMOUNT: `answer_injection_shortfall`'s `extend_budget` branch computes
   `injection_budget_check(budgets, counters, band=<the task's band>, config=config)` first and,
   when its `spent_cost_usd` and `expected_cost_usd` are both numbers, rounds their sum up to the
   cent exactly as `shortfall_decision_seed` does; the extension is the larger of that and the
   seed's `extend_to_usd` (the seed's alone when the sum is not computable). The derived draft's
   check is then computed over that extension.
S4 THE COMMANDS, a NEW FILE at `apps/cli/commands/job_inject_cmd.py`, its docstring naming F028
   and DECISION F028 D4 and classing the exit codes: `EXIT_USAGE = 2` for `text_required`,
   `text_too_long`, `text_invalid`, `unknown_task`, `unknown_option` and `cannot_shrink`;
   `EXIT_NOT_READY = 3` for `job_terminal`, `no_task_plan`, `plan_full`, `planner_unavailable`,
   `budget_unreadable`, `draft_unknown`, `draft_expired`, `draft_needs_decision`,
   `already_confirmed`, `draft_stale`, `draft_not_in_shortfall` and `already_answered`; 1 for
   any other refusal and for a job that does not exist; `CLI_ACTOR = "cli"`. It reaches the module
   as `from packages.orchestration import task_injection as ti` and calls `ti.injection_call_fn()`
   and `ti.injection_budget_inputs(job)` through that name. `job.inject` resolves `--after` with
   `job_plan_cmd._resolve_task_arg` and passes that entry's `inputs["plan"]["planned_id"]` (the
   argument unchanged when the entry has none), drafts, and prints for a draft the task's id,
   title, goal, every acceptance line, band, the placement's rationale, the budget arithmetic,
   every fence flag and the expiry, then the line
   `f"Confirm it with: remedy job inject-confirm {job_id} {token}"`; for a shortfall it prints the
   seed's question and arithmetic and, per option, its label and the line
   `f"  remedy job inject-answer {job_id} {draft_id} --option {option}"`. With `--yes` a drafted
   answer is confirmed at once with `unseen=True` and the confirmation printed, and a shortfall is
   refused as `draft_needs_decision` with exit 3 after the seed is printed. `job.inject-confirm`
   and `job.inject-answer` call `confirm_task_injection` and `answer_injection_shortfall` and
   print their answers; a derived draft prints as `job.inject` prints a draft. With `--json` each
   emits `emit_ok(job_id=job_id, **answer)`, `--yes` emitting `draft` and `confirmation`. Every
   refusal goes through `fail(code, detail, json_output=..., exit_code=..., job_id=job_id)`.
S5 THE REGISTRATION. Three `CommandEntry` items in `apps/cli/command_catalog.py`, placed directly
   after the `job.veto-task` entry, each `group_id="job"`, `action_class="write_metadata"`,
   `supports_json=True`, `may_mutate_repo=False`, `may_execute_commands=False`,
   `exit_codes=(0, 1, 2, 3)`: `job.inject` (args `_JOB_ID`, positional `text`, option `--after`,
   flag `--yes` with `is_flag=True`, `_JSON_OPT`), `job.inject-confirm` (`_JOB_ID`, positional
   `token`, `_JSON_OPT`) and `job.inject-answer` (`_JOB_ID`, positional `draft`, required option
   `--option`, `_JSON_OPT`). The reviewer measured, by wiring three stubs in its simulation tree,
   that `tests/docs/test_vocabulary.py` refuses a description holding the word task unless it
   also holds `job plan`, `step` or `run` (docs/system/vocabulary.md, "What counts as the
   meaning"), so every description and argument help that says task also says `job plan`. The
   module joins `apps/cli/commands/__init__.py`'s import list and its handler tuple, beside
   `job_veto_cmd`; `docs/guides/exit-codes.md` gains the rows `| \`remedy job inject\` | 3 |`,
   `| \`remedy job inject-confirm\` | 3 |` and `| \`remedy job inject-answer\` | 3 |` directly
   after the `job veto-task` row; `tests/orchestration/import_reachability_allowlist.txt` gains
   `apps.cli.commands.job_inject_cmd` between `apps.cli.commands.job_context_cmd` and
   `apps.cli.commands.job_pause_cmd`. The same probe measured these guards and no others red
   without those edits: the vocabulary test, the two exit-code tests of
   `tests/cli/test_exit_codes.py` (whose static reading requires the handler to REACH exit 3,
   as `job_veto_cmd` reaches it through a named constant), and the reachability guard.

THE TESTS
NEW FILE at `tests/cli/test_job_inject.py`, driven through `apps.cli.grouped.main` as
`tests/cli/test_job_veto.py` drives it, over a running job with a stored task plan, with
`task_injection.injection_call_fn` and, where a budget matters, `injection_budget_inputs`
monkeypatched: a draft's human output holding the confirm line with its token, and its JSON
envelope; `--after` by the planned id and by the entry id giving the same `depends_on`; `--yes`
confirming with `confirmed_unseen` True on disk and `draft` and `confirmation` in JSON; `--yes`
over a shortfall exiting 3 with the seed printed and nothing confirmed; `inject-confirm`
confirming; `inject-answer` for each option; and one exit code per class: `text_invalid` 2,
`unknown_option` 2, `planner_unavailable` 3, `draft_unknown` 3, `draft_unparseable` 1, a missing
job 1. In `tests/orchestration/test_task_injection.py`: `unseen` stored and logged, a mistyped
`confirmed_unseen` raising, S2's three branches and `budget_unreadable` for undecodable actuals and
for unreadable budgets, and S3 answering 1.30 where the seed said 1.22 after the counters grew to
$0.98 spent at band `M`, and the seed's amount where it is the larger.

BUNDLE — the commits are C1 to C7, in this order.
C1 — copy this block and the payloads: `.agent/authored/f028-r4-block.md`,
  `.agent/authored/f028-r4-records.diff`, `.agent/authored/f028-r4-plan.md`, by
  `shutil.copyfile`. Subject: `F028 R4 C1: copy round 4 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 91; STOP rather than commit at 500 or more.
C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F028 R4 C2: book round 3, resolve R-1077, record D4`
  Expected by `git show --numstat`: 41/0 decisions.md, 4/0 live_review.md, 9/10 plan.md.
C3 — S1 to S3: `packages/orchestration/task_injection.py`.
  Subject: `F028 R4 C3: mark an unseen confirmation, share the budget and planner inputs, and recompute an extension`
C4 — S4 and S5: `apps/cli/commands/job_inject_cmd.py`, `apps/cli/command_catalog.py`,
  `apps/cli/commands/__init__.py`, `docs/guides/exit-codes.md`,
  `tests/orchestration/import_reachability_allowlist.txt`.
  Subject: `F028 R4 C4: add remedy job inject, inject-confirm and inject-answer`
C5 — THE TESTS: the two test files. Subject: `F028 R4 C5: test the injection commands, the audit mark, the inputs and the amount`
C6 — THE TOOL: `.agent/authored/f028-r4-mutations.py`. Subject: `F028 R4 C6: add the round 4 mutation tool`
C7 — THE HANDBACK: `.agent/handoff.md`, rewritten, per `docs/agents/handback_template.md`.
  Subject: `F028 R4 C7: rewrite handoff for round 4`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by `git show --numstat`. MEASURE C3, C4 and C5 before
   you commit them; a commit that would reach 500 is split into parts with their own subjects,
   each part leaving the selection of G4 green, and you say so.
3. The round's whole tracked path set is: the `.agent/authored/f028-r4-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the six paths C3 and C4
   name, `tests/cli/test_job_inject.py`, `tests/orchestration/test_task_injection.py`, and
   `.agent/handoff.md`. Report the list `git diff --name-only aa38800a` measures after C7.
   Touch nothing else; in particular not `packages/orchestration/pingpong_job.py`,
   `packages/orchestration/ui_server.py`, anything under `apps/ui/`, or `README.md`.
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
 against the PAYLOADS table; then compare each `.agent/authored/f028-r4-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f028-r4/block.md`), read back with
 `git show <C1>:<path>`. One reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 321066 | 28649ba056ab1f7c4b3da41d3fda66ac7c066b45ad444c03801b9a528860fafc |
 | .agent/decisions.md | 2263097 | 52b1935b5398fcdb838f8be59a142c72c6c02863c2aa5081f66269319329124f |
 | .agent/plan.md | 1117 | d0f9fdc2973dd87cf4c30e757eb7b5916db02f459deb776c9bcc0428cc191d49 |
 Also `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's text at
 `aa38800a` and at C2 (the reviewer read `['R-1077']` and `[]`), and `git diff --name-only <C1>
 <C2>`, which must name exactly the paths of the table above.

G3 THE CODE — `python3 -m ruff check packages/orchestration/task_injection.py
 apps/cli/commands/job_inject_cmd.py apps/cli/command_catalog.py apps/cli/commands/__init__.py
 tests/cli/test_job_inject.py tests/orchestration/test_task_injection.py` at C6, with its real
 exit code. Then quote from the diff the three handlers whole and `injection_budget_inputs`.

G4 THE TESTS — in the primary checkout at C6, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/cli/test_job_inject.py tests/orchestration/test_task_injection.py tests/orchestration/test_task_injection_runner.py tests/cli/test_exit_codes.py tests/cli/test_advertised_commands.py tests/cli/test_job_veto.py tests/cli/test_cli_ux.py tests/test_command_catalog.py tests/test_grouped_cli.py tests/test_help_renderer.py tests/orchestration/test_dead_command_check.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_imports.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_data_paths.py tests/test_subprocess_timeouts.py tests/test_no_interactive_guard.py tests/test_path_utils.py tests/regression/test_named_bugs.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection less `tests/cli/test_job_inject.py`, serially, in the primary
 checkout at `aa38800a`, and read `1563 passed, 7 skipped` at real exit code 0; the seven skips
 are the F252 quarantines. Report every `SKIPPED` line, the node counts of the two edited test
 files by `--collect-only -q` at `aa38800a` and at C6, and account for any difference from 1563
 beyond the nodes the round adds (the catalog tests parametrized per command gain nodes for the
 three new entries; count them). Then `python3 -m apps.cli.main integrity check --json`: all six
 checks `pass`, `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f028-r4-mutations.py` takes a worktree path and,
 for each mutation below, edits the named file INSIDE that worktree (asserting its FROM text
 occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/cli/test_job_inject.py tests/orchestration/test_task_injection.py` from the worktree's root
 after purging its `__pycache__` directories, restores the bytes, and prints one line per
 mutation: label, exit code, failed count, failing node ids. An unmutated control runs first and
 last; it ends with `restored byte-identical: True` per file and
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.
  m1 `text_invalid` leaves the usage class (job_inject_cmd.py);
  m2 `draft_unknown` leaves the not-ready class (job_inject_cmd.py);
  m3 `--yes` over a shortfall exits 0 (job_inject_cmd.py);
  m4 `--yes` confirms with `unseen=False` (job_inject_cmd.py);
  m5 `--after` passes the entry's own id instead of its planned id (job_inject_cmd.py);
  m6 the drafted output omits the confirm line (job_inject_cmd.py);
  m7 the confirmation stores `confirmed_unseen` False always (task_injection.py);
  m8 the `injection` block omits `confirmed_unseen` (task_injection.py);
  m9 `extend_budget` takes the seed's amount alone (task_injection.py);
  m10 `injection_budget_inputs` answers `BudgetCounters()` for undecodable actuals (task_injection.py).
 Run it: `git worktree add --detach .remedy-wt/f028-r4-mut <C6>`, then
 `python3 -B .agent/authored/f028-r4-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f028-r4-mut`
 and report its whole output. EVERY mutation must be red; one that stays green is reported as
 green, and you then add the test that catches it in C5 before C7 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f028-r4-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G6 TREE AND PUSH — after C7: `git status --porcelain`, empty; `git log --oneline -n 8`, showing
 C7 back to C1 and `aa38800a` in order (more lines if constraint 2 split a commit);
 `git worktree list | wc -l`, equal to your step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 to C6), every gate's real
output and exit code, the authored-text proofs, the item-status table AGENTS.md requires (one row
per commit and per gate), the deviations, and the next expected action. Your Session section
reads SESSION 1 of feature F028, round 4, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 4, then the browser's command for the three steps, the run-log event of a folded injection
with every reader of its name, and the send module. State the open-findings count, 0, and the
operator-questions count, 0.
