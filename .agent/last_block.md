STEP — F274 ROUND 19 — the self-use precondition: generate the tier-1 item, run it to the approval gate, and record what it surfaced

Goal: satisfy docs/roadmap/STATUS_closure_protocol.md precondition 6, which F274 cannot close
without. EXACTLY ONE self-use item is consumed by this close. Every one of the twelve items in
`scripts/self_use_queue.json` already carries a `consumed_by`, so `next_self_use_item()` answers
`None` and the protocol's own instruction applies: call
`packages.orchestration.self_use_generator.generate_and_append_if_empty` FIRST, then plan and RUN
the item it appends through `packages.orchestration.self_use_runner.run_next_self_use_item` to the
normal approval gate like any other job — NEVER applied — and record verbatim every string
`packages.orchestration.self_use_findings.describe_self_use_run_defects` returns for the run's own
`JobPlan`. This round also books round 18's PASS verdict and the two R-0819 recurrences that
round's gates earned.

Base commit for every reading in this block: `ae7607e6`.

THE ITEM'S `consumed_by` STAYS EMPTY THIS ROUND. Precondition 6 says the `consumed_by` is set "in
the closure commit", and an item a run could check off itself is not a gate — the queue file's own
header says so. C3 appends the entry with a blank `consumed_by` and G4 proves it blank.

THIS ROUND REGISTERS NO FINDING, AND THAT IS DELIBERATE RATHER THAN AN OMISSION. Precondition 6
requires every defect string registered as a normal R-id finding BEFORE the close, and §3 item 30
requires the open set searched for the DEFECT before an id is minted — a step only the reviewer
performs and only against text it has read. The defect strings do not exist until this round's run
produces them. So this round REPORTS them verbatim and the CLOSURE round registers them in its
first commit, which is where the closure sequence puts findings anyway. An empty tuple means
nothing to register, not that nothing was checked, and the handback says which of the two it is.

WHAT THE REVIEWER MEASURED BEFORE AUTHORING, read-only and against a COPY of the queue rather than
the tracked file, which was left byte-identical. `pending_self_use_items()` is 0 and
`next_self_use_item()` is `None` at the base. The generator's tier 1 — the oldest open Low or
Medium finding in `.agent/live_review.md` — resolves to `R-0445`, and
`generate_and_append_if_empty` against the copy appended `SU-013`, "Address ledger finding
R-0445", provenance `generated (self-use-generator tier 1, ledger scan, R-0445)`, `consumed_by`
the EMPTY STRING, taking the queue from 38745 to 43764 bytes and 12 to 13 items, after which
`pending_self_use_items()` is 1, `next_self_use_item()` answers `SU-013` and `SU-013` is the ONLY
entry with a blank `consumed_by`. Role config resolves `builder` and `reviewer` to provider
`ollama` with model `muse-glimmer:latest`, and the local daemon answers `/api/tags` with that model
present — which matters because `run_next_self_use_item` REFUSES to run unflagged when role config
resolves to `fake`.

THE RUN'S OUTCOME IS NOT PREDICTED AND NO GATE BELOW ORDERS ONE. A real provider run is not
reproducible, so G5 orders PROPERTIES — that a real provider ran, that the job reached the approval
gate, that nothing was applied, that the primary checkout stayed clean — and orders every number
REPORTED rather than matched. F272's comparable run took 251.76 seconds; that is context, not a
budget.

FRAME CONVENTION. Every slice is delimited by a line reading `BEGIN <NAME> sha256=<hex> bytes=<n>`
and a line reading `END <NAME>`; the slice is the bytes BETWEEN those two lines, its leading
newline and its trailing newline INCLUDED, and marker lines never reach any file. No line of this
block's FRAME is a run of a single repeated character.


## Bundle — the commits of this round, in this order

C0a  Save this block verbatim as `.agent/authored/f274-r19.md`.
C0b  Mirror the same bytes into `.agent/last_block.md`.
C1   Replace `.agent/plan.md` with the PLAN19 slice.
C2   Append the RECORD19 slice to `.agent/live_review.md` — books round 18's PASS verdict and the
     two R-0819 recurrences, as three paragraphs.
