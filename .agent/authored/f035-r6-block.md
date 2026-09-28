STEP F035 R6 — T003: the evidence panel's "Ownership" tab, the whole job's history, and a headless render of the task detail's section and the tab

GOAL
Round 5 passed and repaired R-1082. Book that verdict with R-1082's resolution, DECISION F035 D6
and one assumption-log row, then land the evidence panel's fourth tab, "Ownership", with its pure
state function, and prove the task detail's "Who did what" section and the tab in a headless
browser, from the F288 round 6 harness. The end-to-end proof is the next round's.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code, its tests and the harness yourself against S1 to S5 below. Read DECISION F035 D6
in the booking diff first. Before you write anything, read whole: `apps/ui/src/api/ownership.ts`
and `ownership.test.ts`; `apps/ui/src/components/graph/EvidencePanel.tsx`, its CSS module,
`evidencePanel.ts` and `evidencePanel.test.ts`; `EvidenceTab` in `semanticZoom.ts`; `TABS` in
`zoomDeepLink.ts` and `zoomDeepLink.test.ts`; `tests/ui_contracts/test_evidence_panel_contract.py`;
`tests/ui_contracts/test_ownership_view_contract.py`; `DetailPopover.tsx`; the five
`.agent/authored/f288-r6-render_*` files, `.agent/authored/f288-r6-render.txt` and S4 of
`.agent/authored/f288-r6-block.md`, the harness you adapt; and G5 of
`.agent/authored/f035-r5-block.md`, whose tool you extend.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f035-r6-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f035-r6/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f035-r6-sim/`       The reviewer's simulation tree; do not touch it.
  `.remedy-wt/f035-review/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f035-r6-worker/`    YOURS for logs, scripts, screenshots and scratch configs; create
                                  it if absent. `.remedy-wt/f035-render-run/` is the harness's
                                  work dir, removed at its end. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Never run npm or npx; the harness runs the primary's own `vite` binary as F288's did. Stop
every process you start by its own pid, never with `pkill -f`.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f035-ownership-ledger`, and `git log --oneline -1` must read `36d5c359`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f035-r6/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` and `git branch --list 'remedy/*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f035-r6-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| booking.diff | 63 | 11743 | a3517a844a2aa38ad15141f35121160944410aed0e39cd9e16c4932effdf03c5 |
| plan.md | 29 | 914 | 44cb05f4b87d1302a9c53516d3cc6c813c7451d633e707b2f0aff6808e6f0aaa |

`plan.md` is a REWRITE of `.agent/plan.md`. `booking.diff` goes on with `git apply`; the
reviewer generated it with `git diff HEAD` from a tree at `36d5c359`. It removes R-1082's
`Landed:` line from `.agent/live_review.md` and appends round 5's gate entry and R-1082's `Done:`
resolution there, appends DECISION F035 D6 to `.agent/decisions.md`, and appends one row to
`docs/ui/design_reference/assumption_log.md`.

THE SPECIFICATION. No `any` type and no raw colour in TypeScript or CSS; every sentence is shown
verbatim, never passed through `scrubUiText`, never cut.
S1 THE STATE, in `ownership.ts`: `OWNERSHIP_EMPTY_LINE = "No action is recorded for this job
   yet."` and `ownershipPanelState(view: OwnershipView | null, loaded: boolean)`, answering
   `{ kind: "loading" }` while not loaded, `{ kind: "unreadable", line: OWNERSHIP_UNREADABLE_LINE }`
   for a loaded `null` or a view whose `error` is not "", `{ kind: "empty", line:
   OWNERSHIP_EMPTY_LINE }` for a view with no entry, and `{ kind: "entries", entries }` with every
   entry in the view's order otherwise.
