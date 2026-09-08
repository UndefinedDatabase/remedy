STEP — F274 ROUND 9 — a DELETION ROUND: cut six read-only cockpit sections and their six map edges

Goal: delete the six cockpit section builders of `packages/orchestration/ui_server.py` whose subject
modules owe no carry-over, together with their six lines in the deletion map and the six tests those
cuts force. That takes the map from 37 edges to 31 and the cluster modules with NO recorded edge from
four to TEN. Book round 8's PASS verdict and the R-0819 RECURRENCE. NO CLUSTER MODULE IS DELETED THIS
ROUND — only consumer edges are cut.

Base commit for every reading in this block: `a903a44cdc73bd9588f65a2a3534fc9c4a6e4b1a`.

THIS IS A DELETION ROUND under operator amendment amend0906-triage-throughput rule 1: the change set
carries NO ADDED line under `packages/`, `apps/` or `tests/` — only deleted cockpit sections, the
deleted map lines those cuts force, the tests those cuts force, and this workflow's own `.agent/`
bookkeeping. That rule's four measurements are gate G5, and it is why NO mutation red-proof of the
deleted code is ordered. The two appends into the permanent record keep their full byte forensics
regardless, per the gate-budget rule of docs/agents/planner_reviewer_prompt.md §3.

WHY SIX AND NOT THE EIGHT THE ROUND 8 HANDBACK MEASURED: DECISION F274 D4, the DECISION9 slice below,
rules it before a line is cut. `_build_overnight_section` and `_build_builder_routing_section` are
HELD because their subject modules are the sources of F260's two carry-overs, so cutting their edges
would make the map read "deletable" for two modules that are not. Read D4 before C5.

FRAME CONVENTION. No line of this block is a run of a single repeated character. Every slice is
delimited by a line reading `BEGIN <NAME> sha256=<hex> bytes=<n>` and a line reading `END <NAME>`,
and the slice is the bytes BETWEEN those two lines, the leading newline of an appended slice
included. Marker lines are never written to any file.


## Bundle — the commits of this round, in this order

C0a  Save this block verbatim as `.agent/authored/f274-r9.md`.
C0b  Mirror the same bytes into `.agent/last_block.md`.
C1   Replace `.agent/plan.md` with the PLAN9 slice.
C2   Append the RECORD9 slice to `.agent/live_review.md` — books round 8's PASS verdict and the
     R-0819 RECURRENCE. It registers no id and resolves none.
C3   Append the DECISION9 slice to `.agent/decisions.md` — DECISION F274 D4.
C4   Append the SLIPS9 slice to `.agent/prose_slips.md`.
C5   THE CUT: six section builders, six dashboard dict lines, six map lines, six tests. A PURE
     DELETION — this commit adds no line to any file.
C6   The handback: rewrite `.agent/handoff.md`, then push.

C1 is the first substantive commit because this round touches the finding ledger and the plan must be
current before every commit (docs/agents/planner_reviewer_prompt.md §3 item 23). C3 lands D4 BEFORE
C5 cuts a line, which is the order DECISION F274 D3 set for round 5's single endpoint deletion.


## Change set — these paths and nothing else

  .agent/authored/f274-r9.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/decisions.md
  .agent/prose_slips.md
  .agent/handoff.md
  packages/orchestration/ui_server.py
  tests/orchestration/cluster_deletion_map.txt
  tests/ui_server/test_dashboard_cockpit_truth.py
  tests/orchestration/test_overnight_mission_integration.py
  tests/orchestration/test_model_route_tournament_integration.py


## C5 — the cut, described by SYMBOL

DELETE BY SYMBOL, NOT BY LINE NUMBER, AND WORK BOTTOM-UP WITHIN EACH FILE. The spans below are the
reviewer's reading at the base commit named above and are a CROSS-CHECK on the arithmetic, not the
instruction: every earlier deletion in the same file moves every later line number. Each span runs
from the `def` line through the function's last line INCLUSIVE, plus the blank lines that separate it
from whatever follows, so the file is left with the same blank-line rhythm it had before.

