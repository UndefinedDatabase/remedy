# Handback — F085 Sandbox hardening, R71 (the defeated no-shell test, repaired)

Branch: feature/f085-sandbox-hardening. Base SHA: 6a04b37b. HEAD: 2eb5d1f3 + this commit.
Outcome: the R70 BLOCKER is repaired in the TEST only; both of its assertions proved reachable by
mutation. No file under `packages/` or `apps/` touched. All nine gates ran; one reported mismatch
against the BLOCK's own arithmetic is declared below and was NOT fixed.

## Range
Review of 6a04b37b..HEAD — seven commits: C0a C0b C1 C2 C3 C4 C5.

## Commits

### 89f82709 chore(f085): save the R71 step block  (C0a)
| Path | +/- | Reason |
| `.agent/authored/f085-r71.md` | +408/-0 | block saved byte-verbatim from transport |

### a4bee9fc chore(f085): mirror the R71 block into last_block  (C0b)
| Path | +/- | Reason |
| `.agent/last_block.md` | +334/-234 | mirror of the same bytes |

### 17df8755 docs(f085): advance the plan to the R71 repair round  (C1)
| Path | +/- | Reason |
| `.agent/plan.md` | +9/-7 | PLAN25F→PLAN25T applied |

### ea9e80b5 docs(f085): register R-0564 and R-0565 and record the R70 PASS  (C2)
| Path | +/- | Reason |
| `.agent/live_review.md` | +65/-0 | RECORD40 appended at EOF |

### 3cf6788e test(f085): follow the no-shell test to the guard spawn seam  (C3)
| Path | +/- | Reason |
| `tests/test_command_discovery.py` | +25/-9 | NOSHELLF→NOSHELLT, one method body only |

### 2eb5d1f3 docs(f085): record R-0564 as landed  (C4)
| Path | +/- | Reason |
| `.agent/live_review.md` | +4/-0 | NOSHELLLANDED appended at EOF |

### C5 handback (self-referential, R-0149 pattern)
| Path | +/- | Reason |
| `.agent/handoff.md` | rewrite | this file; a handoff cannot table its own commit |

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

## External actions
`git worktree add --detach .remedy-wt/redctl-r71 HEAD` → ok. `git worktree remove --force
.remedy-wt/redctl-r71` → ok. `git push -u origin feature/f085-sandbox-hardening` after this commit.
No PR, no merge, no force-push, no history rewrite.

## Verification
- **G1 STATE.** `.agent/STOP` ABSENT before C0a and again before C5. `git status --porcelain` EMPTY
  at round start, after every commit, and after G8. `git worktree list` one line at start and end.
- **G2 TRANSPORT.** Five copies byte-EQUAL — transport, committed+working `.agent/authored/
  f085-r71.md`, committed+working `.agent/last_block.md`: sha256 9c87a93b…1ba630, 29863 B, 408
  lines, 12 marker lines each. TOTAL 408 ≤ 490 · PROSE 255 ≤ 400 · RECORD40 65 ≤ 140.
- **G3 SHAPES.** PLAN25F→PLAN25T @17df8755 `.agent/plan.md`: TO contains FROM False, FROM 1x pre /
  0x post, TO 1x post, re-apply reproduces the post-commit blob BYTE-EXACTLY, numstat 9/7.
  RECORD40 @ea9e80b5 `.agent/live_review.md`: PREFIX True, SUFFIX True, `pre+slice==post` True,
  ADDED 65 == slice 65 IN ORDER, numstat 65/0. NOSHELLF→NOSHELLT @3cf6788e
  `tests/test_command_discovery.py`: TO contains FROM False, FROM 1x pre / 0x post, TO 1x post,
  re-apply BYTE-EXACT, numstat 25/9. NOSHELLLANDED @2eb5d1f3, measured against C4's OWN pre-commit
  blob: PREFIX True, SUFFIX True, `pre+slice==post` True, ADDED 4 == slice 4 IN ORDER, numstat 4/0.
  Marker LINES (`^(BEGIN|END)-[A-Z0-9]+$`) = 0 in every edited file post-commit.
- **G4 SUITES**, primary checkout, SERIAL, one pytest at a time. `tests/test_command_discovery.py
  -q -rf`: base 6a04b37b re-measured by me → **exit 1**, `1 failed, 91 passed`, `assert
  mock_run.called`; at HEAD → **exit 0**, `92 passed in 6.67s`. Same file `-k TestNoShellTrue` →
  **exit 0**, `2 passed, 90 deselected` (2 selected, 2 passed). `tests/orchestration/
  test_exec_guard.py` → **exit 0**, `44 passed`. `test_test_runner.py test_resource_safety.py
  test_integrity_gate.py test_dashboard_contract.py` → **exit 0**, `160 passed`. CANARY
  `tests/cli/test_golden_path.py -q` → **exit 0**, `42 passed`.
- **G5 PLAN CONTRACT.** `.agent/plan.md` after C1: **39 lines** ≤ 50; `## Goal` True; `## Next
  Steps` True; `\bF\d{3}\b` True.
