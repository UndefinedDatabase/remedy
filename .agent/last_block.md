STEP F110 T003 / ROUND 12 - F110 Model routing by task class
FEATURE F110 - Model routing by task class (Tier 3) - SESSION 3, ROUND 12

Goal
  THE PROMOTION-EVIDENCE SCHEMA ROUND. A benchmark run that licenses a cheaper
  tier becomes something a project can WRITE DOWN: config.py learns that a
  table-valued key can declare what its ENTRIES look like, F110 registers
  `model_routing.promotion_evidence` as a table of RECORDS, and model_routing
  gains a PURE parser turning that raw mapping into PromotionEvidence records.
  NOTHING IS WIRED THIS ROUND - no call reads the new key yet, deliberately, so
  the schema lands and is pinned BEFORE routing behaviour moves. Book round 11's
  PASS verdict, resolve R-0787 and R-0788, and record one prose slip.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f110-r12.md
  C0b mirror it to .agent/last_block.md
  C1  apply PLAN12 to .agent/plan.md (FIRST substantive commit, item 23)
  C2  append RECORD11, DONE787 and DONE788 to .agent/live_review.md and
      SLIPS12 to .agent/prose_slips.md
  C3  PRODUCTION: config.py learns typed table entries and registers the key
  C4  PRODUCTION: model_routing.py gains the pure evidence parser
  C5  TESTS: the config surface and the parser
  C6  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f110-r12.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/plan.md (C1) - .agent/live_review.md (C2) -
  .agent/prose_slips.md (C2) -
  packages/orchestration/config.py (C3) -
  packages/orchestration/model_routing.py (C4) -
  tests/orchestration/test_config.py (C5) -
  tests/orchestration/test_model_routing.py (C5) - .agent/handoff.md (C6)
  NO DOCS ARE EDITED. packages/orchestration/role_config.py IS NOT TOUCHED.
  If any commit would exceed the AGENTS.md insertion cap, SPLIT IT; such a
  split is pre-authorised and is not a deviation.

BASE for this round is ccb736b9. Every byte, count, citation and measurement
below was taken there by the reviewer.

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by delimiter
     index from the COMMITTED .agent/authored/f110-r12.md - marker lines
     EXCLUDED - and write it with a script, never by retyping. If a slice looks
     wrong, apply it as written and DECLARE it in the handback.
  2. C1 is the first substantive commit; this round touches the finding ledger,
     so item 23 binds.
  3. C3 precedes C4 precedes C5. Do not reorder.
  4. Newline conventions, MEASURED at ccb736b9 - re-measured at THIS round's
     base, never carried forward. .agent/live_review.md is 2204274 bytes and
     ends WITHOUT a trailing newline; its append is the two bytes newline
     newline then the slice, and it must still end without one.
     .agent/prose_slips.md is 59944 bytes, same shape, same two-byte append.
     .agent/plan.md is 1875 bytes and ends WITH one. Where an extractor yields a
     trailing newline the target does not take, the TARGET wins.
     .agent/decisions.md IS NOT TOUCHED this round.
  5. NO RUFF GATE IS ORDERED and you must not add one; the reviewer lints it.
     Sort any import block you touch as ruff's isort would - an ALL-CAPS name
     sorts ABOVE a CamelCase one in a `from ... import (...)` list, which is the
     single fact R-0788 cost a round to learn.
  6. NOTHING IS WIRED. No production call reads
     `model_routing.promotion_evidence` this round and role_config.py is not
     edited. The parser is a pure function on a plain mapping; making a routed
     call use it is the NEXT round, deliberately separate so the schema is
     pinned before behaviour moves. Record that absence in the model_routing
     docstring in the AGENTS.md discoverability idiom.
  7. ROUNDS 4 THROUGH 11 SHIPPED BEHAVIOUR IS NOT REVISED. Every constant and
     function those rounds added keeps its behaviour and its signature. You are
     ADDING. In particular `PromotionEvidence`, `PromotionAssertionResults`,
     `build_effective_task_class_tiers` and `validate_task_class_tier_overrides`
     are UNCHANGED - the parser produces the records those already consume.
  8. NO EXISTING TEST IS EDITED, RENAMED, DELETED OR SKIPPED. Measured at
     ccb736b9, the reviewer prototyped this round's config.py change in a
     disposable worktree and ran the three affected suites: 74, 92 and 391
     passed with 3 skipped, all exit 0, no test edited. If you find an existing
     test that must change, STOP, do not change it, and report it as a blocked
     item in the handback.
  9. A sentence this round makes stale INSIDE the change set is repaired in the
     commit that falsifies it. A sentence OUTSIDE the change set that this round
     makes stale is DECLARED in the handback and NOT repaired.
 10. Read .agent/STOP from disk before the first commit and again before C6.
 11. Destructive verification runs ONLY inside a disposable git worktree, never
     in the primary checkout. Purge __pycache__ before every run, use python3
     -B, remove the worktree BY ITS EXACT PATH when done, and prune.
 12. NO remedy.toml IS CREATED IN THE REPOSITORY ROOT. Tests write TOML to a
     pytest tmp_path; any probe writes outside the repository root.

