STEP — F274 ROUND 14 — the last two `worker_recommend` edges, and the event vocabulary D7 ruled down

Goal: cut the `agent_loop.py` and `autonomy_loop.py` edges, which is where DECISION F274 D7 item 4
lands. Both loops stop calling `recommend_worker` and take their token mode from
`derive_token_mode`; `CycleDecision.selected_worker` goes; and `token_policy_applied` loses
`estimated_context_tokens`, `remote_model_requires_approval` and `selected_worker` in
`packages/orchestration/event_schemas.py` IN THE SAME COMMIT as the last emitter that writes them,
with the test and smoke-script pins moved in that commit too. `packages.orchestration.worker_recommend`
then holds NO recorded edge and becomes deletable. Also book round 13's PASS verdict, register
R-0836 and append the prose slip round 13 owed.

Base commit for every reading in this block: `f1f50ecd`.

WHY THE REGISTRY AND THE EMITTERS MOVE TOGETHER. `token_policy_applied` is a readiness signal that
SURVIVES the cluster deletion — `autonomy_readiness.py` reads it at lines 129, 248 and 318 and
`project_brain.py` at line 661 — so this round shrinks its vocabulary rather than deleting the
event. `validate_event_metadata` rejects BOTH extra and missing keys, so a tree where the registry
and an emitter disagree is red; one commit is what keeps every boundary green, and G7(a) proves it.

WHAT THE REVIEWER RAN BEFORE AUTHORING. The whole change was applied in a disposable worktree at the
base commit above and every gate below, both red proofs included, was run against the applied tree.
That run also covered `tests/orchestration/` and `tests/storage/` entire: 12145 passed with ONE
failure, `test_vitest_passes`, reading `Cannot find package 'vitest'` because a fresh worktree has no
`apps/ui/node_modules` — the known environment class, and why constraint 7 orders G6 into the
primary checkout.

FRAME CONVENTION. Every slice is delimited by a line reading `BEGIN <NAME> sha256=<hex> bytes=<n>`
and a line reading `END <NAME>`; the slice is the bytes BETWEEN those two lines, its leading newline
included, and marker lines never reach any file. No line of this block's FRAME — every line outside
a BEGIN/END pair — is a run of a single repeated character; inside PAIRS14 such runs occur, being
the closing parentheses of the python it carries, and each is pinned by its slice's byte count.


## Bundle — the commits of this round, in this order

C0a  Save this block verbatim as `.agent/authored/f274-r14.md`.
C0b  Mirror the same bytes into `.agent/last_block.md`.
C1   Replace `.agent/plan.md` with the PLAN14 slice.
C2   Append the RECORD14 slice to `.agent/live_review.md` — books round 13's PASS verdict and
     REGISTERS R-0836.
C3   Append the SLIPS14 slice to `.agent/prose_slips.md`.
C4   THE CUT: apply the pairs of PAIRS14. ONE commit.
C5   The handback: rewrite `.agent/handoff.md`, then push.

C1 is the first substantive commit because this round touches the finding ledger and the plan must be
current before every commit (§3 item 23); C2 precedes C4 because findings persist FIRST (§4 item 4).


## Change set — these paths and nothing else

  .agent/authored/f274-r14.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/prose_slips.md
  .agent/handoff.md
  packages/orchestration/agent_loop.py
  packages/orchestration/autonomy_loop.py
  packages/orchestration/event_schemas.py
  tests/storage/test_persistence.py
  tests/orchestration/cluster_deletion_map.txt
  scripts/remedy_smoke.sh


## C4 — the cut

PAIRS14 carries the pairs. `--- Q<n> FILE <path>` opens a pair, `--- Q<n> FROM` opens its FROM block
and `--- Q<n> TO` opens its TO block; a block is every following line up to the next marker. Replace
each FROM block with its TO block, once, keeping line endings. Marker lines reach no file. Q5's TO
block is EMPTY, which is a deletion, and its FROM block ends with the blank line that followed the
deleted call, so no double blank line is left behind.

PAIR SHAPES, MEASURED MECHANICALLY AND NOT BY EYE. The reviewer ran the containment test on every
pair at the base commit and records the output rather than a label: every pair printed
`TO contains FROM: false`, so EVERY pair here is a REWRITE owing the FROM-zero proof gate G4(a)
orders, and none carries the §4.9 append obligation. At that same commit each FROM block occurs
EXACTLY ONCE in its file; every pair was measured.

