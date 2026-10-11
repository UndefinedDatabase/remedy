# Public HTTP API v1

> Status (F253, accepted 2026-10-09): built. Every route served today is listed below; F303
> adds the shipped cockpit's migration to this API and the MCP facet (`docs/roadmap/features/T12_F303.md`).

The public HTTP API is the interface through which a program drives Remedy over HTTP instead of
its command line. Each route answers exactly what its twin command answers with `--json` —
the same operations `docs/system/machine-client-contract-v1.md` describes for the command line,
reached over a socket instead of a process.

## Where it is served

Two servers answer this namespace: the cockpit's own server, started by `remedy ui start`, and the
supervisor's unix socket, which `remedy serve start` opens. Both are bound to this machine only;
neither is reachable from another host. With `serve.api_port` set in `remedy.toml`, or
`REMEDY_SERVE_API_PORT` in the environment, `remedy serve start` also answers this API on
`127.0.0.1` at that port, and nothing but this API there; `0` lets the system pick a free port.
`remedy serve status --json` names the port under `api_port`, and the token is the same
`serve.token` file the socket uses. This port, like the socket, is never bound beyond this
machine.

## The token

Every route under `/api/v1` takes its token in the `Authorization` header, as
`Authorization: Bearer <token>`, never in the query string — a token in the query is refused.
The supervisor's token is the file `serve.token` in the `serve` folder of the data root, readable
by its owner only. The cockpit's token is the one its start printed.

A program can be given a token of its own, called a client token. The operator writes it into
`clients.json` in the `api` folder of the data root, beside `calls.jsonl`. The file holds one
object whose one key `clients` is a list, and each entry names a client, its token, the projects it
may order work on, the largest number of model tokens and of provider calls an order may spend
(`null` for no limit) and whether it may approve a result into the repository:

    {"clients": [{"name": "nightly-bot", "token": "<at least 32 characters>",
                  "projects": ["demo"], "max_total_tokens": 200000,
                  "max_provider_calls": 40, "may_apply": false}]}

A project is written by its slug or its id, and no two entries share a name or a token. The file
must be readable by its owner only; a file that group or others can read or write counts as
holding no client. It is read again at every call, so an edit, a new client or a removed one takes
effect at the next call. A file that is missing, that cannot be read, that is not JSON, or that
holds anything outside this shape counts as holding no client at all, and the server's own token
keeps working. A client token reads every route the server's token reads and is accepted under
`/api/v1` alone: the cockpit's other routes refuse it as they refuse a wrong token.

## The envelope and its refusals

A route's success is its twin command's own `--json` answer: `{"schema_version": 1, "ok": true,
...}` — or, for a route whose table row below names a key under "Answers as", that key's value
alone, as the whole body of the envelope. A path may hold a segment written in braces, such as
`{job}`; it stands for one value the caller supplies, such as a job id or its own prefix, exactly
as the command line accepts it. Such a value may be percent-encoded, as `td%3A...` for `td:...`;
it is decoded before it is used. A refusal carries `{"schema_version": 1, "ok": false, "error":
"<token>", "message": "<sentence>"}`; a missing or wrong token answers 401 with
`api_token_invalid`; a path this registry does not name answers 404 with `api_route_not_found`. A
query key in a route's table row is either a flag, whose value is `true` or `false`, or a key
that takes one value, written `key=<value>` in the table; either kind is given at most once, and
a value is never empty. A query key a route's table row does not list, a key given more than
once, a flag's value other than `true`/`false`, or an empty value for a key that takes one,
answers 400 with `api_query_invalid` (DECISION F253 D2 (2), D5 (1)); and every other refusal a
route answers is one its table row's `Refusals` column names, sharing its HTTP status, its
`error` token and its `message` sentence with the route's own twin command. `PUT` and `DELETE`
under `/api/v1` answer 401 with `api_token_invalid` without the token, and 405 with
`api_method_not_allowed` with it; each such request is written to the ledger below like any
other. A `POST` is a write, and the next section says how a write is answered.

## Writes

