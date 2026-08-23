── STEP T001a/3 — F022 Live cost ticker · Runde 5 ────────────────────────────

Fortschritt: ~15 % (T001 halb — R5 baut die Emission, R6 den Umschlag · T002
             offen · T003 offen; ab hier entsteht Produktionscode, der Bauplan
             steht seit R4 fest) — Schaetzung

Goal:        Record the R4 verdict, split T001 across two rounds in the round
             map, rule the tick's WRITER as DECISION F022 D2, and build the
             first half of T001: one budget tick per safe-point evaluation in
             `should_stop`, its humanize-catalog key in the SAME commit, and a
             backend test file pinning the payload's honesty and the cadence.

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the plan ·
             C2 the R4 verdict and the map repair · C3 DECISION F022 D2 ·
             C4 the emission, the catalog key and the backend tests · C5 the
             handback.

Change:      Exactly these paths, nothing else:
               .agent/authored/f022-r5.md        (C0a)
               .agent/last_block.md              (C0b)
               .agent/plan.md                    (C1)
               .agent/live_review.md             (C2)
               .agent/decisions.md               (C3)
               packages/orchestration/safe_points.py        (C4)
               apps/ui/src/api/humanizeCatalog.ts           (C4)
               tests/orchestration/test_budget_tick.py      (C4, new file)
               .agent/handoff.md                 (C5)

─── Slice convention ──────────────────────────────────────────────────────────
Each authored text below begins at its `<<<SLICE <name>` line and ends at its
`<<<END <name>` line; neither marker line is part of the slice, and no slice
contains a marker line. Extract them PROGRAMMATICALLY by marker line out of the
committed C0a blob — never retype, never rewrap, never reflow. The slices are
PLANF022R5, STEPSF022R5-FROM, STEPSF022R5-TO, GATE4 and DEC2.

Constraints:
 1. NEVER edit a slice. Apply it byte for byte. If a slice contradicts a fact
    you measure, apply it anyway and DECLARE the contradiction in the handback
    under Deviations. Repair nothing outside your slices; rule on nothing.
 2. C1 is the FIRST substantive commit (§3 checklist item 23): this round
    touches the finding ledger, so the plan advances before anything else but
    the two block-save commits.
 3. `.agent/plan.md` and the map pair are WHOLE-TEXT and FROM/TO respectively.
    Containment measured mechanically at emission, one reading per pair:
      STEPSF022R5: TO contains FROM: false  → REWRITE, so order the FROM-0x /
      TO-1x proof for it.
    GATE4 and DEC2 are APPENDS to append-only records: never rewrite a landed
    paragraph in either file, and add nothing to them beyond the slice.
 4. C2 both REWRITES (the map pair) and APPENDS (GATE4) in one commit, which is
    the shape R3's C2 already proved. Prove it by RECONSTRUCTION, which is
    strictly stronger than a prefix reading: take the round-base blob of
    `.agent/live_review.md`, replace the FROM string exactly once by the TO
    string, then append one newline plus GATE4 plus one newline, and require
    the result BYTE-EQUAL to the committed file.
 5. C4 is ONE commit and may not be split. The humanize catalog is pinned EQUAL
    to the Python stream vocabulary by
    `tests/ui_contracts/test_humanize_catalog.py`, so an emitter landing
    without its catalog key — or a key landing without its emitter — is a red
    suite at that commit. DECISION F022 D1 already binds this.
 6. Do not touch budget ENFORCEMENT, the pricing and basis rules, or
    MetricsBar's other metrics. `should_stop`'s return values, its reasons and
    its sources are unchanged by this round: the tick is a NOTIFICATION beside
    the decision, never an input to it.
 7. Destructive verification runs ONLY inside a disposable worktree under
    `.remedy-wt/`. The primary checkout satisfies `git status --porcelain`
    empty at every commit and at the handback.
 8. Every numeral this block states about the ROUND BASE `94694b3f` was
    measured by the reviewer at that commit and is a REFERENCE to report
    against, not a target to reproduce. Where your measurement differs, report
    BOTH and reconcile NOTHING.
 9. Size, measured by the reviewer on the final bytes of this block and stated
    once here: this block is 366 lines TOTAL with 67 CONTENT lines inside its
    slices, so PROSE is 299 — under DECISION F085 D6's 490 and D5's 400.

