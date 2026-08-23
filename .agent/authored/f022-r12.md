── STEP T003b-a/3 — F022 Live cost ticker · Runde 12 ─────────────────────────

Fortschritt: ~80 % (T001 fertig · T002 fertig · T003a fertig · T003b halb —
             diese Runde liefert die Server-Seite der Schluss-Zahl, repariert
             R-0670 und schreibt das R11-Urteil auf Platte) — Schaetzung

Goal:        Serve the ledger's final budget figure. DECISION F022 D7 rules the
             last `budget.tick` in the job's run log as the authority for the
             terminal reconciliation; this round puts it on the dashboard
             payload so the next round's client half has something real to read.
             It also repairs R-0670, whose fix has been waiting for a round that
             touches `ui_server.py` on its own account, and records the R11
             verdict with two recurrences.

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the plan ·
             C2 repair the round map · C3 the R11 verdict and two recurrences ·
             C4 R-0670's comment repair · C5 the final-figure section and its
             tests · C6 resolve R-0670 · C7 the handback.

Change:      Exactly these paths, nothing else:
               .agent/authored/f022-r12.md                     (C0a)
               .agent/last_block.md                            (C0b)
               .agent/plan.md                                  (C1)
               .agent/live_review.md                           (C2, C3, C6)
               packages/orchestration/ui_server.py             (C4, C5)
               tests/ui_server/test_budget_final_section.py    (C5, NEW)
               .agent/handoff.md                               (C7)

─── Slice convention ──────────────────────────────────────────────────────────
Each authored text below begins at its `<<<SLICE <name>` line and ends at its
`<<<END <name>` line; neither marker line is part of the slice, and no slice
contains a marker line. Extract them PROGRAMMATICALLY by marker line out of the
committed C0a blob — never retype, never rewrap, never reflow. The whole-text
slices are PLANF022R12, LEDGER12 and DONE670. MAPFROM12/MAPTO12 and
GUARDFROM/GUARDTO are FROM/TO pairs, and this block carries no other pair. Every
slice is quoted WITHOUT its trailing newline; PLANF022R12 replaces its file
whole, and LEDGER12 and DONE670 each land as one newline plus the slice plus one
newline.

CONTAINMENT TEST, run by the reviewer on the final bytes, output quoted, one
reading per pair and none of it generalised from another:
  MAPFROM12/MAPTO12 — `TO contains FROM: false` → REWRITE.
  GUARDFROM/GUARDTO — `TO contains FROM: false` → REWRITE.

Constraints:
 1. NEVER edit a slice. Apply it byte for byte. If a slice contradicts a fact
    you measure, apply it anyway and DECLARE the contradiction in the handback
    under Deviations. Repair nothing outside your slices; rule on nothing.
 2. C1 is the FIRST substantive commit (§3 checklist item 23): this round
    touches the finding ledger, so the plan advances before anything else but
    the two block-save commits.
 3. COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4, C5, C6, C7 and no other. Within
    `.agent/live_review.md` the pair at C2 precedes both of that file's appends,
    at C3 and C6 (R-0639/R-0640); `packages/orchestration/ui_server.py` carries
    a pair at C4 and no append. C3 lands BEFORE the repair so the findings
    persist first (§4.4a), and C6 lands AFTER it so DONE670 describes work that
    is already on disk — THIS constraint is what makes DONE670's claim true
    (§3 item 20, R-0524 carve-out), and it is why the two ledger appends are
    two commits rather than one.
 4. LEDGER12 holds, in this order and each separated by ONE blank line: the
    `Recurrence: R-0431` paragraph, the `Recurrence: R-0413` paragraph and the
    `Gate: R11` paragraph. It lands in ONE commit, C3, or none of it does.
 5. C5 IS THE ONLY COMMIT THAT ADDS BEHAVIOUR, and it adds exactly one read-only
    section to an existing payload. It changes no existing key, no envelope and
    no event. If a golden or a key-set assertion goes red, that is a real
    finding about the addition and it goes in the handback — do NOT weaken an
    assertion to accommodate it.
 6. NO CLIENT CHANGE. Nothing under `apps/` is in the Change set. The client
    half of T003b — the reconciliation and its delta label — is R13's work and
    the map this block repairs says so.
 7. Destructive verification runs ONLY inside a disposable worktree under
    `.remedy-wt/`. The primary checkout satisfies `git status --porcelain`
    empty at every commit and at the handback. Run no suite concurrently with a
    working-tree reading (R-0479).
 8. Every numeral this block states about the ROUND BASE `f6259860` was produced
    by a reviewer script or tool run at that commit and is a REFERENCE to report
    against, not a target to reproduce. Where your measurement differs, report
    BOTH and reconcile NOTHING.
 9. Size, measured by the reviewer on the final bytes of this block and stated
    once here: this block is 349 lines TOTAL with 69 CONTENT lines inside its
    slices, so PROSE is 280 — under DECISION F085 D6's 490 and D5's 400.