SPEC - C3, packages/orchestration/config.py
  This is a SPEC, not a slice: write it in this module's own idiom and improve
  on any wording below that is worse than what you would write. Do not depart
  from the BEHAVIOUR without declaring it.

  (a) A TABLE-VALUED KEY DECLARES WHAT ITS ENTRIES ARE. `ConfigKeySpec` gains an
      optional field naming the type each ENTRY of a table key holds - `str` for
      a flat map, `dict` for a table of records - defaulting to None meaning
      "entries unchecked". Round 10's `model_routing.task_class_tiers` declares
      `str`, which is what it already validates today.
      WHY THIS IS NEEDED AND WHY THE OBVIOUS ROUTE FAILS, MEASURED: round 10's
      `validate_config` dict branch reports any entry that is not a string. The
      reviewer registered the evidence key in a disposable worktree WITHOUT this
      field and a WELL-FORMED evidence table produced the spurious warning
      "model_routing.promotion_evidence: expected string entries, got
      'architecture' = {...}". One shape rule cannot serve both tables, and
      hard-coding a key name inside validate_config would put policy in the
      lower layer.
  (b) `model_routing.promotion_evidence` IS REGISTERED: env var
      `REMEDY_MODEL_ROUTING_PROMOTION_EVIDENCE`, value_type dict, entry type
      dict, default None, description naming F110 and saying the value maps a
      task class to the benchmark run that licenses a cheaper tier for it.
  (c) validate_config CHECKS ENTRIES AGAINST THE DECLARED ENTRY TYPE and stays
      SHAPE-ONLY. Whether a task class exists, whether a run meets the promotion
      bars, whether a field is missing - all POLICY, all model_routing's, and
      config.py still must not import it.
  (d) The module docstring's table-valued-key paragraph gains a sentence on
      entry types. Keep it short.
      MEASURED AT ccb736b9, so you do not have to rediscover it: registering the
      key is by itself enough to make the NESTED evidence table resolve whole -
      the reviewer's worktree probe read the full record back including its
      `assertion_results` sub-table, with ZERO "Unknown key" diagnostics, where
      the unregistered key produced TEN.

