── STEP T002b/3 — F022 Live cost ticker · Runde 8 ────────────────────────────

Fortschritt: ~55 % (T001 fertig · T002 fertig nach dieser Runde · T003 offen;
             der COST-Wert wird ab hier wirklich gezeichnet, mit Fuellung,
             Schwelle und Schaetzmarke) — Schaetzung

Goal:        Record the R7 verdict, resolve R-0653, register R-0671 and R-0672,
             rule the render as DECISION F022 D5, and close T002: the COST
             metric draws — coin glyph, formatted value, estimate marker, fill
             track and threshold treatment — pinned by goldens and a source
             contract.

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the plan ·
             C2 the R7 verdict, one resolution and two findings · C3 DECISION
             F022 D5 · C4 the fixture-stream goldens · C5 the render and its
             source contract · C6 the handback.

Change:      Exactly these paths, nothing else:
               .agent/authored/f022-r8.md        (C0a)
               .agent/last_block.md              (C0b)
               .agent/plan.md                    (C1)
               .agent/live_review.md             (C2)
               .agent/decisions.md               (C3)
               apps/ui/src/api/costMetric.test.ts                    (C4)
               apps/ui/src/components/icons/RemedyGlyphs.tsx         (C5)
               apps/ui/src/components/metrics/TopMetricsBar.tsx      (C5)
               apps/ui/src/components/metrics/TopMetricsBar.module.css (C5)
               tests/ui_contracts/test_cost_metric_render.py         (C5, new file)
               .agent/handoff.md                 (C6)

─── Slice convention ──────────────────────────────────────────────────────────
Each authored text below begins at its `<<<SLICE <name>` line and ends at its
`<<<END <name>` line; neither marker line is part of the slice, and no slice
contains a marker line. Extract them PROGRAMMATICALLY by marker line out of the
committed C0a blob — never retype, never rewrap, never reflow. The slices are
PLANF022R8, LEDGER8 and DEC5.

Constraints:
 1. NEVER edit a slice. Apply it byte for byte. If a slice contradicts a fact
    you measure, apply it anyway and DECLARE the contradiction in the handback
    under Deviations. Repair nothing outside your slices; rule on nothing.
 2. C1 is the FIRST substantive commit (§3 checklist item 23): this round
    touches the finding ledger, so the plan advances before anything else but
    the two block-save commits.
 3. `.agent/plan.md` is a WHOLE-TEXT replacement. LEDGER8 and DEC5 are APPENDS
    to append-only records: never rewrite a landed paragraph in either file,
    and add nothing to them beyond the slice. This block carries NO FROM/TO
    pair.
 4. LEDGER8 holds, in this order and each separated by ONE blank line: the
    `Done: R-0653` resolution, the `R-0671` record, the `R-0672` record, and
    the `Gate: R7` paragraph. It lands in ONE commit, C2. The gate paragraph
    states that the resolution and the findings are written in that same
    commit; THIS constraint is what makes that true (§3 checklist item 20,
    R-0524 carve-out), so C2 carries every one of those paragraphs or none.
 5. `apps/ui/src/api/costMetric.ts` IS NOT IN THE CHANGE SET. R7's module is
    correct and this round consumes it; if the render seems to want a new field
    on `CostMetricView`, that is a sign the render is deciding something the
    module should decide, and it is a finding for the handback rather than an
    edit. C4 adds tests to `costMetric.test.ts` and changes no production byte.
 6. NO WIRING this round. `apps/ui/src/api/remedyApi.ts` and
    `apps/ui/src/components/shell/RemedyShell.tsx` are OUT of the change set:
    feeding the live tick into a `RemedyMetric[]` is T003's end-to-end work,
    and the feature file scopes T002 to "the COST metric component on fixture
    streams". Do not touch budget enforcement, the pricing and basis rules, the
    emission, the envelope, or MetricsBar's other metrics — the other seven
    metrics' rendered output is byte-identical to what it was, and C5's own
    contract test is where you prove it.
 7. Destructive verification runs ONLY inside a disposable worktree under
    `.remedy-wt/`. The primary checkout satisfies `git status --porcelain`
    empty at every commit and at the handback. A fresh worktree has no
    `apps/ui/node_modules`, so drive vitest at one from the PRIMARY install:
    `npx vitest run --root <worktree>/apps/ui --config <primary>/apps/ui/vitest.config.ts`
    run from the primary `apps/ui`. Scope that run to the ONE test file you are
    proving; an unscoped worktree run also loads
    `src/components/prompt/promptTraceLens.test.ts`, which fails to resolve
    under `--root` and is a worktree artifact rather than a result. `pytest`
    needs no such route and runs in the worktree directly.
 8. Every numeral this block states about the ROUND BASE `142af5e4` was
    measured by the reviewer at that commit and is a REFERENCE to report
    against, not a target to reproduce. Where your measurement differs, report
    BOTH and reconcile NOTHING.
 9. THE TOKENS NAMED BELOW WERE ALL RESOLVED IN THE SHIPPED SHEET, not in the
    reference: `--remedy-blue-100`, `--remedy-orange-400`, `--remedy-red-500`,
    `--remedy-line`, `--remedy-muted`, `--remedy-faint` and
    `--remedy-ink-strong` each have exactly one definition in
    `apps/ui/src/styles/tokens.css` and one in
    `docs/ui/design_reference/tokens.css`, measured at the round base. Use no
    token this list does not name and no literal hex in a new rule.
