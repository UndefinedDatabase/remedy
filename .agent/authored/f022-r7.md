── STEP T002a/3 — F022 Live cost ticker · Runde 7 ────────────────────────────

Fortschritt: ~40 % (T001 fertig · T002 zur Haelfte nach dieser Runde · T003
             offen; ab hier rechnet der Client die Fuellung und sonst nichts)
             — Schaetzung

Goal:        Record the R6 verdict, register R-0670, rule the client's cost
             reading as DECISION F022 D4, and land T002's LOGIC half: a pure
             `costMetric.ts` that turns one budget tick into every render
             decision the COST metric needs, with vitest tests that pin each.

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the plan ·
             C2 the R6 verdict and finding R-0670 · C3 DECISION F022 D4 ·
             C4 the type widening, the cost module and its tests · C5 the
             handback.

Change:      Exactly these paths, nothing else:
               .agent/authored/f022-r7.md        (C0a)
               .agent/last_block.md              (C0b)
               .agent/plan.md                    (C1)
               .agent/live_review.md             (C2)
               .agent/decisions.md               (C3)
               apps/ui/src/api/types.ts          (C4)
               apps/ui/src/api/costMetric.ts     (C4, new file)
               apps/ui/src/api/costMetric.test.ts (C4, new file)
               .agent/handoff.md                 (C5)

─── Slice convention ──────────────────────────────────────────────────────────
Each authored text below begins at its `<<<SLICE <name>` line and ends at its
`<<<END <name>` line; neither marker line is part of the slice, and no slice
contains a marker line. Extract them PROGRAMMATICALLY by marker line out of the
committed C0a blob — never retype, never rewrap, never reflow. The slices are
PLANF022R7, LEDGER7 and DEC4.

Constraints:
 1. NEVER edit a slice. Apply it byte for byte. If a slice contradicts a fact
    you measure, apply it anyway and DECLARE the contradiction in the handback
    under Deviations. Repair nothing outside your slices; rule on nothing.
 2. C1 is the FIRST substantive commit (§3 checklist item 23): this round
    touches the finding ledger, so the plan advances before anything else but
    the two block-save commits.
 3. `.agent/plan.md` is a WHOLE-TEXT replacement. LEDGER7 and DEC4 are APPENDS
    to append-only records: never rewrite a landed paragraph in either file,
    and add nothing to them beyond the slice. This block carries NO FROM/TO
    pair.
 4. LEDGER7 holds the finding paragraph first and the gate paragraph second,
    separated by ONE blank line, and lands in ONE commit, C2. The gate
    paragraph states that R-0670 is registered in the same commit; THIS
    constraint is what makes that true (§3 checklist item 20, R-0524
    carve-out), so C2 carries both paragraphs or neither.
 5. C4 is ONE commit carrying the type widening, the module and its tests
    together.
 6. NO React, NO CSS and NO component file this round. `TopMetricsBar.tsx`,
    `TopMetricsBar.module.css`, `RemedyShell.tsx` and `remedyApi.ts` are OUT
    of the change set: the render and the wiring are R8. Do not touch budget
    enforcement, the pricing and basis rules, the emission, the envelope R6
    landed, or MetricsBar's other metrics.
 7. `apps/ui/src/api/costMetric.ts` MUST NOT import from `./types`, and
    `apps/ui/src/api/types.ts` imports the view type FROM `./costMetric`. That
    direction is the one that has no cycle. `costMetric.ts` therefore declares
    its own input and output types.
 8. Destructive verification runs ONLY inside a disposable worktree under
    `.remedy-wt/`. The primary checkout satisfies `git status --porcelain`
    empty at every commit and at the handback. A fresh worktree has no
    `apps/ui/node_modules`, so drive vitest at one from the PRIMARY install:
    `npx vitest run --root <worktree>/apps/ui --config <primary>/apps/ui/vitest.config.ts`
    run from the primary `apps/ui`. If your sandbox refuses `npx`, report that
    refusal as the gate's result and run the mutation as a temporary edit
    inside the worktree with the same command shape; never mutate the primary
    checkout.
 9. Every numeral this block states about the ROUND BASE `d97cdbb2` was
    measured by the reviewer at that commit and is a REFERENCE to report
    against, not a target to reproduce. Where your measurement differs, report
    BOTH and reconcile NOTHING.
