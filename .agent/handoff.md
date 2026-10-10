# Handback — F302 round 5: book round 4, DECISION F302 D4, the Built State of T001 to T003, and T004 (`remedy stats calls`)

## Session

SESSION 1 of feature F302 · round 5 · rounds so far 5

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~80 % (T001 to T004 built · closure open) — Schätzung

## Range

Review of `5df8bc937`..`92e659575` (four commits on `feature/f302-claude-cli-tokens` — C1
`60144de92`, C2 `38568e5bc`, C3 `07c88ecdc`, C4 `92e659575` — plus this handback, C5).

## Commits

### `60144de92` F302 R5 C1: save the round 5 block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f302-r5.md` | 143/0 | NEW FILE — byte copy of `block.md` |

### `38568e5bc` F302 R5 C2: book round 4, a prose slip, DECISION F302 D4, the Built State of T001 to T003, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | 10/0 | appended `src/append-decisions.txt` — DECISION F302 D4 |
| `.agent/live_review.md` | 2/0 | appended `src/ledger-append.txt` — books round 4's PASS verdict |
| `.agent/plan.md` | 6/9 | replaced with `src/plan.md` |
| `.agent/prose_slips.md` | 1/0 | appended `src/prose_slips-append.txt` — a prose slip |
| `docs/roadmap/features/T3_F302.md` | 20/0 | appended `src/built-state.txt` — the Built State of T001 to T003 |

### `07c88ecdc` F302 R5 C3: remedy stats calls, tokens by kind per provider call and per landed change (T004, DECISION F302 D4)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/command_catalog_stats.py` | 22/0 | the `stats.calls` entry, under its own banner, between `stats.cache` and the cost report's banner |
| `apps/cli/commands/__init__.py` | 2/1 | `stats_calls_cmd` added to the import list (before `stats_ledger_cmd`) and to the end of the handler-collecting tuple |
| `apps/cli/commands/stats_calls_cmd.py` | 77/0 | NEW FILE — the `stats calls` handler |
| `packages/orchestration/call_tokens.py` | 143/0 | NEW FILE — `recorded_calls` and `summarize_call_tokens` |
| `tests/cli/test_stats_calls.py` | 109/0 | NEW FILE |
| `tests/orchestration/import_reachability_allowlist.txt` | 2/0 | `apps.cli.commands.stats_calls_cmd` and `packages.orchestration.call_tokens`, each at its sorted place |
| `tests/orchestration/test_call_tokens.py` | 132/0 | NEW FILE |

### `92e659575` F302 R5 C4: the claude-cli worker launch page reads the measurement and remedy stats calls

| Path | +/- | Reason |
|---|---|---|
| `docs/system/claude-cli-worker-launch-v1.md` | 21/4 | replaced with `code-claude-cli-worker-launch-v1.md` — banner changes, two sections added at the end |

### This commit — F302 R5 C5: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file |

## External actions

- `git -C /home/decodeux/Repos/remedy push origin feature/f302-claude-cli-tokens` — runs once after
  this commit, per the block's THEN step; reported in the worker's final reply only.
- No `gh` command ran this round. No merge, no branch creation, no force-push, no stash touched, no
  pull request opened.
- No worktree was added or removed by the worker. This round made no provider call and never
  started `claude`.

## Verification

**Opening block check** (before the block was read): a Python script read `block.md`'s own sha256
(`1cba36563a04aa8afc6b4d9404854fbabbc7f894baae7f54c8e47f422ae77a51`) and line count (143) — both
equal the harness's stated values.

**Pre-state / C0** (before any write): `git rev-parse HEAD` read
`5df8bc9379b9b2ea8b263f1c8166fcc56b6e0e90`; `git branch --show-current` read
`feature/f302-claude-cli-tokens`; `git status --porcelain` empty; `.agent/STOP` absent.
`git branch --show-current` was re-checked immediately before every one of the four commits C1-C4
and read `feature/f302-claude-cli-tokens` each time.

**Gate 1** (after C0, before C1 — every line of `digests.txt` against the file it names, one Python
script): 18 of 18 comparisons `True` (`block.md`, the five `src/` files, the three `sim-*` files,
`selection.txt`, and the seven `code-*` files). `ALL_TRUE: True`.

**C1's byte proof** (reported at copy time): `.agent/authored/f302-r5.md` sha256
`1cba36563a04aa8afc6b4d9404854fbabbc7f894baae7f54c8e47f422ae77a51`, 143 lines — equal to `block.md`'s
own.