TWO REMOVALS THAT ARE EASY TO MISS, both already inside the pairs. `_initial_events` in
`agent_loop.py` existed ONLY to feed `recommend_worker`, so Q1 removes it — left behind it is an
unused local and `ruff` says so. And `_emit_token_policy_applied` loses its `events` parameter for
the same reason, so Q4 updates its ONE call site in the same commit.

DELIBERATELY NOT DONE. `packages/orchestration/worker_recommend.py` is NOT deleted here: it loses
its last recorded EDGE, which makes it deletable, and it dies with the cluster in the deletion round
DECISION F260 D3 governs. R-0836, which this round REGISTERS, is NOT fixed here — it is F272's
residue rather than D7's, and mixing it in is what AGENTS.md Scope Control forbids — so
`event_schemas.py` keeps its `agent_loop_cycle_decision` and `agent_loop_stopped` entries, and
`selected_worker` still occurs there ONCE afterwards, inside that surviving entry. That is why gate
G4(b) scopes its zero-gate away from this file.


## Constraints

1. Apply every slice BYTE FOR BYTE. Do not reflow, retype or re-indent one. If something looks
   wrong, apply it as given and DECLARE the doubt in the handback.
2. RECORD14 and SLIPS14 are APPENDS: the target's existing bytes are a byte-exact PREFIX of the
   result and the slice is an exact SUFFIX. Each carries its OWN leading newline — ADD NO SEPARATOR
   of your own. PLAN14 replaces `.agent/plan.md` entirely. PAIRS14 is appended to no file.
3. The path set of C0a..C4 is exactly the "Change set" paths other than `.agent/handoff.md`, at C5.
4. C4 IS ONE COMMIT and the reason is load-bearing: `validate_event_metadata` rejects extra keys, so
   a commit that shrinks the registry without the emitters, or the emitters without the registry,
   is RED at its own boundary. The map line and the edge it records are cut together for the same
   reason — `tests/orchestration/test_cluster_deletion_map.py` reds in both directions.
5. Any destructive check runs ONLY inside a disposable `git worktree`, never in the primary checkout,
   which satisfies `git status --porcelain` == empty at every commit boundary; prune each worktree.
6. Do not write a `Done:` paragraph of your own. This round registers R-0836 and resolves nothing.
7. Every gate runs at a commit STRICTLY EARLIER than C5, so the handback can quote each. Run G6 in
   the PRIMARY CHECKOUT: `apps/ui/node_modules` and `apps/ui/dist` are gitignored, so npm-backed
   tests in a fresh worktree fail on the missing build, not on this round. Do not report C5's own
   insertion count; the reviewer measures it at the next gate.
8. READING A COMMITTED BLOB, since several gates measure one: `git show <commit>:<path>` into memory
   or scratch under the gitignored `.remedy-wt/`, or a disposable worktree. NEVER overwrite-restore.
9. EVERY SUITE COUNT BELOW WAS MEASURED IN THE REVIEWER'S DRY-RUN WORKTREE, so it is a REFERENCE and
   the ordered property is the EXIT CODE. Report the number YOUR run produces and say so if it
   differs; round 13's block stated a worktree count for a primary-checkout command and was wrong.


## Done when — the gates, one line per gate in the handback

G1  TRANSPORT, at C0b. `sha256` of the committed `.agent/authored/f274-r14.md` equals `sha256` of the
    committed `.agent/last_block.md`, and both equal the digest the delegation message states. Report
    the digest you measured. Per §3 item 37 this covers those artefacts and is not a claim about the
    bytes emitted into a prompt.

G2  THE RECORD APPEND, at C2, re-derived from the COMMITTED blobs.
    (a) BYTES: `.agent/live_review.md` 594390 -> 602276; pre-image a byte-exact PREFIX; post-image
        equal to pre plus the RECORD14 slice — that second clause is the BYTE reader, the prefix
        clause alone being blind to a flip inside the appended region.
    (b) STRUCTURE over the WHOLE appended region: a unit is a maximal run of consecutive non-empty
        lines; COUNT N from the slice and REPORT it; the file's last N units equal the slice's units
        IN ORDER and everything before is unchanged. Units 234 -> 236.
    (c) NEGATIVE CONTROL: flip the byte at ZERO-INDEXED offset 594391 of the post-image — the `G`
        opening the FIRST appended paragraph, not the last — and confirm the BYTE reader of (a) and
        the STRUCTURAL reader of (b) each reject it.
    (d) COUNTS: registrations 69 -> 70, distinct resolutions 6 -> 6, OPEN SET 63 -> 64 BY DISTINCT
        ID, `^Gate: ` 44 -> 45, `^Gate: F274 R13 ` 0 -> 1, `^- R-0836 — ` 0 -> 1. The open set RISES
        by design: this round registers a finding it does not fix.

