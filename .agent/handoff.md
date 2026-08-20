# Handoff — F086 Release capability, R4 (record + the packaging DECISIONs)

Branch: feature/f086-release-capability (continued; no branch created, no PR opened).
Base 0cabd17e · HEAD this commit · Open findings 155 (156 registered, 1 resolved).
Fortschritt: ~3 % (F086 beansprucht · R1-R3 gegated · Paketform entschieden · T001/T002/T003 offen) — Schätzung

## Range

Review of 0cabd17e..HEAD

## Commits

### 2abb622b chore(state): save the F086 R4 authored block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f086-r4.md | +302/-0 | C0a, `shutil.copyfile` of `.remedy-wt/f086-r4.md` |

### 67d16973 chore(state): mirror the R4 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +193/-168 | C0b, whole-file mirror of the COMMITTED C0a blob |

### a4059de3 chore(state): advance the plan to the F086 R4 record and decision round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +23/-21 | C1, PLAN4 slice byte-verbatim, whole file |

### 4f812309 chore(review): record the F086 R3 verdict in the review ledger
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C2, RECORD2 appended by pure concatenation |

### 596eb7b0 docs(decisions): rule the F086 wheel asset carry and the single version literal
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +78/-0 | C3, DECISION1 then DECISION2 appended; no landed section edited |

### this commit docs(state): write the F086 R4 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C4, cannot table itself (R-0149 pattern) |

## External actions

`git push origin feature/f086-release-capability` after this commit. No worktree added
or removed (`git worktree list` stayed ONE line), no `gh`, no PR, no venv, no build.

## Verification

| Gate | Exit | Result |
|---|---|---|
| G1 | 0 | `git status --porcelain` EMPTY, `git worktree list` ONE line, `.agent/STOP` absent, branch still feature/f086-release-capability |
| G2 | 0 | scratch, committed authored and committed last_block all byte-EQUAL: sha256 84485aac89d300e388c7a432af78dca51f6da510784d67de60a653cbcdf53b20, 21879 B, 302 lines |
| G3 | 0 | `.agent/plan.md` byte-equal to extracted PLAN4, sha256 872e59f1…5682, 43 lines (<50), has `## Goal`, `## Next Steps`, `F086` |
| G4 | 0 | 156 registered / 1 resolved / 155 open at BOTH SHAs; registered, resolved and OPEN sets IDENTICAL (symdiff empty); 0 dups, 0 unregistered resolutions, 0 `Landed:` |
| G5a | 0 | REQUIRED: compared 152, equal 152 (paragraph extraction, whole block) |
| G5b | 0 | NEGATIVE CONTROL at 25f7a5af: compared 152, equal 113 — strictly fewer; halves DISAGREE, so the check can fail |
| G6 | 0 | RECORD2 present verbatim, begins `Gate:`, no `^- R-\d+ — ` match; `Steps` present; `<<<` occurs 0x |
| G7 | 0 | file at 0cabd17e is a byte-exact PREFIX of HEAD = True; remainder == D1+D2 exactly; D1 sha256 998c729d…7dfd (3251 B), D2 sha256 ead658cf…9e4a (2059 B); `## DECISION F086 D1` 1x, `D2` 1x, `<<<` 0x |
| G8 | 0 | `160 passed in 19.97s`, four state readers, PRIMARY checkout, serial |
| G9 | 0 | `42 passed in 20.48s`, canary, serial, after G8 finished |
| G10 | 0 | authored/f086-r4.md, decisions.md, last_block.md, live_review.md, plan.md (+ handoff.md with this commit); `pyproject.toml`, `ui_server.py`, `apps/`, `tests/`, `docs/` ABSENT |
| G11 | 0 | insertions 302, 193, 23, 2, 78 — none over 500, no exemption invoked |
| G12 | 0 | one parent per commit (linear); reflog shows only `commit:` entries |

## Authored-text proofs

PLAN4, RECORD2, DECISION1 and DECISION2 were extracted PROGRAMMATICALLY by their
one-line markers from the COMMITTED `.agent/authored/f086-r4.md` and applied
byte-verbatim, never retyped: G3 the plan equality, G6 the ledger append, G7 the
decisions prefix-plus-remainder equality; `<<<` occurs 0x in every target.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |

## Deviations & assumptions

1. NO departure from the ordered sequence: five commits in block order plus C4, none
   extra, dropped or reordered. No code, no test, no `docs/` file, no `pyproject.toml`.
2. NO contradiction found between DECISION F086 D1/D2 and `.agent/f086_inventory.md`:
   every figure the DECISIONs cite is the inventory's own reading — 414 members /
   2038283 B / 0 under `apps/ui/dist/` (b, c), 65 src files and the 182948-byte lockfile
   (b), the generic `dist/` ignore and the absent `artifacts`/`force-include` (f), the
   three `.parent` hops (g), the reachable npm spawn (i), `pyproject.toml:7` agreeing
   with the wheel METADATA (e), no `--version` under `apps/` (h).
3. G5 note: "carried at the F086 claim" = the ids in BOTH the HEAD ledger and the
   `76661dc1` blob (152); a first pass over all 184 paragraphs there was the wrong set.

## Next

Reviewer re-runs G1-G12 over `0cabd17e..HEAD` and, on PASS, authors R5 — T001 under
DECISION F086 D1 — Phase 1 rule 1 (`.agent/STOP`) before rule 2.
