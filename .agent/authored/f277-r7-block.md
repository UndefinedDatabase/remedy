STEP R7 T003 (part 1) — F277 Machine contracts: the shared `fail()` and the first two groups

GOAL
Book round 6's PASS, then open T003. `apps/cli/json_envelope.py` gains `fail(error,
message, *, json_output, exit_code=1, **payload)` — the helper that replaces the
`print(f"Error: ...", file=sys.stderr)` / `sys.exit(1)` pair this CLI has written out
by hand at 237 sites — and the first two command groups are migrated onto it: `event`
and `file`, chosen because their handlers already thread `json_output` end to end, so
the migration is the pairs themselves and nothing else. DECISION F277 D7 fixes the
helper's parameter spellings against the feature file's `fail(code, message, ...)`,
which names two different things with one word, and re-measures T003's planning
numbers, all of which predate F261's deletions.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it,
run the self-review loop before every commit, keep `.agent/plan.md` current, keep the
tree clean, push at the end, rewrite `.agent/handoff.md`. You never issue a verdict —
the reviewer does that from the committed diff and its own re-runs.

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git -C . status --porcelain` must be empty and `git branch --show-current` must
   read `feature/f277-machine-contracts` at `62b40261`. Report all three.
3. Verify this block's own bytes before you use it (R-0954): measure the line count
   and sha256 of `.remedy-wt/f277-r7-payloads/block.md` and compare both with the two
   readings your delegation message states for it. Report both numbers you measured
   beside both you were given. If either differs, stop and say so — do not proceed on
   a block you cannot verify. (The readings live in the delegation message and not in
   this file, because a file cannot carry its own digest.)

PAYLOADS
All payloads live under `.remedy-wt/f277-r7-payloads/`, which is gitignored. Verify
each one's line count and sha256 BEFORE using it and report every reading (amend0917
rule 4: the transport proof is one digest per file). Never retype a payload; never
edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 2 | 5057 | 570af581a6bd835d7b1306c0cf721c57fb70a5f8804e95f214d38203b1bd2fb1 |
| decisions.md | 53 | 4208 | 758b9801ca2408bddf97bfc5b7098a13281e1a4f25dc9adc5905d2e2395a35ae |
| plan.md | 49 | 2641 | 1f3d19f47a7f97036cb96b7d82f428f43881e32f3aaa1ddf88934353f5f0e88d |
| slips.md | 1 | 1050 | 9c516f045ec2b356fd977f31d29050f43916d6b8dbe1cf9f8bf7ec0c8640f851 |
| s1-envelope.diff | 67 | 2890 | af5cbb951e218596f282f0839752e65be5847046436f27bccddfb4392cec31c0 |
| s2-envelope-tests.diff | 66 | 2799 | 08460e8438819b0f623890941e194db3a0e1e8ad192e0004cf0ae47b897b5fbf |
| s3-event-group.diff | 142 | 5715 | bf96d71ba91178df814c3d32b05f414f2feac6a916b2f72a97a16847b4131a83 |
| s4-file-group.diff | 66 | 2667 | 1d5550094824ba0efef8f04c8c2b802bfbef59c55a4e994180c9c0a586b539c6 |
| s5-feature-file.diff | 47 | 3551 | 05f132b9f08eb6ff9e3f368f15086878de8fd840b5a0604fe79c2e457f653c13 |

`ledger.md`, `decisions.md` and `slips.md` are APPENDS; `plan.md` is a REWRITE. The
first two begin with a single newline that is the separator between records, exactly
as round 6's did; `slips.md` has no leading newline, because `.agent/prose_slips.md`
holds one line per entry with no blank line between them. The five `.diff` files are
applied with `git apply`, never retyped.

BUNDLE — SEVEN COMMITS, in this order