10. Size, measured by the reviewer on the final bytes of this block and stated
    once here: this block is 382 lines TOTAL with 69 CONTENT lines inside its
    slices, so PROSE is 313 — under DECISION F085 D6's 490 and D5's 400.

─── What R8 builds ────────────────────────────────────────────────────────────

R7 decided everything the COST metric shows and drew none of it. `CostMetricView`
carries `display`, `unit`, `estimated`, `fill`, `level`, `limitless` and
`tooltip`, and no component reads any of them yet. This round is the render, and
it adds NO rule: every branch below is a field lookup, and where the render is
tempted to compute, constraint 5 says that is a finding.

`TopMetricsBar.tsx` is generic over the array it is handed and falls back to
`ChartGlyph` for an unknown key, so an eighth metric renders today rather than
crashing — measured at the round base. What it cannot do today is show a
formatted string, a prefix, a limit-relative fill or a threshold, and those four
are the whole of this round's visible change.

DECISION F022 D5 below rules the render. Read it as the specification; the prose
here does not repeat it.

─── The goldens (C4) ──────────────────────────────────────────────────────────

`apps/ui/src/api/costMetric.test.ts` gains ONE describe block and nothing else —
no existing test is edited. The Acceptance section requires "goldens per
threshold and basis", so:

 GO1 A FIXTURE TICK STREAM, declared as an ordered array of payloads exactly as
     they arrive on the envelope, walking one job from its first tick to over
     its limit — normal, then warn, then exceeded — with a basis that CHANGES
     mid-stream from `lower_bound` to `actual`, plus a limitless job's tick.
 GO2 A FROZEN GOLDEN TABLE, one entry per fixture, each the whole serialised
     `CostMetricView`. Assert deep equality per entry. Write the goldens out by
     hand; a table generated from the module agrees with whatever the module
     does and pins nothing.
 GO3 A COVERAGE ASSERTION over the table itself, so it cannot silently lose a
     state: every one of `"normal"`, `"warn"` and `"exceeded"` appears as a
     `level`, `null` appears as a `level`, and `estimated` takes both `true` and
     `false`. Fail with the missing state named.

─── The render (C5) ───────────────────────────────────────────────────────────

`RemedyGlyphs.tsx` gains `CoinGlyph`, written in the exact idiom of the file's
neighbours — `viewBox="0 0 16 16"`, `fill="none"`, `stroke="currentColor"`,
`strokeWidth="1.4"`, `strokeLinecap="round"` — drawing what
`docs/ui/design_reference/assets_spec.md` line 179 already specifies for the
budget/cost entry: a coin, circle plus an inner cent-bar. This is CONFORMANCE
rather than a new asset: the glyph is named by the asset authority already, so
`assets_spec.md` needs no amendment and none is in the change set.

`TopMetricsBar.tsx` gains, and nothing more:
  - `cost: CoinGlyph` in `iconByKey`;
  - a `cost` arm in `mainValue` returning `m.cost.display`, or the em dash when
    `m.cost` is absent — the component formats nothing itself;
  - the estimate marker: a `~` in its own span, rendered when and only when
    `m.cost.estimated` is true, before the value;
  - the fill track, rendered when and only when `m.cost.fill` is not null, with
    the level class from `m.cost.level`;
  - the tooltip: when `m.cost` is present its `tooltip` array renders as plain
    rows. The existing `m.tooltip` branch is UNTOUCHED and keeps its
    `data-testid="token-tooltip"`; the cost rows get their own testid. The
    `tabIndex` and the hover and focus handlers currently gate on `m.tooltip`
    and must also open for a cost metric, or the tooltip is mouse-only;
  - the accessible name: for a cost metric the `aria-label` names the estimate
    in words when `estimated`, and names the level in words at `"warn"` and at
    `"exceeded"`. That is not decoration — see DECISION F022 D5 clause 3.

