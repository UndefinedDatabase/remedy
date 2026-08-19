# Handback — F085 Sandbox hardening (stage 1), R57

Feature F085 · Round R57 · Branch `feature/f085-sandbox-hardening` · Base 3bb82a25

## Range
Review of 3bb82a25..HEAD. SEVEN commits: C0a C0b C1 C2 C3 C4 C5. A REPAIR round: the defect R56 landed is one missing blank line in a test file, so this round registers R-0558, adds the blank line and records the R56 FAIL. `packages/orchestration/exec_guard.py` and `packages/orchestration/ui_server.py` are untouched by design.

## Commits
### 36704887 docs(f085): save the R57 step block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f085-r57.md` | +298/-0 | C0a — the R57 block, byte-verbatim from the reviewer's original |
### df6936de docs(f085): mirror the R57 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +203/-250 | C0b — the COMMITTED blob copied over; single-state-file rewrite |
### ddd4f8b8 docs(f085): advance the plan to the R57 repair
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +5/-5 | C1 — PLAN11F→PLAN11T, the first substantive commit; 44 lines after |
### a6c5176f docs(f085): record the R56 FAIL and register R-0558
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +59/-0 | C2 — RECORD25 appended; registers R-0558 and resolves nothing |
### 356a1568 fix(f085): restore the two-blank-line separation before the npm key set
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_exec_guard.py` | +1/-0 | C3 — FIXBLANKF→FIXBLANKT; exactly one newline byte, no code touched |
### 847af55f docs(f085): note R-0558 landed in the R57 blank-line fix
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-0 | C4 — the worker's single `Landed:` line naming C3's SHA, plus its blank separator |
### C5 — self-reference, a handback cannot table the commit that writes it
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | in the round report | C5 — this file; its own insertions go to the operator |

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit |

## External actions
`git push -u origin feature/f085-sandbox-hardening` after C5; outcome reported to the operator. No PR, no merge, no other `gh` call, no worktree add and no worktree remove.

## Verification
G1 STATE — `.agent/STOP` absent before C0a and again before C5 (`Path.exists()` False at both points); `git status --porcelain` EMPTY at round start and after each of the six commits preceding this one, whose own post-commit reading goes to the operator; `git worktree list` one line throughout; `git ls-files .remedy-wt` empty.
G2 TRANSPORT — the committed `.agent/authored/f085-r57.md`, the committed `.agent/last_block.md`, BOTH working copies and the reviewer's `.remedy-wt/f085-r57.md` are all five byte-EQUAL, disk-to-disk and not by digest fallback: sha256 d186ed7740849c36c93e83bcc6ae3509ae820d743aa0eb7d06d3e575a7a18b74, 22571 B, 298 lines, 10 marker lines — every figure measured on every copy.
G3 SHAPES — REWRITE 1, PLAN11F→PLAN11T on `.agent/plan.md` at ddd4f8b8: `TO contains FROM: false`, FROM 1x in the pre-commit blob, FROM 0x and TO exactly 1x after, numstat `5 5`. REWRITE 2, FIXBLANKF→FIXBLANKT on `tests/orchestration/test_exec_guard.py` at 356a1568: `TO contains FROM: false`, FROM 1x before, FROM 0x and TO exactly 1x after, numstat `1 0`; the file goes 29917 B / 731 lines to 29918 B / 732 lines, so the whole effect is one newline byte. PROSE APPEND, C2 / RECORD25 / `.agent/live_review.md` at a6c5176f: byte-exact PREFIX, remainder exactly one blank line plus the slice, exact SUFFIX, 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` in the file, and each of the slice's 57 non-empty lines occurring exactly once among the 59 lines that commit adds to that path, numstat `59 0`.
G4 SUITES — primary checkout, never a worktree, each exit 0. `python3 -m pytest tests/orchestration/test_exec_guard.py -rf -q`: `35 passed in 14.26s`, the expected 35 since the round ships and deletes no test. `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q`: `159 passed in 19.78s` against the base 159. CANARY `python3 -m pytest tests/cli/test_golden_path.py -q`: `42 passed in 20.26s` against the base 42.
G5 LINT — both halves over the same two paths, the repository's own `pyproject.toml`, no `--isolated`. `python3 -m ruff check packages/orchestration/exec_guard.py tests/orchestration/test_exec_guard.py`: exit 0, `All checks passed!` — the blind gate, green before and after. `python3 -m ruff check --preview packages/orchestration/exec_guard.py tests/orchestration/test_exec_guard.py` AFTER C3: exit 0, `All checks passed!`. The worker also ran that exact preview command once BEFORE C3 and reproduced the reviewer's red: exit 1, `Found 1 error.`, `error[E305][*]: Expected 2 blank lines after class or function definition, found (1)` at `tests/orchestration/test_exec_guard.py:691:1`, `[*] 1 fixable with the --fix option.` — `--fix` was NOT run, per constraint 9, and no preview finding anywhere else in the repository was touched.
G6 PLAN CONTRACT — `.agent/plan.md` after C1 is 44 lines against the 50-line cap, the figure the block projected; contains `## Goal` true, contains `## Next Steps` true, matches `\bF\d{3}\b` true.
G7 ARITHMETIC — 172 registered / 27 done / 0 landed and 145 open at 3bb82a25; 173 / 27 / 1 and 146 open at HEAD. Registered symmetric difference exactly `{R-0558}`, landed symmetric difference exactly `{R-0558}`, done symmetric difference EMPTY. Max registered R-0557 at base and R-0558 at HEAD; max resolved R-0532 at both; 0 duplicate ids and 0 resolutions naming an unregistered id at both SHAs; next free id R-0559.
G8 HYGIENE — measured BEFORE C5: `git diff --name-only 3bb82a25..HEAD` holds exactly `.agent/authored/f085-r57.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md` and `tests/orchestration/test_exec_guard.py` and nothing else; it holds NEITHER `packages/orchestration/exec_guard.py` NOR `packages/orchestration/ui_server.py`. Per-commit INSERTIONS 298, 203, 5, 59, 1, 2 — none over 500, so the oversize allowance spent at d4473f85 stays untouched. Every commit has exactly one parent, the tree is clean and `git worktree list` is one line.
BLOCK SIZE, re-measured from the committed `.agent/authored/f085-r57.md`: TOTAL 298 against the 490 cap ruled by DECISION F085 D6, PROSE 199 against 400 (298 minus the 99 slice-body lines, so marker lines count as prose), RECORD25 58 against 140 — all three agree with the figures constraint 10 states.

