STEP CORRECTION ROUND / F031 — DECISION INBOX
Goal:        Correct a FALSE SENTENCE THE REVIEWER ITSELF AUTHORED, which the
             last round applied byte for byte exactly as it was told to and
             correctly declared rather than silently fixing. `R-0708` is now in
             the append-only ledger carrying the clause "`tests/ui_server/` is
             outside F031's change set", and that clause is measurably wrong:
             F031 changes FIVE files under `tests/ui_server/`, one of them the
             very file the finding is about. The finding's CONCLUSION survives
             and this round proves why. It also records the RECORD ROUND verdict.
             This round writes NO `docs/roadmap/STATUS.md` line, syncs NO README,
             and creates NO pull request. No production code, no tests, no docs.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the ledger append · C3 the handoff · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r70.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/handoff.md`. This list bounds what you WRITE INTO THE
             REPOSITORY. It does NOT bound what you DO: G11 orders a push.
             NOTHING under `apps/`, `packages/`, `tests/` or `docs/`.

Constraints:
 1. THIS BLOCK REACHES YOU AS A FILE, NOT AS PROSE IN A PROMPT. Read
    `.remedy-wt/f031-r70.md` from disk and copy it BYTE FOR BYTE to
    `.agent/authored/f031-r70.md` — with `shutil.copyfile` or a read-then-write
    in python, never by retyping it and never with `cp`, which this session's
    guard rejects. This block asserts NO digest of its own, because a digest
    written inside the text it measures cannot be true; G2 has you measure four
    points and prove them EQUAL, and the reviewer holds the scratch value
    independently.
 2. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. A slice's text is its content lines joined with a newline
    plus ONE trailing newline. If a slice contradicts something you measure,
    apply it anyway and DECLARE the contradiction in the handback under
    Deviations — a corrected slice destroys the transport proof. THE LAST ROUND
    DID EXACTLY THIS AND IT IS WHY THIS ROUND EXISTS: declaring beats fixing,
    every time, because a declared contradiction reaches a reviewer who can
    measure it while a silent fix reaches nobody.
 3. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3.
 4. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES THE RECORD ROUND.
    That is ordered: the plan becomes current at C1.
 5. NOTHING IS EDITED OUT OF THE LEDGER. `.agent/live_review.md` is APPEND-ONLY
    and `R-0708`'s existing paragraph is NOT rewritten, NOT deleted and NOT
    touched. The correction is a NEW paragraph appended after it. An append-only
    record is corrected by appending, never by revising history in place.
 6. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Gate:` paragraph of
    your own and never mint a finding id. LEDGER70 carries ONE paragraph. NO
    FINDING IS REGISTERED AND NONE IS RESOLVED THIS ROUND. If you find a further
    defect, report it in the handback under Deviations and let the reviewer rule
    on it.
 7. THE LEDGER SETS MOVE ONCE. Across C2 `^Gate: F\d+ R\d+ — ` moves 50 to 51
    with the ADDED key exactly `F031 R69`. `^- R-\d+ — ` stays 269,
    `^Done: R-\d+ — ` stays 17, `^Landed: R-` stays 0 and `^Gate: R\d+ — `
    stays 19. The open set is 252 before C2 and 252 after C2, and the maximum id
    is `R-0708` at BOTH points — this round mints nothing.
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
    next. Declare DECISION D15 only if the MANDATED content still does not fit
    in that shape, and name what actually caused it.
11. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `${...}` and every other expansion, `cp`, brace literals
    containing a quote character, `cd x && y`, file redirects, and every form of
    environment assignment. Route anything that counts, hashes or compares
    through a quoted python heredoc, read real exit codes from
    `subprocess.run(...).returncode`, and pass `cwd=` rather than `cd`. Run
    pytest SERIALLY — never two pytest processes alive at once. `--timeout` IS
    NOT AVAILABLE to pytest here: passing it exits 4 and reports no failure.
12. EVERY NUMERAL THIS BLOCK STATES ABOUT THE ROUND BASE `31331a3f` was measured
    by the reviewer at that commit. It is a REFERENCE to report against, NOT a
    target to reproduce. Where your measurement differs, report BOTH and
    reconcile NOTHING.
13. THIS IS THE LAST ROUND OF ITS SESSION. The rounds this session delegated are
    CLOSURE 2 OF 3, the RECORD ROUND and this CORRECTION ROUND, and a SESSION
    line naming all three — including this terminating round itself — belongs in
    the handoff. The next expected action is CLOSURE 3 OF 3 and you name it by
    that label and by no round number, because §3 item 35 forbids numbering a
    round that has not begun.
