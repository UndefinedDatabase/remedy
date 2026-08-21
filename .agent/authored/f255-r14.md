── STEP R14 — F255 Teacher role ───────────────────────────────
Goal:        Register finding R-0606 against the R13 block's own G6, persist the
             R13 verdict to the finding ledger, and advance the plan. This round
             BUILDS NOTHING: the session that reviewed R13 reached its limit, and
             a PASS that lives only in a chat window is a verdict this project
             cannot audit later (DECISION F085 D9).

Bundle:      C0a save this block · C0b mirror it · C1 the plan, FIRST · C2
             register R-0606 · C3 record the R13 verdict · C4 the handback, then
             push.

Change:      Exactly these paths, in this order, one commit each.
             C0a `.agent/authored/f255-r14.md`
             C0b `.agent/last_block.md`
             C1  `.agent/plan.md`
             C2  `.agent/live_review.md`
             C3  `.agent/live_review.md`
             C4  `.agent/handoff.md`
             Nothing else is created, modified, deleted or staged. NO source file
             and NO test file is touched this round. These paths are PRESENT at
             the base `28e6058f` and must stay untouched:
             `packages/orchestration/teacher_spend.py`,
             `tests/orchestration/test_teacher_spend.py`,
             `packages/orchestration/token_ledger.py`, `.agent/decisions.md`.

Constraints:
1. NO SLICE IS EDITED. Every text between the SLICE and END markers is applied
   byte for byte. A slice you believe is wrong is applied anyway and DECLARED in
   the handback; you never repair it silently. Marker lines never reach a target.
2. TRANSPORT. `.remedy-wt/f255-r14.md` is this block on disk. C0a copies that
   FILE to `.agent/authored/f255-r14.md` — copy it, never retype it — and C0b
   copies the same file to `.agent/last_block.md`. Prove all three byte-EQUAL;
   the reviewer stated the expected digest when it delegated, and that digest
   cannot appear in this file because this file is what it digests.
3. THE PLAN COMES FIRST. Findings R-0377, R-0491 and R-0548 are OPEN and all rule
   that the `.agent/plan.md` update is the FIRST substantive commit of a round
   with substance to record.
4. THE FINDING PERSISTS BEFORE THE VERDICT. C2 registers R-0606 and C3 records
   the R13 verdict, in that order (§4.4), so a session that dies between them
   leaves the finding on disk rather than losing it.
5. BOTH APPENDS ARE BLANK-SEPARATED (R-0578): FIND0606 at C2 and RECORDR13 at C3
   are each appended preceded by exactly one blank line. This round registers
   R-0606 and resolves nothing: registered goes 181 to 182, resolved stays 3.
6. THE TWO APPENDED SLICES, FIND0606 AND RECORDR13, ARE EACH SINGLE-PARAGRAPH —
   the reviewer measured each for an interior blank line and found none — so the
   LAST-UNIT paragraph reading G6 orders is exact for each of them. That
   measurement is the counter-measure R-0606 itself names, applied in the block
   that registers it. PLAN255R14 is a full replacement, not an append, so no
   paragraph reading is ordered or owed for it.
7. THIS ROUND CONTAINS NO FROM/TO PAIR and creates no file outside `.agent/`, so
   no containment reading and no FROM-zero count is owed (§4.9, R-0207).
8. YOU NEVER WRITE A `Done:` OR A `Landed:` PARAGRAPH.
9. `.agent/STOP` is read from disk before C0a. If it exists, stop and write the
   handback instead.
10. `git status --porcelain` is EMPTY after every commit. No worktree is created,
    and the primary checkout is never mutated to take a reading — use
    `git show <sha>:<path>`.
11. YOU DO NOT WAIT ON ANY CI RUN and you report no run's conclusion.

<<<SLICE PLAN255R14
# Plan — F255 Teacher role

Branch: feature/f255-teacher-role, cut from `main` at b35d350b, the merge commit
of pull request #207. No pull request is open for this branch; on this project
the PR is created by the closure round.
`.agent/live_review.md` is the source of truth for the open set, for the next
free finding id and for the round map; this file repeats none of them.

