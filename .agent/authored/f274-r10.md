STEP — F274 ROUND 10 — a DELETION ROUND: the second half of the cockpit cut, six more sections and six more edges

Goal: delete the six remaining read-only cockpit section builders of `packages/orchestration/ui_server.py`
whose subject modules KEEP an edge afterwards, together with their six lines in the deletion map and
the test edits those cuts force. That takes the map from 31 edges to 25. The zero-edge set does NOT
move — that is the point of this round, not a shortfall in it — so no module becomes newly deletable
and DECISION F274 D4's carry-over hazard cannot arise here at all. Book round 9's PASS verdict. NO
CLUSTER MODULE IS DELETED THIS ROUND.

Base commit for every reading in this block: `3bcaa45c85c779dece35a02d369cc333416a0963`.

THIS IS A DELETION ROUND under operator amendment amend0906-triage-throughput rule 1: the change set
carries NO ADDED line under `packages/`, `apps/` or `tests/` — only deleted cockpit sections, the
deleted map lines those cuts force, and the test edits those cuts force, every one of which removes
lines and adds none. That rule's four measurements are gate G5. The two appends into the permanent
record keep their full byte forensics regardless, per the gate-budget rule of
docs/agents/planner_reviewer_prompt.md §3.

WHY `worker_registry` IS NOT IN THIS ROUND, and it is the measurement that shaped it: an `ast` walk of
`ui_server.py` — not a grep for section names — shows that module is imported by TWO top-level
definitions, `_build_worker_registry_section` and `_build_token_economy_section`. The second is the
cockpit view of `packages/orchestration/token_economy.py`, which SURVIVES the cluster deletion, so
cutting the worker-registry section alone would leave the edge standing and the map unchanged.
DECISION F274 D5, the DECISION10 slice below, rules this before a line is cut. Read it before C5.

FRAME CONVENTION. No line of this block is a run of a single repeated character. Every slice is
delimited by a line reading `BEGIN <NAME> sha256=<hex> bytes=<n>` and a line reading `END <NAME>`,
and the slice is the bytes BETWEEN those two lines, the leading newline of an appended slice
included. Marker lines are never written to any file.


## Bundle — the commits of this round, in this order

C0a  Save this block verbatim as `.agent/authored/f274-r10.md`.
C0b  Mirror the same bytes into `.agent/last_block.md`.
C1   Replace `.agent/plan.md` with the PLAN10 slice.
C2   Append the RECORD10 slice to `.agent/live_review.md` — books round 9's PASS verdict. It
     registers no id and resolves none.
C3   Append the DECISION10 slice to `.agent/decisions.md` — DECISION F274 D5.
C4   Append the SLIPS10 slice to `.agent/prose_slips.md`.
C5   THE CUT: six section builders, six dashboard dict lines, six map lines, four cockpit presence
     tests and three redaction surfaces. A PURE DELETION — this commit adds no line to any file.
C6   The handback: rewrite `.agent/handoff.md`, then push.

C1 is the first substantive commit because this round touches the finding ledger and the plan must be
current before every commit (docs/agents/planner_reviewer_prompt.md §3 item 23). C3 lands D5 BEFORE
C5 cuts a line, which is the order DECISION F274 D3 and D4 both set.


## Change set — these paths and nothing else

  .agent/authored/f274-r10.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/decisions.md
  .agent/prose_slips.md
  .agent/handoff.md
  packages/orchestration/ui_server.py
  tests/orchestration/cluster_deletion_map.txt
  tests/ui_server/test_dashboard_cockpit_truth.py
  tests/orchestration/test_provider_trust.py
  tests/orchestration/test_provider_patch_material.py
  tests/orchestration/test_overnight_executor.py


## C5 — the cut, described by SYMBOL

DELETE BY SYMBOL, NOT BY LINE NUMBER, AND WORK BOTTOM-UP WITHIN EACH FILE. The spans below are the
reviewer's `ast` reading at the base commit named above and are a CROSS-CHECK on the arithmetic, not
the instruction: every earlier deletion in the same file moves every later line number. Each span runs
from the `def` line through the function's last line INCLUSIVE, plus the blank lines that separate it
from whatever follows, so the file keeps the blank-line rhythm it had before.

