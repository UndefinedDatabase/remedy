# Handback — F008 SSE event stream, R13 (T002 Last-Event-ID resume)

## Range
Review of `a76ea1e7`..`HEAD` (branch feature/f008-sse-event-stream, 8 commits).

## Commits

### 7fc5046d chore(authored): save the F008 R13 step block
| Path | +/- | Reason |
| `.agent/authored/f008-r13.md` | +458/-0 | C0a, the block saved verbatim |

### 13ac3e84 chore(state): mirror the F008 R13 step block
| Path | +/- | Reason |
| `.agent/last_block.md` | +387/-123 | C0b, same bytes mirrored |

### 390d6d10 chore(plan): advance the plan to F008 R13
| Path | +/- | Reason |
| `.agent/plan.md` | +17/-17 | C1, PLANF008R13 applied whole |

### 540bd0d3 docs(review): register R-0619 and record the R12 verdict
| Path | +/- | Reason |
| `.agent/live_review.md` | +4/-0 | C2, LEDGER13 appended |

### 2d33fee5 test(ui-server): give the socketless handlers a headers attribute
| Path | +/- | Reason |
| `tests/ui_server/test_sse_stream.py` | +6/-1 | C3, HELPERFROM→TO and RAISEFROM→TO |

### 245d8651 feat(ui-server): resolve the SSE resume position from header or cursor
| Path | +/- | Reason |
| `packages/orchestration/ui_server.py` | +32/-1 | C4, RESOLVEFROM→TO and ROUTEFROM→TO |

### b5501c79 test(ui-server): pin the Last-Event-ID resume decision
| Path | +/- | Reason |
| `tests/ui_server/test_sse_stream.py` | +90/-0 | C5, TESTS13 appended |

### C6 docs(state): write the F008 R13 handback
| Path | +/- | Reason |
| `.agent/handoff.md` | self | C6 cannot table itself (R-0149); numbers in the round report |

## External actions
- `git worktree add --detach .remedy-wt/r13-red b5501c79` — ok; `git worktree remove --force .remedy-wt/r13-red` + `git worktree prune` — ok, before this file was written.
- `git push` — reported in the round report; re-run after C6.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — `[]`. No merge, no PR created, no branch created.

