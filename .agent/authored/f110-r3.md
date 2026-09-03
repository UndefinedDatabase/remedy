STEP F110 T001c / ROUND 3 - F110 Model routing by task class
FEATURE F110 - Model routing by task class (Tier 3) - SESSION 1, ROUND 3

Goal
  Consolidation order E.b: make the orchestrator role's model resolve THROUGH
  role_config instead of being a third, independent answer to "which model", and
  book round 2's PASS verdict into the ledger in the same round.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f110-r3.md
  C0b mirror it to .agent/last_block.md
  C1  apply PLAN3 to .agent/plan.md (FIRST substantive commit, item 23)
  C2  append RECORD2 to .agent/live_review.md and SLIPS3 to
      .agent/prose_slips.md - round 2's verdict, booked
  C3  THE PRODUCTION COMMIT: resolve_orchestrator_model per SPEC CODE
  C4  THE TEST COMMIT: the new tests per SPEC TESTS
  C5  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f110-r3.md (new, C0a) · .agent/last_block.md (C0b) ·
  .agent/plan.md (C1) · .agent/live_review.md (C2) ·
  .agent/prose_slips.md (C2) · packages/orchestration/role_config.py (C3) ·
  packages/orchestration/gauntlet_runner.py (C3) ·
  apps/cli/commands/mission_cmd.py (C3) ·
  tests/orchestration/test_orchestrator_model_routing.py (new, C4) ·
  .agent/handoff.md (C5)

BASE for this round is 490f575f. Every byte and count below was measured there.

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by delimiter
     index from the COMMITTED .agent/authored/f110-r3.md - marker lines
     EXCLUDED - and write it with a script, never by retyping. If a slice looks
     wrong, apply it as written and DECLARE it in the handback.
  2. C1 is the first substantive commit; this round touches the finding ledger,
     so item 23 binds.
  3. C3 (production) precedes C4 (tests). Do not reorder.
  4. Newline conventions, MEASURED at 490f575f: .agent/live_review.md ends
     WITHOUT a trailing newline (2149060 bytes) and must still end without one
     after C2; .agent/prose_slips.md likewise ends WITHOUT one; .agent/plan.md
     ends WITH one. Each append is the two bytes newline newline then the slice.
     Where an extractor yields a trailing newline the target does not take, the
     TARGET's convention wins.
  5. NO RUFF GATE IS ORDERED and you must not add one; the reviewer lints C3 and
     C4 itself. Write to the repository's existing style and say nothing of lint.
  6. THIS ROUND CHANGES NO BEHAVIOUR AT TODAY'S CONFIGURATION and that is
     deliberate. The reviewer MEASURED at 490f575f that
     role_config.resolve_role_config("orchestrator").model and the planner's own
     default both answer the SAME model id, so the seam moves without the running
     system moving. That is exactly why SPEC TESTS orders a PATCHED
     discriminator: a test that merely compared the two sources today would pass
     before the change as well and would prove nothing (§3 item 27).
  7. A sentence OUTSIDE the change set that this round makes stale is DECLARED
     in the handback and NOT repaired.
  8. Read .agent/STOP from disk before the first commit and again before C5. If
     it exists, finish the commit in hand, write the handback, and stop.
  9. Self-review loop before every commit. Push after C5. No pull request, no
     merge. Destructive verification only inside a disposable git worktree.

SPEC CODE - written by YOU. Two files change plus the new function.

  (a) A NEW PUBLIC FUNCTION in packages/orchestration/role_config.py:

        def resolve_orchestrator_model() -> str

      Semantics, which are the config key's OWN documented promise and not a new
      policy: return the `orchestrator.model` project-config value when it is set
      and non-empty; otherwise return
      `resolve_role_config("orchestrator").model`, i.e. the same answer every
      other role gets. `packages/orchestration/config.py` at 490f575f describes
      that key as "the ONLY orchestrator-specific routing surface" and says
      "Unset means the role resolves exactly like every other one" - this
      function is what makes that sentence true in code. Import `get_config`
      INSIDE the function body: role_config has no module-level import of config
      at 490f575f and this module is imported early by others. Add the function
      to the module docstring's Public API list, which already names
      KNOWN_ROLES, RoleConfig and resolve_role_config. Carry a one-line WHY
      comment above the def per AGENTS.md Code Discoverability.

  (b) THE TWO CALL SITES. Both currently read exactly:

        OrchestratorMove, model=get_config().get("orchestrator.model") or None)

      one in packages/orchestration/gauntlet_runner.py and one in
      apps/cli/commands/mission_cmd.py. Replace the `model=` argument at each
      with `model=resolve_orchestrator_model()`, importing the function the way
      each module already imports its collaborators. Leave the surrounding call
      and every other argument untouched. If either file's `get_config` import
      becomes unused, remove it; if it is still used elsewhere in the file,
      leave it - report which case each file was.

