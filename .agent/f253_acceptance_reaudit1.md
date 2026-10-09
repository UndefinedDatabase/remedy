# F253 acceptance re-audit 1 (amend0930b-slow-cap hardening stage)

Commit audited: ea8f3e9af70702c7ec88e4a37ac7dead4c252a5d, branch feature/f253-public-http-api.

## What I read

- AGENTS.md, `docs/roadmap/features/T12_F253.md` (all of it, amendment sections included),
  `docs/system/public-http-api-v1.md`.
- Production code: `packages/orchestration/public_api.py` (whole), `serve_daemon.py` (listener,
  handler classes), `serve_runs.py` (`OrderLauncher`, `CommandRunner`), `ui_server.py`
  (`_public_api_caller`, `_send_public_api_*`), `config.py` (`serve.api_port`).
- Tests: `tests/orchestration/test_public_api_gate_paths.py` (whole), `tests/ui_server/test_public_api.py`
  (registry, read-route, write-route, 202 and page tests), `tests/orchestration/test_serve_daemon.py`
  (S6a port, S4a/b/c writes, client-token test, S7a run).
- Not read: `.agent/handoff.md`, `.agent/live_review.md`, `.agent/decisions.md`, `.agent/authored/`,
  `.agent/f253_acceptance_audit.md`, any other review record.

## How the mutations ran

- Disposable worktree `/home/decodeux/Repos/remedy/.remedy-wt/f253-reaudit1-wt` (detached at the audited commit).
  Scripts and every full output are in `/home/decodeux/Repos/remedy/.remedy-wt/f253-reaudit1/`
  (`common.py` is the runner; `control*.py`, `s12.py`, `s17.py`, `s18.py`, `s21_23_32.py`,
  `real_supervisor.py` are the drivers; `<name>.txt` is the whole output of each run).
- Each run: `python3 -B -m pytest -p no:cacheprovider -v --basetemp <short dir under the scratch folder> <nodes>`
  with `cwd` and `PYTHONPATH` on the worktree, `TMPDIR` on the scratch folder, no `-n`, one run at a
  time. The runner asserts the mutated text occurs exactly once (else the run is void), applies it,
  runs, and restores the file bytes in a `finally`. After the last run `git status --porcelain` in the
  worktree was empty (every file restored) and in the primary checkout was empty.
- Controls (unmutated, same worktree, run first): `control-12.txt`, `control-18-reads.txt` (exit 0
  each); `control-17-18-writes.txt`, `control-21-23-32.txt` (exit 0 on the second try, see Deviations).
- A mutation counts as RED only when the named test node FAILED on an assertion about the thing
  mutated; I read the failure line of each.
- Product-level proof: `real_supervisor.py` starts a real `remedy serve start --json` child (from the
  worktree, scratch data root, `REMEDY_SERVE_API_PORT=0`), writes `api/clients.json`, and speaks HTTP to
  the printed port with the server token and with a client token; output in `real_supervisor.txt`.

## Results

