STEP F286 R2 — THE CLOSURE SEQUENCE'S FIRST ROUND: book round 1 with R-1104's resolution, take the self-use reading, write the Built State and the checklist consolidation, and take the feature's one full suite

GOAL
Round 1 is reviewed PASS at `a45f74da`. Book its verdict with R-1104's resolution and the plan;
take closure precondition 6's self-use reading, which the reviewer's own run over the same booking
read as `None`; append F286's Built State to its feature file and the checklist consolidation to
the planner prompt; then run this feature's ONE full suite on the tree that ships and commit its
transcript. The evidence bundle, the review package, the rotation, the next paydown's registration,
the STATUS line and the pull request belong to later rounds.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict, never merge, and never write a `Done:` line of your own. No production file
changes this round; the records and the documents travel as payloads. Read first:
`docs/roadmap/STATUS_closure_protocol.md` preconditions 2, 3, 4, 6 and 7 and
`docs/agents/integration_gate.md`.

THE DIRECTORIES
  `.remedy-wt/f286-r2-payloads/` and `.remedy-wt/f286-r2/`  READ-ONLY. The reviewer's.
  every other `.remedy-wt/f286-*` path: the reviewer's; do not touch.
  `.remedy-wt/f286-r2-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR: `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`,
`cp`, `ln`, `sed`, process and command substitution, `cd <dir> && ...`, `for` loops, and one-liners
chained with `;` or `&&` outside a `bash -c`. Capture exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe. Use
`git -C <path>`; never `cd` into a worktree. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`); write any script holding a dollar-brace or a brace next to a quote to
a file under your own directory and run it; run a program in another directory with
`subprocess.run(..., cwd=...)`. Never run npm or npx. Never `git stash`, never `pkill -f`: stop a
process only by its own recorded pid. The `remedy` command may be denied; use
`python3 -m apps.cli.main` where a gate names it.

COMMIT TRAILER — every commit ends with exactly this line:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. In `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain` empty,
   `git branch --show-current` `feature/f286-findings-paydown-v5`, `git log --oneline -1`
   `a45f74da2`.
3. Measure this block's line count and sha256 (`.remedy-wt/f286-r2/block.md`) against your
   delegation message's readings; report both beside both, and stop if either differs.
