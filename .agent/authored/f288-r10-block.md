STEP F288 R10 — THE CLOSING ROUND: book round 9, rotate the ledger, and accept F288 in STATUS with its README pins and the self-use item's consumption, then open the pull request

GOAL
Round 9 passed with the package READY_FOR_REVIEW. Close F288 per
`docs/roadmap/STATUS_closure_protocol.md` Algorithm steps 4 and 5: book round 9, rotate the finding
ledger, flip F288's STATUS line to `[x]` with the README's accepted count, Tier 5 Done cell and
prose, set `SU-034`'s `consumed_by` to `F288` in the same commit, and open the pull request.

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
`.remedy-wt/f288-r10-worker/`, which is yours. Never run npm or npx. `.remedy-wt/f288-r10/`,
`.remedy-wt/f288-r7-sim/` and `.remedy-wt/f288-review/` are the reviewer's and read-only. The
`remedy` command is denied; use `python3 -m apps.cli.main` where a gate names it.

COMMIT TRAILER — every commit ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop.
2. In `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain` empty,
   `git branch --show-current` `feature/f288-event-stream-completeness`, `git log --oneline -1`
   `acd2a908`.
3. Measure this block's line count and sha256 (`.remedy-wt/f288-r10/block.md`) against your
   delegation message's readings; stop if either differs.
4. Report `git worktree list | wc -l`, and `gh pr list --state open --json number,headRefName`, which
   must be EMPTY.

PAYLOADS — under `.remedy-wt/f288-r10/`, lines = newline count; verify each BEFORE use:
| file | lines | bytes | sha256 |
|---|---|---|---|
| build.py | 107 | 6130 | 98d57afb65cdcbccb52f668b38f4f123e22b72cd70792dbe1de50ba74d8a1106 |
| closure.diff | 66 | 4877 | afbc0436e65887e5606359fe858d509267a178ade8f598f5c7088c4a23ef0682 |
| ledger.md | 2 | 2196 | 72bfabbcb2c08ebd4b776ad2f1f2edbdfe8e7e753595a8339de4d964236092c8 |
| plan.md | 26 | 827 | bb1fef9932e67ae9533623efac66aabd670861956568bafadb9446813e1d125d |
| pr_body.md | 84 | 5272 | e230ba0ccd086e1573470e7ebe4f23df55e196a62c6b09f3050860c0492cfc47 |
| readme_para.txt | 10 | 775 | 427fe6e22aaea54aaacb6f9ee3c5bec4518befef49bf2036bbc54c221ef9f878 |
| status_line.txt | 1 | 432 | 9178c5a88b78c1bc34effd722a66bbc7f335c84c58cd1018d609d39f1e658270 |
`ledger.md` is appended to `.agent/live_review.md` byte for byte (it starts with its own blank
line); `plan.md` REWRITES `.agent/plan.md`; `closure.diff` flips F288's STATUS line, moves the
README's accepted count, Tier 5 Done cell and prose, and sets `SU-034`'s `consumed_by` — it goes on
with `git apply --check` then `git apply`; `status_line.txt` is the exact STATUS line closure.diff
writes, for G4's proof; `pr_body.md` is the pull request's description, passed to `gh` as a file;
`readme_para.txt` and `build.py` are the reviewer's sources for closure.diff, copied for the record
and never applied or run.

BUNDLE — C1 to C4, then the pull request.
C1 COPIES: `.agent/authored/f288-r10-block.md` := this block and each payload as
   `.agent/authored/f288-r10-<name>`, by `shutil.copyfile`. Subject `F288 R10 C1: copy round 10
   block and payloads`. Its insertions are this block's line count plus 296; STOP rather than commit
   if that reaches 500.
C2 THE BOOKING: the ledger append and the plan rewrite. Subject `F288 R10 C2: book round 9's PASS,
   the package READY_FOR_REVIEW`. Expected by `git show --numstat`: 2/0 `.agent/live_review.md`,
   6/6 `.agent/plan.md`.
C3 THE ROTATION, its own commit, paths `.agent/live_review.md` and `.agent/live_review_archive.md`
   ONLY: `python3 scripts/rotate_live_review.py`; report its printed output in full. Subject
   `F288 R10 C3: rotate the finding ledger into its archive`. Expected: 0/18
   `.agent/live_review.md`, 18/0 `.agent/live_review_archive.md`.
C4 THE CLOSURE COMMIT, exactly these paths: `docs/roadmap/STATUS.md`, `README.md`,
   `scripts/self_use_queue.json` and `.agent/handoff.md`. `git apply` closure.diff, run G4 on the
   working tree, rewrite `.agent/handoff.md` per `docs/agents/handback_template.md` as the closure
   handback, run G5, then commit. The handback names, spelled exactly so, the package
   `remedy-review-20260927-060235-READY_FOR_REVIEW.zip`, its SHA-256
   `184f155676e7fdfc8bdf8f2db736ed0b96b127f84fb3873580fefe38c10373d2`, its directory
   `/home/decodeux/Repos/remedy-history/zips`, the evidence job `f288r9e1001`, the accepted head
   `57eba86adcc3ceeb83b04a3dfe0cf5d655a0d205` and the self-use item `SU-034`; and it names NO pull
   request number, which does not exist when it is written. Subject `F288 R10 C4: accept F288 in
   STATUS with its README pins and consume SU-034`. Expected for the three applied files: 13/2
   `README.md`, 1/1 `docs/roadmap/STATUS.md`, 1/1 `scripts/self_use_queue.json`. Then `git push`.
