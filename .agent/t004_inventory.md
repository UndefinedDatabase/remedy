# T004 shape inventory — what exists before `remedy stats cache` is written

> Read-only. F105 R42, 2026-08-10. Every claim below carries the `path:line` it
> rests on and was opened and read before it was written. Where the answer is
> "nothing does this", the entry says so instead of naming a near miss.
> Nothing in this round adds a command, a module, a field, a fixture or a test.

## 1. Where a per-call cache-read figure enters the system

Three layers, and the figure changes type twice on the way down.

**Parse.** `UsageActuals.cache_read` is a plain `int`
(`packages/orchestration/token_actuals.py:32`), filled from the Claude CLI
JSON's `usage.cache_read_input_tokens` at
`packages/orchestration/token_actuals.py:110` with a `.get(..., 0) or 0`
default. The field's own docstring says "0 if not reported"
(`packages/orchestration/token_actuals.py:21`). So AT THIS LAYER a provider
that reports no cache field leaves a measured-looking `0` behind — there is no
`None` to distinguish "reported zero" from "reported nothing". `cache_creation`
is the same shape one line up (`token_actuals.py:111`).

**Aggregate.** `_aggregate_usage_actuals` sums `cache_read` over every non-fake
`ProviderAttempt` (`packages/orchestration/pingpong_loop.py:3640` reads the
attempt's figure, `:3644` adds it to the run total). If NO real provider attempt
happened at all the function returns None entirely
(`packages/orchestration/pingpong_loop.py:3666`), so the run carries no usage
record rather than a zeroed one.

**Evidence.** `_build_provider_evidence` writes the `usage` block ONLY when
`actual_available` is true (`packages/orchestration/pingpong_loop.py:3776`,
block opens at `:3777`), and the cache figure lands there as
`cache_read_input_tokens` (`packages/orchestration/pingpong_loop.py:3781`).
`actual_cache_read_tokens` is a permitted top-level field of the closed schema
(`packages/orchestration/provider_token_evidence.py:58`), and a
`manual_operator_repair` bundle is forbidden from carrying it at all
(`packages/orchestration/provider_token_evidence.py:178-184`).

**What a silent provider leaves behind.** At the evidence and ledger layers,
nothing: no `usage` block is written, `_extract_actual` finds no alias for
`actual_cache_read_tokens`
(`packages/orchestration/token_truth.py:70-72` names the aliases,
`:267` returns None when nothing was found), and
`_call_record_from_parts` therefore stores `cache_read=None`
(`packages/orchestration/token_ledger.py:1022`) with `cost_basis` `unknown`
(`packages/orchestration/token_ledger.py:1027-1029`). That NULL is the honest
value the whole `unmeasured` rendering rests on.

**The one lossy seam, stated plainly.** A provider that DID report usage but no
cache field yields `cache_read = 0` at `token_actuals.py:110`, that 0 is summed
at `pingpong_loop.py:3644`, written as `cache_read_input_tokens: 0` at `:3781`,
and stored as a measured `0` — not NULL — in the ledger. So the ledger can hold
a zero that means "not reported by this provider". T004 cannot tell those two
zeros apart from the ledger alone.

## 2. The `Cache read` column `remedy stats cost` already renders

**Row shape.** `CostRow` (`packages/orchestration/token_ledger.py:286`) is
`bucket, calls, tokens_in, tokens_out, cache_read, cache_write, cost_usd,
measured_calls, unmeasured_calls` (`:309-317`). Every measurement field is
`int | None` / `float | None` on purpose; the two basis counters are plain ints
because a count of nothing really is 0 (`token_ledger.py:294-306`). The
`fully_measured` property is at `token_ledger.py:320-323`.

**Where the column is declared.** `_FIGURE_COLUMNS` in
`apps/cli/commands/stats_ledger_cmd.py:47-53` — `cache_read` is the third
entry, header `Cache read`, at `apps/cli/commands/stats_ledger_cmd.py:50`. The
same tuple drives both the table (`:222`) and the JSON payload (`:153`), so the
two output modes cannot drift apart.

**How `unmeasured` is decided.** `_figure` at
`apps/cli/commands/stats_ledger_cmd.py:188-194`: the ONLY test is
`value is None`, and then it returns the constant `UNMEASURED = "unmeasured"`
(`apps/cli/commands/stats_ledger_cmd.py:44`). A real `0` renders as `0`. The
NULL survives that far because `_cost_bucket_rows` uses `SUM()` and does not
coalesce (`packages/orchestration/token_ledger.py:896-921`, the SQL at `:896`,
the mapping at `:908`). In `--json` the same figure is `null`, and the payload
says so in words at `apps/cli/commands/stats_ledger_cmd.py:176-182`.

**Where a `cache` subcommand would sit.** Beside `_cmd_stats_cost`
(`apps/cli/commands/stats_ledger_cmd.py:265`), registered in the module's
`COMMAND_HANDLERS` dict (`apps/cli/commands/stats_ledger_cmd.py:379-387`) and
declared as a `CommandEntry` in the catalog next to `stats.cost`
(`apps/cli/command_catalog.py:2903`). No `stats.cache` entry exists today:
grepping `stats cache` / `stats.cache` across the repo returns hits only in
`.agent/` planning text — NOT FOUND in `apps/`, `packages/`, `tests/` or
`docs/`.

## 3. Does anything carry a ROLE dimension on a token figure?

Yes on both sides — and the two sides do not meet. This is the T004 design
question.

**The ledger side has a `role` column.** `calls.role` is a real column
(`packages/orchestration/token_ledger.py:182`), indexed with `model`
(`:197`), and `role` is one of the three group keys `query_cost` accepts
(`COST_GROUP_KEYS`, `packages/orchestration/token_ledger.py:156`, expression at
`:161`). `remedy stats cost --by role` works today and is pinned by
`tests/cli/test_stats_cost.py:235` and
`tests/orchestration/test_token_ledger.py:982`.

**But that role is not the trace's role.** The ledger's `role` is read from
`token_accounting.json`'s `role` key and nothing else
(`packages/orchestration/token_ledger.py:1017`), and the producer of that file
hardcodes it: `"role": "builder"` at
`packages/orchestration/pingpong_loop.py:3970`. So every ledger row a live run
writes says `builder`, whatever actually ran. The `reviewer` bucket seen in
tests exists only because the fixtures hand-write `{"role": "reviewer"}`
(`tests/cli/test_stats_cost.py:115-116`,
`tests/orchestration/test_token_ledger.py:536-537`).

**The trace side has a richer role vocabulary.** `PromptTraceEntry.role`
(`packages/orchestration/prompt_trace.py:64`) is written with at least seven
distinct values across the call sites:
`builder` (`packages/orchestration/pingpong_loop.py:2785`),
`reviewer` (`packages/orchestration/pingpong_loop.py:2971`),
`intake` (`packages/orchestration/intake.py:137`),
`flight_plan` (`packages/orchestration/flight_plan.py:183`),
`orchestrator` (`packages/orchestration/orchestrator_loop.py:922`),
`mission_plan` (`packages/orchestration/mission_compiler.py:282`) and
`planner` (`apps/cli/commands/job.py:238`).

**Is there a JOIN key? NOT FOUND for five of the seven roles.**
A ledger row's identity is `"<job_id>:<task_id>"`
(`packages/orchestration/token_ledger.py:465-488`), and a row is one FINALIZED
TASK RUN, not one HTTP request (`token_ledger.py:474-476`). A trace entry
carries `run_id`, `job_id`, `task_id` and `round` fields
(`packages/orchestration/prompt_trace.py:60-63`), so `(job_id, task_id)` is the
only candidate key. It is populated ONLY at the two pingpong sites
(`packages/orchestration/pingpong_loop.py:2786-2788` and `:2973-2975`).
`job.py:239` sets `job_id` alone — no `task_id`, so it cannot form the key.
The `intake`, `flight_plan`, `orchestrator` and `mission_plan` sites pass
neither: `intake.py:135-146`, `flight_plan.py:181-192`,
`orchestrator_loop.py:920-931` and `mission_compiler.py:280-291` all leave the
identity fields at their `""` defaults.

The gap is worse than a missing field. Those four roles produce no ledger row at
all: rows are only ever created from `task_runs/<task_id>/provider_evidence.json`
(`packages/orchestration/token_ledger.py:554-556`), and the live write hook
returns early unless the path really is that task-run layout
(`packages/orchestration/pingpong_evidence.py:586-589`) and both identifiers are
present (`:576-577`). An intake or flight-plan call therefore has a prompt trace
and no ledger row to join it to.

**One per-role cache figure DOES exist, just not in the ledger.**
`_aggregate_usage_actuals` builds a `by_role` map keyed on
`ProviderAttempt.role` (`packages/orchestration/pingpong_loop.py:3598`, keyed at
`:3619`) that accumulates `cache_read` per role
(`packages/orchestration/pingpong_loop.py:3650`) and returns it at `:3698`. It
reaches disk twice: as the `builder_*`/`reviewer_*` cache fields of
`token_accounting.json` (`packages/orchestration/pingpong_loop.py:3990-3997`)
and whole, inside `accounting["usage_actuals"]`
(`packages/orchestration/pingpong_loop.py:4010`), written out by
`packages/orchestration/pingpong_evidence.py:410-415`. It is NOT copied into
`provider_evidence.json` — `_build_provider_evidence`'s `usage` block is
role-aggregated (`packages/orchestration/pingpong_loop.py:3777-3782`) — and so
it never reaches the ledger. Its vocabulary is `builder`/`reviewer` only
(`packages/orchestration/pingpong_loop.py:3619` defaults an unnamed attempt to
`builder`).

## 4. The ledger schema where a cache-read figure lands

`calls` is a single flat table at `packages/orchestration/token_ledger.py:178-193`:
`call_id` PK, `job_id`, `task_id`, `role`, `model`, `ts_utc` NOT NULL,
`tokens_in`, `tokens_out`, `cache_read`, `cache_write`, `cost_usd`,
`cost_basis` (CHECK-constrained to the three bases), `evidence_ref`.
`SCHEMA_VERSION` is 1 (`token_ledger.py:102`) and migrations are numbered steps
(`token_ledger.py:169`), so adding a version 2 is a supported move, not a rewrite.

**Would per-role grouping need a schema change? It depends on which "role".**

- Grouping by the role the ledger ALREADY stores: NO schema change and no query
  change either — `query_cost(by="role")` exists
  (`packages/orchestration/token_ledger.py:711`, `:766-769`). But per §3 that
  role is a constant `builder` in production data, so the answer would be one
  bucket and would be worthless.
- Grouping by the trace's role vocabulary (`intake`, `flight_plan`, …): a
  SCHEMA CHANGE IS NOT WHAT IS MISSING FIRST. There is no per-role row and no
  per-role figure in `provider_evidence.json` to put in one; the granularity of
  a row is a whole task run (`token_ledger.py:474-476`), which can contain
  several attempts across two roles. Either the producer starts writing an
  honest `role` (a one-line change at `pingpong_loop.py:3970` plus a decision
  about multi-role task runs), or the row granularity itself changes — and that
  second option breaks the `call_id` identity that makes backfill idempotent
  (`token_ledger.py:468-472`).

## 5. Fixtures a `remedy stats cache` test could read as ACTUALS

All of them are built in test code; there is NO on-disk evidence fixture tree in
the repository carrying `actual_cache_read_tokens` — `grep -rln` over `tests/`
finds it only in four Python test modules, and under
`tests/orchestration/fixtures/` the only cache-bearing file is a provider stream
capture, `tests/orchestration/fixtures/stream/basic_session.jsonl:6`
(`cache_read_input_tokens: 900`), which is a CLI-transcript fixture, not an
evidence tree.

- `tests/cli/test_stats_cost.py:77` — the `evidence_dir` fixture: a real
  two-task evidence tree under `tmp_path`, with `actual_cache_read_tokens: 64`
  and `actual_cache_creation_tokens: 32` on the measured run
  (`tests/cli/test_stats_cost.py:94-95`) and a deliberately unmeasured second
  run (`:104-114`). It also hand-writes the two `token_accounting.json` role
  files (`:101`, `:115-116`) — which, per §3, is the only reason a second role
  bucket exists at all.
- `tests/cli/test_stats_cost.py:121` — `filled_ledger`: the same tree after one
  real `backfill-ledger`, i.e. the state every query test starts from. This is
  the closest thing to "cache stats render from fixture actuals" that exists.
- `tests/orchestration/test_token_ledger.py:495` — `evidence_tree`: four task
  runs (full actuals, no usage, malformed counters, no evidence file),
  `actual_cache_read_tokens: 64` at `:517`.
- `tests/orchestration/test_token_ledger.py:909` — `cost_ledger`: four
  `CallRecord`s written row by row, two `builder` and two `reviewer`, with
  `cache_read=64` on one (`:917`). It bypasses evidence entirely, so it pins
  query behaviour but proves nothing about the producer.
- `tests/orchestration/test_provider_evidence_integration.py:978` —
  `test_cache_tokens_reconcile_by_role`, the one existing test that already
  asserts something about cache tokens PER ROLE.

## 6. The smallest honest first slice

Add `remedy stats cache` as a read-only view over the ledger rows that already
exist, reporting the cache-read share — `cache_read / (tokens_in + cache_read)`
— per bucket, with the same `unmeasured`-never-`0` discipline `stats cost`
applies, and grouped by the ledger's existing group keys. It would touch
`apps/cli/commands/stats_ledger_cmd.py` (a `_cmd_stats_cache` beside
`_cmd_stats_cost` at `:265`, an entry in `COMMAND_HANDLERS` at `:379`),
`apps/cli/command_catalog.py` (one `CommandEntry` beside `stats.cost` at
`:2903`) and one new test module built on the fixture shape of
`tests/cli/test_stats_cost.py:77`. It would reuse `query_cost` unchanged.

What that slice would explicitly NOT do: it would not add a ledger column, not
bump `SCHEMA_VERSION`, not touch `packages/orchestration/token_ledger.py`, not
change what `pingpong_loop.py:3970` writes into `token_accounting.json`, not
invent a role for a call that has none, and not report per-role figures in the
trace's vocabulary — because §3 shows no join key exists for five of the seven
trace roles. Where the ledger's `role` is NULL or is the hardcoded constant, the
view must say so rather than present one `builder` bucket as a per-role
breakdown. It would also not attempt to separate a reported `0` from an
unreported one, because §1 shows the ledger cannot.

## Open questions for the reviewer

1. Is "cache-read share per role" (plan.md, feature file Acceptance) satisfied
   by the ledger's `role` column as it is actually populated today — one
   constant `builder` — or does T004 have to fix the producer at
   `packages/orchestration/pingpong_loop.py:3970` first?
2. If the producer is fixed: a task run can contain builder AND reviewer
   attempts, but a ledger row is one task run
   (`packages/orchestration/token_ledger.py:474-476`). Does the row split, does
   the role become a list, or does the view read `by_role` out of
   `token_accounting.json` instead of the ledger?
3. Does "cache stats render from fixture actuals" mean an evidence-tree fixture
   backfilled into a ledger (the `tests/cli/test_stats_cost.py:121` shape), or a
   directly-written ledger (the `tests/orchestration/test_token_ledger.py:909`
   shape)? Only the first exercises the producer path.
4. Should the measured-zero / unreported-zero collapse at
   `packages/orchestration/token_actuals.py:110` be recorded as a finding
   against the actuals feature rather than worked around inside T004?
5. The feature file's edge case says providers without cache reporting show
   "not reported". Is that the existing word `unmeasured`
   (`apps/cli/commands/stats_ledger_cmd.py:44`), or a second vocabulary?
