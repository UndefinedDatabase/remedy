# Structure ledger v1: what is large may only shrink

> Status (F300, 2026-10-09): built. DECISIONs F300 D1 and D2 in `.agent/decisions.md` hold the
> rules this page states; the feature is `docs/roadmap/features/T2_F300.md`.

Remedy's program code holds functions and files that grew far past the size a person can read in
one sitting. This page is the ledger of those debts: each one with its measured size, and for the
largest the boundary it should be cut along and the steps in order. A test holds every size on
this page, so a debt can shrink and can never grow, and no new one can appear.

## The measure
`remedy integrity structure` measures a repository: every Python function from its `def` line to
its last line, read from Python's own syntax tree, and every tracked text file by its lines. It
names a function longer than 100 lines and a file longer than 1,000 lines, largest first, and
changes nothing. The two limits are options of the command; for Remedy they are fixed at 100 and
1,000. Remedy's ledger covers the files git tracks under `packages/`, `apps/` and `scripts/`.

## The ratchet
`tests/test_structure_ratchet.py` measures that scope and reads the two tables at the end of this
page. Each row must equal its measure exactly:

- A function or file that grew past its row fails the test. Cut it back; never raise the row.
- A new function or file above its limit fails the test, because it has no row. Cut it below the
  limit.
- A function or file that shrank fails the test until the same commit lowers its row, so the
  record always says what the code is. One that fell to its limit or below, or no longer exists,
  loses its row in the same commit.
- The number of rows of each table and the sum of their lines are pinned in the test and may only
  fall. A row may be renamed when a structural step moves a function to another module or gives
  it another name, because its count and its lines stay; a row is added only by the DECISION that
  the rule below requires.

## The rule
The rule that pays these debts down, one structural step at every rolling findings paydown, and
what a feature owes when it touches a function on this page, is written once, in the section "The
structure rule" of `docs/agents/self_drive_protocol.md`.

## Boundaries and steps
Every function longer than 300 lines and every file longer than 2,000 lines has its boundary here.
Every other row gets its boundary when a feature first touches it or a paydown takes it. Every
step changes no behaviour, re-points every consumer of a moved name to its new home in the same
commit with no alias left behind, and changes the tests in their import lines only.

### Functions
- `run_job` (`packages/orchestration/pingpong_job.py`). Boundary: its own phases — the pre-flight
  guards, the configuration it resolves for the job, the budget accumulators and their nested
  helpers, the episode start, and the main loop over the tasks with the job's terminal steps after
  it; and the stop, pause and budget check that each of its safe points once wrote out. Steps: (1)
  done by F300 T004, every safe point calls `_settle_safe_point`; (2) done by F306, the
  configuration resolution is `resolve_job_execution_config` in
  `packages/orchestration/execution_config.py`, which `pingpong_job.py` re-exports; (3) the
  terminal steps after the task loop become a function of their own; (4) the handling of one
  task's result becomes a function of its own; (5) the budget helpers become one object in a
  module of their own, holding the accumulators. Outside those steps, F308 moved the split of a
  task whose context exceeds its class cap to `split_task_over_class_cap` in
  `packages/orchestration/run_task_list.py`.
- `run_pingpong` (`packages/orchestration/pingpong_loop.py`). Boundary: the builder, test and
  reviewer phases its own banners name, and the target snapshot check written out four times.
  Steps: (1) the snapshot check becomes one function each place calls, each keeping its own exit
  from the loop; (2) the two retries without a resumed session become one function; (3) the
  builder's and the reviewer's prompt composition become a function each; (4) the closing record
  of the run becomes a function of its own. Step (5), done by F141: the builder's context,
  `build_builder_context` in `packages/orchestration/builder_context.py`. Step (6), done by F307:
  the construction of the two role providers is one block whose two calls share their options.
- `list_decisions` (`packages/orchestration/decision_queue.py`). Boundary: its nine numbered
  sections, one per source of decisions. Steps: (1) the three largest sections — plan approvals,
  escalations and budget stops — become a function each that returns its decisions; (2) the other
  six follow, in a module of their own, with the order of the sections kept.
- `export_job_evidence` (`packages/orchestration/job_evidence.py`). Boundary: the per-task loop of
  independent writes, the review subject, and the ordered chain of gates. Steps: (1) one task's
  evidence becomes a function of its own; (2) the review subject becomes a function of its own;
  (3) the gate chain becomes a function of its own, in exactly its present order.
- `_RemedyHandler._handle_command_submission` (`packages/orchestration/serve_http_handler.py`). Boundary:
  the chain of command clauses after the shared checks, each repeating the same accept, refuse
  and fail tail. Steps: (1) the shared tail becomes one method, taken by one clause at a time;
  (2) the chain becomes a table from command to its handler; the clauses with a shape of their own
  keep their status codes and audit words.
