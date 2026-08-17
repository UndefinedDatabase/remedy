# Handback — F085 Sandbox hardening (stage 1) — R29

Branch `feature/f085-sandbox-hardening` · Base `b0d09db4` · HEAD before this
commit `f62dfa88`. State-only round: no `.py` file changed.

Fortschritt: ~60 % (T001 gebaut · R13-R28 PASS · T002a KOMPLETT · T002b 5 von 12
Sites auf dem Seam, 7 offen · T002c-d, T003 offen) — Schätzung, gegen die
Klassentabelle aus Amendment F085 D1 gemessen.

Deviations, declared: this file measures 131 lines against the
100-line cap for a >5-commit round. Cause is mandated content only — six
per-commit tables, the six-row item-status table, eight gates with real readings
and the constraint-8 staleness report. No section dropped, no transcript pasted.

## Range

Review of b0d09db4..HEAD.

## Commits

### 57b152c3 docs(f085): save the R29 step block (C0a)
| Path | +/- | Reason |
| `.agent/authored/f085-r29.md` | +306/-0 | the block, sha256 5c93aff8… verified before commit |
### 5dfb8305 docs(f085): mirror the R29 block into last_block (C0b)
| Path | +/- | Reason |
| `.agent/last_block.md` | +212/-304 | written from `git show HEAD:.agent/authored/f085-r29.md` |
### e1ce0b68 docs(review): record the R28 PASS and register R-0519 (C1)
| Path | +/- | Reason |
| `.agent/live_review.md` | +69/-0 | RECORD1 appended: R28 gate entry + R-0519 |
### 1f5d58c0 docs(f085): advance the plan to R29 (C2)
| Path | +/- | Reason |
| `.agent/plan.md` | +8/-8 | PLANF→PLANT rewrite of Current Step and Next Steps |
### f62dfa88 docs(f085): record the T002b migration state in the inventory (C3)
| Path | +/- | Reason |
| `.agent/f085_inventory.md` | +16/-0 | INVF→INVT paragraph under `### test — 12` |
### this commit docs(f085): rewrite the handback for R29 (C4)
| Path | +/- | Reason |
| `.agent/handoff.md` | self-reference | a handback cannot table its own commit (R-0149); insertions are in the round report |

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a  | done   | |
| C0b  | done   | |
| C1   | done   | |
| C2   | done   | |
| C3   | done   | |
| C4   | done   | this commit |

## External actions

`git push -u origin feature/f085-sandbox-hardening` after C4 — outcome in the
round report. No `gh` command, no PR, no merge, no worktree added or removed.

## Verification

