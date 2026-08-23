── STEP CLOSURE 3/3 — F022 Live cost ticker · Runde 19 ───────────────────────

Fortschritt: ~100 % (T001, T002 und T003 gebaut und verifiziert ·
             Integrations-Gate BESTANDEN · Evidence-Job und Review-Zip gebaut ·
             STATUS-Zeile, README-Sync und Pull Request in dieser Runde —
             danach ist F022 fertig) — Schaetzung

Goal:        Close F022. Record the R18 verdict, then flip the roadmap ledger's
             `[~]` to `[x]` with the values only R18's package could produce,
             sync the README capability list in the SAME commit so the two can
             never disagree in any committed state, carry this closure's one
             candidate onto disk, and open the pull request. The PR is NOT
             merged this session: it merges at the next feature's Open PR Gate,
             and that gap is the operator's manual-review window.

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the plan ·
             C2 the R18 verdict · C3 the closure commit, which is the STATUS
             line, the three README sync pairs, the candidates file and the
             handback together · then the pull request.

Change:      Exactly these paths, nothing else:
               .agent/authored/f022-r19.md      (C0a)
               .agent/last_block.md             (C0b)
               .agent/plan.md                   (C1)
               .agent/live_review.md            (C2)
               docs/roadmap/STATUS.md           (C3)
               README.md                        (C3)
               .agent/candidates.md             (C3)
               .agent/handoff.md                (C3)
             This list bounds what you WRITE. It does not bound what you DO:
             G11 orders a push and G12 orders the pull request, and AGENTS.md
             Push Discipline binds whether or not any block names it (finding
             R-0674).

─── Slice convention ──────────────────────────────────────────────────────────
Each authored text below begins at its `<<<SLICE <name>` line and ends at its
`<<<END <name>` line; neither marker line is part of the slice, and no slice
contains a marker line. Extract them PROGRAMMATICALLY by marker line out of the
committed C0a blob — never retype, never rewrap, never reflow. The whole-text
slices are PLANF022R19, LEDGER19 and CANDIDATES. The remaining slices are the
halves of FROM/TO pairs, named STATUSFROM/STATUSTO, RM1FROM/RM1TO,
RM2FROM/RM2TO and RM3FROM/RM3TO. Every slice is quoted WITHOUT its trailing
newline; PLANF022R19 and CANDIDATES each replace their file whole as the slice
plus exactly one newline, and LEDGER19 lands as one newline plus the slice plus
one newline.

CONTAINMENT TEST, run by the reviewer on the final bytes, output quoted, one
reading per pair and none generalised to the rest:
  STATUSFROM/STATUSTO — `TO contains FROM: false` → REWRITE.
  RM1FROM/RM1TO       — `TO contains FROM: false` → REWRITE.
  RM2FROM/RM2TO       — `TO contains FROM: false` → REWRITE.
  RM3FROM/RM3TO       — `TO contains FROM: false` → REWRITE.

Constraints:
 1. NEVER edit a slice. Apply it byte for byte. If a slice contradicts a fact
    you measure, apply it anyway and DECLARE the contradiction in the handback
    under Deviations. Repair nothing outside your slices; rule on nothing.
 2. C1 is the FIRST substantive commit (§3 checklist item 23): this round writes
    the finding ledger, so the plan advances before anything else but the two
    block-save commits.
 3. COMMIT ORDER IS C0a, C0b, C1, C2, C3 and no other. C3 IS THE LAST COMMIT ON
    THIS BRANCH (Rule A4) and it carries the STATUS edit, all three README pairs,
    the candidates file and the handback TOGETHER — the README capability sync
    lands in the SAME commit as the `[x]` edit because README and STATUS may
    never disagree in any committed state (R-0154, the ledger cross-check pin).
 4. APPLY THE FOUR PAIRS BEFORE ANY WHOLE-FILE WRITE in the same target, and
    apply each pair exactly once (R-0639/R-0640). Each FROM occurs exactly once
    in its target at the round base; the reviewer measured that and G7 orders
    you to measure it again.
 5. NO PRODUCTION CODE, NO TESTS, NO NEW DOCS. The closure commit's path set is
    fixed by docs/roadmap/STATUS_closure_protocol.md step 5 and holds no feature
    file: the Built State landed at R17 and is not touched again.
 6. NO REPAIR of any open finding, and NO NEW FINDING ID. This round mints
    nothing: the one thing this closure review raised is a CANDIDATE, and the
    closure protocol reserves ids for the NEXT session's first reviewed round.
 7. Destructive verification runs ONLY inside a disposable worktree under
    `.remedy-wt/`, removed BY ITS EXACT PATH and never by a glob (R-0662). The
    primary checkout satisfies `git status --porcelain` empty at every commit.
 8. Every numeral this block states about the ROUND BASE `9a1e677f` was produced
    by a reviewer script or tool run at that commit and is a REFERENCE to report
    against, not a target to reproduce. Where your measurement differs, report
    BOTH and reconcile NOTHING.
 9. Size, measured by the reviewer on the final bytes of this block and stated
    once here: this block is 356 lines TOTAL with 97 CONTENT
    lines inside its slices, so PROSE is 259 — under DECISION F085 D6's
    490 and D5's 400.