## Verification
- G1 STOP absent, read immediately before C0a; branch feature/f008-sse-event-stream; `git status --porcelain` empty after every one of the seven commits and now; `git worktree list` names the primary checkout alone.
- G2 Transport EQUAL three ways — the scratch block, `.agent/authored/f008-r13.md` at C0a and `.agent/last_block.md` at C0b — sha256 4aaaafb36a773dbf9a4e9fd24772602d45e039e41566144c413d12a032d07415, 30793 bytes, 458 lines.
- G3 ELEVEN slices by ordered extraction from the committed C0a blob, newline-included, as sha256/bytes/lines: PLANF008R13 8d41b66d/2466/45, LEDGER13 51cf1279/5628/3, RESOLVEFROM 62776105/183/5, RESOLVETO 97981379/1317/29, ROUTEFROM 897b674c/142/3, ROUTETO e8297527/526/10, HELPERFROM 1ea7c575/378/7, HELPERTO 134bca15/591/11, RAISEFROM f46d77d3/154/3, RAISETO 6e50d886/183/4, TESTS13 8766b87d/3919/88.
- G4 `.agent/plan.md` at C1 sha256 8d41b66d…, 2466 bytes, 45 lines (<50), BYTE-EQUAL to PLANF008R13; `## Goal` 1x, `## Next Steps` 1x line-anchored, `F008` 2x.
- G5 (a) the C1 blob is a byte-exact PREFIX of the C2 blob and the remainder == newline+LEDGER13, sha256 171854d4…, 5629 bytes, 4 lines; (b) an INDEPENDENT blank-line split of the C2 file gives 208 units whose LAST TWO are LEDGER13's two paragraphs in order. Negative control: one flipped byte REJECTED by both readings, the unflipped value ACCEPTED by both.
- G6 C1→C2: `^- R-\d+ — ` 190→191, `^Done: R-\d+ — ` 0→0, `^Landed: ` 0→0, `^Gate: R\d+ — ` 12→13 over 13 DISTINCT keys R1..R13; `^- R-0619 — ` 0→1, `^- R-0620 — ` 0→0. Header sweep: 12 of the 13 `Gate:` lines match `^Gate: R(\d+) — the R(\d+) entry\.` with second == first−1, the R13 pair exactly once; the non-match count is 1 and that line is `Gate: R1 — the F255 R21 entry.`, which has no F008 predecessor.
- G7 CONSTRUCTIVE: in the `a76ea1e7` blob of `packages/orchestration/ui_server.py` RESOLVEFROM and ROUTEFROM each occur EXACTLY ONCE; replacing each with its TO yields sha256 b5149772…, byte-equal to the C4 blob at sha256 b5149772…. Base blob sha256 ba5672b2….
- G8 Same for the test file: HELPERFROM and RAISEFROM each occur EXACTLY ONCE in the `a76ea1e7` blob and the reconstruction is sha256 1c748bc7…, byte-equal to the C3 blob. The C3 blob is a byte-exact PREFIX of the C5 blob whose remainder is TWO newlines then TESTS13 (3921 bytes). `git diff C3..C5` on that path ADDS 90 lines — the two blank lines then TESTS13's 88 lines IN ORDER, 88+2 — and REMOVES 0.
- G9 PRIMARY checkout, run SERIALLY, never two pytest processes at once, all at C5: the SSE file exits 0 at 57 passed + 0 skipped; the state readers exit 0 at 457 + 0; `tests/docs/` exits 0 at 295 + 0. TESTS13 holds 17 lines matching `^    def test_`, so 40+17 = 57 and 440+17 = 457; all three identities hold.
- G10 RED PROOF in a disposable worktree at `.remedy-wt/r13-red`, the primary checkout untouched: with `packages/orchestration/ui_server.py` alone written back to its `a76ea1e7` blob the SSE file EXITS 1 with 15 failing tests, among them `TestResumeStart::test_a_last_event_id_resumes_one_past_the_event_it_names` and `TestResumeRoute::test_the_header_reaches_the_writer_as_the_next_position`; restored to its C4 blob the same command EXITS 0. 42 tests survive the revert by design — the query-cursor fallbacks the old route already served.
- G11 Ruff as a MULTISET of rule codes over the two touched paths: HEAD at C5 `{}` at exit 0, base `a76ea1e7` `{}` at exit 0 per path through `--stdin-filename` so `per-file-ignores` still resolves and no file is overwritten. EQUAL and both EMPTY. CONTROL through the SAME extractor: an unused import yields `{'F401': 1}` at exit 1.
- G12 `git diff --name-only a76ea1e7..b5501c79` gives exactly the six non-handoff paths of the Change list with no path on either side alone; C6 adds the seventh, `.agent/handoff.md`, and the BASE..C6 reading is in the round report (R-0149). Every commit BASE..C5 has exactly one parent. BOTH numstat cells per path, from `git show --numstat`: 458/0, 387/123, 17/17, 4/0, 6/1, 32/1, 90/0 — every insertion under 500 and EVERY CELL, insertion and deletion, equal to the `+/-` column above, both sides read from git's numstat and never from file line counts.
- G13 Lines beginning `<<<SLICE ` or `<<<END `: 0 in `.agent/plan.md` at C1, `.agent/live_review.md` at C2, `tests/ui_server/test_sse_stream.py` at C5, `packages/orchestration/ui_server.py` at C4 and `.agent/handoff.md` at C6.
- G14 This round's own reflog entries, counted by the OPERATION before the first `:` in `%gs`: `amend` 0, `rebase` 0, `cherry` 0. No total asserted.
- G15 Branch pushed; `gh pr list --state open --json number,headRefName,baseRefName,isDraft` returns `[]`. Nothing merged, no PR opened, no branch created.
- G16 This file carries every mandated section and the item-status table below, naming C0a, C0b, C1, C2, C3, C4, C5 and C6 exactly once each; it is 84 lines against the 100-line cap this round's eight commits allow, so no DECISION D15 stated-cause line is owed.

## Authored-text proofs
- `.agent/authored/f008-r13.md` at C0a == the scratch block byte for byte and `.agent/last_block.md` at C0b == the same bytes (G2). All eleven slices were extracted from the COMMITTED C0a blob by their marker lines and applied unedited; G4, G5, G7 and G8 are the disk-to-disk comparisons, each a byte-equality against the extracted slice.

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
| C6 | done | this commit |

## Deviations & assumptions
- No departure from the ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5, C6. No extra commit, no dropped commit, no reordering.
- OBJECTION to RESOLVETO, raised not acted on, the slice applied byte for byte: `resolve_sse_start` guards with `str(last_event_id or "")`, so an integer `0` — admitted by the `Any` annotation — is falsy and falls back to the cursor, which contradicts the docstring's and TESTS13's claim that "the first event is 0; a truthiness test here would resume at 0 and replay it for ever". The tests pass the STRING `"0"`, which is truthy, so the suite is green and the HTTP path (headers are always strings) is correct; the defect is latent and only reachable by a non-string caller.
- Assumption, stated: G12 orders `git diff --name-only BASE..C6`, a value that cannot exist while C6 is being written; the pre-C6 reading is above and the full BASE..C6 reading is in the round report.

## Next
The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1); its SECOND is the Open PR Gate (Phase 1 rule 2), which finds no open pull request and therefore continues on this branch at R14, whose work is T002's forced-disconnect hammer — kill the connection mid-stream N times and require the client transcript to byte-equal the ledger's envelope sequence.