─── What R5 builds, and the four things that will go wrong if you improvise ───

The tick emits in `should_stop`
(`packages/orchestration/safe_points.py`), immediately after the
`evaluate_budget` call and BEFORE the `if evaluation.exhausted` test, exactly as
DECISION F022 D1 rules. The reviewer built this change end to end in a
disposable worktree at the round base before writing this block, and the four
constraints below are each a measured failure that dry run produced or avoided.
Take them as orders, not as suggestions.

(a) THE WRITER IS `RunLogWriter`, NOT `timeline.append_run_event`. Every other
one-shot emitter in this repository takes the short route through
`append_run_event`, and that route is WRONG here. It resolves its id with
`UUID(str(job_id))`, while a JobPlan's `job_id` is `uuid4().hex[:16]` —
sixteen hex characters, which `UUID()` rejects with `ValueError`. Taking the
short route would raise on every ping-pong safe point, the soft failure in (d)
would swallow it, and the ticker would be silently dead on the one job shape
that runs long enough to need it. `RunLogWriter.__init__` only ever does
`str(job_id)`, and it is the same writer ping-pong already logs through.

(b) THE EVENT NAME IS AN INLINE STRING LITERAL AT THE CALL SITE, never a module
constant. `tests/ui_contracts/test_humanize_catalog.py` derives the Python
stream vocabulary with an AST walk that keeps a name only when it is an
`ast.Constant` string in the emitting call. A module constant is an `ast.Name`
and is invisible to it, so the catalog key would sit unpaired and the pin would
go red — the `command.accepted` constant escapes that only through a hard-coded
hatch that names `ui_server.py` and reaches nothing else.

(c) ALL OF A JOB'S TICKS SHARE ONE RUN-LOG FILE. `RunLogWriter` mints a fresh
run id per instance and this emitter is constructed per evaluation, so a long
job would otherwise leave one `.jsonl` file per safe point. Pass a stable run id
instead. Nothing parses a run-log file name — `load_run_events` globs `*.jsonl`
and sorts by timestamp — so the stable name costs nothing.

(d) IT FAILS SOFT, for the reason `_emit_command_accepted_event` does: a
notification that breaks the run it reports on is worse than a missing frame.
Catch `(OSError, RuntimeError, ValueError, TypeError)` around the write and
return. `should_stop`'s own result is unaffected either way.

─── The payload, which DECISION F022 D1 already fixed ─────────────────────────

Absolute values only; a key exists only when its value does. `spent_tokens` and
`unmeasured_calls` always, from the evaluation's counters. `spent_usd` only when
`measured_cost_usd` is not None. `limit_tokens` and `limit_usd` only when the
configured limits carry `max_total_tokens` and `max_cost_usd` respectively. An
absent limit is an ABSENT KEY, never null and never zero — that is what makes
the acceptance criterion "the limitless variant never fabricates a denominator"
a property of the envelope rather than of the client's care.

`basis` is an object with one key per figure. `tokens` reads `lower_bound` when
the evaluation's `token_lower_bound` is true and `actual` otherwise. `cost`
reads `absent` when there is no cost figure at all, `lower_bound` when
`cost_lower_bound` is true, and `actual` otherwise. No display sentence is
transported; the feature file's basis strings are composed in the client.

No payload key may collide with a named parameter of `RunLogWriter.log`
(`task_id`, `artifact_id`, `provider`, `role`, `model`, `outcome`, `message`).
A colliding key would be hijacked out of `metadata` into the event envelope.
None of the keys above collides; a test below pins that.

─── The backend tests ─────────────────────────────────────────────────────────

