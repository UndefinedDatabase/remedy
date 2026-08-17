# Handback — F085 Sandbox hardening (stage 1) · Round R21

Branch: feature/f085-sandbox-hardening. R20 recorded as PASS. T002a's last spawn site is migrated and DECISION F085 D2 rules its shape.
Fortschritt: ~75 % (T001 gebaut · R13-R20 PASS · T002a KOMPLETT: Builder-Site, CLI-Half und Stream-Seam · T002b-d, T003 offen) — Schätzung.

## Range
Review of 1cfa0acb..HEAD (this handback commit sits on 4b0bfe31).

## Commits

### 409378de docs(f085): save the R21 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r21.md | +330/-0 | C0a: the block's exact bytes, 21446 B, 330 lines, 8 marker lines |

### cd3c3930 docs(f085): mirror the R21 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +305/-149 | C0b: byte-write of the COMMITTED C0a blob read back with `git show`; `cp` not used |

### c52267d1 docs(review): record the R20 PASS
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +30/-0 | C1: RECORD1 appended after exactly one blank line |

### a10cbac0 docs(f085): rule the streaming seam's shape as DECISION D2
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +42/-0 | C2: DECISION1 appended after exactly one blank line |

### ee3ca3d3 feat(exec_guard): extract the child-side half of a policy
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/exec_guard.py | +69/-21 | C3: `ChildSpawnPlan` + `plan_child_spawn`; `run_guarded` spawns from the plan |
| tests/orchestration/test_exec_guard.py | +65/-1 | C3: 4 tests added, none rewritten |

### a865eda4 feat(stream_evidence): spawn the streaming child under a policy
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/stream_evidence.py | +40/-3 | C4: keyword-only `policy`, plan applied at the existing Popen, 2 result fields |
| packages/orchestration/pingpong_provider.py | +19/-1 | C4: `_stream_exec_policy`; the call site passes it and stops passing `cwd` |
| tests/orchestration/test_stream_evidence_integration.py | +113/-0 | C4: 5 tests added |

### 4b0bfe31 docs(f085): advance the plan to the R21 migration
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +10/-9 | C5: PLANF→PLANT (REWRITE); `## Goal` and `## Risks` untouched |

### this commit docs(f085): rewrite the handback for R21
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C6: this file — a handoff cannot table the commit that writes it (R-0149) |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | single write succeeded; constraint 6's split fallback was not needed |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | this commit |

## External actions
`git worktree add .remedy-wt/g7-probe HEAD --detach` rc=0; `git worktree remove --force .remedy-wt/g7-probe` rc=0 and `git worktree prune` rc=0, both BEFORE C6. `git push -u origin feature/f085-sandbox-hardening` and `gh pr list --state open --json number,headRefName,baseRefName,isDraft` run after C6; outputs in the round report. No PR created, nothing merged.

