# Handback — F032 R9 (T002d, the stop-reason card, and the session's close)

## Session

SESSION 2 of feature F032 · round R9 · rounds so far 9

SESSION 2 ENDS HERE. It delegated four rounds, R6 through R9; session 1 was
R1 through R5. Nine rounds across two sessions is inside the soft limit of 25
rounds or 7 sessions, so no limit report is owed.

## Range

Review of `c23e7cc6` (round base) .. C5 `9aa51005`, plus C6, which is the
commit writing this file and cannot table itself.

## Commits

### 3dee8a49 docs(agent): save the F032 R9 step block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f032-r9.md | +350 / -0 | C0a, the block saved byte for byte from `.remedy-wt/f032-r9.md` |

### 80e3c96f docs(agent): mirror the R9 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +192 / -198 | C0b, the mirror; same git blob as C0a |

### de45b9e0 docs(agent): point the plan at R9 and the stop-reason producer
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +21 / -19 | C1, slice PLANF032R9 |

### 298f25ce docs(agent): book the R8 verdict and register R-0713
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +4 / -0 | C2, slice LEDGER9 appended; `F032 R8` gate key and `R-0713` |

### f0ec4b09 fix(orchestration): the patch card shows its placeholder again
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/decision_queue.py | +9 / -1 | C3, the `R-0713` fix (S2) |

### e26e95e0 feat(orchestration): the stop-reason card cites its own record
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/decision_evidence.py | +1 / -1 | C4, `stop_reason` joins `TRIPLE_REQUIRED_TYPES` (S5) |
| packages/orchestration/decision_queue.py | +53 / -0 | C4, the stop-reason refs and the unkeyed outcome (S3, S4) |

### 9aa51005 test(orchestration): pin the stop-reason triple and the patch placeholder
| Path | +/- | Reason |
|------|-----|--------|
| tests/orchestration/test_decision_evidence.py | +176 / -2 | C5, S6 |

### C6 docs(agent): hand back F032 R9 and close session 2
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | self | C6 cannot table its own numstat (R-0149) |

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | |
| C0b mirror it into `last_block` | done | |
| C1 the plan | done | |
| C2 the R8 verdict and `R-0713` | done | |
| C3 the `R-0713` fix | done | |
| C4 the stop-reason triple and the gate set | done | |
| C5 its tests | done | |
| C6 the session-closing handback | done | this commit |
| push | done | reported to the operator only; see `## External actions` |
| S1 read the branch and the measured record first | done | branch, `StopReason` and `derive_stop_reasons` read before writing |
| S2 the `R-0713` fix, one line | done | uses `_pa_target_path or '?'` |
| S3 the refs come from the stop record | done | id always, reason code and related file guarded |
| S4 the outcome is unkeyed | done | one outcome keyed `UNKEYED_OPTION`, no `payload` added |
| S5 `stop_reason` joins the gate set | done | same commit as its triple, C4 |
| S6 the tests | done | 63 tests in the file, up from 55 |

## External actions

- `git worktree add --detach .remedy-wt/f032-r9-mut 9aa51005` — exit 0, used for
  the two G7 mutation red-proofs only.
- `git worktree remove .remedy-wt/f032-r9-mut` then `git worktree prune` — both
  exit 0; `git worktree list` back to 1 line.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` —
  exit 0, output `[]`. Nothing merged, nothing created.
- `git push origin feature/f032-evidence-triple` — INTENT, run after this
  commit. Its exit code and the resulting remote tip are not values any file
  this round writes and are reported in the round report instead.

## Verification

- G1 hygiene, base and sentinel — `git rev-parse HEAD` before C0a
  `c23e7cc633fb2adf8b6dce5b1c576a8440055e52`, the round base; branch
  `feature/f032-evidence-triple`; `git status --porcelain` 0 lines after each of
  C0a..C6; `.agent/STOP` ABSENT at both readings. Exit 0.
- G2 transport — sha256
  `80008f17ccd928a18b9530814ab7d805688e53eea89144e5f2ea0a2b6a933a33`, 29489
  bytes, 350 lines, EQUAL across the scratch original, the committed
  `.agent/authored/f032-r9.md` blob and the committed `.agent/last_block.md`
  blob; both paths are the SAME git blob `31ca746bb33c`. This proves the
  scratch original, the saved copy and the mirror agree; it says NOTHING about
  the bytes of any prompt. Exit 0.
- G3 extraction and caps — 2 regions from the committed C0a blob, PLANF032R9 48
  content lines and LEDGER9 3; CONTENT 51, TOTAL 350, PROSE 299; PROSE under
  400 TRUE, TOTAL under 490 TRUE. Exit 0.
- G4 the plan — byte-equal to PLANF032R9 TRUE, minus-trailing-newline negative
  control FALSE, `wc -l` 48 and under 50, `^## Goal$` 1, `^## Next Steps$` 1.
  Exit 0.
