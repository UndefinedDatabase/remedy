STEP F110 T002/T003 / ROUND 10 - F110 Model routing by task class
FEATURE F110 - Model routing by task class (Tier 3) - SESSION 3, ROUND 10

Goal
  THE CONFIGURATION ROUND. The per-project override map stops being an argument
  a caller passes and becomes a TABLE READ FROM remedy.toml: config.py learns to
  resolve a TABLE-VALUED key through the precedence chain it already has, F110
  registers one such key, and the routing layer lays that table over the shipped
  seed mapping through the validator round 6 already built - so a project can
  re-tier a class, and CANNOT re-tier one the hard rules protect. Book round 9's
  PASS verdict and its two prose slips in the same round.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f110-r10.md
  C0b mirror it to .agent/last_block.md
  C1  apply PLAN10 to .agent/plan.md (FIRST substantive commit, item 23)
  C2  append RECORD9 to .agent/live_review.md, SLIPS10 to
      .agent/prose_slips.md and DECISION5 to .agent/decisions.md
  C3  PRODUCTION: config.py learns table-valued keys and registers F110's
  C4  PRODUCTION: role_config.py routes against the CONFIGURED table
  C5  TESTS: the config surface and the routing layer
  C6  DOCS: the configuration document gains the new key
  C7  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f110-r10.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/plan.md (C1) - .agent/live_review.md (C2) -
  .agent/prose_slips.md (C2) - .agent/decisions.md (C2) -
  packages/orchestration/config.py (C3) -
  packages/orchestration/role_config.py (C4) -
  tests/orchestration/test_config.py (C5) -
  tests/orchestration/test_role_config.py (C5) -
  docs/system/remedy-toml-configuration-system-v0.md (C6) -
  .agent/handoff.md (C7)
  If any commit would exceed the AGENTS.md insertion cap, SPLIT IT; such a
  split is pre-authorised and is not a deviation.

BASE for this round is a1368633. Every byte, count, citation and measurement
below was taken there by the reviewer.

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by delimiter
     index from the COMMITTED .agent/authored/f110-r10.md - marker lines
     EXCLUDED - and write it with a script, never by retyping. If a slice looks
     wrong, apply it as written and DECLARE it in the handback.
  2. C1 is the first substantive commit; this round touches the finding ledger,
     so item 23 binds.
  3. C3 precedes C4 precedes C5. Do not reorder: C4 imports what C3 registers.
  4. Newline conventions, MEASURED at a1368633 - all four re-measured at THIS
     round's base, never carried forward. .agent/live_review.md is 2190200 bytes
     and ends WITHOUT a trailing newline; its append is the two bytes newline
     newline then the slice, and it must still end without one.
     .agent/prose_slips.md is 56793 bytes, same shape, same two-byte append.
     .agent/decisions.md is 734845 bytes and ends WITH exactly one newline; its
     append is ONE newline, the slice, then one final newline. .agent/plan.md is
     2152 bytes and ends WITH one. Where an extractor yields a trailing newline
     the target does not take, the TARGET wins.
  5. NO RUFF GATE IS ORDERED and you must not add one; the reviewer lints it.
  6. THIS IS A DOCS ROUND, so tests/docs/ is a gate, not an afterthought - see
     G7. Only the ONE documentation file in the change set is edited; no other
     file under docs/ is written, and docs/roadmap/ is NOT touched.
  7. ROUNDS 4 THROUGH 9 SHIPPED BEHAVIOUR IS NOT REVISED. In particular
     build_effective_task_class_tiers, validate_task_class_tier_overrides and
     route_role_call keep their current signatures and behaviour: this round
     CALLS them, it does not change them. model_routing.py IS NOT EDITED AT ALL
     this round and is not in the change set.
  8. NO EXISTING TEST IS EDITED, RENAMED, DELETED OR SKIPPED. Measured at
     a1368633, the reviewer applied this round's config.py change in a
     disposable worktree and ran test_config.py, test_role_config.py and
     test_model_routing.py together: 536 passed, 3 skipped, exit 0, no test
     edited. If you find an existing test that must change, STOP, do not change
     it, and report it as a blocked item in the handback.
  9. A sentence this round makes stale INSIDE the change set is repaired in the
     commit that falsifies it. A sentence OUTSIDE the change set that this round
     makes stale is DECLARED in the handback and NOT repaired.
 10. Read .agent/STOP from disk before the first commit and again before C7. If
     it exists at either reading, finish the commit in hand, write the handback
     and stop.
 11. Destructive verification runs ONLY inside a disposable git worktree, never
     in the primary checkout. Purge __pycache__ before every run, use python3
     -B, remove the worktree BY ITS EXACT PATH when done, and prune.
 12. NO remedy.toml IS CREATED IN THE REPOSITORY ROOT. Measured at a1368633
     there is none and none is tracked, and creating one would change how every
     test in the suite resolves configuration. Every test writes its TOML to a
     pytest tmp_path and passes it to load_config explicitly.

