── STEP T003/8 — F261 — ROUND 22 ──
Goal: Book round 21's PASS, resolve R-0900, register R-0923 to R-0926 for F273, record the round
21 prose slip and DECISION F261 D21, then delete the `repair` group with its handler by one
table; run the suite once.

Base commit: `13128d25`, on `feature/f261-cli-vocabulary-v2`. SESSION 5 of F261. Read AGENTS.md,
docs/agents/self_drive_protocol.md, `.agent/f261_t003_inventory.md`, and DECISION F261 D21 once
C1 has landed it.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block that is two or
more characters long is a run of a single repeated character, and every box-drawing rule inside the STEP and SLICE header
lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)` and `$?` in a compound command are refused by form, so write such checks
as Python scripts under `.remedy-wt/f261r22w/`, and never name a script after a standard-library
module; a pipe into `tail` hides pytest's exit code. The editable install resolves `apps` and
`packages` to the PRIMARY checkout, so a pytest run inside a worktree goes through a runner
script that changes into the worktree, puts it first on `sys.path` and in `PYTHONPATH`, and
asserts `apps.cli.grouped` loaded from inside it. Never call `run_job` or a runner yourself: a
job run started from inside a checkout creates a `remedy/job-*` branch in it.
`git branch --list 'remedy/job-*'` reads 16 lines now; keep it so. While a deletion is staged
but not committed, `test_every_enumerated_path_exists_in_this_repo` fails; run no suite then.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f261-r22.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN22; slice RECORD22 is appended to
    `.agent/live_review.md`, slice DEC21 to `.agent/decisions.md` and slice SLIP21 to
    `.agent/prose_slips.md`; in `docs/roadmap/features/T2_F273.md` the bytes of slice P273B-FROM
    are replaced by those of slice P273B-TO
C2  the `repair` group: copy `.remedy-wt/f261-block/f261-r22-repair.jsonl` to
    `.agent/authored/f261-r22-repair.jsonl` and apply it per THE TABLE, in one commit
C3  `.agent/handoff.md`, the handback; then `git push origin feature/f261-cli-vocabulary-v2`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f261-r22.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md` and
`docs/roadmap/features/T2_F273.md`. C2: the table's own carrier and the paths G3 names.
C3: `.agent/handoff.md`. The mutation carrier G5 names is READ from `.remedy-wt/` and is never
committed and never copied into `.agent/`.

## The appends and the pair

RECORD22, DEC21 and SLIP21 each begin with an empty line, and all three targets end in a
newline at `13128d25`: an append is the file's bytes followed by the slice's bytes, and nothing
else. The pair P273B: TO contains FROM: false, so it is a REWRITE; P273B-FROM occurs once
in `docs/roadmap/features/T2_F273.md` at `13128d25`, and at C1 P273B-FROM occurs 0 times and
P273B-TO once.

## THE TABLE

The carrier holds one JSON array per line. Its sha256, to verify before copying:
`f261-r22-repair.jsonl` `40190142a060931ec34fe47d1e8f2f5fc438c556c60cf339be7d8c742e9b182d`.
Apply the rows strictly in the order they appear in the file, each against the tree as the
previous rows left it, from the repository root:
`["edit", path, old, new, count]` opens the path with `encoding="utf-8", newline=""`, requires
the number of occurrences of `old` to equal `count` exactly, and replaces every occurrence with
`new`; `["delete", path]` removes the file; `["move", src, dst]` renames the file, whose target
must not exist; `["create", path, content]` writes `content` to a path that must not exist, with
the same encoding and newline setting. A count that differs or a target that exists is a STOP:
touch nothing further, commit nothing of the table, and hand back with the row and the reading.
Stage C2 with `git add -A` after the table and its carrier. The table is the reviewer's measured
dry run of DECISION F261 D21, applied on `13128d25` in the reviewer's own worktree.

## SPEC S — the suite, once, after G5 and before C3

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f261r22w/`. Report pytest's return code, the run's last output line, and every
distinct bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `.
Re-run each bad node alone, once, the same way, and report that return code beside it.

## Constraints

