# Handback — F083 R23 (repair: the CI note named the wrong stage for the TypeScript check)

Branch: feature/f083-ci-self-check. Base 07d6577a. Docs- and state-only round.

## Range

Review of 07d6577a..HEAD — 6 commits, C0a..C4.

## Commits

### 3f3e28ed docs(f083): save the R23 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f083-r23.md | +263/-0 | C0a — the R23 block saved verbatim |

### 0f3eece5 chore(agent): mirror the R23 block to last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +182/-207 | C0b — mirror of the COMMITTED C0a file |

### 8fbcbc6f docs(f083): record the R22 verdict and register R-0486 and R-0487
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +8/-0 | C1 — RECORD-R22 appended at EOF, no committed text edited |

### f35cb48e docs(f083): put the TypeScript compile check in the stage that selects it
| Path | +/- | Reason |
|---|---|---|
| docs/system/ci-self-check-v1.md | +12/-7 | C2 — UIROW, STDROW and D6SEC, one correction, one commit |

### ff3d713e docs(f083): advance the plan to the integration gate
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +14/-11 | C3 — PLAN slice, whole-file replacement |

### C4 docs(f083): write the R23 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | this file | C4 — R-0149 self-reference: a handoff cannot table the commit that writes it |

## External actions

`git push -u origin feature/f083-ci-self-check` after C4 — result in the round
report. No worktree was added, so none had to be removed. No PR created, edited
or merged. No `gh` command run.

## Verification — item status, every ordered item once

