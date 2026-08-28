STEP T001 read-endpoint part two — F037 R7

Goal: the diff envelope becomes reachable over HTTP. Two GET routes — one per
job, one per task run — call `build_diff_view` and return its envelope, which
finishes T001. The round also repairs `R-0715`, a stale numeral in the docstring
of the very guard this round edits.

Base: `6b778634`. Branch: `feature/f037-rendered-diff-viewer`. SESSION 2 of
feature F037, round 7, rounds so far 6.

Bundle, one commit each, in this order:
C0a  save this block verbatim to `.agent/authored/f037-r7.md`
C0b  mirror the C0a blob into `.agent/last_block.md`
C1   `.agent/plan.md` from slice PLANF037R7
C2   `.agent/live_review.md` append GATER6
C3   `packages/orchestration/ui_server.py`, the two routes, per SPEC S1 to S5
C4   `tests/ui_server/test_command_channel.py` from pairs WALKPAIR and DOCPAIR,
     and `.agent/live_review.md` append LANDED715
C5   `tests/ui_server/test_diff_endpoint.py`, new, per SPEC S6 to S12
C6   `.agent/handoff.md`, the handback

Change set — these paths and no others:
  .agent/authored/f037-r7.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  packages/orchestration/ui_server.py
  tests/ui_server/test_command_channel.py
  tests/ui_server/test_diff_endpoint.py
  .agent/handoff.md
Run `git push origin feature/f037-rendered-diff-viewer` AFTER C6. Create no pull
request and merge nothing: the Open PR Gate returned `[]` when this block was
authored.

Slice convention: the authored texts in this block are PLANF037R7, GATER6,
LANDED715, WALKPAIR and DOCPAIR. Each is delimited by a line `<<<SLICE <NAME>`
and a line `<<<END <NAME>`; the marker lines are never part of the text. A pair
slice carries a `<<<FROM` line and a `<<<TO` line inside it, which are likewise
never part of either text.

Constraints:
1. Apply every slice byte for byte, extracted from the COMMITTED C0a blob by its
   marker LINES in Python. Never retype a slice, never edit a slice.
2. `.agent/plan.md` is a WHOLE-FILE replacement by PLANF037R7.
3. WALKPAIR and DOCPAIR are FROM/TO pairs against
   `tests/ui_server/test_command_channel.py`. The containment test was run
   before emission, one reading per pair: WALKPAIR `TO contains FROM: false`,
   DOCPAIR `TO contains FROM: false`. Both are REWRITES, so each orders its FROM
   at 0x and its TO at 1x in the file after C4, and neither orders an append
   reading. Each FROM was measured at exactly ONE occurrence in that file at the
   base commit; report the count you measure before each edit.
4. WALKPAIR's FROM spans the WHOLE `paths += [...]` list literal, not a prefix
   of it, because the pair changes that structure's arity.
5. GATER6 and LANDED715 are appends at EOF of `.agent/live_review.md`, in
   different commits. The append convention is the file's existing one: a single
   separator newline, then the slice bytes.
6. No finding id is minted this round. R6 PASSED and produced no defect.
   `R-0715` is an EXISTING open finding; C4 repairs it and appends LANDED715.
   Do NOT write a `Done:` paragraph for it — only reviewer-authored text sets
   Resolved (docs/agents/planner_reviewer_prompt.md §4 item 4), and the reviewer
   writes that at the next gate.
7. Do NOT touch `packages/orchestration/diff_view_source.py` or
   `packages/orchestration/diff_parser.py`. R7 consumes both unchanged.
8. Do NOT touch the `Landed: R-0711` line or any existing `Done:` paragraph.
9. In `ui_server.py`, add NO new `path == "<literal>"` comparison. The guard
   `LITERAL_GET_ROUTES` in `tests/ui_server/test_command_channel.py` asserts the
   set of such literals by EXACT EQUALITY, measured at the base, so a new literal
   route would turn it red. Both routes below are reached without one.

