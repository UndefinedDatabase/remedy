# Handoff — F295 session 3, round 11: book round 10, register R-1149, land DECISION F295 D10 (R-1148's repair)

## Session

SESSION 3 of feature F295 · rounds 10 to 11 · rounds so far 11

Context self-assessment: "The reviewer's context is comfortable after two rounds; the session
continues."

Fortschritt: ~72 % (T001 and T002 landed · T003's stdin proof and R-1147's resume guard landed
· R-1148's repair landed, review pending · R-1146, R-1147's providers, the hunk decision and
T004 open; then the hardening stage and the closure) — Schätzung

## Range

Review of `9233a90bc`..`931166c5a`, plus this handback commit.

## Commits

### 0f137b0e5 F295 R11 C1: book round 10, register R-1149, DECISION F295 D10, a prose slip, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f295-r11.md` | 153/0 (new) | byte copy of the round 11 block |
| `.agent/live_review.md` | 4/0 | append round 10's gate entry (PASS) and the registration of R-1149, exactly as the reviewer prepared it |
| `.agent/decisions.md` | 10/0 | append DECISION F295 D10 |
| `.agent/prose_slips.md` | 1/0 | append one prose-slip line, exactly as the reviewer prepared it |
| `.agent/plan.md` | 11/13 | rewrite to round 11's current step |

### 1f8e9e5a3 F295 R11 C2: a job that remedy do plans records its order text digest, so its run manifest is written (R-1148)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/do_sequence.py` | 8/0 | DECISION F295 D10 (1), (2): `hashlib` imported at the module top in sorted order; `plan_order_job` computes `job_file_sha256` once, right after `mission = order`, from `mission.encode("utf-8")`, with the one-line why-comment directly above it, and passes it to each of its three `JobPlan(` constructions (the LLM plan, the failed LLM plan, the deterministic plan) |

### 931166c5a F295 R11 C3: tests that a remedy do job records its order digest, writes its manifest and stops durably (R-1148)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_do_sequence_order_digest.py` | 188/0 (new) | five unit tests over all three `plan_order_job` constructions: the deterministic plan, an explicit `deterministic_tasks=` plan, a successful LLM task plan (mocks copied from `tests/cli/test_plan_approval.py`), a failed LLM task plan (digest still on the one job record), and the digest taken over the order's UTF-8 bytes (a non-ASCII order) |
| `tests/cli/test_do_sequence_cli.py` | 57/0 | two tests appended, using the file's own `repo` fixture, tripwires and `_do`: a full `do` run's job record carries `job_file_sha256` matching its own `mission`, a non-empty `run_manifest.path` and an empty `run_manifest.error`, named by `status --json`'s `client.jobs[*].evidence.run_manifest_path`; and a `--plan-only` job run with `--deadline 2000-01-01T00:00:00+00:00` ends `status` `stopped`, `stop.source` `budget`, an empty `run_manifest.error`, and `status --json` lists it `state` `stopped` |

### F295 R11 C4: handback (self-reference exception — committed by this same write)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file, rewritten in full per `docs/agents/handback_template.md` |

## External actions

None during the round before C4. After C4: `git push origin feature/f295-machine-client-contract-v1`;
its outcome is in the worker's final reply (write-once rule). No PR opened, no `gh` command, beyond
the Open PR Gate check the block did not ask this round to repeat (round 10's handoff already
recorded no open PR for this branch).

## Verification

Gates ran once each, after C3 and before C4.

1. `git -C /home/decodeux/Repos/remedy status --porcelain` → empty output. Byte comparison of
   every file C1 wrote (`git show 0f137b0e5:<path>`) against its prepared file, five of five
   equal (`.agent/authored/f295-r11.md` vs `block.md`, `.agent/live_review.md` vs
   `dry-live_review.md`, `.agent/decisions.md` vs `dry-decisions.md`, `.agent/prose_slips.md` vs
   `dry-prose_slips.md`, `.agent/plan.md` vs `dry-plan.md`).
2. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r11/run.py /home/decodeux/Repos/remedy 5
   python3 -m ruff check packages/orchestration/do_sequence.py
   tests/orchestration/test_do_sequence_order_digest.py tests/cli/test_do_sequence_cli.py`
   ```
   exit 0
   All checks passed!
   ```
3. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r11/run_selection.py /home/decodeux/Repos/remedy`
   ```
   exit 0
   SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
   SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
   SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
   3963 passed, 3 skipped in 65.49s (0:01:05)
   ```
   No FAILED, ERROR or `process(es) behind` line.
4. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r11/run.py /home/decodeux/Repos/remedy 3
   python3 -m apps.cli.main integrity check --json`
   ```
   exit 1
   {"check_count": 6, "checks": [{"message": "handlers=174", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "1 open blocker/high: R-1147", "name": "high_blockers_open", "status": "fail"}], "error": "integrity_failed", "fail_count": 1, "message": "integrity gate failed with 1 failing check(s)", "ok": false, "passed": false, "schema_version": 1, "version": 1}
   ```
   `fail_count` 1, the one failing check `high_blockers_open` reading `1 open blocker/high: R-1147`;
   R-1147 was booked before this round and stays open after this round by design (its provider half
   is still open).
5. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r11/run.py /home/decodeux/Repos/remedy 3
   python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
   ```
   exit 0
   ['R-1138', 'R-1139', 'R-1143', 'R-1146', 'R-1147', 'R-1148', 'R-1149']
   ```
   R-1148 is resolved by the reviewer in the next round's first commit, not by this round.

## Authored-text proofs

- `block.md` → `.agent/authored/f295-r11.md`: 153 lines / 153 lines, sha256
  `78c73475b49a09b9df19014382b930058be425a46859492e717357038aa8fcaf` / same, byte comparison equal.
- Every prepared file copied over its target (`dry-live_review.md`, `dry-decisions.md`,
  `dry-prose_slips.md`, `dry-plan.md`): byte comparison equal, before the commit and again from the
  committed bytes in gate 1.
- Append proofs: `git show 9233a90bc:.agent/live_review.md` plus the bytes of
  `append-live_review.txt` equals the new file: `True`; the same for `.agent/decisions.md` with
  `append-decisions.txt`: `True`; the same for `.agent/prose_slips.md` with
  `append-prose_slips.txt`: `True`.
- Every prepared file's sha256 was read with Python before use and matched the block's value
  (`dry-live_review.md`, `dry-decisions.md`, `dry-prose_slips.md`, `dry-plan.md`,
  `append-live_review.txt`, `append-decisions.txt`, `append-prose_slips.txt`, and `block.md`
  itself, 153 lines, verified before any read of its text).
- `git diff --cached --numstat` before the C1 commit matched the block's cells: `153 0` (the
  authored copy), `10 0` (decisions), `4 0` (the ledger), `11 13` (the plan), `1 0` (the prose
  slips).

## Deviations & assumptions

- Attribution line: every commit of this round closes with
  `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`, the model this worker runs on.
- Helper scripts `verify_block.py`, `verify_prepared.py`, `copy_c1.py`, `append_proof.py` and
  `gate1_byte_compare.py` under `.remedy-wt/f295-r11-worker/` did the digest checks, copies,
  append proofs and the gate-1 byte comparison the block's sandbox rules require. They are not
  committed.
- Before staging C2, this worker ran `python3 -m ruff check packages/orchestration/do_sequence.py`
  directly (not through the block's `run.py` wrapper) as a pre-commit sanity check.
- Before staging C3, this worker ran, as pre-commit sanity checks only: the five new tests of
  `tests/orchestration/test_do_sequence_order_digest.py` alone (`5 passed`); the two new tests
  appended to `tests/cli/test_do_sequence_cli.py` alone (`2 passed`); then the whole of
  `tests/cli/test_do_sequence_cli.py` (`48 passed`); and `python3 -m ruff check` on both test files
  directly. These are additional to, not instead of, the five numbered gates below, each of which
  ran exactly once, in order, after C3 and before C4, exactly as the block requires. No two test
  commands ran at once, no mutation red-proof was run, the full suite was never run, and
  `REMEDY_TEST_MAX_WORKERS` was never set.
- C2 touched only `packages/orchestration/do_sequence.py`; no new `except` clause, no new module,
  no catalog or docs change. No other departure from the block's ordered commit sequence (C1 to
  C4, gates, push) or its constraints.

## Round verdicts

Rounds 1 to 5 and 7 to 10 PASS and round 6 FAIL, booked in the ledger (round 10 by this round's
C1). Round 11's verdict is the reviewer's to give and book in the next round's first commit.

## For the operator, in plain sentences

Every job that the command `remedy do` plans now keeps a fingerprint of the order it was planned
from. Without it, Remedy could not write the run record it keeps for each run, so those records
were missing for every such job, and a job that ran out of budget kept looking as if it had never
started. Both now work: the run record is written, and a job that ran out of budget reads as
stopped. Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): not present during this round; if it appears, finish the commit
   in hand, write the handoff and stop.
2. Phase 1 rule 2: the Open PR Gate; no pull request is open for this branch yet.
3. Phase 1 rule 4: the reviewer reviews round 11 and books its verdict in the next round's first
   commit.
4. R-1146: the budget decision is answered under `--json`.

Operator questions open: 0.
Open findings: 7 (R-1147 High, R-1146 and R-1148 Medium, owned by F295; R-1138, R-1139, R-1143 and
R-1149 Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 (block copy, four record copies, append proofs, numstat) | done | `0f137b0e5` |
| C2 (`do_sequence.py`, DECISION F295 D10 (1), (2)) | done | `1f8e9e5a3` |
| C3 (order-digest unit tests, CLI manifest/budget-stop tests) | done | `931166c5a` |
| Gate 1 (status and byte comparisons) | done | porcelain empty, five of five equal |
| Gate 2 (ruff) | done | `All checks passed!` |
| Gate 3 (selection) | done | `3963 passed, 3 skipped`, exit 0 |
| Gate 4 (integrity check) | done | exit 1, `fail_count` 1, `high_blockers_open`: `1 open blocker/high: R-1147` |
| Gate 5 (open finding ids) | done | `['R-1138', 'R-1139', 'R-1143', 'R-1146', 'R-1147', 'R-1148', 'R-1149']` |
| C4 handback commit | done | this file |
| Push after C4 | pending | runs right after this commit, reported in the worker's final reply |
