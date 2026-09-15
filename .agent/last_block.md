── STEP T003/1 — F261 — ROUND 13 ──
Goal: Book round 12's PASS, record DECISION F261 D12 and the T003 inventory, give `GroupDef` a
`hidden` field and rename the `plan` group to the hidden `roadmap` group, in two commits by
applying two tables; run the suite once.

Base commit: `80e9cc0f`, on `feature/f261-cli-vocabulary-v2`. SESSION 3 of F261. Read AGENTS.md,
docs/agents/self_drive_protocol.md, and DECISION F261 D12 once C1 has landed it.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block is a run
of a single repeated character, and every box-drawing rule inside the STEP and SLICE header
lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)` and `$?` in a compound command are refused by form, so write such checks
as Python scripts under `.remedy-wt/f261r13w/`, and never name a script after a standard-library
module; a pipe into `tail` hides pytest's exit code. The editable install resolves `apps` and
`packages` to the PRIMARY checkout, so a pytest run inside a worktree goes through a runner
script that changes into the worktree, puts it first on `sys.path` and in `PYTHONPATH`, and
asserts `apps.cli.grouped` loaded from inside it. Never call `run_job` or a runner yourself: a
job run started from inside a checkout creates a `remedy/job-*` branch in it.
`git branch --list 'remedy/job-*'` reads 16 lines now; keep it so.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f261-r13.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN13; slice RECORD13 is appended to
    `.agent/live_review.md` and slice DEC12 to `.agent/decisions.md`; the new file
    `.agent/f261_t003_inventory.md` is written with the bytes of slice INV13
C2  THE HIDDEN FIELD: copy `.remedy-wt/f261-block/f261-r13-hidden.jsonl` to
    `.agent/authored/f261-r13-hidden.jsonl` and apply it per THE TABLES, in one commit
C3  THE ROADMAP GROUP: the same with `f261-r13-roadmap.jsonl`, in one commit
C4  `.agent/handoff.md`, the handback; then `git push origin feature/f261-cli-vocabulary-v2`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f261-r13.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md`, `.agent/decisions.md` and `.agent/f261_t003_inventory.md`. C2 and C3:
each table's own carrier and the paths G3 names. C4: `.agent/handoff.md`.

## The appends

RECORD13 and DEC12 each begin with an empty line, and both targets end in a newline at
`80e9cc0f`: an append is the file's bytes followed by the slice's bytes, and nothing else.
`.agent/f261_t003_inventory.md` does not exist at `80e9cc0f`.

## THE TABLES

Each carrier holds one JSON array per line. Their sha256 digests, to verify before copying:
`f261-r13-hidden.jsonl` `a3099103745c4c21d24fc953c543b342baddb2302cf28a460bcd827cba918ad3`,
`f261-r13-roadmap.jsonl` `fd0bd680c5ca91e5f29b071c45e2798dd0834ba45745d475b84684c47700ac59`.
Apply the rows strictly
in file order, each against the tree as the previous rows left it, from the repository root:
`["edit", path, old, new, count]` opens the path with `encoding="utf-8", newline=""`, requires
the number of occurrences of `old` to equal `count` exactly, and replaces every occurrence with
`new`; `["delete", path]` removes the file; `["move", src, dst]` renames the file, whose target
must not exist; `["create", path, content]` writes `content` to a path that must not exist, with
the same encoding and newline setting. A count that differs or a target that exists is a STOP:
touch nothing further, commit nothing of that table, and hand back with the row and the reading.
Stage each commit with `git add -A` after its table and its carrier. The tables are the
reviewer's measured dry run of DECISION F261 D12: the hidden table its CHOSEN FIRST and the
roadmap table its CHOSEN SECOND.

## SPEC S — the suite, once, after G5 and before C4

