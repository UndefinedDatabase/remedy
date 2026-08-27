STEP CLOSURE 3 OF 3 / F031 — DECISION INBOX
Goal:        CLOSE F031. Record the RECORD ROUND's verdict, which is PASS on
             every gate its block ordered and which the reviewer re-ran in
             full. Register ONE new finding `R-0709` for a defect the open set
             does not hold. Record the reviewer's ruling on closure
             precondition 2 as DECISION F031 D27. Then flip
             `docs/roadmap/STATUS.md` from `[~]` to `[x]` with the README
             capability sync in the SAME commit, and create the pull request.
             THE PULL REQUEST IS NOT MERGED THIS SESSION AND YOU MERGE NOTHING.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the
             plan · C2 the ledger append · C3 the decision · C4 THE CLOSURE
             COMMIT · then push · then create the pull request.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r72.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/decisions.md`, `docs/roadmap/STATUS.md`, `README.md`,
             `.agent/candidates.md`, `.agent/handoff.md`. This list bounds what
             you WRITE INTO THE REPOSITORY. It does NOT bound what you DO: G11
             orders a push and G12 orders a pull request. NOTHING under
             `apps/`, `packages/` or `tests/`, and under `docs/` ONLY
             `docs/roadmap/STATUS.md`.

Constraints:
 1. THIS BLOCK REACHES YOU AS A FILE, NOT AS PROSE IN A PROMPT. Read
    `.remedy-wt/f031-r72.md` from disk and copy it BYTE FOR BYTE to
    `.agent/authored/f031-r72.md` — with `shutil.copyfile` or a read-then-write
    in python, never by retyping it and never with `cp`, which this session's
    guard rejects. This block asserts NO digest of its own, because a digest
    written inside the text it measures cannot be true; G2 has you measure four
    points and prove them EQUAL, and the reviewer holds the scratch value
    independently.
 2. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. A slice's text is its content lines joined with a newline
    plus ONE trailing newline. If a slice contradicts something you measure,
    apply it anyway and DECLARE the contradiction in the handback under
    Deviations — a corrected slice destroys the transport proof. Declaring
    beats fixing every time, because a declared contradiction reaches a
    reviewer who can measure it while a silent fix reaches nobody.
 3. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4. Every sentence in
    LEDGER72 and in DECISION27 that describes THIS round's own landed change
    depends on that order, and this constraint is what fixes it. C4 IS THE LAST
    COMMIT ON THIS BRANCH — Rule A4 of docs/roadmap/STATUS_closure_protocol.md
    puts the STATUS edit last, and nothing follows it.
 4. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES THE RECORD ROUND.
    That is ordered: the plan becomes current at C1.
 5. NOTHING IS EDITED OUT OF THE LEDGER. `.agent/live_review.md` is APPEND-ONLY
    and so is `.agent/decisions.md`. No existing paragraph of either is
    rewritten, deleted or touched. This round's additions are NEW paragraphs
    appended after them. An append-only record is corrected by appending.
 6. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Gate:` paragraph of
    your own, never mint a finding id and never author a `Done:` line. LEDGER72
    carries the round's gate entry and ONE newly minted finding. NO FINDING IS
    RESOLVED THIS ROUND. If you find a further defect, report it in the
    handback under Deviations and let the reviewer rule on it.
 7. THE LEDGER SETS MOVE AS FOLLOWS ACROSS C2. `^Gate: F\d+ R\d+ — ` moves 52
    to 53 with the ADDED key exactly `F031 R71`. `^- R-\d+ — ` moves 269 to 270
    with the ADDED id exactly `R-0709`. `^Done: R-\d+ — ` stays 17,
    `^Landed: R-` stays 0 and `^Gate: R\d+ — ` stays 19. The open set is 252
    before C2 and 253 after C2, and the maximum id is `R-0708` before and
    `R-0709` after.
 8. RE-READ `.agent/STOP` FROM DISK before C0a and again before C4. If it
    exists at either reading, finish the commit in hand, write the handback and
    STOP — do NOT create the pull request. Never create it, never delete it.
 9. NOTHING DESTRUCTIVE IS ORDERED THIS ROUND. Create no worktree. The primary
    checkout reads `git status --porcelain` 0 lines at every commit.
