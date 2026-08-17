# Handback — F085 Sandbox hardening (stage 1) · Runde 36 (T002b migration)

Branch: feature/f085-sandbox-hardening · Base SHA: 23b5fcd9 · HEAD: this commit (C4).
Fortschritt: ~72 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R35
PASS · T002a KOMPLETT · T002b 10 von 12 Sites auf dem Seam, 2 offen · T002c-d, T003
offen) — Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

## Range
Review of 23b5fcd9..HEAD.

## Commits

### 8a0766c1 docs(f085): save the R36 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r36.md | +400/-0 | C0a — block saved byte-for-byte |

### 3a3060b3 docs(f085): mirror the R36 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +361/-292 | C0b — full replacement with the same bytes |

### e27c1c61 docs(review): record the R35 PASS and register R-0526
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +47/-0 | C1 — RECORD4 appended (R35 gate entry + R-0526) |

### 83bc6df1 feat(f085): put the mission verify runner on the guarded seam
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/mission_state.py | +8/-6 | C2 — M1 import, M3 docstring, M2 closure |
| tests/orchestration/test_mission_state.py | +26/-0 | C2 — T1, the first test reaching the default closure |

### 405b8fe3 docs(f085): advance the plan to R36
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +8/-9 | C3 — PLANF4->PLANT4 applied |

### C4 (this commit) docs(f085): rewrite the handback for R36
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | full rewrite | C4 — this handback; a handoff cannot table the commit that writes it (R-0149). Its own insertions are reported in the round report, per checklist item 14. |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |

## External actions
`git worktree add --detach .remedy-wt/g8-r36 83bc6df1` — created for G8 only; `git worktree remove --force` + `git worktree prune` — removed, `git worktree list` back to 1 line before C4. `git push -u origin feature/f085-sandbox-hardening` — outcome in the round report (run after this commit). No PR, no merge, no gh command.

## Verification
G1 STATE — `.agent/STOP` absent before C0a and again before C4 (re-read from disk both times, `ls` exit 2 both times). `git status --porcelain` = 0 lines at round start and after every commit. `git worktree list` = 1 line at round start and 1 line again after G8.
G2 TRANSPORT — the committed `.agent/authored/f085-r36.md`, the committed `.agent/last_block.md` and BOTH working copies are byte-EQUAL, all four measured. sha256 208ad9d39755891b5bb83f9382e6f3d613c97cafc4652ad2b8b662887d3ce8d1 · 24223 B · 400 lines · 22 marker lines. Region digests, trailing newlines included: 1-100 7d583ed088d96c3245a051f35151a7838b072899a73a6d93e0017ce88be36361, 101-200 ace9d81332b444d2402949aadc266459b64fb48195022325093b586a852b0130, 201-400 9b5a96536a6ac44deefe8959b01f216696f2fd1d6cd968c8eaeaa515ab420055.
G3 APPEND SHAPE for e27c1c61 — pre-commit blob 387274 B is a byte-exact PREFIX of the 391135 B post-commit file; remainder 3861 B = exactly one blank line plus RECORD4; RECORD4 is an exact suffix; its first line occurs 1x among the 47 lines the diff ADDS; 0 lines match `^(BEGIN|END)-[A-Z0-9]+$` while the BEGIN substring occurs 13x. `git show --numstat` = 47 0 .agent/live_review.md.
G4 ARITHMETIC — base 23b5fcd9: 140 registered / 22 done / 0 landed, 118 open, max registered R-0525, max resolved R-0525. HEAD: 141 / 22 / 0, 119 open, max registered R-0526, max resolved STILL R-0525. Registered symmetric difference {R-0526}; done symmetric difference empty; landed symmetric difference empty; 0 duplicate ids; 0 resolutions naming an unregistered id; maximum id R-0526; next free id R-0527 (moved from R-0526).
G5 PAIR PROOFS at HEAD after 83bc6df1, per pair — M1F, M3F and T1F each still occur exactly 1x in their target file, which is what an APPEND-shaped pair guarantees. M2F occurs 0x and M2T occurs 1x, the rewrite reading, ordered for that pair alone. The §4.9 append obligation: every line M1T (1), M3T (3) and T1T (20) add that their own FROM does not contain occurs exactly 1x among the 8 + 26 lines C2's diff ADDS. 0 marker lines reached either file. The string `subprocess` occurs 0x in `packages/orchestration/mission_state.py` at HEAD. `git show --numstat` for C2 = 8 6 packages/orchestration/mission_state.py / 26 0 tests/orchestration/test_mission_state.py. PLANF4->PLANT4 in `.agent/plan.md` after C3: FROM 0x, TO 1x.
G6 LINT AND SUITES — every command run in the PRIMARY checkout, never a worktree. `python3 -m ruff check packages/orchestration/mission_state.py tests/orchestration/test_mission_state.py` exit 0, `All checks passed!`. `python3 -m pytest tests/orchestration/test_mission_state.py -q` exit 0, `82 passed in 0.47s`. `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q` exit 0, `159 passed in 19.83s`. CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` exit 0, `42 passed in 20.24s`. No `tests/docs/` gate ordered and none run.
G7 HYGIENE — `git diff --name-only 23b5fcd9..HEAD` measured BEFORE C4 holds exactly `.agent/authored/f085-r36.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `packages/orchestration/mission_state.py`, `tests/orchestration/test_mission_state.py` and nothing else — the declared change set minus `.agent/handoff.md`, which C4 writes. Per-commit insertions before C4: 400, 361, 47, 34, 8 — none exceeds 500. Every commit has exactly one parent. `git reflog -10` holds only `commit:` entries.
G8 RED PROOF — run ONLY inside the disposable worktree at 83bc6df1: the module-level `from packages.orchestration.exec_guard import run_guarded_test_command` deleted and re-added as the first statement inside the `runner` closure, then `python3 -m pytest tests/orchestration/test_mission_state.py -q -rf` exit 1, `1 failed, 81 passed in 0.58s`. Failing id `tests/orchestration/test_mission_state.py::TestVerifyTaskExecution::test_the_default_runner_goes_through_the_guarded_seam`; reason, quoted: `E       AttributeError: <module 'packages.orchestration.mission_state' ...> has no attribute 'run_guarded_test_command'` raised at `monkeypatch.setattr(mission_state, "run_guarded_test_command", _fake_guarded)`, `test_mission_state.py:703`. Red as the block predicted, so the module-level import is load-bearing. Worktree removed and pruned; `git worktree list` = 1 line.

