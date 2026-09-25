STEP F285 R3 — THE CLOSURE SEQUENCE'S FIRST ROUND: book round 2, then generate and run the closure's self-use item

GOAL
Book round 2's PASS with the resolution of R-1055, then meet closure precondition 6 of
`docs/roadmap/STATUS_closure_protocol.md`: generate the closure's self-use item, which the
reviewer's dry run reads as `SU-032`, "Address ledger finding R-1064", and RUN it to its approval
gate on the `self_use` role, recording its readings and its defects under `.agent/selfuse_f285/`.
It is never applied. Its diff is judged by the reviewer at the next gate (DECISION F285 D1).

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict, never merge, and never write a `Done:` or `Landed:` line.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f285-r3-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f285-r3/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f285-r3-drafts/`    READ-ONLY. The reviewer's drafts and builders.
  `.remedy-wt/f285-r3-dry/`       The reviewer's dry tree; do not touch it.
  `.remedy-wt/f285-r3-selfuse/`   Where the self-use run writes its job file; the payload names it.
  `.remedy-wt/f285-r3-worker/`    YOURS for logs and scripts; create it if absent. All of these
                                  are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `cd <dir> && git ...`, and multi-operation
one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace or a brace next to a quote is
refused: write such a script to a file under your own directory and run the file. The ONE npm
command this round may run is G3's `npm --prefix apps/ui run build`; never `npm install`,
`npm ci` or `npx`. Never `git stash`, never `pkill -f`.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f285-findings-paydown-v4`, and `git log --oneline -1` must read `0fc0d8d0`. Report
   all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f285-r3/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*'` as found.

PAYLOADS — under `.remedy-wt/f285-r3-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 12 | 6713 | 935261ff0ee1a812d1ebcc096539bc14b654008eb1cd61c55d9abb3d9a953b03 |
| plan.md | 29 | 1080 | 2402f472e5956ee2702f17bcfe79a921ef321fa86c90afec34a3be88bca89911 |
| selfuse.py | 85 | 4481 | 4476d47c9625234cba0966f285120ac10854057463095cee5fdd0242127e808b |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `0fc0d8d0`, and it appends to
`.agent/live_review.md` the F285 round 2 gate entry and R-1055's resolution. `selfuse.py` is a
TOOL for C3: it is run from the primary checkout, never applied to a tracked file.

BUNDLE — the commits are C1, C2, C3 and C4, in this order.

C1 — copy this block and the payloads
  `.agent/authored/f285-r3-block.md` := this block, and `.agent/authored/f285-r3-records.diff`,
  `.agent/authored/f285-r3-plan.md` and `.agent/authored/f285-r3-selfuse.py` := records.diff,
  plan.md and selfuse.py. All by `shutil.copyfile`.
  Subject: `F285 R3 C1: copy round 3 block and payloads into .agent/authored/`
  Expected insertions: 296 (this block's 170 lines plus 126 for the three payloads). Report the number you measure and STOP rather than commit if any
  commit of this round would reach 500 insertions.

C2 — THE BOOKING, in this order:
   1. `git apply` records.diff
   2. rewrite `.agent/plan.md` := plan.md
  Subject: `F285 R3 C2: book F285 R2 with the resolution of R-1055`
  Expected insertions by `git show --numstat`: 4 .agent/live_review.md, 10 .agent/plan.md.

C3 — THE SELF-USE ITEM (closure precondition 6): run
  `bash -c 'python3 .remedy-wt/f285-r3-payloads/selfuse.py 2>&1 | tee .remedy-wt/f285-r3-worker/selfuse.log; echo "REAL_EXIT=${PIPESTATUS[0]}"'`
  in the primary checkout, with a Bash timeout of 3600000 milliseconds: the run makes real
  provider calls, each allowed ten minutes, and may take most of an hour. It appends the
  generated item to `scripts/self_use_queue.json`, runs it with `max_tasks` 1 on the `self_use`
  role's configured provider, and writes `.agent/selfuse_f285/`. A job that ends blocked or
  stopped is an OUTCOME to record, never a reason to stop or to re-run; only a Python exception
  before the job exists is a STOP. Commit `scripts/self_use_queue.json` and
  `.agent/selfuse_f285/**`, and nothing else.
  Subject: `F285 R3 C3: generate and run the closure's self-use item, record its readings`

C4 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F285 R3 C4: rewrite handoff for round 3`
  Then `git push origin feature/f285-findings-paydown-v4`. Do NOT create a pull request.
  Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's whole tracked path set is: the `.agent/authored/f285-r3-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `scripts/self_use_queue.json`,
   `.agent/selfuse_f285/**` and `.agent/handoff.md`. Report the list you measure with
   `git diff --name-only 0fc0d8d0 HEAD` after C4. No `consumed_by` is set this round: the
   closure commit sets it.
4. The self-use job is NEVER applied: no `remedy job apply`, no `--approve`, no copying of its
   files into the checkout. It may leave a `remedy/job-*` branch, a worktree or an evidence
   directory behind; report each, and delete nothing you did not create as scratch.
5. If a gate other than the self-use outcome goes red, STOP, commit and push what is verified,
   write an honest handoff under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push.
7. DO NOT run the full suite: it runs once, in a later round of this closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C4 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f285-r3-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f285-r3/block.md`), read back with
 `git show <C1>:<path>`. Report one reading per copy.

G2 THE BOOKING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its builder printed from its dry tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 315159 | 60ce388e3f800369481eff65360cd9ae896dc56057f75f6a3eedb5e1dc047aae |
 | .agent/plan.md | 1080 | 2402f472e5956ee2702f17bcfe79a921ef321fa86c90afec34a3be88bca89911 |
 Also the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT at C2: the reviewer read R-1008 and R-1064.

G3 THE UI BUILD AND THE TESTS, in the primary checkout at C3: first
 `bash -c 'npm --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'`
 (a failing build is a STOP) and `git status --porcelain`, which must still be empty; then,
 SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/docs tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_self_use_findings.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection in its dry tree with the generated item appended as C3
 appends it and read `531 passed` at real exit code 0, the `-rs` summary printing none.
 Then `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass`
 at `fail_count` 0.

G4 THE SELF-USE READINGS — the whole output of C3's command and its real exit code; the item's
 id, title and provenance; the job's id and state; the builder and reviewer provider and model
 from `.agent/selfuse_f285/execution_config.txt`, which must name the `self_use` role's provider
 and never `fake`; the budgets and the budget actuals; every task's status, verdict and final
 status; `.agent/selfuse_f285/changed_paths.txt` and `.agent/selfuse_f285/run_defects.txt`
 verbatim; and `git worktree list` and `git branch --list 'remedy/job-*'` after the run.

G5 SIZES — `git show --numstat --format= <commit>` for C1, C2 and C3, each reported beside the
 expected insertions of its entry above where one is stated, and placed in the handback's
 `## Commits` table exactly as the tool printed it.

G6 TREE AND PUSH — after C4: `git status --porcelain`, which must be empty;
 `git log --oneline -n 5`, which must show C4, C3, C2, C1 and `0fc0d8d0` in that order; the
 push's real outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
 which must be EMPTY. These readings go in your reply, since C4 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the self-use readings, the
authored-text proofs, the item-status table AGENTS.md requires (one row per commit and per gate),
the deviations, and the next expected action. Report what you ran, not what you expected to find.
Your Session section reads SESSION 1 of feature F285, round 3, and says in one sentence how much
context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 3 and of the self-use run's diff, then the rest of the closure sequence. State the
open-findings count, 2, and the operator-questions count, 5.