1. NO SLICE AND NO CARRIER IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C3, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f261r22w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f261-block/` and your
   own directory. `git worktree list` reads one row now; leave it so. Create no symlink.
5. Every commit stays under 500 insertions, read as the first column of `git show --numstat
   --format= <commit>` with git's default rename detection.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph of your own: slice RECORD22 already carries the only one.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 274 lines TOTAL and 196 lines of PROSE,
   against the caps of 490 and 400, where PROSE is every line that is not a line of slice CONTENT — the
   `BEGIN` and `END` marker lines count as prose.
8. GATE ORDER. G1 and G2 after C1; G3, G4 and G5 after C2; then SPEC S, whose result is G6; G7
   after C3 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r22.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; the committed carrier's sha256 equals its digest above.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN22, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its `13128d25` blob
followed by RECORD22, `.agent/decisions.md` its blob followed by DEC21, and
`.agent/prose_slips.md` its blob followed by SLIP21.
`docs/roadmap/features/T2_F273.md` equals its `13128d25` blob with the pair P273B applied, with
the counts The appends and the pair give. Over `.agent/live_review.md`: `^Gate: F\d+ R\d+ — `
reads 130 at `13128d25` and 131 at C1, with `Gate: F261 R21 — ` 0 times at `13128d25` and once
at C1; distinct `^- R-\d+ — ` ids 125 and 129, C1 minus base exactly `R-0923` through `R-0926`;
distinct `^Done: R-\d+ — ` ids 8 and 9, the one added exactly `R-0900`; the open set by distinct
id 117 and 120. `python3 -m pytest tests/docs/ -q` exits 0 at C1.

G3 THE TABLE, at C2. `git diff --no-renames --name-only` from C2's parent prints exactly C2's
carrier and these paths: `apps/cli/command_catalog.py`, `apps/cli/commands/__init__.py`, `apps/cli/commands/repair_cmd.py`, `docs/README.md`, `docs/guides/do-continue-v1.md`, `docs/system/real-test-execution-v1.md`, `docs/system/repair-loop-v0.md`, `docs/system/repair-loop-v1.md`, `docs/system/repair-request-builder-v0.md`, `packages/orchestration/mission_readiness.py`, `packages/orchestration/repair_loop.py`, `packages/orchestration/self_dogfood.py`, `packages/orchestration/test_execution_service.py`, `tests/cli/test_repair_request_cli.py`, `tests/cli/test_repair_runtime.py`, `tests/cli/test_repair_v1_cli.py`, `tests/orchestration/import_reachability_allowlist.txt`, `tests/orchestration/test_test_failure_repair.py`, `tests/test_command_catalog.py`.
`git rev-parse C2:<object>` equals the reviewer's dry run — which applied the table on
`13128d25` itself, the record touching none of these objects — for `apps`, `packages`, `scripts`,
`tests`, `docs/guides`, `docs/system`, `docs/README.md`, `README.md` and `.claude` in that order:
`39fdb3f1fca1ec21ad4ca1067a22ff6f2cd1af21`, `6d6fc2208138ed0af51f66b076c006a47bbae905`, `208d836b3d5d6532fe9354d9455ab71c67639ed2`, `b60c8a87538caf19d0b58aca1b5accfc6795f143`, `52e345b71419d519c98eba49cea68cc424c249ce`, `7d40cbc697ff8db91bca3cc014b9fc1ac699dc70`, `dc5ae72ef5c8b8479f5f4f499e135f9533b95b2f`, `60ca9975fc7ee622c78aaf9e61219ab89e210233`, `e3cd5e0ac262f3f993506e95825e270e39c03ec0`.
Report C2's insertions per constraint 5.

G4 THE SWEEP, at C2. `git ls-tree <C2> -- apps/cli/commands/repair_cmd.py` prints nothing, and
the same command for `packages/orchestration/repair_loop.py` prints its blob, because that module
survives. THE DELETED WORDS: `git grep -n -I -E '\brepair_cmd\b|_cmd_(repair_(start|propose|status|request|request_show)|failure_show)\b|remedy +repair +[a-z]|\["repair", *"'
<C2> -- apps packages scripts tests docs README.md AGENTS.md .claude ':!docs/roadmap'
':!docs/archive'` exits 1 and prints nothing; the same command at `13128d25` exits 0 and prints
78 lines in 15 files. THE CONTROL, which is what proves this round did not reach the group it
deferred: `git grep -n -I -E '\bpropose_cmd\b|\bpropose\.(list|show|evaluate|approve|reject|defer|materialize)\b|remedy +propose +[a-z]'`
over the same paths reads 60 lines in 12 files at `13128d25` AND 60 lines in 12 files at C2.
Report all four counts. `python3 -m ruff check` over every `.py` path of C2 that still exists at
C2 exits 0; report how many paths that was.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f261r22w/wt <C2's sha>`, each run
through the runner over `tests/test_command_catalog.py`, `tests/cli/test_advertised_commands.py`,
`tests/orchestration/test_import_reachability.py` and `tests/docs/` with `-rf --tb=no`. The four
mutations are rows of `.remedy-wt/f261r22w/../f261-block/f261-r22-mutations.jsonl`, whose sha256
must equal `04d1f2c3440c8442d1a4d979aeacd2086749e970517bcb215d625d1abcded96a`; each row is
`[label, path, from, to, node]`, the `from` bytes must occur EXACTLY ONCE in that path inside the
worktree, and the file is restored with `git -C .remedy-wt/f261r22w/wt checkout -- <path>` after
each run. Read that carrier; never retype its bytes. (a) CONTROL: must exit 0. Each of M1 to M4
must exit 1 with its row's node AMONG the failed nodes — M1 additionally reds
`TestCatalogIntegrity::test_command_id_format`, because the entry it re-inserts carries a
`repair.` id under the `dev` group, and that second red is expected rather than a STOP.
Report each exit code, summary line, number of failed nodes and each FROM's occurrence count;
then `git worktree remove --force .remedy-wt/f261r22w/wt` and read
`git branch --list 'remedy/job-*'`.

