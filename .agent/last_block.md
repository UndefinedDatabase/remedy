# F281 Round 7 — step block

## Goal

Book round 6's PASS, and clear the full "Run" bucket (30 of 30) — the last of
the small/medium buckets before Project (65) and Job (~120), the two large
remaining buckets. Zero introduced beyond a documented, truthful side effect:
two of the thirty edits (`test.list`, `test.status`) add "job's tasks" to
satisfy the Run word's own `task`/`evidence` fragment, and that same text
happens to also satisfy the separate `Job`-word fragment (`task`) on those
same two surfaces — a bonus fix, not a new violation. Net: 32 fixed, 0
introduced, pre-verified in a disposable worktree against the real
`tests/docs/test_vocabulary.py` functions before authoring.

## Bundle

C0a: save this block verbatim to `.agent/authored/f281-r7.md`.
C0b: mirror this block verbatim to `.agent/last_block.md`.
C1: RECORD6 + PLAN7 — one commit.
C2: CODE — 30 catalog text edits in `apps/cli/command_catalog.py`, all
clearing a `Run`-word meaning violation (the description contains "run" but
no `task`/`evidence` fragment). Each edit uses one of two honest strategies:
(a) the "run" usage genuinely names the Run entity (a job/mission's
execution) — add a true `task` or `evidence` mention already implied by the
command's real behaviour; or (b) the "run" usage is an ordinary English verb
unrelated to the Run entity (e.g. "run pytest", "run CI stages") — reword to
a synonym ("execute") that removes the word entirely. Every edit was applied
and measured in a scratch worktree first; none is guessed.
C3: HANDBACK.

## C1 — RECORD6 + PLAN7

### RECORD6 — append to `.agent/live_review.md`, after its current last line,
separated by exactly one blank line, verbatim:

```
Gate: F281 R6 — the F281 round 6 entry. VERDICT PASS. Written by the planner and reviewer of F281's first session after reading the committed range `78d32152`..`cc1cd3b0` (commits `94259710`, `0945520f`, `8ba2c5ed`, `60c81988`, `cc1cd3b0`) and independently re-deriving every reading below; the worker's report was evidence for none of them except where named. THE TRANSPORT: `.agent/authored/f281-r6.md` and `.agent/last_block.md` are byte-identical to the reviewer's own authored block, sha256 `060104df78a179c32b9c9b2a0b5e7e6ce7f5b900fb248ffed09a7dcedeffa11c`, 12066 bytes, reproduced directly. THE CODE, reproduced by `git show 60c81988`: all 9 FROM/TO edits landed exactly as ordered (8 identical `mission_id` ArgDefs replaced by one global find-and-replace, plus `mission.handoff`'s distinct `mission_id` ArgDef, `mission.run`'s `run_id` ArgDef, `mission.start`'s `goal` ArgDef, and 5 command descriptions). THE MEASUREMENT, reproduced directly at HEAD against the real, committed catalog: `_meaning_violations()` reads 216, `_synonym_offenders()` reads 2 — both exactly matching the block's own prediction (232→216, 16 fixed, 0 introduced). THE GATES, reproduced directly: `python3 -m pytest tests/docs/test_vocabulary.py tests/test_command_catalog.py tests/cli/test_advertised_commands.py -q` reads `74 passed`; `python3 -m pytest tests/cli/test_golden_path.py -q` reads `42 passed`; `python3 -m ruff check apps/cli/command_catalog.py` reads `All checks passed!`. THE TREE: `git status --porcelain` empty, `git worktree list` one row, HEAD `cc1cd3b0` matches `origin/feature/f281-cli-help-surface`. WHY PASS: every byte independently reproduces and the vocabulary-function measurement matches exactly.
```

### PLAN7 — replace the entire content of `.agent/plan.md` with exactly:

```
# Plan — F281 CLI help surface

Branch: feature/f281-cli-help-surface, cut from `main` at
`c617dd74df26b8e677161b265a88d5926f4d78ab`, the merge commit of pull request 253
(F280's closure).

## Goal

Every catalog description, role label and help page reads as the finished
vocabulary of DECISION amend0905-vocab D4 once F280 has pruned and renamed the
command tree (`docs/roadmap/features/T2_F281.md`). DONE when T001 and the
Acceptance list hold.

## Current Step

ROUND 7. C1 books round 6's PASS and re-points `.agent/plan.md`. C2 clears the
full "Run" bucket (30 of 30): the group descriptions for `ci`, `teacher` and
`test`; the command descriptions and ArgDef help text of `ci.run`,
`integrity.check`, `teacher.ask`, `teacher.narrate`, `test.status`,
`test.result`, `test.list`, `test.run` (`--apply-id`, `--intent-id`),
`mission.run` (description, `--iterations`, `--no-llm`), `mission.readiness`,
`run.show` (description and `run_id`), `job.resume` (`--cycles`), `job.run`
(`--test-command`), `job.apply` (description and `--approve`), `job.evidence`
(`--verification-command`), `do.run` (`--ui`), and `stats.bench` (description
and `--series`). Two of the thirty edits (`test.list`, `test.status`) also
land a bonus, truthful fix on the separate `Job`-word bucket, as a documented
side effect — not a new violation.

After this round: Order remains 1 (`stats.bench`, still the word-sense
collision round 4 named — untouched by this round), Mission, Task, Evidence,
Decision and Run all read 0. Only Project (65) and Job (118, down from 120)
remain — the two largest buckets.

## Next Steps

1. Re-run `_meaning_violations()` grouped by word at the start of round 8;
   expected: Project and Job are the only two buckets left, at approximately
   183-184 total (re-measure rather than trust). Job (~118) is by far the
   largest; Project (~65) is next. Given their size, a future round should
   look for shared constants (as the many `job_id`/`--project` ArgDefs)
   before writing many per-command edits — grep for the most-repeated exact
   help strings among the violations first.
2. This session (session 1 of F281) has now run 7 delegated rounds, inside
   the operator's 6-to-8 target (amend0905-throughput: 6-8 default, 4 the
   floor). The session's own honest assessment governs whether it continues
   or ends with a handoff; either is a legitimate outcome per the protocol.
3. Help wrap, `doctor core` dead-commands (D11d), the D11a catalog
   group-reach test, the visible-order data-pinned test, the F259 enforced
   flip (bounded by DECISION F281 D2's two-item floor, possibly `stats.bench`
   as a third), and the README quickstart's R-0895 line remain entirely
   undone — none of T001's non-description work has started yet.

## Risks

- Same as rounds 2-6: every catalog description edit is verified by
  re-running the real `_meaning_violations()`/`_synonym_offenders()`
  functions against the modified catalog before authoring, diffed fixed vs.
  introduced.
- The Job bucket (~118) likely contains many shared constants and many
  genuinely distinct descriptions; it will need several rounds and careful
  checking for the "fragment is itself a binding word" and "same word,
  different sense" traps this feature has already found twice.
```

## C2 — CODE (30 catalog text edits, all in `apps/cli/command_catalog.py`)

Apply each FROM → TO pair below EXACTLY, in order. Every FROM string must
appear verbatim exactly once at the cited location; if it does not match,
STOP and report the exact mismatch rather than guessing or forcing a match.

1. `ci` group description (near line 137). FROM:
```
    "ci": GroupDef("ci", "CI", "Remedy's own CI stages, run locally.", user_facing=False),
```
TO:
```
    "ci": GroupDef("ci", "CI", "Remedy's own CI stages, executed locally.", user_facing=False),
```

2. `ci.run` CommandEntry description (near line 2052). FROM:
```
        description="Run Remedy's own CI stages locally and print the summary.",
```
TO:
```
        description="Execute Remedy's own CI stages locally and print the summary.",
```

3. `ci.run`'s `--stage` ArgDef (near line 2055). FROM:
```
            ArgDef("--stage", "Run one stage by name instead of all of them", required=False, is_option=True),
```
TO:
```
            ArgDef("--stage", "Execute one stage by name instead of all of them", required=False, is_option=True),
```

4. `integrity.check` CommandEntry description (near line 2067). FROM:
```
        description="Run pre-handoff integrity checks.",
```
TO:
```
        description="Execute pre-handoff integrity checks.",
```

5. `integrity.check`'s `--collect-only` ArgDef (near line 2071). FROM:
```
            ArgDef("--collect-only", "Also run pytest collect-only", required=False, is_option=True, default="false"),
```
TO:
```
            ArgDef("--collect-only", "Also execute pytest collect-only", required=False, is_option=True, default="false"),
```

6. `teacher` group description (near line 123). FROM:
```
    "teacher": GroupDef("teacher", "Teacher", "Explain a run. Read-only, never steers it."),
```
TO:
```
    "teacher": GroupDef("teacher", "Teacher", "Explain a run from its evidence. Read-only, never steers it."),
```

7. `teacher.ask` CommandEntry description (near line 274). FROM:
```
        description="Ask the teacher about a run or your code. Records one spend row; never steers the run.",
```
TO:
```
        description="Ask the teacher about a run's evidence or your code. Records one spend row; never steers the run.",
```

8. `teacher.ask`'s `--job-id` ArgDef (near line 278). FROM:
```
            ArgDef("--job-id", "Job whose run log grounds the answer", required=False, is_option=True),
```
TO:
```
            ArgDef("--job-id", "Job whose run log (its evidence) grounds the answer", required=False, is_option=True),
```

9. `teacher.narrate` CommandEntry description (near line 260). FROM:
```
        description="Narrate a job's run log in plain sentences (read-only).",
```
TO:
```
        description="Narrate a job's run evidence in plain sentences (read-only).",
```

