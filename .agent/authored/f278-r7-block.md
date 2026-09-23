STEP F278 R7 — BOOK ROUND 6, REGISTER AND REPAIR R-1036, MARK THE SECOND HANDLER GROUP

GOAL
Book round 6's PASS, register R-1036, R-1037 and R-1038 with DECISION F278 D6, repair
R-1036 — a final job review that fails to build or write is now recorded as a BLOCKING
review instead of vanishing — and mark every blind exception handler in twelve modules of
the job, pingpong, apply, command-line, runtime and snapshot areas with
`# noqa: BLE001 — <reason>`, three commits of comment text only.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHAT THE ROUND DOES, per DECISION F278 D6 in this round's `decisions.md` payload.
The findings are persisted FIRST, in the booking commit, before the repair. The R-1036
repair keeps the job complete, names the exception type in `job.metadata`, and writes
`final_job_review.json` with verdict `BLOCKED` and a `review_error` naming the type when
no review was written, so the final verifier's check reads it as blocked. The marking
diffs change the trailing comment of each `except` line and nothing else;
`.agent/authored/f278-r6-marking_check.py`, committed last round, proves that per commit.
The marking skips the R-1036 line. `pyproject.toml` is NOT touched this round.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f278-r7-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f278-r7-scratch/` and `.remedy-wt/f278-r7-research/`  The reviewer's; do not
      edit or delete them. Put your own logs under `.remedy-wt/f278-r7-worker/`. All are
      gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `cd <dir> && git ...`, and multi-operation
one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`).

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f278-durable-writes-loud-failures`, and `git log --oneline -1` must read
   `ead4ec77`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f278-r7-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f278-r7-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| decisions.md | 27 | 1941 | 26a2693c1b150868a76510e4bf53f6d819db13b8056d569f633454e3f28cf9ee |
| ledger.md | 8 | 5893 | fda2bcd6b9c062b1504d6e20e581dc9aaa5055d86e540b5cb498c19300e2ba6f |
| mark_cli.diff | 207 | 11291 | cdebe33083cbde71de4b21e58b16a272e346df38412fb73a40f374b9e51e5534 |
| mark_orchestration.diff | 392 | 20886 | b8df73d62aa9aead8bfdd2f87e46fcc38c736378312f754eaaa1e76242770bbc |
| mark_services.diff | 288 | 13312 | 5730c9d5307b243a42a512f187cc7c9bf0ffeff2a1232acd4dfb571319369716 |
| mutations.py | 46 | 1869 | df53847366d7721ab4f8bd24df0d4439cf56bdf431e2c4fb4031f0cb3a9937f0 |
| plan.md | 28 | 991 | 49badbd2eec9369931b36ed8e8659c0fe48787d6b5df9496501a973afd4a04e7 |
| r1036.diff | 61 | 3310 | 8e798b4d8cc16545bcb473ea1942aaa4985771bec9cb0216c1799cd71e91aa68 |

`ledger.md` is an APPEND of four paragraphs by byte concatenation — the round 6 `Gate:`
entry and the three registrations — beginning with the single newline that separates
records; `decisions.md` is an APPEND the same way. `plan.md` is a REWRITE of
`.agent/plan.md`. The `.diff` payloads go on with `git apply` in the order C3 to C6; the
reviewer generated each from the tree it applies to. `mutations.py` is a TOOL for G5.

BUNDLE — the commits are C1a, C1b, C1c, C2, C3, C4, C5, C6 and C7, in this order.

C1a — `.agent/authored/f278-r7-block.md` := this block, and one
  `.agent/authored/f278-r7-<name>` for each of decisions.md, ledger.md, plan.md and
  mutations.py.
  Subject: `F278 R7 C1a: copy round 7 block, bookkeeping payloads and tool`
  Its insertions are this block's line count plus 109. STOP rather than commit at 500 or more.
C1b — one `.agent/authored/f278-r7-<name>` for each of r1036.diff and
  mark_orchestration.diff.
  Subject: `F278 R7 C1b: copy round 7 repair and first marking diff into .agent/authored/`
  Expected insertions: 453.
C1c — one `.agent/authored/f278-r7-<name>` for each of mark_cli.diff and mark_services.diff.
  Subject: `F278 R7 C1c: copy round 7 remaining marking diffs into .agent/authored/`
  Expected insertions: 495.
  Every copy in C1a to C1c is made by `shutil.copyfile`, keeping the payload's file name.

C2 — THE BOOKING AND THE REGISTRATIONS, one commit: append ledger.md to
  `.agent/live_review.md`, append decisions.md to `.agent/decisions.md`, and rewrite
  `.agent/plan.md` := plan.md.
  Subject: `F278 R7 C2: book round 6's PASS and register R-1036, R-1037 and R-1038`
  Expected insertions: 45 (27 decisions, 8 live review, 10 plan).

