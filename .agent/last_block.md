── STEP T003b-b/3 — F022 Live cost ticker · Runde 14 ──────────────────────────

Fortschritt: ~88 % (T001 fertig · T002 fertig · T003a fertig · T003b-a fertig —
             diese Runde baut die Client-Haelfte: die Schluss-Abrechnung gegen
             die Ledger-Zahl mit ihrem Delta-Label) — Schaetzung

Goal:        Render the terminal reconciliation in the COST tile: at terminal the
             ledger's final figure replaces the live one, and a difference
             between what the client RECEIVED and what the ledger HOLDS is
             labelled as the transport statement DECISION F022 D7 rules it to be.
             This closes T003b and with it the last unbuilt half of F022.

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the plan ·
             C2 the R13 verdict · C3 DECISION F022 D8 · C4 the reconciliation
             module and its tests · C5 the transport, type and mapping · C6 the
             render and its contract · C7 the handback.

Change:      Exactly these paths, nothing else:
               .agent/authored/f022-r14.md                        (C0a)
               .agent/last_block.md                               (C0b)
               .agent/plan.md                                     (C1)
               .agent/live_review.md                              (C2)
               .agent/decisions.md                                (C3)
               apps/ui/src/api/costReconciliation.ts              (C4)
               apps/ui/src/api/costReconciliation.test.ts         (C4)
               apps/ui/src/api/types.ts                           (C5, C6)
               apps/ui/src/api/remedyApi.ts                       (C5)
               apps/ui/src/api/remedyApi.test.ts                  (C5)
               apps/ui/src/components/shell/RemedyShell.tsx       (C6)
               apps/ui/src/components/metrics/TopMetricsBar.tsx   (C6)
               tests/ui_contracts/test_cost_metric_render.py      (C6)
               .agent/handoff.md                                  (C7)

─── Slice convention ──────────────────────────────────────────────────────────
Each authored text below begins at its `<<<SLICE <name>` line and ends at its
`<<<END <name>` line; neither marker line is part of the slice, and no slice
contains a marker line. Extract them PROGRAMMATICALLY by marker line out of the
committed C0a blob — never retype, never rewrap, never reflow. The whole-text
slices are PLANF022R14, LEDGER14 and DEC14. This block carries NO FROM/TO pair
at all, so it states no containment reading: there is nothing to classify.
Every slice is quoted WITHOUT its trailing newline. PLANF022R14 replaces its
file whole; LEDGER14 and DEC14 each land as one newline plus the slice plus one
newline, appended to the end of their files.

THE PRODUCTION CODE OF C4, C5 AND C6 IS NOT A SLICE. It is SPECIFIED below and
you author it, under the self-review loop AGENTS.md mandates. Only the three
`.agent/` texts above are byte-for-byte transport.

