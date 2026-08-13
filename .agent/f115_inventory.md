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

LOAD-BEARING GAP: only four of the seven `build_trace_entry` call sites pass
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

## T001 persistence inventory (R7)

Facts only, each with a `path:line` citation read at this round. The shape
question T001 has to answer is already visible: `token_ledger.py` documents that
A ROW IS ONE FINALIZED TASK RUN keyed `"<job_id>:<task_id>"` (DECISION F103
D16), while a segment manifest belongs to ONE PROVIDER CALL — so "the manifest
alongside the ledger row" is a one-to-many mapping, not a column copy. Answer
each question directly below it; write "not found" plus the command you ran
rather than an inference.

Q1. The ledger row: every column of the table a task run writes, taken from the
CREATE TABLE statement itself, with its `path:line`. Name which columns are
NULLable and which carry a default.

A1. The row is one entry in the `calls` table, created by migration step 1 at
`packages/orchestration/token_ledger.py:178-192`. Thirteen columns, in this
order: `call_id TEXT PRIMARY KEY NOT NULL`, `job_id TEXT`, `task_id TEXT`,
`role TEXT`, `model TEXT`, `ts_utc TEXT NOT NULL`, `tokens_in INTEGER`,
`tokens_out INTEGER`, `cache_read INTEGER`, `cache_write INTEGER`,
`cost_usd REAL`, `cost_basis TEXT NOT NULL CHECK (cost_basis IN (...))` and
`evidence_ref TEXT`. NOT NULL: exactly three — `call_id`, `ts_utc`,
`cost_basis`. NULLable: the other ten, `job_id` and `task_id` among them.
NO column carries a SQL DEFAULT: the CREATE TABLE statement has no DEFAULT
clause anywhere (`token_ledger.py:178-192`). Defaults exist only in Python, on
`CallRecord` (`token_ledger.py:203-228`), where every field except `call_id`
and `ts_utc` defaults to `None` and `cost_basis` defaults to
`COST_BASIS_UNKNOWN` = `"unknown"` (`token_ledger.py:129`). The CHECK list is
generated from `COST_BASES` (`token_ledger.py:132-134`, `:153`), so the schema
and the constant cannot drift apart. The same migration step creates
`meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)` (`:172-175`) and three
indexes, on `job_id`, on `ts_utc` and on `(role, model)` (`:195-197`). The
column order is restated once as `_CALL_COLUMNS` (`:137-151`), which both the
INSERT (`:422-428`) and `verify_ledger`'s SELECT (`:688-692`) build from.

Q2. The write path: the ONE call site the module names
(`pingpong_evidence.write_evidence_bundle`) — its `path:line`, what it receives,
and specifically whether the prompt-trace entries (or anything carrying a
`segment_manifest`) are in scope AT THAT POINT or only reachable from disk.

A2. `write_evidence_bundle` is `packages/orchestration/pingpong_evidence.py:442`
(body through `:538`). Its one ARMED caller is `_write_task_run_evidence`, which
passes the ledger target at `packages/orchestration/job_evidence.py:2536-2542`
(`ledger_project_id=`, `ledger_job_id=job_id`, `ledger_task_id=task.task_id`);
the project id is resolved once, higher up, at `job_evidence.py:216-221`. What
the function RECEIVES is `bundle`, a plain dict built by
`build_evidence_bundle(run_data, promotion_data)` (`job_evidence.py:2523`), plus
`bundle["prompt_trace_jsonl_path"]` — a PATH STRING, set at
`job_evidence.py:2526-2530` only when that file exists (the same assignment
appears at `pingpong_evidence.py:629-631`). No `PromptTraceEntry` object travels
in the bundle, so nothing carrying a `segment_manifest` is in scope at that
point. The hook is tighter still: `_record_finalized_call_in_ledger`
(`pingpong_evidence.py:546`) is called at `pingpong_evidence.py:517-525`,
immediately after `provider_evidence.json` is written and BEFORE the trace file
is copied into the bundle at `pingpong_evidence.py:527-536`; and it re-reads
only `provider_evidence.json` and `token_accounting.json` from disk, through
`call_record_from_evidence` (`pingpong_evidence.py:574-589`,
`token_ledger.py:513-583`). A manifest is therefore reachable ONLY from disk,
and at hook time only from the run-dir source path — the bundle-local
`task_runs/<task_id>/prompt_trace.jsonl` does not exist yet.

Q3. The trace file: the exact path pattern `prompt_trace.jsonl` is written to,
its writer's `path:line`, and whether anything deletes, rotates or truncates it
after a run — quote the code you checked, or state that a search found no
deleter and name the search.

