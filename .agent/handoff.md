# Handback — F085 Sandbox hardening (stage 1) · Round R17

Branch: feature/f085-sandbox-hardening. T002a's CLI half completed; behaviour held by five goldens.

## Range
Review of 396ad913..HEAD (this handback commit sits on bc0d3850).

## Commits

### c847ec27 docs(f085): save the R17 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r17.md | +309/-0 | C0a: block copied byte-for-byte (shutil.copyfile) |

### a0bc19de docs(f085): mirror the R17 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +225/-232 | C0b: the COMMITTED C0a blob, not the scratch file |

### 2dae006e docs(review): record the R16 PASS
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +28/-0 | C1: RECORD1 only — a record registers no id |

### 3199f721 feat(f085): route the remaining claude CLI calls through the guard
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pingpong_provider.py | +2/-10 | C2 CALLF→CALLT then STRUCTF→STRUCTT: both spawns become `_guarded_cli_run` |
| tests/orchestration/test_claude_cli_exec_guard.py | +42/-0 | C2 ASTF→ASTT (two new AST assertions) + GOLDF→GOLDT (five behaviour goldens) |
| tests/orchestration/test_structured_cli_envelope.py | +1/-1 | C2 MOCKF→MOCKT: the mock target moves with the spawns — one indivisible unit (R-0507) |

### 23ea5816 docs(review): resolve R-0507 and R-0509 now that their fixes have landed
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +25/-0 | C3: DONE1 then DONE2, appended AFTER C2 landed — separate commit on purpose |

### bc0d3850 docs(f085): advance the plan to the checklist-promotion round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +8/-7 | C4 PLANF→PLANT over Current Step and the first Next Steps item |

### this commit docs(f085): rewrite the handback for R17
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C5: this file — a handoff cannot table the commit that writes it (R-0149) |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit |

## Verification
- G1 `git status --porcelain` rc=0 EMPTY before every commit; `git worktree list` 1 line; `.agent/STOP` absent before C0a and before C5. Observed: the G9 suite transiently creates and removes `tests/regression/test_wrapper_slow_*.py` in the work tree while running — no commit was taken during a run.
- G2 scratch original, `.agent/authored/f085-r17.md` post-C0a and `.agent/last_block.md` post-C0b: sha256 cc496f97e15b8feb9a82368c78493c03f48f1a64c8302dca265874e4fdebb195, 19911 B, 309 lines, byte-equal True.
- G3 C1: pre 6c374ca1… (286462 B), post 98be125d… (289062 B), prefix True, remainder == blank+RECORD1 True, RECORD1 1× in the whole file; numstat READING +28/-0. C3: pre 98be125d…, post 27c1e4ef… (291333 B), prefix True, remainder == blank+DONE1+blank+DONE2 True, DONE1 1× and DONE2 1×; READING +25/-0. Marker lines matching `^<<<(SLICE|END)` = 0 after both commits.
- G4 base 125/4/0 → 121 open; after C1 125/4/0 → 121 open (a record adds no id); HEAD 125/6/0 → 119 open. Symmetric diffs: registered [] (NO registration), resolved R-0507 and R-0509. 0 duplicate registered ids, 0 duplicate resolved ids, 0 resolutions naming an unregistered id. Max R-0510, next free R-0511.
- G5 PLANF 0× / PLANT 1× at HEAD. plan.md sha256 8c68c6ae324fd779094990ee19c5961b35f6df4fcdb6639ef8f085aecc65c9f2, 2704 B, 44 lines (under 50). `## Goal` and `## Risks` byte-identical to base: True/True. `## Next Steps` parses to 1, 2, 3, 4 — no repeat.
- G6 AST over pingpong_provider.py at HEAD, `subprocess.run/Popen/call/check_output` call nodes: `_resolve_version` 0, `_call` 0 (both defs in the module), `_call_reviewer_structured` 0, `_guarded_cli_run` 0. WHOLE MODULE 0 — T002a's CLI half is complete.
- G7 eight-file provider suite: at C1 rc=0 "341 passed"; at HEAD rc=0 "346 passed". The +5 is exactly the five goldens C2 adds; the two readings are NOT equal and must not be reported as equal.
- G8 `python3 -m ruff check pingpong_provider.py test_claude_cli_exec_guard.py test_structured_cli_envelope.py` rc=0 "All checks passed!". Repo-wide ruff not ordered — already red at base.
- G9 state readers rc=0 "157 passed" at base and HEAD; canary `tests/cli/test_golden_path.py` rc=0 "42 passed" at base and HEAD. Both match base.
- G10 `git diff --name-only 396ad913..HEAD` before C5: the 7 declared paths minus handoff, 0 outside. Insertions +309, +225, +28, +45, +25, +8 — none over 500 (C5's own count is not ordered; it is in the round report). `git log --format=%h %p`: 6 commits, one parent each, linear. `git reflog -12`: 0 entries not prefixed `commit:`; no amend, rebase, reset or force-push.

## Authored-text proofs
All 15 slices extracted by marker pair and applied byte-verbatim; no marker line reached any target file (0 in all four). Pair shapes re-classified mechanically by containment before applying, matching constraint 3: CALLF→CALLT, STRUCTF→STRUCTT, MOCKF→MOCKT, ASTF→ASTT, PLANF→PLANT all REWRITE with FROM 1× before and 0× after; GOLDF→GOLDT APPEND, whose FROM legitimately survives 1× inside its own TO, so no "FROM 0×" was read for it. Constraint 4 honoured: CALLT and STRUCTT are byte-identical, each site located by its own distinct FROM, CALLF→CALLT applied first; the shared line occurs 2× in the file afterwards, as expected. Disk-to-disk equality is G2.

## External actions
`git push -u origin feature/f085-sandbox-hardening` and `gh pr list --state open --json number,headRefName,baseRefName,isDraft` run after C5; outputs in the round report. No PR created, nothing merged, no worktree added, removed or pruned.

## Deviations & assumptions
Bundle ran C0a, C0b, C1, C2, C3, C4, C5 in the block's order — none added, dropped or reordered. No gate contradicted the block; no gate came out red. Deviations, declared: this handback is 80 lines and roughly 1.6k tokens, over the 60-line/800-token cap. Cause: seven per-commit changed-files tables, the item-status table, and ten ordered gates whose real readings the block requires. No section was dropped.

## Next
Reviewer re-runs G1-G10 over 396ad913..HEAD and issues the R17 verdict, re-reading `.agent/STOP` first (Phase 1 rule 1 before rule 2). If PASS, the next round promotes three standing rules into docs/agents/planner_reviewer_prompt.md §3 — what R-0508 and R-0510 are still open for.
