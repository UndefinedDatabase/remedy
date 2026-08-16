# Handback — F085 Sandbox hardening (stage 1) · R15

Branch: feature/f085-sandbox-hardening. No PR created, nothing merged.

## Range
Review of c5d80471..HEAD, HEAD being this handback commit (a commit cannot name its own SHA).

## Commits

### 49fdb0c0 docs(f085): save the R15 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r15.md | +400/-0 | C0a — block copied via `shutil.copyfile` |

### c839faa8 docs(f085): mirror the R15 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +339/-153 | C0b — the COMMITTED C0a blob, not the scratch file |

### 41d6e0b0 docs(review): record the R14 PASS and register a scoping finding
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +50/-0 | C1 — RECORD1 then FIND1 appended |

### 75267002 feat(f085): give the claude CLI seam its guarded runner
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pingpong_provider.py | +57/-5 | C2 — IMP1/2/3, three helpers, `_resolve_version` onto `_guarded_cli_run` |
| tests/orchestration/test_claude_cli_exec_guard.py | +77/-0 | C2 — NEW goldens spawning a real fake CLI |

### 2847ccac docs(f085): advance the plan to the R15 CLI runner round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +9/-8 | C3 — PLANF→PLANT |

### this commit docs(f085): rewrite the handback for R15
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | self | C4 — this file (R-0149 self-reference) |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |

## External actions
`git push -u origin feature/f085-sandbox-hardening`, then `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — outputs in the round report. No PR created or merged, no worktree added or removed, `remedy` never called.

## Verification
Ten ordered gates, each RUN, real exit codes.
- G1 — `git status --porcelain` EMPTY before every commit; `.agent/STOP` ABSENT on disk before C0a and before C4; `git worktree list` = 1 line.
- G2 — `.remedy-wt/f085-r15.md` == `.agent/authored/f085-r15.md` (post-C0a) == `.agent/last_block.md` (post-C0b): sha256 e2f4ef715c40f02df7d552e15348268b2d0edb24b986ff91e762c666314e2d88, 22895 B, 400 lines. C0b read `git cat-file blob HEAD:.agent/authored/f085-r15.md`.
- G3 — pre-C1 blob is a byte-exact PREFIX of the post-C1 file; HEAD blob == worktree file; remainder byte-equals blank+RECORD1+blank+FIND1 in order; each slice 1× in the whole file; 0 marker lines added (the single pre-existing `<<<` is R7 prose, 1 at base and 1 at HEAD). numstat READING: `50 0`.
- G4 — base 121/3/0 = 118 open; HEAD 122/3/0 = 119 open, rise of exactly one. registered and open HEAD−base = {R-0507}, base−HEAD = {} both ways, resolved HEAD−base = {}. 0 duplicate ids, 0 resolutions naming an unregistered id, max R-0507, next free R-0508. OPEN FINDINGS: 119.
- G5 — PLANF 0× at HEAD, PLANT 1×. `.agent/plan.md` sha256 2bc83535db136fb6ee1e8dc4a5611cb70f3c44f0a7464612056903386247b189, 2603 B, 43 lines (<50). `## Goal` and `## Risks` byte-IDENTICAL to base; `## Current Step` and `## Next Steps` not.
- G6 — `pytest tests/orchestration/test_claude_cli_exec_guard.py -q` exit 0, `8 passed in 1.40s`. By AST over the HEAD blob, `subprocess.run/Popen/call/check_output` nodes: `_resolve_version` 0, `_guarded_cli_run` 0, `_call` 1, `_call_reviewer_structured` 1.
- G7 — the seven-file set: exit 0 `333 passed` at C1 (base reading) and exit 0 `333 passed` at HEAD. Equal.
- G8 — `ruff check packages/orchestration/pingpong_provider.py tests/orchestration/test_claude_cli_exec_guard.py` exit 0, `All checks passed!`.
- G9 — state readers exit 0, `157 passed` at base and at HEAD. Canary `tests/cli/test_golden_path.py` exit 0, `42 passed` at base and at HEAD.
- G10 — `git diff --name-only c5d80471..HEAD` BEFORE C4 is exactly `.agent/authored/f085-r15.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `packages/orchestration/pingpong_provider.py`, `tests/orchestration/test_claude_cli_exec_guard.py`; 0 paths outside the declared set. Insertions C0a 400, C0b 339, C1 50, C2 134, C3 9 — none over 500; C4's own count is ordered nowhere and goes in the round report. ONE parent per commit, linear 49fdb0c0←c839faa8←41d6e0b0←75267002←2847ccac from c5d80471; last 20 reflog entries all `commit:`, no amend, rebase, reset or force-push.

## Authored-text proofs
Disk-to-disk, not by digest fallback: the three files above are byte-EQUAL at sha256 e2f4ef71…314e2d88, 22895 B / 400 lines. All 15 slices were extracted programmatically by their marker pair and applied byte-verbatim; every FROM was located exactly once before replacement; 0 `<<<SLICE`/`<<<END` lines reached any target file.

## Deviations & assumptions
No commit was added, dropped or reordered: C0a, C0b, C1, C2, C3, C4 ran as ordered. Three observations, none a scope change, none repaired:
1. IMP3 is APPEND-shaped, not a REWRITE: IMP3T CONTAINS IMP3F, so IMP3F still occurs 1× at HEAD, where constraint 3 classes every non-CLST pair a REWRITE. The pair applied correctly — its FROM occurred exactly once and was replaced once — and no gate ordered an "IMP3F 0×" reading.
2. `.agent/plan.md` Next Steps now numbers 1, 2, 2, 3: PLANF's FROM ends after the old item 1, so PLANT's new item 2 lands ahead of the surviving old items 2 and 3. Left as authored; repairing it would reword a slice, which constraint 2 forbids. G5 passes as written.
3. The Change set heading says "exactly these SIX paths" and enumerates SEVEN. Measured: 7 across the bundle, 6 before C4 — the reading G10 orders.
Deviations, declared: this handback is 78 lines, over the ≤60 baseline and within the ≤100 allowed for a bundle of more than five commits. The length is set by mandated content — six per-commit tables, the ten-gate verification table, the item-status table, the transport and pair proofs. No section was dropped to meet the cap.

## Next
The reviewer re-runs G1-G10 over c5d80471..HEAD and issues the R15 verdict. Phase 1 rule 1 first: re-read `.agent/STOP` from disk.
