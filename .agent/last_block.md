── STEP T001b/3 — F022 Live cost ticker · Runde 6 ────────────────────────────

Fortschritt: ~25 % (T001 fertig nach dieser Runde · T002 offen · T003 offen;
             die Zahlen erreichen ab hier wirklich den Client, vorher endeten
             sie im Umschlag) — Schaetzung

Goal:        Record the R5 verdict, rule the envelope widening as DECISION F022
             D3, and close T001: `_safe_event_summary` carries the budget tick's
             whitelisted figures for that ONE event kind, leaving every other
             kind's frame byte-identical, with tests that pin both halves.

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the plan ·
             C2 the R5 verdict · C3 DECISION F022 D3 · C4 the conditional
             widening and its tests · C5 the handback.

Change:      Exactly these paths, nothing else:
               .agent/authored/f022-r6.md        (C0a)
               .agent/last_block.md              (C0b)
               .agent/plan.md                    (C1)
               .agent/live_review.md             (C2)
               .agent/decisions.md               (C3)
               packages/orchestration/ui_server.py            (C4)
               tests/ui_server/test_budget_tick_envelope.py   (C4, new file)
               .agent/handoff.md                 (C5)

─── Slice convention ──────────────────────────────────────────────────────────
Each authored text below begins at its `<<<SLICE <name>` line and ends at its
`<<<END <name>` line; neither marker line is part of the slice, and no slice
contains a marker line. Extract them PROGRAMMATICALLY by marker line out of the
committed C0a blob — never retype, never rewrap, never reflow. The slices are
PLANF022R6, GATE5 and DEC3.

Constraints:
 1. NEVER edit a slice. Apply it byte for byte. If a slice contradicts a fact
    you measure, apply it anyway and DECLARE the contradiction in the handback
    under Deviations. Repair nothing outside your slices; rule on nothing.
 2. C1 is the FIRST substantive commit (§3 checklist item 23): this round
    touches the finding ledger, so the plan advances before anything else but
    the two block-save commits.
 3. `.agent/plan.md` is a WHOLE-TEXT replacement. GATE5 and DEC3 are APPENDS to
    append-only records: never rewrite a landed paragraph in either file, and
    add nothing to them beyond the slice. This block carries NO FROM/TO pair —
    the round map already describes this round and needs no repair.
 4. C4 is ONE commit carrying the widening and its tests together.
 5. `_safe_event_summary` has ONE writer and TWO transports — the cursor
    endpoint and the SSE stream — so what you add reaches both or neither. That
    is the point, not a hazard, and its docstring says so.
 6. Do not touch budget ENFORCEMENT, the pricing and basis rules, the emission
    R5 landed, or MetricsBar's other metrics. NO TypeScript changes this round:
    the client-side type widening belongs to T002, and a UI change here would
    put a rendering change inside a transport commit.
 7. Destructive verification runs ONLY inside a disposable worktree under
    `.remedy-wt/`. The primary checkout satisfies `git status --porcelain`
    empty at every commit and at the handback.
 8. Every numeral this block states about the ROUND BASE `9b854cf5` was
    measured by the reviewer at that commit and is a REFERENCE to report
    against, not a target to reproduce. Where your measurement differs, report
    BOTH and reconcile NOTHING.
 9. Size, measured by the reviewer on the final bytes of this block and stated
    once here: this block is 288 lines TOTAL with 56 CONTENT lines inside its
    slices, so PROSE is 232 — under DECISION F085 D6's 490 and D5's 400.

─── What R6 builds, and why it is conditional ─────────────────────────────────

`_safe_event_summary` returns exactly `{seq, event, timestamp, outcome,
task_id}` and DROPS the event's `metadata`. R5 emits a `budget.tick` whose every
figure lives in that metadata, so today a client subscribing to the stream
receives tick frames carrying no spend, no limit and no basis. DECISION F022 D1's
payload is correct and, until this round, unreachable.

