# Handoff — F110 Model routing by task class, round 9

## Session

SESSION 3 of feature F110 · round 9 · rounds so far 9

## State

- Branch: `feature/f110-model-routing-by-task-class`, pushed, NO pull request open.
- Base of this round: `328228dc` (F110 R8 C6). HEAD before the handback: `8c57d0bc`.
- Fortschritt: T001 is CLOSED as designed — the role-to-class inventory (round 8),
  the single seam (round 8) and now THE WIRING. All seven inventoried call sites
  route, in ONE change, because all seven already funnel through
  `role_config.resolve_role_config`; that function now calls `route_role_call` and
  carries the routed-call evidence on the `RoleConfig` it already returned.
  DECISION F110 D4 is recorded. Round 8's PASS verdict and its prose slip are
  booked.
- Open findings: 278 open over 347 registered and 69 resolved — UNCHANGED, carried
  from the round-8 verdict booked this round; this round minted no id and resolved
  none. `R-0767` stays OPEN on the same seam and was not absorbed.
- `.agent/STOP` read TWICE, per constraint 10: before the first commit (`ls`
  reported "No such file or directory") and again before C5 (same). ABSENT both
  times.

## Range

Review of `328228dc..HEAD`.

## Commits

### d8747fb0 F110 R9 C0a: save the round 9 block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f110-r9.md` | +399 / -0 | the block saved by `shutil.copyfile`, byte-identical by construction |

### 366f0c0b F110 R9 C0b: mirror the block to last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +356 / -356 | mirrored from the COMMITTED authored file by `shutil.copyfile` |

### b789c394 F110 R9 C1: the round 9 plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +20 / -18 | PLAN9 applied; first substantive commit, item 23 |

### b3b1a9f5 F110 R9 C2: book round 8 - the verdict, the prose slip and DECISION D4
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +3 / -1 | RECORD8 appended (the file ends without a newline, so git counts the last line as rewritten) |
| `.agent/prose_slips.md` | +3 / -1 | SLIPS9 appended, same shape |
| `.agent/decisions.md` | +61 / -0 | DECISION F110 D4 appended |

### 6c7fb4eb F110 R9 C3: wire the routing seam into the role resolver
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/role_config.py` | +93 / -7 | the wiring: the import, the `routed_call` field, the fourth parameter, the one-exception helper, the deliberate absence |
| `packages/orchestration/model_routing.py` | +12 / -10 | MODULE DOCSTRING ONLY — the two sentences this round falsifies |

### 8c57d0bc F110 R9 C4: the routed evidence, the repair role and the invariants
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_role_config.py` | +217 / -0 | six new test classes, 48 new tests; ZERO deletions, so no existing test was edited, renamed, deleted or skipped |