SPEC - C3, packages/orchestration/config.py
  This is a SPEC, not a slice: write the code in this module's own idiom and
  improve on any wording below that is worse than what you would write. Do not
  depart from the BEHAVIOUR without declaring it.

  (a) TABLE-VALUED KEYS BECOME A KIND config.py UNDERSTANDS. A ConfigKeySpec
      whose value_type is dict resolves to the WHOLE TOML SUB-TABLE as one
      value, through the existing precedence chain, instead of being flattened
      into one unregistered key per entry.
      THE MECHANISM, MEASURED: _flatten_toml recurses into every dict, so
      `[remedy.model_routing.task_class_tiers]` with two entries currently
      flattens to two keys, NEITHER of which is in _KEY_SPEC_MAP, and load_config
      then appends one "Unknown key in ..." diagnostic per entry. Stop the
      recursion at a key that is registered as table-valued: derive the set of
      such keys FROM THE REGISTRY ITSELF - the keys whose spec has
      `value_type is dict` - so registering a second table key later needs no
      second edit here. Do not hand-list the names.
  (b) F110'S KEY IS REGISTERED: `model_routing.task_class_tiers`, env var
      `REMEDY_MODEL_ROUTING_TASK_CLASS_TIERS`, value_type dict, default None,
      with a description naming F110 and saying the value is a task-class to
      model-tier map. Default None and NOT an empty dict, so "unset" and
      "explicitly empty" stay distinguishable.
  (c) validate_config GAINS A dict BRANCH, and it validates SHAPE ONLY: the
      value is a mapping and every key and every value in it is a string. A
      non-string entry gets one warning naming the key and the offending entry.
      WHY SHAPE ONLY, AND WHERE THE REST LIVES: whether a task class exists,
      whether a tier exists, and whether an override breaks a hard rule are
      POLICY questions that model_routing.validate_task_class_tier_overrides
      already answers, and config.py must not import model_routing - config is
      the lower layer and the whole module is deliberately policy-free. C4 runs
      the policy validation where the policy lives.
  (d) THE PUBLIC API docstring list gains nothing it does not need, but the
      module docstring gains a short paragraph on table-valued keys: what they
      are, that the stop-set is derived from the registry, and that an env var
      cannot carry a table so such a key is configured in TOML only.

SPEC - C4, packages/orchestration/role_config.py
  (e) THE CONFIGURED TABLE IS READ AND LAID OVER THE SEED MAPPING. A new
      module-level function returns the EFFECTIVE task-class table: it reads
      `model_routing.task_class_tiers` from the config, and when that value is
      missing or empty it returns model_routing.TASK_CLASS_TIERS unchanged.
      Otherwise it calls model_routing.build_effective_task_class_tiers with the
      configured map and returns what that returns. Import get_config INSIDE the
      function body, which is the idiom resolve_orchestrator_model already
      established in this module and which its comment explains.
  (f) A REFUSED OVERRIDE MAP WARNS, NAMES EVERY VIOLATED RULE, AND ROUTES
      AGAINST THE SHIPPED TABLE. build_effective_task_class_tiers raises
      OverrideRefused carrying every violation. Catch it, emit ONE UserWarning
      whose text names the config key and EVERY violated rule name it carries,
      and return model_routing.TASK_CLASS_TIERS. This is DECISION F110 D5 below;
      implement what that decision says and do not re-decide it.
  (g) THE SEAM ROUTES AGAINST THE EFFECTIVE TABLE. resolve_routed_call_evidence
      passes the table from (e) to route_role_call as its effective_tiers
      argument. Nothing else about that function changes: it still swallows
      OriginatingTaskClassRequired and nothing else, and still returns None for
      an inheriting role with no origin.
  (h) provider, model AND effort ARE UNTOUCHED. The precedence chain is not
      read, not reordered and not extended. This round changes only what a call
      RECORDS, exactly as round 9's docstring paragraph says, and that paragraph
      stays true - do not weaken it.

