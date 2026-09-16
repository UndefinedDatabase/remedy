── STEP T002/8 — F261 — ROUND 12 ──
Goal: Book round 11's PASS and the resolutions of R-0901 and R-0902, record DECISION F261 D11,
and give the job-result sense of `promote` apply words, with a guard test that holds the kept
senses, in four commits by applying four tables; run the suite once.

Base commit: `a75814c6`, on `feature/f261-cli-vocabulary-v2`. SESSION 3 of F261. Read AGENTS.md,
docs/agents/self_drive_protocol.md, and DECISIONs F261 D6 and D11 once C1 has landed D11.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block is a run
of a single repeated character, and every box-drawing rule inside the STEP and SLICE header
lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)` and `$?` in a compound command are refused by form, so write such checks
as Python scripts under `.remedy-wt/f261r12w/`, and never name a script after a standard-library
module; a pipe into `tail` hides pytest's exit code. The editable install resolves `apps` and
`packages` to the PRIMARY checkout, so a pytest run inside a worktree goes through a runner
script that changes into the worktree, puts it first on `sys.path` and in `PYTHONPATH`, and
asserts `packages.orchestration.job_fulfillment` loaded from inside it. Never call `run_job` or a
runner yourself: a job run started from inside a checkout creates a `remedy/job-*` branch in it.
`git branch --list 'remedy/job-*'` reads 16 lines now; keep it so.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f261-r12.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN12; slice RECORD12 is appended to
    `.agent/live_review.md` and slice DEC11 to `.agent/decisions.md`
C2  THE STAGING PIPELINE: copy `.remedy-wt/f261-block/f261-r12-staging.jsonl` to
    `.agent/authored/f261-r12-staging.jsonl` and apply it per THE TABLES, in one commit
C3  THE RUN LEVEL: the same with `f261-r12-run.jsonl`, in one commit
C4  THE REPAIR PROMPT: the same with `f261-r12-prompt.jsonl`, in one commit
C5  THE GUARD: the same with `f261-r12-guard.jsonl`, in one commit
C6  `.agent/handoff.md`, the handback; then `git push origin feature/f261-cli-vocabulary-v2`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f261-r12.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md` and `.agent/decisions.md`. C2 to C5: each table's own carrier and the
paths G3 names. C6: `.agent/handoff.md`.

## The appends

RECORD12 and DEC11 each begin with an empty line, and both targets end in a newline at
`a75814c6`: an append is the file's bytes followed by the slice's bytes, and nothing else.

## THE TABLES

Each carrier holds one JSON array per line. Their sha256 digests, to verify before copying:
`f261-r12-staging.jsonl` `135761a9a5f78ceb6cfeecd680d2608f1e5a476f37f9ee9a3d102544553d9a43`,
`f261-r12-run.jsonl` `55178efb73f806533e89190dc6dc33636dc48c38dd951665c8bf7614c198dab3`,
`f261-r12-prompt.jsonl` `755eb74f3cfdc7aa091b0917fb04d8a90dbc56a14e87da0d8d746f5517613965`,
`f261-r12-guard.jsonl` `66402eafbf440a0d96093c376fb47a17fbaadbd898e46becc033f7b91cadebef`.
Apply the rows strictly
in file order, each against the tree as the previous rows left it, from the repository root:
`["edit", path, old, new, count]` opens the path with `encoding="utf-8", newline=""`, requires
the number of occurrences of `old` to equal `count` exactly, and replaces every occurrence with
`new`; `["delete", path]` removes the file; `["move", src, dst]` renames the file, whose target
must not exist; `["create", path, content]` writes `content` to a path that must not exist, with
the same encoding and newline setting. A count that differs or a target that exists is a STOP:
touch nothing further, commit nothing of that table, and hand back with the row and the reading.
Stage each commit with `git add -A` after its table and its carrier. The tables are the
reviewer's measured dry run of DECISION F261 D11: the staging table its CHOSEN FIRST, the run
table its CHOSEN SECOND, the prompt table its CHOSEN THIRD, and the guard table the renames of
prose and test names by the same ruling and its CHOSEN FIFTH.

## SPEC S — the suite, once, after G5 and before C6

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f261r12w/`. Report pytest's return code, the run's last output line, and every
distinct bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `.
Re-run each bad node alone, once, the same way, and report that return code beside it.

## Constraints

