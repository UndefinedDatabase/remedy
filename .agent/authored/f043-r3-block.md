STEP F043 R3 — THE TOKEN AND COST TILES ONTO THE TERM, AND THE '?' PANEL: a live breakdown under the catalog's explanation, the tile's own tooltip deleted, and a searchable Terms panel opened by the question mark

GOAL
Book round 2's PASS, record DECISION F043 D3, move the token and cost tiles' breakdown into their
labels' terms, and add the '?' panel with its search, its Terms button and the place of every
entry, against the reviewer's tests and a render harness that mounts the real shell.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE TESTS ARE THE REVIEWER'S AND THE CODE IS YOURS:
the test files and the render harness travel as payloads and are the acceptance, and you write
the production code against them and against S1 to S8 below. You never edit a payload; if one
looks wrong to you, STOP and report it. Read DECISION F043 D3 in the records diff before you write
code, and read whole, before you edit or call them, every file S1 to S8 name, the learning
overlay `apps/ui/src/components/lessons/LessonsOverlay.tsx` with its sheet (the style S6 follows),
and the tests that read the files you edit: `tests/ui_contracts/test_cost_metric_render.py` (it
pins the breakdowns' two test ids and the tokens caption line), `tests/ui_contracts/test_design_drift.py`,
`tests/ui_contracts/test_raw_colour_ratchet.py`, `tests/ui_contracts/test_tour_overlay_contract.py`
and `tests/ui_contracts/test_timeline_scrub_wiring.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f043-r3-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f043-r3/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f043-scratch/`      The reviewer's scripts; do not touch them.
  `.remedy-wt/f043-r3-worker/`    YOURS for logs and scripts; create it if absent. All are
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
   `feature/f043-explanation-layer`, and `git log --oneline -1` must read `03f77c7f9`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f043-r3/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f043-r3-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 60 | 9572 | d7aa02b9efadf2de2a77de4902f49a3aa2dc17f67cf30145dff018e944cff1a6 |
| tests.diff | 362 | 16276 | 1415236547a3162f47871197cda55afa2ec54ac9b124cc5a146866c66970e432 |
| plan.md | 30 | 1121 | fbc4cb2858bc623bb6f0675f5deafa5dde98af0c450f2e2bce70c0edd55c565a |
| render_index.html | 11 | 243 | ff814916d0fa8a75b278d1ddd77bc5d426b83c1b5e4a7239161a11d4e38eeae1 |
| render_main.tsx | 47 | 2567 | a21867e3f5abbdf6353d51fc580bfa68bb35922ea7abd8f0e4a20fbddeabcd37 |
| render_vite.config.mjs | 28 | 744 | 6c9d24558a507a827d445c793cd6203f7f0f24ac2659dcfe3cff96c20b7d1c6a |
| render_drive.mjs | 218 | 9889 | db21658694cf42b8ce6ea34729e715933ab9201593376a0edaa5cf5386fbef8f |
| render_measure.py | 186 | 6393 | 445b9ab6767000cadbf3aea56c4f3a6cb39c7a7778d9afa31c603856fc9f6ddf |

`plan.md` is a REWRITE of `.agent/plan.md`. The two `.diff` files go on with `git apply`; the
reviewer generated them with `git diff HEAD` from a tree at `03f77c7f9`. `records.diff` appends
round 2's gate entry to `.agent/live_review.md` and DECISION F043 D3 to `.agent/decisions.md`.
`tests.diff` edits `apps/ui/src/api/terminology.test.ts`,
`apps/ui/src/components/term/termAudit.test.ts` and `tests/ui_contracts/test_design_drift.py`, and
adds the NEW FILE at `apps/ui/src/api/termSearch.test.ts`, the NEW FILE at
`apps/ui/src/components/term/termPanel.test.ts` and the NEW FILE at
`tests/ui_contracts/test_term_panel_wiring.py`. The five `render_*` files are the render harness;
they are copied, never applied, and run from their copies.

THE SPECIFICATION — the tests are the acceptance; these clauses fix what they leave open. No
`@mui` import, no colour literal, only `--remedy-*` tokens in CSS.
S1 `apps/ui/src/api/terminology.ts`: the catalog equals EXACTLY what the test "words every entry
   exactly as DECISIONS F043 D1 to D3 wrote it" pins: two entries after `metric.proof`,
   `metric.tokens` then `metric.cost`, and the key `blocked.task` renamed `task.blocked` with its
   entry unchanged.
S2 `apps/ui/src/components/term/Term.tsx`: an optional fourth prop `detail?: ReactNode` under a
   doc comment naming DECISION F043 D3 (live figures under the catalog's explanation; the
   explanation stays the catalog's). The tooltip renders, after the body span and only when
   `detail !== undefined`, `<span className={styles.tipDetail}>{detail}</span>`. `Term.module.css`
   gains `.tipDetail`: a block with 6px top margin, 6px top padding and a 1px solid
   `--remedy-line` top border.
S3 `apps/ui/src/components/metrics/TopMetricsBar.tsx`: `METRIC_TERMS` also maps `tokens` and
   `cost` to `metric.tokens` and `metric.cost`, its comment naming DECISIONS F043 D1 to D3; a
   function `metricDetail(m: RemedyMetric): ReactNode` answers, for a tile with `m.cost`,
   `<span className={styles.tooltipRows} data-testid="cost-tooltip">` holding one
   `<span className={styles.costTooltipRow}>` per line of `m.cost.tooltip`, keyed by the line;
   otherwise, for a tile with `m.tooltip`, `<span className={styles.tooltipRows}
   data-testid="token-tooltip">` holding one `<span className={styles.tooltipRow}>` per role, each
   `<span>{role}</span><span>{formatTokenCount(count)}</span>`; otherwise `undefined`. The label
   becomes `<Term term={METRIC_TERMS[m.key]} detail={metricDetail(m)}>{m.label}</Term>` for a key
   the map holds and `m.label` otherwise. DELETE the tile's own tooltip: the `useState` import and
   `tooltipKey` state, `hasTooltip`, the article's `tabIndex` and its four pointer and focus
   handlers, and the two `role="tooltip"` blocks. Nothing else in the file changes. In
   `TopMetricsBar.module.css` delete the `.tooltip` rule, add `.tooltipRows { display: block; }`
   under a one-line comment naming DECISION F043 D3, and give `.costTooltipRow` `display: block`.
S4 `apps/ui/src/components/panels/TaskChecklistCard.tsx`: `stateTerm` answers `task.blocked`
   where it answered `blocked.task`. Nothing else changes.
S5 `apps/ui/src/api/termSearch.ts`, NEW, pure, a header comment naming T5_F043 T003 and DECISION
   F043 D3. Exports the interface `TermListing` (`readonly key`, `readonly entry: TermEntry`);
   `searchTermEntries(catalog, query)`, keeping the entries whose lower-cased title and body,
   joined by a space, hold every white-space-separated word of the lower-cased query, sorted by
   lower-cased title and then by key; `TERM_PLACES`, exactly `agent` "Right panel", `graph`
   "Graph", `metric` "Metrics bar", `panel` "Right panel", `phase` "Timeline", `status` "Live
   status" and `task` "Task list"; `termPlace(key)`, the place of the key's first dotted word by an
   OWN key of `TERM_PLACES`, or ""; the interface `KeyTarget` (`readonly tagName?`, `readonly
   isContentEditable?`); and `isHelpShortcut(key, target)`, true only for `"?"` with a null target
   or one that is not content-editable and whose upper-cased tag is none of INPUT, TEXTAREA and
   SELECT.
S6 `apps/ui/src/components/term/TermPanel.tsx` and `TermPanel.module.css`, NEW, a header comment
   naming T5_F043 T003 and DECISION F043 D3 and why the rows carry `data-term-entry` and never
   `data-term`. Exports `TERM_PANEL_LABEL = "Terms"`, `TERM_SEARCH_LABEL = "Search the terms"`,
   `termPanelEmptyLine(query)` = `` `No term matches “${query.trim()}”.` `` and
   `TermPanel({ onClose })`. It renders `<section className={styles.panel} role="dialog"
   aria-label={TERM_PANEL_LABEL} data-ui="term-panel">` holding a header with an `<h2>` reading
   the label and a `Close terms` button calling `onClose`; a `<p>` reading "What the cockpit's
   words mean. Press ? anywhere to open this list."; an `<input type="search">` with
   `aria-label={TERM_SEARCH_LABEL}`, `placeholder="Search"`, the query as its value and
   `autoFocus`; then, for `searchTermEntries(TERM_CATALOG, query)`, either a `<p>` with the empty
   line or a `<dl>` holding one `<div key={key} className={styles.item} data-term-entry={key}>`
   per row with exactly `<dt>{title}</dt><dd className={styles.place}>{termPlace(key)}</dd><dd>{body}</dd>`.
   A window `keydown` listener, added and removed in an effect keyed by `onClose`, calls it on
   Escape. The sheet follows the learning overlay's: fixed at 24px from the top, right and bottom,
   `width: min(440px, calc(100vw - 48px))`, `z-index: var(--remedy-z-overlay)`, the same glass,
   border, radius, shadow and blur, the same header, close and quiet-text styles, a 36px search
   field with a `:focus-visible` outline in `--remedy-focus`, a scrolling list, the title in 13px
   bold `--remedy-ink-strong`, the body in 12px `--remedy-ink`, the place in 11px `--remedy-muted`.
S7 `apps/ui/src/components/shell/RemedyShell.tsx`: import `TermPanel` and `isHelpShortcut`; after
   the results panel's state, under a comment naming F043 T003 and DECISION F043 D3, a
   `termsOpen` state and an effect with no dependencies that adds a window `keydown` listener
   `onKey` — `const target = event.target instanceof HTMLElement ? event.target : null;` then
   `if (isHelpShortcut(event.key, target)) {` prevent the default and open — written as
   `window.addEventListener("keydown", onKey);` and removed in its cleanup as
   `window.removeEventListener("keydown", onKey);`; the `<RightLivePanel` line gains
   `onOpenTerms={() => setTermsOpen(true)}`; and directly after the results panel's mount, under a
   comment naming DECISION F043 D3, `{termsOpen && (<TermPanel onClose={() => setTermsOpen(false)} />)}`.
S8 `apps/ui/src/components/panels/RightLivePanel.tsx`: an optional prop `onOpenTerms?: () =>
   void`, and after the Results button, under a comment naming F043 T003 and DECISION F043 D3,
   `{onOpenTerms && (<button type="button" className={styles.advancedToggle} onClick={onOpenTerms} aria-keyshortcuts="?">Terms</button>)}`.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C2, C3, C4, C5 and C6, in this order.

C1a — copy this block and the plan
  `.agent/authored/f043-r3-block.md` := this block and `.agent/authored/f043-r3-plan.md` :=
  plan.md, by `shutil.copyfile`.
  Subject: `F043 R3 C1a: copy round 3 block and plan into .agent/authored/`
  Its insertions are this block's line count plus 30. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the records and tests diffs
  `.agent/authored/f043-r3-records.diff` := records.diff and `.agent/authored/f043-r3-tests.diff`
  := tests.diff.
  Subject: `F043 R3 C1b: copy round 3 records and tests diffs into .agent/authored/`
  Expected insertions: 422.

C1c — copy the render page and driver
  `.agent/authored/f043-r3-render_main.tsx` and `.agent/authored/f043-r3-render_drive.mjs` :=
  render_main.tsx and render_drive.mjs.
  Subject: `F043 R3 C1c: copy the round 3 render page and driver into .agent/authored/`
  Expected insertions: 265.

C1d — copy the rest of the render harness
  `.agent/authored/f043-r3-render_index.html`, `.agent/authored/f043-r3-render_vite.config.mjs`
  and `.agent/authored/f043-r3-render_measure.py` := their payloads.
  Subject: `F043 R3 C1d: copy the rest of the round 3 render harness into .agent/authored/`
  Expected insertions: 225.

C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F043 R3 C2: book F043 R2, record D3, advance the plan`
  Expected by `git show --numstat` (insertions and deletions): 42/0 .agent/decisions.md, 2/0 .agent/live_review.md, 8/11 .agent/plan.md.

C3 — THE CODE: S1 to S8 in one commit. If it would reach 500 insertions, split S1 to S4 into a
  first commit and S5 to S8 into a second, and say so.
  Subject: `F043 R3 C3: show the tiles' breakdown in their terms and open a searchable Terms panel on ?`
  The reviewer's own version of S1 to S8 read 62/0 apps/ui/src/api/termSearch.ts, 13/1 apps/ui/src/api/terminology.ts, 3/14 apps/ui/src/components/metrics/TopMetricsBar.module.css, 36/31 apps/ui/src/components/metrics/TopMetricsBar.tsx, 4/1 apps/ui/src/components/panels/RightLivePanel.tsx, 1/1 apps/ui/src/components/panels/TaskChecklistCard.tsx, 22/1 apps/ui/src/components/shell/RemedyShell.tsx, 8/0 apps/ui/src/components/term/Term.module.css, 6/1 apps/ui/src/components/term/Term.tsx, 45/0 apps/ui/src/components/term/TermPanel.module.css, 63/0 apps/ui/src/components/term/TermPanel.tsx.

C4 — THE TESTS: `git apply` tests.diff.
  Subject: `F043 R3 C4: add the reviewer's tests for the tiles' terms, the search and the Terms panel`
  Expected: 82/0 apps/ui/src/api/termSearch.test.ts, 28/3 apps/ui/src/api/terminology.test.ts, 12/7 apps/ui/src/components/term/termAudit.test.ts, 41/0 apps/ui/src/components/term/termPanel.test.ts, 4/1 tests/ui_contracts/test_design_drift.py, 44/0 tests/ui_contracts/test_term_panel_wiring.py.

C5 — THE TOOL: your mutation tool (G5) saved as `.agent/authored/f043-r3-mutations.py`.
  Subject: `F043 R3 C5: add the round 3 mutation tool`

C6 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F043 R3 C6: rewrite handoff for round 3`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; C3's own clause
   says what to do if it would not.
3. The round's whole tracked path set is: the `.agent/authored/f043-r3-*` copies and tool, the
   paths records.diff and tests.diff edit or add, `.agent/plan.md`, the files S1 to S8 name, and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 03f77c7f9` at the
   branch tip after C6. Do NOT touch `apps/ui/src/components/tour/`,
   `apps/ui/src/components/lessons/`, `apps/ui/src/api/costMetric.ts`,
   `apps/ui/src/api/remedyApi.ts`, `tests/ui_contracts/test_cost_metric_render.py`, `docs/`,
   `packages/`, `apps/cli/`, `apps/ui/package.json`, `.agent/context.md`, `.agent/prose_slips.md`,
   `.agent/candidates.md`, `.agent/operator_questions.md` or `README.md`.
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
 against the PAYLOADS table. Then compare each `.agent/authored/f043-r3-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f043-r3/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS AND THE TESTS — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named, equals the reviewer's reading, printed from its
 simulation tree. Report each path beside the hash you read:
 | path | at | bytes | sha256 |
 |---|---|---|---|
 | .agent/decisions.md | C2 | 2528261 | 36b9c53f3acc94ec280342802bbf3c65d3aea3fb11b7b22f02c5f84a0358e4a0 |
 | .agent/live_review.md | C2 | 124439 | b72cda64aaada4b0fd1ffb57b3a778afa8a44ec947ad46ec912bc7178763f845 |
 | .agent/plan.md | C2 | 1121 | fbc4cb2858bc623bb6f0675f5deafa5dde98af0c450f2e2bce70c0edd55c565a |
 | apps/ui/src/api/termSearch.test.ts | C4 | 3665 | e855c0db980afa8c09981dffa98a8a8e6bc81eb8ae497f4ddd833a53fa9b5140 |
 | apps/ui/src/api/terminology.test.ts | C4 | 15417 | 6f079c59b1731141099e266a2c942b1ff3e85080a1044031ae24a652738572c8 |
 | apps/ui/src/components/term/termAudit.test.ts | C4 | 12148 | 06f56b3ef84f82a4dd93a30703dbcf8210c46c1f229172867d14597ac5e61624 |
 | apps/ui/src/components/term/termPanel.test.ts | C4 | 2050 | 68a17877efcc75b2c6a3efd1ca92ac6d165302ff032db53bd917f3f7fb6038ff |
 | tests/ui_contracts/test_design_drift.py | C4 | 14465 | e01784858200b0fbd99f47b04d393e8f5bae7108ff3b0095a3d3c4637db21cfc |
 | tests/ui_contracts/test_term_panel_wiring.py | C4 | 1838 | 57054b5a97dda069554a27be39c885705e05467234d27c80faae3467ddf3f6ca |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show <commit>:<path>` at
 C2 (the reviewer read `[]`); the ledger's last non-empty line at C2 begins `Gate: F043 R2 — the
 F043 round 2 entry`; and `git diff --name-only <C1d> <C2>`, which must name exactly the C2 paths
 of the table above.

G3 THE CODE AND THE TESTS — at C5: `python3 -m ruff check .agent/authored/f043-r3-mutations.py
 .agent/authored/f043-r3-render_measure.py tests/ui_contracts/test_term_panel_wiring.py
 tests/ui_contracts/test_design_drift.py`, and `apps/ui/node_modules/.bin/eslint src` run with
 `apps/ui` as its working directory, each with its real exit code. Report `git show --numstat
 <C3>` and the whole diff of C3. Then, in the primary checkout at C5, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_escalation.py tests/cli/test_plan_approval.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_live_review_rotation.py tests/regression/test_resource_safety.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 This selection runs `tsc --noEmit` (`test_typescript_compiles`), the whole vitest suite
 (`test_vitest_passes`) and eslint over `apps/ui/src` (`tests/ui_contracts/test_ui_lint.py`);
 name each of those nodes' outcomes. The reviewer ran the selection serially in its dry tree,
 which carries C2, this round's tests and the reviewer's own version of S1 to S8 but no
 `.agent/authored/f043-r3-*` copy and no built `apps/ui/dist`, with the primary's `node_modules`
 linked in, and read `1748 passed, 6 skipped` at real exit code 0, the same six skips round 2's
 dry tree printed, among them `tests/ui_contracts/test_responsive.py:555` for an unbuilt `dist`,
 which your checkout has built (round 2's primary run read `1746 passed, 5 skipped`); through the
 primary's binaries in the same tree the whole vitest suite read `2004 passed | 5 skipped` over
 102 files at exit 0. Report every `SKIPPED` line yours prints and the vitest counts of
 `src/api/terminology.test.ts`, `src/api/terminologyAudit.test.ts`, `src/api/termSearch.test.ts`,
 `src/components/term/termAudit.test.ts` and `src/components/term/termPanel.test.ts` (the
 reviewer's read 13, 8, 11, 12 and 4). Then `python3 -m apps.cli.main integrity check --json`,
 which must read all six checks `pass` at `fail_count` 0.

G4 THE RENDER — at C5, in the primary checkout:
 `python3 -B .agent/authored/f043-r3-render_measure.py /home/decodeux/Repos/remedy`, which builds
 the harness page over the checkout's own `apps/ui/src`, serves it on 127.0.0.1 port 9010, drives
 `/usr/bin/google-chrome --headless=new` over CDP port 9380, stops both by pid and removes its work
 dir. Report its whole output from the first `PASS` or `FAIL` line on, and its exit code; it must
 print `RENDER: 10 of 10 checks pass` and exit 0. Read the screenshot it writes to
 `/home/decodeux/Repos/remedy/.remedy-wt/f043-r3-render-panel.png` and say in one sentence what
 it shows. The reviewer's own run over its version of S1 to S8 read 10 of 10.

G5 THE RED PROOFS — your tool `.agent/authored/f043-r3-mutations.py` takes a worktree path, and
 for each mutation below edits the named production file INSIDE that worktree (asserting its
 FROM text occurs exactly once there), runs the named check, restores the bytes, and prints one
 line per mutation: its label, the exit code, and the failed count or the harness's
 `RENDER: <n> of 10` reading. Vitest runs as `<primary>/apps/ui/node_modules/.bin/vitest run
 --root <worktree>/apps/ui --config <primary>/apps/ui/vitest.config.ts` over the five test files
 G3 names, with `<worktree>/apps/ui` as the working directory (checklist item 33); pytest as
 `python3 -B -m pytest -q -p no:cacheprovider tests/ui_contracts/test_term_panel_wiring.py` with
 the worktree as the working directory and first on `PYTHONPATH`; the harness as
 `python3 -B <worktree>/.agent/authored/f043-r3-render_measure.py <worktree>`. The primary is
 `/home/decodeux/Repos/remedy`. The tool runs an unmutated control of all three checks first and
 last, reports `restored byte-identical: True` after each restore, and ends with
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  p1 `searchTermEntries` breaks a tie of titles by nothing instead of by key (`termSearch.ts`,
     vitest);
  p2 the search also reads the key (same);
  p3 `isHelpShortcut` opens inside an INPUT (same);
  p4 `termPlace` reads `TERM_PLACES[family] ?? ""`, without the own-key test (same);
  p5 the panel's rows carry `data-term` in place of `data-term-entry` (`TermPanel.tsx`, vitest);
  p6 `METRIC_TERMS` loses `cost` (`TopMetricsBar.tsx`, vitest);
  w1 the shell never adds its `keydown` listener (`RemedyShell.tsx`, the wiring test);
  h1 the term's tooltip no longer renders its `detail` (`Term.tsx`, the harness);
  h2 the panel closes on "Esc" instead of "Escape" (`TermPanel.tsx`, the harness);
  h3 the search field loses `autoFocus` (same);
  h4 p3's change, read by the harness instead (`termSearch.ts`, the harness).
 Run it: `git worktree add --detach .remedy-wt/f043-r3-mut <C5>`, then in Python
 `os.symlink("/home/decodeux/Repos/remedy/apps/ui/node_modules",
 "/home/decodeux/Repos/remedy/.remedy-wt/f043-r3-mut/apps/ui/node_modules",
 target_is_directory=True)`, then
 `python3 -B .agent/authored/f043-r3-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f043-r3-mut`
 and report its whole output. The reviewer's own version of this probe, run against its version
 of S1 to S8, turned every one red with every control passing. EVERY mutation must exit
 non-zero; one that stays green is reported as green, never papered over, and you then STOP and
 report it. Then remove the symlink with `os.unlink`, `git worktree remove --force
 .remedy-wt/f043-r3-mut`, `git worktree prune`, and report `git worktree list | wc -l`.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`, which must show C6, C5, C4, C3, C2, C1d, C1c, C1b, C1a and
 `03f77c7f9` in that order (one more line if C3 was split); `git worktree list | wc -l`, which
 must equal your step 4 reading; the push's real outcome; and `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, which must be EMPTY. These readings go in your reply,
 since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (report what you measure for C3's files and for
C5), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Report what you ran, not what you expected to find. Your Session section reads SESSION 1
of feature F043, round 3, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 3, then the first-run tour on an overlay card shared with the result tour. State the
open-findings count, 0, and the operator-questions count, 0.
