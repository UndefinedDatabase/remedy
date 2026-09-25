STEP F023 R10 — THE CLOSING ROUND: BOOK ROUND 9, ROTATE THE LEDGER, ACCEPT F023 IN STATUS WITH ITS README PINS, OPEN THE PULL REQUEST

GOAL
Book round 9's PASS, rotate the finding ledger into its archive, flip F023's STATUS line to `[x]`
with the README's accepted count, Tier 5 Done cell and Tier 5 prose in the same commit, and open
the pull request into `main`. F023 registered no finding, so there is no ownership step; F023 is
not a findings-paydown feature, so it registers nothing.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f023-r10-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f023-r10/`           READ-ONLY. The reviewer's block, texts, builder and controls.
  `.remedy-wt/f023-r10-sim/`       The reviewer's simulated tree; do not touch.
  `.remedy-wt/f023-r10-dry/`       The reviewer's authoring tree; do not touch.
  `.remedy-wt/f023-r10-worker/`    YOURS for logs, captures and scripts; create it if absent.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, `ln`, `npm ci`, `npm install`, process substitution, command
substitution, `cd <dir> && git ...`, and multi-operation one-liners chained with `;` or `&&`
outside a `bash -c`. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use
`git -C <path>` rather than `cd`. Put multi-step code in a scratch Python file under your
directory. The `remedy` CLI may be denied: run `python3 -m apps.cli.main ...`. Never use
`git stash` in any form.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`: report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f023-semantic-zoom-l0-l3`, and `git log --oneline -1` must read `940d8174`.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f023-r10/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `gh pr list --state open --json number,headRefName` as found;
   the second must be EMPTY.

PAYLOADS — under `.remedy-wt/f023-r10-payloads/`, printed by the reviewer's builder
(lines = newline count). Verify each BEFORE using it and report every reading.

| file | lines | bytes | sha256 |
|---|---|---|---|
| closure.diff | 57 | 3573 | d451d6e27694b5efa62bb17090bfa4fbed6d5c29755cf6fa0589e6926bf51968 |
| ledger.diff | 10 | 6102 | fa0ec064350fa23dbff3a9ed18fe4197e665380c4a70ce9113ae517077e98316 |
| plan.md | 28 | 930 | 326bd57570bf1c8e0a93f51b5cb55afa30d381885fafeb5eda05bbd0352f8607 |
| pr_body.md | 67 | 3772 | c9993e7ab0650231b3eac4313d5e30c7ec4e464b3bd580169e28d741cfbd7bfd |
| status_line.txt | 1 | 395 | 206ee8ee8d199a919227b46ab27dffb8247ef0194aa5d288e51e5eaf36bd2c33 |

`ledger.diff` appends round 9's `Gate:` entry to `.agent/live_review.md`. `plan.md` is a REWRITE of
`.agent/plan.md`. `closure.diff` flips F023's STATUS line to `[x]` and moves the README's accepted
count, its Tier 5 Done cell and its Tier 5 prose. `pr_body.md` is the pull request's description,
passed to `gh` as a file. `status_line.txt` is the exact STATUS line `closure.diff` writes, used
only for G4's proof. The `.diff` files go on with `git apply --check` then `git apply`. Never retype
or edit a payload; copy with `shutil.copyfile`.

BUNDLE — commits C1 to C4 and then the pull request, in this order.

C1 — `.agent/authored/f023-r10-block.md` := this block; `.agent/authored/f023-r10-<name>` for each
  payload, keeping its file name. Byte for byte, with `shutil.copyfile`.
  Subject: `F023 R10 C1: copy round 10 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 163. Report the number you measure, and STOP
  rather than commit if it is 500 or more.

C2 — `git apply` ledger.diff → `.agent/live_review.md` · `.agent/plan.md` := plan.md.
  Subject: `F023 R10 C2: book round 9's PASS, the package READY_FOR_REVIEW`
  Expected by `git show --numstat` (insertions/deletions): 2/0 live_review.md, 7/8 plan.md.