Constraints:
 1. NEVER edit a slice. Apply it byte for byte. If a slice contradicts a fact
    you measure, apply it anyway and DECLARE the contradiction in the handback
    under Deviations. Repair nothing outside your Change set; rule on nothing.
 2. C1 is the FIRST substantive commit (§3 checklist item 23): this round
    touches the finding ledger, so the plan advances before anything else but
    the two block-save commits.
 3. COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4, C5, C6, C7 and no other. C4
    precedes C5 and C5 precedes C6, because the module must exist before the
    type names its output and the type must exist before the shell composes it.
 4. THE SINGLE ARITHMETIC HOME IS NOT MOVED. `apps/ui/src/api/costMetric.ts`
    stays the only shipped source whose CODE names `spent_usd`, `spent_tokens`,
    `limit_usd` or `limit_tokens`. `costReconciliation.ts` therefore takes the
    figures as an opaque payload and hands them to `costMetricOf`; it reads
    only the already-decided view fields. A COMMENT may name a field — the
    guard strips comments before scanning — but no line of code may. This is
    not advice: `tests/ui_contracts/test_cost_metric_render.py` asserts the
    home list equals exactly one path, `apps/ui/src/api/costMetric.ts`,
    measured green at the round base, and a new name there turns it red.
 5. NO SECOND MONEY ARITHMETIC. `costReconciliation.ts` performs no division,
    no subtraction and no multiplication on any figure. It compares two strings
    that `costMetricOf` already produced. The delta is NAMED, never COMPUTED —
    DECISION F022 D7's closing clause and DECISION F022 D8 clause 3.
 6. THE SHELL'S EXISTING SEAM SURVIVES VERBATIM. The substring
    `metricsWithCostTicker(dashboard.metrics, stream.budget)` must still occur
    in `RemedyShell.tsx` after C6, because a contract test pins it; wrap that
    call, never replace it. `metrics={dashboard.metrics}` must still be absent.
 7. NO NEW `docs/` PATH AND NO ROADMAP EDIT. DECISION F022 D7 already amended
    the feature file's Terminal-reconciliation bullet; this round builds against
    it and changes no specification.
 8. Destructive verification runs ONLY inside a disposable worktree under
    `.remedy-wt/`. The primary checkout satisfies `git status --porcelain`
    empty at every commit and at the handback.
 9. Every numeral this block states about the ROUND BASE `5d3e6045` was produced
    by a reviewer script or tool run at that commit and is a REFERENCE to report
    against, not a target to reproduce. Where your measurement differs, report
    BOTH and reconcile NOTHING.
10. Size, measured by the reviewer on the final bytes of this block and stated
    once here: this block is 393 lines TOTAL with 116 CONTENT
    lines inside its slices, so PROSE is 277 — under DECISION F085 D6's
    490 and D5's 400.

─── What C4 builds ────────────────────────────────────────────────────────────

`apps/ui/src/api/costReconciliation.ts`, a new module that is the single home
for every decision DECISION F022 D8 rules, and for nothing else. It exports one
pure function that takes the bar's metrics, the LEDGER figures, the RECEIVED
figures and whether the job is still running, and returns the metrics array with
the cost tile reconciled — by REFERENCE and unchanged whenever there is nothing
to say, exactly as `costTicker.ts` already does for the live tick.

Its behaviour is DECISION F022 D8 and nothing beyond it:
  · running, or no ledger figure → the metrics array comes back BY REFERENCE.
  · terminal with a ledger figure → the cost tile's view becomes the LEDGER's,
    produced by `costMetricOf`, so the tile shows the ledger's own display,
    unit, marker, fill, level and tooltip.
  · the note is attached only when a received figure exists AND its display
    differs from the ledger's, and it reads exactly
    `final (ledger): X — live estimate was Y` with X the ledger display and Y
    the received one.
  · no received figure → the ledger view with NO note.
The module's header carries the one-line WHY above its export and the
"Remedy deliberately does not" sentence AGENTS.md's discoverability rules ask
for, naming what it refuses to do: compute a difference.

`apps/ui/src/api/costReconciliation.test.ts` covers, each as its own case: the
by-reference return while running; the by-reference return with a null ledger
figure; the ledger view replacing the live one at terminal; the note's exact
text when the displays differ; the ABSENCE of the note when they are equal; the
absence of the note when no figure was received; a metrics array carrying no
cost tile coming back by reference; and the source guard — the module's code,
comments stripped, names no figure field. Give that guard a POSITIVE CONTROL,
as `costMetric.test.ts` does for its own scan, so a guard that scans nothing
cannot pass.

─── What C5 builds ────────────────────────────────────────────────────────────

The ledger figure reaches the client. In `apps/ui/src/api/types.ts` the
`RemedyDashboard` interface gains `budgetFinal: BudgetTickFigures | null`,
imported as a type from `./costMetric` beside the existing `CostMetricView`
import. In `apps/ui/src/api/remedyApi.ts` the mapper reads the wire's
`budget_final` into it, defaulting to `null` — the server returns `None` for a
job that emitted no tick, and an absent figure stays absent rather than becoming
an empty object. `remedyApi.test.ts` gains cases for the mapped figure, for the
null, and for a payload with no `budget_final` key at all.

