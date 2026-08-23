── STEP T003a/3 — F022 Live cost ticker · Runde 10 ───────────────────────────

Fortschritt: ~70 % (T001 fertig · T002 fertig · T003a diese Runde · T003b offen;
             diese Runde verdrahtet den Ticker zum ersten Mal live und schreibt
             das R9-Urteil auf Platte) — Schaetzung

Goal:        Make the COST metric REACH the metrics bar. `costMetricOf` has been
             correct and pinned since R7 and drawn since R8, and it has no
             production caller at all, so the tile a user sees is not merely
             empty — it is absent. This round carries the latest budget tick
             from the one stream ingest point to the bar, and records the R9
             verdict on the way.

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the plan ·
             C2 repair the round map · C3 the R9 verdict and the R-0644
             recurrence · C4 DECISION F022 D6 · C5 the tick reader · C6 the
             stream state and the runner view · C7 the metric composition and
             the dashboard's cost tile · C8 the shell wiring and its source
             contract · C9 the R-0671 assertion · C10 the handback.

Change:      Exactly these paths, nothing else:
               .agent/authored/f022-r10.md                        (C0a)
               .agent/last_block.md                               (C0b)
               .agent/plan.md                                     (C1)
               .agent/live_review.md                              (C2, C3)
               .agent/decisions.md                                (C4)
               apps/ui/src/api/budgetTick.ts                      (C5, NEW)
               apps/ui/src/api/budgetTick.test.ts                 (C5, NEW)
               apps/ui/src/api/brainStream.ts                     (C6)
               apps/ui/src/api/brainStream.test.ts                (C6)
               apps/ui/src/api/brainStreamRunner.ts               (C6)
               apps/ui/src/api/brainStreamRunner.test.ts          (C6)
               apps/ui/src/api/costTicker.ts                      (C7, NEW)
               apps/ui/src/api/costTicker.test.ts                 (C7, NEW)
               apps/ui/src/api/remedyApi.ts                       (C7)
               apps/ui/src/api/remedyApi.test.ts                  (C7)
               apps/ui/src/components/shell/RemedyShell.tsx       (C8)
               tests/ui_contracts/test_cost_metric_render.py      (C8)
               apps/ui/src/api/costMetric.test.ts                 (C9)
               .agent/handoff.md                                  (C10)

─── Slice convention ──────────────────────────────────────────────────────────
Each authored text below begins at its `<<<SLICE <name>` line and ends at its
`<<<END <name>` line; neither marker line is part of the slice, and no slice
contains a marker line. Extract them PROGRAMMATICALLY by marker line out of the
committed C0a blob — never retype, never rewrap, never reflow. The whole-text
slices are PLANF022R10, LEDGER10 and DEC6. MAPFROM and MAPTO are the halves of a
FROM/TO pair, and this block carries no other pair. Every slice is quoted
WITHOUT its trailing newline; PLANF022R10 replaces its file whole, and LEDGER10
and DEC6 each land as one newline plus the slice plus one newline.

CONTAINMENT TEST, run by the reviewer on the final bytes, output quoted:
  MAPFROM/MAPTO — `TO contains FROM: false` → REWRITE.
That is the reading for every pair this block carries, taken per pair; none of
it is generalised from another.

