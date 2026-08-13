BEGIN BLOCK f045-r8
── STEP T003c/5 — F045 Loop definitions · ROUND 8 ────────────────────────

Goal:        Close R-0351 and R-0352 in the review record with the reviewer's
             own verified text, register R-0354, and land the READ-ONLY half of
             the T003 CLI: `remedy loop list` and `remedy loop validate`,
             reachable through the real handler table rather than merely
             importable.
Bundle:      ITEM 1 C0a+C0b save block · ITEM 2 C1 live_review · ITEM 3 C2 the
             loop command module and its wiring · ITEM 4 C3 tests · ITEM 5 C4
             plan + handoff · ITEM 6 gates.
Change:      .agent/authored/f045-r8.md · .agent/last_block.md ·
             .agent/live_review.md · apps/cli/commands/loop_cmd.py (NEW) ·
             apps/cli/command_catalog.py · apps/cli/commands/__init__.py ·
             tests/cli/test_loop_cmd.py (NEW) · .agent/plan.md ·
             .agent/handoff.md. Nine files, nothing else.
             `remedy loop run` is R9's work — do NOT write it this round.
             `packages/orchestration/loop_run.py` and
             `tests/orchestration/test_loop_run.py` are NOT in this change set:
             R7's code is reviewed and PASSED, and touching it now would put a
             repair on top of a verdict.
             No `docs/` file changes: this repository has no ist-doc that
             enumerates CLI commands — `apps/cli/command_catalog.py` IS that
             reference, and it is in the change set. Do not create one.
Constraints: Never work on main; never force-push; no PR; merge nothing. Any
             red-proof runs ONLY inside a disposable git worktree under
             `.remedy-wt/` (gitignored at .gitignore:235), never in the primary
             checkout, whose `git status --porcelain` must be empty at handback.
             No test may read or write the operator's real job store; gate (l)
             checks that it did not.
Insertion budget, per commit: C0a and C0b ≈ block size (single `.agent/**`
             state-file rewrites, cap-exempt by DECISION F104 D1) · C1 ≤ 10 ·
             C2 ≤ 170 · C3 ≤ 140 · C4 ≤ 130. Every figure is far under the
             AGENTS.md 500-insertion cap.
Done when:   every gate in ITEM 6 has been RUN and its real output recorded.
Handback:    completion report + rewrite .agent/handoff.md

Symbols cited as precedent, grepped to their own definitions at emission
(R-0349 and R-0353 counter-measures — prefer the symbol over a bare line
number, and check each before relying on it):
  `COMMAND_HANDLERS`            apps/cli/commands/queue_cmd.py — the per-module
                                handler dict, keyed by command_id
  `collect_all_handlers`        apps/cli/commands/__init__.py — imports every
                                command module and merges their COMMAND_HANDLERS;
                                a module absent from BOTH its import list and its
                                `for mod in (...)` tuple is unreachable
  `CommandEntry`, `GroupDef`,
  `ArgDef`, `GROUPS`, `CATALOG` apps/cli/command_catalog.py
  `load_loop_specs`,
  `validate_loop_specs`,
  `INERT_TRIGGER_NOTICE`,
  `LoopSpecError`, `LoopSpec`   packages/orchestration/loop_spec.py
  `last_run_for_loop`           packages/orchestration/loop_run.py
  `EXIT_ERROR`                  apps/cli/commands/queue_cmd.py
Contracts you will rely on, and which you should confirm by reading them:
  `load_loop_specs(project_path=None)` raises on the FIRST error; a missing
  file is NOT an error and yields `()`.
  `validate_loop_specs(project_path=None)` NEVER raises and returns EVERY
  error message in file order; a missing file yields `[]`.
  Both default to `Path("remedy.toml")`, which is CWD-relative.
  `LoopSpec.is_inert` is True exactly for the schedule and event trigger kinds.

═══ ITEM 1 · C0a and C0b — save this block verbatim ═══
C0a: write the block bytes (BEGIN..END markers included) to
`.agent/authored/f045-r8.md`. No trailing whitespace on any line.
Commit subject: `chore(f045): save the R8 block verbatim`
C0b: copy that file over `.agent/last_block.md`, replacing the R7 block.
Commit subject: `chore(f045): point last_block at the R8 block`
Prove it: cmp .agent/authored/f045-r8.md .agent/last_block.md → exit 0

═══ ITEM 2 · C1 — .agent/live_review.md ═══
This is the reviewer's own text, written after the reviewer re-ran R7's
verification itself. Apply it EXACTLY as given — do not reword, do not
"improve", do not renumber. If any of it contradicts the disk, STOP and report
rather than correcting it yourself.

