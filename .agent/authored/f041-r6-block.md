STEP F041 R6 — R-1106, THE TOUR'S PREVIEW ANCHOR AND THE END-TO-END RUN: book round 5, register R-1106 and record D6, then repair R-1106, give the guided tour a "See it running" stop on both sides, and prove the preview flow on a real small app through a real UI server

GOAL
Round 5 passed at `fd124cc9` with one Low finding, R-1106. Book the gate entry and the
registration and record DECISION F041 D6 in one commit, then land D6: R-1106's repair in
`readmeCockpitHtml`; a `preview` anchor in `packages/orchestration/result_tour.py` and
`apps/ui/src/api/resultTour.ts`, with its stop, its prompt line and the shell's "Show me"; and the
end-to-end test `tests/ui_server/test_preview_end_to_end.py`. This is F041's last building round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code, its tests and the mutation tool yourself against S1 to S4. Only the `.agent/`
records travel as payloads. Read DECISION F041 D6 and finding R-1106 in records.diff before you
write code. Before you write anything, read whole: `apps/ui/src/api/artifactPreview.ts` and its
test; `packages/orchestration/result_tour.py` and `tests/orchestration/test_result_tour.py`;
`resolve_spec` and `RuntimeConfigError` in `packages/runtimes/runtime_config.py`;
`apps/ui/src/api/resultTour.ts` and `resultTour.test.ts`; `components/tour/TourOverlay.tsx`;
`components/shell/RemedyShell.tsx`; `tests/ui_contracts/test_tour_view_contract.py` and
`test_artifact_preview.py`; `tests/ui_server/test_tour_e2e_live.py` for `_start_server`;
`tests/ui_server/test_preview_commands.py`; `tests/runtimes/test_runtime_cli_process_boundary.py`
and `tests/runtimes/runtime_cleanup.py`; `tests/ports.py`; `packages/orchestration/preview_control.py`,
`preview_worker.py` and `preview_runner.py`; `start_ui_server` and `_build_preview_json` in
`packages/orchestration/ui_server.py`; how `remedy runtime status` finds a folder's runtime
record in `apps/cli/commands/runtime_cmd.py`; and your round 5 tool `.agent/authored/f041-r5-mutations.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f041-r6-payloads/`, `.remedy-wt/f041-r6/`, `.remedy-wt/f041-r6-dry/`  READ-ONLY:
                                  the reviewer's payloads, block, scripts and tree.
  `.remedy-wt/f041-r6-worker/`    YOURS for logs and scripts; create it if absent. Gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe.
Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Never run npm or npx: run the primary's own binaries under `apps/ui/node_modules/.bin/`.
Stop a process only by its own recorded pid, never with `pkill -f`. Never `git reset` a commit.
Every comment and docstring you write names a command only as a whole real command, never with a
placeholder in place of a word (`tests/cli/test_advertised_commands.py` refuses such a line).

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f041-artifact-preview`, and `git log --oneline -1` must read `fd124cc9b`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f041-r6/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f041-r6-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 30 | 13790 | 47a62d052dfdc2b54d34290e9ee2036c1fb7007d146204386bc1a368c931983e |
| plan.md | 27 | 926 | f75b5bc5d721c87cc25f6ad73e369823cf47343847e2b59ab7bc5639911e48a1 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `fd124cc9b`. It appends to `.agent/live_review.md`
round 5's gate entry and the registration of R-1106, and to `.agent/decisions.md` DECISION F041 D6.

THE SPECIFICATION.
S1 R-1106. `readmeCockpitHtml` makes ONE `replace` over the alternation
   `/<img src="([^"]*)" alt="([^"]*)">|<img\b[^>]*>/g`: a match of the first alternative becomes
   what it becomes today (the rewritten tag for a listed capture, else its alt text), a match of
   the second becomes "". No marker, no placeholder and no second pass remain, and the comment
   above it names R-1106. Every existing test of the function stays as it is and passes. New tests
   in `artifactPreview.test.ts`, each ONE whole-output literal: a README fragment whose text holds
   `@@artifact-image-0@@` with no image comes back unchanged; the same text beside a listed capture
   image comes back with the image rewritten and the text unchanged. You write no `Done:` line and
   no `Landed:` line.
S2 THE TOUR, in `packages/orchestration/result_tour.py`. `TOUR_ANCHOR_KINDS` gains `"preview"` last,
   and `TOUR_PREVIEW_REF = "app"`. `TourAnchorContext` gains a last field `previewable: bool =
   False`. A new `_project_previewable(job) -> bool`, docstring naming DECISION F041 D6: `repo_path
   = getattr(job, "repo_path", "")`; False unless it is a non-empty `str` naming an existing
   directory; else it imports `resolve_spec` and `RuntimeConfigError` from
   `packages.runtimes.runtime_config` INSIDE its body, and answers True when `resolve_spec(repo_path)`
   returns and False when it raises `RuntimeConfigError`. `collect_tour_context` passes
   `previewable=_project_previewable(job)`. `anchor_problem` gains a branch before its `else`:
   `kind == "preview"` resolves exactly when `context.previewable` and `ref == TOUR_PREVIEW_REF`. A
   new `_preview_stop(context) -> dict | None`: None unless previewable, else title "See it
   running", body "Open Results in the cockpit and press Start app to try the change yourself; the
   link appears once the app answers.", anchor `{"kind": "preview", "ref": TOUR_PREVIEW_REF}`,
   each through `_bounded_text` as its neighbours are. `fallback_tour_stops` subtracts one more from
   `room` when that stop exists and places it after "How to run it" and before the Definition of
   Done. `build_tour_prompt` appends the anchor line `preview app` after the command lines only for
   a previewable context. Nothing else in the module changes, and for a context that is not
   previewable every tour, stop list and prompt is byte for byte what it is at `fd124cc9b`.
S3 THE CLIENT. In `apps/ui/src/api/resultTour.ts`, `TOUR_ANCHOR_KINDS` gains `"preview"` last;
   `tourAnchorLabel` answers "The app preview" for it; `tourCanShow` answers true for node, diff and
   preview. In `RemedyShell.tsx`, `handleTourShowAnchor` gains `else if (anchor.kind === "preview")
   { setResultsOpen(true); }` after its diff branch, and its comment names DECISION F041 D6.
   Nothing else in either file changes.
S4 THE TESTS. EDITED, and only these lines: the `TOUR_ANCHOR_KINDS` literal in
   `tests/orchestration/test_result_tour.py` becomes the five kinds; in `resultTour.test.ts` the
   kinds literal becomes the five, and the label and `tourCanShow` cases gain `preview`. NEW, in
   `tests/orchestration/test_result_tour.py`: `_project_previewable` is False for a job whose
   `repo_path` is "" while `monkeypatch.chdir` has put the working directory in a folder holding a
   valid `.remedy/config.toml`, False for a folder with nothing to run, False for a path that is
   not a directory, and True for a folder with a `[runtime]` section whose `cmd` is an argv list;
   `anchor_problem` over `preview`/`app` previewable, `preview`/`app` not previewable and
   `preview`/`other`; the fallback tour of a previewable job with a report, one changed file and a
   run command, as ONE whole-shape literal with the preview stop in its place; a previewable job
   with ten changed areas still yields exactly eight stops, one of them the preview stop; and the
   prompt holds the line `preview app` for a previewable context and is byte-equal to the
   non-previewable one with that line removed. In `tests/ui_contracts/test_artifact_preview.py`: the
   shell's `handleTourShowAnchor` body holds `anchor.kind === "preview"` followed by
   `setResultsOpen(true)`. NEW FILE at `tests/ui_server/test_preview_end_to_end.py`, `pytestmark =
   pytest.mark.subprocess`, one test, module docstring naming F041 T003 and DECISION F041 D6:
   (a) a project under `tmp_path` holding `server.py`, a stdlib `http.server` bound to
   `127.0.0.1` at `int(os.environ["PORT"])` answering every GET with 200 and the body
   `fixture app ok`, and `.remedy/config.toml` with `[runtime]` `cmd = [<sys.executable>,
   "server.py"]`, `port = worker_port()` and `health_path = "/"`; (b) `REMEDY_DATA_DIR` under
   `tmp_path` and `REMEDY_PREVIEW_IDLE_TTL_SECONDS` = "2" by `monkeypatch.setenv`, then
   `reset_config()`, which a `finally` calls again after undoing both; (c) a saved `JobPlan` whose
   `repo_path` is the project, as `test_preview_commands.py` saves one; (d) a real UI server in a
   daemon thread, `_start_server`'s shape from `test_tour_e2e_live.py` copied, not imported; (e)
   OPEN: `job.preview-start` posted to the door with the bearer token, the CSRF header and a fresh
   nonce answers 200 `accepted`; (f) LIVE: `GET /api/jobs/<id>/preview` read every 0.5 seconds for
   at most 120 seconds until the state is `live`, EVERY answer before it holding `url` "" and
   `port` 0, the live answer holding `http://127.0.0.1:<the configured port>/` and that port;
   (g) THE LINK: a GET of that url answers 200 with a body holding `fixture app ok`; (h) the app's
   and the supervisor's pids read from the harness's own runtime record for the project, as
   `remedy runtime status` finds it, both alive by `psutil`; (i) IDLE: no read of the view any
   more; `load_preview` read from disk every 0.5 seconds for at most 60 seconds until the state is
   `stopped`, with the reason `stopped after 2 seconds without a viewer`; (j) TRUTHFUL: the view
   then answers `stopped`, `url` "", `port` 0 and that reason; within 10 seconds neither pid is a
   running process by `psutil` (absent, or a zombie); and a GET of the old url no longer answers
   200; (k) a `finally`
   that, if the project's runtime is still recorded, runs `run_runtime_verb("stop", <project>)` and
   reports it. The test never sleeps longer than 0.5 seconds at a time.

BUNDLE — the commits are C1a, C1b, C2, C3, C4, C5, C6, C7 and C8, in this order.
C1a — `.agent/authored/f041-r6-block.md` := this block, and `.agent/authored/f041-r6-plan.md` :=
  plan.md, by `shutil.copyfile`. Subject: `F041 R6 C1a: copy round 6 block and plan into
  .agent/authored/`. Its insertions are this block's line count plus 27.
C1b — `.agent/authored/f041-r6-records.diff` := records.diff. Subject: `F041 R6 C1b: copy round 6
  records diff into .agent/authored/`. Expected insertions: 30.
C2 — `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md. Subject: `F041 R6 C2: book
  round 5, register R-1106, record D6`. Expected by `git show --numstat`: 10/0 .agent/decisions.md, 4/0 .agent/live_review.md, 7/8 .agent/plan.md.
C3 — S1 and its tests. Subject: `F041 R6 C3: rewrite the README's images in one pass (R-1106)`.
C4 — S2 and its tests in `tests/orchestration/test_result_tour.py`. Subject: `F041 R6 C4: offer a
  "See it running" stop for a job whose project can run`.
C5 — S3, its `resultTour.test.ts` lines and the contract test's addition. Subject: `F041 R6 C5:
  open the results panel from the tour's preview stop`.
C6 — the end-to-end test. Subject: `F041 R6 C6: prove the preview flow on a real small app`.
C7 — your mutation tool as `.agent/authored/f041-r6-mutations.py`. Subject: `F041 R6 C7: add the
  round 6 mutation tool`.
C8 — `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`. Subject: `F041 R6 C8:
  rewrite handoff for round 6`. Then `git push origin feature/f041-artifact-preview` and report
  its real outcome. Do NOT create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split one that
   would reach it into lettered parts with their own subjects (C4a, C4b and so on), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f041-r6-*` files,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `apps/ui/src/api/artifactPreview.ts` and its test, `packages/orchestration/result_tour.py`,
   `tests/orchestration/test_result_tour.py`, `apps/ui/src/api/resultTour.ts` and its test,
   `apps/ui/src/components/shell/RemedyShell.tsx`, `tests/ui_contracts/test_artifact_preview.py`,
   `tests/ui_server/test_preview_end_to_end.py` and `.agent/handoff.md`. Report the list
   `git diff --name-only fd124cc9b` measures after C8. Do NOT touch anything else, in particular
   `packages/runtimes/`, the preview modules, `ui_server.py`, the tour's golden fixtures under
   `tests/orchestration/fixtures/result_tour/`, `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md` or `README.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C8, and the correction is declared. An
   EXISTING test that goes red is never edited to pass unless S4 names its line; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`, no `git reset`. Leave every worktree listed at
   your step 4, its branch, and every stash alone; the one G5 adds is removed as its last action.
6. DO NOT run the full suite: it belongs to F041's closure (amend0917 rule 1). Run no self-use
   job and no command that calls a provider. The only app this round starts is S4's own fixture,
   and the end-to-end test must leave no process of it running; report any it leaves.

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a word
is a finding (guardrail G4). G1 to G5 run before C8 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured against
 the PAYLOADS table; then compare each `.agent/authored/f041-r6-*` payload copy byte for byte with
 its source (the block copy against `.remedy-wt/f041-r6/block.md`), read back with `git show
 <commit>:<path>` from the commit that added it. One reading each.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its dry tree:
 | path | at | bytes | sha256 |
 |---|---|---|---|
 | .agent/decisions.md | C2 | 2471829 | ff24027213680d67f95a6681cad2e50c50bc891083993e8599d9ecdaa9f2b02e |
 | .agent/live_review.md | C2 | 308369 | a4147b1205d3cdf235420170483364e28ead2311d0234800e47fad1bbd3ee09c |
 | .agent/plan.md | C2 | 926 | f75b5bc5d721c87cc25f6ad73e369823cf47343847e2b59ab7bc5639911e48a1 |
 Also: `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's TEXT at
 `fd124cc9b` and at C2 (the reviewer read `[]` and `['R-1106']`), and `git diff --name-only <C1b>
 <C2>`, which must name exactly the three paths of the table.

G3 THE CODE — `python3 -m ruff check packages/orchestration/result_tour.py
 tests/orchestration/test_result_tour.py tests/ui_contracts/test_artifact_preview.py
 tests/ui_server/test_preview_end_to_end.py .agent/authored/f041-r6-mutations.py` at C7, with its
 real exit code. Then report, quoted from the commits, the whole of `readmeCockpitHtml`,
 `_project_previewable`, `_preview_stop`, `fallback_tour_stops`, the changed lines of
 `anchor_problem`, `build_tour_prompt`, `resultTour.ts` and `RemedyShell.tsx`, and the whole
 end-to-end test.

G4 THE TESTS — in the primary checkout at C7, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_result_tour.py tests/ui_server/test_tour_route.py tests/ui_server/test_tour_e2e_live.py tests/cli/test_job_show.py tests/ui_server/test_preview_end_to_end.py tests/ui_server/test_preview_commands.py tests/orchestration/test_preview_worker.py tests/orchestration/test_preview_control.py tests/orchestration/test_preview_runner.py tests/ui_server/test_command_channel.py tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -8; echo "REAL_EXIT=${PIPESTATUS[0]}"'
bash -c 'apps/ui/node_modules/.bin/vitest run --root apps/ui 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran both in the primary checkout at `fd124cc9b`, the first without the new file:
 `1748 passed, 4 skipped` over 1752 collected nodes, and `93 passed | 1 skipped` test files with
 `1905 passed | 5 skipped` tests, all at real exit code 0. Yours must show the same four D3
 quarantine skips and nothing else skipped or failed; report the whole tail of each, every
 `SKIPPED` line, the selection's `--collect-only -q` count at C7, and the node count each file
 this round grows adds to it. Report the end-to-end test's own duration from `--durations=0` on a
 second run of that file alone, and `ps` evidence after it that no `server.py` of its project runs.
 Then `python3 -m apps.cli.main integrity check --json`, all six checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f041-r6-mutations.py`, following your round 5 tool's
 route (vitest scoped with `--root <worktree>/apps/ui --config
 /home/decodeux/Repos/remedy/apps/ui/vitest.config.ts`, pytest with the worktree as the working
 directory and `python3 -B`), prints one line per mutation with the runner's exit code and failed
 count, unmutated controls first and last, `restored byte-identical: True` after each, and
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`; a collection or import error is a broken
 edit, not a reading:
  n1 `readmeCockpitHtml` restored whole from `fd124cc9b` (R-1106's revert probe);
  n2 `anchor_problem` resolves a `preview` anchor whatever `previewable` says;
  n3 `_project_previewable` asks `resolve_spec` for an empty `repo_path` too;
  n4 `fallback_tour_stops` leaves the preview stop out;
  n5 `build_tour_prompt` lists `preview app` for every context;
  n6 `tourCanShow` answers false for `preview`;
  n7 `handleTourShowAnchor` no longer opens the results panel for `preview`;
  n8 `idle_stop_due` in `preview_control.py` never answers true, run against the end-to-end test
     alone, which must FAIL rather than hang, inside its own 60-second wait.
 Run it on `git worktree add --detach .remedy-wt/f041-r6-mut <C7>` and report its whole output,
 then `ps` evidence that n8 left no `server.py` of its project running. EVERY mutation must be
 red; a green one is reported as green, and you then add the test that catches it before C8 and
 re-run. Then `git worktree remove --force .remedy-wt/f041-r6-mut`, `git worktree prune`, and
 report `git worktree list | wc -l` and `git status --porcelain`, which must be empty.

G6 TREE AND PUSH — after C8, in your reply since C8 cannot hold them: `git status --porcelain`,
 empty; `git log --oneline -n 10`, C8 to C1a and `fd124cc9b` in order (more if a commit was
 split); `git worktree list | wc -l`, equal to your step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count you
MEASURED beside the one this block expected (none is expected for C3 to C7 — report what you
measure), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected action.
Your Session section reads SESSION 2 of feature F041, round 6, and says in one sentence how much
context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round 6
with the resolution of R-1106, then F041's closure sequence. State the open-findings count, 1
(R-1106, repaired and awaiting review), and the operator-questions count, 1.
