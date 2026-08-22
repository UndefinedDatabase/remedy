# Handback — F021 R5 (the correction round)

Feature F021 Live activity feed + now-card · Round R5 · branch `feature/f021-live-activity-feed` · round base `91d14c88a0b2a083fa83bde57df1d6d248e2de52`.
No pull request exists and none was created — F021 is mid-feature. This round built nothing and touched no file under `apps/`, `packages/` or `tests/`.

Fortschritt: ~12 % (T001 offen · T002 offen · T003 offen; R1 beansprucht, R2
             vermessen, R3 und R5 entschieden, R4 verdiktiert — R5 korrigiert
             den Boden, gebaut wird ab R6) — Schätzung

## Range

Review of `91d14c88`..HEAD — six commits, C0a C0b C1 C2 C3 C4, in that order.

## Items

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this handback; a commit cannot table its own SHA or numstat |

## Commits

### d5f9d141 docs(state): save the F021 R5 correction block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r5.md | +238/-0 | the R5 block saved byte-for-byte |

### 464bab56 docs(state): mirror the F021 R5 correction block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +166/-120 | mirrored FROM the committed C0a blob |

### f8705c3e docs(state): point the F021 plan at the R5 correction round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +17/-17 | PLANF021R5, whole-file replacement |

### c8cfd46d docs(review): record the R4 verdict and widen the R-0419 evidence
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | RECORD4 appended |

### 03421366 docs(state): rule DECISION F021 D3 on the re-measured emitter set
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +10/-0 | DECIDE3 appended |

### C4 (SHA unknowable to itself) docs(state): hand back F021 R5
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | in the round report | the commit that writes this file cannot name its own SHA, numstat or `git status` reading; the worker's round report carries all three, which is where G1 and G12 route them (R-0494, R-0149) |

## External actions

- `git worktree add --detach .remedy-wt/g6-wt 03421366`, then `git worktree remove --force .remedy-wt/g6-wt` and `git worktree prune` — the G6 negative controls; `git worktree list` then shows the primary checkout alone.
- `gh pr list --state open --json number,headRefName` → `[]`. Neither `gh pr create` nor `gh pr merge` was run.
- `git push -u origin feature/f021-live-activity-feed` after C4 — outcome in the round report, since the push follows the commit that writes this file.

## Verification

One line per gate; the raw transcripts are in the round report, not here (R-0582).

