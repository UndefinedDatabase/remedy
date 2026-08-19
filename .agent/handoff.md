# Handoff — F085 Sandbox hardening, STEP T003 closure run 2, round R72

Branch: feature/f085-sandbox-hardening. Base SHA: f023e2b1. Tip before this commit: 987bf3be.

## Range

Review of f023e2b1..HEAD (8 commits: C0a, C0b, C1, C2, C3, C4, C5, C6).

## Commits

### 42f043cd chore(f085): save the R72 step block (C0a)
| Path | +/- | Reason |
| `.agent/authored/f085-r72.md` | +374/-0 | block saved byte-verbatim from transport |

### b7abf889 chore(f085): mirror the R72 block into last_block (C0b)
| Path | +/- | Reason |
| `.agent/last_block.md` | +301/-335 | verbatim rewrite, single state file (D1 exempt) |

### 4bbfac80 docs(f085): advance the plan to the R72 gate round (C1)
| Path | +/- | Reason |
| `.agent/plan.md` | +8/-9 | PLAN26F→PLAN26T rewrite of Current Step + whole Next Steps |

### 5f592bdd docs(f085): record the R71 PASS and register R-0566 (C2)
| Path | +/- | Reason |
| `.agent/live_review.md` | +44/-0 | RECORD41 appended at EOF |

### 0f7e3f7e docs(f085): resolve R-0564 with the authored done text (C3)
| Path | +/- | Reason |
| `.agent/live_review.md` | +15/-3 | LANDEDF→LANDEDT; the one overwrite §4 item 4 mandates |

### 2f786299 docs(f085): rule the open-findings count as DECISION F085 D7 (C4)
| Path | +/- | Reason |
| `.agent/decisions.md` | +26/-0 | DECISIOND7 appended at EOF |

### 987bf3be chore(f085): commit the R72 integration gate evidence (C5)
| Path | +/- | Reason |
| `.agent/gate_f085_r72/` | +185/-0 | 9 files under that dir, exactly the ones G4 names |

### C6 this commit docs(f085): write the R72 handback
| Path | +/- | Reason |
| `.agent/handoff.md` | self | cannot table itself (R-0149) |

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | this commit |

## Verification

G1 STATE — `.agent/STOP` absent before C0a and again before C6. `git status --porcelain` empty at
round start and after every commit. `git worktree list` one line at start and one line at end.
G2 TRANSPORT — committed authored, committed last_block and BOTH working copies all four byte-EQUAL:
sha256 8deb1e027ffa9a44f0a870c8b780ca7f048f3c1a4e1904eb7625c5f061193383, 29673 B, 374 lines,
12 marker lines each. TOTAL 374 ≤ 490; PROSE 263 ≤ 400; RECORD41 44 ≤ 140.
G3 SHAPES — PLAN26F→PLAN26T at 4bbfac80: TO contains FROM false, FROM 1x pre / 0x post, TO 1x post,
re-apply reproduces the post blob byte-exactly; numstat 8/9. RECORD41 at 5f592bdd: PREFIX true,
SUFFIX true, pre+slice == post true, ADDED 44 == slice 44 IN ORDER; numstat 44/0. LANDEDF→LANDEDT at
0f7e3f7e against C3's OWN pre blob: FROM 1x pre / 0x post, TO 1x post, re-apply byte-exact;
numstat 15/3. DECISIOND7 at 2f786299: PREFIX/SUFFIX/concat true, ADDED 26 == slice 26 IN ORDER;
numstat 26/0. Marker LINES 0 in all three edited files.
G4 INTEGRATION GATE — merge base a5a70621, unmoved. BRANCH: exit 0, 118.4 s, `17132 passed,
19 skipped`, FAILED 0. BASE (worktree on branch tmp/base-gate-r72, never detached): exit 1, 153.6 s,
`5 failed, 17042 passed, 19 skipped`, FAILED 5. comm -13 branch-only 0 lines; comm -23 base-only
5 lines. PARITY: dist sha256 09463f43…3e51 BEFORE and AFTER (unchanged), index.html mtime
1787160844952953724 → 1787161006911038970 (MOVED) — parity claim VOID on the mtime half, caused by
a real npm install + vite build inside the base worktree despite REMEDY_UI_NO_AUTO_BUILD=1, whose
output was byte-identical; R-0565's blind spot is now demonstrated, not predicted. ATTRIBUTION:
0 branch-only ids, nothing to re-run there; all 5 base-only ids are one environment class —
`apps/ui/dist/index.html` stale BY MTIME in a fresh worktree, `_frontend_is_stale()` trips,
auto-build off, server exits, `_start_server()` times out. Each shows "ERROR: React UI not built."
in the base log and each PASSES on a serial re-run at base (exit 0, `1 passed`) once dist is fresh.
NO BLOCKER: a blocker needs a branch-only id and there is none. R70's one branch-only id
`tests/test_command_discovery.py::TestNoShellTrue::test_run_tests_local_no_shell_true` appears in
NEITHER comm output. Wall budget: both runs under 5 min, no perf note.
G5 PLAN CONTRACT — `.agent/plan.md` 38 lines ≤ 50; `## Goal` true, `## Next Steps` true,
`\bF\d{3}\b` true (F085).
G6 ARITHMETIC — base f023e2b1: 180 registered / 31 done / 1 landed; HEAD: 181 / 32 / 0. OPEN under
DECISION F085 D7 (REG−DONE) = 149 at BOTH SHAs. OPEN under the rejected REG−DONE−LANDED = 148 at
base and 149 at HEAD. Registered symdiff {R-0566}, done symdiff {R-0564}, landed symdiff {R-0564}.
Duplicate ids 0 and resolutions naming an unregistered id 0, at both SHAs. Max registered
R-0565→R-0566, max resolved R-0563→R-0564. Next free id R-0567.
G7 CANARY — `python3 -m pytest tests/cli/test_golden_path.py -q` in the primary checkout: exit 0,
`42 passed in 20.44s`.
G8 HYGIENE — `git diff --name-only f023e2b1..HEAD` before C6 lists 14 paths, ALL under `.agent/`:
authored/f085-r72.md, last_block.md, plan.md, live_review.md, decisions.md and the 9 files under
gate_f085_r72/. No path under `packages/`, `apps/`, `docs/`, `scripts/` or `tests/`; none ends
`.log`. Per-commit insertions before C6: 374, 301, 8, 44, 15, 26, 185 — none over 500. All 8
commits single-parent.

