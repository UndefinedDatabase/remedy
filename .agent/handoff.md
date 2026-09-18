# Handoff — F270 History apply: one commit per task, merge on demand · Round 8 (CI repair)

## Session

SESSION 1 of feature F270 · round 8 · rounds so far 8

Context self-assessment: the worker read the block, AGENTS.md's Commit Gate and Open PR Gate, the ledger payload with R-0979, `wait_ready` in `packages/runtimes/dev_server.py` and the test it times once each, and every figure below comes from a command run in this round.

## Range

Review of b91fb1ec..HEAD — branch `feature/f270-history-apply`.

## Summary

Round 8 repairs pull request 258's hosted CI under AGENTS.md amendment amend0820-gate-autonomy. Hosted run `35401706742` on `b91fb1ec` failed `tests/runtimes/test_dev_server.py::TestReadiness::test_delayed_readiness`.

- C1 booked round 7's verdict (PASS) and R-0979 into `.agent/live_review.md`, set `.agent/plan.md`, and saved byte copies of the five payloads, the block included.
- C2 is the repair. The test now takes `time.monotonic()` before `start()` and asserts that the whole wait from that point is at least 1.4 s. It no longer relies on `wait_ready`'s own clock, which starts only after `start()` has returned. No production file changed.
- C3 is this handoff.

## Commits

