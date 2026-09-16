── STEP T003/8 — F261 — ROUND 24 ──
Goal: Book round 23's PASS, register R-0931 for F273 and record DECISION F261 D23, then delete
`job rerun` by one table and rename the group `teach` to `teacher` by a second; run the suite once.

Base commit: `fc13ba87`, on `feature/f261-cli-vocabulary-v2`. SESSION 6 of F261. Read AGENTS.md,
docs/agents/self_drive_protocol.md, `.agent/f261_t003_inventory.md`, and DECISION F261 D23 once
C1 has landed it.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block that is two or
more characters long is a run of a single repeated character, and every box-drawing rule inside the STEP and SLICE header
lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)` and `$?` in a compound command are refused by form, so write such checks
as Python scripts under `.remedy-wt/f261r24w/`, and never name a script after a standard-library
module; a pipe into `tail` hides pytest's exit code. The editable install resolves `apps` and
`packages` to the PRIMARY checkout, so a pytest run inside a worktree goes through a runner
script that changes into the worktree, puts it first on `sys.path` and in `PYTHONPATH`, and
asserts `apps.cli.grouped` loaded from inside it. Never call `run_job` or any runner yourself: a
job run started from inside a checkout creates a `remedy/job-*` branch in it.
`git branch --list 'remedy/job-*'` reads 16 lines now; keep it so. While a deletion or a move is
staged but not committed, `test_every_enumerated_path_exists_in_this_repo` fails; run no suite then.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f261-r24.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN24; slice RECORD24 is appended to
    `.agent/live_review.md` and slice DEC23 to `.agent/decisions.md`; in
    `docs/roadmap/features/T2_F273.md` the bytes of slice P273D-FROM are replaced by those of
    slice P273D-TO
C2  `job rerun`: copy `.remedy-wt/f261-block/f261-r24-rerun.jsonl` to
    `.agent/authored/f261-r24-rerun.jsonl` and apply it per THE TABLES, in one commit
C3  `teach` becomes `teacher`: copy `.remedy-wt/f261-block/f261-r24-teacher.jsonl` to
    `.agent/authored/f261-r24-teacher.jsonl` and apply it per THE TABLES, in one commit
C4  `.agent/handoff.md`, the handback; then `git push origin feature/f261-cli-vocabulary-v2`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f261-r24.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md`, `.agent/decisions.md` and `docs/roadmap/features/T2_F273.md`. C2 and C3:
each table's own carrier and the paths G3 names for that commit. C4: `.agent/handoff.md`. The
gate carrier G4 names and the mutation carrier G5 names are READ from `.remedy-wt/f261-block/`
and are never committed and never copied into `.agent/`.

## The appends and the pair

RECORD24 and DEC23 each begin with an empty line, and both targets end in a newline at
`fc13ba87`: an append is the file's bytes followed by the slice's bytes, and nothing else. The
pair P273D: TO contains FROM: false, so it is a REWRITE; P273D-FROM occurs once in
`docs/roadmap/features/T2_F273.md` at `fc13ba87`, and at C1 P273D-FROM occurs 0 times and
P273D-TO once.

## THE TABLES

Each carrier holds one JSON array per line. Their sha256, to verify before copying:
`f261-r24-rerun.jsonl` `a3ece98b795f51e1e7703c0f5cc07af38c5787296d31d38606064f5c678bdbc7` and
`f261-r24-teacher.jsonl` `f9d47405806677c0bb788285a86135ce0f3af981bd860581d76caed517242a2b`.
Apply a table's rows strictly in the order they appear in its file, each against the tree as the
previous rows left it, from the repository root:
`["edit", path, old, new, count]` opens the path with `encoding="utf-8", newline=""`, requires
the number of occurrences of `old` to equal `count` exactly, and replaces every occurrence with
`new`; `["delete", path]` removes the file; `["move", src, dst]` renames the file, whose target
must not exist; `["create", path, content]` writes `content` to a path that must not exist, with
the same encoding and newline setting. A count that differs or a target that exists is a STOP:
touch nothing further, commit nothing of that table, and hand back with the row and the reading.
Stage each commit with `git add -A` after its table and its carrier. The rerun table is the
reviewer's measured dry run of DECISION F261 D23 on `fc13ba87`, and the teacher table is its
generator's output on that dry run's commit, applied there by the reviewer.