─── What the reviewer measured at `f6259860`, and the change specified ────────

THE FIGURES ARE ALREADY LOADED. `_load_events(job)` returns
`load_run_events(resolve_data_root(), job.id)`, and that function globs EVERY
`*.jsonl` under `runs/<job_id>/` and sorts the result by timestamp. The budget
ticks live in `budget-ticks.jsonl` under exactly that directory, because
`_emit_budget_tick` writes them through `RunLogWriter` with the stable run id
`BUDGET_TICK_RUN_ID`. So the dashboard builder already holds every tick the job
emitted, in timestamp order, and needs no new I/O and no new endpoint — which is
the half of DECISION F022 D7 that makes it cheap.

C4 — R-0670's REPAIR, and it is the pair GUARDFROM/GUARDTO. The
`BUDGET_TICK_EVENT` comment names `tests/ui_contracts/test_humanize_catalog.py`
as the guard that catches a rename of that constant. The finding measured, by
mutation at `f685a707`, that the catalog test is EXIT 0 under exactly that
rename while `tests/ui_server/test_budget_tick_envelope.py` is EXIT 1 — the
named guard is blind to the drift the sentence promises it catches. The pair
names the guard that was MEASURED to catch it. Nothing but the comment changes.

C5 — THE FINAL-FIGURE SECTION. Add one module-level function to
`packages/orchestration/ui_server.py`, beside the other `_build_*` section
builders, and one key to the dashboard dict `_build_dashboard` returns:

  `_build_budget_final(events)` returns the whitelisted payload of the LAST
  event whose `event` field equals `BUDGET_TICK_EVENT`, and `None` when the job
  emitted no tick. "Last" is the last in the list, because `load_run_events`
  has already sorted by timestamp — say so in the comment rather than re-sorting,
  and name the function that guarantees it. It reuses
  `_budget_tick_summary_payload` and adds NO field of its own: the whitelist is
  a redaction boundary (DECISION F022 D3 clause two) and a second projection
  beside it would be a second place for a key to leak. A job with no tick yields
  `None` and NEVER an empty object or a zero — an absent figure is absent, which
  is the same honesty rule that stops a limitless job rendering a denominator.

  The dashboard gains `"budget_final": _build_budget_final(events)` beside
  `"token_usage"`. It is ADDITIVE: no existing key changes.

  Carry the one-line WHY above the definition, per AGENTS.md's discoverability
  conventions, and say in it what this figure IS — the ledger's own last word on
  a job's spend, as distinct from `token_usage`, which is an ESTIMATE summed
  from `metadata.estimated_tokens` over a different event population and is not
  a reconciliation source. A reader who confuses the two ships a fabricated
  delta, so the distinction belongs where they would search for it.

  `tests/ui_server/test_budget_final_section.py` is NEW and pins, at minimum:
  the last tick wins when several exist; the payload equals what
  `_budget_tick_summary_payload` returns for that tick's metadata; a job with no
  tick yields `None`; a tick whose metadata carries an unwhitelisted key does
  NOT leak it; and the key is present on the dashboard payload. Write the tests
  in the style of the neighbouring `tests/ui_server/` files.

C6 — DONE670 resolves the finding. It is the reviewer's authored text and the
only thing that sets Resolved (§4.4).

─── Done when ─────────────────────────────────────────────────────────────────

