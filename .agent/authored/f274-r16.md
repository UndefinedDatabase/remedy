STEP — F274 ROUND 16 — the closure sequence opens: book round 15, book the owed R-0819 recurrence, and rule the split

Goal: F274 has reached the SESSION half of its soft limit — 15 delegated rounds, and this is session
SEVEN of SEVEN — so under operator amendment amend0827-process-diet rule 6 the next obligation is a
SCOPE REPORT rather than more feature work, and under amend0905-throughput the standing default at
that point is SPLIT-AND-CLOSE, executed by the session on its own authority. This round opens that
sequence. It books round 15's PASS verdict and the R-0819 recurrence the previous session left owed
on its durable carrier, and it records DECISION F274 D8 — the dated split ruling carrying the scope
report, the rejected alternatives and the reversal. NO LINE UNDER `packages/`, `apps/`, `tests/`,
`scripts/` OR `docs/` MOVES THIS ROUND, and gate G6 proves it.

Base commit for every reading in this block: `2cc1211f`.

THIS IS A CLOSURE-SEQUENCE ROUND, WHICH IS THE ONE PLACE A BOOKKEEPING ROUND IS PERMITTED. Operator
amendment amend0827-process-diet rule 1 forbids a round whose whole change set is verdicts,
registrations or corrections, "with exactly one exception: a feature's closure sequence" —
docs/agents/planner_reviewer_prompt.md §4 item 6, and docs/roadmap/STATUS_closure_protocol.md under
its "Closure-candidate findings" heading. This round is the first of that sequence, so the exception
applies and the round is not a violation of that rule. It is also why no repair is ordered here: the
feature registers nothing new and fixes nothing new, it rules and books.

WHAT THE REVIEWER RAN BEFORE AUTHORING. All three appliable slices were applied to a disposable
worktree at the base commit above, and every numeral gates G2, G3 and G4 order was read out of that
applied tree rather than computed by hand — the plan replacement, both appends, both negative
controls — and the four suite readings of G5 were taken there too. The suite figures are therefore
reference values a correct round reproduces, not predictions. ONE OF THEM IS DELIBERATELY NOT THE
WORKTREE READING: `tests/ui_server/test_dashboard_contract.py` gives 73 passed and 1 skipped in any
fresh worktree, because `test_typescript_compiles` skips when `apps/ui/node_modules/.bin/tsc` is
absent, and gives 74 passed and 0 skipped in the primary checkout where constraint 6 puts it. G5
orders the PRIMARY figure. That mismatch was round 13's declared deviation and it is not repeated
here.

EVERY NUMERAL THE ROUND 15 GATE PARAGRAPH CARRIES WAS RE-VERIFIED AGAINST GIT BEFORE IT WENT INTO A
SLICE, rather than copied from the handback that carried it: the seven commits and their order, the
three ledger sizes 602276, 607839 and 609858, the authored blob at 28161 bytes with its digest, the
six per-commit insertion counts, the two-path diff of the fix commit, and the map digest at both
ends. All reproduce exactly, and the slice says so in its own words.

FRAME CONVENTION. Every slice is delimited by a line reading `BEGIN <NAME> sha256=<hex> bytes=<n>`
and a line reading `END <NAME>`; the slice is the bytes BETWEEN those two lines, its leading newline
included, and marker lines never reach any file. No line of this block's FRAME — every line outside
a BEGIN/END pair — is a run of a single repeated character.


## Bundle — the commits of this round, in this order

C0a  Save this block verbatim as `.agent/authored/f274-r16.md`.
C0b  Mirror the same bytes into `.agent/last_block.md`.
C1   Replace `.agent/plan.md` with the PLAN16 slice.
C2   Append the RECORD16 slice to `.agent/live_review.md` — books round 15's PASS verdict and the
     owed R-0819 RECURRENCE, as two paragraphs.
C3   Append the DECISION16 slice to `.agent/decisions.md` — DECISION F274 D8, the split ruling.
C4   The handback: rewrite `.agent/handoff.md`, then push.

C1 is the first substantive commit because this round touches the finding ledger and the plan must be
current before every commit (§3 item 23). C2 precedes C3 because the ruling in DECISION F274 D8 is
written against a record that already carries round 15's verdict, and because findings and verdicts
persist first (§4 item 4).


