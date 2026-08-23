── STEP RULE/3 — F022 Live cost ticker · Runde 11 ────────────────────────────

Fortschritt: ~75 % (T001 fertig · T002 fertig · T003a fertig · T003b offen;
             diese Runde baut nichts, sie entscheidet die Quelle der
             Schluss-Zahl und schreibt das R10-Urteil auf Platte) — Schaetzung

Goal:        Rule where the terminal reconciliation's ledger figure comes from,
             and amend the feature file that names a source which does not
             exist. Record the R10 verdict and one recurrence on the way. This
             round writes NO production code: T003b cannot be built against a
             name, and the reviewer measured that both the named source and its
             obvious substitute are wrong.

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the plan ·
             C2 repair the round map · C3 the R10 verdict and the R-0625
             recurrence · C4 DECISION F022 D7 · C5 the feature-file amendment ·
             C6 the handback.

Change:      Exactly these paths, nothing else:
               .agent/authored/f022-r11.md          (C0a)
               .agent/last_block.md                 (C0b)
               .agent/plan.md                       (C1)
               .agent/live_review.md                (C2, C3)
               .agent/decisions.md                  (C4)
               docs/roadmap/features/T5_F022.md     (C5)
               .agent/handoff.md                    (C6)

─── Slice convention ──────────────────────────────────────────────────────────
Each authored text below begins at its `<<<SLICE <name>` line and ends at its
`<<<END <name>` line; neither marker line is part of the slice, and no slice
contains a marker line. Extract them PROGRAMMATICALLY by marker line out of the
committed C0a blob — never retype, never rewrap, never reflow. The whole-text
slices are PLANF022R11, LEDGER11 and DEC7. MAPFROM11/MAPTO11 and SPECFROM/SPECTO
are FROM/TO pairs, and this block carries no other pair. Every slice is quoted
WITHOUT its trailing newline; PLANF022R11 replaces its file whole, and LEDGER11
and DEC7 each land as one newline plus the slice plus one newline.

CONTAINMENT TEST, run by the reviewer on the final bytes, output quoted, one
reading per pair and none of it generalised from another:
  MAPFROM11/MAPTO11 — `TO contains FROM: false` → REWRITE.
  SPECFROM/SPECTO   — `TO contains FROM: false` → REWRITE.

Constraints:
 1. NEVER edit a slice. Apply it byte for byte. If a slice contradicts a fact
    you measure, apply it anyway and DECLARE the contradiction in the handback
    under Deviations. Repair nothing outside your slices; rule on nothing.
 2. C1 is the FIRST substantive commit (§3 checklist item 23): this round
    touches the finding ledger, so the plan advances before anything else but
    the two block-save commits.
 3. COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4, C5, C6 and no other. Both pairs
    are applied before either append reads its file (R-0639/R-0640). LEDGER11's
    two paragraphs land in ONE commit, C3, or neither: its `Gate: R10` paragraph
    states that the recurrence is written in that same commit, and THIS
    constraint is what makes that true (§3 item 20, R-0524 carve-out).
 4. NO PRODUCTION CODE, NO TESTS. Nothing under `apps/`, `packages/` or `tests/`
    is in the Change set. T003b is the NEXT round's work and this round exists
    to make that round buildable.
 5. NO REPAIR of any open finding. R-0670 still waits for the next round that
    touches `packages/orchestration/ui_server.py` on its own account, which this
    round is not.
 6. C5 EDITS A ROADMAP FEATURE FILE, which AGENTS.md permits for feature detail
    files under `docs/roadmap/features/` — only `docs/roadmap/ROADMAP.md` needs
    an explicit operator request, and it is NOT in the Change set. Because the
    Change set holds a `docs/roadmap/**` path, G9 gates `tests/docs/` and
    `tests/orchestration/test_roadmap_index.py` beside the state readers.
 7. Destructive verification runs ONLY inside a disposable worktree under
    `.remedy-wt/`. The primary checkout satisfies `git status --porcelain`
    empty at every commit and at the handback. Run no suite concurrently with a
    working-tree reading (R-0479).
 8. Every numeral this block states about the ROUND BASE `3e1d3fae` was produced
    by a reviewer script or a reviewer tool run at that commit and is a
    REFERENCE to report against, not a target to reproduce. Where your
    measurement differs, report BOTH and reconcile NOTHING.
 9. Size, measured by the reviewer on the final bytes of this block and stated
    once here: this block is 381 lines TOTAL with 137 CONTENT lines inside its
    slices, so PROSE is 244 — under DECISION F085 D6's 490 and D5's 400.

