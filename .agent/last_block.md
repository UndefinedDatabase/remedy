── STEP T003/8 — F261 — ROUND 20 ──
Goal: Book round 19's PASS, register R-0913, R-0914 and R-0915 for F273, record DECISION F261
D19, and delete `do repair-attest`, `do job-resume` and `do replan` in three commits by applying
three tables; run the suite once.

Base commit: `71cba20e`, on `feature/f261-cli-vocabulary-v2`. SESSION 4 of F261. Read AGENTS.md,
docs/agents/self_drive_protocol.md, `.agent/f261_t003_inventory.md`, and DECISION F261 D19 once
C1 has landed it.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block that is two or
more characters long is a run of a single repeated character, and every box-drawing rule inside the STEP and SLICE header
lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)` and `$?` in a compound command are refused by form, so write such checks
as Python scripts under `.remedy-wt/f261r20w/`, and never name a script after a standard-library
module; a pipe into `tail` hides pytest's exit code. The editable install resolves `apps` and
`packages` to the PRIMARY checkout, so a pytest run inside a worktree goes through a runner
script that changes into the worktree, puts it first on `sys.path` and in `PYTHONPATH`, and
asserts `apps.cli.grouped` loaded from inside it. Never call `run_job` or a runner yourself: a
job run started from inside a checkout creates a `remedy/job-*` branch in it.
`git branch --list 'remedy/job-*'` reads 16 lines now; keep it so. While a deletion is staged
but not committed, `test_every_enumerated_path_exists_in_this_repo` fails; run no suite then.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f261-r20.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN20; slice RECORD20 is appended to
    `.agent/live_review.md` and slice DEC19 to `.agent/decisions.md`; in `docs/roadmap/features/T2_F273.md` the bytes of slice P273-FROM
    are replaced by those of slice P273-TO
C2  `do repair-attest`: copy `.remedy-wt/f261-block/f261-r20-repair-attest.jsonl` to
    `.agent/authored/f261-r20-repair-attest.jsonl` and apply it per THE TABLES, in one commit
C3  `do job-resume`: the same with `f261-r20-job-resume.jsonl`, in one commit
C4  `do replan`: the same with `f261-r20-replan.jsonl`, in one commit
C5  `.agent/handoff.md`, the handback; then `git push origin feature/f261-cli-vocabulary-v2`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f261-r20.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md`, `.agent/decisions.md` and
`docs/roadmap/features/T2_F273.md`. C2 to C4: each table's own carrier and the paths G3 names.
C5: `.agent/handoff.md`.

## The appends and the pair

RECORD20 and DEC19 each begin with an empty line, and both targets end in a
newline at `71cba20e`: an append is the file's bytes followed by the slice's bytes, and nothing
else. The pair P273: TO contains FROM: false, so it is a REWRITE; P273-FROM occurs once
in `docs/roadmap/features/T2_F273.md` at `71cba20e`, and at C1 P273-FROM occurs 0 times and
P273-TO once.

## THE TABLES

Each carrier holds one JSON array per line. Their sha256 digests, to verify before copying:
`f261-r20-repair-attest.jsonl` `6595ebb1ffade5df75f5872466dfda79c786965e933459ef91f6284f0d81fe73`,
`f261-r20-job-resume.jsonl` `1de11feedd5dde3b2b4978df2e1da56ffb88205fa6efb0ceb4e05381a7de4eb4`,
`f261-r20-replan.jsonl` `8982ac33ac039403f315d213258d8e0b0e37a2d296f98e8e7504b574a41b9d33`.
Apply the rows strictly
in file order, each against the tree as the previous rows left it, from the repository root:
`["edit", path, old, new, count]` opens the path with `encoding="utf-8", newline=""`, requires
the number of occurrences of `old` to equal `count` exactly, and replaces every occurrence with
`new`; `["delete", path]` removes the file; `["move", src, dst]` renames the file, whose target
must not exist; `["create", path, content]` writes `content` to a path that must not exist, with
the same encoding and newline setting. A count that differs or a target that exists is a STOP:
touch nothing further, commit nothing of that table, and hand back with the row and the reading.
Stage each commit with `git add -A` after its table and its carrier. The tables are the
reviewer's measured dry run of DECISION F261 D19, applied on top of C1's record: the
repair-attest table its CHOSEN FIRST, the job-resume table its CHOSEN SECOND and the replan
table its CHOSEN THIRD.

