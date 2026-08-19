# Handback — F085 Sandbox hardening, R70 (the INTEGRATION GATE)

Branch: feature/f085-sandbox-hardening. Base SHA: 126b70ae. HEAD: 660540f6 + this commit.
G4 outcome: BLOCKER — one branch-only failure reproduces serially, does not reproduce at the merge
base, and is coupled to this feature's code. No fix attempted (constraint 11).

## Range
Review of 126b70ae..HEAD — six commits: C0a C0b C1 C2 C3 C4.

## Commits

### 585a4390 chore(f085): save the R70 step block  (C0a)
| Path | +/- | Reason |
| `.agent/authored/f085-r70.md` | +308/-0 | block saved byte-verbatim from transport |

### 6b6ff1e5 chore(f085): mirror the R70 block into last_block  (C0b)
| Path | +/- | Reason |
| `.agent/last_block.md` | +228/-340 | mirror of the same bytes |

### cdbcfb16 chore(f085): advance the plan to the R70 integration gate  (C1)
| Path | +/- | Reason |
| `.agent/plan.md` | +7/-9 | PLAN24F→PLAN24T applied |

### d2e65482 docs(f085): record the R69 PASS  (C2)
| Path | +/- | Reason |
| `.agent/live_review.md` | +54/-0 | RECORD38 appended at EOF |

### 660540f6 chore(f085): record the R70 integration gate evidence  (C3)
| Path | +/- | Reason |
| `.agent/gate_f085_r70/` | +262/-0 | 10 files: attribution, both FAILED lists, both comm outputs, both run tails, branch_meta, base_parity, full_log_provenance |

### C4 handback (self-referential, R-0149 pattern)
| Path | +/- | Reason |
| `.agent/handoff.md` | rewrite | this file; a handoff cannot table its own commit |

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C0a | done | |
| C0b | done | |
| C1  | done | |
| C2  | done | |
| C3  | done | evidence committed; G4 verdict is BLOCKER, reported not fixed |
| C4  | done | this handback |

## External actions
- `git worktree add -b tmp/base-gate-r70 .remedy-wt/base-r70 a5a70621` → rc 0, on a branch, not detached.
- `git worktree remove --force .remedy-wt/base-r70` + `git worktree prune` → rc 0.
- `git branch -D tmp/base-gate-r70` → "Deleted branch tmp/base-gate-r70 (was a5a70621)".
- `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

## Verification (real exit codes, real values)
- **G1 STATE.** `.agent/STOP` absent before C0a and before C4 (`ls` → No such file). `git status
  --porcelain` empty at round start and after every commit. `git worktree list` one line at both ends.
- **G2 TRANSPORT.** Committed `.agent/authored/f085-r70.md`, committed `.agent/last_block.md`, both
  working copies and the transport file: ALL FIVE BYTE-EQUAL, sha256
  31f928b9466a6d46a22ed4be1da815f545419861ac9341f12a03cdff414442f3, 24310 B, 308 lines, 6 marker
  lines each. TOTAL 308 ≤ 490; PROSE 232 ≤ 400; RECORD38 54 ≤ 140 (PLAN24F 12, PLAN24T 10).
- **G3 SHAPES.** PLAN24F→PLAN24T over `.agent/plan.md` at cdbcfb16: `TO contains FROM: False`;
  FROM 1x pre-commit; FROM 0x and TO 1x post-commit; re-applying FROM→TO to the pre-commit blob
  reproduces the post-commit blob BYTE-EXACTLY (True). numstat `7 9`.
  RECORD38 over `.agent/live_review.md` at d2e65482: PREFIX True, SUFFIX True, `pre + slice == post`
  True, ADDED lines 54 == slice lines 54 and equal IN ORDER (True). numstat `54 0`.
  Marker LINES `^(BEGIN|END)-[A-Z0-9]+$`: 0 in both edited files.
- **G4 INTEGRATION GATE.** Suites ran SERIALLY, one pytest process at a time.
  - Branch run `python3 -m pytest -n auto -q` (primary checkout): **exit 1**, **152 s**,
    `1 failed, 17131 passed, 19 skipped in 151.31s`. FAILED list 1 line.
  - Base run, same command, `REMEDY_UI_NO_AUTO_BUILD=1`, in `.remedy-wt/base-r70` at a5a70621:
    **exit 1**, **113 s**, `8 failed, 17039 passed, 19 skipped in 111.77s`. FAILED list 8 lines.
  - Parity: `apps/ui/node_modules` and `apps/ui/dist` COPIED with `cp -a`, never symlinked; no symlink
    found. DIST_SHA256 BEFORE == AFTER = fb68a7293502c79b8ece61d154f5752100a16da1a08a481a7a4c1d79a5a503c0.
  - `comm -13` branch-only: **1** line. `comm -23` base-only: **8** lines. Both committed.
  - Attribution — one entry per id, none absent (`.agent/gate_f085_r70/attribution.txt`):
    - **BLOCKER**, `tests/test_command_discovery.py::TestNoShellTrue::test_run_tests_local_no_shell_true`.
      Serial re-run, primary checkout: exit 1, `1 failed in 0.47s`,
      `assert mock_run.called → AssertionError: assert False` at line 663. Same id serial at the merge
      base: **exit 0, `1 passed in 0.21s`** — does NOT reproduce. Coupling: this feature replaced
      `subprocess.run(...)` in `run_tests_local` with `run_guarded_test_command(...)`
      (`packages/orchestration/test_runner.py`), which spawns via `subprocess.Popen`
      (`packages/orchestration/exec_guard.py:427`), so the test's `patch("subprocess.run")` is never
      reached. `git diff --stat a5a70621..HEAD -- tests/test_command_discovery.py` is EMPTY — the
      branch never touched the failing test. Round STOPPED here; no fix attempted.
    - 8 base-only ids, all `tests/ui_server/test_live_state.py::TestUIServerIntegration::*`, one
      environment class, missing artifact named per id: a built `apps/ui/dist/index.html` newer than
      the worktree's checked-out `apps/ui/src` (src 18:54:11 vs copied dist 18:52:27 →
      `_frontend_is_stale()` True → `_auto_build_frontend` returns None under
      `REMEDY_UI_NO_AUTO_BUILD=1`, ui_server.py:2781 → "ERROR: React UI not built." + `sys.exit(1)`,
      ui_server.py:2856/2867 → "Server did not start in time"). Direct confirmation: the class re-run
      SERIALLY in that same worktree with the artifact fresh → **exit 0, `16 passed in 2.12s`**. No
      genuine base failure; no id unattributed.
  - Wall budget: branch run 152 s, under ~5 min. No perf note owed.
- **G5 PLAN CONTRACT.** `.agent/plan.md` at HEAD: **37 lines** ≤ 50; `## Goal` True; `## Next Steps`
  True; `\bF\d{3}\b` True.