10. THE PACKAGE IS NOT REBUILT. R18 built it from a clean tree at `f215ced4`,
    the reviewer verified its SHA-256 over the published file and read its
    manifest, and the STATUS line names that head. Building a second package
    now would name a head the verdict does not cover.

─── Why this round exists ─────────────────────────────────────────────────────

R18 passed every one of its fourteen gates under the reviewer's own re-runs and
its verdict is not on disk, so C2 writes it: DECISION F085 D9 rules that a PASS
is written by the NEXT round's ledger commit, and Rule A4 does not seal the
branch against that. The closure values exist for the first time — evidence job
`f022-closure`, the package `remedy-review-20260823-135731-READY_FOR_REVIEW.zip`
and its SHA-256 — which is exactly why the STATUS line could not be authored
before R18 ran (finding R-0371, whose third instance R18 registered).

This round's own verdict will have no on-disk gate entry, by construction. Every
reviewed round records its verdict in `.agent/live_review.md`, but the round
that writes that record cannot record the gate on itself, so every branch ends
with one round whose verdict lives only in `.agent/handoff.md` and in the pull
request. That absence is the TERMINATOR and not a missing gate (§4 item 13): do
not open a repair round to close it.

─── Done when ─────────────────────────────────────────────────────────────────

Run every gate below yourself, record its REAL exit code, and put ONE LINE per
gate in the handback with the transcripts kept out of it (R-0582). Gates G1
through G10 all run BEFORE C3, so the handback can quote every one of them
(§3 checklist item 31). G11 and G12 run after C3 and their outcomes are NOT
values of any file this round writes — they are reported to the reviewer, which
is where the next session will read them. The round base is `9a1e677f`.

 G1  `.agent/STOP` absent, read from disk before C0a and again before C3.
     Branch `feature/f022-live-cost-ticker`. `git status --porcelain` 0 lines
     after every one of C0a, C0b, C1 and C2.
 G2  TRANSPORT. sha256 over the block file at `.remedy-wt/f022-r19.md`, over the
     committed C0a blob, over the committed C0b blob and over
     `.agent/last_block.md` on disk: report all four digests, byte counts and
     line counts, and require them EQUAL. The digest the delegation names is the
     fifth reading and must agree.
 G3  EXTRACTION. Run an extractor over the COMMITTED C0a blob that finds the
     slices by their marker LINES and report how many slices and how many
     CONTENT lines it printed, plus the block's TOTAL and PROSE line counts.
     PROSE is TOTAL minus CONTENT, so the marker lines count as prose. Report
     those against constraint 9's numerals; reconcile nothing.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF022R19 plus exactly one
     newline. NEGATIVE CONTROL: the same comparison against the BARE slice must
     be FALSE, and report both byte counts. `^## Goal$` once, `^## Next Steps$`
     once, and `wc -l` STRICTLY UNDER 50 — AGENTS.md caps this file at fewer
     than 50 lines, so report the number you measure.
 G5  APPEND at C2, proved twice. The base blob is a byte-exact PREFIX of the
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
     ~20 bytes surrounding the flip. Remove the worktree by its exact path;
     `git worktree list` back to one line.
 G6  LEDGER INTEGRITY, base versus C2. Report for both points: the count of
     lines matching `^- R-\d+ — `, whether they are all DISTINCT, the MAXIMUM
     id, the count of `^Done: R-` with its distinct ids, of `^Landed: `, of
     `^Recurrence: R-` with its DISTINCT ids, and of `^Gate: R` with its
     distinct keys. Report the ids ADDED and REMOVED as sets. At base the
     reviewer measured 237 records, all distinct, maximum `R-0676`, 2 `Done:`
     lines over `R-0653` and `R-0670`, 0 `Landed:`, 11 `Recurrence:` lines over
     9 DISTINCT ids, and 18 `Gate:` lines over 18 distinct keys, none of them
     `R18`. THIS ROUND MINTS NO ID: the ids ADDED and the ids REMOVED must BOTH
     be the EMPTY SET, the record count and the maximum UNCHANGED at 237 and
     `R-0676`, the `Recurrence:` readings UNCHANGED at 11 over 9, and the
     `Gate:` keys must gain exactly `R18`. Report what you measure.
 G7  THE FOUR PAIRS at C3. For EACH pair separately report: the containment
     output, the count of the FROM in its target at the round base and at C3,
     and the count of the TO at both. Every FROM is 1 then 0; every TO is 0 then
     1. Then report, in `docs/roadmap/STATUS.md` at C3, the count of
     `^- \[~\] F\d+ — ` which must be 0, and of `^- \[x\] F\d+ — ` which must be
     57; the reviewer measured 1 and 56 at the base. Report also that each
     edited file equals its base with ONLY its own pairs applied and nothing
     else.
 G8  THE CROSS-CHECK PIN AND THE DOCS ROUND GATE. Because the Change set holds
     `docs/roadmap/**`, run in the PRIMARY checkout at C3 and report the REAL
     exit code of `python3 -m pytest tests/docs/ -q` and of
     `python3 -m pytest tests/orchestration/test_roadmap_index.py -q`, then the
     canary `python3 -m pytest tests/cli/test_golden_path.py -q`. The reviewer
     measured 295, 30 and 42 at the round base, all exit 0. Never run two pytest
     processes at once (R-0619). THE FULL SUITE IS NOT RE-RUN: R18 ran it and
     the reviewer re-ran it independently at `f215ced4`, both reading
     `17722 passed, 20 skipped`.
 G9  STRUCTURE, reported for the commits BEFORE C3 and for the range as a whole
     (C3's own numbers belong to the next session's record, not here): every
     commit single-parent; each commit's INSERTION count, each under the 500
     cap; the range path set against the Change set above with the difference
     reported in BOTH directions; `git show --numstat` agreeing cell by cell
     with the handback's `## Commits` table; the LINE-ANCHORED patterns
     `^<<<SLICE ` and `^<<<END ` counting 0 in each of `.agent/plan.md`,
     `.agent/live_review.md`, `docs/roadmap/STATUS.md`, `README.md` and
     `.agent/candidates.md`; `git ls-files .remedy-wt` 0; `git ls-files` over
     the published zip 0; one worktree; and the round's reflog rows with amend,
     rebase and cherry counted IN THE OPERATION FIELD before the first colon
     (R-0613), each 0.
 G10 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
     BEFORE C3. Report it verbatim; the reviewer measured `[]`. If it is not
     empty, STOP and report rather than creating a second PR.
 G11 PUSH, after C3: `git push origin feature/f022-live-cost-ticker`. No
     `--force`, no `--force-with-lease`, no history rewrite, no branch deletion.
 G12 THE PULL REQUEST, after the push:
     `gh pr create --base main --head feature/f022-live-cost-ticker`. Its
     description carries what changed and why, the key DECISIONs F022 D1 through
     D8, how to review, a changed-files summary, the latest verdict, the open
     findings count and the runtime actuals. DO NOT MERGE IT. Neither the PR
     number nor the push outcome is a value of any file this round writes — C3
     is authored before either exists — so report both in your completion report
     to the reviewer and write NEITHER into `.agent/handoff.md`, which states
     them only as intents (finding R-0371, third instance registered at R18).

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             every mandated section in order, one changed-files table per
             commit, an item-status row per Bundle item, the round base SHA, ONE
             line per gate, a `## Closure values` table carrying the verdict,
             accepted HEAD, evidence job, package, package SHA-256, the STATUS
             and README counts and the open-findings count, and the
             `Fortschritt:` block above carried VERBATIM across all five of its
             lines. Every count you report names the exact string or pattern
             counted and the file it was counted in (R-0442). THE CAP IS THE
             AGENTS.md ONE: read `### handoff.md` there and apply the tier that
             genuinely fits this round's commit count, declaring a DECISION D15
             stated cause with your own measured numeral only if the mandated
             content exceeds the tier that applies (finding R-0676). C3's own
             numstat, its SHA and the PR number cannot exist inside the file C3
             writes (§3 item 31); write `n/a` in those cells and say why once.
             `## Next` states that F022 is CLOSED, that the pull request is open
             and NOT merged, and that the next session's Open PR Gate merges it
             before claiming the next feature — and that the next session's
             FIRST reviewed round registers or rules the entry
             `.agent/candidates.md` carries and empties that file.
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF022R19
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
R19 closes F022. It records the R18 verdict, flips the STATUS line to `[x]`
with the evidence job, package and SHA-256 that R18 produced, syncs the README
capability list in that same commit, writes this closure's one candidate to
`.agent/candidates.md`, and opens the pull request without merging it.