10. TWO REPO-WIDE SWEEPS take in every new file under `apps/ui/src`, both in
    `tests/ui_contracts/` and both measured green at the round base, so know
    them before you write: `test_there_is_still_exactly_one_subscription`
    reads every non-test `.ts` and `.tsx` there and forbids `EventSource`
    outside `brainStreamDeps.ts` while pinning `useBrainStream(` at 2 sites,
    and `test_no_scanlines_in_frontend` reads every `.ts` including test files
    and forbids the string `scanline`. A pure cost module trips neither; G11
    is what proves it rather than this sentence.
11. Size, measured by the reviewer on the final bytes of this block and stated
    once here: this block is 362 lines TOTAL with 64 CONTENT lines inside its
    slices, so PROSE is 298 — under DECISION F085 D6's 490 and D5's 400.

─── What R7 builds ────────────────────────────────────────────────────────────

R6 put the tick's figures on the wire. Nothing reads them: `RemedyMetricKey` at
`apps/ui/src/api/types.ts:3` is a CLOSED union of seven strings with no `cost`
in it, and `RemedyMetric.value` is `number | "—"`, which has nowhere to put a
limit, a basis or a threshold. This round adds the reading and NOT the drawing.

The shape is F021's, and it is deliberate: every rule this client has lives in a
plain `.ts` module that the node-environment vitest can reach, and React is left
holding nothing but subscribe-and-render. `apps/ui/vitest.config.ts` measures as
`environment: "node"` with `include: ["src/**/*.test.ts"]` — so a `.test.tsx`
would not even be COLLECTED, and a component test is not available to this round
at any price. `apps/ui/src/api/feedRow.ts` beside its `feedRow.test.ts` is the
precedent to copy, down to declaring its own interface.

DECISION F022 D4 below rules the semantics. Read it as the specification; the
prose here does not repeat it.

─── The module ────────────────────────────────────────────────────────────────

New file `apps/ui/src/api/costMetric.ts`. It exports, at minimum:

  BudgetTickFigures  the envelope's `budget` payload as it ARRIVES — every
                     field optional, because this is parsed JSON from a server
                     the client does not control. Field names are the wire's,
                     which are snake_case: `spent_tokens`, `spent_usd`,
                     `limit_tokens`, `limit_usd`, `unmeasured_calls`, `basis`.
  CostLevel          `"normal" | "warn" | "exceeded"`.
  CostMetricView     what one COST metric renders: the formatted `display`
                     string WITHOUT any prefix, the `unit` it is in, an
                     `estimated` boolean the component turns into the `~`,
                     `fill` as a ratio or `null`, `level` as a CostLevel or
                     `null`, `limitless` as a boolean, and `tooltip` as an
                     ORDERED array of already-composed strings.
  costMetricOf       `(figures: unknown) => CostMetricView`. Total: it accepts
                     anything and never throws.

Every value the component will need is decided HERE. A component that had to
choose a unit, pick a denominator or compose a tooltip line would be a second
home for these rules, and the whole reason this module exists is that there is
exactly one.

Formatting lives here too — export `formatUsd` and `formatTokenCount`.
`TopMetricsBar.tsx:27-31` carries a private `formatTokens` with the same
1k/1M rule; do NOT touch it and do NOT import it. R8 makes the component use
the exported one and deletes the private copy, in the commit that already
touches that file.

─── The tests ─────────────────────────────────────────────────────────────────

