STEP T001 — F275 round 16 — delete the main builder adapter module group, the ELEVENTH

Goal: book session 9's round 15 PASS, its five prose slips and its resolution of R-0855;
register the two findings this round owes; and delete
`packages/orchestration/main_builder_adapter` whole, with its handler, the `builder` group and
its ten commands, six `ContractAction` members, the three `worker` commands whose remaining
half it carried, two test files and two documentation pages.

This is a PRODUCTION round. `apps/cli/commands/worker_facade_cmd.py` loses three of its five
commands and the alias registry that served only them; `apps/cli/command_catalog.py` loses a
whole group and a dangling `related=` reference; and a documented operator path in
`docs/system/core-product-spine-v0.md` loses a numbered step and is renumbered.

Base: `38e03d2f`. Branch: `feature/f275-one-world-completion-part-three`. Session 9, round 16.

EVERY NUMERAL BELOW WAS MEASURED BY AN APPLIED DRY RUN, NOT DERIVED. The reviewer applied this
exact change set in a disposable worktree at `38e03d2f`, ran the full suite serially to green
with the change COMMITTED, ran all four red-proofs with matched controls, and read the numstat
off the resulting commit. Where a number below disagrees with what you measure, REPORT THE
MEASUREMENT AND DO NOT ADJUST THE CHANGE SET.

WHY THE THREE `worker` COMMANDS DIE RATHER THAN NARROW AGAIN. Round 15 registered R-0857 when
it took the TEMPLATE half of `worker doctor`, `worker add` and `worker disable`; that finding's
FIX CLAUSE binds this round by name and orders those three deleted WHOLE rather than left
reporting that an adapter which no longer exists is absent. This block discharges that clause.


BUNDLE — the commits below, in this order

  C0a  save the authored block:  `shutil.copyfile` `.remedy-wt/f275-r16.md` to
       `.agent/authored/f275-r16.md`. Never retype it.
  C0b  mirror the same bytes:    `shutil.copyfile` the same source to `.agent/last_block.md`.
  C1   advance `.agent/plan.md`  — replaced WHOLE by the PLAN16 slice.
  C2   the record: append LEDGER16 to `.agent/live_review.md` and SLIPS16 to
       `.agent/prose_slips.md`.
  C3   delete the module group — twenty-four paths.
  C4   the handback: rewrite `.agent/handoff.md` whole.

C1 is the FIRST substantive commit and advances the plan before the ledger commit, per §3
item 23. C2 books round 15's verdict and its resolution of R-0855 and registers R-0859 and
R-0860 BEFORE C3 changes anything they describe, which is the ordering §3 item 20's R-0524
carve-out requires of a slice stating a fact about this round's own landed change; the R-0860
paragraph names that ordering rather than a SHA that cannot exist when it is written.


THE CHANGE SET OF C3 — twenty-four paths, 13 insertions against 2502 deletions

WHOLE-FILE REMOVALS, six paths, by `git rm`:
  packages/orchestration/main_builder_adapter.py                   0 / 964
  apps/cli/commands/main_builder_adapter_cmd.py                    0 / 143
  tests/orchestration/test_main_builder_adapter.py                 0 / 474
  tests/cli/test_main_builder_adapter_cli.py                       0 / 139
  docs/system/main-builder-adapter-v0-token-controlled-session-rail.md   0 / 142
  docs/guides/main-builder-adapter-user-guide-v0.md                0 / 80

CATALOG AND CONTRACT:
  apps/cli/command_catalog.py                                      1 / 142
      Delete the `"builder": GroupDef(...)` line; delete the 110-line span that begins at the
      `# ── builder (Main Builder Adapter v0, Step 1981) ───` section comment and ends at the
      `),` closing the LAST `CommandEntry` whose `group_id="builder"` — that span holds TEN
      command records, and you count them from the span rather than from this sentence and
      report the number you counted. THE SPAN STOPS BEFORE THE NEXT SECTION COMMENT: the line
      `# ── brain ───` belongs to the section that follows and MUST SURVIVE. The reviewer's
      own first dry run swallowed it, and every `# ── ` section comment in the file is to be
      counted before and after to prove none was lost. Then delete the three `CommandEntry`
      records whose `command_id` is `"worker.doctor"`, `"worker.add"` and `"worker.disable"` —
      30 lines — leaving the `worker` GROUP itself alive with its nine other commands. Finally
      the ONE insertion: the surviving `mission.run` record reads
      `related=("worker.doctor", "mission.report")`, which after this commit names a command
      that does not exist, so it becomes `related=("mission.report",)`.
  packages/orchestration/run_contract.py                           0 / 12
      Delete the six `ContractAction` members `BUILDER_ADAPTER_SHOW`,
      `BUILDER_ADAPTER_ENABLE`, `BUILDER_PACKAGE_CREATE`, `BUILDER_SESSION_CREATE`,
      `BUILDER_SESSION_SHOW` and `BUILDER_SESSION_INTAKE`, and their six
      `_DEFAULT_ALLOWED_ACTIONS` rows. `BUILDER_ROUTING_DECIDE`, `BUILDER_ROUTING_REPORT` and
      the three `EXTERNAL_BUILDER_*` members are DIFFERENT actions and SURVIVE: none of them
      begins with `BUILDER_ADAPTER_`, `BUILDER_PACKAGE_` or `BUILDER_SESSION_`.
  apps/cli/commands/__init__.py                                    1 / 2
      `main_builder_adapter_cmd` out of the import block and out of the `for mod in (…)` tuple.