10. YOUR HANDBACK FITS THE TIER ITS BUNDLE EARNS. Read the `### handoff.md`
    section of AGENTS.md, count the commits this Bundle orders, and derive your
    own cap from that rule — do not take a number from this block. Write NO
    BLANK LINE between a `###` commit heading and its table, none between a
    `##` heading and its first line, and none between one commit block and the
    next. IF AND ONLY IF the MANDATED content still does not fit in that shape,
    declare a DECISION D15 stated-cause overage — and THAT DECLARING LINE
    STATES YOUR OWN MEASURED LINE COUNT AS A NUMERAL, beside the specific
    mandated content that caused it. Never forward that number to your
    completion report or any other channel that does not survive the session.
    This is the standing rule the OPEN finding `R-0430` carries.
11. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `${...}` and every other expansion, `cp`, brace literals
    containing a quote character, `cd x && y`, file redirects, and every form of
    environment assignment. Route anything that counts, hashes or compares
    through a quoted python heredoc, read real exit codes from
    `subprocess.run(...).returncode`, and pass `cwd=` rather than `cd`. Run
    pytest SERIALLY — never two pytest processes alive at once. `--timeout` IS
    NOT AVAILABLE to pytest here: passing it exits 4 and reports no failure.
12. EVERY NUMERAL THIS BLOCK STATES ABOUT THE ROUND BASE `f7cc2dd2` was
    measured by the reviewer at that commit. It is a REFERENCE to report
    against, NOT a target to reproduce. Where your measurement differs, report
    BOTH and reconcile NOTHING.
13. THE FOUR REPLACEMENT PAIRS ARE CLASSIFIED BY A MECHANICAL CONTAINMENT TEST
    THE REVIEWER RAN, one reading per pair, and the output is printed here.
    SFROM/STO — `TO contains FROM: false`, so REWRITE. RFROM1/RTO1 —
    `TO contains FROM: false`, so REWRITE. RFROM2/RTO2 —
    `TO contains FROM: false`, so REWRITE. RFROM3/RTO3 —
    `TO contains FROM: true`, so APPEND, and for that pair you prove the §4.9
    APPEND obligation and NEVER a FROM-zero count. Each FROM occurs EXACTLY
    ONCE in its target at `f7cc2dd2`, which the reviewer measured.
14. THIS IS THE LAST ROUND OF ITS SESSION AND THE LAST ROUND OF THIS BRANCH.
    This session delegated exactly ONE round — this CLOSURE ROUND, which
    terminates it. A SESSION line naming that roster, including this
    terminating round itself, belongs in the handoff. Per
    docs/agents/planner_reviewer_prompt.md §4 item 13 this round gets NO gate
    entry of its own in `.agent/live_review.md`, by construction: that absence
    is the TERMINATOR and not a missing gate, and its verdict lives in the
    handoff and the pull request.
15. DO NOT RE-RUN THE FULL SUITE. `python3 -m pytest -n auto -q` is NOT a gate
    of this round; the integration gate PASSED at R65 and closure precondition
    2 is settled by DECISION F031 D27, which C3 lands.
16. YOU MERGE NOTHING AND YOU DELETE NO BRANCH. No `--force`, no
    `--force-with-lease`, no history rewrite, no `gh pr merge`.

