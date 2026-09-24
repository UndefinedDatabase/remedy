STEP F015 R9 — THE CLOSING ROUND: BOOK ROUND 8, ROTATE THE LEDGER, ACCEPT F015 IN STATUS WITH ITS README PINS, OPEN THE PULL REQUEST

GOAL
Book round 8's PASS, rotate the finding ledger into its archive, flip F015's STATUS line to `[x]`
with the README's accepted count, Tier 5 Done cell and Tier 5 prose in the same commit, and open
the pull request into `main`. F015 registered no finding, so there is no ownership step; F015 is
not a findings-paydown feature, so it registers nothing.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f015-r9-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f015-r9-scratch/`   READ-ONLY. The reviewer's simulation tools and logs.
  `.remedy-wt/f015-r9-worker/`    YOURS for logs, captures and scripts; create it if absent.

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
   `feature/f015-interactive-plan-editing`, and `git log --oneline -1` must read `2cdf826f`.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f015-r9-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `gh pr list --state open --json number,headRefName` as found;
   the second must be EMPTY.

PAYLOADS — under `.remedy-wt/f015-r9-payloads/`, printed by the reviewer's simulation
(lines = newline count). Verify each BEFORE using it and report every reading.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.diff | 10 | 5383 | 6951a42a52e21a23282bc0b8c7f85b338ed277749873d1a9ad24fb5657e45c06 |
| plan.md | 29 | 1005 | f54fe04928fcc3407237e5fabc2a197be7077132a0c4086333bacfe39b9cf5f9 |
| closure.diff | 53 | 4051 | 4e13ffbc4d25ab7df49f7da055212ff703cc328a1473f803613202758b0b7651 |
| pr_body.md | 55 | 3279 | 24afd9c200bf936244dbc82ad7f105798b54431f592c559c343bcff192e64856 |
| status_line.txt | 1 | 398 | 427f92353f11dcbe18192cfbadd0d10e6318183a15f5dcb31807d904e70eeca4 |

`ledger.diff` appends round 3's `Gate:` entry to `.agent/live_review.md`. `plan.md` is a REWRITE of
`.agent/plan.md`. `closure.diff` flips F015's STATUS line to `[x]` and moves the README's accepted
count, its Tier 5 Done cell and its Tier 5 prose. `pr_body.md` is the pull request's description,
passed to `gh` as a file. `status_line.txt` is the exact STATUS line `closure.diff` writes, used
only for G4's proof. The `.diff` files go on with `git apply --check` then `git apply`. Never retype
or edit a payload; copy with `shutil.copyfile`.

BUNDLE — commits C1 to C4 and then the pull request, in this order.

C1 — `.agent/authored/f015-r9-block.md` := this block; `.agent/authored/f015-r9-<name>` for each
  payload, keeping its file name. Byte for byte, with `shutil.copyfile`.
  Subject: `F015 R9 C1: copy round 9 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 148. Report the number you measure, and STOP
  rather than commit if it is 500 or more.

C2 — `git apply` ledger.diff → `.agent/live_review.md` · `.agent/plan.md` := plan.md.
  Subject: `F015 R9 C2: book round 8's PASS, the package READY_FOR_REVIEW`
  Expected by `git show --numstat` (insertions/deletions): 2/0 live_review.md, 6/5 plan.md.

C3 — THE ROTATION, its own commit, paths `.agent/live_review.md` and
  `.agent/live_review_archive.md` ONLY (operator amendment amend0905-throughput, AFTER the verdict
  booking and BEFORE the STATUS flip): `python3 scripts/rotate_live_review.py`. Report its printed
  output in full.
  Subject: `F015 R9 C3: rotate the finding ledger into its archive`
  Expected (insertions/deletions): 0/6 live_review.md, 6/0 live_review_archive.md.

C4 — THE CLOSURE COMMIT, exactly these paths and no others: `docs/roadmap/STATUS.md`, `README.md`
  and `.agent/handoff.md`. `git apply` closure.diff, run G4 on the working tree, then rewrite
  `.agent/handoff.md` per `docs/agents/handback_template.md` as the closure handback, then run G5,
  then commit. The handback names, each spelled exactly as below, the package
  `remedy-review-20260924-151010-READY_FOR_REVIEW.zip`, its SHA-256
  `920b9e1c3763632b86e97cb9724831e9c9e58378bbc71bac4532638e976da840`, its directory
  `/home/decodeux/Repos/remedy-history/zips`, the evidence job `f015r8e1001` and the accepted head
  `15aec1449745c1843ad4096e44974b8710b0756c`, all from round 8; and it does NOT name a pull
  request number, which does not exist when it is written. There is no
  `scripts/self_use_queue.json` edit: the closure's self-use track answered NONE
  (`.agent/selfuse_f015/result.txt`).
  Subject: `F015 R9 C4: accept F015 in STATUS with its README pins`
  Expected for the two applied files (insertions/deletions): 13/2 README.md, 1/1 STATUS.md.
  Then `git push origin feature/f015-interactive-plan-editing`.