`packages/orchestration/ui_server.py` — delete these six TOP-LEVEL functions entirely:

  | symbol                                  | span at the base | lines |
  |-----------------------------------------|------------------|-------|
  | `_build_main_builder_adapter_section`    | 596-631          | 36    |
  | `_build_managed_execution_section`       | 632-675          | 44    |
  | `_build_overnight_run_section`           | 844-884          | 41    |
  | `_build_provider_trust_section`          | 885-922          | 38    |
  | `_build_provider_verification_section`   | 1031-1062        | 32    |
  | `_build_local_advisor_section`           | 1161-1187        | 27    |

and the six lines of the dashboard dict inside `_build_dashboard` that call them, at base lines 1740,
1741, 1742, 1748, 1749 and 1754 — the keys `overnight_run`, `provider_trust`, `provider_verification`,
`main_builder_adapter`, `managed_execution` and `local_advisor`.

`_build_worker_registry_section` and `_build_token_economy_section` SURVIVE UNTOUCHED, with their dict
lines and the worker-registry presence test, for the reason DECISION F274 D5 rules. So do
`_build_overnight_section` and `_build_builder_routing_section`, which DECISION F274 D4 holds.

`tests/orchestration/cluster_deletion_map.txt` — delete these six lines. Each occurs exactly once at
the base:

  packages.orchestration.local_model_advisor <- packages/orchestration/ui_server.py
  packages.orchestration.main_builder_adapter <- packages/orchestration/ui_server.py
  packages.orchestration.managed_builder_execution <- packages/orchestration/ui_server.py
  packages.orchestration.overnight_executor <- packages/orchestration/ui_server.py
  packages.orchestration.provider_trust <- packages/orchestration/ui_server.py
  packages.orchestration.provider_trust_verification <- packages/orchestration/ui_server.py

Every OTHER line naming those same modules STAYS — each of the six keeps at least one consumer
elsewhere, which is exactly why this round moves no module to zero. Delete the six lines whose
consumer is `packages/orchestration/ui_server.py` and no others. THE MAP LINES GO IN THE SAME COMMIT
AS THE EDGES THEY RECORD, because the map test reds in both directions.

`tests/ui_server/test_dashboard_cockpit_truth.py` — delete four methods of class `TestDashboardShape`:
`test_provider_trust_section_present` (base 287-298), `test_provider_verification_section_present`
(299-312), `test_local_advisor_section_present` (378-390) and `test_overnight_run_section_present`
(391-402). The class keeps its other members, so no `pass` is needed and none may be added.
`test_worker_registry_section_present` STAYS.

THE THREE REDACTION GUARDS LOSE ONE SURFACE EACH AND SURVIVE AT FULL STRENGTH OTHERWISE. Each asserts
that no secret, path, traceback or diff leaks across a LIST of surfaces, and one entry of each list is
a builder this round deletes. Delete exactly two lines per file — the import line and its blob line —
and nothing else; every other surface in each list stays asserted:

  `tests/orchestration/test_provider_trust.py`, base lines 324 and 331
  `tests/orchestration/test_provider_patch_material.py`, base lines 235 and 242
  `tests/orchestration/test_overnight_executor.py`, base lines 363 and 372

In each file the two lines are the only occurrences of their text; the reviewer measured that. Do NOT
delete the surrounding test, the loop, or any other blob line.

Nothing else. In particular do NOT touch `tests/orchestration/test_cluster_deletion_map.py`.


## Constraints

1. Apply every slice BYTE FOR BYTE. Do not reflow, retype or re-indent one. If something looks wrong,
   apply it as given and DECLARE the doubt in the handback.
2. RECORD10, DECISION10 and SLIPS10 are APPENDS: the target's existing bytes are a byte-exact PREFIX
   of the result and the slice is an exact SUFFIX. Each carries its OWN leading newline — ADD NO
   SEPARATOR of your own. PLAN10 replaces `.agent/plan.md` entirely.
3. The path set of C0a through C5 is exactly the paths listed under "Change set" other than
   `.agent/handoff.md`, which C6 writes.
