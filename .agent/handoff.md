# Handback — F021 R8 (record the R7 verdict, rule the two infrastructure DECISIONS)

Branch: feature/f021-live-activity-feed · Round base: `fc56d4cc7b4aeccce460560ce1275192db0e8e10`
Open findings: 212 registered, maximum id R-0649, next free R-0650. No id minted, nothing resolved.
This round built nothing and touched no file under `apps/`, `packages/` or `tests/`.

Fortschritt: ~35 % (T001 fertig und verifiziert · T002 offen · T003 offen; R7
             schrieb das R6-Verdikt, R8 faellt die beiden Infrastruktur-
             ENTSCHEIDUNGEN, T002 wird in R9 gebaut) — Schaetzung

## Range

Review of `fc56d4cc`..HEAD — six commits, C0a through C4.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |

## Commits

### 741923b9 docs(state): save the F021 R8 decide-infra block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r8.md | +259/-0 | the block, copied byte-for-byte |

### b9f8f136 docs(state): mirror the F021 R8 decide-infra block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +161/-125 | written FROM the committed C0a blob |

### fd1e3b4f docs(state): point the F021 plan at the R8 decide-infra round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +16/-12 | slice PLANF021R8, full replacement |

### 9c7fdfc2 docs(decisions): rule F021 D4 and D5, the two infra decisions T002 needs
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +20/-0 | slice DECIDE45, appended |

### 17b9fce7 docs(review): record the R7 verdict and add its evidence to R-0585
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | slice RECORD7, appended |

### C4 docs(state): hand back F021 R8 with the two infrastructure decisions ruled — role: the handback commit, which writes this file and therefore cannot name its own SHA or its own numstat; §3 checklist item 31 orders those readings NOWHERE and the next reviewer takes them at its first gate (finding R-0494)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | measured at the next gate | this handback |

## External actions

- `git worktree add --detach .remedy-wt/f021r8-mut 17b9fce7`, then `git worktree remove --force` and `git worktree prune`; `git worktree list` ends with the primary checkout alone. G5's and G7's destructive halves only.
- `gh pr list --state open --json number,headRefName` → `[]`. No `gh pr create`, no `gh pr merge`.
- `git push -u origin feature/f021-live-activity-feed` after C4; its outcome is in the round report, not here, because this file is written by the commit that precedes it.

## Verification

- G1 EXECUTED: `.agent/STOP` absent immediately before C0a and again immediately before C4; branch `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2 and C3. C4's own reading is ordered nowhere and is not stated here.
- G2 EXECUTED: the authored blob at C0a, `.agent/last_block.md` at C0b, the bytes received, and the reviewer's own emitted copy still on disk at `.remedy-wt/f021-r8.md` are all sha256 `a9d295e3283d08603d50f62407c95f81628545aeecb5adff4be5099135c3b1f4`, 26644 bytes, 259 lines — 1 distinct digest across 4 readings.
- G3 EXECUTED: 3 slices (PLANF021R8, DECIDE45, RECORD7) over 66 CONTENT lines, extracted from the committed C0a blob by their marker LINES; TOTAL 259 against D6's 490 and PROSE 193 against D5's 400, both equal to constraint 8.
- G4 EXECUTED: `cmp .agent/plan.md` against PLANF021R8 exit 0, negative control against RECORD7 exit 1; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 46 against the 50 cap.
- G5 EXECUTED: reader (a) — the round-base blob of `.agent/decisions.md` is a byte-exact prefix of the C2 file, remainder sha256 `f128493ecd04a7d2a9c9172cfa2f27da1826955eb9777c5e88fa80136aa39f2c`, 7147 bytes, 20 lines, file 492990 bytes/6989 lines to 500137/7009. Reader (b) — units 1225 then 1235, DECIDE45's own 10 against constraint 4's TEN, every one of the 1235 positions equal elementwise over the whole list. The byte-offset-2 `D`→`Q` equal-length mutant of the FIRST paragraph is REJECTED by both readers while both ACCEPT the true file.
- G6 EXECUTED, round base then C2: `^## DECISION ` headings 113 then 115, a rise of exactly 2; `^## DECISION F021 D4 ` 0 then 1; `^## DECISION F021 D5 ` 0 then 1; DISTINCT headings 113 of 113 then 115 of 115, so distinct at BOTH points.
- G7 EXECUTED: reader (a) — the round-base blob of `.agent/live_review.md` is a byte-exact prefix of the C3 file, remainder sha256 `d2c9ec8f5ae67ca84d9cf4514e368254af95f379c696baaed7a926b60ab2c323`, 4075 bytes, 2 lines, file 453575 bytes/1086 lines to 457650/1088. Reader (b) — units 224 then 225, RECORD7's own 1 against constraint 4's ONE, all 225 positions equal elementwise. The byte-offset-2 `L`→`Q` equal-length mutant of the FIRST paragraph is REJECTED by both readers while both ACCEPT the true file. Both destructive halves ran in the disposable worktree `.remedy-wt/f021r8-mut`, whose name no directory already used; it was removed and pruned before this handback.
- G8 EXECUTED, round base then C3: `- R-` entries 212 then 212, DISTINCT at both; maximum registered id R-0649 at both; `Done: R-` 0 then 0; `Landed: ` 0 then 0; `Gate: R` keys 7 then 8, DISTINCT at both (R1–R7 then R1–R8); `Gate: R8` 0 then 1; `- R-0585 —` 1 then 1, because this round adds evidence to it and does not re-register it.
- G9 EXECUTED at C3 in the primary checkout, serially: `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py -q -rf` exit 0, 511 passed + 0 skipped = 511, equal to the reviewer's round-base reading. No docs gate owed: the `Change:` list is six `.agent/` paths and zero `docs/` paths — checked against the list, not against the sentence.
- G10 EXECUTED at C3, serially, after G9 finished: `python3 -m pytest tests/cli/test_golden_path.py -q -rf` exit 0, 42 passed + 0 skipped = 42.
- G11 EXECUTED at C3, serially, after G10: `python3 -m pytest tests/ui_contracts/ -q -rf` exit 0, 426 passed and 4 skipped = 430 — identical to the reviewer's round-base reading, so no regression from outside this round.
- G12 EXECUTED: the `fc56d4cc`..C3 range holds 5 paths and 0 of them begin `apps/`, `packages/` or `tests/`; `git ls-files .remedy-wt` reads 0.
- G13 EXECUTED at C3 over `fc56d4cc`..C3, NOT to C4: 5 range paths with both set differences against this block's five non-handoff `Change:` paths EMPTY; all 5 commits single-parent; `git show --numstat` equals `git diff --numstat` cell by cell for C0a, C0b, C1, C2 and C3 and both agree with the tables above; insertions 259, 161, 16, 20, 2, every one under the 500 cap; leading `<<<SLICE ` and `<<<END ` read 0 LINES in `.agent/plan.md`, `.agent/decisions.md` and `.agent/live_review.md`; this round's 5 reflog rows are all `commit:` — amend 0, rebase 0, cherry 0.
- G14 EXECUTED: `gh pr list --state open --json number,headRefName` → `[]`. Neither `gh pr create` nor `gh pr merge` was run this round.
- G15 EXECUTED: this file carries every mandated section of docs/agents/handback_template.md, an item-status row for each of C0a, C0b, C1, C2, C3 and C4, the round base SHA, one line per gate with the transcripts kept in the round report (R-0582), the `Fortschritt:` line verbatim across all three of its lines, and the four `## Next` items constraint 7 requires in its order; its own `wc -l` is declared below.

