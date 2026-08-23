── STEP DECISION — F022 R4 ──
Goal:        Record the F022 R3 verdict, carry a recurrence of the OPEN finding
             R-0553 that R3's own context slice landed, and rule the budget tick
             envelope as DECISION F022 D1 on the ground the R3 inventory
             measured. This round BUILDS NOTHING and MINTS NOTHING: no file under
             `apps/`, `packages/` or `tests/` is touched and no new finding id is
             created.

Fortschritt: ~5 % (T001 offen · T002 offen · T003 offen; R3 hat den Boden
             vermessen, R4 entscheidet die Tick-Huelle — gebaut wird ab R5, und
             der Bauplan steht danach fest) — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the ledger
             append · C3 the DECISION · C4 context · C5 the handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f022-r4.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `.agent/decisions.md` (C3) · `.agent/context.md` (C4) ·
             `.agent/handoff.md` (C5).

Preface:     You are already on `feature/f022-live-cost-ticker`. THE ROUND BASE
             IS `33a0c6c1`, the R3 handback commit, and every base reading below
             is taken there. Create no branch. Run NO `gh pr create` and NO
             `gh pr merge`.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4, C5 and is not negotiable. C1
    precedes the ledger commit because the plan must be current first (§3
    checklist item 23). C5 is the LAST commit and carries the handback. EVERY
    gate below runs after C4 and BEFORE C5, so the handback can quote all of them
    honestly (§3 checklist item 31); C5's own readings are owed to the next
    round's ledger entry and are not gated here.
 3. THIS ROUND MINTS NO FINDING ID AND RESOLVES NOTHING. It writes no `Done:`
    line and no `Landed:` line. The maximum registered id is `R-0669` at the
    round base and must still be `R-0669` at C4. R-0553 stays OPEN: GATE3 records
    a recurrence of it, which is evidence added to an open finding and not a
    resolution.
 4. `.agent/live_review.md` AND `.agent/decisions.md` ARE BOTH APPEND-ONLY THIS
    ROUND. For each, the round-base blob must be a byte-exact PREFIX of the file
    after its commit, the new text is separated from the existing last paragraph
    by exactly one blank line, and the file ends in exactly one newline. Nothing
    already in either file is edited, reordered or deleted: §3 checklist item 20
    forbids rewriting landed text.
 5. The whole-file replacements are PLANF022R4 at C1 and CONTEXTF022R4 at C4,
    each written as the slice plus exactly one terminating newline. GATE3 is the
    append at C2 and DEC1 the append at C3.
 6. CONTEXTF022R4 REPLACES A SENTENCE THAT CONTRADICTED ITSELF. The R3 context
    slice claimed the file "names no round numbers" while naming `R2` in that
    same sentence — the R-0553 class, in the reviewer's own text. Its replacement
    states where the map lives and makes NO claim about its own contents, which
    is R-0553's counter-measure applied rather than restated.
 7. MEASURED DISAGREEMENTS ARE REPORTED, NEVER RECONCILED. Where a number below
    disagrees with what you measure, report BOTH and continue. Do not edit a
    slice and do not adjust your measurement to match mine.
 8. Block size, measured on these final bytes: TOTAL 306 lines against DECISION
    F085 D6's 490, and PROSE — TOTAL minus the slice CONTENT lines — 203 against
    DECISION F085 D5's 400. Marker lines count as prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again immediately before
     C5; the branch is `feature/f022-live-cost-ticker`; and
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1, C2, C3
     and C4.
 G2  TRANSPORT: sha256 over `.agent/authored/f022-r4.md` at C0a, over
     `.agent/last_block.md` at C0b, over the source file this block was read
     from, and over the digest the delegation names are all equal. That digest is
     stated OUTSIDE this file, because a digest of these bytes cannot exist
     inside them (§3 checklist item 9). Write C0b FROM the committed C0a blob,
     never from the source a second time, and report the digest with the byte and
     line counts.
 G3  SLICES: extract the slices from the COMMITTED C0a blob by their
     `<<<SLICE `/`<<<END ` marker LINES and report how many slices and how many
     CONTENT lines that extractor printed. Re-measure constraint 8's two numerals
     from that same blob and report both against their caps.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF022R4 plus one terminating
     newline, proved against the slice extracted from the committed C0a blob,
     with a NEGATIVE CONTROL against the BARE slice which must DIFFER. Report
     both readings, plus `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` at most
     50.
 G5  THE LEDGER APPEND AT C2, UNDER TWO INDEPENDENT READERS. Reader (a): the
     round-base blob of `.agent/live_review.md` is a byte-exact PREFIX of the
     file at C2 and the remainder is exactly one newline plus GATE3 plus one
     newline — report the remainder's byte count against GATE3's. Reader (b), an
     independent blank-line splitter: confirm the LAST unit equals GATE3 exactly,
     and report the unit count at the base and at C2. Then the NEGATIVE CONTROL,
     inside a disposable worktree under `.remedy-wt/f022r4-neg` and NEVER in the
     primary checkout: flip one printable byte at the START of the appended
     paragraph at unchanged length and confirm BOTH readers REJECT that mutant
     while ACCEPTING the true file. Remove the worktree and report
     `git worktree list` as a line count.
 G6  THE DECISION APPEND AT C3, under the same two readers as G5: the round-base
     blob of `.agent/decisions.md` is a byte-exact PREFIX of the file at C3, the
     remainder is exactly one newline plus DEC1 plus one newline, and an
     independent blank-line splitter reads the LAST unit as DEC1's own last
     paragraph. Report the remainder's byte count, the unit count at the base and
     at C3, and the count of lines beginning `## DECISION F022 D1 ` in the file
     at C3, which must be 1 — the prefix is quoted rather than the whole heading,
     so this gate cannot drift against DEC1's own wording.
 G7  THE LEDGER SETS, line-anchored, at the round base then at C2: `^- R-\d+ — `
     and how many are DISTINCT; `^Done: R-`; `^Landed: `; `^Gate: R` and how many
     are DISTINCT; `^Gate: R3 `; and the MAXIMUM registered id. Report each at
     BOTH points, plus the set of ids added and the set removed. I measured the
     base as 230 entries all distinct, 0, 0, 3 distinct keys, 0 and `R-0669`.
 G8  `.agent/context.md` at C4 is byte-equal to CONTEXTF022R4 plus one
     terminating newline, with a NEGATIVE CONTROL against the BARE slice which
     must DIFFER. Report both readings, plus `wc -l`, and — because these are the
     contract readers' own assertions — that `## Active Branch` occurs once and
     that a `feature/` slug, the substring `Steps`, the substring `pytest` and
     the roadmap id `F022` are each present.
 G9  THE SELF-CONTRADICTION IS GONE AND THE MAP IS STILL SINGLE. Read
     `.agent/context.md` with every run of whitespace collapsed to a single
     space, because the phrase is LINE-WRAPPED in the file and a raw substring
     count reads 0 at both points and would therefore prove nothing. Under that
     normalisation count `names no round numbers` at the round base and at C4: I
     measured 1 at the base, and it must read 0 at C4. Report the raw count too,
     which I measured as 0 at the base, so the pair shows the normalisation is
     what makes the gate bite. Then count the round-number tokens matching
     `\bR\d+\b` in that file at both points: I measured exactly one at the base,
     `R2`, and C4 is not required to reach 0 — the replacement is judged by the
     absence of the CLAIM, not by the absence of the tokens. Count the
     literal `→` in `.agent/context.md` and in `.agent/plan.md` at C4: both must
     read 0, and I measured both at 0 at the round base too, so report this pair
     as a REGRESSION guard rather than as a change.
 G10 RANGE, executed after C4: the range from the round base to C4 lists exactly
     the paths of this block's `Change:` list other than `.agent/handoff.md`,
     with the set difference EMPTY in both directions, and 0 paths beginning
     `packages/`, `apps/` or `tests/`. Report the two set differences and that
     count. Then: every commit single-parent; `git show --numstat` and
     `git diff --numstat` agreeing cell by cell with the handback's own
     `## Commits` table for C0a through C4 (§3 checklist item 28), C5's row being
     owed to the next round's ledger entry; every insertion count under the 500
     cap, EXCEPT that C3 is exempt as the verbatim rewrite of a single `.agent/**`
     state file only if it exceeds the cap — report C3's insertions either way;
     leading `<<<SLICE ` and `<<<END ` reading 0 LINES in `.agent/plan.md`,
     `.agent/live_review.md`, `.agent/decisions.md` and `.agent/context.md`;
     `git ls-files .remedy-wt` reading 0; and this round's reflog rows classified
     with `amend`, `rebase` and `cherry` each 0.
 G11 THE CONTRACT SUITES, run in the PRIMARY checkout and SERIALLY, never two
     pytest processes at once, after C4: `python3 -m pytest tests/ui_server/
     tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py
     tests/orchestration/test_integrity_gate.py -q -rf`. Report the exit code and
     the passed-plus-skipped total. I measured this at `33a0c6c1` as exit 0 at
     528 passed.
 G12 THE CATALOG PIN, run serially after G11, because DEC1 rules on it and a
     decision about a suite states that suite's colour at the commit it was
     ruled: `python3 -m pytest tests/ui_contracts/test_humanize_catalog.py
     -q -rf`. Report the exit code and the total. I measured it at `33a0c6c1` as
     exit 0 at 9 passed.
 G13 CANARY, run serially after G12: `python3 -m pytest
     tests/cli/test_golden_path.py -q -rf`. Report the exit code and the total. I
     measured it at `33a0c6c1` as exit 0 at 42 passed. NO docs gate is ordered
     this round because no path under `docs/` is in the change set.
 G14 DEC1'S CITATIONS RESOLVE, every one, at C4 — the check §3 checklist item 9
     orders and the one a DECISION most needs, since its whole value is that a
     later round can act on it without re-deriving it. For each of these, report
     the line you actually read there: `packages/orchestration/safe_points.py:616`
     is the `evaluate_budget` call and `:617` the `if evaluation.exhausted` test;
     `packages/orchestration/safe_points.py:606` is the operator-stop return;
     `apps/cli/commands/job.py:2374` binds `job.budget` to `_cmd_job_budget`;
     `packages/orchestration/budget_guard.py:216` is `class BudgetEvaluation`
     with `token_lower_bound` at `:223` and `cost_lower_bound` at `:225`;
     `packages/orchestration/ui_server.py:2748` is `_safe_event_summary` and
     `:3119` the `command.accepted` constant;
     `tests/ui_contracts/test_humanize_catalog.py:222` is the equality pin. Report
     any that does NOT resolve as a measured disagreement under constraint 7; do
     not repair the slice.
 G15 THE STANDING STALENESS GATE (R-0417): for EACH file this round touched,
     re-read it end to end at C4 and report every sentence that states a count, a
     list of modules, a round map or a completion, together with whether it still
     holds at C4. Report the sentences you found; do NOT repair anything outside
     your slices, and declare any residual instead.
 G16 NO PULL REQUEST IS CREATED AND NONE IS MERGED. Report the output of
     `gh pr list --state open --json number,headRefName` and state that this
     round ran neither `gh pr create` nor `gh pr merge`.
 G17 THE HANDBACK carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each commit of the
     `Bundle:` list, the round base SHA, ONE LINE PER GATE with the transcripts
     kept in the round report rather than in the file (R-0582), and this block's
     `Fortschritt:` line verbatim across all three of its lines. Its own `wc -l`
     is reported, and a DECISION D15 line declares any overage.

