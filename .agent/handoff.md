# Handback — F083 R21 (T003 part 1: the hosted workflow and its thin-wrapper guards)

Branch: feature/f083-ci-self-check. No PR created, none merged. No branch switch.

## Range

Review of 35b80d17..HEAD.

## Commits

### e9c5b2f2 docs(f083): save the R21 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f083-r21.md | +252/-0 | C0a — the block saved verbatim |

### 3134bf3b chore(f083): mirror the R21 step block to last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +180/-204 | C0b — mirrored from the committed authored file |

### 8eed6be8 docs(f083): record the R20 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C1 — RECORD-R20 appended at EOF |

### 3a2e9ce4 ci(f083): add the hosted CI workflow as a thin entrypoint wrapper
| Path | +/- | Reason |
|---|---|---|
| .github/workflows/ci.yml | +52/-0 | C2 — one job, one `remedy ci run`, no stage matrix |

### c9d45ab0 test(f083): pin the hosted workflow as a thin wrapper
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_ci_workflow.py | +56/-0 | C3 — five text guards, no YAML parse |

### 55923c8b docs(f083): advance the plan to the T003 workflow half
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +14/-14 | C4 — PLAN slice, whole-file replace |

### C5 (this commit) docs(f083): write the R21 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C5 — a handoff cannot table the commit that writes it |

## External actions

`git worktree add --detach .remedy-wt/probe-r21 HEAD` rc 0; `git worktree remove
--force` rc 0; `git worktree prune` rc 0. Push: see Next. No `gh` command run.

## Verification — item-status table, every ordered gate measured

| Item | Status | Measured value |
|---|---|---|
| 1 | done | `pwd` = /home/decodeux/Repos/remedy; `git status --porcelain` = "" before C0a and before C5; `git worktree list` = 1 line at start and at handback; `.agent/STOP` absent at both |
| 2 | done | `git rev-parse HEAD` at start = 35b80d17f087be731ac5eedb66e670aa65850e99 |
| 3 | done | authored == last_block byte-equal True; sha256 f0524ec4a2eae48ae8caa1255a5b7f4d1b00fcf6b1b450fc907a4f600faad074; 20628 bytes; 252 lines |
| 4 | done | pre 271015 B, post 275871 B; prefix True; tail (4856 B) byte-equals the extracted RECORD-R20 slice True; `git show --numstat 8eed6be8` = `2 0 .agent/live_review.md` (deletions 0) |
| 5 | done | plan == PLAN slice True; sha256 3e06a8df6d276e06a2960908b5fb096831e97a79959734b8008ddce017c2c2fc; 39 lines (<50); `## Goal` True, `## Next Steps` True; unchecked-box lines 0 |
| 6 | done | `git diff --name-only 35b80d17..HEAD -- packages/ apps/ scripts/` printed nothing (stdout == "", exit 0) |
| 7 | done | read at C3 = c9d45ab0: `Found 26 errors.`; ruff's actual final line `[*] 25 fixable with the \`--fix\` option.`; exit 1 — unchanged |
| 8 | done | `All checks passed!`, exit 0 |
| 9 | done | `5 passed in 0.06s`, exit 0 |
| 10 | done | probe worktree at c9d45ab0 with the npm step moved after the run step: exit 1, `1 failed, 4 passed in 0.06s`; the one failure is `test_hosted_workflow_installs_the_ui_toolchain_before_the_run` (`assert 1824 < 1445`); worktree removed + pruned, `git worktree list` = 1 line |
| 11 | done | `9 passed in 7.78s`, exit 0 |
| 12 | done | `46 passed in 8.08s`, exit 0 |
| 13 | done | `18 passed in 1.14s`, exit 0 |
| 14 | done | `78 passed in 33.46s`, exit 0 |
| 15 | done | registered 112, resolved 9, landed 0, open 103, max R-0484, next free R-0485, no duplicate id, every resolved id registered — unchanged |
| 16 | done | .agent/authored/f083-r21.md, .agent/last_block.md, .agent/live_review.md, .agent/plan.md, .github/workflows/ci.yml, tests/orchestration/test_ci_workflow.py |
| 17 | done | insertions 252, 180, 2, 52, 56, 14 (C0a..C4); none exceeds 500 |
| 18 | done | No `git commit --amend`, no `git rebase` and no `git reset` was run this round; the history is linear. |

## Authored-text proofs

Both slices were extracted programmatically from the COMMITTED
`.agent/authored/f083-r21.md` by their BEGIN/END SLICE markers, never retyped, and
carry no marker line. RECORD-R20 (4856 B) equals the live_review tail byte-for-byte;
PLAN (2174 B) equals `.agent/plan.md` byte-for-byte (sha256 above, item 5).

## Deviations & assumptions

1. The workflow's header comment says "calls the local CI entrypoint exactly
   once" instead of quoting the command: guard 4 asserts `remedy ci run` occurs
   EXACTLY once in the file, so quoting it in prose would redden the guard.
2. Deviations, declared: this handoff is longer than 60 lines. Cause: the
   mandated per-commit changed-files tables for 7 commits plus the 18-row
   item-status table with its measured values. The AGENTS.md >5-commit allowance
   (<=100 lines) applies; no section was dropped.

## Next

(1) Read `.agent/STOP` from disk (self-drive Phase 1 rule 1) before anything else.
(2) Run the Open PR Gate: `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.
(3) Then T003's second half — the CI documentation under `docs/`, its registration
in the `docs/README.md` index, and the runtime-budget table from `## Q9` through
`## Q12` — whose round also records THIS round's verdict, which until then lives
only in the round report.

Fortschritt: 85 % (F083 beansprucht · R1 bis R7 und R9 bis R20 PASS, R8 FAIL auf einem roten ruff-Gate und in R9 repariert · T001 und T002 fertig · T003 zur Hälfte: die gehostete Workflow-Datei ruft denselben `remedy ci run` Entrypoint einmal auf, ohne Stage-Matrix und ohne Marker-Ausdruck im YAML, installiert die UI-Toolchain davor — D6 macht das tragend — und wiederholt nichts; Guards pinnen genau diese Eigenschaften · offen: die CI-Doku mit der Laufzeit-Budget-Tabelle aus den gemessenen Daten, danach Integration Gate und Closure) — Rundenzahl gemessen, Prozentwert geschätzt
