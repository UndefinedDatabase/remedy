# STEP T001/1 — F274 round 1 — claim the feature, book F272's last verdict, measure the flip and rule its route

Goal: claim F274 in the roadmap ledger, cut its branch, re-point the two state files, re-head
the review record and book F272's round 31 verdict into it, then land T001 in full — run the
DECISION F272 D7 raising-property probe over `Job.id`, commit the measured site set, and
record the route as DECISION F274 D1. NO PRODUCTION LINE MOVES IN THIS ROUND.

Base: `main` at `13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, the merge commit of pull request
244. Every base measurement below was taken by the reviewer at that commit.

## Conventions

This block carries authored TEXTS and authored PAIRS. A whole text appears between a line
beginning `<<<BEGIN <NAME> ` and a line reading exactly `<<<END <NAME>>>`, and is read
INCLUSIVE of the newline that ends its last content line. A pair is two such texts named
`<NAME>_FROM` and `<NAME>_TO`, and each half is read with that final newline STRIPPED. Extract
every text programmatically by matching those two marker lines; never retype one. The named
units in this block are PLANF274R1, CONTEXTF274R1, REHEADTO, RECORDR31, STATUSPAIR_FROM,
STATUSPAIR_TO and D1SLICE. No line of this block is a run of a repeated character.

## Bundle

C0a  save this block to `.agent/authored/f274-r1.md` by `shutil.copyfile`
C0b  mirror the same file to `.agent/last_block.md` by `shutil.copyfile`
C1   `.agent/plan.md` = PLANF274R1 and `.agent/context.md` = CONTEXTF274R1
C2   `.agent/live_review.md` re-head: replace the region before `## Findings` with REHEADTO
C3   `.agent/live_review.md` append RECORDR31
C4   `docs/roadmap/STATUS.md` apply STATUSPAIR
C5   `.agent/f274_id_probe_inventory.md` — the probe measurement, written by you
C6   `.agent/decisions.md` append D1SLICE
C7   `.agent/handoff.md` full rewrite

## Change set

Exactly these paths, and nothing else: `.agent/authored/f274-r1.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/context.md`, `.agent/live_review.md`, `docs/roadmap/STATUS.md`,
`.agent/f274_id_probe_inventory.md`, `.agent/decisions.md`, `.agent/handoff.md`.

## Constraints

1. Apply every slice VERBATIM. If you believe one is wrong, apply it as written and declare
   the disagreement in the handback; never silently repair an authored text.
2. Cut the branch `feature/f274-one-world-completion-part-two` from `main` at the base SHA
   above BEFORE C0a. Never work on `main`. Never force-push.
3. The commit order is C0a, C0b, C1, C2, C3, C4, C5, C6, C7 and is not varied. C1 is the first
   substantive commit because this round touches the finding ledger and
   `docs/agents/planner_reviewer_prompt.md` §3 item 23 requires the plan to advance first.
4. Read `.agent/STOP` with `os.path.exists` before C0a, before C5 and before C7, and report all
   three readings. If it exists, finish the half-written commit, write the handback and stop.
5. The probe of C5 is DESTRUCTIVE verification and runs ONLY inside a disposable
   `git worktree`, never in the primary checkout, which satisfies `git status --porcelain`
   empty at every commit boundary. Remove and prune that worktree before C6, and report
   `git worktree list` counts at the start and the end of the round.
6. Scratch files go under the gitignored `.remedy-wt/` and are removed BY EXACT PATH, never by
   a glob. `.remedy-wt/f274-r1-block.md` is KEPT: it is the first link of the transport chain.
7. Do not mint a finding id this round. The next free id is R-0829 and it stays free. Do not
   write a `Done:` paragraph: only the reviewer's authored text resolves a finding.
8. The base measurements this block asserts are to be CONFIRMED on disk before use, and any
   divergence declared rather than absorbed: `.agent/live_review.md` 493225 bytes / 537 lines,
   sha256 `9b104c3cb3fbd36b9aaf4cb1d4340f9812b768bda128805cc5c08aaf71201438`;
   `.agent/decisions.md` 872485 bytes / 10897 lines, sha256
   `6db4150fe9437cc702fcbd1199be58a5342e80678183f05944f14ba6a5e73993`; `.agent/plan.md` 1838
   bytes; `.agent/context.md` 3366 bytes; `docs/roadmap/STATUS.md` 40038 bytes.

