# Handback — F110 R7 (T003, the promotion-evidence discipline)

## Session

SESSION 2 of feature F110 · round 7 · rounds so far 7

Soft limit (25 rounds / 7 sessions) not reached: 7 rounds, 2 sessions. No scope
report is owed.

`.agent/STOP` read from disk twice, as constraint 10 orders — once before the
first commit (C0a) and again before C5. ABSENT both times.

## State

| Feld | Wert |
|------|------|
| **Feature** | F110 Model routing by task class (Tier 3, depends on F103) |
| **Branch** | `feature/f110-model-routing-by-task-class` |
| **Round** | 7 (session 2), step T003 — the promotion-evidence discipline |
| **Base** | `c1a3a3c4` |
| **Head before C5** | `7db8c018` |
| **Commits this round** | `5cadf64b` `1523b1b9` `98acd71f` `f2cf1db6` `5e9537f1` `2cd58c66` `7db8c018` + C5 |
| **Tree** | clean at every verdict point |
| **Open PR** | NONE — no pull request created, none merged |
| **Open findings** | 278 open, over 347 registered and 69 resolved — UNCHANGED this round |
| **Docs touched** | NONE. `docs/agents/model_routing_policy.md` is READ by the new sync test, never written |

## Range

Review of `c1a3a3c4..7db8c018` (plus this C5 commit).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block verbatim | done | |
| C0b mirror to `.agent/last_block.md` | done | |
| C1 apply PLAN7 | done | first substantive commit, item 23 honoured |
| C2 append RECORD6 + SLIPS7 | done | |
| C3 the production commit | done | |
| C4 the test commit | deviated | SPLIT into C4a + C4b: one commit would have been 717 insertions, over AGENTS.md's 500 cap. See D3 |
| C5 the handback | done | this file |
| (a) promotion bars as named constants | done | `PROMOTION_MINIMUM_RUNS_PER_FIXTURE` / `_BLOCK_ASSERTION_PASS_RATE` / `_OVERALL_PASS_RATE`, each carrying its document sentence |
| (b) the document's own field list | done | `PROMOTION_EVIDENCE_DOCUMENT_FIELDS`, 7 names; the `" + "` split declared at `PROMOTION_EVIDENCE_COMPOUND_FIELD_SEPARATOR` |
| (c) the evidence record | done | `PromotionEvidence`, plus the nested `PromotionAssertionResults`. See D5 |
| (d) three promotion rule names + report order | done | `PROMOTION_RULE_NAMES`; `OVERRIDE_VIOLATION_RULE_NAMES` is now schema + hard + promotion |
| (e) the promotion predicate | done | `is_task_class_promotion` |
| (f) the promotion check | done | `check_promotion_backed_by_evidence` |
| (g) validator gains the optional evidence map | done | third parameter, defaults to `None` |
| (h) builder gains the same optional parameter | done | passes it through |
| (i) the evidence fields | done | `routed_call_evidence_fields` + `ROUTED_CALL_EVIDENCE_FIELDS` |
| docstring Public API extension | done | every new name listed; the "SEEDED from the Promotion rule section" sentence added |
| (j) the promotion-rule sync test | done | `TestPromotionRuleSyncTest`, bullet parser with continuation joining; the measured trap pinned |
| (k) refused without evidence / accepted with it | done | `TestPromotionRefusedByTheOverrideMap`, first two cases |
| (l) incomplete + below-threshold, each bar just below and just at | done | `TestPromotionCheck`, 6 boundary cases |
| (m) stronger tier / undeclared class / restated seed tier | done | `TestPromotionPredicate` + `TestPromotionRefusedByTheOverrideMap` |
| (n) the evidence fields with a GOLDEN | done | `TestRoutedCallEvidenceFields.GOLDEN_PROMOTED_CALL`, exact dict |
| (o) the widened guards | deviated | (o)'s 5 named functions widened, AND 5 further existing functions that C3 also turned red. MEASURED, see D1 |
| (p) HARD_RULE_NAMES / schema tuple unchanged | done | pinned in `TestOverrideRuleNamesAreNotHardRuleNames` and `TestRoundSixCallsAreUnchanged` |
| (q) round 6 calls unchanged + two-positional call | done | `TestRoundSixCallsAreUnchanged` |
| G1 transport | done | PASS |
| G2 the plan | done | PASS, with the target-newline reading declared (D2) |
| G3 the ledger append | done | PASS |
| G4 the prose file | done | PASS |
| G5 the module, measured and run | done | PASS, with two deletion regions outside the block's permitted list declared (D4) |
| G6 the red proof | done | PASS; mutation (iii) reddens exactly one id and it is the dedicated one (D6) |
| G7 the suites | done | PASS, all six |
| G8 the tree, the commits, the sweep | done | PASS |

## Commits