1. NO SLICE AND NO TABLE IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C6, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f261r12w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f261-block/` and your
   own directory. `git worktree list` reads one row now; leave it so. Create no symlink.
5. Every commit stays under 500 insertions, read as the first column of `git show --numstat
   --format= <commit>` with git's default rename detection.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph beyond the two RECORD12 carries, and no `Landed:` line.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 285 lines TOTAL and 217 lines of PROSE,
   against the caps of 490 and 400.
8. GATE ORDER. G1 and G2 after C1; G3, G4 and G5 after C5; then SPEC S, whose result is G6; G7
   after C6 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r12.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; each committed carrier's sha256 equals its digest above.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN12, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its `a75814c6` blob
followed by RECORD12, and `.agent/decisions.md` its `a75814c6` blob followed by DEC11. Over
`.agent/live_review.md`: `^Gate: F\d+ R\d+ — ` reads 120 at `a75814c6` and 121 at C1, with
`Gate: F261 R11 — ` once at C1; distinct `^- R-\d+ — ` ids 105 and 105; distinct
`^Done: R-\d+ — ` ids 6 and 8, C1 minus base exactly `R-0901` and `R-0902`; the open set by
distinct id 99 and 97.

G3 THE TABLES, at C2, C3, C4 and C5. `git diff --no-renames --name-only` from each commit's
parent prints exactly that commit's carrier and: at C2 `apps/cli/commands/job.py`, `apps/ui/src/api/humanizeCatalog.ts`, `docs/system/first-fulfilled-job-demo-v0.md`, `packages/orchestration/job_fulfillment.py`, `packages/orchestration/staging_workspace.py`, `tests/cli/test_job_report.py`, `tests/orchestration/test_fence_production_e2e.py` and `tests/orchestration/test_job_fulfillment.py`; at C3 `apps/cli/commands/do_cmd.py`, `apps/ui/src/api/humanizeCatalog.ts`, `packages/orchestration/agent_run_trace.py`, `packages/orchestration/pingpong_evidence.py`, `packages/orchestration/pingpong_loop.py`, `tests/orchestration/test_evidence_bundle.py` and `tests/orchestration/test_repair_loop.py`; at C4
`packages/orchestration/pingpong_loop.py` and `tests/orchestration/test_builder_prompt_golden.py`; at C5 `apps/cli/command_catalog.py`, `docs/roadmap/features/T2_F261.md`, `docs/system/self-use-track-v1.md`, `packages/orchestration/final_verifier.py`, `packages/orchestration/job_evidence.py`, `packages/orchestration/pingpong_job.py`, `packages/orchestration/self_use_job.py`, `packages/orchestration/self_use_runner.py`, `packages/orchestration/token_measurement.py`, `scripts/build_review_manifest.py`, `tests/cli/test_task_input.py`, `tests/docs/test_retired_promote_word.py`, `tests/orchestration/test_final_verifier.py`, `tests/orchestration/test_job_task_runner.py`, `tests/orchestration/test_review_final_verifier_reproducible.py`, `tests/orchestration/test_review_gate_embedded_verdicts.py` and `tests/orchestration/test_self_use_runner.py`. `git rev-parse <commit>:<object>` equals the dry run, for
`apps`, `tests`, `docs`, `scripts`, `packages` and `README.md` in that order: C2 `34149b9ba9c13c731c32bc40addae28f854c1c48`, `ac75c12366724c7a2a8afe9ee153f8a4735725fa`, `a806f9ec99ef116d3d80f762a6e3ffa654d24f59`, `68e16104807fd30c528b58559e4d7968d011ef48`, `36e5e18bf75b99999665a9e0dc8a3f6b51432c62`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`;
C3 `db1fd362f0487035e883aa31ebbd78598a26984d`, `f497a3733c61dd7e667793ea813d5ef836d0356f`, `a806f9ec99ef116d3d80f762a6e3ffa654d24f59`, `68e16104807fd30c528b58559e4d7968d011ef48`, `58ec80b5874bb61d738ac5d959a1d73e5567b8d9`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`; C4 `db1fd362f0487035e883aa31ebbd78598a26984d`, `dcec9a3a509b6b1854486d9790563629af1d829d`, `a806f9ec99ef116d3d80f762a6e3ffa654d24f59`, `68e16104807fd30c528b58559e4d7968d011ef48`, `c0c391ae525b2b334955a539442b49d83eaa75f5`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`; C5 `fbc3f1d7e67e9c1d52347b80e58ef1b228eb1be4`, `0f80e084907c5e1ce5f8da08c469845ea4d06caf`, `43175c761c057c2c37403fe449653981c52a8b43`, `e3c01bde145e2c323bf157e1bb4a97cdaaa747cc`, `0e39ea4b746aee228ea56e5a3ed92565f135fe00`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`. Report each commit's insertions per constraint 5.

G4 THE SWEEP, at C5. `git grep -n -I -i -E 'staging_promoted|promote_staged_changes|promotion_readiness|promotion_allowed|promotion_files|files_promoted|target_not_promoted|no_promotion_files|requires_target_promotion|promotion_dry_run_completed|PromotionResult'
<C5> -- apps packages scripts tests docs README.md ':!docs/roadmap'` exits 1 and prints nothing.
`python3 -m ruff check` over every `.py` path of C2 to C5 exits 0.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f261r12w/wt <C5's sha>`, each run
through the runner over `tests/docs/test_retired_promote_word.py`,
`tests/orchestration/test_repair_loop.py`, `tests/orchestration/test_builder_prompt_golden.py`,
`tests/orchestration/test_job_fulfillment.py`, `tests/cli/test_job_report.py` and
`tests/orchestration/test_evidence_bundle.py` with `-rf --tb=no`. Mutation <n> is in the file
its line below names, replaces the bytes of slice MUT-<n>-FROM, whose count there must read 1,
with those of slice MUT-<n>-TO, is left unstaged, and is restored with
`git -C .remedy-wt/f261r12w/wt checkout -- <that file>`. (a) CONTROL: must exit 0. Each of (1)
to (5) must exit 1 with the named node among the failed nodes:
(1) `packages/orchestration/job_fulfillment.py`, the old field beside the new one:
`test_no_file_outside_the_map_carries_the_word`;
(2) `packages/orchestration/model_routing.py`, a job-result token among the routing words:
`test_no_kept_file_carries_a_token_outside_its_set`;
(3) `packages/runtimes/dev_server.py`, a kept token gone:
`test_every_token_listed_for_a_file_still_occurs_in_it`;
(4) `packages/orchestration/pingpong_loop.py`, the old repair prompt line:
`test_segments_reassemble_into_the_frozen_render[full]`;
(5) `packages/orchestration/pingpong_loop.py`, apply never allowed:
`TestFinalAdjudication::test_no_findings_ready`.
Report each exit code, summary line and number of failed nodes; then
`git worktree remove --force .remedy-wt/f261r12w/wt` and read `git branch --list 'remedy/job-*'`.