`packages/orchestration/ui_server.py` — delete these six TOP-LEVEL functions entirely:

  | symbol                                  | span at the base | lines |
  |-----------------------------------------|------------------|-------|
  | `_build_repair_loop_section`             | 596-633          | 38    |
  | `_build_external_builder_section`        | 961-991          | 31    |
  | `_build_overnight_mission_section`       | 1030-1068        | 39    |
  | `_build_model_route_tournament_section`  | 1069-1102        | 34    |
  | `_build_candidate_quality_section`       | 1146-1178        | 33    |
  | `_build_local_candidate_section`         | 1179-1210        | 32    |

and the six lines of the dashboard dict inside `_build_dashboard` that call them, at base lines 1951,
1952, 1953, 1956, 1957 and 1960 — the keys `local_candidate`, `candidate_quality`,
`external_builder`, `model_route_tournament`, `overnight_mission` and `repair_loop`.

`_build_overnight_section` and `_build_builder_routing_section` SURVIVE UNTOUCHED, with their dict
lines and their two presence tests. So does the `"repair_loop"` key of the PIPELINE payload near base
line 2175, which is a different subject the React UI really does read; the reviewer measured that
distinction and it is the one place in this cut where two unrelated things share a name.

`tests/orchestration/cluster_deletion_map.txt` — delete these six lines. Each occurs exactly once at
the base:

  packages.orchestration.candidate_quality <- packages/orchestration/ui_server.py
  packages.orchestration.external_builder_sandbox <- packages/orchestration/ui_server.py
  packages.orchestration.local_candidate_generator <- packages/orchestration/ui_server.py
  packages.orchestration.model_route_tournament <- packages/orchestration/ui_server.py
  packages.orchestration.overnight_mission <- packages/orchestration/ui_server.py
  packages.orchestration.repair_loop_v2 <- packages/orchestration/ui_server.py

THE MAP LINES GO IN THE SAME COMMIT AS THE EDGES THEY RECORD, because the map test reds in both
directions and a line left behind is as red as a new edge. The two lines for `overnight_readiness`
and `builder_routing` STAY.

`tests/ui_server/test_dashboard_cockpit_truth.py` — delete three methods of class
`TestDashboardShape`: `test_local_candidate_section_present` (base 325-335),
`test_candidate_quality_section_present` (336-346) and `test_external_builder_section_present`
(347-358). The class keeps its other members, so no `pass` is needed and none may be added.

`tests/orchestration/test_overnight_mission_integration.py` — delete
`TestSafeSurfaces::test_cockpit_section_readonly` (base 60-67). The class keeps two other tests.

`tests/orchestration/test_model_route_tournament_integration.py` — delete
`TestSafeSurfaces::test_cockpit_section_readonly` (base 98-105) and
`TestSafeSurfaces::test_cockpit_no_fake_winner` (base 106-111, the end of the file). The class keeps
`test_review_bundle_summary_safe`.

Nothing else. In particular do NOT touch `tests/orchestration/test_cluster_deletion_map.py`: round
7's widened walker is what makes this round's reading trustworthy and it stays exactly as it is.


## Constraints

1. Apply every slice BYTE FOR BYTE. Do not reflow, retype or re-indent one. If something looks wrong,
   apply it as given and DECLARE the doubt in the handback.
2. RECORD9, DECISION9 and SLIPS9 are APPENDS: the target's existing bytes are a byte-exact PREFIX of
   the result and the slice is an exact SUFFIX. Each carries its OWN leading newline — ADD NO
   SEPARATOR of your own. PLAN9 replaces `.agent/plan.md` entirely.
3. The path set of C0a through C5 is exactly the paths listed under "Change set" other than
   `.agent/handoff.md`, which C6 writes.
4. Any destructive check runs ONLY inside a disposable `git worktree`, never in the primary checkout,
   which satisfies `git status --porcelain` == empty at every commit boundary. Remove and prune each
   worktree you create.
5. Do not write a `Done:` paragraph of your own. RECORD9 resolves nothing and registers nothing; add
   neither.
6. Every gate below runs at a commit STRICTLY EARLIER than C6, so the handback can quote each.
7. RUN THE FULL SUITE IN THE PRIMARY CHECKOUT, never in a fresh worktree: `apps/ui/node_modules` and
   `apps/ui/dist` are gitignored, so a fresh worktree has neither.
