── STEP R17 — F255 Teacher role ───────────────────────────────
Goal:        Persist the R16 verdict and its three findings, then close the one
             of them that is a code defect: grounding source (2), workspace code,
             has NO production caller — `ask_teacher` accepts `code` and
             `code_path` and nothing outside the tests ever passes them, so the
             source the ruled Design puts in Stage 2's context is unreachable
             from the CLI. R16 PASSED; all three findings are against the
             REVIEWER's block, none against the worker's execution.

Bundle:      C0a save this block · C0b mirror it · C1 the plan, FIRST · C2
             register R-0608, R-0609 and R-0610 · C3 record the R16 verdict ·
             C4 close R-0610 in the CLI · C5 its tests · C6 the handback, then
             push.

Change:      Exactly these paths, in this order, one commit each.
             C0a `.agent/authored/f255-r17.md`
             C0b `.agent/last_block.md`
             C1  `.agent/plan.md`
             C2  `.agent/live_review.md`
             C3  `.agent/live_review.md`
             C4  `apps/cli/commands/teach_cmd.py` and
                 `apps/cli/command_catalog.py`
             C5  `tests/cli/test_teach_cmd.py`
             C6  `.agent/handoff.md`
             Nothing else is created, modified, deleted or staged. These paths are
             PRESENT at the base `8f885b4f` and must stay untouched:
             `packages/orchestration/teacher_model.py`,
             `packages/orchestration/teacher_qa.py`,
             `packages/orchestration/teacher_spend.py`,
             `tests/orchestration/test_teacher_model.py`,
             `.agent/decisions.md`, `docs/roadmap/features/T5_F255.md`.
             C4 AND C5 ARE SEPARATE COMMITS BY DESIGN, and that is R-0609's
             counter-measure applied by the block that registers it: a source
             change and the tests that hold it to its spec are ordered as two
             commits from the start, so the 500-insertion cap is never something
             the worker has to discover mid-round.

             WHAT C4 BUILDS — the `--file` option that gives grounding source (2)
             a caller. `_cmd_teach_ask` gains a `file` parameter, wired from a new
             `ArgDef("--file", ..., required=False, is_option=True)` on the
             `teach.ask` catalog entry. When it is given, the command reads THAT
             ONE FILE read-only, in text mode, and passes its contents as `code`
             and the path as `code_path` to `ask_teacher`; when it is absent both
             stay None and behaviour is exactly what it is today.
             A FILE THAT CANNOT BE READ NEVER FAILS THE COMMAND, because a
             teacher that could fail a run would not be passive: the command
             prints ONE plain line naming the path and the reason, then answers
             from the sources it does have. It NEVER silently drops the file —
             silence would let an operator believe an answer read code it never
             opened, which is the invention this role exists to refuse.
             THE COMMAND STAYS `write_metadata` AND STAYS READ-ONLY TOWARD THE
             WORKSPACE: reading a source file writes nothing, so DECISION F255
             D10 is untouched and the ledger row remains the only write.
             `_grounding_sources` already derives its list from the context's
             facts, so passing `code` makes `code` appear in that list with no
             change to that helper; the context it builds for the printed source
             list is built with the SAME `code` and `code_path` arguments as the
             one `ask_teacher` builds, or the two disagree.

             WHAT C5 BUILDS — the tests that hold C4 to it, in
             `tests/cli/test_teach_cmd.py`, all with an injected fake `call`:
             * WITH `--file`, THE ANSWER IS CODE-GROUNDED. The rendered prompt the
               fake `call` receives contains the file's text and its path, and the
               JSON output's `grounding_sources` contains `code`.
             * WITHOUT `--file`, NOTHING CHANGES. `grounding_sources` does not
               contain `code`, and the prompt carries no code block.
             * AN UNREADABLE PATH IS SAID OUT LOUD AND STILL ANSWERS. Pointing
               `--file` at a path that does not exist prints a line naming that
               path, exits 0, still produces an answer, and leaves `code` out of
               `grounding_sources`.
             * READING A FILE WRITES NOTHING NEW. The data-root hash map with the
               ledger excluded by name is unchanged across an ask WITH `--file`,
               and the file itself is byte-identical afterwards.

