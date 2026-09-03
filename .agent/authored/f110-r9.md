STEP F110 T001 / ROUND 9 - F110 Model routing by task class
FEATURE F110 - Model routing by task class (Tier 3) - SESSION 3, ROUND 9

Goal
  THE WIRING ROUND, the third and last clause of T001. All seven inventoried
  call sites route through the seam in ONE change, because all seven already
  funnel through role_config.resolve_role_config - that function now calls
  route_role_call and carries the routed-call evidence on the RoleConfig it
  already returns. DECISION F110 D4 rules WHERE that evidence lands. Book round
  8's PASS verdict and its prose slip in the same round.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f110-r9.md
  C0b mirror it to .agent/last_block.md
  C1  apply PLAN9 to .agent/plan.md (FIRST substantive commit, item 23)
  C2  append RECORD8 to .agent/live_review.md, SLIPS9 to
      .agent/prose_slips.md and DECISION4 to .agent/decisions.md
  C3  THE PRODUCTION COMMIT: the wiring, and the two docstring repairs
  C4  THE TEST COMMIT: the routed evidence, the repair role, the invariants
  C5  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f110-r9.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/plan.md (C1) - .agent/live_review.md (C2) -
  .agent/prose_slips.md (C2) - .agent/decisions.md (C2) -
  packages/orchestration/role_config.py (C3) -
  packages/orchestration/model_routing.py (C3, DOCSTRING ONLY) -
  tests/orchestration/test_role_config.py (C4) - .agent/handoff.md (C5)
  If C4 would exceed the AGENTS.md insertion cap, SPLIT IT (C4a, C4b); that
  split is pre-authorised and is not a deviation.

BASE for this round is 328228dc. Every byte, count, citation and measurement
below was taken there by the reviewer. NO DOCS ARE EDITED, no file under
docs/ is written, and no file outside the change set is touched.

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by delimiter
     index from the COMMITTED .agent/authored/f110-r9.md - marker lines
     EXCLUDED - and write it with a script, never by retyping. If a slice looks
     wrong, apply it as written and DECLARE it in the handback.
  2. C1 is the first substantive commit; this round touches the finding ledger,
     so item 23 binds.
  3. C3 (production) precedes C4 (tests). Do not reorder.
  4. Newline conventions, MEASURED at 328228dc - all four figures re-measured
     at THIS round's base rather than carried forward, which is the lesson
     round 8's deviation D1 paid for. .agent/live_review.md is 2185166 bytes
     and ends WITHOUT a trailing newline; its append is the two bytes newline
     newline then the slice, and it must still end without one.
     .agent/prose_slips.md is 55971 bytes, same shape, same two-byte append.
     .agent/decisions.md is 731148 bytes and ends WITH exactly one newline; its
     append is ONE newline, the slice, then one final newline. .agent/plan.md
     is 1969 bytes and ends WITH one. Where an extractor yields a trailing
     newline the target does not take, the TARGET wins.
  5. NO RUFF GATE IS ORDERED and you must not add one; the reviewer lints it.
  6. TWO PRODUCTION FILES ARE EDITED AND ONLY ONE CHANGES BEHAVIOUR.
     role_config.py is the round's real change. model_routing.py is edited in
     the SAME commit for its MODULE DOCSTRING ONLY - no constant, no signature
     and no function body of rounds 4 through 8 is revised - because this round
     falsifies two of its sentences and constraint 9 requires repairing them
     there. No other file under packages/ or apps/ is written, and NO CALL SITE
     IS EDITED: the wiring reaches all seven through the resolver they share.
  7. ROUNDS 4 THROUGH 8 SHIPPED BEHAVIOUR IS NOT REVISED. Every constant and
     function those rounds added keeps its behaviour and its signature.
     route_role_call still RAISES for a direct caller; only the config layer,
     which has no originating class to supply, records the absence.
  8. NO EXISTING TEST IS EDITED, RENAMED, DELETED OR SKIPPED. The reviewer
     applied this round's own change in a disposable worktree at 328228dc and
     ran the two suites together: 425 passed, 3 skipped, exit 0, with no test
     edited. Every addition here is a NEW name. If you find an existing test
     that must change, STOP, do not change it, and report it as a blocked item.
  9. A sentence this round makes stale INSIDE the change set is repaired in the
     commit that falsifies it. A sentence OUTSIDE the change set that this round
     makes stale is DECLARED in the handback and NOT repaired - no file outside
     the change set is written for a prose reason.
 10. Read .agent/STOP from disk before the first commit and again before C5. If
     it exists at either reading, finish the commit in hand, write the handback
     and stop.
 11. Destructive verification runs ONLY inside a disposable git worktree, never
     in the primary checkout. Purge __pycache__ before every run and use
     python3 -B. Remove the worktree BY ITS EXACT PATH when done and prune.

