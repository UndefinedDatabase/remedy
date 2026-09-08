STEP — F274 ROUND 8 — a DELETION ROUND: cut smoke section 12ah, the last consumer of `context_optimizer`

Goal: delete section 12ah of `scripts/remedy_smoke.sh` and its line in the deletion map, which
takes `packages.orchestration.context_optimizer` to ZERO consumer edges under the WIDENED walker
round 7 landed — so unlike round 6's reading, this one is honest about non-python consumers. Book
round 7's PASS verdict and resolve findings R-0833 and R-0834. NO CLUSTER MODULE IS DELETED THIS
ROUND.

Base commit for every reading in this block: `b7b954b0c50f311ea74403eaaf9e43fef5192835`.

THIS IS A DELETION ROUND under operator amendment amend0906-triage-throughput rule 1: the change
set carries NO edited line under `packages/`, `apps/` or `tests/` — only a deleted script section,
the deleted map line it forces, and this workflow's own `.agent/` bookkeeping. That rule's four
measurements are gate G4 below, and it is why NO mutation red-proof of the deleted code is ordered
and no per-file byte reconstruction is asked for. The append into the record keeps its full
forensics regardless, per the gate-budget rule of docs/agents/planner_reviewer_prompt.md §3.

FRAME CONVENTION. No line of this block is a run of a single repeated character. Every slice is
delimited by a line reading `BEGIN <NAME> sha256=<hex> bytes=<n>` and a line reading `END <NAME>`,
and the slice is the bytes BETWEEN those two lines, the leading newline of an appended slice
included. Marker lines are never written to any file.


## Bundle — the commits of this round, in this order

C0a  Save this block verbatim as `.agent/authored/f274-r8.md`.
C0b  Mirror the same bytes into `.agent/last_block.md`.
C1   Replace `.agent/plan.md` with the PLAN8 slice.
C2   Append the RECORD8 slice to `.agent/live_review.md` — books round 7's PASS verdict and
     RESOLVES R-0833 and R-0834.
C3   Append the SLIPS8 slice to `.agent/prose_slips.md`.
C4   THE CUT: section 12ah and its map line. A PURE DELETION — this commit adds no line to any file.
C5   The handback: rewrite `.agent/handoff.md`, then push.

C1 is the first substantive commit because this round touches the finding ledger and the plan must
be current before every commit.


## Change set — these paths and nothing else

  .agent/authored/f274-r8.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/prose_slips.md
  .agent/handoff.md
  scripts/remedy_smoke.sh
  tests/orchestration/cluster_deletion_map.txt


## C4 — the cut

`scripts/remedy_smoke.sh` — delete SECTION 12ah ENTIRELY. It is one contiguous run of 49 lines and
2011 bytes that occurs exactly once in the file at the base commit; the reviewer measured both
figures and the uniqueness. The run BEGINS at the comment banner line that immediately precedes the
line `    # 12ah. Context Optimizer (Step 71)` and ENDS immediately before the comment banner line
that precedes the line `    # 12ai. Brain nodes: decision_queue (Step 69)`. Everything between goes:
the banner, the `12ah` heading comment, the `_SMOKE_SECTION="12ah"` assignment, the `echo`, the
whole `python3 -c` body with its closing quote, and the blank line that ends the run. SECTION 12ai
SURVIVES UNTOUCHED — round 7 repaired it and it is not this round's business. After the cut the
token `12ah` occurs ZERO times under `scripts/`, `packages/`, `apps/` and `tests/` — NOT zero
repo-wide, because this block names the section and C0a and C0b commit this block under `.agent/`,
which is exactly the scope G4(c) states. The smoke script must still parse: `bash -n` is part of
gate G4.

`tests/orchestration/cluster_deletion_map.txt` — delete the single line
`packages.orchestration.context_optimizer <- scripts/remedy_smoke.sh`. It occurs exactly once at the
base commit. THE MAP LINE GOES IN THE SAME COMMIT AS THE CUT, because the map test reds in both
directions and a line left behind is as red as a new edge.

