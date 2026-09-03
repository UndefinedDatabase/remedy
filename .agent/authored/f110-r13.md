STEP F110 T003 / ROUND 13 - F110 Model routing by task class
FEATURE F110 - Model routing by task class (Tier 3) - SESSION 3, ROUND 13

Goal
  THE EVIDENCE WIRING ROUND, and the last unbuilt clause of T003. The parser
  round 12 landed gets its caller: the config-reading layer reads
  `model_routing.promotion_evidence`, parses it, and hands the records BOTH to
  the table builder - so a documented benchmark run actually licenses a cheaper
  tier - AND to the seam, so a routed call records WHAT promoted it. Book round
  12's PASS verdict and one prose slip in the same round.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f110-r13.md
  C0b mirror it to .agent/last_block.md
  C1  apply PLAN13 to .agent/plan.md (FIRST substantive commit, item 23)
  C2  append RECORD12 to .agent/live_review.md and SLIPS13 to
      .agent/prose_slips.md
  C3  PRODUCTION: the wiring, and the docstring sentences it falsifies
  C4  TESTS: evidence reaching the table, the seam and a routed call
  C5  DOCS: the configuration document gains the evidence key
  C6  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f110-r13.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/plan.md (C1) - .agent/live_review.md (C2) -
  .agent/prose_slips.md (C2) -
  packages/orchestration/role_config.py (C3) -
  packages/orchestration/model_routing.py (C3, DOCSTRING ONLY) -
  tests/orchestration/test_role_config.py (C4) -
  docs/system/remedy-toml-configuration-system-v0.md (C5) -
  .agent/handoff.md (C6)
  packages/orchestration/config.py IS NOT TOUCHED - round 12 registered the key
  and nothing more is owed there. If any commit would exceed the AGENTS.md
  insertion cap, SPLIT IT; such a split is pre-authorised and is not a deviation.

BASE for this round is f943e436. Every byte, count, citation and measurement
below was taken there by the reviewer.

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by delimiter
     index from the COMMITTED .agent/authored/f110-r13.md - marker lines
     EXCLUDED - and write it with a script, never by retyping. If a slice looks
     wrong, apply it as written and DECLARE it in the handback.
  2. C1 is the first substantive commit; this round touches the finding ledger,
     so item 23 binds.
  3. C3 precedes C4 precedes C5. Do not reorder.
  4. Newline conventions, MEASURED at f943e436 - re-measured at THIS round's
     base, never carried forward. .agent/live_review.md is 2209946 bytes and
     ends WITHOUT a trailing newline; its append is the two bytes newline
     newline then the slice, and it must still end without one.
     .agent/prose_slips.md is 61137 bytes, same shape, same two-byte append.
     .agent/plan.md is 2106 bytes and ends WITH one. Where an extractor yields a
     trailing newline the target does not take, the TARGET wins.
     .agent/decisions.md IS NOT TOUCHED this round.
  5. NO RUFF GATE IS ORDERED and you must not add one; the reviewer lints it.
     Sort any import block you touch as ruff's isort would - an ALL-CAPS name
     sorts ABOVE a CamelCase one in a `from ... import (...)` list.
  6. THIS IS A DOCS ROUND, so tests/docs/ is a gate - see G7. Only the ONE
     documentation file in the change set is edited and docs/roadmap/ is NOT
     touched.
  7. ROUNDS 4 THROUGH 12 SHIPPED BEHAVIOUR IS NOT REVISED. Every constant and
     function keeps its behaviour and its SIGNATURE - in particular
     `resolve_effective_task_class_tiers()` still takes no argument and still
     returns a plain dict, and `promotion_evidence_from_mapping` is CALLED, not
     changed. model_routing.py is edited for its MODULE DOCSTRING ONLY and any
     deletion outside that docstring is a STOP.
  8. NO EXISTING TEST IS EDITED, RENAMED, DELETED OR SKIPPED. Every addition is
     a NEW name. If you find an existing test that must change, STOP, do not
     change it, and report it as a blocked item in the handback.
  9. A sentence this round makes stale INSIDE the change set is repaired in the
     commit that falsifies it. A sentence OUTSIDE the change set that this round
     makes stale is DECLARED in the handback and NOT repaired.
 10. Read .agent/STOP from disk before the first commit and again before C6.
 11. Destructive verification runs ONLY inside a disposable git worktree, never
     in the primary checkout. Purge __pycache__ before every run, use python3
     -B, remove the worktree BY ITS EXACT PATH when done, and prune.
 12. NO remedy.toml IS CREATED IN THE REPOSITORY ROOT. Tests write TOML to a
     pytest tmp_path; any probe writes outside the repository root.

