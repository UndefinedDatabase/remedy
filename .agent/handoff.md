# Handback — F008 SSE event stream, R36 (THE CLOSURE COMMIT: STATUS `[x]`, README sync, candidates carrier, PULL REQUEST #209 — F008 CLOSED)
## Range
Review of `3035bc2a`..C5, the handback commit itself (7 commits, branch feature/f008-sse-event-stream). C5's SHA cannot exist inside C5, so it is named by role and the round report carries the value (R-0371).
## Commits
### ca549646 docs(state): save the F008 R36 block verbatim
| Path | +/- | Reason |
| `.agent/authored/f008-r36.md` | +490/-0 | C0a, the R36 block saved byte for byte |

### 2feb045a docs(state): mirror the F008 R36 block to last_block
| Path | +/- | Reason |
| `.agent/last_block.md` | +402/-381 | C0b, the same bytes mirrored from the COMMITTED C0a blob |

### 3d753960 docs(state): set the plan to the F008 R36 closure round
| Path | +/- | Reason |
| `.agent/plan.md` | +13/-15 | C1, PLANF008R36 applied whole |

### 65c9e315 docs(review): record the R35 verdict in the live review ledger
| Path | +/- | Reason |
| `.agent/live_review.md` | +2/-0 | C2, LEDGER36's paragraph appended |

### 7061b6bf test(docs): pin at most one claim instead of its holder
| Path | +/- | Reason |
| `tests/docs/test_docs_consistency.py` | +10/-7 | C3, PINFROM→PINTO; it lands BEFORE C4 or the docs gate goes red on the closure commit |

### e20fe420 docs(status): close F008 and sync the README capability list
| Path | +/- | Reason |
| `docs/roadmap/STATUS.md` | +1/-1 | C4, STATUSFROM→STATUSTO, the `[x]` line |
| `README.md` | +5/-2 | C4, RMCOUNT, RMTIER and RMLIST — README and STATUS never disagree in a committed state (R-0154) |
| `.agent/candidates.md` | +18/-10 | C4, CANDIDATES applied whole, the closure-candidate carrier |

### C5 docs(state): write the F008 R36 handback
| Path | +/- | Reason |
| `.agent/handoff.md` | self | C5 cannot table itself (R-0149); its numbers are in the round report |

## External actions
- `git push -u origin feature/f008-sse-event-stream` ran after C4 with `git status --porcelain` printing 0 lines, EXIT 0, printing `3035bc2a..e20fe420  feature/f008-sse-event-stream -> feature/f008-sse-event-stream` and the tracking line. The second push, after C5, belongs to the round report (G13).
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` EXIT 0, output `[]` — the pre-check, not the gate. Then `gh pr create --base main --head feature/f008-sse-event-stream --title 'F008 — SSE event stream (Tier 5)' --body-file .remedy-wt/f008-pr-body.md` EXIT 0, printing `https://github.com/UndefinedDatabase/remedy/pull/209`. PULL REQUEST NUMBER 209.
- `gh pr view 209 --json state,mergeable,isDraft,autoMergeRequest` EXIT 0, verbatim: `{"autoMergeRequest":null,"isDraft":false,"mergeable":"MERGEABLE","state":"OPEN"}`. THE PULL REQUEST WAS NOT MERGED AND AUTO-MERGE WAS NOT ENABLED (constraint 6) — it merges at the next feature's Open PR Gate. No branch was created or deleted and no worktree was added or removed.

