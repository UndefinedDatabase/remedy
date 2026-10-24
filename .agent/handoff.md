# Handoff — F157 round 6

## Session

SESSION 2 of feature F157 · round 6 · rounds so far 6. This round booked round 5's verdict and
R-1453's resolution, registered R-1454, and landed the reduced-capability end-to-end DECISION
F157 D3 (6) orders: a one-task job run through the real `job.run` command handler with a reduced
claude-cli adapter (`json_schema=False`) names its one predicted degradation in its evidence file,
its job report and its run report, text and JSON, beside a control run with the registry's adapter
that names none — every ordered commit landed and every gate passed, with no discrepancy.

Fortschritt: ~85 % (T001, T002 and T003 landed · R-1454 and the closure open) — Schätzung.

## Range

Review of `a45458127`..`be1366f76`.

## Commits

### d847a22ca F157 R6 C1: book round 5, R-1453 resolved and R-1454, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f157-r6.md` | +115/-0 | NEW FILE — this round's block, the authored-text proof |
| `.agent/live_review.md` | +7/-0 | books round 5's Gate verdict PASS, R-1453 RESOLVED, and registers R-1454 |
| `.agent/plan.md` | +7/-7 | rewritten: Current Step → round 6's end-to-end, Next Steps → the closure sequence |
| `.agent/prose_slips.md` | +1/-0 | one line on round 5's gate-5 prose/measured-length discrepancy |

### be1366f76 F157 R6 C2: a job run with a reduced adapter names its degradation in its evidence and both reports
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_capability_degradation_e2e.py` | +193/-0 | NEW FILE — a reduced `ClaudeCliReferenceAdapter` subclass (`json_schema=False` via `dataclasses.replace`) installed for `"claude-cli"`; a fake `_guarded_cli_run` answering `--version`, the builder, the reviewer's native call and its schema-in-prompt call; a one-task job run through `COMMAND_HANDLERS["job.run"]` twice (reduced, then the registry's adapter) asserting `task_capability_degradations`, `capability_decisions.jsonl`'s one line, the recorded reviewer argv, `format_job_report_text`'s line and `_cmd_run_show`'s text and JSON line, both ways |

## External actions

`git push origin feature/f157-capability-matrix` — run once immediately after this commit; no PR
opened, per the block's constraint.

## Verification

1. `git -C <repo> status --porcelain` → empty.
   `python3 .remedy-wt/f157-r6/prep/verify.py .` → every line `True`; last line `ALL True`; the
   `C3` row read `absent` at the time this gate ran, before this commit existed.

2. `python3 .remedy-wt/f157-r6/prep/run_selection.py . .remedy-wt/f157-r6-worker/selection-output.txt`
   → `exit 0`; last pytest line `6191 passed, 2 skipped in 57.28s`; no `FAILED`, no `ERROR`, no
   `process(es) behind` line anywhere in the output. The two `SKIPPED` lines: the pre-existing
   `test_install_smoke.py` (opt-in, needs network) and `test_agent_tooling.py` (a standing D12
   quarantine). Run once, as the block's rule states.

3. `python3 -m ruff check tests/orchestration/test_capability_degradation_e2e.py`
   → `All checks passed!`, exit 0.

4. `python3 -m apps.cli.main integrity check --json` → `"fail_count": 0`, `"ok": true`, 6 of 6
   checks `pass`.

5. `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`
   → `9`.

## Authored-text proofs

`.agent/authored/f157-r6.md`, applied at C1, compared disk-to-disk against the committed prepared
file `c1-.agent__authored__f157-r6.md` (itself byte-equal to `block.md`): byte-equal, 115 lines,
sha256 `905abfdda2fbc5e194888f3cb2c484424d32481552d760400b12fe402d85c8a8` on both sides, and equal
to `block.md`'s own sha256. The other three C1 targets (`.agent/live_review.md` 160,476 bytes,
`.agent/prose_slips.md` 425,791 bytes, `.agent/plan.md` 1,215 bytes) were each compared
disk-to-disk against their own prepared `c1-*` file before the commit and read byte-equal;
`verify.py`'s gate 1 re-confirms all four after the commit.

## Deviations & assumptions

None. Every ordered commit, constraint and gate in the block matched what landed on disk; no
production file changed this round.

For the operator: this round's test run covered a selection chosen for it, not the entire test
collection the repository holds; every test in that selection passed on its one run.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | this commit |
| Gate 1 | done | |
| Gate 2 | done | |
| Gate 3 | done | |
| Gate 4 | done | |
| Gate 5 | done | |
| Push | done | `git push origin feature/f157-capability-matrix` immediately after this commit |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work.
2. Phase 1 rule 2: run the Open PR Gate before starting anything unrelated.
3. Review round 6 and book its verdict in the next round's first commit.
4. Decide R-1454 by DECISION and repair it.
5. The closure sequence of `docs/roadmap/STATUS_closure_protocol.md`.
6. Operator questions open: 2.
7. Open findings count (gate 5): 9.
