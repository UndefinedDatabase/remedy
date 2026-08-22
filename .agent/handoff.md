# Handback — F021 R26, the ring round

Branch `feature/f021-live-activity-feed`. ROUND BASE `d121dd0935bfc072d96c5f6035a37d0df6b4099e` (short `d121dd09`).

Fortschritt: ~92 % (T002 — Uhr, Ankunftsstempel und Ring verdrahtet; es fehlen
             NowCard-Punkt und Feed-Scroll)
             — Schaetzung

## Range
Review of `d121dd09`..HEAD, HEAD being C6 — the commit that carries this file.

## Commits

### 6541c3d3 docs(state): save the F021 R26 step block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f021-r26.md` | +490/-0 | C0a — the block saved verbatim, byte for byte |

### 8381ef96 docs(state): mirror the F021 R26 step block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +411/-224 | C0b — written FROM the committed C0a blob |

### 9ba0f2ef docs(state): point the F021 plan at R26, the ring round
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +18/-19 | C1 — PLANF021R26 plus one terminator; 48 lines |

### 7eb82ed0 feat(ui): thread the arrival stamp through the feed ring
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/feedRow.ts` | +12/-2 | C2 — FEEDROWFIELD, FEEDROWSIG, FEEDROWRET |
| `apps/ui/src/api/brainStream.ts` | +2/-1 | C2 — RECVSIG, RECVCALL |
| `apps/ui/src/api/brainStreamDriver.ts` | +1/-1 | C2 — DRIVERTHREAD |
| `apps/ui/src/api/brainStream.test.ts` | +15/-3 | C2 — TESTDRIVE, TESTREPLAY, TESTPROJ, TESTSTAMP |
| `apps/ui/src/api/feedRow.test.ts` | +13/-1 | C2 — FEEDTESTSHIM, FEEDTESTSTAMP |
| `apps/ui/src/api/actionClass.test.ts` | +1/-1 | C2 — ACTIONROW |

### 024727c2 test(ui-contracts): retarget the ring seam pins at the stamped projection
| Path | +/- | Reason |
|---|---|---|
| `tests/ui_contracts/test_brain_stream_ring.py` | +3/-2 | C3 — CONTRACTPATHROW, CONTRACTCALL, CONTRACTGUARD; both existing guards retargeted, neither deleted nor loosened |

### 350cb7bc test(ui-contracts): pin the arrival stamp along the whole ring path
| Path | +/- | Reason |
|---|---|---|
| `tests/ui_contracts/test_brain_stream_ring.py` | +29/-0 | C4 — CONTRACTRINGSTAMP, carried ALONE |

### 3cdbdd65 docs(review): record the R25 verdict and DECISION F021 D8
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4/-0 | C5 — RECORD26 appended; no id minted, none resolved |

### C6 docs(state): hand back F021 R26 — SHA unnameable here, since this table sits inside the commit it describes (R-0494)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | C6 — this file |

## External actions
- `git worktree add .remedy-wt/r26-red 3cdbdd65` → exit 0, detached HEAD (G11 only).
- `apps/ui/node_modules` SYMLINKED into that worktree (`os.symlink`, `ln -s` semantics — never a copy, R-0591); unlinked before removal.
- `git worktree remove .remedy-wt/r26-red` → exit 0; `git worktree prune` → exit 0; `git worktree list` = the primary checkout ALONE.
- `gh pr list --state open --json number,headRefName` → exit 0, `[]`. NO `gh pr create` and NO `gh pr merge` was run this round.
- `git push -u origin feature/f021-live-activity-feed` → runs immediately AFTER C6; a commit cannot record the push that carries it. Its result is in the round report.

## Verification
G1 PASS — `.agent/STOP` ABSENT immediately before C0a and again before C6; branch `feature/f021-live-activity-feed`; `git status --porcelain` printed 0 lines after each of C0a, C0b, C1, C2, C3, C4 and C5 (C6's own reading is ordered nowhere). Owed reading from R25: `d121dd09` is single-parent and touches `.agent/handoff.md` alone at +51/-40, under the 500-insertion cap.
G2 PASS — sha256 `8c57ed2d6ba2f60dd466c84e83209f92829fa738082fccb5a18a4659714dd059`, 32107 bytes, 490 lines, EQUAL over all four copies: the reviewer's `.remedy-wt/f021-r26.md`, the bytes I read, `.agent/authored/f021-r26.md` at C0a and `.agent/last_block.md` at C0b, the last written FROM the committed C0a blob.
G3 PASS — my marker-line extractor over the COMMITTED C0a blob printed 3 whole texts (PLANF021R26, RECORD26, CONTRACTRINGSTAMP), 16 pairs and 180 CONTENT lines; 0 stray `<<<` lines. Re-measured from that same blob: TOTAL 490 against DECISION F085 D6's 490, PROSE 310 against D5's 400 — both equal to constraint 11.
G4 PASS — `cmp .agent/plan.md <PLANF021R26 + one newline>` exit 0; NEGATIVE CONTROL `cmp` against the bare slice exit 1 (EOF after byte 2875, line 48). Last byte is a newline; `wc -l` reads EXACTLY 48, equal to the reviewer's count; `^## Goal$` 1 and `^## Next Steps$` 1.
G5 PASS — all SIXTEEN FROMs read exactly 1 in their target at `d121dd09`. The FOURTEEN REWRITES read FROM 0 / TO 1 after their applying commit. FEEDROWRET and CONTRACTPATHROW, whose containment I re-measured TRUE, read FROM 1 / TO 1 and carry NO zero count. Deletions: C2 `7eb82ed0` 9, C3 `024727c2` 2.
G6 PASS — the C3 blob of `tests/ui_contracts/test_brain_stream_ring.py` (17713 B / 399 L) is a byte-exact PREFIX of the C4 file (19073 B / 428 L); remainder sha256 `910eba3e8773a44a36557c408a8a9e57794a3e82e4880d04701cbdc3e07f6aa3`, 1360 B, 29 lines. C4 ADDS 29 lines and DELETES 0; those 29 are ELEMENTWISE and IN ORDER the convention's TWO blank separator lines followed by CONTRACTRINGSTAMP's own 27 lines. Counted directly, not by a linter: EXACTLY 2 blank lines precede the new top-level class.
G7 PASS — reader (a): the `d121dd09` blob is a byte-exact PREFIX of the C5 file and the remainder is EXACTLY one newline + RECORD26 + one newline, sha256 `84c68a86710d8c786977d6888384b25a3fa0b2f70647a6071f352345a2b04d77`, 6200 B, 4 lines; file 566016 B / 1168 L before, 572216 B / 1172 L after. Reader (b), SET-WISE: units 265 → 267 with RECORD26 exactly 2 units, ELEMENTWISE equal over the WHOLE list. NEGATIVE CONTROL at offset 4 of the FIRST paragraph, byte `v` → `X` at equal length: BOTH readers REJECTED it and BOTH ACCEPTED the true file.
G8 PASS — base then C5: `- R-` 222 → 222, DISTINCT 222 at both; MAXIMUM registered id R-0659 at BOTH; `Done: R-` 0 → 0; `Landed: ` 0 → 0; `Gate: R` keys 24 → 25, DISTINCT at both; `Gate: R26` 0 → 1. The C5 diff has 0 deletion lines.
G9 PASS — PRIMARY checkout, from `apps/ui`, run SERIALLY: `npx tsc --noEmit` exit 0 with EMPTY stdout and stderr; `npm run test:unit` exit 0 at 15 files and 212 tests — the reviewer's base reading was 15 and 209, and this round adds exactly the 3 new cases.
G10 PASS — PRIMARY checkout, working directory `/home/decodeux/Repos/remedy`, run SERIALLY, counted BY PASSED PLUS SKIPPED: `tests/ui_contracts/` exit 0 at 472 passed + 4 skipped = 476; `tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py` exit 0 at 511 passed = 511; canary `tests/cli/test_golden_path.py` exit 0 at 42.
G11 PASS, ALL THREE WENT RED — disposable worktree `.remedy-wt/r26-red` at `3cdbdd65`, `node_modules` symlinked, NEVER the primary checkout. Green first: tsc 0, vitest 15 files / 212 tests, `tests/ui_contracts/` 471 passed + 5 skipped = 476 (one more skip than primary, for want of `apps/ui/dist/`). The target line measured 1 occurrence whole-line AND 1 indent-agnostic, agreeing. Mutated to pass a literal `0`: `npx tsc --noEmit` exit 2, `src/api/brainStream.ts(89,3): error TS6133: 'receivedAtMs' is declared but its value is never read.`; `npm run test:unit` exit 1, 2 failed — `the recent ring > the row carries the arrival stamp the transport handed in` and `the recent ring > each row keeps its OWN stamp as the ring fills`; `pytest tests/ui_contracts/` exit 1, 3 failed — `test_brain_stream_ring.py::TestAppendSitsBehindTheReplayGuard::test_the_projection_is_called_inside_receive_brain_frame`, `::TestAppendSitsBehindTheReplayGuard::test_the_replay_guard_returns_before_the_append`, `::TestTheRingCarriesTheArrivalStamp::test_the_ring_threads_the_stamp_into_the_row`. Byte restored, file byte-identical (sha256 `9c4412851b0761b1f8e95262e8d5b0574615679aaeda297f9604a4e1a6cf1d3a`), all three green again.
G12 PASS — `d121dd09`..`3cdbdd65`: path set EQUAL to the eleven non-handoff `Change:` paths, difference EMPTY BOTH ways; all seven commits single-parent; `git show --numstat` and `git diff --numstat` agree cell by cell with every `## Commits` table above; insertions 490, 411, 18, 44, 3, 29, 4 — each under the 500 cap; `git ls-files .remedy-wt` 0; `git worktree list` the primary checkout ALONE; `gh pr list --state open` EMPTY. Marker sweep, LINE-ANCHORED over all SIX prefixes this block uses (`<<<SLICE `, `<<<END `, `<<<PAIR `, `<<<FROM`, `<<<TO`, `<<<ENDPAIR`) plus any line starting `<<<`: 0 in each of the nine files a slice or pair LANDED in; the two block mirrors read 70 by construction. Reflog BY OPERATION FIELD (text before the first `:`), scoped to this round's seven rows: every operation is `commit`, and `amend`, `rebase` and `cherry` each occur 0 times in that field.

