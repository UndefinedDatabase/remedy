── STEP T003/2 — F261 — ROUND 14 ──
Goal: Book round 13's PASS, register R-0903 for F273, record DECISION F261 D13, and delete the
`orchestrator` group, the `rollback` group and the `loop` command group in three commits by
applying three tables; run the suite once.

Base commit: `c3047df0`, on `feature/f261-cli-vocabulary-v2`. SESSION 3 of F261. Read AGENTS.md,
docs/agents/self_drive_protocol.md, `.agent/f261_t003_inventory.md`, and DECISION F261 D13 once
C1 has landed it.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block is a run
of a single repeated character, and every box-drawing rule inside the STEP and SLICE header
lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)` and `$?` in a compound command are refused by form, so write such checks
as Python scripts under `.remedy-wt/f261r14w/`, and never name a script after a standard-library
module; a pipe into `tail` hides pytest's exit code. The editable install resolves `apps` and
`packages` to the PRIMARY checkout, so a pytest run inside a worktree goes through a runner
script that changes into the worktree, puts it first on `sys.path` and in `PYTHONPATH`, and
asserts `apps.cli.grouped` loaded from inside it. Never call `run_job` or a runner yourself: a
job run started from inside a checkout creates a `remedy/job-*` branch in it.
`git branch --list 'remedy/job-*'` reads 16 lines now; keep it so. While a deletion is staged
but not committed, `test_every_enumerated_path_exists_in_this_repo` fails; run no suite then.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f261-r14.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN14; slice RECORD14 is appended to
    `.agent/live_review.md` and slice DEC13 to `.agent/decisions.md`; in
    `docs/roadmap/features/T2_F273.md` the bytes of slice P273-FROM are replaced by those of
    slice P273-TO
C2  THE ORCHESTRATOR GROUP: copy `.remedy-wt/f261-block/f261-r14-orchestrator.jsonl` to
    `.agent/authored/f261-r14-orchestrator.jsonl` and apply it per THE TABLES, in one commit
C3  THE ROLLBACK GROUP: the same with `f261-r14-rollback.jsonl`, in one commit
C4  THE LOOP COMMAND GROUP: the same with `f261-r14-loop.jsonl`, in one commit
C5  `.agent/handoff.md`, the handback; then `git push origin feature/f261-cli-vocabulary-v2`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f261-r14.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md`, `.agent/decisions.md` and `docs/roadmap/features/T2_F273.md`. C2 to C4:
each table's own carrier and the paths G3 names. C5: `.agent/handoff.md`.

## The appends and the pair

RECORD14 and DEC13 each begin with an empty line, and both targets end in a newline at
`c3047df0`: an append is the file's bytes followed by the slice's bytes, and nothing else. The
pair P273: TO contains FROM: false, so it is a REWRITE; P273-FROM occurs once in
`docs/roadmap/features/T2_F273.md` at `c3047df0`, and at C1 P273-FROM occurs 0 times and P273-TO
once.

## THE TABLES

Each carrier holds one JSON array per line. Their sha256 digests, to verify before copying:
`f261-r14-orchestrator.jsonl` `ca79da0130865fe41d52f8c81d2c25e88e77815f54eda041f3375a45beaaecd2`,
`f261-r14-rollback.jsonl` `ca2125be096e9e6f0317282bac75a31ec160a958c00f584686294af3d44e4f0e`,
`f261-r14-loop.jsonl` `fc3a9b2fe8bb1ca5a294211da8b55ab4097c02a41ea892efc009430e87a4ccc8`.
Apply the rows strictly
in file order, each against the tree as the previous rows left it, from the repository root:
`["edit", path, old, new, count]` opens the path with `encoding="utf-8", newline=""`, requires
the number of occurrences of `old` to equal `count` exactly, and replaces every occurrence with
`new`; `["delete", path]` removes the file; `["move", src, dst]` renames the file, whose target
must not exist; `["create", path, content]` writes `content` to a path that must not exist, with
the same encoding and newline setting. A count that differs or a target that exists is a STOP:
touch nothing further, commit nothing of that table, and hand back with the row and the reading.
Stage each commit with `git add -A` after its table and its carrier. The tables are the
reviewer's measured dry run of DECISION F261 D13: the orchestrator table its CHOSEN FIRST, the
rollback table its CHOSEN SECOND and the loop table its CHOSEN THIRD.