4. Any destructive check runs ONLY inside a disposable `git worktree`, never in the primary checkout,
   which satisfies `git status --porcelain` == empty at every commit boundary. Remove and prune each
   worktree you create.
5. Do not write a `Done:` paragraph of your own. RECORD10 resolves nothing and registers nothing; add
   neither.
6. Every gate below runs at a commit STRICTLY EARLIER than C6, so the handback can quote each.
7. RUN THE FULL SUITE IN THE PRIMARY CHECKOUT, never in a fresh worktree: `apps/ui/node_modules` and
   `apps/ui/dist` are gitignored, so a fresh worktree has neither and both the vitest foundation test
   and the npm-backed tests then fail on the missing build rather than on anything this round did.
8. READING A COMMITTED BLOB, since several gates below measure one. Use `git show <commit>:<path>`
   into memory or into a scratch file under the gitignored `.remedy-wt/`, or read it in a disposable
   worktree. NEVER write a blob over the tracked file and restore it afterwards: that mutates the
   primary checkout, which constraint 4 and docs/agents/self_drive_protocol.md guardrail G5 forbid.
9. THE KNOWN FLAKE, stated so you do not repair it. Finding R-0569 is OPEN and names the fixed port
   5273 under xdist, pinned at `tests/orchestration/test_product_smoke.py` line 90. If a server-backed
   file such as `tests/ui_server/test_command_channel.py` fails under `-n auto`, RE-RUN THAT FILE
   SERIALLY and report both results. The reviewer hit exactly this during the dry run, in a worktree,
   alongside npm and vitest failures of the kind constraint 7 names — 19 failures under `-n auto` of
   which 12 were environment or flake and every one passed serially. Do NOT edit any file to make such
   a red go away; report it.


## Done when — the gates, one line per gate in the handback

G1  TRANSPORT, at C0b. `sha256` of the committed `.agent/authored/f274-r10.md` equals `sha256` of the
    committed `.agent/last_block.md`, and both equal the digest the delegation message states. Report
    the digest you measured.

G2  THE RECORD APPEND, at C2, re-derived from the COMMITTED blobs.
    (a) BYTES: `.agent/live_review.md` 569829 -> 574989; pre-image a byte-exact PREFIX; post-image
        equal to pre plus the 5160-byte RECORD10 slice with no separator added. THESE ARE THE TWO
        READINGS gate (c) calls the BYTE reader: the prefix comparison alone cannot see a flip inside
        the appended region, so it is the `post == pre + slice` clause that carries that half.
    (b) STRUCTURE, over the WHOLE appended region: a unit is a maximal run of consecutive non-empty
        lines; COUNT N from the slice itself (do not take it from this block); the file's last N units
        equal the slice's units IN ORDER and everything before them is unchanged. Units 227 -> 228.
    (c) NEGATIVE CONTROL: flip the byte at ZERO-INDEXED BYTE offset 569830 of the post-image — read as
        bytes, not characters; it is the `G` opening the FIRST appended paragraph — and confirm that
        the BYTE reader of (a) and the STRUCTURAL reader of (b) each reject it. Flip in memory or in a
        disposable worktree.
    (d) COUNTS: registrations 68 -> 68, resolutions 5 -> 5, OPEN SET 63 -> 63 BY DISTINCT ID (distinct
        `^- R-\d+ — ` ids minus distinct `^Done: R-\d+ — ` ids), `^Gate: ` 40 -> 41, `^Gate: F274 R9`
        0 -> 1, `^Landed: ` UNCHANGED at 37 lines. This round spends NO id: the open set must not
        move, and a move in either direction is a red gate.

G3  THE DECISION APPEND, at C3, re-derived from the COMMITTED blobs.
    (a) BYTES: `.agent/decisions.md` 894911 -> 899779; prefix true; post equal to pre plus the
        4868-byte DECISION10 slice.
    (b) STRUCTURE over the whole appended region, N counted from the slice: units 1968 -> 1977, last N
        units equal the slice's units IN ORDER, everything before unchanged.
    (c) NEGATIVE CONTROL at zero-indexed byte offset 894912 — the `#` opening the FIRST appended
        paragraph — rejected by the byte reader and by the structural reader.
    (d) `^## DECISION F274 D5` occurs exactly ONCE in the post-image and ZERO times in the pre-image.