SPEC — packages/orchestration/ui_server.py

S1. Add ONE key to the `handlers` dict literal inside `do_GET`:
    `"diff": _build_diff_json`. Add it to that dict and nowhere else. That dict
    is the set the guard's AST walk derives the walkable endpoints from, so this
    key enters the route walk for free — that is WHY the job scope is a dict key
    and not a structural route.

S2. `_build_diff_json(job)` — a module-level function beside the other
    `_build_*_json` builders, with their signature shape. It returns
    `build_diff_view(_resolve_evidence_dir(str(job.id)))`. It is a THIN caller:
    it contains no filesystem logic, no path building and no error handling of
    its own, because `build_diff_view` never raises and names every absence in
    its own envelope. Write the one-line WHY above it saying exactly that.

S3. `_build_task_run_diff_json(job, task_id)` — the same shape, returning
    `build_diff_view(_resolve_evidence_dir(str(job.id)), task_id=task_id)`.

S4. Add the structural route for the task-run scope, placed AFTER the
    `debug-detail` route block and BEFORE the final 404 line of `do_GET`. Match
    the shape the three `nodes/.../detail` routes already use:
    `len(parts) == 7 and parts[1] == "api" and parts[2] == "jobs" and
    parts[4] == "task-runs" and parts[6] == "diff"`, then `_load_job(parts[3])`
    with the same early return on its error, then
    `self._send_json(200, _build_task_run_diff_json(job, parts[5]))`.
    WHY a structural route rather than a dict key, written as the comment above
    it: the task-run scope needs a second path segment, and the dict dispatch is
    keyed on a single `parts[4]`. Name in that comment that this route is
    therefore spelled out in `_walkable_paths` by hand, since the AST walk has
    no literal to derive it from.

S5. Import `build_diff_view` from `packages.orchestration.diff_view_source`
    following whatever import style the neighbouring builders in that file
    already use — read them and match. `_resolve_evidence_dir` is already
    defined in `ui_server.py`; do not redefine or move it.
    An UNKNOWN task run is NOT an HTTP error: the route answers 200 and the
    envelope carries `available` False with `reason` `unknown_task_run`. Absence
    is data here, which is the whole design of `build_diff_view`, and a 404
    would make a job with no diff indistinguishable from a bad URL.

SPEC — tests/ui_server/test_diff_endpoint.py, new file

S6. Follow the harness `tests/ui_server/test_live_state.py::TestUIServerIntegration`
    uses — read it first and match it: an autouse fixture that sets
    `REMEDY_DATA_DIR` to `tmp_path`, builds and saves a job, and a
    `_start_server` helper that starts the real server on port 0 in a daemon
    thread and waits for its info file. Use `HTTPConnection` against
    `127.0.0.1` exactly as that class does. Do not import from
    `test_command_channel.py`.
S7. Point the server's evidence resolution at a tmp directory by writing
    `<REMEDY_DATA_DIR>/job_evidence_index/<job_id>.json` holding
    `{"evidence_dir_local": "<the tmp evidence dir>"}` — that is the first
    branch `_resolve_evidence_dir` reads, and it keeps the test independent of
    the working directory. Build the evidence dir with a `workspace.diff` and a
    `task_runs/T001/safe.diff` whose diffs name DIFFERENT file paths, so serving
    one where the other was asked for is a red.
S8. The job route: `GET /api/jobs/<job_id>/diff?token=<token>` answers 200, and
    the body has `scope` `job`, `available` True, `source` `workspace.diff` and
    `files` naming the job diff's path.
S9. The task-run route: `GET /api/jobs/<job_id>/task-runs/T001/diff?token=`
    answers 200 with `scope` `task_run`, `task_id` `T001`, `available` True and
    `files` naming ONLY the task diff's path.
