# Handback — F086 R21, the R20 record and the two checklist promotions (branch feature/f086-release-capability)

## Range

Review of a7373e00..HEAD (6 commits: 7f82ad08, 6d2233fb, ba8cf1b9, a4fba89b, e1af7921, C4; C5 then appends VERDICT to this file).

## Commits

### 7f82ad08 docs(state): save the F086 R21 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f086-r21.md | +351/-0 | C0a — the R21 block, byte-verbatim |

### 6d2233fb docs(state): mirror the F086 R21 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +256/-387 | C0b — mirror read back from the committed C0a with `git show` |

### ba8cf1b9 docs(state): advance the plan to F086 R21
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +16/-14 | C1 — PLAN21, whole file, alone, before the ledger moves |

### a4fba89b docs(review): register R-0587 and record the R20 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | C2 — pure append: FIND0587 then RECORD19 |

### e1af7921 docs(agents): promote the R-0586 and R-0587 rules into the checklist
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +32/-0 | C3 — both pairs in ONE commit: the item-20 clause and the new item 26 |

### C4 and C5, grouped — a handoff cannot table the commit that writes it (R-0149)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C4 — this file |
| .agent/handoff.md | append | C5 — the VERDICT slice, appended byte-verbatim |

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — Open PR Gate re-read; result on the G14 line. Nothing created, nothing merged.
- `git push -u origin feature/f086-release-capability` — outcome in the round report.
- NO worktree added and none removed: this round ordered no mutation, so `git worktree list` read one line throughout.

## Verification

- G1 HYGIENE: `git status --porcelain` empty at every commit and at the handback; `.agent/STOP` re-read from disk before C0a and at the handback, absent both times; branch feature/f086-release-capability; `git worktree list` one line.
- G2 TRANSPORT: `.remedy-wt/f086-r21.md`, committed `.agent/authored/f086-r21.md` and committed `.agent/last_block.md` byte-EQUAL at sha256 7c28f5c828d665ee5c10a52371ce5448c25e1efd24f57a7ee02d0de2aa5c807a, 29051 B over 351 lines.
- Constraint 7 re-measured on the committed C0a: 351 total / 215 prose / 136 slice incl. 16 marker lines — the block's own declaration, under D6's 490 and D5's 400.
- G3 PLAN: `.agent/plan.md` at ba8cf1b9 byte-equal to PLAN21 at sha256 b54a06d4a5f5ca611d463a20782fe7bb3590ec67b71e4367a2ecd28cafc7245e, 42 lines (< 50), contains `## Goal`, `## Next Steps`, `F086`.
- G4 THE LEDGER APPEND: pre-C2 blob is a byte-exact PREFIX of the post-C2 blob; the 4-line remainder equals blank + FIND0587 + blank + RECORD19 at sha256 837f39fd87b59a52fbedc4a6078b4b79e216b3b8b96bde0a0037e9950048263f.
- G5 LEDGER SETS: at a4fba89b BOTH extractions read 170 / 3 / 0 / 0 / 0 / 167 and their registered SETS are equal; registered symmetric difference against a7373e00 is exactly `['R-0587']`; CONTROL f0b27118..7b84524c reads `[]` registered while its resolved set gains `R-0584`.
- G6 THE R-0586 RULE: over the lines a4fba89b ADDS to `.agent/live_review.md`, backtick-quoted spans deleted first, `\bHEAD\b` reads 0 (0 before the strip too); RED CONTROL over `fd166295`'s added lines reads 3 with the same extractor. Binds the ledger commit only, by the block's own wording.
- G7 THE R-0587 RULE: at a7373e00, 17 headers, exactly one string occurring more than once and it is `Gate: R19 — the R18 entry.`; at a4fba89b, 18 headers, that duplicate SET UNCHANGED (constraint 3 forbids repairing it), `Gate: R21 — the R20 entry.` occurring 1x, LAST in the file, followed by ` R20 PASSED,`.
- G8 THE TWO PAIRS: printed `TO contains FROM: true` for both, hence both APPEND-shaped; each FROM occurs 1x at a7373e00 AND 1x at e1af7921 — the append form, not a defect — and all 14 + 18 TO-ONLY lines occur exactly 1x among C3's 32 added lines. ORDERED EQUALITY holds: e1af7921's file equals the a7373e00 blob with each FROM's single occurrence replaced by its TO and nothing else, sha256 085c6c830b898e7c3d37590430c943b007e5772b3735c37e5d62b42244c80461 over 805 lines, against 773 lines at a7373e00.
- G9 AIMED AND RENUMBERED NOTHING: `grep -c '^  21\. \*\*'` reads 1 and `grep -c '^  26\. \*\*'` reads 1; CHECK20TO is followed by `  21. **A baseline gate resolves its own paths at the base it names.** Finding R-0532. A` and CHECK26TO by `  Why this is on disk and not a habit: item 2 has recurred six times across`.
- G10 NO MARKER LEAKED: 0 lines beginning `<<<SLICE ` or `<<<END ` in `.agent/plan.md`, `.agent/live_review.md` and `docs/agents/planner_reviewer_prompt.md` at C4 — the three readings are in the round report, and `.agent/handoff.md`'s fourth reading is taken after C5.
- G11 SUITES, primary checkout, serially, the second started only after the first reported: `-q -rf` over the four state readers exit 0, 160 passed; then the golden-path canary exit 0, 42 passed. No suite reads the edited prompt file — its one hit under `tests/` is inside a `@pytest.mark.skip` reason string in `tests/test_agent_tooling.py`, whose test reads `.claude/agents/remedy-reviewer.md`.
- G12 CHANGE SET: `git diff --name-only a7373e00..HEAD` before C4 equals the constraint-2 list minus `.agent/handoff.md` AS SETS, symmetric difference empty; all five forbidden paths resolve at a7373e00 via `git ls-tree` and none appears in the range.
- G13 HISTORY: five single-parent commits, linear; `git reflog` over this round shows only `commit:` entries — no amend, rebase, reset, force-push. Insertions before C4: 351, 256, 16, 4, 32 — none over 500, no DECISION F104 D1 exemption invoked.
- G14 HANDBACK AND PR GATE: this file's `wc -l`, the seven-heading list, the C4-prefix-of-C5 measurement and the Open PR Gate output are in the round report; the gate printed `[]`.

