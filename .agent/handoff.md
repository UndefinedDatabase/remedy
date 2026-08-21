# Handoff — F008 SSE event stream, R8 (worker → reviewer)

Branch: feature/f008-sse-event-stream. Open findings: 186 registered, 0 `Done:` lines; R-0614 registered this round.

## Range
Review of `83408011`..HEAD, where HEAD is the tip this commit creates (its SHA cannot exist in the text that becomes it).

## Commits
### dd4c36ff chore(authored): save the F008 R8 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f008-r8.md | +489/-0 | C0a, the step block saved verbatim |
### 0e375f9a chore(state): mirror the F008 R8 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +442/-211 | C0b, single state-file rewrite of the same bytes |
### ee08a6cf chore(plan): advance the plan to F008 R8
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +22/-21 | C1, PLANF008R8 applied byte for byte |
### dd762b80 docs(review): register R-0614 and record the R6 and R7 verdicts
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | C2, LEDGER appended before either fix commit |
### f6ddcd8c feat(ui-server): add the SSE frame reader and the shared event envelope
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | +78/-11 | C3, SUMMARY rewrite then HELPERS append |
### dc5e95db test(ui-server): cover the SSE frame reader and heartbeat cadence
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_sse_stream.py | +147/-0 | C4, TESTSSE applied byte for byte, new file |
### (this commit) docs(state): write the F008 R8 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | see round report | C5, a handoff cannot table the commit that writes it (R-0149) |

## External actions
- `git worktree add --detach .remedy-wt/g11 HEAD` → exit 0; `git worktree remove --force` + `prune` → exit 0 (G11 red proof).
- `git worktree add --detach .remedy-wt/g12base 83408011` → exit 0; removed and pruned → exit 0 (G12 base lint).
- `git push -u origin feature/f008-sse-event-stream` → see G16.
- `gh pr list --state open` → empty list. Nothing merged, no PR created, no branch created.

## Verification
- G1 `.agent/STOP` absent before C0a; branch feature/f008-sse-event-stream; `git status --porcelain` empty after every commit and at the handback; `git worktree list` names the primary checkout alone.
- G2 Transport EQUAL three ways — scratch block, `.agent/authored/f008-r8.md` at C0a, `.agent/last_block.md` at C0b — sha256 c8bd326868b2e828f9b8510a1c8ddbee9c8cdd19447217869985d9831c72083a, 31403 bytes, 489 lines.
- G3 7 slices by ordered extraction from the COMMITTED authored file: PLANF008R8 ce848d01 2551b 45L · LEDGER b7a33b2b 7207b 5L · SUMMARYFROM f9bb5a39 496b 11L · SUMMARYTO eee8d7a6 118b 4L · HELPERSFROM 3562a4b8 41b 1L · HELPERSTO b768feba 2710b 75L · TESTSSE 26c3a934 5588b 147L.
- G4 `.agent/plan.md` at C1 sha256 ce848d01…c98b, 2551 bytes, 45 lines (<50), byte-equal to PLANF008R8; `## Goal` 1, `## Next Steps` 1, `F008` 2.
- G5 (a) C1 blob is a byte-exact prefix of C2, remainder de191e03… 7208 bytes 6 lines = newline+LEDGER; (b) independent blank-line split into 198 units whose last three are LEDGER's three paragraphs in order; one flipped byte REJECTED by both readings, unflipped accepted by both.
- G6 `.agent/live_review.md` C1→C2: `^- R-\d+ — ` 185→186, `^Done: R-\d+ — ` 0→0, `^Landed: ` 0→0, `^Gate: R\d+ — ` 6→8 over 8 DISTINCT keys R1..R8, `^- R-0614 — ` 0→1, `^- R-0615 — ` 0 at both.
- G7 `ui_server.py` 83408011→C3: SUMMARYFROM 1→0, SUMMARYTO 0→1, HELPERSFROM 1→1, HELPERSTO 0→1 (contained exactly once); `git show --numstat f6ddcd8c` = 78 insertions, 11 deletions.
- G8 C3 adds 78 lines to the path; HELPERS TO 75 lines minus its 1 FROM line = 74. Whole-diff reading FALSE, pair-scoped reading TRUE: added[0:4] equals SUMMARY TO in order, added[4:78] equals the 74 TO-minus-FROM lines in order. See Deviations.
- G9 `tests/ui_server/test_sse_stream.py` at C4 sha256 26c3a934…b11c, 5588 bytes, 147 lines, byte-equal to TESTSSE; `git show --numstat dc5e95db` = 147 insertions, 0 deletions (insertions = line count).
- G10 Primary checkout, run SERIALLY: state readers exit 0 at 414 passed + 0 skipped = 414; `tests/docs/` exit 0 at 295 passed + 0 skipped = 295. Arithmetic: 400 (constraint 10) + 14 collected in the new file = 414.
- G11 RED PROOF in a disposable worktree: `ui_server.py` reverted to its 83408011 blob → exit 1, 14 failed, 0 passed; restored to the C3 blob (byte-identical, sha256 e2b132e7…) → exit 0, 14 passed. Worktree removed and pruned; `git worktree list` = primary alone.
- G12 Red control FIRST on scratch input: exit 1, multiset ['F821','I001'] — non-empty, so the extractor reads. Then `ruff check --output-format json`: `ui_server.py` at 83408011 (in a worktree) exit 0 empty; at C3 exit 0 empty; `test_sse_stream.py` at C4 exit 0 empty.
- G13 `git diff --name-only 83408011..C5` equals the Change list exactly, no path on either side alone; every commit single-parent; insertions 489, 442, 22, 6, 78, 147 — all under 500 — agreeing cell by cell with the `+/-` column above.
- G14 Marker lines (`^<<<SLICE ` / `^<<<END `): `.agent/plan.md` at C1 0, `.agent/live_review.md` at C2 0, `ui_server.py` at C3 0, `test_sse_stream.py` at C4 0, `.agent/handoff.md` at C5 0.
- G15 This round's own reflog entries by OPERATION (text before the first `:`): `amend` 0, `rebase` 0, `cherry` 0.
- G16 `git push -u origin feature/f008-sse-event-stream` → see round report; `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`. Nothing merged.
- G17 This file: every mandated section present, item-status table below, line count in the round report; cap 100.

