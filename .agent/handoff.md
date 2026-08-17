# Handback — F085 Sandbox hardening (stage 1), Runde R50

Branch `feature/f085-sandbox-hardening`, base SHA 25a5b42e. Record + amendment round; no source
file touched.

## Range

Review of 25a5b42e..HEAD.

## Commits

### c22cb9dd chore(f085): save the authored R50 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r50.md | +334/-0 | C0a — reviewer block saved byte-verbatim |

### 634447bc chore(f085): mirror the R50 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +239/-250 | C0b — identical bytes mirrored from the committed blob |

### 2241cb69 docs(f085): advance the plan to R50
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +6/-4 | C1 — PLAN4F→PLAN4T rewrite |

### 56722bd7 docs(f085): record the R49 PASS and register R-0552 and R-0553
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +73/-0 | C2 — RECORD18 appended |

### 8bb7a287 docs(f085): split the runtime policy row into runtime-server and runtime-build
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T2_F085.md | +10/-7 | C3a — AMEND8F→AMEND8T rewrite |

### 9b9cd0b4 docs(f085): append amendment F085 D8 for the runtime policy split
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T2_F085.md | +30/-0 | C3b — DEC8 appended |

### C4 docs(f085): rewrite the handback for R50
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | this file | C4 — a handback cannot table its own commit (R-0149) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3a | done | |
| C3b | done | |
| C4 | done | this commit |

## External actions

`git push -u origin feature/f085-sandbox-hardening` — run after C4; result in the round report.
No `gh` command, no PR, no merge, no worktree added or removed.

## Verification

G1 STATE, pass. `.agent/STOP` absent before C0a and again before C4; `git status --porcelain`
empty at round start and after each of the seven commits; `git worktree list` one line throughout.
G2 TRANSPORT, pass, disk-to-disk with no digest fallback. `.remedy-wt/f085-r50.md`, the committed
and the working `.agent/authored/f085-r50.md` and the committed and the working
`.agent/last_block.md` are all five byte-EQUAL: sha256
061fa19d22524bd91e69697f28285376e82f45005d7894f833ab991adb390cd7, 24335 B, 334 lines, 12 marker
lines — every figure measured on every copy.
G3 SHAPES, pass, one reading per pair. C1: PLAN4F 0x, PLAN4T 1x in `.agent/plan.md`, numstat
`6 4`. C2: pre-commit blob an exact prefix, remainder exactly one blank line plus the slice, slice
an exact suffix, 0 marker LINES in the file, 72 slice lines of which 2 empty, each non-empty slice
line exactly once among the 73 lines added to that path, numstat `73 0`. C3a: AMEND8F 0x, AMEND8T
1x in `docs/roadmap/features/T2_F085.md`, numstat `10 7`. C3b: prefix, one blank line plus slice,
exact suffix, 0 marker LINES, 29 slice lines of which 3 empty, each non-empty line exactly once
among the 30 added, numstat `30 0`.
G4 SUITE, exit 0, primary checkout, no worktree: `python3 -m pytest
tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q` →
`159 passed in 19.77s`, base 159. CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` →
exit 0, `42 passed in 20.55s`, base 42.
G5 DOCS TIER, exit 0: `python3 -m pytest tests/docs/ -q` → `295 passed in 0.43s`, base 295.
G6 PLAN CONTRACT on `.agent/plan.md` at 2241cb69, pass: 41 lines against the 50-line cap;
`## Goal` true, `## Next Steps` true, `\bF\d{3}\b` true (F083, F085).
G7 ARITHMETIC, pass. 25a5b42e: 166 registered / 27 done / 0 landed, 139 open, 0 duplicate ids, 0
resolutions naming an unregistered id, max registered R-0551, max resolved R-0532. HEAD: 168 / 27
/ 0, 141 open, 0 duplicates, 0 orphan resolutions. Registered symmetric difference exactly
{R-0552, R-0553}; done and landed symmetric differences EMPTY.
G8 HYGIENE, pass. `git diff --name-only 25a5b42e..HEAD` before C4 = `.agent/authored/f085-r50.md`,
`.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
`docs/roadmap/features/T2_F085.md` — the change set minus `.agent/handoff.md`, nothing else.
Per-commit INSERTIONS before C4: 334, 239, 6, 73, 10, 30 — none over 500, so the allowance spent
at d4473f85 is not called on again. All commits single-parent.
BLOCK SIZE re-measured from the committed `.agent/authored/f085-r50.md`: TOTAL 334, PROSE 182,
RECORD18 72 — each equal to what the block stated, each under its DECISION F085 D6 cap.

## Authored-text proofs

All six slices were extracted PROGRAMMATICALLY from the committed `.agent/authored/f085-r50.md`
by BEGIN-/END- marker pair and applied byte-verbatim; none was retyped and no marker line reached
a target file. The disk-to-disk comparison against the reviewer's own `.remedy-wt/f085-r50.md` is
G2 above.

## Deviations & assumptions

None. The ordered sequence C0a, C0b, C1, C2, C3a, C3b, C4 was followed exactly, with no extra,
dropped or reordered commit, and no gate came out red.
Deviations, declared: this file is 133 lines, over the ≤100 allowance, under DECISION D15
stated cause — seven per-commit changed-files tables, the seven-row item-status table and the
G1-G8 transcripts including the transport and the four pair proofs are all mandated content, and
no section was dropped to meet the cap.

## Next

ONE. The next round is R51, started by a FRESH session, and it implements T002c:
`_run_process_check` onto the guard seam KEEPING its wall timeout and closing its
`env=os.environ.copy()` gap, and `_run_app_once` under the dod-app policy with no wall timeout and
network allowed. T002d then follows under the DECISION F085 D8 split, then T003, the integration
gate and closure.
TWO. R50's own verdict is NOT on disk as a gate entry, because the round that records a verdict
cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13). That absence is the
terminator, not a missing gate, and R51 must not open a repair round to close it; R50's verdict,
when the reviewer issues it, is recorded by R51's OWN record slice.
THREE. Open findings: 141. Next free finding id: R-0554.
FOUR. Phase 1 rule 1 first: re-read `.agent/STOP` from disk — ahead of the Open PR Gate.

Fortschritt: ~85 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R49 PASS ·
T002a KOMPLETT · T002b KOMPLETT · T002c entsperrt durch Amendment F085 D7, noch nicht gebaut ·
T002d entsperrt durch Amendment F085 D8, noch nicht gebaut · T003 offen) — Schätzung, gegen die
Klassentabelle aus Amendment F085 D1 gemessen.
