── STEP T001/2 — F261 — ROUND 2 ──
Goal: Book round 1's PASS and register R-0891; then land T001's renames `do job-promote` to
`job apply` and `do job-run` to `job run`, one commit each, by applying two edit tables.

Base commit: `0fbe97c1`, on `feature/f261-cli-vocabulary-v2`. SESSION 1 of F261. Read
AGENTS.md, docs/agents/self_drive_protocol.md and DECISION F261 D1 in `.agent/decisions.md`.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block is a run
of a single repeated character, and every box-drawing rule inside the STEP and SLICE header
lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)` and `$?` in a compound command are refused by form, so write such checks
as Python scripts under `.remedy-wt/f261r2w/`; a pipe into `tail` hides pytest's exit code. The
editable install resolves `apps` and `packages` to the PRIMARY checkout, so a pytest run inside a
worktree goes through a runner script that changes into the worktree, puts it first on
`sys.path` and in `PYTHONPATH`, and asserts `apps.cli.command_catalog` loaded from inside it.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f261-r2.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE BOOKKEEPING COMMIT: `.agent/plan.md` becomes slice PLAN2; slice RECORD2 is appended to
    `.agent/live_review.md`; slice SLIP2 is appended to `.agent/prose_slips.md`
C2  RENAME A: copy `.remedy-wt/f261-block/f261-r2-rename-a.jsonl` to
    `.agent/authored/f261-r2-rename-a.jsonl`, then apply it per THE EDIT TABLES, in one commit
C3  RENAME B: the same with `f261-r2-rename-b.jsonl`, in one commit
C4  `.agent/handoff.md`, the handback; then `git push origin feature/f261-cli-vocabulary-v2`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f261-r2.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md` and `.agent/prose_slips.md`. C2 and C3: each table's own carrier path
and the paths its lines name. C4: `.agent/handoff.md`.

## THE EDIT TABLES

Each carrier holds one JSON array per line, `[path, old, new, count]`. The sha256 of
`f261-r2-rename-a.jsonl` is `71f42b5d936f21ed730bea12a3eccb90fcf913cc939a9b3044f7b39aa68503b3`
and that of `f261-r2-rename-b.jsonl` is
`bb8e4ff2e0a16065cb4fbdfbfd08e7929c3cc69d47a3ec237144f0445315625b`; verify each before copying.
Apply the lines strictly in file order, each against the file as the previous lines left it:
open the path with `encoding="utf-8", newline=""`, require the number of occurrences of `old` to
equal `count` exactly, and replace every occurrence with `new`. A count that differs is a STOP:
touch nothing further, commit nothing of that table, and hand back with the line and both counts.
The tables are the reviewer's measured dry run: rename A converts every dependent of
`do.job-promote`, and rename B every dependent of `do.job-run`, adds both pairs to
`TestRenamedCommands`, makes the F114 paragraph of `README.md` name `job resume`, and renames
`test_job_run_is_expensive` and `test_job_run_has_a_yes_flag_to_skip_the_cost_confirmation`
after `job resume`. Neither table touches `do promote`, the `promote` identifiers, or the
`do job-flow` step labels.

## The appends

RECORD2 and SLIP2 each begin with an empty line, and `.agent/live_review.md` and
`.agent/prose_slips.md` each end in a newline at `0fbe97c1`: an append is the file's bytes
followed by the slice's bytes, and nothing else.

## Constraints

