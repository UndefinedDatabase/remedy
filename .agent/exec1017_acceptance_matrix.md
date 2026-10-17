# exec-1017 Phase 7 — acceptance matrix (deterministic; no model, no network)

Every row runs with the counting fake planner, the fake builder and reviewer, or the fake `pi`
inside the real tool sandbox. Scale matrix = `tests/orchestration/scale_matrix.py` version 2, run by
`tests/cli/test_do_scale_matrix.py`.

| Case | Where | What it proves |
|---|---|---|
| Tiny README edit | scale matrix `tiny-readme`, `incident-readme-german-payload`; `tests/regression/test_readme_order_20261017.py` | bounded lane, 1 job, 1 task, 0 planner calls; the 2026-10-17 order verbatim from an order folder |
| Bugfix with regression test | scale matrix `small-bug-and-regression-test` | one task carries the requested test |
| Medium endpoint task | scale matrix `medium-api-endpoint` | full lane, no check-only job, ≤ 7 planner calls |
| Multi-file task | scale matrix `monorepo-schema-change` | full lane, planned milestones |
| Large-repository small edit | scale matrix `large-readme-edit` (10,000 files) | the same cost as the tiny edit |
| Ambiguous target | scale matrix `ambiguous-vague-target`, `ambiguous-bare-readme` | approval kept / hold, never a guess |
| Explicitly required test command | scale matrix `incident-readme-german-payload` (passed), `required-test-command-fails` (job blocked, run step failed); regression module | the project's command runs blocking; a red run never completes |
| Missing test command | scale matrix `required-test-command-missing`; `test_order_verification.py` | `not_run` with the reason, never `passed` |
| No test requested | scale matrix `no-test-requested` | `not_required`, said so |
| Failed reviewer | scale matrix `failed-reviewer`; `test_review_reports.py` failed walk | run step failed, report `failed` |
| Pi token-limit exhaustion | `tests/orchestration/test_pi_loop_limits.py` | turn cap and input cap end the sandboxed loop early, work and usage kept, `budget_exhausted`, no retry; job tokens left lower the cap |
| Cancellation | `test_review_reports.py` (SIGTERM, Ctrl-C), `test_exec_guard.py` observer cancel | report `cancelled`; a live stream can end a child |
| Automatic report capture | `test_review_reports.py`, `test_stage_review_reports.py` | report without a job id; ZIP has the 10 newest, not the 11th, failed included, no secret, repeatable bytes |
| Repeated or resumed execution | `tests/cli/test_do_order_file.py` (order_already_running, abandoned mission waits), `tests/cli/test_decision_cmd.py` (extend then resume) | existing behaviour, unchanged by this branch |
| HTTP path | `tests/ui_server/test_public_api.py`, `test_execution_options.py` | `capture_review` reaches `remedy do`; `claude-cli` and unavailable providers refused before start |

Not run, by design: a real Pi/Ollama benchmark. Proposed for the operator's approval: run the
incident order once through the API against remedy-lab with `capture_review: true` and compare
the report with the baseline (28 builder turns, 223,221 input tokens, 6 min 41 s).