S10. The unknown run: `.../task-runs/T404/diff` answers 200 with `available`
     False, `reason` `unknown_task_run` and `task_run_ids` holding `T001`.
     Assert the STATUS is 200 explicitly, since that is the design decision S5
     names and a later change to 404 must be a red.
S11. Both routes refuse a bad token with 403 — one test per route.
S12. A job whose evidence index is absent: the job route answers 200 with
     `available` False and `reason` `evidence_dir_unavailable`.

Done when — eight gates. Run every one, record its REAL exit code and its
verbatim summary line, and put one line per gate in the handback.

G1 hygiene. Read `.agent/STOP` from disk before C0a and again before C6; report
   ABSENT or PRESENT at both points, and if PRESENT stop after the current
   commit and hand off. Report `git rev-parse HEAD` before C0a — it must equal
   the base above — and `git branch --show-current`. Report the
   `git status --porcelain` LINE COUNT after each of C0a, C0b, C1, C2, C3, C4
   and C5; each must be 0.

G2 transport, ONE digest comparison. After C0a report the sha256, byte count and
   line count of `.agent/authored/f037-r7.md`. After C0b report that
   `git rev-parse HEAD:.agent/authored/f037-r7.md` and
   `git rev-parse HEAD:.agent/last_block.md` are the SAME blob hash. State
   plainly that this chain covers the saved copy, its mirror and the working
   copy, and claims nothing about the bytes of any prompt.

G3 extraction and caps. Extract every slice from the COMMITTED C0a blob by its
   marker lines and print each slice's NAME and line count. Print TOTAL (the
   block's lines), CONTENT (the sum of the slice line counts) and
   PROSE = TOTAL − CONTENT, all as measured. PROSE must be at most 400 and TOTAL
   at most 490.

G4 the plan at C1. `.agent/plan.md` byte-equal to PLANF037R7 under the
   newline-included convention: report True or False. Report the NEGATIVE
   CONTROL against the slice minus its trailing newline; it must be False.
   Report `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` strictly under 50.

G5 the record, full byte forensics — this is the append into the record.
   At C2, appending GATER6: the base `.agent/live_review.md` is 1162114 bytes;
   report the measured value beside it, then report that the post-append length
   equals base + 1 + the GATER6 byte length and that the base is a byte PREFIX
   of the result. Reader (b), independent and structural: have your script COUNT
   N, the number of blank-line units in GATER6, and compare the LAST N units of
   the file against the slice's N units IN ORDER. NEGATIVE CONTROL: flip one
   byte inside the FIRST appended paragraph and report that reader (a) and
   reader (b) BOTH come back False.
   At C4, appending LANDED715: the same two readers and the same control against
   the length measured after C2.
   COUNTS after C4, line-anchored, each reported as measured:
     `^- R-\d+ — ` 279, unchanged — no id is minted this round
     `^Done: R-\d+ — ` 27, unchanged — the reviewer writes R-0715's at the next gate
     `^Landed: R-` 2 — the surviving `R-0711` line plus LANDED715
     `^Gate: F\d+ R\d+ — ` 77
   Report the size of the open set, which is every registered id minus every
   resolved id, and confirm `R-0715` is still in it.

G6 the red-proofs for the two routes, run ONLY inside a disposable
   `git worktree` at the C5 tree and never in the primary checkout. Purge
   `__pycache__` and use `python3 -B` before EVERY run, and restore the file
   between mutations. Report the UNMUTATED CONTROL first —
   `python3 -B -m pytest tests/ui_server/test_diff_endpoint.py -q` — with its
   real exit code and verbatim summary; a colour with no baseline is not
   evidence. Then three mutations, each described BY PROPERTY because you wrote
   the code, and for each one quote the exact lines you changed FROM and TO, the
   count of that string's occurrences before the edit, the real exit code, the
   verbatim summary and every failing node id in full:
     (a) remove the `"diff"` key from the `handlers` dict, so the job route
         falls through to the 404.
     (b) make the structural route ignore `parts[5]` and pass `task_id=None`,
         so the task-run route serves the JOB diff.
     (c) make the unknown-task-run case answer 404 instead of 200 with the
         named absence.
   Additionally, and in the SAME worktree, run
   `python3 -B -m pytest tests/ui_server/test_command_channel.py -q` UNMUTATED
   and report its real exit code and verbatim summary, because C4 edits that
   file and the route walk is the guard this round is required not to break.
   If any mutation comes back GREEN, report the green plainly and diagnose WHY
   the mutated branch is unreachable by the tests. Do NOT substitute a different
   mutation and do NOT add a test to make it red. Remove and prune the worktree
   afterwards and report `git worktree list` line count and
   `git status --porcelain` line count in the primary checkout.