C1a — copy the four state payloads into `.agent/authored/`
  `.agent/authored/f277-r7-block.md`      := this block, byte-for-byte
  `.agent/authored/f277-r7-ledger.md`     := ledger.md
  `.agent/authored/f277-r7-decisions.md`  := decisions.md
  `.agent/authored/f277-r7-plan.md`       := plan.md
  `.agent/authored/f277-r7-slips.md`      := slips.md
  Subject: `F277 R7 C1a: copy round 7 payloads into .agent/authored/`
  Expected insertions: the block's own line count plus 105. Report what you measure;
  the block's count moves with every edit to the block itself, so no fixed number is
  stated for this commit. It is well under 500 either way.

C1b — book round 6's PASS, record DECISION F277 D7, the slip, and rewrite the plan
  `.agent/live_review.md`  += ledger.md          (append, +2)
  `.agent/decisions.md`    += decisions.md       (append, +53)
  `.agent/prose_slips.md`  += slips.md           (append, +1)
  `.agent/plan.md`         := plan.md            (rewrite, +23/-19)
  Subject: `F277 R7 C1b: book round 6's PASS, record DECISION F277 D7, rewrite plan`
  EXPECTED INSERTIONS: 79 by `git show --numstat` — 2 + 53 + 1 + 23. That is the
  reading DECISION F104 D1 fixes; `git commit`'s own terminal summary applies rename
  detection and may print a different pair. If your measurement differs from 79,
  report the number you measured and say so — do not adjust the payloads to reach it.

C2 — the shared `fail()`
  `git apply .remedy-wt/f277-r7-payloads/s1-envelope.diff`
  Touches `apps/cli/json_envelope.py` only.
  Subject: `F277 R7 C2: add the shared fail helper to the JSON envelope`
  Expected insertions: 37.

C3 — the helper's tests
  `git apply .remedy-wt/f277-r7-payloads/s2-envelope-tests.diff`
  Touches `tests/cli/test_json_envelope.py` only.
  Subject: `F277 R7 C3: test the shared fail helper in both shapes`
  Expected insertions: 51.

C4 — migrate the `event` group
  `git apply .remedy-wt/f277-r7-payloads/s3-event-group.diff`
  Touches `apps/cli/commands/event.py`, `tests/cli/test_event_list_cmd.py` and
  `tests/orchestration/import_reachability_allowlist.txt`. The allowlist line is in
  this commit and not in C2 on purpose: `event.py` importing the envelope at module
  level is what first makes `apps.cli.json_envelope` reachable from the D11 (c) entry
  points, so the allowlist entry and the import that earns it land together.
  Subject: `F277 R7 C4: migrate the event group onto the shared fail helper`
  Expected insertions: 42.

C5 — migrate the `file` group
  `git apply .remedy-wt/f277-r7-payloads/s4-file-group.diff`
  Touches `apps/cli/commands/file.py` and `tests/cli/test_file_provenance_cli.py`.
  Subject: `F277 R7 C5: migrate the file group onto the shared fail helper`
  Expected insertions: 29.

C6 — amend T003 for DECISION F277 D7
  `git apply .remedy-wt/f277-r7-payloads/s5-feature-file.diff`
  Touches `docs/roadmap/features/T2_F277.md` only.
  Subject: `F277 R7 C6: amend T2_F277.md's T003 for DECISION F277 D7`
  Expected insertions: 32.

