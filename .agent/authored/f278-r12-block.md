STEP F278 R12 — the closure: the rotation, the accepted STATUS line with its README pins, and the pull request

GOAL
Book round 11's PASS, rotate the finding ledger as its own commit, flip F278's STATUS line to
accepted with the README's three pinned places and the self-use entry's `consumed_by` in that same
commit, and open the pull request. The pull request is NEVER merged by the session that opens it.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. Every appliable byte of this round is a reviewer payload: the
ledger entry, the plan, the STATUS line and the three README pairs. You author only the pull
request's description and the handback.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f278-r12-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f278-r12-scratch/`   YOURS for logs and scripts, EXCEPT `build_closure.py`, which
      the reviewer put there before C1 and is read-only to you. It is the reviewer's dry run of C2
      to C4 in a disposable worktree at `5558aa1d`: with all four pairs and the queue edit applied,
      `tests/docs/` read `315 passed` at exit 0; with the STATUS flip alone and the README
      untouched the same suite read `3 failed, 312 passed` at exit 1, the control proving those
      three places bind.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, heredocs written with `cat >`, process substitution, `$?` or
`${...}` outside a `bash -c`, `cd <dir> && git ...`, shell `for` loops, brace expansion, `awk`,
`xxd`, `bc`, a `grep` pattern holding `$`, and multi-operation one-liners chained with `;`, `&&`
or `|` outside a `bash -c`; put multi-step code in a scratch Python file, and never put a `#`
after a newline inside a `python3 -c` argument. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`. The `remedy` CLI is denied session-wide: use
`python3 -m apps.cli.main ...` or the module a gate names. For the pull request body, write it to
a scratch file and pass `--body-file`. NEVER USE `git stash` IN ANY FORM, and never check out
another commit in the primary checkout.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` empty, `git branch --show-current` reads
   `feature/f278-durable-writes-loud-failures`, `git log --oneline -1` reads `5558aa1d`.
3. Verify this block's own bytes (R-0954): line count and sha256 of `.remedy-wt/f278-r12-block.md`
   against the two readings your delegation message states. Report both beside both, and stop if
   either differs.
4. Record the first line of `git stash list`.

PAYLOADS — under `.remedy-wt/f278-r12-payloads/`, printed by the reviewer's measurement
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 2 | 2371 | 9599aba3f85c683e4d7ebd5ee54c534b26e6ec25ad8acfd9720ee67739710ab8 |
| plan.md | 28 | 1030 | 3fcd1b8ca04ff18ceaba9681e2a34097e3e76db3f2346a7c8019f9919c26eaad |
| readme_count_from.txt | 0 | 36 | eb97e2238fecfc7b4abd0d9a35cbf69ce5b323915288f27506cbe34001301806 |
| readme_count_to.txt | 0 | 36 | 02205025b2739a377b34f50948095a51de409d93bd36935b9db7aea45bdfa579 |
| readme_prose_from.txt | 0 | 27 | ffcd85056bd4e13d8d0c64883d6769d0d80821e56ec9417504245c24e4640299 |
| readme_prose_to.txt | 7 | 587 | f1280dcc322f7ffb0bd7238221113ab5506e10b97336b4faaec1e5f70736f859 |
| readme_tier_from.txt | 0 | 44 | 108b2c75ad90a36e36fee3bb55b2996c44d266fea0e38cc9fb84e54de4a9f5f0 |
| readme_tier_to.txt | 0 | 44 | 654915a8657fe94b203354b6994b68a6dadb005a21de49c872e1e1b124520517 |
| status_from.txt | 0 | 45 | f844a4503c6a065ceb23cf8f181a5407588f0a4b5fa5b5519bfac8e22264715a |
| status_to.txt | 0 | 402 | 579d40f8334d85f139af279f3cd0f8360af08fa307246c8091d198a21b0d923d |

`ledger.md` is an APPEND beginning with the single newline that separates records: round 11's
`Gate:` entry. `plan.md` is a REWRITE. The four FROM/TO pairs are REWRITES — the reviewer's
containment test printed `TO contains FROM: False` for each — so each FROM must read exactly ONE
occurrence in its target before the edit and ZERO after, and its TO exactly one after. None of the
pair files carries a trailing newline, and you add none. Never retype or edit a payload.