SPEC - THE PRODUCTION COMMIT (C3)
  This is a SPEC, not a slice: write the code yourself, in this module's own
  idiom, and improve on any wording below that is worse than what you would
  write. Do not depart from the BEHAVIOUR without declaring it.

  (a) THE IMPORT, AND ITS DIRECTION. role_config.py imports
      OriginatingTaskClassRequired and route_role_call from
      packages.orchestration.model_routing, at module level. Measured at
      328228dc: model_routing.py's only imports are `warnings` and
      `dataclasses` (nothing else at module level), so this import creates NO
      cycle. The direction is CONFIG depending on POLICY, which is the one
      direction model_routing.py's own docstring permits - that docstring
      forbids the INVERSE, policy importing config, and says so twice.

  (b) RoleConfig GAINS ONE FIELD, and it is a nested mapping rather than four
      flattened ones:
          routed_call: dict[str, str | None] | None = field(default=None, compare=False)
      `field` is added to the `from dataclasses import dataclass` line. The
      keys are exactly model_routing.ROUTED_CALL_EVIDENCE_FIELDS, so this round
      introduces NO second spelling of task_class, tier, reason or promoted_by.
      WHY compare=False, MEASURED AND NOT ASSUMED: a frozen dataclass derives
      __hash__ from its COMPARED fields, so an unqualified dict field makes
      hash() raise `TypeError: unhashable type: 'dict'`. The reviewer ran both
      shapes at 328228dc - with compare=False hash() succeeds, without it it
      raises - so this keeps RoleConfig exactly as hashable and as comparable
      as it has always been.

  (c) resolve_role_config GAINS A FOURTH PARAMETER, LAST IN THE LIST:
          originating_task_class: str | None = None
      Last and defaulted, because a trailing optional parameter breaks no
      caller: measured at 328228dc, every call site passes `role` positionally
      and everything else by keyword.

  (d) THE HELPER THAT SWALLOWS EXACTLY ONE EXCEPTION AND NOTHING ELSE. A
      module-level function - name it in the AGENTS.md discoverability idiom,
      two to four words carrying a domain word - takes the role and the
      originating class, returns route_role_call(role, originating_task_class),
      and returns None when and only when route_role_call raises
      OriginatingTaskClassRequired. No other exception is caught.
      WHY THE RAISE IS CAUGHT HERE AND NOWHERE ELSE, measured at 328228dc:
      `repair` is the SOLE member of TASK_CLASS_INHERITING_ROLES and also a
      member of KNOWN_ROLES, so resolve_role_config("repair") is an ordinary
      config resolution that has always worked and that this round must not
      break - G6 mutation (i) is the reviewer's proof that this is not
      hypothetical. None is `repair`'s HONEST answer at this layer: the role
      inherits its tier from the original task, and a config resolver has no
      original task to name. A direct caller still gets the raise, unchanged.

  (e) resolve_role_config RETURNS RoleConfig WITH routed_call SET from (d), and
      changes NOTHING about how provider, model and effort are resolved. The
      existing precedence chain, the provider-aware model default and the
      unknown-role warning are untouched.

  (f) THE PUBLIC API LIST of role_config.py gains a line for RoleConfig's new
      field and one for resolve_role_config's new parameter, in that docstring's
      existing style.

  (g) THE DELIBERATE ABSENCE, in the AGENTS.md discoverability idiom, in
      role_config.py's module docstring: Remedy deliberately does NOT select a
      model from the routed tier here. The seam answers a TIER and F110 maps no
      tier to a model id, so this round changes what a call RECORDS and nothing
      about which model runs. A reader searching here for the code that turns a
      tier into a model id must find that sentence, not a silent absence.

  (h) THE TWO SENTENCES THIS ROUND FALSIFIES IN model_routing.py, repaired in
      this same commit, DOCSTRING ONLY. FIRST, the opening paragraph's closing
      clause "no call site routes through the seam". SECOND, the whole paragraph
      beginning "Remedy deliberately does not WIRE THE SEAM INTO ANY CALL SITE
      YET", including "AT THIS COMMIT NOTHING CALLS IT". Replace both with what
      is TRUE after C3: the seam is wired at
      packages/orchestration/role_config.resolve_role_config, the one function
      all seven inventoried call sites already share, so a reader searching for
      the place a call routes lands there. KEEP unchanged the mission_compile
      paragraph and the "THE WORD TIER MEANS SOMETHING ELSE ONE MODULE OVER"
      paragraph; DECISION F110 D4 depends on the second. Measured at 328228dc:
      no test reads model_routing.__doc__ and none asserts that nothing imports
      the module, so this repair is owed to the reader, not to a gate.

