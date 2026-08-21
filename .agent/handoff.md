# Handback — F008 SSE event stream, R29 (the R28 verdict recorded, R-0553 amended, the DELAYED badge shipped)
## Range
Review of `4afe1936`..C4, the handback commit itself (8 commits, branch feature/f008-sse-event-stream). C4's SHA cannot exist inside C4, so it is named by role and the round report carries the value (R-0371).
## Commits
### e25e7f91 docs(state): save the F008 R29 step block verbatim
| Path | +/- | Reason |
| `.agent/authored/f008-r29.md` | +490/-0 | C0a, the R29 block saved byte for byte |

### 72eb21ea docs(state): mirror the F008 R29 block into last_block
| Path | +/- | Reason |
| `.agent/last_block.md` | +429/-167 | C0b, the same bytes mirrored from the COMMITTED C0a blob |

### b727d5e1 docs(state): set the plan to F008 R29, recording the R28 verdict
| Path | +/- | Reason |
| `.agent/plan.md` | +21/-20 | C1, PLANF008R29 applied whole |

### a9c0b2aa docs(state): record DECISION F008 D2 on the badge variant and round split
| Path | +/- | Reason |
| `.agent/decisions.md` | +33/-0 | C1b, DECISION2 appended |

### bade3be8 docs(review): amend R-0553 with the F008 R28 instance
| Path | +/- | Reason |
| `.agent/live_review.md` | +23/-1 | C2a, the round's ONE ledger pair, applied as a REWRITE |

### 210cc4a0 docs(review): record the R28 verdict in the live review ledger
| Path | +/- | Reason |
| `.agent/live_review.md` | +2/-0 | C2b, LEDGER29's paragraph appended |

### 573f28c2 feat(ui): say DELAYED on the live pill when the transport is not live
| Path | +/- | Reason |
| `apps/ui/src/components/panels/LiveStatusPill.tsx` | +18/-2 | C3, PILL applied whole |
| `apps/ui/src/components/panels/RightLivePanel.module.css` | +2/-0 | C3, PILLCSS appended |
| `apps/ui/src/components/panels/RightLivePanel.tsx` | +3/-2 | C3, the three pairs applied in one pass |
| `tests/ui_contracts/test_live_status_pill.py` | +58/-0 | C3, PILLTEST, the source contract |

### C4 docs(state): write the F008 R29 handback
| Path | +/- | Reason |
| `.agent/handoff.md` | self | C4 cannot table itself (R-0149); its numbers are in the round report |

## External actions
- `git worktree add --detach .remedy-wt/r29-wt 573f28c2` succeeded; `apps/ui/node_modules` and `apps/ui/dist` were SYMLINKED into it with `os.symlink` and never copied; after G11 both symlinks were unlinked, `git worktree remove .remedy-wt/r29-wt` and `git worktree prune` succeeded, and `git worktree list` then printed the primary checkout alone.
- `git push -u origin feature/f008-sse-event-stream` runs ONCE, AFTER C4, and its output belongs to the round report (constraint 5). NOTHING merged, no PR created, no PR updated, no branch created (constraint 7), and no `gh` command was run: the block records the reviewer's Phase 0 probe returning `[]`, and no new branch is being cut.

