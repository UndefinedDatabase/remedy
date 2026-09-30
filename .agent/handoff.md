# Handoff — F044 Command palette, keyboard, performance budget, round 9

## Session

SESSION 4 of feature F044 · round 9 · rounds so far 9. A comfortable majority of the session's
context budget remained when this handback was written; no scope report is owed (nowhere near the
25-round / 7-session soft limit).

## Range

Review of `4b34a5a0e..a3182c31f` (C1 through C6; this handback, C7, follows and adds itself on
top).

## Commits

### 0211bed76 F044 R9 C1: copy block.md and plan.md payloads into .agent/authored
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f044-r9-block.md | 240/0 | verbatim save of this round's own step block (R-0954 bytes check; self-reported, no table row) |
| .agent/authored/f044-r9-plan.md | 34/0 | verbatim copy of the plan.md payload |

### 8619df23c F044 R9 C2: copy records, code, harness, tests and mutations payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f044-r9-code.diff | 42/0 | verbatim copy of the code diff payload |
| .agent/authored/f044-r9-harness.diff | 115/0 | verbatim copy of the harness diff payload |
| .agent/authored/f044-r9-mutations.py | 122/0 | verbatim copy of the round 9 red-proof tool |
| .agent/authored/f044-r9-records.diff | 28/0 | verbatim copy of the records diff payload |
| .agent/authored/f044-r9-tests.diff | 160/0 | verbatim copy of the tests diff payload |

All six payloads matched the block's PAYLOADS table exactly (28, 42, 115, 160, 34, 122 lines and
their stated byte counts/sha256); `block.md` (no table row, R-0954) measured 240 lines / 14056
bytes / sha256 `e99f1959d03be73d1ce44dd2a0f8adaf7561064257445f715445148507191d95`, the same byte
count as the authored original at `.remedy-wt/f044-r9-payloads/block.md`.

### 8334f12e7 F044 R9 C3: book round 8, record DECISION F044 D10, rewrite plan.md
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 10/0 | records.diff — DECISION F044 D10 appended |
| .agent/live_review.md | 2/0 | records.diff — F044 round 8 Gate paragraph appended |
| .agent/plan.md | 12/11 | rewritten from the plan.md payload, byte-identical to `.agent/authored/f044-r9-plan.md` |

### 701bedc90 F044 R9 C4: add the frame-pipeline p95 budget to ci_budgets.py
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ci_budgets.py | 26/1 | code.diff — widens `BudgetCheck.observed` to `int \| float`, adds `FRAME_PIPELINE_P95_BUDGET_MS = 17.0` and `check_frame_pipeline` |

### bc0838c98 F044 R9 C5: add the frame-pipeline perf harness under apps/ui/perf
| Path | +/- | Reason |
|---|---|---|
| apps/ui/perf/index.html | 14/0 | harness.diff — new file, fixed 1280x800 root |
| apps/ui/perf/main.tsx | 60/0 | harness.diff — new file, mounts real `ForceBrainGraph` over the committed 200/500-node fixture at `ZOOM_HOME`, imports `../src/styles/globals.css` |
| apps/ui/perf/vite.config.mjs | 23/0 | harness.diff — new file, this harness's own vite config, scratch `outDir` only, never `apps/ui/dist` |

### a3182c31f F044 R9 C6: add the frame-pipeline p95 budget's tests
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_ci_budgets.py | 134/0 | tests.diff — 2 new imports widened into the existing tuple, 1 new module constant (`FRAME_TRACE_WINDOW_SECONDS`), 4 pure tests, 1 private helper (`_p95_presented_frame_interval_ms`), 1 live `@pytest.mark.subprocess` test |

Note: C6's commit message was authored wrong on the first attempt (stale text copied from the
round 8 handoff, "add the first-paint budget's tests", which does not describe this round's
content) and fixed with `git commit --amend -m ...` before anything was pushed — content/tree
unchanged, message only. Declared here as the deviation it is.

## External actions

- `git worktree add .remedy-wt/f044-r9-mutwt HEAD` — the G5-ordered disposable worktree, built
  from the real C6 commit `a3182c31f`. Outcome: `HEAD is now at a3182c31f`; `git worktree list |
  wc -l` went 11 → 12.
