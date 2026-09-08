STEP — F274 ROUND 13 — rule DECISION F274 D7, then cut the first of `worker_recommend`'s three edges

Goal: rule what happens to worker recommendation before a line moves, then cut the one of its three
edges that emits no run-log event. D7 rules that nothing inherits worker recommendation, that the
token mode never belonged to it and moves to `packages/orchestration/token_policy.py`, and that the
`token_policy_applied` vocabulary is ruled DOWN explicitly rather than by omission. This round lands
`derive_token_mode` with its guard, deletes the dashboard's `worker_recommendation` section with the
two pins holding it, removes the one map line its cut retires, and books round 12's PASS verdict and
the prose slip round 12 owed. THE TWO LOOP EDGES DO NOT MOVE and
`packages/orchestration/event_schemas.py` is untouched — that is the next round, per D7 item 6.

Base commit for every reading in this block: `64346333`.

WHY THE REVIEWER RULED BEFORE ORDERING. Rounds 9 through 12 cut read-only views; every remaining
edge is live runtime code. The reviewer applied this entire change in a disposable worktree at the
base commit above and ran every gate below and both red controls against the applied tree BEFORE
authoring this block, so every numeral here was read off the applied tree rather than off the script
that produced it — the clause the R-0819 recurrence added at round 12. That reading settled the one
guard prose would have missed: `Worker:` is asserted twice in `tests/cli/test_cli_ux.py`, and both
assertions read `_cmd_do_report`'s ping-pong report rather than the dashboard, so deleting the
dashboard's `Worker:` line cannot reach them.

FRAME CONVENTION. Every slice is delimited by a line reading `BEGIN <NAME> sha256=<hex> bytes=<n>`
and a line reading `END <NAME>`; the slice is the bytes BETWEEN those two lines, its leading
newlines included, and marker lines never reach any file. NO LINE OF THIS BLOCK'S FRAME — every line
outside a BEGIN/END pair — is a run of a single repeated character. Inside a slice one such run
occurs, the closing `"""` of TOKENMODE's docstring; it is recoverable rather than ambiguous because
its slice carries a byte count and a digest, which is what §3 item 37 asks for.


## Bundle — the commits of this round, in this order

C0a  Save this block verbatim as `.agent/authored/f274-r13.md`.
C0b  Mirror the same bytes into `.agent/last_block.md`.
C1   Replace `.agent/plan.md` with the PLAN13 slice.
C2   Append the RECORD13 slice to `.agent/live_review.md` — books round 12's PASS verdict.
C3   Append the SLIPS13 slice to `.agent/prose_slips.md`.
C4   Append the DECIDE13 slice to `.agent/decisions.md` — DECISION F274 D7.
C5   THE CUT: apply the pairs of PAIRS13, append TOKENMODE to
     `packages/orchestration/token_policy.py` and TESTS13 to `tests/test_token_policy.py`.
C6   The handback: rewrite `.agent/handoff.md`, then push.

C1 is the first substantive commit because this round touches the finding ledger and the plan must be
current before every commit (docs/agents/planner_reviewer_prompt.md §3 item 23). C4 precedes C5
because D7 is the ruling the cut executes, and TOKENMODE's docstring cites it by name.


## Change set — these paths and nothing else

  .agent/authored/f274-r13.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/prose_slips.md
  .agent/decisions.md
  .agent/handoff.md
  packages/orchestration/dashboard.py
  packages/orchestration/token_policy.py
  tests/test_token_policy.py
  tests/ui_server/test_dashboard_contract.py
  tests/orchestration/cluster_deletion_map.txt
  scripts/remedy_smoke.sh


## C5 — the cut: the pairs of PAIRS13, then the two appends

PAIRS13 carries the pairs. `--- P<n> FILE <path>` opens a pair, `--- P<n> FROM` opens its FROM block
and `--- P<n> TO` opens its TO block; a block is every following line up to the next marker. Replace
each FROM block with its TO block, once, keeping line endings. Marker lines reach no file. Four
pairs DELETE and each spans a forward anchor, so no trailing blank line is ambiguous.