C3 — THE ROTATION, its own commit, paths `.agent/live_review.md` and
  `.agent/live_review_archive.md` ONLY (operator amendment amend0905-throughput, AFTER the verdict
  booking and BEFORE the STATUS flip): `python3 scripts/rotate_live_review.py`. Report its printed
  output in full.
  Subject: `F023 R10 C3: rotate the finding ledger into its archive`
  Expected (insertions/deletions): 0/16 live_review.md, 16/0 live_review_archive.md.

C4 — THE CLOSURE COMMIT, exactly these paths and no others: `docs/roadmap/STATUS.md`, `README.md`
  and `.agent/handoff.md`. `git apply` closure.diff, run G4 on the working tree, then rewrite
  `.agent/handoff.md` per `docs/agents/handback_template.md` as the closure handback, then run G5,
  then commit. The handback names, each spelled exactly as below, the package
  `remedy-review-20260925-052148-READY_FOR_REVIEW.zip`, its SHA-256
  `6e041624017f41e1644f71f3d8c18ae8dd4d677b1d8df4fe6206f89b6f76b4bb`, its directory
  `/home/decodeux/Repos/remedy-history/zips`, the evidence job `f023r9e1001` and the accepted head
  `54e5ffd2485bf90c405f5ad662b7d86be8dd3eb9`, all from round 9; and it does NOT name a pull
  request number, which does not exist when it is written. There is no
  `scripts/self_use_queue.json` edit: the closure's self-use track answered NONE
  (`.agent/selfuse_f023/result.txt`).
  Subject: `F023 R10 C4: accept F023 in STATUS with its README pins`
  Expected for the two applied files (insertions/deletions): 17/2 README.md, 1/1 STATUS.md.
  Then `git push origin feature/f023-semantic-zoom-l0-l3`.

THE PULL REQUEST — after C4 and its push:
  `gh pr create --base main --head feature/f023-semantic-zoom-l0-l3 --title "F023 — Semantic zoom L0–L3" --body-file .remedy-wt/f023-r10-payloads/pr_body.md`.
  DO NOT MERGE IT. Report the number and URL in your final reply only.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f023-r10-*` copies C1 makes,
   `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/roadmap/STATUS.md`, `README.md` and `.agent/handoff.md`. Report the set you measure with
   `git diff --name-only 940d8174` over the range to C4.
4. C4 is the LAST commit on this branch (Rule A4). Nothing follows it except, if the reviewer's
   closure gate asks for one, a commit whose path set is exactly `.agent/candidates.md` — which
   this block does not order and you never write on your own initiative.
5. If any gate goes red, STOP before C4: commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. A closure that cannot be proved is not closed.
6. NOTHING IS MERGED. No `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
7. Delete nothing you did not create: every `remedy/job-*` branch, every `.remedy-wt/job-*`
   worktree and the reviewer's worktrees whose names begin `.remedy-wt/f015-`, `.remedy-wt/f020-`, `.remedy-wt/f023-` or `.remedy-wt/f284-` stay.
8. DO NOT run the full suite: this feature's run is committed at
   `.agent/authored/f023-closure-suite.txt`.

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G4 run before the handback is written, and
the handback states their readings. G5 runs after the handback is written and before C4 is
committed, so its readings go in your final reply, not the handback.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 committed `.agent/authored/f023-r10-*` blob, read with `git show <C1>:<path>`, compared byte for
 byte with its source (the block copy against `.remedy-wt/f023-r10/block.md`). One reading per
 file, all equal.

