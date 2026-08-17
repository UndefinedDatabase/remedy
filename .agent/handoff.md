# Handback — F085 Sandbox hardening (stage 1), R32

Feature F085 · Round R32 · Branch `feature/f085-sandbox-hardening` · Base SHA 16234fbf

## Range

Review of 16234fbf..HEAD

## Commits

### a3b5cf95 docs(f085): save the R32 step block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f085-r32.md` | +400/-0 | C0a — the R32 block saved byte-for-byte |

### e766b6b4 docs(f085): mirror the R32 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +288/-240 | C0b — the identical bytes mirrored |

### 94e70839 docs(review): promote the slice-fact rule into the pre-emission checklist
| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | +16/-0 | C1 — ITEM20F→ITEM20T; item 20 lands after item 19 |

### ce69c39a docs(review): record the R31 PASS and resolve R-0520
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +55/-0 | C2 — RECORD1 appended: the R31 gate entry and the R-0520 resolution |

### ed88be4c feat(f085): move the integrity gate collect-only spawn onto the guarded seam
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/integrity_gate.py` | +13/-3 | C3 — IGIMPT, IGSPAWNT, IGERRT; `cwd=None` kept deliberately |
| `tests/orchestration/test_integrity_gate.py` | +28/-0 | C3 — TESTIG pins the seam, the args and the bytes decode |

### d2c45c23 docs(f085): advance the plan to R32
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +12/-9 | C4 — PLANF→PLANT; 46 lines, under the 50-line cap |

### (this commit) docs(f085): rewrite the handback for R32
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | C5 — this file; a handback cannot table the commit that writes it (R-0149), so its own insertion count is reported in the round report |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |

## External actions

- `git worktree add .remedy-wt/r32-red HEAD --detach` → created, detached at ed88be4c (G7 red proof only)
- `git worktree remove --force .remedy-wt/r32-red` + `git worktree prune` → removed before C4; `git worktree list` is one line
- `git push -u origin feature/f085-sandbox-hardening` → runs immediately after this commit; its outcome is in the round report
- No PR, no merge, no `gh` command.

## Verification

G1 STATE — exit 0. `git status --porcelain` empty at round start and after each of the six commits. `.agent/STOP` absent before C0a and again before C5 (`ls .agent/STOP` exit 2, "No such file or directory"). `git worktree list` one line at the handback.

G2 TRANSPORT — exit 0. The committed `.agent/authored/f085-r32.md`, the committed `.agent/last_block.md` and BOTH working copies are all four byte-EQUAL: sha256 75deb8c5d666fc2f4053583eb8c4a3d94dd2db8f52c227df2a22b2392cf1e686, 23119 B, 400 lines, 24 marker lines, region digests 1-100 eb26791d, 101-200 656230ba, 201-400 0d724fc0. Measured, not hand-computed.

G3 APPEND SHAPE (C2) — exit 0. The pre-commit blob of `.agent/live_review.md` is a byte-exact PREFIX of the post-commit file; the remainder is 4361 B = 1 newline + RECORD1's 4360 B, and RECORD1 is an exact suffix. RECORD1's first line occurs once among the 55 lines the commit ADDS. 0 lines match `^(BEGIN|END)-[A-Z0-9]+$` in that file, while the substring `END-` hits 12 times in its prose. `git show --numstat`: `55  0  .agent/live_review.md`.

G4 ARITHMETIC — exit 0. Base 16234fbf: 135 registered / 16 done / 0 landed, 119 open, max registered R-0520, max resolved R-0519 — reproduces the reviewer's base reading. HEAD: 135 / 17 / 0, 118 open, both maxima R-0520. Registered symmetric difference EMPTY; done symmetric difference exactly {R-0520}; landed symmetric difference empty; 0 duplicate ids; 0 resolutions naming an unregistered id; max id R-0520; next free R-0521 at both ends.

G5 CHECKLIST ITEM (HEAD after C1) — exit 0. In `docs/agents/planner_reviewer_prompt.md` the item-20 opener occurs exactly once (line 381), the closing paragraph opener `  Why this is on disk and not a habit: item 2 has recurred six times across` occurs exactly once, and 0 lines match `^(BEGIN|END)-[A-Z0-9]+$`. The item-20 opener occurs once among the lines C1 ADDS and is the first of them. `git show --numstat`: `16  0  docs/agents/planner_reviewer_prompt.md`.

G6 MIGRATION PAIRS (HEAD after C3) — exit 0. In `packages/orchestration/integrity_gate.py`: IGSPAWNF 0x, IGERRF 0x, IGSPAWNT 1x, IGERRT 1x, IGIMPT 1x. `from packages.orchestration.exec_guard import run_guarded_test_command` occurs once among the 13 lines C3 ADDS to that file. `import subprocess` still occurs exactly once as a whole line — the `git ls-files` call in `_check_relevant_untracked` still needs it. `def test_collect_only_runs_on_the_guarded_seam(monkeypatch):` occurs once among the 28 lines C3 ADDS to `tests/orchestration/test_integrity_gate.py`. 0 marker lines reached either file. `git show --numstat`: `13  3  packages/orchestration/integrity_gate.py` and `28  0  tests/orchestration/test_integrity_gate.py`.

G7 THE MIGRATION IS REAL, PROVED TWICE.
- Round gate, PRIMARY checkout: `python3 -m pytest tests/orchestration/test_integrity_gate.py -q -rf` → exit 0, `16 passed in 0.27s`. READING, not a target; the reviewer's base reading at 16234fbf was `15 passed`, and the difference is the one node C3 adds.
- Behaviour equality, PRIMARY checkout: `python3 -c "from packages.orchestration.integrity_gate import _check_collect_only as c; r=c(); print(r.name, r.status, r.message)"` → exit 0, prints `collect_only IntegrityStatus.PASS pytest collection passed`. Identical to the reviewer's reading of the UNMIGRATED function at 16234fbf: the guard's allowlist does not starve a real collection.
- RED PROOF, disposable worktree `.remedy-wt/r32-red` at ed88be4c, never the primary checkout. The guarded call was replaced by the bare `subprocess.run([...], capture_output=True, text=True, timeout=120)`, the import and the decode branch left standing. `python3 -m pytest tests/orchestration/test_integrity_gate.py -q -rf` → exit 1, `1 failed, 15 passed in 19.27s`. Failing node: `tests/orchestration/test_integrity_gate.py::test_collect_only_runs_on_the_guarded_seam`. Exception text: `AssertionError: assert {} == {'cmd': ['bash', 'scripts/remedy_pytest.sh', 'tests/', '--collect-only', '-q'], 'cwd': None, 'timeout_sec': 120}` at `tests/orchestration/test_integrity_gate.py:235` — the monkeypatched seam is never entered, so `seen` stays empty. Worktree removed and pruned before C4.

G8 LINT AND STATE READERS, all in the PRIMARY checkout.
- `python3 -m ruff check packages/orchestration/integrity_gate.py tests/orchestration/test_integrity_gate.py` (repository configuration, no `--isolated`) → exit 0, `All checks passed!`.
- `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q` → exit 0, `159 passed in 20.30s`. Base reading `158 passed`; the +1 is the node C3 adds. No red, so R-0518's `node_modules` case did not arise.
- `python3 -m pytest tests/docs/ -q` → exit 0, `295 passed in 0.51s` (base `295 passed`).
- CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, `42 passed in 22.25s` (base `42 passed`).

G9 COMMIT HYGIENE — exit 0, measured BEFORE C5. `git diff --name-only 16234fbf..HEAD` holds exactly `.agent/authored/f085-r32.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `docs/agents/planner_reviewer_prompt.md`, `packages/orchestration/integrity_gate.py`, `tests/orchestration/test_integrity_gate.py` — the declared change set minus `.agent/handoff.md`, which C5 writes. Per-commit insertions: 400, 288, 16, 55, 41, 12; none exceeds 500. All six commits have exactly one parent. `git reflog -10` holds only `commit:` entries.

