── STEP R4 — F255 Teacher role ────────────────────────────────
Goal:        Record the R3 verdict, and AMEND `docs/roadmap/features/T5_F255.md`
             from the six rulings R3 landed — adding the Design, Task slicing,
             Acceptance, Edge cases, Orchestrator brief and Do-not-touch sections
             its registration stub has never carried, and naming on disk the
             registered phrases the rulings supersede, so the feature file and
             `.agent/decisions.md` never disagree. Still no code: R5 builds.

Bundle:      C0a save this block · C0b mirror it · C1 record the R3 verdict ·
             C2 amend the feature file · C3 the plan · C4 the handback, then
             push.

Change:      Exactly these paths, in this order, one commit each.
             C0a `.agent/authored/f255-r4.md`
             C0b `.agent/last_block.md`
             C1  `.agent/live_review.md`
             C2  `docs/roadmap/features/T5_F255.md`
             C3  `.agent/plan.md`
             C4  `.agent/handoff.md`
             Nothing else is created, modified, deleted or staged. NO source
             file and NO test changes this round. These paths are PRESENT at the
             base and must stay untouched: `docs/roadmap/STATUS.md`,
             `docs/roadmap/ROADMAP.md`, `docs/agents/handback_template.md`,
             `packages/orchestration/role_config.py`,
             `apps/cli/command_catalog.py`, `.agent/decisions.md`,
             `.agent/context.md`, `.agent/f255_inventory.md`.

Constraints:
1. NO SLICE IS EDITED. Every text between `<<<SLICE x` and `<<<END x` is applied
   byte for byte. A slice you believe is wrong is applied anyway and DECLARED in
   the handback; you never repair it silently. Marker lines never reach a target.
2. TRANSPORT. `.remedy-wt/f255-r4.md` is this block on disk. C0a copies that
   FILE to `.agent/authored/f255-r4.md` — copy it, never retype it — and C0b
   copies the same file to `.agent/last_block.md`. Prove all three byte-EQUAL;
   the reviewer stated the expected digest when it delegated, and that digest
   cannot appear in this file because this file is what it digests.
3. NO FROM/TO PAIR EXISTS THIS ROUND. RECORDR3 and AMEND255 are APPENDS and
   PLAN255R4 is a WHOLE-FILE replacement. The reviewer ran the containment test
   over this block's slices before emission and found no pair to classify, so no
   FROM count is ordered anywhere below.
4. THE FEATURE FILE IS AMENDED BY APPEND ONLY. AMEND255 is appended to
   `docs/roadmap/features/T5_F255.md` preceded by exactly one blank line. NOT ONE
   EXISTING BYTE OF THAT FILE CHANGES — in particular its line 1 title and its
   lines 2-4 dependency block, which `packages/orchestration/roadmap_index.py`
   parses, and its `## Scope (registered verbatim, plan0806 2026-08-06)` block,
   which is the operator's registration record and is never rewritten. The
   supersessions are stated in the appended text, not by editing the registered
   words. G5 proves the untouched prefix byte for byte.
5. THE LEDGER APPEND IS BLANK-SEPARATED and RECORDR3 is a `Gate:` paragraph, so
   it adds no `- R-` line and no `Done:` line. This round registers no finding:
   the registered and resolved counts must both come back UNCHANGED, which G4
   orders measured rather than assumed.
6. YOU NEVER WRITE A `Done:` OR A `Landed:` PARAGRAPH.
7. NOTHING IS BUILT THIS ROUND. You add no role, no command, no config key and
   no test. The amendment DESCRIBES the T-slices; R5 executes the first of them.
8. `.agent/STOP` is read from disk before C0a. If it exists, stop and write the
   handback instead.
9. `git status --porcelain` is EMPTY after every commit. No worktree is created
   this round, because no destructive check is ordered.
10. YOU DO NOT WAIT ON ANY CI RUN and you report no run's conclusion.