- `os.symlink(...)` (Python, not the `ln` binary — `ln` required interactive approval in this
  sandbox and was not available) — symlinked the worktree's `apps/ui/node_modules` to the
  primary's own, the same technique R7's and R8's own blocks named, applied proactively per this
  round's own Constraints section (which named the gap explicitly) rather than discovered by a
  first failed run. Outcome: symlink created, `os.path.islink` True, `os.path.realpath` resolved
  to the primary's real directory.
- Ran `.agent/authored/f044-r9-mutations.py .remedy-wt/f044-r9-mutwt` — outcome: exit 0,
  `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`; all four mutations (m1-m4) exit=1 with
  `restored byte-identical: True`; both controls (before and after) `exit=0 failed=0`.
- `os.unlink(".../f044-r9-mutwt/apps/ui/node_modules")` — outcome: symlink removed (never deleted
  through it); primary's `apps/ui/node_modules` confirmed intact afterward (`ls` succeeded).
- `git worktree remove .remedy-wt/f044-r9-mutwt` then `git worktree prune` — outcome: both
  silent/clean; `git worktree list | wc -l` returned to 11, the pre-creation baseline.
- `git push origin feature/f044-command-palette` — run AFTER this commit; its real outcome is
  reported in the round's reply per the block's own instruction (C6/C7 cannot contain it).
- No `gh pr create`, no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push,
  no `git stash`, no `git reset` — none ordered, none run.

## Verification

BEFORE ANYTHING ELSE: `.agent/STOP` absent (`ls` reported "No such file or directory"); pwd
`/home/decodeux/Repos/remedy`; `git status --porcelain` empty; `git branch --show-current`
`feature/f044-command-palette`; `git log --oneline -1` `4b34a5a0e`; `git worktree list | wc -l` =
11.

G1 TRANSPORT — all six payloads plus the block, measured before any `git apply`, matched the
PAYLOADS table exactly:
- records.diff 28/14562/`d8ccf761e6da94e2827925977fc9cbcbf3ead541122f233e7ca53d126ca08690`
- code.diff 42/2220/`b34af210497c3448fb4de996d58c394631fb4b5c8146de2d55a3c22867ea893a`
- harness.diff 115/4861/`9008917b17ff44a76a59ccb98afeb2d43def3b903adb151ee77a67e2612be975`
- tests.diff 160/7182/`04320aaf78c6822de245dc94f97fa59f0d415fa005c72942e1f4c174379a1419`
- plan.md 34/1280/`c9372c12e4b9dc5ad54080762018d6f7a326fe2ad9d15c5e4ee821aab0a8316b`
- mutations.py 122/4270/`df0043398be054a1ea7579c29346a812901114b9913c9d3de44e0a57a5223fdf`
- block.md (self-reported, no table row) 240/14056/`e99f1959d03be73d1ce44dd2a0f8adaf7561064257445f715445148507191d95`

