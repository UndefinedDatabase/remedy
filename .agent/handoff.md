# Handback — F086 R28

## Range

Review of b86812be..HEAD — 8 commits, C0a C0b C1 C2 C3 C4 C5 C6, one worker, no PR.

## Commits

| # | SHA | Path | +/- | Reason |
|---|---|---|---|---|
| C0a | f76caa4e | .agent/authored/f086-r28.md | 353/0 | save the R28 block |
| C0b | 5bb492a2 | .agent/last_block.md | 264/243 | mirror the block |
| C1 | 72b2c395 | .agent/plan.md | 16/11 | PLAN28 — plan advanced to R28 |
| C2 | fbe6e8ae | .agent/live_review.md | 6/0 | FIND0595 + FIND0596 + RECORD27 appended |
| C3 | 3ea49692 | docs/roadmap/features/T2_F086.md | 3/1 | BUILT pair — the R-0595 correction |
| C4 | 9503d2bf | tests/docs/test_docs_consistency.py | 6/2 | LINK pair — the R-0596 gate repair |
| C5 | 27596f3e | .agent/live_review.md | 4/0 | DONE0595 + DONE0596 appended |
| C6 | self | .agent/handoff.md | self-ref | this handback (R-0149) |

| Item | Status | Reason |
|---|---|---|
| R-0595 | done | registered at C2, corrected at C3, resolved at C5 |
| R-0596 | done | registered at C2, repaired at C4, resolved at C5 |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`; two disposable worktrees added under `.remedy-wt/` for G10's red control, at C4 and at b86812be, both removed with `git worktree remove --force` and `git worktree prune` before C5; one `git push` after C6; no PR created or merged.

## Verification

Raw transcript in the round report per R-0582; one line per gate here.
- G1 HYGIENE — `.agent/STOP` absent, read from disk before C0a and again at the handback; branch feature/f086-release-capability; `git status --porcelain` empty at every commit and here; `git worktree list` 1 line at every commit and here, the two G10 worktrees having existed only between C4 and C5 with no commit taken while they did; NO path in the primary checkout was overwritten to take a reading — every non-current reading came from `git show <sha>:<path>` into memory.
- G2 TRANSPORT — the `.remedy-wt/` scratchpad, the committed C0a and the committed C0b are byte-EQUAL at sha256 6bdf7e7d5d41c9018724b9e560c71d1c1d62c898f86183fc5ce3f178a622a3b5, 30770 B over 353 lines.
- G3 PLAN — `.agent/plan.md` at C1 byte-equals PLAN28 extracted from the committed C0a: sha256 277c0482644efd2b53f26b8a79443d3f00a5abd6baaf12611e8929b7e505233e, 49 lines (under 50), with `## Goal`, `## Next Steps` and `F086` all present.
- G4 LEDGER APPENDS — pre-C2 is a byte-exact PREFIX of post-C2 whose 6-line remainder equals blank + FIND0595 + blank + FIND0596 + blank + RECORD27 at sha256 509fb277956a124fb0973d4b9db3d1ba264f01c6430557ca199023d0b3731342; pre-C5 is a byte-exact PREFIX of post-C5 whose 4-line remainder equals blank + DONE0595 + blank + DONE0596 at sha256 e5185e15320b506a1f9c2e912c97b04e9618ce0d48b127a41b0941ecc2e66022.
- G5 LEDGER SETS — both extractions AGREE at all three ends: 177 registered / 4 resolved / 0 dup / 0 unregistered / 0 `Landed:` / 173 open at b86812be, 179 / 4 / 0 / 0 / 0 / 175 at C2, and 179 / 6 / 0 / 0 / 0 / 173 at C5; registered gains exactly R-0595 and R-0596 at C2 and nothing at C5, resolved is unchanged at C2 and gains exactly those two at C5; the control over f0b27118..7b84524c reads `[]` registered gained and exactly R-0584 resolved gained.
- G6 ITEM-20 SCAN — backtick-quoted spans deleted first, then `\bHEAD\b` reads 0 over C2's 6 added lines and 0 over C5's 4; the RED CONTROL, the same extractor over fd166295's added lines, reads 3.
- G7 ITEM-26 HEADERS — 24 headers at b86812be and 25 at C2; the set occurring more than once is UNCHANGED and exactly `Gate: R19 — the R18 entry.`; `Gate: R28 — the R27 entry.` occurs 1x, is the LAST such header, and the text after it begins `R27 `.
- G8 BUILT PAIR — REWRITE-shaped, the containment test printed `TO contains FROM: False`; BUILTFROM reads 1x at b86812be and 0x at C3 while BUILTTO reads 1x at C3; the ORDERED EQUALITY holds at sha256 ec119ea594eb021f741dffc9cc815da8c9bef4c7065a78ce11630f149e9bbfa2, 92 lines against the base's 90; `tests/test_packaging_smoke.py` is ABSENT from this round's change set.
- G9 LINK PAIR — same REWRITE form, `TO contains FROM: False`, LINKFROM 1x at b86812be and 0x at C4, LINKTO 1x at C4, ordered equality at sha256 c763e230f26e5e95e867fa10e93fa132d2f22254bf9f078db54380cdd8a65ff1, 2033 lines against the base's 2029; each blob fed to `python3 -m ruff check --stdin-filename tests/docs/test_docs_consistency.py -` gives an EMPTY rule-code multiset at exit 0 at both ends, so C4's multiset is a subset of the base's and nothing was written to the tree.
- G10 GATE REPAIR IS REAL — at C4 the collect-only reading is exactly five ids, `[README.md]`, `[AGENTS.md]`, `[docs/README.md]`, `[docs/roadmap/STATUS.md]`, `[docs/roadmap/ROADMAP.md]`, with neither `[README.md0]` nor `[README.md1]` present; the red-control row in a disposable worktree at C4 FAILS with `AssertionError: docs/README.md has broken links: ['system/no-such-doc-v0.md']` at exit 1 (1 failed, 294 passed), and the SAME control in a second worktree at b86812be PASSES at 295 passed, exit 0; both worktrees removed and pruned, `git worktree list` back to 1 line and the tree clean before C5.
- G11 SUITES, serial in the primary checkout, each started after the previous ENDED — `tests/docs/` 295 passed at exit 0, equal to the 295 the reviewer measured at b86812be; then the four-file state-reader selection 160 passed at exit 0; then the canary 42 passed at exit 0. No suite reads `docs/roadmap/features/T2_F086.md` for the sentence C3 corrects, so G8 is that commit's whole evidence.
- G12 NO MARKER LEAKED — marker LINES beginning `<<<SLICE ` or `<<<END ` count 0 in `.agent/plan.md`, `.agent/live_review.md`, `docs/roadmap/features/T2_F086.md` and `tests/docs/test_docs_consistency.py` at C6.
- G13 CHANGE SET, HISTORY, HANDBACK — the range path set equals the Change list with no path on either side alone; all twelve forbidden paths are present at b86812be and untouched; `docs/system/release-capability-v1.md` is absent at both ends; the range is linear and every `git reflog` entry is `commit:`; every `+/-` cell above is pasted from `git diff --numstat <sha>^ <sha>`, max insertion column 353 under the 500 cap; the `wc -l` of this file is in the round report, measured against the bound constraint 11 states; all seven mandated headings are present in the template's order with no section dropped.
- G14 OPEN PR GATE — re-read at the handback, literal output `[]`. Nothing created, nothing merged.

## Authored-text proofs

PLAN28, FIND0595, FIND0596, RECORD27, BUILTFROM, BUILTTO, LINKFROM, LINKTO, DONE0595 and DONE0596 were extracted PROGRAMMATICALLY from the committed C0a at f76caa4e and applied byte-verbatim; G3, G4, G8 and G9 are their disk-to-disk equalities. No slice was retyped, rewrapped or reformatted, and no marker line reached a target.

## Deviations & assumptions

None. The commit sequence was C0a, C0b, C1, C2, C3, C4, C5, C6 exactly as the block labels it — nothing added, dropped or reordered, and C3 and C4 both landed before C5 as constraint 5 requires. No slice needed the constraint 1 declaration.

## Next

The reviewer reviews b86812be..HEAD and records R28's verdict as `Gate: R29 — the R28 entry.`; R29 then writes the packaging ist-doc with its two `docs/README.md` rows, which is the first change the repaired link gate will judge.
