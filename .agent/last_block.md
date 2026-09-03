STEP F110 T002c / ROUND 6 - F110 Model routing by task class
FEATURE F110 - Model routing by task class (Tier 3) - SESSION 2, ROUND 6

Goal
  Ship the PER-PROJECT OVERRIDE SCHEMA: an override map is validated before it
  is applied, every violation is collected and NAMED, and an override that
  breaks a hard rule is REFUSED rather than silently dropped - the feature
  file's "per-project overrides allowed but hard rules always win. Violating
  overrides fail config validation with the rule named." Add `mission` to the
  orchestration class set per DECISION F110 D2. Book round 5's PASS verdict and
  that DECISION in the same round.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f110-r6.md
  C0b mirror it to .agent/last_block.md
  C1  apply PLAN6 to .agent/plan.md (FIRST substantive commit, item 23)
  C2  append RECORD5 to .agent/live_review.md and DECISION2 to
      .agent/decisions.md - round 5's verdict and its ruling, booked
  C3  THE PRODUCTION COMMIT: the override schema in model_routing.py
  C4  THE TEST COMMIT: the violating override fixtures in test_model_routing.py
  C5  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f110-r6.md (new, C0a) · .agent/last_block.md (C0b) ·
  .agent/plan.md (C1) · .agent/live_review.md (C2) · .agent/decisions.md (C2) ·
  packages/orchestration/model_routing.py (C3) ·
  tests/orchestration/test_model_routing.py (C4) · .agent/handoff.md (C5)

BASE for this round is 78071a87. Every byte, count and citation below was
measured there by the reviewer. NO DOCS ARE EDITED.
docs/agents/model_routing_policy.md is read, never written.

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by delimiter
     index from the COMMITTED .agent/authored/f110-r6.md - marker lines
     EXCLUDED - and write it with a script, never by retyping. If a slice looks
     wrong, apply it as written and DECLARE it in the handback.
  2. C1 is the first substantive commit; this round touches the finding ledger,
     so item 23 binds.
  3. C3 (production) precedes C4 (tests). Do not reorder.
  4. Newline conventions, MEASURED at 78071a87. .agent/live_review.md is 2164463
     bytes and ends WITHOUT a trailing newline; it must still end without one
     after C2, and its append is the two bytes newline newline then the slice.
     .agent/decisions.md is 725637 bytes and ends WITH exactly one newline; it
     must still end with exactly one after C2, and its append is the ONE byte
     newline, then the slice, then one final newline, so consecutive entries stay
     separated by exactly one blank line. .agent/plan.md ends WITH one. Where an
     extractor yields a trailing newline the target does not take, the TARGET's
     convention wins.
  5. NO RUFF GATE IS ORDERED and you must not add one; the reviewer lints it.
  6. NOTHING IS WIRED TO A CALL SITE THIS ROUND, and NO CONFIG FILE IS READ OR
     WRITTEN. packages/orchestration/config.py is neither edited nor imported.
     The override map is a MAPPING PASSED IN; the reader that produces one from a
     TOML table arrives with the resolver-seam round. Record that absence in the
     module docstring in the AGENTS.md discoverability idiom, so a reader looking
     for the config loader lands on the reason it is not here yet.
  7. ROUND 4'S AND ROUND 5'S SHIPPED BEHAVIOUR IS NOT REVISED, with ONE exception
     this block names: ORCHESTRATION_TASK_CLASSES gains `mission` per DECISION
     F110 D2. TASK_CLASS_TIERS, MODEL_TIERS, HARD_RULE_NAMES,
     SAFETY_RELEVANT_CLASSES, normalize_task_class, resolve_task_class_tier,
     model_tier_rank, the hard-rule checks and validate_routing_choice all keep
     their current behaviour. You are ADDING to this module.
  8. EXACTLY ONE EXISTING TEST IS EDITED, and DECISION F110 D2 is why:
     `test_the_covered_classes_are_the_two_the_feature_file_names`, at
     tests/orchestration/test_model_routing.py lines 382 to 385 measured at
     78071a87, asserts ORCHESTRATION_TASK_CLASSES equals exactly the two-class
     frozenset, which D2 makes false. Rewrite it so it pins the NEW membership
     exactly, and rename it so its name no longer says "the two"; repair the
     class docstring at line 357 of that file in the same commit. NO OTHER
     existing test is edited, renamed, deleted or skipped. Reviewer measurement,
     taken in a disposable worktree at 78071a87: adding `mission` to that set and
     changing nothing else takes the file from 127 passed to 1 failed, 126
     passed and 3 skipped, and the single failure is that test.
  9. A sentence OUTSIDE the change set that this round makes stale is DECLARED in
     the handback and NOT repaired. A sentence INSIDE a file this round edits
     that this round's own commit falsifies IS repaired in that commit - round
     5's C4b is the precedent and the reviewer accepted it.
  10. Read .agent/STOP from disk before the first commit and again before C5.
  11. Self-review loop before every commit. Push after C5. No pull request, no
      merge. Destructive verification only inside a disposable git worktree.
      NEVER `cd` into that worktree for any purpose: address it by absolute path,
      run pytest as `python3 -B -m pytest <abs-worktree>/tests/...`, and run
      `git status --porcelain` in the primary checkout immediately after every
      mutation, in the same step, not at cleanup.

