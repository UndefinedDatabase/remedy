STEP F036 R1 — CLAIM F036 AND LAND T001: the tour's stop shape, the anchor check against the job's own records, and the mechanical tour

GOAL
Pull request 290 is merged; `main` is at `9dc2f2a7`. The first unchecked STATUS line is F286, the
fifth findings paydown, and no finding is open, so DECISION F036 D2 moves F286 one feature down
and F036 is claimed. Cut F036's branch, claim it, re-head the live review record, book F035's
round 10 verdict, record DECISIONS F036 D1 and D2 and operator question Q6, and land T001 in a
NEW module `packages/orchestration/result_tour.py`: the tour and stop shape and their refusal, the
anchor context read from the job's own records, the anchor check that drops what does not resolve,
and the mechanical tour — plus their tests. No file is written by the module, nothing calls it
yet, no model is called, and no report, command, event name or browser code changes this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against S1 to S7 below. Only the `.agent/` records, the
STATUS change and the F286 file line travel as payloads. Read DECISION F036 D1 in the claim diff
before you write code: it is the design this specification implements. Before you write
anything, read whole: `ReportSources`, `DoDCheckRow`, `NOT_RECORDED`, `build_report_sources` and
`write_final_report` in `packages/orchestration/run_report.py`; `build_diff_view` in
`packages/orchestration/diff_view_source.py`; `resolve_job_evidence_dir` in
`packages/orchestration/evidence_index.py`; `job_evidence_dir` and `job_evidence_index_dir` in
`packages/orchestration/data_paths.py`; `result_path`, `save_gate_result`, `load_gate_result` and
`GateResult` in `packages/orchestration/dod_gate.py`; `CheckEvidence` in
`packages/orchestration/dod_runners.py`; and `ALLOWED_UNWIRED` in `tests/test_no_orphan_modules.py`.
For fixtures, read how `tests/orchestration/test_job_digest.py` builds a `JobPlan` with
`TaskEntry` tasks, and reuse the real writers: `write_final_report` for `report.md`,
`save_gate_result` for `dod_result.json`, and an index record
`<job_evidence_index_dir()>/<job_id>.json` holding `{"evidence_dir_local": "<dir>"}` whose
directory holds a `workspace.diff`, so `resolve_job_evidence_dir` and `build_diff_view` read it.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f036-r1-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f036-r1/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f036-r1-dry/`, `.remedy-wt/f036-r1-sim/`  The reviewer's trees; do not touch them.
  `.remedy-wt/f036-r1-src/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f036-r1-worker/`    YOURS for logs and scripts; create it if absent. All are
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
   `git status --porcelain` must be empty, `git branch --show-current` must read `main`, and
   `git log --oneline -1` must read `9dc2f2a7`. Report all three. Then
   `git checkout -b feature/f036-guided-result-tour` and report the branch. Do NOT pull: the Open
   PR Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f036-r1/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f036-r1-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 217 | 23898 | 4fe060f8764a52b92f52da33eac333d09ea47b63cc144cf9670f6c14830e8ddc |
| context.md | 37 | 1584 | 5449d15ba2a97e113204f094c96cde87c07504e73fb3b4d9126ea9880dc2567f |
| plan.md | 29 | 1015 | 641a2a58417d49a992393a69cc39ef173df07a71cb788b219b99947dedd11167 |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`.
`claim.diff` goes on with `git apply`; the reviewer generated it with `git diff HEAD` from a tree at
`9dc2f2a7` into which it wrote the edits. It edits `.agent/live_review.md` (the re-head, which
replaces everything above the `## Findings` heading line, then F035's round 10 gate entry
appended), `docs/roadmap/STATUS.md` (F036's line `[ ]` to `[~]`, moved above F286's Tier 2
heading), `docs/roadmap/features/T2_F286.md` (one two-line note), `.agent/decisions.md`
(DECISIONS F036 D1 and D2 appended) and `.agent/operator_questions.md` (Q6 replaces `EMPTY`).

