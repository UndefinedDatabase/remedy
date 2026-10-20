# Handback — F312 round 5 (closure's integration-gate round)

## Session

SESSION 1 of feature F312 · round 5 · rounds so far 5

Context self-assessment: this session verified all ten prepared-file digests with a Python
sha256 reader before using any of them, executed C1 to C5 exactly as the block ordered with no
patching of the reviewer-authored `selfuse.py` or `launch.py`/`wait.py`, and all four gates
passed on the first run.

State block:
Feature F312 (`[~]` in STATUS since round 1's C1), branch `feature/f312-scope-kinds`, base
`7321e48df` (round 4's handback, reviewed PASS). Head: this commit (C6), after C1 to C5.
Fortschritt: ~90 % (T001 to T003 landed; the consolidation pass, the self-use run and the one
full suite done · the evidence, the package and the closing round remain) — Schätzung

## Range

Review of `7321e48df`..HEAD (C1 to C5 below, then this commit, C6, which also carries this
handback).

## Commits

### a16b86054 F312 R5 C1: book round 4, resolve R-1377 to R-1380, the plan
307 insertions, 9 deletions.
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f312-r5.md` | +162 (new file) | byte copy of `block.md` |
| `.agent/authored/f312-r5-selfuse.py` | +127 (new file) | byte copy of the reviewer-authored self-use script |
| `.agent/plan.md` | +7/-9 | byte copy of the prepared plan |
| `.agent/live_review.md` | +10 | byte append: round 4's `Gate:` entry and `Done:` resolutions for R-1377 to R-1380 |
| `.agent/prose_slips.md` | +1 | byte append: round 4's slip line |

### 618db1b81 F312 R5 C2: F312's Built State
32 insertions.
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T2_F312.md` | +32 | byte append of the authored Built State paragraph (precondition 4) |

### 34c815565 F312 R5 C3: the checklist's consolidation pass for F312
13 insertions.
| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | +13 | byte insertion of the consolidation paragraph directly before "The next consolidation measures against 34."; nothing joined, list stays at 34 items |

### e04884674 F312 R5 C4: the closure's self-use item run to its approval gate, never applied
430 insertions.
| Path | +/- | Reason |
|---|---|---|
| `scripts/self_use_queue.json` | +8 | the generator's one appended entry, `SU-066`, `consumed_by` empty |
| `.agent/selfuse_f312/SU-066.md` | +73 (new file) | the job file the run produced |
| `.agent/selfuse_f312/entry_and_job_file.txt` | +5 (new file) | entry id/title/provenance/consumed_by + job file path |
| `.agent/selfuse_f312/execution_config.txt` | +43 (new file) | the plan's execution config |
| `.agent/selfuse_f312/result_state.txt` | +16 (new file) | job id, state, stop reason/source, error, budgets/actuals, per-task states |
| `.agent/selfuse_f312/timing.txt` | +3 (new file) | started/finished/wall seconds |
| `.agent/selfuse_f312/changed_paths.txt` | +2 (new file) | the job's root-changed files |
| `.agent/selfuse_f312/full_transcript.txt` | +38 (new file) | job + per-task summary |
| `.agent/selfuse_f312/staleness_after.txt` | +2 (new file) | the staleness catalog read from the job's workspace after the run |
| `.agent/selfuse_f312/job_diff.txt` | +236 (new file) | `git diff HEAD...remedy/job-24460560b40f4cd7`, verbatim |
| `.agent/selfuse_f312/run_defects.txt` | +4 (new file) | `describe_self_use_run_defects()` over the run's `JobPlan` |

### 2fa2079ae F312 R5 C5: the closure's one full suite and its CPU cost
28 insertions.
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f312-closure-suite.txt` | +28 (new file) | the one full-suite transcript and the cost script's reading, in `f310-closure-suite.txt`'s shape |

### this commit (C6) F312 R5 C6: handback
1 file.
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file (a handoff cannot table its own commit) |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` before C1: `[]`, no open
PR — the Open PR Gate passes trivially. No other `gh` command this round. No worktree add/remove
of my own (the self-use script added and removed its own temporary job-branch worktree
internally, as its own code shows). The push is run after this commit, so its outcome is reported
in the final reply only.

## Verification

Gates run once each, after C5 and before this commit.

1. `git status --porcelain` → empty (no output).
   `python3 .remedy-wt/f312-r5/prep/verify.py .`:
   ```
   True	a16b86054 single parent equal to the commit before it
   True	618db1b81 single parent equal to the commit before it
   True	34c815565 single parent equal to the commit before it
   True	e04884674 single parent equal to the commit before it
   True	2fa2079ae single parent equal to the commit before it
   True	C1 paths exactly ['.agent/authored/f312-r5-selfuse.py', '.agent/authored/f312-r5.md', '.agent/live_review.md', '.agent/plan.md', '.agent/prose_slips.md']: [same]
   True	C2 paths exactly ['docs/roadmap/features/T2_F312.md']: [same]
   True	C3 paths exactly ['docs/agents/planner_reviewer_prompt.md']: [same]
   True	C4 paths are the queue and .agent/selfuse_f312/ only: [the ten selfuse_f312 files + scripts/self_use_queue.json]
   True	C5 paths exactly ['.agent/authored/f312-closure-suite.txt']: [same]
   absent	C6
   True	C1 the block copy
   True	C1 the self-use script copy
   True	C1 the plan
   True	C1 .agent/live_review.md is the base plus src-ledger.md
   True	C1 .agent/prose_slips.md is the base plus src-slips.md
   True	C2 the feature file is its parent plus the authored Built State
   True	C3 the consolidation paragraph stands right before the next-consolidation line
   True	C5 the transcript carries `command: python3 -m pytest -n auto -q`
   True	C5 the transcript carries `real exit code:`
   True	C5 the transcript carries `summary line:`
   True	C5 the transcript carries `bad node ids (failed + errors):`
   True	C5 the transcript carries `reflog unchanged during the run:`
   True	C5 the transcript carries `cost exit code:`
   ALL True
   ```
2. The ten files under `.agent/selfuse_f312/`, each non-empty, byte sizes:
   `SU-066.md` 3909; `entry_and_job_file.txt` 252; `execution_config.txt` 1367;
   `result_state.txt` 1346; `timing.txt` 105; `changed_paths.txt` 34;
   `full_transcript.txt` 1991; `staleness_after.txt` 222; `job_diff.txt` 10031;
   `run_defects.txt` 248.
3. The suite of C5: exit code `0`; summary line
   `22015 passed, 11 skipped, 1 warning in 342.48s (0:05:42)`; bad node ids (failed + errors):
   `NONE`.
4. `python3 -m apps.cli.main integrity check --json`:
   ```
   {"check_count": 6, ..., "checks": [..., {"message": "13 open blocker/high: R-1335, R-1336,
   R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362, R-1369",
   "name": "high_blockers_open", "status": "fail"}], "error": "integrity_failed",
   "fail_count": 1, "ok": false, "passed": false}
   ```
   `fail_count` 1, the one failing check `high_blockers_open` naming the same thirteen ids as at
   the base (DECISION F310 D7). Then
   `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`
   → `87` (the base's 91, less the four resolved: R-1377, R-1378, R-1379, R-1380).

## Authored-text proofs

C1's three byte copies (`.agent/authored/f312-r5.md` ← `block.md`, 162 lines/sha256
`52906eef8f30a11aad25d275c7176142b87c94be15617e49a12f71a51f6ee387`;
`.agent/authored/f312-r5-selfuse.py` ← `selfuse.py`; `.agent/plan.md` ← `dry-plan.md`) and the
two byte appends (`.agent/live_review.md` ← `src-ledger.md`; `.agent/prose_slips.md` ←
`src-slips.md`) were each proved equal by a Python bytes-equality script before the commit
(`.remedy-wt/f312-r5-worker/c1_prove.py`, `ALL True`), and `verify.py`'s "C1" lines above confirm
it again. C2's append (`docs/roadmap/features/T2_F312.md` ← `src-built-state.md`) and C3's
insertion (`docs/agents/planner_reviewer_prompt.md` ← `src-consolidation.md`) were each proved
equal to parent-plus-addition by a standalone Python equality check before their commits, and
`verify.py`'s "C2" and "C3" lines confirm them again. All eight prepared-file digests named in
the block (`block.md`, `verify.py`, `selfuse.py`, `dry-plan.md`, `src-ledger.md`, `src-slips.md`,
`src-built-state.md`, `src-consolidation.md`, `launch.py`, `wait.py`) matched before any file was
used.

## Self-use run

- Entry id: `SU-066` — "Refresh the pinned toolchain" (job id `24460560b40f4cd7`).
- Builder: provider `claude-cli`, model `claude-sonnet-4-6`, effort `medium` (source `cli`).
  Reviewer: provider `claude-cli`, model `claude-sonnet-4-6`, effort `medium` (source `cli`).
- Job state: `blocked`. Stop reason: (empty). Error: `task_T003_gate_failed:
  final_status=staged_blocked; reviewer_verdict=blocked`.
- Task status / reviewer verdict (from `result_state.txt`):
  - T001: `applied_to_job_workspace` / verdict `pass`
  - T002: `applied_to_job_workspace` / verdict `pass`
  - T003: `blocked` / verdict `blocked`
  - T004: `skipped` / verdict (none)
  - T005: `skipped` / verdict (none)
- Wall seconds (from `timing.txt`): `917.8`.
- Paths in `changed_paths.txt`: `t001-findings.md`, `t002-findings.md`.
- `job_diff.txt`, VERBATIM:
  ```
  $ git diff HEAD...remedy/job-24460560b40f4cd7  (exit 0)
  diff --git a/t001-findings.md b/t001-findings.md
  new file mode 100644
  index 000000000..72e78eec6
  --- /dev/null
  +++ b/t001-findings.md
  @@ -0,0 +1,158 @@
  +# T001 Findings: Pinned Toolchain — Tools with Newer Releases
  +
  +Sources read:
  +- `pyproject.toml` (declared dependencies and dev extra)
  +- `constraints.txt` (exact pins with hashes)
  +- `.github/workflows/ci.yml` (Python matrix)
  +
  +Network-dependent lookups (PyPI newest versions, GitHub Python manifest) could not be
  +performed — no HTTP tool is available in this environment. Every item that required a
  +network query is explicitly marked **unknown — network unavailable**.
  +
  +---
  +
  +## 1. Directly pinned tools in `pyproject.toml`
  +
  +`pyproject.toml` pins two tools with `==` in the `dev` extra (DECISION F279 D1):
  +
  +| Tool | Pinned in pyproject.toml | PyPI newest |
  +|------|--------------------------|-------------|
  +| `ruff` | `0.15.17` | **unknown — network unavailable** |
  +| `uv` | `0.12.18` | **unknown — network unavailable** |
  +
  +Both pins are also repeated verbatim in `constraints.txt`.
  +
  +---
  +
  +## 2. All tools tracked by `remedy doctor toolchain`
  +
  +`toolchain.py` reports every package declared in `pyproject.toml`'s `dependencies` and
  +`optional-dependencies["dev"]`.  The ten tools, with their declared range, their
  +`constraints.txt` pin, and the PyPI newest version:
  +
  +| Tool | pyproject.toml range | constraints.txt pin | PyPI newest |
  +|------|----------------------|---------------------|-------------|
  +| `pydantic` | `>=2.0,<3` | **2.13.5** | unknown — network unavailable |
  +| `psutil` | `>=5.9,<8` | **7.2.2** | unknown — network unavailable |
  +| `tomli` | `>=2.0,<3; python_version < '3.11'` | **2.4.1** | unknown — network unavailable |
  +| `pytest` | (unbounded) | **9.1.1** | unknown — network unavailable |
  +| `pytest-xdist` | (unbounded) | **3.8.0** | unknown — network unavailable |
  +| `ruff` | `==0.15.17` | **0.15.17** | unknown — network unavailable |
  +| `mypy` | (unbounded) | **2.3.1** | unknown — network unavailable |
  +| `pytest-cov` | (unbounded) | **7.1.0** | unknown — network unavailable |
  +| `coverage` | (unbounded) | **7.16.1** | unknown — network unavailable |
  +| `uv` | `==0.12.18` | **0.12.18** | unknown — network unavailable |
  +
  +Because the "newest" column is unknown for every tool, no pin is confirmed movable or
  +confirmed current from this run.  The `constraints.txt` regeneration command in its own
  +header is the authoritative way to refresh all pins:
  +
  +```
  +uv pip compile pyproject.toml --extra dev --extra ollama --universal \
  +    --python-version 3.10 --generate-hashes --no-annotate \
  +    --exclude-newer <DATE> -o constraints.txt
  +```
  +
  +---
  +
  +## 3. All transitive packages in `constraints.txt`
  +
  +These are pinned as indirect dependencies and are not tracked by `remedy doctor toolchain`,
  +but are listed here for completeness.  All "newest" values require network access.
  +
  +| Package | Pinned version | PyPI newest |
  +|---------|---------------|-------------|
  +| `annotated-types` | 0.8.0 | unknown — network unavailable |
  +| `anyio` | 4.15.1 | unknown — network unavailable |
  +| `ast-serialize` | 0.11.2 | unknown — network unavailable |
  +| `certifi` | 2026.7.22 | unknown — network unavailable |
  +| `colorama` | 0.4.6 | unknown — network unavailable |
  +| `exceptiongroup` | 1.3.1 | unknown — network unavailable |
  +| `execnet` | 2.1.2 | unknown — network unavailable |
  +| `h11` | 0.16.0 | unknown — network unavailable |
  +| `httpcore` | 1.0.9 | unknown — network unavailable |
  +| `httpx` | 0.28.1 | unknown — network unavailable |
  +| `idna` | 3.20 | unknown — network unavailable |
  +| `iniconfig` | 2.3.0 | unknown — network unavailable |
  +| `librt` | 0.15.0 | unknown — network unavailable |
  +| `mypy-extensions` | 1.1.0 | unknown — network unavailable |
  +| `ollama` | 0.6.2 | unknown — network unavailable |
  +| `packaging` | 26.3 | unknown — network unavailable |
  +| `pathspec` | 1.1.1 | unknown — network unavailable |
  +| `pluggy` | 1.6.0 | unknown — network unavailable |
  +| `pydantic-core` | 2.46.5 | unknown — network unavailable |
  +| `pygments` | 2.21.0 | unknown — network unavailable |
  +| `typing-extensions` | 4.16.0 | unknown — network unavailable |
  +| `typing-inspection` | 0.4.4 | unknown — network unavailable |
  +
  +---
  +
  +## 4. Python versions in the CI matrix
  +
  +**Current matrix** (`.github/workflows/ci.yml` line 38):
  +
  +```yaml
  +python-version: ['3.10', '3.12']
  +```
  +
  +**Floor** (`pyproject.toml` line 8): `requires-python = ">=3.10"`
  +
  +### 3.10 (floor slot)
  +
  +Correct and should not move.  The CI comment at lines 31–34 states explicitly:
  +> "pyproject.toml promises `requires-python = ">=3.10"`, so the floor AND a current
  +> interpreter both run the whole suite"
  +
  +The floor slot must match the declared minimum.
  +
  +### 3.12 (current-interpreter slot)
  +
  +**Should move**, but the target version is unknown — network unavailable.
  +
  +Python releases one new stable version every October.  As of the task date (2026-10-21):
  +- Python 3.13 reached stable: October 2024
  +- Python 3.14 reached stable: October 2025
  +- Python 3.15: October 2026 release window (may or may not yet be on hosted runners)
  +
  +The `3.12` slot has fallen at least two versions behind the newest stable.  It must be
  +updated to the highest stable version available on GitHub's hosted `ubuntu-latest` runners.
  +
  +### Newest stable Python — source
  +
  +The authoritative source is:
  +
  +```
  +https://raw.githubusercontent.com/actions/python-versions/main/versions-manifest.json
  +```
  +
  +Take the highest version whose entry carries `"stable": true`.
  +
  +**This URL was not fetched** — no HTTP tool is available in this environment.  The newest
  +stable Python version is therefore **unknown — network unavailable** in this run.
  +
  +### Recommendation (pending network confirmation)
  +
  +Once the manifest is fetched, update the matrix to:
  +
  +```yaml
  +python-version: ['3.10', '<newest-stable>']
  +```
  +
  +where `<newest-stable>` is the value read from the manifest.  The floor `3.10` stays.
  +
  +---
  +
  +## 5. Items that can move without network (file-readable only)
  +
  +None.  Every "can this pin move?" question requires comparing the pinned version to the
  +PyPI newest release, which needs the network.  No pin can be confirmed movable or
  +confirmed current from files alone.
  +
  +---
  +
  +## 6. Next step
  +
  +Run `remedy doctor toolchain` (or `remedy doctor toolchain --json`) on a machine with
  +outbound network access to PyPI.  That command fetches the PyPI JSON API for each of the
  +ten tracked tools and fills in the "newest" column.  Then fetch the Python manifest URL
  +above to determine the target Python version for the matrix's current-interpreter slot.
  diff --git a/t002-findings.md b/t002-findings.md
  new file mode 100644
  index 000000000..a25e61453
  --- /dev/null
  +++ b/t002-findings.md
  @@ -0,0 +1,65 @@
  +# T002 Findings: Release Notes for Tools That Move
  +
  +## STATUS: BLOCKED — network fetch not possible in this environment
  +
  +This task requires fetching remote changelog content.  No fetch was possible.
  +Evidence of the constraint and a proper escalation path follow.
  +
  +---
  +
  +## Evidence of environment constraint
  +
  +The tools available to this agent in this session are:
  +
  +| Tool | Can make HTTP requests? |
  +|------|------------------------|
  +| `Read` | No — reads local filesystem paths only |
  +| `Write` | No — writes local filesystem paths only |
  +| `Edit` | No — edits local filesystem paths only |
  +| `Glob` | No — pattern-matches local filesystem only |
  +| `Grep` | No — searches local filesystem only |
  +
  +No `Bash`, `Shell`, `HTTP`, `Fetch`, `WebSearch`, or equivalent tool is present.
  +There is no mechanism in this session to issue an HTTP GET to any URL.
  +
  +Fetch attempts were not made because no tool capable of making them exists.
  +This is not an assertion about general network reachability of the host; it is a
  +statement about the agent's tool inventory.
  +
  +---
  +
  +## Formal task block
  +
  +**Blocker:** The primary acceptance criterion — "Every tool Task 1 found has its
  +release notes quoted or summarized, with the address they were read from" — cannot
  +be satisfied without reading remote changelog content.  The agent cannot read remote
  +content.  This task must be re-run in an environment that provides an HTTP or shell
  +tool, or a human operator must fetch the content and paste it into context.
  +
  +---
  +
  +## What a capable environment must fetch
  +
  +The following URLs are the authoritative changelogs.  The relevant version range for
  +each tool is **pinned version (from `constraints.txt`) → newest version on PyPI**;
  +the newest version must be determined first (see T001).
  +
  +| Tool | Pin | Changelog URL |
  +|------|-----|---------------|
  +| `ruff` | 0.15.17 | https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md |
  +| `uv` | 0.12.18 | https://github.com/astral-sh/uv/blob/main/CHANGELOG.md |
  +| `pydantic` | 2.13.5 | https://github.com/pydantic/pydantic/blob/main/HISTORY.md |
  +| `mypy` | 2.3.1 | https://github.com/python/mypy/blob/master/CHANGELOG.md |
  +| `pytest` | 9.1.1 | https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst |
  +| `pytest-xdist` | 3.8.0 | https://github.com/pytest-dev/pytest-xdist/blob/master/CHANGELOG.rst |
  +| `pytest-cov` | 7.1.0 | https://github.com/pytest-dev/pytest-cov/blob/master/CHANGELOG.rst |
  +| `coverage` | 7.16.1 | https://github.com/nedbat/coveragepy/blob/master/CHANGES.rst |
  +| `psutil` | 7.2.2 | https://github.com/giampaolo/psutil/blob/master/HISTORY.rst |
  +| `tomli` | 2.4.1 | https://github.com/hukkin/tomli/blob/master/CHANGELOG.md |
  +| Python (CI matrix) | 3.12 | https://docs.python.org/3/whatsnew/index.html (3.13, 3.14, 3.15) |
  +
  +For each tool, the content to extract is:
  +- Removed or renamed features, flags, or configuration keys
  +- Changed default behaviours
  +- New warnings or errors enabled by default
  +- Data format changes (especially for `coverage`)
  ```
- `run_defects.txt`, VERBATIM:
  ```
  From describe_self_use_run_defects():

  1. job 24460560b40f4cd7 (blocked): task_T003_gate_failed: final_status=staged_blocked; reviewer_verdict=blocked
  2. T003 (blocked): completion_gate_failed: final_status=staged_blocked; reviewer_verdict=blocked
  ```
- No finding is registered by this round for these two defect strings (per the block's
  instruction); the next round's first commit registers them, per `## Next` below.

## Closure suite

`.agent/authored/f312-closure-suite.txt`, whole and verbatim:
```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 343.3s (the launcher's reading); pytest's own reported wall time: 342.48s (0:05:42)
summary line: 22015 passed, 11 skipped, 1 warning in 342.48s (0:05:42)
bad node ids (failed + errors):
  - NONE
leftover processes: NONE
tree it ran on: e04884674 (F312 R5 C4: the closure's self-use item run to its approval gate, never applied)
tree note: C1 to C4 changed only .agent/ files, the feature file, the checklist page and the self-use queue
reflog before: e04884674 HEAD@{2026-10-21 00:33:56 +0200}: commit: F312 R5 C4: the closure's self-use item run to its approval gate, never applied
reflog after: e04884674 HEAD@{2026-10-21 00:33:56 +0200}: commit: F312 R5 C4: the closure's self-use item run to its approval gate, never applied
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F312 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1294.96 CPU seconds, 342.49 wall seconds, 22026 tests collected, exit status 0, recorded 2026-10-20T22:39:48Z
This closure's suite used 1294.96 CPU seconds, 2.5 percent more than F310's 1263.08, within the 10 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 0 percent.
The test modules whose CPU time rose most since F310's closure run:
  +4.45 s  tests/orchestration/test_review_zip_hygiene.py (34.66 -> 39.11)
  +3.91 s  tests/orchestration/test_review_package_full_integration.py (4.25 -> 8.16)
  +3.02 s  tests/cli/test_serve_client_parity.py (6.89 -> 9.91)
  +2.99 s  tests/orchestration/test_run_manifest_integrity.py (5.97 -> 8.96)
  +2.86 s  tests/runtimes/test_runtime_cli_process_boundary.py (8.88 -> 11.74)
  +2.58 s  tests/orchestration/test_event_name_coupling.py (19.26 -> 21.84)
  +2.57 s  tests/cli/test_do_scale_matrix.py (37.69 -> 40.26)
  +2.35 s  tests/orchestration/test_run_manifest_zero_call_expectations.py (2.46 -> 4.81)
  +2.26 s  tests/orchestration/test_subtree_rerun_prepare.py (12.44 -> 14.70)
  +2.16 s  tests/orchestration/test_product_smoke.py (3.22 -> 5.38)
```

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | a16b86054 |
| C2 | done | 618db1b81 |
| C3 | done | 34c815565 |
| C4 | done | e04884674 |
| C5 | done | 2fa2079ae |
| Gate 1 | done | ALL True |
| Gate 2 | done | all ten files non-empty |
| Gate 3 | done | exit 0, 22015 passed, 11 skipped, no bad node ids |
| Gate 4 | done | fail_count 1 on the standing thirteen; 87 open findings |
| C6 | done | this commit |

## Deviations & assumptions

- None of C1 to C5 was amended; each landed on its first attempt, and `selfuse.py`,
  `launch.py` and `wait.py` were run unedited, as ordered.
- C4's self-use run itself stopped at `blocked` (T003's completion gate failed; T004 and T005
  were skipped as a direct consequence), which is the normal shape of "run to the approval gate,
  never applied" when a task is refused there — not a deviation from the block, which anticipates
  exactly this outcome by requiring `run_defects.txt` and forbidding this round from registering
  any finding for it.
- C5 step 4's exit code for `scripts/closure_suite_cost.py` was not read via a second shell
  invocation (the sandbox refuses the compound `cmd; echo $?` shape this session's shell tool
  would otherwise use to capture it, and the block forbids a second real run of the command
  itself). Instead the script's own `compare()` function was read: the printed sentence
  "within the 10 percent limit" is only reachable through the `return head + ..., 0` branch, so
  the exit code is 0 by construction from the one run already made, not re-queried.
- The records of the operator's failed lab job were not read this round either: the data root
  is not readable in this session, unchanged since round 3 (DECISION F312 D1).

## For the operator, in plain sentences

Before this feature closes, Remedy ran one real piece of paid work on itself: it asked a frontier
model to check whether the versions of the testing and linting tools Remedy's CI installs are
still current, read their release notes, and raise the pins — and the run stopped partway through
at an internal review step, before anything was written to the project, when that review step
would not approve one of the five pieces of work. Separately, Remedy's whole test collection ran
once on the code that will ship: 22,015 tests passed, none failed, and 11 were intentionally
skipped. That run took about five minutes and forty-two seconds. The reading on computer time used
says this feature's test run cost about two and a half percent more computer time than the
previous feature's, which is well inside the allowed range.

## Next

In order: Phase 1 rule 1 (`.agent/STOP`) — absent, no action needed; rule 2, the Open PR Gate —
no pull request is open for this branch yet; the reviewer reviews round 5, books its verdict and
registers every self-use run defect in the next round's first commit; then the evidence bundle
and the review package (the suite is green); then the closing round: the rotation, the STATUS
line, the README and the pull request.
Operator questions open: 1. Open findings: 87 (gate 4, `open_finding_ids`, rule: the base's 91
less the four R-1377–R-1380 resolutions booked at C1 of this round).