SPEC CODE - additions to packages/orchestration/model_routing.py, written by YOU

  (a) `mission` JOINS ORCHESTRATION_TASK_CLASSES, per DECISION F110 D2, which
      C2 of this round commits and which states the measurement and the reason.
      Update that constant's own comment: the seed table routing `mission` to the
      top tier is exactly the property an override can move, which is what the
      set now guards. Say plainly that the set is deliberately WIDER than the
      feature file's two literal call kinds, and why, so a reader comparing the
      two does not read it as drift.

  (b) OVERRIDE_REASON, the reason token recorded when an OVERRIDE and not the
      seed mapping supplied a class's tier. It sits beside SEED_MAPPING_REASON
      and UNKNOWN_CLASS_REASON and is a fixed token for the same reason they are:
      evidence readers group on it.

  (c) REVIEWER_WORKER_CLASS_PAIRS, the declared (worker class, reviewer class)
      pairs, so policy hard rule 1 is checkable against a TABLE and not only
      against a per-call pairing. Seed it with the one pair the seed mapping
      supports today, standard_build and standard_review, and state that every
      member must be a key of TASK_CLASS_TIERS.

  (d) THE TWO SCHEMA RULE NAMES, as module-level string constants: one for an
      override naming a task class the seed table does not, one for an override
      naming a tier MODEL_TIERS does not. Collect them in their own tuple.
      HARD_RULE_NAMES IS NOT EXTENDED - a schema fault is a malformed config, not
      a policy breach, and an existing test pins that tuple at exactly the rule
      names round 5 shipped. Then declare the ORDER violations are reported in: the
      schema names first, then the hard-rule names, INDEPENDENT of MODEL_TIERS
      for the reason HARD_RULE_NAMES already states.
      WHY an override for an undeclared class is REFUSED rather than ignored: the
      resolver routes an undeclared class conservatively at call time, but an
      OVERRIDE for a class nobody declares is dead config that silently does
      nothing - which is the casual mapping edit this feature exists to stop.
      Say that at the constant.

  (e) A VIOLATION RECORD - a frozen dataclass carrying the task class and the
      rule name - so "refused with the rule named" is STRUCTURAL and a caller can
      branch on it, rather than a prose message it would have to parse.

  (f) THE COLLECTING OVERRIDE VALIDATOR, returning EVERY violation in a whole
      override map, in the declared order of (d). It takes the override mapping
      and the safety-relevant class set as a parameter defaulting to
      SAFETY_RELEVANT_CLASSES, for the reason (c) of round 5 gives. It reports:
        - each schema fault, per offending entry;
        - hard rule 2, an orchestration class whose EFFECTIVE tier is below top;
        - hard rule 3, a safety-relevant class whose EFFECTIVE tier is below mid;
        - hard rule 1, a pair of (c) whose EFFECTIVE reviewer tier ranks below its
          EFFECTIVE worker tier - attributed to the REVIEWER class, because that
          is the entry an operator must change.
      EFFECTIVE means the override map laid over the seed table, so an override
      lowering only the reviewer half of a pair is caught. A schema-faulty entry
      is reported and then NOT judged against the hard rules, because ranking a
      tier MODEL_TIERS does not name RAISES by design. Each violation's rule name
      is the value a check RETURNED wherever a check exists, never a label this
      function attaches - the discipline validate_routing_choice already states.

  (g) A REFUSAL EXCEPTION carrying the violations it was raised for, whose
      message names every violated rule.

  (h) THE EFFECTIVE-TABLE BUILDER: normalize the override keys, validate, RAISE
      the exception of (g) if there is any violation at all, otherwise return the
      seed table overlaid with the overrides. It must not mutate TASK_CLASS_TIERS.
      WHY it RAISES rather than dropping the offending entry: a silently dropped
      override leaves the operator believing it took effect, which is the silent
      downgrade policy hard rule 2 forbids. The hard rules win by REFUSING the
      config, not by quietly editing it. Put that sentence in the docstring.

  (i) THE OVERRIDE-AWARE RESOLVER, the sibling of resolve_task_class_tier taking
      an already-built effective table. Its REASON is DERIVED by comparison and
      never asserted: the unknown pair when the effective table does not name the
      class, OVERRIDE_REASON when it does and the tier differs from the seed
      table's, SEED_MAPPING_REASON when it does and the tier agrees - so an
      override that restates the seed tier is honestly reported as the seed
      mapping. Round 5's resolve_task_class_tier is NOT changed.

  Extend the module docstring's Public API list with everything (b) through (i)
  adds. Round 5's list is the shape to follow.