The widening is CONDITIONAL ON THE EVENT KIND, and that is the whole design. Two
guards make an unconditional widening impossible: `tests/ui_server/test_sse_stream.py`
asserts the summary's key set with an exact set equality, and it pins a GOLDEN
BYTE STREAM rebuilt from the frame writers themselves. The reviewer measured both
at the round base — the key-set assertion feeds the summary an event named `x`,
and the golden's events are named `e0` and `e1`, so NEITHER is a tick and both
stay green byte for byte when only ticks gain a field. An unconditional widening
turns both red in the same commit as a new feature, which would leave two
independent changes sharing one failure and no way to tell them apart.

THE PAYLOAD IS COPIED KEY BY KEY OUT OF A WHITELIST, never passed through. The
`safe` in this function's name is load-bearing: it is a REDACTION boundary, and
this repository carries a `packages/orchestration/redaction_patterns` module with
forbidden field names and secret patterns precisely because event metadata is not
trusted. Passing a tick's metadata through wholesale would make any key a run-log
writer ever puts on a tick reachable by any stream subscriber. Whitelist the
outer fields DECISION F022 D1 rules, and whitelist the two keys inside `basis`
as well — a nested pass-through is the same leak one level down, and the
reviewer's dry run confirmed both leaks are blocked and neither guard is
redundant.

AN ABSENT KEY STAYS ABSENT. Do not fill a default, a null or a zero for a limit
the tick never carried: the acceptance criterion that a limitless job never
renders a fabricated denominator is enforced by the shape of this payload, and
supplying a default here would undo at the last hop what R5 was careful about at
the first. A tick whose metadata is missing or is not a dict yields an empty
payload rather than an error.

─── The tests ─────────────────────────────────────────────────────────────────

New file `tests/ui_server/test_budget_tick_envelope.py`, written by you, in the
conventions of `tests/ui_server/test_sse_stream.py`. Every test below is
REQUIRED and each must be able to fail:

 T1  A non-tick event's summary key set is EXACTLY the five it was before. Name
     the five; this is the byte-compatibility half and it is the one a future
     round will be tempted to break.
 T2  A tick event's summary carries those five PLUS the payload key, and the
     payload holds every field DECISION F022 D1 rules that the metadata carried.
 T3  A field the whitelist does not name — put a plausible secret in the tick's
     metadata — does NOT appear anywhere in the serialised summary. Assert
     against the serialised JSON text, not only against the dict keys.
 T4  The same, one level down: a key inside `basis` that the whitelist does not
     name does not survive.
 T5  A limit the tick never carried is ABSENT from the payload — assert key
     absence, not a null and not a zero.
 T6  A tick with NO metadata, and a tick whose metadata is not a dict, both
     yield an empty payload and raise nothing.
 T7  The cursor endpoint and the SSE stream carry the SAME summary for a tick.
     `test_sse_stream.py` already has a one-envelope test for the general case;
     this one pins that a tick is not an exception to it.

─── Done when ─────────────────────────────────────────────────────────────────