Constraints:
 1. NEVER edit a slice. Apply it byte for byte. If a slice contradicts a fact
    you measure, apply it anyway and DECLARE the contradiction in the handback
    under Deviations. Repair nothing outside your slices; rule on nothing.
 2. C1 is the FIRST substantive commit (§3 checklist item 23): this round
    touches the finding ledger, so the plan advances before anything else but
    the two block-save commits.
 3. COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4, C5, C6, C7, C8, C9, C10 and no
    other. C2 applies the ONE pair; C3, C4 are pure appends. Doing the pair
    before the appends is what leaves each append reading over a single-valued
    remainder (R-0639/R-0640). LEDGER10's two paragraphs land in ONE commit, C3,
    or neither: the `Gate: R9` paragraph states that the recurrence is written
    in that same commit, and THIS constraint is what makes that true (§3 item
    20, R-0524 carve-out).
 4. THE PRODUCTION CHANGE IS DESCRIBED, NOT SLICED. C5 through C9 carry no
    authored bytes: you write that code yourself, to the specification below,
    under AGENTS.md's self-review loop. The specification fixes behaviour and
    seam, never wording — name things per AGENTS.md "Code Discoverability
    Conventions" and carry the one-line WHY comment above each new definition.
 5. NO CSS AND NO NEW VISUAL TOKEN. R8 already shipped the coin, the estimate
    marker, the track and the threshold treatment for this tile, and DECISION
    F022 D5 rules them. This round makes the tile REACHABLE and changes nothing
    about how it looks, so `docs/ui/design_reference/` is satisfied by R8's
    ruling and no `.module.css` file is in the Change set.
 6. NO BACKEND CHANGE. Nothing under `packages/` is in the Change set. The tick
    already reaches the client: `_safe_event_summary` puts a `budget` key on a
    `budget.tick` frame and on no other kind. This round consumes that and adds
    nothing to it.
 7. R-0670 IS NOT REPAIRED HERE and that is deliberate. It is routed to the next
    round that touches `packages/orchestration/ui_server.py` on its own account,
    constraint 6 keeps that file out of this Change set, and rewriting a landed
    comment inside an unrelated commit is the move R-0427 records as wrong.
 8. Destructive verification runs ONLY inside a disposable worktree under
    `.remedy-wt/`. The primary checkout satisfies `git status --porcelain`
    empty at every commit and at the handback. Run no suite concurrently with a
    working-tree reading (R-0479).
 9. Every numeral this block states about the ROUND BASE `a8952614` was produced
    by a reviewer script at that commit and is a REFERENCE to report against,
    not a target to reproduce. Where your measurement differs, report BOTH and
    reconcile NOTHING.
10. Size, measured by the reviewer on the final bytes of this block and stated
    once here: this block is 482 lines TOTAL with 121 CONTENT lines inside its
    slices, so PROSE is 361 — under DECISION F085 D6's 490 and D5's 400.

─── What the reviewer measured at `a8952614`, and why this round exists ───────

`costMetricOf` HAS NO PRODUCTION CALLER. Searched repo-wide, by reading every
`.ts` and `.tsx` under `apps/ui/src` except `*.test.ts` and `*.test.tsx`: the
only non-test file containing the string `costMetricOf(` is
`apps/ui/src/api/costMetric.ts` itself, at its own `export function` line. Every
other occurrence is in `costMetric.test.ts`.

`normalizeDashboardPayload` BUILDS NO COST METRIC. Its `const metrics:
RemedyMetric[] = [` literal at line 87 yields the keys `open`, `planned`,
`done`, `progress` and `tokens` directly plus two helper-built entries,
`metricTests` and `metricProof` — seven, and `cost` is not among them. So
`RemedyMetric.cost` is never populated by anything, `TopMetricsBar` never
receives a `cost` metric to render, and the feature that R7 and R8 built is
invisible in the running application. That is what T003a fixes, and it is why
this round comes before the terminal reconciliation rather than after it.

THE GUARD THIS ADDITION BREAKS, named per §3 checklist item 7 rather than
discovered by the worker: `apps/ui/src/api/remedyApi.test.ts` line 343 opens
`it("tokens is the last metric, order is open/planned/done/progress/tests/proof/
tokens", ...)`, line 345 asserts `expect(result.metrics).toHaveLength(7)` and
line 347 asserts the seven keys in order. An eighth metric turns both assertions
red and makes the test's own NAME false. C7 therefore updates the assertions AND
the test name in the SAME commit as the source change — that is not scope drift,
it is the pin moving with the thing it pins.

THE OTHER WRITER, checked because a single reading is not a repository claim
(R-0419): `remedyApi.ts` holds a second `metrics: [` at line 301, inside
`normalizeApiFailure`. It builds four entries and is the DEGRADED path, reached
only when endpoints failed. It gains NO cost tile, because a dashboard that
could not load has no stream figures either and a tile there would be a promise
the degraded path cannot keep. C7 records that as a deliberate absence in a
comment where a reader would search for it.

─── The production change, specified ──────────────────────────────────────────

C5 — `apps/ui/src/api/budgetTick.ts`, NEW. One exported total function,
`budgetTickFiguresOf(frame: BrainStreamFrame): BudgetTickFigures | null`. It
takes `BrainStreamFrame` and `BudgetTickFigures` with `import type` only, so the
emitted runtime graph does not name `brainStream.ts` back — the same one-way
shape `feedRow.ts` already documents in its own header. It returns null unless
the frame's envelope carries the kind `budget.tick` AND a `budget` object;
otherwise it returns that `budget` object. It CHECKS every field rather than
asserting: the envelope is parsed JSON from a server this client does not
control, and the kind is `frame.event.event`, which reads like a typo and is
not one. It performs no arithmetic and composes no sentence — those are
`costMetric.ts`'s job and this module does not duplicate them.
`budgetTick.test.ts` pins: a tick frame yields its figures; a non-tick frame
yields null; a tick frame with no `budget` key yields null; a frame whose
`event` is a string, null, an array or absent yields null and throws nothing.

