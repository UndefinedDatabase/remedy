# F317 — one real order lands (operator amendment amend1024-one-real-order, Part G)

Run on 2026-10-24 on the operator's machine, with real provider calls of the Claude Code CLI
2.1.310. Collected by `.agent/authored/amend1024-g-evidence.py`; no client token is stored here.

## Setup (G1, G2)

- A temporary project `/tmp/amend1024-g/greet-project`: the package `greet` with `greet/core.py`
  (`build_greeting`) and `greet/cli.py`, a `README.md` and `tests/test_greet.py` with three tests,
  registered with `remedy project register` in its own data root `/tmp/amend1024-g/data`.
- A client `real-order-client` written into that data root's `api/clients.json` (mode 0600; the
  `remedy client` group has no command that creates one, DECISION amend1024 D6) and granted
  `host_tools` with `remedy client grant-host-tools real-order-client`.
- A supervisor of that data root, `remedy serve start` with `REMEDY_SERVE_API_PORT=18731`, started
  from this branch's code.
- The order, sent with `POST /api/v1/orders` and the client's token, names no provider, no file and
  no shape; its header carries only what the API requires, its project and the caps
  `max-total-tokens: 300000` and `max-provider-calls: 40` (`run2-applied/order_file.md`).

## Run 2 — `run2-applied/` (order `e4eaaaa9cebd3304`, job `24270f620da248bc`)

| Acceptance | Evidence |
|---|---|
| Planned with claude-cli | `24270f620da248bc/scope_decision.json`: planner `claude-cli`, `single_job: true`, files `greet/core.py`, `README.md`, `tests/test_greet.py`, a German reason; `summary.json`: planner calls `scope_decision`, `intake`, `task_plan` |
| Exactly one job | `summary.json`: shape `one job`, shape source `the planner's scope decision`, one job id |
| The builder ran the tests itself | `24270f620da248bc/builder_bash_calls.json`: `python3 -m pytest -q` run by the builder, results `5 passed` and `9 passed`, read from the builder's own raw streams under `task_runs/*/streams/builder/` |
| A command outside the list was refused | `24270f620da248bc/builder_refused_commands.json`: one `printf … >> README.md && …` refused by the CLI |
| The reviewer accepted | the reviewer's raw streams `task_runs/*/streams/reviewer/` read `"verdict": "pass"` for each of the three tasks; `order_poll.json`: job `completed`, phase `awaiting_apply`; `24270f620da248bc/story.json` |
| `remedy job apply` brought the change in | `apply_answer.json` (exit 0), `project_diff_after_apply.patch`: `greet/core.py` title-cases the name, `README.md` has the sentence, six new tests; the project's suite then reads 9 passed |
| Real provider calls | 6 builder and reviewer calls: 36 input, 5,193 output, 135,803 cache-read and 22,317 cache-written tokens; 3 planner calls of about 3,500 estimated tokens; `summary.json` `order_budget_used`: 9 calls, 8,711 tokens, 2.1 minutes |

## Run 1 — `run1-declined/` (order `3a45850644d6d551`, job `e17412639ed14265`)

The same order, before a claude-cli builder streamed by default. It landed a correct change (one
job, the tests green in the DoD), but a claude-cli call in JSON mode keeps only its final answer,
so nothing showed which commands the builder ran; its four refused commands are in
`run1-declined/e17412639ed14265/runs/*.builder_command_refusals.jsonl`. The result was declined on purpose and the order sent again
after DECISION amend1024 D5; run 1 stays as the evidence of why.
