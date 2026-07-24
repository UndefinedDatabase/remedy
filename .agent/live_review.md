# Live Review — F147 Golden-path CLI

Per-feature ledger. Findings are authored by the reviewer (Window 1)
and applied here verbatim by the worker. R-XXXX IDs continue
monotonically across features (last used: R-0084). History lives in
git and in each feature's evidence zip.

### R-0085: bare-mission intercept silently drops explicit flags; legacy do-run path unreachable for bare form
- **Status**: Done: R-0085
- **Severity**: High
- **Area**: apps/cli/commands/do_cmd.py (_cmd_do / _is_bare_mission), apps/cli/grouped.py
- **Details**: _is_bare_mission checks only a subset of do.run flags. Any
  invocation carrying unchecked flags — --max-total-tokens,
  --max-provider-calls, --max-wall-clock-minutes, --deadline, --mode,
  --max-rounds, --test-command, --timeout-profile, --provider-timeout-sec,
  --repair-rounds, --keep-staging, --stream-evidence,
  --claude-cli-write-mode, --max-output-chars, or explicit
  --autonomy-level 0/1/2 / --max-cycles 3 — still matches and is rerouted
  to the plan-only golden path; those flags are SILENTLY IGNORED (F018
  budget flags dropped without error). Explicit `remedy do run "<goal>"`
  is indistinguishable from bare `remedy do "<goal>"`, so the legacy v1
  executor path is unreachable for a bare goal. Silent-scope-change class.
- **Evidence**: diff 2e4a8c3 — _is_bare_mission omits the flags above;
  reviewer traced `remedy do "x" --max-total-tokens 500` → intercept True.
- **Expected fix**: Golden path triggers ONLY when the invocation is truly
  bare: mission plus at most --json/--repo, and the `run` subcommand was
  injected (not typed). Detect explicitness robustly (injection marker set
  in grouped.py at the _DEFAULT_COMMAND injection site, or argparse None-
  sentinel defaults for the intercept-relevant flags) — worker's choice,
  recorded in .agent/decisions.md. ANY other explicit flag or explicit
  `run` → legacy path unchanged. Tests: bare mission → golden path;
  mission + --max-total-tokens → legacy path (budgets honored, not
  dropped); explicit `do run "goal"` → legacy path; bare + --json →
  golden path.

### R-0086: corrupt runtime state reported as "stopped" — spec demands "unknown" + warning
- **Status**: Done: R-0086
- **Severity**: Medium
- **Area**: apps/cli/commands/status_cmd.py (runtime section)
- **Details**: load_state() returns None for BOTH absent and unreadable
  state files; status maps None → "stopped". An unreadable/corrupt
  runtime.json therefore reports "stopped" with no warning. Feature spec:
  degrade to "unknown" WITH a warning, never a crash. Acceptance case
  "corrupt runtime state file" has no test.
- **Evidence**: dev_server.py:700-722 (load_state_result distinguishes
  STATE_ABSENT / STATE_UNREADABLE; load_state discards it);
  status_cmd.py maps None → "stopped".
- **Expected fix**: Use load_state_result(repo): STATE_ABSENT → "stopped";
  STATE_UNREADABLE (or any parse error) → "unknown" + warning line (text)
  and a warning field (json). Test: write garbage runtime.json into the
  runtime state path → status exit 0, runtime "unknown", warning present.

### R-0087: stops_pending counts blocker stop-reasons, not F011 kill-switch stop requests
- **Status**: Done: R-0087
- **Severity**: Medium
- **Area**: apps/cli/commands/status_cmd.py (stops section)
- **Details**: Counts stop_reasons.list_stop_reasons(job_id) with
  status=="active" — the blocker/sr:* subsystem. "Pending stop requests"
  in the feature = F011 kill-switch requests
  (packages/orchestration/safe_points.stop_requested, control/jobs/<id>/
  stop.json). A pending `remedy job stop` is invisible; blocker reasons
  are miscounted as stops.
- **Evidence**: status_cmd.py stops loop; safe_points.py:389
  (stop_requested — "is a stop pending?").
- **Expected fix**: stops_pending = count of non-terminal jobs where
  safe_points.stop_requested(str(job.id)) is not None. Test: create job →
  request stop via the F011 path → status shows stops_pending == 1.

### R-0088: decisions_open computed with empty events — event-derived decisions never counted
- **Status**: Open
- **Severity**: Medium
- **Area**: apps/cli/commands/status_cmd.py (decisions section)
- **Details**: list_decisions(j, []) passes an empty event list; all
  event-derived decision classes are structurally invisible, so
  decisions_open undercounts. Canonical pattern exists in decision.py:
  load_run_events(resolve_data_root(), job_id) → list_decisions(job,
  events).
- **Evidence**: decision.py:32-41 vs status_cmd.py decisions loop.
- **Expected fix**: Reuse the decision.py pattern per job (import, no
  copy). Test: fixture producing at least one open decision visible via
  `remedy decision list` must yield decisions_open >= 1 in status.

### R-0089: status omits the "all projects" label and per-section next-command lines
- **Status**: Open
- **Severity**: Medium
- **Area**: apps/cli/commands/status_cmd.py
- **Details**: Feature spec: until scoping lands, status shows all jobs
  and SAYS "all projects" (label now, filter later) — label absent in
  text and json. Spec also: "Each section ends with the single most
  useful next command" — no section prints one.
- **Evidence**: status_cmd.py full read — no "all projects", no next-
  command lines.
- **Expected fix**: Jobs section labeled "all projects" (text header +
  json field, e.g. scope: "all projects"). Each section ends with one
  next command (jobs → remedy do/decision list <id> as fits; decisions →
  remedy decision list <id>; runtime/stops → the most useful existing
  command). Assert label + at least one next-command line in tests.

### R-0090: golden-path smoke lacks the stop leg
- **Status**: Open
- **Severity**: Medium
- **Area**: tests/cli/test_golden_path.py (TestGoldenPathSmoke)
- **Details**: Feature T003 smoke = init → do → status → STOP → status
  shows the stopped job. Implemented smoke ends at the first status; the
  kill-switch leg is untested.
- **Evidence**: test_golden_path.py:284-309.
- **Expected fix**: Extend the smoke: `remedy job stop <id>` (F011) →
  second status run shows the job's stop as pending (stops_pending >= 1
  after R-0087) or the stopped state — assert whichever the machinery
  produces, honestly.

### R-0091: handback without raw verification transcripts; baseline mischaracterized
- **Status**: Open
- **Severity**: Low
- **Area**: .agent/handoff.md
- **Details**: Instructed handback format (raw command/exit/output
  transcripts, baseline vs final) was not delivered; baseline stated as
  "21 failed (all docs/missing-file; unrelated)" — the real main baseline
  is 20 failed incl. catalog-classification and runtime-timeout tests.
  Numbers were honest in aggregate (reviewer verified zero new failures)
  but the handoff must carry the evidence, not characterizations.
- **Evidence**: handoff.md "Test baseline" section vs reviewer's
  main-worktree run (20 failed / 962 passed; identical ruff 432).
- **Expected fix**: Next handback includes raw transcripts: exact
  commands, exit codes, tail output for golden-path run, full-gate run on
  branch AND the stated main baseline comparison. Fixed by the handback
  itself; mark Done when delivered.