8. READING A COMMITTED BLOB, since several gates below measure one. Use `git show <commit>:<path>`
   into memory or into a scratch file under the gitignored `.remedy-wt/`, or read it in a disposable
   worktree. NEVER write a blob over the tracked file and restore it afterwards: that mutates the
   primary checkout, which constraint 4 and docs/agents/self_drive_protocol.md guardrail G5 forbid.
9. THE KNOWN FLAKE, stated so you do not repair it. Finding R-0569 is OPEN and names the fixed port
   5273 under xdist, pinned at `tests/orchestration/test_product_smoke.py` line 90. If a server-backed
   file such as `tests/ui_server/test_command_channel.py` fails under `-n auto`, RE-RUN THAT FILE
   SERIALLY and report both results. The reviewer hit exactly this during the dry run — 9 failures in
   that file under `-n auto`, 106 passed serially, and a clean `-n auto` rerun — and it is not this
   round's business. Do NOT edit any file to make it go away.


## Done when — the gates, one line per gate in the handback

G1  TRANSPORT, at C0b. `sha256` of the committed `.agent/authored/f274-r9.md` equals `sha256` of the
    committed `.agent/last_block.md`, and both equal the digest the delegation message states. Report
    the digest you measured.

G2  THE RECORD APPEND, at C2, re-derived from the COMMITTED blobs.
    (a) BYTES: `.agent/live_review.md` 563333 -> 569829; pre-image a byte-exact PREFIX; post-image
        equal to pre plus the 6496-byte RECORD9 slice with no separator added.
    (b) STRUCTURE, over the WHOLE appended region: a unit is a maximal run of consecutive non-empty
        lines; COUNT N from the slice itself (do not take it from this block); the file's last N
        units equal the slice's units IN ORDER and everything before them is unchanged. Units
        225 -> 227.
    (c) NEGATIVE CONTROL: flip the byte at ZERO-INDEXED BYTE offset 563334 of the post-image — read as
        bytes, not characters; it is the `G` opening the FIRST appended paragraph — and confirm BOTH
        readers reject it. Flip in memory or in a disposable worktree.
    (d) COUNTS: registrations 68 -> 68, resolutions 5 -> 5, OPEN SET 63 -> 63 BY DISTINCT ID (distinct
        `^- R-\d+ — ` ids minus distinct `^Done: R-\d+ — ` ids), `^Gate: ` 39 -> 40, `^Gate: F274 R8`
        0 -> 1, `^Landed: ` UNCHANGED at 37 lines. This round spends NO id: the open set must not
        move, and a move in either direction is a red gate.

G3  THE DECISION APPEND, at C3, re-derived from the COMMITTED blobs.
    (a) BYTES: `.agent/decisions.md` 889313 -> 894911; prefix true; post equal to pre plus the
        5598-byte DECISION9 slice.
    (b) STRUCTURE over the whole appended region, N counted from the slice: units 1959 -> 1968, last
        N units equal the slice's units IN ORDER, everything before unchanged.
    (c) NEGATIVE CONTROL at zero-indexed byte offset 889314 — the `#` opening the FIRST appended
        paragraph — rejected by BOTH readers.
    (d) `^## DECISION F274 D4` occurs exactly ONCE in the post-image and ZERO times in the pre-image.

G4  THE PROSE STATE FILES. `.agent/plan.md` at C1 is BYTE-EQUAL to the PLAN9 slice, is 47 lines
    against the cap of 50, and carries both `## Goal` and `## Next Steps`. `.agent/prose_slips.md` at
    C4 goes 160319 -> 161300 with the pre-image a byte-exact prefix and each appended line once.

