# Handback — F086 R1 · claim, live-review reset, two closure candidates registered

Branch `feature/f086-release-capability`, cut from `main` at 76661dc1 (merge of PR #206). Bundle
C0a, C0b, C1, C2, C3, C4 in order; no extra commit, none dropped, none reordered.

Fortschritt: ~1 % (F086 beansprucht · T001/T002/T003 offen) — Schätzung

## Range

Review of 76661dc1..HEAD

## Commits

### 708f4408 chore(state): save the F086 R1 block verbatim as authored text
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f086-r1.md | +377/-0 | C0a — block saved by file copy, never retyped |

### 8e264a14 chore(state): mirror the committed F086 R1 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +375/-297 | C0b — whole-file mirror of the COMMITTED C0a blob |

### f4fe4142 docs(state): reset plan.md for the F086 release-capability claim
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +34/-40 | C1 — whole file := PLAN slice, before any ledger commit |

### 745e6014 docs(state): reset live_review.md for F086 and register R-0570 and R-0571
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +33/-4140 | C2 — header + R-0570 + R-0571 + 152 carried F085 paragraphs |

### 8f35e77e docs(roadmap): claim F086 in the ledger and reset the claim state
| Path | +/- | Reason |
|------|-----|--------|
| docs/roadmap/STATUS.md | +1/-1 | C3a — the F086 line moves from `[ ]` to `[~]` |
| .agent/context.md | +27/-28 | C3b — whole file := CONTEXT slice |
| .agent/candidates.md | +4/-39 | C3c — whole file := CANDIDATES slice; carrier emptied |

### this commit docs(state): write the F086 R1 handback
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | self-referential | C4 — its own insertion count cannot exist while it is written; it is reported in the round report |

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → exit 0, output `[]`;
  nothing to merge, so the branch was created.
- `git checkout -b feature/f086-release-capability` → exit 0, from HEAD 76661dc1.
- `git push -u origin feature/f086-release-capability` → exit 0, new remote branch. No PR opened.
- `git worktree add` / `remove`: none — no destructive or red-proof check was needed this round.

## Verification

| Gate | Command / property | Exit | Real result |
|------|--------------------|------|-------------|
| G1 | `git worktree list`; `.agent/STOP` | 0 | 1 line; STOP absent. The post-C4 `git status --porcelain` reading is self-referential and sits in the round report |
| G2 | sha256 of the three block copies | 0 | 7220323b5f3b79e649ae9a613cd8ec3402cd115c84ffa01a709b2c0c284b8880, 26550 bytes, 377 lines, all three byte-EQUAL |
| G3 | recount with the C2 regexes at HEAD | 0 | registered 154, resolved 0, `Landed:` 0, duplicate ids 0, unregistered resolutions 0; open at HEAD 154 vs open at base 152; set equality TRUE, added exactly R-0570 and R-0571; max id R-0571, next free R-0572 |
| G4 | carried paragraphs vs the 76661dc1 blob | 0 | compared 152, byte-equal 152 — the two numbers agree |
| G5 | `Steps` in `.agent/live_review.md` | 0 | present |
| G6 | STATUS.md at HEAD | 0 | FROM 0x, TO 1x, `^- [~]` 1x, `^- [x] F###` 51x, `<<` 0x |
| G7 | `.agent/context.md` at HEAD | 0 | `## Active Branch`, `feature/`, `Steps`, an F-id and `pytest`/`resource` all present |
| G8 | `.agent/plan.md` at HEAD | 0 | `## Goal`, `## Next Steps`, an F-id present; 43 lines, under 50 |
| G9 | files vs slices in the COMMITTED authored block | 0 | context 107f45de… 47 lines, plan 83abea54… 43 lines, candidates 22f2c43b… 13 lines — all byte-equal |
| G10 | the four state-reader suites, `-q -rf`, primary checkout, serial | 0 | 160 passed in 19.92s |
| G11 | `python3 -m pytest tests/docs/ -q` | 0 | 295 passed |
| G12 | `python3 -m pytest tests/orchestration/test_roadmap_index.py -q` | 0 | 30 passed |
| G13 | `python3 -m pytest tests/cli/test_golden_path.py -q` | 0 | 42 passed |
| G14 | `git diff --name-only 76661dc1..HEAD` | 0 | at C3, the 7 non-handoff paths — exactly the ordered set minus `.agent/handoff.md`, which is C4's own file; the post-C4 listing is in the round report |
| G15 | `git show --numstat` per commit | 0 | C0a 377, C0b 375, C1 34, C2 33, C3 32 — none over 500; C2 is additionally exempt under DECISION F104 D1. C4 in the round report |
| G16 | `git log --format=%p 76661dc1..HEAD`; `git reflog` | 0 | one parent per commit, linear; reflog shows only `commit:` and `checkout:` |

## Authored-text proofs

All eight slices were extracted programmatically by their one-line markers from the COMMITTED
`.agent/authored/f086-r1.md` and applied byte-verbatim; no marker line reached a target file, and
the three whole-file targets are byte-equal to their slices (G9). The STATUSLINE pair measured as a
REWRITE (`TO contains FROM: false`); it matched 1 line before, FROM 0x and TO 1x after.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a block save | done | 708f4408 |
| C0b last_block mirror | done | 8e264a14 |
| C1 plan.md | done | f4fe4142 |
| C2 live_review.md reset | deviated | 745e6014 — separator convention, below |
| C3 claim | done | 8f35e77e |
| C4 handback | done | this commit |

Open findings: 154, next free id R-0572. `.agent/candidates.md` carries no candidate.

## Deviations & assumptions

C2 separator convention, DECLARED. The block orders slices a, b, c then the carried set "in this
exact order" and states the one-blank-line separator only for item d. A literal concatenation would
butt `## Findings`, R-0570, R-0571 and the first carried paragraph together with no blank line,
contradicting both the shape d prescribes and the pre-reset record at 76661dc1. Exactly one blank
line was therefore placed after `## Findings` and between all 154 finding paragraphs. No slice byte
was altered; G4 reads 152 of 152.

Stated-cause overage (AGENTS.md DECISION D15): this file is 111 lines against the 100-line cap for a
>5-commit bundle. The cause is mandated content — six per-commit tables, the sixteen-row gate table,
the item-status table, the transport and pair proofs and this declared deviation. No section dropped.

## Next

The reviewer gates 76661dc1..HEAD and issues the R1 verdict. Then R2, the packaging-shape
inventory, MEASURED from a real build. Phase 1 rule 1 first: re-read `.agent/STOP` from disk.