## Verification
- G1 `.agent/STOP` ABSENT — `ls -la .agent/STOP` printed `No such file or directory` — read immediately before C0a; `git rev-parse --abbrev-ref HEAD` printed feature/f008-sse-event-stream; `git status --porcelain` printed 0 lines after each of C0a, C0b, C1, C2, C3 and C4, and again before the push. The post-C5 reading is in the round report.
- G2 Transport EQUAL three ways — `.remedy-wt/f008-r36.md` as received, `.agent/authored/f008-r36.md` at C0a and `.agent/last_block.md` at C0b — all sha256 188502199d1931b706c9f016fcf990f435e4754e6f087658d721352576d0fdd9 over 34965 bytes and 490 lines, equal as bytes, and that value EQUALS the digest carried in the task prompt.
- G3 FOURTEEN slices, the COUNT taken from an ordered extraction out of the COMMITTED C0a blob (`git show ca549646:.agent/authored/f008-r36.md`) by their marker lines; newline-INCLUDED sha256 prefix/bytes/lines: PLANF008R36 c70165b8/1875/35, LEDGER36 fcb8264e/5058/1, PINFROM adbd3049/741/10, PINTO 9671c2dc/978/13, STATUSFROM 9cb58ff9/32/1, STATUSTO 005eda59/345/1, RMCOUNT-FROM b4eace4e/68/1, RMCOUNT-TO 255edbe6/76/1, RMTIER-FROM 1cc9fdd3/34/1, RMTIER-TO 5f45bebc/34/1, RMLIST-FROM f9c4e4d1/124/2, RMLIST-TO cb965285/334/5, CANDIDATES 08f555f1/1798/27, PRBODY f90f6a2f/3505/69. The script's aggregate readings over those fourteen: ANY TRAILING WHITESPACE False, ANY LEADING BLANK LINE False, ALL NEWLINE TERMINATED True.
- G4 `.agent/plan.md` at C1 sha256 c70165b8f514b03bfd2013c0edc2e9c93a17b57a190b9902e0bc336ad56ebd15, 1875 bytes, 35 lines (<50), BYTE-EQUAL to PLANF008R36; `Steps` occurs, `^## Goal$` 1x and `^## Next Steps$` 1x line-anchored, and `\bF\d{3}\b` matches with `F008`.
- G5 The append at C2, base bytes read with `git show 3035bc2a:.agent/live_review.md` into `.remedy-wt/` scratch and never over the tracked file. (a) the 532191-byte base blob is a byte-exact PREFIX of the 537250-byte C2 blob and the remainder == newline+LEDGER36, sha256 27e9faf4, 5059 bytes, 2 lines; (b) an INDEPENDENT blank-line split of the WHOLE C2 file, its terminating newline normalised first, gives 247 units whose LAST unit is LEDGER36's paragraph. NEGATIVE CONTROL: one PRINTABLE ASCII byte of the remainder flipped to another printable one (remainder offset 1, `G`→`Z`) REJECTED by BOTH readings, the unflipped value ACCEPTED by both.
- G6 Sets at the round base / at C2, line-anchored: `^- R-\d+ — ` 201/201 — this round mints NO id — `^- R-0630 — ` 0/0, `^- R-0593 — ` 1/1, `^- R-0629 — ` 1/1, `^- R-0429 — ` 1/1, `^- R-0553 — ` 1/1, `^- R-0628 — ` 1/1, `^- R-0368 — ` 1/1, `^Done: R-\d+ — ` 6/6, `^Landed: ` 0/0, `^Gate: R\d+ — ` 35/36 over 35 then 36 DISTINCT keys. HEADER SWEEP at C2: of 36 `Gate: ` lines, 35 match `^Gate: R(\d+) — the R(\d+) entry\.` with second == first−1, 1 does NOT and its text to its first period is `Gate: R1 — the F255 R21 entry.` THE R36 PAIR, BOTH READINGS LABELLED: LINE-ANCHORED over `^Gate: ` lines — the entry-key reading — 1; as a bare substring anywhere in the file 1. (The R35 pair reads 1 line-anchored and 2 as a bare substring, R-0600 quoting F086's identically-worded header; that is the very asymmetry `.agent/candidates.md` now carries.)
- G7 The STATUS edit at C4: STATUSFROM 1 at the round base and 0 at C4, STATUSTO 0 at the base and 1 at C4, and the base blob with that substitution applied ONCE is BYTE-EQUAL to the C4 blob — which is also the proof no other line of that file changed. `^- \[x\] F\d{3} — ` 53 at the base and 54 at C4; `^- \[~\] ` 1 at the base and 0 at C4.
- G8 The README sync at C4, three pairs in one commit. FROM at base / FROM at C4 / TO at base / TO at C4: RMCOUNT 1/0/0/1, RMTIER 1/0/0/1, RMLIST 1/1/0/1 — RMLIST-TO CONTAINS RMLIST-FROM, so 1 at both is the APPEND shape, not a miss. The one-pass reading covering all three: the round-base blob with RMCOUNT, RMTIER and RMLIST each substituted ONCE, in that order, is BYTE-EQUAL to the C4 blob. `README.md` 129 lines at the base, 132 at C4.
- G9 The pin at C3: PINFROM 1 at the round base and 0 at C3, PINTO 0 at the base and 1 at C3, and the base blob of `tests/docs/test_docs_consistency.py` with that substitution applied ONCE is BYTE-EQUAL to the C3 blob. `git show --name-only` for C3 lists exactly `tests/docs/test_docs_consistency.py` and nothing else. The carrier at C4: `.agent/candidates.md` sha256 08f555f198534fe8481b4702e8c49643302e42a8bf034ab1ec365d6605538dc5, 1798 bytes, 27 lines, BYTE-EQUAL to CANDIDATES; `git show --name-only` for C4 lists exactly `.agent/candidates.md`, `README.md` and `docs/roadmap/STATUS.md`.
- G10 In the PRIMARY checkout, SERIALLY, one process at a time. At C3, where the claim is still `[~]`: `python3 -m pytest tests/docs/ -q -rf` EXIT 0, 295 passed, 0 skipped, SUM 295. At C4, where it is gone: the same command EXIT 0, 295 passed, 0 skipped, SUM 295 — that PAIR is the proof PINTO is independent of which feature is claimed. Then `python3 -m pytest tests/cli/test_golden_path.py -q -rf` at C4 EXIT 0, 42 passed, 0 skipped, SUM 42. The runner reported 0 failed for all three, so nothing stops here.
- G11 `git diff --name-only 3035bc2a..e20fe420`, measured from the round base this block's header names and no other SHA, lists 8 paths which are EXACTLY the Change set minus `.agent/handoff.md`, the set difference EMPTY in both directions. Walking `git rev-list --reverse 3035bc2a..e20fe420` gives SIX commits, each read to have exactly ONE parent, with `git show --numstat` and `git diff --numstat` AGREEING on every cell and every cell equal to the `+/-` column above: insertions 490, 402, 13, 2, 10 and 24 — every one under 500, 490 the maximum. Lines BEGINNING with `<<<SLICE ` or `<<<END `: 0 in the plan at C1, 0 in the ledger at C2, 0 in the test file at C3, and 0 in each of STATUS.md, README.md and `.agent/candidates.md` at C4. `git log --format=%H%x09%(trailers:key=Co-Authored-By,valueonly) 3035bc2a..HEAD` run BEFORE C5 lists 6 commits, of which 6 return a NON-EMPTY value — that is the measurement, not a universal. This round's own reflog entries, classified by the OPERATION before the first `:` in `%gs`: SIX classified pre-C5, all `commit`; `amend` 0, `rebase` 0, `cherry` 0. No total over the whole reflog is asserted (R-0601).
- G12 See `## External actions` above for the four readings in order: clean tree + push EXIT 0; `gh pr list` `[]`; `gh pr create` EXIT 0 → PULL REQUEST 209; `gh pr view 209` OPEN, MERGEABLE, not a draft, autoMergeRequest null. No `gh` command was refused by the session guard.
- G13 This file carries every mandated section of docs/agents/handback_template.md, the `## Next` content constraint 10 names in that order, the item-status table below holding exactly one row for each of C0a, C0b, C1, C2, C3, C4 and C5 — "exactly one row" scoping to that TABLE — the pull request number from G12(c), and the four closure values the STATUS line quotes. Measured with `wc -l` in `.remedy-wt/` BEFORE it was written here it is 90 lines, UNDER the 100 this round's seven commits allow. One line per gate here; the raw transcripts are in the round report (R-0582).

## Authored-text proofs
- `.agent/authored/f008-r36.md` at C0a == the received block byte for byte and `.agent/last_block.md` at C0b == the same bytes (G2). All FOURTEEN slices were extracted from the COMMITTED C0a blob by their marker lines and applied programmatically — never retyped, rewrapped, reflowed, reindented or whitespace-adjusted. Whole-file byte equality: PLANF008R36 (G4) and CANDIDATES (G9). Ordered-append equality with a negative control: LEDGER36 (G5). One-pass substitution equality against the round-base blob: PINFROM/PINTO (G9), STATUSFROM/STATUSTO (G7), RMCOUNT, RMTIER and RMLIST (G8). File-copy equality: PRBODY → `.remedy-wt/f008-pr-body.md`, both sha256 f90f6a2feb3662750695067f25601d43cad3c57a20131228f1bc074424dd997e, passed to `gh pr create --body-file`; it is never committed as itself, its bytes reaching the record inside the C0a blob. G11 confirms 0 marker lines in each committed target it names.

## State — Fortschritt
100 % (T001 ✅ · T002 ✅ · T003 ✅ · Integrations-Gate PASSED · Evidence-Job und READY_FOR_REVIEW-Paket verifiziert · STATUS `[x]`, README-Sync und Pull Request gelandet — F008 GESCHLOSSEN, der PR merged am Open PR Gate des nächsten Features) — Schätzung

## Closure values — the four the STATUS line quotes, plus the pull request
| Value | Reading |
|-------|---------|
| Pull request | #209 — https://github.com/UndefinedDatabase/remedy/pull/209, OPEN, NOT merged |
| Evidence job | `f008-closure` |
| package | `remedy-review-20260821-193052-READY_FOR_REVIEW.zip` |
| SHA-256 | `1d827ac756433f3be73f02947d9b1410e7759c4fc9ef6dfd95f5032924b9a366` |
| accepted HEAD | `870f198ea9c0e4b51075f3386d1025cce805811a` |

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | the docs-pin fix; landed before C4, and G10 ran the docs suite green at both |
| C4 | done | the closure commit; the push and the pull request follow it with no commit between |
| C5 | done | this commit |

## Deviations & assumptions
- No departure from the ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5. No extra commit, no dropped commit, no reordering; C1 was the first substantive commit, C3 landed before C4, and the push and `gh pr create` ran between C4 and C5 with no commit between them.
- NO OBJECTION to any slice: all fourteen were applied byte for byte and none looked wrong to me. No `--no-verify` was used on any of the six pre-C5 commits.
- ITEM-25 NOTATION, declared: the block's second FROM-uniqueness reading for PINFROM is "the count of LINES matching `\[~\] F008`", which is 1 only when the file's OWN backslashes are matched literally — the source line is `assert re.search(r"^- \[~\] F008 —", text, re.M)`. Measured at `3035bc2a` by my own script: regex `\\\[~\\\] F008` 1 line; regex `\[~\] F008` 0 lines; substring `F008` 3 lines. PINFROM itself counts 1 in that file, so both halves of item 25 agree under the literal-backslash reading and I report the other two rather than silently picking the one that matches.
- PARTIAL READ, declared against the AGENTS.md File Editing Safety Rule: `.agent/live_review.md` (532191 bytes at the round base) and `tests/docs/test_docs_consistency.py` (2040 lines) were not read end to end. Both edits were made programmatically over whole-file bytes with the byte-level equalities of G5 and G9 standing in for the human read, and the test file additionally passed `python3 -m py_compile` and the full `tests/docs/` suite at C3 and at C4. `.agent/plan.md`, `.agent/candidates.md`, `README.md`'s Status section and STATUS.md's Tier 5 section WERE read before their commits.
- Constraint 3, stated as the measurement it rests on: G11's `git diff --name-only 3035bc2a..e20fe420` lists exactly the 8 Change-set paths minus `.agent/handoff.md` and nothing else, so no file under `packages/`, `apps/` or `docs/roadmap/features/` was edited this round, and the one test file in the set was edited by C3 alone. Constraint 4: R-0630 stays FREE and R-0368, R-0429, R-0553, R-0593, R-0622, R-0628 and R-0629 are all still OPEN — G6's `^- R-\d+ — ` reads 201 at the base and at C2, `^Done: R-\d+ — ` 6 at both and `^Landed: ` 0 at both.
- `npm run lint` was NOT run: it is red at base, it is R-0622, and it is not a gate (R-0364). No full-suite run was ordered this round; the integration gate is R34's and the docs gate plus the canary are what G10 orders.
- The session command guard rejects `$(...)`, `; echo $?`, heredocs, shell loops and chained `;` commands BY FORM, so every multi-step gate was written to a script under the gitignored `.remedy-wt/` and run from there; `git status --porcelain` printed 0 lines after each of C0a through C4, so nothing from that directory was committed. No gate command was piped, so no exit code this round is a pipeline's last stage.
## Next
THIS IS THE LAST ROUND OF THIS BRANCH, so its verdict has NO on-disk gate entry by construction — that absence is the branch terminator, not a missing gate (§4 item 13, the carve-out belonging to the round that CREATES the pull request). The next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1); its SECOND is the Open PR Gate (Phase 1 rule 2), at which PULL REQUEST 209 — this feature's, OPEN and MERGEABLE — is the one to merge. The next free finding id is R-0630. R-0368, R-0429, R-0553, R-0593, R-0622, R-0628 and R-0629 are all OPEN, and `.agent/candidates.md` now carries ONE candidate — the line-anchoring rule for uniqueness gates over `.agent/live_review.md` — which the next feature's FIRST reviewed round must register or resolve, emptying the file in that same round. Rule A5 then proposes F009 — The single write channel — as the next feature, it being the first `[ ]` line this ledger carries top to bottom.
