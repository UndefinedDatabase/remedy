# Handback — F085 Sandbox hardening (stage 1) · Runde 35 (T002b interlude)

Branch: feature/f085-sandbox-hardening · Base SHA: 6ca30b16 · HEAD: this commit (C4).
Fortschritt: ~70 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34
PASS · T002a KOMPLETT · T002b 9 von 12 Sites auf dem Seam, 3 offen · T002c-d, T003
offen) — Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

## Range
Review of 6ca30b16..HEAD.

## Commits

### 54f5f447 docs(f085): save the R35 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r35.md | +331/-0 | C0a — block saved byte-for-byte |

### 84f912a9 docs(f085): mirror the R35 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +215/-257 | C0b — full replacement with the same bytes |

### 6d3b0230 docs(review): narrow checklist item 20 to paths rewritten every round
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +11/-0 | C1 — I20F->I20T applied |

### cde59e8c docs(review): record the R34 PASS and register and resolve R-0525
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +78/-0 | C2 — RECORD3 appended |

### 5e484694 docs(f085): advance the plan to R35
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +3/-3 | C3 — PLANF3->PLANT3 applied |

### C4 (this commit) docs(f085): rewrite the handback for R35
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
`git push -u origin feature/f085-sandbox-hardening` — outcome in the round report (run after this commit). No worktree add/remove: this round ordered no destructive check. No PR, no merge, no gh command.

## Verification
G1 STATE — `.agent/STOP` absent before C0a and again before C4 (re-read from disk both times). `git status --porcelain` = 0 lines at round start and after every commit. `git worktree list` = 1 line throughout; no worktree created.
G2 TRANSPORT — the committed `.agent/authored/f085-r35.md`, the committed `.agent/last_block.md`, BOTH working copies and the `.remedy-wt/` scratch are all five byte-EQUAL. sha256 41a8470f56a9063fb40a82526f0731bb57b2de20f296b075de572848a6f8581d · 21145 B · 331 lines · 10 marker lines. Region digests, trailing newlines included: 1-100 c9271720b7cfafdaace2084ea4be25573c30b21917d5b69cd1d0238f4d408bdd, 101-200 72829987007260b78060e784880c098c26c24d40c66d0f1b64558b80ebba6147, 201-331 3e006c9f27531922202f443377bd7f450f22c93b066f09e81e0b7608befa98c8. All measured, none computed by hand.
G3 APPEND SHAPE for cde59e8c — pre-commit blob 381289 B is a byte-exact PREFIX of the 387274 B post-commit file; remainder 5985 B = exactly one blank line plus RECORD3; RECORD3 is an exact suffix; its first line occurs 1x among the 78 lines the diff ADDS; 0 lines match `^(BEGIN|END)-[A-Z0-9]+$` while the BEGIN substring occurs 11x. `git show --numstat` = 78 0 .agent/live_review.md.
G4 ARITHMETIC — base 6ca30b16: 139 registered / 21 done / 0 landed, 118 open, max registered R-0524, max resolved R-0524. HEAD: 140 / 22 / 0, 118 open, both maxima R-0525. Registered symmetric difference {R-0525}; done symmetric difference {R-0525}; landed symmetric difference empty; 0 duplicate ids; 0 resolutions naming an unregistered id; maximum id R-0525; next free id R-0526 (moved from R-0525).
G5 NARROWING + APPEND OBLIGATION for 6d3b0230 — the I20F text still occurs exactly 1x, which is what an APPEND-shaped pair guarantees. The item-15 opener, the item-20 opener and the closing-paragraph opener each occur exactly 1x, so no item was added, removed or renumbered. All 11 TO-only lines occur exactly 1x among the 11 lines the commit's diff ADDS — the §4.9 append obligation, ordered instead of a FROM-zero count. 0 marker lines reached the file. `git show --numstat` = 11 0 docs/agents/planner_reviewer_prompt.md.
G6 SUITES — run in the PRIMARY checkout, never a worktree. `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q` exit 0, `159 passed in 19.77s`. `python3 -m pytest tests/docs/ -q` exit 0, `295 passed in 0.42s` — NOT read as evidence about C1: the reviewer's red control showed `tests/docs/` stays at 295 passed with that file cut to `# broken`, so the suite is blind to C1 by construction and G5 is the only check on C1's content. CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` exit 0, `42 passed in 20.27s`. No ruff run and no red proof ordered: this round changed no production code.
G7 HYGIENE — `git diff --name-only 6ca30b16..HEAD` measured BEFORE C4 holds exactly `.agent/authored/f085-r35.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `docs/agents/planner_reviewer_prompt.md` and nothing else — the declared change set minus `.agent/handoff.md`, which C4 writes. Per-commit insertions before C4: 331, 215, 11, 78, 3 — none exceeds 500. Every commit has exactly one parent. `git reflog -10` holds only `commit:` entries.