G4  THE PROSE STATE FILES. `.agent/plan.md` at C1 is BYTE-EQUAL to the PLAN10 slice, is 47 lines
    against the cap of 50, and carries both `## Goal` and `## Next Steps`. `.agent/prose_slips.md` at
    C4 goes 161300 -> 161811 with the pre-image a byte-exact prefix and each appended line once.

G5  THE DELETION ROUND'S FOUR MEASUREMENTS, at C5.
    (a) `python3 -B -m pytest tests/orchestration/test_import_reachability.py -q` EXIT 0.
    (b) THE FULL SUITE green, in the PRIMARY CHECKOUT per constraint 7: `python3 -m pytest -q -n auto`.
        Report the exit code and the passed/failed/skipped counts. The reviewer measured 19781 passed,
        23 skipped, 0 failed with this cut applied, against 19785 at the base — a difference of exactly
        the four deleted cockpit presence tests. THE THREE REDACTION TESTS STILL PASS AND STILL RUN:
        they lost a surface, not their assertions. Constraint 9 governs a red in a server-backed file.
    (c) A grep over every tracked file under `packages/`, `apps/`, `tests/` and `scripts/`, ALL FILE
        TYPES AND NO FILTER — 1313 files at the base. The six deleted symbols
        `_build_main_builder_adapter_section`, `_build_managed_execution_section`,
        `_build_overnight_run_section`, `_build_provider_trust_section`,
        `_build_provider_verification_section` and `_build_local_advisor_section` TOTAL ZERO. They
        total 18 at the base. Report the total. THE SCOPE IS DELIBERATE AND THE REVIEWER MEASURED WHY:
        `.agent/` is excluded because THIS BLOCK NAMES ALL SIX SYMBOLS and C0a and C0b commit this
        block there, so a repo-wide zero is unmeetable by construction; `docs/` is excluded because
        `docs/roadmap/features/T2_F260.md` names `_build_overnight_run_section` in describing the
        TARGET plan, which this round does not edit.
    (d) `python3 -m ruff check` EXIT 0 over the five touched `.py` paths — `packages/orchestration/
        ui_server.py`, `tests/ui_server/test_dashboard_cockpit_truth.py`,
        `tests/orchestration/test_provider_trust.py`,
        `tests/orchestration/test_provider_patch_material.py` and
        `tests/orchestration/test_overnight_executor.py`. All five are ruff-clean at the base; the
        reviewer ran that command there. AND the frozen ceiling: `ruff check .` REPORTS 26 ERRORS,
        unchanged, so DECISION F083 D5 is untouched — that command EXITS 1 while reporting them,
        which is the gate passing, because the ceiling is 26 rather than 0. Only `.py` paths are
        named here, per the clause the R-0819 recurrence added at round 9.

G6  THE EDGE TRUTH AND THE RATCHET, at C5, in a disposable worktree. Purge `__pycache__` in that
    worktree before the first run and use `python3 -B` for every run.
    (a) CONTROL: `python3 -B -m pytest tests/orchestration/test_cluster_deletion_map.py -q` EXIT 0.
        The reviewer measured 3 passed there with this cut applied.
    (b) Measured edges equal recorded edges at 25, with APPEARED and DISAPPEARED both empty. The
        cluster modules with NO measured edge are STILL EXACTLY THE TEN round 9 left:
        `candidate_quality`, `context_optimizer`, `context_pack`, `external_builder_sandbox`,
        `local_candidate_generator`, `model_route_tournament`, `overnight_mission`, `repair_loop_v2`,
        `review_bundle` and `self_repair_proposal` — this round adds none, and a zero-edge set of any
        other size is a red gate. The non-`.py` consumers are THE EMPTY LIST. The modules still
        holding an edge into `ui_server.py` are EXACTLY `builder_routing`, `overnight_readiness` and
        `worker_registry`; report those three, because DECISION F274 D4 and D5 turn on them.
    (c) RED: append the line `packages.orchestration.main_builder_adapter <- packages/orchestration/
        ui_server.py` back to `tests/orchestration/cluster_deletion_map.txt`. Count that exact byte
        string in that file first: it must be ZERO after C5. The command of (a) must then be EXIT 1
        reporting `DISAPPEARED (1)` and naming that exact edge. Restore BY EXACT PATH, confirm
        byte-identity against the committed blob, and confirm the control of (a) returns to EXIT 0.