## Change set — these paths and nothing else

  .agent/authored/f274-r16.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/decisions.md
  .agent/handoff.md


## Constraints

1. Apply every slice BYTE FOR BYTE. Do not reflow, retype or re-indent one. If something looks
   wrong, apply it as given and DECLARE the doubt in the handback.
2. RECORD16 and DECISION16 are APPENDS: the target's existing bytes are a byte-exact PREFIX of the
   result and the slice is an exact SUFFIX of it. Each carries its OWN leading newline — ADD NO
   SEPARATOR of your own, and do not strip one. PLAN16 REPLACES `.agent/plan.md` entirely and has no
   leading newline. FORTSCHRITT is appliable to no file; it is text the handback quotes.
3. Extract each slice from the COMMITTED `.agent/authored/f274-r16.md` by its BEGIN and END marker
   lines and apply it with a script. Do not retype a slice by hand into a target.
4. The path set of C0a through C3 is exactly the "Change set" paths other than `.agent/handoff.md`,
   which is C4's.
5. NO DESTRUCTIVE CHECK RUNS IN THE PRIMARY CHECKOUT. Any mutation or red control runs only inside a
   disposable `git worktree`, which is removed and pruned; `git status --porcelain` is empty at every
   commit boundary.
6. Run every command of G5 IN THE PRIMARY CHECKOUT, serially, one suite per invocation. The suites
   need the installed dependencies a fresh worktree lacks, and G5's dashboard figure is the primary
   checkout's.
7. Every gate below runs at a commit STRICTLY EARLIER than C4, so the handback can quote each one's
   real result (§3 item 31). Take G2, G3 and G4 at C1, C2 and C3 respectively; take G5, G6 and G7 at
   C3; take G1 and G8 at C0b and C3.
8. Do not write a `Done:` paragraph or a finding registration of your own. This round registers no
   finding and resolves none, and the open set is 63 by distinct id at both ends of it.
9. Report each gate's REAL result, including a failure. A gate that fails is a handback that says so;
   it is never a gate quietly re-scoped until it passes.


## The slices

BEGIN PLAN16 sha256=6bad38a2aac05d593b58c0856f786d2ceec07dacbaefed8a1348b0827c4a1410 bytes=2086
# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Finish what F272 could not reach inside its own limit. AT SESSION SEVEN OF SEVEN THE SOFT LIMIT
BINDS, so the goal is now the amend0905-throughput SPLIT-AND-CLOSE default: close F274 at the edge
work it actually built, and carry the cluster deletion, the atomic record flip and the classic
runner to a follow-up feature registered directly after it.

## Current Step

The closure sequence's first round: book round 15's PASS verdict and the second R-0819 recurrence
this feature owes, then record DECISION F274 D8 — the dated split ruling with its scope report, its
rejected alternatives and its reversal. No line under `packages/`, `apps/` or `tests/` moves.

## Next Steps

1. Register the follow-up feature in ONE atomic ledger commit — the STATUS line directly after
   F274's inside the same Tier 2 heading, the feature file, the `TOTAL_FEATURES` pin, the README
   counters, and the `Depends on` edit in every open feature naming F274 — and give F274's own file
   a Built State section naming which slices moved.
2. The integration-gate round: the full suite per docs/agents/integration_gate.md.
3. The self-use item closure precondition 6 requires. The queue holds no pending item, so
   `generate_and_append_if_empty` runs first, then the item is planned and run to the approval gate.
4. The closure sequence itself: the remaining verdict bookings, the ledger rotation, the evidence
   job, the fresh review zip, the STATUS `[x]` flip with the README sync, and the pull request.

## Risks

- The map was blind twice and is fixed once: R-0834's file-type blindness is closed, R-0832's
  event-name coupling is OPEN. Treat every "zero edges" reading as a claim about the WALKER.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12.
END PLAN16

BEGIN RECORD16 sha256=02bc3cd590ff642c93b20621eb73274ec64ea3a90b26e3fbf35115ee38095938 bytes=6360