SPEC - THE TEST COMMIT (C4), tests/orchestration/test_role_config.py
  New test classes and functions only; no existing test is touched. Every
  expected class and tier is READ from model_routing rather than spelled, in the
  idiom TestProviderAwareDefaults' docstring already sets for this file.

  (i) EVERY DECLARED ROLE CARRIES ITS EVIDENCE. Parametrized over the eight
      roles of ROLE_TASK_CLASSES: resolve_role_config(role).routed_call is a
      mapping whose keys are exactly ROUTED_CALL_EVIDENCE_FIELDS and whose
      task_class equals ROLE_TASK_CLASSES[role].
  (j) THE INHERITING ROLE ANSWERS None WITHOUT AN ORIGIN AND ROUTES WITH ONE.
      resolve_role_config("repair").routed_call is None. With
      originating_task_class supplied, it is a full mapping whose task_class is
      the originating one. Use TWO originating classes whose tiers DIFFER, so a
      constant cannot pass: the reviewer measured `architecture` at the top tier
      and `format` at the cheap tier at 328228dc.
  (k) THE UNDECLARED ROLE WARNS AND ROUTES CONSERVATIVELY. An unknown role still
      resolves, still returns the default provider, and its routed_call carries
      UNDECLARED_ROLE_TASK_CLASS with UNKNOWN_CLASS_REASON at TOP_TIER. Note
      that TWO warnings are now raised for such a role - role_config's own and
      model_routing's - and assert that BOTH are UserWarning rather than
      asserting a count of one.
  (l) RoleConfig IS STILL HASHABLE AND STILL COMPARES AS IT DID. hash() of a
      resolved config with real evidence succeeds; two configs for the same role
      compare equal when their provider, model and effort agree. This is the
      test that makes SPEC (b)'s compare=False a pinned property rather than a
      style choice, and mutation (iii) below is ordered against it.
  (m) THE WIRING CHANGED NO RESOLUTION. For every role in KNOWN_ROLES the
      resolved provider, model and effort are what they were - assert against
      DEFAULT_PROVIDER, DEFAULT_MODEL and DEFAULT_EFFORT - plus one case with a
      config_file override, so a routing fault cannot pass as a config change.
  (n) THE INVENTORY IS UNMOVED. model_routing.ROLE_CONFIG_CALL_SITES holds the
      same pairs after this round, because the wiring adds no call to
      resolve_role_config - it changes what that function DOES. Assert against
      the constant, never against a spelled numeral.