G2 THE BOOKING — at C2, read with `git show <C2>:<path>`, each equal to the reviewer's simulation:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 313141 | 5bee8c5621bd681e8bcd1dc1b3c49899ab4b984f24fe0761b97feda5bf0d3e8f |
 | .agent/plan.md | 930 | 326bd57570bf1c8e0a93f51b5cb55afa30d381885fafeb5eda05bbd0352f8607 |
 Also: among the lines C2's diff ADDS, those beginning `Gate: F023 R9 — ` (1); and the open set by
 distinct id via `open_finding_ids` from `scripts/rotate_live_review.py` at `940d8174` and at C2 —
 the reviewer read R-1008 alone at both. Report yours beside each.

G3 THE ROTATION — at C3: the reviewer's simulation of `python3 scripts/rotate_live_review.py`
 printed, line for line:
 gate records moved: 8
 finding pairs moved: 0 (0 records)
 old ledger size: 313141 bytes
 new ledger size: 296371 bytes
 old archive size: 4976495 bytes
 new archive size: 4993265 bytes
 open findings before: 1
 open findings after: 1
 and left the two ledger files at:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 296371 | 87742b92b88379339fd9aabe28b83961c8cb255cfb82b20d134ffd9e2ad679ad |
 | .agent/live_review_archive.md | 4993265 | 44772b348a7d24a9db4c2e38d6f4c55bab38ba6be74fc1bf75e87a6ff52bf541 |
 Report yours beside each, and C3's path set, which is the two ledger files and nothing else.

G4 THE CLOSURE EDITS AND THE TREE — with closure.diff applied, before the handback is written:

 | path | bytes | sha256 |
 |---|---|---|
 | docs/roadmap/STATUS.md | 51749 | dc043ed7cbd4716df30ba0f559ac839c710de2b8e50ef3e4e3b2a847169e2b16 |
 | README.md | 31191 | 864dc8f21bff00d7ccf7091d7cedbf6fefdce04e1345bd198b5fc22789f3dcdb |
 Also: the count of lines of
 `docs/roadmap/STATUS.md` equal to the one line of status_line.txt, byte for byte, which must be 1;
 serially,
 `bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'`,
 which the reviewer's dry run over the same tree WITHOUT the golden path read as
 `395 passed, 1 skipped` at exit 0; then `python3 -m apps.cli.main integrity check --json`, all six
 checks `pass` at `fail_count` 0; and `python3 -m apps.cli.main integrity block
 .remedy-wt/f023-r10/block.md`, real exit code 0 with every item `[OK]`. The reviewer red-controlled
 the pins there: with the accepted count left at 100 the selection read `1 failed, 394 passed, 1 skipped`, and with
 the STATUS line left `[~]` it read `3 failed, 392 passed, 1 skipped`. Report yours beside each.

G5 THE HANDBACK'S PINS — after the handback is written, before C4 is committed: for each of the
 five strings C4 names — the package filename, its SHA-256, its directory, the evidence job and
 the accepted head — the count of its occurrences in the new `.agent/handoff.md`, each of which
 must be at least 1; and the count of the string `pull/` in it, which must be 0. If any count
 misses, fix the handback and measure again before committing; report both measurements.

G6 THE PUSH AND THE PULL REQUEST — after C4: `git log --oneline -n 5`, showing C4, C3, C2, C1 and
 `940d8174`; `git status --porcelain` empty; the push's real outcome; the pull request's number
 and URL; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft` showing
 exactly that one pull request, from this branch into `main`, not a draft. These go in your final
 reply, not the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, and AGENTS.md's
item-status table with one row per C-item, the pull request and each gate: state block, the
per-commit changed-files table with the insertions git MEASURED beside the ones this block
expected, every gate reading G1 to G4 with its real exit code, the deviations, and the next
action. Your Session section reads SESSION 1 of feature F023, round 10, and says in one sentence
how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), then the Open PR
Gate — the pull request this round opens is merged by the NEXT feature's session, never by this
one — and then Rule A5, the first unchecked feature in `docs/roadmap/STATUS.md`. State the
open-findings count, 1, and the operator-questions count, 3.
