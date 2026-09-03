# Handback — F110 R8 (T001, the role and call-site inventory, and the routing seam)

## Session

SESSION 2 of feature F110 · round 8 · rounds so far 8

Soft limit (25 rounds / 7 sessions) not reached: 8 rounds, 2 sessions. No scope
report is owed.

`.agent/STOP` read from disk twice, as constraint 10 orders — once before the
first commit (C0a) and again before C5. ABSENT both times.

THIS IS THE LAST ROUND OF THE SESSION.

## State

| Feld | Wert |
|------|------|
| **Feature** | F110 Model routing by task class (Tier 3, depends on F103) |
| **Branch** | `feature/f110-model-routing-by-task-class` |
| **Round** | 8 (session 2), step T001 — the role/call-site inventory and the seam |
| **Base** | `4cfcb464` |
| **Head** | `f7765ec0` (last test commit) → C5 is the handback commit |
| **Open findings** | 278 open, over 347 registered and 69 resolved — UNCHANGED; this round minted no R-id |
| **`.agent/candidates.md`** | untouched, still declares EMPTY |
| **Open PR** | NONE on this branch |
| **Tree** | clean at every commit; `git status --porcelain` empty |

## Range

Review of `4cfcb464..f7765ec0` (plus the C5 handback commit).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block verbatim | done | |
| C0b mirror to `last_block.md` | done | |
| C1 apply PLAN8 | done | first substantive commit, item 23 |
| C2 RECORD7 + SLIPS8 + DECISION3 | done | one commit, three appends |
| C3 production | done | 253 insertions, 6 deletions, all 6 in the module docstring |
| C4 tests | done | 370 insertions — under the cap, so NOT split |
| C5 handback | done | this file |
| SPEC (a) role-to-class map | done | `ROLE_TASK_CLASSES`, 8 roles, exactly the reviewer's reading |
| SPEC (b) inheriting roles | done | `TASK_CLASS_INHERITING_ROLES`, `repair` alone |
| SPEC (c) role resolver | done | `resolve_role_task_class` |
| SPEC (d) the seam | done | `route_role_call` |
| SPEC (e) call-site inventory | done | `ROLE_CONFIG_CALL_SITES`, 7 pairs, no line numbers |
| SPEC (f) deliberate absence | done | `mission_compile`, in the module docstring |
| SPEC Public API extension | done | 10 new lines in the docstring's Public API list |
| SPEC (g) declared classes are seed keys / disjoint | done | `TestEveryDeclaredRoleClassIsASeedTableKey` |
| SPEC (h) the repair rule executes and discriminates | done | `TestTheRepairRuleIsExecutable` |
| SPEC (i) a declared role ignores an originating class | done | `TestADeclaredRoleIgnoresAnOriginatingClass` |
| SPEC (j) orchestrator routes to the top tier | done | `TestTheOrchestratorRoleRoutesToTheTopTier` |
| SPEC (k) the seam's evidence mapping + GOLDEN | done | `TestTheSeamReturnsTheRoutedCallEvidence` |
| SPEC (l) the inventory is checked | done | `TestTheCallSiteInventoryIsChecked` |
| SPEC (m) the undeclared role warns | done | `TestTheUndeclaredRolePathWarnsAndAnswersConservatively` |
| G1 transport | done | one digest twice; 399 lines against a projection of 399 |
| G2 the plan | done | `cmp` exit 0, 44 lines, one `## Goal`, one `## Next Steps` |
| G3 the ledger append | done | arithmetic exact, second reader in order, negative control rejected |
| G4 decisions + prose_slips | done | arithmetic exact; prose_slips byte-equality only, per the gate budget |
| G5 the module, measured and run | done | 253/6, `ast.parse` clean, every function RUN |
| G6 the red proof | done | control 391/3; four mutations red 4, 2, 3 and 5 ids; no id shared |
| G7 the suites | done | 391+3, 33, 34, 63, 295, 42 — all exit 0 |
| G8 tree, commits, sweep | done | clean tree, no docs diff, no packages/apps diff outside the module |

## Commits

### 50adb6a8 F110 R8 C0a: save the round 8 block verbatim
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f110-r8.md` | +399 / -0 | the block, byte for byte |

### e54c81fc F110 R8 C0b: mirror the block to last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +305 / -257 | `shutil.copyfile` of the committed authored file |

### 4b476fb7 F110 R8 C1: the plan names round 8, the inventory and the seam
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +16 / -16 | PLAN8 applied byte for byte |

### 34a77f33 F110 R8 C2: book round 7 - the verdict, the prose slip and DECISION D3
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/decisions.md` | +49 / -0 | DECISION3 appended |
| `.agent/live_review.md` | +3 / -1 | RECORD7 appended |
| `.agent/prose_slips.md` | +3 / -1 | SLIPS8 appended |

### f342e3e7 F110 R8 C3: the role-to-class map, the inheriting roles and the routing seam
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/model_routing.py` | +253 / -6 | SPEC (a)–(f) + the Public API list |

### f7765ec0 F110 R8 C4: the inventory sweep, the executable repair rule and the seam
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_model_routing.py` | +370 / -4 | SPEC (g)–(m) |

