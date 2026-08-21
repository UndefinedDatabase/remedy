# Handback — F008 SSE event stream, R23 (the real DOM-free stream host, the R22 record)
## Range
Review of `476bfdfb`..C4, the handback commit itself (6 commits, branch feature/f008-sse-event-stream). C4's SHA cannot exist inside C4, so it is named by role and the round report carries the value (R-0371).
## Commits
### 467b32b9 docs(state): save the F008 R23 block verbatim
| Path | +/- | Reason |
| `.agent/authored/f008-r23.md` | +344/-0 | C0a, the R23 block saved byte for byte |

### 0b2f5cf7 docs(state): mirror the F008 R23 block into last_block
| Path | +/- | Reason |
| `.agent/last_block.md` | +292/-145 | C0b, the same bytes mirrored from the COMMITTED C0a blob |

### 46028e49 docs(state): set the plan to F008 R23, the real stream host
| Path | +/- | Reason |
| `.agent/plan.md` | +25/-26 | C1, PLANF008R23 applied whole |

### 7696ed84 docs(review): record the R22 verdict
| Path | +/- | Reason |
| `.agent/live_review.md` | +2/-0 | C2, LEDGER23's single paragraph appended |

### 96d316a6 feat(ui): land the real DOM-free host behind the stream seam
| Path | +/- | Reason |
| `apps/ui/src/api/brainStreamHost.ts` | +126/-0 | C3, HOSTSRC as a NEW file, whole |

### C4 docs(state): write the F008 R23 handback
| Path | +/- | Reason |
| `.agent/handoff.md` | self | C4 cannot table itself (R-0149); its numbers are in the round report |

## External actions
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — exit 0, `[]`, so the round continues on this branch. `git push -u origin feature/f008-sse-event-stream` is run ONCE, AFTER C4, and its output belongs to the round report (constraint 5). NOTHING merged, no PR created, no PR updated, no branch created (constraint 8). NO worktree was created or removed: nothing exercises the new module yet, so no red control was ordered and none was run (constraint 6).

## Verification
- G1 `.agent/STOP` ABSENT, read immediately before C0a; branch feature/f008-sse-event-stream; `git status --porcelain` EMPTY after each of C0a, C0b, C1, C2 and C3. The post-C4 porcelain and `git worktree list` are in the round report (constraint 5).
- G2 Transport EQUAL three ways — the scratch block at `.remedy-wt/f008-r23.md` as received, `.agent/authored/f008-r23.md` at C0a and `.agent/last_block.md` at C0b — sha256 3696b3b558ae5118a9d73589f025fd24af99047dc2b65e9067578efa19c9bc24, 21363 bytes, 344 lines, and that value EQUALS the digest carried in the task prompt.
- G3 THREE slices, the COUNT taken from the ordered extraction out of the COMMITTED C0a blob by their marker lines, newline-included as sha256/bytes/lines: PLANF008R23 377da548/2355/42, LEDGER23 46ec4d5d/2892/1 and HOSTSRC 664ce74e/4990/126 — all three equal to the digests the block names, at the 42 and 126 lines it names, and NONE carries trailing whitespace on any line (the offending-line list was empty for all three).
- G4 `.agent/plan.md` at C1 sha256 377da54827f189538d9aed747badb5a63d247487b9b57b05086848b39657e6fb, 2355 bytes, 42 lines (<50), BYTE-EQUAL to PLANF008R23; `Steps` occurs 1x, `## Goal` 1x and `## Next Steps` 1x line-anchored, `\bF\d{3}\b` matches `F008`.
- G5 (a) the C1 blob (3a3b873f, 464715 bytes, 1074 lines) is a byte-exact PREFIX of the C2 blob (bcebd967, 467608 bytes, 1076 lines) and the remainder == newline+LEDGER23, sha256 7701e4f6133d9e7b836037c8f072191625fccfc9df678743f623e9043769a3c4, 2893 bytes, 2 lines; (b) an INDEPENDENT blank-line split of the WHOLE C2 file, its terminating newline normalised first, gives 233 units whose LAST is LEDGER23's single paragraph. NEGATIVE CONTROL: one flipped ASCII byte of the remainder (offset 40, `.`→`X`) REJECTED by BOTH readings, the unflipped value ACCEPTED by BOTH.
- G6 At C1/C2, line-anchored: `^- R-\d+ — ` 200/200 — NO id was minted — `^- R-0629 — ` 0/0, `^Done: R-\d+ — ` 6/6, `^Landed: ` 0/0, `^Gate: R\d+ — ` 22/23 over 22 then 23 DISTINCT keys. Header sweep at C2: of 23 `^Gate: ` lines, 22 match `^Gate: R(\d+) — the R(\d+) entry\.` with second == first−1, 1 does NOT and its text begins `Gate: R1 — the F255 R21 entry. R21 PASSED and F255 IS CLOSED. NO finding is registered against it:`, and the R23 pair `Gate: R23 — the R22 entry.` occurs EXACTLY ONCE.
- G7 `git ls-tree 476bfdfb -- apps/ui/src/api/brainStreamHost.ts` is EMPTY, so the file did NOT exist at the base; its blob at C3 is sha256 664ce74eea95405886146ffd9bc28ed2850035c35219534c480e8552601eec42, BYTE-EQUAL to HOSTSRC's 664ce74eea95405886146ffd9bc28ed2850035c35219534c480e8552601eec42. `git show --numstat` at C3 reads 126/0 — insertions only, ZERO deletions, the file being new. `git ls-tree 96d316a6 -- apps/ui/src/api/brainStreamHost.test.ts` is EMPTY: NO test file was created (constraint 3).
- G8 PRIMARY checkout, run SERIALLY, never two test processes at once, AT C3. In `apps/ui`: `npm run --silent typecheck` EXIT 0 with NO output on stdout or stderr — the gate this round rests on — and `npx vitest run` EXIT 0 at 7 test files and 119 tests, UNCHANGED from the base, no test importing the new module yet. From the root: the state readers plus canary EXIT 0 at 465 passed + 0 skipped = 465, `tests/ui_contracts/` EXIT 0 at 393 passed + 4 skipped = 397. `npm run --silent lint` EXIT 1 at `56 problems (54 errors, 2 warnings)`, exactly constraint 7's measured value and one above the base's 55 because eslint cannot parse the one file this round adds — that is R-0622 and NOT a gate (R-0364). G8's STOP clause was never reached.
- G9 `git diff --name-only 476bfdfb..96d316a6` equals the Change set MINUS `.agent/handoff.md` exactly — five paths, none on either side alone; the full `476bfdfb..C4` reading is in the round report (constraint 5). Every commit in the range has exactly ONE parent. BOTH numstat cells per path from `git show --numstat`, each cross-checked against `git diff --numstat` and AGREEING: 344/0, 292/145, 25/26, 2/0 and 126/0 — every insertion under 500, and EVERY CELL, insertion and deletion, equal to the `+/-` column above.
- G10 Lines BEGINNING with `<<<SLICE ` or `<<<END `: 0 in `.agent/plan.md` at C1, 0 in `.agent/live_review.md` at C2, 0 in `apps/ui/src/api/brainStreamHost.ts` at C3, and 0 in this file, measured on the exact bytes committed as C4.
- G11 This round's own reflog entries, counted by the OPERATION before the first `:` in `%gs`: all five pre-C4 entries are `commit` (467b32b9, 0b2f5cf7, 46028e49, 7696ed84, 96d316a6, five entries found and five classified); `amend` 0, `rebase` 0, `cherry` 0. No total asserted.
- G12 This file carries every mandated section of docs/agents/handback_template.md and the item-status table below, which holds exactly one row for each of C0a, C0b, C1, C2, C3 and C4. Measured with `wc -l` in the session scratchpad BEFORE it was written it is 67 lines, UNDER the 100 this round's six commits allow, so no DECISION D15 stated-cause line is owed. One line per gate here; the raw transcripts are in the round report (R-0582).

