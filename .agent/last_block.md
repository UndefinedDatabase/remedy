── STEP T002/6 — F261 — ROUND 10 ──
Goal: Book round 9's PASS, register R-0901, record DECISION F261 D9, and fold `job digest`,
`job summary` and `job status` into `job show --full` in three commits by applying three
tables; run the suite once.

Base commit: `a00c1624`, on `feature/f261-cli-vocabulary-v2`. SESSION 3 of F261. Read AGENTS.md,
docs/agents/self_drive_protocol.md, and DECISIONs F261 D7, D8 and D9 once C1 has landed D9.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block is a run
of a single repeated character, and every box-drawing rule inside the STEP and SLICE header
lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)` and `$?` in a compound command are refused by form, so write such checks
as Python scripts under `.remedy-wt/f261r10w/`, and never name a script after a standard-library
module; a pipe into `tail` hides pytest's exit code. The editable install resolves `apps` and
`packages` to the PRIMARY checkout, so a pytest run inside a worktree goes through a runner
script that changes into the worktree, puts it first on `sys.path` and in `PYTHONPATH`, and
asserts `apps.cli.commands.job` loaded from inside it. Never call `run_job` or a runner yourself:
a job run started from inside a checkout creates a `remedy/job-*` branch in it.
`git branch --list 'remedy/job-*'` reads 16 lines now; keep it so.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f261-r10.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN10; slice RECORD10 is appended to
    `.agent/live_review.md` and slice DEC9 to `.agent/decisions.md`
C2  THE DIGEST FOLD: copy `.remedy-wt/f261-block/f261-r10-fold-1.jsonl` to
    `.agent/authored/f261-r10-fold-1.jsonl` and apply it per THE TABLES, in one commit
C3  THE SUMMARY FOLD: the same with `f261-r10-fold-2.jsonl`, in one commit
C4  THE STATUS FOLD: the same with `f261-r10-fold-3.jsonl`, in one commit
C5  `.agent/handoff.md`, the handback; then `git push origin feature/f261-cli-vocabulary-v2`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f261-r10.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md` and `.agent/decisions.md`. C2 to C4: each table's own carrier and the
paths G3 names. C5: `.agent/handoff.md`.

## The appends

RECORD10 and DEC9 each begin with an empty line, and both targets end in a newline at
`a00c1624`: an append is the file's bytes followed by the slice's bytes, and nothing else.

## THE TABLES

Each carrier holds one JSON array per line. Their sha256 digests, to verify before copying:
`f261-r10-fold-1.jsonl` `b7cfcbed8c02a270f0864cae0d9efe17761f6f6719cbed4b587c4d2da6cfe68e`,
`f261-r10-fold-2.jsonl` `e1cb068aa05e2f8879a61caa06bdd86c87b144a6a60daa3bf20c9cc5b49d9fe9`,
`f261-r10-fold-3.jsonl` `b14b2aa8ad6de7866e243174063dee46de6e89d81fc725a62c85f69a10e1ca10`.
Apply the rows strictly
in file order, each against the tree as the previous rows left it, from the repository root:
`["edit", path, old, new, count]` opens the path with `encoding="utf-8", newline=""`, requires
the number of occurrences of `old` to equal `count` exactly, and replaces every occurrence with
`new`; `["delete", path]` removes the file; `["move", src, dst]` renames the file, whose target
must not exist; `["create", path, content]` writes `content` to a path that must not exist, with
the same encoding and newline setting. A count that differs or a target that exists is a STOP:
touch nothing further, commit nothing of that table, and hand back with the row and the reading.
Stage each commit with `git add -A` after its table and its carrier. The tables are the
reviewer's measured dry run of DECISION F261 D9: fold-1 its CHOSEN FIRST, fold-2 its CHOSEN
SECOND, and fold-3 its CHOSEN THIRD.

## SPEC S — the suite, once, after G5 and before C5

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f261r10w/`. Report pytest's return code, the run's last output line, and every
distinct bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `.
Re-run each bad node alone, once, the same way, and report that return code beside it.

## Constraints