## Authored-text proofs
Every applied slice was extracted from the COMMITTED `.agent/authored/f008-r8.md` by its marker lines and compared byte for byte on disk: `.agent/plan.md` == PLANF008R8 (True), `.agent/live_review.md` remainder == newline+LEDGER (True, two independent readings), `ui_server.py` contains SUMMARY TO once and HELPERS TO once with both FROM bodies accounted for, `tests/ui_server/test_sse_stream.py` == TESTSSE (True). Nothing was retyped, rewrapped or edited.

## Deviations & assumptions
- No departure from the ordered commit sequence: C0a, C0b, C1, C2, C3, C4, C5 were committed in that order, none added, none dropped, none reordered.
- OBJECTION, G8 scope. G8 reads "the lines C3's diff ADDS ... are, IN ORDER, exactly the HELPERS TO lines absent from its FROM body". C3 carries BOTH pairs, so its added set is 78 lines, of which 4 belong to the SUMMARY REWRITE; the literal whole-diff comparison is therefore FALSE by construction, not by defect. Both readings are reported above and nothing was changed to make either agree. §4.9's ordered-equality obligation, read pair-scoped, HOLDS exactly.
- G12 red-control count. The block cites a red control returning four codes; mine returns two (F821, I001). The multiset is a property of the control file's own contents, which the block does not fix, not of this repository — the ordered property, a NON-EMPTY multiset at non-zero exit, holds.
- `.agent/context.md` untouched per constraint 7: its clause "T001's endpoint itself is NOT built yet" stays true after C3, which lands the reader and no route.

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |

## Next
The next session's FIRST action is the `.agent/STOP` re-read from disk (Phase 1 rule 1), its SECOND the Open PR Gate (Phase 1 rule 2). Then continue here at R9: wire this reader to `GET /api/jobs/<jid>/events/stream` beside the `events-since` branch in `_RemedyHandler.do_GET`, with the socket writer and a 404 for an unknown job before one byte of stream.
