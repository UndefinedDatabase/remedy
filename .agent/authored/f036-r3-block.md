STEP F036 R3 — T002'S SECOND HALF: the tour versioned at every reported terminal, `job show --full`'s tour section and `job show --tour`, and the fixture goldens

GOAL
Round 2 passed. Book its verdict and record DECISION F036 D4, then wire the tour: storage and
versions in `packages/orchestration/result_tour.py`, one call in `long_run_executor._apply_terminal`
directly after the final report is written, a `tour` section in `job show --full` with a
`--tour` flag that shows it alone, the module moved from the orphan guard's allow-list into the
reachability list, and three fixture goldens. No browser code, route, event name or report
content changes this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against S1 to S7 below; the two catalog descriptions of S5
are given verbatim and are typed exactly. Only the `.agent/` records travel as payloads. Read
DECISION F036 D4 in the booking diff before you write code: it is the design this specification
implements. Before you write anything, read whole: `packages/orchestration/result_tour.py` as
round 2 left it; `_apply_terminal`, `REPORTED_TERMINALS` and `TERMINAL_MAX_CYCLES_REACHED` in
`packages/orchestration/long_run_executor.py`; `write_final_report` and
`REPORT_ERROR_METADATA_KEY` in `packages/orchestration/run_report.py`; `durable_write_json` in
`packages/common/secure_fs.py`; `_cmd_show_job`, `_SHOW_SECTION_ORDER`, `ShowSectionError`,
`_SHOW_SECTIONS`, `_build_show_sections` and the `"job.show"` dispatch entry in
`apps/cli/commands/job.py`; the `job.show` entry of `apps/cli/command_catalog.py`;
`tests/cli/test_job_show.py`; `tests/orchestration/test_run_report_hook.py` for how a test drives
`_apply_terminal`; `ALLOWED_UNWIRED` in `tests/test_no_orphan_modules.py`; the head of
`tests/orchestration/import_reachability_allowlist.txt`; and the meaning table
`_meaning_violations` reads in `tests/docs/test_vocabulary.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f036-r3-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f036-r3/`           READ-ONLY. The reviewer's block.
  Every other `.remedy-wt/f036-r*-dry/`, `-sim/` and `-src/` directory and
  `.remedy-wt/f036-review/`       The reviewer's; do not touch them.
  `.remedy-wt/f036-r3-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Set `REMEDY_DATA_DIR` inside tests with `monkeypatch.setenv`, never on a command line.
Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f036-guided-result-tour`, and `git log --oneline -1` must read `42543dd9`. Report
   all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f036-r3/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f036-r3-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| booking.diff | 65 | 11302 | ebff11af5645fcd79e809a73e28ff5cf35098f54b3239d0f9e9fe43ba5f11be9 |
| plan.md | 28 | 941 | 820cd94b4b14c178410416da717186c14f4c0b4ec5178ecc081f35f760f9cf78 |

`plan.md` is a REWRITE of `.agent/plan.md`. `booking.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `42543dd9`. It appends round 2's gate entry to
`.agent/live_review.md` and DECISION F036 D4 to `.agent/decisions.md`.

THE SPECIFICATION. No `except Exception` anywhere, and no new `# noqa: BLE001`.
S1 STORAGE, in `result_tour.py`. `TOUR_ERROR_METADATA_KEY = "tour_error"`.
   `tour_path(job_id, version) -> Path` is `job_evidence_dir(job_id) / "tour.json"` for version 1
   and `/ f"tour_v{version}.json"` for version 2 and above. `stored_tour_versions(job_id) ->
   list[int]` answers the sorted versions of the REGULAR FILES directly in that directory whose
   name is `tour.json` (version 1) or `tour_v<N>.json` with N a decimal of 2 or more; `[]` when
   the directory is absent or an `OSError` stops the listing. `load_result_tour(job_id)` answers
   `None` with no version stored, else `(version, tour)` for the highest version, and raises
   `ResultTourError` naming the version when that file does not read or parse, or when
   `tour_problems` of its tour is not `[]`.
