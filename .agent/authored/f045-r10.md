BEGIN BLOCK f045-r10
── STEP T003e/6 — F045 Loop definitions · ROUND 10 ───────────────────────

Goal:        Land `remedy loop run <name>`, the write half of the T003 CLI and
             the first operator-visible path that exercises loop_ref
             provenance end to end. It MATERIALIZES and stops; it never
             executes. Register R-0356 first.
Bundle:      ITEM 1 C0a+C0b save block · ITEM 2 C1 register R-0356 · ITEM 3 C2
             DECISION F045 D7 · ITEM 4 C3 the command and its catalog entry ·
             ITEM 5 C4 tests · ITEM 6 C5 plan + handoff · ITEM 7 gates.
Change:      .agent/authored/f045-r10.md · .agent/last_block.md ·
             .agent/live_review.md · .agent/decisions.md ·
             apps/cli/commands/loop_cmd.py · apps/cli/command_catalog.py ·
             tests/cli/test_loop_cmd.py · .agent/plan.md · .agent/handoff.md.
             Nine files, nothing else. Do NOT touch
             `packages/orchestration/loop_run.py` or `loop_spec.py`: `run_loop`
             already does everything this command needs and is reviewed and
             passed. Do NOT touch `apps/cli/commands/__init__.py` — `loop_cmd`
             is already registered there and the new handler joins its existing
             `COMMAND_HANDLERS` dict.
Constraints: Never work on main; never force-push; no PR; merge nothing. Any
             red-proof runs ONLY in a disposable worktree under `.remedy-wt/`
             (gitignored at .gitignore:235). No test may read or write the
             operator's real job store; gate (m) checks it did not.
Insertion budget, per commit: C0a and C0b ≈ block size (single `.agent/**`
             state-file rewrites, cap-exempt by DECISION F104 D1) · C1 ≤ 4 ·
             C2 ≤ 45 · C3 ≤ 130 · C4 ≤ 190 · C5 ≤ 130. C4 is the largest
             because eight tests need eight configs and fixtures; it is still
             far under the AGENTS.md 500-insertion cap.
Done when:   every gate in ITEM 7 has been RUN and its real output recorded.
Handback:    completion report + rewrite .agent/handoff.md

TWO CHECKS BEFORE YOU WRITE CODE — report both findings in your handback:
  CHECK 1. `apps/cli/commands/queue_cmd.py` defines a private
  `_resolve_project_id(project_flag)` that calls
  `project_registry.select_project(project_flag, ".")` and exits with its
  `EXIT_NO_PROJECT = 3` on `ProjectNotFoundError`. Grep how many command
  modules under `apps/cli/commands/` define their own `_resolve_project_id`.
  If several already do, MIRROR that pattern in `loop_cmd.py` and do NOT
  extract a shared helper — extracting one would be a refactor riding along
  with a feature, which AGENTS.md forbids in the same commit, and the suite
  was stabilized recently. If `loop_cmd.py` would be the SECOND definition
  only, still mirror it and say so; the extraction is someone's later call,
  not this round's.
  CHECK 2. Find how existing CLI tests obtain a project so `select_project`
  resolves — read `tests/cli/test_mission_cmd.py` and one other CLI test that
  needs a project. REUSE that fixture pattern verbatim in spirit. Do NOT
  invent a new way to register a project, and do NOT reach into the registry's
  internals if the tests already have a supported route.

═══ ITEM 1 · C0a and C0b — save this block verbatim ═══
C0a: write the block bytes (BEGIN..END markers included) to
`.agent/authored/f045-r10.md`. No trailing whitespace on any line.
Commit subject: `chore(f045): save the R10 block verbatim`
C0b: copy that file over `.agent/last_block.md`, replacing the R9 block.
Commit subject: `chore(f045): point last_block at the R10 block`
Prove it: cmp .agent/authored/f045-r10.md .agent/last_block.md → exit 0

═══ ITEM 2 · C1 — register R-0356, before anything else ═══
File `.agent/live_review.md`. APPEND at the END of the `## Findings` section,
after R-0355's paragraph, one blank line between paragraphs. Reviewer's text;
apply it EXACTLY, do not reword, do not renumber.

