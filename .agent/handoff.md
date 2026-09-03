# Handback — F110 R6 (T002c, the per-project override schema)

## Session

SESSION 2 of feature F110 · round 6 · rounds so far 6

Soft limit (25 rounds / 7 sessions) not reached: 6 rounds, 2 sessions. No scope
report is owed.

`.agent/STOP` read from disk twice, as constraint 10 orders — once before the
first commit (C0a) and again before C5. ABSENT both times.

## State

| Feld | Wert |
|------|------|
| **Feature** | F110 Model routing by task class (Tier 3, depends on F103) |
| **Branch** | `feature/f110-model-routing-by-task-class` |
| **Round** | 6 (session 2), step T002c — the per-project override schema |
| **Base** | `78071a87` |
| **Head before C5** | `a62d4920` |
| **Commits this round** | `007c6aee` `6f54d420` `c610156c` `fc668181` `ecd12bf2` `a62d4920` + C5 |
| **Tree** | clean at every verdict point |
| **Open PR** | NONE — no pull request created, none merged |
| **Open findings** | 278 (347 registered, 69 resolved) — unchanged |
| **`.agent/candidates.md`** | not touched this round |
| **Next expected action** | reviewer gates this round; then T003, the promotion-evidence discipline |

## Range

Review of `78071a87..a62d4920` (C5 adds the handback commit on top).

## Commits

### 007c6aee F110 R6 C0a: save the round 6 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f110-r6.md | +397 / -0 | the block between the sentinels, written verbatim |

### 6f54d420 F110 R6 C0b: mirror the round 6 block to last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +305 / -160 | byte-identical mirror of the committed authored file |

### c610156c F110 R6 C1: the plan names the override schema round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +19 / -20 | PLAN6, extracted by marker index from the committed authored file |

### fc668181 F110 R6 C2: book round 5 PASS and DECISION F110 D2
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +45 / -0 | DECISION2 appended: `mission` joins the orchestration class set |
| .agent/live_review.md | +3 / -1 | RECORD5 appended: round 5's PASS verdict booked |

### ecd12bf2 F110 R6 C3: the per-project override schema, refused with the rule named
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/model_routing.py | +309 / -7 | SPEC CODE (a) through (i); the 7 deletions are the module docstring's opening paragraph (4) and the ORCHESTRATION_TASK_CLASSES comment (3) |

### a62d4920 F110 R6 C4: violating override fixtures per rule, each refused with the rule named
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_model_routing.py | +364 / -4 | SPEC TESTS (j) through (q); the 4 deletions are the module docstring's first line, the class docstring constraint 8 names, and the 2 lines of the one edited test |

### C5 (this commit) — F110 R6 C5: the round 6 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | — | a handoff cannot table the commit that writes it (R-0149 pattern); per G8 its numbers go to neither a round report nor this file |

## Item status

Every ordered item of the block, exactly once.

### Bundle
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this file |

### SPEC CODE
| Item | Status | Reason |
|---|---|---|
| (a) `mission` joins ORCHESTRATION_TASK_CLASSES | done | comment rewritten; says plainly why the set is wider than the feature file's two call kinds |
| (b) OVERRIDE_REASON | done | `"per_project_override"`, beside its two siblings |
| (c) REVIEWER_WORKER_CLASS_PAIRS | done | seeded `(("standard_build", "standard_review"),)` |
| (d) the two schema rule names + their tuple + the declared order | done | HARD_RULE_NAMES NOT extended; the undeclared-class WHY sits at the constant |
| (e) OverrideViolation | done | frozen dataclass, `(task_class, rule_name)` |
| (f) validate_task_class_tier_overrides | done | collecting, effective-table based, schema-faulty entries not judged |
| (g) OverrideRefused | done | carries `.violations`; message names every violated rule |
| (h) build_effective_task_class_tiers | done | raises; the "silently dropped override" sentence is in the docstring |
| (i) resolve_task_class_tier_with_overrides | done | reason derived by comparison; round 5's resolver untouched |
| Public API list extended | done | every name (b)–(i) adds |

### SPEC TESTS
| Item | Status | Reason |
|---|---|---|
| (j) a violating override map per hard rule + a conforming counterpart | done | see deviation D2 on how "an orchestration class" and "`mission`" relate |
| (k) the two schema faults | done | each with its own rule name; neither raises out of the validator |
| (l) the collecting property | done | 5 violations, declared order, provably not alphabetical; conforming map empty |
| (m) the builder | done | overlay, no mutation, raise, `.violations` and the message |
| (n) the override-aware resolver | done | all three reason cases |
| (o) HARD_RULE_NAMES unchanged | done | plus a per-name check that no schema name is in it |
| (p) REVIEWER_WORKER_CLASS_PAIRS members are seed-table keys, seed table conforms | done | |
| (q) the membership pin rewritten, not deleted | done | `test_the_covered_classes_are_exactly_the_set_decision_d2_declares` |

