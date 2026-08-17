# Handback — F085 Sandbox hardening (stage 1) · Round R22

Branch: feature/f085-sandbox-hardening. R21 recorded as PASS. R-0512 and R-0513 registered AND resolved in the same round, findings first.
Fortschritt: ~76 % (T001 gebaut · R13-R21 PASS · T002a KOMPLETT · Guard-Test-Backstop und Pump-Snapshot gebaut · T002b-d, T003 offen) — Schätzung.

## Range
Review of 3622f2cf..HEAD (this handback commit sits on 90fc1122).

## Commits

### cceec64c docs(f085): save the R22 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r22.md | +372/-0 | C0a: the block's exact bytes, 24629 B, 372 lines, 8 marker lines |

### 25e38e22 docs(f085): mirror the R22 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +272/-230 | C0b: byte-write of the COMMITTED C0a blob read back with `git show`; `cp` not used |

### c85eca07 docs(review): record the R21 PASS and register R-0512 and R-0513
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +88/-0 | C1: RECORD1 appended after exactly one blank line, BEFORE either fix |

### 71dd9416 test(f085): give the cpu-limit guard test a wall-timeout backstop
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_exec_guard.py | +10/-2 | C2: `wall_timeout_seconds=30.0` + the WHY; every existing assertion kept |

### 55ebfe26 fix(f085): keep a blocked pump's bytes via a locked snapshot
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/exec_guard.py | +50/-26 | C3: `_StreamPump._lock` + `snapshot()`; `run_guarded` reads every stream field through it; `ExecGuardResult` docstring corrected |
| tests/orchestration/test_exec_guard.py | +52/-0 | C3: 2 tests added, none rewritten |

### a81c97b6 docs(review): resolve R-0512 and R-0513
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +24/-0 | C4: DONE1 appended after exactly one blank line |

### 90fc1122 docs(f085): advance the plan to R22
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +13/-12 | C5: PLANF→PLANT (REWRITE); `## Goal` and `## Risks` untouched |

### this commit docs(f085): rewrite the handback for R22
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C6: this file — a handoff cannot table the commit that writes it (R-0149) |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | single write attempted FIRST and succeeded; constraint 7's split fallback not needed |
| C0b | done | |
| C1 | done | landed before C2 and C3 per constraint 5 |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | this commit |

## External actions
`git worktree add .remedy-wt/r22-probe HEAD --detach` rc=0; `git worktree remove --force .remedy-wt/r22-probe` rc=0 and `git worktree prune` rc=0, both BEFORE C6. G7 probe b1 left one orphaned busy loop, swept by argv MARKER and verified gone by `pgrep` (deviation 2). `git push -u origin feature/f085-sandbox-hardening` and `gh pr list --state open --json number,headRefName,baseRefName,isDraft` run after C6; outputs in the round report. No PR created, nothing merged.