New file `apps/ui/src/api/costMetric.test.ts`, in the conventions of
`apps/ui/src/api/feedRow.test.ts`. Every test below is REQUIRED and each must be
able to fail; add the discriminator that makes that true wherever an assertion
could pass for the wrong reason.

 U1  BOTH LIMITS CONFIGURED. Unit is usd, the denominator is `limit_usd`, and
     the tooltip enumerates BOTH limits with their own fills, usd line first.
     Discriminator: assert the token line is present too, so this cannot pass
     by the enumeration having been dropped.
 U2  ONLY A TOKEN LIMIT. Unit is tokens and the threshold is computed on the
     token fill. Pin all three levels and both boundaries: a fill just under
     0.85 is `"normal"`, exactly 0.85 is `"warn"`, exactly 1.0 is `"exceeded"`,
     and well over 1.0 stays `"exceeded"`.
 U3  LIMITLESS, IN BOTH ITS SHAPES. (i) spend exists and no limit does. (ii)
     `spent_usd` exists, `spent_tokens` does NOT, and only `limit_tokens` is
     configured — clause 1 finds no usable pair, so this is limitless too, and
     the token limit is NEVER borrowed as a dollar denominator. For each:
     `fill` is null, `level` is null, `limitless` is true, and NOTHING in the
     view names a denominator. Assert that over the SERIALISED view, not only
     over the fields — the acceptance criterion is that no fake denominator is
     rendered, and a stray tooltip line is a rendered denominator.
 U4  THE BASIS DRIVES THE MARKER, PER SHOWN UNIT. `estimated` is false only for
     an `"actual"` basis of the unit actually shown. Cover `"actual"`,
     `"lower_bound"`, `"absent"` and a MISSING basis object.
     Discriminator, and this is the one that matters: build a TOKENS-unit view
     whose `basis.tokens` is `"actual"` while `basis.cost` is `"lower_bound"`,
     and assert `estimated` is FALSE — a module that read the cost basis
     unconditionally would pass every other case in this test.
 U5  UNMEASURED CALLS REACH THE TOOLTIP. Pin the actuals line for
     `unmeasured_calls` of 0, of 1 and of 3, singular and plural both.
 U6  MALFORMED INPUT IS NOT AN ERROR. `null`, `undefined`, a string, an array,
     a number, `{}`, a negative spend, a `NaN` spend, a limit of `0` and a
     `basis` that is not an object each yield a view and throw nothing. A
     limit of `0` is NOT a denominator — assert that case lands on the
     limitless variant rather than on a division by zero.
 U7  NO PRICE ARITHMETIC IN THE FRONTEND — the Acceptance section's "guard on
     price constants in the frontend", living beside the code it guards.
     Read `costMetric.ts` off disk with `node:fs`, STRIP its block and line
     comments first — a token a comment merely mentions is not a token the
     code uses (R-0584) — and over what remains assert: zero case-insensitive
     matches of `price`, `rate`, `tariff`, `perToken` and `per_token`; and
     every numeric literal is one of the values D4 clause 5 permits. Assert
     the stripper actually removed something, so the guard cannot pass over an
     empty string.

─── Done when ─────────────────────────────────────────────────────────────────

