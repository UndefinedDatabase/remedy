STEP F043 R2 — THE TERMS OF THE RIGHT PANEL, THE PLAIN METRICS AND THE SCRUBBED BADGE: more catalog entries on the real cards, a term inside a button that takes no focus, and two descendant rules of the panel's sheet narrowed

GOAL
Book round 1's PASS, record DECISION F043 D2, and carry the explanation layer to the right panel's
cards, the six plain metrics' labels and the graph stage's SCRUBBED badge against the reviewer's
tests and a render harness that proves them in a real browser.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE TESTS ARE THE REVIEWER'S AND THE CODE IS YOURS:
the test files and the render harness travel as payloads and are the acceptance, and you write
the production code against them and against S1 to S9 below. You never edit a payload; if one
looks wrong to you, STOP and report it. Read DECISION F043 D2 in the records diff before you write
code, and read whole, before you edit or call them, every file S1 to S9 name, and the tests that
read those files: `tests/ui_contracts/test_timeline_scrub_wiring.py` (it slices the SCRUBBED
banner out of `BrainGraphStage.tsx` and needs `>SCRUBBED<` inside it),
`tests/ui_contracts/test_apply_state_partial.py`, `tests/ui_contracts/test_design_drift.py` and
`tests/ui_contracts/test_raw_colour_ratchet.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f043-r2-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f043-r2/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f043-scratch/`      The reviewer's scripts; do not touch them.
  `.remedy-wt/f043-r2-worker/`    YOURS for logs and scripts; create it if absent. All are
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
   `feature/f043-explanation-layer`, and `git log --oneline -1` must read `15331eb0b`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f043-r2/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f043-r2-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 67 | 10261 | 331d5a5911967cfce54167b58cf82142397e499afff3cab44193878c5f105208 |
| tests.diff | 385 | 17893 | 1e760003a803add1588f915e9e3790b71812ea2ab8bbd279f6e585954cf01508 |
| plan.md | 33 | 1296 | b86e126b4d6c27ef2303ff73d79f1e434e7a7717a2532ed7a598de8a5bb8251c |
| render_index.html | 11 | 243 | f500fc2e4e8e14f5bbd9d8e0b85f418f9232f2048154728e951495e3e65d0584 |
| render_main.tsx | 87 | 4180 | 8be109699f8fdcee24a928f8476c782de3995f4d6b6a718b3e46f8b9318d3f8c |
| render_vite.config.mjs | 28 | 744 | 6c9d24558a507a827d445c793cd6203f7f0f24ac2659dcfe3cff96c20b7d1c6a |
| render_drive.mjs | 200 | 9523 | 0555ab124c0155c81994c2b83c432532bdc3c000bfe92c1f77d8890973d8ac0c |
| render_measure.py | 186 | 6393 | 4fd6da7d1902fc4a827dc660bb5aef7eff52bc0d36721e431845a18acba9a8b6 |

`plan.md` is a REWRITE of `.agent/plan.md`. The two `.diff` files go on with `git apply`; the
reviewer generated them with `git diff HEAD` from a tree at `15331eb0b`. `records.diff` appends
round 1's gate entry to `.agent/live_review.md` and DECISION F043 D2 to `.agent/decisions.md`.
`tests.diff` edits `apps/ui/src/api/terminology.test.ts` and
`apps/ui/src/components/term/termAudit.test.ts`. The five `render_*` files are the render harness;
they are copied, never applied, and run from their copies.

THE SPECIFICATION — the tests are the acceptance; these clauses fix what they leave open. No
`@mui` import, no colour literal, and in every file that gains a `Term` one import line,
`import { Term } from "../term/Term";`, placed directly above that file's `import styles` line.
S1 `apps/ui/src/api/terminology.ts`: the catalog gains EXACTLY the entries the test "words every
   entry exactly as DECISIONS F043 D1 and D2 wrote it" pins beyond round 1's, written after
   `phase.finalized` in the order `metric.open`, `metric.planned`, `metric.done`,
   `metric.progress`, `metric.tests`, `metric.proof`, `task.done`, `task.in_progress`,
   `blocked.task`, `task.planned`, `task.partially_applied`, `panel.tasks`, `panel.decisions`,
   `panel.activity`, `panel.agent_now`, `agent.live`, `graph.scrubbed`. Nothing else changes.
S2 `apps/ui/src/components/term/Term.tsx`: `Term` takes a third, optional prop `insideControl`
   (boolean, default false) under a doc comment naming DECISION F043 D2 and why: a term inside a
   button or another control takes no focus of its own, and the '?' panel lists every term for
   the keyboard. With it true the span carries no `tabIndex` and no focus or blur handler; hover,
   Escape and everything else are unchanged.