C3 — `git apply --check` then `git apply` r1036.diff.
  Subject: `F278 R7 C3: record a lost final job review as a blocking one`
  Expected insertions: 40.
C4 — the same for mark_orchestration.diff.
  Subject: `F278 R7 C4: give each blind handler in the job, loop, provider and apply modules a reason`
  Expected insertions: 42.
C5 — the same for mark_cli.diff.
  Subject: `F278 R7 C5: give each blind handler in the job, worker and dev commands a reason`
  Expected insertions: 22.
C6 — the same for mark_services.diff.
  Subject: `F278 R7 C6: give each blind handler in the test, runtime, snapshot and hunk modules a reason`
  Expected insertions: 31.

C7 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`, WITH the item-status table AGENTS.md requires — one
  row per commit and per gate. Subject: `F278 R7 C7: rewrite handoff for round 7`
  Then `git push origin feature/f278-durable-writes-loud-failures` and report its outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Report every `git apply --check` exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's whole tracked path set is: the `.agent/authored/f278-r7-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, every path of the G3
   table, and `.agent/handoff.md`. Report the list `git diff --name-only ead4ec77 <C7>`
   gives. Nothing under `docs/`, no `pyproject.toml`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no branch deletion, no
   force-push, no `git stash`, no checkout of another branch.
6. Leave `.remedy-wt/job-129b3ad7206d4f8d`, its branch and every existing stash alone. The
   worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards (finding R-0940).
7. DO NOT run the full suite (amend0917 rule 1); F278's one run belongs to its closure.
8. Report each commit's insertion count in your handback's `## Commits` table as
   `git show --numstat` gives it, and the handback commit's own count in your reply.
9. The worker never writes a `Done:` paragraph (§4 item 4 of
   docs/agents/planner_reviewer_prompt.md); R-1036's resolution is the reviewer's to author.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C7 is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the PAYLOADS table;
 then each `.agent/authored/f278-r7-*` copy, read with `git show <commit>:<path>` from the
 commit that added it, compared byte for byte with its source (the block copy against
 `.remedy-wt/f278-r7-block.md`). One reading per copy.

G2 THE BOOKING — at C2: each appended file equals its `ead4ec77` bytes plus its payload's
 bytes, by strict concatenation, and `.agent/plan.md` equals plan.md; then the sha256 read
 with `git show <C2>:<path>` equals the reviewer's dry-run reading:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 444483 | 8a7327d7382565e768756b4770169c42b1d324b6e68f98e99afd7ab588a3b03a |
 | .agent/decisions.md | 1854051 | d470d8f512699c60dda07e8bf869860bfc4cae5718be3d56eb13c9a33e01a034 |
 | .agent/plan.md | 991 | 49badbd2eec9369931b36ed8e8659c0fe48787d6b5df9496501a973afd4a04e7 |
 And the open set by distinct id with `open_finding_ids` from `scripts/rotate_live_review.py`
 at `ead4ec77` and at C2, with both set differences: the reviewer read 26 then 29, ADDED
 exactly `R-1036`, `R-1037` and `R-1038`, REMOVED none.

