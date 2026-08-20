# Handback — F255 R4 (Teacher role): record R3, amend the feature file

## Range
Review of `a0b8e542..HEAD` — branch `feature/f255-teacher-role`, six commits, no code.

## Commits

### abb8b7ea docs(state): save the F255 R4 step block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f255-r4.md` | 337/0 | C0a — the R4 block, byte-copied from `.remedy-wt/f255-r4.md`. |

### bbbf37ca docs(state): mirror the F255 R4 step block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 266/313 | C0b — same bytes mirrored; verbatim rewrite of one `.agent/` state file. |

### 4e1df902 docs(review): record the R3 verdict
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/0 | C1 — RECORDR3 appended after exactly one blank line. No finding registered. |

### d5ffa2e3 docs(roadmap): amend the F255 feature file with the R3 rulings
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T5_F255.md` | 128/0 | C2 — AMEND255 appended. Zero deletions: no registered byte changed. |

### ef792c68 chore(plan): advance the plan to F255 R4
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 19/22 | C3 — whole-file PLAN255R4, 40 lines. |

### (this commit) docs(state): write the F255 R4 handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | see round report | C4 — this file; a handback cannot table its own cell (R-0149). |

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |

## External actions
`git push` after C4 — real output in the round report. No pull request created and none
open on this branch; no CI run awaited or reported (constraint 10); no `gh` command run;
no git worktree created or removed this round.

## Verification
One line per gate; the full transcripts are in the round report, not here (R-0582).
- G1 `.agent/STOP` read from disk before C0a and ABSENT; branch `feature/f255-teacher-role`; `git status --porcelain` EMPTY after every commit and at the handback; `git worktree list` reports the primary checkout alone. All blob readings taken with `git show`.
- G2 `.remedy-wt/f255-r4.md`, `.agent/authored/f255-r4.md` @abb8b7ea and `.agent/last_block.md` @bbbf37ca are all EQUAL at sha256 `0c6e610c…`, 24010 B, 337 lines — the digest stated at delegation.
- G3 slices extracted by `python3 .remedy-wt/extract_r4.py <NAME>` from the COMMITTED C0a blob, never retyped; newline-INCLUDED convention (R-0600): RECORDR3 `fb634121…` 3552 B 1 line, AMEND255 `70d2db45…` 7006 B 127 lines, PLAN255R4 `b2c1af4e…` 2217 B 40 lines.
- G4 base blob is a byte-exact PREFIX of the C1 blob; remainder `af409091…` 3553 B 2 lines equals LF + RECORDR3, blank separator PRESENT; an independent paragraph split (186 units) yields RECORDR3 as its LAST unit at `fb634121…` 3552 B 1 line newline-INCLUDED and `0d6ad873…` 3551 B STRIPPED; a one-character mutant of the remainder is REJECTED by BOTH readings. Registered / resolved / open / line-anchored `Landed:` measured 178 / 0 / 178 / 0 at a0b8e542 AND 178 / 0 / 178 / 0 at C1 — UNCHANGED, as constraint 5 orders. `Gate: R4 — the R3 entry.` occurs 1x, is the LAST line beginning `Gate: R`, and all four header keys are distinct.
- G5 the base blob of `docs/roadmap/features/T5_F255.md` at a0b8e542 — 2730 B over 47 lines, 2713 characters, the difference being multi-byte UTF-8 — is a byte-exact PREFIX of the C2 blob, and the remainder equals a blank line followed by AMEND255 byte for byte. Line 1 `# T5_F255 — Teacher role (evidence-grounded live explainer & learn-along tutor)` and lines 2-4 `**Tier 5 · Registered by registration round plan0806 (2026-08-06,` / `operator-relayed) · Depends on: stable ledger event vocabulary (Tier 2),` / `F103 (budget separation) · Blocks/used by: —**` are identical to the same lines at the base, which is what `packages/orchestration/roadmap_index.py` parses. `## Scope (registered verbatim, plan0806 2026-08-06)` occurs 1x and the text from it to `## Non-goals` is byte-identical at both ends (`e7170e74…`, 1970 B). The C2 blob's `## ` headings in order: Goal & Done · Scope (registered verbatim, plan0806 2026-08-06) · Non-goals · Amendment status (F255 R3/R4, 2026-08-20) · Design (ruled at R3) · Task slicing · Acceptance · Edge cases & assumption defaults (A9) · Orchestrator brief · Do not touch.
- G6 `python3 -m pytest tests/orchestration/test_roadmap_index.py -q -rf` exit 0, 30 passed; `python3 -m pytest tests/docs/ -q -rf` exit 0, 295 passed. Each reported separately; 325 together, equal to the reviewer's pre-measurement.
- G7 `.agent/plan.md` @ef792c68 byte-equals PLAN255R4 at `b2c1af4e…`, 2217 B, 40 lines — under the 50-line cap — with `## Goal` 1x, `## Next Steps` 1x and `F255` 3x.
- G8 serially, in the primary checkout, never two pytest processes at once: the four-file state-reader selection exit 0, 160 passed; `tests/cli/test_golden_path.py` exit 0, 42 passed. Both equal the reviewer's reading at a0b8e542.
- G9 `git diff --name-only a0b8e542..HEAD` equals the Change list with no path on either side alone; the same command scoped to `apps/ packages/ tests/ scripts/` — `docs/` deliberately excluded, because C2 changes a file under it — is EMPTY; each of the eight paths named untouched is PRESENT at the base and absent from the range; every commit in the range has exactly one parent; insertion columns 337, 266, 2, 128, 19, every one under 500, the same `+/-` cells as the table above. Reflog, as TWO measured claims read from the operation PREFIX before the first colon (R-0601): after C3, 5 entries whose prefix is `commit`, one per commit made so far, and 0 entries whose prefix contains `amend`, `reset`, `rebase` or `cherry`. C4's own entry, the final 6 / 0 reading and C4's numstat cell are in the round report.
- G10 lines beginning `<<<SLICE ` or `<<<END `: `.agent/live_review.md` @4e1df902 0, `docs/roadmap/features/T5_F255.md` @d5ffa2e3 0, `.agent/plan.md` @ef792c68 0. `.agent/handoff.md` carries no such line either; its committed-blob reading is in the round report.
- G11 `git push` after C4 — real output in the round report.

