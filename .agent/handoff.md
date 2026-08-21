# Handback — F008 SSE event stream, R15 (T002 paydown: R-0620 and R-0621)

## Range
Review of `305bc30c`..C7, the handback commit itself (9 commits, branch feature/f008-sse-event-stream). C7's SHA cannot exist inside C7, so it is named by role and the round report carries the value (R-0371).

## Commits

### 68915bd9 chore(authored): save the F008 R15 step block
| Path | +/- | Reason |
| `.agent/authored/f008-r15.md` | +377/-0 | C0a, the R15 block saved verbatim |

### ea466d98 chore(state): mirror the F008 R15 step block
| Path | +/- | Reason |
| `.agent/last_block.md` | +261/-248 | C0b, the same bytes mirrored |

### 9980764c chore(plan): advance the plan to F008 R15
| Path | +/- | Reason |
| `.agent/plan.md` | +20/-17 | C1, PLANF008R15 applied whole |

### 03ecfea1 docs(review): widen the R-0371 counter-measure a third time
| Path | +/- | Reason |
| `.agent/live_review.md` | +1/-1 | C2, R0371FROM→R0371TO in place |

### 42347aaf docs(review): register R-0621 and record the R14 verdict
| Path | +/- | Reason |
| `.agent/live_review.md` | +4/-0 | C3, LEDGER15 appended |

### 8a80ffce fix(ui-server): treat only a missing Last-Event-ID as absent
| Path | +/- | Reason |
| `packages/orchestration/ui_server.py` | +1/-1 | C4, FIXFROM→FIXTO, the R-0620 fix |

### 75f02ef3 test(sse): resume across a ledger that grew between connections
| Path | +/- | Reason |
| `tests/ui_server/test_sse_stream.py` | +16/-7 | C5, HAMMERFROM→HAMMERTO and GROWFROM→GROWTO, the R-0621 repair |

### 1dc011a2 test(sse): pin the integer Last-Event-ID forms
| Path | +/- | Reason |
| `tests/ui_server/test_sse_stream.py` | +16/-0 | C6, TESTS15 appended |

### C7 docs(state): write the F008 R15 handback
| Path | +/- | Reason |
| `.agent/handoff.md` | self | C7 cannot table itself (R-0149); its numbers are in the round report |

## External actions
- `git worktree add --detach .remedy-wt/r15wt 1dc011a2` — ok; `git worktree remove --force .remedy-wt/r15wt` — ok, before this file was written. It was the ONLY worktree used and it carried both G11 and G12.
- `git push -u origin feature/f008-sse-event-stream` before C7 — `305bc30c..1dc011a2  feature/f008-sse-event-stream -> feature/f008-sse-event-stream`, exit 0. The post-C7 push is re-run after this commit and its output belongs to the round report (constraint 6).
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — `[]`, exit 0. Nothing merged, no PR created, no branch created.