THE SURVIVOR THAT LOSES CODE:
  apps/cli/commands/worker_facade_cmd.py                           0 / 210
      Delete `_cmd_worker_doctor`, `_cmd_worker_add` and `_cmd_worker_disable` whole, their
      three `COMMAND_HANDLERS` rows, and the four section-banner comment blocks that titled
      them and the alias registry. Delete `_WORKER_ALIASES` and `_resolve_alias`: after the
      three commands go, this round's own sweep shows they have no reader left, which is
      R-0855's fix clause applied to this deletion. `_err`, `_cmd_mission_run`,
      `remedy_scripts_dir` and `_cmd_doctor_core` SURVIVE, and `COMMAND_HANDLERS` keeps
      `mission.run` and `doctor.core`.

TESTS:
  tests/cli/test_worker_facade_cmd.py                              4 / 157
      Delete the classes `TestWorkerAliasRegistry`, `TestWorkerDoctor`, `TestWorkerAdd` and
      `TestWorkerDisable` whole, with the banner comment above each. In
      `TestHandlerRegistry::test_all_handlers_present` the expected set becomes
      `{"mission.run", "doctor.core"}`; in
      `TestCatalogIntegration::test_worker_facade_commands_in_catalog` the tuple becomes
      `("mission.run", "mission.report")`; in `TestCollectHandlers::test_facade_in_collected`
      it becomes `("mission.run", "mission.report", "doctor.core")`. In
      `TestCatalogIntegration::test_all_facade_commands_have_handlers` the assertion
      `len(facade_cmds) == 5` becomes `len(facade_cmds) == len(COMMAND_HANDLERS)`: the
      PROPERTY it existed to state is that every handler the facade registers is carried by the
      catalog, and a literal is a pin that goes stale every time the facade changes (§3 item
      16). Finally `from unittest.mock import patch` has no remaining user and goes, and the
      blank line ruff's `I001` wants after `import pytest` goes with it.
  tests/cli/test_product_spine.py                                  1 / 13
      Delete `test_worker_facade_in_catalog` and `test_worker_doctor_is_read_only` whole, and
      in `test_all_operator_commands_have_handlers` the tuple becomes
      `("mission.run", "mission.report", "doctor.core")`.
  tests/orchestration/test_development_artifact_boundary.py        4 / 8
      Drop `"main_builder_adapter"` from `_PRODUCT_MODULES`; delete the
      `test_main_builder_adapter` method whole. Its deletion would leave
      `test_worker_doctor_core_no_agent` iterating an EMPTY tuple, which asserts nothing, so
      REPOINT that loop at the four modules `_cmd_doctor_core` really imports —
      `apps.cli.commands.worker_facade_cmd`, `apps.cli.command_catalog`,
      `packages.orchestration.run_contract` and `packages.orchestration.config`. The guard then
      states the property its name claims instead of degenerating to a vacuous pass.
  tests/cli/test_cli_ux.py                                         1 / 1
      Drop `"builder"` from the hardcoded `_INTERNAL_GROUPS` set.
  tests/orchestration/test_cluster_deletion_map.py                 0 / 2
  tests/orchestration/import_reachability_allowlist.txt            0 / 2
  tests/orchestration/cluster_deletion_map.txt                     0 / 1

PACKAGING, SCRIPTS AND THE ORDER FILE:
  pyproject.toml                                                   0 / 1
  scripts/remedy_test_fast.sh                                      0 / 1
  .agent/f275_deletion_order.md                                    0 / 1
      REGENERATED from `measured_order()`, never typed, keeping the 26 header lines
      BYTE-VERBATIM and writing one component per line, comma-joined within a cycle, NO leading
      indentation, TRAILING NEWLINE. `_render` in
      `tests/orchestration/test_cluster_deletion_order.py` is the ASSERTION MESSAGE's formatter
      and indents by two spaces; it is NOT this file's format. Unlike round 15's this
      regeneration is a PURE SHRINK — five components fall to four and no survivor moves — so a
      `0 1` numstat is correct here and would have been wrong last round.

DOCUMENTATION:
  docs/README.md                                                   0 / 2
      The two rows linking the deleted pages, matched on the LINK TARGET.
  docs/system/core-product-spine-v0.md                             1 / 2
      The numbered operator path loses `6. Check worker → remedy worker doctor <name> --json`
      and the list is RENUMBERED WHOLE from seven steps to six, per §3 item 17: a pair that
      changes a numbered structure's arity spans the whole structure, so the old step 7
      becomes step 6 in the same edit rather than leaving two steps numbered 6.
  docs/system/development-artifact-boundary-v0.md                  0 / 2
      The `Builder status` and `Package truth` table rows, both naming the deleted module.
  docs/system/test-lanes-v0.md                                     0 / 1

DELIBERATELY NOT TOUCHED, the round's one scope ruling, unchanged from round 15: the roadmap
files under `docs/roadmap/features/` that still name a deleted token. `T2_F085.md`,
`T2_F151.md` and `T2_F262.md` are `[x]` in `docs/roadmap/STATUS.md` and are closed features'
records of what they built; `T2_F260.md` carries the deletion LIST that authorises this work
and must stand until the list is discharged; `T2_F267.md` is `[ ]` and its repair is already
registered as R-0858.