G6 THE SUITE, SPEC S at C5: must exit 0 with no bad node; report the last output line. A bad
node whose lone re-run exits 0 is reported as such with both readings, and is not a STOP; a bad
node whose lone re-run fails is.

G7 THE TREE, after C6 and the push. `git status --porcelain` prints `''`; C0a to C6 are
single-parent commits in that order on `a75814c6`; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f261-cli-vocabulary-v2`; `git worktree list` prints one row, and
`git branch --list 'remedy/job-*'` prints 16 lines.

## The handback, C6

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 3 of feature F261 · round 12 · rounds so far 12`, with one sentence of context
self-assessment. `## Commits` lists C0a to C5, each row's `+/-` cell equal to constraint 5's
reading of that commit and its deletions column; C6's own numbers appear nowhere, per item 31 of
§3. `## Verification` gives G1 to G6 with real exit codes. It states the open findings at 97 by
distinct id, with the High ids R-0803, R-0804 and R-0807, and `Operator questions open: 0`. Its
`## Next` names, in order: Phase 1 rule 1; the reviewer's verdict on round 12; the plan of T003,
the prune to D4, split by group.

── SLICE PLAN12 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN12 sha256=42fffe8356bf17b5700ace8acc4d12330d5af4014fe98a968ae800652e934050
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 12 finishes T002. It books round 11's PASS and the resolutions of R-0901 and R-0902 and
records DECISION F261 D11, then gives the job-result sense of `promote` apply words in the
staging pipeline, at the run level and in the builder's repair prompt, and adds
`tests/docs/test_retired_promote_word.py`, which holds the senses DECISION amend0905-vocab D5
keeps by file and token, one table per commit.

## Next Steps

1. T003, the prune to D4, with R-0900, its split planned by group before its first round.
2. T004, the descriptions, role labels, help wrapping and the remaining Acceptance tests.

## Risks