S3 `apps/ui/src/components/metrics/TopMetricsBar.tsx`: a module constant `METRIC_TERMS:
   Readonly<Record<string, string>>` mapping exactly `open`, `planned`, `done`, `progress`,
   `tests` and `proof` to `metric.<key>`, under a comment naming DECISIONS F043 D1 and D2 and
   saying the token and cost tiles are absent because their own breakdown tooltip opens on the
   whole tile until the next round moves them onto the term's tooltip; the label's text becomes
   `{METRIC_TERMS[m.key] ? <Term term={METRIC_TERMS[m.key]}>{m.label}</Term> : m.label}`.
   Nothing else changes, the tile's own tooltip included.
S4 `apps/ui/src/components/panels/TaskChecklistCard.tsx`: a function `stateTerm(task)` directly
   after `stateText`, reading the same conditions in the same order and answering
   `task.partially_applied`, `task.done`, `task.in_progress`, `blocked.task` and `task.planned`,
   under a comment naming DECISION F043 D2; both `<h2>Tasks</h2>` become
   `<h2><Term term="panel.tasks">Tasks</Term></h2>`; and the row's state word becomes
   `<span className={styles.taskState}><Term term={stateTerm(row)} insideControl>{stateText(row)}</Term></span>`.
S5 `apps/ui/src/components/panels/DecisionInboxCard.tsx`: `<h2>Decision inbox</h2>` becomes
   `<h2><Term term="panel.decisions">Decision inbox</Term></h2>`.
S6 `apps/ui/src/components/panels/ActivityFeedCard.tsx`: both `<h2>Activity</h2>` become
   `<h2><Term term="panel.activity">Activity</Term></h2>`.
S7 `apps/ui/src/components/panels/AgentNowCard.tsx`: `<h2>Agent is doing now</h2>` becomes
   `<h2><Term term="panel.agent_now">Agent is doing now</Term></h2>`, and the Live badge becomes
   `<span className={styles.liveSmall}><span /> <Term term="agent.live">Live</Term></span>`.
S8 `apps/ui/src/components/graph/BrainGraphStage.tsx`: the badge becomes
   `<span className={styles.scrubBadge}><Term term="graph.scrubbed">SCRUBBED</Term></span>`, so
   the banner still holds `>SCRUBBED<`. Its `Term` import goes directly above `import styles`.