`TopMetricsBar.module.css` gains the cost rules and edits none of the existing
ones. The track follows `docs/ui/design_reference/ux_spec.md` §10's own
specification — 6px high, radius 3, `--remedy-blue-100` as the base, a 350ms
width transition — and NOT the neighbouring `.progressTrack`, whose 5px, rgba
base and 600ms predate that spec; leave `.progressTrack` exactly as it is and
say in the handback that the two now differ and why.

`tests/ui_contracts/test_cost_metric_render.py`, new, in the conventions of
`tests/ui_contracts/test_remedy_shell_stream.py` — a comment stripper with its
own self-test FIRST, then every assertion over COMMENT-STRIPPED source (R-0584).
Required:
 P1  The stripper self-test: it removes a comment the component really carries.
 P2  `CoinGlyph` is defined in `RemedyGlyphs.tsx` and imported and mapped to
     `cost` in `TopMetricsBar.tsx`.
 P3  THE MARKER IS THE BASIS, NOT THE THRESHOLD: the `~` renders off
     `estimated`. Assert that the `~` and the level names do not occur in one
     expression — a `~` driven by `warn` would be a false honesty marker, which
     is worse than none.
 P4  NO FAKE DENOMINATOR AT THE RENDER LAYER: the track is guarded on the fill
     being non-null, and the source names no default, no `?? 0` and no `|| 0`
     on `fill`.
 P5  NEVER COLOUR-ONLY: for both `warn` and `exceeded` the component's source
     puts the level into the accessible name, and the stylesheet gives each a
     non-colour signal as well. Assert both halves.
 P6  THE COMPONENT DOES NO ARITHMETIC BUT THE CLAMP: over the comment-stripped
     `.tsx`, the only `/` outside a JSX closing tag or a string is none, and
     the only numeric literals in the cost branch are the clamp's `0` and `100`.
 P7  THE OTHER SEVEN ARE UNTOUCHED: the seven existing `iconByKey` entries are
     all still named, `data-testid="token-tooltip"` still occurs, the `tokens`
     "estimated" caption still renders off `isTokens`, and `.progressTrack`
     still renders off `m.key === "progress"`.
 P8  THE STYLESHEET USES NAMED TOKENS: the new rules reference
     `--remedy-orange-400` and `--remedy-red-500`, and the cost rules carry no
     literal hex value.

─── Done when ─────────────────────────────────────────────────────────────────