## Next Steps
1. The next session's Open PR Gate merges this pull request before any new
   feature is claimed, which is the operator's manual-review window.
2. That session's FIRST reviewed round registers or rules the candidate this
   round records and empties `.agent/candidates.md` in the same round.

## Risks
- The closure PR is created but NOT merged by the round that makes it. Merging
  it here would close the operator's only review window.
- This round's own verdict has no on-disk gate entry by construction (§4 item
  13). It lives in `.agent/handoff.md` and in the pull request, and no repair
  round is opened for that gap.
- Open F022 findings: R-0672 and R-0625 want their next-DECISION and
  next-numeral clauses honoured; R-0431, R-0413 and R-0533 are recorded and
  already paid for; R-0674, R-0675 and R-0676 are registered and repaired by
  none, their subjects being landed append-only text; and R-0445 is a standing
  defect of `docs/agents/integration_gate.md`, routed by the finding itself.
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks, not F022 defects.
- R-0403 is open and this package shows it: `.remedy-wt/` scratch is a large
  share of every review zip built on this machine. It routes to a paydown
  branch and is not an F022 defect.
<<<END PLANF022R19

<<<SLICE LEDGER19
Gate: R18 — the F022 R18 entry. R18 PASSED ON EVERY ONE OF ITS FOURTEEN GATES, AND THE REVIEWER RE-RAN EVERY ONE OF THEM ITSELF RATHER THAN READING THE HANDBACK'S WORD FOR ANY OF THEM. THE ROUND'S SUBSTANCE IS THAT F022 NOW HAS A PACKAGE: a fresh feature-scoped evidence bundle and a FRESH review zip built from a clean tree at the reviewed head, which are the three values the STATUS line could not be authored without. TRANSPORT HELD IN ITS STRONGEST FORM: the reviewer's own scratch original at `.remedy-wt/f022-r18.md`, the committed C0a blob, the committed C0b blob and `.agent/last_block.md` on disk are ALL sha256 `3b4a5683ae7ebd92dd9ffb5588c3ea756ca574406bc21434987be887147d4ad6` over 36770 bytes and 458 lines, and C0a and C0b resolve to the SAME git blob `dc52827b`. THE EXTRACTION printed 3 slices over 190 CONTENT lines against a TOTAL of 458, so PROSE is 268 and constraint 9 reproduces exactly. `.agent/plan.md` at `3d4678b8` is 2671 bytes, which is PLANF022R18's 2670 plus one newline, the BARE-slice control FALSE, `^## Goal$` and `^## Next Steps$` once each, and 46 lines strictly under the cap of 50. THE APPEND AT `f215ced4` HOLDS UNDER BOTH READERS: the base blob is a byte-exact PREFIX of the committed file and the remainder is 9891 bytes, which is one newline plus LEDGER18's 9889 plus one newline, while an independent blank-line split counted N as 3 paragraphs and found the LAST 3 units equal to them IN ORDER, 283 units becoming 286; the worker's byte-flip control at offset 602979 is rejected by both readers while both accept the true file. THE SETS MOVED EXACTLY WHERE THE ROUND PROMISED: 236 records becoming 237, all DISTINCT at both, maximum `R-0675` becoming `R-0676`, ids ADDED exactly `R-0676` with ids REMOVED the EMPTY SET, `^Done: R-` 2 and 2, `^Landed: ` 0 and 0, `^Recurrence: R-` 10 over 8 becoming 11 over 9 by gaining a FIRST `R-0371` line, and `^Gate: R` 17 becoming 18 by gaining exactly the key `R17`. THE FULL SUITE IS GREEN ON THIS BRANCH UNDER THE REVIEWER'S OWN RUN, which is closure precondition 2 re-confirmed rather than re-litigated: `python3 -m pytest -n auto -q` exited 0 at `17722 passed, 20 skipped` in 187.41 s, reproducing the worker's own 17722 and 20 in 137.75 s exactly on both counts, and the worker proved its `^FAILED` extractor could match before reporting zero. INTEGRITY PASSED with 5 of 5 checks, `fail_count` 0 and no open blocker or high findings, over a working tree whose `git status --porcelain` printed 0 lines. THE EVIDENCE JOB IS `f022-closure` and its script asserted every precondition that has historically produced a BLOCKED_EVIDENCE package before writing anything: the four scoped suites selected 10, 16, 15 and 30 with node-id counts equal to selected and 0 deselected, every `test_files` entry a real sorted file, the packager's OWN `_unsafe_text` scanner rejected 0 of the packaged strings while its red control bit, and all four `output_hash` values equal sha256 of their `stdout_summary` exactly — the pitfall that blocked the F083 closure. THE PACKAGE IS `remedy-review-20260823-135731-READY_FOR_REVIEW.zip` at sha256 `85fe27aaeefe0b885b6b2fe081187cff51a0e070ae7d9d5320e7d57d1e150f58`, and the reviewer recomputed that digest over the published 68628435-byte file itself rather than quoting the build's line. Its manifest reads `package_status` `READY_FOR_REVIEW`, `review_subject_alignment` `PASS`, `committed_review_subject.base_commit` `c34ef32b0ac3e6a7af161fa724f42ba1c3167786` — this branch's point of departure — and `.head_commit` `f215ced4998f6eb6e5ca82117d889b70777ffe12`, which is C2 and is therefore the `accepted HEAD` the STATUS line names. THE PACKAGE ALSO SHOWS TWO ALREADY-REGISTERED DEFECTS AND NEITHER IS NEW: its alignment block reports `dirty_file_count_total` 1 beside empty lists, which is R-0666, and a large share of its 11924 members is `.remedy-wt/` scratch, which is R-0403. STRUCTURE HELD: 4 commits before the handback, every one single-parent, insertions 458, 350, 17 and 6, each under the 500 cap; the range path set minus the Change set EMPTY and the Change set minus the range exactly `.agent/handoff.md`, which is C3's own; the anchored markers count 0 in both state files; `git ls-files` is 0 for `.remedy-wt`, for the evidence directory and for the published zip, so neither artifact entered the repository; one worktree; and amend, rebase and cherry each 0 in the reflog's OPERATION field. THE OPEN PR GATE printed an empty JSON array and no PR was created. THE ROUND DECLARED TWO DEVIATIONS AND BOTH ARE HONEST: it resolved the handback cap to the 60-line tier itself, correctly, because five commits is not more than five per-commit tables, and declared its measured 83 lines against it — which is finding R-0676's counter-measure working the first time it was tried; and it disclosed that the evidence script and the zip were each run twice, the first pair without a measurable exit code because this session's shell guard rejects the form that reads one, with the superseded package deleted BY ITS EXACT PATH and never by a glob. THE VERDICT IS PASS: every gate reproduced under the reviewer's own execution, the full suite is green, the package is READY_FOR_REVIEW over the right base and the right head, and F022 has everything closure requires.
<<<END LEDGER19