G6 THE SUITE, SPEC S at C2: must exit 0 with no bad node; report the last output line. A bad
node whose lone re-run exits 0 is reported as such with both readings, and is not a STOP; a bad
node whose lone re-run fails is.

G7 THE TREE, after C3 and the push. `git status --porcelain` prints `''`; C0a to C3 are
single-parent commits in that order on `13128d25`; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f261-cli-vocabulary-v2`; `git worktree list` prints one row, and
`git branch --list 'remedy/job-*'` prints 16 lines.

## The handback, C3

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 5 of feature F261 · round 22 · rounds so far 22`, with one sentence of context
self-assessment. `## Commits` lists C0a to C2, each row's `+/-` cell equal to constraint 5's
reading of that commit and its deletions column; C3's own numbers appear nowhere, per item 31 of
§3. `## Verification` gives G1 to G6 with real exit codes. It states the open findings at 120 by
distinct id, with the High ids R-0803, R-0804 and R-0807, and `Operator questions open: 0`. Its
`## Next` names, in order: Phase 1 rule 1; the reviewer's verdict on round 22; and the `propose`
group, which DECISION F261 D21 defers together with the ruling `worker_queue.get_next_job` needs.

── SLICE PLAN22 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN22 sha256=3d635a50765286234be27bd8c192821c3e5a5fd92e87ab2c87db1a67042ba16b
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 22 continues T003. It books round 21's PASS, resolves R-0900, registers R-0923 to R-0926
for F273 and records DECISION F261 D21, then deletes the `repair` group with its handler by one
table. The `propose` group, which the inventory pairs with it, is deferred by D21.

## Next Steps

1. The `propose` group, with the DECISION its deletion needs about the unresolved-proposal gate
   of `packages/orchestration/worker_queue.py`, and the F011 `--status` discriminator that
   `tests/cli/test_job_stop.py` loses with `propose.list`.
2. The rest of T003 in the inventory's order, with R-0767 and R-0894.
3. `job budget <id> set` over the run-contract budget fields and the token budget profile, the
   word DECISION amend0905-vocab D4 gives those writes, with R-0906 and R-0909.
4. T004, which owes the visible group order of D4 and the README quickstart of R-0895.

## Risks

- 117 findings are open by distinct id before this round's record and 120 after it; three are
  High, R-0803, R-0804 and R-0807.
- The feature's soft limit of 25 rounds leaves three after this one, and the inventory proposes
  more than three; the session that reaches the limit owes the scope report and executes the
  split-and-close default of operator amendment amend0905-throughput, placing the follow-up
  feature directly after F261 per amend0906.
- A deletion that would break a SURVIVING command is deferred to a round that can rule on it,
  never shipped with a finding: that is why `propose` is not in this round.
END PLAN22

── SLICE RECORD22 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD22 sha256=1f843dd7deb54ef99eb704ffb272d3800a8115d32abb71d23b76fd792accf289

