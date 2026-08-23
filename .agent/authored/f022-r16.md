── STEP RECORD/3 — F022 Live cost ticker · Runde 16 ──────────────────────────

Fortschritt: ~95 % (T001 fertig · T002 fertig · T003 fertig · Integration Gate
             bestanden — diese Runde baut nichts, sie schreibt das R15-Urteil
             auf Platte und uebergibt die Sitzung sauber) — Schaetzung

Goal:        Record the R15 verdict and one recurrence, repair the round map,
             and hand the session over cleanly. This round writes NO production
             code: R15 ran the full suite twice and a gate verdict that lives
             only in a session is a verdict the next session must re-derive —
             at the price of two more full-suite runs, which is exactly what
             DECISION F085 D9 exists to prevent.

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the plan ·
             C2 repair the round map · C3 the R15 verdict and the R-0445
             recurrence · C4 the session-ending handback.

Change:      Exactly these paths, nothing else:
               .agent/authored/f022-r16.md    (C0a)
               .agent/last_block.md           (C0b)
               .agent/plan.md                 (C1)
               .agent/live_review.md          (C2, C3)
               .agent/handoff.md              (C4)

─── Slice convention ──────────────────────────────────────────────────────────
Each authored text below begins at its `<<<SLICE <name>` line and ends at its
`<<<END <name>` line; neither marker line is part of the slice, and no slice
contains a marker line. Extract them PROGRAMMATICALLY by marker line out of the
committed C0a blob — never retype, never rewrap, never reflow. The whole-text
slices are PLANF022R16 and LEDGER16. MAPFROM16 and MAPTO16 are the halves of a
FROM/TO pair, and this block carries no other pair. Every slice is quoted
WITHOUT its trailing newline; PLANF022R16 replaces its file whole, and LEDGER16
lands as one newline plus the slice plus one newline.

CONTAINMENT TEST, run by the reviewer on the final bytes, output quoted:
  MAPFROM16/MAPTO16 — `TO contains FROM: false` → REWRITE.
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
 4. LEDGER16 holds, in this order and separated by ONE blank line: the
    `Recurrence: R-0445` paragraph and the `Gate: R15` paragraph. It lands in
    ONE commit, C3, or neither does: the gate paragraph states that the
    recurrence is written in that same commit, and THIS constraint is what makes
    that true (§3 item 20, R-0524 carve-out).
 5. NO PRODUCTION CODE, NO TESTS, NO `docs/`. Nothing under `apps/`,
    `packages/`, `tests/` or `docs/` is in the Change set. R-0445's own repair
    belongs to `docs/agents/integration_gate.md` and is explicitly routed to a
    follow-up branch by the finding itself; performing it here would be scope
    drift into a process doc from a feature branch.
 6. NO REPAIR of any open finding. R-0445's recurrence is RECORDED, not fixed.
 7. Destructive verification runs ONLY inside a disposable worktree under
    `.remedy-wt/`. The primary checkout satisfies `git status --porcelain`
    empty at every commit and at the handback.
 8. Every numeral this block states about the ROUND BASE `f51be462` was produced
    by a reviewer script or tool run at that commit and is a REFERENCE to report
    against, not a target to reproduce. Where your measurement differs, report
    BOTH and reconcile NOTHING.
 9. Size, measured by the reviewer on the final bytes of this block and stated
    once here: this block is 266 lines TOTAL with 52 CONTENT
    lines inside its slices, so PROSE is 214 — under DECISION F085 D6's
    490 and D5's 400.

─── Why this round exists ─────────────────────────────────────────────────────

R15 passed and its verdict is not on disk. Under this workflow a round records
the PREVIOUS round's verdict, so the last reviewed round of any session strands
its own — DECISION F085 D9 rules that a PASS is written by the next round's
ledger commit, and docs/agents/self_drive_protocol.md rules that the handoff is
the only return channel. R15 was the integration gate: re-deriving its verdict
costs two full-suite runs of roughly three minutes each plus a parity restore,
so leaving it unwritten is the most expensive verdict this feature could strand.
The session's round budget is spent, so rather than open closure and leave it
half-done, this round closes the books.

One item also came out of the R15 gate and belongs on disk before the session
ends: a recurrence of a standing finding that the gate procedure itself
manufactures base failures. It is recorded, not repaired — constraints 5 and 6.

─── Done when ─────────────────────────────────────────────────────────────────

