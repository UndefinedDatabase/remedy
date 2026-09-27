STEP F028 R12 — THE CLOSING ROUND: book round 11, rotate the ledger, and accept F028 in STATUS with its README pins, then open the pull request

GOAL
Round 11 passed with the package READY_FOR_REVIEW. Close F028 per
`docs/roadmap/STATUS_closure_protocol.md` Algorithm steps 4 and 5: book round 11, rotate the finding
ledger, flip F028's STATUS line to `[x]` with the README's accepted count, Tier 5 Done cell and
prose in the same commit, and open the pull request. No self-use item is consumed: round 10 read
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
`.remedy-wt/f028-r12-worker/`, which is yours. Never run npm or npx. `.remedy-wt/f028-r12/`,
`.remedy-wt/f028-r10-sim/` and `.remedy-wt/f028-review/` are the reviewer's and read-only. The
`remedy` command is denied; use `python3 -m apps.cli.main` where a gate names it.

COMMIT TRAILER — every commit ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop.
2. In `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain` empty,
   `git branch --show-current` `feature/f028-task-injection`, `git log --oneline -1`
   `41e4b9fd`.
3. Measure this block's line count and sha256 (`.remedy-wt/f028-r12/block.md`) against your
   delegation message's readings; stop if either differs.
4. Report `git worktree list | wc -l`, and `gh pr list --state open --json number,headRefName`, which
   must be EMPTY.

PAYLOADS — under `.remedy-wt/f028-r12/`, lines = newline count; verify each BEFORE use:
| file | lines | bytes | sha256 |
|---|---|---|---|
| build.py | 104 | 5844 | 356e6c3eff06599372f05609e848518f50571a4fd5ea7fcdc45f20a35c300c27 |
| closure.diff | 55 | 3456 | d5a46d60f97f1139a337cf0d35a225ed7102fb86529ed9567ce589f451911ba3 |
| ledger.md | 2 | 1868 | 9a8d58f847d5b4c827c598898c00c777ead5dd715c5cc066ab896c5488d9b5f1 |
| plan.md | 25 | 802 | bc5319158c2afb0405567f624c17d6addb067d15eb7348da689c7ba6ea6c5d42 |
| pr_body.md | 83 | 5237 | 730ec6829fc17c6fc9da16243125c064f3530112dbc8d7b8f6c7c6f475a4f68a |
| readme_para.txt | 12 | 1008 | ffee8298a57459bca3e524d1ff7fe965ee0a9180cf861117b61150f2e4936b16 |
| status_line.txt | 1 | 389 | 1a332d9cfaa685cab2397a6b8ff3450e7383d44c1278665913ea060fb9f4fbad |
`ledger.md` is appended to `.agent/live_review.md` byte for byte (it starts with its own blank
line); `plan.md` REWRITES `.agent/plan.md`; `closure.diff` flips F028's STATUS line and moves the
README's accepted count, Tier 5 Done cell and prose — it goes on
with `git apply --check` then `git apply`; `status_line.txt` is the exact STATUS line closure.diff
writes, for G4's proof; `pr_body.md` is the pull request's description, passed to `gh` as a file;
`readme_para.txt` and `build.py` are the reviewer's sources for closure.diff, copied for the record
and never applied or run.

BUNDLE — C1 to C4, then the pull request.
C1 COPIES: `.agent/authored/f028-r12-block.md` := this block and each payload as
   `.agent/authored/f028-r12-<name>`, by `shutil.copyfile`. Subject `F028 R12 C1: copy round 12
   block and payloads`. Its insertions are this block's line count plus 282; STOP rather than commit
   if that reaches 500.
C2 THE BOOKING: the ledger append and the plan rewrite. Subject `F028 R12 C2: book round 11's PASS,
   the package READY_FOR_REVIEW`. Expected by `git show --numstat`: 2/0 `.agent/live_review.md`,
   5/5 `.agent/plan.md`.
C3 THE ROTATION, its own commit, paths `.agent/live_review.md` and `.agent/live_review_archive.md`
   ONLY: `python3 scripts/rotate_live_review.py`; report its printed output in full. Subject
   `F028 R12 C3: rotate the finding ledger into its archive`. Expected: 0/36
   `.agent/live_review.md`, 36/0 `.agent/live_review_archive.md`.
C4 THE CLOSURE COMMIT, exactly these paths: `docs/roadmap/STATUS.md`, `README.md` and
   `.agent/handoff.md`. `git apply` closure.diff, run G4 on the
   working tree, rewrite `.agent/handoff.md` per `docs/agents/handback_template.md` as the closure
   handback, run G5, then commit. The handback names, spelled exactly so, the package
   `remedy-review-20260927-132129-READY_FOR_REVIEW.zip`, its SHA-256
   `904723bf332d1f076cdfde262f84609fada02ca86635f3ef09a88c3d025692fe`, its directory
   `/home/decodeux/Repos/remedy-history/zips`, the evidence job `f028r11e1001`, the accepted head
   `9cfd84d1217c24057173f4b9a8db03734c174c09` and `self-use NONE (queue exhausted)`; and it names NO pull
   request number, which does not exist when it is written. Subject `F028 R12 C4: accept F028 in
   STATUS with its README pins`. Expected for the two applied files: 15/2
   `README.md`, 1/1 `docs/roadmap/STATUS.md`. Then `git push`.
