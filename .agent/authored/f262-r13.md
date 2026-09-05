═══════════════════════════════════════════════════════════════
STEP — F262 R13/? — T003 batch 1: shared list-options helper + job.list wiring
═══════════════════════════════════════════════════════════════

GOAL: Start T003 (sort/filter/limit behaviour, newest-first default) with its first batch. T002's per-command date work is done or excused for all 18 catalog list commands (round 12 closed the last gap). Build ONE shared helper — `packages/orchestration/list_options.py` — that filters by `--since`/`--until`, orders by `--sort`/`--desc` (newest-first is the DEFAULT with no flags at all), and caps by `--limit`, instead of 18 hand-rolled implementations (the design question `.agent/plan.md`'s Next Steps named). Wire it into `job.list` end to end as the first proof of the design; the remaining 17 commands are later T003 batches, the same batch-by-batch pacing T002 used across rounds 2-12. Also book round 12's reviewer verdict into the ledger, plus one `.agent/prose_slips.md` line for an arithmetic slip the reviewer's own round 12 block made.

BACKGROUND FACTS (already verified by the reviewer — do not re-derive):
- Every list command's catalog entry already carries `--sort`/`--desc`/`--since`/`--until`/`--limit` (T001's `_with_list_options()` in `apps/cli/command_catalog.py` injects them into every list-shaped entry). NO handler currently reads any of `args.sort`/`args.desc`/`args.since`/`args.until`/`args.limit` — confirmed by the reviewer with `grep -rln "args\.sort\|args\.desc\|args\.since\|args\.until\|args\.limit" apps/cli/commands/*.py`, zero hits. T003 is greenfield behaviour, not a bug fix.
- `job.list`'s handler (`_cmd_list_jobs` in `apps/cli/commands/job.py`) builds ITS SAME `jobs` list (a `list[Job]`, from `packages.core.models`) for both the `--json` branch and the text branch — a single reassignment of `jobs` before either branch changes both at once, no separate logic needed per branch.
- `Job.created_at` (`packages/core/models.py`) is a real `datetime` object already, not a string — sort on it directly, never re-parse it from its own `.isoformat()`.
- No existing test in `tests/test_grouped_cli.py`'s `TestJobListCLI` class or elsewhere asserts a particular ORDER for `job.list`'s output — confirmed by the reviewer; only single-job / `rc == 0` / key-presence checks exist today, so imposing a real default order is safe.

═══ COMMIT SEQUENCE (5 commits total) ═══

──────────────────────────────────────────────────────────
C0a — save this entire step block verbatim
──────────────────────────────────────────────────────────
Save the FULL literal text of this prompt message (everything between the "STEP —" header above and the final "END OF BLOCK" marker at the bottom) to `.agent/authored/f262-r13.md`, byte for byte, exactly as received. Commit message: `F262 R13 C0a: save block verbatim to .agent/authored/f262-r13.md`

──────────────────────────────────────────────────────────
C0b — mirror to .agent/last_block.md
──────────────────────────────────────────────────────────
Copy `.agent/authored/f262-r13.md` to `.agent/last_block.md`, whole-file replace. Verify `sha256sum` of both files matches after writing. Commit message: `F262 R13 C0b: mirror block to .agent/last_block.md`

──────────────────────────────────────────────────────────
C1 — append GATE12 to .agent/live_review.md AND one line to .agent/prose_slips.md
──────────────────────────────────────────────────────────
Append exactly the text between the GATE12 markers below to the END of `.agent/live_review.md`: one newline, then the GATE12 text verbatim (it is a SINGLE LINE — no internal newlines), nothing else added.

