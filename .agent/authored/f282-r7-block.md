STEP F282 R7 — BOOK ROUND 6 AND LAND T015 AND T016: R-0622's UI LINT GATE AND R-1029's BOOTSTRAP RULE

GOAL
Book round 6's PASS and the resolutions of R-1004 and R-1045, record DECISION F282 D7, and land
two slices: `apps/ui`'s lint gets `typescript-eslint` and its parser, its one real finding in
`RemedyShell.tsx` is repaired, and a pytest node makes the lint a gate (T015, R-0622); and both
session bootstraps read `.agent/decisions.md` by part, never whole (T016, R-1029).

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f282-r7-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f282-r7-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f282-r7-worker/`    YOURS for logs and scripts. All three are gitignored.

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
   `feature/f282-findings-paydown-v2`, and `git log --oneline -1` must read `2a8186c4`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f282-r7-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f282-r7-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.diff | 14 | 5777 | da29db6dada9ea34bb628bee6ff77e29f8f1bdcdcab3f60f799cd0bb3be5ce7b |
| decisions.diff | 36 | 2902 | 4ea8573a441fee31edab284e5af477878fac4bd2b9548f21a5a58616b270fbc3 |
| plan.md | 30 | 1160 | a6555da8391f79ebe0044a4424497ee353e729bf9dccfe09271f801a41beb98b |
| product.diff | 470 | 19327 | 8551204164261e501dddd0f7885fc5c1879c20ff58f9effe6d18cf82b6d14c80 |
| tests.diff | 122 | 5591 | 4bf7d1ad94eeb07fb9acd01c1edc26aeb7867cd12badcfa6f3db9fff46e872d9 |
| mutations.py | 68 | 3267 | 9f718884e97181d48ad0dabaab65a233b19f64490ad4bdcc82b68ab9ad914330 |

`plan.md` is a REWRITE of `.agent/plan.md`, copied whole. The `.diff` files go on with
`git apply`; the reviewer generated every one from a tree at `2a8186c4` and applied all of
them, in the commit order below, to a fresh worktree at `2a8186c4` with `git apply --check`
then `git apply`, every one at real exit code 0. `ledger.diff` appends three paragraphs to
`.agent/live_review.md` — the `Gate: F282 R6` entry and the `Done:` lines of R-1004 and
R-1045. `product.diff` edits `apps/ui/package.json`, `apps/ui/package-lock.json` (the
`npm install -D typescript-eslint@^8.70.1` the reviewer ran, 333 lines),
`apps/ui/eslint.config.js`, `apps/ui/src/components/shell/RemedyShell.tsx`,
`docs/agents/self_drive_protocol.md` and `docs/agents/planner_reviewer_prompt.md` (its §1
bootstrap, not the §3 checklist). `tests.diff` creates `tests/ui_contracts/test_ui_lint.py`
and `tests/docs/test_bootstrap_reads_decisions_by_part.py` and edits
`tests/ui_contracts/test_digest_mount.py`. `mutations.py` is a TOOL for G5: it is run, never
applied. AFTER C3 the lint needs the new package in `apps/ui/node_modules`: run
`npm ci --prefix apps/ui --no-audit --no-fund` in the primary checkout and report its exit
code; `node_modules` is gitignored and is the only untracked thing this writes.

BUNDLE — the commits are C1a, C1b, C1c, C2, C3, C4 and C5, in this order.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f282-r7-block.md` := this block, and one `.agent/authored/f282-r7-<name>`
  for each of ledger.diff, decisions.diff and plan.md, keeping each payload's own file name.
  All by `shutil.copyfile`.
  Subject: `F282 R7 C1a: copy round 7 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 80. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the product payload: `.agent/authored/f282-r7-product.diff`, by `shutil.copyfile`.
  Subject: `F282 R7 C1b: copy round 7 product payload into .agent/authored/`
  Expected insertions: 470.

C1c — copy the test payloads: `.agent/authored/f282-r7-tests.diff` and
  `.agent/authored/f282-r7-mutations.py`, by `shutil.copyfile`.
  Subject: `F282 R7 C1c: copy round 7 test payloads into .agent/authored/`
  Expected insertions: 190.

C2 — THE BOOKKEEPING, in this order:
   1. `git apply` ledger.diff     → `.agent/live_review.md`
   2. `git apply` decisions.diff  → `.agent/decisions.md`
   3. rewrite `.agent/plan.md` := plan.md
  Subject: `F282 R7 C2: book round 6, resolve R-1004 and R-1045 and record DECISION F282 D7`
  Expected insertions by `git show --numstat`: 28 decisions.md, 6 live_review.md, 9 plan.md.

C3 — THE PRODUCT: `git apply` product.diff.
  Subject: `F282 R7 C3: let the UI lint parse TypeScript, repair its finding, read decisions by part`
  Expected by `git show --numstat` (insertions/deletions): 12/1 eslint.config.js,
  333/0 package-lock.json, 1/0 package.json, 6/3 RemedyShell.tsx,
  3/1 planner_reviewer_prompt.md, 5/0 self_drive_protocol.md.

C4 — THE TESTS: `git apply` tests.diff, then `git add` the two new files.
  Subject: `F282 R7 C4: gate the UI lint and the bootstrap rule, R-0622 and R-1029`
  Expected (insertions/deletions): 32/0 test_bootstrap_reads_decisions_by_part.py,
  12/2 test_digest_mount.py, 46/0 test_ui_lint.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F282 R7 C5: rewrite handoff for round 7`
  Then `git push origin feature/f282-findings-paydown-v2` and report its real outcome. Do
  NOT create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f282-r7-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the six product-diff
   paths and the three test paths named above, and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only 2a8186c4 HEAD` after C5. Do NOT touch
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`,
   `.agent/context.md`, `README.md` or anything under `docs/roadmap/`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`, and no `npm install` beyond the `npm ci` ordered.
6. Leave `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-6a38b3203cca4928`,
   `.remedy-wt/job-e7268925db3a4831`, `.remedy-wt/job-e7a145761bf04f86`, the reviewer's
   `.remedy-wt/f282-r7-dry` and `.remedy-wt/f282-r7-sim`, their branches and every existing
   stash alone. The worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last
   action, and `git worktree list` is reported afterwards (finding R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run
   and F282's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f282-r7-*` copy byte for
 byte with its source (the block copy against `.remedy-wt/f282-r7-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKKEEPING AND THE PRODUCT — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named, equals the reviewer's reading, which its
 simulation printed from a tree it built by applying these payloads at `2a8186c4`:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 416714 | f3c06e2b382f2a4b7b70ddf6e6988391b718db7f40745bdb9792086af9b9505b |
 | C2 | .agent/decisions.md | 1926652 | c3940d43605b9a1bea462d4098efa64986127ad1feaaa273cc80c3f632aaf0d3 |
 | C2 | .agent/plan.md | 1160 | a6555da8391f79ebe0044a4424497ee353e729bf9dccfe09271f801a41beb98b |
 | C3 | apps/ui/package.json | 917 | 20dbc5b0133872799684a72122e5f851584cda4098f6b56d9eadb019d95d76f4 |
 | C3 | apps/ui/package-lock.json | 195480 | cd879535da0e509e7a629ff1fb5527ae088a1bc9e98ccbdcd4db27890b427da7 |
 | C3 | apps/ui/eslint.config.js | 1136 | 1046b9d03d48aa2f4c25671d9fded8032156ddf1238cafb20231431132849366 |
 | C3 | apps/ui/src/components/shell/RemedyShell.tsx | 11668 | 589f3a43ae2563e1a2a51c36ba7e653a116e794b040500e06f4651f17fb26615 |
 | C3 | docs/agents/self_drive_protocol.md | 33367 | ec1a1de785e2dc83c8266a5d821055e66bf1be4fd54399727084f2d08cac0770 |
 | C3 | docs/agents/planner_reviewer_prompt.md | 97059 | 1243bb5b434293cb1776f5c479927aab65704f6a58e0cb036bce0dd6ad02b6eb |
 | C4 | tests/ui_contracts/test_ui_lint.py | 2004 | 5fcbb12c0bf1939f4ffad94b21200b9f1a08c1056a6add0be9916cab419b5917 |
 | C4 | tests/ui_contracts/test_digest_mount.py | 20073 | 199df622fe67764ee7ac0cbe5f79785ab15fdc8f5b4495ef23471a36387c1af8 |
 | C4 | tests/docs/test_bootstrap_reads_decisions_by_part.py | 1285 | 543718b90e4819dda346da879490fb57a225fbad046735934cc00404bd1ac78f |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `2a8186c4` and at C2, with the set
 difference in both directions (the reviewer read 13 and 11, R-1004 and R-1045 leaving and
 none arriving); and `git diff --name-only` between consecutive commits from C1c to C4,
 which must name exactly the paths each commit lists.

G3 THE LINTER ON THIS BLOCK — at C4, in the primary checkout:
 `python3 -m apps.cli.main integrity block .remedy-wt/f282-r7-block.md`, real exit code 0,
 every item `[OK]`. Report the whole output.

G4 THE TESTS AND THE LINT — in the primary checkout at C4, after the `npm ci`, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/ui_contracts/ tests/ui_server/test_dashboard_contract.py tests/docs/ tests/test_agent_tooling.py tests/orchestration/test_block_lint.py tests/orchestration/test_integrity_gate.py tests/test_ble001_ratchet.py tests/orchestration/test_live_review_rotation.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/orchestration/test_roadmap_index.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside a disposable
 worktree carrying the round's edits and a fresh `npm ci`, and read `1386 passed, 6 skipped` at
 real exit code 0. Then `npm run --silent lint --prefix apps/ui`, real exit code 0 with no
 output; `npm run --silent typecheck --prefix apps/ui`, real exit code 0; `python3 -m ruff
 check` over the three test files, real exit code 0; and `python3 -m apps.cli.main integrity
 check --json`, all six checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f282-r7-mut <C4>`, then
 `npm ci --prefix .remedy-wt/f282-r7-mut/apps/ui --no-audit --no-fund` (report its exit code),
 then `python3 -B .remedy-wt/f282-r7-payloads/mutations.py .remedy-wt/f282-r7-mut` and report
 its whole output. The reviewer read, over the same script against a tree byte-identical to C4:
 control_before `30 passed` at exit 0;
 m1 (no TypeScript parser) 2 failed at exit 1;
 m2 (`no-undef` back on) 1 failed at exit 1;
 m3 (the write effect missing its port) 2 failed at exit 1;
 m5 (the port rebuilt every render) 1 failed at exit 1;
 m4 (Phase 0 reading decisions whole) 1 failed at exit 1;
 r1 (`eslint.config.js` at `2a8186c4`) 2 failed at exit 1;
 control_after `30 passed` at exit 0; every `restored byte-identical` line True. Then
 `git worktree remove --force .remedy-wt/f282-r7-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 8`, which must show C5, C4, C3, C2, C1c, C1b, C1a and `2a8186c4` in
 that order; `git worktree list`, which must show the primary checkout and exactly the
 worktrees constraint 6 names; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be
 EMPTY. These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F282, round 7, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 7, then T014 and T017 — R-0892 and R-0866. State the open-findings count, 11, and
the operator-questions count, 0.
