STEP T001 — F275 round 15 — delete the managed builder execution module group, the TENTH

Goal: book session 8's round 14 PASS, its prose slip and its drafted finding R-0855; register
the three findings this round's own deletion owes; sweep the survivor state R-0855 names; and
delete `packages/orchestration/managed_builder_execution` whole, with its handler, its
seventeen commands, the `execution` group, fourteen `ContractAction` members, two test files,
four documentation pages and the survivors that lose code.

This is a PRODUCTION round, not a deletion round under amend0906-triage-throughput: three
surviving files lose code — `apps/cli/commands/worker_facade_cmd.py`,
`packages/orchestration/exec_guard.py` and `apps/cli/commands/orchestrator_cmd.py` — so the
mutation red-proofs are ordered in full.

Base: `fadf4715`. Branch: `feature/f275-one-world-completion-part-three`. Session 9, round 15.

EVERY NUMERAL BELOW WAS MEASURED BY AN APPLIED DRY RUN, NOT DERIVED. The reviewer applied this
exact change set in a disposable worktree at `fadf4715`, ran the full suite serially to green,
ran all four red-proofs with matched controls, and split the result into the two production
commits ordered below. Where a number below disagrees with what you measure, REPORT THE
MEASUREMENT AND DO NOT ADJUST THE CHANGE SET.


BUNDLE — six commits, in this order

  C0a  save the authored block:  `shutil.copyfile` `.remedy-wt/f275-r15.md` to
       `.agent/authored/f275-r15.md`. Never retype it.
  C0b  mirror the same bytes:    `shutil.copyfile` the same source to `.agent/last_block.md`.
  C1   advance `.agent/plan.md`  — replaced WHOLE by the PLAN15 slice.
  C2   the record: append LEDGER15 to `.agent/live_review.md`, SLIPS15 to
       `.agent/prose_slips.md`, and DECISION15 to `.agent/decisions.md`.
  C3   sweep the survivor state finding R-0855 names — three paths.
  C4   delete the module group — thirty paths.
  C5   the handback: rewrite `.agent/handoff.md` whole.

C1 is the FIRST substantive commit and it advances the plan before the ledger commit, per §3
item 23. C2 registers R-0855 through R-0858 BEFORE C3 and C4 change anything they describe,
which is the ordering §3 item 20's R-0524 carve-out requires of a slice that states a fact
about this round's own landed change: DECISION15 and the R-0856 through R-0858 paragraphs
each name that ordering rather than a SHA that cannot exist when they are written.


THE CHANGE SET OF C3 — three paths, 3 insertions against 17 deletions

  apps/cli/commands/orchestrator_cmd.py                     0 / 3
      In `_cmd_orchestrator_decide`, delete the three lines `adv = data.get("advisor")`,
      `if adv:` and the `print` beneath them. Round 14 removed `"advisor"` from
      `export_decision_json`, so the branch can never fire.
  packages/orchestration/orchestrator_brain.py              0 / 13
      Delete the whole `# Local Model Advisor integration (Steps 1509-1511)` banner block,
      its explanatory paragraph, the closing rule line, `_CONFIDENCE_ORDER` and the blank
      lines that separated them. `_CONFIDENCE_ORDER` has exactly one occurrence repo-wide —
      its own definition — because round 14 deleted its only reader.
  tests/orchestration/test_cluster_deletion_map.py          3 / 1
      Replace the one-line comment above `CLUSTER_MODULES` with a comment that states NO
      count, per §3 item 16. The tuple shrinks once per group commit, so any numeral there
      is wrong from the next commit onward.


THE CHANGE SET OF C4 — thirty paths, 42 insertions against 4801 deletions

WHOLE-FILE REMOVALS, eight paths, by `git rm`:
  packages/orchestration/managed_builder_execution.py        0 / 1694
  apps/cli/commands/managed_builder_execution_cmd.py         0 / 350
  tests/orchestration/test_managed_builder_execution.py      0 / 1793
  tests/cli/test_managed_builder_execution_cli.py            0 / 95
  docs/system/managed-external-builder-execution-v1.md       0 / 177
  docs/system/managed-external-builder-execution-v1-1-hardening.md   0 / 88
  docs/guides/managed-external-builder-execution-user-guide-v1.md    0 / 79
  docs/system/controlled-claude-code-operator-path-v0.md     0 / 146

The last two are NOT in the map the round 14 handback carried; the reviewer's own token sweep
found them and read both pages. Each is entirely about the deleted feature: the user guide
documents `execution template-list/show/approve/run`, and the operator path's every numbered
step but two is an `execution` command. A page whose subject this commit deletes is deleted
with it — AGENTS.md Scope Control forbids the attic by name.

CATALOG AND CONTRACT:
  apps/cli/command_catalog.py                                0 / 197
      Delete the `"execution": GroupDef(...)` line, and the 196-line span that begins at the
      `# ── execution ─` section comment and ends at the last `CommandEntry` whose
      `group_id="execution"`. That span holds SEVENTEEN command entries; count them from the
      span rather than from this list, and report the number you counted.
  packages/orchestration/run_contract.py                     0 / 34
      Delete the fourteen `EXECUTION_*` members of `ContractAction`, their fourteen
      `ContractAction.EXECUTION_*` rows in `_DEFAULT_ALLOWED_ACTIONS`, the four-line
      `# Managed Builder Execution v1 (Step 2035)` comment above the members, and the two
      one-line comments `# v1.1: approval hardening read-only surfaces` and
      `# v1.2: operator path (Step 2506)`. `SELF_EXECUTION_STATUS` is NOT one of them and
      SURVIVES: it does not begin with `EXECUTION_`.
  apps/cli/commands/__init__.py                              1 / 2
      `managed_builder_execution_cmd` out of the import block and out of the `for mod in (…)`
      tuple.

