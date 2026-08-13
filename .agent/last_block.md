BEGIN BLOCK f045-r7
── STEP T003b/4 — F045 Loop definitions · ROUND 7 ────────────────────────

Goal:        Fix R-0351 and R-0352. The job a loop firing PERSISTS must carry
             the mission text, and `run_loop(root=X)` must put that job in X's
             store rather than in the process-wide one. Pin both with tests
             that read the STORE, not the `save` callable.
Bundle:      ITEM 1 C0a+C0b save block · ITEM 2 C1 loop_run.py · ITEM 3 C2
             tests · ITEM 4 C3 decisions.md · ITEM 5 C4 plan + handoff ·
             ITEM 6 gates, including the red-proof.
Change:      .agent/authored/f045-r7.md · .agent/last_block.md ·
             packages/orchestration/loop_run.py ·
             tests/orchestration/test_loop_run.py · .agent/decisions.md ·
             .agent/plan.md · .agent/handoff.md. Nothing else. Do NOT touch
             apps/ or docs/ — the CLI is R8's work. `.agent/live_review.md` is
             deliberately NOT in this change set: the `Done:` lines for R-0351
             and R-0352 are the reviewer's to author next round, after the
             reviewer has verified this one. Writing them yourself would
             certify your own repair.
Constraints: Never work on main; never force-push; no PR; merge nothing. The
             red-proof runs ONLY inside a disposable git worktree under
             `.remedy-wt/` (gitignored at .gitignore:235) with REMEDY_DATA_DIR
             pointed inside that worktree — never in the primary checkout,
             whose `git status --porcelain` must be empty at handback.
Insertion budget, per commit: C0a and C0b ≈ block size (single `.agent/**`
             state-file rewrites, cap-exempt by DECISION F104 D1) · C1 ≤ 40 ·
             C2 ≤ 70 · C3 ≤ 45 · C4 ≤ 130. Every figure is far under the
             AGENTS.md 500-insertion cap; the split exists so a code commit and
             its test commit stay separate (R-0345 counter-measure), not
             because any commit approaches the cap.
Done when:   every gate in ITEM 6 has been RUN and its real output recorded.
Handback:    completion report + rewrite .agent/handoff.md

Citations, re-measured at emission against tip `3cbcbd4c` (R-0353
counter-measure). Check each one before relying on it:
  packages/orchestration/loop_run.py:131  def _materialize_loop_job(...)
  packages/orchestration/loop_run.py:159  (save or _save_job)(job)
  packages/orchestration/loop_run.py:165  def loop_to_job(...)
  packages/orchestration/loop_run.py:195  the loop_to_job call to the helper
  packages/orchestration/loop_run.py:215  def run_loop(...)
  packages/orchestration/loop_run.py:240  the job-kind call to loop_to_job
  packages/orchestration/loop_run.py:257  the mission-kind call to the helper
  packages/orchestration/loop_run.py:262  job.mission = mission.goal
  packages/orchestration/storage.py:44    def _resolve_jobs_dir(root=None)
  packages/orchestration/storage.py:75    def save_job(job, root=None)
  packages/orchestration/storage.py:83    def load_job(job_id, root=None)
  packages/core/models.py:227             mission: str | None = None

═══ ITEM 1 · C0a and C0b — save this block verbatim ═══
C0a: write the block bytes (BEGIN..END markers included) to
`.agent/authored/f045-r7.md`. No trailing whitespace on any line.
Commit subject: `chore(f045): save the R7 block verbatim`
C0b: copy that file over `.agent/last_block.md`, replacing the R6 block.
Commit subject: `chore(f045): point last_block at the R7 block`
Prove it: cmp .agent/authored/f045-r7.md .agent/last_block.md → exit 0

═══ ITEM 2 · C1 — packages/orchestration/loop_run.py ═══
Five changes in this one file. Write the code yourself; what is fixed below is
the SEMANTICS, not the characters.

(1) `_materialize_loop_job` gains two keyword-only parameters:
    `mission: str | None = None` and `root: Path | None = None`.

(2) The mission text is passed into the `Job(...)` constructor as `mission=`,
    so it is set BEFORE `plan_job(job)` and before the save. This is the shape
    the precedent uses: `mission_state.continue_mission` sets
    `mission=mission.goal` inside its own `Job(...)` call. `grep -n "def
    continue_mission" packages/orchestration/mission_state.py` and
    `grep -n "mission=mission.goal" packages/orchestration/mission_state.py`
    locate both; check them rather than trusting this sentence.