C3   THE SELF-USE ITEM: generate and append it to `scripts/self_use_queue.json`, run it, and write
     the run's evidence under `.agent/selfuse_f274/`. ONE commit.
C4   The handback: rewrite `.agent/handoff.md`, then push.

C1 is the first substantive commit because this round touches the finding ledger and the plan must
be current before every commit (§3 item 23). C2 precedes C3 because verdicts persist first
(§4 item 4).


## Change set — these paths and nothing else

  .agent/authored/f274-r19.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/selfuse_f274/
  .agent/handoff.md
  scripts/self_use_queue.json


## C3 — how the run is isolated

THE RUN MUST NOT BE ABLE TO DIRTY THE PRIMARY CHECKOUT, because `git status --porcelain` must be
empty at every commit boundary and this job's whole subject is editing a file in this repository.
Three separate paths keep that true and they are not interchangeable:

  queue_path  the TRACKED `scripts/self_use_queue.json` in the primary checkout — this is the file
              C3 commits, and the run must consume the entry C3 appended to it
  dest_dir    a directory under the gitignored `.remedy-wt/` — the planned job file and the
              persisted `JobPlan` land here, not in the repository
  repo_path   a DISPOSABLE `git worktree` at this round's base, created on a throwaway branch
              (`git worktree add -b tmp/f274-r19-selfuse <path> ae7607e6`), because the
              self-dogfood branch guard refuses a detached head by design

Remove and prune that worktree afterwards and delete the throwaway branch. There are 14 worktrees
registered before you start; leave that number as you found it. Copy the evidence into
`.agent/selfuse_f274/` only AFTER the run has exited.


## C3 — the evidence directory

Write these under `.agent/selfuse_f274/`, all with `.txt` names and never `.log` (R-0169:
`.gitignore` drops `*.log` silently and the review-zip guard rejects any member matching `\.log$`).
Their CONTENT is measured, not authored.

  entry_and_job_file.txt   the appended queue entry's id, title, provenance and `consumed_by`, and
                           the path `plan_next_self_use_item` rendered the job file to
  result_state.txt         the `JobPlan`'s `job_id`, `state` and per-task `task_id`/`status`
  execution_config.txt     the `JobPlan`'s `execution_config` verbatim, plus a line reading
                           `FAKE_APPEARS_IN_EXECUTION_CONFIG: <True|False>`
  timing.txt               the wall clock and the `JobPlan`'s `budgets`
  run_defects.txt          the `describe_self_use_run_defects(result)` tuple: its LENGTH, then each
                           string on its own line, VERBATIM and never reworded or truncated; if the
                           tuple is empty the file says so in those words
  jobplan.txt              the persisted `JobPlan` as JSON, or the reader output that renders it
  full_transcript.txt      the run's own stdout and stderr, written after the run exited


## Constraints

1. Apply every slice BYTE FOR BYTE. Do not reflow, retype or re-indent one. If something looks
   wrong, apply it as given and DECLARE the doubt in the handback.
2. RECORD19 is an APPEND: the target's existing bytes are a byte-exact PREFIX of the result and the
   slice is an exact SUFFIX of it. It carries its OWN leading newline — ADD NO SEPARATOR of your
   own, and do not strip one. PLAN19 REPLACES `.agent/plan.md` entirely and has no leading newline.
   FORTSCHRITT is appended to no file.
3. Extract each slice from the COMMITTED `.agent/authored/f274-r19.md` by its BEGIN and END marker
   lines and apply it with a script. Do not retype a slice by hand into a target.
4. CALL THE SHIPPED FUNCTIONS. Do not hand-edit `scripts/self_use_queue.json` and do not
   reimplement any part of the generator, the planner or the runner. The whole point of this
   precondition is that Remedy's own code performs the step.
5. DO NOT APPLY THE JOB'S PROPOSED CHANGE. The run goes to the approval gate and stops there. A
   `JOB_BLOCKED` result is a legitimate outcome to record, not a failure to repair, and this round
   repairs nothing either way.
6. DO NOT SET `consumed_by`. It stays the empty string; the closure round sets it.
7. The whole change set of C0a through C3 is exactly the "Change set" paths other than
   `.agent/handoff.md`, which is C4's. `git status --porcelain` is empty at every commit boundary.
