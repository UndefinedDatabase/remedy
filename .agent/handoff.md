# Handoff — F105 R5 (T002 repair)

Feature F105 Cache-optimal prompt ordering, round R5: close R-0229 and R-0230,
each with a red-proof, and record DECISION F105 D2. No feature work.
Branch `feature/f105-cache-optimal-prompt-ordering`. No PR exists or was created.

## Range
Review of `65d3c7b9..HEAD` (five commits below plus this handoff commit).

## Commits

### f7fa9417 chore(f105): save the R5 repair block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f105-r5-1.md | +295 | C1 — the R5 block, byte for byte |

### 2890f4f8 chore(f105): mirror the R5 repair block into last_block.md
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +234/-202 | C1 — same bytes; split out, see Deviations |

### 0eb04776 chore(f105): persist R-0229 and R-0230 and the R4 record
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +38 | C2 — pairs A and B, findings before any fix |

### 6f627e13 chore(f105): pin the conventions mapping to expected literals
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_role_conventions.py | +24 | C3 — 4 literal-per-role tests |
| .agent/live_review.md | +2 | C3 — the R-0229 `Landed:` line |

### 8e54c7d1 fix(f105): treat an undecodable conventions document as a load error
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/role_conventions.py | +1/-1 | C4 — catch UnicodeDecodeError |
| tests/orchestration/test_role_conventions.py | +8 | C4 — the non-UTF-8 test |
| .agent/live_review.md | +2 | C4 — the R-0230 `Landed:` line |

### (this commit) chore(f105): hand back R5
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +25 | C5 — pair C, DECISION F105 D2 |
| .agent/plan.md | +31/-17 | C5 — the authored rewrite, verbatim |
| .agent/context.md | +5/-4 | C5 — pair D |
| .agent/handoff.md | rewrite | C5 — this file |

## External actions
- `git worktree add .remedy-wt/f105-r5-redproof HEAD --detach` → created at 6f627e13.
- `git worktree remove --force .remedy-wt/f105-r5-redproof` + `git worktree prune`
  → `git worktree list` shows the primary checkout alone. Nothing committed from it.
- `git push -u origin feature/f105-cache-optimal-prompt-ordering` runs immediately
  after this commit; its real outcome is in the completion report.
- No PR created, edited or merged. No `gh` command run.

## Verification
| # | Command | Exit | Real trimmed output |
|---|---|---|---|
| A | `cmp .agent/authored/f105-r5-1.md .agent/last_block.md` | 0 | no output |
| B | `pytest tests/orchestration/test_role_conventions.py -q` | 0 | `26 passed in 0.10s` |
| C | `pytest tests/orchestration/test_prompt_segments.py -q` | 0 | `22 passed in 0.09s` |
| D | `pytest tests/orchestration/test_test_runner.py -q -k "live_review or context_md or plan_md"` | 0 | `4 passed, 47 deselected in 0.14s` |
| E | `pytest tests/docs/ -q` | 0 | `294 passed in 0.25s` |
| F | `pytest tests/cli/test_golden_path.py -q` (canary) | 0 | `42 passed in 19.43s` |
| G | `git status --porcelain` | 0 | empty |
| H | `git worktree list` | 0 | `/home/decodeux/Repos/remedy … [feature/f105-…]` alone |
| I | integrity check `--json` via `apps.cli.grouped:main` | 0 | `passed=True fail_count=0`, 5 checks |

J — C3 red-proof, inside `.remedy-wt/f105-r5-redproof` at 6f627e13 with the two
values of `CONVENTIONS_SEGMENT_NAMES` exchanged: `2 failed, 23 passed in 0.12s`.
Failing: `TestRoleConventionsMappings::test_segment_name_mapping_holds_the_expected_literal`
`[worker-worker_conventions]` and `[reviewer-reviewer_conventions]`. File restored,
worktree removed and pruned before this handoff.

K — C4 red-proof, primary checkout, the test added BEFORE the module change:
`1 failed, 25 deselected in 0.09s` with `UnicodeDecodeError: 'utf-8' codec can't
decode byte 0xff in position 0: invalid start byte` at `role_conventions.py:107`.
After the except-clause change: `1 passed, 25 deselected in 0.08s`.

## Authored-text proofs
- Step block: `cmp` of `.agent/authored/f105-r5-1.md` against `.agent/last_block.md`
  exit 0, no output — identical.
- Pairs A, B, C, D, the `plan.md` body and both `Landed:` lines were SLICED by line
  range out of `.agent/authored/f105-r5-1.md` on disk, never retyped. Each FROM was
  counted `== 1` immediately before its write; pair D is REWRITE-shaped and after
  the write FROM is 0x and TO is 1x. No touched file carries trailing whitespace.

## Deviations & assumptions
- Deviations, declared: this handoff is 114 lines, over the 60/100 caps. Cause, per
  DECISION D15: the six per-commit tables, the nine-row verification table, the two
  red-proof transcripts and the C1 deviation record. No section was dropped.
- DEVIATION, C1 — the block ordered ONE commit for both files. Measured, that commit
  is 529 insertions, over the AGENTS.md 500 cap, and F105's once-per-feature oversize
  exception is already spent on `ea48ea89` (523). The cause is the block itself: it is
  295 authored lines, 55 over the 240-line cap DECISION F105 D2 sets in that very
  block. AGENTS.md ("if a diff exceeds 500 lines, stop and split") resolves it, so C1
  landed as two commits — f7fa9417 (+295) and 2890f4f8 (+234, also exempt as a single
  `.agent/**` state-file rewrite under DECISION F104 D1). Bytes, order and the `cmp`
  proof are unchanged. The reviewer's D2 needs a smaller R6 block to hold.
- DEVIATION, C3 ordering — the red-proof ran against the COMMITTED state 6f627e13
  rather than before the commit, because `git worktree add … HEAD` cannot see an
  uncommitted test. Strictly stronger evidence; the result matches the `Landed:` line.
- Assumption: pair A's TO keeps its internal blank line and ends at
  "…pin it with a test. OPEN."; pair B's TO is contiguous through the R5 step line.
- No `docs/`, `docs/roadmap/`, `AGENTS.md` or `apps/` byte changed; neither
  conventions document was touched; the literal 800 is in neither module nor test.

## Open findings
R-0221 OPEN (carried). R-0229 and R-0230 carry `Landed:` lines only — a worker never
writes `Done:`. `LAST_REVIEWED_SHA` stays 1a054862 until the reviewer gates R5.

## Next
The reviewer gates R5 over `65d3c7b9..HEAD`, then authors the R6 block (the distilled
discoverability block for both conventions documents) at 240 authored lines or fewer.