A write is a `POST`. Only the supervisor that `remedy serve start` starts answers writes, on its
socket and on its port; the cockpit's own server answers every `POST` under `/api/v1` with 405 and
`api_method_not_allowed`. The body of a write is a JSON object that holds only the keys the
route's table row names under "Query or body", each of the kind the row gives: `string` is one
string, `strings` is a list of non-empty strings, and `flag` is `true` or `false`, where `true`
passes the command's option of that name and `false` passes nothing; no body at all is the empty
object, and a write takes no query string. The supervisor runs the twin command as a process of
its own and answers that command's own envelope, so a refusal carries the command's own token and
message. The statuses are the ones the table row's `Refusals` column names, and any other refusal
answers the status the row gives after "any other", which is 409. A body the supervisor cannot
read, or one larger than 64 kilobytes, answers 400 with `api_body_invalid`; a path value that
begins with `-`, or that holds `/` or a NUL character once decoded, answers 400 with
`api_path_invalid`, because no job or decision id does; an apply of a job whose record names no
repository answers 409 with `api_job_repository_unknown`, because the API applies only to the
repository a job's own record names and never to one the caller chooses; and a command that
prints no answer within 120 seconds answers 500 with `api_command_failed`. The supervisor runs one
command for a job at a time, so a second write for that job waits for the first. `PUT` and
`DELETE` still answer 405.

A client token (see "The token") is refused with 403 and `api_client_policy_refused` when an order
names a project outside the client's projects, when an order's header does not name a
`max-total-tokens:` or a `max-provider-calls:` the client has a limit for, or names a larger one,
and when it asks to apply a result and the client may not approve one; nothing is run. A client
token may also answer a decision, decline a result or apply a job only for a job of one of its
projects, and when it answers a budget decision it may not raise `max_total_tokens` or
`max_provider_calls` above its own limits; otherwise the call is refused the same way and nothing
is run.

## The ledger

Every request under `/api/v1`, a refused one included, appends one line to `api/calls.jsonl`
under the data root, with seven fields: `ts`, `token_fp`, `client`, `method`, `path`, `status` and `error`.
The caller's token is kept only as its fingerprint, never itself, and the query string is never
written at all. `client` is the name of the client whose token the call presented, and is empty for
the server's token and for a refused one. A line that cannot be written changes nothing in the answer sent.

## The version rule

The major number is in the path. Inside `/api/v1` a route, an answer key or a refusal token is
only ever added, and each addition raises the minor number of the registry's version. A route
that is to go is first marked deprecated, which makes it answer the header `Deprecation: true`
and shows it in the table below; it is removed only under a new major path.

## Orders

`GET /api/v1/orders/{order}` polls an order by the id a `POST` to `/api/v1/orders` answered:
`state` reads `running`, `ended` or `lost` and `answer` holds what `remedy do` printed, exactly as
`remedy client order <order> --json` reads them. An order id this registry's own shape rejects, or
one no record names, answers 404 with `order_not_found`. A poll that finds the order's process gone
and no end in its record reads the record again for up to two seconds, because the supervisor writes
an end only after the process has finished, and answers `ended` once the end is there, `lost`
otherwise.

`POST /api/v1/orders` starts an order through the supervisor's own `OrderLauncher`, the way
`remedy do run <options> --no-ui --yes -- order.md` would inside its own folder under the data
root, and answers 202 with its record read exactly as the route above reads it. Its body's `order`
is the order file's whole text, header included, and is required, answering 400 with
`api_body_invalid` when it is missing; a broken header or an empty order answers 400 with the
parser's own token, `order_file_invalid_header` or `order_file_empty`; `no_llm`, `new_mission`,
`force_job` and `force_mission` pass their `remedy do` flag when `true`, and `builder_provider`,
`reviewer_provider` and `deadline` pass their option with their value. An order whose header names
no project, or one that names a project this machine does not register as exactly one, is refused
before anything starts, with 409 `api_order_project_unknown` — because the order would otherwise
run in a folder nobody chose; every other refusal is `remedy do`'s own, read back only once the
order is polled. When the order's child process cannot be started at all, nothing is left behind:
the order's folder is removed and the call answers 500 with `api_command_failed`.