Done when - EIGHT GATES, each run and its real exit code recorded
  G1 TRANSPORT. sha256sum .agent/authored/f110-r9.md .agent/last_block.md -
     ONE digest twice. Report wc -l of the authored file. Per
     docs/agents/planner_reviewer_prompt.md item 37 this proves the saved copy
     and its mirror agree and claims nothing about the emitted bytes.
  G2 THE PLAN. cmp the PLAN9 extraction against .agent/plan.md - exit 0. Report
     wc -l (must be under 50) and grep -c for '^## Goal' and '^## Next Steps'
     (1 each).
  G3 THE LEDGER APPEND, .agent/live_review.md, full forensics. State the
     arithmetic 2185166 + 2 + len(RECORD8) against the real new size; show the
     pre-C2 content is an exact byte PREFIX; show it still ends WITHOUT a
     newline. SECOND READER: a script COUNTS N from the slice, then compares the
     LAST N blank-line units of the whole file against the slice's N paragraphs
     IN ORDER. NEGATIVE CONTROL: flip one byte inside the FIRST appended
     paragraph and show the second reader REJECTS it. Report the count of lines
     matching the RECORD8 header EXACTLY AS THE SLICE SPELLS IT - the separator
     after "R8" is U+2014 EM DASH, not a hyphen; copy the string from the
     extracted slice rather than retyping it - before C2 (expect 0) and after
     C2 (expect 1).
  G4 THE DECISIONS APPEND, .agent/decisions.md, full forensics, same five
     readings as G3 with its own convention: 731148 + 1 + len(DECISION4) + 1,
     ends with exactly ONE newline, second reader over the paragraphs it counts,
     negative control on the FIRST appended paragraph. Report
     grep -c '^## DECISION F110 D4 ' before and after C2. .agent/prose_slips.md
     gets a BYTE-EQUALITY check only, per the gate budget: final bytes ==
     before + 2 newlines + SLIPS9, with the base an exact prefix.
  G5 THE TWO MODULES, MEASURED AND RUN. git show --numstat for C3, per path.
     Run ast.parse over both real files. QUOTE EVERY DELETED LINE VERBATIM and
     name its region: for model_routing.py every deletion must be inside the
     MODULE DOCSTRING and any that is not is a STOP. Then RUN the shipped code
     and print what it RETURNED: resolve_role_config(role).routed_call for every
     member of KNOWN_ROLES, the "repair" answer with no origin and with each of
     two origins at different tiers, an unknown role, and hash() of a config.
  G6 THE RED PROOF, in a disposable worktree at C4, never cd-ed into, with
     __pycache__ purged and python3 -B. Print the imported module __file__ from
     inside the worktree to prove it is the worktree's copy. Run the UNMUTATED
     CONTROL FIRST and report its count and exit code. Then, one at a time,
     reverting between each:
       (i)   remove the OriginatingTaskClassRequired catch in the helper of (d)
       (ii)  the helper ignores its role argument and routes a fixed role
       (iii) drop compare=False from the field of (b)
       (iv)  the helper ignores originating_task_class and always passes None
     For each: the exit code, the number of failures, and the FULL LIST of red
     test ids, never truncated. State whether the red sets are pairwise disjoint
     - report what you MEASURED, do not assume. Read git status --porcelain ON
     THE PRIMARY CHECKOUT immediately after every mutation, in the same step.
     Every revert is a git checkout -- <exact path> INSIDE the worktree, and
     each must return the worktree to the control's count.
  G7 THE SUITES, each its own invocation, run serially, all exit 0. The
     reviewer ran all six at 328228dc with this round's change applied in a
     worktree, and the counts below are what they returned there - report yours
     beside them and explain any difference:
       pytest tests/orchestration/test_role_config.py -q          (34 at base;
         this round ADDS to it - report the number YOU measure, do not target
         a number this block names)
       pytest tests/orchestration/test_model_routing.py -q        (391 passed,
         3 skipped - UNMOVED; this round adds no test there)
       pytest tests/orchestration/test_teacher_model.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_orchestrator_model_routing.py tests/orchestration/test_job_role_routing.py tests/cli/test_teach_cmd.py -q   (87 - UNMOVED)
       pytest tests/test_do_job_flow.py tests/orchestration/test_job_evidence.py tests/orchestration/test_execution_config_evidence.py tests/orchestration/test_task_plan_evidence.py tests/orchestration/test_token_cost_policy.py tests/orchestration/test_model_aliases.py -q   (333 - UNMOVED)
       pytest tests/docs/ -q                                      (295 - UNMOVED)
       pytest tests/cli/test_golden_path.py -q                    (42 - the canary)
     The four UNMOVED suites are the round's regression evidence: they exercise
     the five call sites passing a role VARIABLE, where a wiring fault surfaces
     without any new test naming it.
  G8 THE TREE, THE COMMITS AND THE SWEEP. git status --porcelain empty
     immediately before C5 is staged. git ls-files .remedy-wt returns nothing.
     git worktree list shows no worktree of this round's making. Report
     git diff --stat 328228dc..<C4> -- docs/ (must be empty) and
     git diff --stat 328228dc..<C4> -- packages/ apps/ with
     role_config.py and model_routing.py EXCLUDED (must be empty) - that second
     command is constraint 6 MEASURED rather than asserted. Report the
     per-commit INSERTION count, the + column only, for every commit BEFORE the
     handback commit, cell by cell against the handback's own ## Commits table,
     and confirm each is under the AGENTS.md 500-insertion cap. The handback
     commit's own numbers go in neither place - the reviewer measures them at
     the next gate.

