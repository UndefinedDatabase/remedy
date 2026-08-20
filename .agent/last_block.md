── STEP R3 — F255 Teacher role ────────────────────────────────
Goal:        Record the R2 verdict, and RULE the five spec-vs-reality gaps R2
             measured plus the dead handback cap R-0602 registers, as six
             operator-visible DECISIONs. Ruling is the whole round: the feature
             file is amended in R4 from these rulings, and no code is written
             until that amendment lands.

Bundle:      C0a save this block · C0b mirror it · C1 record the R2 verdict ·
             C2 the six DECISIONs · C3 the plan · C4 the handback, then push.

Change:      Exactly these paths, in this order, one commit each.
             C0a `.agent/authored/f255-r3.md`
             C0b `.agent/last_block.md`
             C1  `.agent/live_review.md`
             C2  `.agent/decisions.md`
             C3  `.agent/plan.md`
             C4  `.agent/handoff.md`
             Nothing else is created, modified, deleted or staged. NO source
             file, NO test and NO document changes this round — in particular
             `docs/roadmap/features/T5_F255.md` is NOT amended here; R4 does
             that, from the rulings C2 lands. These paths are PRESENT at the
             base and must stay untouched: `docs/roadmap/features/T5_F255.md`,
             `docs/agents/handback_template.md`, `docs/roadmap/STATUS.md`,
             `packages/orchestration/role_config.py`,
             `packages/orchestration/token_ledger.py`,
             `apps/cli/command_catalog.py`, `.agent/context.md`,
             `.agent/f255_inventory.md`.

Constraints:
1. NO SLICE IS EDITED. Every text between `<<<SLICE x` and `<<<END x` is applied
   byte for byte. A slice you believe is wrong is applied anyway and DECLARED in
   the handback; you never repair it silently. Marker lines never reach a target.
2. TRANSPORT. `.remedy-wt/f255-r3.md` is this block on disk. C0a copies that
   FILE to `.agent/authored/f255-r3.md` — copy it, never retype it — and C0b
   copies the same file to `.agent/last_block.md`. Prove all three byte-EQUAL;
   the reviewer stated the expected digest when it delegated, and that digest
   cannot appear in this file because this file is what it digests.
3. NO FROM/TO PAIR EXISTS THIS ROUND. RECORDR2 and DECISIONS255 are APPENDS and
   PLAN255R3 is a WHOLE-FILE replacement. The reviewer ran the containment test
   over this block's slices before emission and found no pair to classify, so no
   FROM count is ordered anywhere below.
4. EVERY APPEND IS BLANK-SEPARATED. RECORDR2 and DECISIONS255 are each appended
   preceded by exactly one blank line (R-0578), copied from their extracted
   slice files and never retyped. Nothing already in either file is rewritten,
   reordered or deleted.
5. YOU NEVER WRITE A `Done:` OR A `Landed:` PARAGRAPH, and this round registers
   no finding either. The registered and resolved counts must both come back
   UNCHANGED, which G4 orders measured rather than assumed: RECORDR2 is a
   `Gate:` paragraph and adds no `- R-` line and no `Done:` line.
6. THE RULINGS ARE APPLIED, NOT EVALUATED. DECISIONS255 is the reviewer's ruling
   under §4 item 7 of docs/agents/planner_reviewer_prompt.md. You do not act on
   any decision this round — you do not add a role, a command, a test or a
   config key, and you do not amend the feature file. Landing the text IS the
   work.
7. `.agent/STOP` is read from disk before C0a. If it exists, stop and write the
   handback instead.
8. `git status --porcelain` is EMPTY after every commit. No worktree is created
   this round, because no destructive check is ordered.
9. YOU DO NOT WAIT ON ANY CI RUN and you report no run's conclusion.

