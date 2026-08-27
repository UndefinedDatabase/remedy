STEP RECORD ROUND / F031 — DECISION INBOX
Goal:        Put on disk the two things that exist only in the reviewer's head:
             the CLOSURE 2 OF 3 verdict, and the finding raised while running
             closure precondition 2. A verdict that is never written is the
             registered defect R-0659, and this session will not repeat it. This
             round writes NO `docs/roadmap/STATUS.md` line, syncs NO README, and
             creates NO pull request — closure is DEFERRED to the operator and
             the handoff says why. No production code, no tests, no docs.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the ledger append · C3 the handoff · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r69.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/handoff.md`. This list bounds what you WRITE INTO THE
             REPOSITORY. It does NOT bound what you DO: G11 orders a push.
             NOTHING under `apps/`, `packages/`, `tests/` or `docs/`;
             `.agent/candidates.md` is NOT in it and stays EMPTY — the defect it
             would have carried is registered as a real finding this round
             instead, so no dangling candidate is left behind.

Constraints:
 1. THIS BLOCK REACHES YOU AS A FILE, NOT AS PROSE IN A PROMPT. Read
    `.remedy-wt/f031-r69.md` from disk and copy it BYTE FOR BYTE to
    `.agent/authored/f031-r69.md` — with `shutil.copyfile` or a read-then-write
    in python, never by retyping it and never with `cp`, which this session's
    guard rejects. This block asserts NO digest of its own, because a digest
    written inside the text it measures cannot be true; G2 has you measure four
    points and prove them EQUAL, and the reviewer holds the scratch value
    independently.
 2. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. A slice's text is its content lines joined with a newline
    plus ONE trailing newline. If a slice contradicts something you measure,
    apply it anyway and DECLARE the contradiction in the handback under
    Deviations — a corrected slice destroys the transport proof.
 3. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3.
 4. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES CLOSURE 2. That is
    ordered: the plan becomes current at C1.
 5. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Gate:` paragraph of
    your own and never mint a finding id. LEDGER69 carries TWO paragraphs, in
    this order: the CLOSURE 2 gate entry, then the finding `R-0708`. NO FINDING
    IS RESOLVED THIS ROUND. If you find a further defect, report it in the
    handback under Deviations and let the reviewer rule on it; do not repair it
    and do not name it with an id.
 6. THE LEDGER SETS MOVE TWICE, AND ONLY TWICE. Across C2
    `^Gate: F\d+ R\d+ — ` moves 49 to 50 with the ADDED key exactly `F031 R68`,
    and `^- R-\d+ — ` moves 268 to 269 with the ADDED id exactly `R-0708`.
    `^Done: R-\d+ — ` stays 17, `^Landed: R-` stays 0 and `^Gate: R\d+ — `
    stays 19. The open set is 251 before C2 and 252 after C2.
 7. RE-READ `.agent/STOP` FROM DISK before C0a and again before C3. If it exists
    at either reading, finish the commit in hand, write the handback and STOP.
    Never create it, never delete it.
 8. NOTHING DESTRUCTIVE IS ORDERED THIS ROUND. Create no worktree. The primary
    checkout reads `git status --porcelain` 0 lines at every commit.
 9. YOUR HANDBACK FITS THE TIER ITS BUNDLE EARNS. Read the `### handoff.md`
    section of AGENTS.md, count the commits this Bundle orders, and derive your
    own cap from that rule — do not take a number from this block. Write NO
    BLANK LINE between a `###` commit heading and its table, none between a
    `##` heading and its first line, and none between one commit block and the
    next. Declare DECISION D15 only if the MANDATED content still does not fit
    in that shape, and name what actually caused it.
10. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `${...}` and every other expansion, `cp`, brace literals
    containing a quote character, `cd x && y`, file redirects, and every form of
    environment assignment. Route anything that counts, hashes or compares
    through a quoted python heredoc, read real exit codes from
    `subprocess.run(...).returncode`, and pass `cwd=` rather than `cd`. Run
    pytest SERIALLY — never two pytest processes alive at once. `--timeout` IS
    NOT AVAILABLE to pytest here: passing it exits 4 and reports no failure.