Handback:   completion report + rewrite `.agent/handoff.md`.

The slices follow. Each begins with a `<<<SLICE <name>` line and ends with a
`<<<END <name>` line; neither marker line is part of the slice, and no slice
includes a terminating newline unless a gate above says it does.

<<<SLICE PLANF022R4
# Plan — F022 Live cost ticker

Branch: feature/f022-live-cost-ticker, cut from `main` at `c34ef32b`, the merge
commit of pull request #211. `.agent/live_review.md` is the source of truth for
the open set, the round map and the finding-id ceiling.

## Goal
Money is visible while it burns, honestly: the MetricsBar's COST metric renders
from budget tick events {spent, limit, basis} — bar fill against the limit, a
'~' prefix plus tooltip whenever the basis is estimated, warn colour at ≥85% —
and the final figure reconciles with the ledger at terminal. DONE when the
ticker tracks a fixture stream exactly, basis changes flip the prefix and
tooltip live, the warn threshold triggers per tokens, limitless jobs render the
spent-only variant with no fake denominator, and the terminal reconciliation
displays the ledger figure with any delta labelled.

## Current Step
R4 records the R3 verdict, carries a recurrence of the open finding R-0553 that
R3's own context slice landed, and rules the budget tick envelope as DECISION
F022 D1 — the emission site, the payload's field set, the basis vocabulary and
the no-client-arithmetic contract — on the ground the R3 inventory measured. It
mints no id and builds nothing.

