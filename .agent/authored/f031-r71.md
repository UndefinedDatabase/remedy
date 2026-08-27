STEP RECORD ROUND / F031 — DECISION INBOX
Goal:        Record the CORRECTION ROUND's verdict, which is PASS on every gate
             its block ordered, and record — WITHOUT MINTING AN ID — a recurrence
             of the OPEN finding `R-0430`, whose standing rule that round's own
             handback broke. This round writes NO `docs/roadmap/STATUS.md` line,
             syncs NO README and creates NO pull request. No production code, no
             tests, no docs. CLOSURE 3 OF 3 IS DELIBERATELY NOT ORDERED: it turns
             on a question only the operator can answer, and guardrail G8 of
             `docs/agents/self_drive_protocol.md` ends a session on exactly that
             kind of question rather than guessing at it.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the ledger append · C3 the handoff · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r71.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/handoff.md`. This list bounds what you WRITE INTO THE
             REPOSITORY. It does NOT bound what you DO: G11 orders a push.
             NOTHING under `apps/`, `packages/`, `tests/` or `docs/`.

Constraints:
 1. THIS BLOCK REACHES YOU AS A FILE, NOT AS PROSE IN A PROMPT. Read
    `.remedy-wt/f031-r71.md` from disk and copy it BYTE FOR BYTE to
    `.agent/authored/f031-r71.md` — with `shutil.copyfile` or a read-then-write
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
 3. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3. Every sentence in LEDGER71
    that describes THIS round's own landed change depends on that order, and
    this constraint is what fixes it.
 4. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES THE CORRECTION
    ROUND. That is ordered: the plan becomes current at C1.
 5. NOTHING IS EDITED OUT OF THE LEDGER. `.agent/live_review.md` is APPEND-ONLY.
    The existing paragraphs of `R-0430` and of `R-0708` are NOT rewritten, NOT
    deleted and NOT touched. This round's correction is a NEW paragraph appended
    after them. An append-only record is corrected by appending, never by
    revising history in place.
 6. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Gate:` paragraph of
    your own and never mint a finding id. LEDGER71 carries ONE paragraph. NO
    FINDING IS REGISTERED AND NONE IS RESOLVED THIS ROUND — the `R-0430`
    recurrence is recorded inside this round's own gate entry precisely so that
    no second id is spent on a defect the open set already holds. If you find a
    further defect, report it in the handback under Deviations and let the
    reviewer rule on it.
 7. THE LEDGER SETS MOVE ONCE. Across C2 `^Gate: F\d+ R\d+ — ` moves 51 to 52
    with the ADDED key exactly `F031 R70`. `^- R-\d+ — ` stays 269,
    `^Done: R-\d+ — ` stays 17, `^Landed: R-` stays 0 and `^Gate: R\d+ — `
    stays 19. The open set is 252 before C2 and 252 after C2, and the maximum
    id is `R-0708` at BOTH points — this round mints nothing.
 8. RE-READ `.agent/STOP` FROM DISK before C0a and again before C3. If it exists
    at either reading, finish the commit in hand, write the handback and STOP.
    Never create it, never delete it.
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
    completion report, a transcript, or any other channel that does not survive
    the session: under self-drive the handoff is the only return channel. This
    is the standing rule the OPEN finding `R-0430` already carries, and the
    round you are recording broke it.
11. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `${...}` and every other expansion, `cp`, brace literals
    containing a quote character, `cd x && y`, file redirects, and every form of
    environment assignment. Route anything that counts, hashes or compares
    through a quoted python heredoc, read real exit codes from
    `subprocess.run(...).returncode`, and pass `cwd=` rather than `cd`. Run
    pytest SERIALLY — never two pytest processes alive at once. `--timeout` IS
    NOT AVAILABLE to pytest here: passing it exits 4 and reports no failure.
12. EVERY NUMERAL THIS BLOCK STATES ABOUT THE ROUND BASE `a6be2fdf` was measured
    by the reviewer at that commit. It is a REFERENCE to report against, NOT a
    target to reproduce. Where your measurement differs, report BOTH and
    reconcile NOTHING.
13. THIS IS THE LAST ROUND OF ITS SESSION. This session delegated exactly ONE
    round — this RECORD ROUND, which terminates it — and a SESSION line naming
    that roster, including this terminating round itself, belongs in the
    handoff. The next expected action is CLOSURE 3 OF 3 and you name it by that
    label and by no round number, because §3 item 35 forbids numbering a round
    that has not begun.
14. DO NOT RE-RUN THE FULL SUITE. `python3 -m pytest -n auto -q` is NOT a gate
    of this round; it is registered as intermittent in `R-0708` and another
    sample would add nothing this round can act on.

