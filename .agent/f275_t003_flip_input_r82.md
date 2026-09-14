# F275 T003 — the flip's input set: subtracted, re-keyed, re-checked

THIS ROUND PERFORMS NO FLIP. No production line moved; nothing under `packages/`, `apps/`,
`tests/`, `docs/` or `scripts/` was edited; no transform was executed; and no suite beyond
the canary was run. What follows is a measurement, and the set that measurement fixes on
disk for the flip round to re-derive.

The producer is `.agent/authored/f275-r82-input.py.md`, committed beside this file. It takes
the four trees, the two pinned JSON inputs from round 77, the two committed instruments and
a scratch directory AS ARGUMENTS and embeds no commit and no repository path, so the flip
round re-derives its input at ITS OWN base rather than inheriting a set measured here. It
prints no wall-clock value, and three runs of the committed blob agreed byte for byte.

THE RUN, VERBATIM. Every indented line below is a line of that generator's stdout, unedited.

 S0  THE PINNED INPUTS, BY BYTE COUNT AND DIGEST

     corrected set      r77_corrected.json                  120753 bytes  sha256 765b5ba99f2c92765349c3a013f4074c62ece893cb50b373450927af0290a512
     corrected owners   r77_corrected_owners.json           121095 bytes  sha256 670c6e952667b7c52b6c5a9ffd832dcc9f096aedfba114b83bc28ca061591b44
     re-key stage       rekey.py                              5186 bytes  sha256 f56394e9ac2582d5655a64a135fbf95b2930c24d14e791a23a2eb2630742a721
     owner check        owner_stage.py                       24253 bytes  sha256 7be3437450d1f183d241e8a5161a6ae182652d0aecd674ea10e8f870407eddb8

 S1  THE SUBTRACTION

     corrected set, ruled sites               : 2185
     corrected set, distinct tuples           : 2185
     owners map, keys                         : 2184
     ruled sites the owners map does NOT name : 1
         tests/orchestration/test_repair_loop_v1.py|56|28|id

     DROP tests/cli/test_repair_runtime.py|68|32|id
         occurrences in the corrected set : 1
         owner in the owners map          : Job
     DROP packages/orchestration/brain_detail.py|345|54|id
         occurrences in the corrected set : 1
         owner in the owners map          : Task

     after the subtraction, ruled sites        : 2183
     after the subtraction, owner keys         : 2182
     CROSS-CHECK sites removed                 : 2  exactly two: True
     CROSS-CHECK owner keys removed            : 2  exactly two: True
     CROSS-CHECK dropped sites that survive    : 0  none survives: True

     the canonical form is sorted(surviving set) rendered by json.dumps with
     separators=(",", ":"), encoded UTF-8
     canonical payload, bytes                  : 111904
     canonical payload, sha256                 : b347365ec9f7f17462c69a5c11c89d01fd3418fda350661fc2fa6e3545edbda4

 S2  THE RE-KEY AND ITS TWO CONTROLS

     paths under packages/, apps/ or tests/ that DIFFER between BASE and TIP : 0

     the re-key stage, BASE to TIP
     $ python3 -B rekey.py tree_base tree_tip r82_subtracted.json r82_subtracted_owners.json r82_rekey_tip.json
     ruled sites in R                     : 2183
     recovered by (scope, attr, occurrence): 2183
     CONTROL, recovered by (line, col, attr): 2183
     UNRESOLVED                            : 0
     owners carried across                 : 2182

     wrote .remedy-wt/r82/scratch/r82_rekey_tip.json and .remedy-wt/r82/scratch/r82_rekey_tip_owners.json
     REAL EXIT CODE = 0

     the re-key stage, BASE to SHIFT
     $ python3 -B rekey.py tree_base tree_shift r82_subtracted.json r82_subtracted_owners.json r82_rekey_shift.json
     ruled sites in R                     : 2183
     recovered by (scope, attr, occurrence): 2183
     CONTROL, recovered by (line, col, attr): 2174
     UNRESOLVED                            : 0
     owners carried across                 : 2182

     wrote .remedy-wt/r82/scratch/r82_rekey_shift.json and .remedy-wt/r82/scratch/r82_rekey_shift_owners.json
     REAL EXIT CODE = 0

     the re-key stage, BASE to DELETE
     $ python3 -B rekey.py tree_base tree_delete r82_subtracted.json r82_subtracted_owners.json r82_rekey_delete.json
     ruled sites in R                     : 2183
     recovered by (scope, attr, occurrence): 2183
     CONTROL, recovered by (line, col, attr): 2174
     UNRESOLVED                            : 0
     owners carried across                 : 2182

     wrote .remedy-wt/r82/scratch/r82_rekey_delete.json and .remedy-wt/r82/scratch/r82_rekey_delete_owners.json
     REAL EXIT CODE = 0

     CROSS-CHECK re-key BASE to TIP equals the subtracted set as a SET : True
     CROSS-CHECK re-key BASE to TIP equals the subtracted set IN ORDER : True

     the DELETE set against the TIP set, as sets
         sites in both                        : 2174
         in TIP and not in DELETE             : 9
             packages/orchestration/brain_detail.py|142|21|id
             packages/orchestration/brain_detail.py|293|17|name
             packages/orchestration/brain_detail.py|293|33|name
             packages/orchestration/brain_detail.py|293|54|name
             packages/orchestration/brain_detail.py|345|45|id
             packages/orchestration/brain_detail.py|350|11|description
             packages/orchestration/brain_detail.py|350|35|description
             packages/orchestration/brain_detail.py|350|65|description
             packages/orchestration/brain_detail.py|360|30|id
         in DELETE and not in TIP             : 9
             packages/orchestration/brain_detail.py|144|16|id
             packages/orchestration/brain_detail.py|292|17|name
             packages/orchestration/brain_detail.py|292|33|name
             packages/orchestration/brain_detail.py|292|54|name
             packages/orchestration/brain_detail.py|344|45|id
             packages/orchestration/brain_detail.py|349|11|description
             packages/orchestration/brain_detail.py|349|35|description
             packages/orchestration/brain_detail.py|349|65|description
             packages/orchestration/brain_detail.py|359|30|id

     the ruled sites of the mutated file, partitioned
         the mutated file                     : packages/orchestration/brain_detail.py
         its ruled sites in the set           : 9
         merely RE-LOCATED, statement text unchanged : 8
         RE-BOUND to a different statement           : 1
         CROSS-CHECK 8 + 1 = 9 against 9 : True
         RE-BOUND
             old coordinates at TIP           : 142:21 .id
             new coordinates at DELETE        : 144:16 .id
             old source line                  :     job_id_str = str(job.id)
             new source line                  :     node_map = {n.id: n for n in graph.nodes}
             owner carried across by the map  : Job

 S3  THE SHIPPED OWNER CHECK

     the owner check over the CORRECTED set at BASE, the BEFORE reading
     $ python3 -B owner_stage.py tree_base r77_corrected.json r77_corrected_owners.json
     ruled sites                 : 2185
     live record classes         : 71
        1908  CONFIRMED: the owner verdict matches the receiver's record
         107  REFUSED to decide: receiver's class not statically bound
         104  REFUSED to decide: annotation carries no class identity
          66  REFUSED to decide: receiver expression does not resolve
     DECIDED                     : 1908
     REFUSED, the stated blind spot: 277
     CONTRADICTED                : 0
     REAL EXIT CODE = 0

     the owner check over the re-keyed subtracted set at TIP
     $ python3 -B owner_stage.py tree_tip r82_rekey_tip.json r82_rekey_tip_owners.json
     ruled sites                 : 2183
     live record classes         : 71
        1908  CONFIRMED: the owner verdict matches the receiver's record
         106  REFUSED to decide: receiver's class not statically bound
         103  REFUSED to decide: annotation carries no class identity
          66  REFUSED to decide: receiver expression does not resolve
     DECIDED                     : 1908
     REFUSED, the stated blind spot: 275
     CONTRADICTED                : 0
     REAL EXIT CODE = 0

     the owner check over the re-keyed subtracted set at DELETE
     $ python3 -B owner_stage.py tree_delete r82_rekey_delete.json r82_rekey_delete_owners.json
     ruled sites                 : 2183
     live record classes         : 71
        1907  CONFIRMED: the owner verdict matches the receiver's record
         107  REFUSED to decide: receiver's class not statically bound
         103  REFUSED to decide: annotation carries no class identity
          66  REFUSED to decide: receiver expression does not resolve
     DECIDED                     : 1907
     REFUSED, the stated blind spot: 276
     CONTRADICTED                : 0
     REAL EXIT CODE = 0

 S4  THE SET BY FILE

     distinct files                            : 191
     ruled sites                               : 2183
     sites with attribute .description        : 39
     sites with attribute .id                 : 2100
     sites with attribute .name               : 44
     CROSS-CHECK the attribute counts sum to   : 2183  against 2183 : True

     one line per file, SORTED BY PATH
             8  apps/cli/commands/brain.py
             2  apps/cli/commands/context.py
            11  apps/cli/commands/do_cmd.py
            49  apps/cli/commands/job.py
             2  apps/cli/commands/loop_cmd.py
             3  apps/cli/commands/memory.py
             2  apps/cli/commands/patch.py
             2  apps/cli/commands/policy.py
             2  apps/cli/commands/project.py
             7  apps/cli/commands/repo.py
             3  apps/cli/commands/review_cmd.py
            11  packages/orchestration/agent_loop.py
             1  packages/orchestration/approval_queue.py
             2  packages/orchestration/autonomy_loop.py
             4  packages/orchestration/autonomy_readiness.py
            21  packages/orchestration/autorun.py
             9  packages/orchestration/brain_detail.py
             2  packages/orchestration/brain_viewer.py
            18  packages/orchestration/builder_bridge.py
             6  packages/orchestration/cockpit.py
             3  packages/orchestration/context_coverage.py
             2  packages/orchestration/context_inspector.py
             6  packages/orchestration/continue_from_node.py
             7  packages/orchestration/dag_schedule.py
             2  packages/orchestration/dashboard.py
             2  packages/orchestration/decision_queue.py
            20  packages/orchestration/do_run.py
             5  packages/orchestration/event_replay.py
             1  packages/orchestration/file_provenance.py
             1  packages/orchestration/flight_plan.py
             3  packages/orchestration/guidance.py
             8  packages/orchestration/job_fulfillment.py
             2  packages/orchestration/job_runner.py
             6  packages/orchestration/llm_planner.py
            20  packages/orchestration/long_run_executor.py
             1  packages/orchestration/loop_run.py
             2  packages/orchestration/memory_candidates.py
             1  packages/orchestration/memory_learn.py
             1  packages/orchestration/mission_readiness.py
             6  packages/orchestration/mission_state.py
             3  packages/orchestration/orchestrator_loop.py
             5  packages/orchestration/patch_apply.py
             4  packages/orchestration/patch_revert.py
            15  packages/orchestration/project_brain.py
             2  packages/orchestration/project_brain_aggregate.py
             1  packages/orchestration/project_context_coverage.py
             2  packages/orchestration/project_registry.py
             5  packages/orchestration/proof_chain.py
             2  packages/orchestration/proposed_tasks.py
             8  packages/orchestration/repair_loop.py
             3  packages/orchestration/reviewer.py
             2  packages/orchestration/run_contract.py
             1  packages/orchestration/self_dogfood.py
             1  packages/orchestration/source_context.py
             1  packages/orchestration/stop_reasons.py
             1  packages/orchestration/task_execution.py
            12  packages/orchestration/task_runner.py
            11  packages/orchestration/test_execution_service.py
             2  packages/orchestration/test_failure_artifact.py
             5  packages/orchestration/timeline.py
             1  packages/orchestration/token_economy.py
             1  packages/orchestration/token_policy.py
            19  packages/orchestration/trust_report.py
            45  packages/orchestration/ui_server.py
            24  packages/orchestration/ui_view_model.py
             3  packages/orchestration/verifier.py
             1  packages/orchestration/watchdog.py
             5  packages/orchestration/worker_queue.py
            12  tests/cli/test_change_proof_cli.py
            11  tests/cli/test_context_inspect_cli.py
             9  tests/cli/test_context_inspect_runtime.py
            25  tests/cli/test_decision_answers.py
             2  tests/cli/test_do_continue_cli.py
             3  tests/cli/test_file_provenance_cli.py
             2  tests/cli/test_golden_path.py
             8  tests/cli/test_job_commands.py
            15  tests/cli/test_job_context_cmd.py
            10  tests/cli/test_job_digest_cli.py
            25  tests/cli/test_job_report.py
             5  tests/cli/test_loop_cmd.py
            24  tests/cli/test_open_decisions_view.py
             3  tests/cli/test_orchestrator_brain_cli.py
            23  tests/cli/test_patch_cmd.py
             6  tests/cli/test_plan_approval.py
             4  tests/cli/test_product_spine.py
             1  tests/cli/test_real_test_execution_cli.py
             3  tests/cli/test_repair_request_cli.py
             3  tests/cli/test_repair_runtime.py
             6  tests/cli/test_repair_v1_cli.py
             1  tests/cli/test_scoped_listings.py
             3  tests/cli/test_self_dogfood_cli.py
             7  tests/cli/test_self_dogfood_execution_cli.py
            11  tests/orchestration/test_approval_queue.py
             6  tests/orchestration/test_autonomy.py
             2  tests/orchestration/test_autorun.py
             1  tests/orchestration/test_builder_bridge.py
             8  tests/orchestration/test_builder_repair_loop.py
             1  tests/orchestration/test_bundled_clarification.py
             1  tests/orchestration/test_change_set.py
            16  tests/orchestration/test_checkpoints.py
             3  tests/orchestration/test_context_inspector.py
            15  tests/orchestration/test_dag_schedule.py
             8  tests/orchestration/test_decision_inbox.py
            11  tests/orchestration/test_do_continue.py
            36  tests/orchestration/test_dod_gate.py
            38  tests/orchestration/test_escalation.py
             2  tests/orchestration/test_event_ledger.py
             2  tests/orchestration/test_f018_authority_integration.py
             3  tests/orchestration/test_fence_e2e.py
            21  tests/orchestration/test_fence_production_e2e.py
             2  tests/orchestration/test_flight_plan.py
             1  tests/orchestration/test_job_budgets.py
             4  tests/orchestration/test_job_digest.py
            44  tests/orchestration/test_job_fulfillment.py
            40  tests/orchestration/test_long_run_executor.py
            17  tests/orchestration/test_loop_run.py
             1  tests/orchestration/test_mission_e2e.py
            20  tests/orchestration/test_mission_readiness.py
            26  tests/orchestration/test_mission_state.py
            29  tests/orchestration/test_orchestrator_brain.py
            14  tests/orchestration/test_project_brain.py
             1  tests/orchestration/test_project_scope.py
            25  tests/orchestration/test_proof_chain.py
             2  tests/orchestration/test_proposed_tasks.py
             1  tests/orchestration/test_real_ollama_smoke.py
             1  tests/orchestration/test_real_test_execution.py
            10  tests/orchestration/test_repair_apply_cycle.py
             2  tests/orchestration/test_repair_loop_hardened.py
             7  tests/orchestration/test_repair_loop_v1.py
            29  tests/orchestration/test_repair_request_builder.py
            16  tests/orchestration/test_resume_cli.py
             2  tests/orchestration/test_run_contract.py
            14  tests/orchestration/test_run_report_hook.py
            13  tests/orchestration/test_self_dogfood.py
            27  tests/orchestration/test_self_dogfood_execution.py
            13  tests/orchestration/test_self_healing_cycles.py
             1  tests/orchestration/test_small_repo_fixtures.py
            15  tests/orchestration/test_source_apply.py
             2  tests/orchestration/test_source_context_quality.py
            30  tests/orchestration/test_structured_planner_cli.py
             4  tests/orchestration/test_task_execution.py
             8  tests/orchestration/test_test_execution_service.py
            49  tests/orchestration/test_test_failure_repair.py
             1  tests/orchestration/test_token_economy.py
             1  tests/orchestration/test_token_economy_integration.py
             7  tests/orchestration/test_watchdog.py
             1  tests/orchestration/test_worker_execution.py
             4  tests/storage/test_persistence.py
            47  tests/test_agent_loop.py
             8  tests/test_autonomy_readiness.py
            34  tests/test_brain_detail.py
            65  tests/test_brain_smoke.py
            49  tests/test_brain_viewer.py
             6  tests/test_cli_execution_loop_closure.py
            48  tests/test_cli_main.py
            44  tests/test_cockpit.py
            45  tests/test_context_coverage.py
             5  tests/test_execution_foundation.py
             5  tests/test_grouped_cli.py
             1  tests/test_imports.py
             4  tests/test_llm_planner.py
             4  tests/test_memory_learn.py
            28  tests/test_patch_apply.py
            50  tests/test_patch_intent_approval.py
            71  tests/test_project_brain.py
            18  tests/test_project_constitution.py
             8  tests/test_project_context_coverage.py
             1  tests/test_repair_context_reviewer_memory.py
             1  tests/test_run_contract.py
            87  tests/test_run_log_cli.py
             5  tests/test_runner.py
            10  tests/test_task_runner.py
             1  tests/test_test_runner.py
            71  tests/test_timeline.py
             1  tests/test_token_policy.py
            25  tests/test_trust_report.py
            46  tests/test_verifier.py
            20  tests/test_workspace.py
             1  tests/ui_contracts/test_graph_architecture.py
             6  tests/ui_contracts/test_responsive.py
            13  tests/ui_contracts/test_ux_quality.py
             1  tests/ui_server/test_auth_redaction.py
             5  tests/ui_server/test_brain_view_model.py
             4  tests/ui_server/test_command_channel.py
             7  tests/ui_server/test_command_dispatch.py
             3  tests/ui_server/test_dashboard_contract.py
             1  tests/ui_server/test_decisions_endpoint.py
             2  tests/ui_server/test_diff_endpoint.py
             1  tests/ui_server/test_digest_route.py
             1  tests/ui_server/test_live_state.py
             1  tests/ui_server/test_server_concurrency.py

