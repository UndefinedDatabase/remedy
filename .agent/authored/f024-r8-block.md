STEP F024 R8 — THE CLOSING ROUND: BOOK ROUND 7, ROTATE THE LEDGER, ACCEPT F024 IN STATUS WITH ITS README PINS, OPEN THE PULL REQUEST

GOAL
Book round 7's PASS, rotate the finding ledger into its archive, flip F024's STATUS line to `[x]`
with the README's accepted count, Tier 5 Done cell and Tier 5 prose in the same commit, and open
the pull request into `main`. F024 registered no finding, so there is no ownership step; F024 is
not a findings-paydown feature, so it registers nothing.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f024-r8-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f024-r8/`           READ-ONLY. The reviewer's block, texts, builder and controls.
  `.remedy-wt/f024-r8-sim/`       The reviewer's simulated tree; do not touch.
  `.remedy-wt/f024-r8-dry/`       The reviewer's authoring tree; do not touch.
  `.remedy-wt/f024-r8-worker/`    YOURS for logs, captures and scripts; create it if absent.

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
   `feature/f024-phase-timeline-scrubber`, and `git log --oneline -1` must read `59ee84e4`.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f024-r8/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `gh pr list --state open --json number,headRefName` as found;
   the second must be EMPTY.

PAYLOADS — under `.remedy-wt/f024-r8-payloads/`, printed by the reviewer's builder
(lines = newline count). Verify each BEFORE using it and report every reading.

| file | lines | bytes | sha256 |
|---|---|---|---|
| closure.diff | 57 | 3903 | 1a4bb0c9b0b51f7606ea1ec98686c8fc049e7b1ddc70acb8e059e8ed148debd8 |
| ledger.diff | 10 | 6157 | bcb63619df95ed9dd0edd636a9b680358675b4be6e9a471a67b5e2074f851717 |
| plan.md | 28 | 939 | ba905eb3bc560879445dc9063a7fd10d6c2c077cb9a01d148660986f69436dfa |
| pr_body.md | 64 | 3766 | 24f29a751141417916a80258efa09a399274631718a5d35c8fcc1d118cd85275 |
| status_line.txt | 1 | 402 | 8e33ff67a040a9bd6a5e3b9bec0a0938ab568c09efbbe7119b5eae75e631a268 |

`ledger.diff` appends round 7's `Gate:` entry to `.agent/live_review.md`. `plan.md` is a REWRITE of
`.agent/plan.md`. `closure.diff` flips F024's STATUS line to `[x]` and moves the README's accepted
count, its Tier 5 Done cell and its Tier 5 prose. `pr_body.md` is the pull request's description,
passed to `gh` as a file. `status_line.txt` is the exact STATUS line `closure.diff` writes, used
only for G4's proof. The `.diff` files go on with `git apply --check` then `git apply`. Never retype
or edit a payload; copy with `shutil.copyfile`.

BUNDLE — commits C1 to C4 and then the pull request, in this order.

C1 — `.agent/authored/f024-r8-block.md` := this block; `.agent/authored/f024-r8-<name>` for each
  payload, keeping its file name. Byte for byte, with `shutil.copyfile`.
  Subject: `F024 R8 C1: copy round 8 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 160. Report the number you measure, and STOP
  rather than commit if it is 500 or more.

C2 — `git apply` ledger.diff → `.agent/live_review.md` · `.agent/plan.md` := plan.md.
  Subject: `F024 R8 C2: book round 7's PASS, the package READY_FOR_REVIEW`
  Expected by `git show --numstat` (insertions/deletions): 2/0 live_review.md, 7/6 plan.md.

C3 — THE ROTATION, its own commit, paths `.agent/live_review.md` and
  `.agent/live_review_archive.md` ONLY (operator amendment amend0905-throughput, AFTER the verdict
  booking and BEFORE the STATUS flip): `python3 scripts/rotate_live_review.py`. Report its printed
  output in full.
  Subject: `F024 R8 C3: rotate the finding ledger into its archive`
  Expected (insertions/deletions): 0/20 live_review.md, 20/0 live_review_archive.md.

C4 — THE CLOSURE COMMIT, exactly these paths and no others: `docs/roadmap/STATUS.md`, `README.md`
  and `.agent/handoff.md`. `git apply` closure.diff, run G4 on the working tree, then rewrite
  `.agent/handoff.md` per `docs/agents/handback_template.md` as the closure handback, then run G5,
  then commit. The handback names, each spelled exactly as below, the package
  `remedy-review-20260925-082755-READY_FOR_REVIEW.zip`, its SHA-256
  `1c4b4b358b97b54252a665e60acd3eaaedb134b8b3b0cbbe5ee36d80e60289e6`, its directory
  `/home/decodeux/Repos/remedy-history/zips`, the evidence job `f024r7e1001` and the accepted head
  `b650ced4b1d0fef4c9156de0b217cbad7a76bef7`, all from round 7; and it does NOT name a pull
  request number, which does not exist when it is written. There is no
  `scripts/self_use_queue.json` edit: the closure's self-use track answered NONE
  (`.agent/selfuse_f024/result.txt`).
  Subject: `F024 R8 C4: accept F024 in STATUS with its README pins`
  Expected for the two applied files (insertions/deletions): 17/2 README.md, 1/1 STATUS.md.
  Then `git push origin feature/f024-phase-timeline-scrubber`.

