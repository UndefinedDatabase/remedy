# Handback — F021 R7 (record the R6 verdict, register R-0649, close the session)

Branch: feature/f021-live-activity-feed · Round base: `6f5078d77c3fb3e2e60a0aa32c8e0e49d9aef391`
Open findings: 212 registered, maximum id R-0649, next free R-0650. One id minted, nothing resolved.

Fortschritt: ~30 % (T001 fertig und verifiziert · T002 offen · T003 offen; R6
             lieferte Modul, Katalog und den Contract-Test, R7 schreibt das
             Verdikt und schließt die Session — T002 beginnt in R8) — Schätzung

## Range

Review of `6f5078d7`..HEAD — five commits, C0a through C3.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |

## Commits

### 487ac619 docs(state): save the F021 R7 record-and-close block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r7.md | +223/-0 | the block, copied byte-for-byte |

### 9bb77da3 docs(state): mirror the F021 R7 record-and-close block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +157/-291 | written FROM the committed C0a blob |

### 0882ba7b docs(state): point the F021 plan at the R7 record-and-close round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +13/-15 | slice PLANF021R7, full replacement |

### 30a09f4b docs(review): record the R6 verdict and register R-0649
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | slice RECORD6, appended |

### C3 docs(state): hand back F021 R7 and close the reviewer session — role: the handback commit, which writes this file and therefore cannot name its own SHA or its own numstat; §3 checklist item 31 orders those readings NOWHERE and the next reviewer takes them at its first gate (finding R-0494)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | measured at the next gate | this handback |

## External actions

- `git worktree add --detach .remedy-wt/f021r7g5neg 30a09f4b`, then `git worktree remove --force` and `git worktree prune`; `git worktree list` ends with the primary checkout alone. G5's destructive half only.
- `gh pr list --state open --json number,headRefName` → `[]`. No `gh pr create`, no `gh pr merge`.
- `git push -u origin feature/f021-live-activity-feed` after C3.

## Verification

- G1 EXECUTED: `.agent/STOP` absent before C0a and before C3; branch `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after each of C0a, C0b, C1 and C2. C3's own reading is ordered nowhere and is not stated here.
- G2 EXECUTED: the authored blob at C0a, `.agent/last_block.md` at C0b, the bytes received and the reviewer's own `.remedy-wt/f021-r7.md` are all sha256 `5d0eebbe12a16d57a1a3696944ef8f24f696e99ac1e2c69d990dde632b86957e`, 21611 bytes, 223 lines — 1 distinct digest across 5 readings.
- G3 EXECUTED: 2 slices over 47 CONTENT lines extracted from the committed C0a blob by marker line; TOTAL 223 against D6's 490 and PROSE 176 against D5's 400, both equal to constraint 8.
- G4 EXECUTED: `cmp .agent/plan.md` against PLANF021R7 exit 0, negative control against RECORD6 exit 1; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 42 against the 50 cap.
- G5 EXECUTED: reader (a) — the round-base blob is a byte-exact prefix, remainder sha256 `2c4560714396bfc4c24d2ac451ca80f85324048fc9afdd98f48a706fc77a11ef`, 7529 bytes, 6 lines, file 446046 bytes/1080 lines to 453575/1086. Reader (b) — units 221 then 224, RECORD6's own 3 against constraint 4's THREE, every one of the 224 positions equal elementwise. The byte-offset-2 `L`→`Z` mutant of the FIRST paragraph is REJECTED by both readers and the true file ACCEPTED by both.
- G6 EXECUTED, round base then C2: `- R-` 211 then 212, DISTINCT at both; `Done: R-` 0/0; `Landed: ` 0/0; `Gate: R` keys 6 then 7, all DISTINCT; `Gate: R7` 0 then 1; maximum id R-0648 then R-0649; `- R-0649 —` 0 then 1; `- R-0449 —` 1/1; `- R-0585 —` 1/1.
- G7 EXECUTED at C2 in the primary checkout: `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py -q -rf` exit 0, 511 passed + 0 skipped = 511, equal to the reviewer's round-base reading. No docs gate owed: the Change list is five `.agent/` paths and zero `docs/` paths.
- G8 EXECUTED at C2, serially, after G7 finished: `python3 -m pytest tests/cli/test_golden_path.py -q -rf` exit 0, 42 passed + 0 skipped = 42.
- G9 EXECUTED at C2, serially, after G8: `python3 -m pytest tests/ui_contracts/ -q -rf` exit 0, 426 passed and 4 skipped — identical to the reviewer's round-base reading, so no regression from outside this round.
- G10 EXECUTED: the `6f5078d7`..C2 range holds 4 paths and 0 of them begin `apps/`, `packages/` or `tests/`; `git ls-files .remedy-wt` reads 0.
- G11 EXECUTED at C2 over `6f5078d7`..C2, not to C3: 4 range paths with both set differences against the four non-handoff Change paths EMPTY; all 4 commits single-parent; `git show --numstat` equals `git diff --numstat` cell by cell for C0a, C0b, C1 and C2 and both agree with the tables above; insertions 223, 157, 13, 6, every one under the 500 cap; leading `<<<SLICE ` and `<<<END ` read 0 lines in `.agent/plan.md` and in `.agent/live_review.md`; this round's 4 reflog rows are all `commit:` — amend 0, rebase 0, cherry 0.
- G12 EXECUTED: `gh pr list --state open --json number,headRefName` → `[]`. Neither `gh pr create` nor `gh pr merge` was run this round.
- G13 EXECUTED: this file carries every mandated section, an item-status row for each of C0a, C0b, C1, C2 and C3, the round base SHA, one line per gate with the transcripts kept in the round report, the `Fortschritt:` line verbatim across all three of its lines, and the four `## Next` items constraint 7 requires in its order.

