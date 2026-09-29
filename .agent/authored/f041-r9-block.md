STEP F041 R9 — THE CLOSING ROUND: BOOK ROUND 8, ROTATE, ACCEPT F041, OPEN THE PULL REQUEST

GOAL
Book round 8's PASS; rotate the finding ledger into its archive; flip F041's STATUS line to `[x]`
with the README's accepted count, Tier 5 Done cell and Tier 5 prose in the same commit; and open the
pull request into `main`. The closure's self-use reading was `None` (queue exhausted), so no queue
entry changes. F041 is not a findings-paydown feature, so nothing is registered. This closes F041.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f041-r9-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f041-r9/`           READ-ONLY. The reviewer's block and scripts.
  `.remedy-wt/f041-r9-sim/` and every other `.remedy-wt/f041-*` path   The reviewer's; do not
                                  touch.
  `.remedy-wt/f041-r9-worker/`    YOURS for logs and scripts; create it if absent.

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
   `feature/f041-artifact-preview`, and `git log --oneline -1` must read `f48d56ec8`.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f041-r9/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found, and
   `gh pr list --state open --json number,headRefName`, which must read `[]`.

PAYLOADS — under `.remedy-wt/f041-r9-payloads/`, printed by the reviewer's builder
(lines = newline count). Verify each BEFORE using it and report every reading.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 2 | 2278 | 61ca15beb81ec0c6da9f917e44ca3f2b15498a7d33339ae74cc41cde5f386a46 |
| plan.md | 25 | 726 | 307edc373c1e79b102c5ae9f972d24c9b0297d04468eeb43e583cbe725b8eba9 |
| status_line.txt | 1 | 418 | 73b46269474e390a0f5964f9a64a481a42865b685a5a25da593700c11063d555 |
| closure.diff | 52 | 3019 | f6399647c8ee1ebcb48dbba0aac5517897202c21a81ae60a527fe5f7692accfd |
| pr_body.md | 76 | 4619 | 668a71eef31403be9aed0d7e5ac5e511c4e2d315054121ba088f846335207102 |

`ledger.md` is APPENDED to `.agent/live_review.md` as raw bytes (round 8's `Gate:` entry, which
begins with its own blank line). `plan.md` is a REWRITE of `.agent/plan.md`. `closure.diff` edits
`docs/roadmap/STATUS.md` and `README.md`; its STATUS line is `status_line.txt`, whose one line it
carries byte for byte. `pr_body.md` is the pull request's body. `closure.diff` goes on with
`git apply --check` then `git apply`. Never retype or edit a payload.

BUNDLE — four commits, then the push and the pull request, in this order.

C1 — `.agent/authored/f041-r9-block.md` := this block; `.agent/authored/f041-r9-<name>` for each
  payload, keeping its file name. All by `shutil.copyfile`.
  Subject: `F041 R9 C1: copy round 9 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 156. Report the number you measure, and STOP
  rather than commit if it is 500 or more.
C2 — append ledger.md to `.agent/live_review.md` (bytes to bytes), then `.agent/plan.md` := plan.md.
  Subject: `F041 R9 C2: book round 8's PASS, the package READY_FOR_REVIEW`
  Expected by `git show --numstat` (insertions/deletions): 2/0 .agent/live_review.md, 4/5 .agent/plan.md.
C3 — `python3 scripts/rotate_live_review.py`, and report its whole printed output; then commit
  exactly the two ledger files. The reviewer's run of the same script over its simulated tree at
  C2 printed (its last line names the simulated tree's paths where yours names the checkout's):
    gate records moved: 4
    finding pairs moved: 2 (4 records)
    old ledger size: 315887 bytes
    new ledger size: 304007 bytes
    old archive size: 5508061 bytes
    new archive size: 5519941 bytes
    open findings before: 0
    open findings after: 0
    written: /home/decodeux/Repos/remedy/.remedy-wt/f041-r9-sim/.agent/live_review.md and /home/decodeux/Repos/remedy/.remedy-wt/f041-r9-sim/.agent/live_review_archive.md
  Subject: `F041 R9 C3: rotate the finding ledger into its archive`
  Expected: 0/16 .agent/live_review.md, 16/0 .agent/live_review_archive.md.
C4 — `git apply` closure.diff; run G4 BEFORE writing the handback; then rewrite
  `.agent/handoff.md` per `docs/agents/handback_template.md` and commit all three together.
  Subject: `F041 R9 C4: accept F041 in STATUS with its README pins`
  Expected, measured before the handback joins the commit: 12/2 README.md, 1/1 docs/roadmap/STATUS.md.