## Goal
A fourth configured role, `teacher`, that narrates a running mission and answers
operator questions about the operator's own code, and never influences the run.
DONE when passive narration keyed to an enumerated set of ledger events (Stage 1,
deterministic templates, zero tokens) and on-demand Q&A (Stage 2, through the
teacher role's own model) both work, the three grounding sources are never mixed
silently, teacher spend is reported as its own role in the F103 ledger, and the
read-only invariant is proven behaviourally.

## Current Step
R14: a RECORD round. It registers finding R-0606 against the R13 block's own G6,
persists the R13 verdict to `.agent/live_review.md`, and advances this plan. It
builds nothing — the session that reviewed R13 reached its limit, and a verdict
that lives only in a chat window is a verdict this project cannot audit.

## Next Steps
1. R15 FINISHES T004, the model half of Stage 2: `remedy teach ask` on the CLI
   over `teacher_qa.build_teacher_context`, the teacher model call through
   `resolve_role_config("teacher")`, the honest refusal when no model is
   configured, and the spend row written through the `teacher_spend` seam R13
   built. There is NO generic text-completion provider in this repository today:
   the providers under `packages/providers/` are role-specific and
   schema-bound, so R15 must design the teacher's model seam, not discover one.
2. The INTEGRATION GATE round follows T004 — the full suite, per
   docs/agents/integration_gate.md — because T002 and T003 touch the CLI
   catalog, which the parser and the help renderer both read.
3. The CLOSURE round follows, per docs/roadmap/STATUS_closure_protocol.md:
   evidence job, fresh review zip, the STATUS line, and the pull request.

## Risks
- `teacher_spend.record_teacher_question` HAS NO CALLER YET. R13 built and
  red-proofed the seam; until R15 wires it, F255's cost acceptance is unmet.
- THE READ-ONLY PROOF COVERS NARRATE ONLY; `teach ask` needs its own, and it
  must exclude the ledger row R13 introduced by name rather than by silence.
<<<END PLAN255R14
<<<SLICE FIND0606
- R-0606 — Low — A GATE ORDERED A PARAGRAPH SPLIT WHOSE LAST UNIT IS A MULTI-PARAGRAPH SLICE, WHICH NO RUN CAN PRODUCE. G6 of the F255 R13 block ordered, over `.agent/decisions.md` at C3, "the SAME prefix, remainder and separator readings G5 names", and G5's second, independent reading is a blank-line paragraph split whose LAST unit IS the appended slice. That shape is right for RECORDR12, which is one paragraph by construction, and unmeetable for DECISION255D7, which contains blank lines and therefore becomes the last SIX units of any blank-line split — so the clause was satisfiable by no run at all, in the safe-looking direction, exactly the vacuous-gate class of R-0438 arriving through a slice's SHAPE rather than through a missing path. The reviewer wrote G6 by pointing at G5 instead of re-reading G5 against the slice G6 governs, which is why one clause was correct for one slice and impossible for the other while both looked identical on the page. Nothing was lost: the worker applied the slice verbatim, measured the LAST-K-UNITS reading with K = 6 derived by splitting the slice itself, ran two one-byte negative controls that the prefix reading and both K-unit readings reject, reported the literal last unit as well — 191 B, sha256 e5a22db464395e26b5c08540009567eb84209cb0842ed019a900bd5a6fa71bde, the slice's own closing paragraph — and declared the contradiction rather than repairing it silently, which is the R-0252 shape of a round spending a declared deviation to prove a reviewer mistake. FIX: a block states an independent paragraph reading as LAST-K UNITS, with K derived by splitting the slice, unless the block has MEASURED that slice to be a single paragraph, in which case a LAST-UNIT clause is exact and is preferred; and a gate that reuses another gate's readings by reference names the slice each reading is taken over, because a reading is a property of the pair of gate and slice and never of the gate alone. This rule is NOT yet in docs/agents/planner_reviewer_prompt.md §3; the docs round that promotes it into the pre-emission checklist is the round that closes this finding.
<<<END FIND0606
<<<SLICE RECORDR13
Gate: R14 — the R13 entry. R13 PASSED. ONE finding is registered this round, R-0606, against the R13 BLOCK's own G6 and NOT against the round's work, which is clean. Every gate the R13 block ordered was RE-EXECUTED by the reviewer over `8d8e7a5c..28e6058f` rather than read from the handback, and every number below is the reviewer's own. THE TRANSPORT HELD IN THE PRIMARY FORM: `.remedy-wt/f255-r13.md`, the committed `.agent/authored/f255-r13.md` at `fa934355` and the committed `.agent/last_block.md` at `e4d89120` are byte-EQUAL at sha256 d1a48700a8e9467719ed0081ad96936384c1f52325349c4df14114a7b83da6fd over 30557 B and 489 lines, the digest stated at delegation. SEVEN SLICES, a count taken from the reviewer's own ordered extraction of the committed blob and agreeing with the worker's independent count, newline convention NEWLINE-INCLUDED: PLAN255R13 323dd245 2429 B 42 lines; RECORDR12 d80e2dda 5094 B 1 line; DECISION255D7 b33a7e1a 2341 B 36 lines; LEDGERFROM 28123d19 1157 B 16 lines; LEDGERTO b00e8a04 1659 B 22 lines; TEACHSPEND a693df17 3315 B 90 lines; TEACHSPENDTEST 40e5ebc5 3531 B 116 lines — each prefix being the first 8 hex of the sha256 the R13 handback states in full at `28e6058f`. THE PLAN LANDED FIRST AGAIN: `.agent/plan.md` at `562bb67e` byte-equals PLAN255R13 over 2429 B and 42 lines, under the 50-line cap, carrying `## Goal` once, `## Next Steps` once and the F-id F255, and it is the first commit after the two block-save commits. THE TWO APPENDS ARE PREFIX-CLEAN: the `.agent/live_review.md` blob at `8d8e7a5c` is a byte-exact prefix of the blob at `8366e85a` whose remainder equals one newline followed by RECORDR12, and the `.agent/decisions.md` blob at `8d8e7a5c` is a byte-exact prefix of the blob at `f185dc77` whose remainder equals one newline followed by DECISION255D7, both compared as bytes by the reviewer against its own extraction. THE SETS DID NOT MOVE, as a `Gate:` paragraph must not move them: 181 registered / 3 resolved / 178 open / 0 line-anchored `Landed:` at BOTH `8d8e7a5c` and `8366e85a`; `Gate: R13 — the R12 entry.` occurs 1x, sits last among the thirteen lines beginning `Gate: R`, and all thirteen header keys are distinct. `## DECISION F255 D7` occurs 0x at `8d8e7a5c` and 1x at `f185dc77`, where all 79 lines beginning `## DECISION ` are distinct. THE ONE PAIR APPLIED CLEANLY AND TOUCHED NOTHING ELSE: in `packages/orchestration/token_ledger.py` LEDGERFROM occurs 1x at `8d8e7a5c` and 0x at `573a80c3` — the FROM-zero count a REWRITE owes — LEDGERTO occurs 0x then 1x, the file grows 1669 to 1675 lines, and the base blob with LEDGERFROM replaced once by LEDGERTO is byte-IDENTICAL to the C4 blob, which is the strongest available statement that the commit changed the pair and nothing besides. THE TWO FILES WERE CREATED, NOT EDITED, and each is the authored bytes: `packages/orchestration/teacher_spend.py` and `tests/orchestration/test_teacher_spend.py` are both ABSENT at `8d8e7a5c` under `git ls-tree` and both PRESENT at `b3b76f84`, each byte-EQUAL to its slice at 90 and 116 lines, numstat 90/0 and 116/0. THE ROUND GATE HOLDS, re-run serially by the reviewer in the primary checkout, never two pytest processes at once: the new `test_teacher_spend.py` exits 0 at 5 passed, `test_token_ledger.py` exits 0 at 112 passed, the three repo-wide glob sweeps exit 0 at 132 passed — the same 132 as at the base, so the new module under `packages/` trips none of them — the four state-reader files exit 0 at 160 passed, the canary exits 0 at 42 passed, and scoped ruff over the three touched paths exits 0 at `All checks passed!`. THE FIVE RED CONTROLS BEHIND THE NEW SUITE WERE RUN BY THE REVIEWER BEFORE DELEGATION, in a disposable worktree since removed: carrying the call_id into `task_id` gives 1 failed / 4 passed, defaulting the usage counts to zero gives 1 failed / 4 passed, pinning the cost basis to unknown gives 1 failed / 4 passed, attributing the row to a mission role gives 2 failed / 3 passed, and a constant call_id gives 1 failed / 4 passed — so the NULL task_id, the honest NULL counts, the reported-cost basis, the role attribution and the per-question identity are each a real tripwire, and the module restored byte-identically to 5 passed afterwards. THE RANGE AND THE HISTORY HOLD: nine paths over nine single-parent commits; per-commit insertions 489, 427, 13, 2, 37, 14, 206, 48 and 1, every one under the 500 cap; every `+/-` cell of the handback's `## Commits` table is byte-identical to `git diff --numstat`; all four paths the block named untouched are PRESENT at `8d8e7a5c` and ABSENT from the range; and zero lines beginning `<<<SLICE ` or `<<<END ` appear in any of the seven written files. THE HANDBACK ITSELF MEASURES CLEAN: 82 lines at `28e6058f`, inside the 100-line allowance its nine-commit table earns, no trailing whitespace on any line, all seven mandated headings in the order docs/agents/handback_template.md gives them, and the Fortschritt line carried verbatim from the block. THE ADDED COMMIT IS THE ROUND CORRECTING ITSELF, NOT REWRITING HISTORY: C6 as first pushed said "four scratch files" where five existed, and rather than amend, the worker added C6b, which rewrites `.agent/handoff.md` to DROP the numeral instead of restating it — the R-0402 counter-measure applied correctly, since correcting a count is where the next wrong count lands (R-0486). The reviewer read C6b's diff: it is a single line replaced, and the reflog carries no amend, reset, rebase or cherry entry. C6 AND C6b'S OWN REFLOG ENTRIES ARE MEASURED HERE, which is what R-0494 asks of the next gate: at `28e6058f` the round has made 9 commits and its reflog entries whose operation prefix reads exactly `commit` number 9, with 0 whose prefix contains amend, reset, rebase or cherry. THE PUSH LANDED: `origin/feature/f255-teacher-role` resolves to `28e6058f`, the commit the branch holds. WHAT R13 DOES NOT YET DO, stated so no later reader mistakes a green gate for a finished feature: `teacher_spend.record_teacher_question` has NO caller — R13 built the seam and R15 wires it — so F255's cost acceptance is proven possible and not yet met.
<<<END RECORDR13

Done when:
G1 HYGIENE. `.agent/STOP` read from disk before C0a and reported absent or
   present; branch is feature/f255-teacher-role; `git status --porcelain` EMPTY
   after every commit and at the handback; `git worktree list` reports the
   primary checkout alone.
G2 TRANSPORT. Report the sha256 and the byte and line counts of
   `.remedy-wt/f255-r14.md`, of `.agent/authored/f255-r14.md` at C0a and of
   `.agent/last_block.md` at C0b, and state whether all three are EQUAL.
G3 SLICES EXTRACTED, NEVER RETYPED. Extract each slice from the COMMITTED
   `.agent/authored/f255-r14.md` by its markers and report each slice's name,
   sha256, byte count and line count, naming the newline convention (R-0600).
   Report the number of slices as a COUNT YOU TOOK FROM THAT LISTING; this block
   states no numeral of its own for it (R-0604, checklist item 11).
G4 THE PLAN, FIRST. `.agent/plan.md` at C1 byte-equals PLAN255R14; report its
   sha256, byte and line counts, that the line count is under 50, and that
   `## Goal`, `## Next Steps` and a roadmap F-id all occur in it. Report also
   that C1 is the FIRST commit of this round other than C0a and C0b.
G5 THE FINDING REGISTERED. Over `.agent/live_review.md`, report: the base blob at
   `28e6058f` is a byte-exact PREFIX of the C2 blob; the remainder's sha256, byte
   and line counts; that the remainder equals one newline followed by FIND0606;
   and that the byte after that leading newline is not a newline.
G6 THE R13 VERDICT RECORDED. Report the same three readings for C3 over the C2
   blob — prefix, remainder equal to one newline followed by RECORDR13, and the
   separator — AND, for EACH of C2 and C3, a SECOND, INDEPENDENT blank-line
   paragraph split of that commit's blob whose LAST unit is the slice that
   commit appended, giving that unit's sha256 under BOTH newline conventions with
   the byte count of each. Constraint 6 records the measurement that makes the
   LAST-UNIT reading exact here. Run a negative control for each: one character
   of the expected remainder mutated, rejected by BOTH readings.
G7 THE SETS AND THE KEYS. Report registered / resolved / open / line-anchored
   `Landed:` at `28e6058f`, at C2 and at C3, the registered count being lines
   matching `^- R-\d+ — ` and the resolved count lines matching `^Done: R-\d+ — `:
   the reviewer measured 181 / 3 / 178 / 0 at `28e6058f`, C2 owes 182 / 3 / 179 /
   0 because it adds one registered line, and C3 owes the same as C2 because a
   `Gate:` paragraph adds neither kind of line. Report that `R-0606` occurs 0x at
   `28e6058f`, that `Gate: R14 — the R13 entry.` occurs 1x at C3 and is the LAST
   line beginning `Gate: R`, and that every such header key is distinct.
G8 CHANGE SET, HISTORY AND CAPS. Report `git diff --name-only 28e6058f..HEAD` and
   state that it equals the Change list with no path on either side alone. Report
   that each path the Change section names untouched is PRESENT at the base and
   absent from the range; that every commit in the range has one parent; and each
   commit's insertion column from `git diff --numstat`, every one under 500, with
   the same `+/-` cells appearing byte-identically in the handback's `## Commits`
   table (checklist item 28). C4's own cell and the complete change set belong to
   the round report.
   THE REFLOG IS TWO MEASURED CLAIMS, NOT ONE UNIVERSAL (R-0601), AND NEITHER IS
   A TOTAL (R-0605): report the count of this round's reflog entries whose
   OPERATION PREFIX — the text before the first colon of
   `git reflog --format=%gs` — reads exactly `commit`, WITH the commit it was
   taken at and the number of commits the round has made AT THAT MOMENT, and
   state that the two are equal. State no total: C4 is unwritten as this is
   composed, so the reviewer measures its entry at the next gate (R-0494). Report
   also the count whose prefix contains `amend`, `reset`, `rebase` or `cherry`,
   which must be 0.
G9 NO MARKER LEAKED, AND THE PUSH. Report the count of LINES beginning with the
   SLICE or END marker prefixes in `.agent/plan.md` at C1, `.agent/live_review.md`
   at C3 and `.agent/handoff.md` at C4 — every count 0. Then, after C4,
   `git push` and report its real output. Do NOT create a pull request and do NOT
   wait on the CI run the push starts (constraint 11).

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             all seven mandated headings in the template's order, the item-status
             table for the C0a..C4 bundle, the `## Commits` table G8 pins, and one
             LINE per gate rather than its transcript (R-0582). Its `## Next`
             section names the next session's FIRST action as Phase 1 rule 1, the
             `.agent/STOP` re-read, and its SECOND as R15, which finishes T004 —
             `remedy teach ask` on the CLI, the teacher model call, the honest
             refusal with no model configured, and the spend row written through
             the `teacher_spend` seam R13 built, noting that no generic
             text-completion provider exists in this repository today. It states
             that R13 PASSED, that its verdict and finding R-0606 are now ON DISK
             at C3 and C2, that R14 awaits review, and that no pull request is
             open. Transcripts go in the round report. The handback carries this
             Fortschritt line verbatim (R-0418):
             Fortschritt: ~80 % (T001, T002 and T003 COMPLETE · T004 split in two
             by the reviewer at R13 — the billing ruling and the spend writer are
             built, red-proofed and REVIEWED; the model call and the CLI are R15
             and the seam has no caller yet · integration gate and closure
             remain) — Schätzung
──────────────────────────────────────────────────────────────