<<<BEGIN GATE12>>>
Gate: R12 — the F262 R12 entry. R12 closed the last named T002 gap round 11's audit found: `test.list`'s TEXT branch gained a real per-row listing (test_run_id/status/exit_code/created) replacing a bare count-only print, plus an honest empty-state message — its `--json` branch needed no change since it already built the same `out["runs"]` shape the text branch now reuses — AND THE REVIEWER RE-RAN EVERY GATE ITSELF. TRANSPORT HELD: `.agent/authored/f262-r12.md`/`.agent/last_block.md` share one sha256 digest, `29ed10fe8418108ed320a1a3f7c37127d4835fb1c312b6bbd9a399e23f271210`, confirmed by the reviewer's own sha256sum of both committed files. THE DIFF WAS READ, NOT ONLY GATED: `git diff de9d412e..0bab90b9` for `apps/cli/commands/real_test_execution_cmd.py` and `tests/cli/test_real_test_execution_cli.py` shows exactly PAIR P1 (the text branch rewrite) and TEST T1's two new functions, every other line in both files untouched, confirmed by reading the full diff. `python3 -m py_compile` exited 0 on both touched files, run together by the reviewer. THE GATE11 LEDGER APPEND (commit c8d48c23) WAS RE-VERIFIED BYTE-EXACT: base (2449694 bytes) + one newline + GATE11 (2836 bytes, 0 internal newlines) reproduces the post-commit file (2452539 bytes) exactly. THE TESTS MOVED EXACTLY AS THE REAL RUN SHOWED, reproduced independently: `tests/cli/test_real_test_execution_cli.py` read 8 passed (6 pre-existing plus 2 new) — the round's OWN step block prose had predicted "expected 7 (5 pre-existing + 2 new)", a reviewer-authored miscount of the file's pre-existing test count, not a defect in the applied change; the worker's real pytest run reported the true number honestly rather than reconciling it, and this is routed to `.agent/prose_slips.md` in this same commit rather than an R-id, per amend0827 rule 2 (no product-effect defect). THE STATE READERS AND THE CANARY WERE UNMOVED, reproduced by the reviewer as ONE combined invocation: `tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py` read 646 passed, matching 515+52+21+16+42 exactly. HYGIENE HELD: `git status --porcelain` empty at HEAD `02f92f4c`, `git ls-files .remedy-wt` empty, `.agent/STOP` absent. THE PLAN HELD: `.agent/plan.md` measured 2312 bytes, matching the handback's own reported byte-for-byte comparison of the authored PLAN13 slice against the written file. THE VERDICT IS PASS.
<<<END GATE12>>>

Then append exactly the text between the PROSE_SLIP markers below to the END of `.agent/prose_slips.md`: one newline, then the text verbatim (single line, no internal newlines), nothing else added.

<<<BEGIN PROSE_SLIP>>>
2026-09-04 · F262 R12 (reviewer) · The R12 step block's own prose predicted `tests/cli/test_real_test_execution_cli.py`'s post-round pytest count as "expected 7 (5 pre-existing + 2 new)"; the file actually held 6 pre-existing tests before the round, so the correct total after C2's two new tests is 8, exactly what the worker's real pytest run reported — the worker reported the true number honestly rather than reconciling it to match the wrong prediction. Reviewer-authored miscount in the block's own prose, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).
<<<END PROSE_SLIP>>>

Commit message: `F262 R13 C1: append GATE12 to live_review.md and one line to prose_slips.md - books round 12's PASS verdict`

──────────────────────────────────────────────────────────
C2 — production code + tests (one commit, one new production file, one production rewrite, two test files)
──────────────────────────────────────────────────────────

