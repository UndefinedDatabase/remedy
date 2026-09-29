STEP F291 R6 — THE CLOSING ROUND: BOOK ROUND 5, ROTATE, ACCEPT F291, OPEN THE PULL REQUEST

GOAL
Book round 5's PASS; rotate the finding ledger into its archive; flip F291's STATUS line to `[x]`
with the README's accepted count, the Tier 5 row (Done 35, and Total 37, which F291's registration
left at 36) and a Tier 5 paragraph, and the self-use queue's one `consumed_by` edit for `SU-037`
(closure precondition 6), in the same commit; and open the pull request into `main`. F291 is not a
findings-paydown feature, so nothing is registered, and no open finding is left to re-assign. This
closes F291.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f291-r6-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f291-r6/`           READ-ONLY. The reviewer's block.
  every other `.remedy-wt/f291-*` path   The reviewer's; do not touch.
  `.remedy-wt/f291-r6-worker/`    YOURS for logs and scripts; create it if absent.

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
   `feature/f291-self-use-sources-v2`, and `git log --oneline -1` must read `f246cdfe4`.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f291-r6/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found, and
   `gh pr list --state open --json number,headRefName`, which must read `[]`.

PAYLOADS — under `.remedy-wt/f291-r6-payloads/`, printed by the reviewer's builder
(lines = newline count). Verify each BEFORE using it and report every reading.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 2 | 2070 | 63e150513a3a5fdf1b71471eff1d17f4a47514a5c289639bb5c7cb37e97f7a33 |
| plan.md | 26 | 815 | 6ae85237b331594e683ea49bdd248b963a31c4ed603c45806e25ded451c04862 |
| status_line.txt | 1 | 410 | 5399db2a31cd4e6dbbc53672c7e61029859e79b9c81af85f9c2c485dde74cabc |
| closure.diff | 63 | 4363 | 72ebc0f9153df3eb81f98bd2d8027605730cd3798824ace9cd98902929d076a6 |
| pr_body.md | 51 | 3346 | c5e1a8da764150f74cc8adde998b924dab583ed934f11e0a7f2bca7524ede5c1 |

`ledger.md` is APPENDED to `.agent/live_review.md` as raw bytes (round 5's `Gate:` entry, which
begins with its own blank line). `plan.md` is a REWRITE of `.agent/plan.md`. `closure.diff` edits
`docs/roadmap/STATUS.md`, `README.md` and `scripts/self_use_queue.json`; its STATUS line is
`status_line.txt`, whose one line it carries byte for byte. `pr_body.md` is the pull request's
body. `closure.diff` goes on with `git apply --check` then `git apply`. Never retype or edit a
payload.

BUNDLE — four commits, then the push and the pull request, in this order.

C1 — `.agent/authored/f291-r6-block.md` := this block; `.agent/authored/f291-r6-<name>` for each
  payload, keeping its file name. All by `shutil.copyfile`.
  Subject: `F291 R6 C1: copy round 6 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 143. Report the number you measure, and
  STOP rather than commit if it is 500 or more.
C2 — append ledger.md to `.agent/live_review.md` (bytes to bytes), then `.agent/plan.md` := plan.md.
  Subject: `F291 R6 C2: book round 5's PASS, the package READY_FOR_REVIEW`
  Expected by `git show --numstat` (insertions/deletions): 2/0 .agent/live_review.md, 7/7 .agent/plan.md.
C3 — `python3 scripts/rotate_live_review.py`, and report its whole printed output; then commit
  exactly the two ledger files. The reviewer's run of the same script over its simulated tree at
  C2 printed (its last line names the simulated tree's paths where yours names the checkout's):
    gate records moved: 11
    finding pairs moved: 1 (2 records)
    resolved-text records moved: 0
    old ledger size: 147574 bytes
    new ledger size: 119226 bytes
    old archive size: 5729902 bytes
    new archive size: 5758250 bytes
    open findings before: 0
    open findings after: 0
    written: /home/decodeux/Repos/remedy/.remedy-wt/f291-r6-sim/.agent/live_review.md and /home/decodeux/Repos/remedy/.remedy-wt/f291-r6-sim/.agent/live_review_archive.md
  Subject: `F291 R6 C3: rotate the finding ledger into its archive`
  Expected: 0/26 .agent/live_review.md, 26/0 .agent/live_review_archive.md.
C4 — `git apply` closure.diff; run G4 BEFORE writing the handback; then rewrite
  `.agent/handoff.md` per `docs/agents/handback_template.md` and commit all four together.
  Subject: `F291 R6 C4: accept F291 in STATUS with its README pins and the self-use queue`
  Expected, measured before the handback joins the commit: 10/2 README.md, 1/1 docs/roadmap/STATUS.md, 1/1 scripts/self_use_queue.json.
