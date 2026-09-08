STEP — F274 ROUND 15 — fix R-0836: delete the two event kinds nothing has emitted since F272 round 19

Goal: finish a deletion F272 left half-performed. `packages/orchestration/event_schemas.py` registers
`agent_loop_cycle_decision` and `agent_loop_stopped`, and `tests/orchestration/test_event_ledger.py`
pins both there, while NO production code has emitted either since F272 round 19 deleted their sole
emitter `_cmd_run_loop`. That round repaired the cockpit half — it deleted the two orphaned
`humanizeCatalog.ts` entries — and left the registry half standing. This round deletes both entries
and the sites that pin them. Also book round 14's PASS verdict, book a RECURRENCE of R-0819 for a
per-pair count two of that block's pairs could not meet, and RESOLVE R-0836 in this same round.

Base commit for every reading in this block: `ea0d78c4`.

NO CLUSTER MODULE AND NO EDGE MOVES THIS ROUND, and gate G8 proves it:
`tests/orchestration/cluster_deletion_map.txt` is byte-identical at the base and at C3.

WHAT THE REVIEWER RAN BEFORE AUTHORING. The whole change was applied in a disposable worktree at the
base commit above, and every gate below plus both red proofs was run against the applied tree.

THE COUNTER-MEASURE THE R-0819 RECURRENCE ADDS WAS APPLIED TO THIS BLOCK BEFORE IT WAS EMITTED, which
is why gate G4(a) can order a per-pair TO count here and round 14's could not. The reviewer grouped
this block's TO blocks BY TARGET FILE and compared them for byte equality: `event_schemas.py` holds
one pair, `test_event_ledger.py` holds five, and NO two TO blocks in either group are byte-identical.
It then applied all six pairs to the committed base in memory and measured each pair in the
POST-image, getting FROM 0 and TO 1 for every one. Both readings are what G4(a) orders back.

FRAME CONVENTION. Every slice is delimited by a line reading `BEGIN <NAME> sha256=<hex> bytes=<n>`
and a line reading `END <NAME>`; the slice is the bytes BETWEEN those two lines, its leading newline
included, and marker lines never reach any file. No line of this block's FRAME — every line outside a
BEGIN/END pair — is a run of a single repeated character.


## Bundle — the commits of this round, in this order

C0a  Save this block verbatim as `.agent/authored/f274-r15.md`.
C0b  Mirror the same bytes into `.agent/last_block.md`.
C1   Replace `.agent/plan.md` with the PLAN15 slice.
C2   Append the RECORD15 slice to `.agent/live_review.md` — books round 14's PASS verdict and the
     R-0819 RECURRENCE.
C3   THE FIX: apply the pairs of PAIRS15. ONE commit.
C4   Append the RESOLVE15 slice to `.agent/live_review.md` — the authored `Done: R-0836`.
C5   The handback: rewrite `.agent/handoff.md`, then push.

C1 is the first substantive commit because this round touches the finding ledger and the plan must be
current before every commit (§3 item 23). C2 precedes C3 because findings persist FIRST (§4 item 4).


## Change set — these paths and nothing else

  .agent/authored/f274-r15.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/handoff.md
  packages/orchestration/event_schemas.py
  tests/orchestration/test_event_ledger.py


## C3 — the fix

PAIRS15 carries the pairs. `--- S<n> FILE <path>` opens a pair, `--- S<n> FROM` opens its FROM block
and `--- S<n> TO` opens its TO block; a block is every following line up to the next marker. Replace
each FROM block with its TO block, once, keeping line endings. Marker lines reach no file.

PAIR SHAPES, MEASURED MECHANICALLY AND NOT BY EYE. The reviewer ran the containment test on every
pair at the base commit and records the output rather than a label: every pair printed
`TO contains FROM: false`, so EVERY pair here is a REWRITE and none carries the §4.9 append
obligation. At that same commit each FROM block occurs EXACTLY ONCE in its file.