CONSTRAINTS

 1. Apply every authored slice BYTE FOR BYTE. If a slice looks wrong, apply it as written and
    declare it in the handback. Never edit a slice.
 2. The change set above is EXHAUSTIVE. Touch no other path. If a gate demands a change to a
    path not listed, stop and declare it rather than widening.
 3. Each append is `post = pre + b"\n" + slice`, where the slice is the bytes strictly between
    its marker lines INCLUDING the newline that ends its last text line — round 15 measured
    that convention against round 14's commits and it is stated here so no worker has to
    re-derive it. Both targets end with a newline, so the joining byte is one `\n`.
 4. `.agent/plan.md` is replaced WHOLE by PLAN16. Measure its line count against the AGENTS.md
    cap of 50 and report the number you measured; it carries `## Goal` and `## Next Steps`.
 5. Destructive verification runs ONLY inside a disposable `git worktree` under `.remedy-wt/`.
    The primary checkout satisfies `git status --porcelain` empty at the handback.
 6. Env-var assignment (`VAR=x cmd`, `env VAR=x`, `export`) and `cp` are DENIED by this
    sandbox. Copy with `python3 -c "import shutil; shutil.copyfile(a, b)"`. Capture real exit
    codes with `bash -c '<cmd>; echo "REAL_EXIT=$?"'` or from `subprocess.run`.
 7. The full suite is run SERIALLY in the PRIMARY checkout with the change COMMITTED. Under
    `-n auto` the `ui_server` command-channel tests race for a port. A fresh worktree has no
    `apps/ui/node_modules`, which is why the suite gate is not run in one. NOTE, measured by
    the reviewer twice now: `tests/orchestration/test_evidence_index.py` reads
    `git status --porcelain`, so it FAILS while the deletion is unstaged and PASSES once the
    change is committed. Commit C3 before running the suite.
 8. R-0855's FIX CLAUSE BINDS THIS BLOCK and this block discharges it in its own text: the
    `_WORKER_ALIASES` / `_resolve_alias` order, the four banner-comment orders, the
    `related=` repair and the documentation orders ARE that sweep. R-0857's fix clause binds it
    too and is discharged by deleting the three `worker` commands whole. No further sweep is
    owed and none may be invented.
 9. Report every number you measure even where it differs from a number above.
10. In the change-set section the runs of SPACES that align the `ins / del` column carry no
    meaning and are not appliable bytes: the appliable bytes are the three marker-delimited
    slices alone, each proved against its own target by its own gate, and G8 resolves the
    commit against the PATH SET rather than any column position (§3 item 37).


AUTHORED SLICES

--- BEGIN-PLAN16 ---
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 16 books round 15's PASS, five prose slips and the resolution of R-0855, registers R-0859
and R-0860, and deletes the ELEVENTH module group,
`packages/orchestration/main_builder_adapter.py`, whole. This is a PRODUCTION round: the
`builder` group and its ten commands go, six `ContractAction` members go, and
`worker_facade_cmd.py` loses three of its five commands — `worker doctor`, `worker add` and
`worker disable` — which R-0857's fix clause orders deleted whole rather than narrowed a second
time.

## Next Steps

1. The `overnight_executor` component, which this round's regeneration makes the order file's
   first line. It is a SINGLE module.
2. The remaining components in the recorded order — `worker_registry`, then
   `overnight_readiness`, then the `provider_trust` / `provider_trust_verification` pair, which
   is the last cycle.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831,
   R-0840, R-0842, R-0844 through R-0846, R-0848, R-0849 and R-0851 through R-0860 named among
   the ideas deleted rather than inherited. That round also discharges R-0843's widened sweep
   and R-0858's repair of F267.
4. T002, the atomic record flip, alone, because every later commit's size depends on its
   ruling.

## Risks

- The open set is 83 by distinct id at this round's base `38e03d2f`; the ledger commit this
  block fixes as C2 registers two and resolves one, taking it to 84. Four are High — R-0803,
  R-0804, R-0806 and R-0807 — all F273's rather than this feature's, per DECISION F272 D12.
- This round removes three USER-FACING commands and a documented step from the core product
  spine. R-0860 records the loss and its inheritor; no stub, shim or alias replaces them.
- The full suite is run SERIALLY: under `pytest -n auto` the `ui_server` command-channel tests
  race for a port, and the vitest node needs `apps/ui/node_modules`.
--- END-PLAN16 ---

--- BEGIN-SLIPS16 ---
2026-09-09 · F275 R15 · The round 15 block's constraint 3 stated that each authored slice "carries no trailing newline of its own" and that the append is `post = pre + b"\n" + slice`. The second half is right and the first is wrong: the slices as delimited by their marker lines DO end in a newline, and only the inclusive reading reproduces the committed `.agent/plan.md` at 2588 bytes. The worker proved the convention against round 14's own commits before writing a byte, applied the inclusive reading, and declared the difference; the reviewer confirmed it independently at both readings. Nothing landed wrong because the growth arithmetic `growth == 1 + len(slice)` holds under the reading actually used. The lesson is that a block which states a slice's TERMINAL BYTE must measure that byte rather than describe it, because the extraction and the sentence beside it are produced by different means and only one of them was mechanical.

2026-09-09 · F275 R15 · The round 15 block's BUNDLE heading read "six commits, in this order" above a list of SEVEN — C0a, C0b, C1, C2, C3, C4 and C5. Seven were ordered, seven were made in order, and no gate could see the discrepancy because every gate resolves against the named commits rather than the count; the worker caught it and reported it. This is §3 item 16 exactly — a heading stating a count of the contents beneath it — committed in the block written by the reviewer who had just re-read that item, which is why the item says to sweep every heading rather than the one that changed.