G7  THE CUT'S SHAPE, at C5, measured against the COMMITTED blobs.
    (a) LINE ARITHMETIC, one reading per file: `packages/orchestration/ui_server.py` 4065 -> 3841;
        `tests/orchestration/cluster_deletion_map.txt` 46 -> 40; `tests/ui_server/
        test_dashboard_cockpit_truth.py` 416 -> 365; `tests/orchestration/test_provider_trust.py`
        389 -> 387; `tests/orchestration/test_provider_patch_material.py` 301 -> 299;
        `tests/orchestration/test_overnight_executor.py` 429 -> 427.
    (b) PARSE AND STRUCTURE, with `ast` rather than grep: all five `.py` files parse; the six deleted
        symbols are absent from the top-level definitions of `ui_server.py` while
        `_build_worker_registry_section`, `_build_token_economy_section`, `_build_overnight_section`,
        `_build_builder_routing_section` and `_build_dashboard` are still present; and each of the
        three redaction tests still exists and still asserts its remaining surfaces.
    (c) The map holds 25 non-comment lines and still holds a line for each of
        `packages.orchestration.overnight_readiness`, `packages.orchestration.builder_routing` and
        `packages.orchestration.worker_registry`.

G8  THE TREE, at C5. `git status --porcelain` EMPTY; `git ls-files .remedy-wt` EMPTY; `git worktree
    list` the same count as before your first worktree and after your last prune; `git diff
    --name-only 3bcaa45c85c779dece35a02d369cc333416a0963..<C5>` naming exactly the paths of constraint
    3 and nothing else; every commit C0a through C5 single-parent. Report the INSERTION count of each
    commit C0a through C5 — the `+` column only, per AGENTS.md DECISION F104 D1 — and confirm that
    C5's is ZERO, because a deletion round's cut adds no line. Do not report C6's own numbers; the
    reviewer measures them at the next gate.


## Handback — rewrite `.agent/handoff.md` at C6, then push

Carry the mandated sections of `docs/agents/handback_template.md`: the state block, the commits table
with its `+/-` column taken from `git diff --numstat` and compared cell by cell against the insertion
counts G8 reports, the changed-files table, ONE LINE PER GATE G1 through G8 with its real result, the
deviations, the open-findings count, and the next expected action. No length cap. Name the SESSION
NUMBER as SESSION 5 of feature F274 and the round as 10. State the open-findings count as the number
G2(d) MEASURED. Add the one sentence of context self-assessment amend0905-throughput requires.

DECLARE, do not silently repair: if any gate goes red, or any slice does not apply as described,
report the real command, the real exit code and the real output and say what you did.


BEGIN PLAN10 sha256=a68bc5340a505cabdaedaa3ccab925c89e1577fcbf9aea4c761ee2549e9d21e8 bytes=2863
# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Finish what F272 could not reach inside its own limit: the prototype cluster deletion and the
classic-to-unified record flip DECISION F272 D15 measured as ATOMIC. DECISION
amend0907-cluster-first D1 reorders the slices so the deletion runs FIRST.

## Current Step

Round 10, a DELETION ROUND under operator amendment amend0906-triage-throughput and the second
half of the cockpit cut round 9 began: delete the six remaining read-only cockpit sections of
`packages/orchestration/ui_server.py` whose subject modules KEEP an edge afterwards, with their six
deletion-map lines and the test edits those cuts force. DECISION F274 D5 rules the cut and records
why `worker_registry` is not among them. Book round 9's PASS verdict. No cluster module is deleted
this round and no module reaches zero edges, so D4's carry-over hazard cannot arise here.

## Next Steps

