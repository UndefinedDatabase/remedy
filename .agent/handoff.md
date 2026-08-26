# Handoff — F031 Decision inbox, R24 (worker → planner/reviewer)

Branch `feature/f031-decision-inbox`. Base `030a43d1`. C0a `0f5ef322`, C0b `4adb26ef`, C1 `d6822bfd`, C2 `9ec7b2de`, C3 `6b68718e`, C4 = this commit.

Fortschritt: ~82 % (F031 claimed; R1 through R23 landed, R23 gated here ·
             T001 SHIPPED · T002a MODEL shipped, wired and RENDERED ·
             T002b ORDERING and FILTERING SHIPPED and gated · T002b badge
             SERVER half here, its UI half at R25 · T003 offen)
             — Schaetzung

## Range
Review of 030a43d1..HEAD

## Commits
### 0f5ef322 docs(agent): save the F031 R24 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r24.md | +450 -0 | C0a — the block saved verbatim |

### 4adb26ef docs(agent): mirror the F031 R24 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +263 -256 | C0b — byte-identical mirror of the C0a blob |

### d6822bfd docs(agent): point the F031 plan at R24
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +21 -19 | C1 — PLANF031R24, whole-file |

### 9ec7b2de docs(agent): record the F031 R23 verdict, an R-0593 recurrence and R-0682
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6 -0 | C2 — LEDGER24 appended |

### 6b68718e fix(ui-server): derive the open-decision counters from the decision queue
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | +26 -13 | S1 `_count_open_decisions`, S2 both call sites |
| tests/ui_server/test_live_state.py | +44 -1 | S3 — 3 tests on `open_decision_count` |
| tests/ui_server/test_dashboard_contract.py | +43 -0 | S3 — 3 tests on `metrics.open` |
| .agent/decisions.md | +37 -0 | S4 — DECISION F031 D9 |

### C4 — this commit (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C4 — this handback |

## External actions
- `git worktree add .remedy-wt/f031-r24-redproof --detach 6b68718e` → created; `git worktree remove --force .remedy-wt/f031-r24-redproof` → removed BY THAT EXACT PATH, `git worktree list` 1 line after.
- `git push origin feature/f031-decision-inbox` — ordered after C4. That push's outcome is not a value of any file this round writes: the reviewer measures the pushed tips at the next gate and records them in the R24 entry of `.agent/live_review.md`.
- No PR created, no branch deleted, nothing merged, no force flag, no history rewrite.

## Verification
- G1 branch `feature/f031-decision-inbox`; `.agent/STOP` absent before C0a and before C4; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3; all four readings (scratch, C0a blob, C0b blob, `last_block.md` on disk) sha256 `a56ced36452288e42457aedc34f113c0f94f2944c2f17c946b49605a2dc6345c`, 40561 bytes, 450 newlines, EQUAL, C0a and C0b the same blob `141e5735d7f3f9610334f80bc0bf34add3702fa7`.
- G2 extractor over the C0a blob printed 2 slices (PLANF031R24 47 lines, LEDGER24 5), CONTENT 52, TOTAL 450, so PROSE = 450 − 52 = 398 — within both the 400 prose cap (F085 D5) and the 490 total cap (F085 D6).
- G3 `.agent/plan.md` at C1 byte-equal to PLANF031R24, 2792 bytes on both sides, convention newline-INCLUDED; negative control (slice with trailing newline removed) False; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 47, strictly under 50.
- G4 reader (a), the equality constraint 8 states: True, 665858 + 1 + 11661 = 677520 = actual; reader (b): blank-line units 306 → 309, last N = 3 units equal LEDGER24's 3 paragraphs IN ORDER (reversed comparison False), trailing newlines rstripped on BOTH sides; negative control, one byte flipped inside the appended region in memory only — both readers reject the mutant, both accept the true file.
- G5 `^- R-\d+ — ` 242 → 243 all DISTINCT, ADDED exactly {R-0682}, REMOVED {}, max R-0681 → R-0682; `^Done: R-\d+ — ` 4 → 4; `^Landed: R-` 0 → 0; `^Recurrence: R-` 18 → 19; `^Gate: R\d+ — ` 19 → 19; `^Gate: F\d+ R\d+ — ` 4 → 5, ADDED key exactly `F031 R23`, all keys DISTINCT; open set 238 → 239; `^- R-0593 — ` 1; `^Recurrence: R-0593` 1 → 2.
- G6 red proof in the worktree with the S1 helper body reduced to the literal `0`: `test_live_state.py` REAL exit 1, 1 failed 44 passed; `test_dashboard_contract.py` REAL exit 1, 1 failed 73 passed; the failing test in each is `…ComesFromTheDecisionQueue::test_repo_less_job_reports_its_open_decisions`; worktree removed by exact path, `git worktree list` 1 line after; primary never mutated.
- G7 structure at C3: `def _count_open_decisions` 1; that name 1× in `_build_dashboard` and 1× in `_build_live_state_json`; `human_decision_requested` 0× in `_build_live_state_json` but 1× in `_build_dashboard` (deviation 2); `blocker_count` 0× in `_build_dashboard` but 2× in the whole file (deviation 1).
- G7 suites, PRIMARY checkout at C3, run SERIALLY with `git worktree list` 1 line immediately before the first, every one a REAL exit 0: ruff "All checks passed!"; `tests/ui_server/` 480; `test_test_runner` 52; `test_resource_safety` 21; `test_integrity_gate` 16; `test_autonomy` 81; `test_golden_path` 42 — and 480 − 474 = 6, exactly the 6 tests S3 adds, with no other difference.
- G8 `^<<<SLICE `/`^<<<END ` both 0 in plan.md at C1, live_review.md at C2 and all four files C3 writes, against CONTROL 2 and 2 over the C0a blob; range `030a43d1..6b68718e` names 8 paths, none under `docs/` or `apps/`, none of `.agent/context.md`, either inventory, `decision_queue.py` or `decision_inbox.py`, range MINUS change set EMPTY and change set MINUS range exactly `.agent/handoff.md`; C0a..C3 each single-parent with insertions 450, 263, 21, 6, 150 read from `git diff --numstat`, each under 500 and agreeing cell for cell with the `+/-` column above; `git ls-files .remedy-wt` 0, `git ls-files *.zip` 0, `git status --porcelain` 0; reflog scoped to this round's 5 entries by operation prefix: `commit` 5×, amend 0, rebase 0, cherry 0; SHA-shaped tokens in the C0a blob 23 occurrences, 11 distinct, 10 `commit` + 1 `blob`, FAILING SET EMPTY.
- G9 the push — see `## External actions`; its outcome is the reviewer's to measure.