THE SPECIFICATION. No `except Exception` anywhere. `result_tour.py` imports nothing from
`pingpong_job`, `ui_server` or `apps` at module level, writes no file, calls no model, reads no
clock and changes no record.
S1 THE MODULE, a NEW FILE at `packages/orchestration/result_tour.py`. A docstring naming F036 T001 and DECISION F036 D1, with one sentence stating that
   Remedy deliberately does not write a stop whose anchor does not resolve (D1 (3)). Constants
   `TOUR_SCHEMA = "remedy.tour.v1"`, `TOUR_FILENAME = "tour.json"`, `MAX_TOUR_STOPS = 8`,
   `TOUR_TITLE_MAX_CHARS = 80`, `TOUR_BODY_MAX_CHARS = 400`,
   `TOUR_ANCHOR_KINDS = ("node", "diff", "evidence", "command")`,
   `TOUR_GENERATOR_FALLBACK = "fallback"`, `TOUR_TOP_LEVEL_AREA = "the top level"`, and
   `class ResultTourError(ValueError)`.
S2 THE CONTEXT. A frozen dataclass `TourAnchorContext` with `task_ids: tuple[str, ...]`,
   `diff_files: tuple[tuple[str, int, int], ...]` (path, added, deleted, in diff order),
   `evidence_files: tuple[str, ...]` and `run_commands: tuple[str, ...]`, each defaulting to
   `()`. `collect_tour_context(job) -> TourAnchorContext` reads: `task_ids`, `str(t.task_id)` for
   every task of `job.tasks` in order; `diff_files` from
   `build_diff_view(resolve_job_evidence_dir(job_id))["files"]`, each file's `path` and its
   `stats` `added` and `deleted`; `evidence_files`, the sorted names of the REGULAR FILES directly
   in `job_evidence_dir(job_id)` (never a directory, never a nested file), `()` when the directory
   is absent or an `OSError` stops the listing; `run_commands`, the non-empty string `command` of
   every check of `load_gate_result(job_id)` in recorded order, each command once, at its first
   occurrence, `()` when no gate was recorded.
S3 THE STOP. A stop is exactly `{"title", "body", "anchor": {"kind", "ref"}}`.
   `tour_stop_problems(stop) -> list[str]` answers one readable line per breach: not a dict;
   keys other than exactly those three; a title that is not a string, is empty after stripping,
   holds a newline or exceeds `TOUR_TITLE_MAX_CHARS`; a body that is not a string, is empty after
   stripping or exceeds `TOUR_BODY_MAX_CHARS`; an anchor that is not a dict of exactly `kind` and
   `ref`; a kind outside `TOUR_ANCHOR_KINDS`; a ref that is not a non-empty string. `[]` for a
   sound stop. `tour_problems(tour) -> list[str]` does the same for a whole tour: keys exactly
   `schema, job_id, generator, stops, dropped`; `schema == TOUR_SCHEMA`; `job_id` and
   `generator` non-empty strings; `stops` a list of at most `MAX_TOUR_STOPS` stops, each reported
   with its index and every `tour_stop_problems` line; `dropped` a list of dicts of exactly
   `title` and `reason`, both strings.
S4 THE ANCHOR. `anchor_problem(anchor, context) -> str` answers "" when the anchor resolves and
   one readable line naming the kind and the ref when it does not: `node` resolves when the ref
   is in `task_ids`; `diff` when it equals a path of `diff_files`; `evidence` when it is in
   `evidence_files`; `command` when it EQUALS, byte for byte, one of `run_commands`.
S5 THE RESOLVER. `resolve_tour_stops(stops, context) -> tuple[list[dict], list[dict]]` walks the
   stops in order. A stop with any `tour_stop_problems` line is dropped with those lines joined by
   "; " as its reason; a sound stop whose anchor does not resolve is dropped with the
   `anchor_problem` line; a sound, resolving stop after `MAX_TOUR_STOPS` have been kept is dropped
   with the reason `past the 8-stop ceiling`, built from the constant. Every drop appends
   `{"title": <the stop's title when it is a string, else "">, "reason": <reason>}` to the second
   list and logs one warning through the module's `logging.getLogger(__name__)`. A kept stop is a
   NEW dict equal to the input stop; the input is never changed.