Two orders sent at once both run: the supervisor starts each as it arrives and keeps no waiting
line, so the second never waits for the first to end, and the route refuses neither order for the
other. Remedy sets no limit on how many orders run at once (DECISION F253 D15).

An order may carry a key, the body key `order_key`: one to 64 letters, digits, `.`, `_` or `-`,
beginning with a letter or a digit; any other value answers 400 `api_body_invalid`. The supervisor
keeps the text of an order with a key in a file named for the key, and the order runs from a link to
that file, so the record's `order_file` names the key's file. An order whose key's file a mission
that has not ended records is refused before anything starts with 409 `order_already_running`, the
mission's id under `mission_id`, so a program that sends the same order again with the same key, for
example after a lost answer, does not start the work twice. With `new_mission` set to `true` the
order starts another mission anyway. An order without a key is started again when it is sent again:
Remedy does not recognise a resent order that has no key. Two orders with one key sent close
together may both start, as two `remedy do` of one order file may.

## Runs

`POST /api/v1/jobs/{job}/run` starts the run of a job, the way `remedy job run` does, and answers
202 with the run's record: `job_id`, `pid`, `started_at`, `out_log`, `err_log`, and `exit_code` and
`ended_at`, which are `null` until the run ends, and `state` and `answer`, read as the poll below
reads them. Its body takes `builder_provider` and
`reviewer_provider`, each a string that names the model that builds or the one that reviews; either
may be left out. No other option of `remedy job run` is offered over HTTP: each other one either
raises a limit, which a client token's ceilings bound only at the order, or runs a command of the
caller's choice. A job id prefix is accepted, and the run starts under the job's full id.

Before anything starts, the job is read: a value that is no job id answers 404 `invalid_job_id`; a
well-formed id that no job has, or a job whose record cannot be read, answers 404 `job_not_found`;
a prefix that matches several jobs answers 400 `ambiguous_job_id`; and a client token's job
outside its projects answers 403 `api_client_policy_refused`, as for every write on a job. A job
whose run has not ended answers 409 `job_already_running`, and a run that cannot start answers 500
`api_command_failed`.

The route answers when the run has started, not when it ends. A client polls `GET
/api/v1/jobs/{job}/run` until `state` is not `running`, and only then reads the digest or applies,
because the digest can read a job `completed` a moment before the run that finished it has ended.
The poll answers what `remedy client run <job> --json` answers: the record, `state` (`running`,
`ended` or `lost`) and `answer`, which is `null` while the run is `running` and afterwards holds
what `remedy job run --json` printed. A poll that finds the run's process gone and no end in its
record reads the record again for up to two seconds, because the supervisor writes an end only after
the process has finished, and answers `ended` once the end is there, `lost` otherwise. An unknown
job, or a job with no run, answers 404 `run_not_found`. The supervisor
hands the one launcher that starts runs to its socket and to its port alike, so both answer from
one list of runs; a server that has no such launcher, the cockpit's own among them, answers the
route 405 `api_method_not_allowed` (DECISION F253 D18).

## A client's test

A program's own test can start a real supervisor and drive this API against it. Set two
environment variables for the child process: `REMEDY_DATA_DIR`, a scratch folder whose path is
short (a unix socket path has a length limit), so the test never touches the data of the machine,
and `REMEDY_SERVE_API_PORT` set to `0`, so the system picks a free port. Run `remedy serve start
--json` as a child process in a folder of its own. It prints one line as soon as it answers, the
envelope `remedy serve status --json` prints, and the key `api_port` holds the port; the token is
the file `serve/serve.token` under the scratch folder. Register each repository the test orders
work on with `remedy project register --repo <repo> --json`, run from a folder that is no
repository, because an order names its project. From then on every request goes to `127.0.0.1` at
that port with `Authorization: Bearer <token>`. When the test ends, whether it passed or failed, run
`remedy serve stop --json` with the same environment and wait for the child to end.

