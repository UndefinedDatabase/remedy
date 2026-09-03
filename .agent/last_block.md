STEP F110 T001 / ROUND 8 - F110 Model routing by task class
FEATURE F110 - Model routing by task class (Tier 3) - SESSION 2, ROUND 8

Goal
  Ship the CALL-SITE AND ROLE INVENTORY and the ROUTING SEAM: every role Remedy
  resolves a runtime config for declares a TASK CLASS, the one policy sentence
  that has been pinned but inert since round 4 - "Repair prompts follow the tier
  of the original task class" - becomes EXECUTABLE, and the set of provider-call
  sites is a CHECKED fact rather than a list that rots. The feature file calls
  T001's inventory "the real work". Book round 7's PASS verdict, its prose slip
  and DECISION F110 D3 in the same round.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f110-r8.md
  C0b mirror it to .agent/last_block.md
  C1  apply PLAN8 to .agent/plan.md (FIRST substantive commit, item 23)
  C2  append RECORD7 to .agent/live_review.md, SLIPS8 to
      .agent/prose_slips.md and DECISION3 to .agent/decisions.md
  C3  THE PRODUCTION COMMIT: the role-to-class map and the seam
  C4  THE TEST COMMIT: the inventory sweep, the repair rule, the seam
  C5  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f110-r8.md (new, C0a) · .agent/last_block.md (C0b) ·
  .agent/plan.md (C1) · .agent/live_review.md (C2) ·
  .agent/prose_slips.md (C2) · .agent/decisions.md (C2) ·
  packages/orchestration/model_routing.py (C3) ·
  tests/orchestration/test_model_routing.py (C4) · .agent/handoff.md (C5)
  If C4 would exceed the AGENTS.md insertion cap, SPLIT IT as round 7 did (C4a, C4b); that split is pre-authorised and is not a deviation.

BASE for this round is 4cfcb464. Every byte, count, citation and measurement
below was taken there by the reviewer. NO DOCS ARE EDITED and no file outside the
change set is written; the policy document and role_config.py are READ, never written.

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by delimiter
     index from the COMMITTED .agent/authored/f110-r8.md - marker lines
     EXCLUDED - and write it with a script, never by retyping. If a slice looks
     wrong, apply it as written and DECLARE it in the handback.
  2. C1 is the first substantive commit; this round touches the finding ledger,
     so item 23 binds.
  3. C3 (production) precedes C4 (tests). Do not reorder.
  4. Newline conventions, MEASURED at 4cfcb464. .agent/live_review.md is 2177227
     bytes and ends WITHOUT a trailing newline; its append is the two bytes
     newline newline then the slice, and it must still end without one.
     .agent/prose_slips.md is 53575 bytes, likewise ends WITHOUT one, same
     two-byte append. .agent/decisions.md is 728132 bytes and ends WITH exactly
     one newline; its append is the ONE byte newline, then the slice, then one
     final newline. .agent/plan.md ends WITH one. Where an extractor yields a
     trailing newline the target does not take, the TARGET wins.
  5. NO RUFF GATE IS ORDERED and you must not add one; the reviewer lints it.
  6. NOTHING IS WIRED INTO AN EXISTING CALL SITE THIS ROUND. No file under
     packages/ or apps/ other than model_routing.py is edited, and that module
     imports neither config.py nor role_config.py. The seam is a function call
     sites WILL call; making them call it is the next round. Record that absence
     in the module docstring in the AGENTS.md discoverability idiom.
     WHY role_config IS NOT IMPORTED though this round is about its roles:
     model_routing is the POLICY layer and role_config the CONFIG layer, and the
     docstring already forbids that inversion for config.py. The coupling is
     enforced BY A TEST instead - SPEC TESTS (l) - which is stronger than an
     import, because an import fails only when something is MISSING while the
     test fails when the two sets DISAGREE in either direction.
  7. ROUNDS 4 THROUGH 7 SHIPPED BEHAVIOUR IS NOT REVISED. Every constant and
     every function those rounds added keeps its current behaviour and its
     current signature. You are ADDING to this module.
  8. NO EXISTING TEST IS EDITED, RENAMED, DELETED OR SKIPPED. Measured at
     4cfcb464: every addition here is a NEW name, and role_config.KNOWN_ROLES is
     read by a NEW test only. If you find an existing test that must change,
     STOP, do not change it, and report it as a blocked item in the handback.
  9. A sentence OUTSIDE the change set that this round makes stale is DECLARED in
     the handback and NOT repaired. A sentence INSIDE a file this round edits
     that this round's own commit falsifies IS repaired in that commit.
  10. Read .agent/STOP from disk before the first commit and again before C5.
  11. Self-review loop before every commit. Push after C5. No pull request, no
      merge. Destructive verification only inside a disposable git worktree, and
      NEVER `cd` into it: address it by absolute path, run
      `python3 -B -m pytest <abs-worktree>/tests/...`, and read
      `git status --porcelain` in the primary checkout immediately after every
      mutation, in the same step, not at cleanup.

