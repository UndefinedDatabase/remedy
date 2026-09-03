STEP F110 T003 / ROUND 7 - F110 Model routing by task class
FEATURE F110 - Model routing by task class (Tier 3) - SESSION 2, ROUND 7

Goal
  Ship the PROMOTION-EVIDENCE DISCIPLINE: moving a class to a CHEAPER tier is
  refused unless a documented benchmark run backs it, the bars come from the
  policy document rather than from a hand-typed number, and every routed call
  can report which evidence promoted it. The feature file's T003 wording is "a
  promotion without evidence refused, with evidence logged". Book round 6's PASS
  verdict and its two prose slips in the same round.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f110-r7.md
  C0b mirror it to .agent/last_block.md
  C1  apply PLAN7 to .agent/plan.md (FIRST substantive commit, item 23)
  C2  append RECORD6 to .agent/live_review.md and SLIPS7 to
      .agent/prose_slips.md - round 6's verdict and the reviewer's own slips
  C3  THE PRODUCTION COMMIT: the promotion-evidence discipline
  C4  THE TEST COMMIT: refused without evidence, accepted with it, and the
      policy-document sync test over the promotion rule
  C5  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f110-r7.md (new, C0a) · .agent/last_block.md (C0b) ·
  .agent/plan.md (C1) · .agent/live_review.md (C2) ·
  .agent/prose_slips.md (C2) · packages/orchestration/model_routing.py (C3) ·
  tests/orchestration/test_model_routing.py (C4) · .agent/handoff.md (C5)

BASE for this round is c1a3a3c4. Every byte, count, citation and red id below was
measured there by the reviewer. NO DOCS ARE EDITED.
docs/agents/model_routing_policy.md is READ by the new sync test, never written.

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by delimiter
     index from the COMMITTED .agent/authored/f110-r7.md - marker lines
     EXCLUDED - and write it with a script, never by retyping. If a slice looks
     wrong, apply it as written and DECLARE it in the handback.
  2. C1 is the first substantive commit; this round touches the finding ledger,
     so item 23 binds.
  3. C3 (production) precedes C4 (tests). Do not reorder.
  4. Newline conventions, MEASURED at c1a3a3c4. .agent/live_review.md is 2168965
     bytes and ends WITHOUT a trailing newline; it must still end without one
     after C2, and its append is the two bytes newline newline then the slice.
     .agent/prose_slips.md is 53495 bytes and likewise ends WITHOUT one, with the
     same two-byte append. .agent/plan.md ends WITH one. Where an extractor
     yields a trailing newline the target does not take, the TARGET's convention
     wins - and round 6's G4 is the reason this sentence is here.
  5. NO RUFF GATE IS ORDERED and you must not add one; the reviewer lints it.
  6. NO CONFIG FILE IS READ OR WRITTEN and packages/orchestration/config.py is
     neither edited nor imported, exactly as in round 6. Nothing is wired to a
     call site. The evidence map, like the override map, is PASSED IN.
  7. ROUND 6'S BEHAVIOUR IS PRESERVED UNDER ITS OWN CALLS. The new evidence
     parameter of the override validator and of the effective-table builder is
     OPTIONAL and defaults to no evidence, so every round-6 call - including a
     two-positional-argument one - answers exactly what it answered at c1a3a3c4.
     TASK_CLASS_TIERS, MODEL_TIERS, HARD_RULE_NAMES, OVERRIDE_SCHEMA_RULE_NAMES,
     normalize_task_class, resolve_task_class_tier,
     resolve_task_class_tier_with_overrides, model_tier_rank, the hard-rule
     checks and validate_routing_choice all keep their current behaviour.
  8. EXACTLY THE EXISTING TESTS NAMED IN SPEC TESTS (o) ARE EDITED, and each is
     WIDENED rather than weakened. No other existing test is edited, renamed,
     deleted or skipped.
  9. A sentence OUTSIDE the change set that this round makes stale is DECLARED in
     the handback and NOT repaired. A sentence INSIDE a file this round edits
     that this round's own commit falsifies IS repaired in that commit.
  10. Read .agent/STOP from disk before the first commit and again before C5.
  11. Self-review loop before every commit. Push after C5. No pull request, no
      merge. Destructive verification only inside a disposable git worktree.
      NEVER `cd` into that worktree for any purpose: address it by absolute path,
      run pytest as `python3 -B -m pytest <abs-worktree>/tests/...`, and run
      `git status --porcelain` in the primary checkout immediately after every
      mutation, in the same step, not at cleanup.

