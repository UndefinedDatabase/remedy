# Handback — F031 Decision inbox, round R13

Feature F031 · round R13 · branch `feature/f031-decision-inbox` · base
`13306809da092eef995061b5809dd70e5a93f505`. Five commits, so the AGENTS.md
`### handoff.md` tier is the ≤60-line one (≤100 needs >5 commits).

Fortschritt: ~40 % (F031 claimed; R1 through R12 landed and gated ·
             T001 SHIPPED · T002a's MODEL shipped and red-proofed ·
             the `.tsx` projection, T002b ordering/filtering/badge and
             T003 offen) — Schaetzung

## Range

Review of `13306809da092eef995061b5809dd70e5a93f505`..HEAD (C3).

## Commits

### 09b6cd82 chore(agent): save the F031 R13 step block verbatim
| Path | +/- | Reason |
| `.agent/authored/f031-r13.md` | +345/-0 | C0a — the block saved verbatim |

### f010184a chore(agent): mirror the R13 block into last_block
| Path | +/- | Reason |
| `.agent/last_block.md` | +203/-308 | C0b — mirrored from the committed C0a blob |

### a48e0144 docs(agent): restore the seed-key risk to the F031 plan at R13
| Path | +/- | Reason |
| `.agent/plan.md` | +31/-31 | C1 — PLANF031R13, carrying the R-0680 repair |

### bae304bc docs(agent): record the F031 R12 verdict and register R-0680
| Path | +/- | Reason |
| `.agent/live_review.md` | +4/-0 | C2 — LEDGER13 appended, and nothing else |

### C3 — this commit, docs(agent): write the F031 R13 handback
| Path | +/- | Reason |
| `.agent/handoff.md` | rewrite | C3 — a handoff cannot table its own commit (R-0149) |

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a  | done   | |
| C0b  | done   | |
| C1   | done   | |
| C2   | done   | |
| C3   | done   | this commit |
| push | done   | ordered after C3; outcome carried by G10 to the reviewer |

## External actions

`git push origin feature/f031-decision-inbox`, run after C3, no force and no rewrite.
This gate's outcome is not a value of any file this round writes: the reviewer
measures the pushed tips at the next gate and records them in the R13 entry of
`.agent/live_review.md`. Also `git worktree add --detach .remedy-wt/f031-r13-mutant
bae304bc` and `git worktree remove --force` at that exact path, for the G5 negative
control. `gh pr list --state open` read as `[]`. No PR created, none merged.

## Verification

G1 PASS — `git branch --show-current` = `feature/f031-decision-inbox`, not `main`; `.agent/STOP` ABSENT on disk before C0a and again before C3; `git status --porcelain` 0 lines after each of C0a, C0b, C1 and C2.
G2 PASS — all FOUR readings equal at sha256 `77ed31a73bb85778af3de70bcf3eb29eec311c639d692b03f117d80e27add5c8`, 29728 bytes, 345 lines; C0a's and C0b's file resolve to the SAME blob id `15e71b0dbeabdd80100b08cb9c236d1a013258d7`.
G3 PASS — my extractor over the committed C0a blob printed 2 slices (PLANF031R13, LEDGER13), 52 CONTENT lines inside markers, 345 TOTAL lines.
G4 PASS — `.agent/plan.md` at `a48e0144` byte-equal to PLANF031R13 under the newline-INCLUDED convention, slice 2910 bytes and file 2910 bytes, both 49 lines; NEGATIVE CONTROL against the slice with its trailing newline removed FALSE; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 49, strictly under 50. THE REPAIR MEASURED, NOT ASSUMED: `R19` occurs 0 times in `.agent/plan.md` at the base `13306809` and 2 times at C1.
G5 PASS — the one equality over the whole file in the shape constraint 7 states: TRUE, arithmetic 588533 + 1 + 9147 = 597681 against an actual 597681. SECOND, INDEPENDENT reader: blank-line split, N = 2 paragraphs as my own split measured, the last 2 units equal LEDGER13's 2 paragraphs IN ORDER TRUE; unit count 288 before, 290 after. NEGATIVE CONTROL, written only inside the disposable worktree: one byte flipped at offset 591682 inside the FIRST paragraph the append added — BOTH readers reject the mutant and BOTH accept the true file.
G6 PASS — `^- R-\d+ — ` 240 → 241, all DISTINCT at both ends, ids ADDED exactly `R-0680`, ids REMOVED the EMPTY SET, maximum `R-0679` → `R-0680`; `^Done: R-` 2 → 2 and `^Recurrence: R-` 15 → 15, both UNCHANGED; `^Gate: R\d+ — ` 12 → 13 gaining exactly the key `R12`, with `R19` and `R1` through `R11` still present and all 13 DISTINCT. The §3 item 10 open set at C2 is 239.
G7 PASS — `^<<<SLICE ` and `^<<<END ` both 0 in `.agent/plan.md` at C1 and `.agent/live_review.md` at C2; `git diff --name-only 13306809..bae304bc` names NO path under `packages/`, `apps/`, `tests/` or `docs/`, and neither `.agent/decisions.md` nor `.agent/context.md` nor either inventory; per commit over C0a..C2 each single-parent with `git diff --numstat` insertions 345, 203, 31 and 4, each under 500 and each equal cell for cell to the `## Commits` table above; range path set MINUS change set EMPTY, change set MINUS range exactly `.agent/handoff.md`; `git ls-files .remedy-wt` 0 and `git ls-files *.zip` 0. REFLOG, scoped to this round's 4 entries and read by the OPERATION PREFIX before the first colon of `git reflog --format=%gs`: all 4 are `commit`, so `amend` 0, `rebase` 0 and `cherry` 0.
G8 PASS — `npm run test:unit` in `apps/ui` exit 0 at 21 files and 312 tests, unchanged from the base's 21 and 312, which is the expected reading since this round adds no test; `npm run typecheck` in `apps/ui` exit 0 with zero diagnostics. No lint command was ordered and none was run.
G9 PASS — my extractor measured 12 SHA-shaped tokens, 6 distinct, in the committed C0a blob; every one resolves under `git cat-file -t` to type `commit` (`13306809`, `13306809da092eef995061b5809dd70e5a93f505`, `6325ac2f`, `8b4e2295`, `8df27c6e`, `f94ca4f5`) and the FAILING SET is EMPTY. `git worktree list` printed 1 line immediately before the first pytest. The five suites ran SERIALLY in the primary checkout at the C2 tree, never two alive at once, every one a real exit 0 at 474, 52, 21, 16 and 42 — identical to the reviewer's base readings, so there is no difference to account for.
G10 — ordered and run after C3; see `## External actions` for the command and its named carrier. The real outcome is reported in the round report.

