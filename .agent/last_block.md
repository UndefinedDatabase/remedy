── STEP R6 — F255 Teacher role ────────────────────────────────
Goal:        Register R-0604, record the R5 verdict, and BUILD the first half of
             T001: the role name `teacher` joins `KNOWN_ROLES`, and the frozen
             pin that guards that tuple is renamed and extended in the SAME
             commit. This is the first round of this feature to touch source.
             `ConventionsRole`, the conventions document and the `teacher.model`
             config key are T001's second half and belong to R7.

Bundle:      C0a save this block · C0b mirror it · C1 register R-0604 · C2
             record the R5 verdict · C3 the role vocabulary and its pin,
             together · C4 the plan · C5 the handback, then push.

Change:      Exactly these paths, in this order, one commit each.
             C0a `.agent/authored/f255-r6.md`
             C0b `.agent/last_block.md`
             C1  `.agent/live_review.md`
             C2  `.agent/live_review.md`
             C3  `packages/orchestration/role_config.py` AND
                 `tests/orchestration/test_role_config.py` — ONE commit, both
                 files, because the tuple and the pin that freezes it may never
                 be separated (R-0151).
             C4  `.agent/plan.md`
             C5  `.agent/handoff.md`
             Nothing else is created, modified, deleted or staged. These paths
             are PRESENT at the base and must stay untouched:
             `packages/orchestration/role_conventions.py`,
             `packages/orchestration/config.py`, `apps/cli/commands/do_cmd.py`,
             `packages/orchestration/token_cost_policy.py`,
             `docs/roadmap/features/T5_F255.md`, `.agent/decisions.md`,
             `.agent/context.md`, `AGENTS.md`.

Constraints:
1. NO SLICE IS EDITED. Every text between `<<<SLICE x` and `<<<END x` is applied
   byte for byte. A slice you believe is wrong is applied anyway and DECLARED in
   the handback; you never repair it silently. Marker lines never reach a target.
2. TRANSPORT. `.remedy-wt/f255-r6.md` is this block on disk. C0a copies that
   FILE to `.agent/authored/f255-r6.md` — copy it, never retype it — and C0b
   copies the same file to `.agent/last_block.md`. Prove all three byte-EQUAL;
   the reviewer stated the expected digest when it delegated, and that digest
   cannot appear in this file because this file is what it digests.
3. FOUR PAIRS, AND THEY DO NOT ALL HAVE THE SAME SHAPE. The reviewer ran the
   containment test over each before emission and quotes each result as the test
   printed it. ROLEDOCFROM→ROLEDOCTO: `TO contains FROM: True` — APPEND-shaped.
   ROLETUPFROM→ROLETUPTO: `False` — REWRITE. PINNAMEFROM→PINNAMETO: `False` —
   REWRITE. PINTUPFROM→PINTUPTO: `False` — REWRITE. G6 orders the FROM-zero
   count for the three rewrites ONLY, and never for the append, whose FROM the
   applied file necessarily still carries (§4.9, R-0207).
4. EVERY FROM IS UNIQUE IN ITS TARGET. The reviewer measured each of the four
   FROM texts at exactly 1 occurrence in its file at the base. Apply each by a
   count-checked replacement: assert the FROM occurs exactly once BEFORE
   replacing, and stop if it does not.
5. THE TUPLE AND ITS PIN LAND IN ONE COMMIT. C3 changes two files at once, which
   this project otherwise avoids, because `tests/orchestration/test_role_config.py`
   freezes `KNOWN_ROLES` as an exact tuple: a commit that adds the name without
   the pin, or the pin without the name, is RED on its own. Splitting them is
   the R-0151 defect, not tidiness.
6. THE LEDGER APPENDS ARE BLANK-SEPARATED. R0604 at C1 and RECORDR5 at C2 are
   each appended preceded by exactly one blank line (R-0578). This round
   registers one finding and resolves none: the registered count moves 179 to
   180 and the resolved count stays 3.
7. YOU NEVER WRITE A `Done:` OR A `Landed:` PARAGRAPH.
8. NOTHING ELSE IS BUILT. No `ConventionsRole` member, no conventions document,
   no config key, no CLI flag, no narration code. If the change looks
   incomplete, that is because T001's second half is R7's.
9. `.agent/STOP` is read from disk before C0a. If it exists, stop and write the
   handback instead.
10. `git status --porcelain` is EMPTY after every commit. No worktree is created
   this round: the reviewer already ran the destructive red-proof G7 reports.