SPEC CODE - additions to packages/orchestration/model_routing.py, written by YOU

  (a) THE ROLE-TO-CLASS MAP: each orchestration ROLE Remedy resolves a runtime
      config for, mapped to the TASK CLASS it declares. Every value must be a key
      of TASK_CLASS_TIERS. The roles, and the reviewer's reading of each, which
      you may improve on but must not silently depart from:
        builder -> standard build · reviewer -> standard review
        design_worker -> architecture · test_worker -> standard build
        final_verifier -> standard review · teacher -> summarize
        summary -> summarize · orchestrator -> mission, per DECISION F110 D3,
          which C2 of this round commits and which states the measurement and
          the alternative it rejected
      `repair` is NOT in this map; see (b).
      Comment the map as the T001 inventory in executable form, and say that a
      role in neither this map nor (b) is a role nobody declared a class for -
      which the test of (l) makes impossible to add quietly.

  (b) THE INHERITING ROLES, as their own frozen set, holding `repair` alone
      today. This is the policy document's OWN rule bullet - "Repair prompts
      follow the tier of the original task class." - which round 4's sync test
      has PINNED VERBATIM since it landed and which nothing has ever executed.
      State at the constant that the sentence was a checked string and is now a
      checked behaviour, and that the sync test pinning its wording is what stops
      the two drifting.

  (c) THE ROLE RESOLVER: given a role and an optional originating task class,
      return the task class that role's call declares.
        - a role in (a) returns its declared class, and the originating argument
          is IGNORED rather than allowed to override it, because a declared
          class is the declaration;
        - a role in (b) returns the ORIGINATING class, and RAISES when none is
          supplied - guessing would break the document's rule, and a repair
          prompt routed to a guessed tier is exactly the silent downgrade the
          policy forbids;
        - a role in NEITHER warns and answers conservatively, matching
          role_config's own unknown-role path, which warns rather than raising:
          two layers disagreeing about one unknown role is worse than either
          choice alone. Say in the docstring which behaviour you matched.

  (d) THE SEAM: one function a call site invokes with its role - and, for an
      inheriting role, the originating class - plus the optional effective table
      and evidence map rounds 6 and 7 shipped. It resolves the class through (c),
      then DELEGATES and recomputes nothing, returning the routed-call evidence
      mapping round 7 defines, so class, tier, reason and what promoted it all
      come from ONE place and cannot disagree. One-line WHY above its def: this
      is the single seam docs/roadmap/features/T3_F110.md asks for, and every
      call site routes through it once the wiring round lands.

  (e) THE CALL-SITE INVENTORY, as a module-level constant: each production call
      site that resolves a role's runtime configuration, as its repository path
      paired with the role it names - the LITERAL where one is passed, a declared
      DYNAMIC marker where a variable is. MEASURED by the reviewer at 4cfcb464
      with an AST sweep over packages/ and apps/, finding these calls to
      resolve_role_config:
        packages/orchestration/artifact_summary.py  role='summary'
        packages/orchestration/role_config.py       role='orchestrator'
        packages/orchestration/pingpong_job.py      role is a variable
        packages/orchestration/self_use_runner.py   role is a variable
        packages/orchestration/teacher_model.py     role is a variable  (twice)
        apps/cli/commands/do_cmd.py                 role is a variable
      Record it as a MULTISET of (path, role-or-marker) pairs and NOT with line
      numbers, which move under any edit above them. Note at the constant that a
      sweep keyed on literal roles alone would reach only two of the seven, which
      is why the inventory pins the CALL SITES and not the role strings.

  (f) A DELIBERATE ABSENCE, in the AGENTS.md idiom: `mission_compile` is a
      declared orchestration class with NO role and NO call site, because
      missions are compiled outside the role-config surface. A reader searching
      for that call site must land on the sentence saying there is not one yet.

  Extend the module docstring's Public API list with everything (a) through (e)
  adds. Round 7's list is the shape to follow.