Done when — run every gate yourself and record its REAL exit code, ONE LINE per
gate in the handback with transcripts kept out of it. G1 through G10 all run
BEFORE C3, so the handback can quote every one of them. G11 is the single
exception and its own text states how it is treated. The round base is
`a6be2fdf` throughout. Read every non-current revision with
`git show <rev>:<path>` into memory; never write a past blob over a tracked file.
 G1. BRANCH, CLEANLINESS, STOP. Branch is `feature/f031-decision-inbox`.
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1 and C2.
     `.agent/STOP` read from disk before C0a and before C3, both ABSENT.
 G2. TRANSPORT. Report the sha256, byte count and line count of this block as
     read from `.remedy-wt/f031-r71.md`, as saved at C0a, as mirrored at C0b and
     as read off disk at C2 — all four must be EQUAL — and say whether C0a and
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
 G4. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R71 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G5. THE LEDGER APPEND, PROVED TWICE, THE SECOND READER COVERING THE WHOLE
     APPENDED REGION. `.agent/live_review.md` at C2 equals its pre-commit blob
     plus ONE newline plus LEDGER71. The reviewer measured the base blob at
     `a6be2fdf` itself: 1007162 bytes over 401 blank-line units. If it reads
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
     are DISTINCT, and the maximum id, which is `R-0708` at BOTH points. Every
     movement constraint 7 names is checked here, INCLUDING the ones that must
     NOT move. Report the open set at both points.
 G7. THE TWO NAMED PARAGRAPHS ARE UNTOUCHED. Prove constraint 5 held: extract the
     `- R-0430 — ` paragraph and the `- R-0708 — ` paragraph from
     `.agent/live_review.md` at the round base and again at C2, report each
     paragraph's sha256 at BOTH points, and confirm they are EQUAL and that each
     occurs EXACTLY ONCE at each point. Report also that the file at C2 STARTS
     WITH the file at the round base as a byte prefix, which is what append-only
     means and what forbids an in-place revision.
 G8. THE STATE READERS AND THE CANARY. This round rewrites `.agent/` state, so
     `.agent/context.md`'s standing constraint binds: run, as ONE pytest process
     and never two at once, `python3 -m pytest tests/ui_server/
     tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
     tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q`
     from the repository root. Report the REAL exit code, the summary line
     verbatim, and the COUNT of lines matching `^FAILED`. PROVE YOUR `^FAILED`
     EXTRACTOR IS NOT BLIND by running it over a string you know contains such a
     line and reporting that it matched — a zero from an extractor that cannot
     match is not a reading. The reviewer measured 620 passed at a REAL exit 0
     with zero `^FAILED` lines at the round base. IF YOUR RUN IS RED, report the
     failing node ids VERBATIM and hand back; do not re-run until green.
 G9. STRUCTURE, ARTIFACTS AND MARKERS, reported for the commits BEFORE C3.
     Compare the path set of `git diff --name-only a6be2fdf..C2` BOTH WAYS
     against this round's expected set — the Change line's list MINUS
     `.agent/handoff.md`, which C3 writes — and report both residues EMPTY.
     Report `git diff --stat a6be2fdf..C2` restricted to `apps/`, `packages/`,
     `tests/` and `docs/` — the last WHOLE — and confirm each EMPTY. Report each
     commit's insertions from `git diff --numstat` for C0a through C2, confirm
     each single-parent and under 500. Line-anchored `^<<<SLICE ` and `^<<<END `
     are 0 and 0 in `.agent/plan.md` at C1 and `.agent/live_review.md` at C2,
     against a CONTROL over the C0a blob which is not 0. Report `git ls-files
     .remedy-wt` 0 lines, `git status --porcelain` 0 lines, `git worktree list`
     1 line, and `git branch --list "tmp/*"` 0 lines.
G10. THE OPEN PR GATE, READ AND NOT ACTED ON, AND STALENESS.
     `gh pr list --state open --json number,headRefName,baseRefName,isDraft` —
     report it verbatim. CREATE NO PR AND MERGE NOTHING. Then: every sentence C1
     and C2 land that states a fact about a file is re-measured at C2; any that
     has gone stale is REPORTED as a residual and never repaired by editing a
     slice. Report explicitly that you checked and name any residual.