## SPEC S — the suite, once, after G5 and before C5

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f261r14w/`. Report pytest's return code, the run's last output line, and every
distinct bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `.
Re-run each bad node alone, once, the same way, and report that return code beside it.

## Constraints

1. NO SLICE AND NO TABLE IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C5, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f261r14w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f261-block/` and your
   own directory. `git worktree list` reads one row now; leave it so. Create no symlink.
5. Every commit stays under 500 insertions, read as the first column of `git show --numstat
   --format= <commit>` with git's default rename detection.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph and no `Landed:` line.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 290 lines TOTAL and 215 lines of PROSE,
   against the caps of 490 and 400.
8. GATE ORDER. G1 and G2 after C1; G3, G4 and G5 after C4; then SPEC S, whose result is G6; G7
   after C5 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r14.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; each committed carrier's sha256 equals its digest above.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN14, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its `c3047df0` blob
followed by RECORD14, and `.agent/decisions.md` its `c3047df0` blob followed by DEC13.
`docs/roadmap/features/T2_F273.md` equals its `c3047df0` blob with the pair P273 applied, with
the counts The appends and the pair give. Over `.agent/live_review.md`: `^Gate: F\d+ R\d+ — `
reads 122 at `c3047df0` and 123 at C1, with `Gate: F261 R13 — ` once at C1; distinct
`^- R-\d+ — ` ids 105 and 106, C1 minus base exactly `R-0903`; distinct `^Done: R-\d+ — ` ids 8
and 8; the open set by distinct id 97 and 98. `python3 -m pytest tests/docs/ -q` exits 0 at C1.

G3 THE TABLES, at C2, C3 and C4. `git diff --no-renames --name-only` from each commit's parent
prints exactly that commit's carrier and: at C2 `apps/cli/command_catalog.py`, `apps/cli/commands/__init__.py`, `apps/cli/commands/orchestrator_cmd.py`, `docs/system/orchestrator-brain-v0.md`, `packages/orchestration/decision_evidence.py`, `packages/orchestration/model_routing.py`, `packages/orchestration/orchestrator_brain.py`, `tests/cli/test_orchestrator_brain_cli.py`, `tests/orchestration/import_reachability_allowlist.txt`, `tests/orchestration/test_orchestrator_brain.py` and `tests/test_command_catalog.py`; at C3 `apps/cli/command_catalog.py`, `apps/cli/commands/real_test_execution_cmd.py`, `docs/guides/real-test-execution-snapshot-rollback-user-guide-v1.md`, `docs/system/real-test-execution-snapshot-rollback-proof-v1.md`, `packages/orchestration/real_test_execution.py`, `tests/cli/test_real_test_execution_cli.py`, `tests/orchestration/test_real_test_execution.py` and `tests/test_command_catalog.py`; at C4
`apps/cli/command_catalog.py`, `apps/cli/commands/__init__.py`, `apps/cli/commands/loop_cmd.py`, `apps/cli/cost_preview_confirm.py`, `docs/system/vocabulary.md`, `packages/orchestration/loop_spec.py`, `tests/cli/test_cost_preview_confirm.py`, `tests/cli/test_loop_cmd.py`, `tests/orchestration/import_reachability_allowlist.txt` and `tests/test_command_catalog.py`. `git rev-parse <commit>:<object>` equals the dry run, for `apps`, `tests`, `docs`,
`scripts`, `packages` and `README.md` in that order: C2 `e508e584b116eb1c055a381d7de738ba6ba6e11f`, `d35ae9056e1a03bb93f733ab7036d79b8d7b7ff6`, `d86c24c61bf0d6bb7f0a1b6666f9a8cd5949bb92`, `e3c01bde145e2c323bf157e1bb4a97cdaaa747cc`, `791284ffa3c944cbada295852d18be5a638c0e2e`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`; C3 `4a71ad70ec3f148c37dc0520e88b5cafce14c078`, `a3ea1381531d0af0a89423c8b0b00da50c05c838`, `cd7dbc5c0dfc00700ec6bf5b8e874b44897d9365`, `e3c01bde145e2c323bf157e1bb4a97cdaaa747cc`, `355d0c1138499eb7bf10739a9284a03d7e19d08b`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`; C4 `7952f315479e3656e0a3b8bb5d09cf5b055f8408`, `a1c7c1bcfeb7f5310ae222494c9e739da8a20c95`, `cf0d7c41ed07a8d4ce292b22a49f148fb540f9a1`, `e3c01bde145e2c323bf157e1bb4a97cdaaa747cc`, `7ad5c86b22c81faadc62bc18a5176009a5dc9005`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`.
Report each commit's insertions per constraint 5.