11. YOU DO NOT WAIT ON ANY CI RUN and you report no run's conclusion.

<<<SLICE ROLEDOCFROM
KNOWN_ROLES: tuple[str, ...] = (
    "builder",
<<<END ROLEDOCFROM

<<<SLICE ROLEDOCTO
#: ``teacher`` (F255) narrates a running mission and answers operator questions.
#: It is listed here so its calls resolve without the unknown-role warning. It is
#: read-only by construction and never influences a run, which is why it carries
#: no CLI override flags and no per-role budget limit (DECISION F255 D1 and D3).
KNOWN_ROLES: tuple[str, ...] = (
    "builder",
<<<END ROLEDOCTO

<<<SLICE ROLETUPFROM
    "orchestrator",
)
<<<END ROLETUPFROM

<<<SLICE ROLETUPTO
    "orchestrator",
    "teacher",
)
<<<END ROLETUPTO

<<<SLICE PINNAMEFROM
    def test_all_seven_roles_present(self):
        assert KNOWN_ROLES == (
<<<END PINNAMEFROM

<<<SLICE PINNAMETO
    def test_all_eight_roles_present(self):
        assert KNOWN_ROLES == (
<<<END PINNAMETO

<<<SLICE PINTUPFROM
            "orchestrator",
        )
<<<END PINTUPFROM

<<<SLICE PINTUPTO
            "orchestrator",
            # F255: the teacher role. A read-only narrator and tutor;
            # same built-in defaults as every other role.
            "teacher",
        )
<<<END PINTUPTO

<<<SLICE R0604
- R-0604 — Low — A BLOCK STATED A COUNT OF ITS OWN SLICES WITHOUT COUNTING THEM, AGAINST A CHECKLIST ITEM THAT ALREADY FORBIDS EXACTLY THAT. G3 of the F255 R5 block, saved at `d450dfe2`, opens "Report the extraction command and the sha256, byte count AND line count of each of the nine slices". The block carries TEN: CAPFROM, CAPTO, ITEM30FROM, ITEM30TO, R0603, RECORDR4, DONE0462, DONE0602, DONE0603 and PLAN255R5, counted by the reviewer from the committed blob with the same marker regex the worker used. The worker measured all ten, applied all ten and DECLARED the discrepancy rather than dropping a slice to match the numeral or silently correcting the prose, which is the behaviour constraint 1 asks for and the reason this is registered against the block and not against the round. No slice was lost and nothing on disk is wrong. What makes this worth an id is that the rule was already written down: checklist item 11 of docs/agents/planner_reviewer_prompt.md says a claim a block makes about its OWN text is MEASURED before emission and written as the property that was measured — "State what was counted, or state nothing" — and names the R-0402, R-0404, R-0436 and R-0441 family it was promoted to stop. This is that family's next member, and it arrived in the very block that added item 30 for a different recurrence, which is the sharpest available evidence that a checklist item alone does not bind an author who does not run it. The counter-measure is therefore mechanical rather than more prose: the reviewer's pre-emission run already extracts and lists every slice in order to compute the per-slice digests, so item 11 gains one sentence requiring any numeral a block states about its own parts to be taken FROM that listing rather than written beside it, and a block that would rather not count says "each slice" and states no number at all.
<<<END R0604

