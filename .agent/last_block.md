── STEP R15 — F255 Teacher role ───────────────────────────────
Goal:        Register finding R-0607 against the R14 block's omitted canary,
             persist the R14 verdict to the finding ledger, and advance the plan.
             This round BUILDS NOTHING: the session that reviewed R14 reached its
             limit, and a PASS that lives only in a chat window is a verdict this
             project cannot audit later (DECISION F085 D9).

Bundle:      C0a save this block · C0b mirror it · C1 the plan, FIRST · C2
             register R-0607 · C3 record the R14 verdict · C4 the handback, then
             push.

Change:      Exactly these paths, in this order, one commit each.
             C0a `.agent/authored/f255-r15.md`
             C0b `.agent/last_block.md`
             C1  `.agent/plan.md`
             C2  `.agent/live_review.md`
             C3  `.agent/live_review.md`
             C4  `.agent/handoff.md`
             Nothing else is created, modified, deleted or staged. NO source file
             and NO test file is touched this round. These paths are PRESENT at
             the base `501c08a7` and must stay untouched:
             `packages/orchestration/teacher_spend.py`,
             `tests/orchestration/test_teacher_spend.py`,
             `packages/orchestration/token_ledger.py`, `.agent/decisions.md`.

Constraints:
1. NO SLICE IS EDITED. Every text between the SLICE and END markers is applied
   byte for byte. A slice you believe is wrong is applied anyway and DECLARED in
   the handback; you never repair it silently. Marker lines never reach a target.
2. TRANSPORT. `.remedy-wt/f255-r15.md` is this block on disk. C0a copies that
   FILE to `.agent/authored/f255-r15.md` — copy it, never retype it — and C0b
   copies the same file to `.agent/last_block.md`. Prove all three byte-EQUAL;
   the reviewer stated the expected digest when it delegated, and that digest
   cannot appear in this file because this file is what it digests.
3. THE PLAN COMES FIRST. Findings R-0377, R-0491 and R-0548 are OPEN and all rule
   that the `.agent/plan.md` update is the FIRST substantive commit of a round
   with substance to record.
4. THE FINDING PERSISTS BEFORE THE VERDICT. C2 registers R-0607 and C3 records
   the R14 verdict, in that order (§4.4), so a session that dies between them
   leaves the finding on disk rather than losing it.
5. BOTH APPENDS ARE BLANK-SEPARATED (R-0578): FIND0607 at C2 and RECORDR14 at C3
   are each appended preceded by exactly one blank line. This round registers
   R-0607 and resolves nothing: registered goes 182 to 183, resolved stays 3.
6. THE TWO APPENDED SLICES, FIND0607 AND RECORDR14, ARE EACH SINGLE-PARAGRAPH —
   the reviewer measured each for an interior blank line and found none — so the
   LAST-UNIT paragraph reading G6 orders is exact for each of them. That is the
   counter-measure R-0606 names. PLAN255R15 is a full replacement, not an append,
   so no paragraph reading is ordered or owed for it.
7. THIS ROUND CONTAINS NO FROM/TO PAIR and creates no file outside `.agent/`, so
   no containment reading and no FROM-zero count is owed (§4.9, R-0207).
8. YOU NEVER WRITE A `Done:` OR A `Landed:` PARAGRAPH.
9. `.agent/STOP` is read from disk before C0a. If it exists, stop and write the
   handback instead.
10. `git status --porcelain` is EMPTY after every commit. No worktree is created,
    and the primary checkout is never mutated to take a reading — use
    `git show <sha>:<path>`.
11. YOU DO NOT WAIT ON ANY CI RUN and you report no run's conclusion.

<<<SLICE PLAN255R15
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
R15: a RECORD round. It registers finding R-0607 against the R14 block's omitted
canary, persists the R14 verdict, and advances this plan. It builds nothing — the
session that reviewed R14 reached its limit, and a verdict that lives only in a
chat window is a verdict this project cannot audit.

## Next Steps
1. R16 FINISHES T004, the model half of Stage 2: `remedy teach ask` on the CLI
   over `teacher_qa.build_teacher_context`, the teacher model call through
   `resolve_role_config("teacher")`, the honest refusal when no model is
   configured, and the spend row written through the `teacher_spend` seam R13
   built. There is NO generic text-completion provider in this repository today:
   the providers under `packages/providers/` are role-specific and schema-bound,
   so R16 must DESIGN the teacher's model seam rather than discover one, and
   that design is the round's first and largest risk.