From the primary checkout's root, serially:
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, with `PYTHONPATH`,
`REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed and `PYTHONDONTWRITEBYTECODE=1`, output under
`.remedy-wt/f261r13w/`. Report pytest's return code, the run's last output line, and every
distinct bad node, the text after a line-initial `FAILED ` or `ERROR ` up to the first ` - `.
Re-run each bad node alone, once, the same way, and report that return code beside it.

## Constraints

1. NO SLICE AND NO TABLE IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a, before C2 and before C4, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished, hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f261r13w/`, uncommitted; no
   `.py` file under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f261-block/` and your
   own directory. `git worktree list` reads one row now; leave it so. Create no symlink.
5. Every commit stays under 500 insertions, read as the first column of `git show --numstat
   --format= <commit>` with git's default rename detection.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph and no `Landed:` line.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 379 lines TOTAL and 217 lines of PROSE,
   against the caps of 490 and 400.
8. GATE ORDER. G1 and G2 after C1; G3, G4 and G5 after C3; then SPEC S, whose result is G6; G7
   after C4 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r13.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; each committed carrier's sha256 equals its digest above.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN13, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/f261_t003_inventory.md` is byte-identical to
INV13. `.agent/live_review.md` equals its `80e9cc0f` blob followed by RECORD13, and
`.agent/decisions.md` its `80e9cc0f` blob followed by DEC12. Over `.agent/live_review.md`:
`^Gate: F\d+ R\d+ — ` reads 121 at `80e9cc0f` and 122 at C1, with `Gate: F261 R12 — ` once at
C1; distinct `^- R-\d+ — ` ids 105 and 105; distinct `^Done: R-\d+ — ` ids 8 and 8; the open set
by distinct id 97 and 97.

G3 THE TABLES, at C2 and C3. `git diff --no-renames --name-only` from each commit's parent
prints exactly that commit's carrier and: at C2 `apps/cli/command_catalog.py`, `apps/cli/grouped.py`, `tests/cli/test_cli_ux.py` and `tests/test_grouped_cli.py`; at C3 `.claude/skills/remedy-self-drive/SKILL.md`, `apps/cli/command_catalog.py`, `apps/cli/commands/__init__.py`, `apps/cli/commands/plan_cmd.py`, `apps/cli/commands/roadmap_cmd.py`, `docs/README.md`, `docs/agents/self_drive_protocol.md`, `docs/system/roadmap-mirror-v1.md`, `packages/orchestration/feature_mission_adapter.py`, `tests/cli/test_plan_cli.py`, `tests/orchestration/import_reachability_allowlist.txt`, `tests/orchestration/test_roadmap_index.py` and `tests/test_command_catalog.py`.
`git rev-parse <commit>:<object>` equals the dry run, for `apps`, `tests`, `docs`, `scripts`,
`packages`, `README.md` and `.claude` in that order: C2 `87c3490a646d984dcc327a6ef7fd027d1a90f7d5`, `430b31b67ee36f78a8e0651bdc47aaf4149b028e`, `43175c761c057c2c37403fe449653981c52a8b43`, `e3c01bde145e2c323bf157e1bb4a97cdaaa747cc`, `0e39ea4b746aee228ea56e5a3ed92565f135fe00`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`, `3f74bb69e1e2e5f765a6de44bc9a9c30575228d8`; C3 `c52ed4353a91a27168fe9ac9d689a101c5957b7f`, `166acfa62b5734c6145067c195ea7a7e85153b6a`, `11be22ad7d9041f1b266294440e8d20051e94819`, `e3c01bde145e2c323bf157e1bb4a97cdaaa747cc`, `2fc99e37a3f697f772cb10014e7ea5d40e5aaa32`, `15b9e0e8fec9721c7c17a872cc8f1a2bed3a2952`, `e3cd5e0ac262f3f993506e95825e270e39c03ec0`. Report each
commit's insertions per constraint 5.

G4 THE SWEEP, at C3. `git grep -n -I -E 'remedy plan (status|next)\b|"plan\.(status|next)"'
<C3> -- apps packages scripts tests docs README.md AGENTS.md .claude ':!docs/roadmap'` prints
exactly five lines: `docs/system/vocabulary.md` line 228, `tests/orchestration/test_failure_postmortem.py`
lines 1055 and 1066, and `tests/test_command_catalog.py` lines 276 and 277. `python3 -m ruff
check` over every `.py` path of C2 and C3 exits 0.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f261r13w/wt <C3's sha>`, each run
through the runner over `tests/cli/test_plan_cli.py`, `tests/cli/test_cli_ux.py`,
`tests/test_grouped_cli.py` and `tests/test_command_catalog.py` with `-rf --tb=no`. Mutation <n>
is in the file its line below names, replaces the bytes of slice MUT-<n>-FROM, whose count there
must read 1, with those of slice MUT-<n>-TO, and is restored with
`git -C .remedy-wt/f261r13w/wt checkout -- <that file>`. (a) CONTROL: must exit 0. Each of (1)
to (5) must exit 1 with the named node among the failed nodes:
(1) `apps/cli/grouped.py`, `--all-commands` listing hidden groups:
`TestHiddenGroup::test_a_hidden_group_is_absent_from_all_commands`;
(2) `apps/cli/grouped.py`, the default help listing hidden groups:
`TestHiddenGroup::test_a_hidden_group_is_absent_from_the_default_help`;
(3) `apps/cli/command_catalog.py`, `roadmap` not hidden: `TestCatalogRegistration::test_the_group_is_hidden`;
(4) `apps/cli/commands/roadmap_cmd.py`, a `plan.next` handler row:
`TestRenamedCommands::test_no_old_id_is_left_in_the_dispatch_table`;
(5) `apps/cli/grouped.py`, the parser skipping hidden groups:
`TestHiddenGroup::test_a_hidden_groups_command_still_dispatches`.
Report each exit code, summary line and number of failed nodes; then
`git worktree remove --force .remedy-wt/f261r13w/wt` and read `git branch --list 'remedy/job-*'`.