PAIR SHAPES, MEASURED MECHANICALLY AND NOT BY EYE. The reviewer ran the containment test on every
pair at the base commit and records each pair's own output rather than one reading generalised to
the rest: `TO contains FROM: true` for P5 and P8, `TO contains FROM: false` for P1, P2, P3, P4, P6,
P7, P9, P10 and P11. So P5 and P8 are APPEND-shaped and owe the §4.9 append obligation rather than a
FROM-zero count, and every pair reading `false` is a REWRITE. P6 is the one to read twice: its TO
looks like an append of `, RunState`, but the FROM block ends in a newline the TO does not contain.
At that commit each FROM block occurs EXACTLY ONCE in its file; every pair was
measured. TOKENMODE and TESTS13 each carry TWO leading newlines, landing two blank lines below the
last definition of its file as PEP 8 requires; the byte count and digest in each BEGIN marker fix
that exactly, so add and remove no newline.

DELIBERATELY NOT DONE, so it does not read as an omission. `event_schemas.py` keeps all six
`token_policy_applied` keys, because both emitters still write all six and D7 item 4 requires the
registry to change in the same commit as the last emitter that drops one. `worker_recommend.py` is
NOT deleted: it keeps two recorded edges and two cluster-internal consumers, and dies with the
cluster. Nothing under `apps/ui/` is touched, because the event KIND is unchanged.


## Constraints

1. Apply every slice BYTE FOR BYTE. Do not reflow, retype or re-indent one. If something looks
   wrong, apply it as given and DECLARE the doubt in the handback.
2. RECORD13, SLIPS13, DECIDE13, TOKENMODE and TESTS13 are APPENDS: the target's existing bytes are a
   byte-exact PREFIX of the result and the slice is an exact SUFFIX. Each carries its OWN leading
   newlines — ADD NO SEPARATOR of your own. PLAN13 replaces `.agent/plan.md` entirely. PAIRS13 is
   appended to no file.
3. The path set of C0a..C5 is exactly the "Change set" paths other than `.agent/handoff.md`, at C6.
4. COMMIT ORDER IS LOAD-BEARING: C1 before every other substantive commit, C4 before C5, and C5 is
   ONE commit — the map line and the edge it records are cut together, because
   `tests/orchestration/test_cluster_deletion_map.py` reds in BOTH directions, so a tree in which
   only one of the two has moved is red at a commit boundary.
5. Any destructive check runs ONLY inside a disposable `git worktree`, never in the primary checkout,
   which satisfies `git status --porcelain` == empty at every commit boundary; prune each worktree.
6. Do not write a `Done:` paragraph of your own; this round resolves and registers no finding.
7. Every gate below runs at a commit STRICTLY EARLIER than C6, so the handback can quote each. Do
   not report C6's own insertion count; the reviewer measures it at the next gate.
8. THE FULL SUITE IS NOT ORDERED THIS ROUND: the round gate is G6's scoped commands plus the canary
   (docs/agents/planner_reviewer_prompt.md §3, verification tier 1). Run G6 in the PRIMARY CHECKOUT,
   because `apps/ui/node_modules` and `apps/ui/dist` are gitignored and npm-backed tests in a fresh
   worktree then fail on the missing build rather than on anything this round did.
9. READING A COMMITTED BLOB, since several gates measure one: use `git show <commit>:<path>` into
   memory or a scratch file under the gitignored `.remedy-wt/`, or read it in a disposable worktree;
   NEVER write a blob over the tracked file and restore it. The R-0569 flake constraint earlier
   rounds carried is DELIBERATELY ABSENT: it names `tests/orchestration/test_product_smoke.py`,
   which no command in G6 or G7 collects, so it would be a clause no run of this round can reach.


## Done when — the gates, one line per gate in the handback

G1  TRANSPORT, at C0b. `sha256` of the committed `.agent/authored/f274-r13.md` equals `sha256` of
    the committed `.agent/last_block.md`, and both equal the digest the delegation message states.
    Report the digest you measured. Per §3 item 37 this covers those artefacts and is not a claim
    about the bytes emitted into a prompt.