THE PULL REQUEST — after C4 and its push:
  `gh pr create --base main --head feature/f024-phase-timeline-scrubber --title "F024 — Phase timeline with scrubber" --body-file .remedy-wt/f024-r8-payloads/pr_body.md`.
  DO NOT MERGE IT. Report the number and URL in your final reply only.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f024-r8-*` copies C1 makes,
   `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/roadmap/STATUS.md`, `README.md` and `.agent/handoff.md`. Report the set you measure with
   `git diff --name-only 59ee84e4` over the range to C4.
4. C4 is the LAST commit on this branch (Rule A4). Nothing follows it except, if the reviewer's
   closure gate asks for one, a commit whose path set is exactly `.agent/candidates.md` — which
   this block does not order and you never write on your own initiative.
5. If any gate goes red, STOP before C4: commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. A closure that cannot be proved is not closed.
6. NOTHING IS MERGED. No `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
7. Delete nothing you did not create: every `remedy/job-*` branch, every `.remedy-wt/job-*`
   worktree and the reviewer's worktrees whose names begin `.remedy-wt/f015-`, `.remedy-wt/f020-`,
   `.remedy-wt/f023-`, `.remedy-wt/f024-` or `.remedy-wt/f284-` stay.
8. DO NOT run the full suite: this feature's run is committed at
   `.agent/authored/f024-closure-suite.txt`.

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G4 run before the handback is written, and
the handback states their readings. G5 runs after the handback is written and before C4 is
committed, so its readings go in your final reply, not the handback.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 committed `.agent/authored/f024-r8-*` blob, read with `git show <C1>:<path>`, compared byte for
 byte with its source (the block copy against `.remedy-wt/f024-r8/block.md`). One reading per
 file, all equal.

G2 THE BOOKING — at C2, read with `git show <C2>:<path>`, each equal to the reviewer's simulation:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 311161 | 13c07741e2c2105a151d4338bc999a3f642f3a2d1cc7b5720446e692755cce5c |
 | .agent/plan.md | 939 | ba905eb3bc560879445dc9063a7fd10d6c2c077cb9a01d148660986f69436dfa |
 Also: among the lines C2's diff ADDS, those beginning `Gate: F024 R7 — ` (1); and the open set by
 distinct id via `open_finding_ids` from `scripts/rotate_live_review.py` at `59ee84e4` and at C2 —
 the reviewer read R-1008 alone at both. Report yours beside each.

G3 THE ROTATION — at C3: the reviewer's simulation of `python3 scripts/rotate_live_review.py`
 printed, line for line:
 gate records moved: 10
 finding pairs moved: 0 (0 records)
 old ledger size: 311161 bytes
 new ledger size: 292216 bytes
 old archive size: 4993265 bytes
 new archive size: 5012210 bytes
 open findings before: 1
 open findings after: 1
 and left the two ledger files at:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 292216 | 0ddd96d6df7623ed6932d829a06f413b8898ae38ca5cd91358286c4febbc2ed0 |
 | .agent/live_review_archive.md | 5012210 | 95c0d02ec6788a1067a8cbeaf2eff92a5c908503e890acf1d16081ba88c1e90f |
 Report yours beside each, and C3's path set, which is the two ledger files and nothing else.

G4 THE CLOSURE EDITS AND THE TREE — with closure.diff applied, before the handback is written:

 | path | bytes | sha256 |
 |---|---|---|
 | docs/roadmap/STATUS.md | 52107 | c8058ed59f6ac736cc1f64c390d561e7c120ff3fbd97a9c9011d308813d60869 |
 | README.md | 32262 | 85f398bdc88f1738d58e7b958581d9d10b815309a659b0662e1e045a4b5c0f0a |
 Also: the count of lines of
 `docs/roadmap/STATUS.md` equal to the one line of status_line.txt, byte for byte, which must be 1;
 serially,
 `bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'`,
 which the reviewer's dry run over the same tree WITHOUT the golden path read as
 `395 passed, 1 skipped` at exit 0; then `python3 -m apps.cli.main integrity check --json`, all six
 checks `pass` at `fail_count` 0; and `python3 -m apps.cli.main integrity block
 .remedy-wt/f024-r8/block.md`, real exit code 0 with every item `[OK]`. The reviewer red-controlled
 the pins there: with the accepted count left at 101 the selection read `1 failed, 394 passed, 1 skipped`, and with
 the STATUS line left `[~]` it read `3 failed, 392 passed, 1 skipped`. Report yours beside each.

G5 THE HANDBACK'S PINS — after the handback is written, before C4 is committed: for each of the
 five strings C4 names — the package filename, its SHA-256, its directory, the evidence job and
 the accepted head — the count of its occurrences in the new `.agent/handoff.md`, each of which
 must be at least 1; and the count of the string `pull/` in it, which must be 0. If any count
 misses, fix the handback and measure again before committing; report both measurements.

G6 THE PUSH AND THE PULL REQUEST — after C4: `git log --oneline -n 5`, showing C4, C3, C2, C1 and
 `59ee84e4`; `git status --porcelain` empty; the push's real outcome; the pull request's number
 and URL; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft` showing
 exactly that one pull request, from this branch into `main`, not a draft. These go in your final
 reply, not the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, and AGENTS.md's
item-status table with one row per C-item, the pull request and each gate: state block, the
per-commit changed-files table with the insertions git MEASURED beside the ones this block
expected, every gate reading G1 to G4 with its real exit code, the deviations, and the next
action. Your Session section reads SESSION 1 of feature F024, round 8, and says in one sentence
how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), then the Open PR
Gate — the pull request this round opens is merged by the NEXT feature's session, never by this
one — and then Rule A5, the first unchecked feature in `docs/roadmap/STATUS.md`. State the
open-findings count, 1, and the operator-questions count, 3.