1. NO SLICE AND NO TABLE IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C5, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f261r10w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f261-block/` and your
   own directory. `git worktree list` reads one row now; leave it so. Create no symlink.
5. Every commit stays under 500 insertions, read as the first column of `git show --numstat
   --format= <commit>` with git's default rename detection.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 292 lines TOTAL and 226 lines of PROSE,
   against the caps of 490 and 400.
8. GATE ORDER. G1 and G2 after C1; G3, G4 and G5 after C4; then SPEC S, whose result is G6; G7
   after C5 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r10.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; each committed carrier's sha256 equals its digest above.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN10, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its `a00c1624` blob
followed by RECORD10, and `.agent/decisions.md` its `a00c1624` blob followed by DEC9. Over
`.agent/live_review.md`: `^Gate: F\d+ R\d+ — ` reads 118 at `a00c1624` and 119 at C1, with
`Gate: F261 R9 — ` once at C1; distinct `^- R-\d+ — ` ids 103 and 104, C1 minus base exactly
`R-0901`; distinct `^Done: R-\d+ — ` ids 6 and 6; the open set by distinct id 97 and 98.

G3 THE FOLDS, at C2, C3 and C4. `git diff --no-renames --name-only` from each commit's parent
prints exactly that commit's carrier and: at C2 `README.md`, `apps/cli/command_catalog.py`,
`apps/cli/commands/job.py`, `packages/orchestration/job_digest.py`,
`tests/cli/test_job_digest_cli.py`, `tests/cli/test_job_show.py`, `tests/test_command_catalog.py`
and `tests/ui_contracts/test_decision_urgency_parity.py`; at C3 `apps/cli/command_catalog.py`,
`apps/cli/commands/job.py`, `docs/guides/simple-operator-quickstart-v0.md`,
`packages/orchestration/event_replay.py`, `packages/orchestration/ui_server.py`,
`tests/cli/test_job_show.py`, `tests/test_command_catalog.py` and
`tests/ui_server/test_dashboard_contract.py`; at C4 `apps/cli/command_catalog.py`,
`apps/cli/commands/job.py`, `docs/guides/simple-operator-quickstart-v0.md`,
`docs/system/core-product-spine-v0.md`, `docs/system/first-fulfilled-job-demo-v0.md`,
`docs/system/first-perfect-job-demo-v0.md`, `packages/orchestration/run_report.py`,
`scripts/remedy_smoke.sh`, `tests/cli/test_job_show.py`, `tests/cli/test_open_decisions_view.py`,
`tests/cli/test_plan_approval.py`, `tests/cli/test_product_spine.py`,
`tests/orchestration/test_job_fulfillment.py` and `tests/test_command_catalog.py`.
`git rev-parse <commit>:<object>` equals the dry run, for `apps`, `tests`, `docs`, `scripts`,
`packages` and `README.md` in that order: C2 `80d1da4c4c7c0ee10cffee649652b0e018530fe4`, `b2126781106cca151f31fefa8a14a084f7b61d8a`, `d74ed73f2a078c66e6c60f11370bfb581892e704`, `fb0b7d81f311c40c72f4ff1e30c51dd74efd4f06`, `6d7aff6a499ba248c9963ab51306aa613ba4ed0e`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`; C3 `f996a904da9b597a03f2aa064decb74972d62af9`, `e3248c39083942cb3c932e0b571499cd619a9c2a`, `618a425091887943bf78f0c1265bdce7dccaa469`, `fb0b7d81f311c40c72f4ff1e30c51dd74efd4f06`, `b9d7334d589f71ed5fb0ee86121dfb35a31c7e96`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`; C4 `36d6d17bd21f9a3338258f946130fbb242b62b3c`, `56e365a3fd4ef667edde9bca61fc6ae6d57de04d`, `d02995d35969a26eb40f2be7130e388b0d94687e`, `68e16104807fd30c528b58559e4d7968d011ef48`, `f8b5f7a16a7d83bdf2f6eb09a04a4115e67b8376`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`.
Report each commit's insertions per constraint 5.

G4 THE SWEEP, at C4. `git grep -n -I -F -e '"job.digest"' -e '"job.summary"' -e '"job.status"'
-e _cmd_job_digest -e _cmd_job_summary -e _cmd_job_status <C4> -- apps packages scripts tests
docs README.md ':!docs/roadmap'` prints exactly three lines, the `DELETED` entries of those three
ids in `tests/test_command_catalog.py`. `git grep -n -I -E 'remedy job (digest|summary|status)\b'
<C4> -- apps packages scripts tests docs README.md ':!docs/roadmap'` exits 1 and prints nothing.
`python3 -m ruff check` over every `.py` path of C2, C3 and C4 exits 0, and
`bash -n scripts/remedy_smoke.sh` exits 0.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f261r10w/wt <C4's sha>`, each run
through the runner over `tests/cli/test_job_show.py`, `tests/test_command_catalog.py`,
`tests/cli/test_job_digest_cli.py`, `tests/cli/test_open_decisions_view.py`,
`tests/cli/test_product_spine.py`, `tests/orchestration/test_job_fulfillment.py` and
`tests/cli/test_advertised_commands.py` with `-rf --tb=no`. Every mutation is in
`apps/cli/commands/job.py`, replaces the bytes of slice MUT-<n>-FROM, whose count there must
read 1, with those of slice MUT-<n>-TO, and is restored with
`git -C .remedy-wt/f261r10w/wt checkout -- apps/cli/commands/job.py`. (a) CONTROL: must exit 0.
Each of (1) to (5) must exit 1 with the named node among the failed nodes:
(1) a `job.status` handler row: `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table`;
(2) the digest wrapped in a key: `TestJsonModeMatchesTheEnvelopeExactly::test_the_payload_is_not_wrapped_in_an_extra_key`;
(3) a summary that is never live: `TestSummarySection::test_a_job_with_run_events_is_live`;
(4) the open decisions printed after the job line:
`TestJobStatusView::test_the_open_decision_block_is_printed_first`;
(5) two registry entries swapped: `TestSections::test_full_prints_the_registered_sections_in_the_d4_order`.
Report each exit code, summary line and number of failed nodes; then
`git worktree remove --force .remedy-wt/f261r10w/wt` and read `git branch --list 'remedy/job-*'`.

