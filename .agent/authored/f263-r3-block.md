STEP F263 R3 — BOOK ROUND 2's FAIL AND R-1042, REPAIR IT, AND RUN ROUND 2's RED PROOFS

GOAL
Round 2 stopped at G4: the reviewer's test payload imports `job_evidence_dir` and never uses
it, and `ruff check .` also lints the byte-identical transport copy under `.agent/authored/`,
which is never edited. Book round 2's FAIL with finding R-1042 first, then repair it under
DECISION F263 D3 — the import dropped and `.agent/authored` excluded from ruff — then resolve
R-1042 and run the red proofs round 2 never reached, so T001 is proved whole.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f263-r3-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f263-r2-payloads/`  READ-ONLY. Round 2's originals; G5 runs its `mutations.py`.
  `.remedy-wt/f263-r3-worker/`    YOURS for logs and scripts. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `cd <dir> && git ...`, and multi-operation
one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace is refused: write such a
script to a file under your own directory and run the file.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f263-human-change-absorption`, and `git log --oneline -1` must read `0e2e04ef`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f263-r3-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f263-r3-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 4 | 3532 | bd46367a5804e6c3015751ab4d447c2c1de823bf03ab67bb06ab722b8f2005b7 |
| decisions.md | 24 | 1678 | 96e3bbe1fecc4c85db9663a660e54496ebe2059493c198a344d278d31c0c69b0 |
| plan.md | 31 | 1267 | f34e30268b9ef21938ea3fbe1ac8e1eeadf4571e8c01ae0ca8052a71d2f8cd67 |
| fix.diff | 28 | 1233 | 71ee2b03dfc836a924574d211e34887946577e38d68dc74319a106306b69a969 |
| done.md | 2 | 702 | 44acc80f3fec819179b73ac882b8ac9e02c4e8b3f02f5ded0f4e5196ae195da1 |
| ruff_probe.py | 34 | 1266 | 8510fec0a87a13351cf16667c600782ef727d463f110f645f921475135df11e7 |

`ledger.md`, `decisions.md` and `done.md` are APPENDS by byte concatenation: each begins with
the single newline that separates records, because `.agent/live_review.md` and
`.agent/decisions.md` each end in exactly one newline. `ledger.md` carries round 2's gate entry
and the registration of R-1042; `done.md` carries R-1042's resolution. `plan.md` is a REWRITE of
`.agent/plan.md`. `fix.diff` goes on with `git apply` and edits `pyproject.toml` and
`tests/orchestration/test_human_change_evidence.py`; the reviewer generated it from a tree at
`0e2e04ef` and applied it to a fresh worktree there, `git apply --check` and `git apply` at real
exit code 0. `ruff_probe.py` is a TOOL for G5: it is run, never applied to a tracked file.

BUNDLE — the commits are C1, C2, C3, C4 and C5, in this order.

C1 — copy this block and every payload
  `.agent/authored/f263-r3-block.md` := this block, and one `.agent/authored/f263-r3-<name>`
  for each payload, keeping each payload's own file name. All by `shutil.copyfile`.
  Subject: `F263 R3 C1: copy round 3 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 123. STOP rather than commit at 500 or more.

C2 — THE FINDING FIRST, with the booking and the decision, one commit: append ledger.md to
  `.agent/live_review.md`, append decisions.md to `.agent/decisions.md`, and rewrite
  `.agent/plan.md` := plan.md.
  Subject: `F263 R3 C2: book round 2's FAIL, register R-1042 and record DECISION F263 D3`
  Expected insertions by `git show --numstat`: 24 decisions.md, 4 live_review.md, 7 plan.md.

C3 — THE REPAIR: `git apply --check` then `git apply` fix.diff, `git add` both paths.
  Subject: `F263 R3 C3: drop the unused import and keep ruff out of .agent/authored (R-1042)`
  Expected insertions: 5 pyproject.toml, 0 test_human_change_evidence.py (one deletion).

C4 — THE RESOLUTION: append done.md to `.agent/live_review.md`.
  Subject: `F263 R3 C4: resolve R-1042`
  Expected insertions: 2.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`,
  WITH the item-status table AGENTS.md requires — one row per commit and per gate.
  Subject: `F263 R3 C5: rewrite handoff for round 3`
  Then `git push origin feature/f263-human-change-absorption` and report its real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Report the `git apply --check` exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1.
3. The round's whole tracked path set is: the `.agent/authored/f263-r3-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `pyproject.toml`,
   `tests/orchestration/test_human_change_evidence.py` and `.agent/handoff.md`. Report the
   list `git diff --name-only 0e2e04ef <C5>` gives. Never edit
   `.agent/authored/f263-r2-test_human_change_evidence.py` or any other landed copy.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no branch deletion, no
   force-push, no `git stash`, no checkout of another branch.
6. Leave `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-e7268925db3a4831`,
   `.remedy-wt/job-e7a145761bf04f86`, their branches and every existing stash alone. The
   worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards (finding R-0940).