WHAT EACH PAIR DOES, because four of the six are not simple deletions. S1 deletes both registry
entries, spanning forward to the `context_budget_optimized` line that follows them. S2 drops the two
membership assertions and adds one for `token_policy_applied`, so the test still asserts something
the product really writes. S3 re-points `test_different_schemas_for_different_events` at three LIVE
kinds. S4 re-points the `get_event_schema` probe at `agent_loop_started`. S5 deletes the two whole
test methods that existed only to describe the dead schemas, spanning forward to the `def
test_forbidden_strings` line that follows them. S6 re-points a scope SAMPLE.

S6 IS THE ONE PAIR THE FINDING DID NOT STRICTLY REQUIRE, and the block says so rather than widening
its scope silently. `_normalize_event` derives an event's scope from its PREFIX, not from the
registry, so that sample would have stayed green untouched. It is changed because a sample naming an
event the product no longer writes is the stale-prose class R-0835 recorded, and the RESOLVE15 slice
records the refinement against the registration's own wording.


## Constraints

1. Apply every slice BYTE FOR BYTE. Do not reflow, retype or re-indent one. If something looks wrong,
   apply it as given and DECLARE the doubt in the handback.
2. RECORD15 and RESOLVE15 are APPENDS: the target's existing bytes are a byte-exact PREFIX of the
   result and the slice is an exact SUFFIX. Each carries its OWN leading newline — ADD NO SEPARATOR
   of your own. PLAN15 replaces `.agent/plan.md` entirely. PAIRS15 is appended to no file.
3. The path set of C0a..C4 is exactly the "Change set" paths other than `.agent/handoff.md`, at C5.
4. COMMIT ORDER IS LOAD-BEARING AND THIS CONSTRAINT IS WHAT MAKES THE RESOLUTION TRUE. C3, the fix,
   is committed BEFORE C4, the commit that writes `Done: R-0836`. That paragraph asserts a fact about
   this round's OWN landed change, and under §3 item 20 such a claim names the ordering constraint
   fixing its commit rather than a SHA that cannot exist when the text is authored. This is it.
5. Any destructive check runs ONLY inside a disposable `git worktree`, never in the primary checkout,
   which satisfies `git status --porcelain` == empty at every commit boundary; prune each worktree.
6. Do not write a `Done:` paragraph of your own. RESOLVE15 is the reviewer-authored resolution; apply
   it verbatim and add nothing.
7. Every gate runs at a commit STRICTLY EARLIER than C5, so the handback can quote each. Run G5 in
   the PRIMARY CHECKOUT: `apps/ui/node_modules` and `apps/ui/dist` are gitignored, so npm-backed
   tests in a fresh worktree fail on the missing build, not on this round. Do not report C5's own
   insertion count; the reviewer measures it at the next gate.
8. READING A COMMITTED BLOB, since several gates measure one: `git show <commit>:<path>` into memory
   or scratch under the gitignored `.remedy-wt/`, or a disposable worktree. NEVER overwrite-restore.
9. EVERY SUITE COUNT BELOW WAS MEASURED IN THE REVIEWER'S DRY-RUN WORKTREE, so it is a REFERENCE and
   the ordered property is the EXIT CODE. Report the number YOUR run produces and say so if it
   differs; round 13's block stated a worktree count for a primary-checkout command and was wrong.


## Done when — the gates, one line per gate in the handback

G1  TRANSPORT, at C0b. `sha256` of the committed `.agent/authored/f274-r15.md` equals `sha256` of the
    committed `.agent/last_block.md`, and both equal the digest the delegation message states. Report
    the digest you measured. Per §3 item 37 this covers those artefacts and is not a claim about the
    bytes emitted into a prompt.

G2  THE VERDICT APPEND, at C2, re-derived from the COMMITTED blobs.
    (a) BYTES: `.agent/live_review.md` 602276 -> 607839; pre-image a byte-exact PREFIX; post-image
        equal to pre plus the RECORD15 slice — that second clause is the BYTE reader, the prefix
        clause alone being blind to a flip inside the appended region.
    (b) STRUCTURE over the WHOLE appended region: a unit is a maximal run of consecutive non-empty
        lines; COUNT N from the slice and REPORT it; the file's last N units equal the slice's units
        IN ORDER and everything before is unchanged. Units 236 -> 238.
    (c) NEGATIVE CONTROL: flip the byte at ZERO-INDEXED offset 602277 of the post-image — the `G`
        opening the FIRST appended paragraph, not the last — and confirm the BYTE reader of (a) and
        the STRUCTURAL reader of (b) each reject it.
    (d) COUNTS: registrations 70 -> 70, distinct resolutions 6 -> 6, OPEN SET 64 -> 64 BY DISTINCT
        ID, `^Gate: ` 45 -> 46, `^Gate: F274 R14 ` 0 -> 1. G7 is what moves the open set.