10. `test` group description (near line 128). FROM:
```
    "test": GroupDef("test", "Test", "Discover and run project tests.", user_facing=False),
```
TO:
```
    "test": GroupDef("test", "Test", "Discover and execute project tests.", user_facing=False),
```

11. `test.status` CommandEntry description (near line 610). FROM:
```
        description="Show current test run status for a job (lease state, latest run, usage).",
```
TO:
```
        description="Show current test run status for a job's tasks (lease state, latest run, usage).",
```

12. `test.result` CommandEntry description (near line 621). FROM:
```
        description="Show a safe test run result by test_run_id (read-only; no raw output).",
```
TO:
```
        description="Show a safe test run result for a task, by test_run_id (read-only; no raw output).",
```

13. `test.result`'s `test_run_id` ArgDef (near line 623). FROM:
```
        args=(ArgDef("test_run_id", "Test run ID"), _JSON_OPT),
```
TO:
```
        args=(ArgDef("test_run_id", "Test run ID (identifies one task's test execution)"), _JSON_OPT),
```

14. `test.list` CommandEntry description (near line 631). FROM:
```
        description="List safe test run records for a job (read-only; no raw output).",
```
TO:
```
        description="List safe test run records for a job's tasks (read-only; no raw output).",
```

15. `test.run`'s `--intent-id` ArgDef (near line 592). FROM:
```
            ArgDef("--intent-id", "Link run to a patch intent ID", required=False,
                   is_option=True, default=""),
```
TO:
```
            ArgDef("--intent-id", "Link run to a patch intent ID (same task as --task-id)", required=False,
                   is_option=True, default=""),
```

16. `test.run`'s `--apply-id` ArgDef (near line 594). FROM:
```
            ArgDef("--apply-id", "Link run to an apply record ID", required=False,
                   is_option=True, default=""),
```
TO:
```
            ArgDef("--apply-id", "Link run to an apply record ID (same task as --task-id)", required=False,
                   is_option=True, default=""),
```

17. `mission.run` CommandEntry description (near line 869). FROM:
```
        description="Run the F070 orchestrator for one mission's jobs. Stops on a terminal move, the iteration limit, a stop request or an escalation.",
```
TO:
```
        description="Execute the F070 orchestrator for one mission's jobs. Stops on a terminal move, the iteration limit, a stop request or an escalation.",
```

18. `mission.run`'s `--iterations` ArgDef (near line 873). FROM:
```
            ArgDef("--iterations", "Max orchestrator iterations this run", required=False, is_option=True),
```
TO:
```
            ArgDef("--iterations", "Max iterations before the orchestrator stops", required=False, is_option=True),
```

19. `mission.run`'s `--no-llm` ArgDef (near line 874). FROM:
```
            ArgDef("--no-llm", "Run without a provider — reports the honest no_provider terminal", required=False, is_option=True, is_flag=True),
```
TO:
```
            ArgDef("--no-llm", "Execute without a provider — reports the honest no_provider terminal", required=False, is_option=True, is_flag=True),
```

20. `mission.readiness` CommandEntry description (near line 1057). FROM:
```
        description="Read-only: is this job safe to run unattended?",
```
TO:
```
        description="Read-only: is this job safe to execute unattended?",
```

21. `run.show` CommandEntry description (near line 1569). FROM:
```
        description="Show a persisted ping-pong run report.",
```
TO:
```
        description="Show a persisted ping-pong run report, task and evidence included.",
```

22. `run.show`'s `run_id` ArgDef (near line 1574). FROM:
```
            ArgDef("run_id", "Run ID"),
```
TO:
```
            ArgDef("run_id", "Run ID (its task and evidence folder)"),
```

23. `job.resume`'s `--cycles` ArgDef (near line 1382). FROM:
```
            ArgDef("--cycles", "Maximum cycles for the resumed run (capped by the rollout default)",
                   required=False, is_option=True),
```
TO:
```
            ArgDef("--cycles", "Maximum cycles for the resumed run's tasks (capped by the rollout default)",
                   required=False, is_option=True),
```

24. `job.run`'s `--test-command` ArgDef (near line 1611). FROM:
```
            ArgDef("--test-command", "Test command to run in staging (persisted on continuation)", required=False, is_option=True, default=None),
```
TO:
```
            ArgDef("--test-command", "Test command to execute in staging (persisted on continuation)", required=False, is_option=True, default=None),
```

25. `job.apply` CommandEntry description (near line 1865). FROM:
```
        description="Review and apply job workspace changes to target repo. Dry-run by default; --approve applies.",
```
TO:
```
        description="Review and apply job workspace changes to target repo. Preview by default; --approve applies.",
```