## SPEC S — the suite, once, after G5 and before C5

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f261r20w/`. Report pytest's return code, the run's last output line, and every
distinct bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `.
Re-run each bad node alone, once, the same way, and report that return code beside it.

## Constraints

1. NO SLICE AND NO TABLE IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C5, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f261r20w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f261-block/` and your
   own directory. `git worktree list` reads one row now; leave it so. Create no symlink.
5. Every commit stays under 500 insertions, read as the first column of `git show --numstat
   --format= <commit>` with git's default rename detection.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph and no `Landed:` line.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 322 lines TOTAL and 233 lines of PROSE,
   against the caps of 490 and 400, where PROSE is every line that is not a line of slice CONTENT — the
   `BEGIN` and `END` marker lines count as prose.
8. GATE ORDER. G1 and G2 after C1; G3, G4 and G5 after C4; then SPEC S, whose result is G6; G7
   after C5 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r20.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; each committed carrier's sha256 equals its digest above.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN20, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its `71cba20e` blob
followed by RECORD20 and `.agent/decisions.md` its `71cba20e` blob followed by DEC19.
`docs/roadmap/features/T2_F273.md` equals its `71cba20e` blob with the pair P273 applied, with
the counts The appends and the pair give. Over `.agent/live_review.md`: `^Gate: F\d+ R\d+ — `
reads 128 at `71cba20e` and 129 at C1, with `Gate: F261 R19 — ` once at C1; distinct
`^- R-\d+ — ` ids 115 and 118, C1 minus base exactly `R-0913`, `R-0914` and `R-0915`; distinct `^Done: R-\d+ — ` ids 8
and 8; the open set by distinct id 107 and 110. `python3 -m pytest tests/docs/ -q` exits 0 at C1.

G3 THE TABLES, at C2, C3 and C4. `git diff --no-renames --name-only` from each commit's parent
prints exactly that commit's carrier and: at C2 `apps/cli/command_catalog.py`, `apps/cli/commands/do_cmd.py`, `packages/orchestration/repair_attest.py`, `tests/orchestration/test_repair_attest.py` and `tests/test_command_catalog.py`; at C3 `apps/cli/command_catalog.py`, `apps/cli/commands/do_cmd.py`, `apps/cli/commands/run_invocation.py`, `tests/cli/test_job_run_invocation_truth.py`, `tests/cli/test_stream_evidence_tristate.py`, `tests/orchestration/test_job_worktree_handoff.py` and `tests/test_command_catalog.py`; at C4
`apps/cli/command_catalog.py`, `apps/cli/commands/decision.py`, `apps/cli/commands/do_cmd.py`, `apps/cli/commands/job.py`, `tests/cli/test_plan_approval.py`, `tests/orchestration/test_prompt_trace.py`, `tests/orchestration/test_stream_evidence_integration.py` and `tests/test_command_catalog.py`.
`git rev-parse <commit>:<object>` equals the reviewer's dry run, which applied C1's
record before the tables, for `apps`, `tests`, `docs`, `scripts`, `packages` and `README.md` in
that order: C2 `7524164c6d1a22cc42084214fe90c5ade52ee9b6`, `799e2d94e7e902746494cc49a0bc69da5ff17728`, `0122c1025e45824dca796279be023995e45fb7d4`, `208d836b3d5d6532fe9354d9455ab71c67639ed2`, `c6d3df574ec0f9cb9f61ca05fdc5ccdd577ad4d9`, `666769d2b1a77cdb2ccdffc841f84f64d3eabdf8`; C3 `00706e15ef63770af935f60522718c674d317ee3`, `bad1d8e1e1330202aae36a08286575536e7ade6e`, `0122c1025e45824dca796279be023995e45fb7d4`, `208d836b3d5d6532fe9354d9455ab71c67639ed2`, `c6d3df574ec0f9cb9f61ca05fdc5ccdd577ad4d9`, `666769d2b1a77cdb2ccdffc841f84f64d3eabdf8`; C4 `6616756a89099aa89354731652ff95f2347fb1f5`, `49127a5cb0d840076d1dc9f46c95961a0338e5f2`, `0122c1025e45824dca796279be023995e45fb7d4`, `208d836b3d5d6532fe9354d9455ab71c67639ed2`, `c6d3df574ec0f9cb9f61ca05fdc5ccdd577ad4d9`, `666769d2b1a77cdb2ccdffc841f84f64d3eabdf8`.
Report each commit's insertions per constraint 5.

G4 THE SWEEP, at C4. `git grep -n -I -E '(^|[^.])repair-attest|(^|[^.])job-resume|do replan|_cmd_do_repair_attest|_cmd_do_job_resume|_cmd_do_replan|collect_diff_stat'
<C4> -- apps packages scripts tests docs README.md AGENTS.md .claude ':!docs/roadmap'` exits 1
and prints nothing; at `71cba20e` the same command exits 0 and names 11 files.
`python3 -m ruff check` over every `.py` path of C2 to C4 that still exists at C4 exits 0, except
`tests/orchestration/test_prompt_trace.py`, which reports the same two `I001` findings at
`71cba20e` and is reported with both readings rather than repaired in this round.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f261r20w/wt <C4's sha>`, each run
through the runner over `tests/test_command_catalog.py`, `tests/cli/test_cli_ux.py`,
`tests/test_grouped_cli.py`, `tests/orchestration/test_import_reachability.py` and
`tests/cli/test_advertised_commands.py` with `-rf --tb=no`. Mutation <n> is in the file its line
below names, replaces the bytes of slice MUT-<n>-FROM, whose count there must read 1, with those
of slice MUT-<n>-TO, and is restored with `git -C .remedy-wt/f261r20w/wt checkout -- <that
file>`. (a) CONTROL: must exit 0. Each of (1) to (5) must exit 1 with the named node among the
failed nodes:
(1) `apps/cli/commands/do_cmd.py`, a `do.repair-attest` handler row, (2) the same file, a
`do.job-resume` handler row, and (3) the same file, a `do.replan` handler row: each
`TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table`; (4)
`apps/cli/command_catalog.py`, a `related=` naming `do.job-resume`:
`TestCatalogIntegrity::test_every_related_reference_resolves_to_a_live_command`; (5)
`apps/cli/commands/decision.py`, the `do replan` line restored after the rejection:
`test_every_advertised_command_exists_in_the_catalog`.
Report each exit code, summary line and number of failed nodes; then
`git worktree remove --force .remedy-wt/f261r20w/wt` and read `git branch --list 'remedy/job-*'`.

