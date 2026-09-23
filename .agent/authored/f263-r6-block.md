STEP F263 R6 — BOOK ROUND 5 AND LAND T003's APPLY HALF: every apply absorbs first

GOAL
Book round 5's PASS and DECISION F263 D6, then land the apply half of T003: `apply_job` — and
with it `do run --apply` and every commit flag — absorbs a hand edit before a single file is
copied, the apply's drift block on the guard flag is deleted, and a hand edit to a file the job
also changed stops the apply with the path named as the human's. With it every slice of F263,
T001 to T003, has landed.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

THE OLD BEHAVIOUR IS SHOWN FIRST
G5's first probe puts `packages/orchestration/job_apply.py` back to its bytes at `5fd8b648` —
the apply that absorbs nothing and still refuses on the guard flag — and runs the new tests
against it; the reviewer read 5 of them fail. One existing test,
`TestDryRunTargetMutation` in `tests/orchestration/test_job_apply.py`, pinned the deleted block
and now pins that the flag alone refuses nothing (DECISION F263 D6 (4)).

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f263-r6-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f263-r6-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f263-r6-worker/`    YOURS for logs and scripts. All three are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `cd <dir> && git ...`, and multi-operation
one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace or a brace beside a quote is
refused: write such a script to a file under your own directory and run the file.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f263-human-change-absorption`, and `git log --oneline -1` must read `5fd8b648`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f263-r6-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f263-r6-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 2 | 1944 | 1df9f158819b1898f6ea4fa9cd416c273506011492c50b3b07c4874378c3fb23 |
| decisions.md | 34 | 2618 | 944dca0817ac5e479a0e9617c37dfdeb05b977761353b5c195e23199b8d27feb |
| plan.md | 30 | 1162 | aa2b56a82505783e5e542575fad30c40e9aeda653cfff3be4ff0657951330f23 |
| mutations.py | 80 | 3086 | e16365ecfc9f6f2e7fae77e97d8952775f6e9e45c2eedcd89888e6a35662ae2c |
| product.diff | 128 | 6349 | aa91bad6450bb5364ea06135857a7a49937b8e3b9679aaaca659307ead7ef435 |
| test_human_change_at_apply.py | 156 | 6714 | 968665d74ef7d81543a1c37a97cfa0ea69ff222a0f5b07c345b1f09388970731 |

`ledger.md` and `decisions.md` are APPENDS by byte concatenation: each begins with the single
newline that separates records, because `.agent/live_review.md` and `.agent/decisions.md` each
end in exactly one newline. `plan.md` is a REWRITE of `.agent/plan.md`.
`test_human_change_at_apply.py` is a NEW FILE at
`tests/orchestration/test_human_change_at_apply.py`, copied whole. `product.diff` edits
`packages/orchestration/job_apply.py`, `packages/orchestration/human_change.py` and
`tests/orchestration/test_job_apply.py` and goes on with `git apply`; the reviewer generated it
from a tree at `5fd8b648` and applied it to a fresh worktree there, `git apply --check` and
`git apply` at real exit code 0. `mutations.py` is a TOOL for G5: it is run, never applied to a
tracked file.

BUNDLE — the commits are C1a, C1b, C2, C3 and C4, in this order.

C1a — copy this block and the bookkeeping payloads with the tool
  `.agent/authored/f263-r6-block.md` := this block, and one `.agent/authored/f263-r6-<name>`
  for each of ledger.md, decisions.md, plan.md and mutations.py. All by `shutil.copyfile`.
  Subject: `F263 R6 C1a: copy round 6 block, bookkeeping payloads and red-proof tool`
  Its insertions are this block's line count plus 146. STOP rather than commit at 500 or more.

C1b — copy the product payloads: product.diff and test_human_change_at_apply.py.
  Subject: `F263 R6 C1b: copy round 6 product payloads into .agent/authored/`
  Expected insertions: 284.

C2 — THE BOOKING, one commit: append ledger.md to `.agent/live_review.md`, append
  decisions.md to `.agent/decisions.md`, and rewrite `.agent/plan.md` := plan.md.
  Subject: `F263 R6 C2: book round 5's PASS and DECISION F263 D6`
  Expected insertions by `git show --numstat`: 34 decisions.md, 2 live_review.md, 10 plan.md.

C3 — THE APPLY HALF, one commit: `git apply --check` then `git apply` product.diff, copy
  test_human_change_at_apply.py to `tests/orchestration/test_human_change_at_apply.py`, and
  `git add` every path.
  Subject: `F263 R6 C3: absorb before every apply and name a hand edit the job also changed`
  Expected insertions: 15 human_change.py, 30 job_apply.py (4 deletions),
  156 test_human_change_at_apply.py, 6 test_job_apply.py (2 deletions).

