STEP F044 R6 — THE GRAPH'S KEYS AND THE HELD "?": "j", "k", Enter and Escape through the one keymap as the zoom's own picks, and the keymap's overlay while "?" is held

GOAL
Book round 5, record DECISION F044 D6 with its assumption-log row, and build D6 (1) to (3) against
the reviewer's tests and a render harness that proves the keys in a real browser.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE TESTS ARE THE REVIEWER'S AND THE CODE IS YOURS:
the test files and the render harness travel as payloads and are the acceptance, and you write
the production code against them and against S1 to S9 below. You never edit a payload; if one
looks wrong to you, STOP and report it. Read DECISION F044 D6 in the records diff before you write
code, and read whole, before you edit or call them: `apps/ui/src/api/keymap.ts`,
`apps/ui/src/components/graph/semanticZoom.ts`, `useSemanticZoom.ts`, `zoomView.ts`,
`BrainGraphStage.tsx`, `ForceBrainGraph.tsx`'s node click, `brainView.ts`'s `selectionIdOf`,
`apps/ui/src/components/shell/RemedyShell.tsx`, and the guards that read them:
`tests/ui_contracts/test_semantic_zoom_wiring.py`, `tests/ui_contracts/test_zoom_deep_link_wiring.py`,
`tests/ui_contracts/test_run_detail_wiring.py`, `tests/ui_contracts/test_timeline_scrub_wiring.py`
(which keeps every timer out of the shell) and `tests/ui_contracts/test_palette_sheet_wiring.py`. Do
NOT apply the reviewer's test diff to your working tree before its own commit; read the payload
files with the Read tool.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f044-r6-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f044-r6/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f044-scratch/`      The reviewer's scripts; do not touch them.
  `.remedy-wt/f044-r6-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, `for` loops over shell variables, and multi-operation one-liners chained with `;` or `&&`
