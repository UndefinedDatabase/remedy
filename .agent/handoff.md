# Handback — F083 CI self-check · R9 (record R8 FAIL, repair the ruff red, promote checklist item 11)

BLOCKER — why the round ENDS here: `.agent/STOP` APPEARED mid-round. Untracked,
empty, 0 bytes, created 2026-08-15 15:51:12 +0200 — after gate 9 (15:50:56), before
gate 13 (15:52:32). ABSENT at round start. Per G8 and R-0347 the sentinel is NOT
deleted and scope is NOT widened. C0a–C5 were already committed and all 17 gates
already run when it appeared, so nothing is half-applied: this handback is written
as C6 and the round ENDS. Every ordered gate is GREEN, gate 7 included — the red
one this round existed to clear.

## Range
Review of 4406f1c1..HEAD. Branch feature/f083-ci-self-check. C6 is this commit and
cannot table its own SHA (R-0371, R-0149); its SHA, the push result, the post-C6
tree and the PR list go to the operator in the final message.

## Commits
### a5be5330 docs(f083): save the R9 block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f083-r9.md | +250/-0 | C0a — byte copy of the scratchpad original |

### 1f2aae5e chore(f083): mirror the R9 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +163/-313 | C0b — byte-identical mirror; single-`.agent/`-file rewrite, AGENTS.md-exempt |

### 8e6fd0fc docs(f083): record the R8 FAIL and its two findings
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +5/-0 | C1 — RECORD-R8 appended at EOF: gate line, blank line, R-0463, R-0464 |

### f6e23275 docs(f083): shift the round map for the R9 repair round
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-5 | C2 — STEPS rewrite; the map shifts by one, closure moves to R15 |

### 196b8f4f fix(f083): separate the ci_cmd import block from the first def
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/ci_cmd.py | +1/-0 | C3 — BLANK rewrite applied as text; no `ruff --fix`, no formatter |

### bb5b8836 docs(f083): add checklist item 11 on convention paragraphs
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +15/-1 | C4 — OPENER (rewrite) and ITEM11 (append) in ONE commit |

### 5c7c6a7c docs(f083): point the plan at the R9 repair round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +9/-9 | C5 — whole-file PLAN slice |

### C6 — this commit, docs(f083): write the R9 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | this file | C6 — self-reference exception (R-0149) |

## External actions
`git push -u origin feature/f083-ci-self-check` runs AFTER C6; its result postdates
this file (R-0449, R-0452) and goes in the final message. NO PR created. NO worktree
added — `git worktree list` was ONE line throughout. No `gh` write command.

## Verification — every ordered gate, real values, real exit codes
1. `git status --porcelain` EMPTY at round start, exit 0. Pre-C6 it is NOT empty:
   exactly `?? .agent/STOP`, exit 0 — the blocker itself, nothing else, left in place.
   `git worktree list` 1 line throughout. `.agent/STOP` ABSENT at start, PRESENT now.
2. BASE `git rev-parse HEAD` = 4406f1c144e1121d22cc31fec2456fc9d4453865 — EQUALS
   4406f1c1.
3. TRANSPORT: `.remedy-wt/.cache/f083-r9/f083-r9.md`, `.agent/authored/f083-r9.md`
   and `.agent/last_block.md` all = sha256
   322dedf6b5ca6f5f2dde8c45dc939d24088d61920fa12012c67faa76695c58d2, 23438 bytes,
   250 lines. ALL THREE EQUAL True. Measured lines EQUAL the declared footer 250.
4. C1 8e6fd0fc: `pre` prefixes `post` True; `post[len(pre):]` == `b"\n" + RECORD-R8`
   True, the slice extracted by marker from the COMMITTED authored file (sha256
   7edaab77…, 7048 B, 4 lines). numstat `5  0` — deletion column 0.
5. C2 f6e23275: STEPS-FROM 0x, STEPS-TO 1x. `R9 the R8 record` 1,
   `R14 the integration gate` 1, `R13 the integration gate` 0. numstat `6  5`.
