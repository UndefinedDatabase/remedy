STEP F038 R13 — THE CLOSURE SEQUENCE'S FIRST ROUND: book round 12, resolve R-1096, finish R-1097, say how each answer was written, write the user guide's chat section and the Built State, consolidate the checklist, and take the feature's one full suite

GOAL
Round 12 is reviewed PASS at `1bcb713a`. Book it with R-1096's resolution and a recurrence line
that keeps R-1097 open; finish R-1097 with one contract test; land DECISION F038 D13, one plain line
under every answer saying how it was written, on the command line and in the cockpit; append the
user guide's chat section, the Built State of `docs/roadmap/features/T5_F038.md` and the checklist
consolidation (it joins nothing and keeps the §3 list at 34 items); then run this feature's ONE full
suite on the tree that ships and commit its transcript. The self-use item, the evidence bundle, the
review package, the rotation, the STATUS line and the pull request belong to later rounds.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict, never merge, and never write a `Done:` line. THE PRODUCTION CHANGE IS SPECIFIED,
NOT SLICED: you write the code and its tests against S1 and S2; the records and the documents travel
as payloads. Read first: `docs/roadmap/STATUS_closure_protocol.md` preconditions 2, 3 and 7,
`docs/agents/integration_gate.md`, DECISION F038 D13 and R-1097's recurrence line in records.diff,
`render_chat_answer` and `CHAT_GENERATOR_MECHANICAL` in `packages/orchestration/chat_answer.py`,
`_render_chat_answer_turn` in `apps/cli/commands/chat_cmd.py`, `apps/ui/src/api/chatTurn.ts`,
`apps/ui/src/components/graph/EvidenceChatTab.tsx` and its sheet, `tests/ui_contracts/test_chat_citations.py`,
and `.agent/authored/f038-r12-mutations.py`.

THE DIRECTORIES
  `.remedy-wt/f038-r13-payloads/` and `.remedy-wt/f038-r13/`  READ-ONLY. The reviewer's.
  every other `.remedy-wt/f038-*` path and `.remedy-wt/f038-review/`: the reviewer's; do not touch.
  `.remedy-wt/f038-r13-worker/`   YOURS for logs, scripts and the vitest scratch; create it if
                                  absent. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR: `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`,
`cp`, `sed`, process and command substitution, `cd <dir> && git ...`, `for` loops, and one-liners
chained with `;` or `&&` outside a `bash -c`. Capture exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe. Use
`git -C <path>`; never `cd` into a worktree. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`); write any script holding a dollar-brace or a brace next to a quote to a
file under your own directory and run it. The ONE npm command this round may run is C6's
`npm --prefix apps/ui run build`; never `npm install`, `npm ci` or `npx`. Never `git stash`, never
`pkill -f`: stop a process only by its own recorded pid. The `remedy` command is denied; use
`python3 -m apps.cli.main` where a gate names it.

COMMIT TRAILER — every commit ends with exactly this line:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. In `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain` empty,
   `git branch --show-current` `feature/f038-grounded-chat`, `git log --oneline -1` `1bcb713a3`.
3. Measure this block's line count and sha256 (`.remedy-wt/f038-r13/block.md`) against your
   delegation message's readings; report both beside both, and stop if either differs.
4. Report `git worktree list | wc -l` and `git branch --list 'remedy/*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f038-r13-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE use and report every reading. Never retype or edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 55 | 8610 | e295ec9372ac2407df31a818d7bb244734aacda1dc9dd6096bd96ad7c8194536 |
| plan.md | 30 | 1064 | 7cc9b0c21f0786aa56447acdc70d271cd1787630b0e1fe15386508cad4d7da99 |
| landed.diff | 10 | 2200 | d599c55dee5c5ef5f5b1e2741579db877caa02d7dfcd1c5b29df59f801cda932 |
| closure_docs.diff | 195 | 15200 | dc2d2a4a324cfc6dd0e3df008e6fc0ca0f7ae14fe038b7792fc6643d139c861e |