2026-09-09 · F275 R15 · Four numerals in the round 15 block were wrong: constraint 4 said PLAN15 was 44 lines against an actual 45; the change-set spec said `packages/orchestration/exec_guard.py` was 24/19 against an actual 24/21 and `apps/cli/command_catalog.py` was 0/197 against an actual 0/196; and the C4 total said 42/4801 against an actual 42/4802, which is exactly the sum of the two path-level corrections. The worker measured all four correctly and declared them. The `command_catalog.py` figure has a diagnosable cause worth keeping: the reviewer's dry-run applier deleted a section's `CommandEntry` block by scanning forward to the next non-matching `CommandEntry`, which swallowed the FOLLOWING section's `# ── ` comment line, while the worker applied the block's SPEC — a span ending at the last matching record — and did not. The landed state is the worker's and is correct. The lesson is that a block shipping a SPEC per path re-derives its `+/-` column from the FINAL dry-run commits, and that a span-scanning applier stops at the next SECTION COMMENT, not at the next record.

2026-09-09 · F275 R15 · The round 15 block ordered `Landed: R-XXXX` discipline in its handback section while its C3 change set named only three paths, none of them `.agent/live_review.md`, and constraint 2 declared that change set exhaustive. The two orders cannot both be obeyed, so the worker routed the `Landed: R-0855` line into `.agent/handoff.md`, which amend0827-process-diet rule 1 makes a durable carrier, and declared it. That was the correct resolution of the reviewer's contradiction. The lesson is that a block whose round RESOLVES a finding names `.agent/live_review.md` in the change set of the commit that resolves it, or says in its own text where the landed line is to be written.

2026-09-09 · F275 R15 · While re-running gate G5 the reviewer prefixed its probe command with `git checkout 795e4080 -- .`, which reverted and staged `.agent/handoff.md` in the PRIMARY checkout — a work-tree write by a role that writes nothing. It was caught immediately by `git status --porcelain`, restored with `git checkout HEAD --` plus `git reset`, and the restored file proved byte-identical to the committed `38e03d2f` blob at 19871 bytes; no commit was made and no history was touched. The lesson is that a read-only re-gate composes its probes out of `git show <sha>:<path>` and disposable worktrees only, and never out of a command that writes into the checkout it is measuring.
--- END-SLIPS16 ---