G6 THE SUITE, SPEC S at C3: must exit 0 with no bad node; report the last output line. A bad
node whose lone re-run exits 0 is reported as such with both readings, and is not a STOP; a bad
node whose lone re-run fails is.

G7 THE TREE, after C4 and the push. `git status --porcelain` prints `''`; C0a to C4 are
single-parent commits in that order on `80e9cc0f`; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f261-cli-vocabulary-v2`; `git worktree list` prints one row, and
`git branch --list 'remedy/job-*'` prints 16 lines.

## The handback, C4

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 3 of feature F261 · round 13 · rounds so far 13`, with one sentence of context
self-assessment. `## Commits` lists C0a to C3, each row's `+/-` cell equal to constraint 5's
reading of that commit and its deletions column; C4's own numbers appear nowhere, per item 31 of
§3. `## Verification` gives G1 to G6 with real exit codes. It states the open findings at 97 by
distinct id, with the High ids R-0803, R-0804 and R-0807, and `Operator questions open: 0`. Its
`## Next` names, in order: Phase 1 rule 1; the reviewer's verdict on round 13; the first
deletion round `.agent/f261_t003_inventory.md` proposes.

── SLICE PLAN13 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN13 sha256=77e2602fc65e08a4451937021583fc2ba546ebd1cae34906d87382c9ff90b02e
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 13 opens T003. It books round 12's PASS, records DECISION F261 D12 and writes
`.agent/f261_t003_inventory.md`, then gives `GroupDef` a `hidden` field that keeps a group out
of both root helps and renames the `plan` group to the hidden `roadmap` group, one table per
commit.

## Next Steps

1. T003's deletion rounds in the order `.agent/f261_t003_inventory.md` proposes, each
   re-measured before it is authored, beginning with `orchestrator`, `rollback` and the `loop`
   command.
2. The prunes of `do`, `job`, `mission` and `worker`, the `--builder` and `--reviewer` flags
   with R-0767 and R-0894, `teach` to `teacher`, the `settings` alias and the `flight_plan`
   rename, with R-0900.
3. T004.

## Risks

- 97 findings are open by distinct id before and after this round's record; three are High,
  R-0803, R-0804 and R-0807.
- The inventory proposes sixteen rounds after this one, past F261's soft limit of 25 rounds;
  the session that reaches the limit owes the scope report and the split-and-close default.
- `job show` prints JSON that the canary, `tests/cli/test_plan_approval.py` and
  `scripts/remedy_smoke.sh` parse, so every change to it only adds keys.
END PLAN13

── SLICE RECORD13 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD13 sha256=125da975f558a12c5aa82c17f47589dc5f5f4347532440b0e94da7c88593f9c7