Run every gate below yourself, record its REAL exit code, and put ONE LINE per
gate in the handback with the transcripts kept out of it (R-0582). G1 through
G13 run after C6 and BEFORE C7, so the handback can quote all of them (§3
checklist item 31). The round base is `f6259860` throughout.

 G1  `.agent/STOP` absent, read from disk before C0a and again before C7.
     Branch `feature/f022-live-cost-ticker`. `git status --porcelain` 0 lines
     after every one of C0a through C6.
 G2  TRANSPORT. sha256 over the block file the reviewer wrote at
     `.remedy-wt/f022-r12.md`, over the committed C0a blob, over the committed
     C0b blob and over `.agent/last_block.md` on disk: report all four digests,
     byte counts and line counts, and require them EQUAL. The digest the
     delegation names is the fifth reading and must agree.
 G3  EXTRACTION. Run an extractor over the COMMITTED C0a blob that finds the
     slices by their marker LINES and report how many slices and how many
     CONTENT lines it printed, plus the block's TOTAL and PROSE line counts.
     Report those against constraint 9's numerals; reconcile nothing.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF022R12 plus exactly one
     newline. NEGATIVE CONTROL: the same comparison against the BARE slice must
     be FALSE, and report both byte counts. `^## Goal$` once, `^## Next Steps$`
     once, `wc -l` at most 50.
 G5  THE TWO PAIRS. Report each pair's containment output and require it to
     match the convention block. At C2 in `.agent/live_review.md`: MAPFROM12 1x
     at the round base and 0x at C2, MAPTO12 0x at base and 1x at C2, the byte
     length changing by exactly `len(MAPTO12) - len(MAPFROM12)`, and `^## Steps$`
     still exactly once. At C4 in `packages/orchestration/ui_server.py`:
     GUARDFROM 1x at base and 0x at C4, GUARDTO 0x at base and 1x at C4, and the
     same byte-length identity. Confirm for BOTH that the committed file equals
     the base file with only that replacement applied and nothing else. ALSO
     report the longest line length of the `## Steps` paragraph at C2: no line
     in it may exceed 84 characters, because the R11 map pair left a 99-character
     line where its TO joined the sentence that followed it (R-0431), and this
     pair spans that join precisely so it can fix it.
 G6  APPEND at C3, and the same two readers at C6. For each: the previous
     commit's blob of that file is a byte-exact PREFIX and the remainder is
     exactly one newline plus the slice plus one newline — report the
     remainder's byte count and the slice's. Then an INDEPENDENT reader: split
     both files on blank lines, let N be the number of paragraphs YOUR script
     counts in the slice, and require the LAST N units of the committed file to
     equal the slice's N paragraphs IN ORDER. Report N; do not take it from this
     block. NEGATIVE CONTROL, in a disposable worktree, applied to the FIRST
     appended paragraph of LEDGER12 and to the FIRST of DONE670: flip ONE byte
     at an offset you name and confirm BOTH readers reject each mutant while
     both accept the true file. THE OFFSET IS A BYTE OFFSET — the file carries
     multi-byte em dashes, so a CHARACTER offset lands early, outside the
     appended region, where reader (b) accepts the mutant and the control proves
     nothing. Report the ~20 bytes surrounding each flip. Remove the worktree.
 G7  LEDGER INTEGRITY, base versus C6. Report for both points: the count of
     lines matching `^- R-\d+ — `, whether they are all DISTINCT, the MAXIMUM
     id, the count of `^Done: R-` with its distinct ids, of `^Landed: `, of
     `^Recurrence: R-` with its distinct ids, and of `^Gate: R` with its
     distinct keys. Report the ids ADDED and REMOVED as sets. At base the
     reviewer measured 234 records, all distinct, maximum `R-0673`, 1 `Done:`
     line for `R-0653`, 0 `Landed:`, 5 `Recurrence:` lines and 11 `Gate:` lines
     over 11 distinct keys. This round MINTS NO NEW ID: it is expected to add no
     record, to take `^Recurrence: R-` to 7 by gaining `R-0431` and `R-0413`, to
     add `Gate: R11`, and to take `^Done: R-` to 2 by gaining `R-0670`. Report
     what you measure. `R-0670`, `R-0431` and `R-0413` must each still occur
     exactly once as a `^- R-\d+ — ` record.
 G8  THE MUTATION R-0670 EXISTS FOR, re-run so the repaired comment is not taken
     on trust. In a disposable worktree at C5, rewrite `BUDGET_TICK_EVENT`'s
     value to `"budget.ticks"` and change nothing else, then run BOTH
     `tests/ui_contracts/test_humanize_catalog.py` and
     `tests/ui_server/test_budget_tick_envelope.py` and report each exit code
     and count. The comment the round installs names the SECOND as the guard, so
     the second must be RED and the first is reported whatever it shows. Remove
     the worktree. If the second is green, the repaired comment is as wrong as
     the one it replaced — say so and do not repair it further.
 G9  `python3 -m pytest tests/ui_server/ -q` from the REPOSITORY ROOT, exit 0.
     The reviewer measured 455 passed at the round base; this round adds a test
     file, so report the difference and name what the new file contributes.
 G10 `python3 -m pytest tests/ui_contracts/ -q` from the REPOSITORY ROOT, exit 0.
     The reviewer measured 518 passed and 4 skipped at the round base. Run it
     from the repository root and say so: the same command from `apps/ui`
     collects nothing and exits reporting no failure (R-0463).
 G11 THE FOUR STATE READERS plus THE CANARY, serially in the PRIMARY checkout at
     C6, exit 0: `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py`,
     `tests/orchestration/test_integrity_gate.py`, then
     `tests/cli/test_golden_path.py`. The reviewer measured 544 across the four
     and 42 for the canary at the round base; `tests/ui_server/` moves by
     whatever G9 reports and the other three do not. Never run two pytest
     processes at once.
 G12 STRUCTURE, reported for the commits BEFORE C7 and for the range as a whole
     (C7's own numbers belong to the next round's ledger entry, not here):
     every commit single-parent; each commit's INSERTION count, each under the
     500 cap; the range path set against the Change set above with the
     difference reported in BOTH directions; `git show --numstat` agreeing cell
     by cell with the handback's `## Commits` table; the LINE-ANCHORED patterns
     `^<<<SLICE ` and `^<<<END ` counting 0 in `.agent/plan.md` and
     `.agent/live_review.md`; `git ls-files .remedy-wt` 0; one worktree; and the
     round's reflog rows with amend, rebase and cherry counts, each 0.
 G13 `gh pr list --state open --json number,headRefName`. Report it verbatim.
     Create no PR and merge nothing: T003b's client half is unbuilt and the
     integration gate has not run.
 G14 STALENESS. Every sentence C1 through C6 land that states a fact about a
     file is re-measured at C6, and any that has gone stale is reported as a
     residual rather than repaired. Report explicitly that you checked, and name
     any residual. Slices are NEVER edited to fix one.