Run every gate below yourself, record its REAL exit code, and put ONE LINE per
gate in the handback with the transcripts kept out of it (R-0582). G1 through
G12 run after C4 and BEFORE C5, so the handback can quote all of them (§3
checklist item 31). The round base is `9b854cf5` throughout.

 G1  `.agent/STOP` absent, read from disk before C0a and again before C5.
     Branch `feature/f022-live-cost-ticker`. `git status --porcelain` 0 lines
     after every one of C0a, C0b, C1, C2, C3 and C4.
 G2  TRANSPORT. sha256 over the block file the reviewer wrote at
     `.remedy-wt/f022-r6.md`, over the committed C0a blob, over the committed
     C0b blob and over `.agent/last_block.md` on disk: report all four digests,
     byte counts and line counts, and require them EQUAL. The digest the
     delegation names is the fifth reading and must agree.
 G3  EXTRACTION. Run an extractor over the COMMITTED C0a blob that finds the
     slices by their marker LINES and report how many slices and how many
     CONTENT lines it printed, plus the block's TOTAL and PROSE line counts.
     Report those against constraint 9's numerals; reconcile nothing.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF022R6 plus exactly one
     newline. NEGATIVE CONTROL: the same comparison against the BARE slice must
     be FALSE, and report both byte counts. `^## Goal$` once, `^## Next Steps$`
     once, `wc -l` at most 50.
 G5  APPEND at C2 and again at C3, each proved twice. The round-base blob is a
     byte-exact PREFIX of the committed file, and the remainder is exactly one
     newline plus the slice plus one newline — report the remainder's byte count
     and the slice's. Then an INDEPENDENT reader: split both files on blank
     lines, report the unit counts before and after, and require the LAST unit
     equal to the slice's own last paragraph. Lines beginning
     `## DECISION F022 D3 ` count 1 at C3. NEGATIVE CONTROL, in a disposable
     worktree: flip ONE byte of the appended region at an offset you name and
     confirm BOTH readers reject the mutant while both accept the true file.
     Remove the worktree; `git worktree list` back to one line.
 G6  LEDGER INTEGRITY, base versus C2. Report for both points: the count of
     lines matching `^- R-\d+ — `, whether they are all DISTINCT, the MAXIMUM
     id, the count of `^Done: R-`, of `^Landed: `, and of `^Gate: R` with its
     distinct keys. Report the ids ADDED and REMOVED as sets. At base the
     reviewer measured 230 records, all distinct, maximum `R-0669`, 0 and 0 for
     Done and Landed, and 5 `Gate:` lines with 5 distinct keys. `^## Steps$`
     occurs exactly once at C2 and the map text is UNCHANGED this round —
     report the map paragraph byte-identical at base and at C2.
 G7  RUFF, the repository's own configuration and NOT `--isolated`:
     `python3 -m ruff check packages/orchestration/ui_server.py
     tests/ui_server/test_budget_tick_envelope.py` at C4, exit 0. Pair it with a
     RED CONTROL inside the disposable worktree — a file whose only line is an
     unused import — and report both exit codes.
 G8  THE TWO GUARDS THE WIDENING MUST NOT BREAK, at C4, each exit 0 and each
     with its passed count: `python3 -m pytest tests/ui_server/test_sse_stream.py
     -q` and `python3 -m pytest tests/ui_server/test_command_channel.py -q`. The
     reviewer measured 66 and 100 at the round base WITH this change applied in a
     worktree, so equal counts are expected; report what you measure. Then
     RED-PROOF that they really do guard: in the disposable worktree make the
     widening UNCONDITIONAL — add the payload key for every event kind, not only
     the tick — and report which tests fail and by what name. If that mutation
     leaves both files GREEN, say so plainly: it would mean the block's whole
     rationale is wrong, and that is worth more than a green line.
 G9  THE NEW TESTS: `python3 -m pytest
     tests/ui_server/test_budget_tick_envelope.py -q` at C4, exit 0, with the
     passed count and the node ids reported. Then RED-PROOF the whitelist, in
     the worktree: replace the key-by-key copy with a wholesale pass-through of
     the tick's metadata and report which tests fail — T3 and T4 must both be
     among them. Revert before the next gate.
 G10 NO REGRESSION, serially in the PRIMARY checkout at C4, each exit 0 with its
     count: `tests/orchestration/test_budget_tick.py`,
     `tests/ui_contracts/test_humanize_catalog.py` and
     `tests/orchestration/test_safe_points.py`. The reviewer measured 10, 9 and
     78 at the round base. Never run two pytest processes at once.
 G11 THE FOUR STATE READERS, serially, at C4, exit 0: `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py` and
     `tests/orchestration/test_integrity_gate.py`. The reviewer measured 528
     passed at the round base; this round ADDS a file under `tests/ui_server/`,
     so report the count you measure and the difference, and do NOT treat a
     larger number as a failure.
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

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             every mandated section in order, one changed-files table per
             commit, an item-status row per Bundle item, the round base SHA,
             ONE line per gate, and the `Fortschritt:` block above carried
             VERBATIM across all three of its lines. The cap is 100 lines for
             this commit count; declare a DECISION D15 stated cause if the
             mandated content genuinely does not fit.
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF022R6
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
R6 records the R5 verdict, rules the envelope widening as DECISION F022 D3, and
closes T001: `_safe_event_summary` carries the budget tick's whitelisted figures
for that ONE event kind, so every other kind's frame stays byte-identical and
the tick's numbers reach a client for the first time.