Gate: F274 R15 — the F274 round 15 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER ITSELF against the COMMITTED blobs, in the primary checkout and in a disposable worktree. THIS ENTRY IS BOOKED BY ROUND 16 RATHER THAN BY ROUND 15, under operator amendment amend0827-process-diet rule 1, which makes a committed and pushed `.agent/handoff.md` a durable carrier so that a verdict never buys a round of its own; the carrier is the round 15 handback at `45f211b0`, superseded as the session-end state at `2cc1211f`, and this paragraph is the text it carried. Range `ea0d78c4`..`45f211b0`, seven commits, every one single-parent, in the ordered sequence C0a, C0b, C1, C2, C3, C4, C5. G1 TRANSPORT covers the chain this workflow can walk, per docs/agents/planner_reviewer_prompt.md §3 item 37 and not the emitted bytes: the reviewer's scratch original `.remedy-wt/f274-r15-FINAL.md`, hashed BEFORE delegation, and both committed copies are all 28161 bytes at `542a112cf3ccdbcaf3d32f980c60cd7dd13f85a4bbbc7a18b39b3c6604467d0b`. G2 THE VERDICT APPEND at `9537f46b`: 602276 to 607839 bytes, exact append, N counted as 2, units 236 to 238, ordered equality true, the control at byte offset 602277 rejected by BOTH readers; registrations 70 to 70, distinct resolutions 6 to 6, OPEN SET 64 TO 64 BY DISTINCT ID, `^Gate: ` 45 to 46. G3: `.agent/plan.md` byte-equal to its slice at 42 lines against the cap of 50. G4 THE FIX at `2d027f36`: every pair reads FROM 0 and TO 1; the repo-wide sweep for `agent_loop_cycle_decision` and `agent_loop_stopped` over `packages/`, `apps/`, `tests/`, `scripts/` and `docs/` EXITS 1 WITH NO MATCH against TWELVE sites at the base, both counts re-measured by the reviewer; and that commit's own path set is exactly `packages/orchestration/event_schemas.py` and `tests/orchestration/test_event_ledger.py`. G5 THE SUITES, each run ALONE: 19, 26, 81, 82, 3 and the canary at 42, every figure the block's reference, and `ruff` EXIT 0 on both touched paths with the frozen ceiling of DECISION F083 D5 unchanged at 26. G6 THE RED PROOFS, re-run by the reviewer in its own disposable worktree at the round's last content commit: the sweep gate is shown to be able to FAIL — control exit 1 with no match, mutated exit 0 naming the file, restored exit 1 — and the rewritten assertions are shown to BIND, deleting `token_policy_applied` from the registry redding exactly `test_schemas_exist` and `test_different_schemas_for_different_events`, the two tests the fix rewrote. G7 THE RESOLUTION APPEND at `2f79a714`, which runs AFTER the fix so the paragraph it lands is true when it lands: 607839 to 609858 bytes, exact append, N counted as 1, units 238 to 239, control at 607840 rejected by both readers, distinct resolutions 6 to 7, OPEN SET 64 TO 63 BY DISTINCT ID, `^Done: R-0836 — ` 0 to 1. G8 THE TREE AND THE SCOPE GUARD: porcelain empty, `git ls-files .remedy-wt` empty, worktrees 14, per-commit insertions 341, 235, 14, 4, 8 and 2 for C0a through C4, every one under the DECISION F104 D1 cap of 500, and `tests/orchestration/cluster_deletion_map.txt` BYTE-IDENTICAL at the base and at C4, both `7fbf3909fd6d094e0ab3654e8842222a1adf6a51cd6c74bf119b1f7c256d5155`. THE REVIEWER RE-VERIFIED EVERY ONE OF THOSE NUMERALS AGAINST GIT AT `2cc1211f` BEFORE BOOKING THIS PARAGRAPH, rather than copying them from the carrier: the seven commits and their order, the three ledger sizes, the authored blob's length and digest, the six insertion counts, the two-path commit diff and the map digest at both ends all reproduce exactly. TWO DEVIATIONS WERE DECLARED AND THE REVIEWER SUSTAINS BOTH. THE FIRST IS THE REVIEWER'S OWN DEFECT and is booked as the R-0819 recurrence directly below. THE SECOND IS PROCEDURAL: the session's shell guard refused `$?` and a `python3 -c` body carrying a `#` comment BY FORM, and every affected check was re-run through a Python runner invoking the identical command and printing the real return code, so no exit code was inferred. NO FINDING IS REGISTERED BY THIS GATE AND NO NEW ID IS MINTED, so the open set stands at 63 by distinct id and the next free id is R-0837.

