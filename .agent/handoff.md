# Handoff — F310 round 1 (budgets per provider class)

## Session

SESSION 1 of feature F310 · round 1 · rounds so far 1

Context self-assessment: the worker ran on a long, interrupted session with four stops and three
reviewer rulings; the working context stayed small because every file was read once and the gates
were run once on the final tree.

State block:
Feature F310 (claimed `[~]`), branch `feature/f310-provider-budgets`, base `ee53c20b3`.
Fortschritt: ~30 % (claim and T001 landed · T002, T003 and T004 open) — Schätzung

## Range

Review of `ee53c20b3`..HEAD (the four commits below, then this handback's own commit).

## Commits

### 5fa8aa1d3 F310 R1 C1: claim F310, re-head the ledger, DECISIONs F310 D1 to D3
347 insertions, 38 deletions (`git show --shortstat`).
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f310-r1.md` | +255 | byte copy of the corrected block |
| `docs/roadmap/STATUS.md` | +1/-1 | F310 claimed |
| `.agent/live_review.md` | +17/-18 | re-headed |
| `.agent/decisions.md` | +38 | DECISIONs F310 D1 to D3 |
| `.agent/plan.md`, `.agent/context.md` | +21/-10, +15/-9 | state |

### b5c78226c F310 R1 C2: the registry's budget keys move to config_keys_budget.py (structure step)
122 insertions, 104 deletions.
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/config_keys_budget.py` | +116 | the budget group, moved unchanged |
| `packages/orchestration/config.py` | +2/-102 | splice and import |
| `docs/system/structure-ledger-v1.md` | +2/-1 | row 1695 to 1595, step (6) named |
| `tests/test_structure_ratchet.py` | +1/-1 | `MAX_FILE_LINES` 64375 to 64275 |
| `tests/orchestration/import_reachability_allowlist.txt` | +1 | new module listed |

### e18b07d09 F310 R1 C3: budgets per provider class, read by run_job and named by the execution offer
278 insertions, 73 deletions.
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/budget_profiles.py` | +103 | provider class, profiles, `effective_job_budgets` |
| `packages/orchestration/config_keys_budget.py` | +71 | seven profile keys |
| `packages/orchestration/pingpong_job.py` | +10/-11 | `run_job` reads its limits through the profiles |
| `packages/orchestration/do_sequence.py`, `job_plan.py` | -1 net, -21 | plan budgets no longer limits; `apply_plan_budgets` deleted |
| `packages/orchestration/execution_options.py`, `apps/cli/client_interface_execution.py` | small | `class` per provider, `profiles` under `budgets` |
| `docs/guides/environment.md`, `docs/system/machine-client-contract-v1.md` | regenerated | new keys and offer |
| `docs/system/job-budget-enforcement-v0.md` | +38 | profiles section, precedence sentence |
| `docs/system/structure-ledger-v1.md`, `tests/test_structure_ratchet.py` | rows and pins | see Verification |
| `tests/orchestration/test_job_plan.py` | -23 | `TestBudgetPrecedence` deleted |
| `tests/cli/test_plan_approval.py` | +6/-3 | amendment 1: one test renamed, asserts the reverse |
| `tests/orchestration/import_reachability_allowlist.txt` | +1 | `budget_profiles` listed |
| `.agent/authored/f310-r1-amend1.md` | +19 | byte copy of amendment 1 |

### 4b74287bd F310 R1 C4: the provider class, the profiles and the offer, tested
229 insertions.
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_budget_profiles.py` | +210 | 28 tests |
| `tests/orchestration/test_execution_options.py` | +19 | profiles and class in the offer |

### this handback's commit (C5)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file |
| `.agent/operator_questions.md` | +1 entry | Q19 replaces the EMPTY line |

## External actions

- `git push -u origin feature/f310-provider-budgets` after C5; the result is in the worker's report.
- No pull request opened; no other gh command.

## Verification

All gates ran once, on the tree at `4b74287bd`, before this commit.
1. `git status --porcelain` printed nothing. `verify.py` (sha256 `f892fbc2…d62f`, 133 lines): every
   line `True`, C5 `absent`, last line `ALL True`.
2. `python3 -m ruff check` over the 13 Python files of C2 to C4: `All checks passed!`
3. `run_selection.py`: `paths 107`, `exit 0`, `4878 passed, 2 skipped in 58.49s`; no FAILED, ERROR or
   "process(es) behind" line. SKIPPED: `tests/test_install_smoke.py:175` (opt-in install smoke) and
   `tests/test_agent_tooling.py:43` (D12 quarantine, F252).
4. `python3 -m apps.cli.main integrity check --json`: exit 1, `fail_count` 1. Accepted reading
   (reviewer ruling): the one failing check is `high_blockers_open`, naming exactly R-1335, R-1336,
   R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362 and R-1369; the
   other five checks pass. It is the ledger's standing state, identical at the base.
5. `open_finding_ids` of `scripts/rotate_live_review.py` over the ledger: `87`, read at `4b74287bd`.
6. `python3 -m apps.cli.main client execution --json`: exit 0. `budgets.profiles` =
   `{"local": {"max_provider_calls": 200, "max_total_tokens": 1500000, "max_wall_clock_minutes": 480},
   "paid": {"max_cost_usd": null, "max_provider_calls": null, "max_total_tokens": null,
   "max_wall_clock_minutes": null}}`. Builder classes: pi local, claude paid, claude-cli paid, fake paid.

Structure ratchet rows lowered: `config.py` 1695 to 1595; `run_job` 1442 to 1441; `plan_order_job`
250 to 249; `pingpong_job.py` 5339 to 5338; `MAX_FILE_LINES` 64375 to 64274 (C2: 64275, C3: 64274);
`MAX_FUNCTION_LINES` 28964 to 28962. No row rose, none was added.

## Authored-text proofs

Byte copies, sha256 equal to the source in `.remedy-wt/f310-r1/prep/`: block (corrected,
`dbad0091…bbb3`, 255 lines), the five prepared state files, amendment 1 (`3ec3b3dd…0261`, 19
lines), the profiles section of `docs/system/job-budget-enforcement-v0.md` (checked by `verify.py`),
and the operator question (checked by `verify.py` after this commit).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 branch | done | |
| C1 | done | after the first refusal (stop 1) |
| C2 | done | |
| C3 | done | after stop 2 and amendment 1 |
| C4 | done | |
| C5 | done | this commit |
| Gate 1 | done | |
| Gate 2 | done | |
| Gate 3 | done | |
| Gate 4 | deviated | exit 1, `fail_count` 1; accepted reading above |
| Gate 5 | done | 87 |
| Gate 6 | done | |

## Deviations & assumptions

- Stop 1, reviewer's block defect: the block carried machine-local paths that the agent-state check
  refused in the authored copy. The reviewer corrected the block; C1 was committed from the
  corrected copy.
- Stop 2: an existing test pinned the behaviour DECISION F310 D2 removes (a plan's suggested
  budgets filling a limit). Amendment 1 added the test file and a copy of itself to C3; the test
  is renamed and asserts the reverse.
- Stop 3, reviewer's `verify.py` defect: the check wanted the wrapped precedence sentence on one
  line. The reviewer changed `verify.py`; the wrapped text stays and there is no fix commit.
- Stop 4, reviewer's block defect: gate 4 ordered `fail_count` 0, which the base already
  contradicts. Accepted as stated in Verification; gates were not re-run.
- C2's ledger bullet has one unwrapped line; accepted by the reviewer, C2 not amended.
- Existing tests changed: `TestBudgetPrecedence` deleted (ordered), the renamed plan-approval test,
  the ratchet pins, the reachability allowlist.

## For the operator

Remedy now gives every job a default limit that depends on where its models run. A job that uses
only models served on this machine gets eight hours, two hundred provider calls and one and a half
million tokens; any other job gets no default limit, exactly as before. A limit that a person, an
order or a decision already set always wins, and the task plan's own suggested limits are only an
estimate and never a limit. Every client can now read both sets of defaults and the kind of each
provider. One question is open for you: whether an order's own limit should stay the ceiling.

## Next

In order: Phase 1 rule 1 (`.agent/STOP`), then rule 2 (Open PR Gate), then book round 1's verdict in
the next round's first commit, then T002, under DECISION F310 D4.
Operator questions open: 1. Open findings: 87 (gate 5, `open_finding_ids`, read at `4b74287bd`).
