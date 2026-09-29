STEP F039 R11 — THE CLOSURE SEQUENCE'S SELF-USE ROUND: book round 10 with R-1103's resolution, then generate and run the closure's self-use item to its approval gate

GOAL
Round 10 passed and the one full suite is green. Book round 10's verdict with R-1103's `Done:` line
and the plan, then meet precondition 6 of `docs/roadmap/STATUS_closure_protocol.md`: generate the
closure's self-use item and run it to its approval gate on the `self_use` role, recording its readings
under `.agent/selfuse_f039/`. The job is never applied. The evidence bundle, the review package, the
rotation, the STATUS line and the pull request belong to later rounds.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. Every change this round makes travels as a payload or is
produced by the payload script; you write no code and no prose outside the handback.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f039-r11-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f039-r11/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f039-r11-selfuse/`   Where the self-use run writes its job file; the payload names it.
  `.remedy-wt/f039-r11-jobtree/`   The payload adds and removes it itself; never touch it.
  `.remedy-wt/f039-r11-rec/` and `.remedy-wt/f039-review/`   The reviewer's; do not touch them.
  `.remedy-wt/f039-r11-worker/`    YOURS for logs and scripts; create it if absent. All are
                                   gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution,
`cd <dir> && git ...`, and multi-operation one-liners chained with `;` or `&&` outside a
`bash -c`. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read
`${PIPESTATUS[0]}` when you pipe. Use `git -C <path>` rather than `cd`, and never `cd` your shell
into a worktree. Use `python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A
heredoc containing a dollar-brace or a backslash inside an f-string is refused or fails: write
such a script to a file under your own directory and run the file. Never run npm or npx. The
`remedy` command is denied; use `python3 -m apps.cli.main` where a gate names it.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f039-story-replay-mode`, and `git log --oneline -1` must read `0f07b2f8b`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f039-r11/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` and the count of `git branch --list 'remedy/*'` as found.

PAYLOADS — under `.remedy-wt/f039-r11-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 27 | 899 | 07e203e61c0a43997ef16568598002c71d302667fe8218974093d155c62c91c9 |
| booking.diff | 12 | 5844 | f6126c3132481ad35e671e61b9c95a3fb6f647f31ef986b80bad3fcd6b28ed5b |
| selfuse.py | 121 | 6424 | c000469068a75a2c080ba89e3c522a6cfc4239915197e968bce3b5c88a95ee08 |

`plan.md` is a REWRITE of `.agent/plan.md`. `booking.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a records tree at `0f07b2f8`. It appends round 10's gate
entry and R-1103's `Done:` paragraph to `.agent/live_review.md`. `selfuse.py` is the reviewer's
script for C3, adapted from F288's `.agent/authored/f288-r7-selfuse.py`, run from the primary
checkout.

BUNDLE — the commits are C1, C2, C3 and C4, in this order.

C1 — copy this block and the payloads
  `.agent/authored/f039-r11-block.md` := this block, and `.agent/authored/f039-r11-plan.md`,
  `.agent/authored/f039-r11-booking.diff` and `.agent/authored/f039-r11-selfuse.py` := the three
  payloads, by `shutil.copyfile`. Subject: `F039 R11 C1: copy round 11 block and payloads into
  .agent/authored/`. Its insertions are this block's line count plus 160. Report the number you
  measure and STOP rather than commit if it is 500 or more.

C2 — THE BOOKING: `git apply --check` then `git apply` booking.diff, then rewrite `.agent/plan.md`
  := plan.md. Subject: `F039 R11 C2: book round 10 and resolve R-1103`. Expected by
  `git show --numstat`: 4/0 `.agent/live_review.md`, 5/9 `.agent/plan.md`. Push after C2.

C3 — THE SELF-USE ITEM (closure precondition 6): run
  `bash -c 'python3 .remedy-wt/f039-r11-payloads/selfuse.py 2>&1 | tee .remedy-wt/f039-r11-worker/selfuse.log; echo "REAL_EXIT=${PIPESTATUS[0]}"'`
  in the primary checkout AFTER C2 is committed, with a Bash timeout of 3600000 milliseconds: the
  run makes real provider calls, each allowed ten minutes, and may take most of an hour. It appends
  the generated item to `scripts/self_use_queue.json`, runs it on the `self_use` role's configured
  provider, and writes `.agent/selfuse_f039/`. The reviewer's run of the generator in its records
  tree, over the same booking, read the item as `SU-035`, from Tier 2 (`doc_config_keys`),
  generated from the claim that `docs/guides/story-user-guide-v1.md` backticks the config key
  `story.html`; report what the run reads. A job that ends blocked or stopped is an OUTCOME to
  record, never a reason to stop or to re-run; only a Python exception before the job exists is a
  STOP. Commit `scripts/self_use_queue.json` and `.agent/selfuse_f039/**`, and nothing else.
  Subject: `F039 R11 C3: generate and run the closure's self-use item, record its readings`