C7 — the handback
  Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`, then
  `git push -u origin feature/f277-machine-contracts`.
  Subject: `F277 R7 C7: rewrite handoff for round 7`

CONSTRAINTS
1. Never edit a payload and never retype one. Every `.diff` goes on with `git apply`;
   run `git apply --check` first and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. Do not touch any file this block does not name. In particular, do not migrate a
   third group, do not change the catalog, and do not touch `apps/cli/grouped.py`.
4. If a gate goes red, STOP. Do not repair the reviewer's slice, do not guess which
   half of a disagreement is wrong. Commit and push what is verified, write an honest
   handoff recording the stop under AGENTS.md "If Blocked", and hand back. Round 5 of
   this feature did exactly that and it was the right call.
5. `.agent/plan.md` must read 49 lines after C1b — it is under the 50-line rule, but
   only just; do not add to it.

DONE-WHEN — SIX GATES, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4).

G1 TRANSPORT AND STATE
 (a) For each of the nine payload files, report the line count and sha256 you measured
     against the PAYLOADS table above. Nine readings, all equal.
 (b) For each of the four `.agent/authored/f277-r7-*` state copies at C1a, compare it
     byte-for-byte with its source payload under `.remedy-wt/f277-r7-payloads/`, plus
     the block copy against this block. Five readings, all True.
 (c) The three appends at C1b. For each of `.agent/live_review.md`,
     `.agent/decisions.md` and `.agent/prose_slips.md`: the file's bytes at `62b40261`
     plus the payload's bytes equal the file's bytes at C1b. Report pre, payload, post
     and post-minus-pre for each. Three readings, all True. Then ONE negative control,
     on `.agent/live_review.md` only: flip a single bit inside the appended region and
     show the same reading returns False. (amend0917 rule 4 — one digest comparison per
     append, one negative control for the round, not per file.)
 (d) `.agent/plan.md` at C1b equals `plan.md` byte-for-byte. Report both sha256s.
 (e) The open set by distinct id in `.agent/live_review.md` — the ids matching
     `^- R-\d+ — ` minus the ids matching `^Done: R-\d+ — ` — is 20 at `62b40261` and
     20 at C1b. This round registers and resolves nothing, so the two counts are equal;
     report both numbers, not a claim that they match.

G2 CODE TRANSPORT
 At C6, run `git rev-parse` over exactly this path list and compare each blob id with
 this table. The table was printed by a single `git hash-object` call over this same
 list in the reviewer's dry run, from the tree the reviewer tested — it was not typed
 by hand (finding R-1014).

 | path | blob id at C6 |
 |---|---|
 | apps/cli/json_envelope.py | 5a4e1eafa839e35cea9ac9a04e1afda9171f44f8 |
 | tests/cli/test_json_envelope.py | cb5108a96703c1816bec20f3427b9e8c0a9a39fe |
 | apps/cli/commands/event.py | a272e18feba8dc56ba71331a565acfd4fcc958bb |
 | tests/cli/test_event_list_cmd.py | b2e08d141cdb8d4db94d4a2b201cc0fa79888b5f |
 | tests/orchestration/import_reachability_allowlist.txt | c8cf618a07a2f4df00c1bb3d5578203442c0cb5e |
 | apps/cli/commands/file.py | 980ea2ae0e9444f2d3bf66f5bf34adc8475ec952 |
 | tests/cli/test_file_provenance_cli.py | e7d2de221a2f366872655682251ed8d72de51074 |
 | docs/roadmap/features/T2_F277.md | ed63a980b27d875ecc67e99b2613d6e97db775ac |

 Then `git diff --name-only <C1b> <C6>` must name exactly those eight paths and no
 ninth. Report the list and its length.

G3 THE TARGETED SUITE — in the primary checkout, at C6:
```
python3 -m pytest -q -p no:cacheprovider tests/cli/test_json_envelope.py \
  tests/cli/test_event_list_cmd.py tests/cli/test_file_provenance_cli.py \
  tests/cli/test_change_proof_cli.py tests/cli/test_product_spine.py \
  tests/test_brain_viewer.py tests/test_context_coverage.py tests/test_data_paths.py \
  tests/test_grouped_cli.py tests/test_command_catalog.py \
  tests/cli/test_command_catalog.py tests/test_no_orphan_modules.py \
  tests/orchestration/test_import_reachability.py tests/cli/test_golden_path.py \
  tests/docs