SPEC TESTS - additions to tests/orchestration/test_model_routing.py
  (j) A VIOLATING OVERRIDE MAP PER HARD RULE, each refused WITH THE RULE NAMED,
      asserted against the module's rule-name CONSTANT and never a retyped
      literal: an orchestration class demoted below top; `mission` demoted below
      top, which is DECISION F110 D2's own acceptance fixture; a fixture
      safety-relevant class demoted below mid; and the reviewer half of a pair of
      (c) demoted below its worker half. A CONFORMING counterpart for each, so
      every pair discriminates rather than merely producing a refusal.
  (k) THE TWO SCHEMA FAULTS: an override key the seed table does not name, and a
      tier MODEL_TIERS does not name. Each is refused with ITS OWN schema rule
      name, and neither raises out of the validator - a malformed config is
      reported, not crashed on.
  (l) THE COLLECTING PROPERTY: one override map breaking every rule at once
      returns one violation per rule, in the declared order of (d) and provably
      not in alphabetical order; a conforming map returns an empty result.
  (m) THE BUILDER: it returns the overlaid table for a conforming map, leaves
      TASK_CLASS_TIERS unmutated, and RAISES for a violating one - with the
      raised object's violations and its message naming every violated rule.
  (n) THE OVERRIDE-AWARE RESOLVER reports the override reason only where the
      effective tier DIFFERS from the seed, the seed reason where an override
      restates the seed tier, and the unknown pair for a class the table does not
      name.
  (o) HARD_RULE_NAMES still holds exactly the rule names round 5 shipped: the
      schema names are NOT in it.
  (p) EVERY MEMBER OF REVIEWER_WORKER_CLASS_PAIRS IS A KEY OF TASK_CLASS_TIERS,
      and the seed table alone - with no override at all - routes each pair's
      reviewer at or above its worker, so the shipped table conforms.
  (q) THE MEMBERSHIP PIN OF CONSTRAINT 8 IS REWRITTEN, NOT DELETED: it still
      asserts the EXACT membership of ORCHESTRATION_TASK_CLASSES, now naming
      every class the set holds. A wider pin is still a pin; a deleted one is not.
  Round 4's and round 5's other tests are not edited; this file otherwise only
  gains cases.

