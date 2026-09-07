# STEP T003/2 — F274 round 3 — map the deletion by its EDGES, and rule what that map forces

Goal: give R-0830 the plan it stays open for. Land a test-backed map of every SURVIVING consumer
that must be cut before a cluster module can be deleted, rule the consequences as DECISION F274
D2, register the route-policy capability the second carry-over has no home for, and book round
2's PASS verdict.

Base: `feature/f274-one-world-completion-part-two` at
`4ba5e0f6df26fbf0ed791f1eaa4d072d722802a6`. Stay on that branch; do not cut a new one, and do not merge anything.

WHY THIS ROUND EXISTS RATHER THAN THE CARRY-OVER. F260's Design orders the two carry-overs before
the first `git rm`, and the reviewer began authoring the first of them and stopped on what it
measured at `4ba5e0f6df26fbf0ed791f1eaa4d072d722802a6`: the destination name `mission report` IS ALREADY TAKEN by a live command
whose own handler imports `packages.orchestration.dogfood_run`, a cluster module. More broadly,
105 of the catalog's 341 command ids sit in a handler file that imports the cluster, `mission.run`
and `mission.report` among them. A carry-over authored onto that ground would have been authored
blind, so this round lays the ground first. NOTHING IS DELETED THIS ROUND and no command changes.

## Conventions

This block carries authored TEXTS. A whole text begins on a line whose PREFIX is
`<<<BEGIN <NAME> ` and ends on a line reading exactly `<<<END <NAME>>>`, and it is read INCLUSIVE
of the newline ending its last content line. Extract every text programmatically by matching those
two marker lines; never retype one and never hand-type a digest. The named units in this block are
PLANF274R3, RECORDR3 and D2SLICE274. RECORDR3 and D2SLICE274 EACH CARRY THEIR OWN leading blank
line — append each as-is and never add a separator newline of your own. PLANF274R3 is a whole-file
replacement and carries no leading blank line. No line of this block is a run of a single repeated
character.

## Bundle

C0a  save this block to `.agent/authored/f274-r3.md` by `shutil.copyfile`
C0b  mirror the same file to `.agent/last_block.md` by `shutil.copyfile`
C1   `.agent/plan.md` = PLANF274R3
C2   `.agent/live_review.md` findings region append RECORDR3
C3   the deletion-map test and its data file, written by you to the SPEC below
C4   `.agent/decisions.md` append D2SLICE274
C5   `.agent/handoff.md` full rewrite

## Change set

Exactly these paths and nothing else: `.agent/authored/f274-r3.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`,
`tests/orchestration/test_cluster_deletion_map.py`,
`tests/orchestration/cluster_deletion_map.txt`, `.agent/decisions.md`, `.agent/handoff.md`.
Nothing under `packages/`, `apps/`, `docs/` or `scripts/` is edited, nothing is deleted, and
`tests/orchestration/test_import_reachability.py` is NOT edited — C3 imports from it.

## Constraints

1. Apply every slice VERBATIM. If you believe one is wrong, apply it as written and declare the
   disagreement in the handback; never silently repair an authored text.
2. The commit order is C0a, C0b, C1, C2, C3, C4, C5 and is not varied. C1 precedes every other
   substantive commit because this round registers a finding and §3 item 23 requires the plan to
   advance first.
3. Read `.agent/STOP` with `os.path.exists` before C0a, before C3 and before C5, and report all
   three readings. If it exists, finish the commit in hand, write the handback and stop.
4. `.agent/live_review.md` is split by the FIRST occurrence of the marker `\n## Findings\n`. The
   text BEFORE it is the HEAD region; the marker and everything after it is the append-only
   FINDINGS region. C2 appends to the findings region and must leave the head byte identical.
5. This block mints exactly one finding id, R-0831, inside RECORDR3. Do not mint another and do
   not write a `Done:` paragraph: only reviewer-authored text resolves a finding. R-0830 stays
   OPEN — this round delivers its plan but does not discharge the deletion it plans.