Run every gate below yourself, record its REAL exit code, and put ONE LINE per
gate in the handback with the transcripts kept out of it (R-0582). Every gate
below runs after C3 and BEFORE C4, so the handback can quote all of them (§3
checklist item 31). The round base is `f51be462` throughout.

 G1  `.agent/STOP` absent, read from disk before C0a and again before C4.
     Branch `feature/f022-live-cost-ticker`. `git status --porcelain` 0 lines
     after every one of C0a, C0b, C1, C2 and C3.
 G2  TRANSPORT. sha256 over the block file at `.remedy-wt/f022-r16.md`, over the
     committed C0a blob, over the committed C0b blob and over
     `.agent/last_block.md` on disk: report all four digests, byte counts and
     line counts, and require them EQUAL. The digest the delegation names is the
     fifth reading and must agree.
 G3  EXTRACTION. Run an extractor over the COMMITTED C0a blob that finds the
     slices by their marker LINES and report how many slices and how many
     CONTENT lines it printed, plus the block's TOTAL and PROSE line counts.
     Report those against constraint 9's numerals; reconcile nothing.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF022R16 plus exactly one
     newline. NEGATIVE CONTROL: the same comparison against the BARE slice must
     be FALSE, and report both byte counts. `^## Goal$` once, `^## Next Steps$`
     once, `wc -l` at most 50.
 G5  THE PAIR at C2 in `.agent/live_review.md`. Report the containment output
     and require it to match the convention block. MAPFROM16 1x at the round
     base and 0x at C2; MAPTO16 0x at base and 1x at C2; the file's byte length
     changing by exactly `len(MAPTO16) - len(MAPFROM16)`; `^## Steps$` still
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
     `^Recurrence: R-` with its DISTINCT ids, and of `^Gate: R` with its
     distinct keys. Report the ids ADDED and REMOVED as sets. At base the
     reviewer measured 234 records, all distinct, maximum `R-0673`, 2 `Done:`
     lines over `R-0653` and `R-0670`, 0 `Landed:`, 9 `Recurrence:` lines over 8
     DISTINCT ids, and 15 `Gate:` lines over 15 distinct keys. This round MINTS
     NO NEW ID: it is expected to add no record, to take `^Recurrence: R-` to 10
     by gaining a SECOND `R-0445` line — so the DISTINCT recurrence-id count
     STAYS 8 — and to add exactly the key `R15`. `R-0445` must still occur
     exactly once as a `^- R-\d+ — ` record. Report what you measure.
 G8  THE FOUR STATE READERS plus THE CANARY, serially in the PRIMARY checkout at
     C3, exit 0: `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py`,
     `tests/orchestration/test_integrity_gate.py`, then
     `tests/cli/test_golden_path.py`. The reviewer measured 470, 52, 21 and 16
     for 559 across the four, and 42 for the canary, at the round base. Never
     run two pytest processes at once. This round rewrites `.agent/` state and
     those four are its readers. THE FULL SUITE IS NOT RE-RUN: R15 ran it twice
     and this round changes no file the suite reads.
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
     IT STILL CREATES NO PR: closure has not run, and the closure protocol
     creates the PR itself, last, after the evidence job and a FRESH review zip.
 G11 STALENESS. Every sentence C1, C2 and C3 land that states a fact about a
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
             expected to print `[]` because this session created none; (3) R17,
             CLOSURE, per docs/roadmap/STATUS_closure_protocol.md — the evidence
             job and a FRESH review zip are mandatory and a zip failure is a
             closure blocker, the reviewer authors the STATUS line, the worker
             commits it last and creates the PR, and that PR is NOT merged then
             but at the NEXT feature's Open PR Gate; (4) that R16's own verdict
             is the branch TERMINATOR under §4 item 13 — the last round of a
             session has no on-disk gate entry by construction, and the next
             session gates R16 as its first act. State plainly that the session
             ended at its declared round budget with every PRODUCTION round's
             verdict AND the integration gate's verdict on disk, which is a
             clean stop and not a blocker.
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF022R16
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
R16 records the R15 verdict, registers the R-0445 recurrence, repairs the round
map and ends the session cleanly. It builds nothing: T001, T002 and T003 are
complete, the integration gate has passed, and a verdict that lives only in a
session is a verdict that did not happen.

## Next Steps
1. R17 closure, per docs/roadmap/STATUS_closure_protocol.md — the evidence job
   and a FRESH review zip are mandatory, the reviewer authors the STATUS line,
   and the worker commits it last and creates the PR.

## Risks
- The closure PR is created but NOT merged by the round that makes it: it merges
  at the NEXT feature's Open PR Gate, which is what preserves the operator's
  manual-review window.
- Open F022 findings: R-0672 and R-0625 want their next-DECISION and
  next-numeral clauses honoured, and R-0672 gained a third instance at R14;
  R-0431, R-0413, R-0533 and R-0445 are already recorded and already paid for.