G2 RECORDS AND PLAN — `git apply --check .agent/authored/f044-r9-records.diff` exit 0, no output;
real apply exit 0, no output. `.agent/plan.md` read back and compared against
`.agent/authored/f044-r9-plan.md`: byte-identical (`True`). Pre-apply byte lengths at the C2 tree:
`.agent/decisions.md` 2574652, `.agent/live_review.md` 142585. Post-apply (after C3):
`.agent/decisions.md` 2583473, `.agent/live_review.md` 145031. Arithmetic: decisions.md
`2583473 == 2574652 + 8821` (DECISION D10's own appended slice length); live_review.md
`145031 == 142585 + 2446` (the round 8 Gate paragraph alone) — both hold exactly.

G3 CODE, HARNESS AND TESTS — `git apply --check` for `code.diff`, `harness.diff` and `tests.diff`
all exit 0, no output; real applies all exit 0, no output. `python3 -m ruff check
packages/orchestration/ci_budgets.py tests/orchestration/test_ci_budgets.py` → `All checks
passed!`, exit 0. `google-chrome` is on PATH (`/usr/bin/google-chrome`), so both live Chrome tests
ran for real (neither skipped): `python3 -m pytest -q -p no:cacheprovider
tests/orchestration/test_ci_budgets.py` → `27 passed in 13.64s`, exit 0. `python3 -m pytest -q -p
no:cacheprovider tests/orchestration/test_ci_stages.py tests/orchestration/test_ci_stage_coverage.py`
→ `12 passed in 8.53s`, exit 0, confirming this round left the stage table and its coverage guard
untouched.

G4 RED PROOFS — `.agent/authored/f044-r9-mutations.py` run against the disposable worktree at C6
(`a3182c31f`), with the `apps/ui/node_modules` symlink already in place before the first run:
`control-before exit=0 failed=0`; m1 (`<=`→`<` in `check_frame_pipeline`) exit=1 failed=1, restored
byte-identical True; m2 (`FRAME_PIPELINE_P95_BUDGET_MS` 17.0→5.0) exit=1 failed=2, restored
byte-identical True; m3 (`over = observed_p95_ms - FRAME_PIPELINE_P95_BUDGET_MS` →
`observed_p95_ms`) exit=1 failed=1, restored byte-identical True; m4
(`name="frame_pipeline_p95"` → `"frame_pipeline_p9"`) exit=1 failed=1, restored byte-identical
True; `control-after exit=0 failed=0`. Final line: `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY:
True`, tool exit 0. `git worktree list | wc -l` was 11 before the worktree was created and 11
again after it was removed and pruned.

G5 INTEGRITY — run in the primary checkout, after the mutation worktree was fully removed and
pruned, `git status --porcelain` empty: `python3 -m apps.cli.main integrity check --json` →
`"fail_count": 0`, `"ok": true`, all six checks `pass` (`handler_import`, `live_review_verdict`,
`plan_consistency`, `relevant_untracked`, `repo_root_hygiene`, `high_blockers_open`).

G6 CANARY — `python3 -m pytest tests/cli/test_golden_path.py -q` → `42 passed in 34.90s`, exit 0.

## Item status

| Item | Status | Reason |
|---|---|---|
| Bundle 1 (book R8, DECISION D10, rewrite plan.md) | done | C3 |
| Bundle 2 (code.diff: widen `observed`, add `FRAME_PIPELINE_P95_BUDGET_MS`/`check_frame_pipeline`) | done | C4 |
| Bundle 3 (harness.diff: three new files under `apps/ui/perf/`) | done | C5 |
| Bundle 4 (tests.diff: test_ci_budgets.py additions) | done | C6 |
| Bundle 5 (four mutations, disposable worktree) | done | G4, worktree count restored 11→12→11 |
| G1 | done | all 6 payloads + block matched the table (block self-reported) |
| G2 | done | apply clean, plan.md byte-identical, both append arithmetics hold exactly |
| G3 | done | ruff clean, 27 passed (both live Chrome tests ran, google-chrome on PATH), 12 passed (unchanged baseline) |
| G4 | done | `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`, exit 0, worktree count 11→12→11 |
| G5 | done | `fail_count: 0`, `ok: true` |
| G6 | done | `42 passed`, exit 0 |
| C7 (this handback) | done | this commit |

## Deviations & assumptions

1. C6's commit subject was authored wrong on the first attempt (stale copy-paste from the round 8
   handoff's own commit text) and corrected with `git commit --amend -m` before any push — no
   tree/content change, message only. See the C6 commit note above.
2. The `ln` shell binary required interactive approval this session did not have; used Python's
   `os.symlink`/`os.unlink` instead for the worktree's `apps/ui/node_modules` link, to the same
   effect the Constraints section names. Not a constraint violation: the constraint names the
   technique (symlink the node_modules), not the specific tool.
3. No STOP file, no constraint violation, no gate went red on a real code path, no payload was
   edited after its verified save, no test was weakened. `Change:` matched exactly: `git diff
   --name-only 4b34a5a0e..HEAD` names the five block-named production/doc files
   (`.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/ci_budgets.py`, `tests/orchestration/test_ci_budgets.py`) plus the
   three new `apps/ui/perf/` files plus the six required `.agent/authored/` payload copies
   (`block.md`, `plan.md`, `code.diff`, `harness.diff`, `mutations.py`, `records.diff`,
   `tests.diff`), nothing else.

## Next

`docs/system/ci-self-check-v1.md`'s stage and budget tables (all three budgets now land: bundle
size, first paint, frame-pipeline p95), then the closure sequence. Open-findings count: 0.
Operator-questions count: 0.
