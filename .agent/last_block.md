BEGIN BLOCK f045-r3-1
── STEP T003a/3 — F045 Loop definitions · ROUND 3 (findings + the mission path) ──

Goal:        Close all four open findings, land DECISIONs F045 D4 and D5, fix
             the STOP re-check gap on disk, and build the action dispatch:
             `run_loop` (job + mission kinds), the inert-trigger notice, and
             `last_run_for_loop`.
Bundle:      ITEM 1 C0 save block · ITEM 2 C1 finding resolutions · ITEM 3 C2
             decisions D4+D5 · ITEM 4 C3 protocol STOP re-check · ITEM 5 C4
             loop_spec mission-template validation · ITEM 6 C5 its tests ·
             ITEM 7 C6 extract the shared job builder · ITEM 8 C7 run_loop and
             last_run_for_loop · ITEM 9 C8 their tests · ITEM 10 C9 plan +
             handoff · ITEM 11 gates.
Change:      .agent/authored/f045-r3-1.md · .agent/last_block.md ·
             .agent/live_review.md · .agent/decisions.md ·
             docs/agents/self_drive_protocol.md ·
             packages/orchestration/loop_spec.py ·
             tests/orchestration/test_loop_spec.py ·
             packages/orchestration/loop_run.py ·
             tests/orchestration/test_loop_run.py · .agent/plan.md ·
             .agent/handoff.md. Nothing else. Do NOT edit config.py,
             budget_resolution.py, long_run_executor.py, mission_state.py,
             packages/core/models.py or any file under apps/.
Constraints: SPLIT round. Never work on main; never force-push; no PR this
             round; merge nothing. Do-not-touch (feature file):
             scheduling/cron, the routine library, notifications. This round
             adds NO CLI — that is the next round.
Insertion budget, per commit (counter-measure for R-0345, stated before
             emission): C0 ≈ block size · C1 ≤ 15 · C2 ≤ 60 · C3 ≤ 12 ·
             C4 ≤ 12 · C5 ≤ 45 · C6 ≤ 50 · C7 ≤ 100 · C8 ≤ 170 · C9 ≤ 115.
             No commit bundles a module with its test file. Every commit is
             under the AGENTS.md 500-insertion cap by construction; if any one
             exceeds it, split and declare.
Done when:   every gate in ITEM 11 has been RUN and its real exit code and
             output recorded. "Green" as a word is a finding.
Handback:    completion report + rewrite .agent/handoff.md

═══ ITEM 1 · C0 — save this block verbatim ═══
Write the block bytes (BEGIN..END markers included) to BOTH
`.agent/authored/f045-r3-1.md` and `.agent/last_block.md`. No trailing
whitespace on any line. Prove it:
  cmp .agent/authored/f045-r3-1.md .agent/last_block.md   → exit 0, no output
Commit subject: `chore(f045): save the R3 block verbatim`

═══ ITEM 2 · C1 — the finding resolutions ═══
File `.agent/live_review.md`. Four APPEND-shaped edits: each existing finding
paragraph keeps its bytes and gains a `Done:` line directly BELOW it, separated
by one blank line. Change nothing else in the file. The trailing `OPEN.` inside
each finding paragraph stays exactly as it is — the `Done:` line is what marks
resolution in this repository, and rewriting the paragraph would break the
record it exists to preserve.

Below R-0344's paragraph, add this one line:
Done: R-0344 — RESOLVED at the R3 gate. Verified against the disk, not the report: no assertion in `tests/orchestration/test_loop_run.py` matches against a string that carries a filesystem path — the file's assertions read `job.user_prompt`, `job.name`, `job.project_id`, `job.metadata`, `job.budgets`, `job.state` and two `LoopRunError` messages whose text names a loop and a variable and no path. The R1 defect's own site is fixed too: `tests/orchestration/test_loop_spec.py:265` scans `reported_keys` rather than whole warning strings, and `:115` asserts the exact message `loop 'typo-carrier': unknown key 'cadence'`, which contains no path. `python3 -m pytest tests/orchestration/test_loop_run.py tests/orchestration/test_loop_spec.py -q` prints `23 passed`.