S2 THE WRITER. `write_result_tour(job, *, call_fn=<a module-private sentinel>) -> Path | None`:
   the call function is `tour_call_fn()` when none is handed in, and the one handed in —
   `None` included — otherwise; the tour is `generate_result_tour(job, call_fn)`; it is written
   with `packages.common.secure_fs.durable_write_json` at `tour_path` of one more than the
   highest stored version (1 when none), after creating the directory. An `OSError`, a
   `ValueError` or a `ResultTourError` anywhere in that sequence is caught: the job's `metadata`
   gets `TOUR_ERROR_METADATA_KEY` set to `"<ExceptionType>: <message>"` and the answer is `None`.
   On success that key is removed and the answer is the path. It never raises for those three.
S3 THE RENDERER. `render_tour_lines(tour) -> list[str]`: first
   `Guided tour of job <job_id> (<generator>, <n> stop)`, with `stops` for any n other than 1;
   then for each stop, numbered from 1, `  <i>. <title>`, then each line of the body as
   `     <line>` (five spaces), then `     -> <kind>: <ref>`.
S4 THE HOOK. In `long_run_executor._apply_terminal`, directly after the
   `write_final_report(job)` call and inside the same condition, import `write_result_tour` from
   `packages.orchestration.result_tour` in the function body, as the report writer is, and call
   `write_result_tour(job)`. Nothing else in that module changes.
S5 THE COMMAND LINE, in `apps/cli/commands/job.py` and `apps/cli/command_catalog.py`.
   `_SHOW_SECTION_ORDER` and `_SHOW_SECTIONS` gain `"tour"` LAST, after `"dod"`. `_tour_section(job)`
   answers `({"stored": <bool>, "version": <int>, "tour": <tour>}, render_tour_lines(tour))`:
   the stored latest tour with `stored` true, or, when none is stored,
   `build_fallback_tour(job)` with `stored` false and `version` 0, writing nothing; a
   `ResultTourError` from `load_result_tour` becomes `ShowSectionError("tour_unreadable",
   <its message>)`. `_build_show_sections(job, names=None)` builds only the sections whose name
   is in `names` when `names` is given. `_cmd_show_job` gains the keyword `tour: bool = False`:
   with `full` it changes nothing, and without `full` it adds the sections built with
   `names=("tour",)`, printed the way `--full` prints its sections. The dispatch passes
   `tour=getattr(args, "tour", False)`. In the catalog's `job.show` entry the `--full`
   description's closing words `status, report and Definition of Done)` become
   `status, report, Definition of Done and guided tour)`, and a new flag follows `--full`:
   `ArgDef("--tour", <DESC>, required=False, is_option=True, is_flag=True)`, where <DESC> is
   exactly the following words on one line, single-spaced where this block wraps them: Add the job's guided tour: at most eight numbered stops, each tied to a task (a step in
   the job's plan), a changed file, a file of the job's evidence folder or a command its
   Definition of Done ran
S6 THE GUARDS. `ALLOWED_UNWIRED` in `tests/test_no_orphan_modules.py` loses the
   `packages/orchestration/result_tour.py` entry round 1 added, and nothing else in that file
   changes. `tests/orchestration/import_reachability_allowlist.txt` gains the line
   `packages.orchestration.result_tour` directly after `packages.orchestration.repository_snapshot`.
   `tests/cli/test_job_show.py`'s two pins of the section order each gain `"tour"` after `"dod"`,
   and nothing else in that file changes except the new tests below.
S7 THE GOLDENS, under the NEW directory `tests/orchestration/fixtures/result_tour/`: a recorded
   model answer `model_answer.json` of five stops — two that restate the fixture's records and
   anchor to a diff path and a recorded command, one stating a number the records lack, one naming
   a path they lack, one using the word "seamless", none anchored to a task — and three goldens,
   each a whole tour as `json.dumps(tour, indent=2, sort_keys=True, ensure_ascii=False)` plus a
   final newline, with the job id replaced by `<job>`: `golden_green_mechanical.json`, the
   mechanical tour of a completed job with a report, a two-area diff and a released gate of one
   passing check; `golden_held_mechanical.json`, the mechanical tour of a blocked job with a
   report and a held gate of one passing and one failed check; and `golden_generated.json`, the
   tour `generate_result_tour` builds for the green fixture from `model_answer.json`, with the
   three claim drops listed. Each golden is written once from the code and then read by its test.