<<<SLICE RECORDR2
Gate: R3 — the R2 entry. R2 PASSED with NO finding against its work and none against its block. Every gate the R2 block ordered was RE-EXECUTED by the reviewer over `6c47a490..73d7d6e2` rather than read from the handback, and every one holds. THE TRANSPORT HELD IN THE PRIMARY FORM: `.remedy-wt/f255-r2.md`, the committed `.agent/authored/f255-r2.md` at `759d9179` and the committed `.agent/last_block.md` at `29cd160a` are byte-EQUAL at sha256 6f36cbc3950bb5a940a821771d0535c235457a24b6fa77f1b367748690aa2eb1 over 25463 B and 250 lines, the digest stated at delegation. THE TWO FINDINGS LANDED AS AN APPEND AND THE SETS MOVED BY EXACTLY TWO: the base blob at `6c47a490` holds 176 registered, 0 resolved, 176 open and 0 line-anchored `Landed:`, and the C1 blob at `b9c0cb64` holds 178 / 0 / 178 / 0; the pre-C1 blob is a byte-exact PREFIX of the post-C1 blob and the remainder equals a blank line, R0601, a blank line and R0602 in that order; `- R-0601 — ` and `- R-0602 — ` each occur exactly 1x. THE R1 VERDICT ENTRY LANDED THE SAME WAY: the pre-C2 blob is a byte-exact PREFIX of the post-C2 blob, the 2-line remainder is a blank line followed by RECORDR1 at sha256 1b50c445146c0211 over 5513 B with the separator PRESENT, an independent paragraph split yields RECORDR1 as its LAST unit at sha256 e42585d9b7c57386 over 5512 B and 1 line with the trailing newline INCLUDED and at sha256 4440c6d762eb142e over 5511 B with it STRIPPED — both conventions given, per R-0600 — and `Gate: R2 — the R1 entry.` occurs 1x, is the LAST line beginning `Gate: R`, with no header key repeated. THE INVENTORY IS THE ROUND'S PRODUCT AND ITS CITATIONS RESOLVE: the reviewer re-extracted every `path:line` from `.agent/f255_inventory.md` at `e589ddee` independently of the worker's checker and resolved each against `git ls-tree` and the file's real length at `73d7d6e2` — 78 citations, 50 distinct, 78 of 78 RESOLVE — and the reviewer's own checker REJECTS both a path that is not tracked and a real path at line 99999, so the gate is not vacuous. THE INVENTORY IS ALSO TRUE, WHICH A CITATION GATE CANNOT SHOW: the reviewer re-measured its load-bearing claims at source rather than accepting them. `KNOWN_ROLES` at `role_config.py:56` is the seven-name tuple the inventory lists; the unknown-role branch at line 125 calls `warnings.warn` and does not raise, so WARN-AND-DEFAULT is the real behaviour; `ActionClass` at `command_catalog.py:31` is a `typing.Literal` of exactly the eight members named; `RunEvent.event` at `run_log.py:66` is an unconstrained `str`, so the run-log vocabulary is genuinely open; `EVENT_METADATA_SCHEMAS` holds exactly SEVEN entries, counted by AST rather than by regex after the reviewer's own first regex miscounted them as zero; the `do` group holds fifteen command ids and none is `watch`, and no `teach` command id exists; `pool` occurs twice under `packages/orchestration/`, both an unrelated local in `evidence_index.py`; and `teacher` occurs exactly once repo-wide, in a comment at `tests/docs/test_docs_consistency.py:26`. Every one of those readings matches the inventory. THE ROUND GATE WAS RE-RUN SERIALLY BY THE REVIEWER IN THE PRIMARY CHECKOUT: the four-file state-reader selection exited 0 at `160 passed` and the canary exited 0 at `42 passed`, each equal to the count measured at `6c47a490`. THE RANGE IS WHAT THE HANDBACK DECLARES: six paths over seven single-parent commits, every `+/-` cell byte-identical to `git diff --numstat` at 250/0, 199/335, 4/0, 2/0, 282/0 and 18/16 with C5's own 66/47 routed to the round report; a maximum insertion column of 282, under the 500 cap; `git diff --name-only` scoped to `apps/ packages/ tests/ docs/ scripts/` EMPTY, so constraint 7 of that block held and nothing outside `.agent/` moved; zero marker lines in every written file; and a handback of 86 lines, inside the ≤100 its seven-commit table earns. THE REFLOG WAS REPORTED IN THE CORRECTED FORM R-0601 ORDERS, as two measured claims rather than one universal — seven commit-producing entries reading `commit`, and zero entries whose OPERATION PREFIX carries a rewrite word — and the reviewer re-measured both. FOUR DEVIATIONS WERE DECLARED AND ALL FOUR ARE CORRECT: the line-anchored `Landed:` count is 0 at both ends while the unanchored substring count is 19 at both ends and 21 after RECORDR1, which quotes the token twice in prose, and reporting both readings is the R-0600 discipline applied unprompted; C5 cannot table its own commit; the inventory was corrected after the worker's own citation checker rejected a bare filename, BEFORE C3 was committed, which is the gate working as designed rather than a defect; and the handback correctly makes no claim of compliance with the 800-token cap that R-0602 registers as dead letter.
<<<END RECORDR2