Run every gate below yourself, record its REAL exit code, and put ONE LINE per
gate in the handback with the transcripts kept out of it (R-0582). G1 through
G14 run after C5 and BEFORE C6, so the handback can quote all of them (§3
checklist item 31). The round base is `142af5e4` throughout.

 G1  `.agent/STOP` absent, read from disk before C0a and again before C6.
     Branch `feature/f022-live-cost-ticker`. `git status --porcelain` 0 lines
     after every one of C0a, C0b, C1, C2, C3, C4 and C5.
 G2  TRANSPORT. sha256 over the block file the reviewer wrote at
     `.remedy-wt/f022-r8.md`, over the committed C0a blob, over the committed
     C0b blob and over `.agent/last_block.md` on disk: report all four digests,
     byte counts and line counts, and require them EQUAL. The digest the
     delegation names is the fifth reading and must agree.
 G3  EXTRACTION. Run an extractor over the COMMITTED C0a blob that finds the
     slices by their marker LINES and report how many slices and how many
     CONTENT lines it printed, plus the block's TOTAL and PROSE line counts.
     Report those against constraint 10's numerals; reconcile nothing.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF022R8 plus exactly one
     newline. NEGATIVE CONTROL: the same comparison against the BARE slice must
     be FALSE, and report both byte counts. `^## Goal$` once, `^## Next Steps$`
     once, `wc -l` at most 50.
 G5  APPEND at C2 and again at C3, each proved twice. The round-base blob is a
     byte-exact PREFIX of the committed file, and the remainder is exactly one
     newline plus the slice plus one newline — report the remainder's byte
     count and the slice's. Then an INDEPENDENT reader: split both files on
     blank lines, report the unit counts before and after, and require the
     appended units to equal the slice's own paragraphs IN ORDER — for C2 that
     means EVERY paragraph of LEDGER8 is checked, not only the last (R-0578).
     Lines beginning `## DECISION F022 D5 ` count 1 at C3. NEGATIVE CONTROL, in
     a disposable worktree: flip ONE byte in the FIRST appended paragraph and
     ONE in the LAST, at offsets you name, and confirm both readers reject each
     mutant while both accept the true file. Remove the worktree; `git worktree
     list` back to one line.
 G6  LEDGER INTEGRITY, base versus C2. Report for both points: the count of
     lines matching `^- R-\d+ — `, whether they are all DISTINCT, the MAXIMUM
     id, the count of `^Done: R-` with its distinct ids, of `^Landed: `, and of
     `^Gate: R` with its distinct keys. Report the ids ADDED and REMOVED as
     sets. At base the reviewer measured 231 records, all distinct, maximum
     `R-0670`, 0 `Done:`, 0 `Landed:`, and 7 `Gate:` lines with 7 distinct
     keys. This round is EXPECTED to add `R-0671` and `R-0672`, to take
     `^Done: R-` to 1 for `R-0653`, and to add `Gate: R7`; report what you
     measure. `R-0653` must still occur exactly once as a `^- R-0653 — ` record
     — a resolution APPENDS and never rewrites the finding it resolves.
     `^## Steps$` occurs exactly once at C2 and the map text is UNCHANGED —
     report the map paragraph byte-identical at base and at C2.
 G7  TYPECHECK: `npm run typecheck` from `apps/ui` at C5, exit 0, in the PRIMARY
     checkout. The reviewer measured exit 0 with no output at the round base.
 G8  VITEST: `npm run test:unit` from `apps/ui` at C5, exit 0, with the
     test-file count and the test count. The reviewer measured 17 files and 235
     tests at the round base; C4 adds tests to an EXISTING file, so the file
     count is expected to hold while the test count rises. Report both and the
     difference; do NOT treat a larger test count as a failure.
 G9  RED-PROOFS, each reverted before the next, and report which tests fail and
     by what name for each. (a) and (b) mutate the `.tsx` and are proved with
     `python3 -m pytest tests/ui_contracts/test_cost_metric_render.py -q` INSIDE
     a disposable worktree, which needs no node_modules; (c) mutates the test
     data and is proved with the scoped vitest run constraint 7 names.
     (a) render the fill track unconditionally, dropping the non-null guard —
         P4 must go red;
     (b) drive the `~` from `level === "warn"` instead of from `estimated` —
         P3 must go red;
     (c) change ONE figure in ONE golden entry — GO2 must go red and name that
         entry.
     If any mutation leaves the suite GREEN, say so plainly: it would mean the
     test does not reach the rule, and that is worth more than a green line.
     Before each next mutation the worktree file is restored to be BYTE-EQUAL
     to its committed blob; report that equality, not the act of reverting.
 G10 THE FOUR STATE READERS, serially in the PRIMARY checkout at C5, exit 0:
     `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py` and
     `tests/orchestration/test_integrity_gate.py`. The reviewer measured 544
     passed in total at the round base. Never run two pytest processes at once.
 G11 THE CLIENT-SOURCE CONTRACTS at C5, exit 0: `python3 -m pytest
     tests/ui_contracts/ -q`. The reviewer measured 495 passed and 4 skipped at
     the round base; C5 adds a file, so report the count you measure and the
     difference. These read `apps/ui/src` as TEXT, and two of them sweep EVERY
     `.ts` and `.tsx` under it — `test_there_is_still_exactly_one_subscription`
     forbids `EventSource` outside `brainStreamDeps.ts` and pins
     `useBrainStream(` at 2 sites, and `test_no_scanlines_in_frontend` forbids
     the string `scanline`.
 G12 THE CANARY at C5: `python3 -m pytest tests/cli/test_golden_path.py -q`,
     exit 0. The reviewer measured 42 passed at the round base.
 G13 STRUCTURE, reported for the commits BEFORE C6 and for the range as a whole
     (C6's own numbers belong to the next round's ledger entry, not here):
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
 G15 STALENESS. Every sentence C1 through C5 land that states a fact about a
     file is re-measured at C5, and any that has gone stale is reported as a
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

<<<SLICE PLANF022R8
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
R8 records the R7 verdict, resolves R-0653, registers R-0671 and R-0672, rules
DECISION F022 D5, and closes T002 with the RENDER half: the coin glyph, the
formatted value, the estimate marker, the fill track and the threshold
treatment, pinned by fixture-stream goldens and a source contract.

## Next Steps
1. R9 T003 the terminal reconciliation, the delta labelling, the live wiring
   through `remedyApi.ts` and `RemedyShell.tsx`, and the fake-job end-to-end.
2. R10 the integration gate.
3. R11 closure.

## Risks
- T002 was split across R7 and R8 because its logic half is testable under the
  node-environment vitest and its render half is not: the config collects
  `src/**/*.test.ts` only, so the component is gated by a `tests/ui_contracts/`
  source contract instead. The live WIRING moved to R9 with T003, where the
  feature file already puts the end-to-end.
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks rather than F022
  defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- R-0665 is open and this feature needs its route: every UI feature is told to
  record visual deviations in an `assumption_log` that does not exist. F022
  records them as DECISIONs in `.agent/decisions.md` and says so, which is a
  route rather than a fix.
