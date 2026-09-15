── STEP T003/4 — F261 — ROUND 16 ──
Goal: Book round 15's PASS and its prose slip, register R-0905 for F273, record DECISION F261
D15, and delete the `guide`, `dashboard` and `repo` groups in three commits by applying three
tables; run the suite once.

Base commit: `782b4e02`, on `feature/f261-cli-vocabulary-v2`. SESSION 4 of F261. Read AGENTS.md,
docs/agents/self_drive_protocol.md, `.agent/f261_t003_inventory.md`, and DECISION F261 D15 once
C1 has landed it.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block that is two or
more characters long is a run of a single repeated character, and every box-drawing rule inside the STEP and SLICE header
lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)` and `$?` in a compound command are refused by form, so write such checks
as Python scripts under `.remedy-wt/f261r16w/`, and never name a script after a standard-library
module; a pipe into `tail` hides pytest's exit code. The editable install resolves `apps` and
`packages` to the PRIMARY checkout, so a pytest run inside a worktree goes through a runner
script that changes into the worktree, puts it first on `sys.path` and in `PYTHONPATH`, and
asserts `apps.cli.grouped` loaded from inside it. Never call `run_job` or a runner yourself: a
job run started from inside a checkout creates a `remedy/job-*` branch in it.
`git branch --list 'remedy/job-*'` reads 16 lines now; keep it so. While a deletion is staged
but not committed, `test_every_enumerated_path_exists_in_this_repo` fails; run no suite then.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f261-r16.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN16; slice RECORD16 is appended to
    `.agent/live_review.md`, slice DEC15 to `.agent/decisions.md` and slice SLIP16 to
    `.agent/prose_slips.md`; in `docs/roadmap/features/T2_F273.md` the bytes of slice P273-FROM
    are replaced by those of slice P273-TO
C2  THE GUIDE GROUP: copy `.remedy-wt/f261-block/f261-r16-guide.jsonl` to
    `.agent/authored/f261-r16-guide.jsonl` and apply it per THE TABLES, in one commit
C3  THE DASHBOARD GROUP: the same with `f261-r16-dashboard.jsonl`, in one commit
C4  THE REPO GROUP AND ITS DEV STATUS BLOCK: the same with `f261-r16-repo.jsonl`, in one commit
C5  `.agent/handoff.md`, the handback; then `git push origin feature/f261-cli-vocabulary-v2`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f261-r16.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md` and
`docs/roadmap/features/T2_F273.md`. C2 to C4: each table's own carrier and the paths G3 names.
C5: `.agent/handoff.md`.

## The appends and the pair

RECORD16, DEC15 and SLIP16 each begin with an empty line, and their targets end in a
newline at `782b4e02`: an append is the file's bytes followed by the slice's bytes, and nothing
else. The pair P273: TO contains FROM: false, so it is a REWRITE; P273-FROM occurs once
in `docs/roadmap/features/T2_F273.md` at `782b4e02`, and at C1 P273-FROM occurs 0 times and
P273-TO once.

## THE TABLES

Each carrier holds one JSON array per line. Their sha256 digests, to verify before copying:
`f261-r16-guide.jsonl` `b629cbf34ba4641d1f897f19a41dc8b8827000b2896c4b5520f8a5a558112256`,
`f261-r16-dashboard.jsonl` `d7cbe8ba9d79ec5e8a22e695167cd0639aaa84f6d5338fb06cd2ec6b3289ead1`,
`f261-r16-repo.jsonl` `d2c2ff35f200780e0e07f10f0e5ef63ca68dd76e2de6e8dcede0c354a8a433c4`.
Apply the rows strictly
in file order, each against the tree as the previous rows left it, from the repository root:
`["edit", path, old, new, count]` opens the path with `encoding="utf-8", newline=""`, requires
the number of occurrences of `old` to equal `count` exactly, and replaces every occurrence with
`new`; `["delete", path]` removes the file; `["move", src, dst]` renames the file, whose target
must not exist; `["create", path, content]` writes `content` to a path that must not exist, with
the same encoding and newline setting. A count that differs or a target that exists is a STOP:
touch nothing further, commit nothing of that table, and hand back with the row and the reading.
Stage each commit with `git add -A` after its table and its carrier. The tables are the
reviewer's measured dry run of DECISION F261 D15, applied on top of C1's record: the guide table
its CHOSEN FIRST, the dashboard table its CHOSEN SECOND and the repo table its CHOSEN THIRD.

