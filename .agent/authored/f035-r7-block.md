STEP F035 R7 — REPAIR R-1083 AND R-1084, THEN THE END-TO-END PROOF: one real job acted on through the browser's door and the command line, its ledger file, command, route and report agreeing entry for entry

GOAL
Round 6 passed. Its first commit books that verdict and registers R-1083 and R-1084, with DECISION
F035 D7 and one prose-slip line. Then repair R-1084 in `ownership_phrases.py` and R-1083 in the
two ownership lists and the render harness, and land the end-to-end proof DECISION F035 D7 orders
in a NEW `tests/ui_server/test_ownership_e2e_live.py`. The closure sequence follows.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict, never merge, and never write a `Done:` paragraph. THE PRODUCTION CHANGE IS
SPECIFIED, NOT SLICED. Read R-1083, R-1084 and DECISION F035 D7 in the booking diff first. Before
you write anything, read whole: `packages/orchestration/ownership_phrases.py`, its test and its
golden; `apps/ui/src/components/graph/EvidencePanel.tsx` and `EvidencePanel.module.css`;
`apps/ui/src/components/detail/DetailPopover.tsx` and `DetailPopover.module.css`;
`tests/ui_contracts/test_ownership_view_contract.py`; the five `.agent/authored/f035-r6-render_*`
files and `.agent/authored/f035-r6-render.txt`; `tests/ui_server/test_pause_e2e_live.py` and
`tests/ui_server/test_steering_note_e2e_live.py`, the models for the live test, and how
`tests/ui_server/test_task_veto_e2e_live.py` and `tests/ui_server/test_command_dispatch.py` send
`job.veto-task` and `chat.send` through the door; and `ownershipEntriesForTask` in
`apps/ui/src/api/ownership.ts`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f035-r7-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f035-r7/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f035-r7-sim/`       The reviewer's simulation tree; do not touch it.
  `.remedy-wt/f035-review/`       The reviewer's scripts; do not touch them.
  `.remedy-wt/f035-r7-worker/`    YOURS for logs, scripts, screenshots and scratch configs; create
                                  it if absent. `.remedy-wt/f035-render-run/` is the harness's
                                  work dir, removed at its end. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Never run npm or npx. Stop every process you start by its own pid, never with `pkill -f`.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f035-ownership-ledger`, and `git log --oneline -1` must read `4d56671b`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f035-r7/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` and `git branch --list 'remedy/*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f035-r7-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| booking.diff | 63 | 15216 | 4d83746fda228af1f2928e28c3204e694b3f33fde68e170f14ad63d7265b6a7b |
| plan.md | 29 | 1035 | 76656d4727d49f7b77dd82a9cbf518085f370def55c306b2d92b7be9daf6af74 |

`plan.md` is a REWRITE of `.agent/plan.md`. `booking.diff` goes on with `git apply`; the
reviewer generated it with `git diff HEAD` from a tree at `4d56671b`. It appends round 6's gate
entry with the registrations of R-1083 and R-1084 to `.agent/live_review.md`, DECISION F035 D7 to
`.agent/decisions.md`, and one line to `.agent/prose_slips.md`.

THE SPECIFICATION. No `except Exception` in Python; no `any` type and no raw colour in TypeScript
or CSS; every sentence shown verbatim.
S1 R-1084'S REPAIR: in `ownership_sentence`, the `task_vetoed` unreachable clause is appended only
   when the consequence names at least one id; the golden gains one line for a veto whose
   consequence is `unreachable` with no id, reading `<actor> vetoed <task> — reason: “<text>”.`
   and nothing after it; an inline assertion pins the same. In the same commit append to
   `.agent/live_review.md` the line `Landed: R-1084 — <what changed>, in this commit.`
S2 R-1083'S REPAIR: the `<ul>` of `OwnershipTab` and of the task detail's section each get the
   class `ownershipList` of their own CSS module, which sets `list-style: none`, `margin: 0` and
   `padding: 0`, and gives each `li` of it `font-size: 13px`, `line-height: 1.45` and a gap between
   rows from a `--remedy-*` token the file already uses; nothing else in either list changes. The
   contract test gains one test that both CSS modules define `.ownershipList` with
   `list-style: none` and both components' lists carry `styles.ownershipList`. The harness moves to
   five NEW files `.agent/authored/f035-r7-render_*`, copies of round 6's with these changes only:
   the task detail's screenshot `render-detail.png` is taken with the evidence panel NOT mounted,
   so the task with entries is seen, and `render-tab.png` after it is mounted; and a check C-g
   reads, in (i) and in (iv), the list's computed `list-style-type` as `none` and every row's
   computed `font-size` as `13px`. Its output is saved as `.agent/authored/f035-r7-render.txt`. In
   the same commit append `Landed: R-1083 — <what changed>, in this commit.`