8. Every gate below runs at a commit STRICTLY EARLIER than C4, so the handback can quote each
   one's real result (§3 item 31). Take G2 at C1, G3 at C2, and G4 through G8 at C3.
9. Report each gate's REAL result, including a failure. A gate that fails is a handback that says
   so; it is never a gate quietly re-scoped until it passes. If the run errors, the error IS the
   result and it goes in `run_defects.txt` and the handback verbatim.


## The slices

BEGIN PLAN19 sha256=59178fc0eae86485deb54ad37d958295473431ba38115e13725aa05790a667ef bytes=2504
# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Close F274 at the edge work it actually built and carry the cluster deletion, the atomic record
flip and the classic runner to F275, per DECISION F274 D8. F275 is registered and the
integration gate has PASSED; what remains is the self-use precondition and the closure itself.

## Current Step

The self-use round closure precondition 6 requires. Every queue item is consumed, so
`generate_and_append_if_empty` runs FIRST and appends the tier-1 item; that item is then planned
and RUN through `run_next_self_use_item` to the normal approval gate under a real provider, never
applied, with its `consumed_by` left EMPTY for the closure commit to set. The run's evidence and
whatever `describe_self_use_run_defects` returns are recorded verbatim. It also books round 18's
PASS verdict and the two R-0819 recurrences that round's gates earned.

## Next Steps

1. Register, as normal R-id findings, every string `describe_self_use_run_defects` returned for
   the self-use run — or record that it returned the empty tuple, which means nothing to register
   rather than nothing checked. This is the first commit of the closure round.
2. The ledger rotation by `scripts/rotate_live_review.py`, as its own commit, after the verdict
   bookings and before the STATUS flip.