6. Scratch goes under the gitignored `.remedy-wt/` and is removed BY EXACT PATH, never by a glob.
   `.remedy-wt/f274-r3-block.md` is KEPT: it is the first link of the transport chain.
7. Base measurements to CONFIRM on disk before use, declaring any divergence. `.agent/plan.md`
   2292 bytes / 41 lines. `.agent/live_review.md` 514989 bytes / 552 lines, its HEAD region 3396
   bytes / 43 lines at sha256
   `9622379fe041a62bb69372e6b6dc2266ee639e2be6bdf87a12d905c3db998cda`, its FINDINGS region 511593
   bytes / 509 lines at sha256
   `991f2c0e4b6eb6184dc9f96799ee02681d9a962d9ece80ee51ef1aa1165e911e`. `.agent/decisions.md`
   881507 bytes / 10961 lines at sha256
   `d2981fda0c5d1e103e97220fd0c71bbe3cc03fa1a0abedea6694e10b5258c477`.
8. Both files C3 creates are NEW. Confirm with
   `git ls-tree 4ba5e0f6df26fbf0ed791f1eaa4d072d722802a6 -- <path>` returning empty for each, and report both readings.
9. The repository is at a FROZEN ruff ceiling of 26 and DECISION F083 D5 forbids raising it. C3
   must leave that number unchanged. Bare `ruff` is denied; the spelling is
   `python3 -m ruff check <path>`.
10. This round rewrites `.agent/` state, so the four state readers named in G6 are run AS FOUR.

## The deletion map of C3 — a SPEC, not a slice

Build both files to this specification and report what you built. Neither is dictated byte for
byte: the property is what is gated.

- `tests/orchestration/test_cluster_deletion_map.py` records, per cluster module, the SURVIVING
  CONSUMERS that must be cut before that module can be deleted, and holds the record against the
  live import graph.
- IT REUSES the walker already shipped in `tests/orchestration/test_import_reachability.py` —
  import `first_party_imports`, `resolve_module_path` and `REPO_ROOT` from it. Do not write a
  second import walker; this repository keeps one call-directory walker on purpose.
- THE CLUSTER is the twenty-four module names F260's Design lists, pinned in a module-level
  constant and spelled `packages.orchestration.<name>`: provider_trust,
  provider_trust_verification, external_builder_sandbox, local_model_advisor,
  local_candidate_generator, candidate_quality, builder_routing, worker_registry,
  model_route_tournament, context_pack, context_optimizer, overnight_mission, overnight_executor,
  overnight_readiness, repair_loop_v2, dogfood_run, self_repair_proposal, main_builder_adapter,
  managed_builder_execution, execution_approval_policy, progress_ledger, review_bundle,
  worker_recommend, feature_planner.
- A SURVIVING CONSUMER is any `.py` file under `packages/`, `apps/` or `scripts/` that imports a
  cluster module and is itself neither a cluster module nor a handler of a cluster command. The
  cluster-command handlers are pinned in a second module-level constant, listed BY PATH and never
  matched by filename pattern, because `apps/cli/commands/worker.py` and
  `apps/cli/commands/context.py` host surviving commands as well as cluster ones. The reviewer's
  dry run used these seventeen: builder_routing_cmd, candidate_quality_cmd, dogfood_cmd,
  external_builder_cmd, local_advisor_cmd, local_candidate_cmd, main_builder_adapter_cmd,
  managed_builder_execution_cmd, overnight_cmd, overnight_mission_cmd, progress_cmd, provider_cmd,
  repair_loop_v2_cmd, review_cmd, route_policy_cmd, self_repair_cmd and tournament_cmd, each under
  `apps/cli/commands/`.
- `tests/orchestration/cluster_deletion_map.txt` holds one edge per line in the form
  `<cluster module> <- <repo-relative consumer path>`, sorted, GENERATED from the measurement
  rather than typed. A leading comment block states what it is and that the deletion round removes
  a line in the same commit that cuts its edge; blank and hash-comment lines are ignored.