G3 THE PRODUCT BYTES AND THE COMMENT-ONLY PROOF — at C6, the sha256 of each file read with
 `git show <C6>:<path>`:
 | path | bytes | sha256 |
 |---|---|---|
 | apps/cli/commands/dev.py | 8461 | 17e505e3c44a0fb6b067b3fb49a4a72882f064aefb8e2555556832116f71b5bb |
 | apps/cli/commands/job.py | 100510 | 4ca5059a3408cc2d93e11eb05dca7fab3f84eea86c945a47d660924e943d1b11 |
 | apps/cli/commands/worker_facade_cmd.py | 18213 | 7b3c88b4dd23b173b2e63842e0536084230f479e42cfbda31df60bebf0f7e318 |
 | packages/orchestration/hunk_ledger.py | 19338 | 5445af6538a9da0c9496cacfa9f3bcc1925f5dfc111afeb9b57db497d7872914 |
 | packages/orchestration/job_apply.py | 102494 | 281647f28aa1a1ca536dfbbc20819701124ef99ace80a2d88934f7b168d30562 |
 | packages/orchestration/pingpong_job.py | 194929 | cafb5e682a3ad0b414f963b852eec7fa1a6500c1f73313e27f49abd54f9432f7 |
 | packages/orchestration/pingpong_loop.py | 226278 | 3ffbcc5b841bce84effe94b499f9ce5a296c5bda8d3c0b2c27e1218ba517c22c |
 | packages/orchestration/pingpong_provider.py | 81843 | ff4790a9a8570fb612633527802c0b290ef5947230106d91cdafa2844815ea76 |
 | packages/orchestration/real_test_execution.py | 21141 | fb8313a5e6d5378ad084f02bf37115741d88cbf45cdbdb5d479e1d4c56a40503 |
 | packages/orchestration/repository_snapshot.py | 59530 | 1b418d1a659fdd8d42fb69ce5a09b1b8d52befc57e3a8f5af7bed57d5668b159 |
 | packages/orchestration/test_execution_service.py | 44075 | 1d9f25a888a6009957069e704c6fd4744241dc2127180b713c167351ee262012 |
 | packages/runtimes/runtime_supervisor.py | 25671 | 0701dba31bb7983d74aae404df1be1cb4a4fa06254afad6ee58e5c6c99ed8efc |
 | tests/orchestration/test_pingpong_integration.py | 8938 | 135f506f80309b0858e697adc85d1cf396efcf7734846740da6840c73ea3579d |
 Then `bash -c 'python3 .agent/authored/f278-r6-marking_check.py . <C4> <C5> <C6>; echo "REAL_EXIT=$?"'`,
 which must print `OK` for each with pairs 42, 22 and 31 and exit 0, and the same script over
 `<C3>` alone, the negative control, which must print `VIOLATION` and exit 1. Finally
 `python3 -m ruff check --select BLE001` over every Python path of the G3 table except the
 test file, `All checks passed!` at exit 0.

G4 THE TESTS — in the primary checkout at C6, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_hunk_ledger.py tests/orchestration/test_job_apply.py tests/orchestration/test_test_execution_service.py tests/orchestration/test_final_verifier.py tests/orchestration/test_repository_snapshot.py tests/orchestration/test_pingpong_integration.py tests/orchestration/test_real_test_execution.py tests/orchestration/test_pingpong.py tests/cli/test_worker_facade_cmd.py tests/cli/test_job_commands.py tests/runtimes/test_runtime_state_machine.py tests/orchestration/test_stream_evidence_integration.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection WITHOUT the golden path in a disposable worktree carrying
 C2 to C6 and read `685 passed, 1 skipped` at real exit code 0; report what you read. Then
 `python3 -m ruff check` over every path of the G3 table, real exit code 0, and
 `python3 -m apps.cli.main integrity check --json`, all five checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f278-r7-mut <C6>`, then
 `python3 .remedy-wt/f278-r7-payloads/mutations.py .remedy-wt/f278-r7-mut` and report its
 whole output. The reviewer read, over the same script against its own tree carrying C6:
 control_before `1 passed` at exit 0; m1 (the failure no longer named on the job) and m2 (no
 blocking record written) each `1 failed` at exit 1, at
 `TestRunJobFinalReviewFailure::test_a_review_that_cannot_be_built_blocks_the_apply`;
 control_after `1 passed` at exit 0, every restore byte-identical. Then
 `git worktree remove --force .remedy-wt/f278-r7-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C7, in your reply: `git status --porcelain`, empty;
 `git log --oneline -n 10`, showing C7 back to C1a and then `ead4ec77`; `git worktree list`,
 the primary checkout and `.remedy-wt/job-129b3ad7206d4f8d` only; the push's real outcome;
 and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: the state block, the per-commit
changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the ITEM-STATUS TABLE, the deviations,
and the next expected action. Your Session section reads SESSION 1 of feature F278,
round 7, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 7, then the last marking round — R-1037 and R-1038 repaired first, the third
handler group marked, BLE001 turned on with the ratchet test. State the open-findings
count, 29, and the operator-questions count, 0.