Gate: F261 R12 — the F261 round 12 entry. VERDICT PASS. Written by the planner and reviewer of session 38 after reading the committed range `a75814c6`..`80e9cc0f` and re-deriving the readings below; the worker's report was evidence for none of them. It is booked here by the first commit of round 13 that writes the record, per operator amendment amend0827-process-diet rule 1. THE TRANSPORT: `.agent/authored/f261-r12.md` at `0e1808d9` and `.agent/last_block.md` at `247fd612` are byte-identical to the reviewer's scratch original, sha256 `2bd2c3d75bdf08906dc31170a50034030625dcf62185f679dd3ffb17d400a870`, and the four tables committed at `01eda6bf`, `b7b2d179`, `f4d5f4dd` and `514941fc` are byte-identical to the reviewer's. THE STATE: at `52b7b07a` and again at `80e9cc0f`, `.agent/plan.md` equals PLAN12, and `.agent/live_review.md` and `.agent/decisions.md` equal their `a75814c6` blobs followed by RECORD12 and DEC11. THE TABLE COMMITS: at `01eda6bf`, `b7b2d179`, `f4d5f4dd` and `514941fc` the `apps`, `tests`, `docs`, `scripts`, `packages` and `README.md` objects equal the reviewer's dry-run commits of the tables, which had reproduced the research helper's trees exactly; each commit's `--no-renames` path set is the dry run's plus its carrier, and `git show --numstat` reads 239, 78, 5 and 367 insertions. In the dry run's production diff the job-result names of the staging pipeline, the fulfillment record, the evidence manifest, the final adjudication and the trace event kind take the apply names DECISION F261 D11 gives, the builder's repair prompt reads `Do not apply changes to the target repository, commit, or push.`, and `promote_ready` and the recommended actions of `packages/orchestration/final_verifier.py` are unchanged. At `80e9cc0f` the grep of the eleven retired names over `apps`, `packages`, `scripts`, `tests`, `docs` without `docs/roadmap`, and `README.md` exits 1 with no output. In the reviewer's dry run a full suite under `-n auto` without `tests/ui_server` read 1 failed, `test_vitest_passes`, and 17673 passed. Over `tests/docs/test_retired_promote_word.py`, `tests/orchestration/test_repair_loop.py`, `tests/orchestration/test_builder_prompt_golden.py`, `tests/orchestration/test_job_fulfillment.py`, `tests/cli/test_job_report.py` and `tests/orchestration/test_evidence_bundle.py`, which passed 362 unmutated, adding the old field beside the new one failed 1 test, adding a job-result token to the model routing module failed 1, removing a kept token from `packages/runtimes/dev_server.py` failed 1, restoring the old blocker code failed 1, restoring the old repair prompt line failed 3, and never allowing an apply failed 1. The record slices applied on top of the dry run passed `tests/docs/`, `tests/ui_server/test_dashboard_contract.py` and the other files the reviewer ran among those that read the edited state files, apart from `test_vitest_passes`, at 854 passed. THE REVIEWER'S RUN in the primary checkout at `80e9cc0f` of those six files, `tests/docs/`, `tests/orchestration/test_final_verifier.py`, `tests/orchestration/test_job_task_runner.py`, `tests/orchestration/test_review_gate_embedded_verdicts.py`, `tests/orchestration/test_self_use_runner.py`, `tests/cli/test_task_input.py`, `tests/orchestration/test_review_final_verifier_reproducible.py`, `tests/orchestration/test_fence_production_e2e.py`, `tests/ui_contracts/test_humanize_catalog.py`, `tests/cli/test_golden_path.py`, `tests/cli/test_job_show.py`, `tests/test_command_catalog.py`, `tests/ui_server/test_dashboard_contract.py` and `tests/orchestration/test_test_runner.py`, whose `test_vitest_passes` runs the UI tests from the primary checkout, read 1295 passed, and `git branch --list 'remedy/job-*'` read 16 lines. The open set reads 97 by distinct id at `80e9cc0f`.
END RECORD13

── SLICE DEC12 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC12 sha256=8214c25e7807c06e8bd41cd37970a549e9cb0f58f7d04655b840c28dcc77afca

## DECISION F261 D12 (2026-09-15, F261 round 13) — a group can be hidden, `plan` becomes the hidden `roadmap` group, and T003 follows a recorded inventory

