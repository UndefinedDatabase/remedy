STEP F265 R7 — THE CLOSING ROUND: BOOK ROUND 6, ROTATE THE LEDGER, ACCEPT F265 IN STATUS WITH ITS README PINS, OPEN THE PULL REQUEST

GOAL
Book round 6's PASS, rotate the finding ledger into its archive, flip F265's STATUS line to `[x]`
with the README's accepted count, Tier 5 Done cell and Tier 5 prose in the same commit, and open
the pull request into `main`. F265 registered one finding, R-1046, which F284 owns from its
registration, so there is no ownership step; F265 is not a findings-paydown feature, so it
registers nothing.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f265-r7-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f265-r7-scratch/`   READ-ONLY. The reviewer's simulation tools and logs.
  `.remedy-wt/f265-r7-worker/`    YOURS for logs, captures and scripts; create it if absent.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, `ln`, `npm ci`, `npm install`, process substitution,
`cd <dir> && git ...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`.
Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C <path>` rather than
`cd`. Put multi-step code in a scratch Python file under your directory. The `remedy` CLI may be
denied: run `python3 -m apps.cli.main ...`. Never use `git stash` in any form.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`: report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f265-teacher-learning-ui`, and `git log --oneline -1` must read `8b4a1071`.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f265-r7-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `gh pr list --state open --json number,headRefName` as found;
   the second must be EMPTY.

PAYLOADS — under `.remedy-wt/f265-r7-payloads/`, printed by the reviewer's simulation
(lines = newline count). Verify each BEFORE using it and report every reading.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.diff | 10 | 6890 | d98a651c14b9685e08f5a295161d220faef6a3b3f7aeb1559b12e19986ed1329 |
| plan.md | 28 | 967 | dc0ecf7e7ef8a0b3571fa6ff46a273306fcdf258dc2a35986427698ecc90fcb6 |
| closure.diff | 51 | 3051 | 0919457866e13d58e1b6fb7d8f1663870b3f3f5823e6b146208c9a647289cd89 |
| pr_body.md | 90 | 4802 | 24d6f08d1068a375a52b9a7b4a134e0519e6b2a144b6d9282849d3780a3f762b |
| status_line.txt | 1 | 414 | d03dbe76a263cd4e612613d0af164f562706f09488e0c8ee71c5f8594078b03e |

`ledger.diff` appends round 6's `Gate:` entry to `.agent/live_review.md`. `plan.md` is a REWRITE of
`.agent/plan.md`. `closure.diff` flips F265's STATUS line to `[x]` and moves the README's accepted
count, its Tier 5 Done cell and its Tier 5 prose. `pr_body.md` is the pull request's description,
passed to `gh` as a file. `status_line.txt` is the exact STATUS line `closure.diff` writes, used
only for G4's proof. The `.diff` files go on with `git apply --check` then `git apply`. Never retype
or edit a payload; copy with `shutil.copyfile`.

BUNDLE — commits C1 to C4 and then the pull request, in this order.

C1 — `.agent/authored/f265-r7-block.md` := this block; `.agent/authored/f265-r7-<name>` for each
  payload, keeping its file name. Byte for byte, with `shutil.copyfile`.
  Subject: `F265 R7 C1: copy round 7 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 180. Report the number you measure, and STOP
  rather than commit if it is 500 or more.

C2 — `git apply` ledger.diff → `.agent/live_review.md` · `.agent/plan.md` := plan.md.
  Subject: `F265 R7 C2: book round 6's PASS, the package READY_FOR_REVIEW`
  Expected by `git show --numstat` (insertions/deletions): 2/0 live_review.md, 6/6 plan.md.

C3 — THE ROTATION, its own commit, paths `.agent/live_review.md` and
  `.agent/live_review_archive.md` ONLY (operator amendment amend0905-throughput, AFTER the verdict
  booking and BEFORE the STATUS flip): `python3 scripts/rotate_live_review.py`. Report its printed
  output in full.
  Subject: `F265 R7 C3: rotate the finding ledger into its archive`
  Expected (insertions/deletions): 0/18 live_review.md, 18/0 live_review_archive.md.

C4 — THE CLOSURE COMMIT, exactly these paths and no others: `docs/roadmap/STATUS.md`, `README.md`
  and `.agent/handoff.md`. `git apply` closure.diff, run G4 and G5 on the working tree, then
  rewrite `.agent/handoff.md` per `docs/agents/handback_template.md` as the closure handback: it
  names the package, its SHA-256, its directory, the evidence job and the accepted head from
  round 6, and it does NOT name a pull request number, which does not exist when it is written.
  There is no `scripts/self_use_queue.json` edit: the closure's self-use track answered NONE
  (`.agent/selfuse_f265/result.txt`).
  Subject: `F265 R7 C4: accept F265 in STATUS with its README pins`
  Expected for the two applied files (insertions/deletions): 11/2 README.md, 1/1 STATUS.md.
  Then `git push origin feature/f265-teacher-learning-ui`.