SPEC - C5, the tests
  New tests only. tests/orchestration/test_config.py takes the config-surface
  cases and tests/orchestration/test_role_config.py the routing ones. Every
  expected class and tier is READ from model_routing rather than spelled.
  (i) A TOML TABLE RESOLVES AS ONE dict, with source PROJECT, and load_config
      reports NO warning for it. Write the TOML to tmp_path and pass it to
      load_config; assert the resolved value equals the whole table.
  (j) AN UNSET KEY RESOLVES TO None, and a USER-file table is overridden by a
      PROJECT-file one - the precedence chain, exercised on a table.
  (k) validate_config REPORTS A NON-STRING ENTRY and stays silent on a
      well-formed table.
  (l) A LEGAL OVERRIDE REACHES A ROUTED CALL. Configure a table that re-tiers a
      class the hard rules do NOT protect, and assert that
      resolve_role_config(<a role declaring that class>).routed_call carries the
      OVERRIDDEN tier and the OVERRIDE reason rather than the seed one. Pick the
      class and role by READING ROLE_TASK_CLASSES and TASK_CLASS_TIERS, and pick
      a target tier that leaves every hard rule satisfied - the reviewer
      measured that `summarize` is seeded `cheap` and is named by the `teacher`
      and `summary` roles, and that no hard rule pins it.
  (m) AN ILLEGAL OVERRIDE IS REFUSED, WARNS WITH THE RULE NAMED, AND ROUTES
      SEEDED. Configure a table demoting an ORCHESTRATION class below the top
      tier. Assert a UserWarning is emitted, that its text contains
      model_routing.RULE_ORCHESTRATION_BELOW_TOP_TIER, and that the resulting
      routed_call carries the SEEDED tier - the override did not take effect.
      Assert the rule name by READING the constant, never by spelling it.
  (n) CONFIG FAULTS DO NOT BREAK CONFIG RESOLUTION. With the illegal table
      configured, resolve_role_config still returns the same provider, model and
      effort it returns with no config at all. A routing fault must not become a
      config-resolution fault - the round 9 lesson, one layer further out.

SPEC - C6, docs/system/remedy-toml-configuration-system-v0.md
  (o) The document gains a SHORT section on the new key: the TOML shape as a
      fenced example, that hard rules win so an override breaking one is refused
      with the rule named and the shipped table used, and that this key is TOML
      only because an env var cannot carry a table. Read the file first and
      match its existing heading level and table style. Do NOT restate the seed
      mapping - docs/agents/model_routing_policy.md owns it - and do not touch
      the existing key table beyond adding the new row if that is the file's
      own convention for a new key.

