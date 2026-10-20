# Handoff — F312 round 1 (claim, step (2) of plan_order_job's boundary, and T001)

## Session

SESSION 1 of feature F312 · round 1 · rounds so far 1

Context self-assessment: the session stayed inside the block — every prepared file was digest-checked with a Python reader before use, the structural move (C2) and the feature code (C3) were kept in separate commits exactly as ordered, and the one pytest selection ran alone.

State block:
Feature F312 (`[~]` in STATUS since C1), branch `feature/f312-scope-kinds`, base `0eda402fe`. Head: this commit (C5), after C1 to C4.
Fortschritt: ~45 % (claim and T001 landed · T002 and T003 open) — Schätzung

## Range

Review of `0eda402fe`..HEAD (C1 to C4 below, then this commit, C5, which also carries this handback).

## Commits

### 65afa4cf5 F312 R1 C1: claim F312, re-head the ledger, DECISIONs F312 D1 and D2
298 insertions, 58 deletions.
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f312-r1.md` | +214 | byte copy of the block |
| `.agent/context.md` | +10/-10 | byte copy of the prepared context |
| `.agent/decisions.md` | +20 | appended DECISIONs F312 D1 and D2 |
| `.agent/live_review.md` | +19/-14 | re-headed at the F312 claim |
| `.agent/plan.md` | +14/-13 | byte copy of the prepared plan |
| `docs/roadmap/STATUS.md` | +1/-1 | F312 claimed (`[ ]` to `[~]`) |

### dcb1436f1 F312 R1 C2: the first-pass task plan becomes _first_pass_task_plan (structure step)
107 insertions, 91 deletions; structural, no behaviour change.
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/do_sequence.py` | +103/-87 | `plan_order_job`'s `if plan_call_fn is not None:` body (487 lines, unindented) becomes `_first_pass_task_plan`, called from `plan_order_job`; measured 165 lines (was 249) |
| `docs/system/structure-ledger-v1.md` | +3/-3 | `plan_order_job` row 249→165; step (2) of its boundary reads "done by F312 … `_first_pass_task_plan`" |
| `tests/test_structure_ratchet.py` | +1/-1 | `MAX_FUNCTION_LINES` 28852→28768 (the 84-line fall) |

### 5eb6b0bf3 F312 R1 C3: the task-plan guard reads the kind of the person's order
78 insertions, 22 deletions.
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/do_scope.py` | +41/-2 | `order_scope_kind` and its three constants (DECISION F312 D1); `out_of_scope_task_ids` reads the kind, open-order branch over `is_checking_only`; module docstring paragraph |
| `packages/orchestration/do_sequence.py` | +27/-20 | `_deliverable_task_plan`'s open-order refusal message; `plan_order_job` gains `scope_order` (DECISION F312 D2), docstring re-wrapped at 100 cols (net 0 lines); `_first_pass_task_plan` gains `scope_order`, passes it to `_deliverable_task_plan`; `_step_shape` passes `scope_order=ctx.order` |
| `docs/guides/do-run-v1.md` | +10 | the three-kinds paragraph inserted after "…never a second job." |

### a7b1eadf9 F312 R1 C4: the three kinds and the outline that no longer fences, tested
170 insertions.
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_do_scope.py` | +45 | `order_scope_kind` over the six fixture orders; `out_of_scope_task_ids` over the lab site order (T002/T003/T004, the fenced order) |
| `tests/orchestration/test_do_sequence.py` | +18 | `_deliverable_task_plan` refuses an all-checking-artifact plan for the open lab order |
| `tests/orchestration/test_do_sequence_scope_order.py` | +86 (new file) | `plan_order_job` with a mocked planner over a fencing outline: open `scope_order` lets both tasks through; no `scope_order` and a fenced `scope_order` both still refuse on the outline's own fence |
| `tests/cli/test_do_sequence_cli.py` | +21 | `--force-mission` over the file's own `ORDER`, two forced milestones: `plan_order_job` called at least twice, every call's `scope_order` equal to `ORDER` |

### this commit (C5) F312 R1 C5: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file (a handoff cannot table its own commit) |

## External actions

The push is run after this commit, so its outcome is reported in the final reply only. Before this commit: no push, no `gh` command, no pull request (none was open at session start; none is opened this round).

## Verification

1. Gate 1: `git status --porcelain` — empty. `python3 .remedy-wt/f312-r1/prep/verify.py .`:
   ```
   True	65afa4cf5 single parent equal to the commit before it
   True	dcb1436f1 single parent equal to the commit before it
   True	5eb6b0bf3 single parent equal to the commit before it
   True	a7b1eadf9 single parent equal to the commit before it
   True	every commit carries an F312 R1 Cn subject: 4 of 4
   True	C1 paths exactly [...]
   True	C2 paths inside its set: [...]
   True	C3 paths inside its set: [...]
   True	C4 paths all under tests/: [...]
   absent	C5
   True	C1 .agent/authored/f312-r1.md equals block.md
   True	C1 docs/roadmap/STATUS.md equals dry-STATUS.md
   True	C1 .agent/live_review.md equals dry-live_review.md
   True	C1 .agent/decisions.md equals dry-decisions.md
   True	C1 .agent/plan.md equals dry-plan.md
   True	C1 .agent/context.md equals dry-context.md
   True	C2 do_sequence.py defines _first_pass_task_plan once
   True	C2 the guard call is moved unchanged
   True	C2 adds no scope_order (the structural step changes no behaviour)
   True	C2 ledger names step (2) done by F312
   True	C3 do_scope.py defines order_scope_kind once
   True	C3 do_scope.py defines ORDER_SCOPE_NAMES_FILES = "names_files"
   True	C3 do_scope.py defines ORDER_SCOPE_FENCED = "fenced"
   True	C3 do_scope.py defines ORDER_SCOPE_OPEN = "open"
   True	C3 _step_shape passes scope_order=ctx.order once
   True	C3 the open order's refusal message
   True	C3 the fenced refusal message stays
   True	C3 the guide paragraph stands right after its anchor
   True	C3 the guide is the base plus the paragraph and nothing else
   True	C3 leaves packages/orchestration/order_scope.py byte-identical (do not touch)
   ALL True
   ```
