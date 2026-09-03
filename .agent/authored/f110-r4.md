STEP F110 T002a / ROUND 4 - F110 Model routing by task class
FEATURE F110 - Model routing by task class (Tier 3) - SESSION 1, ROUND 4

Goal
  Land the CLASS TABLE that F110 exists for: a task class maps to a model tier,
  seeded from docs/agents/model_routing_policy.md, with the policy-document SYNC
  TEST the feature file names as an explicit acceptance line. Book round 3's
  PASS verdict in the same round.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f110-r4.md
  C0b mirror it to .agent/last_block.md
  C1  apply PLAN4 to .agent/plan.md (FIRST substantive commit, item 23)
  C2  append RECORD3 to .agent/live_review.md and SLIPS4 to
      .agent/prose_slips.md - round 3's verdict, booked
  C3  THE PRODUCTION COMMIT: packages/orchestration/model_routing.py
  C4  THE TEST COMMIT: tests/orchestration/test_model_routing.py
  C5  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f110-r4.md (new, C0a) · .agent/last_block.md (C0b) ·
  .agent/plan.md (C1) · .agent/live_review.md (C2) ·
  .agent/prose_slips.md (C2) ·
  packages/orchestration/model_routing.py (new, C3) ·
  tests/orchestration/test_model_routing.py (new, C4) ·
  .agent/handoff.md (C5)

BASE for this round is 05d78941. Every byte and count below was measured there.
THIS ROUND WRITES NO DOCS: docs/agents/model_routing_policy.md is READ by the
sync test and is NOT edited. It is not in the change set.

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by delimiter
     index from the COMMITTED .agent/authored/f110-r4.md - marker lines
     EXCLUDED - and write it with a script, never by retyping. If a slice looks
     wrong, apply it as written and DECLARE it in the handback.
  2. C1 is the first substantive commit; this round touches the finding ledger,
     so item 23 binds.
  3. C3 (production) precedes C4 (tests). Do not reorder.
  4. Newline conventions, MEASURED at 05d78941: .agent/live_review.md ends
     WITHOUT a trailing newline (2153907 bytes) and must still end without one
     after C2; .agent/prose_slips.md likewise ends WITHOUT one; .agent/plan.md
     ends WITH one. Each append is the two bytes newline newline then the slice.
     Where an extractor yields a trailing newline the target does not take, the
     TARGET's convention wins.
  5. NO RUFF GATE IS ORDERED and you must not add one; the reviewer lints C3 and
     C4 itself. Write to the repository's existing style, say nothing of lint.
  6. NO HARD RULES THIS ROUND. The feature file's three hard rules - reviewer
     never weaker than its paired worker, orchestrator and mission-compile
     always top tier, safety-relevant classes never below mid - are ROUND 5 and
     are deliberately out of scope here. Do not implement, stub or name them in
     code. This round ships the TABLE and its sync test; adding an unenforced
     rule would put a claim on disk this round cannot prove.
  7. NOTHING IS WIRED TO A CALL SITE THIS ROUND. `model_routing.py` is imported
     by its test and by nothing else. That is deliberate: consolidation order
     E.d puts the per-call-site class declarations after the seam work, and the
     seam work is not finished. Do not edit any caller.
  8. A sentence OUTSIDE the change set that this round makes stale is DECLARED
     in the handback and NOT repaired.
  9. Read .agent/STOP from disk before the first commit and again before C5. If
     it exists, finish the commit in hand, write the handback, and stop.
  10. Self-review loop before every commit. Push after C5. No pull request, no
     merge. Destructive verification only inside a disposable git worktree.