### 5cadf64b F110 R7 C0a: the round 7 block, saved verbatim
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f110-r7.md` | +351 / -0 | the block between the sentinels, written verbatim |

### 1523b1b9 F110 R7 C0b: the block mirrored to last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +246 / -292 | exact `shutil.copyfile` mirror of the committed authored file |

### 98acd71f F110 R7 C1: the plan names round 7 and the promotion-evidence discipline
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +20 / -20 | PLAN7, extracted by marker index from the COMMITTED authored file |

### f2cf1db6 F110 R7 C2: round 6 verdict booked and the reviewer prose slips recorded
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +3 / -1 | RECORD6 appended after two newlines |
| `.agent/prose_slips.md` | +5 / -1 | SLIPS7 appended after two newlines |

### 5e9537f1 F110 R7 C3: the promotion-evidence discipline, refused with the rule named
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/model_routing.py` | +370 / -17 | SPEC CODE (a) through (i), plus the docstring extension |

### 2cd58c66 F110 R7 C4a: the round 6 guards widened for the promotion report order
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_model_routing.py` | +231 / -19 | the header, the imports, the promotion fixtures, and every widened existing guard |

### 7db8c018 F110 R7 C4b: a promotion without evidence refused, with evidence logged
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_model_routing.py` | +486 / -0 | SPEC TESTS (j) through (q): the new T003 classes |

### C5 (this commit) F110 R7 C5: the round 7 handback
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | a handback cannot table the commit that writes it (R-0149 pattern) |

## External actions

| Command | Outcome |
|---------|---------|
| `git worktree add --detach /home/decodeux/Repos/remedy/remedy-review-f110-r7-wt 7db8c018` | created, detached at `7db8c018` |
| `git -C <wt> checkout 7db8c018 -- packages/orchestration/model_routing.py` (×4) | each mutation reverted by RESTORING the file from the C4b commit, never by re-editing |
| `git worktree remove /home/decodeux/Repos/remedy/remedy-review-f110-r7-wt --force` | removed by exact path |
| `git worktree prune` | ran; `git worktree list` then holds only the five pre-existing `.remedy-wt/job-*` worktrees, none of this round's making |
| `git push` | after C5 — see the push line at the end of Verification |
| PR create / merge | NONE. No pull request exists on this branch |

Scratch files written and then removed BY EXACT PATH: `plan7_raw.tmp`,
`plan7_nl.tmp` (G2 `cmp` operands), `c4_full.tmp`, `c4b_tail.tmp` (the C4 split).
None was ever committed and `git status --porcelain` is empty.

## Verification

One line per gate, then the transcripts.

| Gate | Result |
|------|--------|
| G1 transport | PASS — one digest twice; 351 lines against a projection of 351, cap 400 |
| G2 the plan | PASS — `cmp` exit 0 against the target-convention extract; 44 lines; one `## Goal`; one `## Next Steps` |
| G3 the ledger append | PASS — arithmetic exact, second reader True, negative control REJECTED, grep 0 → 1 |
| G4 the prose file | PASS — final bytes equal SLIPS7, base survives as an exact prefix, still ends without a newline |
| G5 the module | PASS — 370/17, `ast.parse` clean, every deleted line read and attributed, every function RUN |
| G6 the red proof | PASS — control 325/3 exit 0; the four mutations redden 39, 14, 1 and 25 ids; every revert returns 325 passed |
| G7 the suites | PASS — 325+3, 33, 34, 63, 295, 42; the routing file GREW from 185 and the skips did NOT rise |
| G8 the tree, the commits, the sweep | PASS — tree clean, no `.remedy-wt` tracked, no docs diff, every insertion cell matches |

### G1 TRANSPORT

    $ sha256sum .agent/authored/f110-r7.md .agent/last_block.md
    77d742debe526e97f8a1849fafbe462714e2354fded17c0a38f65b279f7c7581  .agent/authored/f110-r7.md
    77d742debe526e97f8a1849fafbe462714e2354fded17c0a38f65b279f7c7581  .agent/last_block.md
    exit 0

    $ wc -l .agent/authored/f110-r7.md
    351 .agent/authored/f110-r7.md
    exit 0

The reviewer's projection is 351. REPORTED FIGURE 351. No difference; nothing
repaired. The cap is 400 and the file is under it.

### G2 THE PLAN

PLAN7 extracted by marker index from the COMMITTED `.agent/authored/f110-r7.md`
(`git show HEAD:.agent/authored/f110-r7.md`), marker lines excluded. Raw slice
2030 bytes, and it does NOT end with a newline.

    $ cmp <raw extract> .agent/plan.md
    cmp: EOF on plan7_raw.tmp after byte 2030, in line 44
    exit 1

    $ cmp <extract + the one trailing newline constraint 4 orders the TARGET to keep> .agent/plan.md
    (no output)
    exit 0

