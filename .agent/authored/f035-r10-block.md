STEP F035 R10 — THE CLOSING ROUND: book round 9, rotate the ledger, and accept F035 in STATUS with its README pins, then open the pull request

GOAL
Round 9 passed with the package READY_FOR_REVIEW. Close F035 per
`docs/roadmap/STATUS_closure_protocol.md` Algorithm steps 4 and 5: book round 9, rotate the finding
ledger, flip F035's STATUS line to `[x]` with the README's accepted count, Tier 5 Done cell and
prose in the same commit, and open the pull request. No self-use item is consumed: round 9 read
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
`.remedy-wt/f035-r10-worker/`, which is yours. Never run npm or npx. `.remedy-wt/f035-r10/`,
`.remedy-wt/f035-r10-sim/`, `.remedy-wt/f035-r9-sim/` and `.remedy-wt/f035-review/` are the reviewer's and read-only. The
`remedy` command is denied; use `python3 -m apps.cli.main` where a gate names it.

COMMIT TRAILER — every commit ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop.
2. In `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain` empty,
   `git branch --show-current` `feature/f035-ownership-ledger`, `git log --oneline -1`
   `ce75183d`.
3. Measure this block's line count and sha256 (`.remedy-wt/f035-r10/block.md`) against your
   delegation message's readings; stop if either differs.
4. Report `git worktree list | wc -l`, and `gh pr list --state open --json number,headRefName`, which
   must be EMPTY.

PAYLOADS — under `.remedy-wt/f035-r10/`, lines = newline count; verify each BEFORE use:
| file | lines | bytes | sha256 |
|---|---|---|---|
| build.py | 104 | 5845 | 57cfbaeab6d1deb5c11d4413e05e776f2fc946b9b79a4395fc2204d17cab417b |
| closure.diff | 52 | 4019 | 9062d47ea03a000461b98b41e564328f589c191b10c2cb4121ae886103fce39d |
| ledger.md | 2 | 2734 | 0f7b71278e1367677043d5e85fced794d2523c7dfe9fa33f8e685d48e05c2d7f |
| plan.md | 25 | 759 | 55442986ce0f6596382af7918c1a0f4c34f519f828becaeec8a1859cf302776e |
| pr_body.md | 91 | 5656 | a834c4b7c2bb946cd4e36bc3d5b0296a1a9c5b7445349ee6e7bda312da237172 |
| readme_para.txt | 9 | 810 | 2a1425d599b4eedee0fbe631e667dd30cbcd4dfc012cac8f76222ac67a16ed7e |
| status_line.txt | 1 | 390 | fdabd7a33f5fb336b9edb0e2c1d46601b3e841cd97cd8005e937f207be339051 |
`ledger.md` is appended to `.agent/live_review.md` byte for byte (it starts with its own blank
line); `plan.md` REWRITES `.agent/plan.md` by `shutil.copyfile`, never by retyping; `closure.diff`
flips F035's STATUS line and moves the README's accepted count, Tier 5 Done cell and prose — it goes
on with `git apply --check` then `git apply`; `status_line.txt` is the exact STATUS line closure.diff
writes, for G4's proof; `pr_body.md` is the pull request's description, passed to `gh` as a file;
`readme_para.txt` and `build.py` are the reviewer's sources for closure.diff, copied for the record
and never applied or run.

BUNDLE — C1 to C4, then the pull request.
C1 COPIES: `.agent/authored/f035-r10-block.md` := this block and each payload as
   `.agent/authored/f035-r10-<name>`, by `shutil.copyfile`. Subject `F035 R10 C1: copy round 10
   block and payloads`. Its insertions are this block's line count plus 284; STOP rather than commit
   if that reaches 500.
C2 THE BOOKING: the ledger append and the plan rewrite. Subject `F035 R10 C2: book round 9's PASS,
   the package READY_FOR_REVIEW`. Expected by `git show --numstat`: 2/0 `.agent/live_review.md`,
   4/7 `.agent/plan.md`.
C3 THE ROTATION, its own commit, paths `.agent/live_review.md` and `.agent/live_review_archive.md`
   ONLY: `python3 scripts/rotate_live_review.py`; report its printed output in full. Subject
   `F035 R10 C3: rotate the finding ledger into its archive`. Expected: 0/34
   `.agent/live_review.md`, 34/0 `.agent/live_review_archive.md`.
C4 THE CLOSURE COMMIT, exactly these paths: `docs/roadmap/STATUS.md`, `README.md` and
   `.agent/handoff.md`. `git apply` closure.diff, run G4 on the
   working tree, rewrite `.agent/handoff.md` per `docs/agents/handback_template.md` as the closure
   handback, run G5, then commit. The handback names, spelled exactly so, the package
   `remedy-review-20260928-050815-READY_FOR_REVIEW.zip`, its SHA-256
   `9b3e3841d2c11725c8a03579fa2a7d5dcb963aac3386faeb5a6ab5517ac2b8aa`, its directory
   `/home/decodeux/Repos/remedy-history/zips`, the evidence job `f035r9e1001`, the accepted head
   `7f25c03bddca1d9c08b58821288b7eed42d1e3cb` and `self-use NONE (queue exhausted)`; and it names NO
   pull request number, which does not exist when it is written. Subject `F035 R10 C4: accept F035 in
   STATUS with its README pins`. Expected for the two applied files: 12/2
   `README.md`, 1/1 `docs/roadmap/STATUS.md`. Then `git push`.
