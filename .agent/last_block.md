# STEP T003/1 — F274 round 2 — the D11c reachability ratchet, and the ruling the probe forced

Goal: land the import-reachability test operator amendment amend0905-vocab-rebuild requires and
F260's Design names as the proof that must be green before the prototype-cluster deletion; rule
its shape and T003's split boundary as DECISION F274 D1; register the finding the reviewer's own
dry run produced; and book round 1's PASS verdict and the reviewer's two round 1 slips, which
`.agent/STOP` deferred out of the previous session.

Base: `feature/f274-one-world-completion-part-two` at
`9c65a9225cdf4d60822d459d698b66d2d7cb19d7`. Stay on that branch; do not cut a new one, and do
not merge anything.

WHAT CHANGED UNDER THE PREVIOUS BLOCK. A block for round 2 exists on disk at
`.remedy-wt/f274-r2-block.md` and is SUPERSEDED by this one. Do not read it and do not apply it.
Operator amendment amend0907-cluster-first landed on `main` and merged into this branch at
`f85200e4`, and it does two things that void that block: DECISION amend0907-cluster-first D1
reorders this feature so that T003 runs FIRST, before T001 and T002, so the `Job.id` probe that
block ordered is no longer the next slice; and DECISION amend0907-cluster-first D2 takes the id
R-0829, which that block promised was free.

## Conventions

This block carries authored TEXTS. A whole text begins on a line whose PREFIX is
`<<<BEGIN <NAME> ` and ends on a line reading exactly `<<<END <NAME>>>`, and it is read
INCLUSIVE of the newline ending its last content line. Extract every text programmatically by
matching those two marker lines; never retype one and never hand-type a digest. The named units
in this block are PLANF274R2, HEADF274R2, RECORDR2, D1SLICE274 and SLIPS274R2. RECORDR2 and
SLIPS274R2 EACH CARRY THEIR OWN leading blank line — append each as-is and never add a separator
newline of your own. D1SLICE274 also carries its own leading blank line. PLANF274R2 and
HEADF274R2 are whole-region replacements and carry no leading blank line. No line of this block
is a run of a single repeated character.

## Bundle

C0a  save this block to `.agent/authored/f274-r2.md` by `shutil.copyfile`
C0b  mirror the same file to `.agent/last_block.md` by `shutil.copyfile`
C1   `.agent/plan.md` = PLANF274R2
C2   `.agent/live_review.md` HEAD region = HEADF274R2, findings region untouched
C3   `.agent/live_review.md` findings region append RECORDR2, head region untouched
C4   `.agent/decisions.md` append D1SLICE274
C5   the reachability test and its allowlist, written by you to the SPEC below
C6   `.agent/prose_slips.md` append SLIPS274R2
C7   `.agent/handoff.md` full rewrite

## Change set

Exactly these paths and nothing else: `.agent/authored/f274-r2.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `.agent/decisions.md`,
`tests/orchestration/test_import_reachability.py`,
`tests/orchestration/import_reachability_allowlist.txt`, `.agent/prose_slips.md`,
`.agent/handoff.md`. Nothing under `packages/`, `apps/`, `docs/` or `scripts/` is edited, and
NOTHING IS DELETED THIS ROUND.

## Constraints

1. Apply every slice VERBATIM. If you believe one is wrong, apply it as written and declare the
   disagreement in the handback; never silently repair an authored text.
2. The commit order is C0a, C0b, C1, C2, C3, C4, C5, C6, C7 and is not varied. C1 precedes every
   other substantive commit because this round registers a finding and §3 item 23 requires the
   plan to advance first.
3. Read `.agent/STOP` with `os.path.exists` before C0a, before C5 and before C7, and report all
   three readings. If it exists, finish the commit in hand, write the handback and stop.
4. `.agent/live_review.md` is split by the FIRST occurrence of the marker `\n## Findings\n`. The
   text BEFORE that marker is the HEAD region; the marker and everything after it is the FINDINGS
   region, which is append-only. C2 replaces the head and must leave the findings region byte
   identical. C3 appends to the findings region and must leave the head byte identical.
5. Do not mint a finding id of your own. This block mints exactly one, R-0830, inside RECORDR2.
   Do not write a `Done:` paragraph: only reviewer-authored text resolves a finding.