Handback - rewrite .agent/handoff.md per docs/agents/handback_template.md
  It carries: SESSION 3 of F110, round 9, rounds so far 9; the state block with
  the Fortschritt line; the item-status table with every SPEC item and every
  gate exactly once; the per-commit changed-files tables; one line per gate with
  its real result; the authored-text proofs; the deviations; the next step. NO
  length cap applies (AGENTS.md amend0827 rule 3) - do not declare one. Report
  the two STOP readings, and DECLARE any sentence outside the change set this
  round makes stale without repairing it.

<<<BEGIN PLAN9>>>
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

Round 9, session 3 — THE WIRING ROUND, the third and last clause of T001.
All seven inventoried call sites route through the seam in one change,
because all seven already funnel through `resolve_role_config`: that
function now calls `route_role_call` and carries the routed-call evidence
on the `RoleConfig` it already returns. DECISION F110 D4 rules where that
evidence lands. Round 8's PASS verdict and its prose slip are booked in
the same round.

## Next Steps

- The configuration round: the per-project override map and the promotion
  evidence map are READ from configuration rather than defaulting to the
  shipped table — consolidation order E.d.
- The acceptance round: a fixture run whose every call's evidence shows
  class, tier and reason, per the feature file's Acceptance section.
- The integration gate round, before closure.
- The closure sequence, which also runs the one checklist consolidation
  pass DECISION F110 D1 carries into it, and which updates the Design
  bullet of `docs/roadmap/features/T3_F110.md`.

## Risks

- `resolve_role_config` now calls into the policy layer, so a routing fault
  could become a config-resolution fault. `repair` is the live case: it
  raises when no originating class is supplied, which is why the wiring
  answers `None` there rather than breaking a resolution that worked.
- Recording is not selecting: the seam answers a TIER and F110 maps no tier
  to a model id, so this round changes what is RECORDED and nothing about
  which model runs.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
<<<END PLAN9>>>