## Authored-text proofs
- `.agent/authored/f008-r23.md` at C0a == the scratch block byte for byte and `.agent/last_block.md` at C0b == the same bytes (G2). ALL THREE slices were extracted from the COMMITTED C0a blob by their marker lines and applied unedited — never retyped, rewrapped, reflowed, reindented or whitespace-adjusted. G4 is the disk-to-disk byte-equality for PLANF008R23, G5 the ordered-append equality for LEDGER23 agreed by two independent readings with a negative control, and G7 the byte-equality for HOSTSRC as a new file. There was NO FROM/TO pair this round, so no containment reading is claimed. All three slices reached a commit; G10 confirms no marker line reached one.

## State — Fortschritt
~92 % (T001 ✅ · T002 ✅ · T003 Regeln+Treiber+Runner+Store ✅, Host kompiliert, Suite+Hook offen) — Schätzung

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |
## Deviations & assumptions
- No departure from the ordered commit sequence C0a, C0b, C1, C2, C3, C4. No extra commit, no dropped commit, no reordering; C1 was the first substantive commit, as constraint 2 requires. NO DEPENDENCY WAS ADDED (constraint 3): `apps/ui/package.json` and `apps/ui/package-lock.json` were not opened, no jsdom, happy-dom or testing library was installed or attempted, NO existing source file was edited and NO test file was created. R-0629 stays free, R-0628 stays OPEN with no `Done:` and no `Landed:` line, R-0622 stays OPEN and no TypeScript parser was added to make lint green (constraint 4). No objection is raised against any slice: all three applied cleanly and every value the block predicted was MET — 377da548 at 42 lines, 46ec4d5d, 664ce74e at 126 lines, the 22→23 gate move with findings held at 200, the 7-file/119-test vitest reading, the 465 and 397 pytest readings and the 56-problem lint value. Nothing was adjusted to make anything pass.
- The one thing this round does NOT claim: `apps/ui/src/api/brainStreamHost.ts` is COMPILED, not PROVED. No test imports it, so the unchanged 119 is evidence that it broke nothing, never that it works; its suite and its three red controls are R24's, and no round may call the module proved until they land.
- Commit-message convention: these six subjects carry no `Co-Authored-By` trailer, matching every prior round on this branch. The session command guard rejects `$(...)`, `; echo $?`, heredocs and chained `;` commands BY FORM, so every multi-step gate was written to a script under the gitignored `.remedy-wt/` and run from there; nothing from that directory was committed. No gate script needed a mid-round correction this time.

## Next
The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1); its SECOND is the Open PR Gate (Phase 1 rule 2), which returned `[]` at R23 and therefore continues on this branch. R23 IS PENDING REVIEW: its verdict is owed by the next round's ledger commit and no line of this round records one. The next free finding id is R-0629. R24's work is the adapter's OWN vitest suite plus three red controls — the malformed-frame guard, the close-before-reconnect and the polling cursor — which is what turns this round's compiled module into a proved one; R25 then adds the thin `useBrainStream` hook and the visible delayed badge under `npm run typecheck` plus a `tests/ui_contracts/` source contract (R-0628), and the integration gate follows before closure.