6. Scratch goes under the gitignored `.remedy-wt/` and is removed BY EXACT PATH, never by a glob.
   `.remedy-wt/f274-r2v2-block.md` is KEPT: it is the first link of the transport chain.
   `.remedy-wt/f274-r2-block.md` is the SUPERSEDED block and is also KEPT, untouched.
7. Base measurements to CONFIRM on disk before use, declaring any divergence. `.agent/plan.md`
   1909 bytes / 36 lines. `.agent/live_review.md` 504536 bytes / 545 lines, its HEAD region 3063
   bytes / 40 lines at sha256
   `77b1cd43268d4f21ab8fffeafed1df64c15972f7090bca271c09910fd97998f4`, its FINDINGS region 501473
   bytes / 505 lines at sha256
   `09f49be742173d4ae4b05fe71c465dc3fde583a71406b66ef977f148988565d5`. `.agent/decisions.md`
   878136 bytes / 10919 lines at sha256
   `b3aece0b92c2fdcd7f33753e5d6828fca9e144e3c661434418b22b12075b6cd5`. `.agent/prose_slips.md`
   154472 bytes / 573 lines at sha256
   `7a71913871e7e2baaa0f40fa927d69b897185d399e5ba8bb1682b1a76cad6ee5`.
8. Both files C5 creates are NEW. Neither path exists at the base; confirm that with
   `git ls-tree 9c65a9225cdf4d60822d459d698b66d2d7cb19d7 -- <path>` returning empty for each,
   and report both readings.
9. The repository is at a FROZEN ruff ceiling and DECISION F083 D5 forbids raising it. The
   reviewer measured `python3 -m ruff check .` at 26 errors at the base. C5 must leave that
   number unchanged. Bare `ruff` is denied to this session; the spelling is
   `python3 -m ruff check <path>`.
10. This round rewrites `.agent/` state, so the four state readers named in G7 are run AS FOUR,
    not as three.

## The reachability test of C5 — a SPEC, not a slice

Build both files to this specification and report what you built. Neither is dictated byte for
byte: the property is what is gated, not the wording.

- `tests/orchestration/test_import_reachability.py` computes the transitive FIRST-PARTY import
  closure of a pinned tuple of entry points and asserts that closure against an allowlist file.
- THE ENTRY POINTS are the six DECISION amend0905-vocab D11 (c) names — the golden path, the job
  path, the mission path, the self-use runner, the teacher and the cockpit read endpoints —
  resolved to these dotted modules and pinned in a module-level constant:
  `apps.cli.commands.do_cmd`, `apps.cli.commands.job`, `apps.cli.commands.mission_cmd`,
  `packages.orchestration.self_use_runner`, `apps.cli.commands.teach_cmd` and
  `packages.orchestration.ui_server`.
- THE CLOSURE IS COMPUTED STATICALLY, by parsing each module with `ast` and collecting every
  `Import` and `ImportFrom` naming a dotted path whose first segment is `packages` or `apps`.
  It does NOT import the modules: importing the cockpit would run module-level side effects. A
  `from X import y` contributes both `X` and `X.y`, and a name that resolves to no file on disk
  is dropped. Relative imports are skipped; this repository has none first-party.
  Imports inside `if TYPE_CHECKING` blocks and inside function bodies ARE followed, because for
  a test that guards a deletion an over-approximation is the safe direction: a module that might
  be imported must not be deleted.
- `tests/orchestration/import_reachability_allowlist.txt` holds one dotted module per line,
  sorted, and is GENERATED from the closure the test itself computes rather than typed. Blank
  lines and lines beginning with a hash are ignored by the reader.
- TEST FUNCTIONS, whose names you choose, asserting each of these properties:
  (a) every entry point resolves to a file on disk — without it a typo silently shrinks the
      measured set to nothing and the whole ratchet passes vacuously;
  (b) the closure MINUS the allowlist is empty, which is D11c's own sentence and the half a new
      orphan module reds;
  (c) every allowlist entry still resolves to a file on disk, which is the half a deletion round
      that forgets its allowlist entries reds.
  Each failure message names the offending modules, one per line.
- The module docstring states WHY the walk is static and WHY over-approximation is the safe
  direction, and names DECISION amend0905-vocab D11 (c) and this feature's T003 as what the test
  is for, per the repository's discoverability conventions.

