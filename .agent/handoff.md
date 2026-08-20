# Handback — F086 R25

## Range

Review of `e33ba23a..HEAD`.

## Commits

Every `+/-` cell below is READ OUT of `git diff --numstat <sha>^ <sha>` for that commit and pasted from that reading, never derived from a file's line count before and after (constraint 9, the R-0592 counter-measure applied to the block that registers it).

| Commit | Short SHA | Path | +/- | Reason |
|---|---|---|---|---|
| C0a | b2751475 | `.agent/authored/f086-r25.md` | +329/-0 | the R25 block saved byte-verbatim |
| C0b | 67fbecb5 | `.agent/last_block.md` | +157/-208 | mirror of the committed C0a, read back from git |
| C1 | 404706f5 | `.agent/plan.md` | +5/-5 | whole file := PLAN25 |
| C2 | 2df326eb | `.agent/live_review.md` | +4/-0 | append: blank, FIND0592, blank, RECORD24 |
| C3 | 764b5a4a | `docs/agents/planner_reviewer_prompt.md` | +18/-0 | the CHECK28 APPEND pair, adding item 28 |
| C4, C5 | this commit, then its successor | `.agent/handoff.md` | see round report | this handback, then VERDICT appended verbatim |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` -> exit 0, output `[]` (G14). `git push -u origin feature/f086-release-capability` runs ONCE after C5, so its outcome is in the round report. No PR created, nothing merged, no worktree added or removed.

## Verification

G1 HYGIENE: `.agent/STOP` absent, read from disk before C0a and again now; branch `feature/f086-release-capability`; `git status --porcelain` EMPTY at every commit and now; `git worktree list` ONE line throughout.
G2 TRANSPORT: `.remedy-wt/f086-r25.md`, the committed `.agent/authored/f086-r25.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 1b8b5e50f3c473c945dc768ce18b53a7c09418c348f2407b2f32202baa5c9f3b, 26126 B over 329 lines.
G3 PLAN: `.agent/plan.md` at 404706f5 is byte-equal to PLAN25 extracted from the COMMITTED C0a, sha256 593fb7b6d0e8a9791dd25f08ee62fa6a8b6ffd1d0ab71663a17017f6fce384c7, 45 lines (under the AGENTS.md 50), carrying `## Goal`, `## Next Steps` and `F086`.
G4 LEDGER APPEND: the pre-C2 blob is a byte-exact PREFIX of the post-C2 blob and the 4-line remainder is byte-equal to a blank line, FIND0592, a blank line, RECORD24 — sha256 a52e460cd4c8e4a8991ceee3cbb440553f61951fa4b765e9c3e0771b5ecc885d, 6499 B.
G5 LEDGER SETS: two independent extractions (python regex over the blob; `grep -oE` over the same blob on stdin) AGREE at each end — 174 registered / 4 resolved / 0 duplicates / 0 unregistered resolutions / 0 `Landed:` / 170 open at `e33ba23a`, and 175 / 4 / 0 / 0 / 0 / 171 at C2; the resolved set is UNCHANGED and the registered set gains exactly `R-0592` and loses nothing. CONTROL over `f0b27118..7b84524c` reads `[]` registered while its resolved set gains exactly `R-0584`, so the reading is not vacuous.
G6 ITEM-20 SCAN: over the lines C2 ADDS, backtick-quoted spans deleted FIRST, `\bHEAD\b` reads 0. RED CONTROL, same two-step extractor over the lines `fd166295` adds to the same file: 3.
G7 ITEM-26 HEADERS: 21 at `e33ba23a`, 22 at C2; the set of headers occurring more than once is UNCHANGED and is exactly `Gate: R19 — the R18 entry.`, which constraint 3 preserves rather than repairs. `Gate: R25 — the R24 entry.` occurs 1x, is the LAST such header, and the text after it begins `R24 ` (after the single space separating header from body).
G8 THE CHECK28 PAIR, in the APPEND form: the containment test printed `TO contains FROM: True`; CHECK28FROM occurs exactly 1x at `e33ba23a` and exactly 1x at C3; and the ORDERED EQUALITY holds — the C3 blob is byte-equal to the `e33ba23a` blob with CHECK28FROM's single occurrence replaced by CHECK28TO and nothing else changed. C3 sha256 c41442d8c72fa67b170e2596b457440e3b5375a074159eb65136dc625fcc014f, 883 lines against the base's 865.
G9 STRUCTURE: `^  26. **`, `^  27. **` and `^  28. **` each read 1, so nothing was renumbered and no existing item moved. The line FOLLOWING CHECK28TO's last line is the line beginning `  Why this is on disk and not a habit:`.
G10 NO MARKER LEAKED: 0 LINES beginning `<<<SLICE ` or `<<<END ` in `.agent/plan.md`, in `.agent/live_review.md` and in `docs/agents/planner_reviewer_prompt.md` at C4. The `.agent/handoff.md` reading can only be taken after C5 and is in the round report.
G11 SUITES, serially in the PRIMARY checkout: `test_test_runner.py test_dashboard_contract.py test_resource_safety.py test_integrity_gate.py -q -rf` — exit 0, `160 passed in 19.98s`; then, started only after that had ENDED, the canary `tests/cli/test_golden_path.py -q` — exit 0, `42 passed in 20.35s`. No suite here reads `docs/agents/planner_reviewer_prompt.md`, so G8 and G9 are C3's whole evidence and green says nothing about it.
G12 CHANGE SET AND HISTORY: the range's path set is the five paths tabled above, equal to the Change list other than `.agent/handoff.md`, with no path on either side alone; all seven paths the Change section FORBIDS are PRESENT at `e33ba23a` and none is touched; every commit has exactly one parent; every `git reflog` entry of the round is `commit:`; the numstat pairs are `329 0`, `157 208`, `5 5`, `4 0`, `18 0`, each byte-identical to the `+/-` cell tabled for that commit, and the insertion column alone — 329, 157, 5, 4, 18 — is under 500 for every commit (DECISION F104 D1). C4's and C5's own rows cannot be measured before they exist and are in the round report.
G13 THE HANDBACK: `wc -l` of `.agent/handoff.md` at C4 reads 55, within the bound CONSTRAINT 8 sets for it. All seven mandated headings of docs/agents/handback_template.md are present in the template's order and no section is dropped. The C5 reading and the prefix-and-remainder equality against VERDICT are in the round report.
G14 OPEN PR GATE, re-read at the handback: `gh pr list --state open --json number,headRefName,baseRefName,isDraft` -> exit 0, literal output `[]`. Nothing created, nothing merged.