3. The evidence job and the fresh review zip. The zip's `base_commit` is the FORK POINT
   `13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, whose ancestry-path and plain `rev-list` counts are
   EQUAL — never `git merge-base`, which names `origin/main`'s tip here and gives unequal counts.
4. The closure commit: the STATUS `[x]` flip, the README sync and the one `consumed_by` edit in
   ONE commit; then the pull request, which is NOT merged this session.

## Risks

- The map was blind twice and is fixed once: R-0834's file-type blindness is closed, R-0832's
  event-name coupling is OPEN. Treat every "zero edges" reading as a claim about the WALKER.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12.
- The self-use run needs a REAL provider: `run_next_self_use_item` refuses to run unflagged when
  role config resolves to `fake`. Role config resolves `builder` and `reviewer` to `ollama`.
END PLAN19

BEGIN RECORD19 sha256=791acec71bdf836830e6541688dbee9331aab8b3b57e9d8880361780bb3bcc3e bytes=10339

Gate: F274 R18 — the F274 round 18 entry, THE INTEGRATION-GATE ROUND, and this is the only place in this record that may carry a full-suite claim for F274. VERDICT PASS, AND THE INTEGRATION GATE ITSELF PASSES; every gate was re-run by the reviewer, and BOTH SUITE HALVES were re-run independently by it rather than read from the handback, which is the counter-measure open finding R-0645 asks for and the reason this entry can distinguish a flake from a regression at all. Range `4f3f0b8f`..`ae7607e6`, seven commits, every one single-parent, in the ordered sequence C0a, C0b, C1, C2, C3, C4, C5. THE ROUND MEASURED AND DID NOT REPAIR: the whole range names sixteen paths and every one begins `.agent/`, no test was deleted, no assertion weakened and no ceiling raised. G1 TRANSPORT covers the chain this workflow can walk per §3 item 37 and not the emitted bytes: the reviewer's scratch original `.remedy-wt/f274-r18-FINAL.md` and both committed copies are all 27125 bytes at `0dc373000fc32fee8f211b806b759cf51dd4bdf2cf72332f577c24913e06e810`. G2 THE PLAN at `79779c5c`: byte-equal to its slice at 2416 bytes and 42 lines against the cap of 50. G3 THE TWO PROSE APPENDS: `.agent/live_review.md` 622238 to 628109 at `487cd679` and `.agent/prose_slips.md` 163910 to 164868 at `40e4e35a`, each an exact append with N counted as 1, ordered equality true and the control on the FIRST appended paragraph rejected by BOTH readers; units 242 to 243, `^Gate: ` 48 to 49, `^Gate: F274 R17 ` 0 to 1, registrations 70 to 70, distinct resolutions 7 to 7, OPEN SET 63 TO 63 BY DISTINCT ID. G4 THE BRANCH RUN, step 1 of docs/agents/integration_gate.md, in the primary checkout at `40e4e35a`: EXIT 1, `2 failed, 19765 passed, 23 skipped, 1 warning in 173.93s`. G5 THE BASE RUN, step 2, in a throwaway worktree on a throwaway branch at the GATE BASE `d0d8b24da2a080ebcff85e63e73a547e6a8066e6` — which is `git merge-base HEAD origin/main` and therefore `origin/main`'s own tip, this branch having merged main IN at `f85200e4`, and which is DELIBERATELY NOT the fork point the closure package must use: EXIT 0, `19790 passed, 23 skipped, 1 warning in 146.79s`, FAILED 0. R-0736's FIX CLAUSE WAS ORDERED AND IT WORKED, which is the first time this repository has run the gate without paying that finding's cost: parity was restored with `shutil.copytree(src, dst, symlinks=True)` — 43005 files and 27 preserved symlinks against the primary's 27 — and the copied `apps/ui/dist` was then STAMPED strictly newer than the newest file under `apps/ui/src`, after which the string `React UI not built` occurs ZERO times in the base output against the 114 the literal recipe produces. NO FILE UNDER `apps/ui/dist` CHANGED ITS MTIME ACROSS THE RUN, which is the R-0444 event reading and the one that carries the parity claim. G6 THE COMPARISON, step 3: the BASE-ONLY set is EMPTY, so no id needs environment attribution; the BRANCH-ONLY set is NOT empty and holds two ids, both in `tests/orchestration/test_product_smoke.py` and both traced by the worker to ONE leaked child holding port 5273 on xdist worker gw6. STEP 4 ATTRIBUTION CLASSIFIES BOTH AS THE xdist-FLAKE CLASS AND THEREFORE AS RECORDED, NOT BLOCKING, and the evidence is now much wider than one actor's re-runs. The worker re-ran each id serially three times on the branch and once at the base, eight of eight green. THE REVIEWER'S OWN THREE FULL-SUITE SAMPLES OF THIS BRANCH DISAGREE WITH EACH OTHER, WHICH IS THE POINT: at `4f3f0b8f` it measured EXIT 0 with 19767 passed and ZERO failures, at `ae7607e6` it measured EXIT 1 with 19766 passed and ONE failure, and that one failure is a THIRD id, `tests/ui_server/test_command_channel.py::TestCommandChannelDoor::test_non_object_args_is_400_on_field_args`, which the worker's run passed. The reviewer re-ran that id alone — 1 passed — its whole file serially — 106 passed — and its whole directory UNDER xdist — 506 passed. ALL THREE IDS ACROSS ALL THREE RED SAMPLES START A REAL SERVER ON A REAL PORT, so the shared mechanism is a port-binding race under parallel execution and not a property of any commit: three full-suite samples of the SAME code produced three DIFFERENT failure sets, which is exactly what R-0645 records about this command. COUPLING WAS CHECKED RATHER THAN ASSUMED: `git diff --name-status d0d8b24d..ae7607e6` leaves `tests/orchestration/test_product_smoke.py` and `tests/ui_server/test_command_channel.py` UNTOUCHED by this branch. `packages/orchestration/ui_server.py` IS modified by it, so the third id was not dismissed on the file-untouched argument alone; it was re-run deterministically in isolation, in its file and in its directory under xdist, and passed every time. G7 AND G8 THE TREE AND THE NUMBERS: porcelain empty, `git ls-files .remedy-wt` empty, worktrees 14 at both ends with the temporary base branch deleted, per-commit insertions 304, 217, 16, 2, 2 and 178 for C0a through C4, every one under the DECISION F104 D1 cap of 500, eleven evidence files under `.agent/gate_f274_r18/` and NOT ONE with a `.log` extension, and the unquoted `\bHEAD\b` count ZERO in both record-bound slices. TEN DEVIATIONS WERE DECLARED AND THE REVIEWER SUSTAINS ALL TEN; TWO OF THEM ARE THE REVIEWER'S OWN GATE DEFECTS AND ARE BOOKED AS THE TWO R-0819 RECURRENCES BELOW. The remaining eight are sustained without further comment: reading G4's own "at C3" over constraint 7's "at C4", which is the only physically possible order since C4 commits the run's output; the branch half going red and NOT being repaired, which is what constraint 4 required; the branch-only set being non-empty against this block's reference of empty; the PASSED difference reading 25 rather than 23, both figures reported and reconciled by the two flakes; three evidence files beyond the eight named, all inside the declared directory and one of them named by G6 itself; `.agent/plan.md` being one round stale at the C0a and C0b boundaries, the case §3 item 23 permits; the scratch living under the gitignored `.remedy-wt/` with both runs' output buffered through the pipe and written only after exit, as R-0176 requires; and the worker's observation, volunteered rather than ordered, that the editable install did NOT shadow the base worktree because the base run's warnings summary names the worktree's own `model_routing.py`. NO FINDING IS REGISTERED BY THIS GATE AND NO NEW ID IS MINTED, so the open set stands at 63 by distinct id and the next free id is R-0837.

RECURRENCE of R-0819 at F274 round 18, the first of two this round, measured by the reviewer at `ae7607e6`. NO NEW ID IS SPENT: §3 item 30 requires the open set searched for the DEFECT before an id is minted, and R-0819 is OPEN and holds this class — a gate ordering a value no correct run can produce. THE INSTANCE. The round 18 block's gate G5(e) ordered that "ANY mtime falling inside the run window VOIDS the parity claim and forces per-id attribution", while gate G5(b) of the SAME BLOCK ordered the copied `apps/ui/dist` stamped to an mtime STRICTLY GREATER than the newest file under `apps/ui/src` — and `git worktree add` stamps those sources at checkout time, seconds before the run. The forward stamp therefore lands after the window opens whenever the worktree is fresh, which is always, so G5(e) fires on a tree where nothing was written and the two clauses cannot both be satisfied by any correct run. THE CAUSE IS NEW AND IS WHAT THIS RECURRENCE ADDS: it is not a wrong range and not a wrong value, but TWO CLAUSES OF ONE GATE ORDERED AGAINST EACH OTHER, one establishing a precondition whose own side effect trips the other's alarm. THE ADDITION TO R-0819's FIX, binding on every later block of this feature and of F275: where a gate ORDERS a state to be established and then MEASURES that state, the measurement names the EVENT and never the VALUE — "did this file's mtime CHANGE across the run", never "does this file's mtime fall inside the window" — because the value is exactly what the establishing clause just set. THE ROUND LOST NOTHING: the worker measured the event reading as well, reported FILES_WITH_CHANGED_MTIME as 0 beside FILES_WITH_MTIME_INSIDE_RUN_WINDOW as 4, proved the stamp was on disk 17.38 seconds before the window opened by pointing at its own setup record's timestamp, and declared the contradiction rather than resolving it silently. The reviewer sustains that reading: nothing wrote to `apps/ui/dist` during the base run, the parity claim holds, and the clause that fired is vacuous here because the base failure set is empty.

RECURRENCE of R-0819 at F274 round 18, the second of two this round, measured by the reviewer at `ae7607e6`. NO NEW ID IS SPENT, for the reason the paragraph above gives. THE INSTANCE. The round 18 block's gate G6 ordered the branch's lower passed-count explained by naming "at least three deleted test files" from `git diff --name-status d0d8b24d..<C4> -- tests/`, and THAT COMMAND RETURNS ZERO LINES BEGINNING `D`: F274 deleted no test FILE at all, against either candidate base, and the reviewer re-measured it at both — `d0d8b24d..ae7607e6` and `13dfaabd..ae7607e6` each give a D count of 0. The count really did fall, by the 23 tests a collect-only differencing measures, but it fell because tests were REMOVED FROM SURVIVING FILES and because deleting the `feature` command group cost `tests/test_grouped_cli.py` eight `[feature]` parameter ids from a file that is byte-identical in both trees. THE CAUSE IS THE ONE §3 item 34 EXISTS FOR AND IT IS NOT THE CAUSE THE FIRST RECURRENCE NAMES: the reviewer ordered EVIDENCE OF A SHAPE IT HAD NEVER MEASURED, having checked which source files this branch deleted and never which test files, and then asserted the test-count delta had the same shape. THE ADDITION TO R-0819's FIX, binding forward: a gate that orders the worker to NAME INSTANCES of a category — deleted files, renamed symbols, changed rows — is run by the reviewer FIRST and the instances counted, because a gate demanding three of something there are none of is unmeetable in exactly the way a gate demanding a wrong number is, and it is harder to see because the number is not written down. THE ROUND LOST NOTHING: the worker measured the D count as 0, said so, substituted a direct measurement that actually explains the delta, and declared the substitution.
END RECORD19

BEGIN FORTSCHRITT sha256=2580b1c8439b6887e27a3d6c3bfa70ede6285cdb9e628ad19e88614828a92038 bytes=248
Fortschritt: F274 schließt bei ~35 % des ursprünglichen Umfangs, Integrationsgate BESTANDEN, F275 registriert (Löschkarte ✅ · Reachability-Ratsche ✅ · D1–D8 ✅ · F275 ✅ · Gate ✅ · Self-Use läuft · Closure offen) — Schätzung
END FORTSCHRITT


## Done when

G1  TRANSPORT, one digest comparison, at C3. `.agent/authored/f274-r19.md` and
    `.agent/last_block.md` are BYTE-IDENTICAL to each other and to the reviewer's scratch original
    at `/home/decodeux/Repos/remedy/.remedy-wt/f274-r19-FINAL.md`. Report the sha256 and byte count
    of all three. This proof covers the chain this workflow can walk and claims nothing about the
    bytes that reached you (§3 item 37).

G2  THE PLAN, at C1. `.agent/plan.md` is byte-identical to the PLAN19 slice; report its sha256,
    byte count and line count, and that it carries exactly one `## Goal` and one `## Next Steps`.
    Reference: 2504 bytes, 42 lines, both headings once, against the AGENTS.md cap of 50 lines.

