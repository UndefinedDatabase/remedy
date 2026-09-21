STEP R18 — F277 CLOSURE: the consolidation, the rotation, the flip and the pull request

GOAL
Every closure precondition holds. Book round 17's PASS, resolve R-1014 through the single
checklist consolidation pass, rotate the ledger, and flip F277 to `[x]` with the README
sync and the SU-025 `consumed_by` edit in ONE commit that is the LAST on this branch.
Then open the pull request. The pull request is NOT merged in this session — it merges at
the next feature's start through the Open PR Gate, which is the operator's review window.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

READ FIRST, BEYOND THE THREE YOUR DELEGATION NAMES
`docs/roadmap/STATUS_closure_protocol.md` Algorithm steps 4 and 5 in full, including the
amend0905-throughput rotation paragraph and the amend0911-feedback ownership paragraph.
This round IS step 5, and step 5 fixes the closure commit's path set exactly.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f277-r18-payloads/`  READ-ONLY. The reviewer's originals live here and this
      round's transport proof is a comparison against them. Read them; never write here.
  `.remedy-wt/f277-r18-scratch/`   YOURS. Every log, exit-code capture and script goes
      here. Both are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, and multi-operation one-liners chained
with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and never pipe pytest into `tail`. Use
`python3 -c` or `python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`);
a `python3 -c` script containing a newline followed by `#` is rejected, so use the
heredoc there.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty and `git branch --show-current` must read
   `feature/f277-machine-contracts` at `365051fa`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f277-r18-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.

PAYLOADS — all six under `.remedy-wt/f277-r18-payloads/`
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| checklist.diff | 24 | 1865 | 47f97064d756f9ca79ca694d12e2cd4a31ef59960574d618f1e23b8c0502c329 |
| ledger.md | 4 | 5572 | 9d0cecea7069a4c7390201d755a536d52b58fd561a074b6a1920ed3d2d201283 |
| plan.md | 46 | 2314 | 7420146c3f96c4078923f574f0987796b739a345287a0824a885112d864cb41f |
| queue.diff | 12 | 9431 | 602ea535db08600bfe831123717d72f5824dcf9d50474e2380629885648c37d9 |
| readme.diff | 35 | 1627 | bf1d4d52edf45eadd8062dada116300188474e98d0392226579808e93a0af47d |
| status.diff | 12 | 2398 | 4c6be11764e32cb5ca01c4f9a61e8755dc204c94ff3a2c930f6fca0b9c8e5bc0 |

`ledger.md` is an APPEND of TWO PARAGRAPHS beginning with a single newline that is the
record separator: the round 17 `Gate:` entry and the `Done: R-1014` resolution, in that
order. `plan.md` is a REWRITE. The four `.diff` files go on with `git apply`; every one
was generated from the tree at `365051fa` and dry-run with `git apply --check` at exit 0.
`checklist.diff` and `readme.diff` were tested mechanically for containment — TO contains
FROM: true for both, so both are APPEND-shaped and no FROM-zero count is owed;
`status.diff` and `queue.diff` each replace one line with one line and are REWRITES.
There is no slips payload and no decisions payload this round.

BUNDLE — the commits are C1a, C1b, C2, C3 and C4, in this order, and C4 IS THE LAST
COMMIT ON THIS BRANCH

C1a — copy this block and all six payloads into `.agent/authored/`
  `.agent/authored/f277-r18-block.md` := this block, byte-for-byte, and one
  `.agent/authored/f277-r18-<name>` per payload, keeping each payload's own file name.
  Subject: `F277 R18 C1a: copy round 18 payloads into .agent/authored/`
  SIZE. The payloads total 133 lines, so this commit's insertions are 133 plus this
  block's own line count, and the 500 cap binds at 367 block lines. Round 12 spent this
  FEATURE'S ONE permitted oversize declaration. Compute `500 minus 133 minus <the block
  line count you measured>`, report it, and STOP rather than commit if it is negative.

C1b — book round 17's PASS and resolve R-1014
  `.agent/live_review.md` += ledger.md (append, +4)
  `.agent/plan.md`        := plan.md   (rewrite, +26/-24)
  Subject: `F277 R18 C1b: book round 17's PASS and resolve R-1014`
  EXPECTED INSERTIONS: 30 by `git show --numstat` — 4 plus the plan rewrite's own DIFF
  insertions of 26, measured by applying these payloads in a disposable worktree at
  `365051fa`. If yours differs, report what you measured and say so.

C2 — THE SINGLE CHECKLIST CONSOLIDATION PASS, which is what resolves R-1014
  `git apply .remedy-wt/f277-r18-payloads/checklist.diff`, touching only
  `docs/agents/planner_reviewer_prompt.md`. R-1014's fix clause asked for its rule to
  MERGE into item 12 rather than become a new item, because amend0827 rule 4 forbids the
  list to grow; the diff appends a clause to item 12 and adds no item.
  Subject: `F277 R18 C2: merge R-1014's rule into checklist item 12`
  Expected insertions: 14.