SPEC CODE - additions to packages/orchestration/model_routing.py, written by YOU

  (a) THE PROMOTION BARS, AS NAMED CONSTANTS: the minimum runs per fixture, the
      minimum block-level assertion pass rate, and the minimum overall pass rate.
      Each carries the sentence of docs/agents/model_routing_policy.md's
      "Promotion rule" section it comes from. They are SEEDED from that document
      and pinned to it by the sync test of (j), exactly as the class table is
      pinned to the "Seed mapping" section - so lowering a bar in code without
      lowering it in the policy is a red test rather than a quiet saving.

  (b) THE DOCUMENT'S OWN FIELD LIST, as a tuple: the names the "logged per run"
      bullet of that section carries, normalized through normalize_task_class.
      That bullet holds ONE COMPOUND PHRASE, "model id + quantization", which is
      SPLIT ON " + " before normalizing; declare that split at the constant,
      because it is the only translation between the document and the code and a
      silent one would turn the sync test into a tautology.

  (c) THE EVIDENCE RECORD - a frozen dataclass carrying every name in (b), plus
      the runs-per-fixture count and the corpus the run was measured on. State
      WHY those last two are NOT in (b): the document names them in its prose and
      not in its logged-per-run bullet, and pretending otherwise would make the
      sync test assert something the document does not say.

  (d) THE THREE PROMOTION RULE NAMES, as module-level string constants: a
      promotion with NO evidence, evidence that is present but INCOMPLETE, and
      evidence that is complete but BELOW a bar of (a). Collect them in their own
      tuple, in that order, and extend the override report order to the schema
      names, then the hard-rule names, then these.
      WHY THEY ARE THEIR OWN CLASS AND NOT HARD RULES: a hard rule is never
      satisfiable by evidence - no benchmark buys a reviewer weaker than its
      worker - while a promotion rule is precisely a rule EVIDENCE DISCHARGES.
      Merging the two would let a measured, documented promotion read as a policy
      breach. HARD_RULE_NAMES and OVERRIDE_SCHEMA_RULE_NAMES are both left
      exactly as they are.

  (e) THE PROMOTION PREDICATE: given a task class and a candidate tier, is this a
      PROMOTION? True only when the candidate tier ranks STRICTLY BELOW the seed
      table's tier for that class. False for a class the seed table does not name
      - that is a schema fault, not a promotion - and False for a move to an
      equal or stronger tier. WHY ONLY CHEAPER: the policy's promotion rule is
      about spending less, and a move to a STRONGER tier costs money rather than
      quality, so it needs no benchmark to justify it.

  (f) THE PROMOTION CHECK, returning ITS OWN rule name when violated and None
      when not, the shape every check in this module shares. It returns None
      outright when (e) says the change is not a promotion. Otherwise: no
      evidence at all gives the WITHOUT-EVIDENCE name; evidence with any document
      field of (b) unset gives the INCOMPLETE name; evidence whose runs or either
      pass rate falls below its bar of (a) gives the BELOW-THRESHOLD name. One
      one-line WHY comment above the def.

  (g) THE OVERRIDE VALIDATOR GAINS AN OPTIONAL EVIDENCE MAP - task class to the
      record of (c) - defaulting to no evidence. It reports promotion violations
      AFTER the hard rules, attributed to the promoted class. Constraint 7 binds:
      nothing else about that function changes, and a caller that supplies no
      evidence map gets round 6's answers unchanged.

  (h) THE EFFECTIVE-TABLE BUILDER GAINS THE SAME OPTIONAL PARAMETER and passes it
      through, so a promotion without evidence is REFUSED by the same exception
      that already refuses a hard-rule breach. The hard rules and the promotion
      discipline win the same way: by refusing the config, not by editing it.

  (i) THE EVIDENCE FIELDS, as a function returning the mapping a routed call
      records: the task class, the tier, the reason, and WHAT PROMOTED IT - None
      when the class was not promoted, and otherwise a reference locating the
      benchmark run rather than a copy of the whole record. Tier and reason come
      from resolve_task_class_tier_with_overrides and are never recomputed here,
      so the two can never disagree. This is the feature file's Evidence line:
      "routed_model, tier, reason on every call".

  Extend the module docstring's Public API list with everything (a) through (i)
  adds, and say in the docstring that the promotion bars are SEEDED from the
  policy document's "Promotion rule" section the way the table is seeded from its
  "Seed mapping" section. Round 6's list is the shape to follow.