Gate: F261 R21 — the F261 round 21 entry. VERDICT PASS. Written by the planner and reviewer of session 40 after reading the committed range `ab748c47`..`13128d25` and re-deriving every reading below; the worker's report was evidence for none of them. It is booked here by the first commit of round 22 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r21.md` at `55c8a3ff` and `.agent/last_block.md` at `3e419b6d` are byte-identical to the reviewer's scratch original, sha256 `8d967dc0902c9dffd6f08013e69214e69701176ac41deddb9daae0bcc9584654`, and the two tables committed at `58be13e3` and `28520ab8` are byte-identical to the reviewer's, which are the two research helpers' with the reviewer's own two amendments applied. THE STATE: at `e9e6bc93` and again at `13128d25`, `.agent/plan.md` equals PLAN21, `.agent/live_review.md` and `.agent/decisions.md` equal their `ab748c47` blobs followed by RECORD21 and DEC20, and `docs/roadmap/features/T2_F273.md` equals its `ab748c47` blob with the pair P273 applied; the `Gate: F\d+ R\d+ — ` count reads 129 then 130, the distinct registered ids 118 then 125 with the delta exactly R-0916 to R-0922, the distinct `Done:` ids 8 then 8, and the open set 110 then 117. THE TABLE COMMITS: at `58be13e3` and `28520ab8` the `apps`, `packages`, `scripts`, `tests`, `docs/guides`, `docs/system`, `docs/README.md`, `README.md` and `.claude` objects equal the reviewer's dry-run commits object for object, all eighteen of them, so the worker reproduced exactly the tree the reviewer tested; the path sets are the dry run's plus each commit's carrier, 34 and 7, and `git show --numstat` reads 216 and 146 insertions, every commit of the round under 500. In the reviewer's dry run the production diff leaves `do continue` with its catalog entry, its handler and `packages/orchestration/do_continue.py`, takes the repair-reconcile block of `packages/orchestration/repair_loop.py` whose only caller that module was, keeps `docs/guides/do-continue-v1.md` under a dated banner, and re-points the hints at `patch apply`, which `change proof` already recommends. THE SWEEP: the round 21 block's pattern matches 117 lines in 21 files at `ab748c47`, and at `13128d25` the same `git grep` exits 0 with exactly three lines, in `docs/system/repair-loop-v1.md`, `tests/cli/test_advertised_commands.py` and `tests/orchestration/test_self_dogfood_execution.py`, each a deliberate quotation or a dated historical record. A DEFECT THE REVIEWER'S OWN RUN FOUND AND THE HELPER'S TARGETED SET DID NOT: the status banner first named the deleted module by path, which `tests/docs/test_named_source_paths.py` forbids an operator-facing page to do, and the reviewer amended the carrier before the block was authored rather than registering it. THE GATE THE REVIEWER GOT WRONG: G5 mutation (5) was unmeetable as ordered, because slice MUT-5-FROM held a truncated line rather than the whole line at `docs/system/architecture.md`, so its occurrence count read 0 and the worker declared it instead of editing the slice or the target, which is the right answer; re-run by the reviewer at `13128d25` with the target's real line the mutation exits 1 with `test_every_group_only_advertisement_reaches_a_command` the sole failure against a control of 401 passed, so the guard reaches that page and discriminates. That is a reviewer-prose inaccuracy that left nothing wrong on disk and is recorded in `.agent/prose_slips.md`, not as an id, per operator amendment amend0827-process-diet rule 2. THE REVIEWER'S RUN in the primary checkout at `13128d25` of the round's own test files, the files nearest every production module it touched, `tests/cli/test_golden_path.py`, the whole of `tests/docs/`, `tests/orchestration/test_event_name_coupling.py`, `tests/ui_server/test_dashboard_cockpit_truth.py` and `tests/orchestration/test_evidence_index.py` read 1275 passed, `python3 -m ruff check` over the nineteen edited files that survive printed `All checks passed!`, `git worktree list` reads one row and `git branch --list 'remedy/job-*'` 16 lines. The worker ran the full suite once in the primary checkout, as the block orders: exit 0, `17728 passed, 23 skipped, 1 warning in 1298.35s`, with no line-initial `FAILED ` or `ERROR ` in the transcript. The open set reads 117 by distinct id at `13128d25`.