THEN — `git push origin feature/f041-artifact-preview`; then
  `gh pr create --base main --head feature/f041-artifact-preview --title "F041 — Artifact preview" --body-file .remedy-wt/f041-r9-payloads/pr_body.md`,
  and report its real output: the number and the URL.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f041-r9-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `.agent/live_review_archive.md`,
   `docs/roadmap/STATUS.md`, `README.md` and `.agent/handoff.md`. Report the set you measure with
   `git diff --name-only f48d56ec8` after C4. `scripts/self_use_queue.json` does not change.
4. C4 is the LAST commit on this branch (Rule A4). If a gate goes red, STOP, commit and push what
   is verified, write an honest handoff under AGENTS.md "If Blocked", and hand back without
   creating the pull request.
5. NOTHING IS MERGED. No `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
6. Delete nothing you did not create; leave every worktree, branch and stash alone.
7. Your handback names no pull request number, which does not exist when it is written; the
   number goes in your reply.

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G4 run before the handback is written; G5
and G6 after C4.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 committed `.agent/authored/f041-r9-*` blob, read with `git show <C1>:<path>`, compared byte for
 byte with its source (the block copy against `.remedy-wt/f041-r9/block.md`). One reading per file.

G2 THE BOOKING, THE ROTATION AND THE ACCEPTANCE — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named (the C4 rows from the working tree before the
 handback joins the commit), equals the reviewer's simulation:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 315887 | f631c614250c6998c29171184fcd24610a16d78e9105d186051b99b0acf4ef16 |
 | C2 | .agent/plan.md | 726 | 307edc373c1e79b102c5ae9f972d24c9b0297d04468eeb43e583cbe725b8eba9 |
 | C3 | .agent/live_review.md | 304007 | 47d0dfa4aa5b8622f87831949d9a40b369f1b9043d5c94b52e40fd0a0a2ab70e |
 | C3 | .agent/live_review_archive.md | 5519941 | babc6f47220fea33507c93d6a3b5e40a78eeead9fb01fa1587fcefeaac9171c2 |
 | C4 | README.md | 45688 | 4e7e9ecbb024fb909d48c67333cc3e1296547f29ba10471c0ae7dbf3bbdfdaac |
 | C4 | docs/roadmap/STATUS.md | 58294 | 6a3745de1a4272035562c58e781ccfcc6836df3ad97015aa6a8ebbf1b123f204 |
 Also: C3's path set, exactly the two ledger files; and the open set by distinct id via
 `open_finding_ids` over the ledger's TEXT at C2, C3 and C4, which the reviewer's simulation read
 as empty at each.

G3 THE STATUS LINE — at C4, the status_line.txt content with its trailing newline stripped occurs
 exactly 1 time in `docs/roadmap/STATUS.md`, and no STATUS line begins `- [~]`.

G4 THE TESTS — in the primary checkout with closure.diff applied, before the handback, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/cli/test_golden_path.py 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same command inside its simulated tree at C4 and read `512 passed` at real
 exit code 0, and with the accepted count left at 116, `tests/docs/` read `1 failed, 326 passed` at
 exit 1. Then `python3 -m apps.cli.main integrity check --json`, all six checks `pass` at
 `fail_count` 0.

G5 SIZES — `git show --numstat --format=` for C1 to C3, placed in the handback's `## Commits`
 table exactly as the tool printed it; C4's own numbers go in your reply.

G6 TREE, PUSH AND PULL REQUEST — after the pull request: `git status --porcelain` empty;
 `git log --oneline -n 5`, showing C4, C3, C2, C1 and `f48d56ec8`; the push's real outcome;
 the pull request's number and URL; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must hold exactly
 that one pull request, from `feature/f041-artifact-preview` into `main`, not a draft. These go in
 your reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, and AGENTS.md's
item-status table with one row per commit and per gate: the state block, the per-commit
changed-files table with the insertions git MEASURED beside the ones this block expected, every
gate's real output and exit code, the authored-text proofs, the deviations, and the next action.
Your Session section reads SESSION 2 of feature F041, round 9, rounds so far 9, and says in one
sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), then the Open PR
Gate, which merges this feature's pull request in the NEXT feature's session and never in this
one, then Rule A5, the first unchecked feature in `docs/roadmap/STATUS.md`. State the
open-findings count, 0, and the operator-questions count, 1.
