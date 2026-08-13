# F115 R1 — shape inventory: the token ledger and the prompt-segment registry

> Written at F115 R1 before any code. Every claim below cites `path:line` from
> source read in this round. Where the answer is "this does not exist yet", it
> says so in those words.

## Q1 — Where is a ledger row WRITTEN?

`record_call(record, *, project_id=None, path=None) -> bool`
(`packages/orchestration/token_ledger.py:398`). One statement, one commit:
`INSERT OR IGNORE INTO calls (...)` at `token_ledger.py:425-428`. It never
raises — every failure is logged and counted as a miss
(`token_ledger.py:447-455`).

Call sites of `record_call` outside tests — exactly two:

1. `packages/orchestration/token_ledger.py:623`, inside `backfill_ledger`
   (`token_ledger.py:587`), reached from the CLI at
   `apps/cli/commands/stats_ledger_cmd.py:477`.
2. `packages/orchestration/pingpong_evidence.py:593`, inside
   `_record_finalized_call_in_ledger` (`pingpong_evidence.py:546`), called from
   `pingpong_evidence.py:519` right after `provider_evidence.json` is written.

The live path IS armed in production: `job_evidence.py:2536-2542` passes
`ledger_project_id` / `ledger_job_id` / `ledger_task_id` into
`write_evidence_bundle`, resolved once at `job_evidence.py:216-221` via
`_resolve_job_ledger_project_id` (`job_evidence.py:65`). Without those the hook
returns immediately (`pingpong_evidence.py:574-577`).

The field set a row carries today — 13 columns, `_CALL_COLUMNS`
(`token_ledger.py:137-151`), mirroring `CallRecord` (`token_ledger.py:203-228`)
field for field:

    call_id, job_id, task_id, role, model, ts_utc,
    tokens_in, tokens_out, cache_read, cache_write,
    cost_usd, cost_basis, evidence_ref

Provenance of each is mapped in one shared function `_call_record_from_parts`
(`token_ledger.py:985-1031`), used by BOTH producers so they cannot disagree.
`call_id` is `"<job_id>:<task_id>"` (`token_ledger.py:465-488`); a row is one
FINALIZED TASK RUN, not one HTTP request (`token_ledger.py:37-41`, DECISION
D16). `evidence_ref` is the relative path `task_runs/<task_id>`
(`token_ledger.py:574`).

There is NO segment, no manifest, no prompt and no task-class column.

## Q2 — Storage shape

SQLite, one file per project, `ledger.sqlite`
(`token_ledger.py:108`), at `<data_root>/projects/<project_id>/ledger.sqlite`
(`token_ledger_path_for`, `token_ledger.py:358-369`). This is the only SQLite
user in Remedy (`token_ledger.py:16-19`); everything else is atomic JSON.

Schema verbatim, `_MIGRATIONS[1]` (`token_ledger.py:169-199`):

    CREATE TABLE IF NOT EXISTS meta (
        key   TEXT PRIMARY KEY,
        value TEXT NOT NULL
    )

    CREATE TABLE IF NOT EXISTS calls (
        call_id      TEXT PRIMARY KEY NOT NULL,
        job_id       TEXT,
        task_id      TEXT,
        role         TEXT,
        model        TEXT,
        ts_utc       TEXT NOT NULL,
        tokens_in    INTEGER,
        tokens_out   INTEGER,
        cache_read   INTEGER,
        cache_write  INTEGER,
        cost_usd     REAL,
        cost_basis   TEXT NOT NULL CHECK (cost_basis IN ({_COST_BASIS_CHECK})),
        evidence_ref TEXT
    )

    CREATE INDEX IF NOT EXISTS idx_calls_job_id ON calls (job_id)
    CREATE INDEX IF NOT EXISTS idx_calls_ts_utc ON calls (ts_utc)
    CREATE INDEX IF NOT EXISTS idx_calls_role_model ON calls (role, model)

Migrations are numbered steps, so an additive `version 2` appends an entry and
never rewrites version 1's path (`token_ledger.py:167-168`, applied at
`token_ledger.py:1072-1089`). `SCHEMA_VERSION = 1` (`token_ledger.py:102`).
WAL mode, `busy_timeout` 5000 ms (`token_ledger.py:386-389`). Reads go through
`_connect_readonly` (`token_ledger.py:837-862`), which uses `mode=rw` plus
`PRAGMA query_only=1` so a query can neither create nor migrate a database.

