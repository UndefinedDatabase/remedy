STEP F278 R6 — BOOK ROUND 5, FAIL THE SECRET DETECTOR CLOSED, MARK THE FIRST HANDLER GROUP

GOAL
Book round 5's PASS and DECISION F278 D5; make `run_manifest._contains_secret` answer True
when the redactor it reuses raises, with a test; then mark every blind exception handler in
`packages/orchestration/job_evidence.py`, `packages/orchestration/run_manifest.py` and
`scripts/build_review_manifest.py` with `# noqa: BLE001 — <reason>`, one file per commit,
changing comment text only.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHAT THE ROUND DOES, per DECISION F278 D5 in this round's `decisions.md` payload.
`_contains_secret` answered False on any exception, so a detector that could not run cleared
the value; every caller refuses or flags a value when the answer is True, so it now answers
True. The marking diffs change the trailing comment of each `except` line and nothing else;
`marking_check.py` proves that per commit. Two lines of `scripts/build_review_manifest.py`
keep their `# pragma: no cover` after the noqa. `pyproject.toml` is NOT touched: BLE001 is
enabled only in the commit that leaves no unmarked handler (DECISION F278 D4).

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f278-r6-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f278-r6-scratch/` and `.remedy-wt/f278-r6-research/`  The reviewer's; do not
      edit or delete them. Put your own logs under `.remedy-wt/f278-r6-worker/`. All are
      gitignored. Another agent may be reading under `.remedy-wt/f278-r7-research/`; ignore it.

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
   `4353fb9e`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f278-r6-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f278-r6-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| decisions.md | 32 | 2295 | 29e71118edfd3d21a9d70023a5205de0936f7acab0e5b560f7ae7f1af7e92826 |
| failclosed.diff | 41 | 1871 | 0fcbe162f88193782f36cb1f10ca776527af2b6d7a6bc7a82775cd54e60ad417 |
| ledger.md | 2 | 2641 | 4714de121db7120a79d9e73eec1344766bd13728dd8eb175b93adca991326e23 |
| mark_build_review_manifest.diff | 239 | 13801 | aaa19215976be90ae40f90a33b6502ef16bbcce11b49b2a3f64d3a4fa6de8769 |
| mark_job_evidence.diff | 260 | 14308 | 0b3d1393799880646443ec4ce7f9bb63a1ce25cbbdb16f29946a90298dae2ebb |
| mark_run_manifest.diff | 199 | 11098 | 1a5e6a02a934a256ecec2fef5f0b240e94da329ad4a86821672c53f7b376c7ba |
| marking_check.py | 47 | 1875 | a08ff5c29e21f69d41207d079b5c0e342a061cc180278e4b20a46d0db31d62d1 |
| mutations.py | 44 | 1811 | cc1472daed47ea2c371f4f0cc7c3c0b2341ed02820369b7bc9553d21393ccb1a |
| plan.md | 29 | 1096 | db40aced6129afd6dd2f8a330bc88eb1306df09d1b65b70dc3a2daac461a4944 |

`ledger.md` and `decisions.md` are APPENDS by byte concatenation, each beginning with the
single newline that separates records. `plan.md` is a REWRITE of `.agent/plan.md`. The
`.diff` payloads go on with `git apply` in the order C3 to C6; the reviewer generated each
from the tree it applies to. `marking_check.py` and `mutations.py` are TOOLS for G3 and G5:
they are run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C2, C3, C4, C5, C6 and C7, in this order. The
copies are three commits because together they exceed the 500-line cap.

C1a — `.agent/authored/f278-r6-block.md` := this block, and one
  `.agent/authored/f278-r6-<name>` for each of decisions.md, ledger.md and plan.md.
  Subject: `F278 R6 C1a: copy round 6 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 63. STOP rather than commit at 500 or more.
C1b — one `.agent/authored/f278-r6-<name>` for each of failclosed.diff,
  mark_job_evidence.diff, marking_check.py and mutations.py.
  Subject: `F278 R6 C1b: copy round 6 fail-closed payload, first marking diff and tools`
  Expected insertions: 392.
C1c — one `.agent/authored/f278-r6-<name>` for each of mark_run_manifest.diff and
  mark_build_review_manifest.diff.
  Subject: `F278 R6 C1c: copy round 6 remaining marking diffs into .agent/authored/`
  Expected insertions: 438.
  Every copy in C1a to C1c is made by `shutil.copyfile`, keeping the payload's file name.

C2 — THE BOOKING, one commit: append ledger.md to `.agent/live_review.md`, append
  decisions.md to `.agent/decisions.md`, and rewrite `.agent/plan.md` := plan.md.
  Subject: `F278 R6 C2: book round 5's PASS and DECISION F278 D5`
  Expected insertions: 44 (32 decisions, 2 live review, 10 plan).

C3 — `git apply --check` then `git apply` failclosed.diff.
  Subject: `F278 R6 C3: fail the manifest's secret detector closed when its redactor raises`
  Expected insertions: 20.
C4 — the same for mark_job_evidence.diff.
  Subject: `F278 R6 C4: give each blind handler in job_evidence a reason`
  Expected insertions: 29.
C5 — the same for mark_run_manifest.diff.
  Subject: `F278 R6 C5: give each blind handler in run_manifest a reason`
  Expected insertions: 22.