- TEST FUNCTIONS, whose names you choose, asserting each of these properties:
  (a) every module named in the cluster constant still resolves to a file on disk, so the map
      cannot quietly describe a tree that no longer exists;
  (b) the recorded edge set EQUALS the measured one, reporting the two directions separately —
      edges that APPEARED, which is a consumer newly reaching the cluster, and edges that
      DISAPPEARED, which is a cut whose line the deletion round forgot to remove;
  (c) no recorded consumer is itself a cluster module, since a cluster-internal edge blocks
      nothing and must never be recorded as a blocker.
- The module docstring names finding R-0830 as the reason the map exists and states that the
  deletion is bounded by EDGES rather than by F260's module list.

The reviewer built this specification and ran it in a disposable worktree at `4ba5e0f6df26fbf0ed791f1eaa4d072d722802a6` before
emitting this block: it measured 42 edges over 22 cluster modules and 16 distinct surviving
consumer files, leaving `review_bundle` and `self_repair_proposal` as the only two cluster modules
with NO surviving consumer. Your numbers are YOURS — report what you measure and do not reconcile
toward these. A materially different figure is reported, not adjusted.

## Done when

G1 TRANSPORT — ONE digest comparison. `.remedy-wt/f274-r3-block.md`, `.agent/authored/f274-r3.md`
and `.agent/last_block.md` are byte-identical and all three hash to the digest the delegation
states beside this block. Report the untruncated 64-character value. Per §3 item 37 this chain
covers those three artefacts and claims nothing about the bytes emitted to you.

G2 THE RECORD APPEND (C2). (a) BYTE: the findings region's pre-image is a byte-exact PREFIX of its
post-image, and the post-image equals the pre-image followed by the RECORDR3 slice, which carries
its own leading blank line; the head region is byte-identical across the commit. (b) STRUCTURAL:
an independent reader compares the LAST N blank-line separated units of the whole file against the
slice's N paragraphs IN ORDER, where N is COUNTED by your script from the slice and never taken
from this block. A UNIT IS DEFINED HERE, because round 2 spent a deviation on its absence: split
on a blank line and compare each unit with its leading and trailing newlines STRIPPED, since the
slice carries its own leading newline while the same paragraph read from the whole file does not. (c) NEGATIVE CONTROL, in memory only, flipping one byte inside the FIRST appended
paragraph: both readers REJECT the flipped image and ACCEPT the real one, and the file on disk is
unchanged. This file holds multi-byte UTF-8, so a CHARACTER offset from `str.index` is NOT a byte
offset — locate the flip by searching the ENCODED bytes at or after the append point. (d) COUNTS,
before and after: distinct `^- R-\d{4}`, distinct `^Done: R-\d{4}`, the open set BY DISTINCT ID,
`^Gate: `, `^Gate: F274 R2` which is 0 before and 1 after, and `^- R-0831` which is 0 before and 1
after.

G3 THE DECISION APPEND (C4). The pre-image of `.agent/decisions.md` is a byte-exact PREFIX of the
post-image and the post-image equals the pre-image followed by the D2SLICE274 slice.
`^## DECISION F274 D` occurs 1 time before and exactly 2 times after, and `^## DECISION F274 D2 `
heads exactly one section.

G4 THE DELETION MAP (C3) — the property, not bytes this block dictates. Run each as its own
command and record its real exit code.
  (a) GREEN: the new test file alone is EXIT 0; and run TOGETHER WITH
      `tests/orchestration/test_import_reachability.py` in one command it is also EXIT 0, which is
      what proves the reuse import resolves under pytest's collection. Report both passed counts
      and the map file's edge-line count.
  (b) RED CONTROL ONE, an edge that APPEARS. In a disposable worktree at the C3 commit, append to
      a surviving module that the map does not already list as a consumer — the reviewer used
      `packages/orchestration/data_paths.py` — a single import line naming a cluster module, run
      the test, and report EXIT 1 with the appeared edge named. Restore that ONE file by exact
      path and re-run to EXIT 0.
  (c) RED CONTROL TWO, an edge that DISAPPEARS. In the same worktree append one line to the map
      naming an edge that does not exist, run the test, report EXIT 1 with the disappeared edge
      named, then remove that ONE line by exact path and re-run to EXIT 0.
  (d) THE CEILING: `python3 -m ruff check .` in the primary checkout reports 26 errors, unchanged
      from the base, and `python3 -B -m pytest tests/orchestration/test_ci_budgets.py -q -p no:randomly`
      is EXIT 0.
  Remove the worktree by exact path and prune; report `git worktree list` counts at the start and
  end of the round.