### C5 — the handback commit
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | a handoff cannot table the commit that writes it (R-0149 pattern) |

Per-commit INSERTION counts, the `+` column only, for every commit before the
handback commit: **399, 305, 16, 55, 253, 370**. Every one is under the
AGENTS.md 500-insertion cap; no oversize exception was spent this round, and
C4 therefore was NOT split.

## External actions

| Command | Outcome |
|---|---|
| `git worktree add /home/decodeux/Repos/remedy/remedy-review-r8-wt f7765ec0 --detach` | created, detached at `f7765ec0` |
| `git worktree remove /home/decodeux/Repos/remedy/remedy-review-r8-wt --force` | removed BY EXACT PATH |
| `git worktree prune` | ran; only the five pre-existing `.remedy-wt/job-*` worktrees survive |
| `git push -u origin feature/f110-model-routing-by-task-class` | pushed after C5 |

No pull request created. No merge. No force-push. No history rewrite.

## Verification

**G1 TRANSPORT** — exit 0.

    $ sha256sum .agent/authored/f110-r8.md .agent/last_block.md
    11b0c5855d8a82ee04728791ef426d8c5473ae15ca13025441c0cc35828eee5e  .agent/authored/f110-r8.md
    11b0c5855d8a82ee04728791ef426d8c5473ae15ca13025441c0cc35828eee5e  .agent/last_block.md
    $ wc -l .agent/authored/f110-r8.md
    399 .agent/authored/f110-r8.md

ONE DIGEST TWICE. 33816 bytes. **399 lines against the Handback paragraph's
projection of 399 — EXACT, and under the cap of 400.** The fifth exact
projection in a row. The committed blob was also compared to the working copy
inside the extractor (`git show HEAD:.agent/authored/f110-r8.md` == disk: True),
so every slice below was extracted from the COMMITTED bytes.

**G2 THE PLAN** — exit 0.

    $ cmp <PLAN8 extracted from the committed authored file> .agent/plan.md
    (no output — exit 0)
    $ wc -l .agent/plan.md
    44 .agent/plan.md
    $ grep -c '^## Goal' .agent/plan.md
    1
    $ grep -c '^## Next Steps' .agent/plan.md
    1

44 lines, under 50. The extracted PLAN8 is 1968 bytes marker-excluded; the file
is 1969 — PLAN8 plus the ONE trailing newline the target's convention adds,
which is the reading round 7's own record states and the reading under which
`cmp` exits 0.

**G3 THE LEDGER APPEND** — `.agent/live_review.md`.

    arithmetic: 2177227 + 2 + 7937 = 2185166 ; real new size 2185166 ; equal=True
    pre-C2 content is an exact byte PREFIX: True
    still ends WITHOUT a newline: True
    SECOND READER: N counted by the script from the slice = 1
    last N units equal the slice paragraphs IN ORDER: True
    NEGATIVE CONTROL (flip byte at offset 2177229, inside the FIRST appended
      paragraph): second reader accepts = False
    $ grep -c '^Gate: F110 R7 — ' .agent/live_review.md
    0   (before C2)
    1   (after C2)

**G4 THE DECISIONS APPEND** — `.agent/decisions.md`.

    arithmetic: 728132 + 1 + 3014 + 1 = 731148 ; real new size 731148 ; equal=True
    pre-C2 content is an exact byte PREFIX: True
    ends with exactly ONE newline byte: True
    SECOND READER: N counted by the script from the slice = 8
    last N units equal the slice paragraphs IN ORDER: True
    NEGATIVE CONTROL (flip byte at offset 728133, inside the FIRST appended
      paragraph): second reader accepts = False
    $ grep -c '^## DECISION F110 D3 ' .agent/decisions.md
    0   (before C2)
    1   (after C2)

**G4 `.agent/prose_slips.md`** — byte-equality only, per the gate budget.

    final bytes == before + 2 newlines + SLIPS8: True
    pre-C2 content an exact byte PREFIX: True
    still ends WITHOUT a newline: True
    sizes: before 54853, slice 1116, after 55971

**The before-size is 54853 and NOT the 53575 constraint 4 states — DEVIATION D1
below.** The append itself is exact under either number; only the block's stated
base byte count is wrong, and it gates nothing here because this file gets a
byte-equality check rather than arithmetic.

**G5 THE MODULE, MEASURED AND RUN.**

    $ git show --numstat f342e3e7 -- packages/orchestration/model_routing.py
    253	6	packages/orchestration/model_routing.py
    $ python3 -c "ast.parse(<the real file text>)"
    ast.parse OK, lines 1262

EVERY DELETED LINE, VERBATIM, AND THE REGION IT CAME FROM — all six are in the
MODULE DOCSTRING, which G5 permits:

    -is applied, and the PROMOTION-EVIDENCE DISCIPLINE that refuses a move to a
    -CHEAPER tier unless a documented benchmark run backs it. Nothing else yet: no
    -config file is read, no model id is named and no call site routes through it.
      → the docstring's opening paragraph; rewritten because this round's own
        commit falsifies "Nothing else yet" (constraint 9 repairs in-file).
    -Nothing in production imports this module yet: the per-call-site task-class
    -declarations come after the resolver seam work, so the table lands and is
    -pinned before anything routes through it.
      → the docstring's "nothing routes yet" paragraph; the clause "the
        per-call-site task-class declarations come after the resolver seam work"
        became false this round, so it was repaired in the same commit.