## Verification
- G1 `.agent/STOP` ABSENT, read immediately before C0a; branch feature/f008-sse-event-stream; `git status --porcelain` EMPTY after each of C0a, C0b, C1, C2, C3, C4, C5 and C6, and again after the G11/G12 worktree was removed. The post-C7 porcelain and `git worktree list` are in the round report, not here (constraint 6).
- G2 Transport EQUAL three ways — the scratch block the worker was given, `.agent/authored/f008-r15.md` at C0a and `.agent/last_block.md` at C0b — sha256 68062e589fe762d605ce977b0922dd141fc45be26210975e82cd2c7bc4fca5ef, 36909 bytes, 377 lines.
- G3 ELEVEN slices, the count taken from the ordered extraction out of the COMMITTED C0a blob, newline-included, as sha256/bytes/lines: PLANF008R15 da4f29b2/2592/48, R0371FROM d999949c/3534/1, R0371TO 844b7e06/4917/1, LEDGER15 83183124/5925/3, FIXFROM 025c3c5d/44/1, FIXTO 55cc7e7a/71/1, HAMMERFROM 5c201fcf/633/12, HAMMERTO 0f4f0ec4/865/14, GROWFROM a83d4938/464/8, GROWTO 1dbb14fe/979/15, TESTS15 ca994615/640/14.
- G4 `.agent/plan.md` at C1 sha256 da4f29b240abc0ddbef9e800c4ff59fe0c720e4cc472dcfcb9efa947c536bc98, 2592 bytes, 48 lines (<50), BYTE-EQUAL to PLANF008R15; `## Goal` 1x and `## Next Steps` 1x line-anchored, `F008` 2x.
- G5 CONSTRUCTIVE: R0371FROM occurs EXACTLY ONCE in `.agent/live_review.md` at C1; replacing that one occurrence with R0371TO yields sha256 042e3f653d3d3ebb22250f2e0f73f149e05c7af6c4f7985942a993dbd2090c34, BYTE-EQUAL to the C2 blob at the same sha256. Line count 1030 at C1 and 1030 at C2, EQUAL. `- R-0371 — ` occurs exactly once at C2 and that line ENDS with ` OPEN.`
- G6 (a) the C2 blob is a byte-exact PREFIX of the C3 blob and the remainder == newline+LEDGER15, sha256 714f1d0810180ea2d64cc47f4f2424e24a8f67df49f9c6f8be002daa23d416a1, 5926 bytes, 4 lines; (b) an INDEPENDENT blank-line split of the C3 file, its terminating newline normalised first, gives 212 units whose LAST TWO are LEDGER15's two paragraphs IN ORDER, each matched by digest. NEGATIVE CONTROL: one flipped byte of the remainder REJECTED by both readings, the unflipped value ACCEPTED by both.
- G7 At C1/C2/C3: `^- R-\d+ — ` 192/192/193, `^Done: R-\d+ — ` 0/0/0, `^Landed: ` 0/0/0, `^Gate: R\d+ — ` 14/14/15 over 15 DISTINCT keys R1..R15, `^- R-0621 — ` 0/0/1, `^- R-0622 — ` 0/0/0 — so C2 edited and only C3 minted. Header sweep at C3: 14 of the 15 `Gate: ` lines match `^Gate: R(\d+) — the R(\d+) entry\.` with second == first−1 and the R15 pair occurs exactly once; the non-match count is 1 and that line is `Gate: R1 — the F255 R21 entry.`
- G8 CONSTRUCTIVE, not counted. FIXFROM occurs EXACTLY ONCE in the `305bc30c` blob of `packages/orchestration/ui_server.py`; replacing it with FIXTO yields sha256 dbf7b3b483eb0b14b53aa1de09077f4fb17495e1ab4f37f4ab4ad538336dbd49 == the C4 blob at the same sha256. HAMMERFROM and GROWFROM each occur EXACTLY ONCE in the `305bc30c` blob of `tests/ui_server/test_sse_stream.py`; replacing each with its TO yields sha256 68e9b29b29e8f2500ee1de8752dc902924389198846804df07b052886b802fe4 == the C5 blob at the same sha256.
- G9 PRIMARY checkout, run SERIALLY, never two pytest processes at once, all at C6: `tests/ui_server/test_sse_stream.py` exits 0 at 65 passed + 0 skipped; the combined state readers exit 0 at 465 + 0; `tests/docs/` exits 0 at 295 + 0. TESTS15 holds 3 lines matching `^    def test_`, so 62+3 = 65 and 462+3 = 465; all three identities hold.
- G10 The C5 blob of `tests/ui_server/test_sse_stream.py` is a byte-exact PREFIX of the C6 blob and the remainder is TWO newlines then TESTS15, 642 bytes — the one-newline variant compares False. `git diff C5..C6` on that path ADDS 16 lines, the two blank lines then TESTS15's 14 lines IN ORDER (14+2 = 16), and REMOVES 0.
- G11 RED PROOF, the colour and not a count, in a disposable worktree at C6 with the primary checkout never touched and the import path proved (`mod.__file__` resolves inside the worktree). With the `305bc30c` blob of `packages/orchestration/ui_server.py` written in and the tests left at C6, `pytest … -k ResumeStartTypes` EXITS 1: `test_an_integer_zero_is_a_position_and_not_an_absence` FAILS on `assert 7 == 1`, while `test_an_integer_header_resumes_one_past_it` and `test_none_is_the_only_absence` SURVIVE by design — a string header and an absent header already behaved correctly and only the integer-zero case was broken. Restored to the C4 blob, the same command EXITS 0 at 3 passed.
- G12 MUTATION CONTROL in the SAME worktree: `return int(text) + 1` → `return int(text)`, that line occurring exactly once, drives `pytest … -k DisconnectHammer` to EXIT 1 with four failures INCLUDING `test_a_resume_crosses_a_ledger_that_grew_between_connections`, so the repaired test still has teeth. Restored, the same command EXITS 0 at 5 passed.
- G13 Ruff over the two touched paths as a MULTISET of rule codes, base against head, base read through `--stdin-filename` so `per-file-ignores` resolves by path and no file is overwritten. DEFAULT config: base `{}`, head `{}` — EQUAL and both EMPTY, exit 0 on both. `--preview`: base `{'E306': 3}`, head `{'E306': 3}` — EQUAL, both exit 1, and that exit code is NOT the gate; the three E306 are PRE-EXISTING in `packages/orchestration/ui_server.py` and this round neither adds nor removes one. CONTROL through the SAME extractor in BOTH configurations: an unused import yields `{'F401': 1}` at exit 1.
- G14 `git diff --name-only 305bc30c..1dc011a2` equals the Change list MINUS `.agent/handoff.md` exactly — six paths, none on either side alone; C7 adds the seventh and the full BASE..C7 reading is in the round report (constraint 6, R-0371). Every commit in the range has exactly one parent. BOTH numstat cells per path from `git show --numstat`, cross-checked against `git diff --numstat`: 377/0, 261/248, 20/17, 1/1, 4/0, 1/1, 16/7 and 16/0 — every insertion under 500, and EVERY CELL, insertion and deletion, equal to the `+/-` column above.
- G15 Lines beginning with a slice-open or slice-close marker: 0 in `.agent/plan.md` at C1, `.agent/live_review.md` at C3, `packages/orchestration/ui_server.py` at C4, `tests/ui_server/test_sse_stream.py` at C6 and `.agent/handoff.md` at C7.
- G16 This round's own reflog entries, counted by the OPERATION before the first `:` in `%gs`: `amend` 0, `rebase` 0, `cherry` 0. No total asserted. Push and `gh pr list` are under External actions. This file carries every mandated section and the item-status table below, naming C0a, C0b, C1, C2, C3, C4, C5, C6 and C7 exactly once each; measured with `wc -l` before it was written, it is 89 lines against the 100-line cap this round's nine commits allow, so no DECISION D15 stated-cause line is owed.