### the handback commit (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this file; a handback cannot table the commit that writes it, and its numbers are measured at the next gate |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | |
| C0b mirror the block | done | |
| C1 PLAN9 | done | |
| C2 RECORD8 / SLIPS9 / DECISION4 | done | |
| C3 production | done | |
| C4 tests | done | one commit; the pre-authorised split was not needed (217 insertions) |
| C5 handback | done | |
| SPEC (a) the import and its direction | done | module-level, config -> policy, no cycle |
| SPEC (b) `routed_call` with `compare=False` | done | `field` added to the `dataclasses` import |
| SPEC (c) fourth parameter, last, defaulted | done | |
| SPEC (d) the one-exception helper | done | `resolve_routed_call_evidence` |
| SPEC (e) resolution unchanged | done | |
| SPEC (f) Public API list | deviated | three lines, not two — see deviation D2 |
| SPEC (g) the deliberate absence | done | |
| SPEC (h) the two falsified sentences | done | docstring only; both KEPT paragraphs verified present |
| SPEC (i) every declared role carries its evidence | done | 24 tests over the 8 declared roles |
| SPEC (j) the inheriting role | done | two origins at DIFFERENT tiers, asserted |
| SPEC (k) the undeclared role warns twice | done | category asserted, never a count of one |
| SPEC (l) hashable and comparable | done | |
| SPEC (m) the wiring changed no resolution | done | KNOWN_ROLES + a `config_file` override |
| SPEC (n) the inventory is unmoved | done | asserted against the constant, no spelled numeral |
| G1 transport | done | PASS |
| G2 the plan | done | PASS |
| G3 the ledger append | done | PASS |
| G4 the decisions append + prose_slips byte equality | done | PASS |
| G5 the two modules, measured and run | done | PASS |
| G6 the red proof | done | all four mutations detected; red sets NOT pairwise disjoint — deviation D3 |
| G7 the six suites | done | all exit 0 |
| G8 the tree, the commits and the sweep | done | PASS |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add /home/decodeux/Repos/remedy/remedy-review-r9-wt 8c57d0bc --detach` | created, detached at `8c57d0bc` |
| `git worktree remove /home/decodeux/Repos/remedy/remedy-review-r9-wt --force` | removed BY EXACT PATH |
| `git worktree prune` | exit 0 |
| `git push -u origin feature/f110-model-routing-by-task-class` | `328228dc..8c57d0bc`, branch tracked |

No PR created, none merged, no `gh` command run. The five
`.remedy-wt/job-*` worktrees are PRE-EXISTING and were not touched.

## Verification

### G1 TRANSPORT — PASS
    $ sha256sum .agent/authored/f110-r9.md .agent/last_block.md      exit 0
    59f9d6c6903248168c562ee2e348eb2a62908f96e1d31172d6f2d07502e07118  .agent/authored/f110-r9.md
    59f9d6c6903248168c562ee2e348eb2a62908f96e1d31172d6f2d07502e07118  .agent/last_block.md
    $ wc -l .agent/authored/f110-r9.md                               399
ONE digest twice, over 30628 bytes. The delivered scratch file carried the same
digest as the prompt stated, verified BEFORE anything else was done. Per
`docs/agents/planner_reviewer_prompt.md` item 37 this proves the saved copy and
its mirror agree and claims nothing about the emitted bytes.

### G2 THE PLAN — PASS
    $ cmp <PLAN9 extraction> .agent/plan.md      exit 0, no output
    $ wc -l .agent/plan.md                       exit 0, 46   (under 50)
    $ grep -c '^## Goal' .agent/plan.md          exit 0, 1
    $ grep -c '^## Next Steps' .agent/plan.md    exit 0, 1

### G3 THE LEDGER APPEND, `.agent/live_review.md` — PASS
    arithmetic  2185166 + 2 + 5032 = 2190200   real size 2190200   MATCH True
    pre-C2 content is an exact byte PREFIX: True (prefix length 2185166)
    still ends WITHOUT a newline: True
    SECOND READER: N counted from the slice = 1; last 1 blank-line unit of the
      whole file compared against the slice's 1 paragraph IN ORDER -> [True]
    NEGATIVE CONTROL: byte 2185168 flipped inside the FIRST appended paragraph,
      b'G' -> b'g'; the second reader ACCEPTS: False   (required False)
    header COPIED FROM THE SLICE (U+2014 EM DASH after "R8"): 'Gate: F110 R8 — '
      count of lines starting with it BEFORE C2: 0
      count of lines starting with it AFTER  C2: 1

### G4 THE DECISIONS APPEND, `.agent/decisions.md` — PASS
    arithmetic  731148 + 1 + 3695 + 1 = 734845   real size 734845   MATCH True
    pre-C2 content is an exact byte PREFIX: True (prefix length 731148)
    ends with EXACTLY ONE newline: True
    SECOND READER: N counted from the slice = 7; last 7 blank-line units of the
      whole file compared against the slice's 7 paragraphs IN ORDER ->
      [True, True, True, True, True, True, True]
    NEGATIVE CONTROL: byte 731152 flipped inside the FIRST appended paragraph,
      b'D' -> b'd'; the second reader ACCEPTS: False   (required False)
    $ grep -c '^## DECISION F110 D4 ' .agent/decisions.md
      BEFORE C2: exit 1, "0"      AFTER C2: exit 0, "1"

### G4 `.agent/prose_slips.md` — BYTE EQUALITY ONLY, per the gate budget — PASS
    final bytes == before + 2 newlines + SLIPS9 : True
    56793 == 55971 + 2 + 820 = 56793 ; base an exact PREFIX: True ;
    ends without a newline: True

### G5 THE TWO MODULES, MEASURED AND RUN — PASS
    $ git show --numstat --format= 6c7fb4eb      exit 0
    12      10      packages/orchestration/model_routing.py
    93      7       packages/orchestration/role_config.py

    $ ast.parse over both REAL files                exit 0
    ast.parse OK: packages/orchestration/role_config.py    12609 bytes
    ast.parse OK: packages/orchestration/model_routing.py  65588 bytes

EVERY DELETED LINE OF C3, QUOTED VERBATIM, WITH ITS REGION.

`packages/orchestration/model_routing.py` — 10 deletions, EVERY ONE INSIDE THE
MODULE DOCSTRING (which runs from line 1 to its closing `"""`; the two regions
are the opening paragraph's closing clause and the "does not WIRE THE SEAM"
paragraph). No deletion outside it, so no STOP condition arose:

    every provider call site will invoke. Nothing else yet: no config file is read,
    no model id is named and no call site routes through the seam.
    Remedy deliberately does not WIRE THE SEAM INTO ANY CALL SITE YET.
    :func:`route_role_call` is the one function every provider call site will invoke,
    and AT THIS COMMIT NOTHING CALLS IT — no file under ``packages/`` or ``apps/``
    other than this one imports this module. A reader searching for the place a call
    site routes through the seam must land HERE: that wiring is the NEXT round, and
    it is deliberately separate so the role declarations and the CALL-SITE INVENTORY
    (:data:`ROLE_CONFIG_CALL_SITES`) land — and start going red on a new, undeclared
    call site — BEFORE any routing behaviour moves.

The `mission_compile` paragraph and the "THE WORD TIER MEANS SOMETHING ELSE ONE
MODULE OVER" paragraph are UNCHANGED, as SPEC (h) requires; neither appears
above and both are present in the file.

`packages/orchestration/role_config.py` — 7 deletions, region named for each:

    resolve_role_config(role, cli_args=None, config_file=None) -> RoleConfig   [module docstring, Public API list]
    from dataclasses import dataclass                                          [module imports]
        for field in _FIELDS:                                                  [resolve_role_config body, the precedence loop]
            value = cli.get(field)                                             [same loop]
                value = cfg.get(field)                                         [same loop]
                resolved[field] = value                                        [same loop]
        return RoleConfig(role=role, **resolved)                               [resolve_role_config return]

THE SHIPPED CODE WAS RUN AND THIS IS WHAT IT RETURNED (`python3 -B`, real
process, primary checkout at C3):

    resolve_role_config(role).routed_call for every member of KNOWN_ROLES
      builder        -> {'task_class': 'standard_build',  'tier': 'mid',   'reason': 'seed_mapping', 'promoted_by': None}
      reviewer       -> {'task_class': 'standard_review', 'tier': 'mid',   'reason': 'seed_mapping', 'promoted_by': None}
      repair         -> None
      design_worker  -> {'task_class': 'architecture',    'tier': 'top',   'reason': 'seed_mapping', 'promoted_by': None}
      test_worker    -> {'task_class': 'standard_build',  'tier': 'mid',   'reason': 'seed_mapping', 'promoted_by': None}
      final_verifier -> {'task_class': 'standard_review', 'tier': 'mid',   'reason': 'seed_mapping', 'promoted_by': None}
      orchestrator   -> {'task_class': 'mission',         'tier': 'top',   'reason': 'seed_mapping', 'promoted_by': None}
      teacher        -> {'task_class': 'summarize',       'tier': 'cheap', 'reason': 'seed_mapping', 'promoted_by': None}
      summary        -> {'task_class': 'summarize',       'tier': 'cheap', 'reason': 'seed_mapping', 'promoted_by': None}

    the inheriting role
      repair, no origin       -> None
      repair, 'architecture'  -> {'task_class': 'architecture', 'tier': 'top',   'reason': 'seed_mapping', 'promoted_by': None}
      repair, 'format'        -> {'task_class': 'format',       'tier': 'cheap', 'reason': 'seed_mapping', 'promoted_by': None}
      the two tiers really do DIFFER: 'top' against 'cheap'

    an unknown role
      routed_call -> {'task_class': 'undeclared_role', 'tier': 'top', 'reason': 'unknown_class_conservative', 'promoted_by': None}
      provider/model/effort -> ollama muse-glimmer:latest medium   (the defaults, unmoved)
      warnings raised: [('UserWarning', "Unknown role 'nonexistent'; using default runtime confi"),
                        ('UserWarning', "Role 'nonexistent' declares no task class; routing cons")]

    hash() and equality
      hash(resolve_role_config("builder"))  -> 3580414363435600634
      two configs for one role compare equal -> True
      tuple(cfg.routed_call) == ROUTED_CALL_EVIDENCE_FIELDS -> True
        (('task_class', 'tier', 'reason', 'promoted_by'))

    the raise is UNCHANGED for a direct caller
      model_routing.route_role_call("repair") raised OriginatingTaskClassRequired, .role == 'repair'
      role_config.resolve_routed_call_evidence("repair") -> None

### G6 THE RED PROOF — all four mutations DETECTED
Disposable worktree `/home/decodeux/Repos/remedy/remedy-review-r9-wt` at
`8c57d0bc`, NEVER `cd`-ed into (every command ran with `cwd=` set on a
subprocess), `__pycache__` purged before every run, `python3 -B` throughout.

    module __file__ printed FROM INSIDE the worktree:
      /home/decodeux/Repos/remedy/remedy-review-r9-wt/packages/orchestration/role_config.py
    __pycache__ dirs purged before the control run: 0 (fresh worktree)

    UNMUTATED CONTROL   exit 0   82 passed   failures 0

    (i) remove the OriginatingTaskClassRequired catch in the helper
        exit 1 | 6 failed, 76 passed | failures 6
        primary checkout `git status --porcelain` immediately after: <empty>
        FULL LIST:
          tests/orchestration/test_role_config.py::TestAllRoles::test_each_known_role_resolves[repair]
          tests/orchestration/test_role_config.py::TestCliOverride::test_cli_nested_by_role
          tests/orchestration/test_role_config.py::TestCliOverride::test_cli_overrides_defaults
          tests/orchestration/test_role_config.py::TestRoleConfigStaysHashableAndComparable::test_configs_compare_on_provider_model_and_effort
          tests/orchestration/test_role_config.py::TestRoutedCallEvidenceForInheritingRoles::test_inheriting_role_records_nothing_without_an_origin[repair]
          tests/orchestration/test_role_config.py::TestWiringChangedNoResolution::test_every_known_role_resolves_exactly_as_before[repair]
        revert `git checkout -- packages/orchestration/role_config.py` (INSIDE the
          worktree) -> exit 0, 82 passed, back to the control's count: True

    (ii) the helper ignores its role argument and routes a fixed role
        exit 1 | 22 failed, 60 passed | failures 22
        primary checkout `git status --porcelain` immediately after: <empty>
        FULL LIST:
          ...::TestRoleConfigStaysHashableAndComparable::test_configs_compare_on_provider_model_and_effort
          ...::TestRoutedCallEvidenceForDeclaredRoles::test_declared_role_ignores_a_supplied_originating_class[design_worker]
          ...::TestRoutedCallEvidenceForDeclaredRoles::test_declared_role_ignores_a_supplied_originating_class[final_verifier]
          ...::TestRoutedCallEvidenceForDeclaredRoles::test_declared_role_ignores_a_supplied_originating_class[orchestrator]
          ...::TestRoutedCallEvidenceForDeclaredRoles::test_declared_role_ignores_a_supplied_originating_class[reviewer]
          ...::TestRoutedCallEvidenceForDeclaredRoles::test_declared_role_ignores_a_supplied_originating_class[summary]
          ...::TestRoutedCallEvidenceForDeclaredRoles::test_declared_role_ignores_a_supplied_originating_class[teacher]
          ...::TestRoutedCallEvidenceForDeclaredRoles::test_declared_role_records_its_declared_class[design_worker]
          ...::TestRoutedCallEvidenceForDeclaredRoles::test_declared_role_records_its_declared_class[final_verifier]
          ...::TestRoutedCallEvidenceForDeclaredRoles::test_declared_role_records_its_declared_class[orchestrator]
          ...::TestRoutedCallEvidenceForDeclaredRoles::test_declared_role_records_its_declared_class[reviewer]
          ...::TestRoutedCallEvidenceForDeclaredRoles::test_declared_role_records_its_declared_class[summary]
          ...::TestRoutedCallEvidenceForDeclaredRoles::test_declared_role_records_its_declared_class[teacher]
          ...::TestRoutedCallEvidenceForDeclaredRoles::test_declared_role_records_the_tier_the_seam_answers[design_worker]
          ...::TestRoutedCallEvidenceForDeclaredRoles::test_declared_role_records_the_tier_the_seam_answers[orchestrator]
          ...::TestRoutedCallEvidenceForDeclaredRoles::test_declared_role_records_the_tier_the_seam_answers[summary]
          ...::TestRoutedCallEvidenceForDeclaredRoles::test_declared_role_records_the_tier_the_seam_answers[teacher]
          ...::TestRoutedCallEvidenceForInheritingRoles::test_inheriting_role_records_nothing_without_an_origin[repair]
          ...::TestRoutedCallEvidenceForInheritingRoles::test_inheriting_role_records_the_originating_class[repair-architecture]
          ...::TestRoutedCallEvidenceForInheritingRoles::test_inheriting_role_records_the_originating_class[repair-format]
          ...::TestRoutedCallEvidenceForUndeclaredRoles::test_both_layers_warn_and_every_warning_is_a_user_warning
          ...::TestRoutedCallEvidenceForUndeclaredRoles::test_undeclared_role_routes_conservatively
        (every id above is prefixed `tests/orchestration/test_role_config.py`;
         nothing is truncated — this is the complete list of 22)
        revert -> exit 0, 82 passed, back to the control's count: True

    (iii) drop compare=False from the field of SPEC (b)
        exit 1 | 2 failed, 80 passed | failures 2
        primary checkout `git status --porcelain` immediately after: <empty>
        FULL LIST:
          tests/orchestration/test_role_config.py::TestRoleConfigStaysHashableAndComparable::test_a_resolved_config_with_real_evidence_is_hashable
          tests/orchestration/test_role_config.py::TestRoleConfigStaysHashableAndComparable::test_configs_compare_on_provider_model_and_effort
        revert -> exit 0, 82 passed, back to the control's count: True

    (iv) the helper ignores originating_task_class and always passes None
        exit 1 | 3 failed, 79 passed | failures 3
        primary checkout `git status --porcelain` immediately after: <empty>
        FULL LIST:
          tests/orchestration/test_role_config.py::TestRoleConfigStaysHashableAndComparable::test_configs_compare_on_provider_model_and_effort
          tests/orchestration/test_role_config.py::TestRoutedCallEvidenceForInheritingRoles::test_inheriting_role_records_the_originating_class[repair-architecture]
          tests/orchestration/test_role_config.py::TestRoutedCallEvidenceForInheritingRoles::test_inheriting_role_records_the_originating_class[repair-format]
        revert -> exit 0, 82 passed, back to the control's count: True

PAIRWISE DISJOINTNESS — MEASURED, AND THE ANSWER IS NO. Reported as measured,
not assumed (deviation D3):

    (i)  vs (ii)   intersection 2  {test_configs_compare_on_provider_model_and_effort,
                                    test_inheriting_role_records_nothing_without_an_origin[repair]}
    (i)  vs (iii)  intersection 1  {test_configs_compare_on_provider_model_and_effort}
    (i)  vs (iv)   intersection 1  {test_configs_compare_on_provider_model_and_effort}
    (ii) vs (iii)  intersection 1  {test_configs_compare_on_provider_model_and_effort}
    (ii) vs (iv)   intersection 3  {test_configs_compare_on_provider_model_and_effort,
                                    test_inheriting_role_records_the_originating_class[repair-architecture],
                                    test_inheriting_role_records_the_originating_class[repair-format]}
    (iii) vs (iv)  intersection 1  {test_configs_compare_on_provider_model_and_effort}

Mutations (i), (ii) and (iii) each still carry ids NO other mutation reddens, so
each is individually discriminated. Mutation (iv)'s red set is a strict SUBSET of
(ii)'s: routing a fixed role also discards the originating class, so (ii) is the
wider fault and contains (iv)'s. Every mutation is DETECTED (exit 1); none is
uniquely fingerprinted against (ii) alone. Read the honest limit rather than a
disjointness claim the measurement does not support.

### G7 THE SUITES — each its own invocation, run serially, every one exit 0

| Command | Exit | Measured | Block's figure at base | Difference |
|---|---|---|---|---|
| `pytest tests/orchestration/test_role_config.py -q` | 0 | 82 passed | 34 | +48, this round's new tests; 82 − 48 = 34 confirms the base |
| `pytest tests/orchestration/test_model_routing.py -q` | 0 | 391 passed, 3 skipped, 1 warning | 391 passed, 3 skipped | UNMOVED |
| `pytest tests/orchestration/test_teacher_model.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_orchestrator_model_routing.py tests/orchestration/test_job_role_routing.py tests/cli/test_teach_cmd.py -q` | 0 | 87 passed | 87 | UNMOVED |
| `pytest tests/test_do_job_flow.py tests/orchestration/test_job_evidence.py tests/orchestration/test_execution_config_evidence.py tests/orchestration/test_task_plan_evidence.py tests/orchestration/test_token_cost_policy.py tests/orchestration/test_model_aliases.py -q` | 0 | 333 passed | 333 | UNMOVED |
| `pytest tests/docs/ -q` | 0 | 295 passed | 295 | UNMOVED |
| `pytest tests/cli/test_golden_path.py -q` | 0 | 42 passed | 42 | UNMOVED, the canary |

The block's own combined figure — "425 passed, 3 skipped" for the two routing
suites together — is 34 + 391, i.e. the reviewer applied the PRODUCTION change
without this round's tests. This round measures 82 + 391 = 473 passed with the
same 3 skipped, because C4 adds 48 tests. The four UNMOVED suites are the
regression evidence for the five call sites that pass a role VARIABLE.

### G8 THE TREE, THE COMMITS AND THE SWEEP — PASS

    $ git status --porcelain                      exit 0, EMPTY (immediately before C5 is staged)
    $ git ls-files .remedy-wt                     exit 0, EMPTY
    $ git worktree list                           exit 0 — the primary checkout plus the five
      PRE-EXISTING .remedy-wt/job-* worktrees; NO worktree of this round's making survives
    $ git diff --stat 328228dc..8c57d0bc -- docs/                              exit 0, EMPTY
    $ git diff --stat 328228dc..8c57d0bc -- packages/ apps/ \
        ':(exclude)packages/orchestration/role_config.py' \
        ':(exclude)packages/orchestration/model_routing.py'                    exit 0, EMPTY
      — constraint 6 MEASURED rather than asserted: outside those two files, no
        file under packages/ or apps/ changed, and NO CALL SITE WAS EDITED.

PER-COMMIT INSERTION COUNTS, the `+` column only, cell by cell against the
`## Commits` table above; the handback commit's own numbers appear in neither
place:

| Commit | Insertions | Table agrees | Under the 500 cap |
|---|---|---|---|
| `d8747fb0` | 399 | 399 | yes |
| `366f0c0b` | 356 | 356 | yes |
| `b789c394` | 20 | 20 | yes |
| `b3b1a9f5` | 67 | 61 + 3 + 3 = 67 | yes |
| `6c7fb4eb` | 105 | 93 + 12 = 105 | yes |
| `8c57d0bc` | 217 | 217 | yes |

No commit needed the oversize exception; none was declared.

## Authored-text proofs

Every slice was extracted BY DELIMITER INDEX, marker lines EXCLUDED, from the
COMMITTED `.agent/authored/f110-r9.md` by
`remedy-review-r9-scratch/extract.py` — never retyped and never taken from the
delegating prompt. C0a and C0b both used `shutil.copyfile`, so the saved copy and
its mirror are byte-identical to the delivered file by construction. Disk-to-disk
re-derivation AFTER the commits:

    PLAN9     .agent/plan.md == PLAN9 + the target's one trailing newline      True
    RECORD8   .agent/live_review.md ends with 2 newlines + RECORD8 (5032 B)    True
    SLIPS9    .agent/prose_slips.md ends with 2 newlines + SLIPS9 (820 B)      True
    DECISION4 .agent/decisions.md ends with newline + DECISION4 (3695 B) + nl  True

The four byte figures of constraint 4 were re-measured on disk at THIS round's
base before any append and all four were CORRECT: `.agent/live_review.md`
2185166 without a trailing newline, `.agent/prose_slips.md` 55971 the same shape,
`.agent/decisions.md` 731148 with exactly one, `.agent/plan.md` 1969 with one.
That is round 8's deviation D1 not repeating.

## Deviations & assumptions

**D1 — an unordered rename inside the function the round edits.**
SPEC (b) orders `field` onto the `from dataclasses import dataclass` line. The
existing precedence loop in `resolve_role_config` was `for field in _FIELDS:`,
which after that import SHADOWS the newly-imported `dataclasses.field` inside the
one function this round rewrites. The loop variable was renamed to `field_name`
(4 of C3's 7 deletions in `role_config.py`). Behaviour is identical — the loop
reads `cli`/`cfg` and writes `resolved` exactly as before, and all six G7 suites
pass — but the SPEC did not order it, so it is declared rather than left silent.

**D2 — SPEC (f) asked for two Public API lines and three were written.**
The list gained a line for `RoleConfig.routed_call` and a line for
`resolve_role_config`'s new parameter as ordered, and ALSO a line for
`resolve_routed_call_evidence`, the module-level helper SPEC (d) orders. That
helper is a public name in a module whose docstring lists its public names; a
public function absent from the list is exactly the discoverability gap AGENTS.md
warns about. Declared because it is one line more than the SPEC counted.

**D3 — G6's red sets are NOT pairwise disjoint, and the block asked for the
measurement rather than the claim.** All six pairs intersect; the full matrix is
in the G6 transcript above. `test_configs_compare_on_provider_model_and_effort`
is in all four red sets because it asserts BOTH that the two `routed_call`
payloads differ AND that the configs compare and hash equal — every one of the
four mutations breaks one of those halves. Mutation (iv)'s set is a strict subset
of (ii)'s. Each mutation is still DETECTED, and (i), (ii) and (iii) each own ids
no other mutation reddens.

**D4 — the G6 harness's first pass printed a wrong reading, corrected and
re-run.** Its "back to control" check compared the whole pytest summary LINE,
which carries the elapsed time, so it printed `False` four times while the COUNT
had returned to 82 passed / exit 0 every time. The harness was corrected to strip
the timing and the whole gate was RE-RUN from the control; the transcript above
is the corrected run. The first, wrong reading is declared rather than quietly
replaced.

**D5 — a sentence OUTSIDE the change set that this round makes imprecise, NOT
repaired (constraint 9).** `docs/roadmap/features/T3_F110.md`, "Task slicing",
T001 bullet: "call-site/role inventory + the single resolver seam (consolidation
order if needed) + class declarations on all call sites." This round satisfies
"class declarations on all call sites" AT THE SHARED RESOLVER rather than at each
of the seven sites — DECISION F110 D4 rejected the per-site route explicitly.
No file under `docs/` was written, per constraint 9 and the change set; the block
already assigns the Design-bullet update to the closure round.

**Nothing else measured stale.** `tests/orchestration/test_model_routing.py`'s
module docstring was read in full and asserts nothing about the seam being
unwired; no test reads `model_routing.__doc__`; a grep for `route_role_call`,
"routes through the seam", "NOTHING CALLS IT", "not wired" and "WIRE THE SEAM"
over `docs/`, `packages/`, `apps/` and `tests/` returns no other claim this round
falsifies. `docs/agents/model_routing_policy.md` names no seam at all.

**No ruff run and no lint gate added**, per constraint 5 — the reviewer lints.
**No existing test edited, renamed, deleted or skipped**, per constraint 8:
C4 is `217 insertions, 0 deletions` on `tests/orchestration/test_role_config.py`,
which is that constraint measured rather than asserted.
**Rounds 4 through 8 shipped behaviour is not revised**, per constraint 7:
`model_routing.py` changed only inside its module docstring (all 10 deletions
quoted above), and `route_role_call` still RAISES for a direct caller — run and
shown in G5.
**No blocked item.** No commit was split; C4's pre-authorised split was not needed.

## Next

Window 1 reviews `328228dc..HEAD` and rules on round 9. The next build round is
the CONFIGURATION round: the per-project override map and the promotion-evidence
map READ from configuration rather than defaulting to the shipped table
(consolidation order E.d).
