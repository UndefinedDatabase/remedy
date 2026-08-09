# Handoff — F105 Cache-optimal prompt ordering, R1 (claim + candidate sweep)

Feature F105, round **R1**, branch `feature/f105-cache-optimal-prompt-ordering`,
cut from `main` at **cfda4245**. One-session self-drive, one delegated worker.
Review range `cfda4245..HEAD` (HEAD = the commit that writes this file). **No
production code: `packages/`, `apps/`, `tests/`, `README.md`, ROADMAP.md
byte-unchanged.** Nothing merged, no PR created or edited, no force-push, no
worktree.

## Commits

### 5d7b9fce chore(f105): save the R1 claim-and-sweep block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f105-r1-1.md | +253 | the R1 block + authored pairs A-G, verbatim (new) |
| .agent/last_block.md | +233/-87 | same bytes; replaces the F104 R11 block |

### 23e4873f chore(f105): claim F105 and reset the agent state to the new feature
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS.md | +1/-1 | pair A: F105 `[ ]` → `[~]` under Rule A5 |
| .agent/plan.md | +33/-40 | pair D, full file, 42 lines |
| .agent/context.md | +27/-29 | pair E, full file, 43 lines |
| .agent/live_review.md | +16/-245 | pair F, full file, 29 lines; R-0221 carried |

### 1da568ef docs(agents): sweep the F104 closure candidates into the reviewer rules
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +21 | pair B appends 11 lines to §4.4 (`Landed:` vs `Done:`); pair C appends item 13, 10 lines (end-of-branch terminator) |

### f78d1e57 chore(f105): empty the closure-candidate carrier after the sweep
| Path | +/- | Reason |
|---|---|---|
| .agent/candidates.md | +21/-34 | pair G, full file, 33 lines; `**No open candidates.**` 1x |

### (this commit) chore(f105): hand back R1
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this file (template self-reference exception) |

## External actions
`git push -u origin feature/f105-cache-optimal-prompt-ordering` after this
commit; result in the completion report. Nothing else left the repo.

## Verification
Run by me from the repo root, real exit codes, after f78d1e57:

| Gate | Command | Exit | Result |
|---|---|---|---|
| A | `cmp .agent/authored/f105-r1-1.md .agent/last_block.md` | **0** | no output — byte-identical |
| B | `python3 -m pytest tests/docs/ -q` | **0** | 294 passed in 0.25s |
| C | `python3 -m pytest tests/orchestration/test_test_runner.py -q -k "live_review or context_md or plan_md"` | **0** | 4 passed, 47 deselected in 0.13s |
| D | `python3 -m pytest tests/regression/test_resource_safety.py -q` | **0** | 21 passed in 10.99s |
| E | `python3 -m pytest tests/cli/test_golden_path.py -q` (canary) | **0** | 42 passed in 19.39s |
| F | `remedy integrity check --json` via the `apps.cli.grouped:main` entry point | **0** | `"passed": true` (line 3), 0 fails |
| G | `grep -c '\*\*No open candidates\.\*\*' .agent/candidates.md` | **0** | **1** |
| H | `git diff main --numstat -- docs/roadmap/STATUS.md` | **0** | `1 1` — exactly one line |
| I | `git status --porcelain` | **0** | EMPTY (before this commit; re-checked after) |

Extra, not ordered: `pytest tests/ui_server/test_dashboard_contract.py -q -k "not
auto_build"` → **0**, 68 passed — the other `.agent/context.md` reader (§4.11).

## Authored-text proofs
Gate A exit **0**; both files sha256
`641787222d082ea0da10b816e13c8846ebb2df2e61537398ea6f3ce4eedf68f4`. Every pair
was sliced out of `.agent/authored/f105-r1-1.md` on disk, never retyped.
Pair A (rewrite): FROM 1x → 0x, TO 0x → 1x. Pairs B and C (append-shaped): FROM
1x before AND after; TO-ONLY lines 0x before, 1x after — 11 for B, 10 for C.
Pairs D-G (full file): the authored text IS the file, plus one trailing newline.
No trailing whitespace, no tab, no CR anywhere in the authored file.

## Deviations & assumptions — declared
- **D1 (label only, pair C).** Its header says "FROM (3 lines…)" and "then 11
  added lines"; the authored FROM is **2** lines and the addition is **10**. The
  bytes between the FROM and TO markers are unambiguous and I applied them
  verbatim — a 3-line FROM would insert at the same point. Pair B matches.
- **D2.** `remedy` is not invocable on PATH here; gate F ran through
  `python3 -c "… from apps.cli.grouped import main …"`, the entry point
  `pyproject.toml` binds the console script to, exactly as the block orders.
- **D3.** `.agent/plan.md` was reset in 23e4873f, not before 5d7b9fce: the block
  orders the block-save commit to carry its two files alone. Same shape as the
  accepted 04889d8d (F104 R9) and 59037f57 (F104 R11).
- **D4.** The commit-size exemption offered for 5d7b9fce was not needed: 486
  insertions, under the 500 cap. Nothing was waived.
- **This handoff is 107 lines** (AGENTS.md D15 stated cause): five per-commit
  changed-files tables, the nine-row gate table, the pair-shape proofs, the
  item-status table and four declared deviations. No section dropped.

## Item status
| Item | Status | Reason |
|---|---|---|
| C1 save the block | done | 5d7b9fce; cmp exit 0, two files only |
| C2 claim F105 + reset plan/context/live_review | done | 23e4873f; pairs A, D, E, F |
| C3 sweep part 1 (pairs B + C) | done | 1da568ef; planner_reviewer_prompt.md only |
| C4 sweep part 2 (pair G) | done | f78d1e57; candidates.md emptied |
| C5 handoff + push | done | this commit; push result in the completion report |

## Open findings
**1** — R-0221 (Low, carried from F103 R5 through all of F104, F252 flake-debt
class, not this feature's code). Next free ID **R-0229**. Closure candidates:
**0 open** — both F104 entries RESOLVED as reviewer rules in 1da568ef.

## Next
Reviewer confirms `cfda4245..HEAD`, gates R1, then authors **R2 — T001**:
`packages/orchestration/prompt_segments.py` (registry, rank scale, `compose()`,
stable delimiters, manifest) plus `tests/orchestration/test_prompt_segments.py`.
R2 is a SPLIT round — it touches production code.