THE TESTS — appended to `tests/orchestration/test_result_tour.py` unless named otherwise. At least,
one test each: two writes give `tour.json` then `tour_v2.json`, `stored_tour_versions` reads
`[1, 2]` and `load_result_tour` answers version 2; files named `tour_v1.json`, `tour_vx.json`
and a directory `tour_v3.json` are not versions; a write handed `call_fn=None` never calls
`tour_call_fn`, and a write handed nothing calls it once (spy with `monkeypatch`); a failing
`durable_write_json` answers `None` and records `tour_error`, and a later good write removes it;
`load_result_tour` raises `ResultTourError` for unparseable JSON and for an unsound tour, and
answers `None` with nothing stored; `render_tour_lines` gives the exact lines of S3 for a
two-stop tour whose second body holds a newline; `_apply_terminal` writes exactly one
`tour.json` for each terminal of `REPORTED_TERMINALS`, none for `TERMINAL_MAX_CYCLES_REACHED` and
none with `write_report=False`, and its first stop anchors to `report.md`; each of the three
goldens equals the tour its fixture builds. In `tests/cli/test_job_show.py`: `--tour` alone
gives a `sections` object holding only `tour`, stored true and version 1 for a stored tour, and
prints `render_tour_lines` of it; with nothing stored the section reads stored false and version
0; an unreadable stored tour gives the section error `tour_unreadable` and exit 0; `--full`'s
sections end with `tour`.

BUNDLE — the commits are C1, C2, C3, C4, C5 and C6, in this order.

C1 — copy this block and the payloads
  `.agent/authored/f036-r3-block.md` := this block, `.agent/authored/f036-r3-booking.diff` :=
  booking.diff and `.agent/authored/f036-r3-plan.md` := plan.md, by `shutil.copyfile`.
  Subject: `F036 R3 C1: copy round 3 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 93. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C2 — THE BOOKING, the round's first substantive commit: `git apply` booking.diff, then rewrite
  `.agent/plan.md` := plan.md.
  Subject: `F036 R3 C2: book round 2, record DECISION F036 D4`
  Expected by `git show --numstat`: 47/0 decisions.md, 2/0 live_review.md, 7/8 plan.md.

C3 — THE CODE AND THE GUARDS: `packages/orchestration/result_tour.py`,
  `packages/orchestration/long_run_executor.py`, `apps/cli/commands/job.py`,
  `apps/cli/command_catalog.py`, `tests/test_no_orphan_modules.py`,
  `tests/orchestration/import_reachability_allowlist.txt`, and the two order pins of
  `tests/cli/test_job_show.py`.
  Subject: `F036 R3 C3: store the tour at every reported terminal and show it on the command line`

C4 — THE TESTS AND THE GOLDENS: the new tests of both test files and the fixture directory.
  Subject: `F036 R3 C4: test the tour's storage, hook and command line, and pin three goldens`

C5 — THE TOOL: your mutation tool (G5) saved as `.agent/authored/f036-r3-mutations.py`.
  Subject: `F036 R3 C5: add the round 3 mutation tool`

C6 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F036 R3 C6: rewrite handoff for round 3`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C3a and C3b, C4a and C4b), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f036-r3-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the production and guard
   paths C3 names, `tests/cli/test_job_show.py`, `tests/orchestration/test_result_tour.py`, the
   files under `tests/orchestration/fixtures/result_tour/`, and `.agent/handoff.md`. Report the
   list you measure with `git diff --name-only 42543dd9` at the branch tip after C6. Do NOT touch
   any other file under `apps/`, `packages/` or `tests/`, `.agent/context.md`,
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`, `README.md`
   or anything under `docs/`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C6, and the correction is declared. An
   EXISTING test that goes red is never edited to pass, except the two order pins S6 orders;
   report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F036's belongs to its closure. No test may reach a live model: every call function in the
   tests is a stub or `None`, and the suite's refused Ollama stays in force.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C6 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f036-r3-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f036-r3/block.md`), read back with
 `git show <C1>:<path>`. Report one reading per copy.