The reviewer built this specification and ran it in a disposable worktree at
`9c65a9225cdf4d60822d459d698b66d2d7cb19d7` before emitting this block: the closure measured 319
modules out of 367 first-party modules on disk, the three functions passed, and both red controls
below went red. Your numbers are YOURS — report what you measure and do not reconcile toward
these. A materially different closure size is reported, not adjusted.

## Done when

G1 TRANSPORT — ONE digest comparison. `.remedy-wt/f274-r2v2-block.md`, `.agent/authored/f274-r2.md`
and `.agent/last_block.md` are byte-identical and all three hash to the digest the delegation
states beside this block. Report the untruncated 64-character value. Per §3 item 37 this chain
covers those three artefacts and claims nothing about the bytes that were emitted to you.

G2 THE RECORD HEAD (C2). The head region is byte-equal to HEADF274R2, and the findings region's
sha256 is `09f49be742173d4ae4b05fe71c465dc3fde583a71406b66ef977f148988565d5` both before and
after the commit. `\n## Findings\n` occurs exactly once before and after. Report the head's byte
and line counts before and after.

G3 THE RECORD APPEND (C3). (a) BYTE: the findings region's pre-image is a byte-exact PREFIX of
its post-image, and the post-image equals the pre-image followed by the RECORDR2 slice, which
carries its own leading blank line. The head region is byte-identical across this commit.
(b) STRUCTURAL: an independent reader compares the LAST N blank-line separated units of the whole
file against the slice's N paragraphs IN ORDER, where N is COUNTED by your script from the slice
and never taken from this block. (c) NEGATIVE CONTROL, in memory only, flipping one byte inside
the FIRST appended paragraph: both readers REJECT the flipped image and ACCEPT the real one, and
the file on disk is unchanged by the control. This file holds multi-byte UTF-8, so a CHARACTER
offset from `str.index` is NOT a byte offset: locate the flip by searching the ENCODED bytes at
or after the append point, or it lands outside the appended region and the structural reader
accepts it while looking exercised. The reviewer's own dry run made that mistake before
catching it. (d) COUNTS, before and after: distinct `^- R-\d{4}`,
distinct `^Done: R-\d{4}`, the open set BY DISTINCT ID, `^Gate: `, `^Gate: F274 R1` which is 0
before and 1 after, and `^- R-0830` which is 0 before and 1 after.

G4 THE DECISION APPEND (C4). The pre-image of `.agent/decisions.md` is a byte-exact PREFIX of the
post-image and the post-image equals the pre-image followed by the D1SLICE274 slice.
`^## DECISION F274 D` occurs 0 times before and exactly 1 time after, and `^## DECISION F274 D1 `
heads exactly one section.

G5 THE REACHABILITY TEST (C5) — the property, not bytes this block dictates. Run each as its own
command and record its real exit code.
  (a) GREEN: `python3 -B -m pytest tests/orchestration/test_import_reachability.py -q -p no:randomly`
      is EXIT 0. Report the passed count and the allowlist's line count.
  (b) RED CONTROL ONE, the orphan. In a disposable worktree at the C5 commit, append to
      `packages/orchestration/self_use_runner.py` a single import line reaching a module the
      allowlist does not hold, run the same command, and report that it is EXIT 1 naming the newly
      reachable modules. The reviewer's own dry run used `packages.orchestration.bench_run` and
      saw eight modules named. Then restore that ONE file by exact path and re-run to EXIT 0.
  (c) RED CONTROL TWO, the stale entry. In the same worktree append one line naming a module with
      no file on disk to the allowlist, run the same command, report EXIT 1 naming that module,
      then remove that ONE appended line by exact path and re-run to EXIT 0.
  (d) THE CEILING: `python3 -m ruff check .` in the primary checkout reports 26 errors, unchanged
      from the base, and `python3 -B -m pytest tests/orchestration/test_ci_budgets.py -q -p no:randomly`
      is EXIT 0.
  Remove the worktree by exact path and prune; report `git worktree list` counts at the start and
  end of the round.

