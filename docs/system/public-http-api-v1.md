# Public HTTP API v1

> Status (F253, accepted 2026-10-09): built. Every route served today is listed below; F303
> names what the edition `remedy`, Remedy's face since 2026-10-15, needs from this API
> (`docs/roadmap/features/T12_F303.md`).

The public HTTP API is the interface through which a program drives Remedy over HTTP instead of
its command line. Each route answers exactly what its twin command answers with `--json` —
the same operations `docs/system/machine-client-contract-v1.md` describes for the command line,
reached over a socket instead of a process.

## Where it is served

The supervisor that `remedy serve start` starts answers this namespace on its unix socket. The
cockpit's own server, which `remedy ui start` once started, was deleted on 2026-10-15 (amend1015f
D3). The socket is bound to this machine only and is not reachable from another host. With `serve.api_port` set in `remedy.toml`, or
`REMEDY_SERVE_API_PORT` in the environment, `remedy serve start` also answers this API on
`127.0.0.1` at that port, and nothing but this API there; `0` lets the system pick a free port.
`remedy serve status --json` names the port under `api_port`, and the token is the same
`serve.token` file the socket uses. This port, like the socket, is never bound beyond this
machine.

## The token

Every route under `/api/v1` takes its token in the `Authorization` header, as
`Authorization: Bearer <token>`, never in the query string — a token in the query is refused.
The supervisor's token is the file `serve.token` in the `serve` folder of the data root, readable
by its owner only.

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
keeps working. A client token is accepted under `/api/v1` alone: the write door refuses it as it
refuses a wrong token. It reads and acts only on its own projects: a route that names a job (its
story, logs, proof, run, diff, and every write) or an order of another project answers 403
`api_client_policy_refused`, and the digest and what changed list only its own projects, their
missions and their jobs (since version 1.16). The server's own token reads every project.

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
`error` token and its `message` sentence with the route's own twin command. The two routes that
start work, `POST /api/v1/orders` and `POST /api/v1/jobs/{job}/run`, are the exception: what they
refuse before anything starts is their own, as the sections Orders and Runs say. `PUT` and `DELETE`
under `/api/v1` answer 401 with `api_token_invalid` without the token, and 405 with
`api_method_not_allowed` with it; each such request is written to the ledger below like any
other. A `POST` is a write, and the next section says how a write is answered.

## Writes

A write is a `POST`. Only the supervisor that `remedy serve start` starts answers writes, on its
socket and on its port; a handler without the supervisor's runner answers every `POST` under
`/api/v1` with 405 and `api_method_not_allowed`. The body of a write is a JSON object that holds only the keys the
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