THE PULL REQUEST, after C4 and its push: `gh pr create --base main --head
   feature/f288-event-stream-completeness --title "F288 — Event stream completeness & prompt nodes
   in the live graph" --body-file .remedy-wt/f288-r10/pr_body.md`. DO NOT MERGE IT. Report its
   number and URL in your final reply only.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f288-r10-*` copies,
   `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json` and `.agent/handoff.md`.
4. C4 is the LAST commit on this branch (Rule A4). Nothing follows it.
5. If any gate goes red, STOP before C4: commit and push what is verified, write the handoff under
   AGENTS.md "If Blocked", and hand back. A closure that cannot be proved is not closed.
6. NOTHING IS MERGED: no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
7. Delete nothing you did not create; every existing worktree and branch stays, the job branch
   `remedy/job-8356faebdc904fd1` included.
8. DO NOT run the full suite: this feature's run is `.agent/authored/f288-closure-suite.txt`.

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G4 run before
the handback is written, and the handback states their readings; G5 runs after the handback is
written and before C4 is committed, so its readings go in your final reply.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f288-r10-*` copy byte-equal to its source by `git show <C1>:<path>`.
G2 THE BOOKING, at C2, read with `git show <C2>:<path>`, each equal to the reviewer's simulation:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 329140 | bad17846b41b6a384e9a00a8fa95462d0238b88d30316af3e2188874c10ee7fe |
   | .agent/plan.md | 827 | bb1fef9932e67ae9533623efac66aabd670861956568bafadb9446813e1d125d |
   and `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger at C2 — the
   simulation read `[]`.
G3 THE ROTATION, at C3: the reviewer's simulation of `python3 scripts/rotate_live_review.py` printed,
   line for line apart from its final `written:` line, which names the simulation's own paths:
   gate records moved: 7
   finding pairs moved: 1 (2 records)
   old ledger size: 329140 bytes
   new ledger size: 307379 bytes
   old archive size: 5192790 bytes
   new archive size: 5214551 bytes
   open findings before: 0
   open findings after: 0
   and left the two ledger files at:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 307379 | 94fb5a46f631031d7f8fb208a39f6483f52bd0e89a048968fa61bf7a1be7408b |
   | .agent/live_review_archive.md | 5214551 | cb6be2aabc6fe66fa93beb13cca4cab5e7f76596c752b4d86dd24ac1dc2ac296 |
   Report yours beside each, and C3's path set, which is the two ledger files and nothing else.
G4 THE CLOSURE EDITS AND THE TREE, with closure.diff applied, before the handback is written:
   | path | bytes | sha256 |
   |---|---|---|
   | docs/roadmap/STATUS.md | 54827 | d4ffb2a5c949822f253db6114240ab1e20df5b0af8b454ae19b49d0dcfbbc2ed |
   | README.md | 38039 | a4b520406918a5d42c007af43d53e44ea56cd3987c37aa1db156e98b825b3625 |
   | scripts/self_use_queue.json | 138342 | c209340be1e923abbcf91717127436917be59141606f22bd77a4d7e67909a268 |
   the count of lines of `docs/roadmap/STATUS.md` equal to the one line of status_line.txt, which
   must be 1; `SU-034`'s `consumed_by` read through `load_self_use_queue` from
   `packages.orchestration.self_use_queue`, which must be `F288`, with `pending_self_use_items()`
   empty; serially,
   `bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'`,
   which the simulation read as `512 passed` at exit 0; then
   `python3 -m apps.cli.main integrity check --json`, six checks with status `pass` at `fail_count`
   0 — each check's status is the reading, not the exit code. The reviewer red-controlled both
   README pins: with the accepted count left at 107, and with the Tier 5 Done cell left at 24,
   `tests/docs/` read `1 failed, 326 passed` at exit 1 each time.
G5 THE HANDBACK'S PINS, after the handback is written and before C4 is committed: for each of the six
   strings C4 names, its count in the new `.agent/handoff.md`, each at least 1; the count of `pull/`
   in it, which must be 0; and the presence of its item-status table section.
G6 AFTER C4: `git log --oneline -n 5`, showing C4, C3, C2, C1 and `acd2a908`; `git status
   --porcelain` empty; the push's real outcome; the pull request's number and URL; and `gh pr list
   --state open --json number,headRefName,baseRefName,isDraft` showing exactly that one pull request,
   from this branch into `main`, not a draft. These go in your final reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block, the
per-commit changed-files table with the `git show --numstat` counts you measured beside the ones
above, every gate reading G1 to G4 with its real exit code, the authored-text proofs, the deviations,
the next action, and — INSIDE `.agent/handoff.md` itself, as its own section — the item-status table
AGENTS.md requires, one row per commit, the pull request and each gate. Session section: SESSION 2 of
feature F288, round 10, rounds so far 10, plus one sentence on how much context you had left.
`## Next`: Phase 1 rule 1, then the Open PR Gate — the pull request this round opens is merged by the
NEXT feature's session, never by this one — then Rule A5, the first unchecked feature in
`docs/roadmap/STATUS.md`. State the open-findings count as the script reads it at C3, and "Operator
questions open: 0".