2. The INTEGRATION GATE round follows T004 — the full suite, per
   docs/agents/integration_gate.md — because T002 and T003 touch the CLI
   catalog, which the parser and the help renderer both read.
3. The CLOSURE round follows, per docs/roadmap/STATUS_closure_protocol.md:
   evidence job, fresh review zip, the STATUS line, and the pull request.

## Risks
- `teacher_spend.record_teacher_question` HAS NO CALLER YET. R13 built and
  red-proofed the seam; until R16 wires it, F255's cost acceptance is unmet.
- THE READ-ONLY PROOF COVERS NARRATE ONLY; `teach ask` needs its own, and it
  must exclude the ledger row R13 introduced by name rather than by silence.
<<<END PLAN255R15
<<<SLICE FIND0607
- R-0607 — Low — A BLOCK ORDERED NO CANARY, SO A ROUND HANDED BACK WITHOUT THE ONE GATE EVERY HANDBACK OWES. docs/agents/planner_reviewer_prompt.md §3 verification tier 2 reads "every handback additionally runs the golden-path smoke", with no carve-out for a round that builds nothing, and the F255 R14 block's G1 through G9 order no pytest command at all — the reviewer treated "this round touches only `.agent/`" as though it meant "this round can break nothing". It does not: `.agent/plan.md`, `.agent/live_review.md` and `.agent/context.md` are READ by tests/orchestration/test_test_runner.py, tests/ui_server/test_dashboard_contract.py, tests/regression/test_resource_safety.py and tests/orchestration/test_integrity_gate.py, which is exactly the class §4.11 exists to warn about and exactly why the comparable R12 record round DID order both the state-reader four and the canary. The omission cost nothing this time and that is luck rather than design: the reviewer ran both suites itself at `501c08a7` after the handback and measured exit 0 at 160 passed and exit 0 at 42 passed, so no contract test was in fact broken. FIX: a block's done-when carries the canary UNCONDITIONALLY, and a block whose change set includes any `.agent/` state file also carries the four state-reader files, both stated as gates rather than inferred from the change set; a round that builds nothing is not a round that verifies nothing. This rule is NOT yet in docs/agents/planner_reviewer_prompt.md §3; the docs round that promotes it into the pre-emission checklist is the round that closes this finding.
<<<END FIND0607
<<<SLICE RECORDR14
Gate: R15 — the R14 entry. R14 PASSED. ONE finding is registered this round, R-0607, against the R14 BLOCK's omitted canary and NOT against the round's work, which is clean. R14 was a RECORD round that built nothing, and every gate its block ordered was RE-EXECUTED by the reviewer over `28e6058f..501c08a7` rather than read from the handback; every number below is the reviewer's own. THE TRANSPORT HELD IN THE PRIMARY FORM: `.remedy-wt/f255-r14.md`, the committed `.agent/authored/f255-r14.md` at `6fb98520` and the committed `.agent/last_block.md` at `e007a6a8` are byte-EQUAL at sha256 8f75de11bdcf8b41f77874884a80e8ccd415572e526923752cf40d4726b97cb9 over 20517 B and 190 lines, the digest stated at delegation. THREE SLICES, a count taken from the reviewer's own ordered extraction of the committed blob and agreeing with the worker's independent count, newline convention NEWLINE-INCLUDED: PLAN255R14 sha256 3d9d7d9e983d6c9f20591e2af19b52242351ab542cdfa6bace732ef8fe1e9833 over 2465 B and 42 lines; FIND0606 sha256 303f5618cd6ba5cbcff07998fb0c5cfe900d2a90197d7e34c0c08b8c449bc4dc over 2129 B and 1 line; RECORDR13 sha256 635f596fcd560b6838e7a70ecc35d1b2917a33e38afe80d39348e50988c42e8f over 6149 B and 1 line. THE PLAN LANDED FIRST AGAIN: `.agent/plan.md` at `bd8470f5` byte-equals PLAN255R14 over 2465 B and 42 lines, under the 50-line cap, carrying `## Goal` once, `## Next Steps` once and the F-id F255, and it is the first commit after the two block-save commits. THE FINDING PERSISTED BEFORE THE VERDICT, which is what §4.4 asks and what makes a dying session lose nothing: the `.agent/live_review.md` blob at `28e6058f` is a byte-exact prefix of the blob at `5dcded51` whose remainder equals one newline followed by FIND0606, and THAT blob is in turn a byte-exact prefix of the blob at `60a1c978` whose remainder equals one newline followed by RECORDR13 — two nested prefix readings, each compared as bytes against the reviewer's own extraction. THE SETS MOVED BY EXACTLY ONE REGISTRATION AND NOTHING ELSE: 181 registered / 3 resolved / 178 open / 0 line-anchored `Landed:` at `28e6058f`, then 182 / 3 / 179 / 0 at BOTH `5dcded51` and `60a1c978`, the second commit adding a `Gate:` paragraph, which is neither kind of line. `R-0606` occurs 0x at `28e6058f` and its registration line occurs 1x at `60a1c978`; `Gate: R15 — the R14 entry.` did not exist anywhere before this paragraph, and `Gate: R14 — the R13 entry.` occurs 1x, sits last among the fourteen lines beginning `Gate: R` as of `60a1c978`, and all fourteen header keys are distinct. R-0606 IS THE ROUND'S OWN LESSON APPLIED TO ITSELF: the block measured both appended slices for an interior blank line, found none, and therefore ordered the LAST-UNIT paragraph reading that R-0606 had just shown to be unmeetable for a multi-paragraph slice — the worker re-measured that property rather than trusting the constraint, and both readings hold with one-byte negative controls rejected under each. THE RANGE AND THE HISTORY HOLD: five paths over six single-parent commits, all five under `.agent/`; per-commit insertions 190, 111, 13, 2, 2 and 27, every one under the 500 cap; every `+/-` cell of the handback's `## Commits` table is byte-identical to `git diff --numstat`; all four paths the block named untouched — `packages/orchestration/teacher_spend.py`, `tests/orchestration/test_teacher_spend.py`, `packages/orchestration/token_ledger.py` and `.agent/decisions.md` — are PRESENT at `28e6058f` and ABSENT from the range; and zero lines beginning `<<<SLICE ` or `<<<END ` appear in any written file. THE HANDBACK ITSELF MEASURES CLEAN: 66 lines at `501c08a7`, inside the 100-line allowance its six-commit table earns, no trailing whitespace on any line, and all seven mandated headings in the order docs/agents/handback_template.md gives them. C4'S OWN REFLOG ENTRY IS MEASURED HERE, which is what R-0494 asks of the next gate: at `501c08a7` the round has made 6 commits and its reflog entries whose operation prefix reads exactly `commit` number 6, with 0 whose prefix contains amend, reset, rebase or cherry. THE PUSH LANDED: `origin/feature/f255-teacher-role` resolves to `501c08a7`, the commit the branch holds. WHAT THE R14 BLOCK GOT WRONG IS R-0607: it ordered no pytest command at all, so the canary that docs/agents/planner_reviewer_prompt.md §3 owes on EVERY handback did not run inside the round. The reviewer ran it afterwards at `501c08a7`, serially in the primary checkout — the four state-reader files exit 0 at 160 passed and the canary exits 0 at 42 passed — so nothing was broken and the omission cost only the proof, which is the cheapest possible version of this mistake and still a mistake.
<<<END RECORDR14