NOT A GATE and not run this round: `npm run lint`, `npm run typecheck` and
`npm run test:unit`. The Change set holds no file under `apps/`.

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             every mandated section in order, one changed-files table per
             commit, an item-status row per Bundle item, the round base SHA,
             ONE line per gate, and the `Fortschritt:` block above carried
             VERBATIM across all three of its lines. Every count you report
             names the exact string or pattern counted and the file it was
             counted in (R-0442). The cap is 100 lines for this commit count;
             declare a DECISION D15 stated cause with your own measured numeral
             in the declaring line if the mandated content genuinely does not
             fit. THIS HANDBACK LIKELY ENDS THE SESSION, so its `## Next`
             section names, in this order: (1) Phase 1 rule 1 — re-read
             `.agent/STOP` from disk before anything else; (2) the Open PR Gate;
             (3) R13, the client half of T003b — reading `budget_final` into the
             dashboard type and rendering the terminal reconciliation with its
             delta label, per DECISION F022 D7; (4) that R12's own verdict is
             NOT on disk and R13's ledger commit owes it.
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF022R12
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
R12 is the server half of T003b. It adds one read-only section to the dashboard
payload carrying the ledger's last budget tick, which DECISION F022 D7 rules as
the authority for the terminal reconciliation, and it needs no new endpoint
because the dashboard builder already loads every tick the job emitted. It also
repairs R-0670, whose fix waited for a round that touches `ui_server.py` on its
own account, and records the R11 verdict with two recurrences.

