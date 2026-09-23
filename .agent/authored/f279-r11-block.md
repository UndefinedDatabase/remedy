STEP F279 R11 — the closure: the rotation, the accepted STATUS line with its README pins, and the pull request

GOAL
Book round 10's PASS, rotate the finding ledger as its own commit, flip F279's STATUS line to
accepted with the README's three pinned places and the self-use entry's `consumed_by` in that same
commit, and open the pull request. The pull request is NEVER merged by the session that opens it.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. Every appliable byte of this round is a reviewer payload: the
ledger entry, the plan, the STATUS line and the three README pairs. You author only the pull
request's description and the handback.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f279-r11-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f279-r11-scratch/`   YOURS for logs and scripts, EXCEPT every file the reviewer put
      there before C1 (`review_r10.py`, `build_payloads.py`, `sim.py`, `numstat_c1.py`), which is
      read-only to you. `sim.py` is the reviewer's dry run of C2 to C4 in a disposable worktree at
      `081b9b6c`: with all four pairs and the queue edit applied, `tests/docs/` read `322 passed` at
      exit 0; with the STATUS flip alone and the README untouched, the same suite read `3 failed,
      319 passed` at exit 1, the control proving those three places bind.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, heredocs written with `cat >`, process substitution, `$?` or
`${...}` outside a `bash -c`, `cd <dir> && git ...`, shell `for` loops, brace expansion, `awk`,
`xxd`, `bc`, a `grep` pattern holding `$`, and multi-operation one-liners chained with `;`, `&&`
or `|` outside a `bash -c`; put multi-step code in a scratch Python file, and never put a `#`
after a newline inside a `python3 -c` argument. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`. The `remedy` CLI is denied: use `python3 -m apps.cli.main
...`. For the pull request body, write it to a scratch file and pass `--body-file`. NEVER USE
`git stash` IN ANY FORM, and never check out another commit in the primary checkout.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` empty, `git branch --show-current` reads
   `feature/f279-configuration-toolchain-truth`, `git log --oneline -1` reads `081b9b6c`.
3. Verify this block's own bytes (R-0954): line count and sha256 of
   `.remedy-wt/f279-r11-block.md` against the two readings your delegation message states. Report
   both beside both, and stop if either differs.
4. Record the first line of `git stash list`.

PAYLOADS — under `.remedy-wt/f279-r11-payloads/`, printed by the reviewer's simulation
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 2 | 1968 | e34012ff9fc8b946aead9381cedb5e98026d592f5fd7ec86f5a933ebb7f2d365 |
| plan.md | 27 | 1038 | 695238ee1a62b81da01a821675f460245af3c695f8e8d8f9ff998ed85441bdfa |
| readme_count_from.txt | 0 | 36 | 02205025b2739a377b34f50948095a51de409d93bd36935b9db7aea45bdfa579 |
| readme_count_to.txt | 0 | 36 | 3fd68988e8ab6d75b729233f90595ba2899aaa2ab64d7af7a8e1473860163c14 |
| readme_prose_from.txt | 0 | 15 | b1b58e6d9cbb506197ae26b7e71e7d3034af0f6794f84e35139ccd25601932ac |
| readme_prose_to.txt | 8 | 647 | 047581aed83cc81843a48dd11e8af9a30a5cb01c106855cee5b023b298604f4e |
| readme_tier_from.txt | 0 | 44 | 654915a8657fe94b203354b6994b68a6dadb005a21de49c872e1e1b124520517 |
| readme_tier_to.txt | 0 | 44 | 22d4243158f48ba63d636fbde3a5ce508c80092a31b5b7b4791d7074a4289780 |
| status_from.txt | 0 | 93 | 675de2bb964ec7ef2a2895e1afd84141ba69b7a810e89bf75f3e4f2f6d8bc425 |
| status_to.txt | 0 | 514 | 78b1d003b2cde4d6d5b7303f711619e10a35afd77e4f4369bddafab9f51dbd0b |

`ledger.md` is an APPEND beginning with the single newline that separates records: round 10's
`Gate:` entry. `plan.md` is a REWRITE. The four FROM/TO pairs are REWRITES — the reviewer's
containment test printed `TO contains FROM: False` for each — so each FROM must read exactly ONE
occurrence in its target before the edit and ZERO after, and its TO exactly one after. None of the
pair files carries a trailing newline, and you add none. Never retype or edit a payload.