--- BEGIN-LEDGER16 ---
Gate: F275 R15 — the F275 round 15 entry. VERDICT PASS, booked by round 16 rather than by a round of its own, per operator amendment amend0827-process-diet rule 1, and carried from the pushed `.agent/handoff.md` at `38e03d2f`, which that rule makes a durable carrier. THE VERDICT WAS ISSUED BY THE PLANNER AND REVIEWER OF SESSION 9, which re-ran every one of the eight gates itself against the COMMITTED blobs over the range `fadf4715`..`38e03d2f`; the worker's report was evidence for nothing. Seven single-parent commits C0a `d68fa6d2`, C0b `74b90eab`, C1 `b98dcf29`, C2 `a33a93a6`, C3 `8124377d`, C4 `795e4080` and C5 `38e03d2f`, with per-commit insertions 433, 408, 20, 26, 3 and 42 for the six before the handback commit, every one under the AGENTS.md DECISION F104 D1 cap of 500. G1 WAS THE PRIMARY PROOF OF §4 ITEM 9 AND NOT THE DIGEST FALLBACK: the reviewer's own delegation source and both committed copies are 48472 bytes at `bbb87d8b66a18521c37f6214526202700667be0174b9b3a543df3442216eb0e4` and compare BYTE-EQUAL; per §3 item 37 that chain covers those three artefacts and claims nothing about the emitted bytes. G2: `.agent/plan.md` byte-identical to PLAN15 at 2588 bytes and `5a43749f…`, 45 lines against the cap of 50, both mandated headings present, the block 433 lines against its cap of 490. G3, OVER THREE APPENDS: `.agent/live_review.md` 618783 to 634559, growth 15776 = 1 + 15775; `.agent/prose_slips.md` 184231 to 185058, growth 827 = 1 + 826; `.agent/decisions.md` 966757 to 970963, growth 4206 = 1 + 4205; for each the prefix and suffix byte-exact and the joining byte read back as a newline; N COUNTED from each slice by the reviewer's own reader as 5, 1 and 7, ordered equality holding over the WHOLE appended region with a per-unit sha256 on both sides for all thirteen units; and ALL THREE negative controls, flipped IN MEMORY inside the FIRST appended paragraph per §3 item 36, REJECTED by BOTH readers, with all three files re-read from disk and byte-equal to their committed post-blobs. `^Gate: ` 36 to 37, and `^Gate: F275 R14 `, `^- R-0855 — `, `^- R-0856 — `, `^- R-0857 — `, `^- R-0858 — ` and `^## DECISION F275 D7 ` exactly 1 each; THE OPEN SET 79 TO 83 BY DISTINCT ID against registrations 83 to 87 and resolutions 4 to 4. G4: all EIGHT whole-file removals absent from `git ls-tree` at C4 over 4567 tracked files, and the sweep over the 1682 tracked files outside `.agent/` and `.data/`, printed IN FULL, read exactly TEN lines RAW and FOUR with backtick-quoted spans stripped; three of the four are the `docs/roadmap/features/` lines the round's scope ruling declares and the fourth is the FALSE POSITIVE the block names by path, `tests/cli/test_real_test_execution_cli.py:79`, where the token `execution.list` matches inside `real_test_execution.list_test_runs`. G5: through the SHIPPED readers, by import with the resolved `__file__` printed at both ends, `_BASE_CATALOG` and `collect_all_handlers()` both fell 267 to 250, `GROUPS` 49 to 48 and `ALL_KNOWN_ACTIONS` 120 to 106, zero duplicate ids at both ends; all SEVENTEEN `execution.` ids PRESENT in both readers at the base and ABSENT from both at C4, `execution` gone from `GROUPS`; and THE HUMAN APPROVAL GATE PROVEN UNTOUCHED BY IMPORT RATHER THAN BY ASSERTION, with `patch.approve`, `do.continue`, `worker.doctor`, `worker.add`, `worker.disable`, `mission.run`, `doctor.core` and `builder.adapter-show` all PRESENT at C4. The regenerated order file holds FIVE components against six, compares EQUAL to a fresh regeneration from the live import graph at both ends, and its 26-line header sha256 is unchanged at `aff913e6…`; the REORDER DECISION F275 D3 permits is visible, `main_builder_adapter` moving from position four to position one. G6: ALL FOUR RED-PROOFS RE-RUN BY THE REVIEWER IN ITS OWN DISPOSABLE WORKTREE AT C4, `__pycache__` purged before every run, `python3 -B`, each probe's control run over that probe's OWN selection in the SAME script immediately before its mutation — controls exit 0 at 3, 3, 3 and 51 passed against mutants exit 1 at 1, 1, 2 and 2 failures — every target restored byte-identically and proved by sha256, worktree porcelain empty. G7: ruff `All checks passed!` at exit 0 over all thirteen edited Python files still existing at C4, repo-wide `ruff check .` reading 26 diagnostics at BOTH ends with the two SETS compared item by item and IDENTICAL; ratchets 870 passed and canary 42 passed, both exit 0; and THE FULL SUITE RE-RUN BY THE REVIEWER SERIALLY IN THE PRIMARY CHECKOUT, GREEN at 18689 passed, 23 skipped and ZERO failed, with 18689 + 23 = 18712 equal to the tip collection exactly. The arithmetic closes BY THE ID SET: 18867 at the base against 18712 at the tip, 157 LOST and 2 GAINED, attributed 133 to `tests/orchestration/test_managed_builder_execution.py`, 12 to `tests/cli/test_managed_builder_execution_cli.py`, 8 to `tests/test_grouped_cli.py` — which parametrises over the catalog and is in no change set — 2 to the two RENAMED node ids, 1 to `test_development_artifact_boundary.py` and 1 to `test_product_spine.py`; the 2 GAINED are exactly the two renames C4 orders, so a GAINED set is expected and is not a defect. G8: `.agent/STOP` absent, porcelain empty, ONE worktree, branch correct, and both path sets EXACT with the missing and extra sets EMPTY for each. WHAT THE ROUND ACHIEVED: the TENTH module group, `managed_builder_execution` at 1694 module lines, in ONE commit at 42 insertions against 4802 deletions over 30 paths — the largest single deletion of this feature — taking its 350-line handler whole, SEVENTEEN commands, the `execution` group, FOURTEEN `ContractAction` members, two test files and FOUR documentation pages, two of which the reviewer's own token sweep found and which appear in no consumer map this feature ever produced. It also carried a RULING and a REPAIR: DECISION F275 D7 records, from a repo-wide resolution of every caller of the four approval functions, that deleting `remedy execution approve` together with the executor it gates leaves no ungated path because NOT ONE SURVIVING MODULE CALLS ANY OF THEM; and C3 discharged R-0855. THE WORKER'S EIGHT DECLARED DEVIATIONS ARE ALL SUSTAINED AND SIX ARE THE REVIEWER'S OWN AUTHORING ERRORS: the slice trailing-newline convention, which the worker proved against round 14's commits and applied correctly; four wrong numerals, all of which the worker measured right; and a BUNDLE heading counting six over a body of seven. None put anything wrong on disk, so under amend0827-process-diet rule 2 each is a dated `.agent/prose_slips.md` line and not an id. ONE DEVIATION IS THE REVIEWER'S OWN CONDUCT: while re-running G5 it prefixed a probe with `git checkout 795e4080 -- .`, which reverted and staged `.agent/handoff.md` in the primary checkout — a work-tree write by a read-only role — caught by the next porcelain, restored, and proved byte-identical to the committed `38e03d2f` blob at 19871 bytes, with no commit made and no history touched. It is recorded because a reviewer that hides its own slip cannot be trusted about the worker's.

Done: R-0855 — RESOLVED at C3 `8124377d`, verified by the reviewer of session 9 reading the committed diff rather than the worker's report. All three instances the finding names are gone. FIRST, `apps/cli/commands/orchestrator_cmd.py` loses the three lines `adv = data.get("advisor")`, `if adv:` and the print beneath them, so no code path now reads a JSON key round 14 removed. SECOND, `packages/orchestration/orchestrator_brain.py` loses the whole Local Model Advisor banner, its explanatory paragraph and `_CONFIDENCE_ORDER`, whose only reader round 14 had already deleted. THIRD, the `CLUSTER_MODULES` comment in `tests/orchestration/test_cluster_deletion_map.py` is rewritten to state NO count, per §3 item 16, and says in its own words why: the tuple loses a module group per deletion round, so any numeral there is stale from the next commit onward. The finding's FIX CLAUSE was also honoured by the block that ordered this repair — the round 15 block accompanies every definition it orders deleted with an order to sweep that definition's callers, its readerless constants and the section comment above it, and says so in its own constraint 8 — and that clause REMAINS BINDING on every remaining deletion round of this feature, including the one this entry's block orders. The worker wrote `Landed: R-0855` into `.agent/handoff.md` rather than into this record because the block's C3 change set did not name `.agent/live_review.md` and constraint 2 forbids touching an unnamed path; that omission is the reviewer's, the worker's routing was correct, and this paragraph is the authored resolution that replaces the landed line.

