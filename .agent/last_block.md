── STEP T003/3 — F009 ────────────────────────────────────────
Goal:        Close this session's record: persist the R13 verdict and rule the
             T003 round split as DECISION F009 D16, so the next session resumes
             from disk instead of re-deriving it. NO PRODUCTION CODE IS WRITTEN.

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R13 verdict
             · C3 DECISION F009 D16 · C4 handback.

THE ROUND BASE is `1e7539bee16179f6c7d4629198d2d5aff65f609e`. Every gate reading
below said to be "at the round base" is measured against that SHA. C4's own SHA
cannot exist inside C4, so C4 is named by role and the round report carries its
value (R-0371).

THIS ROUND EXISTS BECAUSE A DECISION THAT LIVES ONLY IN A SESSION'S CHAT IS LOST
WHEN THAT SESSION ENDS — the same reason R12 existed. The R13 review reached a
verdict no on-disk record carries, and planning the next round surfaced a
measured fact that changes how T003 must be cut. Persisting both costs one short
round of no new work. NOTHING under `packages/`, `apps/`, `tests/` or `docs/` is
touched.

Change set — these paths and nothing else:
  `.agent/authored/f009-r14.md`
  `.agent/last_block.md`
  `.agent/plan.md`
  `.agent/live_review.md`
  `.agent/decisions.md`
  `.agent/handoff.md`

Slice convention: the authored units below are delimited by `<<<SLICE <NAME>` and
`<<<END <NAME>` lines. Extract each from the COMMITTED C0a blob by those marker
lines, with a script, and apply it programmatically. The marker lines themselves
are never written into any target file. A slice's content is every line strictly
between its two markers, newline-terminated.

<<<SLICE PLANF009R14
# Plan — F009 The single write channel

Branch: feature/f009-single-write-channel, cut from `main` at `ce49348b`, the
merge commit of pull request #209. `.agent/live_review.md` is the source of truth
for the open set, the round map and the finding-id ceiling.

## Goal
Exactly ONE door for UI-initiated change: POST /api/jobs/{jid}/commands validates
against the UI-exposed catalog subset, authenticates with a bearer token plus an
X-Remedy-CSRF double-submit, rate-limits per token and job, deduplicates by
client nonce, and ENQUEUES into the existing decision, approval and control
machinery without touching files, jobs or shells directly. Every other POST, PUT
and DELETE answers 405. DONE when the exposed commands round-trip through their
effects on fixtures, replayed nonces are idempotent, unauthenticated and
cross-site attempts fail closed and are audited as rejected, and a route-walking
test plus an import guard prove no other mutating route exists.

## Current Step
R14 closes this session and writes no production code. It records the R13 verdict
and rules DECISION F009 D16, which cuts the rest of T003 into four rounds and
retires the 501 seam one COMMAND at a time rather than all at once. The plan
approval became the package function `resolve_flight_plan_approval` at R13.

## Next Steps
1. `job.stop` dispatches to `safe_points.request_stop`. That path writes
   DECISION F009 D14's reserved `accepted` outcome, publishes the nonce record
   through `publish_nonce_result` with R-0637's bound applied AT PUBLICATION, and
   moves R-0636's replay token off `not_implemented`. `decision.resolve` keeps
   answering 501 until the round after.
2. Then `decision.resolve` dispatches and the seam is gone; then the
   `command.accepted` SSE event; then the queue-only import guard, the
   per-command side-effect assertions and the route-walking 405 test; then the
   integration gate and closure. DECISION F009 D16 carries the ordering and why.

## Risks
- R-0636 and R-0637 are owed by the round that adds the publish call site, which
  is the FIRST of the four rounds D16 rules and not this one.
- Splitting by command means the door is briefly dispatching one exposed id and
  refusing the other with 501. That is honest — `not_implemented` is exactly what
  the audit records for a command this door has not yet dispatched — but it is a
  state the tests must assert deliberately rather than inherit.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which is
  R-0622 and routes to a paydown branch.
<<<END PLANF009R14