## Next Steps
1. R5 T001 the tick emission in `should_stop`, with its backend tests, the
   humanize-catalog key and the catalog pin gated in the same commit.
2. R6 T002 the COST metric on fixture streams; R7 T003 the terminal
   reconciliation and the delta labelling.
3. R8 the integration gate, then closure.

## Risks
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks rather than F022
  defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- T002 widens a CLOSED union and a value type that has nowhere to put a limit or
  a basis, both measured in the R3 inventory. That is a type-level change, not an
  additive one, and R6 is sized for it.
<<<END PLANF022R4

<<<SLICE CONTEXTF022R4
# Context — F022 Live cost ticker

## Active Branch
feature/f022-live-cost-ticker, cut from `main` at `c34ef32b`, the merge commit
of pull request #211 which closed F021.

## Scope
F022 only: the budget tick emission, the MetricsBar COST metric and the terminal
reconciliation. The roadmap feature file is
`docs/roadmap/features/T5_F022.md` and its Task slicing fixes the order.

## Do not touch
Budget enforcement, the pricing and basis rules, and MetricsBar's other metrics.
The feature file's own Do-not-touch section governs and is not narrowed here.

## Assumptions
- The UI never computes money. The backend is the single arithmetic home and the
  client's only arithmetic is the fill ratio.
