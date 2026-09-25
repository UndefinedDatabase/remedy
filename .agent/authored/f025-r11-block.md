STEP F025 R11 — THE CLOSING ROUND: BOOK ROUND 10, ROTATE THE LEDGER, ACCEPT F025 IN STATUS WITH ITS README PINS AND THE SELF-USE ITEM'S CONSUMED_BY, OPEN THE PULL REQUEST

GOAL
Book round 10's PASS, rotate the finding ledger into its archive, flip F025's STATUS line to `[x]`
with the README's accepted count, Tier 5 Done cell and Tier 5 prose and SU-030's `consumed_by` in
the same commit, and open the pull request into `main`. Every open finding F025 owned is already
owned by F285, so there is no ownership step; F025 is not a findings-paydown feature, so it
registers nothing.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, write the handback. You never
issue a verdict and never merge. Read first `.agent/authored/f024-r8-block.md`, which this round
follows, and `docs/roadmap/STATUS_closure_protocol.md` algorithm steps 4 and 5.

THE DIRECTORIES
  `.remedy-wt/f025-r11/`          READ-ONLY. This block, its payloads and the reviewer's builder.
  `.remedy-wt/f025-r11-worker/`   YOURS for logs and scripts; create it if absent. Both gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, command substitution, `cd <dir> && git ...`, and
multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C <path>`, never `cd` your shell into a worktree.
Copy and hash with python (`shutil.copyfile`). Never run npm or npx, never `git stash`.

COMMIT TRAILER — every commit ends with exactly this line:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop.
2. In the primary checkout `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain`
   must be empty, `git branch --show-current` must read `feature/f025-pause-resume`, and
   `git log --oneline -1` must read `21aa3097`.
3. Measure this block's line count and sha256 (`.remedy-wt/f025-r11/block.md`) and compare both
   with your delegation message's readings; stop if either differs.
4. Report `git worktree list`, and `gh pr list --state open --json number,headRefName`, which
   must be EMPTY.

PAYLOADS — under `.remedy-wt/f025-r11/`, lines = newline count; verify each BEFORE use:
| file | lines | bytes | sha256 |
|---|---|---|---|
| build.py | 94 | 4851 | 65206a60685e8a35225cac1ceeb206f75ffcec7bb78af8845494aea5a1539285 |
| closure.diff | 71 | 7869 | 61ac6e1f9533b901563f7d5fde571a4641181c9be0c4646652778bb508ffcc45 |
| ledger.md | 2 | 2054 | 6b5156f7ec0f8a776b81eeb06ab64d062a3fecdb9c58ce5de26699780e6bb089 |
| plan.md | 27 | 919 | 26e264db5b56730d4e92b0e9330d41326ed8edea45f17ffc627740bc7409f6f2 |
| pr_body.md | 72 | 4597 | d57cc2e1a4c041fa8a1e06032351095e047efe8f2ee7f5f22acc1cead88fbe2c |
| readme_para.txt | 15 | 1173 | f297eda0dd146cf76cbce02f4ba109d78eca9fcd42655c5239b1a42e2c74a2b4 |
| status_line.txt | 1 | 442 | fe1b07fe32f88cf36e5828f2a14f97dcdf1a4273b657ab20fa2d534095ff3705 |
`ledger.md` is appended to `.agent/live_review.md` (it starts with its own blank line); `plan.md`
REWRITES `.agent/plan.md`; `closure.diff` flips F025's STATUS line, moves the README's accepted
count, Tier 5 Done cell and Tier 5 prose, and sets SU-030's `consumed_by` to `F025` — it goes on
with `git apply --check` then `git apply`; `status_line.txt` is the exact STATUS line closure.diff
writes, for G4's proof; `pr_body.md` is the pull request's description, passed to `gh` as a file;
`readme_para.txt` and `build.py` are the reviewer's sources for closure.diff, copied for the record
and never applied or run.

BUNDLE — C1 to C4, then the pull request.
C1 COPIES: `.agent/authored/f025-r11-block.md` := this block and each payload as
    `.agent/authored/f025-r11-<name>`. Subject `F025 R11 C1: copy round 11 block and payloads`.
    Expected by `git show --numstat`: this block's line count plus 282, that is the block copy's own lines and 94/0 `.agent/authored/f025-r11-build.py`, 71/0 `.agent/authored/f025-r11-closure.diff`, 2/0 `.agent/authored/f025-r11-ledger.md`, 27/0 `.agent/authored/f025-r11-plan.md`, 72/0 `.agent/authored/f025-r11-pr_body.md`, 15/0 `.agent/authored/f025-r11-readme_para.txt`, 1/0 `.agent/authored/f025-r11-status_line.txt`.
C2 THE BOOKING: the ledger append and the plan rewrite. Subject `F025 R11 C2: book round 10's
    PASS, the package READY_FOR_REVIEW`. Expected: 2/0 `.agent/live_review.md`, 6/8 `.agent/plan.md`.
C3 THE ROTATION, its own commit, paths `.agent/live_review.md` and `.agent/live_review_archive.md`
    ONLY: `python3 scripts/rotate_live_review.py`; report its printed output in full. Subject
    `F025 R11 C3: rotate the finding ledger into its archive`. Expected: 0/50 `.agent/live_review.md`, 50/0 `.agent/live_review_archive.md`.
C4 THE CLOSURE COMMIT, exactly these paths: `docs/roadmap/STATUS.md`, `README.md`,
    `scripts/self_use_queue.json` and `.agent/handoff.md`. `git apply` closure.diff, run G4 on the
    working tree, rewrite `.agent/handoff.md` per `docs/agents/handback_template.md` as the
    closure handback, run G5, then commit. The handback names, spelled exactly so, the package
    `remedy-review-20260925-174026-READY_FOR_REVIEW.zip`, its SHA-256
    `5202e21aed884f7ae6a8b79a852d2c4683436f2220d1a910d072cec01ac38e6f`, its directory
    `/home/decodeux/Repos/remedy-history/zips`, the evidence job `f025r10e1001` and the accepted
    head `f7b127bde0e2d705f0a8da49b1d9404d983048d4`, all from round 10; and it names NO pull request
    number, which does not exist when it is written. Subject `F025 R11 C4: accept F025 in STATUS
    with its README pins and the self-use item's consumed_by`. Expected for the three applied
    files: 18/2 `README.md`, 1/1 `docs/roadmap/STATUS.md`, 1/1 `scripts/self_use_queue.json`. Then `git push origin feature/f025-pause-resume`.
