# Handback — F085 R59 · T002e, the `runtime-server` seam
Branch `feature/f085-sandbox-hardening` · base 79f79f27 · last measured commit b2104539 (this file is C5).

## Range
Review of 79f79f27..HEAD

## Commits
### fe6f592b docs(f085): save the R59 step block
| Path | +/- | Reason |
| `.agent/authored/f085-r59.md` | +447/-0 | C0a, block saved byte-verbatim |
### 29b17f14 docs(f085): mirror the R59 block into last_block
| Path | +/- | Reason |
| `.agent/last_block.md` | +368/-357 | C0b, same bytes mirrored |
### 0279b57e docs(f085): advance the plan to the R59 runtime-server seam
| Path | +/- | Reason |
| `.agent/plan.md` | +10/-8 | C1, PLAN13F→PLAN13T |
### b5b76e3c docs(f085): promote path resolution into the reviewer checklist
| Path | +/- | Reason |
| `docs/agents/planner_reviewer_prompt.md` | +14/-0 | C2, CHECKF→CHECKT, §3 item 24 |
### 307b4456 docs(f085): record the R58 PASS and register R-0559
| Path | +/- | Reason |
| `.agent/live_review.md` | +65/-0 | C3, RECORD27 appended |
### b2104539 feat(f085): add the runtime-server exec policy and its test
| Path | +/- | Reason |
| `packages/orchestration/exec_guard.py` | +58/-0 | C4, SEAMCODE appended |
| `tests/orchestration/test_exec_guard.py` | +31/-0 | C4, TESTCODE appended |
### C5 (this commit) docs(f085): write the R59 handback
| Path | +/- | Reason |
| `.agent/handoff.md` | rewrite | C5, self-referential; insertions in the round report |

## External actions
- `git worktree add .remedy-wt/g9-r59 HEAD` — created, detached at b2104539, for G9 only.
- `git worktree remove --force .remedy-wt/g9-r59` — removed; `git worktree list` back to one line.
- `git push -u origin feature/f085-sandbox-hardening` — after C5. No PR, no merge, no force-push.

