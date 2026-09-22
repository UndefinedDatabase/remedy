STEP F283 R24 — the closure: the rotation, the accepted STATUS line with its README pins, and the pull request

GOAL
Book round 23's PASS, rotate the finding ledger as its own commit, flip F283's STATUS line to
accepted with the README's three pinned places and the self-use entry's `consumed_by` in that same
commit, and open the pull request. The pull request is NEVER merged by the session that opens it.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. Every appliable byte of this round is a reviewer payload: the
ledger entry, the plan, the STATUS line and the three README pairs. You author only the pull
request's description and the handback.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f283-r24-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f283-r24-scratch/`   YOURS for logs and scripts, EXCEPT every file the reviewer put
      there before C1, which is read-only to you. `build_closure.py` is the reviewer's dry run of
      C4: it applied all four pairs in a disposable worktree at `120a3b77`, derived the two README
      numerals from the flipped ledger rather than by hand, and read `315 passed` at exit 0 from
      `tests/docs/`; with the STATUS flip alone and the README untouched the same suite read
      `3 failed, 312 passed` at exit 1, which is the control proving those three places bind.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, heredocs written with `cat >`, process substitution, `$?` or
`${...}` outside a `bash -c`, `cd <dir> && git ...`, shell `for` loops, brace expansion, `awk`, a
`grep` pattern holding `$`, and multi-operation one-liners chained with `;` or `&&` outside a
`bash -c`; put multi-step code in a scratch file. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`. The `remedy` CLI is denied session-wide: use
`python3 -m apps.cli.main ...` or the module a gate names. NEVER USE `git stash` IN ANY FORM, and
never check out another commit in the primary checkout.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` empty, `git branch --show-current` reads
   `feature/f283-machine-contracts-part-two`, `git log --oneline -1` reads `120a3b77`.
3. Verify this block's own bytes (R-0954): line count and sha256 of
   `.remedy-wt/f283-r24-block.md` against the two readings your delegation message states. Report
   both beside both, and stop if either differs.

PAYLOADS — under `.remedy-wt/f283-r24-payloads/`, printed by the reviewer's measurement
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 2 | 2451 | 6716c4cfb6df5c27540c79f9e662c4bd28aebb37b98679c722a5cb6fa2182fe4 |
| plan.md | 31 | 1294 | db95460d0184a6f61a818fc926697b6749dc989dbeb67e28efe75f5c239b352c |
| status_from.txt | 0 | 102 | d9c5446c1dbab78d0dec6eaf33911099882a9723f859b64da0dfdd4e10f68927 |
| status_to.txt | 0 | 459 | f61ccefed4a4729066b87282c780b0a2d9be04f4ab38bbc9a2b11a49b5c2a494 |
| readme_count_from.txt | 0 | 36 | 2a2ecc67482bd80ba59b9ab239da0a8462750eaad8b6fc218767d969ab74baaa |
| readme_count_to.txt | 0 | 36 | eb97e2238fecfc7b4abd0d9a35cbf69ce5b323915288f27506cbe34001301806 |
| readme_tier_from.txt | 0 | 44 | 328676d61807166a0d7a817f52fc9838b63fed3b7315e8535b0a47264023ab97 |
| readme_tier_to.txt | 0 | 44 | 108b2c75ad90a36e36fee3bb55b2996c44d266fea0e38cc9fb84e54de4a9f5f0 |
| readme_prose_from.txt | 0 | 72 | 257201b3df30f9959183a4b441c07aa601fc2a3dc2e3efcd7cff73f334a5e775 |
| readme_prose_to.txt | 5 | 432 | 7656e4b7ea3b7a44ffe71ad0f13a7d6f6044730366103d403853180ccfb49425 |