C3 — THE LEDGER ROTATION, its own commit, exactly as amend0905-throughput orders
  `python3 scripts/rotate_live_review.py`. Its path set is exactly
  `.agent/live_review.md` and `.agent/live_review_archive.md`; if it touches anything
  else, STOP. Report the script's full output, which prints the old and new sizes.
  Subject: `F277 R18 C3: rotate the live review ledger into its archive`
  The reviewer ran this in a disposable worktree over the same slices: the ledger goes
  from 492707 to 421313 bytes, the archive from 4361155 to 4432550, and the open-findings
  count is 22 before and 22 after — that equality is the property the rotation must
  preserve and the one to report.
  THE ROTATION RUNS AFTER C1b ON PURPOSE. It moves every resolved finding PAIR into the
  archive, so `R-1014`'s registration and its `Done:` line travel together; running it
  before C1b would leave the registration behind and the resolution in front of it.

C4 — THE CLOSURE COMMIT, last on the branch under Rule A4
  `git apply` each of `status.diff`, `readme.diff` and `queue.diff`, then rewrite
  `.agent/handoff.md`, then commit ALL FOUR PATHS TOGETHER:
  `docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json` and
  `.agent/handoff.md`. That is exactly the path set Algorithm step 5 fixes, and R-0154
  requires the README sync in the SAME commit as the STATUS `[x]` edit because README and
  STATUS may never disagree in any committed state.
  Subject: `F277 R18 C4: close F277 — STATUS x, README sync, SU-025 consumed`
  Expected insertions: 1 for STATUS, 10 for README, 1 for the queue, plus the handoff's.
  Then `git push -u origin feature/f277-machine-contracts`, then create the pull request
  with `gh pr create`. DO NOT MERGE IT — guardrail G1 forbids merging a pull request this
  session created, and the gap is the operator's review window.
  THE HANDOFF CANNOT NAME THE PULL REQUEST NUMBER, which does not exist when C4 is
  written, and no trailing commit may fix that: DECISION amend0827 D2 permits exactly ONE
  successor to the closure commit and only when its path set is exactly
  `.agent/candidates.md`, which this is not. Write the push and the pull request as
  PENDING in the handoff and report their real outcomes, with the pull request number and
  URL, in your reply.

THE PULL REQUEST DESCRIPTION carries what AGENTS.md's PR workflow requires: what changed
and why, the key decisions (F277 D5 through D10), how to review, the changed-files
summary, the latest verdict, the open-findings count and the runtime actuals you can read
from the record — rounds, and the closure suite's own numbers. End it with exactly:
`🤖 Generated with [Claude Code](https://claude.com/claude-code)`

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. Do not touch any file this block does not name. The round's whole tracked path set is
   the seven `.agent/authored/f277-r18-*` copies, `.agent/live_review.md`,
   `.agent/live_review_archive.md`, `.agent/plan.md`,
   `docs/agents/planner_reviewer_prompt.md`, `docs/roadmap/STATUS.md`, `README.md`,
   `scripts/self_use_queue.json` and `.agent/handoff.md`. Report the length you measure
   rather than checking it against a number this block states. In particular do NOT touch
   `.agent/candidates.md`, `.agent/decisions.md`, `.agent/operator_questions.md` or
   `docs/roadmap/features/T2_F277.md`, whose Built State is already current.
4. If a gate goes red, STOP, and STOP HARDER HERE THAN ANYWHERE: a closure that half
   lands is worse than one that does not start. Commit and push what is verified, write
   an honest handoff under AGENTS.md "If Blocked", and hand back.
5. NOTHING IS MERGED. No `gh pr merge`, no checkout of `main`, no branch deletion.
6. Leave the three `remedy/job-*` worktrees and both review packages alone.

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4).

G1 TRANSPORT AND STATE
 (a) For each of the six payload files, report the line count, byte count and sha256 you
     measured against the PAYLOADS table above. Eighteen readings, all equal.
 (b) For each `.agent/authored/f277-r18-*` copy at C1a — one per payload plus the block
     copy — compare it byte-for-byte with its source under
     `.remedy-wt/f277-r18-payloads/` (the block copy against
     `.remedy-wt/f277-r18-block.md`). Report one reading per copy and how many you
     compared; all True.
 (c) The append at C1b, by strict byte concatenation: the file's bytes at `365051fa` plus
     the payload's bytes equal the file's bytes at C1b. The reviewer measured 487135 plus
     5572 equals 492707; report yours beside that. Then reading (b), the independent
     structural reader (§3 item 36): let N be the number of blank-line-separated
     paragraphs your script COUNTS in `ledger.md`, and compare the LAST N such units of
     the whole file against those N paragraphs IN ORDER. Report N as you counted it. Then
     ONE negative control: flip a single bit inside the FIRST appended paragraph and show
     BOTH readings return False.
 (d) `.agent/plan.md` at C1b equals `plan.md` byte-for-byte at 46 lines. Report both
     sha256s and the line count.
 (e) The open set by distinct id in `.agent/live_review.md`: report it at `365051fa`, at
     C1b and at C3, as three numbers. The reviewer measured 23, then 22 once `R-1014`
     resolves, then 22 again after the rotation — the rotation MOVES records and changes
     no count, which is the property amend0905-throughput requires of it.