## SPEC S — the suite, once, after G5 and before C5

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f261r16w/`. Report pytest's return code, the run's last output line, and every
distinct bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `.
Re-run each bad node alone, once, the same way, and report that return code beside it.

## Constraints

1. NO SLICE AND NO TABLE IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C5, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f261r16w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f261-block/` and your
   own directory. `git worktree list` reads one row now; leave it so. Create no symlink.
5. Every commit stays under 500 insertions, read as the first column of `git show --numstat
   --format= <commit>` with git's default rename detection.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph and no `Landed:` line.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 327 lines TOTAL and 246 lines of PROSE,
   against the caps of 490 and 400.
8. GATE ORDER. G1 and G2 after C1; G3, G4 and G5 after C4; then SPEC S, whose result is G6; G7
   after C5 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r16.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; each committed carrier's sha256 equals its digest above.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN16, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its `782b4e02` blob
followed by RECORD16, `.agent/decisions.md` its `782b4e02` blob followed by DEC15, and
`.agent/prose_slips.md` its `782b4e02` blob followed by SLIP16.
`docs/roadmap/features/T2_F273.md` equals its `782b4e02` blob with the pair P273 applied, with
the counts The appends and the pair give. Over `.agent/live_review.md`: `^Gate: F\d+ R\d+ — `
reads 124 at `782b4e02` and 125 at C1, with `Gate: F261 R15 — ` once at C1; distinct
`^- R-\d+ — ` ids 107 and 108, C1 minus base exactly `R-0905`; distinct `^Done: R-\d+ — ` ids 8
and 8; the open set by distinct id 99 and 100. `python3 -m pytest tests/docs/ -q` exits 0 at C1.

G3 THE TABLES, at C2, C3 and C4. `git diff --no-renames --name-only` from each commit's parent
prints exactly that commit's carrier and: at C2 `apps/cli/command_catalog.py`, `apps/cli/commands/__init__.py`, `apps/cli/commands/guide.py`, `packages/orchestration/brain_viewer.py`, `packages/orchestration/guidance.py`, `packages/orchestration/ui_server.py`, `scripts/remedy_smoke.sh`, `tests/cli/test_cli_ux.py`, `tests/orchestration/import_reachability_allowlist.txt`, `tests/orchestration/test_test_runner.py`, `tests/test_command_catalog.py`, `tests/test_data_paths.py`, `tests/ui_contracts/test_responsive.py` and `tests/ui_server/test_live_state.py`; at C3 `apps/cli/command_catalog.py`, `apps/cli/commands/__init__.py`, `apps/cli/commands/dashboard_cmd.py`, `packages/orchestration/brain_viewer.py`, `packages/orchestration/dashboard.py`, `packages/orchestration/guidance.py`, `scripts/remedy_smoke.sh`, `tests/orchestration/import_reachability_allowlist.txt`, `tests/test_command_catalog.py` and `tests/ui_server/test_dashboard_contract.py`; at C4
`apps/cli/command_catalog.py`, `apps/cli/commands/__init__.py`, `apps/cli/commands/dev.py`, `apps/cli/commands/repo.py`, `apps/ui/src/api/humanizeCatalog.ts`, `packages/orchestration/brain_detail.py`, `packages/orchestration/decision_queue.py`, `packages/orchestration/git_status.py`, `packages/orchestration/guidance.py`, `scripts/remedy_smoke.sh`, `tests/cli/test_command_catalog.py`, `tests/cli/test_job_commands.py`, `tests/orchestration/import_reachability_allowlist.txt`, `tests/orchestration/test_autonomy.py`, `tests/orchestration/test_decision_evidence.py`, `tests/orchestration/test_event_name_coupling.py`, `tests/orchestration/test_project_brain.py`, `tests/regression/test_named_bugs.py`, `tests/test_command_catalog.py`, `tests/test_data_paths.py`, `tests/test_remedy_smoke_script.py`, `tests/test_repair_context_reviewer_memory.py` and `tests/ui_contracts/test_ux_quality.py`. `git rev-parse <commit>:<object>` equals the reviewer's dry run, which applied C1's
record before the tables, for `apps`, `tests`, `docs`, `scripts`, `packages` and `README.md` in
that order: C2 `2fda7bfebd75f650c6d9d076ad7aae742e73d115`, `0703a4aa03910c2c2d7b0d5650b2e25aa14b3d51`, `7011cc224223ee0f93b1f8e9c4580541fe1495d2`, `d9bd174b6b8eafd21937c9eaa373b4714163adf0`, `c3fb9da9b9cc0427baafe1ccae92f805c6975606`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`; C3 `a905622a8cd70de5570c9980efb01678f61b4030`, `0432f04cd89b205d1ae954b6711d7a20e507f3bb`, `7011cc224223ee0f93b1f8e9c4580541fe1495d2`, `905fe83392dc21f8a719ad135f1164da208505a9`, `5596f804eabcbcef80e297b6a96586f53500b513`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`; C4 `febc8677a2f3fc2116e4c12e7ca9b27085d79fef`, `1d3216ce89c2b9a13b1fa043540b5f1f49fd6655`, `7011cc224223ee0f93b1f8e9c4580541fe1495d2`, `f4efd167393d503042688f2ab5cb16f0a6c50644`, `007cdcb33516473d5988a52cab5b79e9f8c9e13f`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`.
Report each commit's insertions per constraint 5.