## 1. The subtraction took only refused sites, and that is measured

The owner check was run over the corrected set at BASE and again over the subtracted set at
TIP. S3 reads DECIDED 1908 and REFUSED 277 over 2185 ruled sites in the first, and DECIDED
1908 and REFUSED 275 over 2183 in the second. The decided count is UNCHANGED and the refused
count falls by EXACTLY TWO, which is the number of sites removed. That is the reading of the
two runs: neither site DECISION F275 D55 named was one the check decided, both sat in the
refused blind spot, and no decided site left the input. CONTRADICTED is zero in both runs, so
the corrected set's zero-contradiction property survives the subtraction untouched.

The comparison is over the SET and not over the tree, because S2's first reading is that ZERO
paths under `packages/`, `apps/` or `tests/` differ between BASE and TIP — every path the
ruled set reaches carries the same bytes in both.

## 2. The re-key onto this TIP is an identity, and that is not a passing gate on its own

BASE to TIP recovers all 2183 sites by the scope key and all 2183 by the line-key control,
with nothing unresolved. That agreement is not evidence about the stage: no path under
`packages/`, `apps/` or `tests/` differs between the two trees, so there is nothing for a
key to survive and the stage's discriminating power is untested by this tree pair.

The SHIFT control is what tests it. With three blank lines inserted inside one module's
docstring the scope key still holds all 2183 while the line key falls to 2174, and
2183 − 2174 = 9, which is exactly the ruled-site count S2's partition prints for that file.
A control that separates the two keys is the reason the identity above can be read at all.