G5 THE PLAN (C1). `.agent/plan.md` is BYTE-EQUAL to PLANF274R3, is under the AGENTS.md cap of 50
lines, and carries `## Goal` and `## Next Steps`. Report its line count.

G6 THE SUITES AND THE TREE, run SERIALLY in the primary checkout, each as its own command with its
real exit code recorded and no pipe between the command and the exit reading: the four state
readers AS FOUR — `python3 -B -m pytest tests/ui_server/ -q -p no:randomly`,
`python3 -B -m pytest tests/orchestration/test_test_runner.py -q -p no:randomly`,
`python3 -B -m pytest tests/regression/test_resource_safety.py -q -p no:randomly` and
`python3 -B -m pytest tests/orchestration/test_integrity_gate.py -q -p no:randomly` — and the
canary `python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly`. Also report
`git status --porcelain` immediately before each commit, `git ls-files .remedy-wt`, and each
commit's insertion count from `git diff --numstat <parent> <commit>` against the cap of 500, for
every commit EXCEPT C5, whose own numbers cannot exist while its text is being written.

## Handback

Rewrite `.agent/handoff.md` in full per `docs/agents/handback_template.md`: feature and round,
`SESSION 2` of F274, branch, commit SHAs, the changed-files table with its `+/-` column taken from
`git diff --numstat` and compared cell by cell against the counts G6 orders, the REAL verification
results one line per gate, the open-findings count, the item-status table covering every C and G
item above exactly once, the one-sentence context self-assessment amend0905-throughput requires,
and the next expected action. It has no length cap. Then
`git push origin feature/f274-one-world-completion-part-two`. DO NOT create a pull request and DO
NOT merge anything.

<<<BEGIN PLANF274R3 whole-text
# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Finish what F272 could not reach inside its own limit: the prototype cluster deletion and the
classic-to-unified record flip DECISION F272 D15 measured as ATOMIC. DECISION
amend0907-cluster-first D1 reorders the slices so the deletion runs FIRST.

## Current Step

Round 3: land the test-backed cluster deletion map — per cluster module, the surviving consumers
that must be cut before it can go — rule what that map forces as DECISION F274 D2, and register
R-0831, the route-policy knobs the second carry-over has no F110 home for. This is the plan
finding R-0830 stays open for. Nothing is deleted and no command changes.

## Next Steps

1. Cut the edges the map records, module group by module group, starting with the two modules
   that already have none: `review_bundle` and `self_repair_proposal`.
2. The first carry-over, on the route DECISION F274 D2 fixes: the read-only overnight readiness
   and report views survive as `mission readiness` and `mission report`, the latter only in the
   commit that deletes the cluster-bound command already holding that name.
3. Draft DECISION F260 D3, the deletion paragraph, naming every deleted module and the feature
   that inherited its idea. Nothing is deleted before it exists.
4. The cluster deletion itself, one commit per module group, NEVER SPLIT ACROSS SESSIONS.
5. T001 — measure the `Job.id` flip with a recording property, rule the cap route, and rule the
   persisted key: `Job` stores its identity under the JSON key `"id"`, so renaming the field
   alone makes a stored job load with a FRESH id.
6. T002 — the classic runner and the resolver collapse.

## Risks

- The deletion reaches further than F260's Design describes: 105 of the catalog's 341 command ids
  sit in a handler file that imports the cluster, `mission.run` and `mission.report` among them.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12.
<<<END PLANF274R3>>>

<<<BEGIN RECORDR3 findings-append

