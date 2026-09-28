STEP F036 R4 — T003'S FIRST HALF: the `tour` route over one shared view, the browser's pure tour module and its loader, and the repair of R-1087

GOAL
Round 3 passed with one Low finding. Book its verdict, register R-1087 and record DECISION F036
D5, then add `tour_view(job)` to `packages/orchestration/result_tour.py` and serve it at
`GET /api/jobs/<job_id>/tour`, rebuild the command line's `tour` section on it, repair R-1087 in
the claim check, and add the browser's side: a pure module `apps/ui/src/api/resultTour.ts`, a
never-throwing `loadTourView` in `apps/ui/src/api/remedyApi.ts`, their vitest file and a contract
test. No component, shell, CSS, event name or report content changes this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against S1 to S6 below. Only the `.agent/` records travel as
payloads. Read DECISION F036 D5 and finding R-1087 in the booking diff before you write code.
Before you write anything, read whole: `packages/orchestration/result_tour.py` as round 3 left
it; `_build_ownership_json`, `_build_lessons_json`, `_load_job` and the `handlers` dict of
`_RemedyHandler.do_GET` in `packages/orchestration/ui_server.py`; `_tour_section` in
`apps/cli/commands/job.py`; `tests/ui_server/test_ownership_route.py`,
`tests/ui_server/test_handler_table_walk.py` and `_walkable_paths` in
`tests/ui_server/test_command_channel.py`; `apps/ui/src/api/ownership.ts` and
`apps/ui/src/api/ownership.test.ts`; `fetchJson`, `ownershipViewPath`'s use and
`loadOwnershipView` in `apps/ui/src/api/remedyApi.ts`;
`tests/ui_contracts/test_ownership_view_contract.py` and `strip_ts_comments` in
`tests/ui_contracts/test_brain_stream_ring.py`; and `.agent/authored/f035-r5-mutations.py`, whose
vitest route your tool reuses.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f036-r4-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f036-r4/`           READ-ONLY. The reviewer's block.
  Every other `.remedy-wt/f036-r*` directory and `.remedy-wt/f036-review/`  The reviewer's; do
                                  not touch them.
  `.remedy-wt/f036-r4-worker/`    YOURS for logs, scripts and the vitest scratch config and
                                  cache; create it if absent. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Set `REMEDY_DATA_DIR` inside tests with `monkeypatch.setenv`, never on a command line, and
never call `monkeypatch.undo()` in a test whose fixtures isolate the data root through the same
`monkeypatch`. Never run npm or npx; vitest, tsc and eslint run through the pytest wrappers G4
names, and your tool runs the primary checkout's own `apps/ui/node_modules/.bin/vitest` binary.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f036-guided-result-tour`, and `git log --oneline -1` must read `09782a43`. Report
   all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f036-r4/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f036-r4-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| booking.diff | 58 | 13496 | 53ce68fc4cbea645eba7c84652de075490cc20868a94bf7e98c9347c341a6f98 |
| plan.md | 28 | 960 | 02058c3525a3779798d8fa16cfc2d55725c11ba2ff6466b55e2f4c33fe4cb288 |

`plan.md` is a REWRITE of `.agent/plan.md`. `booking.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `09782a43`. It appends round 3's gate entry and
the registration of R-1087 to `.agent/live_review.md`, and DECISION F036 D5 to
`.agent/decisions.md`.

THE SPECIFICATION. No `except Exception` anywhere, and no new `# noqa: BLE001`.
S1 THE VIEW, in `result_tour.py`. `TOUR_VIEW_KEYS = ("stored", "version", "tour", "error")` and
   `tour_view(job) -> dict` answering exactly those keys: the latest stored tour with `stored`
   true, its version and `error` ""; with nothing stored, `build_fallback_tour(job)` with
   `stored` false, `version` 0 and `error` ""; and when `load_result_tour` raises
   `ResultTourError`, `build_fallback_tour(job)` with `stored` false, `version` 0 and `error` the
   exception's message. It writes nothing.
S2 THE ROUTE AND THE SECTION. `_build_tour_json(job)` in `ui_server.py` returns `tour_view(job)`,
   imported in its body the way `_build_ownership_json` imports its view, and the `handlers` dict
   gains `"tour": _build_tour_json` after `"lessons"`. `_tour_section` in
   `apps/cli/commands/job.py` builds from `tour_view(job)`: a non-empty `error` raises
   `ShowSectionError("tour_unreadable", <the error>)`, and otherwise its data is
   `{"stored", "version", "tour"}` from the view and its lines `render_tour_lines(tour)`, so its
   behaviour is round 3's.