**An order's jobs (version 1.18).** Both answers carry `jobs`, while the order runs and after it
ended: every job this run of the order file planned, in planned order and over every repository
it touched, read from the repositories' missions (a batch records the order file it came from and
each job link names its batch), so a client needs no job id to see what is happening. Each entry
holds `job_id`, `title` (the order's first line; sibling jobs of one order add their repository
or files), `state` (the job's own word), `phase`, `executable`, `tasks` (`total`, `done` and the
`current` task's title), `waits_for` and `waiting_reason`, `verification` (the job's verification
status) and `story` (the route of the job's story). `phase` is one of the closed words the
interface lists under `order_job_phases`: `running`; `waiting`, when the job runs only after the
job it names under `waits_for` is applied and committed, because its workspace is cut from the
repository's HEAD; `ready`, the one job that may run now (`executable`); `needs_plan_approval`;
`awaiting_apply`, a finished result nothing applied or declined yet; `applied`; `declined`;
`blocked`; `stopped`, resumable; `cancelled`, ended for good; `failed`; `checked` (since 1.20), a
job with no build task that ran only its checks, the job of an order that asked only for its tests
to run, with nothing to apply. A job whose record cannot be read is listed with state `missing`,
never left out, and an order that planned nothing yet lists none. The view is read when polled:
it is no live stream, and a client that wants to know sooner polls again.

**Stopping, cancelling and abandoning work.** `POST /api/v1/jobs/{job}/stop` pauses one job, as
`remedy job stop` does: a running job's Pi call in flight is ended within about a second
(another provider's call finishes first), it starts nothing new and stays resumable; a job that never started ends at once, `stopped`; a completed job is refused with
409 `job_not_stoppable`, because its result waits for an apply or a decline
(`POST /api/v1/jobs/{job}/decline`). A stopped job, run or not, can be resumed, so it stays among
the jobs that still need something. `POST /api/v1/jobs/{job}/abandon` ends one job for good, as
`remedy job abandon` does: `cancelled` is terminal, a cancelled job asks no decision, never runs
again and is listed among the ended jobs; a running job answers `cancel_pending` and ends
`cancelled` at its next safe point. `POST /api/v1/orders/{order}/cancel` is the one call that
abandons an order, whatever it is doing: it records the request, cancels every job of the order,
and the order's walk reads it before every step and every apply, so no job of it starts or lands
afterwards. A planner call in flight is ended, not awaited (since 1.20): the local Ollama
planner closes its own request's connection, which makes the server stop generating for it, and
the Claude CLI planner's child is ended by its execution guard; the call writes no plan (no
fallback plan either), its ledger entry reads `cancelled`, and an answer that arrives later is
discarded. Measured against a local streaming server: the call ends within one poll (0.25 s) of
the request being written. No Ollama server or other process is touched. The order's
`phase` reads `cancelling` while anything of it still runs and `cancelled` once nothing can; a
result waiting for its apply stays for the person unless the body sets `decline_results`; an
applied result is never reverted. Both cancels are idempotent and survive a supervisor restart.
A `cancel_pending` job whose process dies before its safe point (a crash, a reboot) is not left
`running`: the supervisor ends it `cancelled` when that run or walk ends, and again when it starts,
for every job a process it started could have held; a job only a run in a terminal may hold keeps
waiting for that run (R-1365, inside 1.21: no key, word or route changed).
Records, evidence and worktrees stay as the retention rules keep them: neither a stop nor a cancel
is a deletion.

`POST /api/v1/orders` starts an order through the supervisor's own `OrderLauncher`, the way
`remedy do run <options> --no-ui --run-unattended -- order.md` would inside its own folder under the data
root, and answers 202 with its record read exactly as the route above reads it. Its body's `order`
is the order file's whole text, header included, and is required, answering 400 with
`api_body_invalid` when it is missing; a broken header or an empty order answers 400 with the
parser's own token, `order_file_invalid_header` or `order_file_empty`; `no_llm`, `new_mission`,
`force_job` and `force_mission` pass their `remedy do` flag when `true`, and `builder_provider`,
`reviewer_provider` and `deadline` pass their option with their value. An order whose header names
no project, or one that names a project this machine does not register as exactly one, is refused
before anything starts, with 409 `api_order_project_unknown` — because the order would otherwise
run in a folder nobody chose. An order whose header sets no cap — none of `max-cost-usd`,
`max-total-tokens`, `max-provider-calls` and `max-wall-clock-minutes` — is refused before anything
starts with 400 `order_file_no_cost_cap` and the sentence `remedy do` refuses it with. Every other
refusal is `remedy do`'s own, read back only once the order is polled. When the order's child process cannot be started at all, nothing is left behind:
the order's folder is removed and the call answers 500 with `api_command_failed`. The refusals
this paragraph and the paragraph on keys below name are the route's own, not `remedy do`'s:
`remedy do` words the same tokens for an order file it was given by name and for its own
`--new-mission` option, so a test holds each of these answers whole (DECISION F297 D10).

Two orders sent at once both run: the supervisor starts each as it arrives and keeps no waiting
line, so the second never waits for the first to end, and the route refuses neither order for the
other. Remedy sets no limit on how many orders run at once (DECISION F253 D15).

An order may carry a key, the body key `order_key`: one to 64 letters, digits, `.`, `_` or `-`,
beginning with a letter or a digit; any other value answers 400 `api_body_invalid`. The supervisor
keeps the text of an order with a key in a file named for the key, and the order runs from a link to
that file, so the record's `order_file` names the key's file. A repository has one lasting mission,
and every order is a batch of jobs in it. An order whose key's file an earlier order still has
unfinished jobs for, in a mission that has not ended, is refused before anything starts with 409
`order_already_running`, the mission's id under `mission_id`, so a program that sends the same
order again with the same key, for example after a lost answer, does not start the work twice.
With `new_mission` set to `true` the order is accepted anyway and added as one more order to the
repository's one mission. An order without a key is started again when it is sent again:
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
`api_command_failed`. These refusals are the route's own: `remedy job run` does not read the job
before its run starts, so no command answers them, and a test holds each of these answers whole
(DECISION F297 D10).

The route answers when the run has started, not when it ends. A client polls `GET
/api/v1/jobs/{job}/run` until `state` is not `running`, and only then reads the digest or applies,
because the digest can read a job `completed` a moment before the run that finished it has ended.
The poll answers what `remedy client run <job> --json` answers: the record, `state` (`running`,
`ended` or `lost`) and `answer`, which is `null` while the run is `running` and afterwards holds
what `remedy job run --json` printed. A poll that finds the run's process gone and no end in its
record reads the record again for up to two seconds, because the supervisor writes an end only after
the process has finished, and answers `ended` once the end is there, `lost` otherwise. An unknown
job, or a job with no run, answers 404 `run_not_found`, the envelope `remedy client run <job>
--json` answers for the same value. The supervisor
hands the one launcher that starts runs to its socket and to its port alike, so both answer from
one list of runs; a server that has no such launcher answers the
route 405 `api_method_not_allowed` (DECISION F253 D18).

## Execution offer

`GET /api/v1/execution` (since 1.17) answers what this server offers an execution, read from its
own configuration when asked: each role's providers with their defaults, measured availability,
isolation and installed models, and which of them a client may choose; the lanes, order flags,
budget caps, verification statuses, review reports, phases and the routes that show a run. The
server decides: `builder_provider` and `reviewer_provider` that it does not offer (`claude-cli`,
whose Claude Code CLI runs with the host's tools outside the tool sandbox; `ollama` as a builder,
which writes no file; one that is offered but not available here) are refused by `POST
/api/v1/orders` and `POST /api/v1/jobs/{job}/run` with 400 `api_provider_not_offered` before
anything starts, never replaced by another. No route takes a test command: verification always
runs the project's own. A run's effective configuration is the job's `execution_config` in the
`job run` answer and in the review report (`docs/system/review-reports-v1.md`).

## Stories

`GET /api/v1/jobs/{job}/story` answers one job's run story, as `remedy client story <job> --json`
does, so a client can show a person what the job did in the client's own words (operator amendment
amend1015-face-migration). It is a read of what the runner wrote and changes nothing. A job id
prefix is accepted; the refusals are `invalid_job_id` 404, `job_not_found` 404 and
`ambiguous_job_id` 400, and a client token reads only a job of one of its projects (403
`api_client_policy_refused`).

