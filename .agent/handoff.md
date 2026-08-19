# Handback — F085 Sandbox hardening (stage 1), R56

Feature F085 · Round R56 · Branch `feature/f085-sandbox-hardening` · Base 49a3fdcb

## Range
Review of 49a3fdcb..HEAD. SIX commits: C0a C0b C1 C2 C3 C4. The npm environment question is settled BEFORE any call site migrates; `packages/orchestration/ui_server.py` is untouched by design.

## Commits
### 27f65ce3 docs(f085): save the R56 step block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f085-r56.md` | +345/-0 | C0a — the R56 block, byte-verbatim from the reviewer's original |
### f6a36dd3 docs(f085): mirror the R56 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +244/-152 | C0b — the COMMITTED blob copied over; single-state-file rewrite |
### 9a218ec1 docs(f085): advance the plan to the R56 environment question
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +10/-12 | C1 — PLAN10F→PLAN10T, the first substantive commit; 44 lines after |
### 33c99b54 docs(f085): record the R55 PASS
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +33/-0 | C2 — RECORD24 appended; no registration line and no resolution |
### 94574142 feat(f085): widen the runtime-build env row to the npm and node config keys
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/exec_guard.py` | +17/-3 | C3 — ALLOWF→ALLOWT; the row is now the `test` base plus 8 named npm/node keys |
| `tests/orchestration/test_exec_guard.py` | +44/-0 | C3 — TESTSNPM appended; the two tests that pin both halves |
### C4 — self-reference, a handback cannot table the commit that writes it
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | in the round report | C4 — this file; its own insertions go to the operator |

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |

## External actions
`git push -u origin feature/f085-sandbox-hardening` after C4; outcome reported to the operator. No PR, no merge, no other `gh` call, no worktree add and no worktree remove.

## Verification
G1 STATE — `.agent/STOP` absent before C0a and again before C4 (`Path.exists()` False at both points); `git status --porcelain` EMPTY at round start and after each of the five commits preceding this one, whose own post-commit reading goes to the operator; `git worktree list` one line throughout; `git ls-files .remedy-wt` empty.
G2 TRANSPORT — the committed `.agent/authored/f085-r56.md`, the committed `.agent/last_block.md`, BOTH working copies and the reviewer's `.remedy-wt/f085-r56.md` are all five byte-EQUAL, disk-to-disk and not by digest fallback: sha256 1a9fcbdbd41463fd0fcd2116837d2ec6dec100304614149609db5b467a33cb82, 24319 B, 345 lines, 12 marker lines — every figure measured on every copy.
G3 SHAPES — REWRITE 1, PLAN10F→PLAN10T on `.agent/plan.md` at 9a218ec1: FROM 1x in the pre-commit blob, FROM 0x and TO exactly 1x after, numstat `10 12`. REWRITE 2, ALLOWF→ALLOWT on `packages/orchestration/exec_guard.py` at 94574142: FROM 1x before, FROM 0x and TO exactly 1x after, numstat `17 3`. PROSE APPEND, C2 / RECORD24 / `.agent/live_review.md` at 33c99b54: byte-exact PREFIX, remainder exactly one blank line plus the slice, exact SUFFIX, 0 marker LINES in the file, and each of the slice's 32 non-empty lines (all 32 of its lines are non-empty) occurring exactly once among the 33 lines that commit adds to that path, numstat `33 0`. CODE APPEND, C3 / TESTSNPM / `tests/orchestration/test_exec_guard.py` at 94574142: byte-exact PREFIX, remainder exactly one blank line plus the slice, exact SUFFIX, 0 marker LINES, and the 44 lines that commit adds to that path are exactly one blank line followed by the slice's 43 lines IN ORDER, numstat `44 0`.
G4 SUITES — primary checkout, never a worktree, each exit 0. `python3 -m pytest tests/orchestration/test_exec_guard.py -rf -q`: `35 passed in 14.27s` against the base 33, which is the base plus this round's two tests. `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q`: `159 passed in 20.90s` against the base 159. CANARY `python3 -m pytest tests/cli/test_golden_path.py -q`: `42 passed in 22.15s` against the base 42.
G5 LINT — `python3 -m ruff check packages/orchestration/exec_guard.py tests/orchestration/test_exec_guard.py`, the repository's own `pyproject.toml` and no `--isolated` flag: `All checks passed!`, exit 0.
G6 PLAN CONTRACT — `.agent/plan.md` after C1 is 44 lines against the 50-line cap, the figure the block projected; contains `## Goal` true, contains `## Next Steps` true, matches `\bF\d{3}\b` true.
G7 ARITHMETIC — 172 registered / 27 done / 0 landed at 49a3fdcb and 172 / 27 / 0 at HEAD; 145 open at both; max registered R-0557 and max resolved R-0532 at both; ALL THREE symmetric differences EMPTY; 0 duplicate ids and 0 resolutions naming an unregistered id at both SHAs; next free id R-0558.
G8 HYGIENE — measured BEFORE C4: `git diff --name-only 49a3fdcb..HEAD` holds exactly `.agent/authored/f085-r56.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `packages/orchestration/exec_guard.py` and `tests/orchestration/test_exec_guard.py` and nothing else; it does NOT hold `packages/orchestration/ui_server.py`. Per-commit INSERTIONS 345, 244, 10, 33, 61 — none over 500, so the oversize allowance spent at d4473f85 stays untouched. Every commit has exactly one parent, the tree is clean and `git worktree list` is one line.
BLOCK SIZE, re-measured from the committed `.agent/authored/f085-r56.md`: TOTAL 345 against the 490 cap ruled by DECISION F085 D6, PROSE 194 against 400 (345 minus the 151 slice-body lines, so marker lines count as prose), RECORD24 32 against 140 — all three agree with the figures constraint 9 states.

## Authored-text proofs
Every slice was extracted PROGRAMMATICALLY by its marker pair out of the committed `.agent/authored/f085-r56.md` under that block's CONVENTION; none was retyped, reflowed or taken from the delegation prompt. All six were used — PLAN10F and ALLOWF each matched their target exactly 1x, and PLAN10T, ALLOWT, TESTSNPM and RECORD24 were written. The disk-to-disk comparison result is G2 above; 0 marker LINES reached any target file.

## Deviations & assumptions
No departure from the block's ordered commit sequence: C0a C0b C1 C2 C3 C4 ran in that order with no extra commit, no dropped commit and no reordering. NO ASSUMPTION ABOUT SLICE SHAPE WAS NEEDED: the CONVENTION states newline-inclusion, so both appends held as `post == pre + "\n" + slice` byte-exactly with no further joiner and no terminator added. DECLARED, since the change set says "nothing else": the extraction, application and measurement ran as `python3 - <<'PY'` heredocs, and the only file written outside the change set is a handback draft under the gitignored `.remedy-wt/`, which `git ls-files .remedy-wt` shows is untracked and which is not the reviewer's block file. No red control and no destructive check was ordered or run, so no worktree was created and none was removed. This round REGISTERED NOTHING and RESOLVED NOTHING, as constraint 7 orders. Deviations, declared — DECISION D15 stated cause: this file is 75 lines, inside the ≤100-line allowance a six-commit round carries, but 8555 B ≈ 2.1k tokens against the handback template's ≤800-token hard cap. The cause is MANDATED content only: six per-commit changed-files tables, the item-status table, an eight-entry verification transcript covering two rewrite pairs, two appends, three suites and a lint gate, and the four verbatim Fortschritt lines. No section was dropped and no transcript was padded; the R55 handback at 49a3fdcb carried the same reading at ≈1.9k tokens.

## Fortschritt
Fortschritt: ~94 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R55 PASS ·
T002a KOMPLETT · T002b KOMPLETT · T002c KOMPLETT · T002d zur Hälfte — Naht, Extraktion und die
Umgebungszeile gebaut, die fünf Call-Sites offen · T003 offen) — Schätzung, gegen die
Klassentabelle aus Amendment F085 D1 gemessen.

## Next
ONE: the next round is R57, which migrates the two `runtime-build` call sites in `_auto_build_frontend` (`packages/orchestration/ui_server.py`) onto `run_guarded_runtime_build_command` with `check=True`, now that the row those sites will run under answers the environment question. Then the three `runtime-server` sites, then T003, the integration gate and closure.
TWO: R56's own verdict is NOT on disk as a gate entry, because the round that records a verdict cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13) — that absence is the terminator, and R57 must not open a repair round to close it.
THREE: 145 findings are open and R-0558 is the next free id.
FOUR: Phase 1 rule 1 first: re-read `.agent/STOP` from disk — the self-drive protocol requires every handoff that names the next session's first action to put that rule ahead of the PR Gate.
