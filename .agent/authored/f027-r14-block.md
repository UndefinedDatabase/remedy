STEP F027 R14 — THE CLOSING ROUND: BOOK ROUND 13, ROTATE THE LEDGER, ACCEPT F027 IN STATUS WITH ITS README PINS, OPEN THE PULL REQUEST

GOAL
Book round 13's PASS, rotate the finding ledger into its archive, flip F027's STATUS line to `[x]`
with the README's accepted count, Tier 5 Done cell and Tier 5 prose in the same commit, and open the
pull request into `main`. No finding is open, so there is no ownership step; F027 is not a
findings-paydown feature, so it registers nothing; and its self-use track read
`self-use NONE (queue exhausted)`, so no `consumed_by` is edited.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, write the handback. You never issue a
verdict and never merge. Read first `.agent/authored/f026-r8-block.md`, which this round follows, and
`docs/roadmap/STATUS_closure_protocol.md` algorithm steps 4 and 5.

THE DIRECTORIES
  `.remedy-wt/f027-r14/`          READ-ONLY. This block, its payloads and the reviewer's builder.
  `.remedy-wt/f027-r14-worker/`   YOURS for logs and scripts; create it if absent. Both gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR: `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`,
`cp`, process and command substitution, `cd <dir> && git ...`, and one-liners chained with `;` or
`&&` outside a `bash -c`. Capture exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C
<path>`; never `cd` into a worktree. Copy and hash with python (`shutil.copyfile`). Never run npm or
npx, never `git stash`, never delete a branch.

COMMIT TRAILER — every commit ends with exactly this line:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop.
2. In `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain` empty,
   `git branch --show-current` `feature/f027-task-veto`, `git log --oneline -1` `409f285e`.
3. Measure this block's line count and sha256 (`.remedy-wt/f027-r14/block.md`) against your
   delegation message's readings; stop if either differs.
4. Report `git worktree list | wc -l`, and `gh pr list --state open --json number,headRefName`, which
   must be EMPTY.

PAYLOADS — under `.remedy-wt/f027-r14/`, lines = newline count; verify each BEFORE use:
| file | lines | bytes | sha256 |
|---|---|---|---|
| build.py | 96 | 5231 | 68199f3ceac279a4633c0f1b36f685e76e144acef4c1b10be2d5076d8c4070e9 |
| closure.diff | 58 | 3250 | 3baf6e021f457fcbe19c2ef40dabc798c2b5345e6be55516d69553f48c73501d |
| ledger.md | 2 | 2157 | 4ff7d7b9b67a3c680cce2b6c66b6ddedb71c1e10bc074a644d0e0a993f4cde6e |
| plan.md | 25 | 790 | fe5531980cf69bbfce067ef61dff82ff84687106fa92b997756ef9e6eab5c80c |
| pr_body.md | 80 | 5287 | 5274110b3b9d8a86a75d98189e85364a0c17b445ea05717319638f4999ce01c1 |
| readme_para.txt | 15 | 1175 | 6faf99f4f55a066a6187691ea70b4310017700ada360eb7f9d929c5efe74fa69 |
| status_line.txt | 1 | 384 | 6e08265fbf7c1534847239b7a939422e825bccdb8026348fb4b56c4368905dbb |
`ledger.md` is appended to `.agent/live_review.md` (it starts with its own blank line); `plan.md`
REWRITES `.agent/plan.md`; `closure.diff` flips F027's STATUS line and moves the README's accepted
count, Tier 5 Done cell and Tier 5 prose — it goes on with `git apply --check` then `git apply`;
`status_line.txt` is the exact STATUS line closure.diff writes, for G4's proof; `pr_body.md` is the
pull request's description, passed to `gh` as a file; `readme_para.txt` and `build.py` are the
reviewer's sources for closure.diff, copied for the record and never applied or run.

BUNDLE — C1 to C4, then the pull request.
C1 COPIES: `.agent/authored/f027-r14-block.md` := this block and each payload as
   `.agent/authored/f027-r14-<name>`. Subject `F027 R14 C1: copy round 14 block and payloads`. Its
   insertions are this block's line count plus 277.
C2 THE BOOKING: the ledger append and the plan rewrite. Subject `F027 R14 C2: book round 13's PASS,
   the package READY_FOR_REVIEW`. Expected by `git show --numstat`: 2/0 `.agent/live_review.md`,
   5/7 `.agent/plan.md`.
C3 THE ROTATION, its own commit, paths `.agent/live_review.md` and `.agent/live_review_archive.md`
   ONLY: `python3 scripts/rotate_live_review.py`; report its printed output in full. Subject
   `F027 R14 C3: rotate the finding ledger into its archive`. Expected: 0/44 `.agent/live_review.md`,
   44/0 `.agent/live_review_archive.md`.
C4 THE CLOSURE COMMIT, exactly these paths: `docs/roadmap/STATUS.md`, `README.md` and
   `.agent/handoff.md`. `git apply` closure.diff, run G4 on the working tree, rewrite
   `.agent/handoff.md` per `docs/agents/handback_template.md` as the closure handback, run G5, then
   commit. The handback names, spelled exactly so, the package
   `remedy-review-20260926-111715-READY_FOR_REVIEW.zip`, its SHA-256
   `abb65b1df0346c8670423a7da903e3e3c6facfc4cac4602bb5a983b47b4bd993`, its directory
   `/home/decodeux/Repos/remedy-history/zips`, the evidence job `f027r13e1001`, the accepted head
   `f3afc333a70eae5f339fce8c18004db68a7cea1f` and the self-use reading `self-use NONE (queue
   exhausted)`; and it names NO pull request number, which does not exist when it is written. Subject
   `F027 R14 C4: accept F027 in STATUS with its README pins`. Expected for the two applied files:
   18/2 `README.md`, 1/1 `docs/roadmap/STATUS.md`. Then `git push origin feature/f027-task-veto`.
THE PULL REQUEST, after C4 and its push: `gh pr create --base main --head feature/f027-task-veto
   --title "F027 — Task veto" --body-file .remedy-wt/f027-r14/pr_body.md`. DO NOT MERGE IT. Report its
   number and URL in your final reply only.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f027-r14-*` copies,
   `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/roadmap/STATUS.md`, `README.md` and `.agent/handoff.md`.