SURVIVORS THAT LOSE CODE:
  apps/cli/commands/worker_facade_cmd.py                     3 / 54
      Delete `template_id` from all four entries of `_WORKER_ALIASES`. In `_cmd_worker_doctor`
      delete the `managed_builder_execution` import, the `template` local, the
      `template_exists` and `template_enabled` checks with their blockers, and the
      `"template_id"` key of `report`. In `_cmd_worker_add` delete the
      `managed_builder_execution` import, the `template` block, the `"template_id"` key, the
      `results["note"]` line and the `print` that renders it, and make `results["ready"]` read
      `results.get("adapter_enabled", False)` alone; the quickstart list loses its
      `execution approve` step and is RENUMBERED to four items, and `advanced` loses
      `template_id` and the two `execution` low-level commands. In `_cmd_worker_disable` delete
      the `managed_builder_execution` import, `template_ok`, and the `"template_disabled"` and
      `"template_id"` keys. THE ADAPTER HALF SURVIVES: `main_builder_adapter` is a LATER
      component of the order file and dies in a later round, so each of the three commands
      keeps its adapter behaviour and loses only its template behaviour.
  packages/orchestration/exec_guard.py                      24 / 19
      Seven docstring and comment citations of `managed_builder_execution` are PROSE that
      would dangle. The anchor moves into this surviving module and is stated ONCE. In
      `test_command_exec_policy` replace the sentence deferring to
      `managed_builder_execution._builder_exec_policy` with the reason itself, recovered from
      that function's own docstring before it is deleted, and mark it the one statement the
      others cite. In `dod_process_exec_policy`, `dod_app_exec_policy`,
      `runtime_build_exec_policy` and `runtime_server_exec_policy` replace the same deferral
      with a citation of `:func:`test_command_exec_policy``. In `run_guarded_test_command`
      replace the `_guarded_exit_code` citation with the translation it described. Above
      `FORBIDDEN_ENV_KEYS` drop the "same spelling and members as" clause: after this commit
      this is the ONE definition of the set. NO BEHAVIOUR CHANGES — every edit is inside a
      docstring or a comment, and the four `ExecGuardPolicy` constructions are untouched.

TESTS:
  tests/cli/test_worker_facade_cmd.py                        7 / 33
      Delete the `template_id` assertion from `test_claude_alias_fields`; delete the
      `_TMPL_PATCH`, `_ENABLE_TMPL` and `_DISABLE_TMPL` constants; drop the template `@patch`
      decorator, its parameter and its `return_value` from the four `TestWorkerDoctor` tests,
      from both `TestWorkerAdd` tests and from `TestWorkerDisable`; drop the
      `template_enabled`, `template_disabled` and `mock_enable_tmpl.assert_not_called()`
      assertions. RENAME `test_add_enables_both` to `test_add_enables_adapter` and
      `test_disable_both` to `test_disable_adapter`: each now exercises one half, and a name
      that counts two is the §3 item 16 defect in a node id.
  tests/cli/test_cli_ux.py                                   1 / 1
      Drop `"execution"` from the hardcoded `_INTERNAL_GROUPS` set at the top of the file.
  tests/orchestration/test_development_artifact_boundary.py  0 / 8
      Drop `"managed_builder_execution"` from `_PRODUCT_MODULES`, delete the whole
      `test_managed_builder_execution` method of `TestProductModulesNoLiveReview`, and drop
      the module from the tuple `test_worker_doctor_core_no_agent` iterates.
  tests/cli/test_product_spine.py                            0 / 5
      Delete `test_no_stale_adapter_flag_in_operator_path` whole. Its helper raises on a
      missing page by design, and the page it reads is deleted by this commit.
  tests/orchestration/test_cluster_deletion_map.py           0 / 2
      The `CLUSTER_MODULES` and `CLUSTER_COMMAND_HANDLERS` entries. C3 already fixed the
      comment above the tuple; do not touch it again here.
  tests/test_test_categories.py                              0 / 1
  tests/orchestration/import_reachability_allowlist.txt      0 / 2
  tests/orchestration/cluster_deletion_map.txt               0 / 1

PACKAGING, SCRIPTS AND THE ORDER FILE:
  pyproject.toml                                             0 / 1
  scripts/remedy_test_fast.sh                                0 / 1
  .agent/f275_deletion_order.md                              1 / 2
      REGENERATED from `measured_order()`, never typed. This file REORDERS as well as
      shrinking: six components fall to five AND `main_builder_adapter` moves from position
      four to position one, because deleting this module changes the graph's topological
      order. Keep the 26 header lines BYTE-VERBATIM and write the body as one component per
      line, comma-joined within a cycle, with NO leading indentation and a TRAILING NEWLINE.
      `_render` in `tests/orchestration/test_cluster_deletion_order.py` is the ASSERTION
      MESSAGE's formatter and indents by two spaces; it is NOT this file's format, and the
      reviewer's own first dry run used it and had to be corrected.

DOCUMENTATION:
  docs/README.md                                             0 / 5
      The rows linking the four deleted pages, matched on the LINK TARGET.
  docs/system/core-product-spine-v0.md                       0 / 1
      The `| `execution approve/run/show` | ... |` table row.
  docs/system/mission-run-loop-morning-report-v0.md          0 / 2
      The `See `docs/controlled-claude-code-operator-path-v0.md`` line and the
      `- Approving managed execution` bullet.
  docs/system/development-artifact-boundary-v0.md            2 / 4
      The `managed_builder_execution.py` bullet, the `Execution status` table row, and the
      guard-test sentence beneath the bullet, which still cites
      `test_execution_approval_policy.py` — a file round 12 deleted.
  docs/system/test-lanes-v0.md                               0 / 1
  docs/guides/simple-operator-quickstart-v0.md               3 / 3
      Three table cells lose their `execution template-*` half and keep their `builder
      adapter-*` half.