### Constraints
| Item | Status | Reason |
|---|---|---|
| 1 byte-for-byte slice application | done | all three slices extracted by marker index from the COMMITTED authored file with a script; nothing retyped |
| 2 C1 first substantive commit | done | |
| 3 C3 before C4 | done | |
| 4 newline conventions | done | see G3/G4; both files verified byte for byte |
| 5 no ruff gate | done | none ordered, none added, none run — see deviation D1 |
| 6 nothing wired, no config file | done | nothing imports the module but its own test; `config.py` neither edited nor imported; the deliberate-absence note is in the module docstring |
| 7 rounds 4/5 behaviour unrevised except `mission` | done | measured: 7 deletions, all in the two permitted regions |
| 8 exactly one existing test edited | done | plus the class docstring the constraint names; see deviation D3 |
| 9 stale sentences | done | one declared (below), two repaired in their own commit |
| 10 read `.agent/STOP` twice | done | absent both times |
| 11 self-review, push, disposable worktree, never `cd` into it | done | see deviation D4 on the worktree's location |

### Gates
| Item | Status | Reason |
|---|---|---|
| G1 transport | done | PASS |
| G2 the plan | done | PASS |
| G3 the ledger append | done | PASS |
| G4 the decisions append | done | PASS, with one reading declared — see D5 |
| G5 the module | done | PASS |
| G6 the red proof | done | PASS, all four mutations discriminate |
| G7 the suites | done | PASS |
| G8 tree, commits, sweep | done | PASS |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add /home/decodeux/Repos/remedy/remedy-review-f110-r6-wt a62d4920` | created, detached at a62d4920 |
| `git worktree remove /home/decodeux/Repos/remedy/remedy-review-f110-r6-wt --force` | removed |
| `git worktree prune` | exit 0 |
| `git push -u origin feature/f110-model-routing-by-task-class` | see the push line at the end of Verification |

No pull request created, none merged, no force-push, no history rewrite, no work
on `main`. The branch still has NO OPEN PULL REQUEST.

## Verification

One line per gate, then the transcripts.

- **G1 TRANSPORT** — PASS. One digest, twice. 397 lines against a projection of 397; cap 400.
- **G2 THE PLAN** — PASS. `cmp` exit 0; 44 lines (<50); `^## Goal` 1; `^## Next Steps` 1.
- **G3 THE LEDGER APPEND** — PASS. Arithmetic equal, second reader in order, negative control rejects, grep 0 → 1.
- **G4 THE DECISIONS APPEND** — PASS. Arithmetic equal, prefix survives, exactly one trailing newline, second reader in order, negative control rejects, grep 0 → 1. One reading declared as D5.
- **G5 THE MODULE** — PASS. 309 insertions / 7 deletions, every deletion in a permitted region; `ast.parse` clean; every shipped function RUN and its real return value recorded.
- **G6 THE RED PROOF** — PASS. Control 185 passed / 3 skipped, exit 0. Mutations redden 10, 7, 7 and 8 ids respectively; each leaves the other three mutations' own cases GREEN.
- **G7 THE SUITES** — PASS. 185 (+3 skipped, grown from 127), 33, 34, 63, 295, 42 — the last five unmoved.
- **G8 TREE / COMMITS / SWEEP** — PASS. Clean tree, no `.remedy-wt` files tracked, no worktree of this round's making survives, `docs/` untouched, every insertion count matches the Commits table above cell by cell.

### G1 transport

    $ sha256sum .agent/authored/f110-r6.md .agent/last_block.md
    41e6e7588d20ce43963390f5e2821906b36447a9ebb8022e46334ec36993fdce  .agent/authored/f110-r6.md
    41e6e7588d20ce43963390f5e2821906b36447a9ebb8022e46334ec36993fdce  .agent/last_block.md
    exit 0

    $ wc -l .agent/authored/f110-r6.md
    397 .agent/authored/f110-r6.md
    exit 0

397 lines against the reviewer's projection of 397 — EXACT, the third exact
projection in a row. The §3 cap of 400 is met with 3 lines to spare. No
difference to report and nothing repaired. File size 29021 bytes, no trailing
whitespace on any line, ends with exactly one newline.

### G2 the plan