SPEC - C4, packages/orchestration/model_routing.py
  (e) A PURE PARSER, `promotion_evidence_from_mapping`, takes the raw mapping a
      config table produces and returns a mapping of normalized task class to
      `PromotionEvidence`. It reads NO config, imports nothing new beyond what
      the module already has, and is a pure function of its argument - the
      property the module docstring already promises for everything in it.
      Class keys pass through `normalize_task_class`, exactly as
      `validate_task_class_tier_overrides` normalizes its keys.
  (f) THE NESTED `assertion_results` BECOMES A `PromotionAssertionResults`.
      Its two integer readings are the ones
      `PROMOTION_MINIMUM_BLOCK_ASSERTION_PASS_RATE` and
      `PROMOTION_MINIMUM_OVERALL_PASS_RATE` are compared against; read their
      names from `PromotionAssertionResults`' own fields rather than inventing
      spellings.
  (g) A MALFORMED ENTRY IS SKIPPED, NOT GUESSED AT AND NOT RAISED. An entry that
      is not a mapping, or whose `assertion_results` is present but not a
      mapping, or whose fields are of the wrong type, does not produce a record.
      WHY SKIPPING IS THE SAFE DIRECTION HERE, and it is the opposite of the
      override map's answer for a reason worth stating in the code: a missing
      evidence record means the promotion it would have licensed is REFUSED by
      `check_promotion_backed_by_evidence` with
      `RULE_PROMOTION_WITHOUT_EVIDENCE`, so a malformed record fails CLOSED -
      the class keeps its seeded tier. A malformed OVERRIDE, by contrast, is
      refused loudly because dropping it would leave the operator believing a
      re-tier took effect. Both choices refuse to act on input they do not
      understand; they differ only in which direction is conservative.
  (h) THE RETURN VALUE IS EXACTLY WHAT THE EXISTING CONSUMERS TAKE. Measured at
      ccb736b9 by the reviewer, running the real functions: a `PromotionEvidence`
      for `architecture` with model_id `qwen3-8b-instruct`, quantization
      `q4_k_m`, prompt_hash `0f1e2d3c4b5a6978`, tokens 1234, cost 0.42,
      reviewer_verdict `pass`, runs_per_fixture 3, corpus `F082` and assertion
      results 92 and 81 makes `build_effective_task_class_tiers` ACCEPT
      `{"architecture": "cheap"}` - a top-tier class promoted to cheap - and the
      routed evidence then reads tier `cheap`, reason `per_project_override`,
      promoted_by `qwen3-8b-instruct + q4_k_m@0f1e2d3c4b5a6978 on F082`. The
      SAME map with NO evidence raises `OverrideRefused` carrying one violation
      whose `rule_name` is `promotion_without_evidence`. Your parser must produce
      a record that reproduces the first of those two readings.
  (i) THE DELIBERATE ABSENCE, in the AGENTS.md idiom: nothing reads this parser
      yet. Name where the wiring will go - the config-reading layer in
      role_config.py, which is where `resolve_effective_task_class_tiers`
      already reads the tiers table - so a reader searching for the caller finds
      the sentence rather than a silence.

SPEC - C5, the tests
  New tests only, split by module: config-surface cases into
  tests/orchestration/test_config.py, parser cases into
  tests/orchestration/test_model_routing.py. Read every expected class, tier and
  field name from the module rather than spelling it.
  (j) THE EVIDENCE TABLE RESOLVES WHOLE, nested sub-table included, from a TOML
      file written to tmp_path, with source PROJECT and NO load warning.
  (k) A WELL-FORMED EVIDENCE TABLE IS REPORTED SILENTLY by validate_config, and
      a table whose ENTRY is a scalar is reported. The round 10 tiers key must
      STILL report a non-string entry - assert that too, so (a)'s entry type is
      shown to discriminate BETWEEN the two keys rather than to disable the
      check.
  (l) THE PARSER ROUND-TRIPS A COMPLETE RECORD: every field of
      `PromotionEvidence` comes back with the value the mapping carried, and
      `assertion_results` is a `PromotionAssertionResults` with both readings.
  (m) THE PARSER SKIPS WHAT IT CANNOT READ: a non-mapping entry, an entry whose
      `assertion_results` is a scalar, and an entry with a wrong-typed field
      each produce NO record, while a well-formed sibling in the SAME mapping
      still does - so skipping is shown to be per-entry rather than per-table.
  (n) THE PARSED RECORD LICENSES A REAL PROMOTION. Feed the parser's output to
      `build_effective_task_class_tiers` for a map promoting a top-tier class to
      cheap, and assert it is ACCEPTED and that the routed evidence carries the
      promoted tier and a non-None `promoted_by`. Then assert the SAME map with
      an EMPTY evidence mapping raises `OverrideRefused` whose violation
      `rule_name` is `RULE_PROMOTION_WITHOUT_EVIDENCE`, read from the constant.
      This is the test that makes the round mean something: without it the
      parser is a shape exercise.