## Authored-text proofs

PLAN25, FIND0592, RECORD24, both CHECK28 halves and VERDICT were EXTRACTED programmatically from the committed `.agent/authored/f086-r25.md`, never retyped, and each landed byte-exact: G3 for PLAN25, G4 for the two ledger slices, G8 for the pair, and the C5 remainder for VERDICT in the round report.
The block itself: the scratchpad, the committed authored copy and the committed last-block mirror are byte-EQUAL (G2) at the digest the delegation named, so nothing was altered in transport.

## Deviations & assumptions

NONE TO THE ORDERED SEQUENCE: C0a, C0b, C1, C2, C3, C4, C5 ran in that order — no extra commit, none dropped, none reordered — and the change set is exactly the six paths the block names and nothing else.
NO SLICE DEFECT FOUND: every constant the block asserts about the tree reproduced on measurement — the base's 865 lines, CHECK28FROM at 1x, VERDICT at 39 lines, the `Gate: R19 — the R18 entry.` duplicate — so constraint 1's declare-do-not-repair path was not needed this round.
ONE READING TAKEN LITERALLY, declared rather than assumed: G7 asks that the text immediately following `Gate: R25 — the R24 entry.` begin `R24 `; the byte immediately after `entry.` is the single space separating header from body, and `R24 ` begins directly after it.
THE R-0592 INSTANCE REPRODUCED HERE, reported because it is this round's subject: `.agent/last_block.md` went from 380 lines to 329, while C0b's numstat reads `157 208`. Neither line count appears in the table above; the numstat pair does.

## Next

The reviewer reviews `e33ba23a..HEAD` and records R25's verdict in `.agent/live_review.md` as `Gate: R26 — the R25 entry.` (§3 item 26). F086's next substantive round is closure.

## Reviewer's session verdict — authored by the reviewer, applied by the worker

Written because finding R-0571 is that a verdict issued and never put on disk cannot be
told apart from one never issued. Session of 2026-08-20, self-drive per
docs/agents/self_drive_protocol.md, resuming at `e33ba23a` under a three-round cap
declared up front per guardrail G7. The reviewer wrote nothing in the work tree, one
delegated worker per round made every commit, and the verdict below rests on gates the
reviewer RE-EXECUTED over the committed diff, never on a handback.

| Round | Range | Verdict |
|---|---|---|
| R24 | 39bfc199..e33ba23a | PASS — one finding, R-0592, against the reviewer |
| R25 | e33ba23a..this range | verdict not yet on disk; see the last paragraph |

R24 was inherited ungated, so Phase 1 rule 4 reviewed it before any new work was
planned. All fourteen of its gates reproduce to the byte on the reviewer's own runs:
the three-way transport digest, PLAN24, the eight-line ledger remainder, the ordered
equality over the three checklist pairs, both ledger extractions with the control
moving, the item-20 scan with its red control reading 3, the header check, and both
suites green at exit 0 on runs the reviewer took serially and independently.

R-0592 IS A GAP IN THE REVIEWER'S GATE COVERAGE, NOT IN THE WORKER'S EXECUTION. The
worker computed every insertion count R24's G12 ordered and reported all five
correctly; the `## Commits` table beside them carried the same value for one commit a
second time, derived from line counts instead of from the diff, and no clause of that
block and no item of the §3 checklist had ever named that table. R25 registers it and
lands item 28, which closes the class rather than the instance.

WHAT THIS FEATURE STILL OWES: closure alone. NO INSTALL HAS BEEN PROVEN in this session
or any other and no round of this workflow can prove one; DECISION F086 D4 records that
with its measurement, the release workflow has never been dispatched, and closure names
both as unproven rather than counting a skipped test as coverage.

R25 IS NOT A TERMINATOR — F086's pull request is created at closure, which has not
happened — so this session claims no §4 item 13 carve-out and leaves its last verdict to
be recorded (R-0583). THE NEXT SESSION'S FIRST ACTIONS are Phase 1 rule 1, then rule 2,
then rule 4: review this round and record R25's verdict as `Gate: R26 — the R25 entry.`,
the header shape §3 item 26 binds. Its first substantive work is closure.