## Authored-text proofs

Both slices were extracted PROGRAMMATICALLY from the COMMITTED C0a blob by their
`<<<SLICE` / `<<<END` marker LINES; no marker line reached a target file (G7).
PLANF031R13 → `.agent/plan.md` at C1: disk-to-disk byte-equal TRUE, trailing-newline
-removed control FALSE. LEDGER13 → `.agent/live_review.md` at C2: whole-file equality
against base blob + one newline + slice TRUE, corroborated by the independent
blank-line reader. Both measured under G4 and G5 above.

## Deviations & assumptions

1. HANDBACK CAP OVERAGE, declared under DECISION D15: this file is 118 lines against
   the ≤60-line tier that 5 commits earn. The mandated content behind it: five
   per-commit tables, the six-row item-status table, one line per gate for ten
   gates, the authored-text proofs, the finding counts and the verbatim
   `Fortschritt:` block, whose 4 lines I counted myself. No section was dropped.
2. COMMIT SEQUENCE: no departure — C0a, C0b, C1, C2, C3 exactly as constraint 3
   orders, no extra commit, none dropped, no reordering.
3. ASSUMPTION, as G4 requires it stated: the convention is newline-INCLUDED, so each
   slice ends in the newline its last content line carries.
4. TOOLING DEVIATION, no change of meaning: the shell rejected `cd apps/ui && npm …`
   and `gh … ; echo $?` by shape, so those command lines were run with the working
   directory set through a `python3` subprocess. Every exit code above is real.
5. CONTRADICTIONS: none. Every value the block predicted reproduced exactly, and no
   clause of it disagreed with another.

## Findings

Per DECISION F009 D10 each count carries its rule and its commit. By the §3 item 10
rule — every `^- R-\d+ — ` paragraph in `.agent/live_review.md` minus every
`^Done: R-\d+ — ` line — the open set is 239, measured at C2 `bae304bc`, up from 238
at the base `13306809`. This round minted exactly one id, `R-0680`, and wrote no
`Recurrence:` and no `Done:` line. The findings THIS FEATURE MUST STILL ACT ON — a
narrower set, never called "open" unqualified — are the twenty the plan lists at C1,
of which R-0495 and R-0574 are the two Highs.

## Next

1. Phase 1 rule 1: re-read `.agent/STOP` from disk. It was ABSENT at this round's
   two reads; the next session reads it again rather than inheriting that.
2. Phase 1 rule 2, the Open PR Gate: `gh pr list --state open` is EMPTY and NO pull
   request exists for `feature/f031-decision-inbox` in any state, so none is merged
   and none is created yet.
3. The R13 verdict is UNRECORDED. It is owed by the NEXT round's ledger commit,
   which by DECISION F085 D9 no artefact of this round could carry.
4. The next build step projects the shipped `decisionCard.ts` model into a `.tsx`
   card per DECISION F031 D4, mounted in `RightLivePanel`, with no branching of its
   own — every decision it makes must already exist in `decisionCard.ts`.