## SPEC S — the suite, once, after G5 and before C4

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f261r24w/`. Report pytest's return code, the run's last output line, and every
distinct bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `.
Re-run each bad node alone, once, the same way, and report that return code beside it.

## Constraints

1. NO SLICE AND NO CARRIER IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C4, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f261r24w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f261-block/` and your
   own directory. `git worktree list` reads one row now; leave it so. Create no symlink.
5. Every commit stays under 500 insertions, read as the first column of `git show --numstat
   --format= <commit>` with git's default rename detection.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph: this round resolves no finding.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 265 lines TOTAL and 204 lines of PROSE,
   against the caps of 490 and 400, where PROSE is every line that is not a line of slice CONTENT — the
   `BEGIN` and `END` marker lines count as prose.
8. GATE ORDER. G1 and G2 after C1; G3 half C2 after C2; G3 half C3, G4 and G5 after C3; then
   SPEC S, whose result is G6; G7 after C4 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r24.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; each committed carrier's sha256 equals its digest above.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN24, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its `fc13ba87` blob
followed by RECORD24, and `.agent/decisions.md` its blob followed by DEC23.
`docs/roadmap/features/T2_F273.md` equals its `fc13ba87` blob with the pair P273D applied, with
the counts The appends and the pair give. Over `.agent/live_review.md`: `^Gate: F\d+ R\d+ — `
reads 132 at `fc13ba87` and 133 at C1, with `Gate: F261 R23 — ` 0 times at `fc13ba87` and once at
C1; distinct `^- R-\d+ — ` ids 133 and 134, C1 minus base exactly `R-0931`; distinct
`^Done: R-\d+ — ` ids 9 and 9; the open set by distinct id 124 and 125.
`python3 -m pytest tests/docs/ -q` exits 0 at C1.

G3 THE TABLES. HALF C2, at C2: `git diff --no-renames --name-only` from C2's parent prints
exactly C2's carrier and these paths: `README.md`, `apps/cli/command_catalog.py`, `apps/cli/commands/__init__.py`, `apps/cli/commands/job_rerun_cmd.py`, `packages/orchestration/run_manifest.py`, `packages/orchestration/worktrees.py`, `tests/cli/test_job_rerun_integrity_errors.py`, `tests/cli/test_job_rerun_manifest.py`, `tests/orchestration/import_reachability_allowlist.txt`, `tests/orchestration/test_run_manifest_input_coverage.py`, `tests/orchestration/test_run_manifest_integrity.py`, `tests/orchestration/test_run_manifest_reference_coverage.py`, `tests/orchestration/test_run_manifest_strict_boundaries.py`, `tests/test_command_catalog.py`.
`git rev-parse C2:<object>` for `apps`, `packages`, `scripts`, `tests`, `docs/guides`,
`docs/system`, `docs/README.md`, `README.md` and `.claude`, in that order, equals the reviewer's
dry run, which applied the table on `fc13ba87` itself, the record touching none of these
objects: `ff95a593890b1f47e479052ccdd11a71afbfce68`, `7af6331963c75cb02b15b159837e7f0186daf37c`, `3e3c450e0dffcdd11abbc52b0a7b085359df38e4`, `9a67f6e8bfa5b11c9814506df1562e1e9bd6e109`, `52e345b71419d519c98eba49cea68cc424c249ce`, `cc42698197076bc70d79a91b05ca633d7ebd2df8`, `c282d425ef909cf9257605294f23aba7d9457fac`, `142c3f25897ec869c73753beb4e37b21c772f642`, `e3cd5e0ac262f3f993506e95825e270e39c03ec0`.
From the primary checkout at C2, `python3 -B -m pytest -q tests/cli/test_golden_path.py` exits 0.
HALF C3, at C3: the same name list from C3's parent prints exactly C3's carrier and these paths:
`README.md`, `apps/cli/command_catalog.py`, `apps/cli/commands/__init__.py`, `apps/cli/commands/teach_cmd.py`, `apps/cli/commands/teacher_cmd.py`, `packages/orchestration/teacher_model.py`, `packages/orchestration/teacher_qa.py`, `tests/cli/test_cli_ux.py`, `tests/cli/test_teach_cmd.py`, `tests/cli/test_teacher_cmd.py`, `tests/orchestration/import_reachability_allowlist.txt`, `tests/orchestration/test_import_reachability.py`, `tests/orchestration/test_teacher_model.py`, `tests/orchestration/test_teacher_qa.py`, `tests/test_command_catalog.py`.
The same objects at C3 equal: `57cdc70d5ddc3b059e3cb6023b538057fa9df9e2`, `ec2c3efd7541c8cc7d30b2b226b109e1b285da45`, `3e3c450e0dffcdd11abbc52b0a7b085359df38e4`, `c4a66e215510d3e625f77e4e591a99996ff37e5e`, `52e345b71419d519c98eba49cea68cc424c249ce`, `cc42698197076bc70d79a91b05ca633d7ebd2df8`, `c282d425ef909cf9257605294f23aba7d9457fac`, `9cef3616d99c9689b6b100ea7792e9d8c2b7e57d`, `e3cd5e0ac262f3f993506e95825e270e39c03ec0`.
Report the insertions of C2 and of C3 per constraint 5.

G4 THE SWEEP, at C2 and at C3. `git ls-tree` at C3 prints nothing for
`apps/cli/commands/job_rerun_cmd.py`, `apps/cli/commands/teach_cmd.py` and
`tests/cli/test_teach_cmd.py`, and prints a blob for `apps/cli/commands/teacher_cmd.py` and
`packages/orchestration/run_manifest.py`. The four patterns are the `deleted`, `control`,
`fulfill` and `teach` values of `.remedy-wt/f261-block/f261-r24-gates.json`, sha256
`d8a6716f204e17a8a05cbe2daf3aa797930cf8501f2022d02fd44e118c74a838`; read them from that file in Python
and pass each as one argv element to
`git grep -n -I -E <pattern> <rev> -- apps packages scripts tests docs README.md AGENTS.md .claude ':!docs/roadmap' ':!docs/archive'`,
never retyping them in a shell, at `fc13ba87`, at C2 and at C3. The expected readings, lines and
files: `deleted` 31 and 12 at `fc13ba87`, 2 and 2 at C2, 2 and 2 at C3; `control` 67 and 11 at `fc13ba87`, 67 and 11 at C2, 67 and 11 at C3; `fulfill` 21 and 7 at `fc13ba87`, 21 and 7 at C2, 21 and 7 at C3; `teach` 77 and 17 at `fc13ba87`, 77 and 17 at C2, 10 and 6 at C3. At C3 the `deleted` lines are the new `TestDeletedCommands` id and a
`tests/docs/test_docs_consistency.py` pin of accepted F012 history, and the `teach` lines are
the two `TestRenamedCommands` rows, four lines of `docs/system/vocabulary.md` and four prose uses
of the verb, as DECISION F261 D23 names them; print every such line. `control` is the `propose`
group and `fulfill` the word D23 defers: both must read the same at all three revisions.
`python3 -m ruff check` over every `.py` path C2 or C3 edits that still exists at C3 exits 0;
report how many paths that was.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f261r24w/wt <C3's sha>`, each run
through the runner over `tests/test_command_catalog.py`, `tests/cli/test_advertised_commands.py`,
`tests/orchestration/test_import_reachability.py`, `tests/cli/test_cli_ux.py`,
`tests/cli/test_teacher_cmd.py`, `tests/orchestration/test_teacher_qa.py`,
`tests/orchestration/test_teacher_model.py` and `tests/docs/` with `-rf --tb=no`. The mutations are
the rows of `.remedy-wt/f261-block/f261-r24-mutations.jsonl`, whose sha256 must equal
`c611f931d1a411ac3412d6879191823d96e3a6506954c7ebe3994a0996adfa2b`; each row is
`[label, path, from, to, node]`, the `from` bytes must occur EXACTLY ONCE in that path inside the
worktree, and the file is restored with `git -C .remedy-wt/f261r24w/wt checkout -- <path>` after
each run. Read that carrier; never retype its bytes. (a) CONTROL: must exit 0. Each mutation row
must exit 1 with its row's node AMONG the failed nodes; a rename row reds further nodes that pin
the same id, and those are expected rather than a STOP. Report each exit code, summary line,
number of failed nodes and each FROM's occurrence count; then
`git worktree remove --force .remedy-wt/f261r24w/wt` and read `git branch --list 'remedy/job-*'`.

