STEP F278 R4 — BOOK ROUND 3, END T002: THE RUNTIME GROUP AND THE INLINE WRITERS

GOAL
Book round 3's PASS and DECISION F278 D3, then end T002: delete `dev_server`'s
`atomic_write_bytes`, `atomic_write_text` and `_atomic_write` and move every caller —
`runtime_supervisor`, `apps/cli/commands/runtime_cmd.py` and one test — onto `durable_write`,
empty the guard's `STILL_TO_MIGRATE` set in the same commit, then move the two inline
temporary-file writers, `repository_snapshot.update_apply_record_state` and
`project_registry.save_project`, onto `durable_write`, each with a test class in its own file.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHAT CHANGES FOR A CALLER, per DECISION F278 D3 in this round's `decisions.md` payload.
Every site writes the same bytes at the same mode, 0o600. The supervisor's handshake write
and the command's stop-request write gain the `mkdir` the deleted helper used to perform.
A failed fsync of a runtime record now raises where the old helper suppressed it.
`update_apply_record_state` keeps its boolean; `save_project` keeps raising.
`tests/runtimes/test_runtime_state_machine.py`'s
`test_a_failed_atomic_write_leaves_no_temp_file` is NOT edited: it patches the global
`os.replace`, which `durable_write` calls, and its glob `.runtime.json.*.tmp` matches the
temporary name `durable_write` makes.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f278-r4-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f278-r4-scratch/`   The reviewer's scripts; do not edit or delete them. Put
      your own logs under `.remedy-wt/f278-r4-worker/`. All are gitignored.

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
   `ce53bd0c`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f278-r4-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f278-r4-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| decisions.md | 37 | 2639 | b4ec398d9779c0c14d231033c93b156f419fd3f09ded7504d5a6a65d78e1ee2c |
| dev.diff | 222 | 9394 | 9f046c613dbfa9ba7e3ba77768aea40ed3fd969e5c0619aad9d7bfc1719733a1 |
| ledger.md | 2 | 2554 | 853dfa7911672073de9d402472aa906ec3d759b070929b26639d4e458c58c165 |
| plan.md | 29 | 1070 | 1a4ebc33f20ebab4850918210d74d059a979f077284daa3daece359606a82c29 |
| reg.diff | 89 | 3425 | 0b91a513e93dec603865a35d948d5049f40faa59b90d32f44e86ec05e80f51bf |
| revert_probes.py | 51 | 1986 | 4380516d4eba13419c2112c1f872b5fa3d48c1e25299e1ed2d8c2eb39901a731 |
| snap.diff | 95 | 3997 | 6265e189a3c6faf7874d3fd2a64cdf5723091d61abb3d8896eacb2b9cff43492 |

`ledger.md` and `decisions.md` are APPENDS by byte concatenation, each beginning with the
single newline that separates records. `plan.md` is a REWRITE of `.agent/plan.md`. The
`.diff` payloads go on with `git apply` in the order C3, C4, C5; the reviewer generated each
from the tree it applies to. `revert_probes.py` is a TOOL for G5: it is run, never applied
to a tracked file.

BUNDLE — the commits are C1a, C1b, C2, C3, C4, C5 and C6, in this order.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f278-r4-block.md` := this block, and one `.agent/authored/f278-r4-<name>`
  for each of decisions.md, ledger.md and plan.md, keeping each payload's own file name.
  All by `shutil.copyfile`.
  Subject: `F278 R4 C1a: copy round 4 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 68. STOP rather than commit at 500 or more.

C1b — copy the product payloads
  One `.agent/authored/f278-r4-<name>` for each of dev.diff, snap.diff, reg.diff and
  revert_probes.py, by `shutil.copyfile`.
  Subject: `F278 R4 C1b: copy round 4 product payloads into .agent/authored/`
  Expected insertions: 457.

C2 — THE BOOKING, one commit: append ledger.md to `.agent/live_review.md`, append
  decisions.md to `.agent/decisions.md`, and rewrite `.agent/plan.md` := plan.md.
  Subject: `F278 R4 C2: book round 3's PASS and DECISION F278 D3`
  Expected insertions: 48 (37 decisions, 2 live review, 9 plan).

C3 — THE RUNTIME GROUP: `git apply --check` then `git apply` dev.diff.
  Subject: `F278 R4 C3: move the runtime records onto durable_write and empty the guard's set`
  Expected insertions: 21.

C4 — THE APPLY RECORD: `git apply --check` then `git apply` snap.diff.
  Subject: `F278 R4 C4: move the apply-record state update onto durable_write`
  Expected insertions: 44.

C5 — THE PROJECT REGISTRY: `git apply --check` then `git apply` reg.diff.
  Subject: `F278 R4 C5: move the project record onto durable_write`
  Expected insertions: 35.