## Q3 — What the prompt-segment MANIFEST contains, and where it is persisted

One manifest row is `PromptSegmentManifestEntry`
(`packages/orchestration/prompt_segments.py:89-98`): `name`, `rank` (int),
`sha256`, `chars`, `tokens_estimated`. Ranks come from
`SegmentStabilityRank` (`prompt_segments.py:53-61`): SYSTEM 0, CONVENTIONS 1,
DOSSIER 2, JOB_CONTEXT 3, TASK 4, STEERING 5. `tokens_estimated` is the repo's
chars/4 ESTIMATE, never a tokenizer count (`prompt_segments.py:14-17`).
`ComposedPrompt.manifest_as_dicts()` (`prompt_segments.py:107-122`) is the
JSON-ready form, in composition order.

It is persisted into call evidence through the prompt TRACE, not the ledger:
`PromptTraceEntry.segment_manifest` (`prompt_trace.py:77`) and
`segment_manifest_chars` (`prompt_trace.py:83`), both derived from one
`composed_prompt` argument at `prompt_trace.py:154-159` so they cannot
disagree. Entries reach disk as JSONL via `write_trace_jsonl`
(`prompt_trace.py:192`) or `append_trace_jsonl` (`prompt_trace.py:205`), and
the job's trace file is copied into the evidence bundle as
`prompt_trace.jsonl` at `pingpong_evidence.py:527-536`, sourced from
`job_evidence.py:2528`.

LOAD-BEARING GAP: only four of the eight `build_trace_entry` call sites pass
`composed_prompt`, so only those four produce a non-empty manifest —
`flight_plan.py:191`, `intake.py:145`, `orchestrator_loop.py:930`,
`mission_compiler.py:290`. The three call sites that produce the prompts of a
real ping-pong task run do NOT pass it: the builder
(`pingpong_loop.py:2824-2840`), the reviewer (`pingpong_loop.py:3010-3031`) and
the planner (`apps/cli/commands/job.py:236-248`). An empty
`segment_manifest` means "this prompt was not composed through the registry",
not "composition produced no segments" (`prompt_trace.py:74-76`).

## Q4 — Is there ALREADY a link between a ledger row and its segment manifest?

There is a JOINABLE PATH, but NO column and NO direct reference. Precisely:

* A ledger row carries `job_id`, `task_id` and
  `evidence_ref = "task_runs/<task_id>"` (`token_ledger.py:137-151`,
  `token_ledger.py:574`).
* The evidence bundle for that same task run is written into
  `<evidence_dir>/task_runs/<task_id>/` (`pingpong_evidence.py:465`,
  gated at `pingpong_evidence.py:586`), and `prompt_trace.jsonl` is written
  into that SAME directory (`pingpong_evidence.py:533`).
* Each trace line carries its own `job_id`, `task_id`, `round`, `role`,
  `phase` and `transport_attempt` (`prompt_trace.py:61-63`, `:64`, `:95-99`).

So `(job_id, task_id)` — equivalently the row's own `evidence_ref` — reaches
the manifest without inventing an identifier. Three real caveats:

1. The relation is ONE ledger row to MANY trace lines. A row is one finalized
   task run (`token_ledger.py:37-41`); a task run makes many provider calls,
   each with its own trace line. There is no per-call ledger row to join to.
2. On live ping-pong data those trace lines carry an EMPTY
   `segment_manifest`, per Q3. Today the join resolves to nothing for exactly
   the rows F115 cares about.
3. `prompt_trace.jsonl` copied into a task-run directory is the whole JOB's
   trace file, not that task's (`prompt_trace.py:200-204`,
   `job_evidence.py:2528`), so a consumer must filter by `task_id`.

The feature file's premise at `docs/roadmap/features/T2_F115.md:14-15`
("The prompt-segment registry records a manifest ... into call evidence")
is therefore true of the module and its four wired call sites, and NOT true of
the builder/reviewer calls that generate ledger rows.

## Q5 — What `remedy stats` exposes today