G3  THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to the PLAN15 slice, is 42 lines against the cap
    of 50, and carries both `## Goal` and `## Next Steps`.

G4  THE FIX, at C3, measured against the COMMITTED blobs.
    (a) THE PAIRS: for each of the six, the FROM block occurs ZERO times in its file and the TO block
        EXACTLY ONCE. Both halves are reachable here — see the counter-measure paragraph above, which
        measured them before this gate was written. Report twelve numbers.
    (b) THE SWEEP: `git grep -E 'agent_loop_cycle_decision|agent_loop_stopped' -- packages apps tests
        scripts docs` finds NO MATCH and exits 1, against twelve sites at the base. `.agent/` is
        deliberately outside the sweep: the ledger and this block both name the two kinds and must.
    (c) THE REGISTRY, read BY IMPORTING the module rather than by grepping the source: neither kind
        is a key of `EVENT_METADATA_SCHEMAS`, `get_event_schema` returns None for both, and the keys
        that DO survive still include `agent_loop_started`, `context_budget_optimized` and
        `token_policy_applied`.
    (d) Both touched files still parse under `ast`, and `git diff --name-only ea0d78c4..<C3>` names
        exactly those two paths.

G5  THE SUITES, at C3, in the primary checkout per constraint 7. RUN EACH COMMAND ALONE and report
    its own number, per constraint 9. Prefix each path with `python3 -B -m pytest` and suffix `-q`.
    (a) EACH OF THESE EXIT 0, with the reviewer's own worktree count in brackets:
        `tests/orchestration/test_event_ledger.py` [19, down from 21 because two whole test methods
        are deleted], `tests/storage/test_persistence.py` [26],
        `tests/orchestration/test_autonomy.py` [81], `tests/orchestration/test_project_brain.py` [82],
        `tests/orchestration/test_import_reachability.py` [3], and THE CANARY
        `tests/cli/test_golden_path.py` [42, measured at round 13].
    (b) `python3 -m ruff check packages/orchestration/event_schemas.py
        tests/orchestration/test_event_ledger.py` EXIT 0, and `python3 -m ruff check .` REPORTS 26
        ERRORS, unchanged, so DECISION F083 D5's frozen ceiling is untouched; that command EXITS 1
        while reporting them, which is the gate PASSING, the ceiling being 26 and not 0.

G6  THE RED PROOFS, in a disposable worktree at C3 per constraint 5, each run with its UNMUTATED
    control FIRST in that same worktree, so a colour has a baseline.
    (a) THE SWEEP GATE CAN FAIL, which is what makes G4(b) evidence rather than decoration. Control:
        the G4(b) command exits 1 with no match. Then insert an `"agent_loop_stopped"` entry into
        `EVENT_METADATA_SCHEMAS` in `packages/orchestration/event_schemas.py`, directly above its
        `    "context_budget_optimized": frozenset({` line — that line occurs ONCE in that file at C3
        — and confirm the same command now EXITS 0 and names that file. Restore and confirm exit 1.
    (b) THE REWRITTEN ASSERTIONS BIND rather than merely pass. Control:
        `tests/orchestration/test_event_ledger.py` EXIT 0. Then delete the whole
        `"token_policy_applied"` entry from `EVENT_METADATA_SCHEMAS` — the three-line block from
        `    "token_policy_applied": frozenset({` to its closing `    }),`, which occurs ONCE in that
        file at C3 — and confirm EXIT 1 with BOTH `TestEventSchemaRegistry::test_schemas_exist` and
        `TestEventSchemaRegistry::test_different_schemas_for_different_events` failing, which are
        exactly the two tests S2 and S3 rewrote. Restore, confirm EXIT 0, report the ids.