(3) The save stops discarding `root`. When the caller passed an explicit
    `save` callable, call it with the job and nothing else — its declared type
    is `Callable[[Job], None]` and must NOT change. Otherwise call
    `storage.save_job(job, root)` with the root. Do not unify the two by
    giving `save` a second parameter: every existing caller passes a
    one-argument list-appender and would break.

(4) `loop_to_job` gains a keyword-only `root: Path | None = None` and forwards
    it to the helper, so the JOB action path isolates exactly as the mission
    path does.

(5) `run_loop` passes `root=root` on BOTH branches, passes `mission=mission.goal`
    into the helper on the mission branch, and the post-hoc assignment
    `job.mission = mission.goal` is DELETED. That assignment is the defect: it
    runs after the record is already on disk.

Docstrings: `_materialize_loop_job`'s gains one sentence stating that the
mission text is set in the constructor, before the save, so the PERSISTED
record carries it; and one stating that an explicit `save` overrides `root`
entirely, because such a caller has taken responsibility for where the job
goes. `loop_to_job`'s and `run_loop`'s each gain a line naming what `root`
isolates. Do not restate the fix in a comment on top of that.

Commit subject: `fix(f045): persist the mission text and honour root when saving`

═══ ITEM 3 · C2 — tests/orchestration/test_loop_run.py ═══
First, the module docstring. It currently says every call passes an explicit
`save` callable so no test touches the real job store. The three tests below
pass NO `save`, so that sentence is about to become false — a stale contract in
a header is a finding. Replace it with a sentence that stays true: most calls
pass an explicit `save`; the store tests pass none and isolate through `root`
instead, which is the very property they exist to prove.

Then add exactly three tests at the END of the file.

(1) `test_mission_run_persists_the_mission_text_on_the_stored_job`
    Build a mission loop with the existing `_mission_loop(tmp_path)` helper.
    Call `run_loop(spec, project_id="remedy", date="2026-08-13", root=tmp_path)`
    with NO `save`. Read the record back with
    `storage.load_job(outcome.job.id, tmp_path)` and assert the STORED job's
    `mission` equals the rendered goal. Assert against the stored object and
    never against `outcome.job`: reading the in-memory object is precisely the
    defect R-0351 names, and a test that does it passes either way.

(2) `test_run_loop_root_isolates_the_job_store_on_the_mission_path`
    Same call shape, no `save`. Then `last_run_for_loop(spec.name, root=tmp_path)`
    must return a job whose `id` equals `outcome.job.id`. This is the pin
    R-0352 asks for: run with `root`, find it with the SAME `root`.

(3) `test_run_loop_root_isolates_the_job_store_on_the_job_path`
    The same, through `_job_loop(tmp_path)` and the job action kind.

Every expected value is computed from the spec or from the module under test.
`tmp_path` may be PASSED as `root` but must never appear inside an expected
string (R-0344 counter-measure: no assertion matches a string carrying a
filesystem path).

Commit subject: `test(f045): pin the persisted mission text and root isolation`

═══ ITEM 4 · C3 — .agent/decisions.md, DECISION F045 D6 ═══
Append after D5, in the same heading shape as the five F045 decisions already
there:
`## DECISION F045 D6 (2026-08-14) — an explicit save callable overrides root; root steers only the DEFAULT save`

Write the body yourself, covering exactly these four things and no padding:
- WHAT: `_materialize_loop_job` takes both `save` and `root`; when `save` is
  given it is called with the job alone and `root` is not consulted.
- WHY: `save` exists so a caller can capture the job without a store at all,
  and every current caller passes a one-argument list-appender. Giving `save` a
  root argument would break all of them and would ask a test double to honour a
  path it has no store behind.
- The alternative considered and rejected: drop `save` entirely and make every
  test pass `root`. Rejected because the store round-trip is the subject of only
  three tests; forcing the other twenty through a real store would make every
  one of them slower and none of them stricter.
- HOW TO REVERSE: change `save`'s annotation from `Callable[[Job], None]` to one
  that also takes the root, and update every caller in
  `tests/orchestration/test_loop_run.py`.

Commit subject: `docs(f045): record DECISION F045 D6 on save versus root`