Done when - EIGHT GATES, each run and its real exit code recorded
  G1 TRANSPORT. sha256sum .agent/authored/f110-r10.md .agent/last_block.md -
     ONE digest twice. Report wc -l of the authored file. Per
     docs/agents/planner_reviewer_prompt.md item 37 this proves the saved copy
     and its mirror agree and claims nothing about the emitted bytes.
  G2 THE PLAN. cmp the PLAN10 extraction against .agent/plan.md - exit 0.
     Report wc -l (must be under 50) and grep -c for '^## Goal' and
     '^## Next Steps' (1 each).
  G3 THE LEDGER APPEND, .agent/live_review.md, full forensics. State the
     arithmetic 2190200 + 2 + len(RECORD9) against the real new size; show the
     pre-C2 content is an exact byte PREFIX; show it still ends WITHOUT a
     newline. SECOND READER: a script COUNTS N from the slice, then compares the
     LAST N blank-line units of the whole file against the slice's N paragraphs
     IN ORDER. NEGATIVE CONTROL: flip one byte inside the FIRST appended
     paragraph and show the second reader REJECTS it. Report the count of lines
     matching the RECORD9 header EXACTLY AS THE SLICE SPELLS IT - the separator
     after "R9" is U+2014 EM DASH, not a hyphen; copy the string from the
     extracted slice rather than retyping it - before C2 (expect 0) and after
     C2 (expect 1).
  G4 THE DECISIONS APPEND, .agent/decisions.md, full forensics, the same five
     readings as G3 with its own convention: 734845 + 1 + len(DECISION5) + 1,
     ends with exactly ONE newline, second reader over the paragraphs it counts,
     negative control on the FIRST appended paragraph. Report
     grep -c '^## DECISION F110 D5 ' before and after C2. .agent/prose_slips.md
     gets a BYTE-EQUALITY check only, per the gate budget: final bytes ==
     before + 2 newlines + SLIPS10, with the base an exact prefix.
  G5 THE PRODUCTION FILES, MEASURED AND RUN. git show --numstat for C3 and C4,
     per path. Run ast.parse over both real files. QUOTE EVERY DELETED LINE
     VERBATIM and name its region. Then RUN the shipped code and print what it
     RETURNED, against TOML written to a scratch path outside the repository
     root: the resolved value and source for a configured table; the warnings
     list (must be empty for a well-formed table); the effective table for no
     config, for a legal override and for an illegal one; the routed_call a
     declared role gets in each of those three states; and the full text of the
     warning the illegal map produces.
  G6 THE RED PROOF, in a disposable worktree at C5, never cd-ed into, with
     __pycache__ purged and python3 -B. Print the imported module __file__ from
     inside the worktree. Run the UNMUTATED CONTROL FIRST and report its count
     and exit code. Then, one at a time, reverting between each:
       (i)   _flatten_toml recurses into table-valued keys again
       (ii)  the OverrideRefused catch is removed
       (iii) the refusal path returns the CONFIGURED map instead of the shipped
             table - the silent-downgrade mutation
       (iv)  the effective table is ignored and route_role_call is called
             without it
     For each: the exit code, the number of failures, and the FULL LIST of red
     test ids, never truncated. When you parse those ids, PRINT ONE RAW pytest
     summary line beside your parsed set and confirm they agree - the node id is
     the SECOND whitespace-separated token of a "FAILED ..." line, and both the
     worker and the reviewer mis-parsed this in round 9. State whether the red
     sets are pairwise disjoint - report what you MEASURED, do not assume, and
     non-disjoint is a REPORTABLE RESULT rather than a fault. Read git status
     --porcelain ON THE PRIMARY CHECKOUT immediately after every mutation, in
     the same step. Every revert is a git checkout -- <exact path> INSIDE the
     worktree, and each must return the worktree to the control's count.
  G7 THE SUITES, each its own invocation, run serially, all exit 0. The counts
     in brackets are what the reviewer measured at a1368633 for the suites this
     round does not add to - report yours beside them and explain any
     difference. For the two suites this round DOES add to, report the number
     YOU measure and do not target a number this block names.
       pytest tests/orchestration/test_config.py -q            (63 at base, +new)
       pytest tests/orchestration/test_role_config.py -q       (82 at base, +new)
       pytest tests/orchestration/test_model_routing.py -q     (391 passed,
         3 skipped - UNMOVED; model_routing.py is not edited this round)
       pytest tests/docs/ -q                                   (295 - the docs
         gate constraint 6 names; this round edits a file under docs/)
       pytest tests/orchestration/test_teacher_model.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_orchestrator_model_routing.py tests/orchestration/test_job_role_routing.py tests/cli/test_teach_cmd.py -q   (87 - UNMOVED)
       pytest tests/test_do_job_flow.py tests/orchestration/test_job_evidence.py tests/orchestration/test_execution_config_evidence.py tests/orchestration/test_task_plan_evidence.py tests/orchestration/test_token_cost_policy.py tests/orchestration/test_model_aliases.py -q   (333 - UNMOVED)
       pytest tests/cli/test_golden_path.py -q                 (42 - the canary)
     The UNMOVED suites are this round's regression evidence: config.py is
     imported almost everywhere, so a fault in the flatten change surfaces there
     rather than in either suite this round grows.
  G8 THE TREE, THE COMMITS AND THE SWEEP. git status --porcelain empty
     immediately before C7 is staged. git ls-files .remedy-wt returns nothing.
     No worktree of this round's making survives. Confirm NO remedy.toml exists
     in the repository root (constraint 12). Report
     git diff --stat a1368633..<C6> -- packages/ apps/ with config.py and
     role_config.py EXCLUDED (must be empty) and
     git diff --stat a1368633..<C6> -- docs/ (must list the ONE documentation
     file and nothing else) - constraint 6 and 7 MEASURED rather than asserted.
     Report the per-commit INSERTION count, the + column only, for every commit
     BEFORE the handback commit, cell by cell against the handback's own
     ## Commits table, and confirm each is under the AGENTS.md 500-insertion
     cap. The handback commit's own numbers go in neither place - the reviewer
     measures them at the next gate.