## Next Steps
1. R7 T002 the COST metric on fixture streams — the client type widening, the
   fill, the '~' prefix and tooltip, the thresholds and the no-limit variant.
2. R8 T003 the terminal reconciliation and the delta labelling.
3. R9 the integration gate, then closure.

## Risks
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks rather than F022
  defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- R7 widens a CLOSED union, `RemedyMetricKey`, and a value type with nowhere to
  put a limit or a basis, both measured in the R3 inventory. That is a
  type-level change rather than an additive one, and R7 is sized for it.
- R7 is the first F022 round to touch `apps/ui/src`, where the shipped stylesheet
  and the design_reference sheet define different token sets; grep the shipped
  CSS, never the reference, when a token is claimed to exist.
<<<END PLANF022R6

<<<SLICE GATE5
Gate: R5 — the F022 R5 entry. R5 PASSED ON EVERY ONE OF ITS SEVENTEEN GATES, AND IT IS THE FIRST F022 ROUND TO SHIP PRODUCTION CODE. THE REVIEWER RE-RAN EVERY MEASURABLE GATE ITSELF AND ADDED A MUTATION THE BLOCK NEVER ORDERED. TRANSPORT HELD IN ITS STRONGEST FORM: the reviewer's own emitted bytes at `.remedy-wt/f022-r5.md`, the committed C0a blob at `d43b0a3b`, the committed C0b blob at `d63cab91`, `.agent/last_block.md` on disk and `.agent/authored/f022-r5.md` on disk are ALL sha256 `657abe6c545fe74321dd533fc0bd919f942a1111e3c1df004b954964b9b70e88` over 33039 bytes and 366 lines, so §4.9's primary comparison against the reviewer's own original was available and was used rather than the digest fallback. THE EXTRACTION out of the committed blob printed 5 slices over 67 CONTENT lines, so TOTAL re-measures at 366 and PROSE at 299, under DECISION F085 D6's 490 and D5's 400, and constraint 9's numerals reproduce exactly. `.agent/plan.md` at `ec0916aa` is byte-equal to PLANF022R5 plus one newline at 2234 bytes against the bare slice's 2233, with the bare-slice control DIFFERING, `^## Goal$` and `^## Next Steps$` once each and 41 lines. THE LEDGER COMMIT IS PROVED BY RECONSTRUCTION, which is strictly stronger than a prefix reading and was the right choice because the round both REWROTE the round map and APPENDED a verdict: the round-base blob with the STEPSF022R5 FROM string replaced exactly once by the TO string, then one newline plus GATE4 plus one newline, is BYTE-EQUAL to `0c8d9712:.agent/live_review.md` at 497163 bytes — so nothing else in that file moved, which no prefix test could have shown. The FROM counted 1 at base and 0 at C2, the TO 0 then 1, and a one-byte flip of the reconstruction is REJECTED. THE DECISION APPEND HOLDS UNDER TWO READERS: the base blob is a byte-exact PREFIX at `7fa31892`, the remainder is 5662 bytes which is exactly one newline plus DEC2's 5660 plus one newline, an independent blank-line splitter reads 1261 units before and 1270 after with the LAST equal to DEC2's own last paragraph, and `## DECISION F022 D2 ` counts 1. THE SETS ARE UNCHANGED WHERE THE ROUND PROMISED: 230 records all DISTINCT at base and at C2, maximum id `R-0669` at both, `^Done: R-` 0, `^Landed: ` 0, ids added and ids removed BOTH the empty set, and `^Gate: R` moving 4 to 5 with the distinct keys gaining `Gate: R4`. `^## Steps$` occurs once. THE MARKER SWEEP NEEDED THE RIGHT READING AND GOT IT: lines BEGINNING `<<<SLICE ` or `<<<END ` count 0 in every slice target, while the substring occurs 6 times inside `.agent/live_review.md` — every one of them backticked prose in a historical finding or an earlier gate entry, which is the R-0462 class this record has quoted for rounds, and the worker counted lines rather than substrings exactly as the gate said. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout, every one matching the figure the block referenced: the new `tests/orchestration/test_budget_tick.py` exit 0 at 10 passed, `tests/ui_contracts/test_humanize_catalog.py` exit 0 at 9, `test_safe_points.py` 78, `test_budget_stop_integration.py` 39, `test_job_budgets.py` 135, `test_long_run_executor.py` 74, `test_predictive_budget.py` 75, `tests/ui_server/test_sse_stream.py` 66, the four state readers 528, and the canary `tests/cli/test_golden_path.py` 42. `ruff check` over the two authored Python paths with the repository's own configuration is exit 0. THE MUTATIONS ARE THE HEART OF THIS VERDICT, because a new test file that cannot fail is decoration. The reviewer re-ran both ordered red-proofs in a disposable worktree at `9b854cf5` and reproduced the round's own colours exactly: routing the emission through `timeline.append_run_event` fails 2 of 10 with `test_a_pingpong_shaped_job_id_still_emits` among them, and moving the emission inside the `if evaluation.exhausted:` branch fails 9 of 10 with `test_an_exhausted_budget_still_ticks_and_still_stops` among them. THE REVIEWER THEN ADDED A THIRD MUTATION THE BLOCK NEVER ORDERED, swapping the `absent`-before-`lower_bound` order in the cost basis, and `test_a_limitless_money_side_leaves_the_keys_out` catches it alone — so the ordering that the C4 docstring justifies from `packages/orchestration/budget_guard.py:304-305`, where an unpriced run sets `cost_lower_bound` true with no cost figure at all, is pinned by a test and not only by a comment. THE TESTS CARRY THEIR OWN DISCRIMINATORS, which is why they are worth what they cost: T6 proves its premise with `pytest.raises(ValueError)` over `UUID(job_id)` before asserting the tick exists, T9 asserts the healthy arm wrote exactly one tick before proving the broken arm adds none, and T10 asserts the signature reader actually found named parameters before asserting disjointness from them. Each is the shape a guard test needs and each was written by the worker rather than ordered. THE PRODUCTION DIFF IS WHAT THE BLOCK ORDERED AND NOTHING MORE: `_emit_budget_tick` and `_budget_tick_payload` added above `should_stop`, one call inserted between `evaluate_budget` and the exhaustion test, one catalog line, and no change to `should_stop`'s returns, reasons or sources. STRUCTURE HELD: seven commits over `94694b3f`..`9b854cf5`, every one single-parent, insertions 366, 336, 14, 7, 18, 425 and 50, each under the 500 cap; the range path set is exactly the block's declared Change set with the difference EMPTY in both directions; `git ls-files .remedy-wt` 0; one worktree; `git status --porcelain` empty; 0 amend, 0 rebase and 0 cherry; and the `## Commits` table agrees cell by cell with `git diff-tree --numstat` for every tabled commit. THE HANDBACK IS COMPLIANT at 99 lines against the 100 the seven-commit case allows, every mandated section present and in order, an item-status row per Bundle item, one line per gate, and the block's three-line `Fortschritt:` carried VERBATIM. THE ROUND'S TWO DECLARED DEVIATIONS ARE BOTH CORRECT AND ONE OF THEM CORRECTS THE REVIEWER. The first is a strengthening the block did not ask for: T7 measures BOTH the under-limit and the over-limit arm, because a T7 restricted to the sentence it was given would stay GREEN under the very mutation G11 ordered it to fail — the worker read the gate against the test and fixed the test, which is the reading §3 checklist item 18 exists to force. The second is a REVIEWER DEFECT, and it is a RECURRENCE OF R-0425 rather than a new id, because §3 checklist item 30 requires the open set searched for the DEFECT before minting one and R-0425 already holds this exact class with a standing rule binding the reviewer: a line number written into a record is read back off the file at that line before it is emitted. DEC2 cites `packages/orchestration/pingpong_job.py:2887` for the claim that ping-pong already logs through `RunLogWriter` with a sixteen-character id, and line 2887 is the `def _append_job_stopped_event` line while the `RunLogWriter(` construction it means is at `:2903`. Measured at `7f6033ca`, so the claim is TRUE — the function named is the function that does it — and only the granularity is loose; the reviewer took that number from a range in a search result and did not read the line back, which is precisely what R-0425 forbids. LOW, and R-0425 STAYS OPEN. THE VERDICT IS PASS: every numeral R5 states reproduced under the reviewer's own measurement, all three mutations went red including the one nobody ordered, no id moved, no path outside the declared Change set was touched, and the feature's first production commit landed with its catalog pin, its regression tests and its red proofs in the same commit.
<<<END GATE5