Done: R-0900 — RESOLVED by F261 round 21. `28520ab8` names a command the catalog carries at every advertisement that named a group alone, and adds the guard the finding's fix clause asks for. The seven `remedy brain <job_id>` and `remedy brain --json` sites of `docs/system/architecture.md` and the two of `packages/orchestration/brain_detail.py` now name `brain graph`, which is the command the surrounding prose means and the id `apps/cli/commands/brain.py` dispatches; the `remedy do --yes` sites of `flight_plan.py` and `orchestrator_loop.py` and the `remedy do --task-file` site of `docs/system/vocabulary.md` now name `do run`; the `remedy project <project_id>` alias line of `architecture.md`, which no catalog entry ever carried, is deleted and the sentence claiming the alias is replaced by what a bare group really does; and `58be13e3` removed the four `remedy do --continue` sites with the module that held them. `tests/cli/test_advertised_commands.py` gains `scan_group_only_invocations`, `_group_only_resolves` and `test_every_group_only_advertisement_reaches_a_command`, which resolve a one-token advertisement against `_DEFAULT_COMMAND` and `_ALWAYS_INJECT` IMPORTED from `apps/cli/grouped.py` rather than against the group list, so a group that gains or loses a default cannot leave the guard behind. Verified by the reviewer of session 40 at `13128d25`: the guard's own sweep reads 60 group-only advertisements over both corpora with 0 unrunnable, and restoring the group-only form at `packages/orchestration/brain_detail.py` or at `docs/system/architecture.md` fails that node alone against a control of 401 passed. The `brain` half of the finding and the `do --continue` half are both discharged; the `do continue` command itself left in the same round.

- R-0923 — Medium, STARTING A REPAIR FROM A PERSISTED FAILURE ARTIFACT HAS NO HEIR, AND THE REPAIR-ATTEMPT STORE LOSES ITS ONLY WRITER WHILE TWO MODULES STILL READ IT. Raised by the planner and reviewer of session 40 while preparing F261 round 22, from readings its research helper took at the base tree and ran again on the applied tree, after searching the open set for the repair loop and the repair attempts under §3 item 30: no open finding describes it, and R-0918, registered one round earlier, names the reconciliation that ran AFTER an apply rather than the word that started a repair. THE DEFECT, read at `13128d25`: `repair start` and the `repair` group's own proposal word were the only production callers of `start_repair_loop_v0` and `run_repair_attempt` in `packages/orchestration/repair_loop.py`, and this round deletes them under DECISION amend0905-vocab D4. Nothing turns a `TestFailureArtifact` into a fix task or a repair patch intent from the command line afterwards; the in-run repair rounds of `remedy do run --repair-rounds <n>` are a phase of a run, not a word an operator can aim at an artifact. Measured on a scratch data root holding a real failure artifact: both words exit 0 at the base and exit 2 at the applied tip. The `repair_attempts_v1` store in job metadata therefore has no writer left, while `load_repair_attempts` is still called by `packages/orchestration/mission_readiness.py` and `packages/orchestration/self_dogfood.py`. `evaluate_repair_eligibility`, `save_repair_attempt`, `create_or_reuse_fix_task`, `build_fixture_repair`, `export_repair_loop_json`, `summarize_repair_loop`, `export_repair_attempt_json` and `summarize_repair_attempt` keep test callers or none, and the module stays whole under DECISION F261 D17's rule. WHY MEDIUM: a user-observable step of the repair loop leaves with no heir and a persisted store stops being written while it is still read; nothing prints anything false. WHY F273's: giving the repair loop a surviving word changes what the CLI offers, which D4 gives F261 the catalog for and not the behaviour. FIX: either give the repair loop a word under a surviving group with a test that drives a failure artifact to a repair attempt, or delete the attempt store's readers and its writer together and say in `docs/system/repair-loop-v1.md` that a repair is only ever a phase of a run. Owner: F273.

- R-0924 — Low, READING A REPAIR ATTEMPT'S APPROVAL STATE HAS NO HEIR. Raised by the planner and reviewer of session 40 while preparing F261 round 22, after searching the open set for the repair status word under §3 item 30: no open finding describes it, and R-0923 names the writer while this names the reader. THE DEFECT, read at `13128d25`: the deleted `repair status` printed an attempt's id, its failure artifact, its repair task, its intent id, its status, its stop reason, its approval state, its kind, its expected effect and whether it resolved the failure. Measured by the helper against a scratch data root: `remedy mission readiness <job> --json` consumes the attempts only to gate the `can_propose_repair` and `can_apply_approved_repair` capabilities, and `remedy self inspect --job-id <job>` raises one item for an attempt that has no intent; neither prints an attempt, and no other surviving command reads the store. WHY LOW: a read-only view leaves and the data it showed is still on disk, reachable by any later word. WHY F273's: it is the same repair-loop surface as R-0923 and is answered by the same ruling. FIX: either the surviving repair word of R-0923 prints the attempt list, or the cockpit's repair section carries the fields and a test pins them. Owner: F273.

