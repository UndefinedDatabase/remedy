# Handback — F031 R4

Feature F031, round R4 (the R3 verdict and the R-0601 recurrence). Branch
`feature/f031-decision-inbox`. Base `f26c5da5e5b6563b1b4fd8e71946344e8c3f6fac`.

Fortschritt: ~3 % (F031 claimed; R1, R2 and R3 landed and gated · the
             source inventory is on disk · the design rulings and T001
             are next · no T-slice started) — Schaetzung

## Range

Review of `f26c5da5..HEAD` — C3's own SHA cannot exist in the text C3 writes.

## Commits

### 3ff12773 docs(state): save the F031 R4 record step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r4.md | +291/-0 | C0a: the block saved verbatim |

### ef3653fe docs(state): mirror the F031 R4 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +166/-238 | C0b: mirror of the committed C0a blob |

### 1d91b6d9 docs(state): advance the plan to the F031 R4 record round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +29/-24 | C1: the PLANF031R4 slice |

### 9808ecbd docs(review): record the F031 R3 PASS and one recurrence
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | C2: GATE3 then RECUR601 appended |

### C3 — this commit, self-reference (R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | n/a | C3: this handback; it cannot table itself |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a  | done   | |
| C0b  | done   | |
| C1   | done   | |
| C2   | done   | |
| C3   | done   | this commit |
| push | deviated | ordered after C3; G10 bars its outcome from any file this round writes (R-0371), so it is reported to the reviewer, not stated here |

## External actions

- `git worktree add --detach .remedy-wt/f031-r4-control 9808ecbd`, then
  `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/f031-r4-control`
  by its EXACT path (R-0662) — G5's mutant control only, gone before G9.
- `git push origin feature/f031-decision-inbox`, ordered after C3 per G10; its
  outcome is reported to the reviewer and is in no file this round writes.
- No pull request created, nothing merged.

## Verification

One line per gate; the transcripts stayed in the round report (R-0582).

- G1 branch `feature/f031-decision-inbox`, not `main`; `.agent/STOP` read off
  disk and ABSENT before C0a and again before C3; `git status --porcelain` 0
  lines after each of C0a, C0b, C1 and C2.
- G2 all four readings sha256
  `e8481b51c7f1fb5a2cab4b26c6a238523d3916859ce820acfa6ac602e3736a96`, 24209
  bytes, 291 lines; C0a's and C0b's file is the SAME blob `302388e9`.
- G3 my extractor over the committed C0a blob printed 3 slices, 51 content
  lines inside markers, 291 total lines.
- G4 `.agent/plan.md` at C1 byte-equal to PLANF031R4, 2988 bytes on both sides
  under the newline-INCLUDED convention; the trailing-newline-removed control
  is FALSE; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 49, under 50.
- G5 reader A, byte offsets: the base blob is a byte-exact PREFIX, the GATE3
  region equals its 4696 slice bytes at offset 532443 and RECUR601 its 2653 at
  537140, delta 7351 = 1 + 4696 + 1 + 2653. Reader B, an independent
  blank-line split, 275 units to 277 with the LAST TWO equal to GATE3 then
  RECUR601 IN ORDER. A one-byte flip inside the FIRST appended paragraph, made
  in a disposable worktree, was REJECTED by both readers while both accepted
  the true file.
- G6 `^- R-\d+ — ` 238 to 238, ids ADDED the EMPTY SET, ids REMOVED the EMPTY
  SET, maximum `R-0677` UNCHANGED, `^Done: R-` 2 to 2, `^Recurrence: R-` 13 to
  14 gaining exactly one `R-0601` line, `^Gate: R\d+ — ` 3 to 4 gaining exactly
  the key `R3` with `R19`, `R1` and `R2` still present.
- G7 `^<<<SLICE ` and `^<<<END ` both 0 in `.agent/plan.md` and in
  `.agent/live_review.md` at C2; `git diff --name-only f26c5da5..9808ecbd`
  names four paths, none under `packages/`, `apps/`, `tests/` or `docs/`, and
  does NOT name `.agent/f031_inventory.md`.