Nothing else. In particular do NOT touch `tests/orchestration/test_cluster_deletion_map.py`: round
7's widened walker is what makes this round's reading trustworthy and it stays exactly as it is.


## Constraints

1. Apply every slice BYTE FOR BYTE. Do not reflow, retype or re-indent one. If something looks
   wrong, apply it as given and DECLARE the doubt in the handback.
2. RECORD8 and SLIPS8 are APPENDS: the target's existing bytes are a byte-exact PREFIX of the
   result and the slice is an exact SUFFIX. Each carries its OWN leading newline — ADD NO SEPARATOR
   of your own. PLAN8 replaces `.agent/plan.md` entirely.
3. The path set of C0a through C4 is exactly the paths listed under "Change set" other than
   `.agent/handoff.md`, which C5 writes.
4. Any destructive check runs ONLY inside a disposable `git worktree`, never in the primary
   checkout, which satisfies `git status --porcelain` == empty at every commit boundary. Remove and
   prune each worktree you create.
5. Do not write a `Done:` paragraph of your own. RECORD8 already carries the two the reviewer
   authored; apply them verbatim and add nothing.
6. Every gate below runs at a commit STRICTLY EARLIER than C5, so the handback can quote each.
7. RUN THE FULL SUITE IN THE PRIMARY CHECKOUT, never in a fresh worktree: `apps/ui/node_modules`
   and `apps/ui/dist` are gitignored, so a fresh worktree has neither and the server-backed tests
   fail on a missing UI build rather than on anything this round did.


## Done when — the gates, one line per gate in the handback

G1  TRANSPORT, at C0b. `sha256` of the committed `.agent/authored/f274-r8.md` equals `sha256` of
    the committed `.agent/last_block.md`, and both equal the digest the delegation message states.
    Report the digest you measured.

G2  THE RECORD APPEND, at C2, re-derived from the COMMITTED blobs.
    (a) BYTES: `.agent/live_review.md` 554669 -> 563333; pre-image a byte-exact PREFIX; post-image
        equal to pre plus the 8664-byte RECORD8 slice with no separator added.
    (b) STRUCTURE, over the WHOLE appended region: a unit is a maximal run of consecutive non-empty
        lines; COUNT N from the slice itself (do not take it from this block); the file's last N
        units equal the slice's units IN ORDER and everything before them is unchanged.
        Units 222 -> 225.
    (c) NEGATIVE CONTROL: flip the byte at ZERO-INDEXED BYTE offset 554670 of the post-image — read
        as bytes, not characters; it is the `G` opening the first appended paragraph — and confirm
        BOTH readers reject it. Flip in memory or in a disposable worktree.
    (d) COUNTS: registrations 68 -> 68, RESOLUTIONS 3 -> 5, OPEN SET 65 -> 63 BY DISTINCT ID
        (distinct `^- R-\d+ — ` ids minus distinct `^Done: R-\d+ — ` ids), `^Gate: ` 38 -> 39,
        `^Gate: F274 R7` 0 -> 1, `^Done: R-0833 — ` exactly 1, `^Done: R-0834 — ` exactly 1. The
        two `Landed:` lines round 7 wrote SURVIVE beside the resolutions: `^Landed: ` is unchanged
        at 37 lines.

G3  THE STATE PROSE FILES. `.agent/plan.md` at C1 is BYTE-EQUAL to the PLAN8 slice, is 41 lines
    against the cap of 50, and carries both `## Goal` and `## Next Steps`. `.agent/prose_slips.md`
    at C3 goes 159553 -> 160319 with the pre-image a byte-exact prefix and each appended line once.