- R-0356 — Low — the reviewer applied R-0354's counter-measure and still got the open-finding set wrong, twice. R-0354 ordered that a block name findings explicitly instead of by position. The R8 block did exactly that — "the open findings as exactly two, R-0350 and R-0354" — and the R9 block did it again with three, "R-0350, R-0354 and R-0355". The disk says four: re-deriving the set mechanically from `.agent/live_review.md`, every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line, yields R-0350, R-0353, R-0354 and R-0355. R-0353 has carried no `Done:` line since it was registered at R6 and its paragraph still ends `OPEN.`; it was dropped from the count at R8 and stayed dropped. Naming items explicitly removes the ambiguity R-0354 was about and does nothing about the COUNT, because both blocks carried the set forward from the previous block instead of re-deriving it from the record. The R9 worker re-derived it, wrote the accurate four into `.agent/plan.md` and declared the deviation rather than copying the block's number — the third round running in which a worker corrected the reviewer's own bookkeeping. Nothing landed wrong. Counter-measure, to be applied ON DISK rather than in reviewer habit, which is what finally closed R-0347: the pre-emission checklist in `docs/agents/planner_reviewer_prompt.md` §3 gains a step requiring the open-finding set to be RECOMPUTED from `.agent/live_review.md` at emission and never carried forward from the previous block. That edit is R11's, together with R-0353's own on-disk counter-measure. OPEN.

Commit subject: `docs(f045): register R-0356, the open-set miscount`

═══ ITEM 3 · C2 — .agent/decisions.md, DECISION F045 D7 ═══
Append after D6, same heading shape as the six F045 decisions already there:
`## DECISION F045 D7 (2026-08-14) — `remedy loop run --yes` confirms MATERIALIZATION, never execution`

Write the body yourself, covering exactly these points:
- WHAT: `remedy loop run <name>` materializes the loop through `run_loop` and
  stops. The job it produces is PLANNED. `--yes` skips the interactive
  confirmation and NOTHING else: it does not approve execution, does not
  change the job's state, and does not run a task.
- WHY this reading and not the other: `docs/roadmap/features/T2_F045.md` lists
  the surface as `run <name> [--yes]` without saying what `--yes` approves,
  while `packages/orchestration/loop_run.py`'s module docstring makes the
  approval semantics load-bearing — the job stops at PLANNED, nothing
  "executes a task, approves a plan, or implies ``--yes``", and
  `LoopSpec.unattended` is RECORDED and "changes NOTHING about the job's
  state". Quote the docstring sentence you rely on, having read it, rather
  than paraphrasing it (this is R-0348's counter-measure: a decision that
  states what another module requires quotes the sentence that establishes it).
  Of the two readings, "confirm the materialization" is the one the repository's
  own rules already select, and it is the smaller change.
- The consequence for the operator: after `loop run`, the job is theirs to
  start, and the command says so by naming the next command.
- HOW TO REVERSE: if `--yes` should ever mean "and run it", it must go through
  the same approval path a typed goal uses and must refuse for a loop whose
  spec is not `unattended`; changing this command alone would let a config
  file start execution, which is what the current semantics exist to prevent.
Commit subject: `docs(f045): record DECISION F045 D7 on what loop run --yes means`

═══ ITEM 4 · C3 — the command and its catalog entry ═══
(1) `apps/cli/commands/loop_cmd.py` gains `_cmd_loop_run` and a third entry in
    the existing `COMMAND_HANDLERS` dict, `"loop.run"`. Semantics:
    - Resolve the project exactly as CHECK 1 concluded.
    - Load the specs with `load_loop_specs()`; `LoopSpecError` prints
      `Error: {exc}` on stderr and exits `EXIT_ERROR`.
    - Select the spec whose `name` matches the argument. No match: print an
      error naming the requested loop AND the names that do exist, on stderr,
      and exit `EXIT_ERROR`. Nothing is created.
    - Confirmation. When `--yes` was NOT given: if stdin is not a TTY, do NOT
      prompt — print an error telling the operator to pass `--yes`, exit
      `EXIT_USAGE`, and create nothing. A command that blocks on `input()`
      under a pipe or over a non-interactive SSH session would hang a run
      forever, and this feature exists to be driven that way. If stdin IS a
      TTY, prompt with what will be created and let the operator decline;
      declining creates nothing and exits 0.
    - Materialize with `run_loop(spec, project_id=project_id)` — no `date`, no
      `root`, no `save`, so it uses today's date and the real store, which is
      exactly what an operator invocation should do.
    - Report: the job id, its state, the mission id when the outcome carries
      one, and — when `outcome.notice` is set — that notice. Print
      `outcome.notice` itself; do NOT import `INERT_TRIGGER_NOTICE` and print
      the constant. The outcome is what knows whether a run was inert, and
      finding R-0355 is exactly what happens when display code reaches for the
      constant instead of the value it was given.
    - Finally print the next command the operator needs, naming the job id, so
      the stop-at-PLANNED contract is visible instead of implied.
    - It never executes anything.
