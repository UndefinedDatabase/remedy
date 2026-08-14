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
