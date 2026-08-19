# Handback — F085 R58 · T002d second half: the two `runtime-build` call sites

Branch `feature/f085-sandbox-hardening`, base SHA b2bb3809, six ordered commits. Every number
below was measured by this worker. Deviations, declared: 135 lines against the ≤100-line
allowance the six-commit bundle earns, under AGENTS.md DECISION D15. Stated cause: the mandated
per-commit tables, the item-status table and the REAL G1-G9 results with exit codes and output.
No section is dropped and no gate reading is summarized to "green".

## Range
Review of b2bb3809..HEAD

## Commits

### b5bcc11b docs(f085): save the R58 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r58.md | +436/-0 | C0a — block copied byte-verbatim from `.remedy-wt/f085-r58.md` |

### c2b0b317 docs(f085): mirror the R58 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +366/-228 | C0b — mirror of the committed authored file |

### 240934ad docs(f085): advance the plan to the R58 call-site migration
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +8/-9 | C1 — PLAN12F→PLAN12T |

### 728469ac docs(f085): record the R57 PASS and resolve R-0558
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +53/-1 | C2 — RECORD26F→RECORD26T; reviewer text, the worker authored none |

### 35db0c2f feat(f085): route both auto-build npm commands through the runtime-build guard
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | +13/-6 | C3 — DOCIMPORT + INSTALL + BUILD, one commit |
| tests/ui_server/test_dashboard_contract.py | +35/-0 | C3 — TESTGUARD, one new test |

### C4 (this commit) docs(f085): write the R58 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C4 — a handoff cannot table the commit that writes it |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | four pairs in one commit, as the Change section requires |
| C4 | done | this commit |

## Verification — real commands, real exit codes
- G1 STATE. `.agent/STOP` absent before C0a and again before C4 (`ls` exit 2 both times).
  `git status --porcelain` empty at round start and after every commit. `git worktree list` one
  line at round start and one at the end; the G9 worktree existed only in between.
- G2 TRANSPORT, disk-to-disk, no digest fallback. `.remedy-wt/f085-r58.md`, both working copies
  and both committed blobs — FIVE copies — are byte-EQUAL at sha256
  6d46cb294da82694650390a40f65c57cc886dd9885d3e1302a638270e193bd77, 29671 B, 436 lines, 24 marker
  lines. Block sizes re-measured from the committed file: TOTAL 436 (cap 490), PROSE 267 (cap
  400), RECORD26T 53 (cap 140) — all three agree with constraint 11 exactly.
- G3 SHAPES. All six pairs `TO contains FROM: false`, FROM 1x in the blob it is applied to, and in
  each post-commit blob FROM 0x with TO exactly 1x. Re-applying the extracted FROM→TO to the
  pre-commit blob reproduces the post-commit blob BYTE-EXACTLY for all four (commit, path) pairs,
  sha256 equal on both sides. numstat: 240934ad `8 9`; 728469ac `53 1`; 35db0c2f `13 6` and
  `35 0`. Lines matching `^(BEGIN|END)-[A-Z0-9]+$` at HEAD: 0 in `.agent/plan.md`, 0 in
  `.agent/live_review.md`, 0 in `ui_server.py`, 0 in the test file.
- G4 SUITES, primary checkout, each exit 0: dashboard contract `71 passed` — base 70, one test
  added, so YES it is 71; responsive `92 passed`; exec_guard `35 passed`; the four state readers
  `160 passed` (base 159, expected 160); canary golden path `42 passed`.
- G5 LINT. `python3 -m ruff check <both paths>` exit 0, `All checks passed!`. NARROWED PREVIEW per
  path, rule-code MULTISET at b2bb3809 vs HEAD, exit 1 at both SHAs on both paths:
  `packages/orchestration/ui_server.py` `E306 x3` → `E306 x3`;
  `tests/ui_server/test_dashboard_contract.py` `E226 x1, E303 x11, W391 x1` → identical. Both
  multisets IDENTICAL per path — no new code, no higher count. No `--isolated`, no `--fix`.
- G6 PLAN CONTRACT after C1: 43 lines against the 50-line cap, which is the reviewer's projection
  exactly; `## Goal` True, `## Next Steps` True, `\bF\d{3}\b` True.
