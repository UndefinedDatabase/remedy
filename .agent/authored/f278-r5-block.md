STEP F278 R5 — BOOK ROUND 4, T003's FIRST SLICE: THE STREAM ARTIFACT'S DEGRADATIONS

GOAL
Book round 4's PASS and DECISION F278 D4, then land T003's first slice in ONE product commit:
`packages/orchestration/stream_evidence.py`'s blind exception handlers are narrowed to the
exception each call expects or recorded as a degradation, and the stream artifact gains a
`degradations` field — in `StreamCaptureResult.to_dict` and as `stream_degraded` events in
`run_events.jsonl` — with a test class in `tests/orchestration/test_stream_evidence.py`.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHAT THE SLICE DOES, per DECISION F278 D4 in this round's `decisions.md` payload.
`_stop_process_tree` catches `OSError` for signalling or stopping a process that is already
gone and `subprocess.TimeoutExpired` for a wait, and nothing else. In `run_streamed_command`
a failed stderr drain, stdout close, process reap or stderr close is appended to the capture
as a degradation once the capture is done. In `capture_stream_evidence` a failing `on_cap`
callback is recorded and emitted as a `stream_degraded` event before the cap event, and that
one handler keeps `except Exception` with `# noqa: BLE001 — recorded as a degradation below`.
A degradation holds the step and the exception's TYPE, never its message. The existing
fields of the stream artifact are unchanged. `ruff check --select BLE001` over the module
reads zero after the slice, against 11 before it.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f278-r5-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f278-r5-scratch/`   The reviewer's scripts; do not edit or delete them. Put
      your own logs under `.remedy-wt/f278-r5-worker/`. All are gitignored.

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
   `924f7dd6`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f278-r5-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f278-r5-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| decisions.md | 36 | 2721 | d5eed1b068cccaa742bfdecd75b02e36cfe8e8fe794710eb0874cb4111d7d81f |
| ledger.md | 2 | 2939 | c294a5a762d10121437f05f38a3a00fc0f6471e8c0519dcf85c91c3601ba9dab |
| mutations.py | 56 | 2283 | 61611dcb1c0a56e235641a4b879b0bbf08a4a1572d5c011eb13dab93b04caa09 |
| plan.md | 29 | 1058 | 54e1accca56d2146515fe4e2bafdb716691a91fe58d47c6da52c77dff116f58b |
| stream.diff | 275 | 11131 | 18cb10da9c52baf22ef2de480f068aa527925eefdec5c4b3a0d1e76551f06cac |

`ledger.md` and `decisions.md` are APPENDS by byte concatenation, each beginning with the
single newline that separates records. `plan.md` is a REWRITE of `.agent/plan.md`.
`stream.diff` goes on with `git apply`; the reviewer generated it from the tree it applies
to. `mutations.py` is a TOOL for G5: it is run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C2, C3 and C4, in this order.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f278-r5-block.md` := this block, and one `.agent/authored/f278-r5-<name>`
  for each of decisions.md, ledger.md and plan.md, keeping each payload's own file name.
  All by `shutil.copyfile`.
  Subject: `F278 R5 C1a: copy round 5 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 67. STOP rather than commit at 500 or more.

C1b — copy the product payloads
  `.agent/authored/f278-r5-stream.diff` and `.agent/authored/f278-r5-mutations.py`, by
  `shutil.copyfile`.
  Subject: `F278 R5 C1b: copy round 5 product payloads into .agent/authored/`
  Expected insertions: 331.

C2 — THE BOOKING, one commit: append ledger.md to `.agent/live_review.md`, append
  decisions.md to `.agent/decisions.md`, and rewrite `.agent/plan.md` := plan.md.
  Subject: `F278 R5 C2: book round 4's PASS and DECISION F278 D4`
  Expected insertions: 49 (36 decisions, 2 live review, 11 plan).

C3 — THE SLICE: `git apply --check` then `git apply` stream.diff.
  Subject: `F278 R5 C3: record stream capture degradations and narrow its handlers`
  Expected insertions: 139 — 61 for `stream_evidence.py` and 78 for its test file.