1. NO SLICE AND NO TABLE IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C4, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f261r2w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f261-block/` and your
   own directory. `git worktree list` reads one row now; leave it so.
5. Every commit stays under 500 insertions.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 204 lines TOTAL and 162 lines of PROSE,
   against the caps of 490 and 400.
8. GATE ORDER. G1 and G2 after C1; G3 after C2; G4, G5 and G6 after C3 and before C4; G7 after
   C4 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r2.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; each committed carrier's sha256 equals its digest above.

G2 THE BOOKKEEPING, at C1. `.agent/plan.md` is byte-identical to PLAN2, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its `0fbe97c1` blob
followed by RECORD2, and `.agent/prose_slips.md` its `0fbe97c1` blob followed by SLIP2. Over
`.agent/live_review.md`: `^Gate: F\d+ R\d+ — ` reads 110 at `0fbe97c1` and 111 at C1, with
`Gate: F261 R1 — ` once; the open set by distinct id, every `^- R-\d+ — ` id minus every
`^Done: R-\d+ — ` id, reads 90 and 91, and C1's set minus the base set is exactly `R-0891`.

G3 RENAME A, at C2. `git show --numstat` of C2 names exactly
`.agent/authored/f261-r2-rename-a.jsonl`, `apps/cli/command_catalog.py`,
`apps/cli/commands/do_cmd.py`, `packages/orchestration/job_promote.py`,
`packages/orchestration/pingpong_job.py`, `tests/orchestration/test_job_promote.py`,
`tests/orchestration/test_job_task_runner.py`, `tests/orchestration/test_job_worktree_handoff.py`,
`tests/test_command_catalog.py` and `tests/test_observability_index.py`. `git rev-parse
<C2>:<dir>` equals the dry run: `apps` `0436a56ed63741607de0d9a3b2e81734f77efd13`, `packages`
`a6ad0e0d18d870db078a176a7819d1034e32bcac`, `tests` `bc90517f0d15228739cd0db35f5b2b90562b4c33`.

G4 RENAME B, at C3. `git show --numstat` of C3 names exactly
`.agent/authored/f261-r2-rename-b.jsonl` and these: `README.md`, `apps/cli/command_catalog.py`, `apps/cli/commands/do_cmd.py`, `apps/cli/commands/run_invocation.py`, `docs/system/core-product-spine-v0.md`, `packages/orchestration/job_evidence.py`, `packages/orchestration/pingpong_job.py`, `packages/orchestration/pingpong_provider.py`, `packages/orchestration/self_use_job.py`, `tests/cli/test_job_context_cmd.py`, `tests/cli/test_job_run_invocation_truth.py`, `tests/cli/test_stream_evidence_tristate.py`, `tests/cli/test_teach_cmd.py`, `tests/orchestration/test_f018_authority_integration.py`, `tests/orchestration/test_job_plan_state_reads.py`, `tests/orchestration/test_job_state_field.py`, `tests/orchestration/test_job_task_runner.py`, `tests/orchestration/test_job_worktree_handoff.py`, `tests/orchestration/test_job_worktree_integration.py`, `tests/orchestration/test_token_ledger.py`, `tests/test_command_catalog.py` and `tests/test_do_job_flow.py`. `git rev-parse <C3>:<dir>`
equals the dry run: `apps` `508aa87f54c3afd81cee3781d979fc7a2746a822`, `packages` `ffa8be243f09710b8fef1b2ab596197c5d1aaee2`,
`tests` `3ba748d7488de1014a8b87b775527d4a23110037`, `docs/system` `4ac761f148b5974f31ceb78edd7fa57ac969b817`, and
`README.md` `9d94d8b52787c3342330d1ff9d51e715c26dbdbe`; `scripts` equals its blob at `0fbe97c1`.
`git grep -n -e 'do\.job-promote' -e 'do\.job-run' -e _cmd_do_job_promote -e _cmd_do_job_run <C3>
-- ':!.agent' ':!.data' ':!docs/roadmap'` prints exactly two lines, both `RENAMED` pairs in
`tests/test_command_catalog.py`. `python3 -m ruff check` over every `.py` path of C2 and C3
exits 0.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f261r2w/wt <C3's sha>`, each run
through the runner over `tests/test_command_catalog.py` with `-rf --tb=no`. (a) CONTROL: must
exit 0. (b) In `apps/cli/command_catalog.py` the bytes `command_id="job.apply",`, whose count
there must read 1, become `command_id="do.job-promote",`: must exit 1 with
`TestRenamedCommands::test_no_old_id_is_left_in_the_catalog` among the failed nodes. Restore
with `git -C .remedy-wt/f261r2w/wt checkout -- apps/cli/command_catalog.py`. (c) In
`apps/cli/commands/do_cmd.py` the bytes `"job.run": lambda`, count 1, become `"job.rum": lambda`:
must exit 1 with `TestRenamedCommands::test_every_new_id_parses_from_its_words_and_has_a_handler`
among the failed nodes. Restore the same way. Report each exit code, summary line and every
failed node id; then `git worktree remove .remedy-wt/f261r2w/wt`.