Run every gate below yourself, record its REAL exit code, and put ONE LINE per
gate in the handback with the transcripts kept out of it (R-0582). G1 through
G14 run after C4 and BEFORE C5, so the handback can quote all of them (§3
checklist item 31). The round base is `d97cdbb2` throughout.

 G1  `.agent/STOP` absent, read from disk before C0a and again before C5.
     Branch `feature/f022-live-cost-ticker`. `git status --porcelain` 0 lines
     after every one of C0a, C0b, C1, C2, C3 and C4.
 G2  TRANSPORT. sha256 over the block file the reviewer wrote at
     `.remedy-wt/f022-r7.md`, over the committed C0a blob, over the committed
     C0b blob and over `.agent/last_block.md` on disk: report all four digests,
     byte counts and line counts, and require them EQUAL. The digest the
     delegation names is the fifth reading and must agree.
 G3  EXTRACTION. Run an extractor over the COMMITTED C0a blob that finds the
     slices by their marker LINES and report how many slices and how many
     CONTENT lines it printed, plus the block's TOTAL and PROSE line counts.
     Report those against constraint 11's numerals; reconcile nothing.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF022R7 plus exactly one
     newline. NEGATIVE CONTROL: the same comparison against the BARE slice must
     be FALSE, and report both byte counts. `^## Goal$` once, `^## Next Steps$`
     once, `wc -l` at most 50.
 G5  APPEND at C2 and again at C3, each proved twice. The round-base blob is a
     byte-exact PREFIX of the committed file, and the remainder is exactly one
     newline plus the slice plus one newline — report the remainder's byte
     count and the slice's. Then an INDEPENDENT reader: split both files on
     blank lines, report the unit counts before and after, and require the
     appended units to equal the slice's own paragraphs IN ORDER — for C2 that
     means EVERY paragraph of LEDGER7 is checked, not only the last (R-0578).
     Lines beginning `## DECISION F022 D4 ` count 1 at C3. NEGATIVE CONTROL, in
     a disposable worktree: flip ONE byte in the FIRST appended paragraph and
     ONE in the LAST, at offsets you name, and confirm both readers reject each
     mutant while both accept the true file. Remove the worktree; `git worktree
     list` back to one line.
 G6  LEDGER INTEGRITY, base versus C2. Report for both points: the count of
     lines matching `^- R-\d+ — `, whether they are all DISTINCT, the MAXIMUM
     id, the count of `^Done: R-`, of `^Landed: `, and of `^Gate: R` with its
     distinct keys. Report the ids ADDED and REMOVED as sets. At base the
     reviewer measured 230 records, all distinct, maximum `R-0669`, 0 and 0 for
     Done and Landed, and 6 `Gate:` lines with 6 distinct keys. This round is
     EXPECTED to add exactly `R-0670` and exactly `Gate: R6`; report what you
     measure. `^## Steps$` occurs exactly once at C2 and the map text is
     UNCHANGED this round — report the map paragraph byte-identical at base and
     at C2.
 G7  TYPECHECK: `npm run typecheck` from `apps/ui` at C4, exit 0. The reviewer
     ran it at the round base in the primary checkout and measured exit 0 with
     no output. Run it in the PRIMARY checkout — a fresh worktree has no
     `node_modules` and `tsc` cannot be pointed at another root the way vitest
     can (R-0518).
 G8  VITEST: `npm run test:unit` from `apps/ui` at C4, exit 0, with the test-file
     count and the test count. The reviewer measured 16 files and 218 tests at
     the round base; this round ADDS one file, so report the count you measure
     and the difference, and do NOT treat a larger number as a failure. Report
     the node names of the new file's tests.
 G9  RED-PROOFS, in a disposable worktree under `.remedy-wt/` by the route
     constraint 8 names, each reverted before the next. Report which tests fail
     and by what name for each:
     (a) make the denominator fall back to the OTHER unit's limit when the
         matching one is absent — U3's shape (ii) must go red;
     (b) move the warn threshold from 0.85 to 0.95 — U2 must go red;
     (c) drive `estimated` from `basis.cost` for every unit — U4's tokens-unit
         discriminator must go red.
     If any mutation leaves the suite GREEN, say so plainly: it would mean the
     test does not reach the rule, and that is worth more than a green line.
     Before each next mutation the worktree file is restored to be BYTE-EQUAL
     to its committed blob; report that equality, not the act of reverting.
 G10 THE FOUR STATE READERS, serially in the PRIMARY checkout at C4, exit 0:
     `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py` and
     `tests/orchestration/test_integrity_gate.py`. The reviewer measured 544
     passed in total at the round base. Never run two pytest processes at once.
 G11 THE CLIENT-SOURCE CONTRACTS at C4, exit 0: `python3 -m pytest
     tests/ui_contracts/ -q`. The reviewer measured 495 passed and 4 skipped at
     the round base. These read `apps/ui/src` as TEXT, which is why a round
     that adds a client file gates them.
 G12 THE CANARY at C4: `python3 -m pytest tests/cli/test_golden_path.py -q`,
     exit 0. The reviewer measured 42 passed at the round base.
 G13 STRUCTURE, reported for the commits BEFORE C5 and for the range as a whole
     (C5's own numbers belong to the next round's ledger entry, not here):
     every commit single-parent; each commit's INSERTION count, each under the
     500 cap; the range path set against the Change set above with the
     difference reported in BOTH directions; `git show --numstat` agreeing cell
     by cell with the handback's `## Commits` table; lines BEGINNING `<<<SLICE `
     or `<<<END ` counting 0 in every file a slice landed in — count LINES, not
     the substring, because this record quotes those markers inside backticks in
     its own prose; `git ls-files .remedy-wt` 0; one worktree; and the round's
     reflog rows with amend, rebase and cherry counts, each of which must be 0.
 G14 `gh pr list --state open --json number,headRefName`. Report it verbatim.
     Create no PR and merge nothing this round.
 G15 STALENESS. Every sentence C1 through C4 land that states a fact about a
     file is re-measured at C4, and any that has gone stale is reported as a
     residual rather than repaired. Report explicitly that you checked, and name
     any residual. Slices are NEVER edited to fix one.