Below R-0345's paragraph, add this one line:
Done: R-0345 — RESOLVED at the R3 gate. Verified against the disk, not the report: `git log --numstat` over the R2 range shows five commits at 5, 59, 168, 182 and 74 insertions — every one under the AGENTS.md 500-insertion cap, and `packages/orchestration/loop_run.py` (168) landed in `6794e7f0` while `tests/orchestration/test_loop_run.py` (182) landed separately in `5d613f49`, so no commit bundled a new module with its test file. The R2 block carried the per-commit insertion budget the counter-measure demands, and this block carries one too.

Below R-0346's paragraph, add this one line:
Done: R-0346 — RESOLVED at the R3 gate. Verified against the disk, not the report: `grep -c "^## DECISION F045 D" .agent/decisions.md` prints 3, at lines 4626, 4648 and 4664 — D1 (top-level `[[loop]]`), D2 (the mirrored deadline contract) and D3 (T002 materializes the job action). The two decisions that lived only in a module docstring now live in the file the repo searches for decisions, and this round's change set carries `.agent/decisions.md` for D4 and D5, which is the counter-measure applied rather than restated.

Below R-0347's paragraph, add this one line:
Done: R-0347 — RESOLVED at the R3 gate. Fixed on disk rather than in reviewer habit, which is the whole point of the finding: `docs/agents/self_drive_protocol.md` Phase 2 now orders the `.agent/STOP` re-read before each round is authored, so the sentinel has a re-check point in the round loop instead of only in the one-shot Phase 0 probe. Verified before the fix that the gap was real — `grep -c "re-reads" docs/agents/self_drive_protocol.md` printed 0. The reviewer also performed the re-read for this round before authoring: `.agent/STOP` is absent, the operator having removed the sentinel that halted R3's first attempt, and this block keeps the `git status --porcelain` gate the counter-measure requires.

Commit subject: `docs(f045): resolve R-0344 to R-0347`

═══ ITEM 3 · C2 — DECISIONs D4 and D5 ═══
File `.agent/decisions.md`. APPEND at the very END, preceded by one blank line.
Change nothing above it.

## DECISION F045 D4 (2026-08-13) — `action.mission` is a GOAL TEMPLATE, validated like `goal_template`

`LoopAction.mission` carries a mission's GOAL as operator-authored text, not a
mission id and not a reference to an already-stored mission. A loop that named
an id could not be versioned in the config file this feature requires: the id
does not exist until the mission is created, and it differs per machine. The
text therefore accepts the same `{project}` and `{date}` placeholders as
`action.goal_template`, and `loop_spec._semantic_errors` rejects any OTHER
placeholder at VALIDATION time, mirroring the goal_template rule directly above
it. The feature file's A9 line — "undefined variables fail validation, not
runtime" — is written about goal templates; applying it to only one of the two
operator-authored templates in the same table would be an accident, not a
design.

Alternatives considered: (a) `action.mission` names a stored mission id —
rejected, ids are per-machine runtime values and cannot live in versioned
config; (b) leave the mission text unvalidated — rejected, an undefined
placeholder would then reach `run_loop` and fail at run time, which A9 forbids
for the sibling field.

Reverse this decision by deleting the `action.mission` branch in
`_semantic_errors` and treating the field as an opaque string.

## DECISION F045 D5 (2026-08-13) — a mission-action loop records `loop_ref` on the JOB

`Mission` is a frozen dataclass in `packages/orchestration/mission_state.py`
whose fields are `id`, `project_id`, `goal`, `status`, `created_at`,
`job_links` and `schema_version`, the last pinned to
`MISSION_SCHEMA_VERSION` (currently 1). There is no metadata map, so loop
provenance could only be added as a NEW FIELD, which moves that schema version
— and that schema belongs to F056, not to this feature. A loop's provenance
therefore rides on the JOB the loop materializes, under the
`LOOP_REF_METADATA_KEY` metadata key T002 already established, and the mission
stays reachable from that same job through `metadata["mission_id"]` and through
`mission_state.mission_for_job`. Nothing about the mission record changes, so
no existing mission file needs migrating.

Alternatives considered: (a) add a `loop_ref` field to `Mission` — rejected, it
moves `MISSION_SCHEMA_VERSION` inside another feature's schema from inside this
feature's branch; (b) record nothing for the mission path — rejected, the
feature's Acceptance line requires `loop_ref` visible in evidence, and evidence
is job-shaped.