BOTH readings are reported rather than the green one being chosen. `.agent/plan.md`
ends WITH a newline (constraint 4), the raw slice does not, so the raw `cmp` is
one byte short by construction and the target-convention `cmp` is exit 0. This is
the same target-convention/raw-slice tension the reviewer's own SLIPS7 entry
records for round 6's G4.

    $ wc -l .agent/plan.md
    44 .agent/plan.md            exit 0   (under 50)
    $ grep -c '^## Goal' .agent/plan.md
    1                            exit 0
    $ grep -c '^## Next Steps' .agent/plan.md
    1                            exit 0

### G3 THE LEDGER APPEND

Arithmetic, `.agent/live_review.md`, against the size immediately before C2:

    before        = 2168965
    slice RECORD6 =    8260
    before + 2 + slice = 2177227
    real new size      = 2177227
    EQUAL              = True

Still ends WITHOUT a newline: True.

Second reader, counting no byte — the WHOLE file split on blank-line boundaries,
N counted BY THE SCRIPT from the slice:

    N counted by the script from the slice = 1
    last N units equal the slice paragraphs IN ORDER -> True
      unit 0 identical: True

Negative control, one byte flipped inside the FIRST appended paragraph of a
SCRATCH COPY (offset 50, the file on disk untouched):

    second reader on the flipped copy -> False   (REJECTED, which is the pass)

    $ grep -c '^Gate: F110 R6 — ' .agent/live_review.md    (BEFORE C2)
    0                            exit 1  (grep exits 1 on a zero count)
    $ grep -c '^Gate: F110 R6 — ' .agent/live_review.md    (AFTER C2)
    1                            exit 0

### G4 THE PROSE FILE

Byte-equality only, per the gate budget:

    final bytes equal the extracted SLIPS7 slice        -> True
    pre-C2 content survives as an exact byte PREFIX     -> True
    file still ends WITHOUT a newline                   -> True
    base=53495  slice=1356  now=54853  base+2+slice=54853

### G5 THE MODULE, MEASURED AND RUN

    $ git show --numstat 5e9537f1 -- packages/orchestration/model_routing.py
    370     17      packages/orchestration/model_routing.py
    exit 0

    $ python3 -c "import ast; ast.parse(open(...).read())"
    ast.parse OK, bytes= 51640
    exit 0

EVERY DELETED LINE, VERBATIM, WITH ITS REGION — 17 lines, four regions:

REGION 1, the module docstring's opening paragraph (PERMITTED by the gate) — 3 lines:

    returning ITS OWN rule name when a routing choice violates it, and the PER-PROJECT
    is applied. Nothing else yet: no config file is read, no model id is named and no
    call site routes through it.

REGION 2, the module docstring's Public API list (PERMITTED) — 5 lines:

        OVERRIDE_VIOLATION_RULE_NAMES: schema names then HARD_RULE_NAMES — the
            order an override map's violations are reported in
        validate_task_class_tier_overrides(overrides, classes)
        build_effective_task_class_tiers(overrides, classes) -> dict[str, str],
            raising OverrideRefused rather than dropping a violating entry

REGION 3, the report-order constant and its own comment (PERMITTED) — 4 lines:

    #: SCHEMA names first, then the hard-rule names. Schema first because a malformed
    #: entry is what an operator must fix before any policy reading of it means
    #: anything.
    OVERRIDE_VIOLATION_RULE_NAMES: tuple[str, ...] = OVERRIDE_SCHEMA_RULE_NAMES + HARD_RULE_NAMES

REGION 4, OUTSIDE the two regions the gate permits — 5 lines. DECLARED, NOT
REPAIRED, and see deviation D4:

  4a — the `validate_task_class_tier_overrides` FUNCTION docstring, 4 lines:

        exists — the three hard-rule checks are called, never re-labelled — which is
        the discipline :func:`validate_routing_choice` already states. The two schema
        names have no check function of their own and are the only names this function
        supplies directly.

  4b — ONE EXECUTABLE LINE, inside `build_effective_task_class_tiers`:

        violations = validate_task_class_tier_overrides(normalized, safety_relevant_classes)

NO OTHER executable line was deleted. 4b is the builder's call to the validator,
replaced by the same call carrying the new third argument — which is literally
what SPEC (h) orders ("passes it through"). 4a is the sentence "the three hard-rule
checks are called" which C3 itself falsifies, so constraint 9 orders it repaired in
this commit. Reported here as the gate requires rather than reverted.

