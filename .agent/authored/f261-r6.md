── STEP T002/2 — F261 — ROUND 6 ──
Goal: Book round 5's PASS, record DECISION F261 D5, and rename `job_promote.py` to `job_apply.py`
with its test files and then its identifiers, in two commits by applying two tables; run the suite once.

Base commit: `a1c42d72`, on `feature/f261-cli-vocabulary-v2`. SESSION 2 of F261. Read AGENTS.md,
docs/agents/self_drive_protocol.md, and DECISIONs F261 D4 and D5 once C1 has landed D5.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block is a run
of a single repeated character, and every box-drawing rule inside the STEP and SLICE header
lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)` and `$?` in a compound command are refused by form, so write such checks
as Python scripts under `.remedy-wt/f261r6w/`; a pipe into `tail` hides pytest's exit code. The
editable install resolves `apps` and `packages` to the PRIMARY checkout, so a pytest run inside a
worktree goes through a runner script that changes into the worktree, puts it first on
`sys.path` and in `PYTHONPATH`, and asserts `packages.orchestration.job_apply` loaded from inside it.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f261-r6.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN6; slice RECORD6 is appended to
    `.agent/live_review.md` and slice DEC5 to `.agent/decisions.md`
C2  THE MODULE RENAME: copy `.remedy-wt/f261-block/f261-r6-rename-1.jsonl` to
    `.agent/authored/f261-r6-rename-1.jsonl` and apply it per THE TABLES, in one commit
C3  THE IDENTIFIERS: the same with `f261-r6-rename-2.jsonl`, in one commit
C4  `.agent/handoff.md`, the handback; then `git push origin feature/f261-cli-vocabulary-v2`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f261-r6.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md` and `.agent/decisions.md`. C2 and C3: each table's own carrier and the
paths G3 and G4 name. C4: `.agent/handoff.md`.

## The appends

RECORD6 and DEC5 each begin with an empty line, and both targets end in a newline at `a1c42d72`:
an append is the file's bytes followed by the slice's bytes, and nothing else. RECORD6 is the
`Gate: F261 R5 — ` paragraph of `.agent/handoff.md` at `a1c42d72`, byte for byte.

## THE TABLES

Each carrier holds one JSON array per line. The sha256 of `f261-r6-rename-1.jsonl` is
`04842b38d640455bbef9e1edd7fe960f75e240fbc1ea516ae2fd0e84231da4a1` and that of `f261-r6-rename-2.jsonl` is
`3602beb201f683ddd57f9b708c9ba79c6568929e34213d32c7f06c622718fd5e`; verify each before copying. Apply the rows strictly
in file order, each against the tree as the previous rows left it, from the repository root:
`["edit", path, old, new, count]` opens the path with `encoding="utf-8", newline=""`, requires
the number of occurrences of `old` to equal `count` exactly, and replaces every occurrence with
`new`; `["delete", path]` removes the file; `["move", src, dst]` renames the file, whose target
must not exist; `["create", path, content]` writes `content` to a path that must not exist, with
the same encoding and newline setting. A count that differs or a target that exists is a STOP:
touch nothing further, commit nothing of that table, and hand back with the row and the reading.
Stage each commit with `git add -A` after its table and its carrier. The tables are the
reviewer's measured dry run of DECISION F261 D5: table 1 moves the module and its two test files
and re-points every reference to the module; table 2 renames the identifiers D5 maps.

## SPEC S — the suite, once, after G5 and before C4

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f261r6w/`. Report pytest's return code, the run's last output line, and every
distinct bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `.
Re-run each bad node alone, once, the same way, and report that return code beside it.

## Constraints