Reverse this decision by adding the field to `Mission` and bumping
`MISSION_SCHEMA_VERSION` in a round that legitimately owns F056's schema.

Commit subject: `docs(f045): record decisions D4 and D5`

═══ ITEM 4 · C3 — the STOP re-check point (fixes R-0347) ═══
File `docs/agents/self_drive_protocol.md`. APPEND-shaped pair: the TO contains
the FROM verbatim and adds a paragraph after it.
FROM (exactly one line):
Each round is: author → delegate → review → verdict.
TO:
Each round is: author → delegate → review → verdict.

Before AUTHORING each round the reviewer re-reads `.agent/STOP` from disk.
Phase 0 runs once at session start, G6 binds at any point, and a sentinel that
appears mid-session is otherwise invisible until an unrelated gate trips over
it (finding R-0347). Every block's gate list therefore also keeps a
`git status --porcelain` gate, and every handoff that names the next session's
first action names Phase 1 rule 1 before rule 2.

Commit subject: `docs(agents): give the stop sentinel a re-check point`

═══ ITEM 5 · C4 — mission-template validation (DECISION D4) ═══
File `packages/orchestration/loop_spec.py`, function `_semantic_errors`.
APPEND-shaped pair: the TO contains the FROM verbatim.
FROM:
    if spec.action.goal_template:
        for var in _undefined_template_vars(spec.action.goal_template):
            fail(f"goal_template references undefined variable '{var}'",
                 "action.goal_template")

    return errors
TO:
    if spec.action.goal_template:
        for var in _undefined_template_vars(spec.action.goal_template):
            fail(f"goal_template references undefined variable '{var}'",
                 "action.goal_template")

    # DECISION F045 D4: action.mission is an operator-authored goal TEMPLATE
    # too, so the same placeholders fail VALIDATION here rather than surfacing
    # as a run-time error (feature file, A9).
    if spec.action.mission:
        for var in _undefined_template_vars(spec.action.mission):
            fail(f"action.mission references undefined variable '{var}'",
                 "action.mission")

    return errors

Commit subject: `feat(f045): validate the mission action's goal template`

═══ ITEM 6 · C5 — tests for D4 ═══
File `tests/orchestration/test_loop_spec.py`. APPEND two tests at the END,
following the file's existing helper and naming conventions (read the file
first and reuse whatever fixture helper it already has for writing a
`remedy.toml` under `tmp_path`; do not invent a second one).
NOTE (counter-measure for R-0344): neither assertion may match against a string
that carries a filesystem path.
 1. a mission action whose text uses BOTH `{project}` and `{date}` validates
    clean — `validate_loop_specs` returns `[]`.
 2. a mission action whose text uses `{sprint}` produces exactly the one
    message `loop '<name>': action.mission references undefined variable
    'sprint'` — assert the whole returned list equals that single-element list,
    the shape line 115 of this file already uses.
Commit subject: `test(f045): pin the mission template validation`

═══ ITEM 7 · C6 — extract the shared job builder ═══
File `packages/orchestration/loop_run.py`. Pure refactor, NO behaviour change:
extract from `loop_to_job` a module-private `_materialize_loop_job` that owns
the `Job(...)` construction, the `plan_job` call and the save, and have
`loop_to_job` call it. It takes the spec, the already-rendered `prompt`, the
`project_id`, an optional `extra_metadata` mapping merged into the metadata
dict AFTER the three keys T002 established, and the optional `save`. The base
metadata, the `name=prompt[:50]` truncation, the `state=RunState.PENDING`, the
budgets mapping and the `(save or _save_job)` fallback are copied across
unchanged. One-line WHY comment above it saying that one place builds a loop's
job so the job and mission paths cannot drift apart in what provenance they
record. The two local imports stay where they are — inside the function that
performs the work — matching this module's existing shape.
This commit adds no new public name and changes no test. Its gate is that
`python3 -m pytest tests/orchestration/test_loop_run.py -q` still prints the
same count it printed before the refactor; report both numbers.
Commit subject: `refactor(f045): extract the shared loop job builder`

═══ ITEM 8 · C7 — run_loop, the inert notice, and last_run_for_loop ═══
File `packages/orchestration/loop_run.py`. Add, with a one-line WHY comment
directly above every public definition (AGENTS.md Code Discoverability):

  @dataclass(frozen=True)
  class LoopRunOutcome            # fields: job: Job, mission_id: str | None = None,
                                  # notice: str | None = None
  def run_loop(spec, *, project_id: str, date: str | None = None,
               save: Callable[[Job], None] | None = None,
               root: Path | None = None) -> LoopRunOutcome
  def last_run_for_loop(name: str, *, root: Path | None = None) -> Job | None

