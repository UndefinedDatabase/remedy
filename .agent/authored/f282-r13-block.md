STEP F282 R13 — THE CLOSURE: BOOK ROUND 12, MOVE THE CARRIED IDS, ROTATE, REGISTER F284, ACCEPT F282 AND OPEN THE PULL REQUEST

GOAL
Book round 12's PASS and move R-0499, R-0950 and R-1008 to the next findings-paydown feature, F284,
in one commit; rotate the finding ledger as its own commit; register F284 — Findings paydown v3 as
its own commit (operator amendment amend0911-feedback rule B); flip F282's STATUS line to accepted
with the README's three pinned places in the same commit as the closure handback; and open the pull
request. The pull request is NEVER merged by the session that opens it.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. Every appliable byte of this round is a reviewer payload; you
author only the pull request's description and the handback.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f282-r13-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f282-r13-scratch/`   READ-ONLY. `sim.py` is the reviewer's dry run of C2 to C5 in a
      disposable worktree at `f6fd80de`: with every payload applied, `tests/docs/` read `327 passed`
      at exit 0 at C4 and again at C5; with the STATUS flip applied and the README left as C4
      leaves it, the same suite read `3 failed, 324 passed` at exit 1, the control proving the
      README's three places bind.
  `.remedy-wt/f282-r13-worker/`    YOURS for logs, scripts and the pull request body.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, `ln`, `npm ci`, `npm install`, process substitution,
`cd <dir> && git ...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`.
Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C <path>` rather than
`cd`. Put multi-step code in a scratch Python file under your directory. The `remedy` CLI is
denied: run `python3 -m apps.cli.main ...`. For the pull request body, write it to a scratch file
and pass `--body-file`. Never use `git stash` in any form, and never check out another commit in
the primary checkout.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f282-findings-paydown-v2`, and `git log --oneline -1` must read `f6fd80de`.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f282-r13-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.

PAYLOADS — under `.remedy-wt/f282-r13-payloads/`, printed by the reviewer's simulation
(lines = newline count). Verify each BEFORE using it and report every reading.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.diff | 34 | 11741 | c6acba4d56b83928f9de4dc83df53212224c017ef507aca374d297857452251f |
| plan.md | 27 | 916 | 1ff066cfdfb3b2ac3afaffa2a0be06b56ed28b098ba23bfc73fd3826d3d9e86e |
| registration.diff | 105 | 5629 | c13674b54855cf71bbdb07fcd30e8846d48972d602e1ef6d1e5ad5cb01767121 |
| closure.diff | 50 | 3389 | 5f25e7f06fa0deead61e7cf0458e315ecfaab977d370801294a43e033bcc5c9a |

Every `.diff` goes on with `git apply --check` then `git apply`, reading the payload file directly.
`ledger.diff` adds one superseding `Owner: F284 — ...` line at the end of the paragraphs of R-0499,
R-0950 and R-1008, and appends round 12's `Gate:` entry. `plan.md` is a REWRITE of
`.agent/plan.md`. `registration.diff` creates the NEW FILE at `docs/roadmap/features/T2_F284.md`,
inserts F284's line into `docs/roadmap/STATUS.md` directly after F019's under its own Tier 2 heading
with the Tier 5 list re-opened after it, raises `TOTAL_FEATURES` in
`tests/docs/test_docs_consistency.py` to 284 with its comment, and raises the README's registered
count and its Tier 2 total. `closure.diff` flips F282's STATUS line to `[x]` and moves the README's
accepted count, its Tier 2 Done cell and its Tier 2 prose.

BUNDLE — commits C1 to C5 and then the pull request, in this order.

C1 — `.agent/authored/f282-r13-block.md` := this block; `.agent/authored/f282-r13-<name>` for each
  payload. Byte for byte, with `shutil.copyfile`.
  Subject: `F282 R13 C1: copy round 13 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 216. Report the number you measure.

C2 — `git apply` ledger.diff → `.agent/live_review.md` · `.agent/plan.md` := plan.md.
  Subject: `F282 R13 C2: book round 12's PASS and move R-0499, R-0950 and R-1008 to F284`
  Expected by `git show --numstat` (insertions/deletions): 5/0 live_review.md, 7/9 plan.md.

C3 — THE ROTATION, its own commit, paths `.agent/live_review.md` and
  `.agent/live_review_archive.md` ONLY (operator amendment amend0905-throughput, AFTER the verdict
  booking and BEFORE the STATUS flip): `python3 scripts/rotate_live_review.py`. Report its printed
  output in full.
  Subject: `F282 R13 C3: rotate the finding ledger into its archive`