- No currency field is emitted unless a price basis exists, so no invented
  dollars reach the display.
- The tick is additive on the SSE transport, which enumerates no event kinds, and
  is NOT additive on the humanize catalog, which is pinned equal to the Python
  vocabulary. Both halves were measured in `.agent/f022_inventory.md`.

## Constraints
- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- A round that emits a new Python event kind adds the matching key in
  `apps/ui/src/api/humanizeCatalog.ts` in the SAME commit and gates
  `tests/ui_contracts/test_humanize_catalog.py`; the two sets are pinned EQUAL
  and neither may move alone (DECISION F022 D1).
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout, which satisfies
  `git status --porcelain` empty at every verdict.
- This is a UI feature, so `docs/ui/design_reference/` is binding and any visual
  deviation is documented with a technical reason.

## Steps
The round map lives in the `## Steps` section of `.agent/live_review.md`, per
R-0447's remedy, and this file deliberately does not restate it: a second copy
of the map is what fell out of step and cost this feature a finding.
<<<END CONTEXTF022R4

<<<SLICE GATE3
Gate: R3 — the F022 R3 entry. R3 PASSED ON EVERY ONE OF ITS FIFTEEN GATES, AND THE REVIEWER RE-RAN ALL OF THEM PLUS AN INDEPENDENT AUDIT OF THE INVENTORY'S OWN CLAIMS. TRANSPORT HELD IN ITS STRONGEST FORM, not the digest fallback: `.agent/authored/f022-r3.md` at `a5390e74`, `.agent/last_block.md` at `256c290e` and the bytes the reviewer EMITTED, still on disk at `.remedy-wt/f022-r3.md`, are all sha256 `b823ea0234133b702a4e627f7f601bf4c268dc7e5c76fb02f154268d948dd471` over 24075 bytes and 294 lines, so §4.9's primary comparison against the reviewer's own original was available and was used. THE EXTRACTION out of the committed C0a blob printed 5 slices over 103 CONTENT lines, and constraint 9's numerals re-measure as 294 TOTAL and 191 PROSE, under DECISION F085 D6's 490 and D5's 400. THE WHOLE-FILE REPLACEMENTS ARE BYTE-EQUAL DISK TO DISK, each against the slice extracted from the committed blob and each with a negative control against the bare slice that DIFFERS: `.agent/plan.md` at `eef9fd34` at 39 lines with `^## Goal$` and `^## Next Steps$` once each, and `.agent/context.md` at `aead9822` at 42 lines carrying `## Active Branch` once plus the `feature/` slug, `Steps`, `pytest` and `F022` that the state-contract readers assert. THE LEDGER COMMIT IS PROVED BY RECONSTRUCTION, WHICH IS STRICTLY STRONGER THAN A PREFIX READING AND WAS CHOSEN BECAUSE THE ROUND BOTH REWROTE AND APPENDED: the round-base blob of `.agent/live_review.md` with the STEPSF022 FROM string replaced exactly once by the TO string, then one newline plus GATE2 plus one newline, is BYTE-EQUAL to the file at `2b5ca446` — so nothing else in that file moved, which no prefix test could have shown. The FROM counted 1 at the base and 0 at C2 and the TO 0 then 1; an independent blank-line splitter read 252 units at the round base and 253 at C2 with the last equal to GATE2; and a one-byte flip at offset 477451, `G` to `H` at unchanged length, is REJECTED by both readers while both ACCEPT the true file. THE SETS ARE UNCHANGED WHERE THE ROUND PROMISED: 230 entries all DISTINCT at both points, `^Done: R-` 0, `^Landed: ` 0, maximum id `R-0669` at both, the ids added and the ids removed BOTH the empty set, and `^Gate: R` moving 2 to 3 with the distinct keys gaining `Gate: R2` beside `Gate: R1` and `Gate: R41`. THE MAP IS SINGLE AGAIN: the arrow counted 3 in `.agent/context.md` and 0 in `.agent/plan.md` at the base, and 0 in both at C3, while `.agent/live_review.md` moved 24 to 29 — so the duplicate map was deleted rather than re-synchronised, which is R-0447's remedy applied instead of restated. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout: the four state readers exit 0 at 528 passed, and the canary `tests/cli/test_golden_path.py` exit 0 at 42 passed. STRUCTURE HELD: seven commits over `66f87edc`..`33a0c6c1`, every one single-parent, insertions 294, 224, 12, 12, 4, 246 and 83, each under the 500 cap; the range path set EQUAL to the block's declared set with the difference empty in both directions and 0 paths beginning `packages/`, `apps/` or `tests/`; `git show --numstat` agreeing cell by cell with the handback's `## Commits` table; `^<<<SLICE ` and `^<<<END ` reading 0 in all four slice targets; `git ls-files .remedy-wt` 0; one worktree; `git status --porcelain` empty; and 0 amend, 0 rebase and 0 cherry in the round's reflog rows. THE INVENTORY WAS AUDITED RATHER THAN ACCEPTED, because a cited number is still a claim: the reviewer re-ran the AST predicate itself and reproduces 4 production call sites of `evaluate_budget` at exactly the cited lines with 51 repo-wide and 47 in `tests/**`; `class BudgetEvaluation` at `packages/orchestration/budget_guard.py:216` with all eight fields including `token_lower_bound` and `cost_lower_bound`; `def evaluate_budget` at `:254`, `collect_ledger_cost_for_job` at `:645` and `_LIMIT_ORDER` at `:245`; `apps/ui/src/components/metrics/TopMetricsBar.tsx` at 100 lines with `cost`, `spent` and `usd` all 0 case-insensitively; `RemedyMetricKey` a CLOSED union of exactly seven strings and `RemedyMetric.value` typed as a number or an em dash; the fill branch gated on the `progress` key; and `apps/ui/src/api/humanizeCatalog.ts` holding 83 keys, all distinct, with kinds beginning `budget` the EMPTY set, `context_budget_optimized` the only one containing the substring and `command.accepted` the dotted precedent. Every audited claim reproduced; not one number in that file was wrong. THE ROUND'S DECLARED DISAGREEMENT IS THE MOST VALUABLE THING IN IT, AND IT CORRECTS THE REVIEWER. G9(b) of the R3 block named `RemedyTimelineEventKind` and its three literals as the event vocabulary. That reproduces exactly and is the WRONG SET for this feature: the worker measured a second and larger one, the 83-key pair of `apps/ui/src/api/humanizeCatalog.ts` and the static Python stream vocabulary, pinned EQUAL by `tests/ui_contracts/test_humanize_catalog.py`, and that is the vocabulary the live SSE feed carries. The three-literal timeline union is a separate seam built by `_build_timeline_events`. No number the block stated was wrong; its SCOPE was, and constraint 8 is the reason that cost nothing — the block ordered the property and named its own reading as a reference to be reported against, so the worker measured more and reported rather than reconciling. THE ROUND ALSO FOUND A GATE THE FEATURE WILL NEED AND NO F022 ROUND HAS RUN: `tests/ui_contracts/test_humanize_catalog.py` pins the catalog equal to the Python emitters, so the first round emitting a `budget`-named event must add the catalog key in the same commit and gate that suite. The reviewer ran it at `33a0c6c1` and it is exit 0 at 9 passed, so the pin is green now and the obligation is forward-looking. DECISION F022 D1, committed this round, binds it. RECURRENCE OF R-0553, dated 2026-08-23, recorded here rather than under a new id because §3 checklist item 30 requires the open set searched for the DEFECT before an id is minted and R-0553 already holds this class — an authored slice asserting an unmeasured universal that is false of its own members, written by the reviewer inside the very slice that was correcting a related defect. The R3 slice CONTEXTF022R3 states that `.agent/context.md` "names no round numbers, so it cannot fall out of step with the map", and that sentence names `R2` seven words later. Measured at `aead9822`, the file's round-number tokens are exactly one, `R2`, and it sits inside the clause denying it. THE WORKER HANDLED IT EXACTLY AS THE RULES REQUIRE, which is worth recording: constraint 1 forbade editing a slice, so it applied the bytes verbatim, declared the contradiction as a G15 residual before the reviewer read the diff, repaired nothing outside its slices and ruled on nothing. That is the second consecutive round in which a worker declared a reviewer defect rather than silently fixing it. THE DEFECT IS LOW AND IT IS THE REVIEWER'S: no gate was misreported and the ordered repair did land in full — the duplicate map is gone and the arrow count is 0 — so only the justifying clause is false, not the change it justifies. R4's CONTEXTF022R4 replaces the sentence with one that states where the map lives and makes NO claim about its own contents, which is R-0553's own counter-measure rather than a rewrite of landed record text. R-0553 STAYS OPEN. THE VERDICT IS PASS: every numeral R3 states reproduced under the reviewer's own measurement, the shipped work is a plan, a map repair, a context deletion and a 246-line inventory whose every audited claim holds, and the single defect the round leaves on disk is one clause of a reviewer-authored slice, declared by the worker before review.
<<<END GATE3

