# Handback — F085 R46

Feature F085 (sandbox hardening) · Round R46 · Branch feature/f085-sandbox-hardening · Base SHA 470d2577

## Range

Review of 470d2577..HEAD

## Commits

### 6f302271 docs(f085): save the R46 step block — C0a
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r46.md | +192/-0 | block saved byte-verbatim from the reviewer's .remedy-wt file |

### 5b351a2e docs(f085): mirror the R46 block into last_block — C0b
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +144/-429 | identical bytes mirrored |

### 9afeeb86 docs(f085): record the R45 PASS, register R-0547, correct the D6 figure — C1
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +60/-0 | RECORD14 appended |
| .agent/decisions.md | +17/-0 | DEC6C appended; DEC6 itself left byte-identical |

### C2 — this commit, docs(f085): rewrite the handback for R46
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | a handback cannot table the commit that writes it (R-0149) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | this commit |

## External actions

`git push -u origin feature/f085-sandbox-hardening` after C2. No worktree added, no PR, no merge.

## Verification

G1 STATE, exit 0. `.agent/STOP` absent before C0a and again before C2. `git status --porcelain` exit 0 with empty output at round start and after each of C0a, C0b, C1. `git worktree list` one line throughout.

G2 TRANSPORT, exit 0. All five copies byte-EQUAL disk-to-disk, no digest fallback — reviewer `.remedy-wt/f085-r46.md`, committed `.agent/authored/f085-r46.md`, committed `.agent/last_block.md` and both working copies: sha256 89a8b79bd98dbc53c40225c15b0070e9a57cad5d1cb788d6eef2dac6bce1363c, 13950 B, 192 lines, 4 marker lines, each of the four values measured separately on every copy.

G3 APPEND SHAPE, exit 0, measured separately per path. RECORD14 → `.agent/live_review.md`: pre-commit blob is a byte-exact prefix true; remainder is exactly one blank line plus the slice true; slice is an exact suffix true; 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` in the file; slice 59 lines of which 3 empty; C1 adds 60 lines to the path; 0 non-empty slice lines occur ≠1x among them; numstat `60 0`. DEC6C → `.agent/decisions.md`: prefix true, remainder true, suffix true, 0 marker LINES; slice 16 lines of which 3 empty; C1 adds 17 lines; 0 violations; numstat `17 0`.

G4 SUITE, both in the primary checkout, both exit 0. Four state-reading files `-rf -q` → `159 passed in 19.84s`, against the reviewer's base reading of 159 at 470d2577. CANARY `tests/cli/test_golden_path.py -q` → `42 passed in 20.34s`, base 42.

G5 ARITHMETIC, exit 0. Line-start patterns `^- R-\d{4} `, `^Done: R-\d{4}`, `^Landed: R-\d{4}`. Base 470d2577: 161 / 27 / 0, 134 open, max registered R-0546, max resolved R-0532, 0 duplicate ids, 0 resolutions naming an unregistered id — reproduces the reviewer's stated base exactly. HEAD: 162 / 27 / 0, 135 open, max registered R-0547, 0 duplicates, 0 orphan resolutions. Symmetric differences: registered exactly R-0547; done EMPTY; landed EMPTY. Next free id R-0548.

G6 HYGIENE, exit 0, measured before C2. `git diff --name-only 470d2577..HEAD` returns exactly four paths — `.agent/authored/f085-r46.md`, `.agent/decisions.md`, `.agent/last_block.md`, `.agent/live_review.md` — the declared change set minus `.agent/handoff.md`, and nothing else. Insertions: C0a 192, C0b 144, C1 77; none exceeds 500, so the allowance spent at d4473f85 was not called on again. C2's own insertions go in the round report. Every commit has exactly one parent.

## Authored-text proofs

Both slices were extracted PROGRAMMATICALLY from the committed `.agent/authored/f085-r46.md` by BEGIN-/END- marker pair, read back through `git show HEAD:` — neither retyped, neither taken from the prompt, which carried none. RECORD14 sha256 ecb74b8c782b1baaa916590eac651c0832fc5495e9ec933480f94e5f36e0ed9d, 5134 B, 59 lines. DEC6C sha256 b1bb9c74c7725deabace604e20dac61b3471a7ea7b86210401e4a944aad93c67, 1100 B, 16 lines. Neither slice carries a FROM, so no containment reading is owed. 0 marker lines reached either target. The disk-to-disk equality against the reviewer's original is G2.

## Constraint 7 — the block's own size, re-measured from the committed file

TOTAL 192 lines; PROSE 117 — 192 minus the 75 lines strictly inside a marker pair, markers counted as prose, which is the counting DECISION F085 D5 fixes. Both readings AGREE with the reviewer's stated PROSE 117 / TOTAL 192; there is no disagreement to report. Inside the 490-line total D6-as-corrected rules and the 400-line prose cap D5 rules.

## Deviations & assumptions

1. This handback exceeds the 60-line cap under AGENTS.md DECISION D15. Cause, named: the four-commit per-commit changed-files table, the item-status table over C0a-C2, the six G1-G6 transcripts carrying their real numbers, the authored-text pair proofs and the constraint 7 size reading. No section was dropped and no transcript was padded. Actual line count: 83.
2. `.agent/plan.md` was NOT updated and still reads `Current Step: R45`. The block's change set names five paths, plan.md is not among them, constraint 5 forbids touching anything outside it and G6 goes red on any extra path — so advancing the plan would have turned a green gate red, which constraint 6 makes a STOP. Declared rather than repaired: AGENTS.md commit-gate item 1 is therefore unmet for this round's commits, and R47 owes the advance. This is a defect in the block, not a choice.
3. No commit was added, dropped or reordered. The bundle ran C0a, C0b, C1, C2 exactly as ordered, and no gate came out red.

Fortschritt: ~85 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R45 PASS ·
T002a KOMPLETT · T002b KOMPLETT, alle Sites der Klasse auf dem Seam · T002c-d, T003 offen) —
Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

## Next

R47, started by a FRESH session. Its first two acts are the checklist item 16 widening that R-0537 and R-0543 both name and that R45 then R46 each cut for size, and the correction R-0547 asks the checklist to carry. T002c then opens with the two DoD sites in `packages/orchestration/dod_runners.py`, whose policy differs from the `test` class because their children are the long-lived harness and take no wall timeout. T002d, T003, the integration gate and closure follow.

R46's OWN verdict is deliberately NOT on disk as a gate entry. The round that records a verdict cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13), so that absence is this round's terminator and not a missing gate: R47 must NOT open a repair round to close it. R46's verdict, when the reviewer issues it, is recorded by R47's own record slice.

Open findings: 135, next free id R-0548. Phase 1 rule 1 first: re-read `.agent/STOP` from disk.