CONTEXT. DECISION amend0905-vocab D4 names one hidden group, `roadmap`, which "appears in no help at all and stays callable", and `docs/roadmap/features/T2_F261.md` gives `GroupDef` a `hidden` field for it. Measured at `80e9cc0f` by the reviewer's research helpers and re-read by the reviewer on the dry-run trees: `_print_root_help` in `apps/cli/grouped.py` is the only place that lists the groups, for `remedy --help` and for `remedy --all-commands`, and `apps/cli/commands/plan_cmd.py` holds the two commands of the `plan` group.

CHOSEN, FIRST: `GroupDef` gains `hidden: bool = False` as its last field, so every existing construction stays valid. `_print_root_help` lists no hidden group in either form; the parser still adds every group, so a hidden group's own help and its commands work. `tests/cli/test_cli_ux.py` gains `TestHiddenGroup`, which hides existing groups under a monkeypatch and checks both root helps, the group's own help and dispatch.

CHOSEN, SECOND: the group `plan` becomes the group `roadmap`, hidden and not user-facing, placed last in `GROUPS`. Its commands `plan.status` and `plan.next` become `roadmap.status` and `roadmap.next`, `apps/cli/commands/plan_cmd.py` moves to `apps/cli/commands/roadmap_cmd.py` with its handlers, and the pairs join the `RENAMED` list of `tests/test_command_catalog.py`, which gains a check that no old id is left in the dispatch table. `tests/cli/test_plan_cli.py` keeps its file name and gains tests that the group is hidden, that neither root help lists it and that `remedy plan` is an unknown command. `docs/system/roadmap-mirror-v1.md`, its `docs/README.md` row and the docstring of `packages/orchestration/feature_mission_adapter.py` name the new group, and so do the Phase 0 probe lines of `docs/agents/self_drive_protocol.md` and `.claude/skills/remedy-self-drive/SKILL.md`, because a session that ran them as written would call a group that no longer exists. `docs/system/vocabulary.md` keeps its sentences about today's `plan status` and `plan next`, because F259 owns that page.

CHOSEN, THIRD: `.agent/f261_t003_inventory.md` records the measurement of the rest of T003 at `80e9cc0f` and a proposed order of rounds with the rulings they must make; it is a measurement not re-verified by the reviewer, and each round re-measures its own slice before it is authored.

CONSEQUENCE. `remedy plan status` and `remedy plan next` are unknown commands; `remedy roadmap status` and `remedy roadmap next` do what they did, and neither root help names `roadmap`. HOW TO REVERSE: revert the round's two table commits and delete this section and the inventory.
END DEC12

── SLICE INV13 ── target `.agent/f261_t003_inventory.md` ── NEW FILE ──
BEGIN INV13 sha256=5d1ae05fb4f7827d208f8580f64daa3b1393803afc243f06f4c55d3685ce0f8d
# F261 T003 inventory — the prune to DECISION amend0905-vocab D4

Measured at `80e9cc0f` by the reviewer's research helper of session 38, read-only, and NOT
re-verified by the reviewer: sizes are estimates and every round re-measures its own slice before
it is authored. Written by F261 round 13; the order below is a proposal the rounds follow unless
a measurement contradicts it.

## The catalog at `80e9cc0f`

44 groups and 207 commands. After round 13 the `plan` group is the hidden `roadmap` group. The
groups D4 does not name, with their command counts: context 1, context-pack 1, contract 3,
dashboard 2, guide 1, loop 3, orchestrator 4, policy 3, propose 7, queue 4, readiness 2, repair 6,
repo 2, review 4, rollback 2, token 4. Beyond D4's lists today: `do` continue, evidence,
job-resume, repair-attest, replan, report, run; `job` attach-repo, cancel, create, enqueue,
fulfill, pause, permit, rerun, resume-queue; `mission` ledger; `worker` run.

## Findings of the measurement

1. `do report <run_id>` and `do report list` already are D4's `run show <id>` and `run list`, so
   they are renamed rather than deleted; no `run` group exists yet.
2. `do job-resume` resumes a job plan through `resume_job_plan`, while `job resume` is the F047
   checkpoint resume: two commands, one D4 word.