## Authored-text proofs

All six slices were extracted PROGRAMMATICALLY from the committed `.agent/authored/f085-r72.md` by
marker pair under the block's CONVENTION and applied byte-verbatim; slice sha256 prefixes PLAN26F
74f67fb2, PLAN26T d851c3bb, LANDEDF 99f827da, LANDEDT 310013e2, RECORD41 523cab94, DECISIOND7
e5e71c25. Disk-to-disk: transport file and committed copy byte-equal at 8deb1e02…3383. The worker
authored no ledger text (constraint 8).

## External actions

`git worktree add -b tmp/base-gate-r72 .remedy-wt/base-r72 a5a70621` — ok. `git worktree remove
--force` + `git worktree prune` + `git branch -D tmp/base-gate-r72` — ok, list back to one line.
`git push -u origin feature/f085-sandbox-hardening` — see round report. No PR, no merge.

## Deviations & assumptions

No departure from the block's ordered commit sequence: C0a, C0b, C1, C2, C3, C4, C5, C6 exactly.
Deviations, declared — this handback is 138 lines against the ≤100 cap. Stated cause: the mandated
content — 8 per-commit tables, the item-status table, the eight-gate verification block with G4's
full number set, and the authored-text proofs. No section was dropped.
DISAGREEMENT REPORTED, NOT FIXED (constraint 8): RECORD41 says "the correct reading at f023e2b1 is
181 minus 32, that is 149". Measured, f023e2b1 reads 180 registered / 31 done; 181/32 is the HEAD
reading. The value 149 is right at both SHAs and the finding's substance is unaffected, but the
operands are attributed to the wrong SHA. Reported for the reviewer; no slice was edited.
`git worktree remove` needed `--force` because the base run's own npm build dirtied
`apps/ui/package-lock.json` in that worktree — noted, not routed around.

Fortschritt: ~100 % der Bauarbeit; der Regress aus R70 ist repariert und gegengeprüft, R71 PASS, und
das Integration Gate läuft in dieser Runde erneut, weil eine Reparatur nach einem Gate dessen Vergleich
entwertet. R-0564 ist aufgelöst, R-0566 registriert, die Zählregel als DECISION F085 D7 festgeschrieben.
Offen bleibt nur noch die Closure. Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

## Next

FOUR: Phase 1 rule 1 first: re-read `.agent/STOP` from disk — ahead of the PR Gate.
ONE: G4 came back clean (0 branch-only ids, every base-only id attributed), so R73 is CLOSURE per
docs/roadmap/STATUS_closure_protocol.md — evidence job, FRESH review zip, the reviewer-authored
STATUS line, and the PR the operator merges at the next Open PR Gate.
TWO: R72 carries no verdict of its own, because the round that records a verdict cannot record one
on itself (docs/agents/planner_reviewer_prompt.md §4 item 13); R73 carries it.
THREE: open findings under DECISION F085 D7 = 149; next free id R-0567.
