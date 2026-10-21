# Handback — F311 round 2

## Session

SESSION 1 of feature F311 · round 2

Context self-assessment: this session verified every prepared file's digest before using it,
executed C1 to C4 exactly as the block ordered, found one gate-1 line unfixable without an
amend or rebase the block forbids (declared below, not a stop condition), and gates 2 to 5 each
passed on their first run.

Fortschritt: ~45 % (pulse, reader and stall reading landed · twins and routes open) — Schätzung

## Range

Review of `4ed1b3dee70eac63f4b1f5c4607a252934cb7da3`..HEAD (C1 to C4 below, then this commit,
C5, which also carries this handback).

## Commits

### b78128011 F311 R2 C1: book round 1, register R-1383, the D3 addendum, the plan
242 insertions, 13 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f311-r2.md` | +218 (new file) | byte copy of `block.md` |
| `.agent/decisions.md` | +8 | byte copy appending DECISION F311 D3's addendum |
| `.agent/live_review.md` | +4 | byte copy booking round 1's PASS verdict and registering R-1383 |
| `.agent/plan.md` | +11/-13 | byte copy rewritten for round 2 |
| `.agent/prose_slips.md` | +1 | byte copy appending one line |

### ce81ee7dd F311 R2 C2: the story's open decision and the worked seconds become public (structure step)
8 insertions, 6 deletions.

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/budget_stop.py` | +3/-2 | `_work_seconds` renamed `budget_work_seconds`, one WHY line, its caller re-pointed |
| `packages/orchestration/client_diff.py` | +2/-2 | its import and call re-pointed to `job_story_open_decision` |
| `packages/orchestration/client_story.py` | +3/-2 | `_open_decision` renamed `job_story_open_decision`, one WHY line, its caller re-pointed |

### 105378025 F311 R2 C3: the reader of now and insight, the stall reading and the model server
343 insertions, 2 deletions.

| Path | +/- | Reason |
|---|---|---|
| `docs/guides/environment.md` | +1 | byte copy registering `insight.stall_seconds` |
| `packages/orchestration/config_keys_ui.py` | +17/-2 | byte copy adding the `insight.stall_seconds` `ConfigKeySpec` |
| `packages/orchestration/job_insight.py` | +323 (new file) | `job_insight_entry`, `insight_advice`, `job_insight`, `now_insight`, `model_server_state`, `fetch_ollama_json`, `insight_stall_seconds` and the vocabulary constants (DECISIONs F311 D1, D3 and its addendum, D4) |
| `tests/test_no_orphan_modules.py` | +2 | `ALLOWED_UNWIRED` entry for `job_insight.py` |

### 1c83f4e93 F311 R2 C4: the reader, the stall reading, the probe and R-1383, tested
352 insertions, 2 deletions.