Done when - EIGHT GATES, each run and its real exit code recorded
  G1 TRANSPORT. sha256sum .agent/authored/f110-r12.md .agent/last_block.md -
     ONE digest twice. Report wc -l of the authored file. Per
     docs/agents/planner_reviewer_prompt.md item 37 this proves the saved copy
     and its mirror agree and claims nothing about the emitted bytes.
  G2 THE PLAN. cmp the PLAN12 extraction against .agent/plan.md - exit 0.
     Report wc -l (must be under 50) and grep -c for '^## Goal' and
     '^## Next Steps' (1 each).
  G3 THE LEDGER APPEND, full forensics. RECORD11, DONE787 and DONE788 are ONE
     append in ONE commit, joined in that order by the file's own paragraph
     separator. State the arithmetic 2204274 + 2 + len(the joined text) against
     the real size after C2; show the pre-C2 content is an exact byte PREFIX;
     show the file still ends WITHOUT a newline. SECOND READER: a script COUNTS
     N from the appended text, then compares the LAST N blank-line units of the
     whole file against its N paragraphs IN ORDER. NEGATIVE CONTROL: flip one
     byte inside the FIRST appended paragraph and show the second reader
     REJECTS it. Report the count of lines matching the RECORD11 header EXACTLY
     AS THE SLICE SPELLS IT - the separator after "R11" is U+2014 EM DASH, not
     a hyphen; copy the string from the extracted slice - before C2 (expect 0)
     and after C2 (expect 1). Report grep -c '^Done: R-0787 — ' and
     '^Done: R-0788 — ' after C2 (1 each).
  G4 .agent/prose_slips.md gets a BYTE-EQUALITY check only, per the gate budget:
     final bytes == 59944 + 2 newlines + SLIPS12, base an exact prefix, still
     ending without a newline. Then report the OPEN FINDING SET, derived
     mechanically after C2: every '^- R-\d+ — ' paragraph minus every
     '^Done: R-\d+ — ' line, both counted as SETS OF UNIQUE IDS and not as line
     counts - two ids in this ledger carry two Done paragraphs each, so a line
     count reads two low. Report the unique registered count, the unique
     resolved count and the open count, and confirm R-0787 and R-0788 are NOT
     in the open set while R-0767 IS.
  G5 THE TWO PRODUCTION FILES, MEASURED AND RUN. git show --numstat for C3 and
     C4, per path. ast.parse over both. QUOTE EVERY DELETED LINE VERBATIM and
     name its region; for model_routing.py every deletion must be inside the
     MODULE DOCSTRING and any that is not is a STOP. Then RUN the shipped code
     and print what it RETURNED, against TOML written outside the repository
     root: the resolved evidence value and its source; the load warnings (empty);
     validate_config for a well-formed and for a malformed table; the parser's
     output for a complete record, for each malformed shape of SPEC (m), and the
     effective table and routed evidence SPEC (n) describes, in both the
     with-evidence and the no-evidence case.
  G6 THE RED PROOF, in a disposable worktree at C5, never cd-ed into,
     __pycache__ purged, python3 -B, module __file__ printed from inside it.
     Control first, with its count and exit code. Then, one at a time, reverting
     between each:
       (i)   the entry-type check is dropped from validate_config
       (ii)  the parser ACCEPTS a malformed entry instead of skipping it
       (iii) the parser drops assertion_results, leaving it None
       (iv)  the flatten stop-set no longer includes the new key
     For each: the exit code, the failure count, and the FULL LIST of red test
     ids, never truncated. PRINT ONE RAW pytest "FAILED ..." line beside your
     parsed set and confirm they agree - the node id is the SECOND
     whitespace-separated token. State whether the red sets are pairwise
     disjoint: report what you MEASURED, and non-disjoint is a REPORTABLE
     RESULT rather than a fault. Read git status --porcelain ON THE PRIMARY
     CHECKOUT immediately after every mutation. Revert with
     git checkout -- <exact path> INSIDE the worktree; each revert must return
     the worktree to the control's count.
  G7 THE SUITES, each its own invocation, run serially, all exit 0. The counts
     in brackets are what the reviewer measured at ccb736b9. Report yours beside
     them and explain any difference. ONLY the two suites this round adds to may
     move; for those, report the number YOU measure rather than targeting one.
       pytest tests/orchestration/test_config.py -q                (74 at base, +new)
       pytest tests/orchestration/test_model_routing.py -q         (391 passed,
         3 skipped at base, +new)
       pytest tests/orchestration/test_role_config.py -q           (92 - UNMOVED)
       pytest tests/orchestration/test_orchestrator_model_routing.py -q  (20 - UNMOVED)
       pytest tests/cli/test_init_cmd.py tests/cli/test_worker_facade_cmd.py tests/orchestration/test_budget_stop_integration.py tests/orchestration/test_checkpoints.py tests/orchestration/test_dead_model_list.py tests/orchestration/test_f018_authority_integration.py -q   (304 - UNMOVED)
       pytest tests/orchestration/test_fence_e2e.py tests/orchestration/test_job_budgets.py tests/orchestration/test_loop_spec.py tests/orchestration/test_predictive_budget.py tests/orchestration/test_safe_points.py -q   (433 - UNMOVED)
       pytest tests/runtimes/test_runtime_config.py tests/runtimes/test_runtime_lifecycle_safety.py tests/test_data_paths.py tests/ui_server/test_command_channel.py -q   (199 - UNMOVED)
       pytest tests/docs/ -q                                       (295 - UNMOVED)
       pytest tests/cli/test_golden_path.py -q                     (42 - the canary)
     THIS GATE LIST IS WIDER THAN ROUND 10'S ON PURPOSE. config.py is read by
     25 test files, and round 10 shipped a red tip because a suite outside the
     narrow set stubbed a config reader. The five UNMOVED groups are the
     regression evidence for a change in the lowest layer this feature touches.
  G8 THE TREE, THE COMMITS AND THE SWEEP. git status --porcelain empty
     immediately before C6 is staged. git ls-files .remedy-wt returns nothing.
     No worktree of this round's making survives. Confirm NO remedy.toml exists
     in the repository root. Report git diff --stat ccb736b9..<C5> -- docs/
     (MUST be empty) and the same over packages/ and apps/ with config.py and
     model_routing.py EXCLUDED (MUST be empty) - constraints 6 and 7 MEASURED
     rather than asserted, and the second is what proves role_config.py was not
     touched. Report the per-commit INSERTION count, the + column only, for
     every commit BEFORE the handback commit, cell by cell against the
     handback's own ## Commits table, and confirm each is under the AGENTS.md
     500-insertion cap.

