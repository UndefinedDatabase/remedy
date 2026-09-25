STEP F026 R8 — THE CLOSING ROUND: BOOK ROUND 7, ROTATE THE LEDGER, ACCEPT F026 IN STATUS WITH ITS README PINS AND THE SELF-USE ITEM'S CONSUMED_BY, OPEN THE PULL REQUEST

GOAL
Book round 7's PASS, rotate the finding ledger into its archive, flip F026's STATUS line to `[x]`
with the README's accepted count, Tier 5 Done cell and Tier 5 prose and SU-031's `consumed_by` in
the same commit, and open the pull request into `main`. Every open finding is already owned by F285,
so there is no ownership step; F026 is not a findings-paydown feature, so it registers nothing.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, write the handback. You never issue a
verdict and never merge. Read first `.agent/authored/f025-r11-block.md`, which this round follows, and
`docs/roadmap/STATUS_closure_protocol.md` algorithm steps 4 and 5.

THE DIRECTORIES
  `.remedy-wt/f026-r8/`          READ-ONLY. This block, its payloads and the reviewer's builder.
  `.remedy-wt/f026-r8-worker/`   YOURS for logs and scripts; create it if absent. Both gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR: `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`,
`cp`, process and command substitution, `cd <dir> && git ...`, and one-liners chained with `;` or
`&&` outside a `bash -c`. Capture exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C
<path>`; never `cd` into a worktree. Copy and hash with python (`shutil.copyfile`). Never run npm or
npx, never `git stash`.

COMMIT TRAILER — every commit ends with exactly this line:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop.
2. In `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain` empty,
   `git branch --show-current` `feature/f026-task-edit-runtime`, `git log --oneline -1` `d1d487f9`.
3. Measure this block's line count and sha256 (`.remedy-wt/f026-r8/block.md`) against your
   delegation message's readings; stop if either differs.
4. Report `git worktree list`, and `gh pr list --state open --json number,headRefName`, which must be
   EMPTY.

PAYLOADS — under `.remedy-wt/f026-r8/`, lines = newline count; verify each BEFORE use:
| file | lines | bytes | sha256 |
|---|---|---|---|
| build.py | 94 | 4788 | 7f71bc64fab21d4c6283491a3fe7774e00a40b8e3db2201fd3f8af2127f0ea4f |
| closure.diff | 69 | 8534 | cb9d220ea582bb33f878ff312acc7ecba2a6312328911d81aaf6883c48f13ec7 |
| ledger.md | 2 | 2106 | 0b1b97c8b69593360e4c3f165d021e59e55102667a967398f7ffec7d8fc2c5b0 |
| plan.md | 27 | 872 | b71a56fd8f5324d32b9d4616d2e6ad1b2b69dac456efaa4b1767235db12cceb5 |
| pr_body.md | 74 | 4719 | 3e1e87084484db1255829f4df33796d43d59c5913cd453cd462dca27719a423f |
| readme_para.txt | 13 | 1090 | e9a34ccb8471361ccf2113c55c54bd77779d31dd8a8ff78aa3ba74afaa957d9f |
| status_line.txt | 1 | 394 | ba53cb4ae6ba5c4893e09561a4033add40f51162fed6560bdca05e754ac61a08 |
`ledger.md` is appended to `.agent/live_review.md` (it starts with its own blank line); `plan.md`
REWRITES `.agent/plan.md`; `closure.diff` flips F026's STATUS line, moves the README's accepted count,
Tier 5 Done cell and Tier 5 prose, and sets SU-031's `consumed_by` to `F026` — it goes on with `git
apply --check` then `git apply`; `status_line.txt` is the exact STATUS line closure.diff writes, for
G4's proof; `pr_body.md` is the pull request's description, passed to `gh` as a file;
`readme_para.txt` and `build.py` are the reviewer's sources for closure.diff, copied for the record and
never applied or run.

BUNDLE — C1 to C4, then the pull request.
C1 COPIES: `.agent/authored/f026-r8-block.md` := this block and each payload as
   `.agent/authored/f026-r8-<name>`. Subject `F026 R8 C1: copy round 8 block and payloads`. Its
   insertions are this block's line count plus 280.
C2 THE BOOKING: the ledger append and the plan rewrite. Subject `F026 R8 C2: book round 7's PASS, the
   package READY_FOR_REVIEW`. Expected by `git show --numstat`: 2/0 `.agent/live_review.md`, 7/9 `.agent/plan.md`.
C3 THE ROTATION, its own commit, paths `.agent/live_review.md` and `.agent/live_review_archive.md`
   ONLY: `python3 scripts/rotate_live_review.py`; report its printed output in full. Subject
   `F026 R8 C3: rotate the finding ledger into its archive`. Expected: 0/42 `.agent/live_review.md`, 42/0 `.agent/live_review_archive.md`.
C4 THE CLOSURE COMMIT, exactly these paths: `docs/roadmap/STATUS.md`, `README.md`,
   `scripts/self_use_queue.json` and `.agent/handoff.md`. `git apply` closure.diff, run G4 on the
   working tree, rewrite `.agent/handoff.md` per `docs/agents/handback_template.md` as the closure
   handback, run G5, then commit. The handback names, spelled exactly so, the package
   `remedy-review-20260925-224758-READY_FOR_REVIEW.zip`, its SHA-256
   `8a9aa2d963b00ecad738490efc6df69df72dc782252a2c0f9f16d6cfb9cd6bc8`, its directory
   `/home/decodeux/Repos/remedy-history/zips`, the evidence job `f026r7e1001` and the accepted head
   `3cb0798d20a293f9954074ff9b2c4ae32704035c`, all from round 7; and it names NO pull request
   number, which does not exist when it is written. Subject `F026 R8 C4: accept F026 in STATUS with
   its README pins and the self-use item's consumed_by`. Expected for the three applied files:
   16/2 `README.md`, 1/1 `docs/roadmap/STATUS.md`, 1/1 `scripts/self_use_queue.json`. Then `git push origin feature/f026-task-edit-runtime`.