G6 THE TWO PROSE FILES. `.agent/plan.md` is BYTE-EQUAL to PLANF274R2, is under the AGENTS.md cap
of 50 lines and carries `## Goal` and `## Next Steps`; report its line count. `.agent/prose_slips.md`
pre-image is a byte-exact PREFIX of its post-image and the post-image equals the pre-image
followed by the SLIPS274R2 slice; report byte and line counts before and after.

G7 THE SUITES AND THE TREE, run SERIALLY in the primary checkout, each as its own command with
its real exit code recorded and no pipe between the command and the exit reading: the four state
readers AS FOUR — `python3 -B -m pytest tests/ui_server/ -q -p no:randomly`,
`python3 -B -m pytest tests/orchestration/test_test_runner.py -q -p no:randomly`,
`python3 -B -m pytest tests/regression/test_resource_safety.py -q -p no:randomly` and
`python3 -B -m pytest tests/orchestration/test_integrity_gate.py -q -p no:randomly` — and the
canary `python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly`. Also report
`git status --porcelain` immediately before each commit, `git ls-files .remedy-wt`, and each
commit's insertion count from `git diff --numstat <parent> <commit>` against the cap of 500, for
every commit EXCEPT C7, whose own numbers cannot exist while its text is being written.

## Handback

Rewrite `.agent/handoff.md` in full per `docs/agents/handback_template.md`: feature and round,
`SESSION 2` of F274, branch, commit SHAs, the changed-files table with its `+/-` column taken from
`git diff --numstat` and compared cell by cell against the counts G7 orders, the REAL verification
results one line per gate, the open-findings count, the item-status table covering every C and G
item above exactly once, the one-sentence context self-assessment amend0905-throughput requires,
and the next expected action. It has no length cap. Then
`git push origin feature/f274-one-world-completion-part-two`. DO NOT create a pull request and DO
NOT merge anything.

<<<BEGIN PLANF274R2 whole-text
# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Finish what F272 could not reach inside its own limit: the prototype cluster deletion and the
classic-to-unified record flip DECISION F272 D15 measured as ATOMIC. DECISION
amend0907-cluster-first D1 reorders the slices so the deletion runs FIRST.

## Current Step

Round 2: land the D11c import-reachability test and its allowlist, rule the test's shape and
T003's split boundary as DECISION F274 D1, register R-0830 — the cluster is reachable from all
six D11c entry points, so F260's "already absent from the reachable set" precondition is
unmeetable as written — and book round 1's PASS verdict and the reviewer's two round 1 slips.

## Next Steps

1. The two carry-overs F260's Design names, done BEFORE the first `git rm`: overnight readiness
   and the overnight report become read-only `mission readiness` / `mission report`; every
   user-settable route-policy knob is checked against F110's config keys, existing knob deleted,
   missing knob registered as a finding and never rebuilt.
2. Draft DECISION F260 D3, the deletion paragraph, naming every module and the feature that
   inherited its idea. Nothing is deleted before it exists.
3. The cluster deletion itself, one commit per module group, NEVER SPLIT ACROSS SESSIONS: a
   session that cannot finish it does not start it.
4. T001 — measure the `Job.id` flip with a recording property and rule the cap route. The probe
   also has to rule the persisted key: `Job` stores its identity under the JSON key `"id"`, so
   renaming the field alone makes a stored job load with a FRESH id.
5. T002 — the classic runner and the resolver collapse.

## Risks

- The deletion is far larger than F260's Design lists: 33 production files import the cluster,
  and consumers outside the handler set must be cut before a module can go.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, and all of them are F273's
  rather than this feature's, per DECISION F272 D12. R-0827 was the fifth until operator
  amendment amend0907-cluster-first resolved it.
<<<END PLANF274R2>>>