G6 THE SUITE, SPEC S at C4: must exit 0 with no bad node; report the last output line. A bad
node whose lone re-run exits 0 is reported as such with both readings, and is not a STOP; a bad
node whose lone re-run fails is.

G7 THE TREE, after C5 and the push. `git status --porcelain` prints `''`; C0a to C5 are
single-parent commits in that order on `71cba20e`; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f261-cli-vocabulary-v2`; `git worktree list` prints one row, and
`git branch --list 'remedy/job-*'` prints 16 lines.

## The handback, C5

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 4 of feature F261 · round 20 · rounds so far 20`, with one sentence of context
self-assessment. `## Commits` lists C0a to C4, each row's `+/-` cell equal to constraint 5's
reading of that commit and its deletions column; C5's own numbers appear nowhere, per item 31 of
§3. `## Verification` gives G1 to G6 with real exit codes. It states the open findings at 110 by
distinct id, with the High ids R-0803, R-0804 and R-0807, and `Operator questions open: 0`. Its
`## Next` names, in order: Phase 1 rule 1; the reviewer's verdict on round 20; the `do
continue` hints with the command and `do_continue.py`, with R-0900, as the inventory proposes.

── SLICE PLAN20 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN20 sha256=1226ca7ecd76873ac1cbc9a7ffef4620139420d5cbd0f66641bd407b76c7b535
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 20 continues T003. It books round 19's PASS, registers R-0913, R-0914 and R-0915 for F273
and records DECISION F261 D19, then deletes `do repair-attest`, `do job-resume` and `do replan`,
one table per commit.

## Next Steps

1. The `do continue` hints, then the command and `do_continue.py`, with R-0900, as
   `.agent/f261_t003_inventory.md` proposes.
2. The rest of T003 in the inventory's order, each round re-measured before it is authored,
   with R-0767 and R-0894.
3. `job budget <id> set` over the run-contract budget fields and the token budget profile, the
   word DECISION amend0905-vocab D4 gives those writes, with R-0906 and R-0909.
4. T004, which owes the visible group order of D4 and the README quickstart of R-0895.

## Risks

- 107 findings are open by distinct id before this round's record and 110 after it; three are
  High, R-0803, R-0804 and R-0807.
- The feature's soft limit of 25 rounds leaves five after this one, and the inventory proposes
  more than five; the session that reaches the limit owes the scope report and executes the
  split-and-close default of operator amendment amend0905-throughput.
- Every deletion of a `do` word is measured against its heir on a fixture before it is authored,
  because three of this round's capabilities turned out to have no heir at all.
END PLAN20

── SLICE RECORD20 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD20 sha256=a3321e56909bc176e1cad13fc4155464682ea96aeb62281c073443ec33138521

Gate: F261 R19 — the F261 round 19 entry. VERDICT PASS. Written by the planner and reviewer of session 39 after reading the committed range `ac87bcc4`..`71cba20e` and re-deriving the readings below; the worker's report was evidence for none of them. It is booked here by the first commit of round 20 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r19.md` at `3d6f7bcf` and `.agent/last_block.md` at `690710d3` are byte-identical to the reviewer's scratch original, sha256 `05bbae28083528a53f95defd8aa4db6d68f519e20c1fc67c5449c01ef8641560`, and the two tables committed at `747d0a19` and `146f97a9` are byte-identical to the reviewer's, which are the research helper's. THE STATE: at `4ba46a24` and again at `71cba20e`, `.agent/plan.md` equals PLAN19, `.agent/live_review.md`, `.agent/decisions.md` and `.agent/prose_slips.md` equal their `ac87bcc4` blobs followed by RECORD19, DEC18 and SLIP19, and `docs/roadmap/features/T2_F273.md` equals its `ac87bcc4` blob with the pair P273 applied. THE TABLE COMMITS: at `747d0a19` and `146f97a9` the `apps`, `tests`, `docs`, `scripts`, `packages`, `README.md` and `.claude` objects equal the reviewer's dry-run commits, which applied the record before the tables and reproduced the helper's trees exactly; each commit's `--no-renames` path set is the dry run's plus its carrier, and `git show --numstat` reads 217 and 15 insertions. THE RENAME: in the dry run's production diff `do.report` becomes `run.show` and its `list` sentinel becomes `run.list` in a new `run` group placed after `job`, `_cmd_do_report` becomes `_cmd_run_show` and `_cmd_run_list`, every JSON key of the `do run` payload keeps its name while its value names the new word, and `do.evidence` leaves with `_cmd_do_evidence` while `export_evidence` stays for the redaction tests of surviving code. The research helper ran the old and the new command over one persisted run against one scratch data root and reported all five invocations byte-identical over 570759 bytes of stdout; the reviewer did not re-run that probe and instead measured the claim it rests on, that `apply_list_options` with `default_sort_field=None` and no flag returns its rows untouched, which reads true on the primary checkout's own module, and re-ran the tests that pin both readings. The sweep pattern of the round 19 block matches 28 lines in 7 files at `ac87bcc4`, and at `71cba20e` the same `git grep` over `apps`, `packages`, `scripts`, `tests`, `docs` without `docs/roadmap`, `README.md`, `AGENTS.md` and `.claude` exits 1 with no output. In the reviewer's dry run a full suite under `-n auto` without `tests/ui_server` read 1 failed, `test_vitest_passes`, 17281 passed and 29 skipped, and the whole of `tests/ui_server` read 497 passed. Over `tests/test_command_catalog.py`, `tests/cli/test_cli_ux.py`, `tests/test_grouped_cli.py`, `tests/orchestration/test_import_reachability.py` and `tests/cli/test_advertised_commands.py`, which passed 395 unmutated, removing the `run` group failed 4 tests, removing `run.show` from the catalog while its handler row stayed failed 3, removing that handler row while the entry stayed failed 2, restoring the old `do report` hint failed 1, putting `do.report` back failed 1, putting `do.evidence` back failed 1, changing what `run list --json` prints failed 1, and dropping the `--limit` the catalog attaches failed 1. A CORRECTION TO THE RECORD, which is append-only and is not rewritten: R-0803 quotes `remedy do report list` as the command whose output it measured, and that word is `remedy run list` from `747d0a19` onward; the finding's defect, a suite writing into the operator's data root, is untouched by this round. THE REVIEWER'S RUN in the primary checkout at `71cba20e` of those five files, every other test file the round edited, `tests/cli/test_golden_path.py`, `tests/docs/`, `tests/orchestration/test_command_discovery.py`, `tests/test_remedy_smoke_script.py` and `tests/ui_contracts/` read 2074 passed and 4 skipped, `python3 -m ruff check` over eleven edited files printed `All checks passed!`, and `git branch --list 'remedy/job-*'` read 16 lines. The open set reads 107 by distinct id at `71cba20e`.

