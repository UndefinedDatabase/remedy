STEP F264 R10 — THE CLOSING ROUND: BOOK ROUND 9, ROTATE THE LEDGER, ACCEPT F264 IN STATUS WITH ITS README PINS, OPEN THE PULL REQUEST

GOAL
Book round 9's PASS, rotate the finding ledger into its archive, flip F264's STATUS line to `[x]`
with the README's accepted count, Tier 5 Done cell and Tier 5 prose in the same commit, and open
the pull request into `main`. F264 owned no finding, so there is no ownership step, and it is not a
findings-paydown feature, so it registers nothing.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f264-r10-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f264-r10-scratch/`   READ-ONLY. The reviewer's simulation tools and logs.
  `.remedy-wt/f264-r10-worker/`    YOURS for logs, captures and scripts.

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
   `feature/f264-steering-channel`, and `git log --oneline -1` must read `0eb5b2d6`.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f264-r10-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `gh pr list --state open --json number,headRefName` as found;
   the second must be EMPTY.

PAYLOADS — under `.remedy-wt/f264-r10-payloads/`, printed by the reviewer's simulation
(lines = newline count). Verify each BEFORE using it and report every reading.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.diff | 10 | 7278 | 189220a51bd7920f4a0552d4b1e4a95619d0b063b9a2e9166b27c6a1ef7c32f5 |
| plan.md | 27 | 895 | d4228171605278544097525691199fe0701077c6c63e35a3c9394a28d7a43d84 |
| closure.diff | 52 | 2720 | 5cc76025350d8db85b69563d03c1c1286db1b7030e45a967ce8ba196c5f568b3 |
| pr_body.md | 116 | 6077 | 2b7b38709ec97aeef6a90f0c0642cf0c2dcdac219bf223fbe8a7557907a2bf1d |
| status_line.txt | 1 | 402 | a1135b53799a77b573c812c1f56e290466b59586c5f146c443700281120b1ac2 |

`ledger.diff` appends round 9's `Gate:` entry to `.agent/live_review.md`. `plan.md` is a REWRITE of
`.agent/plan.md`. `closure.diff` flips F264's STATUS line to `[x]` and moves the README's accepted
count, its Tier 5 Done cell and its Tier 5 prose. `pr_body.md` is the pull request's description,
passed to `gh` as a file. `status_line.txt` is the exact STATUS line `closure.diff` writes, used
only for G4's proof. The `.diff` files go on with `git apply --check` then `git apply`. Never retype
or edit a payload; copy with `shutil.copyfile`.

BUNDLE — commits C1 to C4 and then the pull request, in this order.

C1 — `.agent/authored/f264-r10-block.md` := this block; `.agent/authored/f264-r10-<name>` for each
  payload, keeping its file name. Byte for byte, with `shutil.copyfile`.
  Subject: `F264 R10 C1: copy round 10 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 206. Report the number you measure, and STOP
  rather than commit if it is 500 or more.

C2 — `git apply` ledger.diff → `.agent/live_review.md` · `.agent/plan.md` := plan.md.
  Subject: `F264 R10 C2: book round 9's PASS, the package READY_FOR_REVIEW`
  Expected by `git show --numstat` (insertions/deletions): 2/0 live_review.md, 6/5 plan.md.

C3 — THE ROTATION, its own commit, paths `.agent/live_review.md` and
  `.agent/live_review_archive.md` ONLY (operator amendment amend0905-throughput, AFTER the verdict
  booking and BEFORE the STATUS flip): `python3 scripts/rotate_live_review.py`. Report its printed
  output in full.
  Subject: `F264 R10 C3: rotate the finding ledger into its archive`
  Expected (insertions/deletions): 0/24 live_review.md, 24/0 live_review_archive.md.

C4 — THE CLOSURE COMMIT, exactly these paths and no others: `docs/roadmap/STATUS.md`, `README.md`
  and `.agent/handoff.md`. `git apply` closure.diff, run G4 and G5 on the working tree, then
  rewrite `.agent/handoff.md` per `docs/agents/handback_template.md` as the closure handback: it
  names the package, its SHA-256, its directory, the evidence job and the accepted head from
  round 9, and it does NOT name a pull request number, which does not exist when it is written.
  There is no `scripts/self_use_queue.json` edit: the closure's self-use track answered NONE
  (`.agent/selfuse_f264/result.txt`).
  Subject: `F264 R10 C4: accept F264 in STATUS with its README pins`
  Expected for the two applied files (insertions/deletions): 12/2 README.md, 1/1 STATUS.md.
  Then `git push origin feature/f264-steering-channel`.