C6 — `brainStream.ts` gains `budget: BudgetTickFigures | null` on
`BrainStreamState`, null in `initialBrainStreamState()`. `receiveBrainFrame`
folds it BEHIND the replay guard, in the same position as the `feedRowOf`
projection and for the same reason: a reconnect replay must not re-apply a tick.
The fold CARRIES THE PREVIOUS VALUE FORWARD when the frame is not a tick, and it
carries it forward BY REFERENCE — `state.budget`, never a copy — because the
runner compares this field with `===` and a fresh object equal in content would
announce a change nobody made. A replay still returns the IDENTICAL state
object, ring and budget included.
`brainStreamRunner.ts` gains `budget: BudgetTickFigures | null;` on
`BrainStreamView`, seeded in `cachedView` from `state.budget` rather than from a
literal, and compared in `publish` with `next.budget === cachedView.budget`
alongside the existing five comparisons. The field's type is NAMED and never an
inline object literal: `tests/ui_contracts/test_brain_stream_ring.py`'s
`test_the_view_type_carries_the_ring` slices the interface to the FIRST `}`
after its opening line, so a brace inside a field type would truncate that slice
and take an unrelated assertion red.
The two `.test.ts` files gain the matching cases: a tick frame sets `budget`; a
later non-tick frame leaves it `===` identical; a replayed tick does not
re-apply; the view publishes it; a tick that changes nothing else still
publishes once and a non-tick frame that changes nothing publishes not at all.

C7 — `apps/ui/src/api/costTicker.ts`, NEW. One exported function,
`metricsWithCostTicker(metrics: readonly RemedyMetric[], figures:
BudgetTickFigures | null): RemedyMetric[]`. It returns a NEW array in which the
`cost` entry — and only that entry — carries `cost: costMetricOf(figures)` and
`unknown: false` when `figures` is non-null, and is returned unchanged when
`figures` is null. It calls `costMetricOf` and decides nothing else: the unit,
the denominator, the marker, the thresholds and the tooltip lines are all
DECISION F022 D4's and they stay in `costMetric.ts`. When `metrics` carries no
`cost` entry it returns the input array UNCHANGED and by reference, so a
degraded dashboard is untouched and React sees no new identity.
`remedyApi.ts` adds the eighth entry to the `const metrics` literal, AFTER
`tokens`: `{ key: "cost", label: "Cost", value: "—", unknown: true }`. It is
`unknown` at load because no tick has arrived, which is exactly the honest em
dash `docs/ui/design_reference/ux_spec.md` §10 requires for a value that is not
yet derivable — never a fake zero. `costTicker.test.ts` pins: the cost entry is
filled from a tick; a null tick leaves the array reference-identical; an array
with no cost entry is returned by reference; no other entry is mutated.

C8 — `RemedyShell.tsx` passes `metricsWithCostTicker(dashboard.metrics,
stream.budget)` to `TopMetricsBar` in place of the bare `dashboard.metrics`.
Nothing else in that file changes; `streamStatus={stream.status}`,
`recent={stream.recent}`, `recentDropped={stream.recentDropped}` and the
`// The cockpit subscribes HERE` comment all stay exactly as they are, because
`tests/ui_contracts/test_remedy_shell_stream.py` and
`test_brain_stream_ring.py` assert each of them against this file.
`tests/ui_contracts/test_cost_metric_render.py` gains a class pinning the PATH
this round builds, against comment-stripped source in that file's existing
style: the shell hands `stream.budget` to the bar through
`metricsWithCostTicker(`; `costTicker.ts` names `costMetricOf(` and performs no
division of its own; and `costMetric.ts` is the ONLY non-test source under
`apps/ui/src` naming any of `spent_usd`, `spent_tokens`, `limit_usd` or
`limit_tokens`. That last assertion is the one R-0673 binds, and G12 below runs
it at the base first rather than asserting it blind.

