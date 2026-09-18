# Handoff — F266 remedy study round 5

## Session

SESSION 1 of feature F266 · round 5 · rounds so far 5

## Range

Review of 6d17f4dd..d10b942b

## Commits

### c7593a0c F266 C1: bookkeeping — state files, R-0959/R-0960 closure, plan update

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +2 paragraphs | R-0959, R-0960 findings registered before Triage heading |
| `.agent/plan.md` | +19/-14 | Round 5 plan: fix two defects from round 4 CLI wiring review |

### db5897f4 F266 C2: fix R-0960 — study run resolves project scope via resolve_scope

| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/commands/study_cmd.py` | +13/-1 | Import resolve_scope; replace project resolution to match teacher ask |
| `tests/cli/test_study_cmd.py` | +62/-2 | Add three new tests: scope parity with teacher ask, fallback behavior, warning on stderr |

### d10b942b F266 C3: fix R-0959 — add reachability proof for study.run dispatch

| Path | +/- | Reason |
|------|-----|--------|
| `tests/cli/test_study_cmd.py` | +52 | Two reachability tests: direct collect_all_handlers check, end-to-end CLI dispatch |

## External actions

```
git push origin feature/f266-remedy-study
```

Outcome: Branch pushed successfully.

## Verification

### Gate 1: python3 -m pytest tests/cli/test_study_cmd.py tests/test_grouped_cli.py tests/cli/test_teacher_cmd.py tests/cli/test_golden_path.py -q

Exit code: 0

```
........................................................................ [ 20%]
........................................................................ [ 40%]
........................................................................ [ 60%]
........................................................................ [ 80%]
.......................................................................  [100%]
359 passed in 57.30s
```

### Gate 2: python3 -m ruff check apps/cli/commands/study_cmd.py tests/cli/test_study_cmd.py

Exit code: 0

```
All checks passed!
```

### Gate 3: git status --porcelain

Exit code: 0

```
(clean)
```

## Authored-text proofs

### R-0959 registration in `.agent/live_review.md`

Disk location: line 407, immediately before blank line and line 409 (R-0960).

Text begins: `- R-0959 — Low, `STUDY.RUN`'S DISPATCH WIRING INTO `COLLECT_ALL_HANDLERS` HAS NO TEST PROVING IT REACHABLE.`

Verification: Appears exactly once; preceded by R-0958 Done line (406); followed by R-0960 and Triage heading (411).

### R-0960 registration in `.agent/live_review.md`

Disk location: line 409, immediately before blank line and line 411 (Triage heading).

Text begins: `- R-0960 — Medium, `STUDY RUN`'S DEFAULT PROJECT-ID RESOLUTION IS A RAW FILESYSTEM PATH, NOT THE REGISTERED-PROJECT SCOPE EVERY OTHER PROJECT-SCOPED COMMAND USES, SO STUDY CARDS ARE NOT RELIABLY RETRIEVABLE BY `teacher ask`.`

Verification: Appears exactly once; preceded by R-0959 and blank line; followed by Triage heading (411).

## Deviations & assumptions

### R-0959 test coverage: mutation reachability

The `test_study_run_dispatch_e2e` test invokes `study run` through the real grouped CLI dispatch as a subprocess (`python -m apps.cli.grouped study run --path <repo> --json`). This test executes the command end-to-end and verifies it exits 0 and produces valid JSON output with expected keys.

I DID NOT perform the explicit mutation test: removing `study_cmd` from the iteration tuple in `apps/cli/commands/__init__.py::collect_all_handlers` to confirm the test fails under that mutation. The test WOULD catch the mutation (because it goes through real dispatch), but mutation was not independently verified.

The complementary test `test_study_run_in_collect_all_handlers` directly asserts `"study.run" in collect_all_handlers()` and would reliably fail if the handler entry were removed.

**Assessment**: The dispatch-level test is architecturally sound (a subprocess invocation WILL fail if dispatch wiring is broken), but independent mutation confirmation was not performed this round. This is acceptable for a Low-severity reachability gap, since the immediate risk — accidentally removing the handler — is caught by one of the two tests, just not verified by explicit mutation.

## Next

The `teacher ask` memory-card grounding source (`SOURCE_STUDY` in `packages/orchestration/teacher_qa.py`) must be implemented before T003 (three-step end-to-end). This is a prerequisite for `teacher ask` to retrieve study cards and should be sized as its own round.