G4 THE SWEEP, at C4. `git grep -n -I -E 'remedy (orchestrator|rollback|loop)\b|orchestrator_cmd|loop_cmd|create_rollback_proof|get_rollback_proof|export_rollback_proof_json'
<C4> -- apps packages scripts tests docs README.md ':!docs/roadmap'` exits 1 and prints nothing.
`python3 -m ruff check` over every `.py` path of C2 to C4 that still exists at C4 exits 0.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f261r14w/wt <C4's sha>`, each run
through the runner over `tests/test_command_catalog.py`, `tests/cli/test_cli_ux.py`,
`tests/test_grouped_cli.py` and `tests/orchestration/test_import_reachability.py` with
`-rf --tb=no`. Mutation <n> is in the file its line below names, replaces the bytes of slice
MUT-<n>-FROM, whose count there must read 1, with those of slice MUT-<n>-TO, and is restored with
`git -C .remedy-wt/f261r14w/wt checkout -- <that file>`. (a) CONTROL: must exit 0. Each of (1)
to (4) must exit 1 with the named node among the failed nodes:
(1) `apps/cli/commands/self_cmd.py`, an `orchestrator` handler row, (2)
`apps/cli/commands/real_test_execution_cmd.py`, a `rollback` handler row, and (3) the same file,
a `loop` handler row: each `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table`;
(4) `apps/cli/command_catalog.py`, the `loop` group restored without commands:
`TestCatalogIntegrity::test_every_group_has_at_least_one_command`.
Report each exit code, summary line and number of failed nodes; then
`git worktree remove --force .remedy-wt/f261r14w/wt` and read `git branch --list 'remedy/job-*'`.

G6 THE SUITE, SPEC S at C4: must exit 0 with no bad node; report the last output line. A bad
node whose lone re-run exits 0 is reported as such with both readings, and is not a STOP; a bad
node whose lone re-run fails is.

G7 THE TREE, after C5 and the push. `git status --porcelain` prints `''`; C0a to C5 are
single-parent commits in that order on `c3047df0`; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f261-cli-vocabulary-v2`; `git worktree list` prints one row, and
`git branch --list 'remedy/job-*'` prints 16 lines.

## The handback, C5

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 3 of feature F261 · round 14 · rounds so far 14`, with one sentence of context
self-assessment. `## Commits` lists C0a to C4, each row's `+/-` cell equal to constraint 5's
reading of that commit and its deletions column; C5's own numbers appear nowhere, per item 31 of
§3. `## Verification` gives G1 to G6 with real exit codes. It states the open findings at 98 by
distinct id, with the High ids R-0803, R-0804 and R-0807, and `Operator questions open: 0`. Its
`## Next` names, in order: Phase 1 rule 1; the reviewer's verdict on round 14; the loop modules,
the `queue` group and `job_queue.py`, as the inventory proposes.

── SLICE PLAN14 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN14 sha256=d52f058fb8d85251212615af7441e0b1beeae43a1d2b6224fea148e448b9335a
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 14 continues T003. It books round 13's PASS, registers R-0903 for F273 and records
DECISION F261 D13, then deletes the `orchestrator` group, the `rollback` group and the `loop`
command group with the package code only they called, one table per commit.

## Next Steps

1. The loop modules with the run report's loop reference, the `queue` command group, and
   `job_queue.py` with its binding, configuration keys and queue directory, with their
   deletion paragraph, as `.agent/f261_t003_inventory.md` proposes.
2. The rest of T003 in the inventory's order, each round re-measured before it is authored,
   with R-0767, R-0894 and R-0900.
3. T004.

## Risks