## The probe of C5 — a SPEC, not a slice

The probe is throwaway scratch, so it is described rather than shipped as an authored text.
Build it to this specification and report what you built.

In a disposable worktree at the base SHA:

- In `packages/core/models.py`, rename the `Job` field `id` to `job_id`, leaving its
  `Field(default_factory=uuid4)` default untouched.
- In its place put a `property` named `id` that records its CALLER and then returns
  `self.job_id`. It must RETURN the real value, not raise: a returning probe keeps the suite
  green, so ONE pass yields the whole runtime site set instead of a raise-per-run fixpoint.
- The caller is `sys._getframe(2)` from inside the recording helper — frame 0 is the helper,
  frame 1 is the property, frame 2 is the real reader — recorded as `f_code.co_filename` and
  `f_lineno` into a process-local set, flushed by `atexit` to one file per PID under a scratch
  directory. One file per PID is required because the run is distributed by `pytest-xdist`.
- Do NOT raise `AttributeError` anywhere in this probe. `hasattr()` and
  `getattr(x, "id", default)` swallow it, so an `AttributeError` probe silently UNDER-COUNTS
  the site set, which is the one error this measurement exists to avoid.

Run, in this order, and report each with its real exit code and its `N failed, N passed` tail:

- (a) the UNMUTATED CONTROL, before any edit: `python3 -B -m pytest tests/ -q -p no:randomly
  -n auto`. A colour with no baseline is not evidence. The reviewer measured this control at
  the base SHA as 13 failed and 19737 passed, every failure in the known environment class —
  `tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`
  plus `tests/ui_server/` ids — because a fresh worktree has neither `apps/ui/node_modules` nor
  a built `apps/ui/dist`. Report your control's failures and state whether each is in that
  class; a control failure OUTSIDE it stops the round under G8.
- (b) the same command with the probe installed, then aggregate every per-PID file into one
  set of distinct `file:line` sites.

Then write `.agent/f274_id_probe_inventory.md` carrying, all from YOUR run: the total distinct
sites; the split into production (`packages/`, `apps/`, `scripts/`) and test (`tests/`) with a
distinct-FILE count for each; the per-file site counts for every production file, sorted by
path; the control and probe exit codes and tails; and one paragraph naming the probe's known
limit — it observes only sites the suite EXECUTES, so it is a lower bound on production reads,
where DECISION F272 D15's `ast` sweep was an upper bound, and the honest site set is bracketed
by the two rather than given by either. Name the commit the measurement was taken at.

## The persisted-key demonstration, also in C5

The rename exposes a hazard beyond attribute reads, and the inventory records it as a
reproduced measurement rather than as a claim. In the same worktree, with the field renamed,
run `python3 -B -m pytest tests/test_storage.py::test_backward_compat_job_without_project_id -q
-p no:randomly` and record its real output. The reviewer measured it as EXIT 1, failing at
`assert loaded.id == job_id` with two DIFFERENT UUIDs: the stored JSON carries the key `"id"`,
so a renamed field no longer matches it and pydantic mints a FRESH id on load. The job loads
successfully carrying the wrong identity, which is silent corruption of stored state rather
than a red test. Record the reading and the reason; do NOT repair it — the ruling belongs to
T002's first round, and DECISION F272 D5 answered the same question for the `status` rename by
ruling that the stored key does not move.

## Done when

G1 TRANSPORT — ONE digest comparison. `.remedy-wt/f274-r1-block.md`, `.agent/authored/f274-r1.md`
and `.agent/last_block.md` are byte-identical and all three hash to the digest the delegation
states beside this block. Report the untruncated 64-character value; never retype a digest.
Per §3 item 37 this chain covers those three artefacts and claims nothing about emitted bytes.

G2 THE RE-HEAD (C2). In `.agent/live_review.md` the byte string `\n## Findings\n` occurs
EXACTLY ONCE before the edit and exactly once after it. Splitting the file at that single
occurrence, the TAIL — from `## Findings` to end of file — is 490724 bytes over 498 lines with
sha256 `d7ed620f9242c7929e0d8ae77070ef28b87c063578d8b03acd8cef88fac1cb03` BEFORE the edit, and
that digest is UNCHANGED after it. The HEAD before the edit is 2501 bytes over 39 lines; after
the edit the head is byte-equal to REHEADTO. Report all four readings. This is the whole proof
that the append-only findings region survived the re-head untouched.