<<<SLICE DEC3
## DECISION F022 D3 (2026-08-23) — the tick's figures cross the envelope, for that kind alone and through a whitelist

CONTEXT, measured by the reviewer at `9b854cf5` by applying this change end to end in a disposable worktree before this block was written. DECISION F022 D1 ruled the tick's payload and DECISION F022 D2 ruled its writer. Neither reached the transport, and the transport is where the payload stopped: `_safe_event_summary` at `packages/orchestration/ui_server.py` returns exactly `{seq, event, timestamp, outcome, task_id}` and drops the event's `metadata`, which is where every figure D1 rules lives. Until this round a client subscribing to the stream received `budget.tick` frames carrying no spend, no limit and no basis — a correct payload nobody could render.

CHOSEN (1), THE WIDENING IS CONDITIONAL ON THE EVENT KIND. The summary gains its extra key for `budget.tick` and for nothing else, so every other kind's frame is byte-identical to what it was. This is not caution for its own sake: `tests/ui_server/test_sse_stream.py` asserts the summary's key set with an exact set equality, and it pins a GOLDEN BYTE STREAM that it rebuilds from the frame writers rather than transcribing, so the golden cannot be edited into agreement without a code change. Measured: the key-set assertion feeds the summary an event named `x` and the golden's events are named `e0` and `e1`, so neither is a tick, and with the conditional widening applied both files stay green at 66 and 100 passed. An unconditional widening turns both red in the same commit as a new feature, which would leave two independent changes sharing one failure.

