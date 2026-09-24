STEP F282 R5 — BOOK ROUND 4 AND LAND T008 TO T011: R-0999, R-1015, R-1034 AND R-1000

GOAL
Book round 4's PASS and the resolutions of R-1007, R-1016, R-1027 and R-1035, record DECISION
F282 D5, and land four slices: an empty staged diff becomes the finding a failing review needs, so
the repair loop runs (T008, R-0999); the self-use generator walks past a ledger paragraph that
quotes the retired job-result word (T009, R-1015); `ui stop` is classified as the local state
change it makes (T010, R-1034); and closure precondition 7 names `RESERVED_NAMESPACES`, with a
test holding every entry to a tree nothing in production imports (T011, R-1000).

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f282-r5-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f282-r5-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f282-r5-worker/`    YOURS for logs and scripts. All three are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, `cd <dir> && git ...`, and
multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit
codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace is refused: write such a
script to a file under your own directory and run the file.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f282-findings-paydown-v2`, and `git log --oneline -1` must read `17caab1d`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f282-r5-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f282-r5-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.diff | 18 | 8583 | f197124a9623082e8ba3cf9a79ab24d46770b2a3f8e7a33a25ed83cb8d1b3f9c |
| decisions.diff | 34 | 2641 | 2d3ea3654b469af7927a0e94aed1a8f153d0f3977a88d5b38c4d83d07763bf18 |
| plan.md | 31 | 1236 | 0ef46b03008870aa4fa4202f1502d158ea9433bf3f7db0f0d24cff3acbf52f22 |
| product.diff | 91 | 5032 | 7b29cfef9896b977030bbffda0d4fb2c985cf170673fb9fbd15a5abfda022617 |
| tests.diff | 184 | 9241 | 359dc7ae90aea3bcc032190b8dd30ab03417e05e776ebce901b69f33d13250c7 |
| mutations.py | 76 | 3629 | 1d8c251a9e14e6a2d8fae5ed159a21878492182dd3ee0b9e387e10518314acf6 |

