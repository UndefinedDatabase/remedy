
## DECISION F268 D16 (2026-09-18, reviewer, round 8) — every `remedy do` walks the sequence, with T2_F268.md's flag list
CONTEXT: T2_F268.md's Design lists `do`'s flags completely and says nothing else lives under `do`;
R-0933 is `--builder-provider` validated and then unread on the non-bare path. Measured at
`3c18ade2` by the reviewer's research helper and the reviewer's scratch probe: `apps/cli/grouped.py`
sends `remedy do "<order>"` to the sequence only when every flag after the order is in its bare-flag
list, and anything else (`--project`, a budget flag, `--autonomy-level`, an explicit `do run`) to the
autorun branch of `_cmd_do`, which calls `run_do` with no provider; `run_job` in
`packages/orchestration/pingpong_job.py` already takes `budgets`, `builder_model` and
`reviewer_model` — on a fixture, a dict from `resolve_job_budgets(cli_max_total_tokens="100000")`
was recorded as the job's budgets and both models as `cli`-sourced in its `execution_config`;
`select_project("<slug>", repo)` resolved a registered slug and raised `ProjectNotFoundError` for an
unknown one; `intake.make_structured_call_fn` takes `model=`; the planner has exactly one provider,
Ollama, and `role_config` knows no planner role.
CHOSEN: (1) every `remedy do` invocation, with or without the word `run`, walks the sequence; the
bare-flag detection in `grouped.py` and the autorun branch of `_cmd_do` leave. (2) `--autonomy-level`,
`--max-cycles`, `--ui` and `--dry-run` leave `do` (catalog, parser, handler). (3) `--no-llm` stays,
outside the Design's list: it is how a fake-provider walk plans without a model, and every
acceptance test uses it. (4) `--project <slug-or-id>`: the init step selects that project through
`select_project` instead of resolving or registering the repository; an unknown project fails the
init step and nothing after it runs. (5) The budget flags are resolved with `resolve_job_budgets`
before the first step, an invalid value exits 2 with nothing run, and when any budget flag is given
the run step passes the resolved budgets to `run_job`, as `job run` does. (6) `--builder-model` and
`--reviewer-model` are validated as `job run` validates them, passed to `run_job`, and carried on every
`Next: remedy job run` line beside the provider flags. (7) `--planner-model` is passed as `model=` to
every structured planner call the plan and shape steps build; under `--no-llm` there is none.
(8) `--planner-provider` is NOT created: its one legal value would be `ollama`, and a flag with one
value advertises a choice that does not exist; the operator may overturn this (operator question
Q3). R-0933 is resolved by (1) together with a test that reads the provider recorded on a job that
an explicit `remedy do run "<order>" --builder-provider fake` started.
ALTERNATIVES: keep the autorun branch for the flags outside the list, rejected because the Design
says nothing else lives under `do` and R-0933 is that branch. REVERSE: restore the branch, the
bare-flag detection and the four flags from git history; delete this paragraph.