**C2's byte proofs** (before commit, by a separate read-only script, after a separate one-time
append/copy script): each of the four appended files (`live_review.md`, `prose_slips.md`,
`decisions.md`, `T3_F302.md`) equals `git show 5df8bc937:<path>` followed by its slice, `True` ×4;
`live_review.md`, `prose_slips.md` and `T3_F302.md` also equal `sim-live_review.md`,
`sim-prose_slips.md` and `sim-T3_F302.md`, `True` ×3; `.agent/plan.md` equals `src/plan.md`, `True`.
Eight of eight `True`. `git diff --cached --numstat`: `.agent/decisions.md` 10/0,
`.agent/live_review.md` 2/0, `.agent/plan.md` 6/9, `.agent/prose_slips.md` 1/0,
`docs/roadmap/features/T3_F302.md` 20/0.

**C3's byte proofs** (before commit): all seven paths equal their prepared `code-*` file, `True` ×7.
`git diff --cached --numstat`: `apps/cli/command_catalog_stats.py` 22/0,
`apps/cli/commands/__init__.py` 2/1, `apps/cli/commands/stats_calls_cmd.py` 77/0,
`packages/orchestration/call_tokens.py` 143/0, `tests/cli/test_stats_calls.py` 109/0,
`tests/orchestration/import_reachability_allowlist.txt` 2/0,
`tests/orchestration/test_call_tokens.py` 132/0.

**C3's read-back checks**, before commit: `apps/cli/commands/__init__.py` carries `stats_calls_cmd`
in its import list immediately before `stats_ledger_cmd`, and at the end of the tuple passed to
`table.update(...)`, nothing else changed; `apps/cli/command_catalog_stats.py` carries the
`stats.calls` `CommandEntry` under its own banner comment, between the `stats.cache` entry and the
`# ── stats — the cost report (F115) ──` banner; `tests/orchestration/import_reachability_allowlist.txt`
carries `apps.cli.commands.stats_calls_cmd` and `packages.orchestration.call_tokens`, each sorted
within its own block of same-prefix entries. All held.

**C4's byte proof** (before commit): `docs/system/claude-cli-worker-launch-v1.md` equals
`code-claude-cli-worker-launch-v1.md`, `True`. `git diff --cached --numstat`:
`docs/system/claude-cli-worker-launch-v1.md` 21/4.

**Gate 2** (after C4): `git -C /home/decodeux/Repos/remedy status --porcelain` empty, `True`. The
byte proofs of C2 step 2 (8), C3 step 3 (7) and C4 (1), re-run at this commit: 16 of 16 `True`.

**Gate 3** (the round's one test selection, run once, after C4, by a Python script whose
`subprocess.run` named `cwd="/home/decodeux/Repos/remedy"`):
```
python3 -m pytest -q -rfEs @/home/decodeux/Repos/remedy/.remedy-wt/f302-r5/selection.txt
```
Exit 0. `8237 passed, 9 skipped in 669.43s (0:11:09)`. No `FAILED` or `ERROR` line. The nine SKIPPED
lines:
```
SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:383: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:392: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:399: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
```