<<<SLICE RECORDR3
Gate: R4 — the R3 entry. R3 PASSED with NO finding against its work and none against its block. Every gate the R3 block ordered was RE-EXECUTED by the reviewer over `73d7d6e2..a0b8e542` rather than read from the handback, and every one holds. THE TRANSPORT HELD IN THE PRIMARY FORM: `.remedy-wt/f255-r3.md`, the committed `.agent/authored/f255-r3.md` at `f728166b` and the committed `.agent/last_block.md` at `8228c53f` are byte-EQUAL at sha256 afb54bafa34745eae85ee5ea82cffebca33f85c620818e02e416cafc987aaf09 over 28352 B and 384 lines, the digest stated at delegation. THE VERDICT ENTRY LANDED AS AN APPEND AND THE SETS DID NOT MOVE: the pre-C1 blob at `73d7d6e2` is a byte-exact PREFIX of the post-C1 blob at `b4def48c`; the 2-line remainder is a blank line followed by RECORDR2 at sha256 aba1b59ed1e22d34 over 4788 B with the separator PRESENT; an independent paragraph split yields RECORDR2 as its LAST unit at sha256 80ea3987f4fd3b19 over 4787 B and 1 line with the trailing newline INCLUDED and at sha256 74c6e6a02a4d3a48 over 4786 B with it STRIPPED, both conventions given per R-0600; registered 178, resolved 0, open 178 and line-anchored `Landed:` 0 at BOTH ends, which is what a `Gate:` paragraph must produce; and `Gate: R3 — the R2 entry.` occurs 1x, is the LAST line beginning `Gate: R`, with the three header keys all distinct. THE SIX RULINGS LANDED VERBATIM AND BY APPEND, WHICH MATTERS BECAUSE `.agent/decisions.md` IS 387 KB OF STANDING RULINGS THAT A REWRITE COULD SILENTLY DAMAGE: the pre-C2 blob is a byte-exact PREFIX of the post-C2 blob at `0b018e32`, the 186-line remainder equals a blank line followed by DECISIONS255 byte for byte, `^## DECISION F255 D` reads 0 at the base and 6 at C2, the six headings are D1 through D6 in order, and NO heading text in that file occurs twice across all 389 of them. THE PLAN IS BYTE-EXACT: `.agent/plan.md` at `5ce2edd7` equals PLAN255R3 at 43 lines, under the 50-line cap, carrying `## Goal`, `## Next Steps` and the feature id. THE ROUND GATE WAS RE-RUN SERIALLY BY THE REVIEWER IN THE PRIMARY CHECKOUT: the four-file state-reader selection exited 0 at `160 passed` and the canary exited 0 at `42 passed`, each equal to the count measured at `73d7d6e2`. THE RULING ROUND RULED AND BUILT NOTHING, WHICH IS ITS CENTRAL CONSTRAINT: `git diff --name-only 73d7d6e2..a0b8e542` scoped to `apps/ packages/ tests/ docs/ scripts/` is EMPTY, all eight paths the Change section names as untouched are PRESENT at the base and ABSENT from the range, and the range is exactly six `.agent/` paths over six single-parent commits. THE CAPS AND THE HISTORY HOLD: every `+/-` cell is byte-identical to `git diff --numstat` at 384/0, 327/193, 2/0, 186/0 and 23/22 with C4's own 71/57 routed to the round report; the maximum insertion column is 384, under the 500 cap; zero marker lines reached any written file; the handback is 100 lines, exactly at the ≤100 its six-commit table earns; and the reflog reads six commit-producing entries with prefix `commit` and ZERO entries whose operation prefix carries a rewrite word. THE WORKER DECLARED SIX DEVIATIONS AND ALL SIX ARE CORRECT, one of them notable for its honesty: it reported that the whole-line reflog control would ALSO have read 0 this round, because none of its six commit subjects happens to contain the word `reset`, so the false-hit hazard R-0601 names did not fire here — reporting a control that did not discriminate, rather than presenting it as evidence, is the discipline R-0327 asks for and it was volunteered rather than ordered.
<<<END RECORDR3

<<<SLICE AMEND255
## Amendment status (F255 R3/R4, 2026-08-20)

The Scope block above is the operator's registration record and is preserved
verbatim. Three of its phrases were measured against the code at R3 and found to
name ground that does not exist; each is SUPERSEDED by a ruling in
`.agent/decisions.md`, and the superseding text is stated here so that this file
and those rulings never disagree on disk.

- "resolved through the same role_config mechanism as orchestrator/worker/
  reviewer" — SUPERSEDED by DECISION F255 D1. `worker` is not a member of
  `KNOWN_ROLES`; it is a member of the separate `ConventionsRole` enum. The
  teacher joins BOTH vocabularies, for the two different things they carry.
- "Dependencies: stable ledger event vocabulary (Tier 2)" — SUPERSEDED by
  DECISION F255 D2. No such vocabulary exists: run-log event names are free
  strings. F255 does not build one; it narrates an enumerated subset and says
  "unknown" elsewhere.