- R-0913 — Medium, THE HEIR OF `do job-resume` RESUMES A JOB WHOSE WORKTREE OR BRANCH IS GONE INSTEAD OF REFUSING IT, AND SILENTLY MARKS A DELETED WORKTREE RETAINED AGAIN. Raised by the planner and reviewer of session 39 while preparing F261 round 20, from readings its research helper took at the base tree, after searching the open set for the resume guard and the cleanup status under §3 item 30: no open finding describes it, and R-0819 names `repair_attest.py` for a different reason. THE DEFECT, read at `71cba20e`: `resume_job_plan` in `packages/orchestration/pingpong_job.py` refuses a job whose `worktree_cleanup_status` is outside `JOB_RECOVERABLE_STATES` with `job_not_resumable`, and one whose recorded branch is gone with `job_branch_missing: …; refusing to create a replacement branch or fall back to a copy`; `do job-resume` was its only production caller, and this round deletes that command under DECISION amend0905-vocab D4, which leaves `job run` as the heir inventory ruling 5 names. Measured on one fixture by the helper: against a record whose `worktree_cleanup_status` reads `deleted`, `do job-resume` exits 1 with `job_not_resumable` while `job run` exits 0, proceeds, and resets that field to `retained`; against a record whose branch `remedy/job-<id>` has been deleted and whose worktree is gone, `do job-resume` exits 1 with `job_branch_missing` while `job run` exits 0 and the record still claims a worktree and a branch that do not exist. `job resume`, the F047 checkpoint word, guards a pending stop signal, worktree-head drift and the approval gate, which are different properties. WHY MEDIUM: a surviving command continues a job on state it cannot have, and a record that says where the work lives stops being true; nothing is written outside that record. WHY F273's: giving `job run` the refusals means changing what a surviving command does, which F261 does not. FIX: make the job-run path refuse a non-recoverable cleanup status and a missing recorded branch with those two messages, or record a DECISION that a resume may rebuild a worktree and make the record say so, with a test for the branch-missing case. Owner: F273.

