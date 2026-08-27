# Handback — F032 R6 (T002a, the budget stop gets its receipts)

## Session

SESSION 2 of feature F032 · round R6 · rounds so far 6

Session 1 was R1 through R5 and ended at `59c8bcd0`. The soft limit is 25 rounds
or 7 sessions, whichever comes first; neither is near.

## Range

Review of `59c8bcd0e589c1ed7b1e14941ad21e6238584b9e`..`HEAD`
(branch `feature/f032-evidence-triple`, round base `59c8bcd0`).

## Commits

### cd20fb84 chore(agent): save the F032 R6 block as authored text
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f032-r6.md` | +404 / -0 | C0a — the block saved byte for byte from `.remedy-wt/f032-r6.md` |

### 1b1d119c chore(agent): mirror the F032 R6 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +318 / -215 | C0b — same bytes, same git blob as C0a |

### 955c8f08 docs(agent): point the plan at R6, the first producer upgrade
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +21 / -21 | C1 — whole-file replacement by slice PLANF032R6 |

### faf02674 docs(agent): book the F032 R5 verdict and resolve R-0711
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +4 / -0 | C2 — append of slice LEDGER6 |

### 96629ec8 docs(roadmap): rule DECISION F032 D6, the budget stop states its options
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/decisions.md` | +41 / -0 | C3 — append of slice DECISION6 |
| `docs/roadmap/features/T5_F032.md` | +13 / -0 | C3 — append of slice FEATURE6 (amendment A6) |

### 4c5b6f15 feat(orchestration): the budget stop carries its receipts and joins the gate set
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/decision_queue.py` | +68 / -1 | C4 — refs, per-choice outcomes, `payload.options`, retired emit-gate comment |
| `packages/orchestration/decision_evidence.py` | +10 / -7 | C4 — `TRIPLE_REQUIRED_TYPES` holds `token_budget`; its `#:` comment retired |

### c0a87dca test(orchestration): pin the budget stop triple and the live gate set
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_decision_evidence.py` | +196 / -4 | C5 — exact-membership test replaces the empty-set test; eight budget-branch tests |

### C6 docs(agent): hand back F032 R6
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | self | C6 — a handoff cannot table the commit that writes it (R-0149) |

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | |
| C0b mirror it into `last_block` | done | |
| C1 the plan | done | |
| C2 the R5 verdict and `Done: R-0711` | done | |
| C3 DECISION F032 D6 and its feature-file amendment | done | |
| C4 the budget triple, the gate set and the two retired comments | done | |
| C5 its tests | done | |
| C6 the handback | done | this commit |
| push | done | stated as intent below; outcome is in the round report only |
| S1 read the budget branch first | done | the three strings each counted 1 at `59c8bcd0e589` |
| S2 refs built from what the branch already has | done | 1 always, 2 conditional, none with an empty target |
| S3 outcomes keyed per choice, limit named as a noun phrase | done | `the exhausted limit of <n>` / `the exhausted limit` |
| S4 `payload={"options": ["extend", "abandon"]}` | done | `next_actions` unchanged |
| S5 `token_budget` joins the gate set; two comments retired | done | both retired at their source in the same commit |
| S6 the tests | done | in `tests/orchestration/test_decision_evidence.py` only |

## External actions

- `git worktree add --detach .remedy-wt/f032r6-mut c0a87dca` — exit 0.
- `git worktree remove --force .remedy-wt/f032r6-mut` — exit 0; `git worktree prune` — exit 0.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — exit 0, output `[]`. Nothing merged, nothing created.
- INTENT after C6: `git push origin feature/f032-evidence-triple`. Its outcome is not a value of any file this round writes, so no exit code and no remote tip are stated here; both are in the round report.
- No pull request was created and nothing was merged.

## Verification

- G1 hygiene, base, sentinel — exit 0. `git rev-parse HEAD` before C0a was `59c8bcd0e589c1ed7b1e14941ad21e6238584b9e`, the round base; branch `feature/f032-evidence-triple`; `git status --porcelain` 0 lines after each of C0a…C6; `.agent/STOP` ABSENT at both readings.
- G2 transport — exit 0. Scratch `.remedy-wt/f032-r6.md`, the C0a blob and the C0b blob are all sha256 `7018fa817a638c7cb3b4612326fa85fc477c063abd525a295739048a0f873492`, 30984 bytes, 404 lines, and ALL THREE EQUAL; C0a and C0b are the SAME git blob `8a69c3970dce13b2412c3c0d8c82ef662b9e94f6`. This proves the scratch original, the saved copy and the mirror agree; it says nothing about the bytes of any prompt.
- G3 extraction and caps — exit 0. 4 regions: PLANF032R6 45, LEDGER6 3, DECISION6 40, FEATURE6 12; CONTENT 100; TOTAL 404; PROSE 304 — under 400, and TOTAL under 490.
- G4 the plan — exit 0. `.agent/plan.md` at C1 byte-equal to PLANF032R6; the minus-trailing-newline NEGATIVE CONTROL FALSE; `wc -l` 45, under 50; `^## Goal$` 1 and `^## Next Steps$` 1.
- G5 the three appends — exit 0. `live_review.md` 1047137 + 1 + 4847 = 1051985, base a byte PREFIX; independent structural reader: LEDGER6 is 2 paragraphs and the LAST 2 units of the file equal them in order; the in-memory one-byte flip inside the FIRST appended paragraph is REJECTED BY BOTH readers and the tracked file was never mutated. `decisions.md` 639470 + 1 + 2601 = 642072; `T5_F032.md` 9364 + 1 + 846 = 10211, both prefix-clean. `^## DECISION F032 D\d+ ` 5→6 and `^## DECISION ` 163→164, ADDED key exactly `D6`; `^## Design amendments$` still 1. Ledger sets across C2: `^Gate: F\d+ R\d+ — ` 57→58 adding exactly `F032 R5`; `^Done: R-\d+ — ` 21→22 adding exactly `R-0711`; `^- R-\d+ — ` 272→272, `^Gate: R\d+ — ` 19→19, `^Landed: R-` 1→1; open set 251→250; maximum id `R-0711`. Unchanged across C3, C4 and C5.
- G6 the code — `python3 -m ruff check packages/orchestration/decision_queue.py packages/orchestration/decision_evidence.py` REAL exit 0, output verbatim `All checks passed!`. Both drives of `list_decisions` read back the rendered card; `TRIPLE_REQUIRED_TYPES` is `frozenset({'token_budget'})`. Full transcript in the round report.
- G7 tests green then red — scoped file REAL exit 0, `36 passed`; worktree CONTROL unmutated REAL exit 0, `36 passed`; mutation (a) emptying the gate set REAL exit 1, `2 failed, 34 passed`; mutation (b) replacing the extend downside with `-` REAL exit 1, `8 failed, 28 passed`; each mutated string counted exactly 1 in the file it was changed in before it was applied. Nine decision-schema guard files as ONE pytest process: REAL exit 0, `324 passed`, `^FAILED` count 0 with the extractor sighted on a probe string containing such a line. `test_f018_authority_integration.py` REAL exit 0, `114 passed`, `^FAILED` 0.
- G8 structure, canary, PR gate — `tests/cli/test_golden_path.py` REAL exit 0, `42 passed`. Both path residues over `59c8bcd0..c0a87dca` EMPTY against the expected nine-path set; `apps/` diff EMPTY. Insertions 404, 318, 21, 4, 54, 78, 196 across C0a…C5, each single-parent and under 500. `^<<<SLICE ` and `^<<<END ` are 0 and 0 in all seven listed written files, against a CONTROL of 4 and 4 over the C0a blob. `git ls-files .remedy-wt` 0 lines, `git worktree list` 1 line, `git branch --list "tmp/*"` 0 lines. `gh pr list` `[]`.