BUNDLE — commits C1 to C4 and then the pull request, in this order.

C1 — `.agent/authored/f278-r12-block.md` := this block; `.agent/authored/f278-r12-<name>` for each
  payload. Byte for byte, with `shutil.copyfile`.
  Subject: `F278 R12 C1: copy round 12 block and payloads into .agent/authored/`

C2 — `.agent/live_review.md` += ledger.md · `.agent/plan.md` := plan.md. The append is strict byte
  concatenation onto the file as it stands at `5558aa1d`.
  Subject: `F278 R12 C2: book round 11's PASS`

C3 — THE ROTATION, its own commit, paths `.agent/live_review.md` and
  `.agent/live_review_archive.md` ONLY (operator amendment amend0905-throughput, run AFTER the
  verdict booking and BEFORE the STATUS flip): `python3 scripts/rotate_live_review.py`. Report the
  script's printed output in full.
  Subject: `F278 R12 C3: rotate the finding ledger into its archive`

C4 — THE CLOSURE COMMIT, exactly these paths and no others: `docs/roadmap/STATUS.md`, `README.md`,
  `scripts/self_use_queue.json` and `.agent/handoff.md`.
  (a) Apply `status` to `docs/roadmap/STATUS.md` — the `[~]` line becomes the accepted `[x]` line.
  (b) Apply `readme_count`, `readme_tier` and `readme_prose` to `README.md` — the accepted count
      (its `Next:` clause stays on the same line), the Tier 2 table's Done cell, and the Tier 2
      prose entry. All three are pinned by `tests/docs/test_docs_consistency.py` and all three
      land HERE: README and STATUS may never disagree in any committed state (finding R-0154).
  (c) In `scripts/self_use_queue.json`, the entry whose id is `SU-027` — and only that entry —
      gets `"consumed_by": "F278",` where it now reads `"consumed_by": "",`. Change nothing else
      in that file: no reformatting, no reordering, no other entry; edit the text, never
      re-serialise the JSON. The reviewer measured that `"consumed_by": "",` occurs exactly ONCE
      in the file at `5558aa1d`, inside SU-027; report the count you measure before and after.
  (d) `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md` as the closure
      handback. It names the package, its SHA-256, its directory, the evidence job and the
      accepted head from round 11; it does NOT name a pull request number, which does not exist
      when it is written.
  Subject: `F278 R12 C4: accept F278 in STATUS with its README pins and the self-use entry`
  Then `git push origin feature/f278-durable-writes-loud-failures`.

THE PULL REQUEST — after C4 and its push, `gh pr create --base main --head
  feature/f278-durable-writes-loud-failures` with the title `F278 — Durable writes & loud
  failures`. The description carries, in plain sentences an operator can read: what changed and
  why; the key decisions by id with one clause each (F278 D1 to D7, from `.agent/decisions.md`);
  the four findings found and repaired inside the feature (R-1036, R-1037, R-1038, R-1039), each
  in one sentence; how to review — the package `remedy-review-20260923-030723-READY_FOR_REVIEW.zip`,
  SHA-256 `6dd87e83b40530115ebc046825f71dddaf99cb85a25c0f529278d14196d6c65c`, in
  `/home/decodeux/Repos/remedy-history/zips`, evidence job `f278r11e1001`, accepted head
  `77773f76ac1a640e4345574a2918468743e94730`; a changed-files table for the branch against
  `9817a927` (paths grouped by directory with counts are acceptable); the latest verdict, round
  11's PASS plus this round's own, still ungated, work; the open-findings count, 26, none of them
  this feature's own; and the runtime actuals — 12 rounds across 2 sessions, rounds 1 to 8 in the
  first and 9 to 12 in the second, one closure repair round, the full suite green at 18546 passed
  and 20 skipped, token and cost figures NOT MEASURED. End the description with the line
  `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
  DO NOT MERGE IT. Report the number and URL in your final reply only.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f278-r12-*` copies C1 makes,
   `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json` and `.agent/handoff.md`.
   Report the set you measure.
