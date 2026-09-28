STEP F038 R15 — THE CLOSING ROUND: book round 14, rotate the ledger, and accept F038 in STATUS with its README pins, then open the pull request

GOAL
Round 14 passed with the package READY_FOR_REVIEW. Close F038 per
`docs/roadmap/STATUS_closure_protocol.md` Algorithm steps 4 and 5: book round 14, rotate the finding
ledger, flip F038's STATUS line to `[x]` with the README's accepted count, Tier 5 Done cell and
prose in the same commit, and open the pull request. No self-use item is consumed: round 14 read
the queue exhausted, so closure precondition 6 reads `self-use NONE (queue exhausted)`.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full. You never issue a verdict and never merge. Every
change travels as a payload or is produced by the rotation script; you write only the handback.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution,
`cd <dir> && git ...`, and multi-operation one-liners chained with `;` or `&&` outside a
`bash -c`. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C <path>`
rather than `cd`, and never `cd` your shell into a worktree. Use `python3 - <<'PY'` for counting,
hashing and copying (`shutil.copyfile`); a heredoc containing a dollar-brace, or a brace next to a
quote, is refused, so write such a script to a file under `.remedy-wt/f038-r15-worker/`, which is
yours. Never run npm or npx. `.remedy-wt/f038-r15/`, `.remedy-wt/f038-r15-sim/`, every other
`.remedy-wt/f038-*` path and `.remedy-wt/f038-review/` are the reviewer's and read-only. The
`remedy` command is denied; use `python3 -m apps.cli.main` where a gate names it.

COMMIT TRAILER — every commit ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop.
2. In `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain` empty,
   `git branch --show-current` `feature/f038-grounded-chat`, `git log --oneline -1`
   `00102b5c0`.
3. Measure this block's line count and sha256 (`.remedy-wt/f038-r15/block.md`) against your
   delegation message's readings; stop if either differs.
4. Report `git worktree list | wc -l`, and `gh pr list --state open --json number,headRefName`, which
   must be EMPTY.

PAYLOADS — under `.remedy-wt/f038-r15/`, lines = newline count; verify each BEFORE use:
| file | lines | bytes | sha256 |
|---|---|---|---|
| build.py | 108 | 5621 | 0bbcd2d93ca92d01f4b8cd75da88325370ae263d9c093c77fed020e49fcb0525 |
| closure.diff | 55 | 4315 | 96cbce2451ee47613e5041d71f4e913a70aafe8354412419ffadb0d42dd3b3d8 |
| ledger.md | 2 | 1901 | dedc5829de05b6846c1c75a07b352964037cf2cb8898973a5ea0289e00855b2e |
| plan.md | 26 | 831 | dbd3bd2d83dfc6f411d345e4127c81c2bf50d51e933fde1f754e7ae87a61b17f |
| pr_body.md | 72 | 4098 | ff0d917fe9a871f389396286137871fec7de1bac2d5b0c2c4b6098435ef8c2dd |
| readme_para.txt | 12 | 1110 | 3d9df534db37ca3f7a698d7a085b27cdc326f807e6b572c1dde3c24a7721ada9 |
| status_line.txt | 1 | 406 | 9f99d781bb2979aea3f5d30ffdb27738d280b2c51d9ff2bd207a1af3091ad9c8 |
`ledger.md` is appended to `.agent/live_review.md` byte for byte (it starts with its own blank
line); `plan.md` REWRITES `.agent/plan.md` by `shutil.copyfile`, never by retyping; `closure.diff`
flips F038's STATUS line and moves the README's accepted count, Tier 5 Done cell and prose — it goes
on with `git apply --check` then `git apply`; `status_line.txt` is the exact STATUS line closure.diff
writes, for G4's proof; `pr_body.md` is the pull request's description, passed to `gh` as a file;
`readme_para.txt` and `build.py` are the reviewer's sources for closure.diff, copied for the record
and never applied or run.

BUNDLE — C1 to C4, then the pull request.
C1 COPIES: `.agent/authored/f038-r15-block.md` := this block and each payload as
   `.agent/authored/f038-r15-<name>`, by `shutil.copyfile`. Subject `F038 R15 C1: copy round 15
   block and payloads`. Its insertions are this block's line count plus 276; STOP rather than commit
   if that reaches 500.
C2 THE BOOKING: the ledger append and the plan rewrite. Subject `F038 R15 C2: book round 14's PASS,
   the package READY_FOR_REVIEW`. Expected by `git show --numstat`: 2/0 `.agent/live_review.md`,
   4/6 `.agent/plan.md`.
C3 THE ROTATION, its own commit, paths `.agent/live_review.md` and `.agent/live_review_archive.md`
   ONLY: `python3 scripts/rotate_live_review.py`; report its printed output in full. Subject
   `F038 R15 C3: rotate the finding ledger into its archive`. Expected: 0/46
   `.agent/live_review.md`, 46/0 `.agent/live_review_archive.md`.
C4 THE CLOSURE COMMIT, exactly these paths: `docs/roadmap/STATUS.md`, `README.md` and
   `.agent/handoff.md`. `git apply` closure.diff, run G4 on the
   working tree, rewrite `.agent/handoff.md` per `docs/agents/handback_template.md` as the closure
   handback, run G5, then commit. The handback names, spelled exactly so, the package
   `remedy-review-20260928-194656-READY_FOR_REVIEW.zip`, its SHA-256
   `98bc29b2c6aa67360bf61f1a85fb4f5583f6552100c2615c918a5b54b426bab4`, its directory
   `/home/decodeux/Repos/remedy-history/zips`, the evidence job `f038r14e1001`, the accepted head
   `2fe5345e08ad4b013b8d5a9395e5b1a83b7415f5` and `self-use NONE (queue exhausted)`; and it names NO
   pull request number, which does not exist when it is written. Subject `F038 R15 C4: accept F038 in
   STATUS with its README pins`. Expected for the two applied files: 15/2
   `README.md`, 1/1 `docs/roadmap/STATUS.md`. Then `git push`.
THE PULL REQUEST, after C4 and its push: `gh pr create --base main --head
   feature/f038-grounded-chat --title "F038 — Grounded chat & intent dispatch"
   --body-file .remedy-wt/f038-r15/pr_body.md`. DO NOT MERGE IT. Report its
   number and URL in your final reply only.

CONSTRAINTS
1. Never edit or retype a payload. `build.py` is NOT run: it would reset the reviewer's tree.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f038-r15-*` copies,
   `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/roadmap/STATUS.md`, `README.md` and `.agent/handoff.md`.