G2  THE RECORD APPEND, at C2, re-derived from the COMMITTED blobs.
    (a) BYTES: `.agent/live_review.md` 589620 -> 594390; pre-image a byte-exact PREFIX; post-image
        equal to pre plus the RECORD13 slice — that second clause is the BYTE reader, the prefix
        clause alone being blind to a flip inside the appended region.
    (b) STRUCTURE over the WHOLE appended region: a unit is a maximal run of consecutive non-empty
        lines; COUNT N from the slice itself and REPORT the N you counted; the file's last N units
        equal the slice's units IN ORDER and everything before them is unchanged. Units 233 -> 234.
    (c) NEGATIVE CONTROL: flip the byte at ZERO-INDEXED offset 589621 of the post-image — the `G`
        opening the FIRST appended paragraph — and confirm the BYTE reader of (a) and the STRUCTURAL
        reader of (b) each reject it.
    (d) COUNTS: registrations 69 -> 69, resolutions 6 -> 6, OPEN SET 63 -> 63 BY DISTINCT ID,
        `^Gate: ` 43 -> 44, `^Gate: F274 R12 ` 0 -> 1. This round registers and resolves nothing.

G3  THE DECISION APPEND, at C4, re-derived from the COMMITTED blobs.
    (a) BYTES: `.agent/decisions.md` 905078 -> 911446; prefix exact; post equal to pre plus the
        DECIDE13 slice.
    (b) STRUCTURE, N counted from the slice and REPORTED: units 1986 -> 2000, the last N units equal
        the slice's units IN ORDER, everything before unchanged.
    (c) NEGATIVE CONTROL at zero-indexed offset 905079 — the `#` opening the appended heading —
        rejected by both readers.
    (d) `^## DECISION F274 D7` 0 -> 1.

G4  THE PROSE STATE FILES. `.agent/plan.md` at C1 is BYTE-EQUAL to the PLAN13 slice, is 44 lines
    against the cap of 50, and carries both `## Goal` and `## Next Steps`. `.agent/prose_slips.md`
    at C3 goes 162746 -> 163225 with the pre-image a byte-exact prefix and the appended line once.

G5  THE CUT, at C5, measured against the COMMITTED blobs.
    (a) THE PAIRS: for each REWRITE the FROM block occurs ZERO times in its file and the TO block
        EXACTLY ONCE. For the APPEND-shaped P5 and P8 the §4.9 obligation applies instead: the FROM
        block occurs EXACTLY ONCE and each TO-only line is among the lines C5's diff ADDS. Report
        the readings.
    (b) THE ZERO-GATE, scoped to exactly three files and deliberately no wider: `worker_recommend`
        totals ZERO in `packages/orchestration/dashboard.py` against 3 at the base, and
        `worker_recommendation` totals ZERO in that file, in `scripts/remedy_smoke.sh` and in
        `tests/ui_server/test_dashboard_contract.py` against 2, 1 and 1 at the base. THE SCOPE IS
        THE POINT: this block names both strings and is committed at C0a, while
        `packages/orchestration/worker_recommend.py` and `apps/cli/commands/worker_recommend_cmd.py`
        legitimately keep theirs, so a repo-wide zero would be a gate that cannot pass.
    (c) THE MAP: `tests/orchestration/cluster_deletion_map.txt` goes 38 -> 37 lines, its edges — the
        lines that are neither blank nor comments — go 23 -> 22, its `worker_recommend` edges go
        3 -> 2, and its post-image `sha256` is
        `abacf799bc8716ffbfe54a15ff8d1236e13e3dae44f7f322e962a675acb60c00`.
    (d) THE MOVE LANDED WHOLE: `derive_token_mode` is defined exactly once in
        `packages/orchestration/token_policy.py`, is named in that module's `Public API::` docstring
        block, and that module imports `RunState`. Every touched `.py` file still parses under `ast`.
    (e) NOTHING ELSE MOVED: `git diff --name-only 64346333..<C5>` names exactly the paths of
        constraint 3, and `event_schemas.py`, `agent_loop.py`, `autonomy_loop.py` and
        `worker_recommend.py`, all under `packages/orchestration/`, are each BYTE-IDENTICAL at the
        base and at C5.