C6 — the same for mark_build_review_manifest.diff.
  Subject: `F278 R6 C6: give each blind handler in the review manifest builder a reason`
  Expected insertions: 27.

C7 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`, WITH the item-status table AGENTS.md requires — one
  row per commit and per gate. Subject: `F278 R6 C7: rewrite handoff for round 6`
  Then `git push origin feature/f278-durable-writes-loud-failures` and report its outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Report every `git apply --check` exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's whole tracked path set is: the `.agent/authored/f278-r6-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/run_manifest.py`, `packages/orchestration/job_evidence.py`,
   `scripts/build_review_manifest.py`, `tests/orchestration/test_run_manifest_security.py`
   and `.agent/handoff.md`. Report the list `git diff --name-only 4353fb9e <C7>` gives.
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
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C7 is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the PAYLOADS table;
 then each `.agent/authored/f278-r6-*` copy, read with `git show <commit>:<path>` from the
 commit that added it, compared byte for byte with its source (the block copy against
 `.remedy-wt/f278-r6-block.md`). One reading per copy.

G2 THE BOOKING — at C2: each appended file equals its `4353fb9e` bytes plus its payload's
 bytes, by strict concatenation, and `.agent/plan.md` equals plan.md; then the sha256 read
 with `git show <C2>:<path>` equals the reviewer's dry-run reading:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 438590 | 13baaf026006aea7a1f73f7bd57b49dc42a0b9879aeeab0f10fcd6778aedf588 |
 | .agent/decisions.md | 1852110 | b49d866c38d1d8a4b3aebadb1116cfbbb94eefd5be0ad1876499c476c943816b |
 | .agent/plan.md | 1096 | db40aced6129afd6dd2f8a330bc88eb1306df09d1b65b70dc3a2daac461a4944 |
 And the open set by distinct id with `open_finding_ids` from `scripts/rotate_live_review.py`
 at `4353fb9e` and at C2, with both set differences (the reviewer read 26, 26, both empty).

G3 THE PRODUCT BYTES AND THE COMMENT-ONLY PROOF — at C6, the sha256 of each file read with
 `git show <C6>:<path>`:
 | path | bytes | sha256 |
 |---|---|---|
 | packages/orchestration/job_evidence.py | 137163 | 5167debd2143cfd0e7f3b1db35211d54f422f493b2e448449aaba0db56640347 |
 | packages/orchestration/run_manifest.py | 338975 | 85ae5b97395af295bcfffec67d045263e1616c969834ddf9a2d6a70032bff284 |
 | scripts/build_review_manifest.py | 180325 | 59744d2e5801c60ce1aec0917cb6c2d1e5cb19ad2682b294832b30cc6c246b53 |
 | tests/orchestration/test_run_manifest_security.py | 8734 | 94c56e4208ce70642bf2b53ac7d8ff92bafffecf76db46b3fa504c53da365a5a |
 Then `bash -c 'python3 .remedy-wt/f278-r6-payloads/marking_check.py . <C4> <C5> <C6>; echo "REAL_EXIT=$?"'`,
 which must print `OK` for each commit with pairs 29, 22 and 27 and exit 0, and the same
 script over `<C3>` alone, the negative control, which must print `VIOLATION` and exit 1.
 Finally `bash -c 'python3 -m ruff check --select BLE001 packages/orchestration/job_evidence.py packages/orchestration/run_manifest.py scripts/build_review_manifest.py; echo "REAL_EXIT=$?"'`
 at C6, `All checks passed!` at exit 0.

G4 THE TESTS — in the primary checkout at C6, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_run_manifest_security.py tests/orchestration/test_run_manifest.py tests/orchestration/test_job_evidence.py tests/orchestration/test_review_zip_hygiene.py tests/orchestration/test_run_manifest_standard_json.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection WITHOUT the golden path in a disposable worktree carrying
 C2 to C6 and read `301 passed, 1 skipped` at real exit code 0; report what you read. Then
 `python3 -m ruff check` over every path of the G3 table, real exit code 0, and
 `python3 -m apps.cli.main integrity check --json`, all five checks `pass` at `fail_count` 0.

G5 THE RED PROOF — `git worktree add --detach .remedy-wt/f278-r6-mut <C6>`, then
 `python3 .remedy-wt/f278-r6-payloads/mutations.py .remedy-wt/f278-r6-mut` and report its
 whole output. The reviewer read, over the same script against its own tree carrying C6:
 control_before `2 passed` at exit 0; m1 (the detector answers False again) `1 failed,
 1 passed` at exit 1, at `test_a_failing_redactor_reports_a_secret`; control_after
 `2 passed` at exit 0, the restore byte-identical. Then
 `git worktree remove --force .remedy-wt/f278-r6-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C7, in your reply: `git status --porcelain`, empty;
 `git log --oneline -n 10`, showing C7 back to C1a and then `4353fb9e`; `git worktree list`,
 the primary checkout and `.remedy-wt/job-129b3ad7206d4f8d` only; the push's real outcome;
 and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: the state block, the per-commit
changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the ITEM-STATUS TABLE, the deviations,
and the next expected action. Your Session section reads SESSION 1 of feature F278,
round 6, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 6, then T003's next marking group — the job, pingpong, apply, runtime and snapshot
modules. State the open-findings count, 26, and the operator-questions count, 0.
