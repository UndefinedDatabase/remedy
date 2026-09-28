STEP F035 R8 — THE CLOSURE SEQUENCE'S FIRST ROUND: book round 7, register and repair R-1085 and R-1086, write the Built State, consolidate the checklist, and take the feature's one full suite

GOAL
Book round 7's PASS with the resolutions of R-1083 and R-1084, register R-1085 and R-1086 and
record DECISION F035 D8; repair both findings; append the Built State to
`docs/roadmap/features/T5_F035.md` and run the checklist consolidation (it joins nothing and keeps
`docs/agents/planner_reviewer_prompt.md` §3 at 34 items); then run this feature's ONE full suite
on the tree that ships and commit its transcript. The self-use generator's reading waits for the
next round, because it mints a job for any open finding and R-1085 and R-1086 are resolved only by
the next round's booking; the evidence bundle, the review package, the rotation, the STATUS line
and the pull request belong to later rounds.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, write the handback. You never
issue a verdict, never merge, and never write a `Done:` line. Read first:
`docs/roadmap/STATUS_closure_protocol.md` preconditions 2, 3 and 7, `docs/agents/integration_gate.md`,
R-1085, R-1086 and DECISION F035 D8 in the payloads, `.ownershipList` in both
`apps/ui/src/components/graph/EvidencePanel.module.css` and
`apps/ui/src/components/detail/DetailPopover.module.css`, the R-1083 test of
`tests/ui_contracts/test_ownership_view_contract.py`, and the module docstring of
`tests/ui_server/test_ownership_e2e_live.py`.

THE DIRECTORIES
  `.remedy-wt/f035-r8-payloads/` and `.remedy-wt/f035-r8/`  READ-ONLY. The reviewer's.
  `.remedy-wt/f035-r8-sim/`, `.remedy-wt/f035-review/` and every older `f035-*` path: the
  reviewer's; do not touch them.
  `.remedy-wt/f035-r8-worker/`   YOURS for logs and scripts; create it if absent. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR: `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`,
`cp`, process and command substitution, `cd <dir> && git ...`, `for` loops, and one-liners chained
with `;` or `&&` outside a `bash -c`. Capture exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`,
read `${PIPESTATUS[0]}` when you pipe. Use `git -C <path>`; never `cd` into a worktree. Write any
script holding a dollar-brace or a brace-quote shape to a file under your own directory and run it.
The ONE npm command this round may run is C6's `npm --prefix apps/ui run build`; never `npm
install`, `npm ci` or `npx`. Never `git stash`, never `pkill -f`. The `remedy` command is denied;
use `python3 -m apps.cli.main` where a gate names it.

COMMIT TRAILER — every commit ends with exactly this line:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop.
2. In `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain` empty,
   `git branch --show-current` `feature/f035-ownership-ledger`, `git log --oneline -1` `9c42693f`.
3. Measure this block's line count and sha256 (`.remedy-wt/f035-r8/block.md`) against your
   delegation message's readings; stop if either differs.
4. Report `git worktree list | wc -l` and `git branch --list 'remedy/*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f035-r8-payloads/`; verify each one's line count, byte count and sha256
BEFORE use and report every reading. Never retype or edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| booking.diff | 46 | 11027 | e79dfa7046fa5526f2e3efdae80dbc7aee8cb5035bcdd74114f08dcf6e90b3f0 |
| closure_docs.diff | 110 | 8738 | e92816286879438731ce16dce0085418f85d56a03834436a3000fbed33392a8c |
| plan.md | 29 | 1033 | fb11f045b48acc4dba3e8c48539d2245768071d2e9b6cf7308b0cb6124b34b1c |

`plan.md` REWRITES `.agent/plan.md`. `booking.diff` (`git diff HEAD` from a tree at `9c42693f`)
removes the `Landed:` lines of R-1083 and R-1084 from `.agent/live_review.md` and appends round
7's gate entry, the registrations of R-1085 and R-1086 and the `Done:` resolutions of R-1083 and
R-1084; and appends DECISION F035 D8 to `.agent/decisions.md`. `closure_docs.diff`, generated in
the same tree, appends the Built State to `docs/roadmap/features/T5_F035.md` and inserts, in
`docs/agents/planner_reviewer_prompt.md`, the consolidation paragraph directly before the line
`  The next consolidation measures against 34.` (containment test: TO contains FROM: true — an
APPEND; that line occurs once before and once after).