RECURRENCE of R-0819 at F274 round 15, measured by the reviewer at `45f211b0` and booked here by round 16's first ledger commit. NO NEW ID IS SPENT: docs/agents/planner_reviewer_prompt.md §3 item 30 requires the open set searched for the DEFECT before an id is minted, and R-0819 is OPEN and holds this class — a gate ordering a value no correct run can produce. THE INSTANCE. The round 15 block's gate G4(d) ordered that `git diff --name-only ea0d78c4..<C3>` "names exactly those two paths", meaning `packages/orchestration/event_schemas.py` and `tests/orchestration/test_event_ledger.py`. That range begins at the round's BASE and therefore necessarily contains C0a, C0b, C1 and C2, so it names SIX paths — the two above plus `.agent/authored/f274-r15.md`, `.agent/last_block.md`, `.agent/plan.md` and `.agent/live_review.md` — and the ordered reading is reachable by no correct round. All six are inside the block's own declared change set, so nothing was out of scope; only the gate was wrong. THE CAUSE IS NEW AND IS WHAT THIS RECURRENCE ADDS, and it is not the cause the round 14 recurrence names. That one was a property of the pair SET which no per-pair reading could see, and its counter-measure — group the TO blocks by target file and compare them — WAS applied in this very block and worked, G4(a)'s twelve numbers all reproducing. This defect is different: the gate's PROPERTY is right and its RANGE is wrong, because a per-commit property was ordered over a BASE-to-commit range that contains the round's own bookkeeping commits. THE ADDITION TO R-0819's FIX, binding on every later block of this feature and of the feature that inherits its remaining scope: a gate asserting the path set of ONE commit names that commit's own diff — `git diff --name-only <parent>..<commit>`, or `git show --name-only <commit>` — and never a range beginning at the round's base; a base-anchored range is correct only for a claim about the WHOLE round's change set, and the two claims are then stated separately because they have different answers. THE ROUND LOST NOTHING: the worker ran BOTH readings, reported the six-path range and the two-path commit diff, and declared the gap rather than adjusting anything.
END RECORD16

BEGIN DECISION16 sha256=b14177ac0e5148619e4e9d80f118c0ba6e6ded0f4d9a1186c5c7de7f77a13554 bytes=8322

## DECISION F274 D8 — F274 CLOSES AT THE EDGE WORK IT BUILT, and the cluster deletion, the atomic record flip and the classic runner move to a follow-up feature registered directly after it (2026-09-08)

Date: 2026-09-08. Feature F274, round 16, session 7. Status: decided by the reviewer under
docs/agents/planner_reviewer_prompt.md §4 item 7 and EXECUTED on the session's own authority under
operator amendment amend0905-throughput; the operator's veto is any later session.

WHY THIS RULING HAPPENS NOW RATHER THAN LATER. F274 stands at 15 delegated rounds and this is its
SEVENTH session, so the SESSION half of the soft limit binds first and the ROUND half does not bind
at all. `docs/roadmap/features/T2_F274.md` rules the applicable limit explicitly in its Orchestrator
brief — "This feature's soft limit is the standing 7 sessions and 25 rounds: amend0906 granted
12-and-40 to F272 BY NAME, on a measurement of F272's scope, and such a grant does not travel with a
split" — so the wider budget F272 ran under is not available here and no reading of amend0906 makes
it so. Operator amendment amend0827-process-diet rule 6 makes the obligation at the limit a SCOPE
REPORT rather than more work, and amend0905-throughput makes the standing default at that point
SPLIT-AND-CLOSE, EXECUTED BY THE SESSION rather than proposed and waited on. Rowing on quietly is a
protocol violation; so is stopping to ask a question the default already answers.

THE SCOPE REPORT, PART ONE — WHAT F274 ACTUALLY BUILT. Measured by the reviewer at `2cc1211f`, this
round's base, over the range from the branch's fork point
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, which is 130
commits, and 46 files under `packages/`, `apps/`, `tests/`, `scripts/` and `docs/` at 1269
insertions against 1340 deletions — a feature that removed more than it added, which is what a
deletion feature should read like.