S2 THE TAB: `"ownership"` joins `EvidenceTab` in `semanticZoom.ts`, `{ tab: "ownership", label:
   "Ownership" }` is the fourth entry of `EVIDENCE_TABS`, and `"ownership"` the fourth of `TABS`
   in `zoomDeepLink.ts`. In `EvidencePanel.tsx`, `{tab === "ownership" && <OwnershipTab
   jobId={jobId} token={token} />}` follows the chat line, and `OwnershipTab` sits in the same file
   after `DiffTab`, shaped as it: one effect guarded by `cancelled`, keyed on the job id and the
   token, calling `loadOwnershipView`; it renders `ownershipPanelState`'s line in a `<p
   className={styles.note}>` for every kind but `entries`, and for `entries` one `<ul>` whose
   `<li key={entry.recordRef}>` holds `<span className={styles.ownershipChip}>` with
   `ownershipChipWord(entry.action)` and `<span className={styles.ownershipSentence}>` with the
   sentence. `EvidencePanel.module.css` gains the two classes, token-only, `.ownershipChip` as the
   popover's and `.ownershipSentence` with `white-space: pre-line`, so the raw-colour ratchet does
   not move.
S3 THE TEST PINS: `evidencePanel.test.ts`'s tab-list assertion and `zoomDeepLink.test.ts` gain
   `ownership`; `tests/ui_contracts/test_evidence_panel_contract.py` gains the assertion of the
   ownership line beside its three; `tests/ui_contracts/test_ownership_view_contract.py` gains a
   test that `OwnershipTab` never renders an `error` and carries the `cancelled` guard. Nothing
   they already assert is removed or loosened. `ownership.test.ts` gains one test per S1 state.
S4 THE HARNESS: five files under `.agent/authored/`, `f035-r6-render_measure.py`,
   `f035-r6-render_index.html`, `f035-r6-render_main.tsx`, `f035-r6-render_vite.config.mjs` and
   `f035-r6-render_drive.mjs`, adapted from the F288 files with the same mechanics (work dir
   `.remedy-wt/f035-render-run`, the primary's `node_modules` symlinked in, the primary's `vite`,
   `python3 -m http.server` on 127.0.0.1 port 8994, `/usr/bin/google-chrome --headless=new` with
   its own user-data dir and CDP on port 9364, both stopped by their own pids, the work dir removed
   at the end). The page, 1280x800, imports from `apps/ui/src` by relative path and renders from
   one fixed view of four entries — a task veto of task A with a two-line reason, a note to task A,
   a pause of task B, and a job stop with task ids [] — (i) `DetailPopover` for task A, (ii)
   `DetailPopover` for task C, which no entry names, (iii) `DetailPopover` for task A with a view
   whose `error` is `"boom: secret"`, and (iv) `EvidencePanel` opened on the ownership tab, its
   `loadOwnershipView` reading the fixed view through a `window.fetch` the page replaces.
   `drive.mjs` prints one line per check and exits 0 only when all pass and no page exception
   was thrown:
     C-a (i) holds `data-ui="ownership-section"` after `data-ui="unreachable-section"` when both
         exist, and its chips read, in order, `Veto` then `Note`;
     C-b (i)'s sentences equal the fixed view's two sentences for task A character for
         character, the two-line reason included, and the second line is rendered below the
         first (its text's bounding box is taller than one line);
     C-c every chip of (i) is a pill: computed `border-radius` at least half its height, and its
         height at most 24 pixels;
     C-d (ii) holds no `data-ui="ownership-section"`;
     C-e (iii)'s section reads exactly `Who did what could not be read for this job.` and the
         page's text nowhere holds `boom: secret`;
     C-f (iv)'s tab row reads `Diff`, `Prompt trace`, `Chat`, `Ownership`, and its list holds the
         four sentences of the view in order.
   It saves `Page.captureScreenshot` PNGs as `.remedy-wt/f035-r6-worker/render-detail.png` and
   `.remedy-wt/f035-r6-worker/render-tab.png` and prints their byte counts. Its output is saved as
   `.agent/authored/f035-r6-render.txt`.
S5 UNCHANGED: every Python file under `packages/` and `apps/cli/`, `DetailPopover.tsx`,
   `RemedyShell.tsx`, `remedyApi.ts`, and every existing assertion.

BUNDLE — the commits are C1, C2, C3, C4, C5 and C6, in this order.

C1 — copy this block and the payloads: `.agent/authored/f035-r6-block.md`,
  `.agent/authored/f035-r6-plan.md` and `.agent/authored/f035-r6-booking.diff`, by
  `shutil.copyfile`. Subject: `F035 R6 C1: copy round 6 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 92. Report the number you measure.
C2 — THE BOOKING, the round's first substantive commit: `git apply` booking.diff, then rewrite
  `.agent/plan.md` := plan.md. Subject: `F035 R6 C2: book round 5, resolve R-1082, record D6,
  one assumption row, advance the plan`. Expected by `git show --numstat`: 34/0 decisions.md,
  3/1 live_review.md, 8/6 plan.md, 1/0 assumption_log.md.
C3 — S1, S2 and S3. Subject: `F035 R6 C3: the evidence panel's ownership tab, the whole job's history`
C4 — S4's five harness files and the render transcript, after G4 below has passed.
  Subject: `F035 R6 C4: render the ownership section and tab headless`