SPEC TESTS - NEW FILE tests/orchestration/test_orchestrator_model_routing.py
  Unit tests over `resolve_orchestrator_model` only. Cover:
    - the configured key WINS: with `orchestrator.model` set to a sentinel the
      function returns that sentinel;
    - the key UNSET falls through to role_config, and this case MUST use a
      PATCHED discriminator so it can fail: force
      `resolve_role_config("orchestrator").model` to a sentinel that the
      planner's own default is not, and assert the function returns the
      SENTINEL. Comparing the two unpatched sources proves nothing today,
      because constraint 6 records that they already agree;
    - an EMPTY or whitespace-only configured value is treated as unset;
    - the returned value is always a non-empty string.
  Patch through pytest's monkeypatch against the names the function actually
  resolves at call time. Do not assert the literal model id anywhere.

Done when - the gates. Run each, record the REAL exit code and the REAL output.

  G1 TRANSPORT. After C0b: sha256sum .agent/authored/f110-r3.md
     .agent/last_block.md - one digest twice, both lines verbatim. This proves
     the saved copy and its mirror agree and nothing more. ALSO report
     wc -l .agent/authored/f110-r3.md: the reviewer's own pre-emission
     projection is 233 lines, and reporting the committed file's real count is
     what turns that projection into a measurement rather than a trusted number.
     A difference is reported, not repaired - the §3 item 1 cap is 400.
  G2 THE PLAN. Extract PLAN3 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md          -> exit 0
       wc -l .agent/plan.md                    -> report; must be under 50
       grep -c '^## Goal' .agent/plan.md       -> 1
       grep -c '^## Next Steps' .agent/plan.md -> 1
  G3 THE LEDGER APPEND, full arithmetic, the record file. For RECORD2 at C2
     against the size immediately before that commit: report before + 2 + slice
     length, the real new size, and whether they are equal. Then a SECOND READER
     that counts no byte: split the WHOLE file on blank-line boundaries, let N be
     counted BY THE SCRIPT from the slice, and report whether the LAST N units
     equal the slice's N paragraphs IN ORDER. Then a NEGATIVE CONTROL: in a
     scratch copy flip one byte inside the FIRST appended paragraph and report
     that the second reader REJECTS it. Also report
     grep -c '^Gate: F110 R2 — ' .agent/live_review.md, which must be 0 before
     C2 and 1 after.
  G4 THE PROSE FILE. Byte-equality check ONLY: report whether the final bytes of
     .agent/prose_slips.md equal the extracted SLIPS3 slice, whether the pre-C2
     content is preserved as an exact byte PREFIX, and whether the file still
     ends without a newline.
  G5 THE PRODUCTION CHANGE. For each of the three changed files report
     git show --numstat C3 -- <path>, and additionally:
       count of 'resolve_orchestrator_model' in each file AFTER C3
       count of the string 'orchestrator.model' in gauntlet_runner.py and
         mission_cmd.py BEFORE C3 and AFTER C3
       whether each file still parses, via ast.parse on its real text
     Report the diff's added and removed lines verbatim for all three files. The
     change must be the new function, its docstring entry, and the two model
     arguments - nothing else.
  G6 THE MUTATION RED PROOF, in a disposable git worktree at the C4 commit and
     NEVER in the primary checkout. Report the UNMUTATED CONTROL FIRST: run the
     new test file and report its exit code and count. Then mutate ONLY the
     fall-through branch of resolve_orchestrator_model so it ignores role_config
     and returns the planner's default path instead, and report which test ids go
     RED. THE DISCRIMINATOR: the unset-key case must redden while the
     configured-key case stays GREEN. Both red, or neither, is a FAILED proof -
     report it as such rather than reporting a colour. Purge __pycache__ and run
     python3 -B, print the imported module's __file__ to prove the worktree copy
     is the one under test, then remove the worktree and prune.
  G7 THE SUITES, EACH AS ITS OWN INVOCATION, RUN SERIALLY. Measured by the
     reviewer at 490f575f:
       python3 -m pytest tests/orchestration/test_orchestrator_loop.py tests/cli/test_worker_facade_cmd.py tests/orchestration/test_role_config.py -q   298 passed
       python3 -m pytest tests/orchestration/test_orchestrator_model_routing.py -q   report the count
       python3 -m pytest tests/orchestration/test_job_role_routing.py -q              14 passed
       python3 -m pytest tests/cli/test_golden_path.py -q                             42 passed
     A moved count in the first, third or fourth is the finding.
  G8 THE TREE, THE COMMITS AND THE SWEEP. Read git status --porcelain
     immediately before C5 is staged, git ls-files .remedy-wt (no output), and
     git worktree list (no worktree of this round's own making). Then, for C0a
     through C4 - the commits BEFORE the handback commit, per item 14 - report
     each one's insertion count from git show --numstat, the '+' column ONLY,
     and compare it CELL BY CELL against the Commits table of the handback you
     are writing. C5's own numbers go to neither a round report nor this file;
     the reviewer measures them at the next gate. Then THE STALENESS SWEEP over
     every file this round touched, one entry per file, stale or NOT stale, why.

Handback
  Rewrite .agent/handoff.md per docs/agents/handback_template.md: SESSION 1 of
  F110, round 3, the state block, the item-status table with every ordered item
  appearing exactly once, the Commits table, one line per gate then the
  transcripts, the deviations, the next steps. No length cap.

SLICES. Each slice lies between its own one-line BEGIN and END marker. The
marker lines are NEVER part of the slice. The slices carried here are PLAN3,
RECORD2 and SLIPS3.

<<<BEGIN PLAN3>>>
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

Round 3, session 1 — T001c, consolidation order E.b. The orchestrator's
model is read today straight from the `orchestrator.model` config key at
two call sites, bypassing `role_config` entirely, so it is a third
independent answer to "which model". This round routes it through
`role_config` while keeping the config key exactly as the operator-facing
surface it already is. Round 2's PASS verdict is booked in the same round.

## Next Steps

- T002: the resolver proper — the class table seeded from
  `docs/agents/model_routing_policy.md`, the config schema, the hard-rule
  checks, and one violating fixture per rule refused with the rule named.
  Consolidation order E.d puts the per-call-site class declarations here,
  AFTER the seam work, so a declared class cannot record a routing reason
  that a rival mechanism then overrode.
- T003: the promotion-evidence discipline, the evidence fields and the
  goldens — a promotion without evidence refused, with evidence logged.
- The integration gate, then the closure sequence, which also runs the one
  checklist consolidation pass DECISION F110 D1 carries into it.

## Risks

- E.b is behaviour-neutral at today's configuration: the two sources
  already answer the same model id. That is measured, not assumed, and it
  is why the round's tests use a patched discriminator rather than
  comparing the two sources.
- E.c is deliberately NOT done. Rebinding `make_structured_call_fn`'s
  Ollama planner is failover work and the feature file puts it out of
  scope; the inventory's section G records the distinction.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
<<<END PLAN3>>>

<<<BEGIN RECORD2>>>
Gate: F110 R2 — the round 2 entry. VERDICT PASS, over the range `bbfbb83b..490f575f`. THE TRANSPORT PROOF IS AGAIN NAMED FOR WHAT IT COVERS (§3 item 37): one digest `f7a27a7fb401e8d4859af018daa75ebd3f06515da8e4716f27f3276d70c4f27c` over `.agent/authored/f110-r2.md` and `.agent/last_block.md` shows the saved copy and its mirror agree, and the reviewer holds no scratch original, so no claim is made about the emitted bytes. EVERY SLICE WAS RE-DERIVED BYTE FOR BYTE BY THE REVIEWER: `.agent/plan.md` equals PLAN2 exactly; `.agent/live_review.md` equals its base plus two newlines plus RECORD1 plus two newlines plus DONE1, with the file still ending without a newline; and `.agent/prose_slips.md` equals its base plus two newlines plus SLIPS2, its base preserved as an exact byte PREFIX. THE PRODUCTION CHANGE IS EXACTLY WHAT WAS ORDERED AND NOTHING MORE — `git show 5bbb0cde` reads +28/-2 over `packages/orchestration/pingpong_job.py`, the new `default_role_provider_name` plus the two third arguments, with every other `_resolve_cfg` default untouched and the source taxonomy unchanged. THE REVIEWER LINTED IT ITSELF, which round 1 established is the reviewer's job because the worker's permission layer refuses the tool: `ruff check` over the changed module and both changed test files answers "All checks passed!". THE MUTATION RED PROOF WAS NOT TAKEN ON TRUST — THE REVIEWER RE-RAN IT in its own disposable worktree at `490f575f`, with the module path printed to confirm the worktree's copy was the one imported: the UNMUTATED CONTROL is 14 passed at exit 0, and with the fallback line mutated to `return "fake"` the run is 9 failed and 5 passed at exit 1. THE DISCRIMINATOR HOLDS: all nine reddened ids are no-injection or unusable-name cases, and all four `TestInjectedProvider` cases stayed GREEN, so the proof distinguishes the defect from its neighbour rather than merely producing a colour. The worker's own deviation D5 is right and honest — the fifth surviving test is a shape check that cannot discriminate, and it said so instead of counting it as evidence. THE SHIPPED FUNCTION WAS RUN, not read: no injection answers `ollama` for both `builder` and `reviewer`, matching `role_config.resolve_role_config(role).provider`; an injected `FakeProvider` answers `fake`; an injected custom name answers that name; and an object with no name, an empty name or a non-string name all fall back to `ollama`. So `R-0768`'s defect is genuinely gone: an unflagged run now records the resolved product default instead of a literal the run never used. THE SUITES WERE RE-RUN BY THE REVIEWER, each as its own invocation and serially, at 191, 75, 383, 14 and 42, every one exit 0. The 191 is the load-bearing one: `tests/orchestration/test_job_task_runner.py` HELD its count with the six fixtures repaired, so NO SEVENTH TEST MOVED, which the block made the condition of the repair being correct rather than convenient. THE SIX FIXTURE REPAIRS WERE READ LINE BY LINE and each adds only `builder="fake"` and `reviewer="fake"` to a `_make_args` call: no assertion was weakened, no expected value changed, no test deleted. DEVIATION D2 IS ACCEPTED AND IS BETTER THAN THE BLOCK: three of the six tests carry TWO `_make_args` calls and the worker repaired only the first, because the second is the CONTINUATION run whose neighbouring test asserts `builder_source == "persisted"` — naming the provider there would have destroyed the very precedence the test exists to pin. DEVIATION D4 IS ACCEPTED: the new default is evaluated eagerly at every `run_job` call by Python's argument order, even when an explicit or persisted value wins, and the worker verified the function is pure — `resolve_role_config` reads tables, returns a frozen dataclass, performs no I/O and emits no warning for `builder` or `reviewer`. THE OPEN SET MOVED BY EXACTLY ONE, from 279 to 278 over 347 distinct registered ids and 69 distinct resolved, and `R-0768` is the only id that moved; `R-0767`, its sibling on the same seam, is untouched and stays OPEN, which is correct because it widens a CLI allow-list and reaches no resolver. A CORRECTION THIS RECORD OWES, appended rather than written over the landed text, per §3 item 20: `.agent/f110_inventory.md` section F says of `R-0767` and `R-0768` that "Both stay REGISTERED and unrepaired on this branch", and that sentence is now FALSE for `R-0768`, which this round resolved. It was true when it was written at `94150e14` and the same paragraph predicted its own falsification by naming the round that would do it, so the inventory is NOT rewritten — this dated correction is the repair the record permits. THE TREE is clean, `git ls-files .remedy-wt` returns nothing, no worktree of the round's own making survives, the nine committed paths are exactly the change set, and the branch is pushed at `490f575f`.
<<<END RECORD2>>>

<<<BEGIN SLIPS3>>>
2026-09-03 · F110 R2 · The reviewer's own pre-emission count of the round 2 block projected 262 lines while the block as committed is 263, measured on `.agent/authored/f110-r2.md` — the same off-by-one as the round 1 projection of 397 against a committed 398, and from the same cause: the projection SUMS per-slice line counts plus hand-counted marker and blank lines instead of counting assembled bytes. The §3 item 1 cap of 400 was met with room in both rounds and no gate consumed the projected figure. THE COUNTER-MEASURE RECORDED HERE IS THE ONE ACTUALLY AVAILABLE, because the obvious one is not: assembling a block of this size in a single pass to count it exceeds the reviewer's own tooling limit, so from round 3 on every block's gate G1 additionally reports `wc -l` of the COMMITTED authored file, which turns the projection into a measurement the round itself checks rather than a number the reviewer is trusted on. Reviewer-prose miscount, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIPS3>>>
