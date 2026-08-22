# Handback — F021 R9 (the frame-to-row projection, T002's first production code)

Round base: `f5f0158526342247abf4f8215b7dbdfbd007789c` — the R8 handback commit.

Fortschritt, verbatim from the block, across all three of its lines:

```
Fortschritt: ~40 % (T001 fertig · T002 begonnen — die Projektion Frame→Zeile
             landet in dieser Runde, der Ring und die Komponenten folgen in R10
             und R11; T003 offen) — Schaetzung
```

## Range

Review of `f5f0158526342247abf4f8215b7dbdfbd007789c`..HEAD (C4).

## Commits

### 02749b50 docs(state): save the F021 R9 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f021-r9.md | +389/-0 | C0a — the step block saved verbatim |

### 66a18dca docs(state): mirror the F021 R9 step block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +273/-143 | C0b — written from the committed C0a blob |

### 347a68db docs(state): point the F021 plan at the R9 feed-row round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +21/-19 | C1 — PLANF021R9, whole-file replacement |

### 40965b8d feat(ui): project a brain-stream frame into an activity-feed row
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/feedRow.ts | +52/-0 | C2 — FEEDROW, new file, uncalled by design |
| apps/ui/src/api/feedRow.test.ts | +67/-0 | C2 — FEEDROWTEST, new file, eight `it(` blocks |

### 4df4a3bd docs(review): record the R8 verdict as PASS on every gate
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C3 — RECORD8 appended, no id minted |

### C4 (role: this handback — a handoff cannot table the commit that writes it, so its own short SHA does not exist when these bytes are authored; R-0149 pattern, and §3 checklist item 31 leaves its numstat and porcelain reading to the next reviewer's first gate)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C4 — the G16 handback, this file |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |

## External actions

- `git worktree add --detach .remedy-wt/r9base f5f01585` exit 0 — G9 base reading, `apps/ui/node_modules` SYMLINKED (never copied); symlink unlinked, worktree removed, `git worktree prune` exit 0.
- `git worktree add --detach .remedy-wt/r9red 40965b8d` exit 0 — G10 red control, same symlink discipline; symlink unlinked, worktree removed and pruned. `git worktree list` now ends with the primary checkout alone.
- `gh pr list --state open --json number,headRefName` exit 0, output `[]`. Neither `gh pr create` nor `gh pr merge` was run this round.
- `git push -u origin feature/f021-live-activity-feed` — run immediately AFTER C4; its outcome is reported in the round report, since a commit cannot record the push that follows it.

## Verification

One line per gate; the raw transcripts stay in the round report (R-0582).

- G1 PASS — `.agent/STOP` absent before C0a and again before C4; branch `feature/f021-live-activity-feed`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3.
- G2 PASS — C0a blob, C0b blob, both working copies and the reviewer's emitted `.remedy-wt/f021-r9.md` are all sha256 `bcff6f7bf4e1ab3802ae77933dc7fb920ec0716baa0b2b6ec6cc2437a32caa91` over 26224 bytes and 389 lines. C0b was written from the C0a blob.
- G3 PASS — extractor over the committed C0a blob printed 4 slices and 168 CONTENT lines; TOTAL 389 against the 490 cap, PROSE 221 against the 400 cap, both equal to constraint 9.
- G4 PASS — `cmp` committed `.agent/plan.md` vs PLANF021R9 exit 0; negative control vs RECORD8 exit 1; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 48 against the 50 cap.
- G5 PASS — `git ls-tree` at the round base printed 0 lines, so both files were ABSENT; `cmp` exit 0 for each file against its own slice and exit 1 for each against the other; 52 and 67 lines.
- G6 PASS — reader (a): base blob is a byte-exact prefix, remainder sha256 `1f79c8b91ddd720d0d7cad8e22296cf14521be10e4a632921b7e6d5aa018d8b6` over 4011 bytes and 2 lines, file 457650 bytes/1088 lines to 461661/1090. Reader (b): 225 units to 226, elementwise over the whole list, RECORD8's own units 1 as constraint 4 states. NEGATIVE CONTROL byte offset 2 of the first paragraph, `L` to `Q`, equal length: REJECTED by both readers, true file ACCEPTED by both. See the assumption below for the newline convention reader (b) needs.
- G7 PASS — round base to C3: `- R-` 212 to 212, all DISTINCT at both; maximum registered id R-0649 at both; `Done: R-` 0 to 0; `Landed: ` 0 to 0; `Gate: R` keys 8 to 9, all DISTINCT at both; `Gate: R9` 0 to 1. Every reading equals the one the block ordered.
- G8 PASS — `npx tsc --noEmit` from `apps/ui` in the primary checkout at C2: exit 0, no output.
- G9 PASS — `npx vitest run` from `apps/ui`, primary checkout at C2: exit 0, 12 files, 168 tests. ROUND BASE, taken in the disposable worktree with node_modules symlinked: exit 0, 11 files, 160 tests. Rise: files +1, tests +8, exactly as ordered.
- G10 PASS — `    seq: frame.seq,` occurs exactly ONCE in `feedRow.ts`, whole-line 1 and indent-agnostic 1 agreeing, at line 45. Mutated to `    seq: 0,` in the disposable worktree: `npx vitest run` exit 1, RED, failing `carries the frame's own seq rather than any envelope field` (and also `an uncatalogued kind still yields a row, on the generic line`), 2 failed of 168. Restored byte-equal: exit 0, 168 passed. The primary checkout was never mutated.
- G11 PASS — `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py -q -rf` exit 0, 511 passed plus skipped, equal to the round-base reading. No docs gate is owed: the `Change:` list's seven paths are all under `.agent/` or `apps/ui/`, checked against the list.
- G12 PASS — `python3 -m pytest tests/cli/test_golden_path.py -q -rf` exit 0, 42, equal to the round-base reading.
- G13 PASS — `python3 -m pytest tests/ui_contracts/ -q -rf` exit 0, 426 passed and 4 skipped = 430, UNCHANGED from the round base, so the humanize-catalog equality still holds.
- G14 PASS — base-to-C3 path set is exactly the six non-handoff `Change:` paths, both set differences EMPTY; all 5 commits single-parent; `git show --numstat` and `git diff --numstat` agree cell by cell and match the tables above; insertions 389, 273, 21, 119, 2, every one under 500; leading `<<<SLICE ` and `<<<END ` 0 lines in `.agent/plan.md`, `.agent/live_review.md` and both new files; the only paths under `apps/`, `packages/` or `tests/` are the two new files, status `A`, nothing modified or deleted; `git ls-files .remedy-wt` 0 lines; all 5 reflog rows read `commit:`, so amend 0, rebase 0, cherry 0.
- G15 PASS — `gh pr list --state open --json number,headRefName` exit 0, `[]` — an EMPTY list, which is the fact constraint 7(b) hands the next session.
- G16 PASS — every mandated section of the handback template is present, an item-status row exists for C0a, C0b, C1, C2, C3 and C4, the round base SHA is named, one line per gate with transcripts kept out, the `Fortschritt:` line is verbatim across all three of its lines, and `## Next` carries constraint 7's four items in order. `wc -l` 109.