- "`remedy do watch --learn`" and "same isolation rules as watch" — SUPERSEDED
  by DECISION F255 D5. No `watch` command exists, so no isolation rules exist to
  inherit. The surface is `remedy teach`, and the isolation rules are stated
  below rather than inherited.

The measurement behind all three is `.agent/f255_inventory.md`, written at R2,
where every claim carries a citation resolved against the tree at `73d7d6e2`.

## Design (ruled at R3)

A fourth configured role, `teacher`, that reads and explains and never writes.
Two stages, deliberately unequal in cost:

STAGE 1 — passive narration. Deterministic templates keyed to an ENUMERATED set
of run-log event names, declared in one place inside the teacher module and
pinned by a test. Zero tokens, no network, no model. An event outside the set is
narrated as unknown rather than guessed at — the honesty rule applied to the
feature's own blind spot.

STAGE 2 — on-demand Q&A through the teacher role's own model, over a small
context: the relevant ledger slice plus the code location asked about, behind a
cache-stable prefix.

THREE GROUNDING SOURCES, NEVER MIXED SILENTLY, each with its own honesty rule:
(1) ledger and evidence — what is happening; asserts only what the evidence
shows and says unknown where it is silent; (2) workspace code, read-only — what
this function or file does; explains code that exists and never invents; (3) the
model's own language and concept knowledge — what a term means; ordinary tutor
knowledge, and explicitly not a claim about Remedy's state. Every answer labels
which source it speaks from.

ISOLATION, STATED HERE BECAUSE THERE IS NOTHING TO INHERIT (DECISION F255 D5):
the teacher opens the append-only JSONL run log READ-ONLY, re-reads it whole
through the existing production reader `load_run_events`, tolerates a malformed
trailing line by dropping that line, holds no lock, subscribes to nothing, and
has no write path to the run. There is no follow or tail API in Remedy today and
this feature does not add one.

COST SEPARATION (DECISION F255 D3): teacher spend is attributed by the `role`
column the F103 ledger already carries and is read with `query_cost(by="role")`.
Stage 1 charges nothing because it calls no model. No budget LIMIT is scoped to
the teacher; the separation is reporting, not a cap, and no text in this feature
may claim otherwise.

## Task slicing

- **T001** the role vocabularies. `teacher` joins `KNOWN_ROLES` (seven names to
  eight) and `ConventionsRole`, with its conventions document; the frozen pin
  `test_all_seven_roles_present` is renamed and extended IN THE SAME COMMIT as
  the tuple it guards. A `teacher.model` config key modelled on the existing
  `orchestrator.model` spec.
- **T002** Stage 1 narration: the enumerated event-name set in one place, the
  deterministic templates, the read-only run-log reader, the unknown-event path,
  and the `remedy teach` surface that prints it.
- **T003** the read-only invariant, proven behaviourally (DECISION F255 D4): the
  bytes on disk are unchanged across a teacher command, in the shape of
  `tests/orchestration/test_job_budgets.py`'s persisted-job test, plus the
  `action_class="read_only"` declaration in the command catalog.
- **T004** Stage 2 Q&A: `remedy teach ask`, the small context, the source
  labelling, the level dial, and spend recorded under the role name `teacher`.

## Acceptance

- `KNOWN_ROLES` holds eight names, the renamed pin asserts all eight, and
  `resolve_role_config("teacher")` returns a config WITHOUT emitting the
  unknown-role warning.
- Stage 1 narration for an enumerated event is DETERMINISTIC: two runs over the
  same run log produce byte-identical output, and the token ledger records no
  call for either.
- An event name outside the enumerated set is narrated as unknown — a test
  drives an unregistered name and asserts the narration neither invents a
  description nor raises.
- READ-ONLY, behaviourally: the run's files are byte-identical before and after
  a narrate and after an ask.
- Stage 2 records exactly one ledger call attributed to role `teacher`, and
  `query_cost(by="role")` reports teacher spend separately from mission spend.
- Every answer names its grounding source; a test asserts that a
  ledger-grounded answer makes no claim about code it did not read, and that a
  code-grounded answer makes no claim about run state.
- The level dial changes DEPTH, not FACTS: the same question at two levels
  yields answers whose claim set is the same.

## Edge cases & assumption defaults (A9)

- An empty or absent run log narrates as "nothing recorded yet", never as an
  error and never as an invented summary.
- A torn final JSONL line is dropped, matching the existing reader's behaviour;
  the narration does not report a count it cannot support.
- With no model configured, Stage 2 refuses with an honest message and Stage 1
  keeps working, because Stage 1 is offline by construction.