<<<BEGIN RECORD8>>>
Gate: F110 R8 — the round 8 entry. VERDICT PASS, over the range `4cfcb464..f7765ec0` plus the handback commit `6d6988e7`. THE TRANSPORT PROOF COVERS THE SAVED COPY AND ITS MIRROR AND NOTHING MORE (§3 item 37): one digest `11b0c5855d8a82ee04728791ef426d8c5473ae15ca13025441c0cc35828eee5e` at 33816 bytes over `.agent/authored/f110-r8.md` at `50adb6a8`, its mirror at `e54c81fc` and both working copies at `6d6988e7`. The block is 399 lines against a projection of 399 — the fifth exact projection in a row — and under the §3 item 1 cap of 400. EVERY SLICE WAS RE-DERIVED BYTE FOR BYTE BY THE REVIEWER: `.agent/plan.md` equals PLAN8 plus the one trailing newline the target's convention adds, at 44 lines; `.agent/live_review.md` is 2177227 + 2 + 7937 = 2185166, the real size, still ending without a newline, base preserved as an exact prefix, second reader in order, negative control on the FIRST appended paragraph rejected; `.agent/decisions.md` is 728132 + 1 + 3014 + 1 = 731148, ending with exactly one newline, its eight paragraphs in order; `.agent/prose_slips.md` equals its base plus two newlines plus SLIPS8. DEVIATION D1 IS CORRECT AND THE BLOCK WAS WRONG: constraint 4 gave `.agent/prose_slips.md` as 53575 bytes where the real size at `4cfcb464` is 54853, and the reviewer confirms the arithmetic the worker could not have known to check — 53495 at `c1a3a3c4`, plus two newlines, plus SLIPS7's 1356 bytes, is 54853 exactly. The stated newline CONVENTION was right and G4 gated that file by byte equality rather than by arithmetic, so nothing on disk is wrong; recorded in `.agent/prose_slips.md` this round, no R-id, per amend0827-process-diet rule 2. THE DELETIONS WERE READ LINE BY LINE: C3 is 253 insertions against 6 deletions, all six in the module docstring, and C4 is 370 against 4, all four the test module's docstring, which said "four rounds" and was falsified by that round's own commit — constraint 9 repairs, deviation D3 declares, and no existing test function was edited, renamed, deleted or skipped. EVERY SHIPPED FUNCTION WAS RUN BY THE REVIEWER RATHER THAN READ: the role map declares eight roles, every declared class is a seed-table key, `repair` is the sole inheriting role, and the two sets cover `role_config.KNOWN_ROLES` exactly with nothing left over in either direction. THE REPAIR RULE IS EXECUTABLE AND DISCRIMINATES — the inheriting role answers `architecture` for an `architecture` origin and `format` for a `format` one, different classes at different tiers, and raises `OriginatingTaskClassRequired` when no origin is given. A declared role IGNORES an originating class. The undeclared role warns and answers `undeclared_role`, which the seam routes to the top tier with `unknown_class_conservative` — the A9 default. THE INVENTORY IS THE ROUND'S REAL DELIVERABLE AND THE REVIEWER RE-SWEPT IT INDEPENDENTLY: an AST walk of the reviewer's own over `packages/` and `apps/` finds seven calls to `resolve_role_config` and the multiset of (path, role) pairs equals `ROLE_CONFIG_CALL_SITES` entry for entry, including the DOUBLE call in `teacher_model.py`; five of the seven pass the role as a variable, which is why the inventory pins the call SITES. THE RED PROOF WAS RE-RUN IN FULL in a disposable worktree at `f7765ec0`, module path printed from inside it, primary checkout `git status --porcelain` read immediately after every mutation and CLEAN every time; control 391 passed and 3 skipped, the four mutations redden 5, 2, 3 and 5 ids, and THE FOUR RED SETS ARE PAIRWISE DISJOINT — the cleanest discrimination this feature has produced. Mutation (iii), dropping one inventory entry, reddens exactly three ids and every one is an inventory test, which is the proof the sweep compares against the constant instead of re-deriving it. One benign difference from the handback: the reviewer's mutation (i) reddens five where the worker reported four, because the two runs substituted different fixed classes; the property under proof is identical and holds in both. THE SUITES WERE RE-RUN BY THE REVIEWER at 391 passed with 3 skipped for the routing file — grown from 325, skip count unmoved — then 33, 34, 63, 295 and 42, every one exit 0. CONSTRAINT 6 WAS MEASURED, NOT ASSERTED: `git diff --name-only 4cfcb464..f7765ec0 -- packages/ apps/` lists `packages/orchestration/model_routing.py` and nothing else, and `git diff --stat` over `docs/` is empty. The per-commit insertion counts match the handback's Commits table cell by cell — 399, 305, 16, 55, 253, 370 — every one under the AGENTS.md cap; `6d6988e7` is 463 insertions against 578 deletions, a full-file rewrite of a single `.agent/**` state file and exempt under DECISION F104 D1. The open set is 278 over 347 registered and 69 resolved, UNCHANGED; the round minted no id and `R-0767` stays OPEN. The tree is clean, `git ls-files .remedy-wt` returns nothing, no worktree of the round's making survives, `.agent/candidates.md` is untouched and still EMPTY, and the branch is pushed with no pull request open.
<<<END RECORD8>>>