G11. PUSH. After C3, run `git push origin feature/f031-decision-inbox`. No
     `--force`, no `--force-with-lease`, no history rewrite, no branch deletion.
     ITS OUTCOME IS NOT A VALUE OF ANY FILE THIS ROUND WRITES: C3 is authored
     before the push exists, so `.agent/handoff.md` states the push only as an
     INTENT under `## External actions`, with NO exit code and NO remote tip.
     Report the real exit code and the resulting remote tip in your completion
     report to the reviewer instead.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C3, in the shape constraint 10 orders: feature and round, branch,
             the round base SHA, the per-commit changed-files table with the
             `+/-` column taken from `git diff --numstat` ITSELF and agreeing
             cell for cell with G9, an item-status row for EVERY Bundle item, ONE
             LINE PER GATE for G1 through G10 with its real exit code, the
             open-findings count after this round, and the next expected action.
             ANY COMMIT YOU MAKE BEYOND THE ORDERED SEQUENCE RECEIVES ITS OWN
             `## Commits` ROW AND ITS OWN ITEM-STATUS ROW, and the Deviations
             section says so in those same words.
             CARRY FORWARD THE FIVE CLOSURE VALUES UNCHANGED under a
             `## Closure values` heading — the evidence job id `f031-closure`,
             the package filename
             `remedy-review-20260827-122441-READY_FOR_REVIEW.zip`, its SHA-256
             `4b862bf093f4082821662357d730042c28ad6c16078dfa5bced812aca0db4bfa`,
             the status `READY_FOR_REVIEW`, and the manifest head
             `f0dad9a8076e8cfc4208dbe5a7097619a31d4cd5` — because CLOSURE 3
             cannot be authored without them and the package is NOT rebuilt.
             STATE PLAINLY THAT CLOSURE IS DEFERRED TO THE OPERATOR and put the
             question to them in one sentence: closure precondition 2 measured
             four GREEN and one RED in five runs at the reviewed head, the red
             being `R-0708` and shown NOT to be an F031 defect, so may the STATUS
             line carry `[x]`. Make the next-action section CLOSURE 3 OF 3 and
             name no round number for it. Include the SESSION line constraint 13
             orders.

<<<SLICE PLANF031R71
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1-D26.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
RECORD ROUND. The CORRECTION ROUND passed every gate its block ordered and this
round writes that verdict. It also records, WITHOUT MINTING AN ID, a recurrence
of the OPEN finding `R-0430`: that round's handback declared a DECISION D15
overage without stating its own measured line count, which is exactly the
standing rule `R-0430` already carries. This round writes NO STATUS line, syncs
NO README and creates NO pull request.

## Next Steps
1. CLOSURE 3 of 3 — the STATUS line from `[~]` to `[x]` with the README
   capability sync in the SAME commit, then the pull request, which is NOT
   merged in the session that creates it. The five closure values it needs
   already exist and are carried in the handoff; the package is NOT rebuilt.
   IT IS BLOCKED ON THE OPERATOR QUESTION IN THE FIRST RISK BELOW, and no
   session starts it before that question is answered.

## Risks
- CLOSURE 3 IS BLOCKED ON AN OPERATOR QUESTION. Closure precondition 2 asks for
  a green suite; the reviewer measured four GREEN and one RED in five runs at
  the reviewed head, the red being `R-0708`. Whether an intermittently green
  precondition may carry an `[x]` is not answered by
  `docs/roadmap/STATUS_closure_protocol.md`, whose Failure-honesty section
  offers a repair round, an `[!]` line or an explicit operator decision — a
  choice guardrail G8 forbids this session to make for itself.
- `R-0708` IS NOT AN F031 DEFECT. Commit `6b68718e` is the only one on this
  branch touching `tests/ui_server/test_live_state.py`; it changes one import
  line and inserts a class that starts no server, and it leaves
  `TestUIServerIntegration`, its `_start_server` helper and
  `test_context_budget_endpoint` untouched.
- THE CLOSURE PACKAGE ALREADY EXISTS and does not need rebuilding. It was built
  from a clean tree at the reviewed head and its manifest names that head.
- R-0495 and R-0574 are inherited standing Highs from the already-closed F085
  and F086, documented risks rather than F031 defects.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 252 and this round
  moves it by nothing.
<<<END PLANF031R71

