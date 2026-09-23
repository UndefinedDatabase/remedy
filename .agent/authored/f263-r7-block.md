STEP F263 R7 — the closure sequence's first half: the one-path guard, the built state, the self-use item and the feature's one full suite

GOAL
Book round 6's PASS, add the guard test that holds absorption to one implementation, append the
feature file's Built State, generate the closure's self-use item and run it to its approval gate,
and run this feature's ONE full suite, committing its transcript.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. The reviewer authors every payload; you apply them byte for
byte. This round closes nothing: the STATUS line, the evidence job, the review zip and the pull
request belong to later rounds, and no commit of this round may touch `docs/roadmap/STATUS.md`,
`README.md` or any `consumed_by` field of `scripts/self_use_queue.json`.

THREE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f263-r7-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f263-r7-scratch/`   READ-ONLY. The reviewer's simulation tools.
  `.remedy-wt/f263-r7-worker/`    YOURS for logs, captures and scripts.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, heredocs written with `cat >`, process substitution, `$?` or
`${...}` outside a `bash -c`, `cd <dir> && git ...`, shell `for` loops, brace expansion, `awk`,
`xxd`, `bc`, a `grep` pattern holding `$`, and multi-operation one-liners chained with `;`, `&&`
or `|` outside a `bash -c`; put multi-step code in a scratch Python file. Capture real exit codes
as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C <dir>` for a worktree. The `remedy` CLI
itself is denied: run `python3 -m apps.cli.main ...`. NEVER USE `git stash` IN ANY FORM, and never
check out another commit in the primary checkout.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` empty, `git branch --show-current` reads
   `feature/f263-human-change-absorption`, `git log --oneline -1` reads `d59371c1`.
3. Verify this block's own bytes (R-0954): line count and sha256 of `.remedy-wt/f263-r7-block.md`
   against the two readings your delegation message states. Report both beside both, and stop if
   either differs.
4. Record, before anything runs: `git branch --list 'remedy/job-*'` count, `git worktree list`,
   and the first line of `git stash list`.

PAYLOADS — under `.remedy-wt/f263-r7-payloads/`, printed by the reviewer's dry run
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| built_state.md | 67 | 4666 | 7fe23a18a86d8e30c9a3e368c801989743d7653a75eab325f1090627ae3fa5d8 |
| ledger.md | 2 | 2444 | 81f1f7010f5c9683a39c444dcf370dad0fb26fc68f7085a7d6bfc5aba6652770 |
| plan.md | 33 | 1300 | 2365c1ee82c6098299a9de560529201680663bacec243a56fe7c573bd10b8192 |
| test_human_change_one_path.py | 60 | 2752 | 914a2589d84c7f4957f275d1506fa66eeaa7065e25e93a6b255ecab716c0c145 |
| mutations.py | 57 | 2436 | bd7986ba20e5b9e2e4b4a7ada54005cc94179cd3c88fe583516304f241a71b10 |

`ledger.md` is an APPEND beginning with the single newline that separates records: round 6's
`Gate:` entry. `built_state.md` is an APPEND onto `docs/roadmap/features/T2_F263.md`, beginning
with the blank line that separates it from the Orchestrator brief. `plan.md` is a REWRITE.
`test_human_change_one_path.py` is a NEW file. Appends are strict byte concatenation onto the file
as it stands at `d59371c1`. Never retype or edit a payload; copy with `shutil.copyfile`.

BUNDLE — commits C1 to C6, in this order.

C1 — `.agent/authored/f263-r7-block.md` := this block; `.agent/authored/f263-r7-<name>` for each
  payload, keeping its file name.
  Subject: `F263 R7 C1: copy round 7 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 219. Report the number you measure.

C2 — `.agent/live_review.md` += ledger.md · `.agent/plan.md` := plan.md.
  Subject: `F263 R7 C2: book round 6's PASS`
  Expected insertions by `git show --numstat`: 2 live_review.md, 13 plan.md.

C3 — `tests/orchestration/test_human_change_one_path.py` := test_human_change_one_path.py.
  Subject: `F263 R7 C3: hold the command, the safe points and the apply to one absorption path`
  Expected insertions: 60.

C4 — `docs/roadmap/features/T2_F263.md` += built_state.md.
  Subject: `F263 R7 C4: write the feature file's Built State`
  Expected insertions: 67.