Group `stats` — "Honest counts from the evidence on disk."
(`apps/cli/command_catalog.py:109`). Five subcommands:

| Subcommand | Catalog | Class | Args |
|---|---|---|---|
| `stats failures` | `command_catalog.py:2902` | read_only | `--job`, `--since`, `--project`, `--all-projects`, `--json` |
| `stats cost` | `command_catalog.py:2920` | read_only | `--since`, `--job`, `--by`, `--project`, `--all-projects`, `--json` |
| `stats cache` | `command_catalog.py:2943` | read_only | `--since`, `--job`, `--by`, `--project`, `--all-projects`, `--json` |
| `stats backfill-ledger` | `command_catalog.py:2966` | write_metadata | `evidence_dir`, `--project`, `--all-projects`, `--json` |
| `stats verify-ledger` | `command_catalog.py:2987` | read_only | `evidence_dir`, `--project`, `--all-projects`, `--json` |

There is NO `stats report` subcommand yet — this does not exist yet.
Handlers: `stats_ledger_cmd.py:543-572`. `--by` accepts exactly
`role|model|day` (`token_ledger.py:156`, validated at
`stats_ledger_cmd.py:56-70`). Output modes are plain text or `--json`; NO
`--markdown` flag exists on any `stats` subcommand.

Renderer-pair patterns to follow:

* Within `stats`: `_cost_payload` / `_render_cost_human`
  (`stats_ledger_cmd.py:162`, `:197`) and `_cache_payload` /
  `_render_cache_human` (`stats_ledger_cmd.py:386`, `:403`), both fed by one
  shared reader `_load_ledger_reports` (`stats_ledger_cmd.py:266`). These are
  plain-text tables, not markdown.
* The MARKDOWN/JSON pure-renderer pair the feature actually wants already
  exists elsewhere: `packages/orchestration/gauntlet_matrix.py` —
  `matrix_json` (`:85`), deterministic `matrix_json_bytes` (`:99`),
  `render_matrix_markdown` (`:173`) and `write_matrix` (`:195`), all pure
  functions over a verdict object. A `--markdown` flag convention also exists
  in the CLI (`apps/cli/grouped.py:206-207`, e.g.
  `command_catalog.py:3304`, handled at `candidate_quality_cmd.py:94`).

## Q6 — Where cost and BASIS labels come from, and what an UNPRICED call is

Not from `token_cost_policy.py`. That module builds a separate job-level
evidence artifact `token_cost_policy.json` from role configs, the token-truth
report and the prompt-trace summary (`token_cost_policy.py:9-13`,
`build_token_cost_policy` at `:102`, returned shape at `:221-235`). Its
vocabulary is `cost_risk_findings` / `recommendations`
(`token_cost_policy.py:61-63`, `:238`), it reads no price table, and it never
touches the ledger. It is NOT the source of the ledger's basis labels.

The ledger's basis is set in one place, `_call_record_from_parts`
(`token_ledger.py:1027-1029`): `provider_reported` when a real
`total_cost_usd` was present in `provider_evidence.json`
(`token_ledger.py:1007`), otherwise `unknown`. The closed set is
`COST_BASES = {provider_reported, price_table, unknown}`
(`token_ledger.py:127-134`), enforced by the table's own CHECK built from that
frozenset (`token_ledger.py:153`, `:190`). No code in Remedy writes
`price_table` (`token_ledger.py:305-306`); no price is ever computed
(`token_ledger.py:42-45`, `stats_ledger_cmd.py:15-18`).

An UNPRICED call on disk: a `task_runs/<id>/provider_evidence.json` with no
`total_cost_usd` and no `actual_*` counters — the real claude-cli case. A
concrete example is the fixture at `tests/cli/test_stats_cost.py:107-117`
(`"actual_call_count": 0`, `"cost_call_count": 0`,
`"actual_missing_reasons": ["provider reports no ledger usage"]`). It becomes
a row with NULL counts, NULL `cost_usd` and `cost_basis = "unknown"` — never a
fabricated zero (`token_ledger.py:534-540`). At render time it prints the word
`unmeasured` (`stats_ledger_cmd.py:44`, `_figure` at `:188`) and `null` in
JSON (`_row_payload`, `stats_ledger_cmd.py:150-159`); `_row_basis`
(`stats_ledger_cmd.py:134-147`) adds a fourth rendered word, `mixed`, for a
partly-measured bucket. Aggregation preserves NULL rather than coalescing
(`token_ledger.py:878-921`, `_add_optional` at `:924`).