3. `--builder` and `--reviewer` are the only route into the ping-pong path of `do run` and the
   only provider value `job run` passes to `run_job`; `--builder-provider` is validated there
   and then dropped. Deleting the flags needs `job run` wired to the provider flags (R-0767) and
   the ping-pong path of `do run` deleted with its scope flags (R-0894).
4. `job create`, `job attach-repo` and `job permit` carry sections 3 to 6 of
   `scripts/remedy_smoke.sh` and the fixtures of `tests/test_test_runner.py`,
   `tests/orchestration/test_test_runner.py`, `tests/test_command_discovery.py` and
   `tests/test_cli_main.py`; once `job permit` is gone no CLI word grants a capability that
   `test run` and `patch apply` check.
5. Guards that change as groups go: `tests/cli/test_cli_ux.py` asserts at least 40 groups and
   names `token`, `context-pack` and `contract` as internal; `tests/test_command_catalog.py`
   requires the group `policy` and the commands `job.create`, `job.attach-repo`, `job.permit`,
   `policy.contract` and `policy.token`; every `related=` must resolve.
6. The queue heir T003 names, `mission list --status planned`, does not exist, and `run show`,
   `run list`, `worker doctor` and `job run --tasks` have no owning feature; `job contract` and
   `mission contract` belong to F269, and `--plan-only`, `--force-*` and `--step-by-step` to F268.
7. `packages/orchestration/do_continue.py` has one importer, `_cmd_do_continue`, and holds the
   `do --continue` hints R-0900 names.
8. `flight_plan`, `flight plan` and `FlightPlan` occur in about 97 lines under `apps/cli`, 27
   under `apps/ui`, 236 under `packages`, 469 under `tests` and 22 under `docs`; `JobPlan`
   already names the job record, so `FlightPlan` needs another name; the job record key
   `flight_plan`, the schema tag `flight_plan_v1`, the decision type `flight_plan_approval` and
   the planner prompt text are persisted or frozen names.

## Proposed order

| Round | Commits | Deletion round (amend0906 rule 1) |
|---|---|---|
| A | `orchestrator` · `rollback` · the `loop` command | yes |
| B | the loop modules and the report's loop reference · the `queue` command · `job_queue.py` with the F048 binding, its config keys and `queue_dir`, with a deletion paragraph naming the heirs | yes |
| C | `guide` (with the group-count guard) · `dashboard` · `repo` with its `dev status` block | yes, if their hints are deleted |
| D | `readiness` · `contract` and its hints · `policy` | no |
| E | `context` · `token` with `context-pack` · `review` | no |
| F | `do report` becomes `run show` and `run list` · `do evidence` | no |
| G | `do repair-attest` · `do job-resume` · `do replan` | mostly |
| H | the `do continue` hints, then the command and `do_continue.py`, with R-0900 | no |
| I | `propose` · `repair` | no |
| J | `job run` provider wiring (R-0767) · the ping-pong path of `do run` with its flags (R-0894) | no |
| K | the queue commands of `job` with `worker run` · `mission ledger` | mostly |
| L | `job rerun` · `job fulfill` | yes |
| M | the fixtures and the smoke spine moved off `job create` · `job create`, `job attach-repo`, `job permit` | no |
| N | `teach` becomes `teacher` · the `settings` alias | no |
| O, P | the `flight_plan` rename in two rounds: module, identifiers and schema names; job key, schema tag, decision type, prompt text, prose | no |

Ordering constraints: a hint is re-pointed or deleted in or before the commit that deletes its
command, as DECISION F261 D10 did; `related=` chains are cut in the order guide, repo,
readiness, contract, policy and `do continue` before `repair`; `do replan` goes before the
`flight_plan` rename; fixtures move before `job create` is deleted.

## Rulings the rounds must make

1. Package code orphaned by a command deletion is deleted in the same round when its only
   production importer dies; where it still feeds a cockpit section, a finding is registered.
2. A cockpit route whose payload is a deleted command's output goes with it.
3. `do run` loses only `--builder`, `--reviewer`, the flags only its ping-pong path reads and
   the scope flags; its other flags belong to F268.
4. `job run` passes `--builder-provider` and `--reviewer-provider` to `run_job`, a wiring change
   of a surviving command that needs its own DECISION.