## Authored-text proofs

- PLANF032R6 — `.agent/plan.md` at C1 is byte-equal to the slice extracted from the COMMITTED `.agent/authored/f032-r6.md` blob under the block's newline convention; negative control FALSE.
- LEDGER6 — `.agent/live_review.md` at C2 equals its pre-commit blob plus one newline plus the slice, byte for byte, under two independent readers.
- DECISION6 — `.agent/decisions.md` at C3 equals its pre-commit blob plus one newline plus the slice, byte for byte.
- FEATURE6 — `docs/roadmap/features/T5_F032.md` at C3 equals its pre-commit blob plus one newline plus the slice, byte for byte.
- Every slice was extracted programmatically from the committed C0a blob and written without retyping.

## Gate coverage after this round

ENFORCED by `TRIPLE_REQUIRED_TYPES` after this round: `token_budget`, and only
`token_budget`. STILL CARRYING THE LEGACY PLACEHOLDER
`recorded_before_evidence_requirements`: the other seven producing types of
`decision_queue.list_decisions` — `patch_approval`, `stop_reason`,
`test_failure`, `repo_dirty`, `memory_review`, `flight_plan_approval` and
`task_decision` (eight distinct types across nine construction sites, since
`flight_plan_approval` is built in two arms). Each joins the set only in the
commit that gives its producer a real triple.

## Deviations & assumptions

- NO DEPARTURE FROM THE ORDERED COMMIT SEQUENCE. The commits are exactly C0a, C0b, C1, C2, C3, C4, C5, C6, in that order, and no commit was made beyond the ordered sequence.
- ASSUMPTION, ordered by constraint 5: C0a and C0b landed while `.agent/plan.md` still described R5. AGENTS.md requires `plan.md` to be current before every commit; the block orders this sequence explicitly and the plan becomes current at C1, one commit later.
- OBSERVED, NOT FIXED, and no finding id minted (constraint 7 forbids me one). Two comments in `packages/orchestration/decision_evidence.py` — the `#:` block above `UNKEYED_OPTION` and the docstring of `evidence_triple_problems` — both say "six of the eight producing branches carry no options list (DECISION F032 D3)". The budget branch now carries an options list, so that count is one too high from this round on. S5 named exactly two comments to retire and said "Retire nothing else", so I retired exactly those two and left these. The reviewer decides whether this is a slip or a finding.
- SCRATCH, untracked and gitignored: `.remedy-wt/g5a.py`, `.remedy-wt/c3.py`, `.remedy-wt/g5b.py`, `.remedy-wt/g6drive.py`, `.remedy-wt/mut_a.py`, `.remedy-wt/mut_b.py`, `.remedy-wt/g8.py` were written to route counting, hashing and mutation through python under this session's command guard. `git ls-files .remedy-wt` is 0 lines and `git status --porcelain` is 0 lines, so nothing entered the repository. The disposable worktree `.remedy-wt/f032r6-mut` was removed and pruned before this handback.
- No numeral the block quoted about the round base disagreed with my measurement: the three S1 string counts were each 1, the append bases were 1047137, 639470 and 9364, ruff read `All checks passed!` at exit 0, the nine guard files read `324 passed` and the golden path read `42 passed`.

## Open findings

250 open after this round (272 registered, 22 resolved). `R-0711` moved from
open to resolved at C2. No new finding id was minted by this worker.

## Next

The reviewer re-runs G1 through G8 at `HEAD` and rules on R6; T002 then
continues with the patch-approval producer, which joins
`TRIPLE_REQUIRED_TYPES` in the commit that gives it a real triple.
