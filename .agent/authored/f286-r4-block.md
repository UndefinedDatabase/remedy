STEP F286 R4 — THE CLOSING ROUND: BOOK ROUND 3, ROTATE, REGISTER F290, ACCEPT F286, OPEN THE PULL REQUEST

GOAL
Book round 3's PASS; rotate the finding ledger into its archive; register F290 — Findings paydown
v6 after F200 under its own Tier 2 heading with `TOTAL_FEATURES` and the README counters (operator
amendment amend0911-feedback rule B); flip F286's STATUS line to `[x]` with the README's accepted
count, Tier 2 Done cell and Tier 2 prose in the same commit; and open the pull request into `main`.
The closure's self-use reading was `None` (queue exhausted), so no queue entry changes. This closes
F286.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f286-r4-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f286-r4/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f286-r4-drafts/`, `.remedy-wt/f286-r4-sim/` and every other `.remedy-wt/f286-*`
  path   The reviewer's; do not touch.
  `.remedy-wt/f286-r4-worker/`    YOURS for logs and scripts; create it if absent.

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
   `feature/f286-findings-paydown-v5`, and `git log --oneline -1` must read `ea1851750`.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f286-r4/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found, and
   `gh pr list --state open --json number,headRefName`, which must read `[]`.

PAYLOADS — under `.remedy-wt/f286-r4-payloads/`, printed by the reviewer's builder
(lines = newline count). Verify each BEFORE using it and report every reading.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 2 | 1762 | 901e5d2b54c5cf2f066ddcd58d120f081611f39c86c579fa123980891df07f43 |
| plan.md | 23 | 626 | 1300c7f3f0431d4da3ba6912e20b717664d41941cdf238cf2c5fdea771e37123 |
| register.diff | 98 | 4689 | 1b65f45df184bb28e60cf2c1effd07c341cac98294653ff71f1d2c015b9bcecb |
| status_line.txt | 1 | 403 | cecff0c7b32f1355d500a4aa53f1a776cf91fa44f2a9f02d0c26c546576f0388 |
| closure.diff | 47 | 2431 | d7482236e613c51c807c44b0f3d0ce32b1d06f099304e2845016df3c85f7927e |
| pr_body.md | 51 | 2402 | 90703ae0fc6102018e1f69d9ed1c82461abebd26bc9edce37b5dac9a32d8751c |

`ledger.md` is APPENDED to `.agent/live_review.md` as raw bytes (round 3's `Gate:` entry, which
begins with its own blank line). `plan.md` is a REWRITE of `.agent/plan.md`. `register.diff` adds
`docs/roadmap/features/T2_F290.md` and edits `docs/roadmap/STATUS.md`,
`tests/docs/test_docs_consistency.py` and `README.md`. `closure.diff` edits
`docs/roadmap/STATUS.md` and `README.md`; its STATUS line is `status_line.txt`, whose one line it
carries byte for byte. `pr_body.md` is the pull request's body. Every `.diff` goes on with
`git apply --check` then `git apply`. Never retype or edit a payload.

BUNDLE — five commits, then the push and the pull request, in this order.

C1 — `.agent/authored/f286-r4-block.md` := this block; `.agent/authored/f286-r4-<name>` for each
  payload, keeping its file name. All by `shutil.copyfile`.
  Subject: `F286 R4 C1: copy round 4 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 222. Report the number you measure, and STOP
  rather than commit if it is 500 or more.
C2 — append ledger.md to `.agent/live_review.md` (bytes to bytes), then `.agent/plan.md` := plan.md.
  Subject: `F286 R4 C2: book round 3's PASS, the package READY_FOR_REVIEW`
  Expected by `git show --numstat` (insertions/deletions): 2/0 .agent/live_review.md, 4/5 .agent/plan.md.
C3 — `python3 scripts/rotate_live_review.py`, and report its whole printed output; then commit
  exactly the two ledger files. The reviewer's run of the same script over its simulated tree at
  C2 printed (its last line names the simulated tree's paths where yours names the checkout's):
    gate records moved: 13
    finding pairs moved: 1 (2 records)
    old ledger size: 325851 bytes
    new ledger size: 293209 bytes
    old archive size: 5475419 bytes
    new archive size: 5508061 bytes
    open findings before: 0
    open findings after: 0
    written: /home/decodeux/Repos/remedy/.remedy-wt/f286-r4-sim/.agent/live_review.md and /home/decodeux/Repos/remedy/.remedy-wt/f286-r4-sim/.agent/live_review_archive.md
  Subject: `F286 R4 C3: rotate the finding ledger into its archive`
  Expected: 0/30 .agent/live_review.md, 30/0 .agent/live_review_archive.md.
C4 — `git apply` register.diff.
  Subject: `F286 R4 C4: register F290 — Findings paydown v6 under amend0911-feedback rule B: feature file, STATUS line, pin 290, README counters`
  Expected: 2/2 README.md, 7/0 docs/roadmap/STATUS.md, 37/0 docs/roadmap/features/T2_F290.md, 5/1 tests/docs/test_docs_consistency.py.
