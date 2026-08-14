# Handback — F057 Rate-limit-aware scheduler · Round 2 (R1 verdict + two fixes)

## Range
36b745bd..HEAD, 6 commits, branch feature/f057-rate-limit-scheduler. Every commit
pushed. No PR, no merge, no `main` commit, no force-push. T002 is NOT in this
round: no governor, no `acquire`, no clock, no new module.

## Commits
| SHA | Subject | Item |
| 835c40f5 | chore(f057): save the R2 block verbatim | C0a |
| 07fd8c19 | chore(f057): point last_block at the R2 block | C0b |
| 28949e9b | docs(f057): record the R1 verdict and register four findings | C1 |
| 47575d5f | docs(f057): correct the rate-limit predicate's call-graph claim | C2 |
| 08810088 | test(f057): assert FrozenInstanceError instead of bare Exception | C3 |
| (this)   | chore(f057): handback R2 | C4 |

## Changed files (36b745bd..HEAD)
| Path | +/- | Reason |
| .agent/authored/f057-r2.md | +187/-0 | C0a, the R2 block verbatim |
| .agent/last_block.md | +160/-377 | C0b, `cmp` vs the authored file exit 0 |
| .agent/live_review.md | +7/-0 | C1, APPEND only: GATE-R1 + R-0363..R-0366 |
| packages/orchestration/rate_governor.py | +7/-3 | C2, one docstring paragraph |
| tests/orchestration/test_rate_governor.py | +2/-1 | C3, one import + one assert |
| .agent/plan.md | rewrite | C4 |
| .agent/handoff.md | rewrite | C4 |
No eighth file. Nothing above the appended block in live_review.md moved.

## Item status
| Item | Status | Reason |
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | numstat gate deviated, see Deviations 1; the edit itself is exact |
| C3 | done | |
| C4 | done | |

## Round gates — real output
1 `git status --porcelain` → empty · 2 `git worktree list` → 1 line ·
3 branch → `feature/f057-rate-limit-scheduler` · 4 `Gate: R1 — PASS` → 1 ·
5 `- R-0363 — ` 1, `- R-0364 — ` 1, `- R-0365 — ` 1, `- R-0366 — ` 1 ·
6 R-0361 line sha256 (line + its newline) →
`70a8c9fb1a6ddebd2a1592b467cf9cb7e18f43ad0449c245d110bc0f1f056a7b`, matches ·
7 `## Steps` → 1 · 8 `pytest.raises(Exception)` in the test file → 0 ·
9 test_rate_governor.py → **46 passed**, exit 0 (46 before this round too: C3
changed an assertion, not the count) · 10 tests/docs/ → **295 passed**, exit 0 ·
11 canary test_golden_path.py → **42 passed**, exit 0 · 12 ruff over the two
feature files → `All checks passed!`, exit 0 · 13 `wc -l < .agent/plan.md` → 36 ·
14 `cmp .agent/authored/f057-r2.md .agent/last_block.md` → exit 0, both sha256
`114397a2c11b3492b5683d8390dcc84986c339d9382067971b3b706969aff684` ·
15 do-not-touch `git diff --stat 21c8148e..HEAD` over provider_timeouts.py,
pingpong_loop.py, stream_evidence.py → EMPTY · 16 red-proof below.

## Transport — disk to disk, proved
Each authored text was extracted from the COMMITTED `.agent/authored/f057-r2.md`
(`git show HEAD:…`, byte-equal to the working copy) between its markers, written
to the target, and applied == extracted asserted on the re-read bytes. sha256:
GATE-R1 `19cf92db51b90ced89bb03c16bdd5272b0634271f1dbfb7c71cbe8e9aa42d607`,
FINDINGS-R1 `645c1da38862afef8ee535d59fbc04b2cb8ecacdfb4e283256bb74fc96bd9144`,
R0365-TO `457d4424c9ffa22fdf997fac945360b66d871c7554fd443c76eb2c5dd55c31f4`,
R0366-TO `af0c5533d666c894012432f75299c4102dda1aaeeef07ba84a01a506b4db88ec`.
Both FROM texts: 1 occurrence before their edit, 0 after. Both TO texts: exactly
1. No authored text was retyped.