G5  THE DELETION ROUND'S FOUR MEASUREMENTS, at C5 — amend0906-triage-throughput rule 1 asks for these
    and for nothing else about the deleted code.
    (a) `python3 -B -m pytest tests/orchestration/test_import_reachability.py -q` EXIT 0.
    (b) THE FULL SUITE green, in the PRIMARY CHECKOUT per constraint 7: `python3 -m pytest -q -n auto`.
        Report the exit code and the passed/failed/skipped counts. The reviewer measured 19785 passed,
        23 skipped, 0 failed with this cut applied, against 19791 passed at the base — a difference of
        exactly the six deleted tests. Constraint 9 governs a red in a server-backed file.
    (c) A grep over every tracked file under `packages/`, `apps/`, `tests/` and `scripts/`, ALL FILE
        TYPES AND NO FILTER — 1313 files at the base. The six deleted symbols
        `_build_repair_loop_section`, `_build_external_builder_section`,
        `_build_overnight_mission_section`, `_build_model_route_tournament_section`,
        `_build_candidate_quality_section` and `_build_local_candidate_section` TOTAL ZERO. They total
        18 at the base. Report the total. THE SCOPE IS DELIBERATE AND THE REVIEWER MEASURED WHY:
        `.agent/` is excluded because THIS BLOCK NAMES ALL SIX SYMBOLS and C0a and C0b commit this
        block there, so a repo-wide zero is unmeetable by construction; `docs/` is excluded because
        `docs/roadmap/features/T2_F260.md` and `T2_F261.md` name three of them in describing the
        TARGET plan, which this round does not edit.
    (d) `python3 -m ruff check` EXIT 0 over the four touched `.py` paths — `packages/orchestration/
        ui_server.py`, `tests/ui_server/test_dashboard_cockpit_truth.py`,
        `tests/orchestration/test_overnight_mission_integration.py` and
        `tests/orchestration/test_model_route_tournament_integration.py`. All four are ruff-clean at
        the base; the reviewer ran that command there. AND the frozen ceiling: `ruff check .` reports
        26 errors, unchanged, so DECISION F083 D5 is untouched. Only `.py` paths are named here, which
        is the clause the R-0819 recurrence in RECORD9 adds.

G6  THE EDGE TRUTH AND THE RATCHET, at C5, in a disposable worktree. Purge `__pycache__` in that
    worktree before the first run and use `python3 -B` for every run, so no stale bytecode answers
    for a file you just changed.
    (a) CONTROL: `python3 -B -m pytest tests/orchestration/test_cluster_deletion_map.py -q` EXIT 0.
        The reviewer measured 3 passed there with this cut applied.
    (b) Measured edges equal recorded edges at 31. The cluster modules with NO measured edge are
        exactly these ten: `candidate_quality`, `context_optimizer`, `context_pack`,
        `external_builder_sandbox`, `local_candidate_generator`, `model_route_tournament`,
        `overnight_mission`, `repair_loop_v2`, `review_bundle` and `self_repair_proposal`. The
        non-`.py` consumers the widened walk finds are THE EMPTY LIST. `overnight_readiness` and
        `builder_routing` still have exactly one edge each, into `ui_server.py` — report those two
        explicitly, because DECISION F274 D4 turns on them.
    (c) RED: append ONE of the six deleted lines back to `tests/orchestration/cluster_deletion_map.txt`
        — use `packages.orchestration.repair_loop_v2 <- packages/orchestration/ui_server.py`, which
        occurs ZERO times in that file after C5. The command of (a) must be EXIT 1 reporting
        `DISAPPEARED (1)` and naming that exact edge. Restore BY EXACT PATH, confirm byte-identity
        against the committed blob, and confirm the control of (a) returns to EXIT 0. The reviewer
        ran this control at the cut and measured exactly that: 1 failed, 2 passed, the message
        `DISAPPEARED (1)` naming that line.

G7  THE CUT'S SHAPE, at C5, measured against the COMMITTED blobs.
    (a) LINE ARITHMETIC, one reading per file: `packages/orchestration/ui_server.py` 4278 -> 4065;
        `tests/orchestration/cluster_deletion_map.txt` 52 -> 46; `tests/ui_server/
        test_dashboard_cockpit_truth.py` 450 -> 416; `tests/orchestration/
        test_overnight_mission_integration.py` 76 -> 68; `tests/orchestration/
        test_model_route_tournament_integration.py` 111 -> 97.
    (b) PARSE AND STRUCTURE, with `ast` rather than grep: all five `.py` files parse; the six deleted
        symbols are absent from the top-level definitions of `ui_server.py` while
        `_build_overnight_section`, `_build_builder_routing_section` and `_build_dashboard` are still
        present; and the three named classes still hold their surviving methods.
    (c) The map holds 31 non-comment lines and still holds the two lines naming
        `packages.orchestration.overnight_readiness` and `packages.orchestration.builder_routing`.