- 99 findings are open by distinct id before this round's record and 97 after it; three are
  High, R-0803, R-0804 and R-0807.
- `job show` prints JSON that the canary, `tests/cli/test_plan_approval.py` and
  `scripts/remedy_smoke.sh` parse, so every change to it only adds keys.
- T003 deletes groups and flags across the catalog and is the slice most likely to exceed the
  commit-size cap.
END PLAN12

── SLICE RECORD12 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD12 sha256=00e618a8652252328f93a0aedf53c3968edff661c9bcb3c94e0a7a9db58d3eba

Gate: F261 R11 — the F261 round 11 entry. VERDICT PASS. Written by the planner and reviewer of session 38 after reading the committed range `25a97421`..`a75814c6` and re-deriving the readings below; the worker's report was evidence for none of them. It is booked here by the first commit of round 12 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r11.md` at `434ba2e6` and `.agent/last_block.md` at `c4479ef2` are byte-identical to the reviewer's scratch original, sha256 `b940e63ba6455709fd401599064e13f19ea7b119a635369271c2dde93e9a27b4`, and the four tables committed at `5c138db1`, `e7a26a2f`, `03ffb0f1` and `585eb7af` are byte-identical to the reviewer's. THE STATE: at `e4293dd4` and again at `a75814c6`, `.agent/plan.md` equals PLAN11 and `.agent/decisions.md` equals its `25a97421` blob followed by DEC10; `.agent/live_review.md` equals its `25a97421` blob followed by RECORD11 at `e4293dd4`, and followed by RECORD11 and LANDED11 at `d2398063` and again at `a75814c6`. THE TABLE COMMITS: at `5c138db1`, `e7a26a2f`, `03ffb0f1` and `585eb7af` the `apps`, `tests`, `docs`, `scripts`, `packages` and `README.md` objects equal the reviewer's dry-run commits of the tables, which had reproduced the research helper's trees exactly; each commit's `--no-renames` path set is the dry run's plus its carrier, and `git show --numstat` reads 68, 347, 32 and 34 insertions. In the dry run's production diff the report section computes what `_cmd_job_report` computed and adds the run report `_cmd_job_run_report` rendered, in the mode the job's terminal status gives, `do job-report` goes with only its handler and catalog entry, and `_cmd_show_job` catches `JobStoreError`. At `a75814c6` the fixed-string grep of `"job.report"`, `"do.job-report"` and the three deleted handler names prints only their two `DELETED` entries in `tests/test_command_catalog.py`, and the grep of `remedy job report`, `remedy do job-report` or `job-report` over `apps`, `packages`, `scripts`, `docs` without `docs/roadmap`, and `README.md` exits 1 with no output. In the reviewer's dry run a full suite under `-n auto` without `tests/ui_server` read 1 failed, `test_vitest_passes`, and 17669 passed. Over `tests/cli/test_job_show.py`, `tests/test_command_catalog.py`, `tests/cli/test_job_report.py`, `tests/cli/test_open_decisions_view.py`, `tests/cli/test_product_spine.py`, `tests/orchestration/test_job_fulfillment.py`, `tests/cli/test_advertised_commands.py` and `tests/orchestration/test_job_task_runner.py`, which passed 478 unmutated, restoring a `job.report` handler row failed 1 test, making every report final failed 8, swapping the status and report registry entries failed 1, restoring the `do job-report` hint for a blocked job failed 2, leaving `JobStoreError` uncaught failed 2, and dropping the progress view from the report text failed 7. The record slices applied on top of the dry run passed `tests/docs/`, `tests/ui_server/test_dashboard_contract.py` and the other files the reviewer ran among those that read the edited state files, apart from `test_vitest_passes`, at 850 passed. THE REVIEWER'S RUN in the primary checkout at `a75814c6` of those eight files, `tests/cli/test_plan_approval.py`, `tests/cli/test_golden_path.py`, `tests/docs/`, `tests/ui_server/test_dashboard_contract.py`, `tests/orchestration/test_event_replay.py` and `tests/orchestration/test_run_report.py` read 1033 passed, and `git branch --list 'remedy/job-*'` read 16 lines. The open set reads 99 by distinct id at `a75814c6`.