DELIBERATELY NOT TOUCHED, and this is the round's one scope ruling. Four roadmap files still
name a deleted token and none is edited. `docs/roadmap/features/T2_F085.md` and
`docs/roadmap/features/T2_F262.md` are `[x]` in `docs/roadmap/STATUS.md`: a closed feature file
is a historical record of what that feature built, and git is the archive.
`docs/roadmap/features/T2_F260.md` line 345 is the deletion LIST that authorises this work and
must stand until the list is discharged. `docs/roadmap/features/T2_F267.md` is `[ ]` — an
unstarted plan naming two commands this commit deletes — and that is registered as R-0858
rather than repaired, because editing another feature's plan is re-planning it.


CONSTRAINTS

 1. Apply every authored slice BYTE FOR BYTE. If a slice looks wrong, apply it as written and
    declare it in the handback. Never edit a slice.
 2. The change set above is EXHAUSTIVE. Touch no other path. If a gate demands a change to a
    path not listed, stop and declare it rather than widening.
 3. Each append is `post = pre + b"\n" + slice`. All three targets end with a newline; the
    joining byte is one `\n` and the slice carries no trailing newline of its own.
 4. `.agent/plan.md` is replaced WHOLE by PLAN15. PLAN15 is 44 lines against the AGENTS.md cap
    of 50 and carries `## Goal` and `## Next Steps`.
 5. Destructive verification runs ONLY inside a disposable `git worktree` under `.remedy-wt/`.
    The primary checkout satisfies `git status --porcelain` empty at the handback.
 6. Env-var assignment (`VAR=x cmd`, `env VAR=x`, `export`) and `cp` are DENIED by this
    sandbox. Copy with `python3 -c "import shutil; shutil.copyfile(a, b)"`. Capture real exit
    codes with `bash -c '<cmd>; echo "REAL_EXIT=$?"'` or from `subprocess.run`.
 7. The full suite is run SERIALLY in the PRIMARY checkout with the change COMMITTED. Under
    `-n auto` the `ui_server` command-channel tests race for a port. A fresh worktree has no
    `apps/ui/node_modules`, which is why the suite gate is not run in one.
 8. R-0855's FIX CLAUSE BINDS THIS BLOCK and this block discharges it in its own text: every
    definition ordered deleted above is accompanied by an order to sweep its callers, the
    constants left with no reader and the section comment above it. That is what the
    `exec_guard.py`, `run_contract.py` comment, `worker_facade_cmd.py` `template_id` and
    documentation orders are. No further sweep is owed and none may be invented.
 9. Report every number you measure even where it differs from a number above.
10. In the two change-set sections the runs of SPACES that align the `ins / del` column carry
    no meaning and are not appliable bytes: nothing in this block's frame reaches a file, the
    appliable bytes are the four marker-delimited slices alone, and each is proved against its
    own target by its own gate. G8 resolves each commit against the PATH SET rather than
    against any column position (§3 item 37).


AUTHORED SLICES

--- BEGIN-PLAN15 ---
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 15 books round 14's PASS and one prose slip, registers R-0855 through R-0858, records
DECISION F275 D7 on the approval gate, sweeps the survivor state R-0855 names, and deletes the
TENTH module group, `packages/orchestration/managed_builder_execution.py`, whole. This is a
PRODUCTION round: `worker_facade_cmd.py` loses the template half of three user-facing
commands, `exec_guard.py` loses seven prose citations of the dying module, `run_contract.py`
loses fourteen `ContractAction` members, and the catalog loses the `execution` group with
seventeen commands.

## Next Steps

1. The `main_builder_adapter` component, which this round's regeneration moves from position
   four to position one of the order file. It takes the adapter half of the three `worker`
   commands this round halved.
2. The remaining components in the recorded order — each a single module except the
   `provider_trust` / `provider_trust_verification` pair, which is the last cycle.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831,
   R-0840, R-0842, R-0844 through R-0846, R-0848, R-0849 and R-0851 through R-0857 named among
   the ideas deleted rather than inherited. That round also discharges R-0843's widened sweep.
4. T002, the atomic record flip, alone, because every later commit's size depends on its
   ruling.

## Risks

- The open set is 79 by distinct id at this round's base `fadf4715`; the ledger commit this
  block fixes as C2 registers four, taking it to 83. Four are High — R-0803, R-0804, R-0806
  and R-0807 — all F273's rather than this feature's, per DECISION F272 D12.
- Deleting `remedy execution approve` deletes a HUMAN approval command. DECISION F275 D7 rules
  that this leaves no ungated path because the executor it gates dies in the same commit, and
  records the measurement behind it rather than asserting it.
- The full suite is run SERIALLY: under `pytest -n auto` the `ui_server` command-channel tests
  race for a port, and the vitest node needs `apps/ui/node_modules`.
--- END-PLAN15 ---

--- BEGIN-SLIPS15 ---
2026-09-09 · F275 R14 · The reviewer's LEDGER14 slice recorded probe C's unmutated control as "470 passed" beside a mutated reading of 507; 470 was measured over a SIX-file selection while probe C runs over THREE, so the two numbers in that sentence come from different selections and are not comparable as written. The worker measured the matched control at 499 and declared the difference, and the reviewer re-measured 499 against 507 independently. Nothing is wrong on disk and the finding's conclusion is untouched, because it rests on the mutated reading alone: at exit 0 either way, an orphan `GroupDef` is invisible to every catalog guard. The lesson is that a control belongs to a SELECTION, not to a worktree, and a probe's control must be run over the probe's own selection in the same script that runs the probe.
--- END-SLIPS15 ---

--- BEGIN-DECISION15 ---
## DECISION F275 D7 — deleting `remedy execution approve` together with the executor it gates leaves no ungated path, so F275's Do-not-touch clause does not protect it (2026-09-09)

