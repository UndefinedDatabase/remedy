STEP R15 — F277 closure: the one bad node, repaired, and the suite re-read

GOAL
The integration gate is red at exactly one node. `command_discovery_completed` got its
writer in F277 round 3 and the UI's humanize catalog was never given the matching entry,
so a Python emitter and a TypeScript catalog have drifted apart. The repair is one catalog
line. This is the FIRST repair round under the shrinking rule of operator amendment
amend0917 rule 2, which allows three: the bad set must strictly SHRINK with no node newly
bad.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep `.agent/plan.md` current, keep the tree
clean, push at the end, rewrite `.agent/handoff.md`. You never issue a verdict.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f277-r15-payloads/`  READ-ONLY. The reviewer's originals live here and this
      round's transport proof is a comparison against them. Read them; never write here.
  `.remedy-wt/f277-r15-scratch/`   YOURS. Every log, exit-code capture and driver script
      goes here. Both are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, and multi-operation one-liners chained
with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and NEVER pipe pytest into `tail` — the shell
reports the pipe's last exit code, which is how a red suite reads as 0. Redirect to a file
in your scratch directory and read the file. Use `python3 -c` or `python3 - <<'PY'` for
counting, hashing and copying (`shutil.copyfile`); a `python3 -c` script containing a
newline followed by `#` is rejected, so use the heredoc there.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty and `git branch --show-current` must read
   `feature/f277-machine-contracts` at `4a7877ba`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f277-r15-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.

PAYLOADS — all four under `.remedy-wt/f277-r15-payloads/`
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| catalog.diff | 11 | 710 | a9b88a27aad50f28935acabe24e705809bf4feec5819b823ad31fe7ce3b97df0 |
| ledger.md | 2 | 5668 | 001cbadd00f4b3d51aafc145959365845e398a575b6796415ef243b0a27e5d19 |
| plan.md | 45 | 2356 | 2d48e7729bffdff91d43079f64fc5bcb3e144b48a1194844411c9e632d0fc368 |
| slips.md | 2 | 2344 | b5936db13f0cd255272c5c558282c49d5a006d59db8064a9bfd2858e007be2a3 |

`ledger.md` is an APPEND of ONE PARAGRAPH beginning with a single newline that is the
record separator. `slips.md` is an APPEND of TWO LINES with NO leading newline.
`plan.md` is a REWRITE. `catalog.diff` goes on with `git apply`; it was generated from the
tree at `4a7877ba` and dry-run with `git apply --check` at exit 0. Its pair was tested
mechanically for containment: TO contains FROM: true, so it is APPEND-shaped and the §4.9
append obligation applies — no FROM-zero count is owed. There is no decisions payload and
no questions payload; `.agent/decisions.md` and `.agent/operator_questions.md` are not
touched.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order

C1a — copy this block and all four payloads into `.agent/authored/`
  `.agent/authored/f277-r15-block.md` := this block, byte-for-byte, and one
  `.agent/authored/f277-r15-<name>` per payload, keeping each payload's own file name.
  Subject: `F277 R15 C1a: copy round 15 payloads into .agent/authored/`
  SIZE. The payloads total 60 lines, so this commit's insertions are 60 plus this block's
  own line count, and the 500 cap of DECISION F104 D1 binds at 440 block lines. Round 12
  spent this FEATURE'S ONE permitted oversize declaration, so a second is a Medium finding
  and not a declaration you may make. Compute `500 minus 60 minus <the block line count you
  measured>`, report it beside your measured insertions, and STOP rather than commit if it
  is negative.

C1b — book round 14's PASS and two slips, rewrite the plan
  `.agent/live_review.md` += ledger.md (append, +2)
  `.agent/prose_slips.md` += slips.md  (append, +2)
  `.agent/plan.md`        := plan.md   (rewrite, +16/-17)
  Subject: `F277 R15 C1b: book round 14's PASS and two reviewer slips, rewrite plan`
  EXPECTED INSERTIONS: 20 by `git show --numstat` — 2 plus 2 plus the plan rewrite's own
  DIFF insertions of 16, all three measured by applying these payloads in a disposable
  worktree at `4a7877ba` and reading `git diff --numstat`. If your measurement differs
  from 20, report the number you measured and say so; do not adjust the payload.

C2 — THE REPAIR: one catalog entry, so the emitter and the catalog agree again
  `git apply .remedy-wt/f277-r15-payloads/catalog.diff`, touching only
  `apps/ui/src/api/humanizeCatalog.ts`. It inserts
  `"command_discovery_completed"` with a one-sentence rendering line, in alphabetical
  position directly after `"command.accepted"`.
  Subject: `F277 R15 C2: give the humanize catalog the command discovery entry`
  Expected insertions: 1, measured the same way.