Gate: F274 R2 — the F274 round 2 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER IN THE PRIMARY CHECKOUT AND IN A DISPOSABLE WORKTREE RATHER THAN READ FROM THE HANDBACK. Range `9c65a9225cdf4d60822d459d698b66d2d7cb19d7`..`4ba5e0f6df26fbf0ed791f1eaa4d072d722802a6` is the round as the worker pushed it; nine commits, every one single-parent, in the block's ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6 and the handback. THE ROUND LANDED THE D11c IMPORT-REACHABILITY RATCHET, WHICH IS THE PROOF F260's DESIGN NAMES AS THE GATE THAT OPENS THE CLUSTER DELETION, AND IT IS THE FIRST PRODUCTION ARTEFACT THIS FEATURE HAS SHIPPED. G1 TRANSPORT: `.remedy-wt/f274-r2v2-block.md`, `.agent/authored/f274-r2.md` and `.agent/last_block.md` are all 35679 bytes and all hash to `1e2a7bb50df1f497b424dd87289fcdf3f477c5601d57f9fd891e4c6e58408e3f`; per §3 item 37 that chain covers those three artefacts and claims nothing about emitted bytes. G2 THE RECORD HEADING: the head went 3063 bytes over 40 lines to 3396 over 43 and is byte-equal to the HEADF274R2 slice, `\n## Findings\n` occurs exactly once on both sides, and the append-only findings region hashes to `09f49be742173d4ae4b05fe71c465dc3fde583a71406b66ef977f148988565d5` BEFORE the edit and to the SAME digest after it. G3 THE APPEND: prefix true, post equals pre plus the slice with no added separator, the head byte-identical across the commit, N counted from the slice as 2, and the negative control flipped at byte 504880 — inside the FIRST appended paragraph, the append beginning at byte 504869 — rejected by BOTH readers with the disk unchanged; registrations 63 to 64, resolutions 3 to 3, OPEN SET 60 TO 61 BY DISTINCT ID, `^Gate: ` 32 to 33, `^Gate: F274 R1` 0 to 1 and `^- R-0830` 0 to 1. G4 THE DECISION APPEND: prefix true, 878136 bytes to 881507, `^## DECISION F274 D` 0 to 1 and `^## DECISION F274 D1 ` heading exactly one section. G5 THE REACHABILITY TEST IS A REAL GUARD AND THE REVIEWER PROVED IT BOTH WAYS IN ITS OWN DISPOSABLE WORKTREE: unmutated EXIT 0 at 3 passed; with a single import of `packages.orchestration.bench_run` appended to `packages/orchestration/self_use_runner.py` it is EXIT 1 naming EIGHT newly reachable modules, and after restoring that one file by exact path it is EXIT 0 again; with one nonexistent module appended to the allowlist it is EXIT 1 naming that module, and EXIT 0 again after removing that one line. The allowlist is 324 lines carrying 319 module entries, sorted and unique, and the closure measures 319 of the 367 first-party modules on disk — reproducing the reviewer's own pre-emission dry run exactly. `python3 -m ruff check .` reports 26 errors at the base and 26 at the round's head, so the frozen ceiling DECISION F083 D5 protects is untouched, and `test_ci_budgets.py` is EXIT 0 at 10 passed. G6: `.agent/plan.md` is byte-equal to its slice at 41 lines against the cap of 50, and `.agent/prose_slips.md` went 154472 bytes over 573 lines to 156171 over 579 with the prefix property true. G7 THE SUITES, re-run by the reviewer serially in the primary checkout, every one EXIT 0: `tests/ui_server/` 515 passed, `test_test_runner.py` 52, `test_resource_safety.py` 21, `test_integrity_gate.py` 16, and the canary `tests/cli/test_golden_path.py` 42 passed. The tree was empty at every boundary, `git ls-files .remedy-wt` is empty, and worktrees went 14 to 15 to 14. Every commit is under the 500-insertion cap, the largest being C5 at 469. SIX DEVIATIONS WERE DECLARED AND THE REVIEWER SUSTAINS ALL SIX. TWO DESERVE THE RECORD. THE FIRST IS THE REVIEWER'S AND IT IS A REAL DEFECT OF THE BLOCK: gate G3(b) ordered a comparison of blank-line separated units without DEFINING one, and the slice carries its own leading newline, so a reader that keeps boundary newlines rejects the true image while a reader that strips them accepts it. The worker hit exactly that, restored the file to its pre-image and re-ran the whole gate from clean rather than adjusting the reading, which is the correct handling; the negative control still discriminates under the stripped definition, so nothing landed wrong, and the counter-measure is that a structural gate STATES the unit definition it is measured under. THE SECOND is the worker's observation that C0a and C0b necessarily land while `.agent/plan.md` still describes the previous round; that is not a defect but the rule, since §3 item 23 exempts exactly the two block-save commits, which write nothing but the block itself. NO FINDING IS RESOLVED BY THIS GATE, and the one it minted, R-0830, stays open for the deletion plan round 3 delivers.

