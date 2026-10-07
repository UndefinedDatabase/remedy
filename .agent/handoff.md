# Handoff — F295 session 4, round 17: round 16 booked, R-1152 repaired (`change proof` lists the job's applies)

## Session

SESSION 4 of feature F295 · rounds 16 to 17 · rounds so far 17

Context self-assessment (quoted from the block): "The reviewer's context is comfortable after two
rounds; the session continues."

Fortschritt: ~85 % (T001, T002 and T003 landed · R-1152's repair, review pending · T004 open; then
the hardening stage and the closure) — Schätzung

## Range

Review of `89ad24d76`..`4d3aaa3ad`, plus this handback commit.

## Commits

### 5503d991d F295 R17 C1: book round 16's PASS, register R-1152, DECISION F295 D15, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f295-r17.md` | 112/0 (new) | byte copy of this round's block |
| `.agent/live_review.md` | 4/0 | append round 16's booking and R-1152, exactly as prepared |
| `.agent/decisions.md` | 10/0 | append DECISION F295 D15, exactly as prepared |
| `.agent/plan.md` | 12/7 | rewrite to round 17's current step |

### 5685031ac F295 R17 C2: change proof lists the job's applies, never as verified (R-1152, DECISION F295 D15)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/job_apply.py` | 33/0 | prepared reader of a job's applies |
| `packages/orchestration/proof_chain.py` | 28/0 | the proof lists them under `job_applies` |

### 4d3aaa3ad F295 R17 C3: tests of the proof's job applies through the parser (R-1152)

| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_change_proof_cli.py` | 115/0 | tests of `job_applies` through the parser |

### F295 R17 C4: handback (self-reference exception — committed by this same write)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file, rewritten in full per `docs/agents/handback_template.md` |

## External actions

No `gh` command was run, no PR opened. After C4:
`git push origin feature/f295-machine-client-contract-v1`; its outcome is in the worker's final reply
(write-once rule). `.agent/STOP` was absent throughout.

## Verification

Gates ran in the block's order, once each, after C3 and before C4; all five read green.

1. `git -C /home/decodeux/Repos/remedy status --porcelain` → empty. Byte comparison of every file C1
   to C3 wrote (`git show <commit>:<path>`) against its prepared file, seven of seven equal.
   ```
   porcelain: ''
   5503d991d .agent/authored/f295-r17.md == block.md : True
   5503d991d .agent/live_review.md == dry-live_review.md : True
   5503d991d .agent/decisions.md == dry-decisions.md : True
   5503d991d .agent/plan.md == dry-plan.md : True
   5685031ac packages/orchestration/job_apply.py == dry-job_apply.py : True
   5685031ac packages/orchestration/proof_chain.py == dry-proof_chain.py : True
   4d3aaa3ad tests/cli/test_change_proof_cli.py == dry-test_change_proof_cli.py : True
   ALL EQUAL: True
   ```
2. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r15/run.py /home/decodeux/Repos/remedy 5
   python3 -m ruff check packages/orchestration/job_apply.py packages/orchestration/proof_chain.py
   tests/cli/test_change_proof_cli.py`
   ```
   exit 0
   All checks passed!
   ```
3. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r17/run_selection.py /home/decodeux/Repos/remedy`
   ```
   exit 0
   SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
   SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
   SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
   4056 passed, 3 skipped in 36.60s
   ```
   No FAILED line, no ERROR line, no `process(es) behind` line.
4. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r15/run.py /home/decodeux/Repos/remedy 3
   python3 -m apps.cli.main integrity check --json`
   ```
   exit 0
   {"check_count": 6, "checks": [{"message": "handlers=175", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
   ```
5. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r15/run.py /home/decodeux/Repos/remedy 3
   python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
   ```
   exit 0
   ['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1152']
   ```

## Authored-text proofs

- `block.md` → `.agent/authored/f295-r17.md`: 112 lines / 112 lines, sha256
  `f8eb7a364290f9866234d99772e27014339afc975d2a618a2b65b729a6cf6a86` / same, verified before any
  other read of the block; byte comparison equal from the committed bytes in gate 1.
- Every prepared file's sha256 was read with Python before use and matched the block's value
  (eight of eight). `HEAD` equalled `origin/feature/f295-machine-client-contract-v1` at
  `89ad24d767f711a241d2480026223f8c8c2dce96` before any write.
- Append proofs, each `True`: `git show 89ad24d76:.agent/live_review.md` plus `append-live_review.txt`
  equals the new ledger; `git show 89ad24d76:.agent/decisions.md` plus `append-decisions.txt` equals
  the new decisions file.
- `git diff --cached --numstat` before each commit matched the block's cells exactly: C1 `112 0`,
  `10 0`, `4 0`, `12 7`; C2 `33 0`, `28 0`; C3 `115 0`.

## Deviations & assumptions

None. Every file in C1 to C3 is a byte copy of a reviewer-prepared file; the worker authored no
code and no record text beyond this handback. Gates ran once each in the block's order, none red.
No mutation red-proof, no full suite, no `REMEDY_TEST_MAX_WORKERS`, never two test commands at once.
No commit exceeded 500 insertions. Every commit ends with `Co-Authored-By: Claude Sonnet 5.5
<noreply@anthropic.com>`. Helper scripts under `.remedy-wt/f295-r17-worker/` (gitignored) did the
digest checks, copies and proofs.

## Round verdicts

Rounds 1 to 5, 7 to 13, 15 and 16 PASS, rounds 6 and 14 FAIL, booked in the ledger (round 16 by this
round's C1); round 17's verdict is the reviewer's to give and book in the next round's first commit.

## For the operator, in plain sentences

When a program has approved a job's changes and Remedy has written them into the project, the
program can now read afterwards what was written and when. Before this round Remedy's record of
proof answered "nothing to check" for such a job. The record still does not call these changes
verified, because no test was linked to them. Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): not present during this round; if it appears, finish the commit
   in hand, write the handoff and stop.
2. Phase 1 rule 2: the Open PR Gate; no pull request is open for this branch yet.
3. Phase 1 rule 4: the reviewer reviews round 17 and books its verdict and R-1152's resolution in
   the next round's first commit.
4. T004: the contract page and the gate test.

Operator questions open: 0.
Open findings: 5 (R-1152 Medium, owned by F295, repaired, review pending; R-1138, R-1139, R-1143 and
R-1149, Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 (book round 16, register R-1152, D15, plan) | done | `5503d991d` |
| C2 (job applies in the proof, reader) | done | `5685031ac` |
| C3 (tests of `job_applies`) | done | `4d3aaa3ad` |
| Gate 1 (status and byte comparisons) | done | porcelain empty, seven of seven equal |
| Gate 2 (ruff) | done | `All checks passed!` |
| Gate 3 (selection) | done | `4056 passed, 3 skipped`, exit 0 |
| Gate 4 (integrity check) | done | `"fail_count": 0` |
| Gate 5 (open finding ids) | done | `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1152']` |
| C4 handback commit | done | this file |
| Push after C4 | pending | runs right after this commit, reported in the worker's final reply |