S3 THE END-TO-END PROOF, `tests/ui_server/test_ownership_e2e_live.py`, `@pytest.mark.subprocess`,
   shaped as `test_steering_note_e2e_live.py`: its own runner, server starter and door helper; a
   three-task job run in a subprocess with a fake provider held at its first build; then, in this
   order, through the door with one real token `job.veto-task` of the THIRD task with a reason,
   and `chat.send` with a message; on the real command line `python3 -m apps.cli.main job steer
   <job_id> "<note>" --task <second task>`, then `job pause <job_id> --task <second task>
   --reason "<reason>"`, then `job unpause <job_id> --task <second task>`; then the run is
   released and ends with exit 0. It asserts: (a) the evidence export's `ownership.json` equals
   `build_ownership_ledger` of the finished job; (b) `python3 -m apps.cli.main job ownership
   <job_id> --json` and the route `/api/jobs/<job_id>/ownership` answer the same entries, each
   the file's entry plus its `sentence`; (c) the actions, in the ledger's order, are exactly the
   five this run made, and each sentence equals a literal the test writes out — the veto and the
   message `You (browser, token #1) …`, the note and the pause `You (command line) …`, the resume
   `You resumed …` — whose consumption clauses name the task and round the run's own markers
   record; (d) `format_job_report_text` of the finished job holds `Ownership:` and the five
   sentences in that order; (e) the entries per task, by `ownershipEntriesForTask`'s rule written
   in Python in the test, are the veto for the third task, the note, the pause and the resume for
   the second, and for the first only the job-wide message if its round took it in. Every child
   process is stopped by its own pid.
S4 UNCHANGED: `ownership.py`, `pingpong_job.py`, `job_digest.py`, `ui_server.py`, the command,
   `ownership.ts`, `remedyApi.ts`, `RemedyShell.tsx`, and every existing assertion.

BUNDLE — the commits are C1 to C7, in this order.

C1 — copy this block and the payloads: `.agent/authored/f035-r7-block.md`,
  `.agent/authored/f035-r7-plan.md` and `.agent/authored/f035-r7-booking.diff`, by
  `shutil.copyfile`. Subject: `F035 R7 C1: copy round 7 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 92. Report the number you measure.
C2 — THE BOOKING, the round's first substantive commit: `git apply` booking.diff, then rewrite
  `.agent/plan.md` := plan.md. Subject: `F035 R7 C2: book round 6, register R-1083 and R-1084,
  record D7, one prose slip, advance the plan`. Expected by `git show --numstat`: 32/0
  decisions.md, 6/0 live_review.md, 9/9 plan.md, 1/0 prose_slips.md.
C3 — S1. Subject: `F035 R7 C3: repair R-1084, a veto with no unreachable task says nothing more`
C4 — S2's CSS, components and contract test. Subject: `F035 R7 C4: repair R-1083, the ownership lists take the panel's type scale`
C5 — S2's harness files and transcript, after G4 has passed, and the `Landed: R-1083` line.
  Subject: `F035 R7 C5: render the ownership lists again, the detail seen with the panel closed`
C6 — S3 and your mutation tool `.agent/authored/f035-r7-mutations.py`. Subject:
  `F035 R7 C6: prove ownership end to end through both doors, add the mutation tool`
C7 — THE HANDBACK, `.agent/handoff.md` rewritten per `docs/agents/handback_template.md`, its own
  commit. Subject: `F035 R7 C7: rewrite handoff for round 7`. Then `git push`. Do NOT create a
  pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split one that
   would reach it into parts with their own subjects, and say so.
3. The round's whole tracked path set is: the `.agent/authored/f035-r7-*` copies, harness,
   transcript and tool, `.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md`,
   `.agent/plan.md`, `packages/orchestration/ownership_phrases.py`,
   `tests/orchestration/fixtures/ownership/golden/sentences.txt`,
   `tests/orchestration/test_ownership_phrases.py`,
   `apps/ui/src/components/graph/EvidencePanel.tsx`,
   `apps/ui/src/components/graph/EvidencePanel.module.css`,
   `apps/ui/src/components/detail/DetailPopover.tsx`,
   `apps/ui/src/components/detail/DetailPopover.module.css`,
   `tests/ui_contracts/test_ownership_view_contract.py`,
   `tests/ui_server/test_ownership_e2e_live.py`, and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only 4d56671b` after C7. Touch nothing else.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. A test this round itself wrote that is wrong may be
   corrected before C7, and the correction is declared. An EXISTING assertion that goes red is
   never edited to pass; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave every existing worktree, branch, stash and process alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` and the
   `remedy/*` branch count are reported afterwards; neither may change.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F035's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C7 is written.