## Authored-text proofs

`.agent/authored/f021-r7.md` at `487ac619` is byte-identical to the block the reviewer emitted and to `.agent/last_block.md` at `9bb77da3` — one sha256 over all of them (G2). Both slices were extracted programmatically from that committed blob by their marker lines; neither was retyped, rewrapped or reindented, and no marker line landed in a target file (G11). `.agent/plan.md` at C1 compares at exit 0 against PLANF021R7 with RECORD6 as a negative control at exit 1 (G4); `.agent/live_review.md` at C2 is the round-base blob plus one newline plus RECORD6 under two independent readers with a first-paragraph mutant control (G5).

## Deviations & assumptions

- The ordered commit sequence C0a, C0b, C1, C2, C3 was followed exactly: no extra commit, none dropped, none reordered.
- Constraint 7(c) and the PLANF021R7 slice DISAGREE on round numbering, and both are in this block. Constraint 7(c) calls T002 "R8's work" and says "R7 must FIRST rule the two infrastructure DECISIONS"; PLANF021R7, committed at C1 this round, assigns those DECISIONS to R8 and T002 to R9. R7 is THIS round, it built nothing and it ruled neither DECISION. `## Next` item (c) therefore carries the substance — T002 is the next build and both DECISIONS are ruled before it — without the round attribution, because writing "R7 must first rule them" into a handback written BY R7 after R7 ruled nothing would put a false sentence on disk. NOT reconciled; the next reviewer owns the numbering. This is the R-0585 clause-versus-clause shape, in the same block that records an R-0585 instance.
- DECISION D15, stated-cause overage: this file is 88 lines against the 60-line allowance a five-commit round has. The cause is mandated content only — five per-commit changed-files tables at 4 lines each, the five-row item-status table, the three verbatim `Fortschritt:` lines, one line for each of the thirteen gates G13 requires, and the four `## Next` items constraint 7 mandates in full. No section was dropped and no transcript was copied in; the transcripts live in the round report.

## Next

1. FIRST action, before anything else: docs/agents/self_drive_protocol.md Phase 1 rule 1 — re-read `.agent/STOP` from disk. Phase 0 is one-shot but G6 binds at any point, so rule 1 comes BEFORE rule 2's Open PR Gate; that ordering is required by the protocol's Phase 2 and by finding R-0347. Never delete the sentinel.
2. The Open PR Gate will find NO open pull request — measured at G12 this round as `[]` — so rule 5 applies and F021 continues on `feature/f021-live-activity-feed`. The branch is mid-feature by design; nothing is owed a merge and nothing is owed a PR.
3. The next build is T002 — the feed, its rows and the NowCard over fixture streams, with the scroll discipline that never yanks a reader who has scrolled up. It cannot be written until the two infrastructure DECISIONS it depends on are RULED FIRST: the frontend test environment, which collects no component test at all today (`apps/ui/vitest.config.ts` sets `environment: "node"` with `include: ["src/**/*.test.ts"]`, measured at `6f5078d7`), and the single-subscription fan-out.
4. The R6 handback commit `6f5078d7` has never had its own `git status --porcelain` reading or its own insertion count recorded, because §3 checklist item 31 orders them nowhere. The next reviewer takes both at its first gate and records them in that round's entry. The same is true of this round's C3, for the same reason.