6. C3 196b8f4f: BLANK-FROM 0x, BLANK-TO 1x. numstat `1  0`.
7. THE RED GATE IS GREEN. Exact command, repository root, no `--isolated`, no
   substituted flag: `python3 -m ruff check apps/cli/commands/ci_cmd.py
   apps/cli/command_catalog.py apps/cli/commands/__init__.py tests/cli/test_ci_cmd.py`.
   BEFORE C3, run by me on the BASE bytes: `I001 [*] Import block is un-sorted or
   un-formatted --> apps/cli/commands/ci_cmd.py:15:1` / `Found 1 error.` / REAL_EXIT=1.
   AFTER C3: `All checks passed!` / REAL_EXIT=0.
8. C4 bb5b8836, six counts, the two shapes DIFFER: OPENER-FROM 0x after, OPENER-TO 1x
   after (REWRITE); ITEM11-FROM 1x BEFORE and 1x AFTER, ITEM11-TO 0x before, 1x after
   (APPEND). Numerals at C4: `  11. **A convention paragraph` 1, `  10. **The
   open-finding set` 1, `  12. **` 0, `eleven checks mechanically` 1, `ten checks
   mechanically` 0. numstat `15  1`. The gate says "at C3", where those five read
   0 / 1 / 0 / 0 / 1 — see D1.
9. `python3 -m pytest tests/cli/test_ci_cmd.py -q` — 6 passed, REAL_EXIT=0 [BASE 6, 0].
10. Four catalog suites, all four paths confirmed on disk first (R-0438), ONE run —
    601 passed, REAL_EXIT=0. UNMOVED from the 601 at BASE, as R-0464 predicts for a
    round that adds no group.
11. Each run separately, exit code from the process: dashboard contract 70 passed,
    exit 0 [70, 0]; resource safety 21 passed, exit 0 [21, 0]; integrity gate 15
    passed, exit 0 [15, 0]; canary golden path 42 passed, exit 0 [42, 0].
12. NOTHING ELSE MOVED: `git diff --name-only 4406f1c1..HEAD -- packages/ tests/
    apps/cli/command_catalog.py` printed NOTHING — 0 bytes, empty list, exit 0.
13. INTEGRITY GATE (Python; the `remedy` CLI is denied here): `passed` true,
    `fail_count` 0, `check_count` 5. handler_import pass `handlers=338`, equal to BASE,
    this round adding no handler; live_review_verdict pass; plan_consistency pass
    `unchecked=0, context_complete=False`; relevant_untracked pass `untracked=1,
    relevant=0` — that untracked file IS `.agent/STOP`; high_blockers_open pass.
14. OPEN SET at HEAD: registered 92, `Done:` 4, `Landed:` 0, registered-minus-done 88,
    max R-0464, next free R-0465, duplicates NONE. Matches the expected 92 / 4 / 0.
15. C5 PLAN byte-equals the slice as a whole file: sha256
    364eb49935b945adfa4d8626e86fd7180689ca8085690128fdda6574babba28e, 30 lines (< 50),
    `## Goal` present, `## Next Steps` present, `- [ ]` lines 0, numbered items under
    `## Next Steps` 1.
16. CHANGE SET measured BEFORE the handoff, i.e. at C5: SIX paths, not seven (D2) —
    `.agent/authored/f083-r9.md`, `.agent/last_block.md`, `.agent/live_review.md`,
    `.agent/plan.md`, `apps/cli/commands/ci_cmd.py`,
    `docs/agents/planner_reviewer_prompt.md`. The seventh, `.agent/handoff.md`, is
    added by C6 itself. Nothing outside the ordered change set.
17. Insertions (`+` column only): C0a 250 · C0b 163 · C1 5 · C2 6 · C3 1 · C4 15 ·
    C5 9. None over 500. C0b is the AGENTS.md-exempt single-`.agent/`-file rewrite,
    reported anyway. C6's own count cannot exist inside C6 (R-0149) — final message.