## Authored-text proofs
Every slice was extracted PROGRAMMATICALLY by its marker pair out of the committed `.agent/authored/f085-r57.md` under that block's CONVENTION; none was retyped, reflowed or taken from the delegation prompt. All five were used — PLAN11F and FIXBLANKF each matched their target exactly 1x, and PLAN11T, FIXBLANKT and RECORD25 were written. FIXBLANK was applied as a byte-level replace of the exact extracted FROM by the exact extracted TO, never by an editor insert: FROM is 142 B and TO is 143 B. The disk-to-disk comparison result is G2 above; 0 marker LINES reached any target file. The only text the WORKER authored is C4's single `Landed: R-0558 — …` line, per constraint 7; no `Done:` paragraph was written.

## Deviations & assumptions
No departure from the block's ordered commit sequence: C0a C0b C1 C2 C3 C4 C5 ran in that order with no extra commit, no dropped commit and no reordering. NO ASSUMPTION ABOUT SLICE SHAPE WAS NEEDED: the CONVENTION states newline-inclusion, so both rewrites held as exact byte replacements and RECORD25 held as `post == pre + "\n" + slice` byte-exactly, with no joiner and no terminator added. DECLARED, since the change set says "nothing else": the extraction, application and measurement ran as `python3 - <<'PY'` heredocs, and the only file written outside the change set is this handback's draft under the gitignored `.remedy-wt/`, which `git ls-files .remedy-wt` shows untracked and which is not the reviewer's block file. DECLARED as an EXTRA, unordered reading, not a scope widening: the pre-C3 `--preview` run recorded under G5, which is read-only and changed nothing. `python3 -m ruff --fix` was never run, nothing was reformatted, and the 634 preview findings elsewhere in the repository were not touched. No red control and no destructive check was ordered or run, so no worktree was created and none was removed. This round REGISTERED R-0558 and RESOLVED NOTHING, as constraint 8 orders. Deviations, declared — DECISION D15 stated cause: this file is 79 lines, inside the ≤100-line allowance a seven-commit round carries, but ≈2.5k tokens against the handback template's ≤800-token hard cap. The cause is MANDATED content only: seven per-commit changed-files tables, the seven-row item-status table, a G1-G8 verification transcript that carries BOTH halves of G5 including the pre-fix red output this round exists to remove, the block-size re-measurement and the four verbatim Fortschritt lines. No section was dropped and no transcript was padded.

## Fortschritt
Fortschritt: ~94 % (T001 gebaut · R13-R55 PASS · R56 FAIL, an R57 repariert · T002a KOMPLETT ·
T002b KOMPLETT · T002c KOMPLETT · T002d zur Hälfte — Naht, Extraktion und die Umgebungszeile
gebaut, die fünf Call-Sites offen · T003 offen) — Schätzung, gegen die Klassentabelle aus
Amendment F085 D1 gemessen.

## Next
ONE: the next round is R58, which migrates the two `runtime-build` call sites in `_auto_build_frontend` (`packages/orchestration/ui_server.py`) onto `run_guarded_runtime_build_command` with `check=True`. Then the three `runtime-server` sites, then T003, the integration gate and closure.
TWO: R58 also carries the reviewer-authored `Done: R-0558` that resolves this round's finding, replacing the `Landed:` line C4 writes, and the R57 verdict, because the round that records a verdict cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13).
THREE: 146 findings are open and R-0559 is the next free id.
FOUR: Phase 1 rule 1 first: re-read `.agent/STOP` from disk — the self-drive protocol requires every handoff that names the next session's first action to put that rule ahead of the PR Gate.