- R-0914 — Medium, AFTER `do repair-attest` GOES NO COMMAND WRITES THE OPERATOR ATTESTATION THAT THE EVIDENCE AND REVIEW BUILDERS STILL READ, AND THE CANONICAL PATH BESIDE IT HAS NO PRODUCTION CALLER EITHER. Raised by the planner and reviewer of session 39 while preparing F261 round 20, from readings its research helper took at the base tree, after searching the open set for the attestation under §3 item 30: no open finding describes it, and R-0819 names a `run_dir` shape inside the same module. THE DEFECT, read at `71cba20e`: `_cmd_do_repair_attest` in `apps/cli/commands/do_cmd.py` was the only production caller of `attest_operator_repair` in `packages/orchestration/repair_attest.py`, which wrote `provider_evidence.json`, `review.json`, `token_accounting.json`, `manual_repair_provenance.json` and `safe.diff` under a task's evidence directory with a verdict of `operator_attested`; those artefacts are still read by `packages/orchestration/job_evidence.py`, by `is_attestable_source` in `packages/orchestration/review_subject.py`, and by `scripts/build_review_manifest.py` and `scripts/build_review_zip.py`. The helper measured the surviving neighbours on the same fixture: `job evidence` wrote its own thirty-five-file bundle and added nothing to the task's evidence directory, `job show --full --json` carried no attestation, and `test run <job> T001` exits 2 because it takes no task id — so a task blocked on a reviewer verdict can no longer be unblocked by an operator's hand-fix from the command line. `packages/orchestration/manual_attestation.py` and `create_manual_completion_bundle` are the canonical path beside it and already have no production caller. WHY MEDIUM: an evidence path the review package understands can no longer be produced, and a public function with four test files driving it stays behind them. WHY F273's: giving the attestation a word again, or deleting the writer and the parallel path with the four test files that drive them, is paydown; F261 prunes the catalog. FIX: either give the attestation a surviving word and a test that writes the five artefacts, or delete `attest_operator_repair` with `manual_attestation.py`, re-point the four test files at what remains, and say in `docs/system/` that an operator repair is attested no longer. Owner: F273.