- `_cmd_decision_resolve` (`apps/cli/commands/decision.py`). Boundary: the one branch per kind of
  decision id. Steps: (1) each branch becomes a function of its own that returns the exit code;
  (2) the command keeps only the dispatch, in the present order of its tests.
  Step (1) for the budget branch, done by F310: `_resolve_budget_decision`.
- `run_cycles` (`packages/orchestration/long_run_executor.py`). Boundary: the numbered steps its
  own comments give, and the resume of a parked job before the loop. Steps: (1) the resume becomes
  a function; (2) one batch of tasks becomes a function; (3) the decision by the job's shape
  becomes a function.
- `run_mission` (`packages/orchestration/orchestrator_loop.py`). Boundary: the safe point of each
  iteration, the context it assembles, the call and its refusals, and the two streak counters.
  Steps: (1) the two streak counters become functions that answer an escalation or nothing;
  (2) the context assembly becomes a function; (3) the safe point becomes a function.
- `doctor_core_report` (`apps/cli/commands/worker_facade_cmd.py`). Boundary: its five banner
  sections. Steps: (1) the three nested helpers for dead model ids move to the module; (2) each
  section becomes a function of its own, keeping the order of the checks it appends. Step (1),
  done by F307: `_dead_origin`, `_dead_provenance_short` and `_dead_provenance`, which take the
  shipped entries as an argument.
- `_apply_from_workspace` (`packages/orchestration/job_apply.py`). Boundary: its banner phases —
  validation, refusals, the durable record before any write, the write, then verify, test, commit
  and push. Steps: (1) the steps after the write become a function each; (2) the validation phase
  becomes a function that answers the plan; both refusal checks stay where they are.
- `build_manifest_from_snapshot` (`scripts/build_review_manifest.py`). Boundary: no phase seam;
  the most mechanical cut is the large manifest literal and the package status it derives. Steps:
  (1) the manifest literal becomes a function; (2) the package status becomes a function, with its
  keys and words unchanged.
- `summarize_trust_report` (`packages/orchestration/trust_report.py`). Boundary: its ten numbered
  sections. Steps: (1) each section becomes a function that answers its lines, the patch intents
  and the artifacts first.
- `_build_dashboard` (`packages/orchestration/serve_http_handler.py`). Boundary: its commented sections that
  feed one answer. Steps: (1) the task list and the activity become a function each; (2) the
  lifecycle and the phases become a function; the proof chain is built once and passed in.
- `main` (`scripts/build_review_zip.py`). Boundary: the three phases its comments name and the one
  publication. Steps: (1) the publication becomes a function, fed only the verified bytes; (2) the
  build with evidence becomes a function, one sub-step per phase.
- `execute_test_run` (`packages/orchestration/test_execution_service.py`). Boundary: its numbered
  gates. Steps: (1) the discovery of a safe test command becomes a function; (2) the admission
  gates before it become a function; the lease and its release stay where they are.
- `_collect_calls` (`packages/orchestration/run_manifest.py`). Boundary: the three parts of its
  per-task loop — the task without a run, the lineage and membership check of each entry, and the
  expectation check. Steps: (1) the check of one entry becomes a function, lineage still first;
  (2) the task without a run becomes a function. Step (2), done by F308: the task without a run is
  `expect_task_without_run` in `packages/orchestration/run_task_list.py`.
- `execute_move` (`packages/orchestration/orchestrator_loop.py`). Boundary: one branch per kind
  of move, the dispatch branch holding most of its lines. Steps: (1) done by F301, the dispatch
  branch is `dispatch_milestone_job` in `packages/orchestration/orchestrator_dispatch.py`, which
  reads the loop's helpers from the loop's module, and the function left the table.
- `build_client_digest` (`packages/orchestration/client_digest.py`). Boundary: one entry per
  kind it builds — a project, a job, a decision — and the window over the ended jobs. Steps:
  (1) done by F205, one job's entry is `_job_entry`; (2) done by amend1015c, the reading of
  each project's missions and ledgers is `_read_projects`, and the listing of its plans is
  `_listed_plans`; (3) done by amend1015c, the window over the ended jobs is
  `_ended_job_window`.
- `plan_order_job` (`packages/orchestration/do_sequence.py`). Boundary: the intake call, the
  first-pass task plan with its approval, the record a plan that cannot be parsed leaves, and the
  deterministic plan. Steps: (1) done by F297, the record of a plan that cannot be parsed is
  `_record_unparsed_plan`; (2) done by F312, the first-pass task plan with its approval is
  `_first_pass_task_plan`; (3) the deterministic plan becomes a function.
