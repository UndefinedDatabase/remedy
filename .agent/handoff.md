# Handback — F077 Autonomy watchdog · R8

Branch: `feature/f077-autonomy-watchdog`. No PR exists; none was created.

**This round's green gate proves the ACTION correct in isolation and proves
NOTHING about the loop.** `act_on_trips` has NO call site: `orchestrator_loop.py`
neither imports nor calls `watchdog` (DECISION F077 D8). R9 adds the call site
and pays the four whole-ledger guards in `tests/orchestration/test_mission_e2e.py`.

## Range
Review of `7649a86b..HEAD` (the R7 handback is this round's base, R-0368).

## Commits

### 92199fa9 chore(f077): save the R8 block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f077-r8.md | +224/-0 | the R8 block, saved verbatim (C0) |

### 7195a57c chore(f077): mirror the R8 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +216/-437 | `cp` of the same bytes; second C0 commit as ordered |

### 09977a05 docs(f077): record the R7 verdict, register R-0385 and resolve R-0384
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | FINDING-R385, GATE-R7, DONE-R384 appended (C1) |

### f6a5f115 feat(f077): add the watchdog trip action, unwired
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/watchdog.py | +184/-1 | `act_on_trips`, `TripAction`, the marker, four constants (C2) |

### 1b99e748 test(f077): pin the watchdog trip action
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_watchdog.py | +278/-0 | twelve action tests, three fixtures (C3) |

### 5ba77db0 docs(f077): mirror the R8 state into plan and context
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +22/-16 | R8 Current Step, R9-R11 next, eighteen open, next id R-0386 |
| .agent/context.md | +14/-5 | Scope gains the unwired action; Steps renumbered through R8 |

### \<this commit\> chore(f077): handback R8
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this file (R-0149: a handoff cannot table itself) |

## External actions
`git push -u origin feature/f077-autonomy-watchdog`. No `gh` command, no PR, no
worktree added or removed.

## Verification
1. `git status --porcelain` → EMPTY. `git worktree list` → 1 line.
2. `cmp .agent/authored/f077-r8.md .agent/last_block.md` → exit 0; shared sha256
   `ed8c458f5cda183e7aa36d63a693ba982a01530176d40e6d58bcaf7e0bfecdca`,
   **224 lines** (under the 240 ceiling and the 400 cap).
3. live_review: `^Gate: R7 — PASS` 1, `^- R-0385 — ` 1, `^Done: R-0384 — ` 1,
   `^Landed: R-0384 — ` 1 (the Landed line stayed), `^## Steps` 1.
4. Open set recomputed (`^- R-\d+ — ` paragraphs minus `^Done: R-\d+ — `
   lines): 20 registered, 2 resolved (R-0383, R-0384) → **EIGHTEEN open**:
   R-0361, R-0362, R-0363, R-0364, R-0367, R-0368, R-0369, R-0371, R-0374,
   R-0375, R-0376, R-0377, R-0378, R-0379, R-0380, R-0381, R-0382, R-0385.
   The block predicted seventeen; see Deviations. Reported unadjusted.
5. `git show --numstat 09977a05 -- .agent/live_review.md` → `6  0`. Deletion
   column 0, so nothing above the append moved.
6. `git diff --name-only 7649a86b..HEAD` → the seven committed Change-line
   files (`.agent/handoff.md` is the eighth, in this commit; `.agent/decisions.md`
   was not needed). `git diff --stat 7649a86b..HEAD -- docs/ apps/` → NO OUTPUT.
7. `grep -rn "watchdog" packages/orchestration/orchestrator_loop.py` → **ZERO
   hits**, not the one the block expected. No import, no call: D8 holds.
8. `pytest tests/orchestration/test_watchdog.py -q` → **25 passed** (13
   pre-existing + 12 new). `grep -c "def test_"` → 25.
9. `pytest test_orchestrator_loop.py test_mission_e2e.py test_escalation.py -q`
   → **286 passed** BEFORE C2 and **286 passed** after C3. No regression.
10. `pytest tests/cli/test_golden_path.py -q` → `42 passed` (canary).
11. `pytest test_dashboard_contract.py test_resource_safety.py
    test_test_runner.py -q` → `142 passed`.
12. `ruff check packages/orchestration/watchdog.py
    tests/orchestration/test_watchdog.py` → `All checks passed!`.
13. `python3 -c "import packages.orchestration.watchdog"` → exit 0. No cycle:
    every heavy import sits inside `act_on_trips`.
14. `integrity check --json` → `passed: true`, `fail_count: 0`,
    `check_count: 5`.
15. `wc -l .agent/plan.md` → 48, `grep -c ""` → 48 (equal, newline-terminated);
    `^## Goal` 1, `^## Next Steps` 1. context.md: `## Active Branch` 1,
    `feature/f077-autonomy-watchdog` 1, `Steps` 1, `F077` 7, `resource` 1,
    `pytest` 1.
16. Insertions per commit, measured: 224, 216, 6, 184, 278. None over 500. This
    handback commit cannot quote its own numstat from inside itself (R-0371);
    it rewrites one 161-line file, so its insertions are ≤161 by construction.
17. Trailing-whitespace scan over all eight touched files → none.
18. `test -e .agent/STOP` → ABSENT, checked before the round and again here.

## Authored-text proofs
All three C1 slices were extracted BY SCRIPT (`.remedy-wt/f077_r8_apply_c1.py`,
gitignored) from the COMMITTED `.agent/authored/f077-r8.md` via
`git show HEAD:...` between their own markers, and appended disk-to-disk;
nothing was retyped. FINDING-R385 2136 bytes, GATE-R7 4400, DONE-R384 981, each
one physical line, each present in the target EXACTLY ONCE afterwards, with
zero marker lines leaked. The script refuses to run if a slice is already
present. C2 and C3 are worker-authored code, not authored text.

## Item status
| Item | Status | Reason |
|---|---|---|
| C0 | done | two commits as ordered; `cmp` exit 0 |
| C1 | done | |
| C2 | done | |
| C3 | done | twelve tests, one more than the block's eleven minima |
| C4 | deviated | records EIGHTEEN open, not the block's seventeen (below) |
| C5 | done | this file |

## Deviations & assumptions
- **The open count is EIGHTEEN, not seventeen.** The block's own arithmetic —
  "eighteen minus R-0384, plus R-0385" — is 18. Recomputed mechanically from
  `.agent/live_review.md`: 20 registered, 2 `Done:`, 18 open. Reported
  unadjusted and mirrored as 18 in both state files, per the block's own
  instruction to report what I got.
- **Gate 7 finds zero hits, not one.** The block says "the one pre-existing hit
  is a prose comment mentioning escalation". There is no such hit;
  `orchestrator_loop.py` contains the string `watchdog` nowhere. The property
  the gate exists to prove — no import, no call — holds strictly.
- **DECISION F077 D7 vs. this block's Change line.** D7 closes with "R8 adds
  the watchdog clause in the same commit as the watchdog", but this block's
  Change line names nine files and its Constraints forbid editing
  `mission_state.py` and `mission_cmd.py`. The block was followed and the
  clause is NOT written; the three docstrings stay true-as-of-R7. This is
  flagged, not improvised around — R9 is the natural home, since that is the
  round in which the watchdog gains a caller.
- **One module-docstring sentence was repaired, beyond the ordered paragraph.**
  "Deciding what to DO about a trip … is deliberately NOT here; that is F077
  T002" became false the moment `act_on_trips` landed in this file. Leaving it
  is exactly the R-0384 class. It now says the action is its own section at the
  end of the file. One sentence, no behaviour.
- **`_as_uuid` is imported across a module boundary.** `act_on_trips` calls
  `orchestrator_loop._as_uuid`, a module-private name, because D1 orders the
  attachment to be "exactly as `escalate_repeated_refusal` does". Precedent
  exists (`dod_runners`, `worker_registry`, `mission_compiler` all reach for a
  private of another orchestration module). The alternative — a second
  `_as_uuid` in `watchdog.py` — duplicates a concept the repo wants spelled once.
- **Declared (DECISION D15):** this handback is 161 lines, over the 60-line cap.
  Cause: seven per-commit tables, the eighteen-gate transcript with real values,
  the eighteen named findings, the authored-text proofs, the item-status table
  and the five deviations above. No section dropped.

## Next
1. Phase 1 rule 1 of `docs/agents/self_drive_protocol.md` is the next session's
   FIRST action: re-read `.agent/STOP` from disk, BEFORE rule 2's Open PR Gate.
2. Then rule 2. There is NO open PR for this branch.
3. The next reviewed round is R9 — wire `act_on_trips` into the loop's
   iteration seam, pay the four whole-ledger guards in
   `tests/orchestration/test_mission_e2e.py` (the `numbers == [1..7]` equality,
   the seven-kind move list with its bare `e["move"]["kind"]`, the universal
   `context_digest`/`cost` assertion a zero-cost entry fails, and
   `len(open_at_pause) == 1`), add the loop-integration test, and settle the
   D7 docstring clause deferred above.
4. Eighteen findings are open; the next free id is R-0386. R-0385 is new this
   round and OPEN; R-0384 is resolved.