`ledger.md` is an APPEND beginning with the single newline that separates records: the round 23
`Gate:` entry. `plan.md` is a REWRITE. The four FROM/TO pairs are REWRITES — the reviewer ran the
containment test on each and every one printed `TO contains FROM: false` — so each FROM must read
exactly ONE occurrence in its target before the edit and ZERO after, and its TO exactly one after.
Never retype or edit a payload; none of these files carries a trailing newline you may add.

BUNDLE — commits C1 to C4 and then the pull request, in this order.

C1 — `.agent/authored/f283-r24-block.md` := this block; `.agent/authored/f283-r24-<name>` for each
  payload. Byte-for-byte, with `shutil.copyfile`.
  Subject: `F283 R24 C1: copy round 24 block and payloads into .agent/authored/`

C2 — `.agent/live_review.md` += ledger.md · `.agent/plan.md` := plan.md
  Subject: `F283 R24 C2: book round 23's PASS`

C3 — THE ROTATION, its own commit, paths `.agent/live_review.md` and
  `.agent/live_review_archive.md` ONLY (operator amendment amend0905-throughput, a step of the
  closure sequence, run AFTER the verdict booking and BEFORE the STATUS flip):
  `python3 scripts/rotate_live_review.py`. Report the old and new ledger sizes the script prints,
  and the open-findings count before and after, which must be IDENTICAL.
  Subject: `F283 R24 C3: rotate the finding ledger into its archive`

C4 — THE CLOSURE COMMIT, exactly these paths and no others: `docs/roadmap/STATUS.md`, `README.md`,
  `scripts/self_use_queue.json`, `.agent/plan.md` if it needs it, and `.agent/handoff.md`.
  (a) Apply `status` — the STATUS line's `[~]` becomes the accepted `[x]` line.
  (b) Apply `readme_count`, `readme_tier` and `readme_prose` — the accepted count with its `Next:`
      clause on the same line, the Tier 2 table's Done cell, and the Tier 2 prose entry. All three
      are pinned by `tests/docs/test_docs_consistency.py` and all three land HERE: README and
      STATUS may never disagree in any committed state (finding R-0154).
  (c) In `scripts/self_use_queue.json`, the entry whose id is `SU-026` — and only that entry —
      gets `"consumed_by": "F283"` where it now reads `"consumed_by": ""`. Change nothing else in
      that file: no reformatting, no reordering, no other entry. The reviewer measured that the
      string `"consumed_by": "",` occurs exactly ONCE in the file at `120a3b77`; report the count
      you measure before and after.
  (d) `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md` as the closure
      handback. It names the package, its SHA-256, its directory, the evidence job and the
      accepted head; it does NOT name a pull request number, which does not exist when it is
      written.
  Subject: `F283 R24 C4: accept F283 in STATUS with its README pins and the self-use entry`
  Then `git push origin feature/f283-machine-contracts-part-two`.

THE PULL REQUEST — after C4 and its push, `gh pr create` with base `main`. Title:
  `F283 — Machine contracts, part two: the refusal sweep, the JSON gap and the exit-code taxonomy`.
  The description carries: what changed and why, in plain sentences an operator can read; the key
  decisions by id with one clause each (F283 D1 to D13); how to review — the package name with its
  SHA-256 and directory, the evidence job id, and the accepted head; a changed-files table for the
  branch; the latest verdict, which is round 23's PASS plus this round's own, still ungated, work;
  the open-findings count, 26, and that none is this feature's own; and the runtime actuals the
  reviewer observed — 24 rounds across 5 sessions, this session's rounds 20 to 24, the feature's
  one full suite green at 18503 passed and 20 skipped, token and cost figures NOT MEASURED. End
  the description with the line
  `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
  DO NOT MERGE IT. Report the number and URL in your final reply only.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f283-r24-*` copies C1 makes,
   `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json` and `.agent/handoff.md`.
   Report the set you measure. Nothing under `packages/`, `apps/`, `tests/`, no other file under
   `docs/` or `scripts/`, and none of `.agent/candidates.md`, `.agent/context.md`,
   `.agent/decisions.md`, `.agent/operator_questions.md`, `.agent/prose_slips.md`.