<<<SLICE LEDGER14
Gate: R14 — the R13 entry. R13 PASSED. Every gate was re-run by the reviewer against the committed blobs and every value reproduced, and the round declared no deviation and no objection. TRANSPORT HELD — the reviewer's scratch original, `.agent/authored/f009-r13.md` at `97f364be` and `.agent/last_block.md` at `19aec738` are all sha256 23b45930601cfdfe083f267acb946475c378f41c24331daa7ca4aaa380a63ed8 over 23444 bytes and 351 lines, equal to the digest the task prompt named, and the reviewer's own ordered marker extraction out of the committed C0a blob gives exactly the nine slices PLANF009R13, LEDGER13, EXTRACT, CLIFROM_B, CLITO_B, CLIFROM_A, CLITO_A, CLIFROM_C and CLITO_C, aggregating to 11031 bytes over 149 lines. `.agent/plan.md` at `f9c51774` is BYTE-EQUAL to PLANF009R13 at 41 lines against the 50-line cap, with `^## Goal$` and `^## Next Steps$` matching one line each and `F009` the first `\bF\d{3}\b` match. THE LEDGER APPEND HOLDS UNDER BOTH READERS: at `a97d4004` the round-base blob is a byte-exact prefix and the remainder is exactly a newline plus LEDGER13, sha256 e913b82d376b68f5f21794d4cb9e4127a4ed01d05daa07cede564d9d33606330 over 3823 bytes, the file going 454664 to 458487 bytes and 1082 to 1084 lines, while under the paragraph reader the last blank-line unit of 222 equals the appended slice; the NEGATIVE CONTROL is the reviewer's own, flipping one bit of the byte at offset 454665, which reads `G`, and BOTH readers reject the flip while both accept the true file. THE SETS HELD line-anchored at the round base and at C2: `^- R-\d+ — ` 203 and 203 with every id DISTINCT at each, `^Done: R-\d+ — ` 2 at both, `^Landed: ` 0 at both, `^> Next free id` 0 at both, `^Gate: R\d+ — ` 12 and 13 over that many DISTINCT keys, `^Gate: R13 — ` 0 and 1, max id R-0637, and item 10's rule giving 201 open at `a97d4004`. THE EXTRACTION IS PROVED AS AN EXACT REWRITE OF NOTHING ELSE, which is the strongest reading available and the one that matters for a refactor: at `c204f0b5` the round-base blob of `packages/orchestration/flight_plan.py` is a byte-exact PREFIX, EXTRACT is an exact SUFFIX, the file equals prefix plus slice with nothing between, and the 43 lines that commit's diff ADDS are EXACTLY EXTRACT's lines IN ORDER (R-0531); in `apps/cli/commands/decision.py` each of the three pairs reads FROM 1 then 0 and TO 0 then 1 with the whole-line and indent-agnostic counts AGREEING at every one of the twelve readings, and the file obtained by applying the three replacements to the round-base blob in the order B, A, C is BYTE-EQUAL to what landed — so no byte changed anywhere in that file beyond the three authored pairs. THE SUITES AND THE LINT ARE THE REVIEWER'S OWN, run serially in the primary checkout: `python3 -m ruff check` EXITS 0 over both paths, the four-file approval group EXITS 0 at 191 passed and `tests/cli/test_golden_path.py` EXITS 0 at 42 passed, the 191 being the same count the reviewer measured at the round base BEFORE ordering the gate (R-0364), which is what makes it a behaviour-preservation reading rather than a bare colour. THE PROBE IS THE REVIEWER'S OWN AND WAS RUN BEFORE THE ROUND WAS DELEGATED, in its own disposable worktree over content byte-identical to what landed — the C3 blob of `packages/orchestration/flight_plan.py` is sha256 2298635f1e4151f8d9712786b7d5224223bc642f8cb3c95d6f123cb858a1730d, equal to the file the reviewer probed: against a control of 191 passed, replacing everything after the extracted function's docstring with a raise fails SIXTEEN node ids across three of the four files and leaves 175 passing, and the worker's independently produced list matches the reviewer's id for id. The approval suites therefore genuinely REACH `resolve_flight_plan_approval`, which is the one thing a green refactor suite cannot establish on its own. THE ONE BEHAVIOURAL RISK WAS READ IN THE SOURCE RATHER THAN ARGUED: the extracted function re-reads `job.flight_plan` where the CLI held a local name bound by `getattr`, and `packages/core/models.py` declares `flight_plan` as a plain field rather than a copying property, so both names bind the same dict and the mutate-then-save sequence is unchanged. THE RANGE HELD: six single-parent commits, `git show --numstat` and `git diff --numstat` AGREEING on every cell, insertions 351, 286, 17, 2, 49 and 34, all under the 500-insertion cap of AGENTS.md DECISION F104 D1; the path set from the round base to `c204f0b5` is exactly the six declared paths other than the handback's, the set difference empty in both directions; `^<<<SLICE ` and `^<<<END ` read 0 lines in all four committed targets; `git ls-files .remedy-wt` reads 0; this round's reflog entries classify as `commit` with `amend`, `rebase` and `cherry` 0 each; and the primary checkout is clean with one worktree. THE HANDBACK IS WHOLE: 82 lines against the 100 a bundle of more than five commits allows, every mandated section present, an item-status table with exactly one row for each of C0a through C4, the round base SHA present, one line per gate, and the Fortschritt line verbatim.
<<<END LEDGER14