<<<END PLANF022R8

<<<SLICE LEDGER8
Done: R-0653 — RESOLVED BY MEASUREMENT AT THE F022 R7 GATE: the vitest red control IS runnable inside a disposable worktree, and the route the finding could not find is to resolve the RUNNER from the primary install while resolving the SOURCES from the worktree. R-0653 recorded that `npm run test:unit -- --root <worktree>` dies at startup with `ERR_MODULE_NOT_FOUND: Cannot find package 'vitest'` because the config's own import cannot resolve there, and that the `ln -s` which would supply `node_modules` is denied — a correct measurement of the command it tried. The working form is `npx vitest run <one test file> --root <worktree>/apps/ui --config <primary>/apps/ui/vitest.config.ts` executed with the working directory inside the PRIMARY `apps/ui`: npx and the config both resolve against the primary install, `--root` points the collector at the worktree's sources, and nothing is written to the primary checkout, so guardrail G5 holds. Measured by the reviewer at `8e34539b` in `.remedy-wt/r7review`, unmutated baseline 17 passed, then three mutations of `apps/ui/src/api/costMetric.ts`: borrowing the other unit's limit as a denominator gives 3 failed and 14 passed; moving the warn threshold from 0.85 to 0.95 gives 2 failed and 15 passed; driving the estimate marker off `basis.cost` for every unit gives 1 failed and 16 passed, the one failure being exactly the tokens-unit discriminator written to catch it. The worker had independently found the same route and reported the same three colours, so the reading is two-party. ONE CAVEAT IS PART OF THE RESOLUTION, not a residual: an UNSCOPED worktree run also collects `src/components/prompt/promptTraceLens.test.ts`, which fails to resolve under `--root` and is a worktree artifact rather than a result — scope the run to the file under proof, which is what a red control wants anyway. R-0653's compensating-control paragraph stands and is now redundant rather than load-bearing: the behavioural half has been shown to fail, so the vitest suite is no longer gated green-only.

- R-0671 — Low, THE ONE HONESTY RULE THE COST MODULE STATES AND NO TEST PINS: A NEGATIVE FIGURE IS DOCUMENTED AS ABSENT AND NOTHING WOULD CATCH IT BEING RENDERED. Raised by the reviewer at the F022 R7 gate by a mutation the block never ordered. `usableFigure` in `apps/ui/src/api/costMetric.ts` at `8e34539b` reads `typeof value === "number" && Number.isFinite(value) && value >= 0` under a comment that rules "a string, a NaN, an infinity and a negative are treated as ABSENT rather than coerced: a fabricated number is worse than a missing one". MEASURED in `.remedy-wt/r7review` by deleting the `&& value >= 0` clause and leaving every other byte alone: the whole file stays GREEN at 17 passed. The consequence is not abstract — under that mutant `costMetricOf({spent_usd: -1, limit_usd: 4, basis: {cost: "actual"}})` returns `display` `"$-1.00"`, `fill` `-0.25`, `level` `"normal"`, `limitless` `false` and a tooltip line reading `Cost $-1.00 of $4.00 (-25%)`, where the true module returns `display` `"—"`, `fill` null and `limitless` true. U6's `broken` list CONTAINS `{ spent_usd: -1, limit_usd: 4 }`, so the case reads on the page as covered, and its assertions are that nothing throws, that `display` is a string and that `unit` is one of two strings — every one of which the mutant satisfies. That is the R-0584 shape moved from comments to test data: a case enumerated is not a case asserted, and the guard-test discriminator rule this repository already applies to Python guards was not applied to this one. The NaN and infinity arms stay guarded by `Number.isFinite` under the same mutation, so this finding is scoped to the negative arm alone. Low, because the shipped module is CORRECT and only its proof is missing; the fix is one assertion pinning the limitless view for a negative spend, and it belongs to the next round that touches that test file.