- R-0915 — Medium, WITH `do replan` GONE NOTHING REGENERATES A JOB'S PLAN, AND SIX REFUSALS THAT NAMED IT NOW NAME NO NEXT ACTION, SO A REJECTED PLAN IS TERMINAL. Raised by the planner and reviewer of session 39 while preparing F261 round 20, from readings its research helper took at the base tree, after searching the open set for the replan under §3 item 30: no open finding describes it. THE DEFECT, read at `71cba20e`: `_cmd_do_replan` in `apps/cli/commands/do_cmd.py` was the only production caller of `replan` in `packages/orchestration/flight_plan.py`, which appended the current plan to the job's version chain, re-armed its approval to `pending` and rewrote its task list; six printed rejections in `apps/cli/commands/decision.py` and `apps/cli/commands/job.py` named that command as the way forward. The helper measured the surviving words on the same fixture: `job plan` exits 0 with `already planned — no changes made.` on a planned job and uses the legacy planner rather than the flight plan, `mission plan` belongs to the mission namespace, and `do "<goal>" --plan-only`, the flag DECISION amend0905-vocab D4 gives, exits 2 as an unrecognized argument because F268 has not built it. So after this round a job whose plan an operator rejected, or whose clarifications are answered, has no command that gives it a new plan, and the refusals that used to point at one now point nowhere — the shape DECISION F261 D17 left behind when `contract set` went and R-0906 recorded. `replan` and `ReplanRejectedError` keep callers under `tests/` alone. WHY MEDIUM: a user-observable step of the plan-approval loop leaves with no heir and its refusals lost their next action; nothing prints anything false. WHY F273's: building a replan word, or pointing the six refusals at `do <order> --plan-only` once F268 ships it, changes surviving surfaces; F261 prunes the catalog. FIX: point the six refusals at the word that regenerates a plan once one exists, and either give the flight-plan replan a surviving command with a test that versions the old plan and re-arms approval, or delete `replan` with its tests and say in `docs/system/` that a rejected plan is answered by a new order. Owner: F273.
END RECORD20

── SLICE DEC19 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC19 sha256=923f245914793e636a8caad70cebd7f00490edfa2796857888c7743bca335ade