Ruled by the reviewer while authoring F275 round 15, under docs/agents/planner_reviewer_prompt.md §4 item 7, which routes a ruling to a loud, persisted, reversible decision rather than to a question the operator is never asked. Reverse it by deleting this section, which puts `remedy execution approve` back under the Do-not-touch clause and stops the cluster deletion at component line 1 of `.agent/f275_deletion_order.md`.

WHY THIS IS A SECOND DECISION AND NOT DECISION F275 D6. D6 ruled about `packages/orchestration/execution_approval_policy.py`, a prototype POLICY layer that could authorise an execution WITHOUT a human, and its whole argument was that the module is not a human gate. `remedy execution approve` IS a human gate: an operator types it, per session, and `remedy worker add` prints it as step 4 of its own quickstart beside the sentence "Execution still requires explicit approval per session." D6's reasoning therefore does not reach it, and reading D6 as covering it would be exactly the widening §3 item 34 warns against.

THE MEASUREMENT, taken at `fadf4715` and not assumed. Every caller of the four approval functions — `approve_managed_execution`, `get_execution_approval`, `list_execution_approvals` and `validate_execution_approval` — was resolved repo-wide by grep over every tracked `.py` file. All of them live in exactly three places: `packages/orchestration/managed_builder_execution.py` itself, its own handler `apps/cli/commands/managed_builder_execution_cmd.py`, and its own two test files. NOT ONE SURVIVING MODULE CALLS ANY OF THEM. The gate and the thing it gates are the same module, and this commit deletes both.

THE READING. A gate exists to stand between an actor and a capability. When the capability is removed in the same commit as the gate, there is no path left to gate: after this commit Remedy cannot launch a managed builder execution at all, by any route, approved or not. The change is therefore STRICTLY MORE CONSERVATIVE than the state before it, which is the same fail-safe direction D6 relied on. `packages/orchestration/exec_guard.py` SURVIVES and keeps its own six importers — `integrity_gate`, `ci_run`, `pingpong_loop`, `pingpong_promote`, `runtime_supervisor` and the dod seams — but none of those ever passed through `execution approve`; they call the guard directly and their posture is unchanged by this commit. F017's human gate is likewise untouched, and the round's own G5 gate proves it by import rather than by assertion: `patch.approve` and `do.continue` are PRESENT in both shipped readers after the deletion.

CHOSEN: `remedy execution approve` and the sixteen other `execution` commands are deleted with their module, their group, their tests and their four documentation pages, and F275's Do-not-touch clause is read — as D6 already read it — as protecting F017's human gate rather than any file that happens to contain the word "approve". The capability loss is registered as R-0856 in the same round rather than mitigated.

ALTERNATIVES CONSIDERED AND REJECTED. (a) Keep the `execution` group and delete only the module. Rejected: the seventeen handlers import the module at call time, so every one of them would exit with `ModuleNotFoundError` — a command advertised in `remedy --all-commands` that cannot run is worse than an absent one, and R-0847 already records that the advertised-commands guard is blind to exactly this shape. (b) Keep `execution approve` alone as a stub that refuses. Rejected by AGENTS.md Scope Control, which forbids a stub, a shim and a compatibility reader by name, and by the observation that a gate with nothing behind it is a false live indicator. (c) Stop the deletion and ask the operator. Rejected by §2 of the planner and reviewer prompt, which bars a ruling request, and by operator amendment amend0908-f275-finish rule 2, which permits an early stop only where a module group is genuinely undeletable under the three rules in `docs/roadmap/features/T2_F275.md` T001 — this one is not.
--- END-DECISION15 ---