SPEC TESTS - additions to tests/orchestration/test_model_routing.py
  (g) EVERY DECLARED CLASS IS A SEED-TABLE KEY, and the declaring map and the
      inheriting set are DISJOINT - a role is declared or inheriting, never both.
  (h) THE REPAIR RULE IS EXECUTABLE AND DISCRIMINATES: the inheriting role
      returns the originating class for at least two DIFFERENT originating
      classes with different tiers, so the test proves inheritance rather than a
      constant; and it RAISES when no originating class is supplied.
  (i) A DECLARED ROLE IGNORES AN ORIGINATING CLASS rather than being overridden
      by it, asserted with an originating class whose tier DIFFERS from the
      declared one, so the assertion cannot pass by coincidence.
  (j) THE ORCHESTRATOR ROLE ROUTES TO THE TOP TIER, asserted through the seam
      against TOP_TIER and never a retyped literal; and round 5's hard rule
      refuses that same class below top, so DECISION F110 D3's whole point - that
      this role's class is one the hard rules already guard - is a test, not a
      claim.
  (k) THE SEAM returns the evidence mapping round 7 declared, with the same keys,
      for a declared role, for an inheriting role, and for a promoted class with
      its evidence. Include a GOLDEN: one fully specified seam call asserted as
      an EXACT dict.
  (l) THE INVENTORY IS CHECKED, and this is the round's real deliverable. Re-run
      the AST sweep IN THE TEST over packages/ and apps/, collect every call to
      role_config's resolver as a (path, role-or-marker) pair, and assert the
      multiset EQUALS the constant of (e), so a new provider call site cannot
      land without this test going red. In the SAME class, assert that the
      literal roles the constant names are members of role_config.KNOWN_ROLES,
      and that EVERY member of KNOWN_ROLES is in the declaring map or in the
      inheriting set - the coupling constraint 6 keeps out of the imports. A file
      that fails to parse FAILS the test with that file named, and is never
      skipped: a silently skipped file is a call site nothing covers.
  (m) THE UNDECLARED ROLE path answers conservatively and warns, asserted on the
      warning as well as on the answer. Rounds 4 through 7's tests are not
      edited; this file only gains cases.