- 97 findings are open by distinct id before this round's record and 98 after it; three are
  High, R-0803, R-0804 and R-0807.
- The inventory proposes more rounds than F261's soft limit of 25 leaves; the session that
  reaches the limit owes the scope report and the split-and-close default.
- A deletion's consumers include shell strings, subprocess help calls and the UI event
  catalog, so every deletion round runs the whole suite on its committed tree.
END PLAN14

── SLICE RECORD14 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD14 sha256=55596e0b877c5bba22e15721f8da289880c3ef422f4282fe31d1afec6bf90b37

Gate: F261 R13 — the F261 round 13 entry. VERDICT PASS. Written by the planner and reviewer of session 38 after reading the committed range `80e9cc0f`..`c3047df0` and re-deriving the readings below; the worker's report was evidence for none of them. It is booked here by the first commit of round 14 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r13.md` at `5b461ba9` and `.agent/last_block.md` at `f567eda3` are byte-identical to the reviewer's scratch original, sha256 `0aebf9128ef0c7de15a917dd345716030399c1101de00cec2ef308b8b1f7b815`, and the two tables committed at `f70e1611` and `ed02d512` are byte-identical to the reviewer's. THE STATE: at `d2891eb9` and again at `c3047df0`, `.agent/plan.md` equals PLAN13, `.agent/f261_t003_inventory.md` equals INV13, and `.agent/live_review.md` and `.agent/decisions.md` equal their `80e9cc0f` blobs followed by RECORD13 and DEC12. THE TABLE COMMITS: at `f70e1611` and `ed02d512` the `apps`, `tests`, `docs`, `scripts`, `packages`, `README.md` and `.claude` objects equal the reviewer's dry-run commits of the tables, which had reproduced the research helper's trees exactly; each commit's `--no-renames` path set is the dry run's plus its carrier, and `git show --numstat` reads 76 and 136 insertions. In the dry run's production diff `GroupDef` gains `hidden` with a default of false, `_print_root_help` lists no hidden group in either form while the parser still adds every group, and `apps/cli/commands/plan_cmd.py` moves to `apps/cli/commands/roadmap_cmd.py` with its ids and handlers renamed. At `c3047df0` the grep of `remedy plan status`, `remedy plan next` and the two quoted old ids over `apps`, `packages`, `scripts`, `tests`, `docs` without `docs/roadmap`, `README.md`, `AGENTS.md` and `.claude` prints five lines: `docs/system/vocabulary.md` line 228, two commit-subject fixtures of `tests/orchestration/test_failure_postmortem.py` and the two `RENAMED` pairs of `tests/test_command_catalog.py`. In the reviewer's dry run a full suite under `-n auto` without `tests/ui_server` read 1 failed, `test_vitest_passes`, and 17682 passed. Over `tests/cli/test_plan_cli.py`, `tests/cli/test_cli_ux.py`, `tests/test_grouped_cli.py` and `tests/test_command_catalog.py`, which passed 506 unmutated, listing hidden groups under `--all-commands` failed 2 tests, listing them in the default help failed 1, making `roadmap` not hidden failed 2, restoring a `plan.next` handler row failed 1, and making the parser skip hidden groups failed 19. The record slices and the inventory applied on top of the dry run passed `tests/docs/`, `tests/test_agent_tooling.py`, `tests/ui_server/test_dashboard_contract.py` and the other files the reviewer ran among those that read the edited state files, apart from `test_vitest_passes`, at 864 passed. THE REVIEWER'S RUN in the primary checkout at `c3047df0` of those four files, `tests/orchestration/test_roadmap_index.py`, `tests/orchestration/test_import_reachability.py`, `tests/test_agent_tooling.py`, `tests/cli/test_golden_path.py`, `tests/cli/test_advertised_commands.py`, `tests/docs/`, `tests/test_cli_main.py` and `tests/ui_server/test_dashboard_contract.py` read 1031 passed and 1 skipped, and `git branch --list 'remedy/job-*'` read 16 lines. The open set reads 97 by distinct id at `c3047df0`.

