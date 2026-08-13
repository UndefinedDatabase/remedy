BEGIN BLOCK f045-r5-1
── STEP T003b/3 — F045 Loop definitions · ROUND 5 (the action dispatch) ──

Goal:        Build the loop action dispatch — `run_loop` across the job and
             mission kinds, the honest inert-trigger notice, and
             `last_run_for_loop` — register R-0350 and close R-0348/R-0349.
Bundle:      ITEM 1 C0a+C0b save block · ITEM 2 C1 register R-0350 · ITEM 3 C2
             resolve R-0348/R-0349 · ITEM 4 C3 extract the shared job builder ·
             ITEM 5 C4 run_loop and last_run_for_loop · ITEM 6 C5 their tests ·
             ITEM 7 C6 the reachability probe · ITEM 8 C7 plan + handoff ·
             ITEM 9 gates.
Change:      .agent/authored/f045-r5-1.md · .agent/last_block.md ·
             .agent/live_review.md · packages/orchestration/loop_run.py ·
             tests/orchestration/test_loop_run.py · .agent/plan.md ·
             .agent/handoff.md. Nothing else. Do NOT edit loop_spec.py,
             test_loop_spec.py, mission_state.py, storage.py, job_runner.py,
             packages/core/models.py, .agent/decisions.md or anything under
             apps/.
Constraints: SPLIT round. Never work on main; never force-push; no PR; merge
             nothing. Do-not-touch (feature file): scheduling/cron, the routine
             library, notifications. This round adds NO CLI — that is R6.
             ITEM 7's mutation runs ONLY inside a disposable git worktree under
             `.remedy-wt/` (gitignored scratch), never in the primary checkout,
             which must satisfy an empty `git status --porcelain` at handback.
Insertion budget, per commit: C0a ≈ block size · C0b ≈ block size · C1 ≤ 8 ·
             C2 ≤ 8 · C3 ≤ 55 · C4 ≤ 105 · C5 ≤ 175 · C7 ≤ 115. ITEM 1 is two
             commits because two small commits are more reviewable than one and
             it takes the cap question off the table at commit time — not
             because of a measured size (finding R-0350). No commit bundles a
             module with its test file.
Done when:   every gate in ITEM 9 has been RUN and its real exit code and
             output recorded.
Handback:    completion report + rewrite .agent/handoff.md

═══ ITEM 1 · C0a and C0b — save this block verbatim ═══
C0a: write the block bytes (BEGIN..END markers included) to
`.agent/authored/f045-r5-1.md`. No trailing whitespace on any line.
Commit subject: `chore(f045): save the R5 block verbatim`
C0b: copy that file over `.agent/last_block.md`, replacing the R4 block.
Commit subject: `chore(f045): point last_block at the R5 block`
Prove it: cmp .agent/authored/f045-r5-1.md .agent/last_block.md → exit 0

═══ ITEM 2 · C1 — register R-0350 ═══
File `.agent/live_review.md`. APPEND at the END of the `## Findings` section,
after R-0349's paragraph, one blank line between paragraphs. One line:

- R-0350 — Low — a block's stated reason for a correct instruction was arithmetic it had not done. The R4 block's insertion-budget clause ordered ITEM 1 as two commits "because one commit carrying both copies of the block exceeds the 500-insertion cap". The disk disagrees: `git log --numstat` shows C0a `99ecc0c5` at 246 insertions and C0b `aa019a46` at 158, so one combined commit would have been 404 — under the cap. `.agent/last_block.md` is in any case a single `.agent/**` state file whose verbatim rewrite is cap-EXEMPT by DECISION F104 D1, so the cap was never the constraint. The instruction itself was right for reasons the block did not give: two small commits review better than one, and splitting removes a cap question from commit time. The worker followed it and reported the false reason instead of quietly accepting it, which is the behaviour that keeps a block honest. Nothing landed wrong. This is the R-0336/R-0345 family once more — a number asserted rather than computed from the artifact that produces it. Counter-measure, applied from R5 on: a block that justifies an instruction with a size claim either states the measured figures or gives the non-numeric reason instead. OPEN.