### f9b39633 F270 R8 C1: book round 7's closure verdict PASS, register R-0979, save the round 8 payload and block copies
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f270-r8-block.md` | +67 / -0 | Byte copy of the block |
| `.agent/authored/f270-r8-ledger.md` | +4 / -0 | Byte copy of ledger.md |
| `.agent/authored/f270-r8-plan.md` | +25 / -0 | Byte copy of plan.md |
| `.agent/authored/f270-r8-test_from.txt` | +6 / -0 | Byte copy of test_from.txt |
| `.agent/authored/f270-r8-test_to.txt` | +9 / -0 | Byte copy of test_to.txt |
| `.agent/live_review.md` | +4 / -0 | `b91fb1ec` bytes + ledger.md (Gate F270 R7 PASS, R-0979) |
| `.agent/plan.md` | +7 / -5 | := plan.md |

122 insertions, 5 deletions (`git show --numstat`).

### e0fe9573 F270 R8 C2: R-0979 — test_delayed_readiness times the wait from before start(), not from wait_ready's own clock
| Path | +/- | Reason |
|------|-----|--------|
| `tests/runtimes/test_dev_server.py` | +4 / -1 | test_from.txt (1x at `b91fb1ec`) rewritten to test_to.txt |

4 insertions, 1 deletion (`git show --numstat`).

### C3 (this commit) F270 R8 C3: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C1, with 122.

## External actions

- `git worktree add --detach .remedy-wt/f270-r8-g4 e0fe9573` for G4, then `git worktree remove --force` on it. `git worktree list` afterwards shows the primary checkout alone: `/home/decodeux/Repos/remedy  e0fe9573 [feature/f270-history-apply]`.
- `git push` after C3 (this commit) pushes C1 to C3 to the branch of pull request 258. The push is not forced. This round does not merge, comment on or edit pull request 258.
- No evidence job and no zip.

## Verification

- **Transport**, before any write: `sha256sum` of the block read `5e54026c170c8761f273f356a543231db104036bc7155986aeccba0b3ecc78de`. ledger.md `025805f5…19e3`, plan.md `33e4f712…7dc9`, test_from.txt `7a638305…18a2` and test_to.txt `a9c01472…bbc4` each matched the block's digests.
- **G1** at C2, `python3 .remedy-wt/f270-r8/g1_g2.py`, exit 0: each of the five payload digests `True`. Each `.agent/authored/f270-r8-*` copy equals its payload: `True` for all five. `.agent/plan.md equals plan.md: True`. `.agent/live_review.md equals b91fb1ec bytes + ledger.md: True`. `G1 ALL: True`.
- **G2** (same script): `test_from.txt count: 0  test_to.txt count: 1`; `numstat of HEAD: e0fe9573 | 4	1	tests/runtimes/test_dev_server.py`, so that file alone. C2's build script printed `TO contains FROM: False` and `before FROM 1 TO 0 | after FROM 0 TO 1`.
- **G3** at C2, primary checkout, serial: `python3 -m pytest -q -p no:cacheprovider tests/runtimes/test_dev_server.py tests/cli/test_golden_path.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py` → `208 passed in 64.34s (0:01:04)`, exit 0, 0 failed. `python3 -m ruff check tests/runtimes/test_dev_server.py` → `All checks passed!`, exit 0.
- **G4**, disposable worktree `.remedy-wt/f270-r8-g4` at C2, run from its root. The `packages.runtimes.dev_server` import resolved inside the worktree.
  - Control, unmutated, after purging `__pycache__` (0 dirs present): `python3 -B -m pytest -q -p no:cacheprovider tests/runtimes/test_dev_server.py::TestReadiness` → `4 passed in 3.87s`, exit 0.
  - Mutant: in `wait_ready` the line `            if READY_STATUS_MIN <= status <= READY_STATUS_MAX:` (count 1, then 0) became `            if True:`. After purging `__pycache__` (2 dirs), the same command gave `4 failed in 0.37s`, exit 1. `test_delayed_readiness` went red on the new assertion: `assert (1437662.994474985 - 1437662.990302461) >= 1.4`. All four nodes failed:
    ```
    FAILED tests/runtimes/test_dev_server.py::TestReadiness::test_immediate_readiness
    FAILED tests/runtimes/test_dev_server.py::TestReadiness::test_delayed_readiness
    FAILED tests/runtimes/test_dev_server.py::TestReadiness::test_readiness_timeout_stops_the_tree_and_leaves_no_state
    FAILED tests/runtimes/test_dev_server.py::TestReadiness::test_child_exits_before_readiness
    ```
  - The worktree was then removed (see External actions).
- **G5** comes after the push, so the round report carries it.
- Full suite not run (amend0917-throughput). The hosted CI re-runs it on the push.

## Authored-text proofs

- The byte copies are at `.agent/authored/f270-r8-{block.md,ledger.md,plan.md,test_from.txt,test_to.txt}`. Each is `True` against its payload (G1). The block copy's digest is `5e54026c170c8761f273f356a543231db104036bc7155986aeccba0b3ecc78de`.
- `.agent/live_review.md` and `.agent/plan.md`: byte checks `True` (G1).
- `tests/runtimes/test_dev_server.py`: built from `git show b91fb1ec:` bytes with a single FROM→TO replace. The script asserts FROM 1x before, and FROM 0x and TO 1x after (G2).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | `f9b39633`; Gate F270 R7 PASS and R-0979 booked |
| C2 repair (R-0979) | done | `e0fe9573`; G4 red-proof holds |
| C3 handoff | done | This commit |

## Open findings

By distinct id, `python3 scripts/rotate_live_review.py --dry-run` (exit 0, nothing written) reads `open findings before: 129`. That is round 7's 128 plus R-0979, which this round registers. R-0979 is repaired in C2 and stays open until the reviewer books its resolution. R-0974, R-0977 and R-0978 stay open, owned by F273.

## Deviations & assumptions

- **Commit sequence:** as ordered (C1, C2, C3, then the push). No extra commit.
- **Driver scripts:** the copies, the replace and the gates ran through gitignored scratch in `.remedy-wt/f270-r8/`: `c1_build.py`, `c2_build.py`, `g1_g2.py` and `g4_tools.py`.
- **Open-findings count:** the count comes from the rotation script's `--dry-run`, which writes nothing (`git status --porcelain` was empty after it).

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. The review of round 8.
3. The Open PR Gate on pull request 258, after its hosted CI on the pushed tip.

Operator questions open: 5