2. Gate 2: `python3 -m ruff check` over every Python file C2, C3 and C4 touched (`packages/orchestration/do_sequence.py`, `packages/orchestration/do_scope.py`, `tests/test_structure_ratchet.py`, `tests/orchestration/test_do_scope.py`, `tests/orchestration/test_do_sequence.py`, `tests/orchestration/test_do_sequence_scope_order.py`, `tests/cli/test_do_sequence_cli.py`): exit 0, `All checks passed!`.
3. Gate 3: `python3 .remedy-wt/f312-r1/prep/run_selection.py . .remedy-wt/f312-r1-worker/selection-output.txt`: `paths 88`, `exit 0`, `3765 passed, 2 skipped in 106.51s (0:01:46)`; no FAILED or ERROR line, no "process(es) behind" line. SKIPPED lines:
   - `SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.`
   - `SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access`
4. Gate 4: `python3 -m apps.cli.main integrity check --json`: exit 1, `fail_count` 1, the one failing check `high_blockers_open`: `"13 open blocker/high: R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362, R-1369"` — the thirteen of DECISION F310 D7, no other.
5. Gate 5: `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` — `87`.
6. Gate 6: `python3 -c "from packages.orchestration.do_scope import order_scope_kind as k; print(k('Super, jetzt mach ein schickes design'), k('Bring die webseite auf prototyp niveau und füge funktionalität hinzu'))"` — `open open`.

## Authored-text proofs

Byte copy of `block.md` to `.agent/authored/f312-r1.md` at C1, proved by a sha256 equality in the copy script (214 lines, matching the prompt's digest and line count exactly) and confirmed again by `verify.py`'s `C1 .agent/authored/f312-r1.md equals block.md` line above. The other five C1 copies (`docs/roadmap/STATUS.md`, `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/context.md`) are prepared-file byte copies, each proved equal by sha256 in the copy script and again by `verify.py`.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | branch `feature/f312-scope-kinds` from `0eda402fe` |
| C1 | done | 65afa4cf5 |
| C2 | done | dcb1436f1 |
| C3 | done | 5eb6b0bf3 |
| C4 | done | a7b1eadf9 |
| C5 | done | this commit |
| Gate 1 | done | ALL True |
| Gate 2 | done | All checks passed! |
| Gate 3 | done | exit 0, 3765 passed, 2 skipped |
| Gate 4 | done | fail_count 1 on the standing thirteen |
| Gate 5 | done | 87 |
| Gate 6 | done | open open |

## Deviations & assumptions

- None from the block's ordered commit sequence: C0 to C4 ran in order, each committing exactly the paths its `ALLOWED` set names (confirmed by `git diff --cached --numstat` before every commit and by `verify.py` after C4).
- C2's structural move did not need the optional second function `_first_pass_plan_approval`: `_first_pass_task_plan` measured 96 lines, at the ratchet's 100-line limit, so the `if run_unattended:` branch stayed inside it.
- C3's re-wrap of `plan_order_job`'s docstring at 100 columns, with the new `scope_order` sentence added, measured the function at exactly 165 lines — unchanged from its C2 row — so no further ledger or ratchet edit was needed in C3 (the block's "if its measure falls, lower its row" did not apply; it held even).
- The records of the operator's failed lab job (`ee8c1df67ef94353` and the failed run) were not read: the data root is not readable in this session, per DECISION F312 D1; the finding's text and the code were the evidence, as the block and the DECISION both state.
- `docs/README.md` was not touched: nothing in this round adds, moves or renames a doc.

## For the operator, in plain sentences

Remedy now tells three kinds of request apart before it plans a job: one that names a file, one that says "and nothing else", and one that says neither, like "make it look nice". For that plain third kind, Remedy no longer refuses a job just because the files the planner ends up touching were never named in the request; it only refuses when every planned step would merely check something rather than carry out the requested work. A plan written for one milestone inside a bigger request can still say what that smaller job should do, but it can no longer draw a stricter line than the person themselves drew. A piece of the planner that was growing large was split into a function of its own first, with no change to what it does, so the new behaviour had room to land cleanly on top of it. Two pieces of this feature are still open for the next round: teaching Remedy to ask a clarifying question after two failed attempts at a plain request, and proving the whole thing end to end with the original example requests that first exposed the problem. One question still waits for the operator from an earlier round, about findings closed without their proof recorded.

## Next

In order: Phase 1 rule 1 (`.agent/STOP`); the Open PR Gate; the booking of round 1's verdict in the next round's first commit; T002 under DECISION F312 D3, and T003.
Operator questions open: 1. Open findings: 87 (gate 5, `open_finding_ids`, read at C1's ledger).
