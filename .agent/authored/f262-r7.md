STEP T002/5 - F262 List commands v2, ROUND 7
FEATURE F262 - List commands v2 (Tier 2) - SESSION 2, ROUND 7

Goal
  Ship T002 batch 5: `job.list` and `queue.list` gain `--json` end to
  end (catalog `args` + `supports_json=True`, handler `json_output`
  kwarg + json branch, dispatch lambda) - the same shape round 6
  proved once for `project.list`. `job.list`'s json output carries
  `created_at` (its TEXT output already prints an ISO date - only
  --json was missing). `queue.list`'s json output carries the RAW
  `created_at` string plus `goal` (its TEXT output prints an AGE,
  `_age(entry.created_at)`, a pre-existing derived display this round
  does NOT change - out of scope, not a gap). Neither `Job` nor the
  queue entry model has a second/updated timestamp, so neither json
  gains an `updated_at` key - same precedent as rounds 5 and 6. Three
  production files (apps/cli/command_catalog.py touched TWICE, once
  per command; apps/cli/commands/job.py; apps/cli/commands/
  queue_cmd.py), two test files (tests/test_grouped_cli.py,
  tests/cli/test_queue_cmd.py). No model or store change.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f262-r7.md
  C0b mirror it to .agent/last_block.md
  C1  append GATE6 to .agent/live_review.md - books round 6's PASS
      verdict (the reviewer's own, independently re-verified)
  C2  apply CODE PAIR J1 and CODE PAIR Q1 to
      apps/cli/command_catalog.py (two separate edits, one commit);
      apply CODE PAIR J2 and CODE PAIR J3 to apps/cli/commands/job.py;
      apply CODE PAIR Q2 and CODE PAIR Q3 to
      apps/cli/commands/queue_cmd.py; add the TEST SPEC additions
      below to tests/test_grouped_cli.py and
      tests/cli/test_queue_cmd.py (ALL of the above in ONE commit,
      five files total)
  C3  apply PLAN8 to .agent/plan.md
  C4  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f262-r7.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md (C1) - apps/cli/command_catalog.py (C2) -
  apps/cli/commands/job.py (C2) - apps/cli/commands/queue_cmd.py (C2) -
  tests/test_grouped_cli.py (C2) - tests/cli/test_queue_cmd.py (C2) -
  .agent/plan.md (C3) - .agent/handoff.md (C4)

CODE PAIR J1 (apps/cli/command_catalog.py) - REWRITE. FROM is the
ENTIRE `job.list` CommandEntry literal, unique in the file (the only
entry whose command_id is "job.list").
<<<BEGIN PAIR_J1_FROM>>>
    CommandEntry(
        command_id="job.list",
        group_id="job",
        subcommand="list",
        description="List jobs (scoped to current project by default).",
        action_class="read_only",
        args=(_PROJECT_SCOPE_OPT, _ALL_PROJECTS_FLAG),
    ),
<<<END PAIR_J1_FROM>>>
<<<BEGIN PAIR_J1_TO>>>
    CommandEntry(
        command_id="job.list",
        group_id="job",
        subcommand="list",
        description="List jobs (scoped to current project by default).",
        action_class="read_only",
        args=(_PROJECT_SCOPE_OPT, _ALL_PROJECTS_FLAG, _JSON_OPT),
        supports_json=True,
    ),
<<<END PAIR_J1_TO>>>

CODE PAIR Q1 (apps/cli/command_catalog.py) - REWRITE, the SAME file as
J1 but a DIFFERENT, non-overlapping entry - apply both independently.
FROM is the ENTIRE `queue.list` CommandEntry literal, unique in the
file.
<<<BEGIN PAIR_Q1_FROM>>>
    CommandEntry(
        command_id="queue.list",
        group_id="queue",
        subcommand="list",
        description="List queue entries (scoped to the current project by default).",
        action_class="read_only",
        args=(_PROJECT_SCOPE_OPT, _ALL_PROJECTS_FLAG),
        related=("queue.add",),
    ),
<<<END PAIR_Q1_FROM>>>
<<<BEGIN PAIR_Q1_TO>>>
    CommandEntry(
        command_id="queue.list",
        group_id="queue",
        subcommand="list",
        description="List queue entries (scoped to the current project by default).",
        action_class="read_only",
        args=(_PROJECT_SCOPE_OPT, _ALL_PROJECTS_FLAG, _JSON_OPT),
        supports_json=True,
        related=("queue.add",),
    ),
<<<END PAIR_Q1_TO>>>
`_JSON_OPT` is already defined and imported at module level in this
file - reference the existing name in both J1 and Q1, do not add a new
import or definition.

CODE PAIR J2 (apps/cli/commands/job.py) - REWRITE, the entire
`_cmd_list_jobs` function body, unique in the file.
<<<BEGIN PAIR_J2_FROM>>>
def _cmd_list_jobs(
    *,
    project: str | None = None,
    all_projects: bool = False,
) -> None:
    from packages.orchestration.project_scope import resolve_scope, scoped_jobs

    scope = resolve_scope(project_flag=project, all_projects=all_projects)
    jobs, degraded, skipped = scoped_jobs(scope)
    if not jobs:
        print("No jobs found.")
        return
    known = _known_project_ids()
    for job in jobs:
        label = _scope_label(job, scope, known)
        print(f"{job.id}  {job.state.value:<12}  {job.created_at.isoformat()}  {job.name}{label}")
    if skipped:
        print(f"  ({len(skipped)} unreadable job file(s) skipped)", file=sys.stderr)
<<<END PAIR_J2_FROM>>>
<<<BEGIN PAIR_J2_TO>>>
def _cmd_list_jobs(
    *,
    project: str | None = None,
    all_projects: bool = False,
    json_output: bool = False,
) -> None:
    from packages.orchestration.project_scope import resolve_scope, scoped_jobs

    scope = resolve_scope(project_flag=project, all_projects=all_projects)
    jobs, degraded, skipped = scoped_jobs(scope)
    if json_output:
        import json as _json
        print(_json.dumps({
            "version": 1,
            "job_count": len(jobs),
            "jobs": [{"id": str(job.id), "state": job.state.value, "name": job.name,
                     "created_at": job.created_at.isoformat(),
                     "project_id": job.project_id or ""} for job in jobs],
        }, sort_keys=True))
        return
    if not jobs:
        print("No jobs found.")
        return
    known = _known_project_ids()
    for job in jobs:
        label = _scope_label(job, scope, known)
        print(f"{job.id}  {job.state.value:<12}  {job.created_at.isoformat()}  {job.name}{label}")
    if skipped:
        print(f"  ({len(skipped)} unreadable job file(s) skipped)", file=sys.stderr)
<<<END PAIR_J2_TO>>>
`degraded` (from `scoped_jobs`) is already unused in the ORIGINAL
function - it stays unused, not a defect this round introduces or
must fix.

CODE PAIR J3 (apps/cli/commands/job.py) - REWRITE, the
`COMMAND_HANDLERS["job.list"]` dispatch entry, unique in the file.
<<<BEGIN PAIR_J3_FROM>>>
    "job.list": lambda args: _cmd_list_jobs(
        project=getattr(args, "project", None),
        all_projects=getattr(args, "all_projects", False),
    ),
<<<END PAIR_J3_FROM>>>
<<<BEGIN PAIR_J3_TO>>>
    "job.list": lambda args: _cmd_list_jobs(
        project=getattr(args, "project", None),
        all_projects=getattr(args, "all_projects", False),
        json_output=args.json,
    ),
<<<END PAIR_J3_TO>>>

CODE PAIR Q2 (apps/cli/commands/queue_cmd.py) - REWRITE, the entire
`_cmd_queue_list` function body, unique in the file.
<<<BEGIN PAIR_Q2_FROM>>>
def _cmd_queue_list(*, project: str | None = None, all_projects: bool = False) -> None:
    from packages.orchestration.job_queue import list_entries_safe

    if all_projects:
        project_ids = _project_ids_with_a_queue()
    else:
        project_ids = [_resolve_project_id(project)]

    rows: list[tuple[str, Any]] = []
    skipped_total = 0
    for project_id in project_ids:
        entries, _degraded, skipped = list_entries_safe(project_id)
        skipped_total += len(skipped)
        rows.extend((project_id, entry) for entry in entries)

    if not rows:
        print("No queue entries found.")
    for project_id, entry in rows:
        owner = entry.claimed_by or "-"
        label = f"  (project: {project_id[:8]})" if all_projects else ""
        print(f"{entry.id[:12]}  {entry.status:<8}  prio {entry.priority:<4}  "
              f"{_age(entry.created_at):>4}  {owner:<24}  {_goal_label(entry)}{label}")
<<<END PAIR_Q2_FROM>>>
<<<BEGIN PAIR_Q2_TO>>>
def _cmd_queue_list(*, project: str | None = None, all_projects: bool = False,
                    json_output: bool = False) -> None:
    from packages.orchestration.job_queue import list_entries_safe

    if all_projects:
        project_ids = _project_ids_with_a_queue()
    else:
        project_ids = [_resolve_project_id(project)]

    rows: list[tuple[str, Any]] = []
    skipped_total = 0
    for project_id in project_ids:
        entries, _degraded, skipped = list_entries_safe(project_id)
        skipped_total += len(skipped)
        rows.extend((project_id, entry) for entry in entries)

    if json_output:
        import json as _json
        print(_json.dumps({
            "version": 1,
            "entry_count": len(rows),
            "entries": [{"id": entry.id, "status": entry.status, "priority": entry.priority,
                        "created_at": entry.created_at, "claimed_by": entry.claimed_by or "",
                        "goal": _goal_label(entry), "project_id": project_id}
                       for project_id, entry in rows],
        }, sort_keys=True))
        return

    if not rows:
        print("No queue entries found.")
    for project_id, entry in rows:
        owner = entry.claimed_by or "-"
        label = f"  (project: {project_id[:8]})" if all_projects else ""
        print(f"{entry.id[:12]}  {entry.status:<8}  prio {entry.priority:<4}  "
              f"{_age(entry.created_at):>4}  {owner:<24}  {_goal_label(entry)}{label}")
<<<END PAIR_Q2_TO>>>
`entry.created_at` is already a plain ISO string (the existing
`_age(created_at: str, ...)` helper a few lines above takes it as
`str` and calls `datetime.fromisoformat` on it) - do not call
`.isoformat()` on it, it is not a datetime object. `skipped_total` and
its trailing stderr print (`if skipped_total: print(...)`, the two
lines AFTER this function's own end - not shown in this FROM/TO slice)
are UNCHANGED and stay exactly where they are, after this pair's
replaced region.

CODE PAIR Q3 (apps/cli/commands/queue_cmd.py) - REWRITE, the
`COMMAND_HANDLERS["queue.list"]` dispatch entry, unique in the file.
<<<BEGIN PAIR_Q3_FROM>>>
    "queue.list": lambda args: _cmd_queue_list(
        project=getattr(args, "project", None),
        all_projects=getattr(args, "all_projects", False),
    ),
<<<END PAIR_Q3_FROM>>>
<<<BEGIN PAIR_Q3_TO>>>
    "queue.list": lambda args: _cmd_queue_list(
        project=getattr(args, "project", None),
        all_projects=getattr(args, "all_projects", False),
        json_output=args.json,
    ),
<<<END PAIR_Q3_TO>>>

TEST SPEC for C2 - written BY HAND (not marker-extracted), two
separate additions:

  (a) In tests/test_grouped_cli.py, append at the true END of the
  file (after `TestProjectListCLI`, currently the last class), ONE
  new class matching that class's own established style (monkeypatch
  `REMEDY_DATA_DIR`, `StringIO` + `monkeypatch.setattr("sys.stdout",
  ...)`, local imports inside each test body). `_make_job` and
  `save_job` are ALREADY imported/defined at the top of this file (see
  `_make_job()` near the top and `from packages.orchestration.storage
  import save_job`) - reuse them, do not redefine.

      class TestJobListCLI:
          """job.list JSON must include version: 1, job_count and created_at."""

          def test_catalog_has_json_flag(self) -> None:
              from apps.cli.command_catalog import get_command
              cmd = get_command("job.list")
              assert cmd.supports_json is True
              assert any(a.name == "--json" for a in cmd.args)

          def test_list_json_has_created_at(self, tmp_path, monkeypatch) -> None:
              monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
              job = _make_job()
              save_job(job)
              from apps.cli.commands.job import _cmd_list_jobs
              buf = StringIO()
              monkeypatch.setattr("sys.stdout", buf)
              _cmd_list_jobs(json_output=True, all_projects=True)
              data = json.loads(buf.getvalue())
              assert data["version"] == 1
              assert data["jobs"][0]["created_at"]

  (b) In tests/cli/test_queue_cmd.py: ONE new method added to the
  EXISTING `TestCatalog` class (place it directly after
  `test_no_queue_command_may_execute_or_mutate_the_repo`, the last
  method in that class):

          def test_list_has_json_flag(self):
              from apps.cli.command_catalog import get_command
              assert get_command("queue.list").supports_json is True

  ONE new method added to the EXISTING `TestList` class (place it
  directly after `test_a_corrupt_entry_is_counted_not_hidden`, the
  last method in that class), using the file's own `project` fixture
  and `_run` helper exactly as its neighboring tests do:

          def test_json_has_created_at_and_goal(self, project):
              data_root, project_id = project
              _run(["queue", "add", "json goal", "--project", project_id], data_root)

              proc = _run(["queue", "list", "--project", project_id, "--json"], data_root)
              data = json.loads(proc.stdout)
              assert data["version"] == 1
              assert data["entries"][0]["created_at"]
              assert data["entries"][0]["goal"] == "json goal"

Constraints
  1. C1's append to .agent/live_review.md is applied BYTE FOR BYTE:
     extract GATE6 from the COMMITTED .agent/authored/f262-r7.md by its
     BEGIN/END markers (excluded) and apply with a script, never by
     retyping. GATE6 carries ZERO internal newlines and NO trailing
     newline of its own. The base file (measured by the reviewer before
     this round) is 2433283 bytes with NO trailing newline, last byte
     `.`; the applied file must equal base + one newline byte + GATE6's
     own bytes. Report the arithmetic and a byte comparison against a
     script-extracted copy of GATE6, both directions, plus a negative
     control (flip GATE6's first byte in a scratch copy, confirm it
     does NOT match the real tail).
  2. All six PAIRs (J1, Q1, J2, J3, Q2, Q3) are extracted from the
     COMMITTED .agent/authored/f262-r7.md by marker index and applied
     with str.replace(FROM, TO, 1) via a script, never by hand-
     retyping. Before editing, confirm each FROM occurs EXACTLY ONCE
     in its target file (report the count for all six; if any is not
     exactly 1, STOP and report rather than editing). All six are
     REWRITEs: report FROM count before (1), FROM count after (0), TO
     count after (1) for each. J1 and Q1 both target
     apps/cli/command_catalog.py - apply them as two independent
     str.replace calls against the same file, in either order, and
     confirm afterward that BOTH edits landed (grep for both
     `command_id="job.list"` and `command_id="queue.list"` each still
     appearing exactly once, now each followed by `supports_json=True`
     within its own entry).
  3. The test additions are written by hand from the TEST SPEC above
     (not extracted from a marker slice), placed exactly where the
     spec says.
  4. `python3 -m py_compile apps/cli/command_catalog.py
     apps/cli/commands/job.py apps/cli/commands/queue_cmd.py
     tests/test_grouped_cli.py tests/cli/test_queue_cmd.py` must exit
     0 for all five (ruff is denied this session per prior rounds -
     attempt it anyway and report the exact refusal or the real
     result, never assume).
  5. C2 is ONE commit covering all five files.
  6. PLAN8 REPLACES .agent/plan.md whole-file, ending WITHOUT a
     trailing newline, same as every prior round.
  7. Before writing each pair, confirm its FROM is unique in its
     target file exactly as constraint 2 requires - report each count
     explicitly, not just "looks fine".
  8. A sentence OUTSIDE the change set that earlier rounds already
     found stale (docs/roadmap/features/T2_F262.md line 5,
     "REGISTRATION ONLY") remains outside this round's change set too -
     re-declare it in the handback, do not repair it.
  9. Read .agent/STOP from disk before the first commit and again
     before C4. If it exists, finish the commit in hand, write the
     handback, and stop.
  10. Self-review loop before every commit (git diff --stat, git diff).
      Push after C4 (git push origin feature/f262-list-commands-v2). No
      pull request, no merge.
  11. `git rev-parse HEAD` before C0a must read
      `7c25e9363ee43c6b91d26659e7d538ce9b9650f2` (report the full SHA);
      `git branch --show-current` must read
      `feature/f262-list-commands-v2`.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f262-r7.md .agent/last_block.md
     One digest, twice. Report both lines verbatim.
  G2 THE LEDGER APPEND, FULL FORENSICS. Report:
       base size immediately before C1 (bytes, trailing-newline byte)
       GATE6 own byte length and internal-newline count
       base + 1 + GATE6_length, compared against the post-C1 file's
         real byte length - state match True/False
       tail slice (last GATE6_length bytes of the post-C1 file)
         compared against GATE6 - state equal True/False
       negative control: flip the first byte of a COPY of GATE6,
         confirm the flipped copy does NOT match the real tail - state
         rejected True/False
  G3 THE SIX PAIRS, READ AND COUNTED, PER CONSTRAINT 2's SHAPES. Then
     read the FULL diff of apps/cli/command_catalog.py,
     apps/cli/commands/job.py and apps/cli/commands/queue_cmd.py and
     confirm nothing beyond the named insertions changed in EACH file
     (every other CommandEntry, every other handler function and
     every other dispatch line byte-for-byte untouched). `python3 -m
     py_compile` on all five touched/added files, reported
     individually, each exit 0.
  G4 THE TESTS, BEFORE AND AFTER. Report
       python3 -m pytest tests/test_grouped_cli.py -q
       python3 -m pytest tests/cli/test_queue_cmd.py -q
     BOTH before C2 (baseline: 516 passed, 24 passed respectively) and
     after C2 (518 passed - base + 2 - and 26 passed - base + 2 -
     respectively, fully green, nothing else in either file touched).
  G5 THE STATE READERS AND THE CANARY (this round rewrites `.agent/`
     state):
       python3 -m pytest tests/ui_server/ -q
       python3 -m pytest tests/orchestration/test_test_runner.py -q
       python3 -m pytest tests/regression/test_resource_safety.py -q
       python3 -m pytest tests/orchestration/test_integrity_gate.py -q
       python3 -m pytest tests/cli/test_golden_path.py -q
     Report each pass count; a moved count against this session's own
     prior readings (515/52/21/16/42) is itself a finding.
  G6 THE PLAN. Extract PLAN8 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md            -> exit 0
       wc -l .agent/plan.md                      -> report; must be under 50
       grep -c '^## Goal' .agent/plan.md         -> 1
       grep -c '^## Next Steps' .agent/plan.md   -> 1
  G7 THE TREE, THE COMMITS AND THE SWEEP. `git status --porcelain`
     immediately before C4 is staged -> empty. `git ls-files
     .remedy-wt` -> no output. For C0a, C0b, C1, C2 and C3 (every
     commit before the handback), report each one's insertion count
     from `git show --numstat`, the '+' column only, compared cell by
     cell against the handback's Commits table. Then the staleness
     sweep, one line per file this round touched, plus the constraint-8
     check.

Handback
  Rewrite .agent/handoff.md per docs/agents/handback_template.md.
  SESSION 2, ROUND 7 of F262. Item-status table with every ordered item
  (C0a through C4, G1 through G7) exactly once, Commits table, one line
  per gate followed by its real transcript, Deviations (apply anything
  that looks wrong exactly as specified and declare it - never silently
  correct the block), Next (per PLAN8's Next Steps: loop.list/
  patch.list need a timestamp design decision before any date can
  appear; the remaining un-audited handlers from the 28-command audit
  still need their own pass; T003 starts once date coverage is far
  enough along to sort by). ALSO include, as the FINAL section of the
  handback, a note that this is the natural end of session 2 (rounds
  5, 6 and 7 this session, plus round 4's review at session start) -
  the operator's next session should re-run Phase 0 of
  docs/agents/self_drive_protocol.md before continuing to round 8.

<<<BEGIN GATE6>>>
Gate: R6 — the F262 R6 entry. R6 SHIPPED T002 BATCH 4, project.list gains its first `--json` support end to end (catalog `args=(_JSON_OPT,)` + `supports_json=True`, handler `json_output` kwarg + json branch, dispatch lambda) plus `created_at` in --json and a `created=` field in text mode — the first list command this feature added --json to from scratch rather than extending an existing flag, AND THE REVIEWER RE-RAN EVERY GATE ITSELF rather than reading the handback back. TRANSPORT HELD: `.agent/authored/f262-r6.md`/`.agent/last_block.md` share one sha256 digest, `28f43d572f760237b8155e83f3d4b97249221ac766a86c60a5e01ba55527b3b9`, over 327 lines. THE LEDGER APPEND (booking R5) IS PROVEN IN FULL: base immediately before C1 was 2428711 bytes with no trailing newline, GATE5 measured at 4571 bytes with 0 internal newlines, base plus one newline plus GATE5 equals 2433283 against an actual post-C1 size of 2433283 — match True; the tail slice equals GATE5 byte for byte — equal True; a negative control flipping GATE5's first byte was correctly rejected — rejected True. THE THREE PAIRS WERE READ, NOT ONLY GATED: `apps/cli/command_catalog.py`'s diff is exactly PAIR C1 (the `project.list` CommandEntry gains `args=(_JSON_OPT,)` and `supports_json=True`), every other CommandEntry confirmed byte-for-byte untouched by reading the full diff. `apps/cli/commands/project.py`'s diff is exactly PAIR H1 (the whole `_cmd_list_projects` function rewritten: new `json_output` kwarg, a json branch built before the existing empty-check, and the text print line gains `(created=...)`) and PAIR H2 (the dispatch lambda now passes `json_output=args.json`), every other handler and dispatch line confirmed byte-for-byte untouched. `python3 -m py_compile` exited 0 on all three touched/added files, run individually by the reviewer. THE THREE NEW TESTS MATCH THE TEST SPEC: `test_catalog_has_json_flag`, `test_list_json_has_created_at` and `test_list_text_shows_created` in a new `TestProjectListCLI` class appended at the true end of `tests/test_grouped_cli.py`, read in full against the block's own TEST SPEC. THE TESTS MOVED EXACTLY AS EXPECTED: `tests/test_grouped_cli.py` read 513 passing before C2 and 516 after, reproduced by the reviewer independently, base plus 3 exactly, nothing else in the file touched. THE STATE READERS AND THE CANARY WERE UNMOVED FROM THIS SESSION'S OWN BASELINE, reproduced by the reviewer: `tests/ui_server/` 515, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `test_golden_path` 42. HYGIENE HELD: `git status --porcelain` empty at HEAD `7c25e9363ee43c6b91d26659e7d538ce9b9650f2`, `git ls-files .remedy-wt` empty, and every commit's insertion counts match the handback's Commits table cell for cell, each measured independently via `git show --numstat`: `bfb62f97c2a1ec0239fe0963d491abfcfc46b799` 327 new, `8b84ed3024178baa02c09bb6e6b282142ee5791d` 221 plus 187 deleted (mirror), `50553eb1968cfb9cc5ccb72ddc71f094f3dff8b5` 2 plus 1 deleted, `0d829a161e16665d098dc16a0aad385966accd11` 2 new on `command_catalog.py`, 12 plus 3 on `project.py`, 33 new on `test_grouped_cli.py`, and `746dbb9ad359c4a5ec9c5c127ca136215adba175` 13 plus 10 deleted. THE PLAN HELD BYTE-EXACT: PLAN7 extracted from the committed authored file compares equal to `.agent/plan.md`. THE PUSH DISCHARGED — `git ls-remote origin refs/heads/feature/f262-list-commands-v2` and the local `git rev-parse HEAD` both read `7c25e9363ee43c6b91d26659e7d538ce9b9650f2`, and nothing was created or merged; the branch carries R1 through R6 unmerged. THE DECLARED DEVIATIONS ARE ALL TOOLING OR PRE-EXISTING STALENESS, NONE A DEFECT ON DISK: `git commit`'s own rewrite-detected stat line disagreed with `git show --numstat` for the whole-file C0b mirror, the same substitution already declared every prior round; several Bash compound-command rejections re-expressed as single invocations; ruff's exact denial text was equally a refusal, not a run; `docs/roadmap/features/T2_F262.md` line 5's "REGISTRATION ONLY" sentence remains stale since round 2, outside this round's declared change set, correctly declared and left unrepaired again. THE VERDICT IS PASS.
<<<END GATE6>>>

<<<BEGIN PLAN8>>>
# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 7, session 2 — T002 batch 5: `job.list` and `queue.list` gain
`--json` end to end (same shape round 6 proved once for
`project.list`). `job.list`'s json carries `created_at` (text already
had it); `queue.list`'s json carries the RAW `created_at` (text keeps
its existing AGE display, `_age()`, unchanged - a pre-existing choice
outside this round's scope) plus `goal`. Neither surface adds an
`updated_at` - neither `Job` nor the queue entry model has a second
timestamp.

## Next Steps

- `loop.list`/`patch.list` have no timestamp on their own model and
  need a design decision before any date can appear (round 3's
  handback carries the full 28-command audit).
- The remaining un-audited handlers from that 28-command list (worker.
  list, worker.registry-list, change.list, review.list, config.list,
  builder.adapter-list, the execution.* trio) still need their own
  pass once T002's date coverage stabilizes.
- T003 (sort/filter/limit behavior) starts once date coverage is far
  enough along to sort by.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, it is not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix unless it
  blocks T003's sort behavior for them specifically.
<<<END PLAN8>>>