New file `tests/orchestration/test_budget_tick.py`, written by you, following
the conventions of `tests/orchestration/test_safe_points.py` — a module
docstring naming the feature, `tmp_path` fixtures, and a control root of the
test's own so nothing touches a developer's data dir. Point the data root at
`tmp_path` via the `REMEDY_DATA_DIR` environment variable with `monkeypatch`.
Every test below is REQUIRED and each must be able to fail:

 T1  A priced job with both limits configured emits exactly ONE tick per
     `should_stop` call, and its payload carries `spent_tokens`, `spent_usd`,
     `limit_tokens`, `limit_usd`, `unmeasured_calls` and a `basis` of
     `actual`/`actual`.
 T2  A job whose only limit is a non-money one emits a tick whose payload has
     NEITHER a `limit_usd` KEY nor a `spent_usd` KEY — assert key ABSENCE, not
     a null and not a zero — and whose `basis.cost` is `absent`.
 T3  `budgets=None` or `counters=None` emits NOTHING: no evaluation, no figure.
 T4  Unmeasured provider calls make `basis.tokens` read `lower_bound` and carry
     the count in `unmeasured_calls`.
 T5  An unpriced cost figure makes `basis.cost` read `lower_bound`.
 T6  A job id of the ping-pong shape — `uuid4().hex[:16]`, not a UUID — emits a
     tick. This is (a)'s regression test and it is the most valuable one here:
     it fails if anyone ever routes the emission through `append_run_event`.
 T7  An EXHAUSTED budget still emits its tick, and `should_stop` still returns
     `should_stop=True` with its unchanged reason and source. This is D1's
     "above the exhaustion test" ruling, pinned.
 T8  Three consecutive `should_stop` calls for one job produce three ticks in
     ONE `.jsonl` file. This is (c), pinned.
 T9  A write that raises is swallowed: monkeypatch the writer to raise `OSError`
     and assert `should_stop` returns its normal result. This is (d), pinned.
 T10 No payload key collides with a named parameter of `RunLogWriter.log`:
     assert the payload's key set is disjoint from that parameter set, reading
     the parameter names out of the function's own signature with `inspect` so
     the test tracks the signature instead of a transcription of it.

Note for T1-T8: `BudgetCounters` validates itself. `measured_call_count > 0`
requires a non-empty `actual_sources`, and every member must be in
`VALID_ACTUAL_SOURCES` (`token_actuals` is one). The reviewer lost two probe
runs to that; you need not.

─── Done when ─────────────────────────────────────────────────────────────────

