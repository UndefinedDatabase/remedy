# Handoff — F105 R31 (the mission-plan evidence sink, and R-0257 fixed)

Branch: feature/f105-cache-optimal-prompt-ordering. Base of this round: 0ba30611.
Commits, in order: 176666af (C1a), 974ce1aa (C1b), be125608 (C2), 3d37567f (C3),
45765a8f (C4), db3bdef3 (C5), plus this C6 commit (plan + handoff).

## Changed files
| Path | What |
|---|---|
| .agent/authored/f105-r31-1.md | R31 block saved verbatim (new, 384 lines) |
| .agent/last_block.md | the same 384 lines, mirrored |
| .agent/live_review.md | PAIR_A: R30 round line, the PASS record, R-0257; PAIR_B: next free ID R-0258; plus the one `Landed: R-0257` line |
| packages/orchestration/mission_compiler.py | PAIR_C: composition back inside the try; PAIR_D/E: `plan_mission` owns the traces list and appends them |
| apps/cli/commands/mission_cmd.py | PAIR_F: `remedy mission plan` names the provider |
| tests/orchestration/test_mission_compiler.py | PAIR_G plus the one mandated import line |
| .agent/plan.md | PAIR_H full replacement, 42 lines |
| .agent/handoff.md | this file |

## Items
| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | |

## Gates (real exit codes, real output)
| Gate | Exit | Output |
|---|---|---|
| A transport | 0 | reviewer original, authored copy and last_block all `8833261bcf731bec965fbcd52ff7aa8339141a5ae076397cfeee41232f307003`; three `cmp` runs silent |
| B size | 0 | `384 .agent/authored/f105-r31-1.md` — under DECISION F105 D5's cap of 400 |
| C application | 0 | per-pair proofs below |
| D markers | 1 (grep no-match) | `grep -c -E '^<<<'` prints `0` in `.agent/live_review.md`, `mission_compiler.py`, `mission_cmd.py`, `test_mission_compiler.py` and `.agent/plan.md` |
| E touched suite | 0 | `126 passed in 0.55s` |
| F callers | 0 | `78 passed in 1.20s`; `tests/cli/` `1329 passed in 260.58s (0:04:20)` |
| G red-proof M1 | 1 | worktree at db3bdef3, `PYTHONDONTWRITEBYTECODE=1`, `append_trace_jsonl` -> `write_trace_jsonl` in import and call: `1 failed, 120 passed in 0.60s`, the failure exactly `test_a_recompile_appends_rather_than_truncating` (`assert 1 == 2`) |
| H red-proof M2 | 1 | same worktree, M1 reverted first with `git diff --stat` empty; `traces=prompt_traces,` deleted: `2 failed, 119 passed in 0.63s`, exactly `test_planning_writes_the_trace_into_the_evidence_dir` and `test_a_recompile_appends_rather_than_truncating`; worktree removed and pruned |
| I state files | 0 | `tests/docs/` `294 passed in 0.25s`; dashboard contract `70 passed in 3.89s` |
| J canary | 0 | `42 passed in 19.22s` |
| K hygiene | 0 | `git status --porcelain` empty and `git worktree list` the primary alone before this commit; insertions 384, 257, 53, 13, 17, 67 — each under 500 |

## Pair proofs (sliced from the COMMITTED authored file, whole-line markers only)
APPEND pairs, FROM 1x before AND after, TO 1x: PAIR_A (TO 53 lines, 52 TO-only;
be125608 is +53/-1 = 52 TO-only plus PAIR_B's one line, strays 0), PAIR_G (TO 75,
66 TO-only; db3bdef3 is +67/-0 = 66 plus the mandated
`from packages.orchestration import mission_compiler` import, strays 0).
REWRITE pairs PAIR_B/C/D/E/F: FROM 0x after, TO 1x each, in the named file.
3d37567f is +12/-7 in `mission_compiler.py` with 0 strays either way, and +1/-0
in `.agent/live_review.md` — that one line is the `Landed: R-0257` line C3
ordered, the second and last addition outside a TO this round. 45765a8f is
+12/-2 in `mission_compiler.py` and +5/-1 in `mission_cmd.py`, strays 0 in both.
PAIR_H: `cmp .agent/plan.md` against the sliced text silent; `wc -l` = 42 < 50.

Open findings: 5 — R-0221, R-0239, R-0247, R-0256, R-0257. R-0257's fix landed in
3d37567f and carries its `Landed:` line; the `Done:` verdict is the reviewer's.
R-0246 landed at R30 and still awaits the same.

Deviations, declared (DECISION D15): this file is 71 lines against the cap of
60. The overage is mandated content only — an 8-row changed-files table, the
7-row item-status table, an 11-row gate table carrying real output, and the
per-pair application proofs; no section was dropped to meet the cap.
Second deviation: gate K's `git status --porcelain`, `git worktree list` and
per-commit insertion counts are recorded above as measured immediately BEFORE
this C6 commit — a commit cannot state its own stat. The post-commit re-run of
gate K is in the handback.

Next: gate R31 over `0ba30611..HEAD`. Then R-0256 (compose once at the
flight-plan and intake sites), then the orchestrator prompt. Pushed; no PR.
