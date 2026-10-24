# Handoff — F157 round 5

## Session

SESSION 2 of feature F157 · round 5 · rounds so far 5. This round booked round 4's verdict and
R-1453's repair, landed DECISION F157 D5, added `format_capability_degradations` and widened
`read_capability_degradations` to many directories, moved the job report's per-task lines into
their own module as a structural step, and wired a run's and a job task's capability degradations
back into `remedy run show`'s text and JSON and into the job report's per-task line — every
ordered commit landed and every gate passed, with one discrepancy between the block's own gate-5
prose and the measured code declared below rather than resolved silently.

Fortschritt: ~75 % (T001 and T002 landed · T003: three routes, the evidence and its two report
surfaces landed, the end-to-end open) — Schätzung.

## Range

Review of `ee99fc1bf`..`befb4c129`.

## Commits

### abca6cd48 F157 R5 C1: book round 4, R-1452 resolved and R-1453, DECISION F157 D5, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f157-r5.md` | +163/-0 | NEW FILE — this round's block, the authored-text proof |
| `.agent/decisions.md` | +10/-0 | append DECISION F157 D5 |
| `.agent/live_review.md` | +7/-0 | book round 4's Gate verdict PASS and register R-1453 |
| `.agent/plan.md` | +8/-7 | rewritten: Current Step → round 5, Next Steps → the end-to-end and the closure sequence |

### 2b34acbfb F157 R5 C2: one wording for a degradation, the reader over many directories, and the reviewer call held by a test
| Path | +/- | Reason |
|---|---|---|
| `packages/contracts/capability_matrix.py` | +13/-0 | adds `format_capability_degradations` (DECISION F157 D5 (1)) |
| `packages/orchestration/capability_routes.py` | +20/-17 | `read_capability_degradations` now takes `*evidence_dirs`, loops over each, skips a falsy or absent one, runs `capability_degradation_entries` once over all of them |
| `apps/cli/commands/worker.py` | +3/-8 | `_cmd_worker_show`'s `Degradations:` text now built from `capability_degradation_entries(decisions)` through `format_capability_degradations`; the printed line is unchanged, `tests/cli/test_worker.py` untouched |
| `tests/contracts/test_capability_matrix.py` | +31/-0 | tests for `format_capability_degradations`: an empty list, a degraded entry, an unavailable entry, two entries joined |
| `tests/orchestration/test_capability_routes.py` | +75/-1 | tests for the many-directory reader (two directories, one distinct line and a repeat each); R-1453's test proving `_review_impl` reaches the branch `routed_reviewer_schema` names, by WHICH stub ran rather than by a stub that raises to signal a wrong branch |

### 933d8a76d F157 R5 C3: the job report's per-task detail lines move to their own module
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/job_report_task_lines.py` | +27/-0 | NEW FILE — `task_report_detail_lines(job, task, steering_map)`, the steering-note lines moved unchanged out of `format_job_report_text` (DECISION F157 D5 (4)) |
| `packages/orchestration/job_report.py` | +2/-4 | the four-line steering loop replaced by one call, `lines.extend(task_report_detail_lines(job, t, steering_map))`; imports the new module |
| `docs/system/structure-ledger-v1.md` | +1/-1 | `format_job_report_text`'s row lowered 120 → 117, its measured length after the move |
| `tests/test_structure_ratchet.py` | +1/-1 | `MAX_FUNCTION_LINES` lowered by 3, matching the row |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | `packages.orchestration.job_report_task_lines` added in sorted position |

### befb4c129 F157 R5 C4: a run's and a task's degradations read back and shown
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/capability_evidence.py` | +58/-0 | NEW FILE — `task_capability_degradations(job_id, task_id, run_id)`, `run_capability_degradations(run_id, record)` (the plan lookup via `load_job_plan_safe`, imported inside the function), `capability_report_line(record)` (DECISION F157 D5 (2)/(3)) |
| `packages/orchestration/job_report_task_lines.py` | +7/-1 | appends `      Degradations: <wording>` under a task whose own evidence names one |
| `apps/cli/commands/run_report_cmd.py` | +5/-1 | `_cmd_run_show` always sets `data[CAPABILITY_DEGRADATIONS_FIELD]` from `run_capability_degradations`; `_print_text_report`'s report-lines tuple gains `capability_report_line(data)` as its last member |
| `tests/cli/test_run_report_cmd.py` | +77/-0 | tests for `remedy run show` printing the line for a degraded run directory and none for a native one, and the JSON list both ways |
| `tests/orchestration/test_capability_evidence.py` | +150/-0 | NEW FILE — both readers over a line in each directory, over both together and over none; the plan lookup reaching the task's directory and a plan that cannot be read; the report line `None` and its text; the job report printing a task's line and printing none for a job without one |
| `docs/system/worker-adapter-contract-v2.md` | +8/-0 | one paragraph appended on the two readers and the two places a run's degradations are shown |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | `packages.orchestration.capability_evidence` added in sorted position |

