── STEP RECORD/3 — F022 Live cost ticker · Runde 13 ──────────────────────────

Fortschritt: ~80 % (T001 fertig · T002 fertig · T003a fertig · T003b halb —
             diese Runde baut nichts, sie schreibt das R12-Urteil auf Platte
             und uebergibt die Sitzung sauber) — Schaetzung

Goal:        Record the R12 verdict and one recurrence, repair the round map,
             and hand the session over cleanly. This round writes NO production
             code: R12 shipped backend code and a verdict that lives only in a
             handoff is a verdict the next session must re-derive, which is what
             DECISION F085 D9 exists to prevent.

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the plan ·
             C2 repair the round map · C3 the R12 verdict and the R-0533
             recurrence · C4 the session-ending handback.

Change:      Exactly these paths, nothing else:
               .agent/authored/f022-r13.md    (C0a)
               .agent/last_block.md           (C0b)
               .agent/plan.md                 (C1)
               .agent/live_review.md          (C2, C3)
               .agent/handoff.md              (C4)

─── Slice convention ──────────────────────────────────────────────────────────
Each authored text below begins at its `<<<SLICE <name>` line and ends at its
`<<<END <name>` line; neither marker line is part of the slice, and no slice
contains a marker line. Extract them PROGRAMMATICALLY by marker line out of the
committed C0a blob — never retype, never rewrap, never reflow. The whole-text
slices are PLANF022R13 and LEDGER13. MAPFROM13 and MAPTO13 are the halves of a
FROM/TO pair, and this block carries no other pair. Every slice is quoted
WITHOUT its trailing newline; PLANF022R13 replaces its file whole, and LEDGER13
lands as one newline plus the slice plus one newline.

CONTAINMENT TEST, run by the reviewer on the final bytes, output quoted:
  MAPFROM13/MAPTO13 — `TO contains FROM: false` → REWRITE.
That is the reading for every pair this block carries, taken per pair.

Constraints:
 1. NEVER edit a slice. Apply it byte for byte. If a slice contradicts a fact
    you measure, apply it anyway and DECLARE the contradiction in the handback
    under Deviations. Repair nothing outside your slices; rule on nothing.
 2. C1 is the FIRST substantive commit (§3 checklist item 23): this round
    touches the finding ledger, so the plan advances before anything else but
    the two block-save commits.
 3. COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4 and no other. Within
    `.agent/live_review.md` the pair at C2 precedes that file's append at C3
    (R-0639/R-0640), so the append reads a remainder no pair will change.
 4. LEDGER13 holds, in this order and separated by ONE blank line: the
    `Recurrence: R-0533` paragraph and the `Gate: R12` paragraph. It lands in
    ONE commit, C3, or neither does: the gate paragraph states that the
    recurrence is written in that same commit, and THIS constraint is what makes
    that true (§3 item 20, R-0524 carve-out).
 5. NO PRODUCTION CODE, NO TESTS, NO `docs/`. Nothing under `apps/`,
    `packages/`, `tests/` or `docs/` is in the Change set. If something looks
    broken, it is the next session's work and it goes in the handback.
 6. NO REPAIR of any open finding. R-0533's recurrence is RECORDED, not fixed;
    the false sentence it concerns is in a landed slice and §3 item 20 forbids
    rewriting landed text.
 7. Destructive verification runs ONLY inside a disposable worktree under
    `.remedy-wt/`. The primary checkout satisfies `git status --porcelain`
    empty at every commit and at the handback.
 8. Every numeral this block states about the ROUND BASE `ee40613e` was produced
    by a reviewer script or tool run at that commit and is a REFERENCE to report
    against, not a target to reproduce. Where your measurement differs, report
    BOTH and reconcile NOTHING.
 9. Size, measured by the reviewer on the final bytes of this block and stated
    once here: this block is 262 lines TOTAL with 54 CONTENT lines inside its
    slices, so PROSE is 208 — under DECISION F085 D6's 490 and D5's 400.

─── Why this round exists ─────────────────────────────────────────────────────

R12 passed every gate and its verdict is not on disk. Under this workflow a
round records the PREVIOUS round's verdict, so the last reviewed round of any
session strands its own — DECISION F085 D9 rules that a PASS is written by the
next round's ledger commit, and docs/agents/self_drive_protocol.md rules that
the handoff is the only return channel. R12 shipped backend code, so leaving its
verdict unwritten would make the next session re-derive a review that has
already happened. The session's round budget is spent, so rather than open
T003b's client half and leave it part-built, this round closes the books.