G6  THE SUITES, at C5, in the primary checkout per constraint 8. RUN EACH COMMAND ALONE and report
    its own number — the clause the R-0819 recurrence added at round 12. Each figure below was
    measured on the applied tree at the base commit. Prefix every pytest path with
    `python3 -B -m pytest` and suffix it with `-q`.
    (a) `tests/test_token_policy.py` EXIT 0, 28 passed.
    (b) `tests/ui_server/test_dashboard_contract.py` EXIT 0, 73 passed and 1 skipped.
    (c) `tests/orchestration/test_cluster_deletion_map.py` EXIT 0, 3 passed.
    (d) `tests/test_remedy_smoke_script.py` EXIT 0, 191 passed.
    (e) `tests/storage/test_persistence.py` EXIT 0, 26 passed. This file pins
        `token_policy_applied`, which this round leaves alone; it is here to prove that.
    (f) THE CANARY `tests/cli/test_golden_path.py` EXIT 0, 42 passed.
    (g) `python3 -m ruff check` over the four touched `.py` paths EXIT 0, and `python3 -m ruff check
        .` REPORTS 26 ERRORS, unchanged, so DECISION F083 D5's frozen ceiling is untouched — that
        command EXITS 1 while reporting them, which is the gate PASSING, the ceiling being 26 not 0.

G7  THE RED PROOFS, in a disposable worktree at C5 per constraint 5, each run with its UNMUTATED
    control FIRST in that same worktree, so a colour has a baseline.
    (a) THE MAP RATCHET REALLY BITES. Control: `tests/orchestration/test_cluster_deletion_map.py`
        EXIT 0. Then re-insert the single line `packages.orchestration.worker_recommend <-
        packages/orchestration/dashboard.py` into `tests/orchestration/cluster_deletion_map.txt` —
        those exact bytes occur ZERO times in that file at C5 — and confirm EXIT 1 with
        `DISAPPEARED (1)` naming that edge. Restore, confirm EXIT 0, and report both exit codes and
        the digest you restored to.
    (b) THE NEW GUARD DISCRIMINATES. Control: `tests/test_token_policy.py` EXIT 0. Then delete the
        two consecutive lines `    if task_count <= 2:` and `        return "compact"` from
        `packages/orchestration/token_policy.py` — that exact two-line sequence occurs EXACTLY ONCE
        in that file at C5 — and confirm EXIT 1 with
        `TestDeriveTokenMode::test_one_or_two_tasks_is_compact` among the failures. Restore and
        confirm EXIT 0. Report the failing node ids you saw.

G8  THE TREE, at C5. `git status --porcelain` EMPTY; `git ls-files .remedy-wt` EMPTY; `git worktree
    list` the same count as before your first worktree and after your last prune; every commit C0a
    through C5 single-parent. Report the INSERTION count of each commit C0a through C5; the reviewer
    measured C5's applied change as 44 insertions and 15 deletions over six files, against the
    DECISION F104 D1 cap of 500. Read `.agent/STOP` at the round's start, before C5 and after C6,
    and report all three readings.


## Handback — rewrite `.agent/handoff.md` at C6, then push

Carry the mandated sections of `docs/agents/handback_template.md`: the state block, the commits
table with its `+/-` column taken from `git diff --numstat`, the changed-files table, ONE LINE PER
GATE G1 through G8 with its real result, the deviations, the open-findings count and the next
expected action. No length cap. Name the SESSION NUMBER as SESSION 6 of feature F274 and the round
as 13, state the open-findings count as the number G2(d) MEASURED, and add the one sentence of
context self-assessment amend0905-throughput requires. DECLARE, do not silently repair: if any gate
goes red or any slice does not apply as described, report the real command, the real exit code and
the real output, and say what you did.


BEGIN PLAN13 sha256=955118d161f90d65f027ecb5986d13b5c064d1321afa0da1c24d6102f7e8ab6c bytes=2691
# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Finish what F272 could not reach inside its own limit: the prototype cluster deletion and the
classic-to-unified record flip DECISION F272 D15 measured as ATOMIC. DECISION
amend0907-cluster-first D1 reorders the slices so the deletion runs FIRST.

## Current Step

Round 13, the FIRST of `worker_recommend`'s three edges. Rule DECISION F274 D7 before a line moves:
worker recommendation dies with the cluster and nothing inherits it, the token mode never belonged
to it and moves to `packages/orchestration/token_policy.py`, and the `token_policy_applied`
vocabulary is ruled down to what a surviving producer measures. Then cut the `dashboard.py` edge —
the one emitting no run-log event — deleting the `worker_recommendation` section with its
contract-test and smoke-script pins. Book round 12's PASS verdict and the slip round 12 owed.

## Next Steps