C4 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`, WITH the item-status table AGENTS.md requires — one
  row per commit and per gate. Subject: `F278 R5 C4: rewrite handoff for round 5`
  Then `git push origin feature/f278-durable-writes-loud-failures` and report its outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Report the `git apply --check` exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's whole tracked path set is: the `.agent/authored/f278-r5-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/stream_evidence.py`,
   `tests/orchestration/test_stream_evidence.py` and `.agent/handoff.md`. Report the list
   `git diff --name-only 924f7dd6 <C4>` gives. `pyproject.toml` is NOT touched this round:
   BLE001 is enabled only in the commit that leaves no unmarked handler (DECISION F278 D4).
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

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C4 is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the PAYLOADS table;
 then each `.agent/authored/f278-r5-*` copy, read with `git show <commit>:<path>` from the
 commit that added it, compared byte for byte with its source (the block copy against
 `.remedy-wt/f278-r5-block.md`). One reading per copy.

G2 THE BOOKING — at C2: each appended file equals its `924f7dd6` bytes plus its payload's
 bytes, by strict concatenation, and `.agent/plan.md` equals plan.md; then the sha256 read
 with `git show <C2>:<path>` equals the reviewer's dry-run reading:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 435949 | 68313ce3e282ef331c07614bdde29bf4a2abb07483491bd17c4014b54b1ff1fa |
 | .agent/decisions.md | 1849815 | c77fde5f327391bf0aada4372f53172a7f07164cef3349369eff150892b99e1c |
 | .agent/plan.md | 1058 | 54e1accca56d2146515fe4e2bafdb716691a91fe58d47c6da52c77dff116f58b |
 And the open set by distinct id with `open_finding_ids` from `scripts/rotate_live_review.py`
 at `924f7dd6` and at C2, with both set differences (the reviewer read 26, 26, both empty).

G3 THE PRODUCT BYTES — at C3, the sha256 of each file read with `git show <C3>:<path>`:
 | path | bytes | sha256 |
 |---|---|---|
 | packages/orchestration/stream_evidence.py | 36246 | d284904286486579a191928993996a5c15dc004816dc46285e42c23ebf6eaca4 |
 | tests/orchestration/test_stream_evidence.py | 19788 | 98278280ec8842641cee78b6b1f4e27affd0c0d09de0544586a2f9eb46b3d4c2 |
 Then `bash -c 'python3 -m ruff check --select BLE001 packages/orchestration/stream_evidence.py; echo "REAL_EXIT=$?"'`
 at C3 must read `All checks passed!` at exit 0; at `924f7dd6` the same command read
 `Found 11 errors.`, which the reviewer measured.

G4 THE TESTS — in the primary checkout at C3, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_stream_evidence.py tests/orchestration/test_stream_evidence_integration.py tests/orchestration/test_stream_export_e2e.py tests/orchestration/test_event_names.py tests/orchestration/test_event_name_coupling.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection WITHOUT the golden path in a disposable worktree carrying
 C2 and C3 and read `236 passed, 1 skipped` at real exit code 0; report what you read. Then
 `python3 -m ruff check` over both paths of the G3 table, real exit code 0, and
 `python3 -m apps.cli.main integrity check --json`, all five checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f278-r5-mut <C3>`, then
 `python3 .remedy-wt/f278-r5-payloads/mutations.py .remedy-wt/f278-r5-mut` and report its
 whole output. The script asserts each FROM occurs exactly once, applies it, runs
 `TestDegradations`, restores the bytes, and runs an unmutated control first and last. The
 reviewer read, over the same script against its own tree carrying C3:
 control_before `4 passed` at exit 0;
 m1 (the on_cap failure not recorded) `1 failed, 3 passed` at exit 1, at
   `test_a_failing_cap_callback_is_recorded_in_the_result_and_the_events`;
 m2 (the stderr close failure not recorded) and m3 (the run's degradations never appended)
   each `1 failed, 3 passed` at exit 1, at
   `test_a_failing_stderr_close_reaches_the_run_artifact`;
 m4 (`to_dict` drops the field) `2 failed, 2 passed` at exit 1, at
   `test_a_clean_capture_records_no_degradation` and the on_cap test;
 control_after `4 passed` at exit 0, with every `restored byte-identical` line `True`.
 Then `git worktree remove --force .remedy-wt/f278-r5-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C4, in your reply: `git status --porcelain`, empty;
 `git log --oneline -n 6`, showing C4 back to C1a and then `924f7dd6`; `git worktree list`,
 the primary checkout and `.remedy-wt/job-129b3ad7206d4f8d` only; the push's real outcome;
 and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: the state block, the per-commit
changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the ITEM-STATUS TABLE, the deviations,
and the next expected action. Your Session section reads SESSION 1 of feature F278,
round 5, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 5, then T003's marking rounds — the remaining blind handlers, module group by
module group, each narrowed or given a noqa reason, BLE001 enabled in the last one. State
the open-findings count, 26, and the operator-questions count, 0.