─── What C6 builds ────────────────────────────────────────────────────────────

The render. `RemedyMetric` in `types.ts` gains an optional already-composed
`costFinalNote?: string` — the component composes no sentence, the same rule
that put `cost` there as a decided view. `RemedyShell.tsx` wraps its existing
call so the reconciliation runs over the ticker's output, passing
`dashboard.budgetFinal`, `stream.budget` and `dashboard.live.running`.
`TopMetricsBar.tsx` renders the note under the value when it is present, reusing
an existing caption class from `TopMetricsBar.module.css` rather than adding a
rule, and adding no arithmetic of any kind to that component.
`tests/ui_contracts/test_cost_metric_render.py` gains a class pinning this new
seam the way `TestTheLiveTickReachesTheBar` pins the live one: the shell
composes both functions, the import is real, the bar renders the note off its
own field, and the bar still divides nothing.

─── Why this round exists ─────────────────────────────────────────────────────

R12 gave the dashboard a `budget_final` section and MEASURED that no client
reads it. A ledger figure that reaches a payload and no screen is the shape
`tests/ui_contracts/test_cost_metric_render.py` already complains about in its
own docstring for the live tick — "the tile a user saw was not merely empty — it
was absent". This round closes that path, and with it the last DONE clause of
the feature's own Goal that no code answers.

─── Done when ─────────────────────────────────────────────────────────────────

