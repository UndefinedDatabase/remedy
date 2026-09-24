STEP F267 R4 — THE CLOSING ROUND: BOOK ROUND 3, ROTATE THE LEDGER, ACCEPT F267 IN STATUS WITH ITS README PINS, OPEN THE PULL REQUEST

GOAL
Book round 3's PASS, rotate the finding ledger into its archive, flip F267's STATUS line to `[x]`
with the README's accepted count, Tier 2 Done cell and Tier 2 prose in the same commit, and open
the pull request into `main`. F267 registered no finding, so there is no ownership step; F267 is
not a findings-paydown feature, so it registers nothing.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f267-r4-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f267-r4-scratch/`   READ-ONLY. The reviewer's simulation tools and logs.
  `.remedy-wt/f267-r4-worker/`    YOURS for logs, captures and scripts; create it if absent.

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
   `feature/f267-list-commands-v2-completion`, and `git log --oneline -1` must read `74346eb2`.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f267-r4-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `gh pr list --state open --json number,headRefName` as found;
   the second must be EMPTY.

PAYLOADS — under `.remedy-wt/f267-r4-payloads/`, printed by the reviewer's simulation
(lines = newline count). Verify each BEFORE using it and report every reading.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.diff | 10 | 6913 | fa718fb76c36f03bc6d309a10e781ce2125cc9b2717c67a9ebb731568b5db02d |
| plan.md | 29 | 957 | e6ca17d2506cf571dc1a161e9f62ddec905ba5a6f83d1f8ebd847f634b213ceb |
| closure.diff | 48 | 3833 | 041b4bf31d3157fb393ffa44809dec2e2950e7717a8bec016de31c500383be7e |
| pr_body.md | 55 | 2724 | 09f9c5985d0c753c20328c69f396e3dbde61635d262625ea28e2c3a9ebff5275 |
| status_line.txt | 1 | 453 | 84918147523800054e91a3c02c01fe882c4aea46c792a1526dc2fa958dfa29e8 |

`ledger.diff` appends round 3's `Gate:` entry to `.agent/live_review.md`. `plan.md` is a REWRITE of
`.agent/plan.md`. `closure.diff` flips F267's STATUS line to `[x]` and moves the README's accepted
count, its Tier 2 Done cell and its Tier 2 prose. `pr_body.md` is the pull request's description,
passed to `gh` as a file. `status_line.txt` is the exact STATUS line `closure.diff` writes, used
only for G4's proof. The `.diff` files go on with `git apply --check` then `git apply`. Never retype
or edit a payload; copy with `shutil.copyfile`.

BUNDLE — commits C1 to C4 and then the pull request, in this order.

C1 — `.agent/authored/f267-r4-block.md` := this block; `.agent/authored/f267-r4-<name>` for each
  payload, keeping its file name. Byte for byte, with `shutil.copyfile`.
  Subject: `F267 R4 C1: copy round 4 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 143. Report the number you measure, and STOP
  rather than commit if it is 500 or more.

C2 — `git apply` ledger.diff → `.agent/live_review.md` · `.agent/plan.md` := plan.md.
  Subject: `F267 R4 C2: book round 3's PASS, the package READY_FOR_REVIEW`
  Expected by `git show --numstat` (insertions/deletions): 2/0 live_review.md, 6/5 plan.md.

C3 — THE ROTATION, its own commit, paths `.agent/live_review.md` and
  `.agent/live_review_archive.md` ONLY (operator amendment amend0905-throughput, AFTER the verdict
  booking and BEFORE the STATUS flip): `python3 scripts/rotate_live_review.py`. Report its printed
  output in full.
  Subject: `F267 R4 C3: rotate the finding ledger into its archive`
  Expected (insertions/deletions): 0/12 live_review.md, 12/0 live_review_archive.md.

C4 — THE CLOSURE COMMIT, exactly these paths and no others: `docs/roadmap/STATUS.md`, `README.md`
  and `.agent/handoff.md`. `git apply` closure.diff, run G4 on the working tree, then rewrite
  `.agent/handoff.md` per `docs/agents/handback_template.md` as the closure handback, then run G5,
  then commit. The handback names, each spelled exactly as below, the package
  `remedy-review-20260924-110023-READY_FOR_REVIEW.zip`, its SHA-256
  `66aa577c32cf0650a2fb42815ee20d58a78ac6f97ba836fa5536d345b11c42b7`, its directory
  `/home/decodeux/Repos/remedy-history/zips`, the evidence job `f267r3e1001` and the accepted head
  `8042aa506c55b9ee7a2f3ed6d28a0d9f2b86dbbf`, all from round 3; and it does NOT name a pull
  request number, which does not exist when it is written. There is no
  `scripts/self_use_queue.json` edit: the closure's self-use track answered NONE
  (`.agent/selfuse_f267/result.txt`).
  Subject: `F267 R4 C4: accept F267 in STATUS with its README pins`
  Expected for the two applied files (insertions/deletions): 9/3 README.md, 1/1 STATUS.md.
  Then `git push origin feature/f267-list-commands-v2-completion`.

