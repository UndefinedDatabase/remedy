BEGIN BLOCK f045-r9
── STEP T003d/5 — F045 Loop definitions · ROUND 9 (repair) ───────────────

Goal:        Repair the R8 defect: `remedy loop list` prints the RUN notice as
             a legend, telling the operator a loop "ran on demand" on the same
             screen where that loop's row says `last run: never`. Register the
             finding FIRST, in its own commit, then fix the listing and the
             test that pinned the wrong text.
Bundle:      ITEM 1 C0a+C0b save block · ITEM 2 C1 register R-0355 · ITEM 3 C2
             the listing legend · ITEM 4 C3 the test · ITEM 5 C4 plan +
             handoff · ITEM 6 gates.
Change:      .agent/authored/f045-r9.md · .agent/last_block.md ·
             .agent/live_review.md · apps/cli/commands/loop_cmd.py ·
             tests/cli/test_loop_cmd.py · .agent/plan.md · .agent/handoff.md.
             Seven files, nothing else. Do NOT touch
             `packages/orchestration/loop_spec.py`: `INERT_TRIGGER_NOTICE` is
             CORRECT where it is and is still what `remedy loop run` will
             display in R10 — the defect is the LISTING borrowing it, not the
             constant. Do NOT write `remedy loop run` this round. Do NOT
             touch `apps/cli/command_catalog.py` or
             `apps/cli/commands/__init__.py`: the wiring was verified correct.
Constraints: Never work on main; never force-push; no PR; merge nothing. The
             red-proof runs ONLY in a disposable worktree under `.remedy-wt/`
             (gitignored at .gitignore:235). The commit order is fixed: the
             finding is registered BEFORE the repair lands, so the record
             shows the defect existing rather than only its fix
             (docs/agents/self_drive_protocol.md Phase 2 step 4).
Insertion budget, per commit: C0a and C0b ≈ block size (single `.agent/**`
             state-file rewrites, cap-exempt by DECISION F104 D1) · C1 ≤ 4 ·
             C2 ≤ 30 · C3 ≤ 20 · C4 ≤ 130.
Done when:   every gate in ITEM 6 has been RUN and its real output recorded.
Handback:    completion report + rewrite .agent/handoff.md

Facts, measured by the reviewer at emission — check each before relying on it:
  `INERT_TRIGGER_NOTICE = "scheduler not yet available; ran on demand"` is at
  `packages/orchestration/loop_spec.py:68`.
  `packages/orchestration/loop_run.py`'s module docstring says `run_loop`
  "says so through ``loop_spec.INERT_TRIGGER_NOTICE`` rather than pretending
  the trigger fired", and the notice travels on `LoopRunOutcome.notice`.
  `docs/roadmap/features/T2_F045.md` Acceptance binds that sentence to
  RUNNING: "Schedule-trigger loops run manually with the honest 'scheduler not
  yet available; ran on demand' line."
  The reviewer ran the wired `loop.list` handler on a config holding one
  schedule loop and one manual loop and observed exactly this output:
      weekly-sweep              schedule (inert)      job       last run: never
      nightly-tidy              manual                job       last run: never
        (inert: scheduler not yet available; ran on demand)

═══ ITEM 1 · C0a and C0b — save this block verbatim ═══
C0a: write the block bytes (BEGIN..END markers included) to
`.agent/authored/f045-r9.md`. No trailing whitespace on any line.
Commit subject: `chore(f045): save the R9 block verbatim`
C0b: copy that file over `.agent/last_block.md`, replacing the R8 block.
Commit subject: `chore(f045): point last_block at the R9 block`
Prove it: cmp .agent/authored/f045-r9.md .agent/last_block.md → exit 0

═══ ITEM 2 · C1 — register R-0355, BEFORE any repair ═══
File `.agent/live_review.md`. APPEND at the END of the `## Findings` section,
after R-0354's paragraph, one blank line between paragraphs. This is the
reviewer's text; apply it EXACTLY, do not reword and do not renumber. If it
contradicts the disk, STOP and report rather than correcting it yourself.