Done when:
G1 HYGIENE. `.agent/STOP` read from disk before C0a and reported absent or
   present; branch is feature/f255-teacher-role; `git status --porcelain` EMPTY
   after every commit and at the handback; `git worktree list` reports the
   primary checkout alone.
G2 TRANSPORT. Report the sha256 and the byte and line counts of
   `.remedy-wt/f255-r15.md`, of `.agent/authored/f255-r15.md` at C0a and of
   `.agent/last_block.md` at C0b, and state whether all three are EQUAL.
G3 SLICES EXTRACTED, NEVER RETYPED. Extract each slice from the COMMITTED
   `.agent/authored/f255-r15.md` by its markers and report each slice's name,
   sha256, byte count and line count, naming the newline convention (R-0600).
   Report the number of slices as a COUNT YOU TOOK FROM THAT LISTING; this block
   states no numeral of its own for it (R-0604, checklist item 11).
G4 THE PLAN, FIRST. `.agent/plan.md` at C1 byte-equals PLAN255R15; report its
   sha256, byte and line counts, that the line count is under 50, and that
   `## Goal`, `## Next Steps` and a roadmap F-id all occur in it. Report also
   that C1 is the FIRST commit of this round other than C0a and C0b.
G5 THE FINDING REGISTERED. Over `.agent/live_review.md`, report: the base blob at
   `501c08a7` is a byte-exact PREFIX of the C2 blob; the remainder's sha256, byte
   and line counts; that the remainder equals one newline followed by FIND0607;
   and that the byte after that leading newline is not a newline.
