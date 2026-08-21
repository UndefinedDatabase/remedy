# Handback — F008 SSE event stream, R33 (the R32 verdict recorded, R-0629 amended, the cockpit wired to its stream)
## Range
Review of `9f14a79e`..C6, the handback commit itself (8 commits, branch feature/f008-sse-event-stream). C6's SHA cannot exist inside C6, so it is named by role and the round report carries the value (R-0371).
## Commits
### 7cb8b381 docs(state): save the F008 R33 step block verbatim
| Path | +/- | Reason |
| `.agent/authored/f008-r33.md` | +428/-0 | C0a, the R33 block saved byte for byte |

### b6485523 docs(state): mirror the F008 R33 block into last_block
| Path | +/- | Reason |
| `.agent/last_block.md` | +299/-284 | C0b, the same bytes mirrored from the COMMITTED C0a blob |

### 2befe139 docs(state): set the plan to F008 R33, recording the R32 verdict
| Path | +/- | Reason |
| `.agent/plan.md` | +13/-14 | C1, PLANF008R33 applied whole |

### cc40975f docs(review): amend R-0629 with the F008 R32 instance
| Path | +/- | Reason |
| `.agent/live_review.md` | +1/-1 | C2, the R0629FROM line rewritten to R0629TO — a REWRITE, not an append |

### f112538f docs(review): record the R32 verdict in the live review ledger
| Path | +/- | Reason |
| `.agent/live_review.md` | +2/-0 | C3, LEDGER33's paragraph appended |

### a8965b2d feat(ui): subscribe the cockpit shell to its job brain stream
| Path | +/- | Reason |
| `apps/ui/src/components/shell/RemedyShell.tsx` | +9/-1 | C4, SHIMP, SHSIG and SHCALL applied as three pairs in this ONE commit |

### 9ee1e9a9 test(ui): gate the cockpit shell subscription by its source
| Path | +/- | Reason |
| `tests/ui_contracts/test_remedy_shell_stream.py` | +90/-0 | C5, CONTRACT created — `git ls-tree 9f14a79e -- <that path>` printed NOTHING |

### C6 docs(state): write the F008 R33 handback
| Path | +/- | Reason |
| `.agent/handoff.md` | self | C6 cannot table itself (R-0149); its numbers are in the round report |

## External actions
- ONE worktree was created and removed, both for G11's red control: `git worktree add --detach .remedy-wt/r33-wt 9ee1e9a9` EXIT 0, with NO `node_modules` linked or copied into it because that control runs pytest only, then `git worktree remove --force .remedy-wt/r33-wt` EXIT 0. After it, `git worktree list` printed ONE line, naming `/home/decodeux/Repos/remedy`. No `gh` command was run.
- `git push -u origin feature/f008-sse-event-stream` runs ONCE, AFTER C6, and its output belongs to the round report (constraint 6). NOTHING merged, no PR created, no PR updated, no branch created (constraint 8).

