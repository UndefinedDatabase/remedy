STEP F288 R6 — THE SECOND HALF OF T003: the keyboard's parallel list of the live picture's prompt nodes, hidden until it holds focus, and a headless browser's proof of the list, the keys and the drawn dots

GOAL
Round 5 passed. Book it, record DECISION F288 D6, and land it: a pure `promptListEntries`, a
`PromptNodeList` of native buttons rendered in the stage's live branch that the keyboard reaches
and that selects the prompt, and a headless-Chrome harness that proves the list, the keys and the
synapses the canvas is handed, with two screenshots for the reviewer. The canvas stays
`aria-hidden` and the simple view is untouched.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. THE CHANGE IS SPECIFIED, NOT SLICED: you write the code, its
tests and the harness yourself against S1 to S5. Read DECISION F288 D6 in the records diff first.

THE DIRECTORIES
  `.remedy-wt/f288-r6-payloads/` and `.remedy-wt/f288-r6/` are READ-ONLY; every other
  `.remedy-wt/f288-*` directory and `.remedy-wt/f288-review/` belongs to the reviewer.
  `.remedy-wt/f288-r6-worker/` is YOURS, and the harness's work dir `.remedy-wt/f288-render-run`
  is its own while it runs; create yours if absent. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the file.
Never run npm or npx. The Node binaries you may run are
`/home/decodeux/Repos/remedy/apps/ui/node_modules/.bin/vitest` (from `apps/ui`, as `vitest run
<files>` and as G5 orders), and the `vite` binary and `node` only through the harness of S4.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f288-event-stream-completeness`, and `git log --oneline -1` must read `cb022003`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f288-r6/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` and `git stash list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f288-r6-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 58 | 13383 | 64934cead79ba357bc85d8154391f1d79c88e81ca7c9a6e4a8d5ea28ba06ec25 |
| plan.md | 29 | 1044 | 6035ae3a5c0ae1fd5fca6caf2359c612d454d51cab1e7d9f2d273fded3a771c6 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `cb022003`. It appends round 5's gate entry to
`.agent/live_review.md` and DECISION F288 D6 to `.agent/decisions.md`.

THE SPECIFICATION
S1 THE ENTRIES. In `apps/ui/src/components/graph/brainView.ts`, a `PromptListEntry` type
   `{ promptId: string; nodeId: string; label: string; state: string }` and
   `promptListEntries(model: BrainModel, visible: BrainLayoutData): PromptListEntry[]`, pure: in
   model order, one entry per `synapse` node of `model` whose id is among `visible.nodes`' ids, with
   `promptId` its `meta.promptId`, `nodeId` its id, `label` `<meta.role> r<meta.round>`, and `state`
   `done` for `pass`, `current` for `in_progress`, `failed` for `fail`, and the state's own name
   otherwise. Its doc comment names DECISION F288 D6 and graph_spec §14.
S2 THE LIST. A new component `apps/ui/src/components/graph/PromptNodeList.tsx` with a style module
   `PromptNodeList.module.css`, props `entries: readonly PromptListEntry[]`,
   `selectedId: string | null` and `onSelect: (promptId: string) => void`. It renders nothing for
   no entries; otherwise a `<nav aria-label="Prompts in the live graph" data-ui="prompt-node-list">`
   holding a `<ul>` of `<li>`, each with one `<button type="button">` whose `aria-label` is
   `<label> — <state>`, whose `aria-pressed` is `entry.nodeId === selectedId`, and whose `onClick`
   calls `onSelect(entry.promptId)`, and whose visible text is the label. The `nav` is visually
   hidden while no element inside it has focus — one pixel, clipped, out of the flow, never
   `display: none` or `visibility: hidden`, which would take the buttons out of the tab order — and
   when `:focus-within` it is shown at the stage's top-left corner above the canvas, as a small panel
   styled with `var(--remedy-*)` tokens only (no `#hex` and no `rgba(` in the file). Its header
   comment names DECISION F288 D6 and graph_spec §14's pairing of the `aria-hidden` canvas with this
   list.
