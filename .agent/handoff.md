# Handoff — F310 round 4 (the remainder waits for a final stop)

## Session

SESSION 1 of feature F310 · round 4 · rounds so far 4

Context self-assessment: the session stayed small; each file was read before its edit, prepared files were copied by digest-checked byte copies, and the gates ran on the final code tree.

State block:
Feature F310 (claimed `[~]`), branch `feature/f310-provider-budgets`, base `79ed24137`.
Fortschritt: ~85 % (T001 to T004 landed · the closure sequence open) — Schätzung

## Range

Review of `79ed24137`..HEAD (the seven commits below, then this handback's own commit).

## Commits

### 26e992ed0 F310 R4 C1: book round 3, R-1372 resolved, R-1373, DECISION F310 D6, the plan
196 insertions, 15 deletions.
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f310-r4.md` | +159 | byte copy of the block |
| `.agent/live_review.md` | +6 | round 3 booked, R-1372 resolved, R-1373 registered |
| `.agent/decisions.md` | +22 | DECISION F310 D6 and continuations |
| `.agent/plan.md` | +9/-15 | rewritten |

### 3b4ba60d0 F310 R4 C2: the doubling is tested on a job that waited (R-1373)
11 insertions.
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_budget_stop.py` | +9 | the doubling on a job that waited 7,000 s |
| `.agent/live_review.md` | +2 | the one `Landed:` line |

### 6a3e024ec F310 R4 C3: the remainder decision waits for a final stop; the walk names the one question
52 insertions, 32 deletions.
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/budget_stop.py` | +35 | `budget_stop_walk_note`, `raise_remainder_for_final_job` |
| `packages/orchestration/do_sequence.py` | +6/-32 | `do_budget_stop_remainder` deleted; the walk calls the note; docstring paragraph replaced |
| `apps/cli/commands/decision.py` | +5 | an abandon raises the remainder and prints it |
| `docs/system/job-budget-enforcement-v0.md` | +6 | the remainder paragraph |

### 162be0a0e F310 R4 C3b: a cancelled job still asks its mission's remainder question (R-1374)
48 insertions, 7 deletions.
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/decision_queue.py` | +7/-7 | a cancelled job lists only its mission's remainder question; length unchanged |
| `.agent/live_review.md` | +2 | R-1374 registered |
| `.agent/decisions.md` | +4 | DECISION F310 D6 addendum |
| `.agent/authored/f310-r4-amend1.md` | +35 | byte copy of amendment 1 |

### 59a17df4a F310 R4 C4: one question at the stop, the remainder at the abandon, and the lab stop rebuilt
178 insertions, 17 deletions.
| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_do_sequence_cli.py` | +36/-17 | the stop test asks one question; the extend test raises the remainder by hand |
| `tests/orchestration/test_lab_stop_20261020.py` | +98 | new: the lab stop rebuilt, three tests |
| `tests/orchestration/test_budget_stop.py` | +44 | walk note, no-stop note, not-cancelled, cancelled-job listing |

### 2d9f1ed6a F310 R4 C4b: a program driving an order sees one question at a budget stop
32 insertions, 6 deletions.
| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_machine_client_contract.py` | +12/-6 | one decision at the stop, none of kind task decision, `closed_decisions` empty |
| `.agent/authored/f310-r4-amend2.md` | +20 | byte copy of amendment 2 |

### 3a6af6b74 F310 R4 C4c: the F295 gate test's pin follows its deliberate change
23 insertions, 1 deletion.
| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_client_interface.py` | +1/-1 | `F295_GATE_TEST_SHA256` now `dfe3d5b0f1d8…8423` |
| `.agent/decisions.md` | +4 | the DECISION text for the pin |
| `.agent/authored/f310-r4-amend3.md` | +18 | byte copy of amendment 3 |

### this handback's commit (C5)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file |

## External actions

- `git push origin feature/f310-provider-budgets` after C5; the result is in the worker's report.
- No pull request opened; no other gh command.

## Verification

1. `git status --porcelain` printed nothing. `python3 .remedy-wt/f310-r4/prep/verify.py .` (re-run at `3a6af6b74`): every line `True`, `absent` for C5, last line `ALL True`.
2. `python3 -m ruff check` over the Python files of C2 to C4b: `All checks passed!`
3. `run_selection.py` (re-run at `3a6af6b74`): `paths 98`, `exit 0`, `4592 passed, 2 skipped in 64.48s`; no FAILED, ERROR or "process(es) behind" line. SKIPPED: `tests/test_agent_tooling.py:43` (D12 quarantine, F252) and `tests/test_install_smoke.py:175` (opt-in install smoke).
4. `python3 -m apps.cli.main integrity check --json`: exit 1, `fail_count` 1, the one failing check `high_blockers_open` naming R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362 and R-1369 (thirteen, as at the base).
5. `open_finding_ids` of `scripts/rotate_live_review.py` over the ledger: `89`.

Earlier gate 3 runs: two red runs, both fixed by commits above (see Deviations). The first had `tests/cli/test_machine_client_contract.py::test_a_program_drives_an_order_file_to_its_proof_through_the_command_line` red; the second had `tests/cli/test_client_interface.py::test_f295s_gate_test_is_unchanged` red.

Structure ratchet rows lowered: none. No row rose, none was added.

Exception classes the new handlers catch: `ContractError` (in `raise_remainder_for_final_job`). No other handler was written.

Pin digest: sha256 of `tests/cli/test_machine_client_contract.py` as C4b left it, computed with a Python reader at C4c: `dfe3d5b0f1d8d720fc4a0d2ff64c6ff3eeb67b3f69f1e0d5e3e9b1af8d768423`.

## Authored-text proofs

Byte copies, sha256 equal to the source (checked by script before the write and by `verify.py` after): block (`3609ced4…`, 159 lines), the three prepared state files, the docstring paragraph and the documentation paragraph, amendment 1 (35 lines), its two appended texts, amendment 2 (20 lines), amendment 3 (18 lines) and its appended text. Amendments 2 and 3 digests checked by Python reader before the write: `1375e775…` and `c3ba791e…`.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | edited before C3, committed before it |
| C3 | done | |
| C3b | done | added by amendment 1 |
| C4 | done | |
| C4b | deviated | added by amendment 2; the blockers are read in-process (see Deviations) |
| C4c | done | added by amendment 3 |
| C5 | done | this commit |
| Gate 1 | done | |
| Gate 2 | done | |
| Gate 3 | done | third run green; two earlier runs red |
| Gate 4 | done | fail_count 1, the standing thirteen |
| Gate 5 | done | 89 |

## Deviations & assumptions

- Edit order: I made C3's edits before C2's, then committed C2 first with only its own paths; the commit order is as the block says.
- Stop 1, before C4: `list_decisions` answered an empty list for every cancelled job, so the remainder an abandon raises was hidden. The reviewer ruled amendment 1: C3b (finding R-1374), a line-neutral replacement in `list_decisions`, plus one extra test in C4.
- Stop 2, at gate 3: `tests/cli/test_machine_client_contract.py` pinned the replaced two-decision behaviour. Amendment 2 added C4b. The client digest carries no payload and reading the list through the command line added a command and keys the contract page test does not name, so C4b reads the blockers in-process with `budget_stop_blockers`, with `monkeypatch` pointing the data directory at the scratch one. The reviewer accepted this.
- Stop 3, at gate 3: `tests/cli/test_client_interface.py::test_f295s_gate_test_is_unchanged` pins the bytes of the file C4b changed. Amendment 3 added C4c.
- The extend test in C4 raises the remainder by hand, as a job stopped before this feature carries one.
- In the lab-stop test file the job's metadata names a target repository so that the derived "no target repository" stop reason is not an extra open decision.
- I renamed the section heading above the rewritten stop test in `tests/cli/test_do_sequence_cli.py`.
- No mutation red-proof was run, as ordered. The first `sed -i` attempt on the pin was refused by the sandbox; I used the edit tool instead.

## For the operator

When a budget stops a job, the person is asked one question and only one. The follow-up question about the mission's unmet criteria no longer appears beside it. It appears once, when the person abandons the stopped job, because only then is the stop final. A cancelled job used to hide every question, including that one, so the follow-up could be raised and never seen; it now stays visible. The walk's report names the one question and the answer to give. A client driving an order sees the same single question and its open blocking criteria.

## Next

In order: Phase 1 rule 1 (`.agent/STOP`), then rule 2 (Open PR Gate), then book round 4's verdict in the next round's first commit, then the closure sequence's integration-gate round.
Operator questions open: 1. Open findings: 89 (gate 5, `open_finding_ids`, read at `3a6af6b74`, rule: R-1373 and R-1374 open until the reviewer's resolution).