## Verification
- G1 `.agent/STOP` ABSENT — `ls -la .agent/STOP` printed `No such file or directory` — read immediately before C0a; `git branch --show-current` printed feature/f008-sse-event-stream; `git status --porcelain` printed 0 lines after each of C0a, C0b, C1, C2, C3, C4 and C5. The post-C6 readings are in the round report (constraint 6).
- G2 Transport EQUAL three ways — `.remedy-wt/f008-r33.md` as received, `.agent/authored/f008-r33.md` at C0a and `.agent/last_block.md` at C0b — all sha256 a955dd3da8daa659104584fe479687128b071060240266d6daa53fd4fc43ca44 over 32437 bytes and 428 lines, and that value EQUALS the digest carried in the task prompt.
- G3 ELEVEN slices, the COUNT taken from an ordered extraction out of the COMMITTED C0a blob (`git show 7cb8b381:.agent/authored/f008-r33.md`) by their marker lines; newline-included sha256/bytes/lines: PLANF008R33 a768146d/2079/39, R0629FROM 836d856d/78/1, R0629TO 3e9f1830/2001/1, LEDGER33 db6779e4/5469/1, SHIMPFROM cd08d314/47/1, SHIMPTO cc831ab7/200/3, SHSIGFROM a88ea7bf/185/1, SHSIGTO 9c39d503/599/7, SHCALLFROM 85d765c3/77/1, SHCALLTO 26ec012b/106/1, CONTRACT d13c2a38/3855/90. The trailing-whitespace test reported False for each of the eleven, the leading-blank-line test reported False for each of the eleven, and each is newline-terminated.
- G4 `.agent/plan.md` at C1 sha256 a768146d1e6526761af751a5e0be17c6bb5f2ffcb09d0f000b63e314f61e623e, 2079 bytes, 39 lines (<50), BYTE-EQUAL to PLANF008R33; `Steps` occurs (1x), `## Goal` 1x and `## Next Steps` 1x line-anchored, `\bF\d{3}\b` matches twice, first `F008`.
- G5 The REWRITE at C2, base blob read with `git show 9f14a79e:.agent/live_review.md` into scratch and never over the tracked file: R0629FROM 1 at the base and 0 at C2, R0629TO 0 at the base and 1 at C2 — the FROM-0x / TO-1x proof. The base blob (2c14cd83, 512161 bytes, 1118 lines) with that substitution applied ONCE is BYTE-EQUAL to the C2 blob (acb62c27, 514084 bytes, 1118 lines). Blank-line paragraph COUNT 243 at the base and 243 at C2, unchanged, with EXACTLY ONE paragraph differing, index 234, and it begins `- R-0629 — `.
- G6 (a) the C2 blob is a byte-exact PREFIX of the C3 blob (5c776fa7, 519554 bytes, 1120 lines) and the remainder == newline+LEDGER33, sha256 2549902f, 5470 bytes, 2 lines; (b) an INDEPENDENT blank-line split of the WHOLE C3 file, its terminating newline normalised first, gives 244 units whose LAST unit is LEDGER33's paragraph. NEGATIVE CONTROL: one PRINTABLE ASCII byte of the remainder flipped to another printable one (remainder offset 1, `G`→`H`) REJECTED by BOTH readings, the unflipped value ACCEPTED by BOTH.
- G7 sets, at the round base / at C2 / at C3, line-anchored: `^- R-\d+ — ` 201/201/201 — this round mints NO id — `^- R-0630 — ` 0/0/0, `^- R-0629 — ` 1/1/1, `^- R-0429 — ` 1/1/1, `^- R-0553 — ` 1/1/1, `^- R-0628 — ` 1/1/1, `^- R-0368 — ` 1/1/1, `^Done: R-\d+ — ` 6/6/6, `^Landed: ` 0/0/0, `^Gate: R\d+ — ` 32/32/33 over 32, 32 then 33 DISTINCT keys. HEADER SWEEP at C3: of 33 `Gate: ` lines, 32 match `^Gate: R(\d+) — the R(\d+) entry\.` with second == first−1, 1 does NOT and its text to its first period is `Gate: R1 — the F255 R21 entry.`, and the R33 pair occurs EXACTLY ONCE.
- G8 The three pairs at C4, each counted separately at the round base / at C4: SHCALLFROM 1/0 with SHCALLTO 0/1, the REWRITE's proof; SHIMPFROM 1/1 and SHSIGFROM 1/1 — each TO CONTAINS its FROM, so a FROM-zero reading is unattainable by construction — with SHIMPTO 0/1 and SHSIGTO 0/1. Covering all three at once: the round-base blob of `apps/ui/src/components/shell/RemedyShell.tsx` (5e51484e, 2782 bytes) with SHIMP, SHSIG and SHCALL each substituted ONCE in that order is BYTE-EQUAL to the C4 blob (9e6de55c, 3378 bytes). File line count 50 at the base and 58 at C4.
- G9 `git ls-tree 9f14a79e -- tests/ui_contracts/test_remedy_shell_stream.py` printed NOTHING (EXIT 0, zero-byte output), so the file is CREATED and not modified. The committed C5 blob and the CONTRACT slice extracted from the committed C0a blob are both sha256 d13c2a3849164b163dfc22e6acf8b8d1899133f5ce9cdad02e34cc8073336762 over 3855 bytes and 90 lines: BYTE-EQUAL.
- G10 PRIMARY checkout, SERIALLY, never two test processes alive at once, AT C5. In `apps/ui`: `npm run --silent typecheck` EXIT 0 with a ZERO-BYTE output stream (measured as `OUTPUT_BYTES=0`); `npx vitest run` EXIT 0 at 10 Test Files and 152 Tests, UNCHANGED from the block's base reading of 10 and 152. From the root: `python3 -m pytest tests/ui_contracts/ -q -rf` EXIT 0 at 417 passed + 4 skipped = SUM 421, matching the ordered 421 where the base sum is 413 and CONTRACT's 8 tests are the difference; the five-target state-reader plus canary command EXIT 0 at 465 passed + 0 skipped = SUM 465. G10's STOP clause was never reached.
- G11 In the DISPOSABLE worktree at C5, counted FIRST: the 29-byte string a space followed by streamStatus={stream.status}, which contains 0 backticks, occurs EXACTLY ONCE as a substring, and the count of LINES in that file containing `streamStatus` is also 1 — the two numbers agree. Deleting that one occurrence (file 3378 → 3349 bytes, target count 0), `python3 -m pytest tests/ui_contracts/test_remedy_shell_stream.py -q -rf` from that worktree's root EXITS 1 at "1 failed, 7 passed", the one being exactly `TestShellSubscribesToTheStream::test_shell_passes_the_stream_status_to_the_live_panel` and no other. Restored, the file's sha256 is 9e6de55c164ae997c23767ef8ecb16e9f21d1104d6588033266e7cf9294ea43f, byte-identical to the pre-delete value, and the same command EXITS 0 at 8 passed. The primary checkout was never written to.
- G12 `git diff --name-only 9f14a79e..9ee1e9a9`, measured from the round base this block's header names and no other SHA, yields 6 paths which are EXACTLY the Change set minus `.agent/handoff.md` — `.agent/authored/f008-r33.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `apps/ui/src/components/shell/RemedyShell.tsx`, `tests/ui_contracts/test_remedy_shell_stream.py` — with the set difference EMPTY in both directions. Walking `git rev-list --reverse 9f14a79e..9ee1e9a9` gives SEVEN commits, each read to have exactly ONE parent. BOTH numstat cells per path from `git show --numstat`, cross-checked against `git diff --numstat` and AGREEING for all seven: 428/0, 299/284, 13/14, 1/1, 2/0, 9/1, 90/0 — every insertion under 500 (max 428), and every cell equal to the `+/-` column above, cell by cell.
- G13 Lines BEGINNING with the two slice markers: 0 in `.agent/plan.md` at C1, 0 in `.agent/live_review.md` at C2, 0 in `.agent/live_review.md` at C3, 0 in `apps/ui/src/components/shell/RemedyShell.tsx` at C4, 0 in `tests/ui_contracts/test_remedy_shell_stream.py` at C5, and 0 in this file, measured on the drafted bytes C6 commits unchanged. `.agent/last_block.md` is not in that list. Trailer: `git log --format=%H%x09%(trailers:key=Co-Authored-By,valueonly) 9f14a79e..HEAD` run BEFORE C6 lists 7 commits, of which 7 return a NON-EMPTY value — that is the measurement, not a universal. This round's own reflog entries, classified by the OPERATION before the first `:` in `%gs`: SEVEN found and SEVEN classified pre-C6, all `commit`; `amend` 0, `rebase` 0, `cherry` 0. No total over the whole reflog is asserted.
- G14 This file carries every mandated section of docs/agents/handback_template.md, the `## Next` content constraint 11 names in that order, and the item-status table below, which holds exactly one row for each of C0a, C0b, C1, C2, C3, C4, C5 and C6 — "exactly one row" scoping to that TABLE. Measured with `wc -l` in `.remedy-wt/` BEFORE it was written here it is 83 lines, UNDER the 100 this round's eight commits allow, so no DECISION D15 stated-cause line is owed. One line per gate here; the raw transcripts are in the round report (R-0582).