C6 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`, WITH the item-status table AGENTS.md requires — one
  row per commit and per gate. Subject: `F278 R4 C6: rewrite handoff for round 4`
  Then `git push origin feature/f278-durable-writes-loud-failures` and report its outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Report every `git apply --check` exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's whole tracked path set is: the `.agent/authored/f278-r4-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/runtimes/dev_server.py`, `packages/runtimes/runtime_supervisor.py`,
   `apps/cli/commands/runtime_cmd.py`, `packages/orchestration/repository_snapshot.py`,
   `packages/orchestration/project_registry.py`,
   `tests/orchestration/test_durable_write_guard.py`,
   `tests/runtimes/test_supervisor_portability.py`,
   `tests/orchestration/test_repository_snapshot.py`, `tests/test_project_registry.py` and
   `.agent/handoff.md`. Report the list `git diff --name-only ce53bd0c <C6>` gives.
   Nothing under `docs/`, no other module.
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
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C6 is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the PAYLOADS table;
 then each `.agent/authored/f278-r4-*` copy, read with `git show <commit>:<path>` from the
 commit that added it, compared byte for byte with its source (the block copy against
 `.remedy-wt/f278-r4-block.md`). One reading per copy.

G2 THE BOOKING — at C2: each appended file equals its `ce53bd0c` bytes plus its payload's
 bytes, by strict concatenation, and `.agent/plan.md` equals plan.md; then the sha256 read
 with `git show <C2>:<path>` equals the reviewer's dry-run reading:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 433010 | 11dee21ae698fb999218dca428ba694efaa8d8b9500a9b354743a00a7b209c9e |
 | .agent/decisions.md | 1847094 | 261feb3990ab5d221be23db2925aeceb7bf507f9de6a0b3f3fc83ad71cc3d2ac |
 | .agent/plan.md | 1070 | 1a4ebc33f20ebab4850918210d74d059a979f077284daa3daece359606a82c29 |
 And the open set by distinct id with `open_finding_ids` from `scripts/rotate_live_review.py`
 at `ce53bd0c` and at C2, with both set differences (the reviewer read 26, 26, both empty).

G3 THE PRODUCT BYTES — at C5, the sha256 of each file read with `git show <C5>:<path>`:
 | path | bytes | sha256 |
 |---|---|---|
 | apps/cli/commands/runtime_cmd.py | 40387 | b222d6c83d053c12f298d543ecd0771dcfd6d529ed33d4e347fe0843eda18298 |
 | packages/orchestration/project_registry.py | 31199 | bf7230c33583129d7854c482fd37a8c0cd334161b510109d6172665919225631 |
 | packages/orchestration/repository_snapshot.py | 59062 | a27604da7bb71f75c11e484970535be0a264037eabc476565a99fd3c00c72ea5 |
 | packages/runtimes/dev_server.py | 88155 | c0b6c65155c76d22992eab741856a6594cfded51135d8c043b9d7cde6698982d |
 | packages/runtimes/runtime_supervisor.py | 25280 | f37d1160a70036b27251614d078cc0df8e97c07efeeae1764a75bf38380f05eb |
 | tests/orchestration/test_durable_write_guard.py | 3145 | 3eca8ebc217dbaed4ec35f42b9a6266c2e9054a642a3dd4f4fd5a15d9ea39a93 |
 | tests/orchestration/test_repository_snapshot.py | 43121 | 54c047e1968dbd7066f376e10d6c58b7285e25bfedfb9585c530e201a011cd93 |
 | tests/runtimes/test_supervisor_portability.py | 106273 | 6fcaaad3f6867249ccf215d899f4579a15eb4ea3f8a5878982b1ac826acc9f9b |
 | tests/test_project_registry.py | 15351 | 9955bda0a7539475c750cb1f0d629a31216becf01ce5f7b48ed7b761606568f5 |

G4 THE TESTS — in the primary checkout at C5, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_durable_write_guard.py tests/runtimes/ tests/cli/test_runtime_cmd.py tests/orchestration/test_repository_snapshot.py tests/test_project_registry.py tests/orchestration/test_project_resolution.py tests/cli/test_project_current.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection WITHOUT the golden path in a disposable worktree carrying
 C2 to C5 and read `615 passed, 6 skipped` at real exit code 0 in about four minutes, most
 of it `tests/runtimes/`, which starts real processes; report what you read. Then
 `python3 -m ruff check` over every Python path of the G3 table, real exit code 0, and
 `python3 -m apps.cli.main integrity check --json`, all five checks `pass` at `fail_count` 0.

G5 THE REVERT PROBES — `git worktree add --detach .remedy-wt/f278-r4-probe <C5>`, then
 `python3 .remedy-wt/f278-r4-payloads/revert_probes.py .remedy-wt/f278-r4-probe ce53bd0c`
 and report its whole output. Each probe restores production files from `ce53bd0c` while
 the tests stay at C5. The reviewer read, over the same script against its own tree:
 control_before `117 passed` at exit 0;
 p1 (`dev_server.py` alone) and p2 (`dev_server.py`, `runtime_supervisor.py` and
   `runtime_cmd.py`) each `1 failed, 116 passed` at exit 1, the guard's
   `test_no_private_atomic_write_helper_outside_packages_common`;
 p3 (`repository_snapshot.py`) `2 failed, 115 passed` at exit 1, both tests of
   `TestApplyRecordStateIsDurable`;
 p4 (`project_registry.py`) `2 failed, 115 passed` at exit 1, both tests of
   `TestSaveIsDurable`;
 control_after `117 passed` at exit 0, with every `restored clean` line `True`.
 Then `git worktree remove --force .remedy-wt/f278-r4-probe`, `git worktree prune`, and
 report `git worktree list`.

G6 TREE AND PUSH — after C6, in your reply: `git status --porcelain`, empty;
 `git log --oneline -n 8`, showing C6 back to C1a and then `ce53bd0c`; `git worktree list`,
 the primary checkout and `.remedy-wt/job-129b3ad7206d4f8d` only; the push's real outcome;
 and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: the state block, the per-commit
changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the ITEM-STATUS TABLE, the deviations,
and the next expected action. Your Session section reads SESSION 1 of feature F278,
round 4, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 4, then T003 — BLE001 with a frozen ignore list, starting with the handlers in
`packages/orchestration/stream_evidence.py`. State the open-findings count, 26, and the
operator-questions count, 0.