Constraints:
1. NO SLICE IS EDITED. Every text between the SLICE and END markers is applied
   byte for byte. A slice you believe is wrong is applied anyway and DECLARED in
   the handback; you never repair it silently. Marker lines never reach a target.
2. TRANSPORT. `.remedy-wt/f255-r17.md` is this block on disk. C0a copies that
   FILE to `.agent/authored/f255-r17.md` — copy it, never retype it — and C0b
   copies the same file to `.agent/last_block.md`. Prove all three byte-EQUAL;
   the reviewer stated the expected digest when it delegated, and that digest
   cannot appear in this file because this file is what it digests.
3. THE PLAN COMES FIRST. Findings R-0377, R-0491 and R-0548 are OPEN and all rule
   that the `.agent/plan.md` update is the FIRST substantive commit of a round
   with substance to record. Only C0a and C0b may precede it.
4. THE FINDINGS PERSIST BEFORE THE VERDICT. C2 registers all three and C3 records
   the R16 verdict, in that order (§4.4), so a session that dies between them
   leaves the findings on disk rather than losing them.
5. BOTH APPENDS ARE BLANK-SEPARATED (R-0578): FINDINGS3 at C2 and RECORDR16 at C3
   are each appended preceded by exactly one blank line. FINDINGS3 carries THREE
   registration paragraphs separated from each other by exactly one blank line —
   the reviewer measured its own extraction and its own blank-line split and both
   give three. This round registers three findings and resolves NONE: registered
   goes 183 to 186, resolved stays 3.
6. RECORDR16 IS SINGLE-PARAGRAPH — the reviewer measured it for an interior blank
   line and found none — so the LAST-UNIT paragraph reading G6 orders is exact for
   it. FINDINGS3 is MULTI-paragraph, so NO last-unit reading is ordered or owed
   for it and none may be reported as if it were; its proof is the prefix and
   remainder reading plus the two independent extractions G6 orders (R-0606).
7. THIS ROUND CONTAINS NO FROM/TO PAIR, so no containment reading and no
   FROM-zero count is owed (§4.9, R-0207). The code C4 and C5 build is written by
   you to the specification above; it is NOT authored text and carries no
   transport proof.
8. YOU NEVER WRITE A `Done:` OR A `Landed:` PARAGRAPH. R-0610's fix lands this
   round; only the reviewer's own text at the next gate may resolve it, and this
   block deliberately authors no resolution for it.
9. NO TEST OPENS A SOCKET AND NO TEST REQUIRES A RUNNING OLLAMA. Every test that
   reaches `ask_teacher` injects `call`.
10. `.agent/STOP` is read from disk before C0a. If it exists, stop and write the
    handback instead.
11. `git status --porcelain` is EMPTY after every commit. No worktree is created,
    and the primary checkout is never mutated to take a reading — use
    `git show <sha>:<path>`.
12. YOU DO NOT WAIT ON ANY CI RUN, you report no run's conclusion, and you create
    NO pull request: on this project the PR is created by the closure round.

<<<SLICE PLAN255R17
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
R17 persists the R16 verdict and its three findings, then closes the one that is a
code defect: `remedy teach ask` gains `--file`, so grounding source (2) — the
workspace code the ruled Design puts in Stage 2's context — finally has a
production caller instead of only a test one.

## Next Steps
1. The INTEGRATION GATE round follows, per docs/agents/integration_gate.md: the
   full suite, because T002, T003 and T004 all touch the CLI catalog, which the
   parser and the help renderer both read.
2. The CLOSURE round follows, per docs/roadmap/STATUS_closure_protocol.md:
   evidence job, fresh review zip, the STATUS line, and the pull request.

## Risks
- T004 WAS REPORTED COMPLETE AT R16 WHILE SOURCE (2) HAD NO CALLER. That is
  R-0610, and this round closes the code half; the Fortschritt line stops
  claiming a completeness the CLI did not have until now.
- R-0608 AND R-0609 BIND FUTURE BLOCKS, NOT THIS CODE. They are reviewer gate
  defects — a reflog absence clause that reads a harmless `git reset` as history
  rewriting, and a block that ordered a source and its tests as one oversize
  commit — and each is answered by the shape of this block rather than by an edit.