THE PULL REQUEST, after C4 and its push: `gh pr create --base main --head feature/f025-pause-resume
    --title "F025 — Pause/resume (global & per node)" --body-file
    .remedy-wt/f025-r11/pr_body.md`. DO NOT MERGE IT. Report its number and URL in your final
    reply only.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f025-r11-*` copies,
   `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json` and `.agent/handoff.md`.
4. C4 is the LAST commit on this branch (Rule A4). Nothing follows it.
5. If any gate goes red, STOP before C4: commit and push what is verified, write the handoff under
   AGENTS.md "If Blocked", and hand back. A closure that cannot be proved is not closed.
6. NOTHING IS MERGED: no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
7. Delete nothing you did not create; every existing worktree and `remedy/job-*` branch stays.
8. DO NOT run the full suite: this feature's run is `.agent/authored/f025-closure-suite.txt`.

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G4 run
before the handback is written, and the handback states their readings; G5 runs after the handback
is written and before C4 is committed, so its readings go in your final reply.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f025-r11-*` payload copy byte-equal to its source by `git show <C1>:<path>`
   (the block copy against `.remedy-wt/f025-r11/block.md`).
G2 THE BOOKING, at C2, read with `git show <C2>:<path>`, each equal to the reviewer's simulation:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 346741 | d14c863f3fc6da0779e5f0e350823c3edf311da428dcd7fd89fb631b2e81ada2 |
   | .agent/plan.md | 919 | 26e264db5b56730d4e92b0e9330d41326ed8edea45f17ffc627740bc7409f6f2 |
   and `open_finding_ids` over the ledger at C2 — the simulation read `['R-1008', 'R-1055', 'R-1057', 'R-1058']`.
G3 THE ROTATION, at C3: the reviewer's simulation of `python3 scripts/rotate_live_review.py`
   printed, line for line:
   gate records moved: 9
   finding pairs moved: 8 (16 records)
   old ledger size: 346741 bytes
   new ledger size: 311950 bytes
   old archive size: 5012210 bytes
   new archive size: 5047001 bytes
   open findings before: 4
   open findings after: 4
   and left the two ledger files at:
   | path | bytes | sha256 |
   |---|---|---|
   | .agent/live_review.md | 311950 | 8da88e531e3a9d0d446cd3ac66090ce887fce52b7953035769e46b5ebd8df475 |
   | .agent/live_review_archive.md | 5047001 | ba22f90ad33d1798cc3f4bfefb0efbff708f5950425a9c0b0ded7f6fd31d3acf |
   Report yours beside each, and C3's path set, which is the two ledger files and nothing else.
G4 THE CLOSURE EDITS AND THE TREE, with closure.diff applied, before the handback is written:
   | path | bytes | sha256 |
   |---|---|---|
   | docs/roadmap/STATUS.md | 52501 | 3b967b9c294d3c1cf8c886f92bdb37aaf806c98c60ccbef5c8512aa2ec3200ae |
   | README.md | 33436 | b3327ba9a39c78c6b6267353f8892cf09f287b11c859c2c5d6a5355d94f36c16 |
   | scripts/self_use_queue.json | 128171 | 1456337e4fa62d476bf632e3c6a438c095c019ee8740db8f5b27072051fd866e |
   the count of lines of `docs/roadmap/STATUS.md` equal to the one line of status_line.txt, which
   must be 1; serially, `python3 -m pytest -q -p no:cacheprovider tests/docs/
   tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py
   tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py
   tests/cli/test_golden_path.py`, which the simulation read WITHOUT the golden path as `424 passed in 2.39s` at exit 0;
   then `python3 -m apps.cli.main integrity check --json`, six `pass` at `fail_count` 0. The
   reviewer red-controlled the pins: with the accepted count left at 102, `tests/docs/` read
   `1 failed, 326 passed in 1.26s` at exit 1.
G5 THE HANDBACK'S PINS, after the handback is written and before C4 is committed: for each of the
   five strings C4 names, its count in the new `.agent/handoff.md`, each at least 1; and the count
   of `pull/` in it, which must be 0.
G6 AFTER C4: `git log --oneline -n 5`, showing C4, C3, C2, C1 and `21aa3097`; `git status
   --porcelain` empty; the push's real outcome; the pull request's number and URL; and `gh pr list
   --state open --json number,headRefName,baseRefName,isDraft` showing exactly that one pull
   request, from this branch into `main`, not a draft. These go in your final reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the `git show --numstat` counts you measured beside the
ones above, every gate reading G1 to G4 with its real exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit, the pull request and each gate), the
deviations, and the next action. Session section: SESSION 2 of feature F025, round 11, plus one
sentence on how much context you had left. `## Next`: Phase 1 rule 1, then the Open PR Gate — the
pull request this round opens is merged by the NEXT feature's session, never by this one — then
Rule A5, the first unchecked feature in `docs/roadmap/STATUS.md`. State the open-findings count as
the script reads it at C3, and "Operator questions open: <the count of `### Q` headings>".