- G5 the ledger append — 1065424 + 1 + 6286 = 1071711, matching the file; the
  pre-commit blob is a byte PREFIX. Second reader: N 2 paragraphs, the last 2
  blank-line units EQUAL IN ORDER; one byte flipped inside the FIRST appended
  paragraph was REJECTED by both readers, in memory only. Counts before → after
  C2: `^Gate: F\d+ R\d+ — ` 60 → 61, `^- R-\d+ — ` 273 → 274,
  `^Done: R-\d+ — ` 23 → 23, `^Landed: R-` 1 → 1, `^Gate: R\d+ — ` 19 → 19;
  open set 250 → 251, maximum id `R-0712` → `R-0713`; ADDED gate keys
  `{F032 R8}`, ADDED ids `{R-0713}`. Exit 0.
- G6 the code, linted and read back — `python3 -m ruff check` over both modules
  exit 0, output verbatim `All checks passed!`. `list_decisions` read back:
  patch intent naming no file → `'Patch intent for ? awaits approval.'`,
  naming `README.md` → `'Patch intent for README.md awaits approval.'`. Stop
  reason with EMPTY `related_file`: id `'sr:derived_no_repo'`, payload `{}`,
  refs `('failure', 'derived_no_repo', 'the stop record that raised this
  decision')` and `('failure', 'no_target_repo', 'the reason code the run
  recorded')`, ONE outcome `('', 'Clearing the named blocker lets the run
  continue from where it stopped, with the work already done still in place.',
  'Until it is cleared the run makes no further progress, and a blocker cleared
  without understanding why it fired can fire again.')`, `evidence_status`
  `'present'`. Stop reason naming a file: same shape plus
  `('file', 'packages/core/models.py', 'the file this stop is about')`.
  `TRIPLE_REQUIRED_TYPES` = `patch_approval`, `stop_reason`, `test_failure`,
  `token_budget`. Exit 0.
- G7 tests green, then red under mutation, guards unmoved —
  `python3 -m pytest tests/orchestration/test_decision_evidence.py -q` in the
  primary checkout exit 0, `63 passed in 0.30s`. In the disposable worktree at
  C5: CONTROL exit 0 `63 passed in 0.29s`; mutation (a), the `R-0713` fix
  reverted to `pi.get('target_path', '?')` (exact bytes counted 1 before
  applying), exit 1 `1 failed, 62 passed in 0.31s`, 1 `^FAILED` line; mutation
  (b), the `related_file` ref made unconditional (exact two-line string counted
  1 before applying), exit 1 `4 failed, 59 passed in 0.37s`, 4 `^FAILED`
  lines; CONTROL after both restorations exit 0 `63 passed in 0.29s` with the
  worktree's `git status --porcelain` empty. `__pycache__` purged and `-B`
  passed before every run. The nine decision-schema guard files as ONE pytest
  process: exit 0, `324 passed in 6.87s`, `^FAILED` count 0, the extractor
  sighted on a two-line probe string and returned 2.