- **G6 ARITHMETIC.** 126b70ae: 178 registered / 31 done / 0 landed, 147 open, max registered R-0563,
  max resolved R-0563, 0 duplicate ids, 0 orphan resolutions. HEAD: IDENTICAL on all nine readings.
  All three symmetric differences EMPTY. Next free id R-0564.
- **G7 CANARY.** `python3 -m pytest tests/cli/test_golden_path.py -q` → **exit 0**, `42 passed in 21.90s`.
- **G8 HYGIENE.** `git diff --name-only 126b70ae..HEAD` before C4 = 14 paths: `.agent/authored/
  f085-r70.md`, `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`, and the 10 files
  under `.agent/gate_f085_r70/`. Grep for `^(packages|apps|docs|scripts|tests)/` or `\.log$` → NONE.
  Insertions: 585a4390 308, 6b6ff1e5 228, cdbcfb16 7, d2e65482 54, 660540f6 262 — none over 500.
  Every commit single-parent. No second oversize commit.

## Authored-text proofs
`.agent/authored/f085-r70.md` vs the transport file: `cmp` equal, both sha256 31f928b9…414442f3,
24310 B. `.agent/last_block.md` vs it: `cmp` equal, same digest. Both slices were extracted
PROGRAMMATICALLY from the committed authored file by marker pair under the block's CONVENTION;
neither was retyped, reflowed, nor taken from the prompt.

## Deviations & assumptions
1. **Handoff overage, declared.** This file is 143 lines against the ≤100 cap that >5-commit tables
   allow (AGENTS.md DECISION D15, stated cause). Cause: the mandated per-commit tables for six
   commits, the item-status table, the transport and pair proofs, and G4's mandated full numbers —
   both exit codes, both wall times, both FAILED counts, both comm counts and the per-id attribution.
   No section was dropped.
2. **`base_run_tail.txt` committed.** G4's file list names `branch_run_tail.txt` but no base tail;
   `docs/agents/integration_gate.md` step 2 orders "same records" for the base side, which G4
   incorporates by reference. Committed and declared rather than silently added.
3. **`base_parity.txt` carries a MEASURED CAVEAT beyond the two digests G4 orders.** Mtimes taken
   after the runs show `apps/ui/dist` was rewritten INSIDE BOTH checkouts mid-run (primary 18:52:27
   during the branch run; worktree 18:55:23 during the base run) while the content digest stayed
   equal, the rebuild being byte-deterministic. By the block's own stated rule the parity claim
   stands, and every base-only id is additionally attributed per id. The blindness of a content
   digest to an mtime-only rebuild is REPORTED for the reviewer to judge.
4. **Bundle order.** No extra commit, no dropped commit, no reordering: C0a C0b C1 C2 C3 C4 exactly.
5. **No ledger text authored** (constraint 8): no `Landed:` line, no `Done:` paragraph, RECORD38
   unedited. The BLOCKER is REPORTED, not registered — constraint 9 rules this round registers
   nothing, so registering it is the reviewer's act. No disagreement was found between RECORD38 and
   anything measured this round.

Fortschritt: ~100 % der Bauarbeit und das Integration Gate gelaufen (T001 gebaut · T002 KOMPLETT ·
T003 KOMPLETT und akzeptanzgemessen · R69 PASS) — offen bleibt nur noch die Closure: Evidence-Job,
frischer Review-Zip, die STATUS-Zeile und der PR. Schätzung, gegen die Klassentabelle aus Amendment
F085 D1 gemessen.

## Next
ONE: R71 is CLOSURE per docs/roadmap/STATUS_closure_protocol.md — evidence job, FRESH review zip, the
reviewer-authored STATUS line, and the PR the operator merges at the next Open PR Gate. That plan is
now CONDITIONAL on the G4 BLOCKER above, whose fix is its own reviewer-gated round before closure.
TWO: R70 carries no verdict of its own, because the round that records a verdict cannot record one on
itself (docs/agents/planner_reviewer_prompt.md §4 item 13); R71 carries it.
THREE: open findings 147; next free id R-0564.
FOUR: Phase 1 rule 1 first: re-read `.agent/STOP` from disk.
