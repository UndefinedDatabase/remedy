STEP R10 T003 (part 3) — F277: the mission group, and the two helpers it lends out

GOAL
Book round 9's PASS, then migrate the `mission` group onto the shared `fail()`: twelve
refusal sites, two of which live in `_resolve_project_id` and `_load_mission_or_exit` —
helpers that eight mission commands AND `mission contract` share, so threading them
reaches a second module and that module's call sites are threaded in their own commit.
DECISION F277 D9 rules how a catch-all exception is tokenised: `mission_error`, named for
the layer that refused, because `MissionError` carries a dozen conditions distinguished
only by prose and deriving a token from that prose would be a parser over prose.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep `.agent/plan.md` current, keep the tree
clean, push at the end, rewrite `.agent/handoff.md`. You never issue a verdict — the
reviewer does that from the committed diff and its own re-runs.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f277-r10-payloads/`  READ-ONLY. The reviewer's originals live here and this
      round's transport proof is a comparison against them. Read them; never write here.
  `.remedy-wt/f277-r10-scratch/`   YOURS. Every log, exit-code capture, temporary script
      and note goes here. Both are gitignored.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty and `git branch --show-current` must read
   `feature/f277-machine-contracts` at `33d1c9df`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f277-r10-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.

PAYLOADS — all five under `.remedy-wt/f277-r10-payloads/`
Verify each one's line count and sha256 BEFORE using it and report every reading. Never
retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 2 | 4287 | a90429dc6357086fbb851bdc6761b1b666cb7e2c7234bb9633fb0a6a62f09917 |
| decisions.md | 52 | 3870 | f0b40d1812d8a60213a9d7605abbdd44fd7311c7405ed88509c350757d3c8c1c |
| plan.md | 49 | 2710 | 116c0ee356cb5d8b267cf496779b249b8611fed876cdc7fbd8e3205167ca44ab |
| s1-mission.diff | 304 | 13346 | a5350096ddc09e61fa34633520656229e55947459a71199cc8b4af10b8e5c35d |
| s2-contract.diff | 52 | 2491 | 10431783212ebdca53b7676ab8336456248e44c9f06eddd1fdd95597c382ab45 |

`ledger.md` and `decisions.md` are APPENDS and each begins with a single newline that is
the record separator. `plan.md` is a REWRITE. There is NO slips payload this round;
`.agent/prose_slips.md` is not touched. The two `.diff` files go on with `git apply`.

BUNDLE — SIX COMMITS, in this order

C1a — copy the three state payloads into `.agent/authored/`
  `.agent/authored/f277-r10-block.md`     := this block, byte-for-byte
  `.agent/authored/f277-r10-ledger.md`    := ledger.md
  `.agent/authored/f277-r10-decisions.md` := decisions.md
  `.agent/authored/f277-r10-plan.md`      := plan.md
  Subject: `F277 R10 C1a: copy round 10 payloads into .agent/authored/`
  Expected insertions: this block's own line count plus 103. No fixed number is stated,
  because the block's count moves with every edit to the block itself. Report what you
  measure; it is far under 500 either way.

C1b — book round 9's PASS, record DECISION F277 D9, rewrite the plan
  `.agent/live_review.md` += ledger.md     (append, +2)
  `.agent/decisions.md`   += decisions.md  (append, +52)
  `.agent/plan.md`        := plan.md       (rewrite, +29/-29)
  Subject: `F277 R10 C1b: book round 9's PASS, record DECISION F277 D9, rewrite plan`
  EXPECTED INSERTIONS: 83 by `git show --numstat` — 2 + 52 + 29. That is the reading
  DECISION F104 D1 fixes; `git commit`'s terminal summary applies rename detection and
  may print a different pair. If your measurement differs from 83, report the number you
  measured and say so — do not adjust the payloads to reach it.

C2 — migrate the `mission` group
  `git apply .remedy-wt/f277-r10-payloads/s1-mission.diff`
  Touches `apps/cli/commands/mission_cmd.py` and `tests/cli/test_mission_cmd.py`.
  NOTE, because it is the one module so far where it is true: `import sys` STAYS in
  `mission_cmd.py`. Two `file=sys.stderr` writes there are NOTES and not refusals — a
  skipped-unreadable-records line and a contract warning — so neither is a
  `print(); sys.exit()` pair and neither migrates. Do not "tidy" the import away.
  Subject: `F277 R10 C2: migrate the mission group onto the shared fail helper`
  Expected insertions: 90.