NOT A GATE: `npm run lint` in `apps/ui`. The reviewer ran it at the round base
and measured exit 1 with 72 problems, so it cannot fail honestly for this round
(R-0364). That is finding R-0622 and it routes to a paydown branch. Do not run
it, do not repair it, and do not report it as green.

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             every mandated section in order, one changed-files table per
             commit, an item-status row per Bundle item, the round base SHA,
             ONE line per gate, and the `Fortschritt:` block above carried
             VERBATIM across all three of its lines. The cap is 100 lines for
             this commit count; declare a DECISION D15 stated cause if the
             mandated content genuinely does not fit.
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF022R7
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
R7 records the R6 verdict, registers R-0670, rules DECISION F022 D4, and lands
T002's LOGIC half: `apps/ui/src/api/costMetric.ts` turns one budget tick into
every render decision the COST metric needs — unit, denominator, fill,
threshold, estimate marker and tooltip — with vitest tests for each.

## Next Steps
1. R8 T002's RENDER half: the COST metric in `TopMetricsBar.tsx`, its CSS
   tokens, the `remedyApi.ts` wiring and the shell seam that feeds it the live
   tick, plus the ui_contracts source guard.
2. R9 T003 the terminal reconciliation and the delta labelling.
3. R10 the integration gate, then closure.

## Risks
- T002 is split across R7 and R8 because its logic half is testable under the
  node-environment vitest and its render half is not testable at all: the
  config collects `src/**/*.test.ts` only, so the component is gated by
  `tests/ui_contracts/` source contracts instead. Splitting keeps each round's
  evidence answerable by its own gates.
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks rather than F022
  defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- R8 is the round that touches the shipped stylesheet, where the design_reference
  sheet defines tokens the shipped one never adopted; grep the shipped CSS, never
  the reference, when a token is claimed to exist (R-0661). There is no warn
  token in the shipped sheet today.
<<<END PLANF022R7

<<<SLICE LEDGER7
- R-0670 — Low, A PRODUCTION COMMENT NAMES A TEST AS THE GUARD FOR A PROPERTY THAT TEST DOES NOT CHECK. Raised by the reviewer at the F022 R6 gate, by mutation rather than by reading, and registered in the same commit as the R6 verdict. The `BUDGET_TICK_EVENT` comment in `packages/orchestration/ui_server.py`, landed at `f685a707`, reads "`tests/ui_contracts/test_humanize_catalog.py` pins that catalog equal to the emitters, so the two spellings cannot drift apart without a red suite." MEASURED in a disposable worktree at `f685a707`, by rewriting that constant's value to `"budget.ticks"` and leaving every other byte alone: `tests/ui_contracts/test_humanize_catalog.py` is EXIT 0 at 9 passed and `tests/ui_server/test_sse_stream.py` is EXIT 0 at 66 passed, while `tests/ui_server/test_budget_tick_envelope.py` is EXIT 1 at 11 failed and 5 passed. The catalog test pins the CATALOG against the EMITTER's inline literal in `packages/orchestration/safe_points.py` and never reads `ui_server.BUDGET_TICK_EVENT` at all, so the guard the sentence names is blind to exactly the drift the sentence promises it catches. The CONCLUSION is true — the suite really does go red — and only the named MECHANISM is wrong, which is why this is Low and not Medium: nothing is unprotected, and the cost is that a reader asking "may I rename this constant" is sent to the one file that would have answered yes. This is the R-0338 class arriving in shipped code rather than in a document, and the counter-measure is the same one: name the guard that was MEASURED to catch it, which here is `tests/ui_server/test_budget_tick_envelope.py`. Searched before minting per §3 checklist item 30 — R-0427 and R-0593 are the neighbouring open entries and both are STALE-claim findings, a sentence that was true when written and went false later, while this sentence was false on the day it landed; no open finding covers it. NOT repaired in R7, whose change set holds no Python path at all: rewriting a landed comment inside an unrelated commit is the move R-0427 records as the wrong one. Route it to the next round that touches `packages/orchestration/ui_server.py` on its own account, which the plan schedules as R9.