Run every gate below yourself, record its REAL exit code, and put ONE LINE per
gate in the handback with the transcripts kept out of it (R-0582). G1 through
G13 run after C6 and BEFORE C7, so the handback can quote all of them (§3
checklist item 31). The round base is `5d3e6045` throughout.

 G1  `.agent/STOP` absent, read from disk before C0a and again before C7.
     Branch `feature/f022-live-cost-ticker`. `git status --porcelain` 0 lines
     after every one of C0a, C0b, C1, C2, C3, C4, C5 and C6.
 G2  TRANSPORT. sha256 over the block file at `.remedy-wt/f022-r14.md`, over the
     committed C0a blob, over the committed C0b blob and over
     `.agent/last_block.md` on disk: report all four digests, byte counts and
     line counts, and require them EQUAL. The digest the delegation names is the
     fifth reading and must agree.
 G3  EXTRACTION. Run an extractor over the COMMITTED C0a blob that finds the
     slices by their marker LINES and report how many slices and how many
     CONTENT lines it printed, plus the block's TOTAL and PROSE line counts.
     Report those against constraint 10's numerals; reconcile nothing.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF022R14 plus exactly one
     newline. NEGATIVE CONTROL: the same comparison against the BARE slice must
     be FALSE, and report both byte counts. `^## Goal$` once, `^## Next Steps$`
     once, `wc -l` at most 50.
 G5  THE TWO APPENDS, C2 into `.agent/live_review.md` and C3 into
     `.agent/decisions.md`, each proved twice. Reader (a): the pre-commit blob
     is a byte-exact PREFIX of the committed file and the remainder is exactly
     one newline plus the slice plus one newline — report the remainder's byte
     count and the slice's, per file. Reader (b), INDEPENDENT: split both files
     on blank lines, let N be the number of paragraphs YOUR script counts in the
     slice, and require the LAST N units of the committed file to equal the
     slice's N paragraphs IN ORDER. Report N per file; do not take it from this
     block. NEGATIVE CONTROL, in a disposable worktree, applied to the FIRST
     appended paragraph of EACH file: flip ONE byte at an offset you name and
     confirm BOTH readers reject the mutant while both accept the true file. THE
     OFFSET IS A BYTE OFFSET — these files carry multi-byte em dashes, so a
     CHARACTER offset lands early, outside the appended region, where reader (b)
     accepts the mutant and the control proves nothing. Report the ~20 bytes
     surrounding each flip. Remove the worktree; `git worktree list` back to one
     line.
 G6  LEDGER INTEGRITY, base versus C2. Report for both points: the count of
     lines matching `^- R-\d+ — `, whether they are all DISTINCT, the MAXIMUM
     id, the count of `^Done: R-` with its distinct ids, of `^Landed: `, of
     `^Recurrence: R-`, and of `^Gate: R` with its distinct keys. Report the ids
     ADDED and REMOVED as sets. At base the reviewer measured 234 records, all
     distinct, maximum `R-0673`, 2 `Done:` lines over `R-0653` and `R-0670`, 0
     `Landed:`, 8 `Recurrence:` lines and 13 `Gate:` lines over 13 distinct
     keys. This round MINTS NO NEW ID: it is expected to add no record, to leave
     `^Recurrence: R-` at 8, and to add exactly the key `R13`. Report what you
     measure.
 G7  THE SINGLE ARITHMETIC HOME, measured and not asserted. Over every shipped
     `.ts`/`.tsx` under `apps/ui/src` that is not a `.test.ts`/`.test.tsx`, with
     comments stripped, report the LIST of files whose code names any of
     `spent_usd`, `spent_tokens`, `limit_usd`, `limit_tokens`. Require that list
     to be exactly one path, `apps/ui/src/api/costMetric.ts`. Report how many
     files the scan actually read, so a scan that read nothing is visible.
 G8  THE CLIENT SUITES, in the PRIMARY checkout at C6, exit 0 for each:
     `npx vitest run` and `npx tsc --noEmit`, both with `apps/ui` as the working
     directory, and `python3 -m pytest tests/ui_contracts/ -q` from the
     repository root. The reviewer measured, at the round base, vitest at 19
     files and 268 tests, `tsc` at exit 0 with no output, and
     `tests/ui_contracts/` at 518 passed and 4 skipped. Report your own figures
     beside those. NOT A GATE and not run: `npm run lint` in `apps/ui`, which is
     RED at base for reasons this round does not touch (R-0622, R-0364).
 G9  MUTATION, in a disposable worktree at C6 and NEVER in the primary checkout,
     with the positive control reported first. Make the note render
     unconditionally — delete the guard that withholds it when the two displays
     are EQUAL — and report which tests fail and how many. Then restore, and
     make the reconciliation run while the job is still RUNNING, and report the
     same. If either mutation leaves every test green, say so plainly: that is a
     true report about an unguarded property and it is worth more than a colour.
     Remove the worktree; `git worktree list` back to one line.
 G10 THE FOUR STATE READERS plus THE CANARY, serially in the PRIMARY checkout at
     C6, exit 0: `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py`,
     `tests/orchestration/test_integrity_gate.py`, then
     `tests/cli/test_golden_path.py`. The reviewer measured 470, 52, 21 and 16
     for 559 across the four, and 42 for the canary, at the round base. Never
     run two pytest processes at once. This round rewrites `.agent/` state and
     those four are its readers.
 G11 STRUCTURE, reported for the commits BEFORE C7 and for the range as a whole
     (C7's own numbers belong to the next round's ledger entry, not here):
     every commit single-parent; each commit's INSERTION count, each under the
     500 cap; the range path set against the Change set above with the
     difference reported in BOTH directions; `git show --numstat` agreeing cell
     by cell with the handback's `## Commits` table; the LINE-ANCHORED patterns
     `^<<<SLICE ` and `^<<<END ` counting 0 in `.agent/plan.md`,
     `.agent/live_review.md` and `.agent/decisions.md`; `git ls-files .remedy-wt`
     0; one worktree; and the round's reflog rows with amend, rebase and cherry
     counts, each 0.
 G12 `gh pr list --state open --json number,headRefName`. Report it verbatim.
     Create no PR and merge nothing: the integration gate has not run, and the
     closure protocol creates the PR at closure.
 G13 STALENESS. Every sentence C1, C2 and C3 land that states a fact about a
     file is re-measured at C6, and any that has gone stale is reported as a
     residual rather than repaired. Report explicitly that you checked, and name
     any residual. Slices are NEVER edited to fix one.

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             every mandated section in order, one changed-files table per
             commit, an item-status row per Bundle item, the round base SHA,
             ONE line per gate, and the `Fortschritt:` block above carried
             VERBATIM across all three of its lines. Every count you report
             names the exact string or pattern counted and the file it was
             counted in (R-0442). The cap is 60 lines for this commit count;
             declare a DECISION D15 stated cause with your own measured numeral
             in the declaring line if the mandated content genuinely does not
             fit. `## Next` names R15, the integration gate, per
             docs/agents/integration_gate.md.
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF022R14
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
R14 builds T003b's client half: a reconciliation module ruled by DECISION F022
D8, the `budgetFinal` transport into the dashboard type, and the render of the
ledger figure with its delta label. It also records the R13 verdict. This is the
last unbuilt half of the feature.