C3 — THE RED-PROOFS, in a DISPOSABLE worktree only (guardrail G5)
  `git worktree add --detach .remedy-wt/f277-r15-g3 <C2>`, removed as this commit's last
  action with `git worktree remove`, then report `git worktree list`. This is production
  code under `apps/`, so the red-proofs are mandatory. The contract test reads the
  TypeScript SOURCE as text and needs no `node_modules`, which the reviewer confirmed by
  running it in a fresh worktree — so the R-0703 environment trap does not apply here and
  no `--config` is owed.
  In that worktree run, serially, for each of the two mutations:
  `python3 -m pytest -q -p no:cacheprovider tests/ui_contracts/test_humanize_catalog.py`.
  Run the UNMUTATED CONTROL FIRST and report it; the reviewer read `12 passed`, exit 0.
  For each mutation: report the summary line, the real exit code and every FAILED node id,
  then restore the file byte-identically and confirm before the next. A mutation that
  stays GREEN is a finding: stop and report.
   (a) Insert the line `  "no_such_event_is_ever_emitted": "Nothing writes this.",`
       directly above the new `"command_discovery_completed"` entry — a catalog key no
       Python emitter writes. Expected: `1 failed, 11 passed`, exit 1, at
       `TestCatalogCoversTheStreamVocabulary::test_catalog_keys_equal_the_static_stream_vocabulary`.
   (b) Change the new key `"command_discovery_completed"` to
       `"command_discovery_complete"`, one character short, which leaves the real emitter
       uncovered. Expected: the same node, `1 failed, 11 passed`, exit 1.
  This commit writes NOTHING in the primary checkout. Its subject records the proofs:
  Subject: `F277 R15 C3: red-prove the catalog entry in both directions`
  If you have no change to commit here, say so and fold the readings into the handback
  rather than inventing a file to touch — an empty commit is not this block's intent.

C4 — THE SUITE, RE-READ, AND WHY THIS IS NOT A SECOND RUN OF A ONCE-ONLY GATE
  Operator amendment amend0917 rule 1 runs the full suite once per feature, and the
  standing answer to operator question Q1 of 2026-09-20 — executed, unreversed, and
  recorded in `.agent/operator_questions.md` — is that the one run belongs to the code
  actually being shipped: where the tree that run certified has been replaced, the honest
  reading is that the run moves with it. The transcript now on disk certifies `42af2188`,
  which C2 replaces, and the shrinking rule of amend0917 rule 2 cannot be evidenced at
  all without a reading of the repaired tree. So:
  First, best-effort, report the outcome either way and do not stop on a refusal:
  `npm run build` in `apps/ui`, so the built bundle is not older than the source C2
  edits. The reviewer measured that no test asserts `apps/ui/dist` freshness, so a
  failure or a denial here is reportable and not fatal — say which happened.
  Then, in the PRIMARY CHECKOUT, never a worktree:
```
python3 -m pytest -n auto -q
```
  Redirect to a file under your scratch directory and capture the REAL exit code with no
  pipe. Then REWRITE `.agent/authored/f277-closure-suite.txt` in the same shape it already
  has — command, checkout and commit, real exit code, wall clock, summary line, and the
  full list of bad node ids one per line or the words `no bad nodes` — and commit it.
  Subject: `F277 R15 C4: re-run the closure suite against the repaired tree`
  A still-red suite is a legitimate outcome: record every bad node id honestly and hand
  back. Do NOT repair anything further — round 16 would be the second of the three
  repair rounds the rule allows, and it is the reviewer's to order.