--- BEGIN-LEDGER15 ---
Gate: F275 R14 — the F275 round 14 entry. VERDICT PASS, booked by round 15 rather than by a round of its own, per operator amendment amend0827-process-diet rule 1, and carried from the pushed `.agent/handoff.md` at `fadf4715`, which that rule makes a durable carrier. THE VERDICT WAS ISSUED BY THE PLANNER AND REVIEWER OF SESSION 8, which re-ran every one of the eight gates itself against the COMMITTED blobs over the range `16494bbd`..`5fb38765`; that session's own account is the handback text this entry books, and session 9 does not restate those readings as if it had taken them. Six single-parent commits C0a `490221e8`, C0b `dbffaba9`, C1 `11b4dff7`, C2 `ed9a78b0`, C3 `b3ddaa35` and C4 `5fb38765`, per-commit insertions 382, 346, 18, 10, 14 and 233, every one under the AGENTS.md DECISION F104 D1 cap of 500. G1 was the PRIMARY proof of §4 item 9 and not the digest fallback: the delegation source and both committed copies are 37397 bytes at `e8108d5345442dbf948921396afaf07dba35045ab51941fb0c318158e56b073d` and compare BYTE-EQUAL; per §3 item 37 that chain covers those three artefacts and claims nothing about the emitted bytes. G2: `.agent/plan.md` byte-identical to PLAN14 at 2720 bytes, 45 lines against the cap of 50, both mandated headings present. G3: `.agent/live_review.md` 608189 to 618783, growth 10594 = 1 + 10593; `.agent/prose_slips.md` 183299 to 184231, growth 932 = 1 + 931; N counted from each slice as 4 and 1, ordered equality over the WHOLE appended region with a per-unit sha256 on both sides, and BOTH negative controls flipped in the FIRST appended paragraph per §3 item 36 REJECTED by both readers; `^Gate: ` 35 to 36, and `^Gate: F275 R13 `, `^Note: F275 R14 `, `^- R-0853 — ` and `^- R-0854 — ` exactly 1 each; THE OPEN SET 77 TO 79 BY DISTINCT ID against registrations 81 to 83 and resolutions 4 to 4. G4: all five whole-file removals absent from `git ls-tree` at C3 over 4574 tracked files, and the sweep over 1690 tracked files outside `.agent/` and `.data/`, printed IN FULL with the four SURVIVING advisor tokens neutralised first, read exactly FOUR lines RAW and ONE with backtick-quoted spans stripped, which is the binding count and is the single `docs/system/vocabulary.md` line the round's scope ruling leaves to R-0843. G5: through the SHIPPED readers, by import with the resolved `__file__` printed, `_BASE_CATALOG` and `collect_all_handlers()` both fell 269 to 267, `GROUPS` 50 to 49 and `ALL_KNOWN_ACTIONS` 122 to 120, with zero duplicate ids, both deleted ids ABSENT from both readers, and `orchestrator.decide`, `orchestrator.inspect`, `orchestrator.report`, `provider.verify`, `patch.approve` and `do.continue` all PRESENT; `orchestrator.decide` args fell to `('--job-id', '--json')`; the exported decision key set fell from 20 keys to 19 with `advisor` gone; and the regenerated order file held SIX components against seven with its 26-line header sha256 unchanged at `aff913e6…`. G6: ALL FOUR RED-PROOFS WERE RE-RUN BY THE REVIEWER IN ITS OWN DISPOSABLE WORKTREE, each with its OWN matched control over its OWN selection — probe A control exit 0 at 3 passed against mutated exit 1; probe B control exit 0 at 6 passed against mutated exit 1 at 2 failed; probe C control exit 0 at 499 passed against mutated exit 0 at 507 passed; probe D control exit 0 at 61 passed against mutated exit 0 at 61 passed — every file restored byte-identically and proved by sha256. G7: ruff `All checks passed!` over the eight edited Python files still existing at C3 and repo-wide `Found 26 errors.` at both ends with the two diagnostic sets compared item by item and identical; the ratchets and canary 484 passed at exit 0; and THE FULL SUITE WAS RE-RUN BY THE REVIEWER SERIALLY IN THE PRIMARY CHECKOUT and was GREEN at 18844 passed, 23 skipped and ZERO failed, with 18844 + 23 = 18867 equal to the C3 collection against 18919 at the base, a fall of 52 with zero gained. G8: `.agent/STOP` absent, porcelain empty, ONE worktree, branch correct, and `ed9a78b0..b3ddaa35` naming the 24 paths in an EXACT SET MATCH. WHAT THE ROUND ACHIEVED: the NINTH module group, `local_model_advisor` at 947 module lines, in ONE commit at 14 insertions against 1845 deletions over 24 paths, taking its 101-line handler file whole, two commands, the `local-advisor` group, two test files, one doc page and two `ContractAction` members with it, and repairing seven surviving documentation pages. Unlike rounds 11 to 13 this was a PRODUCTION round: three survivors lost code and one loss changed an exported JSON contract. THE WORKER'S SIX DECLARED DEVIATIONS ARE ALL SUSTAINED, and the load-bearing one is the reviewer's own: the LEDGER14 text recorded probe C's unmutated control at "470 passed" beside a mutated 507, where 470 came from a SIX-file selection and the correctly matched control over probe C's THREE files is 499, which the reviewer re-measured independently at 499 against 507. The finding's conclusion is untouched because it rests on the mutated reading alone, so under amend0827-process-diet rule 2 that is a dated `.agent/prose_slips.md` line and not an id. NO FINDING IS RESOLVED BY THIS GATE, and the three artefacts the round's anchors left standing in its survivors are registered below as R-0855.

- R-0855 — Medium, ROUND 14's DELETION LEFT DEAD SURVIVOR STATE ITS ANCHORS DID NOT REACH, IN TWO FILES, AND ONE OF THE TWO IS A CODE PATH THAT READS A JSON KEY THE SAME ROUND REMOVED. Raised by the reviewer of session 8 at the round 14 gate, from the worker's declared deviation 4, and re-measured independently at `5fb38765` before this text was written. It is ONE id rather than two because the defect, the cause and the fix are one: an ordered anchor deleted a definition without sweeping the neighbourhood the definition served, and one sweep repairs both — which is exactly the counter-measure the resolved R-0841 and the open R-0843 already state and which that block failed to apply to its own orders. FIRST INSTANCE, `apps/cli/commands/orchestrator_cmd.py`, in `_cmd_orchestrator_decide`: the three lines `adv = data.get("advisor")`, `if adv:` and the print beneath them SURVIVE, while the same round removed `"advisor"` from `export_decision_json`, so `data.get("advisor")` is now always `None` and the branch can never fire. That is the attic AGENTS.md Scope Control forbids by name, and it is worse than ordinary dead code because a reader takes it as evidence that the exported key still exists. SECOND INSTANCE, `packages/orchestration/orchestrator_brain.py` lines 922 to 931: the ten-line section banner `# Local Model Advisor integration (Steps 1509-1511) — advisory ONLY.` and its explanatory paragraph describe an integration that round deleted, and the constant `_CONFIDENCE_ORDER` beneath it now has EXACTLY ONE occurrence repo-wide — its own definition — because its only reader was `_lower_confidence`, which the same commit removed. A THIRD INSTANCE WAS FOUND BY THE SAME SWEEP AND PREDATES THAT ROUND: `tests/orchestration/test_cluster_deletion_map.py` line 41 reads `# The twenty-four modules F260's Design lists as the prototype cluster.` above a `CLUSTER_MODULES` tuple that holds SEVEN, having shrunk once per group commit since round 7. It is named here rather than given an id of its own because the same sweep fixes it. WHY THIS IS AN ID AND NOT A PROSE SLIP: all three are wrong state on disk under `apps/`, `packages/` and `tests/`, which is precisely what amend0827-process-diet rule 2 reserves an R-id for, and the first instance is a live code path rather than a comment. NO GATE COULD SEE ANY OF THEM — ruff reports no error, the full suite is green, and the round 14 sweep could not fire because none of the three names a deleted symbol. WHAT WOULD RESOLVE IT: one commit deleting the three lines in `orchestrator_cmd.py`, the banner and `_CONFIDENCE_ORDER` in `orchestrator_brain.py`, and correcting the `CLUSTER_MODULES` comment to state no numeral at all per §3 item 16. FIX CLAUSE, BINDING ON EVERY REMAINING DELETION ROUND OF THIS FEATURE: a block that orders a definition deleted also orders the reader to sweep, in the same commit, for the callers of that definition, for the constants left with no reader, and for the section comment above it — and the block says so in its own text rather than leaving the worker to choose between an unordered edit and a declared deviation.

