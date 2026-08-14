# F082 T001 — gauntlet-harness inventory (R2, read-only)

Every answer below was read out of the source at branch head. Citations are
`path.py::symbol`, never bare line numbers (R-0353). "Not present" names where
the search ran and is a real answer, not a gap.

## Q1

`packages/orchestration/gauntlet_runner.py::run_order` — the seam the bench
runs through.

    def run_order(order: GauntletOrder, *, campaign_root: Path, real_data_root: Path,
                  deps: RunnerDeps | None = None,
                  index: int = 1) -> OrderOutcome:

It writes `run.json` (and `dod_result.json` when a gate verdict exists) into
`campaign_root / f"run-{index:02d}-{order.id}"` and returns an `OrderOutcome`.

`gauntlet_runner.py::OrderOutcome` — FIVE fields, all of them:

    order_id: str
    run_dir: Path
    terminal_status: str
    crashed: str = ""
    body: dict[str, Any] = field(default_factory=dict)

`body` is the same dict serialised to `run.json`, built by
`gauntlet_runner.py::_evidence_body`.

`gauntlet_runner.py::RunnerDeps` — ELEVEN callable fields, every one defaulting
to the production verb: `make_project`, `create_mission`, `plan_mission`,
`run_mission`, `load_mission`, `plan_call_fn`, `move_call_fn`, `materialise`,
`dispatch_fn`, `update_dossier_fn`, `execute_fn`. Its docstring states the
substitution contract:

    A dataclass of callables rather than module-level monkeypatching: the tests
    hand over doubles at the call site, and production never learns that tests
    exist.

Six of them — `create_mission`, `plan_mission`, `run_mission`, `load_mission`,
`materialise`, `execute_fn` — are declared `None` and bound in
`RunnerDeps.__post_init__` to avoid import at module load.

## Q2

The record F082 requires is `{order_id, series, pass, cost, wall_s,
repair_rounds, postmortem_classes}`. Field by field, against
`gauntlet_runner.py::OrderOutcome` and the `run.json` body it carries:

- `order_id` — EXISTS VERBATIM. `OrderOutcome.order_id`, and `_evidence_body`
  writes `"order_id": order.id`.
- `series` — NO SOURCE AT ALL. `grep -rn "series" packages/orchestration/`
  (excluding `serial*`) returns nothing. The bench must define it.
- `pass` — DERIVABLE, not present. `OrderOutcome` carries only
  `terminal_status`; the pass judgement is
  `gauntlet_evaluator.py::evaluate_run` returning `RunVerdict.flawless` over
  the run's recorded evidence.
- `cost` — PARTLY DERIVABLE. Token counts come from
  `gauntlet_runner.py::measure_tokens` into `body["tokens"] = {"in", "out"}`,
  or `body["tokens_source"] = "unmeasured"`. Money has NO source in gauntlet
  evidence: see Q5.
- `wall_s` — EXISTS, under a different name. `_evidence_body` writes
  `"wall_seconds": round(wall, 3)`; see Q8.
- `repair_rounds` — NO SOURCE on this path; see Q7.
- `postmortem_classes` — DERIVABLE.
  `gauntlet_matrix.py::postmortem_classes` already computes exactly this
  tuple from a `RunVerdict`; see Q6.

## Q3

`packages/orchestration/gauntlet_orders.py::GauntletOrder` — a frozen
dataclass with ELEVEN fields: `id`, `kind`, `title`, `rationale`,
`risk_probed`, `goal`, `milestones`, `budget`, `injections`, `file_name`,
`sha256`.

The set is declared by `scripts/gauntlet_orders/manifest.json`, whose top-level
keys are exactly `gauntlet_order_set_version`, `orders`, `set_hash`,
`template_digest`; each `orders` entry carries exactly `file`, `id`, `sha256`.
`gauntlet_orders.py::default_orders_dir` fixes the location:

    return root / "scripts" / "gauntlet_orders"

Ten order files live there (`g01-…json` … `g10-…json`) plus `manifest.json`.

Version/freeze tags today, and what F082 still needs:

- Per ORDER FILE there is a SCHEMA version only: every one of the ten carries
  `"gauntlet_order_version": 1` (`grep -h` over the ten files returns
  `10  "gauntlet_order_version": 1,`), checked by
  `gauntlet_orders.py::load_order`. It is not a freeze tag — it never varies
  per order and never changes when an order's text changes.