SPEC - C3, the wiring
  This is a SPEC, not a slice: write it in each module's own idiom and improve
  on any wording below that is worse than what you would write. Do not depart
  from the BEHAVIOUR without declaring it.

  (a) THE KEY GETS A NAMED CONSTANT in role_config.py, beside the existing
      `TASK_CLASS_TIERS_CONFIG_KEY`, holding "model_routing.promotion_evidence".
      Spell the key once.
  (b) A READER, `resolve_promotion_evidence`, returns the parsed records: it
      reads that key from the configuration and returns an EMPTY mapping when
      the value is unset, empty, or not a Mapping - the same three-way guard
      `resolve_effective_task_class_tiers` already applies to the tiers table,
      and for the same reason, since an env var cannot carry a table and a bare
      string can arrive on that path. Otherwise it returns
      `model_routing.promotion_evidence_from_mapping(raw)`. Import get_config
      INSIDE the function body, the idiom this module already uses.
  (c) THE TABLE BUILDER RECEIVES THE EVIDENCE.
      `resolve_effective_task_class_tiers` passes it to
      `build_effective_task_class_tiers` as `promotion_evidence`. ITS SIGNATURE
      AND RETURN TYPE DO NOT CHANGE - constraint 7. This is the line that makes
      a documented run license a cheaper tier: without it every promotion is
      refused with `promotion_without_evidence`, which is exactly what round 12
      measured.
  (d) THE SEAM RECEIVES THE EVIDENCE TOO. `resolve_routed_call_evidence` passes
      the same records to `route_role_call` as its `promotion_evidence`
      argument, so a routed call's `promoted_by` names the run instead of being
      None. Both consumers may call the reader in (b) separately: `get_config`
      is cached, so the cost is a dict lookup and a small parse, and keeping the
      existing signatures is worth more than saving it. Say so in a comment
      rather than leaving the double call to look accidental.
  (e) THE PUBLIC API DOCSTRING LIST GAINS EVERY NEW PUBLIC NAME - both the
      constant of (a) and the function of (b). Derive that list from the round's
      new public names, not from the SPEC items that happen to mention the
      docstring; getting that wrong cost round 9 a declared deviation.
  (f) THE TWO SENTENCES THIS ROUND FALSIFIES IN model_routing.py, repaired in
      the SAME commit, DOCSTRING ONLY. FIRST, the paragraph beginning "Remedy
      deliberately does not CALL :func:`promotion_evidence_from_mapping` from
      anywhere in production yet" - the wiring round it names as future is THIS
      round. SECOND, in the paragraph about not reading a config file, the
      clause "it arrives with the resolver-seam round" - that round landed at
      `6c7fb4eb` and the loader in fact arrived across rounds 10 and 13, so the
      clause misdates itself; repair the DATING and KEEP the paragraph's actual
      claim, which is still true and still load-bearing: this module reads no
      config file and imports config.py from nowhere. Replace the first
      paragraph with what is TRUE after C3 - the parser's caller is
      `resolve_promotion_evidence` in role_config.py - so a reader searching for
      it lands there.

