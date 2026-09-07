── STEP T002 move three / F272 — round 14 ──
Goal:   Retype `JobPlan.state` to `RunState` so one vocabulary describes a job's
        lifecycle, keeping every stored record loadable and every rendering the
        plain word.
Base:   `6c2225b8`. Branch `feature/f272-one-world-completion`. SESSION 7.

## Why this round is authored from a RUN, not from the inventory alone

`.agent/f272_retype_readiness.md` is correct in all it measured; its section 8
says what it could not close. The reviewer closed it by APPLYING move three in a
disposable worktree at `6c2225b8` and running the suites. That run changed the
change set; RECORDR14 carries the full evidence:

- Applied exactly as the inventory bounds it, `tests/orchestration/` reads
  EXIT 1 at 111 failed and 12736 passed, the traceback being `AttributeError:
  'str' object has no attribute 'value'` at `pingpong_job.py:667` — 23 sites
  construct `JobPlan` from a raw string literal and `_import_job` passes the
  record's plain JSON value straight through, so a bare `.value` raises.
- The inventory's COUNT B predicate undercounts. Widened to also accept
  `getattr(x, "state", …)` the count is 18, not 12; four of the six newly
  visible sites are already defensive and TWO are not —
  `job_evidence.py:2198` and `run_manifest.py:6509`. After the retype the first
  makes `_crosscheck_terminal_jobplan_manifest` return before its first check,
  so the terminal integrity crosscheck PASSES BY NOT LOOKING.

With the design below that suite reads EXIT 0 at 12846 passed and 10 skipped,
the only difference from base being the known `node_modules` worktree artifact
an UNMODIFIED control worktree at the same commit fails too.

## Bundle (ordered; commit in this order, nothing added or reordered)

- C0a save this block to `.agent/authored/f272-r14.md` by `shutil.copyfile`
- C0b mirror the same source to `.agent/last_block.md` by `shutil.copyfile`
- C1  `.agent/plan.md` REPLACED by the PLANF272R14 slice
- C2  `.agent/live_review.md` APPEND the RECORDR14 slice
- C3  `.agent/prose_slips.md` APPEND SLIPSR14; `docs/roadmap/features/T2_F272.md`
      APPEND DECISIONR14 — both in this one commit
- C4  the retype: pairs P1 through P8 below, over `pingpong_job.py`,
      `job_evidence.py`, `run_manifest.py` and `test_job_state_field.py`
- C5  `tests/orchestration/test_job_state_field.py` APPEND the TESTSR14 slice
- C6  rewrite `.agent/handoff.md`

C4 carries the inverted pin (P8) because `test_nothing_was_retyped` asserts the
OLD type: splitting it would commit a knowingly red tree. C5 is separate because
its three tests are NEW guards, not the retype.

## Change set — these paths and no others

    .agent/authored/f272-r14.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    docs/roadmap/features/T2_F272.md
    packages/orchestration/pingpong_job.py
    packages/orchestration/job_evidence.py
    packages/orchestration/run_manifest.py
    tests/orchestration/test_job_state_field.py
    .agent/handoff.md

## Constraints

1. Apply every slice between its markers BYTE FOR BYTE. Never edit a slice. If a
   slice is wrong, apply it as given and DECLARE it in the handback.
2. No marker line may reach any file other than the two C0 copies.
3. C4's edits land in ONE commit, in the order given below.
4. Do NOT change any test to make a gate green. If a gate goes red, stop and
   report it with the real transcript.
5. Do NOT touch the six `JOB_*` constants' NAMES or VALUES, the stored JSON key
   `"status"`, or the f-string at `pingpong_job.py:3026`.
6. Mint no finding id. Differences between this block's readings and yours are
   reported in the handback with BOTH numbers; the reviewer rules on each.
7. Destructive verification runs ONLY in a disposable `git worktree`, removed
   afterwards BY EXACT PATH, never by glob. If you create none, say so.