Gate: R6 — the F022 R6 entry. R6 PASSED ON EVERY ONE OF ITS FIFTEEN GATES, AND THE REVIEWER RE-RAN EVERY MEASURABLE ONE ITSELF AND ADDED TWO MUTATIONS THE BLOCK NEVER ORDERED. TRANSPORT held under §4.9's DIGEST FALLBACK and the verdict says so: this reviewer did not author the R6 block and has no scratchpad original, so the proof is the recomputation over the COMMITTED artefacts — the C0a blob at `941d9ca9`, the C0b blob at `4076ae3c`, `HEAD:.agent/last_block.md`, `.agent/last_block.md` on disk and `.agent/authored/f022-r6.md` on disk are ALL sha256 `2651351709f1a203152b892fac8db924dcd838b8cdcf36817e40705a976c4c50` over 29555 bytes and 288 lines, agreeing with the digest the handback names. THE EXTRACTION out of the committed blob printed 3 slices over 56 CONTENT lines, so TOTAL re-measures at 288 and PROSE at 232, under DECISION F085 D6's 490 and D5's 400, and constraint 9's numerals reproduce exactly. `.agent/plan.md` at `276c12d2` is byte-equal to PLANF022R6 plus one newline at 2196 bytes against the bare slice's 2195, with the bare-slice control DIFFERING, `^## Goal$` and `^## Next Steps$` once each and 40 lines. BOTH APPENDS HOLD UNDER BOTH READERS: at `675ee3d3` the round-base blob is a byte-exact PREFIX and the remainder is 7618 bytes, exactly one newline plus GATE5's 7616 plus one newline, with an independent blank-line splitter reading 255 units before and 256 after and the last equal to GATE5's own paragraph; at `bd9a745b` the prefix holds and the remainder is 4370, exactly one newline plus DEC3's 4368 plus one newline, with the splitter reading 1270 before and 1278 after, the last unit equal to DEC3's last paragraph, and `## DECISION F022 D3 ` counting 1. THE SETS ARE UNCHANGED WHERE THE ROUND PROMISED: 230 records all DISTINCT at base and at C2, maximum id `R-0669` at both, `^Done: R-` 0, `^Landed: ` 0, ids added and ids removed BOTH the empty set, `^Gate: R` moving 5 to 6 with the distinct keys gaining `Gate: R5`, `^## Steps$` once, and the map paragraph byte-identical at base and at C2 under this reviewer's own extractor. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout, every one matching the figure the block referenced: `ruff check` over the two authored Python paths with the repository's own configuration exit 0 at "All checks passed!", the new `tests/ui_server/test_budget_tick_envelope.py` exit 0 at 16 passed, `test_sse_stream.py` 66, `test_command_channel.py` 100, `tests/orchestration/test_budget_tick.py` 10, `tests/ui_contracts/test_humanize_catalog.py` 9, `test_safe_points.py` 78, the four state readers 455 plus 52 plus 21 plus 16 for 544 against the block's round-base 528 — a difference of exactly the 16 tests C4 adds — and the canary `tests/cli/test_golden_path.py` 42. THE MUTATIONS ARE THE HEART OF THIS VERDICT, and all four ran in a disposable worktree at `f685a707` with the primary checkout never touched. Making the widening UNCONDITIONAL reproduces the round's own colours exactly: `test_sse_stream.py` 3 failed and 63 passed, the failures being `TestFrameShape::test_the_envelope_carries_the_safe_fields_only` and both `TestFramingGolden` tests, while `test_command_channel.py` stays GREEN at 100 passed. THAT SECOND HALF IS THE ROUND'S G8 "PARTIAL" AND THE WORKER WAS RIGHT TO DECLARE IT: only ONE of the two files guards the conditionality, the block's rationale holds for the key-set pin and the golden alone, and `test_command_channel.py` is a suite the change must not break rather than one that would catch an unconditional widening. The worker reported the weaker truth where a green line was available, which is the conduct the gate's own "say so plainly" clause exists to reward. Replacing the key-by-key copy with a wholesale pass-through gives 3 failed and 13 passed with T3 and T4 BOTH among the failures, as ordered. THE REVIEWER THEN ADDED TWO MUTATIONS NOBODY ORDERED. First, `metadata[field]` for `field in metadata` replaced by `metadata.get(field, 0)` across the whole whitelist, so an absent limit arrives as a fabricated zero: 3 failed and 13 passed with BOTH `TestAnAbsentLimitStaysAbsent` tests among them — the feature's money-honesty criterion is pinned by a test and not only by a docstring. Second, `unmeasured_calls` deleted from `BUDGET_TICK_SUMMARY_FIELDS`, standing for a future round adding a figure to D1's payload that nobody adds here: 7 failed and 9 passed, `TestTheWhitelistCoversTheEmitter::test_every_key_the_emitter_writes_is_named_by_a_whitelist` among them. That class is the one the block never ordered and the worker wrote anyway, and it is the difference between a whitelist and a whitelist that stays correct. THE TEST FILE CARRIES ITS DISCRIMINATORS THROUGHOUT: T3 and T4 assert the secret is really IN the metadata before asserting it is absent from the wire, T4 additionally pins that the NAMED basis keys survived so it cannot pass by the nested object being dropped whole, T7 asserts the tick's figures are in what the two transports compared so it cannot pass by both dropping them together, and the emitter guard proves its payload is populated before asserting a subset. THE PRODUCTION DIFF IS WHAT THE BLOCK ORDERED AND NOTHING MORE: one constant, two whitelists, one helper and one conditional branch, with `_safe_event_summary`'s five existing fields unchanged in name and in value. STRUCTURE HELD: seven commits over `9b854cf5`..`d97cdbb2`, every one single-parent, insertions 288, 182, 13, 2, 16, 346 and 42, each under the 500 cap; the range path set is exactly the block's declared eight-path Change set with the difference EMPTY in both directions; lines BEGINNING `<<<SLICE ` or `<<<END ` count 0 in all three slice targets while the substring occurs 14 times in `.agent/live_review.md`, every one backticked prose; `git ls-files .remedy-wt` 0; one worktree; `git status --porcelain` empty; 0 amend, 0 rebase and 0 cherry. THE HANDBACK IS COMPLIANT at 96 lines against the 100 the seven-commit case allows, and the R-0586 scan over both appended slices reads 0 unquoted `HEAD`. ONE FINDING IS REGISTERED IN THIS SAME COMMIT, R-0670: the `BUDGET_TICK_EVENT` comment names `tests/ui_contracts/test_humanize_catalog.py` as the guard against a spelling drift that test is measurably blind to. It is Low, it is the reviewer's own catch, and it does not touch the verdict. THE VERDICT IS PASS: every numeral R6 states reproduced under the reviewer's own measurement, four mutations went red including two nobody ordered, the one gate reported PARTIAL was reported honestly and reproduces exactly as declared, no id moved, and T001 closes with the tick's figures reaching a client for the first time.
<<<END LEDGER7

