# Public HTTP API v1

> Status (F253, 2026-10-08): built in part. This page lists only the routes that are served today;
> later slices of F253 add the rest (`docs/roadmap/features/T12_F253.md`).

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

## The ledger

Every request under `/api/v1`, a refused one included, appends one line to `api/calls.jsonl`
under the data root, with six fields: `ts`, `token_fp`, `method`, `path`, `status` and `error`.
The caller's token is kept only as its fingerprint, never itself, and the query string is never
written at all. A line that cannot be written changes nothing in the answer sent.

## The version rule

The major number is in the path. Inside `/api/v1` a route, an answer key or a refusal token is
only ever added, and each addition raises the minor number of the registry's version. A route
that is to go is first marked deprecated, which makes it answer the header `Deprecation: true`
and shows it in the table below; it is removed only under a new major path.

## Orders

`GET /api/v1/orders/{order}` polls an order by the id a `POST` to `/api/v1/orders` answered:
`state` reads `running`, `ended` or `lost` and `answer` holds what `remedy do` printed, exactly as
`remedy client order <order> --json` reads them. An order id this registry's own shape rejects, or
one no record names, answers 404 with `order_not_found`.

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
other. The limit on how many orders a client may send at once belongs to the client token's own
policy, not to this route (DECISION F253 D15).

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

API version: `1.7`.

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
| `POST` | `/api/v1/orders` | `order` (string), `no_llm` (flag), `new_mission` (flag), `force_job` (flag), `force_mission` (flag), `builder_provider` (string), `reviewer_provider` (string), `deadline` (string) | `remedy client order --json` | — | no | Starts an order through the supervisor's own `OrderLauncher`, the way `remedy do run <options> --no-ui --yes -- order.md` would inside its own folder under the data root, and answers 202 with its record read exactly as the route above reads it. `order` is the order file's whole text, header included, and required; `no_llm`, `new_mission`, `force_job` and `force_mission` each pass their `remedy do` flag when `true`; `builder_provider`, `reviewer_provider` and `deadline` each pass their option with their value. An order whose header names no project, or one that names a project `select_project` cannot resolve to exactly one, is refused before anything starts with 409 `api_order_project_unknown`; every other refusal is `remedy do`'s own, read back only once the order is polled. |

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