First, APPEND these two lines at the END of the `## Findings` section, after
R-0353's paragraph, one blank line between paragraphs:

Done: R-0351 — RESOLVED at the R7 gate. Verified against the disk, not the report: `run_loop` passes the mission text into `_materialize_loop_job` as `mission=mission.goal` and the helper sets it inside the `Job(...)` constructor, before `plan_job` and before the save, so the PERSISTED record carries it; `grep -n "job.mission = mission.goal" packages/orchestration/loop_run.py` returns nothing, so the post-hoc assignment that caused the finding is gone. The pin is independent of R-0352, which the round's own red-proof could not show because both defects sat on one code path: the reviewer rebuilt the pre-fix state in its own disposable worktree with R-0352's `root` threading KEPT and only R-0351's defect restored, and `test_mission_run_persists_the_mission_text_on_the_stored_job` still failed there with `assert None == 'review remedy for 2026-08-13'` — reaching its own assertion rather than dying earlier on a missing job — while the two isolation tests passed. The test reads the record through `storage.load_job` and never through `outcome.job`, so no fixture can decide its outcome.

Done: R-0352 — RESOLVED at the R7 gate. Verified against the disk, not the report: `_materialize_loop_job` takes `root` and its default save calls `storage.save_job(job, root)`; `loop_to_job` forwards `root`, and both `run_loop` branches pass it, so the job store, the mission record and the job-to-mission link all land under one root. An explicit `save` still overrides `root` and is still called with the job alone — the `Callable[[Job], None]` annotation is unchanged, and DECISION F045 D6 records why that annotation is load-bearing. The reviewer re-ran the red-proof independently in its own disposable worktree at `3cbcbd4c`: the import probe printed the module under `.remedy-wt/f045_r7_rev`, so the probe cannot have imported the fixed code (R-0337), and the three new tests failed there, two of them on `assert None is not None` from `last_run_for_loop`. The operator's real job store was checked afterwards and holds zero jobs carrying a `loop_ref`, so no probe escaped its scratch root.

Then APPEND this finding after those two lines, one blank line between
paragraphs:

- R-0354 — Low — a block's own list contradicted its Goal line, for the third time in this family. The R7 block's ITEM 5 ordered `.agent/plan.md` to say "(R-0350, R-0351, R-0352, R-0353 — the last two are fixed but NOT yet marked resolved)", but "the last two" of that list is R-0352 and R-0353, while the pair the same block's Goal line, its ITEM 2 and its ITEM 3 all name as fixed is R-0351 and R-0352. R-0353 is a citation-hygiene finding about a block, not a code defect, and nothing in the round touched it. The worker wrote the accurate pair into the durable plan and declared the deviation rather than copying a false statement into it, which was the correct move: `.agent/plan.md` is read at every session bootstrap, so a wrong finding pair there outlives the session that wrote it. Nothing landed wrong. This is the R-0331/R-0334 family exactly — a clause the block never read against its own other clauses before emission. Counter-measure, applied from R8 on: a block clause that refers to items by POSITION ("the last two", "the first three") names them explicitly instead, because a positional reference silently drifts when the list around it changes. OPEN.

Commit subject: `docs(f045): close R-0351 and R-0352, register R-0354`

═══ ITEM 3 · C2 — the loop command module and its wiring ═══
One commit, because a module that no dispatch table reaches is not a feature —
a green import gate on an unreachable command is exactly the blind spot this
bundling avoids. Write the code yourself; what is fixed below is the SEMANTICS.

(1) NEW `apps/cli/commands/loop_cmd.py`, following the shape of
    `apps/cli/commands/queue_cmd.py`: module docstring, private `_cmd_*`
    functions, a module-level `COMMAND_HANDLERS` dict at the end mapping
    command_id to a lambda taking the argparse namespace.

    `_cmd_loop_list()` — read-only. Loads every loop through
    `load_loop_specs()` with NO argument, so it reads the project's config
    file exactly where the spec module already looks. `LoopSpecError` is
    caught, printed as `Error: {exc}` on stderr, and exits `EXIT_ERROR`; it
    must never surface a traceback. With no loops, it says so in one honest
    line and exits 0. Otherwise one row per loop carrying, at minimum: the
    loop NAME, the TRIGGER kind, the ACTION kind, and the LAST RUN. A trigger
    for which `LoopSpec.is_inert` is true is marked in that row as inert, so a
    reader can see it cannot fire without running it first. The last run comes
    from `last_run_for_loop(spec.name)`; when it returns `None` the row says
    `never`, and when it returns a job the row shows that job's `created_at`
    and `state`. Do NOT invent a second source for the last run — the job
    store is the one the feature specifies.

    `_cmd_loop_validate()` — read-only. Calls `validate_loop_specs()` with NO
    argument. An empty result prints how many loops validated and exits 0. A
    non-empty result prints EVERY message, one per line, on stderr, and exits
    `EXIT_ERROR`; the feature requires a nonzero exit on any error, and it
    requires every error, not the first — that is why this uses
    `validate_loop_specs` and not `load_loop_specs`.