<<<SLICE STATUSFROM
- [~] F022 — Live cost ticker
<<<END STATUSFROM

<<<SLICE STATUSTO
- [x] F022 — Live cost ticker (T001–T003 complete; accepted 2026-08-23 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f022-closure · package remedy-review-20260823-135731-READY_FOR_REVIEW.zip · SHA-256 85fe27aaeefe0b885b6b2fe081187cff51a0e070ae7d9d5320e7d57d1e150f58 · accepted HEAD f215ced4998f6eb6e5ca82117d889b70777ffe12)
<<<END STATUSTO

<<<SLICE RM1FROM
56 of 255 registered items accepted. Next: F022 (Live cost ticker).
<<<END RM1FROM

<<<SLICE RM1TO
57 of 255 registered items accepted. Next: F031 (Decision inbox).
<<<END RM1TO

<<<SLICE RM2FROM
| 5 | Operator Cockpit | 4 | 29 |
<<<END RM2FROM

<<<SLICE RM2TO
| 5 | Operator Cockpit | 5 | 29 |
<<<END RM2TO

<<<SLICE RM3FROM
feed rows that carry their seq and focus their node on click).

Full per-feature state:
<<<END RM3FROM

<<<SLICE RM3TO
feed rows that carry their seq and focus their node on click).
F022 live cost ticker (the COST tile renders from budget tick events with a bar
fill against the limit, a '~' prefix and tooltip whenever the basis is
estimated, a warn band at 85 % of the token limit, a spent-only variant for
limitless jobs, and the ledger's own final figure replacing the live one at
terminal with any delta labelled).