NO CODE MOVED THIS ROUND and no test could have gone red on C3: the round writes state files and one docs file, so G8 and G9 are C3's entire evidence and the suites gate only the state texts. NO INSTALL RAN — `REMEDY_INSTALL_SMOKE` was set nowhere, no wheel was built, no venv created, no network reached.

## Authored-text proofs

- PLAN21, FIND0587, RECORD19, CHECK20FROM/TO, CHECK26FROM/TO and VERDICT were EXTRACTED programmatically from the COMMITTED `.agent/authored/f086-r21.md`, never retyped and never reformatted.
- Disk-to-disk: `.agent/plan.md` == PLAN21 (G3), `.agent/live_review.md`'s C2 remainder == blank + FIND0587 + blank + RECORD19 (G4), `docs/agents/planner_reviewer_prompt.md` == the base blob with both FROMs replaced by their TOs (G8), `.agent/handoff.md`'s C5 remainder == VERDICT (round report).
- The committed C0a is byte-equal to the `.remedy-wt/f086-r21.md` scratchpad the round was delegated from, and `.agent/last_block.md` mirrors the committed C0a read back with `git show` (G2).

## Deviations & assumptions

- No departure from the block's ordered commit sequence: C0a, C0b, C1, C2, C3 were committed in that order, one commit each, nothing extra, nothing dropped, nothing reordered. C4 is the commit writing this file and C5 appends VERDICT to it; the round report carries both, since a handoff cannot certify a commit that does not exist when it is written.
- ASSUMPTION, stated because it looks like a defect and is not: the duplicate header `Gate: R19 — the R18 entry.` remains on disk at `4dc7cbdf`. Constraint 3 and §3 item 20 forbid rewriting a landed record, and G7 gates that duplicate set as UNCHANGED. FIND0587 is the dated correction.
- No verdict on this round is written here. The worker reports what the gates measured; ruling is the reviewer's. The VERDICT text appended at C5 is the reviewer's own, applied byte-verbatim.

## Next

The reviewer re-runs G1-G14 over a7373e00..HEAD and rules on R21. Before authoring anything, re-read `.agent/STOP` from disk (Phase 1 rule 1 before rule 2). Per the VERDICT text C5 appends, the next session records R21 in `.agent/live_review.md` under the header `Gate: R22 — the R21 entry.`, then takes the integration gate.

## Reviewer's session verdict — authored by the reviewer, applied by the worker

Written because finding R-0571 is that a verdict issued and never put on disk
cannot be told apart from one never issued; appended so the next handback rewrite
cannot silently destroy it. Session of 2026-08-20, self-drive per
docs/agents/self_drive_protocol.md, resuming the branch at `bc85e5f7` and ending
at its declared round cap. The reviewer wrote nothing in the work tree, one
delegated worker per round made every commit, and every verdict below rests on
gates the reviewer re-executed over the committed diff, never on a handback.

| Round | Range | Verdict |
|---|---|---|
| R19 | 7b84524c..bc85e5f7 | PASS — one finding, R-0586, against the reviewer |
| R20 | bc85e5f7..a7373e00 | PASS — one finding, R-0587, against the reviewer |
| R21 | a7373e00..HEAD | verdict not yet on disk; see the last paragraph |

R19 was inherited ungated, so Phase 1 rule 4 reviewed it first. Its checklist edit
landed inside item 16 and moved nothing else, and the reviewer re-ran the claim
that commit rests on rather than repeating it. R20 is the round this feature
needed: `tests/test_install_smoke.py` exists, its pure helpers and its opt-in skip
are gated by tests that go red when the code under them is mutated, and its
install path is honestly declared as unproven rather than dressed as coverage.
Both rounds' defects were the reviewer's own text, not the worker's work, and both
were caught — R-0586 by the reviewer re-reading a landed record, R-0587 by the
WORKER, which applied a bad slice verbatim as its constraints required and then
declared it instead of quietly repairing it. That is the split working as designed.

WHAT THIS FEATURE STILL OWES: the integration gate, then closure. NO INSTALL HAS
BEEN PROVEN in this session or any other, and no round of this workflow can prove
one — DECISION F086 D4 records that with the measurement behind it, and closure
names it as unproven rather than counting a skipped test as coverage. The release
workflow has likewise never been dispatched.

R21 IS NOT A TERMINATOR — F086's pull request is created at closure, which has not
happened — so this session claims no §4 item 13 carve-out and leaves its last
verdict to be recorded. THE NEXT SESSION'S FIRST ACTIONS are Phase 1 rule 1, then
rule 2, then rule 4: review `a7373e00..HEAD` and record R21's verdict in
`.agent/live_review.md` as `Gate: R22 — the R21 entry.`, which is the header
shape §3 item 26 now binds.