- **G6 ARITHMETIC.** 6a04b37b: 178 registered / 31 done / 0 landed, 147 open, max registered
  R-0563, max resolved R-0563, 0 duplicate ids, 0 orphan resolutions. HEAD: 180 / 31 / 1, max
  registered R-0565, max resolved R-0563, 0 duplicates, 0 orphans. Symmetric differences —
  registered EXACTLY {R-0564, R-0565}, landed EXACTLY {R-0564}, done EMPTY. Next free id R-0566.
  Open count: 149 by registered−done; see Deviations 2.
- **G7 LINT**, repo config, from the root. `ruff check tests/test_command_discovery.py` → **exit
  0**, `All checks passed!`. `ruff check --preview tests/test_command_discovery.py` → **exit 0**,
  `All checks passed!`.
- **G8 RED CONTROLS**, in `.remedy-wt/redctl-r71` only, never committed. (i) three-line anchor count
  1; `shell=True,` inserted in `packages/orchestration/exec_guard.py`; `pytest
  tests/test_command_discovery.py -q -rf -k no_shell_true` → **exit 1**, `1 failed`, on `assert not
  call_kwargs.get("shell", False)` with `'shell': True` in the recorded kwargs. REVERTED, worktree
  `git status --porcelain` empty. (ii) five-line anchor count 1; the `run_guarded_test_command(`
  call replaced by `subprocess.CompletedProcess(argv, 0, b"", b"")`; same command → **exit 1**,
  `1 failed`, on `assert spawns` with `assert []`. Both live assertions reachable.
- **G9 HYGIENE**, before C5. `git diff --name-only 6a04b37b..HEAD` = 5 paths: `.agent/authored/
  f085-r71.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
  `tests/test_command_discovery.py`. NONE under `packages/`, `apps/`, `docs/` or `scripts/`;
  exactly one under `tests/`. Insertions: 89f82709 408, a4bee9fc 334, 17df8755 9, ea9e80b5 65,
  3cf6788e 25, 2eb5d1f3 4 — none over 500. Every commit single-parent. No oversize commit.

## Authored-text proofs
All six slices were extracted PROGRAMMATICALLY from the committed `.agent/authored/f085-r71.md` by
marker pair under the block's CONVENTION; none was retyped, reflowed, or taken from the prompt, and
no marker line reached a target file. The disk-to-disk comparison is G2's five-way byte equality
(one digest, no fallback) plus G3's per-pair byte-exact re-apply and ordered-equality readings.

## Deviations & assumptions
1. **Bundle order.** No extra commit, no dropped commit, no reordering: C0a C0b C1 C2 C3 C4 C5
   exactly as ordered.
2. **REPORTED MISMATCH against the block, not fixed** (constraints 8 and 10). G6 and constraint 9
   order "open moves 147 → 148"; my reading at HEAD is **149**. Both formulas give the base 147
   because landed was 0 there: registered−done = 180−31 = **149**; registered−done−landed = 148.
   `docs/agents/planner_reviewer_prompt.md` §4 item 4 rules that a `Landed:` line is NOT a
   resolution — "a surviving `Landed:` line is an unreviewed fix" — and RECORD40 itself writes
   "OPEN." for R-0564, so R-0564 is still open and 149 is the reading consistent with both. Every
   other G6 clause matched exactly. No ledger text was edited to reconcile this; the reviewer rules.
3. **No ledger text authored** beyond the NOSHELLLANDED slice applied verbatim in C4: no `Done:`
   paragraph, RECORD40 unedited. No other disagreement with RECORD40 was found.
4. **Scope.** `packages/` and `apps/` untouched; no test deleted, skipped, xfailed or renamed; only
   the NOSHELLF bytes changed in `tests/test_command_discovery.py`.
5. **Handoff overage, declared.** 140 lines against the ≤100 cap that >5-commit tables allow
   (AGENTS.md DECISION D15, stated cause). Cause: the mandated per-commit tables for seven commits,
   the item-status table, the transport and pair proofs, and nine gates' real numbers including
   G3's four separate shape readings and G8's two controls. No section was dropped.

Fortschritt: ~100 % der Bauarbeit; das Integration Gate lief und hat GENAU EINEN echten Regress
gefunden — ein Test, der die alte Spawn-Stelle festnagelte, wurde durch die Migration entwertet und
ist hier auf die neue Naht nachgezogen, mit zwei Rot-Kontrollen. R70 PASS. Offen bleiben der zweite
Gate-Lauf und die Closure. Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

## Next
ONE: R72 re-runs the INTEGRATION GATE per docs/agents/integration_gate.md, because a repair landed
after a gate invalidates that gate's comparison; closure per
docs/roadmap/STATUS_closure_protocol.md follows it.
TWO: R71 carries no verdict of its own, because the round that records a verdict cannot record one
on itself (docs/agents/planner_reviewer_prompt.md §4 item 13); R72 carries it, and R72 also writes
the reviewer-authored `Done: R-0564` that replaces this round's `Landed:` line.
THREE: open findings 149 by registered−done (148 under the block's landed-subtracting reading, see
Deviations 2); next free id R-0566.
FOUR: Phase 1 rule 1 first: re-read `.agent/STOP` from disk.