## Authored-text proofs

- PLANF021R9 → `.agent/plan.md` at C1: `cmp` exit 0, negative control exit 1 (G4).
- FEEDROW → `apps/ui/src/api/feedRow.ts` and FEEDROWTEST → `apps/ui/src/api/feedRow.test.ts` at C2: `cmp` exit 0 each, cross negative controls exit 1 each (G5).
- RECORD8 → `.agent/live_review.md` at C3: two independent readers accept, both reject the mutant (G6).
- All four slices were extracted programmatically from the COMMITTED C0a blob by their `<<<SLICE `/`<<<END ` marker lines; no marker line reached any target file (G14).

## Deviations & assumptions

- No departure from the ordered commit sequence: C0a, C0b, C1, C2, C3, C4, exactly six commits, in that order, no extra and none dropped.
- ASSUMPTION, stated because G6 reader (b) cannot be written without it: each blob here ends in exactly ONE terminator newline, which terminates its last line and does NOT open a unit, so units are taken after stripping that single terminator. Split naively without that normalisation, the base blob's final unit carries a trailing newline the C3 file's corresponding unit does not, and reader (b) rejects the true file at that one boundary element while the unit COUNTS still read 225, 226 and 1. Both forms are reported; the normalised form is the one that accepts.
- NOTE, not a defect: `git commit`'s own summary for C0b printed 389 insertions and 259 deletions under rewrite detection, while `git show --numstat` and `git diff --numstat` both read 273 and 143. The table above carries the numstat readings, which are the ones G14 compares.
- DECISION D15 overage: this file is 109 lines against the 100-line cap that a >5-commit handback may use. The mandated content that causes it is the per-commit table set for six commits together with G16's ONE LINE PER GATE over sixteen gates, of which G6, G10 and G14 each carry multi-part readings that cannot be split across lines without breaking the one-line-per-gate rule. No section was dropped and no transcript was pasted.
- This round minted NO finding id and resolved none: R-0649 remains the maximum registered id and R-0650 the next free one. No `Done:` or `Landed:` line was written.

## Next

1. The next session's FIRST action is docs/agents/self_drive_protocol.md Phase 1 rule 1 — the `.agent/STOP` check — BEFORE rule 2's Open PR Gate. That protocol's Phase 2 and finding R-0347 both require this order: Phase 0 runs once, but G6 binds at any point.
2. The Open PR Gate will find NO open pull request (G15 read `[]`), so Phase 1 rule 5 applies and F021 continues on `feature/f021-live-activity-feed`. The branch stays open and unmerged; F021 is mid-feature.
3. R10's work is the bounded ring DECISION F021 D5 rules — `recent` on `BrainStreamState` and on `BrainStreamView`. The append belongs INSIDE `receiveBrainFrame` in `apps/ui/src/api/brainStream.ts`, not in the runner's `dispatch`: that function already drops a frame whose `seq` is not ahead of `lastSeq`, and an append placed in `dispatch` would duplicate a row on every reconnect replay.
4. The C4 handback commit of this round has never had its own `git status --porcelain` reading or insertion count recorded, because §3 checklist item 31 orders them nowhere. The next reviewer takes both at its first gate and records them in that round's entry.
