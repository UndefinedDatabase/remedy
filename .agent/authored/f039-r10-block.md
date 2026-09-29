STEP F039 R10 — THE CLOSURE SEQUENCE'S FIRST ROUND: book round 9's FAIL with R-1103, repair R-1103, write the Built State, the checklist consolidation and the guide's window sentence, and take the feature's one full suite

GOAL
Round 9 is reviewed FAIL at `2e4a9a65` on one finding, R-1103: the zero-network test stops reading
the browser's events at its last check. Book the verdict with R-1103's registration and the plan;
repair R-1103 in the test; append F039's Built State to its feature file, the checklist
consolidation to the planner prompt and one sentence to the story guide; then run this feature's ONE
full suite on the tree that ships and commit its transcript. The self-use reading, the evidence
bundle, the review package, the rotation, the STATUS line and the pull request belong to later rounds.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict, never merge, and never write a `Done:` line. THE CHANGE TO THE TEST IS SPECIFIED,
NOT SLICED; the records and the documents travel as payloads. Read first:
`docs/roadmap/STATUS_closure_protocol.md` preconditions 2, 3 and 7, `docs/agents/integration_gate.md`,
R-1103 in records.diff, `tests/ui_server/test_story_export_file_live.py` whole, and your round 9 tool
`.agent/authored/f039-r9-mutations.py`.

THE DIRECTORIES
  `.remedy-wt/f039-r10-payloads/` and `.remedy-wt/f039-r10/`  READ-ONLY. The reviewer's.
  every other `.remedy-wt/f039-*` path and `.remedy-wt/f039-review/`: the reviewer's; do not touch.
  `.remedy-wt/f039-r10-worker/`   YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR: `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`,
`cp`, `ln`, `sed`, process and command substitution, `cd <dir> && ...`, `for` loops, and one-liners
chained with `;` or `&&` outside a `bash -c`. Capture exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe. Use
`git -C <path>`; never `cd` into a worktree. Use `python3 - <<'PY'` for counting, hashing, copying
(`shutil.copyfile`) and linking (`os.symlink`); write any script holding a dollar-brace or a brace
next to a quote to a file under your own directory and run it; run a program in another directory
with `subprocess.run(..., cwd=...)`. Never run npm or npx. Never `git stash`, never `pkill -f`: stop
a process only by its own recorded pid. The `remedy` command is denied; use `python3 -m
apps.cli.main` where a gate names it.

COMMIT TRAILER — every commit ends with exactly this line:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. In `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain` empty,
   `git branch --show-current` `feature/f039-story-replay-mode`, `git log --oneline -1` `2e4a9a65a`.
3. Measure this block's line count and sha256 (`.remedy-wt/f039-r10/block.md`) against your
   delegation message's readings; report both beside both, and stop if either differs.
4. Report `git worktree list | wc -l` and `git branch --list 'remedy/*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f039-r10-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE use and report every reading. Never retype or edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 31 | 1098 | c1d955a895bbf44cd1eadcf9e62df64dea67075fd237e4bf14d95f34bf550adb |
| records.diff | 12 | 8405 | cdcd1da800eb7b49562aa5e7f4918d77320087e2affdce5b47470d78441f4496 |
| closure_docs.diff | 97 | 7722 | a8498b655dc364a960ddf8613f187fb8a529eb184ea934e72ccfa5db83a831dd |

`plan.md` REWRITES `.agent/plan.md`. Both diffs were generated with `git diff HEAD` from trees at
`2e4a9a65` and go on with `git apply`. `records.diff` appends to `.agent/live_review.md` round 9's
gate entry, VERDICT FAIL, and R-1103's registration. `closure_docs.diff` appends the Built State to
`docs/roadmap/features/T5_F039.md`, inserts the consolidation paragraph directly before the line
`  The next consolidation measures against 34.` of `docs/agents/planner_reviewer_prompt.md`, and
rewords one sentence of `docs/guides/story-user-guide-v1.md` to say the test records requests while
the story plays and for two seconds after.

THE SPECIFICATION. No `except Exception`, no new dependency.
S1 R-1103. In `tests/ui_server/test_story_export_file_live.py`: a module constant
   `IDLE_DRAIN_SECONDS = 2.0` directly after `STORY_EXPORT_MAX_BYTES`, under a comment naming R-1103
   and saying why; `ChromePipe` gains `drain(self, seconds: float) -> None`, before `close`, which
   keeps every message Chrome sends as an event until `seconds` pass with no command outstanding,
   returning when `_read_message` times out; and the test calls `pipe.drain(IDLE_DRAIN_SECONDS)`
   directly after its last check, inside the `try`, before the `finally` closes Chrome. Nothing else
   in the file changes. In C3, append to `.agent/live_review.md` one blank line and one line beginning
   `Landed: R-1103 — ` saying in one sentence what changed; it names no commit.

BUNDLE — commits in this order.
C1 COPIES: `.agent/authored/f039-r10-block.md` := this block and each payload as
   `.agent/authored/f039-r10-<name>`, by `shutil.copyfile`. Subject `F039 R10 C1: copy round 10
   block and payloads`. Its insertions are this block's line count plus 140; STOP rather than commit
   at 500 or more.
C2 RECORDS: `git apply --check` then `git apply` records.diff, then `.agent/plan.md` := plan.md.
   Subject `F039 R10 C2: book round 9's FAIL and register R-1103`. Expected by `git show --numstat`:
   4/0 .agent/live_review.md, 9/6 .agent/plan.md.