Handback - rewrite .agent/handoff.md per docs/agents/handback_template.md
  It carries: SESSION 3 of F110, round 10, rounds so far 10; the state block
  with the Fortschritt line; the item-status table with every SPEC item and
  every gate exactly once; the per-commit changed-files tables; one line per
  gate with its real result; the authored-text proofs; the deviations; the next
  step. NO length cap applies (AGENTS.md amend0827 rule 3) - do not declare one.
  Report the two STOP readings, and DECLARE any sentence outside the change set
  this round makes stale without repairing it.

<<<BEGIN PLAN10>>>
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

Round 10, session 3 — THE CONFIGURATION ROUND. `config.py` learns to
resolve a TABLE-VALUED key through the precedence chain it already has,
F110 registers `model_routing.task_class_tiers`, and the routing layer lays
that table over the seed mapping through the validator round 6 built. A
project can re-tier a class; it cannot re-tier one the hard rules protect,
and a refused map warns with the rule named and routes seeded — DECISION
F110 D5. Round 9's PASS verdict and its two prose slips are booked in the
same round.

## Next Steps

- The promotion-evidence round: the evidence map is read from configuration
  too, so a documented benchmark run can license a cheaper tier — the last
  unbuilt clause of T003.
- The acceptance round: a fixture run whose every call's evidence shows
  class, tier and reason, per the feature file's Acceptance section.
- The integration gate round, before closure.
- The closure sequence, which also runs the one checklist consolidation
  pass DECISION F110 D1 carries into it, and which updates the Design
  bullet of `docs/roadmap/features/T3_F110.md`.

## Risks

- `config.py` is imported almost everywhere, so the flatten change is the
  round's real blast radius; the unmoved suites are the regression evidence.
- A refused override map must not break config resolution — the round 9
  lesson one layer further out.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
<<<END PLAN10>>>

