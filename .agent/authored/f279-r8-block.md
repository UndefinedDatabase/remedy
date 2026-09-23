STEP F279 R8 — the closure sequence's first half: the built state, the self-use item and the feature's one full suite

GOAL
Book round 7's PASS, append the feature file's Built State, generate the closure's self-use item
and run it to its approval gate, and run this feature's ONE full suite, committing its transcript.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. The reviewer authors every payload; you apply them byte for
byte. This round closes nothing: the STATUS line, the evidence job, the review zip and the pull
request belong to later rounds, and no commit of this round may touch `docs/roadmap/STATUS.md`,
`README.md` or any `consumed_by` field of `scripts/self_use_queue.json`.

THE REVIEWER CHECKLIST IS NOT EDITED THIS ROUND. The feature file's "Do not touch" section keeps
the checklist's text out of this feature's reach, and F279's one prose lesson is already carried by
checklist item 12; the Built State payload says so. `docs/agents/planner_reviewer_prompt.md` is
therefore outside this round's path set.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f279-r8-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f279-r8-scratch/`   YOURS for logs, captures and scripts, EXCEPT every file the
      reviewer put there before C1 (`measure_r7.py`, `review_r7.py`, `dry.py`), which is
      read-only to you.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, heredocs written with `cat >`, process substitution, `$?` or
`${...}` outside a `bash -c`, `cd <dir> && git ...`, shell `for` loops, brace expansion, `awk`,
`xxd`, `bc`, a `grep` pattern holding `$`, and multi-operation one-liners chained with `;`, `&&`
or `|` outside a `bash -c`; put multi-step code in a scratch Python file. Capture real exit codes
as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C <dir>` for a worktree. A directory outside
the repository is made with Python's `os.makedirs`. The `remedy` CLI itself is denied: run
`python3 -m apps.cli.main ...`. NEVER USE `git stash` IN ANY FORM, and never check out another
commit in the primary checkout.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` empty, `git branch --show-current` reads
   `feature/f279-configuration-toolchain-truth`, `git log --oneline -1` reads `4f43baf6`.
3. Verify this block's own bytes (R-0954): line count and sha256 of `.remedy-wt/f279-r8-block.md`
   against the two readings your delegation message states. Report both beside both, and stop if
   either differs.
4. Record, before anything runs: `git branch --list 'remedy/job-*'` count, `git worktree list`,
   and the first line of `git stash list`.

PAYLOADS — under `.remedy-wt/f279-r8-payloads/`, printed by the reviewer's dry run
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| built_state.md | 67 | 5101 | 1a8ba931d105432bbaa7ce1735dc336f868950d84e1c6bb7eb9c4309e94969d4 |
| ledger.md | 2 | 1873 | e63e3804210b257920edf5297efd48f6cd8d7db0efee4dd086a188614f07ff89 |
| plan.md | 32 | 1335 | f411ff3344534c575356e4bab176d521d3364fcdffb4d62f31b0fa6023c9ad2f |

`ledger.md` is an APPEND beginning with the single newline that separates records: round 7's
`Gate:` entry. `built_state.md` is an APPEND onto `docs/roadmap/features/T2_F279.md`, beginning
with the blank line that separates it from the Orchestrator brief. `plan.md` is a REWRITE. Appends
are strict byte concatenation onto the file as it stands at `4f43baf6`. Never retype or edit a
payload.

BUNDLE — commits C1 to C5, in this order.

C1 — `.agent/authored/f279-r8-block.md` := this block; `.agent/authored/f279-r8-<name>` for each
  payload, keeping its file name. Byte for byte, with `shutil.copyfile`.
  Subject: `F279 R8 C1: copy round 8 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 101. Report the number you measure.

C2 — `.agent/live_review.md` += ledger.md · `.agent/plan.md` := plan.md.
  Subject: `F279 R8 C2: book round 7's PASS`
  Expected insertions by `git show --numstat`: 2 live_review.md, 11 plan.md.

C3 — `docs/roadmap/features/T2_F279.md` += built_state.md.
  Subject: `F279 R8 C3: write the feature file's Built State`
  Expected insertions: 67.