C4 — THE REGISTRATION, its own commit: `git apply` registration.diff, then `git add` the new file.
  Paths exactly `docs/roadmap/features/T2_F284.md`, `docs/roadmap/STATUS.md`,
  `tests/docs/test_docs_consistency.py` and `README.md`.
  Subject: `F282 R13 C4: register F284 — Findings paydown v3 under amend0911-feedback rule B: feature file, STATUS line, pin 284, README counters`
  Expected (insertions/deletions): 2/2 README.md, 7/0 STATUS.md, 44/0 T2_F284.md,
  5/1 test_docs_consistency.py.

C5 — THE CLOSURE COMMIT, exactly these paths and no others: `docs/roadmap/STATUS.md`, `README.md`
  and `.agent/handoff.md`. `git apply` closure.diff, then rewrite `.agent/handoff.md` per
  `docs/agents/handback_template.md` as the closure handback: it names the package, its SHA-256,
  its directory, the evidence job and the accepted head from round 12, and it does NOT name a
  pull request number, which does not exist when it is written. There is no `consumed_by` edit:
  the closure's self-use track answered NONE (DECISION F282 D10).
  Subject: `F282 R13 C5: accept F282 in STATUS with its README pins`
  Expected for the two applied files (insertions/deletions): 11/3 README.md, 1/1 STATUS.md.
  Then `git push origin feature/f282-findings-paydown-v2`.

THE PULL REQUEST — after C5 and its push, `gh pr create --base main --head
  feature/f282-findings-paydown-v2` with the title `F282 — Findings paydown v2`. The description is
  written for the operator in plain, complete sentences that explain every id and file name the
  first time it appears. It carries: what changed and why — 27 of the 30 review findings open at the
  claim were repaired or settled with evidence and none was added, one slice per module; the key
  decisions by id with one clause each (F282 D1 to D11, from `.agent/decisions.md`); what the
  closure found — the full suite's one red node, a one-second clash of archive names in a packaging
  test, repaired in one round, and a self-use track with no eligible item; how to review — the
  package `remedy-review-20260924-025907-READY_FOR_REVIEW.zip`, SHA-256
  `87eccda52d816efd0f352f40decbb30139a11fdb1eb9554d80a5c1489faa2c44`, in
  `/home/decodeux/Repos/remedy-history/zips`, evidence job `f282r12e1001`, accepted head
  `3d7afae1a51b89fc039d44801991ce6390347402`; a changed-files table for the branch against
  `b8fa02ba` (paths grouped by directory with counts are acceptable); the latest verdict, round 12's
  PASS plus this round's own, still ungated, work, and the closure's PASS_WITH_RISKS with the three
  carried findings named in plain words; the open-findings count, 3, all owned by F284; and the
  runtime actuals — 13 rounds across 2 sessions, rounds 1 to 7 in the first and 8 to 13 in the
  second, one closure repair round, token and cost figures NOT MEASURED. End the description with
  the line `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
  DO NOT MERGE IT. Report the number and URL in your final reply only.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f282-r13-*` copies C1 makes,
   `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/roadmap/features/T2_F284.md`, `docs/roadmap/STATUS.md`,
   `tests/docs/test_docs_consistency.py`, `README.md` and `.agent/handoff.md`. Report the set you
   measure with `git diff --name-only f6fd80de HEAD` after C5.
4. C5 is the LAST commit on this branch (Rule A4). Nothing follows it except, if the reviewer's
   closure gate asks for one, a commit whose path set is exactly `.agent/candidates.md` — which
   this block does not order and you never write on your own initiative.
