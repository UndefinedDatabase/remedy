# Handback — F085 Sandbox hardening (stage 1) · Runde 37 (Record + checklist item 11)

Branch: feature/f085-sandbox-hardening · Base SHA: 483975b3 · HEAD: this commit (C4).
Fortschritt: ~73 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R36
PASS · T002a KOMPLETT · T002b 10 von 12 Sites auf dem Seam, 2 offen · T002c-d, T003
offen) — Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

## Range
Review of 483975b3..HEAD.

## Commits

### e2b23b33 docs(f085): save the R37 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r37.md | +329/-0 | C0a — block saved byte-for-byte |

### 857ca31a docs(f085): mirror the R37 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +264/-335 | C0b — full replacement with the same bytes |

### 69155e06 docs(review): widen checklist item 11 to claims about the author's own text
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +19/-0 | C1 — I11F->I11T, item 11 extended in place |

### 75feb987 docs(review): record the R36 PASS and register and resolve R-0526 and R-0527
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +81/-0 | C2 — RECORD5 appended: R36 gate entry, R-0527, both resolutions |

### a979ca03 docs(f085): advance the plan to R37
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +3/-3 | C3 — PLANF5->PLANT5 applied to Current Step alone |

### C4 (this commit) docs(f085): rewrite the handback for R37
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
No worktree was created — this round ordered no destructive check; `git worktree list` = 1 line throughout. `git push -u origin feature/f085-sandbox-hardening` — outcome in the round report (run after this commit). No PR, no merge, no gh command.