<<<END PLAN255R17
<<<SLICE FINDINGS3
- R-0608 — Low — A GATE'S HISTORY-REWRITE ABSENCE CLAUSE COUNTS `reset` BY OPERATION PREFIX, AND A BARE `git reset` THAT ONLY UNSTAGES REWRITES NOTHING. G13 of the F255 R16 block, saved at `883b9886`, orders the count of this round's reflog entries "whose prefix contains `amend`, `reset`, `rebase` or `cherry`, which must be 0". R16's worker staged the C5 pair, measured it at 542 insertions, ran a bare `git reset` to UNSTAGE it so it could be split, and thereby produced one entry reading `reset: moving to HEAD` whose destination is `cbcc65e1` — the commit the branch ALREADY pointed at, so the entry moved the branch tip nowhere, no commit was created, rewritten, dropped or reordered, and `git log --reverse 2e5b8299..8f885b4f` still lists eleven single-parent commits in the block's order. The worker reported the real 1 rather than a convenient 0 and demonstrated the equality, which is the correct response and the reason this is registered against the block's wording and never against the round. THE CLAUSE IS OVER-SCOPED REPO-WIDE, not merely for this round: the reviewer measured `git reflog --format=%gs` at `8f885b4f` and `reset: moving to HEAD` recurs many times across this repository's history, so an unstage is ordinary practice here and any block ordering this clause makes an honest worker choose between an unstage and a green gate. THIS IS NOT A DUPLICATE OF R-0601, and the open set was searched for the DEFECT before this id was minted, as item 30 requires. R-0601 is OPEN and covers the OTHER clause of the same gate — the universal that every reflog entry of a round read `commit:`, unmeetable for a round that navigates branches — and its counter-measure explicitly BLESSES the clause that just failed, stating that `amend`, `reset`, `rebase` and `cherry` "each occur 0 times" as the safe property to order instead. So this finding is R-0601's own fix being too broad, which R-0601 cannot describe because it prescribes it; R-0605 set the precedent for minting a new id in exactly this shape and saying why. FIX: order the absence of HISTORY REWRITING as what it is — no entry of the round whose operation prefix is `amend`, `rebase` or `cherry`, plus, for any `reset` entry, the demonstration that its destination is the commit the branch already pointed at — or drop `reset` from the prefix list and gate the commit list itself, which is the property that actually matters. The landed R-0601 text is NOT rewritten; item 20 rules that the counter-measure is a dated correction in new text, and this paragraph is that correction.

- R-0609 — Low — A BLOCK ORDERED A NEW SOURCE FILE AND ITS TEST AS ONE COMMIT WITHOUT EVER ESTIMATING THEIR COMBINED INSERTIONS, AND THE PAIR CAME TO 542 AGAINST A 500 CAP. C5 of the F255 R16 block, saved at `883b9886`, names `packages/orchestration/teacher_model.py` (NEW) and `tests/orchestration/test_teacher_model.py` (NEW) as one commit. The worker measured the staged pair, found 542 insertions against the hard cap AGENTS.md "Commit Discipline" sets and the block's own G13 re-pins, applied that rule's own prescribed remedy — "stop and split before committing" — and landed `c2f31bdb` at 259 and `8120646c` at 283, module before tests, and declared the split. That was the correct call, AGENTS.md outranks the block, and no oversize exception was consumed. THE ROOT CAUSE IS THE REVIEWER'S: the block specified the module's whole public API and the four behavioural proofs in prose, so their size was foreseeable, and no line was spent estimating it. THIS IS NOT A DUPLICATE OF R-0381 OR R-0385, and the open set was searched for the DEFECT first: both are OPEN and both are about the BLOCK-SAVE pair — the authored file and its `.agent/last_block.md` mirror, whose insertions are about twice the block's line count by construction — and R-0385's fix reaches only that pair, ordering C0 as two commits once a block passes roughly 250 lines. Neither reaches a block ordering a SOURCE file and its TEST file as one commit, which is a different pair with a different arithmetic. FIX, applied by the block that carries this finding rather than merely described by it: a block that orders new code estimates each ordered commit's insertions before emitting, and orders a source file and the tests that pin it as SEPARATE commits from the start whenever their sum could approach the cap — which for a module specified API-by-API in prose it almost always can.

