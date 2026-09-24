STEP F284 R4 — THE CLOSING ROUND: BOOK ROUND 3, CARRY R-1008, ROTATE, REGISTER F285, ACCEPT F284, OPEN THE PULL REQUEST

GOAL
Book round 3's PASS and DECISION F284 D3 with R-1008's `Owner:` line moved to F285; rotate the
finding ledger into its archive; register F285 — Findings paydown v4 after F026 under its own
Tier 2 heading with `TOTAL_FEATURES` and the README counters; flip F284's STATUS line to `[x]`
with the README's accepted count, Tier 2 Done cell and Tier 2 prose in the same commit; and open
the pull request into `main`. This closes F284.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f284-r4-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f284-r4/`           READ-ONLY. The reviewer's block, texts and builders.
  `.remedy-wt/f284-r4-dry/` and `.remedy-wt/f284-r4-sim/`  The reviewer's trees; do not touch.
  `.remedy-wt/f284-r4-worker/`    YOURS for logs and scripts; create it if absent.

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
   `feature/f284-findings-paydown-v3`, and `git log --oneline -1` must read `b6bdea3b`.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f284-r4/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f284-r4-payloads/`, printed by the reviewer's builder
(lines = newline count). Verify each BEFORE using it and report every reading.

| file | lines | bytes | sha256 |
|---|---|---|---|
| book.diff | 53 | 8866 | f2a08514f6f4cac7b592f469cd335846d7cb5a6ddc8e26e3c1107ece60d1dea5 |
| plan.md | 29 | 957 | 73a718b3b590420436648a5db3a3cd35c3560c68fa1da1aeddf6581e9b184c60 |
| register.diff | 99 | 4848 | 23cc562a764835f56010e29d6959f0ff9779dab58d2c36d72980ffca61dc1867 |
| status_line.txt | 1 | 426 | 761589baa99cd8e4a8685506dcdc032abab820887ca151c358f0285819574fc0 |
| closure.diff | 49 | 2722 | 7304cd9a38871b952aabf90c51afa92ffa68b591a3d96f860c7877f5b0d87ae4 |
| pr_body.md | 57 | 3435 | 87018ffca2064a618f48e41af5b1eda47d2ea606a7fba223ffb7b6721642f892 |

`book.diff` inserts R-1008's `Owner: F285` line and appends round 3's `Gate:` entry to
`.agent/live_review.md`, and appends DECISION F284 D3 to `.agent/decisions.md`. `plan.md` is a
REWRITE of `.agent/plan.md`. `register.diff` adds `docs/roadmap/features/T2_F285.md` and edits
`docs/roadmap/STATUS.md`, `tests/docs/test_docs_consistency.py` and `README.md`. `closure.diff`
edits `docs/roadmap/STATUS.md` and `README.md`; its STATUS line is `status_line.txt`, whose one
line it carries byte for byte. `pr_body.md` is the pull request's body. Every `.diff` goes on
with `git apply --check` then `git apply`. Never retype or edit a payload.

BUNDLE — five commits, then the push and the pull request, in this order.