Handback - rewrite .agent/handoff.md per docs/agents/handback_template.md
  It carries: SESSION 3 of F110, round 12, rounds so far 12; the state block
  with the Fortschritt line; the item-status table with every SPEC item and
  every gate exactly once; the per-commit changed-files tables; one line per
  gate with its real result; the authored-text proofs; the deviations; the next
  step. NO length cap applies (AGENTS.md amend0827 rule 3). Report the two STOP
  readings and the open-finding set G4 derives. DECLARE any sentence outside the
  change set this round makes stale without repairing it.

<<<BEGIN PLAN12>>>
# Plan — F110 Model routing by task class

Branch: feature/f110-model-routing-by-task-class, cut from `main` after
pull request 232 was merged at the Open PR Gate.

## Goal

End one-model-for-everything: every provider call declares a TASK CLASS, a
router maps classes to model tiers, and each routed call records the routed
model WITH its reason. The hard rules of
`docs/agents/model_routing_policy.md` are ENFORCED IN CODE, and moving a
class to a cheaper tier is possible only against documented benchmark
evidence — never by editing a mapping casually.

## Current Step

Round 12, session 3 — THE PROMOTION-EVIDENCE SCHEMA. `config.py` learns
that a table-valued key can declare what its ENTRIES hold, F110 registers
`model_routing.promotion_evidence` as a table of records, and
`model_routing` gains a PURE parser turning that raw mapping into
`PromotionEvidence`. Nothing is wired: no call reads the key yet, so the
schema is pinned before routing behaviour moves. Round 11's PASS verdict is
booked and `R-0787` and `R-0788` are resolved.