## Authored-text proofs

Every slice was extracted PROGRAMMATICALLY from the committed `.agent/authored/f085-r32.md` by its `BEGIN-<NAME>`/`END-<NAME>` pair; none was retyped and none came from the delegation prompt. Each FROM matched at exactly one place in its target before replacement: ITEM20F 1x, IGIMPF 1x, IGSPAWNF 1x, IGERRF 1x, PLANF 1x. At HEAD each TO occurs exactly once: ITEM20T, IGIMPT, IGSPAWNT, IGERRT, PLANT. TESTIG is an exact byte suffix of `tests/orchestration/test_integrity_gate.py` and RECORD1 an exact byte suffix of `.agent/live_review.md`. 0 marker lines reached any target file.

## Staleness sweep (constraint 8)

Re-read after C4: `docs/agents/planner_reviewer_prompt.md`, `.agent/live_review.md`, `packages/orchestration/integrity_gate.py`, `tests/orchestration/test_integrity_gate.py`, `.agent/plan.md`, `.agent/last_block.md`, `.agent/authored/f085-r32.md`.

- RECORD1's claim that the promoted rule is checklist item 20 HOLDS at HEAD: item 20 sits at line 381 of `docs/agents/planner_reviewer_prompt.md`, directly after item 19 at line 370, and no item 21 exists. The load-bearing order held — C1 is 94e70839, C2 is ce69c39a.
- OBSERVED FALSIFICATION, reported and NOT repaired. RECORD1's R31 gate entry states that `builder_bridge.py`, `ci_run.py`, `integrity_gate.py` and `mission_state.py` "each show 0 references to `run_guarded_test_command` at HEAD". That reading is true at 16234fbf — the HEAD the entry's own `d4fe1674..HEAD` range names — and C3 of THIS round falsified it for one of its four names: `packages/orchestration/integrity_gate.py` now holds 2 references, while `builder_bridge.py`, `ci_run.py` and `mission_state.py` still hold 0. This is the R-0520 class occurring inside the slice that resolves R-0520. Constraint 1 forbids editing a slice and constraint 7 forbids improvising a repair, so nothing was changed; per the counter-measure the correction belongs in a later appended entry.
- The R31 entry's other content claim reproduces: `job_promote.py` and `pingpong_promote.py` reference `run_guarded_test_command` twice each at HEAD.
- `.agent/plan.md`'s remaining-sites sentence holds at HEAD: `builder_bridge.py`, `ci_run.py` and `mission_state.py` show 0 references each.

