STEP F044 R4 — A QUESTION IN THE BAR REACHES THE CHAT: the Ask row, a chat sheet that asks it at once, the chat tab's two entry points, and the reference's placeholder

GOAL
Book round 3, record DECISION F044 D4 with its assumption-log row, and build D4 (1) to (5) against
the reviewer's tests and a render harness that proves the route in a real browser.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE TESTS ARE THE REVIEWER'S AND THE CODE IS YOURS:
the test files and the render harness travel as payloads and are the acceptance, and you write
the production code against them and against S1 to S7 below. You never edit a payload; if one
looks wrong to you, STOP and report it. Read DECISION F044 D4 in the records diff before you write
code, and read whole, before you edit or call them: `apps/ui/src/api/paletteSheet.ts`,
`apps/ui/src/api/firstRunTour.ts`, `apps/ui/src/components/graph/EvidenceChatTab.tsx`,
`apps/ui/src/components/graph/EvidencePanel.tsx` (the tab's other mount),
`apps/ui/src/components/lessons/LessonsOverlay.tsx` and its sheet (the overlay precedent),
`apps/ui/src/components/command/CommandBar.tsx`, `apps/ui/src/components/shell/RemedyShell.tsx`,
and the guards that read them: `tests/ui_contracts/test_chat_citations.py`,
`tests/ui_contracts/test_evidence_panel_contract.py`, `tests/ui_server/test_dashboard_contract.py`
and `tests/ui_contracts/test_raw_colour_ratchet.py`. Do NOT apply the reviewer's test diff to your
working tree before its own commit; read the payload files with the Read tool.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f044-r4-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f044-r4/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f044-scratch/`      The reviewer's scripts; do not touch them.
  `.remedy-wt/f044-r4-worker/`    YOURS for logs and scripts; create it if absent. All are
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
   `feature/f044-command-palette`, and `git log --oneline -1` must read `a706a0701`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f044-r4/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f044-r4-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 68 | 14983 | 7d4c3a3e8098611cbaf6f7ae8f9343fc90571080be03e0dcc9863f0aa4322dea |
| tests.diff | 133 | 6577 | bd257a23c020f497ecc4f45ebd16e330e56185badd89b8ca47ffa29d024649c5 |
| plan.md | 30 | 1007 | 5e53c31093ece6736b23c5d18bd2843d481b83133bbdfc043a56af56baa11f19 |
| render_index.html | 11 | 243 | c56eebb7169e17c13fb2086be7dd40900567fc6b46439f3ff824087f337cf1de |
| render_main.tsx | 50 | 2421 | 6632aa3538e465b3ae6402a738b56c6cee0bbf64c5156d16c8c920e022f9f1b4 |
| render_vite.config.mjs | 28 | 744 | 6c9d24558a507a827d445c793cd6203f7f0f24ac2659dcfe3cff96c20b7d1c6a |
| render_drive.mjs | 222 | 10409 | 8a3b438a4b8be259cd3f0e0e4b5deb84538f2e5ea1d04d108cfaf50354128991 |
| render_measure.py | 186 | 6393 | 49bb768179477c0e360d448a3eac787518630729f801f5a44728b9d3dd039825 |

`plan.md` is a REWRITE of `.agent/plan.md`. The `.diff` files go on with `git apply`; the reviewer
generated them with `git diff HEAD` from a tree at `a706a0701`. `records.diff` appends F044's round
3 gate entry to `.agent/live_review.md`, DECISION F044 D4 to `.agent/decisions.md` and one row to
`docs/ui/design_reference/assumption_log.md`. `tests.diff` edits the existing
`apps/ui/src/api/paletteSheet.test.ts`, `apps/ui/src/api/firstRunTour.test.ts` and
`tests/ui_contracts/test_palette_sheet_wiring.py`. The `render_*` files are the render harness;
they are copied, never applied, and run from their copies.

THE SPECIFICATION — the tests and the harness are the acceptance; these clauses fix what they
leave open. No `@mui` import, no colour literal outside `styles/tokens.css`, only `--remedy-*`
tokens in CSS, no new dependency, no `z-index` except through a token, no `fetch(` in any file
this round writes, and none of the words POST, PUT or DELETE in `CommandBar.tsx`.
S1 `apps/ui/src/api/paletteSheet.ts`: its header also names DECISION F044 D4 and the Ask row.
   `PaletteSection` gains "Ask" and `PALETTE_SECTION_ORDER` reads Recent, Ask, Commands, Jump,
   Projects, Help. `PaletteAction` gains `{ kind: "chat"; text }` (readonly). New exports:
   `PALETTE_ASK_HINT = "Ask the chat"` and `askRow(query)`, a row with `key` and `ref` "ask",
   section "Ask", label and action text the query with its runs of white space read as one space
   and its ends trimmed, hint `PALETTE_ASK_HINT`, no range and no reason. In `buildPaletteRows`,
   after every other row is built (and never in "task" mode or for a blank query): when
   `routeBarText(query, focusedTaskId)` reads a question, or when no other row was built, the Ask
   row comes first. A remembered "ask" ref names nothing.
S2 `apps/ui/src/api/firstRunTour.ts`: the sixth step's title and body become exactly what the test
   "words every step exactly as DECISION F043 D4 wrote it, DECISION F044 D2 moved its last and D4
   reworded it" pins. Nothing else changes.
S3 `apps/ui/src/components/graph/EvidenceChatTab.tsx`: two optional props, `initialQuestion?:
   string` and nothing else new. `const projectOnly = taskId === "";` and the whole-project flag
   starts at `projectOnly`; while `projectOnly` the scope checkbox and its label are not rendered.
   The ask takes the line to ask as its argument (the input's Enter and the Ask button pass the
   typed text) and is a `useCallback` over the job, the token, the task and the whole-project flag.
   A `useRef` named `askedInitial` and an effect over the ask and `initialQuestion` ask a non-blank
   `initialQuestion` exactly once, the effect setting `askedInitial.current = true;` before it
   asks. The doc comment of the tab names DECISION F044 D4 and both entry points. The evidence
   panel's mount line and every string `test_chat_citations.py` pins stay byte for byte.
S4 `apps/ui/src/components/command/ChatSheet.tsx`, NEW, a header naming T5_F044 T001 and DECISION
   F044 D4 and saying the chat is routed to, not rebuilt. Exports `CHAT_SHEET_TITLE = "Ask the
   chat"` and `ChatSheet({ jobId, serverToken, taskId, question, onClose, onOpenTab })`, `onOpenTab:
   (tab: EvidenceTab) => void`: a `<section>` with `className={styles.sheet}`, `role="dialog"`,
   `aria-label={CHAT_SHEET_TITLE}` and `data-ui="chat-sheet"`, holding a header with an `<h2>` of
   the title and a button reading "Close chat" that calls `onClose`, then `<EvidenceChatTab
   jobId={jobId} token={serverToken} taskId={taskId} onTab={onOpenTab} initialQuestion={question}
   />`. A window key listener closes it on Escape, removed on unmount. It reads and sends nothing
   itself.
S5 `apps/ui/src/components/command/ChatSheet.module.css`, NEW: `.sheet` fixed at `top: 24px`,
   `right: 24px`, `bottom: 24px`, `width: min(520px, calc(100vw - 48px))`, `z-index:
   var(--remedy-z-overlay)`, a column with a 12px gap, `padding: 18px 20px`, vertical scrolling,
   `--remedy-glass-bg-strong` background, `--remedy-glass-border` border, `--remedy-radius-xl`,
   `--remedy-shadow-card`, a 14px backdrop blur and `--remedy-font-ui`; the header and its `h2`
   and the close button as the learning overlay's sheet draws them, in tokens.
S6 `apps/ui/src/components/command/CommandBar.tsx`: `BAR_PLACEHOLDER` becomes `'Ask your agent or
   jump to anything (e.g., "improve error handling")'`, its doc comment naming DECISION F044 D4. A
   new prop `onAskChat: (text: string) => void`. Choosing a row whose action is "chat", outside a
   flow, clears the outcome, empties the bar, closes the sheet, clears the active row and calls
   `onAskChat` with the row's text, WITHOUT remembering the row.
S7 `apps/ui/src/components/shell/RemedyShell.tsx`: import `ChatSheet` from
   `"../command/ChatSheet"`. Under a comment naming DECISION F044 D4, a state `chatAsk: { key:
   number; text: string } | null`, and an evidence handler: "diff" calls `setOpenDiffTaskId` with
   `focusedTaskId`, and "prompt" with a `focusedTaskId` that is not "" calls `onSelectNode(
   shellSelectionIdOf(dashboard.tasks, focusedTaskId))`. The bar gains `onAskChat` setting
   `chatAsk` to the text under a key one higher than the last (1 for the first). Directly after the
   shell's own add-task sheet mount, under a comment naming DECISION F044 D4, while `chatAsk` is
   not null, `<ChatSheet key={chatAsk.key} jobId={dashboard.jobId} serverToken={serverToken}
   taskId={focusedTaskId} question={chatAsk.text} onClose={() => setChatAsk(null)} onOpenTab=<the
   evidence handler> />`.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C2, C3, C4, C5, C6 and C7, in this order.

C1a — copy this block and the plan payload
  `.agent/authored/f044-r4-block.md` := this block and `.agent/authored/f044-r4-plan.md` := plan.md,
  by `shutil.copyfile`.
  Subject: `F044 R4 C1a: copy round 4 block and plan payload into .agent/authored/`
  Its insertions are this block's line count plus 30. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the records diff and the harness runner
  `.agent/authored/f044-r4-records.diff` := records.diff and
  `.agent/authored/f044-r4-render_measure.py` := render_measure.py.
  Subject: `F044 R4 C1b: copy round 4 records diff and harness runner into .agent/authored/`
  Expected insertions: 254.

C1c — copy the tests diff
  `.agent/authored/f044-r4-tests.diff` := tests.diff.
  Subject: `F044 R4 C1c: copy round 4 tests diff into .agent/authored/`
  Expected insertions: 133.

C1d — copy the harness page and driver
  `.agent/authored/f044-r4-render_index.html`, `f044-r4-render_main.tsx`,
  `f044-r4-render_vite.config.mjs` and `f044-r4-render_drive.mjs`, each := its payload.
  Subject: `F044 R4 C1d: copy the round 4 render harness page and driver into .agent/authored/`
  Expected insertions: 311.

C2 — THE RECORDS, in this order: `git apply` records.diff; rewrite `.agent/plan.md` := plan.md.
  Subject: `F044 R4 C2: book F044 R3, record D4 and its assumption-log row`
  Expected by `git show --numstat` (insertions and deletions): 41/0 .agent/decisions.md, 2/0 .agent/live_review.md, 8/11 .agent/plan.md, 1/0 docs/ui/design_reference/assumption_log.md.

C3 — THE PURE RULES: S1 and S2.
  Subject: `F044 R4 C3: add the Ask row and reword the tour's last stop`
  The reviewer's own version read 2/2 apps/ui/src/api/firstRunTour.ts, 32/7 apps/ui/src/api/paletteSheet.ts.

C4 — THE COMPONENTS: S3 to S7.
  Subject: `F044 R4 C4: route a question from the bar to the grounded chat in a sheet`
  The reviewer's own version read 42/0 apps/ui/src/components/command/ChatSheet.module.css, 39/0 apps/ui/src/components/command/ChatSheet.tsx, 15/2 apps/ui/src/components/command/CommandBar.tsx, 32/17 apps/ui/src/components/graph/EvidenceChatTab.tsx, 19/0 apps/ui/src/components/shell/RemedyShell.tsx.

C5 — THE TESTS: `git apply` tests.diff.
  Subject: `F044 R4 C5: add the reviewer's tests for the route to the chat`
  Expected: 3/3 apps/ui/src/api/firstRunTour.test.ts, 36/2 apps/ui/src/api/paletteSheet.test.ts, 25/1 tests/ui_contracts/test_palette_sheet_wiring.py.

C6 — THE TOOL: your mutation tool (G5) saved as `.agent/authored/f044-r4-mutations.py`.
  Subject: `F044 R4 C6: add the round 4 mutation tool`

C7 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F044 R4 C7: rewrite handoff for round 4`
  Then `git push origin feature/f044-command-palette` and report its real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's whole tracked path set is: the `.agent/authored/f044-r4-*` copies and tool, the
   paths the diffs edit, `.agent/plan.md`, the files S1 to S7 name, and `.agent/handoff.md`.
   Report the list you measure with `git diff --name-only a706a0701` at the branch tip after C7.
   Do NOT touch `apps/ui/src/api/chatTurn.ts`, `apps/ui/src/components/graph/EvidencePanel.tsx`,
   `apps/ui/src/components/panels/`, `packages/`, `apps/cli/`, `apps/ui/package.json`,
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
 against the PAYLOADS table. Then compare each `.agent/authored/f044-r4-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f044-r4/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS AND THE TESTS — the sha256 of each file below, read with `git show <commit>:<path>`
 at the commit named, equals the reviewer's reading, printed from its simulation tree. Report
 each path beside the hash you read:
 | path | at | bytes | sha256 |
 |---|---|---|---|
 | .agent/decisions.md | C2 | 2556928 | a19abc055ce628ce76cfdad93207de8e89e2047a1fb66efc71e1fde063c70c4b |
 | .agent/live_review.md | C2 | 131716 | 4d6a24eafa0056c3746c6e4e63b692f2218c159ec0d47036ea0a91cbc3730749 |
 | .agent/plan.md | C2 | 1007 | 5e53c31093ece6736b23c5d18bd2843d481b83133bbdfc043a56af56baa11f19 |
 | docs/ui/design_reference/assumption_log.md | C2 | 33670 | d26afa9898f9f9db41cd4881253080b4dbd1127b2c022aaed975e64ec3927adc |
 | apps/ui/src/api/firstRunTour.test.ts | C5 | 4029 | 909fe6d22086772a4a8d3939e06b8a0d6a7f7d1c6645c01a1439eaa2a46d74c8 |
 | apps/ui/src/api/paletteSheet.test.ts | C5 | 13491 | e408370a192bf153720d01a68d7837dd92ec95d36813243ba67b5c98e4085c1b |
 | tests/ui_contracts/test_palette_sheet_wiring.py | C5 | 3968 | 6c2fd3db2d966802b176aad385a08fb23e260d8b00a64b3e125ecb7a4434170f |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show <commit>:<path>` at
 C2 (the reviewer read `[]`); the ledger's last non-empty line at C2, which must begin
 `Gate: F044 R3 — the F044 round 3 entry`; and `git diff --name-only <C1d> <C2>`, which must name
 exactly the C2 paths of the table above.

G3 THE CODE AND THE TESTS — at C6: `python3 -m ruff check .agent/authored/f044-r4-mutations.py
 .agent/authored/f044-r4-render_measure.py tests/ui_contracts/test_palette_sheet_wiring.py`, and
 `apps/ui/node_modules/.bin/eslint --max-warnings 0 src/api/paletteSheet.ts src/api/firstRunTour.ts
 src/components/graph/EvidenceChatTab.tsx src/components/command/ChatSheet.tsx
 src/components/command/CommandBar.tsx src/components/shell/RemedyShell.tsx` run with `apps/ui`
 as its working directory, each with its real exit code. Report `git show --numstat` of C3 and
 C4, and the diffs of `EvidenceChatTab.tsx` and `RemedyShell.tsx` at C4, whole. Then, in the
 primary checkout at C6, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/ui_server/test_explanation_layer_live.py tests/orchestration/test_test_runner.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_live_review_rotation.py tests/regression/test_resource_safety.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 This selection runs `tsc --noEmit` (`test_typescript_compiles`), the whole vitest suite
 (`test_vitest_passes`), eslint over `apps/ui/src` (`tests/ui_contracts/test_ui_lint.py`) and the
 explanation layer's browser run over the real shell; name each of those nodes' outcomes. The
 reviewer ran the selection serially in its dry tree, which carries C2, this round's tests and
 the reviewer's own version of S1 to S7 but no `.agent/authored/f044-r4-*` copy and no built
 `apps/ui/dist`, with the primary's `node_modules` linked in, and read `1702 passed, 6 skipped` at
 real exit code 0, its skips the four D3 quarantine nodes, the D12 quarantine and
 `tests/ui_contracts/test_responsive.py:555` for an unbuilt `dist`, which your checkout may have
 built. Report every `SKIPPED` line yours prints, the vitest counts of
 `src/api/paletteSheet.test.ts` and `src/api/firstRunTour.test.ts` (the reviewer's read 33 and 7),
 and the pytest count of `tests/ui_contracts/test_palette_sheet_wiring.py` on its own (the
 reviewer's read `10 passed`). Then `python3 -m apps.cli.main integrity check --json`, which must
 read all six checks `pass` at `fail_count` 0.

G4 THE RENDER — at C6, in the primary checkout:
 `python3 -B .agent/authored/f044-r4-render_measure.py /home/decodeux/Repos/remedy`, which builds
 the harness page over the checkout's own `apps/ui/src`, serves it on 127.0.0.1 port 9010, drives
 `/usr/bin/google-chrome --headless=new` over CDP port 9380, stops both by pid and removes its work
 dir. Report its whole output from the first `PASS` or `FAIL` line on, and its exit code; it must
 print `RENDER: 9 of 9 checks pass` and exit 0. Read the screenshot it writes to
 `/home/decodeux/Repos/remedy/.remedy-wt/f044-r4-render-chat.png` and say in one sentence what it
 shows. The reviewer's own run over its version of S1 to S7 read 9 of 9.

G5 THE RED PROOFS — your tool `.agent/authored/f044-r4-mutations.py` takes a worktree path, and
 for each mutation below edits the named production file INSIDE that worktree (asserting its
 FROM text occurs exactly once there), runs the named check, restores the bytes, and prints one
 line per mutation, starting with its label: the exit code, and the failed count or the harness's
 `RENDER: <n> of 9` reading with its failing labels. Vitest runs as
 `<primary>/apps/ui/node_modules/.bin/vitest run --root <worktree>/apps/ui --config
 <primary>/apps/ui/vitest.config.ts src/api/paletteSheet.test.ts src/api/firstRunTour.test.ts`
 with `<worktree>/apps/ui` as the working directory (checklist item 33); the wiring test as
 `python3 -m pytest -q -p no:cacheprovider tests/ui_contracts/test_palette_sheet_wiring.py` with
 `<worktree>` as the working directory; the harness as `python3 -B
 <worktree>/.agent/authored/f044-r4-render_measure.py <worktree>`. The primary is
 `/home/decodeux/Repos/remedy`. The tool runs an unmutated control of every check first and last,
 reports `restored byte-identical: True` after each restore, and ends with
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  a1 the Ask row comes only when no other row was built, even for a question (`paletteSheet.ts`,
     vitest);
  a2 the Ask row comes for every line that is not blank (same);
  a3 the Ask row's text keeps the query as typed (same);
  t1 the sixth tour step keeps its old title (`firstRunTour.ts`, vitest);
  w1 the chat sheet mounts the tab without the question (`ChatSheet.tsx`, the wiring test);
  h1 the tab marks the initial question asked without asking it (`EvidenceChatTab.tsx`, harness);
  h2 the scope checkbox is shown with no task (same);
  h3 the chat sheet's z-index declaration is dropped (`ChatSheet.module.css`, harness);
  h4 Escape no longer closes the chat sheet (`ChatSheet.tsx`, harness);
  h5 `BAR_PLACEHOLDER` goes back to round 3's words (`CommandBar.tsx`, harness).
 Run it: `git worktree add --detach .remedy-wt/f044-r4-mut <C6>`, then in Python
 `os.symlink("/home/decodeux/Repos/remedy/apps/ui/node_modules",
 "/home/decodeux/Repos/remedy/.remedy-wt/f044-r4-mut/apps/ui/node_modules",
 target_is_directory=True)`, then
 `python3 -B .agent/authored/f044-r4-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f044-r4-mut`
 and report its whole output. The reviewer's own version of this probe, run against its version
 of S1 to S7, turned every one red with every control passing. EVERY mutation must exit
 non-zero; one that stays green is reported as green, never papered over, and you then STOP and
 report it. Then remove the symlink with `os.unlink`, `git worktree remove --force
 .remedy-wt/f044-r4-mut`, `git worktree prune`, and report `git worktree list | wc -l`.

G6 TREE AND PUSH — after C7: `git status --porcelain`, which must be empty;
 `git log --oneline -n 11`, which must show C7, C6, C5, C4, C3, C2, C1d, C1c, C1b, C1a and
 `a706a0701` in that order (one more line per repair commit); `git worktree list | wc -l`, which
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
SESSION 1 of feature F044, round 4, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 4, then the form entries' structured flows. State the open-findings count, 0, and the
operator-questions count, 0.