- R-0355 — Medium — a listing borrowed the RUN notice and so asserted a run that never happened. `remedy loop list` prints `INERT_TRIGGER_NOTICE` as a legend under the table whenever any listed loop is inert. That constant is `scheduler not yet available; ran on demand` (`packages/orchestration/loop_spec.py`), whose second clause is a claim about a RUN. The reviewer ran the wired handler on a config with one schedule loop and one manual loop and read the output: a row `weekly-sweep  schedule (inert)  job  last run: never`, followed one line later by `(inert: scheduler not yet available; ran on demand)` — a loop reported as never having run, told on the next line that it ran on demand. The feature file binds that sentence to RUNNING, not to listing ("Schedule-trigger loops run manually with the honest 'scheduler not yet available; ran on demand' line", `docs/roadmap/features/T2_F045.md`, Acceptance), and `packages/orchestration/loop_run.py`'s module docstring states that `run_loop` "says so through `loop_spec.INERT_TRIGGER_NOTICE` rather than pretending the trigger fired" — the notice rides on `LoopRunOutcome.notice`, which a listing never produces. This is the one thing the feature's design exists to prevent, inverted: the honest-notice string used to make a dishonest statement. The R8 block ordered only that an inert trigger be "marked in that row as inert" and never ordered the notice; the worker added the legend and then pinned it with `assert INERT_TRIGGER_NOTICE in out` in `tests/cli/test_loop_cmd.py`, so a test protected the wrong text — the R-0344 shape at the display layer, where the assertion agreed with the code instead of with the requirement. Fix by giving the listing its own legend saying only what a listing can know: the trigger cannot fire until the scheduler exists, so the loop must be run manually. `INERT_TRIGGER_NOTICE` stays untouched and stays `remedy loop run`'s to display. OPEN.

Commit subject: `docs(f045): register R-0355, the listing that borrowed the run notice`

═══ ITEM 3 · C2 — apps/cli/commands/loop_cmd.py ═══
Replace the legend line that prints `INERT_TRIGGER_NOTICE` with the listing's
OWN text, defined as a module-level constant next to `INERT_MARK` so a reader
finds it where the other display strings live. Write the words yourself. The
constraints on it:
- it states that such a trigger cannot fire until the scheduler exists, and
  that the loop therefore has to be run manually;
- it makes NO claim about whether anything ran — no past tense about a run;
- it does not contain the string `ran on demand`.
Remove the now-unused `INERT_TRIGGER_NOTICE` import from this module. Keep the
per-row `(inert)` mark exactly as it is: that part was correct.

Above the new constant put the one-line WHY comment this repository's
discoverability convention asks for, recording the deliberate absence a reader
would otherwise search for — that the listing deliberately does NOT reuse
`loop_spec.INERT_TRIGGER_NOTICE`, because that sentence reports a RUN and a
listing has not run anything. A reader who greps `INERT_TRIGGER_NOTICE` and
finds it missing here must land on the reason.

Commit subject: `fix(f045): give the loop listing its own inert legend`

═══ ITEM 4 · C3 — tests/cli/test_loop_cmd.py ═══
In `test_a_schedule_trigger_loop_is_listed_and_marked_inert`, replace
`assert INERT_TRIGGER_NOTICE in out` with BOTH of these:
- a positive assertion that the listing's own legend constant appears in the
  output — import it from `apps.cli.commands.loop_cmd`, so the test reads the
  expected value out of the module under test rather than restating it;
- a NEGATIVE assertion that `INERT_TRIGGER_NOTICE` does NOT appear anywhere in
  the listing output. This one is the actual pin: it is what goes red if
  anybody reintroduces the run notice into a listing, and without it the
  repair is only a rename.
Keep `INERT_TRIGGER_NOTICE` imported for that negative assertion. Change
nothing else in this file — the other five tests were verified correct.

Commit subject: `test(f045): pin that a listing never prints the run notice`