Extend the module docstring: name F045 T003, DECISION D5, and state that
dispatch across action kinds lives HERE and that `loop_to_job` remains the
job-kind path it always was.

`run_loop` semantics:
- `run_date` is `date` when given, else today's UTC date as `YYYY-MM-DD` from
  `datetime.now(timezone.utc)` — the same default `loop_to_job` uses. Compute
  it ONCE and pass it down, so the job and the mission goal can never be
  rendered against two different dates.
- `notice` is `loop_spec.INERT_TRIGGER_NOTICE` when `spec.is_inert`, else
  `None`. An inert loop still materializes on demand; the notice is how the
  caller says so honestly instead of pretending the trigger fired.
- action kind `job`: delegate to `loop_to_job` with the computed `run_date`,
  return `LoopRunOutcome(job=job, mission_id=None, notice=notice)`.
- action kind `mission` (DECISION D5): raise `LoopRunError` naming the loop if
  `spec.action.mission` is empty; render it with `render_goal_template` to get
  the mission goal; `create_mission(project_id, goal, root=root)`; build the
  job through `_materialize_loop_job` with the rendered goal as the prompt and
  `extra_metadata={"mission_id": mission.id, "mission_role":
  MISSION_ROLE_INITIAL}`; set the job's `mission` field to `mission.goal`, the
  shape `mission_state.start_follow_up` already uses for a mission-linked job;
  then `link_job_to_mission(project_id, mission.id, str(job.id),
  MISSION_ROLE_INITIAL, root=root)`. Return the outcome with `mission_id` set.
  Import the three mission names locally inside the branch, matching this
  module's existing local-import shape.
- any other kind: raise `LoopRunError` naming the loop and the kind.
- APPROVAL SEMANTICS, unchanged and load-bearing: BOTH paths stop at PLANNED.
  Nothing here executes a task, approves a plan or implies `--yes`, and
  `spec.unattended` is still only RECORDED. Say this in `run_loop`'s docstring
  in those terms.

`last_run_for_loop` semantics: read the job store through
`storage.list_jobs_safe(root)`, which ALREADY sorts by `created_at`
DESCENDING, so the FIRST job whose `metadata[LOOP_REF_METADATA_KEY]` equals
*name* is the most recent one — no `max()` and no re-sort. Return `None` when
there is none. Unreadable job files are skipped by that helper; say in the
docstring that a loop whose only run is unreadable reports `None` rather than a
wrong run.
Commit subject: `feat(f045): dispatch a loop action and read its last run`

═══ ITEM 9 · C8 — tests for the dispatch ═══
File `tests/orchestration/test_loop_run.py`. APPEND, reusing the file's
existing spec helpers. Pass an explicit `date` and an explicit `save` list
appender everywhere; pass `root=tmp_path` to everything that touches mission
state, so no test reads or writes the real store.
NOTE (counter-measure for R-0344): no assertion may match against a string that
carries a filesystem path.
Cover exactly these, one test each:
 1. `run_loop` on a job-action loop returns an outcome whose job is PLANNED and
    carries `loop_ref`, and whose `mission_id` is None
 2. `run_loop` on a mission-action loop creates a mission whose `goal` is the
    RENDERED template, and `outcome.mission_id` equals that mission's id
 3. the mission path's job carries `loop_ref` in metadata AND
    `metadata["mission_id"]` — the DECISION D5 pin. Also assert
    `hasattr(mission, "loop_ref") is False`, so this test goes red the day
    someone moves provenance onto the frozen Mission record
 4. the mission job is that mission's INITIAL link: reload the mission with
    `mission_state.load_mission(project_id, mission_id, root=tmp_path)` and
    assert its single job link's `job_id` equals `str(job.id)` and its role is
    `MISSION_ROLE_INITIAL`
 5. `unattended = true` on a MISSION loop is recorded and the job's state is
    still PLANNED, identical to the attended case — assert both states equal
    and PLANNED. This is the "a loop never implies --yes" pin for the mission
    path, the mirror of the T002 job-path pin
 6. a `schedule`-trigger loop yields `outcome.notice ==
    loop_spec.INERT_TRIGGER_NOTICE` and STILL produces a PLANNED job
 7. a `manual`-trigger loop yields `outcome.notice is None`
 8. a mission-action loop with an unsupported placeholder never reaches
    `run_loop`: `validate_loop_specs` reports it, which is DECISION D4's whole
    point. Assert the returned list is the single expected message
 9. `last_run_for_loop` returns the most recent job for that loop name, and
    `None` for a name no job carries