G4 THE SWEEP, at C4. `git grep -n -I -E 'remedy (dashboard|repo)\b|remedy guide( job|$|[^ ])|commands[./](guide|repo|dashboard_cmd)\b|dashboard_cmd|orchestration[./]dashboard\b|_cmd_guide_job|_cmd_dashboard_job|_cmd_dashboard_project|_cmd_repo_status|_cmd_commit_readiness|_build_readiness_next_action|export_guidance_json|summarize_guidance|_build_guide_json|build_job_dashboard|build_project_dashboard|summarize_job_dashboard|export_git_status_json|summarize_git_status|commit_readiness_ok'
<C4> -- apps packages scripts tests docs README.md AGENTS.md .claude ':!docs/roadmap'` exits 1
and prints nothing. `python3 -m ruff check` over every `.py` path of C2 to C4 that still exists
at C4 exits 0.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f261r16w/wt <C4's sha>`, each run
through the runner over `tests/test_command_catalog.py`, `tests/cli/test_cli_ux.py`,
`tests/test_grouped_cli.py`, `tests/orchestration/test_import_reachability.py`,
`tests/cli/test_advertised_commands.py` and `tests/orchestration/test_event_name_coupling.py`
with `-rf --tb=no`. Mutation <n> is in the file its line below names, replaces the bytes of slice
MUT-<n>-FROM, whose count there must read 1, with those of slice MUT-<n>-TO, and is restored with
`git -C .remedy-wt/f261r16w/wt checkout -- <that file>`. (a) CONTROL: must exit 0. Each numbered
mutation must exit 1 with the named node among the failed nodes:
(1) `apps/cli/commands/dev.py`, a `guide` handler row:
`TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table`; (2)
`apps/cli/command_catalog.py`, the `repo` group restored without commands:
`TestCatalogIntegrity::test_every_group_has_at_least_one_command`; (3) the same file, the `ci`
group removed: `TestGroupDefIntegrity::test_all_groups_still_in_catalog`; (4) the same file, a
`related=` naming `dashboard.job`:
`TestCatalogIntegrity::test_every_related_reference_resolves_to_a_live_command`; (5)
`apps/cli/commands/dev.py`, the `repo commit-readiness` hint restored:
`test_every_advertised_command_exists_in_the_catalog`; (6)
`tests/orchestration/test_event_name_coupling.py`, `git_status_read` undeclared:
`TestEventNameCouplingRatchet::test_every_dead_coupling_is_declared`.
Report each exit code, summary line and number of failed nodes; then
`git worktree remove --force .remedy-wt/f261r16w/wt` and read `git branch --list 'remedy/job-*'`.

G6 THE SUITE, SPEC S at C4: must exit 0 with no bad node; report the last output line. A bad
node whose lone re-run exits 0 is reported as such with both readings, and is not a STOP; a bad
node whose lone re-run fails is.