SPEC CODE - NEW FILE packages/orchestration/model_routing.py, written by YOU
  The module owns the class-to-tier table and nothing else yet. It must carry:

  (a) THE TIER VOCABULARY. The three tiers the policy document names, in
      cheapest-to-strongest order, as a module-level tuple. Their order is
      load-bearing for round 5's hard rules, so it is stated once and the module
      docstring says the order is significant.

  (b) `normalize_task_class(phrase: str) -> str`. The ONE documented
      normalization both the code table and the sync test use: strip, lowercase,
      and collapse each run of whitespace to a single underscore. It exists so
      the doc's own phrases - "standard build", "prompt authoring for other
      agents" - become table keys WITHOUT a lossy rename, which is what lets the
      sync test be a straight set comparison instead of a translation.

  (c) THE CLASS TABLE, seeded from the policy document's "Seed mapping" section.
      The reviewer parsed that section at 05d78941 and it yields exactly these
      pairs, which your table must equal: format, extract, summarize and
      boilerplate at the cheap tier; standard_build and standard_review at mid;
      architecture, mission, vision and prompt_authoring_for_other_agents at
      top. Do not add a class the document does not name. Do not rename one.

  (d) `resolve_task_class_tier(task_class: str) -> tuple[str, str]` returning
      `(tier, reason)`. A known class returns its tier with a reason naming the
      seed mapping. An UNKNOWN class returns the TOP tier with the reason
      exactly `unknown_class_conservative` - the string
      docs/roadmap/features/T3_F110.md's "Edge cases & assumption defaults"
      section specifies, because over-spending beats under-thinking. Normalize
      the argument through (b) before lookup, so "Standard Build" and
      "standard_build" resolve alike.

  Carry the one-line WHY comment above each definition per AGENTS.md Code
  Discoverability, and a module docstring with a Public API list in the shape
  packages/orchestration/role_config.py already uses.

SPEC TESTS - NEW FILE tests/orchestration/test_model_routing.py
  (e) THE SYNC TEST, which the feature file's Acceptance section names: parse
      docs/agents/model_routing_policy.md's "Seed mapping" section and assert
      the parsed mapping EQUALS the module's table. The reviewer dry-ran this
      parse at 05d78941: take the lines between the "## Seed mapping" heading
      and the "## Hard rules" heading that begin with "- "; there are FOUR such
      bullets; THREE contain the character U+2192 and one does not. For each
      arrow bullet, the left side split on "/" gives the class phrases and the
      first word of the right side gives the tier. That yields the ten pairs
      SPEC CODE (c) lists.
      THE FOURTH BULLET IS THE PART THAT MUST NOT BE SILENTLY SKIPPED: it reads
      "- Repair prompts follow the tier of the original task class." and is a
      RULE, not a mapping. Assert explicitly that exactly one non-arrow bullet
      exists AND that its text is that sentence, so a future editor who adds a
      second rule bullet turns this test red instead of having it ignored. A
      sync test that filtered non-arrow bullets away silently would pass over
      exactly the change it exists to catch.
  (f) UNIT TESTS for the rest: every table class resolves to its documented
      tier; an unknown class resolves to the TOP tier with the reason exactly
      `unknown_class_conservative`; the normalizer maps "Standard Build",
      "standard build" and "standard_build" to one key; the tier tuple is in
      cheapest-to-strongest order and every table value is a member of it.
      Do not assert any model id anywhere - this round maps classes to TIERS,
      not to models.