- `continue_from_node` (`packages/orchestration/continue_from_node.py`). Boundary: the checks of
  the parent and the node, the child job's record, the link to the project, and the two timeline
  events. Steps: (1) done by F203, the link to the project is `_link_child_to_project`; (2) the
  two timeline events become one function.
- `validate_run_manifest` (`packages/orchestration/run_manifest.py`). Boundary: the declared task
  list every call is bound to, the loop over the calls, the coverage, the ledgers and the
  expectation, the episode order fields, and the embedded snapshot with the stop request. Steps:
  (1) done by F308, the declared task list is read by `declared_job_input_task_ids` in
  `packages/orchestration/run_task_list.py`; (2) the checks of one call become a function of their
  own; (3) the episode order fields become a function of their own; (4) the embedded snapshot's
  checks become a function of their own.
- `_cmd_do_order` (`apps/cli/commands/do_cmd.py`). Boundary: the checks of its arguments, the
  budgets it resolves before the walk, the context it builds and walks, and the answer it gives,
  the JSON document or the text lines. Steps: (1) the budgets resolved before the walk become a
  function of their own; (2) the context the walk carries is built by a function of its own; (3)
  the answer becomes a function of its own, once the client-interface tests, which key the
  answer's sites by this function, read them through the function that gives them. Until a step
  is taken, a feature's edits of this function are line-neutral (DECISION F055 D1).
- `_cmd_do` (`apps/cli/commands/do_cmd.py`). Boundary: the order read before any step, the
  refusals before any step (the rehearsal's conflicting flags, the commit and push flags, the
  planner, the contract template, and an order file a mission still runs) and the one call into
  `_cmd_do_order`. Steps: (1) the refusals before any step become one function that exits 2 or
  returns; (2) the call stays.
- `_cmd_job_run` (`apps/cli/commands/do_cmd.py`). Boundary: the checks of its flags, the budgets
  it resolves from them, the refusals before anything runs (a job that cannot be continued, a
  cancelled job, a plan not approved), the forward to a supervisor that answers, the run, and its
  answer. Steps: (1) the refusals before anything runs become one function that fails or returns;
  (2) the budgets resolved from the flags become a function of their own; (3) the answer becomes a
  function of its own, once the client-interface tests, which key the answer's sites by this
  function, read them through the function that gives them. Until a step is taken, a feature's
  edits of this function are line-neutral (DECISION F055 D3). Step (1), done by F307: the
  refusals, `refuse_job_run_before_it_starts` in `apps/cli/commands/job_run_refusals.py`.
- `_cmd_status` (`apps/cli/commands/status_cmd.py`). Boundary: the scope and project it reads,
  the jobs grouped by state, the counts of open decisions and pending stops, the runtime's state,
  and its answer, the JSON document or the text lines. Steps: (1) the counts of open decisions and
  pending stops become a function each; (2) the runtime's state becomes a function of its own;
  (3) the text lines become a function of their own. Until a step is taken, a feature's edits of
  this function are line-neutral (DECISION F055 D3).
  Step (3), done by F078: the text lines, `_print_status_text` in the same file.
- `decode_persisted_budget_actuals` (`packages/orchestration/budget_guard.py`). Boundary: the
  closed field set and its version, the counts and how they agree, the sources, the start instant
  and its agreement with the job's first run, and the money and clock fields of the versions that
  carry them. Steps: (1) done by F310, the start instant's checks are
  `decode_persisted_started_at` in `packages/orchestration/budget_clock.py`; (2) the counts and the
  sources become a function of their own.

### Files
Each step moves a cluster into a new module and re-exports its names by name from the old one, so
every import path keeps working; a name a test replaces on the old module stays there together
with the code that calls it.

- `packages/orchestration/run_manifest.py`: the workspace identity and its probes, then the
  storage — the write, the recovery and the anchored read — each to a module of its own; the
  decoders last. Step (1), done by F306: the probes and the workspace identity record,
  `packages/orchestration/workspace_identity.py`; the git reads, including the verified read of
  untracked files, stay on this module, because tests replace them there and
  `_read_untracked_verified` raises this module's own `ManifestError`. Step (2), done by F306: the
  job-input definition's builder and its field-set constants,
  `packages/orchestration/job_input_definition.py`; its validation (`validate_job_input_definition`)
  and its decoder (`decode_job_input_definition_v1`) stay on this module, because the validator
  calls shared helpers — `_is_hex64`, `_safe_component`, `VALID_ISOLATION_MODES`,
  `_contains_secret` and `_contains_local_path` — that every other validator on this module uses
  too, and two of which tests replace directly here. Outside those steps, F308 moved the reading
  of the declared task list, its check across a job's episodes and the expectation of a task
  without a run to `packages/orchestration/run_task_list.py`.