- G8 C0a..C2 each single-parent, insertions 291, 166, 29 and 4, each under 500;
  range MINUS change set EMPTY, change set MINUS range exactly
  `.agent/handoff.md`; `git ls-files .remedy-wt` 0, the zip glob 0,
  `git worktree list` 1 line. THE REFLOG READING STATES ITS OWN SCOPE AND
  FIELD, as RECUR601 requires: over THIS ROUND'S 4 HEAD reflog entries only,
  read by the OPERATION PREFIX before the first colon of
  `git reflog --format=%gs`, all four prefixes are `commit`, so amend 0,
  rebase 0 and cherry 0.
- G9 the five suites SERIALLY, never two pytest processes alive, in the primary
  checkout at the C2 tree, `git worktree list` 1 line immediately before the
  first: exit 0 and 470, 52, 21, 16 and 42 passed, in the order the gate lists
  them — cell for cell the reviewer's readings at R3's C4, nothing to account
  for.
- G10 the push is ordered after C3; its outcome is reported to the reviewer and
  is deliberately not a value of this file (R-0371).

## Authored-text proofs

All three slices were extracted PROGRAMMATICALLY by marker LINE out of the
committed C0a blob, never retyped, and applied whole: PLANF031R4 byte-equal
with its negative control FALSE (G4), GATE3 and RECUR601 byte-equal under two
independent readers plus a mutant control (G5). The block carries no FROM/TO
pair, so no containment reading is owed and none is stated.

## Findings

By §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — `
line — the open set is 236, measured at `9808ecbd`. Constraint 8 held: no id
was minted and no finding record moved, proved by G6. The findings THIS FEATURE
MUST STILL ACT ON — a narrower set, never called "open" unqualified — are the
fifteen the C1 plan's Risks section names, measured at `1d91b6d9`.

## Deviations & assumptions

- Commit count and tier, DERIVED as the block ordered rather than quoted:
  constraint 3 fixes FIVE commits (C0a, C0b, C1, C2, C3). AGENTS.md under
  `### handoff.md` reads "≤60 lines (≤100 when per-commit tables of >5 commits
  require it)"; 5 is not greater than 5, so that condition is FALSE and the
  tier is 60. This file measures 158 lines by `wc -l`, over 60, so a DECISION
  D15 stated-cause overage IS claimed. The cause is mandated content: five
  per-commit tables, the item-status table covering six items, ten gate
  results and the four-item `## Next` this block orders by name. No section
  was dropped to fit, and no token cap is claimed — that cap is withdrawn.
- THE BLOCK'S STATED BASE SHA DOES NOT EXIST AS AN OBJECT. Its Base section
  names `f26c5da5e5b60e8b7a3b2ba1a4b1a0e5c0ff5a0d`; `git cat-file -t` on that
  id fails with "could not get object info". The branch tip — which the same
  sentence names as the resolution rule, and which equals the remote tip — is
  `f26c5da5e5b6563b1b4fd8e71946344e8c3f6fac`; the two agree for twelve
  characters and diverge after. I resolved the base by the tip as instructed
  and reconciled nothing (constraint 1). Every base reading the block predicted
  reproduced there exactly: 238 dash-ids all distinct, maximum `R-0677`, 2
  `Done:`, 13 `Recurrence:`, 3 `Gate:` keyed `R19`, `R1`, `R2`, open set 236,
  `.agent/plan.md` 44 lines, the inventory 225 lines with `TO BE MEASURED` 0.
- No extra commit, none dropped, no reordering. No amend, rebase, cherry-pick,
  force push, branch deletion, merge or pull request. No id was minted and
  `.agent/f031_inventory.md` was not touched.

## Next

1. Phase 1 rule 1: re-read `.agent/STOP` from disk before anything else.
2. NO pull request exists for `feature/f031-decision-inbox`, and none should be
   created yet.
3. R5 rules the three design questions `.agent/plan.md` names: what "the
   decision queue" IS, whether the badge is fed by emitting the missing
   decision event kinds or by re-deriving on refetch, and whether the two
   declared-but-unproduced types stay in the set.
4. R5's first commit also records the R4 verdict, which by DECISION F085 D9 no
   artefact of this round can carry.