<<<SLICE DEC1
## DECISION F022 D1 (2026-08-23) — the budget tick envelope: where it emits, what it carries, and why the basis is not a new vocabulary

CONTEXT, measured by the reviewer at `5f53471f` and recorded in `.agent/f022_inventory.md` at that commit. `docs/roadmap/features/T5_F022.md` says the budget guard "already evaluates spent-vs-limits at safe points" and that the tick emits "at those same evaluations", which reads as though every evaluation site is a candidate. The inventory measures four production call sites of `evaluate_budget`. Three of them — `apps/cli/commands/job.py:2127`, `:2172` and `:2221` — sit inside `_cmd_job_budget`, the handler the dispatch table binds to `job.budget` at `apps/cli/commands/job.py:2374`, so they run when a human asks for a budget report and never during a job. The fourth, `packages/orchestration/safe_points.py:616`, sits inside `should_stop`, whose own docstring at lines 601-602 calls it "the SINGLE entry point for safe-point evaluation", and which the run path reaches from `packages/orchestration/long_run_executor.py:1389` and `:1403`, `packages/orchestration/pingpong_job.py:1970` and `apps/cli/commands/do_cmd.py:793`.

CHOSEN (1), THE EMISSION SITE, AND IT IS ABOVE THE EXHAUSTION TEST. The tick emits in `should_stop`, immediately after the `evaluate_budget` call at `packages/orchestration/safe_points.py:616` and BEFORE the `if evaluation.exhausted` test at `:617`. Emitting inside that branch would fire the ticker only at exhaustion, which is the one moment a live cost ticker is no longer needed. The three `_cmd_job_budget` sites emit nothing: a reporting command that ticked would write ledger events for a read. Note a consequence rather than a bug: `should_stop` returns at `:606` on an operator stop, before the budget block, so a safe point stopped by the operator evaluates no budget and emits no tick. No evaluation, no figure — stated here so a later round does not read the gap as a defect.