The answer's keys: `order` is the person's own order text; `job_id`; `updated_at`, `started_at` and
`ended_at` are times or `null`; `state` is one of `reading`, `planning`, `queued` (since 1.19: a
planned job no process runs, which read `planning` before), `working`, `checking`, `done`,
`done_applied`, `stopped`, `failed` and `waiting`. A job stopped on request reads the reason `stopped`
since 1.19 (it read `cancelled` before, although it can be resumed). A job whose task plan the
person rejected reads `stopped` with the reason `declined`, `next` `none` and `end` `abandon`: a
rejected plan is final for its job, and the order's view reads its phase `declined` (R-1366). `state_detail` holds `file` and `round`
while `working`, `reason` while `stopped` or `failed`, `question` and `decision_id` while `waiting`,
and `changed_files` once `done` or `done_applied`, and `after_job` while `queued` behind a job of the
same order whose result has not landed. `next` holds the one next step, `action` (`apply`, `answer`,
`run`, `resume`, `retry` or `none`; a client offers `decline`, `POST /api/v1/jobs/<job>/decline`, beside `apply`), and `route`, the HTTP
operation that takes it, or `null`. `end` (since 1.21) is the way out beside it, so a client can
close every job that is still open whatever it waits for (a stopped, blocked or queued job, one
waiting for an answer or for its predecessor): `{action, route}` with `action` `decline` (`POST
/api/v1/jobs/<job>/decline`) for a completed result waiting for its apply and `abandon` (`POST
/api/v1/jobs/<job>/abandon`) for any other open job, and `null` once the job has ended (applied,
declined, failed or cancelled):