<<<SLICE LEDGER71
Gate: F031 R70 — the F031 CORRECTION ROUND entry. THE ROUND PASSED on every gate its block ordered, G1 through G11, and the reviewer re-ran every one of them itself. TRANSPORT held at four points — the scratch file, C0a, C0b and the working copy all sha256 `b9c6ad125eaf69d2b2e3886120ebf1d379e990a85c47ff783648d58833c6561b` over 21194 bytes and 253 lines, C0a and C0b the SAME blob `ee2c43bb` — and no line of the block is a run of a single repeated character at length 4 or more. THAT PROOF COVERS THE SCRATCH FILE, THE SAVED COPY, ITS MIRROR AND THE WORKING COPY, AND NOT THE BYTES OF ANY PROMPT: under self-drive there is no paste relay, so no gate this workflow can run reaches the emitted bytes, and the verdict claims only the chain it walked. EXTRACTION printed 2 slices at 46 and 1 content lines, CONTENT 47, TOTAL 253, PROSE 206. THE PLAN at C1 is byte-equal to PLANF031R70 with the negative control FALSE, `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` 46. THE LEDGER APPEND at C2 proves twice: 1003228 + 1 + 3933 = 1007162 against a committed 1007162 and a byte-equal reconstruction, N 1, units 400 to 401, the last unit EQUAL IN ORDER, and a one-byte flip at byte offset 1003279 REJECTED by both readers. THE SETS MOVED EXACTLY ONCE as ordered: `^Gate: F\d+ R\d+ — ` 50 to 51 adding the single key `F031 R69`, while `^- R-\d+ — ` stayed 269, `^Done: R-\d+ — ` stayed 17, `^Landed: R-` stayed 0 and `^Gate: R\d+ — ` stayed 19; ids ADDED none and REMOVED none, all ids DISTINCT at both points, the maximum `R-0708` at both, and the open set 252 before and 252 after — the round minted nothing. `R-0708` IS UNTOUCHED: its paragraph is sha256 `8fd175c6b5878251` at the round base and at C2, occurs exactly once at each, and the file at C2 starts with the base file as a byte prefix. THE STATE READERS AND THE CANARY ran as one pytest process at a REAL exit 0, `620 passed in 66.22s`, zero `^FAILED` lines, with the extractor proved sighted on a probe string. NOTHING ELSE MOVED: both path residues EMPTY, `apps/`, `packages/`, `tests/` and `docs/` each EMPTY, insertions 253, 105, 16 and 2, each single-parent and under 500, markers 0 and 0 against a CONTROL of 2 and 2, `.remedy-wt` 0 tracked, worktree 1 line, no `tmp/*` branch, the Open PR Gate read and NOT acted on at `[]`, and the push landing at a remote tip equal to the local one with zero rewrite operations in the reflog window between the round base and the tip. PER `R-0494`, THE HANDBACK COMMIT'S OWN NUMBERS, WHICH NO FILE OF THAT ROUND COULD CARRY, ARE RECORDED HERE: `a6be2fdf` is single-parent at 73 insertions and 40 deletions over `.agent/handoff.md` alone. NOW THE RECURRENCE, RECORDED WITHOUT AN ID PER §3 CHECKLIST ITEM 30 BECAUSE THE OPEN SET ALREADY HOLDS THE DEFECT. `R-0430` carries the standing rule that a handoff declaring a DECISION D15 overage states its own measured line count AS A NUMERAL in the declaring line and never forwards it to a channel that does not survive the session. The R70 handback declares the overage and names its cause correctly — five per-commit tables, ten gate lines, a six-row item-status table and the mandated closure-values block, with no section dropped — and then writes "This file is over 60 lines", which states the CAP and not the COUNT. Measured at `a6be2fdf`, that file is 93 lines. The number therefore reached no durable artifact and the reviewer re-measured it from disk, which is precisely the failure `R-0430` describes; the id is NOT re-minted and this paragraph is the added evidence. PART OF THE CAUSE IS THE REVIEWER'S OWN BLOCK, whose constraint 10 ordered the cause named and never ordered the numeral, and the R71 block that carries this entry orders both. AND THE CORRECTION THE LAST ROUND EARNED. `LEDGER70` and `PLANF031R70` both call commit `6b68718e`'s change to `tests/ui_server/test_live_state.py` an APPEND, one of them a "PURE APPEND". Re-measured at `a6be2fdf` by difflib opcodes over the whole file, it is an INSERTION of 43 lines at line 467 of a 557-line pre-image, taking it to 600 lines, with 91 lines following the inserted region and a module-level helper `_decision_requested_events` inside it beside the class. The worker DECLARED that residual under G10 rather than repairing the slice, which is why it is recoverable at all. EVERYTHING THE FINDING TURNS ON SURVIVES AND WAS RE-VERIFIED HERE: exactly one pre-existing line changes, the import gaining `patch`; the inserted class `TestOpenDecisionCountComesFromTheDecisionQueue` holds three tests that call `_build_live_state_json` under `patch` and reference no server helper, no `start_ui_server` and no `HTTPConnection`; and `TestUIServerIntegration`, its `_start_server` helper and `test_context_budget_endpoint` stand at the same line numbers before and after, inside no changed region. So `R-0708` stays OPEN, stays Medium, and its routing reason — the FAILING CLASS, ITS HELPER AND THE FAILING TEST are outside F031's change set even though the FILE is not — is unaffected. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no unverified completion claim and no silent scope change.
<<<END LEDGER71