<<<BEGIN RECORD9>>>
Gate: F110 R9 — the round 9 entry. VERDICT PASS, over the range `328228dc..8c57d0bc` plus the handback commit `a1368633`. THE TRANSPORT PROOF REACHED THE REVIEWER'S OWN BYTES THIS ROUND, which is stronger than the chain §3 item 37 describes: the worker copied the block with `shutil.copyfile` from the reviewer's scratch original rather than retyping it, so `cmp` between that original — written before delegation and untouched since — and the committed `.agent/authored/f110-r9.md` exits 0, and one digest `59f9d6c6903248168c562ee2e348eb2a62908f96e1d31172d6f2d07502e07118` at 30628 bytes covers the original, the saved copy at `d8747fb0` and the mirror at `366f0c0b`. The block is 399 lines against the reviewer's own projection of 399, under the §3 item 1 cap of 400, which it reached only after real cuts from 420. EVERY SLICE WAS RE-DERIVED BYTE FOR BYTE BY THE REVIEWER and every figure matched the pre-emission projection exactly: `.agent/plan.md` equals PLAN9 plus the one trailing newline the target's convention adds, at 46 lines; `.agent/live_review.md` is 2185166 + 2 + 5032 = 2190200, the real size, base an exact prefix, still ending without a newline; `.agent/decisions.md` is 734845 = 731148 + 1 + 3695 + 1, ending with exactly one newline; `.agent/prose_slips.md` equals its base plus two newlines plus SLIPS9. `ruff check` over all three changed files answers "All checks passed!", run reviewer-side because the worker's permission layer refuses the tool. THE DELETIONS WERE READ LINE BY LINE: C3 is 105 insertions against 17 deletions, of which the 10 in `model_routing.py` are ALL inside the module docstring — the two sentences this round falsified, repaired in the commit that falsified them per constraint 9 — and the 7 in `role_config.py` are the Public API line, the `dataclasses` import line, the four loop-variable lines deviation D1 renames and the return statement. C4 is 217 insertions against ZERO deletions, which is constraint 8 MEASURED rather than asserted: no existing test was edited, renamed, deleted or skipped. EVERY SHIPPED FUNCTION WAS RUN BY THE REVIEWER RATHER THAN READ: all eight declared roles carry the evidence their class implies, `repair` answers None with no origin and answers `architecture` at the top tier and `format` at the cheap tier with one — different classes at different tiers, so inheritance is proven and not a constant — an undeclared role raises TWO UserWarnings, one per layer, and routes `undeclared_role` to the top tier with `unknown_class_conservative`, and a resolved config still hashes while equality still ignores the evidence. THE RED PROOF WAS RE-RUN IN FULL BY THE REVIEWER with FIVE mutations against the worker's four, in a disposable worktree at `8c57d0bc`, module path printed from inside it, primary checkout `git status --porcelain` read immediately after every mutation and CLEAN every time. Control 82 passed, exit 0, and every revert returned to 82. The reviewer's first four mutations reproduce the worker's counts EXACTLY — 6, 22, 2 and 3 — and a fifth, never attaching the evidence at all, reddens 32. DEVIATION D3 IS CORRECT AND THE REVIEWER CONFIRMS IT INDEPENDENTLY: the red sets are NOT pairwise disjoint, every pair intersects, and the "originating class dropped" set is a strict subset of the "role argument ignored" set. That is a REPORTABLE RESULT and not a fault — the block ordered the property MEASURED rather than assumed, every mutation is detected, the catch-removal mutation owns four ids no other reddens and the never-attach mutation owns ten, and the two inheritance fixtures use classes at DIFFERENT tiers so the inheriting path is pinned by value and not by constant. DEVIATIONS D1, D2, D4 AND D5 ARE ALL ACCEPTED. D1 renames a loop variable `field` to `field_name` so SPEC (b)'s `dataclasses.field` import is not shadowed, behaviour identical. D2 added a THIRD Public API line the block did not order, naming the new public function `resolve_routed_call_evidence`; the block's SPEC (f) named two and the round owed three, which is the reviewer's miscount and not the worker's — recorded in `.agent/prose_slips.md` this round. D4 declares that the worker's own red-proof harness first compared pytest summary lines INCLUDING elapsed time and printed a wrong "back to control" reading before it was corrected and the gate re-run; declaring the wrong first reading instead of quietly replacing it is exactly the behaviour to keep, and the reviewer's own harness failed the same way in the same round. D5 declares `docs/roadmap/features/T3_F110.md`'s T001 bullet stale-in-part and leaves it unrepaired, which constraint 9 requires for a sentence outside the change set. THE SUITES WERE RE-RUN BY THE REVIEWER at 82 passed for `test_role_config.py`, grown from 34, then 391 with 3 skipped, 87, 333, 295 and 42, every one exit 0 and every unmoved count matching the block. CONSTRAINT 6 WAS MEASURED, NOT ASSERTED: `git diff --stat 328228dc..8c57d0bc` over `docs/` is empty, and over `packages/` and `apps/` with the two edited files excluded is empty, so no call site was edited and the wiring reached all seven through the resolver they share. The per-commit insertion counts match the handback's Commits table cell by cell — 399, 356, 20, 67, 105, 217 — every one under the AGENTS.md cap; `a1368633` is 414 insertions against 648 deletions, a full-file rewrite of a single `.agent/**` state file and exempt under DECISION F104 D1. The open set is 278 over 347 registered and 69 resolved, UNCHANGED; the round minted no id and `R-0767` stays OPEN. The tree is clean, `git ls-files .remedy-wt` returns nothing, no worktree of the round's making survives, `.agent/candidates.md` is untouched and still EMPTY, and the branch is pushed at `a1368633` with no pull request open.
<<<END RECORD9>>>

