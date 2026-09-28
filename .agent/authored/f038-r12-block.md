STEP F038 R12 — BOOK ROUND 11, RESOLVE R-1095, REGISTER AND REPAIR R-1096 AND R-1097, THEN T003'S END-TO-END PROOF: a question answered with its citations, "stop that task" as a card, the card confirmed through the write door, the job stopping with one audit line

GOAL
Round 11 is reviewed PASS at `b9128a0c`, with R-1095 resolved and two Low findings, R-1096 and
R-1097. Book them, repair both, and land the end-to-end proof T5_F038.md's T003 names, against a
real job run in its own process: the chat route answers a question about a finished task with its
citations, turns "stop that task" into a card, nothing is executed until the card is confirmed
through the write door, and the job then stops with exactly one accepted audit line.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict, never merge, and never write a `Done:` line. THE PRODUCTION CHANGE IS
SPECIFIED, NOT SLICED: you write the code and its tests yourself against S1 to S3 below. Only the
`.agent/` records travel as payloads. Read R-1096 and R-1097 in the records diff before you write
code. Before you write anything, read whole: `apps/ui/src/api/chatTurn.ts` and its test,
`apps/ui/src/components/graph/EvidenceChatTab.tsx` and `evidenceChatAudit.test.ts`,
`tests/ui_contracts/test_chat_citations.py`, `tests/ui_server/test_pause_door_live.py` (the live
e2e you model), the `job.stop` branch and `_dispatch_job_stop` of
`packages/orchestration/ui_server.py`, `_STOP_WORDS` and its use in
`packages/orchestration/chat_intent.py`, and `audit_command_attempt` in
`packages/orchestration/command_audit.py` (an audit line's nonce is its `nonce` key).

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f038-r12-payloads/` READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f038-r12/`          READ-ONLY. The reviewer's block.
  every other `.remedy-wt/f038-*` directory except your own, and `.remedy-wt/f038-review/`
                                  The reviewer's; do not touch them.
  `.remedy-wt/f038-r12-worker/`   YOURS for logs, scripts and the vitest scratch; create it if
                                  absent. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace or a brace next to a quote is refused: write such a script to a file under your own
directory and run the file. Never run npm or npx: vitest, `tsc` and eslint run through the pytest
wrappers G4 names, and G5's tool runs the primary's own `vitest` binary. Stop a process only by
its own recorded pid, never with `pkill -f`.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f038-grounded-chat`, and `git log --oneline -1` must read `b9128a0cb`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f038-r12/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f038-r12-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 16 | 8454 | d0cb849bdd5414e939505edd2fd7e37c116de3955a45d9e7260af695ffb310b1 |
| plan.md | 30 | 1058 | 792b6968af93d012ac071df60bdab926e5aa389a951618ebd78b2bb60d551bfc |
| landed.diff | 12 | 3271 | 1f32ade2d8721246b21be9ac4d651efd1374c0c926ed993c223bb11dba7d0227 |

`plan.md` is a REWRITE of `.agent/plan.md`. Both diffs go on with `git apply`; the reviewer
generated them with `git diff HEAD` from a tree at `b9128a0c` into which it wrote the edits.
`records.diff` appends round 11's gate entry, R-1095's `Done:` and the registrations of R-1096
and R-1097 to `.agent/live_review.md`. `landed.diff` appends their two `Landed:` lines on top of
C2's ledger and goes in with C4a.

THE SPECIFICATION. No `except Exception`, no `any`, no raw colour literal, no new dependency.
S1 R-1096's REPAIR. In `apps/ui/src/api/chatTurn.test.ts`: an answer body with an empty
   `sentences` list decodes to `null` while the same body with its sentence decodes; and a card
   body whose `args` hold a number decodes to `null` while the same body with a string decodes.
S2 R-1097's REPAIR. In `chatTurn.ts`: `chatUnavailableLine(reason)`, exactly "Type a question or
   a request first." for `empty_text`, "This task is not part of the job, so nothing was asked."
   for `unknown_task`, and "The chat could not answer that." for any other reason;
   `describeChatCardResult` keeps `Sent: <verb>.` for an accepted send and gains the card's OWN
   sentences, no longer calling `describeDecisionSubmitResult`, whose import and the comment
   naming it go: unreachable, warn, "No answer came back, so this may not have reached the job.
   You can confirm it again."; 400, error, "The job could not read this card, so nothing was
   done."; 403, error, "This dashboard was not allowed to send it, so nothing was done. Open the
   dashboard again from a fresh link."; 409, error, "The job refused it in its current state, so
   nothing was done."; 429, warn, "Too many commands arrived at once. Wait a moment, then confirm
   it again."; any other status, error, "The job refused it, so nothing was done.";
   `chatEvidenceTabLabel(tab)`, "Open the diff" or "Open the prompt trace". In
   `EvidenceChatTab.tsx`: an unavailable turn shows `chatUnavailableLine(reason)` and never the
   code; each open button reads `chatEvidenceTabLabel(tab)`; the text input carries
   `aria-label="Ask the chat"` and the placeholder "Ask about the whole project" when the box is
   ticked, else `Ask about task <task id>`; and `ChatTurnBlock` takes an optional `sending`
   (default false) under which Confirm is not rendered, the tab setting it on a turn before its
   send and clearing it with the outcome. Tests: vitest pins each sentence and label exactly and
   that no refusal sentence contains "decision" or "answer"; the DOM audit renders a card with
   `sending` true (no Confirm) and false (Confirm), an unavailable `unknown_task` turn (its line
   shown, the code absent from the markup) and an answer with a diff item (a button reading
   "Open the diff"); `tests/ui_contracts/test_chat_citations.py` pins the input's `aria-label`.
S3 THE END-TO-END PROOF. A NEW FILE `tests/ui_server/test_chat_e2e_live.py`, modelled on
   `tests/ui_server/test_pause_door_live.py`'s `TestJobScopeLiveDoor` and owning its own copies
   of that file's helpers, marked `@pytest.mark.subprocess`: a three-task job run by
   `run_job` in its own process with a `SlowProvider` whose SECOND build call — task 2's first —
   writes a `building` file under `tmp_path` and waits for a `go` file before it proceeds, so the
   stop can never race the job's end; a real UI server started in a thread. While task 2's call
   is held: `GET /api/jobs/<job>/chat` asking "Did the tests pass?" with `task` task 1 answers
   `available` true, kind `answer`, scope `node`, subject task 1, at least one evidence item, and
   every sentence either supported with citations all within 1 to n or exactly
   "Not in evidence." with none; asking "stop that task" with `task` task 2 answers a card, verb
   `job.stop`, confirmable; the job's audit file holds no line; the card's verb and args are
   POSTed through the write door with bearer and `X-Remedy-CSRF` and the nonce `chat-e2e-stop`,
   answering 200 with outcome `accepted`; then `go` is written. The runner prints
   `FINAL:stopped`, the job record's status is `stopped`, the run log holds exactly one
   `job_stopped` event, and the audit file holds exactly one line, `job.stop`, `accepted`, nonce
   `chat-e2e-stop`. The reviewer's own version passed three runs out of three, under 2 s each.

BUNDLE — the commits are C1a, C1b, C2, C3, C4a, C4b and C5, in this order.

C1a — `.agent/authored/f038-r12-block.md` := this block and `.agent/authored/f038-r12-plan.md` :=
  plan.md, by `shutil.copyfile`. Subject: `F038 R12 C1a: copy round 12 block and plan payload into .agent/authored/`
  Its insertions are this block's line count plus 30. STOP rather than commit at 500 or more.
C1b — `.agent/authored/f038-r12-records.diff` := records.diff and
  `.agent/authored/f038-r12-landed.diff` := landed.diff. Expected insertions: 28.
  Subject: `F038 R12 C1b: copy round 12 records and landed diffs into .agent/authored/`
C2 — `git apply` records.diff, then `.agent/plan.md` := plan.md. Expected by `git show --numstat`:
  8/0 live_review.md, 8/7 plan.md.
  Subject: `F038 R12 C2: book round 11, resolve R-1095, register R-1096 and R-1097`
C3 — S2's production change in `chatTurn.ts` and `EvidenceChatTab.tsx`.
  Subject: `F038 R12 C3: plain lines, a card's own refusals, a named input and one send at a time`
C4a — S1, S2's tests, S3, and `git apply` landed.diff.
  Subject: `F038 R12 C4a: prove the chat end to end and repair R-1096 and R-1097`
C4b — your mutation tool (G5) saved as `.agent/authored/f038-r12-mutations.py`.
  Subject: `F038 R12 C4b: save the round's mutation tool`
C5 — `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F038 R12 C5: rewrite handoff for round 12`
  Then `git push origin feature/f038-grounded-chat`. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split one that
   would reach it into parts with their own subjects, and say so.
3. The round's whole tracked path set is: the `.agent/authored/f038-r12-*` copies and tool,
   `.agent/live_review.md`, `.agent/plan.md`, `apps/ui/src/api/chatTurn.ts`,
   `apps/ui/src/api/chatTurn.test.ts`, `apps/ui/src/components/graph/EvidenceChatTab.tsx`,
   `apps/ui/src/components/graph/evidenceChatAudit.test.ts`,
   `tests/ui_contracts/test_chat_citations.py`, `tests/ui_server/test_chat_e2e_live.py`, and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only b9128a0cb` at the
   branch tip after C5. Touch nothing else.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong, or this round's own mutation tool, may be corrected before C5 in a
   new commit, and the correction is declared. An EXISTING test that goes red is never edited to
   pass; report it and stop.
5. NOTHING IS MERGED, SENT OR REWRITTEN. No `gh pr merge`, no `gh pr create`, no checkout of
   `main`, no branch deletion, no force-push, no `git stash`, no request to any server this
   round's tests did not start themselves or to any model, and no `git commit --amend` or any
   other rewrite of a commit, pushed or not: a wrong commit subject is declared, never amended.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F038's belongs to its closure. G4's selection takes about two minutes; run it once.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f038-r12-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f038-r12/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <commit>:<path>` at the commit
 named, equals the reviewer's reading, printed from its simulation tree. Report each beside the
 hash you read:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 351471 | 2cefd816fc043626f40d2ab4f412d48f9d719186c568221e57dd0d887053b3ec |
 | C2 | .agent/plan.md | 1058 | 792b6968af93d012ac071df60bdab926e5aa389a951618ebd78b2bb60d551bfc |
 | C4a | .agent/live_review.md | 351904 | 8cfa26e962040319de0cb6f65509b1fda1468690b1ca125840bab8835958f3c9 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show` at C2 and at C4a (the
 reviewer read `['R-1096', 'R-1097']` at both); and `git diff --name-only <C1b> <C2>`, which must
 name exactly the two C2 paths of the table.

G3 THE CODE — `python3 -m ruff check tests/ui_contracts/test_chat_citations.py
 tests/ui_server/test_chat_e2e_live.py .agent/authored/f038-r12-mutations.py` at C4b, with its
 real exit code. Then report, quoted from `git show <C3>`, the whole of `chatUnavailableLine`,
 `describeChatCardResult`, `chatEvidenceTabLabel`, and the tab's lines that set and clear
 `sending` and render Confirm.

G4 THE TESTS — in the primary checkout at C4b, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/orchestration/test_test_runner.py tests/orchestration/test_chat_turn.py tests/ui_server/test_chat_route.py tests/ui_server/test_chat_e2e_live.py tests/ui_server/test_dashboard_contract.py tests/docs tests/test_agent_tooling.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/orchestration/test_development_artifact_boundary.py tests/regression/test_resource_safety.py tests/cli/test_golden_path.py 2>&1 | tail -9; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 It runs the whole vitest suite, `tsc` and eslint over `apps/ui`. The reviewer ran it at
 `b9128a0cb`, without the new e2e file, serially in the primary checkout and read
 `1561 passed, 5 skipped` at exit code 0, the skips being four F252 quarantines in
 `tests/ui_contracts/` and one in `tests/test_agent_tooling.py`; over its simulation tree, whose
 own versions added 2 pytest nodes, it read 1559 passed and 9 skipped, the four further skips being
 toolchain tests a worktree without `apps/ui/node_modules` cannot run. Report every `SKIPPED` line
 and the node counts of `tests/ui_contracts/test_chat_citations.py` (4 at `b9128a0cb`) and
 `tests/ui_server/test_chat_e2e_live.py` at C4b, and account for any difference from 1561 passed.
 Then `python3 -m apps.cli.main integrity check --json`, all six checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f038-r12-mutations.py`, built as round 11's
 `.agent/authored/f038-r11-mutations.py` is, with the same VITEST runner over the worktree's
 `apps/ui/src/api/chatTurn.test.ts` and `apps/ui/src/components/graph/evidenceChatAudit.test.ts`,
 and a PYTEST runner over `tests/ui_contracts/test_chat_citations.py` and
 `tests/ui_server/test_chat_e2e_live.py`, controls of both first and last, then
 `restored byte-identical: True` and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.
 VITEST, in `chatTurn.ts`: r1 an answer with no sentence decoded; r2 a card arg that is not a
 string decoded; r3 `unknown_task`'s line replaced by the code; r4 the 409 sentence replaced by
 "This decision is no longer open. It may already have been answered."; r5 both open labels
 "Open". VITEST, in `EvidenceChatTab.tsx`: r6 Confirm rendered while `sending`; r7 an unavailable
 turn showing its code; r8 the open button reading "Open". PYTEST: r9 (`EvidenceChatTab.tsx`) the
 input's `aria-label` removed; r10 (`packages/orchestration/ui_server.py`) the chat route drops
 the task; r11 (`packages/orchestration/chat_intent.py`) "stop" removed from `_STOP_WORDS`; r12
 (`chat_intent.py`) the stop intent built as `job.pause` with no arguments.
 Run it: `git worktree add --detach .remedy-wt/f038-r12-mut <C4b>`, then
 `python3 -B .agent/authored/f038-r12-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f038-r12-mut`
 and report its whole output. EVERY mutation must be red with at least one failing name; a green
 one is reported as green, never papered over, and you then add the test that catches it in a
 commit before C5 and re-run. Then `git worktree remove --force .remedy-wt/f038-r12-mut`,
 `git worktree prune`, and report `git worktree list | wc -l`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 8`, which must show C5, C4b, C4a, C3, C2, C1b, C1a and `b9128a0cb` in that
 order (more lines if a commit was split or a declared correction added); `git worktree list |
 wc -l`, which must equal your step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 to C4b — report what you
measure), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Report what you ran, not what you expected to find. Your Session section reads SESSION 3
of feature F038, round 12, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 12, then F038's closure sequence: the user guide's chat paragraph, the feature's Built State
and spec-conformance review, the one full suite, the evidence package, the STATUS flip and the
pull request. State the open-findings count, 2 (R-1096 and R-1097, landed and awaiting the
review), and the operator-questions count, 1.
