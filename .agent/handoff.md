# Handoff — F032 R4, the emit gate, legacy rendering and the canary

## Session

`SESSION 1 of feature F032 · round R4 · rounds so far 4`

Feature F032, round R4. Branch `feature/f032-evidence-triple`. Round base
`4316e7f5` (`4316e7f5d5dd272d1d1b4456879850a2ca0cea04`), the tip R3 handed back.
Soft limit 25 rounds / 7 sessions — not approached.

THIS ROUND EDITED PRODUCTION CODE IN A WIDELY-DEPENDED-ON MODULE:
`packages/orchestration/decision_queue.py` gained one optional `HumanDecision`
field, three `export_decision_json` keys and the emit-gate call in
`list_decisions`, and `packages/orchestration/decision_evidence.py` gained the
two status literals, `TRIPLE_REQUIRED_TYPES` (EMPTY), `DecisionEvidenceError`
and `enforce_decision_evidence`. NO EXISTING TEST FILE WAS EDITED. Nothing
under `apps/` was written. `R-0710`'s code fix landed at C4; the finding record
was NOT written. No pull request was created and nothing was merged.

## Range

Review of `4316e7f5..HEAD`.

## Commits

### 87ec1e6e chore(agent): save the F032 R4 block as authored text
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f032-r4.md` | +415/-0 | C0a, the block copied byte for byte from `.remedy-wt/f032-r4.md` |

### cb47f124 chore(agent): mirror the F032 R4 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +317/-308 | C0b, the mirror; same git blob as C0a |

### 28f5b3fb chore(agent): set the plan to F032 R4, the emit gate round
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +21/-21 | C1, whole-file replacement by slice PLANF032R4 |

### ffb4e4f2 docs(agent): record DECISION F032 D5, the per-card marker and opt-in enforcement
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/decisions.md` | +53/-0 | C2, append of slice DEC5 |

### 17715d8f docs(roadmap): add F032 design amendment A5, the per-card legacy marker
| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/features/T5_F032.md` | +16/-0 | C3, append of slice FEATA5 |

### e45b5026 feat(orchestration): wire the evidence triple into the decision queue emit point
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/decision_evidence.py` | +74/-2 | S1–S4: the two status literals, the empty required-type set, the error and the enforcement function |
| `packages/orchestration/decision_queue.py` | +49/-2 | S5–S9: the `evidence` field, three export keys, the emit-gate call, and `R-0710`'s predicate fix |

### b028628c test(orchestration): pin the emit gate, the canary and the memory-review predicate
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_decision_evidence.py` | +192/-0 | S10: the safety property, the canary, the two export cases and the two memory-branch tests |

### C6 (this commit) docs(agent): hand back F032 R4
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | self | a handoff cannot table the commit that writes it (`R-0149`) |

## External actions

- `git worktree add .remedy-wt/f032r4-mut b028628c --detach` — exit 0, created for G6.
- `git worktree remove .remedy-wt/f032r4-mut` — exit 0; `git worktree prune` — exit 0.
  `git worktree list` reads 1 line afterwards.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — output
  `[]`. Nothing merged, nothing created.
- INTENT after this commit: `git push origin feature/f032-evidence-triple`. Its
  outcome is not a value of any file this round writes, so no exit code and no
  remote tip is stated here; both are in the round's completion report.

## Verification

- G1 hygiene and the sentinel — real exit 0. `git rev-parse HEAD` before C0a
  `4316e7f5d5dd272d1d1b4456879850a2ca0cea04`; branch `feature/f032-evidence-triple`;
  `git status --porcelain` 0 lines after each of C0a…C6; `.agent/STOP` ABSENT
  before C0a and again before C6.
- G2 transport — real exit 0. sha256
  `5c720abd6f15d426b41bea8b5b79099fcd59fe703d4ffe4e377375621ebc9436`, 27497 bytes,
  415 lines at all FOUR points (scratch, C0a, C0b, disk at C5); C0a and C0b are the
  SAME git blob `3519e4e4c9017b0b0c94fb3da83f1a20975f6f17`; repeated-character runs
  of length ≥ 4: none.
- G3 extraction and caps — real exit 0. 3 slices from the committed C0a blob:
  PLANF032R4 45, DEC5 52, FEATA5 15; CONTENT 112, TOTAL 415, PROSE 303 (≤ 400),
  TOTAL ≤ 490.
- G4 the prose writes and the docs gate — real exit 0.
  `python3 -m pytest tests/docs/ tests/orchestration/test_roadmap_index.py -q`
  → `325 passed in 0.70s`. Plan byte-equal TRUE, negative control FALSE, `^## Goal$` 1,
  `^## Next Steps$` 1, `\bF\d{3}\b` matched `F032`, 45 lines. Appends: 636058 + 1 + 3411
  = 639470 and 8225 + 1 + 1138 = 9364, both byte-prefix TRUE. `^## DECISION F032 D\d+ `
  4 → 5 with `## DECISION F032 D5` added; `^## Design amendments$` still 1.
- G5 the code, linted and read back by import — real exit 0.
  `python3 -m ruff check` over both files → `All checks passed!`. Import readback:
  `present`, `recorded_before_evidence_requirements`, `TRIPLE_REQUIRED_TYPES`
  `frozenset()` (EMPTY), `DecisionEvidenceError` a `ValueError` subclass,
  `HumanDecision` last field `evidence` with default `None`, and a no-`evidence`
  export carrying `evidence_status` `recorded_before_evidence_requirements`.
- G6 the tests, green then red under mutation — real exit 0 in the primary
  checkout (`24 passed in 0.29s`) and real exit 0 for the worktree CONTROL
  (`24 passed in 0.28s`). All three mutations went RED at real exit 1 with
  `1 failed, 23 passed`; none left the suite green. Worktree removed and pruned.