## Authored-text proofs

`.agent/authored/f021-r8.md` at `741923b9` is byte-identical to the block the reviewer emitted and to `.agent/last_block.md` at `b9f8f136` — one sha256 over all of them (G2), so §4.9's primary cmp-against-scratchpad proof was available and used rather than the digest fallback. All three slices were extracted programmatically from that committed blob by their marker lines; none was retyped, rewrapped, reflowed or reindented, and no marker line landed in a target file (G13). `.agent/plan.md` at C1 compares at exit 0 against PLANF021R8 with RECORD7 as a negative control at exit 1 (G4); `.agent/decisions.md` at C2 and `.agent/live_review.md` at C3 are each the round-base blob plus exactly one newline plus their slice, under two independent readers with a first-paragraph mutant control (G5, G7).

## Deviations & assumptions

- The ordered commit sequence C0a, C0b, C1, C2, C3, C4 was followed exactly: no extra commit, none dropped, none reordered.
- No FROM/TO pair exists this round (constraint 4), so no containment reading is owed and none is stated.
- DECISION D15, stated-cause overage: this file is 97 lines against the 60-line allowance. The cause is mandated content only — six per-commit changed-files tables at 4 lines each, the six-row item-status table, the three verbatim `Fortschritt:` lines, one line for each of the fifteen gates G15 requires, and the four `## Next` items constraint 7 mandates in full. No section was dropped and no transcript was copied in; the transcripts live in the round report.

## Next

1. FIRST action, before anything else: docs/agents/self_drive_protocol.md Phase 1 rule 1 — re-read `.agent/STOP` from disk. Phase 0 is one-shot but G6 binds at any point, so rule 1 comes BEFORE rule 2's Open PR Gate; that ordering is required by the protocol's Phase 2 and by finding R-0347. Never delete the sentinel.
2. The Open PR Gate will find NO open pull request — measured at G14 this round as `[]` — so rule 5 applies and F021 continues on `feature/f021-live-activity-feed`. The branch is mid-feature by design; nothing is owed a merge and nothing is owed a PR.
3. The next build is T002 — the feed, its rows and the NowCard over fixture streams, with the scroll discipline that never yanks a reader who has scrolled up. DECISIONS F021 D4 and D5, ruled at C2 of THIS round, are the ground it is built on: D4 keeps the node vitest and gates the components with a Python source contract under `tests/ui_contracts/`, D5 puts a bounded 500-row event ring inside the existing brain-stream runner and publishes it on the existing view. T002 therefore needs no further infrastructure ruling.
4. The C4 handback commit of this round has never had its own `git status --porcelain` reading or its own insertion count recorded, because §3 checklist item 31 orders them nowhere. The next reviewer takes both at its first gate and records them in that round's entry.