Done: R-0901 — RESOLVED by F261 round 11. `5c138db1` gives the `code_applied` row of the status-section field table in `docs/system/first-perfect-job-demo-v0.md` the expected value `false` and the meaning `Nothing is applied without approval`, where it read `(not in status)`. Verified by the reviewer of session 38: the `docs` object of `5c138db1` equals the reviewer's dry run; at `a75814c6` `_status_section` in `apps/cli/commands/job.py` writes `code_applied` from `_extract_job_truth`, which starts it false and sets it only from a patch intent apply record in state `applied`, a `fulfillment_applied` run event or the latest fulfillment record of a job that used staging, none of which the demo's run writes before an approval; and `tests/docs/` passed in the reviewer's run at `a75814c6`.

Done: R-0902 — RESOLVED by F261 round 11. `585eb7af` makes `_cmd_show_job` catch `JobStoreError` beside `JobNotFoundError`, print `Error: <message>` on stderr and exit 1, and adds `tests/cli/test_job_show.py::TestAnUnreadableJobRecord`, which overwrites a saved job's record with `{not json` at the path `data_paths.job_record_path` gives and requires exit 1, the stderr line `Error: Unreadable job record for <id>` and empty stdout, with and without `--full`. Verified by the reviewer of session 38: the objects of `585eb7af` equal the reviewer's dry run, in which restoring the single `except JobNotFoundError` failed both cases of that test, and the test passed in the reviewer's run at `a75814c6`.
END RECORD12

── SLICE DEC11 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC11 sha256=657dbbe70991c2bb324554220071bd24f7c323703bfe3926afd5fd692d90ea87

## DECISION F261 D11 (2026-09-15, F261 round 12) — the run-level `promote` words: the job-result sense takes apply words, the other senses and the names accepted evidence carries stay, and a test holds the rest by file and token

CONTEXT. DECISION amend0905-vocab D5 makes `apply` replace `promote` as the job-result verb and keeps the word in its other senses, and DECISION F261 D6 renamed the words of `job_apply.py` and left the rest to this step. Measured at `a75814c6` by the reviewer's research helper and re-read by the reviewer on the dry-run trees: most lines matching `promot` in any case under `apps`, `packages`, `scripts`, `tests`, `docs` without `docs/roadmap`, and `README.md` belong to model routing, F110's model promoted into a task class; D5's record of kept occurrences is part (a) of R-0802 in `.agent/live_review_archive.md` and covers feature files and the reviewer prompt only. D6's CONSEQUENCE is corrected here: `promotion_readiness` is read by `do evidence`, not `do report`, and `promoted` is not a job state `RunState` defines but a word in a comment of `packages/orchestration/pingpong_job.py` about values in records on disk, which stays.

CHOSEN, FIRST: THE STAGING PIPELINE. The act of `job fulfill` copying staged files into the target repository is a target apply. `promote_staged_changes` becomes `apply_staged_changes_to_target` and returns a `TargetApplyResult` with `applied` and `files_applied_to_target`; the fulfillment record's `staging_promoted` and `promotion_files` become `applied_to_target` and `files_applied_to_target`, and so do the keys of its export, of the status and report sections of `job show --full` and of its run events; the contract's `requires_target_promotion` becomes `requires_target_apply`, its blocker codes `target_not_promoted` and `no_promotion_files` become `target_not_applied` and `no_files_applied_to_target`, and the run event `staging_promoted` becomes `staging_applied_to_target`, with its UI catalog entry in the same commit. The new names avoid `applied_at` and `files_applied`, which already name fields of the patch apply record and the job apply result.

CHOSEN, SECOND: THE RUN LEVEL. The `do evidence` manifest key `promotion_readiness` becomes `apply_readiness`, with its heading and summaries; the final adjudication's `promotion_allowed` becomes `apply_allowed`, printed as `Apply: allowed` or `Apply: blocked`; the trace event kind `promotion_dry_run_completed` becomes `apply_dry_run_completed`; and the `do` group's description reads `Run, report, and apply Remedy tasks.`

CHOSEN, THIRD: THE REPAIR PROMPT. The builder's repair instruction `Do not promote, commit, or push.` becomes `Do not apply changes to the target repository, commit, or push.`, in a commit of its own with both frozen renders of `tests/orchestration/test_builder_prompt_golden.py`, because a bare "do not apply" could read to a builder as "make no edits".

CHOSEN, FOURTH: WHAT STAYS. The commit gate key `promote_ready` and the recommended actions of `packages/orchestration/final_verifier.py` keep their spelling: the evidence bundles of accepted features committed under `.data/evidence_exports/` carry them, `scripts/build_review_manifest.py` checks such a bundle's `promote_ready` key, and the final verifier's reproducibility check re-derives its report with those strings. The lines that quote D5 or guard the retired word stay, and so does every occurrence in a sense D5 keeps.