PLAN6 was extracted from the COMMITTED authored file
(`git show HEAD:.agent/authored/f110-r6.md`), by index of the `<<<BEGIN PLAN6>>>`
and `<<<END PLAN6>>>` marker lines, markers excluded, with one trailing newline
added per constraint 4 (the target ends with one).

    $ cmp <extracted> .agent/plan.md
    (no output)
    exit 0

    $ wc -l .agent/plan.md
    44 .agent/plan.md            -> under 50, as AGENTS.md requires
    exit 0

    $ grep -c '^## Goal' .agent/plan.md
    1
    exit 0

    $ grep -c '^## Next Steps' .agent/plan.md
    1
    exit 0

The extraction scratch file was removed by exact path afterwards
(`/home/decodeux/Repos/remedy/.agent/g2_extracted_plan6`); `git status
--porcelain` was empty immediately after.

### G3 the ledger append (`.agent/live_review.md`)

    grep -c '^Gate: F110 R5 — ' .agent/live_review.md   BEFORE C2: 0
    grep -c '^Gate: F110 R5 — ' .agent/live_review.md   AFTER  C2: 1

Arithmetic, against the size immediately before C2:

    before               : 2164463      (the block's stated figure, confirmed)
    slice length         : 4500
    before + 2 + slice   : 2168965
    real new size        : 2168965
    EQUAL                : True
    ends WITHOUT newline : True
    base is exact PREFIX : True

Second reader — counts no byte, splits the WHOLE file on blank-line boundaries:

    N counted BY THE SCRIPT from the slice: 1
    LAST N units equal the slice's N paragraphs IN ORDER: True

Negative control — one byte flipped inside the FIRST appended paragraph, in a
scratch copy only:

    flipped byte offset: 2164475
    second reader REJECTS the flipped copy: True

### G4 the decisions append (`.agent/decisions.md`)

    grep -c '^## DECISION F110 D2 ' .agent/decisions.md   BEFORE C2: 0
    grep -c '^## DECISION F110 D2 ' .agent/decisions.md   AFTER  C2: 1

Arithmetic, against the size immediately before C2:

    before                    : 725637   (the block's stated figure, confirmed)
    slice length              : 2493
    before + 1 + slice + 1    : 728132
    real new size             : 728132
    EQUAL                     : True
    pre-C2 content is an exact byte PREFIX : True
    ends with EXACTLY one newline byte     : True

Second reader:

    N counted BY THE SCRIPT from the slice: 8
    LAST N units equal the slice's N paragraphs IN ORDER: True

Negative control:

    flipped byte offset: 725648  (inside the FIRST appended paragraph)
    second reader REJECTS the flipped copy: True

See deviation D5 for the one reading this gate required.

### G5 the module, measured and run

    $ git show --numstat ecd12bf2 -- packages/orchestration/model_routing.py
    309     7       packages/orchestration/model_routing.py
    exit 0

    ast.parse over its real text: OK, no exception
    disk bytes == the bytes committed at a62d4920: True

EVERY DELETED LINE, verbatim, with its region. Constraint 7 permits deletions
only in the ORCHESTRATION_TASK_CLASSES comment and definition and in the module
docstring. All 7 are in those two regions; NONE is from anywhere else.

MODULE DOCSTRING (4 lines — the opening paragraph, which C3 itself falsified by
adding the override schema to a module that said it held "nothing else yet"):

    -Owns the CLASS TABLE — which model TIER a declared task class is routed to — and
    -the THREE HARD RULES of docs/agents/model_routing_policy.md as named checks, each
    -returning ITS OWN rule name when a routing choice violates it. Nothing else yet:
    -no config file is read, no model id is named and no call site routes through it.

ORCHESTRATION_TASK_CLASSES COMMENT (3 lines — replaced by the wider DECISION D2
explanation SPEC CODE (a) orders):

    -#: every job it plans. Note that the seed table already routes ``mission`` to the
    -#: top tier; this set is what makes the guarantee a CHECKED rule rather than a
    -#: property of one table entry an override could quietly move.

THE SHIPPED CODE, RUN. What the functions RETURNED:

    ORCHESTRATION_TASK_CLASSES = ['mission', 'mission_compile', 'orchestrator']

    (k) unknown class -> (OverrideViolation(task_class='a_class_the_document_does_not_name', rule_name='override_unknown_task_class'),)
    (k) unknown tier  -> (OverrideViolation(task_class='format', rule_name='override_unknown_tier'),)

    (j) orchestration demoted -> (OverrideViolation(task_class='mission', rule_name='orchestration_below_top_tier'),)
    (j) orchestration conform -> ()
    (j) safety demoted        -> (OverrideViolation(task_class='architecture', rule_name='safety_class_below_mid_tier'),)
    (j) safety conform        -> ()
    (j) reviewer demoted      -> (OverrideViolation(task_class='standard_review', rule_name='reviewer_weaker_than_worker'),)
    (j) reviewer conform      -> ()

    (l) every rule at once -> ['override_unknown_task_class', 'override_unknown_tier',
                               'reviewer_weaker_than_worker', 'orchestration_below_top_tier',
                               'safety_class_below_mid_tier']
    (l) conforming map     -> ()

    (m) builder conforming -> {'format': 'mid', 'extract': 'cheap', 'summarize': 'cheap',
                               'boilerplate': 'cheap', 'standard_build': 'mid',
                               'standard_review': 'mid', 'architecture': 'top',
                               'mission': 'top', 'vision': 'top',
                               'prompt_authoring_for_other_agents': 'top'}
    (m) TASK_CLASS_TIERS unmutated -> {'format': 'cheap', 'extract': 'cheap',
                               'summarize': 'cheap', 'boilerplate': 'cheap',
                               'standard_build': 'mid', 'standard_review': 'mid',
                               'architecture': 'top', 'mission': 'top', 'vision': 'top',
                               'prompt_authoring_for_other_agents': 'top'}
    (m) raised type: OverrideRefused
    (m) violations : [('a_class_the_document_does_not_name', 'override_unknown_task_class'),
                      ('format', 'override_unknown_tier'),
                      ('standard_review', 'reviewer_weaker_than_worker'),
                      ('mission', 'orchestration_below_top_tier'),
                      ('architecture', 'safety_class_below_mid_tier')]
    (m) message    : per-project model-routing overrides refused — a_class_the_document_does_not_name: override_unknown_task_class, format: override_unknown_tier, standard_review: reviewer_weaker_than_worker, mission: orchestration_below_top_tier, architecture: safety_class_below_mid_tier

    (n) tier DIFFERS from seed -> ('top', 'per_project_override')
    (n) override RESTATES seed -> ('cheap', 'seed_mapping')
    (n) class not in the table -> ('top', 'unknown_class_conservative')

The fixture safety set used above is `frozenset({'architecture'})`, not the
`FIXTURE_SAFETY_CLASSES` round 5 used — see deviation D6 for why an override test
needs a safety class the SEED TABLE names.

### G6 the red proof

Worktree: `/home/decodeux/Repos/remedy/remedy-review-f110-r6-wt`, detached at
a62d4920 (the C4 commit). Never `cd`-ed into; every command addresses it by
absolute path. See deviation D4 for why it is not under `.remedy-wt/`.

PROVENANCE, printed from inside the worktree before any mutation, via a probe
test added to and then removed from the worktree by exact path:

    IMPORTED __file__ = /home/decodeux/Repos/remedy/remedy-review-f110-r6-wt/packages/orchestration/model_routing.py
    1 passed

So the mutated copy is provably the one imported. `find <worktree> -name
__pycache__ -type d` returned NOTHING at the start and every run used
`python3 -B`, so no stale bytecode could shadow a mutation.

**UNMUTATED CONTROL, FIRST:**

    $ python3 -B -m pytest <worktree>/tests/orchestration/test_model_routing.py -q
    185 passed, 3 skipped in 0.42s
    exit 0

**MUTATION (i) — `mission` removed from ORCHESTRATION_TASK_CLASSES again.**
10 failed, 172 passed, 3 skipped:

    TestOrchestrationCallsAlwaysTopTier::test_the_covered_classes_are_exactly_the_set_decision_d2_declares
    TestOverrideRefusedPerHardRule::test_mission_demoted_below_top_is_refused_with_the_rule_named
    TestOverrideValidatorCollectsEveryViolation::test_every_rule_is_reported_exactly_once
    TestOverrideValidatorCollectsEveryViolation::test_the_result_follows_the_declared_order
    TestOverrideValidatorCollectsEveryViolation::test_the_declared_order_is_provably_not_the_alphabet
    TestOverrideValidatorCollectsEveryViolation::test_the_schema_names_are_reported_before_the_hard_rule_names
    TestOverrideValidatorCollectsEveryViolation::test_an_override_key_may_be_spelled_as_the_document_words_it
    TestEffectiveTableBuilder::test_a_violating_map_raises_rather_than_dropping_the_offending_entry
    TestEffectiveTableBuilder::test_the_raised_object_carries_the_violations
    TestEffectiveTableBuilder::test_the_message_names_every_violated_rule[orchestration_below_top_tier]

**MUTATION (ii) — the reviewer-and-worker-pair leg always reports no violation.**
7 failed, 178 passed, 3 skipped:

    TestOverrideRefusedPerHardRule::test_the_reviewer_half_of_a_pair_demoted_below_its_worker_is_refused[standard_build-standard_review]
    TestOverrideRefusedPerHardRule::test_the_pair_violation_is_attributed_to_the_reviewer_class[standard_build-standard_review]
    TestOverrideValidatorCollectsEveryViolation::test_every_rule_is_reported_exactly_once
    TestOverrideValidatorCollectsEveryViolation::test_the_result_follows_the_declared_order
    TestOverrideValidatorCollectsEveryViolation::test_the_schema_names_are_reported_before_the_hard_rule_names
    TestEffectiveTableBuilder::test_the_raised_object_carries_the_violations
    TestEffectiveTableBuilder::test_the_message_names_every_violated_rule[reviewer_weaker_than_worker]

**MUTATION (iii) — the unknown-task-class schema check always reports no violation.**
7 failed, 178 passed, 3 skipped:

    TestOverrideSchemaFaults::test_an_override_naming_an_unknown_task_class_is_refused_with_its_own_rule
    TestOverrideValidatorCollectsEveryViolation::test_every_rule_is_reported_exactly_once
    TestOverrideValidatorCollectsEveryViolation::test_the_result_follows_the_declared_order
    TestOverrideValidatorCollectsEveryViolation::test_the_schema_names_are_reported_before_the_hard_rule_names
    TestEffectiveTableBuilder::test_the_raised_object_carries_the_violations
    TestEffectiveTableBuilder::test_the_message_names_every_violated_rule[override_unknown_task_class]
    TestEffectiveTableBuilder::test_a_schema_faulty_entry_is_refused_rather_than_silently_dropped

**MUTATION (iv) — the effective-table builder RETURNS the overlaid table instead
of raising.** 8 failed, 177 passed, 3 skipped, EVERY ONE of them inside
`TestEffectiveTableBuilder`:

    TestEffectiveTableBuilder::test_a_violating_map_raises_rather_than_dropping_the_offending_entry
    TestEffectiveTableBuilder::test_the_raised_object_carries_the_violations
    TestEffectiveTableBuilder::test_the_message_names_every_violated_rule[override_unknown_task_class]
    TestEffectiveTableBuilder::test_the_message_names_every_violated_rule[override_unknown_tier]
    TestEffectiveTableBuilder::test_the_message_names_every_violated_rule[reviewer_weaker_than_worker]
    TestEffectiveTableBuilder::test_the_message_names_every_violated_rule[orchestration_below_top_tier]
    TestEffectiveTableBuilder::test_the_message_names_every_violated_rule[safety_class_below_mid_tier]
    TestEffectiveTableBuilder::test_a_schema_faulty_entry_is_refused_rather_than_silently_dropped

**THE DISCRIMINATOR HOLDS, MUTATION BY MUTATION.** No mutation reddened
everything (the largest is 10 of 188 collected) and none reddened nothing:

| Under mutation → | (i)'s own cases | (ii)'s own cases | (iii)'s own case | (iv)'s own cases |
|---|---|---|---|---|
| (i) `mission` removed | RED | GREEN | GREEN | `test_a_schema_faulty_entry_...` GREEN |
| (ii) pair leg silenced | GREEN | RED | GREEN | `test_a_violating_map_raises_...` GREEN |
| (iii) unknown-class check silenced | GREEN | GREEN | RED | `test_a_violating_map_raises_...` GREEN |
| (iv) builder returns | GREEN | GREEN | GREEN | RED |

Where a mutation reddens a case outside its own class, the case is one of the
FOUR that deliberately exercise every rule at once
(`TestOverrideValidatorCollectsEveryViolation`'s collectors and the builder's
`.violations` / message checks) — those are supposed to notice any rule going
missing, and each mutation reddens exactly the ONE parametrised
`test_the_message_names_every_violated_rule[...]` case naming its own rule and
leaves the other four parameters green. That per-parameter separation is the
sharpest evidence in this gate.

`test_the_declared_order_is_provably_not_the_alphabet` is RED under (i) and GREEN
under (ii) and (iii), which is the honest reading: dropping the
`orchestration_below_top_tier` entry happens to leave the remaining four names in
alphabetical order, while dropping either of the other two does not.

REVERTS: every revert was
`git -C <worktree> checkout a62d4920 -- packages/orchestration/model_routing.py`
— restoring the file FROM THE C4 COMMIT inside the worktree, never a hand edit.
A post-revert control run after mutation (iv) returned to **185 passed, 3
skipped, exit 0**, so no mutation leaked into the next.

`git status --porcelain` was run in the PRIMARY checkout immediately after every
mutation and every revert, in the same step — eight readings — and again after
the worktree was added, after the probe file was removed, and after the worktree
was removed and pruned. ELEVEN readings, EMPTY every one.

CLEANUP: `git worktree remove /home/decodeux/Repos/remedy/remedy-review-f110-r6-wt --force`
then `git worktree prune`; `ls -d` on that exact path now returns
"No such file or directory".

### G7 the suites, each its own invocation, serially

    $ python3 -m pytest tests/orchestration/test_model_routing.py -q
    185 passed, 3 skipped in 0.33s                      exit 0    [was 127 — GREW by 58]

    $ python3 -m pytest tests/orchestration/test_orchestrator_model_routing.py tests/orchestration/test_job_role_routing.py -q
    33 passed in 0.27s                                  exit 0    [33 expected — unmoved]

    $ python3 -m pytest tests/orchestration/test_role_config.py -q
    34 passed in 0.23s                                  exit 0    [34 expected — unmoved]

    $ python3 -m pytest tests/orchestration/test_config.py -q
    63 passed in 0.34s                                  exit 0    [63 expected — unmoved]

    $ python3 -m pytest tests/docs/ -q
    295 passed in 0.44s                                 exit 0    [295 expected — unmoved]

    $ python3 -m pytest tests/cli/test_golden_path.py -q
    42 passed in 20.76s                                 exit 0    [42 expected — unmoved]

The unmoved 63 on `test_config.py` is constraint 6 MEASURED: this round adds
config vocabulary and touches no config loader. The 3 skips in the first suite
are round 5's pre-existing
`test_a_class_the_rule_does_not_cover_is_never_refused_by_it`, which skips a
class already covered by the violating fixture — `mission` now is one, across
all three tiers. The block projected exactly that shape.

### G8 the tree, the commits and the sweep

    $ git status --porcelain          (immediately before C5 was staged)
    (no output)
    exit 0

    $ git ls-files .remedy-wt
    (no output)
    exit 0

    $ git worktree list
    /home/decodeux/Repos/remedy                                  a62d4920 [feature/f110-model-routing-by-task-class]
    /home/decodeux/Repos/remedy/.remedy-wt/job-48a379ab5ca44ec5  f0e6b9a3 [remedy/job-48a379ab5ca44ec5]
    /home/decodeux/Repos/remedy/.remedy-wt/job-5e91e080219342d9  9fdb3b4b [remedy/job-5e91e080219342d9]
    /home/decodeux/Repos/remedy/.remedy-wt/job-7d1c93e2dc98415a  f0e6b9a3 [remedy/job-7d1c93e2dc98415a]
    /home/decodeux/Repos/remedy/.remedy-wt/job-98e9364a83a34872  21a45836 [remedy/job-98e9364a83a34872]
    /home/decodeux/Repos/remedy/.remedy-wt/job-f76686b8435640e9  4b49af98 [remedy/job-f76686b8435640e9]
    exit 0

The five `job-*` worktrees are NOT of this round's making and were left
untouched; the only worktree this round created is gone.

    $ git diff --stat 78071a87..a62d4920 -- docs/
    (no output)                       -> NO DOCS EDITED, as the block requires
    exit 0

INSERTION COUNTS, `git show --numstat`, the '+' column only, C0a through C4 —
compared CELL BY CELL against the Commits table above:

| Commit | numstat '+' | Commits table | Match |
|---|---|---|---|
| 007c6aee | 397 | 397 | yes |
| 6f54d420 | 305 | 305 | yes |
| c610156c | 19 | 19 | yes |
| fc668181 | 45 (.agent/decisions.md) + 3 (.agent/live_review.md) | 45 + 3 | yes |
| ecd12bf2 | 309 | 309 | yes |
| a62d4920 | 364 | 364 | yes |

Every commit is under the 500-insertion cap; no oversize commit to declare.

THE STALENESS SWEEP — one entry per file this round touched:

| File | Stale? | Why |
|---|---|---|
| .agent/authored/f110-r6.md | NOT stale | it is the round's own block, frozen by construction; digest-identical to its mirror |
| .agent/last_block.md | NOT stale | byte-identical mirror, proven by one digest twice at G1 |
| .agent/plan.md | NOT stale | rewritten this round; Current Step names round 6 / T002c, Next Steps names T003 and the seam round |
| .agent/live_review.md | NOT stale | append-only; the R5 entry is the verdict for the range it names, and earlier entries are historical by design |
| .agent/decisions.md | NOT stale | D2 appended; its REVERSE clause names `78071a87`, which git history still holds and which is this round's base |
| packages/orchestration/model_routing.py | NOT stale | the two sentences C3 itself falsified were repaired in C3 (see G5's deletion list); the Public API list gained every new name; "Nothing in production imports this module yet" is still TRUE — `grep` for an import of it across `packages/`, `apps/` and `tests/` returns exactly one hit, its own test file |
| tests/orchestration/test_model_routing.py | NOT stale | the module docstring's "T002a … and T002b" enumeration and the `TestOrchestrationCallsAlwaysTopTier` class docstring were both repaired in C4, in the commit that falsified them |
| .agent/handoff.md | NOT stale | this file, written now |

## Authored-text proofs

| Slice | Target | Result |
|---|---|---|
| PLAN6 | .agent/plan.md | `cmp` exit 0 against the extraction from the COMMITTED `.agent/authored/f110-r6.md` (G2) |
| RECORD5 | .agent/live_review.md | byte arithmetic equal, base an exact prefix, second reader in order, negative control rejects (G3) |
| DECISION2 | .agent/decisions.md | byte arithmetic equal, base an exact prefix, exactly one trailing newline, second reader in order, negative control rejects (G4) |

All three were extracted BY MARKER INDEX from the committed authored file with a
script. Nothing was retyped from the prompt. No slice looked wrong, so
constraint 1's "apply as written and declare it" clause was not exercised.

## Deviations & assumptions

**D1 — NO RUFF READING EXISTS AND NONE IS CLAIMED.** Constraint 5 forbids adding
a ruff gate and the block orders none; `ruff` is also refused by this worker's
permission layer, as it has been every round of this feature. The reviewer lints
both changed files. Instead of an invented number, two properties were measured
mechanically and are offered as what they are — not a lint result: no line in
either changed file exceeds the `pyproject.toml` `line-length = 120`, no line
carries trailing whitespace, and both files end with exactly one newline. The
import block of the test file was ordered under ruff-isort's `order-by-type`
convention (CONSTANTS, then CamelCase, then snake_case) to match the shape the
file already had.

**D2 — "AN ORCHESTRATION CLASS DEMOTED BELOW TOP" AND "`mission` DEMOTED BELOW
TOP" COLLAPSE TO THE SAME CLASS TODAY, AND THE TESTS SAY SO EXPLICITLY.** SPEC
TESTS (j) lists them as two fixtures. After DECISION F110 D2 the orchestration
set is `{mission, mission_compile, orchestrator}`, but `TASK_CLASS_TIERS` names
only `mission` of the three — so an override naming `orchestrator` or
`mission_compile` is a SCHEMA fault (`override_unknown_task_class`) and can never
reach hard rule 2. Both fixtures were written anyway, and differently: the
general one is parametrised over a module-level
`OVERRIDABLE_ORCHESTRATION_CLASSES`, computed as
`ORCHESTRATION_TASK_CLASSES & set(TASK_CLASS_TIERS)`, so it widens automatically
the day another orchestration class is seeded; the second is the explicit,
hard-coded `test_mission_demoted_below_top_is_refused_with_the_rule_named`, D2's
own acceptance fixture, carrying D2's reasoning in its comment. Nothing was
skipped and nothing was invented — but the reviewer should know the two currently
exercise one class.

**D3 — TWO SENTENCES WERE REPAIRED THAT THE BLOCK NAMED ONLY ONE OF, BOTH UNDER
CONSTRAINT 9, BOTH IN THE COMMIT THAT FALSIFIED THEM.** Constraint 8 names the
`TestOrchestrationCallsAlwaysTopTier` class docstring at line 357; that was
repaired in C4 as ordered. Two more sentences were falsified by this round's own
commits and were repaired in those same commits, on round 5's C4b precedent which
the reviewer accepted and which constraint 9 now states as a rule:

- C3, `model_routing.py`'s opening paragraph said the module owns the table and
  the hard rules and "Nothing else yet" — C3 itself added the override schema.
- C4, `test_model_routing.py`'s docstring first line enumerated "F110 T002a, the
  class table, and T002b, the three hard rules" — C4 itself added T002c's cases.
  This is an ENUMERATION going incomplete rather than a claim going false, which
  is the weaker case of the two; it is declared here so the reviewer can rule the
  other way if it disagrees. That repair also removed the file's only line over
  120 characters, which the previous wording had inherited.

No test was edited beyond the one constraint 8 names.

**D4 — THE DISPOSABLE WORKTREE IS NOT UNDER `.remedy-wt/`, AS THE BLOCK'S OWN
FALLBACK ALLOWS.** `.remedy-wt/` is denied to this worker and any command naming
a path under it is refused, so `git worktree add` was never attempted there. The
worktree was created at `/home/decodeux/Repos/remedy/remedy-review-f110-r6-wt` —
inside the repository, and invisible to `git status` because `.gitignore` carries
the pattern `remedy-review-*`. It was removed by that exact path and pruned;
`ls -d` on it now fails, and `git worktree list` shows only the primary checkout
and the five pre-existing `job-*` worktrees.

**D5 — G4'S SECOND READER NEEDED THE SLICE *AS APPLIED*, AND THE RAW-SLICE
READING IS REPORTED HERE RATHER THAN HIDDEN.** Read against the raw extracted
DECISION2 bytes, the last-N-paragraphs comparison returns **False**. The cause is
the FINAL unit only: the file's last paragraph is 179 bytes and the raw slice's
is 178, because constraint 4 makes the target's newline convention win and the
append is "one newline, then the slice, then one final newline". Units 0 through
6 match byte for byte under BOTH readings; only unit 7 differs, and only by that
one convention byte. Read against the slice AS APPLIED — the extracted bytes plus
the one target-convention newline, which is literally what C2 wrote — the second
reader returns **True**, and the negative control REJECTS a one-byte flip under
that same reading. G3 has no such split because `.agent/live_review.md` ends
without a newline, so its slice-as-applied and its raw slice are the same bytes.

**D6 — THE OVERRIDE TESTS NEEDED THEIR OWN FIXTURE SAFETY SET, AND ROUND 5'S
COULD NOT BE REUSED.** Round 5's `FIXTURE_SAFETY_CLASSES` is
`{fence_evaluation, dod_evaluation}` — neither is a key of `TASK_CLASS_TIERS`, so
an override naming either is refused as a SCHEMA fault before hard rule 3 ever
looks at it, and the safety rule would never have been shown to fire through an
override. A new module-level `OVERRIDE_SAFETY_CLASSES = frozenset({"architecture"})`
was added for the override tests, with the reason written at the constant.
`architecture` is seeded at the TOP tier, so the seed table alone conforms under
that set — pinned by `test_the_seed_table_alone_conforms_under_the_fixture_safety_set`,
which is the discriminator proving every refusal in those cases is caused by the
OVERRIDE and not by the fixture. Round 5's constant is untouched and its tests
are unchanged.

**D7 — A SENTENCE OUTSIDE THE CHANGE SET IS NOW STALE. DECLARED, NOT REPAIRED,
per constraint 9.** `docs/roadmap/features/T3_F110.md` line 30–31 reads
"orchestrator and mission-compile calls always top tier". The shipped
`ORCHESTRATION_TASK_CLASSES` now also holds `mission`, so the feature file's
sentence is narrower than the set that enforces it. This is not an accident: it
is the CONSEQUENCE paragraph of DECISION F110 D2, which rules explicitly that
nothing is renamed and the feature file is not edited, and the module states at
the constant why the set is deliberately wider. NO DOC WAS TOUCHED this round —
`git diff --stat 78071a87..a62d4920 -- docs/` lists nothing.

**D8 — A GAP WORTH NAMING, NOT A STALE SENTENCE.**
`docs/agents/model_routing_policy.md` contains no occurrence of the word
"override" at all (`grep -n 'override\|Override'` returns nothing). Nothing in it
is falsified by this round, so there is nothing to repair; but a reader who goes
to the policy document looking for the override rules will not find them, and the
counter-measure is the module docstring's own account rather than a doc edit this
block does not authorise. Flagged for the reviewer to route into a later round if
it disagrees.

**D9 — ONE SCRATCH FILE AND ONE PROBE TEST WERE CREATED AND REMOVED BY EXACT
PATH.** `/home/decodeux/Repos/remedy/.agent/g2_extracted_plan6` (the G2 extraction
target) and four `.agent/g34_*.bin` files (the G3/G4 pre-C2 snapshots and slice
bytes) lived in the primary checkout between gates; each was deleted by its exact
path, never by glob, and `git status --porcelain` was empty immediately after.
None was ever staged or committed. The G6 provenance probe
(`<worktree>/tests/orchestration/test_zz_import_provenance_probe.py`) existed only
inside the disposable worktree and was removed by exact path before the control
run, so it is in no measured count.

**ASSUMPTION.** The block's ordered commit sequence C0a → C0b → C1 → C2 → C3 →
C4 → C5 was followed exactly: no extra commit, none dropped, none reordered.

## Findings

Open findings: **278**, over 347 distinct registered and 69 distinct resolved,
recomputed from `.agent/live_review.md` under the first-R-id-per-`Done:`-line
reading F109's round 20 entry pinned as canonical — not carried from the previous
round. UNCHANGED: this round registered nothing and resolved nothing.

`.agent/prose_slips.md` was not touched; no reviewer-prose inaccuracy was found
that would belong in it.

## Next

**T003 — the promotion-evidence discipline**: the evidence fields and the
goldens, so a promotion to a cheaper tier without a benchmark evidence reference
is REFUSED and one with evidence is LOGGED. That is the next delegated round; the
session continues after this handback.

THE BRANCH STILL HAS NO OPEN PULL REQUEST, and none was created this round. The
next session's first action is Phase 1 rule 1 — read `.agent/STOP` from disk —
before Phase 1 rule 2, the Open PR Gate.