4. C4 is the LAST commit on this branch (Rule A4). Nothing follows it except, if the reviewer's
   closure gate asks for one, a commit whose path set is exactly `.agent/candidates.md` — which
   this block does not order and you never write on your own initiative.
5. If any gate goes red, STOP before C4: commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. A closure that cannot be proved is not closed, and
   an honest stop here costs one round while a false `[x]` costs the record.
6. NOTHING IS MERGED. No `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
7. Delete nothing you did not create: the `remedy/job-*` branches and the worktree the self-use
   run left behind stay as they are.

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C4's handback text is written.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 committed `.agent/authored/f283-r24-*` blob, read with `git show <C1>:<path>`, compared
 byte-for-byte with its source (the block copy against `.remedy-wt/f283-r24-block.md`). One
 reading per file, all equal.

G2 THE BOOKING — at C2:
 (a) By strict byte CONCATENATION, `.agent/live_review.md` read at `120a3b77` (565994) plus
     ledger.md, the reviewer composed 568445.
 (b) Line-anchored on the committed ledger: `^Gate: F283 R23 — ` 1. Open set by distinct id via
     `open_finding_ids` from `scripts/rotate_live_review.py` at `120a3b77` and at C2: the reviewer
     measured 26 and 26, ADDED and REMOVED both empty.
 (c) `.agent/plan.md` at C2 is sha256-equal to plan.md; report its line count (< 50).

G3 THE ROTATION — at C3: the script's printed old and new ledger sizes; the open-findings count by
 distinct id before and after, IDENTICAL; the number of `Gate:` records and resolved pairs moved;
 and that `.agent/live_review_archive.md` grew by what the ledger lost, reported as both byte
 readings. C3's path set is the two ledger files and nothing else.

G4 THE CLOSURE EDITS — at C4: for each of the four pairs, the FROM's occurrence count in its
 target BEFORE (1) and AFTER (0), and the TO's count after (1); the `"consumed_by": "",` count in
 `scripts/self_use_queue.json` before (1) and after (0), with `"consumed_by": "F283"` at 1 and
 SU-026 the entry carrying it; and `python3 -m json.tool` accepting the file. Then
 `python3 -m pytest tests/docs/ -q`, which the reviewer's dry run read as `315 passed` at exit 0
 with all four pairs applied. Report the accepted count and the Tier 2 Done cell you measure from
 the flipped ledger, which must be 89 and 31.

G5 THE TREE — `python3 -c` calling `run_integrity_checks` from
 `packages.orchestration.integrity_gate` (an object with `.passed`, `.fail_count`, `.checks` —
 attributes, never a dict): `passed` true and `fail_count` 0, taken AFTER C4. Then `git status
 --porcelain`, empty, and `python3 -m pytest tests/cli/test_golden_path.py -q`, the canary every
 handback runs. DO NOT run the full suite: this feature's one run is already committed at
 `.agent/authored/f283-closure-suite.txt`.

G6 THE PUSH AND THE PULL REQUEST — `git log --oneline -n 8`; `git status --porcelain` empty; `git
 stash list`'s first line unchanged from its reading before C1; the push's real outcome; the pull
 request's number and URL; and `gh pr list --state open --json number,headRefName,baseRefName,
 isDraft` showing exactly that one pull request, from this branch into `main`, not a draft. These
 go in your final reply, not the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: state block, the per-commit changed-files
table with the insertions git MEASURED, every gate's real output and exit code, the item-status
table with one row per C-item and gate, the deviations, and the next action. Your Session section
reads SESSION 5 of feature F283, round 24, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), then the Open PR
Gate — the pull request this round opens is merged by the NEXT feature's session, never by this
one — and then Rule A5, the first unchecked feature in `docs/roadmap/STATUS.md`. State the
open-findings count, 26, and the operator-questions count, 0.