THE PULL REQUEST, after C4 and its push: `gh pr create --base main --head
   feature/f035-ownership-ledger --title "F035 — Ownership ledger"
   --body-file .remedy-wt/f035-r10/pr_body.md`. DO NOT MERGE IT. Report its
   number and URL in your final reply only.

CONSTRAINTS
1. Never edit or retype a payload. `build.py` is NOT run: it would reset the reviewer's tree.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f035-r10-*` copies,
   `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/roadmap/STATUS.md`, `README.md` and `.agent/handoff.md`.
4. C4 is the LAST commit on this branch (Rule A4). Nothing follows it.
5. If any gate goes red, STOP before C4: commit and push what is verified, write the handoff under
   AGENTS.md "If Blocked", and hand back. A closure that cannot be proved is not closed.
6. NOTHING IS MERGED: no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
7. Delete nothing you did not create; every existing worktree and branch stays.
8. DO NOT run the full suite: this feature's run is `.agent/authored/f035-closure-suite.txt`.

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G4 run before
the handback is written, and the handback states their readings; G5 runs after the handback is
written and before C4 is committed, so its readings go in your final reply.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f035-r10-*` copy byte-equal to its source by `git show <C1>:<path>`.
G2 THE BOOKING, at C2, read with `git show <C2>:<path>`, each equal to the reviewer's simulation:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 337653 | befcaac35a8164e9d083dc34572660dcb31b6f6fbd518714cbae5c9f75317e4f |
   | .agent/plan.md | 759 | 55442986ce0f6596382af7918c1a0f4c34f519f828becaeec8a1859cf302776e |
   and `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger at C2 — the
   simulation read `[]`.
G3 THE ROTATION, at C3: the reviewer's simulation of `python3 scripts/rotate_live_review.py` printed,
   line for line apart from its final `written:` line, which names the simulation's own paths:
   gate records moved: 7
   finding pairs moved: 5 (10 records)
   old ledger size: 337653 bytes
   new ledger size: 309879 bytes
   old archive size: 5312486 bytes
   new archive size: 5340260 bytes
   open findings before: 0
   open findings after: 0
   and left the two ledger files at:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 309879 | 9b3b354eaa914689cdaae86f1ead92defb7aef42c5d57faf372ec7a3b715f30e |
   | .agent/live_review_archive.md | 5340260 | bf27e6abf38abc805f22a0f9c707ddc7de49efcfdda820b2e6af1ec49669a7c6 |
   Report yours beside each, and C3's path set, which is the two ledger files and nothing else.
G4 THE CLOSURE EDITS AND THE TREE, with closure.diff applied, before the handback is written:
   | path | bytes | sha256 |
   |---|---|---|
   | docs/roadmap/STATUS.md | 56261 | 9a64e3b384631cd4c8bb8ad13d4f8e55df0315d48461e812d29504b0ccfbe3bd |
   | README.md | 41688 | e8e86e038b281e70a1452768fee57da2e3f1f960dae5b6402562585286630ffc |
   the count of lines of `docs/roadmap/STATUS.md` equal to the one line of status_line.txt, which
   must be 1; `pending_self_use_items()` from `packages.orchestration.self_use_queue`, which must be
   empty; serially,
   `bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'`,
   which the simulation read as `512 passed` at exit 0; then
   `python3 -m apps.cli.main integrity check --json`, six checks with status `pass` at `fail_count`
   0 — each check's status is the reading, not the exit code. The reviewer red-controlled both
   README pins: with the accepted count left at 111, and with the Tier 5 Done cell left at 28,
   `tests/docs/` read `1 failed, 326 passed` at exit 1 each time.
G5 THE HANDBACK'S PINS, after the handback is written and before C4 is committed: for each of the six
   strings C4 names, its count in the new `.agent/handoff.md`, each at least 1; the count of `pull/`
   in it, which must be 0; and the presence of its item-status table section.
G6 AFTER C4: `git log --oneline -n 5`, showing C4, C3, C2, C1 and `ce75183d`; `git status
   --porcelain` empty; the push's real outcome; the pull request's number and URL; and `gh pr list
   --state open --json number,headRefName,baseRefName,isDraft` showing exactly that one pull request,
   from this branch into `main`, not a draft. These go in your final reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block, the
per-commit changed-files table with the `git show --numstat` counts you measured beside the ones
above, every gate reading G1 to G4 with its real exit code, the authored-text proofs, the deviations,
the next action, and — INSIDE `.agent/handoff.md` itself, as its own section — the item-status table
AGENTS.md requires, one row per commit, the pull request and each gate. Session section: SESSION 2 of
feature F035, round 10, rounds so far 10, plus one sentence on how much context you had left.
`## Next`: Phase 1 rule 1, then the Open PR Gate — the pull request this round opens is merged by the
NEXT feature's session, never by this one — then Rule A5, the first unchecked feature in
`docs/roadmap/STATUS.md`. State the open-findings count as the script reads it at C3, and "Operator
questions open: 0".