BUNDLE — commits in this order.
C1 COPIES: `.agent/authored/f035-r8-block.md` := this block and each payload as
   `.agent/authored/f035-r8-<name>`, by `shutil.copyfile`. Subject `F035 R8 C1: copy round 8 block
   and payloads`. Its insertions are this block's line count plus 185.
C2 RECORDS: `git apply` booking.diff, then `.agent/plan.md` := plan.md. Subject `F035 R8 C2: book
   round 7, resolve R-1083 and R-1084, register R-1085 and R-1086, record D8`. Expected by
   `git show --numstat`: 19/0 .agent/decisions.md, 8/2 .agent/live_review.md, 9/9 .agent/plan.md.
C3 THE REPAIRS. R-1085: in both CSS modules, `.ownershipList li + li` sets `margin-top: 6px`, under
   a one-line comment saying the design reference has no spacing token; the contract test gains one
   test that neither module's `.ownershipList` rules name `--remedy-radius`. R-1086: the docstring
   of `tests/ui_server/test_ownership_e2e_live.py` says the run ends blocked because every
   remaining task was vetoed, in place of "completes normally" and "nothing parks"; nothing else in
   that file changes. Append `Landed: R-1085 — …` and `Landed: R-1086 — …`, one line each naming
   the files and this commit, to `.agent/live_review.md`. Subject `F035 R8 C3: repair R-1085 and
   R-1086`.
C4 YOUR MUTATION TOOL `.agent/authored/f035-r8-mutations.py`, after G4. Subject `F035 R8 C4: add the
   round 8 mutation tool`.
C5 THE BUILT STATE AND THE CONSOLIDATION: `git apply` closure_docs.diff. Subject `F035 R8 C5: write
   the Built State and consolidate the checklist`. Expected by `git show --numstat`: 8/0
   docs/agents/planner_reviewer_prompt.md, 83/0 docs/roadmap/features/T5_F035.md.