G6 THE SUITE, SPEC S at C4: must exit 0 with no bad node; report the last output line. A bad
node whose lone re-run exits 0 is reported as such with both readings, and is not a STOP; a bad
node whose lone re-run fails is.

G7 THE TREE, after C5 and the push. `git status --porcelain` prints `''`; C0a to C5 are
single-parent commits in that order on `a00c1624`; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f261-cli-vocabulary-v2`; `git worktree list` prints one row, and
`git branch --list 'remedy/job-*'` prints 16 lines.

## The handback, C5

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 3 of feature F261 · round 10 · rounds so far 10`, with one sentence of context
self-assessment. `## Commits` lists C0a to C4, each row's `+/-` cell equal to constraint 5's
reading of that commit and its deletions column; C5's own numbers appear nowhere, per item 31 of
§3. `## Verification` gives G1 to G6 with real exit codes. It states the open findings at 98 by
distinct id, with the High ids R-0803, R-0804 and R-0807, and `Operator questions open: 0`. Its
`## Next` names, in order: Phase 1 rule 1; the reviewer's verdict on round 10; the fold of
`job report` and the deletion of `do job-report`.

── SLICE PLAN10 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN10 sha256=c0fa52eb0a7dd07f795b0bd147cf3e1591e8465f7865e2ecc4f99b7d4ac1063c
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 10 continues T002. It books round 9's PASS, registers R-0901 and records DECISION F261
D9, then folds `job digest`, `job summary` and `job status` into sections of `job show --full`,
one command per commit, each applying a table the round saves under `.agent/authored/` and
adding the command's id to the deleted-command guard.

## Next Steps

1. The fold of `job report` with its `--final` and `--interim` forms and the deletion of
   `do job-report`, with their hints, their `related=` tuples and R-0901.
2. The run-level promote words DECISION F261 D6 leaves, ruled by sense, with the kept-by-sense
   list DECISION amend0905-vocab D5 names written into the record and a test for the
   Acceptance grep of the retired word.
3. T003, the prune to D4, with R-0900; then T004.

## Risks

- 97 findings are open by distinct id before this round's record and 98 after it; three are
  High, R-0803, R-0804 and R-0807.
- `job show` prints JSON that the canary, `tests/cli/test_plan_approval.py` and
  `scripts/remedy_smoke.sh` parse, so every change to it only adds keys.
- `job report` carries the most read tests and printed hints left to fold, so its hints may
  need a commit of their own ahead of the fold to keep each commit under 500 insertions.
END PLAN10

── SLICE RECORD10 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD10 sha256=4eb039973a956530eda42b565bb62a46d9da9af846192e71418917e4d2cd771a

