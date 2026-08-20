# Handback — F086 R2 · the R1 carry repaired, both defects registered

Branch `feature/f086-release-capability`, continued from `25f7a5af`. No branch created, no Open PR
Gate run, no PR opened. Bundle C0a, C0b, C1, C2, C3, C4, C5 in order; none extra, dropped or moved.

Fortschritt: ~1 % (F086 beansprucht · R1 repariert · T001/T002/T003 offen) — Schätzung

## Range

Review of 25f7a5af..HEAD

## Commits

### 2f777a19 chore(state): save the F086 R2 block verbatim
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f086-r2.md | +319/-0 | C0a — `shutil.copyfile` of `.remedy-wt/f086-r2.md`, never retyped |

### 7a6b9c98 chore(state): mirror the R2 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +217/-275 | C0b — whole-file mirror of the COMMITTED C0a blob |

### 4fd5c5d7 chore(state): advance the plan to the R2 repair round
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +13/-10 | C1 — whole file := PLAN2 slice, before any ledger commit |

### 6a894b0b docs(review): register the truncated-carry defect and the self-referential gate
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +4/-0 | C2 — R0572 then R0573 appended; findings persist before the repair |

### 0ac027da docs(review): restore the truncated finding paragraphs verbatim
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +589/-0 | C3 — 39 truncated lines become 628 full paragraph lines; 0 deletions |

### 132b1393 docs(review): record the restoration and resolve the truncated-carry finding
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +2/-0 | C4 — DONE1 appended, strictly after C3 and after G5 ran |

### this commit docs(state): write the F086 R2 handback
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | self-referential | C5 — its own count cannot exist while it is written; it is in the round report |

## External actions

- `git push origin feature/f086-release-capability` — after C5; result in the round report.
- `git worktree add` / `remove`: NONE — G5's negative control reads the `25f7a5af` blob through
  `git show`, read-only, no checkout. No `gh` command, no PR create/edit/merge.

## Verification

Run from `/home/decodeux/Repos/remedy`, `pwd` confirmed; both pytest gates ran SERIALLY, in the
primary checkout.

| Gate | Command / property | Exit | Real result |
|------|--------------------|------|-------------|
| G1 | `git worktree list`; `.agent/STOP`; branch | 0 | 1 line; STOP absent; `feature/f086-release-capability`. Post-C5 `git status --porcelain` is self-referential → round report |
| G2 | sha256 of the three block copies | 0 | 87aa80c9cfe85916490ef1e516b960e6a24d4398a182d15b9fb742d9e48f4abf, 24675 bytes, 319 lines, all three byte-EQUAL; the two committed copies share one git blob id |
| G3 | `.agent/plan.md` vs the PLAN2 slice of the COMMITTED authored file | 0 | byte-equal; `## Goal`, `## Next Steps`, `F086` present; sha256 f5ddab4f6db64c09866e2a429199dade24515e67a2e2645c043a8ac7b8744a08, 46 lines, under 50 |
| G4 | ledger recount, C3 extraction, as SET comparisons | 0 | registered HEAD 156 vs base 154, difference exactly {R-0572, R-0573}, none removed; resolved HEAD exactly {R-0572}; `Landed:` 0; duplicates 0; unregistered resolutions 0; open HEAD 155 vs base 154, difference exactly {R-0573}; max R-0573, next free R-0574 |
| G5a | carried paragraphs at HEAD vs the `76661dc1` blob | 0 | compared 152, equal 152 — the two agree |
| G5b | NEGATIVE CONTROL, same script, `25f7a5af` in place of HEAD | 0 | compared 152, equal 113 — strictly fewer equal than compared, so the check DOES separate the corrupt state from the repaired one |
| G6 | character volume of the carried set | 0 | HEAD 263073, `76661dc1` 263073, difference 0; at `25f7a5af` 210156, a shortfall of 52917 |
| G7a | repair-set paragraphs spanning >1 physical line | 0 | 39 of 39 at HEAD; 0 of 39 at `25f7a5af`; 39 of 39 at `76661dc1` |
| G7b | carried paragraphs whose text ends `OPEN.` | 0 | HEAD 86, `76661dc1` 86 — equal; `25f7a5af` 75 |
| G8 | `Steps` and `<<<` in `.agent/live_review.md` | 0 | `Steps` present; `<<<` 0x |
| G9 | R-0570 / R-0571 vs their slices in the COMMITTED `.agent/authored/f086-r1.md`; header | 0 | both byte-equal to their slices; header byte-unchanged from `25f7a5af` (2354 chars) |
| G10 | the four runtime/state suites, `-q -rf`, primary checkout | 0 | 160 passed in 20.29s |
| G11 | `python3 -m pytest tests/cli/test_golden_path.py -q` | 0 | 42 passed in 20.30s |
| G12 | `git diff --name-only 25f7a5af..HEAD` | 0 | at C4 the 4 non-handoff paths — the ordered set minus `.agent/handoff.md`, which is C5's own file; post-C5 listing → round report |
| G13 | `git show --numstat` per commit | 0 | C0a 319, C0b 217, C1 13, C2 4, C3 589, C4 2. C3 is the only one over 500 and is EXEMPT under AGENTS.md DECISION F104 D1 — verbatim rewrite of a single `.agent/**` state file. C5 → round report |
| G14 | `git log --format=%p 25f7a5af..HEAD`; `git reflog` | 0 | one parent per commit, linear; reflog holds only `commit:` and `checkout:` — no amend, rebase, reset or force-push |