S6 THE MECHANICAL TOUR. `fallback_tour_stops(sources: ReportSources, context) -> list[dict]` is
   pure and deterministic, and every title and body goes through one helper that returns the text
   unchanged when it fits its bound and otherwise its first `bound - 1` characters plus "…". The
   stops, in this order:
   (a) Always: title `How the run ended`; body the parts `State: <state or NOT_RECORDED>`, then
       `terminal status: <terminal_status>`, `stop reason: <stop_reason>` and
       `mission: <mission>`, each only when non-empty, joined by "; " and ended with ".". Anchor
       `evidence` `report.md` when `report.md` is in `evidence_files` or there is no task, else
       `node` with the first task id.
   (b) Areas: a diff file's area is its path's first segment when the path holds "/", else
       `TOUR_TOP_LEVEL_AREA`; areas keep the order of their first file. `room` is
       `MAX_TOUR_STOPS` minus the stops (a), (c) and (d) will add. When the areas fit in `room`,
       each area is one stop; otherwise the first `room - 1` areas are one stop each and one final
       stop gathers every remaining area. An area stop's title is `What changed in <area>/`, or
       `What changed in the top level` for `TOUR_TOP_LEVEL_AREA`; the gathering stop's title is
       `What else changed` and its body starts `<k> more areas; `. A body then reads
       `<n> changed file(s) (+<added> −<deleted>): ` followed by each file as
       `<path> (+<added> −<deleted>)` joined by ", ", with "file" for one and "files" for more
       and the totals summed over the listed files; the minus sign is U+2212. Anchor `diff` with
       the first file's path.
   (c) When `run_commands` is non-empty: title `How to run it`, body
       `The Definition of Done ran: <the FIRST command>`, anchor `command` with that command.
   (d) When `sources.dod_released is not None`: title `Definition of Done`, body
       `<passed> of <total> checks passed; the gate released the job.` (or `held`), where
       `passed` counts the `dod_checks` whose status is `passed`; when any check is not `passed`,
       the body continues ` Not passed: <check ids joined by ", ">.`. Anchor `evidence`
       `dod_result.json`, spelled from `dod_gate.DOD_RESULT_FILENAME`.
S7 THE BUILD AND THE GUARD. `build_fallback_tour(job) -> dict` answers
   `{"schema": TOUR_SCHEMA, "job_id": str(job.job_id), "generator": TOUR_GENERATOR_FALLBACK,
   "stops": <kept>, "dropped": <dropped>}` from `resolve_tour_stops(fallback_tour_stops(
   build_report_sources(job), context), context)` with `context = collect_tour_context(job)`, and
   `tour_problems` of its answer is always `[]`. `ALLOWED_UNWIRED` in
   `tests/test_no_orphan_modules.py` gains, between the `hunk_apply.py` and
   `self_use_findings.py` entries, `("packages/orchestration/result_tour.py", "F036's result
   tour, the stop shape and the mechanical tour; F036 T002 wires it at the job terminal
   (DECISION F036 D1 (6)) and removes this line")`. Nothing else in that file changes.

THE TESTS — NEW FILE at `tests/orchestration/test_result_tour.py`, `REMEDY_DATA_DIR` under
`tmp_path`, records written by the real writers. At least, one test each: a finished job with a
report, a two-area diff and a recorded passing gate yields exactly the five stops S6 states, with
exact titles, bodies and anchors; a job with no diff, no gate and no report yields only stop (a),
anchored to its first task; `report.md` present wins over the first task; a directory named
`cycles` in the evidence directory is not an evidence file; two checks with the same command give
one run command, and the FIRST recorded command is the run stop's; a held gate with a red check
reads `held` and names the check; ten areas with a run command and a gate yield exactly eight
stops, the eighth `Definition of Done`, the seventh `How to run it`, the sixth `What else changed`
naming six more areas, and nothing dropped; a mission longer than 400 characters is cut to exactly
400 ending "…" and the stop is kept; the resolver drops, each with its reason, a node ref not among
the tasks, a diff path not in the diff, an evidence name not in the directory, a command that is
a recorded one cut short by its last word, a title holding a newline, an unknown kind, a
missing key and a non-dict, and a ninth sound stop; the resolver never mutates its input and logs
one warning per drop (`caplog`); `tour_problems` accepts `build_fallback_tour`'s answer and
reports a wrong schema, nine stops and a malformed `dropped` entry; and two builds over the same
records are equal.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the state payloads
  `.agent/authored/f036-r1-block.md` := this block, and `.agent/authored/f036-r1-plan.md` and
  `.agent/authored/f036-r1-context.md` := plan.md and context.md. All by `shutil.copyfile`.
  Subject: `F036 R1 C1a: copy round 1 block and state payloads into .agent/authored/`
  Its insertions are this block's line count plus 66. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the claim diff
  `.agent/authored/f036-r1-claim.diff` := claim.diff.
  Subject: `F036 R1 C1b: copy round 1 claim diff into .agent/authored/`
  Expected insertions: 217.