G7  THE RESOLUTION APPEND, at C4, re-derived from the COMMITTED blobs, and it runs at a commit LATER
    than C3 so the paragraph it lands is true when it lands.
    (a) BYTES: `.agent/live_review.md` 607839 -> 609858; prefix exact; post equal to pre plus the
        RESOLVE15 slice.
    (b) STRUCTURE, N counted from the slice and REPORTED: units 238 -> 239, the last N units equal
        the slice's units IN ORDER, everything before unchanged.
    (c) NEGATIVE CONTROL at zero-indexed offset 607840 — the `D` opening the appended paragraph —
        rejected by both readers.
    (d) COUNTS: distinct resolutions 6 -> 7, OPEN SET 64 -> 63 BY DISTINCT ID, `^Done: R-0836 — `
        0 -> 1. The round opens at 64 and closes at 63, having resolved exactly one finding.

G8  THE TREE AND THE SCOPE GUARD, at C4. `git status --porcelain` EMPTY; `git ls-files .remedy-wt`
    EMPTY; `git worktree list` the same count as before your first worktree and after your last
    prune; every commit C0a through C4 single-parent. Report each commit's INSERTION count; the
    reviewer measured C3's applied change as 8 insertions and 34 deletions over two files, against
    the DECISION F104 D1 cap of 500. AND THE SCOPE GUARD:
    `tests/orchestration/cluster_deletion_map.txt` is BYTE-IDENTICAL at the base and at C4 — report
    the sha256 you measured for both — and no file under `packages/orchestration/` other than
    `event_schemas.py` changed in the range. Read `.agent/STOP` at the round's start, before C3 and
    after C5, reporting all three.


## Handback — rewrite `.agent/handoff.md` at C5, then push

Carry the mandated sections of `docs/agents/handback_template.md`: the state block, the commits table
with its `+/-` column from `git diff --numstat`, the changed-files table, ONE LINE PER GATE G1
through G8 with its real result, the deviations, the open-findings count and the next expected
action. No length cap. Name the SESSION NUMBER as SESSION 6 of feature F274 and the round as 15,
state the open-findings count as the number G7(d) MEASURED, and add the one sentence of context
self-assessment amend0905-throughput requires. DECLARE, do not silently repair: report the real
command, the real exit code and the real output, and say what you did.


BEGIN PLAN15 sha256=f33facfa1a64da6167d48cd6b84ac68acafa7688fdfaa27ea0fd5a786eaa090b bytes=2468
# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Finish what F272 could not reach inside its own limit: the prototype cluster deletion and the
classic-to-unified record flip DECISION F272 D15 measured as ATOMIC. DECISION
amend0907-cluster-first D1 reorders the slices so the deletion runs FIRST.

## Current Step

Round 15, the R-0836 fix: delete the `agent_loop_cycle_decision` and `agent_loop_stopped` entries of
`EVENT_METADATA_SCHEMAS` and the sites in `tests/orchestration/test_event_ledger.py` that pin them.
Their sole emitter died with `_cmd_run_loop` in F272 round 19, so the registry has been describing
two events the product does not write; this finishes that deletion. Book round 14's PASS verdict and
a RECURRENCE of R-0819 for a per-pair count two of that block's pairs could not meet, and resolve
R-0836 in this same round. No cluster module and no edge moves.

## Next Steps

1. The two carry-overs F260's Design names: overnight readiness to `mission readiness`, and the
   route-policy knobs checked against F110's config keys. `mission report` waits for the commit
   deleting its current holder, per DECISION F274 D2; that holder is in `worker_facade_cmd.py`.
2. `orchestrator_brain.py`'s four edges, measured as live signal reads in `_scrub`, `_review_state`,
   `_gather_signals` and `consult_local_advisor_for_decision` — a surviving module reading cluster
   modules, so a behaviour change rather than a deletion.
3. The four `worker_facade_cmd.py` edges and `worker_registry`'s remaining pair.
4. Draft DECISION F260 D3, the deletion paragraph. R-0832's fix clause binds it, and it must name
   the event-name couplings the import map cannot see.
5. The cluster deletion itself, one commit per module group, NEVER SPLIT ACROSS SESSIONS.
   `worker_recommend` is already edge-free and goes with that round.