A3. Two path families, both live.
(1) `<remedy_data_root>/pingpong_runs/<run_id>/prompt_trace.jsonl`, written by
`_persist_run` at `packages/orchestration/pingpong_loop.py:3492`, the directory
coming from `_pingpong_runs_dir` (`pingpong_loop.py:3473-3476`). This is the
file the exporter copies into the evidence tree as
`task_runs/<task_id>/prompt_trace.jsonl` — the path is handed over at
`job_evidence.py:2526-2530` and the copy happens at
`pingpong_evidence.py:528-536`.
(2) `<runs_root>/<job_id>/prompt_trace.jsonl`: `log.path.parent` is
`<runs_root>/<job_id>/` per `packages/orchestration/run_log.py:97` and
`:115-117`. The planner writes there (`apps/cli/commands/job.py:281`), `remedy
do` writes there (`apps/cli/commands/do_cmd.py:382`) and appends there
(`do_cmd.py:2926`); `orchestrator_loop.py:1169-1172` appends, and
`mission_compiler.py:765` appends to `evidence_dir / "prompt_trace.jsonl"`.
Truncation: YES — by the writer itself, not by any cleanup job.
`write_trace_jsonl` opens its path in mode `"w"`: `with path.open("w") as f`
(`packages/orchestration/prompt_trace.py:195`). The comment above
`append_trace_jsonl` states the consequence in full: "Two writers, because the
trace file is per JOB and not per run: `RunLogWriter.path.parent` is
`<runs_root>/<job_id>/`, so a second command against the same job would truncate
the first command's traces if it used `write_trace_jsonl`."
(`prompt_trace.py:200-204`). `do_cmd.py:202-205` repeats it as the reason that
command collects one list and writes once. `append_trace_jsonl`
(`prompt_trace.py:205-210`) is the non-truncating writer.
Deleter or rotation: NOT FOUND. Search run:
`grep -rn "prompt_trace" --include=*.py packages/ apps/ scripts/ | grep -i
"unlink\|remove\|rmtree\|delete\|truncate\|rotate"` — zero matches. A wider
`grep -rn "unlink()\|rmtree(" --include=*.py packages/orchestration/` returns
only staging, snapshot, worktree, checkpoint, patch-revert and job-promote
paths; none of them touches a runs or `pingpong_runs` trace file.

Q4. Schema versioning: how the module versions its schema (the `meta` row), its
`path:line`, and whether an ADDITIVE column has ever been migrated there before.
If yes, cite that migration; if no, say so — that absence is the fact T001 needs.

A4. `SCHEMA_VERSION = 1` (`packages/orchestration/token_ledger.py:102`) is
stored in the `meta` table under the key `"schema_version"`
(`SCHEMA_VERSION_KEY`, `:105`; the table at `:172-175`). Migrations are NUMBERED
STEPS in `_MIGRATIONS: dict[int, tuple[str, ...]]` (`:169-199`), applied by
`_migrate_to_current` (`:1072-1089`): it reads the stored version, runs every
version above it in numeric order, and commits each version's statements
together with its own meta bump, so a ledger never claims a version it does not
have. `_read_schema_version` returns 0 when the `meta` table or the key is
absent (`:1054-1069`), and `open_ledger` runs the migration on every open
(`:373-394`).
Has an ADDITIVE column ever been migrated? NO. `_MIGRATIONS` holds exactly one
key, `1` (`:170`), and its statements are CREATE TABLE / CREATE INDEX only
(`:171-197`). `grep -rn "ALTER TABLE" --include=*.py .` returns no match
anywhere in the repository, and
`git log --oneline -S "_MIGRATIONS" -- packages/orchestration/token_ledger.py`
names a single commit, `b00ffa41 feat(f103): add the SQLite token ledger schema
and writer`. The mechanism exists and has never been exercised past its first
step.

Q5. Readers: every place that SELECTs from the ledger today, with `path:line`,
and how each behaves when a column is NULL or a row is missing. Note any
existing "unattributed"/"no data" rendering precedent.

A5. Four SELECTs exist, all of them inside `token_ledger.py`:
- `record_call`'s disambiguation probe, `token_ledger.py:437-439`. After an
  `INSERT OR IGNORE` (`:425-428`) reported `rowcount == 0`, it asks
  `SELECT 1 FROM calls WHERE call_id = ?`. A row present means an idempotent
  re-record and the call returns True; NO row means a constraint rejected the
  write, so it raises (`:441-445`), is caught at `:447-455`, counts a miss and
  returns False. Fact for T001: `INSERT OR IGNORE` never UPDATEs, so a second
  write for the same `call_id` cannot add anything to a row already present.
- `verify_ledger`, `token_ledger.py:688-692`: selects `_CALL_COLUMNS` for one
  `job_id` and rebuilds a `CallRecord` per row. A missing row lands in
  `missing_rows` (`:696-699`); a row that differs from the record re-derived
  from evidence lands in `drifted_rows` (`:700-701`), and the comparison is
  whole-dataclass equality, so any column the evidence side cannot reproduce
  would make every existing row read as drift. A row with no matching evidence
  is an orphan (`:703-706`). Nothing is ever corrected (`:644-648`).
