# Handback — F314 "Findings paydown v10," round 7

## Session

SESSION 1 of feature F314 · round 7 · rounds so far 7

Context self-assessment: this session booked round 6's PASS verdict and R-1449's registration
(already landed in C1, prepared by the reviewer), repaired R-1449's half-sentence comment, added
F314's consolidation paragraph, ran the closure's self-use item to its approval gate and the
feature's one full suite exactly once each, and is about to push with ample context remaining.

State block:
Feature F314 (claimed `[~]`), branch `feature/f314-findings-paydown-v10`, base `bd41c4b69`.
Fortschritt: ~90 % (T001 to T008 landed; the consolidation pass, the self-use run and the one full
suite done · the evidence, the package and the closing round remain) — Schätzung

## Range

Review of `bd41c4b69`..HEAD.

## Commits

### 60649aa6f F314 R7 C1: book round 6, register R-1449, the plan, the block and the self-use script
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f314-r7.md` | +159/-0 | NEW FILE; byte copy of this round's block, `block.md` |
| `.agent/authored/f314-r7-selfuse.py` | +133/-0 | NEW FILE; byte copy of the reviewer-authored self-use runner script |
| `.agent/live_review.md` | +4/-0 | round 6's PASS gate entry and R-1449's registration appended |
| `.agent/plan.md` | +6/-6 | rewritten for F314 round 7 |

All four paths are byte copies of the reviewer's prepared `c1-*` files; gate 1's `verify.py` and a
direct byte-equality check (see Authored-text proofs) confirm each equality.

### 76b46ba0c F314 R7 C2: run_job's veto terminal comment is one whole sentence (R-1449)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_job.py` | +1/-1 | the half-sentence comment above `settle_veto_terminal`'s call replaced by one whole sentence naming it and DECISION F314 D9, per the reviewer's prepared `c2-*` byte copy |

### db159c470 F314 R7 C3: the checklist's consolidation pass for F314
| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | +12/-0 | F314's consolidation paragraph appended to item 34: nothing joined, no two items merged, the list stays at 34 items, per the reviewer's prepared `c3-*` byte copy |

### 277c8184c F314 R7 C4: the closure's self-use item run to its approval gate, never applied
| Path | +/- | Reason |
|---|---|---|
| `scripts/self_use_queue.json` | +8/-0 | one entry appended by `generate_and_append_if_empty()`: `SU-080`, "Address ledger finding R-1448," tier 1, `consumed_by` empty |
| `.agent/selfuse_f314/SU-080.md` | +10/-0 | NEW FILE; the job markdown the run planned from the queue entry |
| `.agent/selfuse_f314/changed_paths.txt` | +4/-0 | NEW FILE; the job's own changed paths on its own branch |
| `.agent/selfuse_f314/entry_and_job_file.txt` | +5/-0 | NEW FILE; the entry's id, title, provenance and job file path |
| `.agent/selfuse_f314/execution_config.txt` | +43/-0 | NEW FILE; the job's resolved builder/reviewer execution config |
| `.agent/selfuse_f314/full_transcript.txt` | +14/-0 | NEW FILE; the job's task summary transcript |
| `.agent/selfuse_f314/job_diff.txt` | +232/-0 | NEW FILE; `git diff HEAD...remedy/job-480f4964cc1f4cdb`, never applied to this tree |
| `.agent/selfuse_f314/result_state.txt` | +12/-0 | NEW FILE; the job plan's state, budgets, budget actuals and per-task status |
| `.agent/selfuse_f314/run_defects.txt` | +1/-0 | NEW FILE; `describe_self_use_run_defects()` answered an empty tuple, written as `NONE` |
| `.agent/selfuse_f314/staleness_after.txt` | +2/-0 | NEW FILE; the staleness catalog read from the job's own branch after the run |
| `.agent/selfuse_f314/timing.txt` | +3/-0 | NEW FILE; start/finish timestamps and wall seconds |