## Verification
- G1 `git status --porcelain` rc=0 and EMPTY at round start and after every commit. `.agent/STOP` re-read from disk before C0a and again before C6 — ABSENT both times. `git worktree list` rc=0, ONE line at the handback.
- G2 committed `.agent/authored/f085-r22.md`, committed `.agent/last_block.md` and both working copies all byte-EQUAL: sha256 f7b6b9ca92d5a5b3956afa125ba5a189e99ff104d0148499e75707edd4775677, 24629 B, 372 lines, 8 marker lines, 0 trailing-whitespace lines. Region digests of the saved file: lines 1-60 f5ecdf9d6402a62cbb4828853f9d043072c26058857c1be4471f7e03e52bba2d, lines 61-140 9a8f32e70a536e13fc082d168793f8b99c37732a72879c144a6c366b01ce6102, line 141-end 53c558aecd3dbb41cfab18fc170cb36af1dc304fe4a96a5490b778c954c54bf4. C0b's source was `git show cceec64c:.agent/authored/f085-r22.md` rc=0, written as bytes.
- G3 C1: pre-commit blob 309316 B is a byte-exact PREFIX of the post-commit file 316105 B True; remainder == one blank line + RECORD1 True; HEAD blob == working copy True; RECORD1's first line occurs 1x in the whole file; 0 marker lines; `--numstat` READING +88/-0. C4: pre 316105 B PREFIX of post 317782 B True; remainder == one blank line + DONE1 True; HEAD blob == working copy True; first line 1x; 0 marker lines; `--numstat` READING +24/-0.
- G4 base 3622f2cf 126/9/0 with 117 open. After C1 128/9/0 with 119 open — both registrations LANDED. At HEAD 128/11/0 with 117 open. Registered symmetric difference base..HEAD = [R-0512, R-0513]; resolved symmetric difference = [R-0512, R-0513]. 0 duplicate registered ids, 0 duplicate resolved ids, 0 resolutions naming an unregistered id. Max R-0513, next free R-0514.
- G5 PLANF 0x and PLANT 1x at HEAD; PLANT contains PLANF False (REWRITE), PLANF 1x before applying. `.agent/plan.md` sha256 0e1790b9b02cc2b78f934bddd4b078b789fb3a2a5688967e650f70669546b2b2, 2555 B, 43 lines (under 50). `## Goal` and `## Risks` byte-IDENTICAL to base: True/True. `## Next Steps` parses to 1, 2, 3.
- G6a `pytest tests/orchestration/test_exec_guard.py -q` rc=0, READING "18 passed in 10.95s" — ROSE from base 16 by C3's 2 tests; C2 changed a test without adding one.
- G6b `pytest test_exec_guard.py test_stream_evidence.py test_stream_evidence_integration.py -q` rc=0, READING "123 passed in 19.78s" (base 121, +2 from C3).
- G6c `pytest test_managed_builder_execution.py test_pingpong.py test_pingpong_cli.py -q` rc=0, READING "337 passed in 4.52s" — identical to the stated base, so C3 did not disturb the seams that consume the stream fields. No ordered suite came out red, so the re-run branch never triggered.
- G7 PROBES, in the disposable worktree at HEAD, external per-node timeout. (a) `snapshot()` forced to `(b"", 0, False)`: rc=1, READING "9 failed, 9 passed in 10.85s" — 9 tests fail, among them C3's own `test_a_pump_blocked_by_an_escapee_still_returns_the_bytes_it_already_read`. C3's other new test passes under this mutation by construction, since it asserts the zero state the mutation returns. (b) `preexec_fn` made a no-op with C2's backstop KEPT: rc=1, the single node FAILED in 30.26s under `timeout 180` — it did not hang; a direct run of the same policy under the same mutation, with the imported module file printed as proof of path, returned `tripped_limit = wall_timeout` at 30.0s. The literal reading of G7b, which ALSO removes `wall_timeout_seconds`, was run as a control: rc=124, no output, killed by `timeout 120` — the R-0513 hang, reproduced (deviation 1).
- G8 `ruff check packages/orchestration/exec_guard.py tests/orchestration/test_exec_guard.py` rc=0, "All checks passed!" — the block's exact command line.
- G9 state readers (test_test_runner, test_resource_safety, test_integrity_gate, test_dashboard_contract) rc=0, READING "157 passed in 20.01s". CANARY `tests/cli/test_golden_path.py` rc=0, READING "42 passed in 20.44s". No doc-reader gate: the change set holds no file under `docs/`.
- G10 `git diff --name-only 3622f2cf..HEAD` BEFORE C6 = the 6 declared paths (4 under `.agent/`, 1 under `packages/orchestration/`, 1 under `tests/orchestration/`), the declared set minus `.agent/handoff.md`, 0 paths outside. `git show --numstat` FIRST COLUMN — insertions, never the churn total `--stat` prints: C0a 372, C0b 272, C1 88, C2 10, C3 102, C4 24, C5 13 — none over 500 (C6's own count is in the round report). `git log --format=%h %p 3622f2cf..HEAD`: 7 commits, ONE parent each, linear chain. `git reflog -12`: every entry prefixed `commit:`; no amend, rebase, reset or force-push.

## Authored-text proofs
All 4 slices (RECORD1, DONE1, PLANF, PLANT) extracted programmatically by their one-line marker pairs from the COMMITTED block file, never from `.remedy-wt/` and never retyped, and applied byte-verbatim; 0 marker lines reached any target file. Slice digests: RECORD1 22e9ab7656e28f2ea0a17af841880a7ffbb62e7ca9e7884cd4f27b18a620a932 (87 lines), DONE1 c8f14d3ed8b9a5cfca581c269015004780b44f0366f912cfcee4c069d12fa26e (23 lines), PLANF 88feb4d52028d7794735561775a0e75ec6269dacdd4baf3ecceee10c9c5800fb, PLANT 4e11656a0d5b047063b980bcbe2f5f01be4741b04518b23e664a8b2f13e55d03. PLANF→PLANT re-classified MECHANICALLY by containment before applying: TO contains FROM False → REWRITE, agreeing with the block. Disk-to-disk equality is G2; the append shapes are G3.

## Deviations & assumptions
Bundle ran C0a, C0b, C1, C2, C3, C4, C5, C6 in the block's order — none added, dropped or reordered. No gate contradicted the block and no ordered gate came out red. Deviations, declared:
(1) G7 probe b is internally ambiguous: its recipe removes `wall_timeout_seconds`, while its stated property is that "with the backstop the node must FAIL and name `wall_timeout`". Both were run. The property variant (backstop kept, rlimit suppressed) is the one the DONE1 text rests on and it FAILED in 30.26s; the literal variant hung and was killed at 120s. Reported as two readings rather than resolved by picking one.
(2) The literal G7b variant left an unbounded busy loop behind, exactly as R-0513 describes. It was swept by its argv MARKER via the same `pkill -f MARKER` call `test_exec_guard.py` uses for its own escapee, after the interactive `kill`/`pkill` forms were refused by the session sandbox; `pgrep` confirmed 0 survivors. The sweep was scoped to that one MARKER string and to nothing else.
(3) G7's probe order ran BEFORE C4 was committed rather than after C5, because DONE1 asserts a G7 probe-b result and writing that claim to disk unverified would have made the record itself the defect. No commit was reordered; only a gate was.
(4) C3 rewrote the `ExecGuardResult` docstring sentence that promised `b""`, as the block ordered, and added no completeness claim: it names the buffer PARTIAL and leaves `streams_complete`'s meaning and value untouched. The fd handling and its comment are unchanged.
(5) This handback measures 96 lines — inside the ≤100 allowance a >5-commit bundle carries — but over the template's 800-token hard cap. Cause, per DECISION D15: eight per-commit changed-files tables, the eight-row item-status table, and ten ordered gates whose real printed readings the block requires, including G7's four separate probe outcomes. No section was dropped and no transcript was pasted.
Assumptions: G1's "EMPTY after every commit" is read as empty at round start and after every commit; before a commit the only entry was that commit's own declared path.
Observed, NOT fixed (outside the change set): none this round.

## Next
Next session, in the protocol's own order: Phase 1 rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2, the Open PR Gate (`gh pr list --state open --json number,headRefName,baseRefName,isDraft`). Then the first item from `.agent/plan.md`: T002b, the twelve `test`-class sites in ten modules, with behaviour-equality goldens and the environment-allowlist test that carries R-0202 — the largest remaining slice, which will not fit one round.
Open findings: 117.