<<<SLICE RECORDR5
Gate: R6 — the R5 entry. R5 PASSED. One finding is registered this round, R-0604, against the R5 BLOCK's own prose and not against the round's work, which was clean. Every gate the R5 block ordered was RE-EXECUTED by the reviewer over `b40c0616..9d28d93c` rather than read from the handback, and every one holds. THE TRANSPORT HELD IN THE PRIMARY FORM: `.remedy-wt/f255-r5.md`, the committed `.agent/authored/f255-r5.md` at `d450dfe2` and the committed `.agent/last_block.md` at `4ecf0204` are byte-EQUAL at sha256 ce51cd34df901c978b8ad34867a144fa78c19e6d369be46e1d701260b7e7e474 over 26527 B and 287 lines, the digest stated at delegation. THE TOKEN CAP IS GONE AND THE LINE CAP IS NOW SAID TO BE THE OPERATIVE ONE: in `docs/agents/handback_template.md` the CAPFROM text reads 1x at `b40c0616` and 0x at `4d1ca90c` while CAPTO reads 0x then 1x — the FROM-zero count a REWRITE owes — with a numstat of 10/2; the LINE-cap sentence naming ≤60, ≤100 and ≤160 is present exactly once at BOTH ends and was not edited; and the string "800 tokens" survives in the file only inside CAPTO's own historical clause, which records what stood there until 2026-08-20 and why it was withdrawn, not as a rule. THE CHECKLIST GAINED ITEM 30 AS AN APPEND: ITEM30FROM reads 1x at the base AND 1x at `9a4b3fbf`, which is what an APPEND-shaped pair owes and why no FROM-zero count was ordered or reported; the commit adds 19 lines and deletes none; each of the 19 TO-ONLY lines occurs exactly 1x among the lines that commit's diff ADDS; `^  30. ` reads 0x at the base and 1x after; and inside the checklist block — delimited by the line beginning `- **Pre-emission block checklist` and the line beginning `  Why this is on disk` — the item numbers are exactly 1 through 30 with no gap and no repeat. The reviewer re-measured the unscoped control it had ordered: the same regex reads 34 across the whole file, because the Verification-tiers list below the checklist shares its shape, which is why the gate was scoped before it was ordered rather than after it failed. THE THREE RESOLUTIONS AND THE VERDICT LANDED AS ONE APPEND: the pre-C4 blob is a byte-exact PREFIX of the post-C4 blob at `6e5b2196`, and the 8-line remainder equals a blank line, RECORDR4, a blank line, DONE0462, a blank line, DONE0602, a blank line and DONE0603, byte for byte, in that order; an independent paragraph split of the whole blob yields those same four as its LAST four units in the same order; and a one-character mutant is REJECTED by both readings. THE SETS MOVED EXACTLY AS ORDERED AND BOTH ENDS WERE MEASURED: 178 registered / 0 resolved / 178 open / 0 line-anchored `Landed:` at `b40c0616`, 179 / 0 / 179 / 0 at `fcd0ee37` where R-0603 is registered, and 179 / 3 / 176 / 0 at `6e5b2196`; `Done: R-0462 — `, `Done: R-0602 — ` and `Done: R-0603 — ` each occur exactly 1x, each id remains registered 1x so the pair reads as resolved rather than deleted, and `Gate: R5 — the R4 entry.` occurs 1x, sits last, with all five header keys distinct. THE ROUND GATE WAS RE-RUN SERIALLY BY THE REVIEWER IN THE PRIMARY CHECKOUT: the four-file state-reader selection exited 0 at `160 passed`, `tests/docs/` exited 0 at `295 passed` and the canary exited 0 at `42 passed`. THAT DOCS RUN IS A REGRESSION CHECK AND NOT EVIDENCE ABOUT THE TWO EDITS, which the block said before it was run and the worker repeated rather than quietly claiming otherwise: the reviewer had replaced the whole of `docs/agents/handback_template.md` with the single word BROKEN inside a disposable worktree and `tests/docs/` still exited 0 at 295 passed, so that suite is blind to `docs/agents/**` and the proof for C2 and C3 is the pair gates that read the files themselves. THE RANGE AND THE HISTORY HOLD: seven paths over eight single-parent commits, every `+/-` cell byte-identical to `git diff --numstat` at 287/0, 218/268, 2/0, 10/2, 19/0, 8/0 and 18/16 with C6's own 53/54 routed to the round report; a maximum insertion column of 287 under the 500 cap; `git diff --name-only` scoped to `apps/ packages/ tests/ scripts/` EMPTY, so nothing was built; all seven paths named untouched PRESENT at the base and ABSENT from the range; zero marker lines in any written file; and a handback of 98 lines inside the ≤100 its eight-commit table earns, making no claim about the token cap its own C2 had just removed. FOUR OF THE SEVEN DECLARED DEVIATIONS ARE WORTH KEEPING IN THE RECORD: the ten-versus-nine slice miscount, which is R-0604; the whole-line reflog control returning 0 this round and therefore NOT discriminating, reported as measured rather than as the control passing, one round after it returned 1 and did; the two readings of "header key", both measured and the chosen one named so a reviewer can re-measure the one the gate meant; and the handback drafted at 104 lines, re-wrapped without dropping content and re-measured at 98 before being written ONCE, which is the write-once rule working rather than a trim-commit loop.
<<<END RECORDR5

<<<SLICE PLAN255R6
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
R6: register R-0604, record the R5 verdict, and build T001's first half — the
name `teacher` in `KNOWN_ROLES` with its frozen pin renamed and extended in the
SAME commit. The first source-touching round of this feature.