─── What the reviewer measured at `3e1d3fae`, and why this round rules ────────

THE FEATURE FILE NAMES A SOURCE THAT DOES NOT EXIST. Its Design section orders
the terminal reconciliation to "fetch the ledger's job figure (the stats
endpoint)". `packages/orchestration/ui_server.py` dispatches its job endpoints
from one `handlers` dict plus `events-since`; there is no `stats` among them,
and no endpoint literal anywhere in that file contains the string.

THE OBVIOUS SUBSTITUTE IS WRONG, and this is the measurement that decides the
round. The dashboard payload already carries `token_usage`, which reads like the
ledger figure and is not one. `_build_token_usage` sums `metadata.
estimated_tokens` over the job's events and returns `"estimated": True` with
`"source": "event_metadata"`; it attributes those tokens to `context`, `memory`,
`repair`, `planner` and `other` from event kinds such as
`source_context_injected` and `project_memory_recalled`. The ticker's figures
come from `BudgetCounters.measured_token_total` and `measured_cost_usd`, which
count PROVIDER CALLS. The two count different populations, so a "delta" between
them would not be a reconciliation — it would be a fabricated honesty moment,
which is the one thing this feature exists to avoid. A round that wired them
together would have shipped a number that looks like truth and is not.

WHAT DOES EXIST is the run log. `_emit_budget_tick` writes every tick through
`RunLogWriter` under the stable run id `budget-ticks`, so the LAST tick in that
log is the ledger's own record of the final measured figures, in the same
whitelisted shape `_budget_tick_summary_payload` already puts on the wire. That
is a real authority and it is already on disk; DECISION F022 D7 below rules it
as the source and fixes the delta as a statement about TRANSPORT rather than
about arithmetic.

─── Done when ─────────────────────────────────────────────────────────────────