G8  THE TREE, at C5. `git status --porcelain` EMPTY; `git ls-files .remedy-wt` EMPTY; `git worktree
    list` the same count as before your first worktree and after your last prune; `git diff
    --name-only a903a44cdc73bd9588f65a2a3534fc9c4a6e4b1a..<C5>` naming exactly the paths of constraint
    3 and nothing else; every commit C0a through C5 single-parent. Report the INSERTION count of each
    commit C0a through C5 — the `+` column only, per AGENTS.md DECISION F104 D1 — and confirm that
    C5's is ZERO, because a deletion round's cut adds no line. Do not report C6's own numbers; the
    reviewer measures them at the next gate.


## Handback — rewrite `.agent/handoff.md` at C6, then push

Carry the mandated sections of `docs/agents/handback_template.md`: the state block, the commits table
with its `+/-` column taken from `git diff --numstat` and compared cell by cell against the insertion
counts G8 reports, the changed-files table, ONE LINE PER GATE G1 through G8 with its real result, the
deviations, the open-findings count, and the next expected action. No length cap. Name the SESSION
NUMBER as SESSION 5 of feature F274 and the round as 9. State the open-findings count as the number
G2(d) MEASURED. Add the one sentence of context self-assessment amend0905-throughput requires.

DECLARE, do not silently repair: if any gate goes red, or any slice does not apply as described,
report the real command, the real exit code and the real output and say what you did.


BEGIN PLAN9 sha256=66061a3ffd3189ce14db7145d7b2f08b3f186337064da458738e12a25e09fb65 bytes=2808
# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Finish what F272 could not reach inside its own limit: the prototype cluster deletion and the
classic-to-unified record flip DECISION F272 D15 measured as ATOMIC. DECISION
amend0907-cluster-first D1 reorders the slices so the deletion runs FIRST.

## Current Step

Round 9, a DELETION ROUND under operator amendment amend0906-triage-throughput: cut the six
read-only cockpit sections of `packages/orchestration/ui_server.py` whose subject modules owe no
carry-over, with the six deletion-map lines and the six tests those cuts force. DECISION F274 D4
rules the deletion first, and rules why SIX rather than the eight the round 8 handback measured:
`overnight_readiness` and `builder_routing` are the sources of F260's two carry-overs, so their
edges are held until the carry-over lands. Book round 8's PASS verdict and the R-0819 recurrence.
No cluster module is deleted this round.

## Next Steps

1. `worker_recommend`'s three edges, in `agent_loop.py`, `autonomy_loop.py` and `dashboard.py`.
   These are LIVE RUNTIME CALLS rather than read-only views, so a DECISION naming what inherits
   worker recommendation is authored before the cut.
2. The two carry-overs F260's Design names, each with the cockpit section this round held back:
   overnight readiness to `mission readiness`, and the route-policy knobs checked against F110's
   config keys. `mission report` waits for the commit that deletes its current holder, per
   DECISION F274 D2.
3. The `ui_server.py` edges that survive both of the above: `local_model_advisor`,
   `main_builder_adapter`, `managed_builder_execution`, `overnight_executor`, `provider_trust`,
   `provider_trust_verification` and `worker_registry` — each has a second consumer outside
   `ui_server.py`, so cutting its cockpit section alone does not free it.
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
END PLAN9


BEGIN RECORD9 sha256=25dc8376b6080de7cd794d4ccad60a57bc547791cfa82bbf22fa9de610f793a0 bytes=6496

