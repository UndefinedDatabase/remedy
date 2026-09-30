STEP F043 R1 — CLAIM F043 AND LAND T001 AND T002 OVER THE FIRST SURFACES: the explanation catalog, the Term component with its tooltip, and the term audit over the live-status pill and the phase timeline

GOAL
Pull request 299 is merged; `main` is at `21bfc1881` and F043 Explanation layer is the first
unchecked STATUS line. Cut F043's branch, claim it, re-head the live review record, book F291's
round 6, record DECISION F043 D1 with its assumption-log line, and land T001 and T002 over the
first two surfaces against the reviewer's tests and a render harness that proves the tooltip in a
real browser.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE TESTS ARE THE REVIEWER'S AND THE CODE IS YOURS:
the test files and the render harness travel as payloads and are the acceptance, and you write
the production code against them and against S1 to S7 below. You never edit a payload; if one
looks wrong to you, STOP and report it. Read DECISION F043 D1 in the claim diff before you write
code, and read whole, before you edit or call them: `apps/ui/src/components/panels/LiveStatusPill.tsx`,
`apps/ui/src/components/timeline/PhaseTimeline.tsx`, `apps/ui/src/styles/tokens.css`,
`apps/ui/src/api/humanizeCatalog.ts` (the sibling catalog's style), and the tests that read the
two components: `tests/ui_contracts/test_live_status_pill.py`, `tests/ui_contracts/test_timeline_guard.py`
and `tests/ui_contracts/test_raw_colour_ratchet.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f043-r1-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f043-r1/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f043-scratch/`      The reviewer's scripts; do not touch them.
  `.remedy-wt/f043-r1-worker/`    YOURS for logs and scripts; create it if absent. All are
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
   `git status --porcelain` must be empty, `git branch --show-current` must read `main`, and
   `git log --oneline -1` must read `21bfc1881`. Report all three. Then
   `git checkout -b feature/f043-explanation-layer` and report the branch. Do NOT pull: the
   Open PR Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f043-r1/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f043-r1-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 151 | 20295 | 9b96e3d6b553116a328815d1b225a391a3785f88464c6fa778f67475eeeeee2c |
| tests.diff | 373 | 16417 | ebc6731b31e2d8ae5096b6aab4d87e6546349eff34a5e4540ce29a9332773ed1 |
| plan.md | 34 | 1375 | edcad5e50e4cedc4d2ff17386d9e2be2632960351a345ceff3e5d3a9e952b0d4 |
| context.md | 36 | 1565 | c09bc76c498a8083372df0464dcb3aacc6aea90bdec9df01a611c7a9279b8360 |
| render_index.html | 11 | 243 | ef46945d7896d3ef2bfac692e8e0b96ba225e2b92a9767dc7d2d311a516ab05f |
| render_main.tsx | 51 | 2146 | 8b7351ff97f491ec14bc7344e28d7953321031c792881099156d9fe5ccbdbc79 |
| render_vite.config.mjs | 28 | 744 | 6c9d24558a507a827d445c793cd6203f7f0f24ac2659dcfe3cff96c20b7d1c6a |
| render_drive.mjs | 181 | 8432 | 98da710254b4878fbe8d958ea1e336d5c9edc1f589cbdd96365965ce88fef4c8 |
| render_measure.py | 187 | 6424 | 972474ce9fda06d963d2c9ecefbac91fcfca9c5c72f01eaa875ebd46387f2fd5 |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`. The two
`.diff` files go on with `git apply`; the reviewer generated them with `git diff HEAD` from a tree
at `21bfc1881`. `claim.diff` edits `.agent/live_review.md` (the re-head, which replaces everything
above the `## Findings` heading line, then F291's round 6 gate entry appended),
`.agent/decisions.md` (DECISION F043 D1 appended), `docs/roadmap/STATUS.md` (F043's line `[ ]` to
`[~]`) and `docs/ui/design_reference/assumption_log.md` (one row appended). `tests.diff` adds the
NEW FILE at `apps/ui/src/api/terminology.test.ts`, the NEW FILE at
`apps/ui/src/api/terminologyAudit.test.ts` and the NEW FILE at
`apps/ui/src/components/term/termAudit.test.ts`. The five `render_*` files are the render
harness; they are copied, never applied, and run from their copies.

THE SPECIFICATION — the tests are the acceptance; these clauses fix what they leave open. No
`@mui` import, no colour literal outside `styles/tokens.css`, only `--remedy-*` tokens in CSS.
S1 `apps/ui/src/api/terminology.ts`, NEW, pure (no React, no storage, no clock, no network), a
   header comment naming T5_F043 T001 and DECISION F043 D1, saying each entry names the file that
   defines its term and a phrase that file states, and stating the deliberate absence: Remedy
   deliberately does not explain a term whose defining feature has not shipped. Exports the
   interface `TermEntry` (`readonly title`, `readonly body`, `readonly source`, `readonly anchor`,
   all strings), `TERM_BODY_MAX_CHARS = 240`, `TERM_KEY_PATTERN =
   /^[a-z][a-z0-9_]*(\.[a-z0-9_]+)+$/`, `TERM_CATALOG: Readonly<Record<string, TermEntry>>`, whose
   entries are EXACTLY those the test "words every entry exactly as DECISION F043 D1's first round
   wrote it" pins, and `termEntry(key)`, answering the entry for an OWN key of the catalog and
   null otherwise (`Object.prototype.hasOwnProperty.call`), so `toString` answers null.
S2 `apps/ui/src/api/terminologyAudit.ts`, NEW, pure, a header comment naming T5_F043 T002 and
   DECISION F043 D1. Exports `collectDataTerms(markup): string[]` — every value of an attribute
   written as white space, then `data-term="`, then the value up to the next `"`, each value once,
   sorted; the tooltip's `data-term-tip` attribute and text that merely reads `data-term="…"` are
   not collected — the interface `TermAudit` (`readonly missing: readonly string[]`, `readonly
   dead: readonly string[]`), and `auditTermUse(used, catalogKeys)`, both iterables of strings,
   answering the used terms that are not keys as `missing` and the keys that are not used as
   `dead`, each sorted.
S3 `apps/ui/src/components/term/Term.tsx`, NEW, a header comment naming T5_F043 T001, DECISION
   F043 D1 and why the tooltip is portalled. Exports `TERM_HOVER_DELAY_MS = 120` and
   `Term({ term, children }: { term: string; children: ReactNode })`. For a key `termEntry`
   answers null it renders only `<span className={styles.term} data-term={term}>{children}</span>`.
   Otherwise one span with `className={styles.term}`, `data-term={term}`, `tabIndex={0}`,
   `aria-describedby` set to the tooltip's `useId()` id ONLY while the tooltip is open, and the
   children. A pointer entering starts a `TERM_HOVER_DELAY_MS` timer that opens the tooltip; the
   pointer leaving before it fires opens nothing (the timer lives in an effect whose cleanup clears
   it). Focus opens it at once. The pointer leaving and the focus leaving close it. Escape while
   open closes it, stops the event's propagation, and leaves the focus where it is. While open it
   renders, through `createPortal(..., document.body)`, `<span role="tooltip" id={<the id>}
   className={styles.tip} data-ui="term-tip" data-term-tip={term} data-placed={"true" or
   "false"}>` holding exactly two spans, the entry's title (`styles.tipTitle`) and then its body
   (`styles.tipBody`), with nothing between them. THE PLACEMENT is measured in a
   `useLayoutEffect` keyed by the open state, before paint, from the term's
   `getBoundingClientRect()` and the tooltip's `offsetWidth` and `offsetHeight`, against
   `document.documentElement.clientWidth` and `clientHeight`: left is the term's left, moved so the
   tooltip keeps 8 pixels from both edges; top is the term's bottom plus 6, unless the tooltip's
   bottom would then pass `clientHeight - 8`, in which case it is the term's top minus 6 minus the
   tooltip's height, but never less than 8. Until that measurement has set a place, `data-placed`
   reads "false" and no inline position is set; after it, "true" with `left` and `top` inline.
S4 `apps/ui/src/components/term/Term.module.css`, NEW. `.term`: `cursor: help`, a dotted
   underline in `--remedy-line-strong`, and on `:focus-visible` a 2px solid `--remedy-focus`
   outline. `.tip`: `position: fixed` at `left: 0; top: 0` until placed, `z-index:
   var(--remedy-z-tooltip)`, a glass tip (`--remedy-glass-bg-strong` background,
   `--remedy-glass-border` border, `--remedy-radius-md`, `--remedy-shadow-soft`, a backdrop blur),
   `max-width: 280px`, 12px `--remedy-font-ui` text in `--remedy-text`, `text-transform: none`,
   `pointer-events: none`, and a fade-in over `--remedy-dur-fast` with `--remedy-ease-standard`,
   none under `prefers-reduced-motion: reduce`; `.tip[data-placed="false"]` is `visibility:
   hidden`. `.tipTitle` is a block, 11px, weight 800, `--remedy-ink-strong`; `.tipBody` a block in
   `--remedy-ink`.
S5 `apps/ui/src/styles/tokens.css`: directly after the `--remedy-shadow-panel` line, a comment
   naming the explanation layer's tooltip, F043 and DECISION F043 D1 as transcribed byte-exact from
   `docs/ui/design_reference/tokens.css`, then exactly these four lines in this order:
   `--remedy-z-tooltip: 100;`, `--remedy-dur-fast: 120ms;`, `--remedy-ease-standard:
   cubic-bezier(0.4, 0, 0.2, 1);`, `--remedy-focus: #2f6fff;`, each indented two spaces.
S6 `apps/ui/src/components/panels/LiveStatusPill.tsx`: one import of `Term` from
   `"../term/Term"`, and each label wrapped in its term, the dot left outside it:
   `<Term term="status.replay">REPLAY</Term>`, `<Term term="status.delayed">DELAYED</Term>`,
   `<Term term="status.reconnecting">RECONNECTING</Term>`, and in the last arm
   `<Term term={live ? "status.live" : "status.idle"}>{live ? "LIVE" : "IDLE"}</Term>`. Nothing
   else in the file changes.
S7 `apps/ui/src/components/timeline/PhaseTimeline.tsx`: delete `PHASE_HINTS` and the phase item's
   `title` attribute; add `PHASE_TERMS: Record<TimelinePhase, string>` mapping each of the six
   phases to the literal `"phase.<phase>"` under a comment saying the label's term explains what
   begins each phase, naming DECISIONS F024 D1 and F043 D1; import `Term` from `"../term/Term"`;
   and wrap the label span as `<Term term={PHASE_TERMS[phase.phase]}><span
   className={styles.phaseLabel}>{phase.label}</span></Term>`. Nothing else in the file changes.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C2, C3, C4, C5 and C6, in this order.

C1a — copy this block and the state payloads
  `.agent/authored/f043-r1-block.md` := this block, `.agent/authored/f043-r1-plan.md` := plan.md
  and `.agent/authored/f043-r1-context.md` := context.md, all by `shutil.copyfile`.
  Subject: `F043 R1 C1a: copy round 1 block and state payloads into .agent/authored/`
  Its insertions are this block's line count plus 70. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the claim diff
  `.agent/authored/f043-r1-claim.diff` := claim.diff.
  Subject: `F043 R1 C1b: copy round 1 claim diff into .agent/authored/`
  Expected insertions: 151.

C1c — copy the tests diff
  `.agent/authored/f043-r1-tests.diff` := tests.diff.
  Subject: `F043 R1 C1c: copy round 1 tests diff into .agent/authored/`
  Expected insertions: 373.

C1d — copy the render harness
  Each `render_<x>` payload := `.agent/authored/f043-r1-render_<x>`, all five.
  Subject: `F043 R1 C1d: copy the round 1 render harness into .agent/authored/`
  Expected insertions: 458.

C2 — THE CLAIM AND ITS RECORDS, in this order:
   1. `git apply` claim.diff
   2. rewrite `.agent/plan.md` := plan.md
   3. rewrite `.agent/context.md` := context.md
  Subject: `F043 R1 C2: claim F043, re-head the live review record, book F291 R6, record D1`
  Expected by `git show --numstat` (insertions and deletions): 14/13 .agent/context.md, 68/0 .agent/decisions.md, 19/16 .agent/live_review.md, 21/13 .agent/plan.md, 1/1 docs/roadmap/STATUS.md, 1/0 docs/ui/design_reference/assumption_log.md.

C3 — THE CODE: S1 to S7 in one commit. If it would reach 500 insertions, split S1, S2 and S5
  into a first commit and S3, S4, S6 and S7 into a second, and say so.
  Subject: `F043 R1 C3: explain the pill's and the timeline's terms from one catalog`
  The reviewer's own version of S1 to S7 read 108/0 apps/ui/src/api/terminology.ts, 36/0 apps/ui/src/api/terminologyAudit.ts, 5/4 apps/ui/src/components/panels/LiveStatusPill.tsx, 66/0 apps/ui/src/components/term/Term.module.css, 108/0 apps/ui/src/components/term/Term.tsx, 13/10 apps/ui/src/components/timeline/PhaseTimeline.tsx, 7/0 apps/ui/src/styles/tokens.css.

C4 — THE TESTS: `git apply` tests.diff.
  Subject: `F043 R1 C4: add the reviewer's tests for the catalog, the term and the term audit`
  Expected: 193/0 apps/ui/src/api/terminology.test.ts, 43/0 apps/ui/src/api/terminologyAudit.test.ts, 119/0 apps/ui/src/components/term/termAudit.test.ts.

C5 — THE TOOL: your mutation tool (G5) saved as `.agent/authored/f043-r1-mutations.py`.
  Subject: `F043 R1 C5: add the round 1 mutation tool`

C6 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F043 R1 C6: rewrite handoff for round 1`
  Then `git push -u origin feature/f043-explanation-layer`. Do NOT create a pull request: the
  branch opens one at F043's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; C3's own clause
   says what to do if it would not.
3. The round's whole tracked path set is: the `.agent/authored/f043-r1-*` copies and tool, the
   paths claim.diff and tests.diff edit, `.agent/plan.md`, `.agent/context.md`, the files S1 to
   S7 name, and `.agent/handoff.md`. Report the list you measure with `git diff --name-only
   21bfc1881` at the branch tip after C6. Do NOT touch `apps/ui/src/components/tour/`,
   `apps/ui/src/components/shell/RemedyShell.tsx`, `apps/ui/src/api/humanizeCatalog.ts`,
   `apps/ui/src/components/timeline/timelineView.ts`, `apps/ui/src/components/timeline/phaseMapping.ts`,
   `docs/roadmap/features/`, `docs/system/`, `packages/`, `apps/cli/`, `apps/ui/package.json`,
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md` or `README.md`.
4. Every test the payloads carry passes against your code unedited, at C4, and the render
   harness reads every check passing at C4. A payload is never edited to pass; if your code
   cannot meet one, STOP and report it and the reason.
5. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. An EXISTING test
   that goes red is never edited to pass; report it and stop.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
7. Leave every worktree already listed at your step 4, its branch, and every existing stash
   alone. The worktree G5 adds goes under `.remedy-wt/`, is removed as that gate's last action,
   and `git worktree list | wc -l` is reported afterwards.
8. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F043's belongs to its closure. Run no self-use job and no command that calls a provider.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C6 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f043-r1-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f043-r1/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE CLAIM AND THE TESTS — the sha256 of each file below, read with `git show <commit>:<path>`
 at the commit named, equals the reviewer's reading, printed from its simulation tree. Report
 each path beside the hash you read:
 | path | at | bytes | sha256 |
 |---|---|---|---|
 | .agent/context.md | C2 | 1565 | c09bc76c498a8083372df0464dcb3aacc6aea90bdec9df01a611c7a9279b8360 |
 | .agent/decisions.md | C2 | 2520296 | 968372e21a69e904857bb624b1e781839bbf048c1f83bf4756e2c9b59f7ddab8 |
 | .agent/live_review.md | C2 | 120733 | 703ab78998b2dd8063577e74802537e388163b8e6aba500d3b9b30ab37325d00 |
 | .agent/plan.md | C2 | 1375 | edcad5e50e4cedc4d2ff17386d9e2be2632960351a345ceff3e5d3a9e952b0d4 |
 | docs/roadmap/STATUS.md | C2 | 59240 | 2ab18d0c5349c929057db58effc5407995d749184590af7a15c7fbce31f08dcc |
 | docs/ui/design_reference/assumption_log.md | C2 | 30413 | c859925ec647b420ccf44d6296ebae1f150629cb4fcef84e2d32fb3109f82fab |
 | apps/ui/src/api/terminology.test.ts | C4 | 8245 | 84fa56bbb974a55daafd7e81a6012ee1c653ccdde92a2a9b50036fffcb883e93 |
 | apps/ui/src/api/terminologyAudit.test.ts | C4 | 1892 | 0aadb7c726d2c5ea7c576984b0820311ffaafc8ca9fa93ea586136b82eda7007 |
 | apps/ui/src/components/term/termAudit.test.ts | C4 | 5254 | 92bb9f774e42e8105f8023b95536b8f43e09187b754a91eb50eb47aeb6d55dc7 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show <commit>:<path>`, at
 `21bfc1881` and at C2 (the reviewer read `[]` both times); at C2 the ledger has exactly one line
 reading `## Findings` and exactly one reading `## Steps`, and its last non-empty line begins
 `Gate: F291 R6 — the F291 round 6 entry`; F043's STATUS line at C2 read back in full, which must
 read `- [~] F043 — Explanation layer`; and `git diff --name-only <C1d> <C2>`, which must name
 exactly the C2 paths of the table above.

G3 THE CODE AND THE TESTS — at C5: `python3 -m ruff check .agent/authored/f043-r1-mutations.py
 .agent/authored/f043-r1-render_measure.py`, and `apps/ui/node_modules/.bin/eslint
 src/api/terminology.ts src/api/terminologyAudit.ts src/api/terminology.test.ts
 src/api/terminologyAudit.test.ts src/components/term/Term.tsx src/components/term/termAudit.test.ts
 src/components/panels/LiveStatusPill.tsx src/components/timeline/PhaseTimeline.tsx` run with
 `apps/ui` as its working directory, each with its real exit code. Report `git show --numstat
 <C3>` and the diffs of `LiveStatusPill.tsx`, `PhaseTimeline.tsx` and `tokens.css` at C3, whole.
 Then, in the primary checkout at C5, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_escalation.py tests/cli/test_plan_approval.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_live_review_rotation.py tests/regression/test_resource_safety.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 This selection runs `tsc --noEmit` (`test_typescript_compiles`), the whole vitest suite
 (`test_vitest_passes`) and eslint over `apps/ui/src` (`tests/ui_contracts/test_ui_lint.py`);
 name each of those nodes' outcomes. The reviewer ran the selection serially in its dry tree,
 which carries C2, this round's tests and the reviewer's own version of S1 to S7 but no
 `.agent/authored/f043-r1-*` copy and no built `apps/ui/dist`, with the primary's `node_modules`
 linked in, and read `1745 passed, 6 skipped` at real exit code 0, its skips the four D3
 quarantine nodes of `test_graph_architecture.py` and `test_ux_quality.py`, the D12 quarantine and
 `tests/ui_contracts/test_responsive.py:555` for an unbuilt `dist`, which your checkout may have
 built; through the primary's binaries in the same tree `tsc` read exit 0 and the whole vitest
 suite `1982 passed | 5 skipped` over 100 files at exit 0. Your counts may differ from those by
 what the round's copies and your `dist` hold: report every `SKIPPED` line yours prints and the
 vitest counts of the three new test files (the reviewer's read 11, 8 and 7). Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G4 THE RENDER — at C5, in the primary checkout:
 `python3 -B .agent/authored/f043-r1-render_measure.py /home/decodeux/Repos/remedy`, which builds
 the harness page over the checkout's own `apps/ui/src`, serves it on 127.0.0.1 port 9010, drives
 `/usr/bin/google-chrome --headless=new` over CDP port 9380, stops both by pid and removes its work
 dir. Report its whole output from the first `PASS` or `FAIL` line on, and its exit code; it must
 print `RENDER: 7 of 7 checks pass` and exit 0. Read the screenshot it writes to
 `/home/decodeux/Repos/remedy/.remedy-wt/f043-r1-render-tooltip.png` and say in one sentence
 what it shows. The reviewer's own run over its version of S1 to S7 read 7 of 7.

G5 THE RED PROOFS — your tool `.agent/authored/f043-r1-mutations.py` takes a worktree path, and
 for each mutation below edits the named production file INSIDE that worktree (asserting its
 FROM text occurs exactly once there), runs the named check, restores the bytes, and prints one
 line per mutation: its label, the exit code, and the failed count or the harness's
 `RENDER: <n> of 7` reading. Vitest runs as `<primary>/apps/ui/node_modules/.bin/vitest run
 --root <worktree>/apps/ui --config <primary>/apps/ui/vitest.config.ts
 src/api/terminology.test.ts src/api/terminologyAudit.test.ts src/components/term/termAudit.test.ts`
 with `<worktree>/apps/ui` as the working directory (checklist item 33); the harness as
 `python3 -B <worktree>/.agent/authored/f043-r1-render_measure.py <worktree>`. The primary is
 `/home/decodeux/Repos/remedy`. The tool runs an unmutated control of both checks first and
 last, reports `restored byte-identical: True` after each restore, and ends with
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  t1 `termEntry` answers `TERM_CATALOG[key] ?? null` (`terminology.ts`, vitest);
  t2 the `status.delayed` anchor reads "quietly" in place of "visibly" (same);
  a1 `collectDataTerms` returns its values unsorted (`terminologyAudit.ts`, vitest);
  a2 `collectDataTerms` drops the white space required before `data-term=` (same);
  a3 `auditTermUse` returns `dead` unsorted (same);
  c1 `Term` omits `data-term` for a key the catalog lacks (`Term.tsx`, vitest);
  c2 the pill renders REPLAY without its term (`LiveStatusPill.tsx`, vitest);
  h1 the tooltip is portalled into the term's own span instead of `document.body` (`Term.tsx`,
     the harness);
  h2 Escape no longer closes the tooltip (same);
  h3 focus starts the hover timer instead of opening at once (same);
  h4 `TERM_HOVER_DELAY_MS` is 0 (same);
  h5 the placement never moves the tooltip above the term (same).
 Run it: `git worktree add --detach .remedy-wt/f043-r1-mut <C5>`, then in Python
 `os.symlink("/home/decodeux/Repos/remedy/apps/ui/node_modules",
 "/home/decodeux/Repos/remedy/.remedy-wt/f043-r1-mut/apps/ui/node_modules",
 target_is_directory=True)`, then
 `python3 -B .agent/authored/f043-r1-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f043-r1-mut`
 and report its whole output. The reviewer's own version of this probe, run against its version
 of S1 to S7, turned every one red with every control passing. EVERY mutation must exit
 non-zero; one that stays green is reported as green, never papered over, and you then STOP and
 report it. Then remove the symlink with `os.unlink`, `git worktree remove --force
 .remedy-wt/f043-r1-mut`, `git worktree prune`, and report `git worktree list | wc -l`.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`, which must show C6, C5, C4, C3, C2, C1d, C1c, C1b, C1a and
 `21bfc1881` in that order (one more line if C3 was split); `git worktree list | wc -l`, which must
 equal your step 4 reading; the push's real outcome; and `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, which must be EMPTY. These readings go in your reply,
 since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3's own files beyond the
reviewer's reading, and none for C5 — report what you measure), every gate's real output and exit
code, the authored-text proofs, the item-status table AGENTS.md requires (one row per commit and
per gate), the deviations, and the next expected action. Report what you ran, not what you
expected to find. Your Session section reads SESSION 1 of feature F043, round 1, and says in one
sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 1, then the terms of the remaining shell surfaces (the metrics bar, the decision inbox, the
activity feed and its NowCard, the task list and the graph's scrubbed banner). State the
open-findings count, 0, and the operator-questions count, 0.