THE PULL REQUEST, after C4 and its push: `gh pr create --base main --head
   feature/f028-task-injection --title "F028 — Task injection"
   --body-file .remedy-wt/f028-r12/pr_body.md`. DO NOT MERGE IT. Report its
   number and URL in your final reply only.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f028-r12-*` copies,
   `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/roadmap/STATUS.md`, `README.md` and `.agent/handoff.md`.
4. C4 is the LAST commit on this branch (Rule A4). Nothing follows it.
5. If any gate goes red, STOP before C4: commit and push what is verified, write the handoff under
   AGENTS.md "If Blocked", and hand back. A closure that cannot be proved is not closed.
6. NOTHING IS MERGED: no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
7. Delete nothing you did not create; every existing worktree and branch stays.
8. DO NOT run the full suite: this feature's run is `.agent/authored/f028-closure-suite.txt`.

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G4 run before
the handback is written, and the handback states their readings; G5 runs after the handback is
written and before C4 is committed, so its readings go in your final reply.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f028-r12-*` copy byte-equal to its source by `git show <C1>:<path>`.
G2 THE BOOKING, at C2, read with `git show <C2>:<path>`, each equal to the reviewer's simulation:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 342930 | de07c53a382777485726fbc9f9a0b9b272a11ff7687e1386923295021c0bd6da |
   | .agent/plan.md | 802 | bc5319158c2afb0405567f624c17d6addb067d15eb7348da689c7ba6ea6c5d42 |
   and `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger at C2 — the
   simulation read `[]`.
G3 THE ROTATION, at C3: the reviewer's simulation of `python3 scripts/rotate_live_review.py` printed,
   line for line apart from its final `written:` line, which names the simulation's own paths:
   gate records moved: 10
   finding pairs moved: 4 (8 records)
   old ledger size: 342930 bytes
   new ledger size: 305800 bytes
   old archive size: 5214551 bytes
   new archive size: 5251681 bytes
   open findings before: 0
   open findings after: 0
   and left the two ledger files at:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 305800 | d6a70e718556dfd5f526142c9ef93532b0c52a24cda01992b43a05a4658dbdeb |
   | .agent/live_review_archive.md | 5251681 | 8d5c7b464af6e4df33bac23d93c260e403cd3159b6336692630dcdf30fe5c5dd |
   Report yours beside each, and C3's path set, which is the two ledger files and nothing else.
G4 THE CLOSURE EDITS AND THE TREE, with closure.diff applied, before the handback is written:
   | path | bytes | sha256 |
   |---|---|---|
   | docs/roadmap/STATUS.md | 55186 | 503ce42ccb7b3d93c869c00f4246c232aa6a8034ae5b42aa68e17998ec947abe |
   | README.md | 39048 | c305fc3c1cea302f8a6f12a8346b44f62a9d3c4d588a54b2a395505cf327950b |
   the count of lines of `docs/roadmap/STATUS.md` equal to the one line of status_line.txt, which
   must be 1; `pending_self_use_items()` from `packages.orchestration.self_use_queue`, which must be
   empty; serially,
   `bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'`,
   which the simulation read as `512 passed` at exit 0; then
   `python3 -m apps.cli.main integrity check --json`, six checks with status `pass` at `fail_count`
   0 — each check's status is the reading, not the exit code. The reviewer red-controlled both
   README pins: with the accepted count left at 108, and with the Tier 5 Done cell left at 25,
   `tests/docs/` read `1 failed, 326 passed` at exit 1 each time.
G5 THE HANDBACK'S PINS, after the handback is written and before C4 is committed: for each of the six
   strings C4 names, its count in the new `.agent/handoff.md`, each at least 1; the count of `pull/`
   in it, which must be 0; and the presence of its item-status table section.
G6 AFTER C4: `git log --oneline -n 5`, showing C4, C3, C2, C1 and `41e4b9fd`; `git status
   --porcelain` empty; the push's real outcome; the pull request's number and URL; and `gh pr list
   --state open --json number,headRefName,baseRefName,isDraft` showing exactly that one pull request,
   from this branch into `main`, not a draft. These go in your final reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block, the
per-commit changed-files table with the `git show --numstat` counts you measured beside the ones
above, every gate reading G1 to G4 with its real exit code, the authored-text proofs, the deviations,
the next action, and — INSIDE `.agent/handoff.md` itself, as its own section — the item-status table
AGENTS.md requires, one row per commit, the pull request and each gate. Session section: SESSION 2 of
feature F028, round 12, rounds so far 12, plus one sentence on how much context you had left.
`## Next`: Phase 1 rule 1, then the Open PR Gate — the pull request this round opens is merged by the
NEXT feature's session, never by this one — then Rule A5, the first unchecked feature in
`docs/roadmap/STATUS.md`. State the open-findings count as the script reads it at C3, and "Operator
questions open: 0".