Gate: F274 R8 — the F274 round 8 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER ITSELF, in the primary checkout and in a disposable worktree, against the COMMITTED blobs rather than the working tree. Range `b7b954b0c50f311ea74403eaaf9e43fef5192835`..`0466d1ae0afd16a6fb31cb902b9c8a46aeed9e84`, seven commits, every one single-parent, in the ordered sequence C0a, C0b, C1, C2, C3, C4, C5, with the path set over the range to C4 naming exactly the seven declared paths and nothing else. G1 TRANSPORT covers the emitted bytes rather than only the worker's self-consistency, because the block travelled as a FILE the worker copied rather than as text it retyped: the reviewer's scratch original `.remedy-wt/f274-r8-block.md`, written and hashed BEFORE delegation, is BYTE-IDENTICAL to both committed copies, all three 23487 bytes at `2f9c169e3416cd9d528e5957b4547456510cc95146231fa87675bc3ff6d5f5c9`. G2 THE RECORD APPEND at `6fd135160a697ca7ac6c405c1e7b5a73b2cb2ce0`: 554669 to 563333 bytes, pre-image a byte-exact PREFIX, post-image equal to pre plus the 8664-byte RECORD8 slice, N counted from the slice as 3, units 222 to 225, ordered equality true with everything before them unchanged, and the control flipped at zero-indexed byte offset 554670 rejected by BOTH readers; registrations 68 to 68, RESOLUTIONS 3 TO 5, OPEN SET 65 TO 63 BY DISTINCT ID, `^Gate: ` 38 to 39, and `^Landed: ` UNCHANGED at 37 lines — the two `Landed:` lines round 7 wrote SURVIVE beside the resolutions, per DECISION F272 D10. G3: `.agent/plan.md` byte-equal to its slice at 41 lines against the cap of 50 with both mandated headings; `.agent/prose_slips.md` 159553 to 160319 bytes with each appended line occurring once. G4 THE DELETION ROUND'S MEASUREMENTS: import reachability EXIT 0; THE FULL SUITE GREEN IN THE REVIEWER'S OWN RUN at 19791 passed, 23 skipped, 0 failed; the token `12ah` ZERO across `scripts/`, `packages/`, `apps/` and `tests/` against three at the base, and `packages.orchestration.context_optimizer` ZERO under `scripts/` against one; `bash -n` EXIT 0, so a 49-line excision left the script parsing. G5 THE EDGE TRUTH AND THE RATCHET: control EXIT 0, measured equals recorded at 37, the consumers of `packages.orchestration.context_optimizer` THE EMPTY LIST, the zero-edge modules exactly `context_optimizer`, `context_pack`, `review_bundle` and `self_repair_proposal`, the non-`.py` consumers THE EMPTY LIST, and restoring the deleted map line EXIT 1 reporting `DISAPPEARED (1)` and naming that exact edge before a byte-identical restore. G6 THE TREE: porcelain empty, `git ls-files .remedy-wt` empty, worktrees 14 before and after, per-commit insertions 235, 148, 17, 6, 4 and ZERO for C0a through C4 — C4, the cut, is a PURE DELETION as a deletion round requires. THE FROZEN LINT CEILING HELD at 26 errors from `ruff check .` at the base in a worktree run from its own root and 26 in the primary checkout, so DECISION F083 D5 is untouched. TWO DEVIATIONS WERE DECLARED AND THE REVIEWER SUSTAINS BOTH. THE FIRST IS THE REVIEWER'S OWN DEFECT and is booked as the R-0819 recurrence in the paragraph below: gate G4(d) ordered `ruff check scripts/remedy_smoke.sh` EXIT 0, and the reviewer independently measured that command as EXIT 1 with 1207 diagnostics at `b7b954b0c50f311ea74403eaaf9e43fef5192835` and 1202 at `0466d1ae0afd16a6fb31cb902b9c8a46aeed9e84`, so the clause was unmeetable at its own base and measured nothing about that round, while the meaningful half of the same gate, `bash -n`, passed and the real ceiling gate held at 26. The worker reported 1204 and 1199 where the reviewer measures 1207 and 1202; the reviewer records BOTH readings rather than overwriting one, notes that the load-bearing fact is identical under either — red at the base, red at the head of that round, delta approximately the 49 deleted lines — and does not treat a numeral it cannot reproduce exactly as a defect of the worker. THE SECOND DEVIATION IS AN INTERMITTENT FULL SUITE UNDER `-n auto`, correctly attributed by the worker to the ALREADY-OPEN finding R-0569 rather than to that round, and the reviewer confirmed the attribution rather than accepting it: R-0569 is registered and unresolved, it names the fixed port 5273 under xdist, `tests/orchestration/test_product_smoke.py` line 90 still carries `port: int = 5273`, that file is BYTE-UNCHANGED across that round's range, the two named ids pass serially, and the reviewer's own full-suite run was green. NO FINDING IS RESOLVED BY THIS GATE AND NO NEW ID IS MINTED.