- A question about code outside the workspace is answered from source (3), the
  model's own knowledge, and labelled as such — never dressed as a claim about
  this project.

## Orchestrator brief

T001 first: everything else depends on the role existing. Then T002 with T003
in the same order, because a read-only feature whose read-only-ness is unproven
is the failure this feature is most likely to have. T004 last, and only once the
grounding-source labelling of T002 is real — Stage 2 is where mixing sources
would do the damage. Remedy deliberately does not add a follow/tail API here.

## Do not touch

Any write access to the run, mission steering, and any influence on
orchestrator, worker or reviewer decisions. The cockpit panel (Tier 5, not
before). `remedy do watch` — not built by this feature (DECISION F255 D5). A
repo-wide run-log event registry (DECISION F255 D2). Per-role budget LIMITS
(DECISION F255 D3). Catalog-wide runtime enforcement of `action_class`
(DECISION F255 D4) — worth doing, registered as a closure candidate of this
feature, and out of scope here.
<<<END AMEND255

<<<SLICE PLAN255R4
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
R4: record the R3 verdict and amend `docs/roadmap/features/T5_F255.md` by
APPEND — the Design, Task slicing, Acceptance, Edge cases, Orchestrator brief
and Do-not-touch sections, plus the three supersessions the R3 rulings require.
Nothing is built this round and no registered word is rewritten.

## Next Steps
1. R5 APPLIES DECISION F255 D6 to `docs/agents/handback_template.md`, removing
   the withdrawn 800-token cap and stating that the LINE cap is the operative
   bound. It is a docs round and gates tests/docs/ accordingly.
2. R6 BUILDS T001 — the role vocabularies — including the renamed seven-to-eight
   pin in the SAME commit as the tuple it guards.
3. R7 ONWARD BUILDS T002 AND T003 TOGETHER, Stage 1 narration with its
   behavioural read-only proof, then T004 last.

## Risks
- THE AMENDMENT IS NOW THE SPEC. If a T-slice drifts from it, the drift is a
  finding rather than a preference, which is the point of writing it down.
- STAGE 1 MUST STAY ZERO-TOKEN TO BE WORTH HAVING. If narration quietly starts
  calling a model, the feature loses both its cost story and its offline story.
- READ-ONLY IS PROVEN BY ONE TEST SHAPE. If that test is weak, the feature's
  hardest invariant is decorative — DECISION F255 D4 is only as good as the
  test T003 writes.
<<<END PLAN255R4

Done when:
G1 HYGIENE. `.agent/STOP` read from disk before C0a and reported absent or
   present; branch is feature/f255-teacher-role; `git status --porcelain` EMPTY
   after every commit and at the handback; `git worktree list` reports the
   primary checkout alone. No reading is taken by overwriting a file in the
   primary checkout — use `git show <sha>:<path>`.
G2 TRANSPORT. Report the sha256 and the byte and line counts of
   `.remedy-wt/f255-r4.md`, of `.agent/authored/f255-r4.md` at C0a and of
   `.agent/last_block.md` at C0b, and state whether all three are EQUAL.
G3 SLICES EXTRACTED, NEVER RETYPED. Report the extraction command and the
   sha256, byte count AND line count of each slice, naming the newline
   convention used (R-0600).
G4 THE VERDICT ENTRY, AND THE SETS THAT MUST NOT MOVE. C1 appends RECORDR3
   preceded by exactly one blank line. Report the PREFIX property, the
   remainder's sha256, byte and line counts, and that the blank separator is
   present; then a SECOND, independent paragraph-level split whose LAST unit is
   RECORDR3, with that unit's sha256 under BOTH newline conventions and the byte
   count of each. Run a negative control — one character of the expected
   remainder mutated — and report that BOTH readings reject it. Report
   registered, resolved, open and line-anchored `Landed:` at the base and at C1:
   the reviewer measured 178 / 0 / 178 / 0 at `a0b8e542` and constraint 5 orders
   all four UNCHANGED. Report that `Gate: R4 — the R3 entry.` occurs 1x, is the
   LAST line beginning `Gate: R`, and that no `Gate: R` header key repeats.