- `packages/orchestration/pingpong_job.py`: the job model and its store, the job report, and the
  stop and park path, each to a module of its own; `run_job` stays. Step (1), done by F306: the
  execution configuration and its two serializers, `packages/orchestration/execution_config.py`.
  Step (2), done by F307: the job report, `packages/orchestration/job_report.py`.
  Outside those steps, F308 moved the split of a task whose context exceeds its class cap to
  `split_task_over_class_cap` in `packages/orchestration/run_task_list.py`.
- `packages/orchestration/pingpong_loop.py`: the construction of a role's provider, the provider
  call with its retry and its booking, the context pack and the prompt builders, the staging, diff
  and target guard, and the export and token accounting, each to a module of its own. Step (1),
  done by F058: the construction of a role's provider,
  `packages/orchestration/role_provider_factory.py`. Step (2), done by F058, the first part of the
  export: a call's own fields and the reader of a parked run's sessions,
  `packages/orchestration/pingpong_call_record.py`. Step (3), done by F307: the provider call —
  `ProviderAttempt`, the two stream hints, the attempt booking, the rate-limit wait and
  `_call_with_retry` — `packages/orchestration/pingpong_provider_call.py`; the failure status,
  the call identity and the post-mortem stay, beside the run that calls them.
- `packages/orchestration/serve_http_handler.py`: the command channel's checks, each to a module of its
  own. The event stream, the dashboard builders, the launch helpers and the frontend's automatic
  build with its T20 ignore were deleted with the old cockpit (amend1015f D19 and D3), and F307
  renamed the file from `ui_server.py` for what it serves (R-1330).
- `scripts/build_review_manifest.py`: the gate schemas and the verification-tests check, the
  evidence view, and the manual-completion check, each to a module under `packages/`.
- `apps/cli/command_catalog.py`: the types and the argument shorthands to
  `apps/cli/command_catalog_types.py`, then the catalog's data one contiguous group at a time, each
  to a module of its own that `_BASE_CATALOG` splices in at the group's own place, so the help keeps
  its order; the lookups stay. Step (1), done by F301: the types, the shorthands and the `mission`
  group, `apps/cli/command_catalog_mission.py`. Step (2), done by F302: the `stats` group,
  `apps/cli/command_catalog_stats.py`. Step (3), done by F206: the `project` group,
  `apps/cli/command_catalog_project.py`. Step (4), done by F199: the `doctor` group,
  `apps/cli/command_catalog_doctor.py`. Step (5), done by F055: the `do` group,
  `apps/cli/command_catalog_do.py`. Step (6), done by amend1015f: the `client` group,
  `apps/cli/command_catalog_client.py`. Step (7), done by F307: the `job run` entry,
  `apps/cli/command_catalog_job_run.py`.
- `packages/orchestration/job_evidence.py`: the manual-completion bundle, the verification runner,
  and the run-manifest cross-checks with the postmortems, each to a module of its own.
- `packages/orchestration/job_apply.py`: the result model, the history, commit and push policy,
  and the export and summary, each to a module of its own.
- `apps/cli/commands/job.py`: the budget commands, then the sections of `remedy job show`, each to
  a module of its own.
- `packages/orchestration/orchestrator_loop.py`: the protocol, context and milestones, the ledger,
  and the evaluation of a move, each to a module of its own, the shared constants first.
- `scripts/remedy_smoke.sh`: the long block of surface checks and the patch lifecycle, each to a
  file sourced in place, after the tests that read the script's text are pointed at both.
- `packages/runtimes/dev_server.py`: the spec, paths and lock, the ports and the probe, and the
  shutdown of a process tree, each to a module of its own. Step (1), done by F306: the ports and
  the readiness probe, `packages/runtimes/dev_server_ports.py`.
- `packages/orchestration/pingpong_provider.py`: the claude CLI's command line, the output
  contracts, the parsing of the reviewer's answer, the fake provider and the Ollama provider, each
  to a module of its own. Step (1), done by F302: the claude CLI's command line,
  `packages/orchestration/claude_cli_command.py`. Step (2), done by F307: the Ollama provider,
  `packages/orchestration/pingpong_provider_ollama.py`, which `create_provider` imports when it
  builds one. Step (3), done by F307: the fake provider,
  `packages/orchestration/pingpong_provider_fake.py`.