8. Read `.agent/STOP` with `os.path.exists` before C0a, before C4 and before C6
   and report all three. If it exists, finish the current commit, hand back, end.
9. Every run uses `python3 -B`. Report REAL exit codes; "green" is not a result.

## C4 — the retype, as FROM→TO pairs

Each pair states the containment test's own output. Verify each FROM's
occurrence count in its file BEFORE editing and report it.

### P1 `pingpong_job.py` — TO contains FROM: true → APPEND

FROM (expect 1x):

    from packages.core.models import Artifact, Budget, JobFences

TO:

    from packages.core.models import Artifact, Budget, JobFences, RunState

### P2 `pingpong_job.py` — six rebindings; every comment line between them UNCHANGED

Each FROM is 1x in the file. The three `#: F011.` comment lines that sit between
`JOB_PAUSED` and `JOB_STOPPED` are NOT touched.

    JOB_PLANNED = "planned"      ->  JOB_PLANNED = RunState.PLANNED
    JOB_RUNNING = "running"      ->  JOB_RUNNING = RunState.RUNNING
    JOB_BLOCKED = "blocked"      ->  JOB_BLOCKED = RunState.BLOCKED
    JOB_COMPLETED = "completed"  ->  JOB_COMPLETED = RunState.COMPLETED
    JOB_PAUSED = "paused"        ->  JOB_PAUSED = RunState.PAUSED
    JOB_STOPPED = "stopped"      ->  JOB_STOPPED = RunState.STOPPED

Then insert, immediately after the rebound `JOB_STOPPED` line, one blank line and:

    # F272 move three: the lifecycle field is a ``RunState``, but a job record
    # written before this round may carry ANY string — `complete`, `dry_run` and
    # `promoted` all occur in records on disk today — so DECISION F272 D5's
    # promise that every stored record still loads is kept by KEEPING an
    # unrecognised value verbatim rather than raising on it.
    _JOB_STATE_BY_VALUE = {member.value: member for member in RunState}


    def _coerce_job_state(value: object) -> object:
        """Map a stored status string onto its ``RunState`` member, or keep it as-is."""
        if isinstance(value, RunState):
            return value
        return _JOB_STATE_BY_VALUE.get(value, value)

### P3 `pingpong_job.py` — TO contains FROM: false → REWRITE

FROM (expect 1x): `    state: str = JOB_PLANNED`

TO: `    state: RunState = JOB_PLANNED`

### P4 `pingpong_job.py` — TO contains FROM: true → APPEND

`JobPlan` has NO methods today and `fences` is its LAST field, so the method goes
after it, at the end of the class body.

FROM (expect 1x):

    fences: JobFences | None = None

TO:

    fences: JobFences | None = None

    def __post_init__(self) -> None:
        # One spelling per concept: however the field was set — a raw literal, a
        # JOB_* constant or an imported record — it settles as a RunState.
        self.state = _coerce_job_state(self.state)

### P5 `pingpong_job.py` — TO contains FROM: false → REWRITE, BOTH occurrences

These are `_export_job` (667) and `export_job_report` (2968); the bytes are
identical and BOTH get the same TO.

FROM (expect exactly 2x; replace both):

    "status": job.state,

TO:

    "status": job.state.value if isinstance(job.state, RunState) else job.state,

After the edit FROM must read 0x and TO 2x in that file.

### P6 `job_evidence.py` and P7 `run_manifest.py` — TO contains FROM: false → REWRITE

The SAME pair, once in each file (in `_crosscheck_terminal_jobplan_manifest` and
in `_job_is_resumable`). FROM expect 1x IN EACH FILE.

FROM:

    status = str(getattr(job, "state", "") or "")

TO:

    _state = getattr(job, "state", "")
    status = str(getattr(_state, "value", _state) or "")

### P8 `test_job_state_field.py` — TO contains FROM: false → REWRITE