1. The two remaining `worker_recommend` edges, in `agent_loop.py` and `autonomy_loop.py`. Both emit
   `token_policy_applied`, so this is where DECISION F274 D7 item 4 lands: three keys leave
   `packages/orchestration/event_schemas.py` in the same commit as the last emitter that writes
   them, and `CycleDecision.selected_worker` goes with them.
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
END PLAN13


BEGIN RECORD13 sha256=5c710702783d92faa9a5ac9419f63fa01ac2b91b8cd36664ed880e5343e22c80 bytes=4770

Gate: F274 R12 — the F274 round 12 entry. VERDICT PASS, ISSUED BY THE REVIEWER AFTER RE-RUNNING EVERY GATE ITSELF AGAINST THE COMMITTED BLOBS, and carried into this round by the pushed `.agent/handoff.md` at `64346333` under operator amendment amend0827-process-diet rule 1, which makes a committed handback a durable carrier so that a verdict never buys a round of its own. Range `5c7b856b2f3bb35e623e1d1cebd6fc9bf7fbf527`..`379d73f290a3a33ceb3b84fd717ef3ae544d424d`, eight commits, every one single-parent, in the ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6, with the path set over the range to C5 naming exactly the seven declared paths. G1 TRANSPORT covers the chain the self-drive workflow can walk, per docs/agents/planner_reviewer_prompt.md §3 item 37 and not the emitted bytes: the reviewer's scratch original `.remedy-wt/f274-r12-FINAL.md`, hashed BEFORE delegation, is BYTE-IDENTICAL to both committed copies, all three 28151 bytes at `217599381b0074252e4081fa3fa049c4ebf044e59342bc6206f6451cba48a47e`. G2 THE REGISTRATION APPEND at `14158d03`: 579917 to 588670 bytes, prefix exact, post equal to pre plus the 8753-byte RECORD12 slice, N counted as 3, units 229 to 232, ordered equality true, the control at byte offset 579918 rejected by both readers; registrations 68 to 69, OPEN SET 63 TO 64 BY DISTINCT ID, `^Gate: ` 42 to 43, `^- R-0835 — ` 0 to 1. G3: `.agent/plan.md` byte-equal to its slice at 46 lines; `.agent/prose_slips.md` 162264 to 162746 with the appended line once. G4 THE FIX at `f3d6ac65`: each of the three pairs reads FROM 0 and TO 1 in its own file, both files keep their line counts at 85 and 73 because every pair is one line in and one line out, the bare word `feature` totals ZERO across the two touched files, and the test file still parses and still holds exactly one class, `TestProgressChecklistRuntime`, unrenamed. G5 THE SUITES, each command run ALONE as the block ordered: `tests/docs/` 303 passed, `test_development_artifact_boundary.py` 18 passed, `test_progress_feature_runtime.py` 5 passed, and THE FULL SUITE IN THE REVIEWER'S OWN RUN IN THE PRIMARY CHECKOUT at 19765 passed, 23 skipped, 0 failed — IDENTICAL to the base, which is the property this round owed, since it changed one docstring and two markdown lines; `ruff` EXIT 0 on the touched file and the frozen ceiling of DECISION F083 D5 unchanged at 26. G6 THE RESOLUTION APPEND at `35b39b28`, which runs AFTER the fix so the paragraph it lands is true when it lands: 588670 to 589620 bytes against the 950-byte slice, N counted as 1, units 232 to 233, control at 588671 rejected by both readers, resolutions 5 to 6, `^Done: R-0835 — ` 0 to 1, and THE OPEN SET BACK TO 63 BY DISTINCT ID — the round opened and closed at 63, having registered and resolved exactly one finding. G7 THE TREE AND THE SCOPE GUARD: porcelain empty, `git ls-files .remedy-wt` empty, worktrees 14 throughout, per-commit insertions 290, 190, 8, 6, 2, 3 and 2 for C0a through C5, and the scope guard holds — `tests/orchestration/cluster_deletion_map.txt` is BYTE-IDENTICAL at the base and at C5, both `cfdbbe8ecdf2727a526cf49083265201d4f1ab43aabad85fe2204c29cf980702`, and NO file under `packages/orchestration/` changed in the range at all. TWO DEVIATIONS WERE DECLARED AND THE REVIEWER SUSTAINS BOTH. THE FIRST IS THE REVIEWER'S OWN DEFECT: gate G4(c) stated that the bare word `feature` occurred THREE times across the two touched files at the base, and the reviewer re-measured it as TWO by substring and by word-boundary regex, per file and in total. The block conflated three SITES with a word count — the P1 site is a stale plural sentence that contains no occurrence of the word, exactly as the block's own registration paragraph describes it. The gate's ORDERED PROPERTY was a post-fix total of ZERO, and that passed exactly, so the gate measured what it existed to measure. The same wrong figure landed inside RESOLVE12, which constraints 1 and 6 required applied verbatim; it is NOT load-bearing there either — the resolution's claim is that the fix worked, and the zero proves it — so under AGENTS.md's `prose_slips.md` rules it earns a dated line and NOT a correction round. THE SECOND DEVIATION IS PROCEDURAL AND CORRECTLY REASONED: the worker ran G5 against the tree at C5 rather than at C4, because checking C4 out would detach or dirty the primary checkout while constraint 8 forbids running the full suite in a worktree, and it showed that `git diff --name-only f3d6ac65..35b39b28` returns exactly one path, `.agent/live_review.md`, which no command in G5 reads. The reviewer confirmed that diff independently. NO FINDING IS REGISTERED BY THIS GATE AND NO NEW ID IS MINTED, so the open set stands at 63 by distinct id and the next free id is R-0836.
END RECORD13