C4 — THE HANDBACK, which is also this session's handoff
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`,
  WITH the item-status table AGENTS.md requires — one row per commit and per gate.
  Subject: `F263 R6 C4: rewrite handoff for round 6, the end of session 1`
  Then `git push origin feature/f263-human-change-absorption` and report its real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Report the `git apply --check` exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f263-r6-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the three paths
   product.diff edits, `tests/orchestration/test_human_change_at_apply.py` and
   `.agent/handoff.md`. Report the list `git diff --name-only 5fd8b648 <C4>` gives.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no branch deletion, no
   force-push, no `git stash`, no checkout of another branch.
6. Leave `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-e7268925db3a4831`,
   `.remedy-wt/job-e7a145761bf04f86`, their branches and every existing stash alone. The
   worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards (finding R-0940). Run no `remedy` job and no
   `job apply` in the primary checkout.
7. DO NOT run the full suite (amend0917 rule 1); F263's one run belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C4 is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the PAYLOADS table;
 then each `.agent/authored/f263-r6-*` copy, read with `git show <commit>:<path>` from the
 commit that added it, compared byte for byte with its source (the block copy against
 `.remedy-wt/f263-r6-block.md`). One reading per copy.

G2 THE BOOKING — at C2: each appended file equals its `5fd8b648` bytes plus its payload's
 bytes, by strict concatenation, and `.agent/plan.md` equals plan.md; then the sha256 read
 with `git show <C2>:<path>` equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 383889 | 3dac4145b65da0ca21f3a01ebd6076a2b160d0efceea5ad044035f2f310bff8a |
 | .agent/decisions.md | 1891617 | babb8bf798b0243eea3b1ceba616465881161a1dad1e17d0b5d36f6267e26e7f |
 | .agent/plan.md | 1162 | aa2b56a82505783e5e542575fad30c40e9aeda653cfff3be4ff0657951330f23 |
 And the open set by distinct id with `open_finding_ids` from `scripts/rotate_live_review.py`
 at `5fd8b648` and at C2, with both set differences (the reviewer read 28, 28, both empty).

G3 THE PRODUCT BYTES — at C3, read with `git show <C3>:<path>`:
 | path | bytes | sha256 |
 |---|---|---|
 | packages/orchestration/job_apply.py | 104131 | 4fc9af0b4437308fce72ce95882f64f950d56b678dc0fd8fafa9085060bfc1f5 |
 | packages/orchestration/human_change.py | 14217 | 887b418a9e0c7742746aa537933d1dcc45f6fcef0087398c6cc439a0cbc5d60b |
 | tests/orchestration/test_job_apply.py | 93177 | 03ed1c5eddcaefd9c0be31c80824e0076a3ca38fca737649dff44afca2261d9e |
 | tests/orchestration/test_human_change_at_apply.py | 6714 | 968665d74ef7d81543a1c37a97cfa0ea69ff222a0f5b07c345b1f09388970731 |

G4 THE TESTS AND THE LINT — in the primary checkout at C3, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_human_change_at_apply.py tests/orchestration/test_human_change_in_run.py tests/orchestration/test_human_change.py tests/orchestration/test_human_change_evidence.py tests/cli/test_absorb_cmd.py tests/orchestration/test_job_apply.py tests/orchestration/test_job_apply_consistency.py tests/orchestration/test_job_apply_history.py tests/orchestration/test_job_apply_commit.py tests/cli/test_do_sequence_cli.py tests/orchestration/test_job_worktree_handoff.py tests/orchestration/test_job_worktree_integrity.py tests/test_ble001_ratchet.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection WITHOUT the golden path, serially, in a disposable worktree
 carrying C2 and C3 and read `527 passed, 2 skipped` at real exit code 0; report what you
 read. Then `bash -c 'python3 -m ruff check .; echo "REAL_EXIT=$?"'` over the whole
 repository, which must read `All checks passed!` at exit 0, and
 `python3 -m apps.cli.main integrity check --json`, all five checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f263-r6-mut <C3>`, then
 `python3 -B .remedy-wt/f263-r6-payloads/mutations.py .remedy-wt/f263-r6-mut 5fd8b648` and
 report its whole output. It runs `tests/orchestration/test_human_change_at_apply.py` and
 `tests/orchestration/test_job_apply.py`. The reviewer read, against its own tree carrying C2
 and C3:
 control_before `94 passed` at exit 0;
 old_apply (job_apply.py at `5fd8b648`) 5 failed at exit 1 — the OLD behaviour;
 m1 (the apply absorbs nothing) 3 failed at exit 1;
 m2 (conflicts not named) 2 failed at exit 1;
 m3 (a failed absorption does not block) 1 failed at exit 1;
 m4 (the drift block back) 1 failed at exit 1;
 m5 (unverified records counted) 1 failed at exit 1;
 control_after `94 passed` at exit 0, with every `restored byte-identical` line `True`.
 Then `git worktree remove --force .remedy-wt/f263-r6-mut`, `git worktree prune`, and
 report `git worktree list`.

G6 TREE AND PUSH — after C4, in your reply: `git status --porcelain`, empty;
 `git log --oneline -n 6`, showing C4, C3, C2, C1b, C1a and then `5fd8b648`;
 `git worktree list`, the primary checkout and the three `.remedy-wt/job-*` worktrees only;
 the push's real outcome; and `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: the state block, the per-commit
changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the authored-text proofs, the ITEM-STATUS
TABLE, the deviations, and the next expected action. Your Session section reads SESSION 1 of
feature F263, round 6, rounds so far 6, and says in one sentence how much context you had left.
It also states that this round ends session 1 of F263.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the Open PR
Gate (no pull request is open for this branch), the review of round 6 by session 2's reviewer,
then the closure sequence's first round — the Built State in `docs/roadmap/features/T2_F263.md`,
the closure's self-use item, and the feature's one full-suite run. State the open-findings
count, 28, and the operator-questions count, 0.
