# Handoff — F152 round 7 (the consolidation pass, the self-use item, the one full suite)

## Session

SESSION 1 of feature F152 · round 7 · rounds so far 7. This round carried out the closure's three
remaining checks — the checklist's consolidation paragraph, the first real self-use run through
F152's own declared isolation flags, and the feature's one full suite — in sequence with no scope
drift, pausing only to correct two self-made background-launch mistakes (wrong working directory)
before either real run started.

Fortschritt: ~90 % (T001 to T003 landed; the consolidation pass, the self-use run and the one full
suite done · the evidence, the package and the closing round remain) — Schätzung.

## Range

Review of `13d9a8044`..`5501c4fd3` (C1 to C4; C5 — this file — is the commit that carries it, per
the handback template's self-reference exception).

## Commits

### e1502a06a F152 R7 C1: book round 6, R-1460 to R-1462 resolved, the plan, the block and the self-use script
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f152-r7-selfuse.py` | +180/-0 | NEW FILE — the reviewer-authored self-use script for C3, byte-copied from the prepared `c1-` file |
| `.agent/authored/f152-r7.md` | +156/-0 | NEW FILE — this round's block, the authored-text proof |
| `.agent/live_review.md` | +8/-0 | round 6's PASS verdict booked as a Gate entry; R-1460, R-1461 and R-1462 each get a `Done:` line |
| `.agent/plan.md` | +9/-9 | rewritten: Current Step/Next Steps/Risks to round 7 |

### a48675720 F152 R7 C2: the checklist's consolidation pass for F152
| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | +14/-0 | one consolidation paragraph for F152's closure; nothing joined, no two items merged, the list stays at 34 |

### 7816704be F152 R7 C3: the closure's self-use item run to its approval gate, never applied
| Path | +/- | Reason |
|---|---|---|
| `scripts/self_use_queue.json` | +8/-0 | the generator's one appended entry, `SU-082`, `consumed_by` empty |
| 11 files under `.agent/selfuse_f152/` | +375/-0 total | NEW FILES — the self-use run's record (entry markdown, execution config, result state, timing, changed paths, full transcript, worker isolation, staleness-after, job diff, run defects); see "Self-use run" below |

### 5501c4fd3 F152 R7 C4: the closure's one full suite and its CPU cost
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f152-closure-suite.txt` | +28/-0 | NEW FILE — the one full-suite transcript and the cost script's reading, in `f157-closure-suite.txt`'s shape |

### (this commit) F152 R7 C5: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file — carried alone, per the handback template's self-reference exception (R-0149) |

## External actions

No `gh` command beyond the Open PR Gate's own read (`gh pr list --state open ...` → `[]`, run before
C1). No pull request created, edited or merged. `git worktree add --detach` and `git worktree
remove --force` ran once each, but not by me directly: the self-use script (C3) added a detached
worktree at a path under `.remedy-wt/` for the job branch `remedy/job-6f6d2e16e6114f58` to read its
staleness catalog, then removed it and pruned, inside its own single run — confirmed by
`staleness_after.txt` reading "Read from: the job branch remedy/job-6f6d2e16e6114f58" and by
`git worktree list` showing none left afterward. No worktree of my own. No stash entry touched. No
`claude` binary invoked by me; its two real calls (builder, reviewer) ran inside the self-use job
through `claude-cli`, under F152's declared flags and cleaned environment, as C3 orders.
`git push origin feature/f152-worker-config-isolation` runs once, immediately after this commit.

## Verification

**Gate 1.** `git status --porcelain` → empty (exit 0). Then
`python3 .remedy-wt/f152-r7/prep/verify.py .` (the repository root):