FROM (expect 1x): `        assert type(JobPlan().state).__name__ == "str"`

TO: `        assert type(JobPlan().state).__name__ == "RunState"`

## Done when — eight gates, each RUN, each with its REAL exit code

**G1 TRANSPORT.** One digest comparison: `sha256` of the committed
`.agent/authored/f272-r14.md` equals BLOCK_SHA in the delegation wrapper, and its
byte and line counts equal BLOCK_LENGTH and BLOCK_LINES. Per §3 item 37 this
covers the saved copy and its mirror, never the emitted bytes.

**G2 THE RECORD** at C2. `.agent/live_review.md` ← RECORDR14. Four readers:
(a) BYTE — assert the pre-image's terminal byte is exactly one `\n` BEFORE
writing; then `post == pre + b"\n" + slice`, pre a byte-exact prefix of post,
post ending in exactly one `\n`. (b) STRUCTURAL, independently, splitting the
WHOLE image on `\n{2,}`: N is COUNTED BY YOUR SCRIPT from the slice's own
paragraphs and never taken from this block; the last N units equal the slice's
paragraphs IN ORDER, everything before an unchanged prefix. (c) NEGATIVE
CONTROL, in memory and never on disk: flip one bit inside the FIRST appended
paragraph, require (a) and (b) to REJECT, restore, require both to ACCEPT.
(d) COUNTS before → after, reporting each measured value:

    ^- R-\d{4} — distinct ids      305 → 305
    ^Done: R-\d{4} — distinct      248 → 248
    open set BY DISTINCT ID         57 → 57
    ^Gate:                          35 → 36
    ^Gate: F272 R13                  0 → 1

**G3 THE PLAN** at C1. `.agent/plan.md` is byte-equal to the PLANF272R14 slice;
report its byte length and line count against the AGENTS.md cap of 50; `## Goal`
and `## Next Steps` both present.

**G4 THE RETYPE IS REAL** at C4, measured by IMPORTING THE SHIPPED MODULE and
printing the resolved `__file__` rather than by grepping the diff — this gate is
deliberately NOT computed from the predicate that defines the change set, which
is the counter-measure R-0820 requires. Report each reading:

    type(JobPlan().state).__name__                       -> RunState
    type(JobPlan(state="completed").state).__name__      -> RunState
    type(_import_job({"job_id":"j","status":"blocked"}).state).__name__ -> RunState
    type(JOB_BLOCKED).__name__ -> RunState, JOB_BLOCKED == "blocked" -> True
    [m.value for m in RunState] unchanged, nine members
    type(_export_job(JobPlan(job_id="j", state=JOB_BLOCKED))["status"]) is str -> True
    _import_job({"job_id":"j","status":"complete"}).state -> 'complete' (D5 holds)
    _export_job of that job ["status"]                    -> 'complete'

**G5 MUTATION RED-PROOF**, in a disposable worktree at the round's own commit,
never in the primary checkout. Runner `python3 -B -m pytest`, scoped to
`tests/orchestration/test_job_state_field.py -q -p no:randomly`. Report the
UNMUTATED CONTROL first (expect EXIT 0) and the mutated run beside it. Mutation:
in `packages/orchestration/pingpong_job.py` replace the THREE-line span below —
assert it occurs exactly 1x before mutating, because the `"status"` line alone
occurs twice and the span is what makes the target unique — so that `_export_job`
alone loses its `.value`:

    "job_workspace_path": job.job_workspace_path,
    "job_title": job.job_title,
    "status": job.state.value if isinstance(job.state, RunState) else job.state,

by the same three lines whose last reads `"status": job.state,`. Then
`test_the_exported_status_is_a_plain_str_and_not_a_run_state` MUST FAIL. Remove
the worktree by exact path and report `git worktree list` afterwards.