<<<SLICE DECISION16
## DECISION F009 D16 — T003 lands in four rounds and the 501 seam retires one command at a time (2026-08-22)

Measured at `1e7539be`: `UI_EXPOSED_COMMANDS` in `apps/cli/command_catalog.py` holds exactly TWO ids, `job.stop` and `decision.resolve` — not the three effects DECISION F009 D5's table names. The plan approval is not a third id: it arrives as `decision.resolve` carrying an `fp:`-prefixed `decision_id`, which is the same dispatch `_cmd_decision_resolve` already performs in the CLI, and that command's catalog args are `job_id`, `decision_id`, `--reason`, `--answer` and `--as-mission`. `resolve_flight_plan_approval` landed in `packages/orchestration/flight_plan.py` at `c204f0b5`, so all three effect functions D5 names now exist as importable package functions.

CHOSEN: the rest of T003 lands in FOUR rounds, and the 501 seam retires PER COMMAND rather than in one step. FIRST, `job.stop` dispatches to `safe_points.request_stop`; that same round writes D14's reserved `accepted` outcome, adds the `publish_nonce_result` call site with R-0637's bound applied AT PUBLICATION, moves R-0636's replay audit token off `not_implemented`, and ships the tests for that id's effect. `decision.resolve` keeps answering 501 and keeps auditing `not_implemented` through that round, which stays the honest token for a command this door has not yet dispatched. SECOND, `decision.resolve` dispatches — a task decision to `escalation.answer_task_decision` followed by `save_job`, an `fp:`-prefixed id to `resolve_flight_plan_approval` — and the seam is gone when that round ends. THIRD, the `command.accepted` SSE event. FOURTH, the queue-only import guard, the per-command side-effect assertions and the route-walking 405 test. Then the integration gate and closure.

WHY IT IS CUT THIS WAY, measured rather than estimated: DECISION F085 D6 caps a step block at 490 lines TOTAL and AGENTS.md DECISION F104 D1 caps a commit at 500 insertions. The dispatch, the publication, the two finding fixes, the accepted-event emission and the tests for all of it do not fit one block, and a block that does not fit is not delivered — it becomes a declared deviation on a round that did nothing wrong. Splitting by COMMAND rather than by LAYER keeps every round independently testable end to end: each retires the seam for one id and ships the tests that prove that id's effect, instead of landing a half-wired mechanism no test can reach.

WHY R-0636 AND R-0637 ARE BOTH PAID IN THE FIRST OF THE FOUR: each is a one-line change that depends on the publish call site, and that is the round which introduces it. Their fix clauses in `.agent/live_review.md` already say so; deferring either would leave a published record unbounded for a round and buy nothing.

