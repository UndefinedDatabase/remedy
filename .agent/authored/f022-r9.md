── STEP RECORD/3 — F022 Live cost ticker · Runde 9 ───────────────────────────

Fortschritt: ~55 % (T001 fertig · T002 fertig · T003 offen; diese Runde baut
             nichts, sie schreibt das R8-Urteil auf Platte und uebergibt die
             Sitzung sauber) — Schaetzung

Goal:        Record the R8 verdict, register R-0673, record the R-0672
             recurrence, and hand the session over cleanly. This round writes
             NO production code: it exists because a verdict that lives only in
             a session is a verdict that did not happen.

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the plan ·
             C2 the R8 verdict, one finding and one recurrence · C3 the
             session-ending handback.

Change:      Exactly these paths, nothing else:
               .agent/authored/f022-r9.md        (C0a)
               .agent/last_block.md              (C0b)
               .agent/plan.md                    (C1)
               .agent/live_review.md             (C2)
               .agent/handoff.md                 (C3)

─── Slice convention ──────────────────────────────────────────────────────────
Each authored text below begins at its `<<<SLICE <name>` line and ends at its
`<<<END <name>` line; neither marker line is part of the slice, and no slice
contains a marker line. Extract them PROGRAMMATICALLY by marker line out of the
committed C0a blob — never retype, never rewrap, never reflow. The slices are
PLANF022R9 and LEDGER9.

Constraints:
 1. NEVER edit a slice. Apply it byte for byte. If a slice contradicts a fact
    you measure, apply it anyway and DECLARE the contradiction in the handback
    under Deviations. Repair nothing outside your slices; rule on nothing.
 2. C1 is the FIRST substantive commit (§3 checklist item 23): this round
    touches the finding ledger, so the plan advances before anything else but
    the two block-save commits.
 3. `.agent/plan.md` is a WHOLE-TEXT replacement. LEDGER9 is an APPEND to an
    append-only record: never rewrite a landed paragraph, and add nothing
    beyond the slice. This block carries NO FROM/TO pair.
 4. LEDGER9 holds, in this order and each separated by ONE blank line: the
    `R-0673` record, the `Recurrence: R-0672` paragraph, and the `Gate: R8`
    paragraph. It lands in ONE commit, C2. The gate paragraph states that the
    finding and the recurrence are written in that same commit; THIS constraint
    is what makes that true (§3 checklist item 20, R-0524 carve-out), so C2
    carries every one of those paragraphs or none.
 5. NO PRODUCTION CODE, NO TESTS, NO `docs/`. Nothing under `apps/`,
    `packages/`, `tests/` or `docs/` is in the change set. If something looks
    broken, it is the next round's work and it goes in the handback, not in a
    commit.
 6. NO REPAIR of R-0671, R-0672 or R-0673. All three are Low, all three name
    the round that should fix them, and none is a block condition. A repair
    here would be an unreviewed change on a session's last commit.
 7. Destructive verification runs ONLY inside a disposable worktree under
    `.remedy-wt/`. The primary checkout satisfies `git status --porcelain`
    empty at every commit and at the handback.
 8. Every numeral this block states about the ROUND BASE `e5c86774` was
    measured by the reviewer at that commit and is a REFERENCE to report
    against, not a target to reproduce. Where your measurement differs, report
    BOTH and reconcile NOTHING.
 9. Size, measured by the reviewer on the final bytes of this block and stated
    once here: this block is 228 lines TOTAL with 47 CONTENT lines inside its
    slices, so PROSE is 181 — under DECISION F085 D6's 490 and D5's 400.

─── Why this round exists ─────────────────────────────────────────────────────

R8 passed every gate and its verdict is not on disk. Under this workflow a round
records the PREVIOUS round's verdict, so the last reviewed round of any session
would strand its own — DECISION F085 D9 rules that a PASS is written by the next
round's ledger commit, and docs/agents/self_drive_protocol.md rules that the
handoff is the only return channel. The session's round budget is spent, so
rather than open T003 and leave it half-built, this round closes the books.

Two items also came out of the R8 gate and belong on disk before the session
ends: one new finding about a gate this reviewer wrote, and one recurrence of a
finding registered one round earlier. Neither is repaired here — constraint 6.

─── Done when ─────────────────────────────────────────────────────────────────