G6 THE SUITE, SPEC S at C3: must exit 0 with no bad node; report the last output line. A bad
node whose lone re-run exits 0 is reported as such with both readings, and is not a STOP; a bad
node whose lone re-run fails is.

G7 THE TREE, after C4 and the push. `git status --porcelain` prints `''`; C0a to C4 are
single-parent commits in that order on `fc13ba87`; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f261-cli-vocabulary-v2`; `git worktree list` prints one row, and
`git branch --list 'remedy/job-*'` prints 16 lines.

## The handback, C4

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 6 of feature F261 · round 24 · rounds so far 24`, with one sentence of context
self-assessment. `## Commits` lists C0a to C3, each row's `+/-` cell equal to constraint 5's
reading of that commit and its deletions column; C4's own numbers appear nowhere, per item 31 of
§3. `## Verification` gives G1 to G6 with real exit codes. It states the open findings at 125 by
distinct id, with the High ids R-0803, R-0804 and R-0807, and `Operator questions open: 0`. Its
`## Next` names, in order: Phase 1 rule 1; the reviewer's verdict on round 24; and the
`settings` alias surface over `config`.

── SLICE PLAN24 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN24 sha256=bbe2ac62667f8bc0adff8a89b9c6afea4957b78de5b92c0c240de6c9391c83a7
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 24 continues T003. It books round 23's PASS, registers R-0931 for F273 and records
DECISION F261 D23, then deletes `job rerun` by one table and renames the group `teach` to
`teacher` by a second. `job fulfill` is deferred by D23, as `propose` is by D22.

