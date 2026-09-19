# Handoff — F273 Findings paydown v1 · Round 1

## Session

SESSION 1 of feature F273 · round 1 · rounds so far 1

Context self-assessment: the worker read the block, AGENTS.md, `docs/roadmap/features/T2_F273.md`, DECISION F273 D1, the handback template and the self-drive protocol's questions-file rule; every figure below comes from a command run in this round, and the worker's context held all of it without loss.

## Range

Review of 80f7c529..HEAD — branch `feature/f273-findings-paydown-v1`, cut from `main` at `80f7c529`.

## Summary

Round 1 claims F273 and builds three of T001's five.
- C1 claims F273 (STATUS `[~]`), re-heads the live review, books F271 round 6's verdict (PASS), lands DECISION F273 D1, and saves the eight payload copies.
- C2 builds R-0803: every test runs on an isolated data root, and a run that changed the configured root fails with an `R-0803:` line.
- C3 builds R-0804: a test walks every cockpit read endpoint for a two-task fake-provider job.
- C4 builds R-0810: the fake builder keeps one marker per task across repair rounds.
- C5 is this handoff.

Landed: R-0803 — `50eaf606` (resolution waits for the closure suite run, DECISION F273 D1 (1))
Landed: R-0804 — `fbf60c65`
Landed: R-0810 — `f0bfc4ba`

## Commits

### f892f77e F273 R1 C1: claim F273, book F271 round 6's verdict, land DECISION F273 D1 and save the round 1 payloads
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f273-r1-block.md` | +99 / -0 | Byte copy of the block |
| `.agent/authored/f273-r1-context.md` | +40 / -0 | Byte copy of context.md |
| `.agent/authored/f273-r1-decisions.md` | +44 / -0 | Byte copy of decisions.md |
| `.agent/authored/f273-r1-ledger.md` | +2 / -0 | Byte copy of ledger.md |
| `.agent/authored/f273-r1-live_review_head.md` | +22 / -0 | Byte copy of live_review_head.md |
| `.agent/authored/f273-r1-plan.md` | +29 / -0 | Byte copy of plan.md |
| `.agent/authored/f273-r1-status_from.txt` | +1 / -0 | Byte copy of status_from.txt |
| `.agent/authored/f273-r1-status_to.txt` | +1 / -0 | Byte copy of status_to.txt |
| `.agent/context.md` | +17 / -17 | := context.md |
| `.agent/decisions.md` | +44 / -0 | `80f7c529` bytes + decisions.md (DECISION F273 D1) |
| `.agent/live_review.md` | +21 / -19 | live_review_head.md + `80f7c529` bytes from `## Findings` + ledger.md (Gate F271 R6, VERDICT PASS) |
| `.agent/plan.md` | +19 / -13 | := plan.md |
| `docs/roadmap/STATUS.md` | +1 / -1 | F273 line `[ ]` -> `[~]` (status_from.txt -> status_to.txt) |

340 insertions, 50 deletions (`git show --numstat`).

### 50eaf606 F273 R1 C2: R-0803 — every test runs on an isolated data root, and a run that changed the configured root fails
| Path | +/- | Reason |
|------|-----|--------|
| `tests/conftest.py` | +83 / -0 | `_isolated_data_root`, `_data_root_fingerprint`, `pytest_configure`, `pytest_sessionfinish` — `git apply .remedy-wt/f273-proto-r0803.diff` |
| `tests/test_data_root_isolation.py` | +40 / -0 | Pins the per-test half — same diff |

123 insertions, 0 deletions.

### fbf60c65 F273 R1 C3: R-0804 — a test walks every cockpit read endpoint for a two-task fake-provider job
| Path | +/- | Reason |
|------|-----|--------|
| `tests/ui_server/test_handler_table_walk.py` | +126 / -0 | `git apply --include=tests/ui_server/test_handler_table_walk.py .remedy-wt/f273-proto-t001b.diff` |

126 insertions, 0 deletions.