C5 — THE SELF-USE ITEM (closure precondition 6), from a scratch Python file run in the primary
  checkout:
  (a) `packages.orchestration.self_use_generator.generate_and_append_if_empty()` FIRST, with no
      arguments. The reviewer's dry run in a worktree at `d59371c1` appended `SU-029`, "Address
      ledger finding R-1000", provenance `generated (self-use-generator tier 1, ledger scan,
      R-1000)`. Report what yours does, and report `next_self_use_item()`'s answer.
  (b) RUN it with `packages.orchestration.self_use_runner.run_next_self_use_item`, with
      `dest_dir` = `.remedy-wt/f263-r7-selfuse` and nothing else, so `max_tasks` stays 1 and
      both roles resolve from the one `self_use` role configuration (DECISION
      amend0920-selfuse-real D2). It runs to the approval gate and is NEVER applied. A blocked
      or stopped job is an outcome to record, not a reason to stop.
  (c) Save under `.agent/selfuse_f263/`, mirroring `.agent/selfuse_f279/`'s file names: the item
      markdown as `SU-029.md` (or the id (a) really produced), `entry_and_job_file.txt`,
      `execution_config.txt`, `result_state.txt`, `timing.txt`, `full_transcript.txt`, and
      `run_defects.txt` holding every string
      `packages.orchestration.self_use_findings.describe_self_use_run_defects` returns for the
      run's own `JobPlan` — verbatim, and the literal `NONE` if it returns an empty tuple. ALSO
      `human_change_checks.txt`: the returned `JobPlan`'s `metadata.get("human_change_checks")`
      as JSON (the literal `ABSENT` if it is None), and on its next line the sorted list
      `packages.orchestration.human_change.recorded_human_changes(<job id>)` returns. This is
      the Acceptance list's measured cost of the check, read from a real job.
  (d) Then `python3 -m pytest tests/docs/ -q`. The generated item's text lands in the tracked
      `scripts/self_use_queue.json`, which `tests/docs/test_retired_promote_word.py` reads (finding
      R-1015). If yours is red, STOP under constraint 5.
  This commit's paths: `scripts/self_use_queue.json` and `.agent/selfuse_f263/**`. You register
  no finding: the reviewer authors every registration from `run_defects.txt` next round.
  Subject: `F263 R7 C5: generate and run the closure's self-use item, record its defects`

C6 — THE INTEGRATION GATE, this feature's ONE full suite (operator amendment amend0917-throughput
  rule 1), in the PRIMARY checkout, after C5:
  (a) Build the UI first, because a cold `apps/ui/dist` reddens `tests/ui_server/` under `-n`:
      `bash -c 'npm --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'`.
      Never run `npm install`; a build that needs the network is a STOP under constraint 5. Then
      `git status --porcelain`, which must still be empty.
  (b) `python3 -m pytest -n auto -q`, its log written outside the repository at
      `~/remedy-gate-scratch/f263-r7-full-suite.log`; if the sandbox refuses that path, write it
      under `.remedy-wt/f263-r7-worker/` and say so. Commit the summary line, the real exit code
      and the FULL list of bad node ids as `.agent/authored/f263-closure-suite.txt`, together
      with the handback: `.agent/handoff.md` rewritten per `docs/agents/handback_template.md` in
      this same commit.
  Subject: `F263 R7 C6: record the closure suite transcript and rewrite handoff for round 7`
  Then `git push origin feature/f263-human-change-absorption`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is AT MOST: the `.agent/authored/f263-r7-*` copies C1 makes,
   `.agent/live_review.md`, `.agent/plan.md`, `tests/orchestration/test_human_change_one_path.py`,
   `docs/roadmap/features/T2_F263.md`, `scripts/self_use_queue.json`, `.agent/selfuse_f263/**`,
   `.agent/authored/f263-closure-suite.txt` and `.agent/handoff.md`. Report the set you measure
   with `git diff --name-only d59371c1` after C6. Nothing under `packages/` or `apps/`, no
   `docs/roadmap/STATUS.md`, no root `README.md`, and none of `.agent/candidates.md`,
   `.agent/context.md`, `.agent/operator_questions.md`, `.agent/decisions.md`,
   `.agent/prose_slips.md`.
4. If the full suite in C6 is RED, that is this feature's work and not a reason to stop: commit
   the transcript exactly as measured, report every bad node id, and hand back. The repair rounds
   are the reviewer's to order (amend0917-throughput rule 2). Never weaken an assertion, delete a
   test or mark anything xfail on your own initiative.
5. If any other gate goes red, STOP: commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED, NOTHING IS CLOSED. No `gh pr merge`, no `gh pr create`, no checkout of
   `main`, no STATUS edit, no `consumed_by` edit, no review zip, no evidence job.
7. The self-use run may leave `remedy/job-*` branches, worktrees or evidence directories behind.
   Report them; delete NOTHING you did not create as scratch, and never delete a branch. Leave
   the three existing `.remedy-wt/job-*` worktrees and their branches alone.

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G4 run BEFORE C6's handback text is written,
in that order, and G5 is the suite run, the last of them.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 committed `.agent/authored/f263-r7-*` blob, read with `git show <C1>:<path>`, compared byte for
 byte with its source (the block copy against `.remedy-wt/f263-r7-block.md`). One reading per
 file, all equal.

G2 THE BOOKING, THE GUARD AND THE BUILT STATE — read with `git show <commit>:<path>`, each equal
 to the reviewer's dry run:
 | path | at | bytes | sha256 |
 |---|---|---|---|
 | .agent/live_review.md | C2 | 386333 | 5eb308ca8ad0a5edc7d77107c256d8dc94afbbd80b8134979c7b9713b73d7c6a |
 | .agent/plan.md | C2 | 1300 | 2365c1ee82c6098299a9de560529201680663bacec243a56fe7c573bd10b8192 |
 | tests/orchestration/test_human_change_one_path.py | C3 | 2752 | 914a2589d84c7f4957f275d1506fa66eeaa7065e25e93a6b255ecab716c0c145 |
 | docs/roadmap/features/T2_F263.md | C4 | 10918 | 95e5ba419bb70a15addae365e683f12e304930470b019db179f8e8824f78e516 |
 Also: lines beginning `Gate: F263 R6 — ` at C2, 1; the open set by distinct id via
 `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's TEXT at `d59371c1` and
 at C2, with both set differences — the reviewer read 28 and 28, both empty; and at C4, in the
 primary checkout, `python3 -m pytest -q -p no:cacheprovider tests/docs/
 tests/orchestration/test_human_change_one_path.py tests/cli/test_golden_path.py` and
 `python3 -m ruff check .` from the repository root, each with its real exit code.

G3 THE RED PROOFS — `git worktree add --detach .remedy-wt/f263-r7-mut <C3>`, then
 `python3 -B .remedy-wt/f263-r7-payloads/mutations.py .remedy-wt/f263-r7-mut`. The reviewer's dry
 run read: both controls `2 passed` at exit 0; `m1_the_command_spells_its_own_absorption` 2
 failed, `m2_the_safe_point_leaves_the_path` 1 failed, `m3_the_apply_leaves_the_path` 1 failed,
 each at exit 1; every FROM count 1 and every restore byte-identical. Report every line the tool
 prints. Then `git worktree remove --force .remedy-wt/f263-r7-mut`, `git worktree prune`, and
 `git worktree list`.

G4 THE SELF-USE ITEM AND THE TREE — at C5: the generator's answer and `next_self_use_item()`'s;
 the runner's returned entry id, job id, job file path and job state; the `execution_config`'s
 builder and reviewer names and models, which must be the `self_use` role's configured provider
 and never `fake`; the `describe_self_use_run_defects` output verbatim; the two lines of
 `human_change_checks.txt`; `python3 -m pytest tests/docs/ -q` after the queue file is written,
 with its exit code; and `git branch --list 'remedy/job-*'` counted before C1 and after C5 with
 `git worktree list` beside each. Then, still at C5 and BEFORE the UI build:
 `python3 -m apps.cli.main integrity check --json`, all five checks `pass` at `fail_count` 0, and
 `git status --porcelain` empty with no untracked file (closure precondition 3).

G5 THE INTEGRATION GATE — the UI build's last line and real exit code, and `git status
 --porcelain` after it; then `python3 -m pytest -n auto -q` in the primary checkout, its real exit
 code, its summary line and every bad node id, all of it in `.agent/authored/f263-closure-suite.txt`.
 Report whether `tests/orchestration/test_import_reachability.py` or
 `tests/test_no_orphan_modules.py` holds a bad node (closure precondition 7).

G6 TREE AND PUSH — after C6: `git status --porcelain` empty; `git log --oneline -n 7`, showing C6
 to C1 and `d59371c1`; `git worktree list`; `git stash list`'s first line unchanged from its reading
 before C1; the push's real outcome; `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, EMPTY. These go in your final reply, not the handback —
 the push ships the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, and AGENTS.md's
item-status table with one row per commit and per gate: state block, the per-commit
changed-files table with the insertions git MEASURED beside the ones this block expected, every
gate's real output and exit code, the self-use run's entry id, job id, provider, state, defect
list and check-cost reading, the full suite's summary line and bad node ids, the deviations, and
the next action. Your Session section reads SESSION 2 of feature F263, round 7, and says in one
sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
7, then the closure sequence's second half — the registrations the self-use defects ask for, any
repair the suite requires, the evidence job and the review package — and then the closing round:
the ledger rotation, the STATUS line with the README counters in the same commit, and the pull
request. The open set stays at the 28 of `d59371c1` after this round; operator questions open: 0.
