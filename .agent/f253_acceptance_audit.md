# F253 acceptance audit (amend0930b-slow-cap hardening stage)

Commit audited: c7633415bd7f37b2c8af98deacf17845f5420356 (branch
feature/f253-public-http-api), in a detached worktree at
`.remedy-wt/f253-audit-wt`.

Feature file: `docs/roadmap/features/T12_F253.md`.
Headings audited: `## Goal & Done`, `## Acceptance & tests`,
the paragraph "Acceptance, added" and the "Binding additions" bullets of
`## Amendment — DECISION amend1007b D3`. Read in full: the whole file, including
`## Amendment — operator amendment amend1006-luna-control-plane` and
`## Amendment — DECISION F253 D1` (the MCP facet moves to F303; nothing audited was in it).

## What was read, and what was not

Read: the paragraph "Operator amendment amend0930b-slow-cap" of
`docs/agents/self_drive_protocol.md`; the feature file; `docs/system/public-http-api-v1.md`;
`packages/orchestration/public_api.py`, `serve_daemon.py`, `serve_runs.py`,
`api_clients.py` and the relevant parts of `ui_server.py` and `client_digest.py`;
`apps/cli/command_catalog.py` (the `UI_EXPOSED_COMMANDS` set); the tests
`tests/ui_server/test_public_api.py`, `tests/orchestration/test_serve_daemon.py`,
`tests/orchestration/test_public_api_gate_paths.py`, parts of
`tests/orchestration/test_client_digest.py`, and the names of the tests in
`tests/cli/test_machine_client_contract.py` and `tests/cli/test_machine_client_paths.py`.
Lines of the feature files F200, F295, F298, F303 and F304 were found by `grep` to
confirm where a moved statement went and what "second gate test" and "the door" mean.

Not read: `.agent/handoff.md`, `.agent/live_review.md`, `.agent/live_review_archive.md`,
`.agent/plan.md`, `.agent/decisions.md`, `.agent/prose_slips.md`, `.agent/authored/`,
`.agent/operator_questions.md`, any other `.remedy-wt/f253-*` folder, the repository's own
`.data` folder. DECISION labels met in code, tests and the page are treated as text.

## How the mutations ran

One script, `.remedy-wt/f253-audit/mutations.py`, holds every mutation as exact old and
new strings (`check_edits.py` checked that each old string occurs exactly once). For each
mutation it runs `python3 -B -m pytest -q -p no:cacheprovider <nodes>` with the worktree
as working directory: first on the unmutated worktree (control), then with the mutation
applied (mutated), then `git -C <worktree> checkout -- .` and a check that `git status
--porcelain` is empty (it was empty after every mutation). Raw outputs are
`<id>.control.txt` and `<id>.mutated.txt`, results `<id>.result.json`, all in
`.remedy-wt/f253-audit/`. When two mutations in one script run named the same nodes the
control ran once and its exit was reused; each result file holds the exit used.
Only production files were mutated (code, and for statements 7 and 32 the docs page).
Only fake providers and local scratch data roots were used; no model was called.
Two early shell calls (reading files) began with `cd` into the worktree; they changed
nothing. The verdict PROVED (HTTP) is used where a red test sends real HTTP requests to a
running supervisor: the gate tests start `remedy serve start --json` as a child process;
the `test_serve_daemon.py` tests run `run_supervisor` in a thread and use its API port.
A mutated exit of 1 was checked in the raw output to be an assertion failure of the
named test, not a collection error.

## Claims and proofs