<<<SLICE DECISIONS255
## DECISION F255 D1 — the teacher joins BOTH role vocabularies (2026-08-20)

CHOSEN. `teacher` is added to `KNOWN_ROLES` in
`packages/orchestration/role_config.py`, taking it from seven names to eight,
AND to the `ConventionsRole` enum in
`packages/orchestration/role_conventions.py`, because the teacher needs a model
(the first vocabulary) and a persisted behaviour document (the second). The
frozen pin `test_all_seven_roles_present` in
`tests/orchestration/test_role_config.py` is renamed and its tuple extended IN
THE SAME COMMIT as the vocabulary change, never in a follow-up: a ledger-style
count and its test pin land together (finding R-0151).

MEASURED at R2, which is why this is a decision and not a preference: the
registration says the teacher is "resolved through the same role_config
mechanism as orchestrator/worker/reviewer", but `worker` is NOT in
`KNOWN_ROLES` — it exists only as `ConventionsRole.WORKER`. The registration
names two vocabularies as if they were one, and this decision separates them.

DELIBERATELY NOT EXTENDED: `_ROLE_OVERRIDE_ROLES` in `apps/cli/commands/do_cmd.py`
and the `_ROLE_PROMPT_KEYS` / `_ROLE_ESTIMATED_KEYS` maps in
`packages/orchestration/token_cost_policy.py`. Those three lists describe the
roles that perform the BUILD and carry per-role prompt columns; the teacher
neither builds nor is charged against those columns, and its spend is attributed
by the ledger `role` column instead (DECISION F255 D3). A role added to a list
whose meaning it does not share is how a vocabulary rots.

ALTERNATIVE CONSIDERED and rejected: add `teacher` to `KNOWN_ROLES` alone.
Rejected because `role_conventions.py` is where a role's rules are persisted,
and a teacher with no conventions document is a prompt with no written rules —
exactly the state AGENTS.md exists to prevent for every other role.

Reverse this decision by deleting this section and removing the name from both
tuples, which restores the seven-name pin.

## DECISION F255 D2 — F255 does NOT close its own event-vocabulary dependency (2026-08-20)

CHOSEN. Stage 1 narration keys to an EXPLICITLY ENUMERATED subset of run-log
event names, declared in ONE place inside the teacher's own module and pinned by
a test. Every event outside that set is narrated as unknown, under the feature's
own honesty rule for grounding source 1 — "asserts only what evidence shows,
says unknown where it is silent". F255 does NOT build a repo-wide named-event
registry and does NOT make the emitter enforce one.

MEASURED at R2: `RunEvent.event` at `packages/orchestration/run_log.py:66` is an
unconstrained `str` and `RunLogWriter.log` validates nothing; 39 distinct event
names are emitted from 14 files; `EVENT_METADATA_SCHEMAS` covers the METADATA
KEYS of seven event types and has ZERO production callers. The registration's
declared dependency, "stable ledger event vocabulary (Tier 2)", is therefore NOT
satisfied today, and this decision refuses to pretend otherwise.