BUNDLE — commits C1 to C4 and then the pull request, in this order.

C1 — `.agent/authored/f279-r11-block.md` := this block; `.agent/authored/f279-r11-<name>` for each
  payload. Byte for byte, with `shutil.copyfile`.
  Subject: `F279 R11 C1: copy round 11 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 45, git counting each unterminated pair file as
  one line. Report the number you measure.

C2 — `.agent/live_review.md` += ledger.md · `.agent/plan.md` := plan.md. The append is strict byte
  concatenation onto the file as it stands at `081b9b6c`.
  Subject: `F279 R11 C2: book round 10's PASS`
  Expected insertions by `git show --numstat`: 2 live_review.md, 8 plan.md.

C3 — THE ROTATION, its own commit, paths `.agent/live_review.md` and
  `.agent/live_review_archive.md` ONLY (operator amendment amend0905-throughput, run AFTER the
  verdict booking and BEFORE the STATUS flip): `python3 scripts/rotate_live_review.py`. Report the
  script's printed output in full.
  Subject: `F279 R11 C3: rotate the finding ledger into its archive`

C4 — THE CLOSURE COMMIT, exactly these paths and no others: `docs/roadmap/STATUS.md`, `README.md`,
  `scripts/self_use_queue.json` and `.agent/handoff.md`.
  (a) Apply `status` to `docs/roadmap/STATUS.md` — the `[~]` line becomes the accepted `[x]` line.
  (b) Apply `readme_count`, `readme_tier` and `readme_prose` to `README.md` — the accepted count
      (its `Next:` clause stays on the same line), the Tier 2 table's Done cell, and the Tier 2
      prose entry. All three are pinned by `tests/docs/test_docs_consistency.py` and all three
      land HERE: README and STATUS may never disagree in any committed state (finding R-0154).
  (c) In `scripts/self_use_queue.json`, the entry whose id is `SU-028` — and only that entry —
      gets `"consumed_by": "F279",` where it now reads `"consumed_by": "",`. Change nothing else
      in that file: no reformatting, no reordering, no other entry; edit the text, never
      re-serialise the JSON. The reviewer measured that `"consumed_by": "",` occurs exactly ONCE
      in the file at `081b9b6c`, inside SU-028; report the count you measure before and after.
  (d) `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md` as the closure
      handback. It names the package, its SHA-256, its directory, the evidence job and the
      accepted head from round 10; it does NOT name a pull request number, which does not exist
      when it is written.
  Subject: `F279 R11 C4: accept F279 in STATUS with its README pins and the self-use entry`
  Then `git push origin feature/f279-configuration-toolchain-truth`.

THE PULL REQUEST — after C4 and its push, `gh pr create --base main --head
  feature/f279-configuration-toolchain-truth` with the title `F279 — Configuration & toolchain
  truth`. The description is written for the operator in plain, complete sentences that explain
  every id and file name the first time it appears. It carries: what changed and why; the key
  decisions by id with one clause each (F279 D1 to D7, from `.agent/decisions.md`); what the
  closure found — the two guard tests repaired at round 9, and R-1040 and R-1041 registered and
  carried to F282, each in one sentence; how to review — the package
  `remedy-review-20260923-091251-READY_FOR_REVIEW.zip`, SHA-256
  `c59772f93dab75c9a8aa9da3624fa48f45fcc9afe0a372958ce74c2663640224`, in
  `/home/decodeux/Repos/remedy-history/zips`, evidence job `f279r10e1001`, accepted head
  `9ee2659888d3c30969d102616503cc2898e26e2c`; a changed-files table for the branch against
  `c9bc5c20` (paths grouped by directory with counts are acceptable); the latest verdict, round
  10's PASS plus this round's own, still ungated, work, and the closure's PASS_WITH_RISKS with its
  two risks — two suite nodes that fail only under parallel runs, recorded against R-0950 and
  R-1028, and the two findings above; the open-findings count, 28, none of them owned by F279; and
  the runtime actuals — 11 rounds across 2 sessions, rounds 1 to 7 in the first and 8 to 11 in the
  second, one closure repair round, token and cost figures NOT MEASURED. End the description with
  the line `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
  DO NOT MERGE IT. Report the number and URL in your final reply only.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f279-r11-*` copies C1 makes,
   `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json` and `.agent/handoff.md`.
   Report the set you measure with `git diff --name-only 081b9b6c` after C4.