4. C4 is the LAST commit on this branch (Rule A4). Nothing follows it.
5. If any gate goes red, STOP before C4: commit and push what is verified, write the handoff under
   AGENTS.md "If Blocked", and hand back. A closure that cannot be proved is not closed.
6. NOTHING IS MERGED: no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
7. Delete nothing you did not create; every existing worktree and branch stays.
8. DO NOT run the full suite: this feature's run is `.agent/authored/f038-closure-suite.txt`.

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G4 run before
the handback is written, and the handback states their readings; G5 runs after the handback is
written and before C4 is committed, so its readings go in your final reply.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f038-r15-*` copy byte-equal to its source by `git show <C1>:<path>`.
G2 THE BOOKING, at C2, read with `git show <C2>:<path>`, each equal to the reviewer's simulation:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 363192 | b20c2c202f970aaaeb9dd4c2f7ea653df60dffc715768d6a89e3145cd1ccc3e5 |
   | .agent/plan.md | 831 | dbd3bd2d83dfc6f411d345e4127c81c2bf50d51e933fde1f754e7ae87a61b17f |
   and `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger at C2 — the
   simulation read `[]`.
G3 THE ROTATION, at C3: the reviewer's simulation of `python3 scripts/rotate_live_review.py` printed,
   line for line apart from its final `written:` line, which names the simulation's own paths:
   gate records moved: 9
   finding pairs moved: 7 (14 records)
   old ledger size: 363192 bytes
   new ledger size: 324035 bytes
   old archive size: 5380770 bytes
   new archive size: 5419927 bytes
   open findings before: 0
   open findings after: 0
   and left the two ledger files at:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 324035 | c5087b47aca9fda9700ed8cef540a96246d1d6a82732cd147ad8b52a18475d89 |
   | .agent/live_review_archive.md | 5419927 | a357195bb7858b96167692f713f194000459f6ef7b5be49ae676e244fb44c379 |
   Report yours beside each, and C3's path set, which is the two ledger files and nothing else.
G4 THE CLOSURE EDITS AND THE TREE, with closure.diff applied, before the handback is written:
   | path | bytes | sha256 |
   |---|---|---|
   | docs/roadmap/STATUS.md | 56978 | 56c05de0ae64fc7b1053a35ed2615d8993b6a73356424d0e12495208dfdb50ee |
   | README.md | 43580 | c72eb620191e93788ca6538e13b4acde7ca5854d1492eacef9d4d4ee3578d963 |
   the count of lines of `docs/roadmap/STATUS.md` equal to the one line of status_line.txt, which
   must be 1; `pending_self_use_items()` from `packages.orchestration.self_use_queue`, which must be
   empty; serially,
   `bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'`,
   which the simulation read as `512 passed` at exit 0; then
   `python3 -m apps.cli.main integrity check --json`, six checks with status `pass` at `fail_count`
   0 — each check's status is the reading, not the exit code. The reviewer red-controlled both
   README pins: with the accepted count left at 113, and with the Tier 5 Done cell left at 30,
   `tests/docs/` read `1 failed, 326 passed` at exit 1 each time.
G5 THE HANDBACK'S PINS, after the handback is written and before C4 is committed: for each of the six
   strings C4 names, its count in the new `.agent/handoff.md`, each at least 1; the count of `pull/`
   in it, which must be 0; and the presence of its item-status table section.
G6 AFTER C4: `git log --oneline -n 5`, showing C4, C3, C2, C1 and `00102b5c0`; `git status
   --porcelain` empty; the push's real outcome; the pull request's number and URL; and `gh pr list
   --state open --json number,headRefName,baseRefName,isDraft` showing exactly that one pull request,
   from this branch into `main`, not a draft. These go in your final reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block, the
per-commit changed-files table with the `git show --numstat` counts you measured beside the ones
above, every gate reading G1 to G4 with its real exit code, the authored-text proofs, the deviations,
the next action, and — INSIDE `.agent/handoff.md` itself, as its own section — the item-status table
AGENTS.md requires, one row per commit, the pull request and each gate. Session section: SESSION 3 of
feature F038, round 15, rounds so far 15, plus one sentence on how much context you had left.
`## Next`: Phase 1 rule 1, then the Open PR Gate — the pull request this round opens is merged by the
NEXT feature's session, never by this one — then Rule A5, the first unchecked feature in
`docs/roadmap/STATUS.md`; the next claim books this round's verdict. State the open-findings count
as the script reads it at C3, and "Operator questions open: 1".