Commit subject: `docs(f045): register R-0350, the unmeasured size claim`

═══ ITEM 3 · C2 — resolve R-0348 and R-0349 ═══
File `.agent/live_review.md`. Two APPEND-shaped edits: each paragraph keeps its
bytes and gains a `Done:` line directly below it, one blank line between. The
trailing `OPEN.` inside each paragraph stays. R-0350 gets no `Done:` line.

Below R-0348's paragraph:
Done: R-0348 — RESOLVED at the R5 gate. Verified against the disk, not the report: `.agent/decisions.md` D5 now quotes `Mission`'s own class docstring — "ADDITIVE and OPTIONAL" and "which is why :data:`MISSION_SCHEMA_VERSION` does NOT move for it" — and states in its own paragraph that the schema cost is explicitly NOT the reason for the decision, so the entry no longer contradicts the module it describes. Its reversal clause now names the additive-field route and warns that bumping `MISSION_SCHEMA_VERSION` makes `Mission.from_json` raise `unknown mission schema version` for every record already stored. The counter-measure is applied rather than promised: the decision quotes the sentence that establishes the cost it talks about.

Below R-0349's paragraph:
Done: R-0349 — RESOLVED at the R5 gate. Verified against the disk, not the report: the R4 decision text cites `mission_state.continue_mission` at `packages/orchestration/mission_state.py:893`, which is where `grep -n "def continue_mission"` puts it, and `grep -rn "start_follow_up" --include=*.py .` still returns nothing, so the phantom symbol appears nowhere in the repository. The counter-measure is applied in the R5 block itself: every symbol it cites as precedent was grepped to its own definition before emission and carries its `file:line`.

Commit subject: `docs(f045): resolve R-0348 and R-0349`

═══ ITEM 4 · C3 — extract the shared job builder ═══
File `packages/orchestration/loop_run.py`. Pure refactor, NO behaviour change.
Extract from `loop_to_job` a module-private `_materialize_loop_job` that owns
the `Job(...)` construction, the `plan_job` call and the save; have
`loop_to_job` call it. Parameters: the spec, the already-rendered `prompt`, the
`project_id`, an optional `extra_metadata` mapping merged into the metadata
dict AFTER the three keys T002 established, and the optional `save`. Copy
across unchanged: the base metadata, `name=prompt[:50]`,
`state=RunState.PENDING`, the budgets mapping and the `(save or _save_job)`
fallback. The two local imports (`plan_job` from
`packages.orchestration.job_runner:46`, `save_job` from
`packages.orchestration.storage:75`) move into the helper, matching this
module's existing local-import shape. One-line WHY comment above it: one place
builds a loop's job, so the job and mission paths cannot drift apart in what
provenance they record.
This commit adds no public name and changes no test. Its gate: run
`python3 -m pytest tests/orchestration/test_loop_run.py -q` BEFORE and AFTER
the edit and report BOTH counts as observed.
Commit subject: `refactor(f045): extract the shared loop job builder`

═══ ITEM 5 · C4 — run_loop, the inert notice, and last_run_for_loop ═══
File `packages/orchestration/loop_run.py`. Add, with a one-line WHY comment
directly above every public definition (AGENTS.md Code Discoverability):

  @dataclass(frozen=True)
  class LoopRunOutcome        # job: Job · mission_id: str | None = None ·
                              # notice: str | None = None
  def run_loop(spec: LoopSpec, *, project_id: str, date: str | None = None,
               save: Callable[[Job], None] | None = None,
               root: Path | None = None) -> LoopRunOutcome
  def last_run_for_loop(name: str, *, root: Path | None = None) -> Job | None

Extend the module docstring: name F045 T003, say that dispatch across action
kinds lives HERE while `loop_to_job` remains the job-kind path it always was,
and name DECISION F045 D5 for the mission path's provenance.

`run_loop` semantics:
- Compute `run_date` ONCE — `date` when given, else today's UTC date as
  `YYYY-MM-DD` from `datetime.now(timezone.utc)`, the same default
  `loop_to_job` already uses — and pass it down, so the job and the mission
  goal can never be rendered against two different dates.