## Next Steps

- The wiring round: `resolve_effective_task_class_tiers` reads the evidence
  table too and passes it to the builder and to the seam, so a documented
  run actually licenses a cheaper tier at a routed call.
- The acceptance round: a fixture run whose every call's evidence shows
  class, tier and reason, per the feature file's Acceptance section.
- The integration gate round, before closure.
- The closure sequence, which also runs the one checklist consolidation
  pass DECISION F110 D1 carries into it, and which updates the Design
  bullet of `docs/roadmap/features/T3_F110.md`.

## Risks

- `config.py` is read by 25 test files, so the gate list for a change in
  that layer is deliberately wider than round 10's, which shipped a red
  tip from a suite outside the narrow set.
- A malformed evidence record fails CLOSED — the promotion it would have
  licensed is refused — which is the opposite direction from a malformed
  override, and both are stated in code.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
<<<END PLAN12>>>

<<<BEGIN RECORD11>>>
Gate: F110 R11 — the round 11 entry. VERDICT PASS, over the range `0d025469..4d61041e` plus the handback commit `ccb736b9`. THE BRANCH TIP IS GREEN AGAIN, which is what this round existed to do: `python3 -B -m pytest tests/orchestration/test_orchestrator_model_routing.py -q` reads exit 0 at 20 passed where the round 10 tip read exit 1 at 1 failed, 18 passed, and `ruff check` over both edited test files answers "All checks passed!", run reviewer-side. THE TRANSPORT PROOF REACHED THE REVIEWER'S OWN BYTES: `cmp` between the reviewer's scratch original and the committed `.agent/authored/f110-r11.md` exits 0, and one digest `46c7e1c308bac396e4690b2c4418d7820f5333fd33400863b20b726273a943d2` at 24618 bytes covers the original, the saved copy at `46262bf2` and the mirror at `87adb34e`; the block is 262 lines. EVERY SLICE WAS RE-DERIVED BYTE FOR BYTE and every size matched the pre-emission projection: `.agent/plan.md` equals PLAN11 plus the one trailing newline the target's convention adds, at 42 lines; the C2 ledger append is 2196008 + 2 + 7793 = 2203803 and the C5 append is 2203803 + 2 + 469 = 2204274, each with its predecessor an exact byte PREFIX and the file still ending without a newline — two appends to one file in one round, both exact; `.agent/prose_slips.md` is 59944. THE FIX KEEPS THE PROOF INSTEAD OF MERELY WIDENING THE STUB, which is the part worth recording: the removed assertion proved WHICH key `resolve_orchestrator_model` read, and it is replaced by a positive test over the keys the double now records. THE REVIEWER RED-PROOFED THAT DISCRIMINATOR AGAINST THE SHIPPED CODE rather than against its own prototype, in a disposable worktree at `4d61041e` with the module path printed from inside it: control 20 passed exit 0; with the operator-override read replaced by None the suite reads exit 1 at 3 failed, 17 passed, and `TestTheOperatorOverrideKeyIsTheOneRead::test_the_operator_override_key_is_among_the_keys_read` IS among the red ids, so the new test is a real discriminator and not a shape check. The parsed red set was checked against the raw pytest lines beside it, which is round 9's SLIPS10 lesson applied by both parties. The primary checkout read `git status --porcelain` EMPTY during the mutation and the revert returned the worktree to 20 passed. THE CHANGE SET IS EXACTLY WHAT THE BLOCK NAMED: `git diff --stat 0d025469..4d61041e -- packages/ apps/ docs/` is EMPTY, so round 10's production code stands untouched, and the six deletions in the R-0787 fix are all inside `_FakeConfig` and `_patch_config` with none in a test body. THE SUITES WERE RE-RUN BY THE REVIEWER at 20, 74, 92, 391 with 3 skipped, 68, 295 and 42, every one exit 0, and only the repaired suite moved — 19 at the round 10 base to 20, the repaired test plus the one new one. The per-commit insertion counts are 262, 195, 10, 10, 49, 1 and 5, every one under the AGENTS.md cap; `ccb736b9` is 416 insertions against 575 deletions, a full-file rewrite of a single `.agent/**` state file and exempt under DECISION F104 D1. ONE HANDBACK NUMERAL IS WRONG AND IT IS A PROSE SLIP, NOT A FINDING: the handback reports 278 open over 349 registered and 71 resolved, computed as 349 minus 71, but `R-0721` and `R-0725` each carry TWO `Done:` paragraphs, so the unique resolved count is 69 and the OPEN SET IS 280. Nothing on disk is wrong — the ledger is append-only and both duplicate resolutions are landed history that must not be rewritten — and item 10 requires every block to recompute the set mechanically rather than carry it forward, which is what this round's successor does. Recorded in `.agent/prose_slips.md`; no R-id, per amend0827-process-diet rule 2. The tree is clean, `git ls-files .remedy-wt` returns nothing, no worktree of the round's making survives, `.agent/candidates.md` is untouched and still EMPTY, and the branch is pushed at `ccb736b9` with no pull request open.
<<<END RECORD11>>>

