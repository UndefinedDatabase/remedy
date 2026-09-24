STEP F019 R9 — THE CLOSING ROUND: BOOK ROUND 8, ROTATE THE LEDGER, ACCEPT F019 IN STATUS WITH ITS README PINS, OPEN THE PULL REQUEST

GOAL
Book round 8's PASS, rotate the finding ledger into its archive, flip F019's STATUS line to `[x]`
with the README's accepted count, Tier 5 Done cell and Tier 5 prose in the same commit, and open
the pull request into `main`. F019 registered no finding, so there is no ownership step; F019 is
not a findings-paydown feature, so it registers nothing.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f019-r9-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f019-r9/`           READ-ONLY. The reviewer's block, texts, builder and controls.
  `.remedy-wt/f019-r9-sim/`       The reviewer's simulated tree; do not touch.
  `.remedy-wt/f019-r9-worker/`    YOURS for logs, captures and scripts; create it if absent.

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
   `feature/f019-live-node-materialization`, and `git log --oneline -1` must read `787759d9`.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f019-r9/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `gh pr list --state open --json number,headRefName` as found;
   the second must be EMPTY.

PAYLOADS — under `.remedy-wt/f019-r9-payloads/`, printed by the reviewer's builder
(lines = newline count). Verify each BEFORE using it and report every reading.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.diff | 10 | 6871 | 9cec48a06f5de527e90f4bfea483e21d440a9a74f777df6ff794a9b0d8eb0ad6 |
| plan.md | 31 | 1145 | 80c2b1052740038402c711e5d8fa71fc616f38dd0dcc7d6186ed14aa2bb9a51d |
| closure.diff | 54 | 4064 | e83081a1928fdae5b2c1258d4c051f37c0db3f4436d4320e9e3930f6a17a8a49 |
| pr_body.md | 65 | 3708 | ae0e1ca738825b3d86a0ea0f32911a95d19a734e332eeb913873804d1b62e5ab |
| status_line.txt | 1 | 399 | 9c71595a139f7cfc2fa7fd5d5a04bd5545edc9a0c899efcd0002a791b2cf400b |

`ledger.diff` appends round 8's `Gate:` entry to `.agent/live_review.md`. `plan.md` is a REWRITE of
`.agent/plan.md`. `closure.diff` flips F019's STATUS line to `[x]` and moves the README's accepted
count, its Tier 5 Done cell and its Tier 5 prose. `pr_body.md` is the pull request's description,
passed to `gh` as a file. `status_line.txt` is the exact STATUS line `closure.diff` writes, used
only for G4's proof. The `.diff` files go on with `git apply --check` then `git apply`. Never retype
or edit a payload; copy with `shutil.copyfile`.

BUNDLE — commits C1 to C4 and then the pull request, in this order.

C1 — `.agent/authored/f019-r9-block.md` := this block; `.agent/authored/f019-r9-<name>` for each
  payload, keeping its file name. Byte for byte, with `shutil.copyfile`.
  Subject: `F019 R9 C1: copy round 9 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 161. Report the number you measure, and STOP
  rather than commit if it is 500 or more.

C2 — `git apply` ledger.diff → `.agent/live_review.md` · `.agent/plan.md` := plan.md.
  Subject: `F019 R9 C2: book round 8's PASS, the package READY_FOR_REVIEW`
  Expected by `git show --numstat` (insertions/deletions): 2/0 live_review.md, 6/6 plan.md.

C3 — THE ROTATION, its own commit, paths `.agent/live_review.md` and
  `.agent/live_review_archive.md` ONLY (operator amendment amend0905-throughput, AFTER the verdict
  booking and BEFORE the STATUS flip): `python3 scripts/rotate_live_review.py`. Report its printed
  output in full.
  Subject: `F019 R9 C3: rotate the finding ledger into its archive`
  Expected (insertions/deletions): 0/24 live_review.md, 24/0 live_review_archive.md.

C4 — THE CLOSURE COMMIT, exactly these paths and no others: `docs/roadmap/STATUS.md`, `README.md`
  and `.agent/handoff.md`. `git apply` closure.diff, run G4 on the working tree, then rewrite
  `.agent/handoff.md` per `docs/agents/handback_template.md` as the closure handback, then run G5,
  then commit. The handback names, each spelled exactly as below, the package
  `remedy-review-20260924-204836-READY_FOR_REVIEW.zip`, its SHA-256
  `d0340a1a2ed77a6472e2d3f3469a4e5bf590674fd21e4d229b9c4d52d01263ff`, its directory
  `/home/decodeux/Repos/remedy-history/zips`, the evidence job `f019r8e1001` and the accepted head
  `d581b6667a9e29a1d276a39555b9038adb82a92b`, all from round 8; and it does NOT name a pull
  request number, which does not exist when it is written. There is no
  `scripts/self_use_queue.json` edit: the closure's self-use track answered NONE
  (`.agent/selfuse_f019/result.txt`).
  Subject: `F019 R9 C4: accept F019 in STATUS with its README pins`
  Expected for the two applied files (insertions/deletions): 14/2 README.md, 1/1 STATUS.md.
  Then `git push origin feature/f019-live-node-materialization`.