- R-0831 — Medium, EVERY USER-SETTABLE ROUTE-POLICY KNOB THE CLUSTER DELETION WILL REMOVE HAS NO EQUIVALENT IN F110's CONFIGURATION, SO THE SECOND CARRY-OVER HAS NOTHING TO CARRY THE CAPABILITY INTO. Raised by the reviewer at the F274 round 3 authoring, from the audit F260's Design orders as the second of its two carry-overs before the deletion. THE RULE. `docs/roadmap/features/T2_F260.md`, Design section, "Two carry-overs before deletion", item 2, orders that every user-settable knob of route policy be checked against F110's config keys in `packages/orchestration/role_config.py` and `packages/orchestration/model_routing.py`, and rules the outcome in advance: "existing knob → delete; missing knob → register as a finding, never rebuild". This finding is that registration, and it is ONE id rather than eight because it is one defect with eight instances, per §3 item 30. THE MEASUREMENT, taken at `4ba5e0f6df26fbf0ed791f1eaa4d072d722802a6`: the eight knobs F260 names by name are `prefer_local_for_cheap_tasks`, `prefer_ollama_for_cheap_tasks`, `preferred_worker_ids` and `user_selected_worker_ids` on the route policy `apps/cli/commands/route_policy_cmd.py` edits, `prefer_local_advisor` and `require_human_approval` on `builder_routing.BuilderRoutingPolicy`, and `risk_tier` and `default_autonomy_ceiling` on the `worker_registry` worker spec. NOT ONE of those eight names occurs anywhere in `packages/orchestration/role_config.py` or `packages/orchestration/model_routing.py`, and the only two configuration keys F110 owns are `model_routing.task_class_tiers` and `model_routing.promotion_evidence`, both declared in `packages/orchestration/config.py` and both about which MODEL TIER a task class routes to rather than about which WORKER a user prefers or what risk a user will accept. The two families do not overlap at any key. So every one of the eight falls on F260's "missing knob" branch. WHY THIS IS A FINDING AND NOT A REPAIR. F260's own rule says NEVER REBUILD, and this id therefore does not ask for the knobs to be re-implemented; it exists so that the capability loss is a recorded, dated, reversible decision rather than something a reader discovers from a deleted file. The persisted route policy itself lives under a `route_policy` directory written by `worker_registry`, a cluster module, so the stored per-job policies become unreadable at the deletion and the knobs are not merely unsettable but gone. WHAT WOULD RESOLVE IT: the deletion round deleting these knobs with their modules while DECISION F260 D3, the deletion paragraph, names route policy among the ideas deleted rather than inherited, and names this id. That paragraph is owed before the first `git rm` and is not written yet.
<<<END RECORDR3>>>

<<<BEGIN D2SLICE274 decisions-append

## DECISION F274 D2 — the cluster deletion is bounded by EDGES and ordered by the map, and the name `mission report` is not free until its current holder dies (2026-09-07)