S3 R-1087. `_TOUR_PATH_TOKEN_RE`'s slashed-path half becomes `(?:[\w.-]+/)+[\w.-]*\w`, its
   file-name half unchanged. `tests/orchestration/fixtures/result_tour/golden_generated.json`
   is rewritten from the code in the same commit, and only its one path reason changes.
S4 THE PURE MODULE, NEW FILE at `apps/ui/src/api/resultTour.ts`, with a header comment naming
   F036 T003 and DECISION F036 D5 and stating that it opens no socket, reads no clock and keeps no
   storage. It exports: interfaces `TourAnchor` (`kind`, `ref`), `TourStop` (`title`, `body`,
   `anchor`), `TourDrop` (`title`, `reason`), `ResultTour` (`schema`, `jobId`, `generator`,
   `stops`, `dropped`) and `TourView` (`stored`, `version`, `tour`, `error`);
   `TOUR_ANCHOR_KINDS`, the four kinds in round 1's order; `MAX_TOUR_STOPS = 8`;
   `decodeTourView(raw: unknown): TourView | null`, reading the payload as `payload["…"]`, the
   tour as `tour["…"]`, each stop as `stop["…"]`, each anchor as `anchor["…"]` and each dropped
   entry as `drop["…"]`, and answering `null` — the whole view refused — when any value has the
   wrong type, `version` is not a whole number of 0 or more, the schema is not
   `remedy.tour.v1`, an anchor's kind is not one of `TOUR_ANCHOR_KINDS`, an anchor's ref is empty,
   or the stops number more than `MAX_TOUR_STOPS`; `tourViewPath({jobId, token, baseUrl?})`,
   built exactly as `ownershipViewPath` builds its path, with `tour` as the last segment;
   `TOUR_UNREADABLE_LINE` = `This job's tour could not be read.` and `TOUR_EMPTY_LINE` =
   `This job's tour has no stops.`; `tourPanelState(view, loaded)` answering
   `{kind: "loading"}` before loading, `{kind: "unreadable", line: TOUR_UNREADABLE_LINE}` for a
   `null` view, `{kind: "empty", line: TOUR_EMPTY_LINE}` for no stops, and
   `{kind: "stops", stops}` otherwise; `tourNeighbours(count, current)` answering
   `{previous, next}`, each an index or `null` past the ends; `tourStepLabel(count, current)`
   answering `Stop <current + 1> of <count>`; `tourProgress(count, current)` answering one of
   `"done"`, `"current"` or `"ahead"` per stop; and `tourAnchorLabel(anchor)` answering
   `Task <ref>`, `Changed file <ref>`, `Evidence file <ref>` or `Command <ref>` by kind.
S5 THE LOADER, in `remedyApi.ts`, shaped like the ownership door: `export type TourFetcher =
   (path: string) => Promise<unknown>;` and `loadTourView(request, fetchPayload: TourFetcher =
   fetchJson): Promise<TourView | null>`, which answers `decodeTourView` of the payload read at
   `tourViewPath(request)` and `null` — never a throw — for a failed read or a refused payload.
S6 THE CONTRACT, NEW FILE at `tests/ui_contracts/test_tour_view_contract.py`, reading
   `resultTour.ts` through `strip_ts_comments`: the `payload["…"]` keys equal `TOUR_VIEW_KEYS`;
   the `tour["…"]` keys equal the tour's keys in `result_tour.py`; the `stop["…"]`, `anchor["…"]`
   and `drop["…"]` keys equal the stop's, the anchor's and the dropped entry's; the kinds in
   `TOUR_ANCHOR_KINDS` equal `TOUR_ANCHOR_KINDS` of `result_tour.py` in order; the module holds
   none of `fetch(`, `Date.now`, `new Date` and `localStorage`; and `remedyApi.ts`'s
   `loadTourView` reads through `tourViewPath` and `decodeTourView`.