NO DELETION FALLS OUTSIDE THE MODULE DOCSTRING. No constant and no function of
rounds 4 through 7 changed behaviour or signature; constraint 7 holds.

THE SHIPPED CODE, RUN — what the functions RETURNED:

    ROLE_TASK_CLASSES = {'builder': 'standard_build', 'reviewer': 'standard_review',
      'design_worker': 'architecture', 'test_worker': 'standard_build',
      'final_verifier': 'standard_review', 'teacher': 'summarize',
      'summary': 'summarize', 'orchestrator': 'mission'}
    TASK_CLASS_INHERITING_ROLES = frozenset({'repair'})
    UNDECLARED_ROLE_TASK_CLASS = 'undeclared_role'
    DYNAMIC_ROLE_MARKER = '<dynamic>'
    ROLE_CONFIG_RESOLVER_NAME = 'resolve_role_config'
    ROLE_CONFIG_CALL_SITES:
        ('apps/cli/commands/do_cmd.py', '<dynamic>')
        ('packages/orchestration/artifact_summary.py', 'summary')
        ('packages/orchestration/pingpong_job.py', '<dynamic>')
        ('packages/orchestration/role_config.py', 'orchestrator')
        ('packages/orchestration/self_use_runner.py', '<dynamic>')
        ('packages/orchestration/teacher_model.py', '<dynamic>')
        ('packages/orchestration/teacher_model.py', '<dynamic>')

`resolve_role_task_class` on EVERY member of `role_config.KNOWN_ROLES`:

    builder         -> standard_build
    reviewer        -> standard_review
    repair          -> architecture      (originating=architecture supplied)
    design_worker   -> architecture
    test_worker     -> standard_build
    final_verifier  -> standard_review
    orchestrator    -> mission
    teacher         -> summarize
    summary         -> summarize

An inheriting role with NO originating class:

    RAISED OriginatingTaskClassRequired | .role = 'repair'
    message: role 'repair' inherits its task class and no originating task class
    was supplied; docs/agents/model_routing_policy.md: 'Repair prompts follow the
    tier of the original task class.'

A role NEITHER set names:

    returned 'undeclared_role' | warnings: 1 | UserWarning
    warning: Role 'nightwatchman' declares no task class; routing conservatively
      as 'undeclared_role'. Declared roles: builder, design_worker,
      final_verifier, orchestrator, reviewer, summary, teacher, test_worker;
      inheriting roles: repair.
    routed: {'task_class': 'undeclared_role', 'tier': 'top',
             'reason': 'unknown_class_conservative', 'promoted_by': None}

THE SEAM:

    orchestrator : {'task_class': 'mission', 'tier': 'top',
                    'reason': 'seed_mapping', 'promoted_by': None}
    builder      : {'task_class': 'standard_build', 'tier': 'mid',
                    'reason': 'seed_mapping', 'promoted_by': None}
    builder with an originating class of a DIFFERENT tier (IGNORED):
                   {'task_class': 'standard_build', 'tier': 'mid',
                    'reason': 'seed_mapping', 'promoted_by': None}
    repair<-architecture: {'task_class': 'architecture', 'tier': 'top',
                    'reason': 'seed_mapping', 'promoted_by': None}
    repair<-format      : {'task_class': 'format', 'tier': 'cheap',
                    'reason': 'seed_mapping', 'promoted_by': None}
    design_worker on a PROMOTED table with sufficient evidence:
                   {'task_class': 'architecture', 'tier': 'cheap',
                    'reason': 'per_project_override',
                    'promoted_by': 'qwen3-8b-instruct + q4_k_m@0f1e2d3c4b5a6978 on F082'}
    hard rule 2 on ROLE_TASK_CLASSES['orchestrator'] routed at the cheapest tier:
                   'orchestration_below_top_tier'

AN AST SWEEP OF MY OWN over `packages/` and `apps/`, printed beside the constant:

    REVIEWER-INDEPENDENT SWEEP (7) | SHIPPED CONSTANT (7)
      ('apps/cli/commands/do_cmd.py', '<dynamic>')               | (identical)
      ('packages/orchestration/artifact_summary.py', 'summary')  | (identical)
      ('packages/orchestration/pingpong_job.py', '<dynamic>')    | (identical)
      ('packages/orchestration/role_config.py', 'orchestrator')  | (identical)
      ('packages/orchestration/self_use_runner.py', '<dynamic>') | (identical)
      ('packages/orchestration/teacher_model.py', '<dynamic>')   | (identical)
      ('packages/orchestration/teacher_model.py', '<dynamic>')   | (identical)
    MULTISETS EQUAL: True

The block's measurement of the seven call sites is confirmed independently,
including the DOUBLE call in `teacher_model.py` and the two literal roles.