1. NO SLICE AND NO TABLE IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C4, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f261r6w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f261-block/` and your
   own directory. `git worktree list` reads one row now; leave it so.
5. Every commit stays under 500 insertions, read as the first column of `git show --numstat
   --format= <commit>` with git's default rename detection, which is how C2's moves count.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 226 lines TOTAL and 175 lines of PROSE,
   against the caps of 490 and 400.
8. GATE ORDER. G1 and G2 after C1; G3 after C2; G4 and G5 after C3; then SPEC S, whose result is
   G6; G7 after C4 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r6.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; each committed carrier's sha256 equals its digest above.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN6, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its `a1c42d72` blob
followed by RECORD6, and `.agent/decisions.md` its `a1c42d72` blob followed by DEC5. Over
`.agent/live_review.md`: `^Gate: F\d+ R\d+ — ` reads 114 at `a1c42d72` and 115 at C1, with
`Gate: F261 R5 — ` once at C1; distinct `^- R-\d+ — ` ids 100 and 100; distinct
`^Done: R-\d+ — ` ids 4 and 4; the open set by distinct id 96 and 96, equal as sets.

G3 THE MODULE RENAME, at C2. `git diff --no-renames --name-only <C1> <C2>` prints exactly
`.agent/authored/f261-r6-rename-1.jsonl` and these: `apps/cli/commands/do_cmd.py`,
`packages/orchestration/job_apply.py`, `packages/orchestration/job_promote.py`,
`packages/orchestration/self_use_job.py`, `packages/orchestration/self_use_runner.py`,
`tests/orchestration/import_reachability_allowlist.txt`, `tests/orchestration/test_job_apply.py`,
`tests/orchestration/test_job_apply_consistency.py`, `tests/orchestration/test_job_promote.py`,
`tests/orchestration/test_job_promote_consistency.py`,
`tests/orchestration/test_job_worktree_handoff.py` and
`tests/orchestration/test_job_worktree_integrity.py`. `git rev-parse <C2>:<dir>` equals the dry
run: `apps` `4d544c9018a1423edad5152f697fde4ea93c40d7`, `packages` `a53510630e15c346742f9a70a07dfa5376e5a08d`,
`tests` `a4e7f6554bc2ea064d727d0a4f197f6ecfbf106e`; `scripts`, `docs` and `README.md` equal their objects
at `a1c42d72`. Report C2's insertions per constraint 5.

G4 THE IDENTIFIERS, at C3. `git diff --no-renames --name-only <C2> <C3>` prints exactly
`.agent/authored/f261-r6-rename-2.jsonl` and these: `apps/cli/commands/do_cmd.py`,
`packages/orchestration/job_apply.py`, `tests/orchestration/test_job_apply.py`,
`tests/orchestration/test_job_apply_consistency.py`,
`tests/orchestration/test_job_worktree_handoff.py` and
`tests/orchestration/test_job_worktree_integrity.py`. `git rev-parse <C3>:<dir>` equals the dry
run: `apps` `712eeb42e83fb80f3135dc818661dd9d551255c0`, `packages` `da8dbf9ba8526212d6ad8bbf928e79b82eab9df9`,
`tests` `637383130e627f15f94e476a539bcd2cb47519fe`; `scripts`, `docs` and `README.md` equal their objects
at `a1c42d72`. Report C3's insertions per constraint 5. `git grep -n -I -w -e promote_job -e
JobPromotionResult -e PromotionSource -e TaskPromoSummary -e _materialize_promotion_source -e
_materialize_promotion_source_owned -e _promote_from_workspace -e _persist_job_promotion -e
_cleanup_promotion_source -e export_job_promotion_json -e _next_step_for_promotion -e
load_job_promotion -e summarize_job_promotion -e _promotions_dir -e promo_source -e promo_dir -e
promo_file <C3> -- apps packages scripts tests docs ':!docs/roadmap'` exits 1 and prints nothing,
and `git grep -n -I -e job_promote <C3> -- apps packages scripts tests docs ':!docs/roadmap'`
exits 1 and prints nothing. `python3 -m ruff check` over every `.py` path of C2 and C3 that
exists at C3 exits 0.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f261r6w/wt <C3's sha>`, each run
through the runner over `tests/orchestration/test_job_apply.py` with `-rf --tb=no`. (a) CONTROL:
must exit 0. (b) In `apps/cli/commands/do_cmd.py` the bytes
`from packages.orchestration.job_apply import (`, whose count there must read 1, become
`from packages.orchestration.job_promote import (`: must exit 1 with
`TestCLICommandShape::test_cli_dry_run_json` among the failed nodes. Restore with
`git -C .remedy-wt/f261r6w/wt checkout -- apps/cli/commands/do_cmd.py`. (c) In
`packages/orchestration/job_apply.py` the bytes `def apply_job(`, count 1, become
`def promote_job(`: must exit 1 with `TestDryRunCompleted::test_completed_job_dry_run_ready`
among the failed nodes. Restore the same way. Report each exit code, summary line and number of
failed nodes; then `git worktree remove --force .remedy-wt/f261r6w/wt`.

G6 THE SUITE, SPEC S at C3: must exit 0 with no bad node; report the last output line.

