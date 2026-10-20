# Handoff — F310 round 3 (one stop, one question)

## Session

SESSION 1 of feature F310 · round 3 · rounds so far 3

Context self-assessment: the session stayed small; each file was read once before its edit, the prepared files were copied by digest-checked byte copies, and the gates ran once on the final code tree.

State block:
Feature F310 (claimed `[~]`), branch `feature/f310-provider-budgets`, base `e8924be11`.
Fortschritt: ~75 % (claim, T001, T002 and T003 part one landed · T003 part two and T004 open) — Schätzung

## Range

Review of `e8924be11`..HEAD (the five commits below, then this handback's own commit).

## Commits

### 58164d864 F310 R3 C1: book round 2 and R-1372, DECISION F310 D5, the plan
255 insertions, 14 deletions (`git show --shortstat`).
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f310-r3.md` | +225 | byte copy of the block |
| `.agent/live_review.md` | +4 | round 2 booked, R-1372 registered |
| `.agent/decisions.md` | +12 | DECISION F310 D5 |
| `.agent/plan.md` | +14/-14 | rewritten |

### d46c6cf2a F310 R3 C2: a run's saved active moment is read back (R-1372)
17 insertions.
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_budget_clock.py` | +15 | runs the nine-hour local job, reads the saved `active_until` inside the run, resumes an hour later |
| `.agent/live_review.md` | +2 | the one `Landed:` line |

### 56999a8ca F310 R3 C3: the budget branch of the decision answer becomes a function of its own (structure step)
92 insertions, 81 deletions.
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/decision.py` | +85/-77 | the branch moves unchanged into `_resolve_budget_decision`; the branch is one call |
| `tests/cli/test_client_interface.py` | +3/-2 | the answer-tree test reads the new function beside the old |
| `docs/system/structure-ledger-v1.md` | +2/-1 | the step sentence, row 428 to 352 |
| `tests/test_structure_ratchet.py` | +1/-1 | `MAX_FUNCTION_LINES` 28931 to 28855 |

### 7685c0ee2 F310 R3 C4: one stop, one question: the blockers, the doubling and the resume
171 insertions, 29 deletions.
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/budget_stop.py` | +113 | new module: blockers, doubled answers, resume after extend |
| `packages/orchestration/budget_decision.py` | +10/-9 | no answer doubles; answers compared with the limits the run read |
| `packages/orchestration/decision_queue.py` | +4/-5 | the budget decision carries `blockers` |
| `packages/orchestration/api_clients.py` | +16/-1 | `job` keyword; doubled values judged against ceilings |
| `packages/orchestration/public_api.py` | +5/-6 | job passed to the ceiling check; resume after an extended answer |
| `packages/orchestration/public_api_routes.py` | +2/-1 | route description, last sentence |
| `docs/system/public-http-api-v1.md` | +1/-1 | regenerated page |
| `docs/system/job-budget-enforcement-v0.md` | +13 | the one-question section |
| `docs/system/structure-ledger-v1.md`, `tests/test_structure_ratchet.py` | rows and pins | see Verification |
| `tests/orchestration/import_reachability_allowlist.txt` | +1 | new module listed |

### da1f52141 F310 R3 C5: one stop, one question, tested
248 insertions, 1 deletion.
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_budget_stop.py` | +247 | new file, 21 tests |
| `tests/orchestration/test_decision_evidence.py` | +1/-1 | the payload pin gains `"blockers": []` |

### this handback's commit (C6)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file |

## External actions

- `git push origin feature/f310-provider-budgets` after C6; the result is in the worker's report.
- No pull request opened; no other gh command.

## Verification

All gates ran once, on the tree at `da1f52141`, before this commit.
1. `git status --porcelain` printed nothing. `python3 .remedy-wt/f310-r3/prep/verify.py .`: every
   line `True`, C6 `absent`, last line `ALL True`.
2. `python3 -m ruff check` over the 12 Python files of C2 to C5: `All checks passed!`
3. `run_selection.py`: `paths 110`, `exit 0`, `5359 passed, 2 skipped in 61.89s`; no FAILED, ERROR or
   "process(es) behind" line (count 0). SKIPPED: `tests/test_agent_tooling.py:43` (D12 quarantine,
   F252) and `tests/test_install_smoke.py:175` (opt-in install smoke).
4. `python3 -m apps.cli.main integrity check --json`: exit 1, `fail_count` 1, the one failing check
   `high_blockers_open` naming R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349,
   R-1359, R-1360, R-1361, R-1362 and R-1369 (thirteen, as at the base).
5. `open_finding_ids` of `scripts/rotate_live_review.py` over the ledger: `88`.

Structure ratchet rows lowered: `_cmd_decision_resolve` 428 to 352 (C3); `list_decisions` 888 to 887,
`answer_public_api_post` 158 to 157, `answer_budget_decision` 156 to 155, `decision_queue.py` 1183 to
1182 (C4); `MAX_FUNCTION_LINES` 28931 to 28855 (C3) to 28852 (C4); `MAX_FILE_LINES` 64267 to 64266
(C4). No row rose, none was added.

Exception classes the new handlers catch: `ContractError` (blockers); `ValueError` (reading the
limits) and `BudgetCounterError` (decoding the saved actuals) in the doubling; `JobIdError`,
`RunRefused` and `OSError` in the resume; `JobIdError` in the client ceiling check.

Generated pages regenerated: `docs/system/public-http-api-v1.md` (the route description). The
client interface page was regenerated too and did not change.

## Authored-text proofs

Byte copies, sha256 equal to the source (checked by script before the write and by `verify.py` after):
block (`fcf092e5…3548`, 225 lines), the three prepared state files, and the one-question section of
`docs/system/job-budget-enforcement-v0.md` (`src-doc.md`, inserted before the cost section).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | this commit |
| Gate 1 | done | |
| Gate 2 | done | |
| Gate 3 | done | |
| Gate 4 | done | fail_count 1, the standing thirteen |
| Gate 5 | done | 88 |

## Deviations & assumptions

- C4 added one line to `tests/orchestration/import_reachability_allowlist.txt`; the reachability test asked for it and `verify.py` lists it for C4.
- C4 left one existing test red until C5, as the block orders: `tests/orchestration/test_decision_evidence.py::test_the_budget_stop_states_its_options_where_the_gate_reads_them`
  pinned the payload as exactly the two options; C5 changed it to include `"blockers": []`. I read
  this as the block's (3) category (the payload line of section 4). No other existing test changed besides the C3 pair named in the commit table.
- `client_budget_answer_refusal` takes `job` as a keyword-only parameter (`*, job=None`), because the block says "a keyword".
- The docstring of `answer_budget_decision` had one word group changed in place ("an answer is given or doubled for it") so it no longer states the old refusal; no line added.
- No mutation red-proof was run, as ordered.

## For the operator

When a budget stops a job, the person now answers one question. The question lists the open
blocking criteria of the job's mission, so what is still missing is in front of them when they
choose. Answering extend without any numbers now doubles every limit the stop used up, and the time
limit at least to an hour, so a client no longer has to work out new numbers. A number that is
given still holds, but no number can lower a limit below the one the run actually read, which closes
a way to shrink a profile's limit by accident. A client with ceilings is judged on the doubled
values. Over the web interface the job starts again by itself as soon as the extension is
accepted, and the answer says which run it started or why it could not.

## Next

In order: Phase 1 rule 1 (`.agent/STOP`), then rule 2 (Open PR Gate), then book round 3's verdict
in the next round's first commit, then T003 part two and T004, under DECISION F310 D6.
Operator questions open: 1. Open findings: 88 (gate 5, `open_finding_ids`, read at `da1f52141`).