## Next Steps
1. R15 the integration gate, per docs/agents/integration_gate.md.
2. R16 closure, per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- The delta R14 renders is a TRANSPORT statement, not arithmetic: both sides are
  the same quantity from the same producer, so a difference means frames were
  missed. A round that reads it as drift would reintroduce the fabricated
  honesty moment DECISION F022 D7 exists to prevent.
- A contract test in `tests/ui_contracts/test_cost_metric_render.py` pins, as
  measured at `5d3e6045`, `costMetric.ts` as the ONLY shipped client source
  whose code names a figure field. The new module must stay outside that list,
  which is why it takes the payload opaquely and delegates every reading.
- Open F022 findings: R-0672 and R-0625 want their next-DECISION and
  next-numeral clauses honoured; R-0431, R-0413 and R-0533 are reviewer-block
  defects already recorded and already paid for.
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks, not F022 defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- R-0665 is open and this feature needs its route: every UI feature is told to
  record visual deviations in an `assumption_log` that does not exist. F022
  records them as DECISIONs in `.agent/decisions.md`, a route rather than a fix.
<<<END PLANF022R14

<<<SLICE LEDGER14
Gate: R13 — the F022 R13 entry. R13 PASSED ON EVERY ONE OF ITS ELEVEN GATES, AND THE REVIEWER RE-EXECUTED EVERY MEASURABLE ONE OF THEM ITSELF OFF DISK IN THE PRIMARY CHECKOUT. R13 built nothing: it recorded the R12 verdict, registered the R-0533 recurrence, repaired the round map and ended its session at its declared round budget, which DECISION F085 D9 rules is how a PASS reaches disk at all. TRANSPORT HELD IN ITS STRONGEST FORM: the committed C0a blob, the committed C0b blob and `.agent/last_block.md` on disk are ALL sha256 `c0b9ac7b6766e84c0428830865e2b0e0c9dce4de0b1c6fece209f0cff7caaaf0` over 24816 bytes and 262 lines, and C0a and C0b resolve to the SAME git blob `6ad04752`. THE EXTRACTION, run over the committed C0a blob by the reviewer's own marker-line extractor, printed 4 slices over 54 CONTENT lines against a TOTAL of 262, so PROSE is 208 and constraint 9 reproduces exactly. `.agent/plan.md` at `9a65c1a6` is 2473 bytes = PLANF022R13's 2472 plus exactly one newline, with the BARE-slice control FALSE, `^## Goal$` and `^## Next Steps$` once each and 44 lines against the cap of 50. THE PAIR IS EXACT AND SURGICAL: the containment test printed `TO contains FROM: false`, MAPFROM13 went 1 to 0 and MAPTO13 0 to 1 in `.agent/live_review.md` at `3b4bb3e6`, byte length 560928 to 561000 with the delta 72 equal to MAPTO13's 300 minus MAPFROM13's 228, and the committed file equals the base file with ONLY that replacement applied — the reviewer reproduced that by applying the replacement to the base blob and comparing bytes. `^## Steps$` stays exactly once and the `## Steps` paragraph's longest line reads 80 characters against R-0431's 84. THE APPEND HOLDS UNDER BOTH READERS at `d3109219`: the C2 blob is a byte-exact PREFIX of the C3 file and the remainder is 8169 bytes = 1 + LEDGER13's 8167 + 1, while the reviewer's own independent blank-line split counted N=2 paragraphs in the slice and found the LAST 2 units of the committed file equal to them IN ORDER over 273 units becoming 275. THE SETS MOVED EXACTLY WHERE THE ROUND PROMISED: 234 records at base and at C3, all DISTINCT at both with maximum `R-0673`, ids ADDED and ids REMOVED both the EMPTY SET so NO ID WAS MINTED, `^Done: R-` 2 and 2 over `R-0653` and `R-0670`, `^Landed: ` 0 and 0, `^Recurrence: R-` 7 becoming 8 by gaining `R-0533`, `^Gate: R` 12 becoming 13 by gaining the key `R12`, and `^- R-0533 — ` exactly 1 at both points. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout with never two pytest processes alive at once: `tests/ui_server/` 470, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21 and `tests/orchestration/test_integrity_gate.py` 16 for 559 across the four, and the canary `tests/cli/test_golden_path.py` 42 — every one exit 0 and every one matching the block's reference figure exactly. THE REVIEWER'S OWN SPOT-CHECK WAS THE R-0533 RECURRENCE'S RANGE WALK, because that recurrence is the only new claim the round put on disk and a correction that is itself unmeasured would be worse than the sentence it corrects: walking each round's own range with `git diff --name-only`, R8 `142af5e4..e5c86774` and R10 `a8952614..3e1d3fae` each changed `tests/ui_contracts/test_cost_metric_render.py` while R9 `e5c86774..a8952614` and R11 `3e1d3fae..fe6da915` changed no `.py` path at all, and NONE of the four touched `packages/orchestration/ui_server.py` — so both halves of the recurrence reproduce: the "held no Python path" clause really is false for two of the four rounds, and the routing conclusion it was written to support really is true and really was measured. `git merge-base main HEAD` is `c34ef32b`, the SHA the plan and the context file both name. STRUCTURE HELD: 5 commits before the handback, every one single-parent, insertions 262, 146, 14, 4 and 4, each far under the 500 cap; the range path set is exactly the five declared paths with the difference EMPTY in BOTH directions; `git show --numstat` agrees cell by cell with all five `## Commits` rows including the full-file rewrite at `13fb4285`, which reads plus 146 minus 233 in the table and 146 then 233 from the tool — the R-0592 shape, correct here; the anchored markers `^<<<SLICE ` and `^<<<END ` count 0 in both state files; `git ls-files .remedy-wt` is 0; one worktree; and all 6 reflog rows of the round carry the action `commit`, with amend, rebase and cherry each 0. THE HANDBACK IS COMPLIANT at 123 lines with a DECISION D15 stated cause naming that same 123, every mandated section present exactly once and in order, and the three-line `Fortschritt:` block byte-identical to the block's. THE OPEN PR GATE printed an empty JSON array and no PR was created. THE VERDICT IS PASS: every numeral R13 states reproduced under the reviewer's own measurement, no slice was edited, no id was minted, the map now describes the rounds that remain, and R12's verdict — the one this round existed to rescue — is on disk where the next session reads it.
<<<END LEDGER14