C3 THE REPAIR: S1 with its `Landed:` line. Subject `F039 R10 C3: read the browser's events for two
   seconds after the last check (R-1103)`.
C4 YOUR MUTATION TOOL `.agent/authored/f039-r10-mutations.py`, BEFORE G3 runs. Subject
   `F039 R10 C4: save the round's mutation tool`.
C5 THE DOCUMENTS: `git apply --check` then `git apply` closure_docs.diff. Subject `F039 R10 C5:
   write the Built State, the checklist consolidation and the guide's window sentence`. Expected by
   `git show --numstat`: 5/0 docs/agents/planner_reviewer_prompt.md, 2/2
   docs/guides/story-user-guide-v1.md, 58/0 docs/roadmap/features/T5_F039.md.
C6 THE INTEGRATION GATE, in the PRIMARY checkout, after C5 and after G1 to G3. (a) run
   `apps/ui/node_modules/.bin/vite build` with `cwd` `apps/ui` from a Python script, report its exit
   code and last line — a failing build is a STOP — then `git status --porcelain`, still empty.
   (b) `python3 -m pytest -n auto -q`, its log under `.remedy-wt/f039-r10-worker/`; measure its wall
   time. Write `.agent/authored/f039-closure-suite.txt` holding the command, the real exit code, the
   wall time, the summary line, the FULL list of bad node ids (failed plus errors) or the literal
   `NONE`, and one line naming the tree it ran on (C5's SHA). (c) Rewrite `.agent/handoff.md` per
   `docs/agents/handback_template.md` and commit it TOGETHER with the transcript. Subject `F039 R10
   C6: record the closure suite transcript and rewrite handoff for round 10`. Then
   `git push origin feature/f039-story-replay-mode`. No pull request.

CONSTRAINTS
1. Never edit or retype a payload; report each `git apply --check` and `git apply` exit code.
2. Every commit under 500 insertions by `git show --numstat`; split one that would reach it into
   parts with their own subjects, and say so.
3. The round's tracked path set: the `.agent/authored/f039-r10-*` files, `.agent/live_review.md`,
   `.agent/plan.md`, `tests/ui_server/test_story_export_file_live.py`,
   `docs/agents/planner_reviewer_prompt.md`, `docs/guides/story-user-guide-v1.md`,
   `docs/roadmap/features/T5_F039.md`, `.agent/authored/f039-closure-suite.txt` and
   `.agent/handoff.md`. Report `git diff --name-only 2e4a9a65a` at the tip. No edit to `README.md`,
   `docs/roadmap/STATUS.md`, `.agent/decisions.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md`, `scripts/self_use_queue.json` or any other file.
4. A RED full suite in C6 is this feature's work, not a stop: commit the transcript exactly as
   measured, report every bad node id, and hand back; the repair rounds are the reviewer's to order
   (amend0917-throughput rule 2). Never weaken an assertion, delete a test, skip or mark anything
   xfail. An EXISTING test that goes red before C6 is never edited to pass; report it and stop.
5. Any other red gate: STOP, commit and push what is verified, hand back under AGENTS.md "If
   Blocked". Nothing is merged; no `gh pr create`; no force-push; no amend; no evidence job; no
   zip; do not run the self-use generator or runner.
6. Leave every existing worktree, branch and stash alone, the `.remedy-wt/job-*` worktrees and the
   reviewer's included. The worktree G3 adds goes under `.remedy-wt/`, gains the `node_modules`
   link your round 9 tool makes, and is removed as that gate's last action with
   `git worktree remove --force`.
7. The full suite runs ONCE, in C6, and nowhere else this round (amend0917 rule 1).

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a word
is a finding. G1 to G3 run before C6 is written; G4 is C6's suite.
G1 TRANSPORT AND RECORDS: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f039-r10-*` payload copy byte-equal to its source by `git show <C1>:<path>`;
   and `git show <read at>:<path>` of each file below hashes to the reviewer's trees:
   | read at | path | bytes | sha256 |
   |---|---|---|---|
   | C2 | .agent/live_review.md | 363185 | 847d1c490ec3e653852c5440aaae5055fa26d98228a6f06c88f6a0e4220c3bbe |
   | C2 | .agent/plan.md | 1098 | c1d955a895bbf44cd1eadcf9e62df64dea67075fd237e4bf14d95f34bf550adb |
   | C5 | docs/agents/planner_reviewer_prompt.md | 110378 | b1723b14d33e5de6e8e9f97096ea3916d4bd3ef42b31c9f54ee4a5359702f2e9 |
   | C5 | docs/guides/story-user-guide-v1.md | 5373 | 076ea0b7887e6a7ad9b2677fd7d4f1d3dff768c38beca9bd16354382f3e383c4 |
   | C5 | docs/roadmap/features/T5_F039.md | 9795 | f0f2a3fef2f6372d42c9b6bfbd8d121b0b4d423d1254a3f1b3a51532d4708b1c |
   `open_finding_ids` and `latest_gate_verdict` of `scripts/rotate_live_review.py` over the ledger
   at C2 read `['R-1103']` and `FAIL`; at C3 the ledger at C2 is a byte-exact prefix of the ledger
   at C3 and what C3 adds is exactly "\n" plus one line beginning `Landed: R-1103 — ` and ending in
   "\n"; and `live_checklist_items` of `packages/orchestration/block_lint.py` over the planner prompt
   reads 34 items at `2e4a9a65a` and at C5.
G2 THE CODE AND THE TESTS, in the primary checkout at C5, serially: `python3 -m ruff check
   tests/ui_server/test_story_export_file_live.py .agent/authored/f039-r10-mutations.py`, real exit
   code; then
   `bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_server/test_story_export_file_live.py tests/ui_contracts/test_story_player_contract.py tests/docs tests/orchestration/test_block_lint.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -8; echo "REAL_EXIT=${PIPESTATUS[0]}"'`
   — the reviewer read `458 passed, 1 skipped` at exit 0 in its simulation tree carrying its own S1
   and the payloads, the skip the D12 quarantine; report the summary and every SKIPPED line, a skip
   naming `node_modules`, vite or Chrome being red. Then `python3 -m apps.cli.main integrity check
   --json`: six `pass` at `fail_count` 0, the verdict check reading `FAIL`; then
   `python3 -m apps.cli.main integrity block .remedy-wt/f039-r10/block.md`, real exit code and whole
   output; and `git status --porcelain` empty with no untracked file (closure precondition 3).
G3 THE RED PROOFS, at C4 in a disposable worktree `.remedy-wt/f039-r10-mut`: your tool, built as
   round 9's is, `pytest` under `python3 -B` over the worktree's
   `tests/ui_server/test_story_export_file_live.py`, controls first and last each reading the live
   test PASSED, `restored byte-identical: True` and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY:
   <bool>`: m1 `storyPlayerMain.tsx` calls `fetch("http://127.0.0.1:9/late")` 500 ms after load; m2
   it sends an `XMLHttpRequest` to `http://127.0.0.1:9/late-xhr` 1500 ms after load. Every mutation
   must be red. Then ONE REVERT PROBE, whose expected reading is GREEN: m1 together with
   `IDLE_DRAIN_SECONDS = 0.0`, which shows the drain is what catches m1; report its exit code and
   counts, and report it as the probe it is, never as a caught mutation. Remove the worktree
   afterwards, `git worktree prune`, and report `git worktree list | wc -l`.
G4 THE INTEGRATION GATE: the UI build's last line and real exit code; `git status --porcelain`
   after it; then the full suite's real exit code, wall time, summary line and every bad node id,
   all in `.agent/authored/f039-closure-suite.txt`; and whether
   `tests/orchestration/test_import_reachability.py` or `tests/test_no_orphan_modules.py` holds a
   bad node (closure precondition 7).
G5 AFTER C6 AND THE PUSH, in your final reply only: `git status --porcelain` empty, the local tip
   equal to `origin/feature/f039-story-replay-mode`, `git log --oneline -n 8`,
   `git worktree list | wc -l`, `git branch --list 'remedy/*' | wc -l`, the push's real outcome,
   and `gh pr list --state open --json number` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the `git show --numstat` counts you measured beside the
ones above, every gate's real output, the full suite's summary line and bad node ids, the
authored-text proofs, the item-status table AGENTS.md requires (one row per commit, per gate and
per finding), the deviations, and the next action. Session section: SESSION 2 of feature F039,
round 10, rounds so far 10, plus one sentence on how much context you had left. `## Next`: Phase 1
rule 1, the review of round 10 and of its suite transcript, then the closure's evidence round — the
booking of round 10 with R-1103's resolution, the self-use reading, any repair the suite requires,
the evidence bundle and the review package — and then the closing round. State the open-findings
count, 1 (R-1103, landed and awaiting review), and "Operator questions open: 1".