## Next Steps
1. R13 T003b-b — the client half: read `budget_final` into the dashboard type
   and render the terminal reconciliation with its delta label.
2. R14 the integration gate.
3. R15 closure.

## Risks
- The delta R13 renders is a TRANSPORT statement, not arithmetic: both sides are
  the same quantity from the same producer, so a difference means frames were
  missed. A round that reads it as drift would reintroduce the fabricated
  honesty moment DECISION F022 D7 exists to prevent.
- Open F022 findings after this round: R-0672 and R-0625 want their
  next-DECISION and next-numeral clauses honoured; R-0431 and R-0413, recorded
  this round, are reviewer-block defects already paid for.
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks, not F022 defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- R-0665 is open and this feature needs its route: every UI feature is told to
  record visual deviations in an `assumption_log` that does not exist. F022
  records them as DECISIONs in `.agent/decisions.md`, a route rather than a fix.
<<<END PLANF022R12

<<<SLICE MAPFROM12
that does not exist, and record the R10 verdict → R12 T003b the server's
final-figure section and the client's reconciliation with its delta label →
R13 the integration gate → R14 closure. This section is the only place the round map is stated, per
<<<END MAPFROM12

<<<SLICE MAPTO12
that does not exist, and record the R10 verdict → R12 T003b-a the server's
final-figure section, R-0670's repair and the R11 verdict → R13 T003b-b the
client's reconciliation with its delta label → R14 the integration gate → R15
closure. This section is the only place the round map is stated, per
<<<END MAPTO12

<<<SLICE GUARDFROM
#: requires the emitter to pass the name as an INLINE literal so the humanize
#: catalog's AST walk can see it. `tests/ui_contracts/test_humanize_catalog.py`
#: pins that catalog equal to the emitters, so the two spellings cannot drift
#: apart without a red suite.
<<<END GUARDFROM

<<<SLICE GUARDTO
#: requires the emitter to pass the name as an INLINE literal so the humanize
#: catalog's AST walk can see it. The guard against THIS constant drifting from
#: that literal is `tests/ui_server/test_budget_tick_envelope.py`, which was
#: MEASURED to go red when this value is renamed; the humanize-catalog test is
#: not, because it pins the catalog against the emitter's own literal in
#: `packages.orchestration.safe_points` and never reads this constant at all
#: (finding R-0670, measured by mutation at `f685a707`).
<<<END GUARDTO

<<<SLICE LEDGER12
Recurrence: R-0431 — A NARROWED REWRITE PAIR DID NOT REPRODUCE THE WRAP WIDTH OF THE SHAPE IT LANDED IN. Second instance, at F022 R11, in the reviewer's own map pair. NO NEW ID IS MINTED: §3 checklist item 30 requires the open set searched for the DEFECT before an id, and R-0431 already holds this class with the standing rule that a REWRITE pair extends to the whole sentence, bullet or paragraph whose truth value the edit changes, and that a TO slice landing inside a shaped block reproduces that block's continuation indent AND WRAP WIDTH, because a slice is applied into a shape it cannot see. THE INSTANCE: the R11 block's MAPFROM11 ended at `R13 closure.` and the file's own line continued past that point with the sentence that follows the arrow chain, so MAPTO11's last line joined it. MEASURED at `f6259860`: line 53 of `.agent/live_review.md` is 99 characters where every other line of that paragraph is 72 to 80. WHY IT HAPPENED: the pair was NARROWED on purpose, to bring the R11 block under DECISION F085 D6's line cap, and narrowing a pair moves its boundary INTO a line rather than onto one — which is exactly the case R-0431's rule covers and exactly the case the narrowing decision did not re-check. THE CAP AND THE RULE PULL IN OPPOSITE DIRECTIONS and the block honoured only one of them. WHY LOW: nothing is red, the map's TEXT is correct, and the cost is one over-long line in a markdown paragraph that no gate reads and no renderer breaks. THE FIX IS THIS ROUND'S OWN MAP PAIR, whose FROM deliberately spans the join and whose G5 orders the paragraph's longest line reported and bounded — so the repair is measured rather than asserted, and the landed line is corrected by a pair rather than by a rewrite of history. Both instances stay OPEN under R-0431, and the addition this instance earns is one clause: when a pair is narrowed to meet a cap, its FROM ends at a LINE boundary of the target or spans the join, and the block gates the resulting longest line.