RECURRENCE of R-0819 at F274 round 8, measured by the reviewer at `0466d1ae0afd16a6fb31cb902b9c8a46aeed9e84` and booked here by round 9's first ledger commit. NO NEW ID IS SPENT: docs/agents/planner_reviewer_prompt.md §3 item 30 requires the open set to be searched for the DEFECT before an id is minted, and R-0819 is OPEN and its headline already states this exact class — a gate demanding a value that is already impossible at its own base, because the reviewer did not run it at the base before ordering it. The round 8 block's gate G4(d) ordered `python3 -m ruff check scripts/remedy_smoke.sh` to be EXIT 0. Ruff is a Python linter, and naming a `.sh` path explicitly bypasses its file-type discovery, so it parses the shell script as Python: EXIT 1 with 1207 diagnostics at the base `b7b954b0c50f311ea74403eaaf9e43fef5192835` and 1202 at `0466d1ae0afd16a6fb31cb902b9c8a46aeed9e84`, the first at `remedy_smoke.sh:22:16` on `remedy_smoke() {`. The gate could not pass in any round and measured nothing. It did no harm only because the same gate's `bash -n` clause carried the real property and passed, and because the frozen ceiling is gated separately by `ruff check .` at 26. THE ADDITION THIS RECURRENCE MAKES TO R-0819's FIX, binding on every later block of this feature that gates a NON-PYTHON file: name the tool that reads that file's LANGUAGE — `bash -n` or `shellcheck` for a shell script — and never a tool whose file-type discovery an explicit path suppresses. R-0819's own fix clause already requires every gate to be RUN AT THE BASE BEFORE BEING ORDERED, and this instance is that clause going unperformed a second time in the same feature, by the same reviewer, one round after it was quoted in the round 7 record. THE CLAUSE IS APPLIED IN THE BLOCK THAT CARRIES THIS PARAGRAPH: round 9 gates only `.py` paths with ruff, and every gate it orders was executed at `a903a44cdc73bd9588f65a2a3534fc9c4a6e4b1a` before it was written.
END RECORD9


BEGIN SLIPS9 sha256=5e823b0aa14f0060781ed5b3aba3e7dde41bfa5592c74fd2e5941ee8e0c04055 bytes=981

2026-09-08 · F274 R8 · The round 8 block's gate G4(d) paired a real property, `bash -n`, with an unmeetable one, `ruff check` against a `.sh` path, in a single lettered clause, so an honest worker had to split one gate's answer into a pass and a fail; the substantive defect is booked as the R-0819 recurrence and this line records only the packaging error of putting two properties under one letter.

2026-09-08 · F274 R8 · The round 8 handback's round 9 measurement stated that the only cockpit-contract consumer of the eight section builders was `tests/ui_server/test_dashboard_cockpit_truth.py` and that the blast radius per module was three sites; the round 9 dry run measured two further consumers, `tests/orchestration/test_overnight_mission_integration.py` and `tests/orchestration/test_model_route_tournament_integration.py`, which import two of the builders directly, so the sentence was false when written and nothing but the mandated dry run would have caught it.
END SLIPS9


BEGIN DECISION9 sha256=8176bc204f3bf7f1a5050eef5a422fa56e5eac4ce8dd7962a8bb7d62be97db9d bytes=5598

## DECISION F274 D4 — six cockpit sections are DELETED, and the two whose modules owe a carry-over are HELD so the map stays the whole plan (2026-09-08)

Date: 2026-09-08. Feature F274, round 9. Status: decided by the reviewer under
docs/agents/planner_reviewer_prompt.md §4 item 7; the operator's veto is any later session.

CONTEXT, MEASURED AT `a903a44cdc73bd9588f65a2a3534fc9c4a6e4b1a`. Eight prototype-cluster modules
have exactly ONE recorded edge each in `tests/orchestration/cluster_deletion_map.txt`, and in every
case that edge is `packages/orchestration/ui_server.py`, where a read-only cockpit section builder
imports the module and one line of the dashboard dict calls it. F260's Design names those sections
for deletion by name. Under DECISION F274 D2 the deletion is bounded by edges, so these eight edges
are the whole of what stands between eight modules and deletability — a quarter of the
twenty-four-module cluster in one round.

