STEP F285 R6 — THE CLOSING ROUND: BOOK ROUND 5, ROTATE, REGISTER F286, ACCEPT F285, OPEN THE PULL REQUEST

GOAL
Book round 5's PASS; rotate the finding ledger into its archive; register F286 — Findings paydown
v5 after F035 under its own Tier 2 heading with `TOTAL_FEATURES` and the README counters (operator
amendment amend0911-feedback rule B); flip F285's STATUS line to `[x]` with the README's accepted
count, Tier 2 Done cell and Tier 2 prose and `SU-032`'s `consumed_by` in the same commit; and open
the pull request into `main`. This closes F285.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f285-r6-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f285-r6/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f285-r6-drafts/` and `.remedy-wt/f285-r6-sim/`  The reviewer's; do not touch.
  `.remedy-wt/f285-r6-worker/`    YOURS for logs and scripts; create it if absent.

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
   `feature/f285-findings-paydown-v4`, and `git log --oneline -1` must read `2a8bf593`.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f285-r6/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f285-r6-payloads/`, printed by the reviewer's builder
(lines = newline count). Verify each BEFORE using it and report every reading.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 2 | 2078 | 5ef40a3fd49483eed6ca5c1684417d071f8ce0b49f8ebabdf08ce091646f606f |
| plan.md | 26 | 834 | 567fbefd32531eb078836426e3133437cf158e48f028dbec4670b547bcfac7ec |
| register.diff | 97 | 4664 | 03fb310e9c521c1e73f66ef61048c7e2e2aae5b5a429eb9ef6bcd774cb1cd787 |
| status_line.txt | 1 | 434 | cc838d33b288a10b016d3f1fbd1ec2fda9b41497461ff4a7a7f14ff67f7a7f34 |
| closure.diff | 65 | 6841 | c8aced1293d64511e3b27c7e4e0b51c5a4503c900b46c28433de17b589b082f2 |
| pr_body.md | 62 | 3571 | 3f92ef935d43be6bd95455329ac623e92e225b0a6978d3490435ed1e701c03c2 |

`ledger.md` is APPENDED to `.agent/live_review.md` as raw bytes (round 5's `Gate:` entry, which
begins with its own blank line). `plan.md` is a REWRITE of `.agent/plan.md`. `register.diff` adds
`docs/roadmap/features/T2_F286.md` and edits `docs/roadmap/STATUS.md`,
`tests/docs/test_docs_consistency.py` and `README.md`. `closure.diff` edits
`docs/roadmap/STATUS.md`, `README.md` and `scripts/self_use_queue.json`; its STATUS line is
`status_line.txt`, whose one line it carries byte for byte. `pr_body.md` is the pull request's body.
Every `.diff` goes on with `git apply --check` then `git apply`. Never retype or edit a payload.

BUNDLE — five commits, then the push and the pull request, in this order.