Gate: F261 R9 — the F261 round 9 entry. VERDICT PASS. Written by the planner and reviewer of session 37 after reading the committed range `aff2b676`..`2923b992` and re-deriving the readings below; the worker's report was evidence for none of them. It is carried by `.agent/handoff.md` in the session-close commit that follows `2923b992` and booked by the first commit of round 10 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r9.md` at `da6f26fe` and `.agent/last_block.md` at `743c09be` are byte-identical to the reviewer's scratch original, sha256 `41710658bb8d027160387a4b0f83c8a2d96d3eaa63d1881a214641ca8c4c4fdb`, and the three tables committed at `9d6b8791`, `d683f3ed` and `64e54c35` are byte-identical to the reviewer's. THE STATE: at `873d8e49` and again at `2923b992`, `.agent/plan.md` equals PLAN9 and `.agent/live_review.md` and `.agent/decisions.md` equal their `aff2b676` blobs followed by RECORD9 and DEC8. THE FOLDS: at `9d6b8791`, `d683f3ed` and `64e54c35` the `apps`, `packages`, `tests`, `scripts`, `docs` and `README.md` objects equal the reviewer's dry-run commits of the tables, which had reproduced the research helper's trees exactly; each commit's `--no-renames` path set is the dry run's plus its carrier, and `git show --numstat` reads 74, 213 and 91 insertions. In the dry run's production diff each section builder computes what its deleted handler computed, with the handler's prints turned into returned lines, and `_build_show_sections` turns a `ShowSectionError` into an envelope with that error's code. At `64e54c35` the fixed-string grep of the three quoted ids and handler names prints only their `DELETED` entries in `tests/test_command_catalog.py`, the grep of `remedy job assumptions`, `fences` or `dod` exits 1 with no output, and ruff over the round's touched `.py` files exits 0. In the reviewer's dry run a full suite under `-n auto` without `tests/ui_server` read 1 failed, `test_vitest_passes`, and 17684 passed; over `tests/cli/test_job_show.py`, `tests/test_command_catalog.py`, `tests/cli/test_decision_answers.py`, `tests/orchestration/test_fence_e2e.py`, `tests/orchestration/test_fence_production_e2e.py` and `tests/orchestration/test_dod_gate.py`, which passed 256 unmutated, restoring a `job.fences` handler row failed 1 test, raising a plain `RuntimeError` for a missing target repository failed 1, swapping two registry entries failed 1, dropping the dod `check_count` key failed 2 and emptying the assumptions markdown failed 2. THE REVIEWER'S RUN in the primary checkout at `2923b992` of those six files, `tests/cli/test_advertised_commands.py`, `tests/docs/`, `tests/ui_server/test_dashboard_contract.py` and `tests/cli/test_golden_path.py` read 688 passed, and `git branch --list 'remedy/job-*'` read 16 lines. The open set reads 97 by distinct id at `2923b992`.

- R-0901 — Low, THE DEMO PAGE `docs/system/first-perfect-job-demo-v0.md` SAYS THE JOB STATUS VIEW DOES NOT CARRY `code_applied`, WHILE THAT VIEW PRINTS THE KEY. Raised by the planner and reviewer of session 38 while preparing F261 round 10, after searching the open set for the page and for `not in status` under §3 item 30: no open finding describes it. THE DEFECT, read at `a00c1624`: the page's table of the fields of `job status --json` gives `code_applied` the expected value `(not in status)` with the meaning `Status does not claim apply`, while `_cmd_job_status` in `apps/cli/commands/job.py` writes `code_applied` from `_extract_job_truth` into the payload it prints, between `approval_required` and `latest_stop_reason`. The reviewer read the page and the code and ran neither the demo nor the command. WHY LOW: a reader of the demo is told a field is absent that the output shows, and nothing executes the table. WHY F261's: the fold of `job report` rewrites the same page's tables. FIX: the row gives the value the status section prints for the demo job, and the page's field tables are read against the data of the sections they describe. Owner: F261.
END RECORD10

── SLICE DEC9 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC9 sha256=3c2b7184ccfabbf81864ddde67f7c0f83549988597f30717ba3172a77aec5d12

## DECISION F261 D9 (2026-09-15, F261 round 10) — the deletion paragraph of `job digest`, `job summary` and `job status`

CONTEXT. DECISIONs F261 D7 and D8 made the read views of a job sections of `job show --full` and folded four of them. This round folds three more, one per commit, in D4's order. Measured at `a00c1624` by the reviewer's research helper and re-read by the reviewer on the dry-run trees.

CHOSEN, FIRST: `job digest`. Deleted: the catalog entry `job.digest` with its comment, its handler-table row and `_cmd_job_digest`. THE HEIR is the `digest` section: its data is the envelope `build_job_digest` returns, unchanged, the same call `_build_digest_json` in `packages/orchestration/ui_server.py` makes for the completion digest route, and its text is the former output. `README.md`, the docstring of `packages/orchestration/job_digest.py` and `tests/ui_contracts/test_decision_urgency_parity.py` name the section.

CHOSEN, SECOND: `job summary`. Deleted: the catalog entry `job.summary`, its handler-table row and `_cmd_job_summary`. THE HEIR is the `summary` section: its data holds the keys of the former payload in their order, and its text is the former output. The next-step hints of `packages/orchestration/event_replay.py` and `packages/orchestration/ui_server.py` name `remedy job show <id> --full --json`. `tests/cli/test_job_show.py` gains `TestSummarySection`, which reads the section for a job without run events and for a job with them, because until this round only source-text tests under `tests/ui_server` named the view.