G7 THE TREE, after C4 and the push. `git status --porcelain` prints `''`; C0a to C4 are
single-parent commits in that order on `a1c42d72`; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f261-cli-vocabulary-v2`; `git worktree list` prints one row.

## The handback, C4

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 2 of feature F261 · round 6 · rounds so far 6`, with one sentence of context
self-assessment. `## Commits` lists C0a to C3, each row's `+/-` cell equal to constraint 5's
reading of that commit and its deletions column; C4's own numbers appear nowhere, per item 31 of
§3. `## Verification` gives G1 to G6 with real exit codes. It states the open findings at 96 by
distinct id, with the High ids R-0803, R-0804, R-0806 and R-0807, and
`Operator questions open: 1`. Its `## Next` names, in order: Phase 1 rule 1; the reviewer's
verdict on round 6; the output-visible promote words of `job_apply.py`.

── SLICE PLAN6 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN6 sha256=9569f078dfbc49e6ecbcba8b49e031f5c3cbaef26e7dcddd31afbd2872c12f85
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 6 continues T002. It books round 5's PASS and records DECISION F261 D5, then renames
`packages/orchestration/job_promote.py` to `job_apply.py` with its two test files in one commit
and its Python identifiers to apply words in a second, each applying a table the round saves
under `.agent/authored/`. No string value, JSON key or name on disk changes in this round.

## Next Steps

1. The output-visible promote words of `job_apply.py`: its status values, reason codes, the
   record key `promotion_id`, the directory `job_promotions` and its human text, with the
   kept-by-sense list DECISION amend0905-vocab D5 names written into the record.
2. `job show --full` composing the read commands as sections, with the blocked-task findings
   R-0806 asks for and the fix R-0896 needs.
3. One commit per folded read command and `do job-report`, each adding its id to the guard.
4. The remaining run-level promote words, and a test for the Acceptance grep of the retired
   word; then T003, the prune to D4, and T004.

## Risks

- 96 findings are open by distinct id before and after this round's record; four are High,
  R-0803, R-0804, R-0806 and R-0807.
- `job show` prints JSON that the canary, `tests/cli/test_plan_approval.py` and
  `scripts/remedy_smoke.sh` parse, so its `--full` form only adds keys to that JSON.
- Renaming the status `promoted` to `applied` meets the task and manifest status `applied`
  that already exists; the words round rules on it before it renames.
END PLAN6

── SLICE RECORD6 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD6 sha256=fbf994279ea7b3592701238bdce08bf07871bbe5facafd5deb5c88eec5984c7d

Gate: F261 R5 — the F261 round 5 entry. VERDICT PASS. Written by the planner and reviewer of session 36 after reading the committed range `350fa353`..`2cef254d` and re-deriving the readings below; the worker's report was evidence for none of them. It is carried by `.agent/handoff.md` in the session-close commit that follows `2cef254d` and booked by the first commit of round 6 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r5.md` at `c0b5045a` and `.agent/last_block.md` at `871488f1` are byte-identical to the reviewer's scratch original, sha256 `6351d01cd98d59f4ce598f7e8278ccfd457be8e48e78f9cab50ee7138424e69c`, and `.agent/authored/f261-r5-delete-1.jsonl` at `592ab167` and `.agent/authored/f261-r5-delete-2.jsonl` at `3b860345` are byte-identical to the reviewer's tables. THE STATE: at `de5cd238` and again at `2cef254d`, `.agent/plan.md` equals PLAN5, `.agent/live_review.md` and `.agent/decisions.md` equal their `350fa353` blobs followed by RECORD5 and DEC4, and `docs/roadmap/features/T2_F268.md` equals its `350fa353` blob with pair P268B applied. THE DELETIONS: at `592ab167` the `apps`, `packages`, `tests`, `scripts` and `README.md` objects equal the reviewer's dry run of table 1, and at `3b860345` its dry run of tables 1 and 2, which had reproduced the research helper's trees `77eef6c5` and `ef2bc0e5` exactly; `docs` at both equals its object at `de5cd238`, and each commit's `--no-renames` path set is the dry run's plus its own carrier. In the reviewer's dry run a full suite under `-n auto` read 15 failed and 18152 passed, every failure in `tests/ui_server` or `test_vitest_passes`, classes the helper's base control also failed, and a `do.promote` handler-table entry failed `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table` alone. THE REVIEWER'S RUN in the primary checkout at `2cef254d` of `tests/test_command_catalog.py`, `tests/cli/test_cli_ux.py`, `tests/cli/test_product_spine.py`, `tests/orchestration/test_evidence_bundle.py`, `tests/orchestration/test_repair_loop.py`, `tests/orchestration/test_import_reachability.py`, `tests/cli/test_advertised_commands.py`, `tests/docs/`, `tests/ui_server/test_dashboard_contract.py` and `tests/cli/test_golden_path.py` read 766 passed. The open set reads 96 by distinct id at `2cef254d`.
END RECORD6

