# Handback — F086 R27

## Range

Review of 788849bb..HEAD — 7 commits, C0a C0b C1 C2 C3 C4 C5, one worker, no PR.

## Commits

| # | SHA | Path | +/- | Reason |
|---|---|---|---|---|
| C0a | cafe207c | .agent/authored/f086-r27.md | 332/0 | save the R27 block |
| C0b | 5731ac97 | .agent/last_block.md | 216/272 | mirror the block |
| C1 | 66a23044 | .agent/plan.md | 16/17 | PLAN27 — plan advanced to R27 |
| C2 | 66ff5ba5 | .agent/live_review.md | 4/0 | FIND0594 + RECORD26 appended |
| C3 | 5399dc0b | docs/agents/planner_reviewer_prompt.md | 18/0 | CHECK29 pair — item 29 |
| C4 | self | .agent/handoff.md | self-ref | this handback (R-0149) |
| C5 | self | .agent/handoff.md | self-ref | VERDICT appended (R-0149) |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`; one `git push` after C5; no PR created or merged, no worktree added or removed.

## Verification

Raw transcript in the round report per R-0582; one line per gate here.
- G1 HYGIENE — `.agent/STOP` absent read from disk before C0a and again at the handback; branch feature/f086-release-capability; `git worktree list` 1 line; `git status --porcelain` empty at every commit and here; NO tracked path was overwritten to take a reading — every non-current reading came from `git show <sha>:<path>` into memory.
- G2 TRANSPORT — scratchpad, committed C0a and committed C0b byte-EQUAL at sha256 94f81b70d17c0135444c666b7efb432fc5f6ea3b07826d2adb01b247a2813e8e, 26606 B over 332 lines.
- G3 PLAN — `.agent/plan.md` at C1 byte-equals PLAN27 extracted from the committed C0a: sha256 e69c3b53cbc1c2effa7a2b2bda0175bef8818c170c9e4d121974bf23db5e224f, 44 lines (under 50), with `## Goal`, `## Next Steps` and `F086` all present.
- G4 LEDGER APPEND — pre-C2 blob is a byte-exact PREFIX of post-C2; the 4-line remainder byte-equals blank + FIND0594 + blank + RECORD26 at sha256 afb559abfc836b65eae1200cc469de75b3895455169835979d57da2332b0ec5c.
- G5 LEDGER SETS — both extractions AGREE at each end: 176 registered / 4 resolved / 0 dup / 0 unregistered / 0 `Landed:` / 172 open at 788849bb, and 177 / 4 / 0 / 0 / 0 / 173 at C2; resolved set unchanged, registered gains exactly R-0594; the control over f0b27118..7b84524c reads `[]` registered gained and exactly R-0584 resolved gained.
- G6 ITEM-20 SCAN — backtick-quoted spans deleted first, then `\bHEAD\b` over C2's 4 added lines reads 0; the RED CONTROL, same extractor over fd166295's added lines, reads 3.
- G7 ITEM-26 HEADERS — 23 headers at 788849bb and 24 at C2; the set occurring more than once is UNCHANGED and exactly `Gate: R19 — the R18 entry.`; `Gate: R27 — the R26 entry.` occurs 1x, is the LAST such header, and the text after it begins `R26 `.
- G8 CHECK29 PAIR — APPEND-shaped, the containment test printed `TO contains FROM: True`, so no FROM-zero count was attempted; CHECK29FROM reads 1x at 788849bb and 1x at C3; the ORDERED EQUALITY holds — C3 equals the base blob with the single FROM occurrence replaced by TO and nothing else — at sha256 a6d4242c91a32dc5c85c987a30bd1ca8fe71c99d3747893f6ae62017f59de854, 901 lines against the base's 883.
- G9 STRUCTURE — `^  27\. \*\*`, `^  28\. \*\*` and `^  29\. \*\*` each read 1 at C3, so nothing was renumbered; the line following CHECK29TO's last line is `  Why this is on disk and not a habit: item 2 has recurred six times across`.
- G10 NO MARKER LEAKED — marker LINES beginning `<<<SLICE ` or `<<<END ` count 0 in `.agent/plan.md`, `.agent/live_review.md` and `docs/agents/planner_reviewer_prompt.md` at C4; the `.agent/handoff.md` reading is post-C5 and is in the round report.
- G11 SUITES, serial in the primary checkout — the four-file selection 160 passed at exit 0, then, after it ended, the canary 42 passed at exit 0. No suite in this repository reads `docs/agents/planner_reviewer_prompt.md`, so G8 and G9 are C3's whole evidence and the green says nothing about it.
- G12 CHANGE SET — the range path set equals the Change list with no path on either side alone; all seven forbidden paths are present at 788849bb and untouched; the range is linear and every `git reflog` entry is `commit:`; per §3 item 28 every measurable `+/-` cell above is pasted from `git diff --numstat <sha>^ <sha>`, max insertion column 332 under the 500 cap; `wc -l` reads 50 for `.agent/handoff.md` at C4, within the bound this round's block states in constraint 8, and the C5 reading is post-C5 and in the round report; all seven mandated headings are present in the template's order.
- G13 OPEN PR GATE — re-read at the handback, literal output `[]`. Nothing created, nothing merged.

## Authored-text proofs

PLAN27, FIND0594, RECORD26, CHECK29FROM, CHECK29TO and VERDICT were extracted PROGRAMMATICALLY from the committed C0a at cafe207c and applied byte-verbatim; G3, G4 and G8 are their disk-to-disk equalities. No slice was retyped, rewrapped or reformatted, and no marker line reached a target.

## Deviations & assumptions

None. The commit sequence was C0a, C0b, C1, C2, C3, C4, C5 exactly as the block labels it — nothing added, dropped or reordered.

## Next

The reviewer reviews 788849bb..HEAD and records R27's verdict as `Gate: R28 — the R27 entry.`; the packaging ist-doc then precedes closure.