6. T001 — the `Job.id` flip. Then T002 — the classic runner and the resolver collapse.

## Risks

- The map was blind twice and is fixed once: R-0834's file-type blindness is closed, R-0832's
  event-name coupling is OPEN. Treat every "zero edges" reading as a claim about the WALKER.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12.
END PLAN15


BEGIN RECORD15 sha256=c0719cac0a7a574d2d7a31a17638bb107d2d6dc54b5f373ee1a5cfa2649bdf50 bytes=5563

Gate: F274 R14 — the F274 round 14 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER ITSELF against the COMMITTED blobs, in the primary checkout and in a disposable worktree. Range `f1f50ecd`..`ea0d78c4`, seven commits, every one single-parent, in the ordered sequence C0a, C0b, C1, C2, C3, C4, C5, with the path set over the range to C4 naming exactly the eleven declared paths. G1 TRANSPORT covers the chain this workflow can walk, per §3 item 37: the reviewer's scratch original `.remedy-wt/f274-r14-FINAL.md`, hashed BEFORE delegation, and both committed copies are all 35305 bytes at `445b54f35bdf5f4f9fc3b58d7fe413027ea7b5bdd3d51c079421d5e4beff0dc9`. G2 THE RECORD APPEND at `4bfb8001`: 594390 to 602276 bytes, exact append, N counted as 2, units 234 to 236, ordered equality true, the control at byte offset 594391 rejected by BOTH readers; registrations 69 to 70, distinct resolutions 6 to 6, OPEN SET 63 TO 64 BY DISTINCT ID, `^Gate: ` 44 to 45, `^Gate: F274 R13 ` 0 to 1, `^- R-0836 — ` 0 to 1. G3: `.agent/plan.md` byte-equal to its slice at 46 lines against the cap of 50; `.agent/prose_slips.md` 163225 to 163910 as an exact append. G4 THE CUT at `e3d87b25`: every pair reads FROM 0; `worker_recommend` and `selected_worker` both total ZERO in `agent_loop.py` and `autonomy_loop.py`, and `selected_worker` totals ZERO in `tests/storage/test_persistence.py` and `scripts/remedy_smoke.sh` and ONE in `event_schemas.py`, exactly as the block predicted; `EVENT_METADATA_SCHEMAS["token_policy_applied"]` read BY IMPORT holds exactly the three keys `local_first`, `max_context_tokens` and `mode`; and the map goes 37 to 35 lines and 22 to 20 edges with `worker_recommend` at 2 to 0 and the cluster modules holding an edge at 12 to 11, its post-image sha256 `7fbf3909fd6d094e0ab3654e8842222a1adf6a51cd6c74bf119b1f7c256d5155` being THE DIGEST THE BLOCK PREDICTED BEFORE THE ROUND RAN. G5 LINT: EXIT 0 over the four touched paths and the frozen ceiling of DECISION F083 D5 unchanged at 26. G6 THE SUITES, each run ALONE: 26, 81, 21, 3, 3, 191, 28 and the canary at 42, every figure the block's reference; AND THE FULL SUITE IN THE REVIEWER'S OWN RUN IN THE PRIMARY CHECKOUT, EXIT 0 at 19769 passed, 23 skipped and 0 failed, which reconciles exactly with the 19765 the round 12 gate measured plus the four tests round 13 added. G7 THE RED PROOFS, re-run by the reviewer in its own disposable worktree at the round head: the registry-versus-emitter proof gives control EXIT 0 at 26 passed, mutated EXIT 1 with `TestTokenPolicyAppliedSchema::test_autonomy_loop_emits` as the SOLE failing node id and `extra keys ['selected_worker']` as the message, restored EXIT 0; the map ratchet gives control EXIT 0 at 3 passed, mutated EXIT 1 with `DISAPPEARED (2)` naming both re-inserted edges, restored EXIT 0. G8 THE TREE: porcelain empty, `git ls-files .remedy-wt` empty, worktrees 14, per-commit insertions 490, 397, 12, 4, 2 and 24 for C0a through C4, every one under the DECISION F104 D1 cap of 500. THE FEATURE'S POSITION AFTER THIS ROUND: `packages.orchestration.worker_recommend` holds NO recorded consumer edge and is deletable, and the cluster modules with no edge at all go from twelve to thirteen. FOUR DEVIATIONS WERE DECLARED AND THE REVIEWER SUSTAINS ALL FOUR; the first is the reviewer's own defect and is booked as the R-0819 recurrence below. ONE FINDING WAS REGISTERED BY THE ROUND THIS GATE COVERS, R-0836, and it is resolved later in the round this entry is written in.