`plan.md` is a REWRITE of `.agent/plan.md`, copied whole. The `.diff` files go on with
`git apply`; the reviewer generated every one from a tree at `17caab1d` and applied all of
them, in the commit order below, to a fresh worktree at `17caab1d` with `git apply --check`
then `git apply`, every one at real exit code 0. `ledger.diff` appends five paragraphs to
`.agent/live_review.md` — the `Gate: F282 R4` entry and the `Done:` lines of R-1007, R-1016,
R-1027 and R-1035. `product.diff` edits `packages/orchestration/pingpong_loop.py`,
`packages/orchestration/self_use_generator.py`, `apps/cli/command_catalog.py` and
`docs/roadmap/STATUS_closure_protocol.md`. `tests.diff` edits
`tests/orchestration/test_repair_loop.py`, `tests/orchestration/test_self_use_generator.py`,
`tests/docs/test_retired_promote_word.py`, `tests/test_command_catalog.py` and
`tests/test_no_orphan_modules.py`. `mutations.py` is a TOOL for G5: it is run, never applied.
C3 alone leaves `tests/docs/test_retired_promote_word.py` red, because the generator's new
pattern lands before the guard's entry for it in C4; every gate runs at C4.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f282-r5-block.md` := this block, and one `.agent/authored/f282-r5-<name>`
  for each of ledger.diff, decisions.diff and plan.md, keeping each payload's own file name.
  All by `shutil.copyfile`.
  Subject: `F282 R5 C1a: copy round 5 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 83. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the product payloads
  `.agent/authored/f282-r5-<name>` for each of product.diff, tests.diff and mutations.py,
  by `shutil.copyfile`.
  Subject: `F282 R5 C1b: copy round 5 product payloads into .agent/authored/`
  Expected insertions: 351.

C2 — THE BOOKKEEPING, in this order:
   1. `git apply` ledger.diff     → `.agent/live_review.md`
   2. `git apply` decisions.diff  → `.agent/decisions.md`
   3. rewrite `.agent/plan.md` := plan.md
  Subject: `F282 R5 C2: book round 4, resolve four findings and record DECISION F282 D5`
  Expected insertions by `git show --numstat`: 26 decisions.md, 10 live_review.md, 9 plan.md.

C3 — THE PRODUCT: `git apply` product.diff.
  Subject: `F282 R5 C3: repair an empty-diff review, a retired-word copy, ui stop and precondition 7`
  Expected by `git show --numstat` (insertions/deletions): 2/1 command_catalog.py,
  3/1 STATUS_closure_protocol.md, 16/0 pingpong_loop.py, 9/1 self_use_generator.py.

C4 — THE TESTS: `git apply` tests.diff.
  Subject: `F282 R5 C4: test R-0999, R-1015, R-1034 and R-1000`
  Expected (insertions/deletions): 17/6 test_retired_promote_word.py, 35/0 test_repair_loop.py,
  18/0 test_self_use_generator.py, 9/0 test_command_catalog.py, 29/0 test_no_orphan_modules.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F282 R5 C5: rewrite handoff for round 5`
  Then `git push origin feature/f282-findings-paydown-v2` and report its real outcome. Do
  NOT create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f282-r5-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the four product-diff
   paths and the five test paths named above, and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only 17caab1d HEAD` after C5. Do NOT touch
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`,
   `.agent/context.md`, `README.md` or `scripts/self_use_queue.json`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`.
6. Leave `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-6a38b3203cca4928`,
   `.remedy-wt/job-e7268925db3a4831`, `.remedy-wt/job-e7a145761bf04f86`, the reviewer's
   `.remedy-wt/f282-r5-dry` and `.remedy-wt/f282-r5-sim`, their branches and every existing
   stash alone. The worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last
   action, and `git worktree list` is reported afterwards (finding R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run
   and F282's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f282-r5-*` copy byte for
 byte with its source (the block copy against `.remedy-wt/f282-r5-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKKEEPING AND THE PRODUCT — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named, equals the reviewer's reading, which its
 simulation printed from a tree it built by applying these payloads at `17caab1d`:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 406908 | 8bcc35e05d7fa844495e09be5effd8d3bef503c6b9770b10a1165ab7f1b36e09 |
 | C2 | .agent/decisions.md | 1922471 | 7c1304aca9b26cf6c0090949dda6de09a06fa9da9dc3898b2bb85a82ed20c99a |
 | C2 | .agent/plan.md | 1236 | 0ef46b03008870aa4fa4202f1502d158ea9433bf3f7db0f0d24cff3acbf52f22 |
 | C3 | packages/orchestration/pingpong_loop.py | 227966 | 5375865c2bec8b7f5ea3790c5921078031eafd8156a06619e60830c6c5ee9f86 |
 | C3 | packages/orchestration/self_use_generator.py | 19680 | 5273ac4e87a9f2a8dfc2dbdb9c6071c1f6a8b0e0ca9cd8acc0fb05ab6d825558 |
 | C3 | apps/cli/command_catalog.py | 111888 | ee21a3554b80ed6368d84476d3e17a69f14c224add1a7847bb28f379bfcf6387 |
 | C3 | docs/roadmap/STATUS_closure_protocol.md | 20388 | 24faddd3e1047acb9938e6c39bfb65438aca4601d5703916f2c104a6dc543995 |
 | C4 | tests/orchestration/test_repair_loop.py | 61773 | 2166dbacd0531595413294cd7de42dbf987d013add8de8c23c6137f84ce09164 |
 | C4 | tests/orchestration/test_self_use_generator.py | 26154 | 9293998570a987f964f30d7c085518883dac831591291d85bf57ba9d78c26c0d |
 | C4 | tests/docs/test_retired_promote_word.py | 16440 | 3b0fc8c0c5c3d7990a789a5d07390505202e2aa1a93846576980996c9c10e71e |
 | C4 | tests/test_command_catalog.py | 22917 | c5afe87917cff84041152bf56ede953e028d165435bc8b37e2a66da782f52881 |
 | C4 | tests/test_no_orphan_modules.py | 15936 | 365a75ca49a8fa1d18eafb252c23535ea876af8532c851608179c3537f84d2ba |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `17caab1d` and at C2, with the set
 difference in both directions (the reviewer read 21 and 17, R-1007, R-1016, R-1027 and
 R-1035 leaving and none arriving); and `git diff --name-only` between consecutive commits
 from C1b to C4, which must name exactly the paths each commit lists.

G3 THE LINTER ON THIS BLOCK — at C4, in the primary checkout:
 `python3 -m apps.cli.main integrity block .remedy-wt/f282-r5-block.md`, real exit code 0,
 every item `[OK]`. Report the whole output.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_repair_loop.py tests/orchestration/test_repair_loop_hardened.py tests/orchestration/test_pingpong.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_self_use_findings.py tests/test_command_catalog.py tests/cli/test_command_catalog.py tests/cli/test_json_contract.py tests/cli/test_json_envelope.py tests/ui_server/test_live_state.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/docs/ tests/orchestration/test_roadmap_index.py tests/orchestration/test_integrity_gate.py tests/test_ble001_ratchet.py tests/orchestration/test_live_review_rotation.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside a disposable
 worktree carrying the round's edits and read `1142 passed, 1 skipped` at real exit code 0; a
 skip may pass in the primary checkout. Then `python3 -m ruff check` over the three Python
 product files and the five test files, real exit code 0, and
 `python3 -m apps.cli.main integrity check --json`, all six checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f282-r5-mut <C4>`, then
 `python3 -B .remedy-wt/f282-r5-payloads/mutations.py .remedy-wt/f282-r5-mut` and report its
 whole output. The reviewer read, over the same script against a tree byte-identical to C4:
 control_before `231 passed` at exit 0;
 m1 (an empty diff giving no finding) 1 failed at exit 1;
 m2 (the generator copying a retired word) 1 failed at exit 1;
 m3 (the generator's pattern drifting from the guard's) 4 failed at exit 1;
 m4 (`ui.stop` read-only again) 1 failed at exit 1;
 m5 (a product tree added to `RESERVED_NAMESPACES`) 1 failed, 231 passed at exit 1;
 r1, r2 and r3 (`pingpong_loop.py`, `self_use_generator.py` and `command_catalog.py` each at
 `17caab1d`) 1, 3 and 1 failed, each at exit 1;
 control_after `231 passed` at exit 0; every `restored byte-identical` line True. Then
 `git worktree remove --force .remedy-wt/f282-r5-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `17caab1d` in that
 order; `git worktree list`, which must show the primary checkout and exactly the worktrees
 constraint 6 names; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be
 EMPTY. These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F282, round 5, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 5, then T012 and T013 — R-1004 and R-1045. State the open-findings count, 17, and
the operator-questions count, 0.