7. DO NOT run the full suite (amend0917 rule 1); F263's one run belongs to its closure.
8. ORDER: C3, the repair, is committed strictly before C4, which appends R-1042's
   resolution; the resolution text relies on that order.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the PAYLOADS table;
 then each `.agent/authored/f263-r3-*` copy, read with `git show <C1>:<path>`, compared byte
 for byte with its source (the block copy against `.remedy-wt/f263-r3-block.md`). One reading
 per copy.

G2 THE RECORD — at C2 and at C4: each appended file equals its bytes at the commit before plus
 its payload's bytes, by strict concatenation, and `.agent/plan.md` equals plan.md; then the
 sha256 read with `git show <commit>:<path>` equals the reviewer's simulated reading:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 376984 | 6e4b7cfbe8c3ea3987f0ae83e0183a4f431975a526536ba0d62789359e94ab76 |
 | C2 | .agent/decisions.md | 1882987 | 3fcf90ccd7c3b4aa520ef2c46b7622c9c765e6f325df974fe8207d00e15d69f6 |
 | C2 | .agent/plan.md | 1267 | f34e30268b9ef21938ea3fbe1ac8e1eeadf4571e8c01ae0ca8052a71d2f8cd67 |
 | C4 | .agent/live_review.md | 377686 | e46479bcb35f5220c11b443d0e25d4616e9af6805fff5f116c0be4fe4a95455d |
 And the open set by distinct id with `open_finding_ids` from `scripts/rotate_live_review.py`
 at `0e2e04ef`, at C2 and at C4, naming whether R-1042 is in each (the reviewer read 28 without
 it, 29 with it, 28 without it).

G3 THE REPAIR BYTES — at C3, read with `git show <C3>:<path>`:
 | path | bytes | sha256 |
 |---|---|---|
 | pyproject.toml | 6130 | dc079475b049cbf42b9f7b2a83948b9b83145d8cca6f309f6d3887b637a6e0a9 |
 | tests/orchestration/test_human_change_evidence.py | 6862 | 9f4a779a87b0d88d0ec2e1a23053ca71f36caee6ecbd9b267a5efc8673cd1c86 |
 And `.agent/authored/f263-r2-test_human_change_evidence.py` at C4 still equals its bytes at
 `0e2e04ef`.

G4 THE TESTS AND THE LINT — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_human_change_evidence.py tests/orchestration/test_human_change.py tests/orchestration/test_toolchain_pins.py tests/orchestration/test_toolchain.py tests/orchestration/test_ci_budgets.py tests/orchestration/test_ci_workflow.py tests/test_ble001_ratchet.py tests/test_install_smoke.py tests/test_packaging_smoke.py tests/docs/ tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection WITHOUT the golden path, serially, in a disposable worktree
 carrying C2 to C4 and read `582 passed, 3 skipped` at real exit code 0; report what you read.
 Then `bash -c 'python3 -m ruff check .; echo "REAL_EXIT=$?"'` over the WHOLE repository from
 its root, which must read `All checks passed!` at exit 0 — this is the reading CI's `budgets`
 stage takes — and `python3 -m apps.cli.main integrity check --json`, all five checks `pass`
 at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f263-r3-mut <C4>`, then run, and
 report the whole output of, both tools:
 (a) `python3 -B .remedy-wt/f263-r2-payloads/mutations.py .remedy-wt/f263-r3-mut` — round 2's
 seven mutations, which never ran. The reviewer read, against its own tree carrying C2 to C4:
 control_before `43 passed` at exit 0; m1 2 failed, m2 2 failed, m3 2 failed, m4 1 failed,
 m5 2 failed, m6 1 failed, m7 1 failed, each at exit 1; control_after `43 passed` at exit 0;
 every `restored byte-identical` line `True`.
 (b) `python3 -B .remedy-wt/f263-r3-payloads/ruff_probe.py .remedy-wt/f263-r3-mut` — the red
 proof of DECISION F263 D3. The reviewer read: control_before `All checks passed!` at exit 0;
 m8, the `.agent/authored` entry removed, exit 1 with exactly one `F401`, in
 `.agent/authored/f263-r2-test_human_change_evidence.py`; restored byte-identical `True`;
 control_after `All checks passed!` at exit 0.
 Then `git worktree remove --force .remedy-wt/f263-r3-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5, in your reply: `git status --porcelain`, empty;
 `git log --oneline -n 6`, showing C5, C4, C3, C2, C1 and then `0e2e04ef`;
 `git worktree list`, the primary checkout and the three `.remedy-wt/job-*` worktrees only;
 the push's real outcome; and `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: the state block, the per-commit
changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the authored-text proofs, the ITEM-STATUS
TABLE, the deviations, and the next expected action. Your Session section reads SESSION 1 of
feature F263, round 3, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 3, then T002 — `remedy absorb`, the explicit command over the same `absorb` path.
State the open-findings count, 28, and the operator-questions count, 0.