BEGIN SLIPS13 sha256=ea16783104ecc45a5fedee65753a61644f29570d9dd71b1251c67a21057e37d8 bytes=479

2026-09-08 · F274 R12 · The round 12 block's gate G4(c) and the RESOLVE12 slice both stated that the bare word `feature` occurred three times across the two touched files at the base when it occurred twice; the reviewer had counted the three SITES it was repairing, one of which is a plural sentence containing no occurrence of the word, and the worker re-measured it four ways and declared the gap while the gate's ordered property — zero after the fix — passed exactly.
END SLIPS13


BEGIN DECIDE13 sha256=ba146e8da58c078e78300f24843282f1d558a053cd04336e59f5def9d2c03992 bytes=6368

## DECISION F274 D7 — worker recommendation DIES with the cluster and nothing inherits it; the token mode MOVES because it never belonged to it; and the `token_policy_applied` vocabulary is ruled DOWN rather than by omission (2026-09-08)

Date: 2026-09-08. Feature F274, round 13. Status: decided by the reviewer under
docs/agents/planner_reviewer_prompt.md §4 item 7; the operator's veto is any later session.

CONTEXT, MEASURED AT `64346333` BY READING WHAT PRODUCES EACH VALUE RATHER THAN WHAT IT IS NAMED.
`packages.orchestration.worker_recommend` holds THREE surviving consumer edges — `agent_loop.py`,
`autonomy_loop.py` and `dashboard.py`, all under `packages/orchestration/`. UNLIKE ROUNDS 9 THROUGH
12, NONE IS A READ-ONLY VIEW: the two loops each fill four fields of the `token_policy_applied`
run-log event from a `WorkerRecommendation` — `mode`, `estimated_context_tokens`,
`remote_model_requires_approval` and `selected_worker` — `autonomy_loop` additionally fills
`CycleDecision.token_mode` and `CycleDecision.selected_worker`, and `dashboard` fills its
`token_policy` and `worker_recommendation` sections.

THE EVENT DOES NOT DIE WITH THE CLUSTER, WHICH IS WHY THIS IS A RULING RATHER THAN A DELETION.
`token_policy_applied` is a READINESS SIGNAL: `packages/orchestration/autonomy_readiness.py` reads
it in `_has_token_policy_applied` at line 129, publishes it at line 248 and checks it at line 318,
and `packages/orchestration/project_brain.py` reads it at line 661. Both emitters survive, and
`scripts/remedy_smoke.sh` and `tests/storage/test_persistence.py` pin it. Deleting the producer of
its fields without ruling what the event carries afterwards would leave a vocabulary in
`packages/orchestration/event_schemas.py` describing fields nothing writes — the R-0832 shape,
arriving through a schema instead of through a brain node.

THE FOUR FIELDS HAVE THREE DIFFERENT FATES, measured rather than assumed. `token_mode` is computed
inside `recommend_worker` from `len(job.tasks)` and `job.state` alone and reaches no cluster module.
`estimated_context_tokens` is `build_context_pack(...).estimated_tokens`, and
`packages.orchestration.context_pack` IS on the cluster list. `selected_worker` and
`remote_model_requires_approval` come from scoring `worker_adapters.list_worker_specs()`, and
`packages.orchestration.worker_adapters` is NOT on that list and survives.