**G6 THE RED PROOF** — disposable worktree
`/home/decodeux/Repos/remedy/remedy-review-r8-wt` at `f7765ec0`, never `cd`-ed
into (every command ran through `subprocess` with `cwd`), `__pycache__` purged
before every run, `python3 -B` throughout.

    IMPORTED __file__ FROM INSIDE THE WORKTREE:
      /home/decodeux/Repos/remedy/remedy-review-r8-wt/packages/orchestration/model_routing.py

UNMUTATED CONTROL, FIRST: exit 0, **391 passed, 3 skipped**.

    === (i) inheriting role returns a FIXED class instead of the originating one
        exit 1 | 4 failed, 387 passed, 3 skipped
        PRIMARY CHECKOUT git status --porcelain: ''
        RED (4):
          TestTheRepairRuleIsExecutable::test_the_inheriting_role_returns_the_originating_class[architecture]
          TestTheRepairRuleIsExecutable::test_the_originating_class_may_be_spelled_as_the_document_words_it
          TestTheRepairRuleIsExecutable::test_the_seam_routes_it_to_the_originating_classes_tier[architecture]
          TestTheSeamReturnsTheRoutedCallEvidence::test_a_promoted_class_carries_the_run_that_promoted_it
        REVERTED (git checkout -- packages/orchestration/model_routing.py, inside
        the worktree): 391 passed, 3 skipped, exit 0

    === (ii) the resolver ACCEPTS a missing originating class instead of raising
        exit 1 | 2 failed, 389 passed, 3 skipped
        PRIMARY CHECKOUT git status --porcelain: ''
        RED (2):
          TestTheRepairRuleIsExecutable::test_it_raises_when_no_originating_class_is_supplied
          TestTheRepairRuleIsExecutable::test_the_seam_raises_too_rather_than_guessing_a_tier
        REVERTED: 391 passed, 3 skipped, exit 0

    === (iii) one entry DROPPED from the call-site inventory constant
        exit 1 | 3 failed, 388 passed, 3 skipped
        PRIMARY CHECKOUT git status --porcelain: ''
        RED (3):
          TestTheCallSiteInventoryIsChecked::test_only_two_of_the_seven_call_sites_pass_a_role_literal
          TestTheCallSiteInventoryIsChecked::test_the_sweep_and_the_inventory_hold_the_same_number_of_calls
          TestTheCallSiteInventoryIsChecked::test_the_swept_multiset_equals_the_declared_inventory
        REVERTED: 391 passed, 3 skipped, exit 0

    === (iv) the orchestrator role pointed at a CHEAP-tier class
        exit 1 | 5 failed, 386 passed, 3 skipped
        PRIMARY CHECKOUT git status --porcelain: ''
        RED (5):
          TestTheOrchestratorRoleRoutesToTheTopTier::test_an_override_demoting_that_class_is_refused_with_the_rule_named
          TestTheOrchestratorRoleRoutesToTheTopTier::test_its_class_is_one_the_hard_rule_speaks_about
          TestTheOrchestratorRoleRoutesToTheTopTier::test_the_hard_rule_refuses_that_same_class_below_the_top_tier
          TestTheOrchestratorRoleRoutesToTheTopTier::test_the_seam_routes_it_to_the_top_tier
          TestTheSeamReturnsTheRoutedCallEvidence::test_the_golden_orchestrator_call_is_exactly_this_mapping
        REVERTED: 391 passed, 3 skipped, exit 0

THE DISCRIMINATOR, AS A PROPERTY. No mutation reddens nothing, so no proof
failed. **The four red sets are pairwise DISJOINT — not one test id appears
under two mutations** — so each mutation reddens the cases written for its own
behaviour and no other mutation's dedicated fixtures. Specifically:

* (iii) reddens THREE ids and every one of them is in
  `TestTheCallSiteInventoryIsChecked`. Nothing outside the inventory goes red,
  which is the proof the sweep compares against the constant instead of
  re-deriving it: a sweep that re-derived the list would agree with itself and
  stay green.
* (i) reddens the `[architecture]` parameter of both parametrised inheritance
  cases and NOT the `[format]` parameter — because the fixed class the mutation
  returns IS `format`. That is exactly why SPEC (h) demanded two originating
  classes with DIFFERENT tiers: one of them can always be the value a constant
  happens to return, and the other cannot.
* (i)'s fourth id, `test_a_promoted_class_carries_the_run_that_promoted_it`, is
  an INHERITING-role seam case (it routes `repair` with `vision` as the
  originating class), so it belongs to (i)'s own behaviour and to no other
  mutation's fixtures.
* (iv)'s fifth id is the seam GOLDEN, whose exact dict names the orchestrator's
  class — again (iv)'s own behaviour.

`git status --porcelain` was read on the PRIMARY checkout immediately after
EVERY mutation, in the same step, and was EMPTY every time. Every revert was a
`git checkout -- <path>` INSIDE the worktree — the file restored from its
commit, never re-edited back — and every revert returned the worktree to 391
passed, 3 skipped. The worktree was then removed by its exact path and pruned.