Done when - the gates. Run each, record the REAL exit code and the REAL output.

  G1 TRANSPORT. After C0b: sha256sum .agent/authored/f110-r4.md
     .agent/last_block.md - one digest twice, both lines verbatim. ALSO report
     wc -l .agent/authored/f110-r4.md; the reviewer's projection is 259 lines
     and the cap is 400. Report a difference, do not repair it.
  G2 THE PLAN. Extract PLAN4 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md          -> exit 0
       wc -l .agent/plan.md                    -> report; must be under 50
       grep -c '^## Goal' .agent/plan.md       -> 1
       grep -c '^## Next Steps' .agent/plan.md -> 1
  G3 THE LEDGER APPEND, full arithmetic, the record file. For RECORD3 at C2
     against the size immediately before that commit: report before + 2 + slice
     length, the real new size, and whether they are equal. Then a SECOND READER
     that counts no byte: split the WHOLE file on blank-line boundaries, let N be
     counted BY THE SCRIPT from the slice, and report whether the LAST N units
     equal the slice's N paragraphs IN ORDER. Then a NEGATIVE CONTROL: in a
     scratch copy flip one byte inside the FIRST appended paragraph and report
     that the second reader REJECTS it. Also report
     grep -c '^Gate: F110 R3 — ' .agent/live_review.md, 0 before C2 and 1 after.
  G4 THE PROSE FILE. Byte-equality check ONLY: report whether the final bytes of
     .agent/prose_slips.md equal the extracted SLIPS4 slice, whether the pre-C2
     content is preserved as an exact byte PREFIX, and whether the file still
     ends without a newline.
  G5 THE MODULE, MEASURED AND RUN. On packages/orchestration/model_routing.py:
       git show --numstat C3 -- <path>        -> report insertions
       ast.parse over its real text            -> no exception
     Then RUN THE SHIPPED CODE and report the real answers, not the intent:
       resolve_task_class_tier for each of the ten documented classes
       resolve_task_class_tier("a_class_the_document_does_not_name")
       normalize_task_class for "Standard Build", "standard build", "  MISSION  "
     The unknown case must report the top tier and the exact reason string.
  G6 THE SYNC TEST'S RED PROOF, in a disposable git worktree at the C4 commit
     and NEVER in the primary checkout. Report the UNMUTATED CONTROL FIRST: run
     the new test file, report exit code and count. Then, INSIDE THE WORKTREE,
     make TWO separate mutations and report each one's reddened ids, reverting
     between them:
       (i)  change one class's tier in model_routing.py's table
       (ii) change one class phrase in the WORKTREE's copy of
            docs/agents/model_routing_policy.md
     THE DISCRIMINATOR: the sync test must go RED for BOTH, because a sync test
     that only notices code drift is half a sync test. Report which ids redden
     in each case. If either mutation leaves the sync test green, that is a
     FAILED proof - report it as such rather than reporting a colour. Purge
     __pycache__, run python3 -B, print the imported module's __file__ from
     inside the worktree, then remove the worktree and prune.
  G7 THE SUITES, EACH AS ITS OWN INVOCATION, RUN SERIALLY. Measured by the
     reviewer at 05d78941:
       python3 -m pytest tests/orchestration/test_model_routing.py -q            report the count
       python3 -m pytest tests/orchestration/test_orchestrator_model_routing.py tests/orchestration/test_job_role_routing.py -q   33 passed
       python3 -m pytest tests/orchestration/test_role_config.py -q              34 passed
       python3 -m pytest tests/docs/ -q                                          295 passed
       python3 -m pytest tests/cli/test_golden_path.py -q                        42 passed
     tests/docs/ is run because this round's test READS a file under docs/; a
     moved count there, or in the 33, the 34 or the 42, is the finding.
  G8 THE TREE, THE COMMITS AND THE SWEEP. Read git status --porcelain
     immediately before C5 is staged, git ls-files .remedy-wt (no output), and
     git worktree list (no worktree of this round's own making). Confirm
     docs/agents/model_routing_policy.md is UNCHANGED in the primary checkout -
     git diff --stat 05d78941..C4 must not list it. Then, for C0a through C4 -
     the commits BEFORE the handback commit, per item 14 - report each one's
     insertion count from git show --numstat, the '+' column ONLY, compared CELL
     BY CELL against the Commits table of the handback you are writing. C5's own
     numbers go to neither a round report nor this file. Then THE STALENESS
     SWEEP over every file this round touched, one entry per file, stale or NOT
     stale, and why.

Handback
  Rewrite .agent/handoff.md per docs/agents/handback_template.md: SESSION 1 of
  F110, round 4, the state block, the item-status table with every ordered item
  appearing exactly once, the Commits table, one line per gate then the
  transcripts, the deviations, the next steps. No length cap.

SLICES. Each slice lies between its own one-line BEGIN and END marker. The
marker lines are NEVER part of the slice. The slices carried here are PLAN4,
RECORD3 and SLIPS4.

<<<BEGIN PLAN4>>>
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

Round 4, session 1 — T002a, the class table itself. A new module
`packages/orchestration/model_routing.py` maps each task class the policy
document names to a model tier, and a SYNC TEST parses that document and
asserts the two agree — the acceptance line
`docs/roadmap/features/T3_F110.md` calls out by name. An unknown class
routes to the top tier with the reason `unknown_class_conservative`.
Round 3's PASS verdict is booked in the same round.

## Next Steps

- T002b: the three hard rules, each a named check with a violating fixture
  that is refused with the rule named — reviewer never weaker than its
  paired worker, orchestrator and mission-compile always top tier,
  safety-relevant classes never below mid. Deliberately NOT in round 4:
  an unenforced rule on disk is a claim its round cannot prove.
- T002c: the config schema and per-project overrides, where hard rules
  always win and a violating override fails validation naming the rule.
- T003: the promotion-evidence discipline, the evidence fields and the
  goldens — a promotion without evidence refused, with evidence logged.
- Then the per-call-site class declarations (consolidation order E.d),
  the integration gate, and the closure sequence, which also runs the one
  checklist consolidation pass DECISION F110 D1 carries into it.

## Risks

- The table is not wired to any call site yet, by design: E.d puts the
  declarations after the seam work. Nothing routes in production today.
- `apps/cli/commands/mission_cmd.py`'s `_orchestrator_call_fn` docstring
  went half-stale in round 3 and needs a later round's change set.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
<<<END PLAN4>>>

<<<BEGIN RECORD3>>>
Gate: F110 R3 — the round 3 entry. VERDICT PASS, over the range `490f575f..05d78941`. THE TRANSPORT PROOF COVERS THE SAVED COPY AND ITS MIRROR AND NOTHING MORE (§3 item 37): one digest `187c2d573e7cf04079ef52b2310007abc69c4706519335cc545dbc0ec33d536c` over `.agent/authored/f110-r3.md` and `.agent/last_block.md`. THE NEW `wc -l` CLAUSE EARNED ITSELF ON ITS FIRST OUTING: the committed block is 236 lines against the reviewer's stated projection of 233, so the projection was wrong for the THIRD consecutive round and this is the first round in which the round itself said so rather than the reviewer discovering it afterwards. The §3 item 1 cap of 400 was met with room, and the clause is now standing practice. EVERY SLICE WAS RE-DERIVED BYTE FOR BYTE BY THE REVIEWER: `.agent/plan.md` equals PLAN3; `.agent/live_review.md` equals its base plus two newlines plus RECORD2 and still ends without a newline; `.agent/prose_slips.md` equals its base plus two newlines plus SLIPS3, base preserved as an exact byte PREFIX. THE PRODUCTION CHANGE IS A ONE-FOR-ONE IMPORT SWAP AND THE REVIEWER READ ALL THREE DIFFS: `packages/orchestration/role_config.py` gains `resolve_orchestrator_model` and its Public API docstring line, while `packages/orchestration/gauntlet_runner.py` and `apps/cli/commands/mission_cmd.py` each trade a function-local `get_config` import for a `resolve_orchestrator_model` import and pass that call as `model=`. THE IMPORT REMOVAL WAS THE ROUND'S ONE REAL RISK AND IT IS CLEAN: `grep get_config` returns NOTHING in either file afterwards, and both modules import successfully, so the removal took a genuinely dead local import rather than a live one. `ruff check` over all four changed files answers "All checks passed!", run REVIEWER-SIDE because the worker's permission layer refuses the tool. THE MUTATION RED PROOF WAS RE-RUN BY THE REVIEWER WITH A DELIBERATELY DIFFERENT MUTANT, which is stronger evidence than reproducing the worker's: where the worker returned `_DEFAULT_MODEL` and measured 14 failed against 5 passed, the reviewer made the fall-through call `_resolve_model(None)` and measured 15 failed against 4 passed at exit 1, the extra red being a shape check that the reviewer's harsher mutant also breaks. THE DISCRIMINATOR IS THE CLAIM THAT MATTERS AND IT HOLDS UNDER BOTH: every reddened id is an unset-key fall-through case, and `TestConfiguredKeyWins` runs 2 passed under the reviewer's mutant, so the proof separates the defect from its neighbour rather than merely producing a colour. The worker's deviation D2 is honest in the same way round 2's was — it named the shape checks that cannot discriminate instead of counting them as evidence. THE SHIPPED FUNCTION WAS RUN, not read: with the key unset it answers `muse-glimmer:latest`, which is exactly `resolve_role_config("orchestrator").model`. THE SUITES WERE RE-RUN BY THE REVIEWER at 298, 33 and 42, every one exit 0, with the 33 being the two resolver suites together; no count moved. THE OPEN SET IS UNCHANGED AT 278 over 347 distinct registered ids and 69 distinct resolved, which is correct because this round resolved nothing and registered nothing. A REVIEWER FAULT THIS RECORD OWES, and it is the block's, not the round's: gate G5 demanded the production change be "the new function, its docstring entry, and the two model arguments - nothing else", while SPEC CODE (b) of the SAME block explicitly permitted removing a `get_config` import that became unused. Those two clauses cannot both be obeyed, the worker obeyed the gate's narrower reading for everything else and declared the consequence, and the consequence is deviation D3: `_orchestrator_call_fn`'s docstring in `apps/cli/commands/mission_cmd.py` still says the call_fn is bound to "the model named by `orchestrator.model`", which is now only half the truth. Nothing on disk is wrong that a reader would be misled by into a defect, the sentence is stale rather than false, and it is repaired by naming that file in a later round's change set rather than by a round of its own. DEVIATION D6 IS ACCEPTED AND WAS THE SPEC'S GAP, NOT THE WORKER'S: a configured value that is non-blank but carries surrounding whitespace is returned VERBATIM rather than stripped, and a non-string value is treated as unset. Both are tested, both are declared, and returning the operator's own bytes unaltered is the defensible reading of a configuration surface. THE TREE is clean, `git ls-files .remedy-wt` returns nothing, no worktree of the round's own making survives, the ten committed paths are exactly the change set, and the branch is pushed at `05d78941`.
<<<END RECORD3>>>

<<<BEGIN SLIPS4>>>
2026-09-03 · F110 R3 · The reviewer's own step block contradicted itself between two clauses: SPEC CODE (b) explicitly permitted removing a `get_config` import that became unused, while gate G5 required the production change to be "the new function, its docstring entry, and the two model arguments - nothing else". The worker removed the two genuinely dead imports as the SPEC directed, reported the resulting counts, and declared the conflict instead of silently choosing; the reviewer confirmed both files still import and that `grep get_config` returns nothing in either. The checklist neighbour is §3 item 35, which requires a block's prose and its enumeration to be read against each other. Reviewer-prose contradiction between a SPEC and a gate of one block, nothing wrong on disk and the intended change landed; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F110 R3 · The reviewer's pre-emission line projection was wrong for the third consecutive round — 233 stated against a committed 236 — but this is the first round in which the ROUND caught it rather than the reviewer noticing afterwards, because the `wc -l` clause SLIPS3 instituted ran as gate G1 and reported the real count beside the projection. Recorded as evidence that the counter-measure works and should stay, not as a fresh defect. Reviewer-prose miscount, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIPS4>>>