- THE DELETION MAP AS A LIVE RATCHET. `tests/orchestration/cluster_deletion_map.txt` records one
  surviving consumer edge per line, is GENERATED from the live import graph rather than typed, and
  is held against that graph in BOTH directions by `tests/orchestration/test_cluster_deletion_map.py`
  — so a re-inserted edge reddens a test instead of passing unnoticed. Neither file existed before
  this feature. Finding R-0830 is why the deletion is bounded by edges rather than by F260's module
  list at all.
- THE IMPORT-REACHABILITY RATCHET that T003's deletion runs behind:
  `tests/orchestration/test_import_reachability.py` with its 326-line allowlist, ruled a RATCHET
  rather than a one-shot gate by DECISION F274 D1.
- THE EDGE WORK ITSELF. The map today records TWENTY surviving consumer edges across ELEVEN of the
  twenty-four cluster modules, leaving THIRTEEN with no edge at all, and
  `packages.orchestration.worker_recommend` is one of the thirteen and is deletable now. At the
  map's creation commit `0d6da86f` it recorded 42 edges across 22 modules; those two readings are
  NOT a clean before-and-after, because R-0834's fix widened the walker to non-Python files in
  between, so the honest claim is the direction and the current absolute figure, never their
  difference.
- THE COCKPIT AND COMMAND-LAYER CUTS. `packages/orchestration/ui_server.py` lost 458 lines and
  gained none; the `feature` command group was deleted whole at 101 lines; and
  `apps/cli/commands/context.py` and `apps/cli/commands/worker.py` were cut into the per-command
  modules their surviving halves needed.
- SEVEN DATED RULINGS, DECISION F274 D1 through D7, each naming what dies, what inherits its idea
  and how to reverse it — the replace-is-delete discipline AGENTS.md Scope Control requires, applied
  ruling by ruling rather than assembled at the end.
- THE FINDINGS. Seven were registered by this feature, R-0830 through R-0836; four are resolved,
  R-0833, R-0834, R-0835 and R-0836; three stand open as documented risks, R-0830, R-0831 and
  R-0832. The High findings still open on the record are R-0803, R-0804, R-0806 and R-0807, and
  every one of them is F273's rather than this feature's, per DECISION F272 D12.

THE SCOPE REPORT, PART TWO — WHAT IS MISSING, measured at the same commit. Twenty consumer edges
survive across eleven cluster modules: `orchestrator_brain.py` and `apps/cli/commands/
worker_facade_cmd.py` carry four each, `ui_server.py` three, `token_economy.py`, `self_dogfood.py`
and `self_dogfood_execution.py` two each, and `provider_patch_material.py`, `real_test_execution.py`
and `repair_request_builder.py` one each; on the other side `packages.orchestration.provider_trust`
alone is the target of seven of the twenty and is the single biggest blocker. The two carry-overs
F260's Design section names have not begun, DECISION F260 D3 is undrafted, and T001 and T002 have
not begun at all. `.agent/plan.md` carried five open steps into this round, read at `2cc1211f`.

CHOSEN: SPLIT AT THE T-SLICE SEAM THE FEATURE FILE ALREADY NAMES. F274 closes at what it built — the
map, the reachability ratchet, D1 through D7, the cockpit and command-layer edge cuts and the
`worker_recommend` retirement — and a follow-up feature inherits the remaining edges, the two
carry-overs, DECISION F260 D3, the deletion itself, T001 and T002. Three mechanical obligations come
with that and are executed in the registration round, not left as intentions. The follow-up's STATUS
line is placed IMMEDIATELY after F274's inside the SAME Tier 2 heading, per operator amendment
amend0906-split-placement, so Rule A5 proposes it before any other unchecked feature. Every OPEN
feature file naming F274 in its `Depends on` line gains the follow-up there in the same commit. And
the registration is ONE commit carrying the STATUS line, the feature file, the `TOTAL_FEATURES` pin
in `tests/docs/test_docs_consistency.py` and the README counters together, because splitting it
leaves an intermediate state in which `tests/docs/` is red.