<<<SLICE DEC14
## DECISION F022 D8 — when the ledger figure replaces the live one, and what the delta says

CONTEXT. DECISION F022 D7 ruled the SOURCE of the terminal reconciliation: the
last `budget.tick` in the job's run log, served as the dashboard's
`budget_final`. It deliberately ruled nothing about WHEN the client swaps the
live value for that one, nor about what counts as a delta worth showing, because
no client code existed to rule over. Measured at `5d3e6045`: the shell holds the
latest received tick on `stream.budget` and hands it to the bar through
`metricsWithCostTicker`, while `budget_final` reaches the payload and has NO
client reader at all — the dashboard type does not name it.

CHOSEN, clause by clause.

1. THE TRIGGER is terminal AND a ledger figure: the reconciliation runs exactly
when the dashboard's `live.running` is false and the ledger figure is not null.
While the job runs, the ledger's last tick and the client's last tick are the
same event, so rendering one as "final" would claim a finality the run has not
earned — and it would do so in the feature built to stop exactly that.

2. THE FIGURE SHOWN IS THE LEDGER'S, and it is rendered through `costMetricOf`
like any other tick. The reconciliation module chooses no unit, no denominator,
no marker and no threshold; it hands the ledger payload to the module that
already owns those rules. This is what keeps the arithmetic home single, and
`tests/ui_contracts/test_cost_metric_render.py` enforces it independently, as
measured at `5d3e6045`.