THE PULL REQUEST — after C4 and its push:
  `gh pr create --base main --head feature/f267-list-commands-v2-completion --title "F267 — List commands v2 completion" --body-file .remedy-wt/f267-r4-payloads/pr_body.md`.
  DO NOT MERGE IT. Report the number and URL in your final reply only.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f267-r4-*` copies C1 makes,
   `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/roadmap/STATUS.md`, `README.md` and `.agent/handoff.md`. Report the set you measure with
   `git diff --name-only 74346eb2` over the range to C4.
4. C4 is the LAST commit on this branch (Rule A4). Nothing follows it except, if the reviewer's
   closure gate asks for one, a commit whose path set is exactly `.agent/candidates.md` — which
   this block does not order and you never write on your own initiative.
5. If any gate goes red, STOP before C4: commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. A closure that cannot be proved is not closed.
6. NOTHING IS MERGED. No `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
7. Delete nothing you did not create: every `remedy/job-*` branch, every `.remedy-wt/job-*`
   worktree and the reviewer's worktrees whose names begin `.remedy-wt/f267-` stay.
8. DO NOT run the full suite: this feature's run is committed at
   `.agent/authored/f267-closure-suite.txt`.

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G4 run before the handback is written, and
the handback states their readings. G5 runs after the handback is written and before C4 is
committed, so its readings go in your final reply, not the handback.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 committed `.agent/authored/f267-r4-*` blob, read with `git show <C1>:<path>`, compared byte for
 byte with its source (the block copy against `.remedy-wt/f267-r4-block.md`). One reading per
 file, all equal.

G2 THE BOOKING — at C2, read with `git show <C2>:<path>`: `.agent/live_review.md` 305511 bytes,
 sha256 `0bf7c8ef0d1b392e537df01397f031f6a4854778c7c3966b55ed636ca647122c`; `.agent/plan.md` 957
 bytes, sha256 `e6ca17d2506cf571dc1a161e9f62ddec905ba5a6f83d1f8ebd847f634b213ceb`. Also: among the
 lines C2's diff ADDS, those beginning `Gate: F267 R3 — ` (1); and the open set by distinct id via
 `open_finding_ids` from `scripts/rotate_live_review.py` at `74346eb2` and at C2 — the reviewer
 read 4 and 4, R-0499, R-0950, R-1008 and R-1046, both differences empty. Report yours beside
 each.

G3 THE ROTATION — at C3: the reviewer's simulation printed 6 gate records and 0 finding pairs
 moved, the ledger 305511 to 291942 bytes, the archive 4898358 to 4911927 bytes, open findings 4
 before and 4 after, and left `.agent/live_review.md` 291942 bytes, sha256
 `2d4899ac2b8b6e1473befe6b960b0469ad6fafc18af7848f6dfef3b59eefca94` and
 `.agent/live_review_archive.md` 4911927 bytes, sha256
 `268d47762cbc1adaa24779f68a71c747ea32781694243934b72009e69ec507c7`. Report yours beside each, and
 C3's path set, which is the two ledger files and nothing else.

G4 THE CLOSURE EDITS AND THE TREE — with closure.diff applied, before the handback is written:
 `docs/roadmap/STATUS.md` 49747 bytes, sha256
 `8f6cc4c5be4866ecda144eb965ed76603bba6dfe14e7186b3649a9043479a8a9`, and `README.md` 27064 bytes,
 sha256 `7a919d16cdadd8c76741a8d78609eb235d69ea6141deee793cdd13ecfc5c25fb`; the count of lines of
 `docs/roadmap/STATUS.md` equal to the one line of status_line.txt, byte for byte, which must be 1;
 serially,
 `bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'`,
 which the reviewer's dry run over the same tree read as `437 passed, 1 skipped` at exit 0; then
 `python3 -m apps.cli.main integrity check --json`, all six checks `pass` at `fail_count` 0; and
 `python3 -m apps.cli.main integrity block .remedy-wt/f267-r4-block.md`, real exit code 0 with
 every item `[OK]`. The reviewer red-controlled the pins there: with the accepted count left at
 95, or the Tier 2 Done cell left at 35, `tests/docs/` read `1 failed, 326 passed`, and with the
 STATUS line left `[~]` it read `4 failed, 323 passed`. Report yours beside each.

G5 THE HANDBACK'S PINS — after the handback is written, before C4 is committed: for each of the
 five strings C4 names — the package filename, its SHA-256, its directory, the evidence job and
 the accepted head — the count of its occurrences in the new `.agent/handoff.md`, each of which
 must be at least 1; and the count of the string `pull/` in it, which must be 0. If any count
 misses, fix the handback and measure again before committing; report both measurements.

G6 THE PUSH AND THE PULL REQUEST — after C4: `git log --oneline -n 5`, showing C4, C3, C2, C1 and
 `74346eb2`; `git status --porcelain` empty; the push's real outcome; the pull request's number
 and URL; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft` showing
 exactly that one pull request, from this branch into `main`, not a draft. These go in your final
 reply, not the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, and AGENTS.md's
item-status table with one row per C-item, the pull request and each gate: state block, the
per-commit changed-files table with the insertions git MEASURED beside the ones this block
expected, every gate reading G1 to G4 with its real exit code, the deviations, and the next
action. Your Session section reads SESSION 1 of feature F267, round 4, and says in one sentence
how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), then the Open PR
Gate — the pull request this round opens is merged by the NEXT feature's session, never by this
one — and then Rule A5, the first unchecked feature in `docs/roadmap/STATUS.md`. State the
open-findings count, 4, and the operator-questions count, 1.