CHOSEN (2), THE PAYLOAD CARRIES ABSOLUTE VALUES ONLY, AND CURRENCY ONLY WHEN PRICED. Fields: `spent_tokens` always; `spent_usd` only when a cost figure exists; `limit_tokens` and `limit_usd` only when that limit is configured; `basis`; `unmeasured_calls`. An absent limit is an ABSENT KEY, never null and never zero, so the acceptance criterion that the limitless variant never fabricates a denominator is enforced by the envelope's shape rather than by the client's care. `_LIMIT_ORDER` at `packages/orchestration/budget_guard.py:245` fixes five limit kinds, of which cost is one, so a job may be budget-limited with no money limit at all and the spent-only variant is the normal case rather than the edge.

CHOSEN (3), THE BASIS IS THE TWO BOOLEANS THAT ALREADY EXIST, NOT A THIRD SPELLING. `BudgetEvaluation` at `packages/orchestration/budget_guard.py:216` already carries `token_lower_bound` at `:223` and `cost_lower_bound` at `:225`, the second commented "True when the cost figure is a floor, not a total: some call was unpriced". `basis` is therefore an object with one key per figure, each reading `actual` or `lower_bound`, and the cost key additionally able to read `absent`, mapped mechanically from those two fields plus the presence of a cost figure. The feature file's basis strings — "estimated — class defaults", "actuals with N unmeasured calls" — are DISPLAY text, composed in the client from this object and `unmeasured_calls`, and are not transported.