## Authored-text proofs
All three slices were applied by script from the COMMITTED `.agent/authored/f255-r4.md`, never
retyped and never rewrapped. Disk-to-disk against that file: the C1 append remainder equals
LF + RECORDR3 and the C2 append remainder equals LF + AMEND255, each byte for byte; `.agent/plan.md`
at C3 byte-equals PLAN255R4. Digests under G3, G4 and G5 above.

## Deviations & assumptions
- ORDERED COMMIT SEQUENCE FOLLOWED EXACTLY. C0a, C0b, C1, C2, C3, C4 in the block's order,
  one path each, no extra commit, none dropped, none reordered.
- THE REFLOG CONTROL DISCRIMINATED THIS ROUND, which is the first time it has. The
  prefix-scoped reading is 0, but the whole-line reading R-0601 warns against is 1: C2's own
  subject, `docs(roadmap): amend the F255 feature file with the R3 rulings`, contains the word
  `amend`. Read the whole line and this round reports a rewrite that never happened.
- `Landed:` REPORTED UNDER BOTH READINGS. Line-anchored `^Landed:` is 0 at the base and 0 at C1,
  which is the ordered reading. The unanchored substring count moves 23 → 24, because RECORDR3
  quotes the token once in its own prose. No `Landed:` line was written.
- RESOLVED IS 0 UNDER A STRUCTURAL PREDICATE, not a text search. Line-anchored `^Resolved:` is 0
  and `^Done:` is 0 at both ends. A case-insensitive search for the word hits prose 14x at BOTH
  ends and is not the count.
- SCRATCH HELPER, NOT PART OF THE CHANGE SET. `.remedy-wt/extract_r4.py` and the three extracted
  slice files were written under the gitignored `.remedy-wt/` (`.gitignore:235`) and are absent
  from the range.
- NO TOKEN-CAP CLAIM IS MADE. DECISION F255 D6 withdrew the template's 800-token cap; R5 removes
  the sentence. This handback is inside the LINE cap its six-commit table earns.
- Nothing was built: no role, no command, no config key, no test (constraint 7).

## Next
1. Phase 1 rule 1 of the next session: re-read `.agent/STOP` from disk.
2. R5 — the docs round that applies DECISION F255 D6 to `docs/agents/handback_template.md`,
   removing the withdrawn 800-token cap and stating the LINE cap as the operative bound.

R4 awaits review. There is no open pull request on this branch.

Fortschritt: ~12 % (F086 merged · F255 claimed · ground measured · six DECISIONs ruled · the feature file now carries its Design, Task slicing and Acceptance · T001 builds next) — Schätzung
