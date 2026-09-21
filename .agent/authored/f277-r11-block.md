STEP R11 T003 (part 4) — F277: the memory group, six refusals under one token

GOAL
Book round 10's PASS and two reviewer slips, then migrate the `memory` group onto the
shared `fail()`. Nine refusal sites: one list-option refusal, a job lookup, and six card
lookups of which five are byte-identical, so the same condition now carries one token,
`memory_card_not_found`, wherever a card comes back empty. Five of the six card commands
carry no `--json` argument in the catalog yet — they are in the read-only-without-
`supports_json` set T003 empties at the end of the slice — so their handlers are threaded
and proved at the handler, and a guard test states that premise out loud instead of
leaving a later reader to infer it.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep `.agent/plan.md` current, keep the tree
clean, push at the end, rewrite `.agent/handoff.md`. You never issue a verdict.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f277-r11-payloads/`  READ-ONLY. The reviewer's originals live here and this
      round's transport proof is a comparison against them. Read them; never write here.
  `.remedy-wt/f277-r11-scratch/`   YOURS. Every log, exit-code capture, temporary script
      and note goes here. Both are gitignored.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty and `git branch --show-current` must read
   `feature/f277-machine-contracts` at `e90faf51`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f277-r11-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.

PAYLOADS — all four under `.remedy-wt/f277-r11-payloads/`
Verify each one's line count and sha256 BEFORE using it and report every reading. Never
retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 2 | 4388 | 33f0e0a13bd36d5aa724cebb5d2c2047e71f549038aa8663bf21d1b8c2455811 |
| plan.md | 49 | 2679 | 922b9ab526eec009b77ea90d90faaabd78afcbfdc56225b0c31a7baa160d8ee1 |
| slips.md | 2 | 1875 | 40b4f76db324004721064d71770d009a2d9eec3be93b62907dc708f12a6afe3d |
| s1-memory.diff | 294 | 11857 | dc77324d5e107ed4ff8e20f7659fe48d903f7ccf7460501508c4d6a2f79aca1e |

`ledger.md` is an APPEND and begins with a single newline that is the record separator.
`slips.md` is an APPEND of TWO LINES with NO leading newline, because
`.agent/prose_slips.md` holds one line per entry and no blank line between them.
`plan.md` is a REWRITE. There is NO decisions payload this round — the token
`memory_card_not_found` follows DECISION F277 D8's existing rule and settles nothing new,
so `.agent/decisions.md` is not touched. `s1-memory.diff` goes on with `git apply`; it
CREATES `tests/cli/test_memory_cmd.py`, which does not exist yet, so after applying it
you must `git add` that new file explicitly — `git apply` leaves it untracked.

BUNDLE — the commits are C1a, C1b, C2 and C3, in this order

C1a — copy the three state payloads into `.agent/authored/`
  `.agent/authored/f277-r11-block.md`  := this block, byte-for-byte
  `.agent/authored/f277-r11-ledger.md` := ledger.md
  `.agent/authored/f277-r11-plan.md`   := plan.md
  `.agent/authored/f277-r11-slips.md`  := slips.md
  Subject: `F277 R11 C1a: copy round 11 payloads into .agent/authored/`
  Expected insertions: this block's own line count plus 53. No fixed number is stated,
  because the block's count moves with every edit to the block itself. Report what you
  measure; it is far under 500 either way.

C1b — book round 10's PASS and two slips, rewrite the plan
  `.agent/live_review.md` += ledger.md  (append, +2)
  `.agent/prose_slips.md` += slips.md   (append, +2)
  `.agent/plan.md`        := plan.md    (rewrite, +18/-18)
  Subject: `F277 R11 C1b: book round 10's PASS and two slips, rewrite plan`
  EXPECTED INSERTIONS: 22 by `git show --numstat` — 2 + 2 + 18. That is the reading
  DECISION F104 D1 fixes; `git commit`'s terminal summary applies rename detection and
  may print a different pair. If your measurement differs from 22, report the number you
  measured and say so — do not adjust the payloads to reach it.

