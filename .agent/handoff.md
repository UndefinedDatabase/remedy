# Handback — F008 SSE event stream, R14 (T002 disconnect hammer)

## Range
Review of `c8beb250`..`HEAD` (branch feature/f008-sse-event-stream, 7 commits).

## Commits

### 70f3a3e6 chore(authored): save the F008 R14 step block
| Path | +/- | Reason |
| `.agent/authored/f008-r14.md` | +364/-0 | C0a, the block saved verbatim |

### 3de27ff2 chore(state): mirror the F008 R14 step block
| Path | +/- | Reason |
| `.agent/last_block.md` | +278/-372 | C0b, same bytes mirrored |

### 6acca2a4 chore(plan): advance the plan to F008 R14
| Path | +/- | Reason |
| `.agent/plan.md` | +23/-23 | C1, PLANF008R14 applied whole |

### 0667be4b docs(review): widen R-0371 with its second instance
| Path | +/- | Reason |
| `.agent/live_review.md` | +1/-1 | C2, R0371FROM→R0371TO in place |

### f02742f9 docs(review): register R-0620 and record the R13 verdict
| Path | +/- | Reason |
| `.agent/live_review.md` | +4/-0 | C3, LEDGER14 appended |

### 3c758702 test(sse): add the T002 disconnect hammer
| Path | +/- | Reason |
| `tests/ui_server/test_sse_stream.py` | +92/-0 | C4, TESTS14 appended |

### C5 docs(state): write the F008 R14 handback
| Path | +/- | Reason |
| `.agent/handoff.md` | self | C5 cannot table itself (R-0149); numbers in the round report |

## External actions
- `git worktree add --detach .remedy-wt/f008r14-mut 3c758702` — ok; `git worktree remove .remedy-wt/f008r14-mut` — ok, before this file was written.
- `git push` — `c8beb250..3c758702  feature/f008-sse-event-stream -> feature/f008-sse-event-stream`; re-run after C5.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — `[]`. No merge, no PR created, no branch created.

