# Handoff — F295 session 3, round 15: R-1151 registered and repaired, selection green again

## Session

SESSION 3 of feature F295 · rounds 10 to 15 · rounds so far 15

Context self-assessment (quoted from the block): "The reviewer's context is comfortable after six
rounds; the session continues."

Fortschritt: ~80 % (T001 and T002 landed · T003's stdin proof and the budget decision's two
answers landed · R-1147's providers landed and their selection repaired, review pending · the
hunk decision and T004 open; then the hardening stage and the closure) — Schätzung

## Range

Review of `4ae5d4d33`..`4692b7d07`, plus this handback commit.

## Commits

### 0e5652b5a F295 R15 C1: book round 14's FAIL, register R-1151, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f295-r15.md` | 101/0 (new) | byte copy of this round's block |
| `.agent/live_review.md` | 4/0 | append round 14's gate entry (VERDICT FAIL) and R-1151's registration, exactly as the reviewer prepared it |
| `.agent/plan.md` | 7/5 | rewrite to round 15's current step |

### 4692b7d07 F295 R15 C2: the exit-code registry names the site job resume reaches through job run (R-1151)

| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_exit_codes.py` | 7/0 | `UNRESOLVED_SITES` gains a `"job.resume"` entry, `frozenset({0, 1, 2})`, naming the same `sys.exit(code)` / `follow_run(body)` site already named for `"job.run"`, reached through `_cmd_job_run` per DECISION F295 D13 |

### F295 R15 C3: handback (self-reference exception — committed by this same write)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file, rewritten in full per `docs/agents/handback_template.md`, reporting all five gates green |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` returned `[]` — no open PR
for this branch; the Open PR Gate passes with nothing to merge. No PR opened, no other `gh`
command besides this list. After C3: `git push origin feature/f295-machine-client-contract-v1`;
its outcome is in the worker's final reply (write-once rule).

## Verification

Gates ran in the block's order, once each, after C2 and before C3; all five read green.

1. `git -C /home/decodeux/Repos/remedy status --porcelain` → empty. Byte comparison of every file
   C1 and C2 wrote (`git show <commit>:<path>`) against its prepared file, four of four equal
   (`.agent/authored/f295-r15.md` vs `block.md`, `.agent/live_review.md` vs `dry-live_review.md`,
   `.agent/plan.md` vs `dry-plan.md`, `tests/cli/test_exit_codes.py` vs `dry-test_exit_codes.py`).
   ```
   (porcelain empty)
   0e5652b5a .agent/authored/f295-r15.md == block.md : True
   0e5652b5a .agent/live_review.md == dry-live_review.md : True
   0e5652b5a .agent/plan.md == dry-plan.md : True
   4692b7d07 tests/cli/test_exit_codes.py == dry-test_exit_codes.py : True
   ALL EQUAL: True
   ```
2. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r15/run.py /home/decodeux/Repos/remedy 5
   python3 -m ruff check tests/cli/test_exit_codes.py`
   ```
   exit 0
   All checks passed!
   ```
3. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r15/run_selection.py /home/decodeux/Repos/remedy`
   ```
   exit 0
   SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
   SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
   SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
   4444 passed, 3 skipped in 27.12s
   ```
   No FAILED line, no ERROR line, no `process(es) behind` line. The one test gate 3 of round 14
   found red, `tests/cli/test_exit_codes.py::test_declared_codes_equal_the_codes_the_handler_reaches[job.resume]`,
   is now green: `4444 passed` versus round 14's `4443 passed` plus the one failure.
4. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r15/run.py /home/decodeux/Repos/remedy 3
   python3 -m apps.cli.main integrity check --json`
   ```
   exit 1
   {"check_count": 6, "checks": [{"message": "handlers=174", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict FAIL", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "1 open blocker/high: R-1147", "name": "high_blockers_open", "status": "fail"}], "error": "integrity_failed", "fail_count": 1, "message": "integrity gate failed with 1 failing check(s)", "ok": false, "passed": false, "schema_version": 1, "version": 1}
   ```
   `"fail_count": 1`, the one failing check `high_blockers_open` reading `1 open blocker/high:
   R-1147`, exactly as the block expected.
5. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r15/run.py /home/decodeux/Repos/remedy 3
   python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
   ```
   exit 0
   ['R-1138', 'R-1139', 'R-1143', 'R-1147', 'R-1149', 'R-1151']
   ```
   Equals the block's expected list exactly.

## Authored-text proofs

- `block.md` → `.agent/authored/f295-r15.md`: 101 lines / 101 lines, sha256
  `8abfa3390828b53746f11d7fe8397b3ba3db3d5ec4d14804231fb461b0890b3d` / same, byte comparison equal
  (verified before any other read of the block's text, per the round's own opening instruction).
- Every prepared file's sha256 was read with Python before use and matched the block's value:
  `dry-live_review.md` (`d6df47002fb3398a24a95da375bbc07e3fdd5b8279a56929d849c7353a6d76ac`),
  `dry-plan.md` (`1a8ef2ad084e77fae400a4c30cee8a80ec622b584f1f15faa2acced4c2590cbf`),
  `append-live_review.txt` (`dc780b6232befa5e92dcf183b6cd6fd6f049903b24f219480a0ce33fad9ba752`),
  `dry-test_exit_codes.py` (`c7a38a3e2e17854092403724221c1ab252914de6a7bf1a9cf1b650bb0d94cd82`), and
  `block.md` itself, 101 lines, verified first.
- Every prepared file copied over its target: byte comparison equal before the commit and again
  from the committed bytes in gate 1.
- Append proof: `git show 4ae5d4d33:.agent/live_review.md` plus the bytes of
  `append-live_review.txt` equals the new file (`dry-live_review.md`): `True`.
- `git diff --cached --numstat` before each commit matched the block's cells exactly: C1 —
  `101 0` (the authored copy), `4 0` (the ledger), `7 5` (the plan); C2 — `7 0`
  (`tests/cli/test_exit_codes.py`).

## Deviations & assumptions

None. Every committed file in C1 and C2 is a byte copy of a reviewer-prepared file, verified equal
before staging and again from the committed bytes in gate 1. No code or record text was authored
by this worker. All five gates ran exactly once each, in the block's order, after C2 and before
C3; none was red, so the stop-and-report path never triggered. No mutation red-proof was run, the
full suite was not run (only the round's selection), `REMEDY_TEST_MAX_WORKERS` was never set, and
no two test commands ran at once. No commit exceeded the 500-insertion cap (C1's 101 insertions
from the authored block copy is the largest). Every commit ends with
`Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`, the model this worker runs on. The
helper script `verify_block.py`, `verify_prepared.py`, `check_c1_concat.py`,
`verify_c1_copies.py`, `verify_c2_copy.py` and `gate1_byte_compare.py` under
`.remedy-wt/f295-r15-worker/` did the digest checks, byte comparisons and the gate 1 proofs the
block's sandbox rules require; they are not committed (the directory is gitignored).

## Round verdicts

Rounds 1 to 5 and 7 to 13 PASS, rounds 6 and 14 FAIL, booked in the ledger (round 14 by this
round's C1); round 15's verdict, which also covers round 14's code, is the reviewer's to give and
book in the next round's first commit.

## For the operator, in plain sentences

Last round's change to the command that continues a stopped job was right, but one of Remedy's
own checks, which lists every way a command can end, did not yet know that this command can now
end the way `remedy job run` ends. That list is updated, and the tests pass again. Nothing waits
for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): not present during this round; if it appears, finish the commit
   in hand, write the handoff and stop.
2. Phase 1 rule 2: the Open PR Gate; no pull request is open for this branch yet.
3. Phase 1 rule 4: the reviewer reviews rounds 14 and 15 and books the verdict and the resolutions
   of R-1147 and R-1151 in the next round's first commit.
4. T003's last part: the hunk decision under `--json`.

Operator questions open: 0.
Open findings: 6 (R-1147 High and R-1151 Low, owned by F295, both repaired; R-1138, R-1139, R-1143
and R-1149 Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 (book round 14's FAIL, register R-1151, the plan) | done | `0e5652b5a` |
| C2 (`UNRESOLVED_SITES` gains a `job.resume` entry) | done | `4692b7d07` |
| Gate 1 (status and byte comparisons) | done | porcelain empty, four of four equal |
| Gate 2 (ruff) | done | `All checks passed!` |
| Gate 3 (selection) | done | `4444 passed, 3 skipped`, exit 0 |
| Gate 4 (integrity check) | done | `"fail_count": 1`, `high_blockers_open` naming R-1147 |
| Gate 5 (open finding ids) | done | `['R-1138', 'R-1139', 'R-1143', 'R-1147', 'R-1149', 'R-1151']` |
| C3 handback commit | done | this file |
| Push after C3 | pending | runs right after this commit, reported in the worker's final reply |

## Reviewer verdict on round 15 and the end of session 3, added after the handback

Written by the reviewer of F295's third session after it reviewed round 15, and applied by a
worker as this file's one later commit. Under operator amendment amend0827-process-diet rule 1
this committed and pushed handoff is the durable carrier of the verdict and of the three
paragraphs below; the next session does not review round 15 again, it books the texts and goes on.

THE SESSION ENDS HERE, after six delegated rounds, 10 to 15, inside the target of six to eight,
for two reasons: the next round needs fresh research — which command answers a hunk decision and
a patch intent under `--json`, and what the cockpit's door records for each — and this reviewer
left two gaps in its own blocks this session, R-1150 and R-1151, which is the signal the protocol
names for handing over. This sentence replaces the self-assessment above.

VERDICT ON ROUND 15: PASS, and with it the code of round 14. Every file C1 and C2 committed
equals the reviewer's prepared file under `.remedy-wt/f295-r15/`, four of four; the reviewer's
dry run of round 14's selection over `4ae5d4d33` with C2's file applied read green, and the
reviewer's own run in the primary checkout at `306a710e9` read `4444 passed, 3 skipped`.

THE TEXTS TO BOOK. The next round's FIRST commit appends to `.agent/live_review.md`, in this
order, each paragraph preceded by one blank line, exactly the three paragraphs between the marker
lines below (the marker lines themselves are not copied):

BEGIN-R15-BOOKING
Gate: F295 R15 — the F295 round 15 entry, R-1151's repair and the review of round 14's code, over `4ae5d4d33`..`306a710e9` (3 commits, each single-parent; insertions by `git show --numstat`: `0e5652b5a` 112, `4692b7d07` 7, `306a710e9` 97). VERDICT PASS, which also passes the code round 14 committed in `6f9f0a195`, `8838cb092` and `23af94e30`. Every file C1 and C2 committed equals the reviewer's prepared file under `.remedy-wt/f295-r15/`, four of four. `4692b7d07` gives `UNRESOLVED_SITES` in `tests/cli/test_exit_codes.py` a `job.resume` entry, `frozenset({0, 1, 2})`, for the serve supervisor's `follow_run` exit site that `remedy job resume` reaches through `_cmd_job_run`. Before delegating, the reviewer ran round 14's selection over `4ae5d4d33` with that file applied, in a disposable worktree, and read `4443 passed, 4 skipped`, the fourth skip being the UI toolchain a worktree lacks; the worker's one run in the primary checkout read `4444 passed, 3 skipped`, and so did the reviewer's own run there at `306a710e9`, because the records commit changed bytes the dry run did not hold. `remedy integrity check --json` read `"fail_count": 1`, the one failing check naming R-1147, which the next paragraph resolves. MUTATIONS of round 14's code in that worktree, over `tests/orchestration/test_resume_cli.py`, `tests/cli/test_decision_cmd.py` and `tests/cli/test_exit_codes.py`, the unmutated control `427 passed` before and after, seven of seven red: no job handed to `_cmd_job_run` 3, every job handed to it 12, the note never printed 1, the note for `--cycles` only 1, the progress line always on stdout 2, always on stderr 3, and `_cmd_job_run` called without the JSON flag 3. With the hand-off removed, the command-line test was stopped by its builder stand-in, so no model was called.

Done: R-1147 — RESOLVED at F295 R10 to R15, by `100548861` under DECISION F295 D9, by `62e622d24` and `5289f4303` under DECISION F295 D11, by `3aefba842` and `6ed8bd9cd` under DECISION F295 D12, and by `6f9f0a195` under DECISION F295 D13, proved by the reviewer's mutations recorded in the F295 R10, R12, R13 and R15 gate entries above. `remedy job resume` and the loop's resume refuse a job its budget stopped until its budget decision is answered, with exit 3, `budget_decision_open` and the decision's id; an answered `extend` lets the job resume, and an answered `abandon` cancels it so that nothing runs it again; and `remedy job resume` hands a job the ping-pong engine has run to `remedy job run`'s own handler, with the builder and the reviewer its record names, never to the local model the single pass builds with. `test_extend_then_resume_runs_the_job_through_its_own_providers` in `tests/cli/test_decision_cmd.py` resumes exactly the job R-1147 measured, through `apps.cli.grouped.main`, with a stand-in that fails the test if the local builder is ever built.

Done: R-1151 — RESOLVED at F295 R15 by `4692b7d07`, proved by the reviewer's dry run and by the worker's and the reviewer's runs recorded in the F295 R15 gate entry above, against the red reading at `4ae5d4d33` that R-1151 records. `UNRESOLVED_SITES` in `tests/cli/test_exit_codes.py` names the serve supervisor's exit site for `job.resume` as well as for `job.run`, with the reason that `remedy job resume` reaches it through `_cmd_job_run`, so `test_declared_codes_equal_the_codes_the_handler_reaches[job.resume]` passes and still compares the codes `job.resume` reaches with the `(0, 1, 2, 3)` it declares.
END-R15-BOOKING

THE NEXT ROUND, in order: (1) the booking above, with `.agent/plan.md` advanced, as its first
commit; after it `remedy integrity check --json` reads `"fail_count": 0` again. (2) T003's last
part, measured first: for every decision kind `list_decisions` in
`packages/orchestration/decision_queue.py` raises, which command answers it under `--json` —
the hunk decision of F033 and the patch intent first, the two the reviewer of session 2 found
answered "by other commands or by none" (DECISION F295 D8) — and whether that answer is recorded
the way the cockpit's write door records it; then a DECISION and the repair. (3) T004, the
contract page and the gate test; then the SLOW MODE hardening stage; then the closure.

LESSONS THIS SESSION TAUGHT ITS OWN BLOCKS, for the next reviewer: `tests/cli/test_exit_codes.py`
follows a handler's `apps.cli` imports into other commands' handlers, so a block that makes one
command call another's handler names that test and its `UNRESOLVED_SITES`; and
`tests/cli/test_decision_cmd.py` pins the exact set of refusal tokens `decision.py` passes to
`fail()`, so a block adding a refusal there names the pin.

FOR THE OPERATOR, IN PLAIN SENTENCES: this session made a stopped job behave properly for a
program that drives Remedy. When a job stops because it ran out of budget, Remedy no longer lets
it continue by accident; a person or a program can raise its budget or give it up with one
command; a job that was given up never runs again; and a job that continues uses the same AI
builder and reviewer it started with. Along the way it fixed a missing run record for every job
started by `remedy do`. Nothing waits for the operator.

Fortschritt: ~80 % (T001 and T002 landed · T003's stdin proof and the budget decision landed ·
T003's hunk decision and T004 open; then the hardening stage and the closure) — Schätzung.

Open findings after the booking: 4 (R-1138, R-1139, R-1143 and R-1149, Low, owned by F297; R-1147
and R-1151 resolved by the booking). Operator questions open: 0.