### f0bfc4ba F273 R1 C4: R-0810 — the fake builder keeps one marker per task across repair rounds
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/pingpong_loop.py` | +3 / -0 | Marker guard in `_apply_fake_builder_changes` — `git apply --include=...` of the t001b diff |
| `tests/orchestration/test_pingpong_cli.py` | +15 / -0 | `test_a_repair_round_leaves_one_marker_per_task` — same diff |

18 insertions, 0 deletions.

### C5 (this commit) F273 R1 C5: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C1, with 340.

## External actions

- `git checkout -b feature/f273-findings-paydown-v1 80f7c529`; Open PR Gate re-read: `gh pr list --state open` printed `[]`.
- `git worktree add --detach .remedy-wt/f273-r1-mut f0bfc4ba` for G5, then `git worktree remove .remedy-wt/f273-r1-mut` (exit 0). `git worktree list` afterwards: the primary checkout on `feature/f273-findings-paydown-v1` and the reviewer's `.remedy-wt/f273-r1-dry` at `80f7c529`, nothing else.
- After C5: `git push -u origin feature/f273-findings-paydown-v1`. No pull request is opened.

## Verification

Exit codes were read through `.remedy-wt/f273-r1/run.py` or `.remedy-wt/f273-r1/runc.py` (the same, with an explicit cwd, printing `CWD`, the count of `R-0803:` lines in the whole output, the tail and `EXIT <returncode>`).

- **Transport**, before any write: `sha256sum` matched all eight payload digests (block.md `d1f22d8a4c759fe9818cc36db36429fad253ce882fdb8dafca5285f616ed5930`) and both diff digests.
- **G1** (at C4 `f0bfc4ba`): `python3 .remedy-wt/f273-r1/g1.py f0bfc4ba`, EXIT 0 — 23 lines each reading `True`: the 10 digests; `.agent/plan.md` and `.agent/context.md` equal their payloads; `.agent/live_review.md` equals head + the `80f7c529` bytes from `## Findings` + ledger.md; `.agent/decisions.md` equals its `80f7c529` bytes + decisions.md; STATUS equals its `80f7c529` bytes with the pair applied (FROM 1x before, 0x after, TO 1x after; `TO contains FROM: False`); the eight `.agent/authored/f273-r1-*` copies equal their payloads. Last line `ALL True`.
- **G2**: `git rev-parse f0bfc4ba:tests f0bfc4ba:packages`:
  ```
  d2b0f3a9544b4b9feee226c28db82bb60f2bc0da
  e8c063e321a50f8990c9da4f9c673e8a6c33ee1b
  ```
  `git diff --stat 80f7c529 f0bfc4ba -- tests packages`: `packages/orchestration/pingpong_loop.py | 3`, `tests/conftest.py | 83`, `tests/orchestration/test_pingpong_cli.py | 15`, `tests/test_data_root_isolation.py | 40`, `tests/ui_server/test_handler_table_walk.py | 126`, `5 files changed, 267 insertions(+)` — exactly the paths C2 to C4 name.
- **G3** (primary checkout, serial): `python3 -m pytest -q -p no:cacheprovider tests/test_data_root_isolation.py tests/ui_server/test_handler_table_walk.py tests/orchestration/test_pingpong_cli.py tests/test_data_paths.py tests/test_grouped_cli.py tests/orchestration/test_manual_completion_bundle.py tests/ui_server/test_cockpit_contract.py tests/cli/test_golden_path.py tests/docs/ tests/orchestration/test_roadmap_index.py`:
  ```
  CWD /home/decodeux/Repos/remedy
  R-0803 lines 0
  961 passed in 169.94s (0:02:49)
  EXIT 0
  ```