SPEC TESTS - additions to tests/orchestration/test_model_routing.py
  (j) THE PROMOTION-RULE SYNC TEST, and it is this round's real deliverable. It
      parses the "Promotion rule" section of the policy document and asserts the
      parsed runs count and the two parsed percentages EQUAL the constants of
      (a), and that the parsed logged-per-run list EQUALS the tuple of (b).
      PARSE THE BULLETS, joining each bullet's own continuation lines, the way
      the seed-mapping parser already in this file does. A regex over the whole
      section text instead swallows the paragraph that follows the last bullet
      and yields nonsense fields - the reviewer ran exactly that at c1a3a3c4 and
      got a "field" reading "the class stays on the stronger tier. Re-run on
      model version change ...", so this is a measured trap and not a caution.
      Pin the bullet count, and assert every name in (b) is a real field of the
      record of (c).
  (k) A PROMOTION WITHOUT EVIDENCE IS REFUSED WITH THE RULE NAMED, and the SAME
      promotion WITH sufficient evidence is accepted - the feature file's own
      T003 wording, as one discriminating pair.
  (l) INCOMPLETE evidence and BELOW-THRESHOLD evidence are each refused with
      THEIR OWN rule name. One case per bar of (a), each tested JUST BELOW the
      bar and JUST AT it, so the boundary is pinned rather than guessed.
  (m) A move to a STRONGER tier is accepted with no evidence at all; a class the
      seed table does not name is a SCHEMA fault and never a promotion rule; and
      an override restating a class's seed tier is not a promotion either.
  (n) THE EVIDENCE FIELDS: the function of (i) returns exactly the declared keys,
      with the promoted-by key None for an unpromoted class and naming the run
      for a promoted one. Include a GOLDEN - one fully specified promoted call's
      evidence mapping asserted as an EXACT dict - so a renamed, dropped or added
      key is red rather than merely different.
  (o) THE WIDENED GUARDS, rewritten and NOT weakened. MEASURED by the reviewer in
      a disposable worktree at c1a3a3c4: extending the override report order with
      two promotion names and changing nothing else turns exactly these red -
        TestOverrideRuleNamesAreNotHardRuleNames::test_the_report_order_is_the_schema_names_then_the_hard_rule_names
        TestOverrideValidatorCollectsEveryViolation::test_every_rule_is_reported_exactly_once
        TestOverrideValidatorCollectsEveryViolation::test_the_result_follows_the_declared_order
        TestEffectiveTableBuilder::test_the_raised_object_carries_the_violations
        TestEffectiveTableBuilder::test_the_message_names_every_violated_rule, at
          its new parameters
      at 6 failed, 181 passed and 3 skipped. Widen each: the map that breaks every
      rule gains a promotion violation and its evidence argument, so the
      collecting property still covers EVERY name in the report order, and the
      order assertion gains the promotion segment. Delete nothing, skip nothing,
      and do not narrow a parametrization to dodge a new name.
  (p) HARD_RULE_NAMES still holds exactly the names round 5 shipped and the
      schema tuple exactly what round 6 shipped: no promotion name is in either.
  (q) Round 6's override tests otherwise pass UNCHANGED, and one test calls the
      validator with round 6's two positional arguments and no evidence map, so
      constraint 7 is a test rather than a promise.