- Per SET there is `GAUNTLET_ORDER_SET_VERSION = 4`, bumped by a human.
- The actual freeze is by DIGEST, in `gauntlet_orders.py::load_order_set`:

    _require(order.sha256 == str(entry.get("sha256", "")),
             f"{order.file_name}: sha256 {order.sha256} does not match the "
             f"manifest ({entry.get('sha256')}) — the frozen set was edited")

So: editing an order file WITHOUT updating the manifest already fails
validation. But editing the order AND recomputing the manifest digests passes
with no version bump anywhere — nothing forces a bump. F082's acceptance
("Changing an order file without bumping its version fails validation") is
therefore NOT satisfied by today's mechanism; a per-order version field and a
check that it moved when the digest moved is NEW work for R3.

## Q4

The pass definition lives in
`packages/orchestration/gauntlet_evaluator.py::evaluate_run`, which fills
`RunVerdict.flawless`:

    return RunVerdict(..., flawless=not failures, criteria=criteria, ...)

The frozen definition itself is `gauntlet_evaluator.py::PASS_CRITERIA` (nine
criterion ids), and its comment names the constraint F082's Do-not-touch list
repeats:

    #: The pass definition, in report order. Changing this tuple changes what
    #: "flawless" means and therefore needs an ADR (T1_F075.md, Do not touch).

CALLING it without editing it is possible, and is the intended use:
`gauntlet_evaluator.py::evaluate_evidence_dir` is a pure function over an
evidence directory (`evaluate_evidence_dir(evidence_dir, only=None)`), takes no
gauntlet-specific config, and is already called that way by
`scripts/self_run_gauntlet.py`. The bench can therefore reuse the pass
definition as a library call and record its own metrics around the returned
`RunVerdict` — no edit to the evaluator is needed.

## Q5

`packages/orchestration/gauntlet_runner.py::measure_tokens` returns
`dict[str, int] | None`:

    return {"in": total_in, "out": total_out} if measured else None

`None` is not zero — `_evidence_body` then writes `tokens_source:
"unmeasured"` and NO `tokens` key.