| Path | +/- | Reason |
|---|---|---|
| `tests/conftest.py` | +12/-2 | `_no_live_pi_reach` also replaces `job_insight.fetch_ollama_json`, hand-saved and restored |
| `tests/orchestration/test_job_insight.py` | +317 (new file) | every phase word, every stall reason but `waiting_lock` with their advice, the threshold and its env var, the lines clamp, `model_server_state`'s three shapes, `now_insight`'s order filter, redaction, the answer keys |
| `tests/orchestration/test_worker_pulse.py` | +23 | R-1383: `bind_job_clock` binds a fresh pulse for a job with an id |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` at this round's start:
`[]`, no open PR — the Open PR Gate passes trivially. No other `gh` command this round. No
worktree add/remove of my own. The push is ordered to run after this commit, so its outcome is
reported in the final reply only; no pull request is opened (forbidden this round).

## Verification

Gates run once each, after C4 and before this commit.

1. `git status --porcelain` → empty. Then
   `python3 .remedy-wt/f311-r2/prep/verify.py .`:
   ```
   True	b78128011 single parent equal to the commit before it
   True	ce81ee7dd single parent equal to the commit before it
   True	105378025 single parent equal to the commit before it
   True	1c83f4e93 single parent equal to the commit before it
   True	every commit carries an F311 R2 Cn subject: 4 of 4
   True	C1 paths exactly [...]: [same]
   True	C2 paths exactly its set: [same]
   True	C3 paths exactly its set: [same]
   True	C4 paths all under tests/: [...]
   absent	C5
   True	C1 .agent/authored/f311-r2.md equals block.md
   True	C1 .agent/live_review.md equals dry-live_review.md
   True	C1 .agent/decisions.md equals dry-decisions.md
   True	C1 .agent/prose_slips.md equals dry-prose_slips.md
   True	C1 .agent/plan.md equals dry-plan.md
   True	C2 client_story names only job_story_open_decision
   True	C2 client_diff re-pointed
   True	C2 budget_stop names only budget_work_seconds
   True	C2 client_diff.py differs from the base only by the rename and its WHY line
   True	C2 budget_stop.py differs from the base only by the rename and its WHY line
   True	C2 client_story.py differs from the base only by the rename and its WHY line
   True	C3 config_keys_ui.py equals dry-config_keys_ui.py
   True	C3 environment.md equals dry-environment.md
   True	C3 job_insight.py holds every named def and constant (14 checks)
   False	C3 job_insight.py has one network read
   True	C3 the unwired list names job_insight.py
   True	pingpong_job.py, pingpong_loop.py, pingpong_provider.py, config.py, stream_evidence.py byte-identical to the base
   True	apps/ untouched
   True	C4 touches test_job_insight.py, conftest.py, test_worker_pulse.py
   ALL False
   ```
   The one `False` line is explained in Deviations below; nothing else in this round's own
   self-check failed.
2. `python3 -m ruff check` over every Python file C2, C3 and C4 touched (`budget_stop.py`,
   `client_diff.py`, `client_story.py`, `job_insight.py`, `config_keys_ui.py`,
   `test_no_orphan_modules.py`, `conftest.py`, `test_worker_pulse.py`, `test_job_insight.py`) →
   `All checks passed!`
3. `python3 .remedy-wt/f311-r2/prep/run_selection.py . .remedy-wt/f311-r2-worker/selection-output.txt`:
   ```
   paths 94
   exit 0
   4142 passed, 2 skipped in 57.20s
   SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
   SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
   ```
   No `FAILED` or `ERROR` line, no `process(es) behind` line.
4. `python3 -m apps.cli.main integrity check --json` → exit 1, `fail_count` 1:
   ```
   {"check_count": 6, "checks": [..., {"message": "12 open blocker/high: R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362", "name": "high_blockers_open", "status": "fail"}], "error": "integrity_failed", "fail_count": 1, "message": "integrity gate failed with 1 failing check(s)", "ok": false, "passed": false, "schema_version": 1, "version": 1}
   ```
   The one failing check is `high_blockers_open`, naming exactly the twelve ids of DECISION
   F310 D7 that remain open and no other.
5. `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`
   → `88`, the rule `open_finding_ids` applies (every `^- R-\d+ — ` paragraph minus every
   `^Done: R-\d+ — ` line), measured at `1c83f4e93` (this round's C4, before this commit): one
   more than round 1's 87, the one new registration this round made (R-1383), and resolved none.

## Authored-text proofs

C1's five byte copies (`.agent/authored/f311-r2.md` ← `block.md`; `.agent/live_review.md` ←
`dry-live_review.md`; `.agent/decisions.md` ← `dry-decisions.md`; `.agent/prose_slips.md` ←
`dry-prose_slips.md`; `.agent/plan.md` ← `dry-plan.md`) and C3's two (`config_keys_ui.py` ←
`dry-config_keys_ui.py`; `environment.md` ← `dry-environment.md`) were each proved equal by a
Python sha256 reader before their commit, and `verify.py`'s lines above confirm the same
equality again. The five prepared files named with a digest in the prompt (`block.md`,
`verify.py`, `run_selection.py`, `selection.txt`, `digests.txt`) matched before any of them was
used, and the seven further files `digests.txt` itself digests (`dry-live_review.md`,
`dry-decisions.md`, `dry-prose_slips.md`, `dry-plan.md`, `dry-config_keys_ui.py`,
`dry-environment.md`) plus `src-decisions.md` all matched their listed sha256 before use.

## Deviations & assumptions

One self-found defect, not fixed, because fixing it needs an operation this round forbids.
`job_insight.py`'s module docstring, committed in C3, names `urlopen` a second time in prose
(explaining what `fetch_ollama_json` raises), beside the one real call in its body; `verify.py`'s
`C3 job_insight.py has one network read` check counts both and reads `False`. I found this only
at gate 1, after C3 and C4 had already landed. The check is pinned to C3's own commit (`show(c3,
path)`), so the only way to make it read `True` is to rewrite what C3 committed — an amend or a
rebase, both named forbidden by this round's Constraints and by the standing git safety rules I
run under, and unreachable any other way: a further commit renaming the tag, or an untagged
fixup commit, both break the `every commit carries an F311 R2 Cn subject` count the same
`verify.py` run already prints `True` for, trading one `False` line for a different one while
still leaving C3's own snapshot unread as `True`. I therefore left C3 exactly as committed,
reverted the one uncommitted edit I had tried in the working tree so `git status --porcelain`
stays empty, and record this here instead: the defect is cosmetic prose only, costs nothing on
disk, and the next round may correct the docstring's wording in a commit of its own that touches
`job_insight.py` for an unrelated reason.

No other departure from the block's ordered commit sequence occurred: C1 to C4 landed exactly as
ordered, no existing test went red because of C2 or C3, the one bare `SimpleNamespace` I first
wrote for the R-1383 test leaked a context-var closure that crashed an unrelated later test on
its next call (`job.budgets` missing) — found and fixed before committing C4 by using a real
`JobPlan` instead, which is what the block's parenthetical ("a saved record") already pointed at
— and no gate needed a re-run once each had its final input.

## For the operator, in plain sentences

Remedy can now work out, for one job that is running right now, which part of the job it is in,
whether its worker has gone quiet for longer than is normal, and if so what that quiet means and
what you could do about it. It also knows how to ask the local model server whether it is up and
which model it is holding in memory. None of this is reachable over the network yet; this round
only built and tested the part that works it out from what is already saved on disk. A small
wording slip was found in one file's own explanatory comment, not in anything the file actually
does, and is left for a later commit to tidy rather than reopening a commit that already landed.

## Next

In order: Phase 1 rule 1 (`.agent/STOP`) — absent, no action needed; rule 2, the Open PR Gate —
already checked at this round's start, no open pull request, nothing to merge; book round 2's
verdict in the next round's first commit; then the twins `client.now` and `client.insight`.
Operator questions open: 1. Open findings: 88 (gate 5, rule `open_finding_ids`, measured at
`1c83f4e93`).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `b78128011` |
| C2 | done | `ce81ee7dd` |
| C3 | done | `105378025` |
| C4 | done | `1c83f4e93` |
| C5 | done | this commit |
| Gate 1 | deviated | one line `False` (`C3 job_insight.py has one network read`), unfixable without a forbidden amend/rebase; see Deviations |
| Gate 2 | done | `All checks passed!` |
| Gate 3 | done | exit 0, `4142 passed, 2 skipped in 57.20s` |
| Gate 4 | done | `fail_count` 1 on the standing twelve; 88 open findings |
| Gate 5 | done | `88` |
| R-1383 | done | repaired and tested this round (C4); its resolution is for the reviewer to record |
| Push | pending | reported in the final reply only |
