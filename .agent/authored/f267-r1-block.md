STEP F267 R1 — CLAIM F267 AND LAND T002 AND T003: every list handler and the ten-second demo, proved

GOAL
Pull request 272 is merged; `main` is at `9f06c509` and F267 is the next unchecked line. Cut its
branch, claim it, re-head the live review record with F265's closing verdict, record DECISION
F267 D1, and land T002 and T003 as one new test file, `tests/cli/test_list_commands_everywhere.py`:
every list command the catalog derives refuses `--sort bogus` in its HANDLER, naming its valid
fields, and `remedy run list --since 3d --until 1d` finds exactly the run from two days ago.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

WHY THIS IS FIRST
T2_F267.md: T001, the wirings, landed in F273 (DECISION F273 D9), so T002 and T003 are all that
remain, and both are tests. DECISION F267 D1 (in claim.diff) fixes the set: the catalog's own
`_is_list_command`, 13 commands at `9f06c509`, none excluded. No production file changes.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f267-r1-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f267-r1-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f267-r1-worker/`    YOURS for logs and scripts; create it if absent. All three are
                                  gitignored.

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
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read `main`, and
   `git log --oneline -1` must read `9f06c509`. Report all three. Then
   `git checkout -b feature/f267-list-commands-v2-completion` and report the branch. Do NOT
   pull: the Open PR Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f267-r1-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f267-r1-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 131 | 12916 | cd8874f2e4661cfa0c21408d79b89a317a2c526e150f2763f752dc3827c99adb |
| context.md | 39 | 1820 | 884f577e6f16f42ead9a69d8ab0a2b7ab4a47c315bd0a072519ab4496970cfb1 |
| mutations.py | 59 | 2645 | 308498a53f4d3e2874e6e402342dda628db5a396d6f09241e82e2645346d67c9 |
| plan.md | 31 | 1036 | f953dc1eac281536142c677d03a19baf389f860e5828608731b410664b7024be |
| test_list_commands_everywhere.py | 164 | 7077 | e7e0677af6469ae62495dc844da95a8637b90ed6d1718607f093134eb9fa6e32 |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`.
`test_list_commands_everywhere.py` is a NEW FILE at `tests/cli/test_list_commands_everywhere.py`,
copied whole. `claim.diff` goes on with `git apply`; the reviewer generated it from a tree at
`9f06c509` and applied it, in the commit order below, to a fresh worktree at `9f06c509` with
`git apply --check` then `git apply`, both at real exit code 0. It edits `.agent/live_review.md`
(the re-head), `docs/roadmap/STATUS.md` (F267's line `[ ]` to `[~]`) and `.agent/decisions.md`
(DECISION F267 D1 appended). `mutations.py` is a TOOL for G5: it is run, never applied to a
tracked file.

BUNDLE — the commits are C1a, C1b, C2, C3 and C4, in this order.

C1a — copy this block and the state payloads
  `.agent/authored/f267-r1-block.md` := this block, and `.agent/authored/f267-r1-<name>` for
  each of plan.md, context.md and claim.diff. All by `shutil.copyfile`.
  Subject: `F267 R1 C1a: copy round 1 block and state payloads into .agent/authored/`
  Its insertions are this block's line count plus 201. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the mutation tool and the test payload
  `.agent/authored/f267-r1-<name>` for each of mutations.py and test_list_commands_everywhere.py.
  Subject: `F267 R1 C1b: copy round 1 mutation tool and test payload into .agent/authored/`
  Expected insertions: 223.

C2 — THE CLAIM AND ITS RECORDS, in this order:
   1. `git apply` claim.diff
   2. rewrite `.agent/plan.md` := plan.md
   3. rewrite `.agent/context.md` := context.md
  Subject: `F267 R1 C2: claim F267, re-head the live review record, record D1`
  Expected insertions by `git show --numstat`: 15 context.md, 38 decisions.md, 31 live_review.md, 17 plan.md, 1 STATUS.md.

C3 — THE TESTS: copy test_list_commands_everywhere.py to
  `tests/cli/test_list_commands_everywhere.py` and `git add` it.
  Subject: `F267 R1 C3: prove every list handler and the ten-second demo`
  Expected insertions: 164.

C4 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F267 R1 C4: rewrite handoff for round 1`
  Then `git push -u origin feature/f267-list-commands-v2-completion`. Do NOT create a pull
  request: the branch opens one at F267's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f267-r1-*` copies,
   `.agent/live_review.md`, `docs/roadmap/STATUS.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `.agent/context.md`, `tests/cli/test_list_commands_everywhere.py` and `.agent/handoff.md`.
   Report the list you measure with `git diff --name-only 9f06c509` over the range to C4. Do NOT
   touch `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`,
   `README.md`, `docs/roadmap/features/T2_F267.md` or any file under `apps/` or `packages/`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees, their branches, the reviewer's worktrees
   `.remedy-wt/f267-r1-dry` and `.remedy-wt/f267-r1-sim`, and every existing stash alone. The
   worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards (finding R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F267's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C4 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f267-r1-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f267-r1-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE CLAIM — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its simulation printed from a tree it built by applying these
 payloads at `9f06c509`:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 298850 | efac3d878218f508cc4839a3530768df3db611e03459fd2bd31c62939e1bc659 |
 | docs/roadmap/STATUS.md | 49391 | 3edb355e785edfcaa5f8f28d99a3ecc9156d1ee60389bb7bb0526e1baecf8088 |
 | .agent/decisions.md | 1973311 | 37396126bb4586394beb38842a81ff7ed62368ab23b6765ae5b68169cf5b31c1 |
 | .agent/plan.md | 1036 | f953dc1eac281536142c677d03a19baf389f860e5828608731b410664b7024be |
 | .agent/context.md | 1820 | 884f577e6f16f42ead9a69d8ab0a2b7ab4a47c315bd0a072519ab4496970cfb1 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `9f06c509` and at C2, with the set
 difference in both directions (the reviewer read 4 at both — R-0499, R-0950, R-1008 and
 R-1046 — and both differences empty); F267's STATUS line at C2 read back in full, which must
 read `- [~] F267 — List commands v2 completion — sort/filter/limit for the remaining nine commands`;
 and `git diff --name-only <C1b> <C2>`, which must name exactly `.agent/context.md`,
 `.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md` and `docs/roadmap/STATUS.md`.

G3 THE TESTS ON DISK — at C3, `tests/cli/test_list_commands_everywhere.py` read with
 `git show <C3>:<path>` is 7077 bytes with sha256
 `e7e0677af6469ae62495dc844da95a8637b90ed6d1718607f093134eb9fa6e32`, and
 `git diff --name-only <C2> <C3>` names that one path and nothing else.

G4 THE SELECTION — in the primary checkout at C3, SERIALLY, with real exit codes:
```
bash .remedy-wt/f267-r1-scratch/g4.sh /home/decodeux/Repos/remedy
```
 The script runs one pytest selection (the new file, the catalog and list-option tests, the
 existing per-command list tests, `tests/docs/`, the roadmap index, the state-file readers,
 the ledger and block-lint tests and `tests/cli/test_golden_path.py`), then `ruff check` over
 the new file, then `python3 -m apps.cli.main integrity check --json`, each followed by its real
 exit code. The reviewer ran the same script inside its sim worktree carrying C1a (without the
 block copy), C1b, C2 and C3 and read `1026 passed, 3 skipped` at pytest exit 0, ruff at exit 0,
 and all six integrity checks `pass` at `fail_count` 0 with `handlers=150`. The primary checkout
 carries the UI toolchain a worktree lacks, so a skip may pass there, and your tree carries the
 block copy the sim lacked, which a test parametrized over the saved blocks may count once more.
 Report the three readings you get: the pytest summary line and exit code, ruff's exit code, and
 whether all six integrity checks read `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f267-r1-mut <C3>`, then
 `python3 -B .remedy-wt/f267-r1-payloads/mutations.py .remedy-wt/f267-r1-mut` and report its
 whole output. The script asserts each FROM occurs exactly once, applies it, runs
 `tests/cli/test_list_commands_everywhere.py` under `python3 -B`, restores the bytes, and runs
 an unmutated control first and last. The reviewer read, over the same script against its sim
 tree at C3:
 control_before `44 passed` at exit 0;
 m1 (`change list` passes no sort) 2 failed at exit 1;
 m2 (`decision list` passes no sort) 2 failed at exit 1;
 m3 (`mission list` passes no sort) 2 failed at exit 1;
 m4 (`config list` passes no sort) 2 failed at exit 1;
 m5 (`run list` has no date) 2 failed at exit 1;
 m6 (a relative bound points forward in time) 2 failed at exit 1;
 control_after `44 passed` at exit 0; every `restored byte-identical` line True.
 Then `git worktree remove --force .remedy-wt/f267-r1-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C4: `git status --porcelain`, which must be empty;
 `git log --oneline -n 6`, which must show C4, C3, C2, C1b, C1a and `9f06c509` in that order;
 `git worktree list`, which must show the primary checkout, the `.remedy-wt/job-*` worktrees and
 the reviewer's worktrees constraint 6 names, and nothing else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C4 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F267, round 1, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 1, then the closure sequence's first half — the Built State, the checklist consolidation,
the self-use track and the one full suite. State the open-findings count, 4, and the
operator-questions count, 1.
