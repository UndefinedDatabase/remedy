# Live Review — F147 Golden-path CLI

Per-feature ledger. Findings are authored by the reviewer (Window 1)
and applied here verbatim by the worker. R-XXXX IDs continue
monotonically across features (last used: R-0084). History lives in
git and in each feature's evidence zip.

### R-0085: bare-mission intercept silently drops explicit flags; legacy do-run path unreachable for bare form
- **Status**: Resolved
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
- **Status**: Resolved
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
- **Status**: Resolved
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
- **Status**: Resolved
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
- **Status**: Resolved
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
- **Status**: Resolved
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
- **Status**: Resolved
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

### R-0092: `remedy job stop` cannot find golden-path jobs; smoke silently bypassed the broken CLI
- **Status**: Resolved
- **Reviewer**: independently verified — `remedy job stop <golden-path job>` exit 0 +
  request recorded, status stops_pending 1, unknown id exit 3; smoke runs the real CLI;
  pingpong contract untouched (tests/cli/test_job_stop.py green); kill-switch suites' only
  2 failures are byte-identical on main (pre-existing). Resolved at adf25b5.
- **Severity**: High
- **Area**: apps/cli/commands/job_stop_cmd.py (_load_job), tests/cli/test_golden_path.py (smoke),
.agent/decisions.md
- **Details**: _load_job() reads only pingpong_job.load_job_plan — the
  pingpong store. Golden-path jobs are saved via storage.save_job into
  data/jobs/ and are invisible to the kill-switch CLI:
  `remedy job stop <id>` exits with "Error: job not found" for every job
  `remedy do "<mission>"` creates, while `remedy status` lists the same
  job. Feature T003 explicitly gates on the kill switch; the specified
  smoke (init → do → status → stop → status) was designed to catch this.
  The delivered smoke instead calls safe_points.request_stop() in-process
  — a silent workaround of a real defect, unrecorded in decisions.md and
  absent from the handoff. Deviation from the authored R-0090 fix
  ("`remedy job stop <id>`") without report.
- **Evidence**: reviewer probe: do "stop probe" → job saved in
  data/jobs/, status lists it; `remedy job stop <uuid>` → "Error: job not
  found", stops_pending stays 0. job_stop_cmd.py:26-29 (pingpong-only
  lookup); test_golden_path.py smoke uses request_stop(job_id) library
  call.
- **Expected fix**: (a) job_stop_cmd._load_job falls back: pingpong
  load_job_plan miss → storage.load_job (map Core Job onto what the
  handler needs: state.value for the stopped/terminal checks; keep exit
  codes and output contract identical for pingpong jobs). A stop request
  on a planned/pending golden-path job must succeed via request_stop and
  report ok. (b) Smoke test replaced: the stop leg runs the REAL CLI
  `remedy job stop <job_id>` (subprocess, like every other leg), asserts
  exit 0, then asserts status stops_pending >= 1. The in-process
  request_stop call is removed. (c) decisions.md entry documenting the
  store-split discovery and the fallback design. (d) Direct test:
  `remedy job stop <golden-path job>` exits 0 and records the request;
  `remedy job stop <unknown id>` still exits with job-not-found.

### R-0093: explicitly typed flags at default values still enter the golden path
- **Status**: Resolved
- **Reviewer**: probed `do "x" --autonomy-level 1` → legacy executor; `do --json "x"` /
  flag-before-mission → group help (injection never fires — no silent drop); bare + --json /
  --repo → golden path. Default-of-record reconciliation noted in decisions.md. Resolved at adf25b5.
- **Severity**: Low
- **Area**: apps/cli/grouped.py (injection site), apps/cli/commands/do_cmd.py (_is_bare_mission)
- **Details**: The value-equality guard cannot distinguish "flag not
  given" from "flag given at its default": `remedy do "x"
  --autonomy-level 1` (runtime default) routes to the plan-only golden
  path although the user explicitly configured an executor run. Same for
  --max-cycles 3, --mode staged, etc. Non-default values route legacy
  correctly (verified). Related fragility: the guard hard-codes
  autonomy_level == 1 while the catalog ArgDef claims default "2" and the
  handler fallback says `or 2` — three sources of truth for one default.
- **Evidence**: reviewer probe: `do "probe" --autonomy-level 1` → golden
  path output; `do run "probe"` → legacy (marker works); catalog line
  2368 default="2" vs runtime autonomy 1.
- **Expected fix**: Decide bareness at the injection site where raw argv
  is visible: golden path ONLY if, after the mission token, no argument
  token starts with "-" except --json/--repo (and their values). Pass
  that single boolean through (extend the existing _injected_default
  marker or a second marker); the value-equality checks in _cmd_do may
  stay as a defensive belt or be dropped — worker's call, noted in
  decisions.md. Reconcile the default-of-record: make the catalog ArgDef,
  the handler fallback, and reality agree (document in decisions.md which
  one is authoritative). Tests: `do "x" --autonomy-level 1` → legacy;
  `do "x" --json` → golden; `do "x" --repo .` → golden.

### R-0094: closure handback omitted two BLOCKED_EVIDENCE zip builds
- **Status**: Open
- **Severity**: Medium
- **Area**: .agent/handoff.md (closure handback honesty)
- **Details**: remedy-review-20260724-120731-BLOCKED_EVIDENCE.zip
  (blocking: final_verifier VerificationTests total missing/invalid;
  verification_tests.json runs[0].output_hash not sha256 hex) and
  remedy-review-20260724-121236-BLOCKED_EVIDENCE.zip (evidence not
  authoritative) exist on disk; the handoff reports only the READY
  build. STATUS_closure_protocol §2: the zip attempt's outcome is
  recorded in the handoff BEFORE handback, always. Repeat of the
  R-0082/R-0091 class — second handback-honesty lapse within F147.
- **Evidence**: reviewer read .review_zip_manifest.json of both BLOCKED
  zips; handoff Evidence section lists only 121604-READY.
- **Expected fix**: Handoff rewrite lists ALL three build attempts with
  status and blocking reasons, plus what changed between attempts
  (bundle regenerated). Covered by commit 2 below.

### R-0095: STATUS line applied non-verbatim — live-review verdict misstated
- **Status**: Open
- **Severity**: Low
- **Area**: docs/roadmap/STATUS.md (F147 line)
- **Details**: Authored text said `live review PASS — ACCEPTED`; applied
  line says `live review PASS_WITH_RISKS — ACCEPTED`. The live-review
  verdict is PASS (all 9 findings Resolved, no documented risks);
  PASS_WITH_RISKS is the final_verifier verdict inside the package.
  Worker edit outside the four authorized fill slots — only reviewer-
  authored text sets verdicts.
- **Evidence**: STATUS.md F147 line vs the closure-round paste block.
- **Expected fix**: Replace the segment `live review PASS_WITH_RISKS —
  ACCEPTED` with `live review PASS — ACCEPTED`. Touch nothing else on
  the line. Covered by commit 2.

### R-0096: evidence dir not committed as instructed; deviation without decisions.md rationale
- **Status**: Open
- **Severity**: Low
- **Area**: remedy-job-evidence-f147/ (branch provenance)
- **Details**: Closure step 3 instructed committing the evidence dir
  (F081 precedent). Handoff discloses "on disk, not committed" but no
  rationale was recorded. Branch-committed evidence keeps gate JSONs
  reviewable outside the zip.
- **Evidence**: git status showed the dir untracked at closure handback.
- **Expected fix**: `git add remedy-job-evidence-f147/` in commit 2.