G3 THE RECORD APPEND (C3), against its own pre-image, which is C2's post-image and not the
base. (a) BYTE: the pre-image is a byte-exact PREFIX of the post-image, and the post-image
equals the pre-image followed by the RECORDR31 slice, which CARRIES ITS OWN leading blank
line — do not add a separator newline of your own. (b) STRUCTURAL: an
independent reader compares the LAST N blank-line-separated units of the whole file against the
slice's N paragraphs IN ORDER, where N is COUNTED by your script from the slice and never taken
from this block. (c) NEGATIVE CONTROL, in memory only, flipping one byte inside the FIRST
appended paragraph: both readers must REJECT the flipped image and ACCEPT the real one, and the
file on disk must be unchanged by the control. (d) COUNTS: distinct `^- R-\d{4}` and distinct
`^Done: R-\d{4}` before and after, the open set by DISTINCT ID before and after, `^Gate: `
before and after, `^Gate: F272 R31` 0 before and 1 after, and `^- R-0829` 0 before and 0 after.

G4 THE TWO STATE FILES (C1). `.agent/plan.md` is BYTE-EQUAL to PLANF274R1, is under the
AGENTS.md cap of 50 lines, and carries `## Goal` and `## Next Steps`. `.agent/context.md` is
BYTE-EQUAL to CONTEXTF274R1 and satisfies all four of its readers at once: it contains the
substring `Steps`, a `## Active Branch` heading followed by a `feature/` slug, a roadmap F-id,
and the substring `pytest`. Report each of those four as its own boolean.

G5 THE CLAIM (C4). For STATUSPAIR: count FROM in `docs/roadmap/STATUS.md` before the edit — it
must be exactly 1 — and 0 after; count TO as 1 after; and show that the post-image is the
pre-image with that ONE replacement and nothing else. Re-classify the pair before use by
testing whether TO CONTAINS FROM and printing that boolean beside the label; it is a REWRITE
and therefore carries no append obligation. After the edit `^- \[~\] ` occurs exactly once in
the file and `^- \[~\] F274 ` exactly once.

G6 THE MEASUREMENT (C5) — the property, not a number this block dictates. The inventory exists,
names the commit it was measured at, and records the control and probe readings. The
load-bearing property is the one DECISION F274 D1 turns on: THE DISTINCT SITE COUNT EXCEEDS THE
DECISION F104 D1 CAP OF 500 INSERTIONS, and by a wide margin. Report your own total and the
boolean `sites > 500`. The reviewer's own probe at the base SHA observed 1978 distinct sites —
428 production across 80 files and 1545 test across 138 files — and your figure is expected to
be close but is NOT required to equal it; report yours and, if it diverges materially, say so.
Report the persisted-key demonstration's exit code and its two differing UUIDs.

G7 THE DECISION APPEND (C6). The pre-image of `.agent/decisions.md` is a byte-exact PREFIX of
the post-image and the post-image equals the pre-image followed by the D1SLICE slice, which
CARRIES ITS OWN leading blank line — do not add a separator newline of your own.
`^## DECISION F274 D` occurs 0 times before and exactly 1 time after, and
`^## DECISION F274 D1 ` heads exactly one section.

G8 THE GATES AND THE TREE, run SERIALLY in the primary checkout, each as its own command, with
its real exit code recorded and no pipe between the command and the exit reading:
`python3 -B -m pytest tests/docs/ -q -p no:randomly`;
`python3 -B -m pytest tests/orchestration/test_roadmap_index.py -q -p no:randomly`;
the four state readers as FOUR, not three — `python3 -B -m pytest tests/ui_server/ -q -p
no:randomly`, `python3 -B -m pytest tests/orchestration/test_test_runner.py -q -p no:randomly`,
`python3 -B -m pytest tests/regression/test_resource_safety.py -q -p no:randomly` and
`python3 -B -m pytest tests/orchestration/test_integrity_gate.py -q -p no:randomly`; and the
canary `python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly`. Also report
`git status --porcelain` immediately before each commit, `git ls-files .remedy-wt`, the
`git worktree list` count at the start and end of the round, and each commit's insertion count
from `git diff --numstat <parent> <commit>` against the cap of 500 — for every commit EXCEPT
C7, whose own numbers cannot exist while it is being written.