C5 — the handback
  Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`, then
  `git push -u origin feature/f277-machine-contracts`. G6's readings only exist after
  that push, so write them into the handback's own gate section AFTER pushing rather than
  adding a trailing commit — round 14 made that call and this block adopts it.
  Subject: `F277 R15 C5: rewrite handoff for round 15`

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. Do not touch any file this block does not name. The round's whole tracked path set is
   the five `.agent/authored/f277-r15-*` copies, `.agent/authored/f277-closure-suite.txt`,
   `.agent/live_review.md`, `.agent/prose_slips.md`, `.agent/plan.md`,
   `apps/ui/src/api/humanizeCatalog.ts` and `.agent/handoff.md`. Report the length you
   measure rather than checking it against a number this block states.
4. If a gate goes red, STOP — with ONE stated exception, C4's suite, whose red is an
   outcome this block asks you to record rather than repair. Commit and push what is
   verified, write an honest handoff under AGENTS.md "If Blocked", and hand back.
5. Leave the `remedy/job-86f628f5e4fb4e0c` worktree and branch alone; round 13's self-use
   run retained it by design. Do not touch `scripts/self_use_queue.json`.
6. `npm run build` may write under `apps/ui/dist` and `apps/ui/node_modules`, both
   gitignored. If it leaves any TRACKED file dirty, that is a finding: stop and report it
   rather than committing the change.

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4).

G1 TRANSPORT AND STATE
 (a) For each of the four payload files, report the line count, byte count and sha256 you
     measured against the PAYLOADS table above. Twelve readings, all equal.
 (b) For each `.agent/authored/f277-r15-*` copy at C1a — one per payload plus the block
     copy — compare it byte-for-byte with its source under
     `.remedy-wt/f277-r15-payloads/` (the block copy against
     `.remedy-wt/f277-r15-block.md`). Report one reading per copy and the number of copies
     you compared; all True.
 (c) The two appends at C1b. For each of `.agent/live_review.md` and
     `.agent/prose_slips.md`: the file's bytes at `4a7877ba` plus the payload's bytes equal
     the file's bytes at C1b. The reviewer measured the pres as 467843 and 351269 and the
     posts as 473511 and 353613; report yours beside them. Then ONE negative control, on
     `.agent/live_review.md` only: flip a single bit inside the appended paragraph and show
     the reading returns False. Use strict byte concatenation, not a length comparison — a
     same-length flip stays True under a length-only reader, as round 14 reported.
 (d) `.agent/plan.md` at C1b equals `plan.md` byte-for-byte at 45 lines, under the 50-line
     rule of AGENTS.md. Report both sha256s and the line count.
 (e) The open set by distinct id in `.agent/live_review.md` — ids matching `^- R-\d+ — `
     minus ids matching `^Done: R-\d+ — ` — is 22 at `4a7877ba` and 22 at C1b. Report both
     numbers, not a claim that they match. Round 15 registers and resolves nothing.

G2 THE REPAIR — at C2, run
 `python3 -m pytest -q -p no:cacheprovider tests/ui_contracts/test_humanize_catalog.py`
 and report the summary line and the real exit code. The reviewer measured this in a
 disposable worktree at `4a7877ba`: unrepaired `1 failed, 11 passed` at exit 1, which is
 the closure suite's bad node; repaired `12 passed` at exit 0. Then
 `git diff --name-only <C1b> <C2>` must name exactly `apps/ui/src/api/humanizeCatalog.ts`
 — report the list and its length.

G3 THE RED-PROOFS — as C3 specifies: the unmutated control, then mutations (a) and (b),
 each with its summary line, real exit code, failed node ids and a confirmed
 byte-identical restore, then the restored control, then `git status --porcelain` inside
 the mutation worktree, then `git worktree remove` and `git worktree list`.

G4 LINT AND CANARY — `python3 -m ruff check` over every Python file this round's path set
 holds; if that set holds none, report that as the measured reason ruff was not run rather
 than reporting a run that did not happen. Then the standing canary,
 `python3 -m pytest tests/cli/test_golden_path.py -q`, with its output and exit code.

G5 THE SUITE AND THE SHRINKING RULE — report C4's `npm run build` outcome, then the
 suite's summary line, its REAL exit code captured without a pipe, its wall clock, and the
 complete list of bad node ids with its length. Then state the shrinking rule's two
 readings explicitly against the PREVIOUS transcript's set, which holds exactly
 `tests/ui_contracts/test_humanize_catalog.py::TestCatalogCoversTheStreamVocabulary::test_catalog_keys_equal_the_static_stream_vocabulary`:
 whether the new set is a STRICT SUBSET of it, and which nodes if any are newly bad.
 Report both as sets you computed, not as a verdict. Finally confirm that the rewritten
 `.agent/authored/f277-closure-suite.txt` is committed and that its bad-node list is
 byte-identical to the list you just reported.

G6 PUSH AND TREE — after C5: `git push -u origin feature/f277-machine-contracts` and
 report its outcome, then `git status --porcelain`, which must be empty, and
 `git worktree list`. Write these readings into the handback after the push, per C5.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: the state block, the per-commit
changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the item-status table, the deviations,
and the next expected action. Report what you ran, not what you expected to find. Your
Session section reads SESSION 7 of feature F277, round 15.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), then the
review of round 15, then — if the suite came back green — the evidence job and the FRESH
review zip, whose `base_commit` is the branch's FORK POINT `f2494c02`; or, if it is still
red, the second of the three repair rounds. State the open-findings count, which is 22,
and the operator-questions count, which is 2.
