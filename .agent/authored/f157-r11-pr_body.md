## What

F157 — Capability matrix & honest degradation. Features stop assuming what a model can do and ask
one register instead; a run says when it used a fallback.

- `packages/contracts/capability_matrix.py` (new): the register `CAPABILITY_REQUIREMENTS` with
  three entries (`reviewer_schema_gate`, `parked_session_resume`, `stream_evidence_capture`), the
  no-consumer notes for the other three capabilities, and the one decision call
  `require_or_degrade(feature_key, adapter, model)`, answering `native`, `degraded` or
  `unavailable`.
- `packages/orchestration/capability_routes.py` (new): one route per entry for the claude-cli pair a
  run built; `create_role_provider` takes the stream answer from it, `ClaudeCliProvider` its
  reviewer-schema choice and its resume answer. A build with any fallback writes its decisions as
  one line of `capability_decisions.jsonl` beside the run's evidence.
- `packages/orchestration/capability_evidence.py` (new) reads a run's or a job task's degradations
  back; `remedy run show` carries them in its JSON answer and prints a `Degradations:` line, the job
  report prints the same line under a task (through the new door
  `packages/orchestration/job_report_task_lines.py`), and `remedy worker show` prints the pair's
  answers.
- `tests/contracts/test_capability_matrix.py` (new): guards that fail a capability read outside the
  matrix, a decision call whose key is not a register literal, and an incomplete register, each
  with a violation fixture proved red.
- `docs/system/worker-adapter-contract-v2.md` gains the capability-matrix section.

## Why

The honest fallbacks (schema in the prompt, full-context resend, buffered output) were scattered
through features that decided by provider identity, a flag or configuration. A second vendor's
adapter needs one place that says what degrades how, and evidence of when it did.

## Key decisions

- DECISION F157 D2: the register lives beside the adapter contract it reads, and its run-record
  key is `capability_degradations`, never `degraded`, which already means something else.
- DECISION F157 D3: decisions are made where a run builds a provider, evidence is a file beside
  the run because both run-record writers are structure-ledger rows, the planner entry is retired
  until a planner calls through an adapter, and the badge is the command line's `Degradations:`
  line because Remedy ships no web page.
- DECISION F157 D6: a run's degradations name what its pair runs in fallback whenever that feature
  is used; for resume, that every call sends its full context.
- DECISION F157 D7: the closure's self-use record masks the fake secrets of the redaction tests it
  wrote, and the job branch keeps the diff whole.

## How to review and test

- `python3 -m pytest -q tests/contracts/test_capability_matrix.py tests/orchestration/test_capability_routes.py tests/orchestration/test_capability_evidence.py tests/orchestration/test_capability_degradation_e2e.py`
  — the end-to-end runs a one-task job with a reduced claude-cli adapter and finds exactly the
  predicted degradations in its evidence and both reports.
- The closure's one full suite on `b9597df6b`: `23870 passed, 11 skipped, 1 warning in 366.16s`,
  exit 0 (`.agent/authored/f157-closure-suite.txt`); CPU 1413.16 s, 1.8 % above F314's.
- Evidence job `f157r10e1001` on `ce081c649`: `12852 passed, 6 skipped`, exit 0; package
  `remedy-review-20261024-070450-READY_FOR_REVIEW.zip`, SHA-256
  `9486e587f096ea0811f1d4b65439c0b4ee1bbc648e623f4a037dd73adff72403`.
- The reviewer ran 53 mutations of the production code in rounds 2 to 6; every survivor a caller
  could observe became a finding and was repaired with a test it then turned red.

## Changed files

| Area | Files |
|---|---|
| Production | `packages/contracts/capability_matrix.py`, `packages/orchestration/capability_routes.py`, `packages/orchestration/capability_evidence.py`, `packages/orchestration/job_report_task_lines.py` (all new), `packages/orchestration/pingpong_provider.py`, `packages/orchestration/role_provider_factory.py`, `packages/orchestration/job_report.py`, `apps/cli/commands/run_report_cmd.py`, `apps/cli/commands/worker.py` |
| Tests | `tests/contracts/test_capability_matrix.py`, `tests/orchestration/test_capability_routes.py`, `tests/orchestration/test_capability_evidence.py`, `tests/orchestration/test_capability_degradation_e2e.py` (all new), `tests/cli/test_worker.py`, `tests/cli/test_run_report_cmd.py`, the allowlist, the structure ratchet |
| Docs | `docs/system/worker-adapter-contract-v2.md`, `docs/system/structure-ledger-v1.md`, the checklist's consolidation paragraph, the feature file, STATUS, README |
| Records | `.agent/` |

## Verdict

Latest live review: PASS for every round. F157's four findings (R-1451 to R-1454) are all
resolved inside the feature. Open findings: 8, all owned by F316.

## Runtime actuals

Three sessions, eleven delegated rounds. The self-use run made four priced provider calls, each
measured by the job's own ledger; the evidence job's pytest took 1829 s and the full suite 366 s.
Token counts of the planner and worker sessions are not measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