C4 — THE SELF-USE ITEM (closure precondition 6), from a scratch Python file run in the primary
  checkout:
  (a) `packages.orchestration.self_use_generator.generate_and_append_if_empty()` FIRST, with no
      arguments. The reviewer's dry run in a worktree at `4f43baf6` carrying C2 and C3 appended
      `SU-028`, "Refresh the pinned toolchain", from the ORDER tier, its provenance reading
      `generated (self-use-generator order tier, docs/orders/toolchain-refresh.md, <day>)` with
      the day the call ran. Report what yours does, and report `next_self_use_item()`'s answer.
  (b) RUN it with `packages.orchestration.self_use_runner.run_next_self_use_item`, with
      `dest_dir` = `.remedy-wt/f279-r8-selfuse` and nothing else, so `max_tasks` stays 1 and
      both roles resolve from the one `self_use` role configuration (DECISION
      amend0920-selfuse-real D2). Report the `execution_config` the returned `JobPlan` carries,
      which is the proof of which provider actually ran. It runs to the approval gate and is
      NEVER applied. A blocked job is an outcome to record, not a reason to stop.
  (c) Save under `.agent/selfuse_f279/`, mirroring `.agent/selfuse_f278/`'s file names: the item
      markdown as `SU-028.md` (or the id (a) really produced), `entry_and_job_file.txt`,
      `execution_config.txt`, `result_state.txt`, `timing.txt`, `full_transcript.txt`, and
      `run_defects.txt` holding every string
      `packages.orchestration.self_use_findings.describe_self_use_run_defects` returns for the
      run's own `JobPlan` — verbatim, and the literal `NONE` if it returns an empty tuple.
  (d) Then `python3 -m pytest tests/docs/ -q`. The generated item's text lands in the tracked
      `scripts/self_use_queue.json`, which `tests/docs/test_retired_promote_word.py` reads (finding
      R-1015). The reviewer's dry run read `322 passed` at exit 0 with the generated item in
      place. If yours is red, STOP under constraint 5.
  This commit's paths: `scripts/self_use_queue.json` and `.agent/selfuse_f279/**`. You register
  no finding: the reviewer authors every registration from `run_defects.txt` next round.
  Subject: `F279 R8 C4: generate and run the closure's self-use item, record its defects`