## Handback

Rewrite `.agent/handoff.md` in full per `docs/agents/handback_template.md`: feature and round,
`SESSION 1` of F274, branch, commit SHAs, the changed-files table, the REAL verification
results one line per gate, the open-findings count, the item-status table covering every C and
G item above exactly once, and the next expected action. It has no length cap. Then
`git push -u origin feature/f274-one-world-completion-part-two`. DO NOT create a pull request
and DO NOT merge anything this round.

<<<BEGIN PLANF274R1 whole-text
# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, the merge commit of pull request 244. F272 closed
at the scope DECISION F272 D16 fixed; this feature owns the remainder.

## Goal

Finish what F272 could not reach inside its own limit: the classic-to-unified record flip
DECISION F272 D15 measured as ATOMIC, and the prototype cluster deletion. T001 moves no
production line — it replaces D15's receiver-name BOUND with a measured site set and rules how
an atomic change lands under a per-commit cap that forbids it.

## Current Step

Round 1: claim F274 in the ledger, cut the branch, re-point this file and `.agent/context.md`,
re-head `.agent/live_review.md` and book F272's round 31 verdict into it, run the DECISION F272
D7 raising-property probe over `Job.id` in a disposable worktree, commit the measured site set
as `.agent/f274_id_probe_inventory.md`, and record the route as DECISION F274 D1.

## Next Steps

1. Rule the persisted-key question the probe exposed, before any consumer moves: `Job` stores
   its identity under the JSON key `"id"`, so renaming the field alone makes a stored job load
   with a FRESH id. DECISION F272 D5 answered the same question for `status` by ruling the
   stored key does not move.
2. T002 — the classic runner and the resolver collapse, on the route DECISION F274 D1 fixes.
3. T003 — the reachability test, the two carry-overs, DECISION F260 D3, then the cluster
   deletion, one commit per module group. NEVER SPLIT INSIDE T003.

## Risks

- The flip is atomic by construction and far over the DECISION F104 D1 cap of 500 insertions.
  D1 rules the route, and that ruling bounds every later commit's size.
- Five open High findings — R-0803, R-0804, R-0806, R-0807 and R-0827 — are F273's and not
  this feature's, per DECISION F272 D12.
<<<END PLANF274R1>>>

<<<BEGIN CONTEXTF274R1 whole-text
# Context — F274 One world completion, part two

## Active Branch
feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, the merge commit of pull request 244.

## Scope
F274 (Tier 2; depends on F259's binding vocabulary page, on the record F260 closed at, and on
the run re-key and unified record F272 closed at; blocks F261, F266, F268, F269, F270, F271
and F263): the remainder DECISION F272 D16 split off F272 at its operator-set soft limit. Task
slicing per `docs/roadmap/features/T2_F274.md`: T001 measure the flip and rule the cap, T002
the classic runner and the resolver collapse, T003 the reachability test and the prototype
cluster deletion.

## Do not touch
Everything `T2_F272.md`'s "Do not touch" section names, unchanged: the scope-fence builtin
deny list (F017), the approval gate, STATUS semantics. No command is RENAMED here — F261 owns
renames. No module outside F260's Design lists is deleted, and a module that turns out to be
reachable is reported with its import chain, never deleted.

## Assumptions
- Cleanliness before compatibility: no migration shim, no compatibility reader, no alias. A
  helper accepting both records is what AGENTS.md Scope Control forbids by name.
- F272's rulings stay binding here and are NOT restated; `docs/roadmap/features/T2_F272.md`
  keeps its DECISION sections unedited for exactly that purpose. D13, D14 parts 1 and 3, and
  D15 are this feature's starting conditions.
- NEVER SPLIT INSIDE T003. A session reaching its own limit splits between T002 and T003, and
  never within T003.

## Constraints
The bullets in this first group are STANDING project constraints, carried forward from the
context this file replaces.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree, never in the primary
  checkout, which satisfies `git status --porcelain` empty at every verdict.