## Verification
G1 STATE. `.agent/STOP` absent before C0a and again before C5 (`ls` → No such file).
`git status --porcelain` empty at round start and after every commit. `git worktree list` one line at
start and at end, G9's worktree created and removed in between.
G2 TRANSPORT. All FIVE copies byte-EQUAL disk-to-disk, no digest fallback — reviewer's
`.remedy-wt/f085-r59.md`, committed and working `.agent/authored/f085-r59.md`, committed and working
`.agent/last_block.md`: sha256 8df06395327c5573a708a055a05eaf9b0d0d02b5103ba823908f1e13abbc1fed,
31513 B, 447 lines, 14 marker lines — each measured on each copy.
G3 SHAPES. PLAN13F→PLAN13T at 0279b57e is a REWRITE: FROM 0x, TO 1x in the post-commit blob.
CHECKF→CHECKT at b5b76e3c is APPEND-shaped (`TO contains FROM: true`): FROM 1x, TO 1x, no zero count
reported. For BOTH, re-applying the extracted FROM→TO to the pre-commit blob reproduces the post-commit
blob BYTE-EXACTLY. RECORD27 (307b4456), SEAMCODE and TESTCODE (b2104539): pre-commit blob is a
byte-exact PREFIX, the slice an exact SUFFIX, the commit's ADDED lines equal the slice's lines IN ORDER
(65 / 58 / 31). numstat `10 8`, `14 0`, `65 0`, `58 0`, `31 0`. Marker LINES matching
`^(BEGIN|END)-[A-Z0-9]+$` = 0 in all five edited files at HEAD.
G4 SUITES, primary checkout, each exit 0: `test_exec_guard.py -rf -q` → `36 passed`, base 35 plus the
one added test, so it IS 36; the four state readers → `160 passed`, unchanged as expected; canary
`test_golden_path.py -q` → `42 passed`.
G5 LINT, repo `pyproject.toml`, never `--isolated`, over the two `.py` paths, STRONG form:
`ruff check` exit 0 `All checks passed!`; `ruff check --preview` exit 0 `All checks passed!`.
G6 PLAN CONTRACT at 0279b57e: 45 lines (≤50, the projected figure); `## Goal` true, `## Next Steps`
true, `\bF\d{3}\b` true.
G7 ARITHMETIC. 79f79f27: 173 / 28 / 0, 145 open, max registered R-0558, max resolved R-0558.
HEAD: 174 / 28 / 0, 146 open, max registered R-0559, max resolved R-0558, next free R-0560. Registered
symmetric difference `{R-0559}` ADDED; done and landed symmetric differences both EMPTY. Duplicate ids
0 and resolutions naming an unregistered id 0, at BOTH SHAs.
G8 HYGIENE. `git diff --name-only 79f79f27..HEAD` before C5 = exactly the change set minus
`.agent/handoff.md`, holding none of the three R60 paths. Those three resolved on disk, one
`git ls-tree 79f79f27 -- <path>` call each, all three RESOLVE: `apps/cli/commands/runtime_cmd.py`
01ab65ed, `packages/runtimes/dev_server.py` 7715a28e, `packages/runtimes/runtime_supervisor.py`
9f3749ae. Per-commit INSERTIONS before C5: 447, 368, 10, 14, 65, 89 — none over 500, so the d4473f85
oversize allowance is untouched. All six commits single-parent.
G9 RED CONTROL, disposable worktree from HEAD, since removed; the primary checkout was never mutated.
`wall_timeout_seconds=None,` occurs 2x after C4; the LAST occurrence, in `runtime_server_exec_policy`,
alone became `wall_timeout_seconds=30.0,` (numstat `1 1`). `python3 -m pytest
tests/orchestration/test_exec_guard.py -rf -q` → EXIT 1, summary verbatim:
`FAILED tests/orchestration/test_exec_guard.py::test_the_runtime_server_policy_holds_no_clock_and_no_cap`
`1 failed, 35 passed in 14.29s`. Worktree removed; one line; tree clean.
BLOCK SIZE re-measured from the committed `.agent/authored/f085-r59.md`: TOTAL 447 (cap 490), PROSE
243 (cap 400), RECORD27 65 (cap 140) — all three match the block's own figures.

## Authored-text proofs
Every slice was extracted PROGRAMMATICALLY from the committed `.agent/authored/f085-r59.md` by its marker
pair under the block's CONVENTION and applied as bytes, never retyped or reflowed; the disk-to-disk
comparison against the reviewer's original is G2's five-copy equality above.

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C0a  | done   | |
| C0b  | done   | |
| C1   | done   | |
| C2   | done   | |
| C3   | done   | |
| C4   | done   | |
| C5   | done   | this commit |

## Deviations & assumptions
Declared overage (DECISION D15): this file is 111 lines against the ≤100 allowance, caused by mandated
content alone — nine gate transcripts, seven per-commit tables, the item-status table. No section is
dropped. Otherwise none: the ordered sequence C0a·C0b·C1·C2·C3·C4·C5 ran in order with no extra,
dropped or reordered commit, no ledger text was authored by the worker, and nothing in RECORD27
disagrees with any reading measured this round.

## Next
ONE: the next round is R60, which migrates the three `runtime-server` call sites —
`apps/cli/commands/runtime_cmd.py`, `packages/runtimes/dev_server.py` and
`packages/runtimes/runtime_supervisor.py` — onto `runtime_server_exec_policy` via `plan_child_spawn`, each
keeping its own `Popen` and its own supervision. TWO: R60 also carries the R59 verdict, because the round
that records a verdict cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13).
THREE: 146 findings are open and the next free id is R-0560.
FOUR: Phase 1 rule 1 first: re-read `.agent/STOP` from disk.

Fortschritt: ~97 % (T001 gebaut · R13-R58 PASS · T002a KOMPLETT · T002b KOMPLETT · T002c KOMPLETT ·
T002d KOMPLETT · T002e — die `runtime-server`-Policy gebaut, die drei Call-Sites offen · T003 offen)
— Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.