1. `worker_recommend`'s three edges, in `agent_loop.py`, `autonomy_loop.py` and `dashboard.py`.
   These are LIVE RUNTIME CALLS rather than read-only views: the reviewer measured that they feed
   the `token_policy_applied` run-log event and `CycleDecision.selected_worker`, and that
   `selected_worker` is named in `packages/orchestration/event_schemas.py`, so a DECISION naming
   what inherits worker recommendation is authored before the cut and the ruled event vocabulary
   is part of the question.
2. The two carry-overs F260's Design names, each freeing a cockpit section held back so far:
   overnight readiness to `mission readiness`, and the route-policy knobs checked against F110's
   config keys. `mission report` waits for the commit that deletes its current holder, per
   DECISION F274 D2.
3. `worker_registry`'s remaining edge, which is NOT a cockpit deletion: it is carried by
   `_build_token_economy_section` as well, and that view's subject module survives the cluster.
4. The `worker_facade_cmd.py` edges, which carry the `mission report` name collision, and the two
   `feature_cmd.py` edges, which are live CLI commands.
5. Draft DECISION F260 D3, the deletion paragraph. R-0832's fix clause binds it.
6. The cluster deletion itself, one commit per module group, NEVER SPLIT ACROSS SESSIONS.
7. T001 — the `Job.id` flip. Then T002 — the classic runner and the resolver collapse.

## Risks

- The map was blind twice and is now fixed once: R-0834's file-type blindness is closed, R-0832's
  event-name coupling is OPEN. Treat every "zero edges" reading as a claim about the WALKER.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12.
END PLAN10


BEGIN RECORD10 sha256=ccde2840c3c99cfa6e47bcfea929909e04059ba81fc16896521222593b8b686e bytes=5160