Run every gate below yourself, record its REAL exit code, and put ONE LINE per
gate in the handback with the transcripts kept out of it (R-0582). G1 through
G12 run after C5 and BEFORE C6, so the handback can quote all of them (§3
checklist item 31). The round base is `3e1d3fae` throughout.

 G1  `.agent/STOP` absent, read from disk before C0a and again before C6.
     Branch `feature/f022-live-cost-ticker`. `git status --porcelain` 0 lines
     after every one of C0a through C5.
 G2  TRANSPORT. sha256 over the block file the reviewer wrote at
     `.remedy-wt/f022-r11.md`, over the committed C0a blob, over the committed
     C0b blob and over `.agent/last_block.md` on disk: report all four digests,
     byte counts and line counts, and require them EQUAL. The digest the
     delegation names is the fifth reading and must agree.
 G3  EXTRACTION. Run an extractor over the COMMITTED C0a blob that finds the
     slices by their marker LINES and report how many slices and how many
     CONTENT lines it printed, plus the block's TOTAL and PROSE line counts.
     Report those against constraint 9's numerals; reconcile nothing.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF022R11 plus exactly one
     newline. NEGATIVE CONTROL: the same comparison against the BARE slice must
     be FALSE, and report both byte counts. `^## Goal$` once, `^## Next Steps$`
     once, `wc -l` at most 50.
 G5  THE TWO PAIRS. Report each pair's containment output and require it to
     match the convention block. At C2 in `.agent/live_review.md`: MAPFROM11 1x
     at the round base and 0x at C2, MAPTO11 0x at base and 1x at C2, the file's
     byte length changing by exactly `len(MAPTO11) - len(MAPFROM11)`, and
     `^## Steps$` still exactly once. At C5 in
     `docs/roadmap/features/T5_F022.md`: SPECFROM 1x at the round base and 0x at
     C5, SPECTO 0x at base and 1x at C5, and the same byte-length identity.
     Report each count as a number. Confirm for BOTH that the committed file
     equals the base file with only that replacement applied and nothing else.
 G6  APPEND at C3, and the same two readers at C4. For each: the previous
     commit's blob is a byte-exact PREFIX of the committed file and the
     remainder is exactly one newline plus the slice plus one newline — report
     the remainder's byte count and the slice's. Then an INDEPENDENT reader:
     split both files on blank lines, let N be the number of paragraphs YOUR
     script counts in the slice, and require the LAST N units of the committed
     file to equal the slice's N paragraphs IN ORDER. Report N; do not take it
     from this block. NEGATIVE CONTROL, in a disposable worktree, applied to the
     FIRST appended paragraph of LEDGER11 and to the FIRST of DEC7: flip ONE
     byte at an offset you name and confirm BOTH readers reject each mutant
     while both accept the true file. THE OFFSET IS A BYTE OFFSET — both files
     carry multi-byte em dashes and arrows, so a CHARACTER offset lands
     thousands of bytes early, outside the appended region, where reader (b)
     accepts the mutant and the control proves nothing. Report the ~20 bytes
     surrounding each flip. Remove the worktree; `git worktree list` back to one
     line.
 G7  LEDGER INTEGRITY, base versus C3. Report for both points: the count of
     lines matching `^- R-\d+ — `, whether they are all DISTINCT, the MAXIMUM
     id, the count of `^Done: R-` with its distinct ids, of `^Landed: `, of
     `^Recurrence: R-` with its distinct ids, and of `^Gate: R` with its
     distinct keys. Report the ids ADDED and REMOVED as sets. At base the
     reviewer measured 234 records, all distinct, maximum `R-0673`, 1 `Done:`
     line for `R-0653`, 0 `Landed:`, 4 `Recurrence:` lines and 10 `Gate:` lines
     over 10 distinct keys. This round MINTS NO NEW ID: it is expected to add no
     record, to take `^Recurrence: R-` to 5 by gaining `R-0625`, and to add
     `Gate: R10`. Report what you measure. `R-0625` must still occur exactly once
     as a `^- R-0625 — ` record.
 G8  DECISIONS at C4. `^## DECISION F022 D7 ` occurs exactly once in
     `.agent/decisions.md` at C4 and 0 times at the round base. Report both.
 G9  THE DOCS GATES, because C5 touches `docs/roadmap/**`: from the REPOSITORY
     ROOT, `python3 -m pytest tests/docs/ -q` and
     `python3 -m pytest tests/orchestration/test_roadmap_index.py -q`, each exit
     0, run SERIALLY. The reviewer measured 295 and 30 at the round base.
 G10 THE FOUR STATE READERS plus THE CANARY, serially in the PRIMARY checkout at
     C5, exit 0: `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py`,
     `tests/orchestration/test_integrity_gate.py`, then
     `tests/cli/test_golden_path.py`. The reviewer measured 544 passed across
     the four and 42 for the canary at the round base. Never run two pytest
     processes at once.
 G11 STRUCTURE, reported for the commits BEFORE C6 and for the range as a whole
     (C6's own numbers belong to the next round's ledger entry, not here):
     every commit single-parent; each commit's INSERTION count, each under the
     500 cap; the range path set against the Change set above with the
     difference reported in BOTH directions; `git show --numstat` agreeing cell
     by cell with the handback's `## Commits` table; the LINE-ANCHORED patterns
     `^<<<SLICE ` and `^<<<END ` counting 0 in `.agent/plan.md`,
     `.agent/live_review.md`, `.agent/decisions.md` and
     `docs/roadmap/features/T5_F022.md` — ANCHORED because a slice of this block
     legitimately quotes those markers mid-line inside backticks, so an
     unanchored count would be unsatisfiable for every possible round (§3
     checklist item 2); `git ls-files .remedy-wt` 0; one worktree; and the
     round's reflog rows with amend, rebase and cherry counts, each 0.
 G12 `gh pr list --state open --json number,headRefName`. Report it verbatim.
     Create no PR and merge nothing this round: T003b is unbuilt and the
     integration gate has not run.
 G13 STALENESS. Every sentence C1 through C5 land that states a fact about a
     file is re-measured at C5, and any that has gone stale is reported as a
     residual rather than repaired. Report explicitly that you checked, and name
     any residual. Slices are NEVER edited to fix one.