G3  THE PROSE STATE FILES. `.agent/plan.md` at C1 is BYTE-EQUAL to the PLAN14 slice, is 46 lines
    against the cap of 50, and carries both `## Goal` and `## Next Steps`. `.agent/prose_slips.md` at
    C3 goes 163225 -> 163910 with the pre-image a byte-exact prefix and the appended line once.

G4  THE CUT LANDED WHOLE, at C4, measured against the COMMITTED blobs.
    (a) THE PAIRS: every pair is a REWRITE, so for each the FROM block occurs ZERO times in its file
        and the TO block EXACTLY ONCE. Report the readings.
    (b) THE ZERO-GATE, scoped to exactly these files: `worker_recommend` totals ZERO in
        `packages/orchestration/agent_loop.py` and `packages/orchestration/autonomy_loop.py`, and
        `selected_worker` totals ZERO in those two, in `tests/storage/test_persistence.py` and in
        `scripts/remedy_smoke.sh`. `event_schemas.py` IS DELIBERATELY EXCLUDED and its count is
        REPORTED, not gated: it keeps `selected_worker` once, as the prose above measures.
    (c) THE SCHEMA: `EVENT_METADATA_SCHEMAS["token_policy_applied"]` has EXACTLY THREE keys, `mode`,
        `max_context_tokens` and `local_first`. Read it by IMPORTING the module and inspecting the
        frozenset, not by grepping the source.
    (d) THE MAP: `tests/orchestration/cluster_deletion_map.txt` goes 37 -> 35 lines, its edges — the
        lines neither blank nor comments — go 22 -> 20, its `worker_recommend` edges go 2 -> 0, the
        cluster modules holding at least one edge go 12 -> 11, and its post-image `sha256` is
        `7fbf3909fd6d094e0ab3654e8842222a1adf6a51cd6c74bf119b1f7c256d5155`.
    (e) Every touched `.py` file parses under `ast`, and `git diff --name-only f1f50ecd..<C4>` names
        exactly the paths of constraint 3.

G5  LINT, at C4. `python3 -m ruff check` over `packages/orchestration/agent_loop.py`,
    `packages/orchestration/autonomy_loop.py`, `packages/orchestration/event_schemas.py` and
    `tests/storage/test_persistence.py` EXIT 0 — this is the gate that catches an unused
    `_initial_events` or a stale import — and `python3 -m ruff check .` REPORTS 26 ERRORS, unchanged,
    so DECISION F083 D5's frozen ceiling is untouched; that command EXITS 1 while reporting them,
    which is the gate PASSING, the ceiling being 26 and not 0.

G6  THE SUITES, at C4, in the primary checkout per constraint 7. RUN EACH COMMAND ALONE and report
    its own number, per constraint 9. Prefix every pytest path with `python3 -B -m pytest` and suffix
    it with `-q`.
    (a) EACH OF THESE EXIT 0, with the reviewer's own worktree count in brackets:
        `tests/storage/test_persistence.py` [26], `tests/orchestration/test_autonomy.py` [81],
        `tests/orchestration/test_event_ledger.py` [21],
        `tests/orchestration/test_cluster_deletion_map.py` [3],
        `tests/orchestration/test_import_reachability.py` [3],
        `tests/test_remedy_smoke_script.py` [191], `tests/test_token_policy.py` [28], and THE CANARY
        `tests/cli/test_golden_path.py` [42, measured at round 13].
    (b) THE FULL SUITE, because this round changes a run-log event schema the whole product reads:
        `python3 -m pytest -q -n auto`, ORDERED PROPERTY ZERO FAILED. The reviewer states NO passed
        count here on purpose — it has not run the full suite at this base — so report the exit code
        and the passed, failed and skipped counts you measure, and the reviewer reconciles them at
        the next gate. If a server-backed file fails, re-run THAT FILE serially and report both
        results; do not edit any file to make a red go away.