**G7 THE SUITES**, each its own invocation, run serially, all exit 0.

    $ python3 -m pytest tests/orchestration/test_model_routing.py -q
    391 passed, 3 skipped in 2.68s
    $ python3 -m pytest tests/orchestration/test_orchestrator_model_routing.py tests/orchestration/test_job_role_routing.py -q
    33 passed in 0.32s
    $ python3 -m pytest tests/orchestration/test_role_config.py -q
    34 passed in 0.23s
    $ python3 -m pytest tests/orchestration/test_config.py -q
    63 passed in 0.28s
    $ python3 -m pytest tests/docs/ -q
    295 passed in 0.44s
    $ python3 -m pytest tests/cli/test_golden_path.py -q
    42 passed in 20.67s

The routing file GREW from 325 to 391 and the skip count did NOT rise (3 → 3).
The other five are UNMOVED at 33, 34, 63, 295 and 42. `test_role_config.py`
holding at 34 is constraint 6 measured: this round READS `KNOWN_ROLES` from a
new test while `model_routing.py` imports neither `role_config.py` nor
`config.py`.

**G8 THE TREE, THE COMMITS AND THE SWEEP.**

    $ git status --porcelain          (immediately before C5 was staged)
    (no output)
    $ git ls-files .remedy-wt
    (no output)
    $ git worktree list
    /home/decodeux/Repos/remedy                                  f7765ec0 [feature/f110-model-routing-by-task-class]
    /home/decodeux/Repos/remedy/.remedy-wt/job-48a379ab5ca44ec5  f0e6b9a3 [remedy/job-48a379ab5ca44ec5]
    /home/decodeux/Repos/remedy/.remedy-wt/job-5e91e080219342d9  9fdb3b4b [remedy/job-5e91e080219342d9]
    /home/decodeux/Repos/remedy/.remedy-wt/job-7d1c93e2dc98415a  f0e6b9a3 [remedy/job-7d1c93e2dc98415a]
    /home/decodeux/Repos/remedy/.remedy-wt/job-98e9364a83a34872  21a45836 [remedy/job-98e9364a83a34872]
    /home/decodeux/Repos/remedy/.remedy-wt/job-f76686b8435640e9  4b49af98 [remedy/job-f76686b8435640e9]

Only the five PRE-EXISTING `job-*` worktrees survive; none is of this round's
making and none was touched. The worktree this round created is gone.

    $ git diff --stat 4cfcb464..f7765ec0 -- docs/
    (no output — NOTHING)
    $ git diff --stat 4cfcb464..f7765ec0 -- packages/ apps/ ':(exclude)packages/orchestration/model_routing.py'
    (no output — NOTHING)

That second command is CONSTRAINT 6 MEASURED rather than asserted: no file under
`packages/` or `apps/` other than `model_routing.py` was written.

PER-COMMIT INSERTION COUNTS, the `+` column only, CELL BY CELL against the
Commits table above:

| Commit | `git show --numstat` `+` | Commits table | Match |
|---|---|---|---|
| `50adb6a8` | 399 | 399 | yes |
| `e54c81fc` | 305 | 305 | yes |
| `4b476fb7` | 16 | 16 | yes |
| `34a77f33` | 49 + 3 + 3 = 55 | 49 + 3 + 3 = 55 | yes |
| `f342e3e7` | 253 | 253 | yes |
| `f7765ec0` | 370 | 370 | yes |

C5's own numbers appear in neither a round report nor this file.

THE STALENESS SWEEP, one entry per touched file:

| File | Stale? | Why |
|---|---|---|
| `.agent/authored/f110-r8.md` | NOT stale | new; it IS the round's authored record and is never edited |
| `.agent/last_block.md` | NOT stale | byte-identical mirror of the file above, same digest |
| `.agent/plan.md` | NOT stale | rewritten to PLAN8: names round 8, T001, and the wiring round as next |
| `.agent/live_review.md` | NOT stale | append-only; the new entry is round 7's verdict, written by round 8 as the rules require |
| `.agent/prose_slips.md` | NOT stale | append-only; SLIPS8 is dated 2026-09-03 and scoped to R7 |
| `.agent/decisions.md` | NOT stale | append-only; DECISION F110 D3 is the decision C3's map implements, and its CONSEQUENCE paragraph's promise of a deliberate-absence note is now true on disk |
| `packages/orchestration/model_routing.py` | NOT stale | the two sentences this round falsified were repaired IN C3 (constraint 9), and the Public API list gained all ten new names |
| `tests/orchestration/test_model_routing.py` | NOT stale | its docstring said "four rounds" and named four task ids; repaired in C4 to five, naming T001 |
| `.agent/handoff.md` | NOT stale | this rewrite |

## Authored-text proofs

| Slice | Applied to | Proof |
|---|---|---|
| PLAN8 | `.agent/plan.md` | `cmp` against the extraction from the COMMITTED authored file — exit 0 |
| RECORD7 | `.agent/live_review.md` | 2177227 + 2 + 7937 = 2185166 = real size; base an exact byte prefix; second reader in order; negative control rejected |
| SLIPS8 | `.agent/prose_slips.md` | final bytes == base + 2 newlines + SLIPS8, exact byte equality; base an exact prefix |
| DECISION3 | `.agent/decisions.md` | 728132 + 1 + 3014 + 1 = 731148 = real size; base an exact prefix; exactly one trailing newline; second reader in order over 8 paragraphs; negative control rejected |

