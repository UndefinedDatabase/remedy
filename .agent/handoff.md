# Handback — F085 Sandbox hardening (stage 1), R55

Feature F085 · Round R55 · Branch `feature/f085-sandbox-hardening` · Base 1812c219

## Range
Review of 1812c219..HEAD. FIVE commits: C0a C0b C1 C2 C3. A RECORD round — `.agent/**` only, no production code, no test, nothing registered and nothing resolved.

## Commits
### c2a7e52b docs(f085): save the R55 step block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f085-r55.md` | +253/-0 | C0a — the R55 block, byte-verbatim from the reviewer's original |
### 0c6db7cc docs(f085): mirror the R55 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +174/-411 | C0b — the COMMITTED blob copied over; single-state-file rewrite |
### e02f0dcc docs(f085): advance the plan to the R56 migration
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +12/-7 | C1 — PLAN9F→PLAN9T, the first substantive commit; 46 lines after |
### 2bb63069 docs(f085): record the R54 PASS
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +47/-0 | C2 — RECORD23 appended; no registration line and no resolution |
### C3 — self-reference, a handback cannot table the commit that writes it
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | in the round report | C3 — this file; its own insertions go to the operator |

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | this commit |

## External actions
`git push -u origin feature/f085-sandbox-hardening` after C3; outcome reported to the operator. No PR, no merge, no other `gh` call, no worktree add and no worktree remove.

## Verification
G1 STATE — `.agent/STOP` absent before C0a and again before C3 (`ls` exit 2 at both points); `git status --porcelain` EMPTY at round start and after each of the four commits preceding this one, whose own post-commit reading goes to the operator; `git worktree list` one line throughout.
G2 TRANSPORT — exit 0. The committed `.agent/authored/f085-r55.md`, the committed `.agent/last_block.md`, BOTH working copies and the reviewer's `.remedy-wt/f085-r55.md` are all five byte-EQUAL, disk-to-disk and not by digest fallback: sha256 dfcb54609904651d7d882c01e83ade3712e1ab8a42355b62199a4271a89f665e, 19014 B, 253 lines, 6 marker lines — every figure measured on every copy.
G3 SHAPES — THE REWRITE, over its own post-commit file: PLAN9F→PLAN9T at e02f0dcc, `TO contains FROM: false`, FROM 1x in the pre-commit blob, FROM 0x and TO exactly 1x after, numstat `12 7`. THE PROSE APPEND, C2 / RECORD23 / `.agent/live_review.md` at 2bb63069: byte-exact PREFIX, remainder exactly one blank line plus the slice, exact SUFFIX, 0 marker LINES, and each of the slice's 46 non-empty lines (all 46 of its lines are non-empty) occurring exactly once among the 47 lines that commit adds to that path, numstat `47 0`.
G4 STATE READERS — `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q`, primary checkout and no worktree: `159 passed in 19.96s`, exit 0, against the base 159. CANARY `python3 -m pytest tests/cli/test_golden_path.py -q`: `42 passed in 20.47s`, exit 0, against the base 42.
G5 PLAN CONTRACT — `.agent/plan.md` after C1 is 46 lines against the 50-line cap, the figure constraint 7 projected; contains `## Goal` true, contains `## Next Steps` true, matches `\bF\d{3}\b` true.
G6 ARITHMETIC — 172 registered / 27 done / 0 landed at 1812c219 and 172 / 27 / 0 at HEAD; 145 open at both; max registered R-0557 and max resolved R-0532 at both; ALL THREE symmetric differences EMPTY; 0 duplicate ids and 0 resolutions naming an unregistered id at both SHAs; next free id R-0558.
G7 HYGIENE — measured BEFORE C3: `git diff --name-only 1812c219..HEAD` holds exactly `.agent/authored/f085-r55.md`, `.agent/last_block.md`, `.agent/plan.md` and `.agent/live_review.md` and nothing else, and holds NO path under `packages/` or `tests/`. Per-commit INSERTIONS 253, 174, 12, 47 — none over 500, so the oversize allowance spent at d4473f85 stays untouched. Every commit has exactly one parent, the tree is clean and `git worktree list` is one line.
BLOCK SIZE, re-measured from the committed `.agent/authored/f085-r55.md`: TOTAL 253 against the 490 cap ruled by DECISION F085 D6, PROSE 158 against 400 (253 minus the 95 slice-body lines, so marker lines count as prose), RECORD23 46 against 140 — all three agree with the figures constraint 9 states.

## Authored-text proofs
Every slice was extracted PROGRAMMATICALLY by its marker pair out of the committed `.agent/authored/f085-r55.md` under that block's CONVENTION; none was retyped, reflowed or taken from the delegation prompt. All three were used — PLAN9F matched its target exactly 1x, PLAN9T and RECORD23 were written. The disk-to-disk comparison result is G2 above; 0 marker LINES reached any target file.

## Deviations & assumptions
No departure from the block's ordered commit sequence: C0a C0b C1 C2 C3 ran in that order with no extra commit, no dropped commit and no reordering. NO ASSUMPTION ABOUT SLICE SHAPE WAS NEEDED: the CONVENTION states newline-inclusion, so the append held as `post == pre + "\n" + slice` byte-exactly with no further joiner and no terminator added. DECLARED, since the change set says "nothing else": the extraction, application and measurement ran as `python3 - <<'PY'` heredocs, so no helper script was written to disk anywhere and `git status --porcelain` is empty. No red control and no destructive check was ordered or run, so no worktree was created and none was removed. This round REGISTERED NOTHING and RESOLVED NOTHING, as constraint 7 orders.
Deviations, declared — DECISION D15 stated-cause overage: this file is 69 lines against the ≤60 cap a five-commit round carries. The cause is MANDATED content only: the five per-commit changed-files tables (20 lines), the item-status table (7 lines), the eight-entry verification transcript and the four verbatim Fortschritt lines. No section was dropped and no transcript was padded.

## Fortschritt
Fortschritt: ~93 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R54 PASS ·
T002a KOMPLETT · T002b KOMPLETT · T002c KOMPLETT · T002d zur Hälfte — Naht und Extraktion gebaut,
die fünf Call-Sites offen · T003 offen) — Schätzung, gegen die Klassentabelle aus
Amendment F085 D1 gemessen.

## Next
ONE: the next round is R56, which migrates the two `runtime-build` call sites in `_auto_build_frontend` (`packages/orchestration/ui_server.py`) onto `run_guarded_runtime_build_command` with `check=True`, and must FIRST settle the environment question `.agent/plan.md` now carries as a risk. Then the three `runtime-server` sites, then T003, the integration gate and closure.
TWO: R55's own verdict is NOT on disk as a gate entry, because the round that records a verdict cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13) — that absence is the terminator, and R56 must not open a repair round to close it.
THREE: 145 findings are open and R-0558 is the next free id.
FOUR: Phase 1 rule 1 first: re-read `.agent/STOP` from disk — the self-drive protocol requires every handoff that names the next session's first action to put that rule ahead of the PR Gate.
