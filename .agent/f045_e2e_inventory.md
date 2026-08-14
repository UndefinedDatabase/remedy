# F045 — pipeline inventory for the loop end-to-end round (R12, C2)

A SURVEY of what the code already does. It exists so R13 can author the
end-to-end fixture test from measured facts. Every `file:line` below was
produced by a command in THIS round and is quoted with its symbol, because a
symbol survives an edit above it and a line number does not. Nothing here is
remembered; where a question has no answer, it says "nothing does this" and
shows the command whose empty output proves it. No production file was changed.

## Q1 — how a PLANNED job actually gets EXECUTED

There is no single executor. Three distinct paths exist. Two of them run with
no real provider; only the FIRST is measured below as the one that writes the
report (Q5's probe drove it). Whether the second writes a report was not
determined.

**The cycle loop is the standard pipeline.** Entry point: `run_cycles` in
`packages/orchestration/long_run_executor.py` (`grep -n "^def run_cycles"` →
line 1284), signature
`run_cycles(job, limits, provider_call, *, task_step=None, verify=None, …)`.
Its own docstring states the cycle: "One cycle is: safe point -> ready batch ->
execute -> verify -> persist."

It does NOT read `job.state` to decide whether it may run. `run_cycles` is the
last top-level definition in that 1596-line file, so its body is lines
1284-1596, and:

    $ sed -n 1284,2000p packages/orchestration/long_run_executor.py \
        | grep -c "job\.state"
    0

What it consumes instead is tasks whose `status` is PENDING, through
`ready_tasks` (line 771) and `dag_schedule.ready_set` (line 126), whose
docstring reads "Ids of the PENDING tasks whose dependencies are ALL
completed." The PLANNED state is what `plan_job` in
`packages/orchestration/job_runner.py` (`grep -n "def plan_job"` → line 46)
leaves behind; that module contains no executor at all:

    $ grep -n "def \|RunState\." packages/orchestration/job_runner.py
    46:def plan_job(job: Job) -> PlanJobResult:
    61:    job.state = RunState.RUNNING
    92:    job.state = RunState.PLANNED

Terminal transitions all funnel through `_apply_terminal`, which is NOT in
`job_runner.py` — that module really does contain no executor — but back in
`packages/orchestration/long_run_executor.py`. The command that places it:
`grep -rn "_apply_terminal" --include=*.py packages/ apps/` → its definition at
line 911 and its single call site at line 1578. Its docstring says it is "the
ONE place a final run report is written (F053 T002)". It sets
`job.metadata["cycle_terminal_status"]` and then calls `write_final_report(job)`.

One existing test that drives a job end to end through it:
`tests/orchestration/test_long_run_executor.py::TestTerminalStatusMatrix::test_all_green`
— it builds a PLANNED job via `make_job` (line 80, `state=RunState.PLANNED` at
line 88), passes a `FakeProvider()` (line 92) and `task_step=completing_step`
(line 121), and asserts `result.terminal_status == TERMINAL_ALL_GREEN` and
`provider.calls == 2`.

**The fulfillment spine is the second path.** `run_job_fulfill` in
`packages/orchestration/job_fulfillment.py` (`grep -n "def run_job_fulfill"` →
line 608) runs "plan -> work -> review -> repair -> approval -> apply -> test
-> proof -> final review -> completed_verified" with "No real provider. No
network." Its end-to-end test is
`tests/orchestration/test_job_fulfillment.py::TestJobFulfillFixturePass::test_fixture_pass_completes`
(line 348), which asserts `record.status.value == "completed_verified"`.

CAUTION for R13, measured not assumed: this path does not consume the job's
existing plan. It plans its OWN tasks — `task_descriptors = fixture_plan_tasks(job_id)`
(`fixture_plan_tasks` at line 299) — appends them to `job.tasks`, and sets
`job.state = RunState.RUNNING` without ever reading the incoming state. A loop
job handed to it would have its loop-derived plan ignored.

**The third path needs a real provider** and is therefore out of scope:
`_cmd_run_next_task_local` in `apps/cli/commands/job.py` (line 402) imports
`from packages.providers.ollama_builder.provider import OllamaBuilder`.

## Q2 — what the fake provider is, and how a test selects it

There is no module named "fake provider". Selection is by ARGUMENT in every
case; no environment variable picks a provider. The command that shows it:

    $ grep -rn "os.environ\|getenv" packages/orchestration/task_execution.py
    (no output)

Three real mechanisms:

1. **`FixtureTaskExecutor`**, `packages/orchestration/task_execution.py`
   (line 67), "Deterministic executor for testing. Does not call any LLM or
   external service." It is chosen by a STRING FIELD on the request —
   `TaskExecutionRequest.provider` defaults to `"fixture"` (line 35) — which
   `get_executor` (line 131) looks up in `_EXECUTORS` (line 123):
   `{"fixture": FixtureTaskExecutor, "none": NoneExecutor}`. `execute_task`
   (line 140) is its only production caller —
   `grep -rn "get_executor" --include=*.py packages/ apps/ tests/` returns the
   definition, `task_execution.py:142`, and four call sites in
   `tests/orchestration/test_task_execution.py`, nothing else.

2. **A callable passed to `run_cycles`** — the mechanism the cycle loop
   actually uses. The type is `ProviderCall = Callable[[TaskExecutionContext],
   BuilderOutput]` (`packages/orchestration/long_run_executor.py`, line 231),
   and `provider_call` is the THIRD POSITIONAL argument of `run_cycles`. Tests
   pass their own object: `class FakeProvider` in
   `tests/orchestration/test_long_run_executor.py` (line 92), "A builder that
   always returns verifiable output and counts its calls". The `task_step`
   keyword is a second seam, and `run_cycles`'s docstring calls these "Seams
   (all default to the existing production path)".

3. **`run_job_fulfill`'s hardcoded mode** — not a provider at all. Line 636 is
   `record = JobFulfillmentRecord(job_id=job_id, mode="fixture_demo")`. The CLI
   refuses the path without the flag: `apps/cli/commands/job.py:1931` prints
   `'message': 'v0 fulfillment requires --fixture-demo flag'`.

Isolation, separately from provider choice, is by environment variable:
`monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))` is what the fulfillment
tests use (e.g. `test_fixture_pass_completes`), and `run_loop` additionally
takes an explicit `root`.

## Q3 — where `job.metadata` reaches EVIDENCE

The job's evidence area is `job_evidence_dir` in
`packages/orchestration/pingpong_job.py` (line 2788): "The job's own (hidden)
evidence directory", returning `jobs_dir() / job_id / "evidence"`. Both the
report and the cycle records are built on it — `report_path` and
`cycle_evidence_dir` (`packages/orchestration/long_run_executor.py`, line 601)
each import it.

The candidate set was produced mechanically, not from memory:
`grep -rln "job\.metadata" --include=*.py packages/ apps/ | wc -l` prints 48;
of those modules, the ones that also write into an evidence directory were read.
Of those, ONE writer takes a core `Job` and puts `job.metadata` content into
that area: `write_escalation_assumptions_md(job, evidence_dir)` in
`packages/orchestration/escalation.py` (line 371), "Write the mid-run
assumption log into the job's evidence area". It reads through `_metadata(job)`
(line 102) under `JOB_METADATA_ESCALATIONS_KEY = "escalations"` (line 57) and
writes `ESCALATION_ASSUMPTIONS_FILENAME = "escalation_assumptions.md"`
(line 75) into the directory it is given.

That writer is key-specific: it carries the `escalations` list and nothing
else. No writer among the ones read copies the metadata dict wholesale into
evidence, and the probe in Q5 confirms the outcome empirically — a finished
loop job's evidence directory held exactly one file. The bundle
exporter `export_job_evidence` in `packages/orchestration/job_evidence.py`
operates on a different object — its `_build_job_manifest` reads `job.job_id`,
`job.job_title`, `job.tasks[].task_id`, i.e. the persisted plan record, not
`packages.core.models.Job` — and never touches `job.metadata`:

    $ grep -n "job\.metadata" packages/orchestration/job_evidence.py
    (no output)

The only place the WHOLE metadata dict is serialized is the JOB STORE, not the
evidence area: `save_job` in `packages/orchestration/storage.py` writes
`job.model_dump_json(indent=2)` to `<root>/jobs/<job_id>.json`.

## Q4 — where `job.metadata` reaches the REPORT

`collect_report_sources(job)` in `packages/orchestration/run_report.py`
(`grep -n "def collect_report_sources"` → line 718) is the function that would
carry it. It is the only place in that module that reads metadata for content:

    $ grep -n "metadata" packages/orchestration/run_report.py
    738:    metadata = getattr(job, "metadata", None) or {}
    746:        terminal_status=str(metadata.get("cycle_terminal_status", "") or ""),
    747:        stop_reason=str(metadata.get("cycle_stop_reason", "") or ""),
    892:        metadata = getattr(job, "metadata", None)
    893:        if isinstance(metadata, dict):
    894:            metadata[REPORT_ERROR_METADATA_KEY] = f"{type(exc).__name__}: {exc}"
    896:    metadata = getattr(job, "metadata", None)
    897:    if isinstance(metadata, dict):
    898:        metadata.pop(REPORT_ERROR_METADATA_KEY, None)

Lines 892-898 are `write_final_report`'s own error bookkeeping, not report
content. So exactly TWO metadata keys reach the report today, both by explicit
name: `cycle_terminal_status` and `cycle_stop_reason`. The value lands in a
field of the frozen `ReportSources` (line 268) and is rendered by
`_header_lines` (line 394) as `- Terminal status: …`.

## Q5 — does anything carry `loop_ref` into evidence or the report?

No. Nothing does.

    $ grep -rn "loop_ref\|LOOP_REF_METADATA_KEY" --include=*.py . | grep -v node_modules

returns hits in exactly five files: `packages/orchestration/loop_run.py` (where
`LOOP_REF_METADATA_KEY = "loop_ref"` is defined at line 51),
`packages/orchestration/loop_spec.py` (one docstring line),
`apps/cli/commands/loop_cmd.py` (one comment line), and the two F045 test files
`tests/orchestration/test_loop_run.py` and `tests/cli/test_loop_cmd.py`. No
evidence writer and no report builder appears in that list. The targeted
negative:

    $ grep -rn "loop_ref" packages/orchestration/run_report.py \
        packages/orchestration/job_evidence.py \
        packages/orchestration/long_run_executor.py \
        packages/orchestration/escalation.py packages/orchestration/run_manifest.py
    (no output)

Measured end to end, not only grepped. A read-only probe under a gitignored
scratch data root materialized a loop, drove the job to `all_green` through
`_apply_terminal`, and read what was written:

    job.state          = RunState.PLANNED
    job.metadata keys  = ['loop_ref', 'loop_unattended', 'project_id']
    job.metadata[loop_ref] = nightly-tidy
    report path exists = True .../data/jobs/3a3b5a83-…/evidence/report.md
    'loop_ref' in report.md      = False
    'nightly-tidy' in report.md  = False
    evidence files            = ['report.md']
    evidence files mentioning loop = []

The report's header block, verbatim from that run:

    # Run report — tidy probe on 2026-08-14

    - Job: `3a3b5a83-56c5-4628-a591-fd6518fc9ada`
    - Project: probe
    - Mission: not recorded
    - State: completed
    - Terminal status: all_green
    - Duration: not recorded

So the provenance is on the job and reaches disk in the job store, and the
evidence area of a finished loop job contains one file, `report.md`, which does
not mention the loop. The probe wrote only under `.remedy-wt/` and was removed
before handback.

## Q6 — the smallest change that would make `loop_ref` visible

Described only; no code was written and no production file was changed.

ONE file, `packages/orchestration/run_report.py`, and it covers BOTH halves of
the acceptance line at once — because `report_path` puts `report.md` INSIDE
`job_evidence_dir`, which the probe above confirms on disk. Three edits, in the
exact shape `cycle_terminal_status` already has:

1. Add one field to `ReportSources` (line 268), e.g. `loop_ref: str = ""`,
   defaulting to empty so an absent value renders like every other absent
   value and no existing golden changes.
2. In `collect_report_sources` (line 718), read it beside the two keys already
   read at lines 746-747 — the key name should be imported from
   `loop_run.LOOP_REF_METADATA_KEY` rather than retyped, so the writer and the
   reader cannot drift. Note the import direction: `run_report` does not import
   `loop_run` today, so this adds a dependency; a local import inside the
   function matches the module's existing style.
3. In `_header_lines` (line 394), emit one conditional line next to
   `- Stop reason:` — that line is already conditional on its value being
   non-empty, which is why a loop-less job's report would be expected to stay
   byte-identical. R13 must prove that with a test, not assume it.

Not determined, and R13 must decide it rather than assume: whether a SECOND,
evidence-only artifact is wanted in addition to the report line. The report
already lives in the evidence area, so the minimal change needs none; if the
reviewer wants `loop_ref` in a machine-readable record too, the nearest
existing carrier is the cycle record written by `write_cycle_record`
(`long_run_executor`, line 613), which today serializes a `CycleRecord` and
carries no job metadata.

Also not determined: which pipeline R13's fixture test should drive. `run_cycles`
is the one that produces the report the change above touches; `run_job_fulfill`
would discard the loop's plan (see Q1). Sizing that choice is R13's first job.