NEW FILE — create `packages/orchestration/list_options.py` with EXACTLY this content:
<<<BEGIN NEWFILE_LIST_OPTIONS>>>
"""
Shared sort/filter/limit behaviour for list commands (F262 T003).

One implementation, called by a list handler's own already-built row
list, instead of N hand-rolled copies. The same call produces the rows
for BOTH --json and text rendering, so behaviour and the newest-first
default stay identical between the two.

Public API::

    apply_list_options(rows, sort=, desc=, since=, until=, limit=,
                        sort_fields=, default_sort_field=,
                        date_getter=) -> list
    parse_time_bound(value) -> datetime
    ListOptionError
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from typing import Any, TypeVar

T = TypeVar("T")

_RELATIVE_UNITS = {"d": "days", "h": "hours", "m": "minutes", "s": "seconds"}


class ListOptionError(ValueError):
    """--sort/--since/--until/--limit could not be honoured; the CLI layer
    turns this into a clean stderr message and a non-zero exit, never a
    traceback."""


def parse_time_bound(value: str) -> datetime:
    """Parse an ISO-8601 timestamp or a relative form (2d, 12h, 30m, 45s)
    into an absolute, timezone-aware UTC datetime. A relative form always
    means "this far back from now"."""
    value = value.strip()
    if len(value) >= 2 and value[-1] in _RELATIVE_UNITS and value[:-1].isdigit():
        amount = int(value[:-1])
        unit = _RELATIVE_UNITS[value[-1]]
        return datetime.now(timezone.utc) - timedelta(**{unit: amount})
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ListOptionError(
            f"invalid time value {value!r}: expected ISO-8601 or a relative form like 2d/12h"
        ) from exc
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def apply_list_options(
    rows: list[T],
    *,
    sort: str | None,
    desc: bool,
    since: str | None,
    until: str | None,
    limit: str | None,
    sort_fields: dict[str, Callable[[T], Any]],
    default_sort_field: str,
    date_getter: Callable[[T], str | None] | None = None,
) -> list[T]:
    """Filter by --since/--until, order by --sort/--desc (newest-first is
    the DEFAULT with no flags at all), then cap by --limit — in that
    order. `sort_fields` maps a valid --sort NAME to a key function over a
    row; an unknown name raises ListOptionError naming the valid set.
    `date_getter` extracts a row's own date string for --since/--until; a
    store with no timestamp concept passes None and --since/--until are
    accepted but filter nothing."""
    out = list(rows)

    if (since or until) and date_getter is not None:
        lo = parse_time_bound(since) if since else None
        hi = parse_time_bound(until) if until else None
        filtered = []
        for row in out:
            raw = date_getter(row)
            if raw is None:
                continue
            try:
                dt = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
            except ValueError:
                continue
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            if lo is not None and dt < lo:
                continue
            if hi is not None and dt > hi:
                continue
            filtered.append(row)
        out = filtered

    field = sort or default_sort_field
    if field not in sort_fields:
        valid = ", ".join(sorted(sort_fields))
        raise ListOptionError(f"unknown --sort field {field!r}; valid fields: {valid}")
    is_default_reverse = field == default_sort_field
    reverse = (not desc) if is_default_reverse else desc
    out = sorted(out, key=sort_fields[field], reverse=reverse)

    if limit:
        try:
            n = int(limit)
        except ValueError as exc:
            raise ListOptionError(f"invalid --limit value {limit!r}: must be an integer") from exc
        out = out[:n]

    return out
<<<END NEWFILE_LIST_OPTIONS>>>

PAIR P1 (REWRITE) — `apps/cli/commands/job.py`, `_cmd_list_jobs` gains sort/since/until/limit wiring. This is the WHOLE current function body — re-read the file yourself first (lines 123-151) and confirm this FROM matches exactly before applying; if it does not match, STOP and report the mismatch rather than guessing.
FROM (exact):
<<<BEGIN PAIR_P1_FROM>>>
def _cmd_list_jobs(
    *,
    project: str | None = None,
    all_projects: bool = False,
    json_output: bool = False,
) -> None:
    from packages.orchestration.project_scope import resolve_scope, scoped_jobs

    scope = resolve_scope(project_flag=project, all_projects=all_projects)
    jobs, degraded, skipped = scoped_jobs(scope)
    if json_output:
        import json as _json
        print(_json.dumps({
            "version": 1,
            "job_count": len(jobs),
            "jobs": [{"id": str(job.id), "state": job.state.value, "name": job.name,
                     "created_at": job.created_at.isoformat(),
                     "project_id": job.project_id or ""} for job in jobs],
        }, sort_keys=True))
        return
    if not jobs:
        print("No jobs found.")
        return
    known = _known_project_ids()
    for job in jobs:
        label = _scope_label(job, scope, known)
        print(f"{job.id}  {job.state.value:<12}  {job.created_at.isoformat()}  {job.name}{label}")
    if skipped:
        print(f"  ({len(skipped)} unreadable job file(s) skipped)", file=sys.stderr)
<<<END PAIR_P1_FROM>>>
TO:
<<<BEGIN PAIR_P1_TO>>>
def _cmd_list_jobs(
    *,
    project: str | None = None,
    all_projects: bool = False,
    json_output: bool = False,
    sort: str | None = None,
    desc: bool = False,
    since: str | None = None,
    until: str | None = None,
    limit: str | None = None,
) -> None:
    from packages.orchestration.list_options import ListOptionError, apply_list_options
    from packages.orchestration.project_scope import resolve_scope, scoped_jobs

    scope = resolve_scope(project_flag=project, all_projects=all_projects)
    jobs, degraded, skipped = scoped_jobs(scope)
    try:
        jobs = apply_list_options(
            jobs,
            sort=sort, desc=desc, since=since, until=until, limit=limit,
            sort_fields={
                "created_at": lambda j: j.created_at,
                "name": lambda j: j.name,
                "state": lambda j: j.state.value,
            },
            default_sort_field="created_at",
            date_getter=lambda j: j.created_at.isoformat(),
        )
    except ListOptionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    if json_output:
        import json as _json
        print(_json.dumps({
            "version": 1,
            "job_count": len(jobs),
            "jobs": [{"id": str(job.id), "state": job.state.value, "name": job.name,
                     "created_at": job.created_at.isoformat(),
                     "project_id": job.project_id or ""} for job in jobs],
        }, sort_keys=True))
        return
    if not jobs:
        print("No jobs found.")
        return
    known = _known_project_ids()
    for job in jobs:
        label = _scope_label(job, scope, known)
        print(f"{job.id}  {job.state.value:<12}  {job.created_at.isoformat()}  {job.name}{label}")
    if skipped:
        print(f"  ({len(skipped)} unreadable job file(s) skipped)", file=sys.stderr)
<<<END PAIR_P1_TO>>>
Verify FROM occurs exactly once in the file before applying. Note: `jobs` is REASSIGNED before either branch, so both `--json` and text output are filtered/sorted/limited identically by construction — do not duplicate the `apply_list_options` call.

PAIR P2 (REWRITE) — `apps/cli/commands/job.py`, the `job.list` dispatch lambda.
FROM (exact):
<<<BEGIN PAIR_P2_FROM>>>
    "job.list": lambda args: _cmd_list_jobs(
        project=getattr(args, "project", None),
        all_projects=getattr(args, "all_projects", False),
        json_output=args.json,
    ),
<<<END PAIR_P2_FROM>>>
TO:
<<<BEGIN PAIR_P2_TO>>>
    "job.list": lambda args: _cmd_list_jobs(
        project=getattr(args, "project", None),
        all_projects=getattr(args, "all_projects", False),
        json_output=args.json,
        sort=getattr(args, "sort", None),
        desc=getattr(args, "desc", False),
        since=getattr(args, "since", None),
        until=getattr(args, "until", None),
        limit=getattr(args, "limit", None),
    ),
<<<END PAIR_P2_TO>>>
Verify FROM occurs exactly once in the file before applying.

NEW FILE — create `tests/orchestration/test_list_options.py` with EXACTLY this content:
<<<BEGIN NEWFILE_TEST_LIST_OPTIONS>>>
"""
Domain tests: orchestration/test_list_options.py
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from packages.orchestration.list_options import ListOptionError, apply_list_options, parse_time_bound