<<<SLICE DEC4
## DECISION F022 D4 (2026-08-23) — the client's cost reading: one denominator, one estimate marker, two thresholds, and no arithmetic beyond the ratio

CONTEXT, measured by the reviewer at `d97cdbb2`. DECISION F022 D1 ruled the tick's payload, D2 its writer and D3 its passage across the envelope. The figures now reach a client that has no vocabulary for them: `RemedyMetricKey` at `apps/ui/src/api/types.ts:3` is a closed union of seven strings and `RemedyMetric.value` is `number | "—"`, with `suffix` a display string, `tooltip` a `Record<string, number>`, `state` a three-value union and `unknown` a boolean — nowhere for a limit, a basis or a threshold. The feature file's Design and its Goal & Done also disagree on the surface: Design rules the fill against "the strongest configured limit (usd preferred when both)" while Done requires "the warn threshold triggers per tokens". Both are satisfiable at once, and this decision says how, so that no round has to guess.

CHOSEN (1), THE UNIT IS CHOSEN BY WHICH LIMIT EXISTS, USD FIRST. When `limit_usd` and `spent_usd` are both present the metric is in usd; otherwise when `limit_tokens` and `spent_tokens` are both present it is in tokens; otherwise there is no usable denominator and clause 3 applies. That is Design's "usd preferred when both" read as a statement about the LIMITS, and it satisfies Done's "warn threshold triggers per tokens" exactly, because a job configured with a token limit alone lands in the tokens unit and takes its threshold from the token fill. The denominator is ALWAYS the limit of the unit shown: the other unit's limit is never substituted, because a dollar spend over a token limit is a fabricated ratio wearing a real number's clothes.

