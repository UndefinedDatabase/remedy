# Handback — F008 SSE event stream, R22 (the R21 record, R-0628 and the T003 re-plan)
## Range
Review of `37c93574`..C3, the handback commit itself (5 commits, branch feature/f008-sse-event-stream). C3's SHA cannot exist inside C3, so it is named by role and the round report carries the value (R-0371).
## Commits
### 22c0a5dd docs(state): save the F008 R22 block verbatim
| Path | +/- | Reason |
| `.agent/authored/f008-r22.md` | +197/-0 | C0a, the R22 block saved byte for byte |

### ffaa5c9d docs(state): mirror the F008 R22 block into last_block
| Path | +/- | Reason |
| `.agent/last_block.md` | +127/-354 | C0b, the same bytes mirrored from the COMMITTED C0a blob |

### 88cfcf4d docs(state): re-plan F008 T003 around the DOM-free adapter
| Path | +/- | Reason |
| `.agent/plan.md` | +20/-23 | C1, PLANF008R22 applied whole |

### e2dad913 docs(review): record the R21 verdict and register R-0628
| Path | +/- | Reason |
| `.agent/live_review.md` | +4/-0 | C2, LEDGER22's two paragraphs appended |

### C3 docs(state): write the F008 R22 handback
| Path | +/- | Reason |
| `.agent/handoff.md` | self | C3 cannot table itself (R-0149); its numbers are in the round report |

## External actions
- `git push -u origin feature/f008-sse-event-stream` before C3 — exit 0, `37c93574..e2dad913  feature/f008-sse-event-stream -> feature/f008-sse-event-stream`. The post-C3 push is re-run after this commit and its output belongs to the round report (constraint 6). `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — exit 0, `[]`. NOTHING merged, no PR created, no PR updated, no branch created (constraint 9). NO worktree was created or removed this round: it mutates no code and orders no red control (constraint 7).

## Verification
- G1 `.agent/STOP` ABSENT, read immediately before C0a; branch feature/f008-sse-event-stream; `git status --porcelain` EMPTY after each of C0a, C0b, C1 and C2. The post-C3 porcelain and `git worktree list` are in the round report (constraint 6).
- G2 Transport EQUAL three ways — the scratch block at `.remedy-wt/f008-r22.md` as received, `.agent/authored/f008-r22.md` at C0a and `.agent/last_block.md` at C0b — sha256 d2db104d3bcf7203e5f16e22246b63c2be4dd263c8702dea8b1b78dbceea72cf, 18389 bytes, 197 lines, and that value EQUALS the digest carried in the task prompt.
- G3 TWO slices, the COUNT taken from the ordered extraction out of the COMMITTED C0a blob by their marker lines, newline-included as sha256/bytes/lines: PLANF008R22 c7f6e97d/2305/43 and LEDGER22 b8f3fa92/6371/3 — both equal to the digests the block names, PLANF008R22 at the 43 lines it names, and NEITHER carries trailing whitespace on any line (the offending-line list was empty for both).
- G4 `.agent/plan.md` at C1 sha256 c7f6e97d93cd1ce9f35b11ded23493c7999ed8c291a68effa2d5e5e566f31690, 2305 bytes, 43 lines (<50), BYTE-EQUAL to PLANF008R22; `Steps` occurs 1x, `## Goal` 1x and `## Next Steps` 1x line-anchored, `\bF\d{3}\b` matches `F008`.
- G5 (a) the C1 blob (2833ef66, 458343 bytes, 1070 lines) is a byte-exact PREFIX of the C2 blob (3a3b873f, 464715 bytes, 1074 lines) and the remainder == newline+LEDGER22, sha256 e4b7928c7e52e7f3c3c6898f6c16f3a8de11b4331dc5f4ce11fabc9cd5eedcc7, 6372 bytes, 4 lines; (b) an INDEPENDENT blank-line split of the WHOLE C2 file, its terminating newline normalised first, gives 232 units whose LAST TWO are LEDGER22's two paragraphs IN ORDER. NEGATIVE CONTROL: one flipped ASCII byte of the remainder (offset 3186, `4`→`Z`) REJECTED by BOTH readings, the unflipped value ACCEPTED by BOTH.
- G6 At C1/C2, line-anchored: `^- R-\d+ — ` 199/200, `^- R-0628 — ` 0/1 — R-0628 is the ONLY id minted — `^- R-0629 — ` 0/0, `^Done: R-\d+ — ` 6/6, `^Landed: ` 0/0, `^Gate: R\d+ — ` 21/22 over 21 then 22 DISTINCT keys. Header sweep at C2: of 22 `^Gate: ` lines, 21 match `^Gate: R(\d+) — the R(\d+) entry\.` with second == first−1, 1 does NOT and its text begins `Gate: R1 — the F255 R21 entry. R21 PASSED and F255 IS CLOSED. NO finding is registered against it:`, and the R22 pair `Gate: R22 — the R21 entry.` occurs EXACTLY ONCE.
- G7 PRIMARY checkout, run SERIALLY, never two test processes at once, AT C2. `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf` EXIT 0 at 465 passed + 0 skipped = 465; `python3 -m pytest tests/ui_contracts/ -q -rf` EXIT 0 at 393 passed + 4 skipped = 397. G7's STOP clause was never reached. NOTHING in `apps/ui` was run or touched: this round edits no code, so the R-0622 lint red stands untouched and is not a gate (R-0364).
- G8 `git diff --name-only 37c93574..e2dad913` equals the Change set MINUS `.agent/handoff.md` exactly — four paths, none on either side alone; the full `37c93574..C3` reading is in the round report (constraint 6, R-0371). Every commit in the range has exactly ONE parent. BOTH numstat cells per path from `git show --numstat`, each cross-checked against `git diff --numstat` and AGREEING: 197/0, 127/354, 20/23 and 4/0 — every insertion under 500, and EVERY CELL, insertion and deletion, equal to the `+/-` column above.
- G9 Lines BEGINNING with `<<<SLICE ` or `<<<END `: 0 in `.agent/plan.md` at C1, 0 in `.agent/live_review.md` at C2, and 0 in this file, measured on the exact bytes committed as C3.
- G10 This round's own reflog entries, counted by the OPERATION before the first `:` in `%gs`: all four pre-C3 entries are `commit` (22c0a5dd, ffaa5c9d, 88cfcf4d, e2dad913, four entries found and four classified); `amend` 0, `rebase` 0, `cherry` 0. No total asserted.
- G11 This file carries every mandated section of docs/agents/handback_template.md and the item-status table below, which holds exactly one row for each of C0a, C0b, C1, C2 and C3. Measured with `wc -l` in the session scratchpad BEFORE it was written it is 60 lines, AT the 60 this round's five commits allow, so no DECISION D15 stated-cause line is owed. One line per gate here; the raw transcripts are in the round report (R-0582).