Done when - the gates. Run each, record the REAL exit code and the REAL output.

  G1 TRANSPORT. After C0b: sha256sum .agent/authored/f110-r6.md
     .agent/last_block.md - one digest twice, both lines verbatim. ALSO report
     wc -l .agent/authored/f110-r6.md; the reviewer's projection is 397 lines and
     the cap is 400. Report a difference, do not repair it.
  G2 THE PLAN. Extract PLAN6 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md          -> exit 0
       wc -l .agent/plan.md                    -> report; must be under 50
       grep -c '^## Goal' .agent/plan.md       -> 1
       grep -c '^## Next Steps' .agent/plan.md -> 1
  G3 THE LEDGER APPEND, full arithmetic, the record file. For RECORD5 at C2
     against the size immediately before that commit: report before + 2 + slice
     length, the real new size, and whether they are equal. Then a SECOND READER
     that counts no byte: split the WHOLE file on blank-line boundaries, let N be
     counted BY THE SCRIPT from the slice, and report whether the LAST N units
     equal the slice's N paragraphs IN ORDER. Then a NEGATIVE CONTROL: in a
     scratch copy flip one byte inside the FIRST appended paragraph and report
     that the second reader REJECTS it. Also report
     grep -c '^Gate: F110 R5 — ' .agent/live_review.md, 0 before C2 and 1 after.
  G4 THE DECISIONS APPEND, the other record file, same forensics. For DECISION2
     at C2 against the size immediately before that commit: report before + 1 +
     slice length + 1, the real new size, and whether they are equal. Report
     whether the pre-C2 content survives as an exact byte PREFIX, and whether the
     file still ends with exactly one newline byte. Then the same SECOND READER
     and NEGATIVE CONTROL as G3, with N counted by the script and the flipped
     byte inside the FIRST appended paragraph. Also report
     grep -c '^## DECISION F110 D2 ' .agent/decisions.md, 0 before C2 and 1 after.
  G5 THE MODULE, MEASURED AND RUN. On packages/orchestration/model_routing.py:
       git show --numstat C3 -- <path>   -> report insertions AND deletions
       ast.parse over its real text       -> no exception
     Constraint 7 permits deletions ONLY in the ORCHESTRATION_TASK_CLASSES
     comment and definition and in the module docstring, so report EVERY deleted
     line verbatim and say which of those two regions it came from. A deleted
     line from anywhere else is a violation of constraint 7 - report it as such
     rather than repairing it. Then RUN THE SHIPPED CODE and report what the
     functions RETURNED, not what they were meant to return:
       the value of ORCHESTRATION_TASK_CLASSES
       the validator on each schema fault of (k), one at a time
       the validator on each violating override map of (j), one at a time
       the validator on the map that breaks every rule at once, and on a
         conforming map
       the builder on a conforming map, and the exception type, the violations
         and the message it raises on a violating one
       the override-aware resolver on all three of its reason cases
  G6 THE RED PROOF, in a disposable git worktree at the C4 commit and NEVER in
     the primary checkout. Report the UNMUTATED CONTROL FIRST: run the test file,
     report exit code and count. Then make the mutations listed below, one at a
     time, reverting between each:
       (i)   remove `mission` from ORCHESTRATION_TASK_CLASSES again
       (ii)  make the reviewer-and-worker-pair leg of the override validator
             always report no violation
       (iii) make the unknown-task-class schema check always report no violation
       (iv)  make the effective-table builder RETURN the overlaid table instead of
             raising when there is a violation
     For each, report which test ids go RED. THE DISCRIMINATOR: each mutation
     must redden the cases written for ITS OWN behaviour and leave the OTHER
     mutations' cases GREEN. A mutation that reddens everything, or
     nothing, is a FAILED proof - report it as such rather than reporting a
     colour. REVERT BY RESTORING THE FILE FROM THE C4 COMMIT INSIDE THE
     WORKTREE, never by re-editing it back: a hand-reverted file is a second
     mutation nobody measured, and the next mutation's colour then answers for
     both. Purge __pycache__, run python3 -B, print the imported module's
     __file__ from inside the worktree so the mutated copy is provably the one
     imported, then remove the worktree BY ITS EXACT PATH and prune. Constraint
     11 binds every command here.
  G7 THE SUITES, EACH AS ITS OWN INVOCATION, RUN SERIALLY. Measured by the
     reviewer at 78071a87:
       python3 -m pytest tests/orchestration/test_model_routing.py -q     report the count; it was 127 and must GROW
       python3 -m pytest tests/orchestration/test_orchestrator_model_routing.py tests/orchestration/test_job_role_routing.py -q   33 passed
       python3 -m pytest tests/orchestration/test_role_config.py -q       34 passed
       python3 -m pytest tests/orchestration/test_config.py -q            63 passed
       python3 -m pytest tests/docs/ -q                                   295 passed
       python3 -m pytest tests/cli/test_golden_path.py -q                 42 passed
     A moved count in the last five is the finding. In the first, a count that
     did NOT grow means the new cases did not land. test_config.py is gated
     because this round adds config VOCABULARY while constraint 6 forbids it to
     touch the config loader; an unmoved 63 is that constraint measured.
  G8 THE TREE, THE COMMITS AND THE SWEEP. Read git status --porcelain
     immediately before C5 is staged, git ls-files .remedy-wt (no output), and
     git worktree list - which already lists worktrees under .remedy-wt/job-*
     that are NOT of this round's making and must be left alone; what the gate
     requires is that no worktree THIS round created survives. Confirm
     git diff --stat 78071a87..C4 -- docs/ lists NOTHING. Then, for C0a through
     C4 - the commits BEFORE the handback commit, per item 14 - report each
     one's insertion count from git show --numstat, the '+' column ONLY,
     compared CELL BY CELL against the Commits table of the handback you are
     writing. C5's own numbers go to neither a round report nor this file. Then
     THE STALENESS SWEEP over every file this round touched, one entry per file,
     stale or NOT stale, and why.