One item also came out of the R12 gate and belongs on disk before the session
ends: a recurrence of a finding the reviewer's own slice re-committed. It is
recorded, not repaired — constraint 6.

─── Done when ─────────────────────────────────────────────────────────────────

Run every gate below yourself, record its REAL exit code, and put ONE LINE per
gate in the handback with the transcripts kept out of it (R-0582). G1 through
G9 run after C3 and BEFORE C4, so the handback can quote all of them (§3
checklist item 31). The round base is `ee40613e` throughout.

 G1  `.agent/STOP` absent, read from disk before C0a and again before C4.
     Branch `feature/f022-live-cost-ticker`. `git status --porcelain` 0 lines
     after every one of C0a, C0b, C1 and C2 and C3.
 G2  TRANSPORT. sha256 over the block file the reviewer wrote at
     `.remedy-wt/f022-r13.md`, over the committed C0a blob, over the committed
     C0b blob and over `.agent/last_block.md` on disk: report all four digests,
     byte counts and line counts, and require them EQUAL. The digest the
     delegation names is the fifth reading and must agree.
 G3  EXTRACTION. Run an extractor over the COMMITTED C0a blob that finds the
     slices by their marker LINES and report how many slices and how many
     CONTENT lines it printed, plus the block's TOTAL and PROSE line counts.
     Report those against constraint 9's numerals; reconcile nothing.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF022R13 plus exactly one
     newline. NEGATIVE CONTROL: the same comparison against the BARE slice must
     be FALSE, and report both byte counts. `^## Goal$` once, `^## Next Steps$`
     once, `wc -l` at most 50.
 G5  THE PAIR at C2 in `.agent/live_review.md`. Report the containment output
     and require it to match the convention block. MAPFROM13 1x at the round
     base and 0x at C2; MAPTO13 0x at base and 1x at C2; the file's byte length
     changing by exactly `len(MAPTO13) - len(MAPFROM13)`; `^## Steps$` still
     exactly once; and the committed file equal to the base file with only that
     replacement applied and nothing else. ALSO report the longest line length
     of the `## Steps` paragraph at C2: no line in it may exceed 84 characters
     (R-0431).
 G6  APPEND at C3, proved twice. The C2 blob is a byte-exact PREFIX of the
     committed file and the remainder is exactly one newline plus the slice plus
     one newline — report the remainder's byte count and the slice's. Then an
     INDEPENDENT reader: split both files on blank lines, let N be the number of
     paragraphs YOUR script counts in the slice, and require the LAST N units of
     the committed file to equal the slice's N paragraphs IN ORDER. Report N; do
     not take it from this block. NEGATIVE CONTROL, in a disposable worktree,
     applied to the FIRST appended paragraph: flip ONE byte at an offset you
     name and confirm BOTH readers reject the mutant while both accept the true
     file. THE OFFSET IS A BYTE OFFSET — the file carries multi-byte em dashes,
     so a CHARACTER offset lands early, outside the appended region, where
     reader (b) accepts the mutant and the control proves nothing. Report the
     ~20 bytes surrounding the flip. Remove the worktree; `git worktree list`
     back to one line.
 G7  LEDGER INTEGRITY, base versus C3. Report for both points: the count of
     lines matching `^- R-\d+ — `, whether they are all DISTINCT, the MAXIMUM
     id, the count of `^Done: R-` with its distinct ids, of `^Landed: `, of
     `^Recurrence: R-` with its distinct ids, and of `^Gate: R` with its
     distinct keys. Report the ids ADDED and REMOVED as sets. At base the
     reviewer measured 234 records, all distinct, maximum `R-0673`, 2 `Done:`
     lines over `R-0653` and `R-0670`, 0 `Landed:`, 7 `Recurrence:` lines and 12
     `Gate:` lines over 12 distinct keys. This round MINTS NO NEW ID: it is
     expected to add no record, to take `^Recurrence: R-` to 8 by gaining
     `R-0533`, and to add `Gate: R12`. Report what you measure. `R-0533` must
     still occur exactly once as a `^- R-0533 — ` record.
 G8  THE FOUR STATE READERS plus THE CANARY, serially in the PRIMARY checkout at
     C3, exit 0: `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py`,
     `tests/orchestration/test_integrity_gate.py`, then
     `tests/cli/test_golden_path.py`. The reviewer measured 470, 52, 21 and 16
     for 559 across the four, and 42 for the canary, at the round base. Never
     run two pytest processes at once. This round rewrites `.agent/` state and
     those four are its readers.
 G9  STRUCTURE, reported for the commits BEFORE C4 and for the range as a whole
     (C4's own numbers belong to the next session's ledger entry, not here):
     every commit single-parent; each commit's INSERTION count, each under the
     500 cap; the range path set against the Change set above with the
     difference reported in BOTH directions; `git show --numstat` agreeing cell
     by cell with the handback's `## Commits` table; the LINE-ANCHORED patterns
     `^<<<SLICE ` and `^<<<END ` counting 0 in `.agent/plan.md` and
     `.agent/live_review.md`; `git ls-files .remedy-wt` 0; one worktree; and the
     round's reflog rows with amend, rebase and cherry counts, each 0.
 G10 `gh pr list --state open --json number,headRefName`. Report it verbatim.
     Create no PR and merge nothing. THIS IS THE LAST ROUND OF THE SESSION AND
     IT STILL CREATES NO PR: T003b's client half is unbuilt, the integration
     gate has not run, and a PR now would offer an incomplete feature for merge
     at the next session's Open PR Gate.
 G11 STALENESS. Every sentence C1 and C2 and C3 land that states a fact about a
     file is re-measured at C3, and any that has gone stale is reported as a
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
             counted in (R-0442). The cap is 60 lines for this commit count;
             declare a DECISION D15 stated cause with your own measured numeral
             in the declaring line if the mandated content genuinely does not
             fit.
             THIS HANDBACK ENDS THE SESSION, so its `## Next` section names, in
             this order: (1) Phase 1 rule 1 — re-read `.agent/STOP` from disk
             before anything else; (2) the Open PR Gate,
             `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
             expected to print `[]` because this session created none; (3) R14,
             T003b's client half — read `budget_final` into the dashboard type
             and render the terminal reconciliation with its delta label, per
             DECISION F022 D7, remembering that the delta is a TRANSPORT
             statement and never a second arithmetic; (4) that R13's own verdict
             is the branch TERMINATOR under §4 item 13 — the last round of a
             session has no on-disk gate entry by construction, and the next
             session gates R13 as its first act. State plainly that the session
             ended at its declared round budget with every PRODUCTION round's
             verdict on disk, which is a clean stop and not a blocker.
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF022R13
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
R13 records the R12 verdict, registers the R-0533 recurrence, repairs the round
map and ends the session cleanly. It builds nothing: T003a is complete, the
server half of T003b is complete, the session's round budget is spent, and a
verdict that lives only in a session is a verdict that did not happen.

## Next Steps
1. R14 T003b-b — read `budget_final` into the dashboard type and render the
   terminal reconciliation with its delta label, per DECISION F022 D7.
2. R15 the integration gate.
3. R16 closure.

## Risks
- The delta R14 renders is a TRANSPORT statement, not arithmetic: both sides are
  the same quantity from the same producer, so a difference means frames were
  missed. A round that reads it as drift would reintroduce the fabricated
  honesty moment DECISION F022 D7 exists to prevent.
- Open F022 findings: R-0672 and R-0625 want their next-DECISION and
  next-numeral clauses honoured; R-0431, R-0413 and R-0533 are reviewer-block
  defects already recorded and already paid for.
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks, not F022 defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch. Its measured value is in the
  `R-0625` recurrence, not in this sentence.
- R-0665 is open and this feature needs its route: every UI feature is told to
  record visual deviations in an `assumption_log` that does not exist. F022
  records them as DECISIONs in `.agent/decisions.md`, a route rather than a fix.
<<<END PLANF022R13

<<<SLICE MAPFROM13
final-figure section, R-0670's repair and the R11 verdict → R13 T003b-b the
client's reconciliation with its delta label → R14 the integration gate → R15
closure. This section is the only place the round map is stated, per
<<<END MAPFROM13

<<<SLICE MAPTO13
final-figure section, R-0670's repair and the R11 verdict → R13 record the R12
verdict and end that session at its round budget → R14 T003b-b the client's
reconciliation with its delta label → R15 the integration gate → R16 closure.
This section is the only place the round map is stated, per
<<<END MAPTO13

<<<SLICE LEDGER13
Recurrence: R-0533 — A SENTENCE QUANTIFYING ACROSS A RANGE OF ROUNDS WAS WRITTEN FROM RECOLLECTION INSTEAD OF FROM A WALK OF THE RANGE. Second instance, at F022 R12, in the reviewer's own resolution text. NO NEW ID IS MINTED: §3 checklist item 30 requires the open set searched for the DEFECT before an id, and item 22 of the same checklist already names this class — "a sentence quantifying across COMMITS is measured over the whole range by walking it mechanically, `git rev-list --reverse <base>..<head>`, one reading per commit, and written as the list that walk produced, never generalised from the commits the author happened to read". Item 22 cites R-0530 and R-0533; only R-0533 is a record in this ledger, because the F022 R1 reset carried the open set forward rather than the whole history, so this recurrence is registered against R-0533 and R-0530 is named here for the reader who goes looking for it. THE INSTANCE: the `Done: R-0670` paragraph committed at `11a379ee` explains why the fix waited three rounds and says "R8 through R11 held no Python path in their change sets and R12 is the first round that does". MEASURED at `ee40613e` by walking each round's own range with `git diff --name-only`: R8 (`142af5e4..e5c86774`) changed `tests/ui_contracts/test_cost_metric_render.py` and R10 (`a8952614..3e1d3fae`) changed the same file, so two of those four rounds DID hold a Python path; R9 and R11 held none. THE ROUTING CLAIM THE SENTENCE EXISTS TO SUPPORT IS TRUE AND WAS MEASURED IN THE SAME WALK: none of R8, R9, R10 or R11 touched `packages/orchestration/ui_server.py`, which is the path R-0670's own routing clause names, so the finding really did wait for the first round that touches that file and the wait really was the rule working. FOUND BY THE WORKER, which measured the slice it had been ordered to apply byte for byte, applied it anyway as constraint 1 required, and declared the contradiction — the sixth consecutive round in which a worker's declaration rather than a gate is what put a reviewer-authored defect on the record. WHY LOW: no gate consumed the sentence, the conclusion it supports is correct and independently measured, and the cost is one wrong clause beside a right one. WHY IT IS REGISTERED AT ALL: `.agent/live_review.md` is what a later session reads to learn what was verified, and "held no Python path" is the kind of clause a later round would cite when deciding where a fix belongs. THE LANDED PARAGRAPH IS NOT REWRITTEN, per §3 item 20: this correction is dated by the commit that carries it. Both instances stay OPEN under R-0533, and the addition this one earns is one clause: a sentence quantifying over a range of ROUNDS is walked the same way a sentence quantifying over commits is, because a round is only a range of commits wearing a name.

Gate: R12 — the F022 R12 entry. R12 PASSED ON EVERY ONE OF ITS FOURTEEN GATES, AND THE REVIEWER RE-RAN EVERY ONE OF THEM ITSELF AND ADDED FOUR MUTATIONS THE BLOCK NEVER ORDERED. The recurrence above is written in THIS SAME COMMIT, which the R13 block's constraint 4 fixes. THE ROUND'S SUBSTANCE IS THAT THE LEDGER'S FINAL FIGURE IS NOW SERVED. `_build_budget_final` returns the whitelisted payload of the LAST event whose kind is `BUDGET_TICK_EVENT` and `None` when the job emitted none, the dashboard gained `"budget_final"` beside `"token_usage"`, and neither needed a new endpoint or a byte of new I/O because `_load_events` already globs the `budget-ticks` run log and `load_run_events` already sorts by timestamp — the half of DECISION F022 D7 that made it cheap. THE ROUND ALSO CLOSED R-0670, which had waited since R7 for a round that touches `packages/orchestration/ui_server.py` on its own account. TRANSPORT HELD IN ITS STRONGEST FORM: the reviewer's scratch original, the committed C0a blob, the committed C0b blob, `.agent/last_block.md` on disk and `.agent/authored/f022-r12.md` on disk are ALL sha256 `1891867831bb3a2b985e2b70986d8abf3949378053031d4ebfec5c2e288b2ee8` over 31863 bytes and 349 lines, and C0a and C0b resolve to the SAME git blob. THE EXTRACTION printed 7 slices over 69 CONTENT lines, TOTAL 349 and PROSE 280, reproducing constraint 9 exactly. `.agent/plan.md` at `fe6da915` is 2559 bytes = PLANF022R12's 2558 plus one newline, the bare-slice control DIFFERING, headings once each, 45 lines against the cap of 50. BOTH PAIRS ARE EXACT, BOTH PRINTED `TO contains FROM: false`, AND BOTH ARE SURGICAL — each committed file equals its base with ONLY that replacement applied: in `.agent/live_review.md` at `cbe4f643` MAPFROM12 1→0 and MAPTO12 0→1 with byte delta 51 = 305 − 254, and in `packages/orchestration/ui_server.py` at `df8ae445` GUARDFROM 1→0 and GUARDTO 0→1 with byte delta 255 = 520 − 265. THE MAP PAIR ALSO REPAIRED R-0431's LANDED LINE: the `## Steps` paragraph's longest line reads 80 characters at `cbe4f643` against 99 at the round base, which is the measurement that pair was widened to make. BOTH APPENDS HOLD UNDER BOTH READERS: at `d0d5e94b` the remainder is 8279 = 1 + LEDGER12's 8277 + 1 with N=3 paragraphs equal in order over 269→272 units; at `11a379ee` the remainder is 1648 = 1 + DONE670's 1646 + 1 with N=1 over 272→273. THE SETS MOVED EXACTLY WHERE THE ROUND PROMISED: 234 records at base and at C6, ids ADDED and REMOVED both the EMPTY SET so NO ID WAS MINTED, `^Done: R-` 1→2 gaining `R-0670`, `^Recurrence: R-` 5→7 gaining `R-0431` and `R-0413`, `^Gate: R` 11→12 gaining the key `R11`, and `R-0670`, `R-0431` and `R-0413` each still exactly one `^- R-\d+ — ` record. THE MUTATION GATE IS THE ONE THAT MATTERED: G8 re-ran R-0670's own rename in a disposable worktree at C5, and `tests/ui_server/test_budget_tick_envelope.py` — the guard the repaired comment now names — went RED at 11 failed and 5 passed while `tests/ui_contracts/test_humanize_catalog.py` stayed green at 9 passed, which is exactly what the finding measured and exactly why the old sentence was wrong. The comment now names a guard that has been measured twice. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout: `tests/ui_server/` 470 against the base's 455, the +15 being the new file's fifteen tests; `tests/ui_contracts/` 518 passed and 4 skipped, unchanged; the four state readers 470, 52, 21 and 16 for 559; and the canary 42. THE REVIEWER'S FOUR UNORDERED MUTATIONS ALL RAN IN A DISPOSABLE WORKTREE WITH THE PRIMARY CHECKOUT NEVER WRITTEN, against a positive control of 15 passed: taking the FIRST tick instead of the last failed 5 tests naming `test_the_later_tick_wins_over_the_earlier_one`; returning `{}` instead of `None` failed 5 naming `test_it_is_none_and_not_an_empty_object_or_a_zero`; passing the raw metadata through instead of the whitelist failed 3 naming `test_an_unnamed_key_inside_basis_never_reaches_the_dashboard`, so the REDACTION boundary is pinned and not merely described; and deleting the dashboard key failed 3 naming `test_the_dashboard_carries_the_final_figure`. Every property the block ordered is genuinely guarded. STRUCTURE HELD: eight commits before the handback, every one single-parent, insertions 349, 241, 17, 4, 6, 6, 216 and 2, each under the 500 cap; the range path set is exactly the declared seven-path Change set with the difference EMPTY in both directions; `git show --numstat` agrees cell by cell with all nine `## Commits` rows; anchored markers 0 in both state files; one worktree; 0 amend, 0 rebase and 0 cherry. THE HANDBACK IS COMPLIANT at 137 lines with a DECISION D15 stated cause naming that same 137, every mandated section present and in order, and the three-line `Fortschritt:` block byte-identical to the block's. THE ROUND'S ONE SUBSTANTIVE DEVIATION IS CORRECT AND IT CORRECTS THE REVIEWER: the `Done: R-0670` range claim is the R-0533 recurrence above. THE VERDICT IS PASS: every numeral R12 states reproduced under the reviewer's own measurement, four unordered mutations went red against the right tests, no slice was edited, no id was minted, a finding that had waited five rounds for the right carrier was resolved with its guard re-measured, and the terminal reconciliation now has a real figure to read.
<<<END LEDGER13