G7 THE TREE, after C5 and the push. `git status --porcelain` prints `''`; C0a to C5 are
single-parent commits in that order on `782b4e02`; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f261-cli-vocabulary-v2`; `git worktree list` prints one row, and
`git branch --list 'remedy/job-*'` prints 16 lines.

## The handback, C5

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 4 of feature F261 · round 16 · rounds so far 16`, with one sentence of context
self-assessment. `## Commits` lists C0a to C4, each row's `+/-` cell equal to constraint 5's
reading of that commit and its deletions column; C5's own numbers appear nowhere, per item 31 of
§3. `## Verification` gives G1 to G6 with real exit codes. It states the open findings at 100 by
distinct id, with the High ids R-0803, R-0804 and R-0807, and `Operator questions open: 0`. Its
`## Next` names, in order: Phase 1 rule 1; the reviewer's verdict on round 16; the `readiness`
group, the `contract` group and the `policy` group, as the inventory proposes.

── SLICE PLAN16 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN16 sha256=27617676d463743055ebb442ff7579f9928d9bde60d5bf612a3e7e57546f22e5
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 16 continues T003. It books round 15's PASS and its prose slip, registers R-0905 for
F273 and records DECISION F261 D15, then deletes the `guide` group with the group-count guard,
the `dashboard` group, and the `repo` group with its `dev status` block, one table per commit.

## Next Steps

1. The `readiness` group, the `contract` group and its hints, and the `policy` group, as
   `.agent/f261_t003_inventory.md` proposes.
2. The rest of T003 in the inventory's order, each round re-measured before it is authored,
   with R-0767, R-0894 and R-0900.
3. T004.

## Risks

- 99 findings are open by distinct id before this round's record and 100 after it; three are
  High, R-0803, R-0804 and R-0807.
- The inventory proposes more rounds than F261's soft limit of 25 leaves; the session that
  reaches the limit owes the scope report and the split-and-close default.
- A deletion's consumers include shell strings, subprocess help calls, event readers and the
  UI event catalog, so every deletion round runs the whole suite on its committed tree.
END PLAN16

── SLICE RECORD16 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD16 sha256=4258222e167b4b6b354778f2ea5d29cad764680f5d8887ac6db178e6e8c44406

Gate: F261 R15 — the F261 round 15 entry. VERDICT PASS. Written by the planner and reviewer of session 39 after reading the committed range `8aa94f37`..`782b4e02` and re-deriving the readings below; the worker's report was evidence for none of them. It is booked here by the first commit of round 16 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r15.md` at `b08cb881` and `.agent/last_block.md` at `9b58103c` are byte-identical to the reviewer's scratch original, sha256 `5f62f9147cbf6ba6abc43e63e02cd95b132f62e5d3f326ae4ebdb93197889818`, and the three tables committed at `96a0f098`, `16d3940d` and `3055e98f` are byte-identical to the reviewer's. THE STATE: at `42fe8f07` and again at `782b4e02`, `.agent/plan.md` equals PLAN15, `.agent/live_review.md`, `.agent/decisions.md` and `.agent/prose_slips.md` equal their `8aa94f37` blobs followed by RECORD15, DEC14 and SLIP15, and `docs/roadmap/features/T2_F273.md` equals its `8aa94f37` blob with the pair P273 applied. THE TABLE COMMITS: at `96a0f098`, `16d3940d` and `3055e98f` the `apps`, `tests`, `docs`, `scripts`, `packages`, `README.md` and `.claude` objects equal the reviewer's dry-run commits, which applied the record before the tables and whose `apps`, `tests`, `scripts`, `packages`, `README.md` and `.claude` objects had reproduced the research helper's trees exactly; each commit's `--no-renames` path set is the dry run's plus its carrier, and `git show --numstat` reads 13, 18 and 16 insertions. In the dry run's production diff the loop modules leave with the run report's loop reference, the `queue` group leaves with its four commands and its handler module, and `job_queue.py` leaves with the F048 binding of `long_run_executor.py`, the two `queue.*` configuration keys and `queue_dir`, while `worker_queue.py` stays; every deleted symbol's production callers at `8aa94f37` were in the deleted code. The sweep pattern of the round 15 block matches in 20 files at `8aa94f37`, and at `782b4e02` the same `git grep` over `apps`, `packages`, `scripts`, `tests`, `docs` without `docs/roadmap`, `README.md`, `AGENTS.md` and `.claude` exits 1 with no output. In the reviewer's dry run a full suite under `-n auto` without `tests/ui_server` read 1 failed, `test_vitest_passes`, 17492 passed and 29 skipped, and the seven `tests/ui_server` files naming a queue or a loop read 300 passed and 1 skipped. Over `tests/test_command_catalog.py`, `tests/cli/test_cli_ux.py`, `tests/test_grouped_cli.py` and `tests/orchestration/test_import_reachability.py`, which passed 453 unmutated, a `queue` handler row, the `queue` group restored without commands, the `job_queue` allowlist line and the `loop_spec` allowlist line each failed 1 test. The worker declared that the block's frame rule, read literally, flags the two lines of a lone closing brace inside the MUT-1 slices, and edited nothing; the rule's sentence did not state a run's least length, and the slip is the reviewer's. THE REVIEWER'S RUN in the primary checkout at `782b4e02` of those four files, the run report, long-run executor, data paths, mission state, mission command, configuration, configuration command and worker queue tests, `tests/cli/test_golden_path.py`, `tests/cli/test_advertised_commands.py`, `tests/docs/`, `tests/test_remedy_smoke_script.py`, `tests/orchestration/test_command_discovery.py`, `tests/ui_server/test_dashboard_cockpit_truth.py`, `tests/ui_server/test_dashboard_contract.py` and `tests/ui_contracts/` read 2508 passed and 4 skipped, `python3 -m ruff check` over the eleven edited files that survive printed `All checks passed!`, and `git branch --list 'remedy/job-*'` read 16 lines. The open set reads 99 by distinct id at `782b4e02`.

