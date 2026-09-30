STEP F044 R5 — ONE KEYMAP, AND F292 REGISTERED FOR THE SURFACES THE FORM ENTRIES NEED: the keymap module, the shell's one listener through it, the bar's focus request, and the registration of the plan view and hunk controls

GOAL
Book round 4, record DECISION F044 D5 with the F292 registration, its operator question and its
assumption-log row, and build D5 (2) and (3) against the reviewer's tests and a render harness that
proves the keys in a real browser.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE TESTS ARE THE REVIEWER'S AND THE CODE IS YOURS:
the test files and the render harness travel as payloads and are the acceptance, and you write
the production code against them and against S1 to S5 below. You never edit a payload; if one
looks wrong to you, STOP and report it. Read DECISION F044 D5 in the records diff before you write
code, and read whole, before you edit or call them: `apps/ui/src/api/termSearch.ts`,
`apps/ui/src/components/graph/zoomView.ts`, `apps/ui/src/components/graph/useSemanticZoom.ts`,
`apps/ui/src/components/shell/RemedyShell.tsx`, `apps/ui/src/components/shell/ProjectProvider.tsx`,
`apps/ui/src/components/command/CommandBar.tsx`, and the guards that read them:
`tests/ui_contracts/test_term_panel_wiring.py`, `tests/ui_contracts/test_semantic_zoom_wiring.py`,
`tests/ui_contracts/test_digest_mount.py` and `tests/ui_contracts/test_palette_sheet_wiring.py`. Do
NOT apply the reviewer's test diff to your working tree before its own commit; read the payload
files with the Read tool.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f044-r5-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f044-r5/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f044-scratch/`      The reviewer's scripts; do not touch them.
  `.remedy-wt/f044-r5-worker/`    YOURS for logs and scripts; create it if absent. All are
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
   `feature/f044-command-palette`, and `git log --oneline -1` must read `5cbbe6c8e`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f044-r5/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f044-r5-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 226 | 23691 | 34b83bc5aacf546741d4bba9470c93d1755d496f9d6955757d6345afd1727216 |
| tests.diff | 196 | 9955 | 098c214adc18d447203436e401649a932d06a7cf594d0f3fe7d2d70a58d86773 |
| plan.md | 29 | 1030 | 784d6d019145e64dc4b867440a0448e16add1524cfda3f4853ae8cd136366846 |
| render_index.html | 11 | 243 | 5716723bcee9de832ffc634b6d8325f3f3e32c125dc07a3ade5911925b3a0bcd |
| render_main.tsx | 41 | 2157 | 377baf69d83fd59b9eb1ab6c534d9a3c9e1efe6f435eb25794bbfa284b32253e |
| render_vite.config.mjs | 28 | 744 | 6c9d24558a507a827d445c793cd6203f7f0f24ac2659dcfe3cff96c20b7d1c6a |
| render_drive.mjs | 196 | 8239 | 5cef6197dc55e1df3cc30a573c61eac89f63bbbfb55995252ffd2226d1aaecea |
| render_measure.py | 186 | 6393 | 393479827864fc5d06364a3d39617baeea24b9cec0349f67a91ea11a5e1a12fb |

`plan.md` is a REWRITE of `.agent/plan.md`. The `.diff` files go on with `git apply`; the reviewer
generated them with `git diff HEAD` from a tree at `5cbbe6c8e`. `records.diff` is D5's records in
one piece, so F292's registration lands atomically: F044's round 4 gate entry appended to
`.agent/live_review.md`, DECISION F044 D5 appended to `.agent/decisions.md`, the operator question
replacing the empty line of `.agent/operator_questions.md`, two assumption lines in
`.agent/context.md`, one row appended to `docs/ui/design_reference/assumption_log.md`, the NEW FILE
at `docs/roadmap/features/T5_F292.md`, F292's STATUS line directly after F044's, F292 in the
"Depends on" line of `docs/roadmap/features/T16_F240.md`, `TOTAL_FEATURES` from 291 to 292 in
`tests/docs/test_docs_consistency.py`, and the README counter from 291 to 292 registered items.
`tests.diff` adds the NEW FILE at `apps/ui/src/api/keymap.test.ts` and edits the existing
`apps/ui/src/api/termSearch.test.ts` (its `isHelpShortcut` cases leave with the function),
`tests/ui_contracts/test_term_panel_wiring.py` (the '?' guard re-pinned on the keymap) and
`tests/ui_contracts/test_palette_sheet_wiring.py`. The `render_*` files are the render harness;
they are copied, never applied, and run from their copies.

THE SPECIFICATION — the tests and the harness are the acceptance; these clauses fix what they
leave open. No `@mui` import, no colour literal, no new dependency, no `fetch(` in any file this
round writes, and none of the words POST, PUT or DELETE in `CommandBar.tsx`.
S1 `apps/ui/src/api/keymap.ts`, NEW, pure, a header naming T5_F044 T002 and DECISION F044 D5 that
   states the deliberate absence: Remedy deliberately does not take a key from a field, and only
   Ctrl+K or Cmd+K reaches the keymap from one. Exports the interfaces `KeymapTarget` (`tagName?`,
   `isContentEditable?`), `KeymapPress` (`key`, `ctrlKey`, `metaKey`, `altKey`), `KeymapResult`
   (`action: KeymapAction | null`, `pendingG: boolean`) and `KeymapBinding` (`keys`, `action`,
   `label`), every field readonly; the type `KeymapAction` = "open-bar" | "open-terms" |
   "go-projects" | "next-sibling" | "previous-sibling" | "zoom-in" | "walk-back";
   `KEYMAP_BINDINGS` exactly as the test "documents every binding" pins; `isTypingTarget(target)`,
   true for a content-editable target or one whose upper-cased tag is INPUT, TEXTAREA or SELECT,
   false for null; and `keymapAction(press, target, pendingG, dialogOpen)`, which applies, in this
   order: Ctrl+K or Cmd+K ("k" in either case) without Alt is "open-bar" from anywhere; any other
   press with Ctrl, Cmd or Alt, and any press from a typing target, is nothing; a waiting "g"
   followed by "p" is "go-projects"; "g" is nothing and leaves a "g" waiting; "/" "open-bar", "?"
   "open-terms", "j" "next-sibling", "k" "previous-sibling"; Enter "zoom-in" only when the target
   is null or its upper-cased tag is BODY, else nothing; Escape "walk-back" unless `dialogOpen`,
   then nothing; any other key nothing. Every result but the one a "g" makes leaves no "g" waiting.
S2 `apps/ui/src/api/termSearch.ts`: `KeyTarget` and `isHelpShortcut` are deleted, and the header
   says that the key press opening the panel is the keymap's, naming `keymap.ts` and DECISION F044
   D5. Nothing else changes.
S3 `apps/ui/src/components/graph/zoomView.ts`: `escapeWalksBack` keeps its signature and answers
   `!dialogOpen && !isTypingTarget(target)`, importing `isTypingTarget` from
   `"../../api/keymap"`, and its doc comment names the keymap's rule and DECISION F044 D5.
   Nothing else changes; `useSemanticZoom.ts` is not touched.
S4 `apps/ui/src/components/shell/RemedyShell.tsx`: the import of `isHelpShortcut` becomes the
   import of `keymapAction` from `"../../api/keymap"`, and `useRef` joins the React import. The
   shell's one window key listener, under a comment naming T5_F044 T002 and DECISION F044 D5, reads
   `const target = event.target instanceof HTMLElement ? event.target : null;`, whether an element
   with `role="dialog"` is on the page, and `const result = keymapAction(event, target,
   pendingG.current, dialogOpen);`, stores `pendingG.current = result.pendingG;`, and then:
   `if (result.action === "open-terms") {` prevents the default and opens the terms panel;
   "open-bar" prevents the default and calls `setBarFocusRequest((count) => count + 1);`;
   "go-projects" prevents the default and calls `goHome();` from the project context. A state
   `barFocusRequest` starting at 0 and a ref `pendingG` starting false hold what the listener
   needs, and the effect lists `goHome` as its dependency. The listener is still added once with
   `window.addEventListener("keydown", onKey);` and removed with
   `window.removeEventListener("keydown", onKey);`. The bar gains `focusRequest={barFocusRequest}`.
   The comment above `termsOpen` no longer speaks of the listener. Nothing else changes.
S5 `apps/ui/src/components/command/CommandBar.tsx`: a new prop `focusRequest: number`, a ref
   `inputRef` on the input (`ref={inputRef}`), and an effect over `focusRequest` holding exactly
   `if (focusRequest > 0) inputRef.current?.focus();`, under a comment naming DECISION F044 D5.
   Nothing else changes.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C2, C3, C4, C5, C6 and C7, in this order.

C1a — copy this block and the plan payload
  `.agent/authored/f044-r5-block.md` := this block and `.agent/authored/f044-r5-plan.md` := plan.md,
  by `shutil.copyfile`.
  Subject: `F044 R5 C1a: copy round 5 block and plan payload into .agent/authored/`
  Its insertions are this block's line count plus 29. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the records diff and the harness runner
  `.agent/authored/f044-r5-records.diff` := records.diff and
  `.agent/authored/f044-r5-render_measure.py` := render_measure.py.
  Subject: `F044 R5 C1b: copy round 5 records diff and harness runner into .agent/authored/`
  Expected insertions: 412.

C1c — copy the tests diff
  `.agent/authored/f044-r5-tests.diff` := tests.diff.
  Subject: `F044 R5 C1c: copy round 5 tests diff into .agent/authored/`
  Expected insertions: 196.

C1d — copy the harness page and driver
  `.agent/authored/f044-r5-render_index.html`, `f044-r5-render_main.tsx`,
  `f044-r5-render_vite.config.mjs` and `f044-r5-render_drive.mjs`, each := its payload.
  Subject: `F044 R5 C1d: copy the round 5 render harness page and driver into .agent/authored/`
  Expected insertions: 276.

C2 — THE RECORDS AND F292's REGISTRATION, in this order: `git apply` records.diff; rewrite
  `.agent/plan.md` := plan.md.
  Subject: `F044 R5 C2: book F044 R4, record D5, register F292 directly after F044`
  Expected by `git show --numstat` (insertions and deletions): 4/1 .agent/context.md, 46/0 .agent/decisions.md, 2/0 .agent/live_review.md, 19/1 .agent/operator_questions.md, 8/9 .agent/plan.md, 1/1 README.md, 1/0 docs/roadmap/STATUS.md, 1/1 docs/roadmap/features/T16_F240.md, 54/0 docs/roadmap/features/T5_F292.md, 1/0 docs/ui/design_reference/assumption_log.md, 1/1 tests/docs/test_docs_consistency.py.

C3 — THE PURE RULES: S1 to S3.
  Subject: `F044 R5 C3: add the one keymap and move the field rule onto it`
  The reviewer's own version read 106/0 apps/ui/src/api/keymap.ts, 3/20 apps/ui/src/api/termSearch.ts, 5/7 apps/ui/src/components/graph/zoomView.ts.

C4 — THE WIRING: S4 and S5.
  Subject: `F044 R5 C4: listen once through the keymap and let it focus the bar`
  The reviewer's own version read 11/1 apps/ui/src/components/command/CommandBar.tsx, 22/6 apps/ui/src/components/shell/RemedyShell.tsx.

C5 — THE TESTS: `git apply` tests.diff.
  Subject: `F044 R5 C5: add the reviewer's tests for the keymap`
  Expected: 108/0 apps/ui/src/api/keymap.test.ts, 1/22 apps/ui/src/api/termSearch.test.ts, 12/1 tests/ui_contracts/test_palette_sheet_wiring.py, 5/2 tests/ui_contracts/test_term_panel_wiring.py.

C6 — THE TOOL: your mutation tool (G5) saved as `.agent/authored/f044-r5-mutations.py`.
  Subject: `F044 R5 C6: add the round 5 mutation tool`

C7 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F044 R5 C7: rewrite handoff for round 5`
  Then `git push origin feature/f044-command-palette` and report its real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's whole tracked path set is: the `.agent/authored/f044-r5-*` copies and tool, the
   paths the diffs edit or add, `.agent/plan.md`, the files S1 to S5 name, and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 5cbbe6c8e` at the
   branch tip after C7. Do NOT touch `apps/ui/src/components/graph/useSemanticZoom.ts`,
   `apps/ui/src/components/graph/BrainGraphStage.tsx`, `packages/`, `apps/cli/`,
   `apps/ui/package.json`, `.agent/prose_slips.md` or `.agent/candidates.md`.
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
 against the PAYLOADS table. Then compare each `.agent/authored/f044-r5-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f044-r5/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS AND THE TESTS — the sha256 of each file below, read with `git show <commit>:<path>`
 at the commit named, equals the reviewer's reading, printed from its simulation tree. Report
 each path beside the hash you read:
 | path | at | bytes | sha256 |
 |---|---|---|---|
 | .agent/context.md | C2 | 1732 | 33645cfccbd3f345746ef1fbe33786ad2badd0bc34fe4f72f9423ea903442f5b |
 | .agent/decisions.md | C2 | 2561097 | 691cd104bc20d3fe54e3b0cc01bfcdc218052d74b979bc59cfd2a4f71209b8b5 |
 | .agent/live_review.md | C2 | 133356 | 4e7f2c366986315009575aa745d28dfcbffd698d6bbd3f90afb5b6ec95562253 |
 | .agent/operator_questions.md | C2 | 1709 | 2688b3bbf1d7244024f6e67b6f3e9c0698ce3e9dc57318c900ff534b5d2f6096 |
 | README.md | C2 | 47882 | 0779f201a753ec1a87392c8d39948ff96c47a3dbcdd42c00163eb0825cbe8770 |
 | docs/roadmap/STATUS.md | C2 | 59674 | ce38739efcaa2146cbea9249676d574cbe6a2df202502a74e7a369f153f93a00 |
 | docs/roadmap/features/T16_F240.md | C2 | 2518 | 41ab4bf299a53a240df0b2bd9d80828e5203b9e2c58e90cd6c6d15413e5cf521 |
 | docs/roadmap/features/T5_F292.md | C2 | 3546 | e8803f9b2affaf869128a6d268c82b367c41059b1d9a752e36a9ee6d7fa8cdce |
 | docs/ui/design_reference/assumption_log.md | C2 | 34373 | f392e07f32f83511e39348f60727d3adcbd83a627797c4412178c67b39ff360a |
 | tests/docs/test_docs_consistency.py | C2 | 96307 | 781ed84088fffd1d476073c88fe36ccc1333b3a9d71096ff3c9c2cd1a346b8bf |
 | .agent/plan.md | C2 | 1030 | 784d6d019145e64dc4b867440a0448e16add1524cfda3f4853ae8cd136366846 |
 | apps/ui/src/api/keymap.test.ts | C5 | 5599 | cebf127f2e16b1f45739d8328bb662e91e9909dd70b0a8ebd1f5390a8bdb98d1 |
 | apps/ui/src/api/termSearch.test.ts | C5 | 2747 | 5cf21f43a097efa95f36d9baf9f674c3c794db122fff3a23a016a9c6347d858c |
 | tests/ui_contracts/test_palette_sheet_wiring.py | C5 | 4415 | 53041212f9d310393b566b7402cfd510ded798858df516e182b19a85c3b17377 |
 | tests/ui_contracts/test_term_panel_wiring.py | C5 | 2715 | 13ac06ad38488d78835baccfaa69fca9c3926cc054d10264482eb39833295b5c |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show <commit>:<path>` at
 C2 (the reviewer read `[]`); the ledger's last non-empty line at C2, which must begin
 `Gate: F044 R4 — the F044 round 4 entry`; the STATUS lines for F044 and F292 at C2 read back in
 full, F292's directly after F044's; and `git diff --name-only <C1d> <C2>`, which must name
 exactly the C2 paths of the table above.

G3 THE CODE AND THE TESTS — at C6: `python3 -m ruff check .agent/authored/f044-r5-mutations.py
 .agent/authored/f044-r5-render_measure.py tests/ui_contracts/test_palette_sheet_wiring.py
 tests/ui_contracts/test_term_panel_wiring.py tests/docs/test_docs_consistency.py`, and
 `apps/ui/node_modules/.bin/eslint --max-warnings 0 src/api/keymap.ts src/api/keymap.test.ts
 src/api/termSearch.ts src/components/graph/zoomView.ts src/components/command/CommandBar.tsx
 src/components/shell/RemedyShell.tsx` run with `apps/ui` as its working directory, each with its
 real exit code. Report `git show --numstat` of C3 and C4, and the diff of `RemedyShell.tsx` at
 C4, whole. Then, in the primary checkout at C6, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/ui_server/test_explanation_layer_live.py tests/orchestration/test_test_runner.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_live_review_rotation.py tests/regression/test_resource_safety.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 This selection runs `tsc --noEmit` (`test_typescript_compiles`), the whole vitest suite
 (`test_vitest_passes`), eslint over `apps/ui/src` (`tests/ui_contracts/test_ui_lint.py`), the
 docs pins and the explanation layer's browser run over the real shell; name each of those nodes'
 outcomes. The reviewer ran the selection serially in its dry tree, which carries C2, this round's
 tests and the reviewer's own version of S1 to S5 but no `.agent/authored/f044-r5-*` copy and no
 built `apps/ui/dist`, with the primary's `node_modules` linked in, and read `1703 passed, 6
 skipped` at real exit code 0, its skips the four D3 quarantine nodes, the D12 quarantine and
 `tests/ui_contracts/test_responsive.py:555` for an unbuilt `dist`, which your checkout may have
 built. Report every `SKIPPED` line yours prints, the vitest counts of `src/api/keymap.test.ts`,
 `src/api/termSearch.test.ts` and `src/components/graph/zoomView.test.ts` (the reviewer's three
 read 34 together), and the pytest count of `tests/ui_contracts/test_palette_sheet_wiring.py` on its
 own (the reviewer's read `11 passed`). Then `python3 -m apps.cli.main integrity check --json`,
 which must read all six checks `pass` at `fail_count` 0.

G4 THE RENDER — at C6, in the primary checkout:
 `python3 -B .agent/authored/f044-r5-render_measure.py /home/decodeux/Repos/remedy`, which builds
 the harness page over the checkout's own `apps/ui/src`, serves it on 127.0.0.1 port 9010, drives
 `/usr/bin/google-chrome --headless=new` over CDP port 9380, stops both by pid and removes its work
 dir. Report its whole output from the first `PASS` or `FAIL` line on, and its exit code; it must
 print `RENDER: 8 of 8 checks pass` and exit 0. Read the screenshot it writes to
 `/home/decodeux/Repos/remedy/.remedy-wt/f044-r5-render-keys.png` and say in one sentence what it
 shows. The reviewer's own run over its version of S1 to S5 read 8 of 8.

G5 THE RED PROOFS — your tool `.agent/authored/f044-r5-mutations.py` takes a worktree path, and
 for each mutation below edits the named production file INSIDE that worktree (asserting its
 FROM text occurs exactly once there), runs the named check, restores the bytes, and prints one
 line per mutation, starting with its label: the exit code, and the failed count or the harness's
 `RENDER: <n> of 8` reading with its failing labels. Vitest runs as
 `<primary>/apps/ui/node_modules/.bin/vitest run --root <worktree>/apps/ui --config
 <primary>/apps/ui/vitest.config.ts src/api/keymap.test.ts src/api/termSearch.test.ts
 src/components/graph/zoomView.test.ts` with `<worktree>/apps/ui` as the working directory
 (checklist item 33); the wiring test as `python3 -m pytest -q -p no:cacheprovider
 tests/ui_contracts/test_palette_sheet_wiring.py` with `<worktree>` as the working directory; the
 harness as `python3 -B <worktree>/.agent/authored/f044-r5-render_measure.py <worktree>`. The
 primary is `/home/decodeux/Repos/remedy`. The tool runs an unmutated control of every check first
 and last, reports `restored byte-identical: True` after each restore, and ends with
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  k1 a press from a typing target is no longer refused (`keymap.ts`, vitest);
  k2 Alt no longer spoils the Ctrl+K or Cmd+K chord (same);
  k3 an unbound key leaves a waiting "g" waiting (same);
  k4 Enter zooms in from any target (same);
  k5 Escape walks back even while a dialog is open (same);
  k6 `isTypingTarget` compares the tag without upper-casing it (same);
  z1 `escapeWalksBack` ignores a typing target (`zoomView.ts`, vitest);
  h1 the shell no longer prevents the default of "open-bar" (`RemedyShell.tsx`, harness);
  h2 the bar's focus effect is dropped (`CommandBar.tsx`, harness);
  h3 the shell no longer stores the keymap's waiting "g" (`RemedyShell.tsx`, harness);
  w1 the focus request is set to 1 instead of raised by one (same, the wiring test).
 Run it: `git worktree add --detach .remedy-wt/f044-r5-mut <C6>`, then in Python
 `os.symlink("/home/decodeux/Repos/remedy/apps/ui/node_modules",
 "/home/decodeux/Repos/remedy/.remedy-wt/f044-r5-mut/apps/ui/node_modules",
 target_is_directory=True)`, then
 `python3 -B .agent/authored/f044-r5-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f044-r5-mut`
 and report its whole output. The reviewer's own version of this probe, run against its version
 of S1 to S5, turned every one red with every control passing. EVERY mutation must exit
 non-zero; one that stays green is reported as green, never papered over, and you then STOP and
 report it. Then remove the symlink with `os.unlink`, `git worktree remove --force
 .remedy-wt/f044-r5-mut`, `git worktree prune`, and report `git worktree list | wc -l`.

G6 TREE AND PUSH — after C7: `git status --porcelain`, which must be empty;
 `git log --oneline -n 11`, which must show C7, C6, C5, C4, C3, C2, C1d, C1c, C1b, C1a and
 `5cbbe6c8e` in that order (one more line per repair commit); `git worktree list | wc -l`, which
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
SESSION 1 of feature F044, round 5, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 5, then the graph's keys through the keymap and the keymap's cheat overlay. State the
open-findings count, 0, and the operator-questions count, 1.
