# Handoff — F295 session 2, round 9: book round 8, repair R-1145, prove an unattended run never reads stdin (T003, DECISION F295 D8)

## Session

SESSION 2 of feature F295 · rounds 7 to 9 · rounds so far 9

Context self-assessment: "The reviewer's context is comfortable after three rounds; the session
continues."

Fortschritt: ~72 % (T001 and T002 landed · T003's stdin proof landed, review pending · T003's decision kinds and T004 open; then the hardening stage and the closure) — Schätzung

## Range

Review of `977e6e5e5`..`7d24833c8`, plus this handback commit.

## Commits

### af749f212 F295 R9 C1: book round 8, resolve R-1144, register R-1145, DECISION F295 D8, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f295-r9.md` | 122/0 (new) | byte copy of the round 9 block |
| `.agent/live_review.md` | 6/0 | append round 8's gate entry (PASS), the resolution of R-1144 and the registration of R-1145 as the reviewer prepared them |
| `.agent/decisions.md` | 10/0 | append DECISION F295 D8 |
| `.agent/plan.md` | 7/8 | rewrite to round 9's current step |

### 927d233d3 F295 R9 C2: a provider child reads end-of-file, never the caller's stdin (R-1145)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/exec_guard.py` | 3/0 | byte copy of the prepared file: the guarded spawn gives the child end-of-file as stdin |
| `packages/orchestration/stream_evidence.py` | 2/0 | byte copy of the prepared file: the streamed spawn gives the child end-of-file as stdin |

### ce552b87a F295 R9 C3: tests that both provider spawns ignore an open stdin pipe (R-1145)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_exec_guard.py` | 39/0 | byte copy of the prepared test file |
| `tests/orchestration/test_stream_evidence.py` | 39/0 | byte copy of the prepared test file |

### 7d24833c8 F295 R9 C4: an unattended run and the cost confirmation never read an open stdin pipe (T003)

| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_cost_preview_confirm.py` | 46/0 | byte copy of the prepared test file |
| `tests/cli/test_do_flags.py` | 38/0 | byte copy of the prepared test file |

### F295 R9 C5: handback (self-reference exception — committed by this same write)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file, rewritten in full per `docs/agents/handback_template.md` |

## External actions

None during the round before C5. After C5: `git push origin feature/f295-machine-client-contract-v1`;
its outcome is in the worker's final reply (write-once rule). No PR opened, no `gh` command.

## Verification

Gates ran once each, after C4 and before C5.

1. `git -C /home/decodeux/Repos/remedy status --porcelain` → empty output. Byte comparison of
   every file each of C1 to C4 wrote (`git show <commit>:<path>`) against its prepared file,
   ten of ten equal.
2. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r9/run.py /home/decodeux/Repos/remedy 5
   python3 -m ruff check packages/orchestration/exec_guard.py
   packages/orchestration/stream_evidence.py tests/orchestration/test_exec_guard.py
   tests/orchestration/test_stream_evidence.py tests/cli/test_cost_preview_confirm.py
   tests/cli/test_do_flags.py`
   ```
   exit 0
   All checks passed!
   ```
3. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r9/run_selection.py /home/decodeux/Repos/remedy`
   ```
   exit 0
   SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
   SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
   SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
   4134 passed, 3 skipped in 36.67s
   ```
   No FAILED, ERROR or `process(es) behind` line.
4. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r9/run.py /home/decodeux/Repos/remedy 3
   python3 -m apps.cli.main integrity check --json`
   ```
   exit 0
   {"check_count": 6, "checks": [{"message": "handlers=174", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
   ```
5. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r9/run.py /home/decodeux/Repos/remedy 3
   python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
   ```
   exit 0
   ['R-1138', 'R-1139', 'R-1143', 'R-1145']
   ```

## Authored-text proofs

- `block.md` → `.agent/authored/f295-r9.md`: 122 lines / 122 lines, sha256
  `ef8b6111cdd9fd810703c6bb3a9efc1eef239f8f8aebab8de4c3b5b7c26bdc2e` / same, byte comparison equal.
- Every prepared file copied over its target (`dry-live_review.md`, `dry-decisions.md`,
  `dry-plan.md`, `dry-exec_guard.py`, `dry-stream_evidence.py`, `dry-test_exec_guard.py`,
  `dry-test_stream_evidence.py`, `dry-test_cost_preview_confirm.py`, `dry-test_do_flags.py`):
  byte comparison equal, before the commit and again from the committed bytes in gate 1.