- R-0859 — Medium, THE COMMAND CATALOG CARRIES `related=` CROSS-REFERENCES TO COMMANDS THAT NO LONGER EXIST, AND NO GUARD IN THE REPOSITORY CAN SEE THEM. Measured by the reviewer of session 9 at `38e03d2f` by resolving every `related=` tuple in `apps/cli/command_catalog.py` against the live `_BASE_CATALOG` ids read from the SHIPPED reader by import: 250 live ids, and TWO dangling references. `mission.ledger` names `dogfood.run-loop`, deleted by F272 across its rounds 20 to 22; and a `readiness`-group record names `readiness.show`, likewise long gone. Both PREDATE this round — they are not caused by the deletion the next entry describes, and the measurement was taken at the tip BEFORE that deletion was applied. WHY NO GATE SEES IT: `tests/cli/test_advertised_commands.py` scans SCRIPTS AND DOCUMENTATION for advertised command strings and never reads `related=`; the catalog integrity tests check ids, groups and duplicate ids but not the referential closure of `related=`; and `remedy --all-commands` prints the list without resolving it. So a `related=` tuple is the one place in the catalog where a deleted command can survive indefinitely, which is precisely the "attic" AGENTS.md Scope Control forbids by name, and this feature has deleted ELEVEN module groups without one of them being caught. THE HISTORICAL EVIDENCE THAT THIS IS A REGRESSION RATHER THAN A STANDING GAP: the `Gate: F275 R6` entry in this record shows the reviewer of that round checking by hand that "the catalog carries ZERO surviving `command_id` or `related` references to either dead id" and noting that `context.inspect` now reads `related=('context.pack',)`. That check was performed once, by hand, and never again, which is the rule-in-a-round's-prose class R-0548 names. WHY THIS IS AN ID AND NOT A PROSE SLIP: two `related=` tuples in `apps/cli/command_catalog.py` name commands that do not exist, which is wrong state on disk under `apps/`, exactly what amend0827-process-diet rule 2 reserves an id for. WHAT WOULD RESOLVE IT, and both halves are owed: the two dangling references repaired, and A TEST that resolves every `related=` entry against the catalog's own ids so the eleventh deletion cannot repeat the tenth's silence — a single set-difference assertion, which is the cheapest possible guard and would have caught both of these the day they were made. FIX CLAUSE, binding on the round that drafts DECISION F260 D3, which is the last round of this feature whose change set already contains both `apps/cli/command_catalog.py` and a test directory: that round repairs both dangling references and adds the referential-closure test, and names this id in its own commit message. Until that test exists, every remaining deletion round of this feature resolves `related=` by hand as part of R-0855's sweep, and says in its block that it did.

- R-0860 — Medium, THE MANAGED-BUILDER ADAPTER SURFACE IS DELETED: THE `builder` GROUP AND ITS TEN COMMANDS, SIX RUN-PERMISSION ACTIONS, THREE USER-FACING `worker` COMMANDS AND A NUMBERED STEP OF THE DOCUMENTED OPERATOR PATH. Registered under operator RULE 3 of `docs/roadmap/features/T2_F275.md` T001, which requires a round removing a user-observable behaviour to name the behaviour and the feature that inherits the idea. THIS PARAGRAPH DESCRIBES THIS ROUND'S OWN LANDED CHANGE, so under §3 item 20's R-0524 carve-out it names no SHA — the commit it describes does not exist when it is written — and names instead the ordering its block fixes: the block's BUNDLE orders this registration as C2 and the deletion as C3, so every past-tense reading below is true from C3 onward and of no earlier commit. THE BEHAVIOUR LOST, first half: `builder.adapter-list`, `adapter-show`, `adapter-enable`, `package-create`, `session-create`, `session-show`, `session-list`, `session-record-output`, `session-intake` and `integrity` — the adapter registry that named an external builder and its mode, the BuilderRequestPackage a job handed it, and the session record that bound the two — together with six `ContractAction` members, so a run contract can no longer name an adapter action as permitted. SECOND HALF, and this is the part a user notices: `remedy worker doctor`, `remedy worker add` and `remedy worker disable` are DELETED, not narrowed. Round 15 took their template half and registered R-0857 for it; that finding's fix clause ordered them deleted whole in this round rather than left reporting that an adapter which no longer exists is absent, and this round discharges it. With them goes step 6 of the seven-step operator path in `docs/system/core-product-spine-v0.md`, which is renumbered to six steps. The `worker` GROUP SURVIVES with its nine other commands, and `doctor core`, `mission run` and `mission report` are untouched — measured through the shipped readers, not assumed. THE INHERITOR IS F085, which owns `packages/orchestration/exec_guard.py`, the surviving bounded-subprocess guard that six modules already use, and F017, which owns the human approval gate. REMEDY DELIBERATELY SHIPS WITHOUT AN EXTERNAL-BUILDER ADAPTER after this commit, and therefore without any command that onboards, checks or disables an external worker: there is no stub, no shim, no alias and no compatibility reader, per AGENTS.md Scope Control. WHY THIS IS A SEPARATE ID FROM R-0856 AND FROM R-0857, searched for per §3 item 30 before it was minted: R-0856 names the `execution` surface, which is the RUNNER; R-0857 names the NARROWING of three commands and is RESOLVED by this round rather than duplicated by it; this id names the ADAPTER surface and the removal of those same three commands, which is a different behaviour with a different inheritor. WHAT WOULD RESOLVE IT: DECISION F260 D3 naming this id, the `builder` group, the three `worker` commands and the six actions among the ideas DELETED rather than inherited, naming F085 and F017 as above, and recording the deliberate absence where a reader would search for it — which for a deleted operator command is the core-product-spine page this round already edits. FIX CLAUSE, binding on the round that drafts DECISION F260 D3: that paragraph names all thirteen deleted command ids, the `builder` group, the six `ContractAction` members and this id, states F085 as the inheritor of bounded execution and F017 as the inheritor of human approval, and adds to `docs/system/core-product-spine-v0.md` the one-sentence deliberate-absence note AGENTS.md's Code Discoverability Conventions require — "Remedy deliberately ships no external-builder onboarding command because …" — because text search cannot find a command that does not exist, and the operator path this round shortened is exactly where a reader will look for it.
--- END-LEDGER16 ---