Run every gate below yourself, record its REAL exit code, and put ONE LINE per
gate in the handback with the transcripts kept out of it (R-0582). Gates G1
through G14 run after C4 and BEFORE C5, so the handback can quote all of them
(§3 checklist item 31). The round base is `94694b3f` throughout.

 G1  `.agent/STOP` absent, read from disk before C0a and again before C5.
     Branch `feature/f022-live-cost-ticker`. `git status --porcelain` 0 lines
     after every one of C0a, C0b, C1, C2, C3 and C4.
 G2  TRANSPORT. sha256 over the block file the reviewer wrote at
     `.remedy-wt/f022-r5.md`, over the committed C0a blob, over the committed
     C0b blob and over `.agent/last_block.md` on disk: report all four digests,
     all four byte counts and all four line counts, and require them EQUAL. The
     digest the delegation names is the fifth reading and must agree.
 G3  EXTRACTION. Run an extractor over the COMMITTED C0a blob that finds the
     slices by their marker LINES and report how many slices and how many
     CONTENT lines it printed, plus the block's TOTAL and PROSE line counts.
     Report those against constraint 9's numerals; reconcile nothing.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF022R5 plus exactly one
     newline. NEGATIVE CONTROL: the same comparison against the BARE slice must
     be FALSE, and report both byte counts. `^## Goal$` once, `^## Next Steps$`
     once, `wc -l` at most 50.
 G5  RECONSTRUCTION at C2, per constraint 4. Report the byte equality, plus the
     FROM string counted in the round-base blob and at C2 (expect 1 then 0) and
     the TO string counted at both (expect 0 then 1). NEGATIVE CONTROL: inside
     a disposable worktree, flip ONE byte of the reconstructed text at an offset
     you name and confirm the equality FAILS; report the offset and the two
     bytes. Remove the worktree; `git worktree list` back to one line.
 G6  APPEND at C3. The round-base blob of `.agent/decisions.md` is a byte-exact
     PREFIX of the file at C3, and the remainder is exactly one newline plus
     DEC2 plus one newline; report the remainder's byte count and DEC2's. Then
     an INDEPENDENT reader: split both files on blank lines, report the unit
     counts before and after, and require the LAST unit at C3 equal to DEC2's
     own last paragraph. Lines beginning `## DECISION F022 D2 ` must count 1.
 G7  LEDGER INTEGRITY, base versus C2. Report for both points: the count of
     lines matching `^- R-\d+ — `, whether they are all DISTINCT, the MAXIMUM
     id, the count of `^Done: R-`, of `^Landed: `, and of `^Gate: R` with its
     distinct keys. Report the ids ADDED and the ids REMOVED as sets. At base
     the reviewer measured 230 records, all distinct, maximum `R-0669`, 0 and 0
     for Done and Landed, and 4 `Gate:` lines with 4 distinct keys.
 G8  `^## Steps$` occurs exactly once in `.agent/live_review.md` at C2, and the
     map's arrow `→` count is reported at base and at C2 for that file and for
     `.agent/plan.md`.
 G9  RUFF, the repository's own configuration and NOT `--isolated`:
     `python3 -m ruff check packages/orchestration/safe_points.py
     tests/orchestration/test_budget_tick.py` at C4, exit 0. Pair it with a RED
     CONTROL inside the disposable worktree — add a file whose only line is an
     unused import, confirm ruff exits non-zero on it, delete it — and report
     both exit codes, because a linter that cannot fail proves nothing.
 G10 THE CATALOG PIN, which no F022 round before this one has gated:
     `python3 -m pytest tests/ui_contracts/test_humanize_catalog.py -q` at C4,
     exit 0. Then, inside the disposable worktree at C4, DELETE the single
     catalog line whose key is the tick's and re-run it: report the exit code
     and the failing test's name. Restore the worktree or discard it. At the
     round base the reviewer measured this suite green at 9 passed with a
     vocabulary of 83 keys; report the count you measure at C4.
 G11 THE NEW BACKEND TESTS: `python3 -m pytest
     tests/orchestration/test_budget_tick.py -q` at C4, exit 0, and report the
     passed count and the node ids. Then RED-PROOF the two orders that matter,
     each inside the disposable worktree, each reverted before the next:
       (i)  route the emission through `timeline.append_run_event` instead of
            `RunLogWriter` and report WHICH tests fail — T6 must be among them.
       (ii) move the emission INSIDE the `if evaluation.exhausted:` branch and
            report which fail — T7 must be among them.
     Report the colour you observed. If either mutation leaves the file GREEN,
     say so plainly: that is a defect of the tests and it is worth more to this
     feature than a green line.
 G12 NO REGRESSION on the paths this change sits in, serially in the PRIMARY
     checkout, at C4, each exit 0 with its passed count reported:
     `tests/orchestration/test_safe_points.py`,
     `tests/orchestration/test_budget_stop_integration.py`,
     `tests/orchestration/test_job_budgets.py`,
     `tests/orchestration/test_long_run_executor.py`,
     `tests/orchestration/test_predictive_budget.py` and
     `tests/ui_server/test_sse_stream.py`. At the round base the reviewer
     measured 78, 39, 135, 74, 75 and 66 for these six. Never run two pytest
     processes at once; this repository's runtime suites bind ports and a
     parallel run produces false reds.
 G13 THE FOUR STATE READERS, serially, at C4, exit 0: `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py` and
     `tests/orchestration/test_integrity_gate.py`. The reviewer measured 528
     passed at the round base.
 G14 THE CANARY at C4: `python3 -m pytest tests/cli/test_golden_path.py -q`,
     exit 0. The reviewer measured 42 passed at the round base.
 G15 STRUCTURE, reported for the commits BEFORE C5 and for the range as a whole
     (C5's own numbers belong to the next round's ledger entry, not here):
     every commit single-parent; each commit's INSERTION count, each under the
     500 cap; the range path set EQUAL to the Change set above with the
     difference reported in BOTH directions; `git show --numstat` agreeing cell
     by cell with the handback's `## Commits` table; lines beginning `<<<SLICE `
     or `<<<END ` counting 0 in every file a slice landed in; `git ls-files
     .remedy-wt` 0; one worktree; and the round's reflog rows with the counts of
     amend, rebase and cherry, each of which must be 0.
 G16 `gh pr list --state open --json number,headRefName`. Report it verbatim.
     Create no PR and merge nothing this round.
 G17 STALENESS. Every sentence C1 through C4 land that states a fact about a
     file is re-measured at C4, and any that has gone stale is reported as a
     residual rather than repaired. Report explicitly that you checked, and
     name any residual you find. Slices are NEVER edited to fix one.

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             every mandated section in order, one changed-files table per
             commit, an item-status row per Bundle item, the round base SHA,
             ONE line per gate, and the `Fortschritt:` block above carried
             VERBATIM across all three of its lines. The cap is 100 lines for
             this commit count; declare a DECISION D15 stated cause if the
             mandated content genuinely does not fit.
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF022R5
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
R5 records the R4 verdict, splits T001 across two rounds in the round map, rules
the tick's writer as DECISION F022 D2, and builds the first half: one budget
tick per safe-point evaluation in `should_stop`, the matching humanize-catalog
key in the SAME commit, and a backend test file pinning the payload's honesty,
the cadence and the ping-pong job-id shape.