C2 — THE CLAIM AND ITS RECORDS, in this order:
   1. `git apply` claim.diff
   2. rewrite `.agent/plan.md` := plan.md
   3. rewrite `.agent/context.md` := context.md
  Subject: `F036 R1 C2: claim F036, move F286 behind it, book F035 R10, record D1 and D2`
  Expected by `git show --numstat` (insertions and deletions): 15/14 context.md, 84/0
  decisions.md, 24/24 live_review.md, 20/1 operator_questions.md, 16/12 plan.md, 1/1 STATUS.md,
  2/0 T2_F286.md.

C3 — THE CODE: `packages/orchestration/result_tour.py` and the S7 line in
  `tests/test_no_orphan_modules.py`.
  Subject: `F036 R1 C3: build the result tour's stops, anchor check and mechanical tour`

C4 — THE TESTS AND THE TOOL: `tests/orchestration/test_result_tour.py` and your mutation tool
  (G5) saved as `.agent/authored/f036-r1-mutations.py`.
  Subject: `F036 R1 C4: test the result tour's anchors and mechanical stops, add the mutation tool`

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F036 R1 C5: rewrite handoff for round 1`
  Then `git push -u origin feature/f036-guided-result-tour`. Do NOT create a pull request: the
  branch opens one at F036's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C3a and C3b, C4a and C4b), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f036-r1-*` copies and tool,
   `.agent/live_review.md`, `docs/roadmap/STATUS.md`, `docs/roadmap/features/T2_F286.md`,
   `.agent/decisions.md`, `.agent/operator_questions.md`, `.agent/plan.md`, `.agent/context.md`,
   `packages/orchestration/result_tour.py`, `tests/test_no_orphan_modules.py`,
   `tests/orchestration/test_result_tour.py`, and `.agent/handoff.md`. Report the list you measure
   with `git diff --name-only 9dc2f2a7` at the branch tip after C5. Do NOT touch anything under
   `apps/`, any other file under `packages/`, `tests/orchestration/import_reachability_allowlist.txt`,
   `.agent/prose_slips.md`, `.agent/candidates.md`, `README.md` or
   `docs/roadmap/features/T5_F036.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C5, and the correction is declared. An
   EXISTING test that goes red is never edited to pass; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F036's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f036-r1-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f036-r1/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE CLAIM — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree. Report each path beside the hash you read:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2352174 | 1c33828556dcc58f6c7be33b9cdb791de25525cfa1ac0d99c04a6853fc6687d7 |
 | .agent/live_review.md | 311331 | d4d2a48d351672acb1f1d184108acd7cee772a95d6949f09eb699f9d6430cfa6 |
 | .agent/operator_questions.md | 1820 | 2298944376ed536813af18aa234850faff9dc2db07116831e7d1db0f410eaeee |
 | docs/roadmap/STATUS.md | 56261 | 8026d1f9c3a3d91dfb9838a543901455d9e5356166f77aacbc3e818ab1691805 |
 | docs/roadmap/features/T2_F286.md | 2228 | 628333757677145bfbf063cbd9ffad0f901b539987963f36615dd4f92b3e85ea |
 | .agent/plan.md | 1015 | 641a2a58417d49a992393a69cc39ef173df07a71cb788b219b99947dedd11167 |
 | .agent/context.md | 1584 | 5449d15ba2a97e113204f094c96cde87c07504e73fb3b4d9126ea9880dc2567f |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `9dc2f2a7` and at C2 (the reviewer read
 it empty at both); at C2 the ledger has exactly one line reading `## Findings` and exactly one
 reading `## Steps`, and its last non-empty line begins `Gate: F035 R10 — `; the STATUS lines
 of F036 and F286 at C2 read back in full, with their line numbers, where F036's must read
 `- [~] F036 — Guided result tour` and precede F286's; and `git diff --name-only <C1b> <C2>`,
 which must name exactly the paths of the table above.

