# Handoff — F034 Bundled clarification in the Flight Plan (round 1)

Branch: feature/f034-bundled-clarification
Review range: 34878f3..3a8652f (5 commits; 34878f3 = main after PR #150 merge)
Open findings: 0. Next expected action: reviewer round 1.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| Setup (PR gate, branch, claim) | done | PR #150 merged, branch cut from main |
| T001 decision payload + answer parsing | done | |
| T002 write-back + immutability | done | |
| T003 assumptions.md + CLI + plan link | done | |
| T004 guard test + unattended e2e | done | |
| Conditional-answer predicates | skipped | OPTIONAL scope, not trivially cheap; see .agent/decisions.md |

## Commits (ordered, changed files with +/-)

### 4648d69 chore(f034): claim F034, reset live review and plan
| File | + | - |
|------|---|---|
| .agent/live_review.md | 8 | 55 |
| .agent/plan.md | 25 | 23 |
| docs/roadmap/STATUS.md | 1 | 1 |

### f5aef15 feat(f034): bundle intake clarifications into the plan approval decision
| File | + | - |
|------|---|---|
| .agent/plan.md | 5 | 6 |
| apps/cli/command_catalog.py | 8 | 0 |
| apps/cli/commands/decision.py | 76 | 1 |
| apps/cli/grouped.py | 6 | 0 |
| packages/orchestration/decision_queue.py | 28 | 6 |
| packages/orchestration/flight_plan.py | 103 | 2 |
| packages/orchestration/schemas/models.py | 14 | 1 |
| tests/cli/test_decision_answers.py | 163 | 0 |
| tests/orchestration/test_bundled_clarification.py | 202 | 0 |

### 2a365d7 feat(f034): write clarification answers back on approval, then freeze them
| File | + | - |
|------|---|---|
| .agent/plan.md | 4 | 5 |
| apps/cli/commands/decision.py | 23 | 7 |
| packages/orchestration/flight_plan.py | 47 | 0 |
| tests/cli/test_decision_answers.py | 96 | 0 |
| tests/orchestration/test_bundled_clarification.py | 83 | 0 |

### 01f546e feat(f034): assumption log, job assumptions command, plan.md link
| File | + | - |
|------|---|---|
| .agent/plan.md | 5 | 4 |
| apps/cli/command_catalog.py | 10 | 0 |
| apps/cli/commands/decision.py | 6 | 0 |
| apps/cli/commands/job.py | 27 | 0 |
| packages/orchestration/flight_plan.py | 87 | 1 |
| tests/cli/test_decision_answers.py | 61 | 0 |
| tests/orchestration/test_bundled_clarification.py | 86 | 0 |

### 3a8652f feat(f034): interactive-input guard, unattended end-to-end, planner prompt
| File | + | - |
|------|---|---|
| .agent/decisions.md | 32 | 0 |
| .agent/plan.md | 12 | 10 |
| apps/cli/commands/do_cmd.py | 13 | 0 |
| packages/orchestration/flight_plan.py | 21 | 2 |
| tests/cli/test_decision_answers.py | 106 | 0 |
| tests/orchestration/test_bundled_clarification.py | 35 | 0 |
| tests/test_no_interactive_guard.py | 171 | 0 |

## Verification (raw, final tree at 3a8652f)

    $ python3 -m pytest tests/orchestration/test_bundled_clarification.py tests/cli/test_decision_answers.py -q
    ...................................................................      [100%]
    67 passed in 0.73s
    exit=0

(the same command is the T001, T002 and T003 gate; it was green at each
commit with 30, 47 and 61 tests respectively as the slices landed)

    $ python3 -m pytest tests/test_no_interactive_guard.py tests/orchestration/test_bundled_clarification.py tests/cli/test_decision_answers.py -q
    .                                                                        [100%]
    73 passed in 1.71s
    exit=0

    $ python3 -m pytest tests/cli/test_golden_path.py -q          # canary
    ..........................................                               [100%]
    42 passed in 21.80s
    exit=0

## Guard-test red proof (T004, required)

Injected `def _injected_violation_for_guard_proof(): return input("which
database? ")` into packages/orchestration/decision_queue.py, then:

    $ python3 -m pytest tests/test_no_interactive_guard.py -q -p no:randomly
    E       AssertionError: Interactive input found in an unattended execution package. Remedy asks its questions once, at plan time, on the flight plan approval decision — read the resolved clarifications instead:
    E           packages/orchestration/decision_queue.py:296: builtin input()
    E       assert not ['packages/orchestration/decision_queue.py:296: builtin input()']
    1 failed, 5 passed in 1.00s
    exit=1

Injection removed (`git diff --stat packages/orchestration/decision_queue.py`
empty), same command on the real tree:

    6 passed in 0.93s
    exit=0

An earlier regex-based version of the guard was replaced: it also flagged
progress_ledger.py:1118 and token_economy.py:374, both prose ("needs user
input (e.g. ...)"). The AST version has no false positives, so the
allowlist stays empty.

## Regression evidence

- tests/cli/ full suite, branch vs base (main 34878f3), -p no:randomly:
  branch 27 failed / 1058 passed; base 27 failed / 1042 passed. 25 failures
  identical. 2 branch-only (test_runtime_cmd timeout probes) and 2 base-only
  (test_self_dogfood_execution_cli) are order/timing flakes; the 2
  branch-only pass on serial re-run (2 passed, exit 0).
- tests/orchestration/test_project_brain.py + tests/ui_contracts/
  test_graph_architecture.py: identical 7 failures on branch and base
  (missing apps/ui legacy files, unrelated).
- Green after the change: tests/cli/test_plan_approval.py +
  tests/orchestration/test_flight_plan.py -> 56 passed; tests/schemas/ and
  the decision-queue consumer suites -> no new failures.
- ruff clean on every file touched.

## Notes for the reviewer

- Exactly ONE decision per plan: the questions ride the existing
  fp:approval payload (decision_queue.py), never a decision per question.
- Schema changes are additive; a pre-F034 fp1 plan loads with id="" and
  answered_by="" and produces an empty payload (test asserts this).
- answered_by stays human|default|""; the "planner" source in the log is
  derived from an answered record with empty answered_by. Rationale in
  .agent/decisions.md.
- Zero-clarification plans take the plain-plan approval path unchanged.