14. DO NOT RE-RUN THE FULL SUITE. `python3 -m pytest -n auto -q` is NOT a gate of
    this round; it is registered as intermittent in `R-0708` and another sample
    would add nothing this round can act on.

Done when — run every gate yourself and record its REAL exit code, ONE LINE per
gate in the handback with transcripts kept out of it. G1 through G10 all run
BEFORE C3, so the handback can quote every one of them. G11 is the single
exception and its own text states how it is treated. The round base is
`31331a3f` throughout. Read every non-current revision with
`git show <rev>:<path>` into memory; never write a past blob over a tracked file.
 G1. BRANCH, CLEANLINESS, STOP. Branch is `feature/f031-decision-inbox`.
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1 and C2.
     `.agent/STOP` read from disk before C0a and before C3, both ABSENT.
 G2. TRANSPORT. Report the sha256, byte count and line count of this block as
     read from `.remedy-wt/f031-r70.md`, as saved at C0a, as mirrored at C0b and
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
 G4. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R70 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G5. THE LEDGER APPEND, PROVED TWICE, THE SECOND READER COVERING THE WHOLE
     APPENDED REGION. `.agent/live_review.md` at C2 equals its pre-commit blob
     plus ONE newline plus LEDGER70. The reviewer measured the base blob at
     `31331a3f` itself: 1003228 bytes over 400 blank-line units. If it reads
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
 G7. THE R-0708 PARAGRAPH IS UNTOUCHED. Prove constraint 5 held: extract the
     `- R-0708 — ` paragraph from `.agent/live_review.md` at the round base and
     again at C2, report its sha256 at BOTH points, and confirm they are EQUAL
     and that it occurs EXACTLY ONCE at each. Report also that the file at C2
     STARTS WITH the file at the round base as a byte prefix, which is what
     append-only means and what forbids an in-place revision.
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
     Compare the path set of `git diff --name-only 31331a3f..C2` BOTH WAYS
     against this round's expected set — the Change line's list MINUS
     `.agent/handoff.md`, which C3 writes — and report both residues EMPTY.
     Report `git diff --stat 31331a3f..C2` restricted to `apps/`, `packages/`,
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
             being `R-0708` and shown by this round NOT to be an F031 defect, so
             may the STATUS line carry `[x]`. Make the next-action section
             CLOSURE 3 OF 3 and name no round number for it. Include the SESSION
             line constraint 13 orders.

<<<SLICE PLANF031R70
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
CORRECTION ROUND. The RECORD ROUND passed every gate, and this round writes that
verdict together with a correction to a clause the reviewer itself authored
inside `R-0708`. The finding's conclusion stands and this round proves it from
the diff; only the supporting clause was wrong. It writes NO STATUS line, syncs
NO README and creates NO pull request: closure is deferred to the operator.

## Next Steps
1. CLOSURE 3 of 3 — the STATUS line from `[~]` to `[x]` with the README
   capability sync in the SAME commit, then the pull request, which is NOT
   merged in the session that creates it. The five closure values it needs
   already exist and are carried in the handoff; the package is NOT rebuilt.

## Risks
- CLOSURE PRECONDITION 2 IS INTERMITTENT RATHER THAN GREEN. The reviewer ran
  `python3 -m pytest -n auto -q` five times at the reviewed head and measured
  four GREEN at 17817 passed with 20 skipped, and one RED at 17816 passed with
  one failed. The red is `R-0708`.
- `R-0708` IS NOT AN F031 DEFECT, AND THE REASON IS NARROWER THAN THIS PLAN
  ONCE CLAIMED. F031 does change `tests/ui_server/`, five files of it, one of
  them `test_live_state.py` itself. What F031 does to that file is APPEND one
  test class that starts no server; the failing class, its five-second helper
  and the failing test are untouched by this branch.
- WHETHER AN INTERMITTENTLY GREEN PRECONDITION MAY CARRY AN `[x]` IS AN OPERATOR
  QUESTION. The rules do not answer it, and guardrail G8 of the self-drive
  protocol ends a session on exactly that kind of question rather than guessing.
- THE CLOSURE PACKAGE ALREADY EXISTS and does not need rebuilding. It was built
  from a clean tree at the reviewed head and its manifest names that head.
- R-0495 and R-0574 are inherited standing Highs from the already-closed F085
  and F086, documented risks rather than F031 defects, and they rode through six
  prior closures on the same footing.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 252 and this round
  moves it by nothing.