G5 THE FEATURE FILE IS AMENDED WITHOUT LOSING A BYTE. This is the round's
   central gate. Report that the base blob of `docs/roadmap/features/T5_F255.md`
   at `a0b8e542` — 2730 B over 47 lines, a byte count and not a character count,
   which differ here because the file carries multi-byte UTF-8 — is a byte-exact
   PREFIX of the C2 blob,
   and that the remainder equals a blank line followed by AMEND255 byte for
   byte. Report line 1 and lines 2-4 of the C2 blob VERBATIM and state that they
   are identical to the same lines at the base, because
   `packages/orchestration/roadmap_index.py` parses them. Report that the
   `## Scope (registered verbatim, plan0806 2026-08-06)` heading occurs 1x and
   that the text between it and `## Non-goals` is byte-identical at both ends.
   Report every `## ` heading of the C2 blob in order.
G6 THE ROADMAP INDEX STILL PARSES THE FILE. Report the exit code and output of
     `python3 -m pytest tests/orchestration/test_roadmap_index.py -q -rf`
   and of
     `python3 -m pytest tests/docs/ -q -rf`
   The reviewer measured these WITH AMEND255 ALREADY APPLIED, inside a
   disposable worktree at `a0b8e542`: the roadmap-index selection exit 0 at
   30 passed, and `tests/docs/` exit 0 at 295 passed — 325 together, which is
   also the combined count at the unamended base. Report each separately, with
   its own count, so a regression in either is visible on its own.
G7 THE PLAN. `.agent/plan.md` at C3 byte-equals PLAN255R4; report its sha256,
   byte and line counts, that the line count is under 50, and that `## Goal`,
   `## Next Steps` and a roadmap F-id all occur in it.
G8 THE ROUND GATE, serially in the PRIMARY checkout, never two pytest processes
   at once. This round rewrites `.agent/` state AND touches docs/roadmap/**, so
   both selections gate, plus the canary. Report the exact command, exit code
   and tail of each:
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
   The reviewer measured exit 0 at 160 passed and exit 0 at 42 passed, both at
   `a0b8e542` in the primary checkout. G6's two selections count as the docs
   gate and are not repeated here.
G9 CHANGE SET, HISTORY AND CAPS. Report `git diff --name-only a0b8e542..HEAD`
   and state that it equals the Change list with no path on either side alone.
   Report that the SAME command scoped to `apps/ packages/ tests/ scripts/` is
   EMPTY — note that `docs/` is deliberately NOT in that list this round,
   because C2 changes a file under it. Report that each of the eight paths the
   Change section names as untouched is PRESENT at the base and absent from the
   range; that every commit in the range has one parent; and each commit's
   insertion column from `git diff --numstat`, every one under 500, with the
   same `+/-` cells appearing byte-identically in the handback's `## Commits`
   table. C4's own cell and the complete change set belong to the round report.
   THE REFLOG IS REPORTED AS TWO MEASURED CLAIMS, NOT ONE UNIVERSAL (R-0601):
   the count of this round's reflog entries that PRODUCED a commit and read
   `commit`, which must equal the number of commits the round makes; and the
   count of this round's entries, navigation included, whose OPERATION PREFIX —
   the text before the first colon of `git reflog --format=%gs` — contains
   `amend`, `reset`, `rebase` or `cherry`, which must be 0. Read the prefix,
   never the whole line.
G10 NO MARKER LEAKED. Report the count of LINES beginning `<<<SLICE ` or
   `<<<END ` in `.agent/live_review.md` at C1,
   `docs/roadmap/features/T5_F255.md` at C2, `.agent/plan.md` at C3 and
   `.agent/handoff.md` at C4. Every count must be 0.
G11 THE PUSH. After C4, `git push` and report its real output. Do NOT create a
   pull request and do NOT wait on the CI run the push starts (constraint 10).

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             all seven mandated headings in the template's order, the
             item-status table for the C0a..C4 bundle, the `## Commits` table G9
             pins, and one LINE per gate rather than its transcript (R-0582).
             Do NOT claim compliance with the template's 800-token cap: DECISION
             F255 D6 withdrew it at R3 and R5 removes the sentence. Stay inside
             the LINE cap your commit count earns. Its `## Next` section names
             the next session's FIRST action as Phase 1 rule 1, the
             `.agent/STOP` re-read, and its SECOND as R5, the docs round that
             applies DECISION F255 D6 to `docs/agents/handback_template.md` — in
             that order — and states that R4 awaits review. There is no open
             pull request. The full transcripts go in the round report you
             return, never in the file. The handback also carries this
             Fortschritt line verbatim, because with no relay you never see the
             operator brief that would otherwise state it (R-0418):
             Fortschritt: ~12 % (F086 merged · F255 claimed · ground measured ·
             six DECISIONs ruled · the feature file now carries its Design, Task
             slicing and Acceptance · T001 builds next) — Schätzung
──────────────────────────────────────────────────────────────