NOT A GATE and not run this round: `npm run lint`, `npm run typecheck` and
`npm run test:unit`. The Change set holds no file under `apps/`, so none of the
three can say anything about it. For the lint reading specifically, see
LEDGER11's `R-0625` recurrence, which corrects a numeral three earlier blocks
carried.

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             every mandated section in order, one changed-files table per
             commit, an item-status row per Bundle item, the round base SHA,
             ONE line per gate, and the `Fortschritt:` block above carried
             VERBATIM across all three of its lines. Every count you report
             names the exact string or pattern counted and the file it was
             counted in (R-0442). The cap is 100 lines for this commit count;
             declare a DECISION D15 stated cause with your own measured numeral
             in the declaring line if the mandated content genuinely does not
             fit. THIS HANDBACK MAY END THE SESSION, so its `## Next` section
             names, in this order: (1) Phase 1 rule 1 — re-read `.agent/STOP`
             from disk before anything else; (2) the Open PR Gate; (3) R12,
             T003b, built against DECISION F022 D7 and naming its two halves —
             the server's final-figure section and the client's reconciliation
             with the delta label; (4) that R11's own verdict is NOT yet on
             disk and R12's ledger commit owes it.
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF022R11
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
R11 rules the terminal reconciliation's source and builds nothing. The feature
file named "the stats endpoint", which does not exist, and the dashboard's
`token_usage` — the obvious substitute — is an estimate summed over a different
event population, so a delta against it would be fabricated. DECISION F022 D7
rules the run log's last budget tick as the authority and this round amends the
feature file to match. It also records the R10 verdict and the R-0625
recurrence.

## Next Steps
1. R12 T003b — the server's final-figure section and the client's terminal
   reconciliation with the delta label, built against DECISION F022 D7.
2. R13 the integration gate.
3. R14 closure.

## Risks
- T003b is now a TWO-SIDED slice: D7 puts a final-figure section on the server
  as well as the reconciliation on the client, so R12 is larger than T003a was
  and may need splitting at its own block.
- Open F022 findings, each with the round that owns it: R-0670 waits for the
  next round touching `packages/orchestration/ui_server.py` on its own account,
  which R12 will be; R-0672 and R-0625 want their next-DECISION and next-numeral
  clauses honoured, which DECISION F022 D7 and this round's ledger entry do.
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks, not F022 defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- R-0665 is open and this feature needs its route: every UI feature is told to
  record visual deviations in an `assumption_log` that does not exist. F022
  records them as DECISIONs in `.agent/decisions.md`, a route rather than a fix.
<<<END PLANF022R11

<<<SLICE MAPFROM11
budget → R10 T003a the live wiring, which gives the cost module its first
production caller, plus the R9 verdict and this map repair → R11 T003b the
terminal reconciliation and the delta labelling → R12 the integration gate →
R13 closure.
<<<END MAPFROM11

<<<SLICE MAPTO11
budget → R10 T003a the live wiring, which gives the cost module its first
production caller, plus the R9 verdict and this map repair → R11 rule the
terminal reconciliation's SOURCE, because the feature file named an endpoint
that does not exist, and record the R10 verdict → R12 T003b the server's
final-figure section and the client's reconciliation with its delta label →
R13 the integration gate → R14 closure.
<<<END MAPTO11

<<<SLICE SPECFROM
- Terminal reconciliation: on the terminal event, fetch the
  ledger's job figure (the stats endpoint) and render it as the
  final value; a delta beyond rounding renders "final (ledger):
  X — live estimate was Y" (the honesty moment, small type,
  per reference).
<<<END SPECFROM

<<<SLICE SPECTO
- Terminal reconciliation: on the terminal event, read the
  ledger's final budget tick — the last `budget.tick` in the
  job's `budget-ticks` run log, in the same whitelisted shape
  the stream already carries — and render it as the final
  value; a delta beyond rounding renders "final (ledger):
  X — live estimate was Y" (the honesty moment, small type,
  per reference). AMENDED at F022 R11 per DECISION F022 D7:
  this bullet previously named "the stats endpoint", which
  `ui_server.py` does not dispatch, and the nearest substitute
  (`token_usage`) is an estimate over a different event
  population, so a delta against it would be fabricated. The
  delta this bullet asks for is a TRANSPORT statement — what
  the client received against what the ledger holds — and
  never a second arithmetic.