## Red-proof probe for C3 — worktree only
Import path printed first, from inside the worktree: `MODULE
/home/decodeux/Repos/remedy/.remedy-wt/f057-r2-redproof/packages/orchestration/rate_governor.py`
— inside the worktree, so the probe tests the mutated code. Mutation:
`@dataclass(frozen=True)` → `@dataclass()` on `RateLimitSignal` (1 occurrence).
Result: **1 failed, 45 passed**, exit 1. The one failing id is
`test_signal_is_frozen`, failing with `Failed: DID NOT RAISE <class
'dataclasses.FrozenInstanceError'>` — the new assertion names the exception, so
the red is specific rather than incidental. Worktree removed and pruned;
`git worktree list` back to one line, primary `git status --porcelain` empty.

## Findings — 6 open
R-0361, R-0362 carried; R-0363, R-0364, R-0365, R-0366 registered this round.
R-0365 and R-0366 are fixed on disk but stay OPEN in the record: the worker does
not author resolutions, and no `Done:` paragraph was written.
- Landed: R-0365 — the `is_rate_limit_error` docstring now names
  `classify_rate_limit_reason` as owner of the wording table and says the readers
  reach it via `normalize_rate_limit_signal`; commit 47575d5f.
- Landed: R-0366 — `test_signal_is_frozen` asserts
  `dataclasses.FrozenInstanceError`; commit 08810088.
Next free id: R-0367.

## Deviations, declared (this handoff is 119 lines; DECISION D15 — the cause is
## the mandated per-commit table, the 16-gate block, the transport proof, the
## red-proof and the item-status table, none of which may be dropped)
1. **C2's third gate is RED as ordered and unreachable as written.** Ordered:
   `git show --numstat HEAD -- packages/orchestration/rate_governor.py` → `8 4`.
   Real: `7 3`. The cause is arithmetic in the block, not in the edit. R0365-FROM
   is 4 physical lines, R0365-TO is 8, and their LAST line — `    counts as X"
   drift apart, and the drift is the bug.` — is byte identical in both, so git
   renders it as context: 8-1 inserted, 4-1 deleted. No correct application of
   the reviewer's own pair can produce `8 4`. The condition the gate proxies for
   was met and proved directly: FROM 0 occurrences, TO exactly 1 and byte-equal
   to the extracted slice, and `git diff` touches nothing but that paragraph.
   Treated as the R-0336 / R-0361 / R-0364 family — a gate whose expected value
   was never computed from the tool that produces it, here unreachable rather
   than merely wrong — and declared instead of burning the round. No edit was
   made to reach `8 4`.
2. **Extraction and counting used Python, not `sed`, `grep -c` or redirection.**
   This session's sandbox denies `sed`, every pipe-to-file form, and `grep -c`
   patterns anchored with `$`. Marker slicing, line and occurrence counting and
   every sha256 ran as inline `python3` — the substitute R1 declared. Nothing was
   retyped; no scratch file was committed.
3. **The saved block runs to the end of the ROUND GATES section**, through the
   KNOWN-RED BASELINE note and the closing "report the exact output." paragraph,
   rather than stopping at gate item 16. Same boundary R1 declared.
Not a deviation, for the reviewer: repository-wide `python3 -m ruff check` is
still red at exit 1 with the 26 pre-existing errors the KNOWN-RED BASELINE names.
Correctly not a gate this round, and this round added none.

## Next
Next session's FIRST action is Phase 0 of docs/agents/self_drive_protocol.md,
then Phase 1 rule 1 — re-read `.agent/STOP` — BEFORE rule 2. The work itself is
T002: the governor, per-provider cooldown state, `acquire()` with a deadline
taken from budgets, an injected clock, and the stop-beats-wait ordering, with no
real sleeps in unit tests.
