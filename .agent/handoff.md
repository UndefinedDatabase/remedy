# Handback — F083 R22 (T003 part 2: the CI doc, the budget table, one rule promotion)

Branch: feature/f083-ci-self-check. Base 8336140e. Docs- and state-only round.

## Range

Review of 8336140e..HEAD — 8 commits, C0a..C6.

## Commits

### c50f38e8 docs(f083): save the R22 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f083-r22.md | +288/-0 | C0a — the R22 block saved verbatim |

### d589142b docs(f083): mirror the R22 block to last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +211/-175 | C0b — mirror of the COMMITTED C0a file |

### 601d6292 docs(f083): record the R21 verdict and register R-0485
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | C1 — RECORD-R21 appended at EOF, no committed text edited |

### 4f65f713 docs(agents): require commit-sequence departures in the deviations section
| Path | +/- | Reason |
|---|---|---|
| docs/agents/handback_template.md | +6/-0 | C2 — TEMPLATE pair; the R-0485 rule promotion |

### 80526c25 docs(f083): describe Remedy's own CI and its measured budgets
| Path | +/- | Reason |
|---|---|---|
| docs/system/ci-self-check-v1.md | +115/-0 | C3 — the new ist-doc, the only file in the commit |

### 39722f6b docs(index): register the CI self-check note
| Path | +/- | Reason |
|---|---|---|
| docs/README.md | +2/-0 | C4 — QUICKFIND and SYSTABLE pairs, landed after C3 |

### 872ef22d docs(f083): advance the plan past T003
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +15/-17 | C5 — PLAN slice, whole-file replacement |

### C6 docs(f083): write the R22 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | this file | C6 — R-0149 self-reference: a handoff cannot table the commit that writes it |

## External actions

`git push -u origin feature/f083-ci-self-check` after C6 — result in the round
report. No worktree was added, so none had to be removed. No PR created, edited
or merged. No `gh` command run.

## Verification — item status, every ordered item once