CONTEXT. Finding R-0830 established that every module of the prototype cluster is reachable from
the six D11 (c) entry points and that modules outside the cluster import it, so the deletion
cannot be planned from F260's module list alone. Round 3 measured the graph the other way round,
at `4ba5e0f6df26fbf0ed791f1eaa4d072d722802a6`, and the numbers are what force this ruling: 42
SURVIVING EDGES from 16 distinct consumer files into 22 of the 24 cluster modules, and 105 of the
catalog's 341 command ids sitting in a handler file that imports the cluster.

CHOSEN, FIRST: THE MAP IS THE PLAN, AND IT IS A TEST RATHER THAN A DOCUMENT.
`tests/orchestration/cluster_deletion_map.txt` records one `module <- consumer` edge per line and
`tests/orchestration/test_cluster_deletion_map.py` holds it against the live import graph in both
directions, so an edge that appears reds the suite and an edge cut without removing its line reds
it too. A plan written as prose goes stale silently; this one cannot. It reuses the walker
`test_import_reachability.py` already ships, because this repository keeps one call-directory
walker. ALTERNATIVE: an `.agent/` inventory like `.agent/f272_t004_staging.md`, rejected because
the deletion will run over several rounds and possibly several sessions, and an inventory that
nothing re-measures is exactly the artefact that told three consecutive features the deletion was
cheap.

CHOSEN, SECOND: A CLUSTER MODULE IS DELETABLE ONLY WHEN ITS EDGE COUNT IN THE MAP IS ZERO, AND THE
ORDER FOLLOWS FROM THAT rather than from any list a human writes. At this commit exactly two
modules qualify — `review_bundle` and `self_repair_proposal` — and they are where the deletion
starts. Every other module is preceded by the work of cutting its edges, and each such cut is
ordinary product work with its own tests, not part of a deletion round under
amend0906-triage-throughput. This is what "one commit per module group" means once the graph is
known: the group is the module plus the edges that end on it.

CHOSEN, THIRD: THE FIRST CARRY-OVER'S DESTINATION NAME IS OCCUPIED, AND THE COLLISION IS RESOLVED
BY DELETION RATHER THAN BY RENAMING. F260's Design sends the read-only overnight readiness and
report views to `mission readiness` and `mission report`. `mission readiness` is free.
`mission report` IS NOT: the catalog already carries a `mission.report` entry whose handler
`_cmd_mission_report` in `apps/cli/commands/worker_facade_cmd.py` imports
`packages.orchestration.dogfood_run`, a cluster module, so the command that holds the name is
itself deletion-bound. THE RULING: the carried-over report takes the name `mission report` IN THE
SAME COMMIT that deletes the existing cluster-bound handler and its catalog entry, and not before;
the two never coexist, which is what AGENTS.md's "replacing is deleting" requires. `mission
readiness` may land earlier, since nothing holds that name. This is NOT a rename and does not
trespass on F261, which owns renames: the old command is DELETED with its module and a different
command inherits a freed name, which is the same move DECISION F272 D13 made for advertisements.

CONSEQUENCE, AND THE MEASUREMENT THE NEXT ROUND STARTS FROM. The first carry-over is a MOVE of 25
of the 29 top-level definitions of `packages/orchestration/overnight_readiness.py`, 650 of its 894
lines, into a surviving module; the four left behind are the plan path, which dies. That move is
safe, and this is the measured reason: every module the carried definitions import — `permissions`,
`run_contract`, `approval_queue`, `repair_loop`, `repository_snapshot`, `storage`, `proof_chain`,
`timeline`, `integrity_gate` and `data_paths` — survives the cluster deletion, so the carried code
acquires no new cluster edge. At 650 lines the move exceeds the DECISION F104 D1 cap of 500
insertions and is therefore staged across commits with the new module UNWIRED until the last of
them, which keeps every intermediate commit green without spending this feature's single
declared-oversize allowance; that allowance is reserved for T001's atomic flip, which cannot be
staged at all. REVERSE by deleting this section: the map then has no ruled standing, the deletion
order returns to F260's module list, and the `mission report` collision returns to being
undiscovered.
<<<END D2SLICE274>>>