## DECISION F261 D19 (2026-09-16, F261 round 20) — the deletion paragraph of `do repair-attest`, `do job-resume` and `do replan`

CONTEXT. DECISION amend0905-vocab D4 leaves `do` with an order and its flags and deletes every other word under it, and `.agent/f261_t003_inventory.md` puts these three in its round G, ahead of the `flight_plan` rename its rounds O and P owe. Measured at `71cba20e` by the reviewer's research helper, which ran all three commands and each proposed heir in process against one scratch data root and a scratch repository, and re-read by the reviewer on the dry-run trees. As in DECISION F261 D13, package code goes with a command when that command was its only production caller; a symbol whose surviving callers are tests stays, as DECISION F261 D18 left `export_evidence`, and the loss is registered instead.

CHOSEN, FIRST: `do repair-attest`. Deleted: the command, `_cmd_do_repair_attest` and `collect_diff_stat` in `packages/orchestration/repair_attest.py`, whose only caller it was, with that function's tests. The command attested an operator's own repair of a task, writing five artefacts under the task's evidence directory with a verdict of `operator_attested`. `attest_operator_repair` and the module's other exports stay: `job_evidence.py`, `review_subject.py` and the two review-package scripts read what it wrote, and four test files drive it. THE HEIR: none — the helper measured `job evidence`, `job show --full` and `test run` against the same fixture and none of them writes an attestation; R-0914 records the loss and the module's state.

CHOSEN, SECOND: `do job-resume`. Deleted: the command and `_cmd_do_job_resume`, with the test sites that drove the CLI. `resume_job_plan` in `packages/orchestration/pingpong_job.py` stays, driven by two test files. THE HEIR, as inventory ruling 5 names it: `job run`, which continues a job with its persisted controls — for the resume itself. It is no heir for the refusals: the helper measured that against a record whose worktree cleanup status reads `deleted`, and against one whose recorded branch is gone, `do job-resume` exited 1 with `job_not_resumable` and `job_branch_missing` while `job run` exited 0 and, in the first case, set the record back to `retained`. R-0913 records that for F273.

CHOSEN, THIRD: `do replan`. Deleted: the command, `_cmd_do_replan`, and the six printed rejections in `apps/cli/commands/decision.py` and `apps/cli/commands/job.py` that named it, each rewritten to name no command rather than a deleted one. `replan` and `ReplanRejectedError` in `packages/orchestration/flight_plan.py` stay, driven by two test files. The command regenerated a job's flight plan through a provider call — the helper's probe reached a local provider and produced ten tasks, so the word cost a provider call every time it ran — versioned the old plan and re-armed approval to pending. THE HEIR: none. `job plan` no-ops on a planned job and plans through the legacy planner; `mission plan` is the mission namespace; `do <order> --plan-only`, the flag D4 gives, is not built. R-0915 records the loss and the six refusals that now name no next action.

CONSEQUENCE. `remedy do repair-attest`, `remedy do job-resume` and `remedy do replan` are unknown words and their ids join `TestDeletedCommands`; `do` keeps `run`, `continue` and the words rounds H and J still owe. Three capabilities leave with no heir and are recorded as R-0913, R-0914 and R-0915 rather than replaced by a stub. HOW TO REVERSE: revert the round's three table commits and delete this section.
END DEC19

── SLICE P273-FROM ── target `docs/roadmap/features/T2_F273.md` ── REWRITE FROM ──
BEGIN P273-FROM sha256=02ba40253ff05ca183f2962834472ef97e9766110d44ec9dcb59de8a6546f5ad
  directory guard agree, with the test that exports a job whose task carries the minted default.

## Do not touch
END P273-FROM

── SLICE P273-TO ── target `docs/roadmap/features/T2_F273.md` ── REWRITE TO ──
BEGIN P273-TO sha256=c3a3ca4067d71f9e86ae476222c66a78c3cfa1b517970f42955f299fb2baa0b3
  directory guard agree, with the test that exports a job whose task carries the minted default.