<<<BEGIN HEADF274R2 whole-region
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
> BY DISTINCT ID. THOSE THREE NUMERALS ARE THE BRANCH POINT'S AND ARE LEFT AS MEASURED; the
> merge of `origin/main` at `d0d8b24d` moved two of them. Operator amendment
> amend0907-cluster-first resolved R-0827 and registered R-0829, so at that commit the record
> held 63 DISTINCT registered ids against 3 DISTINCT resolved ids — the open set is 60 either
> way, which is why only the components moved. THE NEXT ID THIS FEATURE MINTS IS R-0830, NOT
> the R-0829 this paragraph promised before the merge: that id is taken. See DECISION
> amend0907-cluster-first D2 in `.agent/decisions.md`.
> F272's LAST round has an entry here, which is the exception rather than the rule: under
> docs/agents/self_drive_protocol.md there is no second window, so the reviewer books a
> branch-terminating verdict into the FIRST commit of the next feature's first round rather
> than losing it with the session. Records belonging to features already marked `[x]` in
> docs/roadmap/STATUS.md are not here at all: `scripts/rotate_live_review.py` moves them
> byte-verbatim into the append-only `.agent/live_review_archive.md` in every closure
> sequence, under operator amendment amend0905-throughput, and that archive is read on demand
> by id, never at session start.

## Steps

THE SLICE ORDER BELOW IS THE ONE DECISION amend0907-cluster-first D1 RULED ON 2026-09-07,
reversing the order F260's Orchestrator brief inherited: the deletion runs FIRST, because it
was last in three consecutive features and each closed by split-and-close before reaching it.
R1 claim F274 in the roadmap ledger, cut the branch, re-point `.agent/plan.md` and
`.agent/context.md`, re-head this record and book F272's round 31 verdict into it → R2 the D11c
import-reachability test and its allowlist, DECISION F274 D1 ruling that test's shape and T003's
split boundary, and R-0830 → the two carry-overs F260's Design names, done before the first
`git rm` → DECISION F260 D3, the deletion paragraph, drafted → the prototype cluster deletion
itself, one commit per module group, which is NEVER SPLIT ACROSS SESSIONS → T001, the `Job.id`
flip measured with a recording property, its cap route ruled, and the persisted-key question the
round 1 probe exposed → T002, the classic runner, `job.run --cycles`, `job.run-next`, their
handlers and tests, and the resolver collapse DECISION F260 D5 places in the same commit range →
the integration gate → the closure sequence.
<<<END HEADF274R2>>>

<<<BEGIN RECORDR2 findings-append

