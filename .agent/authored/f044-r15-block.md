STEP F044 R15 — THE CLOSING ROUND: BOOK ROUND 14, CLOSE R-1116, ROTATE, ACCEPT F044, OPEN THE PULL REQUEST

GOAL
Book round 14's PASS and a reviewer-authored `Done:` line closing finding `R-1116` (fixed seven
rounds ago, never formally closed — see the block's own PAYLOADS note below); rotate the finding
ledger into its archive; flip F044's STATUS line to `[x]` with the README's accepted count, the
Tier 5 row (Done 37 of 37) and a feature paragraph, and the self-use queue's one `consumed_by` edit
for `SU-039` (closure precondition 6), in the same commit; and open the pull request into `main`.
`R-1117` stays open, already carrying `Owner: F290`, so nothing is re-assigned. This closes F044.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f044-r15-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  every other `.remedy-wt/f044-*` path   The reviewer's; do not touch.
  `.remedy-wt/f044-r15-worker/`    YOURS for logs and scripts; create it if absent. Gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, `ln`, `npm ci`, `npm install`, process substitution,
`cd <dir> && git ...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`.
Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C <path>` rather than
`cd`. Put multi-step code in a scratch Python file under your directory. The `remedy` CLI may be
denied: run `python3 -m apps.cli.main ...`. Never use `git stash` in any form.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`: report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f044-command-palette`, and `git log --oneline -1` must read `273b0da6a`.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f044-r15-payloads/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found (the reviewer read 11), and
   `gh pr list --state open --json number,headRefName`, which must read `[]`.

PAYLOADS — under `.remedy-wt/f044-r15-payloads/`, lines = newline count. Verify each BEFORE using
it and report every reading.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 12 | 10126 | 84a9b9e67d9d7be0c2ccb6f3b12b1c617b19c662c1cb43a1801d087b3941b451 |
| plan.md | 31 | 1122 | 51e7dc0e8e5baa1adf7086c0cb6f59d67f6239ee533eb24bb7c36e567a6e7fdc |
| closure.diff | 67 | 5253 | 3b34cd37213a892cf02fc3456630efecdc6fead4d390d52a196eaa25f2f52b12 |
| status_line.txt | 1 | 462 | 44100205a1b68840c5364176d7517dfc8d8aa27851af2f6e8f17a52687973f77 |
| pr_body.md | 145 | 9345 | 5dc1ab506b06f45cabc96cf13c6a67f7e28bb126f42d39e64d0d282fa019df64 |

`records.diff` appends TWO things to `.agent/live_review.md` in one hunk: the `Gate: F044 R14 —`
paragraph, and a reviewer-authored `Done: R-1116 —` line. THIS SECOND PART NEEDS EXPLANATION,
BECAUSE IT LOOKS LIKE IT SHOULD HAVE HAPPENED SEVEN ROUNDS AGO AND DID NOT. Finding `R-1116` (raised
at Gate F044 R7, Low severity) was fixed at commit `f48e97be9` (round 8) — both its named comments
in `packages/orchestration/ci_budgets.py` read `DECISION F044 D8` today, re-verified by this
session with a plain grep, zero remaining. But the round that fixed it wrote only a `Landed:` note,
never a reviewer-authored `Done:` line, and `scripts/rotate_live_review.py`'s own `open_finding_ids`
function — the canonical open-set reader every later round's own Gate paragraph has claimed to
quote — only closes a registration on a `Done:` line; a `Landed:` note does not count, by that
function's own docstring and by six other ids' own archived text saying so in as many words
("NOT RESOLVED: only reviewer-authored `Done:` text closes it"). So `R-1116` has read OPEN in the
mechanical count since round 7, even though the code fix has been on disk, unmoved, this whole
time; every Gate paragraph from R8 through R13 said "the open set is [...]" without it, which was
wrong by omission. Nothing was ever decided on the strength of that wrong count — `high_blockers_
open` only gates on High severity, R-1116 is Low, and the closure protocol's own precondition 1 is
satisfied either way (a documented Low risk closes it as much as a `Done:` line does) — so this is
a correction to the ledger's own bookkeeping, not a repair this round is inventing work to justify.
`plan.md` REWRITES `.agent/plan.md`. `closure.diff` edits `docs/roadmap/STATUS.md`, `README.md` and
`scripts/self_use_queue.json`; its STATUS line is `status_line.txt`, whose one line it carries byte
for byte. `pr_body.md` is the pull request's body. `closure.diff` goes on with `git apply --check`
then `git apply`; the reviewer's `git apply --check` of it in the primary checkout at `273b0da6a`
checked all three files cleanly. Never retype or edit a payload.

BUNDLE — four commits, then the push and the pull request, in this order.

C1 — `.agent/authored/f044-r15-block.md` := this block; `.agent/authored/f044-r15-<name>` for each
  payload, keeping its file name. All by `shutil.copyfile`.
  Subject: `F044 R15 C1: copy round 15 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 256. Report the number you measure, and
  STOP rather than commit if it is 500 or more.
C2 — `git apply --check` then `git apply` records.diff (bytes to `.agent/live_review.md`), then
  `.agent/plan.md` := plan.md.
  Subject: `F044 R15 C2: book round 14's PASS and close R-1116 with a Done line`
  Expected by `git show --numstat` (insertions/deletions): 4/0 .agent/live_review.md, 9/9
  .agent/plan.md.