**G6 THE SUITES**, run SERIALLY, each its own invocation, each `-q -p
no:randomly`. Bases measured by the reviewer in the primary checkout at
`6c2225b8`:

    tests/orchestration/          EXIT 0, 12847 passed, 10 skipped
    tests/ui_contracts/           EXIT 0,   809 passed,  4 skipped
    tests/docs/                   EXIT 0,   303 passed
    tests/cli/test_golden_path.py EXIT 0,    42 passed

Require EXIT 0 and ZERO failures for all four, skips unchanged, and RECONCILE
the orchestration passed count: it must equal 12847 plus exactly the number of
tests C5 adds. Report the number you measured rather than repeating one from
here. `tests/ui_contracts/` is named because R-0821's surviving clause requires
it of any block changing a state vocabulary, and this one changes the six
`JOB_*` constants; `tests/docs/` because C3 writes under `docs/roadmap/`.

**G7 LINT AND INTEGRITY.** `python3 -m ruff check` over exactly the four `.py`
files this round changes, and `python3 -m apps.cli.grouped integrity check
--json`. Report both real exit codes. A ruff diagnostic that reproduces at
`6c2225b8` is reported as pre-existing and NOT fixed.

**G8 THE TREE.** `git status --porcelain` at every commit boundary, reported as
its real output and never as the word "empty"; `git ls-files .remedy-wt` EMPTY;
`git worktree list`; and per-commit insertions from `git diff --numstat <parent>
<commit>` for C0a through C5, each under the DECISION F104 D1 cap of 500 and each
matching the handback's `## Commits` table cell for cell. C6 cannot count its own
insertions (§3 item 14) and is excluded.

## Handback

Rewrite `.agent/handoff.md`: feature and round, SESSION 7 of F272, branch, the
`## Commits` table with real `+/-` per path, the item-status table covering C0a
through C6 exactly once each, one line per gate with its REAL exit code then the
transcripts, deviations, and the next expected action. No length cap. Push the
branch. Create NO pull request. Add ONE sentence of context self-assessment in
the Session section.

<<<BEGIN PLANF272R14>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 through 13 PASSED;
round 2 FAILED on a premise DECISION F272 D2 has corrected. T001 is COMPLETE;
T002 has landed the eight administrative fields, widened `RunState`, renamed
`JobPlan.status` to `state`, given `blocked` and `stopped` their place in the
cockpit, and now retypes the field itself.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the consumers, T004 the classic
runner, T005 the reachability test and the cluster deletion.

## Current Step

Move three of DECISION F272 D6: `JobPlan.state` is retyped to `RunState`, the six
`JOB_*` constants become `RunState` members keeping their names and values, and
`__post_init__` coerces every construction path so one type describes the field.
Two record boundaries emit the plain value, and the two `str(getattr(job,
"state", …))` sites that would otherwise silently stop checking are fixed.

## Next Steps

1. The Mission extension — the order, the contract, the mission plan and the
   ordered job references.
2. T003, the eleven consumers named under Design in `T2_F260.md`, one per commit
   where the diff allows, each tested on a job built through the ping-pong path.
3. T004, the classic runner and the resolver collapse.
4. T005, the reachability test and the cluster deletion, which is never split.

## Risks

- A str-Enum changes `str()` and `%s` and nothing else, but the SITE SET of those
  renderings is wider than a bare-attribute predicate sees: `getattr(job,
  "state", …)` hid two, one an integrity check that passed by not looking.
<<<END PLANF272R14>>>