G6 THE SUITES, in the primary checkout at C3, serially, each path its own
`python3 -B -m pytest -q -p no:randomly <path>` run: `tests/test_command_catalog.py`,
`tests/cli/`, `tests/test_grouped_cli.py`, `tests/test_do_job_flow.py`,
`tests/test_observability_index.py`, `tests/orchestration/test_job_promote.py`,
`tests/orchestration/test_job_task_runner.py`, `tests/orchestration/test_job_worktree_handoff.py`,
`tests/orchestration/test_f018_authority_integration.py`,
`tests/orchestration/test_job_plan_state_reads.py`, `tests/orchestration/test_job_state_field.py`,
`tests/orchestration/test_job_worktree_integration.py`, `tests/orchestration/test_token_ledger.py`,
`tests/docs/` and `tests/ui_server/test_dashboard_contract.py`. Each must exit 0; report each
summary line.

G7 THE TREE, after C4 and the push. `git status --porcelain` prints `''`; C0a to C4 are
single-parent commits in that order on `0fbe97c1`; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f261-cli-vocabulary-v2`; `git worktree list` prints one row.

## The handback, C4

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 1 of feature F261 · round 2 · rounds so far 2`, with one sentence of context
self-assessment. `## Commits` lists C0a to C3, each row's `+/-` cell equal to
`git show --numstat` of that commit; C4's own numbers appear nowhere, per item 31 of §3.
`## Verification` gives G1 to G6 with real exit codes. It states the open findings at 91 by
distinct id, R-0891 among them and owned by F261, with the High ids R-0803, R-0804, R-0806 and
R-0807, and `Operator questions open: 1`. Its `## Next` names, in order: Phase 1 rule 1; the
reviewer's verdict on round 2; the deletion of `do job-flow`.

── SLICE PLAN2 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN2 sha256=22ec52711c119bb8839c9f8b273f9877b977ae0a78d4063e149e9943e49aaf72
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 2 books round 1's PASS, registers R-0891, and lands T001's next two renames as two
commits, each applying an edit table the round saves under `.agent/authored/`: `do job-promote`
to `job apply`, then `do job-run` to `job run`. The second commit also makes the F114 paragraph
of `README.md` and two catalog test names say `job resume`, the repair R-0891 records.

## Next Steps

1. The deletion of `do job-flow` with its deletion paragraph, in two commits: the command and
   its tests, then the helpers only it used and the script that runs it.
2. The deletions of `do job-plan` and `do plan`, each with its deletion paragraph.
3. T002: `apply` replaces `promote`, `do promote` joins `job apply`, and `job show --full`
   absorbs the read commands and `do job-report`.
4. T003, the prune to D4; then T004, descriptions, role labels, help wrapping and the tests.

## Risks

- 91 findings are open by distinct id once R-0891 is registered; four are High, R-0803,
  R-0804, R-0806 and R-0807, all owned by F273.
- The canary `tests/cli/test_golden_path.py` names none of T001's commands; the rename guard
  `TestRenamedCommands` in `tests/test_command_catalog.py` and
  `tests/cli/test_advertised_commands.py` are the guards that can catch a T001 rename.
- `job apply` and `job run` keep the flags their old commands had; D4's shorter flag lists,
  such as `run <id> [--tasks n]`, are separate flag renames.
END PLAN2

── SLICE RECORD2 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD2 sha256=59b8853c097e10a93335ae57caa1dbc26a5c34f97eba12e4fea9e3cbcb97ccc0