Run every gate below yourself, record its REAL exit code, and put ONE LINE per
gate in the handback with the transcripts kept out of it (R-0582). G1 through
G10 run after C2 and BEFORE C3, so the handback can quote all of them (§3
checklist item 31). The round base is `e5c86774` throughout.

 G1  `.agent/STOP` absent, read from disk before C0a and again before C3.
     Branch `feature/f022-live-cost-ticker`. `git status --porcelain` 0 lines
     after every one of C0a, C0b, C1 and C2.
 G2  TRANSPORT. sha256 over the block file the reviewer wrote at
     `.remedy-wt/f022-r9.md`, over the committed C0a blob, over the committed
     C0b blob and over `.agent/last_block.md` on disk: report all four digests,
     byte counts and line counts, and require them EQUAL. The digest the
     delegation names is the fifth reading and must agree.
 G3  EXTRACTION. Run an extractor over the COMMITTED C0a blob that finds the
     slices by their marker LINES and report how many slices and how many
     CONTENT lines it printed, plus the block's TOTAL and PROSE line counts.
     Report those against constraint 9's numerals; reconcile nothing.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF022R9 plus exactly one
     newline. NEGATIVE CONTROL: the same comparison against the BARE slice must
     be FALSE, and report both byte counts. `^## Goal$` once, `^## Next Steps$`
     once, `wc -l` at most 50.
 G5  APPEND at C2, proved twice. The round-base blob is a byte-exact PREFIX of
     the committed file, and the remainder is exactly one newline plus the slice
     plus one newline — report the remainder's byte count and the slice's. Then
     an INDEPENDENT reader: split both files on blank lines, report the unit
     counts before and after, and require the appended units to equal LEDGER9's
     own paragraphs IN ORDER — EVERY paragraph is checked, not only the last
     (R-0578). NEGATIVE CONTROL, in a disposable worktree: flip ONE byte in the
     FIRST appended paragraph and ONE in the LAST, at offsets you name, and
     confirm both readers reject each mutant while both accept the true file.
     Remove the worktree; `git worktree list` back to one line.
 G6  LEDGER INTEGRITY, base versus C2. Report for both points: the count of
     lines matching `^- R-\d+ — `, whether they are all DISTINCT, the MAXIMUM
     id, the count of `^Done: R-` with its distinct ids, of `^Landed: `, of
     `^Recurrence: R-` with its distinct ids, and of `^Gate: R` with its
     distinct keys. Report the ids ADDED and REMOVED as sets. At base the
     reviewer measured 233 records, all distinct, maximum `R-0672`, 1 `Done:`
     line for `R-0653`, 0 `Landed:`, 2 `Recurrence:` lines and 8 `Gate:` lines
     over 8 distinct keys. This round is EXPECTED to add exactly `R-0673`, to
     take `^Recurrence: R-` to 3, and to add `Gate: R8`; report what you
     measure. `R-0672` must still occur exactly once as a `^- R-0672 — ` record
     — a recurrence APPENDS and never rewrites the finding it recurs against.
     `^## Steps$` occurs exactly once at C2 and the map text is UNCHANGED —
     report the map paragraph byte-identical at base and at C2.
 G7  THE FOUR STATE READERS, serially in the PRIMARY checkout at C2, exit 0:
     `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py` and
     `tests/orchestration/test_integrity_gate.py`. The reviewer measured 544
     passed in total at the round base. Never run two pytest processes at once.
     This round rewrites `.agent/` state and those four are its readers.
 G8  THE CANARY at C2: `python3 -m pytest tests/cli/test_golden_path.py -q`,
     exit 0. The reviewer measured 42 passed at the round base.
 G9  STRUCTURE, reported for the commits BEFORE C3 and for the range as a whole
     (C3's own numbers belong to the next session's ledger entry, not here):
     every commit single-parent; each commit's INSERTION count, each under the
     500 cap; the range path set against the Change set above with the
     difference reported in BOTH directions; `git show --numstat` agreeing cell
     by cell with the handback's `## Commits` table; lines BEGINNING `<<<SLICE `
     or `<<<END ` counting 0 in `.agent/plan.md` and `.agent/live_review.md`;
     `git ls-files .remedy-wt` 0; one worktree; and the round's reflog rows with
     amend, rebase and cherry counts, each of which must be 0.
 G10 `gh pr list --state open --json number,headRefName`. Report it verbatim.
     Create no PR and merge nothing this round. THIS IS THE LAST ROUND OF THE
     SESSION AND IT STILL CREATES NO PR: the branch is mid-feature, T003 is
     unbuilt, and a PR now would offer an incomplete feature for merge at the
     next session's Open PR Gate.
 G11 STALENESS. Every sentence C1 and C2 land that states a fact about a file is
     re-measured at C2, and any that has gone stale is reported as a residual
     rather than repaired. Report explicitly that you checked, and name any
     residual. Slices are NEVER edited to fix one.