C9 — `costMetric.test.ts` gains ONE assertion, which is the whole of R-0671's
fix: a NEGATIVE `spent_usd` with a usable `limit_usd` renders the LIMITLESS
view. `usableFigure` already rejects a negative, the module is correct, and the
missing thing is the proof.

─── Done when ─────────────────────────────────────────────────────────────────

Run every gate below yourself, record its REAL exit code, and put ONE LINE per
gate in the handback with the transcripts kept out of it (R-0582). G1 through
G13 run after C9 and BEFORE C10, so the handback can quote all of them (§3
checklist item 31). The round base is `a8952614` throughout.

 G1  `.agent/STOP` absent, read from disk before C0a and again before C10.
     Branch `feature/f022-live-cost-ticker`. `git status --porcelain` 0 lines
     after every one of C0a through C9.
 G2  TRANSPORT. sha256 over the block file the reviewer wrote at
     `.remedy-wt/f022-r10.md`, over the committed C0a blob, over the committed
     C0b blob and over `.agent/last_block.md` on disk: report all four digests,
     byte counts and line counts, and require them EQUAL. The digest the
     delegation names is the fifth reading and must agree.
 G3  EXTRACTION. Run an extractor over the COMMITTED C0a blob that finds the
     slices by their marker LINES and report how many slices and how many
     CONTENT lines it printed, plus the block's TOTAL and PROSE line counts.
     Report those against constraint 10's numerals; reconcile nothing.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF022R10 plus exactly one
     newline. NEGATIVE CONTROL: the same comparison against the BARE slice must
     be FALSE, and report both byte counts. `^## Goal$` once, `^## Next Steps$`
     once, `wc -l` at most 50.
 G5  THE PAIR at C2. Report the containment test's own output for MAPFROM in
     MAPTO — it must print false, matching the convention block. Then: MAPFROM
     occurs exactly 1x in `.agent/live_review.md` at the round base and 0x at
     C2; MAPTO occurs 0x at base and exactly 1x at C2; the file's byte length
     changes by exactly `len(MAPTO) - len(MAPFROM)`; and `^## Steps$` still
     occurs exactly once at C2. Report each count as a number.
 G6  APPEND at C3, proved twice, and the same two readers at C4. For each: the
     previous commit's blob is a byte-exact PREFIX of the committed file and the
     remainder is exactly one newline plus the slice plus one newline — report
     the remainder's byte count and the slice's. Then an INDEPENDENT reader:
     split both files on blank lines, let N be the number of paragraphs YOUR
     script counts in the slice, and require the LAST N units of the committed
     file to equal the slice's N paragraphs IN ORDER. Report N; do not take it
     from this block. NEGATIVE CONTROL, in a disposable worktree, applied to the
     FIRST appended paragraph of LEDGER10 and to the FIRST of DEC6: flip ONE
     byte at an offset you name and confirm BOTH readers reject each mutant
     while both accept the true file. THE OFFSET IS A BYTE OFFSET, and the
     reviewer's own dry run is why this is spelled out: both files carry
     multi-byte em dashes and arrows, so a CHARACTER offset lands thousands of
     bytes early, outside the appended region — where reader (b) accepts the
     mutant, correctly, because it compares only the last N units, and the
     control silently proves nothing. Report the ~20 bytes surrounding each
     flip so the placement is auditable. Remove the worktree; `git worktree
     list` back to one line.
 G7  LEDGER INTEGRITY, base versus C3. Report for both points: the count of
     lines matching `^- R-\d+ — `, whether they are all DISTINCT, the MAXIMUM
     id, the count of `^Done: R-` with its distinct ids, of `^Landed: `, of
     `^Recurrence: R-` with its distinct ids, and of `^Gate: R` with its
     distinct keys. Report the ids ADDED and REMOVED as sets. At base the
     reviewer measured 234 records, all distinct, maximum `R-0673`, 1 `Done:`
     line for `R-0653`, 0 `Landed:`, 3 `Recurrence:` lines and 9 `Gate:` lines
     over 9 distinct keys. This round MINTS NO NEW ID: it is expected to add no
     record, to take `^Recurrence: R-` to 4 by gaining `R-0644`, and to add
     `Gate: R9`. Report what you measure. `R-0644` must still occur exactly once
     as a `^- R-0644 — ` record.
 G8  DECISIONS at C4. `^## DECISION F022 D6 ` occurs exactly once in
     `.agent/decisions.md` at C4 and 0 times at the round base. Report both.
 G9  `npm run typecheck` in `apps/ui`, exit 0. The reviewer measured exit 0 with
     no output at the round base.
 G10 `npm run test:unit` in `apps/ui`, exit 0. Report the FILE count and the
     TEST count. The reviewer measured 17 files and 241 tests at the round base;
     this round adds test files and tests, so report the difference and account
     for it by naming which new file contributes what.
 G11 `python3 -m pytest tests/ui_contracts/ -q` from the REPOSITORY ROOT, exit
     0. Report passed and skipped. The reviewer measured 514 passed and 4
     skipped at the round base. Run it from the repository root and say so: the
     same command run from `apps/ui` collects nothing and exits reporting no
     failure, which is a green that means nothing (R-0463).
 G12 THE ABSENCE CLAUSE, RUN AT THE BASE FIRST (R-0673). Before C8, run the new
     contract's "single arithmetic home" assertion over the BASE tree and report
     its result, then run it again at C8. The reviewer ran it at `a8952614`,
     over every `.ts` and `.tsx` under `apps/ui/src` that is not `*.test.ts` or
     `*.test.tsx`, with comments stripped: the files naming ANY of the four
     strings `spent_usd`, `spent_tokens`, `limit_usd`, `limit_tokens` are
     `apps/ui/src/api/costMetric.ts` and no other. The clause is SATISFIED at
     the base, so this round is licensed to remove NOTHING to meet it, and the
     round must keep it satisfied: `budgetTick.ts` passes the whole `budget`
     object through and `costTicker.ts` calls `costMetricOf`, so neither names a
     figure field. A blanket "no `/` anywhere" was considered and REJECTED as
     the assertion, because 28 spaced divisions live in the graph, timeline and
     layout modules at the base and a clause that forbids them forbids the
     round's own geometry — the R-0673 shape this gate exists to avoid. If your
     base run disagrees with either reading, report the disagreement, write the
     assertion to match what YOU measured, and say so.
 G13 STRUCTURE, reported for the commits BEFORE C10 and for the range as a whole
     (C10's own numbers belong to the next round's ledger entry, not here):
     every commit single-parent; each commit's INSERTION count, each under the
     500 cap; the range path set against the Change set above with the
     difference reported in BOTH directions; `git show --numstat` agreeing cell
     by cell with the handback's `## Commits` table; the LINE-ANCHORED patterns
     `^<<<SLICE ` and `^<<<END ` counting 0 in `.agent/plan.md`,
     `.agent/live_review.md` and `.agent/decisions.md` — ANCHORED because a
     slice of this block legitimately quotes those markers mid-line inside
     backticks, so an unanchored count would be unsatisfiable for every possible
     round (§3 checklist item 2); `git ls-files .remedy-wt` 0; one worktree; and
     the round's reflog rows with amend, rebase and cherry counts, each 0.
 G14 THE FOUR STATE READERS plus THE CANARY, serially in the PRIMARY checkout at
     C9, exit 0: `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py`,
     `tests/orchestration/test_integrity_gate.py`, then
     `tests/cli/test_golden_path.py`. The reviewer measured 544 passed across
     the four and 42 for the canary at the round base. Never run two pytest
     processes at once.
 G15 `gh pr list --state open --json number,headRefName`. Report it verbatim.
     Create no PR and merge nothing this round: T003b is unbuilt and the
     integration gate has not run.
 G16 STALENESS. Every sentence C1 through C4 land that states a fact about a
     file is re-measured at C4, and any that has gone stale is reported as a
     residual rather than repaired. Report explicitly that you checked, and name
     any residual. Slices are NEVER edited to fix one.