WHY THIS CLOSE IS SELF-CONSISTENT AND NOT A HALF-PERFORMED ONE. The single state this work must not
leave behind is a partly-deleted cluster, and there is none: no cluster module has been removed, the
map is a complete generated work list rather than a partial one, and every edge cut so far landed
with its own tests and its own dated ruling. What F274 hands over is a SMALLER problem described by
a machine-checked file, not a broken one — which is exactly the condition amend0905-throughput
attaches to the split-and-close default.

ALTERNATIVES CONSIDERED AND REJECTED. (a) RUN ON PAST THE LIMIT and finish T003 — rejected because
amend0827 rule 6 names continuing quietly past the limit a protocol violation in as many words, and
because T003 does not fit: twenty edges across nine consumer files, four of them the Orchestrator
brain's live signal reads, is not one session's work at this feature's measured rate of three to
five rounds per session. (b) START T003 NOW AND SPLIT INSIDE IT — rejected outright; the feature
file's Orchestrator brief states that a session which cannot finish T003 does not start it, and a
half-performed deletion is the one state that brief forbids by name. (c) HARD STOP WITH AN OPERATOR
QUESTION — rejected because amend0905-throughput reserves that for the case where NO self-consistent
close is possible, and one is, as the paragraph above measures. (d) CLOSE F274 WITH NO FOLLOW-UP and
let the remaining scope be absorbed by F271, "no more legacy" — rejected because the deletion is
bounded by a generated map this feature owns and by DECISION F260 D3, which is owed by the deletion
round and by nothing else; routing a specific owed ruling into a feature with a different Goal is
how such a ruling gets lost, which is the failure DECISION F272 D16 was written to avoid one split
earlier.

HOW TO REVERSE. Delete this paragraph; revert the single registration commit that adds the follow-up
feature's STATUS line, its feature file, the `TOTAL_FEATURES` pin, the README counters and the
`Depends on` edits; restore F274's STATUS marker from `[x]` to `[~]` with the README counters that
go with it; and resume at `.agent/plan.md`'s step list as this round found it. Nothing under
`packages/`, `apps/` or `tests/` changes behaviour by this ruling, so the reversal is a
documentation revert and carries no product risk.
END DECISION16

BEGIN FORTSCHRITT sha256=fa638857cf5a1db90dac9284734140d5ec3defa869784d33b5ebf2bdeba1122f bytes=219
Fortschritt: ~35 % des ursprünglichen Umfangs gebaut (T003-Vorarbeit ✅ — Löschkarte, Reachability-Ratsche, D1–D7, Cockpit- und CLI-Kanten · T003-Löschung, T001 und T002 offen → Folge-Feature) — Schätzung
END FORTSCHRITT


## Done when

G1  TRANSPORT, one digest comparison, at C0b. `.agent/authored/f274-r16.md` and
    `.agent/last_block.md` are BYTE-IDENTICAL to each other and to the reviewer's scratch original at
    `/home/decodeux/Repos/remedy/.remedy-wt/f274-r16-FINAL.md`. Report the sha256 and the byte count
    of all three. This proof covers the chain this workflow can walk — the saved copy, its mirror,
    the reviewer's original — and claims nothing about the bytes that reached you (§3 item 37).

G2  THE PLAN, at C1. `.agent/plan.md` is byte-identical to the PLAN16 slice; report its sha256, its
    byte count and its line count, and report that it carries exactly one `## Goal` line and exactly
    one `## Next Steps` line. Reference: 2086 bytes, 37 lines, both headings once, against the
    AGENTS.md cap of 50 lines.

G3  THE RECORD APPEND, at C2. Report, from the file itself: byte count before and after; that the
    post-image equals the pre-image concatenated with the slice EXACTLY; N, the number of blank-line
    paragraphs in the slice, COUNTED by your script and not taken from this block; that the last N
    blank-line units of the whole file equal the slice's N paragraphs IN ORDER; and that a control
    which flips one byte inside the FIRST appended paragraph, at byte offset 609859, is REJECTED by
    both the byte reader and the ordered-unit reader. Then report these counts before and after:
    blank-line units; lines matching `^Gate: `; lines matching `^Gate: F274 R15 `; distinct
    registrations `^- R-\d+ — `; distinct resolutions `^Done: R-\d+ — `; and the open set as
    distinct registrations minus distinct resolutions. Reference: 609858 to 616218 bytes, N is 2,
    units 239 to 241, `^Gate: ` 46 to 47, `^Gate: F274 R15 ` 0 to 1, registrations 70 to 70,
    distinct resolutions 7 to 7, OPEN SET 63 TO 63 BY DISTINCT ID.