- R-0445 is a standing defect of `docs/agents/integration_gate.md` itself, not
  of this branch: its repair is routed to a follow-up branch by the finding, and
  performing it from here would be scope drift into a process doc.
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks, not F022 defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- R-0665 is open and this feature needs its route: every UI feature is told to
  record visual deviations in an `assumption_log` that does not exist. F022
  records them as DECISIONs in `.agent/decisions.md`, a route rather than a fix.
<<<END PLANF022R16

<<<SLICE MAPFROM16
reconciliation with its delta label → R15 the integration gate → R16 closure.
This section is the only place the round map is stated, per
<<<END MAPFROM16

<<<SLICE MAPTO16
reconciliation with its delta label → R15 the integration gate → R16 record the
R15 verdict and end that session at its round budget → R17 closure. This
section is the only place the round map is stated, per
<<<END MAPTO16

<<<SLICE LEDGER16
Recurrence: R-0445 — THE INTEGRATION-GATE PROCEDURE MANUFACTURED ITS BASE FAILURES AGAIN, AND THIS TIME IT MANUFACTURED SIXTY-THREE OF THEM. Second instance recorded in this ledger, at F022 R15. NO NEW ID IS MINTED: §3 checklist item 30 requires the open set searched for the DEFECT before an id, and R-0445 already describes this mechanism to the line. Its own words: "a copy preserves the SOURCE mtime while `git worktree add` stamps the freshly checked-out sources with the checkout time, so the copied build is ALWAYS older than the sources it was built from. `ui_server.py::_frontend_is_stale` therefore returns True, `::_auto_build_frontend` returns None under the flag the same procedure sets, and `::_load_frontend` calls `sys.exit(1)`". THE INSTANCE, MEASURED BY THE WORKER IN THE BASE WORKTREE ITSELF AND RE-READ BY THE REVIEWER FROM `.agent/gate_f022_r15/`: the copied `apps/ui/dist/index.html` carried mtime 1787467082.0774689 while all 92 files under `apps/ui/src` were newer, the newest at 1787467200.83286, so `_frontend_is_stale()` returned True with the pre-run mtime and False with the post-run one. The base run at `c34ef32b` exited 1 with 63 failed against 17588 passed, and all 63 of the failing ids carry BOTH `Failed: Server did not start in time` and the captured stderr `ERROR: React UI not built.`, with 0 carrying any other signature. WHAT THIS ADDS TO R-0445, AND IT IS THE REASON A RECURRENCE IS WORTH WRITING: the finding's own headline says EIGHT, naming `tests/ui_server/test_live_state.py::TestUIServerIntegration`, and F022 R15 measured SIXTY-THREE, in `tests/ui_server/test_command_channel.py` at 61 and `tests/ui_server/test_command_dispatch.py` at 2 — while F021 R38 measured 78 by the same route. The count is not a property of the defect, it is a property of how many tests happen to start the UI server on the day the gate runs, and it grows as the suite grows. A finding whose headline carries a numeral will be read as bounded by it, so the number to carry forward is NOT eight: it is every id that starts the UI server. THE MASKING RISK R-0445 NAMES IS UNCHANGED AND WAS NOT REALISED HERE: masking hides BASE-only ids, and F022's branch-only set is empty over a full suite the reviewer re-ran itself, so nothing of this branch's could have hidden behind it. ALSO OBSERVED, REPORTED AND DELIBERATELY NOT MINTED: `REMEDY_UI_NO_AUTO_BUILD=1` did not prevent a rebuild EVENT — the base worktree's `dist` gained new asset filenames and new digests roughly 100 seconds into the run — but docs/agents/integration_gate.md already states that the flag is "NOT trusted alone" for exactly this reason and already prescribes the counter-measure the worker used, so the procedure behaved as documented rather than surprisingly, and there is no defect here that is not already R-0445's. THE REPAIR REMAINS ROUTED where R-0445 routes it, to `docs/agents/integration_gate.md` on a follow-up branch: after the parity copy, touch `apps/ui/dist/index.html` forward of every file under `apps/ui/src`, and have the procedure assert `_frontend_is_stale()` is False BEFORE the base run rather than discovering it afterwards.