<<<BEGIN RECORDR14>>>
Gate: F272 R13 — the F272 round 13 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ. Range `a9aa8fa7`..`6c2225b8`, six commits, every one single-parent, in exactly the bundle's ordered sequence C0a, C0b, C1, C2, C3 and C4 with nothing added, dropped or reordered. G1 TRANSPORT IS A REAL CHAIN AND NOT MERELY SELF-CONSISTENT: the reviewer's own scratch original `.remedy-wt/f272-r13-block.md` survived the session boundary, and it, the committed `.agent/authored/f272-r13.md` and the committed `.agent/last_block.md` are all 24962 bytes at 322 lines and all hash to `33845a1f979e80338bc39df0e508521a6e4e9c66f2ac6d58941bf12f49674217`; per §3 item 37 that chain covers those three artefacts and is not a claim about the bytes emitted into a prompt. G2 THE RECORD reproduces byte for byte under the reviewer's own readers: `.agent/live_review.md` 1132952 to 1138931, the pre-image a byte-exact prefix, `post == pre + NL + slice` TRUE, both terminal bytes exactly one newline; registrations 305 unchanged, resolutions 247 to 248, open set BY DISTINCT ID 58 to 57, `^Gate: ` 34 to 35, `^Gate: F272 R12 ` 0 to 1, `^Done: R-0821 ` 0 to 1 and `^Landed: R-0821 ` 1 to 1 UNCHANGED. G3 THE PLAN is 2159 bytes byte-equal to its slice at 43 lines against the cap of 50, hashing to `7d0582411487d77bc42f65fb6ba224ee882dc10584a59157e3d33912975a83ee`, with `## Goal` and `## Next Steps` both present. G4 AND G5, THE INVENTORY, RE-DERIVED INDEPENDENTLY BY THE REVIEWER AND NOT READ: importing the shipped `/home/decodeux/Repos/remedy/packages/core/models.py` under CPython 3.10.12 reproduces all ten str-mixin readings and the nine members in declaration order; an `ast` sweep over the tracked `.py` files reproduces 1066 files, `'%s' % <x>.state` at 0 and `str(<x>.state)` at 12 at exactly the twelve paths and lines the inventory names; the three record boundaries print verbatim at 667, 2968 and 3026 in their named enclosing functions; the six constants read 65, 66, 67, 68, 69 and 73 with their values unchanged; and the blast radius is 29 files, identical to the inventory's list, with `-w` returning the same 29. G6 THE SUITES, re-run serially by the reviewer: `tests/ui_contracts/` EXIT 0 at 809 passed and 4 skipped, `tests/docs/` EXIT 0 at 303, the canary EXIT 0 at 42 — the base readings exactly, correctly, because the round changed no `.py` file. G7: ruff correctly NOT invoked over an empty ordered file set, integrity EXIT 0 with `"passed": true` and `"fail_count": 0` over 5 checks. G8 THE TREE: `git status --porcelain` EMPTY, `git ls-files .remedy-wt` EMPTY, thirteen worktree entries being the primary and the twelve pre-existing `remedy/job-*`, and no worktree created or removed. ALL FOUR OF THE WORKER'S NUMERIC DEVIATIONS ARE UPHELD AND EVERY ONE IS THE REVIEWER'S ERROR, NOT THE WORKER'S: the block's pre-image figure for the record was 1132490 against a measured 1132952, stale by exactly round 12's own C6; the tracked `.py` count is 1066 and not 1065; the six constants' blast radius is 29 files and not 27; and `tests/orchestration/test_job_state_field.py` holds exactly ONE assertion move three must invert, at line 53, not the two the block asserted — the block's second was a READING taken by round 10's gate and not a line in the file, and the file's only `isinstance` must NOT be inverted. Each is a reviewer-prose inaccuracy that left nothing wrong on disk, so each is one dated line in `.agent/prose_slips.md` and no id is spent, per operator amendment amend0827-process-diet rule 2. DEVIATION 5 IS RULED IN THE WORKER'S FAVOUR AND SETTLED AS DECISION F272 D10: it followed this block's constraint over round 12's contrary handoff sentence and appended the `Done: R-0821` paragraph BESIDE the surviving `Landed:` line, and the reviewer measures that every id ever resolved after a `Landed:` line — R-0725, R-0757, R-0818 and now R-0821 — carries both, with not one `Landed:` line ever deleted, which is what an append-only record requires and what §3 item 20 forbids overwriting. DEVIATION 6 IS THE ROUND'S BEST CONDUCT: unordered, the worker measured that round 10's rendering guard does not discriminate a missing `.value` at the two record boundaries, and the reviewer confirms it by standing a `RunState` member in the field today — all three of that guard's assertions pass while `_export_job(job)["status"]` is a `RunState` object, and only `type(...) is str` tells them apart.