C5 — your mutation tool (G5's), `.agent/authored/f035-r6-mutations.py`. Subject:
  `F035 R6 C5: add the round 6 mutation tool`
C6 — THE HANDBACK, `.agent/handoff.md` rewritten per `docs/agents/handback_template.md`, its own
  commit. Subject: `F035 R6 C6: rewrite handoff for round 6`. Then `git push`. Do NOT create a
  pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split one that
   would reach it into parts with their own subjects, and say so.
3. The round's whole tracked path set is: the `.agent/authored/f035-r6-*` copies, harness,
   transcript and tool, `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `docs/ui/design_reference/assumption_log.md`, `apps/ui/src/api/ownership.ts`,
   `apps/ui/src/api/ownership.test.ts`, `apps/ui/src/components/graph/EvidencePanel.tsx`,
   `apps/ui/src/components/graph/EvidencePanel.module.css`,
   `apps/ui/src/components/graph/evidencePanel.ts`,
   `apps/ui/src/components/graph/evidencePanel.test.ts`, the files holding `EvidenceTab` and
   `TABS` and the deep link's test, `tests/ui_contracts/test_evidence_panel_contract.py`,
   `tests/ui_contracts/test_ownership_view_contract.py`, and `.agent/handoff.md`. Report the list
   you measure with `git diff --name-only 36d5c359` after C6. Touch nothing else.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. A test this round itself wrote that is wrong may be
   corrected before C6, and the correction is declared. An EXISTING assertion that goes red,
   other than the tab lists S3 orders grown, is never edited to pass; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave every existing worktree, branch, stash and process alone. The worktree G5 adds goes
   under `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l`
   and the `remedy/*` branch count are reported afterwards; neither may change.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F035's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C6 is written.

G1 TRANSPORT AND BOOKING — each payload's line count, byte count and sha256 against the PAYLOADS table, then
 each `.agent/authored/f035-r6-*` payload copy compared byte for byte with its source, read back
 with `git show <C1>:<path>`. One reading per copy.

 Then the booking: the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2340753 | 43c1bcdcd5c1c86dd2cdc850c9c770216ae6ff5af146af67bfdc1c6c180ee55f |
 | .agent/live_review.md | 318081 | e06a5f28de49d41ee9c3b3da1d375cd25777e614a6554802cc7c04a4c0d2fb02 |
 | .agent/plan.md | 914 | 44cb05f4b87d1302a9c53516d3cc6c813c7451d633e707b2f0aff6808e6f0aaa |
 | docs/ui/design_reference/assumption_log.md | 23419 | a33524aa9cf3c2f7332242c1944caeb67fca529c367644703691c461b7171350 |
 Also `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's text at C2, which
 the reviewer read as `[]`, and the count of lines beginning `Landed: R-1082` there, which is 0.

G2 THE CODE — `python3 -m ruff check tests/ui_contracts/test_evidence_panel_contract.py
 tests/ui_contracts/test_ownership_view_contract.py` with its real exit code, and, quoted from
 `git show <C3>`, `ownershipPanelState` and `OwnershipTab`.

G3 THE TESTS — in the primary checkout at C3, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/ui_server/test_ownership_route.py "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" tests/orchestration/test_ownership_phrases.py tests/orchestration/test_ownership_ledger.py tests/orchestration/test_pingpong_job_ownership.py tests/cli/test_job_ownership.py tests/regression/test_named_bugs.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -16; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection, serially, in the primary checkout at `36d5c359`, and read
 `1649 passed, 11 skipped` at real exit code 0; the skips are the F252 quarantines. Report every
 `SKIPPED` line and account for the new total. Then `python3 -m apps.cli.main integrity check
 --json`, which must read all six checks `pass`.

G4 THE RENDER — `python3 .agent/authored/f035-r6-render_measure.py` at C3, its whole output with
 its real exit code, which must be 0 with every check C-a to C-f passing; then `git worktree list
 | wc -l`, `git status --porcelain` and `ls .remedy-wt/f035-render-run`, which must show the work
 dir gone. Save the output as `.agent/authored/f035-r6-render.txt` for C4.

G5 THE RED PROOFS — your tool `.agent/authored/f035-r6-mutations.py` follows G5 of
 `.agent/authored/f035-r5-block.md`: PYTHON runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/ui_contracts/test_evidence_panel_contract.py tests/ui_contracts/test_ownership_view_contract.py`
 from the worktree's root; VITEST runs the primary's vitest over the worktree's
 `ownership.test.ts`, `evidencePanel.test.ts` and `zoomDeepLink.test.ts` through a scratch config
 under `.remedy-wt/f035-r6-worker/`; controls of each runner first and last; one line per
 mutation; `restored byte-identical: True` per file; the primary's `git status --porcelain`,
 empty; and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.
  m1 VITEST `ownership.ts`: an errored view reads as `empty`;
  m2 VITEST `ownership.ts`: a loaded view reads as `loading`;
  m3 VITEST `evidencePanel.ts`: the ownership entry is left out of `EVIDENCE_TABS`;
  m4 VITEST the deep link's `TABS`: `ownership` is left out;
  m5 PYTHON `EvidencePanel.tsx`: the ownership line is removed from the tab bodies;
  m6 PYTHON `EvidencePanel.tsx`: `OwnershipTab`'s effect loses its `cancelled` guard.
 Run it at C5 in `.remedy-wt/f035-r6-mut` and report its whole output. EVERY mutation must be red;
 one that stays green is reported as green, never papered over, and you add the test that
 catches it before C6 and re-run the tool. Then remove the worktree and `git worktree prune`.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C6 down to C1 and `36d5c359` in that order (more lines
 if constraint 2 split a commit); the worktree and `remedy/*` counts, equal to your step 4
 readings; the push's real outcome; and `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, which must be EMPTY. These go in your reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 to C5), every gate's real
output and exit code, the authored-text proofs, the item-status table AGENTS.md requires (one row
per commit and per gate), the deviations, and the next expected action. Report what you ran, not
what you expected to find. Your Session section reads SESSION 1 of feature F035, round 6, and says
in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 6, then the end-to-end proof — one real job through the command line and the browser's
door. State the open-findings count, 0, and the operator-questions count, 0.