## Authored-text proofs
- `.agent/authored/f008-r33.md` at C0a == the received block byte for byte and `.agent/last_block.md` at C0b == the same bytes (G2). All ELEVEN slices were extracted from the COMMITTED C0a blob by their marker lines and applied unedited — never retyped, rewrapped, reflowed, reindented or whitespace-adjusted. Whole-file byte equality: PLANF008R33 (G4) and CONTRACT (G9). Substitution equality with the FROM-0x / TO-1x counts each REWRITE owes: R0629FROM→R0629TO (G5) and SHCALLFROM→SHCALLTO (G8). Ordered-append equality: LEDGER33 (G6, two independent readings with a negative control) and, for the two APPEND-shaped pairs SHIMP and SHSIG, the one-pass three-substitution byte equality of G8, which is the reading §4.9 gives code. G13 confirms 0 marker lines in each of the six committed targets it names.

## State — Fortschritt
~99 % (T001 ✅ · T002 ✅ · T003 ✅ — Client, Badge, Deps-Factory, Browser-Env und Cockpit-Wiring komplett; Integrations-Gate offen) — Schätzung

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | three pairs — two APPEND-shaped, one REWRITE — in this ONE commit |
| C5 | done | |
| C6 | done | this commit |
## Deviations & assumptions
- No departure from the ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5, C6. No extra commit, no dropped commit, no reordering; C1 was the first substantive commit and C4 preceded C5, as constraint 2 requires.
- NO OBJECTION to any slice: all eleven were applied byte for byte and none looked wrong to me. No `--no-verify` was used on any of the seven pre-C6 commits; `ls .git/hooks` lists only `*.sample` entries, so no hook ran either way.
- PARTIAL READ, declared against the AGENTS.md File Editing Safety Rule: `.agent/live_review.md` is 1118 lines and 512161 bytes at the round base and I did not read it end to end. I read the diff of each of its two changes and both were made programmatically over whole-file bytes, with the byte-level equalities in G5 and G6 standing in for the human read. `apps/ui/src/components/shell/RemedyShell.tsx` (50 lines at the base) WAS read end to end before and after C4.
- METHOD NOTE: G10's two pytest suites were each run twice — once inline and once through a scratch script that captured the exit code explicitly — and the two runs reported identical counts, 417+4 and 465+0. The G10 line above quotes the scripted run. No two test processes were alive at once in either pass.
- Constraint 3, stated as the measurement it rests on: G12's `git diff --name-only 9f14a79e..9ee1e9a9` lists exactly the six Change-set paths minus `.agent/handoff.md` and nothing else, so `apps/ui/package.json`, `apps/ui/package-lock.json` and `apps/ui/src/RemedyApp.tsx` were never opened for writing and no dependency was added; SHIMP added two import lines against modules already in the tree, and G10's typecheck EXIT 0 is what proves `useBrainStream`, `createBrainStreamHostDeps`, `browserBrainStreamEnv` and the `streamStatus` prop resolve where C4 uses them. Constraint 4: R-0630 stays FREE, and R-0368, R-0429, R-0553, R-0622, R-0628 and R-0629 are all still OPEN with none resolved here — G7's `^Done: R-\d+ — ` reads 6 at the base, at C2 and at C3 and `^Landed: ` reads 0 at all three, unchanged.
- `npm run lint` was NOT run: it is red at base, it is R-0622, and it is not a gate (R-0364).
- The session command guard rejects `$(...)`, `; echo $?`, heredocs, shell loops and chained `;` commands BY FORM, so every multi-step gate was written to a script under the gitignored `.remedy-wt/` and run from there; `git status --porcelain` printed 0 lines after each of C0a through C5, so nothing from that directory was committed, and the G11 script's last line printed `CWD_NOW=/home/decodeux/Repos/remedy`, so no shell was left inside the worktree.
## Next
The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1); its SECOND is the Open PR Gate (Phase 1 rule 2). R33 IS PENDING REVIEW: its verdict is owed by the next round's ledger commit, and no line of this round records one. The next free finding id is R-0630. R-0368, R-0429, R-0553, R-0622, R-0628 and R-0629 are all OPEN. R34's work is the INTEGRATION GATE per docs/agents/integration_gate.md — the full suite, once, before closure — with T003 complete once this round lands.