SPEC - C4, tests/orchestration/test_role_config.py
  New tests only. Read every class, tier, field and rule name from the modules
  rather than spelling it. Build the evidence record from a TOML file written to
  tmp_path and loaded through `load_config`, so the test exercises the REAL
  config path and not a hand-built dict.
  (g) A PROMOTION WITH EVIDENCE IS ACCEPTED END TO END. Configure BOTH tables -
      a tiers table promoting a top-tier class to the cheapest tier, and an
      evidence table for that class meeting the bars - and assert that
      `resolve_effective_task_class_tiers()` returns that class at the promoted
      tier, with NO warning raised.
  (h) A ROUTED CALL NAMES WHAT PROMOTED IT. For a role whose declared class is
      the promoted one, assert `resolve_role_config(role).routed_call` carries
      the promoted tier, the OVERRIDE reason, and a `promoted_by` that is not
      None and contains the model id the evidence names. THE REVIEWER MEASURED
      the shape that string takes at f943e436, running the real functions:
      `qwen3-8b-instruct + q4_k_m@0f1e2d3c4b5a6978 on F082`. Assert on a
      SUBSTRING you take from the configured evidence, never on that whole
      literal.
  (i) THE SAME PROMOTION WITHOUT EVIDENCE IS STILL REFUSED. Configure the tiers
      table alone and assert the warning names
      `RULE_PROMOTION_WITHOUT_EVIDENCE`, read from the constant, and that the
      class comes back at its SEEDED tier.
  (j) AN UNSET EVIDENCE KEY CHANGES NOTHING. With no evidence configured,
      `resolve_promotion_evidence()` is empty and every routed answer is
      identical to what it was before this round.
  (k) A MALFORMED EVIDENCE VALUE IS NOT A CRASH. A bare string where the table
      belongs yields an empty mapping and a routed call that still resolves,
      with provider, model and effort unchanged - the D5 principle, one layer on.
  (l) `select` A CLASS AND ROLE BY READING THE TABLES. `architecture` is seeded
      at the top tier and is the declared class of `design_worker`, measured at
      f943e436; take them from `TASK_CLASS_TIERS` and `ROLE_TASK_CLASSES` rather
      than spelling them, so a later re-seeding moves the test with the data.

SPEC - C5, docs/system/remedy-toml-configuration-system-v0.md
  (m) The registered-key table gains a row for `model_routing.promotion_evidence`
      in the file's existing column shape - the reviewer measured the neighbour
      row as `| model_routing.task_class_tiers | table | (TOML only) | (none) | no |`.
  (n) The table-valued-keys section covers BOTH keys. Its heading currently
      names only the tiers key; widen the heading so it names the CONCEPT rather
      than one key, and add a short subsection for the evidence table with a
      fenced TOML example including the nested `assertion_results`, one sentence
      that a record failing the bars or missing fields licenses nothing so the
      class keeps its seeded tier, and one sentence that hard rules still win.
      Read the file first and match its heading levels and prose register. Do
      NOT restate the promotion bars - docs/agents/model_routing_policy.md owns
      them - and do not touch any other section.