```
 The reviewer's dry run read `1100 passed` at exit 0. Report the summary line and the
 exit code. Do not run the full suite — amend0917 rule 1 reserves it for the closure
 round.

G4 LINT — `python3 -m ruff check apps/cli/json_envelope.py apps/cli/commands/event.py
 apps/cli/commands/file.py tests/cli/test_json_envelope.py
 tests/cli/test_event_list_cmd.py tests/cli/test_file_provenance_cli.py`. Report the
 output and the exit code.

G5 MUTATION RED-PROOFS — in a DISPOSABLE worktree only (guardrail G5):
 `git worktree add --detach .remedy-wt/f277-r7-g5 <C6>`, and remove it as this gate's
 last action with `git worktree remove`, then report `git worktree list`.
 In that worktree run, serially, for each mutation:
 `python3 -B -m pytest -q -p no:cacheprovider tests/cli/test_json_envelope.py
 tests/cli/test_event_list_cmd.py tests/cli/test_file_provenance_cli.py`.
 Run the UNMUTATED CONTROL FIRST and report it; the reviewer read `34 passed`, exit 0.
 For each mutation: COUNT the occurrences of the anchor text in the named file and
 report the count, which must be 1 — that uniqueness is what makes the revert safe.
 Apply it, run, report the summary line, the exit code and every FAILED node id, then
 restore the file byte-identically and confirm by sha256 against the committed blob
 before the next mutation. A mutation that stays GREEN is a finding: stop and report.

 (a) `apps/cli/json_envelope.py`: replace
     `        print(f"Error: {message}", file=sys.stderr)`
     with `        print(f"Error: {message}")`.
     Expected: 3 failed, 31 passed — `test_without_json_it_is_the_line_this_cli_already_printed`,
     `test_without_json_the_same_refusal_is_the_line_it_always_was`,
     `test_without_json_it_is_the_line_it_always_was`.
 (b) `apps/cli/json_envelope.py`: replace `    sys.exit(exit_code)` with
     `    sys.exit(1)`.
     Expected: 1 failed, 33 passed — `test_the_exit_code_is_the_callers_and_defaults_to_one`.
 (c) `apps/cli/json_envelope.py`: replace the two lines
     `    if json_output:` / `        emit_error(error, message, **payload)`
     with `    if False:` / `        emit_error(error, message, **payload)`.
     Expected: 6 failed, 28 passed, including `test_under_json_it_is_the_envelope_and_nothing_else`,
     `test_an_unknown_job_is_an_envelope_under_json` and
     `test_under_json_it_is_an_envelope_on_stdout`.
 (d) `apps/cli/commands/event.py`: replace
     `    _job, events, jid = _load_job_events(job_id_str, json_output=json_output)`
     with `    _job, events, jid = _load_job_events(job_id_str)` — the FIRST of the two
     occurrences, the one followed by the comment line `    # Every row`; match on both
     lines together so the anchor is unique.
     Expected: 1 failed, 33 passed — `test_an_unknown_job_is_an_envelope_under_json`.
 (e) `apps/cli/commands/event.py`: replace
     `fail("invalid_list_option", str(exc), json_output=json_output)` with
     `fail("bad_sort", str(exc), json_output=json_output)`.
     Expected: 1 failed, 33 passed — `test_an_unknown_sort_field_exits_nonzero_naming_the_valid_set`.
 (f) `apps/cli/commands/file.py`: in the two-line call
     `        fail("invalid_job_id", f"No job matches {job_id_str!r}. Try: remedy job list.",`
     `             json_output=json_output)`, replace `json_output=json_output` with
     `json_output=False`. Match on both lines together so the anchor is unique.
     Expected: 1 failed, 33 passed — `test_under_json_it_is_an_envelope_on_stdout`.

G6 PUSH AND TREE — after C7: `git push -u origin feature/f277-machine-contracts` and
 report its outcome, then `git status --porcelain` (must be empty) and `git worktree
 list` (must show the primary checkout and the two pre-existing `remedy/job-*`
 worktrees and nothing else).

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: the state block, the per-commit
changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the item-status table, the
deviations, and the next expected action. If you deviated anywhere, say where and why
— a declared deviation costs nothing and an undeclared one costs a round. Report what
you ran, not what you expected to find: a gate reported green without its output is
worth less than a gate reported red with it.