`plan.md` REWRITES `.agent/plan.md`. Every diff was generated with `git diff HEAD` from a tree at
`1bcb713a` into which the reviewer wrote the edits, and goes on with `git apply`. `records.diff`
appends to `.agent/live_review.md` round 12's gate entry, R-1096's `Done:` and a `Recurrence: R-1097`
line, and DECISION F038 D13 to `.agent/decisions.md`. `landed.diff` appends a second
`Landed: R-1097 — ` line on top of C2's ledger. `closure_docs.diff` appends the Built State to
`docs/roadmap/features/T5_F038.md`, inserts the consolidation paragraph directly before the line
`  The next consolidation measures against 34.` of `docs/agents/planner_reviewer_prompt.md`, and
inserts the section "Ask a question, or ask for an action" before `## Exit codes` of
`docs/guides/steering-user-guide-v1.md` with one sentence for `remedy chat ask` in its exit codes.

THE SPECIFICATION. No `except Exception`, no `any`, no raw colour literal, no new dependency.
S1 DECISION F038 D13. In `packages/orchestration/chat_answer.py`, four module constants holding
   exactly "Built from the job's records, without a model.", "The model's answer could not be used,
   so this one is built from the job's records, without a model.", "Written by the summary model;
   every sentence was checked against the job's records." and "How this answer was written is not
   recorded.", and `chat_generator_line(generator)` answering them for `mechanical`, any label
   starting `mechanical:`, `summary-role`, and anything else, in that order.
   `_render_chat_answer_turn`'s text form prints that line directly after its `Scope:` line; its
   `--json` form is unchanged. `chatTurn.ts` gains `chatGeneratorLine(generator)` with the same four
   sentences and the same rule, and `ChatTurnBlock` shows it directly under the scope chip in an
   element with `data-ui="chat-generator"`, styled from the sheet's existing tokens. Tests:
   `tests/orchestration/test_chat_answer.py`, each of the four labels exactly;
   `tests/cli/test_chat_ask.py`, a focused question's text output whose line after `Scope:` is the
   mechanical sentence; `chatTurn.test.ts`, the four labels exactly; the DOM audit, an answer
   labelled `mechanical` rendering its sentence; and `tests/ui_contracts/test_chat_citations.py`,
   each of the four Python constants occurring quoted in `chatTurn.ts`.
S2 R-1097, THE REST. `tests/ui_contracts/test_chat_citations.py` gains one test that reads
   `EvidenceChatTab.tsx` and requires, in this order of position in the file, the update setting
   `sending: true`, `await sendChatCard(` and the update clearing `sending` with the outcome, and
   `sending={turn.sending}` anywhere in it. No other existing test is edited.

BUNDLE — commits in this order.
C1 COPIES: `.agent/authored/f038-r13-block.md` := this block and each payload as
   `.agent/authored/f038-r13-<name>`, by `shutil.copyfile`. Subject `F038 R13 C1: copy round 13
   block and payloads`. Its insertions are this block's line count plus 290; split it as
   `C1 (1/2)` and `C1 (2/2)` if that reaches 500.
C2 RECORDS: `git apply --check` then `git apply` records.diff, then `.agent/plan.md` := plan.md.
   Subject `F038 R13 C2: book round 12, resolve R-1096, keep R-1097 open, record DECISION F038 D13`.
   Expected by `git show --numstat`: 33/0 .agent/decisions.md, 6/0 .agent/live_review.md, 8/8
   .agent/plan.md.
C3 THE CODE: S1's production change. Subject `F038 R13 C3: say how each chat answer was written`.
C4a THE TESTS: S1's tests, S2, and `git apply` landed.diff. Subject `F038 R13 C4a: test the
   generator line and finish R-1097`.
C4b YOUR MUTATION TOOL `.agent/authored/f038-r13-mutations.py`, BEFORE G3 runs. Subject
   `F038 R13 C4b: save the round's mutation tool`.
C5 THE DOCUMENTS: `git apply --check` then `git apply` closure_docs.diff. Subject `F038 R13 C5:
   write the chat guide, the Built State and the checklist consolidation`. Expected by
   `git show --numstat`: 5/0 docs/agents/planner_reviewer_prompt.md, 35/1
   docs/guides/steering-user-guide-v1.md, 122/0 docs/roadmap/features/T5_F038.md.
