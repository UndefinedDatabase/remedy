STEP F030 R7 — THE CLOSING ROUND: book round 6, rotate the ledger, and accept F030 in STATUS with its README pins, then open the pull request

GOAL
Round 6 passed with the package READY_FOR_REVIEW. Close F030 per
`docs/roadmap/STATUS_closure_protocol.md` Algorithm steps 4 and 5: book round 6, rotate the finding
ledger, flip F030's STATUS line to `[x]` with the README's accepted count, Tier 5 Done cell and
prose in the same commit, and open the pull request. No self-use item is consumed: round 5 read
the queue exhausted, so closure precondition 6 reads `self-use NONE (queue exhausted)`.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full. You never issue a verdict and never merge. Every
change travels as a payload or is produced by the rotation script; you write only the handback.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution,
`cd <dir> && git ...`, and multi-operation one-liners chained with `;` or `&&` outside a
`bash -c`. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C <path>`
rather than `cd`, and never `cd` your shell into a worktree. Use `python3 - <<'PY'` for counting,
hashing and copying (`shutil.copyfile`); a heredoc containing a dollar-brace, or a backslash inside
an f-string, is refused or fails, so write such a script to a file under
`.remedy-wt/f030-r7-worker/`, which is yours. Never run npm or npx. `.remedy-wt/f030-r7/`,
`.remedy-wt/f030-r7-sim/` and `.remedy-wt/f030-review/` are the reviewer's and read-only. The
`remedy` command is denied; use `python3 -m apps.cli.main` where a gate names it.

COMMIT TRAILER — every commit ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop.
2. In `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain` empty,
   `git branch --show-current` `feature/f030-steering-messages`, `git log --oneline -1`
   `08685d51`.
3. Measure this block's line count and sha256 (`.remedy-wt/f030-r7/block.md`) against your
   delegation message's readings; stop if either differs.
4. Report `git worktree list | wc -l`, and `gh pr list --state open --json number,headRefName`, which
   must be EMPTY.

PAYLOADS — under `.remedy-wt/f030-r7/`, lines = newline count; verify each BEFORE use:
| file | lines | bytes | sha256 |
|---|---|---|---|
| build.py | 104 | 5845 | cf6e4fbc6eb49ccd06658ed1b16c82034b110f3d1e871bc383ae9b6c5fabcc0e |
| closure.diff | 51 | 3948 | 751220030bae40f4ff4daea4f07b40502ca5541ea840153ce6063d8e87d316be |
| ledger.md | 2 | 2220 | 239b978e118759065e4ac7128d790b616112cfee4ea3e287cc04a86aca551c3f |
| plan.md | 26 | 849 | 8f8540c9f00341c92a8543a47a43c704337036293e34da95653f7a5eba253d19 |
| pr_body.md | 84 | 5393 | d8afe076782c884a409a4c57979f4273770c30438bc02cec794add58ed83b849 |
| readme_para.txt | 8 | 732 | 5932856a107a0b80181f78abbdfb9577c70cad29457215f4dc8dfaba760670b8 |
| status_line.txt | 1 | 391 | aeef298a5746ef57d35d28e041b72376d43c0ff0f46aedacc5ed4ed4ca815cd5 |
`ledger.md` is appended to `.agent/live_review.md` byte for byte (it starts with its own blank
line); `plan.md` REWRITES `.agent/plan.md` by `shutil.copyfile`, never by retyping; `closure.diff`
flips F030's STATUS line and moves the README's accepted count, Tier 5 Done cell and prose — it goes
on with `git apply --check` then `git apply`; `status_line.txt` is the exact STATUS line closure.diff
writes, for G4's proof; `pr_body.md` is the pull request's description, passed to `gh` as a file;
`readme_para.txt` and `build.py` are the reviewer's sources for closure.diff, copied for the record
and never applied or run.

BUNDLE — C1 to C4, then the pull request.
C1 COPIES: `.agent/authored/f030-r7-block.md` := this block and each payload as
   `.agent/authored/f030-r7-<name>`, by `shutil.copyfile`. Subject `F030 R7 C1: copy round 7
   block and payloads`. Its insertions are this block's line count plus 276; STOP rather than commit
   if that reaches 500.
C2 THE BOOKING: the ledger append and the plan rewrite. Subject `F030 R7 C2: book round 6's PASS,
   the package READY_FOR_REVIEW`. Expected by `git show --numstat`: 2/0 `.agent/live_review.md`,
   4/4 `.agent/plan.md`.
C3 THE ROTATION, its own commit, paths `.agent/live_review.md` and `.agent/live_review_archive.md`
   ONLY: `python3 scripts/rotate_live_review.py`; report its printed output in full. Subject
   `F030 R7 C3: rotate the finding ledger into its archive`. Expected: 0/22
   `.agent/live_review.md`, 22/0 `.agent/live_review_archive.md`.
C4 THE CLOSURE COMMIT, exactly these paths: `docs/roadmap/STATUS.md`, `README.md` and
   `.agent/handoff.md`. `git apply` closure.diff, run G4 on the
   working tree, rewrite `.agent/handoff.md` per `docs/agents/handback_template.md` as the closure
   handback, run G5, then commit. The handback names, spelled exactly so, the package
   `remedy-review-20260927-234033-READY_FOR_REVIEW.zip`, its SHA-256
   `8b7e2f9ceaee61acc87a55ae5bd2c2b3f467b44ab3136076e34d5b3b666ea452`, its directory
   `/home/decodeux/Repos/remedy-history/zips`, the evidence job `f030r6e1001`, the accepted head
   `b32a0ab6f0809f86b0461a6aac15a4912960162c` and `self-use NONE (queue exhausted)`; and it names NO
   pull request number, which does not exist when it is written. Subject `F030 R7 C4: accept F030 in
   STATUS with its README pins`. Expected for the two applied files: 11/2
   `README.md`, 1/1 `docs/roadmap/STATUS.md`. Then `git push`.
THE PULL REQUEST, after C4 and its push: `gh pr create --base main --head
   feature/f030-steering-messages --title "F030 — Steering messages"
   --body-file .remedy-wt/f030-r7/pr_body.md`. DO NOT MERGE IT. Report its
   number and URL in your final reply only.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f030-r7-*` copies,
   `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/roadmap/STATUS.md`, `README.md` and `.agent/handoff.md`.
