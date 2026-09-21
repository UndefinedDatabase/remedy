STEP R14 — F277 closure: the round 13 repair, and the integration gate

GOAL
Round 13 is FAIL and this is its repair round. Generating the closure's self-use item
copied a ledger paragraph carrying a retired word into `scripts/self_use_queue.json`, so
the branch tip is RED on `tests/docs/test_retired_promote_word.py`. Register that defect
and the self-use run's own blocked strings, land the repair, and then run the INTEGRATION
GATE: the full suite, once, for the whole feature, with its transcript committed. Findings
persist FIRST, in their own commit, before the repair (§4 item 4).

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep `.agent/plan.md` current, keep the tree
clean, push at the end, rewrite `.agent/handoff.md`. You never issue a verdict.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f277-r14-payloads/`  READ-ONLY. The reviewer's originals live here and this
      round's transport proof is a comparison against them. Read them; never write here.
  `.remedy-wt/f277-r14-scratch/`   YOURS. Every log, exit-code capture and driver script
      goes here. Both are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR — do not spend turns rediscovering them.
Denied outright: `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`, `cp`, process
substitution `<(...)`, and multi-operation one-liners chained with `;` or `&&` outside a
`bash -c`. The Bash tool does not surface a non-zero exit on its own, so capture every
gate's REAL code as `bash -c '<cmd>; echo "REAL_EXIT=$?"'` — and note that a pipe into
`tail` reports TAIL's exit code, not pytest's, which is exactly how a red suite can read
as exit 0. Redirect to a file in your scratch directory and read the file instead. For
counting, hashing, byte arithmetic and copying use `python3 -c` or `python3 - <<'PY'`;
`shutil.copyfile` is how you copy. A `python3 -c` script containing a newline followed by
`#` is rejected; use the heredoc form there.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty and `git branch --show-current` must read
   `feature/f277-machine-contracts` at `24f36eaf`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f277-r14-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.

PAYLOADS — all four under `.remedy-wt/f277-r14-payloads/`
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| guard.diff | 22 | 1169 | bed28a452219e16071f41ad95050cf92ce1cf22a8e93855a47e547f51ca6cae7 |
| ledger.md | 6 | 12978 | 004f0081351a2ef2821e6e4ecdc80065127e4b49193a090099037d91bfee4fca |
| plan.md | 46 | 2360 | 00ecf72718137091f3d44709c47d8cce1f3e26b041582925b2dddc460412dad4 |
| slips.md | 3 | 3211 | d9cc4606c545ae2ee6049237e3ccb0b1c93795848b1a0aa2c4715cdf6893a62d |

`ledger.md` is an APPEND of THREE PARAGRAPHS beginning with a single newline that is the
record separator: the R-1015 registration, the R-1016 registration, and the round 13
`Gate:` entry, in that order, each on one line with a blank line between them, which is
the shape every entry in that file already has. `slips.md` is an APPEND of THREE LINES
with NO leading newline. `plan.md` is a REWRITE. `guard.diff` goes on with `git apply`; it
was generated from the tree at `24f36eaf` and dry-run with `git apply --check` at exit 0.
Its pair was tested mechanically for containment: TO contains FROM: true, so it is
APPEND-shaped and the §4.9 append obligation applies — no FROM-zero count is owed and
ordering one would be unmeetable. There is no decisions payload and no questions payload;
`.agent/decisions.md` and `.agent/operator_questions.md` are not touched.

BUNDLE — the commits are C1a, C1b, C2, C3 and C4, in this order

C1a — copy this block and all four payloads into `.agent/authored/`
  `.agent/authored/f277-r14-block.md` := this block, byte-for-byte, and one
  `.agent/authored/f277-r14-<name>` per payload, keeping each payload's own file name.
  Subject: `F277 R14 C1a: copy round 14 payloads into .agent/authored/`
  SIZE. The payloads total 77 lines, so this commit's insertions are 77 plus this block's
  own line count, and the 500 cap of DECISION F104 D1 binds at 423 block lines. Round 12
  spent this FEATURE'S ONE permitted oversize declaration, so a second is a Medium finding
  and not a declaration you may make. Compute `500 minus 77 minus <the block line count you
  measured>`, report it beside your measured insertions, and STOP rather than commit if it
  is negative.