## Authored-text proofs
Every slice was extracted BY MARKER from `.agent/authored/f083-r9.md` by a Python
script and applied byte-verbatim — nothing retyped, reflowed or stripped. sha256 /
bytes / lines: RECORD-R8 7edaab77… 7048/4 · STEPS-FROM 1c41e903… 359/5 · STEPS-TO
211e05e4… 440/6 · BLANK-FROM 8d7ba99f… 56/3 · BLANK-TO 5b114ca8… 57/4 · OPENER-FROM
3f678cff… 79/1 · OPENER-TO 4d09ad4c… 82/1 · ITEM11-FROM f3a49657… 76/1 · ITEM11-TO
cd064716… 1175/15 · PLAN 364eb499… 1616/30. Disk-to-disk three-way byte equality of
the authored file is gate 3; `.agent/plan.md` byte-equals PLAN (gate 15).

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | this file; own SHA not self-tabled (R-0149) |
| Gate 1 | deviated | round-start EMPTY; pre-C6 reading is `?? .agent/STOP` — D4 |
| Gate 2 | done | |
| Gate 3 | done | |
| Gate 4 | done | |
| Gate 5 | done | |
| Gate 6 | done | |
| Gate 7 | done | red at BASE (exit 1), green after C3 (exit 0) |
| Gate 8 | deviated | measured at C4; the "at C3" clause is unsatisfiable — D1 |
| Gate 9 | done | |
| Gate 10 | done | |
| Gate 11 | done | |
| Gate 12 | done | |
| Gate 13 | done | |
| Gate 14 | done | |
| Gate 15 | done | |
| Gate 16 | deviated | six paths at C5, not seven — D2 |
| Gate 17 | done | |

## Deviations & assumptions
- D4, the blocker. `.agent/STOP` appeared mid-round and is PRESENT at handback. Not
  deleted (R-0347), not routed around (G8). No work was interrupted: C0a–C5 and all 17
  gates predate the halt. The round's substance is complete; the ROUND is ended by the
  sentinel, not by a red gate.
- D1. Gate 8's clause "Then over the file at C3, the numerals and the enumeration must
  agree" is UNSATISFIABLE at C3: four of its five anchors are created by C4 itself, so
  at C3 they read 0 / 1 / 0 / 0 / 1. I did not repair the block; I measured BOTH
  commits and report both. The property holds at C4, the commit that lands the edit.
  R-0371 class.
- D2. Gate 16 orders the change set "measured BEFORE the handoff is written into C6, so
  it lists seven paths with `.agent/handoff.md` the seventh and last". Both clauses
  cannot hold: measured before C6 the list is SIX, and the seventh path is created by
  the commit the measurement must precede. I report the measured six and name the
  seventh's origin. Same R-0371 family as D1.
- D3. Inside RECORD-R8, finding R-0463 states "C3 lands item 11 and nothing else",
  while the block's own bundle assigns item 11 to C4 and the ruff repair to C3. I
  applied the slice BYTE-VERBATIM per constraint 2 and did not silently repair it. On
  disk item 11 landed in C4 (bb5b8836); C3 (196b8f4f) is the one-line ruff repair.
- D5. Cap overage, DECISION D15 stated cause, naming BOTH caps (R-0462): this file
  exceeds the ≤100-line cap for a >5-commit bundle AND the ≤800-token hard cap. Cause
  is mandated content only — eight per-commit tables, a value for each of 17 gates, a
  25-row item-status table, the authored-text proofs and the blocker paragraph the
  halt requires. No section dropped; no prose padding.
- No assumption_log entry was needed: no ambiguity was resolved by guessing.

## Open findings
Registered 92, Done 4, Landed 0, OPEN 88. Max id R-0464, next free R-0465, no
duplicate. R-0463 (Medium, blind dry run) and R-0464 (Low, parametrised baseline)
were registered this round and are OPEN; both are charged to the reviewer.

## Next
R10 exactly as `.agent/plan.md` now states it: add the per-stage selection tests over
a fixture tree that pin each stage's marker expression against files whose markers are
known, and promote R-0463's dry-run rule into §3 as checklist item 12. R10 must not
start before the operator clears `.agent/STOP`.

Fortschritt: 34 % (F083 beansprucht · R1 bis R7 PASS, R8 FAIL auf einem roten ruff-Gate und hier repariert · Stage-Tabelle, Stage-Runner und die `remedy ci` CLI-Naht als Code gelandet, mit einem Test der wirklich einen Stage-Argv durch den Runner startet · noch keine hosted workflows, keine Determinismus- oder Budget-Stage) — gemessen, nicht geschätzt