## Next Steps
1. R6 the second half of T001 — the SSE envelope, which drops `metadata` today
   and therefore carries none of the tick's figures to any client.
2. R7 T002 the COST metric on fixture streams; R8 T003 the terminal
   reconciliation and the delta labelling.
3. R9 the integration gate, then closure.

## Risks
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks rather than F022
  defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- R6 widens `_safe_event_summary`, whose key set is pinned exactly and whose
  frames are a golden byte stream, both in `tests/ui_server/test_sse_stream.py`.
  The widening is conditional on the event kind or both readings go red.
- R7 widens a CLOSED union and a value type with nowhere to put a limit or a
  basis, both measured in the R3 inventory. That is a type-level change.
<<<END PLANF022R5

<<<SLICE STEPSF022R5-FROM
as a DECISION → R5 T001 the tick emission → R6 T002 the COST metric → R7 T003
the terminal reconciliation and the delta labelling → R8 the integration gate →
R9 closure.
<<<END STEPSF022R5-FROM

<<<SLICE STEPSF022R5-TO
as a DECISION → R5 T001a the tick emission in `should_stop`, its
humanize-catalog key and its backend tests → R6 T001b the SSE envelope, which
carries none of the tick's figures today → R7 T002 the COST metric → R8 T003
the terminal reconciliation and the delta labelling → R9 the integration gate →
R10 closure.
<<<END STEPSF022R5-TO