## Next Steps
1. R7 BUILDS T001'S SECOND HALF: `teacher` joins `ConventionsRole` with a
   conventions document under `docs/agents/`, and a `teacher.model` config key
   modelled on the existing `orchestrator.model` spec. The conventions loader
   caps such a document, so its size is measured before it is authored.
2. R8 BUILDS T002 AND T003 TOGETHER — Stage 1 narration over an enumerated
   event set, and the behavioural read-only proof — because a read-only feature
   whose read-only-ness is unproven is this feature's likeliest failure.
3. T004, Stage 2 Q&A, comes last and only once the grounding-source labelling
   of T002 is real.

## Risks
- FIVE ROLE LISTS EXIST AND ONLY ONE IS TOUCHED HERE. R2 measured them;
  DECISION F255 D1 rules that the CLI-override and token-cost lists are
  deliberately NOT extended, so a later reader finding `teacher` absent from
  them is seeing a decision rather than an omission.
- STAGE 1 MUST STAY ZERO-TOKEN TO BE WORTH HAVING. If narration quietly starts
  calling a model, the feature loses both its cost story and its offline story.
- THE AMENDMENT IS NOW THE SPEC. A T-slice that drifts from it is a finding
  rather than a preference, which is why it was written before any build.
<<<END PLAN255R6

Done when:
G1 HYGIENE. `.agent/STOP` read from disk before C0a and reported absent or
   present; branch is feature/f255-teacher-role; `git status --porcelain` EMPTY
   after every commit and at the handback; `git worktree list` reports the
   primary checkout alone. No reading is taken by overwriting a file in the
   primary checkout — use `git show <sha>:<path>`.
G2 TRANSPORT. Report the sha256 and the byte and line counts of
   `.remedy-wt/f255-r6.md`, of `.agent/authored/f255-r6.md` at C0a and of
   `.agent/last_block.md` at C0b, and state whether all three are EQUAL.
G3 SLICES EXTRACTED, NEVER RETYPED. Extract each slice from the COMMITTED
   `.agent/authored/f255-r6.md` by its markers and report, for EACH slice the
   block contains, its name, sha256, byte count and line count, naming the
   newline convention used (R-0600). Report the number of slices you found as a
   COUNT YOU TOOK FROM THAT LISTING; this block deliberately states no numeral
   of its own for it (R-0604, checklist item 11).
G4 R-0604 REGISTERED AND R5 RECORDED. C1 appends R0604 and C2 appends RECORDR5,
   each preceded by exactly one blank line. For EACH of the two commits report
   the PREFIX property, the remainder's sha256, byte and line counts, and that
   the separator is present. For C2 report a SECOND, independent
   paragraph-level split whose LAST unit is RECORDR5, giving that unit's sha256
   under BOTH newline conventions with the byte count of each, and run a
   negative control — one character of the expected remainder mutated — showing
   BOTH readings reject it. Report registered / resolved / open / line-anchored
   `Landed:` at the base, at C1 and at C2: the reviewer measured
   179 / 3 / 176 / 0 at `9d28d93c`; C1 owes 180 / 3 / 177 / 0 and C2 the same,
   because a `Gate:` paragraph adds neither kind of line. Report that
   `- R-0604 — ` occurs 1x and that `Gate: R6 — the R5 entry.` occurs 1x, is the
   LAST line beginning `Gate: R`, and repeats no header key.
G5 THE FROM TEXTS WERE UNIQUE BEFORE THEY WERE REPLACED. For each of the four
   FROM slices report its occurrence count in its target file at the base. The
   reviewer measured each at exactly 1. A count other than 1 stops the round.
G6 THE FOUR PAIRS, BY THEIR OWN SHAPES. For the three REWRITE pairs —
   ROLETUPFROM→ROLETUPTO, PINNAMEFROM→PINNAMETO, PINTUPFROM→PINTUPTO — report
   FROM's count at the base and at C3 and TO's count at both ends; each owes
   FROM 0x and TO 1x after C3. For the APPEND-shaped pair ROLEDOCFROM→ROLEDOCTO
   report FROM 1x at BOTH ends and each TO-ONLY line exactly 1x among the lines
   C3's diff ADDS, and do NOT report a FROM-zero count for it: that count is
   unreachable by construction (§4.9, R-0207). Report `git diff --numstat` for
   BOTH files at C3.