DONE WHEN — eight gates, every one EXECUTED with its real exit code recorded

G1 TRANSPORT. `.remedy-wt/f275-r16.md`, the committed `.agent/authored/f275-r16.md` and the
   committed `.agent/last_block.md` are byte-identical: same length, same sha256, all three
   printed. ONE digest comparison. This chain covers those three artefacts and claims nothing
   about any other bytes (§3 item 37).

G2 THE PLAN AND THE BLOCK. `.agent/plan.md` at C1 is byte-identical to the PLAN16 slice
   extracted from the COMMITTED C0a blob between its marker lines, markers excluded; print its
   length, sha256 and line count against the cap of 50; both mandated headings present.
   Re-measure and report the C0a blob's TOTAL line count against the cap of 490.

G3 THE RECORD, over TWO appends — `.agent/live_review.md` and `.agent/prose_slips.md` at C2:
   (a) BYTE READER: pre-length, post-length, growth == 1 + slice length; the pre-blob a
       byte-exact PREFIX of the post-blob; the slice a byte-exact SUFFIX; the joining byte read
       back out of the post-blob is `b'\n'`.
   (b) STRUCTURAL READER: your script COUNTS N from each slice — never a number this block
       asserts — and the LAST N blank-line units of the whole post-file equal the slice's N
       paragraphs IN ORDER, unit by unit, with a per-unit sha256 printed on both sides.
   (c) NEGATIVE CONTROL: flip one byte IN MEMORY inside the FIRST appended paragraph of each
       file (§3 item 36) and show that reader (a) and reader (b) BOTH reject the mutant and
       BOTH accept the truth. Re-read both files from disk afterwards and show them byte-equal
       to their committed post-blobs.
   (d) COUNT PATTERNS in the post-blob of `.agent/live_review.md`: `^Gate: ` rises by exactly
       1; `^Gate: F275 R15 `, `^Done: R-0855 — `, `^- R-0859 — ` and `^- R-0860 — ` are each
       exactly 1.
   (e) THE OPEN SET BY DISTINCT ID, `Landed:` lines never subtracted: report registered, done
       and open before and after. The reviewer measured 87 / 4 / 83 at the base, and this
       round registers two and resolves one.

G4 THE DELETION IS COMPLETE. `git ls-tree -r <C3>` holds none of the six whole-file removal
   paths; report the tracked-file total. Then sweep every tracked file outside `.agent/` and
   `.data/` for these tokens: `main_builder_adapter`, `main-builder-adapter`,
   `BUILDER_ADAPTER_`, `BUILDER_PACKAGE_CREATE`, `BUILDER_SESSION_`, each of the ten
   `builder.<sub>` command ids, `worker.doctor`, `worker.add`, `worker.disable`,
   `worker doctor`, `worker add`, `worker disable`, `get_builder_adapter_spec`,
   `save_builder_adapter_spec`, `BuilderAdapterSpec` and `BuilderAdapterMode`. PRINT THE RAW
   RESULT IN FULL, never truncated, then print the STRIPPED result — the same lines with every
   backtick-quoted span deleted before matching, per §3 item 20's R-0584 clause. THE BINDING
   CONDITION is that every STRIPPED line lies in `docs/roadmap/features/`, which is the round's
   declared scope ruling. Report what you measure and name any line that falls outside it.

G5 THE SHIPPED READERS, THE SECTION COMMENTS AND THE ORDER FILE, at the base `38e03d2f` and at
   C3. Read BY IMPORT, never by grep, with `sys.path` pinned and the resolved `__file__`
   PRINTED FIRST; take the base end inside a disposable worktree. Report at both ends:
   `len(_BASE_CATALOG)`, `len(collect_all_handlers())`, `len(GROUPS)`,
   `len(ALL_KNOWN_ACTIONS)` and the duplicate-id count. Show `builder` ABSENT from `GROUPS` at
   C3 and every `builder.` command id ABSENT from BOTH readers; show the `worker` GROUP still
   PRESENT with its nine surviving ids listed, and `worker.doctor`, `worker.add` and
   `worker.disable` ABSENT from both readers. Show `patch.approve`, `do.continue`,
   `mission.run`, `mission.report` and `doctor.core` PRESENT in both readers at C3. THEN THE
   REFERENTIAL CLOSURE R-0859 NAMES: resolve every `related=` entry in the catalog against the
   live ids at C3 and report the dangling set; it must be EXACTLY the two R-0859 registers —
   `dogfood.run-loop` and `readiness.show` — and must NOT contain `worker.doctor`. Count every
   `# ── ` section comment in `apps/cli/command_catalog.py` at both ends and report both
   numbers: exactly one must be gone. For the order file: print its component count at both
   ends, show its 26 header lines byte-identical with their sha256, and show the file EQUAL to
   a fresh regeneration from the live import graph. The reviewer measured 250 to 237, 250 to
   237, 48 to 47, 106 to 100, 0 duplicates at both ends, five components to four with NO
   survivor moving, and header sha256 `aff913e6…`.

