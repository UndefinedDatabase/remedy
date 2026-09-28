STEP F036 R7 — THE CLOSURE SEQUENCE'S FIRST ROUND: book round 6, register and repair R-1090, write the Built State, consolidate the checklist, and take the feature's one full suite

GOAL
Book round 6's PASS with the resolutions of R-1088 and R-1089 and the registration of R-1090,
and F036's two prose-slip lines; repair R-1090, the docked tour card that wraps its "Show me"
label, and prove it with the render harness; append the Built State to
`docs/roadmap/features/T5_F036.md` and run the checklist consolidation (it joins nothing and keeps
`docs/agents/planner_reviewer_prompt.md` §3 at 34 items); then run this feature's ONE full suite
on the tree that ships and commit its transcript. The self-use item, the evidence bundle, the
review package, the rotation, the STATUS line and the pull request belong to later rounds.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict, never merge, and never write a `Done:` line. Read first:
`docs/roadmap/STATUS_closure_protocol.md` preconditions 2, 3 and 7, `docs/agents/integration_gate.md`,
R-1090 in the booking diff, `apps/ui/src/components/tour/TourOverlay.module.css`, the actions row
of `TourOverlay.tsx`, `tests/ui_contracts/test_tour_overlay_contract.py`, the six
`.agent/authored/f036-r6-render_*` files, `.agent/authored/f036-r6-render.txt` and
`.agent/authored/f036-r6-mutations.py`.

THE DIRECTORIES
  `.remedy-wt/f036-r7-payloads/` and `.remedy-wt/f036-r7/`  READ-ONLY. The reviewer's.
  `.remedy-wt/f036-r7-sim/`, `.remedy-wt/f036-r7-src/`, `.remedy-wt/f036-review/` and every older
  `f036-*` path: the reviewer's; do not touch them.
  `.remedy-wt/f036-r7-worker/`   YOURS for logs, scripts and screenshots; create it if absent.
  `.remedy-wt/f036-render-run/` is the render harness's own work dir. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR: `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`,
`cp`, `sed`, process and command substitution, `cd <dir> && git ...`, `for` loops, and one-liners
chained with `;` or `&&` outside a `bash -c`. Capture exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe. Use
`git -C <path>`; never `cd` into a worktree. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`); write any script holding a dollar-brace to a file under your own
directory and run it. The ONE npm command this round may run is C7's
`npm --prefix apps/ui run build`; never `npm install`, `npm ci` or `npx`. Never `git stash`, never
`pkill -f`: stop a process only by its own recorded pid. The `remedy` command is denied; use
`python3 -m apps.cli.main` where a gate names it.

COMMIT TRAILER — every commit ends with exactly this line:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. In `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain` empty,
   `git branch --show-current` `feature/f036-guided-result-tour`, `git log --oneline -1`
   `032c1ce2`.
3. Measure this block's line count and sha256 (`.remedy-wt/f036-r7/block.md`) against your
   delegation message's readings; report both beside both, and stop if either differs.
4. Report `git worktree list | wc -l` and `git branch --list 'remedy/*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f036-r7-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE use and report every reading. Never retype or edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| booking.diff | 26 | 8386 | 37c1472d39f853dd18c48c54620e50a47a16c18e1ea400483fdb02d83ee552dd |
| closure_docs.diff | 122 | 9739 | 98c5969890cc1113f49a7919b3c5c501f753183a0452307af53faf7cf47faaa1 |
| plan.md | 30 | 1109 | 4bae9ddf5bfc2f8993f881062877519dcce4239dddc210532fbfe8d6465d88bf |

`plan.md` REWRITES `.agent/plan.md`. `booking.diff`, generated with `git diff HEAD` from a tree at
`032c1ce2`, appends to `.agent/live_review.md` round 6's gate entry, the `Done:` resolutions of
R-1089 and R-1088 and the registration of R-1090, and appends F036's two lines to
`.agent/prose_slips.md`. `closure_docs.diff`, generated in the same tree, appends the Built State
to `docs/roadmap/features/T5_F036.md` and inserts, in `docs/agents/planner_reviewer_prompt.md`,
the consolidation paragraph directly before the line
`  The next consolidation measures against 34.` (containment test: TO contains FROM: true — an
APPEND; that line occurs once before and once after).