- G7 ARITHMETIC. b2bb3809: 173 / 27 / 1, 146 open, max registered R-0558, max resolved R-0532.
  HEAD: 173 / 28 / 0, 145 open, max registered R-0558, max resolved R-0558. Registered symmetric
  difference EMPTY; done symmetric difference exactly {R-0558}, direction ADDED; landed symmetric
  difference exactly {R-0558}, direction REMOVED. 0 duplicate ids and 0 resolutions naming an
  unregistered id at both SHAs. Next free id R-0559.
- G8 HYGIENE, measured BEFORE C4. `git diff --name-only b2bb3809..HEAD` is exactly the six paths
  `.agent/authored/f085-r58.md`, `.agent/last_block.md`, `.agent/live_review.md`,
  `.agent/plan.md`, `packages/orchestration/ui_server.py`,
  `tests/ui_server/test_dashboard_contract.py` and nothing else — NEITHER
  `packages/orchestration/exec_guard.py` NOR `runtime_cmd.py` / `dev_server.py` /
  `runtime_supervisor.py`. Per-commit INSERTIONS before C4: 436, 366, 8, 53, 48 — none over 500,
  all five single-parent. C4 cannot measure itself: it touches only `.agent/handoff.md`, the
  AGENTS.md single-state-file rewrite exemption.
- G9 RED CONTROL, in the disposable worktree `.remedy-wt/r58-g9`, since removed. BUILDT→BUILDF
  alone (bare `subprocess.run` restored at the `npm run build` site, the install site left
  migrated), then `python3 -m pytest tests/ui_server/test_dashboard_contract.py -rf -q` → EXIT 1,
  RED. The complete `-rf` summary is one line:
  `FAILED tests/ui_server/test_dashboard_contract.py::TestAutoBuildBehavior::test_auto_build_npm_commands_run_through_the_guard`
  — the only failure, and it is the new test. The rest of the file is NOT red: the run reports
  `1 failed, 69 passed, 1 skipped`, the skip being the UI-toolchain test a fresh worktree skips as
  the block predicted. The failing assertion is `assert bare_run.call_count == 0` → `1 == 0`.
  Worktree then removed; `git worktree list` one line, `git status --porcelain` empty.

## Authored-text proofs
All six slices were extracted PROGRAMMATICALLY from the COMMITTED `.agent/authored/f085-r58.md`
under the block's CONVENTION and applied as byte-level replacements — no editor insert, no hand
edit, no marker line in any target. Disk-to-disk equality of the five copies is under G2; the
per-pair byte-exact replay is under G3.

## External actions
- `git worktree add --detach .remedy-wt/r58-g9 HEAD` created it; `git worktree remove` removed it.
- `git push -u origin feature/f085-sandbox-hardening` after C3 — exit 0, `b2bb3809..35db0c2f`.
  The same push is re-run after C4. No PR, no merge, no force-push.

## Deviations & assumptions
None. C0a, C0b, C1, C2, C3, C4 ran in the block's order with no commit added, dropped or
reordered; no slice was edited, no gate widened, no target file reformatted. No value this worker
measured disagreed with the block: the base preview multisets, the base arithmetic 173/27/1 with
146 open, the base dashboard `70 passed`, TOTAL 436 / PROSE 267 / RECORD26T 53 and the projected
plan length 43 all reproduced exactly.

## Next
ONE: the next round is R59, which migrates the three `runtime-server` call sites in
`packages/orchestration/runtime_cmd.py`, `packages/orchestration/dev_server.py` and
`packages/orchestration/runtime_supervisor.py`; they are `Popen`-shaped and take NO wall timeout,
because a clock would kill a server mid-service, so that round's first task is to establish
whether a `runtime-server` seam exists yet or has to be built.
TWO: R59 also carries the R58 verdict, because the round that records a verdict cannot record one
on itself (docs/agents/planner_reviewer_prompt.md §4.13).
THREE: 145 findings are open and the next free id is R-0559.
FOUR: Phase 1 rule 1 first: re-read `.agent/STOP` from disk.

Fortschritt: ~96 % (T001 gebaut · R13-R55 PASS · R56 FAIL, an R57 repariert · R57 PASS · T002a
KOMPLETT · T002b KOMPLETT · T002c KOMPLETT · T002d KOMPLETT — Naht, Extraktion, Umgebungszeile und
die beiden `runtime-build`-Call-Sites gebaut · T003 offen, mitsamt den drei
`runtime-server`-Call-Sites) — Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.