C2 — migrate the `memory` group
  `git apply .remedy-wt/f277-r11-payloads/s1-memory.diff`, then
  `git add tests/cli/test_memory_cmd.py` (new file, see PAYLOADS).
  Touches `apps/cli/commands/memory.py` and creates `tests/cli/test_memory_cmd.py`.
  `import sys` goes from `memory.py`: unlike `mission_cmd.py` in round 10, every
  `file=sys.stderr` in this module was a refusal and all nine are migrated, so the import
  has no remaining user and `ruff` says so.
  Subject: `F277 R11 C2: migrate the memory group onto the shared fail helper`
  Expected insertions: 143.

C3 — the handback
  Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`, then
  `git push -u origin feature/f277-machine-contracts`.
  Subject: `F277 R11 C3: rewrite handoff for round 11`

CONSTRAINTS
1. Never edit a payload and never retype one. The `.diff` goes on with `git apply`; run
   `git apply --check` first and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. Do not touch any file this block does not name. In particular: no other group, no
   catalog change, no `apps/cli/commands/runtime_cmd.py`, no `.agent/decisions.md`, and
   no edit to `docs/roadmap/features/T2_F277.md`.
4. If a gate goes red, STOP. Do not repair the reviewer's slice and do not guess which
   half of a disagreement is wrong. Commit and push what is verified, write an honest
   handoff under AGENTS.md "If Blocked", and hand back. Round 8 did exactly that.
5. `.agent/plan.md` must read 49 lines after C1b — under the 50-line rule, but only just.

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4).

G1 TRANSPORT AND STATE
 (a) For each of the four payload files, report the line count and sha256 you measured
     against the PAYLOADS table above. Four readings, all equal.
 (b) For each of the three `.agent/authored/f277-r11-*` copies at C1a, compare it
     byte-for-byte with its source under `.remedy-wt/f277-r11-payloads/` (the block copy
     against `.remedy-wt/f277-r11-block.md`). Four readings, all True.
 (c) The two appends at C1b. For each of `.agent/live_review.md` and
     `.agent/prose_slips.md`: the file's bytes at `e90faf51` plus the payload's bytes
     equal the file's bytes at C1b. Report pre, payload, post and post-minus-pre for
     each. Two readings, both True. Then ONE negative control, on `.agent/live_review.md`
     only: flip a single bit inside the appended region and show the reading returns
     False.
 (d) `.agent/plan.md` at C1b equals `plan.md` byte-for-byte, at 49 lines. Report both
     sha256s and the line count.
 (e) The open set by distinct id in `.agent/live_review.md` — ids matching
     `^- R-\d+ — ` minus ids matching `^Done: R-\d+ — ` — is 20 at `e90faf51` and 20 at
     C1b. Report both numbers, not a claim that they match.
 (f) `git diff --name-only e90faf51 <C1b>` must NOT name `.agent/decisions.md`. Report
     the list.

G2 CODE TRANSPORT
 At C2, run `git rev-parse` over exactly this path list and compare each blob id with
 this table. The table was printed by a single `git hash-object` call over this same
 list in the reviewer's dry run, from the tree the reviewer tested and red-proved —
 never typed by hand (finding R-1014).

 | path | blob id at C2 |
 |---|---|
 | apps/cli/commands/memory.py | d973107be1cd64dfea3b9c4d0c5bcb6a93d45acf |
 | tests/cli/test_memory_cmd.py | 67d4d3b4d9f50f1ac868485976091d7db93631f4 |

 Then `git diff --name-only <C1b> <C2>` must name exactly those two paths and no third.
 Report the list and its length. If `tests/cli/test_memory_cmd.py` is missing from that
 list, you forgot the `git add` the PAYLOADS section names — that is the failure mode
 this gate is shaped to catch.

G3 THE TARGETED SUITE — in the primary checkout, at C2:
```
python3 -m pytest -q -p no:cacheprovider tests/cli/test_memory_cmd.py \
  tests/test_data_paths.py tests/test_grouped_cli.py tests/test_command_catalog.py \
  tests/cli/test_command_catalog.py tests/orchestration/test_import_reachability.py \
  tests/test_no_orphan_modules.py tests/cli/test_golden_path.py tests/docs