**Gate 4** (two saved scripts, each `subprocess.run` with explicit `cwd`):
```
python3 -m ruff check packages/orchestration/call_tokens.py apps/cli/commands/stats_calls_cmd.py apps/cli/commands/__init__.py apps/cli/command_catalog_stats.py tests/orchestration/test_call_tokens.py tests/cli/test_stats_calls.py
```
Exit 0: `All checks passed!`
```
python3 -m apps.cli.main integrity check --json
```
Exit 0:
```
{"check_count": 6, "checks": [{"message": "handlers=183", "name": "handler_import", "status":
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

## Authored-text proofs

`.agent/authored/f302-r5.md` = `block.md` (sha256 and line count both equal, proven in C1). The four
C2 appends (`src/ledger-append.txt`, `src/prose_slips-append.txt`, `src/append-decisions.txt`,
`src/built-state.txt`) each applied by byte append and proven equal to `git show 5df8bc937:<path>`
followed by the slice, and three of them also proven equal to the reviewer's own simulation
(`sim-live_review.md`, `sim-prose_slips.md`, `sim-T3_F302.md`); `.agent/plan.md` applied by a plain
file copy of `src/plan.md` and proven byte-equal. `docs/system/claude-cli-worker-launch-v1.md`
applied by a plain file copy of `code-claude-cli-worker-launch-v1.md` and proven byte-equal. C3's
seven paths are code and test source, not reviewer-authored prose text; they were applied by plain
file copy from their prepared `code-*` files and proven byte-equal in Verification, but carry no
separate authored-text (fidelity-protocol) obligation. No other reviewer-authored text carried a
separate obligation this round.

## Deviations & assumptions

- Gate 2's re-check of C4's byte proof was first run by re-invoking `c4_copy.py`, the same script
  that performed C4's one-time copy (it both copies with `shutil.copyfile` and prints the equality
  result), instead of a script that only reads. This re-executed the copy a second time; the bytes
  copied were identical both times (the source file had not changed), so nothing on disk changed and
  no incorrect content was ever written, but it is a literal breach of the rule that "a script that
  copies or appends runs once; every later proof uses a script that only reads." A separate read-only
  script (`c4_proof_readonly.py`) was then written and used for the authoritative Gate 2 re-check
  reported above; `c4_copy.py` was not invoked again after that.
- Otherwise: C0 through C4 ran in the block's exact order, each exactly once; `git branch
  --show-current` was checked before every commit and read `feature/f302-claude-cli-tokens` each
  time; every other append/copy script ran exactly once and every later proof used a separate
  read-only script; gate 3 was the round's only pytest invocation, run once, with no
  `REMEDY_TEST_MAX_WORKERS` set and no `-n` passed, and no test command ran concurrently with
  another; no provider call was made and `claude` was never started, by any means; `.agent/decisions.md`
  was never read whole by the worker (only appended to, and compared for equality, by Python
  scripts whose output was a boolean, never its content); no file under `.remedy-wt/f302-r5/` was
  modified; no mutation outside the paths each commit named; no stash entry touched, no branch other
  than the existing one created, no worktree added or removed by the worker, nothing merged, no
  force-push; `.agent/STOP` did not appear at any point; commit subjects carry no leading-slash token
  and no absolute path; no new line under `apps/`, `packages/`, `scripts/`, `tests/` or `docs/`
  carries the letters `promot`; no `cd` was used and every shell call was one plain command.

This section says nothing about this commit's own self-review, per the block; that is reported in
the worker's final reply only.

## Round verdicts

F302's round 4 PASS verdict is booked by C2 (carried forward via the appended
`.agent/live_review.md`). Round 5's verdict is the reviewer's, to be written after this handback.

## For the operator, in plain sentences

The cut is measured and kept: a small question now reads about 7,000 tokens before it is answered
instead of 21,500 to 28,000, and a real small repair job passed its review with the same change both
ways while its builder's first call read about 435,000 tokens instead of about 726,000. A new
command, `remedy stats calls`, now shows for each kind of worker how many tokens one call reads and
writes of each kind, and how many tokens one change that reached its repository cost. The next
rounds close the feature; nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. Rule 2 (Open PR Gate).
3. Book round 5's verdict in the next round's first commit.
4. The closure sequence.

Operator questions open: 0.
Open findings: 16 (R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176,
R-1196, R-1219, R-1220, R-1225, R-1230 and R-1235, Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0: base and branch | done | preconditions confirmed; HEAD `5df8bc937`, branch `feature/f302-claude-cli-tokens` |
| C1: save the round 5 block | done | byte proof `True`; committed `60144de92` |
| C2: book round 4, a prose slip, DECISION F302 D4, the Built State of T001 to T003, the plan | done | byte proofs `True`, 8 of 8; committed `38568e5bc` |
| C3: remedy stats calls (T004, DECISION F302 D4) | done | byte proofs `True`, 7 of 7; read-back checks held; committed `07c88ecdc` |
| C4: the claude-cli worker launch page reads the measurement and remedy stats calls | done | byte proof `True`; committed `92e659575` |
| Gate 1 | passed | 18 of 18 digest comparisons `True` |
| Gate 2 | passed | status clean; 16 of 16 byte proofs `True` |
| Gate 3 | passed | `8237 passed, 9 skipped` in `669.43s`, exit 0; no FAILED/ERROR |
| Gate 4 | passed | ruff `All checks passed!`; six integrity checks `pass`, `fail_count 0` |
| Gate 5 | passed | open findings list matches exactly |
| Push | pending | reported in the worker's final reply |