## Authored-text proofs
Every slice was extracted PROGRAMMATICALLY from the COMMITTED `.agent/authored/f085-r36.md` by its BEGIN/END marker pair; none was retyped or taken from the prompt; each FROM was asserted to match exactly once before the replace; 0 marker lines reached any target file. Transport is disk-to-disk byte equality (G2), not a digest fallback.
- M1F->M1T — TO contains FROM: true — APPEND. FROM 1x before and 1x after, by construction; the §4.9 append obligation is what is proved (G5). No FROM-zero reading is claimed for this pair, under any wording.
- M3F->M3T — TO contains FROM: true — APPEND. Same reading as M1; no FROM-zero count claimed.
- M2F->M2T — TO contains FROM: false — REWRITE. FROM 1x before, 0x after; TO 1x after.
- T1F->T1T — TO contains FROM: true — APPEND. Same reading as M1; no FROM-zero count claimed.
- PLANF4->PLANT4 — TO contains FROM: false — REWRITE. FROM 1x before, 0x after; TO 1x after.
- RECORD4 — append to `.agent/live_review.md`, proved as an append by G3.
Constraint 8 staleness re-read after C3, at HEAD: `.agent/authored/f085-r36.md`, `.agent/last_block.md`, `.agent/live_review.md`, `packages/orchestration/mission_state.py`, `tests/orchestration/test_mission_state.py`, `.agent/plan.md`. No sentence this round put on disk is falsified by a later commit of the same round: RECORD4's file-state readings all belong to the R35 range and name 6ca30b16, 23b5fcd9, cde59e8c or 2342ed97, and PLANT4's only file claim names 23b5fcd9, the state before this round.

Open findings: 119 (118 + R-0526 registered; nothing resolved this round).

## Deviations & assumptions
The commit sequence executed is exactly the block's Bundle in order: C0a, C0b, C1, C2, C3, C4 — no extra commit, none dropped, no reordering. Every slice applied as written; none edited.
DECLARED, per the "apply as written, declare the problem" rule: constraint 8 states that "RECORD4 states facts about `packages/orchestration/mission_state.py` and `tests/orchestration/test_mission_state.py`". Measured at HEAD, RECORD4 mentions neither path — 0 occurrences of either string in the slice. The constraint's staleness obligation is therefore vacuous for those two files rather than met; the re-read was performed anyway and is reported above. Nothing was changed on account of this.
Length, measured with `wc -l` on the draft before writing the file: 97 lines against the 100-line cap for a >5-commit bundle, so no DECISION D15 overage is claimed.

## Next
The next session's FIRST action is Phase 1 rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2, the Open PR Gate (`gh pr list --state open --json number,headRefName,baseRefName,isDraft`). R36's own verdict is NOT a §4.13 terminator: this branch continues, so the next reviewed round records R36's gate entry in `.agent/live_review.md`.

Carried verbatim from the block, because the reviewer measured it at 23b5fcd9 and it would otherwise be re-derived wrongly:

  The next migration site is `packages/orchestration/ci_run.py`. At 23b5fcd9 its only
  spawn is line 79, `subprocess.run(command, check=False, cwd=cwd, env=env).returncode`
  — no capture, no timeout, output streaming straight to the console. Moving it onto
  `run_guarded_test_command` therefore CHANGES observable behaviour rather than
  preserving it: the seam captures, so a console-streaming CI run would go silent
  unless the migration also decides where that output goes. That decision belongs in
  the round that does it and must be recorded as a DECISION, not taken in passing.
  `builder_bridge.py` comes LAST and stays BLOCKED until the seam can SET an
  environment value rather than only allowlist a key.