G4  THE DECISION APPEND, at C3. The same shape as G3 against `.agent/decisions.md`: byte count
    before and after, exact concatenation, N counted by your script, the last N units equal to the
    slice's paragraphs in order, and the control at byte offset 911447 — inside the FIRST appended
    paragraph — rejected by both readers. Also report `^## DECISION F274 D8 ` before and after.
    Reference: 911446 to 919768 bytes, N is 10, units 2000 to 2010, `^## DECISION F274 D8 ` 0 to 1.

G5  THE SUITES, in the PRIMARY checkout, each in its own invocation, at C3. Report the exit code and
    the passed/skipped counts of each:
      python3 -m pytest tests/ui_server/test_dashboard_contract.py -q
      python3 -m pytest tests/orchestration/test_progress_ledger.py tests/orchestration/test_development_artifact_boundary.py tests/orchestration/test_live_review_rotation.py -q
      python3 -m pytest tests/docs/ -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    Reference: 74 passed and 0 skipped; 59 passed; 303 passed; and the canary at 42 passed. Every
    one exits 0.

G6  THE SCOPE GUARD, at C3. `git diff --name-only 2cc1211f..<C3>` names ONLY paths beginning
    `.agent/`, and names NONE beginning `packages/`, `apps/`, `tests/`, `scripts/`, `docs/` or
    `README.md`. THE BASE-ANCHORED RANGE IS DELIBERATE AND IS THE ONE READING R-0819's FIX CLAUSE
    PERMITS: that clause forbids a base-anchored range for a claim about ONE COMMIT's path set and
    allows it for a claim about the WHOLE ROUND's change set, and this gate makes only the second
    claim. No gate in this block asserts a single commit's path set at all.
    Report the full path list it returns rather than a count. Separately, report that
    `tests/orchestration/cluster_deletion_map.txt` has the same sha256 at `2cc1211f` and at C3, read
    with `git show <commit>:<path>` and never by writing into the checkout.

G7  THE PER-COMMIT NUMBERS, at C3, for C0a, C0b, C1, C2 and C3 and NOT for C4, whose own numbers
    cannot exist while its text is being written. For each, report the insertion count from
    `git diff --numstat <parent>..<commit>` and confirm it is under the DECISION F104 D1 cap of 500
    insertions. The `## Commits` table of `.agent/handoff.md` carries these same values, and its
    `+/-` cells are the `git diff --numstat` columns cell for cell — NOT a file's line counts before
    and after, which differ for a full-file rewrite such as C0b and C1 (§3 item 28). State in the
    handback that you compared the two.

G8  THE TREE AND THE RECORD-SLICE SCAN, at C3. `git status --porcelain` is EMPTY;
    `git ls-files .remedy-wt` is EMPTY; report `git worktree list` and confirm every worktree this
    round created was removed and pruned. Then, for the RECORD16 and DECISION16 slices as committed
    in `.agent/authored/f274-r16.md`: delete every backtick-quoted span, then report the count of
    `\bHEAD\b` in what remains. Reference: ZERO for both, which is what finding R-0586's scan
    requires of any text bound for an append-only record.


## Handback

Rewrite `.agent/handoff.md` per AGENTS.md and docs/agents/handback_template.md. It has no length cap
(amend0827 rule 3); it is valid when its mandated sections are present. It must carry:

- the state block, naming the feature, the round, THE SESSION NUMBER — session 7 of feature F274 —
  the branch, and the commit SHAs;
- the Fortschritt line, verbatim from the FORTSCHRITT slice above;
- the changed-files table and the `## Commits` table whose `+/-` cells G7 pins;
- ONE LINE PER GATE, G1 through G8, each carrying that gate's REAL measured result;
- the open-findings count, 63 by distinct id, with the arithmetic that produced it;
- every deviation, declared with its reason;
- the item-status table AGENTS.md requires, with every ordered item of this block appearing exactly
  once as done, skipped or deviated;
- the next expected action: the registration round that adds the follow-up feature, per DECISION
  F274 D8 as this round lands it.

Then push the branch. Do not create a pull request; the closure sequence creates it in its own round.