<<<BEGIN DONE787>>>
Done: R-0787 — RESOLVED at the F110 R12 gate, fixed in `cc32f16b` (F110 R11 C3). The reviewer verified the repair against the SHIPPED code rather than the handback: `tests/orchestration/test_orchestrator_model_routing.py` reads exit 0 at 20 passed at `4d61041e`, where the same command at `0d025469` read exit 1 at 1 failed, 18 passed. `_FakeConfig.get` no longer refuses unknown keys; it records every key in `keys_read` and answers None for anything but the operator override, None being the correct "no per-project overrides" answer for the F110 routing table. THE PROOF THE REFUSAL CARRIED WAS KEPT RATHER THAN DROPPED, which is why this resolves rather than merely silences: the new `TestTheOperatorOverrideKeyIsTheOneRead::test_the_operator_override_key_is_among_the_keys_read` asserts the override key is among the keys read, and the reviewer red-proofed it in a disposable worktree at `4d61041e` — replacing the `get_config().get(...)` result with None turns the suite red at 3 failed, 17 passed with that test among the red ids. Production code was not changed and did not need to be: it reads `model_routing.task_class_tiers` because round 10's SPEC requires it, and that behaviour was verified correct at `0d025469`.
<<<END DONE787>>>

<<<BEGIN DONE788>>>
Done: R-0788 — RESOLVED at the F110 R12 gate, fixed in `fdfc7e2c` (F110 R11 C4). `python3 -m ruff check tests/orchestration/test_config.py` answers "All checks passed!" at `4d61041e`, run reviewer-side because the worker's permission layer refuses the tool. The fix is the single move the finding measured — `_TABLE_VALUED_KEYS` above `ConfigKeySpec` in the `from packages.orchestration.config import (...)` list — applied as a hand edit rather than by running a formatter, at +1/−1, with no import added and none removed.
<<<END DONE788>>>

<<<BEGIN SLIPS12>>>
2026-09-03 · F110 R11 · The round 11 handback reported the open-finding set as "278 open over 349 registered and 71 resolved", computing it as 349 minus 71 — LINE counts rather than sets of unique ids. `.agent/live_review.md` carries TWO `Done:` paragraphs each for `R-0721` and `R-0725`, so the unique resolved count is 69 and the open set after that round's two registrations is 280, not 278. The block's own Handback clause asked for the derivation "every '^- R-\d+ — ' paragraph minus every '^Done: R-\d+ — ' line" and thereby invited the line-count reading, so the wording is the reviewer's to answer for. Nothing on disk is wrong: the ledger is append-only, both duplicate resolutions are landed history that must not be rewritten, and checklist item 10 requires every block to recompute the set mechanically rather than carry a number forward. THE LESSON: an open-set derivation is stated as a set difference over UNIQUE IDS, and any block that orders the count says "unique" in the order — a ledger that has ever resolved one id twice makes the line-count reading silently wrong, and this one has. Reviewer block-wording slip; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIPS12>>>