- R-0905 — Low, ONCE `repo status` IS DELETED NOTHING WRITES THE `git_status_read` EVENT, WHILE THE READINESS SIGNAL, THE DIRTY-REPO DECISION AND THE DIRTY-REPO STOP REASON STILL READ IT. Raised by the planner and reviewer of session 39 while preparing F261 round 16, after searching the open set for `git_status_read` and `repo_dirty` under §3 item 30: no open finding describes it, and R-0832, which asked for the ratchet that measures such couplings, describes none of these readers. THE DEFECT, read at `782b4e02` and on the reviewer's dry-run trees of round 16: `_cmd_repo_status` in `apps/cli/commands/repo.py` is the only emitter of `git_status_read` under `apps`, `packages` and `scripts`, and the round deletes it with the `repo` group; `_has_git_status` in `packages/orchestration/autonomy_readiness.py` then reads false for every job, and the dirty-repo branches of `list_decisions` in `packages/orchestration/decision_queue.py` and of `derive_stop_reasons` in `packages/orchestration/stop_reasons.py` can no longer fire, while DECISION F261 D15 declares the name in `KNOWN_DEAD_EVENT_COUPLINGS` of `tests/orchestration/test_event_name_coupling.py` so the coupling stays visible. WHY LOW: each reader already returned exactly this for every job on which nobody ran `repo status`, and no command prints anything false. WHY F273's: deleting a decision type, a stop reason and a readiness signal with the tests that pin them, or giving the event a new emitter, changes surviving surfaces, which F261 does not. FIX: delete the three readers with their tests, or emit the event from a surviving command that reads the repository's status, and in either case take `git_status_read` out of `KNOWN_DEAD_EVENT_COUPLINGS` and lower `_COUPLING_CEILING` in the same commit. Owner: F273.
END RECORD16

── SLICE DEC15 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC15 sha256=bc6926de12cd1481d16c4399c997565aec795dc0349180bb29cc2c163685c488

## DECISION F261 D15 (2026-09-16, F261 round 16) — the deletion paragraph of the `guide`, `dashboard` and `repo` groups

CONTEXT. DECISION amend0905-vocab D4 deletes `guide`, `dashboard` and `repo`, and `.agent/f261_t003_inventory.md` puts them in its round C, with the group-count guard of `tests/cli/test_cli_ux.py` and the `dev status` block that called the `repo` group. Measured at `782b4e02` by the reviewer's research helper and re-read by the reviewer on the dry-run trees. As in DECISION F261 D13, a command's package code goes with it when the command was its only production caller, and, per ruling 2 of the inventory, a cockpit route whose payload is only a deleted command's output goes with it.

