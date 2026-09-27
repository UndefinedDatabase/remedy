STEP F288 R8 — THE CLOSURE SEQUENCE'S SECOND ROUND: book round 7, land SU-034's reviewed diff, finish the Built State, and run the one full suite

GOAL
Round 7 passed. Book its verdict, land the self-use job's reviewed one-line change to
`docs/guides/remedy-toml-user-guide.md`, add the self-use run to the Built State of
`docs/roadmap/features/T5_F288.md`, then build `apps/ui` and run the feature's one full suite
(operator amendment amend0917-throughput rule 1), committing its transcript as
`.agent/authored/f288-closure-suite.txt` together with the handback.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. Every change this round makes travels as a payload;
you write no code and no prose outside the handback and the suite transcript.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f288-r8-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f288-r8/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f288-r7-sim/`, `.remedy-wt/f288-r8-drafts/` and `.remedy-wt/f288-review/`
                                  The reviewer's; do not touch them.
  `.remedy-wt/f288-r8-worker/`    YOURS for scripts and the suite's log; create it if absent.
                                  Gitignored, so the log never enters the tracked tree while the
                                  suite runs (docs/agents/integration_gate.md step 2), as F289's
                                  closure suite ran.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution,
`cd <dir> && git ...`, and multi-operation one-liners chained with `;` or `&&` outside a
`bash -c`. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read
`${PIPESTATUS[0]}` when you pipe. Use `git -C <path>` rather than `cd`, and never `cd` your shell
into a worktree. Use `python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A
heredoc containing a dollar-brace or a backslash inside an f-string is refused or fails: write
such a script to a file under your own directory and run the file. Run npm ONLY as C5 (a) orders
it, and never npx. The `remedy` command is denied; use `python3 -m apps.cli.main` where a gate
names it.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f288-event-stream-completeness`, and `git log --oneline -1` must read `fdc274ff`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f288-r8/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f288-r8-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 28 | 949 | 6b48954eaa63b0766ae1b72101533526e000ba03819b119a46f08805602bbbed |
| records.diff | 10 | 9397 | 51046b3dc9bf05ed7a63958fcf337defc543ae2b829e6a5889ccfdd863537e09 |
| selfuse.diff | 12 | 615 | c58d7f302eecbbd724a37dcbc07fc0fe20da969293eadc85681c3c3395700028 |
| built_state.diff | 18 | 1196 | 3265724a56033c50d8277be14289b1712aeee8eeb4d0216be7ffe95445c4db9a |

`plan.md` is a REWRITE of `.agent/plan.md`. The three diffs go on with `git apply`, each on the
commit before it. `records.diff` appends round 7's gate entry to `.agent/live_review.md` after one
blank line. `selfuse.diff` is the self-use job's own change, exported by the reviewer with
`git diff 78e53297 5e4fabe3 -- docs/guides/remedy-toml-user-guide.md` from the job's branch
`remedy/job-8356faebdc904fd1`: one row added to the guide's CLI table. `built_state.diff` inserts
a paragraph on the closure's self-use run above the `**Findings.**` paragraph of the Built State.

BUNDLE — the commits are C1, C2, C3, C4 and C5, in this order.

C1 — copy this block and the payloads
  `.agent/authored/f288-r8-block.md` := this block, and `.agent/authored/f288-r8-plan.md`,
  `.agent/authored/f288-r8-records.diff`, `.agent/authored/f288-r8-selfuse.diff` and
  `.agent/authored/f288-r8-built_state.diff` := the four payloads, by `shutil.copyfile`.
  Subject: `F288 R8 C1: copy round 8 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 68. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C2 — THE BOOKKEEPING: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F288 R8 C2: book round 7`
  Expected by `git show --numstat` (insertions and deletions): 2/0 `.agent/live_review.md`,
  6/7 `.agent/plan.md`.

C3 — THE SELF-USE REPAIR: `git apply` selfuse.diff, nothing else.
  Subject: `F288 R8 C3: land SU-034's reviewed diff — the toml guide documents remedy config show`
  Its body names the job `8356faebdc904fd1` and its commit `5e4fabe3`.
  Expected by `git show --numstat`: 1/0 `docs/guides/remedy-toml-user-guide.md`.

C4 — THE BUILT STATE'S SELF-USE PARAGRAPH: `git apply` built_state.diff, nothing else.
  Subject: `F288 R8 C4: add the closure's self-use run to the Built State`
  Expected by `git show --numstat`: 7/0 `docs/roadmap/features/T5_F288.md`.

