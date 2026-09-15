── STEP T001/3 — F261 — ROUND 3 ──
Goal: Book round 2's PASS and R-0891's resolution, register R-0892 and R-0893, record DECISION
F261 D2, and delete `do job-flow` in two commits by applying two tables; run the full suite once.

Base commit: `d58efc3a`, on `feature/f261-cli-vocabulary-v2`. SESSION 1 of F261. Read AGENTS.md,
docs/agents/self_drive_protocol.md, and DECISIONs F261 D1 and D2 once C1 has landed D2.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block is a run
of a single repeated character, and every box-drawing rule inside the STEP and SLICE header
lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)` and `$?` in a compound command are refused by form, so write such checks
as Python scripts under `.remedy-wt/f261r3w/`; a pipe into `tail` hides pytest's exit code. The
editable install resolves `apps` and `packages` to the PRIMARY checkout, so a pytest run inside a
worktree goes through a runner script that changes into the worktree, puts it first on
`sys.path` and in `PYTHONPATH`, and asserts `apps.cli.command_catalog` loaded from inside it.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f261-r3.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN3; slice RECORD3 is appended to
    `.agent/live_review.md` and slice DEC2 to `.agent/decisions.md`; pairs P268 and P271 are
    applied
C2  DELETION 1: copy `.remedy-wt/f261-block/f261-r3-delete-1.jsonl` to
    `.agent/authored/f261-r3-delete-1.jsonl` and apply it per THE TABLES, in one commit
C3  DELETION 2: the same with `f261-r3-delete-2.jsonl`, in one commit
C4  `.agent/handoff.md`, the handback; then `git push origin feature/f261-cli-vocabulary-v2`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f261-r3.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md`, `.agent/decisions.md`, `docs/roadmap/features/T2_F268.md` and
`docs/roadmap/features/T2_F271.md`. C2 and C3: each table's own carrier and the paths G3 and G4
name. C4: `.agent/handoff.md`.

## The pairs and the appends

P268 `docs/roadmap/features/T2_F268.md`: FROM slice P268-FROM, TO slice ACC268. P271
`docs/roadmap/features/T2_F271.md`: FROM slice P271-FROM, TO slice ACC271. Each FROM occurs
exactly once in its target at `d58efc3a`, and the containment test printed `TO contains FROM:
true` for both, so both are APPEND-shaped and are proved by whole-file equality, with no
FROM-zero count. RECORD3 and DEC2 each begin with an empty line, and both targets end in a
newline at `d58efc3a`: an append is the file's bytes followed by the slice's bytes.

## THE TABLES

Each carrier holds one JSON array per line. The sha256 of `f261-r3-delete-1.jsonl` is
`e42383ce3bb931d604543916c047533e290219500ef10d1c78e08083e1d4f335` and that of `f261-r3-delete-2.jsonl` is
`1b5bed3437f1d6d8aa019ad71781a259f00ddbea69b19829922b903f8453c9bc`; verify each before copying. Apply the rows strictly
in file order, each against the tree as the previous rows left it, from the repository root:
`["edit", path, old, new, count]` opens the path with `encoding="utf-8", newline=""`, requires
the number of occurrences of `old` to equal `count` exactly, and replaces every occurrence with
`new`; `["delete", path]` removes the file; `["move", src, dst]` renames the file, whose target
must not exist; `["create", path, content]` writes `content` to a path that must not exist, with
the same encoding and newline setting. A count that differs or a target that exists is a STOP:
touch nothing further, commit nothing of that table, and hand back with the row and the reading.
Stage each commit with `git add -A` after its table and its carrier. The tables are the
reviewer's measured dry run of DECISION F261 D2: table 1 deletes the command, its transcript
writer and its tests, moves the tests that outlive it, and adds `TestDeletedCommands` to
`tests/test_command_catalog.py`; table 2 deletes the functions only the command reached,
`scripts/remedy_self_job_flow.sh` and their tests, and renames `tests/test_do_job_flow.py` to
`tests/orchestration/test_review_package_status.py`.

## SPEC S — the suite, once, after G5 and before C4

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f261r3w/`. Report pytest's return code, the run's last output line, and every
distinct bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `.

## Constraints