<<<BEGIN SLIPS10>>>
2026-09-03 · F110 R9 · The round 9 block's SPEC (f) ordered the `role_config.py` Public API list to gain "a line for RoleConfig's new field and one for resolve_role_config's new parameter" — two — while the same block's SPEC (d) ordered a NEW PUBLIC FUNCTION into that module, so three were owed. The worker added the third, named it in deviation D2 and was right to. The reviewer enumerated the API additions from the two SPEC items that mentioned the docstring rather than from the round's whole set of new public names. THE LESSON: when a block enumerates what a docstring's Public API list must gain, derive that list from every public name the round ships, not from the SPEC items that happen to mention the docstring. Reviewer block-authoring slip, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F110 R9 · BOTH the worker's and the reviewer's red-proof harnesses mis-parsed pytest's own output in the same round, in different ways: the worker's compared summary lines INCLUDING the elapsed time and so reported a false "back to control" mismatch (its deviation D4), and the reviewer's took the FIRST whitespace-separated token of each "FAILED ..." line as the node id, collecting the literal string "FAILED" for every failure and producing a red-set intersection analysis that was an artifact of the parser rather than a measurement. Both were caught before anything landed — the worker re-ran the whole gate, and the reviewer printed one raw failing line and re-ran. THE LESSON: a harness that derives a SET from tool output prints one RAW line of that output beside its parsed result before any conclusion is drawn from it; a parsed set that is never checked against the bytes it came from is a measurement in appearance only. Reviewer and worker tooling slip, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIPS10>>>

<<<BEGIN DECISION5>>>
## DECISION F110 D5 (2026-09-03, round 10) — what a refused override map does

CONTEXT. Round 10 lets a project configure
`model_routing.task_class_tiers` in `remedy.toml`.
`build_effective_task_class_tiers` already REFUSES a map that breaks a hard
rule or promotes a class without benchmark evidence, raising
`OverrideRefused` with every violation. What the CONFIG layer does with that
refusal is a question round 6 deliberately left to the round that reads a
config file, and this is that round.

CHOSEN. The routing layer catches `OverrideRefused`, emits ONE `UserWarning`
naming the config key and EVERY violated rule, and routes against the
SHIPPED `TASK_CLASS_TIERS`. `validate_config` independently reports SHAPE
faults in the table, so `remedy config` surfaces a malformed table without
a routing call happening at all.

WHY. The hard rules WIN, which is what the feature file demands, and they
win the way `build_effective_task_class_tiers`'s own docstring says they
must — by refusing the config rather than by quietly editing it. The
offending override does not take effect, and the operator is told which rule
refused it rather than left to wonder why a setting did nothing. Routing
seeded is also the conservative direction: every hard rule this feature
enforces protects a class from being routed DOWN, so the shipped table is
never the cheaper answer, which matches the A9 default that over-spending
beats under-thinking.

REJECTED, AND WHY.
(1) RAISE, letting `OverrideRefused` escape `resolve_role_config`. Rejected:
    one typo in `remedy.toml` would then break every provider call in the
    project, because `resolve_role_config` is the function all seven
    inventoried call sites share. That is the round 9 lesson — a routing
    concern must not become a config-resolution fault — one layer further
    out, and it would make a policy guard into an outage.
(2) DROP ONLY THE OFFENDING ENTRIES and apply the rest. Rejected: a silently
    dropped override leaves the operator believing it took effect, which is
    the silent downgrade `docs/agents/model_routing_policy.md` hard rule 2
    exists to forbid, and `build_effective_task_class_tiers`'s docstring
    already rejects this reading in so many words.
(3) WARN BUT APPLY THE MAP ANYWAY. Rejected outright: it makes the hard
    rules advisory, and a rule that a config can override is not a hard rule.
(4) FAIL AT CONFIG LOAD, inside `load_config`. Rejected: `config.py` is the
    lower layer and is deliberately policy-free — it must not import
    `model_routing` to learn what a task class is. Shape validation belongs
    there and does; rule validation belongs where the rules live.

CONSEQUENCE. A project with a refused table still runs, on the shipped
policy, loudly. The warning is the operator-facing surface, so it names the
key and the rules rather than the exception type. Recording is still not
selecting: this round changes which TIER a call records, never which model
runs.

REVERSE THIS DECISION by deleting the `OverrideRefused` catch in
`packages/orchestration/role_config.py` and letting the exception propagate,
and by deleting this paragraph.
<<<END DECISION5>>>