THE PULL REQUEST, after C4 and its push: `gh pr create --base main --head
   feature/f026-task-edit-runtime --title "F026 — Task edit at runtime" --body-file
   .remedy-wt/f026-r8/pr_body.md`. DO NOT MERGE IT. Report its number and URL in your final reply
   only.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f026-r8-*` copies,
   `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json` and `.agent/handoff.md`.
4. C4 is the LAST commit on this branch (Rule A4). Nothing follows it.
5. If any gate goes red, STOP before C4: commit and push what is verified, write the handoff under
   AGENTS.md "If Blocked", and hand back. A closure that cannot be proved is not closed.
6. NOTHING IS MERGED: no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
7. Delete nothing you did not create; every existing worktree and `remedy/job-*` branch stays.
8. DO NOT run the full suite: this feature's run is `.agent/authored/f026-closure-suite.txt`.

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G4 run before
the handback is written, and the handback states their readings; G5 runs after the handback is
written and before C4 is committed, so its readings go in your final reply.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f026-r8-*` payload copy byte-equal to its source by `git show <C1>:<path>`.
G2 THE BOOKING, at C2, read with `git show <C2>:<path>`, each equal to the reviewer's simulation:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 346516 | 5377bff9549cefdead6187a035a034533faa9fd980bcc1f7b867ca46180edf9e |
   | .agent/plan.md | 872 | b71a56fd8f5324d32b9d4616d2e6ad1b2b69dac456efaa4b1767235db12cceb5 |
   and `open_finding_ids` over the ledger at C2 — the simulation read `['R-1008', 'R-1055', 'R-1057',
   'R-1058', 'R-1064']`.
G3 THE ROTATION, at C3: the reviewer's simulation of `python3 scripts/rotate_live_review.py` printed,
   line for line:
   gate records moved: 11
   finding pairs moved: 5 (10 records)
   old ledger size: 346516 bytes
   new ledger size: 305594 bytes
   old archive size: 5047001 bytes
   new archive size: 5087923 bytes
   open findings before: 5
   open findings after: 5
   and left the two ledger files at:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 305594 | f469665adf7d411069780000cf803a0263fe6869094a2de6f96a307aa4d40646 |
   | .agent/live_review_archive.md | 5087923 | 3e4c1a9aaf8ef7849dea1204c9a0718defd6e5472be2d852938c2e2122a0202b |
   Report yours beside each, and C3's path set, which is the two ledger files and nothing else.
G4 THE CLOSURE EDITS AND THE TREE, with closure.diff applied, before the handback is written:
   | path | bytes | sha256 |
   |---|---|---|
   | docs/roadmap/STATUS.md | 52859 | d06a49648597faa946cb6ad6d9bc2cdb10fb41640230e8761f5ab5025ead9d9b |
   | README.md | 34527 | 84c8bc4696ac49313a1add1d1eef29c2bcbe97e062b64fbc8e68b7d5e927706b |
   | scripts/self_use_queue.json | 132155 | 42e21c50581fb4cc64f37217b2870eb476dc4e8fc0342cd4b2798f7800f116e5 |
   the count of lines of `docs/roadmap/STATUS.md` equal to the one line of status_line.txt, which
   must be 1; serially, `python3 -m pytest -q -p no:cacheprovider tests/docs/
   tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py
   tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py
   tests/cli/test_golden_path.py`, which the simulation read WITHOUT the golden path as `424 passed in 2.30s`
   at exit 0; then `python3 -m apps.cli.main integrity check --json`, six `pass` at `fail_count` 0.
   The reviewer red-controlled the pins: with the accepted count left at 103, `tests/docs/` read
   `1 failed, 326 passed in 1.28s` at exit 1.
G5 THE HANDBACK'S PINS, after the handback is written and before C4 is committed: for each of the five
   strings C4 names, its count in the new `.agent/handoff.md`, each at least 1; and the count of
   `pull/` in it, which must be 0.
G6 AFTER C4: `git log --oneline -n 5`, showing C4, C3, C2, C1 and `d1d487f9`; `git status
   --porcelain` empty; the push's real outcome; the pull request's number and URL; and `gh pr list
   --state open --json number,headRefName,baseRefName,isDraft` showing exactly that one pull request,
   from this branch into `main`, not a draft. These go in your final reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block, the
per-commit changed-files table with the `git show --numstat` counts you measured beside the ones
above, every gate reading G1 to G4 with its real exit code, the authored-text proofs, the item-status
table AGENTS.md requires (one row per commit, the pull request and each gate), the deviations, and
the next action. Session section: SESSION 1 of feature F026, round 8, plus one sentence on how much
context you had left. `## Next`: Phase 1 rule 1, then the Open PR Gate — the pull request this round
opens is merged by the NEXT feature's session, never by this one — then Rule A5, the first unchecked
feature in `docs/roadmap/STATUS.md`. State the open-findings count as the script reads it at C3, and
"Operator questions open: <the count of `### Q` headings>".