1. NO SLICE AND NO TABLE IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C4, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f261r3w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f261-block/` and your
   own directory. `git worktree list` reads one row now; leave it so.
5. Every commit stays under 500 insertions by `git show --numstat`.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 269 lines TOTAL and 188 lines of PROSE,
   against the caps of 490 and 400.
8. GATE ORDER. G1 and G2 after C1; G3 after C2; G4 and G5 after C3; then SPEC S, whose result is
   G6; G7 after C4 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r3.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; each committed carrier's sha256 equals its digest above.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN3, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its `d58efc3a` blob
followed by RECORD3, `.agent/decisions.md` its `d58efc3a` blob followed by DEC2, and each of
P268's and P271's targets its `d58efc3a` blob with FROM's one occurrence replaced by TO. Over
`.agent/live_review.md`: `^Gate: F\d+ R\d+ — ` reads 111 at `d58efc3a` and 112 at C1, with
`Gate: F261 R2 — ` once; distinct `^- R-\d+ — ` ids 94 and 96; distinct `^Done: R-\d+ — ` ids 3
and 4; the open set by distinct id 91 and 92, with C1 minus base exactly `R-0892` and `R-0893`
and base minus C1 exactly `R-0891`.

G3 DELETION 1, at C2. `git diff --no-renames --name-only <C1> <C2>` prints exactly
`.agent/authored/f261-r3-delete-1.jsonl` and these: `apps/cli/command_catalog.py`, `apps/cli/commands/do_cmd.py`, `apps/cli/commands/run_invocation.py`, `packages/orchestration/missing_tests_gate.py`, `tests/cli/test_do_job_flow_review_base.py`, `tests/cli/test_job_evidence_review_base.py`, `tests/cli/test_stream_evidence_tristate.py`, `tests/orchestration/test_job_run_refs.py`, `tests/orchestration/test_relevant_regression_coverage.py`, `tests/orchestration/test_token_ledger.py`, `tests/test_command_catalog.py`, `tests/test_do_job_flow.py`, `tests/test_observability_index.py` and `tests/test_role_override_flags.py`. `git rev-parse <C2>:<dir>`
equals the dry run: `apps` `de1c5c2a65b9ed85bdbea6445080db55099b7bf8`, `packages` `8acfc00a946f8317000c034351b1c6dff8562891`,
`tests` `c9c06a59218fa3d5322e0c13c8af12cf563be0e5`; `scripts` equals its object at `d58efc3a` and `docs` its object
at C1.

G4 DELETION 2, at C3. `git diff --no-renames --name-only <C2> <C3>` prints exactly
`.agent/authored/f261-r3-delete-2.jsonl` and these: `apps/cli/commands/do_cmd.py`, `scripts/remedy_self_job_flow.sh`, `tests/orchestration/test_final_audit_evidence.py`, `tests/orchestration/test_job_evidence.py`, `tests/orchestration/test_pingpong_integration.py`, `tests/orchestration/test_prompt_trace.py`, `tests/orchestration/test_review_package_status.py`, `tests/orchestration/test_review_zip_hygiene.py`, `tests/orchestration/test_stream_evidence_integration.py` and `tests/test_do_job_flow.py`. `git rev-parse <C3>:<dir>`
equals the dry run: `apps` `56b0e4eba8dee36586b9d4cd727194bdf365d161`, `packages` `8acfc00a946f8317000c034351b1c6dff8562891`,
`scripts` `fb0b7d81f311c40c72f4ff1e30c51dd74efd4f06`, `tests` `59538d0caf01c71bd8000e909dd660509a106932`; `docs` equals its object at
C1 and `README.md` its object at `d58efc3a`. `git grep -n -w -e _cmd_do_job_flow -e _build_final_audit -e
_persist_job_flow_json -e _persist_command_transcript -e _build_agent_run_trace <C3> -- apps packages
scripts tests docs` prints nothing, and `git grep -n -F do.job-flow <C3> -- apps packages scripts tests
docs` prints exactly one line, the `DELETED` entry in `tests/test_command_catalog.py`.
`python3 -m ruff check` over every `.py` path of C2 and C3 that exists at C3 reports only the two
`I001` findings at lines 360 and 445 of `tests/orchestration/test_prompt_trace.py`, the same two
lines the reviewer's `python3 -m ruff check` of that file reads at `d58efc3a`.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f261r3w/wt <C3's sha>`, each run
through the runner over `tests/test_command_catalog.py` with `-rf --tb=no`. (a) CONTROL: must
exit 0. (b) In `apps/cli/commands/do_cmd.py` the bytes
`    "job.evidence": lambda args: _cmd_job_evidence(`, whose count there must read 1, become
`    "do.job-flow": lambda args: None,` followed by a newline and those same bytes: must exit 1
with `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table` among the failed
nodes. Restore with `git -C .remedy-wt/f261r3w/wt checkout -- apps/cli/commands/do_cmd.py`.
(c) In `apps/cli/command_catalog.py` the bytes `command_id="job.apply",`, count 1, become
`command_id="do.job-flow",`: must exit 1 with
`TestDeletedCommands::test_no_deleted_id_is_left_in_the_catalog` among the failed nodes. Restore
the same way. Report each exit code, summary line and every failed node id; then
`git worktree remove .remedy-wt/f261r3w/wt`.