THE TESTS. `tests/orchestration/test_result_tour.py` gains, at least: `tour_view` for a stored
tour, for none stored and for an unreadable stored one, each with exactly `TOUR_VIEW_KEYS`; a
model stop naming the invented path `docs/my-guide/intro.v2.md` is dropped with a reason naming
that whole path; and a model stop whose body ends with a recorded path and a full stop is kept.
NEW FILE at `tests/ui_server/test_tour_route.py`, shaped like `test_ownership_route.py` on a real
server on port 0: the body equals `tour_view(job)` for a job with a stored tour and for one with
none; an unreadable stored tour answers 200 with its `error`; an unknown job 404; the neighbour
`/tours` answers not found; a wrong token 403. NEW FILE at `apps/ui/src/api/resultTour.test.ts`:
the decoder accepts a served view and refuses each of a wrong schema, an unknown anchor kind, an
empty ref, nine stops, a negative or fractional version and a missing dropped entry key; the path
encodes both values; each panel state; the neighbours at both ends; the step label; the progress;
each anchor label; and `loadTourView` through an injected fetcher, answering `null` without a
throw when the fetcher rejects.

BUNDLE — the commits are C1, C2, C3, C4, C5 and C6, in this order.

C1 — copy this block and the payloads
  `.agent/authored/f036-r4-block.md` := this block, `.agent/authored/f036-r4-booking.diff` :=
  booking.diff and `.agent/authored/f036-r4-plan.md` := plan.md, by `shutil.copyfile`.
  Subject: `F036 R4 C1: copy round 4 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 86. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C2 — THE BOOKING, the round's first substantive commit: `git apply` booking.diff, then rewrite
  `.agent/plan.md` := plan.md.
  Subject: `F036 R4 C2: book round 3, register R-1087, record DECISION F036 D5`
  Expected by `git show --numstat`: 38/0 decisions.md, 4/0 live_review.md, 7/7 plan.md.

C3 — THE PYTHON: `packages/orchestration/result_tour.py`, `packages/orchestration/ui_server.py`,
  `apps/cli/commands/job.py`, and the regenerated golden.
  Subject: `F036 R4 C3: serve one tour view to the browser and the command line, repair R-1087`

C4 — THE BROWSER MODULE: `apps/ui/src/api/resultTour.ts` and `apps/ui/src/api/remedyApi.ts`.
  Subject: `F036 R4 C4: decode the tour view in the browser and load it without a throw`

C5 — THE TESTS AND THE TOOL: the tests of THE TESTS, `tests/ui_contracts/test_tour_view_contract.py`,
  and your mutation tool (G5) saved as `.agent/authored/f036-r4-mutations.py`; split into C5a
  and C5b under constraint 2 if needed.
  Subject: `F036 R4 C5: test the tour route, the browser module and R-1087, add the mutation tool`

C6 — THE HANDBACK: `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`, and ONE
  line appended to `.agent/live_review.md`, preceded by a blank line: `Landed: R-1087 — <one
  sentence: what changed, naming C3's short SHA>`. Nothing else in the ledger changes.
  Subject: `F036 R4 C6: rewrite handoff for round 4, mark R-1087 landed`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects, and say so.
3. The round's whole tracked path set is: the `.agent/authored/f036-r4-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the files C3, C4 and C5
   name, and `.agent/handoff.md`. Report the list you measure with `git diff --name-only 09782a43`
   at the branch tip after C6. Do NOT touch any other file under `apps/`, `packages/` or
   `tests/`, `.agent/context.md`, `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md`, `README.md` or anything under `docs/`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C6, and the correction is declared. An
   EXISTING test that goes red is never edited to pass, except the golden S3 orders rewritten;
   report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F036's belongs to its closure. No test may reach a live model.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C6 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f036-r4-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f036-r4/block.md`), read back with
 `git show <C1>:<path>`. Report one reading per copy.