- R-0856 — Medium, THE WHOLE MANAGED EXTERNAL BUILDER EXECUTION SURFACE IS DELETED: SEVENTEEN COMMANDS, THE `execution` GROUP AND FOURTEEN RUN-PERMISSION ACTIONS, AND NO SURVIVING COMMAND REPLACES ANY OF THEM. Registered under operator RULE 3 of `docs/roadmap/features/T2_F275.md` T001, which requires a round removing a user-observable behaviour to name the behaviour and the feature that inherits the idea. THIS PARAGRAPH DESCRIBES THIS ROUND'S OWN LANDED CHANGE, so under §3 item 20's R-0524 carve-out it names no SHA — the commit it describes does not exist when it is written — and names instead the ordering its block fixes: the block's BUNDLE orders this registration as C2 and the deletion as C4, so every past-tense reading below is true from C4 onward and of no earlier commit. The behaviour: `execution.template-list`, `template-show`, `template-create`, `template-enable`, `template-disable`, `template-update`, `approve`, `run`, `show`, `list`, `debug-bundle`, `integrity`, `approval-show`, `approval-validate`, `approval-list`, `operator-runbook` and `claude-doctor` — the bounded managed runner for an external builder, its command-template registry, its per-session approval records with expiry and scope, its debug bundle, its operator runbook and its Claude readiness doctor. Fourteen `ContractAction` members go with them, so a run contract can no longer even NAME a managed execution as a permitted action. THE INHERITOR IS F085, which owns `packages/orchestration/exec_guard.py` — the surviving, shipped guard that six modules already use — and F017, which owns the human approval gate that `patch approve` and `do continue` still serve. REMEDY DELIBERATELY SHIPS WITHOUT A MANAGED EXTERNAL BUILDER RUNNER after this commit: there is no stub, no shim and no compatibility reader, per AGENTS.md Scope Control, and the deletion is fail-safe because it removes a capability rather than a restriction — DECISION F275 D7 records the measurement behind that reading. WHAT WOULD RESOLVE IT: DECISION F260 D3, the deletion paragraph, naming this id and the `execution` group among the ideas DELETED rather than inherited, and naming F085 and F017 as above. FIX CLAUSE, binding on the round that drafts DECISION F260 D3: that paragraph names all seventeen commands, the `execution` group and the fourteen `ContractAction` members among the deleted ideas, names F085 as the inheritor of bounded subprocess execution and F017 as the inheritor of human approval, and records that Remedy deliberately runs no external builder until a later feature provides one — the deliberate-absence note AGENTS.md's Code Discoverability Conventions require, written where a reader would search for the missing capability.

- R-0857 — Medium, THREE SURVIVING USER-FACING `worker` COMMANDS LOSE HALF THEIR BEHAVIOUR AND KEEP THEIR NAMES, AND NOTHING IN THEIR OUTPUT SAYS SO. `remedy worker doctor`, `remedy worker add` and `remedy worker disable` each paired an ADAPTER from `packages/orchestration/main_builder_adapter` with a TEMPLATE from the module this round deletes. LIKE R-0856 THIS PARAGRAPH DESCRIBES THIS ROUND'S OWN LANDED CHANGE and therefore names no SHA, per §3 item 20's R-0524 carve-out; the ordering it rests on is its block's BUNDLE, which fixes this registration at C2 and the deletion at C4, so "after this commit" below means C4 and nothing earlier. After this commit `worker doctor` no longer reports `template_exists` or `template_enabled`, `worker add` no longer enables a template, no longer returns `template_enabled`, and no longer prints the note "Execution still requires explicit approval per session" or the quickstart step naming `execution approve`, and `worker disable` no longer returns `template_disabled`. The commands still exist, still succeed, and still report `ready` — now on the adapter alone. THIS IS A DIFFERENT DEFECT FROM R-0856 AND WAS SEARCHED FOR SEPARATELY per §3 item 30: R-0856 is a group that DISAPPEARS, where absence is its own signal, while this is a surviving name whose meaning silently narrows, which is the harder failure to notice. It is registered rather than mitigated because the honest mitigation is the NEXT round: `main_builder_adapter` is component line one of the regenerated `.agent/f275_deletion_order.md`, so the adapter half dies too and all three commands become shells the round after this one, at which point they are deleted rather than narrowed. THE INHERITOR IS F275's own next round for the deletion, and F085 for any future readiness check over a bounded runner. WHAT WOULD RESOLVE IT: the round that deletes `main_builder_adapter` deleting these three commands, their catalog entries and their tests in the same commit, and DECISION F260 D3 naming this id. FIX CLAUSE, binding on the round that deletes `main_builder_adapter`: that round deletes `worker doctor`, `worker add` and `worker disable` WHOLE rather than leaving three commands whose only remaining behaviour is to report that an adapter which no longer exists is absent, and it names this id in its own finding text so the narrowing and the removal are one record.