- R-0913 carries a resolution line naming the commit that gave the job-run path the `job_not_resumable` and
  `job_branch_missing` refusals with the test for the branch-missing case, or the DECISION that rules a
  resume may rebuild a worktree.
- R-0914 carries a resolution line naming the surviving word that writes an operator attestation with its
  test, or the commit that deleted `attest_operator_repair` and `manual_attestation.py` with the four test
  files re-pointed.
- R-0915 carries a resolution line naming the word that regenerates a job's plan with its test, or the
  commit that deleted `replan` with its tests, and in either case the commit that pointed the six
  rejections at what a user does next.

## Do not touch
END P273-TO

── SLICE MUT-1-FROM ── G5 (1) only ── never a file ──
BEGIN MUT-1-FROM sha256=780c36792f1003e830942341f930b26c9304b4a78dfb5f54bdaadb3c37db1f72
    "run.show": lambda args: _cmd_run_show(
END MUT-1-FROM

── SLICE MUT-1-TO ── G5 (1) only ── never a file ──
BEGIN MUT-1-TO sha256=75eafc811e48b060d6f38009797ca73bddf9c2c111cf28a04c14eb9de215383b
    "do.repair-attest": lambda args: None,
    "run.show": lambda args: _cmd_run_show(
END MUT-1-TO

── SLICE MUT-2-FROM ── G5 (2) only ── never a file ──
BEGIN MUT-2-FROM sha256=780c36792f1003e830942341f930b26c9304b4a78dfb5f54bdaadb3c37db1f72
    "run.show": lambda args: _cmd_run_show(
END MUT-2-FROM

── SLICE MUT-2-TO ── G5 (2) only ── never a file ──
BEGIN MUT-2-TO sha256=5f3385c6288469a55d1a2b36092acc6fc7ddabda6804106d6047cff1a1231abb
    "do.job-resume": lambda args: None,
    "run.show": lambda args: _cmd_run_show(
END MUT-2-TO

── SLICE MUT-3-FROM ── G5 (3) only ── never a file ──
BEGIN MUT-3-FROM sha256=780c36792f1003e830942341f930b26c9304b4a78dfb5f54bdaadb3c37db1f72
    "run.show": lambda args: _cmd_run_show(
END MUT-3-FROM

── SLICE MUT-3-TO ── G5 (3) only ── never a file ──
BEGIN MUT-3-TO sha256=6fa88b12cb2a6eb06c404b7e1a3fa0f5edda70f55d56b74a6d091609df73885c
    "do.replan": lambda args: None,
    "run.show": lambda args: _cmd_run_show(
END MUT-3-TO

── SLICE MUT-4-FROM ── G5 (4) only ── never a file ──
BEGIN MUT-4-FROM sha256=02712bac189ba552ebc5467fa84fdc74312f3aa5d2cecffbc9dcefe62281b4b2
        related=("do.run",),
        args=(
            ArgDef("run_id", "Run ID"),
END MUT-4-FROM

── SLICE MUT-4-TO ── G5 (4) only ── never a file ──
BEGIN MUT-4-TO sha256=70f589985c7a6ec595aafe282bd07df70d1974faf9b88b44ac5587b320873dd6
        related=("do.run", "do.job-resume"),
        args=(
            ArgDef("run_id", "Run ID"),
END MUT-4-TO

── SLICE MUT-5-FROM ── G5 (5) only ── never a file ──
BEGIN MUT-5-FROM sha256=7a04130797e29b1d9386e48a7db8da6bf20037c6b93db704bab461d232c01e27
            print(f"Flight plan rejected for job {job_id_str}.")
END MUT-5-FROM

── SLICE MUT-5-TO ── G5 (5) only ── never a file ──
BEGIN MUT-5-TO sha256=ba521cf5e2ebaba24e1f9259c004e247e240915f427b3f8bde46bd631a6e9190
            print(f"Flight plan rejected for job {job_id_str}.")
            print(f"Run: remedy do replan {job_id_str}")
END MUT-5-TO