CHOSEN, THIRD: `job status`. Deleted: the catalog entry `job.status`, its handler-table row and `_cmd_job_status`. THE HEIR is the `status` section: its data holds the keys of the former payload in their order, the open decisions among them, and its text is the former output with the open-decision block first. Its next safe action names the job by its full id where the command echoed the id as typed, and it names `remedy job report` until that command folds. `scripts/remedy_smoke.sh` reads `sections.status.data` of `job show --full --json` from stdin, because the escaped newlines in that JSON become control characters inside the Python string literal the script used; the quickstart guide and `docs/system/core-product-spine-v0.md`, `docs/system/first-fulfilled-job-demo-v0.md` and `docs/system/first-perfect-job-demo-v0.md` name the section.

CONSEQUENCE. `remedy job digest`, `remedy job summary` and `remedy job status` exit with an argument error, and their ids join `TestDeletedCommands`. A test that pinned a deleted catalog entry or handler row is deleted, because `TestDeletedCommands` pins the absence, and so is a test of a deleted command's unknown-id output where a `job show` test already covers an unknown id. The registry holds `permissions`, `fences`, `assumptions`, `digest`, `summary`, `status` and `dod`, in D4's order. The done count R-0898 names is now computed by `_summary_section`, `_status_section` and `_cmd_job_report`. `job report` relates to `job show` alone, and `job fulfill` to `job show` and `job report`. HOW TO REVERSE: revert the round's three table commits and delete this section.
END DEC9

── SLICE MUT-1-FROM ── G5 (1) only ── never a file ──
BEGIN MUT-1-FROM sha256=9489ee8832c4a185bac13752680fe3080f85e39ca8e9549c661b18e925664c3b
    "job.fulfill": lambda args: _cmd_job_fulfill(
END MUT-1-FROM

── SLICE MUT-1-TO ── G5 (1) only ── never a file ──
BEGIN MUT-1-TO sha256=7cdf678d2c61c19fb627e1768d2c911f792f4fc66393468922cef2477b542980
    "job.status": lambda args: None,
    "job.fulfill": lambda args: _cmd_job_fulfill(
END MUT-1-TO

── SLICE MUT-2-FROM ── G5 (2) only ── never a file ──
BEGIN MUT-2-FROM sha256=3aa9d4aa6537de9ea09316ff777c1582c4c3c534dec019bd24fb61c89d08caf3
    return digest, lines
END MUT-2-FROM

── SLICE MUT-2-TO ── G5 (2) only ── never a file ──
BEGIN MUT-2-TO sha256=7ebfc974f3c3d6d8f7ba86ee73a6b7fe316953fb04f912ba596b518196a0a56e
    return {"digest": digest}, lines
END MUT-2-TO

── SLICE MUT-3-FROM ── G5 (3) only ── never a file ──
BEGIN MUT-3-FROM sha256=44de823c63ce6773ec4af14b299504bc36848e08707607dc882a794042b4756f
    has_real_events = event_count > 0
END MUT-3-FROM

── SLICE MUT-3-TO ── G5 (3) only ── never a file ──
BEGIN MUT-3-TO sha256=950647c9abb8c9c78e07804910a5ee7df0ebc643e0cb393db22c25e30bbddcf3
    has_real_events = False
END MUT-3-TO

── SLICE MUT-4-FROM ── G5 (4) only ── never a file ──
BEGIN MUT-4-FROM sha256=98766fa827a0b615b6a37cd67e3cc8ac484c47e293fe13daa4a43d65f7332f98
        *open_decision_view["lines"],
        f"Job {job.job_id}",
END MUT-4-FROM

── SLICE MUT-4-TO ── G5 (4) only ── never a file ──
BEGIN MUT-4-TO sha256=1cc809d7366895d4905c623ecc08b658c0185c2fa1f7d71ee9679aa48f6ce06e
        f"Job {job.job_id}",
        *open_decision_view["lines"],
END MUT-4-TO

── SLICE MUT-5-FROM ── G5 (5) only ── never a file ──
BEGIN MUT-5-FROM sha256=7f83d98ee0e8f90aaefa4a0a54a9d8841a7513520af2de7eb8be93ddcca2c46a
    ("summary", _summary_section),
    ("status", _status_section),
END MUT-5-FROM

── SLICE MUT-5-TO ── G5 (5) only ── never a file ──
BEGIN MUT-5-TO sha256=7be1d36c1fb3d76a9b56cdfdeb932228a494e166dacfd501041db604ec62c2b2
    ("status", _status_section),
    ("summary", _summary_section),
END MUT-5-TO
