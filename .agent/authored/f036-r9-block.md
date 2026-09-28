STEP F036 R9 — THE CLOSING ROUND: book round 8, rotate the ledger, and accept F036 in STATUS with its README pins, then open the pull request

GOAL
Round 8 passed with the package READY_FOR_REVIEW. Close F036 per
`docs/roadmap/STATUS_closure_protocol.md` Algorithm steps 4 and 5: book round 8, rotate the finding
ledger, flip F036's STATUS line to `[x]` with the README's accepted count, Tier 5 Done cell and
prose in the same commit, and open the pull request. No self-use item is consumed: round 8 read
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
`.remedy-wt/f036-r9-worker/`, which is yours. Never run npm or npx. `.remedy-wt/f036-r9/`,
`.remedy-wt/f036-r9-sim/`, `.remedy-wt/f036-r8-sim/` and `.remedy-wt/f036-review/` are the reviewer's and read-only. The
`remedy` command is denied; use `python3 -m apps.cli.main` where a gate names it.

COMMIT TRAILER — every commit ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop.
2. In `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain` empty,
   `git branch --show-current` `feature/f036-guided-result-tour`, `git log --oneline -1`
   `40553872`.
3. Measure this block's line count and sha256 (`.remedy-wt/f036-r9/block.md`) against your
   delegation message's readings; stop if either differs.
4. Report `git worktree list | wc -l`, and `gh pr list --state open --json number,headRefName`, which
   must be EMPTY.

PAYLOADS — under `.remedy-wt/f036-r9/`, lines = newline count; verify each BEFORE use:
| file | lines | bytes | sha256 |
|---|---|---|---|
| build.py | 108 | 5591 | f8e200da22b5726c4ec9caca0356f9da67d71567bf15164e621ed9768d86519e |
| closure.diff | 52 | 3997 | 61dc87ac75b43cf6435b02b40dc580f858c040f2bc1d7107b5485f7cc49b60d0 |
| ledger.md | 2 | 2498 | ac9633a41624c232e66afc67fd4ddb39300315923f75c2e752c4d12e08632197 |
| plan.md | 26 | 813 | 0b11b61b4c0c68237e11b1d05ebf6b78c84d3b109f0ff8cef8644f0e5105fe58 |
| pr_body.md | 98 | 5804 | 9d8dbf6a6c2756912b0fc1ecfd16cfd511fab25be8f2009f3756992d45a1e1e9 |
| readme_para.txt | 9 | 780 | 0bdbf52b808dc5a3e7f91d0fbc5129454106115f0a1709d9ad391c1407b68dba |
| status_line.txt | 1 | 392 | ced0285376fa9cb89fc5fa64d0c2eea8c490261d71a66bbde260cd903fc8f629 |
`ledger.md` is appended to `.agent/live_review.md` byte for byte (it starts with its own blank
line); `plan.md` REWRITES `.agent/plan.md` by `shutil.copyfile`, never by retyping; `closure.diff`
flips F036's STATUS line and moves the README's accepted count, Tier 5 Done cell and prose — it goes
on with `git apply --check` then `git apply`; `status_line.txt` is the exact STATUS line closure.diff
writes, for G4's proof; `pr_body.md` is the pull request's description, passed to `gh` as a file;
`readme_para.txt` and `build.py` are the reviewer's sources for closure.diff, copied for the record
and never applied or run.

BUNDLE — C1 to C4, then the pull request.
C1 COPIES: `.agent/authored/f036-r9-block.md` := this block and each payload as
   `.agent/authored/f036-r9-<name>`, by `shutil.copyfile`. Subject `F036 R9 C1: copy round 9
   block and payloads`. Its insertions are this block's line count plus 296; STOP rather than commit
   if that reaches 500.
C2 THE BOOKING: the ledger append and the plan rewrite. Subject `F036 R9 C2: book round 8's PASS,
   the package READY_FOR_REVIEW`. Expected by `git show --numstat`: 2/0 `.agent/live_review.md`,
   5/6 `.agent/plan.md`.
C3 THE ROTATION, its own commit, paths `.agent/live_review.md` and `.agent/live_review_archive.md`
   ONLY: `python3 scripts/rotate_live_review.py`; report its printed output in full. Subject
   `F036 R9 C3: rotate the finding ledger into its archive`. Expected: 0/36
   `.agent/live_review.md`, 36/0 `.agent/live_review_archive.md`.
C4 THE CLOSURE COMMIT, exactly these paths: `docs/roadmap/STATUS.md`, `README.md` and
   `.agent/handoff.md`. `git apply` closure.diff, run G4 on the
   working tree, rewrite `.agent/handoff.md` per `docs/agents/handback_template.md` as the closure
   handback, run G5, then commit. The handback names, spelled exactly so, the package
   `remedy-review-20260928-094901-READY_FOR_REVIEW.zip`, its SHA-256
   `e2bd771b3f1c1a52fcc7e73cdae50c4fd4a837107ee5e46b76d79d8b8dffc2f4`, its directory
   `/home/decodeux/Repos/remedy-history/zips`, the evidence job `f036r8e1001`, the accepted head
   `153537dc8e5a6bb7061f220cdeaffbc1829d3067` and `self-use NONE (queue exhausted)`; and it names NO
   pull request number, which does not exist when it is written. Subject `F036 R9 C4: accept F036 in
   STATUS with its README pins`. Expected for the two applied files: 12/2
   `README.md`, 1/1 `docs/roadmap/STATUS.md`. Then `git push`.