- R-0858 — Low, AN UNSTARTED FEATURE'S PLAN NAMES TWO COMMANDS THIS ROUND DELETES, AND NOTHING WILL TELL THE SESSION THAT CLAIMS IT. `docs/roadmap/features/T2_F267.md` is `[ ]` in `docs/roadmap/STATUS.md` — "List commands v2 completion — sort/filter/limit for the remaining nine commands" — and its Goal names `execution.approval-list` as one of the nine commands it will wire to `apply_list_options`, while its "Why this exists" section names `execution.template-list` among the four DECISION F262 D4 excluded. Both are deleted by this round's C4, so the feature's scope is nine commands of which one cannot exist, and its own DONE condition is unreachable as written. MEASURED at `fadf4715` by reading the file and the ledger line: F262 is `[x]` and F267 is `[ ]`, which is what makes this an open plan rather than a historical record — the same reading spares `T2_F085.md` and `T2_F262.md`, whose identical-looking references are closed features' accounts of what they built. WHY THIS IS AN ID AND NOT A PROSE SLIP: `docs/roadmap/features/T2_F267.md` is wrong state on disk under `docs/`, which amend0827-process-diet rule 2 names, and the harm is real and dated — Rule A5 will one day propose F267, and the session that claims it will plan against a command that has not existed since this commit. WHY IT IS NOT REPAIRED HERE: editing another feature's Goal and scope is re-planning that feature, which AGENTS.md Scope Control forbids as a "while I'm here" edit and which this round's change set does not authorise. WHAT WOULD RESOLVE IT: one commit in the round that drafts DECISION F260 D3 — which is already editing roadmap files — striking `execution.approval-list` from F267's list of nine, restating the count as EIGHT or removing the numeral per §3 item 16, and dropping `execution.template-list` from the D4 exclusion sentence, with a one-line note naming this id and F275 as the feature that deleted them. FIX CLAUSE, binding on the round that drafts DECISION F260 D3: that round also performs the F267 repair above, because it is the only remaining round of this feature whose change set already contains `docs/roadmap/features/`, and a repair that waits for a round with no reason to open is a repair that does not happen.
--- END-LEDGER15 ---


DONE WHEN — eight gates, every one EXECUTED with its real exit code recorded

G1 TRANSPORT. `.remedy-wt/f275-r15.md`, the committed `.agent/authored/f275-r15.md` and the
   committed `.agent/last_block.md` are byte-identical: same length, same sha256, all three
   printed. ONE digest comparison, per the gate budget. This chain covers those three
   artefacts and claims nothing about any other bytes (§3 item 37).

G2 THE PLAN AND THE BLOCK. `.agent/plan.md` at C1 is byte-identical to the PLAN15 slice
   extracted from the COMMITTED C0a blob between its marker lines, markers excluded; print its
   length, sha256 and line count against the cap of 50; `## Goal` and `## Next Steps` both
   present. Re-measure the C0a blob's TOTAL line count and its PROSE line count (TOTAL minus
   the slice bodies) and report both.

G3 THE RECORD, over THREE appends. For `.agent/live_review.md`, `.agent/prose_slips.md` and
   `.agent/decisions.md` at C2:
   (a) BYTE READER: pre-length, post-length, growth == 1 + slice length; the pre-blob is a
       byte-exact PREFIX of the post-blob; the slice is a byte-exact SUFFIX; the joining byte
       read back out of the post-blob is `b'\n'`.
   (b) STRUCTURAL READER: your script COUNTS N from each slice — never a number this block
       asserts — and the LAST N blank-line units of the whole post-file equal the slice's N
       paragraphs IN ORDER, unit by unit, with a per-unit sha256 printed on both sides.
   (c) NEGATIVE CONTROL: flip one byte IN MEMORY inside the FIRST appended paragraph of each
       file (§3 item 36) and show that reader (a) and reader (b) BOTH reject the mutant and
       BOTH accept the truth. Re-read all three files from disk afterwards and show them
       byte-equal to their committed post-blobs.
   (d) COUNT PATTERNS in the post-blobs: `^Gate: ` rises by exactly 1; `^Gate: F275 R14 `,
       `^- R-0855 — `, `^- R-0856 — `, `^- R-0857 — `, `^- R-0858 — ` and
       `^## DECISION F275 D7 ` are each exactly 1.
   (e) THE OPEN SET BY DISTINCT ID, `Landed:` lines never subtracted: report registered, done
       and open before and after. The reviewer measured 83 / 4 / 79 at the base.

G4 THE DELETION IS COMPLETE. `git ls-tree -r <C4>` holds none of the eight whole-file removal
   paths; report the tracked-file total. Then sweep every tracked file outside `.agent/` and
   `.data/` for these tokens: `managed_builder_execution`, `managed-external-builder`,
   `EXECUTION_TEMPLATE_`, `EXECUTION_APPROV`, `EXECUTION_RUN`, `EXECUTION_SHOW`,
   `EXECUTION_DEBUG_BUNDLE`, `EXECUTION_OPERATOR_RUNBOOK`, `EXECUTION_CLAUDE_DOCTOR`, each of
   the seventeen `execution.<sub>` command ids, `execution approve`, `execution template-show`,
   `approve_managed_execution`, `get_execution_approval`, `list_execution_approvals`,
   `validate_execution_approval`, `get_command_template`, `enable_command_template` and
   `disable_command_template`. PRINT THE RAW RESULT IN FULL, never truncated, then print the
   STRIPPED result — the same lines with every backtick-quoted span deleted before matching,
   per §3 item 20's R-0584 clause. THE BINDING CONDITION is that every STRIPPED line lies in
   `docs/roadmap/features/`, which is the round's declared scope ruling above. The reviewer
   measured RAW 10 and STRIPPED 4, the stripped four being `T2_F262.md` twice, `T2_F267.md`
   once and one FALSE POSITIVE in `tests/cli/test_real_test_execution_cli.py` where the token
   `execution.list` matches inside `real_test_execution.list_test_runs`. Report what you
   measure and name any line that falls outside `docs/roadmap/features/` other than that one.