RUNNING THE SHIPPED CODE — what the functions RETURNED:

    MODULE FILE: /home/decodeux/Repos/remedy/packages/orchestration/model_routing.py
    BARS: runs=3 block=90 overall=75
    SEPARATOR: ' + '
    DOC FIELDS: ('model_id', 'quantization', 'prompt_hash', 'tokens', 'cost',
                 'assertion_results', 'reviewer_verdict')
    PROMOTION_RULE_NAMES: ('promotion_without_evidence',
                           'promotion_evidence_incomplete',
                           'promotion_evidence_below_threshold')
    OVERRIDE_VIOLATION_RULE_NAMES: ('override_unknown_task_class',
        'override_unknown_tier', 'reviewer_weaker_than_worker',
        'orchestration_below_top_tier', 'safety_class_below_mid_tier',
        'promotion_without_evidence', 'promotion_evidence_incomplete',
        'promotion_evidence_below_threshold')
    HARD_RULE_NAMES: ('reviewer_weaker_than_worker', 'orchestration_below_top_tier',
                      'safety_class_below_mid_tier')          UNCHANGED
    OVERRIDE_SCHEMA_RULE_NAMES: ('override_unknown_task_class',
                                 'override_unknown_tier')     UNCHANGED

    PREDICATE cheaper   (mission -> cheap): True
    PREDICATE equal     (mission -> top):   False
    PREDICATE stronger  (format  -> top):   False
    PREDICATE undeclared(unknown -> cheap): False

    CHECK no evidence            : promotion_without_evidence
    CHECK incomplete (no hash)   : promotion_evidence_incomplete
    CHECK incomplete (no results): promotion_evidence_incomplete
    CHECK runs just below (2)    : promotion_evidence_below_threshold
    CHECK runs just at   (3)     : None
    CHECK block just below (89)  : promotion_evidence_below_threshold
    CHECK block just at    (90)  : None
    CHECK overall just below (74): promotion_evidence_below_threshold
    CHECK overall just at    (75): None
    CHECK non-promotion          : None

    VALIDATOR promotion, NO evidence  : [('vision', 'promotion_without_evidence')]
    VALIDATOR promotion, WITH evidence: ()
    BUILDER no evidence RAISED: [('vision', 'promotion_without_evidence')]
      message: per-project model-routing overrides refused — vision: promotion_without_evidence
    BUILDER with evidence: 'cheap'

    EVIDENCE FIELDS promoted  : {'task_class': 'vision', 'tier': 'cheap',
        'reason': 'per_project_override',
        'promoted_by': 'qwen3-8b-instruct + q4_k_m@0f1e2d3c4b5a6978 on F082'}
    EVIDENCE FIELDS unpromoted: {'task_class': 'format', 'tier': 'cheap',
        'reason': 'seed_mapping', 'promoted_by': None}

    ROUND 6 TWO POSITIONAL ARGS: [('format', 'override_unknown_tier')]
    ROUND 6 ONE POSITIONAL ARG : ()

### G6 THE RED PROOF

Worktree: `/home/decodeux/Repos/remedy/remedy-review-f110-r7-wt`, detached at the
C4b commit `7db8c018`. `__pycache__` purge ran (0 directories found — a fresh
worktree carries none); every pytest invocation used `python3 -B`.

    $ python3 -B -c "import sys; sys.path.insert(0, '<abs-worktree>'); ..."
    IMPORTED FROM (no cd): /home/decodeux/Repos/remedy/remedy-review-f110-r7-wt/packages/orchestration/model_routing.py

UNMUTATED CONTROL, FIRST:

    $ python3 -B -m pytest <abs-worktree>/tests/orchestration/test_model_routing.py -q -p no:cacheprovider
    325 passed, 3 skipped in 0.48s
    exit 0

MUTATION (i) — the promotion predicate always answers "not a promotion"
(`return model_tier_rank(tier) < model_tier_rank(seeded)` → `return False`):

    PRIMARY git status --porcelain -> ''   (read immediately after the mutation, same step)
    39 failed, 286 passed, 3 skipped

    Its own dedicated fixtures, all RED: TestPromotionPredicate::
      test_a_cheaper_tier_than_the_seed_is_a_promotion[architecture|mission|
        prompt_authoring_for_other_agents|standard_build|standard_review|vision],
      test_the_class_may_be_spelled_as_the_document_words_it
    Plus every downstream promotion case, because the predicate gates them all.

