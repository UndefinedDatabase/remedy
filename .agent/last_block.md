STEP F110 T002b / ROUND 5 - F110 Model routing by task class
FEATURE F110 - Model routing by task class (Tier 3) - SESSION 1, ROUND 5

Goal
  Ship the THREE HARD RULES as named checks, each refusing with its own rule
  name, each with a violating fixture - the acceptance wording of
  docs/roadmap/features/T3_F110.md. Book round 4's PASS verdict in the same
  round.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f110-r5.md
  C0b mirror it to .agent/last_block.md
  C1  apply PLAN5 to .agent/plan.md (FIRST substantive commit, item 23)
  C2  append RECORD4 to .agent/live_review.md and SLIPS5 to
      .agent/prose_slips.md - round 4's verdict, booked
  C3  THE PRODUCTION COMMIT: the hard rules in model_routing.py
  C4  THE TEST COMMIT: the violating fixtures in test_model_routing.py
  C5  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f110-r5.md (new, C0a) · .agent/last_block.md (C0b) ·
  .agent/plan.md (C1) · .agent/live_review.md (C2) ·
  .agent/prose_slips.md (C2) ·
  packages/orchestration/model_routing.py (C3) ·
  tests/orchestration/test_model_routing.py (C4) · .agent/handoff.md (C5)

BASE for this round is 7a4d381f. Every byte and count below was measured there.
NO DOCS ARE EDITED. docs/agents/model_routing_policy.md is read, never written.

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by delimiter
     index from the COMMITTED .agent/authored/f110-r5.md - marker lines
     EXCLUDED - and write it with a script, never by retyping. If a slice looks
     wrong, apply it as written and DECLARE it in the handback.
  2. C1 is the first substantive commit; this round touches the finding ledger,
     so item 23 binds.
  3. C3 (production) precedes C4 (tests). Do not reorder.
  4. Newline conventions, MEASURED at 7a4d381f: .agent/live_review.md ends
     WITHOUT a trailing newline (2158520 bytes) and must still end without one
     after C2; .agent/prose_slips.md likewise ends WITHOUT one; .agent/plan.md
     ends WITH one. Each append is the two bytes newline newline then the slice.
     Where an extractor yields a trailing newline the target does not take, the
     TARGET's convention wins.
  5. NO RUFF GATE IS ORDERED and you must not add one; the reviewer lints it.
  6. NOTHING IS WIRED TO A CALL SITE THIS ROUND, and no config file is read or
     written. The checks are PURE FUNCTIONS over values passed to them. The
     config schema that calls them is T002c, the next round.
  7. THE EXISTING TABLE IS NOT EDITED. TASK_CLASS_TIERS, MODEL_TIERS,
     normalize_task_class and resolve_task_class_tier keep their current
     behaviour byte for byte in effect; round 4's sync test must still pass
     unchanged. You are ADDING to this module, not revising it.
  8. A sentence OUTSIDE the change set that this round makes stale is DECLARED
     in the handback and NOT repaired.
  9. Read .agent/STOP from disk before the first commit and again before C5.
  10. Self-review loop before every commit. Push after C5. No pull request, no
      merge. Destructive verification only inside a disposable git worktree.