THEN — `git push origin feature/f291-self-use-sources-v2`; then
  `gh pr create --base main --head feature/f291-self-use-sources-v2 --title "F291 — Self-use sources v2" --body-file .remedy-wt/f291-r6-payloads/pr_body.md`,
  and report its real output: the number and the URL.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f291-r6-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `.agent/live_review_archive.md`,
   `docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json` and `.agent/handoff.md`.
   Report the set you measure with `git diff --name-only f246cdfe4` after C4.
4. C4 is the LAST commit on this branch (Rule A4). If a gate goes red, STOP, commit and push what
   is verified, write an honest handoff under AGENTS.md "If Blocked", and hand back without
   creating the pull request.
5. NOTHING IS MERGED. No `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
6. Delete nothing you did not create; leave every worktree, branch and stash alone.
7. Your handback names no pull request number, which does not exist when it is written; the
   number goes in your reply.
8. Do not run the full suite; it ran in round 4 and read exit 0.

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G4 run before the handback is written; G5
and G6 after C4.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 committed `.agent/authored/f291-r6-*` blob, read with `git show <C1>:<path>`, compared byte for
 byte with its source (the block copy against `.remedy-wt/f291-r6/block.md`). One reading per file.

G2 THE BOOKING, THE ROTATION AND THE ACCEPTANCE — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named (the C4 rows from the working tree before the
 handback joins the commit), equals the reviewer's simulation:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 147574 | 5146a69ab7f99dd8fc21856e468ba8e1a427880daf74fb91d9e78ba50836e943 |
 | C2 | .agent/plan.md | 815 | 6ae85237b331594e683ea49bdd248b963a31c4ed603c45806e25ded451c04862 |
 | C3 | .agent/live_review.md | 119226 | 8b9bb7636baae546f242bcab191aed14d6b8f97854c4f17be408cef61c537c13 |
 | C3 | .agent/live_review_archive.md | 5758250 | 50a6d371f0e077f803ca521345bb9f9f1f69d31cf4e3936e9d5f4e9a0d9dd200 |
 | C4 | README.md | 47045 | ca760911c087576050b4b125148f2fccc7b7c14b90839bb611669ca4f2c56a91 |
 | C4 | docs/roadmap/STATUS.md | 59240 | 2359ed20e74340db2bd48f04dc507d8167ce9823136f9e4241ed0ee1b6eda144 |
 | C4 | scripts/self_use_queue.json | 145556 | 50ba966d9f64e888b70a0fdab1fc0e62ead6d43994c54d6323fbf977460670c5 |
 Also: C3's path set, exactly the two ledger files; and the open set by distinct id via
 `open_finding_ids` over the ledger's TEXT at C2, C3 and C4, which the reviewer's simulation read
 as empty at each.

G3 THE STATUS LINE — at C4, the status_line.txt content with its trailing newline stripped occurs
 exactly 1 time in `docs/roadmap/STATUS.md`, and no STATUS line begins `- [~]`.

G4 THE TESTS — in the primary checkout with closure.diff applied, before the handback, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/cli/test_golden_path.py 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same command inside its simulated tree at C4 and read `552 passed` at real
 exit code 0, and with the accepted count left at 118, `tests/docs/` read `1 failed, 326 passed` at
 exit 1. Then `python3 -m apps.cli.main integrity check --json`, all six checks `pass` at
 `fail_count` 0.

G5 SIZES — `git show --numstat --format=` for C1 to C3, placed in the handback's `## Commits`
 table exactly as the tool printed it; C4's own numbers go in your reply.

G6 TREE, PUSH AND PULL REQUEST — after the pull request: `git status --porcelain` empty;
 `git log --oneline -n 5`, showing C4, C3, C2, C1 and `f246cdfe4`; the push's real outcome;
 the pull request's number and URL; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must hold exactly
 that one pull request, from `feature/f291-self-use-sources-v2` into `main`, not a draft. These
 go in your reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, and AGENTS.md's
item-status table with one row per commit and per gate: the state block, the per-commit
changed-files table with the insertions git MEASURED beside the ones this block expected, every
gate's real output and exit code, the authored-text proofs, the deviations, and the next action.
Your Session section reads SESSION 1 of feature F291, round 6, rounds so far 6, and says in one
sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), then the Open PR
Gate, which merges this feature's pull request in the NEXT feature's session and never in this
one, then Rule A5, the first unchecked feature in `docs/roadmap/STATUS.md`. State the
open-findings count, 0, and the operator-questions count, 0.