G3 THE CODE — `python3 -m ruff check packages/orchestration/result_tour.py
 tests/orchestration/test_result_tour.py tests/test_no_orphan_modules.py` at C4, with its real
 exit code. Then report, quoted from `git show <C3>`, the whole of `anchor_problem`, the whole
 of `resolve_tour_stops`, and the area grouping and room arithmetic of `fallback_tour_stops`.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_result_tour.py tests/orchestration/test_run_report.py tests/orchestration/test_run_report_hook.py tests/orchestration/test_diff_view_source.py tests/orchestration/test_dod_gate.py tests/orchestration/test_evidence_index.py tests/orchestration/test_job_digest.py tests/orchestration/test_artifact_summaries.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/orchestration/test_event_names.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/test_agent_tooling.py tests/orchestration/test_development_artifact_boundary.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection less `tests/orchestration/test_result_tour.py`, serially, in the
 primary checkout at `9dc2f2a7` before any change, and read `874 passed, 1 skipped` at real exit
 code 0; the same selection over the reviewer's claim tree read no failure. The skip is the F252
 quarantine in `tests/test_agent_tooling.py` and stays skipped. Report every `SKIPPED` line the
 `-rs` summary prints, the node count of `tests/orchestration/test_result_tour.py` by
 `--collect-only -q`, and account for any difference from 874 plus that count. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f036-r1-mutations.py` takes a worktree path, and
 for each mutation below edits `packages/orchestration/result_tour.py` INSIDE that worktree
 (asserting its FROM text occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/orchestration/test_result_tour.py` from the worktree's root after purging its
 `__pycache__` directories, restores the bytes, and prints one line per mutation: its label, the
 exit code, the failed count and the failing node ids. It runs an unmutated control first and
 last and ends with `restored byte-identical: True` and a final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  m1 a `node` anchor resolves whatever its ref;
  m2 the resolver keeps every sound stop, with no ceiling;
  m3 a dropped stop is logged but not listed in `dropped`;
  m4 a `command` anchor resolves when a recorded command merely starts with its ref;
  m5 the context lists directories of the evidence directory as evidence files;
  m6 an area is the file's whole directory instead of its first segment;
  m7 when the areas outnumber the room, every area still gets its own stop;
  m8 stop (a) anchors to the first task even when `report.md` exists;
  m9 an over-long text is not cut;
  m10 the Definition-of-Done stop counts every check as passed;
  m11 a title holding a newline is accepted;
  m12 the run stop uses the LAST recorded command.
 Run it: `git worktree add --detach .remedy-wt/f036-r1-mut <C4>`, then
 `python3 -B .agent/authored/f036-r1-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f036-r1-mut`
 and report its whole output. The tool puts the worktree's root first on `sys.path` for its
 pytest runs, because the editable install otherwise imports the primary checkout's module.
 EVERY mutation must be red with at least one failing node; a mutation that stays green is
 reported as green, never papered over, and you then add the test that catches it in C4 before
 C5 and re-run the tool. Then `git worktree remove --force .remedy-wt/f036-r1-mut`,
 `git worktree prune`, and report `git worktree list | wc -l`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `9dc2f2a7` in that order
 (more lines if constraint 2 split a commit); `git worktree list | wc -l`, which must equal your
 step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 and C4 — report what you
measure), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Report what you ran, not what you expected to find. Your Session section reads SESSION 1
of feature F036, round 1, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 1, then T002 — the generation call with its fallback, the no-new-claims goldens, `tour.json`
stored and versioned at the job terminal, and the command line. State the open-findings count, 0,
and the operator-questions count, 1.