def test_parse_time_bound_relative_form():
    now = datetime.now(timezone.utc)
    bound = parse_time_bound("2d")
    assert abs((now - timedelta(days=2) - bound).total_seconds()) < 5


def test_parse_time_bound_iso():
    bound = parse_time_bound("2026-01-01T00:00:00+00:00")
    assert bound == datetime(2026, 1, 1, tzinfo=timezone.utc)


def test_parse_time_bound_invalid_raises():
    with pytest.raises(ListOptionError):
        parse_time_bound("not-a-time")


def test_default_sort_is_newest_first():
    rows = [{"id": "a", "created_at": "2026-01-01T00:00:00+00:00"},
            {"id": "b", "created_at": "2026-01-03T00:00:00+00:00"},
            {"id": "c", "created_at": "2026-01-02T00:00:00+00:00"}]
    out = apply_list_options(
        rows, sort=None, desc=False, since=None, until=None, limit=None,
        sort_fields={"created_at": lambda r: r["created_at"]},
        default_sort_field="created_at",
        date_getter=lambda r: r["created_at"],
    )
    assert [r["id"] for r in out] == ["b", "c", "a"]


def test_desc_flag_reverses_the_default():
    rows = [{"id": "a", "created_at": "2026-01-01T00:00:00+00:00"},
            {"id": "b", "created_at": "2026-01-03T00:00:00+00:00"}]
    out = apply_list_options(
        rows, sort=None, desc=True, since=None, until=None, limit=None,
        sort_fields={"created_at": lambda r: r["created_at"]},
        default_sort_field="created_at",
        date_getter=lambda r: r["created_at"],
    )
    assert [r["id"] for r in out] == ["a", "b"]