11. EVERY NUMERAL THIS BLOCK STATES ABOUT THE ROUND BASE `f78bba9c` was measured
    by the reviewer at that commit. It is a REFERENCE to report against, NOT a
    target to reproduce. Where your measurement differs, report BOTH and
    reconcile NOTHING.
12. THIS IS THE LAST ROUND OF ITS SESSION. The rounds this session delegated are
    CLOSURE 2 OF 3 and this RECORD ROUND, and a SESSION line naming both —
    including this terminating round itself — belongs in the handoff. The next
    expected action is CLOSURE 3 OF 3 and you name it by that label and by no
    round number, because §3 item 35 forbids numbering a round that has not
    begun.
13. DO NOT RE-RUN THE FULL SUITE. `python3 -m pytest -n auto -q` is NOT a gate of
    this round. The reviewer already ran it five times at the round base and the
    readings are recorded in LEDGER69; running it again would only add a sixth
    sample to a finding that is already registered, and this round changes
    nothing it could affect.

Done when — run every gate yourself and record its REAL exit code, ONE LINE per
gate in the handback with transcripts kept out of it. G1 through G10 all run
BEFORE C3, so the handback can quote every one of them. G11 is the single
exception and its own text states how it is treated. The round base is
`f78bba9c` throughout. Read every non-current revision with
`git show <rev>:<path>` into memory; never write a past blob over a tracked file.
 G1. BRANCH, CLEANLINESS, STOP. Branch is `feature/f031-decision-inbox`.
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1 and C2.
     `.agent/STOP` read from disk before C0a and before C3, both ABSENT.
 G2. TRANSPORT. Report the sha256, byte count and line count of this block as
     read from `.remedy-wt/f031-r69.md`, as saved at C0a, as mirrored at C0b and
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
 G4. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R69 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G5. THE LEDGER APPEND, PROVED TWICE, THE SECOND READER COVERING THE WHOLE
     APPENDED REGION. `.agent/live_review.md` at C2 equals its pre-commit blob
     plus ONE newline plus LEDGER69. The reviewer measured the base blob at
     `f78bba9c` itself: 995738 bytes over 398 blank-line units. If it reads
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
     are DISTINCT, and the maximum id, which is `R-0707` before C2 and `R-0708`
     after it. Every movement constraint 6 names is checked here, INCLUDING the
     ones that must NOT move. Report the open set at both points.
 G7. THE STATE READERS AND THE CANARY. This round rewrites `.agent/` state, so
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
 G8. STRUCTURE, ARTIFACTS AND MARKERS, reported for the commits BEFORE C3.
     Compare the path set of `git diff --name-only f78bba9c..C2` BOTH WAYS
     against this round's expected set — the Change line's list MINUS
     `.agent/handoff.md`, which C3 writes — and report both residues EMPTY.
     Report `git diff --stat f78bba9c..C2` restricted to `apps/`, `packages/`,
     `tests/` and `docs/` — the last WHOLE — and confirm each EMPTY. Report each
     commit's insertions from `git diff --numstat` for C0a through C2, confirm
     each single-parent and under 500. Line-anchored `^<<<SLICE ` and `^<<<END `
     are 0 and 0 in `.agent/plan.md` at C1 and `.agent/live_review.md` at C2,
     against a CONTROL over the C0a blob which is not 0. Report `git ls-files
     .remedy-wt` 0 lines, `git status --porcelain` 0 lines, `git worktree list`
     1 line, and `git branch --list "tmp/*"` 0 lines.
 G9. THE OPEN PR GATE, READ AND NOT ACTED ON.
     `gh pr list --state open --json number,headRefName,baseRefName,isDraft` —
     report it verbatim. CREATE NO PR AND MERGE NOTHING. CLOSURE 3 creates the
     PR, after the operator has ruled on the question the handoff puts to them.