Recurrence: R-0413 — A BLOCK CONSTRAINT CONTRADICTED THE COMMIT SEQUENCE THE SAME CONSTRAINT FIXED, IN ONE SENTENCE. Second instance, at F022 R11, found by the WORKER and confirmed by the reviewer by reading the block's own bytes. NO NEW ID IS MINTED: R-0413 holds the clause-versus-clause class, where a block's two halves are each defensible and disagree with each other, and §3 checklist item 30 sends this here rather than to a new id. THE INSTANCE: the R11 block's constraint 3 reads "COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4, C5, C6 and no other. Both pairs are applied before either append reads its file (R-0639/R-0640)." Its own ordered sequence puts the SPEC pair at C5, AFTER the appends at C3 and C4, so the second sentence is false of the first. THE WORKER FOLLOWED THE ORDERED SEQUENCE, which was the right half to obey, and declared the tension rather than resolving it silently. NOTHING WAS ACTUALLY AT RISK, and the reviewer confirms the worker's reasoning: R-0639/R-0640's property is PER FILE — a bulk read must run over a remainder no pair will later change — and `.agent/live_review.md`'s only pair at C2 does precede its C3 append, while `docs/roadmap/features/T5_F022.md` carries a pair and no append at all. So the ordering was correct and only the sentence generalising it was wrong. WHY LOW: no gate could fail, nothing false reached a durable record beyond the block mirror, and the worker's declaration is the whole cost. THE COUNTER-MEASURE, and it is what THIS block's constraint 3 does: state the pair-before-append property PER FILE, naming the file and the commits, rather than as a universal over "both pairs" — a universal across files is a claim nobody checked, which is the R-0526 shape arriving in an ordering clause.