- Bare `ruff` is DENIED to this session's shell; `python3 -m ruff check <path>` is the spelling
  every gate of this feature orders.
- `remedy` (the built CLI) is DENIED to this session's reviewer session-wide, subagents
  included; a round needing it delegates the run to the worker and reports the exact output.
- This session's shell guard refuses some command FORMS outright — shell loops, `$(...)`
  substitution, and `$?` inside a compound command — so checks of that shape are re-expressed
  in Python and the re-expression is reported.
- A fresh worktree has neither `apps/ui/node_modules` nor a built `apps/ui/dist`, so a full
  suite run there carries a known environment failure class that a control run must establish
  before any mutated run is read as evidence.

This feature is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`,
which AGENTS.md's "Completion Report — Item-Status Table" section requires of every completion
report. This file deliberately does not restate it.
<<<END CONTEXTF274R1>>>

<<<BEGIN REHEADTO whole-text
# Live Review — F274 One world completion, part two

> Round-by-round review record, re-headed at the F274 claim per
> docs/agents/planner_reviewer_prompt.md §1. The heading this replaces named F272, which is
> accepted: its STATUS line went `[x]` at `65c5ccd65c4d801b22ead89d3fb138eb54153828` and its
> pull request 244 merged at `13dfaabd93d7b6452a1d23ca698e29ed47ecf035`. Only the heading,
> this paragraph and the `## Steps` section below are rewritten. Every finding record below
> `## Findings` is carried forward BYTE-IDENTICAL — the block that ordered this re-head gates
> that region's sha256 equal before and after the edit, as its gate G2 — and finding ids
> continue the monotonic R-XXXX series across the re-head. Measured by the reviewer at
> `13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, the branch point: 62 DISTINCT ids matching
> `^- R-\d{4} — ` against 2 DISTINCT ids matching `^Done: R-\d{4} — `, so 60 findings are open
> BY DISTINCT ID, and the next id this feature mints is R-0829.
> F272's LAST round has an entry here, which is the exception rather than the rule: under
> docs/agents/self_drive_protocol.md there is no second window, so the reviewer books a
> branch-terminating verdict into the FIRST commit of the next feature's first round rather
> than losing it with the session. Records belonging to features already marked `[x]` in
> docs/roadmap/STATUS.md are not here at all: `scripts/rotate_live_review.py` moves them
> byte-verbatim into the append-only `.agent/live_review_archive.md` in every closure
> sequence, under operator amendment amend0905-throughput, and that archive is read on demand
> by id, never at session start.

## Steps

R1 claim F274 in the roadmap ledger, cut the branch, re-point `.agent/plan.md` and
`.agent/context.md`, re-head this record and book F272's round 31 verdict into it, and land
T001 — the DECISION F272 D7 raising-property probe over `Job.id`, the measured site set
committed as `.agent/f274_id_probe_inventory.md`, and the route recorded as DECISION F274 D1 →
the persisted-key ruling the probe exposed, before any consumer moves → T002, the classic
runner, `job.run --cycles`, `job.run-next`, their handlers and tests, and the resolver collapse
DECISION F260 D5 places in the same commit range → T003, the D11c reachability test run green
BEFORE deletion, the two carry-overs, DECISION F260 D3 drafted, then the prototype cluster
deletion one commit per module group, which is NEVER split → the integration gate → the closure
sequence.

<<<END REHEADTO>>>

<<<BEGIN RECORDR31 whole-text

Gate: F272 R31 — the F272 round 31 entry, and the last round of that branch. VERDICT PASS, BOOKED BY THE NEXT FEATURE'S FIRST ROUND BECAUSE A BRANCH TERMINATOR HAS NOWHERE ELSE TO LIVE. `docs/agents/planner_reviewer_prompt.md` §4 item 13 rules that the round which writes the record cannot record the gate on itself, so under the two-window relay a terminator's verdict lives only in `.agent/handoff.md`, the completion report and the pull request; under `docs/agents/self_drive_protocol.md` there is no second window and no round report survives the session, so §3 item 31's clause routes those numbers to the next gate, which is this one. Range `e388c603`..`65c5ccd65c4d801b22ead89d3fb138eb54153828`, seven commits, every one single-parent, in exactly the ordered sequence C0a, C0b, C1, C2, C3, C4, C5 the block declared. THE THREE VALUES THE HANDBACK COULD NOT CARRY, measured by the reviewer and recorded here as §3 item 31 requires: C5 is `65c5ccd65c4d801b22ead89d3fb138eb54153828`; its `.agent/handoff.md` row reads +1016/-893 by `git diff --numstat d2e9da48 65c5ccd6`; and the pull request is 244, which merged at `13dfaabd93d7b6452a1d23ca698e29ed47ecf035`. THE CLOSURE COMMIT'S PATH SET is exactly the four declared paths — `README.md`, `docs/roadmap/STATUS.md`, `scripts/self_use_queue.json` and `.agent/handoff.md` — confirmed by `git diff --name-only d2e9da48 65c5ccd6`, with no fifth path. EVERY GATE WAS RE-RUN BY THE REVIEWER IN THE PRIMARY CHECKOUT RATHER THAN READ FROM THE HANDBACK: `tests/docs/` EXIT 0 at 303 passed, `tests/orchestration/test_roadmap_index.py` and `tests/orchestration/test_self_use_queue.py` EXIT 0 at 53 passed together, which is the 30 and 23 the handback reports separately, and the canary `tests/cli/test_golden_path.py` EXIT 0 at 42 passed. THE LEDGER STATE: `^- \[x\] F272 ` occurs once, `^- \[~\] ` occurs ZERO times anywhere in `docs/roadmap/STATUS.md`, and the ledger holds 274 registered items of which 75 are `[x]` and 199 are `[ ]`. THE README PINS ARE NOT GATES THAT CANNOT FAIL, and the reviewer proved it rather than accepting the handback's report of the previous reviewer's proof: in a disposable worktree at `65c5ccd6` the unmutated control over both pin tests is EXIT 0 at 2 passed, setting the accepted count back to 74 turns `test_the_readme_accepted_count_equals_the_status_count` EXIT 1 at 1 failed, and setting the Tier 2 Done cell back to 17 turns `test_the_readme_tier_table_done_column_matches_the_ledger` EXIT 1 at 1 failed; the README was restored byte-identically and the worktree removed and pruned. Both tests live in `tests/docs/test_docs_consistency.py` in class `TestPrimaryDocsAreHonest`, and the control being EXIT 0 is what proves the node ids resolve — a mistyped id exits non-zero and would have faked the red. THE ACCEPTED-BLOCK TOKEN RULE HOLDS: bounding each block from its heading to the next heading, the five blocks carry 16, 13, 10, 6 and 13 distinct F-ids, every one of them `[x]` in the ledger, and the list of ids in an Accepted block that are NOT `[x]` is EMPTY. The reviewer's first pass flagged `F261`, which is a PROBE ARTEFACT and not a defect: an unbounded split let the Tier 5 block run to end of file and swallow the Quickstart comment `# generate a job plan (F261 renames the command)` at line 243, which is a legitimate forward reference outside every Accepted block. THE SELF-USE ITEM: SU-012's `consumed_by` reads `F272`, every other item is unchanged, `json.loads` succeeds, and through the SHIPPED reader `packages.orchestration.self_use_queue` the queue is EXHAUSTED — `pending_self_use_items()` is the empty tuple and `next_self_use_item()` is None over 12 items at schema_version 2 — so the next closure must call `generate_and_append_if_empty` before it can consume one. THE OPEN SET IS 60 BY DISTINCT ID, unchanged across the round: 62 distinct registrations against 2 distinct resolutions, R-0721 and R-0725, with the next free id R-0829 still free and unused. THE TREE was empty at every boundary and `git worktree list` reads 14 entries before and after. THE CLOSE IS `PASS_WITH_RISKS` AND ITS RISKS ARE NAMED RATHER THAN HIDDEN: five High findings — R-0803, R-0804, R-0806, R-0807 and R-0827 — remain open and are F273's by DECISION F272 D12, and `remedy integrity check` passes while its `high_blockers_open` check reports no open blocker or High findings, which is false with five open; that is the already-open R-0648, the pull request body states it, and this closure rests on the named list rather than on that check. NO NEW FINDING IS MINTED BY THIS GATE and none is resolved.
<<<END RECORDR31>>>