- R-0903 — Low, ONCE THE `orchestrator` AND `rollback` GROUPS ARE DELETED, THREE READERS READ RECORDS NO COMMAND WRITES AND ONE VALIDATOR HAS ONLY TEST CALLERS. Raised by the planner and reviewer of session 38 while preparing F261 round 14, after searching the open set for `list_decisions`, `list_rollback_proofs`, `audit_rollback_safety` and `validate_next_safe_action_command` under §3 item 30: no open finding describes them. THE DEFECT, read on the reviewer's dry-run trees of round 14 on `c3047df0`: `_build_orchestrator_section` in `packages/orchestration/ui_server.py` reads decision traces through `list_decisions`, and the code that wrote them is deleted with the orchestrator engine; the cockpit's `rollback_proof_count` and `test integrity` read rollback proofs through `list_rollback_proofs` and `audit_rollback_safety`, and their writer `create_rollback_proof` is deleted with the `rollback` group; and `validate_next_safe_action_command` in `packages/orchestration/do_run.py` loses its last production caller with the orchestrator engine and keeps callers under `tests/` only. `tests/ui_server/test_dashboard_cockpit_truth.py` pins the cockpit's orchestrator section, so the round keeps the readers. WHY LOW: each reader returns an honest empty result and no command a user runs prints anything false. WHY F273's: removing a cockpit section and a function kept alive by its tests is findings paydown, outside the prune. FIX: delete each reader with the cockpit key and the tests that pin it, or give it a producer, and delete the validator with its tests unless a surviving command calls it. Owner: F273.
END RECORD14

── SLICE DEC13 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC13 sha256=eb8200aa8d20b06de2023ed492926b27bb78699ff78da9524b5e877df787e3c9

## DECISION F261 D13 (2026-09-15, F261 round 14) — the deletion paragraph of the `orchestrator` and `rollback` groups and of the `loop` command group

CONTEXT. DECISION amend0905-vocab D4 deletes every group it does not name, and `.agent/f261_t003_inventory.md` puts these three first. Measured at `c3047df0` by the reviewer's research helper and re-read by the reviewer on the dry-run trees. A command's package code goes with it when the command was its only production caller; a reader that a surviving surface still calls stays.

CHOSEN, FIRST: `orchestrator`. Deleted: the group, its commands `orchestrator.inspect`, `orchestrator.decide`, `orchestrator.report` and `orchestrator.idea`, `apps/cli/commands/orchestrator_cmd.py` and its CLI tests, and from `packages/orchestration/orchestrator_brain.py` the situation builder, the option scorer, the anti-loop guard, the model routing plan, the decision selector, the idea intake and their tests. `list_decisions` stays, because `_build_orchestrator_section` in `packages/orchestration/ui_server.py` reads it and `tests/ui_server/test_dashboard_cockpit_truth.py` pins that section. THE HEIRS: reading a situation and choosing one next step belongs to the F070 orchestrator loop behind `remedy mission run`, which the page's own banner names; a new goal enters as an order, the text or file `remedy do` takes; the model routing plan belongs to F110's routing and the `orchestrator.model` configuration key. The deterministic scorer, the report of rejected options and the idea classifier have no heir. `docs/system/orchestrator-brain-v0.md` keeps its text under a dated status line.

CHOSEN, SECOND: `rollback`. Deleted: the group, its commands `rollback.proof` and `rollback.show`, their handlers in `apps/cli/commands/real_test_execution_cmd.py`, and `RollbackProof`, `create_rollback_proof`, `get_rollback_proof`, `export_rollback_proof_json` and `_rollback_path` in `packages/orchestration/real_test_execution.py`. `list_rollback_proofs` and `audit_rollback_safety` stay for the cockpit and `test integrity`, and `snapshot create` relates to `snapshot show`. THE HEIR: checking whether a change can be restored lives in the snapshot commands, `patch revert` and the snapshot truth of `packages/orchestration/repository_snapshot.py`; no roadmap feature inherits the proof record.

CHOSEN, THIRD: `loop`. Deleted: the group, its commands `loop.list`, `loop.validate` and `loop.run`, `apps/cli/commands/loop_cmd.py` and `tests/cli/test_loop_cmd.py`. `packages/orchestration/loop_spec.py` and `loop_run.py` stay for the next deletion round, which takes them with the run report's loop reference. THE HEIR, as `docs/roadmap/features/T2_F261.md` names it: a recurring order is an order file started with `remedy do <file>`; a scheduler has no heir.