NOT A GATE and not run this round: `npm run lint`. It is RED at the base for
reasons this round does not create — 72 problems, which is R-0622 and routes to
a paydown branch — and R-0364 forbids ordering a gate that cannot fail honestly.

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             every mandated section in order, one changed-files table per
             commit, an item-status row per Bundle item, the round base SHA,
             ONE line per gate, and the `Fortschritt:` block above carried
             VERBATIM across all three of its lines. Every count you report
             names the exact string or pattern counted and the file it was
             counted in (R-0442). The cap is 100 lines for this commit count;
             declare a DECISION D15 stated cause with your own measured numeral
             in the declaring line if the mandated content genuinely does not
             fit. The `## Next` section names R11 — T003b, the terminal
             reconciliation and the delta labelling — and states that the
             feature file's "stats endpoint" does not exist among the job
             endpoints, so R11 must rule its source as a DECISION before it can
             build against it.
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF022R10
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
R10 is T003a, the live wiring. It records the R9 verdict and the R-0644
recurrence, repairs the round map, rules DECISION F022 D6, and then carries the
latest budget tick from the stream's one ingest point through the runner view
and the shell into the metrics bar — the step that gives `costMetricOf`, correct
since R7 and drawn since R8, its first production caller. It also pins R-0671's
missing assertion.