<<<BEGIN SLIPS9>>>
2026-09-03 · F110 R8 · Constraint 4 of the round 8 block stated `.agent/prose_slips.md` as 53575 bytes at `4cfcb464` where the file really held 54853 — the reviewer re-derived the figure by arithmetic from an earlier round's base instead of re-measuring it at the round's own base. The stated newline convention was correct and G4 gated that file by byte equality rather than by arithmetic, so the append landed exact and nothing on disk was wrong; the worker applied the constraint as written and declared the discrepancy, which is what constraint 1 asks for. THE LESSON: a byte figure quoted for one round's base is RE-MEASURED at the next round's base, never carried forward or re-derived in the reviewer's head. Reviewer block-authoring slip, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIPS9>>>

<<<BEGIN DECISION4>>>
## DECISION F110 D4 (2026-09-03, round 9) — where the routed-call evidence lands

CONTEXT. Round 8 shipped `route_role_call`, the single seam, and left it
wired to nothing. Round 8's verdict refused to rule on the sink without
measuring the surfaces that already carry a field of nearly the same name,
and named that measurement as session 3's opening work. It has now been
taken, at `328228dc`.

WHAT WAS MEASURED. Four production surfaces carry `model_routing_tier` or
`model_routing_plan.tier`: `packages/orchestration/progress_ledger.py`,
`packages/orchestration/review_bundle.py`,
`packages/orchestration/ui_server.py` and
`apps/cli/commands/orchestrator_cmd.py`. All four read the SAME source — the
`model_routing_plan` of an `orchestrator_brain` decision record — whose
vocabulary is HUMAN_REVIEW_REQUIRED / EXTERNAL_BUILDER_NEEDED /
local_advisor_preferred. That answers WHEN a job escalates to a human or an
external builder. It has nothing to do with F110's cheap/mid/top, and the
name is fully occupied across all four.

CHOSEN. The sink is the `RoleConfig` object `resolve_role_config` already
returns, carrying the evidence as ONE nested mapping field whose keys are
exactly `ROUTED_CALL_EVIDENCE_FIELDS`. One change wires all seven
inventoried call sites, because all seven already funnel through that
function. `role_config.py` imports `model_routing.py` — config depending on
policy, the direction that module's docstring permits — and no cycle is
possible: `model_routing.py` imports only `warnings` and `dataclasses`.

REJECTED, AND WHY.
(1) Flatten the four evidence keys onto `RoleConfig` as top-level fields.
    Rejected: `tier` and `reason` are bare generic words, AGENTS.md's
    discoverability section requires two to four words including a domain
    word, and any name close to `model_routing_tier` collides with the
    escalation vocabulary measured above. Nesting keeps ONE spelling.
(2) Edit each of the seven call sites. Rejected: all seven already share the
    resolver, so seven edits buy exactly what one buys, and every future call
    site would then have to REMEMBER to route. Wiring the resolver makes
    routing the default and an unrouted call site impossible by construction.
(3) Push the evidence into the ledger, the review bundle or the UI this
    round. Rejected: those surfaces read an orchestrator-brain DECISION
    record, not a provider call, so F110's evidence has no existing row
    there. Adding one is a new surface rather than a wiring, and the feature
    file gives that to the report's cost section. Deferred, and named here so
    the round that wants it finds this paragraph.
(4) Widen `packages/orchestration/call_identity.py`'s `CallIdentity`, which
    already carries a `role`. Rejected: that is F012's structure and widening
    it reaches the providers, the ping-pong loop and the run manifest — out
    of T001's scope and against the feature file's "Do not touch".

CONSEQUENCE. Recording is not selecting. The seam answers a TIER and F110
deliberately maps no tier to a model id, so this wiring changes what a call
RECORDS and nothing about which model runs. That absence is stated in
`role_config.py`'s module docstring in the AGENTS.md idiom rather than left
to be rediscovered. The inheriting role `repair` records `None` at this
layer, because a config resolver has no originating task to name, and
`route_role_call` still raises for every direct caller.

REVERSE THIS DECISION by deleting the `routed_call` field and its helper from
`packages/orchestration/role_config.py`, restoring the two docstring
paragraphs in `packages/orchestration/model_routing.py` from `328228dc`, and
deleting this paragraph.
<<<END DECISION4>>>