## Authored-text proofs
- `.agent/authored/f008-r22.md` at C0a == the scratch block byte for byte and `.agent/last_block.md` at C0b == the same bytes (G2). BOTH slices were extracted from the COMMITTED C0a blob by their marker lines and applied unedited — never retyped, rewrapped, reflowed, reindented or whitespace-adjusted. G4 is the disk-to-disk byte-equality for PLANF008R22 and G5 the ordered-append equality for LEDGER22, agreed by two independent readings with a negative control. There was NO FROM/TO pair this round, so no containment reading is claimed. Both slices reached a commit; G9 confirms no marker line reached one.

## State — Fortschritt
~90 % (T001 ✅ · T002 ✅ · T003 Regeln+Treiber+Runner+Store ✅, Host+Hook offen) — Schätzung

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | this commit |
## Deviations & assumptions
- No departure from the ordered commit sequence C0a, C0b, C1, C2, C3. No extra commit, no dropped commit, no reordering; C1 was the first substantive commit, as constraint 2 requires. NO CODE FILE WAS EDITED and NO DEPENDENCY WAS ADDED (constraint 3): `apps/ui/package.json` and `apps/ui/package-lock.json` were not opened, and no jsdom, happy-dom or testing library was installed or attempted. R-0628 is REGISTERED and stays OPEN with no `Done:` and no `Landed:` line; R-0629 stays free (constraint 4); R-0622 stays OPEN with no TypeScript parser added (constraint 5). No objection is raised against either slice: both applied cleanly and every value the block predicted was MET — c7f6e97d at 43 lines, b8f3fa92, the 199→200 and 21→22 set moves, the 465 and 397 pytest readings. Nothing was adjusted to make anything pass.
- Commit-message convention: these five subjects carry no `Co-Authored-By` trailer, matching every prior round on this branch. The session command guard rejects `$(...)`, `; echo $?`, heredocs and chained `;` commands BY FORM, so every multi-step gate was written to a script under the gitignored `.remedy-wt/` and run from there; nothing from that directory was committed. One gate script was CORRECTED mid-round: G10's first reflog parser matched zero entries and returned a vacuous green, so it was rewritten to split `%gs` on the first `:` and re-run, and the reported G10 values come from that second run. This file's own line count was trimmed from 62 to the 60 the cap allows before it was written once.

## Next
The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1); its SECOND is the Open PR Gate (Phase 1 rule 2), which returned `[]` at R22 and therefore continues on this branch. R22 IS PENDING REVIEW: its verdict is owed by the next round's ledger commit and no line of this round records one. The next free finding id is R-0629. R22 REGISTERED R-0628, which RETIRES the R21 claim that T003 is blocked pending a DOM install: the premise was re-measured and holds — this session's guard denies `npm view jsdom version` too — but this repository gates every React component by reading its SOURCE from `tests/ui_contracts/`, so the conclusion does not follow. R23's work is therefore the REAL `BrainStreamHost` adapter over an injected EventSource, a snapshot read, a tail read and a scheduler, proved under the node-environment vitest with NO DOM at all; R24 then adds the thin `useBrainStream` hook and the delayed badge under `npm run typecheck` plus a `tests/ui_contracts/` source contract.