G2 THE CONSOLIDATION DID NOT GROW THE LIST — at C2, count the pre-emission checklist's
 items in `docs/agents/planner_reviewer_prompt.md` mechanically (the lines matching
 `^  \d{1,2}\. \*\*`, taking the first 34 of them, since a later numbered list in that
 file reuses small numbers) and report the count and the numbers BEFORE and AFTER the
 edit. Both must be 34, running 1 to 16, 18, 20 to 31 and 33 to 37. Amend0827 rule 4
 requires the list to come out the same length or shorter, and its own paragraph names 34
 as the figure this consolidation measures against. Then `git diff --name-only <C1b> <C2>`
 must name exactly that one path.

G3 THE ROTATION PRESERVED THE RECORD — at C3, report the script's full output and real
 exit code, the ledger's and the archive's byte sizes before and after, the open-findings
 count before and after (equal), and `git diff --name-only <C2> <C3>`, which must name
 exactly `.agent/live_review.md` and `.agent/live_review_archive.md`. Then confirm by
 search that the archive now holds both the `- R-1014` registration and its
 `Done: R-1014` line, and that the live ledger holds neither — a pair moves whole or the
 rotation is wrong.

G4 THE CLOSURE COMMIT IS EXACTLY WHAT THE PROTOCOL FIXES — at C4,
 `git diff --name-only <C3> <C4>` must name exactly `README.md`,
 `docs/roadmap/STATUS.md`, `scripts/self_use_queue.json` and `.agent/handoff.md`. Report
 the list and its length. Then report, read back from the committed tree: F277's STATUS
 line in full, the README's `N of M registered items accepted` line, the README Tier 2
 table row, and `SU-025`'s `consumed_by` value. The STATUS line's `accepted HEAD` must
 read `deeac639488b1cb1be930a550b2295509652051f`, which is the manifest's
 `committed_review_subject.head_commit` for the READY package, and its package and
 SHA-256 segments must match
 `remedy-review-20260921-032054-READY_FOR_REVIEW.zip` and
 `cd8542e0a6d2ec18fa9d171dcc2a762574e57911d48867e762f81b5dd1681723` — re-read those two
 off the package file itself rather than off this block, and report both readings.

G5 THE CLOSURE GATES — run, and report with real exit codes:
```
python3 -m pytest -q -p no:cacheprovider tests/docs/ \
  tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py \
  tests/regression/test_resource_safety.py
```
 The reviewer's dry run, taken in a disposable worktree at `365051fa` with every slice of
 this round applied INCLUDING the rotation, read `449 passed, 2 skipped` at exit 0; with
 the README accepted count left at 87 it read `1 failed, 448 passed, 2 skipped` at exit 1,
 and with the Tier 2 Done cell left at 29 the same — so the gate can fail and its green
 means something. Then `remedy integrity check --json`, which is closure precondition 3;
 all five checks must read `pass`. Do NOT run the full suite: it ran once, at round 15,
 and `.agent/authored/f277-closure-suite.txt` is what the closure reads back.

G6 PUSH, PULL REQUEST AND TREE — after C4: `git push -u origin
 feature/f277-machine-contracts` and report its outcome; then `gh pr create` and report
 the pull request's number and URL; then `git status --porcelain`, which must be empty,
 `git log --oneline -n 1`, which must be C4, and `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, which must show exactly this one pull request,
 not a draft, from `feature/f277-machine-contracts` into `main`.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: the state block, the per-commit
changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the item-status table, the deviations,
and the next expected action. Report what you ran, not what you expected to find. Your
Session section reads SESSION 7 of feature F277, round 18.

YOUR `## Next` NAMES, IN ORDER, because F277 ends here and the next session starts cold:
Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 18, then the Open
PR Gate, which merges THIS pull request before any new branch is cut. Then Rule A5, which
proposes F283, standing directly behind F277. Name one carried item explicitly:
`.agent/candidates.md` still holds three entries, each recording the finding id it was
registered as, and the disk-vehicle rule makes a non-empty candidates file a block
condition at feature-claim time — so F283's FIRST reviewed round resolves and empties it.
State the open-findings count, which is 22 after C1b, and the operator-questions count,
which is 2.