THE PULL REQUEST — after C4 and its push:
  `gh pr create --base main --head feature/f264-steering-channel --title "F264 — Steering channel (remedy chat)" --body-file .remedy-wt/f264-r10-payloads/pr_body.md`.
  DO NOT MERGE IT. Report the number and URL in your final reply only.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f264-r10-*` copies C1 makes,
   `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/roadmap/STATUS.md`, `README.md` and `.agent/handoff.md`. Report the set you measure with
   `git diff --name-only 0eb5b2d6 HEAD` after C4.
4. C4 is the LAST commit on this branch (Rule A4). Nothing follows it except, if the reviewer's
   closure gate asks for one, a commit whose path set is exactly `.agent/candidates.md` — which
   this block does not order and you never write on your own initiative.
5. If any gate goes red, STOP before C4: commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. A closure that cannot be proved is not closed.
6. NOTHING IS MERGED. No `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
7. Delete nothing you did not create: every `remedy/job-*` branch, every `.remedy-wt/job-*`
   worktree and the reviewer's worktrees whose names begin `.remedy-wt/f264-` stay.
8. DO NOT run the full suite: this feature's run is committed at
   `.agent/authored/f264-closure-suite.txt`.

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G5 run before C4 is written; G4 and G5
therefore read the working tree with closure.diff applied, before the handoff is written.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 committed `.agent/authored/f264-r10-*` blob, read with `git show <C1>:<path>`, compared byte for
 byte with its source (the block copy against `.remedy-wt/f264-r10-block.md`). One reading per
 file, all equal.

G2 THE BOOKING — at C2, read with `git show <C2>:<path>`: `.agent/live_review.md` 329356 bytes,
 sha256 `9cf16924c777dd483e94db1f9c31056664c7356d5a8de3785ac85164995d1ee8`; `.agent/plan.md` 895
 bytes, sha256 `d4228171605278544097525691199fe0701077c6c63e35a3c9394a28d7a43d84`. Also: among the
 lines C2's diff ADDS, those beginning `Gate: F264 R9 — ` (1); and the open set by distinct id via
 `open_finding_ids` from `scripts/rotate_live_review.py` at `0eb5b2d6` and at C2 — the reviewer
 read 3 and 3, R-0499, R-0950 and R-1008, both differences empty. Report yours beside each.

G3 THE ROTATION — at C3: the reviewer's simulation printed 12 gate records and 0 finding pairs
 moved, the ledger 329356 to 302891 bytes, the archive 4852084 to 4878549 bytes, open findings 3
 before and 3 after, and left `.agent/live_review.md` at sha256
 `4314376b2d9bae9f128545dadf29ae90d4a8844418467a6d06049d90e5731941` and
 `.agent/live_review_archive.md` at sha256
 `b60110ea5f4ccce65563aac3a695588c6b3801a1dd30ce477b39f4cb9dfd218f`. Report yours beside each, and
 C3's path set, which is the two ledger files and nothing else.

G4 THE CLOSURE EDITS — with closure.diff applied, before C4 is committed: `docs/roadmap/STATUS.md`
 at 49035 bytes, sha256 `6a886c8514bc26063ae9e5a5a3c535ed0737447c1d60ff1cbd92d10eaa7d09ab`, and
 `README.md` at 26011 bytes, sha256
 `9396a700454779e8c2e00d916809b8573fc387d3f75c0dee433034e8604979ed`; the count of lines of
 `docs/roadmap/STATUS.md` equal to the one line of status_line.txt, byte for byte, which must be 1;
 and, serially,
 `bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'`,
 which the reviewer's dry run over the same tree read as `437 passed, 1 skipped` at exit 0. The
 reviewer red-controlled the README pins there: with the accepted count left at 93, or the Tier 5
 Done cell left at 13, `tests/docs/` read `1 failed, 326 passed`, and with the STATUS line left
 `[~]` it read `3 failed, 324 passed`. Report yours beside each.

G5 THE TREE — with closure.diff applied, before C4: `python3 -m apps.cli.main integrity check
 --json`, all six checks `pass` at `fail_count` 0; and `python3 -m apps.cli.main integrity block
 .remedy-wt/f264-r10-block.md`, real exit code 0 with every item `[OK]`.

G6 THE PUSH AND THE PULL REQUEST — after C4: `git log --oneline -n 5`, showing C4, C3, C2, C1 and
 `0eb5b2d6`; `git status --porcelain` empty; the push's real outcome; the pull request's number
 and URL; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft` showing
 exactly that one pull request, from this branch into `main`, not a draft. These go in your final
 reply, not the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, and AGENTS.md's
item-status table with one row per C-item, the pull request and each gate: state block, the
per-commit changed-files table with the insertions git MEASURED beside the ones this block
expected, every gate's real output and exit code, the deviations, and the next action. Your
Session section reads SESSION 2 of feature F264, round 10, and says in one sentence how much
context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), then the Open PR
Gate — the pull request this round opens is merged by the NEXT feature's session, never by this
one — and then Rule A5, the first unchecked feature in `docs/roadmap/STATUS.md`. State the
open-findings count, 3, and the operator-questions count, 0.