Every slice was extracted BY DELIMITER INDEX from the COMMITTED
`.agent/authored/f110-r8.md` with a Python script (marker lines excluded), never
retyped. The extractor first asserted that
`git show HEAD:.agent/authored/f110-r8.md` equals the file on disk — that check
returned True at 33816 bytes, so the slices provably came from the committed
bytes.

## Deviations & assumptions

**D1 — THE BLOCK'S STATED BASE SIZE FOR `.agent/prose_slips.md` IS WRONG, AND I
APPLIED THE SLICE AS WRITTEN RATHER THAN REPAIRING ANYTHING.** Constraint 4
states the file is 53575 bytes at `4cfcb464`. Measured on disk at `4cfcb464` it
is **54853** bytes — a difference of 1278. The newline CONVENTION the constraint
states is correct (no trailing newline, two-byte append), and that is what the
append used, so the on-disk result is right under either figure; only the
reviewer's numeral is wrong. It gates nothing, because G4 gives this file a
byte-equality check rather than arithmetic. A reviewer-prose inaccuracy that left
nothing wrong on disk — amend0827-process-diet rule 2 territory, not an R-id.

**D2 — THREE NAMES THE SPEC IMPLIES BUT DOES NOT NAME.** SPEC (c) and (e)
describe behaviour that needs vocabulary the block does not supply, so I minted
it rather than departing silently:

* `UNDECLARED_ROLE_TASK_CLASS = "undeclared_role"` — SPEC (c)'s "answers
  conservatively" needs a VALUE. It is deliberately NOT a key of
  `TASK_CLASS_TIERS`, so it flows through the EXISTING resolver to `TOP_TIER`
  with `UNKNOWN_CLASS_REASON` rather than through a second, rival conservative
  path. That is also what DECISION F110 D3 says the reason token is FOR.
* `OriginatingTaskClassRequired` — SPEC (c) says the inheriting role "RAISES";
  a named exception carrying `.role` lets a caller branch on structure, which is
  the discipline `OverrideRefused` already set in this module.
* `ROLE_CONFIG_RESOLVER_NAME = "resolve_role_config"` — SPEC (e)'s inventory is
  meaningless without naming WHAT was swept for, and the test's sweep reads this
  constant instead of retyping the function name, so a rename moves both
  together. All three are in the Public API list.

**D3 — THE TEST FILE'S MODULE DOCSTRING WAS EDITED; NO TEST WAS.** Constraint 8
forbids editing an existing test. The 4 deleted lines in C4 are all in the
FILE'S module docstring, which said "The four rounds this file covers" and named
four task ids — a sentence this round's own commit falsifies, so constraint 9
required repairing it in that commit. Every existing test FUNCTION, class and
fixture is untouched; the only other change to existing lines is INSERTIONS into
the import block. No test was renamed, deleted or skipped, and the skip count is
unmoved at 3.

**D4 — `route_role_call`'s ARGUMENT ORDER.** SPEC (d) lists the arguments as
role, then the originating class, then the effective table, then the evidence
map, and that is the signature shipped:
`route_role_call(role, originating_task_class=None, effective_tiers=None, promotion_evidence=None)`.
`effective_tiers` DEFAULTS to `TASK_CLASS_TIERS`, which the spec's word
"optional" allows and which lets a call site with no project overrides route
without building a table first. Declared because the round-7 evidence function it
delegates to takes the table SECOND and positionally, so the two orders differ on
purpose and a reader comparing them should know it is deliberate.

**D5 — RUFF WAS NOT RUN, BY ORDER AND BY PERMISSION.** Constraint 5 orders no
ruff gate and forbids adding one; the reviewer lints. Independently, this
worker's permission layer refuses the tool, so no reading of it is offered here.
This is a DECLARED REFUSAL, not a skipped gate.

**D6 — NO COMMIT WAS SPLIT AND NO COMMIT WAS ADDED OR REORDERED.** The block
pre-authorises splitting C4 as round 7 did; C4 came in at 370 insertions, under
the AGENTS.md cap, so it was NOT split. The commit sequence is exactly C0a, C0b,
C1, C2, C3, C4, C5.

**D7 — ONE SCRATCH DIRECTORY OUTSIDE THE CHANGE SET, GITIGNORED AND REMOVED.**
Slice extraction and the red-proof driver needed files on disk.
`/home/decodeux/Repos/remedy/remedy-review-r8-scratch/` was used; it matches the
`remedy-review-*` entry of `.gitignore`, never appeared in `git status
--porcelain`, and was removed by its exact path. `.remedy-wt/` was never read,
listed, copied from or named in any command.

**ASSUMPTION** — SPEC (a) invited improvement on the reviewer's reading of each
role but forbade a silent departure. NO ROLE WAS RE-READ: all eight map exactly
as the block states, `orchestrator` to `mission` per DECISION F110 D3.

**A SENTENCE OUTSIDE THE CHANGE SET THIS ROUND MAKES STALE — DECLARED, NOT
REPAIRED.** `docs/roadmap/features/T3_F110.md` line 44 states T001 as
"call-site/role inventory + the single resolver seam + class declarations on all
call sites". The first two clauses are now shipped; the third is NOT — no call
site declares anything yet, by constraint 6. The line is therefore only PARTLY
discharged rather than false, and the plan's Next Steps already names the wiring
round that discharges the rest. No doc was edited this round.