═══ ITEM 5 · C4 — .agent/plan.md and .agent/handoff.md ═══
Rewrite `.agent/plan.md` (under 50 lines, keeping `## Goal`, `## Current Step`,
`## Next Steps`, `## Risks`): Current Step becomes R7 — R-0351 and R-0352 are
fixed in code and pinned, awaiting the reviewer's verdict and the reviewer's
`Done:` lines. Open findings stay 4 (R-0350, R-0351, R-0352, R-0353 — the last
two are fixed but NOT yet marked resolved, because only the reviewer closes a
finding); next free finding ID stays R-0354. Next Steps become: R8 is the CLI —
`remedy loop list`, `remedy loop validate`, `remedy loop run <name> [--yes]`,
the last-run display and the end-to-end fixture loop; then the integration gate;
then closure per docs/roadmap/STATUS_closure_protocol.md. In Risks, DELETE the
third risk (the two-root-resolutions one) — this round is what removes it — and
keep the config-file and inert-trigger risks. Keep the Fortschritt line
`Fortschritt: ~60 % (T001 ✅ · T002 ✅ · T003 läuft) — Schätzung` verbatim.

Then rewrite `.agent/handoff.md` per the AGENTS.md handoff contract (≤60 lines,
or a "Deviations, declared" line naming the real count and the mandated content
that caused it; sections are NEVER dropped). It carries: feature + round and
branch; every commit SHA of this round with its changed files; the ITEM 6 gate
table with REAL exit codes and REAL output, the red-proof included and reported
as a COLOUR; open-findings count 4 naming all four; an item-status table with
one row per ITEM 1-6; the statement that no PR is open, nothing was merged, main
was never touched, no force-push occurred and no worktree was left behind; the
next expected action, which names Phase 1 rule 1 (read `.agent/STOP` from disk)
BEFORE rule 2 (the Open PR Gate), then R8's CLI work; and the Fortschritt line.
Commit subject: `docs(f045): hand back R7 with the persisted-job fixes`

═══ ITEM 6 · gates ═══
Run every command. Record the REAL exit code and REAL output. Report every
count as OBSERVED — do not predict one and do not restate a number this block
gave you. For any test command, report the COLOUR (passed / failed) first; the
count is a note, never the assertion.

(a) cmp .agent/authored/f045-r7.md .agent/last_block.md
(b) grep -n "job.mission = mission.goal" packages/orchestration/loop_run.py
    → must return NOTHING (exit 1). The deleted assignment is the fix.
(c) python3 -m pytest tests/orchestration/test_loop_run.py tests/orchestration/test_loop_spec.py -q
(d) python3 -m pytest tests/cli/test_golden_path.py -q            (canary)
(e) python3 -m ruff check packages/orchestration/loop_run.py tests/orchestration/test_loop_run.py
(f) git diff --name-only 3cbcbd4c..HEAD
    → must list the seven files in Change and nothing else; in particular
      `.agent/live_review.md` must NOT appear.
(g) RED-PROOF, and it runs ONLY in a disposable worktree (guardrail G5).
    After C1 and C2 are committed:
      git worktree add .remedy-wt/f045_r7 3cbcbd4c
      cp tests/orchestration/test_loop_run.py .remedy-wt/f045_r7/tests/orchestration/test_loop_run.py
      cd .remedy-wt/f045_r7
      python3 -c "import packages.orchestration.loop_run as m; print(m.__file__)"
        → MUST print a path UNDER .remedy-wt/f045_r7. If it prints the primary
          checkout's path, the probe would be importing the FIXED module and
          would prove nothing (finding R-0337): STOP and report.
      REMEDY_DATA_DIR="$PWD/.scratch_data" python3 -m pytest tests/orchestration/test_loop_run.py -k "persists_the_mission_text or root_isolates" -q
        → the three new tests must FAIL against the pre-fix module. Report the
          COLOUR. REMEDY_DATA_DIR is set precisely because the pre-fix code
          ignores `root`; without it the red run would write into the
          operator's real job store.
      then leave the worktree and: git worktree remove .remedy-wt/f045_r7 --force
    If the three tests PASS against the pre-fix module, the tests do not pin
    what they claim to pin: STOP and report, do not "strengthen" them silently.
(h) git status --porcelain                        → EMPTY
(i) git worktree list                             → ONE line, after the removal

Push after EVERY commit: `git push origin feature/f045-loop-definitions`.
Do NOT open a PR and do NOT merge anything.

If any gate is RED, or anything here contradicts AGENTS.md or the disk: STOP,
commit nothing further, and report the exact blocker with its raw output.
END BLOCK f045-r7