Handback
  Rewrite .agent/handoff.md per docs/agents/handback_template.md: SESSION 2 of
  F110, round 6, the state block, the item-status table with every ordered item
  appearing exactly once, the Commits table, one line per gate then the
  transcripts, the deviations, the next steps. No length cap. The session
  continues after this round, so the Next section names T003 - the
  promotion-evidence discipline - as the next round, and states that the branch
  still has no open pull request.

SLICES. Each slice lies between its own one-line BEGIN and END marker. The
marker lines are NEVER part of the slice. The slices carried here are PLAN6,
RECORD5 and DECISION2.

<<<BEGIN PLAN6>>>
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

Round 6, session 2 — T002c, the PER-PROJECT OVERRIDE SCHEMA. An override
map is validated before it is applied: every violation is collected and
named, a malformed entry is reported rather than crashed on, and an
override breaking a hard rule is REFUSED rather than silently dropped,
because a dropped override leaves the operator believing it took effect.
`mission` joins the orchestration class set per DECISION F110 D2, so an
override demoting it is refused by name. Round 5's PASS verdict and that
DECISION are booked in the same round.

## Next Steps

- T003: the promotion-evidence discipline, the evidence fields and the
  goldens — a promotion without evidence refused, with evidence logged.
- The per-call-site class declarations and the resolver seam
  (consolidation order E.d), which is where the override map is finally
  READ from a config file instead of being passed in.
- Then the integration gate, and the closure sequence, which also runs
  the one checklist consolidation pass DECISION F110 D1 carries into it.

## Risks

- The safety-relevant class set is EMPTY in production today, so the
  safety rule is proven against a fixture set in its override-map form
  exactly as it already is in its per-choice form.
- Nothing routes in production yet and no config file is read: the schema
  validates a mapping handed to it, and the reader that produces that
  mapping arrives with the seam round.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
<<<END PLAN6>>>

<<<BEGIN RECORD5>>>
Gate: F110 R5 — the round 5 entry. VERDICT PASS, over the range `7a4d381f..78071a87`, whose last commit is the one carrying the verdict text this entry books. THE TRANSPORT PROOF COVERS THE SAVED COPY AND ITS MIRROR AND NOTHING MORE (§3 item 37): one digest, twice. THE `wc -l` CLAUSE REPORTS 252 AGAINST A PROJECTION OF 252 — the second exact projection in a row, after three consecutive rounds low by 1, 1 and 3, and exact for the same reason the first was: the figure was recomputed after the last edit instead of carried from before it. EVERY SLICE WAS RE-DERIVED BYTE FOR BYTE BY THE REVIEWER: `.agent/plan.md` equals PLAN5; `.agent/live_review.md` equals its base plus two newlines plus RECORD4 and still ends without a newline; `.agent/prose_slips.md` equals its base plus two newlines plus SLIPS5, with the base preserved as an exact byte PREFIX. `ruff check` over both changed files answers "All checks passed!", run reviewer-side because the worker's permission layer refuses the tool. EVERY SHIPPED CHECK WAS RUN BY THE REVIEWER, NOT READ. `model_tier_rank` answers 0, 1 and 2 along `MODEL_TIERS` and raises `ValueError` naming `MODEL_TIERS` for a tier it does not hold. Hard rule 1 refuses `reviewer_weaker_than_worker` for a cheap reviewer against a top worker and returns `None` for an equal and for a stronger one. Hard rule 2 refuses `orchestration_below_top_tier` for `orchestrator` at mid, and returns `None` at top and for a class outside its set. Hard rule 3 refuses `safety_class_below_mid_tier` against a FIXTURE safety set, returns `None` at mid, and returns `None` under the production default because that set is empty — which is the honest reading and the whole reason the fixture parameter exists. The collecting validator returns all three names in `HARD_RULE_NAMES` order for a choice breaking all three, and an empty tuple for a conforming one. C3 IS 227 INSERTIONS AND ZERO DELETIONS, so constraint 7 held BY MEASUREMENT rather than by assertion: round 4's table is provably unrevised and its sync test still passes untouched. THE SUITES WERE RE-RUN BY THE REVIEWER at 127 for the routing file, 33 for the orchestrator-and-job-role pair, 34 for `test_role_config.py`, 295 for `tests/docs/` and 42 for the golden-path canary, every one exit 0; the routing file grew from 48 to 127 and nothing else moved. DEVIATION D1 — THE EXTRA COMMIT `0f4ece46` IS ACCEPTED AND THE JUDGEMENT BEHIND IT WAS RIGHT. C3's own module docstring said the module owns the class table and nothing else yet, and C3 itself made that false by adding the rules. The reviewer read the whole commit: five added and two removed lines, all docstring prose, no executable line touched. Constraint 8 covered a stale sentence OUTSIDE the change set, and this sentence was inside it and inside the very commit that falsified it, so declaring-and-not-repairing would have shipped a knowingly false first paragraph of production code; repairing it in its own clearly-labelled commit is the better of the two, and re-running the red proof at `0f4ece46` so it pins the SHIPPED bytes rather than a superseded tree is exactly the right instinct. THE HANDBACK COMMIT'S OWN NUMBERS, which §3 item 31 routes to this entry because a self-drive session has no round report to carry them: `91428271` is 556 insertions against 418 deletions and `78071a87` is 93 insertions against 0 — and the first of those two is a FULL-FILE REWRITE, so its numstat columns and the file's own before-and-after line counts diverge, which is item 28's shape and not a discrepancy. DECISION F110 D2 WAS TAKEN AT THIS GATE and is committed as its own slice into `.agent/decisions.md` in this same round: `mission` belongs in `ORCHESTRATION_TASK_CLASSES` and T002c adds it, because an override demoting it breaks no hard rule today and the policy-document sync test cannot reach an override at all. Round 5's deviation D6 asked for that ruling instead of taking it, which was the correct move and is the behaviour this record exists to reward. THE OPEN SET IS 278, over 347 registered and 69 resolved, UNCHANGED — the round registered nothing and resolved nothing, and the figure was recomputed from the record rather than carried, under the first-R-id-per-`Done:`-line reading F109's round 20 entry pinned as canonical. THE TREE is clean, `git ls-files .remedy-wt` returns nothing, no worktree of the round's own making survives, the eight committed paths are exactly the change set, and the branch is pushed at `78071a87`.
<<<END RECORD5>>>