Done when - the gates. Run each, record the REAL exit code and the REAL output.

  G1 TRANSPORT. After C0b: sha256sum .agent/authored/f110-r8.md
     .agent/last_block.md - one digest twice, both lines verbatim. ALSO report
     wc -l .agent/authored/f110-r8.md against the projection the Handback
     paragraph states; the cap is 400. Report a difference, do not repair it.
  G2 THE PLAN. Extract PLAN8 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md          -> exit 0
       wc -l .agent/plan.md                    -> report; must be under 50
       grep -c '^## Goal' .agent/plan.md       -> 1
       grep -c '^## Next Steps' .agent/plan.md -> 1
  G3 THE LEDGER APPEND, full arithmetic, the record file. For RECORD7 at C2
     against the size immediately before that commit: report before + 2 + slice
     length, the real new size, and whether they are equal. Then a SECOND READER
     that counts no byte: split the WHOLE file on blank-line boundaries, let N be
     counted BY THE SCRIPT from the slice, and report whether the LAST N units
     equal the slice's N paragraphs IN ORDER. Then a NEGATIVE CONTROL: in a
     scratch copy flip one byte inside the FIRST appended paragraph and report
     that the second reader REJECTS it. Also report
     grep -c '^Gate: F110 R7 — ' .agent/live_review.md, 0 before C2 and 1 after.
  G4 THE DECISIONS APPEND, the other record file, same forensics. For DECISION3
     at C2: report before + 1 + slice length + 1, the real new size, and whether
     they are equal; whether the pre-C2 content survives as an exact byte PREFIX;
     whether the file still ends with exactly one newline byte; the same SECOND
     READER with N counted by the script; and the same NEGATIVE CONTROL flipped
     inside the FIRST appended paragraph. Also report
     grep -c '^## DECISION F110 D3 ' .agent/decisions.md, 0 before C2 and 1
     after. FOR .agent/prose_slips.md a BYTE-EQUALITY CHECK ONLY, per the gate
     budget: final bytes equal SLIPS8, pre-C2 content an exact byte prefix, file
     still ending without a newline.
  G5 THE MODULE, MEASURED AND RUN. On packages/orchestration/model_routing.py:
       git show --numstat C3 -- <path>   -> report insertions AND deletions
       ast.parse over its real text       -> no exception
     Report EVERY deleted line verbatim and the region it came from. Constraint 7
     forbids revising rounds 4 through 7, so a deletion outside the module
     docstring is a violation - report it as such rather than repairing it. Then
     RUN THE SHIPPED CODE and report what the functions RETURNED:
       the role-to-class map, the inheriting set and the inventory constant
       the role resolver on every member of role_config.KNOWN_ROLES, supplying an
         originating class where one is required; then on an inheriting role with
         NO originating class, and on a role neither set names
       the seam on a declared role, on an inheriting role, and on a promoted
         class carrying sufficient evidence
       an AST sweep of your own over packages/ and apps/, printing every call
         site it finds beside the inventory constant
  G6 THE RED PROOF, in a disposable git worktree at the last test commit and
     NEVER in the primary checkout. Report the UNMUTATED CONTROL FIRST: run the
     test file, report exit code and count. Then make the mutations listed below,
     one at a time:
       (i)   make the inheriting role return a FIXED class instead of the
             originating one
       (ii)  make the role resolver accept a missing originating class instead of
             raising
       (iii) drop one entry from the call-site inventory constant
       (iv)  point the orchestrator role at a cheap-tier class
     For each, report which test ids go RED. THE DISCRIMINATOR, as a property
     rather than a colour: each mutation reddens the cases written for ITS OWN
     behaviour and reddens no other mutation's DEDICATED fixtures; cases
     asserting over the whole role set or the whole inventory belong to no single
     mutation and may redden under several, which is construction, not failure.
     Mutation (iii) must redden the inventory test of (l) and nothing that is not
     about the inventory - the proof that the sweep compares against the constant
     instead of re-deriving it. A mutation that reddens nothing is a FAILED proof
     - report it as such. REVERT BY RESTORING THE FILE FROM ITS COMMIT INSIDE THE
     WORKTREE, never by re-editing it back.
     Purge __pycache__, run python3 -B, print the imported module's __file__ from
     inside the worktree, then remove the worktree BY ITS EXACT PATH and prune.
     Constraint 11 binds every command here.
  G7 THE SUITES, EACH AS ITS OWN INVOCATION, RUN SERIALLY. Measured by the
     reviewer at 4cfcb464:
       python3 -m pytest tests/orchestration/test_model_routing.py -q     report passed AND skipped; it was 325 passed and 3 skipped, and the passed count must GROW
       python3 -m pytest tests/orchestration/test_orchestrator_model_routing.py tests/orchestration/test_job_role_routing.py -q   33 passed
       python3 -m pytest tests/orchestration/test_role_config.py -q       34 passed
       python3 -m pytest tests/orchestration/test_config.py -q            63 passed
       python3 -m pytest tests/docs/ -q                                   295 passed
       python3 -m pytest tests/cli/test_golden_path.py -q                 42 passed
     A moved count in the last five is the finding, and test_role_config.py is
     gated because this round reads KNOWN_ROLES while constraint 6 forbids it to
     import that module: an unmoved 34 is that constraint measured. A RISEN skip
     count in the first is also the finding.
  G8 THE TREE, THE COMMITS AND THE SWEEP. Read git status --porcelain
     immediately before C5 is staged, git ls-files .remedy-wt (no output), and
     git worktree list - which already holds worktrees under .remedy-wt/job-*
     that are NOT of this round's making and must be left alone; the gate
     requires only that no worktree THIS round created survives. Confirm
     git diff --stat 4cfcb464..<last test commit> -- docs/ lists NOTHING, and
     the same over packages/ and apps/ EXCLUDING model_routing.py, which is
     constraint 6 measured rather than asserted. Then, for every commit BEFORE
     the handback commit, per item 14, report its insertion count from
     git show --numstat, the '+' column ONLY, compared CELL BY CELL against the
     handback's Commits table. C5's own numbers go to neither a round report nor
     this file. Then THE STALENESS SWEEP, one entry per touched file, stale or
     NOT stale, and why.