- R-0672 — Low, A LANDED DECISION'S REVERSAL INSTRUCTION DOES NOT BUILD, BECAUSE IT NAMES TWO OF THE THREE THINGS ITS OWN ROUND ADDED. Raised by the reviewer at the F022 R7 gate; the WORKER had already declared the same defect as a constraint-1 contradiction before the reviewer read the diff, and applied the slice byte for byte as it was required to. DECISION F022 D4's closing paragraph, committed at `c6b026bf`, reads "REVERSE IT by deleting `apps/ui/src/api/costMetric.ts` with its test file and narrowing `RemedyMetricKey` back to seven strings; nothing else reads either." Measured at `8e34539b`: C4 of that round also added the optional field `cost?: CostMetricView` to `RemedyMetric` and, to type it, the line `import type { CostMetricView } from "./costMetric";` at the top of `apps/ui/src/api/types.ts`. Following the instruction literally therefore deletes the module while leaving an import of it standing, and `npm run typecheck` goes red on a path that no longer exists — so a reversal performed exactly as written does not build, and the clause "nothing else reads either" is false of `types.ts`, which is the one other file that round touched. The defect is the REVIEWER's: the slice was authored before the change set it describes had landed, and the reversal was written from the two files that were most in mind rather than from the round's own three-path Change set. This is the R-0526 class — a slice asserting a universal over its own round — arriving in the clause that matters most, because a DECISION's reversal instruction is the one part of it a later reader executes rather than reads. Low, because the omission is discovered by the first `tsc` run and the correct reversal is obvious once seen. NOT repaired by rewriting the landed paragraph, which §3 checklist item 20 forbids: the correction is an appended clause in the next DECISION that touches this ground, and DECISION F022 D5 of this same block carries it.

Gate: R7 — the F022 R7 entry. R7 PASSED ON EVERY ONE OF ITS FIFTEEN GATES, AND THE REVIEWER RE-RAN EVERY ONE OF THEM ITSELF AND ADDED THREE MUTATIONS THE BLOCK NEVER ORDERED. This resolution, both findings above and this paragraph are written in ONE commit, which the block's constraint 4 fixes. TRANSPORT HELD IN ITS STRONGEST FORM: the reviewer authored this round's block, so §4.9's primary comparison against the reviewer's own original was available and was used rather than the digest fallback — `.remedy-wt/f022-r7.md`, the committed C0a blob at `1be0fff5`, the committed C0b blob at `77e3a0ad`, `.agent/last_block.md` on disk and `.agent/authored/f022-r7.md` on disk are ALL sha256 `2ca2930d614185ef4b32f1db7c1885cc5f8793340cafac51be75c2d84377d831` over 36027 bytes and 362 lines, and C0a and C0b are the SAME git blob. THE EXTRACTION out of the committed blob printed 3 slices over 64 CONTENT lines, so TOTAL re-measures at 362 and PROSE at 298, under DECISION F085 D6's 490 and D5's 400, and constraint 11's numerals reproduce exactly. `.agent/plan.md` at `a6ec63ab` is byte-equal to PLANF022R7 plus one newline at 2418 bytes against the bare slice's 2417, with the bare-slice control DIFFERING, `^## Goal$` and `^## Next Steps$` once each and 44 lines. BOTH APPENDS HOLD UNDER BOTH READERS: at `fd530b7c` the round-base blob is a byte-exact PREFIX and the remainder is 8875 bytes, exactly one newline plus LEDGER7's 8873 plus one newline, with an independent blank-line splitter reading 256 units before and 258 after; at `c6b026bf` the prefix holds and the remainder is 5128, exactly one newline plus DEC4's 5126 plus one newline, the splitter reading 1278 before and 1287 after, and `## DECISION F022 D4 ` counting 1. THE SETS MOVED EXACTLY WHERE THE ROUND PROMISED AND NOWHERE ELSE: 230 records at base and 231 at C2, all DISTINCT at both, maximum id `R-0669` to `R-0670`, `^Done: R-` 0 and `^Landed: ` 0 at both, `^Gate: R` 6 to 7 with the distinct keys gaining `Gate: R6`, ids ADDED exactly `{R-0670}` and ids REMOVED the EMPTY SET, `^## Steps$` once, and the map paragraph byte-identical at base and at C2 under the reviewer's own extractor. THE SUITES ARE THE REVIEWER'S OWN, run in the primary checkout, every one matching the figure the block referenced: `npm run typecheck` exit 0 with no output; `npm run test:unit` exit 0 at 17 files and 235 tests against the base's 16 and 218, the difference being exactly the one file and seventeen tests C4 adds; `tests/ui_server/` 455, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21 and `tests/orchestration/test_integrity_gate.py` 16 for 544; `tests/ui_contracts/` 495 passed and 4 skipped; and the canary `tests/cli/test_golden_path.py` 42. THE MUTATIONS ARE THE HEART OF THIS VERDICT, and all six ran in `.remedy-wt/r7review` at `8e34539b` with the primary checkout never touched. All three ordered red-proofs reproduced the worker's colours exactly: borrowing the other unit's limit 3 failed and 14 passed, the warn threshold moved to 0.95 2 failed and 15 passed, and the estimate marker driven off `basis.cost` for every unit 1 failed and 16 passed — that last failing exactly U4's tokens-unit discriminator, which is the assertion written to catch precisely it. THE WORKER'S G9(a) "PARTIAL" IS ACCURATE AND REPRODUCES: under the borrowed-denominator mutation U3's first case goes red while U3's SECOND case, the serialised-view assertion, stays green, because the borrowed denominator reaches `fill` while both tooltip lines are guarded separately and stay empty. The worker reported the weaker truth where a whole-describe claim was available. THE REVIEWER THEN ADDED THREE MUTATIONS NOBODY ORDERED, and one of them found something. Accepting a zero limit as a denominator fails U6's division-by-zero case, 1 failed and 16 passed. Pushing a fabricated denominator into the LIMITLESS branch's tooltip fails U3's serialised-view case, 1 failed and 16 passed — so that assertion is live and does the work it was written for, which is what the G9(a) caveat above does not by itself establish. Deleting the `&& value >= 0` clause from `usableFigure` leaves the file GREEN at 17 passed, and that is R-0671 above. THE TESTS CARRY THEIR DISCRIMINATORS: U1 pins the token line as well as the usd line so the enumeration cannot silently collapse, U2 supplies a `spent_usd` with no usd limit so a module preferring the usd FIGURE over the usd PAIR shows the wrong unit, U4 opposes the two basis values, and U7 asserts its own comment stripper removed something and that the unstripped source would have failed — a guard that proves it is not vacuous before it guards. THE PRODUCTION DIFF IS WHAT THE BLOCK ORDERED AND NOTHING MORE: `costMetric.ts` imports nothing, `types.ts` gains one type-only import, one union member and one OPTIONAL field, and the other seven metrics' shape is untouched. STRUCTURE HELD: seven commits over `d97cdbb2`..`142af5e4`, every one single-parent, insertions 362, 240, 18, 4, 18, 432 and 65, each under the 500 cap; the range path set is exactly the block's declared nine-path Change set with the difference EMPTY in both directions; lines BEGINNING `<<<SLICE ` or `<<<END ` count 0 in all three slice targets while the substring occurs 16 times in `.agent/live_review.md`, every one backticked prose; `git ls-files .remedy-wt` 0; one worktree; `git status --porcelain` empty; 0 amend, 0 rebase and 0 cherry. THE HANDBACK IS COMPLIANT at 99 lines against the 100 the seven-commit case allows, with every mandated section present and in order. THE ROUND'S DECLARED DEVIATIONS ARE ALL CORRECT AND TWO OF THEM CORRECT THE REVIEWER: the incomplete REVERSE clause is R-0672 above, the CONTEXT sentence about seven strings is correctly read as a base measurement because DEC4 names `d97cdbb2` in its own opening words, and the dynamic-import assumption is sound — there is no `@types/node` in this workspace, which the reviewer confirmed against `apps/ui/package.json`. THE VERDICT IS PASS: every numeral R7 states reproduced under the reviewer's own measurement, all three ordered mutations went red plus two unordered ones, the gap the sixth found is registered rather than waved through, and T002's logic half lands with the first mutation-proved vitest guard this repository has ever had.
<<<END LEDGER8