5. `do job-resume` goes with heir `job run`, and the recoverability guard it loses is a finding.
6. `mission ledger` goes with heir the ledger `mission run` prints.
7. `job create`, `job attach-repo`, `job permit` and `job fulfill` go, with findings for the
   capability grant and the repository attach they leave to F269 and F268.
8. Findings are registered for the D4 words no feature owns: `run show` and `run list` if F261
   does not rename `do report` into them, `worker doctor`, `job run --tasks` and
   `mission list --status`.
9. The name that replaces `FlightPlan`, and no reader of the old job key, per DECISION D-A.
10. Whether `teach` becomes `teacher` in words only or also in file and function names.
11. The `settings` alias as an `aliases` field of `GroupDef` with one resolver for every group
    lookup.

## The projection

The proposal is sixteen rounds after round 13, so T003 alone reaches past F261's soft limit of
25 rounds; the session that reaches the limit owes the scope report and executes the
split-and-close default of operator amendment amend0905-throughput.
END INV13

── SLICE MUT-1-FROM ── G5 (1) only ── never a file ──
BEGIN MUT-1-FROM sha256=666cfc8fc99219a08aa4da687103e0983b55cbac7efb20729f7d34a083ac620f
        groups = [(gid, gdef.description) for gid, gdef in GROUPS.items() if not gdef.hidden]
END MUT-1-FROM

── SLICE MUT-1-TO ── G5 (1) only ── never a file ──
BEGIN MUT-1-TO sha256=511e0956c11dc70ceaaafdb472086a8c62842fc523d0931fee5ba0ecf694873c
        groups = [(gid, gdef.description) for gid, gdef in GROUPS.items()]
END MUT-1-TO

── SLICE MUT-2-FROM ── G5 (2) only ── never a file ──
BEGIN MUT-2-FROM sha256=ca48166e3336ee655c345788bedb7e24c7183f72cc6a3aa60367d66d9aab48ee
            if gdef.user_facing and not gdef.hidden
END MUT-2-FROM

── SLICE MUT-2-TO ── G5 (2) only ── never a file ──
BEGIN MUT-2-TO sha256=2fa0edd772496e3387cb444420332f7c2787cd700ecdd2a9a02d01eadd0a0d54
            if gdef.user_facing
END MUT-2-TO

── SLICE MUT-3-FROM ── G5 (3) only ── never a file ──
BEGIN MUT-3-FROM sha256=a5f423e6a62c476c9fd43c11d5af668d8ba649327150b6727422157614f306a5
Proposes, never starts.", user_facing=False, hidden=True),
END MUT-3-FROM

── SLICE MUT-3-TO ── G5 (3) only ── never a file ──
BEGIN MUT-3-TO sha256=55305542ff39f230d72e14bb9e47a94268d5454b630e079da51d8e7e1a2f47be
Proposes, never starts.", user_facing=False),
END MUT-3-TO

── SLICE MUT-4-FROM ── G5 (4) only ── never a file ──
BEGIN MUT-4-FROM sha256=6c709a3f1dea23e1b8a0a7ea761bc3ec8686d2751e95a3276545c9219950938e
    "roadmap.next": lambda args: _cmd_roadmap_next(args),
END MUT-4-FROM

── SLICE MUT-4-TO ── G5 (4) only ── never a file ──
BEGIN MUT-4-TO sha256=73c97955c34483a1406c3881ffcb6e229724f0058d8e770bd84e53170b86007d
    "roadmap.next": lambda args: _cmd_roadmap_next(args),
    "plan.next": lambda args: _cmd_roadmap_next(args),
END MUT-4-TO

── SLICE MUT-5-FROM ── G5 (5) only ── never a file ──
BEGIN MUT-5-FROM sha256=f84c4a39038cc025f46c8aa277834701a1db34548f5707e9bc7e88035a655694
    for group_id, group_def in GROUPS.items():
        group_parser = group_parsers.add_parser(
END MUT-5-FROM

── SLICE MUT-5-TO ── G5 (5) only ── never a file ──
BEGIN MUT-5-TO sha256=e5cf4c2afd28987f5ecdaeb88d071bdf6e5e05f2d0c1c44bb2288958062f5fbe
    for group_id, group_def in GROUPS.items():
        if group_def.hidden:
            continue
        group_parser = group_parsers.add_parser(
END MUT-5-TO