Evidence added to R-0820 rather than a second id, per §3 item 30, because this is that same defect — a static predicate that under-selects, with the gate inheriting the blindness — reached one layer further out. THE INVENTORY'S COUNT B PREDICATE UNDERCOUNTS, AND THE REVIEWER PROVED IT BY RUNNING RATHER THAN BY READING. Move three applied at `6c2225b8` exactly as `.agent/f272_retype_readiness.md` bounds it — the six constants, the field annotation, `.value` at the two boundaries and the one inverted assertion — leaves `tests/orchestration/` at EXIT 1 with 111 failed and 12736 passed, the traceback reading `AttributeError: 'str' object has no attribute 'value'` at `pingpong_job.py:667`, because 23 sites construct `JobPlan` with a raw string literal and `_import_job` passes the record's plain JSON value straight through. Widening the predicate from a bare `Attribute` named `state` to one that also accepts `getattr(x, "state", …)` raises the rendering-site count from 12 to 18; four of the six newly visible sites already carry the defensive `.value` idiom, and two do not: `packages/orchestration/job_evidence.py:2198` and `packages/orchestration/run_manifest.py:6509`, both spelled `status = str(getattr(job, "state", "") or "")`. The first is the one that matters — after the retype `str(RunState.STOPPED)` is `'RunState.STOPPED'`, so `_crosscheck_terminal_jobplan_manifest` returns before its first check and the terminal integrity crosscheck passes BY NOT LOOKING, which is R-0438's vacuous-gate shape arriving in production code rather than in a block. With `__post_init__` coercion, a tolerant boundary and those two sites fixed, the same suite reads EXIT 0 at 12846 passed and 10 skipped against a reviewer-measured base of 12847 passed and 10 skipped, the single difference being the known `node_modules` worktree artifact that an UNMODIFIED control worktree at the same commit fails identically.
<<<END RECORDR14>>>

<<<BEGIN SLIPSR14>>>
2026-09-07 · F272 R13 block, the record's pre-image figures (reviewer) · The block stated `.agent/live_review.md` at `a9aa8fa7` as 1132490 bytes and 705 units; it is 1132952 and 706. The figure was read before round 12's C6, the one-line `Landed: R-0821` append, and then labelled with a commit that is after it. Nothing failed, because G2 ordered the append RELATION and seven counts rather than an absolute length — but a byte length carried across a commit boundary is a reading whose commit must be re-measured, not relabelled.

2026-09-07 · F272 R13 block, the tracked-file count (reviewer) · The block stated 1065 tracked `.py` files; three independent commands read 1066, at `a9aa8fa7` and at the round's own commit. The direction was harmless because both derived counts reproduce over a superset, but the numeral was carried forward from an earlier round's sweep instead of being re-measured for this one.

2026-09-07 · F272 R13 block, the constants' blast radius (reviewer) · The block stated 27 files referencing at least one of the six `JOB_*` constants; the exact command it named returns 29, and so does the same command with `-w`. The worker listed all 29 by path so the next block can gate on the SET rather than the number, which is the counter-measure R-0820 already asks for and which a bare count cannot support.

2026-09-07 · F272 R13 block, the assertions move three inverts (reviewer) · The block ordered "the TWO assertions move three must invert, both in `tests/orchestration/test_job_state_field.py`", and that file holds exactly ONE, at line 53. The second was a READING taken by round 10's gate G4(v), not a line in the file; the file's only `isinstance` is line 90 and it must stay TRUE after the retype. A worker following the block would have hunted a line that does not exist and the nearest candidate was one it had to leave alone. A gate's companion reading is not an assertion, and a block that counts assertions in a file greps that file.
<<<END SLIPSR14>>>