## Authored-text proofs

PLAN2, R0572, R0573 and DONE1 were extracted programmatically by their one-line markers from the
COMMITTED `.agent/authored/f086-r2.md` and applied byte-verbatim; no marker line reached a target
file (G8). `.agent/plan.md` is byte-equal to PLAN2 (G3); each append is pure concatenation, verified
as `new[:len(old)] == old` and `new[len(old):] == slice`. No FROM/TO pair existed this round.

The 39 restored paragraphs are RESTORED, not rewritten: each came byte-for-byte from the `76661dc1`
blob, and the line diff of C3 is 39 opcodes, all `insert`, zero deletions — no landed byte replaced.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a block save | done | 2f777a19 |
| C0b last_block mirror | done | 7a6b9c98 |
| C1 plan.md := PLAN2 | done | 4fd5c5d7 |
| C2 register R-0572, R-0573 | done | 6a894b0b |
| C3 the repair | done | 0ac027da |
| C4 DONE1 append | done | 132b1393 |
| C5 handback | done | this commit |

Open findings: 155, next free id R-0574. `.agent/candidates.md` holds no candidate, unchanged here.

## Deviations & assumptions

No departure from the ordered commit sequence, no adjusted slice byte, no red gate. Below: one
assumption and one stated-cause cap overage, neither of which is a block departure.

This run's repair set has 39 ids, identical to the set the block states the reviewer measured —
same first three R-0502, R-0503, R-0504 and same last three R-0567, R-0568, R-0569, full list in the
round report. Each of the 39 truncated lines occurred EXACTLY ONCE before replacement. Assumption:
`.agent/context.md` and `.agent/decisions.md` need no update — scope, branch and constraints are
unchanged from R1 — and G12's path set forbids touching them.

Stated-cause overage (AGENTS.md DECISION D15): 122 lines against the 100-line cap for a >5-commit
bundle. Cause is mandated content — seven per-commit tables, the fifteen-row gate table (G5 in two
halves, G7 in two readings), the item-status table, the authored-text proofs. No section dropped.

## Next

The reviewer gates 25f7a5af..HEAD and issues the R2 verdict. Then R3, the packaging-shape inventory
in `.agent/f086_inventory.md`, MEASURED from a real `python -m build`. Phase 1 rule 1 first: re-read
`.agent/STOP` from disk.