G4  THE DELETION ROUND'S FOUR MEASUREMENTS, at C4 — amend0906-triage-throughput rule 1 asks for
    these and for nothing else about the deleted code.
    (a) `python3 -B -m pytest tests/orchestration/test_import_reachability.py -q` EXIT 0.
    (b) THE FULL SUITE green, in the PRIMARY CHECKOUT per constraint 7:
        `python3 -m pytest -q -n auto`. Report the exit code and the passed/failed/skipped counts.
    (c) A grep over every tracked file under `scripts/`, `packages/`, `apps/` and `tests/`, ALL
        FILE TYPES. The token `12ah` totals ZERO — it occurs 3 times at the base, all three inside
        the deleted section. The string `packages.orchestration.context_optimizer` totals ZERO
        UNDER `scripts/` ALONE — it occurs once there at the base, in the deleted section. Report
        both totals. THE SCOPE OF EACH CLAUSE IS DELIBERATE AND THE REVIEWER MEASURED WHY. `.agent/`
        is excluded from the `12ah` sweep because THIS BLOCK NAMES THAT SECTION and C0a and C0b
        commit this block, so a repo-wide zero would be unmeetable by construction. And the
        `context_optimizer` clause is scoped to `scripts/` because that string legitimately SURVIVES
        elsewhere at the base — 3 times in `apps/cli/commands/context_optimizer_cmd.py`, 5 in
        `tests/orchestration/test_project_brain.py`, once in
        `tests/orchestration/import_reachability_allowlist.txt` and once in the map test's own
        module list — none of which is this round's business, since the MODULE is not being deleted
        this round, only its last consumer edge.
    (d) `python3 -m ruff check scripts/remedy_smoke.sh` EXIT 0, and `bash -n scripts/remedy_smoke.sh`
        EXIT 0 — the script must still PARSE after a 49-line excision.

G5  THE EDGE TRUTH AND THE RATCHET, at C4, in a disposable worktree.
    (a) CONTROL: `python3 -B -m pytest tests/orchestration/test_cluster_deletion_map.py -q` EXIT 0.
    (b) Measured edges equal recorded edges at 37. The measured consumers of
        `packages.orchestration.context_optimizer` are THE EMPTY LIST. The modules with no edge are
        exactly `context_optimizer`, `context_pack`, `review_bundle` and `self_repair_proposal`.
        The non-`.py` consumers the widened walk finds are THE EMPTY LIST. Report all four.
    (c) RED: append the deleted line back to `tests/orchestration/cluster_deletion_map.txt`. The
        command of (a) must be EXIT 1 reporting `DISAPPEARED (1)` and naming that exact edge.
        Restore BY EXACT PATH and confirm byte-identity. The control of (a) returns to EXIT 0.

G6  THE TREE, at C4. `git status --porcelain` EMPTY; `git ls-files .remedy-wt` EMPTY;
    `git worktree list` the same count as before your first worktree and after your last prune;
    `git diff --name-only b7b954b0c50f311ea74403eaaf9e43fef5192835..<C4>` naming exactly the paths
    of constraint 3 and nothing else; every commit C0a through C4 single-parent. Report the
    INSERTION count of each commit C0a through C4 — the `+` column only, per AGENTS.md DECISION
    F104 D1 — and confirm that C4's is ZERO, because a deletion round's cut adds no line. Do not
    report C5's own numbers; the reviewer measures them at the next gate.


## Handback — rewrite `.agent/handoff.md` at C5, then push

Carry the mandated sections of `docs/agents/handback_template.md`: the state block, the commits
table with its `+/-` column taken from `git diff --numstat` and compared cell by cell against the
insertion counts G6 reports, the changed-files table, ONE LINE PER GATE G1 through G6 with its real
result, the deviations, the open-findings count, and the next expected action. No length cap. Name
the SESSION NUMBER as SESSION 4 of feature F274 and the round as 8. State the open-findings count
as the number G2(d) MEASURED. Add the one sentence of context self-assessment
amend0905-throughput requires.

DECLARE, do not silently repair: if any gate goes red, or any slice does not apply as described,
report the real command, the real exit code and the real output and say what you did.


BEGIN PLAN8 sha256=01c2d47f6880255f2a44a6eb22decbd756190d2127e33d2925cb80b32cec0f71 bytes=2376
# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Finish what F272 could not reach inside its own limit: the prototype cluster deletion and the
classic-to-unified record flip DECISION F272 D15 measured as ATOMIC. DECISION
amend0907-cluster-first D1 reorders the slices so the deletion runs FIRST.