- `packages/orchestration/config.py`: `ConfigKeySpec` to `packages/orchestration/config_key_spec.py`,
  then the key registry one contiguous group at a time, each to a module of its own that
  `_CONFIG_KEY_SPECS` splices in at the group's own place, so the registry and the environment guide
  keep their order; the loader, the resolver and the writer stay. Step (1), done by F301:
  `ConfigKeySpec` and the mission orchestrator's keys, `packages/orchestration/config_keys_mission.py`.
  Step (2), done by F302: the Claude CLI planner's keys, `packages/orchestration/config_keys_claude.py`.
  Step (3), done by F058: the model routing keys, `packages/orchestration/config_keys_model_routing.py`.
  Step (4), done by F058 (finding R-1264): the UI server's first keys, `packages/orchestration/config_keys_ui.py`.
  Step (5), done by F203: the logging keys, `packages/orchestration/config_keys_logging.py`.
  Step (6), done by F310: the budget keys, `packages/orchestration/config_keys_budget.py`.
  Step (7), done by F078: the watchdog's keys, `packages/orchestration/config_keys_autonomy.py`.
- `packages/orchestration/mission_state.py`: the record — its constants, its errors and the
  three types a mission is stored as — then the verify-first follow-up path, each to a module of
  its own; the locations, the store and the links stay. Step (1), done by F205: the record,
  `packages/orchestration/mission_record.py`, and the file left the table. Step (2), begun by
  F297: the follow-up job's creation, `packages/orchestration/mission_followup.py`; the verify task
  and its run follow, with `run_guarded_test_command`, which a test replaces on this module,
  staying beside the code that calls it.
- `packages/orchestration/do_sequence.py`: the context a walk carries, where its jobs go, the
  cockpit, the apply and push, and the walk's summaries, each to a module of its own; the step
  table, the walker, `plan_order_job` and the plan, shape and run steps stay (the study step moved
  to `packages/orchestration/do_study.py` on 2026-10-17, which took the file under its row), because
  a test replaces `plan_order_job` on this module. Step (1), done by F205: the context and the
  targets, `packages/orchestration/do_context.py` and `packages/orchestration/do_targets.py`. Step
  (2), done by F205: the cockpit and the summaries, the cockpit's module deleted with the old face
  since (amend1015f D22) and `packages/orchestration/do_summary.py`. Step (3), done by F205: the
  apply and push, `packages/orchestration/do_apply.py`, and the file left the table. F312 moved
  `do_job_task_listing`, the listing of the walk's jobs, to `packages/orchestration/do_summary.py`
  under step (2).
- `apps/cli/commands/do_cmd.py`: what `remedy do` reads before any step, then the `run`
  handlers, then the `job` handlers, each to a module of its own; `_cmd_do` and `_cmd_do_order`
  stay. Step (1), done by F205: `_order_repo` and the reading of the order file,
  `apps/cli/commands/do_order_input.py`. Step (2), done by F058: the `run` handlers,
  `apps/cli/commands/run_report_cmd.py`.
- `packages/orchestration/public_api.py`: the write routes' argument builders and refusals,
  then the route table, then the page's rendering, each to a module of its own; the answer
  functions stay. Step (1), done by F205: the write routes' argument builders and refusals,
  `packages/orchestration/public_api_writes.py`, and the file left the table.
  Step (2), done by F199: the route table, `packages/orchestration/public_api_routes.py`.

## Functions above 100 lines