- G7 the guards the schema change could move — real exit 0,
  `324 passed in 7.22s`, `^FAILED` count 0 (extractor sighted on a known
  one-FAILED string → 1). No test file was edited.
- G8 structure, artifacts, state readers, Open PR Gate — real exit 0,
  `620 passed in 74.04s (0:01:14)`, `^FAILED` count 0. Path-set residues EMPTY
  both ways; `apps/` diff EMPTY; every commit single-parent and under 500
  insertions; `^<<<SLICE `/`^<<<END ` 0/0 in every written file against a
  CONTROL of 3/3 over the C0a blob; `git ls-files .remedy-wt` 0 lines,
  `git worktree list` 1 line, `git branch --list "tmp/*"` 0 lines;
  `gh pr list` → `[]`.

## Authored-text proofs

`.agent/authored/f032-r4.md` was written with `shutil.copyfile` from
`.remedy-wt/f032-r4.md` and read back at sha256
`5c720abd6f15d426b41bea8b5b79099fcd59fe703d4ffe4e377375621ebc9436` / 27497 bytes /
415 lines, equal to the scratch file, to the C0b mirror (identical git blob) and
to the working copy re-read at C5. `.agent/plan.md` is byte-equal to slice
PLANF032R4 with the negative control FALSE; `.agent/decisions.md` and
`docs/roadmap/features/T5_F032.md` each equal their own pre-commit blob plus one
newline plus their slice, byte-prefix reading TRUE for both.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block | done | |
| C0b mirror into `last_block` | done | |
| C1 the plan | done | |
| C2 DECISION F032 D5 | done | |
| C3 the feature file amendment A5 | done | |
| C4 the wiring and `R-0710`'s fix | done | |
| C5 the tests, including the canary | done | |
| C6 the handback | done | this commit |
| push | done | stated as intent above; outcome in the completion report |
| S1 status literals | done | |
| S2 `TRIPLE_REQUIRED_TYPES`, empty | done | |
| S3 `DecisionEvidenceError` and `enforce_decision_evidence` | done | |
| S4 the raise-not-drop docstring | done | |
| S5 `HumanDecision.evidence` after `payload`, default `None` | done | |
| S6 three export keys, none dropped | done | |
| S7 the emit-gate call in `list_decisions` | done | |
| S8 one-way import direction | done | `decision_evidence` still imports nothing from `decision_queue` |
| S9 `R-0710`'s predicate fix | done | |
| S10 the tests and the canary | deviated | six ordered tests plus two the order did not name — see Deviations |

## Deviations & assumptions

1. `R-0710`'s FIX: `packages/orchestration/decision_queue.py` now selects the
   memory-review cards with `e.validity == "stale" or e.review_status ==
   "needs_review"`, with a WHY comment naming both fields, at commit `e45b5026`
   (C4), pinned by two tests at `b028628c` (C5). Nothing was written into
   `.agent/live_review.md`: no id was minted and no `Done:` line was authored.
2. MUTATION (i), `enforce_decision_evidence` never raises: RED, real exit 1,
   `1 failed, 23 passed in 0.27s`, one `^FAILED` line
   (`test_the_canary_producer_missing_a_field_is_refused`).
3. MUTATION (ii), `export_decision_json` reports PRESENT when `evidence` is
   `None`: RED, real exit 1, `1 failed, 23 passed in 0.27s`, one `^FAILED` line
   (`test_a_tripleless_decision_exports_empty_lists_and_the_legacy_status`).
4. MUTATION (iii), S9 reverted to `e.validity in ("stale", "needs_review")`:
   RED, real exit 1, `1 failed, 23 passed in 0.27s`, one `^FAILED` line
   (`test_a_needs_review_memory_card_raises_a_memory_review_decision`).
   NO MUTATION LEFT THE SUITE GREEN.
5. S10 additions beyond the six tests the order names: a test that the SHIPPED
   `TRIPLE_REQUIRED_TYPES` is `frozenset()`, and a test that an enforced
   OPTIONLESS decision reads no `options` from its payload — the DECISION F032 D3
   six-branch case S3 names but no ordered test covered. Both are additive; no
   ordered test was dropped.
6. The `decision_evidence.py` module docstring said the emit gate "lives at the
   derivation point, not here". `enforce_decision_evidence` now lives HERE and
   is CALLED there, so that sentence would have landed false. It was narrowed to
   say the gate's CALL SITE is `decision_queue.list_decisions` and that this
   module never reaches back into the queue. One paragraph, in a file this round
   edits anyway; declared rather than left contradicting the code.
7. OBSERVATION, not repaired: the memory branch's `safe_summary` still reads
   `f"Memory '{me.key}' is {me.validity}."`, so a card selected by the NEW half
   of the predicate renders as "is active". The order specified the predicate
   and its WHY comment only, so the summary was left alone rather than widened
   into a `while I am here` edit. The local variable is still named `stale` for
   the same reason.
8. No commit was made beyond the ordered sequence C0a, C0b, C1, C2, C3, C4, C5,
   C6, and none was dropped or reordered.

## Open findings

250 open after this round, unchanged: 271 finding paragraphs minus 21 `^Done:`
lines, maximum id `R-0710`. No id was minted and none was resolved — `R-0710`'s
CODE is fixed but its RECORD is the reviewer's to write.

## Next

The reviewer reviews `4316e7f5..HEAD`, books R3's verdict and R4's, writes
`R-0710`'s `Done:` text if it agrees the fix and its two tests discharge the
finding, and plans T002 — the per-producer upgrades, each adding its type to
`TRIPLE_REQUIRED_TYPES` in the same commit that gives its producer a real
triple, with the content goldens and the anti-boilerplate assertions. Phase 1
rule 1 first: re-read `.agent/STOP`.