## Next Steps
1. R11 T003b — the terminal reconciliation, the delta labelling and the
   fake-job end-to-end, opening with the DECISION that rules where the ledger's
   final figure is read from.
2. R12 the integration gate.
3. R13 closure.

## Risks
- The feature file names "the stats endpoint" as the source of the ledger figure
  for the terminal reconciliation, and no such endpoint exists among the job
  endpoints `ui_server.py` dispatches. R11 opens by ruling that source as a
  DECISION rather than by building against a name.
- Open F022 findings, each with the round that owns it: R-0670 waits for the
  next round touching `packages/orchestration/ui_server.py` on its own account;
  R-0672 and its recurrence want a path-by-path reversal, which DECISION F022 D6
  carries; R-0673 wants a whole-file absence run at the base first, which G12
  does; R-0644's recurrence is the correction this round appends.
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks, not F022 defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- R-0665 is open and this feature needs its route: every UI feature is told to
  record visual deviations in an `assumption_log` that does not exist. F022
  records them as DECISIONs in `.agent/decisions.md`, a route rather than a fix.
<<<END PLANF022R10

<<<SLICE MAPFROM
carries none of the tick's figures today → R7 T002 the COST metric → R8 T003
the terminal reconciliation and the delta labelling → R9 the integration gate →
R10 closure. This section is the only place the round map is stated, per
R-0447's remedy, and a round whose scope this map does not describe repairs the
map in that same block or is not emitted, per R-0455.
<<<END MAPFROM

<<<SLICE MAPTO
carries none of the tick's figures today → R7 T002a the COST metric module and
the DECISION that rules its semantics → R8 T002b the render, its goldens and its
source contract → R9 record the R8 verdict and end that session at its round
budget → R10 T003a the live wiring, which gives the cost module its first
production caller, plus the R9 verdict and this map repair → R11 T003b the
terminal reconciliation and the delta labelling → R12 the integration gate →
R13 closure. This section is the only place the round map is stated, per
R-0447's remedy, and a round whose scope this map does not describe repairs the
map in that same block or is not emitted, per R-0455. The map is repaired at R10
rather than at R9 because R9 discovered the drift and had no pair over this file
in its change set.
<<<END MAPTO

<<<SLICE LEDGER10
Recurrence: R-0644 — A REVIEWER-AUTHORED SLICE STATED A COUNT OF A SOURCE FILE'S CONTENTS AND THE SOURCE CONTRADICTS IT, IN A RECORD THAT IS APPEND-ONLY. Second instance, at F022 R9, and it is R-0644's own STANDING RULE going unserved by the reviewer who could have read it. NO NEW ID IS MINTED: §3 checklist item 30 requires the open set searched for the DEFECT before an id, and R-0644 already holds this exact class with the rule that a slice asserting a COUNT about a file outside the block names the SHA per item 20 AND has that count produced by a script at that SHA, or states the enumeration and no numeral at all. THE INSTANCE: the `R-0673` record committed at `5f8cb0cc` says the private `formatTokens` in `apps/ui/src/components/metrics/TopMetricsBar.tsx` "at lines 27 to 31 divides three times" at `142af5e4`. Item 20 was satisfied — the SHA is named and it is the right one — and the numeral was a hand reading. MEASURED at `142af5e4` by script, over `git show 142af5e4:apps/ui/src/components/metrics/TopMetricsBar.tsx`: lines 27 to 31 are the whole of `formatTokens`, and they hold TWO `/` characters and TWO division operators, `value / 1_000_000` on line 28 and `value / 1_000` on line 29. THE CORRECTED VALUE IS TWO. FOUND BY THE WORKER, which measured the slice it had been ordered to apply byte for byte, applied it anyway as constraint 1 required, and declared the contradiction as deviation 2 of the R9 handback — the fifth consecutive round in which a worker's declaration rather than a gate is what put a reviewer-authored defect on the record. WHY THIS CHANGES NOTHING ABOUT R-0673: two divisions make the R8 block's P6 whole-file "no `/`" assertion unsatisfiable while `formatTokens` stands, exactly as three would, so the forced removal R-0673 describes was correct and its counter-measure is unaffected. WHY IT IS RECORDED ANYWAY: `.agent/live_review.md` is what a later session reads to learn what was verified, and a wrong count there is indistinguishable from a right one without re-running a commit that has already been reviewed and closed. THE LANDED PARAGRAPH IS NOT REWRITTEN, per §3 item 20: this correction is dated by the commit that carries it and the wrong sentence stands above it. Both instances stay OPEN under R-0644, and the fix is the one R-0644 already names — the script, run in the same pre-emission pass that measures the block's own size.