Gate: F274 R1 — the F274 round 1 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER IN THE PRIMARY CHECKOUT RATHER THAN READ FROM THE HANDBACK. THIS ENTRY IS BOOKED BY ROUND 2 RATHER THAN BY ROUND 1, for two reasons that are both on the record: `.agent/STOP` appeared mid-session and guardrail G6 of docs/agents/self_drive_protocol.md ended that session before the booking round, and operator amendment amend0827-process-diet rule 1 rules that a verdict written into a committed and pushed `.agent/handoff.md` is persisted and is booked into the FIRST commit of the next round that is happening anyway. Range `13dfaabd93d7b6452a1d23ca698e29ed47ecf035`..`4d6da357ad807d980871dfb606f6e24bb0127ed4`, seven commits, every one single-parent, in the block's ordered sequence C0a, C0b, C1, C2, C3, C4 and the handback, with C5 and C6 NOT PERFORMED. THE ROUND IS A PASS DESPITE TWO SKIPPED COMMITS, AND THE SKIP IS THE REVIEWER'S FAULT RATHER THAN THE ROUND'S. That block's probe clause said a control failure outside an enumerated environment class stops the round under G8; the worker met that clause exactly as written and stopped. It then declined to append DECISION F274 D1, whose text asserted a measurement the skipped commit never took, on the ground that appending it would land a false claim in an append-only record — which is correct, is what constraint 1 and §4 item 4 together require, and is the single most valuable thing the round did. `.agent/decisions.md` was byte-identical at base and head, sha256 `6db4150fe9437cc702fcbd1199be58a5342e80678183f05944f14ba6a5e73993`, `^## DECISION F274 D` counted 0, and `.agent/f274_id_probe_inventory.md` did not exist — the reviewer confirmed all three. THE GATES THE ROUND REACHED ARE GREEN AND INDEPENDENTLY RE-MEASURED. G1 TRANSPORT: `.remedy-wt/f274-r1-block.md`, `.agent/authored/f274-r1.md` and `.agent/last_block.md` were all 30618 bytes and all hashed to `0a01672609eb7de5034f478647ee324397039562b5321690d626e8938426eccc`; per §3 item 37 that chain covers those three artefacts and claims nothing about emitted bytes. G2 THE RECORD RE-HEADING WAS THE ROUND'S DELICATE ACT AND IT IS CLEAN: `\n## Findings\n` occurred exactly once before and after, the head went 2501 bytes over 39 lines to 2534 over 35 and was byte-equal to its slice, and the whole append-only findings region was 490724 bytes over 498 lines with sha256 `d7ed620f9242c7929e0d8ae77070ef28b87c063578d8b03acd8cef88fac1cb03` BEFORE the edit and the SAME digest after it. G3 THE APPEND: prefix true, post equalled pre plus the slice with no added separator, N counted from the slice as 1, the negative control on the first appended paragraph rejected by both readers with the disk unchanged, registrations 62 to 62, resolutions 2 to 2, OPEN SET 60 TO 60 BY DISTINCT ID, `^Gate: ` 31 to 32, `^Gate: F272 R31` 0 to 1. G4: `.agent/plan.md` and `.agent/context.md` were byte-equal to their slices, the plan 36 lines against the cap of 50 and carrying `## Goal` and `## Next Steps`. G5 THE CLAIM: the pair was re-classified before use and the containment test printed `TO contains FROM: false`, so REWRITE with no append obligation; FROM 1 to 0, TO 0 to 1, one replacement and nothing else, and `^- \[~\] ` and `^- \[~\] F274 ` each occurred exactly once. G7 THE SUITES, re-run by the reviewer serially in the primary checkout, every one EXIT 0: `tests/docs/` 303 passed, `test_roadmap_index.py` 30 passed, `tests/ui_server/` 515 passed, `test_test_runner.py` 52, `test_resource_safety.py` 21 and `test_integrity_gate.py` 16, and the canary `tests/cli/test_golden_path.py` 42 passed. The tree was empty at every boundary, `git ls-files .remedy-wt` was empty, and worktrees went 14 to 15 to 14. SEVEN DEVIATIONS WERE DECLARED AND THE REVIEWER SUSTAINS ALL SEVEN; TWO OF THEM ARE THE REVIEWER'S OWN DEFECTS AND ARE RECORDED AS DATED PROSE-SLIP LINES RATHER THAN AS IDS, per amend0827 rule 2, because neither left anything wrong on disk. FIRST, THE PROBE SPEC WAS BROKEN AND THE WORKER CAUGHT IT BEFORE IT COULD CORRUPT A MEASUREMENT: the ordered getter-only `property id` raises on `job.id = uuid4()`, which is live at `tests/ui_server/test_live_state.py` lines 40 and 51 among 54 `.id = ` sites the reviewer counted repo-wide, and each such raise truncates its test before the reads below it — the exact under-counting the spec's own clause against raising existed to prevent. SECOND, THE CONTROL CLAUSE WAS UNMEETABLE BY CONSTRUCTION: it drew the environment class by ENUMERATED NODE ID while its own stated cause reaches further, and the worker showed by measurement that the class is TRANSIENT — the first full-suite pass in a fresh worktree itself builds `apps/ui/node_modules` and `apps/ui/dist`, so a second identical control went from 11 failures to 1. A cold control cannot be all-green on its first pass, so a clause requiring that is a stop trigger rather than a guard. THE ID PROMISE THIS ENTRY WOULD OTHERWISE HAVE REPEATED IS DEAD: round 1's own head paragraph closed with the next free id being R-0829, and operator amendment amend0907-cluster-first took that id on `main` before this entry was written, so the next id this feature mints is R-0830 and this round mints it. See DECISION amend0907-cluster-first D2.

