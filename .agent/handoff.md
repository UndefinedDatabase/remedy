# Handback — F085 Sandbox hardening (stage 1) · Round R16

Branch: feature/f085-sandbox-hardening. Record-and-repair round, no behaviour change.

## Range
Review of 7185d949..HEAD (this handback commit sits on 50c279b7).

## Commits

### f05b68e5 docs(f085): save the R16 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r16.md | +316/-0 | C0a: block copied byte-for-byte (shutil.copyfile) |

### 7a94b0e3 docs(f085): mirror the R16 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +240/-324 | C0b: the COMMITTED C0a blob, not the scratch file |

### d320f79f docs(review): record the R15 PASS and register three block defects
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +74/-0 | C1: RECORD1 (R15 PASS) + FIND1/2/3 = R-0508, R-0509, R-0510 |

### 178152f3 docs(f085): correct the absence claims the guard migration falsified
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/exec_guard.py | +8/-5 | C2 EGF→EGT: PARTIAL COVERAGE replaces "NO CALLER"; allowlist is the caller's |
| packages/orchestration/managed_builder_execution.py | +8/-5 | C2 MBE1/MBE2: LAUNCH not invoke; "No shell, ever" + AST pointer |

### 093cfabc docs(review): resolve R-0506 now that its fix has landed
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +17/-0 | C3: DONE1, appended AFTER C2 landed — separate commit on purpose |

### 50c279b7 docs(f085): advance the plan and repair its numbering
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +9/-9 | C4 PLANF→PLANT over the whole Next Steps section; 1,2,2,3 → 1,2,3,4 (R-0509 repair) |

### this commit docs(f085): rewrite the handback for R16
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
- G1 `git status --porcelain` rc=0 EMPTY before every commit; `git worktree list` 1 line; `.agent/STOP` absent before C0a and before C5.
- G2 scratch original, `.agent/authored/f085-r16.md` post-C0a and `.agent/last_block.md` post-C0b: sha256 bda1ca21008ed866792258791cd785bbde79b9aa975c7c018fbaf50fe82e903e, 22488 B, 316 lines, byte-equal True.
- G3 C1: pre f8a58f0d…, post 52a1dd28…, prefix True, remainder == blank+RECORD1+blank+FIND1+blank+FIND2+blank+FIND3 True, each slice 1×; numstat READING +74/-0. C3: pre 52a1dd28…, post 6c374ca1…, prefix True, remainder == blank+DONE1 True, DONE1 1×; READING +17/-0. Marker tokens 1 `<<<SLICE`/1 `<<<END` before and after both commits (pre-existing R7 prose).
- G4 base 122/3/0 → 119 open; after C1 125/3/0 → 122 open; HEAD 125/4/0 → 121 open. Symmetric diffs: registered R-0508, R-0509, R-0510; resolved R-0506. 0 duplicate ids, 0 resolutions of an unregistered id. Max R-0510, next free R-0511.
- G5 PLANF 0× / PLANT 1× at HEAD. plan.md sha256 8472adc781a6130bcf983c3e7dbccbe47307400e7e64ef46b39c422087e4c4a2, 2589 B, 43 lines. `## Goal` and `## Risks` byte-identical to base: True/True. Next Steps numbers parsed: base 1,2,2,3 → HEAD 1,2,3,4.
- G6 HEAD blobs of both files: "NO CALLER" 0/0; "ONLY place in the codebase that may invoke subprocess" 0/0; "ONLY function that executes a subprocess" 0/0. `git grep -l "from packages.orchestration.exec_guard import" -- packages tests` rc=0, 4 paths: managed_builder_execution.py, pingpong_provider.py, test_exec_guard.py, test_managed_builder_execution.py.
- G7 managed_builder + exec_guard + claude_cli_exec_guard: at C1 rc=0 "152 passed"; at HEAD rc=0 "152 passed".
- G8 `ruff check exec_guard.py managed_builder_execution.py` rc=0 "All checks passed!" at base and HEAD. Repo-wide ruff not ordered — already red at base.
- G9 state readers rc=0 "157 passed" base and HEAD; canary `tests/cli/test_golden_path.py` rc=0 "42 passed" base and HEAD.
- G10 `git diff --name-only 7185d949..HEAD` before C5: the 6 declared paths minus handoff, 0 outside, 0 untouched. Insertions +316, +240, +74, +16, +17, +9 — none over 500. `git log --format=%h %p`: 6 commits, one parent each, linear. `git reflog -12`: 0 entries not prefixed `commit:`.

## Authored-text proofs
All 13 slices extracted by marker pair and applied byte-verbatim; no marker line reached a target. Pair shapes re-classified mechanically by containment: EGF→EGT, MBE1F→MBE1T, MBE2F→MBE2T, PLANF→PLANT all REWRITE, matching constraint 3. Each FROM occurred 1× before and 0× after. Disk-to-disk equality is G2. The whole block was dry-run on a `git archive HEAD` extraction first: 4 pairs applied, ruff rc=0, AST parse rc=0, numbering 1,2,3,4, retired phrases 0.

## External actions
`git push -u origin feature/f085-sandbox-hardening` and `gh pr list --state open --json number,headRefName,baseRefName,isDraft` run after C5; outputs in the round report. No PR created, nothing merged, no worktree added or removed.

## Deviations & assumptions
Bundle ran C0a, C0b, C1, C2, C3, C4, C5 in the block's order — none added, dropped or reordered. No gate contradicted the block. Deviations, declared: this handback is 79 lines and roughly 1.4k tokens, over the 60-line/800-token cap. Cause: seven per-commit changed-files tables, the item-status table, and ten ordered gates whose real readings the block requires. No section was dropped.

## Next
Reviewer re-runs G1-G10 over 7185d949..HEAD and issues the R16 verdict, re-reading `.agent/STOP` first. If PASS, R17 migrates the R-0507 coupled unit: `_call`, `_call_reviewer_structured` and the envelope test's mock.