<<<END SPECTO

<<<SLICE LEDGER11
Recurrence: R-0625 — A NUMERAL ABOUT ANOTHER COMMIT'S TOOL OUTPUT WAS CARRIED ACROSS FOUR BLOCKS WITHOUT THE TOOL EVER BEING RUN AT THAT COMMIT, AND IT WAS MISLABELLED AT ITS ORIGIN. Second instance, at F022 R7 through R10. NO NEW ID IS MINTED: §3 checklist item 30 requires the open set searched for the DEFECT before an id, and R-0625 already holds this class with the counter-measure that a numeral a block states about ANOTHER commit's tool output is produced by RUNNING that tool at that commit before emission, never by recollection — R-0364 applied to a value rather than to a colour. THE INSTANCE: the F022 R7, R8, R9 and R10 blocks each state that `npm run lint` in `apps/ui` is red at their base "at 72 problems". MEASURED by the reviewer at the R10 base `a8952614`, by running the primary checkout's own eslint binary against a disposable worktree of that commit with the primary config passed explicitly, and against the primary tree as a matched control in the same pass: the base reports 74 problems (72 errors, 2 warnings) over 71 files, while `3e1d3fae` reports 78 problems (76 errors, 2 warnings) over 75 files. SO THE NUMERAL WAS THE ERROR COUNT WEARING THE WORD "problems", which is eslint's own summary term for errors plus warnings, and the two differ by exactly the 2 warnings. THE CORRECTED VALUE AT `a8952614` IS 74 PROBLEMS, OF WHICH 72 ARE ERRORS. WHY IT SURVIVED FOUR BLOCKS: the sentence was true enough to never be checked — lint IS red, it IS R-0622, and it IS not a gate — so no gate consumed it and each block copied it from the one before rather than re-running a tool it had already excluded from its gates. THE ROUND'S OWN DELTA IS CLEAN AND WAS MEASURED IN THE SAME PASS: the four files reported at `3e1d3fae` and not at the base are exactly `budgetTick.ts`, `budgetTick.test.ts`, `costTicker.ts` and `costTicker.test.ts`, each contributing exactly one `Parsing error`, and no file's count changed, so R10 introduced no lint rule violation and R-0622's characterisation is untouched. WHY LOW: nothing consumed the number, it was explicitly not a gate, and the R10 worker reported its own 78 against the block's 72 and reconciled NOTHING, exactly as that block's constraint 9 ordered — the process worked and only the value was stale. THE LANDED BLOCKS ARE NOT REWRITTEN, per §3 item 20: this correction is dated by the commit that carries it. Both instances stay OPEN under R-0625, and the fix is the one it already names, with one addition this instance earns: a tool's summary line is quoted with the WORD the tool uses, because "72 problems" and "72 errors" are different readings of the same run and only one of them was taken.