| Item | Status | Measured |
|---|---|---|
| 1 | done | `pwd` = /home/decodeux/Repos/remedy first; `git status --porcelain` empty before C0a and before C6; `git worktree list` 1 line at start and at handback; `.agent/STOP` absent at both |
| 2 | done | `git rev-parse HEAD` at round start = 8336140eed9f1f1e234313c1f0c5fbf829609461 |
| 3 | done | authored file and `.agent/last_block.md` byte-equal; sha256 35e46857c733612a9cdeff09625eacacda99ea2b02675f79fcde4407ad918d0e, 24644 bytes, 288 lines |
| 4 | done | pre 275871 B prefixes post 282756 B; tail (6885 B) byte-EQUALS the RECORD-R21 slice extracted from the committed authored file; `git show --numstat` = `4 0`; `--- BEGIN SLICE` count 4 at base and 4 at HEAD |
| 5 | done | TEMPLATE FROM occurred 1x in the target before C2; all 5 TO-ONLY lines occur 1x each among C2's 6 added lines |
| 6 | done | QUICKFIND FROM 1x before C4, its 1 TO-ONLY line 1x among added; SYSTABLE FROM 1x before C4, its 1 TO-ONLY line 1x among added; C4 adds 2 lines total |
| 7 | done | `.agent/plan.md` byte-equals the PLAN slice; sha256 056a6756b92341b96e8bb3a608f11a816f7b3c0f288d941960293539aaa71d4b, 37 lines, `## Goal` and `## Next Steps` present, 0 unchecked-box lines |
| 8 | done | `git diff --name-only 8336140e..HEAD -- packages/ apps/ scripts/ tests/` printed nothing (empty stdout, exit 0) |
| 9 | deviated | `python3 -m ruff check .` → `Found 26 errors.`, exit 1, unchanged. Taken on the tree committed as C6, not on the C6 commit object — see Deviations |
| 10 | done | `python3 -m pytest tests/docs/ -q` → `295 passed in 0.25s`, exit 0, taken at C4 39722f6b |
| 11 | done | 2 relative links in the new doc, both resolve: `../roadmap/features/T2_F083.md`, `test-lanes-v0.md`. None missing |
| 12 | done | `python3 -m pytest tests/orchestration/test_ci_workflow.py -q` → `5 passed in 0.06s`, exit 0 |
| 13 | done | the five CI suites → `46 passed in 8.08s`, exit 0 |
| 14 | done | verification set + canary → `78 passed in 31.56s`, exit 0 |
| 15 | done | budgets read OUT of the document text vs `CI_STAGES.timeout_sec`: fast 900/900, standard 2100/2100, ui 300/300, smoke 300/300, budgets 300/300 — all five agree |
| 16 | done | 113 registered, 9 resolved (`Done:` lines), 0 `Landed:` lines, 104 open; max R-0485, next free R-0486; no id repeats |
| 17 | done | `.agent/authored/f083-r22.md`, `.agent/handoff.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `docs/README.md`, `docs/agents/handback_template.md`, `docs/system/ci-self-check-v1.md` — 8 paths, none outside the block |
| 18 | done | insertions 288, 211, 4, 6, 115, 2, 15; C6's own is bounded by this file's 122 lines and is reported post-commit in the round report (R-0149). None exceeds 500; 8 commits |
| 19 | done | no `git commit --amend`, `git rebase` or `git reset` was run this round |

## Authored-text proofs

RECORD-R21, TEMPLATE, QUICKFIND, SYSTABLE and PLAN were each extracted
PROGRAMMATICALLY from the COMMITTED `.agent/authored/f083-r22.md` by their
`--- BEGIN SLICE X ---` / `--- END SLICE X ---` markers and never retyped.
`.agent/live_review.md`'s appended tail and `.agent/plan.md`'s whole content are
byte-equal to their slices (items 4 and 7). No marker line and no `FROM:`/`TO:`
label reached any target file: after each edit the target's counts of
`--- BEGIN SLICE`, `--- END SLICE`, `\nFROM:\n` and `\nTO:\n` were all 0, and
`.agent/live_review.md`'s marker count is unchanged at 4.

## Deviations & assumptions

1. **Item 9 taken on the C6 TREE, not the C6 commit object.** The block orders the
   ruff reading "at C6", and C6 is the commit that writes this file — the reading
   cannot be inside the text being written before that text exists (R-0149). It was
   therefore measured on the working tree that C6 commits, byte-identical to C6's
   tree. No commit in this round touches a Python file and ruff scans no `.md`, so
   the reading is invariant across C5, the C6 tree and C6. The post-commit re-run
   at C6 is reported in the round report.
2. **No departure from the ordered commit sequence.** C0a, C0b, C1, C2, C3, C4, C5,
   C6 ran in that order, one commit each, none added, none dropped, none reordered
   — stated here explicitly under the rule C2 of this round adds to
   docs/agents/handback_template.md.
3. `.remedy-wt/` held the extracted slices and the pre-image of
   `.agent/live_review.md` as scratch. It is gitignored and not part of the change
   set (the known R-0403 packaging trade-off).
4. **Deviations, declared (DECISION D15):** this file is 122 lines, above the
   60-line cap. Cause: the mandated per-commit changed-files tables for 8 commits
   (8 tables, 32 lines) plus the 19-row item-status table with its measured values
   (21 lines). No section was dropped to meet the cap.

## Next

1. Read `.agent/STOP` from disk (self-drive Phase 1 rule 1) before anything else.
2. Run the Open PR Gate:
   `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.
3. Then the integration-gate round per docs/agents/integration_gate.md — the full
   suite exactly once. That round also RECORDS this round's verdict, which lives
   only in the round report until it does, and resolves R-0485.

Fortschritt: 90 % (F083 beansprucht · R1 bis R7 und R9 bis R21 PASS, R8 FAIL auf einem roten ruff-Gate und in R9 repariert · T001, T002 und T003 fertig: Stage-Tabelle, Stage-Runner, die `remedy ci` CLI-Naht, die gemessenen Stage-Budgets, die gehostete Workflow-Datei als dünner Wrapper mit ihren Guards, und jetzt die Doku samt Laufzeit-Budget-Tabelle · D4 schliesst eine eigene Determinismus-Stage aus, D5 friert die 26 ruff-Fehler ein, D6 macht den lokalen tsc-Compiler tragend · offen sind nur noch das Integration Gate und die Closure · gehostete Laufzeit ist weiterhin NICHT gemessen) — Rundenzahl gemessen, Prozentwert geschätzt