<<<END PLANF031R70

<<<SLICE LEDGER70
Gate: F031 R69 — the F031 RECORD ROUND entry, AND THE CORRECTION OF A CLAUSE THE REVIEWER ITSELF PUT INTO `R-0708` ONE ROUND EARLIER. THE ROUND PASSED on every gate its block ordered, G1 through G11, and the reviewer re-ran every one itself. TRANSPORT held at four points — scratch, C0a, C0b and the working copy all sha256 `d7c60991d8569544ee89530b38a41edfdd083a45946708c2aaaaada35230062d` over 23831 bytes and 242 lines, C0a and C0b the SAME blob `99a3d96becfa`. EXTRACTION printed 2 slices at 43 and 3 content lines, CONTENT 46, TOTAL 242, PROSE 196. THE PLAN at C1 is byte-equal to PLANF031R69 with the control FALSE and `wc -l` 43. THE LEDGER APPEND at C2 proves twice: 995738 + 1 + 7489 = 1003228 against a committed 1003228 and a byte-equal reconstruction, N 2, units 398 to 400, the last two units EQUAL IN ORDER, and a one-byte flip at byte offset 995779 REJECTED by both readers. THE SETS MOVED EXACTLY TWICE as ordered: `^Gate: F\d+ R\d+ — ` 49 to 50 adding `F031 R68` and `^- R-\d+ — ` 268 to 269 adding `R-0708`, while `^Done: R-\d+ — ` stayed 17, `^Landed: R-` stayed 0 and `^Gate: R\d+ — ` stayed 19; open 251 to 252. NOTHING ELSE MOVED: both path residues EMPTY, `apps/`, `packages/`, `tests/` and `docs/` each EMPTY, insertions 242, 144, 25, 4 and 40, each single-parent and under 500, markers 0 and 0 against a CONTROL of 4, `.remedy-wt` 0 tracked, worktree 1 line, no `tmp/*` branch, and the push landing at a remote tip equal to the local one with zero amend, rebase or cherry-pick entries in the reflog. NOW THE CORRECTION, WHICH IS THE REASON THIS ENTRY EXISTS. `R-0708` closes with the clause "`tests/ui_server/` is outside F031's change set", and THAT CLAUSE IS FALSE. Measured at this round's base over `6325ac2f..HEAD`, F031 changes 31 files under `apps/`, 3 under `packages/` and 8 under `tests/`, and FIVE of those are under `tests/ui_server/`: `test_command_channel.py`, `test_command_dispatch.py`, `test_dashboard_contract.py`, `test_decisions_endpoint.py` and — the one that matters — `test_live_state.py`, the file `R-0708` is about. The companion sentence in PLANF031R69, "this feature changed nothing under `apps/`, `packages/` or `tests/`", is wrong the same way; both meant to say THE ROUND and said THE FEATURE. THE FINDING'S CONCLUSION SURVIVES, AND ON BETTER EVIDENCE THAN IT ORIGINALLY CARRIED. `tests/ui_server/test_live_state.py` is touched by exactly ONE commit on this branch, `6b68718e`, and that commit's diff to the file is a PURE APPEND of the class `TestOpenDecisionCountComesFromTheDecisionQueue` — three tests that call `_build_live_state_json` under `unittest.mock.patch` and start no server at all — plus one import line gaining `patch`. It does not touch `TestUIServerIntegration`, it does not touch the `_start_server` helper whose fixed fifty-times-0.1-second wait IS the defect, and it does not touch `test_context_budget_endpoint`, the id that actually failed. So the correct statement of the routing reason is the narrow one: the FAILING CLASS, ITS HELPER AND THE FAILING TEST are outside F031's change set, even though the FILE is not. `R-0708` stays OPEN, stays Medium, and keeps its severity argument unchanged. THE LESSON IS THE ONE THE ROUND ALREADY DEMONSTRATED. The worker applied the false sentence byte for byte and DECLARED it as a G10 residual rather than quietly repairing it, which is exactly what constraint 2 asks for and is the only reason the error reached a reviewer who could measure it; a silent fix would have left the ledger correct by accident and the reviewer none the wiser. The repair is APPENDED, never edited in place: `R-0708`'s paragraph is byte-identical before and after this commit and the file at C2 still has the base file as a byte prefix, because an append-only record is corrected by appending. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no unverified completion claim and no silent scope change.
<<<END LEDGER70