G7  THE RED PROOFS, in a disposable worktree at C4 per constraint 5, each run with its UNMUTATED
    control FIRST in that same worktree, so a colour has a baseline.
    (a) THE REGISTRY AND THE EMITTERS ARE HELD IN AGREEMENT — the property D7 item 4 promises and the
        reason C4 is one commit. Control: `tests/storage/test_persistence.py` EXIT 0. Then add the
        line `            selected_worker="ollama/qwen3:8b",` to the `log.log` call inside
        `_emit_token_policy_applied` in `packages/orchestration/autonomy_loop.py`, directly after its
        `local_first=True,` line — that three-line window occurs ONCE in that file at C4 — and confirm
        EXIT 1 with `TestTokenPolicyAppliedSchema::test_autonomy_loop_emits` among the failures, which
        is `validate_event_metadata` reporting an extra key. Restore, confirm EXIT 0, report the ids.
    (b) THE MAP RATCHET REALLY BITES FOR BOTH CUT EDGES. Control:
        `tests/orchestration/test_cluster_deletion_map.py` EXIT 0. Then re-insert both lines
        `packages.orchestration.worker_recommend <- packages/orchestration/agent_loop.py` and
        `packages.orchestration.worker_recommend <- packages/orchestration/autonomy_loop.py` into
        `tests/orchestration/cluster_deletion_map.txt` — those exact bytes occur ZERO times in that
        file at C4 — and confirm EXIT 1 with `DISAPPEARED (2)`. Restore, confirm EXIT 0, and report
        the digest you restored to.

G8  THE TREE, at C4. `git status --porcelain` EMPTY; `git ls-files .remedy-wt` EMPTY; `git worktree
    list` the same count as before your first worktree and after your last prune; every commit C0a
    through C4 single-parent. Report each commit's INSERTION count; the reviewer measured C4's
    applied change as 24 insertions and 49 deletions over six files, against the DECISION F104 D1 cap
    of 500. Read `.agent/STOP` at the round's start, before C4 and after C5, reporting all three.


## Handback — rewrite `.agent/handoff.md` at C5, then push

Carry the mandated sections of `docs/agents/handback_template.md`: the state block, the commits table
with its `+/-` column from `git diff --numstat`, the changed-files table, ONE LINE PER GATE G1
through G8 with its real result, the deviations, the open-findings count and the next expected
action. No length cap. Name the SESSION NUMBER as SESSION 6 of feature F274 and the round as 14,
state the open-findings count as the number G2(d) MEASURED, and add the one sentence of context
self-assessment amend0905-throughput requires. DECLARE, do not silently repair: report the real
command, the real exit code and the real output, and say what you did.


BEGIN PLAN14 sha256=92cb34938c23dbf8999d499759ff7d24638e5ef9f8ed1fb30d36fbfa5f15d4e8 bytes=2813
# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Finish what F272 could not reach inside its own limit: the prototype cluster deletion and the
classic-to-unified record flip DECISION F272 D15 measured as ATOMIC. DECISION
amend0907-cluster-first D1 reorders the slices so the deletion runs FIRST.

## Current Step

Round 14, the last two `worker_recommend` edges, in `agent_loop.py` and `autonomy_loop.py`. This is
where DECISION F274 D7 item 4 lands: both loops stop calling `recommend_worker` and take their token
mode from `derive_token_mode`, `CycleDecision.selected_worker` goes, and `token_policy_applied`
loses `estimated_context_tokens`, `remote_model_requires_approval` and `selected_worker` in
`packages/orchestration/event_schemas.py` in the SAME commit as the last emitter that writes them,
with the test and smoke-script pins moved with them. `worker_recommend` then holds NO recorded edge
and becomes deletable. Book round 13's PASS verdict, register R-0836 and append the slip round 13
owed.

## Next Steps

1. Fix R-0836: delete the `agent_loop_cycle_decision` and `agent_loop_stopped` entries of
   `EVENT_METADATA_SCHEMAS` and the ten sites in `tests/orchestration/test_event_ledger.py` that
   pin them. Their sole emitter died with `_cmd_run_loop` in F272 round 19; this is that deletion
   finished, and it is a ruled vocabulary the product no longer speaks.
2. The two carry-overs F260's Design names: overnight readiness to `mission readiness`, and the
   route-policy knobs checked against F110's config keys. `mission report` waits for the commit
   deleting its current holder, per DECISION F274 D2; that holder is in `worker_facade_cmd.py`.
3. `orchestrator_brain.py`'s four edges, measured as live signal reads in `_scrub`, `_review_state`,
   `_gather_signals` and `consult_local_advisor_for_decision` — a surviving module reading cluster
   modules, so a behaviour change rather than a deletion.
4. The four `worker_facade_cmd.py` edges and `worker_registry`'s remaining pair.
5. Draft DECISION F260 D3, the deletion paragraph. R-0832's fix clause binds it.
6. The cluster deletion itself, one commit per module group, NEVER SPLIT ACROSS SESSIONS.
7. T001 — the `Job.id` flip. Then T002 — the classic runner and the resolver collapse.