Gate: R10 — the F022 R10 entry. R10 PASSED ON EVERY ONE OF ITS SIXTEEN GATES, AND THE REVIEWER RE-RAN EVERY ONE OF THEM ITSELF AND ADDED FOUR MUTATIONS THE BLOCK NEVER ORDERED. The recurrence above is written in THIS SAME COMMIT, which the R11 block's constraint 3 fixes. THE ROUND'S SUBSTANCE IS THAT THE FEATURE STOPPED BEING INVISIBLE: `costMetricOf` was correct from R7 and drawn from R8 while having NO production caller — measured at `a8952614` over every non-test `.ts`/`.tsx` under `apps/ui/src`, the only file naming `costMetricOf(` was `costMetric.ts` itself — and `normalizeDashboardPayload` built seven metrics with no `cost` among them, so the tile a user saw was not empty but ABSENT. R10 built the path: `budgetTickFiguresOf` reads one frame, `receiveBrainFrame` folds the latest tick onto `BrainStreamState` behind the replay guard and carries it forward BY REFERENCE, the runner publishes it on `BrainStreamView` and compares it with `===`, `metricsWithCostTicker` fills the eighth tile, and `RemedyShell` composes the bar through it. TRANSPORT HELD IN ITS STRONGEST FORM: the reviewer's scratch original, the committed C0a blob, the committed C0b blob, `.agent/last_block.md` on disk and `.agent/authored/f022-r10.md` on disk are ALL sha256 `49f733db1d02020f7823874a566e8ea359b64cadf38065dbd19ab4f59b566c23` over 38270 bytes and 482 lines, and C0a and C0b resolve to the SAME git blob `a763f93d`. THE EXTRACTION printed 5 slices over 121 CONTENT lines, so TOTAL re-measures at 482 and PROSE at 361, and constraint 10's numerals reproduce exactly. `.agent/plan.md` at `63119805` is 2727 bytes = PLANF022R10's 2726 plus one newline, the bare-slice control DIFFERING, headings once each, 48 lines against the cap of 50. THE PAIR AT `593c26c6` IS EXACT: `TO contains FROM: false`, MAPFROM 1→0, MAPTO 0→1, byte delta 439 = 810 − 371, and the committed file equals the base with ONLY that replacement applied. BOTH APPENDS HOLD UNDER BOTH READERS: at `44063bf0` the prefix is byte-exact and the remainder is 6606 = 1 + LEDGER10's 6604 + 1 with N=2 paragraphs equal in order over 265→267 units; at `d8ca0f11` the remainder is 3564 = 1 + DEC6's 3562 + 1 with N=6 equal in order over 1297→1303. THE SETS MOVED EXACTLY WHERE THE ROUND PROMISED: 234 records at base and 234 at C3, ids ADDED and ids REMOVED both the EMPTY SET so NO ID WAS MINTED, `^Recurrence: R-` 3→4 gaining `R-0644`, `^Gate: R` 9→10 gaining the key `R10`'s predecessor `R9`, and `^- R-0644 — ` exactly 1 at both so the recurrence APPENDED rather than rewrote. THE SUITES ARE THE REVIEWER'S OWN: `npm run typecheck` clean; `npm run test:unit` 19 files and 268 tests against the base's 17 and 241, the +27 accounted for file by file; `tests/ui_contracts/` 518 passed and 4 skipped from the REPOSITORY ROOT against the base's 514 and 4, the +4 being C8's new class; the four state readers 455, 52, 21 and 16 for 544; and the canary 42. STRUCTURE HELD: eleven commits before the handback, every one single-parent, insertions 482, 402, 22, 10, 4, 55, 92, 151, 128, 71 and 12, each under the 500 cap; the range path set is exactly the declared nineteen-path Change set with the difference EMPTY in both directions; `git show --numstat` agrees cell by cell with all nineteen `## Commits` rows, the full-file `.agent/last_block.md` row reading `+402/-148` in both; anchored markers 0 in all three state files; `git ls-files .remedy-wt` 0; one worktree; 0 amend, 0 rebase and 0 cherry. THE FOUR MUTATIONS ARE THE REVIEWER'S OWN AND ALL RAN IN A DISPOSABLE WORKTREE WITH THE PRIMARY CHECKOUT NEVER WRITTEN: reverting the shell to the bare `dashboard.metrics` failed exactly `test_the_shell_hands_the_stream_budget_to_the_bar`; making the ticker name a figure field failed exactly `test_the_figure_fields_have_a_single_home`; replacing the by-reference carry-forward with a spread copy failed 3 tests across `brainStream.test.ts` and `brainStreamRunner.test.ts`, which is the round's subtlest property and it is genuinely pinned; and deleting the kind check in `budgetTickFiguresOf` failed `budgetTick.test.ts` — with the unmutated worktree green at 23 passed as the positive control. THE FIRST TWO OF THOSE CONTROLS WERE VACUOUS ON THE REVIEWER'S FIRST ATTEMPT, because the contract resolves `REPO_ROOT` from its own `__file__` and pytest was pointed at the PRIMARY copy while the mutation sat in the worktree; re-running against the worktree's own test file turned both red, and the first reading is recorded here because a control that cannot fail is the thing this record exists to catch. THE CONTRACT C8 ADDS IS BETTER THAN ORDERED: the block asked for three assertions and the worker added a fourth, `test_the_scan_reaches_the_one_file_it_asserts_about`, which pins that the absence scan reaches a non-empty file list — the vacuous-absence guard of R-0559, supplied unprompted. THE HANDBACK IS COMPLIANT at 136 lines with a DECISION D15 stated cause naming that same 136, every mandated section present and in order, and the three-line `Fortschritt:` block byte-identical to the block's. THE VERDICT IS PASS: every numeral R10 states reproduced under the reviewer's own measurement, four unordered mutations went red against the right tests, no slice was edited, no id was minted, and the COST metric now has a production caller for the first time since R7 built it.
<<<END LEDGER11