Gate: R9 — the F022 R9 entry. R9 PASSED ON EVERY ONE OF ITS ELEVEN GATES, AND THE REVIEWER RE-RAN EVERY MEASURABLE ONE OF THEM ITSELF AND ADDED A MUTATION THE BLOCK NEVER ORDERED. The recurrence above is written in THIS SAME COMMIT, which the R10 block's constraint 3 fixes. TRANSPORT HELD IN ITS STRONGEST FORM: the reviewer's own scratch original survived the session boundary, so §4.9's primary comparison was available and was used rather than the digest fallback — `.remedy-wt/f022-r9.md`, the committed C0a blob, the committed C0b blob, `.agent/last_block.md` on disk and `.agent/authored/f022-r9.md` on disk are ALL sha256 `6ffeb77ff4c8af4003c38ac5c234a8c30776b1ba3936a767838961078e6dc6ac` over 24266 bytes and 228 lines, and C0a and C0b resolve to the SAME git blob `8d2fc01c`. THE EXTRACTION out of the committed blob printed 2 slices over 47 CONTENT lines, so TOTAL re-measures at 228 and PROSE at 181, and constraint 9's numerals reproduce exactly. `.agent/plan.md` at `e8e0c510` is byte-equal to PLANF022R9 plus one newline at 2234 bytes against the bare slice's 2233, with the bare-slice control DIFFERING, `^## Goal$` and `^## Next Steps$` once each and 42 lines against the cap of 50. THE APPEND HOLDS UNDER BOTH READERS: at `5f8cb0cc` the round-base blob is a byte-exact PREFIX and the remainder is 9814 bytes, exactly one newline plus LEDGER9's 9812 plus one newline, while an independent blank-line splitter reads 262 units before and 265 after and finds all three appended units equal to LEDGER9's three paragraphs IN ORDER at 2235, 1620 and 5953 bytes. THE SETS MOVED EXACTLY WHERE THE ROUND PROMISED: 233 records at base and 234 at C2, all DISTINCT at both, maximum id `R-0672` to `R-0673`, ids ADDED exactly `{R-0673}` and ids REMOVED the EMPTY SET, `^Done: R-` 1 at both carrying exactly `R-0653`, `^Landed: ` 0 at both, `^Recurrence: R-` 2 to 3 gaining `R-0672`, `^Gate: R` 8 to 9 gaining the key `R8`, `^- R-0672 — ` still exactly 1 so the recurrence APPENDED rather than rewrote, `^## Steps$` once, and the map paragraph byte-identical at base and at C2. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout: the four state readers 455, 52, 21 and 16 for 544, and the canary `tests/cli/test_golden_path.py` 42 — both matching the numbers the block quoted. STRUCTURE HELD: five commits over `e5c86774`..`a8952614`, every one single-parent, insertions 228, 124, 11, 6 and 42, each under the 500 cap; the range path set is exactly the block's declared five-path Change set with the difference EMPTY in both directions; `git show --numstat` agrees cell by cell with all four of the handback's pre-handback `## Commits` rows, which is the reading §3 item 28 exists for and which full-file rewrites are where it bites — the `.agent/last_block.md` row reads `+124/-278` and so does the tool; lines BEGINNING `<<<SLICE ` or `<<<END ` count 0 in both slice targets; `git ls-files .remedy-wt` 0; one worktree; `git status --porcelain` empty; 0 amend, 0 rebase and 0 cherry. THE REVIEWER'S OWN UNORDERED MUTATION IS THE ONE THE BLOCK COULD NOT SEE: R9's G5 ordered a byte flipped in the FIRST and the LAST appended paragraph and said nothing about the MIDDLE one, so the reviewer flipped a byte inside the `Recurrence: R-0672` paragraph, computed in memory with the primary checkout never written, and BOTH readers rejected it while both accepted the true file — the tail-only reading R-0631 warns about cannot arise here, and now that is measured rather than assumed. THE HANDBACK IS COMPLIANT at exactly 73 lines with a DECISION D15 stated cause naming that same 73, every mandated section present and in order, and the three-line `Fortschritt:` block byte-identical to the block's. THE ROUND'S ONE SUBSTANTIVE DEVIATION IS CORRECT AND IT CORRECTS THE REVIEWER: the `formatTokens` division count is the R-0644 recurrence above. THE VERDICT IS PASS: every numeral R9 states reproduced under the reviewer's own measurement, the round wrote no production code as ordered, repaired none of the three findings it was forbidden to repair, and closed the books on a session that ended at its declared round budget with every reviewed round's verdict on disk.
<<<END LEDGER10