## Deviations & assumptions

The ordered commit sequence C0a · C0b · C1 · C2 · C3 · C4 · C5 was followed exactly: no extra commit, none dropped, no reordering. C1 precedes C2 as constraint 10 requires.

DECLARED OVERAGE: this handback is 128 lines against the ≤100-line cap (AGENTS.md D15, stated-cause overage). The cause is mandated content only — seven per-commit changed-files tables, the item-status table, the nine gate transcripts with their exit codes and decisive lines, the authored-text proofs and the constraint-8 staleness sweep. No section was dropped and no transcript was padded.

## Open findings

118 open — 135 registered, 17 resolved (`Done:`), 0 landed. Next free id R-0521.

## Fortschritt

Fortschritt: ~70 % (T001 gebaut · R13-R31 PASS · T002a KOMPLETT · T002b 9 von 12
Sites auf dem Seam, 3 offen · T002c-d, T003 offen) — Schätzung, gegen die
Klassentabelle aus Amendment F085 D1 gemessen.

## Next

The next session's FIRST action is Phase 1 rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2, the Open PR Gate (`gh pr list --state open --json number,headRefName,baseRefName,isDraft`).

R32's own verdict is NOT a §4.13 terminator: this branch continues. The next reviewed round records R32's gate entry in `.agent/live_review.md`.

The single expected next action: the reviewer reviews 16234fbf..HEAD, re-runs G1-G9 itself and issues the R32 verdict.