- R-0925 — Low, PREPARING A PROVIDER-AGNOSTIC REPAIR REQUEST HAS NO HEIR, AND FOURTEEN FURTHER EXPORTS OF ITS MODULE ALREADY HAD NO PRODUCTION CALLER. Raised by the planner and reviewer of session 40 while preparing F261 round 22, after searching the open set for the repair request package under §3 item 30: no open finding describes it. THE DEFECT, read at `13128d25`: the deleted `repair request` and `repair request-show` were the only production callers of `build_repair_request_package`, `export_build_result_json` and `get_request_package` in `packages/orchestration/repair_request_builder.py`, and handing a safe, structured failure package to an external actor stops being expressible as a command. The module stays whole under DECISION F261 D17's rule, and `load_request_packages` keeps its production reader in `packages/orchestration/ui_server.py`. WHY LOW: the capability was advanced and internal, its module is untouched, and nothing on disk becomes wrong. WHY F273's: deciding whether the package has a word again, or deleting the module with its tests, is paydown. FIX: either give the package a surviving word with a test that builds one, or delete `repair_request_builder.py` with its test file and its cockpit section together. Owner: F273.

- R-0926 — Low, TWO COCKPIT SECTIONS NOW READ REPAIR STORES THAT HAVE NO WRITER LEFT. Raised by the planner and reviewer of session 40 while preparing F261 round 22, after searching the open set for the cockpit repair sections under §3 item 30: no open finding describes them; R-0903, R-0905, R-0907 and R-0919 record the same CLASS for other sections and name neither of these. THE DEFECT, read at `13128d25`: `_build_repair_section` in `packages/orchestration/ui_server.py` reads `job.metadata['repair_attempts_v1']` and is wired as the payload's `repair` key, and `_build_repair_request_section` reads `load_request_packages` and is wired as its `repair_request` key; this round deletes the only writers of both stores, as R-0923 and R-0925 record. Measured by the helper on the applied tree against a job carrying a real failure artifact: the first returns an attempt count of 0 with an empty next safe action, the second a request-package count of 0 with a latest target of `none`. Both sections are KEPT rather than deleted, the reading DECISION F261 D13 took for the orchestrator section under R-0903 and D20 took for the continuation section under R-0919: inventory ruling 2 binds a cockpit ROUTE whose payload is a deleted command's output, and these are keys of the job dashboard payload. Neither advertises a deleted word — the repair section's only next safe action is `remedy patch approve`, which survives — and both stay pinned by `tests/ui_server/test_dashboard_cockpit_truth.py`. WHY LOW: two cockpit sections report zero for ever on any job a pre-round release did not write; nothing prints anything false and no other surface is affected. WHY F273's: deleting a section with its client mapping and its cockpit-truth test, or giving it a writer, changes a surviving surface. FIX: delete both sections with their fixtures once R-0923 and R-0925 are ruled on, or keep them and name the ruling that gave their stores a writer again. Owner: F273.
END RECORD22

── SLICE DEC21 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC21 sha256=6960e3f2732936747cb86b2bd14e7c806f722d8f06df2a422998a973ded05d82

## DECISION F261 D21 (2026-09-16, F261 round 22) — the deletion paragraph of the `repair` group, and why `propose` is not in this round

CONTEXT. DECISION amend0905-vocab D4 names neither `repair` nor `propose`, and `.agent/f261_t003_inventory.md` puts both in its round I, with the ordering constraint that `do continue` goes before `repair` — which round 21 satisfied. Measured at `13128d25` by the reviewer's research helper in its own detached worktree, running all thirteen commands and each proposed heir in process against one scratch data root, and re-applied and re-measured by the reviewer on its own dry-run tree.