THE PULL REQUEST — after C4 and its push:
  `gh pr create --base main --head feature/f265-teacher-learning-ui --title "F265 — Teacher learning UI v1 (post-task lessons)" --body-file .remedy-wt/f265-r7-payloads/pr_body.md`.
  DO NOT MERGE IT. Report the number and URL in your final reply only.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f265-r7-*` copies C1 makes,
   `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/roadmap/STATUS.md`, `README.md` and `.agent/handoff.md`. Report the set you measure with
   `git diff --name-only 8b4a1071 HEAD` after C4.
4. C4 is the LAST commit on this branch (Rule A4). Nothing follows it except, if the reviewer's
   closure gate asks for one, a commit whose path set is exactly `.agent/candidates.md` — which
   this block does not order and you never write on your own initiative.
5. If any gate goes red, STOP before C4: commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. A closure that cannot be proved is not closed.
6. NOTHING IS MERGED. No `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
7. Delete nothing you did not create: every `remedy/job-*` branch, every `.remedy-wt/job-*`
   worktree and the reviewer's worktrees whose names begin `.remedy-wt/f265-` stay.
8. DO NOT run the full suite: this feature's run is committed at
   `.agent/authored/f265-closure-suite.txt`.

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G5 run before C4 is written; G4 and G5
therefore read the working tree with closure.diff applied, before the handoff is written.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 committed `.agent/authored/f265-r7-*` blob, read with `git show <C1>:<path>`, compared byte for
 byte with its source (the block copy against `.remedy-wt/f265-r7-block.md`). One reading per
 file, all equal.

G2 THE BOOKING — at C2, read with `git show <C2>:<path>`: `.agent/live_review.md` 318474 bytes, sha256 `344464e724661fc7693f20397315d18f801fb022af46505457d5e770bdf3a847`; `.agent/plan.md` 967 bytes, sha256 `dc0ecf7e7ef8a0b3571fa6ff46a273306fcdf258dc2a35986427698ecc90fcb6`. Also: among the lines C2's diff
 ADDS, those beginning `Gate: F265 R6 — ` (1); and the open set by distinct id via
 `open_finding_ids` from `scripts/rotate_live_review.py` at `8b4a1071` and at C2 — the reviewer
 read 4 and 4, R-0499, R-0950, R-1008 and R-1046, both differences empty. Report yours beside
 each.

G3 THE ROTATION — at C3: the reviewer's simulation printed 9 gate records and 0 finding pairs
 moved, the ledger 318474 to 298665 bytes, the archive 4878549 to 4898358 bytes, open findings 4
 before and 4 after, and left `.agent/live_review.md` 298665 bytes, sha256 `4aa11c9ec382beb7e9ddf8d2f8c9182387c9b9c0debbaf25ce28345d06352fa6` and `.agent/live_review_archive.md` 4898358 bytes, sha256 `b67d44b80d5a4fdbecb6803e3a7b2f683fce7c1a9815c34881723fd749205476`. Report yours beside each, and C3's path set, which is the two
 ledger files and nothing else.

G4 THE CLOSURE EDITS — with closure.diff applied, before C4 is committed: `docs/roadmap/STATUS.md` 49391 bytes, sha256 `a277d911008aed268fdf929965e2d4bb126ef58b88eda9f524dbafb31c1d036e`, and `README.md` 26629 bytes, sha256 `e95a90c9e10791b0b4d67f9401065471137c09c0bea36007851fd5f4877e349c`; the count of
 lines of `docs/roadmap/STATUS.md` equal to the one line of status_line.txt, byte for byte, which
 must be 1; and, serially,
 `bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'`,
 which the reviewer's dry run over the same tree read as `437 passed, 1 skipped` at exit 0. The
 reviewer red-controlled the README pins there: with the accepted count left at 94, or the Tier 5
 Done cell left at 14, `tests/docs/` read `1 failed, 326 passed`, and with the STATUS line left
 `[~]` it read `3 failed, 324 passed`. Report yours beside each.

G5 THE TREE — with closure.diff applied, before C4: `python3 -m apps.cli.main integrity check
 --json`, all six checks `pass` at `fail_count` 0; and `python3 -m apps.cli.main integrity block
 .remedy-wt/f265-r7-block.md`, real exit code 0 with every item `[OK]`.

G6 THE PUSH AND THE PULL REQUEST — after C4: `git log --oneline -n 5`, showing C4, C3, C2, C1 and
 `8b4a1071`; `git status --porcelain` empty; the push's real outcome; the pull request's number
 and URL; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft` showing
 exactly that one pull request, from this branch into `main`, not a draft. These go in your final
 reply, not the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, and AGENTS.md's
item-status table with one row per C-item, the pull request and each gate: state block, the
per-commit changed-files table with the insertions git MEASURED beside the ones this block
expected, every gate's real output and exit code, the deviations, and the next action. Your
Session section reads SESSION 1 of feature F265, round 7, and says in one sentence how much
context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), then the Open PR
Gate — the pull request this round opens is merged by the NEXT feature's session, never by this
one — and then Rule A5, the first unchecked feature in `docs/roadmap/STATUS.md`. State the
open-findings count, 4, and the operator-questions count, 1.