<<<SLICE DEC6
## DECISION F022 D6 — where the live tick is held, and how it reaches the bar

CONTEXT. `costMetricOf` has been correct since R7 and drawn since R8 and has no
production caller: measured at `a8952614` by reading every `.ts` and `.tsx`
under `apps/ui/src` except `*.test.ts` and `*.test.tsx`, the only non-test file
containing `costMetricOf(` is `costMetric.ts` itself. The tick reaches the
client already — `_safe_event_summary` puts a `budget` key on a `budget.tick`
frame and on no other kind — and nothing reads it.

CHOSEN. The latest tick's figures are held as ONE field on `BrainStreamState`,
folded in `receiveBrainFrame` behind the replay guard, carried forward BY
REFERENCE on every non-tick frame, published on `BrainStreamView` and compared
there with `===`. The shell composes the bar's metrics through one pure
function, `metricsWithCostTicker`, which calls `costMetricOf` and decides
nothing else.

WHY. `receiveBrainFrame` is the single ingest point every frame passes through
and the only place a reconnect replay has already been ruled on, so a fold there
inherits the replay guard instead of re-deriving it. Reference-carrying is not
an optimisation: the runner's `publish` compares with `===`, so a fresh object
of equal content would announce a change nobody made and re-render the cockpit
on every heartbeat. A pure composition function keeps the wiring under the
node-environment vitest, which cannot render React — the same reason
`cockpitLogic.ts` and `brainStream.ts` were extracted from their components.

ALTERNATIVES CONSIDERED. A second store subscribed to the same stream: rejected,
because `tests/ui_contracts/test_brain_stream_ring.py` pins exactly one
`useBrainStream(` call site and a second subscription is a second socket.
Deriving the figures inside `TopMetricsBar` from the feed ring: rejected,
because `FeedRow` deliberately drops the `budget` payload and widening it would
put the whole envelope behind a projection built for a feed. Fetching the
figures over the dashboard endpoint: rejected, because a ticker that polls is
not live and the transport already carries the value.

REVERSE IT path by path, derived from this round's Change set rather than from
the files most in mind. Delete `apps/ui/src/api/budgetTick.ts` and
`apps/ui/src/api/budgetTick.test.ts`; delete `apps/ui/src/api/costTicker.ts` and
`apps/ui/src/api/costTicker.test.ts`; in `apps/ui/src/api/brainStream.ts` remove
the `budget` field from `BrainStreamState`, its `null` seed in
`initialBrainStreamState` and the fold in `receiveBrainFrame`; in
`apps/ui/src/api/brainStreamRunner.ts` remove the `budget` field from
`BrainStreamView`, its seed in `cachedView` and its comparison in `publish`; in
`apps/ui/src/api/remedyApi.ts` remove the eighth `cost` entry from the `metrics`
literal and the deliberate-absence comment in `normalizeApiFailure`; in
`apps/ui/src/components/shell/RemedyShell.tsx` pass `dashboard.metrics` to
`TopMetricsBar` unwrapped; drop the budget cases from
`apps/ui/src/api/brainStream.test.ts` and
`apps/ui/src/api/brainStreamRunner.test.ts`, and restore the seven-key
assertions and the original test name in `apps/ui/src/api/remedyApi.test.ts`;
remove the wiring class from `tests/ui_contracts/test_cost_metric_render.py`.
The R-0671 assertion in `apps/ui/src/api/costMetric.test.ts` is NOT part of this
decision and a reversal keeps it. That is every production and test path this
round's Change set holds, which is what R-0672 and its recurrence require of a
reversal instruction and what DECISION F022 D5 did not do.
<<<END DEC6