## Verification
G1 STATE — `.agent/STOP` re-read from disk before C0a and again before C4; absent both times (`os.path.exists` False both times). `git status --porcelain` = 0 lines at round start and after every commit. `git worktree list` = 1 line at round start and 1 line at C4.
G2 TRANSPORT — the committed `.agent/authored/f085-r37.md`, the committed `.agent/last_block.md` and BOTH working copies are byte-EQUAL, all four measured after C0b. sha256 c8efc5c06444464245a311d03acc78f008246a9c259a7100330bdeac876d8409 · 21768 B · 329 lines · 10 marker lines. Region digests, trailing newlines included: 1-100 707379841e152459f11cbaf3d90e62cff0de31f34ade6233aefba43766a16d0f, 101-200 9bdbc47602dc138ccf12aa74e136325fe4d20a96febafeda6bca68393deef93e, 201-329 89541ee67f8b3ebda2146e4164a567343b43f41a1ddd0527ad5ac2f8aeb144cc. The prompt's ordered digest matched the scratch file before C0a.
G3 APPEND SHAPE for 75feb987 — pre-commit blob 391135 B is a byte-exact PREFIX of the 397527 B post-commit file; remainder 6392 B = exactly one blank line plus RECORD5; RECORD5 is an exact suffix; its first line occurs 1x among the 81 lines the diff ADDS; 0 lines match `^(BEGIN|END)-[A-Z0-9]+$` while the BEGIN substring occurs 15x. `git show --numstat` = 81 0 .agent/live_review.md.
G4 ARITHMETIC — base 483975b3: 141 registered / 22 done / 0 landed, 119 open, max registered R-0526, max resolved R-0525 — the block's base reading, reproduced. HEAD: 142 / 24 / 0, 118 open, max registered R-0527, max resolved R-0527. Registered symmetric difference {R-0527}; done symmetric difference {R-0526, R-0527}; landed symmetric difference empty; 0 duplicate ids; 0 resolutions naming an unregistered id; maximum id R-0527; next free id R-0528 (moved from R-0527).
G5 THE CLAUSE LANDED, measured at HEAD after 69155e06 — I11F still occurs exactly 1x, the APPEND reading. The item-11 opener, the item-12 opener and the closing-paragraph opener each occur exactly 1x, so no item was added, removed or renumbered. The §4.9 append obligation: all 19 lines I11T adds that I11F does not contain occur exactly 1x among the 19 lines C1's diff ADDS (0 lines fail this). 0 marker lines reached the file. `git show --numstat` for C1 = 19 0 docs/agents/planner_reviewer_prompt.md. PLANF5->PLANT5 in `.agent/plan.md` after C3: FROM 0x, TO 1x.
G6 SUITES — every command run in the PRIMARY checkout, never a worktree (R-0518). `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q` exit 0, `159 passed in 19.79s`. `python3 -m pytest tests/docs/ -q` exit 0, `295 passed in 0.51s` — NOT read as evidence about C1; per the block, no test under `tests/docs/` reads `docs/agents/planner_reviewer_prompt.md`, so G5 is the only check on C1's content. CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` exit 0, `42 passed in 20.40s`.
G7 HYGIENE — `git diff --name-only 483975b3..HEAD` measured BEFORE C4 holds exactly `.agent/authored/f085-r37.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `docs/agents/planner_reviewer_prompt.md` and nothing else — the declared change set minus `.agent/handoff.md`, which C4 writes. Per-commit insertions before C4: 329, 264, 19, 81, 3 — none exceeds 500. Every commit has exactly one parent. `git reflog -10` holds only `commit:` entries.

## Authored-text proofs
Every slice was extracted PROGRAMMATICALLY from the COMMITTED `.agent/authored/f085-r37.md` by its BEGIN/END marker pair; none was retyped or taken from the prompt; each FROM was asserted to match exactly once before the replace; 0 marker lines reached any target file. Transport is disk-to-disk byte equality (G2), not a digest fallback.
- I11F->I11T — TO contains FROM: true (measured, and I11T also starts with I11F) — APPEND. FROM 1x before and 1x after, by construction; the §4.9 append obligation is what is proved (G5). No FROM-zero reading is claimed for this pair, under any wording.
- PLANF5->PLANT5 — TO contains FROM: false (measured) — REWRITE. FROM 1x before, 0x after; TO 0x before, 1x after.
- RECORD5 — append to `.agent/live_review.md`, proved as an append by G3.
Constraint 8 staleness re-read after C3, at HEAD, over every file this round edited: `.agent/authored/f085-r37.md`, `.agent/last_block.md`, `docs/agents/planner_reviewer_prompt.md`, `.agent/live_review.md`, `.agent/plan.md`. Each is touched by exactly one commit of this round, so no sentence was falsified by a LATER commit of the same round. RECORD5's claim that item 11 now carries the clause is true when written, because C1 (69155e06) precedes C2 (75feb987) as constraint 9 requires. One measured exception is declared below.

Open findings: 118 (119 − 2 resolved + 1 registered; R-0527 registered, R-0526 and R-0527 resolved).

## Deviations & assumptions
The commit sequence executed is exactly the block's Bundle in order: C0a, C0b, C1, C2, C3, C4 — no extra commit, none dropped, no reordering. Every slice applied byte-verbatim as written; none edited.
DECLARED, per the "apply as written, declare the problem" rule and constraint 8's measurement duty: constraint 8 states "The only file this block both edits and makes claims about is `docs/agents/planner_reviewer_prompt.md`" and that "Every other reading RECORD5 asserts about a state before this round names 483975b3 or an earlier SHA". Measured against RECORD5 itself, both halves fail. RECORD5 names three files this round edits, not one: `docs/agents/planner_reviewer_prompt.md` (C1), `.agent/last_block.md` (C0b) and `.agent/live_review.md` (C2). And RECORD5's transport sentence — "the committed `.agent/authored/f085-r36.md`, the committed `.agent/last_block.md` and both working copies are all five byte-EQUAL at sha256 208ad9d3…" — names NO commit SHA (its three 8-hex tokens are region content digests) and is FALSE at HEAD: `.agent/last_block.md` was overwritten by this round's own C0b and now hashes to c8efc5c0…; the 208ad9d3… reading held at 483975b3 and is recoverable only from the paragraph's scoping sentence "re-run by the reviewer over 23b5fcd9..483975b3", not from the sentence itself. That is the R-0527 shape — a block constraint asserting a property its own slice does not have — recurring inside the constraint written to close R-0527, and the R-0520 shape for the sentence. Applied as written; nothing was edited or "repaired" on account of it.
Length, measured with `wc -l` on the draft before writing the file: 94 lines against the 100-line cap for a >5-commit bundle, so no DECISION D15 overage is claimed.

## Next
The next session's FIRST action is Phase 1 rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2, the Open PR Gate (`gh pr list --state open --json number,headRefName,baseRefName,isDraft`). R37's own verdict is NOT a §4.13 terminator: this branch continues, so the next reviewed round records R37's gate entry in `.agent/live_review.md`.

Carried verbatim from the block, because the reviewer measured it at 483975b3 and it would otherwise be re-derived wrongly:

  The next migration site is `packages/orchestration/ci_run.py`. At 483975b3 its only
  spawn is line 79, `subprocess.run(command, check=False, cwd=cwd, env=env).returncode`
  — no capture, no timeout, output streaming straight to the console. Moving it onto
  `run_guarded_test_command` therefore CHANGES observable behaviour rather than
  preserving it: the seam captures, so a console-streaming CI run would go silent unless
  the migration also decides where that output goes. That decision is the round's own
  work and is recorded as a DECISION in `.agent/decisions.md`, not taken in passing. It
  also passes `env=`, which the seam does not accept: the seam allowlists keys the
  parent already has and cannot SET a value, so that round must establish what happens
  to the caller's `env` before it changes any line.
  `builder_bridge.py` comes LAST and stays BLOCKED for the same allowlist reason.