CHOSEN (2), THE ESTIMATE MARKER READS THE BASIS OF THE FIGURE ACTUALLY SHOWN. A usd metric reads `basis.cost`, a tokens metric reads `basis.tokens`, and `estimated` is false ONLY for the exact string `"actual"`. `"lower_bound"`, `"absent"`, any unrecognised string and a missing or non-object `basis` all mark the figure estimated, because unknown provenance is not an actual and the `~` is cheap while a false claim of exactness is not. The tooltip text is composed in the client from that vocabulary; DECISION F022 D1 clause four already forbids a display sentence on the wire, and this decision does not reopen it.

CHOSEN (3), NO LIMIT MEANS NO DENOMINATOR ANYWHERE. A missing limit, a limit that is not a finite number, and a limit of zero all produce the spent-only variant: `fill` null, `level` null, `limitless` true, and no tooltip line naming a limit. A zero limit is included deliberately — it is the shape that would otherwise divide by zero and render `Infinity` as a fill — and the acceptance criterion is that a limitless job never renders a fabricated denominator, which is a statement about what the user SEES and therefore binds the tooltip as much as the bar.

CHOSEN (4), THE THRESHOLDS ARE ON THE RATIO AND THEY ARE TWO. `fill >= 1` is `"exceeded"`, `fill >= 0.85` is `"warn"`, anything less is `"normal"`, and `level` is null whenever `fill` is. The comparisons are inclusive at both boundaries so that exactly 85% warns and exactly 100% is exceeded; a bar that waited for 85.1% would tell the truth late, and the budget stop the feature file mentions lands moments after 100% either way.

CHOSEN (5), THE ONLY ARITHMETIC IS THE RATIO AND ONE PERCENTAGE OF IT. `costMetricOf` divides spend by limit and multiplies that ratio by 100 for the tooltip's percentage, and does nothing else numeric. It never sums figures, never converts tokens to money, never applies a rate and never carries a price constant — the backend is the single arithmetic home and this is the whole of the client's share. The permitted numeric literals are therefore `0`, `1`, `100`, `0.85`, and the formatting constants `2`, `1000` and `1000000`; the test file's source guard enumerates exactly those.

ALTERNATIVES CONSIDERED. Compute the render decisions inside `TopMetricsBar.tsx`: rejected — the vitest config collects `src/**/*.test.ts` under a node environment, so a rule that lived in the component would ship with no test that can reach it, and F021 already established the pure-module shape for exactly this reason. Show the TIGHTEST fill across both limits rather than preferring usd: rejected, because "tightest" changes unit mid-run as spending moves and a metric whose unit flickers is worse than one that is merely conservative; the tooltip enumerates both fills, so nothing is hidden. Let an absent limit fall back to the other unit's limit: rejected under clause 1. Emit the composed tooltip strings from the backend: rejected, it reopens D1 clause four and puts display copy in the ledger.

REVERSE IT by deleting `apps/ui/src/api/costMetric.ts` with its test file and narrowing `RemedyMetricKey` back to seven strings; nothing else reads either. Clauses 1 to 4 are independent of each other and any one can be re-ruled alone, while clause 5 is a consequence of the no-client-arithmetic rule the feature file's Acceptance section already binds and cannot be reversed here.
<<<END DEC4