NOT A GATE, and neither is run this round: `npm run lint`, `npm run typecheck`
and `npm run test:unit`. This round's change set holds no file under `apps/`, so
none of the three can say anything about it. The reviewer measured all three at
`e5c86774` — typecheck exit 0, `test:unit` exit 0 at 17 files and 241 tests,
lint exit 1 at 72 problems, which is R-0622 and routes to a paydown branch.

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             every mandated section in order, one changed-files table per
             commit, an item-status row per Bundle item, the round base SHA,
             ONE line per gate, and the `Fortschritt:` block above carried
             VERBATIM across all three of its lines. The cap is 60 lines for
             this commit count; declare a DECISION D15 stated cause if the
             mandated content genuinely does not fit.
             THIS HANDBACK ENDS THE SESSION, so its `## Next` section names, in
             this order: (1) Phase 1 rule 1 — re-read `.agent/STOP` from disk
             before anything else; (2) the Open PR Gate,
             `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
             which is expected to print `[]` because this session created none;
             (3) the next round is R10, T003 — the terminal reconciliation, the
             delta labelling, the live wiring through `remedyApi.ts` and
             `RemedyShell.tsx`, and the fake-job end-to-end; (4) the three open
             F022 findings R-0671, R-0672 and R-0673, each named with the round
             that should fix it. State plainly that the session ended at its
             declared round budget with every reviewed round's verdict on disk,
             which is a clean stop and not a blocker.
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF022R9
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
R9 records the R8 verdict, registers R-0673, records the R-0672 recurrence and
ends the session cleanly. It builds nothing: T001 and T002 are complete, the
session's round budget is spent, and a verdict that lives only in a session is
a verdict that did not happen.

## Next Steps
1. R10 T003 — the terminal reconciliation, the delta labelling, the live wiring
   through `remedyApi.ts` and `RemedyShell.tsx`, and the fake-job end-to-end.
2. R11 the integration gate.
3. R12 closure.

## Risks
- Three F022 findings are open and all are Low: R-0671 wants one assertion in
  `costMetric.test.ts` pinning a negative spend as the limitless view; R-0672
  and its recurrence want the next DECISION on this ground to state a complete
  reversal; R-0673 is a reviewer-gate defect that has already been paid for.
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks rather than F022
  defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- R-0665 is open and this feature needs its route: every UI feature is told to
  record visual deviations in an `assumption_log` that does not exist. F022
  records them as DECISIONs in `.agent/decisions.md` and says so, which is a
  route rather than a fix.
<<<END PLANF022R9

<<<SLICE LEDGER9
- R-0673 — Low, A REVIEWER GATE FORCED AN EDIT THE SAME BLOCK'S CHANGE LIST DID NOT LICENSE, AND THE WORKER HAD TO SPEND A DEVIATION CHOOSING BETWEEN THEM. Raised by the reviewer at the F022 R8 gate; the WORKER found it first, declared it as deviation 2 and resolved it the right way round. The R8 block's render section lists what `TopMetricsBar.tsx` "gains, and nothing more" and names six additions, none of them a removal. Its contract-test item P6 then orders, over the whole comment-stripped file, that "the only `/` outside a JSX closing tag or a string is none". Measured at `142af5e4`: that file's private `formatTokens` at lines 27 to 31 divides three times, so P6 could not pass while the function stood, and the two clauses cannot both be satisfied. The worker removed `formatTokens`, imported the identical `formatTokenCount` from `costMetric.ts` — whose own comment already names R8 as the round that does this — and declared the departure. The reviewer verified the substitution is behaviour-preserving rather than taking the claim: the two bodies are the same algorithm with `1_000_000` written as `1000000`, and they agree on 0, 1, 999, 1000, 1001, 1500, 999999, 1000000, 1000001, 2500000 and 123456789, so the tokens metric's rendered output and its tooltip rows are unchanged. THE DEFECT IS THE REVIEWER'S AND IT IS THE MIRROR OF §3 CHECKLIST ITEM 7: that item makes a block grep for EXISTING guards that its addition would break, and this is a block writing a NEW guard that its own protected file already breaks. Item 7 reads outward from the block to the suite; nothing yet reads inward from a block's new whole-file assertion to the file it will be run against. Low, because the outcome is correct, the deviation is declared and the round paid one deviation rather than losing an item — but a worker who had obeyed the change list literally would have shipped a red gate it was forbidden to fix, which is the shape that costs a repair round. The counter-measure for the next block that orders a whole-file absence over a file it is also editing: run that absence over the file AT THE BASE first, and where it is already false, say in the same clause which existing lines the round is licensed to remove.

Recurrence: R-0672 — A LANDED DECISION'S REVERSAL INSTRUCTION DOES NOT NAME EVERYTHING ITS OWN ROUND ADDED. Second instance, at F022 R8, inside the very clause written to correct the first. NO NEW ID IS MINTED: R-0672 already rules that a DECISION's REVERSE paragraph is the one part a later reader EXECUTES rather than reads, and that it must be resolved against the round's own Change set rather than against the files most in mind. The first instance was DECISION F022 D4 omitting `RemedyMetric.cost` and its `import type` line. THE SECOND IS DECISION F022 D5, committed at `4d2681c4`, whose closing paragraph lists four items and calls them "the whole of this round's production surface" — while C5 of that same round ALSO deleted the private `formatTokens` from `TopMetricsBar.tsx` and rewired two call sites to `formatTokenCount`, which a reversal must restore or leave the tokens metric importing a module the reversal deletes. The worker declared it as a constraint-1 contradiction and applied the slice byte for byte, which is what it was required to do. That the recurrence landed in the correcting clause is the whole lesson: R-0672's own text says to resolve the list against the Change set, and the reviewer wrote D5's reversal from the four items it had just specified rather than from the seven paths the block declares — the same failure mode, one round later, with the rule already on disk. Both instances stay OPEN under R-0672 and their fix is one clause in the next DECISION that touches this ground, stating the reversal as a path-by-path list derived mechanically from the round's Change set.

Gate: R8 — the F022 R8 entry. R8 PASSED ON EVERY ONE OF ITS FIFTEEN GATES, AND THE REVIEWER RE-RAN EVERY ONE OF THEM ITSELF AND ADDED A MUTATION THE BLOCK NEVER ORDERED. The finding and the recurrence above are written in THIS SAME COMMIT, which the block's constraint 4 fixes. TRANSPORT HELD IN ITS STRONGEST FORM: the reviewer authored this round's block, so §4.9's primary comparison against the reviewer's own original was available and was used rather than the digest fallback — `.remedy-wt/f022-r8.md`, the committed C0a blob at `b88f3553`, the committed C0b blob at `d92cdf92`, `.agent/last_block.md` on disk and `.agent/authored/f022-r8.md` on disk are ALL sha256 `a077de71476f731f7d7c857916269e002d2e66dcc3e29bfe7f9850fdefdb278d` over 42013 bytes and 382 lines, and C0a and C0b are the SAME git blob. THE EXTRACTION out of the committed blob printed 3 slices over 69 CONTENT lines, so TOTAL re-measures at 382 and PROSE at 313, under DECISION F085 D6's 490 and D5's 400, and constraint 10's numerals reproduce exactly. `.agent/plan.md` at `8051fd56` is byte-equal to PLANF022R8 plus one newline at 2297 bytes against the bare slice's 2296, with the bare-slice control DIFFERING, `^## Goal$` and `^## Next Steps$` once each and 43 lines. BOTH APPENDS HOLD UNDER BOTH READERS: at `6034b603` the round-base blob is a byte-exact PREFIX and the remainder is 12211 bytes, exactly one newline plus LEDGER8's 12209 plus one newline, with an independent blank-line splitter reading 258 units before and 262 after; at `4d2681c4` the prefix holds and the remainder is 6761, exactly one newline plus DEC5's 6759 plus one newline, the splitter reading 1287 before and 1297 after, and `## DECISION F022 D5 ` counting 1. THE SETS MOVED EXACTLY WHERE THE ROUND PROMISED: 231 records at base and 233 at C2, all DISTINCT at both, maximum id `R-0670` to `R-0672`, ids ADDED exactly `{R-0671, R-0672}` and ids REMOVED the EMPTY SET, `^Done: R-` 0 to 1 carrying exactly `R-0653`, `^Landed: ` 0 at both, `^Gate: R` 7 to 8 with the distinct keys gaining `Gate: R7`, `^- R-0653 — ` still exactly 1 so the resolution APPENDED rather than rewrote, `^## Steps$` once, and the map paragraph byte-identical at base and at C2. THE SUITES ARE THE REVIEWER'S OWN, run in the primary checkout: `npm run typecheck` exit 0 with no output; `npm run test:unit` exit 0 at 17 files and 241 tests against the base's 17 and 235, the file count holding and the difference being exactly the six goldens C4 adds; the four state readers 455, 52, 21 and 16 for 544; `tests/ui_contracts/` 514 passed and 4 skipped against the base's 495 and 4, the difference being exactly the nineteen tests C5's new contract file adds; and the canary `tests/cli/test_golden_path.py` 42. THE MUTATIONS ALL RAN IN `.remedy-wt/r8review` AT `68cf3c16` with the primary checkout never touched, and every ordered colour reproduced: dropping the track's non-null fill guard fails exactly `TestNoFakeDenominatorAtTheRenderLayer::test_the_track_is_guarded_on_a_real_fill`, 1 failed and 18 passed; driving the estimate mark from `level === "warn"` fails BOTH `TestTheMarkerIsTheBasisNotTheThreshold` tests, 2 failed and 17 passed; and changing one golden's `fill` from 0.85 to 0.84 fails 1 of 23 under the scoped worktree vitest route, naming the entry `tick 1 renders $3.40 at level warn`. THE REVIEWER'S OWN UNORDERED MUTATION IS THE ONE THAT MATTERED MOST, because DECISION F022 D5 clause 3 rules that a threshold is never colour alone and a rule nobody can break is a rule nobody has tested: deleting the level phrase from the accessible name, so `warn` and `exceeded` survive only as a tint, fails `TestTheThresholdIsNeverColourAlone::test_each_banded_level_reaches_the_accessible` — 1 failed and 18 passed. The accessibility rule is pinned, not merely asserted. THE GOLDENS ARE HAND-WRITTEN AND CORRECT, checked by the reviewer against DECISION F022 D4's clauses rather than against the module: tick 1 is 3.4 over 4, which is 0.85 exactly in IEEE 754 because the divisor is a power of two, so it lands on the inclusive warn boundary the table claims; 4.6 over 4 is 1.15 and rounds to the 115 per cent the tooltip states; the limitless tick carries no `unmeasured_calls` key and correctly grows no line for one. GO3 asserts the table over ITSELF, so a later edit cannot drop a state and leave a green suite. THE RENDER DECIDES NOTHING, as DECISION F022 D5 clause 1 requires: every cost branch is a field lookup, the sole computation is `Math.max(0, Math.min(m.cost.fill * 100, 100))` for the track's width, and `apps/ui/src/api/costMetric.ts` is NOT in the range's path set at all. STRUCTURE HELD: eight commits over `142af5e4`..`e5c86774`, every one single-parent, insertions 382, 245, 17, 8, 20, 91, 385 and 58, each under the 500 cap; the range path set is exactly the block's declared eleven-path Change set with the difference EMPTY in both directions; lines BEGINNING `<<<SLICE ` or `<<<END ` count 0 in all three slice targets; `git ls-files .remedy-wt` 0; one worktree; `git status --porcelain` empty; 0 amend, 0 rebase and 0 cherry. THE HANDBACK IS COMPLIANT at exactly 100 lines against the 100 the eight-commit case allows, every mandated section present and in order. THE ROUND'S FIVE DECLARED DEVIATIONS ARE ALL CORRECT AND TWO OF THEM CORRECT THE REVIEWER — the forced `formatTokens` removal is R-0673 above and the incomplete reversal is the R-0672 recurrence, while the `.costTrack` and `.progressTrack` divergence, the carried lint sentence and the unchanged commit sequence are all as the block ordered. THE VERDICT IS PASS: every numeral R8 states reproduced under the reviewer's own measurement, all three ordered mutations went red plus one unordered one, the two defects the round surfaced were the reviewer's own and are registered rather than waved through, and T002 closes with the COST metric drawn, pinned by a hand-written golden table and a nineteen-test source contract.
<<<END LEDGER9