CHOSEN, FIRST: `guide`. Deleted: the group, `guide.job`, `apps/cli/commands/guide.py` and its tests; `export_guidance_json` and `summarize_guidance` in `packages/orchestration/guidance.py`, and the `guide` route of `packages/orchestration/ui_server.py`, whose payload was the output of `guide job --json` and which nothing in `apps/ui/src` requested; the guidance card that pointed at `dashboard job`, and the git-status card, whose import of `read_job_git_status` had no target in `packages/orchestration/git_status.py`, so the card could never be built; and the viewer's command suggestions for `dashboard job` and `guide job`. `build_guidance_cards` stays, because the cockpit's dashboard payload reads it. THE GUARD: `test_all_groups_still_in_catalog` asserted at least 40 groups, a floor written when groups were only hidden and never deleted; it now asserts that every group D4 keeps and the catalog already holds is still present, and `run` joins that set when this feature creates it. THE HEIR: the guidance cards of the web cockpit, opened with `remedy ui start`.

CHOSEN, SECOND: `dashboard`. Deleted: the group, `dashboard.job` and `dashboard.project`, `apps/cli/commands/dashboard_cmd.py`, `packages/orchestration/dashboard.py` and their tests. `dashboard project` failed on every call with the missing import R-0883 records, so that defect leaves with the command, and F273's closure resolves R-0883 citing this round. The web cockpit's own dashboard payload is built from surviving code and stays. THE HEIR: `remedy ui start` and `remedy brain cockpit`; the project view has no heir.

CHOSEN, THIRD: `repo`. Deleted: the group, `repo.status` and `repo.commit-readiness`, `apps/cli/commands/repo.py` and its tests; `export_git_status_json` and `summarize_git_status` in `packages/orchestration/git_status.py`, whose `read_git_status` stays for the brain graph; the commit-readiness block of `dev status` with its `commit_readiness_ok` key, its blocker and advisory lines and its hint; the git node's next action in `packages/orchestration/brain_detail.py`; the smoke script's `repo status` and commit-readiness sections; and the humanized sentence of `git_status_read`. `repo status` was the only emitter of `git_status_read`, which the readiness signal, the dirty-repo decision and the dirty-repo stop reason still read, so the event name joins `KNOWN_DEAD_EVENT_COUPLINGS` in `tests/orchestration/test_event_name_coupling.py` with its ceiling raised by one, the coupling stays declared rather than invisible, and R-0905 records the readers for F273. THE HEIR: the `git_status` node of `remedy brain graph <job> --json` for the branch, the head and whether the tree is clean, and `git status` itself for the file lists; the commit-readiness preview has no heir.

CONSEQUENCE. `remedy guide`, `remedy dashboard` and `remedy repo` are unknown commands and their ids join `TestDeletedCommands`; the cockpit API has no `guide` route; `dev status` prints no commit-readiness line. HOW TO REVERSE: revert the round's three table commits and delete this section.
END DEC15

── SLICE SLIP16 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIP16 sha256=8a4a1e30f77447afce450bf5a177baa83e5b5a2322fb6445b485afbdde0dd8ae

2026-09-15 · F261 R15 · THE FRAME RULE of the round 15 block said that no line is a run of a single repeated character and stated no least length, while two lines inside its MUT-1 slices are a lone closing brace; the reviewer's pre-emission check counted only lines of two or more characters, the worker read the sentence literally, found those two lines and declared them without editing anything, and the rule that follows is that a frame rule states the least length its check measures.
END SLIP16

── SLICE P273-FROM ── target `docs/roadmap/features/T2_F273.md` ── REWRITE FROM ──
BEGIN P273-FROM sha256=3172892b1b5f766caf211db43b91249e5b31fbf264e4d223d4b0ba833043d057
  the heir sentence of the F261 Design.

## Do not touch
END P273-FROM

── SLICE P273-TO ── target `docs/roadmap/features/T2_F273.md` ── REWRITE TO ──
BEGIN P273-TO sha256=e455e323e2d96a11b661116bc6c48632b936e01c4d1c16cafc6d1166d6e030fd
  the heir sentence of the F261 Design.
- R-0905 carries a resolution line naming the commit that deleted the three readers of `git_status_read`
  with their tests, or the commit that gave the event a surviving emitter, and in either case took the
  name out of `KNOWN_DEAD_EVENT_COUPLINGS`.