- R-0610 — Medium — GROUNDING SOURCE (2), WORKSPACE CODE, HAS NO PRODUCTION CALLER, WHILE THE ROUND THAT SHIPPED STAGE 2 REPORTED T004 COMPLETE. `packages/orchestration/teacher_qa.py` has accepted `code` and `code_path` since the round that built it, and `packages/orchestration/teacher_model.py` at `c2f31bdb` passes both straight through `ask_teacher` to `build_teacher_context`. Measured by the reviewer at `8f885b4f`: the ONLY caller of `ask_teacher` outside the tests is `_cmd_teach_ask` in `apps/cli/commands/teach_cmd.py`, and it passes neither, so no production path can put a `code` fact in a teacher context and grounding source (2) is reachable from the test suite alone. THE RULED DESIGN REQUIRES IT: the Design section of docs/roadmap/features/T5_F255.md describes Stage 2 as running "over a small context: the relevant ledger slice plus the code location asked about", and the Scope names the same pairing, so a Stage 2 that can only ever be ledger-grounded is short of what R3 ruled. THE CLAIM IS THE SHARP EDGE: `.agent/handoff.md` at `8f885b4f` carries the Fortschritt line "T004 COMPLETE at this round", and that sentence was AUTHORED BY THE REVIEWER and ordered verbatim, so the overstatement is the block's and not the worker's — the worker applied the text it was given, as constraint 1 requires. THIS IS THE SAME CLASS THE ROUND SET OUT TO PAY DOWN, which is what makes it worth a Medium rather than a Low: R16 existed partly to stop `teacher_spend.record_teacher_question` sitting uncalled the way R13 left it, and it closed that gap while opening this one a layer up. FIX: give `remedy teach ask` a `--file` option that reads one workspace file read-only and passes it as `code` with its path as `code_path`, with a test that a code-grounded answer names `code` among its grounding sources and one that an unreadable path is reported out loud rather than silently dropped; and stop reporting a task complete while a source its own Design enumerates has no caller.
<<<END FINDINGS3
<<<SLICE RECORDR16
Gate: R17 — the R16 entry. R16 PASSED. THREE findings are registered this round — R-0608, R-0609 and R-0610 — and ALL THREE are against the REVIEWER's block rather than the worker's execution, which did exactly what it was ordered to do and reported two deviations honestly rather than hiding them. Every gate the R16 block ordered was RE-EXECUTED by the reviewer over `2e5b8299..8f885b4f` rather than read from the handback; every number here is the reviewer's own. THE TRANSPORT HELD IN THE PRIMARY FORM: `.remedy-wt/f255-r16.md`, the committed `.agent/authored/f255-r16.md` at `883b9886` and the committed `.agent/last_block.md` at `6d137821` are byte-EQUAL at sha256 8e40970251874febe66b0d0b66ea213d8fcf1df902652013fed3ed77f3565a2e over 36286 B and 478 lines, the digest stated at delegation. FOUR SLICES, a count taken from the reviewer's own ordered extraction of the committed blob and agreeing with the worker's independent count, newline convention NEWLINE-INCLUDED: PLAN255R16 sha256 a9f93d981010431d2c67c995bbe283846a1a6192aa063223da9aa79c6ceea6e1 over 2245 B and 41 lines; RECORDR15 sha256 9ed4d44468e46c7b85204a7a4fc0d7f9410c111fb93216b0f7396928c3ddbbdd over 4742 B and 1 line; DECISIONS255 sha256 02427bbaeb2ef1fd91b810ec6f612622e4dc04981f8c1c7c4a674c554f4ace70 over 6297 B and 102 lines; AMEND255 sha256 b201ac7aece30e31a0d9654d4d72e22289ec5e73a4dacaa6471b521a2a46ceb9 over 1765 B and 26 lines. THE PLAN LANDED FIRST: `.agent/plan.md` at `9dfbcd4a` byte-equals PLAN255R16 over 2245 B and 41 lines, under the 50-line cap, carrying `## Goal` once, `## Next Steps` once and the F-id F255, and `git log --reverse 2e5b8299..9dfbcd4a` opens 883b9886, 6d137821, 9dfbcd4a, so it is the first commit after the two block-save commits. THE THREE APPENDS ARE EXACT: the `.agent/live_review.md` blob at `2e5b8299` is a byte-exact prefix of the blob at `27941050` whose 4743 B remainder equals one newline followed by RECORDR15 with `G` after that newline; the `.agent/decisions.md` blob is a byte-exact prefix of the blob at `85ea2d43` whose 6298 B remainder equals one newline followed by DECISIONS255; and `docs/roadmap/features/T5_F255.md` is a byte-exact prefix of the blob at `cbcc65e1` whose 1766 B remainder equals one newline followed by AMEND255, both with `#` after the newline. The independent blank-line paragraph split of the C2 blob gives 206 units whose LAST unit IS RECORDR15, and no paragraph reading was ordered or reported for the two multi-paragraph slices, which is what R-0606 asks. THE SETS DID NOT MOVE, which is correct for a round that registers nothing: 183 registered / 3 resolved / 180 open / 0 line-anchored `Landed:` at BOTH `2e5b8299` and `27941050`, a `Gate:` paragraph being neither kind of line. `Gate: R16 — the R15 entry.` occurs 0x at `2e5b8299` and 1x at `27941050`, sits last among the sixteen lines beginning `Gate: R`, and all sixteen header keys are distinct. Each of `## DECISION F255 D8`, `## DECISION F255 D9` and `## DECISION F255 D10` occurs 0x at the base and 1x at `85ea2d43`, counted line-anchored. THE SUITES ARE THE REVIEWER'S OWN RUNS, all serial and in the primary checkout at `8f885b4f`: `tests/orchestration/test_teacher_model.py` exit 0 at 18 passed; `tests/cli/test_teach_cmd.py` with `tests/test_command_catalog.py` exit 0 at 33 passed; `tests/docs/` exit 0 at 295 passed; `tests/orchestration/test_roadmap_index.py` exit 0 at 30 passed; the state-reader four exit 0 at 160 passed; the canary `tests/cli/test_golden_path.py` exit 0 at 42 passed; and `ruff check` 0.15.17 over the two new files and the three touched ones exit 0, All checks passed. THE CODE DOES WHAT IT CLAIMS: `teacher_model.py` opens no file and writes nothing of its own, the refusal path returns before `record_teacher_question` is reached so a refusal is never billed, `resolve_teacher_transport` inspects the provider and never the model because `resolve_role_config` always fills one, and `teach.ask` declares `write_metadata` with its pin extended to an EQUALITY of the declared and handler sets in the SAME commit as the catalog entry — the pin the reviewer had measured in a disposable worktree, before delegating, as the ONLY test the new entry turns red. THE RANGE AND THE HISTORY HOLD: twelve paths over eleven single-parent commits; per-commit insertions 478, 402, 18, 2, 103, 27, 259, 283, 153, 223 and 63, every one under the 500 cap; the change set equals the block's Change list with no path on either side alone; all five paths the block named untouched are PRESENT at `2e5b8299` and ABSENT from the range; zero lines beginning with the slice or end marker prefixes appear in any written file; and at `8f885b4f` the round has made 11 commits with 11 reflog entries whose operation prefix reads exactly `commit`, the two being EQUAL. THE HANDBACK MEASURES CLEAN: 102 lines at `8f885b4f`, inside the ≤160 bound docs/agents/handback_template.md gives a bundle whose tables cover more than ten commits, no trailing whitespace on any line, all seven mandated headings in the template's order, an item-status table naming C0a through C8 exactly once, and `## Commits` cells byte-identical to `git diff --numstat`. THE TWO DECLARED DEVIATIONS ARE BOTH THE BLOCK'S FAULT AND ARE REGISTERED AS SUCH: the C5 split is R-0609 and the single `reset: moving to HEAD` entry is R-0608, and in both the worker chose the honest reading over the convenient one. R-0610, the third, is the defect the round's own gates could not have caught, because every gate it ordered was green and the missing thing was a CALLER: grounding source (2) reaches no production path, and the Fortschritt line the reviewer authored called T004 complete anyway. R-0607 REMAINS OPEN and is closed only by a docs round promoting its rule into the docs/agents/planner_reviewer_prompt.md §3 checklist; R16 obeyed that rule, ordering the canary and the state-reader four unconditionally, without claiming to have closed it.
<<<END RECORDR16