═══ ITEM 5 · C4 — .agent/plan.md and .agent/handoff.md ═══
Rewrite `.agent/plan.md` (under 50 lines, keeping `## Goal`, `## Current Step`,
`## Next Steps`, `## Risks`). Current Step becomes R9 — R8 was FAILED by the
reviewer on one defect, R-0355 is registered and repaired, and the read-only
CLI half now says only what a listing can know. Open findings are exactly
three: R-0350, R-0354 and R-0355 — name all three explicitly, never by
position (R-0354's counter-measure). Next free finding ID becomes R-0356. Next
Steps become: R10 is `remedy loop run <name> [--yes]`, which is where
`INERT_TRIGGER_NOTICE` is displayed for real off `LoopRunOutcome.notice`, plus
the end-to-end fixture loop through the fake-provider pipeline; then the
integration gate; then closure per docs/roadmap/STATUS_closure_protocol.md.
Keep both existing risks and add a third: the CLI's read-only half is landed
but `loop run` is not, so no operator-visible path yet exercises the
loop_ref provenance end to end. Keep the Fortschritt line
`Fortschritt: ~60 % (T001 ✅ · T002 ✅ · T003 läuft) — Schätzung` verbatim.

Then rewrite `.agent/handoff.md` per the AGENTS.md handoff contract (≤60 lines,
or a "Deviations, declared" line naming the real count and the mandated content
that caused it; sections are NEVER dropped). It carries: feature + round and
branch, and the fact that this was a REPAIR round after a FAIL verdict on R8;
every commit SHA of this round with its changed files; the ITEM 6 gate table
with REAL exit codes and REAL output, every test result as a COLOUR first; the
open-findings count with R-0350, R-0354 and R-0355 named; an item-status table
with one row per ITEM 1-6; the statement that no PR is open, nothing was
merged, main was never touched, no force-push occurred and no worktree was left
behind; the next expected action, naming Phase 1 rule 1 (read `.agent/STOP`
from disk) BEFORE rule 2 (the Open PR Gate), then R10; and the Fortschritt line.
Commit subject: `docs(f045): hand back the R9 repair of the loop listing`

═══ ITEM 6 · gates ═══
Run every command. Record the REAL exit code and REAL output. Report every
count as OBSERVED. For any test command report the COLOUR first; the count is
a note, never the assertion.

(a) cmp .agent/authored/f045-r9.md .agent/last_block.md
(b) grep -c "^- R-0355 — Medium" .agent/live_review.md
(c) grep -n "INERT_TRIGGER_NOTICE" apps/cli/commands/loop_cmd.py
    → must return NOTHING except, if you wrote it that way, the WHY comment
      naming the deliberate absence. It must NOT appear in any print or import.
(d) the real output, which is what the finding was written from. Run the wired
    handler on a two-loop config and PASTE the actual lines:
    python3 -c "
    import os, sys, pathlib, shutil, argparse
    s = pathlib.Path('.remedy-wt/r9_probe')
    shutil.rmtree(s, ignore_errors=True); s.mkdir(parents=True)
    (s/'remedy.toml').write_text('''
    [[loop]]
    name = \"weekly-sweep\"
    [loop.trigger]
    kind = \"schedule\"
    schedule = \"0 3 * * 1\"
    [loop.action]
    kind = \"job\"
    goal_template = \"sweep {project}\"

    [[loop]]
    name = \"nightly-tidy\"
    [loop.action]
    kind = \"job\"
    goal_template = \"tidy {project} on {date}\"
    ''')
    repo = os.getcwd(); os.environ['REMEDY_DATA_DIR'] = str((s/'data').resolve())
    os.chdir(s); sys.path.insert(0, repo)
    from apps.cli.commands import collect_all_handlers
    collect_all_handlers()['loop.list'](argparse.Namespace())"
    Mind the TOML indentation when you write this — dedent the heredoc content
    so the file is valid TOML. Delete `.remedy-wt/r9_probe` afterwards.
    → the pasted output must contain no past-tense claim about a run.
(e) python3 -m pytest tests/cli/test_loop_cmd.py -q
(f) python3 -m pytest tests/cli/test_command_catalog.py tests/orchestration/test_loop_run.py tests/orchestration/test_loop_spec.py -q
(g) python3 -m pytest tests/cli/test_golden_path.py -q            (canary)
(h) python3 -m ruff check apps/cli/commands/loop_cmd.py tests/cli/test_loop_cmd.py
(i) RED-PROOF, ONLY in a disposable worktree (guardrail G5). After C2 and C3
    are committed:
      git worktree add .remedy-wt/f045_r9 0d9c67f7
      python3 -c "import shutil; shutil.copyfile('tests/cli/test_loop_cmd.py', '.remedy-wt/f045_r9/tests/cli/test_loop_cmd.py')"
      cd .remedy-wt/f045_r9
      python3 -c "import apps.cli.commands.loop_cmd as m; print(m.__file__)"
        → MUST print a path UNDER .remedy-wt/f045_r9, else the probe would be
          importing the REPAIRED module and would prove nothing (R-0337): STOP.
      python3 -c "import os,sys; os.environ['REMEDY_DATA_DIR']=os.getcwd()+'/.scratch_data'; sys.path.insert(0,os.getcwd()); import pytest; print('RC', pytest.main(['tests/cli/test_loop_cmd.py','-k','inert','-q','--no-header','-p','no:cacheprovider']))"
        → the inert test must FAIL there, because the pre-repair module prints
          the run notice and has no legend constant. Report the COLOUR.
      leave the worktree, then: git worktree remove .remedy-wt/f045_r9 --force
(j) git diff --name-only 0d9c67f7..HEAD  → exactly the seven Change files
(k) git status --porcelain               → EMPTY
(l) git worktree list                    → ONE line, after the removal
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
    → must print 0.

Push after EVERY commit: `git push origin feature/f045-loop-definitions`.
Do NOT open a PR and do NOT merge anything.

If any gate is RED, or anything here contradicts AGENTS.md or the disk: STOP,
commit nothing further, and report the exact blocker with its raw output.
END BLOCK f045-r9