Done when - the gates. Run each, record the REAL exit code and the REAL output.

  G1 TRANSPORT. After C0b: sha256sum .agent/authored/f110-r7.md
     .agent/last_block.md - one digest twice, both lines verbatim. ALSO report
     wc -l .agent/authored/f110-r7.md; the reviewer's projection is stated in the
     handback request below and the cap is 400. Report a difference, do not
     repair it.
  G2 THE PLAN. Extract PLAN7 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md          -> exit 0
       wc -l .agent/plan.md                    -> report; must be under 50
       grep -c '^## Goal' .agent/plan.md       -> 1
       grep -c '^## Next Steps' .agent/plan.md -> 1
  G3 THE LEDGER APPEND, full arithmetic, the record file. For RECORD6 at C2
     against the size immediately before that commit: report before + 2 + slice
     length, the real new size, and whether they are equal. Then a SECOND READER
     that counts no byte: split the WHOLE file on blank-line boundaries, let N be
     counted BY THE SCRIPT from the slice, and report whether the LAST N units
     equal the slice's N paragraphs IN ORDER. Then a NEGATIVE CONTROL: in a
     scratch copy flip one byte inside the FIRST appended paragraph and report
     that the second reader REJECTS it. Also report
     grep -c '^Gate: F110 R6 — ' .agent/live_review.md, 0 before C2 and 1 after.
  G4 THE PROSE FILE. Byte-equality check ONLY, per the gate budget: report
     whether the final bytes of .agent/prose_slips.md equal the extracted SLIPS7
     slice, whether the pre-C2 content survives as an exact byte PREFIX, and
     whether the file still ends without a newline.
  G5 THE MODULE, MEASURED AND RUN. On packages/orchestration/model_routing.py:
       git show --numstat C3 -- <path>   -> report insertions AND deletions
       ast.parse over its real text       -> no exception
     Report EVERY deleted line verbatim and say which region it came from; under
     constraint 7 a deletion outside the module docstring and the report-order
     constant is a violation - report it as such rather than repairing it. Then
     RUN THE SHIPPED CODE and report what the functions RETURNED, not what they
     were meant to return:
       the promotion bars and the document field list
       the promotion predicate on a cheaper, an equal, a stronger and an
         undeclared class
       the promotion check on: no evidence, incomplete evidence, evidence just
         below each bar, evidence exactly at each bar, and a non-promotion
       the validator and the builder on a promotion with and without evidence
       the evidence-fields function on a promoted and on an unpromoted class
       the validator called with round 6's two positional arguments alone
  G6 THE RED PROOF, in a disposable git worktree at the C4 commit and NEVER in
     the primary checkout. Report the UNMUTATED CONTROL FIRST: run the test file,
     report exit code and count. Then make the mutations listed below, one at a
     time:
       (i)   make the promotion predicate always answer "not a promotion"
       (ii)  make the promotion check never return the WITHOUT-EVIDENCE name
       (iii) lower the minimum overall pass rate constant to a tenth
       (iv)  make the evidence-fields function omit the promoted-by key
     For each, report which test ids go RED. THE DISCRIMINATOR, stated as the
     property to check rather than as a colour: each mutation must redden the
     cases written for ITS OWN behaviour, and must NOT redden another mutation's
     DEDICATED fixtures. Cases that assert over a map breaking every rule at once
     belong to no single mutation and may redden under several - that is
     construction, not a failure, and round 6's gate was worded too strongly on
     exactly this point. Mutation (iii) must ALSO redden the sync test of (j),
     which is the proof that the bars really are pinned to the document. A
     mutation that reddens nothing is a FAILED proof - report it as such.
     REVERT BY RESTORING THE FILE FROM THE C4 COMMIT INSIDE THE WORKTREE, never
     by re-editing it back. Purge __pycache__, run python3 -B, print the imported
     module's __file__ from inside the worktree, then remove the worktree BY ITS
     EXACT PATH and prune. Constraint 11 binds every command here.
  G7 THE SUITES, EACH AS ITS OWN INVOCATION, RUN SERIALLY. Measured by the
     reviewer at c1a3a3c4:
       python3 -m pytest tests/orchestration/test_model_routing.py -q     report passed AND skipped; it was 185 passed and 3 skipped, and the passed count must GROW
       python3 -m pytest tests/orchestration/test_orchestrator_model_routing.py tests/orchestration/test_job_role_routing.py -q   33 passed
       python3 -m pytest tests/orchestration/test_role_config.py -q       34 passed
       python3 -m pytest tests/orchestration/test_config.py -q            63 passed
       python3 -m pytest tests/docs/ -q                                   295 passed
       python3 -m pytest tests/cli/test_golden_path.py -q                 42 passed
     A moved count in the last five is the finding. A RISEN skip count in the
     first is also the finding: this round may not buy its green by skipping.
     tests/docs/ is gated because C4's sync test READS a file under docs/.
  G8 THE TREE, THE COMMITS AND THE SWEEP. Read git status --porcelain
     immediately before C5 is staged, git ls-files .remedy-wt (no output), and
     git worktree list - which already lists worktrees under .remedy-wt/job-*
     that are NOT of this round's making and must be left alone; what the gate
     requires is that no worktree THIS round created survives. Confirm
     git diff --stat c1a3a3c4..C4 -- docs/ lists NOTHING. Then, for C0a through
     C4 - the commits BEFORE the handback commit, per item 14 - report each
     one's insertion count from git show --numstat, the '+' column ONLY,
     compared CELL BY CELL against the Commits table of the handback you are
     writing. C5's own numbers go to neither a round report nor this file. Then
     THE STALENESS SWEEP over every file this round touched, one entry per file,
     stale or NOT stale, and why.