The script installed the adapter registry into the worker adapter slot (DECISION F315 D2) before
running the job; it was never edited, exited 0, and was run exactly once per the launcher/wait
scripts. Every written file was checked afterward to hold no path of this machine (gate inside the
script itself, verified again by the reviewer's `verify.py` in Gate 1).

### 076d22f1d F314 R7 C5: the closure's one full suite and its CPU cost
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f314-closure-suite.txt` | +27/-0 | NEW FILE; the one full-suite transcript (`python3 -m pytest -n auto -q`) and the `closure_suite_cost.py` reading, in the shape of `f315-closure-suite.txt` |

### this commit — F314 R7 C6: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | n/a (self-reference; R-0149 pattern) | this handback, rewritten per `docs/agents/handback_template.md` |

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `60649aa6f`, exactly the four named paths, each byte-equal to its prepared `c1-*` file |
| C2 | done | `76b46ba0c`, `packages/orchestration/pingpong_job.py` alone, numstat `1 1` |
| C3 | done | `db159c470`, `docs/agents/planner_reviewer_prompt.md` alone, numstat `12 0` |
| C4 | done | `277c8184c`, the self-use item (`SU-080`) run to its approval gate, never applied; exit 0 |
| C5 | done | `076d22f1d`, the one full suite (exit 0, `23783 passed, 11 skipped`) and the cost reading (exit 1, over the limit) |
| C6 | done | this commit |
| Gate 1 (`verify.py`) | done | every line `True`, `C6` read `absent`, last line `ALL True` |
| Gate 2 (ten selfuse files) | done | all ten non-empty, sizes recorded below |
| Gate 3 (suite transcript) | done | exit 0, `23783 passed, 11 skipped, 1 warning in 452.72s (0:07:32)`, bad node ids `NONE` |
| Gate 4 (integrity + open ids) | done | `"fail_count": 0`; open ids the eight named: `R-1246, R-1281, R-1351, R-1353, R-1426, R-1428, R-1448, R-1449` |
| Push | done | see External actions / the reply after this handback |

## External actions

- `git push origin feature/f314-findings-paydown-v10` — to run immediately after this commit,
  carrying `60649aa6f`, `76b46ba0c`, `db159c470`, `277c8184c`, `076d22f1d` and this handback's own
  commit; see the reply for the push's own result.
- No PR created, edited or merged by this session (the block records that none is open for this
  branch yet, and none is ordered by this round). No `gh` command run. No `git worktree add` by
  this session; the self-use script itself added and removed one temporary worktree at
  `.remedy-wt/f314-r7-jobtree` to read the job branch's staleness catalog, then removed it and
  pruned, both inside the reviewer-authored script.
- One scratch directory used, `.remedy-wt/f314-r7-worker/` (created this round), holding the C1/C2/C3
  byte-copy-and-verify scripts and the Gate 2 size-reporting script, plus the launcher's own
  `selfuse.log`/`selfuse.exit` and `suite.log`/`suite.exit`. `.remedy-wt/f314-r7/` (the reviewer's
  prepared tree) was only read, never written.

## Verification

Gate order per the block, run once each, after C5 and before this handoff.

1. `git status --porcelain` → empty.
   `python3 .remedy-wt/f314-r7/prep/verify.py .` → every line `True` (`C6` read `absent`), last
   line `ALL True`. (Full output recorded in the session transcript; every path-equality and
   numstat check for C1 through C5 passed.)

2. The ten files under `.agent/selfuse_f314/`, each non-empty:
   ```
   SU-080.md                1942 bytes
   entry_and_job_file.txt    224 bytes
   execution_config.txt     1367 bytes
   result_state.txt          866 bytes
   timing.txt                 105 bytes
   changed_paths.txt          137 bytes
   full_transcript.txt       1543 bytes
   staleness_after.txt        200 bytes
   job_diff.txt             12931 bytes
   run_defects.txt              5 bytes
   ```

3. The suite of C5 (`python3 -m pytest -n auto -q`): exit code `0`; summary line
   `23783 passed, 11 skipped, 1 warning in 452.72s (0:07:32)`; bad node ids (failed + errors):
   `NONE`.

4. `python3 -m apps.cli.main integrity check --json` →
   `{"check_count": 6, "checks": [{"message": "handlers=201", "name": "handler_import", "status":
   "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status":
   "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency",
   "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked",
   "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root",
   "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings",
   "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true,
   "schema_version": 1, "version": 1}`.
   `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
   → `['R-1246', 'R-1281', 'R-1351', 'R-1353', 'R-1426', 'R-1428', 'R-1448', 'R-1449']` — the eight
   named ids.

## Self-use run

- Entry id: `SU-080`. Title: "Address ledger finding R-1448." Provenance: generated
  (self-use-generator tier 1, ledger scan, R-1448).
- Job id: `480f4964cc1f4cdb`.
- Builder: `claude-cli`, model `claude-sonnet-4-6`, effort `medium` (source `cli` for all three).
  Reviewer: `claude-cli`, model `claude-sonnet-4-6`, effort `medium` (source `cli` for all three).
- Job state: `completed`. Stop reason: (empty). Stop source: (empty).
- Task `T001`: status `applied_to_job_workspace`; reviewer verdict `pass`; final status
  `staged_review_passed`; repair rounds used `0`.
- Wall seconds: `396.1`.
- Changed paths (on the job's own branch, never applied here):
  ```
  apps/cli/commands/do_cmd.py
  packages/orchestration/project_roles.py
  tests/cli/test_do_flags.py
  tests/orchestration/test_project_roles.py
  ```
- Job diff (`job_diff.txt`), verbatim:
  ```
  $ git diff HEAD...remedy/job-480f4964cc1f4cdb  (exit 0)
  diff --git a/apps/cli/commands/do_cmd.py b/apps/cli/commands/do_cmd.py
  index 091d05974..d379cf9b3 100644
  --- a/apps/cli/commands/do_cmd.py
  +++ b/apps/cli/commands/do_cmd.py
  @@ -441,6 +441,19 @@ def _cmd_do(
                   f"planner; the planners are {', '.join(PLANNER_PROVIDERS)}. "
                   "Nothing was run.", json_output=json_output, exit_code=2)

  +    # R-1448: read the project's [roles] table once, before any step, so every
  +    # planner call in the walk uses the same provider.  A table that cannot be
  +    # used is refused with exit 2 before any step.  When no --planner-provider
  +    # was given, the table's planner (if any) is used instead.
  +    from packages.orchestration.project_roles import ProjectRolesError, read_project_roles
  +    try:
  +        _project_roles = read_project_roles(repo)
  +    except ProjectRolesError as exc:
  +        fail("invalid_roles_table", f"{exc} Nothing was run.",
  +             json_output=json_output, exit_code=2)
  +    if planner_provider is None:
  +        planner_provider = _project_roles.get("planner") or None
  +
       # DECISION F269 D1 (4): a name that is not a template exits 2 before any step.
       if contract is not None:
           from packages.orchestration.contract_templates import list_contract_templates
  diff --git a/packages/orchestration/project_roles.py b/packages/orchestration/project_roles.py
  index a170660e5..0331cbdab 100644
  --- a/packages/orchestration/project_roles.py
  +++ b/packages/orchestration/project_roles.py
  @@ -1,15 +1,12 @@
  -"""R-1326: a project's own choice of builder and reviewer provider, read from the `[roles]` table
  -of its `.remedy/config.toml` (DECISION F314 D4, D5).
  +"""R-1326: a project's own choice of builder, reviewer and planner provider, read from the
  +`[roles]` table of its `.remedy/config.toml` (DECISION F314 D4, D5, R-1448).

   `read_project_roles` is the one place that table is read. `resolve_job_execution_config` in
  -`execution_config.py` reads it for the builder and the reviewer. The table sits above the product
  -default and below an explicit option or a continued job's own persisted record.
  -
  -DECISION F314 D5 (2): the table does not yet choose the planner. `resolve_planner_target` in
  -`intake.py` is called at four places of a `remedy do` walk without the walk's repository, and
  -reading the table at one of them would make the walk record one planner and call another; a
  -`planner` key is refused instead, naming `--planner-provider` and `planner.provider` of
  -`remedy.toml` as the ways to choose the planner today. R-1448 carries the design that reads it.
  +`execution_config.py` reads it for the builder and the reviewer. `_cmd_do` in
  +`apps/cli/commands/do_cmd.py` reads it once before any step for the planner (R-1448): it
  +passes the resolved `planner_provider` through `DoContext` so every planner call in the walk
  +uses the same provider. The table sits above the product default and below an explicit option
  +or a continued job's own persisted record.
   """
   from __future__ import annotations

  @@ -23,8 +20,8 @@ try:                                   # Python >= 3.11
    except ModuleNotFoundError:            # Python 3.10 with the tomli backport
        import tomli as tomllib  # type: ignore[no-redef]

  -#: The only keys a `[roles]` table may name (DECISION F314 D5 (2); `planner` is refused, R-1448).
  -PROJECT_ROLES_KEYS = ("builder", "reviewer")
  +#: The keys a `[roles]` table may name (R-1448: `planner` accepted; DECISION F314 D4, D5).
  +PROJECT_ROLES_KEYS = ("builder", "reviewer", "planner")


   class ProjectRolesError(ValueError):
  @@ -38,12 +35,12 @@ def read_project_roles(repo_root: str | Path | None) -> dict[str, str]:
        says nothing about its roles changes nothing downstream. Raises :class:`ProjectRolesError`,
        each message naming the file's relative path `.remedy/config.toml` and the table `[roles]`
        and saying what to write instead, when: the file cannot be read or parsed; `roles` is not a
  -    table; the key is `planner` (DECISION F314 D5 (2); R-1448 carries the design that accepts it
  -    again); a key is not one of `PROJECT_ROLES_KEYS`; a value is not a non-empty string; or
  -    `builder` or `reviewer` names a provider outside `ROLE_PROVIDER_NAMES`, or `builder` names one
  -    `non_writing_provider_refusal` refuses.
  +    table; a key is not one of `PROJECT_ROLES_KEYS`; a value is not a non-empty string; `builder`
  +    or `reviewer` names a provider outside `ROLE_PROVIDER_NAMES`, or `builder` names one
  +    `non_writing_provider_refusal` refuses; or `planner` names a value outside `PLANNER_PROVIDERS`
  +    (R-1448: `planner` is now accepted; `_cmd_do` reads it once before any step).

  -    The two name sets are imported here rather than at module level: `non_writing_provider_refusal`
  +    The name sets are imported here rather than at module level: `non_writing_provider_refusal`
        lives on `do_role_guards.py`, and a module-level import of either risks a cycle with a caller
        that imports this module for the resolution it holds.
        """
  @@ -70,26 +67,30 @@ def read_project_roles(repo_root: str | Path | None) -> dict[str, str]:

        result: dict[str, str] = {}
        for key, value in table.items():
  -        if key == "planner":
  -            raise ProjectRolesError(
  -                f"{CONFIG_RELPATH}: [roles] does not choose the planner; choose it with "
  -                f"--planner-provider or planner.provider of remedy.toml instead")
            if key not in PROJECT_ROLES_KEYS:
                raise ProjectRolesError(
  -                f"{CONFIG_RELPATH}: [roles] names {key!r}; write builder or reviewer instead")
  +                f"{CONFIG_RELPATH}: [roles] names {key!r}; "
  +                f"write one of {', '.join(PROJECT_ROLES_KEYS)} instead")
            if not isinstance(value, str) or not value:
                raise ProjectRolesError(
                    f"{CONFIG_RELPATH}: [roles].{key} must be a non-empty string naming a provider, "
                    f"got {value!r}")
  -        if value not in ROLE_PROVIDER_NAMES:
  -            raise ProjectRolesError(
  -                f"{CONFIG_RELPATH}: [roles].{key} names {value!r}, which is not a provider; "
  -                f"write one of {', '.join(sorted(ROLE_PROVIDER_NAMES))} instead")
  -        if key == "builder":
  -            refusal = non_writing_provider_refusal("builder", value)
  -            if refusal:
  +        if key == "planner":
  +            from packages.orchestration.intake import PLANNER_PROVIDERS
  +            if value not in PLANNER_PROVIDERS:
  +                raise ProjectRolesError(
  +                    f"{CONFIG_RELPATH}: [roles].planner names {value!r}, which is not a planner; "
  +                    f"write one of {', '.join(PLANNER_PROVIDERS)} instead")
  +        else:
  +            if value not in ROLE_PROVIDER_NAMES:
                    raise ProjectRolesError(
  -                    f"{CONFIG_RELPATH}: [roles].builder names {value!r}, which cannot write "
  -                    f"files; write a provider that can, such as pi, instead")
  +                    f"{CONFIG_RELPATH}: [roles].{key} names {value!r}, which is not a provider; "
  +                    f"write one of {', '.join(sorted(ROLE_PROVIDER_NAMES))} instead")
  +            if key == "builder":
  +                refusal = non_writing_provider_refusal("builder", value)
  +                if refusal:
  +                    raise ProjectRolesError(
  +                        f"{CONFIG_RELPATH}: [roles].builder names {value!r}, which cannot write "
  +                        f"files; write a provider that can, such as pi, instead")
            result[key] = value
        return result
  diff --git a/tests/cli/test_do_flags.py b/tests/cli/test_do_flags.py
  index ab008b7ad..2a37a913b 100644
  --- a/tests/cli/test_do_flags.py
  +++ b/tests/cli/test_do_flags.py
  @@ -234,6 +234,56 @@ def test_planner_model_reaches_every_structured_planner_call(repo, capsys, monke
        assert [model for _name, model in calls] == ["p1"] * len(calls), calls


  +# ── R-1448: the [roles] table's planner ──────────────────────────────────────
  +
  +
  +def test_roles_table_planner_is_used_when_no_planner_provider_flag(repo, capsys, monkeypatch):
  +    """R-1448: a project's [roles] table with planner = "ollama" is read once in _cmd_do
  +    before any step and used when --planner-provider was not given, causing
  +    make_structured_call_fn to be called with provider="ollama" rather than
  +    make_provider_call_fn (which is what happens when planner_provider is None)."""
  +    calls: list[tuple[str, object]] = []
  +
  +    def recorder(model_cls, **kwargs):
  +        calls.append((model_cls.__name__, kwargs.get("provider")))
  +        return None
  +
  +    monkeypatch.setattr("packages.orchestration.intake.make_structured_call_fn", recorder)
  +    monkeypatch.setattr("packages.orchestration.study.study_call_fn", lambda *a, **kw: None)
  +
  +    (repo / ".remedy").mkdir(exist_ok=True)
  +    (repo / ".remedy" / "config.toml").write_text('[roles]\nplanner = "ollama"\n', encoding="utf-8")
  +
  +    data = json.loads(_do(capsys, "--json", "--plan-only", llm=True,
  +                          order="Write CONTRIBUTING.md, CHANGELOG.md, CODE_OF_CONDUCT.md and SUPPORT.md"))
  +
  +    assert data["ok"] is True
  +    assert any(provider == "ollama" for _name, provider in calls), (
  +        f"Expected make_structured_call_fn called with provider='ollama' from the [roles] table; "
  +        f"got calls: {calls}")
  +
  +
  +def test_an_invalid_roles_table_exits_2_before_any_step(repo, capsys):
  +    """R-1448: a [roles] table that cannot be used is refused with exit 2 before any step."""
  +    from packages.orchestration.pingpong_job import list_job_plans
  +    from packages.orchestration.project_registry import resolve_project
  +
  +    (repo / ".remedy").mkdir(exist_ok=True)
  +    (repo / ".remedy" / "config.toml").write_text(
  +        '[roles]\nplanner = "no-such-planner"\n', encoding="utf-8")
  +
  +    code, out, err = _exit_code_and_output(capsys)
  +
  +    assert code == 2
  +    assert err == ""
  +    body = json.loads(out)
  +    assert body["ok"] is False
  +    assert body["error"] == "invalid_roles_table"
  +    assert "Nothing was run." in body["message"]
  +    assert resolve_project(repo) is None
  +    assert list_job_plans() == []
  +
  +
   # ── one route under `do` (DECISION F268 D16 (1), (2), R-0933) ────────────────


   class TestTheRefusals:
  @@ -83,8 +98,8 @@ class TestTheRefusals:
            with pytest.raises(ProjectRolesError, match="cannot write files"):
                read_project_roles(tmp_path)

  -    def test_a_planner_key_is_refused(self, tmp_path: Path) -> None:
  -        """DECISION F314 D5 (2): the table does not yet choose the planner (R-1448)."""
  -        _write_config(tmp_path, '[roles]\nplanner = "ollama"\n')
  -        with pytest.raises(ProjectRolesError, match="--planner-provider"):
  +    def test_a_planner_value_outside_planner_providers_is_refused(self, tmp_path: Path) -> None:
  +        """R-1448: [roles].planner with a value that is not a planner is refused."""
  +        _write_config(tmp_path, '[roles]\nplanner = "bogus-planner"\n')
  +        with pytest.raises(ProjectRolesError, match="is not a planner"):
            read_project_roles(tmp_path)
  ```
- `run_defects.txt`, verbatim: `NONE`.

No finding registered by this session from this run (the defects tuple was empty); the next
round's first commit is where the reviewer books any defect it finds and any cost-limit finding
the closure protocol's precondition 2 names.

## Closure suite

Quoting `.agent/authored/f314-closure-suite.txt` whole and verbatim:

```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 453.5s (the launcher's reading); pytest's own reported wall time: 452.72s (0:07:32)
summary line: 23783 passed, 11 skipped, 1 warning in 452.72s (0:07:32)
bad node ids (failed + errors): NONE
leftover processes: NONE
tree it ran on: 277c8184c (F314 R7 C4: the closure's self-use item run to its approval gate, never applied)
tree note: C1 to C4 changed only .agent/ files, one comment line of pingpong_job.py, the checklist page and the self-use queue
reflog before: 277c8184c HEAD@{2026-10-24 02:17:16 +0200}: commit: F314 R7 C4: the closure's self-use item run to its approval gate, never applied
reflog after: 277c8184c HEAD@{2026-10-24 02:17:16 +0200}: commit: F314 R7 C4: the closure's self-use item run to its approval gate, never applied
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F314 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 1
Test load: 1387.98 CPU seconds, 452.74 wall seconds, 23794 tests collected, exit status 0, recorded 2026-10-24T00:24:54Z
This closure's suite used 1387.98 CPU seconds, 10.6 percent more than F315's 1255.17; that is above the 10 percent limit, so this closure registers a finding owned by the rolling findings paydown.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 0 percent.
The test modules whose CPU time rose most since F315's closure run:
  +12.20 s  tests/cli/test_do_scale_matrix.py (31.97 -> 44.17)
  +7.51 s  tests/cli/test_do_sequence_cli.py (26.66 -> 34.17)
  +5.73 s  tests/orchestration/test_subtree_rerun_prepare.py (9.68 -> 15.41)
  +5.57 s  tests/orchestration/test_persisted_call_ownership.py (8.43 -> 14.00)
  +5.23 s  tests/orchestration/test_serve_daemon.py (19.74 -> 24.97)
  +4.95 s  tests/orchestration/test_self_use_runner.py (4.02 -> 8.97)
  +4.72 s  tests/orchestration/test_job_worktree_integration.py (6.24 -> 10.96)
  +4.11 s  tests/cli/test_status_cmd.py (5.60 -> 9.71)
  +4.07 s  tests/orchestration/test_token_ledger.py (7.94 -> 12.01)
  +4.03 s  tests/orchestration/test_run_manifest_task_lifecycle_binding.py (2.73 -> 6.76)
```

## Authored-text proofs

- `.agent/authored/f314-r7.md` against `block.md`: both 159 lines, sha256
  `9c867ca2d031e68079fef687af672013ac36b446dd3ca072ed2da932c96a7d61` on both. Byte-identical.
- `.agent/authored/f314-r7-selfuse.py` against `.remedy-wt/f314-r7/prep/c1-.agent__authored__f314-r7-selfuse.py`:
  sha256 `5b75e85a0912a9a6b19fd9e1aa8a84d60cc9cdbb33be438c6750a5ce040dbd40` on both. Byte-identical.
- `.agent/live_review.md` against `.remedy-wt/f314-r7/prep/c1-.agent__live_review.md`: sha256
  `e86f84ea92e55e5494f49b516eb936425a4cb835a9cd3cb393bd6cc4e09561bc` on both. Byte-identical.
- `.agent/plan.md` against `.remedy-wt/f314-r7/prep/c1-.agent__plan.md`: sha256
  `75f67c185f301398db40255393b636dc7232c59326aec68c1881de49a7bd5eb8` on both. Byte-identical.
- `packages/orchestration/pingpong_job.py` against `.remedy-wt/f314-r7/prep/c2-packages__orchestration__pingpong_job.py`:
  sha256 `4e6eaeb34a6ac5a5f888e77737b58958a17ecab3be7ff2a64f31c93a7e51b575` on both. Byte-identical.
- `docs/agents/planner_reviewer_prompt.md` against `.remedy-wt/f314-r7/prep/c3-docs__agents__planner_reviewer_prompt.md`:
  sha256 `712f40f271eda8ba9ddf2e12ed10cb2bc8b3d5d2040b973bf0d1cce446b3ac14` on both. Byte-identical.

Before using any prepared file, `.remedy-wt/f314-r7/prep/digests.txt` was checked against its own
stated sha256 (`193862abff48cdba3619de278053edb8335ddb27c9193f48f547df59dc1570a7`, matched), then
every one of its ten listed entries was checked with `sha256sum -c digests.txt` and every line
read `OK`, before any prepared file was copied, run or read.

The self-use runner script (`.agent/authored/f314-r7-selfuse.py`) and the C4 job's own diff are
reviewer-authored/job-produced text, not applied to this tree: the script ran unedited, and the
job's diff lives only on its own branch, never merged here (see `## Self-use run` above).

## Deviations & assumptions

None. C1 through C6 landed in the block's exact order, on the one branch, with no extra, dropped
or reordered commit; every prepared byte was copied verbatim and proved equal before being staged;
the self-use script ran unedited, exited 0, and touched only the paths the block named; the one
full suite ran exactly once, after every other commit but the handback, with no marker, `-k`,
path, `--timeout` or `-x`, and no second test command this round; the cost script's exit 1 is the
reading the block itself calls "not a failure of this round," recorded verbatim in the C5
transcript and above, not a deviation from it.

## For the operator, in plain sentences

Before a feature closes, Remedy runs one real piece of work on itself with a paid model, and then
runs its whole test collection once on the code that will ship. The paid run was asked to teach
the tool's own command-line workflow to use a project's own written choice of which model plans
its work, and it ended with the reviewer approving the change as correct, though the change itself
was not applied to this branch. All of the tests passed and none failed, with a small number
skipped as usual. The whole run took a little over seven and a half minutes. The cost reading said
this feature's test run used about a tenth more computer time than the previous feature's did,
which is just over the normal allowance, so that gets written down as something to look at rather
than something that stops the work.

## Next

1. Phase 1 rule 1: if `.agent/STOP` exists, the next session finishes whatever commit is in hand,
   writes the handoff, pushes, and stops, before anything else.
2. Rule 2, the Open PR Gate: check for open pull requests before starting any new unrelated work;
   no pull request is open for this branch yet.
3. The reviewer reviews round 7, books its verdict and registers every self-use run defect in the
   next round's first commit.
4. The evidence bundle and the review package.
5. The closing round: the Built State, the rotation, the next findings paydown, the STATUS line,
   the README and the pull request.

Operator questions open: 2. Open findings: 8.