4. C4 is the LAST commit on this branch (Rule A4). Nothing follows it except, if the reviewer's
   closure gate asks for one, a commit whose path set is exactly `.agent/candidates.md` — which
   this block does not order and you never write on your own initiative.
5. If any gate goes red, STOP before C4: commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. A closure that cannot be proved is not closed.
6. NOTHING IS MERGED. No `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
7. Delete nothing you did not create: the `remedy/job-*` branches and the worktrees the self-use
   runs left behind stay as they are.

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C4's handback text is written;
G4 and G5 therefore read the working tree with C4's edits applied and staged, before the commit.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 committed `.agent/authored/f278-r12-*` blob, read with `git show <C1>:<path>`, compared byte for
 byte with its source (the block copy against `.remedy-wt/f278-r12-block.md`). One reading per
 file, all equal.

G2 THE BOOKING — at C2: by strict byte CONCATENATION onto the `5558aa1d` bytes, the reviewer's dry
 run composed `.agent/live_review.md` at 465513 bytes, sha256
 `50617da22f505ad916549ad1f31683bca1ee661f02df7e299d97dd0565c4a757`; `^Gate: F278 R11 — `
 occurs once; the open set via `open_finding_ids` reads 26 at `5558aa1d` and 26 at C2; and
 `.agent/plan.md` is sha256-equal to plan.md. Report yours beside each.

G3 THE ROTATION — at C3: the reviewer's dry run printed 24 gate records and 4 finding pairs
 moved, the ledger 465513 to 374026 bytes, the archive 4575897 to 4667384 bytes, open findings
 26 before and 26 after, and left the ledger at sha256
 `5ef819652c64cb796ffaea674aedd53881970c34d4cde272e083016a3cde5ac6` and the archive at sha256
 `0b4060395f3142622e074d31d894db6abd79ef4a26eb0b77baddc3177598e624`. Report yours beside
 each, and C3's path set, which is the two ledger files and nothing else.

G4 THE CLOSURE EDITS — before C4 is committed: for each of the four pairs, the FROM's count in its
 target before (1) and after (0) and the TO's count after (1); the `"consumed_by": "",` count in
 `scripts/self_use_queue.json` before (1) and after (0), `"consumed_by": "F278",` at 1 and SU-027
 the entry carrying it, and `python3 -m json.tool` accepting the file; `git diff --numstat` of the
 queue file reading 1 and 1. The reviewer's dry run left `docs/roadmap/STATUS.md` at sha256
 `3cfef11ce652f02f82ffbc6be93ac2beebe4bccfeb708efc84ca8adb27419f60`, `README.md` at
 `f787c108fd9710747058b98b82387f7b3140804834c30a89a0918ab710281892` and the queue at
 `7f4636092fee3f03510cebd13701ee4e76beb8704427fe10816407df3cc622b8`; report yours beside
 each. Then `python3 -m pytest tests/docs/ -q`, which the dry run read as `315 passed` at exit 0.

G5 THE TREE — `python3 -m apps.cli.main integrity check --json` with C4's edits in place: `passed`
 true, `fail_count` 0. Then `python3 -m pytest tests/cli/test_golden_path.py -q`, the canary. DO
 NOT run the full suite: this feature's one run is committed at
 `.agent/authored/f278-closure-suite.txt`.

G6 THE PUSH AND THE PULL REQUEST — after C4: `git log --oneline -n 6`; `git status --porcelain`
 empty; `git stash list`'s first line unchanged from its reading before C1; the push's real
 outcome; the pull request's number and URL; and `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft` showing exactly that one pull request, from this branch
 into `main`, not a draft. These go in your final reply, not the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, and AGENTS.md's
item-status table with one row per C-item, the pull request and each gate: state block, the
per-commit changed-files table with the insertions git MEASURED, every gate's real output and exit
code, the deviations, and the next action. Your Session section reads SESSION 2 of feature F278,
round 12, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), then the Open PR
Gate — the pull request this round opens is merged by the NEXT feature's session, never by this
one — and then Rule A5, the first unchecked feature in `docs/roadmap/STATUS.md`. State the
open-findings count, 26, and the operator-questions count, 0.