Done when:
G1 HYGIENE. `.agent/STOP` read from disk before C0a and reported absent or
   present; branch is feature/f255-teacher-role; `git status --porcelain` EMPTY
   after every commit and at the handback; `git worktree list` reports the
   primary checkout alone.
G2 TRANSPORT. Report the sha256 and the byte and line counts of
   `.remedy-wt/f255-r17.md`, of `.agent/authored/f255-r17.md` at C0a and of
   `.agent/last_block.md` at C0b, and state whether all three are EQUAL.
G3 SLICES EXTRACTED, NEVER RETYPED. Extract each slice from the COMMITTED
   `.agent/authored/f255-r17.md` by its markers and report each slice's name,
   sha256, byte count and line count, naming the newline convention (R-0600).
   Report the number of slices as a COUNT YOU TOOK FROM THAT LISTING; this block
   states no numeral of its own for it (R-0604, checklist item 11).
G4 THE PLAN, FIRST. `.agent/plan.md` at C1 byte-equals PLAN255R17; report its
   sha256, byte and line counts, that the line count is under 50, and that
   `## Goal`, `## Next Steps` and a roadmap F-id all occur in it. Report also
   that C1 is the FIRST commit of this round other than C0a and C0b, from
   `git log --reverse 8f885b4f..<C1>`.