<<<SLICE DEC5
## DECISION F022 D5 (2026-08-23) — the COST metric is drawn from the view and decides nothing, and its threshold is never colour alone

CONTEXT, measured by the reviewer at `142af5e4`. DECISION F022 D4 put every render decision into `costMetricOf`, and nothing draws them. `TopMetricsBar.tsx` is generic over the array it is handed, hardcodes no metric list and falls back to `ChartGlyph` for an unknown key, so an eighth metric already renders; what it cannot do is show a formatted string, a prefix, a limit-relative fill or a threshold. Three of this repository's own authorities bear on how it should: `docs/ui/design_reference/ux_spec.md` §10 specifies the metrics bar's track as 6px, radius 3, `--remedy-blue-100` base with a 350ms width transition, `docs/ui/design_reference/assets_spec.md` line 179 already specifies the budget/cost glyph as a coin — circle plus inner cent-bar, stroke, 16 DOM — with a warn tint at or above 85 per cent of budget, and §14 of the same spec rules that a state change is never colour alone.

CHOSEN (1), THE COMPONENT IS A FIELD LOOKUP AND ITS ONLY ARITHMETIC IS THE CLAMP. Every branch reads a field of `CostMetricView`: `display` for the value, `estimated` for the marker, `fill` for the track's width, `level` for its treatment, `tooltip` for the rows. The component formats nothing, chooses no unit, picks no denominator and composes no sentence. The one number it computes is the track's width — an already-computed ratio expressed as a percentage and clamped into the track — because a fill over 100 per cent must render as a full bar rather than overflow its container. Where the render appears to need a value the view does not carry, that is the view's gap and it is a finding, never a computation moved back into the component.