THE PULL REQUEST — after C4 and its push:
  `gh pr create --base main --head feature/f015-interactive-plan-editing --title "F015 — Interactive plan editing" --body-file .remedy-wt/f015-r9-payloads/pr_body.md`.
  DO NOT MERGE IT. Report the number and URL in your final reply only.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f015-r9-*` copies C1 makes,
   `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/roadmap/STATUS.md`, `README.md` and `.agent/handoff.md`. Report the set you measure with
   `git diff --name-only 2cdf826f` over the range to C4.
4. C4 is the LAST commit on this branch (Rule A4). Nothing follows it except, if the reviewer's
   closure gate asks for one, a commit whose path set is exactly `.agent/candidates.md` — which
   this block does not order and you never write on your own initiative.
5. If any gate goes red, STOP before C4: commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. A closure that cannot be proved is not closed.
6. NOTHING IS MERGED. No `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
7. Delete nothing you did not create: every `remedy/job-*` branch, every `.remedy-wt/job-*`
   worktree and the reviewer's worktrees whose names begin `.remedy-wt/f015-` stay.
8. DO NOT run the full suite: this feature's run is committed at
   `.agent/authored/f015-closure-suite.txt`.

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G4 run before the handback is written, and
the handback states their readings. G5 runs after the handback is written and before C4 is
committed, so its readings go in your final reply, not the handback.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 committed `.agent/authored/f015-r9-*` blob, read with `git show <C1>:<path>`, compared byte for
 byte with its source (the block copy against `.remedy-wt/f015-r9-block.md`). One reading per
 file, all equal.

G2 THE BOOKING — at C2, read with `git show <C2>:<path>`: `.agent/live_review.md` 307764 bytes,
 sha256 `82310ee4224bebb82538f6f905fa28711a58bb02504be67768a90c0c432524bd`; `.agent/plan.md` 1005
 bytes, sha256 `f54fe04928fcc3407237e5fabc2a197be7077132a0c4086333bacfe39b9cf5f9`. Also: among the
 lines C2's diff ADDS, those beginning `Gate: F015 R8 — ` (1); and the open set by distinct id via
 `open_finding_ids` from `scripts/rotate_live_review.py` at `2cdf826f` and at C2 — the reviewer
 read 4 and 4, R-0499, R-0950, R-1008 and R-1046, both differences empty. Report yours beside
 each.

G3 THE ROTATION — at C3: the reviewer's simulation printed 3 gate records and 0 finding pairs
 moved, the ledger 307764 to 301103 bytes, the archive 4911927 to 4918588 bytes, open findings 4
 before and 4 after, and left `.agent/live_review.md` 301103 bytes, sha256
 `41add2d19a15af999decb086828f99332326b74ace154034aa28105a31d05803` and
 `.agent/live_review_archive.md` 4918588 bytes, sha256
 `b5c3f60b45df355b40d1093b68995b3d99c6d21fb5b1d1a03c5ed962cc798273`. Report yours beside each, and
 C3's path set, which is the two ledger files and nothing else.

G4 THE CLOSURE EDITS AND THE TREE — with closure.diff applied, before the handback is written:
 `docs/roadmap/STATUS.md` 50105 bytes, sha256
 `156d7a9b3a598fca2ec2d2c68cae4ed04ff76cbb638223323564ee2bece5ce82`, and `README.md` 27839 bytes,
 sha256 `fd25b1849f613dc121acb1897aaffde21f8e60f625e2cdeddba304066ea20ab4`; the count of lines of
 `docs/roadmap/STATUS.md` equal to the one line of status_line.txt, byte for byte, which must be 1;
 serially,
 `bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'`,
 which the reviewer's dry run over the same tree read as `437 passed, 1 skipped` at exit 0; then
 `python3 -m apps.cli.main integrity check --json`, all six checks `pass` at `fail_count` 0; and
 `python3 -m apps.cli.main integrity block .remedy-wt/f015-r9-block.md`, real exit code 0 with
 every item `[OK]`. The reviewer red-controlled the pins there: with the accepted count left at
 96, or the Tier 5 Done cell left at 15, `tests/docs/` read `1 failed, 326 passed`, and with the
 STATUS line left `[~]` it read `3 failed, 324 passed`. Report yours beside each.

G5 THE HANDBACK'S PINS — after the handback is written, before C4 is committed: for each of the
 five strings C4 names — the package filename, its SHA-256, its directory, the evidence job and
 the accepted head — the count of its occurrences in the new `.agent/handoff.md`, each of which
 must be at least 1; and the count of the string `pull/` in it, which must be 0. If any count
 misses, fix the handback and measure again before committing; report both measurements.

G6 THE PUSH AND THE PULL REQUEST — after C4: `git log --oneline -n 5`, showing C4, C3, C2, C1 and
 `2cdf826f`; `git status --porcelain` empty; the push's real outcome; the pull request's number
 and URL; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft` showing
 exactly that one pull request, from this branch into `main`, not a draft. These go in your final
 reply, not the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, and AGENTS.md's
item-status table with one row per C-item, the pull request and each gate: state block, the
per-commit changed-files table with the insertions git MEASURED beside the ones this block
expected, every gate reading G1 to G4 with its real exit code, the deviations, and the next
action. Your Session section reads SESSION 1 of feature F015, round 9, and says in one sentence
how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), then the Open PR
Gate — the pull request this round opens is merged by the NEXT feature's session, never by this
one — and then Rule A5, the first unchecked feature in `docs/roadmap/STATUS.md`. State the
open-findings count, 4, and the operator-questions count, 1.