- Append proofs: `git show 977e6e5e5:.agent/live_review.md` plus the bytes of
  `append-live_review.txt` equals the new file: `True`; the same for `.agent/decisions.md` with
  `append-decisions.txt`: `True`.
- Every prepared file's sha256 was read with Python before use and matched the block's value.
- `git diff --cached --numstat` before each commit matched the block's cells: C1 `122 0`, `10 0`,
  `6 0`, `7 8`; C2 `3 0`, `2 0`; C3 `39 0`, `39 0`; C4 `46 0`, `38 0`.

## Round verdicts

Rounds 1 to 5, 7 and 8 PASS and round 6 FAIL, booked in the ledger (round 8 by this round's C1).
Round 9's verdict is the reviewer's to give and book in the next round's first commit.

## For the operator, in plain sentences

A program that starts Remedy and leaves its input channel open, without ever writing to it, can no
longer make Remedy wait. Remedy itself never asks a question in that case, and four new tests prove
it by starting real processes with such an open channel. The reviewer found that the processes
Remedy starts for the AI builder and reviewer used to inherit that channel and could have waited on
it until their time limit; they now get an empty input instead. Nothing waits for the operator.

## Deviations & assumptions

- Attribution line: every commit of this round closes with
  `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`, the model this worker runs on.
- Helper scripts `verify.py`, `stage.py` and `gate1.py` under `.remedy-wt/f295-r9-worker/` did the
  digest checks, copies, proofs and staging, as the block's sandbox rules require. They are not
  committed.
- No other departure from the block's commit sequence (C1 to C5, gates, push) or its constraints.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if present, write the handoff and stop.
2. Phase 1 rule 2: the Open PR Gate; no pull request is open for this branch yet.
3. Phase 1 rule 4: the reviewer reviews round 9 and books its verdict and the resolution of R-1145
   in the next round's first commit.
4. T003, second part: which command answers each decision kind under `--json`, the budget raise and
   the hunk decision first.

Operator questions open: 0.
Open findings: 4 (R-1145 Medium, owned by F295, repaired by this round; R-1138, R-1139 and R-1143 Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 (block copy, three record copies, append proofs, numstat) | done | `af749f212` |
| C2 (`exec_guard.py`, `stream_evidence.py`, R-1145 repair) | done | `927d233d3` |
| C3 (two spawn test files) | done | `ce552b87a` |
| C4 (two stdin-proof test files, T003) | done | `7d24833c8` |
| Gate 1 (status and byte comparisons) | done | porcelain empty, ten of ten equal |
| Gate 2 (ruff) | done | `All checks passed!` |
| Gate 3 (selection) | done | `4134 passed, 3 skipped`, exit 0 |
| Gate 4 (integrity check) | done | exit 0, `fail_count` 0 |
| Gate 5 (open finding ids) | done | `['R-1138', 'R-1139', 'R-1143', 'R-1145']` |
| C5 handback commit | done | this file |
| Push after C5 | pending | runs right after this commit, reported in the worker's final reply |

## Reviewer verdict on round 9 and the end of session 2, added after the handback

Written by the reviewer of F295's second session after it reviewed round 9, and applied by a
worker as this file's one later commit. Under operator amendment amend0827-process-diet rule 1
this committed and pushed handoff is the durable carrier of the verdict and the two finding drafts
below; the next session does not review round 9 again, it books the texts and goes on.

THE SESSION ENDS HERE, after three delegated rounds, below the floor of four, for this one reason:
the next round needs fresh research — which code path `remedy job resume` takes for a job its
budget stopped, and the design of the budget decision's answer — and this reviewer's context
already holds three rounds of dry runs, mutations and two probes, so a fresh session does that
research better. This sentence replaces the self-assessment above, which was written before the
probes.

VERDICT ON ROUND 9: PASS, verified by dry run, bytes identical. Every file C1 to C4 committed
equals the reviewer's prepared file under `.remedy-wt/f295-r9/` at the commit that wrote it, ten of
ten, and the four code and record files again at `0c3cdf9fd`; the reviewer's dry run used those
same bytes in a disposable worktree at the same base `977e6e5e5`.

THE TEXTS TO BOOK. The next round's FIRST commit appends to `.agent/live_review.md`, in this
order, each paragraph preceded by one blank line, exactly the four paragraphs between the marker
lines below (the marker lines themselves are not copied):

BEGIN-R9-BOOKING
Gate: F295 R9 — the F295 round 9 entry, R-1145's repair and T003's stdin proof, over `977e6e5e5`..`0c3cdf9fd` (5 commits, each single-parent; insertions by `git show --numstat`: `af749f212` 145, `927d233d3` 5, `ce552b87a` 78, `7d24833c8` 84, `0c3cdf9fd` 65). VERDICT PASS, verified by dry run, bytes identical: every file C1 to C4 committed equals the reviewer's prepared file under `.remedy-wt/f295-r9/` at the commit that wrote it, ten of ten, and the reviewer's dry run used those same bytes in a disposable worktree at the same base `977e6e5e5`. `927d233d3` gives the child of `run_guarded` and of `run_streamed_command` `stdin=subprocess.DEVNULL`; `ce552b87a` and `7d24833c8` add four tests, each starting a real process whose stdin is a pipe nobody writes to and nobody closes. The reviewer's dry run of the round's selection read `4133 passed, 4 skipped`, the extra skip being the vitest check a fresh worktree cannot run, and the worker's one run in the primary checkout read `4134 passed, 3 skipped`; `remedy integrity check --json` read `"fail_count": 0`. RED-PROOFS, in that worktree over the open-pipe tests of `tests/cli/test_do_flags.py`, `tests/cli/test_cost_preview_confirm.py`, `tests/orchestration/test_exec_guard.py` and `tests/orchestration/test_stream_evidence.py`, the unmutated control `5 passed` before and after, five of five red: the guarded child inheriting stdin 1, the streamed child inheriting stdin 1, the confirmation asking on a pipe 1, the confirmation ignoring `--yes` 1, and `remedy do` reading one line of stdin 1; the four that read the pipe blocked until their own timeout, which is the failure each of those tests exists to catch.

Done: R-1145 — RESOLVED at F295 R9 by `927d233d3` and `ce552b87a`, under DECISION F295 D8, proved by the reviewer's red-proofs recorded in the F295 R9 gate entry above. `run_guarded` in `packages/orchestration/exec_guard.py`, which runs the operator's `claude` command line for the builder and the reviewer, and `run_streamed_command` in `packages/orchestration/stream_evidence.py`, which runs the streaming provider, start their child with `stdin=subprocess.DEVNULL`, so a child reads end-of-file at once even when the client that started Remedy holds its stdin open as a pipe. `test_a_guarded_child_reads_end_of_file_while_the_callers_stdin_is_an_open_pipe` and `test_a_streamed_child_reads_end_of_file_while_the_callers_stdin_is_an_open_pipe` run exactly that caller.

- R-1146 — Medium, A JOB STOPPED BY ITS BUDGET RAISES A DECISION WITH THE OPTIONS `extend` AND `abandon` THAT NO COMMAND AND NO DOOR CAN ANSWER, WHILE TWO REFUSALS SEND THE OPERATOR TO EXACTLY THAT DECISION. Raised by the reviewer of F295's second session while measuring T003. SEARCHED BEFORE MINTING (checklist item 30): the open set at `0c3cdf9fd` is `['R-1138', 'R-1139', 'R-1143', 'R-1145']`, and none names a budget decision. MEASURED at `0c3cdf9fd` with `.remedy-wt/f295-r10/probe_stop.py`, on a scratch data root with the fake providers: a job planned by `remedy do <order> --plan-only` and run by `remedy job run <job> --deadline 2000-01-01T00:00:00+00:00` is listed by `remedy decision list <job> --json` and by the client digest with the decision `budget:budget_dd5d4ed727f982e2`, type `token_budget`, status `open`, options `extend` and `abandon`. Read in the code at `0c3cdf9fd`: `_cmd_decision_resolve` in `apps/cli/commands/decision.py` has no branch for a `budget:` id, so it answers `decision_not_resolvable`; the cockpit's `_answerable_by_decision_resolve` in `packages/orchestration/decision_inbox.py` reads it as not answerable; `run_job` in `packages/orchestration/pingpong_job.py` refuses new limits for a stopped job with "use the Decision workflow (extend/abandon)", and `remedy job budget <job> set max_cost_usd <value>` refuses with "a stopped job's limits change through its Decision". WHY MEDIUM: a job its budget stopped can never continue with a raised limit through any door that names the way, and the feature file names the budget raise as a decision a machine client must answer with `--json`. THE REPAIR is designed by the next round as a DECISION: answering `extend` with the raised limit and `abandon` from the command line under `--json`, recorded so that the decision reads resolved afterwards. Owner: F295. OPEN.

- R-1147 — High, `remedy job resume` RUNS A JOB ITS BUDGET STOPPED TO COMPLETION WHILE THE EXHAUSTED LIMIT STILL STANDS, THROUGH A PROVIDER OTHER THAN THE JOB'S OWN BUILDER, AND LEAVES THE BUDGET DECISION OPEN. Raised by the reviewer of F295's second session while measuring T003. SEARCHED BEFORE MINTING (checklist item 30): the open set at `0c3cdf9fd` is `['R-1138', 'R-1139', 'R-1143', 'R-1145']`, R-1146 is drafted beside this paragraph and names the missing answer, not the resume, and none names `job resume`. MEASURED at `0c3cdf9fd`, continuing the run R-1146 measures: `remedy job resume <job> --yes --json` exited 0 after 44.6 seconds, reported the job's one task `verified` with `remaining` 0 and `"model": "muse-glimmer:latest"`, a local model, while the job's `execution_config` names the builder `fake` with source `cli`; afterwards the job record reads `status` `completed`, its `budgets.deadline` still `2000-01-01T00:00:00Z`, and `remedy decision list` still lists the budget decision as `open`. NOT MEASURED: which code path `job resume` took, and whether a job stopped by its cost cap behaves the same. WHY HIGH: the per-job cost cap is the rule every machine order rests on (`docs/roadmap/design/luna-control-plane-v1.md`, rule 5), and the command line itself tells a client to run `remedy job resume <job> --json` after it answers a task decision, so this path is the client's. THE REPAIR: the next round reads the resume path, makes `job resume` honour a budget stop until its decision is answered and run the job's own providers, and pins both with a test that resumes a job stopped by its budget. Owner: F295. OPEN.
END-R9-BOOKING

THE NEXT ROUND, in order: (1) the booking above, with `.agent/plan.md` advanced, as its first
commit; (2) the reviewer reads `_cmd_job_resume` and the run path it calls, reproduces R-1147 with
`python3 -B .remedy-wt/f295-r10/probe_stop.py <tree> <scratch dir> --deadline
2000-01-01T00:00:00+00:00`, and writes DECISION F295 D9 for the budget decision's answer and the
resume guard; (3) the repair lands in small commits with red-proofs. `remedy integrity check
--json` reads one failing check once R-1147 is booked, `high_blockers_open`, until R-1147 is
resolved; a block that orders that gate expects it. Then T004, the hardening stage and the closure.

A SIDE EFFECT TO KNOW ABOUT: the reviewer's second probe made one call to the local model
`muse-glimmer:latest` on this machine, through the resume R-1147 describes, on a scratch data root
under `.remedy-wt/f295-r10/`. Nothing outside this machine was contacted and no repository but the
probe's scratch one was touched.

FOR THE OPERATOR, IN PLAIN SENTENCES, correcting the paragraph above: this session finished the
status reading for a program and proved that Remedy never waits on an open input channel. While
preparing the next step, the reviewer found two real problems with jobs that stop because they ran
out of budget. First, there is no command that lets anyone, person or program, say "give it more
budget" or "give up" for such a job, although Remedy's own messages point to exactly that choice.
Second, the command that continues a stopped job ran such a job to the end anyway, ignoring the
spent budget, and used a local AI model instead of the one the job was set up with. Both are the
next session's first work. The main line is not affected, and nothing waits for the operator.

Fortschritt: ~68 % (T001 and T002 landed · T003's stdin proof landed · R-1146 and R-1147 and the
budget answer open · T004 open; then the hardening stage and the closure) — Schätzung.

Open findings after the booking: 5 (R-1147 High and R-1146 Medium, owned by F295; R-1138, R-1139
and R-1143 Low, owned by F297; R-1145 resolved by the booking). Operator questions open: 0.
