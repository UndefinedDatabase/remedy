# Handback — F086 R29

## Range

Review of 05c6e012..HEAD — 6 commits, C0a C0b C1 C2 C3 C4, one worker, no PR.

## Commits

| # | SHA | Path | +/- | Reason |
|---|---|---|---|---|
| C0a | 9253de0a | .agent/authored/f086-r29.md | 475/0 | save the R29 block |
| C0b | f6818587 | .agent/last_block.md | 372/250 | mirror the block |
| C1 | f2aac277 | .agent/plan.md | 18/23 | PLAN29 — plan advanced to R29 |
| C2 | d4cba0d9 | .agent/live_review.md | 2/0 | RECORD28 appended |
| C3 | 455e5640 | docs/system/release-capability-v1.md; docs/README.md | 154/0; 2/0 | the ist-doc and BOTH index rows in ONE commit |
| C4 | self | .agent/handoff.md | self-ref | this handback (R-0149) |

| Item | Status | Reason |
|---|---|---|
| Bundle 1 — block saved and mirrored | done | C0a + C0b |
| Bundle 2 — plan advanced to R29 | done | C1, first substantive commit per constraint 6 |
| Bundle 3 — RECORD28 in the ledger | done | C2 |
| Bundle 4 — ist-doc + two index rows | done | C3, one commit per constraint 5 |
| Bundle 5 — the handback | done | C4 |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`; one disposable worktree `.remedy-wt/g10ctl` added at C3 for G10's red control and removed with `git worktree remove --force` plus `git worktree prune` before C4; one `git push` after C4; no PR created or merged.

## Verification

Raw transcript in the round report per R-0582; one line per gate here.
- G1 HYGIENE — `.agent/STOP` absent, read from disk before C0a and again at the handback; branch feature/f086-release-capability; `git status --porcelain` empty at every commit and here; `git worktree list` 1 line at every commit and here, the G10 worktree having existed only between C3 and C4 with no commit taken while it did; NO path in the primary checkout was overwritten to take a reading — every non-current reading came from `git show <sha>:<path>` into memory.
- G2 TRANSPORT — the `.remedy-wt/` scratchpad, the committed C0a and the committed C0b are byte-EQUAL at sha256 3c7aba5f2af0cf4958e4bdf131f5fa728cd35b614c4a9e13b75532803f9193ed, 32762 B over 475 lines.
- G3 PLAN — `.agent/plan.md` at C1 byte-equals PLAN29 extracted from the committed C0a: sha256 983b73027a5a1922e814e2b9703ab70df0f90333f2e38c4d521716f45abd9123, 44 lines (under 50), with `## Goal`, `## Next Steps` and `F086` all present.
- G4 LEDGER APPEND — pre-C2 is a byte-exact PREFIX of post-C2 whose 2-line remainder equals a blank line followed by RECORD28, at sha256 8a67100852ff2a3f43e86b2eca35f8e9c659907edff3d4863fd94e8f69b00850.
- G5 LEDGER SETS — both extractions AGREE at both ends: 179 registered / 6 resolved / 0 dup / 0 unregistered / 0 `Landed:` / 173 open at 05c6e012 and the SAME 179 / 6 / 0 / 0 / 0 / 173 at C2; the registered set at C2 EQUALS the one at 05c6e012 and so does the resolved set, gaining `[]` on both sides; the control over f0b27118..7b84524c MOVES, reading `[]` registered gained and exactly `R-0584` resolved gained.
- G6 ITEM-20 SCAN — backtick-quoted spans deleted first, then `\bHEAD\b` reads 0 over C2's 2 added lines; the RED CONTROL, the same two-step extractor over fd166295's 4 added lines, reads 3.
- G7 ITEM-26 HEADERS — 25 headers at 05c6e012 and 26 at C2; the set occurring more than once is UNCHANGED and exactly `Gate: R19 — the R18 entry.`; `Gate: R29 — the R28 entry.` occurs 1x, is the LAST such header, and the text after it begins `R28 ` once its leading space is stripped.
- G8 THE IST-DOC — `git ls-tree` at 05c6e012 prints nothing for the path and at C3 prints its blob; the bytes at C3 equal the DOC slice at sha256 6f4a10254c81df2a53d8e90c5b4609833aed4428b8c255a6540ce542f93224fa over 154 lines, and the 154 lines C3's diff adds for that path are exactly the slice's lines in order.
- G9 THE INDEX PAIRS — both APPEND-shaped, each containment test printed on its own line: `QUICK — TO contains FROM: True` and `SYS — TO contains FROM: True`; QUICKFROM 1x at 05c6e012 and 1x at C3 with QUICKTO 1x at C3, and the same three readings for SYSFROM/SYSTO; the ORDERED EQUALITY holds — C3 equals the base blob with each FROM's single occurrence replaced by its TO and nothing else — at sha256 4eeb90b7c2998ef2ebf04ecb790966d46672c28c8acc27cf889819f33d984d40, 230 lines against the base's 228; over the 2 lines C3 adds to `docs/README.md` each TO-ONLY row occurs exactly 1x.
- G10 THE NEW ROWS ARE JUDGED — at C3 in the primary checkout the single case `TestPrimaryDocLinksResolve::test_every_relative_markdown_link_exists[docs/README.md]` PASSES at exit 0 (1 passed), reading the rows C3 added; the RED CONTROL, in the disposable worktree at C3 with both occurrences of `system/release-capability-v1.md` (2x there, 0x at 05c6e012) rewritten to `system/release-capability-v0.md` in `docs/README.md` alone, FAILS the same command at exit 1 with `AssertionError: docs/README.md has broken links: ['system/release-capability-v0.md', 'system/release-capability-v0.md']`; worktree removed and pruned, `git worktree list` back to 1 line and the tree clean before C4.
- G11 SUITES, serial in the primary checkout, each started after the previous ENDED — `tests/docs/` 295 passed at exit 0, equal to the 295 the reviewer measured at 05c6e012, the count REPORTED and not predicted; then the four-file state-reader selection 160 passed at exit 0; then the canary 42 passed at exit 0.
- G12 NO MARKER LEAKED — marker LINES beginning `<<<SLICE ` or `<<<END ` count 0 in `.agent/plan.md`, `.agent/live_review.md`, `docs/system/release-capability-v1.md` and `docs/README.md` at C4.
- G13 CHANGE SET, HISTORY, HANDBACK — the range path set equals the Change list with no path on either side alone; all thirteen forbidden paths are present at 05c6e012 and untouched; the range is linear (each commit one parent) and every `git reflog` entry of this round is `commit:`; every `+/-` cell above is pasted from `git diff --numstat <sha>^ <sha>`, max insertion column 475 under the 500 cap; the `wc -l` of this file is in the round report, measured against the bound constraint 12 states; all seven mandated headings are present in the template's order with no section dropped.
- G14 OPEN PR GATE — re-read at the handback, literal output `[]`. Nothing created, nothing merged.

## Authored-text proofs

PLAN29, RECORD28, DOC, QUICKFROM, QUICKTO, SYSFROM and SYSTO were extracted PROGRAMMATICALLY from the committed C0a at 9253de0a and applied byte-verbatim; G3, G4, G8 and G9 are their disk-to-disk equalities. No slice was retyped, rewrapped or reformatted, and no marker line reached a target.

## Deviations & assumptions

None. The commit sequence was C0a, C0b, C1, C2, C3, C4 exactly as the block labels it — nothing added, dropped or reordered, and C3 wrote the ist-doc and both index rows together as constraint 5 requires. No slice needed the constraint 1 declaration.

## Next

The reviewer reviews 05c6e012..HEAD and records R29's verdict; CLOSURE is then the next and last round per docs/roadmap/STATUS_closure_protocol.md — evidence job, FRESH review zip, the STATUS line, the README capability sync in that same commit, and the PR.