C5 — `git apply` closure.diff; run G4 BEFORE writing the handback; then rewrite
  `.agent/handoff.md` per `docs/agents/handback_template.md` and commit all three together.
  Subject: `F286 R4 C5: accept F286 in STATUS with its README pins`
  Expected, measured before the handback joins the commit: 8/3 README.md, 1/1 docs/roadmap/STATUS.md.
THEN — `git push origin feature/f286-findings-paydown-v5`; then
  `gh pr create --base main --head feature/f286-findings-paydown-v5 --title "F286 — Findings paydown v5" --body-file .remedy-wt/f286-r4-payloads/pr_body.md`,
  and report its real output: the number and the URL.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f286-r4-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `.agent/live_review_archive.md`,
   `docs/roadmap/features/T2_F290.md`, `docs/roadmap/STATUS.md`,
   `tests/docs/test_docs_consistency.py`, `README.md` and `.agent/handoff.md`. Report the set you
   measure with `git diff --name-only ea1851750` after C5. `scripts/self_use_queue.json` does not
   change.
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
 committed `.agent/authored/f286-r4-*` blob, read with `git show <C1>:<path>`, compared byte for
 byte with its source (the block copy against `.remedy-wt/f286-r4/block.md`). One reading per file.

G2 THE BOOKING, THE ROTATION AND THE REGISTRATION — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named (the C5 rows from the working tree before the
 handback joins the commit), equals the reviewer's simulation:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 325851 | c0fc38ef5d221883c98d5385df6e458fa50ea661c95b171b9dab4c61bd8096a4 |
 | C2 | .agent/plan.md | 626 | 1300c7f3f0431d4da3ba6912e20b717664d41941cdf238cf2c5fdea771e37123 |
 | C3 | .agent/live_review.md | 293209 | 00f885dbe198336a76ffc78bd4f1d7d58af598b381f421c7ca5256461ba900f8 |
 | C3 | .agent/live_review_archive.md | 5508061 | 34ab5296dc8daecc84d0e6419a6aedd0a50c6c7376118145da073d9d350e4780 |
 | C4 | README.md | 44495 | da45fca1b0684bf3bf4a2e652e220487aa0b8e91832f4e9a7be08e91b3695f06 |
 | C4 | docs/roadmap/STATUS.md | 57540 | cb2f70c79d9c46888368d5ec11c5cb9c0867b290fb6e62b11e0cb5191080b90e |
 | C4 | docs/roadmap/features/T2_F290.md | 2128 | bc22312fdfd41e3e5b3d19ec3ad1acad6d940205df349fec7d44250f3a3a7555 |
 | C4 | tests/docs/test_docs_consistency.py | 96307 | 88a11093377748408476fcda5801f2eb3836e58b2753319185953eb467370162 |
 | C5 | README.md | 44846 | 7cd5df08ad311a76317e64d128e763dd500df6ba2f122bc06b5dc1f2a71290a4 |
 | C5 | docs/roadmap/STATUS.md | 57908 | 85e9fcc56c2df573f4fdf8f763750c0f7c6403e0d58f057016ec98a23247d471 |
 Also: C3's path set, exactly the two ledger files; and the open set by distinct id via
 `open_finding_ids` over the ledger's TEXT at C2, C3 and C5, which the reviewer's simulation read
 as empty at each.

G3 THE STATUS LINE — at C5, the status_line.txt content with its trailing newline stripped occurs
 exactly 1 time in `docs/roadmap/STATUS.md`, no STATUS line begins `- [~]`, and the line
 `- [ ] F290 — Findings paydown v6` occurs exactly once, directly under a line reading
 `## Tier 2 — Findings paydown (rolling, operator rule amend0911-feedback)` and a blank line.

G4 THE TESTS — in the primary checkout with closure.diff applied, before the handback, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/cli/test_golden_path.py 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same command inside its simulated tree at C5 and read `512 passed` at real
 exit code 0, and with the accepted count left at 115, or the Tier 2 Done cell left at 38,
 `tests/docs/` read `1 failed, 326 passed` at exit 1. Then
 `python3 -m apps.cli.main integrity check --json`, all six checks `pass` at `fail_count` 0.

G5 SIZES — `git show --numstat --format=` for C1 to C4, placed in the handback's `## Commits`
 table exactly as the tool printed it; C5's own numbers go in your reply.

G6 TREE, PUSH AND PULL REQUEST — after the pull request: `git status --porcelain` empty;
 `git log --oneline -n 6`, showing C5, C4, C3, C2, C1 and `ea1851750`; the push's real outcome;
 the pull request's number and URL; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must hold exactly
 that one pull request, from `feature/f286-findings-paydown-v5` into `main`, not a draft. These
 go in your reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, and AGENTS.md's
item-status table with one row per commit and per gate: the state block, the per-commit
changed-files table with the insertions git MEASURED beside the ones this block expected, every
gate's real output and exit code, the authored-text proofs, the deviations, and the next action.
Your Session section reads SESSION 1 of feature F286, round 4, rounds so far 4, and says in one
sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), then the Open PR
Gate, which merges this feature's pull request in the NEXT feature's session and never in this
one, then Rule A5, the first unchecked feature in `docs/roadmap/STATUS.md`. State the
open-findings count, 0, and the operator-questions count, 1.