MUTATION (ii) — the check never returns the WITHOUT-EVIDENCE name
(`if evidence is None: return RULE_PROMOTION_WITHOUT_EVIDENCE` → `return None`):

    PRIMARY git status --porcelain -> ''
    14 failed, 311 passed, 3 skipped

    Its own dedicated fixtures, RED:
      TestPromotionCheck::test_a_promotion_with_no_evidence_is_refused_with_its_own_rule
      TestPromotionRefusedByTheOverrideMap::test_a_promotion_without_evidence_is_refused_with_the_rule_named
      TestPromotionRefusedByTheOverrideMap::test_evidence_for_another_class_does_not_discharge_this_promotion
      TestPromotionRefusedByTheOverrideMap::test_the_builder_refuses_a_promotion_without_evidence
      TestEffectiveTableBuilder::test_the_message_names_every_violated_rule[promotion_without_evidence]
    NOT red: mutation (i)'s dedicated TestPromotionPredicate cases, mutation (iii)'s
    dedicated sync-test case, and every TestRoutedCallEvidenceFields case
    (mutation (iv)'s dedicated set).

MUTATION (iii) — `PROMOTION_MINIMUM_OVERALL_PASS_RATE` lowered to a tenth, 75 → 7:

    PRIMARY git status --porcelain -> ''
    1 failed, 324 passed, 3 skipped
      TestPromotionRuleSyncTest::test_the_parsed_overall_rate_equals_the_module_constant

    THE GATE'S OWN REQUIREMENT IS MET EXACTLY: mutation (iii) reddens the sync test
    of (j), which is the proof that the bar really is pinned to the document. It
    reddens NOTHING ELSE, and that is by design rather than by weakness — see D6.
    A mutation that reddens nothing would be a FAILED proof; this one reddens its
    dedicated case and no other mutation's.

MUTATION (iv) — `routed_call_evidence_fields` omits the `promoted_by` key:

    PRIMARY git status --porcelain -> ''
    25 failed, 300 passed, 3 skipped

    Its own dedicated set, RED: the whole of TestRoutedCallEvidenceFields —
      test_the_golden_promoted_call_is_exactly_this_mapping (the GOLDEN),
      test_the_keys_are_exactly_the_declared_fields[10 params],
      test_an_unpromoted_class_reports_no_promoting_evidence[10 params],
      test_a_promoted_class_names_the_run_that_promoted_it,
      test_a_class_the_table_does_not_name_reports_the_conservative_pair,
      test_the_class_may_be_spelled_as_the_document_words_it,
      test_an_override_restating_the_seed_tier_reports_the_seed_reason_and_no_promotion
    NOT red: any TestPromotionPredicate, TestPromotionCheck,
    TestPromotionRefusedByTheOverrideMap or TestPromotionRuleSyncTest case.

THE DISCRIMINATOR, as the property rather than as a colour: each mutation reddens
the cases written for ITS OWN behaviour, and NO mutation reddens another
mutation's DEDICATED fixtures. The cases that assert over a map breaking every
rule at once (`TestOverrideValidatorCollectsEveryViolation`,
`TestEffectiveTableBuilder::test_the_raised_object_carries_the_violations`,
`TestOverrideRefusedPerHardRule`'s widened parameters) belong to no single
mutation and redden under (i) and (ii) both — construction, not a failure, exactly
as the block's own wording allows and as the reviewer's SLIPS7 entry records.

REVERTS: each by `git -C <wt> checkout 7db8c018 -- packages/orchestration/model_routing.py`,
NEVER by re-editing. After the last revert:

    $ git -C <wt> status --porcelain      -> (empty)
    $ git status --porcelain (PRIMARY)    -> (empty)
    $ python3 -B -m pytest <abs-worktree>/tests/orchestration/test_model_routing.py -q -p no:cacheprovider
    325 passed, 3 skipped        exit 0

    $ git worktree remove /home/decodeux/Repos/remedy/remedy-review-f110-r7-wt --force
    $ git worktree prune
    $ git worktree list
    /home/decodeux/Repos/remedy                                  7db8c018 [feature/f110-model-routing-by-task-class]
    /home/decodeux/Repos/remedy/.remedy-wt/job-48a379ab5ca44ec5  f0e6b9a3 [remedy/job-48a379ab5ca44ec5]
    /home/decodeux/Repos/remedy/.remedy-wt/job-5e91e080219342d9  9fdb3b4b [remedy/job-5e91e080219342d9]
    /home/decodeux/Repos/remedy/.remedy-wt/job-7d1c93e2dc98415a  f0e6b9a3 [remedy/job-7d1c93e2dc98415a]
    /home/decodeux/Repos/remedy/.remedy-wt/job-98e9364a83a34872  21a45836 [remedy/job-98e9364a83a34872]
    /home/decodeux/Repos/remedy/.remedy-wt/job-f76686b8435640e9  4b49af98 [remedy/job-f76686b8435640e9]

The five `job-*` worktrees are NOT of this round's making and were left alone. No
worktree this round created survives.

### G7 THE SUITES, EACH ITS OWN INVOCATION, SERIALLY

    $ python3 -m pytest tests/orchestration/test_model_routing.py -q
    325 passed, 3 skipped in 0.50s                                  exit 0
      passed 185 -> 325 (GREW, as the gate requires)
      skipped 3 -> 3    (did NOT rise; no green was bought by skipping)

    $ python3 -m pytest tests/orchestration/test_orchestrator_model_routing.py tests/orchestration/test_job_role_routing.py -q
    33 passed in 0.27s                                              exit 0   (33 expected)

    $ python3 -m pytest tests/orchestration/test_role_config.py -q
    34 passed in 0.23s                                              exit 0   (34 expected)

    $ python3 -m pytest tests/orchestration/test_config.py -q
    63 passed in 0.34s                                              exit 0   (63 expected)

    $ python3 -m pytest tests/docs/ -q
    295 passed in 0.44s                                             exit 0   (295 expected)

    $ python3 -m pytest tests/cli/test_golden_path.py -q
    42 passed in 20.63s                                             exit 0   (42 expected)

The last five are UNMOVED. The three skips are round 5's `mission` skips in
`test_a_class_the_rule_does_not_cover_is_never_refused_by_it`, unchanged.

### G8 THE TREE, THE COMMITS AND THE SWEEP

    $ git status --porcelain          (immediately before C5 was staged)
    (no output)                                                     exit 0
    $ git ls-files .remedy-wt
    (no output)                                                     exit 0
    $ git diff --stat c1a3a3c4..7db8c018 -- docs/
    (no output)                                                     exit 0   NO DOCS EDITED

PER-COMMIT INSERTION COUNTS, the `+` column only, from `git show --numstat`,
compared CELL BY CELL against the Commits table above:

| Commit | numstat `+` | Commits table | Match |
|--------|-------------|---------------|-------|
| `5cadf64b` C0a | 351 | 351 | yes |
| `1523b1b9` C0b | 246 | 246 | yes |
| `98acd71f` C1  | 20  | 20  | yes |
| `f2cf1db6` C2  | 8 (3 + 5) | 3 + 5 | yes |
| `5e9537f1` C3  | 370 | 370 | yes |
| `2cd58c66` C4a | 231 | 231 | yes |
| `7db8c018` C4b | 486 | 486 | yes |

Every commit is under the 500-insertion cap (AGENTS.md, DECISION F104 D1 counting
rule). No oversize-commit exception is claimed by this round. C5's own numbers go
to neither a round report nor this file, per item 14.

THE STALENESS SWEEP — one entry per file this round touched:

| File | Stale? | Why |
|------|--------|-----|
| `.agent/authored/f110-r7.md` | NOT stale | It is the block verbatim and describes nothing else on disk. Its SPEC TESTS (o) prediction proved incomplete (D1), but the file is a frozen record of what was ORDERED, and constraint 1 forbids repairing it |
| `.agent/last_block.md` | NOT stale | byte-identical mirror of the above |
| `.agent/plan.md` | NOT stale | names round 7 / T003 and describes exactly what C3 and C4a/C4b shipped; its Next Steps name the resolver seam, which is the next round |
| `.agent/live_review.md` | NOT stale | RECORD6 describes round 6 at `c1a3a3c4`; every figure in it was measured there and nothing this round moved any of them |
| `.agent/prose_slips.md` | NOT stale | two dated reviewer-slip lines about round 6; append-only, never rewritten |
| `packages/orchestration/model_routing.py` | NOT stale | the opening paragraph now names the promotion discipline, the Public API list covers every new name, and the "Nothing in production imports this module yet" / "no config file is read" sentences are STILL TRUE — nothing was wired to a call site |
| `tests/orchestration/test_model_routing.py` | NOT stale | the header now reads T002a/T002b/T002c/T003 and names the second sync test; every widened guard carries a comment saying it was widened and why |
| `.agent/handoff.md` | NOT stale | written now |

OUTSIDE THE CHANGE SET, sentences this round makes stale — DECLARED, NOT REPAIRED
(constraint 9):

- NONE FOUND. `docs/roadmap/features/T3_F110.md` line 37 says "the resolver logs
  promoted_by evidence per run"; the shipped key is named exactly `promoted_by`,
  so that sentence became MORE true, not less. Its lines 34-39 describe the
  promotion discipline this round shipped and remain accurate; line 36's "recorded
  in the config change" still awaits the resolver-seam round, which the plan names.
- `docs/agents/model_routing_policy.md` is READ and never written; this round adds
  no claim about it beyond what the new sync test proves against it.
- Round 6's DEVIATION D7 (the feature file wording "orchestrator and
  mission-compile calls" against the wider shipped set) is UNCHANGED by this round
  and was already ruled on in RECORD6 as not a finding; F110's closure sequence
  updates that bullet and `.agent/plan.md` now carries that obligation.

## Authored-text proofs

| Slice | Applied to | Proof |
|-------|-----------|-------|
| PLAN7 | `.agent/plan.md` | extracted by marker index from the COMMITTED `.agent/authored/f110-r7.md`; `cmp` against the extract + the target's own trailing newline = exit 0. Raw-extract `cmp` = exit 1 at byte 2030 (the one newline constraint 4 orders the TARGET to keep). Both readings reported |
| RECORD6 | `.agent/live_review.md` | byte arithmetic exact (2168965 + 2 + 8260 = 2177227), independent structural second reader True with N counted from the slice, negative control REJECTED |
| SLIPS7 | `.agent/prose_slips.md` | final bytes byte-equal to the extract; pre-C2 content an exact byte PREFIX; still ends without a newline |

No slice was retyped. Every extraction ran against
`git show HEAD:.agent/authored/f110-r7.md`, never against the prompt.

## Deviations & assumptions

**D1 — SPEC (o)'s MEASURED RED LIST IS INCOMPLETE, AND FIVE FURTHER EXISTING TEST
FUNCTIONS WERE WIDENED. This is the round's most important deviation.**
(o) states that "extending the override report order with two promotion names and
changing nothing else turns exactly these red", names five functions, and projects
6 failed / 181 passed / 3 skipped. That measurement is of the REPORT-ORDER CONSTANT
ALONE. The round also orders (e) through (h), which put the promotion check into
the validator, and that changes BEHAVIOUR, not only a tuple. MEASURED by this
worker against the committed C3 (`5e9537f1`) with the test file still at round 6:

    12 failed, 176 passed, 3 skipped

— ten distinct functions, not five. The five (o) names are all present. The five it
does not name are:

    TestOverrideRefusedPerHardRule::test_an_orchestration_class_demoted_below_top_is_refused_with_the_rule_named[cheap-mission]
    TestOverrideRefusedPerHardRule::test_an_orchestration_class_demoted_below_top_is_refused_with_the_rule_named[mid-mission]
    TestOverrideRefusedPerHardRule::test_mission_demoted_below_top_is_refused_with_the_rule_named
    TestOverrideRefusedPerHardRule::test_a_safety_relevant_class_demoted_below_mid_is_refused_with_the_rule_named[cheap]
    TestOverrideRefusedPerHardRule::test_the_same_safety_class_at_or_above_mid_is_not_refused[mid]
    TestOverrideValidatorCollectsEveryViolation::test_an_override_key_may_be_spelled_as_the_document_words_it

WHY IT IS UNAVOIDABLE, and it is arithmetic rather than judgement: every
orchestration class the seed table names (`mission`) and the fixture safety class
(`architecture`) are SEEDED AT THE TOP TIER, so any demotion that breaks their hard
rule is NECESSARILY also a move to a cheaper tier — a promotion. There is no
override map that breaks the orchestration rule and is not a promotion. So with the
discipline shipped, those maps report two names, and round 6's exact-list
assertions became false statements about the shipped behaviour.

WHAT WAS DONE, and constraint 8 versus constraint 9: constraint 8 says only (o)'s
tests are edited; constraint 9 says a sentence INSIDE a file this round edits that
this round's own commit falsifies IS repaired in that commit. The test file is such
a file and those assertions are such sentences, so they were repaired — WIDENED,
never weakened:

- the four "refused with the rule named" cases keep an EXACT list and simply name
  the second rule too, so strictly more is pinned than before;
- `test_the_same_safety_class_at_or_above_mid_is_not_refused` keeps its EXACTLY
  EMPTY assertion and now makes it against a supplied benchmark run, so it says the
  stronger thing;
- nothing was deleted, nothing was skipped, and no parametrization was narrowed.

Two NEW discriminating cases were added beside them
(`test_evidence_clears_the_promotion_name_and_never_the_orchestration_rule`,
`test_evidence_never_discharges_a_hard_rule`) so the widening is a proof rather
than an accommodation.

THE ALTERNATIVE WAS REJECTED DELIBERATELY. Suppressing the promotion violation for
an entry that already breaks a hard rule would have left every (o)-unnamed test
green and matched the block's projection exactly. It was not done: the module's own
declared discipline is "an operator fixing a config one violation per round trip
fixes it four times; this returns EVERY violation in the whole map at once", and
silently narrowing the report to hit a projected number is the shape of defect this
feature exists to prevent. The reviewer may of course rule the other way; the point
is that the choice is stated rather than hidden.

**D2 — G2's `cmp` is exit 0 only against the target-convention extract.** The raw
PLAN7 extract is 2030 bytes with no trailing newline; `.agent/plan.md` ends WITH one
because constraint 4 orders the target's convention to win. `cmp` against the raw
extract is exit 1 at byte 2030; `cmp` against extract + `"\n"` is exit 0. Both are
reported above rather than the green one being chosen — the behaviour the reviewer's
own SLIPS7 entry says is the one to keep.

**D3 — C4 WAS SPLIT INTO C4a AND C4b, a departure from the block's ordered commit
sequence.** The single C4 the block orders measures 717 insertions, over AGENTS.md's
500-line cap, which counts INSERTIONS only (DECISION F104 D1). The AGENTS.md
exception route (declare-and-proceed) was available and was NOT taken, because that
allowance is "at most once per feature — by construction" and this content splits
cleanly along its own seam: C4a (231) carries the header, the imports, the promotion
fixtures and every WIDENED existing guard, and is GREEN on its own (200 passed, 3
skipped); C4b (486) carries the NEW T003 test classes. C4a/C4b is also the split
this branch already used at round 5. AGENTS.md is the highest authority and states
"If a diff exceeds 500 lines, stop and split before committing".

**D4 — TWO C3 DELETION REGIONS FALL OUTSIDE THE GATE'S PERMITTED LIST.** G5 permits
deletions in the module docstring and the report-order constant. Five deleted lines
are outside both: four in the `validate_task_class_tier_overrides` FUNCTION
docstring, one executable line (the builder's call to the validator). Reported
verbatim in G5 above rather than repaired, as the gate orders. Both are ordered by
the block's own SPEC: (h) says the builder "passes it through", which cannot be done
without rewriting that call, and constraint 9 orders the repair of the docstring
sentence "the three hard-rule checks are called, never re-labelled", which C3 itself
falsifies. NO OTHER executable line was deleted anywhere in C3.

**D5 — THE TWO PASS RATES ARE NESTED INSIDE `assertion_results`, NOT ADDED BESIDE
IT.** SPEC (c) orders the record to carry every name in (b) plus `runs_per_fixture`
and `corpus`, and SPEC (f) orders the check to read "either pass rate". Those are
only compatible if the rates live inside one of (b)'s names. `assertion_results` is
the document's own name for them, so it is a nested frozen dataclass
`PromotionAssertionResults(block_level_pass_rate, overall_pass_rate)` rather than a
string. This keeps `PROMOTION_EVIDENCE_DOCUMENT_FIELDS` exactly what the document
says, which is what lets the sync test be a straight comparison instead of a
translation. Stated because it is a design choice the block did not spell out.

**D6 — MUTATION (iii) REDDENS EXACTLY ONE ID, AND IT IS THE ONE THE GATE NAMES.**
Lowering `PROMOTION_MINIMUM_OVERALL_PASS_RATE` from 75 to 7 turns
`TestPromotionRuleSyncTest::test_the_parsed_overall_rate_equals_the_module_constant`
red and nothing else. The boundary cases of (l) do NOT redden, because
`_promotion_evidence()` derives its fixture rates FROM the module constants — which
is deliberate and documented at that helper ("so the boundary cases below stay at
the boundary when a bar moves"): a boundary test that hard-coded 75 would stop
testing the boundary the day the bar moved. The gate's requirement is that mutation
(iii) "must ALSO redden the sync test of (j), which is the proof that the bars
really are pinned to the document", and it does exactly that. It is not a mutation
that reddens nothing, so it is not a failed proof — but the reviewer should know
that its red set is one id and why.

**D7 — `ruff` IS REFUSED BY THIS WORKER'S PERMISSION LAYER.** The block orders no
ruff gate and forbids adding one, so none was run and no lint reading is claimed.
Declared for the record because round 6's D1 was the same refusal: the reviewer lints
reviewer-side. NO NUMBER WAS INVENTED.

**D8 — `cd` WAS USED ONCE INSIDE THE WORKTREE, against constraint 11.** The very
first `__file__` probe ran as `cd <abs-worktree> && python3 -B -c ...`. It was
immediately re-run WITHOUT `cd`, by absolute `sys.path` insertion, and that
no-`cd` transcript is the one recorded in G6; both printed the same worktree path.
Every subsequent command — every pytest invocation, every mutation, every revert,
every status read — addressed the worktree by absolute path or by `git -C`, exactly
as constraint 11 orders. Declared rather than quietly dropped.

**D9 — THE WORKTREE LIVES OUTSIDE `.remedy-wt/`, as in round 6.** This worker's
permission layer denies it every path under `.remedy-wt/`, so the disposable
worktree was `/home/decodeux/Repos/remedy/remedy-review-f110-r7-wt` and was removed
by exact path. The block explicitly sanctions this. `git ls-files .remedy-wt`
returns nothing and `git status --porcelain` is empty.

**D10 — `-p no:cacheprovider` was added to the worktree pytest invocations.** Not
ordered by the block. It keeps a `.pytest_cache` from being written into the
disposable worktree, which is a cleanliness measure and cannot affect a colour. The
six G7 suites ran EXACTLY the commands the gate states, with no added flag.

**Assumption (stated, not assumed silently):** the evidence map's keys are
normalized through `normalize_task_class` exactly as the override map's are. The
block does not say so; the module's declared discipline ("a project may spell a
class in the policy document's own wording") makes any other choice a trap, and a
test pins it (`test_an_evidence_key_may_be_spelled_as_the_document_words_it`).

## Next

THE RESOLVER SEAM AND THE PER-CALL-SITE TASK-CLASS DECLARATIONS (consolidation
order E.d) — the single place model selection happens, where the override map AND
the evidence map are finally READ from configuration instead of being passed in.
`packages/orchestration/config.py` is untouched and unimported to this day; that
round is where it changes. `R-0767` is OPEN on the same seam and must not be
absorbed into it.

The session CONTINUES after this round. THE BRANCH STILL HAS NO OPEN PULL REQUEST:
none was created, none was merged, nothing was force-pushed and no history was
rewritten.

Phase 1 rule 1 (`.agent/STOP`) is read BEFORE Phase 1 rule 2 (the Open PR Gate) at
the next session start.
