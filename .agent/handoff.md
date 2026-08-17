# Handback — F085 Sandbox hardening (stage 1) — R27

Feature F085 · Round R27 · Branch `feature/f085-sandbox-hardening`
Base 369d94a3 · pre-C3 HEAD 0419ac76 · open findings 118 · next free id R-0518
Fortschritt: ~80 % (T001 gebaut · R13-R26 PASS · T002a KOMPLETT · T002b: Seam
gebaut, `test_runner` + `autorun` migriert · T002b Rest, T002c-d, T003 offen) —
Schätzung.

## Range

Review of 369d94a3..HEAD — 5 commits: C0a C0b C1 C2 C3.

## Commits

### 8b1a306e docs(f085): save the R27 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r27.md | +229 | R27 block verbatim; 6 markers, 3 pairs |

### b3c47120 docs(f085): mirror the R27 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +168/-252 | mirrored from the committed blob |

### 2962358e docs(review): record the R26 PASS and register R-0517
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +61 | RECORD2: R26 gate entry + R-0517, appended |

### 0419ac76 docs(f085): advance the plan to R27
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +4/-4 | PLANF2→PLANT2 rewrite of `## Current Step` |

### C3 docs(f085): rewrite the handback for R27 and close the session
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | this file | a handoff cannot table its own commit |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | 229 lines, 6 marker lines, 3 pairs |
| C0b mirror to last_block | done | sourced from the committed blob |
| C1 record R26, register R-0517 | done | append-shaped, numstat 61/0 |
| C2 plan pair | done | PLANF2 matched at exactly one place |
| C3 handback | done | this file, then push |

## External actions

`git push -u origin feature/f085-sandbox-hardening` — run after C3. No PR
created, nothing merged. No `git worktree add`: no destructive check was needed,
so `git worktree list` stayed at its single line all round.

## Verification

G1 STATE — `ls -la .agent/STOP` exit 2 (absent) before C0a and again before C3;
`git status --porcelain` empty (exit 0, no output) at round start and after each
of C0a, C0b, C1, C2; `git worktree list` one line: the repo root at this branch.
G2 TRANSPORT — the committed and working copies of `.agent/authored/f085-r27.md`
and `.agent/last_block.md` are all four byte-EQUAL at sha256
ce7ffcc42df494a9c21e733f410e6d8f48d394bc16239a0be71191232cdeafdd, 14103 B,
229 lines, 6 marker lines; regions 1-60 dfea0906, 61-140 85061d65,
141-229 b03dbb55.
G3 APPEND SHAPE — the pre-commit blob is a byte-exact PREFIX of the post-commit
file; the remainder is exactly one blank line plus RECORD2; RECORD2's first line
occurs 1x among the 61 lines the commit ADDS; 0 lines match
`^(BEGIN|END)-[A-Z0-9]+$` in the file, while the substring `END-` hits 5x — all
of it `APPEND-shaped` prose older than this round.
`git show --numstat` for that path → `61	0	.agent/live_review.md`.
G4 ARITHMETIC — base 369d94a3: 131 registered / 14 done / 0 landed, 117 open,
max R-0516. HEAD: 132 / 14 / 0, 118 open, max R-0517, next free R-0518.
Registered symmetric difference `['R-0517']`; done `[]`; landed `[]`;
0 duplicate ids; 0 resolutions naming an unregistered id.
G5 PLAN PAIR — PLANF2 occurs 0x at HEAD and PLANT2 1x; PLANT2 does not contain
PLANF2, so the pair is a REWRITE. `## Goal` and `## Risks` are byte-IDENTICAL to
their base bytes. `.agent/plan.md` sha256
254757ce2fbc3267ebdda74003373bf987e83371927bb6384a1a50caf470b46c, 2370 B,
41 lines (<50); its `## Next Steps` list parses to the numerals 1, 2, 3.
G6 STATE READERS — `python3 -m pytest tests/orchestration/test_test_runner.py
tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
tests/ui_server/test_dashboard_contract.py -q` exit 0, `158 passed in 21.12s`
— reported as a READING, since that suite spawns wrapper processes under flock
and is timing-sensitive. CANARY: `python3 -m pytest tests/cli/test_golden_path.py
-q` exit 0, `42 passed in 22.01s`. No ruff gate and none skipped by oversight:
the change set contains no `.py` file. No docs gate: nothing under `docs/`.
G7 COMMIT HYGIENE — `git diff --name-only 369d94a3..HEAD` measured before C3 is
exactly `.agent/authored/f085-r27.md`, `.agent/last_block.md`,
`.agent/live_review.md`, `.agent/plan.md` and nothing else. Per-commit
insertions before C3: C0a 229, C0b 168, C1 61, C2 4 — none exceeds 500; C3
cannot measure itself, so its own insertions are reported in the round report.
Every commit has exactly one parent; `git reflog -12` holds only `commit:`
entries.

## Authored-text proofs

RECORD2, PLANF2 and PLANT2 were each extracted PROGRAMMATICALLY by marker pair
from the committed `.agent/authored/f085-r27.md` and applied byte-verbatim; none
was retyped and none was taken from the prompt. RECORD2 slice sha256
9e9cb91b3635dedcca6238dda554a3f67fa7770cacc9febf93aa9dc4f99f2311, 60 lines. No
marker line reached `.agent/live_review.md` or `.agent/plan.md`.

## Deviations & assumptions

Ordered sequence: none. C0a C0b C1 C2 C3 ran exactly as ordered, with no extra,
dropped or reordered commit, and nothing outside the declared change set moved.
Deviations, declared: this handback is 123 lines against the ≤60 cap that a
5-commit round carries. The cause is mandated content only — the five per-commit
tables, the item-status table, and the G1-G7 verification block with its
transport, append-shape, arithmetic and pair proofs (DECISION D15). No section is
dropped and no prose is padded.

## Next

The next session's FIRST action is Phase 1 rule 1 — re-read `.agent/STOP` from
disk — BEFORE rule 2, the Open PR Gate (`gh pr list --state open --json
number,headRefName,baseRefName,isDraft`). R-0517 is OPEN and awaits the next
reviewed round's authored resolution; it is not resolved here, because its fix is
this handback itself and this handback is the round's last commit. R27's own
verdict is NOT a §4.13 terminator — this branch continues, so the next reviewed
round records R27's gate entry in `.agent/live_review.md`. Work then resumes at
T002b: `test_execution_service.py`'s `Popen`, which carries R-0202.