C5 — THE INTEGRATION GATE, this feature's ONE full suite (operator amendment amend0917-throughput
  rule 1), in the PRIMARY checkout, after C4:
  (a) Build the UI first, because a cold `apps/ui/dist` reddens `tests/ui_server/` under `-n`:
      `bash -c 'npm --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'`.
      Never run `npm install`; a build that needs the network is a STOP under constraint 5. Then
      `git status --porcelain`, which must still be empty.
  (b) `python3 -m pytest -n auto -q`, its log written outside the repository
      (`~/remedy-gate-scratch/` is writable). Commit the summary line and the FULL list of bad
      node ids as `.agent/authored/f279-closure-suite.txt`, together with the handback:
      `.agent/handoff.md` rewritten per `docs/agents/handback_template.md` in this same commit.
  Subject: `F279 R8 C5: record the closure suite transcript and rewrite handoff for round 8`
  Then `git push origin feature/f279-configuration-toolchain-truth`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`. F279's one declared oversize
   commit was round 1's `constraints.txt`; there is no second.
3. The round's tracked path set is AT MOST: the `.agent/authored/f279-r8-*` copies C1 makes,
   `.agent/live_review.md`, `.agent/plan.md`, `docs/roadmap/features/T2_F279.md`,
   `scripts/self_use_queue.json`, `.agent/selfuse_f279/**`,
   `.agent/authored/f279-closure-suite.txt` and `.agent/handoff.md`. Report the set you measure
   with `git diff --name-only 4f43baf6` after C5. Nothing under `packages/`, `apps/` or `tests/`,
   no `docs/roadmap/STATUS.md`, no root `README.md`, and none of `.agent/candidates.md`,
   `.agent/context.md`, `.agent/operator_questions.md`, `.agent/decisions.md`,
   `.agent/prose_slips.md`.
4. If the full suite in C5 is RED, that is this feature's work and not a reason to stop: commit
   the transcript exactly as measured, report every bad node id, and hand back. The repair rounds
   are the reviewer's to order (amend0917-throughput rule 2). Never weaken an assertion, delete a
   test or mark anything xfail on your own initiative.
5. If any other gate goes red, STOP: commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED, NOTHING IS CLOSED. No `gh pr merge`, no `gh pr create`, no checkout of
   `main`, no STATUS edit, no `consumed_by` edit, no review zip, no evidence job.
7. The self-use run may leave `remedy/job-*` branches, worktrees or evidence directories behind.
   Report them; delete NOTHING you did not create as scratch, and never delete a branch. Leave
   `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-e7268925db3a4831` and their branches alone.

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C5's handback text is written,
in the order G1, G2, G3, G5, G4: the suite run is the last of them.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 committed `.agent/authored/f279-r8-*` blob, read with `git show <C1>:<path>`, compared byte for
 byte with its source (the block copy against `.remedy-wt/f279-r8-block.md`). One reading per
 file, all equal.

G2 THE BOOKING AND THE BUILT STATE — read with `git show <commit>:<path>`, each equal to the
 reviewer's dry run:
 | path | at | bytes | sha256 |
 |---|---|---|---|
 | .agent/live_review.md | C2 | 388566 | 9a55543b2b8aabcf092102d0b0358421a2a99aa19b8450d46248afe2cb7e99ca |
 | .agent/plan.md | C2 | 1335 | f411ff3344534c575356e4bab176d521d3364fcdffb4d62f31b0fa6023c9ad2f |
 | docs/roadmap/features/T2_F279.md | C3 | 14071 | 4bc6b25f4510d0c7bc9d518d2dd8305a2bdb9d08a4b3ae77f225956b08b3c8e8 |
 Also: lines beginning `Gate: F279 R7 — ` at C2, 1; the open set by distinct id via
 `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's TEXT at `4f43baf6` and
 at C2, with both set differences — the reviewer read 26 and 26, both empty; and
 `python3 -m pytest tests/docs/ -q` at C3, since C3 writes a roadmap file.

G3 THE SELF-USE ITEM — at C4: the generator's answer and `next_self_use_item()`'s; the runner's
 returned entry id, job file path and job state; the `execution_config`'s builder and reviewer
 names and models, which must be the `self_use` role's configured provider and never `fake`; the
 `describe_self_use_run_defects` output verbatim; `python3 -m pytest tests/docs/ -q` after the
 queue file is written, with its exit code; and `git branch --list 'remedy/job-*'` counted before
 C1 and after C4 with `git worktree list` beside each.

G4 THE INTEGRATION GATE — the UI build's last line and real exit code, and `git status
 --porcelain` after it; then `python3 -m pytest -n auto -q` in the primary checkout, its real exit
 code, its summary line and every bad node id, all of it in `.agent/authored/f279-closure-suite.txt`.
 Report whether `tests/orchestration/test_import_reachability.py` or
 `tests/test_no_orphan_modules.py` holds a bad node (closure precondition 7).

G5 THE TREE — at C4, BEFORE the UI build and the suite: `python3 -m apps.cli.main integrity
 check --json`, all five checks `pass` at `fail_count` 0, and `git status --porcelain` empty with
 no untracked file (closure precondition 3). The suite writes no tracked file, so this reading
 stands for the tree G4 runs on.

G6 TREE AND PUSH — after C5: `git status --porcelain` empty; `git log --oneline -n 6`, showing C5
 to C1 and `4f43baf6`; `git worktree list`; `git stash list`'s first line unchanged from its reading
 before C1; the push's real outcome; `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, EMPTY. These go in your final reply, not the handback —
 the push ships the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, and AGENTS.md's
item-status table with one row per commit and per gate: state block, the per-commit
changed-files table with the insertions git MEASURED beside the ones this block expected, every
gate's real output and exit code, the self-use run's entry id, provider, state and defect list,
the full suite's summary line and bad node ids, the deviations, and the next action. Your Session
section reads SESSION 2 of feature F279, round 8, and says in one sentence how much context you
had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
8, then the closure sequence's second half — the registrations the self-use defects ask for, any
repair the suite requires, the evidence job and the review zip — and then the closing round: the
ledger rotation, the STATUS line with the README counters in the same commit, and the pull
request. State the open-findings count, 26 after this round, and the operator-questions count, 0.