## Risks

- The map was blind twice and is fixed once: R-0834's file-type blindness is closed, R-0832's
  event-name coupling is OPEN. Treat every "zero edges" reading as a claim about the WALKER.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12.
END PLAN14


BEGIN RECORD14 sha256=fe77ced157d331f2376fae7a8ca563a0d3c45011e7a3e9d8d21bdcf5391b2587 bytes=7886

Gate: F274 R13 — the F274 round 13 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER ITSELF against the COMMITTED blobs, in the primary checkout and in a disposable worktree. Range `64346333`..`f1f50ecd`, eight commits, every one single-parent, in the ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6, with the path set over the range to C5 naming exactly the twelve declared paths. G1 TRANSPORT covers the chain this workflow can walk, per docs/agents/planner_reviewer_prompt.md §3 item 37 and not the emitted bytes: the reviewer's scratch original `.remedy-wt/f274-r13-FINAL.md`, hashed BEFORE delegation, and both committed copies are all 34537 bytes at `cc5af71b9c5ca531b5c84d3238259240dd62cb2ba05c5d173e52711566a4487a`. G2 THE RECORD APPEND at `ede3c2c6`: 589620 to 594390 bytes, prefix exact, post equal to pre plus the slice, N counted as 1, units 233 to 234, ordered equality true, the control at byte offset 589621 rejected by BOTH readers; registrations 69 to 69, resolutions 6 to 6, OPEN SET 63 TO 63 BY DISTINCT ID, `^Gate: ` 43 to 44, `^Gate: F274 R12 ` 0 to 1. G3 THE DECISION APPEND at `67068126`: 905078 to 911446 bytes, exact append, N counted as 14, units 1986 to 2000, control at 905079 rejected by both readers, `^## DECISION F274 D7` 0 to 1. G4: `.agent/plan.md` byte-equal to its slice at 44 lines against the cap of 50, carrying both mandated headings; `.agent/prose_slips.md` 162746 to 163225 as an exact append. G5 THE CUT at `04ff73a7`: every pair's containment reading reproduced exactly as the block recorded it, `true` for P5 and P8 and `false` for the other nine; `worker_recommend` and `worker_recommendation` both total ZERO in `packages/orchestration/dashboard.py` against 3 and 2 at the base, and `worker_recommendation` totals ZERO in `scripts/remedy_smoke.sh` and `tests/ui_server/test_dashboard_contract.py` against 1 and 1; the map goes 38 to 37 lines and 23 to 22 edges with `worker_recommend` at 3 to 2, and its post-image sha256 is `abacf799bc8716ffbfe54a15ff8d1236e13e3dae44f7f322e962a675acb60c00`, WHICH IS THE DIGEST THE BLOCK PREDICTED BEFORE THE ROUND RAN; and `event_schemas.py`, `agent_loop.py`, `autonomy_loop.py` and `worker_recommend.py` are each BYTE-IDENTICAL at the base and at C5, which is the scope guard that proves the round stopped where D7 item 6 says it stops. G6 THE SUITES, each run ALONE by the reviewer in the primary checkout: 28, 74, 3, 191, 26 passed and the canary at 42, `ruff` EXIT 0 over the four touched paths, and the frozen ceiling of DECISION F083 D5 unchanged at 26 errors. G7 THE RED PROOFS, re-run by the reviewer in its own disposable worktree at the round head: the map ratchet gives control EXIT 0 at 3 passed, mutated EXIT 1 with `DISAPPEARED (1)` naming the re-inserted edge, restored EXIT 0; the new guard gives control EXIT 0 at 28 passed, mutated EXIT 1 with `TestDeriveTokenMode::test_one_or_two_tasks_is_compact` as the ONLY failing node id and 27 still green, restored EXIT 0. G8 THE TREE: porcelain empty, `git ls-files .remedy-wt` empty, worktrees 14, per-commit insertions 490, 429, 17, 2, 2, 84 and 44 for C0a through C5, every one under the DECISION F104 D1 cap of 500. ONE DEVIATION WAS DECLARED AND IT IS THE REVIEWER'S OWN DEFECT, sustained: gate G6(b) ordered `tests/ui_server/test_dashboard_contract.py` at 73 passed and 1 skipped, and the primary checkout gives 74 passed and 0 skipped. The worker measured the cause rather than adjusting anything — `test_typescript_compiles` skips if and only if `apps/ui/node_modules/.bin/tsc` is absent, which is true in a fresh worktree and false in the primary checkout — so the block stated a WORKTREE reading for a command its own constraint 8 orders into the PRIMARY CHECKOUT. The reviewer reproduced 74 passed and confirmed the skip condition by reading the test. The gate's ORDERED PROPERTY was EXIT 0 and that held exactly, so the figure is not load-bearing and earns a dated line in `.agent/prose_slips.md` rather than a correction round. THE WORKER ALSO REPORTED A READING THE BLOCK DID NOT ASK FOR AND THE REVIEWER SUSTAINS IT: the literal `^Done: R-\d+ — ` LINE count is 8 while the DISTINCT resolved-id count is 6, because `R-0721` and `R-0725` each carry two resolution paragraphs; both predate this round, the block's numeral was the DISTINCT one that §3 item 10 requires, and the open set is 63 on either reading. ONE FINDING IS REGISTERED BY THIS GATE, R-0836, and it is NOT this round's to fix.