RECURRENCE of R-0819 at F274 round 14, measured by the reviewer at `ea0d78c4`. NO NEW ID IS SPENT: §3 item 30 requires the open set searched for the DEFECT before an id is minted, and R-0819 is OPEN with the headline "A GATE OVER PRODUCTION CODE DEMANDED ZERO OF A CONDITION THAT IS ALREADY NON-ZERO AT ITS OWN BASE", which is this class exactly — a gate ordering a value no correct run can produce. THE INSTANCE. The round 14 block's gate G4(a) ordered, for every one of its sixteen pairs, that "the FROM block occurs ZERO times in its file and the TO block EXACTLY ONCE". Pairs Q10 and Q12 have BYTE-IDENTICAL TO blocks — both are the single line `        required = {"mode", "max_context_tokens", "local_first"}` — and both land in `tests/storage/test_persistence.py`, so the post-image count for each is TWO and can never be one. Q5's TO block is EMPTY by design, being a deletion, so the clause is undefined for it rather than merely unmeetable. THE CAUSE IS NEW AND IS WHAT THIS RECURRENCE ADDS. The reviewer DID apply the whole change in a worktree before authoring and DID run a mechanical containment test over every pair — the counter-measure R-0819's own fix clause requires, and the one the round 12 recurrence added — but that test measured each pair's FROM against the PRE-image and never measured the TO blocks against EACH OTHER. A per-pair reading cannot see a collision between two pairs, because the property that fails is a property of the SET. THE ADDITION TO R-0819's FIX, binding on every later block of this feature that orders a per-pair count: before ordering "the TO block occurs EXACTLY ONCE", group the block's TO blocks BY TARGET FILE and compare them for byte equality; where two coincide, order the count they can actually meet or drop the clause and rely on the FROM-zero half, which is unaffected. THE ROUND LOST NOTHING: FROM 0 held for all sixteen pairs, the independent zero-gate G4(b) proved the old vocabulary gone, and the worker reported the real numbers and declared the gap rather than adjusting anything.
END RECORD15


BEGIN PAIRS15 sha256=279db4e3bc54686c32f083914559d8befe3f5e5bb0b11b278afff6bb3e7e0dea bytes=3165