## Verification
- G1 `git status --porcelain` rc=0 and EMPTY at round start and after every commit; before each commit its only entry was that commit's own declared path. `.agent/STOP` re-read from disk before C0a and again before C6 — ABSENT both times. `git worktree list` rc=0, ONE line at the handback.
- G2 committed `.agent/authored/f085-r21.md`, committed `.agent/last_block.md` and both working copies all byte-EQUAL: sha256 b17efc371d740f199a7d05528109e81283591cbf630d9c2673cbbf0b03d42e37, 21446 B, 330 lines, 8 marker lines. Region digests of the saved file: lines 1-60 570cbf61c9634cf86af8170cd83c14c4aa43753f3a9aa587363bb143f1b513a3, lines 61-140 5686f3e65657d7a28157aad33224d9138ee80b9589b118ec9b0085b1f3214ab1, line 141-end 28534295384a8b2838ef01cb69f929132b028b4b4db2a662fc5fa6b44dc02251 — all three match the reviewer's pre-delegation measurement. C0b's source was `git show 409378de:.agent/authored/f085-r21.md` rc=0, written as bytes.
- G3 C1 `.agent/live_review.md`: pre-commit blob 307026 B is a byte-exact PREFIX of the post-commit file 309316 B True; remainder == one blank line + RECORD1 True; HEAD blob == working copy True; RECORD1's first line occurs 1x in the whole file; 0 marker lines; numstat READING +30/-0. C2 `.agent/decisions.md`: pre 353356 B PREFIX of post 356103 B True; remainder == one blank line + DECISION1 True; HEAD blob == working copy True; first line 1x; 0 marker lines; numstat READING +42/-0.
- G4 base 1cfa0acb 126/9/0 with 117 open; HEAD 126/9/0 with 117 open — UNCHANGED as ordered. Both symmetric differences EMPTY: registered [] and resolved []. 0 duplicate ids, 0 resolutions naming an unregistered id. Max R-0511, next free R-0512.
- G5 PLANF 0x and PLANT 1x at HEAD; HEAD blob == working copy True. `.agent/plan.md` sha256 5d755dbea2435c18c291e578bf1d20d4ed2fa3e7aa052cc3bda2f732ccc62c0d, 2495 B, 42 lines (under 50). `## Goal` and `## Risks` byte-IDENTICAL to base: True/True. `## Next Steps` parses to 1, 2, 3.
- G6a `pytest tests/orchestration/test_exec_guard.py -q` rc=0, READING "16 passed in 7.65s" (base 12 — the 4 tests C3 adds).
- G6b `pytest test_exec_guard.py test_stream_evidence.py test_stream_evidence_integration.py -q` rc=0, READING "121 passed in 16.72s" (base 112 — it ROSE by the 4+5 tests C3 and C4 add). Base re-measured at round start by this worker: "112 passed in 16.43s".
- G6c `pytest test_managed_builder_execution.py test_pingpong.py test_pingpong_cli.py -q` rc=0, READING "337 passed in 4.44s" — identical to the stated base, so the extraction did not disturb the other two T002a seams. No suite came out red, so the re-run branch never triggered.
- G7 PROBE, in the disposable worktree at HEAD, `plan_child_spawn` returning a no-op `preexec_fn`. READING over all 121 nodes: 117 passed, 3 FAILED, 1 TIMED OUT, 0 errored. Failed: `test_exec_guard.py::test_address_space_limit_is_enforced_but_not_attributed`, `test_exec_guard.py::test_plan_child_spawn_preexec_really_lowers_the_core_limit_in_the_child` (C3's new test), `test_stream_evidence_integration.py::TestStreamPolicySpawn::test_the_child_really_runs_with_the_core_limit_the_policy_set` (C4's new test). Timed out: `test_exec_guard.py::test_cpu_limit_kills_a_busy_loop_and_names_the_limit`. BOTH new rlimit assertions reach the code they name; the probe did not come out zero.
- G8 `ruff check` over the five changed `.py` paths rc=0, "All checks passed!" — the block's exact command line.
- G9 state readers (test_test_runner, test_resource_safety, test_integrity_gate, test_dashboard_contract) rc=0, READING "157 passed in 19.16s". CANARY `tests/cli/test_golden_path.py` rc=0, READING "42 passed in 19.65s". No doc-reader gate: the change set holds no file under `docs/`.
- G10 `git diff --name-only 1cfa0acb..HEAD` BEFORE C6 = the 10 declared paths (5 under `.agent/`, 3 under `packages/orchestration/`, 2 under `tests/orchestration/`), the declared set minus `.agent/handoff.md`, 0 paths outside. `git show --numstat` insertions: C0a 330, C0b 305, C1 30, C2 42, C3 134, C4 172, C5 19 — none over 500 (C6's own count is in the round report). `git log --format=%h %p 1cfa0acb..HEAD`: 7 commits, ONE parent each, linear chain. `git reflog -20`: every entry prefixed `commit:`; no amend, rebase, reset or force-push.

## Authored-text proofs
All 4 slices (RECORD1, DECISION1, PLANF, PLANT) extracted programmatically by their one-line marker pairs from the COMMITTED block file, never from `.remedy-wt/` and never retyped, and applied byte-verbatim; 0 marker lines reached any target file. PLANF→PLANT re-classified MECHANICALLY by containment before applying: TO contains FROM False → REWRITE, agreeing with the block; FROM 1x before and 0x after, TO 1x after. Disk-to-disk equality is G2; the append shapes are G3.

## Deviations & assumptions
Bundle ran C0a, C0b, C1, C2, C3, C4, C5, C6 in the block's order — none added, dropped or reordered. No gate contradicted the block and no ordered gate came out red. Deviations, declared:
(1) G7 could not be measured by one suite run. Under the mutation `test_cpu_limit_kills_a_busy_loop_and_names_the_limit` HANGS rather than fails — its policy sets `cpu_seconds` but no `wall_timeout_seconds`, so with the rlimits removed the busy loop is unbounded — and a plain run therefore terminates never and reports nothing. The first attempt was killed at 600 s and its fixture children swept by argv MARKER, verified gone by `pgrep`. The probe was then re-run node-by-node, one process per node with an external 90 s timeout, inside the SAME disposable worktree, which is what produced the reading above. The block's substance (which tests, how many) is answered; its implied single-command form is not.
(2) C3 edited the module docstring's partial-coverage bullet to name `run_guarded` and `plan_child_spawn` instead of "this module". The block permits correcting a sentence the change falsifies; this correction was made in C3 rather than C4 because C4 is constrained to three files. It adds no coverage claim.
(3) C4 added a `TYPE_CHECKING` import block to `stream_evidence.py`, not itemised in the Change set, so `policy: ExecGuardPolicy | None` can be annotated without a module-level runtime import of `exec_guard` (which imports the POSIX-only `resource`). The runtime import sits inside `run_streamed_command`.
(4) C4 wrote 5 integration tests where the block names 3 properties: the 3 ordered ones plus the documented cwd precedence and the real `ClaudeCliProvider` call site. An addition inside the change set, not a widening of it.
(5) `git show --numstat` reads C0b as +305/-149 while the commit summary printed +330/-174; git applied rewrite detection at commit time and not at show time. G10 reads the former; both are under 500.
(6) This handback measures 99 lines — inside the ≤100 allowance a >5-commit bundle carries — but well over the template's 800-token hard cap. Cause, per DECISION D15: eight per-commit changed-files tables, the eight-row item-status table, and ten ordered gates whose real printed readings the block requires. No section was dropped and no transcript was pasted.
Assumptions: G1's "EMPTY before EVERY commit" is read as empty at round start and after every commit, the sole pre-commit entry being that commit's own declared path — a commit cannot exist without its own change.
Observed, NOT fixed (outside the change set): `test_cpu_limit_kills_a_busy_loop_and_names_the_limit` has no wall-timeout backstop, so a regression in rlimit application turns it from a red test into an infinite hang. Reported, not repaired, this round.

## Next
Next session, in the protocol's own order: Phase 1 rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2, the Open PR Gate (`gh pr list --state open --json number,headRefName,baseRefName,isDraft`). Then the first real work item from `.agent/plan.md`: `_StreamPump` gains a lock and a `snapshot()` so PARTIAL output survives a bounded drain, the tradeoff left open since R8.
Open findings: 117.