Handback
  Rewrite .agent/handoff.md per docs/agents/handback_template.md: SESSION 2 of
  F110, round 8, the state block, the item-status table with every ordered item
  appearing exactly once, the Commits table, one line per gate then the
  transcripts, the deviations, the next steps. No length cap. The reviewer's G1
  projection for this block is 399 lines. THIS IS THE LAST ROUND OF THE SESSION:
  the Next section names the WIRING round - the existing call sites routing
  through the seam - as the next round, and states that the branch has no open
  pull request, so the next session's Open PR Gate finds none.

SLICES. Each slice lies between its own one-line BEGIN and END marker. The
marker lines are NEVER part of the slice. The slices carried here are PLAN8,
RECORD7, SLIPS8 and DECISION3.

<<<BEGIN PLAN8>>>
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

Round 8, session 2 — T001, the CALL-SITE AND ROLE INVENTORY and the
ROUTING SEAM. Every role Remedy resolves a runtime config for declares a
task class; the policy document's own repair-prompt rule, pinned as a
string since round 4, becomes executable; and the set of provider-call
sites is checked by an AST sweep against a declared constant, so a new
call site cannot land undeclared. Round 7's PASS verdict, its prose slip
and DECISION F110 D3 are booked in the same round.

## Next Steps

- The wiring round: the existing call sites route through the seam, and
  the override map and evidence map are READ from configuration instead
  of being passed in.
- The integration gate round, before closure.
- The closure sequence, which also runs the one checklist consolidation
  pass DECISION F110 D1 carries into it, and which updates the Design
  bullet of `docs/roadmap/features/T3_F110.md` so the roadmap names the
  orchestration class set DECISION F110 D2 widened.

## Risks

- Five of the seven call sites pass the role as a variable, so the
  inventory pins the call SITES rather than the role strings; a role
  reaching the resolver dynamically is still caught by that module's own
  unknown-role warning.
- Nothing is wired yet and no config file is read: the declaration lands
  before the wiring, deliberately.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
<<<END PLAN8>>>