C6 THE INTEGRATION GATE, in the PRIMARY checkout, after C5. (a)
   `bash -c 'npm --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'` — a
   failing build is a STOP — then `git status --porcelain`, still empty. (b)
   `python3 -m pytest -n auto -q`, its log under `.remedy-wt/f035-r8-worker/`; measure its wall
   time. Write `.agent/authored/f035-closure-suite.txt` holding the command, the real exit code, the
   wall time, the summary line, the FULL list of bad node ids (failed plus errors) or the literal
   `NONE`, and one line naming the tree it ran on (C5's SHA). (c) Rewrite `.agent/handoff.md` per
   `docs/agents/handback_template.md` and commit it TOGETHER with the transcript. Subject
   `F035 R8 C6: record the closure suite transcript and rewrite handoff for round 8`. Then
   `git push origin feature/f035-ownership-ledger`. No pull request.

CONSTRAINTS
1. Never edit or retype a payload; `git apply --check` before each `git apply`, exit codes reported.
2. Every commit under 500 insertions by `git show --numstat`; split one that would reach it, and
   say so.
3. The round's tracked path set: the `.agent/authored/f035-r8-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the two CSS modules,
   `tests/ui_contracts/test_ownership_view_contract.py`,
   `tests/ui_server/test_ownership_e2e_live.py`, `docs/roadmap/features/T5_F035.md`,
   `docs/agents/planner_reviewer_prompt.md`, `.agent/authored/f035-closure-suite.txt` and
   `.agent/handoff.md`. No edit to `README.md`, `docs/roadmap/STATUS.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md`, `scripts/self_use_queue.json` or any other file.
4. A RED full suite in C6 is this feature's work, not a stop: commit the transcript exactly as
   measured, report every bad node id, and hand back; the repair rounds are the reviewer's to order
   (amend0917-throughput rule 2). Never weaken an assertion, delete a test or mark anything xfail.
5. Any other red gate: STOP, commit and push what is verified, hand back under AGENTS.md "If
   Blocked". Nothing is merged; no `gh pr create`; no force-push; no evidence job; no zip; do not
   run the self-use generator.
6. Leave every existing worktree, branch and stash alone. The worktree G4 adds goes under
   `.remedy-wt/` and is removed as that gate's last action.
7. The full suite runs ONCE, in C6, and nowhere else this round (amend0917 rule 1).

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G4 run
before C6 is written; G5 is C6's suite.
G1 TRANSPORT AND RECORDS: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f035-r8-*` payload copy byte-equal to its source by `git show <C1>:<path>`; and
   `git show <read at>:<path>` of each file below hashes to the reviewer's simulation:
   | read at | path | bytes | sha256 |
   |---|---|---|---|
   | C2 | .agent/live_review.md | 330639 | 18b60ad9c28928966cced64e1e9d964ca265fc70aecf8ad6c07bf1903430a2d9 |
   | C2 | .agent/decisions.md | 2344873 | 4ecf75a9f53ad403edf83167bd594fb183f79c114dfa02efa1abd69962fb0f9a |
   | C2 | .agent/plan.md | 1033 | fb11f045b48acc4dba3e8c48539d2245768071d2e9b6cf7308b0cb6124b34b1c |
   | C5 | docs/roadmap/features/T5_F035.md | 11421 | 15c13450cb2f978129dbede9948fcbf1067a1bf55498f6aeeb6de360d268b98b |
   | C5 | docs/agents/planner_reviewer_prompt.md | 108703 | f56e558c318dd471bd517716154d7b2b69fc48f7a1455cc16502e18ac8e94696 |
   `open_finding_ids` of `scripts/rotate_live_review.py` over the ledger reads `['R-1085',
   'R-1086']` at C2; lines beginning `Landed: R-1083` or `Landed: R-1084` there: 0; and
   `live_checklist_items` of `packages/orchestration/block_lint.py` over the planner prompt reads
   the same 34 numbers at `9c42693f` and at C5.
G2 THE LINTER: `python3 -m apps.cli.main integrity block .remedy-wt/f035-r8/block.md` at C5, real
   exit code 0, whole output.
G3 THE TESTS AND THE TREE, in the primary checkout at C5, serially:
   `bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/docs/ tests/orchestration/test_block_lint.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/ui_contracts/test_ownership_view_contract.py tests/ui_contracts/test_raw_colour_ratchet.py tests/ui_server/test_ownership_e2e_live.py tests/ui_server/test_dashboard_contract.py tests/cli/test_golden_path.py 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'`
   — exit 0, the summary line and every SKIPPED line reported; then `python3 -m apps.cli.main
   integrity check --json`, six `pass` at `fail_count` 0 — the status of each check is the
   reading, not the exit code; and `git status --porcelain` empty with no untracked file (closure
   precondition 3).
G4 THE RED PROOFS, at C3 in a disposable worktree `.remedy-wt/f035-r8-mut`: your tool edits the
   named file inside it (its FROM text occurring exactly once), runs `python3 -B -m pytest -q -p
   no:cacheprovider tests/ui_contracts/test_ownership_view_contract.py` from its root, restores
   the bytes, and prints one line per mutation, controls first and last, `restored byte-identical:
   True`, the PRIMARY checkout's `git status --porcelain`, empty, and `ALL MUTATIONS CAUGHT AND
   RESTORED CLEANLY: <bool>`.
    m1 `EvidencePanel.module.css`: the row gap reads `var(--remedy-radius-sm)` again;
    m2 `DetailPopover.module.css`: the row gap reads `var(--remedy-radius-sm)` again.
   Every mutation must be red; one that stays green is reported, and you add the test that catches
   it before C6. Remove the worktree afterwards and report `git worktree list | wc -l`.
G5 THE INTEGRATION GATE: the UI build's last line and real exit code; `git status --porcelain`
   after it; then the full suite's real exit code, wall time, summary line and every bad node id,
   all in `.agent/authored/f035-closure-suite.txt`; and whether
   `tests/orchestration/test_import_reachability.py` or `tests/test_no_orphan_modules.py` holds a
   bad node (closure precondition 7).
G6 AFTER C6 AND THE PUSH, in your final reply only: `git status --porcelain` empty, the local tip
   equal to `origin/feature/f035-ownership-ledger`, `git log --oneline -n 7`, `git worktree list |
   wc -l`, `git branch --list 'remedy/*' | wc -l`, the push's real outcome, and `gh pr list --state
   open --json number` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block, the
per-commit changed-files table with the `git show --numstat` counts you measured beside the ones
above, every gate's real output, the full suite's summary line and bad node ids, the authored-text
proofs, the item-status table AGENTS.md requires (one row per commit, per gate and per finding),
the deviations, and the next action. Session section: SESSION 1 of feature F035, round 8, rounds so
far 8, plus one sentence on how much context you had left. `## Next`: Phase 1 rule 1, the review of
round 8 including the repairs of R-1085 and R-1086, then the closure's evidence round — the
booking of round 8 with those findings' resolutions, the self-use generator's reading, any repair
the suite requires, the evidence bundle and the review package — and then the closing round. State
the open-findings count, 2 (R-1085 and R-1086, landed and awaiting review), and "Operator questions
open: 0".