G1 STATE. `ls -la .agent/STOP` → `No such file or directory` before C0a and
again before C4. `git status --porcelain` empty at round start and after all five
commits. `git worktree list` one line: the primary checkout.
G2 TRANSPORT. Working + committed `.agent/authored/f085-r29.md` and working +
committed `.agent/last_block.md`, all four byte-EQUAL, sha256
5c93aff876b168aada846b99dcf9ff927df3f41f3329b55a7f40d353422dd813 — 18160 B, 306
lines, 10 marker lines (157, 226, 228, 244, 246, 262, 264, 276, 278, 306),
region digests 1-100 `c40e6be2`, 101-200 `23d988e4`, 201-306 `70c142ae`.
G3 APPEND SHAPE. Pre-commit blob a byte-exact PREFIX: True. Remainder equals one
blank line plus RECORD1: True. RECORD1's first line occurs 1× among the 69 added
lines. Lines matching `^(BEGIN|END)-[A-Z0-9]+$`: 0 — the bare substring `END-`
hits 9×, the prose the gate warned about. numstat `69	0	.agent/live_review.md`.
G4 ARITHMETIC. Base b0d09db4: 133 registered / 15 done / 0 landed, 118 open, max
R-0518. HEAD: 134 / 15 / 0, 119 open, max R-0519, next free R-0520. Registered
symmetric difference `['R-0519']`; done and landed symmetric differences `[]`.
Duplicate ids 0. Resolutions naming an unregistered id 0.
G5 PLAN PAIR. PLANF 0× at HEAD, PLANT 1×. `## Goal` byte-IDENTICAL to base (729
B), `## Risks` byte-IDENTICAL to base (472 B). `.agent/plan.md` sha256
baa0440f25f1856fc951868035c837aa99e60cb80e72f082e34c8375f8dea150 — 2453 B, 42
lines (under 50). `## Next Steps` parses to the numerals 1, 2, 3.
G6 INVENTORY PAIR. INVF 1× at HEAD, INVT 1× at HEAD. The 16 lines C3 adds hold
`Migration state, measured at R29:` exactly once. INVF — the `### test — 12`
heading plus its ten site lines, 11 lines, sha256 74cb89e9… — occurs 1× at base
and 1× at HEAD, so those bytes are unchanged.
numstat `16	0	.agent/f085_inventory.md`.
G7 STATE READERS, in the PRIMARY checkout (`git worktree list` one line).
`python3 -m pytest tests/orchestration/test_test_runner.py
tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
tests/ui_server/test_dashboard_contract.py -rf -q` → exit 0, reading `158 passed
in 19.71s`. CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0,
reading `42 passed in 20.25s`. No ruff and no docs gate: the change set holds no
`.py` file and nothing under `docs/`.
G8 HYGIENE, measured before C4. `git diff --name-only b0d09db4..HEAD` holds
exactly `.agent/authored/f085-r29.md`, `.agent/f085_inventory.md`,
`.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`. Per-commit
insertions 306, 212, 69, 8, 16 — none over 500; all five have one parent.
`git reflog -12 --format=%gs`: 12 entries, 0 whose action is not `commit:`.
STALENESS (constraint 8). Re-read after C3: `.agent/live_review.md`,
`.agent/plan.md`, `.agent/f085_inventory.md`, `.agent/authored/f085-r29.md`,
`.agent/last_block.md`. RECORD1's promise that C3 writes the migration state
beneath the class list is true on disk. Its two quotations name HISTORICAL
artifacts, not current wording — `Fortschritt: ~85 %` at line 5 of
`b0d09db4:.agent/handoff.md` and "ending with … `Popen`" at line 27 of
`07b1ba25:.agent/plan.md`, both verified — so C2 and C4 rewriting those files
now falsifies neither.

## Authored-text proofs

All five slices were extracted PROGRAMMATICALLY from the COMMITTED
`.agent/authored/f085-r29.md` by their marker pairs and applied byte-verbatim;
none was retyped or taken from the prompt. RECORD1 append-verified byte-exactly
(G3); PLANF matched at exactly 1 place and PLANT is 1× at HEAD (G5); INVF matched
at exactly 1 place and INVT is 1× at HEAD (G6); 0 marker lines reached any
target. The block digest was verified equal to 5c93aff8… before C0a.

## Deviations & assumptions

No departure from the ordered sequence C0a · C0b · C1 · C2 · C3 · C4: none extra,
none dropped, none reordered. No worktree created. One measurement was corrected
before being reported: the first G8 reflog predicate tested for the substring
`": commit"` and wrongly called all 12 lines non-`commit:`; rewritten as
`startswith("commit:")` and re-measured. Only the corrected reading is claimed.
Length overage declared at the top of this file.

## Next

Next session's FIRST action is Phase 1 rule 1 — re-read `.agent/STOP` from disk
— BEFORE rule 2, the Open PR Gate
(`gh pr list --state open --json number,headRefName,baseRefName,isDraft`).
R-0519 is OPEN and awaits the next reviewed round's authored resolution. R29's
own verdict is NOT a §4.13 terminator: this branch continues. The next reviewed
round records R29's gate entry in `.agent/live_review.md`. Open findings: 119.
Then T002b continued — the seven `test`-class sites still on a bare spawn, per
`.agent/plan.md` Next Steps item 1.