- G1 `.agent/STOP` ABSENT before C0a and again before C4; branch `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3 — C4's own reading is in the round report.
- G2 TRANSPORT sha256 `8a489735b3da1261ad4ada770591a063bca6fcd03c635d77c8c1e15e9312950b`, 23112 bytes, 238 lines, equal over the received bytes, `.remedy-wt/f021-r5.md`, `.agent/authored/f021-r5.md` at C0a and `.agent/last_block.md` at C0b, which was written FROM the committed C0a blob.
- G3 SLICES the marker extractor over the committed C0a blob prints 3 slices and 52 CONTENT lines; TOTAL 238 against DECISION F085 D6's 490 and PROSE 186 against D5's 400.
- G4 PLAN `cmp .agent/plan.md` against PLANF021R5 exit 0 and the NEGATIVE CONTROL against DECIDE3 exit 1; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 42 under the 50 cap.
- G5 EMITTER re-derived by the worker over `packages/`, `apps/`, `scripts/`: 82 call sites, 60 distinct literals, 11 non-constant event args, 15 inside the four sets; RED CONTROL over `packages/` alone 35, 23, 10, 1; static vocabulary 83 and the literals-vs-trace-sets intersection 0. Every value DECIDE3 states reproduced.
- G6 APPENDS both readers ACCEPT both true files — live_review remainder sha256 `c727dc5b…f459` 4730 bytes 2 lines, 435610/1076 → 440340/1078, units 219 + 1 = 220 with 0 elementwise mismatches; decisions remainder sha256 `5eb1fee3…dca0` 3644 bytes 10 lines, 489346/6979 → 492990/6989, units 1220 + 5 = 1225 with 0 mismatches — and both readers REJECT both first-paragraph mutants (byte offset 2, `L`→`l` and `D`→`d`), written to disk only inside the disposable worktree.
- G7 LEDGER base → C2, line-anchored: `- R-` 211 all distinct → 211 all distinct; `Done: R-` 0 → 0; `Landed: ` 0 → 0; `Gate: R` keys 4 all distinct → 5 all distinct; `Gate: R5` 0 → 1; maximum registered id R-0648 → R-0648; `- R-0419 —` 1 → 1.
- G8 DECISIONS base → C3, line-anchored: `^## DECISION ` 112 → 113 and `^## DECISION F021 D3 ` 0 → 1.
- G9 SUITES `tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py` exit 0, 511 passed + 0 skipped = 511, run serially in the primary checkout; no docs gate is owed because the `Change:` list holds no `docs/roadmap/**` path.
- G10 CANARY `tests/cli/test_golden_path.py` exit 0, 42 passed + 0 skipped = 42, run serially after G9 had finished.
- G11 the range holds 0 paths beginning `apps/`, `packages/` or `tests/`, and `git ls-files .remedy-wt` reads 0.
- G12 the range lists exactly the block's six paths with both set differences EMPTY; every commit single-parent; the numstat readings agree cell by cell with the `## Commits` table above; insertions 238, 166, 17, 2 and 10 for C0a…C3, all under the 500 cap, with C4's own count in the round report; `<<<SLICE ` and `<<<END ` read 0 lines in all three files a slice lands in; and this round's reflog rows are all `commit:` with `amend`, `rebase` and `cherry` each 0.
- G13 NO PULL REQUEST `gh pr list --state open --json number,headRefName` prints the empty list `[]`; neither `gh pr create` nor `gh pr merge` was run.
- G14 this file carries every mandated section of docs/agents/handback_template.md, the item-status table, the round base SHA, one line per gate, the block's three `Fortschritt:` lines verbatim and a `## Next`; its own `wc -l` is in the round report with the DECISION D15 line below.

## Authored-text proofs

`.agent/authored/f021-r5.md` at C0a is byte-equal to the reviewer's emitted copy at `.remedy-wt/f021-r5.md` and to the bytes received, all at sha256 `8a489735b3da1261ad4ada770591a063bca6fcd03c635d77c8c1e15e9312950b`.
All three slices were extracted programmatically from the COMMITTED C0a blob by their marker lines and applied without retyping; `.agent/plan.md` is proved byte-equal to PLANF021R5 by `cmp` at exit 0 (G4).

## Deviations & assumptions

- DECLARED DEVIATION, an extra measurement only: G9 and G10 were ALSO run once before C4, on the C3 tree, so the gate lines above could state a MEASURED total rather than a predicted one — a handback committed at C4 cannot otherwise carry a number produced after C4. The ordered post-C4 runs were then executed as the block requires and both readings appear in the round report. No commit was added, dropped or reordered: the sequence is exactly C0a, C0b, C1, C2, C3, C4.
- DECISION D15, stated-cause overage: this file's own `wc -l` is in the round report and exceeds the 60-line cap. The cause is mandated content — six per-commit changed-files tables (the >5-commit case AGENTS.md and the handback template allow at ≤100 lines), the item-status table, and G14's one-line-per-gate requirement over fourteen gates. No section was dropped and no transcript was pasted here.
- This round minted no finding id and resolved nothing: no `- R-` entry, no `Done:` line, no `Landed:` line. R-0648 stays the maximum registered id and R-0649 is the next free one.

## Next

R6 builds T001 headless-first on the ground this round corrected: `apps/ui/src/api/humanize.ts` with the catalog and its honest generic line, the vitest generic-path test, and the `tests/ui_contracts/` derivation test DECISION F021 D3 rules.
Before authoring it, re-read `.agent/STOP` from disk (Phase 1 rule 1) and only then run the Open PR Gate (rule 2).