CONSEQUENCE. `remedy orchestrator`, `remedy rollback` and `remedy loop` are unknown commands, and their ids join `TestDeletedCommands`. The orchestrator section of the cockpit and the rollback readers now read records nothing writes, and `validate_next_safe_action_command` keeps only test callers; R-0903 records that for F273. HOW TO REVERSE: revert the round's three table commits and delete this section.
END DEC13

── SLICE P273-FROM ── target `docs/roadmap/features/T2_F273.md` ── REWRITE FROM ──
BEGIN P273-FROM sha256=3a73a9509c3bb98888bcc7678bb84fa1f19aedd90e37dd92edee2457cbe1e0ba
  `scripts/remedy_smoke.sh` against the `job show` output of a created job.

## Do not touch
END P273-FROM

── SLICE P273-TO ── target `docs/roadmap/features/T2_F273.md` ── REWRITE TO ──
BEGIN P273-TO sha256=1859a4a2f208a11840493f51ed8f15b2e2eabbc6ce73268672f4c86a33617c0e
  `scripts/remedy_smoke.sh` against the `job show` output of a created job.
- R-0903 carries a resolution line naming, for each of `list_decisions`, `list_rollback_proofs` with
  `audit_rollback_safety`, and `validate_next_safe_action_command`, the commit that deleted it with the
  tests that pinned it or the producer that now writes what it reads.

## Do not touch
END P273-TO

── SLICE MUT-1-FROM ── G5 (1) only ── never a file ──
BEGIN MUT-1-FROM sha256=d7a772cd23160d7043c5055cf28d32759b9573061e3ed12fb3cb5c5e5cbe96a2
    "self.integrity": _cmd_self_integrity,
}
END MUT-1-FROM

── SLICE MUT-1-TO ── G5 (1) only ── never a file ──
BEGIN MUT-1-TO sha256=44d8b35c7a7ba297e740ce5aa41668b74138e243a898d0f5a2aa6849efb2e7a6
    "self.integrity": _cmd_self_integrity,
    "orchestrator.inspect": _cmd_self_inspect,
}
END MUT-1-TO

── SLICE MUT-2-FROM ── G5 (2) only ── never a file ──
BEGIN MUT-2-FROM sha256=cbe639f14da747be791cee1db35f89b390735f19941274249a79769c5bf2af5c
    "snapshot.show": _cmd_snapshot_show,
}
END MUT-2-FROM

── SLICE MUT-2-TO ── G5 (2) only ── never a file ──
BEGIN MUT-2-TO sha256=b95144f3378a462bcc0ca7de5a04555ecbb44ca6d8b569da1e2081e7be0ba369
    "snapshot.show": _cmd_snapshot_show,
    "rollback.show": _cmd_snapshot_show,
}
END MUT-2-TO

── SLICE MUT-3-FROM ── G5 (3) only ── never a file ──
BEGIN MUT-3-FROM sha256=32b3682d9569fadb6a724578d6535cfcbd1ed1c6d74a103d013f6d150bafbe36
    "test.list": _cmd_test_list,
END MUT-3-FROM

── SLICE MUT-3-TO ── G5 (3) only ── never a file ──
BEGIN MUT-3-TO sha256=a1c6696bbd9e7c7b32827cef409711be4e0e10fd0be2d65ef9bc9473dbec0f7c
    "test.list": _cmd_test_list,
    "loop.list": _cmd_test_list,
END MUT-3-TO

── SLICE MUT-4-FROM ── G5 (4) only ── never a file ──
BEGIN MUT-4-FROM sha256=06596a3207dcb091d69878bd45f91ef4d4c72b1c6b2ad83dc13684680c0ff36b
    "stats": GroupDef("stats", "Stats", "Honest counts from the evidence on disk."),
END MUT-4-FROM

── SLICE MUT-4-TO ── G5 (4) only ── never a file ──
BEGIN MUT-4-TO sha256=02bb672aed9e112280313b6840da0eb009de0700286dd31df694159a3e5c3756
    "stats": GroupDef("stats", "Stats", "Honest counts from the evidence on disk."),
    "loop": GroupDef("loop", "Loop", "Recurring orders."),
END MUT-4-TO