C1 — `.agent/authored/f285-r6-block.md` := this block; `.agent/authored/f285-r6-<name>` for each
  payload, keeping its file name. All by `shutil.copyfile`.
  Subject: `F285 R6 C1: copy round 6 block and payloads into .agent/authored/`
  Expected insertions: 425 (this block's 172 lines plus 253 for the payloads). Report the number you measure, and STOP rather than commit if it
  is 500 or more.
C2 — append ledger.md to `.agent/live_review.md` (bytes to bytes), then `.agent/plan.md` := plan.md.
  Subject: `F285 R6 C2: book round 5's PASS, the package READY_FOR_REVIEW`
  Expected by `git show --numstat` (insertions/deletions): 2/0 .agent/live_review.md, 7/8 .agent/plan.md.
C3 — `python3 scripts/rotate_live_review.py`, and report its whole printed output; then commit
  exactly the two ledger files. The reviewer's run of the same script over its simulated tree at
  C2 printed (its last line names the simulated tree's paths where yours names the checkout's):
    gate records moved: 8
    finding pairs moved: 5 (10 records)
    old ledger size: 324183 bytes
    new ledger size: 288691 bytes
    old archive size: 5087923 bytes
    new archive size: 5123415 bytes
    open findings before: 0
    open findings after: 0
    written: /home/decodeux/Repos/remedy/.remedy-wt/f285-r6-sim/.agent/live_review.md and /home/decodeux/Repos/remedy/.remedy-wt/f285-r6-sim/.agent/live_review_archive.md
  Subject: `F285 R6 C3: rotate the finding ledger into its archive`
  Expected: 0/69 .agent/live_review.md, 69/0 .agent/live_review_archive.md.
C4 — `git apply` register.diff.
  Subject: `F285 R6 C4: register F286 — Findings paydown v5 under amend0911-feedback rule B: feature file, STATUS line, pin 286, README counters`
  Expected: 2/2 README.md, 7/0 docs/roadmap/STATUS.md, 36/0 docs/roadmap/features/T2_F286.md, 5/1 tests/docs/test_docs_consistency.py.
C5 — `git apply` closure.diff; run G4 BEFORE writing the handback; then rewrite
  `.agent/handoff.md` per `docs/agents/handback_template.md` and commit all four together.
  Subject: `F285 R6 C5: accept F285 in STATUS with its README pins and the self-use item's consumed_by`
  Expected, measured before the handback joins the commit: 13/3 README.md, 1/1 docs/roadmap/STATUS.md, 1/1 scripts/self_use_queue.json.
THEN — `git push origin feature/f285-findings-paydown-v4`; then
  `gh pr create --base main --head feature/f285-findings-paydown-v4 --title "F285 — Findings paydown v4" --body-file .remedy-wt/f285-r6-payloads/pr_body.md`,
  and report its real output: the number and the URL.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f285-r6-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `.agent/live_review_archive.md`,
   `docs/roadmap/features/T2_F286.md`, `docs/roadmap/STATUS.md`,
   `tests/docs/test_docs_consistency.py`, `README.md`, `scripts/self_use_queue.json` and
   `.agent/handoff.md`. Report the set you measure with `git diff --name-only 2a8bf593` after C5.
4. C5 is the LAST commit on this branch (Rule A4). If a gate goes red, STOP, commit and push what
   is verified, write an honest handoff under AGENTS.md "If Blocked", and hand back without
   creating the pull request.
5. NOTHING IS MERGED. No `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
6. Delete nothing you did not create; leave every worktree, branch and stash alone.
7. Your handback names no pull request number, which does not exist when it is written; the
   number goes in your reply.

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G4 run before the handback is written; G5
and G6 after C5.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 committed `.agent/authored/f285-r6-*` blob, read with `git show <C1>:<path>`, compared byte for
 byte with its source (the block copy against `.remedy-wt/f285-r6/block.md`). One reading per file.

G2 THE BOOKING, THE ROTATION AND THE REGISTRATION — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named (the C5 rows from the working tree before the
 handback joins the commit), equals the reviewer's simulation:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 324183 | 0f0e9e2921f0ff6045dd95ec53c7748d019342a26a1ac2789503aed104a74bd5 |
 | C2 | .agent/plan.md | 834 | 567fbefd32531eb078836426e3133437cf158e48f028dbec4670b547bcfac7ec |
 | C3 | .agent/live_review.md | 288691 | d00aa9357f8c19ede07788406856bdab29a8f1269c3367e504e3bf5c40dac736 |
 | C3 | .agent/live_review_archive.md | 5123415 | e3907f2dbea03ce01c555f4215dbb6e130f4a9fea781190006b35ddb3d700898 |
 | C4 | README.md | 34527 | 6600d61313c49f9ef78623506ce6da90d15074929748bc6cfa0743da2595e774 |
 | C4 | docs/roadmap/STATUS.md | 53038 | f5a559e201a1e3b61f5665144e5ee895f4dc9430f7ac7178f50aad55e8436dee |
 | C4 | docs/roadmap/features/T2_F286.md | 2066 | 1bbca7be52dae99144caf9cc84ef6cea3b2b4c9fde4dea7ec15a49acebecaa6c |
 | C4 | tests/docs/test_docs_consistency.py | 95534 | 7cc2d05690fa7925f679dab931f4c6f4229d5ea4c8a4b6161e35228822aab30b |
 | C5 | README.md | 35251 | bcf40d0ba40d0d3c83df89693fa32ca33e83d568d01106652b4d6f37a7a0ec4a |
 | C5 | docs/roadmap/STATUS.md | 53437 | c1ebf38c4766d1ab0765078d237a3dcd3f322cddd513e09ec423f3f617f5b9f7 |
 | C5 | scripts/self_use_queue.json | 135814 | 9adaabc616139429cdc1feb11ddb3d5bf2d47c512f79c31a75ee2f64763cb4dc |
 Also: C3's path set, exactly the two ledger files; and the open set by distinct id via
 `open_finding_ids` over the ledger's TEXT at C2, C3 and C5, which the reviewer's simulation read
 as empty at each.

G3 THE STATUS LINE — at C5, the status_line.txt content with its trailing newline stripped occurs
 exactly 1 time in `docs/roadmap/STATUS.md`, and no STATUS line begins `- [~]`.

G4 THE TESTS — in the primary checkout with closure.diff applied, before the handback, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/cli/test_golden_path.py 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same command inside its simulated tree at C5 and read `493 passed` at real
 exit code 0, and with the accepted count left at 104 `tests/docs/` read `1 failed, 326 passed` at exit 1.
 Then `python3 -m apps.cli.main integrity check --json`, all six checks `pass` at `fail_count` 0.

G5 SIZES — `git show --numstat --format=` for C1 to C4, placed in the handback's `## Commits`
 table exactly as the tool printed it; C5's own numbers go in your reply.

G6 TREE, PUSH AND PULL REQUEST — after the pull request: `git status --porcelain` empty;
 `git log --oneline -n 6`, showing C5, C4, C3, C2, C1 and `2a8bf593`; the push's real outcome;
 the pull request's number and URL; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must hold exactly
 that one pull request, from `feature/f285-findings-paydown-v4` into `main`, not a draft. These
 go in your reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, and AGENTS.md's
item-status table with one row per commit and per gate: the state block, the per-commit
changed-files table with the insertions git MEASURED beside the ones this block expected, every
gate's real output and exit code, the authored-text proofs, the deviations, and the next action.
Your Session section reads SESSION 1 of feature F285, round 6, and says in one sentence how much
context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), then the Open PR
Gate, which merges this feature's pull request in the NEXT feature's session and never in this
one, then Rule A5, the first unchecked feature in `docs/roadmap/STATUS.md`. State the
open-findings count, 0, and the operator-questions count, 5.