| # | Claim (heading) | Test node(s) | Mutation (file and exact change) | Control exit | Mutated exit | Verdict |
|---|---|---|---|---|---|---|
| 1 | Goal & Done: a PUBLIC, versioned HTTP API (the major number is in the path `/api/v1`) | `tests/orchestration/test_serve_daemon.py::test_the_api_port_answers_the_interface_route_with_the_sockets_own_token` | `packages/orchestration/public_api.py`: `PUBLIC_API_PREFIX = "/api/v1"` -> `"/api/v2"` | 0 | 1 | PROVED (HTTP) |
| 2 | Goal & Done: everything the shipped UI can do is reachable through the published surface (DONE when every shipped-UI capability is reachable) | - | Amendment amend1007b D3: "The third task, the shipped interface's migration, and the capabilities only the shipped interface uses are split off to F303" | - | - | MOVED |
| 3 | Goal & Done: the shipped UI itself consumes ONLY the public API (no privileged side channels) | - | Same sentence of the amendment (the shipped interface's migration is split off to F303); F303 line 24 carries it: "it consumes only the public API" | - | - | MOVED |
| 4 | Goal & Done: a versioning/deprecation policy exists (a deprecated route answers `Deprecation: true`) | `tests/ui_server/test_public_api.py::test_a_deprecated_route_answers_the_deprecation_header` | `packages/orchestration/public_api.py`: in `answer_public_api_get` `headers = {"Deprecation": "true"} if route.deprecated else {}` -> `headers = {}` | 0 | 1 | PROVED |
| 5 | Goal & Done: contract tests pin every published endpoint (11 routes; table below) | the test `PINNED_ROUTES` names for each route; see the table 'Per-route pins' | `packages/orchestration/public_api.py`: each route's `path=` gets an `x` appended (11 mutations) | all 0 | all non-zero | PROVED |
| 6 | Acceptance: the shipped UI consumes ONLY the public API (asserted by test) | - | Same amendment sentence: the shipped interface's migration is split off to F303 | - | - | MOVED |
| 7 | Acceptance: a versioning/deprecation policy exists and is published with the contract document | `tests/ui_server/test_public_api.py::test_the_page_states_the_prefix_the_auth_scheme_and_the_refusal_tokens` | `docs/system/public-http-api-v1.md`: the section `## The version rule` is cut out (the page is the published artifact, not code; see observation 1) | 0 | 1 | PROVED |
| 8 | Acceptance: an unpinned endpoint fails the suite | `tests/ui_server/test_public_api.py::test_every_route_is_pinned_by_name` | `packages/orchestration/public_api.py`: a twelfth route `GET /api/v1/audit-extra` (twin `client.interface`) is added to `PUBLIC_API_ROUTES` | 0 | 1 | PROVED |
| 9 | Acceptance: a mutating call without a token is rejected | `tests/orchestration/test_serve_daemon.py::test_a_post_on_the_api_port_answers_what_the_resolve_command_prints` (red); `tests/ui_server/test_public_api.py::test_post_put_and_delete_without_the_token_are_401` (stayed green, the cockpit answers a write 405 before the check) | `packages/orchestration/ui_server.py`: in `_send_public_api_post` `if not accepted:` -> `if False:` | 0 | 1 | PROVED (HTTP) |
| 10 | Acceptance: every accepted call leaves a ledger entry | `tests/orchestration/test_serve_daemon.py::test_a_post_on_the_api_port_answers_what_the_resolve_command_prints`, `tests/ui_server/test_public_api.py::test_the_ledger_holds_one_line_per_request_in_order` | `packages/orchestration/ui_server.py`: in `_send_public_api_answer` the call `append_public_api_call(` -> `(lambda **_kw: None)(` | 0 | 1 | PROVED (HTTP) |
| 11 | Acceptance, added: F295's gate test passes again driven through HTTP alone | `tests/orchestration/test_public_api_gate_paths.py::test_f295s_gate_path_runs_from_the_order_to_the_proof_over_http_alone` (starts `remedy serve start --json` as a child process) | `packages/orchestration/public_api.py`: in `_start_run_answer` `return 202, build_ok(...run_record_payload...)` -> `return 200, ...` | 0 | 1 | PROVED (HTTP) |
| 12 | Acceptance, added: F298's second gate test (five paths, now in `tests/cli/test_machine_client_paths.py`) passes again driven through HTTP alone | `tests/orchestration/test_public_api_gate_paths.py`: the apply-with-history-and-push, two-jobs, naming-its-project and decline tests (four of the five paths); the fifth, one order file started twice, has no HTTP test | S12a `packages/orchestration/public_api.py`: `options = ["--approve", *repo]` -> `options = [*repo]` (three apply tests); S12b `packages/orchestration/public_api.py`: the `--reason=...` item dropped from `_job_decline_argv` (decline test) | 0/0 | 1/1 | GAP |
| 13 | Acceptance, added: two orders at once never corrupt a record; both run or the second is refused with a token | `tests/orchestration/test_serve_daemon.py::test_two_order_create_posts_sent_at_once_both_run_and_every_record_reads_back_whole` | `packages/orchestration/serve_runs.py`: `OrderLauncher.start` makes every order id `"0123456789abcdef"` and `order_dir.mkdir(mode=0o700)` -> `mkdir(mode=0o700, exist_ok=True)` (two orders share one folder) | 0 | 1 | PROVED (HTTP) |
| 14 | Acceptance, added: a client token outside its policy is refused | `tests/ui_server/test_public_api.py::test_a_client_order_outside_its_projects_through_the_socket_handler_starts_nothing`, `tests/ui_server/test_public_api.py::test_a_client_decline_of_a_job_of_another_project_through_the_socket_handler_runs_nothing` (real HTTP on the supervisor's own handler class over a unix socket) | `packages/orchestration/ui_server.py`: in `_send_public_api_post` `start_order, client=client,` -> `start_order, client=None,` | 0 | 1 | PROVED |
| 15 | Acceptance, added: the contract document read over HTTP equals the command's | `tests/orchestration/test_serve_daemon.py::test_the_api_port_answers_the_interface_route_with_the_sockets_own_token` | `packages/orchestration/public_api.py`: `_client_interface_answer` returns `build_ok(**dict(list(build_client_interface().items())[:-1]))` (last key dropped) | 0 | 1 | PROVED (HTTP) |
| 16 | Binding additions: no second server, no second write protocol; the routes are added to the request handler the cockpit and the supervisor already share | `tests/ui_server/test_public_api.py::test_interface_route_answers_the_command_envelope` (cockpit), `tests/ui_server/test_public_api.py::test_the_same_route_over_the_supervisors_socket_answers_the_same_body` (supervisor socket), `tests/orchestration/test_serve_daemon.py::test_the_api_port_answers_the_interface_route_with_the_sockets_own_token` (supervisor port) | `packages/orchestration/ui_server.py`: in `_RemedyHandler.do_GET` `if is_public_api_path(path):` -> `if False:` (one edit makes all three servers lose the route) | 0 | 1 | PROVED (HTTP) |
| 17 | Binding additions: a write goes through the F009 door as a new command | none found | no mutation; measurement in `measure.txt` (see Gaps) | - | - | GAP |
| 18 | Binding additions: every route calls the function its command-line twin calls, and a test compares each route's answer with its command's envelope (11 routes; table below) | see the table 'Per-route answers' | each route's answer builder gets one key added or changed (11 mutations) | all 0 | all non-zero | GAP |
| 19 | Binding additions: the supervisor serves the API on a localhost port the configuration names (`serve.api_port`) | `tests/orchestration/test_serve_daemon.py::test_run_supervisor_without_the_keyword_reads_serve_api_port_from_configuration`, `tests/orchestration/test_public_api_gate_paths.py::test_a_completed_result_is_declined_over_http_and_waits_for_nothing` | `packages/orchestration/serve_daemon.py`: `get_config().get("serve.api_port")` -> `get("serve.api_portx")` | 0 | 1 | PROVED (HTTP) |
| 20 | Binding additions: ... beside its socket | `tests/orchestration/test_serve_daemon.py::test_a_run_post_on_the_port_starts_the_run_and_the_socket_starts_another` | `packages/orchestration/serve_daemon.py`: in `run_supervisor` right after `thread.start()` the socket server is shut down and closed when an API port is set | 0 | 1 | PROVED (HTTP) |
| 21 | Binding additions: ... so that a client that is another user of the same machine reaches it | none found on the port (client-token tests use `tests/ui_server/test_public_api.py` with the cockpit and socket handlers only) | `packages/orchestration/serve_daemon.py`: `public_api_handler_class` gets a `_public_api_caller` that refuses every client token (the port only) | 0 | 0 | GAP |
| 22 | Binding additions: nothing is bound beyond localhost | `tests/orchestration/test_serve_daemon.py::test_the_api_listener_binds_127_0_0_1_only` | `packages/orchestration/serve_daemon.py`: `("127.0.0.1", resolved_api_port)` -> `("0.0.0.0", resolved_api_port)` | 0 | 1 | PROVED |
| 23 | Binding additions: nothing here adds TLS or a remote story (F201) | none found | no mutation; measurement in `measure.txt` (see Gaps) | - | - | GAP |
| 24 | Binding additions: a client token carries a policy: the projects it may order work on | `tests/ui_server/test_public_api.py::test_a_client_order_for_a_project_it_does_not_list_is_403_and_starts_nothing`, `tests/ui_server/test_public_api.py::test_a_client_write_for_a_job_of_another_project_is_403_and_runs_nothing` | `packages/orchestration/api_clients.py`: `client_lists_project` returns `True` instead of the `any(...)` test | 0 | 1 | PROVED |
| 25 | Binding additions: ... the largest limits it may set (an order's caps; a budget answer) | `tests/ui_server/test_public_api.py::test_a_client_order_is_held_to_its_ceilings` (S25a); `tests/ui_server/test_public_api.py::test_a_client_budget_answer_above_its_ceiling_is_403_and_runs_nothing` (S25b) | `packages/orchestration/api_clients.py`: S25a `if parsed > ceiling:` -> `if False:` in `_cap_refusal`; S25b `if parsed is not None and parsed > ceiling:` -> `if False:` in `client_budget_answer_refusal` | 0/0 | 1/1 | PROVED |
| 26 | Binding additions: ... whether it may approve an apply | `tests/ui_server/test_public_api.py::test_a_client_apply_needs_its_may_apply` | `packages/orchestration/public_api.py`: `if client is not None and route.twin == "job.apply" and not client.may_apply:` -> `if False:` | 0 | 1 | PROVED |
| 27 | Binding additions: a call outside the policy is refused with its own token (`api_client_policy_refused`) | `tests/ui_server/test_public_api.py::test_a_client_apply_needs_its_may_apply` (S27a), `tests/ui_server/test_public_api.py::test_a_client_order_for_a_project_it_does_not_list_is_403_and_starts_nothing` (S27b) | `packages/orchestration/public_api.py`: S27a the apply refusal's token string -> `"api_refused"`; S27b the order refusal's token in `PublicApiWriteRefusal(403, ...)` -> `"api_refused"` | 0/0 | 1/1 | PROVED |
| 28 | Binding additions: every call writes a ledger entry (a client's call names the client) | `tests/ui_server/test_public_api.py::test_a_client_token_reads_a_route_like_the_servers_token_and_the_ledger_names_it` | `packages/orchestration/ui_server.py`: in `_send_public_api_get` `client_name=client.name if client else ""` -> `client_name=""` | 0 | 1 | PROVED |
| 29 | Binding additions: limits are told in tokens and provider calls (ruling R1) | `tests/ui_server/test_public_api.py::test_a_client_order_is_held_to_its_ceilings` (both ceilings) | `packages/orchestration/api_clients.py`: `client_order_refusal` drops the `max-provider-calls` check | 0 | 1 | PROVED |
| 30 | Binding additions: usage is told in tokens and provider calls (ruling R1) | `tests/orchestration/test_client_digest.py::test_each_job_carries_the_calls_and_tokens_by_kind_its_ledger_holds` (the function the digest route calls) | `packages/orchestration/client_digest.py`: a job entry's `"tokens": _tokens_by_kind(usage)` -> `"tokens": {}` | 0 | 1 | PROVED |
| 31 | Binding additions: a client's tests need the real thing: the supervisor on a scratch data root with the fake providers behaves exactly as the real one | `tests/orchestration/test_public_api_gate_paths.py::test_a_completed_result_is_declined_over_http_and_waits_for_nothing` (supervisor started as a child on a scratch root, an order with fake providers) | `packages/orchestration/serve_runs.py`: `child_environment` gives children `REMEDY_DATA_DIR` = the scratch root + `/elsewhere` | 0 | 1 | PROVED (HTTP) |
| 32 | Binding additions: the contract document says how a client's test starts the supervisor | none found | `docs/system/public-http-api-v1.md`: the section `## A client's test` is cut out | 0 | 0 | GAP |

Per-route pins (statement 5): each registry path was changed and the test that
`PINNED_ROUTES` names for the route was run.

| Route | Pinning test (in `tests/ui_server/test_public_api.py`) | Control | Mutated |
|---|---|---|---|
| GET /api/v1/interface | `test_interface_route_answers_the_command_envelope` | 0 | 1 |
| GET /api/v1/digest | `test_digest_route_answers_the_status_commands_client_object` | 0 | 1 |
| GET /api/v1/jobs/{job}/proof | `test_proof_route_answers_the_change_proof_command` | 0 | 1 |
| GET /api/v1/changes | `test_changes_route_answers_the_client_changes_command` | 0 | 1 |
| POST /api/v1/jobs/{job}/decisions/{decision} | `test_the_decision_route_is_pinned_with_its_body_and_its_statuses` | 0 | 1 |
| POST /api/v1/jobs/{job}/decline | `test_the_decline_route_is_pinned_with_its_body_and_its_statuses` | 0 | 1 |
| POST /api/v1/jobs/{job}/apply | `test_the_apply_route_is_pinned_with_its_body_and_its_statuses` | 0 | 1 |
| GET /api/v1/orders/{order} | `test_the_order_poll_route_is_pinned_with_its_statuses` | 0 | 1 |
| POST /api/v1/orders | `test_the_order_create_route_is_pinned_with_its_body_and_its_statuses` | 0 | 1 |
| GET /api/v1/jobs/{job}/run | `test_the_run_poll_route_is_pinned_with_its_statuses` | 0 | 1 |
| POST /api/v1/jobs/{job}/run | `test_the_run_route_is_pinned_with_its_body_and_its_statuses` | 0 | 1 |

Per-route answers (statement 18): each route's answer was changed and the test that
compares it was run.

| Route | Test | Mutation | Control | Mutated | What the test compares with |
|---|---|---|---|---|---|
| GET /api/v1/interface | `tests/ui_server/test_public_api.py::test_interface_route_answers_the_command_envelope` | `build_ok(**build_client_interface())` gets `audit_mutation=1` | 0 | 1 | compares |
| GET /api/v1/digest | `tests/ui_server/test_public_api.py::test_digest_route_answers_the_status_commands_client_object` | `build_ok(**build_client_digest(...))` gets `audit_mutation=1` | 0 | 1 | compares |
| GET /api/v1/jobs/{job}/proof | `tests/ui_server/test_public_api.py::test_proof_route_answers_the_change_proof_command` | `build_ok(**export_proof_chain_json(chain))` gets `audit_mutation=1` | 0 | 1 | compares |
| GET /api/v1/changes | `tests/ui_server/test_public_api.py::test_changes_route_answers_the_client_changes_command` | `build_ok(**build_client_changes(...))` gets `audit_mutation=1` | 0 | 1 | compares |
| GET /api/v1/orders/{order} | `tests/ui_server/test_public_api.py::test_the_order_poll_route_answers_as_the_client_order_command_does` | `_order_answer` returns `build_ok(audit_mutation=1, **order_record_payload(...))` | 0 | 1 | compares |
| GET /api/v1/jobs/{job}/run | `tests/ui_server/test_public_api.py::test_the_run_poll_route_answers_as_the_client_run_command_does` | `_run_answer` returns `build_ok(audit_mutation=1, **run_record_payload(...))` | 0 | 1 | compares |
| POST /api/v1/jobs/{job}/decisions/{decision} | `tests/orchestration/test_serve_daemon.py::test_a_post_on_the_api_port_answers_what_the_resolve_command_prints` | `--reason=` value upper-cased in `_decision_resolve_argv` | 0 | 1 | compares |
| POST /api/v1/jobs/{job}/decline | `tests/orchestration/test_serve_daemon.py::test_a_decline_post_answers_what_the_decline_command_prints` | `!` appended to the `--reason=` value in `_job_decline_argv` | 0 | 1 | compares |
| POST /api/v1/jobs/{job}/apply | `tests/orchestration/test_serve_daemon.py::test_an_apply_post_refuses_as_the_command_does_or_before_it + test_an_apply_post_lands_one_commit_in_the_jobs_own_repository` | `--approve` dropped in `_job_apply_argv` | 0 | 1 | compares (refusals) / effect |
| POST /api/v1/orders | `tests/ui_server/test_public_api.py::test_an_order_create_post_answers_202_with_the_starters_record` | 202 answer gets `audit_mutation=1` | 0 | 1 | literal dict, no command envelope |
| POST /api/v1/jobs/{job}/run | `tests/ui_server/test_public_api.py::test_a_run_post_starts_the_run_by_the_full_id_and_answers_202_with_its_record` | 202 answer gets `audit_mutation=1` | 0 | 1 | literal record, no command envelope |

Observations that are not counted as gaps:

1. The page is a document, so statement 7's mutation edits a docs file, not code. A second
   mutation (S7x) reduces the whole version rule to the single sentence "A route marked
   deprecated answers the header `Deprecation: true`." and runs every test whose name holds
   "page" in `tests/ui_server/test_public_api.py`: control 0, mutated 0. The page tests pin
   the header token only, not the rules (major number in the path, only additions, minor
   number raised, removal only under a new major path). Statement 7 stays PROVED because
   removing the policy altogether turns a test red; the content is unguarded.
2. The `Deprecation: true` header is built by two identical lines, one in
   `answer_public_api_get` and one in `answer_public_api_post`. S4b blanks the POST one and
   runs `-k deprecat` over `tests/ui_server/test_public_api.py`: control 0, mutated 0. Only
   a deprecated GET route is tested (statement 4 is PROVED by the GET line).
3. S30x blanks the job `tokens` of the digest and runs the HTTP digest test
   (`test_digest_route_answers_the_status_commands_client_object`): control 0, mutated 0.
   That test compares the route with the command, and both call the same function, so the
   digest's content is pinned by `tests/orchestration/test_client_digest.py`, not over HTTP.
4. Statement 11's mutation (202 -> 200) is a coarse one; the gate test would also turn red
   for any broken step of its seven.
5. Statement 9: of the two named nodes only the daemon one (a real supervisor port) turned
   red; the cockpit node stayed green because the cockpit never reaches that check for a
   write (it answers 405 first).

## Gaps

Statement 12 (F298's second gate test through HTTP alone).
  `tests/cli/test_machine_client_paths.py` holds five tests (five paths).
  `tests/orchestration/test_public_api_gate_paths.py` drives four of them over HTTP (apply with
  history and push, an order of two jobs, an order naming its project, decline); mutations S12a
  and S12b turn those red (exits 0 -> 1). The fifth, "one order file started twice is refused
  naming the mission that runs it", is not driven: the docstring says it has no HTTP form because
  a client sends text, not a file (`order_already_running`). So the statement as worded (the whole
  second gate test passes again through HTTP) is not met. It would be closed by an HTTP test of
  the nearest path, for example two orders with the same text sent one after the other while the
  first runs, with the refusal token or the outcome the product chooses, or by the feature file
  stating that the fifth path stays on the command line.

Statement 17 (a write goes through the F009 door as a new command).
  Measured in `measure.txt`: the door's command set `UI_EXPOSED_COMMANDS` holds `decision.resolve`
  but not `job.decline`, `job.apply`, `client.order` or `job.run`, and no new door command was
  added. The write routes answer by `CommandRunner.run` (`serve_runs.py`, line 637), which runs
  `python -m apps.cli.main <command> --json` as a child process of the supervisor, and the order
  and run routes call `OrderLauncher.start` and `RunLauncher.start` directly. No test in
  `tests/ui_server/test_public_api.py` mentions the door. The product does not do what the
  sentence says, and nothing tests it. It would be closed either by routing the writes through the
  door with a test of that, or by an amendment that states the child-process design.

Statement 18 (a test compares each route's answer with its command's envelope).
  Nine of the eleven routes have such a test and all nine turn red under their mutation (table
  above). For `POST /api/v1/orders` and `POST /api/v1/jobs/{job}/run` the mutation also turns a
  test red (exit 0 -> 1), but that test compares the 202 answer with a literal dictionary or a
  stand-in record, not with the envelope of `remedy client order --json` or `remedy job run
  --json`; the `job.run` twin prints a different thing (the run's report), so the sentence cannot
  hold for it as worded. Closing it: a test that starts an order and a run over HTTP, then
  compares the 202 body with `remedy client order <id> --json` and `remedy client run <job>
  --json` run against the same data root, and an amendment that names the run route's twin as
  `client.run`.

Statement 21 (another user of the same machine reaches the port).
  The port is a loopback TCP port and `serve.token` is readable by its owner only, so another user
  needs a client token. No test sends a client token to the supervisor's API port: the client-
  token tests use the cockpit handler or the socket handler class. Mutation S22b makes the port's
  handler refuse every client token; the 38 tests selected by `-k "client_token or client_order or
  client_write or client_apply or api_port or post_on_the_api or run_post_on_the_port"` over both
  test files stay green (control 0, mutated 0). It would be closed by an HTTP test that writes
  `api/clients.json` under a scratch root, starts the supervisor and reads a route and is refused
  a write outside the policy with the client token on the port.

Statement 23 (nothing adds TLS or a remote story).
  A negative claim with no test. `measure.txt` counts no `ssl`/`tls` use in the listener code (the
  pattern `https` only matches the class name `ThreadingHTTPServer`), so the product meets it
  today, but nothing would turn red if a TLS wrapper or a non-loopback option were added (the bind
  test pins the address only, statement 22). It would be closed by a test that reads the listener
  setup and fails on any `ssl` import or any configuration key that names a bind address.

Statement 32 (the contract document says how a client's test starts the supervisor).
  The section `## A client's test` of `docs/system/public-http-api-v1.md` states
  `REMEDY_DATA_DIR`, `REMEDY_SERVE_API_PORT=0`, `remedy serve start --json`, the `api_port` key,
  the token file, `remedy project register` and `remedy serve stop --json`. Mutation S32 cuts the
  section out and runs the 12 page tests of `tests/ui_server/test_public_api.py` (`-k page`):
  control 0, mutated 0. Only the environment variable name is pinned, by another section. It would
  be closed by a test that reads the section and checks each command, variable and file name in it
  against `tests/orchestration/test_public_api_gate_paths.py`'s `supervisor` fixture.

Statements: 32. PROVED: 23 (of them PROVED (HTTP): 10). MOVED: 3. GAPS: 6.