G10. STALENESS. Every sentence C1 and C2 land that states a fact about a file is
     re-measured at C2; any that has gone stale is REPORTED as a residual and
     never repaired by editing a slice. Report explicitly that you checked and
     name any residual.
G11. PUSH. After C3, run `git push origin feature/f031-decision-inbox`. No
     `--force`, no `--force-with-lease`, no history rewrite, no branch deletion.
     ITS OUTCOME IS NOT A VALUE OF ANY FILE THIS ROUND WRITES: C3 is authored
     before the push exists, so `.agent/handoff.md` states the push only as an
     INTENT under `## External actions`, with NO exit code and NO remote tip.
     Report the real exit code and the resulting remote tip in your completion
     report to the reviewer instead.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C3, in the shape constraint 9 orders: feature and round, branch, the
             round base SHA, the per-commit changed-files table with the `+/-`
             column taken from `git diff --numstat` ITSELF and agreeing cell for
             cell with G8, an item-status row for EVERY Bundle item, ONE LINE PER
             GATE for G1 through G10 with its real exit code, the open-findings
             count after this round, and the next expected action. CARRY FORWARD
             THE THREE CLOSURE VALUES UNCHANGED under a `## Closure values`
             heading — the evidence job id `f031-closure`, the package filename
             `remedy-review-20260827-122441-READY_FOR_REVIEW.zip`, its SHA-256
             `4b862bf093f4082821662357d730042c28ad6c16078dfa5bced812aca0db4bfa`,
             the status `READY_FOR_REVIEW`, and the manifest head
             `f0dad9a8076e8cfc4208dbe5a7097619a31d4cd5` — because CLOSURE 3
             cannot be authored without them and the package is NOT rebuilt.
             STATE PLAINLY THAT CLOSURE IS DEFERRED TO THE OPERATOR and put the
             question to them in one sentence: closure precondition 2 measured
             four GREEN and one RED in five runs at the reviewed head, the red
             being R-0708 and not an F031 defect, so may the STATUS line carry
             `[x]`. Make the next-action section CLOSURE 3 OF 3 and name no round
             number for it. Include the SESSION line constraint 12 orders.

<<<SLICE PLANF031R69
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
RECORD ROUND. CLOSURE 2 of 3 PASSED and this round writes that verdict, which
would otherwise evaporate exactly as registered finding R-0659 describes. It
also registers R-0708, the intermittent server-start failure the reviewer hit
while running closure precondition 2. It writes NO STATUS line, syncs NO README
and creates NO pull request: closure is deferred to the operator.

## Next Steps
1. CLOSURE 3 of 3 — the STATUS line from `[~]` to `[x]` with the README
   capability sync in the SAME commit, then the pull request, which is NOT
   merged in the session that creates it. The three closure values it needs
   already exist and are carried in the handoff; the package is NOT rebuilt.

## Risks
- CLOSURE PRECONDITION 2 IS INTERMITTENT RATHER THAN GREEN, AND THAT IS WHY
  CLOSURE DID NOT HAPPEN IN THE SESSION THAT PRODUCED THE PACKAGE. The reviewer
  ran `python3 -m pytest -n auto -q` five times at the reviewed head and measured
  four GREEN at 17817 passed with 20 skipped, and one RED at 17816 passed with
  one failed. The red is R-0708. It is not an F031 defect: this feature changed
  nothing under `apps/`, `packages/` or `tests/`.
- WHETHER AN INTERMITTENTLY GREEN PRECONDITION MAY CARRY AN `[x]` IS AN OPERATOR
  QUESTION. The rules do not answer it, and guardrail G8 of the self-drive
  protocol ends a session on exactly that kind of question rather than guessing.
- THE CLOSURE PACKAGE ALREADY EXISTS and does not need rebuilding. It was built
  from a clean tree at the reviewed head and its manifest names that head.