- `notice` is `loop_spec.INERT_TRIGGER_NOTICE` when `spec.is_inert`, else
  `None`. An inert loop still materializes on demand; the notice is how a
  caller says so honestly instead of pretending the trigger fired.
- kind `job`: delegate to `loop_to_job` with the computed `run_date`; return
  `LoopRunOutcome(job=job, mission_id=None, notice=notice)`.
- kind `mission` (DECISION F045 D5): raise `LoopRunError` naming the loop when
  `spec.action.mission` is empty; render it with `render_goal_template` to get
  the mission goal; call `create_mission(project_id, goal, root=root)`
  (`mission_state.py:387`); build the job through `_materialize_loop_job` with
  that rendered goal as the prompt and
  `extra_metadata={"mission_id": mission.id, "mission_role": MISSION_ROLE_INITIAL}`
  (`MISSION_ROLE_INITIAL` is `mission_state.py:79`); set the job's `mission`
  field to `mission.goal` — the shape `mission_state.continue_mission`
  (`mission_state.py:893`) uses at `mission_state.py:948`; then call
  `link_job_to_mission(project_id, mission.id, str(job.id),
  MISSION_ROLE_INITIAL, root=root)` (`mission_state.py:432`). Return the
  outcome with `mission_id` set. Import the three mission names locally inside
  the branch, matching this module's existing local-import shape.
- any other kind: raise `LoopRunError` naming the loop and the kind.
- APPROVAL SEMANTICS, unchanged and load-bearing: BOTH paths stop at PLANNED.
  Nothing here executes a task, approves a plan or implies `--yes`, and
  `spec.unattended` is still only RECORDED. Say this in `run_loop`'s docstring
  in those terms.

`last_run_for_loop` semantics: read the job store through
`storage.list_jobs_safe(root)` (`storage.py:123`), which ALREADY sorts by
`created_at` DESCENDING, so the FIRST job whose
`metadata[LOOP_REF_METADATA_KEY]` equals *name* is the most recent — no `max()`
and no re-sort. Return `None` when there is none. Say in the docstring that
unreadable job files are skipped by that helper, so a loop whose only run is
unreadable reports `None` rather than a wrong run.
Commit subject: `feat(f045): dispatch a loop action and read its last run`

═══ ITEM 6 · C5 — tests for the dispatch ═══
File `tests/orchestration/test_loop_run.py`. APPEND, reusing the file's
existing spec helpers. Pass an explicit `date` and an explicit `save` list
appender everywhere, and pass `root=tmp_path` to everything that touches
mission state or the job store, so no test reads or writes the real store.
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
    `mission_state.load_mission(project_id, mission_id, root=tmp_path)`, assert
    its single job link's `job_id` equals `str(job.id)` and its role is
    `MISSION_ROLE_INITIAL`
 5. `unattended = true` on a MISSION loop is recorded and the job's state is
    still PLANNED, identical to the attended case — assert both states are
    equal and PLANNED. This is the "a loop never implies --yes" pin for the
    mission path, mirroring the T002 job-path pin
 6. a `schedule`-trigger loop yields `outcome.notice` equal to
    `loop_spec.INERT_TRIGGER_NOTICE` and STILL produces a PLANNED job
 7. a `manual`-trigger loop yields `outcome.notice is None`
 8. `last_run_for_loop` returns the most recent job for that loop name, and
    `None` for a name no job carries
 9. `last_run_for_loop` ignores a job whose `loop_ref` names a DIFFERENT loop
For tests 8 and 9 build the `Job` objects directly with explicit DISTINCT
`created_at` values and explicit `metadata={LOOP_REF_METADATA_KEY: ...}`, and
persist them with `storage.save_job(job, tmp_path)` (`storage.py:75`); then
call `last_run_for_loop(name, root=tmp_path)`. Hand-building them is deliberate
and is NOT a deviation from the T002 rule that specs come from a real
`remedy.toml`: the subject under test is the job-store scan and its ordering,
and two jobs materialized inside one test would share a clock reading too
closely for "most recent" to mean anything.
Commit subject: `test(f045): pin loop dispatch and the last-run lookup`