ALTERNATIVE CONSIDERED and rejected: close the dependency first — introduce the
registry and make every emitter use it. Rejected for THIS feature because it
edits the 14 emitting files and every event name in the repository, which is a
Tier 2 infrastructure feature in its own right and is nowhere in F255's scope.
Widening a Tier 5 feature into a Tier 2 refactor is the scope drift AGENTS.md
forbids, and doing it inside a teaching feature would bury it.

CONSEQUENCE, stated plainly so no later text overclaims: F255's narration is
only as stable as the names it enumerates. A rename in an unrelated module
degrades narration for that event to "unknown" rather than breaking the run —
which is the failure mode the honesty rule prefers — and the enumerated set is a
test pin, so such a rename surfaces as a RED TEST rather than as silence.

Reverse this decision by deleting this section, which reopens the choice between
an enumerated subset and a repo-wide registry.

## DECISION F255 D3 — teacher spend is REPORTED per role, and no new limit axis is built (2026-08-20)

CHOSEN. Teacher spend is separated by the `role` column that already exists on
the F103 ledger's `calls` table, and is read with `query_cost(by="role")`. F255
adds NO new budget limit and NO new limit axis. Stage 1 is declared zero-token
and charges nothing; Stage 2 charges under the role name `teacher`.

MEASURED at R2: a "pool" concept does not exist anywhere in
`packages/orchestration/` — the only two hits are an unrelated local variable.
Attribution runs on `_CALL_COLUMNS`'s `role` field; `COST_GROUP_KEYS` is exactly
`("role", "model", "day")`; and all five enforceable limits in `_LIMIT_ORDER`
are JOB-scoped, none of them per-role.

WHAT THIS DECISION DELIBERATELY DOES NOT RULE, and says so rather than letting a
later round discover it: the registration's phrase "its OWN budget pool" is
satisfied in the REPORTING sense and explicitly NOT in the LIMIT sense. No text
in this feature may claim the teacher is capped. If a cap is wanted later it is
a new axis in `budget_guard.py`, ruled then, on its own evidence.

ALTERNATIVE CONSIDERED and rejected: add a per-role limit axis now. Rejected
because it changes the enforcement path that every job already depends on, in
order to cap a role that by construction cannot influence the run — the largest
blast radius in the feature bought for the smallest gain.

Reverse this decision by deleting this section, which reopens per-role limits.

## DECISION F255 D4 — read-only is proven BEHAVIOURALLY, because the annotation proves nothing (2026-08-20)

CHOSEN. The teacher's hard read-only invariant is proven by a BEHAVIOURAL test —
the command runs and the bytes on disk are unchanged — modelled on
`tests/orchestration/test_job_budgets.py:1352`, whose comment states the standard
exactly: `action_class="read_only"` has to be true of the bytes on disk. The
`action_class="read_only"` declaration is carried as well, but it is the label,
never the guarantee.

MEASURED at R2: `ActionClass` is a `typing.Literal` at
`apps/cli/command_catalog.py:31`; a `Literal` annotation is not checked when the
frozen dataclass is constructed; and NO code path anywhere branches on
`action_class == "read_only"` to permit or deny an operation. The only
non-declaration uses are one serialization and one comment. Enforcement today is
the test suite, and only one test in it is behavioural.

CONSEQUENCE: the registration's "Hard invariants: ActionClass read_only" names a
DECLARATION. Any later sentence in this feature claiming that the annotation
enforces the invariant is false, and this decision is the reason a reviewer may
say so without re-deriving it.

ALTERNATIVE CONSIDERED and rejected: build catalog-wide runtime enforcement, so
`read_only` is checked at dispatch for every command. Rejected as out of scope —
it is a trust-core change touching every command's dispatch path, and F255 is a
Tier 5 teaching feature. It is worth doing: it is registered as a closure
candidate of this feature rather than silently dropped.