G6 THE SUITE, SPEC S at C3: must exit 0 with no bad node; report the last output line.

G7 THE TREE, after C4 and the push. `git status --porcelain` prints `''`; C0a to C4 are
single-parent commits in that order on `d58efc3a`; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f261-cli-vocabulary-v2`; `git worktree list` prints one row.

## The handback, C4

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 1 of feature F261 · round 3 · rounds so far 3`, with one sentence of context
self-assessment. `## Commits` lists C0a to C3, each row's `+/-` cell equal to
`git show --numstat` of that commit; C4's own numbers appear nowhere, per item 31 of §3.
`## Verification` gives G1 to G6 with real exit codes. It states the open findings at 92 by
distinct id, R-0892 owned by F268 and R-0893 owned by F271 among them, with the High ids
R-0803, R-0804, R-0806 and R-0807, and `Operator questions open: 1`. Its `## Next` names, in
order: Phase 1 rule 1; the reviewer's verdict on round 3; the deletions of `do job-plan` and
`do plan`.

── SLICE PLAN3 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN3 sha256=d51df1e38221288348fb843b91859efcd591053d780684dd7da43aeec8ce6cce
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 3 books round 2's PASS and R-0891's resolution, registers R-0892 and R-0893, records
DECISION F261 D2, the deletion paragraph of `do job-flow`, and deletes that command in two
commits, each applying a table the round saves under `.agent/authored/`: first the command,
its transcript writer and its tests, with a guard that a deleted id stays deleted; then the
helpers only it used, `scripts/remedy_self_job_flow.sh`, and their tests. The worker runs the
full suite once after the second deletion.

## Next Steps

1. The deletions of `do job-plan` and `do plan`, each with its deletion paragraph and its id
   added to the deleted-command guard.
2. T002: `apply` replaces `promote`, `do promote` joins `job apply`, and `job show --full`
   absorbs the read commands and `do job-report`.
3. T003, the prune to D4; then T004, descriptions, role labels, help wrapping and the tests.

## Risks

- 92 findings are open by distinct id once this round's record lands; four are High, R-0803,
  R-0804, R-0806 and R-0807, all owned by F273.
- After the deletion no command writes the root artifacts that only `do job-flow` wrote and
  the review-package check requires of a provider-run package; R-0892 records it for F268,
  and the closure path, a manual completion bundle, is exempt from them.
- `packages/orchestration/agent_run_trace.py` keeps no production importer; R-0893 records it
  for F271.
END PLAN3

── SLICE RECORD3 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD3 sha256=824f58db6a1955f3ee8846ec7e072369d7aed968ad9849dec497880c31a9baf5

Gate: F261 R2 — the F261 round 2 entry. VERDICT PASS. Written by the planner and reviewer of session 36 after reading the committed range `0fbe97c1`..`d58efc3a` and re-deriving the readings below; the worker's report was evidence for none of them. It is booked here by the first commit of round 3 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r2.md` at `c200b024` and `.agent/last_block.md` at `29ccc3e2` are byte-identical to the reviewer's scratch original, sha256 `eda09a473f68d21415536f16a5ecfb8a7866e93eabfb946f26eaf5806c0669c9`, and the carriers `.agent/authored/f261-r2-rename-a.jsonl` at `9554eed8` and `.agent/authored/f261-r2-rename-b.jsonl` at `2027d797` are byte-identical to the reviewer's tables. THE STATE: at `8ad30506`, `.agent/plan.md` equals PLAN2, `.agent/live_review.md` equals its `0fbe97c1` blob followed by RECORD2, and `.agent/prose_slips.md` its `0fbe97c1` blob followed by SLIP2, each unchanged through `d58efc3a`. THE RENAMES: at `9554eed8` the `apps`, `packages`, `tests`, `scripts`, `docs/system` and `README.md` objects equal the reviewer's rename A dry run, and at `2027d797` they equal its rename B dry run, which is also the tree of `d58efc3a` for each of them; the reviewer's dry run had applied the helper's tables to a fresh worktree and reproduced the helper's two trees exactly before adding the README and test-name edits. In that dry run the reviewer's mutations turned the guard red: putting `command_id="do.job-promote",` back failed `TestRenamedCommands::test_no_old_id_is_left_in_the_catalog` among four, and changing the handler key `"job.run"` failed `TestRenamedCommands::test_every_new_id_parses_from_its_words_and_has_a_handler` alone. THE REVIEWER'S RUN in the primary checkout at `d58efc3a` of `tests/test_command_catalog.py`, `tests/cli/test_job_run_invocation_truth.py`, `tests/cli/test_cost_preview.py`, `tests/cli/test_advertised_commands.py`, `tests/orchestration/test_job_promote.py`, `tests/orchestration/test_job_task_runner.py`, `tests/test_observability_index.py`, `tests/docs/`, `tests/ui_server/test_dashboard_contract.py` and `tests/cli/test_golden_path.py` read 780 passed. The open set reads 91 by distinct id at `d58efc3a`.

