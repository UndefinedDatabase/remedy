STEP F043 R4 — THE FIRST-RUN TOUR ON ONE OVERLAY ENGINE: TourFrame shared with the result tour, a spotlight per step, a once-per-browser record, a relaunch from the Terms panel, and R-1115 repaired

GOAL
Book round 3's PASS, register R-1115, record DECISION F043 D4, repair R-1115, and land T003's
first-run tour on `TourFrame`, the overlay engine the result tour now renders through too, against
the reviewer's tests and a render harness that mounts the real shell in a fresh browser.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE TESTS ARE THE REVIEWER'S AND THE CODE IS YOURS:
the test files and the render harness travel as payloads and are the acceptance, and you write
the production code against them and against S0 to S8 below. You never edit a payload; if one
looks wrong to you, STOP and report it. Read DECISION F043 D4 and R-1115 in the records diff before
you write code, and read whole, before you edit or call them, every file S0 to S8 name,
`apps/ui/src/api/resultTour.ts` (whose `tourNeighbours` and `tourProgress` S5 reuses), and the
tests that read the files you edit: `tests/ui_contracts/test_tour_overlay_contract.py`,
`tests/ui_contracts/test_term_panel_wiring.py`, `tests/ui_contracts/test_digest_mount.py` (it holds
`window.localStorage` to one occurrence in `RemedyShell.tsx`),
`tests/ui_contracts/test_main_layout_guard.py` and `tests/ui_contracts/test_raw_colour_ratchet.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f043-r4-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f043-r4/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f043-scratch/`      The reviewer's scripts; do not touch them.
  `.remedy-wt/f043-r4-worker/`    YOURS for logs and scripts; create it if absent. All are
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
command line. Never run npm or npx yourself: call `apps/ui/node_modules/.bin/tsc`, `.bin/vitest`,
`.bin/eslint` and `.bin/vite` by path. Never stop a process with `pkill -f`; the harness stops
what it started by pid.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f043-explanation-layer`, and `git log --oneline -1` must read `32854ea06`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f043-r4/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f043-r4-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 64 | 11523 | 761e83cb654710e08b93944adacae438bafa961b4de7bbe839d3b55cc02efa4c |
| tests.diff | 218 | 9874 | 853cf3932d36958760899c7a12962faea6da27acadae827554fe598417c08e6f |
| plan.md | 31 | 1102 | c02d3ca6ce875a2dd6ca7c11af2bae0ab90c4e49a34e4119b9d669ae28adc8ef |
| render_index.html | 11 | 243 | fbbc9e97d24286e7cb5f58ff30bd426b544cbb9129cadadd38f623a1603bfb97 |
| render_main.tsx | 47 | 2567 | cae86d09d8abebf044e8e62bd1874e985035dda46577c70a0e9ecc786459f89b |
| render_vite.config.mjs | 28 | 744 | 6c9d24558a507a827d445c793cd6203f7f0f24ac2659dcfe3cff96c20b7d1c6a |
| render_drive.mjs | 261 | 12148 | 3d89f87523de71abeb59e29a085fe603ce3f836369316a1c6cb7c15535f8b705 |
| render_measure.py | 186 | 6393 | 468d7ab95dc676c472e011bbeb378b82f011e7ed6ad25692bc2a76ad6f53ba4f |

`plan.md` is a REWRITE of `.agent/plan.md`. The two `.diff` files go on with `git apply`; the
reviewer generated them with `git diff HEAD` from a tree at `32854ea06`. `records.diff` appends
round 3's gate entry and the registration of R-1115 to `.agent/live_review.md` and DECISION F043 D4
to `.agent/decisions.md`. `tests.diff` edits `apps/ui/src/components/term/termPanel.test.ts`,
`tests/ui_contracts/test_term_panel_wiring.py` and `tests/ui_contracts/test_tour_overlay_contract.py`,
and adds the NEW FILE at `apps/ui/src/api/firstRunTour.test.ts`. The five `render_*` files are
the render harness; they are copied, never applied, and run from their copies.

THE SPECIFICATION — the tests are the acceptance; these clauses fix what they leave open. No
`@mui` import, no colour literal, only `--remedy-*` tokens in CSS.
S0 R-1115: in `apps/ui/src/components/term/Term.module.css`, `.tipDetail` gains `display: block;`
   as its first declaration. Nothing else in the file changes.
S1 `apps/ui/src/api/firstRunTour.ts`, NEW, pure (the storage is handed in), a header comment
   naming T5_F043 T003 and DECISION F043 D4. Exports the interface `FirstRunStep` (`readonly
   title`, `readonly body`, `readonly target`); `FIRST_RUN_STEPS`, EXACTLY the steps the test
   "words every step exactly as DECISION F043 D4 wrote it" pins, under a comment saying the sixth
   stands in for the command palette until one exists; `FIRST_RUN_TOUR_KEY =
   "remedy:first-run-tour"` and `FIRST_RUN_TOUR_SEEN = "seen"`; the type `FirstRunTourStorage =
   Pick<Storage, "getItem" | "setItem">`; `firstRunTourDue(storage)`, false for null, true only
   when `getItem` answers null for the key, false when it throws; `markFirstRunTourSeen(storage)`,
   writing the key and value, doing nothing for null and swallowing a throw; and
   `firstRunStepLabel(count, current)` = `` `Step ${current + 1} of ${count}` ``.
S2 `apps/ui/src/components/tour/TourFrame.tsx`, NEW, a header comment naming T5_F043 T003 and
   DECISION F043 D4, saying both tours render through it, and carrying the portal reason the old
   `TourOverlay.tsx` comment gave (R-1079). It imports `styles` from `"./TourOverlay.module.css"`
   and exports the interface `TourSpot` (`readonly left`, `top`, `width`, `height`, numbers),
   `TOUR_SPOT_PAD_PX = 6`, and `TourFrame({ label, ui, shown, spot = null, closeLabel, onClose,
   children })` with `ui: { readonly card: string; readonly backdrop: string }`. It returns
   `createPortal(..., document.body,)` of: while not `shown` and with no spot, `<div
   className={styles.backdrop} data-ui={ui.backdrop} />`; while not `shown` and with a spot,
   `<div className={styles.spot} data-ui={ui.backdrop} style={...}>` placed at the spot's left and
   top minus the pad, sized its width and height plus twice the pad; then `<section role="dialog"
   aria-label={label} className={styles.card} data-ui={ui.card} data-shown={...}
   data-spot={...}>`, `data-shown` "true" exactly when `shown`, `data-spot` "true" exactly when a
   spot is drawn, holding `<header className={styles.header}><h2>{label}</h2><button
   type="button" className={styles.close} onClick={onClose}>{closeLabel}</button></header>` and
   then `children`.
S3 `apps/ui/src/components/tour/TourOverlay.tsx`: drop the `createPortal` import and its block,
   import `TourFrame`, and return `<TourFrame label="Guided tour" ui={{ card: "tour-overlay",
   backdrop: "tour-backdrop" }} shown={!backdropVisible} closeLabel="Close tour"
   onClose={onClose}>` around exactly the three content blocks the section held after its header.
   The doc comment's portal paragraph becomes one sentence saying the backdrop, the card and the
   portal are `TourFrame`'s, the engine it shares with the first-run tour (DECISION F043 D4).
   Nothing else changes: the read, the stops, the step state and the Escape and arrow keys stay.
S4 `apps/ui/src/components/tour/TourOverlay.module.css`: the selector `.card[data-shown="true"] {`
   becomes the pair `.card[data-shown="true"],` and `.card[data-spot="true"] {` on two lines, the
   rule's declarations unchanged; directly after the line `.card[data-shown="true"] .actions {
   flex-wrap: wrap; }`, which stays, add `.card[data-spot="true"] .actions { flex-wrap: wrap; }`;
   then, under a comment naming DECISION F043 D4, a `.spot` rule: `position: fixed`, `z-index:
   calc(var(--remedy-z-overlay) - 1)`, `border-radius: var(--remedy-radius-lg)`, `box-shadow: 0 0
   0 2px var(--remedy-focus), 0 0 0 100vmax color-mix(in srgb, var(--remedy-ink-strong) 45%,
   transparent)` and `pointer-events: none`.
S5 `apps/ui/src/components/tour/FirstRunTour.tsx`, NEW, a header comment naming T5_F043 T003 and
   DECISION F043 D4. `FirstRunTour({ onClose })` keeps the current step, measures the spot of the
   element `[data-ui="<the step's target>"]` in a `useLayoutEffect` keyed by the target — after
   `scrollIntoView({ block: "nearest", inline: "nearest" })`, from `getBoundingClientRect()`,
   null when the element is absent or has no area — measures again on window `resize`, and closes
   on Escape and steps on the arrow keys through a window `keydown` listener. It renders
   `<TourFrame label="Welcome tour" ui={{ card: "first-run-tour", backdrop: "first-run-backdrop" }}
   shown={false} spot={<the spot>} closeLabel="Close tour" onClose={onClose}>` holding, in the
   result tour's classes, a `<p className={styles.stepLabel}>` with `firstRunStepLabel`, the
   `<ol className={styles.progress} data-ui="tour-progress">` of `tourProgress`, an `<h3
   className={styles.title}>` title, a `<p className={styles.body}>` body, and a `<div
   className={styles.actions}>` with, in order, "Skip tour" (closes), "Previous" (disabled on the
   first step) and "Finish" (closes) on the last step or "Next" elsewhere, using `tourNeighbours`.
   `FirstRunTourMount({ relaunch }: { relaunch: number })`, under a doc comment saying it is the
   tour's storage edge because the shell binds `window.localStorage` once, holds `const storage =
   useMemo(() => window.localStorage, [])`, opens at first when `firstRunTourDue(storage)`, opens
   again in an effect whenever `relaunch` is above 0 and changes, and renders the tour, or null
   while closed, with an `onClose` that calls `markFirstRunTourSeen(storage)` and then closes.
S6 `apps/ui/src/components/term/TermPanel.tsx`: an optional `onStartTour?: () => void` prop under
   a doc comment naming DECISION F043 D4, and, directly after the hint paragraph, `{onStartTour &&
   (<button type="button" className={styles.tour} onClick={onStartTour}>Take the tour</button>)}`
   laid out as you like; `TermPanel.module.css` gains `.tour` in the result tour's button style
   (32px high, `--remedy-radius-sm`, `--remedy-line-strong` border, `--remedy-blue-50` fill,
   `--remedy-blue-strong` text, 12px weight 600, `align-self: flex-start`) with a
   `:focus-visible` outline in `--remedy-focus`.
S7 The two unnamed targets: in `apps/ui/src/components/panels/ChatInput.tsx` the row becomes
   `<div className={styles.chatInputRow} data-ui="chat-input-row">`; in
   `apps/ui/src/components/panels/RightLivePanel.tsx` the Terms button gains `data-ui="terms-button"`
   directly before its `onClick`. Nothing else in either file changes.
S8 `apps/ui/src/components/shell/RemedyShell.tsx`: import `FirstRunTourMount` from
   `"../tour/FirstRunTour"`; directly after the `termsOpen` state, under a comment naming DECISION
   F043 D4, `const [tourRelaunch, setTourRelaunch] = useState(0);`; the Terms panel's mount becomes
   exactly `{termsOpen && (<TermPanel onClose={() => setTermsOpen(false)} onStartTour={() => {
   setTermsOpen(false); setTourRelaunch((count) => count + 1); }} />)}` on one line; and directly
   after it, under a comment naming F043 T003 and DECISION F043 D4, `<FirstRunTourMount
   relaunch={tourRelaunch} />`. `window.localStorage` stays at one occurrence.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C2, C3, C4, C5 and C6, in this order.

C1a — copy this block and the plan
  `.agent/authored/f043-r4-block.md` := this block and `.agent/authored/f043-r4-plan.md` :=
  plan.md, by `shutil.copyfile`.
  Subject: `F043 R4 C1a: copy round 4 block and plan into .agent/authored/`
  Its insertions are this block's line count plus 31. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the records and tests diffs
  `.agent/authored/f043-r4-records.diff` := records.diff and `.agent/authored/f043-r4-tests.diff`
  := tests.diff.
  Subject: `F043 R4 C1b: copy round 4 records and tests diffs into .agent/authored/`
  Expected insertions: 282.

C1c — copy the render page and driver
  `.agent/authored/f043-r4-render_main.tsx` and `.agent/authored/f043-r4-render_drive.mjs` :=
  render_main.tsx and render_drive.mjs.
  Subject: `F043 R4 C1c: copy the round 4 render page and driver into .agent/authored/`
  Expected insertions: 308.

C1d — copy the rest of the render harness
  `.agent/authored/f043-r4-render_index.html`, `.agent/authored/f043-r4-render_vite.config.mjs`
  and `.agent/authored/f043-r4-render_measure.py` := their payloads.
  Subject: `F043 R4 C1d: copy the rest of the round 4 render harness into .agent/authored/`
  Expected insertions: 225.

C2 — THE RECORDS, the round's first substantive commit: `git apply` records.diff, then rewrite
  `.agent/plan.md` := plan.md. This commit persists R-1115 before its repair lands.
  Subject: `F043 R4 C2: book F043 R3, register R-1115, record D4, advance the plan`
  Expected by `git show --numstat` (insertions and deletions): 44/0 .agent/decisions.md, 4/0 .agent/live_review.md, 11/10 .agent/plan.md.

C3 — THE CODE: S0 to S8 in one commit. If it would reach 500 insertions, split S0 to S4 into a
  first commit and S5 to S8 into a second, and say so.
  Subject: `F043 R4 C3: add the first-run tour on one overlay engine and repair R-1115`
  The reviewer's own version of S0 to S8 read 81/0 apps/ui/src/api/firstRunTour.ts, 1/1 apps/ui/src/components/panels/ChatInput.tsx, 1/1 apps/ui/src/components/panels/RightLivePanel.tsx, 8/1 apps/ui/src/components/shell/RemedyShell.tsx, 1/0 apps/ui/src/components/term/Term.module.css, 12/0 apps/ui/src/components/term/TermPanel.module.css, 5/1 apps/ui/src/components/term/TermPanel.tsx, 101/0 apps/ui/src/components/tour/FirstRunTour.tsx, 65/0 apps/ui/src/components/tour/TourFrame.tsx, 16/1 apps/ui/src/components/tour/TourOverlay.module.css, 7/19 apps/ui/src/components/tour/TourOverlay.tsx.

C4 — THE TESTS: `git apply` tests.diff.
  Subject: `F043 R4 C4: add the reviewer's tests for the first-run tour and the shared frame`
  Expected: 99/0 apps/ui/src/api/firstRunTour.test.ts, 6/0 apps/ui/src/components/term/termPanel.test.ts, 13/2 tests/ui_contracts/test_term_panel_wiring.py, 27/7 tests/ui_contracts/test_tour_overlay_contract.py.

C5 — THE TOOL: your mutation tool (G5) saved as `.agent/authored/f043-r4-mutations.py`.
  Subject: `F043 R4 C5: add the round 4 mutation tool`

C6 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F043 R4 C6: rewrite handoff for round 4`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; C3's own clause
   says what to do if it would not.
3. The round's whole tracked path set is: the `.agent/authored/f043-r4-*` copies and tool, the
   paths records.diff and tests.diff edit or add, `.agent/plan.md`, the files S0 to S8 name, and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 32854ea06` at the
   branch tip after C6. Do NOT touch `apps/ui/src/api/resultTour.ts`,
   `apps/ui/src/api/browserDigestPort.ts`, `apps/ui/src/components/lessons/`, `docs/`,
   `packages/`, `apps/cli/`, `apps/ui/package.json`, `.agent/context.md`, `.agent/prose_slips.md`,
   `.agent/candidates.md`, `.agent/operator_questions.md` or `README.md`. Write no `Done:` or
   `Landed:` line for R-1115: the reviewer authors its resolution at the next gate.
4. Every test the payloads carry passes against your code unedited, at C4, and the render
   harness reads every check passing at C4. A payload is never edited to pass; if your code
   cannot meet one, STOP and report it and the reason.
5. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. An EXISTING test
   that goes red is never edited to pass; report it and stop.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no branch switch, no branch deletion,
   no force-push, no `git stash`.
7. Leave every worktree already listed at your step 4, its branch, and every existing stash
   alone. The worktree G5 adds goes under `.remedy-wt/`, is removed as that gate's last action,
   and `git worktree list | wc -l` is reported afterwards.
8. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F043's belongs to its closure. Run no self-use job and no command that calls a provider.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C6 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f043-r4-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f043-r4/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS AND THE TESTS — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named, equals the reviewer's reading, printed from its
 simulation tree. Report each path beside the hash you read:
 | path | at | bytes | sha256 |
 |---|---|---|---|
 | .agent/decisions.md | C2 | 2532152 | a539b446f0d63911d4f87fa7cf2353a81ad180638e5dc3146e8189964616ad72 |
 | .agent/live_review.md | C2 | 127524 | 60cf0ce5f8425cc54daa97e3f298761742012f64c11217801dc9be630d771511 |
 | .agent/plan.md | C2 | 1102 | c02d3ca6ce875a2dd6ca7c11af2bae0ab90c4e49a34e4119b9d669ae28adc8ef |
 | apps/ui/src/api/firstRunTour.test.ts | C4 | 3905 | 18390a7abda3859eb2b58b49ce2f2eee8e1cfa7425845ab1896867d72083979a |
 | apps/ui/src/components/term/termPanel.test.ts | C4 | 2407 | e9683195fea83460ba1e0f7545f32ce52bb581a3cb224d2544fa4d3de18ac93b |
 | tests/ui_contracts/test_term_panel_wiring.py | C4 | 2501 | a549125669b730ba790f6e17c8cc7337f10e0ea5a5b5335e2dcd823a3aed8e86 |
 | tests/ui_contracts/test_tour_overlay_contract.py | C4 | 4678 | 7684d92f098f28ed56f1e430d1d8ce4b0f9ad317c0fcfaba932f334e5a4a46f9 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show <commit>:<path>` at
 `32854ea06` and at C2 (the reviewer read `[]` and `['R-1115']`); the ledger's last non-empty
 line at C2 begins `- R-1115 — Low, THE TERM TOOLTIP'S LIVE DETAIL RENDERS INLINE`; and
 `git diff --name-only <C1d> <C2>`, which must name exactly the C2 paths of the table above.

G3 THE CODE AND THE TESTS — at C5: `python3 -m ruff check .agent/authored/f043-r4-mutations.py
 .agent/authored/f043-r4-render_measure.py tests/ui_contracts/test_term_panel_wiring.py
 tests/ui_contracts/test_tour_overlay_contract.py`, and `apps/ui/node_modules/.bin/eslint src`
 run with `apps/ui` as its working directory, each with its real exit code. Report `git show
 --numstat <C3>` and the whole diff of C3. Then, in the primary checkout at C5, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_escalation.py tests/cli/test_plan_approval.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_live_review_rotation.py tests/regression/test_resource_safety.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 This selection runs `tsc --noEmit` (`test_typescript_compiles`), the whole vitest suite
 (`test_vitest_passes`) and eslint over `apps/ui/src` (`tests/ui_contracts/test_ui_lint.py`);
 name each of those nodes' outcomes. The reviewer ran the selection serially in its dry tree,
 which carries C2, this round's tests and the reviewer's own version of S0 to S8 but no
 `.agent/authored/f043-r4-*` copy and no built `apps/ui/dist`, with the primary's `node_modules`
 linked in, and read `1750 passed, 6 skipped` at real exit code 0, the same six skips round 3's
 dry tree printed, among them `tests/ui_contracts/test_responsive.py:555` for an unbuilt `dist`,
 which your checkout has built (round 3's primary run read `1749 passed, 5 skipped`); through the
 primary's binaries in the same tree the whole vitest suite read `2012 passed | 5 skipped` over
 103 files at exit 0. Report every `SKIPPED` line yours prints and the vitest counts of
 `src/api/firstRunTour.test.ts` and `src/components/term/termPanel.test.ts` (the reviewer's read
 7 and 5). Then `python3 -m apps.cli.main integrity check --json`, which must read all six checks
 `pass` at `fail_count` 0.

G4 THE RENDER — at C5, in the primary checkout:
 `python3 -B .agent/authored/f043-r4-render_measure.py /home/decodeux/Repos/remedy`, which builds
 the harness page over the checkout's own `apps/ui/src`, serves it on 127.0.0.1 port 9010, drives
 `/usr/bin/google-chrome --headless=new` with a fresh profile over CDP port 9380, stops both by pid
 and removes its work dir. Report its whole output from the first `PASS` or `FAIL` line on, and its
 exit code; it must print `RENDER: 9 of 9 checks pass` and exit 0. Read the screenshot it writes
 to `/home/decodeux/Repos/remedy/.remedy-wt/f043-r4-render-tour.png` and say in one sentence what
 it shows. The reviewer's own run over its version of S0 to S8 read 9 of 9.

G5 THE RED PROOFS — your tool `.agent/authored/f043-r4-mutations.py` takes a worktree path, and
 for each mutation below edits the named production file INSIDE that worktree (asserting its
 FROM text occurs exactly once there), runs the named check, restores the bytes, and prints one
 line per mutation: its label, the exit code, and the failed count or the harness's
 `RENDER: <n> of 9` reading. Vitest runs as `<primary>/apps/ui/node_modules/.bin/vitest run
 --root <worktree>/apps/ui --config <primary>/apps/ui/vitest.config.ts
 src/api/firstRunTour.test.ts src/components/term/termPanel.test.ts` with `<worktree>/apps/ui`
 as the working directory (checklist item 33); pytest as `python3 -B -m pytest -q -p
 no:cacheprovider tests/ui_contracts/test_tour_overlay_contract.py
 tests/ui_contracts/test_term_panel_wiring.py` with the worktree as the working directory and
 first on `PYTHONPATH`; the harness as `python3 -B
 <worktree>/.agent/authored/f043-r4-render_measure.py <worktree>`. The primary is
 `/home/decodeux/Repos/remedy`. The tool runs an unmutated control of all three checks first and
 last, reports `restored byte-identical: True` after each restore, and ends with
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  q1 `firstRunTourDue` answers true when the storage throws (`firstRunTour.ts`, vitest);
  q2 `markFirstRunTourSeen` writes "done" in place of the seen value (same);
  q3 the Terms panel offers "Take the tour" with no `onStartTour` (`TermPanel.tsx`, vitest);
  w1 the shell no longer mounts `FirstRunTourMount` (`RemedyShell.tsx`, pytest);
  w2 the result tour names its backdrop "tour-dim" (`TourOverlay.tsx`, pytest);
  h1 the tour's close no longer records it seen (`FirstRunTour.tsx`, the harness);
  h2 `TOUR_SPOT_PAD_PX` is 0 (`TourFrame.tsx`, the harness);
  h3 the frame never draws a spot (same);
  h4 `.tipDetail` loses `display: block` (`Term.module.css`, the harness: R-1115's red proof);
  h5 "Take the tour" leaves the Terms panel open (`RemedyShell.tsx`, the harness);
  h6 the mount ignores the relaunch count (`FirstRunTour.tsx`, the harness).
 Run it: `git worktree add --detach .remedy-wt/f043-r4-mut <C5>`, then in Python
 `os.symlink("/home/decodeux/Repos/remedy/apps/ui/node_modules",
 "/home/decodeux/Repos/remedy/.remedy-wt/f043-r4-mut/apps/ui/node_modules",
 target_is_directory=True)`, then
 `python3 -B .agent/authored/f043-r4-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f043-r4-mut`
 and report its whole output. The reviewer's own version of this probe, run against its version
 of S0 to S8, turned every one red with every control passing. EVERY mutation must exit
 non-zero; one that stays green is reported as green, never papered over, and you then STOP and
 report it. Then remove the symlink with `os.unlink`, `git worktree remove --force
 .remedy-wt/f043-r4-mut`, `git worktree prune`, and report `git worktree list | wc -l`.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`, which must show C6, C5, C4, C3, C2, C1d, C1c, C1b, C1a and
 `32854ea06` in that order (one more line if C3 was split); `git worktree list | wc -l`, which
 must equal your step 4 reading; the push's real outcome; and `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, which must be EMPTY. These readings go in your reply,
 since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (report what you measure for C3's files and for
C5), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate, and one for R-1115), the deviations —
including every clause of S0 to S8 you did not meet to the letter — and the next expected action.
Report what you ran, not what you expected to find. Your Session section reads SESSION 1 of
feature F043, round 4, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 4, then the end-to-end run over the real shell. State the open-findings count, 1 (R-1115,
repaired in this round and resolved only by the reviewer's text), and the operator-questions
count, 0.