G2 THE BOOKING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree. Report each path beside the hash you read:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2364324 | bb8dd2356464c2b92517898203a0bdc1d3b5d8861b8f8001f8ed72100d1d7661 |
 | .agent/live_review.md | 320834 | d702ff0c0a19abb03bf0db696afca3cc8370be6ad39f14c21b292d69cb8cd203 |
 | .agent/plan.md | 960 | 02058c3525a3779798d8fa16cfc2d55725c11ba2ff6466b55e2f4c33fe4cb288 |
 Also: `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's TEXT at C2,
 which the reviewer read as `['R-1087']`; `latest_gate_verdict` of the same text, which the
 reviewer read as `PASS`; and `git diff --name-only <C1> <C2>` names exactly the paths above.

G3 THE CODE — `python3 -m ruff check packages/orchestration/result_tour.py
 packages/orchestration/ui_server.py apps/cli/commands/job.py tests/orchestration/test_result_tour.py
 tests/ui_server/test_tour_route.py tests/ui_contracts/test_tour_view_contract.py` at C5, with its
 real exit code. Then report, quoted from the commits that wrote them, the whole of `tour_view`,
 `_build_tour_json`, the new `_tour_section`, the new `_TOUR_PATH_TOKEN_RE`, `decodeTourView`
 and `loadTourView`.

G4 THE TESTS — in the primary checkout at C5, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_result_tour.py tests/cli/test_job_show.py tests/ui_server/test_tour_route.py tests/ui_server/test_handler_table_walk.py tests/ui_server/test_command_channel.py tests/ui_server/test_ownership_route.py tests/ui_contracts tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/regression/test_resource_safety.py tests/test_agent_tooling.py tests/orchestration/test_development_artifact_boundary.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -8; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection less `tests/ui_server/test_tour_route.py`, serially, in the
 primary checkout at `09782a43` before any change, and read `1758 passed, 5 skipped` at real exit
 code 0. The skips are four F252 quarantines in `tests/ui_contracts/` and the one in
 `tests/test_agent_tooling.py`, and they stay skipped. This selection runs vitest
 (`test_vitest_passes`), `tsc --noEmit` (`test_typescript_compiles`) and eslint
 (`tests/ui_contracts/test_ui_lint.py`) over the whole of `apps/ui`. Report every `SKIPPED` line
 and the node count of each test file this round added or grew, and account for any difference
 from 1758. Then `python3 -m apps.cli.main integrity check --json`, which must read all six
 checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f036-r4-mutations.py` takes a worktree path and has
 two runners, modelled on `.agent/authored/f035-r5-mutations.py`: PYTHON runs `python3 -B -m
 pytest -q -p no:cacheprovider tests/orchestration/test_result_tour.py tests/ui_server/test_tour_route.py
 tests/cli/test_job_show.py` from the worktree's root with that root first on `sys.path`, after
 purging its `__pycache__` directories; VITEST runs the primary's `apps/ui/node_modules/.bin/vitest`
 from the primary's `apps/ui` against a plain-object scratch config under your own directory whose
 `root` is the primary's `apps/ui`, whose `cacheDir` is under your directory, whose
 `test.environment` is `"node"` and whose `test.include` is the WORKTREE's
 `apps/ui/src/api/resultTour.test.ts` by absolute path, with a JSON reporter it reads for the
 failed count. For each mutation below the tool edits the named file INSIDE the worktree
 (asserting its FROM text occurs exactly once), runs the named runner, restores the bytes, and
 prints one line: its label, the exit code, the failed count and the failing node ids. It runs an
 unmutated control of EACH runner first and last and ends with `restored byte-identical: True` and
 a final line `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  m1 PYTHON (`result_tour.py`) `tour_view` reads `stored` true when none is stored;
  m2 PYTHON (`result_tour.py`) `tour_view` lets a `ResultTourError` propagate;
  m3 PYTHON (`result_tour.py`) the slashed-path half is round 3's `\w+(?:/\w+)+` again;
  m4 PYTHON (`result_tour.py`) the slashed-path half no longer has to end at a word character;
  m5 PYTHON (`ui_server.py`) the `tour` entry of `handlers` serves the ownership view;
  m6 VITEST (`resultTour.ts`) the decoder accepts more than `MAX_TOUR_STOPS` stops;
  m7 VITEST (`resultTour.ts`) the decoder accepts an anchor kind outside `TOUR_ANCHOR_KINDS`;
  m8 VITEST (`resultTour.ts`) `tourNeighbours` answers a `next` at the last stop;
  m9 VITEST (`resultTour.ts`) `tourPanelState` answers `stops` for a tour with none;
  m10 VITEST (`remedyApi.ts`) `loadTourView` lets a rejected fetch throw.
 Run it: `git worktree add --detach .remedy-wt/f036-r4-mut <C5>`, then
 `python3 -B .agent/authored/f036-r4-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f036-r4-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a
 mutation that stays green is reported as green, never papered over, and you then add the test
 that catches it in C5 before C6 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f036-r4-mut`, `git worktree prune`, report
 `git worktree list | wc -l`, and report `git status --porcelain`, which must be empty.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C6, C5, C4, C3, C2, C1 and `09782a43` in that order
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
of feature F036, round 4, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 4, then T003's second half — the overlay with its spotlight, stepping and navigation to each
anchor, its place in the shell, and a headless render. State the open-findings count, 1 (R-1087,
landed and awaiting the reviewer's resolution), and the operator-questions count, 1.
