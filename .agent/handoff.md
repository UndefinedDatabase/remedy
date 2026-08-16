# Handback — F083 R24 (repair: the D6 section undercounted what needs the UI toolchain)

Branch: feature/f083-ci-self-check. Base 24bc77c5. Docs- and state-only round.

## Range

Review of 24bc77c5..HEAD — 6 commits, C0a..C4.

## Commits

### d958bef9 docs(f083): save the R24 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f083-r24.md | +232/-0 | C0a — the R24 block saved verbatim |

### 47f982da chore(agent): mirror the R24 block to last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +102/-133 | C0b — mirror of the COMMITTED C0a file |

### 335fd8de docs(f083): record the R23 verdict and register R-0488
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | C1 — RECORD-R23 appended at EOF, no committed text edited |

### 0da1c149 docs(f083): count both files that need the UI toolchain
| Path | +/- | Reason |
|---|---|---|
| docs/system/ci-self-check-v1.md | +13/-10 | C2 — D6FIX, one REWRITE pair, one paragraph |

### 4d564747 docs(f083): advance the plan past the R-0488 repair
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +14/-15 | C3 — PLAN slice, whole-file replacement |

### C4 docs(f083): write the R24 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | this file | C4 — R-0149 self-reference: a handoff cannot table the commit that writes it |

## External actions

`git push -u origin feature/f083-ci-self-check` after C4 — result in the round report. No worktree added or removed, no PR created/edited/merged, no `gh` run.

## Verification — item status, every ordered item once