Gate: R11 — the F022 R11 entry. R11 PASSED ON EVERY ONE OF ITS THIRTEEN GATES, AND THE REVIEWER RE-RAN EVERY ONE OF THEM ITSELF. The two recurrences above are written in THIS SAME COMMIT, which the R12 block's constraint 4 fixes. THE ROUND'S SUBSTANCE IS THAT IT REFUSED TO BUILD AGAINST A NAME. The feature file ordered the terminal reconciliation to fetch "the ledger's job figure (the stats endpoint)", and the reviewer measured that `packages/orchestration/ui_server.py` dispatches no such endpoint; it then measured the substitute a builder would most likely reach for and found it worse than useless — `_build_token_usage` sums `metadata.estimated_tokens` over kinds like `source_context_injected` and returns `"estimated": True`, while the ticker's figures are `BudgetCounters.measured_token_total` and `measured_cost_usd`, which count provider calls, so a delta between them would have been a fabricated honesty moment in the one feature built to prevent those. DECISION F022 D7 rules the run log's last `budget.tick` as the authority and C5 amended the feature file to match, which is §4 item 7 working exactly as written: a wrong spec became an authored amendment, a loud persisted DECISION and a reversal path, with nothing waiting on an operator answer. TRANSPORT HELD IN ITS STRONGEST FORM: the reviewer's scratch original, the committed C0a blob, the committed C0b blob, `.agent/last_block.md` on disk and `.agent/authored/f022-r11.md` on disk are ALL sha256 `47a1a3dbe5ee90d582476b60fea355330239c1732fab481297286002f5bbaa0e` over 31617 bytes and 381 lines, and C0a and C0b resolve to the SAME git blob. THE EXTRACTION printed 7 slices over 137 CONTENT lines, TOTAL 381 and PROSE 244, reproducing constraint 9 exactly. `.agent/plan.md` at `7760e77d` is 2607 bytes = PLANF022R11's 2606 plus one newline, the bare-slice control DIFFERING, headings once each, 46 lines against the cap of 50. BOTH PAIRS ARE EXACT AND BOTH PRINTED `TO contains FROM: false`: in `.agent/live_review.md` at `60edc932` MAPFROM11 1→0 and MAPTO11 0→1 with byte delta 177 = 423 − 246; in `docs/roadmap/features/T5_F022.md` at `ae58934d` SPECFROM 1→0 and SPECTO 0→1 with byte delta 547 = 814 − 267; and each committed file equals its base with ONLY that replacement applied. BOTH APPENDS HOLD UNDER BOTH READERS: at `9933144c` the remainder is 8047 = 1 + LEDGER11's 8045 + 1 with N=2 paragraphs equal in order over 267→269 units; at `5ca8c326` the remainder is 3761 = 1 + DEC7's 3759 + 1 with N=7 equal in order over 1303→1310. THE SETS MOVED EXACTLY WHERE THE ROUND PROMISED: 234 records at base and at C3, ids ADDED and REMOVED both the EMPTY SET so NO ID WAS MINTED, `^Recurrence: R-` 4→5 gaining `R-0625`, `^Gate: R` 10→11 gaining the key `R10`, and `^- R-0625 — ` exactly 1 at both. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout: `tests/docs/` 295 and `tests/orchestration/test_roadmap_index.py` 30, both matching the base and both re-run by the reviewer against the amended feature file BEFORE the round was delegated, in a disposable worktree, so the docs gate was known green rather than hoped green; the four state readers 455, 52, 21 and 16 for 544; and the canary 42. STRUCTURE HELD: seven commits before the handback, every one single-parent, insertions 381, 269, 17, 5, 4, 60 and 13, each under the 500 cap; the range path set is exactly the declared seven-path Change set with the difference EMPTY in both directions; `git show --numstat` agrees cell by cell with all seven `## Commits` rows, the full-file `.agent/last_block.md` row reading `+269/-370` in both; anchored markers 0 in all four named files; one worktree; 0 amend, 0 rebase and 0 cherry. THE HANDBACK IS COMPLIANT at 104 lines with a DECISION D15 stated cause naming that same 104, every mandated section present and in order, and the three-line `Fortschritt:` block byte-identical to the block's. THE ROUND'S TWO SUBSTANTIVE DEVIATIONS ARE BOTH CORRECT AND BOTH CORRECT THE REVIEWER — the constraint-3 contradiction is the R-0413 recurrence above and the 99-character map line is the R-0431 recurrence, and the worker found the first by reading the block's own bytes against its own sequence, which is the check no gate in that block performed. THE VERDICT IS PASS: every numeral R11 states reproduced under the reviewer's own measurement, no slice was edited, no id was minted, and the feature's last unbuildable instruction became a ruled, reversible decision with the spec corrected to match it.
<<<END LEDGER12

<<<SLICE DONE670
Done: R-0670 — RESOLVED AT F022 R12 BY NAMING THE GUARD THAT WAS MEASURED. The `BUDGET_TICK_EVENT` comment in `packages/orchestration/ui_server.py` no longer names `tests/ui_contracts/test_humanize_catalog.py` as the guard against that constant drifting from the emitter's inline literal; it names `tests/ui_server/test_budget_tick_envelope.py`, and it says in the same sentence that the measurement was a rename mutation at `f685a707` and that the catalog test is blind to it because it pins the catalog against the emitter's own literal in `packages.orchestration.safe_points` without ever reading this constant. THE REPAIR LANDED BEFORE THIS PARAGRAPH: the R12 block's constraint 3 orders the comment pair at C4 and this resolution at C6, which is what lets this text speak in the past tense about a change on disk rather than predicting one. THE ROUND DID NOT TAKE THE NEW SENTENCE ON TRUST EITHER — its G8 re-ran the finding's own mutation against the repaired file, rewriting the constant to `"budget.ticks"` in a disposable worktree and requiring the newly named guard to go RED, so the comment names a guard that was measured twice: once when the finding was raised and once when it was resolved. WHY THE FIX WAITED THREE ROUNDS: R-0670 was raised at R7 and its own text routed it to the next round that touches `packages/orchestration/ui_server.py` on its own account, because rewriting a landed comment inside an unrelated commit is the move R-0427 records as the wrong one; R8 through R11 held no Python path in their change sets and R12 is the first round that does. The wait was the rule working, not the finding being forgotten.
<<<END DONE670