<<<BEGIN STATUSPAIR_FROM whole-text
- [ ] F274 — One world completion, part two — the atomic record flip and the cluster deletion
<<<END STATUSPAIR_FROM>>>

<<<BEGIN STATUSPAIR_TO whole-text
- [~] F274 — One world completion, part two — the atomic record flip and the cluster deletion
<<<END STATUSPAIR_TO>>>

<<<BEGIN D1SLICE whole-text

## DECISION F274 D1 — the atomic record flip lands as this feature's one declared-oversize commit, and the probe exposed a persisted-key question T001 did not anticipate (2026-09-07)

CONTEXT. DECISION F272 D15 measured the classic-to-unified flip as ATOMIC over the consumer
graph and bounded it with an `ast` receiver-name sweep at 468 `<job-ish>.id` reads in 74
production files and 1545 in 137 test files, recording in its own terms that this was an UPPER
BOUND from a heuristic and NOT a probe measurement, `.id` being polymorphic here exactly as
`.status` was. T001 of `docs/roadmap/features/T2_F274.md` ordered the DECISION F272 D7
raising-property probe to replace that bound with a measured site set BEFORE any route was
chosen, because a feature that starts flipping sites before the ruling lands repeats the
mistake DECISION F272 D14 part 2 made.

THE MEASUREMENT, taken at `13dfaabd93d7b6452a1d23ca698e29ed47ecf035` and recorded site by site
in `.agent/f274_id_probe_inventory.md`, which is the durable carrier and is not restated here.
The method departs from D7 in one deliberate way: D7 installs a RAISING property and iterates
to a fixpoint, one full suite run per round of sites; this probe installs a RECORDING property
that names its caller and returns the real value, so the suite stays green and ONE pass yields
the whole runtime site set. The reviewer's own run at that commit observed 1978 distinct
`file:line` reads of `Job.id` — 428 across 80 files under `packages/` and `apps/`, and 1545
across 138 files under `tests/`. The heuristic bound was wrong in BOTH directions, which is
the whole reason D7 exists: it over-counted production reads and it MISSED production files
the probe named.