- G8 structure, canary, PR gate — `tests/cli/test_golden_path.py -q` exit 0,
  `42 passed in 20.97s`. Path set of `git diff --name-only c23e7cc6..9aa51005`
  against the expected seven-path set: BOTH residues EMPTY.
  `git diff --stat c23e7cc6..9aa51005 -- apps/` EMPTY, `-- docs/` EMPTY.
  Insertions 350, 192, 21, 4, 9, 54 and 176 across C0a..C5, each single-parent
  and under 500. `^<<<SLICE ` and `^<<<END ` are 0 and 0 in `.agent/plan.md`,
  `.agent/live_review.md`, `packages/orchestration/decision_queue.py`,
  `packages/orchestration/decision_evidence.py` and
  `tests/orchestration/test_decision_evidence.py`, against a CONTROL of 2 and 2
  over the C0a blob. `git ls-files .remedy-wt` 0 lines, `git worktree list` 1
  line, `git branch --list "tmp/*"` 0 lines. Open PR Gate `[]`.

## Authored-text proofs

- PLANF032R9 — extracted from the COMMITTED `.agent/authored/f032-r9.md` blob
  and compared disk to disk against `.agent/plan.md` at C1: byte-equal TRUE,
  negative control FALSE.
- LEDGER9 — extracted from the same committed blob; `.agent/live_review.md` at
  C2 equals its pre-commit blob plus one newline plus the slice, byte for byte,
  confirmed twice by two independent readers.
- The block itself — `.remedy-wt/f032-r9.md`, `.agent/authored/f032-r9.md` and
  `.agent/last_block.md` all sha256
  `80008f17ccd928a18b9530814ab7d805688e53eea89144e5f2ea0a2b6a933a33`.

## Deviations & assumptions

- NO DEPARTURE FROM THE ORDERED COMMIT SEQUENCE. The commits are exactly C0a,
  C0b, C1, C2, C3, C4, C5, C6 in that order, with no extra commit, no dropped
  commit and no reordering. No commit was made beyond the ordered sequence, so
  no extra `## Commits` row and no extra item-status row is owed.
- No slice contradicted anything measured. Every numeral the block stated about
  the round base reproduced exactly at `c23e7cc633fb`: 1065424 ledger bytes,
  423 blank-line units, 60/273/23/1/19, open set 250, maximum `R-0712`,
  `All checks passed!` at ruff exit 0, `324 passed`, `42 passed` and `[]` at
  the Open PR Gate.
- ASSUMPTION, declared because it is the one design choice S6 left open: no arm
  of `derive_stop_reasons` sets `related_file`, so the related-file case is
  driven by substituting `stop_reasons.derive_stop_reasons` for the duration of
  the test — the same technique the memory-review tests in this file already
  use for `local_gateway.list_memory`. The branch under test is still the
  queue's real one, reached through `list_decisions`.
- The `R-0713` fix carries an eight-line WHY comment above the changed line, so
  C3's insertion count is 9 rather than 1. The changed expression is one line.
- No new finding was authored. Nothing this round exposed looked like a defect
  the reviewer has not already registered.

## Gate enforcement after this round

The emit gate enforces FOUR of the eight producing decision types:
`token_budget`, `test_failure`, `patch_approval` and `stop_reason`. A card of
any of those four that is built without a valid triple now RAISES
`DecisionEvidenceError` at derivation.

The remaining FOUR still carry the honest legacy placeholder
`recorded_before_evidence_requirements`: `repo_dirty`, `memory_review`,
`flight_plan_approval` and `task_decision`.

`R-0713` is FIXED IN CODE at C3 but remains OPEN in the record until a reviewer
authors its `Done:` text. Open findings after this round: 251.

## Next

1. Re-read `.agent/STOP` from disk — Phase 1 rule 1 of
   `docs/agents/self_drive_protocol.md` — before anything else.
2. Then the Open PR Gate: `gh pr list --state open --json
   number,headRefName,baseRefName,isDraft`.
3. Then the remaining T002 producers: `repo_dirty`, `memory_review`,
   `flight_plan_approval` and `task_decision`. Repo-dirty's event carries the
   thinnest evidence of the eight; the flight plan has two arms and only one
   offers options, so enforcing that type needs a ruling on what a RESOLVED
   decision owes. Along the way, author `Done: R-0713` against the fix this
   round landed.