| Item | Status | Measured |
|---|---|---|
| 1 | done | `pwd` = /home/decodeux/Repos/remedy first; `git status --porcelain` empty before C0a and before C4; `git worktree list` 1 line at start and at handback; `.agent/STOP` absent at both |
| 2 | done | `git rev-parse HEAD` at round start = 24bc77c56ec16ade6ec410fe8c11154275300f03 |
| 3 | done | authored file and `.agent/last_block.md` byte-equal as COMMITTED blobs; sha256 cb9ab43ea41ae179e6556ff68e34b6be4e0b86beadf7b726760892c928a3ce5a, 21312 bytes, 232 lines |
| 4 | done | pre 293293 B prefixes post 300239 B; tail (6946 B) byte-EQUALS the RECORD-R23 slice extracted from the committed authored file; `git show --numstat` = `6 0`; `--- BEGIN SLICE` count 4 at base and 4 at HEAD |
| 5 | done | counted in `docs/system/ci-self-check-v1.md` ALONE: D6FIX FROM 1x before C2, 0x after; TO 1x after. Marker lines 0; lines equal to `FROM:` or `TO:` 0 |
| 6 | done | `.agent/plan.md` byte-equals the PLAN slice; sha256 e1f4becafde7b177f41df5b7ccb7a488ca7979ccad1bf785bde968427a4a4e6c, 2303 bytes, 39 lines, `## Goal` and `## Next Steps` present, 0 unchecked-box lines |
| 7 | done | `git diff --name-only 24bc77c5..HEAD -- packages/ apps/ scripts/ tests/` printed NOTHING (empty stdout) |
| 8 | done | collected per stage out of `CI_STAGES`, ids matching `test_typescript_compiles` / `test_apps_ui_probe`: fast 0/0 (3975 collected), **standard 1/7** (12600), ui 0/0 (397), smoke 0/0 (23), budgets 0/0 (40), excluded 0/0 (79); every collection exit 0. `tests/runtimes/test_apps_ui_probe.py:35` carries `pytest.mark.skipif(_missing_deps, reason="INTEGRATION BLOCKER: apps/ui dependencies are not installed (apps/ui/node_modules/.bin/vite is missing). Install them once, outside the test run — this test must never run npm install itself.")` |
| 9 | done | `python3 -m pytest tests/docs/ -q` → `295 passed in 0.31s`, exit 0, taken at C2 0da1c149 |
| 10 | done | 2 relative links in the doc, both resolve: `../roadmap/features/T2_F083.md`, `test-lanes-v0.md`. 0 missing |
| 11 | done | `python3 -m ruff check .` → `Found 26 errors.`, exit 1, unchanged. Taken at C3 4d564747 |
| 12 | done | verification set + canary → `78 passed in 31.47s`, exit 0 |
| 13 | done | the three stage/workflow guard files → `25 passed in 7.67s`, exit 0 |
| 14 | done | recomputed at HEAD: 116 registered, 11 `Done:`, 0 `Landed:`, 105 open; max R-0488, next free R-0489; 0 repeated ids, 0 resolutions naming an unregistered id |
| 15 | done | `.agent/authored/f083-r24.md`, `.agent/handoff.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `docs/system/ci-self-check-v1.md` — 6 paths, nothing else |
| 16 | done | insertions 232, 102, 6, 13, 14; C4's own is bounded by this file's line count and is reported post-commit in the round report (R-0149). None exceeds 500. History linear, 6 single-parent commits chained to 24bc77c5 |

## Authored-text proofs

RECORD-R23, D6FIX and PLAN were each extracted PROGRAMMATICALLY from the
COMMITTED `.agent/authored/f083-r24.md` by their BEGIN/END slice markers and
never retyped; the appended tail and `.agent/plan.md` are byte-equal to their
slices (items 4 and 6). No marker line and no `FROM:`/`TO:` label reached any
target file: after C2 the document's marker and bare-label counts are 0, and
`.agent/live_review.md`'s marker count is unchanged at 4.

## Deviations & assumptions

1. **No departure from the ordered commit sequence.** C0a, C0b, C1, C2, C3, C4
   ran in exactly that order, one commit each, none added, none dropped, none
   reordered — stated here explicitly under the rule R22 added to
   docs/agents/handback_template.md.
2. Item 8 was RUN BEFORE C2, not after — committing an unverified correction
   would be backwards, and item 8's STOP clause says a disagreeing reading means
   the document is right. It is invariant here: it reads only `packages/` and
   `tests/`, and item 7 shows neither changed.
3. Item 13 counts 25, not R23's 20: R23 ordered two of these files, this block orders three, and `test_ci_workflow.py` adds 5.
4. `.remedy-wt/` held the slices and the gate script as scratch: gitignored, not
   in the change set (known R-0403 trade-off). No worktree was created.
5. This file is 100 lines, at the template's ≤100 allowance for >5 commits.

## Next

1. Read `.agent/STOP` from disk (self-drive Phase 1 rule 1) before anything else.
2. Run the Open PR Gate:
   `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.
3. Then the integration-gate round per docs/agents/integration_gate.md — the full
   suite exactly once. It also RECORDS this round's verdict, which lives only in
   the round report until it does, and resolves R-0488. R-0482 and R-0487 stay
   open, routed to a paydown branch.

Fortschritt: 92 % (F083 beansprucht · R1 bis R7, R9 bis R21 und R23 PASS, R8 und R22 FAIL — R8 auf einem roten ruff-Gate, R22 auf einer falschen Stage-Zuordnung in der neuen Doku, beide in der Folgerunde repariert · T001, T002 und T003 fertig: Stage-Tabelle, Stage-Runner, die `remedy ci` CLI-Naht, die gemessenen Stage-Budgets, die gehostete Workflow-Datei als dünner Wrapper mit ihren Guards, und die Doku samt Laufzeit-Budget-Tabelle · D4 schliesst eine eigene Determinismus-Stage aus, D5 friert die 26 ruff-Fehler ein, D6 macht den lokalen tsc-Compiler tragend · offen sind im Feature selbst nur noch das Integration Gate und die Closure; R-0482 und R-0487 sind bewusst auf einen eigenen Paydown-Branch geroutet, weil Code- und Testinhalte hier tabu sind · gehostete Laufzeit ist weiterhin NICHT gemessen) — Rundenzahl gemessen, Prozentwert geschätzt