S3 THE STAGE. In `apps/ui/src/components/graph/BrainGraphStage.tsx`, a memoized
   `promptEntries = promptListEntries(model, visible)`, and inside the live branch, directly after
   the `<ZoomBreadcrumbs ... />` line, `<PromptNodeList entries={promptEntries} selectedId={selectedId} onSelect={(promptId) => onSelectNode(promptId)} />`
   on one line. Nothing else in the stage changes, and no `) : (` enters the live branch.
S4 THE HARNESS. Five files under `.agent/authored/`, named `f288-r6-render_measure.py`,
   `f288-r6-render_index.html`, `f288-r6-render_main.tsx`, `f288-r6-render_vite.config.mjs` and
   `f288-r6-render_drive.mjs`, adapted from `.agent/authored/f020-r5-conformance_*` with the same
   mechanics (work dir `.remedy-wt/f288-render-run`, the primary's `node_modules` symlinked in, the
   primary's `vite`, `python3 -m http.server` on 127.0.0.1 port 8993, `/usr/bin/google-chrome
   --headless=new` with its own user-data dir and CDP on port 9363, both stopped by their own pids
   and never by `pkill -f`, the work dir removed at the end). The page imports from
   `apps/ui/src` by relative path and renders, in a 1280x800 viewport, the stage's live wiring
   without the stage: `rebuildBrainModel` over the demo recording's seeds and rows
   (`brainDemoRecording.ts`, through `dashboardBrainSeeds`), `withPromptNodes` with a prompt trace
   of four items — for each of the two recorded tasks a builder item of round 1 and a reviewer item
   of round 1, `runId` that task's recorded attempt id — `buildBrainLayout`, the semantic zoom as
   the stage wires it, `<ForceBrainGraph>` and `<PromptNodeList>` with `promptListEntries`, and a
   selection kept in React state and mirrored to `window.__selected`, with `window.__layout` holding
   the layout. The page renders nothing focusable before the list. `drive.mjs` prints one line per
   check and exits 0 only when all pass and no page exception was thrown:
     C-a the layout holds four `synapse` nodes and the page four list buttons;
     C-b before any key, the `nav`'s bounding box is at most 1x1 pixel;
     C-c one Tab puts focus on the first list button;
     C-d with focus inside, the `nav`'s bounding box is wider and taller than 40 pixels;
     C-e Enter sets `window.__selected` to the first entry's prompt id and its button's
         `aria-pressed` to `true`;
     C-f Tab then Space set `window.__selected` to the second entry's prompt id.
   It saves `Page.captureScreenshot` PNGs as `.remedy-wt/f288-r6-worker/render-before.png` (before
   C-c) and `.remedy-wt/f288-r6-worker/render-after.png` (after C-f), and prints their byte counts.
   Its output is saved as `.agent/authored/f288-r6-render.txt`.
S5 THE CONTRACT. In `tests/ui_contracts/test_brain_stage_mount.py`, new tests that read the sources:
   the stage's live branch (sliced as `tests/ui_contracts/test_semantic_zoom_wiring.py` slices it)
   holds S3's `<PromptNodeList` line and the simple branch does not; `PromptNodeList.tsx` holds
   `type="button"`, `aria-pressed={`, `onSelect(entry.promptId)` and `data-ui="prompt-node-list"`
   and does not hold `aria-hidden`; its style module holds `:focus-within` and neither
   `display: none` nor `visibility: hidden`; and `ForceBrainGraph.tsx` still holds
   `aria-hidden="true"`.

THE TESTS (vitest): in `apps/ui/src/components/graph/brainView.test.ts`, `promptListEntries` over a
model holding synapses in three states and a visible layout lacking one of them: the entries in
model order, the filtered one absent, each field as S1 names it, and no entry for a non-synapse.

BUNDLE — the commits are C1, C2, C3, C4, C5 and C6, in this order.
C1 — `.agent/authored/f288-r6-block.md` := this block, `.agent/authored/f288-r6-records.diff` :=
  records.diff, `.agent/authored/f288-r6-plan.md` := plan.md, all by `shutil.copyfile`.
  Subject: `F288 R6 C1: copy round 6 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 87; STOP rather than commit if that is 500 or more.
C2 — `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F288 R6 C2: book round 5's PASS, record D6 and the round 6 plan`
  Expected by `git show --numstat`: 40/0 decisions.md, 2/0 live_review.md, 9/9 plan.md.
C3 — THE LIST: S1, S2, S3 and S5 with the vitest additions.
  Subject: `F288 R6 C3: let the keyboard reach the live picture's prompts through a parallel list`
C4 — THE HARNESS AND ITS READING: S4's five files and `.agent/authored/f288-r6-render.txt`.
  Subject: `F288 R6 C4: prove the prompt list, its keys and the drawn synapses in headless Chrome`
C5 — THE TOOL: your mutation tool (G5) saved as `.agent/authored/f288-r6-mutations.py`.
  Subject: `F288 R6 C5: add the mutation tool for the round's red proofs`
C6 — THE HANDBACK: `.agent/handoff.md`, rewritten, per `docs/agents/handback_template.md`.
  Subject: `F288 R6 C6: rewrite handoff for round 6`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into lettered parts with their own subjects, and say so.
3. The round's whole tracked path set is: the `.agent/authored/f288-r6-*` copies, harness, reading
   and tool, `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `apps/ui/src/components/graph/brainView.ts`, `apps/ui/src/components/graph/brainView.test.ts`,
   `apps/ui/src/components/graph/PromptNodeList.tsx`,
   `apps/ui/src/components/graph/PromptNodeList.module.css`,
   `apps/ui/src/components/graph/BrainGraphStage.tsx`, `tests/ui_contracts/test_brain_stage_mount.py`,
   and `.agent/handoff.md`. Report the list you measure with `git diff --name-only cb022003` at the
   branch tip after C6. The screenshots are NOT committed.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. A test this round itself wrote that is wrong may be
   corrected before C6, and the correction is declared. An EXISTING test that goes red is never
   edited to pass: report it, name it, and stop.
5. NOTHING IS MERGED, AND THE PRIMARY CHECKOUT NEVER LEAVES THE BRANCH: no `gh pr merge` or
   `gh pr create`, no `git checkout` or `git switch` in the primary checkout, no branch deletion,
   no force-push, no `git stash` of any kind. Read an older commit with `git show <sha>:<path>`.
6. Leave every existing worktree, branch and stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards; Chrome and the server the harness starts are stopped by their own pids.
7. DO NOT run the full suite: F288's one run belongs to its closure.

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G5 run
before C6 is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the table; then each
 `.agent/authored/f288-r6-*` payload copy compared byte for byte with its source (the block copy
 against `.remedy-wt/f288-r6/block.md`), read back with `git show <C1>:<path>`.

G2 THE BOOKING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2243664 | 2420243c48efc1c62bab7d474ad6719fa2b0cad1b3098690186b5a527b9ce670 |
 | .agent/live_review.md | 318731 | d1188613998e89bf48a901b411142b95972db5929d88d50c76c6c22dd5bc5cf8 |
 | .agent/plan.md | 1044 | 6035ae3a5c0ae1fd5fca6caf2359c612d454d51cab1e7d9f2d273fded3a771c6 |
 Also the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT at C2 (the reviewer read it empty).

G3 THE CODE — `python3 -m ruff check tests/ui_contracts/test_brain_stage_mount.py
 .agent/authored/f288-r6-render_measure.py` at C4 with its real exit code; then quote from the diff
 the whole of `promptListEntries`, `PromptNodeList.tsx`, its style module, and the stage's
 `promptEntries` and `<PromptNodeList` lines.

G4 THE TESTS — in the primary checkout at C5, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_self_healing_cycles.py tests/orchestration/test_long_run_executor.py tests/ui_server/test_sse_stream.py tests/ui_server/test_budget_tick_envelope.py tests/ui_contracts tests/ui_server/test_brain_demo_recording_live.py tests/ui_server/test_semantic_zoom_live.py tests/ui_server/test_timeline_scrub_live.py tests/ui_server/test_live_state.py tests/orchestration/test_event_names.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_ble001_ratchet.py tests/test_imports.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran it at `cb022003` and read `1828 passed, 5 skipped` at real exit code 0, the same
 five skips as round 5's, which stay skipped; the vitest suite, the TypeScript compiler and the UI
 lint run inside it. Report every `SKIPPED` line and the Python nodes the round adds
 (`--collect-only -q` on the edited Python test file at `cb022003` and at C5), and account for any
 other difference from 1828. Also `vitest run` over the whole suite from
 `/home/decodeux/Repos/remedy/apps/ui`, whose `Test Files` and `Tests` lines you report (the
 reviewer read 75 files and 1455 tests passed, 5 skipped, at `cb022003`), with the `it(` blocks the
 round adds counted from the diff. Then `python3 -m apps.cli.main integrity check --json`, all six
 checks `pass` at `fail_count` 0.

G5 THE PROOFS — first the harness: `python3 .agent/authored/f288-r6-render_measure.py
 /home/decodeux/Repos/remedy` at C4, its whole output reported (the same text C4 committed), every
 check line `PASS`, real exit code 0, and the two PNGs' paths and byte counts. Then your tool
 `.agent/authored/f288-r6-mutations.py`, which takes a worktree path and for each mutation edits the
 named file INSIDE that worktree (asserting its FROM text occurs exactly once), runs the named
 check, restores the bytes, and prints its label, exit code, failed count and failing names, with an
 unmutated control first and last per runner, `restored byte-identical: True` per file and a final
 line `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Python mutations run
 `python3 -B -m pytest -q -p no:cacheprovider tests/ui_contracts/test_brain_stage_mount.py` from
 the worktree's root after purging its `__pycache__` directories; TypeScript mutations run vitest
 with a PLAIN-OBJECT scratch config (`root` the primary `apps/ui`, `cacheDir` under `.remedy-wt/`,
 `test: { environment: "node", include: [<the worktree's brainView.test.ts>] }`) from the primary
 `apps/ui`, after a route proof that cannot pass whatever the test imports; and the harness
 mutation runs the harness's measure script from the worktree against the worktree as its repo
 root. The mutations:
  m1 `promptListEntries` keeps a synapse the visible layout lacks;
  m2 `promptListEntries` answers `in_progress` rather than `current`;
  m3 `promptListEntries` answers an entry for a `test_run`;
  m4 the list's button calls `onSelect(entry.nodeId)`;
  m5 the style module hides the `nav` with `display: none`;
  m6 the stage renders `<PromptNodeList` in the simple branch instead of the live one;
  m7 the harness, run on a worktree whose `PromptNodeList.tsx` calls `onSelect(entry.nodeId)`,
     must exit non-zero with C-e failing. A fresh worktree has no `apps/ui/node_modules`, so
     the worktree's sources cannot resolve `react`: before m7, symlink the primary's
     `apps/ui/node_modules` into the worktree's `apps/ui/` (the path is gitignored), run the
     unmutated harness there first as m7's control, and delete the symlink before the
     worktree is removed.
 Run it in `git worktree add --detach .remedy-wt/f288-r6-mut <C5>` and report its whole output.
 EVERY mutation must be red; a green one is reported as green, never papered over: you then say
 whether a check can see it, add the one that can, and re-run. Then remove the worktree,
 `git worktree prune`, and report `git worktree list | wc -l`; and `git status --porcelain` must be
 empty, a stray `.vite/` or work dir included.

G6 TREE AND PUSH — after C6: `git status --porcelain` empty; `git log --oneline cb022003..HEAD`;
 `git worktree list | wc -l` and `git stash list | wc -l`, equal to your step 4 readings; the push's
 real outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which
 must be EMPTY. These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this block
expected (none is expected for C3 to C5), every gate's real output and exit code, the authored-text
proofs, the item-status table AGENTS.md requires (one row per commit and per gate), the deviations,
and the next expected action. Your Session section reads SESSION 1 of feature F288, round 6, and
says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
6 with the reviewer's reading of the two screenshots, then the closure sequence. State the
open-findings count, 0, and the operator-questions count, 0.