<<<SLICE GATE4
Gate: R4 — the F022 R4 entry. R4 PASSED ON EVERY ONE OF ITS SEVENTEEN GATES, AND THE REVIEWER RE-RAN THE MEASURABLE ONES ITSELF RATHER THAN READING THEM. TRANSPORT HELD: `.agent/authored/f022-r4.md` at `43558c78`, `.agent/last_block.md` at `dbe1f01d` and both files on disk are all sha256 `3bd226db72ab54c5529af1b787bf3ccb06e9264a8cbe567ed2f7a902f6330354` over 31028 bytes and 306 lines, which is the digest the R4 handback names. THE EXTRACTION out of the committed C0a blob printed 4 slices over 103 CONTENT lines, so TOTAL re-measures at 306 under DECISION F085 D6's 490 and PROSE at 203 under D5's 400 — 203 being TOTAL minus the slices' content, with the marker lines counting as prose, which is the convention this record has used since F085. THE WHOLE-FILE REPLACEMENTS ARE BYTE-EQUAL DISK TO DISK, each against the slice extracted from the committed blob and each with a negative control against the bare slice that DIFFERS: `.agent/plan.md` at `aa3a076a` at 2046 bytes against the bare slice's 2045, and `.agent/context.md` at `3c7afdf9` at 2294 against 2293. THE TWO APPENDS ARE PROVED TWICE OVER: the round-base blob is a byte-exact PREFIX in both, the `.agent/live_review.md` remainder is 7705 bytes which is exactly one newline plus GATE3's 7703 plus one newline, the `.agent/decisions.md` remainder is 5852 which is one plus DEC1's 5850 plus one, and an independent blank-line splitter reads 253 units to 254 in the first with the last equal to GATE3 exactly, and 1252 to 1261 in the second with the last equal to DEC1's own last paragraph. `## DECISION F022 D1 ` counts 1. THE SETS ARE UNCHANGED WHERE THE ROUND PROMISED: 230 records all DISTINCT at base and at C2, maximum id `R-0669` at both, `^Done: R-` 0, `^Landed: ` 0, ids added and ids removed BOTH the empty set, and `^Gate: R` moving 3 to 4 with the distinct keys gaining `Gate: R3` beside `Gate: R41`, `Gate: R1` and `Gate: R2`. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout: the four state readers exit 0 at 528 passed, `tests/ui_contracts/test_humanize_catalog.py` exit 0 at 9 passed, and the canary `tests/cli/test_golden_path.py` exit 0 at 42 passed — every one matching the figure the block stated at `33a0c6c1`. STRUCTURE HELD: seven commits over `33a0c6c1`..`94694b3f`, every one single-parent, insertions 306, 163, 13, 2, 18, 10 and 55, each under the 500 cap; the range path set holds 7 paths and the per-commit union differs from it in NEITHER direction; 0 paths beginning `packages/`, `apps/`, `tests/` or `docs/`; `git ls-files .remedy-wt` 0; one worktree; `git status --porcelain` empty; and 0 amend, 0 rebase and 0 cherry across the reflog rows. THE `## Commits` TABLE AGREES CELL BY CELL with `git diff-tree --numstat` for all six tabled commits, which is §3 checklist item 28's reading and the half a later session actually reads. DECISION F022 D1 WAS AUDITED RATHER THAN ACCEPTED, because a ruling that cites twenty file:line pointers is twenty claims: every one of them resolves at `3c7afdf9`, including the three whose claim spans more than one line — the operator-stop `return ShouldStopResult(` at `safe_points.py:606` really does precede the budget block at `:613`, the "floor, not a total" comment really does sit at `budget_guard.py:224` directly above `cost_lower_bound` at `:225`, and `_LIMIT_ORDER` at `:245` really does fix five limit kinds with `max_cost_usd` among them. Zero unresolved. THE STALENESS SWEEP REPRODUCES IN FULL: the severity-anchored `^- R-\d+ — High` set is exactly two ids and exactly `R-0495` and `R-0574`; an AST Call predicate over 975 tracked `.py` files finds exactly 4 production call sites of `evaluate_budget` at exactly the cited lines, with 47 under `tests/` and 51 repo-wide; `^## Steps$` occurs once; and GATE3's own claims re-measure exactly — seven commits over `66f87edc`..`33a0c6c1` with insertions 294, 224, 12, 12, 4, 246 and 83, and FIFTEEN gate labels in the R3 block. THE R-0553 RECURRENCE THE ROUND DECLARED IS REAL AND ITS REPAIR LANDED: at `aead9822` the round-number tokens of `.agent/context.md` were exactly `['R2']`, sitting inside the very clause that denied naming any, and at `3c7afdf9` that set is EMPTY while the arrow count stays 0 — so CONTEXTF022R4 replaced the false clause with one that makes no claim about its own contents, which is R-0553's own counter-measure rather than a rewrite of landed text. R-0553 STAYS OPEN, because a recurrence is evidence added to an open finding and not a resolution. THE HANDBACK IS COMPLIANT: 97 lines against the 100 the seven-commit case allows, every mandated section of docs/agents/handback_template.md present and in order, an item-status row per Bundle commit, one line per gate, and the block's three-line `Fortschritt:` carried VERBATIM. ONE THING IS OWED FORWARD AND IS NOT A DEFECT OF R4: the round routed its raw transcripts to a "round report", which under docs/agents/self_drive_protocol.md is a channel that ends with the session, so §3 checklist item 31 puts the duty of preserving those numbers on the reviewer — this entry is where they now live, and every figure above is one the reviewer measured rather than one it copied. THE VERDICT IS PASS: no numeral R4 states failed to reproduce, no id moved, no production path was touched, and the round's one job — turning the R3 inventory into a ruling the build can stand on — is done.
<<<END GATE4

<<<SLICE DEC2
## DECISION F022 D2 (2026-08-23) — the tick's WRITER, its file, and the transport gap D1 did not reach

CONTEXT, measured by the reviewer at `94694b3f` by building the change end to end in a disposable worktree before this block was written. DECISION F022 D1 ruled WHERE the tick emits and WHAT it carries. It ruled neither HOW it is written nor whether what it carries survives the journey to a client, and both gaps are load-bearing: the first would have shipped a ticker that is silently dead on the main long-running job shape, and the second is the difference between a feature and an event nobody can render.