## External actions

`git push origin feature/f157-capability-matrix` — run once immediately after this commit; no PR
opened, per the block's constraint.

## Verification

1. `git -C <repo> status --porcelain` → empty.
   `python3 .remedy-wt/f157-r5/prep/verify.py .` → every line `True`; last line `ALL True`; the
   `C5` row read `absent` at the time this gate ran, before this commit existed.

2. `python3 .remedy-wt/f157-r5/prep/run_selection.py . .remedy-wt/f157-r5-worker/selection-output.txt`
   → `exit 0`; last pytest line `6189 passed, 2 skipped in 53.31s`; no `FAILED`, no `ERROR`, no
   `process(es) behind` line anywhere in the output. The two `SKIPPED` lines: the pre-existing
   `test_install_smoke.py` (opt-in, needs network) and `test_agent_tooling.py` (a standing D12
   quarantine). Run once, as the block's rule states.

3. `python3 -m ruff check packages/contracts/capability_matrix.py packages/orchestration/capability_routes.py packages/orchestration/capability_evidence.py packages/orchestration/job_report_task_lines.py packages/orchestration/job_report.py apps/cli/commands/run_report_cmd.py apps/cli/commands/worker.py tests/orchestration/test_capability_routes.py tests/orchestration/test_capability_evidence.py tests/cli/test_run_report_cmd.py tests/contracts/test_capability_matrix.py`
   → `All checks passed!`, exit 0.

4. `python3 -m mypy packages/contracts/capability_matrix.py packages/orchestration/capability_routes.py packages/orchestration/capability_evidence.py packages/orchestration/job_report_task_lines.py`
   → `Success: no issues found in 4 source files`, exit 0.

5. `python3 -m apps.cli.main integrity check --json` → `"fail_count": 0`, `"ok": true`, 6 of 6
   checks `pass`.
   An `ast`-based script under `.remedy-wt/f157-r5-worker/` printed, as `end_lineno - lineno + 1`:
   `format_job_report_text` → `117`; `create_role_provider` → `98`, matching the gate's own `(98)`;
   `_print_text_report` → `99`, NOT the gate's stated `(100)` — see Deviations below.

6. `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`
   → `9`.

## Authored-text proofs

`.agent/authored/f157-r5.md`, applied at C1, compared disk-to-disk against the committed prepared
file `c1-.agent__authored__f157-r5.md` (itself byte-equal to `block.md`): byte-equal, 163 lines,
sha256 `442fcf662bd2d7bda098585491cccecb62813919fca7e28c388f41cd3925fc66` on both sides, and equal to
`block.md`'s own sha256. The other three C1 targets (`.agent/decisions.md` 4,095,838 bytes,
`.agent/live_review.md` 156,629 bytes, `.agent/plan.md` 1,258 bytes) were each compared disk-to-disk
against their own prepared `c1-*` file before the commit and read byte-equal; `verify.py`'s gate 1
re-confirms all four after the commit.

## Deviations & assumptions

Gate 5's prose states `_print_text_report`'s measured length as `(100)`. Measured by the same
`ast`-based script this round and independently by reading the git blob at the base commit
`ee99fc1bf`, the function is 99 lines there and 99 lines after this round's edit — the edit is a
single in-place line replacement inside its existing report-lines tuple, adding no line and
removing none, exactly as C4's own instruction orders ("`_print_text_report`'s length unchanged").
The 99-line measurement at the unmodified base commit is reproducible with no edit of this round's
in it, so the discrepancy is in the gate's stated expectation, not in this round's work; nothing
was padded to manufacture a 100th line. This is declared rather than silently resolved, per the
standing rule that two clauses of one block disagreeing is stated, not quietly picked one way.

For the operator: this round's own test run covered a selection chosen for it, not the full
collection the repository holds; that selection passed in full on its one run.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| R-1453 | done | repaired in C2 (`2b34acbfb`): a test builds the reviewer through `create_role_provider`, stubs both branches `_review_impl` can take, and proves which one ran under the reduced adapter and under the registry's |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit |
| Gate 1 | done | |
| Gate 2 | done | |
| Gate 3 | done | |
| Gate 4 | done | |
| Gate 5 | deviated | measured and reported; the gate's stated `_print_text_report` expectation of 100 does not match the measured 99 at the base commit or after this round's length-unchanged edit — see Deviations |
| Gate 6 | done | |
| Push | done | `git push origin feature/f157-capability-matrix` immediately after this commit |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work.
2. Phase 1 rule 2: run the Open PR Gate before starting anything unrelated.
3. Book round 5's verdict in the next round's first commit.
4. The reduced-capability end-to-end (DECISION F157 D3 (6)).
5. Operator questions open: 2.
6. Open findings count (gate 6): 9.