G7 suite, lint and canary at C5, in the primary checkout, ONE pytest process at
   a time and never two in parallel.
   Run `python3 -m pytest tests/ui_server/test_diff_endpoint.py
   tests/ui_server/test_command_channel.py tests/orchestration/test_diff_view_source.py -q`;
   report the real exit code, the verbatim summary line and the count of lines
   matching `^FAILED`. Add the extractor-blindness control: run the SAME counter
   over a control string containing
   `FAILED tests/ui_server/test_diff_endpoint.py::test_control_string` and report
   that it returns 1, so a 0 above is a measurement and not a blind spot.
   `tests/ui_server/test_command_channel.py` was measured GREEN at the base
   commit at `106 passed`; report the count you measure and, if it differs,
   report the difference rather than explaining it away.
   Report the node-id inventory of the new file from
   `python3 -m pytest tests/ui_server/test_diff_endpoint.py --collect-only -q` —
   the count and the ids. Never derive node ids by regexing `-v` output.
   Run `python3 -m ruff check packages/orchestration/ui_server.py
   tests/ui_server/test_diff_endpoint.py tests/ui_server/test_command_channel.py`
   with the repository's own configuration and NO `--isolated`; report the real
   exit code and the verbatim output.
   Run the canary `python3 -m pytest tests/cli/test_golden_path.py -q`; report
   the real exit code and the verbatim summary.

G8 structure, artifacts and the Open PR Gate, measured at C5.
   Report `git diff --name-only <base>..<C5>` against the change set above minus
   `.agent/handoff.md`, and report BOTH residues — actual minus expected and
   expected minus actual — each of which must be empty.
   Report a restricted `git diff --stat`: `apps/` empty, `docs/` empty,
   `packages/` holding only `ui_server.py`, `tests/` holding only
   `test_command_channel.py` and `test_diff_endpoint.py`.
   Report the per-commit INSERTION count from `git diff --numstat` for C0a, C0b,
   C1, C2, C3, C4 and C5 — not for C6, whose own count cannot exist while its
   text is being written — and confirm each commit is single-parent and each
   insertion count is under 500.
   Report the line-anchored counts of `^<<<SLICE ` and `^<<<END ` in
   `.agent/plan.md` at C1 and `.agent/live_review.md` at C4; both must be 0.
   Then run the SAME counter over the C0a blob and report the number it
   measures, which must be greater than zero, so the sweep is shown not to be
   blind.
   Report the count of the string `thirteen` in
   `tests/ui_server/test_command_channel.py` after C4, which must be 0 — that is
   `R-0715`'s repair, and the counter-measure the finding names is DELETING the
   numeral rather than updating it, so a count of 1 for any other numeral word
   is equally a failure to repair it.
   Report `git ls-files .remedy-wt` line count, which must be 0.
   Report the Open PR Gate verbatim:
   `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.
   The PUSH is ordered after C6 and is deliberately NOT part of any gate: C6
   writes the handback, so the handback cannot report a value that does not
   exist when it is written. Run the push, and do not name its result in
   `.agent/handoff.md`; the reviewer reads the remote tip itself.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It
carries the Session block naming SESSION 2 of feature F037 and round 7, the
range and base SHA, a per-commit changed-files table with a `+/-` column taken
from `git diff --numstat` itself and agreeing cell for cell with the per-commit
reading G8 orders, the external actions, one line per gate G1 through G8 with
its real result, the item-status table covering every C-item, every S-item and
every gate with `done`, `skipped` or `deviated` plus a reason, the Deviations,
and the Next section. It has NO length cap. State in the Next section that the
first action of the next round is to re-read `.agent/STOP` from disk, then the
Open PR Gate, and that T001 is complete with T002 next.

<<<SLICE PLANF037R7
# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495`, the
merge commit of pull request #217 which closed F032.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F037 D1 and D2.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the design amendments that reconcile it with the source.