Done when - EIGHT GATES, each run and its real exit code recorded
  G1 TRANSPORT. sha256sum .agent/authored/f110-r13.md .agent/last_block.md -
     ONE digest twice. Report wc -l of the authored file. Per
     docs/agents/planner_reviewer_prompt.md item 37 this proves the saved copy
     and its mirror agree and claims nothing about the emitted bytes.
  G2 THE PLAN. cmp the PLAN13 extraction against .agent/plan.md - exit 0.
     Report wc -l (must be under 50) and grep -c for '^## Goal' and
     '^## Next Steps' (1 each).
  G3 THE LEDGER APPEND, full forensics. State the arithmetic
     2209946 + 2 + len(RECORD12) against the real size after C2; show the pre-C2
     content is an exact byte PREFIX; show the file still ends WITHOUT a
     newline. SECOND READER: a script COUNTS N from the slice, then compares the
     LAST N blank-line units of the whole file against the slice's N paragraphs
     IN ORDER. NEGATIVE CONTROL: flip one byte inside the FIRST appended
     paragraph and show the second reader REJECTS it. Report the count of lines
     matching the RECORD12 header EXACTLY AS THE SLICE SPELLS IT - the separator
     after "R12" is U+2014 EM DASH, not a hyphen; copy the string from the
     extracted slice - before C2 (expect 0) and after C2 (expect 1).
  G4 .agent/prose_slips.md gets a BYTE-EQUALITY check only, per the gate budget:
     final bytes == 61137 + 2 newlines + SLIPS13, base an exact prefix, still
     ending without a newline. Then report the OPEN FINDING SET after C2,
     derived mechanically as a SET DIFFERENCE OVER UNIQUE IDS - every
     '^- R-\d+ — ' paragraph minus every '^Done: R-\d+ — ' line, each reduced to
     a set of distinct ids before subtracting, because two ids in this ledger
     carry two Done paragraphs each and a LINE count reads two low. Report the
     unique registered count, the unique resolved count and the open count, and
     confirm R-0767 is in the open set.
  G5 THE TWO PRODUCTION FILES, MEASURED AND RUN. git show --numstat for C3, per
     path. ast.parse over both. QUOTE EVERY DELETED LINE VERBATIM and name its
     region; for model_routing.py every deletion must be inside the MODULE
     DOCSTRING and any that is not is a STOP. Then RUN the shipped code against
     TOML written OUTSIDE the repository root and print what it RETURNED: the
     parsed evidence for a configured table; the effective table for the four
     states of SPEC (g), (i), (j) and (k); and for each, the full routed_call a
     declared role gets, including `promoted_by`. Print the full text of any
     warning raised.
  G6 THE RED PROOF, in a disposable worktree at C4, never cd-ed into,
     __pycache__ purged, python3 -B, module __file__ printed from inside it.
     Control first, with its count and exit code. Then, one at a time, reverting
     between each:
       (i)   the evidence is NOT passed to build_effective_task_class_tiers
       (ii)  the evidence is NOT passed to route_role_call
       (iii) the reader returns the RAW mapping instead of the parsed records
       (iv)  the not-a-Mapping guard is dropped from the reader
     For each: the exit code, the failure count, and the FULL LIST of red test
     ids, never truncated. WHEN YOU PARSE THOSE IDS, take EVERYTHING AFTER THE
     FIRST SPACE of a "FAILED ..." line as the node id - NOT the second
     whitespace-separated token, which truncates a parametrized id at its first
     internal space. Print one RAW "FAILED ..." line beside your parsed set and
     confirm they agree. State whether the red sets are pairwise disjoint:
     report what you MEASURED, and non-disjoint is a REPORTABLE RESULT rather
     than a fault. Read git status --porcelain ON THE PRIMARY CHECKOUT
     immediately after every mutation. Revert with git checkout -- <exact path>
     INSIDE the worktree; each revert must return the worktree to the control's
     count.
  G7 THE SUITES, each its own invocation, run serially, all exit 0. The counts
     in brackets are what the reviewer measured at f943e436. Report yours beside
     them and explain any difference. ONLY the suite this round adds to may move.
       pytest tests/orchestration/test_role_config.py -q            (92 at base, +new)
       pytest tests/orchestration/test_model_routing.py -q          (406 passed,
         3 skipped - UNMOVED; model_routing.py is docstring-only this round)
       pytest tests/orchestration/test_config.py -q                 (81 - UNMOVED)
       pytest tests/orchestration/test_orchestrator_model_routing.py -q  (20 - UNMOVED)
       pytest tests/orchestration/test_teacher_model.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_job_role_routing.py tests/cli/test_teach_cmd.py -q   (68 - UNMOVED)
       pytest tests/cli/test_init_cmd.py tests/cli/test_worker_facade_cmd.py tests/orchestration/test_budget_stop_integration.py tests/orchestration/test_checkpoints.py tests/orchestration/test_dead_model_list.py tests/orchestration/test_f018_authority_integration.py -q   (304 - UNMOVED)
       pytest tests/runtimes/test_runtime_config.py tests/runtimes/test_runtime_lifecycle_safety.py tests/test_data_paths.py tests/ui_server/test_command_channel.py -q   (199 - UNMOVED)
       pytest tests/docs/ -q                                        (295 - the docs
         gate constraint 6 names; this round edits a file under docs/)
       pytest tests/cli/test_golden_path.py -q                      (42 - the canary)
  G8 THE TREE, THE COMMITS AND THE SWEEP. git status --porcelain empty
     immediately before C6 is staged. git ls-files .remedy-wt returns nothing.
     No worktree of this round's making survives. Confirm NO remedy.toml exists
     in the repository root. Report git diff --stat f943e436..<C5> over
     packages/ and apps/ with role_config.py and model_routing.py EXCLUDED - it
     MUST be EMPTY, which proves config.py was not touched - and over docs/,
     which MUST list the ONE documentation file and nothing else. Report the
     per-commit INSERTION count, the + column only, for every commit BEFORE the
     handback commit, cell by cell against the handback's own ## Commits table,
     and confirm each is under the AGENTS.md 500-insertion cap.