<<<BEGIN RECORD7>>>
Gate: F110 R7 — the round 7 entry. VERDICT PASS, over the range `c1a3a3c4..4cfcb464`. THE TRANSPORT PROOF AGAIN REACHED THE EMITTED BYTES: the reviewer's scratch original, written before delegation and untouched since, the committed `.agent/authored/f110-r7.md` at `5cadf64b`, its mirror at `1523b1b9` and both working copies at `4cfcb464` are FIVE artefacts carrying ONE digest, `77d742debe526e97f8a1849fafbe462714e2354fded17c0a38f65b279f7c7581`, at 31572 bytes each — so the chain starts at the reviewer's own output rather than at the worker's, which is the condition §3 item 37's caveat is about. THE `wc -l` CLAUSE REPORTS 351 AGAINST A PROJECTION OF 351, the fourth exact projection in a row. EVERY SLICE WAS RE-DERIVED BYTE FOR BYTE: `.agent/plan.md` equals PLAN7 plus the one trailing newline the target's convention adds, at 44 lines with one `## Goal` and one `## Next Steps`; `.agent/live_review.md` equals its base plus two newlines plus RECORD6, 2168965 + 2 + 8260 = 2177227 exactly, still ending without a newline and keeping its base as an exact byte prefix, with the structural second reader in order and the negative control on the FIRST appended paragraph rejected; `.agent/prose_slips.md` equals its base plus two newlines plus SLIPS7, base preserved as an exact prefix, still ending without a newline. `ruff check` over both changed files answers "All checks passed!", run reviewer-side because the worker's permission layer refuses the tool, which the worker declared rather than inventing a reading. DEVIATION D1 IS THE ROUND'S MOST IMPORTANT ARTEFACT AND THE REVIEWER RULES FOR THE WORKER. The block's SPEC (o) predicted six red guards, having been measured against a report-order tuple widened with dummy names and NOT against the promotion check actually firing; the real figure at the committed production commit is TWELVE failed, 176 passed and 3 skipped, because every orchestration class and every fixture safety class the seed table names is seeded at the TOP tier, so ANY map that breaks their hard rule is necessarily ALSO a promotion. The worker widened five further existing functions, declared it, and explicitly REJECTED the alternative of suppressing a promotion violation for an entry already breaking a hard rule — which would have matched the reviewer's projection exactly and contradicted the module's own declared "report EVERY violation at once" discipline. That refusal was right, and the reviewer confirms it: an operator demoting `mission` has TWO independent problems, one of which no benchmark can ever discharge. EVERY WIDENED GUARD WAS READ AND EVERY ONE IS A STRENGTHENING, NOT A WEAKENING: the exact-list assertions gained the second rule name and stayed EXACT lists; the "not refused" case kept its exactly-empty assertion and now makes it against supplied evidence, so it says the stronger thing; and the worker added, unordered, `test_evidence_clears_the_promotion_name_and_never_the_orchestration_rule` and `test_evidence_never_discharges_a_hard_rule`, which are the two properties this whole design turns on. It also introduced a PROMOTABLE_CLASS fixture — a seeded class no hard rule speaks about — which is exactly the isolation the reviewer's own list failed to think of. DEVIATION D3 IS ACCEPTED AND WAS THE RIGHT CALL: C4 would have been 717 insertions, so the worker split it into `2cd58c66` at 231 and `7db8c018` at 486, both under the AGENTS.md cap, rather than spending the once-per-feature oversize exception on a commit that splits cleanly — and C4a is green on its own. DEVIATION D4 IS ACCEPTED AND THE GATE WAS AT FAULT: G5 permitted deletions only in the module docstring and the report-order constant, while SPEC (g) and (h) necessarily change the validator's docstring and the builder's call line. All 17 deletions were read line by line and every one is prose or a call line the ordered change requires; NO shipped behaviour of rounds 4 through 7 was revised. EVERY SHIPPED FUNCTION WAS RUN BY THE REVIEWER, NOT READ. The bars are 3, 90 and 75, held as the document's own PERCENT numerals rather than as floats. The document field list is `model_id`, `quantization`, `prompt_hash`, `tokens`, `cost`, `assertion_results`, `reviewer_verdict`, every one a real field of the evidence record, with `runs_per_fixture` and `corpus` correctly held OUTSIDE that list because the document names them in prose and not in its logged-per-run bullet. The promotion predicate answers True for cheaper, False for equal, False for stronger and False for an undeclared class. The check answers `promotion_without_evidence` for no evidence, `promotion_evidence_incomplete` for an unset field, `promotion_evidence_below_threshold` just below each of the three bars separately, and None exactly AT every bar — the boundary is `>=`, as the document's "≥" says. The builder refuses an unevidenced promotion and accepts the same promotion with evidence, leaving `TASK_CLASS_TIERS` unmutated either way. The evidence mapping carries `task_class`, `tier`, `reason` and `promoted_by`, with `promoted_by` naming the run for a promoted class and None otherwise. THE RED PROOF WAS RE-RUN IN FULL BY THE REVIEWER in a disposable worktree at `7db8c018`, module path printed from inside it, `git status --porcelain` read on the PRIMARY checkout immediately after every mutation and CLEAN every time. Control: 325 passed, 3 skipped, exit 0. The four mutations redden 39, 14, 1 and 25 ids, reproducing the worker's counts exactly, and every revert returned the worktree to 325 passed. MUTATION (iii) REDDENS EXACTLY ONE ID AND THAT IS THE ROUND'S KEY EVIDENCE, not a weakness: lowering the overall bar reddens `TestPromotionRuleSyncTest::test_the_parsed_overall_rate_equals_the_module_constant` and nothing else, because the boundary fixtures derive from the constants BY DESIGN so they follow a bar that moves. The sync test is therefore the single thing standing between the code and a quiet bar reduction — and it stands. That is the promotion rule's acceptance line, and the worker's deviation D6 explains the mechanism correctly. THE SUITES WERE RE-RUN BY THE REVIEWER at 325 passed with 3 skipped for the routing file, then 33, 34, 63, 295 and 42, every one exit 0; the routing file grew from 185, the skip count did NOT rise, and the other five are unmoved. CONSTRAINT 7 WAS TOO STRONGLY WORDED AND THE WORKER IS NOT AT FAULT: it demanded that a caller supplying no evidence map get round 6's answers unchanged, and for any map demoting a seeded class that is unmeetable by the same arithmetic D1 names. What holds, and what the reviewer measured, is the property that matters — round 6's two-positional-argument SIGNATURE still works, a schema fault and an empty map answer exactly as before, and the change is confined to promotions, which is precisely where T003 must change the answer. DEVIATION D8 IS ACCEPTED WITH THE CORRECTION IT DESERVES: the worker `cd`-ed into its worktree once on a first probe and immediately re-ran without it, and the reviewer confirms the primary checkout is clean and its own re-run of the proof used `subprocess` with `cwd` throughout. THE PER-COMMIT INSERTION COUNTS WERE VERIFIED CELL BY CELL against the handback's Commits table and every cell matches: 351, 246, 20, 3 and 5, 370, 231, and 486. `4cfcb464` is 555 insertions against 553 deletions, a full-file rewrite of a single `.agent/**` state file and exempt from the 500-line cap under AGENTS.md DECISION F104 D1; every other commit of the round is under it. THE OPEN SET IS 278, over 347 registered and 69 resolved, UNCHANGED — the round minted no id, and `R-0767` remains OPEN. THE TREE is clean, `git diff --stat c1a3a3c4..7db8c018 -- docs/` lists nothing, `git ls-files .remedy-wt` returns nothing, only the five pre-existing `job-*` worktrees survive, `.agent/candidates.md` is untouched and still EMPTY, and the branch is pushed at `4cfcb464` with no pull request open.
<<<END RECORD7>>>

