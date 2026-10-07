# Handoff — F295 session 5, round 20: round 19 booked, the acceptance audit saved, R-1154 repaired

## Session

SESSION 5 of feature F295 · round 20 · rounds so far 20

Context self-assessment (quoted from the block): "The reviewer's context is comfortable after one
round; this session plans the repair of R-1155 and the repeated audit next."

Fortschritt: ~94 % (T001 to T004 landed; the hardening stage's audit done, R-1154 repaired, R-1155
next; then the closure) — Schätzung

## Range

Review of `d0ca96e49`..`fbcca45d8`, plus this handback commit.

## Commits

### c0fe67f62 F295 R20 C1: book round 19's PASS and R-1153, register R-1154 and R-1155, DECISION F295 D18, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f295-r20.md` | 118/0 (new) | byte copy of this round's block |
| `.agent/live_review.md` | 8/0 | append round 19's gate entry and R-1154/R-1155, exactly as prepared |
| `.agent/decisions.md` | 10/0 | append DECISION F295 D18, exactly as prepared |
| `.agent/plan.md` | 13/15 | rewrite to round 20's current step |

### 52086d219 F295 R20 C2: save the acceptance audit of the hardening stage (DECISION F295 D18)

| Path | +/- | Reason |
|---|---|---|
| `.agent/f295_acceptance_audit.md` | 139/0 (new) | the acceptance audit's report, byte copy of the prepared file |

### fbcca45d8 F295 R20 C3: a test proves remedy do with no-ui never calls the cockpit launcher (R-1154)

| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_do_sequence_cli.py` | 24/0 | test proving `--no-ui` never calls the cockpit launcher (R-1154), byte copy of the prepared file |

### F295 R20 C4: handback (self-reference exception — committed by this same write)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file, rewritten in full per `docs/agents/handback_template.md` |

## External actions

No `gh` command was run, no PR opened. After C4:
`git push origin feature/f295-machine-client-contract-v1`; its outcome is in the worker's final
reply (write-once rule). `.agent/STOP` was absent throughout.

## Verification

Gates ran in the block's order, once each, after C3 and before C4; all five read green.

1. `git -C /home/decodeux/Repos/remedy status --porcelain` → empty. Byte comparison of every file C1
   to C3 wrote (`git show <commit>:<path>`) against its prepared file, six of six equal.
   ```
   porcelain: ''
   c0fe67f62 .agent/authored/f295-r20.md == block.md : True
   c0fe67f62 .agent/live_review.md == dry-live_review.md : True
   c0fe67f62 .agent/decisions.md == dry-decisions.md : True
   c0fe67f62 .agent/plan.md == dry-plan.md : True
   52086d219 .agent/f295_acceptance_audit.md == audit.md : True
   fbcca45d8 tests/cli/test_do_sequence_cli.py == dry-test_do_sequence_cli.py : True
   ALL EQUAL: True
   ```
2. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r15/run.py /home/decodeux/Repos/remedy 5
   python3 -m ruff check tests/cli/test_do_sequence_cli.py`
   ```
   exit 0
   All checks passed!
   ```
3. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r20/run_selection.py /home/decodeux/Repos/remedy`
   ```
   exit 0
   SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
   SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
   SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
   3639 passed, 3 skipped in 120.71s (0:02:00)
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
   ['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1154', 'R-1155']
   ```

## Authored-text proofs

- `block.md` → `.agent/authored/f295-r20.md`: 118 lines / 118 lines, sha256
  `68c9ef56f23f16404fdd7a6af66a0cc52330fe7fa94a56fc29fb7cfbdcca1878` / same, verified before any
  other read; byte comparison equal from the committed bytes in gate 1.
- Every prepared file's sha256 was read with Python before use and matched the block's value (seven
  of seven, re-checked before each commit). `HEAD` equalled
  `origin/feature/f295-machine-client-contract-v1` at `d0ca96e49b53a1cc9333d427d35aea4090758f8d`
  before any write.
- Append proofs, each `True`: `git show d0ca96e49:.agent/live_review.md` plus
  `append-live_review.txt` equals the new ledger; `git show d0ca96e49:.agent/decisions.md` plus
  `append-decisions.txt` equals the new decisions file.
- `git diff --cached --numstat` before each commit matched the block's cells exactly: C1 `118 0`,
  `10 0`, `8 0`, `13 15`; C2 `139 0`; C3 `24 0`.

## Deviations & assumptions

None. Every file in C1 to C3 is a byte copy of a reviewer-prepared file; the worker authored no code
and no record text beyond this handback. Gates ran once each in the block's order, none red. No
mutation red-proof, no full suite, no `REMEDY_TEST_MAX_WORKERS`, never two test commands at once. No
commit exceeded 500 insertions. Every commit ends with `Co-Authored-By: Claude Sonnet 5
<noreply@anthropic.com>`. Helper scripts under `.remedy-wt/f295-r20-worker/` (gitignored) did the
digest checks, copies and proofs. The selection read `3639 passed` against round 19's `3595 passed`;
the selection helper is the reviewer's and was run unchanged.

## Round verdicts

Rounds 1 to 5, 7 to 13 and 15 to 19 PASS, rounds 6 and 14 FAIL, booked in the ledger (round 19 by
this round's C1); round 20's verdict is the reviewer's to give and book in the next round's first
commit.

## For the operator, in plain sentences

A separate checker, who saw only the feature's description and the code, went through every promise
this feature makes and tried to break each one on purpose to see whether a test noticed. Twenty-eight
of thirty-one promises were guarded at once. One real hole was found: no test noticed if Remedy
opened its browser window although the program had asked it not to; this round adds that test. A
second reported hole turned out to be guarded after all. Separately, the reviewer found that a
question Remedy asks when a run stops at its money or time limit stays open even after the limit was
raised and the run finished; the next round repairs that. Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): not present during this round; if it appears, finish the commit
   in hand, write the handoff and stop.
2. Phase 1 rule 2: the Open PR Gate; no pull request is open for this branch yet.
3. Phase 1 rule 4: the reviewer reviews round 20 and books its verdict and R-1154's resolution in the
   next round's first commit.
4. Repair R-1155 under a DECISION of its own.
5. Repeat the acceptance audit for claim 7 and the claims R-1155's repair touches, and write the
   feature file's Built State paragraph.
6. The closure sequence.

Operator questions open: 0.
Open findings: 6 (R-1154 Low, owned by F295, repaired, review pending; R-1155 Low, owned by F295,
open; R-1138, R-1139, R-1143 and R-1149, Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 (book round 19, R-1154/R-1155, D18, plan) | done | `c0fe67f62` |
| C2 (acceptance audit) | done | `52086d219` |
| C3 (R-1154 test) | done | `fbcca45d8` |
| Gate 1 (status and byte comparisons) | done | porcelain empty, six of six equal |
| Gate 2 (ruff) | done | `All checks passed!` |
| Gate 3 (selection) | done | `3639 passed, 3 skipped`, exit 0 |
| Gate 4 (integrity check) | done | `"fail_count": 0` |
| Gate 5 (open finding ids) | done | `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1154', 'R-1155']` |
| C4 handback commit | done | this file |
| Push after C4 | pending | runs right after this commit, reported in the worker's final reply |
