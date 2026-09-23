STEP F263 R9 — the closure: the rotation, the accepted STATUS line with its README pins, and the pull request

GOAL
Book round 8's PASS, rotate the finding ledger as its own commit, flip F263's STATUS line to
accepted with the README's three pinned places and the self-use entry's `consumed_by` in that same
commit, and open the pull request. The pull request is NEVER merged by the session that opens it.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. Every appliable byte of this round is a reviewer payload: the
ledger entry, the plan, the STATUS line and the three README pairs. You author only the pull
request's description and the handback.

THREE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f263-r9-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f263-r9-scratch/`   READ-ONLY. `sim.py` is the reviewer's dry run of C2 to C4 in a
      disposable worktree at `872b4c23`: with all four pairs and the queue edit applied,
      `tests/docs/` read `322 passed` at exit 0; with the STATUS flip alone and the README
      untouched, the same suite read `3 failed, 319 passed` at exit 1, the control proving those
      three places bind.
  `.remedy-wt/f263-r9-worker/`    YOURS for logs, scripts and the pull request body.

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
   `feature/f263-human-change-absorption`, `git log --oneline -1` reads `872b4c23`.
3. Verify this block's own bytes (R-0954): line count and sha256 of
   `.remedy-wt/f263-r9-block.md` against the two readings your delegation message states. Report
   both beside both, and stop if either differs.
4. Record the first line of `git stash list`.

PAYLOADS — under `.remedy-wt/f263-r9-payloads/`, printed by the reviewer's simulation
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 2 | 1966 | fba74e747bcff87053df55b8b56da08653f197072dd93d2cb858a8703cde876f |
| plan.md | 28 | 1062 | ba8be2915fb25b60b3e57dfb08754e009b612e682761ffc3381f114065cded42 |
| readme_count_from.txt | 0 | 36 | 3fd68988e8ab6d75b729233f90595ba2899aaa2ab64d7af7a8e1473860163c14 |
| readme_count_to.txt | 0 | 36 | 6fde87bfc99720c679958134d3a8b182b685e9c6e973acd295571e7ecc8b2dd1 |
| readme_prose_from.txt | 0 | 29 | 6166c454079bb07a73f89ce0393658c440b5307c10d1ac92167672035c495b3b |
| readme_prose_to.txt | 7 | 560 | e9c38e4607c33d7ca929a548239ccca1d85556c76c94bf5beb89f4bfa4a70d6b |
| readme_tier_from.txt | 0 | 44 | 22d4243158f48ba63d636fbde3a5ce508c80092a31b5b7b4791d7074a4289780 |
| readme_tier_to.txt | 0 | 44 | a598619e1b1135cbc48c66f6016f4a549ed77dbe7e4ef1defd2505a465e705e3 |
| status_from.txt | 0 | 47 | 35ed25a3ba6b45d79b2e0ca15155358d04371643bc0eb78604de382beb2e3578 |
| status_to.txt | 0 | 549 | 13933c17a01f45bcb4ff6647f8c7bbda9baf9da85b044a262eb29926f57a2a1b |

`ledger.md` is an APPEND beginning with the single newline that separates records: round 8's
`Gate:` entry. `plan.md` is a REWRITE. The four FROM/TO pairs are REWRITES — the reviewer's
containment test printed `TO contains FROM: False` for each — so each FROM must read exactly ONE
occurrence in its target before the edit and ZERO after, and its TO exactly one after. None of the
pair files carries a trailing newline, and you add none. Never retype or edit a payload.

BUNDLE — commits C1 to C4 and then the pull request, in this order.

C1 — `.agent/authored/f263-r9-block.md` := this block; `.agent/authored/f263-r9-<name>` for each
  payload. Byte for byte, with `shutil.copyfile`.
  Subject: `F263 R9 C1: copy round 9 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 45, git counting each unterminated pair file as
  one line. Report the number you measure.

C2 — `.agent/live_review.md` += ledger.md · `.agent/plan.md` := plan.md. The append is strict byte
  concatenation onto the file as it stands at `872b4c23`.
  Subject: `F263 R9 C2: book round 8's PASS`
  Expected insertions by `git show --numstat`: 2 live_review.md, 8 plan.md.

C3 — THE ROTATION, its own commit, paths `.agent/live_review.md` and
  `.agent/live_review_archive.md` ONLY (operator amendment amend0905-throughput, run AFTER the
  verdict booking and BEFORE the STATUS flip): `python3 scripts/rotate_live_review.py`. Report the
  script's printed output in full.
  Subject: `F263 R9 C3: rotate the finding ledger into its archive`

C4 — THE CLOSURE COMMIT, exactly these paths and no others: `docs/roadmap/STATUS.md`, `README.md`,
  `scripts/self_use_queue.json` and `.agent/handoff.md`.
  (a) Apply `status` to `docs/roadmap/STATUS.md` — the `[~]` line becomes the accepted `[x]` line.
  (b) Apply `readme_count`, `readme_tier` and `readme_prose` to `README.md` — the accepted count
      (its `Next:` clause stays on the same line), the Tier 2 table's Done cell, and the Tier 2
      prose entry. All three are pinned by `tests/docs/test_docs_consistency.py` and all three
      land HERE: README and STATUS may never disagree in any committed state (finding R-0154).
  (c) In `scripts/self_use_queue.json`, the entry whose id is `SU-029` — and only that entry —
      gets `"consumed_by": "F263",` where it now reads `"consumed_by": "",`. Change nothing else
      in that file: no reformatting, no reordering, no other entry; edit the text, never
      re-serialise the JSON. The reviewer measured that `"consumed_by": "",` occurs exactly ONCE
      in the file at `872b4c23`, inside SU-029; report the count you measure before and after.
  (d) `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md` as the closure
      handback. It names the package, its SHA-256, its directory, the evidence job and the
      accepted head from round 8; it does NOT name a pull request number, which does not exist
      when it is written.
  Subject: `F263 R9 C4: accept F263 in STATUS with its README pins and the self-use entry`
  Then `git push origin feature/f263-human-change-absorption`.