<<<BEGIN SLIPS8>>>
2026-09-03 · F110 R7 · THREE CLAUSES OF THE ROUND 7 BLOCK SHARED ONE ROOT CAUSE: the reviewer derived them from a probe that widened the report-order tuple with dummy names and never exercised the promotion CHECK the same round ordered built. SPEC (o) therefore predicted six red guards where twelve go red; constraint 7's "a caller supplying no evidence map gets round 6's answers unchanged" is unmeetable for any map demoting a seeded class, since every orchestration and fixture-safety class is seeded at the top tier and any demotion of one is also a promotion; and G5's permitted-deletion regions omitted the validator docstring and the builder's call line that SPEC (g) and (h) necessarily change. The worker declared all three, chose correctly on each, and widened rather than weakened every affected test. THE LESSON: a pre-emission probe must exercise the BEHAVIOUR the round ships, not only the SHAPE of the constant that names it — a tuple widened with dummy names cannot show what a real check does. Reviewer block-authoring slip, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIPS8>>>

<<<BEGIN DECISION3>>>
## DECISION F110 D3 (2026-09-03, F110 R7) — the orchestrator ROLE declares the `mission` task class, and the policy document is not edited to seed a new one

CONTEXT. Round 8 maps every role Remedy resolves a runtime configuration for to
a task class. All but one map onto a class the policy document's seed mapping
already names; the `orchestrator` role does not, and the choice has to be made
before the map can be written.