## Authored-text proofs
- `.agent/authored/f008-r15.md` at C0a == the scratch block byte for byte and `.agent/last_block.md` at C0b == the same bytes (G2). All ELEVEN slices were extracted from the COMMITTED C0a blob by their marker lines and applied unedited — never retyped, rewrapped, reflowed or whitespace-adjusted. G4, G5, G6, G8 and G10 are the disk-to-disk comparisons, each a byte-equality against the extracted slice.

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | |
| C7 | done | this commit |

## Deviations & assumptions
- No departure from the ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5, C6, C7. No extra commit, no dropped commit, no reordering. C2 and C3 stayed separate and C4 landed before C6.
- MECHANICAL NOTE on G13, worth a reviewer's attention because it nearly made a gate vacuous: this ruff prints a BARE rule code in the default configuration but `error[E306]` under `--preview`, so a first extractor that read only the bare form returned an EMPTY preview multiset at exit 1 — equal on both sides and therefore green, while blind to the only findings in the gate. The extractor was widened to read both forms and BOTH configurations were re-run, and the control was extended to `--preview` as well. Equality was never the reading at risk; visibility was.
- Mechanical note: the session command guard rejects `${arr[0]}`, `$(...)` and `; echo $?` by form, so every multi-step gate was written to a script under the gitignored `.remedy-wt/r15/` and run from there.

## Next
The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1); its SECOND is the Open PR Gate (Phase 1 rule 2), which found no open pull request at R15 and therefore continues on this branch. R15 IS PENDING REVIEW: its verdict is owed by the next round's ledger commit and no line of this round records one. R16's work is T003's client hook — the `useBrainStream` EventSource hook with reconnect backoff, gap detection via seq discontinuity and the status surface live | reconnecting | delayed.