| `next.action` | `next.route` |
|---|---|
| `apply` | `POST /api/v1/jobs/<job>/apply` |
| `answer` | `POST /api/v1/jobs/<job>/decisions/<decision>` |
| `run` (since 1.19) | `POST /api/v1/jobs/<job>/run`, a queued job that waits for nothing |
| `resume` (since 1.19) | `POST /api/v1/jobs/<job>/run`, a job stopped on request |
| `none` | `null` |

Both `end` routes take the body `{"reason": "<why>"}`; `decline` refuses a missing or blank reason
with 400 `missing_argument`, `abandon` records `cancelled` when none is given. Every route, story key,
story word and order phase is listed with the version that added it, and every value change of an
existing field per version, in [api-release-matrix-v1.json](api-release-matrix-v1.json).

`retry` is in the closed list but no state names it since version 1.16: a run of a job whose task
ended blocked or failed re-attempts nothing and ends `blocked` again, and no route puts such a task
back to pending yet, so a failed job's story offers `none` rather than a step that cannot succeed.

`steps` is always the five steps `reading`, `planning`, `building`, `checking` and `finished` in that
order, each `{id, status, phrase, tokens}` with `status` one of `waiting`, `running`, `done`,
`skipped` and `failed`; `building` adds `tasks`, each `{title, status, rounds, files}`. `changes`
lists the job's result as `{path, added, removed}`. `numbers` holds `duration_s`, `tokens_in`,
`tokens_out`, `calls`, `model_turns` and `rounds`, each `null` where nothing was measured, never 0
for "unknown": the fake providers report no tokens, so a fake run's tokens read `null`. `tokens_in`
and `tokens_out` are the provider's measured totals over every model turn of every call; `calls`
counts harness invocations and `model_turns` the model responses inside them (a Pi call runs an agent
loop of many turns). A task's `proof_summary.tokens_estimated` in a job report is the size of the
task's TEXT, never usage. `verification` (since 1.17) is `{status, required}`: `status` is `passed`
or `failed` when the job's tests ran (the tasks' own test runs and the job's DoD test checks),
`not_run` when the order asked for its tests and none ran, or when a test command the tool
sandbox refused could not run (since 1.20; then never `passed`, even beside another task's passing
test, and the story's reason is `sandbox_unavailable`), `not_required` when the order asked for
none and none ran, and `pending` while the job runs; `required` says the order asked for the
tests to run. An unexecuted test is never `passed`. `note_open` is always
`false`, because no route of this API takes a steering note.

A `phrase` and a `reason` are `{key, args}`. Their keys are closed lists, and their arguments are
numbers, paths relative to the repository and, for `provider`, a provider's id word; the story
carries no sentence Remedy wrote, no path outside the repository, no command and no money figure.
The lists, with each key's arguments, are the `story` key of `GET /api/v1/interface`, and
`docs/system/machine-client-contract-v1.md` renders them under "Story words". They only grow inside
`/api/v1`.

## Diffs

`GET /api/v1/jobs/{job}/diff` answers one ended job's change as git prints it, as `remedy client
diff <job> --json` does, so a client can show a person the real change before the person applies
it (operator order amend1015-final-closure, DECISION amend1015c D5, version 1.16). It reads git and
the job's records and changes nothing; Remedy has no diff engine of its own for it.

The answer's keys: `job`, the job's id; `state`, one of `prepared` (the result waits to be
applied), `applied`, `declined`, `failed` (the job ended without a result; `files` is empty when
no commit was made) and `conflict` (the newest apply was refused because the target moved under
the result); `files`, each `{path, change, added, removed, patch, truncated}` with `change` one of
`added`, `modified`, `deleted` and `renamed`, `added` and `removed` the file's line counts (0 for a
binary file), `patch` the file's unified diff with `a/` and `b/` prefixes; and `truncated`.

A result that is not applied is `git diff <base commit> <job branch head>` in the job's own
repository; a result applied with a commit is `git diff <commit>^1 <commit>`; a plain apply commits
nothing and copied exactly the job branch's change, so its diff is that change. A file's `patch` is
cut at a line boundary after 64 KiB and the patches together stop after 512 KiB (that file's
`truncated` is `true`, and so is the answer's); the list stops after 300 files (the answer's
`truncated` is `true`). A path Remedy treats as sensitive (an environment file, a credentials file
or a key) keeps its counts but never its patch, and reads `truncated` `true`.

The refusals: `invalid_job_id` 404, `job_not_found` 404, `ambiguous_job_id` 400, `diff_not_ready`
409 for a job that has not ended or waits for an answer to a question, and `diff_unavailable` 409 when git no longer has the job's
commits. A client token reads only a job of one of its projects (403 `api_client_policy_refused`).

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

API version: `1.22`.

| Method | Path | Query or body | Answers as | Refusals | Deprecated | Description |
|---|---|---|---|---|---|---|
| `GET` | `/api/v1/interface` | — | `remedy client interface --json` | — | no | What a program that drives Remedy can rely on: its operations, arguments, exit codes, state words, templates and budget kinds, as `remedy client interface --json` prints it. |
| `GET` | `/api/v1/execution` | — | `remedy client execution --json` | — | no | What this server offers an execution, read now from its own configuration, as `remedy client execution --json` prints it: under `roles` each of `planner`, `builder`, `reviewer` and `repair` with its `default_provider` and `default_model`, whether HTTP chooses it (`selectable_over_http`), and its `providers`, each with `id`, `available` (measured: an executable found, the Ollama endpoint answering, an API key set), `offered_over_http`, `isolation`, `not_offered_reason` and the installed `models`; then `lanes`, `order_flags`, `budgets`, `verification`, `review_report`, `phases` and `observability`. It names no secret and no host path. A provider not offered is refused by the routes that start work with 400 `api_provider_not_offered`. |
| `GET` | `/api/v1/digest` | `all_ended_jobs` | `remedy status run --json`, its `client` object | — | no | The digest a program reads about once a minute: every project with its missions, the jobs that still need something and the last ended ones, every open decision and the jobs waiting for their apply, as the `client` object of `remedy status --json` holds it; `all_ended_jobs=true` lists every ended job, as `--all-ended-jobs` does. For a client token it holds only the client's own projects and their jobs. |
| `GET` | `/api/v1/jobs/{job}/proof` | — | `remedy change proof --json` | `invalid_job_id` 404, `job_not_found` 404, `ambiguous_job_id` 400 | no | The proof of one job: what each change rests on and where its evidence is, as `remedy change proof <job> --json` prints it; a job id prefix is accepted, as on the command line, and the command's `--path` filter is not offered over HTTP. A client token reads only a job of one of its projects (403 `api_client_policy_refused`). |
| `GET` | `/api/v1/changes` | `since=<value>` | `remedy client changes --json` | `invalid_cursor` 400 | no | What changed since a cursor: the jobs and decisions as the digest shows them, the decisions answered, the missions and the applies, with the cursor for the next read, as `remedy client changes --since <cursor> --json` prints it; without `since` only a cursor is given. For a client token it lists only what belongs to the client's own projects. |
| `GET` | `/api/v1/health` | — | `remedy doctor health --json` | `health_failed` 503 | no | Remedy's own health, as `remedy doctor health --json` prints it: each check PASS, WARN or FAIL with its detail and hint; when a check is FAIL the route answers 503 with the same body, so a monitor can read the status alone. |
| `POST` | `/api/v1/jobs/{job}/decisions/{decision}` | `reason` (string), `answer` (strings) | `remedy decision resolve --json` | `invalid_job_id` 404, `job_not_found` 404, `decision_not_found` 404, `stop_reason_not_found` 404, `proposed_task_not_found` 404, `ambiguous_job_id` 400, `invalid_argument` 400, `missing_argument` 400, `option_not_applicable` 400, `answer_parse_error` 400, `invalid_budget` 400, `decision_not_resolvable` 400, any other 409 | no | Answers one decision of a job, as `remedy decision resolve <job> <decision> --json` does: `reason` is given as `--reason` and each `answer` as one `--answer`; a job id prefix is accepted, as on the command line, and `--as-mission` is not offered over HTTP. A budget decision answered `extend` starts the job's run at once, and the answer names that run under `resumed`, or why it could not start under `resume_refused`. |
| `POST` | `/api/v1/jobs/{job}/decline` | `reason` (string) | `remedy job decline --json` | `invalid_job_id` 404, `job_not_found` 404, `ambiguous_job_id` 400, `missing_argument` 400, any other 409 | no | Declines a completed job's result, as `remedy job decline <job> --reason <reason> --json` does: nothing is applied and the decline is kept on the job, recorded as coming through `api`; a job that is not completed, or whose result already landed, is refused with 409. |
| `POST` | `/api/v1/jobs/{job}/stop` | `reason` (string) | `remedy job stop --json` | `invalid_job_id` 404, `job_not_found` 404, `ambiguous_job_id` 400, any other 409 | no | Stops a job, as `remedy job stop <job> --reason <reason> --json` does, recorded as coming through `api`: a running job stops at its next safe point (a Pi call in flight is ended within about a second, another provider's call finishes first, nothing new starts) and stays resumable, a job that never started, such as one waiting for its predecessor, ends at once, and a job already stopped answers the stop it had with `already_stopped`; a completed job is refused with 409 `job_not_stoppable`, because its result waits for an apply or a decline. A job id prefix is accepted, and a client token stops only a job of one of its projects (403 `api_client_policy_refused`). |
| `POST` | `/api/v1/jobs/{job}/abandon` | `reason` (string) | `remedy job abandon --json` | `invalid_job_id` 404, `job_not_found` 404, `ambiguous_job_id` 400, any other 409 | no | Ends a job for good, as `remedy job abandon <job> --reason <reason> --json` does, recorded as coming through `api`: it never runs again and leaves the digest's active jobs, while its record and evidence stay readable. A job no process runs is `cancelled` at once; a running one answers `cancel_pending` true and ends `cancelled` at its next safe point, or right after its final checks when the cancel arrives while they run, and is never applied; a cancelled one answers `already_cancelled`. A completed job is refused with 409 `job_not_cancellable` (its result waits for an apply or a decline), and so is a failed one. A job id prefix is accepted, and a client token cancels only a job of one of its projects (403 `api_client_policy_refused`). |
| `POST` | `/api/v1/orders/{order}/cancel` | `reason` (string), `decline_results` (flag) | `remedy client cancel-order --json` | `order_not_found` 404, any other 409 | no | Cancels an order a `POST` to `/api/v1/orders` started, as `remedy client cancel-order <order> --json` does, whatever it is doing: a planning order stops before its next step and a planner call in flight is ended and writes no plan, each of its jobs is cancelled as `POST /api/v1/jobs/{job}/abandon` cancels one, no job of it starts afterwards and nothing of it is applied after the request. `phase` reads `cancelling` while the walk or a job still runs and `cancelled` once nothing does; `jobs` names what the cancel did to each job. An applied result stays applied; a result waiting for its apply stays for the person's decision unless `decline_results` is `true`. A second cancel answers `already_cancelled` true. A client token cancels only an order of one of its projects (403 `api_client_policy_refused`). |
| `POST` | `/api/v1/jobs/{job}/apply` | `commit` (string), `commit_auto` (flag), `commit_with_history` (flag), `push` (flag), `skip_blocked` (flag) | `remedy job apply --json` | `job_not_found` 404, `invalid_argument` 400, any other 409 | no | Approves a completed job's result and applies it to the repository the job's own record names, as `remedy job apply <job> --repo <that repository> --approve --json` does: `commit` is given as `--commit`, and each of `commit_auto`, `commit_with_history`, `push` and `skip_blocked` set to `true` as its option; a job id prefix is accepted; `--repo`, `--test-command` and `--dry-run` are not offered over HTTP, and a job whose record names no repository is refused with 409 `api_job_repository_unknown` before any command runs. |
| `GET` | `/api/v1/orders/{order}` | — | `remedy client order --json` | `order_not_found` 404 | no | Polls the order a `POST` to `/api/v1/orders` started, as `remedy client order <order> --json` does: `state` reads `running`, `ended` or `lost`, `phase` what the order is doing (see `order_phases` in `GET /api/v1/interface`), `cancel` its cancel request or null, `jobs` its jobs, and `answer` holds what `remedy do` printed once the order is not `running`. A client token reads only an order whose order file names its projects (403 `api_client_policy_refused`). |
| `POST` | `/api/v1/orders` | `order` (string), `no_llm` (flag), `new_mission` (flag), `force_job` (flag), `force_mission` (flag), `builder_provider` (string), `reviewer_provider` (string), `deadline` (string), `order_key` (string), `capture_review` (flag) | `remedy client order --json` | — | no | Starts an order through the supervisor's own `OrderLauncher`, the way `remedy do run <options> --no-ui --run-unattended -- order.md` would inside its own folder under the data root, and answers 202 with its record read exactly as the route above reads it. `order` is the order file's whole text, header included, and required; `no_llm`, `new_mission`, `force_job`, `force_mission` and `capture_review` each pass their `remedy do` flag when `true` (`capture_review` leaves the walk's review report under the data root's `review_reports`, its id in the answer's `review_report`); `builder_provider`, `reviewer_provider` and `deadline` each pass their option with their value, and a provider HTTP does not offer (`claude-cli`, or one that is no provider of its role; see `GET /api/v1/execution`) is refused before anything starts with 400 `api_provider_not_offered`. An order whose header names no project, or one that names a project `select_project` cannot resolve to exactly one, is refused before anything starts with 409 `api_order_project_unknown`, and one whose header sets none of `max-cost-usd`, `max-total-tokens`, `max-provider-calls` and `max-wall-clock-minutes` with 400 `order_file_no_cost_cap`; every other refusal is `remedy do`'s own, read back only once the order is polled. `order_key` names the order with a key the client chooses, one to 64 letters, digits, `.`, `_` or `-`, beginning with a letter or a digit, any other value answering 400 `api_body_invalid`; an order with a key whose order file an earlier order of a mission that has not ended still has unfinished jobs for is refused before anything starts with 409 `order_already_running`, the mission's id under `mission_id`, unless `new_mission` is `true`, which adds it as one more order to the repository's one mission, and the record's `order_file` then names the key's file. |
| `GET` | `/api/v1/jobs/{job}/logs` | `run=<value>` | `remedy doctor logs --json` | `invalid_job_id` 404, `job_not_found` 404, `ambiguous_job_id` 400 | no | The operations log's lines of one job, oldest first, as `remedy doctor logs <job> --json` prints them; `run` keeps the lines of one run of a task. A job id prefix is accepted when it names one job, a job with no line answers an empty list, and a client token reads only a job of one of its projects. |
| `GET` | `/api/v1/jobs/{job}/story` | — | `remedy client story --json` | `invalid_job_id` 404, `job_not_found` 404, `ambiguous_job_id` 400 | no | One job's run story in closed words a client translates, as `remedy client story <job> --json` prints it: `order`, `state` and `state_detail`, `next` with the one next step and the route that takes it, `end` with the way out of a job that is still open (since 1.21), the five `steps` with the job's tasks under `building`, `changes`, `numbers` (null where not measured) and `note_open`. Every word is in the `story` key of `GET /api/v1/interface`. A job id prefix is accepted, and a client token reads only a job of one of its projects (403 `api_client_policy_refused`). |
| `GET` | `/api/v1/now` | — | `remedy client now --json` | — | no | What runs right now, in closed words a client translates, as `remedy client now --json` prints it (F311): `jobs`, one entry per running job with its `order`, `project`, `state`, `phase`, `task`, `round`, `worker`, `budget` (`used` and `limits`), `last_output_s`, `stalled` with its `stall_reason`, and `waiting_on`; `orders`, the orders that wait with no running job; `model_server`, the local model server's `state`, its `loaded` models and its `queue`; `workers`; and `stall_threshold_s`. A value Remedy cannot know is null. Every word is in the `insight` key of `GET /api/v1/interface`. A client token reads only its own projects' jobs and orders. |
| `GET` | `/api/v1/jobs/{job}/insight` | `lines=<value>` | `remedy client insight --json` | `invalid_job_id` 404, `job_not_found` 404, `ambiguous_job_id` 400 | no | One job's worker seen from outside, as `remedy client insight <job> --json` prints it (F311): the job's entry of `GET /api/v1/now`, plus `stream`, the worker's last `lines` stream lines (default 40, at most 200, already redacted), and `advice`, the closed words for what the operator can do. Every word is in the `insight` key of `GET /api/v1/interface`. A job id prefix is accepted, and a client token reads only a job of one of its projects (403 `api_client_policy_refused`). |
| `GET` | `/api/v1/jobs/{job}/diff` | — | `remedy client diff --json` | `invalid_job_id` 404, `job_not_found` 404, `ambiguous_job_id` 400, `diff_not_ready` 409, `diff_unavailable` 409 | no | One ended job's change as git prints it, as `remedy client diff <job> --json` does: `job`, `state` (`prepared`, `applied`, `declined`, `failed` or `conflict`), `files` with each file's `path`, `change` (`added`, `modified`, `deleted` or `renamed`), `added` and `removed` lines, its unified `patch` and `truncated`, and `truncated` when a patch or the list was cut. A result not yet applied is the job branch against its base commit, an applied one the commit its apply landed. A job that has not ended or waits for an answer answers 409 `diff_not_ready`, commits git no longer has 409 `diff_unavailable`. A job id prefix is accepted, and a client token reads only a job of one of its projects (403 `api_client_policy_refused`). |
| `GET` | `/api/v1/jobs/{job}/run` | — | `remedy client run --json` | `run_not_found` 404 | no | Polls the run the `POST` to this path started, answering the run's record as `remedy client run <job> --json` does: the record's keys, `state` and `answer`. A client polls it until `state` is not `running`: `state` reads `running`, `ended` or `lost`; `exit_code` is `null` until the run ends and stays `null` for a run read `lost`; `answer` is `null` while the run is `running` and afterwards holds what `remedy job run --json` printed, or `null` when it printed no envelope. A job id prefix is accepted; a value that names no one job, or a job with no run, is refused with 404 `run_not_found`, and a client token reads only a job of one of its projects (403 `api_client_policy_refused`). |
| `POST` | `/api/v1/jobs/{job}/run` | `builder_provider` (string), `reviewer_provider` (string) | the run's record, as the supervisor's `RunLauncher` writes it | — | no | Starts a job's run through the supervisor's own `RunLauncher`, as `remedy job run <job> <options> --json` would, and answers 202 with the run's record: `job_id`, `pid`, `started_at`, `out_log`, `err_log`, `exit_code` and `ended_at`, the last two `null` until the run ends, and `state` and `answer` as the route above reads them. `builder_provider` and `reviewer_provider` each pass `--builder-provider=<value>` and `--reviewer-provider=<value>`, a provider HTTP does not offer refused with 400 `api_provider_not_offered`; no other option of `remedy job run` is offered over HTTP. A job id prefix is accepted. A client waits for the run's end by polling the route above until `state` is not `running`. Refusals: `invalid_job_id` 404, `job_not_found` 404 (also for a record that cannot be read), `ambiguous_job_id` 400, `job_already_running` 409, `api_command_failed` 500 when the run cannot start, and `api_client_policy_refused` 403 for a client token's job outside its projects. |

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