C3 — thread the two shared helpers through `contract_cmd.py`
  `git apply .remedy-wt/f277-r10-payloads/s2-contract.diff`
  Touches `apps/cli/commands/contract_cmd.py` and `tests/cli/test_contract_cmd.py`.
  This is its own commit because it is its own claim: `contract_cmd.py` IMPORTS both
  helpers, and C2 alone leaves its two call sites on the `json_output=False` default, so
  the contract group would keep answering a `--json` refusal in prose. Both new tests
  are the red proof of exactly those two arguments.
  Subject: `F277 R10 C3: thread the shared mission helpers through the contract group`
  Expected insertions: 31.

C4 — the handback
  Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`, then
  `git push -u origin feature/f277-machine-contracts`.
  Subject: `F277 R10 C4: rewrite handoff for round 10`

CONSTRAINTS
1. Never edit a payload and never retype one. Every `.diff` goes on with `git apply`;
   run `git apply --check` first and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. Do not touch any file this block does not name. In particular: no other group, no
   catalog change, no `apps/cli/commands/runtime_cmd.py`, and no edit to
   `docs/roadmap/features/T2_F277.md` — T003's paragraph was amended in round 7 and D9
   changes nothing it says.
4. If a gate goes red, STOP. Do not repair the reviewer's slice and do not guess which
   half of a disagreement is wrong. Commit and push what is verified, write an honest
   handoff under AGENTS.md "If Blocked", and hand back. Round 8 did exactly that and it
   was the right call.
5. `.agent/plan.md` must read 49 lines after C1b — under the 50-line rule, but only just.

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4).

G1 TRANSPORT AND STATE
 (a) For each of the five payload files, report the line count and sha256 you measured
     against the PAYLOADS table above. Five readings, all equal.
 (b) For each of the four `.agent/authored/f277-r10-*` copies at C1a, compare it
     byte-for-byte with its source under `.remedy-wt/f277-r10-payloads/` (the block copy
     against `.remedy-wt/f277-r10-block.md`). Four readings, all True.
 (c) The two appends at C1b. For each of `.agent/live_review.md` and
     `.agent/decisions.md`: the file's bytes at `33d1c9df` plus the payload's bytes equal
     the file's bytes at C1b. Report pre, payload, post and post-minus-pre for each. Two
     readings, both True. Then ONE negative control, on `.agent/live_review.md` only:
     flip a single bit inside the appended region and show the reading returns False.
 (d) `.agent/plan.md` at C1b equals `plan.md` byte-for-byte, at 49 lines. Report both
     sha256s and the line count.
 (e) The open set by distinct id in `.agent/live_review.md` — ids matching
     `^- R-\d+ — ` minus ids matching `^Done: R-\d+ — ` — is 20 at `33d1c9df` and 20 at
     C1b. This round registers and resolves nothing; report both numbers, not a claim
     that they match.
 (f) `git diff --name-only 33d1c9df <C1b>` must NOT name `.agent/prose_slips.md`. Report
     the list.

G2 CODE TRANSPORT
 At C3, run `git rev-parse` over exactly this path list and compare each blob id with
 this table. The table was printed by a single `git hash-object` call over this same
 list in the reviewer's dry run, from the tree the reviewer tested and red-proved —
 never typed by hand (finding R-1014).

 | path | blob id at C3 |
 |---|---|
 | apps/cli/commands/mission_cmd.py | 7ccec8fc2ffa425f305067c79f81083e8b27daa1 |
 | tests/cli/test_mission_cmd.py | c499f988fde7cae998157890cae4c064abc21f88 |
 | apps/cli/commands/contract_cmd.py | 395c2b05bb33906b46eb154a663833e16786d41c |
 | tests/cli/test_contract_cmd.py | 2eeb2c16eb294eb36e99a73fe8c3d96a7544f57b |

 Then `git diff --name-only <C1b> <C3>` must name exactly those four paths and no fifth.
 Report the list and its length.

G3 THE TARGETED SUITE — in the primary checkout, at C3:
```
python3 -m pytest -q -p no:cacheprovider tests/cli/test_mission_cmd.py \
  tests/cli/test_contract_cmd.py tests/orchestration/test_mission_compiler.py \
  tests/orchestration/test_orchestrator_loop.py \
  tests/orchestration/test_import_reachability.py tests/test_grouped_cli.py \
  tests/test_command_catalog.py tests/cli/test_command_catalog.py \
  tests/test_no_orphan_modules.py tests/cli/test_golden_path.py tests/docs