CHOSEN, FIRST: the `repair` group goes — its GroupDef, its six catalog entries, `apps/cli/commands/repair_cmd.py`, its dispatch wiring, its allowlist line, three CLI test files and the CLI half of `tests/orchestration/test_test_failure_repair.py`, with the pages that named its words rewritten to the past tense under dated banners. ONE word keeps a measured heir: `repair failure-show` is answered by `remedy job show <id> --full --json`, whose artifact metadata carries every field the deleted exporter printed — measured field by field on the applied tree; it prints every artifact rather than one and does not synthesise the derived related-changes list. The other four capabilities have NO heir and are registered as R-0923, R-0924, R-0925 and R-0926 rather than stubbed.

CHOSEN, SECOND: NO package module and NO package symbol is deleted, which is DECISION F261 D17's rule rather than D19's. `packages/orchestration/repair_loop.py`, `test_failure_artifact.py`, `repair_request_builder.py` and `proposed_tasks.py` each keep production importers unrelated to the deleted handlers, so the module-level test of D19 — a symbol whose only production caller dies leaves with it — does not reach a module that survives for other reasons. Twenty-three symbols become test-only and are named in R-0923 and R-0925 instead. One row beyond the helper's table is the reviewer's: a section banner in `repair_loop.py` named a deleted word in the present tense, inside a surviving module, where no guard can see it.

CHOSEN, THIRD: the `propose` group is DEFERRED to its own round, against the inventory's round I, and this is the substantive ruling of D21. `get_next_job` in `packages/orchestration/worker_queue.py` skips every queued entry for which `_has_unresolved_proposals` is true, and that helper is true for any proposed task still unresolved or approved-but-unmaterialized. `job_fulfillment` writes such a task on every verified fulfillment. Deleting `propose` removes the only production resolver, so every job that produced a follow-up suggestion would be skipped by `worker run` for ever. That is not a capability leaving with no heir, which this feature registers as a finding; it is a SURVIVING command breaking, and repairing it means changing what a surviving command does, which the Do-not-touch section of `docs/roadmap/features/T2_F261.md` forbids this feature. The round that takes `propose` carries a DECISION about that gate, and also inherits the F011 discriminator of `tests/cli/test_job_stop.py`: `--status` is the only option name that is a flag on one command and valued on another, and `propose.list` is the valued half.

CONSEQUENCE. `remedy repair` is an unknown word, its six ids join `TestDeletedCommands`, and the catalog reads 30 groups and 161 commands. Four capabilities leave with no heir and two cockpit sections lose their writers, all recorded rather than replaced by a stub. The inventory's round I is split in two and its remaining half is `.agent/plan.md`'s first next step. HOW TO REVERSE: revert the round's table commit and delete this section.
END DEC21

── SLICE SLIP21 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIP21 sha256=b3399941f74d73753d36c926b655abf1c117bd5a4aecb35857a36bf107ca17b6

2026-09-16, F261 round 21 — the reviewer's slice MUT-5-FROM held a truncated line rather than the whole line at `docs/system/architecture.md`, so gate G5 mutation (5) read an occurrence count of 0 and was unmeetable as ordered; the worker declared it instead of editing the slice or the target, and the reviewer re-ran the mutation with the target's real line and found the guard red on the named node against a green control.
END SLIP21

── SLICE P273B-FROM ── target `docs/roadmap/features/T2_F273.md` ── REWRITE FROM ──
BEGIN P273B-FROM sha256=23b95984a62b3510b12720b5b6550eb85f54ebf143515dfd3c8f55f157058d83
  test that reaches the auto-approve path, or the commit that deleted that branch and its parameter.

## Do not touch
END P273B-FROM

── SLICE P273B-TO ── target `docs/roadmap/features/T2_F273.md` ── REWRITE TO ──
BEGIN P273B-TO sha256=fcb8cd452656553d741ca2cf7819fecff26a506f55b4e29a730bf0e3526b099a
  test that reaches the auto-approve path, or the commit that deleted that branch and its parameter.
- R-0923 carries a resolution line naming the surviving word that starts a repair from a failure
  artifact with its test, or the commit that deleted the repair-attempt store's readers and its
  writer together with the doc sentence that says so.
- R-0924 carries a resolution line naming the surface that prints a repair attempt's approval state
  with its test.
- R-0925 carries a resolution line naming the surviving word that builds a repair request package
  with its test, or the commit that deleted that module with its test file and its cockpit section.
- R-0926 carries a resolution line naming the commit that deleted the two cockpit repair sections
  with their fixtures, or the ruling that gave their stores a writer again.

## Do not touch
END P273B-TO