## Next

**THE WIRING ROUND**: the seven existing call sites `ROLE_CONFIG_CALL_SITES`
names route through `route_role_call`, and the override map and the evidence map
are READ from configuration instead of being passed in. That is the third clause
of T001 plus consolidation order E.d, and it is the only thing standing between
this seam and a routed production call.

THE BRANCH HAS NO OPEN PULL REQUEST — none was created this round and none
existed before it — so the next session's Open PR Gate finds none and proceeds
straight to Phase 1 rule 1 (`.agent/STOP`, absent at this handback) and then to
claiming the next round on this branch.


## Reviewer verdict — ROUND 8: PASS

Appended by the planner/reviewer after the handback was written, per
docs/agents/planner_reviewer_prompt.md §3 item 14 and operator amendment
amend0827-process-diet rule 1. It is booked into `.agent/live_review.md` as
`Gate: F110 R8` in the FIRST commit of the next session's first round, together
with the prose slip named below. THIS SESSION — SESSION 2 of F110 — ENDS HERE,
after three delegated rounds, and the reason is stated below rather than assumed.

WHAT THE REVIEWER RE-DERIVED RATHER THAN READ. The transport proof again reached
the EMITTED bytes: the reviewer's scratch original, written before delegation and
untouched since, the committed `.agent/authored/f110-r8.md` at `50adb6a8`, its
mirror at `e54c81fc`, and both working copies at `6d6988e7` are five artefacts
carrying one digest,
`11b0c5855d8a82ee04728791ef426d8c5473ae15ca13025441c0cc35828eee5e`, at 33816
bytes each. The block is 399 lines against a projection of 399 — the fifth exact
projection in a row — and under the cap of 400, which it reached only after the
reviewer cut it from 415. Every slice is byte-exact: `.agent/plan.md` equals
PLAN8 plus the one trailing newline the target's convention adds, at 44 lines;
`.agent/live_review.md` is 2177227 + 2 + 7937 = 2185166, the real size, still
ending without a newline, base preserved as an exact prefix, second reader in
order, negative control on the FIRST appended paragraph rejected;
`.agent/decisions.md` is 728132 + 1 + 3014 + 1 = 731148, the real size, ending
with exactly one newline, its eight paragraphs in order under the target's own
convention; `.agent/prose_slips.md` equals its base plus two newlines plus
SLIPS8. `ruff check` over both changed files answers "All checks passed!", run
reviewer-side because the worker's permission layer refuses the tool — declared,
not invented.

DEVIATION D1 IS CORRECT AND THE BLOCK WAS WRONG. Constraint 4 gave
`.agent/prose_slips.md` as 53575 bytes; the real size at `4cfcb464` is 54853, and
the reviewer confirms the arithmetic the worker could not have known to check:
53495 at `c1a3a3c4`, plus two newlines, plus SLIPS7's 1356 bytes, is 54853
exactly. The stated newline CONVENTION was right and G4 gated that file by byte
equality rather than by arithmetic, so nothing on disk is wrong and the append is
exact. The worker applied the constraint as written and declared the discrepancy,
which is precisely what constraint 1 asks for. Recorded in
`.agent/prose_slips.md` next round; no R-id, per amend0827-process-diet rule 2.

THE DELETIONS WERE READ LINE BY LINE. C3 is 253 insertions against 6 deletions,
all six in the module docstring — no constant, no signature and no behaviour of
rounds 4 through 7 revised. C4 is 370 against 4, all four the TEST module's
docstring, which said "four rounds" and named four task ids and was falsified by
this round's own commit; repairing it there is constraint 9, and deviation D3
declares it. No existing test function was edited, renamed, deleted or skipped,
which is constraint 8 met exactly.

EVERY SHIPPED FUNCTION WAS RUN BY THE REVIEWER, NOT READ. The role map declares
eight roles and every declared class is a seed-table key; `repair` is the sole
inheriting role; the two sets are disjoint and together cover
`role_config.KNOWN_ROLES` exactly, with no role left over in either direction.
THE REPAIR RULE IS EXECUTABLE AND DISCRIMINATES: the inheriting role answers
`architecture` for an `architecture` origin and `format` for a `format` one —
different classes at different tiers, so inheritance is proven rather than a
constant — and it raises `OriginatingTaskClassRequired` when no origin is given.
A declared role IGNORES an originating class rather than being overridden by it.
The undeclared role warns and answers `undeclared_role`, which the seam then
routes to the top tier with the reason `unknown_class_conservative` — the A9
default, and the honest reason in exactly the case where nobody did declare.
The seam answers `mission` at the top tier for the orchestrator role and routes
the inheriting role to its origin's tier, and round 5's hard rule refuses that
same class below top, so DECISION F110 D3's whole point is a test rather than a
claim.