(2) `apps/cli/command_catalog.py`: add a `loop` group to `GROUPS` and two
    `CommandEntry` rows to `CATALOG`, `loop.list` and `loop.validate`, both
    `action_class="read_only"`. Put the group with the user-facing entries and
    the entries in their own commented section, matching the `# ── queue (F048)`
    convention already in the file. Give each entry a `related` tuple naming
    the other. Neither command takes any argument this round: do NOT add a
    `--config` option. The feature specifies the surface as `loop list`,
    `validate` and `run <name> [--yes]` and nothing more, and the tests reach
    the config file by changing directory instead, so an extra option would be
    CLI surface no one asked for.

(3) `apps/cli/commands/__init__.py`: register the new module in BOTH places
    `collect_all_handlers` needs — the `from apps.cli.commands import (...)`
    list AND the `for mod in (...)` tuple. Registering in only one of them
    leaves the command unreachable while every import still succeeds.

Commit subject: `feat(f045): add the loop list and loop validate commands`

═══ ITEM 4 · C3 — NEW tests/cli/test_loop_cmd.py ═══
This is the file `docs/roadmap/features/T2_F045.md` names under "Suggested
tests". Every test drives the command through `collect_all_handlers()` and an
`argparse.Namespace`, NOT by importing `_cmd_loop_list` directly — going
through the registered table is what proves the command is reachable, and the
precedent is `tests/cli/test_stats_cost.py`, which does exactly that. Read one
such test before writing yours.

Isolation, in every test: `monkeypatch.chdir(tmp_path)` so `remedy.toml` under
`tmp_path` is the config the command finds, and
`monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))` so the job store the
command reads is under `tmp_path` too. Both are required; the first alone
leaves the last-run lookup pointed at the operator's real store.

Write these six tests:
(1) a manual job loop with no runs lists its name, its trigger kind, its
    action kind and `never`.
(2) a schedule-trigger loop is listed and marked inert.
(3) after one real firing, the row shows that run instead of `never`.
    Materialize it with `run_loop(spec, project_id=..., date=..., root=tmp_path)`
    and NO `save`, which is the path R7 fixed, then assert the listed row
    carries something from the stored job.
(4) `loop validate` on a config with MORE THAN ONE error reports every one of
    them and exits nonzero. Assert on `pytest.raises(SystemExit)` and its
    code, and assert each message names its loop.
(5) `loop validate` on a valid config exits 0 without raising.
(6) `loop.list` and `loop.validate` are both present in
    `collect_all_handlers()` and both appear as `command_id`s in `CATALOG`.

R-0344 counter-measure, binding here: no assertion may match a string that
carries a filesystem path. `tmp_path` may be used for chdir, for the env var
and as a `root` argument, but must never appear inside an expected value —
pytest puts the test function's own name in that path, which would let the
fixture directory decide the outcome.

Commit subject: `test(f045): pin the loop list and validate commands`

═══ ITEM 5 · C4 — .agent/plan.md and .agent/handoff.md ═══
Rewrite `.agent/plan.md` (under 50 lines, keeping `## Goal`, `## Current Step`,
`## Next Steps`, `## Risks`). Current Step becomes R8 — the read-only CLI half
landed and R-0351 and R-0352 are closed in the review record. State the open
findings as exactly two, R-0350 and R-0354, and name them both explicitly
rather than by position (this is R-0354's own counter-measure, applied
immediately). Next free finding ID becomes R-0355. Next Steps become: R9 is
`remedy loop run <name> [--yes]` plus the end-to-end fixture loop through the
fake-provider pipeline; then the integration gate; then closure per
docs/roadmap/STATUS_closure_protocol.md. Keep both existing risks. Keep the
Fortschritt line `Fortschritt: ~60 % (T001 ✅ · T002 ✅ · T003 läuft) — Schätzung`
verbatim.