CHOSEN.

1. NOTHING INHERITS WORKER RECOMMENDATION, as DECISION F274 D6 ruled for the `feature` group. F110's
   model routing was the candidate checked first and is NOT the inheritor:
   `packages/orchestration/model_routing.py` routes a TASK CLASS to a model TIER, a different
   question from which worker provider executes a job, and the module that does answer that
   question, `packages.orchestration.worker_registry`, is itself on the cluster list.
   `selected_worker` and `remote_model_requires_approval` are therefore DELETED rather than
   re-sourced: re-deriving them from `worker_adapters` under another name would be
   `recommend_worker` living on without its file, and AGENTS.md Scope Control rules that replacing
   is deleting — no attic, no alias, no compatibility reader.

2. `estimated_context_tokens` is DELETED. Its only producer is a cluster module, and substituting a
   surviving estimator would put a number into a run-log event that no longer measures the thing the
   field is named for. A fabricated measurement is worse than an absent one.

3. `token_mode` SURVIVES AND MOVES, and this is a MOVE rather than an inheritance.
   `derive_token_mode(job) -> str` lands in `packages/orchestration/token_policy.py` with the same
   three branches, in the same order, that `recommend_worker` computes today. A token mode is token
   policy; both surviving emitters already import that module; it is not on the cluster list. The
   derivation never belonged to worker recommendation and only lived there.

4. THE EVENT VOCABULARY IS RULED EXPLICITLY. `token_policy_applied` KEEPS `mode`,
   `max_context_tokens` and `local_first` and LOSES `estimated_context_tokens`,
   `remote_model_requires_approval` and `selected_worker`. `packages/orchestration/event_schemas.py`
   changes in the SAME COMMIT as the last emitter that writes a removed key, so no tree exists in
   which the registry and the emitters disagree. The event KIND is unchanged, so
   `apps/ui/src/api/humanizeCatalog.ts` and `apps/ui/src/api/actionClass.ts` are untouched and
   `tests/ui_contracts/test_humanize_catalog.py` cannot go red — the R-0823 lesson about a deletion
   orphaning a catalog entry, applied ahead of the cut rather than after it.

5. The dashboard's `worker_recommendation` section is DELETED with the two pins holding it: the
   assertion in `tests/ui_server/test_dashboard_contract.py` and the key in the dashboard tuple of
   `scripts/remedy_smoke.sh`. That tuple keeps a key rather than shrinking, checking `token_policy`
   instead, so the section that survives is the one still covered.

6. SEQUENCING, BY EDGE. Round 13 lands items 3 and 5 and cuts the `dashboard.py` edge, the one of
   the three emitting no run-log event; the round after it cuts the two loop edges and lands item 4.
   The unit of the split is the EDGE, which is what DECISION F274 D2 rules the deletion by, and each
   round leaves a tree that is green and self-consistent rather than half-migrated.

ALTERNATIVES CONSIDERED. (a) KEEP ALL SIX KEYS and re-source three from `worker_adapters` plus a
surviving estimator such as `packages/orchestration/context_inspector.py` — rejected under items 1
and 2: it rebuilds `recommend_worker` under a new name and keeps a number whose referent is gone.
(b) DELETE `token_policy_applied` ENTIRELY — rejected: it is a readiness signal with two surviving
emitters and four surviving readers, so it is not cluster-bound at all. (c) MOVE `worker_recommend`
OFF the cluster list — rejected: `docs/roadmap/features/T2_F260.md`'s Design section fixes that
list, and this feature executes it rather than re-planning it.

HOW TO REVERSE. Delete this paragraph and restore, from git history at `64346333`,
`packages/orchestration/worker_recommend.py`'s three consumer edges, the `worker_recommendation`
dashboard section with its two pins, and the three removed keys of `token_policy_applied` in
`packages/orchestration/event_schemas.py`.
END DECIDE13


BEGIN PAIRS13 sha256=c34eba376d0ab23f885440738271f22b7cedef38598e1aae9e339bceeeab9241 bytes=2441

--- P1 FILE packages/orchestration/dashboard.py
--- P1 FROM
    from packages.orchestration.worker_recommend import recommend_worker