<<<SLICE DEC7
## DECISION F022 D7 — the source of the terminal reconciliation's ledger figure

CONTEXT. `docs/roadmap/features/T5_F022.md` orders the terminal reconciliation
to "fetch the ledger's job figure (the stats endpoint)". Measured at `3e1d3fae`:
`packages/orchestration/ui_server.py` dispatches its job endpoints from one
`handlers` dict plus `events-since`, and no `stats` endpoint is among them. The
spec names a source that has never existed, so T003b could not be built as
written.

REJECTED, and this is the substantive half of the ruling. The dashboard payload
already carries `token_usage`, which reads like the ledger figure. It is not
one. `_build_token_usage` sums `metadata.estimated_tokens` across the job's
events and returns `"estimated": True` with `"source": "event_metadata"`,
attributing tokens to `context`, `memory`, `repair`, `planner` and `other` from
kinds such as `source_context_injected` and `project_memory_recalled`. The
ticker's figures are `BudgetCounters.measured_token_total` and
`measured_cost_usd`, which count PROVIDER CALLS. The two populations are
disjoint in intent and in practice, so a delta between them measures neither
drift nor drop — it measures the difference between two unrelated questions.
Rendering it under the words "final (ledger)" would be the fabricated honesty
moment this feature exists to prevent, and it would be indistinguishable on
screen from a real one.

CHOSEN. The ledger figure is the LAST `budget.tick` in the job's run log.
`_emit_budget_tick` writes every tick through `RunLogWriter` under the stable
run id `budget-ticks`, so that log is the ledger's own record of the final
measured figures, already in the whitelisted shape
`_budget_tick_summary_payload` puts on the wire. The server exposes it as a
final-figure section; the client renders it at terminal in place of the live
value.

CONSEQUENTLY THE DELTA IS A TRANSPORT STATEMENT, never a second arithmetic. Both
sides of the comparison are the SAME quantity from the same producer: what the
client received over the stream, against what the ledger holds. A delta
therefore means frames were missed — an SSE gap, a disconnect, a ring overflow,
or a final tick emitted after the client stopped listening — which is exactly
what a reader deserves to be told, and it is measurable rather than guessed. The
client still performs no money arithmetic: it compares two figures the backend
produced and labels the difference.

ALTERNATIVES CONSIDERED. Adding the `stats` endpoint the spec names: rejected,
because it would be a new public surface invented to satisfy a sentence rather
than a need, and the figures already exist. Treating the last tick the CLIENT
holds as final: rejected, because it makes the reconciliation vacuous — the
client would compare a value with itself and could never show a delta, which is
the R-0438 vacuous-gate shape arriving in a feature. Recomputing the final
figure from the event stream in the client: rejected, because the UI never
computes money, which is this feature's founding constraint.

REVERSE IT path by path, derived from this round's Change set rather than from
the files most in mind. In `docs/roadmap/features/T5_F022.md` restore the
Terminal-reconciliation bullet's previous wording, which named the stats
endpoint and which this round's C5 replaced whole. In `.agent/live_review.md`
nothing is reversed, because the map repair at C2 and the ledger entry at C3
record round history rather than this decision. This decision ships no code, so
no production path is reversed here; a later round that builds against it
reverses its own paths under its own decision. That is every path this round's
Change set holds, which is what R-0672 and its recurrence require of a reversal
instruction.
<<<END DEC7