MEASURED by the reviewer at `4cfcb464`, from the shipped constants rather than
the prose. `TASK_CLASS_TIERS` does not name `orchestrator`.
`ORCHESTRATION_TASK_CLASSES` names `orchestrator`, `mission_compile` and
`mission`, and round 6's own `OVERRIDABLE_ORCHESTRATION_CLASSES` computes the
intersection of those two sets and finds `mission` alone — so `orchestrator` and
`mission_compile` are CALL KINDS the hard rule guards, not classes the seed
table routes.

CHOSEN. The `orchestrator` role declares the `mission` class. That class is
seeded at the top tier, it is in `ORCHESTRATION_TASK_CLASSES` after DECISION
F110 D2, and it is therefore already guarded by hard rule 2 against any override
that would demote it — so the orchestrator's call is pinned to the top tier by a
CHECKED rule and not merely by a table entry. The reading is honest as well as
convenient: the orchestrator's call is the mission-level decision every later
call obeys, which is what the policy document's top tier exists for.

ALTERNATIVE CONSIDERED AND REJECTED. Add `orchestrator` to the seed mapping in
`docs/agents/model_routing_policy.md` and to `TASK_CLASS_TIERS` together, keeping
round 4's sync test green. Rejected on two grounds. It edits the human-readable
POLICY to make a code mapping convenient, which inverts the direction this
feature exists to enforce — the document seeds the code, never the reverse. And
it would put a CALL KIND into a vocabulary of WORK KINDS, so the seed mapping
would then answer two different questions with one list.

ALSO REJECTED. Let the role fall through to the conservative unknown-class path,
which routes to the top tier anyway. Rejected because evidence would then record
`unknown_class_conservative` for a role Remedy knows perfectly well, and a reason
saying "nobody declared this" about a declared role makes the evidence base less
trustworthy exactly where it is most read.

CONSEQUENCE. `mission_compile` and `orchestrator` stay in
`ORCHESTRATION_TASK_CLASSES` while being unreachable through an override map,
because neither is a seed-table key — round 6's tests already measure that. They
are kept because the hard rule judges a candidate CHOICE and a later round may
route one directly. The module carries a deliberate-absence note saying
`mission_compile` has no role and no call site.

REVERSE by deleting this DECISION and repointing the orchestrator role at
whatever class a later relay rules, or by seeding `orchestrator` into the policy
document and the table together, which is the rejected alternative above and
needs its own decision.
<<<END DECISION3>>>