THE SPECIFICATION. No raw colour, no new file under `apps/` or `packages/`.
S1 R-1090, THE REPAIR, in `apps/ui/src/components/tour/TourOverlay.module.css` only:
   (a) `white-space: nowrap;` becomes the last declaration of the `.actions button` rule;
   (b) directly after the closing brace of the `.card[data-shown="true"]` rule, a two-line comment
   saying the docked card is the left rail's width, too narrow for Previous, Next and "Show me" in
   one row, so the row wraps instead of a label (R-1090), then the one-line rule
   `.card[data-shown="true"] .actions { flex-wrap: wrap; }`. Nothing else in the file changes.
S2 THE TEST: `tests/ui_contracts/test_tour_overlay_contract.py` gains, directly after
   `test_the_card_carries_data_shown_and_docks_over_the_left_rail_while_shown`, one test
   `test_an_action_label_stays_on_one_line_and_the_docked_row_wraps` that reads the CSS module and
   asserts `white-space: nowrap;` inside the `.actions button {` rule's own braces and the literal
   `.card[data-shown="true"] .actions { flex-wrap: wrap; }` in the file. Nothing else changes.
S3 THE RENDER, NEW files `.agent/authored/f036-r7-render_` + `index.html`, `main.tsx`,
   `vite.config.mjs`, `measure.py` and `drive.mjs`, byte-copies of round 6's by `shutil.copyfile`,
   except `drive.mjs`, whose two screenshot paths name `.remedy-wt/f036-r7-worker/` in place of
   `.remedy-wt/f036-r6-worker/`, and which adds C-k and prints `RENDER: <n> of 11 checks pass`.
   C-k runs right
   after C-i's measurement and before the ArrowRight that follows it, with the shown screenshot
   already taken: for each of the card's buttons whose text is `Previous`, `Next` or `Show me`, a
   `Range` over the button's text gives `getClientRects()` whose distinct rounded `top` values
   number exactly 1, and the button's box lies inside the card's box (left, right and bottom). As
   its RED CONTROL, C-k then adds one `<style>` element to the page that restores round 6's rules
   — `white-space: normal !important` on those buttons and `flex-wrap: nowrap !important` on their
   row — re-counts, requires at least one label with two or more lines, and removes the element.
   C-k passes only when both halves hold, and prints both counts. Its output is saved as
   `.agent/authored/f036-r7-render.txt`.

BUNDLE — commits in this order.
C1 COPIES: `.agent/authored/f036-r7-block.md` := this block and each payload as
   `.agent/authored/f036-r7-<name>`, by `shutil.copyfile`. Subject `F036 R7 C1: copy round 7 block
   and payloads`. Its insertions are this block's line count plus 178.
C2 RECORDS: `git apply --check` then `git apply` booking.diff, then `.agent/plan.md` := plan.md.
   Subject `F036 R7 C2: book round 6, resolve R-1088 and R-1089, register R-1090`. Expected by
   `git show --numstat`: 8/0 .agent/live_review.md, 9/6 .agent/plan.md, 2/0 .agent/prose_slips.md.
C3 THE REPAIR: S1 and S2, then append to `.agent/live_review.md`, preceded by a blank line, one
   line `Landed: R-1090 — <one sentence naming the CSS module and this change>`. Subject
   `F036 R7 C3: keep the tour's action labels on one line in the docked card`.