- `_cost_bucket_rows`, `token_ledger.py:896-903`, the statement behind
  `query_cost` (`:711-772`). NULLs are preserved: the measurement columns are
  `SUM`med, so an all-NULL bucket stays `None` (`:885-891`, `:735-739`); the two
  basis columns are `COUNT`ed, because zero IS the honest value for a count; a
  NULL group column becomes `bucket=None` (`:908-921`, and `CostRow`'s own
  docstring at `:285-307`). A ledger file that does not exist yields an EMPTY
  report with `ledger_exists=False` rather than an error, and does not create
  the database (`:741-743`, `:757-760`).
- `_read_schema_version`, `token_ledger.py:1056-1063`, covered in A4.
Downstream readers: `apps/cli/commands/stats_ledger_cmd.py:266-301`
(`_load_ledger_reports`, feeding `stats cost` and `stats cache` via `query_cost`
at `:291` and `merge_cost_reports` at `:301`), `:469-477`
(`stats backfill-ledger`), `:499-507` (`stats verify-ledger`), and
`packages/orchestration/budget_guard.py:645-671`
(`collect_ledger_cost_for_job`), which is called from the run safe point
(`packages/orchestration/pingpong_job.py:1926-1941`) and from `remedy job
budget` (`apps/cli/commands/job.py:2207-2221`). Both budget callers swallow
every exception and leave the cost `None` — never 0.0
(`pingpong_job.py:1949-1958`, `job.py:2222-2237`).
Rendering precedent for "no data": strong, and the established spelling is
UNMEASURED, not "unattributed". `UNMEASURED = "unmeasured"`
(`stats_ledger_cmd.py:44`) is what `_figure` prints for any `None`
(`:188-194`, and again in the cache view at `:352`); a NULL group column prints
as `"(unnamed)"` (`:220` and `:421`); an absent ledger prints "No ledger on disk
for this scope — nothing has been recorded yet." (`:210-215`); and a partly or
fully unmeasured total gets a sentence in words rather than a silent number
(`:249-261`). The json surface carries `"unmeasured_notation": "null"` beside
the note "a null figure was never reported — it is not a zero; no price is ever
computed" (`:173-182`). The word "unattributed" does not occur in any Python
file: `grep -rn "unattributed" --include=*.py .` returns nothing.

Q6. Correlation: whether a prompt-trace entry can be tied to a ledger row from
the data alone — check which of `job_id`, `task_id`, `run_id` a trace entry
actually carries at the planner, builder and reviewer call sites (a field that
exists in the dataclass but is left empty at a call site is NOT a correlation
key; cite the call site).

A6. The dataclass carries all three fields — `run_id`, `job_id`, `task_id`, each
defaulting to `""` (`packages/orchestration/prompt_trace.py:60-62`) — and
`build_trace_entry` passes them straight through (`:104-172`, assignment at
`:141-143`). What the call sites actually FILL:
- PLANNER, `apps/cli/commands/job.py:240-252`: `job_id=str(job.id)` and nothing
  else. `task_id` and `run_id` are not passed at all, so both stay `""`.
- BUILDER, `packages/orchestration/pingpong_loop.py:2828-2845`:
  `run_id=result.run_id`, `job_id=result.job_id`, `task_id=result.task_id`
  (`:2831-2833`).
- REVIEWER, `packages/orchestration/pingpong_loop.py:3020-3041`: the same three
  (`:3023-3025`).
But `result.job_id` / `result.task_id` are only as full as the caller of
`run_pingpong` made them: the parameters default to `""`
(`pingpong_loop.py:2446-2447`), are copied onto the result at `:2493-2494`, and
the field itself defaults to `""` on `PingPongResult`
(`pingpong_loop.py:103`). The JOB path fills them —
`packages/orchestration/pingpong_job.py:2255-2256` passes
`job_id=job.job_id, task_id=task.task_id`. The standalone `remedy do` path does
NOT: `apps/cli/commands/do_cmd.py:800-820` passes neither, so builder and
reviewer traces produced by that command carry an empty `job_id` and `task_id`.
Against the row: the ledger identity is `"<job_id>:<task_id>"`
(`call_id_for_task_run`, `token_ledger.py:465-489`, which REFUSES an empty
half), and there is no `run_id` column on the row at all (`_CALL_COLUMNS`,
`token_ledger.py:137-151`). So, from the data alone: builder and reviewer trace
entries written through the job path DO carry both halves of a `call_id` and can
be tied to a row; planner trace entries CANNOT — no `task_id`, and no ledger row
is written for planning in any case, since rows are derived only from
`task_runs/<task_id>/provider_evidence.json` (`token_ledger.py:513-583`); and
`remedy do` traces cannot, both halves being empty. One id-free path also
exists: `evidence_ref` on the row is `"task_runs/<task_id>"`
(`token_ledger.py:547-549`, assigned at `:573`), which is exactly the directory
the trace file is copied into (`pingpong_evidence.py:533`).