CHOSEN (2), THE PAYLOAD IS WHITELISTED KEY BY KEY, AT BOTH LEVELS. The `safe` in `_safe_event_summary` is load-bearing — it is a redaction boundary, and this repository carries a `redaction_patterns` module of forbidden field names and secret patterns because event metadata is not trusted input. Passing a tick's metadata through wholesale would make any key a run-log writer ever placed on a tick reachable by any stream subscriber. The outer fields D1 rules are copied by name, and the two keys inside `basis` are copied by name as well, because a nested pass-through is the same leak one level down. Measured in the worktree: a plausible secret placed in a tick's metadata does not appear anywhere in the serialised summary, and neither does an unnamed key placed inside `basis`.

CHOSEN (3), AN ABSENT KEY STAYS ABSENT AND A MALFORMED TICK YIELDS AN EMPTY PAYLOAD. No default, no null and no zero is supplied for a limit the tick never carried, so the acceptance criterion that a limitless job never renders a fabricated denominator survives the last hop as well as the first. A tick with no metadata, or with metadata that is not a dict, produces an empty payload and raises nothing: the summary is built for every event on the stream and may not fail on one.

CHOSEN (4), NO CLIENT CHANGE THIS ROUND. The TypeScript envelope type and the COST metric that reads it are T002's work. Landing them here would put a UI slice in the same commit as a transport change and would mix the two rounds' evidence.

ALTERNATIVES CONSIDERED. Widen unconditionally and update the two pins: rejected under (1), and rejected more strongly because the golden exists to make a wire-format change a deliberate edit, so editing it to accommodate an incidental one is exactly the discipline it was built to enforce. Send the whole metadata dict for ticks only: rejected under (2) — the condition limits WHICH events leak, not WHAT leaks from them. Add a second endpoint for tick figures rather than widening the envelope: rejected, the summary's docstring records that the cursor endpoint and the SSE stream are one consumer contract over two transports with ONE writer, and a second endpoint would give the ticker a different resume story from the feed it rides beside. Have the client re-read the ledger for figures it saw a tick for: rejected, it turns one push into a poll and reintroduces the client-side arithmetic D1's clause four forbids.

REVERSE IT by deleting the conditional branch and its whitelist helper together; nothing else in the summary changes and every existing frame is already unaffected. Ruling (2) survives any reversal of (1) that keeps a payload at all, and rulings (3) and (4) are independent of both.
<<<END DEC3