(2) `apps/cli/command_catalog.py`: one `CommandEntry`, `loop.run`, in the
    existing `# ── loop (F045)` section. `action_class="write_metadata"` — it
    persists a job and does NOT execute, so `may_execute_commands` stays
    False. Args: the loop name, a `--yes` FLAG (`is_flag=True`, it takes no
    value), and the shared `_PROJECT_SCOPE_OPT` already defined in that file.
    Add `loop.run` to the `related` tuples of the two existing loop entries
    and give it theirs.
Commit subject: `feat(f045): add the loop run command, materialize and stop`

═══ ITEM 5 · C4 — tests/cli/test_loop_cmd.py ═══
Append to the existing file, reusing its `project` fixture and its `_dispatch`
helper. `_dispatch` currently passes an empty `argparse.Namespace`; extend it,
or add a sibling, so a namespace with attributes can be dispatched — the
command reads its arguments off that namespace exactly as the real CLI builds
it. Isolation is unchanged and mandatory: chdir plus `REMEDY_DATA_DIR`, plus
whatever CHECK 2 established for the project registry.

Eight tests:
(1) `--yes` on a manual job loop materializes: the store holds a job whose
    `loop_ref` metadata is the loop's name, its state is PLANNED, and the
    printed output contains that job's id. Read the job back through the
    STORE, not out of the printed text alone.
(2) the same run prints the next command naming that job id.
(3) an unknown loop name exits non-zero, names the requested loop and the
    existing one, and leaves the store empty.
(4) no `--yes` with a non-TTY stdin exits non-zero and creates nothing.
(5) a TTY stdin answering yes materializes — monkeypatch the TTY check and
    `input`.
(6) a TTY stdin declining creates nothing and does NOT raise SystemExit.
(7) an inert (schedule-trigger) loop run with `--yes` prints the run notice —
    assert against `loop_spec.INERT_TRIGGER_NOTICE`, which HERE is correct
    because a run really did happen — and the job is still PLANNED, which is
    the "a loop never implies --yes" pin for this command.
(8) `loop.run` is in `collect_all_handlers()` and in `CATALOG`.
Assert states through the model's own enum value rather than a hard-coded
string. R-0344 still binds: no assertion may match a string carrying a
filesystem path.
Commit subject: `test(f045): pin loop run materializing and stopping`

═══ ITEM 6 · C5 — .agent/plan.md and .agent/handoff.md ═══
Rewrite `.agent/plan.md` (under 50 lines, keeping `## Goal`, `## Current Step`,
`## Next Steps`, `## Risks`). RECOMPUTE the open-finding set from
`.agent/live_review.md` — every `^- R-\d+ — ` paragraph minus every
`^Done: R-\d+ — ` line — and write what you actually measure, naming each one.
Do not copy a count from this block; this block deliberately gives you none,
because R-0356 is exactly the failure of carrying one forward. Current Step
becomes R10 — the T003 CLI is complete (`list`, `validate`, `run`) and a loop
now reaches a planned job through an operator-visible path. Next Steps: R11
applies the on-disk counter-measures for R-0353 and R-0356 to
`docs/agents/planner_reviewer_prompt.md` §3 and writes the session-closing
handoff; the end-to-end fixture loop through the fake-provider pipeline, the
integration gate and closure per docs/roadmap/STATUS_closure_protocol.md
remain AFTER this session. Say plainly that the feature is NOT closed. Keep
the Fortschritt line
`Fortschritt: ~60 % (T001 ✅ · T002 ✅ · T003 läuft) — Schätzung` verbatim.