S9 `apps/ui/src/components/panels/RightLivePanel.module.css`: `.cardHeader span {` becomes
   `.cardHeader > span {` under a one-line comment naming F043 and DECISION F043 D2 (a heading's
   term keeps the heading's own type), and `.liveSmall span {` becomes
   `.liveSmall > span:first-child {` under a one-line comment saying the badge's dot is its first
   span and the word after it is the badge's term. The declarations are unchanged.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C2, C3, C4, C5 and C6, in this order.

C1a — copy this block and the plan
  `.agent/authored/f043-r2-block.md` := this block and `.agent/authored/f043-r2-plan.md` :=
  plan.md, by `shutil.copyfile`.
  Subject: `F043 R2 C1a: copy round 2 block and plan into .agent/authored/`
  Its insertions are this block's line count plus 33. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the records and tests diffs
  `.agent/authored/f043-r2-records.diff` := records.diff and `.agent/authored/f043-r2-tests.diff`
  := tests.diff.
  Subject: `F043 R2 C1b: copy round 2 records and tests diffs into .agent/authored/`
  Expected insertions: 452.

C1c — copy the render page and driver
  `.agent/authored/f043-r2-render_main.tsx` and `.agent/authored/f043-r2-render_drive.mjs` :=
  render_main.tsx and render_drive.mjs.
  Subject: `F043 R2 C1c: copy the round 2 render page and driver into .agent/authored/`
  Expected insertions: 287.

C1d — copy the rest of the render harness
  `.agent/authored/f043-r2-render_index.html`, `.agent/authored/f043-r2-render_vite.config.mjs`
  and `.agent/authored/f043-r2-render_measure.py` := their payloads.
  Subject: `F043 R2 C1d: copy the rest of the round 2 render harness into .agent/authored/`
  Expected insertions: 225.

C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F043 R2 C2: book F043 R1, record D2, advance the plan`
  Expected by `git show --numstat` (insertions and deletions): 49/0 .agent/decisions.md, 2/0 .agent/live_review.md, 8/9 .agent/plan.md.

C3 — THE CODE: S1 to S9 in one commit. If it would reach 500 insertions, split S1 and S2 into a
  first commit and S3 to S9 into a second, and say so.
  Subject: `F043 R2 C3: explain the right panel's cards, the plain metrics and the SCRUBBED badge`
  The reviewer's own version of S1 to S9 read 102/0 apps/ui/src/api/terminology.ts, 2/1 apps/ui/src/components/graph/BrainGraphStage.tsx, 14/1 apps/ui/src/components/metrics/TopMetricsBar.tsx, 3/2 apps/ui/src/components/panels/ActivityFeedCard.tsx, 3/2 apps/ui/src/components/panels/AgentNowCard.tsx, 2/1 apps/ui/src/components/panels/DecisionInboxCard.tsx, 5/2 apps/ui/src/components/panels/RightLivePanel.module.css, 14/3 apps/ui/src/components/panels/TaskChecklistCard.tsx, 12/4 apps/ui/src/components/term/Term.tsx.

C4 — THE TESTS: `git apply` tests.diff.
  Subject: `F043 R2 C4: add the reviewer's tests for the panel's, the metrics' and the stage's terms`
  Expected: 129/2 apps/ui/src/api/terminology.test.ts, 146/3 apps/ui/src/components/term/termAudit.test.ts.

C5 — THE TOOL: your mutation tool (G5) saved as `.agent/authored/f043-r2-mutations.py`.
  Subject: `F043 R2 C5: add the round 2 mutation tool`

C6 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F043 R2 C6: rewrite handoff for round 2`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; C3's own clause
   says what to do if it would not.
3. The round's whole tracked path set is: the `.agent/authored/f043-r2-*` copies and tool, the
   paths records.diff and tests.diff edit, `.agent/plan.md`, the files S1 to S9 name, and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 15331eb0b` at the
   branch tip after C6. Do NOT touch `apps/ui/src/components/tour/`,
   `apps/ui/src/components/shell/RemedyShell.tsx`, `apps/ui/src/components/panels/RightLivePanel.tsx`,
   `apps/ui/src/api/remedyApi.ts`, `apps/ui/src/api/decisionOrder.ts`,
   `apps/ui/src/components/metrics/TopMetricsBar.module.css`, `docs/`, `packages/`, `apps/cli/`,
   `apps/ui/package.json`, `.agent/context.md`, `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md` or `README.md`.
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
 against the PAYLOADS table. Then compare each `.agent/authored/f043-r2-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f043-r2/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS AND THE TESTS — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named, equals the reviewer's reading, printed from its
 simulation tree. Report each path beside the hash you read:
 | path | at | bytes | sha256 |
 |---|---|---|---|
 | .agent/decisions.md | C2 | 2524540 | f959e11a02b47b64aeb164b198959279fee4d9e7253101de9d2764537a533209 |
 | .agent/live_review.md | C2 | 122532 | 36aac59085dfea3376879a5ae9a415c8ca1e3a763a108dc2522af777560d5316 |
 | .agent/plan.md | C2 | 1296 | b86e126b4d6c27ef2303ff73d79f1e434e7a7717a2532ed7a598de8a5bb8251c |
 | apps/ui/src/api/terminology.test.ts | C4 | 14217 | 939a2b6645089e7e0e28de8aaa9294659148248ab4d02063c94f8b2742d811ab |
 | apps/ui/src/components/term/termAudit.test.ts | C4 | 11862 | 1da30df5707675361a1cc035c7b5224a073e19da33313c902af8d0895b9873a1 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show <commit>:<path>` at
 C2 (the reviewer read `[]`); the ledger's last non-empty line at C2 begins `Gate: F043 R1 — the
 F043 round 1 entry`; and `git diff --name-only <C1d> <C2>`, which must name exactly the C2 paths
 of the table above.

G3 THE CODE AND THE TESTS — at C5: `python3 -m ruff check .agent/authored/f043-r2-mutations.py
 .agent/authored/f043-r2-render_measure.py`, and `apps/ui/node_modules/.bin/eslint src` run with
 `apps/ui` as its working directory, each with its real exit code. Report `git show --numstat
 <C3>` and the whole diff of C3. Then, in the primary checkout at C5, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_escalation.py tests/cli/test_plan_approval.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_live_review_rotation.py tests/regression/test_resource_safety.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 This selection runs `tsc --noEmit` (`test_typescript_compiles`), the whole vitest suite
 (`test_vitest_passes`) and eslint over `apps/ui/src` (`tests/ui_contracts/test_ui_lint.py`);
 name each of those nodes' outcomes. The reviewer ran the selection serially in its dry tree,
 which carries C2, this round's tests and the reviewer's own version of S1 to S9 but no
 `.agent/authored/f043-r2-*` copy and no built `apps/ui/dist`, with the primary's `node_modules`
 linked in, and read `1745 passed, 6 skipped` at real exit code 0, the same six skips round 1's
 dry tree printed, among them `tests/ui_contracts/test_responsive.py:555` for an unbuilt `dist`,
 which your checkout has built (round 1's primary run read `1746 passed, 5 skipped`); through the
 primary's binaries in the same tree the whole vitest suite read `1988 passed | 5 skipped` over
 100 files at exit 0. Report every `SKIPPED` line yours prints and the vitest counts of
 `src/api/terminology.test.ts`, `src/api/terminologyAudit.test.ts` and
 `src/components/term/termAudit.test.ts` (the reviewer's read 12, 8 and 12). Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G4 THE RENDER — at C5, in the primary checkout:
 `python3 -B .agent/authored/f043-r2-render_measure.py /home/decodeux/Repos/remedy`, which builds
 the harness page over the checkout's own `apps/ui/src`, serves it on 127.0.0.1 port 9010, drives
 `/usr/bin/google-chrome --headless=new` over CDP port 9380, stops both by pid and removes its work
 dir. Report its whole output from the first `PASS` or `FAIL` line on, and its exit code; it must
 print `RENDER: 9 of 9 checks pass` and exit 0. Read the screenshot it writes to
 `/home/decodeux/Repos/remedy/.remedy-wt/f043-r2-render-tooltip.png` and say in one sentence
 what it shows. The reviewer's own run over its version of S1 to S9 read 9 of 9.

G5 THE RED PROOFS — your tool `.agent/authored/f043-r2-mutations.py` takes a worktree path, and
 for each mutation below edits the named production file INSIDE that worktree (asserting its
 FROM text occurs exactly once there), runs the named check, restores the bytes, and prints one
 line per mutation: its label, the exit code, and the failed count or the harness's
 `RENDER: <n> of 9` reading. Vitest runs as `<primary>/apps/ui/node_modules/.bin/vitest run
 --root <worktree>/apps/ui --config <primary>/apps/ui/vitest.config.ts
 src/api/terminology.test.ts src/api/terminologyAudit.test.ts src/components/term/termAudit.test.ts`
 with `<worktree>/apps/ui` as the working directory (checklist item 33); the harness as
 `python3 -B <worktree>/.agent/authored/f043-r2-render_measure.py <worktree>`. The primary is
 `/home/decodeux/Repos/remedy`. The tool runs an unmutated control of both checks first and
 last, reports `restored byte-identical: True` after each restore, and ends with
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  m1 `stateTerm` loses its `blocked` line, so a blocked row explains itself as planned
     (`TaskChecklistCard.tsx`, vitest);
  m2 `insideControl` no longer removes the `tabIndex` (`Term.tsx`, vitest);
  m3 `METRIC_TERMS` also maps `tokens` (to `metric.open`) (`TopMetricsBar.tsx`, vitest);
  m4 the Live badge's word loses its term (`AgentNowCard.tsx`, vitest);
  m5 the decision inbox's heading loses its term (`DecisionInboxCard.tsx`, vitest);
  m6 the SCRUBBED badge loses its term (`BrainGraphStage.tsx`, vitest);
  m7 the `panel.tasks` anchor reads "picks" in place of "chooses" (`terminology.ts`, vitest);
  h1 `.cardHeader > span {` reads `.cardHeader span {` again (`RightLivePanel.module.css`, the
     harness);
  h2 `.liveSmall > span:first-child {` reads `.liveSmall span {` again (same);
  h3 m3's change, read by the harness instead (`TopMetricsBar.tsx`, the harness).
 Run it: `git worktree add --detach .remedy-wt/f043-r2-mut <C5>`, then in Python
 `os.symlink("/home/decodeux/Repos/remedy/apps/ui/node_modules",
 "/home/decodeux/Repos/remedy/.remedy-wt/f043-r2-mut/apps/ui/node_modules",
 target_is_directory=True)`, then
 `python3 -B .agent/authored/f043-r2-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f043-r2-mut`
 and report its whole output. The reviewer's own version of this probe, run against its version
 of S1 to S9, turned every one red with every control passing. EVERY mutation must exit
 non-zero; one that stays green is reported as green, never papered over, and you then STOP and
 report it. Then remove the symlink with `os.unlink`, `git worktree remove --force
 .remedy-wt/f043-r2-mut`, `git worktree prune`, and report `git worktree list | wc -l`.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`, which must show C6, C5, C4, C3, C2, C1d, C1c, C1b, C1a and
 `15331eb0b` in that order (one more line if C3 was split); `git worktree list | wc -l`, which
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
of feature F043, round 2, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 2, then the token and cost tiles onto the term's tooltip with their breakdown and the '?'
panel. State the open-findings count, 0, and the operator-questions count, 0.