- R-0495 and R-0574 are inherited standing Highs from the already-closed F085
  and F086, documented risks rather than F031 defects, and they rode through six
  prior closures on the same footing.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 251 before this
  round and 252 after it, R-0708 being the one entry that moves.
<<<END PLANF031R69

<<<SLICE LEDGER69
Gate: F031 R68 — the F031 CLOSURE 2 OF 3 entry. THE ROUND PASSED. The reviewer re-ran all fourteen of its gates itself and reproduced every number, and the round's three deliverables — the CLOSURE 1 verdict entry, the feature-scoped evidence bundle and the review package — are all on disk and all verified. TRANSPORT HELD AT FULL STRENGTH AND CLOSED AT BOTH ENDS: the reviewer measured the block's digest BEFORE delegating and the worker measured it independently afterwards, and the scratch original at `.remedy-wt/f031-r68.md`, the committed C0a blob, the committed C0b blob and the working copy are ALL sha256 `d0f3d061358c91581421688b2a01292d082a3fd8a286222d1082dd389cce63da` over 31093 bytes and 445 lines, with C0a and C0b the SAME git blob `fe326b382e32`. EXTRACTION from the committed C0a blob printed 3 slices at 47, 1 and 141 content lines, CONTENT 189, TOTAL 445 and PROSE 256, both caps met. THE PLAN at C1 is byte-equal to PLANF031R68 with the minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` 47. THE LEDGER APPEND at C2 proves twice: 991374 + 1 + 4363 = 995738 against a committed 995738 and a byte-equal reconstruction, and the second reader counted N 1 with units 397 before and 398 after, the last unit EQUAL IN ORDER to the slice's paragraph, with a one-byte flip at byte offset 991415 REJECTED by both readers. THE SETS MOVED EXACTLY ONCE: `^Gate: F\d+ R\d+ — ` 48 to 49 adding exactly `F031 R67`, while `^- R-\d+ — ` stayed 268, `^Done: R-\d+ — ` stayed 17, `^Landed: R-` stayed 0 and `^Gate: R\d+ — ` stayed 19; no finding id and no resolved id was added or removed; all ids DISTINCT at both points with maximum `R-0707`; the open set stayed 251. NOTHING ELSE MOVED: both path residues EMPTY over the four-path set, `apps/`, `packages/`, `tests/` and `docs/` each EMPTY, markers 0 and 0 in both edited files against a CONTROL of 3 and 3 over the C0a blob, insertions 445, 392, 29 and 2, each commit single-parent and under 500, `.remedy-wt` 0 tracked lines, the worktree listing 1 line and no `tmp/*` branch. THE ARTIFACTS ARE REAL AND THE REVIEWER OPENED THEM RATHER THAN TAKING THE WORKER'S WORD: the evidence bundle carries four verification runs at 35, 4, 41 and 7 selected with node ids EQUAL to selected, zero deselected, `test_files` sorted, no `..` in any node id, and every `output_hash` equal to sha256 of its own `stdout_summary` — the six packaging pitfalls that have historically produced a BLOCKED_EVIDENCE package, each checked and each clear. THE PACKAGE `remedy-review-20260827-122441-READY_FOR_REVIEW.zip` is 20155047 bytes over 3596 members, and the reviewer computed its SHA-256 independently as `4b862bf093f4082821662357d730042c28ad6c16078dfa5bced812aca0db4bfa`, equal to the worker's; its `.review_zip_manifest.json` carries `package_status` `READY_FOR_REVIEW` with `committed_review_subject.base_commit` `6325ac2fad76ca94e23f7bd02c80427d28e05f1f`, the branch point, and `.head_commit` `f0dad9a8076e8cfc4208dbe5a7097619a31d4cd5`, which IS C2. INTEGRITY returned all five checks PASS with `.fail_count` 0, R-0648 reported and not relied on. THE PUSH landed: remote tip equals local tip `f78bba9c`, and the reflog carries zero amend, rebase or cherry-pick entries, so no history was rewritten. TWO THINGS THE ROUND GOT RIGHT THAT ARE WORTH NAMING. The worker declared, rather than silently reconciling, that the block on disk differed from the digest the previous session's handoff had recorded — the reviewer had revised it before delegating, re-pointing the round base from `44fd8df9` to `a6384213` because two handoff commits had landed in between and a range gate anchored to the older base would have reported a FALSE non-empty residue on a correct round; the block asserts no digest of itself precisely so that this stays checkable, and the worker applied what was on disk and reconciled nothing, which is what constraint 2 asks. And its G13 residual is CONFIRMED by the reviewer: PLANF031R68's risk sentence claims the package will show `.remedy-wt/` scratch, but the published archive holds ZERO members whose path contains `.remedy-wt`, because `scripts/make_review_zip.sh` now rejects that prefix from the published listing — so the sentence landed stale, the worker correctly applied it byte for byte and declared it instead of editing a slice, and R-0403's own finding text is now stale in the same way and needs re-measuring by whoever next touches it. THE ONE GATE THAT DID NOT REPRODUCE IS G7, AND IT IS REGISTERED AS R-0708 BELOW RATHER THAN FAILING THIS ROUND: the round changed nothing under `apps/`, `packages/` or `tests/`, so the intermittency it exposes is a property of the harness and not of this round's diff. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.

- R-0708 — Medium, CLOSURE PRECONDITION 2 IS INTERMITTENT AND THE ONE PROCEDURE THAT READS IT TREATS IT AS A SINGLE DETERMINISTIC COLOUR. Raised by the reviewer while running `python3 -m pytest -n auto -q` as closure precondition 2 at `f78bba9c`. FIVE RUNS AT THE SAME HEAD PRODUCED FOUR GREEN AND ONE RED: four at a REAL exit 0 with `17817 passed, 20 skipped` and zero `^FAILED` lines, and one at exit 1 with `1 failed, 17816 passed, 20 skipped`, the failure being `tests/ui_server/test_live_state.py::TestUIServerIntegration::test_context_budget_endpoint`. THE MECHANISM IS READ FROM THE SOURCE, NOT GUESSED: `_start_server` at `tests/ui_server/test_live_state.py` polls for the server's info file 50 times at 0.1s and then calls `pytest.fail("Server did not start in time")`, so the budget is a FIXED FIVE SECONDS OF WALL CLOCK. Under `-n auto` that budget competes with every other xdist worker for CPU, and on a loaded machine a perfectly healthy server start loses the race. The same test passes SOLO at exit 0 in 0.32s, which is the discriminator: nothing is wrong with the endpoint, only with the budget. THIS IS DISTINCT FROM R-0445 AND FROM THE COLD-`dist` READING, THOUGH ALL THREE ARE THE SAME FIVE SECONDS. R-0445 is deterministic, fires in a BASE WORKTREE, takes out ALL EIGHT ids of that class, and is caused by a parity copy leaving `apps/ui/dist` older than its sources; its repair is to touch `dist` forward, and that repair would NOT have prevented this one, because `apps/ui/dist/index.html` was measured NEWER than every one of the 123 files under `apps/ui/src` at the moment of the red run. The cold-`dist` reading recorded in the F031 CLOSURE 2 block is a third trigger — the auto-build still running when the wait expires — and it too is a warm-`dist` non-explanation here. The unifying defect is the fixed budget, and the repair belongs with it: make the wait adaptive or generous under xdist rather than a flat 5s, in `tests/ui_server/test_live_state.py`, and consider whether the other TestUIServerIntegration ids share it. Medium and not Low because it lands on the ONE gate the closure protocol uses to decide whether a feature may close, so a single unlucky run can block a correct closure and a single lucky run can green-light a broken one. Not High because it produces no false GREEN of substance — the failure is loud, the id is captured here, and the endpoint under test is provably healthy. Routed to a follow-up rather than repaired in this feature: `tests/ui_server/` is outside F031's change set and a test-harness fix inside a closure round is scope drift. OPEN.
<<<END LEDGER69