```
 The selection is every test file that names `commands.memory` or a `_cmd_memory`
 handler, plus the catalog, reachability and golden-path guards. The reviewer's dry run
 read `806 passed` at exit 0. Report the summary line and the exit code. Do not run the
 full suite — amend0917 rule 1 reserves it for the closure round.

G4 LINT — `python3 -m ruff check apps/cli/commands/memory.py
 tests/cli/test_memory_cmd.py`. Report the output and the exit code.

G5 MUTATION RED-PROOFS — in a DISPOSABLE worktree only (guardrail G5):
 `git worktree add --detach .remedy-wt/f277-r11-g5 <C2>`, removed as this gate's last
 action with `git worktree remove`, then report `git worktree list`.
 In that worktree run, serially, for each mutation:
 `python3 -B -m pytest -q -p no:cacheprovider tests/cli/test_memory_cmd.py`.
 Run the UNMUTATED CONTROL FIRST and report it; the reviewer read `13 passed`, exit 0.
 For each mutation: COUNT the occurrences of the anchor text in the named file and report
 the count against the count this block states for it — mutation (a) is the one place in
 this feature where the expected count is FIVE and not one, because the five identical
 refusals are the property under test. Apply it, run, report the summary line, the exit
 code and every FAILED node id, then restore the file byte-identically and confirm before
 the next mutation. A mutation that stays GREEN is a finding: stop and report.

 All five mutations are in `apps/cli/commands/memory.py`.

 (a) ANCHOR COUNT 5. Replace every occurrence of
     `fail("memory_card_not_found", f"memory card not found: {memory_id}",`
     with `fail("card_missing", f"memory card not found: {memory_id}",`.
     Expected: 5 failed, 8 passed — the four parameter cases of
     `test_under_json_it_is_an_envelope_on_stdout` and
     `test_contradict_threads_the_flag_through_its_two_ids`.
 (b) ANCHOR COUNT 1. In the two-line `fail(...)` call inside
     `_cmd_memory_card_supersede`, change the message
     `f"old memory card not found: {old_id}"` to
     `f"memory card not found: {old_id}"` — dropping the one word that says WHICH of its
     two ids was missing.
     Expected: 1 failed, 12 passed —
     `test_supersede_names_the_OLD_card_and_keeps_its_own_wording`.
 (c) ANCHOR COUNT 1. In the two-line `fail("invalid_job_id", ...)` call, change
     `json_output=json_output` to `json_output=False`.
     Expected: 1 failed, 12 passed — `test_an_unknown_job_is_an_envelope_under_json`.
 (d) ANCHOR COUNT 1. Insert the line `    json_output = False` directly above
     `    from packages.memory.local_gateway import approve_memory_card`, which severs
     the flag this round threaded into `_cmd_memory_card_approve`.
     Expected: 1 failed, 12 passed —
     `test_under_json_it_is_an_envelope_on_stdout[_cmd_memory_card_approve-approve_memory_card-None]`.
 (e) ANCHOR COUNT 1. The same severing above
     `    from packages.memory.local_gateway import contradict_memory_card`.
     Expected: 1 failed, 12 passed —
     `test_contradict_threads_the_flag_through_its_two_ids`.

G6 PUSH AND TREE — after C3: `git push -u origin feature/f277-machine-contracts` and
 report its outcome, then `git status --porcelain` (must be empty) and `git worktree
 list` (must show the primary checkout and the two pre-existing `remedy/job-*` worktrees
 and nothing else).

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: the state block, the per-commit
changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the item-status table, the deviations,
and the next expected action. Report what you ran, not what you expected to find.

ONE MORE THING, AND IT IS THIS SESSION'S LAST ROUND. Your handback is the only carrier
between this session and the next. Make its `## Next` section explicit: Phase 1 rule 1
(read `.agent/STOP` from disk) first, then the review of round 11, then T003's remaining
modules in the order `.agent/plan.md` lists them. State the open-findings count and the
operator-questions count, which are 20 and 1.