| # | Claim | Test node(s) | Mutation (file and exact change) | Control exit | Mutated exit | Verdict |
|---|---|---|---|---|---|---|
| 12 | F298's second gate test passes again through HTTP alone (five paths) | `tests/orchestration/test_public_api_gate_paths.py`, five nodes, see sub-table | see sub-table | 0 | 1 (each of five) | PROVED |
| 17 | A write goes through the F009 door as a new command, as amended by D21: every write runs its CLI twin as a child of the supervisor and answers its envelope | `test_serve_daemon.py::test_a_post_on_the_api_port_answers_what_the_resolve_command_prints`, `::test_a_decline_post_answers_what_the_decline_command_prints`, `test_public_api.py::test_a_post_builds_the_command_line_from_the_body_and_the_path` | (a) `public_api.py`: `envelope = run_command(_job_lock_key(segments["job"]), argv)` replaced by `envelope = {"schema_version": 1, "ok": True}`; (b) `serve_runs.py` `CommandRunner.run`: `[*self._prefix, *argv]` replaced by `[*self._prefix, "client", "interface", "--json"]`; (c) `public_api.py` `_decision_resolve_argv` returns `["client","interface","--json"]` | 0 | (a) 1, three of three FAILED; (b) 1, two of two FAILED; (c) 1, the decision test FAILED (decline test stays green, as it should: it is another route) | PROVED as amended (see note 1) |
| 18 | Every route calls its twin's function and a test compares each route's answer with its command's envelope | see sub-table (11 routes) | see sub-table | 0 | 1 for ten routes, 0 for the apply success answer | GAP (apply, success answer only) |
| 21 | The supervisor serves the API on a localhost port the configuration names, beside its socket, so another user reaches it, with a client token | `test_serve_daemon.py::test_a_client_token_on_the_port_reads_a_route_and_is_refused_a_write_outside_its_policy`; `::test_run_supervisor_without_the_keyword_reads_serve_api_port_from_configuration`; real `remedy serve start` run | (a) `serve_daemon.py`: `_PublicApiHandler` gets a `_public_api_caller` override that refuses client tokens; (b) `serve_daemon.py`: `resolved_api_port = get_config().get("serve.api_port")` replaced by `resolved_api_port = None` | 0 | (a) 1, `assert 401 == 200`; (b) 1, `assert (False)`; real run: client token 200 unmutated, 401 under (a) | PROVED |
| 23 | Nothing is bound beyond localhost, and nothing here adds TLS | `test_serve_daemon.py::test_the_api_listener_binds_127_0_0_1_only`, `::test_the_supervisors_listener_source_imports_no_ssl_and_binds_127_0_0_1_only` | (a) `serve_daemon.py`: `("127.0.0.1", resolved_api_port),` replaced by `("0.0.0.0", resolved_api_port),`; (b) `serve_daemon.py`: `import ssl` added after the `ThreadingHTTPServer` import | 0 | (a) 1, both FAILED; (b) 1, the source test FAILED; real run under (a): listening address 00000000 instead of 0100007F | PROVED for the bind and for `serve_daemon.py`; narrow scope limit, see note 2 |
| 32 | The contract document says how a client's test starts the supervisor | `tests/ui_server/test_public_api.py::test_the_clients_test_section_names_what_the_gate_tests_fixture_uses` | `docs/system/public-http-api-v1.md`: (a) heading `## A client's test` renamed; (b) `the file `serve/serve.token` under the scratch folder` replaced by `the token file under the scratch folder`; (c) `` `remedy serve stop --json` `` replaced by `` `remedy serve stop` ``; (d) `` `REMEDY_SERVE_API_PORT` set to `0` `` replaced by `a port variable set to `0`` | 0 | 1 for each of (a) to (d) | PROVED |

### Claim 12, the five paths (each mutation in the production code, each node run alone)

| Path | Test node | Mutation | Control | Mutated | Reading |
|---|---|---|---|---|---|
| apply with history and push | `test_a_result_is_applied_with_its_history_and_pushed_to_the_upstream_over_http` | `public_api.py` `_JOB_APPLY_FLAGS`: drop `"push"` | 0 | 1 | `(pushed, ...) == (True, 'origin', ...)` false, `pushed` False |
| (same, history half) | same | `_JOB_APPLY_FLAGS`: drop `"commit_with_history"` | 0 | 1 | 400 `invalid_argument` (`--push` alone), assert 400 == 200 |
| order of two jobs | `test_an_order_of_two_jobs_is_driven_to_its_end_from_the_answers_alone_over_http` | `public_api.py` `_ORDER_CREATE_FLAGS`: drop `"force_mission"` | 0 | 1 | `ValueError: not enough values to unpack (expected 2, got 1)` |
| one order file started twice, refused naming its mission | `test_one_order_sent_twice_with_one_key_is_refused_naming_the_mission_that_runs_it_over_http` | `public_api.py`: `if order_key is not None and not checked.get("new_mission"):` replaced by `if False:` | 0 | 1 | `assert 202 == 409` |
| order naming its project | `test_an_order_naming_its_project_is_applied_in_that_projects_repository_over_http` | `serve_runs.py` `OrderLauncher.start`: the `project:` header line is stripped from the text written to `order.md` | 0 | 1 | red by timeout: the order never ended within the test's 180 s poll (185 s run); no process was left behind (checked) |
| declined result | `test_a_completed_result_is_declined_over_http_and_waits_for_nothing` | `public_api.py` `_job_decline_argv`: `--reason={body.get('reason', '')}` replaced by `--reason=` | 0 | 1 | 400 `missing_argument`, assert 400 == 200 |

All five tests drive a real `remedy serve start --json` child over HTTP (`Supervisor.request` to
`127.0.0.1:<api_port>` with the token read from `serve/serve.token`); the only non-HTTP step is
`remedy project register --repo`, which the contract page documents as the way a client's test
registers a repository. The docs/system page and the test docstring both name this.

### Claim 18, the eleven routes (extra key `zz` added to the answer, or the answer diverged, in production code only)

| Route | Test node | Mutation | Control | Mutated | Verdict |
|---|---|---|---|---|---|
| GET `/api/v1/interface` | `test_public_api.py::test_interface_route_answers_the_command_envelope` | `build_ok(zz=1, **build_client_interface())` | 0 | 1 | PROVED |
| GET `/api/v1/digest` | `::test_digest_route_answers_the_status_commands_client_object` | `build_ok(zz=1, **build_client_digest(...))` | 0 | 1 | PROVED |
| GET `/api/v1/jobs/{job}/proof` | `::test_proof_route_answers_the_change_proof_command` | `build_ok(zz=1, **export_proof_chain_json(chain))` | 0 | 1 | PROVED |
| GET `/api/v1/changes` | `::test_changes_route_answers_the_client_changes_command` | `build_ok(zz=1, **build_client_changes(parsed_since))` | 0 | 1 | PROVED |
| POST `/api/v1/jobs/{job}/decisions/{decision}` | `test_serve_daemon.py::test_a_post_on_the_api_port_answers_what_the_resolve_command_prints` | after `run_command`, for twin `decision.resolve` add key `zz` to the envelope | 0 | 1 | PROVED |
| POST `/api/v1/jobs/{job}/decline` | `::test_a_decline_post_answers_what_the_decline_command_prints` | same, twin `job.decline` | 0 | 1 | PROVED |
| POST `/api/v1/jobs/{job}/apply`, refusal envelope | `::test_an_apply_post_refuses_as_the_command_does_or_before_it` | same, twin `job.apply`, any envelope | 0 | 1 (refusal test FAILED, success test PASSED) | PROVED for the refusal |
| POST `/api/v1/jobs/{job}/apply`, SUCCESS envelope | `::test_an_apply_post_lands_one_commit_in_the_jobs_own_repository` and the refusal test | same, only when `envelope.get("ok")` | 0 | 0 (both PASSED) | GAP |
| GET `/api/v1/orders/{order}` | `test_public_api.py::test_the_order_poll_route_answers_as_the_client_order_command_does` | `build_ok(zz=1, **order_record_payload(paths, record))` | 0 | 1 | PROVED |
| POST `/api/v1/orders` 202 | `::test_the_order_create_202_answer_equals_what_client_order_prints` | `202, build_ok(zz=1, **order_record_payload(serve_paths(), record))` | 0 | 1 | PROVED |
| GET `/api/v1/jobs/{job}/run` | `::test_the_run_poll_route_answers_as_the_client_run_command_does` | `build_ok(zz=1, **run_record_payload(paths, record))` | 0 | 1 | PROVED |
| POST `/api/v1/jobs/{job}/run` 202 | `::test_the_run_202_answer_equals_what_client_run_prints` | `202, build_ok(zz=1, **run_record_payload(serve_paths(), record))` | 0 | 1 | PROVED |

## Gaps

1. **Claim 18, POST `/api/v1/jobs/{job}/apply`, success answer.** No test compares an applied
   route answer with `remedy job apply --json`'s success envelope. `test_an_apply_post_refuses_as_the_command_does_or_before_it`
   compares the full refusal (`job_not_ready`) with the command's, and
   `test_an_apply_post_lands_one_commit_in_the_jobs_own_repository` and the gate path assert a handful of
   keys (`ok`, `status`, `job_id`, `commit_sha`, `files_applied`, `pushed`, ...). `_apply_command_envelope`
   is used only on the refusal. Mutation `m18-apply-ok-only` (an extra key `zz` added to every ok apply
   envelope) leaves both apply tests green (`m18-apply-ok-only.txt`, exit 0). So the statement "a test
   compares each route's answer with its command's envelope" holds for ten of eleven routes and for
   apply only on its refusal; a success answer that diverged from the command's in a key no test reads
   would not fail the suite. The same is true in spirit of the decision and decline success tests, which
   exclude `job_id`, `decision_id`, `next_command` / `declined_at` from the comparison (named in the tests),
   but those compare everything else and were proven red.
2. **Claim 23, TLS scope (narrow, not blocking the bind).** The only test of "no TLS" reads
   `serve_daemon.py` alone. Adding `import ssl` to `public_api.py` (`m23c-import-ssl-in-public-api.txt`)
   leaves that test green (exit 0), and no other test greps for `ssl` in the API code. The bind half is
   fully pinned (a behavioural test and an AST test on every `ThreadingHTTPServer` call in `serve_daemon.py`),
   and `ui_server.py` refuses a non-localhost host in code, but a TLS story added outside `serve_daemon.py`
   would not fail a test.

Notes:

1. Claim 17. As amended by DECISION F253 D21 the product meets the statement: every write under
   `/api/v1` (decision, decline, apply) runs its CLI twin as `python -m apps.cli.main ...` through
   `CommandRunner.run` and answers its envelope; the order and the run are started by the supervisor's
   `OrderLauncher` and `RunLauncher`. The literal F009-door-as-new-command wording is NOT met and is not
   claimed; the amendment records that and says the operator may overturn it. Mutations (a), (b), (c)
   show the suite fails if a write stops running its twin, on a stub runner (`calls ==` test) and on the
   real child process (stored decision answer and envelope comparison).
2. Claim 21. A client token (from `api/clients.json`) on the real supervisor's port: 200 on
   `/api/v1/interface` and `/api/v1/digest`, 404 `invalid_job_id` (the twin's own refusal, past the policy
   check) on a decline of an unknown job; the ledger names `other-user` on those lines; a wrong token is 401.
   Under mutation (a) the same client token is 401 on all three.
3. Claim 12 mutation for "order naming its project" is red through a hang (the child order never ends),
   not through an assertion on the answer; it fails the test as designed but a sharper assertion would
   fail faster.

## Real-product run (`real_supervisor.txt`)

    control: ready api_port=33679, listening 0100007F (127.0.0.1)
      server token GET interface -> 200; client token GET interface -> 200, GET digest -> 200;
      wrong token -> 401 api_token_invalid; client POST decline unknown job -> 404 invalid_job_id;
      ledger clients ["", "other-user", "other-user", "", "other-user"]; serve stop exit 0
    mutation 21a: client token -> 401 api_token_invalid on interface, digest and the POST; ledger clients all ""
    mutation 23a: listening 00000000 (all interfaces) instead of 0100007F

## Deviations from the instructions

- I used `cd ... 2>/dev/null;` once in a Bash call (to the scratch folder `f253-reaudit1`, not the
  worktree) before a `grep`; no state depended on it.
- I used pipes in several read-only inspection commands (`grep ... | cut`, `| head`, `| sed`); none
  touched the worktree or ran tests. One early compound command with a shell variable and one `ps | grep`
  were refused by the tool and replaced by scripts (`procs.py`).
- The first control runs of the 17/18-write and 21/23/32 groups errored at setup (basetemp path made the
  unix socket path 105 bytes, limit 103); I shortened the basetemp (`common.py`) and re-ran those two
  controls, which then passed. `control-12` and `control-18-reads` ran under the first, longer basetemp
  and passed; their outputs are `control-12.txt` and `control-18-reads.txt`.
- The scratch folder `f253-reaudit1/` (scripts, outputs, `b/`, `rs/`, `scratch/`) sits inside
  `.remedy-wt/` of the primary checkout, which git does not list (status was empty). No file under `/tmp`
  or `.data` was written or read.
- No commit, push or branch was made.

## Worktree removal

`git -C /home/decodeux/Repos/remedy worktree remove --force /home/decodeux/Repos/remedy/.remedy-wt/f253-reaudit1-wt`
succeeded. `git worktree list` afterwards shows the primary checkout (ea8f3e9af, feature/f253-public-http-api)
and the thirteen pre-existing `.remedy-wt/job-*` worktrees; `f253-reaudit1-wt` is gone. `git status --porcelain`
in the primary checkout is empty.