CHOSEN, FIFTH: THE GUARD. `tests/docs/test_retired_promote_word.py` reads every file `git ls-files` lists under `apps`, `packages`, `scripts`, `tests`, `docs` and `README.md` outside `docs/roadmap/`, and holds the tokens of every line matching `promot` against `KEPT_BY_SENSE`, which gives each file that may carry the word one sense and the tokens it may carry: no other file may carry the word, no kept file may carry another token, and every listed token must still occur in its file. The Acceptance bullet of `docs/roadmap/features/T2_F261.md` that grepped for `promote` names this test for its promote half, because a plain grep also matches the senses D5 keeps; its flight-plan half is unchanged and belongs to T003.

CONSEQUENCE. Fulfillment records, run events and evidence manifests written before this round keep the old keys and nothing reads them, as DECISION D-A of `docs/roadmap/features/T2_F261.md` allows. A new occurrence of the word fails the guard until its sense is decided and written into the map. HOW TO REVERSE: revert the round's four table commits and delete this section.
END DEC11

── SLICE MUT-1-FROM ── G5 (1) only ── never a file ──
BEGIN MUT-1-FROM sha256=59249e040e1c7f02a12d92e05dd30574132869c26c59fec0c005cd658743d786
    applied_to_target: bool = False
END MUT-1-FROM

── SLICE MUT-1-TO ── G5 (1) only ── never a file ──
BEGIN MUT-1-TO sha256=e096c3ec44a86aa825058d5227c1f75a89cb25d872a5562d87f84f159c3813cd
    applied_to_target: bool = False
    staging_promoted: bool = False
END MUT-1-TO

── SLICE MUT-2-FROM ── G5 (2) only ── never a file ──
BEGIN MUT-2-FROM sha256=13fcf5a29a7f69285bc1a573f34067384af725e014189d7a3237090d6a2310c8
#: The three promotion-rule names, in the order violations are reported.
END MUT-2-FROM

── SLICE MUT-2-TO ── G5 (2) only ── never a file ──
BEGIN MUT-2-TO sha256=9603c13f03ed74df246cc1bd306d6289d0761937689a1eb5f964811846941e39
#: The three promotion-rule names, in the order violations are reported.
#: promotion_readiness
END MUT-2-TO

── SLICE MUT-3-FROM ── G5 (3) only ── never a file ──
BEGIN MUT-3-FROM sha256=656ce4777f3da632e6b2171d941fcbb740d789344bea752459a3c6879a97f992
        atomic. State is persisted as ``starting``: only readiness promotes it.
END MUT-3-FROM

── SLICE MUT-3-TO ── G5 (3) only ── never a file ──
BEGIN MUT-3-TO sha256=7213f36781a3904cf3a3314d5118803c025309193f42726e6f73c1ab973b774e
        atomic. State is persisted as ``starting``: only readiness moves it on.
END MUT-3-TO

── SLICE MUT-4-FROM ── G5 (4) only ── never a file ──
BEGIN MUT-4-FROM sha256=fdaa76ce0b27e6d6713b78413e2f13835cf1c8142d8aeb7cf8b783a5e1fdfc93
            "Do not touch the target repo. Do not apply changes to the target repository, commit, or push.\n",
END MUT-4-FROM

── SLICE MUT-4-TO ── G5 (4) only ── never a file ──
BEGIN MUT-4-TO sha256=3d1b7e39dee5827998a085eb4287e152016b6aad586013cec8421381c465ec1b
            "Do not touch the target repo. Do not promote, commit, or push.\n",
END MUT-4-TO

── SLICE MUT-5-FROM ── G5 (5) only ── never a file ──
BEGIN MUT-5-FROM sha256=f0257f0170362981d955a60ad907e27aa2903093b5bcbb2ad0359bf7e7d3b311
        adj.reason = "no_open_findings"
        adj.apply_allowed = True
END MUT-5-FROM

── SLICE MUT-5-TO ── G5 (5) only ── never a file ──
BEGIN MUT-5-TO sha256=7841a4f00efdf27fe290c16cc7e9cbda6254bda1964fd2380f85f4230ea92d9b
        adj.reason = "no_open_findings"
        adj.apply_allowed = False
END MUT-5-TO