C5 — THE INTEGRATION GATE AND THE HANDBACK, in the PRIMARY checkout, after C4 and after G1 to G4:
  (a) `bash -c 'npm --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'`
  — a failing build is a STOP — then `git status --porcelain`, still empty. (b)
  `bash -c 'python3 -m pytest -n auto -q > .remedy-wt/f288-r8-worker/suite.txt 2>&1; echo "REAL_EXIT=$?"'`
  with a Bash timeout of 3600000 milliseconds, its wall time measured. Read the log with Python.
  Write `.agent/authored/f288-closure-suite.txt` in exactly this shape, one item per line:
  `Command: python3 -m pytest -n auto -q`, `Real exit code: <n>`, `Wall time: <measured>`,
  `Summary line: <pytest's last line>`, `Bad node ids (failed plus errors):` followed by one id
  per line, sorted, or the single word `NONE`, and `Tree it ran on: C4's SHA <full sha>`. (c)
  Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md` and commit it TOGETHER with
  the transcript. Subject: `F288 R8 C5: record the closure suite and rewrite handoff for round 8`.
  Then `git push`. No pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's whole tracked path set is: the `.agent/authored/f288-r8-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `docs/guides/remedy-toml-user-guide.md`,
   `docs/roadmap/features/T5_F288.md`, `.agent/authored/f288-closure-suite.txt` and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only fdc274ff` after C5.
   No edit to `packages/`, `apps/`, `tests/`, `scripts/`, `README.md`, `docs/roadmap/STATUS.md`,
   `.agent/decisions.md`, `.agent/candidates.md` or `.agent/operator_questions.md`.
4. If the suite is red, commit the transcript exactly as measured, report every bad node id, and
   hand back: the repair is the next round's (amend0917-throughput rule 2). Never weaken an
   assertion, delete a test, mark anything xfail or re-run the suite to get a different answer.
   If a gate other than the suite goes red, STOP, commit and push what is verified, and write an
   honest handoff under AGENTS.md "If Blocked".
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`. The branch `remedy/job-8356faebdc904fd1` stays.
6. Leave every existing worktree, branch and stash alone.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G4 run before C5.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f288-r8-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f288-r8/block.md`), read back with
 `git show <C1>:<path>`. Report one reading per copy.

G2 THE TREE — the byte count and sha256 of each file below, read with `git show <C4>:<path>`,
 equal the reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 324920 | 4d2ad0edf16e5c84c0a0ecac41a3b7cc26b173d03ec14156f5f88a42a36505a7 |
 | .agent/plan.md | 949 | 6b48954eaa63b0766ae1b72101533526e000ba03819b119a46f08805602bbbed |
 | docs/guides/remedy-toml-user-guide.md | 4026 | 4508603f179693f211c9b57d740f226121ba1817b233da940b8676fe4fdcecc4 |
 | docs/roadmap/features/T5_F288.md | 8678 | 7ef88f11f4432d0f8b823ea082676c6d62c75e22fe548b9503171f89594bd208 |
 Also: `git show <C3>:docs/guides/remedy-toml-user-guide.md` is byte-identical to
 `git show 5e4fabe3:docs/guides/remedy-toml-user-guide.md`, and `run_staleness_checks()` from
 `packages.orchestration.doc_staleness` in the primary checkout at C4 answers no claim, as the
 reviewer read in its simulation tree.

G3 THE TESTS, in the primary checkout at C4, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/docs tests/orchestration/test_doc_staleness.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/cli/test_config_cmd.py tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection in its simulation tree holding every edit of this round and
 read `578 passed` at real exit code 0, the `-rs` summary printing none. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks with status
 `pass` at `fail_count` 0 — the status of each check is the reading, not the exit code.

G4 SIZES — `git show --numstat --format= <commit>` for C1 to C4, each reported beside the
 expected insertions of its entry above where one is stated, and placed in the handback's
 `## Commits` table exactly as the tool printed it.

G5 THE SUITE — C5's (a) and (b) readings: the build's output and exit code, the transcript whole,
 and the wall time; the handback carries the transcript's summary line and its bad node ids.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 6`, which must show C5, C4, C3, C2, C1 and `fdc274ff` in that order; the
 push's real outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
 which must be EMPTY. These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
deviations, the next expected action, and — INSIDE `.agent/handoff.md` itself, as its own
section, not only in your reply — the item-status table AGENTS.md requires, one row per commit
and per gate. Round 7's handback carried that table only in the reply, which the ledger records.
Report what you ran, not what you expected to find. Your Session section reads SESSION 2 of
feature F288, round 8, rounds so far 8, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 8 and of the suite's transcript, then the evidence bundle and the review package. State the
open-findings count, 0, and the operator-questions count, 0.