## Do not touch
END P273-TO

── SLICE MUT-1-FROM ── G5 (1) only ── never a file ──
BEGIN MUT-1-FROM sha256=b80c9cb6a8186d1e0e037407c5cb67f8a716ea462f41563da837cf74561af360
    "dev.status": lambda args: _dev_status(json_output=getattr(args, "json", False)),
}
END MUT-1-FROM

── SLICE MUT-1-TO ── G5 (1) only ── never a file ──
BEGIN MUT-1-TO sha256=e6c5cf379ec42ade01d744d5ecde8be7eb1c25fec1a597e872392ee9b0210d41
    "dev.status": lambda args: _dev_status(json_output=getattr(args, "json", False)),
    "guide.job": lambda args: None,
}
END MUT-1-TO

── SLICE MUT-2-FROM ── G5 (2) only ── never a file ──
BEGIN MUT-2-FROM sha256=7048056fc379469f4167ab957a64cd68fb2c735884bc490198ed15a47d36a731
    "file": GroupDef("file", "File", "File-level provenance and tracing.", user_facing=False),
END MUT-2-FROM

── SLICE MUT-2-TO ── G5 (2) only ── never a file ──
BEGIN MUT-2-TO sha256=1e0fc6e1eefe53b26729d74dc3513bac1a9a523281f1fd9c3b42ad6901924b08
    "file": GroupDef("file", "File", "File-level provenance and tracing.", user_facing=False),
    "repo": GroupDef("repo", "Repo", "Read-only repository status.", user_facing=False),
END MUT-2-TO

── SLICE MUT-3-FROM ── G5 (3) only ── never a file ──
BEGIN MUT-3-FROM sha256=cf0f753a2e537729da93543036d6fac27a67b0356ea982e7410ed837f85962fe
    "ci": GroupDef("ci", "CI", "Remedy's own CI stages, run locally.", user_facing=False),
    "integrity": GroupDef("integrity", "Integrity", "Pre-handoff integrity checks.", user_facing=False),
END MUT-3-FROM

── SLICE MUT-3-TO ── G5 (3) only ── never a file ──
BEGIN MUT-3-TO sha256=0e6e304c7d004617f569abb4fbe043da92f09d7bc9edf16d330297722022bedd
    "integrity": GroupDef("integrity", "Integrity", "Pre-handoff integrity checks.", user_facing=False),
END MUT-3-TO

── SLICE MUT-4-FROM ── G5 (4) only ── never a file ──
BEGIN MUT-4-FROM sha256=2cd882e3544109f710e0a8b3c592d8630ddfb5d26298b828241e8202c83cbe93
        related=("brain.view",),
END MUT-4-FROM

── SLICE MUT-4-TO ── G5 (4) only ── never a file ──
BEGIN MUT-4-TO sha256=456e17a8d5a0758c78f31eb32c6e05bd5097a696240912bb4cdae41153ac6292
        related=("brain.view", "dashboard.job"),
END MUT-4-TO

── SLICE MUT-5-FROM ── G5 (5) only ── never a file ──
BEGIN MUT-5-FROM sha256=c882fd9e28e8c74749513a0219ddfc7f8b3dce2dc596553c3aa294e166123c9a
        print("  remedy worker unload --all                  — free VRAM")
END MUT-5-FROM

── SLICE MUT-5-TO ── G5 (5) only ── never a file ──
BEGIN MUT-5-TO sha256=fa2d753e6f176b5cb5788b726a53071644b69a9bf47279a523b6602d517f1a94
        print("  remedy worker unload --all                  — free VRAM")
        print("  remedy repo commit-readiness <job_id>       — commit preview")
END MUT-5-TO

── SLICE MUT-6-FROM ── G5 (6) only ── never a file ──
BEGIN MUT-6-FROM sha256=75bd7dec918f7a4230d121da03f2794f6c613befe83fcd3597af72640218ebfb
    "context_budget_optimized",
    "git_status_read",
)
END MUT-6-FROM

── SLICE MUT-6-TO ── G5 (6) only ── never a file ──
BEGIN MUT-6-TO sha256=672975d78ec8b597217a8cec83882096403f3c707fb4f81e7ac4c04db9559d8a
    "context_budget_optimized",
)
END MUT-6-TO