C4 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`. Subject: `F039 R11 C4: rewrite handoff for round 11`.
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading. If one would reach
   500, split it into lettered parts before committing and declare the split.
3. The round's whole tracked path set is: the `.agent/authored/f039-r11-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `scripts/self_use_queue.json`,
   `.agent/selfuse_f039/**` and `.agent/handoff.md`. Report the list you measure with
   `git diff --name-only 0f07b2f8b` after C4. No `consumed_by` is set this round: the closure
   commit sets it.
4. The self-use job is NEVER applied: no `job apply`, no `--approve`, no copying of its files into
   the checkout. It may leave a `remedy/job-*` branch or an evidence directory behind; report
   each, and delete nothing you did not create as scratch.
5. If a gate other than the self-use outcome goes red, STOP, commit and push what is verified,
   write an honest handoff under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
7. DO NOT run the full suite: it ran once, in round 10, on `fd89095f`.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C4 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f039-r11-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f039-r11/block.md`), read back with
 `git show <C1>:<path>`. Report one reading per copy.

G2 THE BOOKING — the byte count and sha256 of each file below, read with `git show <C2>:<path>`,
 equal the reviewer's reading, printed from its records tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 366785 | 2adf0ff4e1b3ca92f2aa653e1324091d2549df5130820166ea8948ec2aa95221 |
 | .agent/plan.md | 899 | 07e203e61c0a43997ef16568598002c71d302667fe8218974093d155c62c91c9 |
 Also `open_finding_ids` and `latest_gate_verdict` from `scripts/rotate_live_review.py` (import it
 with `scripts` on `sys.path`) over the ledger's TEXT at C2: the reviewer read `[]` and `PASS`.

G3 THE TESTS, in the primary checkout at C3, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/docs tests/orchestration/test_doc_staleness.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_self_use_findings.py tests/orchestration/test_self_use_job.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection in its records tree carrying C2 with the generated item
 appended as C3 appends it and read `641 passed, 1 skipped` at real exit code 0, the skip
 `tests/test_agent_tooling.py:43`, a standing quarantine; report the counts and every skip line you
 read. Then `python3 -m apps.cli.main integrity check --json`, which must read all six checks with
 status `pass` at `fail_count` 0 — the STATUS of each check is the reading, not the exit code.

G4 THE SELF-USE READINGS — the whole output of C3's command and its real exit code; the item's
 id, title and provenance; the job's id and state; the builder and reviewer provider and model
 from `.agent/selfuse_f039/execution_config.txt`, which must name the `self_use` role's provider
 and never `fake`; the budgets and the budget actuals; every task's status, verdict and final
 status; `.agent/selfuse_f039/changed_paths.txt`, `.agent/selfuse_f039/staleness_after.txt`,
 `.agent/selfuse_f039/job_diff.txt` and `.agent/selfuse_f039/run_defects.txt` verbatim; and
 `git worktree list | wc -l` and the count of `git branch --list 'remedy/*'` after the run.

G5 SIZES — `git show --numstat --format= <commit>` for C1, C2 and C3, each reported beside the
 expected insertions of its entry above where one is stated, and placed in the handback's
 `## Commits` table exactly as the tool printed it.

G6 TREE AND PUSH — after C4: `git status --porcelain`, which must be empty;
 `git log --oneline -n 5`, which must show C4, C3, C2, C1 and `0f07b2f8b` in that order; the
 push's real outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
 which must be EMPTY. These readings go in your reply, since C4 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the self-use readings, the
authored-text proofs, the item-status table AGENTS.md requires (one row per commit and per gate),
the deviations, and the next expected action. Report what you ran, not what you expected to find.
Your Session section reads SESSION 2 of feature F039, round 11, rounds so far 11, and says in one
sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 11 and of the self-use run, then the closure's evidence round — the booking of round 11,
any finding the self-use run raises, the evidence bundle and the review package — and then the
closing round. State the open-findings count, 0, and "Operator questions open: 1".