- R-0836 — Medium — THE EVENT-SCHEMA REGISTRY DESCRIBES TWO EVENT KINDS THAT NO PRODUCTION CODE HAS EMITTED SINCE F272 ROUND 19, AND FOUR TESTS PIN THEM THERE, SO NOTHING CAN GO RED WHILE THE PRODUCT'S RULED VOCABULARY DISAGREES WITH WHAT IT ACTUALLY WRITES. Raised by the reviewer at the F274 round 13 gate while authoring round 14, from its own sweep rather than from a reading of the prose, and measured at `f1f50ecd`. THE MEASUREMENT. A repo-wide grep for `agent_loop_cycle_decision` and `agent_loop_stopped` over `packages/`, `apps/`, `tests/` and `scripts/` returns TWELVE sites and NOT ONE of them emits either event: two are the `EVENT_METADATA_SCHEMAS` entries at `packages/orchestration/event_schemas.py` lines 39 and 43, and the other ten are in `tests/orchestration/test_event_ledger.py` at lines 49, 50, 62, 63, 103, 118, 120, 126, 128 and 206 — nine of them assertions and the last a parametrize entry feeding one. THE CAUSE IS ON THE RECORD ALREADY. The `Gate: F272 R19` entry of this ledger records that `_cmd_run_loop` in `apps/cli/commands/job.py` was the SOLE emitter of both kinds, that F272 round 19 deleted it, and that the round correctly deleted the two orphaned `apps/ui/src/api/humanizeCatalog.ts` entries in the same commit — the cockpit half was repaired and the REGISTRY half was not, so the deletion is half-performed on disk. THIS IS NOT R-0832 AND NO SECOND ID IS BEING SPENT ON ONE DEFECT: R-0832 is a SURVIVING reader of an emitter the cluster deletion is ABOUT to remove, and its fix clause binds the map and DECISION F260 D3; this is a registry entry whose emitter is ALREADY GONE, its emitter was a job command rather than a cluster module, and no measurement R-0832 orders would ever reach it. The open set was searched for the defect before this id was minted, per §3 item 30. THE PRODUCT EFFECT, which is why this spends an id under amend0827 rule 2 rather than becoming a prose slip. `validate_event_metadata` returns the empty list for an UNREGISTERED kind and validates a REGISTERED one, so these two entries are unreachable validation that can never fire; a reader of the registry — the file whose own docstring calls it "the single source of truth for what keys each event type must have" — is told the product emits two events it does not; and the tests that assert the entries exist are guards over dead vocabulary, which is exactly why nothing has gone red since. THE FIX, and this finding is NOT resolved by the round that registers it: delete both `EVENT_METADATA_SCHEMAS` entries and the ten test sites that pin them, in one commit, and confirm by the same repo-wide grep reaching ZERO outside that commit's own diff. It is deliberately NOT folded into F274 round 14, whose change set is the two `worker_recommend` loop edges under DECISION F274 D7: this is F272's residue rather than D7's, AGENTS.md Scope Control forbids mixing it in, and a round that deletes a ruled vocabulary deserves its own gate. THE GENERAL LESSON, binding on every later command deletion in this feature and the one the `Gate: F272 R19` deviation half-learned: a round deleting the sole emitter of an event kind sweeps EVERY artefact that names that kind — the cockpit catalog, the action classifier, the schema registry and the tests over all three — because the catalog was the only one a red test made visible, and the registry has no such test by construction.
END RECORD14


BEGIN SLIPS14 sha256=db33a94bb1bcc2202e28459007cd62973acef15f3247a5ceebaaeb213d0171af bytes=685