| Item | Status | Measured |
|---|---|---|
| 1 | done | `pwd` = /home/decodeux/Repos/remedy first; `git status --porcelain` empty before C0a and before C4; `git worktree list` 1 line at start and at handback; `.agent/STOP` absent at both |
| 2 | done | `git rev-parse HEAD` at round start = 07d6577ab346722ad0687886ff077a918db2610e |
| 3 | done | authored file and `.agent/last_block.md` byte-equal as COMMITTED blobs; sha256 c194ee19da65f7d34fbb8b61bd8c69dea0a82254f954de36d5edf8cda1df04d7, 27100 bytes, 263 lines |
| 4 | done | pre 282756 B prefixes post 293293 B; tail (10537 B) byte-EQUALS the RECORD-R22 slice extracted from the committed authored file; `git show --numstat` = `8 0`; `--- BEGIN SLICE` count 4 at base and 4 at HEAD |
| 5 | done | after C2, counted in `docs/system/ci-self-check-v1.md` ALONE: UIROW FROM 0x / TO 1x; STDROW FROM 0x / TO 1x; D6SEC FROM 0x / TO 1x. Each FROM occurred exactly 1x before its replacement |
| 6 | done | `.agent/plan.md` byte-equals the PLAN slice; sha256 b846a529a780417c8c6b8dc4dccc266671cf522be00a27bfa05e77e09f117417, 2401 bytes, 40 lines, `## Goal` and `## Next Steps` present, 0 unchecked-box lines |
| 7 | done | `git diff --name-only 07d6577a..HEAD -- packages/ apps/ scripts/ tests/` printed NOTHING (empty stdout) |
| 8 | done | collected per stage out of `CI_STAGES`, ids containing `test_typescript_compiles`: fast 0 (3975 collected), **standard 1** (12600), ui 0 (397), smoke 0 (23), budgets 0 (40), excluded 0 (79); every collection exit 0. The one hit is `tests/ui_server/test_dashboard_contract.py::TestJobSummaryCommandContract::test_typescript_compiles`. The `ui` selection yields 7 distinct files, all under `tests/ui_contracts/`, and **0** of them contain `node_modules`, `npx`, `tsc` or `npm ` |
| 9 | done | `python3 -m pytest tests/docs/ -q` → `295 passed in 0.31s`, exit 0, taken at C2 f35cb48e |
| 10 | done | 2 relative links in the doc, both resolve: `../roadmap/features/T2_F083.md`, `test-lanes-v0.md`. 0 missing |
| 11 | done | `python3 -m ruff check .` → `Found 26 errors.`, exit 1, unchanged. Taken at C3 ff3d713e |
| 12 | done | verification set + canary → `78 passed in 31.51s`, exit 0 |
| 13 | done | `tests/orchestration/test_ci_stages.py` + `test_ci_stage_selection.py` → `20 passed in 7.60s`, exit 0 |
| 14 | done | recomputed at HEAD: 115 registered, 10 `Done:`, 0 `Landed:`, 105 open; max R-0487, next free R-0488; 0 repeated ids, 0 resolutions naming an unregistered id |
| 15 | done | `.agent/authored/f083-r23.md`, `.agent/handoff.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `docs/system/ci-self-check-v1.md` — 6 paths, nothing else |
| 16 | done | insertions 263, 182, 8, 12, 14; C4's own is bounded by this file's line count and is reported post-commit in the round report (R-0149). None exceeds 500. History linear, 6 single-parent commits chained to 07d6577a |

## Authored-text proofs

RECORD-R22, UIROW, STDROW, D6SEC and PLAN were each extracted PROGRAMMATICALLY
from the COMMITTED `.agent/authored/f083-r23.md` by their
`--- BEGIN SLICE X ---` / `--- END SLICE X ---` markers and never retyped.
`.agent/live_review.md`'s appended tail and `.agent/plan.md`'s whole content are
byte-equal to their slices (items 4 and 6). No marker line and no `FROM:`/`TO:`
label reached any target file: after C2 the document's counts of `BEGIN SLICE`,
`END SLICE` and of lines equal to `FROM:` or `TO:` are all 0, and
`.agent/live_review.md`'s marker count is unchanged at 4.

## Deviations & assumptions

1. **No departure from the ordered commit sequence.** C0a, C0b, C1, C2, C3, C4 ran
   in exactly that order, one commit each, none added, none dropped, none
   reordered — stated here explicitly under the rule R22 added to
   docs/agents/handback_template.md.
2. `.remedy-wt/` held the extracted slices and the gate scripts as scratch. It is
   gitignored and not part of the change set (the known R-0403 packaging
   trade-off). No git worktree was created this round, so none had to be pruned.
3. This file is 100 lines, inside the template's ≤100 allowance for >5 commits.

## Next

1. Read `.agent/STOP` from disk (self-drive Phase 1 rule 1) before anything else.
2. Run the Open PR Gate:
   `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.
3. Then the integration-gate round per docs/agents/integration_gate.md — the full
   suite exactly once. That round also RECORDS this round's verdict, which lives
   only in the round report until it does, and resolves R-0486. R-0487 stays open
   and is routed to a paydown branch with R-0482.

Fortschritt: 90 % (F083 beansprucht · R1 bis R7, R9 bis R21 PASS, R8 und R22 FAIL — R8 auf einem roten ruff-Gate, R22 auf einer falschen Stage-Zuordnung in der neuen Doku, beide in der Folgerunde repariert · T001, T002 und T003 fertig: Stage-Tabelle, Stage-Runner, die `remedy ci` CLI-Naht, die gemessenen Stage-Budgets, die gehostete Workflow-Datei als dünner Wrapper mit ihren Guards, und die Doku samt Laufzeit-Budget-Tabelle · D4 schliesst eine eigene Determinismus-Stage aus, D5 friert die 26 ruff-Fehler ein, D6 macht den lokalen tsc-Compiler tragend · offen sind im Feature selbst nur noch das Integration Gate und die Closure; R-0487 (docs/README.md wird nie auf tote Links geprüft) ist neu registriert und bewusst auf einen eigenen Paydown-Branch geroutet, weil Testinhalte hier tabu sind · gehostete Laufzeit ist weiterhin NICHT gemessen) — Rundenzahl gemessen, Prozentwert geschätzt