G3  THE RECORD APPEND, at C2. Report from the file itself: byte count before and after; that the
    post-image equals the pre-image concatenated with the slice EXACTLY; N, the number of
    blank-line paragraphs in the slice, COUNTED by your script and not taken from this block; that
    the last N blank-line units of the whole file equal the slice's N paragraphs IN ORDER; and that
    a control flipping one byte inside the FIRST appended paragraph, at byte offset 628110, is
    REJECTED by both the byte reader and the ordered-unit reader. Then report before and after:
    blank-line units; `^Gate: `; `^Gate: F274 R18 `; lines beginning
    `RECURRENCE of R-0819 at F274 round 18`; distinct `^- R-\d+ — `; distinct `^Done: R-\d+ — `;
    and the open set as the first minus the second. Reference: 628109 to 638448 bytes, N is 3,
    units 243 to 246, `^Gate: ` 49 to 50, `^Gate: F274 R18 ` 0 to 1, the recurrence line count 0
    to 2, registrations 70 to 70, distinct resolutions 7 to 7, OPEN SET 63 TO 63 BY DISTINCT ID.

G4  THE GENERATION, at C3, performed by calling
    `packages.orchestration.self_use_generator.generate_and_append_if_empty` against the TRACKED
    queue file. Report, from the committed file and through the shipped loader
    `packages.orchestration.self_use_queue`, never by reading the JSON by hand:
    (a) `pending_self_use_items()` and `next_self_use_item()` BEFORE the call. Reference: 0 and
        `None`.
    (b) the returned entry's `id`, `title`, `provenance` and `consumed_by`. Reference: `SU-013`,
        `Address ledger finding R-0445`,
        `generated (self-use-generator tier 1, ledger scan, R-0445)`, and the EMPTY STRING.
    (c) the queue file's byte count and item count before and after. Reference: 38745 to 43764
        bytes, 12 to 13 items.
    (d) `pending_self_use_items()` and `next_self_use_item()` AFTER, and the full list of entry ids
        whose `consumed_by` is blank. Reference: 1, `SU-013`, and the list holding `SU-013` alone —
        which is what leaves exactly one item for the closure commit to consume.