## Current Step

Round 8, a DELETION ROUND under operator amendment amend0906-triage-throughput: delete section
12ah of `scripts/remedy_smoke.sh`, the last recorded consumer of `context_optimizer`, and its line
in the deletion map. That takes the module to zero edges under the WIDENED walker round 7 landed,
so this time the reading is honest about non-python consumers. Book round 7's PASS verdict and
resolve R-0833 and R-0834. No cluster module is deleted this round.

## Next Steps

1. `worker_recommend`'s three edges, in `agent_loop.py`, `autonomy_loop.py` and `dashboard.py`.
   These are LIVE RUNTIME CALLS rather than read-only views, so a DECISION naming what inherits
   worker recommendation is authored before the cut.
2. The fifteen edges `packages/orchestration/ui_server.py` still holds, which is the largest single
   block of remaining work and wants a DECISION covering the cockpit endpoints as a group.
3. The `worker_facade_cmd.py` edges, which carry the `mission report` name collision DECISION
   F274 D2 rules, and the two `feature_cmd.py` edges, which are live CLI commands.
4. The first carry-over, on the route DECISION F274 D2 fixes: the read-only overnight readiness
   and report views survive as `mission readiness` and `mission report`.
5. Draft DECISION F260 D3, the deletion paragraph. R-0832's fix clause binds it.
6. The cluster deletion itself, one commit per module group, NEVER SPLIT ACROSS SESSIONS.
7. T001 — the `Job.id` flip. Then T002 — the classic runner and the resolver collapse.

## Risks

- The map was blind twice and is now fixed once: R-0834's file-type blindness is closed, R-0832's
  event-name coupling is OPEN. Treat every "zero edges" reading as a claim about the WALKER.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12.
END PLAN8


BEGIN RECORD8 sha256=dff683cb2b9e8b3b340ea3c33f083899145301f80e168d06f079d25e80a2f19d bytes=8664

