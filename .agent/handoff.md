# Handback — F008 R10 (SSE event stream: the route, the writer, 404 before the stream)

## Range
Review of `a063be56`..HEAD. C5 is this commit (R-0149 self-reference).

## Commits

### b96dec03 chore(authored): save the F008 R10 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f008-r10.md | +489/-0 | C0a saves the block verbatim |

### 0743410b chore(state): mirror the F008 R10 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +428/-126 | C0b mirrors the same bytes |

### 1613ae7e chore(plan): advance the plan to F008 R10
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +15/-18 | C1 applies PLANF008R10, ahead of the ledger |

### 42df4347 docs(review): record the R9 verdict in the ledger
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C2 appends LEDGER10, no id minted |

### bd5ca5d2 feat(ui-server): stream a job's SSE events on a route
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | +65/-0 | C3, all four pairs |

### 5f763ba4 test(ui-server): cover the SSE route, writer and disconnect
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_sse_stream.py | +154/-0 | C4 appends TESTS10 |

### C5 (this commit) docs(state): write the F008 R10 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C5; its own numbers belong to the round report |

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

## External actions
- `git worktree add --detach .remedy-wt/g11 5f763ba4` → created for G11; `git worktree remove` then `git worktree prune` → primary checkout alone.
- `git push -u origin feature/f008-sse-event-stream` → `a063be56..5f763ba4`, tracking set; pushed again after C5.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`. No PR created, no branch created, nothing merged.

## Verification
- G1 `.agent/STOP` absent before C0a; branch feature/f008-sse-event-stream; `git status --porcelain` empty after every commit and at the handback; `git worktree list` names the primary checkout alone.
- G2 scratch block, `.agent/authored/f008-r10.md` at C0a and `.agent/last_block.md` at C0b are all sha256 b8446596…350590, 27169 bytes, 489 lines — all three EQUAL.
- G3 11 slices by ordered extraction from the committed C0a blob, newline-included; e.g. PLANF008R10 f2003a51/2236 B/42 L, LEDGER10 83a82ef5/2531 B/1 L, TESTS10 5c5ddc27/6499 B/154 L. Full per-slice table in the round report.
- G4 `.agent/plan.md` at C1: f2003a51…, 2236 bytes, 42 lines (<50), byte-equal to PLANF008R10 = true; `^## Goal$` 1, `^## Next Steps$` 1, `F008` 2.
- G5 (a) the C1 blob is a byte-exact prefix and the remainder is 87adc12d…, 2532 bytes, 2 lines, equal to a newline plus LEDGER10; (b) an independent blank-line split of the normalised C2 file yields 202 units whose LAST equals LEDGER10's paragraph. NEGATIVE CONTROL: a one-byte flip is REJECTED by both readings, the unflipped value ACCEPTED by both.
- G6 at C1/C2: `^- R-\d+ — ` 188/188, `^Done: R-\d+ — ` 0/0, `^Landed: ` 0/0, `^Gate: R\d+ — ` 9/10 over ten DISTINCT keys R1..R10, `^- R-0617 — ` 0/0. Header shape `^Gate: R(\d+) — the R(\d+) entry\.` with second = first−1 matches `Gate: R10 — the R9 entry.` exactly once.
- G7 FROM count at `a063be56` is 1 for all four pairs. IMPORT: FROM at C3 = 0 and the TO occurs 1x. DRAIN, ROUTE, METHOD: the TO occurs exactly 1x each in the C3 blob.
- G8 the `a063be56` and C3 blobs of ui_server.py DIFFER; `^import time$` occurs 1x at C3 and 0x at `a063be56`; C3 numstat is +65/−0.
- G9 the C3 blob of the test file is a byte-exact PREFIX of its C4 blob (true), TESTS10 is an exact SUFFIX of the C4 blob (true), and the 154 lines C4's diff ADDS are exactly TESTS10's 154 lines in order (true).
- G10 serially, in the primary checkout: the state-reader command exits 0 at 427 passed + 0 skipped = 427; `tests/docs/` exits 0 at 295 + 0 = 295. `tests/ui_server/test_sse_stream.py` alone collects 27 at C4. TESTS10 adds 13 tests, and the measured 414 + 13 = 427 reconciles exactly.
- G11 RED PROOF in a disposable worktree at C4, never in the primary checkout: with `packages/orchestration/ui_server.py` alone restored to its `a063be56` blob the file EXITS 1 with 11 failed / 16 passed, the failures naming `drain_sse_frames` and `_send_sse_stream` — the round's new writer and route. Restored to the C4 blob the same command EXITS 0 at 27 passed. Worktree removed and pruned; `git worktree list` names the primary checkout alone.
- G12 ruff rule-code MULTISETS are EQUAL: empty at `a063be56` (read via `git show <sha>:<path>` piped through `ruff check --stdin-filename <path> -`, nothing written to the checkout) and empty at C4; exit 0 at both, behind a red control that returned {I001:1, F401:1} at exit 1.
- G13 `git diff --name-only a063be56..C5` equals the Change list with no path on either side alone; every commit in the range has exactly one parent; insertions 489, 428, 15, 2, 65, 154 are each under 500 and agree cell by cell with the `+/-` column above.
- G14 lines beginning `<<<SLICE ` or `<<<END `: 0 in plan.md@C1, live_review.md@C2, ui_server.py@C3, test_sse_stream.py@C4 and handoff.md@C5.
- G15 over this round's own reflog entries the OPERATION (text before the first `:` of `%gs`) is `commit` throughout; amend 0, rebase 0, cherry 0. No total asserted.
- G16 `git push` reported `a063be56..5f763ba4` and then the C5 fast-forward; `gh pr list --state open` returned `[]`. Nothing merged.
- G17 this file carries every section docs/agents/handback_template.md mandates plus the item-status table naming C0a, C0b, C1, C2, C3, C4 and C5 exactly once each. Its line count is 85, under the 100-line cap this round's seven commits allow, so no DECISION D15 stated-cause line is owed.

## Authored-text proofs
Every slice was applied byte for byte out of the committed `.agent/authored/f008-r10.md`, none retyped, rewrapped or edited. Disk-to-disk results: PLANF008R10 byte-equal to `.agent/plan.md` at C1 (G4); LEDGER10 confirmed by prefix-plus-remainder AND by an independent blank-line split, both with a negative control (G5); IMPORT, DRAIN, ROUTE and METHOD confirmed by their FROM/TO counts in the C3 blob (G7); TESTS10 confirmed by prefix, suffix and ordered equality against C4's diff (G9).

## Deviations & assumptions
The ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5 was followed exactly: no extra commit, none dropped, none reordered. One OBJECTION to the block, declared rather than acted on: constraint 9 requires every suite to run in the PRIMARY checkout, while G11 requires its run in a DISPOSABLE worktree and never in the primary checkout. G11 is the specific order and self_drive_protocol G5 requires that isolation, so G11 was followed; its command touches no `apps/ui/node_modules`, and the restored-blob run exiting 0 at 27 shows the worktree reading is sound. Constraint 9's stated rationale (untrustworthy pass counts without node_modules) is read as binding the G10 count suites.

## Next
The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1). Its SECOND is the Open PR Gate (Phase 1 rule 2), which finds no open pull request and therefore continues on feature/f008-sse-event-stream at R11 — the per-job connection cap answering 429 beyond it and the framing golden the feature file names as T001's contract test.