G5 THE SHIPPED READERS AND THE ORDER FILE, at the base `fadf4715` and at C4. Read BY IMPORT,
   never by grep, with `sys.path` pinned and the resolved `__file__` PRINTED FIRST so no
   editable install can shadow the reading; take the base end inside a disposable worktree.
   Report at both ends: `len(_BASE_CATALOG)`, `len(collect_all_handlers())`, `len(GROUPS)`,
   `len(ALL_KNOWN_ACTIONS)` and the duplicate-id count. Show `execution` ABSENT from `GROUPS`
   at C4 and every `execution.` command id ABSENT from BOTH readers. Show `patch.approve`,
   `do.continue`, `worker.doctor`, `worker.add`, `worker.disable`, `mission.run`, `doctor.core`
   and `builder.adapter-show` PRESENT in both readers at C4 — the human approval gate and the
   surviving worker facade. For the order file: print its component count at both ends, show
   its 26 header lines byte-identical at both ends with their sha256, show the file EQUAL to a
   fresh regeneration from the live import graph, and print the component list at C4 IN ORDER
   so the REORDER is visible. The reviewer measured 267 to 250, 267 to 250, 49 to 48, 120 to
   106, 0 duplicates at both ends, six components to five, and header sha256 `aff913e6…`.

G6 THE RED-PROOFS — four, all inside ONE disposable worktree checked out at C4, `__pycache__`
   purged before EVERY run, `python3 -B`, and each probe's UNMUTATED CONTROL run over that
   probe's OWN selection in the SAME script immediately before its mutation. After each probe
   restore the target with `git checkout -- <path>` and prove the restore by sha256 before and
   after; the worktree porcelain is empty at the end.
   A. Append `packages/orchestration/managed_builder_execution.py` back into
      `tests/orchestration/import_reachability_allowlist.txt`. Selection:
      `tests/orchestration/test_import_reachability.py`. Must go RED.
   B. Add `"packages.orchestration.managed_builder_execution",` back as the first entry of
      `CLUSTER_MODULES` in `tests/orchestration/test_cluster_deletion_map.py`. Selection:
      that same file. Must go RED.
   C. Insert the line `packages.orchestration.managed_builder_execution` immediately above
      `packages.orchestration.main_builder_adapter` in `.agent/f275_deletion_order.md`.
      Selection: `tests/orchestration/test_cluster_deletion_order.py`. Must go RED.
   D. In `apps/cli/commands/worker_facade_cmd.py`, replace the single line
      `    results["ready"] = results.get("adapter_enabled", False)` — which occurs exactly
      once in that file at C4 — with `    results["ready"] = False`. Selection:
      `tests/cli/test_worker_facade_cmd.py`. Must go RED. This probe exists because C4
      REWRITES that file's tests, and a rewritten assertion that no longer bites is the
      failure this gate is here to exclude.
   The reviewer ran all four at `fadf4715` plus this change set: controls exit 0 at 3, 3, 3 and
   51 passed; mutants exit 1 at 1, 1, 2 and 2 failures. Report your own numbers.

G7 RUFF, THE RATCHETS AND THE FULL SUITE.
   (a) `python3 -m ruff check` over every edited `.py` file that still exists at C4 — expect
       `All checks passed!` at exit 0.
   (b) `python3 -m ruff check .` repo-wide at the base inside a disposable worktree and at C4
       in the primary checkout. The GATE IS THE EQUALITY of the two diagnostic SETS, compared
       item by item, not the exit code: ruff exits 1 at both ends reporting a pre-existing 26.
       If your base reading differs from 26, check the worktree for your own scratch files
       before reporting it — that cost round 14 a retraction.
   (c) `python3 -B -m pytest` over `tests/orchestration/test_import_reachability.py`,
       `test_cluster_deletion_map.py`, `test_cluster_deletion_order.py`, `tests/docs/`,
       `tests/cli/test_advertised_commands.py`, `tests/cli/test_cli_ux.py`,
       `tests/cli/test_product_spine.py` and `tests/test_grouped_cli.py` — exit 0.
   (d) The canary `python3 -B -m pytest tests/cli/test_golden_path.py -q` — exit 0.
   (e) THE FULL SUITE, `python3 -B -m pytest tests/ -q`, SERIALLY, in the PRIMARY checkout,
       with C4 COMMITTED. BINDING: zero failed, and passed + skipped equals the C4 collection.
       The reviewer measured 18689 passed, 23 skipped, zero failed, against a collection of
       18712.
   (f) THE ARITHMETIC BY THE ID SET, both sides collected in the same environment: report the
       base id count, the C4 id count, the LOST set and the GAINED set with a per-file
       attribution of each. The reviewer measured 18867 at the base and 18712 at C4 — 157 lost
       and 2 GAINED, the two gained being `TestWorkerAdd::test_add_enables_adapter` and
       `TestWorkerDisable::test_disable_adapter`, which are the two renames C4 orders. A
       GAINED set is expected this round and is not a defect.

G8 THE TREE. Re-read `.agent/STOP` from disk and report it ABSENT. `git status --porcelain`
   empty. `git worktree list` naming the primary checkout ALONE. Branch correct. Compare
   `git diff --name-only <C2>..<C3>` against this block's three C3 paths and
   `git diff --name-only <C3>..<C4>` against its thirty C4 paths, each as a SET: report the
   missing set and the extra set, both of which must be EMPTY. For every commit BEFORE C5,
   report its parent count and its insertion count against the DECISION F104 D1 cap of 500.
   C5's own numbers belong to the next round's ledger entry and are not reported here (§3
   item 31).


HANDBACK

Rewrite `.agent/handoff.md` WHOLE at C5, per docs/agents/handback_template.md. It has no length
cap (amend0827 rule 3). It carries: SESSION 9 of F275, round 15; the range; a per-commit
changed-files table with the `+/-` column read from `git show --numstat` and compared cell by
cell against the Verification lines (§3 item 28); ONE LINE PER GATE with its real exit code;
the authored-text proofs table; every deviation, declared rather than repaired; the item-status
table; the open-findings count; and the next expected action. Push ONCE, after C5. Create no
PR, edit none, merge none.

Write no verdict, no `Done:` paragraph and no finding of your own. If a fix lands before the
reviewer has authored its resolution, write `Landed: R-XXXX — <one line>` and nothing else.