G5  THE RUN, at C3, performed by calling
    `packages.orchestration.self_use_runner.run_next_self_use_item` with the three paths the "how
    the run is isolated" section separates. Report, and MATCH NOTHING — every number here is
    whatever the run really produced:
    (a) the exact call, including `dest_dir`, `repo_path`, `queue_path` and every budget keyword.
    (b) the returned `JobPlan`'s `job_id` and `state`, and each task's `task_id` and `status`.
    (c) the `execution_config` verbatim, and whether the literal string `fake` appears anywhere in
        it. IT MUST NOT: the whole precondition is that Remedy's real provider ran. If it does,
        that is a gate FAILURE — report it and stop rather than re-running until it does not.
    (d) the wall clock and the `JobPlan`'s `budgets`.
    (e) `describe_self_use_run_defects(result)` — its tuple LENGTH and every string VERBATIM. Do
        not summarise, truncate or reword one; that module exists to quote the job's own words.
    (f) that NOTHING WAS APPLIED: `git status --porcelain` in the PRIMARY checkout names only the
        paths of this round's own change set at the moment of the C3 commit and nothing the job
        proposed, and the disposable worktree was removed and pruned.

G6  THE EVIDENCE DIRECTORY, at C3. Report the file list committed under `.agent/selfuse_f274/`,
    that every one ends `.txt` and none ends `.log`, and that `run_defects.txt` holds the same
    tuple length G5(e) reports. A directory whose `run_defects.txt` disagrees with the handback is
    the defect this gate exists to catch.