Gate: F274 R7 — the F274 round 7 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER ITSELF, in the primary checkout and in two disposable worktrees, against the COMMITTED blobs rather than the working tree. Range `450365a7214b3d6c04c394a645a5fee65cc00867`..`b7b954b0c50f311ea74403eaaf9e43fef5192835`, nine commits, every one single-parent, in exactly the ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6, C7, with the path set over `450365a7214b3d6c04c394a645a5fee65cc00867`..`685af2abb467eb0f53eae972abf03f7037c3f8d4` naming exactly the eight declared paths and nothing else. G1 TRANSPORT covers the emitted bytes rather than only the worker's self-consistency, because the block travelled as a FILE the worker copied rather than as text it retyped: the reviewer's own scratch original `.remedy-wt/f274-r7-block.md`, written and hashed BEFORE delegation, is BYTE-IDENTICAL to the committed `.agent/authored/f274-r7.md` and `.agent/last_block.md`, all three 31076 bytes at `fef320ac5fb35964459f808402ed4f61f5d3718e8232aff6b987d168a1bb6e70`. G2 THE TWO RECORD APPENDS both hold, re-derived from the committed blobs: at `f40a94d240061e730f98d59265eeac14b2fd21bb` 543921 to 554047 bytes against the 10126-byte RECORD7 slice, prefix true, post equal to pre plus slice, N counted from the slice as 3, units 217 to 220, the last three units matching IN ORDER with everything before them unchanged, and the control flipped at zero-indexed byte offset 543922 — the `G` opening the first appended paragraph — rejected by BOTH readers; at `685af2abb467eb0f53eae972abf03f7037c3f8d4` 554047 to 554669 against the 622-byte LANDED7 slice, N counted as 2, units 220 to 222, ordered equality true, and the control at byte offset 554048 — the `L` opening the first appended paragraph — rejected by both. Registrations 66 to 68, resolutions 3 to 3, OPEN SET 63 TO 65 BY DISTINCT ID, `^Gate: ` 37 to 38, `^Gate: F274 R6` 0 to 1, `^- R-0833 — ` and `^- R-0834 — ` exactly 1 each. G3: `.agent/plan.md` is byte-equal to its slice at 43 lines against the cap of 50 and carries both mandated headings; `.agent/prose_slips.md` 158733 to 159553 bytes with each appended line occurring once. G4 IS THE GATE THIS ROUND EXISTED FOR AND IT IS THE ONE THE REVIEWER RAN MOST CAREFULLY: section 12ai's embedded python was EXTRACTED FROM THE COMMITTED `scripts/remedy_smoke.sh` at `a81aef39e18ac09f94c16d219045048c46cde43c` — 961 bytes — and EXECUTED, giving EXIT 0 and printing `brain nodes: OK (decision_queue)`, with no occurrence of `context_budget` anywhere in the extracted body; and the sweep round 6 could not pass, re-run over all 1313 tracked files of `packages/`, `apps/`, `tests/` and `scripts/` with NO file-type filter at all, TOTALS ZERO against round 6's five. G5 THE EXTENDED GUARD IS LOAD-BEARING IN BOTH DIRECTIONS, proved in the reviewer's own disposable worktree at `a3082c281d130da20fa80947b81b063ba34b9302` with `__pycache__` purged and `python3 -B`: control EXIT 0 at 3 passed; neutering the new walker's return to `set()` is EXIT 1 reporting `DISAPPEARED (1)` and naming `context_optimizer <- scripts/remedy_smoke.sh`, which proves the new walker and not something else produces that edge; appending an embedded import of `review_bundle` to the smoke script is EXIT 1 reporting `APPEARED (1)` and naming `review_bundle <- scripts/remedy_smoke.sh`, which proves the walker sees a NEW embedded consumer rather than only the one it was written for; each mutated file restored byte-identically by exact path and the control returned to EXIT 0. G6 THE EDGE TRUTH: measured equals recorded at 38, the consumers of `packages.orchestration.context_optimizer` are EXACTLY `['scripts/remedy_smoke.sh']`, the zero-edge modules are `context_pack`, `review_bundle` and `self_repair_proposal`, and the non-`.py` consumers the widened walk finds are exactly `['scripts/remedy_smoke.sh']` — so round 6's zero-edge reading for that module IS CORRECTED ON DISK BY THE GUARD ITSELF, which is the outcome this round was designed to produce. G7 THE SUITES AND THE CEILING, re-run serially by the reviewer: the deletion map 3, import reachability 3, the smoke-script test 191, `test_project_brain.py` 82, the canary 42 and `test_ci_budgets.py` 10, every one EXIT 0; `ruff check .` 26 errors in a worktree checked out at `450365a7214b3d6c04c394a645a5fee65cc00867` and run from that worktree's own root, and 26 in the primary checkout, so DECISION F083 D5's frozen ceiling is untouched. G8 THE TREE: porcelain empty, `git ls-files .remedy-wt` empty, worktrees 14 before and after, per-commit insertions 380, 304, 18, 6, 4, 5, 30 and 4 for C0a through C6. TWO DEVIATIONS WERE DECLARED AND THE REVIEWER SUSTAINS BOTH, AND BOTH ARE THE REVIEWER'S OWN PROSE rather than ids, per amend0827 rule 2, because neither left anything wrong on disk: the block's G2(c) wrote the pattern `^Landed: ` beside the numeral 31 to 33, which is the DISTINCT-ID reading while the line reading is 35 to 37 — four ids carry two `Landed:` lines each — and both readings move by exactly two, which the reviewer re-measured; and the RECORD7 slice described section 12ai's surviving ordering assertion as "the one pinning the ordering weight 25" when that section asserts only membership in `_NODE_TYPE_ORDER` and the numeral 25 is pinned in `tests/orchestration/test_project_brain.py` instead, so the sub-clause described the wrong file while the pair that preserved the assertion was exact. NEITHER IS LOAD-BEARING AND NEITHER EARNS A CORRECTION ROUND. TWO FINDINGS ARE RESOLVED BY THIS GATE, R-0833 and R-0834, and their resolutions are the two paragraphs below.