Handback - rewrite .agent/handoff.md per docs/agents/handback_template.md
  It carries: SESSION 3 of F110, round 13, rounds so far 13; the state block
  with the Fortschritt line; the item-status table with every SPEC item and
  every gate exactly once; the per-commit changed-files tables; one line per
  gate with its real result; the authored-text proofs; the deviations; the next
  step. NO length cap applies (AGENTS.md amend0827 rule 3). Report the two STOP
  readings and the open-finding set G4 derives. DECLARE any sentence outside the
  change set this round makes stale without repairing it. STATE PLAINLY whether
  T003 is now complete on this branch, and name what the integration gate round
  will have to run.

<<<BEGIN PLAN13>>>
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

Round 13, session 3 — THE EVIDENCE WIRING, the last unbuilt clause of T003.
The config-reading layer reads `model_routing.promotion_evidence`, parses it
through the round-12 parser, and hands the records BOTH to the table builder,
so a documented benchmark run licenses a cheaper tier, AND to the seam, so a
routed call's `promoted_by` names the run. Round 12's PASS verdict and one
prose slip are booked in the same round.

## Next Steps

- The acceptance round: a fixture run whose every call's evidence shows
  class, tier and reason, per the feature file's Acceptance section, plus
  the reviewer/worker pairing assertion that section also names.
- The integration gate round, before closure.
- The closure sequence, which also runs the one checklist consolidation
  pass DECISION F110 D1 carries into it, and which updates the Design and
  Task-slicing bullets of `docs/roadmap/features/T3_F110.md`.

## Risks

- Two consumers each read and parse the evidence table; `get_config` is
  cached so the cost is small, and keeping the existing signatures was
  judged worth more than saving it.
- A malformed evidence record fails CLOSED — the promotion it would have
  licensed is refused and the class keeps its seeded tier.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
<<<END PLAN13>>>