- R-0830 — Medium, THE PRECONDITION THAT IS SUPPOSED TO OPEN THE PROTOTYPE-CLUSTER DELETION IS UNMEETABLE AS WRITTEN, BECAUSE ALL TWENTY-FOUR CLUSTER MODULES ARE REACHABLE FROM THE VERY ENTRY POINTS THE PROOF MEASURES. Raised by the reviewer at the F274 round 2 authoring, from its own dry run rather than from a reading of the prose. THE RULE. `docs/roadmap/features/T2_F260.md`, Design section, "Proof before deletion", requires that the import-reachability test over the six DECISION amend0905-vocab D11 (c) entry points "is run against the tree BEFORE deletion and must already pass with these modules absent from the reachable set", and `docs/roadmap/features/T2_F274.md` T003 carries that requirement into this feature with the ORDER RULING that a module the probe reaches is NOT deleted but reported with its import chain. THE MEASUREMENT, taken at `9c65a9225cdf4d60822d459d698b66d2d7cb19d7` by computing the transitive first-party `ast` import closure of `apps.cli.commands.do_cmd`, `apps.cli.commands.job`, `apps.cli.commands.mission_cmd`, `packages.orchestration.self_use_runner`, `apps.cli.commands.teach_cmd` and `packages.orchestration.ui_server`: the closure holds 319 of the 367 first-party modules on disk, and it holds EVERY ONE of the twenty-four modules F260's Design names as the cluster. Every one of them is reachable from `packages.orchestration.ui_server`, which is itself one of the six entry points, and sixteen are reached from it directly. So the precondition as worded is satisfied by no tree that still contains the cluster, and a slice that waits for it waits forever. THE SECOND HALF, WHICH IS THE PART THAT BITES. The reachability is NOT merely self-referential through the cockpit sections the deletion would remove anyway. A reverse sweep over `packages/`, `apps/`, `tests/` and `scripts/` at the same commit finds 33 DISTINCT PRODUCTION FILES importing a cluster module, and beyond the cluster's own `*_cmd.py` handlers and `packages/orchestration/ui_server.py` these SURVIVING consumers do: `packages/orchestration/orchestrator_brain.py`, `packages/orchestration/provider_patch_material.py`, `packages/orchestration/real_test_execution.py`, `packages/orchestration/repair_request_builder.py`, `packages/orchestration/self_dogfood.py`, `packages/orchestration/self_dogfood_execution.py`, `packages/orchestration/token_economy.py`, `packages/orchestration/agent_loop.py`, `packages/orchestration/autonomy_loop.py`, `packages/orchestration/dashboard.py`, `packages/orchestration/project_brain.py`, `apps/cli/commands/context.py`, `apps/cli/commands/worker.py`, `apps/cli/commands/worker_facade_cmd.py` and `apps/cli/commands/feature_cmd.py`. Those fifteen files are the SURVIVING consumers — the ones that are neither `ui_server` nor a handler of a cluster module — and eleven of them live under `packages/orchestration/` itself. `provider_trust` alone has seven such consumers and `worker_recommend` four. On the test side, counting DISTINCT FILES rather than import sites, `review_bundle` is imported from 16 test files, `progress_ledger` from 16 and `execution_approval_policy` from 3. DECISION amend0907-cluster-first D1's CONTEXT paragraph states that the cluster's orchestration modules "share only infrastructure with the build path — `data_paths`, `storage`, `run_log`, `timeline`, `project_registry`, `list_options` — so deleting them does not disturb what T001 and T002 touch", and that sentence is contradicted by this measurement: eleven surviving `packages/orchestration/` modules that are none of those six infrastructure names import the cluster directly. THE EFFECT. Read literally the ORDER RULING defers all twenty-four modules and the deletion round deletes nothing, which would make T003 a no-op and leave the cluster alive — the outcome three features have already produced. Read loosely it licenses deleting modules the probe says are reachable, which is the destructive reading the same ruling exists to forbid. Neither is what the amendment intended, so the gate cannot be run as written in either direction. THE FIX, and this finding is NOT resolved by the round that registers it: F274 R2 lands the test as a RATCHET rather than as a precondition, per DECISION F274 D1, so the allowlist records the reachable set instead of asserting the cluster is already outside it; the deletion round then SHRINKS the allowlist and the test's third assertion reds if it forgets to. What remains owed, and what this id stays open for, is the measured deletion PLAN: for each cluster module, the surviving consumers that must be cut before it can go, and for each such consumer the ruling on whether it is cut, moved or itself deleted. That plan is the round after the carry-overs, and F260's Design list is a starting point rather than the answer, because it names the modules and not the edges.
<<<END RECORDR2>>>

<<<BEGIN D1SLICE274 decisions-append

## DECISION F274 D1 — the reachability proof lands as a RATCHET, and "never split inside T003" binds the deletion rather than its prerequisites (2026-09-07)