── SLICE DEC5 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC5 sha256=a678723e46243b8a17eb7aa40d068bbf4d36298335898ccd4bf4e574b50e1375

## DECISION F261 D5 (2026-09-15, F261 round 6) — the name map of the `job_apply.py` rename, and what it leaves to the words round

CONTEXT. DECISION F261 D4 orders the rename of `packages/orchestration/job_promote.py` to `job_apply.py` in three steps: the module and its test files, the identifiers, and the output-visible words. Round 6 lands the first two. This section fixes the names, so that the third step and every later reader find one spelling per concept, per the discoverability conventions of AGENTS.md.

CHOSEN, FIRST: THE FILES. `packages/orchestration/job_promote.py` becomes `packages/orchestration/job_apply.py`, `tests/orchestration/test_job_promote.py` becomes `tests/orchestration/test_job_apply.py`, and `tests/orchestration/test_job_promote_consistency.py` becomes `tests/orchestration/test_job_apply_consistency.py`. Every import of the module, every `patch`, `monkeypatch.setattr` and `__import__` target that names it, its `:mod:` references and its import-reachability allowlist line follow, and the module aliases `JP` and `jp_mod` in the tests become `job_apply`.

CHOSEN, SECOND: THE IDENTIFIERS. `promote_job` becomes `apply_job`, `JobPromotionResult` `JobApplyResult`, `TaskPromoSummary` `TaskApplySummary`, `PromotionSource` `ApplySource`, `export_job_promotion_json` `export_job_apply_json`, `summarize_job_promotion` `summarize_job_apply`, `load_job_promotion` `load_job_apply_record`, `_persist_job_promotion` `_persist_job_apply_record`, `_promotions_dir` `_apply_records_dir`, `_materialize_promotion_source` and `_materialize_promotion_source_owned` `_materialize_apply_source` and `_materialize_apply_source_owned`, `_cleanup_promotion_source` `_cleanup_apply_source`, `_promote_from_workspace` `_apply_from_workspace`, `_next_step_for_promotion` `_next_step_for_apply`, and the locals `promo_source`, `promo_dir` and `promo_file` `apply_source`, `record_dir` and `record_file`; the test classes and test functions of `test_job_apply.py`, `test_job_apply_consistency.py`, `test_job_worktree_handoff.py` and `test_job_worktree_integrity.py` that carry the word take an apply word in its place. `summarize_job_apply` is named for what it formats, the result, and `load_job_apply_record` for what it reads, the stored record. At `a1c42d72` none of the new names occurred in `apps`, `packages`, `scripts`, `tests` or `docs`.

CHOSEN, THIRD: WHAT THE WORDS ROUND INHERITS. The two tables change no string literal other than the module paths and names that `patch`, `monkeypatch.setattr` and `__import__` resolve. So the status values `promoted`, `promoted_test_failed`, `promoted_record_update_failed` and `promoted_cleanup_failed`, the reason codes that begin `promotion_` and `no_promotable_files`, the text `Promotion:` and `unpromoted`, and the temporary-directory prefix `remedy-promo-` that tests assert stay for the words round; so do the result field `promotion_id`, which is a JSON key and the stored record's file name, and the data directory `job_promotions`. Identifiers in files the tables do not touch are untouched, among them `promotion_allowed` in `packages/orchestration/pingpong_loop.py` and `TestPromotionSafetyReuse` in `tests/orchestration/test_job_task_runner.py`, and so are the other senses D5 keeps. The accepted feature files under `docs/roadmap/features/` that name the old module, its test file or `promote_job` are history and stay byte-identical, per D5.

CONSEQUENCE. No command, printed text, JSON key or file on disk changes. No test would fail if a module named `job_promote.py` were restored beside `job_apply.py`: the Acceptance grep of `docs/roadmap/features/T2_F261.md` is the check on the retired word, and T002's last promote step turns it into a test. HOW TO REVERSE: revert the round's two table commits and delete this section.
END DEC5