26. `job.apply`'s `--approve` ArgDef (near line 1872). FROM:
```
            ArgDef("--approve", "Apply changes (without this flag, dry-run only)", required=False, is_option=True, default="false"),
```
TO:
```
            ArgDef("--approve", "Apply changes (without this flag, preview only)", required=False, is_option=True, default="false"),
```

27. `job.evidence`'s `--verification-command` ArgDef (near line 1855). FROM:
```
            ArgDef("--verification-command", "Explicit verification command to execute and record (repeatable). Each is run and stored as a verification run covering the test files it names", required=False, is_option=True),
```
TO:
```
            ArgDef("--verification-command", "Explicit verification command to execute and record (repeatable) into the evidence bundle. Each execution is stored as a verification run covering the test files it names", required=False, is_option=True),
```

28. `do.run`'s `--ui` ArgDef (near line 1549). FROM:
```
            ArgDef("--ui", "Start UI alongside run", required=False, is_option=True, default="false"),
```
TO:
```
            ArgDef("--ui", "Start UI alongside execution", required=False, is_option=True, default="false"),
```

29. `stats.bench` CommandEntry description (near line 1661). FROM:
```
        description=(
            "Capability trend from the append-only bench history: the last run, "
            "the series before it, and a regression warning naming the order and "
            "both numbers. Never runs the bench (read-only)."
        ),
```
TO:
```
        description=(
            "Capability trend from the append-only bench history: the latest entry, "
            "the series before it, and a regression warning naming the order and "
            "both numbers. Never executes the bench (read-only)."
        ),
```

30. `stats.bench`'s `--series` ArgDef (near line 1670). FROM:
```
            ArgDef("--series", "Which bench series to read (default: the series of the latest run)", required=False, is_option=True),
```
TO:
```
            ArgDef("--series", "Which bench series to read (default: the series of the latest entry)", required=False, is_option=True),
```

## Constraints

- `command:stats.bench:description` still carries a separate, UNCHANGED
  `Order`-word violation (the word "order" appears in "naming the order and
  both numbers") — that is round 4's already-decided word-sense collision,
  not part of this round's scope; edit 29 touches only the `Run`-word text
  (the two "run" occurrences) and must not touch "the order and both
  numbers".
- The C2 commit's path set is exactly one file:
  `apps/cli/command_catalog.py`.
- Bare `ruff` is denied to this session's shell; use `python3 -m ruff check
  <path>`.
- Do not touch any handler docstring or runtime-printed string (e.g.
  `apps/cli/commands/integrity_cmd.py`, `apps/cli/commands/mission_cmd.py`,
  `apps/cli/commands/do_cmd.py`, `apps/cli/commands/bench_cmd.py`,
  `packages/orchestration/job_apply.py`) even where they happen to echo the
  OLD catalog text word-for-word — this round's scope is the catalog surface
  only (T2_F281.md T001), and editing those files would be scope creep
  outside this block's change set.

## Gates (at most six; run and record real exit codes)

- G1 VIOLATION DIFF: import `tests.docs.test_vocabulary` and report
  `_meaning_violations()` and `_synonym_offenders()` against the real,
  committed (post-edit) catalog. Expect meaning violations to read 184
  (216 minus 32: the 30 Run-bucket fixes plus the 2 bonus Job-bucket fixes
  from edits 11 and 14), synonym offenders unchanged at 2. If it doesn't read
  exactly 184, STOP and report before committing (you may `git stash` your
  C2 edit to confirm the before-count reads 216, then restore).
- G2 TARGETED: `python3 -m pytest tests/docs/test_vocabulary.py
  tests/test_command_catalog.py tests/cli/test_advertised_commands.py -q` —
  expect 74 passed, unchanged.
- G3 CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` — expect 42
  passed, unchanged.
- G4 RUFF: `python3 -m ruff check apps/cli/command_catalog.py` reads `All
  checks passed!`.
- G5 SWEEP: `grep -c '(same task as --task-id)' apps/cli/command_catalog.py`
  reads 2 (edits 15 and 16); `grep -c 'Dry-run by default'
  apps/cli/command_catalog.py` reads 0 (edit 25 landed; the old phrase is
  gone).
- G6 TREE: `git status --porcelain` empty, `git worktree list` shows only the
  primary checkout, HEAD matches `origin/feature/f281-cli-help-surface` after
  push.

No mutation red-proof is ordered this round, for the same reason rounds 2-6
named: G1's own before/after diff against the real vocabulary-check functions
is the red/green proof for a prose-only catalog edit.

## Done-when

C1 and C2 are committed with the exact path sets named above; G1-G6 all pass
with real recorded output, G1's delta matching exactly (216→184, 32 fixed, 0
introduced); the branch is pushed; `.agent/handoff.md` is rewritten as C3
naming this round, its commits, its verification results, and the next
expected action (round 8 addresses the two remaining buckets: Job at ~118,
Project at 65).