C1b — FINDINGS PERSIST FIRST: register R-1015 and R-1016, book round 13's FAIL, rewrite
      the plan
  `.agent/live_review.md` += ledger.md (append, +6)
  `.agent/prose_slips.md` += slips.md  (append, +3)
  `.agent/plan.md`        := plan.md   (rewrite, +18/-21)
  Subject: `F277 R14 C1b: register R-1015 and R-1016, book round 13's FAIL, rewrite plan`
  EXPECTED INSERTIONS: 27 by `git show --numstat` — 6 plus 3 plus the plan rewrite's own
  DIFF insertions of 18. Every one of those three numbers was measured by applying these
  same payloads in a disposable worktree at `24f36eaf` and reading `git diff --numstat`,
  not counted by eye; that is the counter-measure this round's second prose-slip line puts
  in force. If your measurement differs from 27, report the number you measured and say
  so; do not adjust the payload to reach it.

C2 — THE REPAIR: teach the retired-word guard that the queue file quotes the ledger
  `git apply .remedy-wt/f277-r14-payloads/guard.diff`, touching only
  `tests/docs/test_retired_promote_word.py`. It adds a `KEPT_BY_SENSE` entry for
  `scripts/self_use_queue.json` under the guard's own existing sense
  `H: history or a retired-word guard`, carrying the one token `promotion`, with a comment
  naming R-1015 and saying the entry is a stopgap the generator's own screen will retire.
  Subject: `F277 R14 C2: teach the retired-word guard that the self-use queue quotes the
  ledger`
  Expected insertions: 12, measured the same way.
  DO NOT add any other token, do not widen the entry to the whole file, and do not touch
  `scripts/self_use_queue.json` — the queue's pending item is closure precondition 6's and
  editing it here would break the run this closure already made.

C3 — THE INTEGRATION GATE, and it runs ONCE for the whole feature
  First `remedy integrity check --json`, which is closure precondition 3. Report the full
  JSON and the exit code. The reviewer read all five checks `pass` at exit 0 at
  `24f36eaf`; `plan_consistency` reporting `context_complete=False` is part of that pass
  and is not a failure.
  Then, in the PRIMARY CHECKOUT, never a worktree:
```
python3 -m pytest -n auto -q
```
  Redirect its output to a file under your scratch directory and capture the REAL exit
  code — do not pipe into `tail`, which would report tail's code. Then write
  `.agent/authored/f277-closure-suite.txt` containing the summary line and the FULL list
  of bad node ids (failed plus errors), one per line, or the words `no bad nodes` when
  there are none, and commit that file.
  Subject: `F277 R14 C3: integration gate — the full suite once, transcript committed`
  This is the ONE full-suite run of this feature (amend0917 rule 1). A RED suite is a
  legitimate outcome of this gate, not a gate failure: record every bad node id honestly
  and hand back. The repair rules of amend0917 rule 2 are the reviewer's to order next
  round, and inventing a repair here would spend a round the shrinking rule has to count.