## Authored-text proofs
PLANF021R26 — `cmp` against the slice extracted from the committed C0a blob plus one terminator: exit 0; negative control against the bare slice: exit 1. RECORD26 — prefix-plus-remainder equality under two independent readers with a same-length mutant rejected (G7). CONTRACTRINGSTAMP — prefix equality plus elementwise ordered equality of the added lines (G6). All 16 pair halves were extracted MECHANICALLY from the committed C0a blob by their marker lines and applied by exact byte replacement, refusing unless FROM occurred exactly once; not one half was retyped, rewrapped, reflowed or reindented.

## Deviations & assumptions
None. The ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6 was executed exactly: no extra commit, none dropped, none reordered. C2 was kept as ONE commit across all six TypeScript files per constraint 3, and no default value was added anywhere.
Observations, no action taken and no slice altered: (a) FEEDTESTSHIM places its shim `function feedRowOf` BETWEEN two `import` statements in `feedRow.test.ts`; that is legal TypeScript and it was applied byte for byte rather than tidied. (b) `.agent/decisions.md` was not touched — DECISION F021 D8 lives in `.agent/live_review.md`, which is the only path the `Change:` list allows for it.
DECISION D15 overage, declared: this file measures 101 lines by `wc -l`. That is over the 60-line baseline cap AND one line over the ≤100 tier the template grants a handback with per-commit tables for more than 5 commits; this round has 8. Cause is mandated content only — eight per-commit changed-files tables for C0a through C6, twelve one-line gate results, the item-status table, the external-actions list and the authored-text proofs. No section was dropped and no transcript was inlined (R-0582).

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | `6541c3d3` |
| C0b | done | `8381ef96` |
| C1 | done | `9ba0f2ef` |
| C2 | done | `7eb82ed0`, one commit, six files |
| C3 | done | `024727c2` |
| C4 | done | `350cb7bc`, alone |
| C5 | done | `3cdbdd65` |
| C6 | done | this commit |

## Next
THIS SESSION IS OVER. The NEXT session begins at docs/agents/self_drive_protocol.md Phase 1 rule 1 — the `.agent/STOP` check — BEFORE rule 2's Open PR Gate (R-0347); that gate will find NO open pull request, so rule 5 applies and F021 continues on this branch. R26's own verdict is UNRECORDED and the next round's ledger commit owes it. R27 builds the NowCard's recency dot from `recency.ts` with the CSS `docs/ui/design_reference/assets_spec.md` governs — the first round able to subtract two instants on ONE clock.