4. C4 is the LAST commit on this branch (Rule A4). Nothing follows it.
5. If any gate goes red, STOP before C4: commit and push what is verified, write the handoff under
   AGENTS.md "If Blocked", and hand back. A closure that cannot be proved is not closed.
6. NOTHING IS MERGED: no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
7. Delete nothing you did not create; every existing worktree and branch stays.
8. DO NOT run the full suite: this feature's run is `.agent/authored/f030-closure-suite.txt`.

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G4 run before
the handback is written, and the handback states their readings; G5 runs after the handback is
written and before C4 is committed, so its readings go in your final reply.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f030-r7-*` copy byte-equal to its source by `git show <C1>:<path>`.
G2 THE BOOKING, at C2, read with `git show <C2>:<path>`, each equal to the reviewer's simulation:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 325137 | d6558b4028cf3f510a12baea6593f71439cf7ac6b6653f2eab6c3f8617d846d8 |
   | .agent/plan.md | 849 | 8f8540c9f00341c92a8543a47a43c704337036293e34da95653f7a5eba253d19 |
   and `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger at C2 — the
   simulation read `[]`.
G3 THE ROTATION, at C3: the reviewer's simulation of `python3 scripts/rotate_live_review.py` printed,
   line for line apart from its final `written:` line, which names the simulation's own paths:
   gate records moved: 11
   finding pairs moved: 0 (0 records)
   old ledger size: 325137 bytes
   new ledger size: 297093 bytes
   old archive size: 5284442 bytes
   new archive size: 5312486 bytes
   open findings before: 0
   open findings after: 0
   and left the two ledger files at:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 297093 | 8abade92d79023af5cd6084d7554ca0b6f36781cc0e031ae9ae806587d84d2cf |
   | .agent/live_review_archive.md | 5312486 | 239c6c1bfef520232e01387c33380c28200f9a5eb64a16d6ed954cb2cc617c0c |
   Report yours beside each, and C3's path set, which is the two ledger files and nothing else.
G4 THE CLOSURE EDITS AND THE TREE, with closure.diff applied, before the handback is written:
   | path | bytes | sha256 |
   |---|---|---|
   | docs/roadmap/STATUS.md | 55903 | 012c2bedbd1cb52f89a30c9ece2ce61eb2e554f2cb24a751b1038fb0114b52e9 |
   | README.md | 40877 | 4cb87a6a5ef59c44d070103685c086e1801f3993792ea20afa6db80b9160bb1e |
   the count of lines of `docs/roadmap/STATUS.md` equal to the one line of status_line.txt, which
   must be 1; `pending_self_use_items()` from `packages.orchestration.self_use_queue`, which must be
   empty; serially,
   `bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'`,
   which the simulation read as `512 passed` at exit 0; then
   `python3 -m apps.cli.main integrity check --json`, six checks with status `pass` at `fail_count`
   0 — each check's status is the reading, not the exit code. The reviewer red-controlled both
   README pins: with the accepted count left at 110, and with the Tier 5 Done cell left at 27,
   `tests/docs/` read `1 failed, 326 passed` at exit 1 each time.
G5 THE HANDBACK'S PINS, after the handback is written and before C4 is committed: for each of the six
   strings C4 names, its count in the new `.agent/handoff.md`, each at least 1; the count of `pull/`
   in it, which must be 0; and the presence of its item-status table section.
G6 AFTER C4: `git log --oneline -n 5`, showing C4, C3, C2, C1 and `08685d51`; `git status
   --porcelain` empty; the push's real outcome; the pull request's number and URL; and `gh pr list
   --state open --json number,headRefName,baseRefName,isDraft` showing exactly that one pull request,
   from this branch into `main`, not a draft. These go in your final reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block, the
per-commit changed-files table with the `git show --numstat` counts you measured beside the ones
above, every gate reading G1 to G4 with its real exit code, the authored-text proofs, the deviations,
the next action, and — INSIDE `.agent/handoff.md` itself, as its own section — the item-status table
AGENTS.md requires, one row per commit, the pull request and each gate. Session section: SESSION 1 of
feature F030, round 7, rounds so far 7, plus one sentence on how much context you had left.
`## Next`: Phase 1 rule 1, then the Open PR Gate — the pull request this round opens is merged by the
NEXT feature's session, never by this one — then Rule A5, the first unchecked feature in
`docs/roadmap/STATUS.md`. State the open-findings count as the script reads it at C3, and "Operator
questions open: 0".