Done when — run every gate yourself and record its REAL exit code, ONE LINE per
gate in the handback with transcripts kept out of it. G1 through G10 all run
BEFORE C4, so the handback can quote every one of them. G11 and G12 are the
exceptions and their own text states how they are treated. The round base is
`f7cc2dd2` throughout. Read every non-current revision with
`git show <rev>:<path>` into memory; never write a past blob over a tracked file.
 G1. BRANCH, CLEANLINESS, STOP. Branch is `feature/f031-decision-inbox`.
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1, C2, C3
     and C4. `.agent/STOP` read from disk before C0a and before C4, both ABSENT.
 G2. TRANSPORT. Report the sha256, byte count and line count of this block as
     read from `.remedy-wt/f031-r72.md`, as saved at C0a, as mirrored at C0b and
     as read off disk at C3 — all four must be EQUAL — and say whether C0a and
     C0b are the same git blob. Report whether any line of the block as saved is
     a run of a single repeated character at length 4 or more, which must come
     back as none. THEN STATE IN ONE SENTENCE WHAT THIS PROOF COVERS: the scratch
     file, the saved copy, its mirror and the working copy, and NOT the bytes of
     any prompt.
 G3. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES. Report how many slices your extractor printed, each
     slice's own line count, the CONTENT total, the TOTAL line count, and PROSE
     as TOTAL minus CONTENT. MARKERS ARE PROSE. PROSE at most 400, TOTAL at most
     490.
 G4. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R72 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G5. THE LEDGER APPEND, PROVED TWICE, THE SECOND READER COVERING THE WHOLE
     APPENDED REGION. `.agent/live_review.md` at C2 equals its pre-commit blob
     plus ONE newline plus LEDGER72. The reviewer measured the base blob at
     `f7cc2dd2` itself: 1012298 bytes over 402 blank-line units. If it reads
     differently before C2, something moved this round did not order — stop and
     hand back. Report both byte counts and the sum. Then the SECOND, INDEPENDENT
     reader: split the whole file on blank lines, let N be the number of
     paragraphs YOUR SCRIPT COUNTS in that slice — never a number this block
     asserts — and compare the LAST N units against the slice's N paragraphs IN
     ORDER. Report N and the unit count before and after. THE NEGATIVE CONTROL
     GOES ON THE FIRST APPENDED PARAGRAPH, AT A BYTE OFFSET, NOT A CHARACTER
     OFFSET — the file carries multi-byte em dashes and a character offset lands
     outside the appended region where the control proves nothing. Flip ONE byte
     IN MEMORY and report that BOTH readers REJECT it. Never mutate the tracked
     file.
 G6. THE LEDGER SETS. Report at two points — before C2 and after C2 — the
     line-anchored counts of `^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-`,
     `^Gate: R\d+ — ` and `^Gate: F\d+ R\d+ — `, plus the finding ids, the
     RESOLVED ids and the gate keys ADDED and REMOVED as SETS, whether all ids
     are DISTINCT, and the maximum id at each point. Every movement constraint 7
     names is checked here, INCLUDING the ones that must NOT move. Report the
     open set at both points.
 G7. THE DECISION APPEND. `.agent/decisions.md` at C3 equals its pre-commit blob
     plus ONE newline plus DECISION27, byte for byte; report both byte counts and
     the sum, and report that the file at C3 STARTS WITH its pre-commit blob as a
     byte prefix. Report the line-anchored count of `^## DECISION F031 D\d+ ` at
     both points and the ADDED key as a SET, which must be exactly
     `## DECISION F031 D27`.
 G8. THE STATE READERS AND THE CANARY, run BEFORE C4. This round rewrites
     `.agent/` state, so `.agent/context.md`'s standing constraint binds: run, as
     ONE pytest process and never two at once, `python3 -m pytest
     tests/ui_server/ tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py
     tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q`
     from the repository root. Report the REAL exit code, the summary line
     verbatim, and the COUNT of lines matching `^FAILED`. PROVE YOUR `^FAILED`
     EXTRACTOR IS NOT BLIND by running it over a string you know contains such a
     line and reporting that it matched. The reviewer measured 620 passed at a
     REAL exit 0 with zero `^FAILED` lines at the round base. IF YOUR RUN IS RED,
     report the failing node ids VERBATIM and hand back.
 G9. THE CLOSURE EDITS AND THE DOCS PINS. Apply the four pairs, then BEFORE
     committing C4 run, as ONE pytest process, `python3 -m pytest tests/docs/
     tests/orchestration/test_roadmap_index.py -q` from the repository root and
     report the REAL exit code and the summary line verbatim. The reviewer
     measured this GREEN on the fully synced edit and RED on the STATUS flip
     WITHOUT the README sync, failing exactly
     `test_the_readme_accepted_count_equals_the_status_count` and
     `test_the_readme_tier_table_done_column_matches_the_ledger` — so the gate is
     PROVED SIGHTED and a green here is a reading rather than a silence. Then
     report, for `docs/roadmap/STATUS.md` and `README.md` at C4: for EACH of the
     three REWRITE pairs, its FROM occurs 0 times and its TO occurs EXACTLY ONCE
     in its file. For the APPEND pair RFROM3/RTO3 the §4.9 obligation is the
     PROSE one and NEVER a FROM-zero count: report that RFROM3 occurs EXACTLY
     ONCE in `README.md`, and that every line of RTO3 OTHER THAN RFROM3 occurs
     exactly once AMONG THE LINES C4's DIFF ADDS to `README.md`.