```
True	e1502a06a single parent equal to the commit before it
True	e1502a06a subject carries a F152 R7 Cn tag: F152 R7 C1: book round 6, R-1460 to R-1462 resolved, the plan, the blo
True	e1502a06a adds no machine path
True	a48675720 single parent equal to the commit before it
True	a48675720 subject carries a F152 R7 Cn tag: F152 R7 C2: the checklist's consolidation pass for F152
True	a48675720 adds no machine path
True	7816704be single parent equal to the commit before it
True	7816704be subject carries a F152 R7 Cn tag: F152 R7 C3: the closure's self-use item run to its approval gate, neve
True	7816704be adds no machine path
True	5501c4fd3 single parent equal to the commit before it
True	5501c4fd3 subject carries a F152 R7 Cn tag: F152 R7 C4: the closure's one full suite and its CPU cost
True	5501c4fd3 adds no machine path
True	on feature/f152-worker-config-isolation
True	C1 paths [...four C1 paths...]
True	C1 .agent/authored/f152-r7-selfuse.py equals c1-.agent__authored__f152-r7-selfuse.py
True	C1 .agent/authored/f152-r7.md equals c1-.agent__authored__f152-r7.md
True	C1 .agent/live_review.md equals c1-.agent__live_review.md
True	C1 .agent/plan.md equals c1-.agent__plan.md
True	C2 the checklist page alone
True	C2 page equals the prepared copy
True	C3 paths: the queue and 11 file(s) under .agent/selfuse_f152/
True	C3 writes eleven self-use files: 11
True	C3 queue gains exactly one appended entry: SU-082
True	C3 the new entry is not consumed
True	C4 the transcript alone
True	C4 transcript carries 'command:'
True	C4 transcript carries 'real exit code:'
True	C4 transcript carries 'wall time:'
True	C4 transcript carries 'summary line:'
True	C4 transcript carries 'bad node ids (failed + errors):'
True	C4 transcript carries 'leftover processes:'
True	C4 transcript carries 'tree it ran on:'
True	C4 transcript carries 'reflog unchanged during the run:'
True	C4 transcript carries 'cost exit code:'
absent	C5
True	the saved block equals block.md
ALL True
```

Every line `True` (C5 correctly `absent` before this commit exists); the last line `ALL True`.

**Gate 2.** The eleven files under `.agent/selfuse_f152/`, each confirmed non-empty, by byte size:

```
SU-082.md: 936 bytes
entry_and_job_file.txt: 295 bytes
execution_config.txt: 1367 bytes
result_state.txt: 857 bytes
timing.txt: 105 bytes
changed_paths.txt: 41 bytes
full_transcript.txt: 1578 bytes
worker_isolation.txt: 861 bytes
staleness_after.txt: 200 bytes
job_diff.txt: 9792 bytes
run_defects.txt: 5 bytes
```

**Gate 3.** C4's suite: command `python3 -m pytest -n auto -q`, real exit code `1`, wall `330.0s`
(launcher) / `329.18s (0:05:29)` (pytest). Decisive lines:

```
    def test_every_remedy_name_production_code_spells_is_registered():
>       assert scan(spelled_names) == {}
E       AssertionError: assert {'REMEDY_ISOL...solation.py']} == {}
E       Left contains 1 more item:
E       {'REMEDY_ISOLATION_POISON': ['packages/orchestration/worker_isolation.py']}
tests/orchestration/test_env_registry.py:130: AssertionError
FAILED tests/orchestration/test_env_registry.py::test_every_remedy_name_production_code_spells_is_registered
1 failed, 23940 passed, 11 skipped, 1 warning in 329.18s (0:05:29)
```

One bad node id, no leftover-process line. Committed exactly as read, per C4 point 6 — not
investigated or repaired this round.

**Gate 4.** `python3 -m apps.cli.main integrity check --json`, run once:

```
{"check_count": 6, "checks": [{"message": "handlers=201", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```

`fail_count` 0, all six checks `pass`. Then
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
→ `['R-1246', 'R-1281', 'R-1351', 'R-1353', 'R-1426', 'R-1428', 'R-1448', 'R-1450']` — exactly the
eight ids the block names.

## Authored-text proofs

C1's byte copy (`.remedy-wt/f152-r7-worker/c1_copy.py`) read `True` for all four targets
immediately after copying: `.agent/authored/f152-r7.md`, `.agent/authored/f152-r7-selfuse.py`,
`.agent/live_review.md`, `.agent/plan.md`. `block.md`'s own line count and sha256 — `156` lines,
`1a5dbecce17db33d7e5ad88efa008697ecd12e3662c211f3ca2b7411fd4a8916` — were independently computed
directly against the prepared `block.md` and against `.agent/authored/f152-r7.md` and matched.
C2's byte copy (`.remedy-wt/f152-r7-worker/c2_copy.py`) read `True` for
`docs/agents/planner_reviewer_prompt.md`. Gate 1's `verify.py` run independently re-confirmed every
`C1 ... equals c1-...` line `True`, `C2 page equals the prepared copy` `True`, and `the saved block
equals block.md` `True`.