Handback
  Rewrite .agent/handoff.md per docs/agents/handback_template.md: SESSION 2 of
  F110, round 7, the state block, the item-status table with every ordered item
  appearing exactly once, the Commits table, one line per gate then the
  transcripts, the deviations, the next steps. No length cap. The reviewer's G1
  projection for this block is 351 lines. The session continues after this round,
  so the Next section names the resolver seam and the per-call-site class
  declarations as the next round, and states that the branch still has no open
  pull request.

SLICES. Each slice lies between its own one-line BEGIN and END marker. The
marker lines are NEVER part of the slice. The slices carried here are PLAN7,
RECORD6 and SLIPS7.

<<<BEGIN PLAN7>>>
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

Round 7, session 2 — T003, the PROMOTION-EVIDENCE DISCIPLINE. Moving a
class to a CHEAPER tier is refused unless a documented benchmark run
backs it: no evidence, incomplete evidence and below-threshold evidence
are each refused with their own rule name, the bars are seeded from the
policy document's "Promotion rule" section and pinned to it by a sync
test, and every routed call can report which evidence promoted it. Round
6's PASS verdict and its two prose slips are booked in the same round.

## Next Steps

- The resolver seam and the per-call-site task-class declarations
  (consolidation order E.d): the single place model selection happens,
  where the override map and the evidence map are finally READ from
  configuration instead of being passed in.
- The integration gate round, before closure.
- The closure sequence, which also runs the one checklist consolidation
  pass DECISION F110 D1 carries into it, and which updates the Design
  bullet of `docs/roadmap/features/T3_F110.md` so the roadmap names the
  orchestration class set DECISION F110 D2 widened.

## Risks

- The safety-relevant class set is EMPTY in production today, so that
  rule is proven against a fixture set in both its per-choice and its
  override-map form.
- Nothing routes in production yet and no config file is read: the schema
  and the evidence discipline validate mappings handed to them.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
<<<END PLAN7>>>