Done: R-0891 — RESOLVED by F261 round 2. `2027d797` makes the F114 paragraph of `README.md` read "`remedy job resume` — the one command wired to it so far" and "Real cost bands for `job.resume` are not calibrated yet", and renames `test_job_run_is_expensive` and `test_job_run_has_a_yes_flag_to_skip_the_cost_confirmation` in `tests/test_command_catalog.py` to `test_job_resume_is_expensive` and `test_job_resume_has_a_yes_flag_to_skip_the_cost_confirmation`, bodies unchanged. Verified by the reviewer of session 36: the `README.md` blob at `2027d797` equals the reviewer's dry run, and no occurrence of `remedy job run` or `job.run` remains in that paragraph; `tests/test_command_catalog.py` passed within the reviewer's 780-passed run at `d58efc3a`, and `apps/cli/command_catalog.py` there still marks `job.resume` alone `is_expensive`, which `test_exactly_one_command_is_marked_expensive_so_far` asserts. No test pins the README sentence, so its repair is proved by the blob, not by a colour.

- R-0892 — Medium, ONCE `do job-flow` IS DELETED NO COMMAND WRITES THE ROOT ARTIFACTS ONLY IT WROTE, WHICH THE REVIEW-PACKAGE CHECK REQUIRES OF A PROVIDER-RUN EVIDENCE PACKAGE, SO A PACKAGE EXPORTED BY `job run` AND `job evidence` CAN NEVER PASS IT. Raised by the planner and reviewer of session 36 while preparing F261 round 3, after searching the open set for the defect under §3 item 30: no open finding describes it. THE DEFECT, read at `d58efc3a`: `REQUIRED_ROOT_ARTIFACTS` in `scripts/build_review_manifest.py` lists `job_flow.json`, `manifest.json`, `agent_run_trace.jsonl`, `agent_run_trace_summary.json`, `prompt_trace_summary.json` and `command_transcript.json`, and every missing one is recorded as an error unless the package is a manual completion, which `MANUAL_COMPLETION_EXEMPT_ROOT_ARTIFACTS` exempts; the candidate check in `scripts/make_review_zip.sh` requires the same six. Under `apps/` and `packages/` the only writers of `job_flow.json`, `command_transcript.json`, `agent_run_trace.jsonl` and `agent_run_trace_summary.json` are functions in `apps/cli/commands/do_cmd.py` reachable only from `_cmd_do_job_flow`, which DECISION F261 D2 deletes. WHY MEDIUM: an operator who runs a job and exports its evidence gets a package the review-package check calls incomplete, and nothing short of the closure's manual completion bundle yields one it accepts; the readers are kept, because relaxing a trust check to make packages pass that fail today is a change to the check, not a deletion. WHY F268's: F268's T001 builds the one sequence of plan, run and stop before apply that `do job-flow` was, so the evidence its runs export is where these artifacts are produced again or where the check is re-ruled. FIX: a provider run through F268's flow exports a package that passes `scripts/build_review_manifest.py`'s required-artifact check, a test builds one from a fake-provider run, and `.claude/skills/remedy-evidence-review/SKILL.md`, which still describes `job_flow.json` and `_build_final_audit`, describes the heir's package. Owner: F268.