Reverse this decision by deleting this section.

## DECISION F255 D5 — F255 ships `remedy teach` and does NOT build `do watch` (2026-08-20)

CHOSEN. The feature's CLI surface is `remedy teach`. F255 does NOT build
`remedy do watch`, and it STATES its own isolation rules instead of inheriting
rules that were never written. The rules it states, taken from what the run log
actually is: the teacher opens the append-only JSONL run log READ-ONLY, re-reads
it whole through the existing production reader
`packages/orchestration/timeline.py:68`, tolerates a malformed trailing line by
dropping that line, holds no lock, and has no write path to the run at all.

MEASURED at R2: the `do` group holds fifteen commands and none is `watch`; no
`teach` command exists; and the searches that establish both are recorded in
`.agent/f255_inventory.md`. The registration's phrase "same isolation rules as
watch" therefore refers to rules that do not exist, and its CLI phrase
`remedy do watch --learn` names a command that does not exist.

ALTERNATIVE CONSIDERED and rejected: build `do watch --learn` as the
registration literally says. Rejected because `do watch` is a general live-run
viewer that is useful independently of teaching; building it inside F255 would
silently widen a teaching feature into a cockpit feature, which the
registration's own Non-goals forbid — "cockpit panel ships with Tier 5, not
before". A feature that grows a second feature inside itself cannot be reviewed
against its own Done condition.

CONSEQUENCE: the registration's CLI phrase is SUPERSEDED. R4 writes the
superseding text into `docs/roadmap/features/T5_F255.md` itself, so the feature
file and this ruling never disagree on disk — a decision that lives only here
while the feature file still says `do watch` is the R-0417 staleness class.

Reverse this decision by deleting this section and restoring the `do watch`
phrasing in the feature file.

## DECISION F255 D6 — the handback token cap is withdrawn; the LINE cap is the operative bound (2026-08-20)

CHOSEN, ruling finding R-0602. The sentence "Hard cap: this file stays ≤800
tokens — ≤1600 in the >10-commit LARGE case" is REMOVED from
`docs/agents/handback_template.md`. The line cap in that same file — ≤60, ≤100
when a >5-commit table requires it, ≤160 in the LARGE case — becomes the single
operative bound on a handback's size, and the template says so explicitly.

MEASURED: over the twelve most recent commits that rewrote `.agent/handoff.md`,
every one exceeds the token cap, in a band from 1306 to 2983 by the chars/4
estimate — 1.6x to 3.7x — while the LINE cap in the same document is met by all
of them. Two caps on one artifact disagreed, and only one was ever obeyed.

WHY WITHDRAW RATHER THAN RAISE. Raising the number to fit current practice
blesses whatever the last round happened to write and must be raised again the
next time a bundle grows. The line cap already scales with commit count, is
measured with `wc -l` and needs no tokenizer, whereas a token cap depends on an
estimator nobody has agreed on — chars/4 is itself a guess, and the true count
differs per model. A cap that cannot be measured identically by two readers
cannot be enforced by either.

ALTERNATIVE CONSIDERED and rejected: restate the cap at 3000 tokens. Rejected
for the reason above — it is the current maximum dressed as a rule, and it would
still leave two caps that can disagree.

WHERE THIS LANDS: the template edit is NOT made by this round, whose change set
is `.agent/` only. It lands in the docs round that follows the feature-file
amendment, and until it lands no round is failed against the 800-token number
and no handback claims to meet it.

Reverse this decision by deleting this section and restoring the removed
sentence.
<<<END DECISIONS255

<<<SLICE PLAN255R3
# Plan — F255 Teacher role

Branch: feature/f255-teacher-role, cut from `main` at b35d350b, the merge commit
of pull request #207. No pull request is open for this branch; on this project
the PR is created by the closure round.
`.agent/live_review.md` is the source of truth for the open set, for the next
free finding id and for the round map; this file repeats none of them.