G7 THE VOCABULARY IS REAL, AND THE PIN IS A TRIPWIRE. Report the exact command,
   exit code and tail of
     `python3 -m pytest tests/orchestration/test_role_config.py -q -rf`
   The reviewer measured exit 0 at 32 passed at the base and exit 0 at 33 passed
   with these four pairs applied — the parametrize over `KNOWN_ROLES` gains the
   teacher case, which is where the extra test comes from. Report also, from a
   short `python3 -c` you run yourself, that `len(KNOWN_ROLES)` is 8 and that
   `resolve_role_config("teacher")` returns a config whose `.role` is `teacher`
   WITHOUT raising under `warnings.simplefilter("error")` — the acceptance
   criterion the amended feature file states. Do NOT run a mutation red-proof:
   the reviewer already ran it in a disposable worktree before emitting this
   block — removing `"teacher"` from the tuple while the pin still asserts it
   turns `test_all_eight_roles_present` RED at
   `tests/orchestration/test_role_config.py:124` with 1 failed and 31 passed —
   and constraint 10 forbids you creating a worktree.
G8 RUFF, SCOPED TO THE TWO FILES C3 TOUCHES, measured against the SAME two files
   at the base so a pre-existing error is not read as a new one (R-0364).
   Report the exact command, exit code and output of
     `python3 -m ruff check packages/orchestration/role_config.py tests/orchestration/test_role_config.py`
   at C3. The reviewer measured `All checks passed!` for those two paths at the
   base and again with the four pairs applied.
G9 THE PLAN. `.agent/plan.md` at C4 byte-equals PLAN255R6; report its sha256,
   byte and line counts, that the line count is under 50, and that `## Goal`,
   `## Next Steps` and a roadmap F-id all occur in it.
G10 THE ROUND GATE, serially in the PRIMARY checkout, never two pytest processes
   at once. This round rewrites `.agent/` state and touches source, so the four
   state-reader files gate alongside the role test and the canary. Report the
   exact command, exit code and tail of each:
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
   The reviewer measured exit 0 at 160 passed and exit 0 at 42 passed, both at
   `9d28d93c` in the primary checkout.
G11 CHANGE SET, HISTORY AND CAPS. Report `git diff --name-only 9d28d93c..HEAD`
   and state that it equals the Change list with no path on either side alone.
   Report that each of the eight paths the Change section names as untouched is
   PRESENT at the base and absent from the range; that every commit in the range
   has one parent; and each commit's insertion column from `git diff --numstat`,
   every one under 500, with the same `+/-` cells appearing byte-identically in
   the handback's `## Commits` table. C5's own cell and the complete change set
   belong to the round report.
   THE REFLOG IS REPORTED AS TWO MEASURED CLAIMS, NOT ONE UNIVERSAL (R-0601):
   the count of this round's reflog entries that PRODUCED a commit and read
   `commit`, which must equal the number of commits the round makes; and the
   count whose OPERATION PREFIX — the text before the first colon of
   `git reflog --format=%gs` — contains `amend`, `reset`, `rebase` or `cherry`,
   which must be 0. Read the prefix, never the whole line. Report ALSO what the
   retired whole-line reading would have returned this round, as a control, and
   say plainly whether it discriminated.
G12 NO MARKER LEAKED. Report the count of LINES beginning `<<<SLICE ` or
   `<<<END ` in `.agent/live_review.md` at C2,
   `packages/orchestration/role_config.py` and
   `tests/orchestration/test_role_config.py` at C3, `.agent/plan.md` at C4 and
   `.agent/handoff.md` at C5. Every count must be 0.
G13 THE PUSH. After C5, `git push` and report its real output. Do NOT create a
   pull request and do NOT wait on the CI run the push starts (constraint 11).

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             all seven mandated headings in the template's order, the
             item-status table for the C0a..C5 bundle, the `## Commits` table
             G11 pins, and one LINE per gate rather than its transcript
             (R-0582). The template's token cap was removed at R5; the LINE cap
             your commit count earns is the bound. Its `## Next` section names
             the next session's FIRST action as Phase 1 rule 1, the
             `.agent/STOP` re-read, and its SECOND as R7, T001's second half —
             `ConventionsRole`, the conventions document and the `teacher.model`
             config key — in that order, and states that R6 awaits review. There
             is no open pull request. The full transcripts go in the round
             report you return, never in the file. The handback also carries
             this Fortschritt line verbatim, because with no relay you never see
             the operator brief that would otherwise state it (R-0418):
             Fortschritt: ~20 % (F086 merged · F255 claimed · ground measured ·
             six DECISIONs ruled · the spec written · T001 first half BUILT: the
             teacher role name resolves) — Schätzung
──────────────────────────────────────────────────────────────