C6 THE INTEGRATION GATE, in the PRIMARY checkout, after C5 and after G1 to G3. (a)
   `bash -c 'npm --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'` — a
   failing build is a STOP — then `git status --porcelain`, still empty. (b)
   `python3 -m pytest -n auto -q`, its log under `.remedy-wt/f038-r13-worker/`; measure its wall
   time. Write `.agent/authored/f038-closure-suite.txt` holding the command, the real exit code,
   the wall time, the summary line, the FULL list of bad node ids (failed plus errors) or the
   literal `NONE`, and one line naming the tree it ran on (C5's SHA). (c) Rewrite
   `.agent/handoff.md` per `docs/agents/handback_template.md` and commit it TOGETHER with the
   transcript. Subject `F038 R13 C6: record the closure suite transcript and rewrite handoff for
   round 13`. Then `git push origin feature/f038-grounded-chat`. No pull request.

CONSTRAINTS
1. Never edit or retype a payload; report each `git apply --check` and `git apply` exit code.
2. Every commit under 500 insertions by `git show --numstat`; split one that would reach it into
   parts with their own subjects, and say so.
3. The round's tracked path set: the `.agent/authored/f038-r13-*` files, `.agent/live_review.md`,
   `.agent/decisions.md`, `.agent/plan.md`, `packages/orchestration/chat_answer.py`,
   `apps/cli/commands/chat_cmd.py`, `apps/ui/src/api/chatTurn.ts`,
   `apps/ui/src/api/chatTurn.test.ts`, `apps/ui/src/components/graph/EvidenceChatTab.tsx`,
   `apps/ui/src/components/graph/EvidenceChatTab.module.css`,
   `apps/ui/src/components/graph/evidenceChatAudit.test.ts`,
   `tests/orchestration/test_chat_answer.py`, `tests/cli/test_chat_ask.py`,
   `tests/ui_contracts/test_chat_citations.py`, `docs/roadmap/features/T5_F038.md`,
   `docs/agents/planner_reviewer_prompt.md`, `docs/guides/steering-user-guide-v1.md`,
   `.agent/authored/f038-closure-suite.txt` and `.agent/handoff.md`. Report
   `git diff --name-only 1bcb713a3` at the tip. No edit to `README.md`, `docs/roadmap/STATUS.md`,
   `.agent/candidates.md`, `.agent/operator_questions.md`, `scripts/self_use_queue.json` or any
   other file.
4. A RED full suite in C6 is this feature's work, not a stop: commit the transcript exactly as
   measured, report every bad node id, and hand back; the repair rounds are the reviewer's to order
   (amend0917-throughput rule 2). Never weaken an assertion, delete a test, skip or mark anything
   xfail. An EXISTING test that goes red before C6 is never edited to pass; report it and stop.
5. Any other red gate: STOP, commit and push what is verified, hand back under AGENTS.md "If
   Blocked". Nothing is merged; no `gh pr create`; no force-push; no amend; no evidence job; no
   zip; do not run the self-use generator or runner.
6. Leave every existing worktree, branch and stash alone, the `.remedy-wt/job-*` worktrees and the
   reviewer's included. The worktree G3 adds goes under `.remedy-wt/` and is removed as that gate's
   last action.
7. The full suite runs ONCE, in C6, and nowhere else this round (amend0917 rule 1).

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a word
is a finding. G1 to G3 run before C6 is written; G4 is C6's suite.
G1 TRANSPORT AND RECORDS: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f038-r13-*` payload copy byte-equal to its source by `git show <C1>:<path>`;
   and `git show <read at>:<path>` of each file below hashes to the reviewer's simulation:
   | read at | path | bytes | sha256 |
   |---|---|---|---|
   | C2 | .agent/decisions.md | 2415624 | 89e667ac363553c5980c0f1ff69fef2faaeee77335458391e9fa537acb28217f |
   | C2 | .agent/live_review.md | 356772 | bcb94ed0e72e3bace3116fe83c05de8668784ec3c077e53e038e1e24dc218590 |
   | C2 | .agent/plan.md | 1064 | 7cc9b0c21f0786aa56447acdc70d271cd1787630b0e1fe15386508cad4d7da99 |
   | C4a | .agent/live_review.md | 357076 | 41c4496014576dec759ac87a3782b362e27a13a4a8195e1ffc393dfe74bc2b43 |
   | C5 | docs/roadmap/features/T5_F038.md | 15549 | 28ad03a18608428f9fc9e0cc1074a8284a5c8ae8610fcd736ef4952017cb2b03 |
   | C5 | docs/agents/planner_reviewer_prompt.md | 109903 | 6a32ca01d129bdaf96a41e68effca22e5869733415cfe4718ac0be8a4c6e1201 |
   | C5 | docs/guides/steering-user-guide-v1.md | 7075 | 8d1069bf1005641b7bdc50ce1aaf7723fecad2337c21daa3dc3063744742673b |
   `open_finding_ids` and `latest_gate_verdict` of `scripts/rotate_live_review.py` over the ledger
   at C2 and at C4a read `['R-1097']` and `PASS`; and `live_checklist_items` of
   `packages/orchestration/block_lint.py` over the planner prompt reads 34 items at `1bcb713a3`
   and at C5.
G2 THE CODE AND THE TESTS, in the primary checkout at C5, serially: `python3 -m ruff check
   packages/orchestration/chat_answer.py apps/cli/commands/chat_cmd.py
   tests/orchestration/test_chat_answer.py tests/cli/test_chat_ask.py
   tests/ui_contracts/test_chat_citations.py .agent/authored/f038-r13-mutations.py`, real exit
   code; then
   `bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/orchestration/test_test_runner.py tests/orchestration/test_chat_answer.py tests/orchestration/test_chat_turn.py tests/cli/test_chat_ask.py tests/cli/test_chat_cmd.py tests/ui_server/test_chat_route.py tests/ui_server/test_dashboard_contract.py tests/docs tests/test_agent_tooling.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/orchestration/test_block_lint.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py 2>&1 | tail -8; echo "REAL_EXIT=${PIPESTATUS[0]}"'`
   — the reviewer read `1664 passed, 5 skipped` at exit 0 at `1bcb713a3`, the skips the five F252
   quarantines, and its own versions of S1 and S2 add 4 pytest nodes; report the summary, every
   SKIPPED line and the node counts of the three touched Python test files at `1bcb713a3` and at
   C5, and account for the difference. Then `python3 -m apps.cli.main integrity check --json`, six
   `pass` at `fail_count` 0 — the status of each check is the reading; then
   `python3 -m apps.cli.main integrity block .remedy-wt/f038-r13/block.md`, real exit code and whole
   output; and `git status --porcelain` empty with no untracked file (closure precondition 3).
G3 THE RED PROOFS, at C4b in a disposable worktree `.remedy-wt/f038-r13-mut`: your tool, built as
   round 12's is, with the VITEST runner over the worktree's `chatTurn.test.ts` and
   `evidenceChatAudit.test.ts` and a PYTEST runner over `tests/ui_contracts/test_chat_citations.py`,
   `tests/orchestration/test_chat_answer.py` and `tests/cli/test_chat_ask.py`, controls of both
   first and last, `restored byte-identical: True` and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY:
   <bool>`: m1 (`chat_answer.py`) a `mechanical:` label answered the unknown sentence; m2
   (`chat_cmd.py`) the line not printed; m3 (`chatTurn.ts`) the summary sentence changed; m4 (the
   tab) the line not rendered; m5 (the tab) the update setting `sending: true` deleted; m6
   (`chat_answer.py`) the mechanical constant's sentence changed. Every mutation must be red; one
   that stays green is reported, and you add the test that catches it and re-run before C5. Remove
   the worktree afterwards, `git worktree prune`, and report `git worktree list | wc -l`.
G4 THE INTEGRATION GATE: the UI build's last line and real exit code; `git status --porcelain`
   after it; then the full suite's real exit code, wall time, summary line and every bad node id,
   all in `.agent/authored/f038-closure-suite.txt`; and whether
   `tests/orchestration/test_import_reachability.py` or `tests/test_no_orphan_modules.py` holds a
   bad node (closure precondition 7).
G5 AFTER C6 AND THE PUSH, in your final reply only: `git status --porcelain` empty, the local tip
   equal to `origin/feature/f038-grounded-chat`, `git log --oneline -n 9`,
   `git worktree list | wc -l`, `git branch --list 'remedy/*' | wc -l`, the push's real outcome,
   and `gh pr list --state open --json number` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the `git show --numstat` counts you measured beside the
ones above, every gate's real output, the full suite's summary line and bad node ids, the
authored-text proofs, the item-status table AGENTS.md requires (one row per commit, per gate and
per finding), the deviations, and the next action. Session section: SESSION 3 of feature F038,
round 13, rounds so far 13, plus one sentence on how much context you had left. `## Next`: Phase 1
rule 1, the review of round 13 and of its suite transcript, then the closure's evidence round —
the booking of round 13 with R-1097's resolution, the self-use item, any repair the suite requires,
the evidence bundle and the review package — and then the closing round. State the open-findings
count, 1 (R-1097, landed and awaiting review), and "Operator questions open: 1".