## Authored-text proofs
Every slice was extracted PROGRAMMATICALLY from the COMMITTED `.agent/authored/f085-r35.md` by its BEGIN/END marker pair; none was retyped or taken from the prompt; each FROM was asserted to match exactly once before the replace; 0 marker lines reached any target file. Transport is disk-to-disk byte equality (G2), not a digest fallback.
- I20F->I20T — TO contains FROM: true — APPEND. FROM occurs 1x before and 1x after, by construction. The §4.9 append obligation is what is proved: every TO-only line occurs exactly 1x among the commit's ADDED lines (G5). No FROM-zero reading is claimed for this pair, under any wording.
- PLANF3->PLANT3 — TO contains FROM: false — REWRITE. FROM 1x before, 0x after; TO 1x after.
- RECORD3 — append to `.agent/live_review.md`, proved as an append by G3.
Constraint 8 staleness re-read after C3, at HEAD: `.agent/authored/f085-r35.md`, `.agent/last_block.md`, `docs/agents/planner_reviewer_prompt.md`, `.agent/live_review.md`, `.agent/plan.md`. No sentence this round put on disk is falsified by a later commit of the same round; RECORD3's readings of prior state name 2342ed97, c15798a8, 7480d880 or 6ca30b16, and its claim about the state this round creates names constraint 9. Its four sentences mentioning `.agent/handoff.md` were checked individually: the one that LOCATES landed text names 2342ed97, 6ca30b16 and 7480d880; the other three state the rule or the path list and locate nothing.

Open findings: 118 (unchanged — R-0525 was registered and resolved in the same round).

## Deviations & assumptions
None. The commit sequence executed is exactly the block's Bundle in order: C0a, C0b, C1, C2, C3, C4 — no extra commit, none dropped, no reordering. Stated-cause overage per AGENTS.md DECISION D15: this handback is 101 lines against the 100-line cap for a >5-commit bundle. The cause is mandated content, not verbosity — six per-commit tables, the seven-gate verification table with its region digests and set arithmetic, the item-status table, the transport and pair proofs, and the migration design the block requires to be carried verbatim in `## Next`. No section was dropped to meet the cap.

## Next
The next session's FIRST action is Phase 1 rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2, the Open PR Gate (`gh pr list --state open --json number,headRefName,baseRefName,isDraft`). R35's own verdict is NOT a §4.13 terminator: this branch continues, so the next reviewed round records R35's gate entry in `.agent/live_review.md`.

Then the MIGRATION round, whose design the reviewer derived at 6ca30b16 and which is carried here verbatim so it is not re-derived wrongly:

  The next MIGRATION round takes the default `runner` closure in
  `packages/orchestration/mission_state.py` — at 6ca30b16 it is the
  `subprocess.run(argv, cwd=..., capture_output=True, text=True, timeout=900)` call
  inside `if runner is None:`, and it is the capture-and-timeout shape already
  migrated at `pingpong_loop.py`, `test_runner.py`, `job_promote.py` and
  `integrity_gate.py`.
  The import MUST be added at MODULE level, not inside the closure. Every existing
  seam test intercepts the call with
  `monkeypatch.setattr(<module>, "run_guarded_test_command", _fake_guarded)`
  (`tests/orchestration/test_pingpong.py`, `test_integrity_gate.py`,
  `test_job_promote.py` at 6ca30b16), and that patch cannot reach a name bound by a
  function-local import — a local import would leave the site untestable by the
  established pattern while every gate stayed green.
  The reviewer checked the cycle at 6ca30b16: `packages/orchestration/exec_guard.py`
  contains no reference to `mission_state`, so a module-level import adds no cycle.
  The seam returns BYTES while this closure has always returned `str`, so the decode
  `(proc.stdout or b"").decode("utf-8", "replace") + (proc.stderr or b"").decode(
  "utf-8", "replace")` is part of the change, matching `pingpong_loop.py` at 6ca30b16.
  `builder_bridge.py` still comes LAST and stays BLOCKED until the seam can SET an
  environment value rather than only allowlist a key.