SPEC CODE - additions to packages/orchestration/model_routing.py, written by YOU

  (a) TIER COMPARISON. A named helper giving a tier's RANK along MODEL_TIERS,
      so every rule below is an index comparison on the one ordered vocabulary
      rather than a second ranking. An unknown tier is a programming error, not
      a routing decision: raise rather than return a silent default, and say so
      in the docstring. Also expose the MID tier as a named constant derived
      from MODEL_TIERS, the way TOP_TIER already is - do not write the literal.

  (b) THE THREE RULE NAMES, as module-level string constants, because "refused
      with the rule named" means the caller receives a STABLE token and not a
      prose sentence. Name them for what they forbid.

  (c) SAFETY_RELEVANT_CLASSES, a frozenset that is EMPTY today. The policy
      document scopes this rule to "fence/DoD evaluation prompts, if any become
      LLM calls" and none is one yet. Document that emptiness as a DELIBERATE
      ABSENCE in the AGENTS.md discoverability idiom - a reader searching for
      why the safety rule never fires must land on the explanation - and state
      that the check takes the set as a PARAMETER defaulting to this constant,
      which is what lets its test prove the rule fires.

  (d) THE THREE CHECKS. Each takes the values it judges, returns the rule-name
      constant when the rule is VIOLATED, and returns None when it is not:
        - reviewer never weaker than the paired worker for the same task; equal
          is allowed and stronger is fine, so only strictly-weaker violates;
        - orchestrator and mission-compile calls always top tier;
        - a safety-relevant class never below mid.
      Each carries the one-line WHY comment above its def.

  (e) A COLLECTING VALIDATOR returning EVERY violated rule name for a candidate
      routing choice, in MODEL_TIERS-independent, stable order - not just the
      first. A config validation that reports one of three broken rules sends
      its operator round the loop three times.

  (f) ONE DOCSTRING SENTENCE settling a name collision the reviewer ruled on at
      the round 4 gate: packages/orchestration/orchestrator_brain.py already
      uses `tier` for an UNRELATED vocabulary (HUMAN_REVIEW_REQUIRED,
      EXTERNAL_BUILDER_NEEDED), surfacing as `model_routing_plan.tier` and
      `model_routing_tier`. NOTHING IS RENAMED - AGENTS.md forbids mass renames
      as their own activity - so this module's docstring names that other
      vocabulary and says which is which, so a reader searching "tier" lands on
      the distinction. Add the sentence; touch no other file.

  Extend the module docstring's Public API list with everything (a) through (e)
  adds. Round 4's list is the shape to follow.

SPEC TESTS - additions to tests/orchestration/test_model_routing.py
  (g) A VIOLATING FIXTURE PER RULE, refused WITH THE RULE NAMED - assert against
      the rule-name CONSTANT, never a retyped string literal, so a rename cannot
      leave a test asserting a dead token.
  (h) A CONFORMING case per rule, so each test pair discriminates rather than
      merely producing a refusal.
  (i) THE SAFETY RULE IS PROVEN NON-VACUOUS: pass a FIXTURE safety set so the
      check actually fires, and separately assert that the PRODUCTION constant
      is empty today - the emptiness is then a stated property with a test on
      it, not an accident nobody would notice changing.
  (j) THE COLLECTING VALIDATOR returns all three rule names for a choice that
      breaks all three, and an empty result for a conforming one.
  (k) The tier-rank helper RAISES for an unknown tier.
  Round 4's existing tests are not edited; this file only gains cases.