--- P1 TO
    from packages.orchestration.token_policy import derive_token_mode
--- P2 FILE packages/orchestration/dashboard.py
--- P2 FROM
    # Token/worker
    rec = recommend_worker(job, events)
--- P2 TO
    # Token mode
    token_mode = derive_token_mode(job)
--- P3 FILE packages/orchestration/dashboard.py
--- P3 FROM
        "token_policy": {
            "token_mode": rec.token_mode,
        },
        "worker_recommendation": {
            "recommended_worker": rec.recommended_worker,
        },
--- P3 TO
        "token_policy": {
            "token_mode": token_mode,
        },
--- P4 FILE packages/orchestration/dashboard.py
--- P4 FROM
    wr = data.get("worker_recommendation", {})
    lines.append(f"  Worker: {wr.get('recommended_worker', '?')}")

    mem = data.get("memory", {})
--- P4 TO
    mem = data.get("memory", {})
--- P5 FILE packages/orchestration/token_policy.py
--- P5 FROM
    build_default_token_policy(job) -> TokenPolicy
--- P5 TO
    build_default_token_policy(job) -> TokenPolicy
    derive_token_mode(job) -> str
--- P6 FILE packages/orchestration/token_policy.py
--- P6 FROM
from packages.core.models import Job
--- P6 TO
from packages.core.models import Job, RunState
--- P7 FILE tests/test_token_policy.py
--- P7 FROM
from packages.core.models import Job, Task
--- P7 TO
from packages.core.models import Job, RunState, Task
--- P8 FILE tests/test_token_policy.py
--- P8 FROM
    build_default_token_policy,
--- P8 TO
    build_default_token_policy,
    derive_token_mode,
--- P9 FILE tests/ui_server/test_dashboard_contract.py
--- P9 FROM
        assert "worker_recommendation" in data
        assert "memory" in data
--- P9 TO
        assert "memory" in data
--- P10 FILE scripts/remedy_smoke.sh
--- P10 FROM
for k in ('readiness', 'decisions', 'test_status', 'worker_recommendation', 'memory', 'events', 'next_actions'):
--- P10 TO
for k in ('readiness', 'decisions', 'test_status', 'token_policy', 'memory', 'events', 'next_actions'):
--- P11 FILE tests/orchestration/cluster_deletion_map.txt
--- P11 FROM
packages.orchestration.worker_recommend <- packages/orchestration/dashboard.py
packages.orchestration.worker_registry <- packages/orchestration/token_economy.py
--- P11 TO
packages.orchestration.worker_registry <- packages/orchestration/token_economy.py
END PAIRS13


BEGIN TOKENMODE sha256=e35869fedb39118ac48a3facaa3acfb506883a6d9fa28de68a67fb15e5807235 bytes=550


def derive_token_mode(job: Job) -> str:
    """The token mode a job's shape asks for: caveman, compact or standard.

    Deterministic — reads the task count and the run state and nothing else.
    DECISION F274 D7 moved this here out of `worker_recommend`, which dies
    with the prototype cluster: a token mode is token policy.
    """
    task_count = len(job.tasks) if job.tasks else 0
    if task_count == 0 or job.state == RunState.COMPLETED:
        return "caveman"
    if task_count <= 2:
        return "compact"
    return "standard"
END TOKENMODE


BEGIN TESTS13 sha256=43794bc94a9b3236284d4624a92850d23351748094a1d093a3fa1e74aeccd523 bytes=807


class TestDeriveTokenMode:
    """DECISION F274 D7: the token mode derivation survives the cluster deletion."""

    def test_no_tasks_is_caveman(self):
        assert derive_token_mode(_make_job(task_count=0)) == "caveman"

    def test_completed_job_is_caveman_however_many_tasks(self):
        job = _make_job(task_count=5)
        job.state = RunState.COMPLETED
        assert derive_token_mode(job) == "caveman"

    def test_one_or_two_tasks_is_compact(self):
        assert derive_token_mode(_make_job(task_count=1)) == "compact"
        assert derive_token_mode(_make_job(task_count=2)) == "compact"

    def test_three_or_more_tasks_is_standard(self):
        assert derive_token_mode(_make_job(task_count=3)) == "standard"
        assert derive_token_mode(_make_job(task_count=9)) == "standard"
END TESTS13