G7  THE SCOPE GUARD AND THE PER-COMMIT NUMBERS, at C3. `git diff --name-only ae7607e6..<C3>` names
    ONLY paths beginning `.agent/` or the single path `scripts/self_use_queue.json` — the
    base-anchored range is the correct reading because the claim is about the WHOLE round's change
    set — and names NONE beginning `packages/`, `apps/`, `tests/` or `docs/`. Report the full list.
    Then, for C0a, C0b, C1, C2 and C3 and NOT for C4, report the insertion count from
    `git diff --numstat <parent>..<commit>` and confirm each is under the DECISION F104 D1 cap of
    500. The `## Commits` table of `.agent/handoff.md` carries these same values and its `+/-`
    cells are the numstat columns cell for cell (§3 item 28); state that you compared the two.

G8  THE TREE AND THE RECORD-SLICE SCAN, at C3. `git status --porcelain` is EMPTY; `git ls-files
    .remedy-wt` is EMPTY; report `git worktree list` and confirm it is back to 14 with the
    throwaway branch deleted. Then, for the RECORD19 slice as committed in
    `.agent/authored/f274-r19.md`: delete every backtick-quoted span and report the count of
    `\bHEAD\b` in what remains. Reference: ZERO (R-0586).


## Handback

Rewrite `.agent/handoff.md` per AGENTS.md and docs/agents/handback_template.md. It has no length
cap (amend0827 rule 3); it is valid when its mandated sections are present. It must carry:

- the state block, naming the feature, the round, THE SESSION NUMBER — session 7 of feature F274 —
  the branch, and the commit SHAs;
- the Fortschritt line, verbatim from the FORTSCHRITT slice above;
- the changed-files table and the `## Commits` table whose `+/-` cells G7 pins;
- ONE LINE PER GATE, G1 through G8, each carrying that gate's REAL measured result;
- THE DEFECT STRINGS, verbatim and in full, under their own heading, with their tuple length — or
  the sentence that the tuple was EMPTY, which means nothing to register rather than nothing
  checked. This is the material the closure round registers, so it may not be summarised here;
- the open-findings count, 63 by distinct id, with the arithmetic that produced it;
- every deviation, declared with its reason;
- the item-status table AGENTS.md requires, with every ordered item appearing exactly once;
- the next expected action: the closure round — register the defect strings if any, rotate the
  ledger, build the evidence job and the review zip, flip STATUS and open the pull request.

Then push the branch. Do not create a pull request; the closure round creates it.