═══ ITEM 7 · C6 — the reachability probe (no commit) ═══
Prove the DECISION D5 pin is discriminating rather than decorative. Do this
ONLY in a disposable worktree:
  git worktree add .remedy-wt/r5probe HEAD
In that worktree, change `run_loop`'s mission branch to pass
`extra_metadata={}` instead of the mission keys, then run
`python3 -m pytest tests/orchestration/test_loop_run.py -q` FROM INSIDE the
worktree and report WHICH tests fail and how many — the colour is not ordered,
the observation is. Before running, prove the import path with
`python3 -c "import packages.orchestration.loop_run as m; print(m.__file__)"`
and report that line: a probe run from the primary checkout imports unmutated
code and proves nothing (finding R-0337). Then remove the worktree with
`git worktree remove --force .remedy-wt/r5probe` and `git worktree prune`, and
report `git worktree list`. No commit comes from this item.

═══ ITEM 8 · C7 — plan and handoff (session-closing) ═══
Rewrite `.agent/plan.md` (under 50 lines, keeps `## Goal` and `## Next
Steps`): Current Step becomes R5 done — dispatch, the inert notice and the
last-run lookup built; R-0348/R-0349 resolved, R-0350 registered; R6 = the CLI
(`remedy loop list | validate | run`), then the integration gate, then closure.
Open findings becomes 1 (R-0350); next free finding ID R-0351. Fortschritt
becomes `Fortschritt: ~60 % (T001 ✅ · T002 ✅ · T003 läuft) — Schätzung`. Keep
the config-file risk and the inert-trigger risk; replace the third with: the
mission path writes real mission records, so every test touching it passes an
explicit `root`.
Then rewrite `.agent/handoff.md` per the AGENTS.md handoff contract (≤60 lines,
or a "Deviations, declared" line naming the real count and the mandated content
that caused it; sections are NEVER dropped). It carries: feature + round,
branch, every commit SHA, a per-commit changed-files table, the raw results of
ITEM 9's gates AND of ITEM 7's probe, open-findings count 1, an item-status
table with one row per ITEM 1-9, the next expected action, and the Fortschritt
line verbatim. The "next expected action" section names Phase 1 rule 1 (read
`.agent/STOP` from disk) BEFORE rule 2 (the Open PR Gate) — the R-0347
counter-measure; its absence is a finding. Because this closes the session, the
handoff also states that the branch has no PR, that nothing was merged, and
that R6 is the CLI round.
Commit subject: `docs(f045): update the plan and handoff for R5`

═══ ITEM 9 · gates ═══
Run every command; record the REAL exit code and REAL output. Report counts as
OBSERVED — do not predict them and do not restate a count this block gave you.

(a) cmp .agent/authored/f045-r5-1.md .agent/last_block.md
(b) grep -c "^- R-0350 — Low" .agent/live_review.md
(c) grep -c "^Done: R-" .agent/live_review.md
(d) python3 -m pytest tests/orchestration/test_loop_run.py tests/orchestration/test_loop_spec.py -q
(e) python3 -m pytest tests/docs/ -q
(f) python3 -m pytest tests/cli/test_golden_path.py -q      (canary)
(g) python3 -m ruff check packages/orchestration/loop_run.py tests/orchestration/test_loop_run.py
(h) git worktree list                                       → one line only
(i) git status --porcelain                                  → EMPTY

Gates (b) and (c) are scoped to `.agent/live_review.md`, never to this block or
to `.agent/authored/**`, both of which legitimately contain the same strings.

Push after EVERY commit: `git push origin feature/f045-loop-definitions`.
Do NOT open a PR and do NOT merge anything.

If any gate is RED, or anything here contradicts AGENTS.md or the disk: STOP,
commit nothing further, and report the exact blocker with its raw output.
END BLOCK f045-r5-1