G2 THE BOOKING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree. Report each path beside the hash you read:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2361115 | 29737d500ff5d2eaffe283d5f0b3b5051123efe1e4da55feb09baf31ae160a58 |
 | .agent/live_review.md | 316115 | ca43e961fcf184d9490ee07e659a33ba1376951cf3fbdfd12095d214ac7d9b5d |
 | .agent/plan.md | 941 | 820cd94b4b14c178410416da717186c14f4c0b4ec5178ecc081f35f760f9cf78 |
 Also: `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's TEXT at C2,
 which the reviewer read empty; the ledger's last non-empty line at C2 begins
 `Gate: F036 R2 — `; and `git diff --name-only <C1> <C2>` names exactly the paths above.

G3 THE CODE — `python3 -m ruff check packages/orchestration/result_tour.py
 packages/orchestration/long_run_executor.py apps/cli/commands/job.py apps/cli/command_catalog.py
 tests/test_no_orphan_modules.py tests/cli/test_job_show.py tests/orchestration/test_result_tour.py`
 at C4, with its real exit code. Then report, quoted from `git show <C3>`, the whole of
 `stored_tour_versions`, `write_result_tour` and `_tour_section`, and the changed lines of
 `_apply_terminal`, `_cmd_show_job` and the catalog entry.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_result_tour.py tests/orchestration/test_run_report_hook.py tests/orchestration/test_long_run_executor.py tests/orchestration/test_pause_resume_cycles.py tests/orchestration/test_resume_kill.py tests/orchestration/test_task_veto_cycles.py tests/orchestration/test_checkpoints.py tests/orchestration/test_escalation.py tests/orchestration/test_orchestrator_loop.py tests/orchestration/test_self_healing_cycles.py tests/orchestration/test_mission_e2e.py tests/cli/test_cost_preview.py tests/cli/test_job_report.py tests/cli/test_job_show.py tests/cli/test_job_digest_cli.py tests/cli/test_product_spine.py tests/cli/test_advertised_commands.py tests/cli/test_command_catalog.py tests/test_command_catalog.py tests/test_grouped_cli.py tests/test_help_renderer.py tests/test_cli_main.py tests/orchestration/test_model_routing.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/test_agent_tooling.py tests/orchestration/test_development_artifact_boundary.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection, serially, in the primary checkout at `42543dd9` before any
 change, and read `2134 passed, 4 skipped` at real exit code 0, with the 24 round-2 nodes of
 `tests/orchestration/test_result_tour.py` among them. The skips are three in
 `tests/orchestration/test_model_routing.py` and the F252 quarantine in
 `tests/test_agent_tooling.py`, and they stay skipped. Report every `SKIPPED` line, the node
 counts of `tests/orchestration/test_result_tour.py` and `tests/cli/test_job_show.py` by
 `--collect-only -q` at `42543dd9` and at C4, and account for any difference from 2134. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f036-r3-mutations.py` takes a worktree path, and
 for each mutation below edits the named file INSIDE that worktree (asserting its FROM text
 occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/orchestration/test_result_tour.py tests/cli/test_job_show.py` from the worktree's root
 with that root first on `sys.path` after purging its `__pycache__` directories, restores the
 bytes, and prints one line per mutation: its label, the exit code, the failed count and the
 failing node ids. It runs an unmutated control first and last and ends with
 `restored byte-identical: True` and a final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  m1 (`result_tour.py`) every write goes to version 1, overwriting `tour.json`;
  m2 (`result_tour.py`) `load_result_tour` answers the LOWEST stored version;
  m3 (`result_tour.py`) `write_result_tour` catches no `OSError`;
  m4 (`result_tour.py`) a good write leaves `tour_error` in place;
  m5 (`result_tour.py`) `load_result_tour` skips the `tour_problems` check;
  m6 (`result_tour.py`) `render_tour_lines` omits each stop's anchor line;
  m7 (`result_tour.py`) `stored_tour_versions` counts directories too;
  m8 (`long_run_executor.py`) the hook runs outside the report's condition, for every terminal;
  m9 (`apps/cli/commands/job.py`) `--tour` builds every section, not only `tour`;
  m10 (`apps/cli/commands/job.py`) with nothing stored the section raises `tour_unreadable`.
 Run it: `git worktree add --detach .remedy-wt/f036-r3-mut <C5>`, then
 `python3 -B .agent/authored/f036-r3-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f036-r3-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a
 mutation that stays green is reported as green, never papered over, and you then add the test
 that catches it in C4 before C6 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f036-r3-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C6, C5, C4, C3, C2, C1 and `42543dd9` in that order
 (more lines if constraint 2 split a commit); `git worktree list | wc -l`, which must equal your
 step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3, C4 and C5 — report what
you measure), every gate's real output and exit code, the authored-text proofs, the item-status
table AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Report what you ran, not what you expected to find. Your Session section reads SESSION 1
of feature F036, round 3, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 3, then T003 — the browser's read route for the tour, the overlay with its spotlight and
navigation to each anchor, and the demo's tour. State the open-findings count, 0, and the
operator-questions count, 1.