CHOSEN. THE FLIP LANDS AS ONE COMMIT UNDER THE DECLARED-OVERSIZE EXCEPTION AGENTS.md's Commit
Discipline grants each feature exactly once. The measured set is multiples of the DECISION
F104 D1 cap of 500 insertions, and no sequence of smaller commits exists: D15 proved a
half-flipped tree is red at every intermediate boundary, and the only mechanism that would
make a per-caller sequence green is a helper accepting both records — the compatibility reader
AGENTS.md's Scope Control forbids by name, with no attic and no deprecated alias. The worker
declares that commit WITH its inseparability reason in the handback BEFORE review, as the
exception requires, and it is the ONLY oversize commit this feature may contain.

ALTERNATIVES CONSIDERED. One commit under the cap — refuted by measurement rather than by
estimate. A per-consumer sequence — rejected: red at every boundary, and green only via the
forbidden compatibility reader. An operator amendment raising the cap — rejected as
unnecessary and as harmful: AGENTS.md already grants exactly this exception, and spending an
amendment on a rule that already answers the question would weaken the cap for every later
feature.

CONSEQUENCE, AND THE QUESTION THIS PROBE EXPOSED. The flip is NOT only an attribute rename.
`Job` persists its identity under the JSON key `"id"`, so renaming the field alone makes
pydantic ignore that key and mint a FRESH id on load: with the field renamed,
`tests/test_storage.py::test_backward_compat_job_without_project_id` is EXIT 1, failing at
`assert loaded.id == job_id` with two different UUIDs, and the job loads SUCCESSFULLY while
carrying the wrong identity. That is silent corruption of stored state, not a red test, and it
is exactly the question DECISION F272 D5 had to answer for the `status` rename, which it
settled by ruling that the STORED KEY does not move. T002's first round rules the persisted
key for `id` before any consumer is touched, and `docs/roadmap/features/T2_F274.md` gains that
obligation in the same round; this ruling deliberately does not pre-empt it. REVERSE by
deleting this section; the measurement in `.agent/f274_id_probe_inventory.md` stands without
it, and D15 stands without both.
<<<END D1SLICE>>>