Gate: F274 R9 — the F274 round 9 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER ITSELF, in the primary checkout and in a disposable worktree, against the COMMITTED blobs rather than the working tree. Range `a903a44cdc73bd9588f65a2a3534fc9c4a6e4b1a`..`3bcaa45c85c779dece35a02d369cc333416a0963`, eight commits, every one single-parent, in the ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6, with the path set over the range to C5 naming exactly the eleven declared paths and nothing else. G1 TRANSPORT COVERS THE EMITTED BYTES rather than only the worker's self-consistency, because the block travelled as a FILE the worker copied rather than as text it retyped: the reviewer's scratch original `.remedy-wt/f274-r9-FINAL.md`, written and hashed BEFORE delegation, is BYTE-IDENTICAL to both committed copies, all three 34385 bytes at `a1cf8219765b1b75f8b23df24fcd4c40e806f1b373208bd59ee521996ceac95b`. G2 THE RECORD APPEND at `2aa946f0`: 563333 to 569829 bytes, pre-image a byte-exact PREFIX, post-image equal to pre plus the 6496-byte RECORD9 slice, N counted from the slice as 2, units 225 to 227, ordered equality true with everything before them unchanged, and the control flipped at zero-indexed byte offset 563334 — the `G` opening the FIRST appended paragraph — rejected by both the byte reader and the structural reader; registrations 68 to 68, resolutions 5 to 5, OPEN SET 63 TO 63 BY DISTINCT ID, `^Gate: ` 39 to 40, `^Gate: F274 R8` 0 to 1, and `^Landed: ` unchanged at 37 lines. THAT ROUND SPENT NO ID, which is what its own gate demanded of it. G3 THE DECISION APPEND at `0f01d8ef`: 889313 to 894911 bytes against the 5598-byte DECISION9 slice, N counted as 9, units 1959 to 1968, ordered equality true, the control at byte offset 889314 rejected by both readers, and `^## DECISION F274 D4` exactly once in the post-image against zero in the pre-image. G4: `.agent/plan.md` byte-equal to its slice at 47 lines against the cap of 50 with both mandated headings; `.agent/prose_slips.md` 160319 to 161300 bytes with each appended line occurring once. G5 THE DELETION ROUND'S FOUR MEASUREMENTS: import reachability EXIT 0 at 3 passed; THE FULL SUITE GREEN IN THE REVIEWER'S OWN RUN IN THE PRIMARY CHECKOUT at 19785 passed, 23 skipped, 0 failed, against 19791 at the base — a difference of exactly the six deleted tests; the six deleted builder symbols TOTAL ZERO over the 1313 tracked files of `packages/`, `apps/`, `tests/` and `scripts/` with NO file-type filter, against 18 at the base; `ruff check` EXIT 0 over the four touched `.py` paths and the frozen ceiling of DECISION F083 D5 unchanged at 26 errors from `ruff check .`. G6 THE EDGE TRUTH AND THE RATCHET, in the reviewer's own disposable worktree at C5: control EXIT 0 at 3 passed, measured equals recorded at 31 with APPEARED and DISAPPEARED both empty, the zero-edge modules exactly the ten the block named, the non-`.py` consumers THE EMPTY LIST, and `overnight_readiness` and `builder_routing` each still holding exactly one edge into `ui_server.py` — the two DECISION F274 D4 holds. THE RED PROOF BIT: the line `packages.orchestration.repair_loop_v2 <- packages/orchestration/ui_server.py` occurs ZERO times in the map after C5, and appending it back gives EXIT 1 reporting `DISAPPEARED (1)` and naming that exact edge, after which a restore by exact path returns the file to `d0cad9afd865deec689deba4f42e38c63d3f608e140e8bab55025113b3390722` and the control to EXIT 0. G7 THE CUT'S SHAPE, from the committed blobs: `ui_server.py` 4278 to 4065, the map 52 to 46, `test_dashboard_cockpit_truth.py` 450 to 416, `test_overnight_mission_integration.py` 76 to 68 and `test_model_route_tournament_integration.py` 111 to 97, every one as ordered; all five files parse under `ast`; the six deleted symbols are absent from the top-level definitions of `ui_server.py` while `_build_overnight_section`, `_build_builder_routing_section` and `_build_dashboard` are present; the map holds 31 non-comment lines including both held edges. G8 THE TREE: porcelain empty, `git ls-files .remedy-wt` empty, worktrees 14 before and after, per-commit insertions 403, 327, 17, 4, 70, 4 and ZERO for C0a through C5 — C5, the cut, is 275 deletions against 0 insertions across five files, a PURE DELETION as a deletion round requires. TWO CLARIFICATIONS WERE DECLARED AND THE REVIEWER SUSTAINS BOTH AS CLARIFICATIONS RATHER THAN DEFECTS. The first is that a flip inside the appended region is invisible to a bare PREFIX comparison by construction, so "both readers" means the byte reader — the `post == pre + slice` clause the same gate states — and the structural reader; the reviewer re-ran it that way and both rejected the flip at each of the two offsets. The second is that `ruff check .` exits 1 while reporting the 26 errors the frozen ceiling permits, so the gate asked for a COUNT rather than an exit code and was met exactly. THE WORKER ALSO CONFIRMED EVERY LINE SPAN THE BLOCK NAMED against the tree rather than assuming it, and the reviewer re-measured the same spans independently by `ast`. NO FINDING IS REGISTERED OR RESOLVED BY THIS GATE AND NO NEW ID IS MINTED.
END RECORD10


BEGIN SLIPS10 sha256=3d7fbbaf2b1a4b6a66bc42d9dd74490d3f9fa9434d526a3e3c9ba8ce05410e60 bytes=511

2026-09-08 · F274 R9 · The round 9 block's gates G2(c) and G3(c) ordered a flipped byte to be rejected by "BOTH readers" without naming which two, and the only clause of (a) that can see a flip inside the appended region is `post == pre + slice` rather than the byte-exact PREFIX beside it, so an honest worker had to spend a declared clarification saying which reading it had used; the gate was sound as written and the defect is only that it left the reader to work out which half of (a) was load-bearing.
END SLIPS10


BEGIN DECISION10 sha256=75b4f055a0b8c0c0a61450585f46122f2a1e2f259859b86f58e275dd6830a778 bytes=4868

## DECISION F274 D5 — the remaining cockpit sections of cluster modules are DELETED, and `worker_registry`'s edge is not a cockpit deletion at all (2026-09-08)

Date: 2026-09-08. Feature F274, round 10. Status: decided by the reviewer under
docs/agents/planner_reviewer_prompt.md §4 item 7; the operator's veto is any later session.