THE PULL REQUEST — after C4 and its push, `gh pr create --base main --head
  feature/f263-human-change-absorption` with the title `F263 — Human-change absorption (absorb)`.
  The description is written for the operator in plain, complete sentences that explain every id
  and file name the first time it appears. It carries: what changed and why; the key decisions by
  id with one clause each (F263 D1 to D6, from `.agent/decisions.md`); what the closure found —
  the one suite node that fails only under parallel runs, recorded against R-0950, and the
  self-use run's provider timeout, recorded against R-1035, each in one sentence, and the measured
  cost of the human-change check from the self-use job (9 checks, 1.974307 seconds in total,
  0.232568 seconds at the slowest); how to review — the package
  `remedy-review-20260923-143535-READY_FOR_REVIEW.zip`, SHA-256
  `b25a25aeb9eae8ef717b4793555b3862463bc80f3060f6b1e38f6af9756c735b`, in
  `/home/decodeux/Repos/remedy-history/zips`, evidence job `f263r8e1001`, accepted head
  `5c98b36411337d932733b441203a7b10f1fa2336`; a changed-files table for the branch against
  `54a23101` (paths grouped by directory with counts are acceptable); the latest verdict, round
  8's PASS plus this round's own, still ungated, work, and the closure's PASS_WITH_RISKS with its
  two risks named above; the open-findings count, 28, none of them owned by F263; and the runtime
  actuals — 9 rounds across 2 sessions, rounds 1 to 6 in the first and 7 to 9 in the second, no
  closure repair round, token and cost figures NOT MEASURED. End the description with the line
  `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
  DO NOT MERGE IT. Report the number and URL in your final reply only.

CONSTRAINTS
1. Never edit or retype a payload.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f263-r9-*` copies C1 makes,
   `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json` and `.agent/handoff.md`.
   Report the set you measure with `git diff --name-only 872b4c23` after C4.
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
 committed `.agent/authored/f263-r9-*` blob, read with `git show <C1>:<path>`, compared byte for
 byte with its source (the block copy against `.remedy-wt/f263-r9-block.md`). One reading per
 file, all equal.

G2 THE BOOKING — at C2: by strict byte CONCATENATION onto the `872b4c23` bytes, the reviewer's
 dry run composed `.agent/live_review.md` at 392900 bytes, sha256
 `a7a3561fadca848384bde732c5450cab7fe36644d6de8ece344df7ee745ebf94`; `^Gate: F263 R8 — `
 occurs once; the open set via `open_finding_ids` reads 28 at `872b4c23` and 28 at C2; and
 `.agent/plan.md` is sha256-equal to plan.md. Report yours beside each.

G3 THE ROTATION — at C3: the reviewer's dry run printed 10 gate records and 1 finding pair
 moved, the ledger 392900 to 369229 bytes, the archive 4698736 to 4722407 bytes, open findings
 28 before and 28 after, and left the ledger at sha256
 `3131bcb96ac0466c833dbe229985066adf7e2bae7fbf4a0e196203c36eb6a738` and the archive at sha256
 `7ba7790ace766204238663f66bb40c426aa605724217f1aa00651716f1c6a4cd`. Report yours beside
 each, and C3's path set, which is the two ledger files and nothing else.

G4 THE CLOSURE EDITS — before C4 is committed: for each of the four pairs, the FROM's count in its
 target before (1) and after (0) and the TO's count after (1); the `"consumed_by": "",` count in
 `scripts/self_use_queue.json` before (1) and after (0), `"consumed_by": "F263",` at 1 and SU-029
 the entry carrying it, and `python3 -m json.tool` accepting the file; `git diff --numstat` of the
 queue file reading 1 and 1. The reviewer's dry run left `docs/roadmap/STATUS.md` at sha256
 `1314c52b8b353460428f4a697b7b2b7c1fba155d9df75291f02b4e255b379f1c`, `README.md` at
 `b6fc863535c2423be911ca4479ff45160309541685185362aec44aedeec625eb` and the queue at
 `126a2923c5b9838b44563467cd03655d2d1a27dc133875feec44c3d9f82431d8`; report yours beside
 each. Then `python3 -m pytest tests/docs/ -q`, which the dry run read as `322 passed` at exit 0.

G5 THE TREE — `python3 -m apps.cli.main integrity check --json` with C4's edits in place: `passed`
 true, `fail_count` 0. Then `python3 -m pytest tests/cli/test_golden_path.py -q`, the canary. DO
 NOT run the full suite: this feature's run is committed at
 `.agent/authored/f263-closure-suite.txt`.

G6 THE PUSH AND THE PULL REQUEST — after C4: `git log --oneline -n 6`; `git status --porcelain`
 empty; `git stash list`'s first line unchanged from its reading before C1; the push's real
 outcome; the pull request's number and URL; and `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft` showing exactly that one pull request, from this branch
 into `main`, not a draft. These go in your final reply, not the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, and AGENTS.md's
item-status table with one row per C-item, the pull request and each gate: state block, the
per-commit changed-files table with the insertions git MEASURED, every gate's real output and exit
code, the deviations, and the next action. Your Session section reads SESSION 2 of feature F263,
round 9, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), then the Open PR
Gate — the pull request this round opens is merged by the NEXT feature's session, never by this
one — and then Rule A5, the first unchecked feature in `docs/roadmap/STATUS.md`. State the
open-findings count, 28, and the operator-questions count, 0.
