STEP T002/1 - F262 List commands v2, ROUND 3
FEATURE F262 - List commands v2 (Tier 2) - SESSION 1, ROUND 3

Goal
  Ship the first, lowest-risk batch of T002 (dates on every row): four
  list commands whose underlying model ALREADY records created_at (and
  a second lifecycle timestamp) and whose --json output already
  surfaces it - only the TEXT output is missing it. No model or store
  changes this round, no --json changes, no behavior change beyond the
  printed line: blocker.list, decision.list, approval.policy-list,
  self-repair.proposal-list. This is batch 1 of an audited, multi-round
  T002 worklist (see PLAN4's Next Steps for the remaining batches).

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f262-r3.md
  C0b mirror it to .agent/last_block.md
  C1  append GATE2 to .agent/live_review.md - books round 2's PASS
      verdict (the reviewer's own, independently re-verified)
  C2  apply the four CODE PAIRS below (one commit, four files) and add
      the two new test files per the TEST SPEC below (same commit -
      code and its coverage land together)
  C3  apply PLAN4 to .agent/plan.md
  C4  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f262-r3.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md (C1) - apps/cli/commands/blocker.py (C2) -
  apps/cli/commands/decision.py (C2) -
  apps/cli/commands/worker_facade_cmd.py (C2) -
  apps/cli/commands/self_repair_cmd.py (C2) -
  tests/cli/test_blocker_cmd.py (new, C2) -
  tests/cli/test_decision_cmd.py (new, C2) - .agent/plan.md (C3) -
  .agent/handoff.md (C4)

CODE PAIRS for C2 - four independent FROM/TO replacements, each
mechanically confirmed by the reviewer to occur EXACTLY ONCE in its file
before this round and to be a REWRITE (TO does not contain FROM
verbatim). Apply each with str.replace(FROM, TO, 1) via a script, never
by hand-retyping - these are short enough to be applied exactly, unlike
the CODE SPEC style of round 2.

  PAIR B (apps/cli/commands/blocker.py)
  <<<BEGIN PAIR_B_FROM>>>
            print(f"  {s.reason_code} {status_mark}  {s.safe_summary}  (id={s.id[:8]})")
<<<END PAIR_B_FROM>>>
  <<<BEGIN PAIR_B_TO>>>
            resolved_str = f", resolved={s.resolved_at}" if s.resolved_at else ""
            print(f"  {s.reason_code} {status_mark}  {s.safe_summary}  (id={s.id[:8]}, created={s.created_at}{resolved_str})")
<<<END PAIR_B_TO>>>

  PAIR D (apps/cli/commands/decision.py)
  <<<BEGIN PAIR_D_FROM>>>
            print(f"  {d.type} {status_mark} ({d.severity}): {d.safe_summary}  (id={d.id})")
<<<END PAIR_D_FROM>>>
  <<<BEGIN PAIR_D_TO>>>
            resolved_str = f", resolved={d.resolved_at}" if d.resolved_at else ""
            print(f"  {d.type} {status_mark} ({d.severity}): {d.safe_summary}  (id={d.id}, created={d.created_at}{resolved_str})")
<<<END PAIR_D_TO>>>

  PAIR P (apps/cli/commands/worker_facade_cmd.py)
  <<<BEGIN PAIR_P_FROM>>>
        print(f"  [{status}] {p.get('policy_id', '?')}: {p.get('label', '')}")
<<<END PAIR_P_FROM>>>
  <<<BEGIN PAIR_P_TO>>>
        print(f"  [{status}] {p.get('policy_id', '?')}: {p.get('label', '')}"
              f"  (created={p.get('created_at', '')}, updated={p.get('updated_at', '')})")
<<<END PAIR_P_TO>>>

  PAIR S (apps/cli/commands/self_repair_cmd.py)
  <<<BEGIN PAIR_S_FROM>>>
        print(f"  {p.get('proposal_id', '?'):20s}  {p.get('status', '?'):25s}  {p.get('title', '')[:50]}")
<<<END PAIR_S_FROM>>>
  <<<BEGIN PAIR_S_TO>>>
        print(f"  {p.get('proposal_id', '?'):20s}  {p.get('status', '?'):25s}  {p.get('title', '')[:50]}"
              f"  (created={p.get('created_at', '')}, updated={p.get('updated_at', '')})")
<<<END PAIR_S_TO>>>

  Every FROM above was confirmed by the reviewer to occur exactly once
  in its file at this round's base (7c65d9cc..c324929e range, current
  HEAD) via a Python `text.count(FROM)` check, and every pair's
  containment was mechanically tested (`FROM in TO`) and is False for
  all four - REWRITE, not APPEND, for all four.

TEST SPEC for C2 - two new files, following the exact mocking pattern
already used by tests/cli/test_worker_facade_cmd.py's
TestApprovalPolicyList (patch the list function at its OWN module's
dotted path, since the handler imports it locally at call time; capture
stdout via the `capsys` fixture; assert substrings, never exact full
lines).

  tests/cli/test_blocker_cmd.py - a module docstring crediting F262 T002,
  a helper `_stop(*, status="active", resolved_at=None)` returning a
  `packages.orchestration.stop_reasons.StopReason` with
  `id="stop-1"`, `job_id="job-1"`, `source="test"`,
  `reason_code="dirty_repo"`, `severity="warning"`, the given `status`,
  `created_at="2026-09-01T00:00:00+00:00"`, the given `resolved_at`,
  `related_node_id=""`, `related_intent_id=""`, `related_file=""`,
  `safe_summary="a blocker"`, `next_actions=()`. Patch target constant
  `_LIST_STOPS = "packages.orchestration.stop_reasons.list_stop_reasons"`.
  Two tests in a `TestBlockerListText` class:
    - `test_shows_created`: mock returns `[_stop()]`, call
      `apps.cli.commands.blocker._cmd_blocker_list("job-1",
      json_output=False)`, assert
      `"created=2026-09-01T00:00:00+00:00"` in stdout and `"resolved="`
      NOT in stdout (unresolved case shows no resolved fragment).
    - `test_shows_resolved_when_present`: mock returns
      `[_stop(status="resolved",
      resolved_at="2026-09-02T00:00:00+00:00")]`, same call, assert BOTH
      `"created=2026-09-01T00:00:00+00:00"` and
      `"resolved=2026-09-02T00:00:00+00:00"` in stdout.

  tests/cli/test_decision_cmd.py - a module docstring crediting F262
  T002, a helper `_decision(*, status="open", resolved_at=None)`
  returning a `packages.orchestration.decision_queue.HumanDecision` with
  `id="dec-1"`, `type="task_decision"`, the given `status`,
  `severity="blocker"`, `source="test"`, `related_node_id=""`,
  `related_intent_id=""`, `related_file=""`, `safe_summary="a decision"`,
  `next_actions=()`, `created_at="2026-09-01T00:00:00+00:00"`, the given
  `resolved_at`. Patch targets: `_LOAD_JOB_EVENTS =
  "apps.cli.commands.decision._load_job_events"` (mocked to return
  `(None, [], "job-1")`) and `_LIST_DECISIONS =
  "packages.orchestration.decision_queue.list_decisions"`. Two tests in
  a `TestDecisionListText` class, both patching BOTH targets:
    - `test_shows_created`: `list_decisions` mock returns
      `[_decision()]`, call
      `apps.cli.commands.decision._cmd_decision_list("job-1",
      json_output=False)`, assert
      `"created=2026-09-01T00:00:00+00:00"` in stdout and `"resolved="`
      NOT in stdout.
    - `test_shows_resolved_when_present`: mock returns
      `[_decision(status="resolved",
      resolved_at="2026-09-02T00:00:00+00:00")]`, same call, assert BOTH
      timestamps present in stdout.

Constraints
  1. C1's append to .agent/live_review.md is applied BYTE FOR BYTE:
     extract GATE2 from the COMMITTED .agent/authored/f262-r3.md by its
     BEGIN/END markers (excluded) and apply with a script, never by
     retyping. GATE2 carries ZERO internal newlines and NO trailing
     newline of its own. The base file (measured by the reviewer before
     this round) is 2417095 bytes with NO trailing newline; the applied
     file must equal base + one newline byte + GATE2's own bytes,
     exactly 2421305 bytes total. Report the arithmetic and a `cmp`
     against a script-extracted copy of GATE2, both directions.
  2. The four CODE PAIRS are extracted from the COMMITTED
     .agent/authored/f262-r3.md by marker index and applied with
     str.replace(FROM, TO, 1) via a script, never by hand-retyping.
     Report, per pair: FROM count in its file immediately before this
     round (must be 1), FROM count after (must be 0), TO count after
     (must be 1).
  3. The two new test files are written by hand from the TEST SPEC
     above (not extracted from a marker slice) - ordinary careful
     engineering matching the existing test file's style
     (tests/cli/test_worker_facade_cmd.py's TestApprovalPolicyList is
     the model to follow for structure and patching idiom).
  4. `python3 -m py_compile` on all six touched/added .py files must
     exit 0 (ruff is denied this session - attempt it anyway and report
     the exact refusal or the real result, never assume).
  5. C2 is ONE commit covering all six files (four production files, two
     new test files) - the printer changes and their coverage land
     together.
  6. PLAN4 REPLACES .agent/plan.md whole-file, ending WITHOUT a trailing
     newline, same as every prior round.
  7. The reviewer confirmed before authoring this block, by reading the
     actual test suite, that NO existing test asserts an exact full
     line of text output for any of these four commands' list view
     (only loose substring checks exist for approval.policy-list and
     self-repair.proposal-list, and no dedicated CLI test exists at all
     yet for blocker.list or decision.list) - so this round's additive
     text is not expected to break any pre-existing assertion, and the
     two new test files are original coverage, not a repair of broken
     ones.
  8. A sentence OUTSIDE the change set that this round makes stale is
     DECLARED in the handback and NOT repaired.
  9. Read .agent/STOP from disk before the first commit and again
     before C4. If it exists, finish the commit in hand, write the
     handback, and stop.
  10. Self-review loop before every commit (git diff --stat, git diff).
      Push after C4 (git push origin feature/f262-list-commands-v2). No
      pull request, no merge.
  11. `git rev-parse HEAD` before C0a must read
      `c324929e8f0b97b34de30c6e4eb42bbca3357b61` (report the full SHA);
      `git branch --show-current` must read
      `feature/f262-list-commands-v2`.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f262-r3.md .agent/last_block.md
     One digest, twice. Report both lines verbatim.
  G2 THE LEDGER APPEND, FULL FORENSICS. Report:
       base size immediately before C1 (bytes, trailing-newline byte)
       GATE2 own byte length and internal-newline count
       base + 1 + GATE2_length, compared against the post-C1 file's real
         byte length - state match True/False
       tail slice (last GATE2_length bytes of the post-C1 file) compared
         against GATE2 - state equal True/False
       negative control: flip the first byte of a COPY of GATE2, confirm
         the flipped copy does NOT match the real tail - state
         rejected True/False
  G3 THE FOUR PAIRS, READ AND COUNTED. For each of PAIR B, PAIR D, PAIR
     P, PAIR S: FROM count before (1), FROM count after (0), TO count
     after (1), and report the containment check `FROM in TO` (must be
     False for all four, confirming REWRITE). Then read the full diff
     of all four production files and confirm nothing beyond the named
     pair changed in each. `python3 -m py_compile` on all six touched or
     added `.py` files, reported individually, each exit 0.
  G4 THE TESTS, BEFORE AND AFTER. Report
     `python3 -m pytest tests/cli/test_worker_facade_cmd.py -q` and
     `python3 -m pytest tests/cli/test_self_repair_cmd.py -q` BOTH
     before C2 (base counts, both fully green - these must NOT go red)
     and after C2 (same counts, still fully green - the printer change
     is additive and these are pre-existing suites, not new ones).
     Then, only after C2 (they do not exist before it):
     `python3 -m pytest tests/cli/test_blocker_cmd.py -q` and
     `python3 -m pytest tests/cli/test_decision_cmd.py -q`, both 2
     passed.
  G5 THE STATE READERS AND THE CANARY (this round rewrites `.agent/`
     state - live_review.md, plan.md, handoff.md):
       python3 -m pytest tests/ui_server/ -q
       python3 -m pytest tests/orchestration/test_test_runner.py -q
       python3 -m pytest tests/regression/test_resource_safety.py -q
       python3 -m pytest tests/orchestration/test_integrity_gate.py -q
       python3 -m pytest tests/cli/test_golden_path.py -q
     Report each pass count; a moved count against this session's own
     prior readings (515/52/21/16/42) is itself a finding, since this
     round's change set names no path any of these five suites should
     be sensitive to.
  G6 THE PLAN. Extract PLAN4 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md            -> exit 0
       wc -l .agent/plan.md                      -> report; must be under 50
       grep -c '^## Goal' .agent/plan.md         -> 1
       grep -c '^## Next Steps' .agent/plan.md   -> 1
  G7 THE TREE, THE COMMITS AND THE SWEEP. `git status --porcelain`
     immediately before C4 is staged -> empty. `git ls-files
     .remedy-wt` -> no output. For C0a, C0b, C1, C2 and C3 (every commit
     before the handback), report each one's insertion count from
     `git show --numstat`, the '+' column only, compared cell by cell
     against the handback's Commits table. Then the staleness sweep,
     one line per file this round touched.

Handback
  Rewrite .agent/handoff.md per docs/agents/handback_template.md. SESSION
  1, ROUND 3 of F262. Item-status table with every ordered item (C0a
  through C4, G1 through G7) exactly once, Commits table, one line per
  gate followed by its real transcript, Deviations (apply anything that
  looks wrong exactly as specified and declare it - never silently
  correct the block), Next (round 4 continues T002's remaining
  batches, per PLAN4's Next Steps).

SLICES. Each slice lies between its own one-line BEGIN and END marker,
markers excluded. The slices carried here are GATE2, PLAN4, and the four
CODE PAIRS already delimited above (PAIR_B_FROM/TO, PAIR_D_FROM/TO,
PAIR_P_FROM/TO, PAIR_S_FROM/TO).

<<<BEGIN GATE2>>>
Gate: R2 — the F262 R2 entry. R2 SHIPPED T001, THE SHARED LISTING-OPTION SURFACE, AND THE REVIEWER RE-RAN EVERY GATE ITSELF rather than reading the handback back. TRANSPORT HELD: `.agent/authored/f262-r2.md`/`.agent/last_block.md` share one sha256 digest over 301 lines. THE LEDGER APPEND (booking R1) IS PROVEN IN FULL, NOT JUST ASSERTED: base immediately before C1 was 2414126 bytes with no trailing newline, GATE1 measured at 2968 bytes with 0 internal newlines, base plus one newline plus GATE1 equals 2417095 against an actual post-C1 size of 2417095 — match True; the tail slice of the post-C1 file equals GATE1 byte for byte — equal True; a negative control flipping GATE1's first byte was correctly rejected against the real tail — rejected True. THE CODE WAS READ, NOT ONLY GATED: `apps/cli/command_catalog.py`'s diff is exactly the import-line edit, the `CATALOG`→`_BASE_CATALOG` rename on its own binding line, and one inserted section defining `_LIST_SORT_ARG` through `_LIST_LIMIT_ARG`, `_LIST_OPTION_ARGS`, `_is_list_command`, `_with_list_options` and the rebuilt `CATALOG` — nothing inside `_BASE_CATALOG`'s existing entries changed, confirmed by reading the full diff rather than trusting its line count. `tests/test_command_catalog.py` gained exactly the three specified tests and one import, matching the CODE SPEC symbol for symbol. THE CATALOG CHECK IS THE REVIEWER'S OWN: `python3 -c` importing `CATALOG` and `_is_list_command` printed `28` list-shaped commands and an EMPTY missing-flags dict, and `python3 -m py_compile` exited 0 for both changed files, run separately by the reviewer. THE NEW TESTS MOVED BY EXACTLY THREE: `tests/test_command_catalog.py` read 22 passing before C2 and 25 after, reproduced by the reviewer independently. THE MUTATION RED-PROOF RAN TWICE, ONCE BY THE WORKER AND ONCE BY THE REVIEWER, BOTH TIMES INSIDE A DISPOSABLE WORKTREE AND NEVER IN THE PRIMARY CHECKOUT: removing `_LIST_UNTIL_ARG` from `_LIST_OPTION_ARGS` produced `AssertionError: job.list is missing list flags: {'--until'}` in both runs, and reverting the edit inside the same worktree restored a clean pass in both runs; every mutation worktree was removed by its exact path before the next commit. THE FULL SUITE, NOT JUST THE ROUND-SCOPED TESTS, WAS THE GATE — because this round edits a catalog every list command's parser is built from and dozens of unrelated test files import it — and the reviewer's own pre-round baseline of 19601 passed, 23 skipped, 1 warning in 117.31s became 19604 passed, 23 skipped, 1 warning in 121.65s after the round, a difference of exactly the three tests C2 added and nothing else, reproduced by the reviewer as its own independent run. HYGIENE HELD: `git status --porcelain` empty, `git ls-files .remedy-wt` empty, and the five content commits' insertion counts — 301, 260, 2, 62 plus 28 across two files, and 17 — match the handback's Commits table cell for cell, each measured independently via `git show --numstat` on `037a77f4c185be12985b256c03ccd7395de290dc`, `c119c2137aba93ebfa08b81cc67154db16806824`, `66770833739002a96951d21f26e941d3bfa78340`, `55a29fb053d84d169916dc250e8645816b7466db` and `1e5dabe4a4bb39c006e1dba20b4f2ea74ef13d13`. THE PUSH DISCHARGED — `git ls-remote origin refs/heads/feature/f262-list-commands-v2` and the local `git rev-parse HEAD` both read `c324929e8f0b97b34de30c6e4eb42bbca3357b61`, and nothing was created or merged; the branch carries R1 and R2 unmerged. THE FIVE DECLARED DEVIATIONS ARE ALL DECLARED, NOT REPAIRED, AND NONE IS A DEFECT ON DISK: `git worktree list` after cleanup shows nine PRE-EXISTING, unrelated `job-*` worktrees that predate this round and were never touched by it, confirmed by the reviewer as the same nine, none created or removed by this round; the full-suite delta was named explicitly rather than explained away; `docs/roadmap/features/T2_F262.md` line 5's "REGISTRATION ONLY" sentence is now stale since T001 shipped, outside this round's declared change set, correctly declared and left unrepaired; two tooling substitutions (chained Bash one-liners re-expressed singly, `git -C` in place of `cd` for worktree operations) changed no committed byte. THE VERDICT IS PASS.
<<<END GATE2>>>

<<<BEGIN PLAN4>>>
# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 3, session 1 — T002 batch 1: text-output dates for the four
commands whose store already has them and whose --json already shows
them (blocker.list, decision.list, approval.policy-list,
self-repair.proposal-list), plus new coverage for the two that had
none before.

## Next Steps

- Round 4 (T002 batch 2): memory.list (add `updated_at` to its json
  dict, then text); tournament.list and external-builder.submission-list
  (both DROP their timestamp from the json shape today — restore it,
  then add text).
- Round 5 (T002 batch 3): job.list/queue.list/project.list need
  `--json` added before a date can appear there; loop.list/patch.list
  have no timestamp on their own model and need a design decision.
- Round 6+: builder.adapter-list, execution.* (ignore --json entirely,
  pre-existing), worker.list, worker.registry-list, change.list,
  review.list, config.list have NO timestamp concept — most likely
  render "unknown" (Acceptance) rather than invent one. T003 starts
  once date coverage is far enough along to sort by.

## Risks

- The full per-store audit (28 commands) lives in this round's
  handback, not restated here every round.
- Stores with no timestamp concept may render "unknown" permanently —
  that satisfies Acceptance, it is not a gap to close later.
<<<END PLAN4>>>