<<<BEGIN RECORD12>>>
Gate: F110 R12 — the round 12 entry. VERDICT PASS, over the range `ccb736b9..6177329c` plus the handback commit `f943e436`. THE TRANSPORT PROOF REACHED THE REVIEWER'S OWN BYTES: `cmp` between the reviewer's scratch original and the committed `.agent/authored/f110-r12.md` exits 0, and one digest `ec790b803cdbfceb424d8a74f956536e2d0b92fdd0d3b2f40aa290513a098acf` at 28891 bytes covers the original, the saved copy at `f16aa7b1` and the mirror at `d125db16`; the block is 351 lines against the reviewer's own projection of 351, under the §3 item 1 cap of 400. EVERY SLICE WAS RE-DERIVED BYTE FOR BYTE and every size matched the pre-emission projection exactly: `.agent/plan.md` equals PLAN12 plus the one trailing newline the target's convention adds, at 45 lines; `.agent/live_review.md` is 2204274 + 2 + 5670 = 2209946, still ending without a newline, base an exact prefix; `.agent/prose_slips.md` is 61137. `ruff check` over all four changed files answers "All checks passed!", run reviewer-side. THE OPEN SET IS 278 OVER 349 REGISTERED AND 71 UNIQUE RESOLVED, and the worker computed it the way this round's G4 ordered — as a set difference over UNIQUE IDS rather than over LINES, which matters because `R-0721` and `R-0725` each carry two `Done:` paragraphs and the ledger now holds 73 such lines. `R-0787` and `R-0788` are OUT of the open set and `R-0767` is IN it, both confirmed by the reviewer's own derivation. THE PARSER WAS RUN BY THE REVIEWER, NOT READ, against a TOML file written outside the repository root: the nested evidence table resolves whole with source PROJECT, ZERO load warnings and `validate_config` silent; the record round-trips every field with `assertion_results` a real `PromotionAssertionResults`; and SPEC (h)'s reading reproduces exactly — the parsed record makes `build_effective_task_class_tiers` ACCEPT `architecture` at `cheap`, a TOP-tier class promoted, and the routed evidence reads tier `cheap`, reason `per_project_override`, promoted_by `qwen3-8b-instruct + q4_k_m@0f1e2d3c4b5a6978 on F082`, while the same map with an empty evidence mapping raises `OverrideRefused` carrying one violation whose `rule_name` is `promotion_without_evidence`. PER-ENTRY SKIPPING IS REAL AND NOT PER-TABLE: fed one well-formed record beside a non-mapping entry, an entry whose `assertion_results` is a scalar and an entry with a wrong-typed field, the parser returns exactly the one well-formed record. C4 IS 162 INSERTIONS AGAINST ZERO DELETIONS, so constraint 7 is MEASURED — no shipped behaviour of rounds 4 through 11 was revised — and the eight deletions in `config.py` are all in the module docstring, the `validate_config` docstring and the dict branch the round replaces. THE WORKER'S FIRST DEVIATION IS A GOOD CALL AND THE REVIEWER ENDORSES THE REASONING: SPEC (f) asked for the assertion-result field names to be read from the class, and the obvious `from dataclasses import fields` would have modified an existing import line, which G5 would have counted as a deletion outside the module docstring and therefore a STOP; using `PromotionAssertionResults.__dataclass_fields__` reads the names from the same place and keeps C4 purely additive. ITS SECOND DEVIATION IS A CORRECTION OF THE REVIEWER AND IS ACCEPTED IN FULL: G6's instruction to take "the SECOND whitespace-separated token" as a pytest node id TRUNCATES a parametrized id at its first internal space, so the worker's first harness run produced a truncated red set and an unreliable disjointness reading, and it also compared "back to control" over a summary line including elapsed time — the very slip F110 R9 recorded. The worker discarded that run, fixed both faults, re-ran the whole gate and printed both readings side by side; every number it reports comes from the corrected run. That is the block's wording at fault, recorded in `.agent/prose_slips.md` this round. THE SUITES WERE RE-RUN BY THE REVIEWER at 81 and 406 with 3 skipped for the two suites this round grows, then 92, 20, 304, 433, 199, 295 and 42, every one exit 0 and every unmoved count matching the block — a deliberately wide list, because round 10 shipped a red tip from a suite outside a narrow one. `git diff --stat ccb736b9..6177329c` over `docs/` and over `packages/` and `apps/` with the two edited files excluded is EMPTY, so `role_config.py` is untouched and NOTHING IS WIRED, which is what constraint 6 ordered. The per-commit insertion counts are 351, 282, 16, 10, 48, 162 and 379, every one under the AGENTS.md cap; `f943e436` is 467 insertions against 417 deletions, a full-file rewrite of a single `.agent/**` state file and exempt under DECISION F104 D1. THREE STALE SENTENCES ARE DECLARED AND LEFT UNREPAIRED, correctly, since docs sit outside this round's change set: the configuration document's registered-key table omits the new key and its table-valued-keys section names one such key where there are now two, both of which round 13 repairs; and `model_routing.py`'s own "it arrives with the resolver-seam round" clause was already stale before this round touched the file, so constraints 7 and 9 left it alone. The tree is clean, `git ls-files .remedy-wt` returns nothing, no worktree of the round's making survives, `.agent/decisions.md` and `.agent/candidates.md` are untouched, and the branch is pushed at `f943e436` with no pull request open.
<<<END RECORD12>>>

<<<BEGIN SLIPS13>>>
2026-09-03 · F110 R12 · The round 12 block's G6 told the worker to parse a pytest failure id as "the SECOND whitespace-separated token" of a `FAILED ...` line. That is wrong for any PARAMETRIZED id whose parameter contains a space — `FAILED path::Class::test[a wrong-typed field-entry2]` truncates to `path::Class::test[a` — so the worker's first harness run produced a truncated red set and a disjointness reading it could not trust. It discarded that run, corrected the parse to take everything after the first space, re-ran the whole gate and printed both readings side by side, which is exactly the behaviour the round 9 slip asked for. The irony is on the record deliberately: the same block's G6 also carried the round 9 lesson about printing a raw line beside a parsed set, and it was that instruction which caught the reviewer's own bad rule. THE LESSON: a node id is EVERYTHING AFTER THE FIRST SPACE of a `FAILED ` line, never a whitespace-token index, because pytest parameter ids may contain spaces; and a block that orders a parse states the rule in terms of the delimiter, not the token number. Reviewer block-wording slip, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIPS13>>>