## Goal
A fourth configured role, `teacher`, that narrates a running mission and answers
operator questions about the operator's own code, and never influences the run.
DONE when passive narration keyed to ledger events (Stage 1, deterministic
templates, zero tokens) and on-demand Q&A (Stage 2, through the teacher role's
own model) both work, the three grounding sources are never mixed silently,
teacher spend is reported as its own role in the F103 ledger, and the read-only
invariant is proven behaviourally.

## Current Step
R3: record the R2 verdict and land six DECISIONs — the role vocabularies, the
unmet event-vocabulary dependency, spend reporting, behavioural read-only proof,
`remedy teach` in place of `do watch`, and the withdrawal of the dead handback
token cap. Nothing is built and the feature file is not amended this round.

## Next Steps
1. R4 AMENDS `docs/roadmap/features/T5_F255.md` from these rulings, adding the
   Design, Task slicing, Acceptance and Do-not-touch sections its registration
   stub has never carried, and replacing the superseded `do watch` phrasing so
   the file and DECISION F255 D5 never disagree on disk.
2. THE DOCS ROUND AFTER IT applies DECISION F255 D6 to
   `docs/agents/handback_template.md`, removing the withdrawn token cap.
3. R6 ONWARD BUILDS THE T-SLICES the amendment names, Stage 1 before Stage 2,
   the role vocabularies first because everything else depends on them.

## Risks
- THE REGISTRATION NAMES GROUND THAT DOES NOT EXIST, and R2 measured exactly
  which: no stable event vocabulary, no budget pool, no `watch` command, and a
  read-only annotation nothing enforces. The DECISIONs rule each gap rather than
  building around it, but each ruling narrows what "DONE" can honestly mean.
- STAGE 1 MUST STAY ZERO-TOKEN TO BE WORTH HAVING. If narration quietly starts
  calling a model, the feature loses both its cost story and its offline story.
- READ-ONLY IS PROVEN BY ONE TEST SHAPE. If that test is weak, the feature's
  hardest invariant is decorative — DECISION F255 D4 is only as good as the
  test R6 writes.
<<<END PLAN255R3

Done when:
G1 HYGIENE. `.agent/STOP` read from disk before C0a and reported absent or
   present; branch is feature/f255-teacher-role; `git status --porcelain` EMPTY
   after every commit and at the handback; `git worktree list` reports the
   primary checkout alone. No reading is taken by overwriting a file in the
   primary checkout — use `git show <sha>:<path>`.
G2 TRANSPORT. Report the sha256 and the byte and line counts of
   `.remedy-wt/f255-r3.md`, of `.agent/authored/f255-r3.md` at C0a and of
   `.agent/last_block.md` at C0b, and state whether all three are EQUAL.
G3 SLICES EXTRACTED, NEVER RETYPED. Report the extraction command and the
   sha256, byte count AND line count of each slice, naming the newline
   convention used (R-0600).
G4 THE VERDICT ENTRY, AND THE SETS THAT MUST NOT MOVE. C1 appends RECORDR2
   preceded by exactly one blank line. Report that the pre-C1 blob is a
   byte-exact PREFIX of the post-C1 blob, the remainder's sha256, byte and line
   counts, and that the blank separator is present; then a SECOND, independent
   paragraph-level split whose LAST unit is RECORDR2, with that unit's sha256
   under BOTH newline conventions and the byte count of each. Run a negative
   control — one character of the expected remainder mutated — and report that
   BOTH readings reject it. With `^- R-\d+ — ` as registered and
   `^Done: R-\d+ — ` as resolved, report both counts plus open and
   line-anchored `Landed:` at the base and at C1: the reviewer measured
   178 / 0 / 178 / 0 at `73d7d6e2` and constraint 5 orders all four UNCHANGED.
   Report that `Gate: R3 — the R2 entry.` occurs 1x, is the LAST line beginning
   `Gate: R`, and that no `Gate: R` header key repeats.