Full per-feature state:
<<<END RM3TO

<<<SLICE CANDIDATES
# Closure Candidates — carrier of record

> Written per docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate
> findings", disk-vehicle rule, operator ruling 2026-08-01). Read at Window-1
> session bootstrap (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present at
> feature-claim time is a block condition.

NON-EMPTY. One candidate, raised by the reviewer during the F022 closure review
and recorded here without an id because the closure protocol reserves ids for
the next session's first reviewed round. It was MEASURED by the reviewer at
`9a1e677f`, not read back out of a handback.

- FIVE HISTORICAL REVIEW PACKAGES WERE CREATED AT ONE INSTANT DURING THIS
  SESSION AND NOTHING IN THE SESSION'S RECORD ACCOUNTS FOR IT · F022 R19 ·
  2026-08-23. `stat` reports that `remedy-review-20260726-001936-`,
  `-20260726-165629-`, `-20260726-202004-`, `-20260726-215057-` and
  `-20260727-101857-READY_FOR_REVIEW.zip` each carry an mtime EQUAL to their
  ctime at 2026-08-23 13:29:18, all five within 44 milliseconds of each other,
  while their filenames date them to 2026-07-26 and 2026-07-27. Equal mtime and
  ctime means the bytes were WRITTEN at that instant rather than merely touched,
  so five packages named for July were created during this August session by a
  step no round ordered and no handback records. Nothing about F022's closure
  rests on them: this feature's package is
  `remedy-review-20260823-135731-READY_FOR_REVIEW.zip`, the reviewer recomputed
  its SHA-256 over the published file and read its manifest, and all five of
  these are outside the review subject and gitignored. The reason to record it
  anyway is R-0662: a glob in the F021 R40 closure destroyed roughly 78
  historical review packages on this machine, so packages APPEARING
  unaccountably is the same blind spot from the other side, and a restore nobody
  can name is not better than a deletion nobody intended. Candidate
  counter-measure: identify what writes those files — a recovery path in the
  packaging pipeline, a worktree operation, or an operator action — and either
  make it say so, or establish that the five are byte-identical to what the
  filenames claim and record where the originals were kept.
<<<END CANDIDATES