2026-09-08 · F274 R13 · The round 13 block's gate G6(b) ordered `tests/ui_server/test_dashboard_contract.py` at 73 passed and 1 skipped where the primary checkout gives 74 passed and 0 skipped; the reviewer stated a reading taken in its own dry-run WORKTREE for a command the same block's constraint 8 orders into the PRIMARY CHECKOUT, and `test_typescript_compiles` skips exactly when `apps/ui/node_modules/.bin/tsc` is absent, which is the difference between the two trees. Not load-bearing — the gate's ordered property is EXIT 0 and that held — and the lesson is that a per-suite COUNT measured in a worktree may not be stated for a command ordered in the primary checkout.
END SLIPS14


BEGIN PAIRS14 sha256=8f89acaf1f718acb187d0069cb573f0d857b98b80c5aab814991c432ba72aea1 bytes=8130

--- Q1 FILE packages/orchestration/agent_loop.py
--- Q1 FROM
    # Emit token_policy_applied once at loop start
    from packages.orchestration.token_policy import build_default_token_policy
    from packages.orchestration.worker_recommend import recommend_worker
    _tp = build_default_token_policy(job)
    _initial_events = load_run_events(data_dir, job.id)
    _rec = recommend_worker(job, _initial_events)
    log.log(
        "token_policy_applied",
        outcome="applied",
        mode=_rec.token_mode,
        max_context_tokens=_tp.budget.get("expensive_tokens", 100_000),
        estimated_context_tokens=_rec.estimated_context_tokens,
        local_first=True,
        remote_model_requires_approval=_rec.requires_approval,
        selected_worker=_rec.recommended_worker,
    )
--- Q1 TO
    # Emit token_policy_applied once at loop start
    from packages.orchestration.token_policy import (
        build_default_token_policy,
        derive_token_mode,
    )
    _tp = build_default_token_policy(job)
    log.log(
        "token_policy_applied",
        outcome="applied",
        mode=derive_token_mode(job),
        max_context_tokens=_tp.budget.get("expensive_tokens", 100_000),
        local_first=True,
    )
--- Q2 FILE packages/orchestration/autonomy_loop.py
--- Q2 FROM
    token_mode: str
    selected_worker: str
    readiness_level: int
--- Q2 TO
    token_mode: str
    readiness_level: int
--- Q3 FILE packages/orchestration/autonomy_loop.py
--- Q3 FROM
    from packages.orchestration.stop_reasons import derive_stop_reasons
    from packages.orchestration.worker_recommend import recommend_worker
--- Q3 TO
    from packages.orchestration.stop_reasons import derive_stop_reasons
    from packages.orchestration.token_policy import derive_token_mode
--- Q4 FILE packages/orchestration/autonomy_loop.py
--- Q4 FROM
    # Emit token_policy_applied once at loop start
    _emit_token_policy_applied(job, events)
--- Q4 TO
    # Emit token_policy_applied once at loop start
    _emit_token_policy_applied(job)
--- Q5 FILE packages/orchestration/autonomy_loop.py
--- Q5 FROM
        # Get worker recommendation
        rec = recommend_worker(job, events)

--- Q5 TO
--- Q6 FILE packages/orchestration/autonomy_loop.py
--- Q6 FROM
            token_mode=rec.token_mode,
            selected_worker=rec.recommended_worker,
            readiness_level=readiness_level,
--- Q6 TO
            token_mode=derive_token_mode(job),
            readiness_level=readiness_level,
--- Q7 FILE packages/orchestration/autonomy_loop.py
--- Q7 FROM
def _emit_token_policy_applied(job: Job, events: list[dict[str, Any]]) -> None:
    """Emit token_policy_applied run-log event once at loop start."""
    try:
        from packages.orchestration.run_log import RunLogWriter
        from packages.orchestration.token_policy import build_default_token_policy
        from packages.orchestration.worker_recommend import recommend_worker

        tp = build_default_token_policy(job)
        rec = recommend_worker(job, events)
        log = RunLogWriter(job_id=job.id)
        log.log(
            "token_policy_applied",
            outcome="applied",
            mode=rec.token_mode,
            max_context_tokens=tp.budget.get("expensive_tokens", 100_000),
            estimated_context_tokens=rec.estimated_context_tokens,
            local_first=True,
            remote_model_requires_approval=rec.requires_approval,
            selected_worker=rec.recommended_worker,
        )
