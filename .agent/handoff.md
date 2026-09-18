# Handoff — F271 No more legacy: ownership, reachability, replace-is-delete · Round 1

## Session

SESSION 1 of feature F271 · round 1 · rounds so far 1

Context self-assessment: the worker read the block, AGENTS.md, `docs/roadmap/features/T2_F271.md`, DECISION F271 D1 and the prototype's C2 and C3 hunks in full once each, and every figure below comes from a command run in this round.

## Range

Review of a4f79a94..HEAD — branch `feature/f271-no-more-legacy`, cut from `main` at `a4f79a94`.

## Summary

- C1 claims F271: payload copies, `.agent/plan.md` and `.agent/context.md` set, `.agent/live_review.md` re-headed with F270 round 8's verdict and `Done: R-0979` booked, DECISION F271 D1 appended to `.agent/decisions.md`, and the STATUS line flipped from `[ ]` to `[~]`.
- C2 is T001. `apps/cli/command_catalog.py` gains `Reach`, which lists the seven reaches, and `GroupDef` gains two defaulted fields, `feature: str = ""` and `reach: Reach | None = None`. All 30 `GROUPS` entries get their owner and reach by keyword, exactly as D1 (3) gives them. `tests/test_command_catalog.py` gains `TestGroupOwnership`, whose second test plants four groups (no feature, no reach, reach `"nowhere"`, feature `F999`) and asserts their exact refusals. The STATUS lookup reads `docs/roadmap/STATUS.md` under `Path(__file__).resolve().parents[1]`.
- C3 is the D6 deletion. It runs `git rm` on `packages/orchestration/builder_eval.py`, `tests/orchestration/test_builder_eval.py` and `scripts/remedy_builder_eval.sh`, removes the `REAL_OLLAMA_FILES` line from `tests/conftest.py`, and applies the brain pair to `docs/system/project-brain.md`.
- C4 is this handoff.

## Commits

### 6f2ea352 F271 R1 C1: claim F271 — book F270 round 8's verdict and R-0979, land DECISION F271 D1, STATUS [~], save the round 1 payloads
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f271-r1-block.md` | +98 / -0 | Byte copy of the block |
| `.agent/authored/f271-r1-brain_from.txt` | +5 / -0 | Byte copy |
| `.agent/authored/f271-r1-brain_to.txt` | +1 / -0 | Byte copy |
| `.agent/authored/f271-r1-context.md` | +40 / -0 | Byte copy |
| `.agent/authored/f271-r1-decisions.md` | +43 / -0 | Byte copy |
| `.agent/authored/f271-r1-ledger.md` | +4 / -0 | Byte copy |
| `.agent/authored/f271-r1-live_review_head.md` | +22 / -0 | Byte copy |
| `.agent/authored/f271-r1-plan.md` | +29 / -0 | Byte copy |
| `.agent/authored/f271-r1-status_from.txt` | +1 / -0 | Byte copy |
| `.agent/authored/f271-r1-status_to.txt` | +1 / -0 | Byte copy |
| `.agent/context.md` | +14 / -17 | := context.md |
| `.agent/decisions.md` | +43 / -0 | `a4f79a94` bytes + decisions.md (DECISION F271 D1) |
| `.agent/live_review.md` | +17 / -13 | head + `a4f79a94` bytes from `## Findings` + ledger.md |
| `.agent/plan.md` | +19 / -15 | := plan.md |
| `docs/roadmap/STATUS.md` | +1 / -1 | F271 line `[ ]` → `[~]` (status pair) |

338 insertions, 46 deletions (`git show --numstat`).