4. Report `git worktree list | wc -l` and `git branch --list 'remedy/*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f286-r2-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE use and report every reading. Never retype or edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 28 | 909 | 1c861a4d6e4d85151a4283ed2da3d1e950364bbae058cfbd469c1d7da00f416f |
| records.diff | 12 | 7455 | 90556ec184a3bde254cb6bfed4a8dd991cc14e3fb4993e4e9ab9d54470e26e36 |
| closure_docs.diff | 33 | 2240 | cab14a7c2a3709f38f4a1c0de6ae20f54df6fc49f243f04dcdd3f4ed805833cc |

`plan.md` REWRITES `.agent/plan.md`. Both diffs were generated with `git diff HEAD` from the
reviewer's tree at `a45f74da` and go on with `git apply`. `records.diff` appends to
`.agent/live_review.md` round 1's gate entry, VERDICT PASS, and R-1104's `Done:` resolution, which
the reviewer authored. `closure_docs.diff` appends the Built State to
`docs/roadmap/features/T2_F286.md` and inserts the consolidation paragraph directly before the line
`  The next consolidation measures against 34.` of `docs/agents/planner_reviewer_prompt.md`.

BUNDLE — commits in this order.
C1 COPIES: `.agent/authored/f286-r2-block.md` := this block and each payload as
   `.agent/authored/f286-r2-<name>`, by `shutil.copyfile`. Subject `F286 R2 C1: copy round 2
   block and payloads`. Its insertions are this block's line count plus 73; STOP rather than
   commit at 500 or more.
C2 RECORDS: `git apply --check` then `git apply` records.diff, then `.agent/plan.md` := plan.md.
   Subject `F286 R2 C2: book round 1's PASS with R-1104's resolution`. Expected by
   `git show --numstat`: 4/0 .agent/live_review.md, 10/8 .agent/plan.md.
S  THE SELF-USE READING, after C2 and before C3, in the primary checkout, from a Python script:
   call `generate_and_append_if_empty()` of `packages.orchestration.self_use_generator` and then
   `next_self_use_item()` of `packages.orchestration.self_use_queue`, both with no argument, and
   report both return values and `git status --porcelain` after them. The reviewer's run of the
   same two calls in its tree carrying the same C2 read `None` and `None` and wrote nothing. If
   either answers anything but `None`, or the tree is not clean after them, STOP before C3:
   commit nothing more, and hand back with the item's full contents, because the Built State C3
   writes says the reading was `None`.
C3 THE DOCUMENTS: `git apply --check` then `git apply` closure_docs.diff. Subject `F286 R2 C3:
   write the Built State and the checklist consolidation`. Expected by `git show --numstat`:
   4/0 docs/agents/planner_reviewer_prompt.md, 10/0 docs/roadmap/features/T2_F286.md.
C4 THE INTEGRATION GATE, in the PRIMARY checkout, after C3 and after G1 and G2. (a) run
   `apps/ui/node_modules/.bin/vite build` with `cwd` `apps/ui` from a Python script, report its exit
   code and last line — a failing build is a STOP — then `git status --porcelain`, still empty.
   (b) `python3 -m pytest -n auto -q`, its log under `.remedy-wt/f286-r2-worker/`; measure its wall
   time. Write `.agent/authored/f286-closure-suite.txt` holding the command, the real exit code, the
   wall time, the summary line, the FULL list of bad node ids (failed plus errors) or the literal
   `NONE`, and one line naming the tree it ran on (C3's SHA). (c) Rewrite `.agent/handoff.md` per
   `docs/agents/handback_template.md` and commit it TOGETHER with the transcript. Subject `F286 R2
   C4: record the closure suite transcript and rewrite handoff for round 2`. Then
   `git push origin feature/f286-findings-paydown-v5`. No pull request.

CONSTRAINTS
1. Never edit or retype a payload; report each `git apply --check` and `git apply` exit code.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set: the `.agent/authored/f286-r2-*` files, `.agent/live_review.md`,
   `.agent/plan.md`, `docs/agents/planner_reviewer_prompt.md`, `docs/roadmap/features/T2_F286.md`,
   `.agent/authored/f286-closure-suite.txt` and `.agent/handoff.md`. Report
   `git diff --name-only a45f74da2` at the tip. No edit to `README.md`, `docs/roadmap/STATUS.md`,
   `.agent/decisions.md`, `.agent/candidates.md`, `.agent/operator_questions.md`,
   `scripts/self_use_queue.json` or any file under `packages/`, `apps/` or `tests/`.
4. A RED full suite in C4 is this feature's work, not a stop: commit the transcript exactly as
   measured, report every bad node id, and hand back; the repair rounds are the reviewer's to order
   (amend0917-throughput rule 2). Never weaken an assertion, delete a test, skip or mark anything
   xfail. An EXISTING test that goes red before C4 is never edited to pass; report it and stop.
5. Any other red gate: STOP, commit and push what is verified, hand back under AGENTS.md "If
   Blocked". Nothing is merged; no `gh pr create`; no force-push; no amend; no evidence job; no
   zip; do not run the self-use runner or any job that calls a provider.
6. Leave every existing worktree, branch and stash alone, the reviewer's included. This round adds
   no worktree.
7. The full suite runs ONCE, in C4, and nowhere else this round (amend0917 rule 1).

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a word
is a finding. G1 and G2 run before C4 is written; G3 is C4's suite.
G1 TRANSPORT AND RECORDS: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f286-r2-*` payload copy byte-equal to its source by `git show <C1>:<path>`;
   and `git show <read at>:<path>` of each file below hashes to the reviewer's tree:
   | read at | path | bytes | sha256 |
   |---|---|---|---|
   | C2 | .agent/live_review.md | 322135 | 2843947b19d95a0f8817325a30dad2ea95bef69b6385089a1086e388c30d31ca |
   | C2 | .agent/plan.md | 909 | 1c861a4d6e4d85151a4283ed2da3d1e950364bbae058cfbd469c1d7da00f416f |
   | C3 | docs/agents/planner_reviewer_prompt.md | 110730 | f3d943516fb731db5e6e420f4c445c57b412537d43a6dff644bd55423829cc0c |
   | C3 | docs/roadmap/features/T2_F286.md | 3948 | b60ce60205bcd8711e92f7f46af1cf48160e03a798d29b71824ac04a5a2a0e0a |
   `open_finding_ids` and `latest_gate_verdict` of `scripts/rotate_live_review.py` over the ledger
   at C2 read `[]` and `PASS`; `live_checklist_items` of `packages/orchestration/block_lint.py` over
   the planner prompt's text reads 34 items at `a45f74da2` and at C3; and the S readings.
G2 THE TESTS, in the primary checkout at C3, serially:
   `bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/docs tests/orchestration/test_block_lint.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/orchestration/test_doc_staleness.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'`
   — the reviewer read `569 passed, 1 skipped` at exit 0 in its tree carrying C2 and C3 but no
   `.agent/authored/f286-r2-*` copy, the skip the D12 quarantine; your count may differ by what
   the round's copies add. Report the summary and every SKIPPED line. Then
   `python3 -m apps.cli.main integrity check --json`: six `pass` at `fail_count` 0; then
   `python3 -m apps.cli.main integrity block .remedy-wt/f286-r2/block.md`, real exit code and whole
   output; and `git status --porcelain` empty with no untracked file (closure precondition 3).
G3 THE INTEGRATION GATE: the UI build's last line and real exit code; `git status --porcelain`
   after it; then the full suite's real exit code, wall time, summary line and every bad node id,
   all in `.agent/authored/f286-closure-suite.txt`; and whether
   `tests/orchestration/test_import_reachability.py` or `tests/test_no_orphan_modules.py` holds a
   bad node (closure precondition 7).
G4 AFTER C4 AND THE PUSH, in your final reply only: `git status --porcelain` empty, the local tip
   equal to `origin/feature/f286-findings-paydown-v5`, `git log --oneline -n 6`,
   `git worktree list | wc -l`, `git branch --list 'remedy/*' | wc -l`, the push's real outcome,
   and `gh pr list --state open --json number` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the `git show --numstat` counts you measured beside the
ones above, every gate's real output, the full suite's summary line and bad node ids, the
authored-text proofs, the item-status table AGENTS.md requires (one row per commit and per gate),
the deviations, and the next action. Session section: SESSION 1 of feature F286, round 2, rounds so
far 2, plus one sentence on how much context you had left. `## Next`: Phase 1 rule 1, the review of
round 2 and of its suite transcript, then the closure's evidence round — the booking of round 2,
any repair the suite requires, the evidence bundle and the review package — and then the closing
round. State the open-findings count, 0, and "Operator questions open: 1".