THE PULL REQUEST, after C4 and its push: `gh pr create --base main --head
   feature/f036-guided-result-tour --title "F036 — Guided result tour"
   --body-file .remedy-wt/f036-r9/pr_body.md`. DO NOT MERGE IT. Report its
   number and URL in your final reply only.

CONSTRAINTS
1. Never edit or retype a payload. `build.py` is NOT run: it would reset the reviewer's tree.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f036-r9-*` copies,
   `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/roadmap/STATUS.md`, `README.md` and `.agent/handoff.md`.
4. C4 is the LAST commit on this branch (Rule A4). Nothing follows it.
5. If any gate goes red, STOP before C4: commit and push what is verified, write the handoff under
   AGENTS.md "If Blocked", and hand back. A closure that cannot be proved is not closed.
6. NOTHING IS MERGED: no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
7. Delete nothing you did not create; every existing worktree and branch stays.
8. DO NOT run the full suite: this feature's run is `.agent/authored/f036-closure-suite.txt`.

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G4 run before
the handback is written, and the handback states their readings; G5 runs after the handback is
written and before C4 is committed, so its readings go in your final reply.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f036-r9-*` copy byte-equal to its source by `git show <C1>:<path>`.
G2 THE BOOKING, at C2, read with `git show <C2>:<path>`, each equal to the reviewer's simulation:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 344469 | 610eb75199aec2d06fb2f895292cf1d05c8ba8392d1f1c500503ffc16eb87151 |
   | .agent/plan.md | 813 | 0b11b61b4c0c68237e11b1d05ebf6b78c84d3b109f0ff8cef8644f0e5105fe58 |
   and `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger at C2 — the
   simulation read `[]`.
G3 THE ROTATION, at C3: the reviewer's simulation of `python3 scripts/rotate_live_review.py` printed,
   line for line apart from its final `written:` line, which names the simulation's own paths:
   gate records moved: 10
   finding pairs moved: 4 (8 records)
   old ledger size: 344469 bytes
   new ledger size: 303959 bytes
   old archive size: 5340260 bytes
   new archive size: 5380770 bytes
   open findings before: 0
   open findings after: 0
   and left the two ledger files at:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 303959 | bfede5e874f5b3bc89137538b38c2d89d3e41958839d559c286b4c7cc4c63a70 |
   | .agent/live_review_archive.md | 5380770 | db9bea9d7c9c79cb58c6303a3fde89782f9f49e3cc52ab199ade1a90e8713792 |
   Report yours beside each, and C3's path set, which is the two ledger files and nothing else.
G4 THE CLOSURE EDITS AND THE TREE, with closure.diff applied, before the handback is written:
   | path | bytes | sha256 |
   |---|---|---|
   | docs/roadmap/STATUS.md | 56619 | 3b77eec91532077b3a8b494bf64231517e263ebb1f2cc03d8375cd159ad6c80d |
   | README.md | 42469 | af8845034d3c23d2bd4532418454b7383eb9cdec373300d51a261a7ee45b0671 |
   the count of lines of `docs/roadmap/STATUS.md` equal to the one line of status_line.txt, which
   must be 1; `pending_self_use_items()` from `packages.orchestration.self_use_queue`, which must be
   empty; serially,
   `bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'`,
   which the simulation read as `512 passed` at exit 0; then
   `python3 -m apps.cli.main integrity check --json`, six checks with status `pass` at `fail_count`
   0 — each check's status is the reading, not the exit code. The reviewer red-controlled both
   README pins: with the accepted count left at 112, and with the Tier 5 Done cell left at 29,
   `tests/docs/` read `1 failed, 326 passed` at exit 1 each time.
G5 THE HANDBACK'S PINS, after the handback is written and before C4 is committed: for each of the six
   strings C4 names, its count in the new `.agent/handoff.md`, each at least 1; the count of `pull/`
   in it, which must be 0; and the presence of its item-status table section.
G6 AFTER C4: `git log --oneline -n 5`, showing C4, C3, C2, C1 and `40553872`; `git status
   --porcelain` empty; the push's real outcome; the pull request's number and URL; and `gh pr list
   --state open --json number,headRefName,baseRefName,isDraft` showing exactly that one pull request,
   from this branch into `main`, not a draft. These go in your final reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block, the
per-commit changed-files table with the `git show --numstat` counts you measured beside the ones
above, every gate reading G1 to G4 with its real exit code, the authored-text proofs, the deviations,
the next action, and — INSIDE `.agent/handoff.md` itself, as its own section — the item-status table
AGENTS.md requires, one row per commit, the pull request and each gate. Session section: SESSION 2 of
feature F036, round 9, rounds so far 9, plus one sentence on how much context you had left.
`## Next`: Phase 1 rule 1, then the Open PR Gate — the pull request this round opens is merged by the
NEXT feature's session, never by this one — then Rule A5, the first unchecked feature in
`docs/roadmap/STATUS.md`. State the open-findings count as the script reads it at C3, and "Operator
questions open: 1".