C1 — `.agent/authored/f284-r4-block.md` := this block; `.agent/authored/f284-r4-<name>` for each
  payload, keeping its file name. All by `shutil.copyfile`.
  Subject: `F284 R4 C1: copy round 4 block and payloads into .agent/authored/`
  Expected insertions: 462 (this block's 174 lines plus 288 for the payloads). Report the number you measure, and STOP rather than commit if it
  is 500 or more.
C2 — `git apply` book.diff, then `.agent/plan.md` := plan.md.
  Subject: `F284 R4 C2: book round 3's PASS, carry R-1008 to F285, record D3`
  Expected by `git show --numstat` (insertions/deletions): 27/0 .agent/decisions.md, 3/0 .agent/live_review.md, 10/10 .agent/plan.md.
C3 — `python3 scripts/rotate_live_review.py`, and report its whole printed output; then commit
  exactly the two ledger files. The reviewer's run of the same script over its simulated tree at
  C2 printed:
    gate records moved: 9
    finding pairs moved: 3 (6 records)
    old ledger size: 313847 bytes
    new ledger size: 286104 bytes
    old archive size: 4940878 bytes
    new archive size: 4968621 bytes
    open findings before: 1
    open findings after: 1
  Subject: `F284 R4 C3: rotate the finding ledger into its archive`
  Expected: 0/33 .agent/live_review.md, 33/0 .agent/live_review_archive.md.
C4 — `git apply` register.diff.
  Subject: `F284 R4 C4: register F285 — Findings paydown v4 under amend0911-feedback rule B: feature file, STATUS line, pin 285, README counters`
  Expected: 2/2 README.md, 7/0 docs/roadmap/STATUS.md, 38/0 docs/roadmap/features/T2_F285.md, 5/1 tests/docs/test_docs_consistency.py.
C5 — `git apply` closure.diff; run G4 BEFORE writing the handback; then rewrite
  `.agent/handoff.md` per `docs/agents/handback_template.md` and commit all three together.
  Subject: `F284 R4 C5: accept F284 in STATUS with its README pins`
  Expected, measured before the handback joins the commit: 10/3 README.md, 1/1 docs/roadmap/STATUS.md.
THEN — `git push origin feature/f284-findings-paydown-v3`; then
  `gh pr create --base main --head feature/f284-findings-paydown-v3 --title "F284 — Findings paydown v3" --body-file .remedy-wt/f284-r4-payloads/pr_body.md`,
  and report its real output: the number and the URL.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f284-r4-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `.agent/live_review_archive.md`, `docs/roadmap/features/T2_F285.md`,
   `docs/roadmap/STATUS.md`, `tests/docs/test_docs_consistency.py`, `README.md` and
   `.agent/handoff.md`. Report the set you measure with `git diff --name-only b6bdea3b` after C5.
   There is no `scripts/self_use_queue.json` edit: the self-use track answered NONE at `ddcb0c33`.
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
 committed `.agent/authored/f284-r4-*` blob, read with `git show <C1>:<path>`, compared byte for
 byte with its source (the block copy against `.remedy-wt/f284-r4/block.md`). One reading per file.

G2 THE BOOKING AND THE ROTATION — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named, equals the reviewer's simulation:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/decisions.md | 2024746 | 782c10b3f412d3b37105b4260d782f349af0fde6697ef71282854df20583b53c |
 | C2 | .agent/live_review.md | 313847 | 4c102a3956082e0355bae721353d2740f43683d905ddc8d7854fa7372bbed3a2 |
 | C2 | .agent/plan.md | 957 | 73a718b3b590420436648a5db3a3cd35c3560c68fa1da1aeddf6581e9b184c60 |
 | C3 | .agent/live_review.md | 286104 | cd4468d74dd0b9033b63a2dabba574bceabfa34f58dc43316b85ff8ee960c516 |
 | C3 | .agent/live_review_archive.md | 4968621 | 12d2ed99739cbae2e8d3d69bbdb270d4e81bb9a2f4866e64cc6c2563fe4b775b |
 | C4 | README.md | 28679 | 1e1009a855b6c2893d8699b3fbd94489207a2f6f5e3c3b0184130a2957416817 |
 | C4 | docs/roadmap/STATUS.md | 50642 | b33d5c3118fba723444d1ee11dcf8be546cae4cbfc815ce5606e1e53bcdd992c |
 | C4 | docs/roadmap/features/T2_F285.md | 2246 | 107bde79ad79fa89710788007e22a6ad584dfddf31d36fa6f486acf74e9f5165 |
 | C4 | tests/docs/test_docs_consistency.py | 95239 | 66dc35c0e8a5a8343e46210ed0529bb4486c40429d4b3e272b2c6fe776216fef |
 | C5 | README.md | 29228 | 5c871d3fbd99729a520d0ba0384c8511bd4b97f970c848bc8a1d228f6ac300f5 |
 | C5 | docs/roadmap/STATUS.md | 51033 | 6302d2d31fe1b8c247ca3f6b08b88df7eef2b06b58400cd14634ac44a2e65708 |
 The C5 rows are read from the working tree before the handback joins the commit. Also:
 among the lines C2's diff ADDS to `.agent/live_review.md`, those beginning `Owner: F285 — ` and
 `Gate: F284 R3 — `, 1 each; C3's path set, exactly the two ledger files; and the open set by
 distinct id via `open_finding_ids` over the ledger's TEXT at `b6bdea3b`, C2, C3 and C5, which
 the reviewer's simulation read as R-1008 alone at each.

G3 THE STATUS LINE — at C5, the status_line.txt content with its trailing newline stripped occurs
 exactly 1 time in `docs/roadmap/STATUS.md`, and no STATUS line begins `- [~]`.

G4 THE TESTS — in the primary checkout with closure.diff applied, before the handback, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same command inside its simulated tree at C5 and read `437 passed, 1 skipped` at real exit code 0. Then
 `python3 -m apps.cli.main integrity check --json`, all six checks `pass` at `fail_count` 0, and
 `python3 -m apps.cli.main integrity block .remedy-wt/f284-r4/block.md`, real exit code 0 with
 every item `[OK]`.

G5 SIZES — `git show --numstat --format=` for C1 to C4, placed in the handback's `## Commits`
 table exactly as the tool printed it; C5's own numbers go in your reply.

G6 TREE, PUSH AND PULL REQUEST — after the pull request: `git status --porcelain` empty;
 `git log --oneline -n 6`, showing C5, C4, C3, C2, C1 and `b6bdea3b`; the push's real outcome;
 the pull request's number and URL; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must hold exactly
 that one pull request, from `feature/f284-findings-paydown-v3` into `main`, not a draft. These
 go in your reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, and AGENTS.md's
item-status table with one row per commit and per gate: the state block, the per-commit
changed-files table with the insertions git MEASURED beside the ones this block expected, every
gate's real output and exit code, the authored-text proofs, the deviations, and the next action.
Your Session section reads SESSION 1 of feature F284, round 4, and says in one sentence how much
context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), then the Open PR
Gate, which merges this feature's pull request in the NEXT feature's session and never in this
one, then Rule A5, the first unchecked feature in `docs/roadmap/STATUS.md`. State the
open-findings count, 1, and the operator-questions count, 3.