def test_unknown_sort_field_raises_naming_valid_set():
    rows = [{"id": "a", "created_at": "2026-01-01T00:00:00+00:00"}]
    with pytest.raises(ListOptionError, match="created_at"):
        apply_list_options(
            rows, sort="bogus", desc=False, since=None, until=None, limit=None,
            sort_fields={"created_at": lambda r: r["created_at"]},
            default_sort_field="created_at",
            date_getter=lambda r: r["created_at"],
        )


def test_since_until_filter_by_date():
    rows = [{"id": "a", "created_at": "2026-01-01T00:00:00+00:00"},
            {"id": "b", "created_at": "2026-01-05T00:00:00+00:00"},
            {"id": "c", "created_at": "2026-01-10T00:00:00+00:00"}]
    out = apply_list_options(
        rows, sort=None, desc=False, since="2026-01-02T00:00:00+00:00",
        until="2026-01-09T00:00:00+00:00", limit=None,
        sort_fields={"created_at": lambda r: r["created_at"]},
        default_sort_field="created_at",
        date_getter=lambda r: r["created_at"],
    )
    assert [r["id"] for r in out] == ["b"]


def test_limit_caps_rows():
    rows = [{"id": str(i), "created_at": f"2026-01-{i:02d}T00:00:00+00:00"} for i in range(1, 6)]
    out = apply_list_options(
        rows, sort=None, desc=False, since=None, until=None, limit="2",
        sort_fields={"created_at": lambda r: r["created_at"]},
        default_sort_field="created_at",
        date_getter=lambda r: r["created_at"],
    )
    assert len(out) == 2


def test_invalid_limit_raises():
    rows = [{"id": "a", "created_at": "2026-01-01T00:00:00+00:00"}]
    with pytest.raises(ListOptionError):
        apply_list_options(
            rows, sort=None, desc=False, since=None, until=None, limit="not-a-number",
            sort_fields={"created_at": lambda r: r["created_at"]},
            default_sort_field="created_at",
            date_getter=lambda r: r["created_at"],
        )
<<<END NEWFILE_TEST_LIST_OPTIONS>>>