Where the numbers really come from: `orchestrator_loop.py::measure_call_cost`
builds each ledger entry's `cost`, reading the claude-CLI envelope through
`token_actuals.py::parse_cli_result`:

    cost["usage"] = {
        "input_tokens": actuals.input_tokens,
        "output_tokens": actuals.output_tokens,
        ... "total_cost_usd": actuals.total_cost_usd,

MONEY exists there — `token_actuals.py::UsageActuals.total_cost_usd` — but
`measure_tokens` never reads it, so no money reaches `run.json`.

KEY MISMATCH, verified rather than assumed. `measure_tokens` sums:

    total_in += int(usage.get("prompt_tokens", 0) or 0)
    total_out += int(usage.get("completion_tokens", 0) or 0)

while the only production writer of that dict, `measure_call_cost`, writes
`input_tokens`/`output_tokens`. `grep -rn "prompt_tokens" packages/ apps/
scripts/ tests/` finds no producer of those keys on the mission-ledger path;
the single gauntlet-side use is the test double
`tests/orchestration/test_gauntlet_runner.py::ledger_entry`, which builds
`"usage": {"prompt_tokens": …, "completion_tokens": …}`. Against a real run the
sum would be `{"in": 0, "out": 0}` with `measured=True`. This is reported as an
observation for R3, not repaired here — this round writes no production line.

Basis labels the repo already uses, which F082's cost comparison must respect:

- `token_ledger.py::COST_BASIS_PROVIDER_REPORTED` = `"provider_reported"`,
  `COST_BASIS_PRICE_TABLE` = `"price_table"`, `COST_BASIS_UNKNOWN` =
  `"unknown"` — the enumerated `COST_BASES`, enforced by a SQL CHECK on
  `calls.cost_basis`.
- `gauntlet_evidence.py::TOKENS_SOURCE_MEASURED` / `TOKENS_SOURCE_UNMEASURED`
  — the token-side basis carried in `run.json` and read into
  `RunEvidence.tokens_measured`.
- `orchestrator_loop.py::USAGE_UNMEASURED` = `"unmeasured"`, the ledger-entry
  spelling of the same idea.

## Q6

`packages/orchestration/gauntlet_runner.py::collect_postmortems` returns
`list[dict[str, Any]]`, one dict per `postmortem.json` found under the run's
isolated data root, with exactly three keys:

    records.append({"scope": str(body.get("scope", "")),
                    "failure_class": str(body.get("failure_class", "")),
                    "detail": str(body.get("raw_reason", ""))[:400]})

The "class" is the `failure_class` key; its vocabulary is
`failure_postmortem.py::FailureClass` (the evaluator compares against
`FailureClass.UNKNOWN.value` in `gauntlet_evaluator.py::_check_postmortems`).

The exact list F082 wants already exists as a function:
`gauntlet_matrix.py::postmortem_classes`, deduplicated in first-seen order,
substituting `"(absent)"` for an empty class. `gauntlet_matrix.py::_run_payload`
already puts it in the matrix payload under the key
`"postmortem_classes"` — the same name F082's record uses.

## Q7

NOT PRESENT on the gauntlet path. Where I looked and what is there:

- `grep -rn "repair_round" packages/ apps/ scripts/ tests/` — the counter
  exists, at `long_run_executor.py::CycleRecord.repair_rounds_used`:

    #: F052: repair rounds this cycle actually spent on a FAILED verify.
    repair_rounds_used: int = 0

  and `CycleRecord.to_json` serialises it.
- It does NOT reach the gauntlet. `orchestrator_loop.py::execute_dispatched_job`
  returns `orchestrator_loop.py::JobExecution`, whose fields are
  `terminal_status`, `job_status`, `stop_reason`, `resolved_cycles`,
  `gate_released`, `gate_blocker` — the per-cycle records are dropped at that
  boundary. `gauntlet_runner.py::_evidence_body` has no repair field, and
  `gauntlet_evidence.py::RunEvidence` has none either.
- Job-level counters exist for the pingpong path only:
  `job_evidence.py` renders `task.repair_rounds_used` /
  `execution_config.repair_rounds_allowed`. A gauntlet mission does not produce
  those task records.

NEAREST STANDING-IN SIGNAL, already inside each run's own evidence:
`long_run_executor.py::LEDGER_EVENT_CYCLE_REPAIR_ROUND` = `"cycle_repair_round"`
is emitted once per repair round that really ran, through the `RunLogWriter`
the gauntlet already wires in `execute_dispatched_job`
(`log=RunLogWriter(job_id=job.id)`). That writer appends to
`<data_root>/runs/<job_id>/<run_id>.jsonl` (`run_log.py::RunLogWriter.path`),
and the gauntlet's data root is `run_dir/data`, so the events are inside the
run directory the bench already owns. Counting those events is derivation from
recorded evidence, not a new measurement.

## Q8

PRESENT. `gauntlet_runner.py::_evidence_body` writes:

    "wall_seconds": round(wall, 3),

measured by `run_order` as `time.monotonic() - started`, and the crash path
records it too. It is loaded back by `gauntlet_evidence.py::RunEvidence` as
`wall_seconds: float = 0.0`, surfaced by
`gauntlet_evaluator.py::RunVerdict.to_json` as `"wall_seconds"`, and rendered
by `gauntlet_matrix.py::_wall`. F082's `wall_s` is a rename of an existing
measured field, not new measurement.

## Q9

What a campaign produces today, and who writes it:

- PER RUN: `run.json` — always — and `dod_result.json` when a gate verdict
  exists. Both written by `gauntlet_runner.py::run_order`:

    (run_dir / RUN_FILENAME).write_text(
        json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")

  Names come from `gauntlet_evidence.py::RUN_FILENAME` and
  `DOD_RESULT_FILENAME`. The run directory also holds the run's isolated data
  root (`ISOLATED_ROOT_DIRNAME = "data"`) and its workspace copy
  (`WORKSPACE_DIRNAME = "workspace"`).
- PER CAMPAIGN: `matrix.md` + `matrix.json`, written by
  `gauntlet_matrix.py::write_matrix` (constants `MATRIX_MARKDOWN_FILENAME`,
  `MATRIX_JSON_FILENAME`), called from `scripts/self_run_gauntlet.py` after
  `evaluate_evidence_dir(campaign_root)`.

Can it be reused as-is for F082's "full evidence bundle per run"? The per-run
directory can: it is already self-contained, deterministic and written
unconditionally, including on a crash. The campaign matrix can be reused only
as a REPORT — `matrix_json` is keyed to the pass/flawless framing
(`runs_flawless`, `passed`, `pass_criteria`), not to a metrics trend.
Not present: any call from the gauntlet into the job-level bundle exporter
`job_evidence.py::export_job_evidence`; `grep -rn "export_job_evidence"` finds
no gauntlet caller, so "full evidence bundle" in that sense does not exist on
this path today.

## Q10

`packages/orchestration/data_paths.py::projects_dir` is the data root's PROJECT
area:

    def projects_dir(root: Path | None = None) -> Path:
        """Return the projects storage directory (<root>/projects)."""
        return (root if root is not None else resolve_data_root()) / "projects"

The root itself is `data_paths.py::resolve_data_root`. `data_paths.py` has no
bench-specific helper today — adding one there is the module's own convention
(every area gets a named helper).

APPEND-ONLY `.jsonl` WRITER TO FOLLOW rather than invent:
`orchestrator_loop.py::append_ledger_entry` is the closest precedent and states
the contract F082's history needs:

    Append-only is the point: a ledger a later iteration could edit would prove
    nothing about the iterations before it.

    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(body, sort_keys=True) + "\n")

Its reader `orchestrator_loop.py::read_ledger` skips a torn last line instead
of raising — the property F082's "history survives across runs" wants. The
second precedent is `run_log.py::RunLogWriter.log`, same open-append-write-line
shape into `<root>/runs/<job_id>/<run_id>.jsonl`.

## Q11

The seven test files were enumerated mechanically by parsing each file's AST
(`.remedy-wt/f082_r2_imports.py`), listing every `ImportFrom` whose module name
contains `gauntlet`. I LISTED SEVEN FILES — the count is 7, and the glob
`tests/orchestration/test_gauntlet_*.py` plus
`tests/orchestration/test_self_run_gauntlet.py` returns exactly those seven.

1. `tests/orchestration/test_gauntlet_evaluator.py` — from
   `gauntlet_evaluator`: `ACCEPTED_DISPOSITIONS`, the nine `CRITERION_*`,
   `DISPOSITION_CORRUPTED_ARTIFACT_ACCEPTED`, `DISPOSITION_SILENT_SUCCESS`,
   the nine `FAILURE_*` plus `FAILURE_KINDS`, `INJECTION_CLASSES`, the four
   `INJECTION_*` classes, `PASS_CRITERIA`, `REJECTED_DISPOSITIONS`,
   `evaluate_evidence_dir`, `evaluate_run`; from `gauntlet_evidence`:
   `load_run`.
2. `tests/orchestration/test_gauntlet_evidence.py` — from `gauntlet_evidence`:
   `DOD_RESULT_FILENAME`, `GAUNTLET_RUN_VERSION`, `RUN_FILENAME`,
   `TOKENS_SOURCE_UNMEASURED`, `load_run`, `run_dirs`; from
   `gauntlet_evaluator`: `evaluate_run`.
3. `tests/orchestration/test_gauntlet_injection.py` — from
   `gauntlet_injection`: `BLOCKED_INJECTIONS`, `INJECTION_ERRORS`,
   `INJECTION_SEAMS`, `MissingSeamError`, `RaiseOnceInjector`,
   `RunOutcomeFacts`, `SUPPORTED_INJECTIONS`, `TruncatedResponseInjector`,
   `build_injectors`, `check_injections_supported`, `injection_json`; from
   `gauntlet_evaluator`: `CRITERION_INJECTIONS_DEGRADED`, the five
   `DISPOSITION_*` (`ESCALATED`, `LEDGERED`, `NEVER_FIRED`, `RETRIED`,
   `SILENT_SUCCESS`), `INJECTION_CLASSES`, the four `INJECTION_*`,
   `REJECTED_DISPOSITIONS`, `evaluate_run`; from `gauntlet_evidence`:
   `load_run`.
4. `tests/orchestration/test_gauntlet_matrix.py` — from `gauntlet_matrix`:
   `MATRIX_JSON_FILENAME`, `MATRIX_MARKDOWN_FILENAME`, `MATRIX_VERSION`,
   `TOKENS_UNMEASURED_LABEL`, `matrix_json`, `matrix_json_bytes`,
   `render_matrix_markdown`, `write_matrix`; from `gauntlet_evaluator`:
   `DISPOSITION_SILENT_SUCCESS`, `FAILURE_INJECTION_NOT_DEGRADED`,
   `FAILURE_TERMINAL_NOT_GREEN`, `INJECTION_HARNESS_DEATH_MID_WRITE`,
   `PASS_CRITERIA`, `evaluate_evidence_dir`.
5. `tests/orchestration/test_gauntlet_orders.py` — from `gauntlet_orders`:
   `BUDGET_KEYS`, `GAUNTLET_ORDER_COUNT`, `GAUNTLET_ORDER_SET_VERSION`,
   `GAUNTLET_ORDER_VERSION`, `GauntletOrder`, `MANIFEST_FILENAME`,
   `ORDER_KINDS`, `OrderSetError`, `compute_set_hash`, `default_orders_dir`,
   `default_template_dir`, `file_sha256`, `load_manifest`, `load_order`,
   `load_order_set`, `template_tree_digest`; from `gauntlet_evaluator`:
   `INJECTION_CLASSES`.
6. `tests/orchestration/test_gauntlet_runner.py` — imports the MODULE
   `packages.orchestration.gauntlet_runner` itself plus `ABSENT_ROOT_DIGEST`,
   `ENV_DATA_ROOT`, `ENV_MAX_TOKENS`, `ENV_MAX_WALL_MINUTES`,
   `ISOLATED_ROOT_DIRNAME`, `RunnerDeps`, `TOKENS_UNMEASURED`,
   `_default_execute_fn`, `data_root_digest`, `isolated_environment`,
   `materialise_sample_project`, `measure_tokens`, `run_campaign`,
   `run_order`; from `gauntlet_evaluator`: `CRITERION_DATA_ROOT_UNTOUCHED`,
   `CRITERION_INJECTIONS_DEGRADED`, `DISPOSITION_LEDGERED`,
   `DISPOSITION_SILENT_SUCCESS`, `evaluate_evidence_dir`; from
   `gauntlet_evidence`: `RUN_FILENAME`, `load_run`; from `gauntlet_injection`:
   `MissingSeamError`; from `gauntlet_orders`: `GauntletOrder`,
   `template_tree_digest`.
7. `tests/orchestration/test_self_run_gauntlet.py` — imports the module
   `self_run_gauntlet` (the script, by path) plus, from `gauntlet_matrix`:
   `MATRIX_JSON_FILENAME`, `MATRIX_MARKDOWN_FILENAME`; from `gauntlet_orders`:
   `GauntletOrder`, `load_order_set`.

Plainly: EVERY symbol listed above CANNOT be moved or renamed without editing
one of those seven files. That includes the module paths themselves —
`gauntlet_runner`, `gauntlet_orders`, `gauntlet_evidence`, `gauntlet_evaluator`,
`gauntlet_matrix`, `gauntlet_injection` and `scripts/self_run_gauntlet.py` — and
the private `gauntlet_runner._default_execute_fn`, which a test imports by name
despite its underscore.

Cross-test couplings widen the blast radius, so they are named here.
`test_gauntlet_evaluator.py`, `test_gauntlet_injection.py`,
`test_gauntlet_matrix.py` and `test_self_run_gauntlet.py` all import shared
fixtures out of one test module —
`tests/orchestration/test_gauntlet_evidence.py::write_run`,
`::FLAWLESS_BODY`, `::RELEASED_GATE`, `::RECORDED_DIR`, `::GOLDEN_DIR` — and
`test_self_run_gauntlet.py` additionally imports
`tests/orchestration/test_gauntlet_runner.py::Recorder` and
`tests/orchestration/test_gauntlet_runner.py::an_order`. Those test-side
fixtures are as frozen as the production names.

The workable conclusion for R3: the factoring must be ADDITIVE. New shared
helpers may be introduced and the bench may call the existing symbols, but no
existing gauntlet symbol may be moved, renamed or deleted, because each one is
imported by name.

## Q12

PARTLY PRESENT, and NOT on the gauntlet path.

- Per-call recording exists: `token_ledger.py::CallRecord` carries `role` and
  `model` side by side, with `cost_basis`:

    role: str | None = None
    model: str | None = None

  and `token_ledger.py::COST_GROUP_KEYS = ("role", "model", "day")` groups
  cost by them. Its writer is `token_ledger.py::record_call`, called from
  `pingpong_evidence.py` — the job/pingpong path.
- Per-job role→model mapping exists: `run_manifest.py::_models_for_job`
  returns `{"builder": provider/model, "reviewer": …}` (plus `"repair"` when
  configured), stored as `models: dict[str, str]` on the manifest snapshot.
- Per-call prompt traces can carry it:
  `prompt_trace.py::build_trace_entry` takes `role`, `provider`,
  `provider_kind` and `configured_model`.

NOT PRESENT for a gauntlet mission run: nothing records which model served
which role. `orchestrator_loop.py::run_mission` accepts `provider`,
`provider_kind` and `on_call`, and
`orchestrator_loop.py::make_orchestrator_call_recorder` would write a trace
with `role="orchestrator"` — but `gauntlet_runner.py::run_order` passes NONE of
those three when it calls `deps.run_mission(...)`; it passes only `call_fn`,
`dispatch`, `update_dossier` and `execute`. The runner says so deliberately:

    # Remedy deliberately does NOT name the provider here, so these
    # rows reach evidence unlabelled (DECISION F105 D13).

The model the orchestrator role actually uses is resolved inside
`gauntlet_runner.py::_default_move_call_fn` from
`get_config().get("orchestrator.model")`, and that value is never written into
`run.json`. Recording it for F082 means passing the existing seams at the
existing call site — a record, not a routing change.

## What this means for R3

REUSE UNCHANGED (call it, do not touch it):
- `gauntlet_evaluator.py::evaluate_evidence_dir` / `evaluate_run` /
  `PASS_CRITERIA` — the pass definition, on F082's Do-not-touch list.
- `gauntlet_runner.py::run_order` / `run_campaign` / `RunnerDeps` — the
  execution seam, including its isolation and crash-evidence contract.
- `gauntlet_orders.py::load_order_set` and its digest freeze, pointed at the
  bench's own orders directory via the existing `orders_dir` parameter.
- `gauntlet_evidence.py::load_run` / `run_dirs` — the never-raising reader.
- `gauntlet_matrix.py::postmortem_classes` — already the exact
  `postmortem_classes` field.
- `orchestrator_loop.py::append_ledger_entry` as the append-only JSONL pattern
  for `bench_history.jsonl`.

FACTOR OUT (additively — no existing symbol moves; see Q11):
- The order-directory + manifest freeze so a second frozen set can be loaded
  without duplicating `load_order_set`'s checks. `default_orders_dir` is
  already parameterised, so the factoring is a caller-side choice, not a move.
- A shared "campaign root → per-run record" step, so the bench derives its row
  from the SAME `run.json` the gauntlet writes rather than a parallel one.

BUILD NEW:
- `series`, and the per-order version tag plus the validation that a changed
  order without a bumped tag fails (Q3).
- `repair_rounds` derivation from the `cycle_repair_round` run-log events (Q7).
- Money cost, and the token-key mismatch in `measure_tokens` (Q5) — R3 must
  decide whether the bench reads the ledger itself or the runner is corrected.
- The bench record writer, the history file under the projects area (Q10), and
  the model/role context capture at the existing seams (Q12).

MUST NOT TOUCH:
- `gauntlet_evaluator.py::PASS_CRITERIA` and the criterion functions.
- Any symbol enumerated in Q11, and the seven test files themselves.
- Routing: F082 records model context, it does not choose models.

## S1..S4 — the sample project (R4)

Every claim below was read out of `scripts/gauntlet_sample_project` at branch
head. Citations are `path::symbol` or a real file path, never bare line numbers
(R-0353). "Not present" names where the search ran and is a real answer.

### S1 — what is actually in the sample project

ONE language: Python. `find scripts/gauntlet_sample_project -type f` returns
only `.py` and `.md` files plus `__pycache__` droppings — there is no
`package.json`, no `pyproject.toml`, no `requirements.txt`, and no `.js`,
`.ts`, `.jsx`, `.tsx`, `.vue`, `.html` or `.css` file anywhere in the tree.

The package is `scripts/gauntlet_sample_project/sampleproj/`, SEVEN modules
beside its `__init__.py` (which carries only a docstring and
`__version__ = "0.3.0"`), listed here and counted as seven:

- `sampleproj/cli.py::main` — an `argparse` CLI, `prog="sampleproj"`, with two
  subcommands built in `cli.py::build_parser`: `import <source|-> <target>` and
  `report <target>`. Progress to stdout, `error: ` to stderr, exit 2 on
  `errors.py::SampleProjError`.
- `sampleproj/config.py::resolve` — one setting resolved explicit > environment
  > file > built-in, over `config.py::DEFAULTS` (`max_records` 100,
  `retry_attempts` 3, `report_width` 72) and `config.py::ENV_VARS`.
- `sampleproj/parsing.py::parse_record` / `::parse_records` — `name=value`
  lines; malformed input returns `None` deliberately.
- `sampleproj/importer.py::import_records` / `::plan_import` — one file per
  record into a target directory.
- `sampleproj/report.py::build_report` / `::report_dir` — a fixed-width listing.
- `sampleproj/retry.py::backoff_for` / `::backoff_series` — the doubling ladder
  capped at `retry.py::BACKOFF_CAP_SECONDS` (30), hard-coded on purpose.
- `sampleproj/errors.py` — the message constants and `SampleProjError`.

ENTRY POINT: `python3 -m sampleproj.cli` (`cli.py` ends with
`raise SystemExit(main())`), documented in the project's own
`scripts/gauntlet_sample_project/README.md` under "Commands".

TEST RUNNER: pytest, run from inside the project copy —
`scripts/gauntlet_sample_project/README.md` says `python3 -m pytest tests -q`,
and `scripts/gauntlet_sample_project/conftest.py` inserts the project directory
on `sys.path` precisely so the materialised copy is self-sufficient. SIX test
files (`tests/test_cli.py`, `test_config.py`, `test_importer.py`,
`test_parsing.py`, `test_report.py`, `test_retry.py`). Measured, not assumed:
`python3 -m pytest tests -q` inside the template returns `30 passed`.

HOW A MISSION IS EXPECTED TO CHANGE IT: by editing a module and its test in
place inside the run's own workspace copy, with the suite above as the
executable check. The modules say so themselves — `retry.py`'s docstring names
g01, `parsing.py`'s names g06, `importer.py`'s and `report.py`'s both name g05,
`config.py`'s names g02 and g04, `cli.py`'s names g03 and g08. Each existing
gauntlet order has a designated seam already written into the fixture.

### S2 — how the project reaches a workspace, and whether an order may vary it

`gauntlet_runner.py::materialise_sample_project(run_dir, template_dir=None)`
copies `source = template_dir or default_template_dir()` into
`run_dir / WORKSPACE_DIRNAME`, skipping `gauntlet_orders.py::TEMPLATE_IGNORED_DIRS`
(`__pycache__`, `.pytest_cache`, `.git`), then runs `git init` / `add -A` /
`commit` so the mission's work is a diff against a baseline.
`gauntlet_runner.py::_default_make_project` then registers that workspace as a
`project_registry.py::RemyProject` whose `canonical_repo_path` is the copy.

AN ORDER CANNOT SELECT A DIFFERENT TEMPLATE. The parameter exists on the
function, but `gauntlet_runner.py::run_order` calls the seam as
`workspace = deps.materialise(run_dir)` — one positional argument, no template.
The template is therefore a property of the `RunnerDeps` a CAMPAIGN is given
(`RunnerDeps.materialise`), never of the order. The evidence side agrees:
`gauntlet_runner.py::_template_digest` calls `template_tree_digest()` with no
argument, so `run.json` always records the DEFAULT template's digest whatever
was actually copied.

What R2 Q3 implies for a bench order that would need its own fixture: the
template digest is folded into the set freeze
(`gauntlet_orders.py::compute_set_hash(entries, template_digest=...)` and the
`template_digest` check in `::load_order_set`), so adding a second fixture tree
is not a local act — it changes what "the sample project" digests to, and every
frozen gauntlet order's set hash with it. A bench order needing its own fixture
is therefore NEW work at the runner seam plus a freeze change, not a field in an
order file. F082 has not built it.

### S3 — the five capabilities, one answer each

Counted as answered: FIVE questions, numbered 1 to 5. THREE are yes and TWO are
no.

1. A SMALL CLI TOOL — YES. `sampleproj/cli.py::build_parser` is a real argparse
   CLI with two subcommands, and `tests/test_cli.py` already exercises stdout,
   stderr and exit codes. A distinct unclaimed seam exists: `report_width` is a
   real setting in `config.py::DEFAULTS` and `report.py::build_report` already
   accepts `width=`, but `cli.py::main` never passes it and `build_parser`
   offers no such option, so the setting is unreachable from the command line.
   The file that settles it: `scripts/gauntlet_sample_project/sampleproj/cli.py`.

2. AN API ENDPOINT WITH TESTS — NO. There is no HTTP surface of any kind.
   `grep -rniE "http|flask|fastapi|django|server|route|endpoint|socket|wsgi|asgi|uvicorn|requests"`
   over the whole project (`.py`, `.md`, `.txt`, `.json`, `.cfg`, `.toml`)
   returns ZERO hits, and there is no dependency manifest that could declare a
   web framework. The file that settles it: there is none — the absence itself
   is the answer, and `scripts/gauntlet_sample_project/README.md` describes the
   project as "a small records pipeline" with two CLI commands and nothing else.

3. A FRONTEND WIDGET JUDGED BY BUILD PLUS AN HTTP-LEVEL SMOKE — NO. There is no
   frontend and no build step. No `.js`, `.ts`, `.jsx`, `.tsx`, `.vue`, `.html`
   or `.css` file exists in the tree, and no `package.json`; the only non-Python
   files are `README.md` and `CHANGELOG.md`. The HTTP half fails for the same
   reason as capability 2. The file that settles it: the absence of
   `scripts/gauntlet_sample_project/package.json`, and
   `scripts/gauntlet_sample_project/README.md`, which documents a pytest-only
   check.

4. A BUGFIX ON A FIXTURE REPO — YES, and a genuine defect is already present
   rather than needing to be planted. `sampleproj/config.py::DEFAULT_CONFIG_FILENAME`
   is defined as `"sampleproj.conf"` and `grep -rn "DEFAULT_CONFIG_FILENAME"`
   over the project returns exactly ONE hit, its own definition — nothing reads
   it. `config.py::resolve` consults a file only under
   `if config_path is not None`, so with no explicit path the file layer of the
   precedence chain never runs, while
   `scripts/gauntlet_sample_project/README.md` states the chain as explicit >
   environment > "a `sampleproj.conf` file" > built-in default with no such
   condition. Documented behaviour and real behaviour disagree, and no test in
   `tests/test_config.py` covers the unconditional lookup. The file that settles
   it: `scripts/gauntlet_sample_project/sampleproj/config.py`.

5. A REFACTOR WITH UNCHANGED BEHAVIOUR, TEST-PINNED — YES. `cli.py::main`
   interleaves doing and presenting: the `import` branch calls
   `importer.import_records` and then emits three kinds of progress line inline,
   so no caller can obtain the text without printing it. Extracting the
   rendering leaves observable behaviour identical, and `tests/test_cli.py`
   already pins that behaviour through `capsys` on all three of stdout, stderr
   and the return code, so the pin exists without writing it. The file that
   settles it: `scripts/gauntlet_sample_project/tests/test_cli.py`.

Two notes that cost no answer. First, capability 5's target is deliberately NOT
the duplicated path normalisation in `importer.py::import_records` and
`report.py::report_dir` — that is already gauntlet order g05's goal, and a bench
order restating a gauntlet order measures the same thing twice. Second, the kind
vocabulary is frozen at `gauntlet_orders.py::ORDER_KINDS` (five values, none of
them a refactor kind), and `::load_order` refuses any other, so the refactor
order is filed under `pure_code_change` rather than editing that tuple — the
ADDITIVE constraint of Q11 forbids the edit.

### S4 — what is owed, and what would make it yes

The stop clause does NOT fire: three of five are expressible, which is at or
above the threshold of three. Orders are written for capabilities 1, 4 and 5.
Capabilities 2 and 3 are OWED, and F082 HAS NOT BUILT THEM.

- CAPABILITY 2, an API endpoint with tests. Smallest fixture addition: a
  standard-library-only `http.server` module inside `sampleproj` — one
  `BaseHTTPRequestHandler` serving a single read-only route over the records
  the importer already writes, plus a test that starts it on port 0 and asserts
  the status and body. Standard library only, because the project has no
  dependency manifest and adding one is a larger change than the capability.
- CAPABILITY 3, a frontend widget judged by build plus an HTTP-level smoke.
  Smallest fixture addition: capability 2 first, since the smoke is defined at
  the HTTP level, then one static asset the endpoint serves and a "build" step
  that is a checkable transform of it. This is strictly the larger of the two
  and depends on the other.

Neither addition is made in R4, and no order is written for either. Writing an
order that cannot run would be worse than the gap: the freeze makes it
permanent, and a frozen order whose goal has no seam in the project scores every
future run against something the project cannot do.