## Current Step
R7 finishes T001 by making the resolver reachable over HTTP: a job-scope route
as a key in the `do_GET` handlers dict, which enters the route walk for free,
and a task-run-scope route spelled out structurally because it needs a second
path segment. An unknown task run answers 200 with a named absence rather than
404, because absence is data in this envelope. The round also repairs `R-0715`,
a stale numeral in the docstring of the very route-walk guard it edits, by
deleting the numeral as that finding's counter-measure requires.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R6 gate | ordered | record first |
| C3 the two routes | ordered | no new literal route |
| C4 the walk registration and `R-0715` | ordered | the guard must see the new route |
| C5 the endpoint tests | ordered | |
| C6 the handback | ordered | |

## Next Steps
1. T002 the rendering core: lines, intraline emphasis, hunk heads and collapse,
   against the binding CSS in `docs/roadmap/features/T5_F037.md`, with goldens
   per fixture shape.
2. T003 sidebar, virtual scrolling, lazy language bundles, the 10k-line perf
   fixture and the L3 evidence-panel tab.
3. The integration-gate round before closure, then the closure sequence.

## Risks
- `R-0711` carries a `Landed:` line and no `Done:` text because F032's branch
  ended first. It is the terminator case, not a gap for F037 to close.
- The endpoint tests start a real server on a free port. Run the suites
  serially: two pytest processes at once produce false reds in this directory.
- T002 is the first UI work of this feature, so the design reference in
  `docs/ui/design_reference/` becomes binding from the next round on.
<<<END PLANF037R7