Then rewrite `.agent/handoff.md` per the AGENTS.md handoff contract (≤60 lines,
or a "Deviations, declared" line naming the real count and the mandated content
that caused it; sections are NEVER dropped). It carries: feature + round and
branch; every commit SHA of this round with its changed files; the ITEM 6 gate
table with REAL exit codes and REAL output, every test result given as a COLOUR
first; the open-findings count with R-0350 and R-0354 named; an item-status
table with one row per ITEM 1-6; the statement that no PR is open, nothing was
merged, main was never touched, no force-push occurred and no worktree was left
behind; the next expected action, which names Phase 1 rule 1 (read `.agent/STOP`
from disk) BEFORE rule 2 (the Open PR Gate), then R9; and the Fortschritt line.
Commit subject: `docs(f045): hand back R8 with the read-only loop CLI`

═══ ITEM 6 · gates ═══
Run every command. Record the REAL exit code and REAL output. Report every
count as OBSERVED — do not predict one and do not restate a number this block
gave you. For any test command report the COLOUR (passed / failed) first; the
count is a note, never the assertion.

(a) cmp .agent/authored/f045-r8.md .agent/last_block.md
(b) grep -c "^Done: R-" .agent/live_review.md
(c) grep -c "^- R-0354 — Low" .agent/live_review.md
(d) python3 -m pytest tests/cli/test_loop_cmd.py -q
(e) python3 -m pytest tests/cli/test_command_catalog.py tests/orchestration/test_loop_run.py tests/orchestration/test_loop_spec.py -q
(f) python3 -m pytest tests/cli/test_golden_path.py -q             (canary)
(g) python3 -m ruff check apps/cli/commands/loop_cmd.py apps/cli/command_catalog.py apps/cli/commands/__init__.py tests/cli/test_loop_cmd.py
(h) reachability, through the REAL table and not an import:
    python3 -c "from apps.cli.commands import collect_all_handlers as c; t=c(); print('loop.list', 'loop.list' in t); print('loop.validate', 'loop.validate' in t)"
    → both must print True. A False here means ITEM 3 (3) was done in only one
      of the two places.
(i) RED-PROOF, and it runs ONLY in a disposable worktree (guardrail G5).
    After C2 and C3 are committed:
      git worktree add .remedy-wt/f045_r8 636f3f07
      cp tests/cli/test_loop_cmd.py .remedy-wt/f045_r8/tests/cli/test_loop_cmd.py
      cd .remedy-wt/f045_r8
      python3 -c "import apps.cli.commands as m; print(m.__file__)"
        → MUST print a path UNDER .remedy-wt/f045_r8. If it prints the primary
          checkout's path, the probe would be importing the WIRED table and
          would prove nothing (finding R-0337): STOP and report.
      then run the new test file there, in-process so the environment is set
      without a shell assignment:
      python3 -c "import os,sys; os.environ['REMEDY_DATA_DIR']=os.getcwd()+'/.scratch_data'; sys.path.insert(0,os.getcwd()); import pytest; print('RC', pytest.main(['tests/cli/test_loop_cmd.py','-q','--no-header','-p','no:cacheprovider']))"
        → the tests must FAIL against the unwired tree. Report the COLOUR.
      then leave the worktree and: git worktree remove .remedy-wt/f045_r8 --force
    If they PASS there, the tests do not pin what they claim to: STOP and
    report, do not silently strengthen them.
(j) git diff --name-only 636f3f07..HEAD
    → exactly the nine files in Change and nothing else.
(k) git status --porcelain                        → EMPTY
(l) git worktree list                             → ONE line, after the removal
(m) real-store safety, run AFTER the test gates:
    python3 -c "
    import json
    from packages.orchestration.data_paths import jobs_dir
    d = jobs_dir(); n = 0
    if d.exists():
        for f in d.glob('*.json'):
            try: j = json.loads(f.read_text())
            except Exception: continue
            if 'loop_ref' in (j.get('metadata') or {}): n += 1
    print('REAL_STORE_LOOP_REF_JOBS', n)"
    → must print 0. Anything else means a test escaped its scratch root:
      report it as a blocker, do not delete the jobs.

Push after EVERY commit: `git push origin feature/f045-loop-definitions`.
Do NOT open a PR and do NOT merge anything.

If any gate is RED, or anything here contradicts AGENTS.md or the disk: STOP,
commit nothing further, and report the exact blocker with its raw output.
END BLOCK f045-r8