### ee0bfe46 F271 R1 C2: T001 — every GroupDef names its owning feature and its reach, refused by TestGroupOwnership
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/command_catalog.py` | +46 / -30 | `Reach`, the two defaulted `GroupDef` fields, 30 annotated `GROUPS` entries |
| `tests/test_command_catalog.py` | +53 / -0 | `TestGroupOwnership` (shipped groups clean; planted groups refused exactly) |

99 insertions, 30 deletions.

### 154b34df F271 R1 C3: delete builder_eval.py with its test and script under DECISION amend0911-feedback D6
| Path | +/- | Reason |
|------|-----|--------|
| `docs/system/project-brain.md` | +1 / -5 | brain pair: FROM 1x before, 0x after, TO 1x after |
| `packages/orchestration/builder_eval.py` | +0 / -829 | deleted (D6) |
| `scripts/remedy_builder_eval.sh` | +0 / -158 | deleted (D6) |
| `tests/conftest.py` | +0 / -1 | `"test_builder_eval.py",` line removed from `REAL_OLLAMA_FILES` |
| `tests/orchestration/test_builder_eval.py` | +0 / -752 | deleted (D6) |

1 insertion, 1745 deletions.

### C4 (this commit) F271 R1 C4: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C1, with 338.

## External actions

- `git checkout -b feature/f271-no-more-legacy` from `main` at `a4f79a94`. `gh pr list --state open` returned `[]` before the branch was cut.
- `git worktree add -q --detach .remedy-wt/f271-r1-g5 154b34df` for G5, then `git worktree remove .remedy-wt/f271-r1-g5`. Afterwards `git worktree list` shows the primary checkout alone: `/home/decodeux/Repos/remedy  154b34df [feature/f271-no-more-legacy]`.
- `git push -u origin feature/f271-no-more-legacy` after C4, not forced. No pull request is opened.
- No evidence job and no zip.

## Verification

All gates below ran at C3 (`154b34df`) before C4.

- **Transport**, before any write: `sha256sum` matched all ten digests: the block `785b649d…0cf2e747`, plan.md, context.md, live_review_head.md, ledger.md, decisions.md, status_from/to and brain_from/to. The prototype's digest `e6270600…a164ff` matched as well. The C1 build printed `STATUS FROM before 1 after 0 TO after 1`, and the C3 build printed `brain FROM before 1 after 0 TO after 1`.
- **G1**: `python3 .remedy-wt/f271-r1/work/g1.py` printed `26 checks, all: True` (exit 0). The checks cover the ten payload digests, the ten `.agent/authored/f271-r1-*` copies at HEAD, plan.md, context.md, live_review.md (head + `a4f79a94` bytes from `## Findings` + ledger.md), decisions.md (`a4f79a94` bytes + payload), and STATUS.md and project-brain.md, each equal to its `a4f79a94` bytes with its pair applied.
- **G2**: the fifteen-target command as ordered, run serially in the primary checkout, printed `949 passed in 132.01s (0:02:12)` (exit 0, 0 failed).
- **G3**: `python3 -m ruff check apps/cli/command_catalog.py tests/test_command_catalog.py tests/conftest.py` printed `All checks passed!` (exit 0).
- **G4**: `git grep -n -e builder_eval -e remedy_builder_eval -- . ':!.agent' ':!docs/roadmap'` printed nothing (exit 1). `git ls-tree -r --name-only 154b34df -- <the three deleted paths>` also printed nothing (exit 0), so all three are absent.
- **G5**: disposable worktree `.remedy-wt/f271-r1-g5` at `154b34df`, run from its root with `python3 -B -m pytest -q -p no:cacheprovider tests/test_command_catalog.py -k TestGroupOwnership`. `__pycache__` was purged before each run and found 0 dirs each time. `apps.cli.command_catalog` resolved to `/home/decodeux/Repos/remedy/.remedy-wt/f271-r1-g5/apps/cli/command_catalog.py` on every run. The `"ci":` entry line counted 1.
  - Control, unmutated: `2 passed, 55 deselected in 0.19s`, exit 0.
  - (a) `feature="F083",` removed: `1 failed, 1 passed, 55 deselected in 0.21s`, exit 1, `FAILED tests/test_command_catalog.py::TestGroupOwnership::test_every_group_names_its_feature_and_its_reach`.
  - (b) reach `"dev-path"`: `1 failed, 1 passed, 55 deselected in 0.21s`, exit 1, same failing id.
  - (c) feature `"F999"`: `1 failed, 1 passed, 55 deselected in 0.21s`, exit 1, same failing id.
  - Every mutation was reverted before the next, and the file was byte-equal to the original at the end (`reverted: True`). No mutation stayed green.
- **G6** comes after the push, so the round report carries it.
- Full suite not run (amend0917-throughput).

## Authored-text proofs

- The byte copies are at `.agent/authored/f271-r1-*`, ten files. Each is `True` against its payload (G1). The block copy's digest is `785b649d6e0cc3b1a09b0c4931418e21f325b93a0aaaae1a332a1cfa2cf0e747`.
- `.agent/plan.md`, `.agent/context.md`, `.agent/live_review.md`, `.agent/decisions.md`, `docs/roadmap/STATUS.md` and `docs/system/project-brain.md` were each built from `git show a4f79a94:` bytes, and each byte check is `True` (G1).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 claim | done | `6f2ea352` |
| C2 T001 | done | `ee0bfe46`; G5 red-proof holds for (a), (b) and (c) |
| C3 deletion (D6) | done | `154b34df`; G4 grep at zero |
| C4 handoff | done | This commit |

## Open findings

By distinct id on the committed `.agent/live_review.md` at C3, `^- R-\d+ — ` gives 133 ids and `^Done: R-\d+ — ` gives 4, so 129 are open. That is the reviewer's 130 at `a4f79a94` minus R-0979, now Done. `python3 scripts/rotate_live_review.py --dry-run` counts the live file together with its archive and read `open findings before: 128` (exit 0, nothing written). The archive therefore resolves one more id than the live file does alone.

## Deviations & assumptions

- **Commit sequence:** as ordered (C1, C2, C3, C4, then the push). No extra commit.
- **Prototype:** C2 and C3 are the prototype's hunks, applied with `git apply --include` for C2. For C3, a python replace of the two authored pairs produced the same blobs (`dc48e5bc`, `3beb6acd`), and `git rm` removed the three files. The worker checked every C2 owner and reach against D1 (3). All 30 match, and all 18 distinct owners have a STATUS line.
- **Driver scripts:** the builds and gates ran through gitignored scratch in `.remedy-wt/f271-r1/work/`: `build_c1.py`, `build_c3.py`, `g1.py`, `g5.py`, `openset.py` and `rungate.py` (which prints the exit code).

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. The review of round 1.

Operator questions open: 5