outside a `bash -c`. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read
`${PIPESTATUS[0]}` when you pipe pytest. Use `git -C <path>` rather than `cd`, and never `cd`
your shell into a worktree. Use `python3 - <<'PY'` for counting, hashing and copying
(`shutil.copyfile`). A heredoc containing a dollar-brace or a brace beside a quote is refused:
write such a script to a file under your own directory and run the file. Set environment
variables for a child process inside a Python script (`subprocess.run(..., env=...)`), never on a
command line. Never run npm or npx yourself: call `apps/ui/node_modules/.bin/tsc`, `.bin/vitest`
and `.bin/eslint` by path. Never stop a process with `pkill -f`; the harness stops what it started
by pid. Never open a file for writing before you have read it: `open(p, "w")` empties it first.
Never move a branch with `git reset`: a commit that must change is followed by a new commit.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f044-command-palette`, and `git log --oneline -1` must read `a3b3bd1a9`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f044-r6/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f044-r6-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 64 | 13604 | 890bc12490796d2b53f5a28ac5bb5e33a0bcbe7ce1e6340f774ca1f44fa1ab81 |
| tests.diff | 202 | 10103 | 474dffc2d6df23971b7d5dc56c8f36593807f60a14fcd4ddff416f5a805eb37e |
| plan.md | 28 | 958 | f9138085c1ea947e811b7134af48cb910d8eb036e507b6c7c92e6e4ed9fc4fea |
| render_index.html | 11 | 243 | 1953d80f3abea63ae4dc9fc3858cd587fa0d05dac1a3327c466d9f11a32587fe |
| render_main.tsx | 40 | 2106 | 783f26695e9cf8c25b2b453852f56d7f23ad594f98b766a6cc3e97dada32b6ee |
| render_vite.config.mjs | 28 | 744 | 6c9d24558a507a827d445c793cd6203f7f0f24ac2659dcfe3cff96c20b7d1c6a |
| render_drive.mjs | 227 | 10356 | 3f2e754d38a5b1256eba641dcb15a19477acb150c74cf612c1fee4e37c041db2 |
| render_measure.py | 186 | 6393 | 1e9347a24b81701a53f3987c9d8f53f40c10c4cc90c73fd38f2cf7ea1ad1ce88 |

`plan.md` is a REWRITE of `.agent/plan.md`. The `.diff` files go on with `git apply`; the reviewer
generated them with `git diff HEAD` from a tree at `a3b3bd1a9`. `records.diff` appends F044's round
5 gate entry to `.agent/live_review.md`, DECISION F044 D6 to `.agent/decisions.md` and one row to
`docs/ui/design_reference/assumption_log.md`. `tests.diff` adds the NEW FILE at
`apps/ui/src/components/graph/zoomKeys.test.ts` and edits the existing `apps/ui/src/api/keymap.test.ts`,
`apps/ui/src/components/graph/zoomView.test.ts` (its `escapeWalksBack` cases leave with the
function), `tests/ui_contracts/test_palette_sheet_wiring.py` and
`tests/ui_contracts/test_semantic_zoom_wiring.py` (Escape's guard re-pinned on the graph's keys). The
`render_*` files are the render harness; they are copied, never applied, and run from their copies.

THE SPECIFICATION — the tests and the harness are the acceptance; these clauses fix what they
leave open. No `@mui` import, no colour literal outside `styles/tokens.css`, only `--remedy-*`
tokens in CSS, no new dependency, no `z-index` except through a token, no `fetch(`, and no timer in
`RemedyShell.tsx`, `BrainGraphStage.tsx` or any other file `test_timeline_scrub_wiring.py` names.
S1 `apps/ui/src/api/keymap.ts`: a new export `KEYMAP_HOLD_MS = 400` under a doc comment naming
   DECISION F044 D6 and what the hold does. Nothing else changes.
S2 `apps/ui/src/components/graph/zoomKeys.ts`, NEW, pure, a header naming T5_F044 T002 and
   DECISION F044 D6, saying the machine is not changed and siblings are read in the graph's own
   order. Exports the type `ZoomKeyStep` (`{ kind: "pick"; nodeId }` or `{ kind: "walk-back" }`,
   readonly) and `zoomKeyStep(graph, state, action)`: "walk-back" is a walk back from any state;
   "next-sibling" and "previous-sibling" step one forward or back among, at level 2 or 3 with a
   focus, the run-kind nodes (`isZoomRunKind`) whose `parentId` is the focused node's `parentId`,
   and otherwise the "task" nodes, in the graph's iteration order, wrapping at either end, entering
   at the first going forward and the last going back when the focus is not among them, and
   answering null for none; "zoom-in" at level 1 with a focus picks the first run-kind node whose
   `parentId` is the focused task, null when it has none, and null at every other level; every
   other action is null.
S3 `apps/ui/src/components/graph/useZoomKeys.ts`, NEW, a header naming T5_F044 T002 and DECISION
   F044 D6. Exports `useZoomKeys(graph, state, dispatch, onPick)`. One ref named `latest` holds `{
   graph, state, onPick }`, refreshed by a `useLayoutEffect` with no dependency list. One effect over
   `dispatch` adds one window keydown listener, `window.addEventListener("keydown", onKey);`, and
   removes it: it reads the target as the shell does, whether an element with `role="dialog"` is on
   the page, `keymapAction(event, target, false, dialogOpen)`, and for an action
   `zoomKeyStep(latest.current.graph, latest.current.state, action)`; for a step it prevents the
   default, and then a walk back is `dispatch({ type: "escape" });` and a pick is `dispatch({ type:
   "click", nodeId })` followed by `latest.current.onPick(nodeId)`.
S4 `apps/ui/src/components/graph/useSemanticZoom.ts`: the Escape listener and the import of
   `escapeWalksBack` are deleted; the header says the keys are `useZoomKeys.ts`'s, through the one
   keymap, naming DECISION F044 D6. The reconcile effect stays byte for byte.
S5 `apps/ui/src/components/graph/zoomView.ts`: `escapeWalksBack` and its now-unused import of
   `isTypingTarget` are deleted. Nothing else changes.
S6 `apps/ui/src/components/graph/BrainGraphStage.tsx`: directly after the line calling
   `useZoomDeepLink`, under a comment naming DECISION F044 D6, `useZoomKeys(zoomGraph, zoom.state,
   zoom.dispatch, (nodeId) => {` with a body that reads the node from `zoomGraph`, returns for a
   missing node or a run kind, and otherwise calls `onSelectNode(shellSelectionIdOf(dashboard.tasks,
   id))` for the `id` that `selectionIdOf({ id: nodeId, kind, parentId })` answers when it is not
   null. The imports gain `isZoomRunKind`, `selectionIdOf` and `useZoomKeys`. The line `const zoom =
   useSemanticZoom(zoomGraph);` stays byte for byte.
S7 `apps/ui/src/components/shell/useHeldHelpKey.ts`, NEW, a header naming T5_F044 T002 and
   DECISION F044 D6 that says why the timer lives here. Exports the interface `HeldHelpKey`
   (`readonly shortcutsOpen: boolean`, `press(repeat: boolean): void`) and `useHeldHelpKey(onTap)`.
   `press` (a `useCallback` with no dependencies) ignores a repeat, a pending hold and a shown list;
   otherwise it starts `window.setTimeout(..., KEYMAP_HOLD_MS)`, written so that `}, KEYMAP_HOLD_MS);`
   closes the call, whose firing marks the key held and shows the list. One effect with no
   dependencies adds `window.addEventListener("keyup", onKeyUp);` and a window blur listener and
   removes both, clearing a pending timer on unmount. The keyup handler reads only "?" or "/": with
   a hold pending it clears it and calls the newest `onTap`; with the list shown it hides it. The
   blur clears a pending hold and hides the list.
S8 `apps/ui/src/components/command/KeymapOverlay.tsx` and `KeymapOverlay.module.css`, NEW. Exports
   `KEYMAP_OVERLAY_TITLE = "Keyboard shortcuts"`, `KEYMAP_OVERLAY_HINT = "Let go of ? to close it. A
   quick press of ? shows every term."` and `KeymapOverlay()`: a `<section>` with `role="dialog"`,
   `aria-label` the title, `data-ui="keymap-overlay"`, an `<h2>` of the title, a `<dl>` holding for
   each of `KEYMAP_BINDINGS.map(` one row element with `data-keymap-action` its action, a `<dt>` whose
   `<kbd>` holds the keys and a `<dd>` of the label, and then a `<p>` of the hint. The sheet: fixed,
   centred by `left: 50%`, `top: 50%` and a `translate(-50%, -50%)`, `width: min(420px, calc(100vw -
   48px))`, `z-index: var(--remedy-z-overlay)`, the learning overlay's glass, border, radius, shadow
   and blur, `--remedy-font-ui`; keys in `--remedy-font-mono` on `--remedy-blue-50` in
   `--remedy-blue-strong`.
S9 `apps/ui/src/components/shell/RemedyShell.tsx`: import `KeymapOverlay` and `useHeldHelpKey`.
   Under a comment naming DECISION F044 D6, `const { shortcutsOpen, press: pressHelp } =
   useHeldHelpKey(() => setTermsOpen(true));`. The listener's "open-terms" branch prevents the
   default and calls `pressHelp(event.repeat);` in place of opening the terms, and the effect's
   dependencies become `[goHome, pressHelp]`. Directly after the chat sheet's mount, under a comment
   naming DECISION F044 D6, `{shortcutsOpen && <KeymapOverlay />}`. Nothing else changes.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C2, C3, C4, C5, C6 and C7, in this order.

C1a — copy this block and the plan payload
  `.agent/authored/f044-r6-block.md` := this block and `.agent/authored/f044-r6-plan.md` := plan.md,
  by `shutil.copyfile`.
  Subject: `F044 R6 C1a: copy round 6 block and plan payload into .agent/authored/`
  Its insertions are this block's line count plus 28. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the records diff and the harness runner
  `.agent/authored/f044-r6-records.diff` := records.diff and
  `.agent/authored/f044-r6-render_measure.py` := render_measure.py.
  Subject: `F044 R6 C1b: copy round 6 records diff and harness runner into .agent/authored/`
  Expected insertions: 250.

C1c — copy the tests diff
  `.agent/authored/f044-r6-tests.diff` := tests.diff.
  Subject: `F044 R6 C1c: copy round 6 tests diff into .agent/authored/`
  Expected insertions: 202.

C1d — copy the harness page and driver
  `.agent/authored/f044-r6-render_index.html`, `f044-r6-render_main.tsx`,
  `f044-r6-render_vite.config.mjs` and `f044-r6-render_drive.mjs`, each := its payload.
  Subject: `F044 R6 C1d: copy the round 6 render harness page and driver into .agent/authored/`
  Expected insertions: 306.

C2 — THE RECORDS, in this order: `git apply` records.diff; rewrite `.agent/plan.md` := plan.md.
  Subject: `F044 R6 C2: book F044 R5, record D6 and its assumption-log row`
  Expected by `git show --numstat` (insertions and deletions): 37/0 .agent/decisions.md, 2/0 .agent/live_review.md, 6/7 .agent/plan.md, 1/0 docs/ui/design_reference/assumption_log.md.

C3 — THE GRAPH'S KEYS: S1 to S5.
  Subject: `F044 R6 C3: walk the graph by key through the one keymap`
  The reviewer's own version read 4/0 apps/ui/src/api/keymap.ts, 5/16 apps/ui/src/components/graph/useSemanticZoom.ts, 41/0 apps/ui/src/components/graph/useZoomKeys.ts, 55/0 apps/ui/src/components/graph/zoomKeys.ts, 0/11 apps/ui/src/components/graph/zoomView.ts.

C4 — THE WIRING AND THE OVERLAY: S6 to S9.
  Subject: `F044 R6 C4: select by key in the stage and show the keymap while ? is held`
  The reviewer's own version read 68/0 apps/ui/src/components/command/KeymapOverlay.module.css, 25/0 apps/ui/src/components/command/KeymapOverlay.tsx, 11/2 apps/ui/src/components/graph/BrainGraphStage.tsx, 9/2 apps/ui/src/components/shell/RemedyShell.tsx, 62/0 apps/ui/src/components/shell/useHeldHelpKey.ts.

C5 — THE TESTS: `git apply` tests.diff.
  Subject: `F044 R6 C5: add the reviewer's tests for the graph's keys and the held ?`
  Expected: 8/2 apps/ui/src/api/keymap.test.ts, 76/0 apps/ui/src/components/graph/zoomKeys.test.ts, 1/15 apps/ui/src/components/graph/zoomView.test.ts, 23/1 tests/ui_contracts/test_palette_sheet_wiring.py, 7/1 tests/ui_contracts/test_semantic_zoom_wiring.py.

C6 — THE TOOL: your mutation tool (G5) saved as `.agent/authored/f044-r6-mutations.py`.
  Subject: `F044 R6 C6: add the round 6 mutation tool`

C7 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F044 R6 C7: rewrite handoff for round 6`
  Then `git push origin feature/f044-command-palette` and report its real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's whole tracked path set is: the `.agent/authored/f044-r6-*` copies and tool, the
   paths the diffs edit or add, `.agent/plan.md`, the files S1 to S9 name, and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only a3b3bd1a9` at the
   branch tip after C7. Do NOT touch `apps/ui/src/components/graph/semanticZoom.ts` (the zoom
   transitions), `ForceBrainGraph.tsx`, `packages/`, `apps/cli/`, `apps/ui/package.json`,
   `docs/roadmap/`, `.agent/context.md`, `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md` or `README.md`.
4. Every test the payloads carry passes against your code unedited, at C5, and the render harness
   reads every check passing at C6. A payload is never edited to pass; if your code cannot meet
   one, STOP and report it and the reason.
5. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. An EXISTING test
   that goes red is never edited to pass; report it and stop. A defect you find in your own code
   before the handback is repaired by a further commit, declared, never by moving the branch.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`, no `git reset`.
7. Leave every worktree already listed at your step 4, its branch, and every existing stash
   alone. The worktree G5 adds goes under `.remedy-wt/`, is removed as that gate's last action,
   and `git worktree list | wc -l` is reported afterwards.
8. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F044's belongs to its closure. Run no self-use job and no command that calls a provider.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C7 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f044-r6-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f044-r6/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS AND THE TESTS — the sha256 of each file below, read with `git show <commit>:<path>`
 at the commit named, equals the reviewer's reading, printed from its simulation tree. Report
 each path beside the hash you read:
 | path | at | bytes | sha256 |
 |---|---|---|---|
 | .agent/decisions.md | C2 | 2564233 | 0d9c0cc3258209676f8dd6b94f0e5b5109589ba6da119b46ca59ab2cdc1bd86c |
 | .agent/live_review.md | C2 | 135363 | f855b99a86687fc8cc22c33d1aed9f817d917bb0d5ae06cd7d7ae6137db01647 |
 | docs/ui/design_reference/assumption_log.md | C2 | 35274 | 1835db77e7d2761cca8c2ea61e9a6ad5e96af3b28e0f9e0ee8eeb08aa6b1a5b6 |
 | .agent/plan.md | C2 | 958 | f9138085c1ea947e811b7134af48cb910d8eb036e507b6c7c92e6e4ed9fc4fea |
 | apps/ui/src/api/keymap.test.ts | C5 | 5776 | ae35deb79c455de952089470ae51bad265efeb6e6f67621eef1dc0dac0beab02 |
 | apps/ui/src/components/graph/zoomKeys.test.ts | C5 | 3833 | 4d3f88b6ad45e77fc1ea2d370f0a9af7717e37e126a780f6fafea3585fadebdb |
 | apps/ui/src/components/graph/zoomView.test.ts | C5 | 5771 | b33effce3a88dfe90cbee7ed7d296320f859cfed10f1a4f4cf29146eedbf2a66 |
 | tests/ui_contracts/test_palette_sheet_wiring.py | C5 | 5417 | 9e43c107b44c797db154e266c0e78b6591f8effa20d19d83411cecb9cb426083 |
 | tests/ui_contracts/test_semantic_zoom_wiring.py | C5 | 5101 | 4d48584a81f217c1166e7e125780c0d79a3f01205d838379e13a8915f3e20df8 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show <commit>:<path>` at
 C2 (the reviewer read `[]`); the ledger's last non-empty line at C2, which must begin
 `Gate: F044 R5 — the F044 round 5 entry`; and `git diff --name-only <C1d> <C2>`, which must name
 exactly the C2 paths of the table above.

G3 THE CODE AND THE TESTS — at C6: `python3 -m ruff check .agent/authored/f044-r6-mutations.py
 .agent/authored/f044-r6-render_measure.py tests/ui_contracts/test_palette_sheet_wiring.py
 tests/ui_contracts/test_semantic_zoom_wiring.py`, and `apps/ui/node_modules/.bin/eslint
 --max-warnings 0 src/api/keymap.ts src/components/graph/zoomKeys.ts src/components/graph/useZoomKeys.ts
 src/components/graph/useSemanticZoom.ts src/components/graph/zoomView.ts
 src/components/graph/BrainGraphStage.tsx src/components/shell/useHeldHelpKey.ts
 src/components/shell/RemedyShell.tsx src/components/command/KeymapOverlay.tsx` run with `apps/ui`
 as its working directory, each with its real exit code. Report `git show --numstat` of C3 and C4,
 and the diffs of `BrainGraphStage.tsx` and `RemedyShell.tsx` at C4, whole. Then, in the primary
 checkout at C6, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/ui_server/test_explanation_layer_live.py tests/orchestration/test_test_runner.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_live_review_rotation.py tests/regression/test_resource_safety.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 This selection runs `tsc --noEmit` (`test_typescript_compiles`), the whole vitest suite
 (`test_vitest_passes`), eslint over `apps/ui/src` (`tests/ui_contracts/test_ui_lint.py`) and the
 explanation layer's browser run over the real shell; name each of those nodes' outcomes. The
 reviewer ran the selection serially in its dry tree, which carries C2, this round's tests and the
 reviewer's own version of S1 to S9 but no `.agent/authored/f044-r6-*` copy and no built
 `apps/ui/dist`, with the primary's `node_modules` linked in, and read `1705 passed, 6 skipped` at
 real exit code 0, its skips the four D3 quarantine nodes, the D12 quarantine and
 `tests/ui_contracts/test_responsive.py:555` for an unbuilt `dist`, which your checkout may have
 built. Report every `SKIPPED` line yours prints, the vitest counts of
 `src/components/graph/zoomKeys.test.ts` and `src/api/keymap.test.ts` (the reviewer's two read 21
 together), and the pytest count of `tests/ui_contracts/test_palette_sheet_wiring.py` and
 `tests/ui_contracts/test_semantic_zoom_wiring.py` together (the reviewer's read `21 passed`). Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G4 THE RENDER — at C6, in the primary checkout:
 `python3 -B .agent/authored/f044-r6-render_measure.py /home/decodeux/Repos/remedy`, which builds
 the harness page over the checkout's own `apps/ui/src`, serves it on 127.0.0.1 port 9010, drives
 `/usr/bin/google-chrome --headless=new` over CDP port 9380, stops both by pid and removes its work
 dir. Report its whole output from the first `PASS` or `FAIL` line on, and its exit code; it must
 print `RENDER: 9 of 9 checks pass` and exit 0. Read the screenshot it writes to
 `/home/decodeux/Repos/remedy/.remedy-wt/f044-r6-render-overlay.png` and say in one sentence what it
 shows. The reviewer's own run over its version of S1 to S9 read 9 of 9.

G5 THE RED PROOFS — your tool `.agent/authored/f044-r6-mutations.py` takes a worktree path, and
 for each mutation below edits the named production file INSIDE that worktree (asserting its
 FROM text occurs exactly once there), runs the named check, restores the bytes, and prints one
 line per mutation, starting with its label: the exit code, and the failed count or the harness's
 `RENDER: <n> of 9` reading with its failing labels. Vitest runs as
 `<primary>/apps/ui/node_modules/.bin/vitest run --root <worktree>/apps/ui --config
 <primary>/apps/ui/vitest.config.ts src/components/graph/zoomKeys.test.ts src/api/keymap.test.ts`
 with `<worktree>/apps/ui` as the working directory (checklist item 33); the wiring tests as
 `python3 -m pytest -q -p no:cacheprovider tests/ui_contracts/test_palette_sheet_wiring.py
 tests/ui_contracts/test_semantic_zoom_wiring.py` with `<worktree>` as the working directory; the
 harness as `python3 -B <worktree>/.agent/authored/f044-r6-render_measure.py <worktree>`. The primary
 is `/home/decodeux/Repos/remedy`. The tool runs an unmutated control of every check first and last,
 reports `restored byte-identical: True` after each restore, and ends with
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  z1 a sibling walk stops at the ends instead of wrapping (`zoomKeys.ts`, vitest);
  z2 a run's siblings are every run, not its own task's (same);
  z3 Enter picks the task's last run instead of its first (same);
  z4 a walk back from outside the siblings enters at the first as well (same);
  h1 a key's pick is dispatched but not handed to `onPick` (`useZoomKeys.ts`, harness);
  h2 the release of a tapped "?" no longer opens the terms (`useHeldHelpKey.ts`, harness);
  h3 a hold that fires does not show the list (same);
  h4 the overlay's z-index declaration is dropped (`KeymapOverlay.module.css`, harness);
  h5 the graph's keys read no dialog as open (`useZoomKeys.ts`, harness);
  w1 the overlay lists only the first three bindings (`KeymapOverlay.tsx`, the wiring tests).
 Run it: `git worktree add --detach .remedy-wt/f044-r6-mut <C6>`, then in Python
 `os.symlink("/home/decodeux/Repos/remedy/apps/ui/node_modules",
 "/home/decodeux/Repos/remedy/.remedy-wt/f044-r6-mut/apps/ui/node_modules",
 target_is_directory=True)`, then
 `python3 -B .agent/authored/f044-r6-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f044-r6-mut`
 and report its whole output. The reviewer's own version of this probe, run against its version
 of S1 to S9, turned every one red with every control passing. EVERY mutation must exit
 non-zero; one that stays green is reported as green, never papered over, and you then STOP and
 report it. Then remove the symlink with `os.unlink`, `git worktree remove --force
 .remedy-wt/f044-r6-mut`, `git worktree prune`, and report `git worktree list | wc -l`.

G6 TREE AND PUSH — after C7: `git status --porcelain`, which must be empty;
 `git log --oneline -n 11`, which must show C7, C6, C5, C4, C3, C2, C1d, C1c, C1b, C1a and
 `a3b3bd1a9` in that order (one more line per repair commit); `git worktree list | wc -l`, which
 must equal your step 4 reading; the push's real outcome; and `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, which must be EMPTY. These readings go in your reply,
 since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 and C4 beyond the
reviewer's reading, and none for C6 — report what you measure), every gate's real output and exit
code, the authored-text proofs, the item-status table AGENTS.md requires (one row per commit and
per gate), the deviations, and the next expected action. Count what you list by running a count,
not by eye. Report what you ran, not what you expected to find. Your Session section reads
SESSION 1 of feature F044, round 6, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 6, then the three budgets in CI with their recorded numbers. State the open-findings count,
0, and the operator-questions count, 1.