G5 THE FINDINGS REGISTERED. Over `.agent/live_review.md`: the base blob at
   `8f885b4f` is a byte-exact PREFIX of the C2 blob; report the remainder's
   sha256, byte and line counts; that it equals one newline followed by
   FINDINGS3; and that the byte after that leading newline is not a newline.
   THEN TWO INDEPENDENT EXTRACTIONS OF THE THREE REGISTRATIONS, which must AGREE
   (R-0578): first by splitting FINDINGS3 on blank lines, second by collecting
   the C2 blob's lines matching `^- R-\d+ — ` that are absent at the base.
   Report each id, and that both readings give the same ids in the same order.
G6 THE R16 VERDICT RECORDED. Report for C3 over the C2 blob the same prefix,
   remainder, equality and separator readings, the remainder equal to one newline
   followed by RECORDR16. THEN a SECOND, INDEPENDENT blank-line paragraph split
   of the C3 blob whose LAST unit is RECORDR16, giving that unit's sha256 under
   BOTH newline conventions with the byte count of each. Constraint 6 records the
   measurement that makes the LAST-UNIT reading exact here; re-measure it rather
   than trusting it. NO paragraph reading is ordered for FINDINGS3, which is
   multi-paragraph. Run a negative control for EACH of C2 and C3: one character
   of the expected remainder mutated, rejected by the prefix reading.
G7 THE SETS AND THE KEYS. Report registered / resolved / open / line-anchored
   `Landed:` over `.agent/live_review.md` at `8f885b4f`, at C2 and at C3, the
   registered count being lines matching `^- R-\d+ — ` and the resolved count
   lines matching `^Done: R-\d+ — `: the reviewer measured 183 / 3 / 180 / 0 at
   `8f885b4f`; C2 owes 186 / 3 / 183 / 0 because it adds three registered lines;
   and C3 owes the same as C2, a `Gate:` paragraph adding neither kind of line.
   Report that each of `R-0608`, `R-0609` and `R-0610` occurs 0x at `8f885b4f`,
   that `Gate: R17 — the R16 entry.` occurs 1x at C3 and is the LAST line
   beginning `Gate: R`, and that every such header key is distinct. COUNT
   HEADERS LINE-ANCHORED, never as substrings (R-0584).
G8 THE FIX HAS A CALLER, WHICH IS THE WHOLE POINT OF R-0610. At C5 run
     `python3 -m pytest tests/cli/test_teach_cmd.py tests/test_command_catalog.py -q -rf`
   and report the exact command, exit code and tail; exit 0. Report the NAME of
   each of the four tests the Change section's C5 list requires. Then report, as
   a MEASUREMENT over the tree at C5 rather than as a claim, every caller of
   `ask_teacher` outside `tests/`, and state for each whether it passes `code`:
   the reviewer measured exactly one such caller at `8f885b4f`, `_cmd_teach_ask`,
   passing neither `code` nor `code_path`, which is the defect R-0610 names.