G10. STRUCTURE, ARTIFACTS AND MARKERS, reported for the commits BEFORE C4.
     Compare the path set of `git diff --name-only f7cc2dd2..C3` BOTH WAYS
     against this round's expected set — the Change line's list MINUS
     `docs/roadmap/STATUS.md`, `README.md`, `.agent/candidates.md` and
     `.agent/handoff.md`, which C4 writes — and report both residues EMPTY.
     Report `git diff --stat f7cc2dd2..C3` restricted to `apps/`, `packages/`,
     `tests/` and `docs/` — the last WHOLE — and confirm each EMPTY. Report each
     commit's insertions from `git diff --numstat` for C0a through C3, confirm
     each single-parent and under 500. Line-anchored `^<<<SLICE ` and `^<<<END `
     are 0 and 0 in `.agent/plan.md` at C1, `.agent/live_review.md` at C2 and
     `.agent/decisions.md` at C3, against a CONTROL over the C0a blob which is
     not 0. Report `git ls-files .remedy-wt` 0 lines, `git status --porcelain` 0
     lines, `git worktree list` 1 line, and `git branch --list "tmp/*"` 0 lines.
G11. THE OPEN PR GATE, READ BEFORE C4, AND THE PUSH. Run `gh pr list --state
     open --json number,headRefName,baseRefName,isDraft` and report it verbatim.
     The reviewer read `[]` at the round base. MERGE NOTHING. After C4, run
     `git push origin feature/f031-decision-inbox`. ITS OUTCOME IS NOT A VALUE OF
     ANY FILE THIS ROUND WRITES: C4 is authored before the push exists, so
     `.agent/handoff.md` states the push only as an INTENT under
     `## External actions`, with NO exit code and NO remote tip. Report the real
     exit code and the resulting remote tip in your completion report instead.
G12. THE PULL REQUEST, CREATED AND NOT MERGED. After the push, run `gh pr
     create` targeting `main` from `feature/f031-decision-inbox`. Title:
     `F031 — Decision inbox`. The body carries what changed and why, the key
     decisions including DECISION F031 D27, how to review, a changed-files table
     for the branch, the latest verdict PASS_WITH_RISKS, the open-findings count
     after this round, and the five closure values. DO NOT MERGE IT. Like G11 its
     outcome postdates C4, so report the real exit code and the PR number in your
     completion report and NOT in any file this round writes.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C4, in the shape constraint 10 orders: feature and round, branch,
             the round base SHA, the per-commit changed-files table with the
             `+/-` column taken from `git diff --numstat` ITSELF and agreeing
             cell for cell with G10, an item-status row for EVERY Bundle item,
             ONE LINE PER GATE for G1 through G10 with its real exit code, the
             open-findings count after this round, and the next expected action.
             C4 cannot table its own numstat — write `self` in that cell, as
             `R-0149` requires, and put C4's own numbers nowhere.
             ANY COMMIT YOU MAKE BEYOND THE ORDERED SEQUENCE RECEIVES ITS OWN
             `## Commits` ROW AND ITS OWN ITEM-STATUS ROW, and the Deviations
             section says so in those same words.
             CARRY THE FIVE CLOSURE VALUES under a `## Closure values` heading —
             the evidence job id `f031-closure`, the package filename
             `remedy-review-20260827-122441-READY_FOR_REVIEW.zip`, its SHA-256
             `4b862bf093f4082821662357d730042c28ad6c16078dfa5bced812aca0db4bfa`,
             the status `READY_FOR_REVIEW`, and the manifest head
             `f0dad9a8076e8cfc4208dbe5a7097619a31d4cd5`, which is the accepted
             HEAD the STATUS line names. STATE PLAINLY THAT F031 IS CLOSED, that
             the pull request is NOT merged this session, and that it merges at
             the next feature's start via the Open PR Gate. Make the next-action
             section that merge, and name no round number for it. Include the
             SESSION line constraint 14 orders.

<<<SLICE PLANF031R72
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1-D27.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
CLOSURE 3 OF 3. The RECORD ROUND passed every gate its block ordered and this
round writes that verdict. It registers ONE new finding, `R-0709`, for a defect
the open set does not hold: a block ordered its handback to put a ruling request
to the operator, which `docs/agents/planner_reviewer_prompt.md` §2 forbids, and
the session ended with nothing closed. It records DECISION F031 D27, which rules
closure precondition 2 met on the evidence and carries `R-0708` as a documented
open Medium risk. Then it flips the STATUS line to `[x]` with the README sync in
the SAME commit and opens the pull request, which is NOT merged this session.