<<<BEGIN RECORD6>>>
Gate: F110 R6 — the round 6 entry. VERDICT PASS, over the range `78071a87..c1a3a3c4`. THE TRANSPORT PROOF REACHED THE EMITTED BYTES THIS ROUND, WHICH IS MORE THAN §3 ITEM 37 SAYS THIS WORKFLOW CAN PROVE, and it is recorded as exactly that rather than as the usual claim: the reviewer wrote the emitted block to gitignored scratch BEFORE delegating and left it untouched, and that original, the committed `.agent/authored/f110-r6.md` at `007c6aee`, its mirror `.agent/last_block.md` at `6f54d420`, and both working copies at `c1a3a3c4` are FIVE artefacts carrying ONE digest, `41e6e7588d20ce43963390f5e2821906b36447a9ebb8022e46334ec36993fdce`, at 29021 bytes each. Item 37's caveat is about a chain that walks only the worker's own outputs; this chain starts at the reviewer's. THE `wc -l` CLAUSE REPORTS 397 AGAINST A PROJECTION OF 397 — the third exact projection in a row, and exact for the same reason the last two were: the figure was recomputed after the last edit rather than carried from before it. EVERY SLICE WAS RE-DERIVED BYTE FOR BYTE BY THE REVIEWER. `.agent/plan.md` equals PLAN6 plus the one trailing newline constraint 4's target-convention clause orders, at 44 lines with one `## Goal` and one `## Next Steps`. `.agent/live_review.md` equals its base plus two newlines plus RECORD5 — 2164463 + 2 + 4500 = 2168965, the real size — still ends without a newline, and keeps its base as an exact byte prefix. `.agent/decisions.md` equals its base plus one newline plus DECISION2 plus one newline — 725637 + 1 + 2493 + 1 = 728132, the real size — still ends with exactly one newline, and keeps its base as an exact prefix. Both appends were re-read by an independent structural reader over the whole appended region with N counted from the slice, and both negative controls, flipped inside the FIRST appended paragraph, were rejected. DEVIATION D5 IS CORRECT AND THE GATE WAS WORDED TOO NARROWLY: the reviewer's own second reader compares the file's trailing blank-line units against the slice's paragraphs, and seven of DECISION2's eight paragraphs are byte-identical while the eighth differs by exactly the one trailing newline that same constraint 4 ORDERS the target to add — so the False reading is an artefact of the reviewer's gate wording, the byte-equality proof beside it is exact and total, and the worker reporting both readings instead of choosing the green one is the behaviour this record exists to reward. It is recorded in `.agent/prose_slips.md`, not as a finding. `ruff check` over both changed files answers "All checks passed!", run reviewer-side because the worker's permission layer refuses the tool, which the worker declared as D1 rather than inventing a reading. THE DELETIONS WERE READ LINE BY LINE, WHICH IS WHAT CONSTRAINT 7 EXISTS FOR: C3 is 309 insertions against 7 deletions, four of them the module docstring's opening paragraph and three the `ORCHESTRATION_TASK_CLASSES` comment — the two regions the block permits — and NO executable line was deleted; C4 is 364 against 4, being the test module's docstring first line, the class docstring constraint 8 names, and the two lines of the one edited test. EVERY SHIPPED FUNCTION WAS RUN BY THE REVIEWER, NOT READ. `ORCHESTRATION_TASK_CLASSES` is `mission`, `mission_compile`, `orchestrator`. An override naming an undeclared class returns `override_unknown_task_class` and one naming an undeclared tier returns `override_unknown_tier`, each attributed to its own key and neither raising out of the validator. `{"mission": "cheap"}` returns `orchestration_below_top_tier` and `{"mission": "top"}` returns empty. A fixture safety class demoted below mid returns `safety_class_below_mid_tier`, and the same fixture set over an EMPTY override map returns empty — the discriminator that makes every refusal the override's own. `{"standard_review": "cheap"}` returns `reviewer_weaker_than_worker` attributed to the REVIEWER half, which is the proof the rule is judged against the EFFECTIVE table rather than the override map alone, because the worker half is still the seed tier. One map breaking all five rules returns all five, once each, in the declared order and provably not in alphabetical order. The builder returns a NEW table, leaves `TASK_CLASS_TIERS` unmutated both on success and after a refusal, and raises `OverrideRefused` whose `.violations` and whose message name every violated rule. The override-aware resolver answers `per_project_override` where the tier differs from the seed, `seed_mapping` where an override merely restates it, and the conservative unknown pair for a class the table does not name — and round 5's resolver still answers exactly as it did. THE RED PROOF WAS RE-RUN IN FULL BY THE REVIEWER in a disposable worktree at `a62d4920`, with the module path printed from inside it and `git status --porcelain` read on the PRIMARY checkout immediately after every mutation, CLEAN every time. Control: 185 passed, 3 skipped, exit 0. The four mutations redden 10, 7, 7 and 8 ids, reproducing the worker's counts exactly, and every revert returned the worktree to 185 passed. THE BLOCK'S DISCRIMINATOR CLAUSE WAS TOO STRONG AND THE REVIEWER OWNS IT: it demanded the other mutations' cases stay GREEN, and four cases assert over a map breaking every rule at once, so they belong to no single mutation and redden under several by construction. What the proof establishes, measured pairwise, is the property that matters — each mutation reddens exactly its own rule's `test_the_message_names_every_violated_rule` parameter and its own dedicated fixtures, and no mutation reddens another's dedicated fixtures. That slip is in `.agent/prose_slips.md` too. THE SUITES WERE RE-RUN BY THE REVIEWER at 185 passed with 3 skipped for the routing file, then 33, 34, 63, 295 and 42, every one exit 0; the routing file grew from 127 and the other five are unmoved. THE THREE SKIPS ARE NOT A LOSS AND THE REVIEWER CHECKED: they are `mission` in `test_a_class_the_rule_does_not_cover_is_never_refused_by_it`, skipping with round 5's own reason "covered by the violating fixture above", so the coverage moved to the violating fixture rather than disappearing. DEVIATION D7 IS RULED ON HERE AND IS NOT A FINDING. `docs/roadmap/features/T3_F110.md` still words the rule as "orchestrator and mission-compile calls" while the shipped set also holds `mission`; that section is headed "Design (suggested shape)", DECISION F110 D2 records the widening with its measurement and its reversal step, and the constant's own comment sends a reader to that DECISION. Nothing on disk is false. F110's closure sequence updates that bullet so the roadmap and the code agree, and `.agent/plan.md` carries the obligation from this round on. DEVIATION D8 IS RULED ON AND CORRECTED: the worker reports that `docs/agents/model_routing_policy.md` contains no occurrence of "override", which is true of that exact word and misleading, because the document's own Seed mapping heading reads "(initial, per-project overridable)" — that IS the licence this round's schema enforces, so there is no gap and no docs edit is owed. DEVIATION D4 IS ACCEPTED: the worker's permission layer denies it every path under `.remedy-wt/`, so its worktree lived at `remedy-review-f110-r6-wt` and was removed by exact path; the reviewer confirms `git worktree list` holds only the five pre-existing `job-*` worktrees, `git ls-files .remedy-wt` returns nothing, and that directory is gone from disk. THE PER-COMMIT INSERTION COUNTS WERE VERIFIED CELL BY CELL against the handback's own Commits table and every cell matches: 397, 305, 19, 45 and 3, 309, and 364. `c1a3a3c4` is 591 insertions against 838 deletions, a full-file rewrite of a single `.agent/**` state file and therefore exempt from the 500-line cap under AGENTS.md DECISION F104 D1; every other commit of the round is under it. THE OPEN SET IS 278, over 347 registered and 69 resolved, UNCHANGED — RECORD5 minted no id, the round registered and resolved nothing, and `R-0767` remains OPEN on the seam this feature is working. THE TREE is clean, the eight committed paths are exactly the change set, `.agent/candidates.md` is untouched and still EMPTY, and the branch is pushed at `c1a3a3c4` with no pull request open.
<<<END RECORD6>>>

<<<BEGIN SLIPS7>>>
2026-09-03 · F110 R6 · The reviewer's G4 second reader was worded to compare the file's trailing blank-line units against the RAW slice's paragraphs, but constraint 4 of the same block orders the target's newline convention to win, so `.agent/decisions.md` legitimately carries one trailing newline the slice does not and the reading returned False on the eighth of eight paragraphs while the byte-equality proof beside it was exact and total. Reviewer gate-wording slip, nothing wrong on disk; the worker reported BOTH readings rather than choosing the green one, which is the behaviour to keep. No R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F110 R6 · The reviewer's G6 discriminator demanded that each mutation "leave the OTHER mutations' cases GREEN", which no round could satisfy: four of that file's cases assert over an override map breaking every rule at once, so they belong to no single mutation and redden under several by construction. The property that actually discriminates, and that the reviewer measured pairwise at `a62d4920`, is that each mutation reddens exactly its own rule's parameter of `test_the_message_names_every_violated_rule` plus its own dedicated fixtures, and reddens no other mutation's dedicated fixtures. Reviewer gate-wording slip, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIPS7>>>