G6 THE RED-PROOFS — four, all inside ONE disposable worktree checked out at C3, `__pycache__`
   purged before EVERY run, `python3 -B`, and each probe's UNMUTATED CONTROL run over that
   probe's OWN selection in the SAME script immediately before its mutation. After each probe
   restore the target with `git checkout -- <path>` and prove the restore by sha256 before and
   after; the worktree porcelain is empty at the end.
   A. Append `packages/orchestration/main_builder_adapter.py` back into
      `tests/orchestration/import_reachability_allowlist.txt`. Selection:
      `tests/orchestration/test_import_reachability.py`. Must go RED.
   B. Add `"packages.orchestration.main_builder_adapter",` back as the first entry of
      `CLUSTER_MODULES` in `tests/orchestration/test_cluster_deletion_map.py`. Selection: that
      same file. Must go RED.
   C. Insert the line `packages.orchestration.main_builder_adapter` immediately above
      `packages.orchestration.overnight_executor` in `.agent/f275_deletion_order.md`.
      Selection: `tests/orchestration/test_cluster_deletion_order.py`. Must go RED.
   D. In `apps/cli/commands/worker_facade_cmd.py`, delete the single line
      `    "doctor.core": _cmd_doctor_core,` — which occurs exactly once in that file at C3 —
      from `COMMAND_HANDLERS`. Selection: `tests/cli/test_worker_facade_cmd.py`. Must go RED.
      This probe exists because C3 REWRITES that file's assertions, and a rewritten assertion
      that no longer bites is the failure this gate is here to exclude.
   The reviewer ran all four against this change set: controls exit 0 at 3, 3, 3 and 37 passed;
   mutants exit 1 at 1, 1, 2 and 2 failures. Report your own numbers.

G7 RUFF, THE RATCHETS AND THE FULL SUITE.
   (a) `python3 -m ruff check` over every edited `.py` file that still exists at C3 — expect
       `All checks passed!` at exit 0.
   (b) `python3 -m ruff check .` repo-wide at the base inside a disposable worktree and at C3
       in the primary checkout. The GATE IS THE EQUALITY of the two diagnostic SETS, compared
       item by item, not the exit code: ruff exits 1 at both ends reporting a pre-existing 26.
       The reviewer's dry run needed TWO repairs to reach that equality — an unused
       `unittest.mock.patch` import and the blank line ruff's `I001` then wanted removed after
       `import pytest` — both of which the change set above already orders.
   (c) `python3 -B -m pytest` over `tests/orchestration/test_import_reachability.py`,
       `test_cluster_deletion_map.py`, `test_cluster_deletion_order.py`, `tests/docs/`,
       `tests/cli/test_advertised_commands.py`, `tests/cli/test_cli_ux.py`,
       `tests/cli/test_product_spine.py` and `tests/test_grouped_cli.py` — exit 0.
   (d) The canary `python3 -B -m pytest tests/cli/test_golden_path.py -q` — exit 0.
   (e) THE FULL SUITE, `python3 -B -m pytest tests/ -q`, SERIALLY, in the PRIMARY checkout,
       with C3 COMMITTED. BINDING: zero failed, and passed + skipped equals the C3 collection.
       The reviewer measured 18603 passed, 23 skipped, zero failed, against a collection of
       18626.
   (f) THE ARITHMETIC BY THE ID SET, both sides collected in the same environment: report the
       base id count, the C3 id count, the LOST set and the GAINED set with a per-file
       attribution of each. The reviewer measured 18712 at the base and 18626 at C3 — 86 lost
       and ZERO gained, attributed 51 to `tests/orchestration/test_main_builder_adapter.py`,
       14 to `tests/cli/test_worker_facade_cmd.py`, 10 to
       `tests/cli/test_main_builder_adapter_cli.py`, 8 to `tests/test_grouped_cli.py` — which
       parametrises over the catalog and is in no change set — 2 to
       `tests/cli/test_product_spine.py` and 1 to
       `tests/orchestration/test_development_artifact_boundary.py`.

G8 THE TREE. Re-read `.agent/STOP` from disk and report it ABSENT. `git status --porcelain`
   empty. `git worktree list` naming the primary checkout ALONE. Branch correct. Compare
   `git diff --name-only <C2>..<C3>` against this block's twenty-four C3 paths as a SET: report
   the missing set and the extra set, both of which must be EMPTY. For every commit BEFORE C4,
   report its parent count and its insertion count against the DECISION F104 D1 cap of 500.
   C4's own numbers belong to the next round's ledger entry and are not reported here (§3
   item 31).


HANDBACK

Rewrite `.agent/handoff.md` WHOLE at C4, per docs/agents/handback_template.md. It has no length
cap (amend0827 rule 3). It carries: SESSION 9 of F275, round 16; the range; a per-commit
changed-files table with the `+/-` column read from `git show --numstat` and compared cell by
cell against the Verification lines (§3 item 28); ONE LINE PER GATE with its real exit code;
the authored-text proofs table; every deviation, declared rather than repaired; the item-status
table; the open-findings count; and the next expected action. Push ONCE, after C4. Create no
PR, edit none, merge none.

Write no verdict, no `Done:` paragraph and no finding of your own. The only `Done:` text this
round applies is the reviewer-authored `Done: R-0855` paragraph inside the LEDGER16 slice.