THE PULL REQUEST — after C4 and its push:
  `gh pr create --base main --head feature/f019-live-node-materialization --title "F019 — Live node materialization" --body-file .remedy-wt/f019-r9-payloads/pr_body.md`.
  DO NOT MERGE IT. Report the number and URL in your final reply only.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f019-r9-*` copies C1 makes,
   `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/roadmap/STATUS.md`, `README.md` and `.agent/handoff.md`. Report the set you measure with
   `git diff --name-only 787759d9` over the range to C4.
4. C4 is the LAST commit on this branch (Rule A4). Nothing follows it except, if the reviewer's
   closure gate asks for one, a commit whose path set is exactly `.agent/candidates.md` — which
   this block does not order and you never write on your own initiative.
5. If any gate goes red, STOP before C4: commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. A closure that cannot be proved is not closed.
6. NOTHING IS MERGED. No `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
7. Delete nothing you did not create: every `remedy/job-*` branch, every `.remedy-wt/job-*`
   worktree and the reviewer's worktrees whose names begin `.remedy-wt/f015-` or `.remedy-wt/f019-`
   stay.
8. DO NOT run the full suite: this feature's run is committed at
   `.agent/authored/f019-closure-suite.txt`.

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G4 run before the handback is written, and
the handback states their readings. G5 runs after the handback is written and before C4 is
committed, so its readings go in your final reply, not the handback.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 committed `.agent/authored/f019-r9-*` blob, read with `git show <C1>:<path>`, compared byte for
 byte with its source (the block copy against `.remedy-wt/f019-r9/block.md`). One reading per
 file, all equal.

G2 THE BOOKING — at C2, read with `git show <C2>:<path>`: `.agent/live_review.md` 324355 bytes,
 sha256 `40b7bfe950628223f8686781c475de55355f4de8434b5c55932e5cf01e8be183`; `.agent/plan.md` 1145
 bytes, sha256 `80c2b1052740038402c711e5d8fa71fc616f38dd0dcc7d6186ed14aa2bb9a51d`. Also: among the
 lines C2's diff ADDS, those beginning `Gate: F019 R8 — ` (1); and the open set by distinct id via
 `open_finding_ids` from `scripts/rotate_live_review.py` at `787759d9` and at C2 — the reviewer
 read R-0499, R-0950, R-1008 and R-1046 at both. Report yours beside each.

G3 THE ROTATION — at C3: the reviewer's simulation printed 10 gate records and 1 finding pair
 (2 records) moved, the ledger 324355 to 302065 bytes, the archive 4918588 to 4940878 bytes, open
 findings 4 before and 4 after, and left `.agent/live_review.md` 302065 bytes, sha256
 `36a4838a7b111078b6ab3de8b8f7972d74ab0d7088fd95e519161f0a1ce9fd84` and
 `.agent/live_review_archive.md` 4940878 bytes, sha256
 `2dd64ce58680344f26521a9e065d7c60afe0cf0f2e476c98922d257ec6d49435`. Report yours beside each, and
 C3's path set, which is the two ledger files and nothing else.

G4 THE CLOSURE EDITS AND THE TREE — with closure.diff applied, before the handback is written:
 `docs/roadmap/STATUS.md` 50463 bytes, sha256
 `72f0e4ba7a869890f68aaaf15dc67237db2b020b07360163bad931de10def118`, and `README.md` 28679 bytes,
 sha256 `7619b1cdc92751479441d62b764fe6ea7f5ec863fc1887a83012cb692a4c6a9b`; the count of lines of
 `docs/roadmap/STATUS.md` equal to the one line of status_line.txt, byte for byte, which must be 1;
 serially,
 `bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'`,
 which the reviewer's dry run over the same tree read as `437 passed, 1 skipped` at exit 0; then
 `python3 -m apps.cli.main integrity check --json`, all six checks `pass` at `fail_count` 0; and
 `python3 -m apps.cli.main integrity block .remedy-wt/f019-r9/block.md`, real exit code 0 with
 every item `[OK]`. The reviewer red-controlled the pins there: with the accepted count left at
 97, or the Tier 5 Done cell left at 16, `tests/docs/` read `1 failed, 326 passed`, and with the
 STATUS line left `[~]` it read `3 failed, 324 passed`. Report yours beside each.

G5 THE HANDBACK'S PINS — after the handback is written, before C4 is committed: for each of the
 five strings C4 names — the package filename, its SHA-256, its directory, the evidence job and
 the accepted head — the count of its occurrences in the new `.agent/handoff.md`, each of which
 must be at least 1; and the count of the string `pull/` in it, which must be 0. If any count
 misses, fix the handback and measure again before committing; report both measurements.

G6 THE PUSH AND THE PULL REQUEST — after C4: `git log --oneline -n 5`, showing C4, C3, C2, C1 and
 `787759d9`; `git status --porcelain` empty; the push's real outcome; the pull request's number
 and URL; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft` showing
 exactly that one pull request, from this branch into `main`, not a draft. These go in your final
 reply, not the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, and AGENTS.md's
item-status table with one row per C-item, the pull request and each gate: state block, the
per-commit changed-files table with the insertions git MEASURED beside the ones this block
expected, every gate reading G1 to G4 with its real exit code, the deviations, and the next
action. Your Session section reads SESSION 2 of feature F019, round 9, and says in one sentence
how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), then the Open PR
Gate — the pull request this round opens is merged by the NEXT feature's session, never by this
one — and then Rule A5, the first unchecked feature in `docs/roadmap/STATUS.md`. State the
open-findings count, 4, and the operator-questions count, 3.