<<<BEGIN DECISIONR14>>>
### DECISION F272 D10 (2026-09-07, F272 round 13) — a `Landed:` line SURVIVES beside the `Done:` paragraph that resolves it; the record is append-only and is never overwritten

CONTEXT. `docs/agents/planner_reviewer_prompt.md` §4 item 4 says the reviewer
"replace[s] the `Landed:` line with the authored `Done:` text at the next gate",
and round 12's handoff repeated that as an order. Round 13's block said the
opposite — append the resolution beside the line, leave the line — and required
`^Landed: R-0821 ` to read 1 before and 1 after. The worker followed the block
and declared the contradiction rather than choosing silently.

CHOSEN. The `Landed:` line SURVIVES. A resolution is APPENDED beside it, never
over it.

WHY, MEASURED RATHER THAN ARGUED. Every id ever resolved after a `Landed:` line
carries BOTH — R-0725, R-0757, R-0818 and now R-0821 — and not one `Landed:`
line has ever been deleted; the ledger holds 30 such lines, 26 still awaiting a
reviewer's `Done:`, which is exactly the "unreviewed fix" state §4 item 4 wants
visible. §3 item 20 is the stronger and explicit claim: "appending a correction
is how this record stays honest, and overwriting landed text is worse than a
dated wrong sentence". A `Landed:` line also records WHICH COMMIT landed the
fix, which the `Done:` paragraph does not always repeat.

ALTERNATIVES. Deleting the line, as §4 item 4 reads literally — rejected: it
rewrites an append-only record and loses the landing commit. Treating each case
ad hoc — rejected: that is what produced two documents giving opposite orders.

CONSEQUENCE. §4 item 4 is read as "the reviewer SUPERSEDES the `Landed:` line
with an authored `Done:` paragraph", and supersede means append. A `Landed:`
line alone still means an unreviewed fix; one WITH a `Done:` means a reviewed
fix whose landing commit is still on the record.

REVERSE by deleting this decision; the pairs already on disk are not rewritten
either way, because that is the rule this decision states.
<<<END DECISIONR14>>>

<<<BEGIN TESTSR14>>>


class TestTheRetypeIsComplete:
    """F272 move three — the guards round 13 measured as MISSING.

    Round 10's rendering guard cannot see a missing ``.value`` at the record
    boundary: a ``RunState`` member equals, formats and JSON-serialises exactly
    like its value, so that guard's three assertions are all TRUE for a bare
    member. Only its TYPE tells them apart, which is what the first test reads.
    """

    def test_the_exported_status_is_a_plain_str_and_not_a_run_state(self):
        """The discriminator. A bare ``RunState`` passes every other guard."""
        job = JobPlan(job_id="j1", state=JOB_BLOCKED)
        assert type(_export_job(job)["status"]) is str

    def test_every_construction_path_settles_as_a_run_state(self):
        """One spelling per concept: a raw literal, a JOB_* constant and an
        imported record reach the same type, or the annotation is a lie."""
        assert type(JobPlan(state="completed").state).__name__ == "RunState"
        assert type(JobPlan(state=JOB_BLOCKED).state).__name__ == "RunState"
        assert type(_import_job({"job_id": "j1", "status": "blocked"}).state).__name__ == "RunState"

    def test_a_record_whose_status_is_not_a_run_state_value_still_loads(self):
        """DECISION F272 D5. ``complete``, ``dry_run`` and ``promoted`` occur in
        records on disk; an unrecognised value is KEPT, never raised on."""
        job = _import_job({"job_id": "j1", "status": "complete"})
        assert job.state == "complete"
        assert _export_job(job)["status"] == "complete"
<<<END TESTSR14>>>