C3 — `python3 scripts/rotate_live_review.py`, and report its whole printed output; then commit
  exactly the two ledger files. The reviewer's own run of the same script over its simulated tree
  at C2 printed:
    gate records moved: 9
    finding pairs moved: 1 (2 records)
    resolved-text records moved: 1
    old ledger size: 165768 bytes
    new ledger size: 146865 bytes
    old archive size: 5771445 bytes
    new archive size: 5790349 bytes
    open findings before: 1
    open findings after: 1
    written: <your own checkout's two ledger paths>
  Subject: `F044 R15 C3: rotate the finding ledger into its archive`
  Expected: 0/23 .agent/live_review.md, 24/0 .agent/live_review_archive.md.
C4 — `git apply` closure.diff; run G4 BEFORE writing the handback; then rewrite
  `.agent/handoff.md` per `docs/agents/handback_template.md` and commit all four together.
  Subject: `F044 R15 C4: accept F044 in STATUS with its README pins and the self-use queue`
  Expected, measured before the handback joins the commit: 14/2 README.md, 1/1
  docs/roadmap/STATUS.md, 1/1 scripts/self_use_queue.json.
THEN — `git push origin feature/f044-command-palette`; then
  `gh pr create --base main --head feature/f044-command-palette --title "F044 — Command palette, keyboard, performance budget" --body-file .remedy-wt/f044-r15-payloads/pr_body.md`,
  and report its real output: the number and the URL.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f044-r15-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `.agent/live_review_archive.md`,
   `docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json` and `.agent/handoff.md`.
   Report the set you measure with `git diff --name-only 273b0da6a` after C4.
4. C4 is the LAST commit on this branch (Rule A4). If a gate goes red, STOP, commit and push what
   is verified, write an honest handoff under AGENTS.md "If Blocked", and hand back without
   creating the pull request.
5. NOTHING IS MERGED. No `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
6. Delete nothing you did not create; leave every worktree, branch and stash alone.
7. Your handback names no pull request number, which does not exist when it is written; the
   number goes in your reply.
8. Do not run the full suite; it ran in round 13 and read exit 0.

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G4 run before the handback is written; G5
and G6 after C4.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 committed `.agent/authored/f044-r15-*` blob, read with `git show <C1>:<path>`, compared byte for
 byte with its source (the block copy against `.remedy-wt/f044-r15-payloads/block.md`).

G2 THE BOOKING, THE ROTATION AND THE ACCEPTANCE — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named, equals the reviewer's simulation:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 165768 | b47872179057b32779244349f77af1f6fb300e3d459ba361faba4ec2d445c7f1 |
 | C2 | .agent/plan.md | 1122 | 51e7dc0e8e5baa1adf7086c0cb6f59d67f6239ee533eb24bb7c36e567a6e7fdc |
 | C3 | .agent/live_review.md | 146865 | 37ba4115986018b37d31326c0ac7d200892b93ca092b4bc90097745e82ef0e56 |
 | C3 | .agent/live_review_archive.md | 5790349 | 5363c5a547e9feb748c4d1afb40d518527f8683acaf5c9361011018a463c4667 |
 | C4 | README.md | 48900 | e4f7f3c595aa1b0045ba305ed0ea6fb90e870b14e2ba1f2a255e9ffcee878a8a |
 | C4 | docs/roadmap/STATUS.md | 60075 | 1af81e19655c9a68588823186146ae28fbb892fb2ccf79a2bf215866a78519a1 |
 | C4 | scripts/self_use_queue.json | 148413 | 3129334c8d8f44526d2f486bf7fed57cb602c72923bc45634cc221e988bad8a4 |
 Also: C3's path set, exactly the two ledger files; and the open set by distinct id via
 `open_finding_ids` (in `scripts/rotate_live_review.py`) over the ledger's TEXT at C2, C3 and C4,
 which the reviewer's simulation read as `['R-1117']` at each — the correction landing in THIS
 round's own C2, not a further surprise.

G3 THE STATUS LINE — at C4, the status_line.txt content with its trailing newline stripped occurs
 exactly 1 time in `docs/roadmap/STATUS.md`, and no STATUS line begins `- [~]`.

G4 THE TESTS — in the primary checkout with closure.diff applied, before the handback, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/cli/test_golden_path.py 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same command inside its own disposable simulation worktree at C4 and read
 `552 passed` at real exit code 0. Then `python3 -m apps.cli.main integrity check --json`, all six
 checks `pass` at `fail_count` 0 (the reviewer's simulated tree read the same at C4).

G5 SIZES — `git show --numstat --format=` for C1 to C3, placed in the handback's `## Commits`
 table exactly as the tool printed it; C4's own numbers go in your reply.

G6 TREE, PUSH AND PULL REQUEST — after the pull request: `git status --porcelain` empty;
 `git log --oneline -n 5`, showing C4, C3, C2, C1 and `273b0da6a`; the push's real outcome;
 the pull request's number and URL; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must hold exactly
 that one pull request, from `feature/f044-command-palette` into `main`, not a draft. These
 go in your reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, and AGENTS.md's
item-status table with one row per commit and per gate: the state block, the per-commit
changed-files table with the insertions git MEASURED beside the ones this block expected, every
gate's real output and exit code, the authored-text proofs, the deviations, and the next action.
Your Session section reads SESSION 5 of feature F044, round 15, rounds so far 15, and says in one
sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), then the Open PR
Gate, which merges this feature's pull request in the NEXT feature's session and never in this
one, then Rule A5, the first unchecked feature in `docs/roadmap/STATUS.md`. State the
open-findings count, 1 (`R-1117`, Medium, owned by F290), and the operator-questions count, 0.
--- END STEP ---