<<<SLICE GATER6
Gate: F037 R6 — the resolver round, and the first round of session 2. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran the load-bearing ones itself at `6b778634`. THE ROUND HAD NO DEVIATIONS AT ALL, which is worth recording because the two numerals the block deliberately put at risk both landed on measurement: `^Landed: R-` reads 1, the value that follows from `R-0711` surviving as constraint 6 required, and `.agent/prose_slips.md` measured 6840 bytes at the base, exactly the figure the block named for it. THE NEW MODULE IS REAL AND THE REVIEWER EXERCISED IT RATHER THAN READING ONLY ITS TESTS: `packages/orchestration/diff_view_source.py` resolves an evidence directory, and optionally one task run, to the contract-v1 envelope, importing `DIFF_VIEW_VERSION` from the parser rather than declaring a second version literal. The scoped suite `python3 -m pytest tests/orchestration/test_diff_view_source.py tests/orchestration/test_diff_parser.py -q` is exit 0 at `37 passed`, `python3 -m ruff check` over both new paths under the repository's own configuration is exit 0 at `All checks passed!`, and the canary is exit 0 at `42 passed`. THE REVIEWER ADDITIONALLY RAN A GUARD THE BLOCK NAMED AS A CONSTRAINT BUT NO GATE COVERED: `tests/test_no_interactive_guard.py`, which sweeps every file under `packages/orchestration` against an EMPTY allowlist and therefore acquired the new module, is exit 0 at `6 passed`. BOTH RED-PROOFS REPRODUCE EXACTLY AS REPORTED, run by the reviewer in a disposable worktree with `__pycache__` purged before every run and the module restored between them, each mutated string counted at exactly one occurrence before its edit: unmutated control exit 0 at `9 passed`; defeating the task-run membership check is exit 1 at `2 failed, 7 passed`, killing both `test_unknown_task_run_is_refused_and_reports_the_real_runs` and `test_traversal_task_ids_are_refused_without_reading_anything`; and making the missing-artifact branch report `available` True is exit 1 at `1 failed, 8 passed`, killing `test_missing_job_artifact_still_names_the_path_it_looked_for`. THE REFUSAL DESIGN IS THE ROUND'S BEST DECISION AND IT IS PROVED RATHER THAN ASSERTED: a task id is accepted only by MEMBERSHIP in the real listing of `task_runs/`, never by a pattern match over the argument, so traversal is refused by construction; and the test plants a marker file outside the evidence directory and asserts that marker reaches no field of any returned envelope, which pins that nothing was READ rather than merely that a field was set. THE RECORD MOVED AS ORDERED AND ONLY AS ORDERED: `^- R-\d+ — ` unmoved at 279 with every id distinct, `^Done: R-\d+ — ` 25 to 27, `^Landed: R-` 3 to 1, `^Gate: F\d+ R\d+ — ` 75 to 76, no id added, exactly `R-0717` and `R-0718` newly resolved, and the open set 254 to 252. TWO DECLARED ASSUMPTIONS ARE BOTH SOUND: typing `evidence_dir` as `Path | None` where the spec gave no annotation, and folding "not a file" and "does not decode" into one absence flag, which is what makes the second red-proof a single-site edit rather than two. ONE THING IS TRUE OF THE ROUND AND MUST NOT BE MISREAD AS A DEFECT: `build_diff_view` has no caller anywhere in the tree, because the block forbade touching `ui_server.py` until the route-walk guard had been measured. That is the split the plan ordered, and F037 R7 is the round that closes it. NO BLOCK CONDITION AROSE: nothing fabricated, no false live indicator, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END GATER6

<<<SLICE LANDED715
Landed: R-0715 — the docstring of `_do_get_route_facts` in `tests/ui_server/test_command_channel.py` no longer counts the job endpoints: "The thirteen job endpoints live in a dict literal inside `do_GET`" is now "The job endpoints live in a dict literal inside `do_GET`", which is the delete-the-numeral counter-measure the finding names rather than an update to fifteen, and the clause that carries the real property — that adding one puts it in the walk for free — is unchanged. The same commit adds the task-run diff route to `_walkable_paths`, so the route this round introduces is walked by the 405 discipline. In commit C4 of F037 R7.
<<<END LANDED715

<<<SLICE WALKPAIR
<<<FROM
        paths += [
            f"/api/jobs/{self.job_id}/events-since",
            f"/api/jobs/{self.job_id}/events/stream",
            f"/api/jobs/{self.job_id}/nodes/node-1/detail",
            f"/api/jobs/{self.job_id}/nodes/node-1/human-detail",
            f"/api/jobs/{self.job_id}/nodes/node-1/debug-detail",
        ]
<<<TO
        paths += [
            f"/api/jobs/{self.job_id}/events-since",
            f"/api/jobs/{self.job_id}/events/stream",
            f"/api/jobs/{self.job_id}/nodes/node-1/detail",
            f"/api/jobs/{self.job_id}/nodes/node-1/human-detail",
            f"/api/jobs/{self.job_id}/nodes/node-1/debug-detail",
            f"/api/jobs/{self.job_id}/task-runs/T001/diff",
        ]
<<<END WALKPAIR

<<<SLICE DOCPAIR
<<<FROM
        Derived rather than transcribed: a walk over a hand-written list proves
        that list, not the server. The thirteen job endpoints live in a dict
        literal inside `do_GET`, so adding one puts it in the walk for free.
<<<TO
        Derived rather than transcribed: a walk over a hand-written list proves
        that list, not the server. The job endpoints live in a dict literal
        inside `do_GET`, so adding one puts it in the walk for free.
<<<END DOCPAIR