| Lines | File | Function |
|---|---|---|
| 1434 | `packages/orchestration/pingpong_job.py` | `run_job` |
| 1262 | `packages/orchestration/pingpong_loop.py` | `run_pingpong` |
| 887 | `packages/orchestration/decision_queue.py` | `list_decisions` |
| 718 | `packages/orchestration/job_evidence.py` | `export_job_evidence` |
| 455 | `packages/orchestration/serve_http_handler.py` | `_RemedyHandler._handle_command_submission` |
| 352 | `apps/cli/commands/decision.py` | `_cmd_decision_resolve` |
| 423 | `packages/orchestration/long_run_executor.py` | `run_cycles` |
| 406 | `packages/orchestration/orchestrator_loop.py` | `run_mission` |
| 295 | `apps/cli/commands/worker_facade_cmd.py` | `doctor_core_report` |
| 346 | `packages/orchestration/job_apply.py` | `_apply_from_workspace` |
| 334 | `scripts/build_review_manifest.py` | `build_manifest_from_snapshot` |
| 320 | `packages/orchestration/trust_report.py` | `summarize_trust_report` |
| 317 | `scripts/build_review_zip.py` | `main` |
| 312 | `packages/orchestration/test_execution_service.py` | `execute_test_run` |
| 300 | `packages/orchestration/repository_snapshot.py` | `revert_repository_apply` |
| 299 | `packages/orchestration/final_verifier.py` | `build_final_verifier_report` |
| 282 | `apps/cli/commands/job.py` | `_cmd_run_next_task_local` |
| 280 | `packages/orchestration/patch_apply.py` | `apply_patch_intent` |
| 279 | `packages/orchestration/repository_snapshot.py` | `create_snapshot` |
| 275 | `packages/orchestration/diff_parser.py` | `parse_unified_diff_to_view` |
| 274 | `packages/orchestration/run_manifest.py` | `_collect_calls` |
| 271 | `apps/cli/commands/job.py` | `_cmd_job_budget` |
| 165 | `packages/orchestration/do_sequence.py` | `plan_order_job` |
| 247 | `packages/orchestration/token_truth.py` | `build_token_truth` |
| 236 | `packages/orchestration/job_evidence.py` | `create_manual_completion_bundle` |
| 235 | `apps/cli/commands/job.py` | `_cmd_resume` |
| 230 | `packages/orchestration/run_manifest.py` | `validate_run_manifest` |
| 221 | `scripts/build_review_manifest.py` | `_gate_semantic_problems` |
| 220 | `packages/orchestration/job_apply.py` | `apply_job` |
| 220 | `scripts/build_review_manifest.py` | `validate_manual_completion` |
| 217 | `packages/orchestration/verifier.py` | `verify_task_output` |
| 215 | `packages/runtimes/dev_server.py` | `stop_recorded_runtime` |
| 211 | `packages/orchestration/pingpong_loop.py` | `compose_builder_prompt` |
| 209 | `packages/orchestration/proof_chain.py` | `build_proof_chain` |
| 206 | `apps/cli/commands/runtime_cmd.py` | `_serve_supervisor` |
| 183 | `apps/cli/commands/do_cmd.py` | `_cmd_job_run` |
| 203 | `apps/cli/grouped.py` | `_add_command_args` |
| 199 | `apps/cli/commands/runtime_cmd.py` | `_cmd_runtime_probe` |
| 161 | `apps/cli/commands/do_cmd.py` | `_cmd_do_order` |
| 190 | `packages/orchestration/context_compiler.py` | `compile_task_context` |
| 172 | `packages/orchestration/job_apply.py` | `summarize_job_apply` |
| 190 | `packages/orchestration/pingpong_job.py` | `_strict_apply_to_workspace` |
| 186 | `packages/orchestration/source_apply.py` | `apply_structured_patch` |
| 184 | `packages/orchestration/pingpong_loop.py` | `compose_reviewer_prompt` |
| 183 | `packages/orchestration/task_edit_runtime.py` | `edit_task_at_runtime` |
| 155 | `apps/cli/commands/status_cmd.py` | `_cmd_status` |
| 179 | `scripts/build_review_manifest.py` | `validate_evidence_candidate` |
| 178 | `packages/orchestration/subtree_rerun.py` | `prepare_subtree_rerun` |
| 177 | `apps/cli/commands/job.py` | `_cmd_job_resume` |
| 121 | `packages/orchestration/client_digest.py` | `build_client_digest` |
| 171 | `scripts/build_observability_index.py` | `_build_task_section` |
| 168 | `apps/cli/commands/runtime_cmd.py` | `_cmd_runtime_serve` |
| 168 | `packages/orchestration/builder_bridge.py` | `run_builder_bridge` |
| 160 | `packages/orchestration/artifact_contract_gate.py` | `check_worktree_artifacts` |
| 159 | `packages/orchestration/final_job_review.py` | `build_final_job_review` |
| 159 | `packages/orchestration/final_verifier.py` | `_operator_attested_tasks` |
| 159 | `packages/orchestration/project_context_coverage.py` | `derive_project_context_coverage` |
| 159 | `packages/orchestration/run_manifest.py` | `validate_input_snapshot` |
| 159 | `packages/orchestration/self_use_runner.py` | `run_next_self_use_item` |
| 158 | `packages/orchestration/file_provenance.py` | `build_file_provenance` |
| 151 | `packages/orchestration/public_api.py` | `answer_public_api_post` |
| 155 | `packages/orchestration/budget_decision.py` | `answer_budget_decision` |
| 155 | `packages/orchestration/task_injection.py` | `answer_injection_shortfall` |
| 152 | `scripts/build_observability_index.py` | `build_observability_index` |
| 151 | `packages/orchestration/ownership_phrases.py` | `ownership_sentence` |
| 150 | `packages/orchestration/project_summary.py` | `detect_patterns` |
| 147 | `packages/orchestration/archive_plan.py` | `build_archive_plan` |
| 146 | `packages/orchestration/project_constitution.py` | `load_project_constitution` |
| 145 | `packages/orchestration/context_coverage.py` | `derive_context_coverage` |
| 103 | `apps/cli/commands/dev.py` | `_dev_status` |
| 143 | `packages/orchestration/pingpong_job.py` | `_stop_job` |
| 140 | `packages/orchestration/pingpong_provider_call.py` | `_call_with_retry` |
| 143 | `packages/orchestration/token_authority.py` | `validate_token_truth` |
| 142 | `packages/orchestration/repository_snapshot.py` | `build_snapshot_truth` |
| 142 | `packages/orchestration/stream_evidence.py` | `run_streamed_command` |
| 142 | `packages/orchestration/worktree_resume.py` | `prepare_worktree_resume` |
| 141 | `packages/orchestration/job_evidence.py` | `_write_run_manifest_export` |
| 141 | `packages/orchestration/serve_http_handler.py` | `_RemedyHandler._read_command_payload` |
| 140 | `apps/cli/commands/job.py` | `_cmd_plan_job_local` |
| 140 | `packages/orchestration/builder_bridge.py` | `run_builder_bridge_loop` |
| 140 | `packages/orchestration/change_set.py` | `derive_change_set` |
| 139 | `packages/orchestration/pingpong_job.py` | `_export_job` |
| 138 | `apps/cli/commands/job.py` | `_cmd_job_run_cycles` |
| 138 | `scripts/build_review_manifest.py` | `validate_verification_tests` |
| 137 | `packages/orchestration/run_manifest.py` | `validate_call_expectation` |
| 136 | `packages/runtimes/runtime_supervisor.py` | `Supervisor.run` |
| 135 | `packages/orchestration/run_manifest.py` | `validate_call_ledgers` |
| 134 | `packages/orchestration/project_brain_aggregate.py` | `build_project_brain_aggregate` |
| 134 | `packages/orchestration/token_cost_policy.py` | `build_token_cost_policy` |
| 133 | `packages/orchestration/pingpong_provider.py` | `ClaudeCliProvider._call_reviewer_structured` |
| 133 | `packages/orchestration/serve_http_handler.py` | `_RemedyHandler._dispatch_decision_resolve` |
| 131 | `packages/orchestration/failure_stats.py` | `collect_failures` |
| 131 | `packages/orchestration/pingpong_loop.py` | `_aggregate_usage_actuals` |
| 131 | `packages/orchestration/review_scope.py` | `build_review_scope_packet` |
| 131 | `packages/orchestration/run_manifest.py` | `validate_index_and_tree` |
| 130 | `packages/orchestration/budget_guard.py` | `evaluate_budget` |
| 129 | `packages/orchestration/test_runner.py` | `run_tests_local` |
| 104 | `packages/orchestration/budget_guard.py` | `decode_persisted_budget_actuals` |
| 128 | `packages/runtimes/dev_server.py` | `classify_state` |
| 127 | `packages/orchestration/pingpong_loop.py` | `export_pingpong_json` |
| 127 | `packages/orchestration/stream_evidence.py` | `capture_stream_evidence` |
| 123 | `packages/orchestration/watchdog.py` | `act_on_trips` |
| 126 | `packages/orchestration/artifact_contract_gate.py` | `build_artifact_contract_gate` |
| 122 | `packages/orchestration/exec_guard.py` | `run_guarded` |
| 125 | `packages/orchestration/gauntlet_runner.py` | `run_order` |
| 125 | `packages/orchestration/pingpong_loop.py` | `_build_token_accounting` |
| 125 | `packages/orchestration/run_manifest.py` | `write_run_manifest` |
| 124 | `packages/orchestration/pingpong_job.py` | `_write_run_manifest_record` |
| 124 | `packages/orchestration/task_injection.py` | `apply_injection_to_job` |
| 123 | `packages/orchestration/job_report.py` | `export_job_report` |
| 123 | `packages/orchestration/pingpong_loop.py` | `_build_provider_evidence` |
| 123 | `scripts/build_review_manifest.py` | `evaluate_ready_gate_matrix` |
| 122 | `packages/orchestration/artifact_contract_gate.py` | `check_stream_artifacts` |
| 122 | `packages/orchestration/pingpong_job.py` | `_import_job` |
| 121 | `packages/orchestration/project_summary.py` | `build_project_summary` |
| 120 | `packages/orchestration/job_report.py` | `format_job_report_text` |
| 120 | `packages/orchestration/scope_fences.py` | `_load_fence_spec_effective` |
| 120 | `packages/orchestration/spec_compliance.py` | `build_spec_compliance_checklist` |
| 120 | `packages/orchestration/study.py` | `run_study` |
| 119 | `packages/orchestration/memory_learn.py` | `learn_from_job` |
| 119 | `packages/orchestration/run_contract.py` | `evaluate_run_action` |
| 119 | `packages/orchestration/run_manifest.py` | `_read_worktree_identity` |
| 118 | `packages/orchestration/pingpong_loop.py` | `_record_call_failure` |
| 118 | `packages/orchestration/task_injection.py` | `draft_task_injection` |
| 116 | `packages/orchestration/model_routing.py` | `validate_task_class_tier_overrides` |
| 114 | `packages/orchestration/provider_token_evidence.py` | `validate_provider_token_evidence` |
| 113 | `packages/orchestration/job_evidence.py` | `_build_job_agent_run_trace` |
| 113 | `packages/orchestration/repository_snapshot.py` | `verify_snapshot` |
| 112 | `apps/cli/commands/patch.py` | `_cmd_revert_patch_intent` |
| 112 | `packages/orchestration/pingpong_job.py` | `parse_job_file` |
| 112 | `packages/orchestration/subtree_rerun.py` | `plan_subtree_reset` |
| 112 | `packages/orchestration/task_injection.py` | `confirm_task_injection` |
| 112 | `packages/runtimes/dev_server.py` | `DevServer.start` |
| 112 | `scripts/build_review_manifest.py` | `_verify_task_provenance_integrity` |
| 111 | `packages/orchestration/run_manifest.py` | `_verified_episode_export` |
| 110 | `apps/cli/commands/do_cmd.py` | `_cmd_do` |
| 110 | `packages/orchestration/job_plan.py` | `render_plan_md` |
| 110 | `packages/orchestration/run_manifest.py` | `validate_job_input_definition` |
| 110 | `packages/orchestration/run_manifest.py` | `validate_ledger_chain` |
| 109 | `apps/cli/commands/init_cmd.py` | `_handle_init` |
| 108 | `packages/orchestration/serve_daemon.py` | `run_supervisor` |
| 107 | `packages/orchestration/timeline.py` | `_render_task_block` |
| 106 | `packages/orchestration/diff_view_source.py` | `build_diff_view` |
| 105 | `packages/orchestration/test_execution_service.py` | `finalize_test_outcome` |
| 104 | `packages/orchestration/autonomy_loop.py` | `_decide` |
| 103 | `apps/cli/commands/teacher_cmd.py` | `_cmd_teacher_ask` |
| 103 | `packages/orchestration/pingpong_provider.py` | `ClaudeCliProvider._review_impl` |
| 102 | `packages/common/secure_fs.py` | `read_verified_file_at` |
| 102 | `packages/orchestration/continue_from_node.py` | `continue_from_node` |
| 102 | `packages/orchestration/pingpong_job.py` | `_finalize_job_workspace` |
| 101 | `packages/orchestration/mission_compiler.py` | `compile_mission_plan` |