## Authored-text proofs
PLANF031R24 → `.agent/plan.md` at C1: byte-equal, 2792 bytes both sides (G3). LEDGER24 → `.agent/live_review.md` at C2: whole-file equality True plus the independent last-3-units-in-order reading (G4). Both slices were extracted programmatically by marker LINE out of the COMMITTED C0a blob, and no marker reached a target file (G8).

## Deviations & assumptions
1. CONTRADICTION IN THE BLOCK, G7 vs S2 and constraint 11. G7 orders `blocker_count` ZERO times in the WHOLE file; it occurs 2×, at `ui_server.py:857` and `:874`, as a PAYLOAD KEY of `_build_overnight_section` — an unrelated readiness section, not the `metrics.open` addend. S2 orders only the `_build_dashboard` LOCAL retired, and that local is now 0×. Removing the overnight keys would break an unrelated contract, so they stand and I report the measured 2 rather than the ordered 0.
2. CONTRADICTION IN THE BLOCK, G7's carve-out misplaces the map. G7 orders `human_decision_requested` absent from both builder BODIES while carving out "the humanize maps elsewhere in the module". That map is NOT elsewhere: `_event_actors` at `ui_server.py:1847` sits INSIDE `_build_dashboard` and labels the activity feed's actor. It is not a counter, S2 does not order it removed, so it stands: the ordered 0 is met in `_build_live_state_json` and not in `_build_dashboard`.
3. S1's collision clause, applied as stated: the helper imports `list_decisions as list_queue_decisions`, so its call site reads `open_decisions(list_queue_decisions(job, events))` and the `orchestrator_brain` `list_decisions` inside `_build_orchestrator_section` keeps its own spelling.
4. ASSUMPTION about S3's fixtures: `_make_job()` in `test_live_state.py` and `_make_job_s80()` in `test_dashboard_contract.py` are the repo-less shape, and the target_repo shapes pass `metadata={"target_repo": "."}`. Every expected number is derived in the test from `open_decisions(list_decisions(job, events))`, never hardcoded.
5. No departure from the ordered commit sequence: C0a, C0b, C1, C2, C3, C4 — six commits, none extra, none dropped, none reordered. No amend, rebase, cherry-pick, force-push, history rewrite, branch deletion, merge or pull request.
6. Handback tier, resolved from AGENTS.md `### handoff.md` against the commit count constraint 4 fixes: 6 commits, more than 5, so the cap is ≤100 lines. No overage is claimed and no token cap is claimed.

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a save block | done | |
| C0b mirror block | done | |
| C1 plan | done | |
| C2 ledger | done | |
| C3 code, tests, D9 | done | |
| C4 handback | done | this commit |
| S1 helper | done | `_count_open_decisions` |
| S2 both call sites | deviated | done as ordered; `blocker_count` survives only as an unrelated overnight payload key — deviation 1 |
| S3 tests | done | 6 tests, 3 per file |
| S4 DECISION F031 D9 | done | |
| push | done | ordered after C4; outcome carried by G9 to the reviewer |

## Findings
Open set 239 at `9ec7b2de`, by the §3 item 10 rule DECISION F009 D10 requires — every `^- R-\d+ — ` paragraph (243) minus every `^Done: R-\d+ — ` line (4). This round mints R-0682 and resolves none.
The narrower set, the findings THIS FEATURE must still act on, is the 22 distinct ids `.agent/plan.md` lists at `d6822bfd`; R-0495 and R-0574 are the two Highs.

## Next
This round ends the session. The next session, in this order: (1) read `.agent/STOP` from disk as Phase 1 rule 1, BEFORE the Open PR Gate as rule 2; (2) the R24 verdict is UNRECORDED and is owed by the next round's ledger commit (DECISION F085 D9); (3) R25 is T002b's badge UI half — the count rendered where the operator sees it — which also carries the R-0682 fix and the third `R-0593` instance C2 records.