## Next Steps

1. The `settings` alias surface over `config`, DECISION D-D of the feature file.
2. `job budget <id> set` over the run-contract budget fields and the token budget profile, with
   R-0906 and R-0909, and then `job fulfill`, which D23 defers until that write exists.
3. The `propose` group, with the DECISION its deletion needs about the two surviving gates D22
   names, and the F011 `--status` discriminator `tests/cli/test_job_stop.py` loses with it.
4. The rest of T003 in the inventory's order, with R-0767 and R-0894.
5. T004, which owes the visible group order of D4 and the README quickstart of R-0895.

## Risks

- 124 findings are open by distinct id before this round's record and 125 after it; three are
  High, R-0803, R-0804 and R-0807.
- The feature's soft limit of 25 rounds leaves one after this one, and the steps above are more
  than one round; the session that reaches the limit owes the scope report and executes the
  split-and-close default of operator amendment amend0905-throughput, placing the follow-up
  feature directly after F261 per amend0906.
- A deletion that would break a SURVIVING command is deferred to a round that can rule on it,
  never shipped with a finding: that is why `propose` and `job fulfill` are not in this round.
END PLAN24

── SLICE RECORD24 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD24 sha256=6885ec14d57311f97cd92dbbeb169b56acc50049df8d22f53d2ba0f5bbda9649