CHOSEN (2), THE EIGHTH SEGMENT IS ADDED AND THE DEVIATION IS RECORDED HERE. `ux_spec.md` §10 opens "One hero glass card; 4 segments" while the shipped bar renders seven, so the built state already departs from that count and this round makes it eight. The departure is deliberate and pre-existing: the four-segment sentence describes an earlier composition, while the same section's binding rules — the divider, the icon disc, the kicker, the 30/700 value, the track, the honest em dash — are followed exactly by every segment including this one. THE ROUTE FOR THIS RECORD IS ITSELF THE POINT: the feature file's header orders visual deviations into an `assumption_log`, and finding R-0665 measured that no such file exists anywhere in this repository while seventy-six tracked documents name it — re-measured at `142af5e4`, where `git ls-tree -r --name-only` matches no path containing `assumption` and `git grep -l assumption_log -- docs/` still returns seventy-six. F022 therefore records its visual deviations as DECISIONs in `.agent/decisions.md`, which is the operative decision record this workflow actually reads, and says so rather than writing to a file that is not there. R-0665 stays OPEN; this is a route, not its fix.

CHOSEN (3), THE THRESHOLD IS NEVER COLOUR ALONE. `ux_spec.md` §14 rules that a state change never happens by colour only, and a money bar is the worst place to break that: the reader who cannot distinguish the warn tint from the normal one is exactly the reader a budget warning is for. At `warn` and at `exceeded` the metric therefore carries the level in its ACCESSIBLE NAME in words, and the track carries a non-colour signal of its own beside the tint. The estimate marker is a separate channel from the threshold and the two may never be driven from one another: a `~` that appeared at 85 per cent would claim the figure had become an estimate, which is a false statement about provenance rather than a loud one about spend.

CHOSEN (4), THE TINTS COME FROM THE PRIMITIVES BOTH SHEETS ALREADY CARRY. `--remedy-orange-400` at `warn` and `--remedy-red-500` at `exceeded`, each defined exactly once in `apps/ui/src/styles/tokens.css` and exactly once in `docs/ui/design_reference/tokens.css` — measured, because those two sheets are known to disagree elsewhere and finding R-0661 is what that costs. No new token is minted, no literal hex enters a cost rule, and `assets_spec.md` needs no amendment because the glyph this round draws is one it already specifies.

CHOSEN (5), THE COST TRACK FOLLOWS THE SPEC AND THE PROGRESS TRACK IS LEFT ALONE. The new track is 6px at radius 3 over `--remedy-blue-100` with a 350ms transition, as §10 rules. The neighbouring `.progressTrack` is 5px over an rgba base at 600ms and predates that sentence; it is out of this feature's scope and MetricsBar's other metrics are on its Do-not-touch list, so the two will differ on disk until a round owns that file for its own reasons. Saying so here is cheaper than a reader discovering it and assuming one of them is a typo.

CORRECTION TO DECISION F022 D4, appended here because §3 checklist item 20 forbids rewriting a landed paragraph. D4's REVERSE clause names deleting `costMetric.ts` with its test file and narrowing `RemedyMetricKey`, and adds "nothing else reads either". That is incomplete and the completed form is: also remove the optional `cost?: CostMetricView` field from `RemedyMetric` and the `import type { CostMetricView } from "./costMetric";` line above it in `apps/ui/src/api/types.ts`, without which the reversal leaves an import of a deleted module and `npm run typecheck` goes red. Registered as finding R-0672.

ALTERNATIVES CONSIDERED. Give the threshold its own token pair rather than reusing the primitives: rejected, a token minted for one metric is a token the reference does not carry, which is the R-0661 divergence created deliberately instead of inherited. Signal the threshold by colour alone and rely on the tooltip: rejected under clause 3 — a tooltip is a hover, and a state a keyboard reader cannot reach is a state it does not have. Reuse `.progressTrack` for the cost fill: rejected under clause 5, since the two specs differ and sharing the rule would silently migrate the progress metric's appearance inside a cost feature. Put the formatting in the component and keep the module pure of strings: rejected under clause 1 and D4 clause 5, because the format is part of what "renders honestly" means — `"—"` versus `"$0.00"` is the whole of the no-fake-zeros rule.

REVERSE IT by deleting the cost rules from `TopMetricsBar.module.css`, the cost branches from `TopMetricsBar.tsx`, `CoinGlyph` from `RemedyGlyphs.tsx` and `tests/ui_contracts/test_cost_metric_render.py` entirely, and by dropping the goldens describe block from `costMetric.test.ts`. That is the whole of this round's production surface and it is stated here as a complete list, which is the obligation R-0672 exists to remember.
<<<END DEC5