An order sent with `no_llm` and both providers set to `fake`, and a run started with both
providers set to `fake`, run without any model: the fake builder and reviewer answer, so such a test
costs nothing and needs no key. This repository's own test of it, which drives an order to its
proof, an apply with its history and a push, an order of two jobs, an order that names its project,
a declined result, and an order sent twice with one key over this API alone, is `tests/orchestration/test_public_api_gate_paths.py`.

## Staying current

A client reads `/api/v1/digest` once and then follows `/api/v1/changes`, with its `since` query
key set to the `cursor` each answer gives, to stay current without reading the whole digest
again.

## Why some commands are never published

The exclusion list below names operator-console commands: commands that change or recover this
machine, its configuration or its queue. They are excluded from this API by name, and the list
may only grow.

<!-- BEGIN GENERATED by render_public_api_markdown() -->
## Routes

> GENERATED from `PUBLIC_API_ROUTES` in `packages/orchestration/public_api.py`. Do not
> edit this section by hand: a test fails whenever the registry and this section differ.
> Regenerate it from the repository root with
> `python3 -c "from packages.orchestration.public_api import write_public_api_page; write_public_api_page()"`.

API version: `1.11`.

| Method | Path | Query or body | Answers as | Refusals | Deprecated | Description |
|---|---|---|---|---|---|---|
| `GET` | `/api/v1/interface` | — | `remedy client interface --json` | — | no | What a program that drives Remedy can rely on: its operations, arguments, exit codes, state words, templates and budget kinds, as `remedy client interface --json` prints it. |
| `GET` | `/api/v1/digest` | `all_ended_jobs` | `remedy status run --json`, its `client` object | — | no | The digest a program reads about once a minute: every project with its missions, the jobs that still need something and the last ended ones, every open decision and the jobs waiting for their apply, as the `client` object of `remedy status --json` holds it; `all_ended_jobs=true` lists every ended job, as `--all-ended-jobs` does. |
| `GET` | `/api/v1/jobs/{job}/proof` | — | `remedy change proof --json` | `invalid_job_id` 404, `job_not_found` 404, `ambiguous_job_id` 400 | no | The proof of one job: what each change rests on and where its evidence is, as `remedy change proof <job> --json` prints it; a job id prefix is accepted, as on the command line, and the command's `--path` filter is not offered over HTTP. |
| `GET` | `/api/v1/changes` | `since=<value>` | `remedy client changes --json` | `invalid_cursor` 400 | no | What changed since a cursor: the jobs and decisions as the digest shows them, the decisions answered, the missions and the applies, with the cursor for the next read, as `remedy client changes --since <cursor> --json` prints it; without `since` only a cursor is given. |
| `POST` | `/api/v1/jobs/{job}/decisions/{decision}` | `reason` (string), `answer` (strings) | `remedy decision resolve --json` | `invalid_job_id` 404, `job_not_found` 404, `decision_not_found` 404, `stop_reason_not_found` 404, `proposed_task_not_found` 404, `ambiguous_job_id` 400, `invalid_argument` 400, `missing_argument` 400, `option_not_applicable` 400, `answer_parse_error` 400, `invalid_budget` 400, `decision_not_resolvable` 400, any other 409 | no | Answers one decision of a job, as `remedy decision resolve <job> <decision> --json` does: `reason` is given as `--reason` and each `answer` as one `--answer`; a job id prefix is accepted, as on the command line, and `--as-mission` is not offered over HTTP. |
| `POST` | `/api/v1/jobs/{job}/decline` | `reason` (string) | `remedy job decline --json` | `invalid_job_id` 404, `job_not_found` 404, `ambiguous_job_id` 400, `missing_argument` 400, any other 409 | no | Declines a completed job's result, as `remedy job decline <job> --reason <reason> --json` does: nothing is applied and the decline is kept on the job, recorded as coming through `api`; a job that is not completed, or whose result already landed, is refused with 409. |
| `POST` | `/api/v1/jobs/{job}/apply` | `commit` (string), `commit_auto` (flag), `commit_with_history` (flag), `push` (flag), `skip_blocked` (flag) | `remedy job apply --json` | `job_not_found` 404, `invalid_argument` 400, any other 409 | no | Approves a completed job's result and applies it to the repository the job's own record names, as `remedy job apply <job> --repo <that repository> --approve --json` does: `commit` is given as `--commit`, and each of `commit_auto`, `commit_with_history`, `push` and `skip_blocked` set to `true` as its option; a job id prefix is accepted; `--repo`, `--test-command` and `--dry-run` are not offered over HTTP, and a job whose record names no repository is refused with 409 `api_job_repository_unknown` before any command runs. |
| `GET` | `/api/v1/orders/{order}` | — | `remedy client order --json` | `order_not_found` 404 | no | Polls the order a `POST` to `/api/v1/orders` started, as `remedy client order <order> --json` does: `state` reads `running`, `ended` or `lost`, and `answer` holds what `remedy do` printed once the order is not `running`. |
| `POST` | `/api/v1/orders` | `order` (string), `no_llm` (flag), `new_mission` (flag), `force_job` (flag), `force_mission` (flag), `builder_provider` (string), `reviewer_provider` (string), `deadline` (string), `order_key` (string) | `remedy client order --json` | — | no | Starts an order through the supervisor's own `OrderLauncher`, the way `remedy do run <options> --no-ui --yes -- order.md` would inside its own folder under the data root, and answers 202 with its record read exactly as the route above reads it. `order` is the order file's whole text, header included, and required; `no_llm`, `new_mission`, `force_job` and `force_mission` each pass their `remedy do` flag when `true`; `builder_provider`, `reviewer_provider` and `deadline` each pass their option with their value. An order whose header names no project, or one that names a project `select_project` cannot resolve to exactly one, is refused before anything starts with 409 `api_order_project_unknown`; every other refusal is `remedy do`'s own, read back only once the order is polled. `order_key` names the order with a key the client chooses, one to 64 letters, digits, `.`, `_` or `-`, beginning with a letter or a digit, any other value answering 400 `api_body_invalid`; an order with a key whose order file a mission that has not ended records is refused before anything starts with 409 `order_already_running`, the mission's id under `mission_id`, unless `new_mission` is `true`, and the record's `order_file` then names the key's file. |
| `GET` | `/api/v1/jobs/{job}/run` | — | `remedy client run --json` | `run_not_found` 404 | no | Polls the run the `POST` to this path started, answering the run's record as `remedy client run <job> --json` does: the record's keys, `state` and `answer`. A client polls it until `state` is not `running`: `state` reads `running`, `ended` or `lost`; `exit_code` is `null` until the run ends and stays `null` for a run read `lost`; `answer` is `null` while the run is `running` and afterwards holds what `remedy job run --json` printed, or `null` when it printed no envelope. A job id prefix is accepted; a value that names no one job, or a job with no run, is refused with 404 `run_not_found`. |
| `POST` | `/api/v1/jobs/{job}/run` | `builder_provider` (string), `reviewer_provider` (string) | the run's record, as the supervisor's `RunLauncher` writes it | — | no | Starts a job's run through the supervisor's own `RunLauncher`, as `remedy job run <job> <options> --json` would, and answers 202 with the run's record: `job_id`, `pid`, `started_at`, `out_log`, `err_log`, `exit_code` and `ended_at`, the last two `null` until the run ends, and `state` and `answer` as the route above reads them. `builder_provider` and `reviewer_provider` each pass `--builder-provider=<value>` and `--reviewer-provider=<value>`; no other option of `remedy job run` is offered over HTTP. A job id prefix is accepted. A client waits for the run's end by polling the route above until `state` is not `running`. Refusals: `invalid_job_id` 404, `job_not_found` 404 (also for a record that cannot be read), `ambiguous_job_id` 400, `job_already_running` 409, `api_command_failed` 500 when the run cannot start, and `api_client_policy_refused` 403 for a client token's job outside its projects. |

### Never published

- `patch.apply`
- `patch.revert`
- `rollback.*`
- `snapshot.create`
- `config.set`
- `config.init`
- `init.run`
- `self-repair.proposal-approve`
- `self-repair.proposal-deny`
- `worker.unload`
- `runtime.stop`
- `ui.stop`
- `queue.rm`
- `queue.reclaim`
<!-- END GENERATED by render_public_api_markdown() -->