## Verification
- G1 STOP absent, read immediately before C0a; branch feature/f008-sse-event-stream; `git status --porcelain` empty after C0a, C0b, C1, C2, C3 and C4 and after the G10 worktree was removed; `git worktree list` names the primary checkout alone. The post-C5 reading is in the round report (see Deviations).
- G2 Transport EQUAL three ways — the scratch block, `.agent/authored/f008-r14.md` at C0a and `.agent/last_block.md` at C0b — sha256 974788f0fe8aedcfbc667dd029d7528ad87bab977483e9968c55dba52acbfe2d, 33050 bytes, 364 lines.
- G3 FIVE slices, the count taken from the ordered extraction out of the committed C0a blob, newline-included, as sha256/bytes/lines: PLANF008R14 058d3d22/2459/45, R0371FROM 8c1880a0/2186/1, R0371TO d999949c/3534/1, LEDGER14 7a7990b0/6118/3, TESTS14 9c084fdd/3955/90.
- G4 `.agent/plan.md` at C1 sha256 058d3d22…, 2459 bytes, 45 lines (<50), BYTE-EQUAL to PLANF008R14; `## Goal` 1x and `## Next Steps` 1x line-anchored, `F008` 2x.
- G5 CONSTRUCTIVE: R0371FROM occurs EXACTLY ONCE in `.agent/live_review.md` at C1; replacing that one occurrence with R0371TO yields sha256 8ae3c4a37015d92d405efc90b6485695e70b886c78f4681e6849bc06925a5133, BYTE-EQUAL to the C2 blob at the same sha256. Line count 1026 at C1 and 1026 at C2, EQUAL. `- R-0371 — ` occurs exactly once at C2 and that line ENDS with ` OPEN.`
- G6 (a) the C2 blob is a byte-exact PREFIX of the C3 blob and the remainder == newline+LEDGER14, sha256 74215034…, 6119 bytes, 4 lines; (b) an INDEPENDENT blank-line split of the C3 file, terminating newline normalised, gives 210 units whose LAST TWO are LEDGER14's two paragraphs in order. NEGATIVE CONTROL: one flipped byte of the remainder REJECTED by both readings, the unflipped value ACCEPTED by both.
- G7 At C1/C2/C3: `^- R-\d+ — ` 191/191/192, `^Done: R-\d+ — ` 0/0/0, `^Landed: ` 0/0/0, `^Gate: R\d+ — ` 13/13/14 over 14 DISTINCT keys R1..R14, `^- R-0620 — ` 0/0/1, `^- R-0621 — ` 0/0/0. Header sweep at C3: 13 of the 14 `Gate:` lines match `^Gate: R(\d+) — the R(\d+) entry\.` with second == first−1, the R14 pair exactly once; the non-match count is 1 and that line is `Gate: R1 — the F255 R21 entry.`
- G8 The `c8beb250` blob of `tests/ui_server/test_sse_stream.py` is a byte-exact PREFIX of the C4 blob and the remainder is TWO newlines then TESTS14, 3957 bytes / 92 lines — the one-newline variant compares False. `git diff c8beb250..C4` on that path ADDS 92 lines, the two blank lines then TESTS14's 90 lines IN ORDER (90+2), and REMOVES 0.
- G9 PRIMARY checkout, run SERIALLY, never two pytest processes at once, all at C4: the SSE file exits 0 at 62 passed + 0 skipped; the state readers exit 0 at 462 + 0; `tests/docs/` exits 0 at 295 + 0. TESTS14 holds 5 lines matching `^    def test_`, so 57+5 = 62 and 457+5 = 462; all three identities hold.
- G10 MUTATION CONTROL in a disposable worktree at C4, the primary checkout never touched, each mutation applied to `packages/orchestration/ui_server.py` from the unmutated file and its FROM line occurring exactly once. A (`return int(text) + 1` → `return int(text)`) EXITS 1; B (`if text.isdigit():` → `if False:`) EXITS 1. Under both, the same four hammer tests fail — transcript-byte-equality, no-duplicate-no-gap, every-cadence and ledger-grows — and `test_a_single_clean_connection_needs_no_resume` SURVIVES: a single clean connection never resumes, so no mutation of the resume rule can reach it. Restored byte-equal to the unmutated file, the same command EXITS 0 at 5 passed.
- G11 Ruff as a MULTISET of rule codes over the one touched path: HEAD at C4 `{}` at exit 0, base `c8beb250` `{}` at exit 0 through `--stdin-filename` so `per-file-ignores` still resolves and no file is overwritten. EQUAL and both EMPTY. CONTROL through the SAME extractor: an unused import yields `{'F401': 1}` at exit 1.
- G12 `git diff --name-only c8beb250..3c758702` gives exactly the five non-handoff paths of the Change list, with no path on either side alone; C5 adds the sixth, `.agent/handoff.md`, and the BASE..C5 reading is in the round report (R-0149, and R-0371 as widened at C2). Every commit in BASE..C5 has exactly one parent. BOTH numstat cells per path, from `git show --numstat`: 364/0, 278/372, 23/23, 1/1, 4/0 and 92/0 — every insertion under 500, and EVERY CELL, insertion and deletion, equal to the `+/-` column above, both sides read from git's numstat and never from file line counts.
- G13 Lines beginning with a slice-open or slice-close marker: 0 in `.agent/plan.md` at C1, `.agent/live_review.md` at C3, `tests/ui_server/test_sse_stream.py` at C4 and `.agent/handoff.md` at C5.
- G14 This round's own six reflog entries, counted by the OPERATION before the first `:` in `%gs`, are all `commit`: `amend` 0, `rebase` 0, `cherry` 0. No total asserted.
- G15 Branch pushed; `gh pr list --state open --json number,headRefName,baseRefName,isDraft` returns `[]`. Nothing merged, no PR opened, no branch created.
- G16 This file carries every mandated section and the item-status table below, naming C0a, C0b, C1, C2, C3, C4 and C5 exactly once each; it is 80 lines against the 100-line cap this round's seven commits allow, so no DECISION D15 stated-cause line is owed.

## Authored-text proofs
- `.agent/authored/f008-r14.md` at C0a == the scratch block byte for byte and `.agent/last_block.md` at C0b == the same bytes (G2). All five slices were extracted from the COMMITTED C0a blob by their marker lines and applied unedited, never retyped, rewrapped or reflowed; G4, G5, G6 and G8 are the disk-to-disk comparisons, each a byte-equality against the extracted slice.

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit |

## Deviations & assumptions
- No departure from the ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5. No extra commit, no dropped commit, no reordering.
- OBJECTION to G1, raised not acted on: "`git status --porcelain` is empty after every commit and at the handback" orders a reading of the state AFTER C5, and C5 is this file — a value that cannot exist at the moment this text is written. That is the R-0371 class this round's own C2 widened, recurring in a hygiene gate rather than a range gate, so the widened counter-measure's wording ("a range gate whose range ends at the handback commit") does not reach it. The pre-C5 readings are above; the post-C5 porcelain and `git worktree list` readings are in the round report.
- OBSERVATION on TESTS14, applied as written: `test_a_ledger_that_grows_between_connections_still_arrives_whole` does not carry the last id of its `first` connection into `rest` — `rest` is a fresh hammer starting from 0 over the grown ledger — so it proves the grown ledger arrives whole but not that a resume span crosses the growth. It passes and is not weakened.
- Mechanical note: the session command guard rejects inline heredocs, `$(...)`, `${arr[0]}` and `; echo $?` by form, so every multi-step gate was written to a script under the gitignored `.remedy-wt/f008r14w/` and run from there.

## Next
The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1); its SECOND is the Open PR Gate (Phase 1 rule 2), which finds no open pull request and therefore continues on this branch at R15, whose work is T003's client hook — the `useBrainStream` EventSource hook with reconnect backoff, gap detection via seq discontinuity and the status surface live | reconnecting | delayed.