TEST T1 (APPEND) — `tests/test_grouped_cli.py`. Insert at the TRUE END of the file, immediately after the file's last line.
FROM (exact, the file's own last line):
<<<BEGIN T1_FROM>>>
        assert data["jobs"][0]["created_at"]
<<<END T1_FROM>>>
TO:
<<<BEGIN T1_TO>>>
        assert data["jobs"][0]["created_at"]

    def test_default_order_is_newest_first(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from datetime import datetime, timedelta, timezone
        older = Job(id=uuid4(), name="older", user_prompt="x",
                    created_at=datetime.now(timezone.utc) - timedelta(days=1))
        newer = Job(id=uuid4(), name="newer", user_prompt="x",
                    created_at=datetime.now(timezone.utc))
        save_job(older)
        save_job(newer)
        from apps.cli.commands.job import _cmd_list_jobs
        buf = StringIO()
        monkeypatch.setattr("sys.stdout", buf)
        _cmd_list_jobs(json_output=True, all_projects=True)
        data = json.loads(buf.getvalue())
        assert [j["name"] for j in data["jobs"]] == ["newer", "older"]

    def test_limit_caps_returned_jobs(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        for _ in range(3):
            save_job(_make_job())
        from apps.cli.commands.job import _cmd_list_jobs
        buf = StringIO()
        monkeypatch.setattr("sys.stdout", buf)
        _cmd_list_jobs(json_output=True, all_projects=True, limit="2")
        data = json.loads(buf.getvalue())
        assert data["job_count"] == 2

    def test_unknown_sort_field_exits_nonzero(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        save_job(_make_job())
        from apps.cli.commands.job import _cmd_list_jobs
        with pytest.raises(SystemExit) as exc:
            _cmd_list_jobs(json_output=True, all_projects=True, sort="bogus")
        assert exc.value.code == 1
<<<END T1_TO>>>
Verify FROM occurs exactly once in the file before applying (it is the file's own last line — confirm with a direct read that nothing follows it). `Job`, `Task`, `uuid4`, `save_job`, `json`, `StringIO`, `pytest`, and the module-level `_make_job()` helper are ALL already imported/defined at the top of this file — do not re-import or redefine any of them. This class (`TestJobListCLI`) uses 4-space method indentation — match the surrounding methods exactly.

Apply the two new files and both pairs. All four files (1 new production: `packages/orchestration/list_options.py`; 1 production rewrite: `apps/cli/commands/job.py`; 2 test: `tests/test_grouped_cli.py`, 1 new: `tests/orchestration/test_list_options.py`) in ONE commit.

Run `python3 -m py_compile packages/orchestration/list_options.py apps/cli/commands/job.py tests/test_grouped_cli.py tests/orchestration/test_list_options.py` and confirm exit 0. Then run `python3 -m pytest tests/test_grouped_cli.py tests/orchestration/test_list_options.py -q` and record the exact pass count verbatim — expected 530 (518 pre-existing in test_grouped_cli.py + 3 new there + 9 new in the new file). Commit message: `F262 R13 C2: T003 batch 1 - shared list-options helper + job.list wiring`

──────────────────────────────────────────────────────────
C3 — replace .agent/plan.md with PLAN14
──────────────────────────────────────────────────────────
Replace the ENTIRE content of `.agent/plan.md` with exactly the text between the PLAN14 markers below (whole-file replace, byte-exact — verify with an actual byte-for-byte binary comparison, not `wc -l`/diffstat):

<<<BEGIN PLAN14>>>
# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 13, session 5 - T003 batch 1: `packages/orchestration/list_options.py`
is a new shared helper (`apply_list_options`, `parse_time_bound`,
`ListOptionError`) that filters by --since/--until, orders by
--sort/--desc (newest-first is the DEFAULT with no flags), and caps by
--limit, over any row list (dicts or objects, via key-function maps) -
one implementation instead of 18 hand-rolled ones. Wired into `job.list`
first as the design's proof: `_cmd_list_jobs` reassigns its own `jobs`
list once before either --json or text rendering, so both branches see
the same filtered/sorted/limited rows by construction. An unknown
--sort field exits non-zero naming the valid set, never silently
ignored.

## Next Steps

- T003 batch 2+: wire `apply_list_options` into the remaining 17 list
  commands, one or a few at a time, same pacing T002 used (R2-R12).
  Order by risk/simplicity: patch.list/loop.list/queue.list/
  memory.list next (already-dated, well-tested, isolated handlers);
  loop.list needs care since its JSON rows (per-loop last-run lookup)
  and text rows (iterating LoopSpec objects) are built from two
  different collections today - reconcile that shape before wiring.
- change.list's event-log CREATED date stays open, UNRELATED to D1:
  do_run.py's event stays dead, job.py's real event carries no
  intent_id to join on - see DECISION F262 D1's Alternative section.
  execution.list/worker.list/config.list stay excused per Risks.
- Once every command is wired, add an integration-level smoke test
  proving the ten-second demo in Acceptance: a named run findable by
  one command with --since/--sort.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, it is not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix unless it
  blocks T003's sort behavior for them specifically.
<<<END PLAN14>>>

Commit message: `F262 R13 C3: replace plan.md with PLAN14`

──────────────────────────────────────────────────────────
C4 — handback
──────────────────────────────────────────────────────────
Rewrite `.agent/handoff.md` (whole-file, per AGENTS.md's handback contract) with: Session (SESSION 5 of feature F262, round 13, rounds so far 13), a Range section stating this handback covers `02f92f4c..<C3 sha>` (C4/this handback commit is NOT part of the reviewed content range), an Item Status table (Preconditions, C0a, C0b, C1, C2, C3, C4, plus one row per gate you ran), a Commits table with every file changed per commit and its +/- line counts from `git show --numstat`, a Verification section with the REAL output of every command you ran (py_compile exit codes, the exact pytest pass count for C2's combined run, the canary suite run as ONE combined invocation: `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q`, expected 646 passed), a Deviations & assumptions section (state honestly anything that didn't go exactly as ordered, including the plan.md byte-equality check result and the real pre-existing test count you measured for tests/test_grouped_cli.py before this round, to cross-check the block's own 518 claim), and a Next section naming round 14's likely focus (continuing T003 batch 2 against PLAN14's ordered list — your call which command(s), state your one-sentence reasoning). Follow the exact structure of the R12 handback (commit 02f92f4c, already on disk — read it for the template).

After committing C4, run `git push -u origin feature/f262-list-commands-v2` and report the push result in your closing message.

Do NOT run any `gh pr` command. Do NOT merge anything. Do NOT touch `main`. This round ships no PR — the branch stays open for round 14.

═══════════════════════════════════════════════════════════════
CONSTRAINTS
═══════════════════════════════════════════════════════════════
1. Every FROM string in P1, P2 and T1 must be verified to occur exactly once in its target file, using the file's CURRENT content on disk (re-read each file yourself before applying, do not trust cited context blindly). If a FROM does not match, STOP that pair, do not guess a fix, report the exact mismatch in Deviations instead.
2. Do not touch any file not named in this block. Do NOT wire any list command other than `job.list` this round — the other 17 are later batches.
3. Do not run `ruff` if it requires approval you don't have — note the refusal in Deviations if so, not a blocker.
4. If `.agent/STOP` appears at any point mid-round, finish the commit you are mid-way through (if any), then stop and hand off.
5. Keep C2 as ONE commit covering exactly the four named files.
6. Report every command's REAL exit code and REAL output. Never write "green"/"passed" without the actual number. If the pytest count differs from this block's own prediction, report the REAL number and the real pre-existing count you measured — do not adjust either number to make them agree (the same honesty lesson round 12 booked in GATE12 above).
7. The C3 plan.md gate MUST be an actual byte-for-byte comparison (read both files in binary mode and compare with `==`), not a line-count or diffstat proxy.
8. `packages/orchestration/list_options.py` has NO dependency on `packages.core.models` or any store — it operates only on the row list and key-functions it is given, so it stays reusable for a dict-shaped row (patch.list, review.list, ...) or an object-shaped row (job.list's `Job` instances) alike. Do not add a Job-specific import to it.

END OF BLOCK
