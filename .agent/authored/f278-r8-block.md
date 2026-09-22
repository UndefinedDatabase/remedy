STEP F278 R8 — BOOK ROUND 7, REPAIR R-1037 AND R-1038, MARK THE LAST GROUP, TURN BLE001 ON

GOAL
Book round 7's PASS, the reviewer's `Done: R-1036` and DECISION F278 D7; repair R-1037 (a
plan's budgets or fences that fail to validate now refuse the order) and R-1038 (the review
subject's metadata check no longer clears a value its scanners could not read); narrow one
handler; mark the last blind handlers under `apps/`, `scripts/` and `packages/` in
comment-only commits; then turn ruff's BLE001 on in `pyproject.toml` together with
`tests/test_ble001_ratchet.py`. After this round `ruff check .` over the whole tree reports
zero with BLE001 selected, and T003 is complete.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHAT THE ROUND DOES, per DECISION F278 D7 in this round's `decisions.md` payload.
R-1037: `do_sequence.order_job_limits` builds `JobBudgets` and `JobFences` and raises
`OrderJobPlanError` naming the set that failed, replacing two handlers that dropped it.
R-1038: `_metadata_is_safe` answers False when its scanners raise. The narrowing:
`hunk_decision_record._parsed_decision_stamp` catches `(TypeError, ValueError)`, the two
failures its docstring names. The marking commits change each `except` line's trailing
comment and nothing else; `.agent/authored/f278-r6-marking_check.py` proves that per commit.
The enablement adds `BLE001` to `select`, adds it to the `tests/**` per-file ignores, and adds
the ratchet test, whose `MAX_EXCUSED` is 290 — the count of `noqa: BLE001` marks under the
three roots at that commit, which the reviewer's dry run measured.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f278-r8-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f278-r8-scratch/` and `.remedy-wt/f278-r8-research/`  The reviewer's; do not
      edit or delete them. Put your own logs under `.remedy-wt/f278-r8-worker/`. All are
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
   `2537a4ae`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f278-r8-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f278-r8-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| decisions.md | 31 | 2261 | fae49fff323540126e45781d081224120273e52b9fcfe3b943d063f5d07551e2 |
| enable.diff | 84 | 3629 | 90f7166dd2d91293029c2b8ff635c60fb647c8003137c90e503aa9371e7fb56a |
| ledger.md | 4 | 3586 | 9c94305625794fe949d6ea48104a19a4b56cc9cc350c6a69c151bcafefe3f9ce |
| mark_commands.diff | 167 | 8437 | f067a30e1e7099a3b7c600a7c78b49938019fa26bce7ed1aa78d882451a11745 |
| mark_packages_a.diff | 220 | 11060 | 3eed28bb8f0cad3018f3be5aef04dbe0bd4daaffb8afc06850b305b2dc75e25f |
| mark_packages_b.diff | 499 | 25279 | bece573c3d1efa19e849500f00670d7c8177b0988413b87225d4b15a4209febf |
| mutations.py | 81 | 3212 | 3c3bd7b394e82931ce8a118fa234a7594dcaade4a274571d7e48384444ab5fee |
| narrow.diff | 13 | 499 | 872878b7e8cda77b8020515cd41dd0d9fd3d22e2b8d4861e68186820283bd220 |
| plan.md | 29 | 1083 | 5c12e2429342b5a333c78e59b5d26fe6a5127fde9b2eadf35e1cf30b7907da03 |
| r1037.diff | 104 | 4818 | cfd803253b8022dcf641853130a8a07bfea070383c0df301c95a89f02bc70fe1 |
| r1038.diff | 42 | 1834 | 549aa0488f6f8f6d136128c18a6e6b9ffcebf14306197d60002979ba7a81ef5d |

`ledger.md` is an APPEND of two paragraphs by byte concatenation — the round 7 `Gate:`
entry and the reviewer's `Done: R-1036` — beginning with the single newline that separates
records; `decisions.md` is an APPEND the same way. `plan.md` is a REWRITE of
`.agent/plan.md`. The `.diff` payloads go on with `git apply` in the order C3 to C9; the
reviewer generated each from the tree it applies to. `mutations.py` is a TOOL for G5.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C2, C3, C4, C5, C6, C7, C8, C9 and C10, in this
order. The copies are four commits because the payloads exceed the 500-line cap together.

C1a — `.agent/authored/f278-r8-block.md` := this block, and one
  `.agent/authored/f278-r8-<name>` for each of decisions.md, ledger.md, plan.md and
  mutations.py. Subject: `F278 R8 C1a: copy round 8 block, bookkeeping payloads and tool`
  Its insertions are this block's line count plus 145. STOP rather than commit at 500 or more.
C1b — one copy each of r1037.diff, r1038.diff, narrow.diff, mark_commands.diff and
  enable.diff. Subject: `F278 R8 C1b: copy round 8 repairs, narrowing, command marking and enablement`
  Expected insertions: 410.
C1c — mark_packages_a.diff. Subject: `F278 R8 C1c: copy round 8 first package marking diff`
  Expected insertions: 220.
C1d — mark_packages_b.diff. Subject: `F278 R8 C1d: copy round 8 second package marking diff`
  Expected insertions: 499.
  Every copy in C1a to C1d is made by `shutil.copyfile`, keeping the payload's file name,
  as `.agent/authored/f278-r8-<name>`.

C2 — THE BOOKING, one commit: append ledger.md to `.agent/live_review.md`, append
  decisions.md to `.agent/decisions.md`, and rewrite `.agent/plan.md` := plan.md.
  Subject: `F278 R8 C2: book round 7's PASS, resolve R-1036 and record DECISION F278 D7`
  Expected insertions: 46 (31 decisions, 4 live review, 11 plan).

C3 to C9 — for each diff in this order, `git apply --check` then `git apply`, one commit each:
  C3 r1037.diff — `F278 R8 C3: refuse an order whose budgets or fences do not validate` — 56
  C4 r1038.diff — `F278 R8 C4: keep a metadata value unsafe when its scanners raise` — 21
  C5 narrow.diff — `F278 R8 C5: narrow the decision stamp parser to the errors it names` — 1
  C6 mark_commands.diff — `F278 R8 C6: give each blind handler in the commands and scripts a reason` — 15
  C7 mark_packages_a.diff — `F278 R8 C7: give each blind handler in the first package group a reason` — 20
  C8 mark_packages_b.diff — `F278 R8 C8: give each blind handler in the second package group a reason` — 48
  C9 enable.diff — `F278 R8 C9: turn ruff BLE001 on with the excused-handler ratchet` — 58
  The number after each subject is the expected insertion count.

C10 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`, WITH the item-status table AGENTS.md requires — one
  row per commit and per gate. Subject: `F278 R8 C10: rewrite handoff for round 8`
  Then `git push origin feature/f278-durable-writes-loud-failures` and report its outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Report every `git apply --check` exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's whole tracked path set is: the `.agent/authored/f278-r8-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/handoff.md`, and
   the paths `git diff --name-only <C2> <C9>` lists, which the reviewer read as 47 paths —
   `pyproject.toml`, `tests/test_ble001_ratchet.py`, the two touched test files and 43
   modules under `apps/`, `scripts/` and `packages/`. Report both lists you measure.
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
9. The worker never writes a `Done:` paragraph; R-1037's and R-1038's resolutions are the
   reviewer's to author at the next gate.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C10 is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the PAYLOADS table;
 then each `.agent/authored/f278-r8-*` copy, read with `git show <commit>:<path>` from the
 commit that added it, compared byte for byte with its source (the block copy against
 `.remedy-wt/f278-r8-block.md`). One reading per copy.

G2 THE BOOKING — at C2: each appended file equals its `2537a4ae` bytes plus its payload's
 bytes, by strict concatenation, and `.agent/plan.md` equals plan.md; then the sha256 read
 with `git show <C2>:<path>` equals the reviewer's dry-run reading:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 448069 | 29d27d88adf8bb7271eb02caeeadc92d0e209d5a9cda69bd4a926486c22ef2c5 |
 | .agent/decisions.md | 1856312 | f45edd6f3c471733b1d374b563b5a03ca673d27fb34a75652bb2d09e708de0b2 |
 | .agent/plan.md | 1083 | 5c12e2429342b5a333c78e59b5d26fe6a5127fde9b2eadf35e1cf30b7907da03 |
 And the open set by distinct id with `open_finding_ids` from `scripts/rotate_live_review.py`
 at `2537a4ae` and at C2, with both set differences: the reviewer read 29 then 28, REMOVED
 exactly `R-1036`, ADDED none.

G3 THE PRODUCT BYTES AND THE COMMENT-ONLY PROOF — the sha256 of the bytes
 `git diff <C2> <C9>` prints must be
 `153ab6733619a7ca783c86e7c16f371c9a59326634534204199d31d783324e4c` over 55098 bytes, the
 reviewer's dry-run reading of the same range of trees. Then
 `bash -c 'python3 .agent/authored/f278-r6-marking_check.py . <C6> <C7> <C8>; echo "REAL_EXIT=$?"'`,
 which must print `OK` for each with pairs 15, 20 and 48 and exit 0, and the same script over
 `<C5>` alone, the negative control, which must print `VIOLATION` and exit 1. Finally, at C9,
 `bash -c 'python3 -m ruff check .; echo "REAL_EXIT=$?"'` over the WHOLE tree, which must read
 `All checks passed!` at exit 0 with BLE001 now selected.

G4 THE TESTS — in the primary checkout at C9, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/test_ble001_ratchet.py tests/orchestration/test_do_sequence.py tests/cli/test_do_sequence_cli.py tests/cli/test_plan_approval.py tests/orchestration/test_review_subject_strict_schema.py tests/orchestration/test_review_subject_resolution.py tests/orchestration/test_hunk_decision_record.py tests/orchestration/test_ci_budgets.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_job_plan.py tests/orchestration/test_orchestrator_loop.py tests/orchestration/test_worktree_resume_cli.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection WITHOUT the golden path in a disposable worktree carrying
 C2 to C9 and read `536 passed, 1 skipped` at real exit code 0; report what you read. Then
 `python3 -m apps.cli.main integrity check --json`, all five checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f278-r8-mut <C9>`, then
 `python3 .remedy-wt/f278-r8-payloads/mutations.py .remedy-wt/f278-r8-mut` and report its
 whole output. The reviewer read, over the same script against its own tree carrying C9:
 every `control_before` and `control_after` line at exit 0; m1 (budgets dropped again) and
 m2 (fences dropped again) each exit 1 on their own case of
 `test_a_limit_that_does_not_validate_refuses_the_order`; m3 (a scanner failure clears the
 value again) exit 1 on `test_a_scanner_that_raises_does_not_clear_the_value`; m4 (a reason
 removed) exit 1 on `test_every_excused_handler_states_a_reason`; m5 (a mark removed) exit
 1 on `test_the_count_of_excused_handlers_never_rises`; m6 (BLE001 deselected) exit 1 on
 `test_ble001_stays_selected`; every restore byte-identical. Then
 `git worktree remove --force .remedy-wt/f278-r8-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C10, in your reply: `git status --porcelain`, empty;
 `git log --oneline -n 14`, showing C10 back to C1a and then `2537a4ae`; `git worktree list`,
 the primary checkout and `.remedy-wt/job-129b3ad7206d4f8d` only; the push's real outcome;
 and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: the state block, the per-commit
changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the ITEM-STATUS TABLE, the deviations,
and the next expected action. Your Session section reads SESSION 1 of feature F278,
round 8, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 8 by the NEXT session — this session ends after it — and then F278's closure
sequence: the resolutions of R-1037 and R-1038, the Built State, the one checklist pass,
the self-use item, the one full suite, the evidence job and package, the rotation, the
accepted STATUS line and the pull request. State the open-findings count, 28, and the
operator-questions count, 0.