Gate: R15 — the F022 R15 entry. R15 PASSED ON EVERY ONE OF ITS FIFTEEN GATES, AND THE REVIEWER RE-RAN THE FULL SUITE ITSELF RATHER THAN READING THE GATE'S WORD FOR THE ONE CLAIM THAT MATTERS. THE INTEGRATION GATE'S FINDING IS THAT THIS BRANCH INTRODUCES NO FAILURE. The reviewer's own `python3 -m pytest -n auto -q` from the repository root at `f51be462` exited 0 with `17722 passed, 20 skipped` in 156.53 s and ZERO `^FAILED` lines, reproducing the worker's branch run of `17722 passed, 20 skipped` in 177.04 s exactly on both counts. The branch-only set is therefore empty for a reason stronger than a comparison: the branch side has no failures at all, so `comm -13` could not have produced anything whatever the base did. The recurrence above is written in THIS SAME COMMIT, which the R16 block's constraint 4 fixes. TRANSPORT HELD IN ITS STRONGEST FORM, disk to disk and not by the digest fallback: the reviewer's own scratch original at `.remedy-wt/f022-r15.md`, the committed C0a blob, the committed C0b blob and `.agent/last_block.md` on disk are ALL sha256 `639788e0238299fbdf0879a13cf0bde8343a3974880b1ec2d674fbdfa9cc6ad8` over 29128 bytes and 296 lines, and C0a and C0b resolve to the SAME git blob `3f1d412d`. THE EXTRACTION printed 2 slices over 47 CONTENT lines against a TOTAL of 296, so PROSE is 249 and constraint 10 reproduces exactly. `.agent/plan.md` at `a97dfac3` is 2508 bytes = PLANF022R15's 2507 plus one newline, the BARE-slice control FALSE, headings once each, 44 lines against the cap of 50. THE APPEND HOLDS UNDER BOTH READERS at `0486eddf`: the C1 blob is a byte-exact PREFIX of the C2 file and the remainder is 9861 = 1 + LEDGER15's 9859 + 1, while the reviewer's own independent blank-line split counted N=2 paragraphs and found the LAST 2 units equal to them IN ORDER over 276 units becoming 278. THE SETS MOVED EXACTLY WHERE THE ROUND PROMISED: 234 records at base and at C2, all DISTINCT at both with maximum `R-0673`, ids ADDED and ids REMOVED both the EMPTY SET so NO ID WAS MINTED, `^Recurrence: R-` 8 becoming 9 over 8 DISTINCT ids by gaining a SECOND `R-0672` line, and `^Gate: R` 14 becoming 15 by gaining exactly the key `R14`. THE BASE RUN IS RED AND THAT IS NOT THIS BRANCH'S DOING: it exited 1 with 63 failed at `c34ef32b`, every one attributed by three independent evidences to the environment class recorded above, and the reviewer confirmed independently that all 63 ids live in `tests/ui_server/test_command_channel.py` and `tests/ui_server/test_command_dispatch.py`, neither of which F022's path set has ever touched. THE PARITY CLAIM WENT VOID AND THE ROUND SAID SO INSTEAD OF SMOOTHING IT: G9 measured 3 of 3 `dist` files with mtimes inside the run window, both asset FILENAMES changed and no sha256 matching its pre-run value, which is a real rebuild rather than a byte-identical one — the R-0444 remedy of measuring the EVENT rather than the outcome, working exactly as it was written to. THE ROUND'S CONTROL DISCIPLINE IS THE BEST THIS FEATURE HAS SEEN, and two of its five controls were not ordered by the block at all: the `^FAILED` extractor was proved live against a two-test module OUTSIDE the repository so that "0 FAILED lines" is a measurement rather than a silent miss, and the `comm` route was proved to report with a synthetic pair placing one id in each direction — both of them backing readings whose value is EMPTY, which is precisely where a gate is easiest to fool. The ordered three also held: the parity restore moved the base worktree's `.bin` from 0 symlinks to 23 equalling the primary's, the canary went red under a mutated assertion naming the mutated test, and the append readers both rejected a one-byte mutant at BYTE offset 574400. STRUCTURE HELD: 5 commits before the handback, every one single-parent, insertions 296, 195, 15, 4 and 474, each under the 500 cap; the range path set differs from the Change set only by `.agent/handoff.md`, which is C4's own; the anchored markers count 0 in both state files; `git ls-files .remedy-wt` is 0; one worktree with both temporary branches deleted; and amend, rebase and cherry each 0. THE HANDBACK at `f51be462` IS COMPLIANT at 147 lines with a DECISION D15 stated cause naming that same 147. THE OPEN PR GATE printed an empty JSON array and no PR was created. THE VERDICT IS PASS: the full suite is green on this branch under the reviewer's own run, every base-only id is accounted for by a defect the record already holds, no id was minted, no slice was edited, and F022 has now cleared the only tier that is permitted to say "this branch introduces no failures".
<<<END LEDGER16