C4 THE RENDER: S3's files and `f036-r7-render.txt`, after G3's first run. Split under constraint 2 if needed
   (round 6's two parts measured 360 and 390). Subject `F036 R7 C4: render the docked card's
   actions again` (with ` (1/2)` and ` (2/2)` if split).
C5 YOUR MUTATION TOOL `.agent/authored/f036-r7-mutations.py`, BEFORE G4 runs. Subject `F036 R7 C5: add
   the round 7 mutation tool`.
C6 THE BUILT STATE AND THE CONSOLIDATION: `git apply --check` then `git apply`
   closure_docs.diff. Subject `F036 R7 C6: write the Built State and consolidate the checklist`.
   Expected by `git show --numstat`: 8/0 docs/agents/planner_reviewer_prompt.md, 95/0
   docs/roadmap/features/T5_F036.md.
C7 THE INTEGRATION GATE, in the PRIMARY checkout, after C6. (a)
   `bash -c 'npm --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'` — a
   failing build is a STOP — then `git status --porcelain`, still empty. (b)
   `python3 -m pytest -n auto -q`, its log under `.remedy-wt/f036-r7-worker/`; measure its wall
   time. Write `.agent/authored/f036-closure-suite.txt` holding the command, the real exit code,
   the wall time, the summary line, the FULL list of bad node ids (failed plus errors) or the
   literal `NONE`, and one line naming the tree it ran on (C6's SHA). (c) Rewrite
   `.agent/handoff.md` per `docs/agents/handback_template.md` and commit it TOGETHER with the
   transcript. Subject `F036 R7 C7: record the closure suite transcript and rewrite handoff for
   round 7`. Then `git push origin feature/f036-guided-result-tour`. No pull request.

CONSTRAINTS
1. Never edit or retype a payload; report each `git apply --check` and `git apply` exit code.
2. Every commit under 500 insertions by `git show --numstat`; split one that would reach it into
   parts with their own subjects, and say so.
3. The round's tracked path set: the `.agent/authored/f036-r7-*` files,
   `.agent/live_review.md`, `.agent/prose_slips.md`, `.agent/plan.md`,
   `apps/ui/src/components/tour/TourOverlay.module.css`,
   `tests/ui_contracts/test_tour_overlay_contract.py`, `docs/roadmap/features/T5_F036.md`,
   `docs/agents/planner_reviewer_prompt.md`, `.agent/authored/f036-closure-suite.txt` and
   `.agent/handoff.md`. Report `git diff --name-only 032c1ce2` at the tip. No edit to
   `README.md`, `docs/roadmap/STATUS.md`, `.agent/decisions.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md`, `scripts/self_use_queue.json` or any other file.
4. A RED full suite in C7 is this feature's work, not a stop: commit the transcript exactly as
   measured, report every bad node id, and hand back; the repair rounds are the reviewer's to order
   (amend0917-throughput rule 2). Never weaken an assertion, delete a test, skip or mark anything
   xfail. An EXISTING test that goes red before C7 is never edited to pass; report it and stop.
5. Any other red gate: STOP, commit and push what is verified, hand back under AGENTS.md "If
   Blocked". Nothing is merged; no `gh pr create`; no force-push; no evidence job; no zip; do not
   run the self-use generator or runner.
6. Leave every existing worktree, branch and stash alone, the `.remedy-wt/job-*` worktrees and
   the reviewer's `f036-r7-sim` included. The worktree G4 adds goes under `.remedy-wt/` and is
   removed as that gate's last action.
7. The full suite runs ONCE, in C7, and nowhere else this round (amend0917 rule 1).

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a word
is a finding. G1 to G4 run before C7 is written; G5 is C7's suite.
G1 TRANSPORT AND RECORDS: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f036-r7-*` payload copy byte-equal to its source by `git show <C1>:<path>`;
   and `git show <read at>:<path>` of each file below hashes to the reviewer's simulation:
   | read at | path | bytes | sha256 |
   |---|---|---|---|
   | C2 | .agent/live_review.md | 338454 | e45f5447f9198ef53b47fd484e25438cb9e1808b41af22a1f3e13c6a3cf63861 |
   | C2 | .agent/prose_slips.md | 376317 | fab563682ec66c60d366c91d5fa1ba7cf9d9d0267795a1ff888458edf0a51025 |
   | C2 | .agent/plan.md | 1109 | 4bae9ddf5bfc2f8993f881062877519dcce4239dddc210532fbfe8d6465d88bf |
   | C6 | docs/roadmap/features/T5_F036.md | 12363 | 22a1cf9e9c8b9a7403d0e36b6e3498e4f5b210cd77cc9c5dd0b260a97a5d44a8 |
   | C6 | docs/agents/planner_reviewer_prompt.md | 109446 | b6b7565f213a288e82b1cbd7071a53805048f58e4fde92de824860454aebead3 |
   `open_finding_ids` and `latest_gate_verdict` of `scripts/rotate_live_review.py` over the ledger
   at C2 read `['R-1090']` and `PASS`; and `live_checklist_items` of
   `packages/orchestration/block_lint.py` over the planner prompt reads 34 items at `032c1ce2`
   and at C6.
G2 THE CODE AND THE TESTS, in the primary checkout at C6, serially: `python3 -m ruff check
   tests/ui_contracts/test_tour_overlay_contract.py .agent/authored/f036-r7-render_measure.py
   .agent/authored/f036-r7-mutations.py`, real exit code; then
   `bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/docs tests/cli/test_golden_path.py tests/orchestration/test_block_lint.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py 2>&1 | tail -8; echo "REAL_EXIT=${PIPESTATUS[0]}"'`
   — exit 0, the summary line and every SKIPPED line reported; then `python3 -m apps.cli.main
   integrity check --json`, six `pass` at `fail_count` 0 — the status of each check is the
   reading, not the exit code; then `python3 -m apps.cli.main integrity block
   .remedy-wt/f036-r7/block.md`, real exit code and whole output; and `git status --porcelain`
   empty with no untracked file (closure precondition 3). Quote the CSS diff of C3 whole.
G3 THE RENDER, at C3: while you build S3, run your drafts as
   `python3 .remedy-wt/f036-r7-worker/f036-r7-render_measure.py /home/decodeux/Repos/remedy` (the
   runner finds its sibling files by its own name's prefix); the run whose output C4 commits must
   print `RENDER: 11 of 11 checks pass`, exit 0, and leave no `.remedy-wt/f036-render-run` behind.
   After C4, run `python3 .agent/authored/f036-r7-render_measure.py /home/decodeux/Repos/remedy`
   once more, report its last three lines, C-k's printed counts, both screenshots' paths and
   sizes, and `git status --porcelain` empty.
G4 THE RED PROOFS, at C5 in a disposable worktree `.remedy-wt/f036-r7-mut`: your tool, modelled
   on round 6's CONTRACT route, edits the named file inside it (its FROM text occurring exactly
   once), runs `python3 -B -m pytest -q -p no:cacheprovider
   tests/ui_contracts/test_tour_overlay_contract.py` from its root, restores the bytes, and prints
   one line per mutation, controls first and last, `restored byte-identical: True`, the PRIMARY
   checkout's `git status --porcelain`, empty, and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY:
   <bool>`:
    m1 `TourOverlay.module.css`: the `white-space: nowrap;` line is removed;
    m2 `TourOverlay.module.css`: the `.card[data-shown="true"] .actions` rule line is removed.
   Every mutation must be red; one that stays green is reported, and you add the test that catches
   it and re-run before C6. Remove the worktree afterwards, `git worktree prune`, and report
   `git worktree list | wc -l`.
G5 THE INTEGRATION GATE: the UI build's last line and real exit code; `git status --porcelain`
   after it; then the full suite's real exit code, wall time, summary line and every bad node id,
   all in `.agent/authored/f036-closure-suite.txt`; and whether
   `tests/orchestration/test_import_reachability.py` or `tests/test_no_orphan_modules.py` holds a
   bad node (closure precondition 7).
G6 AFTER C7 AND THE PUSH, in your final reply only: `git status --porcelain` empty, the local tip
   equal to `origin/feature/f036-guided-result-tour`, `git log --oneline -n 9`,
   `git worktree list | wc -l`, `git branch --list 'remedy/*' | wc -l`, the push's real outcome,
   and `gh pr list --state open --json number` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the `git show --numstat` counts you measured beside the
ones above, every gate's real output, the full suite's summary line and bad node ids, the
authored-text proofs, the item-status table AGENTS.md requires (one row per commit, per gate and
per finding), the deviations, and the next action. Session section: SESSION 2 of feature F036,
round 7, rounds so far 7, plus one sentence on how much context you had left. `## Next`: Phase 1
rule 1, the review of round 7 including the repair of R-1090, then the closure's evidence round —
the booking of round 7 with R-1090's resolution, the self-use item, any repair the suite
requires, the evidence bundle and the review package — and then the closing round. State the
open-findings count, 1 (R-1090, landed and awaiting review), and "Operator questions open: 1".