Then rewrite `.agent/handoff.md` per the AGENTS.md handoff contract (≤60 lines,
or a "Deviations, declared" line naming the real count and the mandated content
that caused it; sections are NEVER dropped). It carries: feature + round and
branch; both CHECK results; every commit SHA with its changed files; the ITEM 7
gate table with REAL exit codes and REAL output, every test result as a COLOUR
first; the recomputed open-finding count with each finding named; an
item-status table with one row per ITEM 1-7; the statement that no PR is open,
nothing was merged, main was never touched, no force-push occurred and no
worktree was left behind; the next expected action, naming Phase 1 rule 1 (read
`.agent/STOP` from disk) BEFORE rule 2 (the Open PR Gate), then R11; and the
Fortschritt line.
Commit subject: `docs(f045): hand back R10 with the loop run command`

═══ ITEM 7 · gates ═══
Run every command. Record REAL exit codes and REAL output. Report every count
as OBSERVED. For any test command report the COLOUR first.

(a) cmp .agent/authored/f045-r10.md .agent/last_block.md
(b) grep -c "^- R-0356 — Low" .agent/live_review.md
(c) the recomputed open set, which is a MEASUREMENT, not a restatement:
    python3 -c "
    import re, pathlib
    t = pathlib.Path('.agent/live_review.md').read_text()
    o = re.findall(r'^- (R-\d+) — ', t, re.M); d = re.findall(r'^Done: (R-\d+) — ', t, re.M)
    print('OPEN', [x for x in o if x not in d])"
(d) grep -n "INERT_TRIGGER_NOTICE" apps/cli/commands/loop_cmd.py
    → must still show only the WHY comment from R9. The run path prints
      `outcome.notice`, so this module still must not import the constant.
(e) python3 -m pytest tests/cli/test_loop_cmd.py -q
(f) python3 -m pytest tests/cli/test_command_catalog.py tests/orchestration/test_loop_run.py tests/orchestration/test_loop_spec.py -q
(g) python3 -m pytest tests/cli/test_golden_path.py -q            (canary)
(h) python3 -m ruff check apps/cli/commands/loop_cmd.py apps/cli/command_catalog.py tests/cli/test_loop_cmd.py
(i) reachability through the REAL table:
    python3 -c "from apps.cli.commands import collect_all_handlers as c; t=c(); print({k: k in t for k in ('loop.list','loop.validate','loop.run')})"
    → all three True.
(j) RED-PROOF, ONLY in a disposable worktree (G5). After C3 and C4 are
    committed:
      git worktree add .remedy-wt/f045_r10 3be5ab8b
      python3 -c "import shutil; shutil.copyfile('tests/cli/test_loop_cmd.py', '.remedy-wt/f045_r10/tests/cli/test_loop_cmd.py')"
      cd .remedy-wt/f045_r10
      python3 -c "import apps.cli.commands.loop_cmd as m; print(m.__file__)"
        → MUST print a path UNDER .remedy-wt/f045_r10, else the probe imports
          the finished module and proves nothing (R-0337): STOP.
      python3 -c "import os,sys; os.environ['REMEDY_DATA_DIR']=os.getcwd()+'/.scratch_data'; sys.path.insert(0,os.getcwd()); import pytest; print('RC', pytest.main(['tests/cli/test_loop_cmd.py','-k','run','-q','--no-header','-p','no:cacheprovider']))"
        → the new run tests must FAIL there. Report the COLOUR. If any of them
          PASSES against a tree with no `loop run`, that test does not pin what
          it claims: STOP and report.
      leave the worktree, then: git worktree remove .remedy-wt/f045_r10 --force
(k) git diff --name-only 3be5ab8b..HEAD  → exactly the nine Change files
(l) git status --porcelain               → EMPTY
(m) real-store safety, AFTER the test gates:
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
    → must print 0. A non-zero here means a test ran the command against the
      operator's real store: report it as a blocker, do not delete the jobs.
(n) git worktree list                    → ONE line, after the removal

Push after EVERY commit: `git push origin feature/f045-loop-definitions`.
Do NOT open a PR and do NOT merge anything.

If any gate is RED, or anything here contradicts AGENTS.md or the disk: STOP,
commit nothing further, and report the exact blocker with its raw output.
END BLOCK f045-r10