CHOSEN, FIRST. SIX of the eight sections are deleted, with their six map lines and the six tests
those cuts force, and nothing replaces them: `_build_repair_loop_section`,
`_build_external_builder_section`, `_build_overnight_mission_section`,
`_build_model_route_tournament_section`, `_build_candidate_quality_section` and
`_build_local_candidate_section`. AGENTS.md's Scope Control states that replacing is deleting, that
there is no attic and no compatibility reader, and that git is the archive. NOTHING INHERITS THE
IDEA, and this decision says so out loud rather than leaving it implicit: the cockpit loses six
read-only diagnostic views whose SUBJECTS are modules the same feature is deleting, so there is no
surviving thing for the view to be about. That is the one case in which "what inherits it" has the
honest answer "nothing".

CHOSEN, SECOND, AND THIS IS WHY THE NUMBER IS SIX RATHER THAN EIGHT. `_build_overnight_section` and
`_build_builder_routing_section` are HELD, and their two map lines with them. Their subject modules
are the sources of the two carry-overs F260's Design requires BEFORE deletion: `overnight_readiness`
owes 25 of its 29 top-level definitions to `mission readiness`, as DECISION F274 D2's CONSEQUENCE
clause measured, and `builder_routing.BuilderRoutingPolicy` owes the knobs `prefer_local_advisor`
and `require_human_approval` to the route-policy check against F110's config keys. Cutting those two
edges now would take both modules to ZERO recorded edges while both are still undeletable, and
DECISION F274 D2's CHOSEN FIRST makes the map the plan precisely so that no prose has to be trusted
about what is deletable. A module that reads deletable in the map and is not deletable in a
paragraph elsewhere is the prose plan D2 abolished, arriving through an exception instead of through
a document. Holding the edge is not a fiction: the section really exists and really imports the
module, so the map stays literally true and needs no new mechanism to stay safe.

ALTERNATIVES CONSIDERED AND REJECTED. (a) Cut all eight and record the carry-over debt in this
decision. Rejected on the reason above and on the checklist's own lesson at §3 item 23 and finding
R-0548 — a rule that lives only in prose is a rule the next block does not read — and the next block
here may be a deletion round in a later session, which is exactly when a forgotten debt becomes the
half-performed deletion F274's Orchestrator brief names as the single state this work must not leave
behind. (b) Cut all eight and add a mechanical carry-over-debt guard to the map test in the same
round. Rejected because adding a guard puts an ADDED line under `tests/`, which by
amend0906-triage-throughput rule 1 stops this being a deletion round at all and pulls the full
verification apparatus onto a change that does not need it; the guard is also unnecessary if the
edges are simply not cut yet. (c) Defer all eight until after both carry-overs. Rejected because six
of the modules owe nothing and there is no reason to make them wait.

EVIDENCE THIS RESTS ON, all of it measured by the reviewer in a disposable worktree with the cut
applied, before this decision was written. The React UI does not read the six deleted dashboard
keys: over all 4592 tracked files the quoted keys occur nowhere under `apps/ui/`, and the one
`repair_loop` key the UI does read is the PIPELINE payload built elsewhere in `ui_server.py`, which
this round does not touch. The six builder symbols occur 18 times over the 1313 tracked files of
`packages/`, `apps/`, `tests/` and `scripts/` — all file types, no filter — and ZERO after the cut.
The full suite is 19785 passed, 23 skipped, 0 failed against 19791 passed before, a difference of
exactly the six deleted tests. `ruff check .` is 26 errors before and after, so DECISION F083 D5's
frozen ceiling is untouched.

CONSEQUENCE. The map goes from 37 edges to 31, and the cluster modules with NO recorded edge go from
four to TEN: `candidate_quality`, `external_builder_sandbox`, `local_candidate_generator`,
`model_route_tournament`, `overnight_mission` and `repair_loop_v2` join `context_optimizer`,
`context_pack`, `review_bundle` and `self_repair_proposal`. None of the ten is deleted by this
decision — the modules and their files survive until the deletion round, which runs under DECISION
F260 D3 and names every module it removes.

REVERSE THIS DECISION by restoring the six section builders and their six dashboard dict lines from
git history at `a903a44cdc73bd9588f65a2a3534fc9c4a6e4b1a`, restoring the six tests those cuts
forced, and restoring the six map lines in the same commit.
END DECISION9