```
 The selection is every test file that names `mission_cmd` or either shared helper, plus
 the catalog, reachability and golden-path guards. The reviewer's dry run read
 `1194 passed` at exit 0. Report the summary line and the exit code. Do not run the full
 suite — amend0917 rule 1 reserves it for the closure round.

G4 LINT — `python3 -m ruff check` over the four paths of the G2 table. Report the output
 and the exit code.

G5 MUTATION RED-PROOFS — in a DISPOSABLE worktree only (guardrail G5):
 `git worktree add --detach .remedy-wt/f277-r10-g5 <C3>`, removed as this gate's last
 action with `git worktree remove`, then report `git worktree list`.
 In that worktree run, serially, for each mutation:
 `python3 -B -m pytest -q -p no:cacheprovider tests/cli/test_mission_cmd.py
 tests/cli/test_contract_cmd.py`. These tests drive the real CLI in a subprocess, so the
 selection takes about a minute a run and eight runs are expected.
 Run the UNMUTATED CONTROL FIRST and report it; the reviewer read `130 passed`, exit 0.
 For each mutation: COUNT the occurrences of the anchor text in the named file and report
 the count, which must be 1. Apply it, run, report the summary line, the exit code and
 every FAILED node id, then restore the file byte-identically and confirm before the next
 mutation. A mutation that stays GREEN is a finding: stop and report.

 (a) `mission_cmd.py`: in the four-line `fail("no_project", ...)` call, delete
     `, exit_code=EXIT_NO_PROJECT` so the call ends `json_output=json_output)`.
     Expected: 5 failed, 125 passed — `test_starting_without_a_project_exits_three`,
     `test_a_transition_without_a_project_exits_three`,
     `test_under_json_it_is_an_envelope_on_stdout`,
     `test_without_json_it_is_the_two_lines_it_always_was`,
     `test_no_project_is_an_envelope_under_json_and_exits_three`.
 (b) `mission_cmd.py`: in `_load_mission_or_exit`'s `except MissionNotFoundError:` branch,
     change `json_output=json_output` to `json_output=False`.
     Expected: 2 failed, 128 passed — `test_planning_an_unknown_mission_exits_one`,
     `test_an_unknown_mission_is_an_envelope_under_json`.
 (c) `mission_cmd.py`: change the token `"mission_plan_in_progress"` to
     `"plan_in_progress"`.
     Expected: 1 failed, 129 passed — `test_a_recompile_is_refused_once_a_job_is_linked`.
 (d) `mission_cmd.py`: at the `_load_mission_or_exit` call followed by a blank line and
     `    call_fn = None` — which is what makes this anchor unique among six identical
     calls — drop `, json_output=json_output`.
     Expected: 1 failed, 129 passed — `test_planning_an_unknown_mission_exits_one`.
 (e) `contract_cmd.py`: drop `, json_output=json_output` from the
     `_resolve_project_id(project, ...)` call.
     Expected: 1 failed, 129 passed —
     `test_no_project_is_an_envelope_under_json_and_exits_three`.
 (f) `contract_cmd.py`: drop `, json_output=json_output` from the
     `_load_mission_or_exit(project_id, mission_id, ...)` call.
     Expected: 1 failed, 129 passed — `test_an_unknown_mission_is_an_envelope_under_json`.

 (e) and (f) exist because the reviewer's first mutation set omitted them and both lines
 would otherwise have shipped with no test watching them; the two tests that redden them
 were written in response. Do not skip them as duplicates of (a) and (b) — they are the
 SECOND module's call sites and that is the whole point.

G6 PUSH AND TREE — after C4: `git push -u origin feature/f277-machine-contracts` and
 report its outcome, then `git status --porcelain` (must be empty) and `git worktree
 list` (must show the primary checkout and the two pre-existing `remedy/job-*` worktrees
 and nothing else).

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: the state block, the per-commit
changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the item-status table, the deviations,
and the next expected action. Report what you ran, not what you expected to find.