CONTEXT. Operator amendment amend0907-cluster-first D1 reordered this feature so the prototype
cluster deletion runs first, and named its reachability test as "the gate that opens it". Two
questions had to be answered before that test could be written, and neither is settled by the
texts that order it. Both were forced by the reviewer's own dry run at
`9c65a9225cdf4d60822d459d698b66d2d7cb19d7`, which is registered as finding R-0830: the closure of
the six DECISION amend0905-vocab D11 (c) entry points holds all twenty-four cluster modules, so
F260's Design sentence requiring the test to "already pass with these modules absent from the
reachable set" is satisfied by no tree that still contains them.

THE FIRST QUESTION: what shape does the test take? CHOSEN — A RATCHET, NOT A PRECONDITION. The
test computes the reachable closure and asserts it against an ALLOWLIST file, which is D11c's own
wording — "no module outside an allowlist is importable from" the entry points — and not F260's
paraphrase. It is GREEN at this commit with the measured set recorded, a new orphan reaching the
graph reds it, and a third assertion reds when an allowlist entry names a module that has left
the tree, so a deletion round cannot forget to shrink it. The allowlist is generated from the
closure rather than typed, so the file is a measurement and not a wish. ALTERNATIVES: assert the
cluster absent, rejected because R-0830 measures that as unmeetable today and a gate that cannot
pass is the same defect as one that cannot fail; assert set EQUALITY against a snapshot, rejected
because it reds on every unrelated refactor that removes an import, which trains readers to
regenerate the file without reading it.

THE SECOND QUESTION: what does "NEVER SPLIT INSIDE T003" forbid? CHOSEN — IT BINDS THE DELETION
ITSELF AND NOT ITS PREREQUISITES. F260's brief and `docs/roadmap/features/T2_F274.md` both give
the rule the same stated reason: "a half-performed deletion is the single state this work must
not leave behind." The reachability test, the two carry-overs and the DECISION F260 D3 draft are
ordered BEFORE the first `git rm` and each leaves the tree fully consistent at every commit
boundary, so none of them can produce that state; they may therefore land across sessions. The
`git rm` sequence may not be started by a session that cannot finish it, and that prohibition is
unchanged and unweakened. ALTERNATIVE: read the rule as binding the whole slice, rejected because
it makes the prerequisites unstartable — no session can guarantee in advance that it will finish
a 54-file deletion it has not yet measured — which is the reading under which three consecutive
features never reached this work at all.

CONSEQUENCE. F274 R2 lands the test and the allowlist; the carry-overs and DECISION F260 D3
follow; the deletion round is planned from the reverse-import measurement R-0830 carries rather
than from F260's module list, because that list names modules and the deletion is bounded by
EDGES. R-0830 stays OPEN until that plan exists. REVERSE by deleting this section: the test then
has no ruled shape and the split boundary returns to being ambiguous, which is the state this
ruling replaced.
<<<END D1SLICE274>>>

<<<BEGIN SLIPS274R2 slips-append

2026-09-07 · F274 R1 · The reviewer's probe spec ordered a getter-only `property id` on a pydantic model while 54 `.id = ` assignment sites are live in the suite, so the ordered probe would have raised at each one and truncated the test before the reads below it — the exact under-counting the spec's own clause against raising existed to prevent; the worker caught it before it ran, and the corrected spec gives the property a setter calling `object.__setattr__`, verified working on pydantic 2.13.1.

2026-09-07 · F274 R1 · The reviewer's control clause drew the fresh-worktree environment failure class by ENUMERATED NODE ID and made any failure outside it stop the round, but the class is TRANSIENT — the first full-suite pass in a cold worktree itself builds `apps/ui/node_modules` and `apps/ui/dist`, so a second identical control fell from 11 failures to 1 — which made a cold control unable to pass by construction and stopped a round that had nothing wrong with it; the block's stated 13-failure reading was one sample written as a fact, and a control taken twice and baselined on the second is the counter-measure.

2026-09-07 · F274 R2 · The round 2 block authored in the previous session was still on disk and still hashed to its stated digest, and applying it would have minted R-0829 as a duplicate and failed its own byte gates: operator amendment amend0907-cluster-first had merged into the branch in between, taking that id and re-ordering the feature so the slice the block measured was no longer next. A block held over a session boundary is re-derived against the branch as it now stands before any part of it is trusted, however good its transport digest still is.
<<<END SLIPS274R2>>>