- R-0893 — Low, `packages/orchestration/agent_run_trace.py` KEEPS NO PRODUCTION IMPORTER ONCE `do job-flow` IS DELETED. Raised by the planner and reviewer of session 36 while preparing F261 round 3, after searching the open set under §3 item 30: no open finding describes it. THE DEFECT, read at `d58efc3a`: the module's only importers under `apps/`, `packages/` and `scripts/` are four imports inside `apps/cli/commands/do_cmd.py`, all within `_cmd_do_job_flow` and `_build_agent_run_trace`, which DECISION F261 D2 deletes, while `tests/orchestration/test_agent_run_trace.py`, `tests/orchestration/test_stream_evidence_integration.py` and `tests/orchestration/import_reachability_allowlist.txt` keep naming it. WHY LOW: nothing runs wrongly; the module is dead code a reader may take for a live producer of `agent_run_trace.jsonl`. WHY F271's: F271 owns reachability and replace-is-delete, and deleting the module reaches its tests, the reachability allowlist and the cockpit's humanized catalog keys, which is wider than the command deletion D2 performs. FIX: delete the module with its tests, its allowlist line and the catalog keys only it sources, or name the production importer that makes it live. Owner: F271.
END RECORD3

── SLICE DEC2 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC2 sha256=16f52ed18516c9d0035533bf83c4cfb0314c80c4191bdcd41f0e0dda566beaf3

## DECISION F261 D2 (2026-09-15, F261 round 3) — the deletion paragraph of `do job-flow`: the command, the functions only it reached and its starter script go, the package readers stay, and the consequences are registered

CONTEXT. DECISION F261 D1 ordered `do job-flow` deleted in two commits with the deletion paragraph DECISION amend0905-vocab D3 requires: one dated paragraph naming what is deleted and, per item, the feature that inherited its idea, so that no later session rebuilds it. This is that paragraph. It also corrects D1 where the measurement contradicted it.

WHAT IS DELETED, measured at `d58efc3a` by an `ast` call graph over `apps/cli/commands/do_cmd.py` rooted at every other handler-table entry, which the reviewer's research helper built, and re-read by the reviewer with `git grep`, which finds each name below in that file at `d58efc3a` and none of them under `apps/`, `packages/`, `scripts/`, `tests/` or `docs/` in the reviewer's dry-run tree of the round: the catalog entry `do.job-flow` and its handler-table entry; `_cmd_do_job_flow`; and the functions reachable only from it, `_build_next_approve_command`, `_build_next_approve_command_safe`, `_build_job_token_summary`, `_effective_timeout_sec`, `_build_timeout_hint`, `_read_final_verifier`, `_read_gate_report`, `_read_token_truth`, `_build_final_audit`, `_sanitize_shareable_paths`, `_persist_evidence_index`, `_persist_job_flow_json`, `_persist_command_transcript`, `_persist_observability_index`, `_print_token_summary`, `_print_blocked_diagnostics`, `_print_final_audit`, `_load_prompt_trace_index` and `_build_agent_run_trace`; `scripts/remedy_self_job_flow.sh`, which runs the command; and every test that tests only those. `_index_job_evidence`, `_resolve_cli_role_configs` and `_validate_role_override` are shared with `job evidence` and `job run` and stay.

THE HEIRS. The sequence of plan, run, report, evidence and an apply dry run, and the next-approve hint, belong to F268's T001, `remedy do <order>` stopping before apply, whose `--apply` is `job apply --approve`; this corrects D1, which named F268 only as the heir of `do plan` and `do job-plan`. The token summary belongs to the F103 ledger that `job run` mirrors into; the final audit and its readers belong to the `final_verifier_report.json` and gate files `job evidence` exports; the evidence index belongs to `_index_job_evidence` under `job evidence`; the observability index belongs to `scripts/build_observability_index.py`, which `scripts/make_review_zip.sh` runs; the agent run trace belongs to the run events and live feed of F004, F008 and F021; the starter script belongs to the self-use runner of F257 and F258. The timeout hint, the path sanitizer and the writers of `job_flow.json` and `command_transcript.json` have no heir.

CHOSEN, FIRST: THE PACKAGE READERS STAY. `scripts/build_review_manifest.py` and `scripts/make_review_zip.sh` keep requiring the root artifacts only `do job-flow` wrote, because they also validate packages that already exist, and dropping a requirement would make packages pass that fail today, which is a change to a trust check rather than a deletion. The consequence, that no provider-run package can pass until F268's flow produces those artifacts again or the check is re-ruled, is R-0892. ALTERNATIVE: drop those artifacts from the required lists in the same commit, rejected for that reason.

