# HTTP clients: from an order to its applied change

This guide walks a program through Remedy's public HTTP API with `curl`, from its token to an
applied or declined change: start an order, poll it, read the job's run story, then apply or
decline. Every route, answer key and refusal it names is in
[the public HTTP API's page](../system/public-http-api-v1.md); the words of a story are in
[the machine client contract](../system/machine-client-contract-v1.md) under "Story words".

Text in angle brackets is a placeholder you replace: `<port>`, `<token>`, `<project>`,
`<order>`, `<job>` and `<decision>`. Nothing else in the commands changes.

## 1. The server and the token

Start the supervisor with `remedy serve start --json`. Its one line of output holds the port
under `api_port`; set the environment variable `REMEDY_SERVE_API_PORT` to `0` before it starts
to let the system pick a free port. The server's own token is the file `serve/serve.token` under
the data root (`REMEDY_DATA_DIR`, by default `~/.remedy`). It may do everything.

A program should use a client token instead, which reads and writes only the jobs of its own
projects. The operator writes it into `api/clients.json` under the data root, a file only its
owner may read (mode `0600`):

```json
{"clients": [{"name": "<name>", "token": "<token of at least 32 characters>",
              "projects": ["<project>"], "max_total_tokens": 200000,
              "max_provider_calls": 40, "may_apply": true}]}
```

`<project>` is the slug `remedy project register --repo <repository> --json` answered. Every
request below sends the header `Authorization: Bearer <token>`; a missing or unknown token
answers 401 `api_token_invalid`, and a job outside the token's projects answers 403
`api_client_policy_refused`.

## 2. Start an order

```
curl -s -X POST http://127.0.0.1:<port>/api/v1/orders \
  -H "Authorization: Bearer <token>" \
  --data '{"order": "---\nproject: <project>\nmax-total-tokens: 200000\n---\nAdd a line saying hello to README.md\n", "order_key": "hello-readme-1"}'
```

The answer is 202 with the order's record; keep its `order_id` as `<order>`. The order text needs
a cap in its header (`max-total-tokens`, `max-provider-calls` or `max-wall-clock-minutes`), or the
answer is 400 `order_file_no_cost_cap`; a project this machine does not know answers 409
`api_order_project_unknown`.

`order_key` makes the start safe to repeat. When the answer is lost and the program sends the same
order with the same key again, an order of that key that still has unfinished jobs answers 409
`order_already_running` with its `mission_id`, and nothing starts twice. An order without a key
starts again every time it is sent.

## 3. Poll the order

```
curl -s http://127.0.0.1:<port>/api/v1/orders/<order> -H "Authorization: Bearer <token>"
```

Poll every second or two until `state` is no longer `running`. `ended` means `remedy do` finished
and `answer` holds what it printed: `answer.job_ids` names the order's jobs, each a 16-character
hexadecimal id; take one as `<job>`. `lost` means the order's process is gone without an end. An
unknown order answers 404 `order_not_found`.

## 4. Read the job's story

```
curl -s http://127.0.0.1:<port>/api/v1/jobs/<job>/story -H "Authorization: Bearer <token>"
```

The story says in closed words what the job did and what comes next. A program shows `state`, the
five `steps` and `changes` in its own language, and offers the one action `next.action` names
through `next.route`, which holds the method and the path to call:

- `apply`: the result waits; `next.route` is `POST /api/v1/jobs/<job>/apply`. Offer
  `decline` beside it.
- `answer`: the job waits for a decision; `next.route` is
  `POST /api/v1/jobs/<job>/decisions/<decision>`, and `state_detail.question` names the kind of
  question. The decision's own text and options are in `GET /api/v1/digest`.
- `retry`: in the list, but named by no state: a failed job reads `none`, because a run of it
  re-attempts no task that ended blocked. Give the order again instead.
- `none`: nothing is to be done, for example once the result is applied (`done_applied`).

Reading a story changes nothing, so a program may read it as often as it likes; two reads of an
unchanged job answer the same. A job id prefix is accepted; an unknown id answers 404
`invalid_job_id` or `job_not_found`, and a prefix of several jobs 400 `ambiguous_job_id`.

## 4a. Show the change before apply

```
curl -s http://127.0.0.1:<port>/api/v1/jobs/<job>/diff -H "Authorization: Bearer <token>"
```

Once the story reads `done`, the diff lists each changed file with its `change`, its `added` and
`removed` lines and its unified `patch`, read from git; `state` is `prepared` until the result is
applied, then `applied`, or `declined`, `failed` or `conflict`. A program shows the patches before
it offers `apply`, and says so when a file's or the answer's `truncated` is `true`. A job that has
not ended answers 409 `diff_not_ready`. The page `docs/system/public-http-api-v1.md` ("Diffs")
names the limits.

## 5. Apply or decline

Apply, when the story's `next.action` is `apply` and the token has `may_apply`:

```
curl -s -X POST http://127.0.0.1:<port>/api/v1/jobs/<job>/apply \
  -H "Authorization: Bearer <token>" --data '{}'
```

It answers 200 with `status` `applied` once the change is in the repository. A second apply of the
same job, for example after a lost answer, applies nothing and answers 409 `job_already_applied`;
read the story again, which then reads `done_applied`. Other refusals answer 409 with their own
token, such as `job_not_ready` or `target_changed_during_run` when someone changed the files since
the job started; a token without `may_apply` answers 403 `api_client_policy_refused`.

Decline, when the person does not want the result:

```
curl -s -X POST http://127.0.0.1:<port>/api/v1/jobs/<job>/decline \
  -H "Authorization: Bearer <token>" --data '{"reason": "<why>"}'
```

It answers 200 and records the decline; nothing is applied. A second decline answers the first
one again, unchanged, with `already_declined` true. A job whose result already landed answers 409
`job_already_applied`, and one that is not completed 409 `job_not_declinable`. The story then
reads `stopped` with the reason `declined`.

## Answers and codes

Every answer is one JSON envelope: `ok` is true with the answer's keys, or false with `error`, a
token a program branches on, and `message`, a sentence for a person. The HTTP statuses are 200 and
202 for success, 400 for a request that is wrong, 401 for a token that is missing or unknown, 403
for a client token's limit, 404 for something that does not exist, 409 for a state that refuses
the request, 500 `api_command_failed` when a command cannot start or answer, and 503 from
`GET /api/v1/health` when a health check fails. The same operations on the command
line (`remedy client story <job> --json`, `remedy job apply <job> --approve --json`) answer the
same envelopes and exit with the codes of [the exit code guide](exit-codes.md): 0 for success, 1
for a refusal, 2 for a wrong argument and 3 for something absent or not ready, such as
`job_already_applied`.