<<<BEGIN DECISION2>>>
## DECISION F110 D2 (2026-09-03, F110 R5) — `mission` belongs in the orchestration class set, and T002c adds it

CONTEXT. Round 5 shipped the three hard rules of
`docs/agents/model_routing_policy.md` as named checks. Its deviation D6 asked
for this ruling instead of taking it, which was correct; the reviewer rules on
it here.

MEASURED by the reviewer at `0f4ece46`, by RUNNING the shipped code rather than
reading it. `ORCHESTRATION_TASK_CLASSES` holds `mission_compile` and
`orchestrator`; `TASK_CLASS_TIERS` names neither of those, so the intersection
of the two is EMPTY; and
`check_orchestration_class_routed_to_top_tier("mission", "cheap")` returns
`None`, even though `mission` is a real seeded class the policy document routes
to the top tier.

The hard rules are NOT vacuous and this DECISION does not say they are. They
judge a candidate CHOICE, which is exactly what the T002c override schema feeds
them, and each was confirmed at that same commit to refuse on a violating input.
The gap is narrower and real: a per-project override moving `mission` from the
top tier to the cheap one breaks no hard rule today, and the policy-document
sync test cannot catch it, because that test guards the TABLE against the
DOCUMENT and an override is neither.

CHOSEN. `mission` joins `ORCHESTRATION_TASK_CLASSES` in T002c, with a violating
fixture asserting that an override demoting it is refused BY NAME. F110 exists
to stop a tier moving "by editing a mapping casually", and an override map is
that edit wearing a config file's clothes.

ALTERNATIVE CONSIDERED AND REJECTED. Leave the set as the feature file's two
literal call kinds and rely on the sync test. Rejected because the sync test
demonstrably does not reach an override, which is the surface this feature
exists to police.

CONSEQUENCE, and it is a real one. The set stops matching the wording of
`docs/roadmap/features/T3_F110.md`, which names orchestrator and mission-compile
calls and not `mission`. Nothing is renamed and the feature file is not edited;
the module says at the constant why the set is deliberately wider than the
sentence that seeded it. One existing test asserts the exact two-class
membership; it is REWRITTEN in the same round rather than deleted, so the
membership stays pinned — a pin on a wider set, not a weaker pin.

REVERSE by deleting this DECISION, removing `mission` from
`ORCHESTRATION_TASK_CLASSES`, and restoring that membership test to the
two-class form git history holds at `78071a87`.
<<<END DECISION2>>>