5. If any gate goes red, STOP before C5: commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. A closure that cannot be proved is not closed.
6. NOTHING IS MERGED. No `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
7. Delete nothing you did not create: every `remedy/job-*` branch, every `.remedy-wt/job-*`
   worktree and the reviewer's `.remedy-wt/f282-r13-dry` and `.remedy-wt/f282-r13-sim` stay.
8. DO NOT run the full suite: this feature's run is committed at
   `.agent/authored/f282-closure-suite.txt`.

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written; G4 and G5
therefore read the working tree with C5's diff applied and staged, before the commit.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 committed `.agent/authored/f282-r13-*` blob, read with `git show <C1>:<path>`, compared byte for
 byte with its source (the block copy against `.remedy-wt/f282-r13-block.md`). One reading per
 file, all equal.

G2 THE BOOKING — at C2, read with `git show <C2>:<path>`: `.agent/live_review.md` 438936 bytes,
 sha256 `1958c253f6aae0af24cefa483113f5d7f6daa17ce5a9b55bdff8aa5974b4e05a`; `.agent/plan.md` 916
 bytes, sha256 `1ff066cfdfb3b2ac3afaffa2a0be06b56ed28b098ba23bfc73fd3826d3d9e86e`. Also: among the
 lines C2's diff ADDS, those beginning `Owner: F284 — ` (3) and `Gate: F282 R12 — ` (1); and the
 open set by distinct id via `open_finding_ids` from `scripts/rotate_live_review.py` at `f6fd80de`
 and at C2 — the reviewer read 3 and 3, both differences empty. Report yours beside each.

G3 THE ROTATION — at C3: the reviewer's dry run printed 8 gate records and 28 finding pairs (56
 records) moved, the ledger 438936 to 309259 bytes, the archive 4722407 to 4852084 bytes, open
 findings 3 before and 3 after, and left `.agent/live_review.md` at sha256
 `b1b6d0c41fa0349d3c804f42c5583eb9d427760a43ad0586f770f5611218d3d3` and
 `.agent/live_review_archive.md` at sha256
 `c6b3350b7254169f0282f1ba1ac1f536374180bdc7de5bbb3e26bdbe7a5c856a`. Report yours beside each, and
 C3's path set, which is the two ledger files and nothing else.

G4 THE REGISTRATION AND THE CLOSURE EDITS — at C4, read with `git show <C4>:<path>`, each equal to
 the reviewer's dry run:
 | path | bytes | sha256 |
 |---|---|---|
 | docs/roadmap/features/T2_F284.md | 2678 | 1ecce7fd204416d2da6727590742ac88f209bf9417c2cba3b524b510de5452e3 |
 | docs/roadmap/STATUS.md | 48246 | 127ad44a19739edb23f2694dddf5e737122dbb37afe31cbfcf30c1662ac73ed6 |
 | tests/docs/test_docs_consistency.py | 94944 | 2fa5c750c4994007f27dca9a90abc066131dc8baffeabdcf27118a8f44765f80 |
 | README.md | 24757 | b5b4504aa8f29c7fba763c3a945070c860584495a81c8696126b007ce08427ae |
 then `python3 -m pytest tests/docs/ -q` at C4, which the dry run read as `327 passed` at exit 0.
 Then, with closure.diff applied and staged before C5 is committed: `docs/roadmap/STATUS.md` at
 48679 bytes, sha256 `a19c228d4510817f75bad1545031503549161995fd32056e077874f051883f30`, and
 `README.md` at 25361 bytes, sha256
 `e8e5c18d0d3ab5a838d44818b0055bc1a988b0cfe724bf4ddf8869d3c4c5e09a`; and `python3 -m pytest
 tests/docs/ -q` again, `327 passed` at exit 0 in the dry run. Report yours beside each.

G5 THE TREE — with C5's diff in place: `python3 -m apps.cli.main integrity check --json`, `passed`
 true at `fail_count` 0; `python3 -m apps.cli.main integrity block .remedy-wt/f282-r13-block.md`,
 real exit code 0 with every item `[OK]`; and `python3 -m pytest
 tests/cli/test_golden_path.py -q`, the canary, real exit code 0.

G6 THE PUSH AND THE PULL REQUEST — after C5: `git log --oneline -n 6`; `git status --porcelain`
 empty; the push's real outcome; the pull request's number and URL; and `gh pr list --state open
 --json number,headRefName,baseRefName,isDraft` showing exactly that one pull request, from this
 branch into `main`, not a draft. These go in your final reply, not the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, and AGENTS.md's
item-status table with one row per C-item, the pull request and each gate: state block, the
per-commit changed-files table with the insertions git MEASURED beside the ones this block
expected, every gate's real output and exit code, the deviations, and the next action. Your
Session section reads SESSION 2 of feature F282, round 13, and says in one sentence how much
context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), then the Open PR
Gate — the pull request this round opens is merged by the NEXT feature's session, never by this
one — and then Rule A5, the first unchecked feature in `docs/roadmap/STATUS.md`. State the
open-findings count, 3, and the operator-questions count, 0.