Done: R-0833 — RESOLVED at `a81aef39e18ac09f94c16d219045048c46cde43c`, verified by the reviewer at the F274 round 7 gate. The `context_budget` half of `scripts/remedy_smoke.sh` section 12ai is cut and the `decision_queue` half is unchanged. THE PROOF IS EXECUTION RATHER THAN INSPECTION, which is what this finding's own evidence demanded: the section's embedded python was extracted from the COMMITTED blob at that commit, 961 bytes, and RUN, giving EXIT 0 and printing `brain nodes: OK (decision_queue)` where at `450365a7214b3d6c04c394a645a5fee65cc00867` the same extraction raised `ImportError: cannot import name 'NT_CONTEXT_BUDGET' from 'packages.orchestration.project_brain'`. The five deleted node symbols now total ZERO across all 1313 tracked files of `packages/`, `apps/`, `tests/` and `scripts/` with no file-type filter, against five at the base. The `Landed: R-0833` line above this paragraph is the worker's own marker and STANDS BESIDE this resolution rather than being replaced by it, per DECISION F272 D10. Note for the record, and not a defect: this resolution does NOT restore smoke coverage of the `context_budget` brain node, because that node no longer exists — the section now covers `decision_queue` alone, which is the only half whose subject survives.

Done: R-0834 — RESOLVED at `a3082c281d130da20fa80947b81b063ba34b9302`, verified by the reviewer at the F274 round 7 gate. `measured_edges` in `tests/orchestration/test_cluster_deletion_map.py` now walks EVERY file under a CONSUMER_ROOT rather than `rglob("*.py")`, reading a `.py` file with the existing `ast` walker and every other file with `embedded_first_party_imports`, a regex that matches ONLY the two python import forms at line start so that a bare dotted mention is not an edge — which is why `cluster_deletion_map.txt` does not become its own consumer. THE GUARD WAS PROVED LOAD-BEARING IN BOTH DIRECTIONS in a disposable worktree, with the unmutated control EXIT 0 on each side of the pair: neutering the new function's return to `set()` gives EXIT 1 and `DISAPPEARED (1)` naming `context_optimizer <- scripts/remedy_smoke.sh`, so the new walker is demonstrably what produces that edge; and appending an embedded import of `review_bundle` to the smoke script gives EXIT 1 and `APPEARED (1)` naming `review_bundle <- scripts/remedy_smoke.sh`, so the walker sees a consumer it was NOT written for. THE FALSE READING THIS FINDING NAMED IS CORRECTED ON DISK: the edge is recorded, measured equals recorded at 38, and `packages.orchestration.context_optimizer` reads as having exactly one consumer rather than none, so it is NOT deletable and round 6's claim that it was the fourth takeable module no longer stands anywhere but in the dated `Gate: F274 R6` entry that made it. The `Landed: R-0834` line above stands beside this resolution. THE SCOPE OF THIS RESOLUTION IS THE FILE-TYPE BLINDNESS AND NOTHING ELSE: R-0832's event-name coupling is untouched, still open, and still binds the round that drafts DECISION F260 D3.
END RECORD8


BEGIN SLIPS8 sha256=d30b0fca15a66c9f93739b2a20a473b94f200590f3209290c555b8e6b3c7f3ff bytes=766

2026-09-08 · F274 R7 · The round 7 block's gate G2(c) wrote the pattern `^Landed: ` beside the numeral 31 to 33, which is the DISTINCT-ID reading, while the line reading of that same pattern is 35 to 37 because four ids carry two `Landed:` lines each; both readings move by exactly two, the worker measured both and declared the gap, and the reviewer re-measured it.

2026-09-08 · F274 R7 · The RECORD7 slice described section 12ai's surviving ordering assertion as "the one pinning the ordering weight 25" when that section asserts only membership in `_NODE_TYPE_ORDER`, the numeral 25 being pinned in `tests/orchestration/test_project_brain.py` instead — the sub-clause named the wrong file while pair P4, which actually preserved the assertion, was exact.
END SLIPS8