Gate: F261 R1 — the F261 round 1 entry. VERDICT PASS. Written by the planner and reviewer of session 36 after reading the committed range `7cdde89b`..`0fbe97c1` and re-deriving the readings below; the worker's report was evidence for none of them. It is booked here by the first commit of round 2 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r1.md` at `997b3b9f` and `.agent/last_block.md` at `19e14e71` are byte-identical to the reviewer's scratch original, sha256 `2ec68048843a2743c30d9409b317f62079618343b38b9b077795b7627778a02c`. THE STATE: `.agent/plan.md` at `c092f505` equals PLAN1; at `e2dc892a`, `.agent/live_review.md` equals HEAD1 followed by the bytes of its `7cdde89b` blob from the `## Findings` line on and then RECORD1, `.agent/decisions.md` equals its `7cdde89b` blob followed by DEC1, and `.agent/candidates.md`, `docs/roadmap/features/T2_F273.md` and `docs/roadmap/features/T2_F261.md` each equal their `7cdde89b` blob with pairs PC, PA and PD applied; at `75c96592`, `docs/roadmap/STATUS.md` equals its `7cdde89b` blob with pair PS applied and `.agent/context.md` equals CTX1; every one of those files is unchanged through `0fbe97c1`. The open set reads 90 by distinct id at both ends, R-0889 resolved and R-0890 registered. THE RENAME: `1a8de8cd` changes exactly the paths its block's G5 names, 58 insertions and 35 deletions, and its `apps`, `packages`, `scripts`, `tests` and `docs/system` subtrees equal the reviewer's dry run, in which the reviewer's own mutations turned the guard red: changing the handler key `"job.evidence"` failed `TestRenamedCommands::test_every_new_id_parses_from_its_words_and_has_a_handler` and four tests of `tests/orchestration/test_job_evidence.py`, and putting `command_id="do.job-evidence",` back failed `TestRenamedCommands::test_no_old_id_is_left_in_the_catalog` among five. THE REVIEWER'S RUN in the primary checkout at `0fbe97c1` of `tests/test_command_catalog.py`, `tests/cli/test_advertised_commands.py`, `tests/cli/test_cli_ux.py`, `tests/orchestration/test_job_evidence.py`, `tests/orchestration/test_evidence_index.py`, `tests/orchestration/test_review_zip_hygiene.py`, `tests/docs/`, `tests/orchestration/test_roadmap_index.py`, `tests/orchestration/test_test_runner.py`, `tests/regression/test_resource_safety.py`, `tests/orchestration/test_integrity_gate.py`, `tests/ui_server/test_dashboard_contract.py` and `tests/cli/test_golden_path.py` read 800 passed. The worker's G8 exited 1 on its worktree count alone, because three of the reviewer's own dry-run worktrees were still registered; the reviewer removed them before this verdict, and the slip is in `.agent/prose_slips.md`.

- R-0891 — Low, `README.md` STILL NAMES `remedy job run` AS THE ONE COMMAND WIRED TO F114'S COST PREVIEW, WHICH `job resume` HAS CARRIED SINCE F275 ROUND 34, AND F261's RENAME OF `do job-run` TO `job run` MAKES THAT SENTENCE NAME A LIVE COMMAND WITHOUT A COST PREVIEW. Raised by the planner and reviewer of session 36 while preparing F261 round 2, after searching the open set for the defect under §3 item 30: no open finding describes it. THE DEFECT, read at `0fbe97c1`: the F114 paragraph of `README.md` says "`remedy job run` — the one command wired to it so far" and "Real cost bands for `job.run` are not calibrated yet", while `apps/cli/command_catalog.py` marks `job.resume` alone `is_expensive` and holds no `job.run`; `0523aa36`, F275 round 34's commit that moved the mark, the `--yes` and `--unattended` flags and the cost preview onto `job resume`, changed `docs/README.md` and `docs/guides/cost-preview-user-guide-v0.md` but not `README.md`. In `tests/test_command_catalog.py`, `test_job_run_is_expensive` and `test_job_run_has_a_yes_flag_to_skip_the_cost_confirmation` assert `job.resume` under names that say `job run`. WHY LOW: nothing executes wrongly, but the README tells a reader to expect a cost confirmation from a command that, once renamed, runs without one. WHY F261's: the rename that turns the stale sentence into a false one is F261's. FIX: the rename's own commit makes the README paragraph name `remedy job resume` and `job.resume` and renames the two tests after the command they assert. Owner: F261.
END RECORD2

── SLICE SLIP2 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIP2 sha256=1d8459ad9cc6fb125cd0e39d9577d24c5b59ac68ea33845cbd95f74956609957

2026-09-15 · F261 R1 · G8 of the round 1 block ordered `git worktree list` to print one row while three of the reviewer's own dry-run worktrees under `.remedy-wt/` were still registered, and constraint 4 of the same block forbade the worker to open them; G8 exited 1 on that check alone, the worker declared it, and the reviewer removed the worktrees before the verdict. THE RULE THAT FOLLOWS: before delegating a round whose gates count worktrees, the reviewer removes every worktree it or its helpers created and reads `git worktree list` at one row.
END SLIP2