ALTERNATIVES: (a) one round for all of T003 — rejected on the two caps above, which are measurements and not preferences. (b) split by LAYER, a dispatch module first and the wiring second — rejected because D5 rules that the handler imports the effect functions directly and that the import guard asserts exactly that set, so an intermediate dispatch module would change the very property the guard exists to assert. (c) retire the seam for both ids at once and defer only the tests — rejected outright: it would leave an accepting-but-unproven door on disk between two rounds, which is the one state this feature's Acceptance exists to make impossible.

REVERSE by collapsing the remaining rounds back into a single block, which is possible only if both caps change; the effect mapping itself comes from D5 and is unchanged by this decision.
<<<END DECISION16

Constraints:
1. Apply PLANF009R14, LEDGER14 and DECISION16 BYTE FOR BYTE out of the committed
   C0a blob — those are the slices, and this list is what "every slice" means
   anywhere below. Do not retype, rewrap, reflow, reindent or whitespace-adjust
   any of them. If a slice looks wrong to you, apply it as written and record the
   objection in the handback — an objection is recorded, never acted on.
2. The commit order is C0a, C0b, C1, C2, C3, C4 and nothing comes between them.
   C1 is the first substantive commit (checklist item 23).
3. WRITE NO CODE. Touch nothing under `packages/`, `apps/`, `tests/` or `docs/`.
   DECISION16 names four future rounds and this round performs NONE of them;
   R-0636 and R-0637 stay unpaid, as D16 itself rules.
4. C2 is an APPEND to `.agent/live_review.md` and C3 is an APPEND to
   `.agent/decisions.md`, one commit each. Nothing in either file is edited —
   both are append-only records. Both appends take the SAME shape: the previous
   blob, then one newline, then the slice — which reproduces the single blank line
   that already separates every entry in each file.
5. `.remedy-wt/` is gitignored scratch. Every multi-step gate goes into a script
   there; `git status --porcelain` prints 0 lines after each commit.
6. Push with `git push` after C4, the last commit of this round and of this
   session.

Done when:
- G1 `.agent/STOP` ABSENT, read at Step 0 and again before C4.
  `git rev-parse --abbrev-ref HEAD` prints `feature/f009-single-write-channel` at
  every reading. `git status --porcelain` prints 0 lines after each of C0a
  through C4. Report the round base SHA you read at Step 0.
- G2 Transport EQUAL: the scratch file as received, `.agent/authored/f009-r14.md`
  at C0a and `.agent/last_block.md` at C0b all carry the same sha256, byte count
  and line count, equal to the digest named in the task prompt. Write C0b from the
  COMMITTED C0a blob, never from the scratch file again.
- G3 Report, per slice, the newline-included sha256, byte count and line count;
  the COUNT of slices from your own ordered extraction out of the committed C0a
  blob; and the aggregate byte count, line count and slice count over them.
- G4 `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R14. Report its line count
  against the 50-line cap; `^## Goal$` and `^## Next Steps$` each match exactly
  1 line; the first `\bF\d{3}\b` match is `F009`.
- G5 The appends at C2 to `.agent/live_review.md` and at C3 to
  `.agent/decisions.md`, EACH proved TWICE over independent extractors in the
  general N-paragraph form: (a) the previous blob is a byte-exact PREFIX and the
  remainder EQUALS a newline plus the slice, reported with its sha256, bytes and
  lines; (b) with N COUNTED BY YOUR SCRIPT AND REPORTED, the LAST N blank-line
  units of the whole file equal the slice's N paragraphs IN ORDER. NEGATIVE
  CONTROL on the FIRST appended paragraph of each: flip ONE printable ASCII byte
  and confirm BOTH readings REJECT it while both ACCEPT the unflipped value;
  report all four outcomes per append. The base for C2 is the round base and for
  C3 the C2 commit's blob of `.agent/decisions.md`.