Gate: F261 R23 — the F261 round 23 entry. VERDICT PASS. Written by the planner and reviewer of session 41 after reading the committed range `21ab5e24`..`fc13ba87` and re-deriving every reading below; the worker's report was evidence for none of them. It is booked here by the first commit of round 24 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r23.md` at `db1a231f` and `.agent/last_block.md` at `bc7f6f9d` are byte-identical to the reviewer's scratch original, sha256 `a6ea2722c2b6b65cb3ad84551fc05b1836cfba3424bf1a66bf14abdb4d3ca1a9`, and the table committed at `9c6ca609` is byte-identical to the reviewer's carrier, sha256 `8bba3dcab8f2a759d2561e9294f56b23f83632e9ee0121bfe6db9263b2e9bc9c`, which is the research helper's table unamended. THE STATE: at `46d97b58` and again at `fc13ba87`, `.agent/plan.md` equals PLAN23, `.agent/live_review.md` and `.agent/decisions.md` equal their `21ab5e24` blobs followed by RECORD23 and DEC22, and `docs/roadmap/features/T2_F273.md` equals its `21ab5e24` blob with the pair P273C applied; the first paragraph of RECORD23 is byte-equal to the round 22 verdict carried in `.agent/handoff.md` at `21ab5e24`; the `Gate:` count reads 131 then 132, the distinct registered ids 129 then 133 with the delta exactly R-0927 to R-0930, the distinct `Done:` ids 9 then 9, and the open set 120 then 124. THE TABLE COMMIT: at `9c6ca609` the `apps`, `packages`, `scripts`, `tests`, `docs/guides`, `docs/system`, `docs/README.md`, `README.md` and `.claude` objects equal both the research helper's dry-run commit and the reviewer's own, which re-applied the table on `21ab5e24` with the reviewer's own applier, all nine; the path set is the dry run's fifteen plus the carrier, and `git show --numstat` reads 106 insertions against 489 deletions, the dry run's 64 plus the carrier's 42 rows. THE SWEEP, with the patterns of the reviewer's gate carrier read as argv: the deleted-word pattern reads 60 lines in 12 files at `21ab5e24` and 6 lines at `fc13ba87`, all in `tests/test_command_catalog.py` and all the new `TestDeletedCommands` ids; `tests/cli/test_worker_cli_runtime.py` is absent while `packages/orchestration/worker_queue.py` survives; THE CONTROL on the `propose` group DECISION F261 D22 keeps deferred reads 67 lines in 11 files at both revisions. THE RED-PROOFS ran in the reviewer's own worktree on a tree whose objects the table commit reproduces, twice: a control of 357 passed at exit 0, and each of the five rows of the mutation carrier `cb14d8a8895d94d8b6d999908ccd4c114620149f0227bc5f9f4ab05816557201` exiting 1 with its named node the only failure — re-inserting the `job.enqueue` catalog entry, restoring the `worker.run` dispatch entry, restoring the `mission ledger` hint of `mission run`, restoring a `worker run` fence in `docs/system/worker.md`, and restoring the cockpit worker section's `next_command`; every FROM is whole lines occurring exactly once. THE REVIEWER'S RUN in the primary checkout at `fc13ba87` of the round's own test files, the files nearest every production module it touched, `tests/cli/test_golden_path.py`, the whole of `tests/docs/`, `tests/ui_server/`, `tests/cli/test_propose_cli.py` and `tests/cli/test_propose_cli_runtime.py` as controls on the deferred group, and the proposal, task-execution and worker-execution tests read 1777 passed, and `python3 -m ruff check` over the twelve edited files that survive printed `All checks passed!`. The worker ran the full suite once in the primary checkout, as the block orders: exit 0, `17668 passed, 23 skipped, 1 warning in 1292.89s`, with no line-initial `FAILED ` or `ERROR ` in its transcript, which the reviewer read. The open set reads 124 by distinct id at `fc13ba87`.

- R-0931 — Medium, THE RUN-INPUT DRIFT CHECK F012 SHIPPED HAS NO COMMAND, AND THE MANIFEST DIFF FUNCTIONS KEEP ONLY TEST CALLERS. Raised by the planner and reviewer of session 41 while preparing F261 round 24, from readings its research helper took at `fc13ba87` and the reviewer re-took on its own dry-run tree, after searching the open set for the run manifest, drift and the rerun word under §3 item 30: no open finding describes it; R-0906 names the run contract's budget writers and not the manifest check. THE DEFECT, read at `fc13ba87`: `job rerun <id> --check-manifest` in `apps/cli/commands/job_rerun_cmd.py` loaded a job's recorded run-input manifest, rebuilt the manifest the current environment would produce and diffed the two, exiting 0 on fully verified same inputs, 4 on blocking drift and 5 on incomplete coverage, and this round deletes it under DECISION amend0905-vocab D4, which gives `job` no `rerun`. Measured by the helper against a scratch data root and target repository: an unchanged target exited 5, the same target after an edit exited 4 with `target_tree` blocking, while `job evidence` wrote a `manifest_integrity.json` reading `ok: true` that was byte-identical before and after the edit, so it checks the manifest's integrity and not drift, and `job show --full --json` carries no drift field. After the table, `build_current_candidate`, `diff_manifests`, `load_latest_manifest_for_cli`, `CanonicalLoadResult`, `DIFF_VERSION`, `_INPUT_COVERAGE_IDENTITIES`, `_input_coverage`, `_diff_calls` and `_job_is_resumable` are named in production nowhere outside `packages/orchestration/run_manifest.py`, which stays whole under DECISION F261 D17's rule because the run path writes manifests through it. `docs/roadmap/features/T0_F012.md` still names the command as accepted history, and `tests/docs/test_docs_consistency.py` pins that line. WHY MEDIUM: an accepted operator check leaves with no heir; nothing prints anything false. WHY F273's: a drift view under a surviving word changes what that word does, which F261's Do-not-touch section excludes. FIX: a read-only drift section under a D4 word, for example `job show --full`, over `build_current_candidate` and `diff_manifests`, with its verdict pinned by a test that edits the target; or delete the diff functions with their tests by DECISION and say in the F012 system documentation that the check is gone. Owner: F273.
END RECORD24