10. `last_run_for_loop` ignores a job whose `loop_ref` is a DIFFERENT loop
For tests 9 and 10 build the `Job` objects directly with explicit distinct
`created_at` values and explicit `metadata={LOOP_REF_METADATA_KEY: ...}`, and
persist them with `storage.save_job(job, tmp_path)`; then call
`last_run_for_loop(name, root=tmp_path)`. Building them by hand is deliberate
here and is NOT a deviation from the T002 rule that specs come from a real
`remedy.toml`: the subject under test is the job-store scan and its ordering,
and two jobs materialized in the same test would share a clock reading fine
enough to make "most recent" ambiguous.
Commit subject: `test(f045): pin loop dispatch and the last-run lookup`

═══ ITEM 10 · C9 — plan and handoff ═══
Rewrite `.agent/plan.md` (AGENTS.md: under 50 lines, keeps `## Goal` and
`## Next Steps`): Current Step becomes R3 done — findings R-0344 to R-0347
resolved, D4 and D5 landed, dispatch and last-run built; R4 = the CLI. Open
findings becomes 0; next free finding ID stays R-0348. Fortschritt becomes
`Fortschritt: ~55 % (T001 ✅ · T002 ✅ · T003 läuft) — Schätzung`. Keep the
existing Risks, drop the third one (dispatch now exists) and add: the mission
path writes real mission records, so every test that touches it must pass an
explicit `root`.
Then rewrite `.agent/handoff.md` per the AGENTS.md handoff contract (≤60 lines,
or a "Deviations, declared" line naming the real count and the mandated content
that caused it; sections are NEVER dropped). It carries: feature + round,
branch, every commit SHA, a per-commit changed-files table, the raw results of
ITEM 11's gates, open-findings count 0, an item-status table with one row per
ITEM 1-11, the next expected action, and the Fortschritt line verbatim. The
"next expected action" section names Phase 1 rule 1 (read `.agent/STOP` from
disk) BEFORE rule 2 (the Open PR Gate) — this is the R-0347 counter-measure and
its absence is a finding.
Commit subject: `docs(f045): update the plan and handoff for R3`

═══ ITEM 11 · gates ═══
Run every command; record the REAL exit code and REAL output. Report counts as
OBSERVED — do not predict them and do not restate a count this block gave you.

(a) cmp .agent/authored/f045-r3-1.md .agent/last_block.md
(b) grep -c "^Done: R-0344" .agent/live_review.md              → 1
(c) grep -c "^Done: R-0347" .agent/live_review.md              → 1
(d) grep -c "^## DECISION F045 D" .agent/decisions.md          → 5
(e) grep -c "re-reads" docs/agents/self_drive_protocol.md      → 1
(f) python3 -m pytest tests/orchestration/test_loop_run.py tests/orchestration/test_loop_spec.py -q
(g) python3 -m pytest tests/test_agent_tooling.py -q
(h) python3 -m pytest tests/docs/ -q
(i) python3 -m pytest tests/cli/test_golden_path.py -q      (canary)
(j) python3 -m ruff check packages/orchestration/loop_run.py packages/orchestration/loop_spec.py tests/orchestration/test_loop_run.py tests/orchestration/test_loop_spec.py
(k) git status --porcelain                                  → EMPTY

Gates (b)-(e) are scoped to their target FILE, never to this block or to
`.agent/authored/**`, both of which legitimately contain the same strings.

Push after EVERY commit: `git push origin feature/f045-loop-definitions`.
Do NOT open a PR and do NOT merge anything.

If any gate is RED, or anything here contradicts AGENTS.md or the disk: STOP,
commit nothing further, and report the exact blocker with its raw output. A
halted round with an honest blocker is a success; a green word over a red run
is a finding.
END BLOCK f045-r3-1