G9 RUFF, AND THE SUITES THE FIX COULD REACH. At C5 run
     `python3 -m ruff check apps/cli/commands/teach_cmd.py apps/cli/command_catalog.py tests/cli/test_teach_cmd.py`
   and report its exit code; the reviewer measured ruff 0.15.17 exit 0 over these
   same three paths at `8f885b4f`, so exit 0 is the standard, and a rule code
   appearing that is absent from that base reading is a new error rather than a
   pre-existing one. Then, serially and in the PRIMARY checkout, run
     `python3 -m pytest tests/orchestration/test_teacher_model.py -q -rf`
   and report its exit code and tail; exit 0 at 18 passed at the base.
G10 THE CANARY AND THE STATE READERS, UNCONDITIONALLY — R-0607's rule, which
   binds whether or not the round looks harmless. This round rewrites `.agent/`
   state, so both gate. Run them serially in the PRIMARY checkout, never two
   pytest processes at once, and report the exact command, exit code and tail:
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
   The reviewer measured exit 0 at 160 passed and exit 0 at 42 passed at
   `8f885b4f` in the primary checkout.
G11 CHANGE SET, HISTORY AND CAPS. Report `git diff --name-only 8f885b4f..<C5>`
   and state that it equals the Change list minus `.agent/handoff.md`, which C6
   itself adds, with no path on either side alone. Report that each path the
   Change section names untouched is PRESENT at the base and ABSENT from the
   range; that every commit in the range has one parent; and each commit's
   insertion column from `git diff --numstat` for C0a through C5, every one under
   500, with the same `+/-` cells appearing byte-identically in the handback's
   `## Commits` table (checklist item 28). C6's own cell and the complete change
   set belong to the round report (R-0149).
   THE REFLOG IS TWO MEASURED CLAIMS, NOT ONE UNIVERSAL (R-0601), AND NEITHER IS
   A TOTAL (R-0605): report the count of this round's reflog entries whose
   OPERATION PREFIX — the text before the first colon of
   `git reflog --format=%gs` — reads exactly `commit`, WITH the commit it was
   taken at and the number of commits the round has made AT THAT MOMENT, and
   state that the two are equal. State no total: C6 is unwritten as this is
   composed, so the reviewer measures its entry at the next gate (R-0494).
   HISTORY REWRITING IS GATED AS R-0608 RULES, not by the clause R-0608 retires:
   report the count of entries whose prefix contains `amend`, `rebase` or
   `cherry`, which must be 0, and for EVERY entry whose prefix is `reset`, report
   that entry together with the demonstration that its destination is the commit
   the branch already pointed at. An unstage is not a rewrite, and this block
   does not ask you to pretend otherwise.
G12 NO MARKER LEAKED, AND THE PUSH. Report the count of LINES beginning with the
   SLICE or END marker prefixes in `.agent/plan.md` at C1, `.agent/live_review.md`
   at C3 and `.agent/handoff.md` at C6 — every count 0. Then, after C6,
   `git push` and report its real output. Do NOT create a pull request and do NOT
   wait on the CI run the push starts (constraint 12).

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             all seven mandated headings in the template's order, the item-status
             table for the C0a..C6 bundle, the `## Commits` table G11 pins, and
             one LINE per gate rather than its transcript (R-0582). Its `## Next`
             section names the next session's FIRST action as Phase 1 rule 1, the
             `.agent/STOP` re-read, and its SECOND as the INTEGRATION GATE round
             per docs/agents/integration_gate.md. It states that R16 PASSED, that
             its verdict is ON DISK at C3 and its three findings at C2, that
             R-0610's CODE half is fixed this round while only the reviewer's own
             text at the next gate may resolve it, that R-0607, R-0608 and R-0609
             remain OPEN, and that R17 ITSELF IS THE ROUND WHOSE VERDICT IS NOT
             ON DISK, so it awaits review. It states that no pull request is open.
             Transcripts go in the round report. The handback carries this
             Fortschritt line verbatim (R-0418):
             Fortschritt: ~90 % (T001, T002 and T003 COMPLETE · T004 COMPLETE now
             that grounding source (2) has a production caller — at R16 it did
             not, which is R-0610 · integration gate and closure remain) —
             Schätzung
──────────────────────────────────────────────────────────────