C4 — the handback
  Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`, then
  `git push -u origin feature/f277-machine-contracts`.
  Subject: `F277 R14 C4: rewrite handoff for round 14`

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. Do not touch any file this block does not name. The round's whole tracked path set is
   the five `.agent/authored/f277-r14-*` copies, `.agent/authored/f277-closure-suite.txt`,
   `.agent/live_review.md`, `.agent/prose_slips.md`, `.agent/plan.md`,
   `tests/docs/test_retired_promote_word.py` and `.agent/handoff.md`. NO file under
   `packages/` or `apps/`, and NOT `scripts/self_use_queue.json`.
4. If a gate goes red, STOP — with ONE stated exception, which is C3's suite, whose red is
   an outcome this block asks you to record rather than repair. Do not repair the
   reviewer's slice and do not guess which half of a disagreement is wrong. Commit and
   push what is verified, write an honest handoff under AGENTS.md "If Blocked", and hand
   back. Round 8 did exactly that.
5. There is NO mutation red-proof this round: the change set holds no file under
   `packages/` or `apps/`, so §3's standing obligation over production code has nothing to
   bite on. The guard entry's own red controls were run by the reviewer before emission
   and their readings are in G2 for you to compare against, not to repeat.
6. A third `remedy/job-*` worktree and branch, `remedy/job-86f628f5e4fb4e0c`, exists from
   round 13's self-use run and is explained by that job's `cleanup_status: retained`.
   Leave it alone. Do not prune it, and do not treat it as a leak.

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4).

G1 TRANSPORT AND STATE
 (a) For each of the four payload files, report the line count, byte count and sha256 you
     measured against the PAYLOADS table above. Twelve readings, all equal.
 (b) For each of the five `.agent/authored/f277-r14-*` copies at C1a — the four payload
     copies and the block copy — compare it byte-for-byte with its source under
     `.remedy-wt/f277-r14-payloads/` (the block copy against
     `.remedy-wt/f277-r14-block.md`). One reading per copy; all True.
 (c) The two appends at C1b, with reading (a) the byte arithmetic and reading (b) an
     independent STRUCTURAL reader (§3 item 36). Byte arithmetic: for each of
     `.agent/live_review.md` and `.agent/prose_slips.md`, the file's bytes at `24f36eaf`
     plus the payload's bytes equal the file's bytes at C1b — the reviewer measured the
     two pre values as 454865 and 348058 and the two posts as 467843 and 351269; report
     yours beside them. Structural reader, on `.agent/live_review.md`: let N be the number
     of blank-line-separated paragraphs your script COUNTS in `ledger.md`, and compare the
     LAST N such units of the whole file against those N paragraphs IN ORDER. Report N as
     you counted it. Then ONE negative control: flip a single bit inside the FIRST
     appended paragraph and show BOTH readings return False.
 (d) `.agent/plan.md` at C1b equals `plan.md` byte-for-byte at 46 lines, under the 50-line
     rule of AGENTS.md. Report both sha256s and the line count.
 (e) The open set by distinct id in `.agent/live_review.md` — ids matching `^- R-\d+ — `
     minus ids matching `^Done: R-\d+ — ` — is 20 at `24f36eaf` and 22 at C1b, because
     this round registers R-1015 and R-1016 and resolves neither. Report both numbers and
     the two new ids, not a claim that the arithmetic works out.

G2 THE REPAIR, AND THAT IT DID NOT BLUNT THE GUARD
 At C2, run `python3 -m pytest -q -p no:cacheprovider tests/docs/` and report the summary
 line and the real exit code. The reviewer measured this in a disposable worktree detached
 at `24f36eaf`: unrepaired `1 failed, 313 passed` at exit 1, which is the defect; repaired
 `314 passed` at exit 0. Then report the `KEPT_BY_SENSE` entry for
 `scripts/self_use_queue.json` verbatim from the file, and confirm by count that the entry
 lists exactly one token. `git diff --name-only <C1b> <C2>` must name exactly
 `tests/docs/test_retired_promote_word.py` — report the list and its length.

G3 CLOSURE PRECONDITION 3 — `remedy integrity check --json` at C3. Report the full JSON
 and the real exit code. All five checks must read `pass`; if any reads `fail`, STOP and
 hand back, because that is a closure precondition and not a repairable gate.

G4 THE INTEGRATION GATE — the full suite, once, as C3 specifies. Report the summary line,
 the REAL exit code captured without a pipe, the wall clock, and the complete list of bad
 node ids (failed plus errors) with its length. Then report that
 `.agent/authored/f277-closure-suite.txt` is committed and that its bad-node list is
 byte-identical to the list you just reported — the transcript is what the closure reads
 back instead of re-running, so a transcript that disagrees with the run is worse than no
 transcript.

G5 THE ROUND'S WHOLE PATH SET — `git diff --name-only 24f36eaf <C3>` must name exactly the
 eleven paths constraint 3 lists other than `.agent/handoff.md`: the five
 `.agent/authored/f277-r14-*` copies, `.agent/authored/f277-closure-suite.txt`,
 `.agent/live_review.md`, `.agent/prose_slips.md`, `.agent/plan.md` and
 `tests/docs/test_retired_promote_word.py`. Report the full list and its length, and state
 for each entry which commit introduced it. Report as a measured count that no path under
 `packages/` or `apps/` appears, and that `scripts/self_use_queue.json` does not.

G6 PUSH AND TREE — after C4: `git push -u origin feature/f277-machine-contracts` and
 report its outcome, then `git status --porcelain`, which must be empty.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: the state block, the per-commit
changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the item-status table, the deviations,
and the next expected action. Report what you ran, not what you expected to find. Your
Session section reads SESSION 7 of feature F277, round 14.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), then the
review of round 14, then — if the closure suite was green — the evidence job and the
review zip, or, if it was red, the first repair round under the shrinking rule of
amend0917 rule 2. State the open-findings count, which is 22 after C1b, and the
operator-questions count, which is 2.