THE INVENTORY IS THE ROUND'S REAL DELIVERABLE AND THE REVIEWER RE-SWEPT IT
INDEPENDENTLY. An AST walk of the reviewer's own over `packages/` and `apps/`
finds seven calls to `resolve_role_config`, and the multiset of (path, role) pairs
it produces equals `ROLE_CONFIG_CALL_SITES` entry for entry: `artifact_summary.py`
with the literal `summary`, `role_config.py` with the literal `orchestrator`, and
`do_cmd.py`, `pingpong_job.py`, `self_use_runner.py` and `teacher_model.py` twice
carrying the dynamic marker. Five of the seven pass the role as a variable, so a
sweep keyed on literal roles would have reached two — which is why the inventory
pins the call SITES.

THE RED PROOF WAS RE-RUN IN FULL, in a disposable worktree at `f7765ec0`, module
path printed from inside it, `git status --porcelain` read on the PRIMARY
checkout immediately after every mutation and CLEAN every time. Control: 391
passed, 3 skipped, exit 0. The four mutations redden 5, 2, 3 and 5 ids and THE
FOUR RED SETS ARE PAIRWISE DISJOINT — the cleanest discrimination this feature
has produced. Mutation (iii), dropping one inventory entry, reddens exactly three
ids and every one of them is an inventory test, which is the proof the sweep
compares against the constant instead of re-deriving it. One benign difference
from the handback: the reviewer's mutation (i) reddens five where the worker
reported four, because the two runs substituted different fixed classes for the
inherited one; the property under proof is identical and holds in both.

THE SUITES WERE RE-RUN BY THE REVIEWER at 391 passed with 3 skipped for the
routing file — grown from 325, with the skip count unmoved — then 33, 34, 63,
295 and 42, every one exit 0. The three skips remain round 5's own
"covered by the violating fixture above". CONSTRAINT 6 WAS MEASURED, NOT
ASSERTED: `git diff --name-only 4cfcb464..f7765ec0 -- packages/ apps/` lists
`packages/orchestration/model_routing.py` and nothing else, the module imports
neither `config.py` nor `role_config.py`, and `git diff --stat` over `docs/` is
empty. The per-commit insertion counts match the handback's Commits table cell by
cell — 399, 305, 16, 55, 253, 370 — and every one is under the AGENTS.md cap;
`6d6988e7` is 463 insertions against 578 deletions, a full-file rewrite of a
single `.agent/**` state file and exempt under DECISION F104 D1. The open set is
278 over 347 registered and 69 resolved, UNCHANGED; the round minted no id and
`R-0767` stays OPEN. The tree is clean, `git ls-files .remedy-wt` returns
nothing, no worktree of the round's making survives, `.agent/candidates.md` is
untouched and still EMPTY, and the branch is pushed at `6d6988e7` with no pull
request open.

WHY THIS SESSION ENDS AFTER THREE DELEGATED ROUNDS, STATED RATHER THAN ASSUMED.
Operator amendment amend0827-process-diet rule 6 sets the default at four to five
rounds and forbids stopping "at a nice seam", so the reason is named here and G7
is NOT cited for it. The next round is the WIRING round, and its first act is a
DECISION the reviewer is not yet entitled to take: WHERE F110's routed-call
evidence lands. Two facts make that a real question rather than a formality.
FIRST, the seam returns a TIER, and this feature deliberately refuses to map a
tier to a model id — so wiring cannot yet change model SELECTION, only recording,
and whether it ever should is itself undecided. SECOND, the obvious field name is
already taken: `model_routing_tier` and `model_routing_plan.tier` belong to
`orchestrator_brain.py`'s UNRELATED vocabulary and surface in the ledger, the
review bundle at `review_bundle.py`, the UI server at `ui_server.py` and the CLI —
the collision `model_routing.py`'s own docstring was written to warn about. Ruling
on a sink across four surfaces the reviewer has not measured would be a guess, and
guardrail G8 forbids guessing. Measuring them is a session's opening work, not its
closing work.

WHAT THE NEXT SESSION OWES, IN ORDER. Phase 1 rule 1 first — read `.agent/STOP`
from disk — then rule 2, the Open PR Gate, which finds NO open pull request
because this branch has deliberately created none. Its first round then books
`Gate: F110 R8` into `.agent/live_review.md` and the prose-slip line above into
`.agent/prose_slips.md` as its first commit. Before authoring the wiring round it
reads `packages/orchestration/progress_ledger.py`, `review_bundle.py`,
`ui_server.py` and the CLI surface that carries `model_routing_tier`, and records
the sink ruling as DECISION F110 D4 with its rejected alternatives. `R-0767`
remains OPEN on this same seam and must not be absorbed into a routing commit.

THREE SMALLER THINGS THE NEXT REVIEWER SHOULD NOT REDISCOVER. A block's line
count must be measured on the FINAL bytes AFTER the last edit — round 8's ran to
415 and needed real cuts, not rewraps, because rewrapping a paragraph leaves the
line count where it was. A pre-emission probe must exercise the BEHAVIOUR the
round ships and not merely the SHAPE of the constant that names it; round 7's
three wrong clauses all came from that one shortcut. And a byte figure quoted for
one round's base must be RE-MEASURED at the next round's base rather than
re-derived by arithmetic in the reviewer's head, which is how constraint 4 came to
say 53575 where the file held 54853.