- G6 Line-anchored over `.agent/live_review.md` at the round base and at C2:
  `^- R-\d+ — ` 203 and 203 with all ids DISTINCT at each; `^Done: R-\d+ — ` 2 at
  both; `^Landed: ` 0 at both; `^> Next free id` 0 at both; `^Gate: R\d+ — ` 13
  and 14 over that many DISTINCT keys; `^Gate: R14 — ` 0 and 1. Report the max id
  at C2 and the count item 10's rule gives at C2 — line-anchored `^- R-\d+ — `
  minus line-anchored `^Done: R-\d+ — `. State that value in the handback WITH the
  rule and the commit beside it, per DECISION F009 D10, and report what your
  script printed rather than restating any number from here. Of the `Gate: ` lines
  at C2, report how many match `^Gate: R(\d+) — the R(\d+) entry\.` with the
  second numeral one less than the first, and quote to its first period any that
  does not.
- G7 Line-anchored over `.agent/decisions.md` at the round base and at C3:
  `^## DECISION F009 D\d+ — ` 15 and 16, every captured number DISTINCT at each,
  and `^## DECISION F009 D16 — ` 0 and 1. Report the max F009 decision number at
  C3 and the total `^## DECISION ` count at both.
- G8 In the PRIMARY checkout at C3, run SERIALLY, never two pytest processes at
  once, and report each exit code and its passed-plus-skipped total without
  predicting either: `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
  then `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`.
  Both must EXIT 0. This gate is ordered because R-0607's FIX clause requires it
  of any round whose change set holds an `.agent/` state file.
- G9 The range from the round base to C3: `git diff --name-only` lists EXACTLY
  the paths of the change set above other than `.agent/handoff.md`, the set
  difference empty in both directions, and holds NO path beginning `packages/`,
  `apps/`, `tests/` or `docs/` — constraint 3 as a measurement. Walk
  `git rev-list --reverse` and report, per commit, that it has ONE parent and its
  `git show --numstat` insertions, with `git diff --numstat` AGREEING on every
  cell and every cell equal to the `+/-` column of your handback's `## Commits`
  table (checklist item 28). Every commit stays under the 500-insertion cap of
  AGENTS.md DECISION F104 D1. `^<<<SLICE ` and `^<<<END ` read 0 lines in
  `.agent/plan.md`, `.agent/live_review.md` and `.agent/decisions.md` at C3.
  Classify this round's own reflog entries by the operation before the first `:`
  in the reflog subject and report `amend`, `rebase` and `cherry`, which must each
  be 0; assert no total over the whole reflog (R-0601). Report
  `git ls-files .remedy-wt` as a count.
- G10 The handback carries every mandated section of
  docs/agents/handback_template.md, an item-status table holding exactly one row
  for each of C0a, C0b, C1, C2, C3 and C4, the round base SHA, and one line per
  gate — the raw transcripts go in the round report, not in the handback (R-0582).
  Report its line count against the 100 that AGENTS.md allows a bundle of more
  than five commits, and if it exceeds that, carry the AGENTS.md DECISION D15
  stated-cause line naming the count and the mandated content that caused it. Its
  `## Next` section states, in this order: that THIS SESSION ENDED HERE and that
  the round wrote no production code, with the reason; that no `.agent/STOP` is
  present; that the next session's FIRST action is the `.agent/STOP` re-read
  (Phase 1 rule 1) and its SECOND the Open PR Gate (Phase 1 rule 2), which is
  EMPTY because this branch carries no pull request and F009 opens one at its own
  closure; that the R14 verdict itself is NOT yet on disk and is owed by the first
  reviewed round of the next session; the open-finding count from G6 WITH item
  10's rule and the commit named beside it; that the next free id is derived with
  `max` over the line-anchored entries and what that gives; that
  `.agent/candidates.md` is EMPTY; that the next round is the FIRST of the four
  DECISION F009 D16 rules — `job.stop` dispatch, the `accepted` outcome, the
  publish call site, R-0636 and R-0637 — and that D16 carries the ordering; and
  that R-0403, R-0607, R-0608, R-0609, R-0611, R-0613, R-0622, R-0630, R-0633 and
  R-0635 stay routed to a paydown branch.

Handback:    completion report + rewrite `.agent/handoff.md`. The state block
             repeats this Fortschritt line verbatim: 65 % (T001 gebaut · T002
             gebaut bis auf die Publikation · T003 begonnen: die Extraktion) —
             Schätzung
──────────────────────────────────────────────────────────────