CHOSEN, SECOND: `packages/orchestration/agent_run_trace.py` STAYS FOR NOW. Its only production importers die with the command, but deleting it reaches its test files, the reachability allowlist and the cockpit's humanized catalog keys, which is wider than a command deletion; R-0893 routes it to F271.

CHOSEN, THIRD: THE SPLIT D1 ORDERED MOVES. `_persist_command_transcript` goes in the first commit with the command, because its literal `remedy do job-flow` is an advertised command string that `tests/cli/test_advertised_commands.py` fails on once the command is gone. And `tests/test_do_job_flow.py` survives the first commit, holding the package-status tests that outlive the command, and is renamed to `tests/orchestration/test_review_package_status.py` in the second, because git records a rename below half similarity as an addition, which in the first commit would breach the 500-insertion cap. The `job run` role-flag tests move to `tests/test_role_override_flags.py`, `tests/cli/test_do_job_flow_review_base.py` becomes `tests/cli/test_job_evidence_review_base.py`, and the map in `packages/orchestration/missing_tests_gate.py` points at the moved file.

CHOSEN, FOURTH: A DELETED-COMMAND GUARD. `TestDeletedCommands` in `tests/test_command_catalog.py` fails when a deleted id is back in the catalog or in the dispatch table. The research helper measured that re-adding a `do.job-flow` catalog entry without it turned nothing in the full suite red, and in the reviewer's dry run a `do.job-flow` handler-table entry failed `test_no_deleted_id_is_left_in_the_dispatch_table` and a catalog id changed to `do.job-flow` failed `test_no_deleted_id_is_left_in_the_catalog`.

CONSEQUENCE. A bare `remedy do job-flow` becomes a `do run` goal, as D1's fifth ruling accepts, and `remedy do job-flow --job-file <path>` is read as `remedy do run job-flow --job-file <path>`, whose catalog entry declares no `--job-file`. HOW TO REVERSE: restore the command and its functions from the parent of the round's first deletion commit, and delete this section and the registrations it names.
END DEC2

── SLICE P268-FROM ── target `docs/roadmap/features/T2_F268.md` ── FROM OF P268 ──
BEGIN P268-FROM sha256=6148d2051afa3b7d190fa315d83029c6421dbf7f8f27fe3aa9c4fdc28d37d9e7
- do inside a git repo attaches that repo without a flag; every Next: line in do/job
  show output carries real ids and paths, never angle-bracket placeholders (a test
  greps the rendered output for <job_id>, <path>, <mission>). (R-0811, operator
  tests.md run 2026-09-05).
END P268-FROM

── SLICE ACC268 ── target `docs/roadmap/features/T2_F268.md` ── TO OF P268 ──
BEGIN ACC268 sha256=6c5aaacffc36b0938e58b92a66a761ebbaf2c2cdc6e349f0ccbd44880f502b6d
- do inside a git repo attaches that repo without a flag; every Next: line in do/job
  show output carries real ids and paths, never angle-bracket placeholders (a test
  greps the rendered output for <job_id>, <path>, <mission>). (R-0811, operator
  tests.md run 2026-09-05).
- R-0892 carries a resolution line: a provider run through this feature's flow exports an
  evidence package that passes the required-artifact check of
  `scripts/build_review_manifest.py`, and a test builds one from a fake-provider run.
END ACC268

── SLICE P271-FROM ── target `docs/roadmap/features/T2_F271.md` ── FROM OF P271 ──
BEGIN P271-FROM sha256=ed23caf57f9272ca351f69616560205ec0e1a9f48c0360e9e3bf7e5d4dfa649d
- `docs/roadmap/STATUS_closure_protocol.md` carries precondition 7 and cites the
  AGENTS.md rule.
END P271-FROM

── SLICE ACC271 ── target `docs/roadmap/features/T2_F271.md` ── TO OF P271 ──
BEGIN ACC271 sha256=570ba746f2d9e5402279b4f2912355628d01fa51178ea7f0d4cf7ea5d2c8ff96
- `docs/roadmap/STATUS_closure_protocol.md` carries precondition 7 and cites the
  AGENTS.md rule.
- R-0893 carries a resolution line: `packages/orchestration/agent_run_trace.py` is deleted
  with its tests, its reachability-allowlist line and the catalog keys only it sources, or
  a production importer is named.
END ACC271