- **G4** (primary checkout): `python3 -m ruff check tests/conftest.py tests/test_data_root_isolation.py tests/ui_server/test_handler_table_walk.py tests/orchestration/test_pingpong_cli.py packages/orchestration/pingpong_loop.py` -> `All checks passed!`, EXIT 0.
- **G5** (`python3 .remedy-wt/f273-r1/g5.py .remedy-wt/f273-r1-mut`, one worktree at `f0bfc4ba`, `python3 -B -m pytest -q -p no:cacheprovider` from its root, `__pycache__` purged before every run, each mutation reverted by its saved bytes and confirmed `reverted True`), EXIT 0:
  ```
  import paths: .remedy-wt/f273-r1-mut/tests/conftest.py, .../packages/orchestration/pingpong_loop.py, .../packages/orchestration/project_brain.py (all inside the worktree)
  UNMUTATED control (the four test files): 461 passed in 21.86s — EXIT 0
  (a) tests/conftest.py FROM count 1
      tests/test_data_root_isolation.py: 3 failed in 0.22s — EXIT 1
        FAILED test_the_resolved_root_is_under_the_pytest_temp_base
        FAILED test_each_test_gets_a_fresh_empty_root
        FAILED test_a_cli_subprocess_inherits_the_isolated_root
      tests/test_grouped_cli.py alone: 281 passed in 17.54s — EXIT 1, printing
        R-0803: the test run changed the configured data root .../f273-r1-mut/.data (8 entries), first: ['job_logs', ...]
  (b) packages/orchestration/pingpong_loop.py FROM count 1
      tests/orchestration/test_pingpong_cli.py: 1 failed, 174 passed — EXIT 1
        FAILED TestFakeProviderE2E::test_a_repair_round_leaves_one_marker_per_task
  (c) packages/orchestration/project_brain.py FROM count 1
      tests/ui_server/test_handler_table_walk.py: 1 failed, 1 passed — EXIT 1
        FAILED test_every_cockpit_read_endpoint_answers_200_for_a_fake_job
  tracked diff after reverts: ''
  G5 PASS
  ```
  No mutation stayed green. The worktree was then removed (see External actions).
- **G6** runs after the push and is reported in the round report, because this commit precedes it.
- Full suite: not run (amend0917-throughput).

## Authored-text proofs

- Every `.agent/` and `docs/` file was built by `python3 .remedy-wt/f273-r1/build_c1.py` from `git show 80f7c529:<path>` bytes and the payload bytes; none was hand-edited. Its output: `## Findings lines 1`, `TO contains FROM: False`, `FROM line hits before 1`, `FROM after 0 TO after 1`. G1 re-proves every file against the committed tree.
- The code arrived only by `git apply` of the two reviewer-verified diffs; G2's subtree ids equal the reviewer's dry-run subtrees.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 claim | done | `f892f77e` |
| C2 R-0803 | done | `50eaf606`; resolution waits for the closure suite run |
| C3 R-0804 | done | `fbf60c65` |
| C4 R-0810 | done | `f0bfc4ba` |
| C5 handoff + push | done | This commit, then the push |
| G1, G2, G3, G4, G5 | done | All EXIT 0 as above |
| G6 | done | After the push; in the round report |

## Open findings

On the committed `.agent/live_review.md` (C1 onwards; C2 to C4 do not touch it), by `.remedy-wt/f273-r1/openset.py`: 130 open BY DISTINCT ID (ids with a `^- R-\d+ — ` line minus ids with a `^Done: R-\d+ — ` line) and 129 by the canonical line formula `scripts/rotate_live_review.py::count_open_findings`. Highest id R-0981. No resolution line was written this round.

## Deviations & assumptions

- **Commit sequence:** as ordered: C1, C2, C3, C4, C5, then the push. No extra commit.
- **G3/G4 first run in the wrong checkout:** the worker's shell cwd was the reviewer's `.remedy-wt/f273-r1-dry` worktree, so the first G3 and G4 runs executed there (G3 `961 passed in 66.78s`, EXIT 0; G4 `All checks passed!`, EXIT 0), not in the primary checkout. Both were re-run in the primary checkout with an explicit cwd; the transcripts above are those re-runs. The accidental run may have left `__pycache__` and `.ruff_cache` files in the dry worktree; the worker made no other change there. While checking, a `git status --ignored` of the dry worktree also listed entries under that worktree's own `.data/`. Those were already there from the reviewer's dry run. The worker's run there exited 0 with no `R-0803:` line, so it changed nothing in that root. The primary checkout's `.data/` was never listed, read or written by the worker.
- **Live-review join:** head payload ends `...both readings.\n` and the carried part starts at `## Findings`, so the re-headed file has no blank line before `## Findings`. That is the byte-exact spec, and G1 proves it.
- **Scratch:** gitignored, under `.remedy-wt/f273-r1/`: `build_c1.py`, `g1.py`, `g5.py`, `runc.py` (worker's), plus the reviewer's `run.py` and `openset.py`.

## Next

1. Phase 1 rule 1 (`.agent/STOP`), then the review of round 1.

Operator questions open: 5