## Q7 — Fixture-ledger and golden patterns T002 should follow

* FIXTURE LEDGER — `tests/cli/test_stats_cost.py:49-128`: fixtures
  `data_root` (`:49`, `REMEDY_DATA_DIR` under `tmp_path`), `project_id`
  (`:58`), `ledger_path` (`:67`, with the assertion at `:70` that the real
  data root was not touched), `evidence_dir` (`:79`, two task runs — one
  measured, one unmeasured), and `filled_ledger` (`:123`, built by running the
  real backfill). The ledger is never hand-built with raw SQL; it is produced
  from a real evidence tree, which is what keeps the fixture honest.
* MARKDOWN + JSON GOLDEN FILES ON DISK —
  `tests/orchestration/fixtures/gauntlet/golden/matrix.json` and
  `.../matrix.md`, rendered by `packages/orchestration/gauntlet_matrix.py`
  (`:85`, `:99`, `:173`). This is the only markdown/json golden PAIR in the
  suite and is the closest match to F115's "pure function over query results,
  markdown for humans, json for the UI".
* CONTENT-EQUALITY PROMPT GOLDENS — `tests/orchestration/test_*_prompt_golden.py`
  (six files: builder, reviewer, intake, mission, orchestrator, plan). These
  keep their expected values as INLINE module constants, not files
  (`tests/orchestration/test_builder_prompt_golden.py:83-113`). Useful as the
  precedent for "freeze the bytes and measure them", less so for report output.
* Ledger unit-test corpus: `tests/orchestration/test_token_ledger.py` (the
  `record_call` / `backfill_ledger` / `verify_ledger` behaviours,
  e.g. `:205`, `:626`, `:1293`).

## Closing — which T-slice the evidence resizes

T001 is LARGER than the feature file assumes, and the reason is Q3/Q4, not
Q1/Q2. The file's premise is that "every call already records its segment
manifest" (`T2_F115.md:5-6`, `:14-15`), leaving T001 as a small additive
persistence step. The registry does produce the manifest and the trace schema
does carry it, but the three call sites that generate the prompts behind every
ledger row — builder `pingpong_loop.py:2824`, reviewer
`pingpong_loop.py:3010`, planner `job.py:236` — never pass `composed_prompt`,
so on live data the manifest is empty. T001 must therefore either wire those
sites through the registry first (touching `pingpong_loop.py`, which is
prompt-golden-covered and is the largest module in play) or accept that
current production rows are permanently "unattributed" and build only the
backfill-tolerant path. That choice is a planner decision, not a worker one,
and it should be made before T001 is ordered.

A second, independent resizing: the ledger's `role` column cannot support the
"per-role breakdown" the design asks for (`T2_F115.md:27`). Rows take `role`
from `token_accounting.json` (`token_ledger.py:1017`), and that file hardcodes
`"role": "builder"` for the whole task run (`pingpong_loop.py:4011`). The
existing CLI already states this limit in its own output rather than pretending
otherwise (`_ROLE_LIMIT_NOTE`, `stats_ledger_cmd.py:334-339`). Relatedly, the
"by task class" breakdown (`T2_F115.md:7`) has no source at all: there is no
task-class column on a row, and `task_granularity.py:5` states plainly that
"Remedy has no per-task-class cost history yet".

T002 is roughly as assumed, and is the best-supported slice: the aggregation
primitives (`query_cost` `token_ledger.py:711`, `merge_cost_reports` `:776`),
the NULL-preserving fold (`_add_optional` `:924`) and both the fixture-ledger
and markdown/json golden patterns already exist to copy.

T003 is SMALLER than assumed. The scope/flag plumbing (`--since`, `--job`,
`--by`, `--project`, `--all-projects`, `--json`), the catalog entry shape, the
shared reader and the two-mode output are all in place
(`stats_ledger_cmd.py:266-320`, `command_catalog.py:2920-2941`); adding
`stats report` is largely a fourth entry in the same two established patterns,
plus `--until` and the prior-period comparison, which are genuinely new.