── SLICE DEC23 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC23 sha256=1e08ad587f5f5a562f9816bbcd3d386ca9fbd4703417522f2a0ac33d268c7dc6

## DECISION F261 D23 (2026-09-16, F261 round 24) — the deletion paragraph of `job rerun`, why `job fulfill` is not in this round, and the `teach` group becomes `teacher`

CONTEXT. DECISION amend0905-vocab D4 gives `job` neither `rerun` nor `fulfill`, and `.agent/f261_t003_inventory.md` puts both in its round L; the operator ruling of 2026-09-11, DECISION amend0911-feedback D1, names the group `teach` as `teacher`, and the inventory puts that rename in its round N with ruling 10 open on whether file and function names follow. Measured at `fc13ba87` by two research helpers in their own detached worktrees, and re-applied by the reviewer on its own dry-run trees, the second table regenerated by its generator on the first table's commit and byte-identical to the one built on `fc13ba87`.

CHOSEN, FIRST: `job rerun` goes — its catalog entry, `apps/cli/commands/job_rerun_cmd.py` with its dispatch wiring and allowlist line, the CLI-driven classes of `tests/cli/test_job_rerun_manifest.py` and `tests/cli/test_job_rerun_integrity_errors.py`, the README quickstart line, and the docstrings of `run_manifest.py` and `worktrees.py` that named the word; the manifest loader and diff tests that drive the package directly stay. THE HEIR: none, measured — R-0931 records the loss and the diff functions that become test-only.

CHOSEN, SECOND: `job fulfill` is DEFERRED, on the rule DECISION F261 D21 applied to `propose`. The helper measured at `fc13ba87` that `remedy test run` refuses a job whose run contract allows 0 test runs, which `build_default_run_contract` sets, and that the fixture contract `job_fulfillment.py` saves with `max_test_runs=3` is the only production write of a non-zero budget, so deleting `fulfill` would leave `test run` refused on every new job — a SURVIVING command breaking, which R-0906 already records for the deleted `contract set`. The word goes in the round that builds `job budget <id> set`, the write DECISION amend0905-vocab D4 gives that budget, or later.

CHOSEN, THIRD: the group `teach` becomes `teacher`, with the old word deleted and no alias, as DECISION D-B of `docs/roadmap/features/T2_F261.md` requires. Ruling 10 is taken as WORDS AND NAMES: `apps/cli/commands/teach_cmd.py` moves to `teacher_cmd.py`, `tests/cli/test_teach_cmd.py` to `test_teacher_cmd.py`, `_cmd_teach_*` to `_cmd_teacher_*` and `TestTeach*` to `TestTeacher*`, as DECISION F261 D12 moved `plan_cmd.py` with its group; the two ids join `TestRenamedCommands`, and one operator quotation in the moved test file's docstring is re-spelled to the new word with its date kept. The package modules already read `teacher_model` and `teacher_qa`. Kept on purpose, and listed by the round's sweep: the D4 list and its 2026-09-11 clarification in `docs/system/vocabulary.md`, which F259 owns and which records the rename itself, and the ordinary verb "teach" in four prose lines. The round's gates order the canary `tests/cli/test_golden_path.py` run at the deletion commit and again at the rename commit, one rename per commit.

CONSEQUENCE. `remedy job rerun` and `remedy teach` are unknown words, `remedy teacher narrate` and `remedy teacher ask` carry the teacher role, and the catalog reads 30 groups and 154 commands. The eighteen-slot visible order and its data-pinned test are still T004's. HOW TO REVERSE: revert the round's two table commits and delete this section.
END DEC23

── SLICE P273D-FROM ── target `docs/roadmap/features/T2_F273.md` ── REWRITE FROM ──
BEGIN P273D-FROM sha256=ac8aa4ad2c8277c4c4fc0824f93952646951e0c1538964e655b3546c677b8290
  of a `mission run`, with its test.

## Do not touch
END P273D-FROM

── SLICE P273D-TO ── target `docs/roadmap/features/T2_F273.md` ── REWRITE TO ──
BEGIN P273D-TO sha256=2c179aea8ca65cfcf66c159338581af79acdfcd8818f47c3cfe34b535a45b87c
  of a `mission run`, with its test.
- R-0931 carries a resolution line naming the surviving view that reports run-input drift with the test
  that edits the target, or the DECISION and the commit that deleted the manifest diff functions.

## Do not touch
END P273D-TO