4. C4 is the LAST commit on this branch (Rule A4). Nothing follows it.
5. If any gate goes red, STOP before C4: commit and push what is verified, write the handoff under
   AGENTS.md "If Blocked", and hand back. A closure that cannot be proved is not closed.
6. NOTHING IS MERGED: no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
7. Delete nothing you did not create; every existing worktree and branch stays.
8. DO NOT run the full suite: this feature's run is `.agent/authored/f027-closure-suite.txt`.

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G4 run before
the handback is written, and the handback states their readings; G5 runs after the handback is
written and before C4 is committed, so its readings go in your final reply.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f027-r14-*` payload copy byte-equal to its source by `git show <C1>:<path>`.
G2 THE BOOKING, at C2, read with `git show <C2>:<path>`, each equal to the reviewer's simulation:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 342420 | a63745e6d557d14cb2d50f4a48217225cf908592e3c2cfbd955d15aada278352 |
   | .agent/plan.md | 790 | fe5531980cf69bbfce067ef61dff82ff84687106fa92b997756ef9e6eab5c80c |
   and `open_finding_ids` over the ledger at C2 — the simulation read `[]`.
G3 THE ROTATION, at C3: the reviewer's simulation of `python3 scripts/rotate_live_review.py` printed,
   line for line apart from its final `written:` line, which names the simulation's own paths:
   gate records moved: 6
   finding pairs moved: 8 (16 records)
   old ledger size: 342420 bytes
   new ledger size: 312373 bytes
   old archive size: 5123415 bytes
   new archive size: 5153462 bytes
   open findings before: 0
   open findings after: 0
   and left the two ledger files at:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 312373 | 0e122a516762d45a097966e746744f8fd12bd555957f90a10300d9978658d61e |
   | .agent/live_review_archive.md | 5153462 | 23bf3572867a6976b136185e9986a6056ae5383e6dc1a4abbeb607364f4ef173 |
   Report yours beside each, and C3's path set, which is the two ledger files and nothing else.
G4 THE CLOSURE EDITS AND THE TREE, with closure.diff applied, before the handback is written:
   | path | bytes | sha256 |
   |---|---|---|
   | docs/roadmap/STATUS.md | 53796 | e2fb757b78eef06fa160f45ef979530bb7184eb033cfad06da62693c5b9fe347 |
   | README.md | 36427 | 89d76e2859443841f92e156ed7dc3f130140941097cea6002a048999bd70523d |
   the count of lines of `docs/roadmap/STATUS.md` equal to the one line of status_line.txt, which
   must be 1; serially, `python3 -m pytest -q -p no:cacheprovider tests/docs/
   tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py
   tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py
   tests/cli/test_golden_path.py`, which the simulation read WITHOUT the golden path as `427 passed`
   at exit 0; then `python3 -m apps.cli.main integrity check --json`, six `pass` at `fail_count` 0.
   The reviewer red-controlled both pins: with the accepted count left at 105, and with the Tier 5
   Done cell left at 22, `tests/docs/` read `1 failed, 326 passed` at exit 1 each time.
G5 THE HANDBACK'S PINS, after the handback is written and before C4 is committed: for each of the six
   strings C4 names, its count in the new `.agent/handoff.md`, each at least 1; and the count of
   `pull/` in it, which must be 0.
G6 AFTER C4: `git log --oneline -n 5`, showing C4, C3, C2, C1 and `409f285e`; `git status
   --porcelain` empty; the push's real outcome; the pull request's number and URL; and `gh pr list
   --state open --json number,headRefName,baseRefName,isDraft` showing exactly that one pull request,
   from this branch into `main`, not a draft. These go in your final reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block, the
per-commit changed-files table with the `git show --numstat` counts you measured beside the ones
above, every gate reading G1 to G4 with its real exit code, the authored-text proofs, the item-status
table AGENTS.md requires (one row per commit, the pull request and each gate), the deviations, and
the next action. Session section: SESSION 2 of feature F027, round 14, plus one sentence on how much
context you had left. `## Next`: Phase 1 rule 1, then the Open PR Gate — the pull request this round
opens is merged by the NEXT feature's session, never by this one — then Rule A5, the first unchecked
feature in `docs/roadmap/STATUS.md`. State the open-findings count as the script reads it at C3, and
"Operator questions open: 5".