G6 THE R14 VERDICT RECORDED. Report the same three readings for C3 over the C2
   blob — prefix, remainder equal to one newline followed by RECORDR14, and the
   separator — AND, for EACH of C2 and C3, a SECOND, INDEPENDENT blank-line
   paragraph split of that commit's blob whose LAST unit is the slice that commit
   appended, giving that unit's sha256 under BOTH newline conventions with the
   byte count of each. Constraint 6 records the measurement that makes the
   LAST-UNIT reading exact here; re-measure it rather than trusting it. Run a
   negative control for each: one character of the expected remainder mutated,
   rejected by BOTH readings.
G7 THE SETS AND THE KEYS. Report registered / resolved / open / line-anchored
   `Landed:` at `501c08a7`, at C2 and at C3, the registered count being lines
   matching `^- R-\d+ — ` and the resolved count lines matching `^Done: R-\d+ — `:
   the reviewer measured 182 / 3 / 179 / 0 at `501c08a7`, C2 owes 183 / 3 / 180 /
   0 because it adds one registered line, and C3 owes the same as C2 because a
   `Gate:` paragraph adds neither kind of line. Report that `R-0607` occurs 0x at
   `501c08a7`, that `Gate: R15 — the R14 entry.` occurs 1x at C3 and is the LAST
   line beginning `Gate: R`, and that every such header key is distinct. COUNT
   HEADERS LINE-ANCHORED, never as substrings: the bare prefix `Gate: R15` also
   occurs 3 times at `501c08a7` inside the BODY of finding R-0394 as ordinary
   prose, so a substring count reads those too, while the full header string
   above occurs 0 times there (R-0584, a guard that cannot tell a quotation from
   a use is satisfied by the quotation).
G8 THE CANARY AND THE STATE READERS, WHICH R-0607 EXISTS BECAUSE THE R14 BLOCK
   OMITTED. This round rewrites `.agent/` state, so both gate. Run them serially
   in the PRIMARY checkout, never two pytest processes at once, and report the
   exact command, exit code and tail of each:
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
   The reviewer measured exit 0 at 160 passed and exit 0 at 42 passed, both at
   `501c08a7` in the primary checkout.
G9 CHANGE SET, HISTORY AND CAPS. Report `git diff --name-only 501c08a7..HEAD` and
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
G10 NO MARKER LEAKED, AND THE PUSH. Report the count of LINES beginning with the
   SLICE or END marker prefixes in `.agent/plan.md` at C1, `.agent/live_review.md`
   at C3 and `.agent/handoff.md` at C4 — every count 0. Then, after C4,
   `git push` and report its real output. Do NOT create a pull request and do NOT
   wait on the CI run the push starts (constraint 11).

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             all seven mandated headings in the template's order, the item-status
             table for the C0a..C4 bundle, the `## Commits` table G9 pins, and one
             LINE per gate rather than its transcript (R-0582). Its `## Next`
             section names the next session's FIRST action as Phase 1 rule 1, the
             `.agent/STOP` re-read, and its SECOND as R16, which finishes T004 —
             `remedy teach ask` on the CLI, the teacher model call, the honest
             refusal with no model configured, and the spend row written through
             the `teacher_spend` seam R13 built — stating plainly that NO generic
             text-completion provider exists in this repository today, so R16
             must design that seam rather than look for one. It states that R14
             PASSED, that its verdict and finding R-0607 are now ON DISK at C3
             and C2, and that R15 ITSELF IS THE ROUND WHOSE VERDICT IS NOT ON
             DISK — the session ended here, so R15 awaits review and the next
             session's first block records it. It states that no pull request is
             open. Transcripts go in the round report. The handback carries this
             Fortschritt line verbatim (R-0418):
             Fortschritt: ~80 % (T001, T002 and T003 COMPLETE · T004 split by the
             reviewer at R13 — the billing ruling and the spend writer are built,
             red-proofed and REVIEWED, and the seam has no caller yet; the model
             call and the CLI are R16 · integration gate and closure remain) —
             Schätzung
──────────────────────────────────────────────────────────────