--- Q7 TO
def _emit_token_policy_applied(job: Job) -> None:
    """Emit token_policy_applied run-log event once at loop start."""
    try:
        from packages.orchestration.run_log import RunLogWriter
        from packages.orchestration.token_policy import (
            build_default_token_policy,
            derive_token_mode,
        )

        tp = build_default_token_policy(job)
        log = RunLogWriter(job_id=job.id)
        log.log(
            "token_policy_applied",
            outcome="applied",
            mode=derive_token_mode(job),
            max_context_tokens=tp.budget.get("expensive_tokens", 100_000),
            local_first=True,
        )
--- Q8 FILE packages/orchestration/autonomy_loop.py
--- Q8 FROM
                "token_mode": c.token_mode,
                "selected_worker": c.selected_worker,
                "readiness_level": c.readiness_level,
--- Q8 TO
                "token_mode": c.token_mode,
                "readiness_level": c.readiness_level,
--- Q9 FILE packages/orchestration/event_schemas.py
--- Q9 FROM
    "token_policy_applied": frozenset({
        "mode", "max_context_tokens", "estimated_context_tokens",
        "local_first", "remote_model_requires_approval",
        "selected_worker",
    }),
--- Q9 TO
    # DECISION F274 D7: the three fields worker recommendation produced die with
    # it — the cluster-bound context pack and the adapter scoring both go.
    "token_policy_applied": frozenset({
        "mode", "max_context_tokens", "local_first",
    }),
--- Q10 FILE tests/storage/test_persistence.py
--- Q10 FROM
        required = {
            "mode", "max_context_tokens", "estimated_context_tokens",
            "local_first", "remote_model_requires_approval", "selected_worker",
        }
--- Q10 TO
        required = {"mode", "max_context_tokens", "local_first"}
--- Q11 FILE tests/storage/test_persistence.py
--- Q11 FROM
        assert len(schema) == 6
        assert "mode" in schema
        assert "max_context_tokens" in schema
        assert "estimated_context_tokens" in schema
        assert "local_first" in schema
        assert "remote_model_requires_approval" in schema
        assert "selected_worker" in schema
--- Q11 TO
        assert len(schema) == 3
        assert "mode" in schema
        assert "max_context_tokens" in schema
        assert "local_first" in schema
--- Q12 FILE tests/storage/test_persistence.py
--- Q12 FROM
        required = {"mode", "max_context_tokens", "estimated_context_tokens",
                     "local_first", "remote_model_requires_approval", "selected_worker"}
--- Q12 TO
        required = {"mode", "max_context_tokens", "local_first"}
--- Q13 FILE tests/storage/test_persistence.py
--- Q13 FROM
        valid_meta = {
            "mode": "compact",
            "max_context_tokens": 100000,
            "estimated_context_tokens": 500,
            "local_first": True,
            "remote_model_requires_approval": True,
            "selected_worker": "ollama/qwen3:8b",
        }
--- Q13 TO
        valid_meta = {
            "mode": "compact",
            "max_context_tokens": 100000,
            "local_first": True,
        }
--- Q14 FILE tests/storage/test_persistence.py
--- Q14 FROM
        assert len(schema) == 6
        expected = {"mode", "max_context_tokens", "estimated_context_tokens",
                    "local_first", "remote_model_requires_approval", "selected_worker"}
--- Q14 TO
        assert len(schema) == 3
        expected = {"mode", "max_context_tokens", "local_first"}
--- Q15 FILE scripts/remedy_smoke.sh
--- Q15 FROM
for key in ['mode', 'max_context_tokens', 'estimated_context_tokens',
            'local_first', 'remote_model_requires_approval', 'selected_worker']:
    if key not in meta:
        print('ERROR: token_policy_applied missing ' + key, file=sys.stderr)
        sys.exit(1)
print('    token_policy_applied: OK (worker=' + str(meta['selected_worker']) + ', mode=' + str(meta['mode']) + ')')
--- Q15 TO
for key in ['mode', 'max_context_tokens', 'local_first']:
    if key not in meta:
        print('ERROR: token_policy_applied missing ' + key, file=sys.stderr)
        sys.exit(1)
print('    token_policy_applied: OK (mode=' + str(meta['mode']) + ')')
--- Q16 FILE tests/orchestration/cluster_deletion_map.txt
--- Q16 FROM
packages.orchestration.worker_recommend <- packages/orchestration/agent_loop.py
packages.orchestration.worker_recommend <- packages/orchestration/autonomy_loop.py
packages.orchestration.worker_registry <- packages/orchestration/token_economy.py
--- Q16 TO
packages.orchestration.worker_registry <- packages/orchestration/token_economy.py
END PAIRS14