## Self-use run

Entry `SU-082`, "Write the first tests for packages/orchestration/client_scope.py" (generated,
self-use-generator tier 5, untested module). Job ID `6f6d2e16e6114f58`. Builder: `claude-cli`,
model `claude-sonnet-4-6`, effort `medium`. Reviewer: `claude-cli`, model `claude-sonnet-4-6`,
effort `medium`. Job state `completed`, stop reason empty, stop source empty. Task `T001`: status
`applied_to_job_workspace`, reviewer verdict `pass`, final status `staged_review_passed`,
repair rounds used `0`. Wall seconds `240.2` (script's own timing). Changed paths:
`tests/orchestration/test_client_scope.py`.

`worker_isolation.txt` verbatim:

```
T001: {"adr_ref": "docs/adr/0002-claude-cli-worker-isolation.md", "applied": true, "env_digest": "7db0bffa706f498f7cee90e529f8df70bcee84653661ba0e35204967c1ff7ae5", "home": "operator", "method": "tool_flag", "model": "claude-sonnet-4-6", "names": ["HOME", "LANG", "LOGNAME", "PATH", "SHELL", "TERM", "USER"], "provider": "claude-cli", "role": "builder", "tool_args": ["--setting-sources", "project,local", "--strict-mcp-config"]}
T001: {"adr_ref": "docs/adr/0002-claude-cli-worker-isolation.md", "applied": true, "env_digest": "7db0bffa706f498f7cee90e529f8df70bcee84653661ba0e35204967c1ff7ae5", "home": "operator", "method": "tool_flag", "model": "claude-sonnet-4-6", "names": ["HOME", "LANG", "LOGNAME", "PATH", "SHELL", "TERM", "USER"], "provider": "claude-cli", "role": "reviewer", "tool_args": ["--setting-sources", "project,local", "--strict-mcp-config"]}
```

`job_diff.txt` verbatim:

```
$ git diff HEAD...remedy/job-6f6d2e16e6114f58  (exit 0)
diff --git a/tests/orchestration/test_client_scope.py b/tests/orchestration/test_client_scope.py
new file mode 100644
index 000000000..e25cfad39
--- /dev/null
+++ b/tests/orchestration/test_client_scope.py
@@ -0,0 +1,274 @@
+"""Tests for packages.orchestration.client_scope (amend1015c D2)."""
+
+from __future__ import annotations
+
+from dataclasses import dataclass
+from typing import Any
+from unittest.mock import patch
+from uuid import UUID
+
+from packages.orchestration.client_scope import (
+    client_order_read_refusal,
+    client_project_ids,
+)
+
+
+# ---------------------------------------------------------------------------
+# Helpers
+
+
+def _client(name: str, projects: tuple[str, ...]) -> Any:
+    """Minimal stand-in for ApiClient."""
+
+    @dataclass
+    class _Client:
+        name: str
+        projects: tuple[str, ...]
+
+    return _Client(name=name, projects=projects)
+
+
+def _project(id_: str, slug: str | None = None) -> Any:
+    """Minimal stand-in for RemyProject."""
+
+    @dataclass
+    class _Project:
+        id: UUID
+        slug: str | None
+
+    return _Project(id=UUID(id_), slug=slug)
+
+
+_UUID_A = "00000000-0000-0000-0000-000000000001"
+_UUID_B = "00000000-0000-0000-0000-000000000002"
+
+
+# ---------------------------------------------------------------------------
+# client_project_ids
+
+
+class TestClientProjectIds:
+    def test_returns_project_id_when_client_lists_it_by_id(self) -> None:
+        client = _client("bot", (_UUID_A,))
+        project = _project(_UUID_A, slug=None)
+        with (
+            patch(
+                "packages.orchestration.project_registry.list_projects_readonly",
+                return_value=[project],
+            ),
+            patch(
+                "packages.orchestration.api_clients.client_lists_project",
+                side_effect=lambda c, keys: any(k in c.projects for k in keys),
+            ),
+        ):
+            result = client_project_ids(client)
+        assert result == frozenset({_UUID_A})
+
+    def test_returns_project_id_when_client_lists_it_by_slug(self) -> None:
+        client = _client("bot", ("my-project",))
+        project = _project(_UUID_A, slug="my-project")
+        with (
+            patch(
+                "packages.orchestration.project_registry.list_projects_readonly",
+                return_value=[project],
+            ),
+            patch(
+                "packages.orchestration.api_clients.client_lists_project",
+                side_effect=lambda c, keys: any(k in c.projects for k in keys),
+            ),
+        ):
+            result = client_project_ids(client)
+        assert result == frozenset({_UUID_A})
+
+    def test_returns_empty_when_client_does_not_list_project(self) -> None:
+        client = _client("bot", ("other-project",))
+        project = _project(_UUID_A, slug="my-project")
+        with (
+            patch(
+                "packages.orchestration.project_registry.list_projects_readonly",
+                return_value=[project],
+            ),
+            patch(
+                "packages.orchestration.api_clients.client_lists_project",
+                return_value=False,
+            ),
+        ):
+            result = client_project_ids(client)
+        assert result == frozenset()
+
+    def test_returns_empty_when_no_projects_registered(self) -> None:
+        client = _client("bot", ("anything",))
+        with patch(
+            "packages.orchestration.project_registry.list_projects_readonly",
+            return_value=[],
+        ):
+            result = client_project_ids(client)
+        assert result == frozenset()
+
+    def test_returns_multiple_project_ids(self) -> None:
+        client = _client("bot", (_UUID_A, _UUID_B))
+        projects = [_project(_UUID_A), _project(_UUID_B)]
+        with (
+            patch(
+                "packages.orchestration.project_registry.list_projects_readonly",
+                return_value=projects,
+            ),
+            patch(
+                "packages.orchestration.api_clients.client_lists_project",
+                side_effect=lambda c, keys: any(k in c.projects for k in keys),
+            ),
+        ):
+            result = client_project_ids(client)
+        assert result == frozenset({_UUID_A, _UUID_B})
+
+
+# ---------------------------------------------------------------------------
+# client_order_read_refusal
+
+
+class TestClientOrderReadRefusal:
+    def test_returns_none_when_order_record_not_found(self) -> None:
+        client = _client("bot", (_UUID_A,))
+        with (
+            patch("packages.orchestration.serve_paths.serve_paths"),
+            patch(
+                "packages.orchestration.serve_runs.read_order_record",
+                return_value=None,
+            ),
+        ):
+            result = client_order_read_refusal(client, "ord-unknown")
+        assert result is None
+
+    def test_returns_none_when_client_lists_order_project(self, tmp_path) -> None:
+        order_file = tmp_path / "order.md"
+        order_file.write_text(
+            f"---\nproject: {_UUID_A}\n---\nDo something.\n", encoding="utf-8"
+        )
+
+        from packages.orchestration.serve_runs import OrderRecord
+
+        record = OrderRecord(
+            order_id="ord-abc",
+            pid=1,
+            started_at="2026-01-01T00:00:00Z",
+            order_file=str(order_file),
+            out_log="",
+            err_log="",
+        )
+
+        from packages.orchestration.project_registry import RemyProject
+
+        project = RemyProject(id=UUID(_UUID_A), name="alpha", slug="alpha")
+        client = _client("bot", (_UUID_A,))
+
+        with (
+            patch("packages.orchestration.serve_paths.serve_paths"),
+            patch(
+                "packages.orchestration.serve_runs.read_order_record",
+                return_value=record,
+            ),
+            patch(
+                "packages.orchestration.project_registry.select_project",
+                return_value=(project, "registry"),
+            ),
+            patch(
+                "packages.orchestration.api_clients.client_lists_project",
+                side_effect=lambda c, keys: any(k in c.projects for k in keys),
+            ),
+        ):
+            result = client_order_read_refusal(client, "ord-abc")
+        assert result is None
+
+    def test_returns_refusal_when_order_file_unreadable(self, tmp_path) -> None:
+        from packages.orchestration.serve_runs import OrderRecord
+
+        record = OrderRecord(
+            order_id="ord-abc",
+            pid=1,
+            started_at="2026-01-01T00:00:00Z",
+            order_file=str(tmp_path / "missing.md"),
+            out_log="",
+            err_log="",
+        )
+        client = _client("bot", (_UUID_A,))
+        with (
+            patch("packages.orchestration.serve_paths.serve_paths"),
+            patch(
+                "packages.orchestration.serve_runs.read_order_record",
+                return_value=record,
+            ),
+        ):
+            result = client_order_read_refusal(client, "ord-abc")
+        assert result is not None
+        assert "may not read order" in result
+
+    def test_returns_refusal_when_order_file_names_no_project(self, tmp_path) -> None:
+        order_file = tmp_path / "order.md"
+        order_file.write_text("Do something.\n", encoding="utf-8")
+
+        from packages.orchestration.serve_runs import OrderRecord
+
+        record = OrderRecord(
+            order_id="ord-abc",
+            pid=1,
+            started_at="2026-01-01T00:00:00Z",
+            order_file=str(order_file),
+            out_log="",
+            err_log="",
+        )
+        client = _client("bot", (_UUID_A,))
+        with (
+            patch("packages.orchestration.serve_paths.serve_paths"),
+            patch(
+                "packages.orchestration.serve_runs.read_order_record",
+                return_value=record,
+            ),
+        ):
+            result = client_order_read_refusal(client, "ord-abc")
+        assert result is not None
+        assert "may not read order" in result
+
+    def test_returns_refusal_when_client_does_not_list_order_project(
+        self, tmp_path
+    ) -> None:
+        order_file = tmp_path / "order.md"
+        order_file.write_text(
+            f"---\nproject: {_UUID_B}\n---\nDo something.\n", encoding="utf-8"
+        )
+
+        from packages.orchestration.serve_runs import OrderRecord
+
+        record = OrderRecord(
+            order_id="ord-abc",
+            pid=1,
+            started_at="2026-01-01T00:00:00Z",
+            order_file=str(order_file),
+            out_log="",
+            err_log="",
+        )
+
+        from packages.orchestration.project_registry import RemyProject
+
+        project = RemyProject(id=UUID(_UUID_B), name="beta", slug="beta")
+
+        # client only lists A, not B
+        client = _client("bot", (_UUID_A,))
+
+        with (
+            patch("packages.orchestration.serve_paths.serve_paths"),
+            patch(
+                "packages.orchestration.serve_runs.read_order_record",
+                return_value=record,
+            ),
+            patch(
+                "packages.orchestration.project_registry.select_project",
+                return_value=(project, "registry"),
+            ),
+            patch(
+                "packages.orchestration.api_clients.client_lists_project",
+                side_effect=lambda c, keys: any(k in c.projects for k in keys),
+            ),
+        ):
+            result = client_order_read_refusal(client, "ord-abc")
+        assert result is not None
+        assert "may not read order" in result
```

`run_defects.txt` verbatim:

```
NONE
```

No finding registered by me for this run; the reviewer registers any self-use run defect in the
next round's first commit, per the block.

## Closure suite

`.agent/authored/f152-closure-suite.txt` whole and verbatim:

```
command: python3 -m pytest -n auto -q
real exit code: 1
wall time: 330.0s (the launcher's reading); pytest's own reported wall time: 329.18s (0:05:29)
summary line: 1 failed, 23940 passed, 11 skipped, 1 warning in 329.18s (0:05:29)
bad node ids (failed + errors):
  - tests/orchestration/test_env_registry.py::test_every_remedy_name_production_code_spells_is_registered
leftover processes: NONE
tree it ran on: 7816704be (F152 R7 C3: the closure's self-use item run to its approval gate, never applied)
tree note: C1 to C3 changed only .agent/ files, the checklist page and the self-use queue
reflog before: 7816704be HEAD@{2026-10-24 10:10:25 +0200}: commit: F152 R7 C3: the closure's self-use item run to its approval gate, never applied
reflog after: 7816704be HEAD@{2026-10-24 10:10:25 +0200}: commit: F152 R7 C3: the closure's self-use item run to its approval gate, never applied
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F152 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1405.29 CPU seconds, 329.21 wall seconds, 23952 tests collected, exit status 1, recorded 2026-10-24T08:16:02Z
This closure's suite used 1405.29 CPU seconds, 0.6 percent less than F157's 1413.16, within the 10 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 0 percent.
The test modules whose CPU time rose most since F157's closure run:
  +2.98 s  tests/test_grouped_cli.py (30.80 -> 33.78)
  +2.88 s  tests/serve_http_handler/test_public_api.py (15.14 -> 18.02)
  +2.71 s  tests/orchestration/test_task_deliverables.py (3.15 -> 5.86)
  +2.34 s  tests/orchestration/test_self_use_runner.py (4.74 -> 7.08)
  +1.96 s  tests/test_structure_ratchet.py (1.59 -> 3.55)
  +1.54 s  tests/cli/test_do_scale_matrix.py (37.87 -> 39.41)
  +1.47 s  tests/orchestration/test_run_manifest_prework_resume.py (2.94 -> 4.41)
  +1.24 s  tests/orchestration/test_review_zip_hygiene.py (38.04 -> 39.28)
  +1.20 s  tests/orchestration/test_run_manifest_task_lifecycle_binding.py (3.41 -> 4.61)
  +1.20 s  tests/orchestration/test_public_api_gate_paths.py (18.91 -> 20.11)
```

## Deviations & assumptions

1. My first launch of the self-use command (`python3 .remedy-wt/f152-r7/prep/launch.py selfuse
   .remedy-wt/f152-r7-worker`) ran with the Bash tool's own default working directory
   (`.remedy-wt/`), not the repository root, because the block forbids `cd` and the sandbox refuses
   compound shell shapes. `launch.py`'s subprocess therefore looked for
   `.agent/authored/f152-r7-selfuse.py` relative to `.remedy-wt/` and exited `2` at once with
   `FileNotFoundError` — zero bytes of the reviewer's self-use script ran, no provider call was
   made, no file under `.agent/selfuse_f152/` was written. I deleted the two resulting artifacts
   (`.remedy-wt/f152-r7-worker/selfuse.log`, `.remedy-wt/f152-r7-worker/selfuse.exit`, two statically
   named paths, no wildcard) and relaunched through a small `python3` wrapper under
   `.remedy-wt/f152-r7-worker/` that calls `subprocess.run([...], cwd=repo_root)`, so `launch.py`'s
   own child process runs from the repository root as the block orders, without a shell `cd`. The
   self-use run reported above is that second, real attempt; the discarded first attempt executed
   none of the reviewer's script.
2. The same `cwd`-setting wrapper was used proactively for the suite launch, since the same Bash
   working-directory mismatch would otherwise have applied there too; no failed attempt occurred
   for the suite.
3. The full suite is RED: one failing test,
   `tests/orchestration/test_env_registry.py::test_every_remedy_name_production_code_spells_is_registered`.
   Committed exactly as read, per C4 point 6 — not investigated, not re-run, not repaired this
   round; the repair is the next round's reviewer-authored block.

No other departure from the block's ordered commit sequence: no split, no correction commit, no
file touched outside the paths named per commit, no second test command, no
`REMEDY_TEST_MAX_WORKERS`, no `claude` binary invoked by me.

## For the operator, in plain sentences

The paid run was asked to write the first tests for one module nobody had tested yet, and it
ended with the reviewer approving the result, though the change was never applied to this branch.
This was the first time this feature's own command-line flags and cleaned-up settings, rather than
your personal ones, started that model, and it worked. Across the whole test collection, 23,940
tests passed and 1 failed. The whole run took a little over five minutes. The cost reading said
this feature's computer time was about six tenths of a percent lower than the feature closed just
before it, comfortably inside the allowed range.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | four files byte-equal to the prepared snapshots |
| C2 | done | numstat `14 0`, consolidation paragraph added, list stays at 34 items |
| C3 | done | SU-082 run to its approval gate (pass), never applied; eleven files, one queue entry |
| C4 | done | one full suite run (red, one bad node id), cost script exit 0 within budget |
| C5 | done | this handback |
| Gate 1 | done | every line `True`, last line `ALL True` |
| Gate 2 | done | all eleven self-use files non-empty, sizes reported |
| Gate 3 | done | exit 1, one bad node id, no leftover process |
| Gate 4 | done | `fail_count` 0, all six checks pass; eight open ids match the block |
| Push | pending | runs once immediately after this commit |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work.
2. Phase 1 rule 2: the Open PR Gate — no pull request is open for this branch yet.
3. The reviewer reviews round 7, books its verdict and registers every self-use run defect in the
   next round's first commit.
4. A repair round naming every bad node id (the suite is red).
5. The closing round: the Built State, the rotation, the STATUS line, the README and the pull
   request.

Operator questions open: 3.
Open findings: 8.