CHOSEN (4), NO CLIENT ARITHMETIC BEYOND THE FILL RATIO. The client computes the fill of spent against the configured limit and nothing else: no currency conversion, no price constant, no summation, no unit scaling. The tick carries every figure the display needs as an absolute value. This is the feature file's verbatim order material and it is testable as an ABSENCE, which is how T002 should gate it: no price-like constant under `apps/ui/src`.

CONSEQUENCE THIS DECISION BINDS, found by the R3 inventory. A `budget`-named tick is genuinely additive on the transport — `_safe_event_summary` at `packages/orchestration/ui_server.py:2748` passes the ledger event name through against no whitelist, and `sse_event_frame` emits no SSE event field — but it is NOT additive on the humanize catalog, where `apps/ui/src/api/humanizeCatalog.ts` is pinned EQUAL to the Python static vocabulary by `tests/ui_contracts/test_humanize_catalog.py:222`. The round that emits the first such event therefore adds the catalog key in the SAME commit and gates that suite, which no F022 round had gated before this one. The dotted name needs no new rule: `command.accepted`, at `packages/orchestration/ui_server.py:3119`, is already in that vocabulary.

ALTERNATIVES CONSIDERED. Emit at all four evaluation sites: rejected, three of them are a CLI report and would put ledger writes on a read path. Emit inside the exhaustion branch, where the evaluation is already consumed: rejected for the reason in (1) — it is the smallest diff and it produces a ticker that ticks once, at the end. A single flat basis enum such as actuals or estimated or mixed: rejected, it loses WHICH of the two figures is a floor, and the display must mark the spend and the cost independently. Carry the display sentence on the wire: rejected, it moves copy into the backend and makes the honesty text untranslatable and untestable at the component level. Send a null cost limit for a limitless job: rejected, a null denominator is the fake denominator the acceptance criteria forbid, and an absent key cannot be divided by accident.

REVERSE IT by deleting the emission from `should_stop` and the humanize-catalog key together; they are pinned equal, so neither can drift alone. Rulings (2), (3) and (4) reverse independently of the site choice in (1), and none of them binds MetricsBar's other metrics, which this feature does not touch.
<<<END DEC1
