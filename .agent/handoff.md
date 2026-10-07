# Handoff — F295 session 2, round 8: book round 7, finish T002 (DECISION F295 D7), repair R-1144

## Session

SESSION 2 of feature F295 · rounds 7 to 8 · rounds so far 8

Context self-assessment: "The reviewer's context is comfortable after two rounds; the session
continues."

Fortschritt: ~65 % (T001 landed · T002 landed, review pending · T003 and T004 open; then the hardening stage and the closure) — Schätzung

## Range

Review of `6a8055359`..`5b6a3169c`, plus this handback commit.

## Commits

### 47e092e17 F295 R8 C1: book round 7, resolve R-1142, register R-1144, DECISION F295 D7, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f295-r8.md` | 130/0 (new) | byte copy of the round 8 block |
| `.agent/live_review.md` | 6/0 | append round 7's gate entry (PASS), the resolution of R-1142 and R-1144 as the reviewer prepared them |
| `.agent/decisions.md` | 10/0 | append DECISION F295 D7 |
| `.agent/plan.md` | 9/13 | rewrite to round 8's current step |

### 2502571e8 F295 R8 C2: the job digest's cost basis and the cockpit's cost of the day become public readers (refactor, no behaviour change)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/job_digest.py` | 14/5 | byte copy of the prepared file: the cost-basis rule becomes a public reader |
| `packages/orchestration/project_cockpit.py` | 31/20 | byte copy of the prepared file: the cost-of-the-day rule becomes a public reader |

### 48e9fe062 F295 R8 C3: the client digest carries each job's cost and evidence and each project's cost of the day (T002, DECISION F295 D7)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/client_digest.py` | 81/13 | byte copy of the prepared file: per-job cost and evidence references, per-project cost of the day |

### 23577700a F295 R8 C4: tests for each job's cost and evidence and each project's cost of the day (T002)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_client_digest.py` | 136/0 | byte copy of the prepared test file |
| `tests/cli/test_status_cmd.py` | 27/0 | byte copy of the prepared test file |

### 5b6a3169c F295 R8 C5: the client digest lists projects without rewriting a record (R-1144)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/client_digest.py` | 3/2 | byte copy of the prepared file: project listing no longer rewrites a record |
| `tests/orchestration/test_client_digest.py` | 37/0 | byte copy of the prepared test file: reading changes no file |

### F295 R8 C6: handback (self-reference exception — committed by this same write)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file, rewritten in full per `docs/agents/handback_template.md` |

## External actions

None during the round before C6. After C6: `git push origin feature/f295-machine-client-contract-v1`;
its outcome is in the worker's final reply (write-once rule). No PR opened, no `gh` command.

## Verification

Gates ran once each, after C5 and before C6.

1. `git -C /home/decodeux/Repos/remedy status --porcelain` → exit 0, empty output. Byte
   comparison of every file each of C1 to C5 wrote (`git show <commit>:<path>`) against its
   prepared file, eleven of eleven equal.
2. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r8/run.py /home/decodeux/Repos/remedy 5
   python3 -m ruff check packages/orchestration/client_digest.py
   packages/orchestration/job_digest.py packages/orchestration/project_cockpit.py
   tests/orchestration/test_client_digest.py tests/cli/test_status_cmd.py`
   ```
   exit 0
   All checks passed!
   ```
3. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r8/run_selection.py /home/decodeux/Repos/remedy`
   ```
   exit 0
   SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
   SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
   SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
   3952 passed, 3 skipped in 47.59s
   ```
   No FAILED, ERROR or `process(es) behind` line.
4. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r8/run.py /home/decodeux/Repos/remedy 3
   python3 -m apps.cli.main integrity check --json`
   ```
   exit 0
   {"check_count": 6, "checks": [{"message": "handlers=174", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
   ```
5. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r8/run.py /home/decodeux/Repos/remedy 3
   python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
   ```
   exit 0
   ['R-1138', 'R-1139', 'R-1143', 'R-1144']
   ```

## Authored-text proofs

- `block.md` → `.agent/authored/f295-r8.md`: 130 lines / 130 lines, sha256
  `248cc539914d5db8b503f9f10ac3b1781057a9a34c7b8c2fd460da6469ef4f0f` / same, byte comparison equal.
- Every prepared file copied over its target (`dry-live_review.md`, `dry-decisions.md`,
  `dry-plan.md`, `dry-job_digest.py`, `dry-project_cockpit.py`, `dry-client_digest-c3.py`,
  `dry-test_client_digest-c4.py`, `dry-test_status_cmd.py`, `dry-client_digest.py`,
  `dry-test_client_digest.py`): byte comparison equal, before the commit and again from the
  committed bytes in gate 1.
- Append proofs: `git show 6a8055359:.agent/live_review.md` plus the bytes of
  `append-live_review.txt` equals the new file: `True`; the same for `.agent/decisions.md` with
  `append-decisions.txt`: `True`.
- Every prepared file's sha256 was read with Python before use and matched the block's value.
- `git diff --cached --numstat` before each commit matched the block's cells: C1 `130 0`, `10 0`,
  `6 0`, `9 13`; C2 `14 5`, `31 20`; C3 `81 13`; C4 `136 0`, `27 0`; C5 `3 2`, `37 0`.

## Round verdicts

Rounds 1 to 5 and 7 PASS and round 6 FAIL, booked in the ledger (round 7 by this round's C1).
Round 8's verdict is the reviewer's to give and book in the next round's first commit.

## For the operator, in plain sentences

The status reading for a program is now complete. For every job it shows how much the job has cost
and how exact that figure is, and where its evidence lies on disk: the run numbers, the failure
report, the record of its inputs and the final change. For every project it shows what that project
has cost today. Reading it takes well under a second even with two hundred jobs. The reviewer found
that reading the status could quietly rewrite an old project record; this round stops that, and a
test now proves that reading changes no file. Nothing waits for the operator.

## Deviations & assumptions

- Attribution line: every commit of this round closes with
  `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`, the model this worker runs on.
- Helper scripts `verify.py`, `stage.py` and `gate1.py` under `.remedy-wt/f295-r8-worker/` did the
  digest checks, copies, proofs and staging, as the block's sandbox rules require. They are not
  committed.
- No other departure from the block's commit sequence (C1 to C5, gates, C6) or its constraints.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if present, write the handoff and stop.
2. Phase 1 rule 2: the Open PR Gate; no pull request is open for this branch yet.
3. Phase 1 rule 4: the reviewer reviews round 8 and books its verdict and the resolution of R-1144
   in the next round's first commit.
4. T003: every decision kind answerable with `--json`, and a test that a run with `--yes --no-ui --json` on a pipe never reads stdin.

Operator questions open: 0.
Open findings: 4 (R-1144 Low, owned by F295, repaired by this round; R-1138, R-1139 and R-1143 Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 (block copy, three record copies, append proofs, numstat) | done | `47e092e17` |
| C2 (`job_digest.py`, `project_cockpit.py` refactor) | done | `2502571e8` |
| C3 (`client_digest.py`, T002) | done | `48e9fe062` |
| C4 (two test files) | done | `23577700a` |
| C5 (R-1144 repair) | done | `5b6a3169c` |
| Gate 1 (status and byte comparisons) | done | porcelain empty, eleven of eleven equal |
| Gate 2 (ruff) | done | `All checks passed!` |
| Gate 3 (selection) | done | `3952 passed, 3 skipped`, exit 0 |
| Gate 4 (integrity check) | done | exit 0, `fail_count` 0 |
| Gate 5 (open finding ids) | done | `['R-1138', 'R-1139', 'R-1143', 'R-1144']` |
| C6 handback commit | done | this file |
| Push after C6 | pending | runs right after this commit, reported in the worker's final reply |