CHOSEN (1), THE WRITER IS `RunLogWriter` AND NOT `timeline.append_run_event`. Every other one-shot emitter in this repository — `_emit_command_accepted_event` at `packages/orchestration/ui_server.py:3619` is the model — takes the short route through `append_run_event`, and that route cannot serve this call site. `append_run_event` resolves its id with `UUID(str(job_id))` at `packages/orchestration/timeline.py:63`, while a JobPlan's `job_id` is `uuid4().hex[:16]` at `packages/orchestration/pingpong_job.py:205` — sixteen hex characters, which `UUID()` rejects with `ValueError`. Measured in the worktree: the ping-pong shaped id emits ONE tick through `RunLogWriter` and would have emitted NONE through `append_run_event`, and because the emission fails soft the loss would have been silent. `RunLogWriter.__init__` does only `str(job_id)` at `packages/orchestration/run_log.py:112`, and `packages/orchestration/pingpong_job.py:2887` already logs through it with exactly that id, so this is the repository's own precedent rather than a new mechanism.

CHOSEN (2), THE EVENT NAME IS AN INLINE LITERAL AT THE CALL SITE. `tests/ui_contracts/test_humanize_catalog.py` builds the Python stream vocabulary by an AST walk whose `_event_argument` keeps a name only when it is an `ast.Constant` string, so a module constant is an `ast.Name` and is invisible to it. `command.accepted` survives as a constant only through a hard-coded hatch that names `ui_server.py` and reaches nothing else. Measured: with the literal inline the derived vocabulary moves from 83 kinds to 84 and equals the catalog exactly; with the catalog line deleted the pin fails naming `budget.tick`, so the pin is not merely green, it BITES.

CHOSEN (3), ALL OF A JOB'S TICKS SHARE ONE RUN-LOG FILE. `RunLogWriter` mints a fresh run id per instance and the emitter is constructed per evaluation, so the default would leave one `.jsonl` file per safe point for the length of a long job. A stable run id is passed instead. Nothing in this repository parses a run-log file name — `load_run_events` at `packages/orchestration/timeline.py:79` globs `*.jsonl` and sorts by timestamp — so the stable name costs nothing and was measured to produce exactly one file per job across the probe runs.

CHOSEN (4), IT FAILS SOFT AND THE ROUND'S TESTS PIN THAT IT DOES. A notification that breaks the run it reports on is worse than a missing frame, which is `_emit_command_accepted_event`'s own stated reason. Note a consequence rather than a bug, measured at the base and unchanged by this round: `apps/cli/commands/do_cmd.py:793` calls `should_stop` with an EMPTY job id, and that call raises `StopControlError` out of `validate_job_id` BEFORE the budget block is reached — at the base commit as well as after this change. That path therefore evaluates no budget and emits no tick, and it did not begin doing so here. It is recorded as an open question for the branch that owns that file, not as F022 work.

THE GAP THIS DECISION OPENS AND R6 CLOSES. `_safe_event_summary` at `packages/orchestration/ui_server.py:2748` returns exactly `{seq, event, timestamp, outcome, task_id}` and DROPS the event's `metadata`, which is where every figure D1 ruled lives. A client subscribing to the stream today would receive `budget.tick` frames carrying no spend, no limit and no basis, so D1's payload is correct and, on its own, unreachable. That is not a defect of D1 and it is not repaired here: the summary's key set is pinned by an exact equality at `tests/ui_server/test_sse_stream.py:90` and its frames are a golden byte stream at `:353`, so widening it unconditionally turns both red. R6 widens it CONDITIONALLY, by event kind, which leaves every existing frame byte-identical and both pins green. The round map is split accordingly and `.agent/plan.md` carries the risk.

ALTERNATIVES CONSIDERED. Route through `append_run_event` and normalise the job id to a UUID first: rejected, it would invent an identity the rest of the run log does not use and would break the join with ping-pong's own events. Give each tick its own run id, as every other writer does: rejected, those writers are one-per-invocation while this one is one-per-safe-point, and the file count is unbounded in the length of the job. Emit the display sentence on the wire so the client needs no basis object: rejected by D1 already, and rejected again here because it would move copy into the backend. Widen `_safe_event_summary` unconditionally in this round: rejected, it turns an exact key-set pin and a golden byte stream red in the same commit as a new emitter, which would leave two independent changes sharing one red and no way to tell which caused it.

REVERSE IT by deleting the emitter, its call and the catalog key together — they are pinned equal and none can drift alone — which also reverses D1's clause (1). Rulings (2), (3) and (4) reverse independently of the writer choice in (1). The transport paragraph rules nothing yet; it records a measured gap and names the round that closes it.
<<<END DEC2