--- S1 FILE packages/orchestration/event_schemas.py
--- S1 FROM
    "agent_loop_cycle_decision": frozenset({
        "cycle", "decision", "reason", "next_action", "blocked_by",
        "token_mode", "selected_worker", "readiness_level",
    }),
    "agent_loop_stopped": frozenset({
        "final_decision", "stop_reason", "cycles_run",
        "unresolved_blocker_count",
    }),
    "context_budget_optimized": frozenset({
--- S1 TO
    "context_budget_optimized": frozenset({
--- S2 FILE tests/orchestration/test_event_ledger.py
--- S2 FROM
        assert "agent_loop_started" in EVENT_METADATA_SCHEMAS
        assert "agent_loop_cycle_decision" in EVENT_METADATA_SCHEMAS
        assert "agent_loop_stopped" in EVENT_METADATA_SCHEMAS
        assert "context_budget_optimized" in EVENT_METADATA_SCHEMAS
--- S2 TO
        assert "agent_loop_started" in EVENT_METADATA_SCHEMAS
        assert "context_budget_optimized" in EVENT_METADATA_SCHEMAS
        assert "token_policy_applied" in EVENT_METADATA_SCHEMAS
--- S3 FILE tests/orchestration/test_event_ledger.py
--- S3 FROM
        started = EVENT_METADATA_SCHEMAS["agent_loop_started"]
        decision = EVENT_METADATA_SCHEMAS["agent_loop_cycle_decision"]
        stopped = EVENT_METADATA_SCHEMAS["agent_loop_stopped"]
        assert started != decision, "started and decision must differ"
        assert decision != stopped, "decision and stopped must differ"
        assert started != stopped, "started and stopped must differ"
--- S3 TO
        started = EVENT_METADATA_SCHEMAS["agent_loop_started"]
        budget = EVENT_METADATA_SCHEMAS["context_budget_optimized"]
        policy = EVENT_METADATA_SCHEMAS["token_policy_applied"]
        assert started != budget, "started and budget must differ"
        assert budget != policy, "budget and policy must differ"
        assert started != policy, "started and policy must differ"
--- S4 FILE tests/orchestration/test_event_ledger.py
--- S4 FROM
        assert get_event_schema("agent_loop_stopped") is not None
--- S4 TO
        assert get_event_schema("agent_loop_started") is not None
--- S5 FILE tests/orchestration/test_event_ledger.py
--- S5 FROM
    def test_agent_loop_cycle_decision_schema(self):
        from packages.orchestration.event_schemas import EVENT_METADATA_SCHEMAS
        schema = EVENT_METADATA_SCHEMAS["agent_loop_cycle_decision"]
        assert len(schema) == 8
        assert "next_action" in schema
        assert "blocked_by" in schema
        assert "readiness_level" in schema

    def test_agent_loop_stopped_schema(self):
        from packages.orchestration.event_schemas import EVENT_METADATA_SCHEMAS
        schema = EVENT_METADATA_SCHEMAS["agent_loop_stopped"]
        assert len(schema) == 4
        assert "final_decision" in schema
        assert "stop_reason" in schema
        assert "cycles_run" in schema
        assert "unresolved_blocker_count" in schema

    def test_forbidden_strings(self):
--- S5 TO
    def test_forbidden_strings(self):
--- S6 FILE tests/orchestration/test_event_ledger.py
--- S6 FROM
            ("agent_loop_cycle_decision", "agent"),
--- S6 TO
            ("agent_loop_started", "agent"),
END PAIRS15


BEGIN RESOLVE15 sha256=21e3cf850c2935164c7fa0fd2e35c98a76e8dfc94929a336bcf539ffe64afb89 bytes=2019

Done: R-0836 — RESOLVED in F274 round 15, in the commit this round's own constraint fixes immediately before the commit that writes this paragraph. Both `EVENT_METADATA_SCHEMAS` entries are deleted from `packages/orchestration/event_schemas.py`, and the sites in `tests/orchestration/test_event_ledger.py` that pinned them are gone with them: the two membership assertions, the two whole test methods `test_agent_loop_cycle_decision_schema` and `test_agent_loop_stopped_schema`, and the `get_event_schema` probe are removed or re-pointed at a SURVIVING kind, and `test_different_schemas_for_different_events` now compares `agent_loop_started`, `context_budget_optimized` and `token_policy_applied`, which the product really writes. THE VERIFICATION IS A SWEEP AND A DISCRIMINATOR, not an inspection. A repo-wide `git grep` for `agent_loop_cycle_decision` and `agent_loop_stopped` over `packages/`, `apps/`, `tests/`, `scripts/` and `docs/` returns NO MATCH, against twelve sites before; and the sweep is shown to be capable of failing, because re-inserting one entry into the registry makes that same grep find it again. The rewritten assertions are shown to BIND rather than merely pass: deleting `token_policy_applied` from the registry reds exactly `test_schemas_exist` and `test_different_schemas_for_different_events`, the two the fix rewrote. `tests/orchestration/test_event_ledger.py` goes from 21 tests to 19, which is the two dead-vocabulary tests removed and no other loss. ONE REFINEMENT OF THE REGISTRATION IS RECORDED HERE RATHER THAN LEFT SILENT: the fix clause said "the ten test sites that pin them", and the site at line 206 was NOT a pin — it is a sample in `test_scope_derivation`, which reads a prefix rather than the registry and would have stayed green untouched. It was changed to `agent_loop_started` anyway, because a scope sample naming an event the product no longer writes is the same stale-prose class R-0835 recorded, and the round says so rather than quietly widening its own scope.
END RESOLVE15