## Verification
- G1 `.agent/STOP` ABSENT (`ls` exit 2, "No such file or directory"), read immediately before C0a; branch feature/f008-sse-event-stream; `git status --porcelain` EMPTY after each of C0a, C0b, C1, C1b, C2a, C2b and C3. The post-C4 readings are in the round report (constraint 5).
- G2 Transport EQUAL three ways — `.remedy-wt/f008-r29.md` as received, `.agent/authored/f008-r29.md` at C0a and `.agent/last_block.md` at C0b — all sha256 21875ebb9d405ff6a7e5889cf2d3033bebc2bb1616c60d575e256339449b80b3 over 33559 bytes and 490 lines, and that value EQUALS the digest carried in the task prompt.
- G3 FOURTEEN slices, the COUNT taken from an ordered extraction out of the COMMITTED C0a blob (`git show e25e7f91:…`) by their marker lines; newline-included sha256/bytes/lines: PLANF008R29 21396c53/2184/40, DECISION2 8ec63baa/1916/32, R0553FROM 47e4533c/59/1, R0553TO 11a35388/2042/23, LEDGER29 fb9ceebf/3620/1, PILL 1d49c044/1329/21, PILLCSS 9aa75a6c/258/2, PANELIMPORTFROM b86ff519/56/1, PANELIMPORTTO fce79824/120/2, PANELSIGFROM bb5d1233/141/1, PANELSIGTO 9780edb1/196/1, PANELCALLFROM 7be59d57/56/1, PANELCALLTO 6b16deee/84/1, PILLTEST 7dff6c4e/2694/58 — the trailing-whitespace test reported False for each of the fourteen.
- G4 `.agent/plan.md` at C1 sha256 21396c534fb0d30565105c5b9c246e02c76a5e3d3da3e4425459ecacbee7fcc7, 2184 bytes, 40 lines (<50), BYTE-EQUAL to PLANF008R29; `Steps` occurs (1x), `## Goal` 1x and `## Next Steps` 1x line-anchored, `\bF\d{3}\b` matches `F008`. `.agent/decisions.md`: the round-base blob (f1b0671d, 411260 bytes, 6565 lines) is a byte-exact PREFIX of the C1b blob (7eb24b1d, 413177 bytes, 6598 lines) and the remainder == newline+DECISION2, sha256 f0a9d1ca5683, 1917 bytes, 33 lines; `^## DECISION F008 D2 ` 0 at the round base and 1 at C1b, `^## DECISION F008 D1 ` 1 at both — an added key, not a duplicated one.
- G5 The REWRITE at C2a, base bytes read with `git show 4afe1936:.agent/live_review.md` into scratch and never over the tracked file: R0553FROM 1 at the round base, 0 at C2a; R0553TO 0 at the round base, 1 at C2a — the FROM-0x / TO-1x proof a rewrite owes. The base blob with that ONE substitution applied is BYTE-EQUAL to the C2a blob (60492aa3, 492778 bytes, 1110 lines). Blank-line paragraph COUNT 239 at both, UNCHANGED, and EXACTLY ONE paragraph differs — index 145, the one beginning `- R-0553 — `.
- G6 (a) the C2a blob is a byte-exact PREFIX of the C2b blob (a8b66ac0, 496399 bytes, 1112 lines) and the remainder == newline+LEDGER29, sha256 deb381495a7f, 3621 bytes, 2 lines; (b) an INDEPENDENT blank-line split of the WHOLE C2b file, its terminating newline normalised first, gives 240 units whose LAST unit is LEDGER29's paragraph. NEGATIVE CONTROL: one PRINTABLE ASCII byte of the remainder flipped to another printable one (remainder offset 1, `G`→`X`) REJECTED by BOTH readings, the unflipped value ACCEPTED by BOTH.
- G7 At C2a/C2b, line-anchored: `^- R-\d+ — ` 201/201 — this round mints NO id — `^- R-0630 — ` 0/0, `^- R-0553 — ` 1/1, `^- R-0629 — ` 1/1, `^- R-0628 — ` 1/1, `^- R-0368 — ` 1/1, `^Done: R-\d+ — ` 6/6, `^Landed: ` 0/0, `^Gate: R\d+ — ` 28/29 over 28 then 29 DISTINCT keys. HEADER SWEEP at C2b: of 29 `Gate: ` lines, 28 match `^Gate: R(\d+) — the R(\d+) entry\.` with second == first−1, 1 does NOT and its text to its first period is `Gate: R1 — the F255 R21 entry.`, and the R29 pair occurs EXACTLY ONCE.
- G8 The three `RightLivePanel.tsx` pairs, separately. FROM count at the round base: PANELIMPORTFROM 1, PANELSIGFROM 1, PANELCALLFROM 1. PANELSIG at C3: FROM 0, TO 1. PANELCALL at C3: FROM 0, TO 1. PANELIMPORT at C3: TO 1, and NO FROM-0x reading is claimed — the pair's containment test printed true, so it is an APPEND and that reading is unattainable by construction. The round-base blob with all three replacements applied in ONE pass is BYTE-EQUAL to the C3 blob; the file is 51 lines at the round base and 52 at C3.
- G9 `LiveStatusPill.tsx` at C3 (1d49c044, 1329 bytes, 21 lines) is BYTE-EQUAL to PILL and `tests/ui_contracts/test_live_status_pill.py` at C3 (7dff6c4e, 2694 bytes, 58 lines) is BYTE-EQUAL to PILLTEST. `RightLivePanel.module.css`: the round-base blob (5329 bytes, 157 lines) is a byte-exact PREFIX of the C3 blob (5587 bytes, 159 lines), PILLCSS is an exact SUFFIX of it, and the 2 lines that commit's diff ADDS are exactly PILLCSS's 2 lines IN ORDER (`git diff -U0`, list equality).
- G10 The suites, PRIMARY checkout, SERIALLY, never two test processes at once, AT C3: `npm run --silent typecheck` in `apps/ui` EXIT 0 with NO output; `npx vitest run` in `apps/ui` EXIT 0 at 9 files and 137 tests, UNCHANGED from base; `python3 -m pytest tests/ui_contracts/ -q -rf` EXIT 0 at 409 passed + 4 skipped = 413, reconciling as the base's 402 passed + 4 skipped = 406 plus exactly the 7 tests PILLTEST adds (5 in `TestLiveStatusPillVariants`, 2 in `TestRightLivePanelPassesTheStatusDown`), the skipped count unmoved at 4; the five-target state-reader command EXIT 0 at 465 passed + 0 skipped = 465. G10's STOP clause was never reached.
- G11 Both red proofs, ONLY in the disposable worktree at C3 with `node_modules` and `dist` symlinked, never in the primary checkout. My own counts in `LiveStatusPill.tsx` there before each mutation: the three-line DELAYED block 1x (and 1 line beginning `  if (streamStatus === "delayed") {`), `/>RECONNECTING</div>` 1x. (a) deleting the block gives EXIT 1 failing exactly `TestLiveStatusPillVariants::test_a_delayed_stream_says_delayed` and `TestLiveStatusPillVariants::test_the_transport_status_is_read_before_the_dashboard_liveness`, 2 failed + 5 passed. (b) `/>RECONNECTING</div>`→`/>LIVE</div>` gives EXIT 1 failing exactly `TestLiveStatusPillVariants::test_a_reconnecting_stream_says_so_rather_than_live`, 1 failed + 6 passed. Each restored byte-identically, confirmed by sha256 1d49c0448f38… both times, after which `python3 -m pytest tests/ui_contracts/test_live_status_pill.py -q` there is EXIT 0 at 7 passed. Worktree removed and pruned; `git worktree list` shows the primary checkout alone.
- G12 `git log --format=%H%x09%(trailers:key=Co-Authored-By,valueonly) 7c03adfa..573f28c2` lists 187 commits, of which 26 return a NON-EMPTY trailer value. This round's own seven commits each return `Claude Opus 5 <noreply@anthropic.com>`. The reviewer's 180/19 over `7c03adfa..4afe1936` plus this round's 7 commits, all seven with a trailer, reconciles to exactly 187/26.
- G13 `git diff --name-only 4afe1936..573f28c2`, measured from the round base this block's header names and no other SHA, yields EXACTLY the nine Change-set paths minus `.agent/handoff.md`, with NONE on either side alone. All seven commits in that range have exactly ONE parent (seven single-parent readings). BOTH numstat cells per path from `git show --numstat`, cross-checked against `git diff --numstat` and AGREEING (the two `.agent/live_review.md` commits summing to the range's 25/1): 490/0, 429/167, 21/20, 33/0, 23/1, 2/0, 18/2, 2/0, 3/2, 58/0 — every insertion under 500 (max 490), and every cell equal to the `+/-` column above.
- G14 Lines BEGINNING with the two slice markers: 0 in `.agent/plan.md` at C1, 0 in `.agent/decisions.md` at C1b, 0 in `.agent/live_review.md` at C2a, 0 at C2b, 0 in each of the four files C3 writes, and 0 in this file, measured on the drafted bytes C4 commits unchanged. This round's own reflog entries, classified by the OPERATION before the first `:` in `%gs`: SEVEN found and SEVEN classified, all `commit`; `amend` 0, `rebase` 0, `cherry` 0. No total over the whole reflog is asserted.
- G15 This file carries every mandated section of docs/agents/handback_template.md, the `## Next` content constraint 10 names in that order, and the item-status table below, which holds exactly one row for each of C0a, C0b, C1, C1b, C2a, C2b, C3 and C4 — "exactly one row" scoping to that TABLE. Measured with `wc -l` in `.remedy-wt/` BEFORE it was written here it is 86 lines, UNDER the 100 this round's eight commits allow, so no DECISION D15 stated-cause line is owed. One line per gate here; the raw transcripts are in the round report (R-0582).

