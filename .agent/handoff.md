# Handback — F302 round 4: book round 3, R-1235 with DECISION F302 D3, the page's banner, and T003's measurement

## Session

SESSION 1 of feature F302 · round 4 · rounds so far 4

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~65 % (claim, T001, T002, T003's cut and measurement · T004 open) — Schätzung

## Range

Review of `8255e40d4`..`8d53855ca` (four commits on `feature/f302-claude-cli-tokens` — C1
`f777e99a9`, C2 `204d3c1a5`, C3 `fd845b178`, C4 `8d53855ca` — plus this handback, C5).

## Commits

### `f777e99a9` F302 R4 C1: save the round 4 block and the measurement script

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f302-r4-measure.py` | 270/0 | NEW FILE — byte copy of the prepared `f302-r4-measure.py` (T003's measurement script, C4's own order) |
| `.agent/authored/f302-r4.md` | 152/0 | NEW FILE — byte copy of `block.md` |

### `204d3c1a5` F302 R4 C2: book round 3, R-1235, a prose slip, DECISION F302 D3, the feature file, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | 10/0 | appended `src/append-decisions.txt` — DECISION F302 D3 |
| `.agent/live_review.md` | 4/0 | appended `src/ledger-append.txt` — books round 3's PASS verdict and registers R-1235 (owned by F297) |
| `.agent/plan.md` | 12/16 | replaced with `src/plan.md` |
| `.agent/prose_slips.md` | 1/0 | appended `src/prose_slips-append.txt` — a prose slip |
| `docs/roadmap/features/T3_F302.md` | 6/0 | appended `src/feature-amendment.txt` — the DECISION F302 D3 amendment |

### `fd845b178` F302 R4 C3: the claude-cli worker launch page's banner after DECISION F302 D3

| Path | +/- | Reason |
|---|---|---|
| `docs/system/claude-cli-worker-launch-v1.md` | 3/3 | replaced with `code-claude-cli-worker-launch-v1.md` — only the banner changes |

### `8d53855ca` F302 R4 C4: T003's readings, the fixed question and one real task before and after the cut

| Path | +/- | Reason |
|---|---|---|
| `.agent/f302_after.jsonl` | 10/0 | NEW FILE — byte copy of the measurement script's own `f302_after.jsonl`, written to `.remedy-wt/f302-r4-out` by its one run |
| `.agent/f302_after.md` | 38/0 | NEW FILE — byte copy of the measurement script's own `f302_after.md`, written to `.remedy-wt/f302-r4-out` by its one run |

### This commit — F302 R4 C5: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file |

## External actions

- `git -C /home/decodeux/Repos/remedy push origin feature/f302-claude-cli-tokens` — runs once after
  this commit, per the block's THEN step; reported in the worker's final reply only.
- No `gh` command ran this round. No merge, no branch creation, no force-push, no stash touched, no
  pull request opened.
- No worktree was added or removed by the worker. T003's measurement script's own run created and
  used its own self-use job worktrees and branches under `.remedy-wt/job-*` (as every self-use job
  does) and a scratch repo under its `--work` tree; the block orders these left alone, and they were
  left alone. `.remedy-wt/f302-r4-work` (the script's own `--work` tree) no longer exists after the
  run — the script removed it itself; this was confirmed, not caused, by the worker (gate 6).

## Verification

**Opening block check** (before the block was read): a Python script read `block.md`'s own sha256
(`bddbc57c43fdcc0436da7a1de052de6ef5b11af72bbb22b0165267cffcced20d`) and line count (152) — both
equal the harness's stated values.

**Pre-state / C0** (before any write): `git rev-parse HEAD` read
`8255e40d4a5ca73ae3e5b1b2a9137510b4d612f7`; `git branch --show-current` read
`feature/f302-claude-cli-tokens`; `git status --porcelain` empty; `.agent/STOP` absent;
`.remedy-wt/f302-r4-work` did not exist. `git branch --show-current` was re-checked immediately
before every one of the four commits C1-C4 and read `feature/f302-claude-cli-tokens` each time.

**Gate 1** (after C0, before C1 — every line of `digests.txt` against the file it names, one Python
script): 12 of 12 comparisons `True` (`block.md`, `f302-r4-measure.py`, the five `src/` files, the
three `sim-*` files, `code-claude-cli-worker-launch-v1.md` and `selection.txt`). `ALL_TRUE: True`.

**C1's byte proof** (reported at copy time): `.agent/authored/f302-r4.md` sha256
`bddbc57c43fdcc0436da7a1de052de6ef5b11af72bbb22b0165267cffcced20d`, 152 lines; `f302-r4-measure.py`
sha256 `2a56dd17b5d2fb92cec409b7d5456631e8ede0f6e1b83a7525e21ef20ce8418e`, 270 lines — both equal
their prepared file's own.

**C2's byte proofs** (before commit, by a separate read-only script, after a separate one-time
append/copy script): each of the four appended files (`live_review.md`, `prose_slips.md`,
`decisions.md`, `T3_F302.md`) equals `git show 8255e40d4:<path>` followed by its slice, `True` ×4;
`live_review.md`, `prose_slips.md` and `T3_F302.md` also equal `sim-live_review.md`,
`sim-prose_slips.md` and `sim-T3_F302.md`, `True` ×3; `.agent/plan.md` equals `src/plan.md`,
`True`. Eight of eight `True`. `git diff --cached --numstat`: `.agent/decisions.md` 10/0,
`.agent/live_review.md` 4/0, `.agent/plan.md` 12/16, `.agent/prose_slips.md` 1/0,
`docs/roadmap/features/T3_F302.md` 6/0.

**C3's byte proof** (before commit): `docs/system/claude-cli-worker-launch-v1.md` equals
`code-claude-cli-worker-launch-v1.md`, `True`. `git diff --cached --numstat`:
`docs/system/claude-cli-worker-launch-v1.md` 3/3.

**Gate 2** (after C3): `git -C /home/decodeux/Repos/remedy status --porcelain` empty, `True`. The
byte proofs of C2 step 2 (8) and C3 (1), re-run at this commit by a fresh read-only Python script:
9 of 9 `True`.

**Gate 3** (the round's one test selection, run once, after C3 and before C4, by a Python script
whose `subprocess.run` named `cwd="/home/decodeux/Repos/remedy"`):
```
python3 -m pytest -q -rfEs @/home/decodeux/Repos/remedy/.remedy-wt/f302-r4/selection.txt
```
Exit 0. `3966 passed, 3 skipped in 205.08s (0:03:25)`. No `FAILED` or `ERROR` line. The three
SKIPPED lines:
```
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
```

**Gate 4** (one saved script, `subprocess.run` with explicit `cwd`, printing the exit code):
```
python3 -m apps.cli.main integrity check --json
```
Exit 0:
```
{"check_count": 6, "checks": [{"message": "handlers=182", "name": "handler_import", "status":
"pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"},
{"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"},
{"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message":
"no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status":
"pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status":
"pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
Six of six checks `pass`, `fail_count 0`.

**Gate 5** (one saved script, explicit `cwd`):
```
python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"
```
Exit 0:
```
['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1162', 'R-1172', 'R-1176',
'R-1196', 'R-1219', 'R-1220', 'R-1225', 'R-1230', 'R-1235']
```
Matches the block's ordered list exactly.

**C4's run** (T003's measurement, the one place `claude` starts this round): a Python wrapper under
the worker folder (`c4_runner.py`) created `.remedy-wt/f302-r4-out`, then ran, once, with
`cwd="/home/decodeux/Repos/remedy"` and an internal `subprocess.run` timeout of 5400s (90 minutes,
≥ the ordered 60-minute floor):
```
python3 -B /home/decodeux/Repos/remedy/.agent/authored/f302-r4-measure.py run --out /home/decodeux/Repos/remedy/.remedy-wt/f302-r4-out --work /home/decodeux/Repos/remedy/.remedy-wt/f302-r4-work --remedy-rev 8255e40d4
```
No `--skip-jobs` was passed. Exit 0. The run's actual wall time was ~557s (9m17s). Its whole
captured stdout+stderr (9 lines):
```
question scratch before 0 3 5 21530 0
question scratch after 0 3 5 1689 5359
question remedy before 0 3 5 15192 12861
question remedy after 0 3 5 1207 6197
job before {"exit_code": 0, "entry": "SU-054", "title": "Narrow the excused handler at apps/cli/commands/job.py:1818", "job_id": "288b02c4836542ca", "state": "completed", "error": "", "stop_reason": "", "provider_call_count": 2, "tasks": [{"task_id": "T001", "status": "applied_to_job_workspace", "verdict": "pass", "final_status": "staged_review_passed", "run_id": "da017de615ce4821"}]}
job after {"exit_code": 0, "entry": "SU-054", "title": "Narrow the excused handler at apps/cli/commands/job.py:1818", "job_id": "7ce423fd67604240", "state": "completed", "error": "", "stop_reason": "", "provider_call_count": 2, "tasks": [{"task_id": "T001", "status": "applied_to_job_workspace", "verdict": "pass", "final_status": "staged_review_passed", "run_id": "1c9c87f3a3794fb9"}]}
provider calls read: 8
rendered 10 rows
```
`f302_after.jsonl` was present after the run (10 rows); `f302_after.md` was present too (38 lines).

**C4's copies and proofs**: `.agent/f302_after.jsonl` and `.agent/f302_after.md` copied byte-for-byte
from `.remedy-wt/f302-r4-out`; each copy proven equal to its source, `True` ×2.

**Gate 6** (after C4's copies, before its commit): `git worktree list` named no path under
`.remedy-wt/f302-r4-work`; that folder did not exist (the script's own run removed it); `git status
--porcelain` listed exactly the two copied files among C4's two paths, each `??`. All held.

## Authored-text proofs

`.agent/authored/f302-r4.md` = `block.md` and `.agent/authored/f302-r4-measure.py` =
`f302-r4-measure.py` (sha256 and line count both equal, proven in C1). The four C2 appends
(`src/ledger-append.txt`, `src/prose_slips-append.txt`, `src/append-decisions.txt`,
`src/feature-amendment.txt`) each applied by byte append and proven equal to `git show
8255e40d4:<path>` followed by the slice, and three of them also proven equal to the reviewer's own
simulation (`sim-live_review.md`, `sim-prose_slips.md`, `sim-T3_F302.md`); `.agent/plan.md` applied
by a plain file copy of `src/plan.md` and proven byte-equal. `docs/system/claude-cli-worker-launch-v1.md`
applied by a plain file copy of `code-claude-cli-worker-launch-v1.md` and proven byte-equal. C4's two
files are not reviewer-authored text — they are the measurement script's own writes, copied verbatim
from `.remedy-wt/f302-r4-out` and proven byte-equal to that source; no separate authored-text
obligation applies to them. No other reviewer-authored text carried a separate obligation this
round.

## Deviations & assumptions

- One Bash call during C4 preparation, checking whether `.remedy-wt/f302-r4-out` and
  `.remedy-wt/f302-r4-work` existed yet, was run as
  `ls /home/decodeux/Repos/remedy/.remedy-wt/f302-r4-out 2>&1; ls /home/decodeux/Repos/remedy/.remedy-wt/f302-r4-work 2>&1`
  — two commands joined by `;`, which the block's constraints forbid even for a read-only check. It
  ran before any write, was read-only, and both paths were independently reconfirmed absent/created
  as expected by later Python scripts (`c0_check.py` before, `c4_poll.py`/gate 6 after); nothing
  turned on the joined form. It was not repeated; every other existence check this round used either
  a single plain `ls` call or a Python script.
- C4's ordered form ("Run, ONCE, from a Python wrapper... with... a timeout of at least sixty
  minutes") was satisfied by a wrapper (`c4_runner.py`) that creates the out folder, then calls
  `subprocess.run` once with `cwd="/home/decodeux/Repos/remedy"` and `timeout=5400`, writing the
  exit code and whole output to files in the worker folder — exactly as ordered. That wrapper was
  itself started by a second, thin script (`c4_launch.py`) using `subprocess.Popen(...,
  start_new_session=True)` so the measurement run continued independently of the single Bash tool
  call that launched it, which only waits up to 3,600,000 ms; the worker then polled
  (`c4_poll.py`, read-only, no re-run, no edit of the script's own writes) until the wrapper's own
  `done` marker appeared. This is an extra layer around the ordered wrapper, added only to avoid the
  risk of the harness's own per-call ceiling cutting off the one permitted `claude` run partway
  through; the measurement script itself still ran exactly once, with no `--skip-jobs`, and was
  never re-run or edited. The run finished in ~557s, well inside both the wrapper's internal timeout
  and the harness's per-call ceiling, so the extra layer was not actually needed in the event, but it
  was in place before the run started.
- Otherwise: C0 through C4 ran in the block's exact order, each exactly once; `git branch
  --show-current` was checked before every commit and read `feature/f302-claude-cli-tokens` each
  time; every append/copy script ran exactly once and every later proof used a separate read-only
  script, as the block required; gate 3 was the round's only pytest invocation, run once, with no
  `REMEDY_TEST_MAX_WORKERS` set and no `-n` passed, and no test command ran concurrently with
  another; `claude` was started exactly once this round, only by T003's measurement script, through
  Remedy's own provider path, with no `--skip-jobs`, and was never started any other way; no file
  under `.remedy-wt/f302-r4/` was modified; no mutation outside the paths each commit named; no
  stash entry touched, no branch other than the existing one created, no worktree added or removed
  by the worker, nothing merged, no force-push; `.agent/STOP` did not appear at any point; commit
  subjects carry no leading-slash token and no absolute path; no new line under `apps/`, `packages/`,
  `scripts/`, `tests/` or `docs/` carries the letters `promot`.

This section says nothing about this commit's own self-review, per the block; that is reported in
the worker's final reply only.

## Round verdicts

F302's round 3 PASS verdict is booked by C2 (carried forward via the appended
`.agent/live_review.md`, which also registers R-1235). Round 4's verdict is the reviewer's, to be
written after this handback.

## For the operator, in plain sentences

One promised part of this round is moved to the next cleanup feature, because every file that would
have to record it may not grow under the size rule: a job does not yet write down which of the two
settings its worker started with. This round measured the cut instead: the same small question was
asked once with the old start and once with the new one, and one small real repair job was run
twice, once each way. The numbers are in the file this round committed. The next round writes them
into the feature's record and keeps the cut only if the real job still passed its review. Nothing
waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. Rule 2 (Open PR Gate).
3. Book round 4's verdict in the next round's first commit.
4. T003's Built State from the readings, then T004: tokens by kind in `remedy stats`.

Operator questions open: 0.
Open findings: 16 (R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176,
R-1196, R-1219, R-1220, R-1225, R-1230 and R-1235, Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0: base and branch | done | preconditions confirmed; HEAD `8255e40d4`, branch `feature/f302-claude-cli-tokens` |
| C1: save the round 4 block and the measurement script | done | byte proofs `True` ×2; committed `f777e99a9` |
| C2: book round 3, R-1235, a prose slip, DECISION F302 D3, the feature file, the plan | done | byte proofs `True`, 8 of 8; committed `204d3c1a5` |
| C3: the claude-cli worker launch page's banner | done | byte proof `True`; committed `fd845b178` |
| C4: T003's readings, the fixed question and one real task before and after the cut | done | exit 0; `f302_after.jsonl`/`.md` present; copies proven `True` ×2; committed `8d53855ca` |
| Gate 1 | passed | 12 of 12 digest comparisons `True` |
| Gate 2 | passed | status clean; 9 of 9 byte proofs `True` |
| Gate 3 | passed | `3966 passed, 3 skipped` in `205.08s`, exit 0; no FAILED/ERROR |
| Gate 4 | passed | six integrity checks `pass`, `fail_count 0` |
| Gate 5 | passed | open findings list matches exactly |
| Gate 6 | passed | no worktree/folder under `f302-r4-work`; status shows exactly the two C4 paths, `??` |
| Push | pending | reported in the worker's final reply |