4. C4 is the LAST commit on this branch (Rule A4). Nothing follows it except, if the reviewer's
   closure gate asks for one, a commit whose path set is exactly `.agent/candidates.md` — which
   this block does not order and you never write on your own initiative.
5. If any gate goes red, STOP before C4: commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. A closure that cannot be proved is not closed.
6. NOTHING IS MERGED. No `gh pr merge`, no checkout of `main`, no branch deletion, no force-push.
7. Delete nothing you did not create: every `remedy/job-*` branch and every `.remedy-wt/job-*`
   worktree stays as it is.

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C4's handback text is written;
G4 and G5 therefore read the working tree with C4's edits applied and staged, before the commit.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 committed `.agent/authored/f279-r11-*` blob, read with `git show <C1>:<path>`, compared byte for
 byte with its source (the block copy against `.remedy-wt/f279-r11-block.md`). One reading per
 file, all equal.

G2 THE BOOKING — at C2: by strict byte CONCATENATION onto the `081b9b6c` bytes, the reviewer's
 dry run composed `.agent/live_review.md` at 402643 bytes, sha256
 `aed8b129c596220e1bcb9d9a08450e3a376627e7e79881af202fa8714c8f2c85`; `^Gate: F279 R10 — `
 occurs once; the open set via `open_finding_ids` reads 28 at `081b9b6c` and 28 at C2; and
 `.agent/plan.md` is sha256-equal to plan.md. Report yours beside each.

G3 THE ROTATION — at C3: the reviewer's dry run printed 11 gate records and 0 finding pairs
 moved, the ledger 402643 to 371291 bytes, the archive 4667384 to 4698736 bytes, open findings
 28 before and 28 after, and left the ledger at sha256
 `a460e3257851cb94ddded87060394274614d0d157b81a5b19ff234ba69e6e0bf` and the archive at sha256
 `3ec2362454a4a6b819892703aca67169b1b43031199ce694ad32820267ed49d9`. Report yours beside
 each, and C3's path set, which is the two ledger files and nothing else.

G4 THE CLOSURE EDITS — before C4 is committed: for each of the four pairs, the FROM's count in its
 target before (1) and after (0) and the TO's count after (1); the `"consumed_by": "",` count in
 `scripts/self_use_queue.json` before (1) and after (0), `"consumed_by": "F279",` at 1 and SU-028
 the entry carrying it, and `python3 -m json.tool` accepting the file; `git diff --numstat` of the
 queue file reading 1 and 1. The reviewer's dry run left `docs/roadmap/STATUS.md` at sha256
 `2c26c3dc9d79c4315ef1e2ce1609bd5a938dc6a861098bd83eea8cec36798523`, `README.md` at
 `3332b211e47a672c6f95ddf74fbae418e2e615adf47f16da0fa6056e60c069d6` and the queue at
 `e9b690f7a2a456f6672b4eb4616f422cc726608471a16dabaa4b150a26e6dc25`; report yours beside
 each. Then `python3 -m pytest tests/docs/ -q`, which the dry run read as `322 passed` at exit 0.

G5 THE TREE — `python3 -m apps.cli.main integrity check --json` with C4's edits in place: `passed`
 true, `fail_count` 0. Then `python3 -m pytest tests/cli/test_golden_path.py -q`, the canary. DO
 NOT run the full suite: this feature's run is committed at
 `.agent/authored/f279-closure-suite.txt`.

G6 THE PUSH AND THE PULL REQUEST — after C4: `git log --oneline -n 6`; `git status --porcelain`
 empty; `git stash list`'s first line unchanged from its reading before C1; the push's real
 outcome; the pull request's number and URL; and `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft` showing exactly that one pull request, from this branch
 into `main`, not a draft. These go in your final reply, not the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, and AGENTS.md's
item-status table with one row per C-item, the pull request and each gate: state block, the
per-commit changed-files table with the insertions git MEASURED, every gate's real output and exit
code, the deviations, and the next action. Your Session section reads SESSION 2 of feature F279,
round 11, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), then the Open PR
Gate — the pull request this round opens is merged by the NEXT feature's session, never by this
one — and then Rule A5, the first unchecked feature in `docs/roadmap/STATUS.md`. State the
open-findings count, 28, and the operator-questions count, 0.