## Next Steps
1. MERGE THE CLOSURE PULL REQUEST at the next feature's start, through the
   AGENTS.md Open PR Gate. It is not merged in the session that creates it; the
   gap is the operator's manual-review window.

## Risks
- `R-0708` IS CARRIED OPEN AND IS NOT AN F031 DEFECT. Closure precondition 2
  measured four GREEN and one RED in five runs at the reviewed head. The red is
  a fixed five-second server-start budget in `tests/ui_server/test_live_state.py`
  losing a CPU race under `-n auto`; the same test passes SOLO at exit 0 in
  0.32s. DECISION F031 D27 rules the precondition met and routes the repair to a
  follow-up, because `tests/ui_server/` is outside F031's change set.
- R-0495 and R-0574 are inherited standing Highs from the already-closed F085
  and F086, documented risks rather than F031 defects.
- THE CLOSURE PACKAGE IS NOT ON DISK. It was built and verified at CLOSURE 2 and
  its five values are carried unchanged; `.gitignore` excludes the archive and
  the durable pointer is the STATUS line. This is registered as a closure
  candidate rather than a finding.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 253 after this
  round, which mints `R-0709` and resolves nothing.
<<<END PLANF031R72

<<<SLICE LEDGER72
Gate: F031 R71 — the F031 RECORD ROUND entry. THE ROUND PASSED on every gate its block ordered, G1 through G11, and the reviewer re-ran every one of them itself. TRANSPORT HELD AT FIVE POINTS, NOT FOUR: the scratch original `.remedy-wt/f031-r71.md` SURVIVED to this gate, so the reviewer measured it beside the C0a blob, the C0b blob, the C2 blob and the working copy, and all five are sha256 `fdb9668d55ada56fdd54d24135b49bcd0cab18cc06f673af2bd91d0d4513a66d` over 23321 bytes and 268 lines, with C0a and C0b the SAME blob `2f3a2a42` and no line a run of a single repeated character at length 4 or more. THAT PROOF COVERS THE SCRATCH FILE, THE SAVED COPY, ITS MIRROR AND THE WORKING COPY, AND NOT THE BYTES OF ANY PROMPT. EXTRACTION printed 2 slices at 48 and 1 content lines, CONTENT 49, TOTAL 268, PROSE 219, both caps met. THE PLAN at C1 is byte-equal to PLANF031R71 with the minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` 48. THE LEDGER APPEND at C2 proves twice: 1007162 + 1 + 5135 = 1012298 against a committed 1012298 and a byte-equal reconstruction, N 1 script-counted, units 401 to 402, the last unit EQUAL IN ORDER, and a one-byte flip at byte offset 1007203 inside the first appended paragraph REJECTED by both readers. THE SETS MOVED EXACTLY ONCE as ordered: `^Gate: F\d+ R\d+ — ` 51 to 52 adding the single key `F031 R70`, while `^- R-\d+ — ` stayed 269, `^Done: R-\d+ — ` stayed 17, `^Landed: R-` stayed 0 and `^Gate: R\d+ — ` stayed 19; ids ADDED none and REMOVED none, all DISTINCT at both points, the maximum `R-0708` at both, and the open set 252 before and 252 after — the round minted nothing. THE TWO NAMED PARAGRAPHS ARE UNTOUCHED: `R-0430` is sha256 `f9a4dfe38b2936ab` and `R-0708` is sha256 `8fd175c6b5878251` at the round base and at C2, each occurring exactly once at each, and the file at C2 starts with the base file as a byte prefix. THE STATE READERS AND THE CANARY ran as one pytest process at a REAL exit 0, `620 passed in 66.13s (0:01:06)`, zero `^FAILED` lines, with the extractor proved sighted on a probe string. NOTHING ELSE MOVED: both path residues EMPTY, `apps/`, `packages/`, `tests/` and `docs/` each EMPTY, insertions 268, 101, 21 and 2, each single-parent and under 500, markers 0 and 0 against a CONTROL of 2 and 2, `.remedy-wt` 0 tracked, worktree 1 line, no `tmp/*` branch, the Open PR Gate read and NOT acted on at `[]`, and the push landing at a remote tip equal to the local tip `f7cc2dd2`. PER `R-0494`, THE HANDBACK COMMIT'S OWN NUMBERS, WHICH NO FILE OF THAT ROUND COULD CARRY, ARE RECORDED HERE: `f7cc2dd2` is single-parent at 43 insertions and 73 deletions over `.agent/handoff.md` alone, and that file measures 63 lines. THE `R-0430` FIX LANDED AND IS CONFIRMED: the R71 handback's DECISION D15 declaring line states its own measured count as the numeral 63 beside its cause, which is exactly what the standing rule asks and exactly what the R70 handback failed to do — so the recurrence recorded at the last gate is answered, and `R-0430` stays OPEN only because its rule is standing rather than because this round broke it. THE DECLARED CONVENTION NOTE IS CORRECT AND IS NOT A RESIDUAL: the reviewer re-ran difflib opcodes over `tests/ui_server/test_live_state.py` at `6b68718e` and reads one replace of a single line at line 14, the import gaining `patch`, and one insert of 43 lines at line 467 of a 557-line pre-image taking it to 600 with 91 lines following — identical to LEDGER71 — while `wc -l` over the same blobs reads 556 to 599 with 90 following, the gap being the trailing-newline convention alone. THE `R-0708` ROUTING SURVIVES RE-VERIFICATION: `6b68718e` is the only commit on this branch touching that file, the inserted class holds three tests that each reach `_build_live_state_json` through a `_live_count` helper wrapping it in `patch`, the region references no `_start_server`, no `start_ui_server` and no `HTTPConnection`, and `TestUIServerIntegration`, its `_start_server` helper and `test_context_budget_endpoint` stand at lines 121, 133 and 317 both before and after. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no unverified completion claim and no silent scope change.

- R-0709 — Medium, A BLOCK ORDERED ITS HANDBACK TO PUT A RULING REQUEST TO THE OPERATOR, AND THE SESSION ENDED WITH NOTHING CLOSED. Raised by the reviewer at the R71 gate, measured at `f7cc2dd2`. The R71 block's Handback paragraph ordered the worker to "put the question to them in one sentence: closure precondition 2 measured four GREEN and one RED in five runs at the reviewed head ... so may the STATUS line carry `[x]`", and `.agent/handoff.md` duly ends "CLOSURE IS DEFERRED TO THE OPERATOR, and the question is this". `docs/agents/planner_reviewer_prompt.md` §2 forbids exactly that in the words "The operator is NEVER asked a question, offered a menu, or handed a ruling request", and provides that even a hard STOP ships "the reviewer's already-made recommendation"; §4 item 7 states the mechanism the reviewer must use instead — a loud, persisted, reversible DECISION recorded in the brief and the ledger, proceeded under at once, with "The operator's veto is any later relay; nothing waits for an answer". THE COST IS MEASURED AND NOT HYPOTHETICAL: the operator's reply to that handoff was to start another session with the same skill and no ruling, so the question returned unanswered to a reviewer who was always the one empowered to settle it, and a full session closed nothing. THE ROUTING IS THE DEFECT, NOT THE CAUTION — guardrail G8 of `docs/agents/self_drive_protocol.md` ends a session on "ambiguity the rules do not resolve", and these rules DO resolve this: closure precondition 1 of `docs/roadmap/STATUS_closure_protocol.md` admits any finding "listed as a documented Medium/Low risk", which `R-0708` already was, so G8 was invoked over a question its own §4 item 7 answers. Medium and not Low because the failure mode is a session that terminates having produced nothing, and it recurs by construction until the reviewer rules. Medium and not High because nothing false was written and nothing was lost. THE FIX, binding on the next block whose round is blocked on a judgement the operator has not made: the reviewer rules under §4 item 7, records the ruling as a DECISION in `.agent/decisions.md` with its chosen option, its rejected alternatives and its reversal step, and proceeds — and a block may order a handback to STATE a ruling but never to ASK for one. DECISION F031 D27, which C3 of this round lands, is that fix performed. OPEN.
<<<END LEDGER72

<<<SLICE DECISION27
## DECISION F031 D27 (2026-08-27) — closure precondition 2 is met on the evidence, and `R-0708` is carried as a documented open Medium risk

THE QUESTION. Closure precondition 2 of `docs/roadmap/STATUS_closure_protocol.md`
asks for a green relevant suite. At the reviewed head five runs of
`python3 -m pytest -n auto -q` produced FOUR GREEN at a real exit 0 with
`17817 passed, 20 skipped` and ONE RED at exit 1 with `1 failed, 17816 passed,
20 skipped`. Whether an intermittently green precondition may carry `[x]` is the
judgement this entry settles, under
`docs/agents/planner_reviewer_prompt.md` §4 item 7.

CHOSEN, THE PRECONDITION IS MET AND F031 CLOSES AS PASS_WITH_RISKS. Three
readings carry it. The dedicated integration-gate round the precondition names
PASSED at R65 with a real exit 0 at 17817 passed and 20 skipped, and BOTH
differential sets — branch-only and base-only — EMPTY. The intermittency is in
the instrument and not the feature: `_start_server` polls 50 times at 0.1s and
then fails, so the budget is a flat five seconds of wall clock that competes with
every xdist worker, and the same test passes SOLO at exit 0 in 0.32s. And
precondition 1 already admits a finding "listed as a documented Medium/Low risk",
which `R-0708` is — registered, mechanism read from source rather than guessed,
and routed to a follow-up.

REJECTED, A REPAIR ROUND ON THE HARNESS. `R-0708`'s own text routes the repair
away from this feature because `tests/ui_server/` is outside F031's change set,
and overturning that routing to unblock a closure would let a closure deadline
decide a scope question. REJECTED, AN `[!]` BLOCKED LINE. Nothing about F031 is
blocked: 17817 tests pass, the package was built and verified, and every other
precondition holds — an `[!]` would be dishonest in the opposite direction to a
false `[x]`.

HOW TO REVERSE. Delete this entry and set the F031 STATUS line back to `[~]`.
The closure commit is a single commit touching `docs/roadmap/STATUS.md`,
`README.md` and `.agent/` state, so reverting it restores the prior state
exactly; the pull request it opens is not merged in the session that creates it,
which is the operator's window to do so.
<<<END DECISION27

<<<SLICE SFROM
- [~] F031 — Decision inbox
<<<END SFROM

<<<SLICE STO
- [x] F031 — Decision inbox (T001–T003 complete; accepted 2026-08-27 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f031-closure · package remedy-review-20260827-122441-READY_FOR_REVIEW.zip · SHA-256 4b862bf093f4082821662357d730042c28ad6c16078dfa5bced812aca0db4bfa · accepted HEAD f0dad9a8076e8cfc4208dbe5a7097619a31d4cd5)
<<<END STO

<<<SLICE RFROM1
57 of 255 registered items accepted. Next: F031 (Decision inbox).
<<<END RFROM1

<<<SLICE RTO1
58 of 255 registered items accepted. Next: F032 (Approval with the evidence triple).
<<<END RTO1

<<<SLICE RFROM2
| 5 | Operator Cockpit | 5 | 29 |
<<<END RFROM2

<<<SLICE RTO2
| 5 | Operator Cockpit | 6 | 29 |
<<<END RTO2

<<<SLICE RFROM3
terminal with any delta labelled).
<<<END RFROM3

<<<SLICE RTO3
terminal with any delta labelled).
F031 decision inbox (every open question as a card carrying its type, age and
blocked-subtree size, derived from the decision queue with no new storage,
ordered by a documented rule over age and blocked size, filtered and badged
live, and answerable from the card through the one existing write channel).
<<<END RTO3

<<<SLICE CANDIDATES
# Closure Candidates — carrier of record

> Written per docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate
> findings", disk-vehicle rule, operator ruling 2026-08-01). Read at Window-1
> session bootstrap (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present at
> feature-claim time is a block condition.

- The closure package a STATUS line names is absent from disk at closure time.
  `remedy-review-20260827-122441-READY_FOR_REVIEW.zip` was built and verified at
  F031 CLOSURE 2 — 20155047 bytes over 3596 members, SHA-256 recomputed
  independently by the reviewer — and no copy of it exists anywhere under the
  repository at the closure round, while the F022 package from four days earlier
  still sits in the repository root. `.gitignore` excludes the archive by design
  and the durable pointer is the STATUS line, so this is not a failed build and
  not a protocol breach; what is unexplained is the ASYMMETRY, and the operator's
  review window for F031 cannot be reopened from this machine without a rebuild.
  Decide whether closure should verify the package still exists, or state
  plainly that it is handed over and expected to vanish. · source F031 ·
  2026-08-27
<<<END CANDIDATES
