# Handoff — F105 Cache-optimal prompt ordering, R4

Feature F105, round **R4** (T002 part 1), branch
`feature/f105-cache-optimal-prompt-ordering`. Nothing merged, no PR created or
edited, no force-push, no branch switch, no work on main, no worktree added or
removed.

## Range
Review of **1a054862..HEAD** (4 commits).

## Commits

### ea48ea89 chore(f105): save the R4 block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f105-r4-1.md | +263 | the R4 block, verbatim (new) |
| .agent/last_block.md | +260/-62 | same bytes; replaces the R3 block |

Both files sha256
`6343e79111334c0e68d6beeeed28419d392e280e1471048d8194bc4aeec8491c`.

### 62e7867e chore(f105): record the reviewer gate on R3
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +25 | authored pair A, append-shaped; 77 lines now |

### e9b32469 feat(f105): load the role conventions as a verbatim prompt segment
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/role_conventions.py | +135 | the conventions loaders (new) |
| tests/orchestration/test_role_conventions.py | +188 | goldens and guards (new) |

### (this commit) chore(f105): hand back R4
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +16/-16 | authored text, verbatim; 44 lines; current step R4 |
| .agent/context.md | +5/-3 | authored pair B, rewrite-shaped |
| .agent/handoff.md | rewrite | this file (template self-reference exception) |

## External actions
`git push -u origin feature/f105-cache-optimal-prompt-ordering` — result in the
completion report. No PR created, edited or merged; **no PR exists for this
branch**, it is created at closure. No `gh` command, no worktree add or remove.

## Verification
Run by me from the repo root; real exit codes, real trimmed output.

| Gate | Command | Exit | Result |
|---|---|---|---|
| A | `cmp .agent/authored/f105-r4-1.md .agent/last_block.md` | **0** | no output — byte-identical |
| B | `pytest tests/orchestration/test_role_conventions.py -q` | **0** | 21 passed in 0.08s |
| C | `pytest tests/orchestration/test_prompt_segments.py -q` | **0** | 22 passed in 0.07s |
| D | `pytest tests/orchestration/test_token_economy.py -q` | **0** | 37 passed in 0.16s |
| E | `pytest tests/orchestration/test_test_runner.py -q -k "live_review or context_md or plan_md"` | **0** | 4 passed, 47 deselected in 0.11s |
| F | `pytest tests/docs/ -q` | **0** | 294 passed in 0.25s |
| G | `pytest tests/cli/test_golden_path.py -q` (canary) | **0** | 42 passed in 19.29s |
| H | `git status --porcelain` | **0** | EMPTY — re-run after this commit, real result in the completion report |
| I | `git worktree list` | **0** | `/home/decodeux/Repos/remedy` alone |
| J | `remedy integrity check --json` via `apps.cli.grouped:main` | **0** | `"passed": true`, `"fail_count": 0`, 5 checks |

## Authored-text proofs
- **Pair A** → `.agent/live_review.md`, append-shaped, sliced out of
  `.agent/authored/f105-r4-1.md` on disk, never retyped. FROM occurred **1x**
  before the write, TO occurs **1x** after, 24 of the 25 TO-only lines occur
  **1x** (the 25th is D2). No trailing whitespace on any line.
- **Pair B** → `.agent/context.md`, rewrite-shaped, sliced from the same file on
  disk. FROM **1x → 0x**, TO **0x → 1x**. No trailing whitespace.
- **`.agent/plan.md`** rewritten to the authored slice and compared against it
  byte for byte: **identical**. sha256
  `7f0ca088ddd3988938b2fb07f13eceb6415402ca3c05e58146c77272e7025127`, 44 lines.

## Deviations & assumptions
- **D1 — oversize commit, declared.** ea48ea89 carries **523 insertions**
  (`git diff --cached --stat`), 23 over the AGENTS.md cap. Both files hold the
  SAME authored bytes and C1 mandates committing them together, so the pair is
  inseparable: splitting it leaves the `cmp` proof unprovable. It is the only
  oversize commit in F105 — the previous maximum was 486.
- **D2 — unsatisfiable sub-condition, flagged not fixed.** C2 asks that each
  TO-only line occur exactly once. `  byte changed.` occurs **2x**: it already
  ended the R1 bullet before this write, and the authored R3 bullet ends with the
  same words. The duplicate is in the authored text itself; the application
  duplicated nothing and the text went in byte for byte.
- **D3.** Test 10 asserts `str(CONVENTIONS_TOKEN_CAP) not in <module source>`
  instead of the bare literal `"800"`. Identical assertion today, and it keeps
  the number from being restated in the test either.
- **D4.** `remedy` is not invocable on PATH here, so gate J ran through the
  `python3 -c "… from apps.cli.grouped import main …"` form the block spells out.
- **D5.** `.agent/plan.md` is rewritten in this handback commit rather than
  before C1-C3 — the block sequences it at C4, the shape accepted at R1-R3.
- **Deviations, declared: this handoff is 113 lines** (AGENTS.md D15 stated
  cause): four per-commit changed-files tables, the ten-row gate table, three
  authored-text proofs, the item-status table and five deviations. No section
  dropped, nothing restated from git.

## Item status
| Item | Status | Reason |
|---|---|---|
| C1 save the block, both files, cmp | done | ea48ea89; cmp exit 0, no output; oversize declared (D1) |
| C2 record the reviewer gate on R3 | done | 62e7867e; FROM 1x, TO 1x; D2 on one line |
| C3 loaders and their goldens | done | e9b32469; 323 insertions, 21 tests green |
| C4 state, handoff, push | done | this commit; push result in the completion report |

## Open findings
**1** — R-0221 (Low, carried from F103 R5 through F104 and F105 R1-R3; F252
flake-debt class, not this feature's code). No new findings this round. Next free
finding ID **R-0229**. Closure candidates **0 open**. `LAST_REVIEWED_SHA` =
**1a054862**.

## Next
The reviewer gate on R4: read `git diff 1a054862..HEAD` bottom-up and re-run
gates A-J. Then **R5 = F105 T002 part 2** — the distilled
write-discoverable-code block added to BOTH conventions documents as a reviewed
diff, under the cap this round's loader enforces.