Done when - the gates. Run each, record the REAL exit code and the REAL output.

  G1 TRANSPORT. After C0b: sha256sum .agent/authored/f110-r5.md
     .agent/last_block.md - one digest twice, both lines verbatim. ALSO report
     wc -l .agent/authored/f110-r5.md; the reviewer's projection is 252 lines
     and the cap is 400. Report a difference, do not repair it.
  G2 THE PLAN. Extract PLAN5 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md          -> exit 0
       wc -l .agent/plan.md                    -> report; must be under 50
       grep -c '^## Goal' .agent/plan.md       -> 1
       grep -c '^## Next Steps' .agent/plan.md -> 1
  G3 THE LEDGER APPEND, full arithmetic, the record file. For RECORD4 at C2
     against the size immediately before that commit: report before + 2 + slice
     length, the real new size, and whether they are equal. Then a SECOND READER
     that counts no byte: split the WHOLE file on blank-line boundaries, let N be
     counted BY THE SCRIPT from the slice, and report whether the LAST N units
     equal the slice's N paragraphs IN ORDER. Then a NEGATIVE CONTROL: in a
     scratch copy flip one byte inside the FIRST appended paragraph and report
     that the second reader REJECTS it. Also report
     grep -c '^Gate: F110 R4 — ' .agent/live_review.md, 0 before C2 and 1 after.
  G4 THE PROSE FILE. Byte-equality check ONLY: report whether the final bytes of
     .agent/prose_slips.md equal the extracted SLIPS5 slice, whether the pre-C2
     content is preserved as an exact byte PREFIX, and whether the file still
     ends without a newline.
  G5 THE MODULE, MEASURED AND RUN. On packages/orchestration/model_routing.py:
       git show --numstat C3 -- <path>   -> report insertions AND deletions
       ast.parse over its real text       -> no exception
     The DELETIONS number is the one that matters here: constraint 7 forbids
     revising the round 4 table, so report it and say what each deleted line was
     if it is not zero. Then RUN THE SHIPPED CODE and report real answers:
       each of the three checks on a VIOLATING input and on a CONFORMING one
       the collecting validator on a choice breaking all three rules
       the tier-rank helper on each of the three tiers and on an unknown tier
       the value of the production safety-relevant class set
     Report what the functions RETURNED, not what they were meant to return.
  G6 THE RED PROOF, in a disposable git worktree at the C4 commit and NEVER in
     the primary checkout. Report the UNMUTATED CONTROL FIRST: run the test file,
     report exit code and count. Then make THREE separate mutations, reverting
     between each, one per rule: change that rule's check so it ALWAYS returns
     None - i.e. it never refuses. For each, report which test ids go RED.
     THE DISCRIMINATOR: each mutation must redden ITS OWN rule's violating
     fixture and the collecting-validator case, while the OTHER TWO rules'
     fixtures stay GREEN. A mutation that reddens everything, or nothing, is a
     FAILED proof - report it as such rather than reporting a colour. Purge
     __pycache__, run python3 -B, print the imported module's __file__ from
     inside the worktree, then remove the worktree and prune.
  G7 THE SUITES, EACH AS ITS OWN INVOCATION, RUN SERIALLY. Measured by the
     reviewer at 7a4d381f:
       python3 -m pytest tests/orchestration/test_model_routing.py -q     report the count; it was 48 and must GROW
       python3 -m pytest tests/orchestration/test_orchestrator_model_routing.py tests/orchestration/test_job_role_routing.py -q   33 passed
       python3 -m pytest tests/orchestration/test_role_config.py -q       34 passed
       python3 -m pytest tests/docs/ -q                                   295 passed
       python3 -m pytest tests/cli/test_golden_path.py -q                 42 passed
     A moved count in the last four is the finding. In the first, a count that
     did NOT grow means the new cases did not land.
  G8 THE TREE, THE COMMITS AND THE SWEEP. Read git status --porcelain
     immediately before C5 is staged, git ls-files .remedy-wt (no output), and
     git worktree list (no worktree of this round's own making). Confirm
     git diff --stat 7a4d381f..C4 -- docs/ lists NOTHING. Then, for C0a through
     C4 - the commits BEFORE the handback commit, per item 14 - report each
     one's insertion count from git show --numstat, the '+' column ONLY,
     compared CELL BY CELL against the Commits table of the handback you are
     writing. C5's own numbers go to neither a round report nor this file. Then
     THE STALENESS SWEEP over every file this round touched, one entry per file,
     stale or NOT stale, and why.

Handback
  Rewrite .agent/handoff.md per docs/agents/handback_template.md: SESSION 1 of
  F110, round 5, the state block, the item-status table with every ordered item
  appearing exactly once, the Commits table, one line per gate then the
  transcripts, the deviations, the next steps. No length cap. THIS IS THE LAST
  ROUND OF THE SESSION: the Next section names T002c as the next round and
  states that the branch has no open pull request, so the next session's Open PR
  Gate finds none.

SLICES. Each slice lies between its own one-line BEGIN and END marker. The
marker lines are NEVER part of the slice. The slices carried here are PLAN5,
RECORD4 and SLIPS5.

<<<BEGIN PLAN5>>>
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

Round 5, session 1 — T002b, the THREE HARD RULES the policy document and
`docs/roadmap/features/T3_F110.md` both name, each shipped as its own
named check that returns the rule's name when violated: a reviewer never
routed weaker than its paired worker, orchestrator and mission-compile
calls always top tier, and a safety-relevant class never below mid. Each
rule gets a violating fixture that is refused with the rule named, which
is the feature file's own acceptance wording. Round 4's PASS verdict is
booked in the same round.

## Next Steps

- T002c: the config schema and per-project overrides, where the hard
  rules always win and a violating override fails validation naming the
  rule — the checks this round ships are what that validation calls.
- T003: the promotion-evidence discipline, the evidence fields and the
  goldens — a promotion without evidence refused, with evidence logged.
- Then the per-call-site class declarations (consolidation order E.d),
  the integration gate, and the closure sequence, which also runs the one
  checklist consolidation pass DECISION F110 D1 carries into it.

## Risks

- The safety-relevant class set is EMPTY in production today, because the
  policy document scopes it to "fence/DoD evaluation prompts, if any
  become LLM calls" and none is one yet. The check is therefore proven
  against a fixture set so it is not a rule that can never fire.
- Nothing routes in production yet: the table and its rules are pinned
  before any call site declares a class (order E.d).
- `R-0767` stays OPEN on the same seam and must not be absorbed.
<<<END PLAN5>>>

<<<BEGIN RECORD4>>>
Gate: F110 R4 — the round 4 entry. VERDICT PASS, over the range `05d78941..7a4d381f`. THE TRANSPORT PROOF COVERS THE SAVED COPY AND ITS MIRROR AND NOTHING MORE (§3 item 37): one digest `5b0a124832fd1160e62eebc2fab359c93dfff966c7fef8971694c3e9acbd6dc2`. THE `wc -l` CLAUSE REPORTS 259 AGAINST A PROJECTION OF 259 — the first exact projection of this feature, after three consecutive rounds low by 1, 1 and 3, and it is exact because the reviewer recomputed the figure after its last edit instead of carrying the number written before it. EVERY SLICE WAS RE-DERIVED BYTE FOR BYTE BY THE REVIEWER: `.agent/plan.md` equals PLAN4; `.agent/live_review.md` equals its base plus two newlines plus RECORD3, still ending without a newline; `.agent/prose_slips.md` equals its base plus two newlines plus SLIPS4. THE MODULE IS WELL-BUILT AND THE REVIEWER READ IT: `packages/orchestration/model_routing.py` carries a Public API list in the shape `role_config.py` uses, states that `MODEL_TIERS` is ordered cheapest-first and that the ORDER IS LOAD-BEARING because round 5's hard rules are comparisons along it, and carries the deliberate-absence note AGENTS.md's discoverability section asks for — that a class is mapped to a TIER and never to a model id, because mixing the two would put the promotion discipline behind a casual table edit. `ruff check` over both new files answers "All checks passed!", run reviewer-side. THE SHIPPED CODE WAS RUN, not read: all ten documented classes answer their documented tier with the reason `seed_mapping`, an undocumented class answers `('top', 'unknown_class_conservative')` — the exact string `docs/roadmap/features/T3_F110.md`'s Edge-cases section specifies — and the normalizer maps "Standard Build" and "standard build" alike. THE SYNC TEST IS THE ROUND'S REAL DELIVERABLE AND THE REVIEWER RE-RAN ALL THREE MUTATIONS ITSELF in a disposable worktree at `7a4d381f`, with the module path printed from inside it. Control: 48 passed, exit 0. Mutation (i), the code table's `boilerplate` moved from cheap to mid: 1 failed, 47 passed, the red id being `TestPolicyDocumentSyncTest::test_the_parsed_seed_mapping_equals_the_module_table`. Mutation (ii), the WORKTREE's copy of the policy document changed from `summarize` to `summarise`: the SAME id red, 1 failed and 47 passed — so the test notices DOCUMENT drift as well as CODE drift, which is what makes it a sync test rather than half of one. THE THIRD MUTATION IS THE ONE WORTH RECORDING AND THE WORKER RAN IT UNORDERED, ON ITS OWN INITIATIVE: adding a SECOND non-arrow rule bullet to the document reddens three bullet-structure assertions — the four-bullet count, the one-rule count and the rule's text — WHILE `test_the_parsed_seed_mapping_equals_the_module_table` STAYS GREEN. The reviewer reproduced that exactly, at 3 failed and 45 passed. It is the direct proof that a sync test which silently filtered non-mapping bullets would have passed over a newly added policy RULE, which is the blind spot the block's SPEC TESTS (e) was written to forbid; the worker demonstrating it rather than asserting it is the behaviour this record exists to reward. THE SUITES WERE RE-RUN BY THE REVIEWER at 48, 33, 34, 295 and 42, every one exit 0; the four routing suites together are 115 and `tests/docs/` is unmoved at 295, which matters because this round's test READS a file under `docs/`. THE PRIMARY COPY OF THE POLICY DOCUMENT IS UNTOUCHED: `git diff --stat 05d78941..7a4d381f -- docs/` lists nothing, so mutation (ii) lived and died inside the worktree. CONSTRAINT 7 HOLDS AND WAS MEASURED: nothing outside its own test imports the new module, so the table is pinned before anything routes through it. A DISAGREEMENT THE REVIEWER MUST SETTLE, BECAUSE IT CONCERNS A FIGURE THIS RECORD HAS CARRIED THREE TIMES. Deviation D4 reports the worker's own open-set script reading 65 resolved and 282 open where rounds 2 and 3 stated 69 and 278. THE REVIEWER RECOMPUTED IT UNDER FIVE INDEPENDENT READINGS — a strict `^- R-\d+ . ` registration match, a loose `^- R-\d+\b` one, a strict `^Done: R-\d+ . ` resolution match, a loose `^Done: R-\d+\b` one, and the FIRST-R-id-per-`Done:`-line reading that F109's round 20 entry pinned as this ledger's canonical one — and ALL FIVE agree: 347 distinct registered, 69 distinct resolved across 71 `Done:` lines, 278 open by set difference, with every resolved id also registered and no non-standard `Done:` line anywhere in the file. THE FIGURE 278 STANDS and the rounds that stated it were right. The worker's script has a defect its report does not expose, and the worker was CORRECT to report the delta it could reproduce — zero movement between base and head — while declining to overwrite a figure it could not; that is the honest form of a disagreement and it cost nothing. DEVIATION D9 IS A REAL DISCOVERABILITY FINDING AND THE REVIEWER RULES ON IT HERE: `packages/orchestration/orchestrator_brain.py` already uses the word `tier` for a DIFFERENT vocabulary — `HUMAN_REVIEW_REQUIRED`, `EXTERNAL_BUILDER_NEEDED` — surfacing as `model_routing_plan.tier` and `model_routing_tier` across the ledger, the review bundle, the UI server and the CLI. NOTHING IS RENAMED: AGENTS.md's discoverability section forbids mass renames of existing code as their own activity, and the two vocabularies do not collide literally, because this feature's names are `MODEL_TIERS` and `TASK_CLASS_TIERS` while that one's live on a dataclass field. The counter-measure is a sentence, not a rename, and round 5 adds it to `model_routing.py`'s own docstring so a reader searching for "tier" lands on the distinction instead of on the wrong vocabulary. THE OPEN SET IS 278, unchanged, over 347 registered and 69 resolved. THE TREE is clean, `git ls-files .remedy-wt` returns nothing, no worktree of the round's own making survives, the eight committed paths are exactly the change set, and the branch is pushed at `7a4d381f`.
<<<END RECORD4>>>

<<<BEGIN SLIPS5>>>
2026-09-03 · F110 R4 · The worker's own open-set script read 65 resolved and 282 open against `.agent/live_review.md`, where rounds 2 and 3 had stated 69 and 278; the reviewer recomputed under five independent readings — strict and loose registration matches, strict and loose `Done:` matches, and the first-R-id-per-`Done:`-line reading F109 round 20 pinned as canonical — and all five agree on 347 registered, 69 resolved across 71 `Done:` lines and 278 open, with every resolved id also registered and no non-standard `Done:` line in the file. The stated figure was right and the worker's script carries a defect its report does not expose. It cost nothing, because the worker reported the DELTA it could reproduce (zero movement between base and head) and declined to overwrite a figure it could not — which is the honest form of a disagreement and the behaviour to keep. Worker measurement slip, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIPS5>>>