3. THE DELTA IS LABELLED WHEN THE DISPLAYS DIFFER, and it is named rather than
computed. The comparison is between the ledger view's `display` string and the
received view's `display` string. Comparing the DISPLAYS rather than the raw
figures is the deliberate half: both sides are the same producer's counters, so
a real missed frame moves the shown value, while a difference below the display
precision would render as a label naming two identical figures — a sentence that
contradicts itself on the reader's screen and teaches them to ignore the next
one. ACCEPTED COST, stated rather than hidden: a transport gap smaller than two
decimal places, or smaller than the token formatter's own rounding, is not
surfaced. The figure shown is the ledger's and therefore correct either way;
what is lost is only the notice, and a notice nobody can verify against the
screen is worth less than the trust it spends.

4. AN ABSENT SIDE IS ABSENT. No received figure at terminal renders the ledger
figure with NO label, because a label naming an em dash as the live estimate
would invent a reading the client never took. No ledger figure changes nothing
at all and the live tile stands, which is the same honesty rule that stops a
limitless job fabricating a denominator.

ALTERNATIVES CONSIDERED. Comparing the raw figures: rejected for the
self-contradicting on-screen label clause 3 describes. Reconciling whenever a
ledger figure exists, without the running check: rejected because it claims
finality mid-run. Rendering the difference itself as a magnitude: rejected twice
over, because the feature file's own wording names both values rather than their
difference, and a magnitude is the second arithmetic D7's closing clause forbids
the client. Holding the reconciliation in `costTicker.ts` instead of a new
module: rejected because that module's contract is the LIVE tick, and a second
responsibility there would put the terminal rules where nobody searching for
them would look.

REVERSE IT path by path, derived from this round's Change set rather than from
the files most in mind. Delete `apps/ui/src/api/costReconciliation.ts` and
`apps/ui/src/api/costReconciliation.test.ts`. In `apps/ui/src/api/types.ts`
remove `budgetFinal` from `RemedyDashboard` and `costFinalNote` from
`RemedyMetric`. In `apps/ui/src/api/remedyApi.ts` remove the `budget_final`
mapping, and in `apps/ui/src/api/remedyApi.test.ts` its three cases. In
`apps/ui/src/components/shell/RemedyShell.tsx` unwrap the call so
`metricsWithCostTicker(dashboard.metrics, stream.budget)` is again the whole
argument. In `apps/ui/src/components/metrics/TopMetricsBar.tsx` remove the note
render, and in `tests/ui_contracts/test_cost_metric_render.py` the class that
pins it. In `.agent/plan.md` and `.agent/live_review.md` nothing is reversed:
those record round history rather than this decision. That is every path this
round's Change set holds, which is what R-0672 and its recurrence require of a
reversal instruction.
<<<END DEC14