## 3. The DELETE control is the one that found something

The stage did NOT refuse. BASE to DELETE recovered all 2183 sites, UNRESOLVED 0, exit 0 —
the same banner the identity run prints. Its key is an occurrence index within an enclosing
scope, so removing a ruled statement does not make the key unresolvable; it makes the NEXT
attribute of that name in that scope answer to it, and the owners map carries the old verdict
onto whatever now answers.

One of the nine sites is that shape. The site at `packages/orchestration/brain_detail.py`
142 column 21 re-binds to 144 column 16: the old source line is `    job_id_str = str(job.id)`
and the new one is `    node_map = {n.id: n for n in graph.nodes}`, with the owner `Job`
carried across. The receiver is read rather than assumed: `graph.nodes` resolves to the
`nodes` field of `ProjectBrainGraph`, annotated `tuple[BrainNode, ...]` at
`packages/orchestration/project_brain.py` line 257, so the re-bound site's receiver is a
`BrainNode` while the owner carried across is `Job`. The other eight sites of that file
merely re-locate by one line and their statement text is unchanged.

## 4. This is `R-0880`'s defect reached by a second route, not a new one

`R-0880` already names `BrainNode` among the receivers this set mis-owns, so the open set was
searched for the DEFECT before any id was considered and the search returned `R-0880` itself.
NO NEW ID IS MINTED. Its second obligation — that the transform refuses a site whose owner
verdict cannot be CONFIRMED — would stop this run too, and that is measured rather than
reasoned to: the owner check over the DELETE set reads 1907 CONFIRMED against 1908 at TIP
and 276 REFUSED against 275, so the re-bound site moved out of CONFIRMED and into the refused
blind spot. A fix for `R-0880` fixes this instance.

## 5. What is not claimed

The two pinned JSON inputs are round 77's and live in gitignored scratch. This round makes the
SUBTRACTION and the RE-KEY reproducible from committed bytes; it does NOT make the corrected
set itself reproducible from committed bytes, which needs the round 53 probe run and is not
this round's work.

The DELETE control is a SYNTHETIC mutation. No commit of this branch has yet removed a ruled
statement, and this artefact reports what would happen if one did — not something that has
happened. The set by file in S4 is the subtracted set at TIP and nothing has been flipped.