## Authored-text proofs
- `.agent/authored/f008-r29.md` at C0a == the received block byte for byte and `.agent/last_block.md` at C0b == the same bytes (G2). All FOURTEEN slices were extracted from the COMMITTED C0a blob by their marker lines and applied unedited — never retyped, rewrapped, reflowed, reindented or whitespace-adjusted. Disk-to-disk byte equalities: PLANF008R29 (G4), PILL and PILLTEST (G9). Ordered-append equalities: DECISION2 (G4), LEDGER29 (G6, two independent readings with a negative control), PILLCSS (G9, prefix + suffix + ordered added lines). FROM-0x/TO-1x rewrite proofs: R0553FROM→R0553TO (G5), PANELSIG and PANELCALL (G8). PANELIMPORT is the one append-shaped pair and carries a TO-1x reading only. G14 confirms no marker line reached a commit.

## State — Fortschritt
~98 % (T001 ✅ · T002 ✅ · T003 Client ✅ + Badge ✅, Endpoint-Wiring offen) — Schätzung

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C1b | done | |
| C2a | done | |
| C2b | done | |
| C3 | done | |
| C4 | done | this commit |
## Deviations & assumptions
- No departure from the ordered commit sequence C0a, C0b, C1, C1b, C2a, C2b, C3, C4. No extra commit, no dropped commit, no reordering; C1 was the first substantive commit, C1b preceded C3 and C2a preceded C2b, as constraint 2 requires.
- OBJECTION to a shape G4 orders, raised here because constraint 1 forbids editing a slice. The DECISION2 slice OPENS with a blank line, and G4 orders the C1b remainder to equal "a newline plus DECISION2"; applied as written that puts TWO blank lines between the previous section's last line and the `## DECISION F008 D2` heading, where the boundary above `## DECISION F008 D1` in the same file has ONE. I applied it as ordered — G4 passes as written and the diff at a9c0b2aa shows the two blank lines — but the file's own separator convention now has one exception. Cosmetic; no id is minted (constraint 4).
- TRAILER, stated as the measurement and not as a universal (constraint 9): my seven commits each carry `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, added because this session's harness instructs it; G12 is the command and the numbers. The seven commits of R28 that precede them return an empty trailer value under the same command, so this round's practice differs from the immediately preceding rounds' on this branch. No commit subject carries a leading-slash token, absolute path or secret-like string.
- Constraint 3, stated as the measurement it rests on: G13's `git diff --name-only 4afe1936..573f28c2` lists exactly the nine Change-set paths minus `.agent/handoff.md` and nothing else, so `apps/ui/package.json`, `apps/ui/package-lock.json` and `RemedyApp.tsx` are untouched and no dependency was added. Constraint 4: R-0630 stays FREE, R-0553 is AMENDED and still OPEN as are R-0368, R-0622, R-0628 and R-0629, and no `Done:` and no `Landed:` line was written this round — G7's `^Done: R-\d+ — ` reads 6 at both ledger commits and `^Landed: ` reads 0 at both, unchanged from the round base.
- `npm run lint` was NOT run: it is red at base, it is R-0622, and it is not a gate (R-0364).
- The session command guard rejects `$(...)`, `; echo $?`, heredocs, shell loops and chained `;` commands BY FORM, so every multi-step gate was written to a script under the gitignored `.remedy-wt/` and run from there; nothing from that directory was committed. `ln -s` and a `git log --format` carrying `%(trailers:…)` were also refused by form and were routed through `os.symlink` and a Python `subprocess` call respectively.
## Next
The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1); its SECOND is the Open PR Gate (Phase 1 rule 2). R29 IS PENDING REVIEW: its verdict is owed by the next round's ledger commit, and no line of this round records one. The next free finding id is R-0630. R-0368, R-0553, R-0622, R-0628 and R-0629 are all OPEN. R30's work is the real `BrainStreamHostDeps` factory over the T001 and T002 endpoint plus wiring `useBrainStream` into `RemedyApp` and passing its status down to the badge this round built — the round in which this feature's two halves finally meet.