G1 TRANSPORT AND BOOKING — each payload's line count, byte count and sha256 against the PAYLOADS
 table, then each `.agent/authored/f035-r7-*` payload copy compared byte for byte with its
 source, read back with `git show <C1>:<path>`. Then the sha256 of each file below, read with
 `git show <C2>:<path>`, equals the reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2343519 | 9dcf502ef8f3b64e0e0e471b2da129a8a161b5d5a8f480289e29db79f745bf1a |
 | .agent/live_review.md | 324312 | d3eced8378b91f76620dd175f762d3325ce949f85ec9914df90a91325f585ee0 |
 | .agent/plan.md | 1035 | 76656d4727d49f7b77dd82a9cbf518085f370def55c306b2d92b7be9daf6af74 |
 | .agent/prose_slips.md | 375646 | c5af2e8d96eb539f83c0f767d3c500314c9ffc2fc3ee5c426ed0c09ec3ed870f |
 Also `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's text at C2, which
 the reviewer read as `['R-1083', 'R-1084']`.

G2 THE CODE — `python3 -m ruff check packages/orchestration/ownership_phrases.py
 tests/orchestration/test_ownership_phrases.py tests/ui_contracts/test_ownership_view_contract.py
 tests/ui_server/test_ownership_e2e_live.py` with its real exit code; `git show <C3> --
 tests/orchestration/fixtures/ownership/golden/sentences.txt` whole; and the two `.ownershipList`
 rules quoted from `git show <C4>`.

G3 THE TESTS — first `tests/ui_server/test_ownership_e2e_live.py` alone, three times, each with
 its wall time and real exit code. Then, in the primary checkout at C6, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_server/test_ownership_e2e_live.py tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/ui_server/test_ownership_route.py tests/ui_server/test_pause_e2e_live.py tests/ui_server/test_steering_note_e2e_live.py "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" tests/orchestration/test_ownership_phrases.py tests/orchestration/test_ownership_ledger.py tests/orchestration/test_pingpong_job_ownership.py tests/cli/test_job_ownership.py tests/regression/test_named_bugs.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -16; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection less the new file, serially, in the primary checkout at
 `4d56671b`, and read `1654 passed, 11 skipped` at real exit code 0; the skips are the F252
 quarantines. Report every `SKIPPED` line and account for the new total. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass`.

G4 THE RENDER — `python3 .agent/authored/f035-r7-render_measure.py /home/decodeux/Repos/remedy`
 at C4, its whole output with its real exit code, which must be 0 with C-a to C-g passing; the
 byte counts of the two screenshots, which must differ; then `git status --porcelain` and
 `ls .remedy-wt/f035-render-run`, which must show the work dir gone.

G5 THE RED PROOFS — your tool `.agent/authored/f035-r7-mutations.py` takes a worktree path, edits
 the named file inside it (its FROM text occurring exactly once), runs `python3 -B -m pytest -q
 -p no:cacheprovider tests/orchestration/test_ownership_phrases.py
 tests/ui_contracts/test_ownership_view_contract.py tests/ui_server/test_ownership_e2e_live.py`
 from the worktree's root after purging its `__pycache__`, restores the bytes, and prints one line
 per mutation with its exit code, failed count and failing node ids; an unmutated control runs
 first and last; it ends with `restored byte-identical: True`, the PRIMARY checkout's
 `git status --porcelain`, empty, and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`.
  m1 `ownership_phrases.py`: the unreachable clause is appended for no id again;
  m2 `EvidencePanel.module.css`: `.ownershipList` loses `list-style: none`;
  m3 `EvidencePanel.tsx`: the tab's `<ul>` loses `className={styles.ownershipList}`;
  m4 `ownership.py`: a resume's actor is read from the event's `source`;
  m5 `ui_server.py`: `_build_ownership_json` answers the entries without their `sentence`.
 Run it at C6 in `.remedy-wt/f035-r7-mut` and report its whole output. EVERY mutation must be
 red; one that stays green is reported as green, never papered over, and you add the test that
 catches it before C7 and re-run the tool. Then remove the worktree and `git worktree prune`.

G6 TREE AND PUSH — after C7: `git status --porcelain`, which must be empty;
 `git log --oneline -n 8`, which must show C7 down to C1 and `4d56671b` in that order (more lines
 if constraint 2 split a commit); the worktree and `remedy/*` counts, equal to your step 4
 readings; the push's real outcome; and `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, which must be EMPTY. These go in your reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 to C6), every gate's real
output and exit code, the authored-text proofs, the item-status table AGENTS.md requires (one row
per commit, per gate, and for R-1083 and R-1084), the deviations, and the next expected action.
Report what you ran, not what you expected to find. Your Session section reads SESSION 1 of
feature F035, round 7, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 7 including the repairs of R-1083 and R-1084, then the closure sequence's first round — the
Built State, the checklist consolidation and the one full-suite run. State the open-findings
count, 2 (R-1083 and R-1084, landed and awaiting review), and the operator-questions count, 0.
