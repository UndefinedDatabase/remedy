# Handback — F086 R22

## Range

Review of `e7cdae4d..HEAD`.

## Commits

One table, one row per commit (compact form, constraint 7).

| Commit | Short SHA | Path | +/- | Reason |
|---|---|---|---|---|
| C0a | 787a1141 | `.agent/authored/f086-r22.md` | +336/-0 | the R22 block saved byte-verbatim |
| C0b | 39ab54ef | `.agent/last_block.md` | +185/-200 | mirror of the committed C0a, read back from git |
| C1 | f6bafbdc | `.agent/plan.md` | +11/-9 | whole file := PLAN22 |
| C2 | 79dbd1d4 | `.agent/live_review.md` | +4/-0 | append: blank, FIND0588, blank, RECORD20 |
| C3 | 72640273 | `docs/agents/planner_reviewer_prompt.md` | +15/-0 | item 14 gains the R-0588 clause |
| C4, C5 | this commit, then its successor | `.agent/handoff.md` | see round report | this handback, then VERDICT appended verbatim; a handoff cannot table the commit that writes it (R-0149) |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` -> `[]`. Nothing created, nothing merged. One push of this branch after C5.

## Verification

G1 HYGIENE: `git status --porcelain` empty at every commit and at the handback; `.agent/STOP` absent, re-read before C0a and again now; branch `feature/f086-release-capability`; `git worktree list` one line throughout; no mutation and no disposable worktree ordered.
G2 TRANSPORT: `.remedy-wt/f086-r22.md`, the committed `.agent/authored/f086-r22.md` and the committed `.agent/last_block.md` are all three byte-EQUAL at sha256 d4d00dfbf05f263c2c4f3b5a94eab14ab9533a84dcbcfeadcd46771741a5f4bf, 27444 bytes, 336 lines.
G3 PLAN: `.agent/plan.md` at f6bafbdc byte-equal to PLAN22 extracted from the committed C0a, sha256 1955bfe2937ae46ef5e3c7c5f10e8cc6973391936c535629b64d8b781a206ac7, 44 lines (under 50), containing `## Goal`, `## Next Steps` and `F086`.
G4 LEDGER APPEND: the pre-C2 blob is a byte-exact PREFIX of the post-C2 blob; the remainder is byte-equal to a blank line, FIND0588, a blank line, RECORD20, at sha256 51cae6480f0be3fe54cda0b91134d1bd23ab8b04b8bd6cf31769f7707cceb132 over 4 lines.
G5 LEDGER SETS: both extractions agree at C2 — 171 registered, 3 resolved, 0 duplicates, 0 unregistered resolutions, 0 anchored `Landed:` lines, 168 open — the two registered id SETS are EQUAL, and the symmetric difference against the `e7cdae4d` set is exactly `['R-0588']`; CONTROL `f0b27118..7b84524c` reads `[]` registered while its resolved set gains exactly `R-0584`.
G6 ITEM-20 SCAN: over the lines C2 ADDS, backtick-quoted spans deleted first, `\bHEAD\b` reads 0; RED CONTROL over the lines `fd166295` adds to the same file reads 3. Binds the ledger commit only.
G7 ITEM-26 CHECK: at `e7cdae4d` 18 headers with exactly one string twice, `Gate: R19 — the R18 entry.` (the red control); at C2 19 headers, that duplicate SET UNCHANGED because constraint 3 forbids repairing it, `Gate: R22 — the R21 entry.` occurring 1x, being the LAST such header, and the text after it beginning `R21 `.
G8 THE PAIR: `TO contains FROM: true`, so the pair is APPEND-shaped and the obligation is the append form; CHECK14FROM occurs 1x at `e7cdae4d` AND 1x at C3; each of the 15 CHECK14TO-ONLY lines occurs exactly 1x among C3's 15 added lines; ordered equality holds — C3's file is the `e7cdae4d` blob with CHECK14FROM's single occurrence replaced by CHECK14TO and nothing else changed — at sha256 1df716cdff9b2e290f43e311787a31bdfcde80483a9f37ec53bfc845b9aef12c over 820 lines, against 805 at the base.
G9 STRUCTURE: `grep -c '^  15\. \*\*' docs/agents/planner_reviewer_prompt.md` reads 1, `grep -c '^  14\. \*\*' ...` reads 1, and the line after CHECK14TO's last line is `  15. **Pair shapes are classified by a containment test, never by eye.** Finding` — the clause landed inside item 14 and renumbered nothing.
G10 NO MARKER LEAKED: 0 lines beginning `<<<SLICE ` or `<<<END ` in `.agent/plan.md`, `.agent/live_review.md` and `docs/agents/planner_reviewer_prompt.md` at C4, counting marker LINES; the `.agent/handoff.md` reading can only be taken after C5 and is in the round report.
G11 SUITES, serially in the PRIMARY checkout, the second started only after the first ENDED and reported its code: the four state readers exit 0 with 160 passed; then the canary exits 0 with 42 passed. No suite reads `docs/agents/planner_reviewer_prompt.md`, so G8 and G9 are C3's entire evidence.
G12 CHANGE SET AND HISTORY: the printed path set equals the set constraint 2 names other than `.agent/handoff.md`, with no path on either side alone; every path constraint 2 FORBIDS is PRESENT at `e7cdae4d` by `git ls-tree`; the range is linear with every commit at exactly one parent and the round's `git reflog` entries all `commit:`; insertions before C4 are 336, 185, 11, 4 and 15, none over 500.
G13 THE HANDBACK, BOTH HALVES: (a) `wc -l` of `.agent/handoff.md` at C4 reads 52, within constraint 7's bound of 56; (b) at C5 it must read 96, that is (a) plus VERDICT's 44, within 100. (a) held, so no DECISION D15 "Deviations, declared" line was needed and none was written. All seven mandated headings of docs/agents/handback_template.md are present in the template's order and no section was dropped. The prefix-and-remainder equality is measurable only after C5 and is in the round report.
G14 OPEN PR GATE, re-read at the handback: `gh pr list --state open --json number,headRefName,baseRefName,isDraft` printed `[]`. Nothing created, nothing merged.

## Authored-text proofs

PLAN22, FIND0588, RECORD20, CHECK14FROM, CHECK14TO and VERDICT were all EXTRACTED programmatically from the committed `.agent/authored/f086-r22.md`, never retyped. Disk-to-disk: `.agent/plan.md` at C1 equals PLAN22 exactly (G3); C2's remainder equals blank+FIND0588+blank+RECORD20 exactly (G4); C3's file equals the base with CHECK14FROM replaced by CHECK14TO and nothing else (G8); C5's remainder equals VERDICT exactly, reported in the round report because it is measurable only after C5.
The block itself: the scratchpad, the committed authored copy and the committed last-block mirror are byte-EQUAL (G2). Constraint 8 re-measured from the COMMITTED C0a: 336 lines TOTAL, 217 prose, 119 slice including its 12 marker lines — against DECISION F085 D6's 490 total and D5's 400 prose.

## Deviations & assumptions

None. The block's ordered sequence C0a, C0b, C1, C2, C3, C4, C5 was executed in order, with no extra commit, none dropped and no reordering. Constraint 3 was honoured: the duplicate header at `4dc7cbdf` and the handoff at `e7cdae4d` that lacks its DECISION D15 line are both left standing, and G7 records the duplicate as expected rather than as a violation. No verdict was authored by the worker anywhere.

## Next

The reviewer reviews `e7cdae4d..HEAD` and records R22's verdict in `.agent/live_review.md` as `Gate: R23 — the R22 entry.`; the next substantive work is the integration gate.