## Files above 1,000 lines

| Lines | File |
|---|---|
| 6207 | `packages/orchestration/run_manifest.py` |
| 4943 | `packages/orchestration/pingpong_job.py` |
| 4921 | `packages/orchestration/pingpong_loop.py` |
| 1824 | `packages/orchestration/serve_http_handler.py` |
| 3495 | `scripts/build_review_manifest.py` |
| 2992 | `packages/orchestration/job_evidence.py` |
| 2255 | `apps/cli/command_catalog.py` |
| 2541 | `packages/orchestration/job_apply.py` |
| 2483 | `apps/cli/commands/job.py` |
| 2255 | `packages/orchestration/orchestrator_loop.py` |
| 1898 | `scripts/remedy_smoke.sh` |
| 1983 | `packages/runtimes/dev_server.py` |
| 1574 | `packages/orchestration/pingpong_provider.py` |
| 1879 | `packages/orchestration/token_ledger.py` |
| 1816 | `packages/orchestration/long_run_executor.py` |
| 1545 | `packages/orchestration/config.py` |
| 1650 | `packages/orchestration/brain_detail.py` |
| 1650 | `packages/orchestration/repository_snapshot.py` |
| 1442 | `packages/orchestration/model_routing.py` |
| 1349 | `packages/orchestration/task_injection.py` |
| 1182 | `packages/orchestration/decision_queue.py` |
| 1199 | `packages/orchestration/context_compiler.py` |
| 1168 | `packages/orchestration/mission_dossier.py` |
| 1158 | `packages/orchestration/project_brain.py` |
| 1156 | `packages/orchestration/review_subject.py` |
| 1138 | `packages/orchestration/test_execution_service.py` |
| 1111 | `packages/orchestration/run_report.py` |
| 1094 | `packages/orchestration/final_verifier.py` |
| 1071 | `packages/orchestration/command_discovery.py` |
| 1049 | `packages/orchestration/brain_viewer.py` |
| 1039 | `packages/orchestration/result_tour.py` |