G5 THE DECISIONS. C2 appends DECISIONS255 to `.agent/decisions.md` preceded by
   exactly one blank line. Report that the pre-C2 blob is a byte-exact PREFIX of
   the post-C2 blob and that the remainder equals a blank line followed by the
   slice, byte for byte. Report the count of lines matching `^## DECISION F255 D`
   in that file at the base and at C2 — the reviewer measured 0 at the base and
   the append adds SIX, D1 through D6 — and report each heading verbatim, in
   order, with its D-number. Report that no heading text in the file occurs
   twice.
G6 THE PLAN. `.agent/plan.md` at C3 byte-equals PLAN255R3; report its sha256,
   byte and line counts, that the line count is under 50, and that `## Goal`,
   `## Next Steps` and a roadmap F-id all occur in it.
G7 THE ROUND GATE, serially in the PRIMARY checkout, never two pytest processes
   at once. This round rewrites `.agent/` state and touches no source file, no
   test and nothing under docs/, so the four state-reader files are the gate,
   plus the canary. Report the exact command, exit code and tail of each:
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
   The reviewer measured exit 0 at 160 passed and exit 0 at 42 passed, both at
   `73d7d6e2` in the primary checkout.
G8 CHANGE SET, HISTORY AND CAPS. Report `git diff --name-only 73d7d6e2..HEAD`
   and state that it equals the Change list with no path on either side alone.
   Report that the SAME command scoped to `apps/ packages/ tests/ docs/ scripts/`
   is EMPTY, which is what constraint 6 means in one measurement. Report that
   each of the eight paths the Change section names as untouched is PRESENT at
   the base and absent from the range; that every commit in the range has one
   parent; and each commit's insertion column from `git diff --numstat`, every
   one under 500, with the same `+/-` cells appearing byte-identically in the
   handback's `## Commits` table. C4's own cell and the complete change set
   belong to the round report, not to C4.
   THE REFLOG IS REPORTED AS TWO MEASURED CLAIMS, NOT ONE UNIVERSAL (R-0601):
   the count of this round's reflog entries that PRODUCED a commit and read
   `commit`, which must equal the number of commits the round makes; and the
   count of this round's entries, navigation included, whose OPERATION PREFIX —
   the text before the first colon of `git reflog --format=%gs` — contains
   `amend`, `reset`, `rebase` or `cherry`, which must be 0. Read the prefix,
   never the whole line: commit subjects in this project contain the word
   `reset`, and scanning the whole line reports false rewrites.
G9 NO MARKER LEAKED. Report the count of LINES beginning `<<<SLICE ` or
   `<<<END ` in `.agent/live_review.md` at C1, `.agent/decisions.md` at C2,
   `.agent/plan.md` at C3 and `.agent/handoff.md` at C4. Every count must be 0.
G10 THE PUSH. After C4, `git push` and report its real output. Do NOT create a
   pull request and do NOT wait on the CI run the push starts (constraint 9).

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             all seven mandated headings in the template's order, the
             item-status table for the C0a..C4 bundle, the `## Commits` table G8
             pins, and one LINE per gate rather than its transcript (R-0582).
             Do NOT claim compliance with the template's 800-token cap: DECISION
             F255 D6, which this round lands, withdraws it. Stay inside the LINE
             cap your commit count earns. Its `## Next` section names the next
             session's FIRST action as Phase 1 rule 1, the `.agent/STOP`
             re-read, and its SECOND as R4, the feature-file amendment — in that
             order — and states that R3 awaits review. There is no open pull
             request. The full transcripts go in the round report you return,
             never in the file. The handback also carries this Fortschritt line
             verbatim, because with no relay you never see the operator brief
             that would otherwise state it (R-0418):
             Fortschritt: ~8 % (F086 merged · F255 claimed · R2 measured the
             ground · R3 ruled six DECISIONs · R4 amends the feature file next)
             — Schätzung
──────────────────────────────────────────────────────────────