CONTEXT, MEASURED AT `3bcaa45c85c779dece35a02d369cc333416a0963`. DECISION F274 D4 deleted six cockpit sections whose subject modules
had exactly one edge each. Nine cluster modules still hold an edge into
`packages/orchestration/ui_server.py`. Two of them — `overnight_readiness` and `builder_routing` —
are the carry-over sources D4 deliberately held and they stay held. The other seven each keep at
least one edge OUTSIDE `ui_server.py` after their cockpit section goes, so cutting those sections
cannot take any module to zero and D4's hazard — a module reading deletable in the map while a
paragraph elsewhere says otherwise — cannot arise in this round at all.

CHOSEN, FIRST. SIX cockpit sections are deleted with their six map lines and the test edits those
cuts force, and nothing replaces them: `_build_local_advisor_section`,
`_build_main_builder_adapter_section`, `_build_managed_execution_section`,
`_build_overnight_run_section`, `_build_provider_trust_section` and
`_build_provider_verification_section`. AGENTS.md's Scope Control states that replacing is deleting,
that there is no attic and no compatibility reader, and that git is the archive. NOTHING INHERITS
THE IDEA: the cockpit loses six read-only diagnostic views whose SUBJECTS are modules this feature
is deleting, so there is no surviving thing left for the view to be about.

CHOSEN, SECOND, AND THIS IS THE MEASUREMENT THAT CHANGED THE ROUND. `worker_registry` is NOT among
them, and its edge is NOT a cockpit deletion. An `ast` walk of `ui_server.py` — rather than a grep
for section names — shows that the module is imported by TWO top-level definitions:
`_build_worker_registry_section`, which is a cluster-bound cockpit view, and
`_build_token_economy_section`, which is the cockpit view of `packages/orchestration/token_economy.py`,
a module that SURVIVES the cluster deletion and that DECISION F274 D3 already named as the inheritor
of the context-budget idea. Deleting the worker-registry section alone would therefore leave the edge
standing and the map unchanged, and deleting the token-economy section as well would destroy a view
of a surviving module, which is outside this feature's scope. That edge is retired later, by making
`_build_token_economy_section` stop reading a cluster module — ordinary product work with its own
tests, not a deletion round.

ALTERNATIVES CONSIDERED AND REJECTED. (a) Cut the worker-registry section anyway, for tidiness.
Rejected: it removes a test surface and buys no edge, so it is churn against a suite that was just
stabilised. (b) Cut both worker-registry and token-economy sections. Rejected: the token-economy view
is not this feature's to delete, and AGENTS.md's Scope Control forbids the "while I'm here" edit by
name. (c) Fold the seven into round 9. Rejected before round 9 ran, because the two carry-over
sources needed a ruling first and mixing a ruled hold with an unruled one is how a hold gets lost.

EVIDENCE THIS RESTS ON, all of it measured by the reviewer in a disposable worktree with the cut
applied, before this decision was written. The six builder symbols occur 18 times over the 1313
tracked files of `packages/`, `apps/`, `tests/` and `scripts/` — all file types, no filter — and ZERO
after the cut. The full suite is 19781 passed, 23 skipped, 0 failed against 19785 before, a
difference of exactly the four deleted cockpit presence tests; the three redaction guards in
`test_provider_trust.py`, `test_provider_patch_material.py` and `test_overnight_executor.py` SURVIVE
and still assert every other surface they covered, each having lost only the one surface that no
longer exists. `ruff check .` is 26 errors before and after, so DECISION F083 D5's frozen ceiling is
untouched.

CONSEQUENCE. The map goes from 31 edges to 25 and the zero-edge set does NOT move, staying at the ten
modules D4 left it at — which is the point of this round rather than a shortfall in it. After this
round `packages/orchestration/ui_server.py` holds exactly THREE cluster edges, and every one of them
is deliberately held with its reason on the record: `overnight_readiness` and `builder_routing` by
D4, `worker_registry` by this decision. The cockpit is no longer what blocks the deletion.

REVERSE THIS DECISION by restoring the six section builders and their six dashboard dict lines from
git history at `3bcaa45c85c779dece35a02d369cc333416a0963`, restoring the four cockpit presence tests and the three redaction
surfaces, and restoring the six map lines in the same commit.
END DECISION10
