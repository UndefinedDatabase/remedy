═══════════════════════════════════════════════════════════════
STEP — F262 R14/? — T003 batch 2: queue.list + memory.list, plus DECISION F262 D2
═══════════════════════════════════════════════════════════════

GOAL: Continue T003 with its second batch: wire `packages/orchestration/list_options.py` (built in R13) into `queue.list` and `memory.list`. Also book round 13's reviewer verdict into the ledger, and register a DECISION resolving a genuine design conflict the reviewer found while investigating `queue.list`: its existing no-flag default order is PRIORITY, not date, and is load-bearing (a named, passing test asserts it) — T003's newest-first-by-default principle must NOT silently override it. `list_options.py`'s `apply_list_options` is widened so a caller can opt OUT of forcing a default order (queue.list does; job.list and memory.list still force one, since both already forced newest-first before this feature and continue to).

BACKGROUND FACTS (already verified by the reviewer — do not re-derive):
- `tests/cli/test_queue_cmd.py::TestList::test_priority_is_recorded_and_orders_the_listing` (unmodified by this round) asserts that a `--prio 9` entry added SECOND still lists FIRST — `queue.list`'s current no-flag order is priority-descending, sourced from `packages.orchestration.job_queue.list_entries_safe`, which the CLI layer (`_cmd_queue_list` in `apps/cli/commands/queue_cmd.py`) does no re-sorting of today. This is DECISION F262 D2's subject.
- `packages/memory/local_gateway.py`'s `list_memory()` ALREADY does `entries.sort(key=lambda e: e.created_at, reverse=True)` internally — its no-flag default is ALREADY newest-first, so wiring `apply_list_options` with `default_sort_field="created_at"` changes nothing about the no-flag case; it only ADDS `--sort`/`--since`/`--until`/`--limit` capability on top of the existing behaviour.
- `packages/memory/models.py`'s `MemoryEntry.updated_at` is `str | None` (can genuinely be `None`); `created_at` is always a populated `str`. Only `created_at` and `key` are exposed as valid `--sort` fields for `memory.list` this round — `updated_at` is left out to avoid a `None`-vs-`str` comparison crash during sort, which is out of this round's scope to solve.
- Both `_cmd_queue_list` and `_cmd_memory_list` already have `sys` imported at module scope in their respective files — no new import of `sys` is needed for either.

═══ COMMIT SEQUENCE (5 commits total) ═══

──────────────────────────────────────────────────────────
C0a — save this entire step block verbatim
──────────────────────────────────────────────────────────
Save the FULL literal text of this prompt message (everything between the "STEP —" header above and the final "END OF BLOCK" marker at the bottom) to `.agent/authored/f262-r14.md`, byte for byte, exactly as received. Commit message: `F262 R14 C0a: save block verbatim to .agent/authored/f262-r14.md`

──────────────────────────────────────────────────────────
C0b — mirror to .agent/last_block.md
──────────────────────────────────────────────────────────
Copy `.agent/authored/f262-r14.md` to `.agent/last_block.md`, whole-file replace. Verify `sha256sum` of both files matches after writing. Commit message: `F262 R14 C0b: mirror block to .agent/last_block.md`

──────────────────────────────────────────────────────────
C1 — append GATE13 to .agent/live_review.md AND DECISION F262 D2 to .agent/decisions.md
──────────────────────────────────────────────────────────
Append exactly the text between the GATE13 markers below to the END of `.agent/live_review.md`: one newline, then the GATE13 text verbatim (it is a SINGLE LINE — no internal newlines), nothing else added.

<<<BEGIN GATE13>>>
Gate: R13 — the F262 R13 entry. R13 started T003 (sort/filter/limit behaviour): a new shared helper, `packages/orchestration/list_options.py` (`apply_list_options`/`parse_time_bound`/`ListOptionError`), filters by `--since`/`--until`, orders by `--sort`/`--desc` (newest-first the DEFAULT with no flags), and caps by `--limit`, wired into `job.list` first as the design's proof (`_cmd_list_jobs` reassigns its own `jobs` list once before either `--json` or text rendering) — AND THE REVIEWER RE-RAN EVERY GATE ITSELF. TRANSPORT HELD: `.agent/authored/f262-r13.md`/`.agent/last_block.md` share one sha256 digest, `f791b61c5a52e5444eb6bf1173e19645df07cd6d077bc416fec0a9b5aa864a73`, confirmed by the reviewer's own sha256sum of both committed files. THE DIFF WAS READ, NOT ONLY GATED: `git diff 02f92f4c..9e27a561` shows exactly the new file `packages/orchestration/list_options.py` byte-for-byte as authored, PAIR P1 and PAIR P2 in `apps/cli/commands/job.py`, and the new/appended test files (`tests/orchestration/test_list_options.py` new, `tests/test_grouped_cli.py`'s three appended tests), every diff re-read in full, nothing else touched. `python3 -m py_compile` exited 0 on all four touched/new files, run together by the reviewer. THE GATE12 LEDGER APPEND (commit 87cd8050) AND ITS PROSE_SLIP (same commit) WERE BOTH RE-VERIFIED BYTE-EXACT: live_review.md base 2452539 plus one newline plus GATE12 (2486 bytes, 0 internal newlines) equals 2455026; prose_slips.md base 72998 plus one newline plus the 584-byte slip equals 73583 — both exact. THE TESTS MOVED EXACTLY AS THE HANDBACK CLAIMED, reproduced independently: `tests/test_grouped_cli.py tests/orchestration/test_list_options.py` read 530 passed (518 pre-existing plus 3 plus 9 new). THE STATE READERS AND THE CANARY WERE UNMOVED, reproduced by the reviewer as ONE combined invocation: `tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py` read 646 passed, matching 515+52+21+16+42 exactly. HYGIENE HELD: `git status --porcelain` empty at HEAD `3459e7a8`, `git ls-files .remedy-wt` empty, `.agent/STOP` absent. THE PLAN HELD: `.agent/plan.md` measured 2388 bytes, matching the handback's own reported byte-for-byte comparison of the authored PLAN14 slice against the written file. THE VERDICT IS PASS.
<<<END GATE13>>>

Then append exactly the text between the DECISION markers below to the END of `.agent/decisions.md`: one newline (NO blank line — this file's existing entries butt directly against each other with a single newline, confirmed by the reviewer reading the file's own tail), then the DECISION text verbatim, nothing else added.

<<<BEGIN DECISION_F262_D2>>>
## DECISION F262 D2 (2026-09-05, F262 R14) — queue.list's no-flag default order stays its existing PRIORITY order; T003's newest-first default does not override it

CONTEXT. T2_F262.md's Design section states "Newest-first is the DEFAULT, not a flag. A list whose store cannot order says so rather than presenting arbitrary order as recency." Round 14 investigated wiring the R13 shared helper (`packages/orchestration/list_options.py`) into `queue.list` next, following PLAN14's Next Steps ordering. `tests/cli/test_queue_cmd.py::TestList::test_priority_is_recorded_and_orders_the_listing` asserts the CLI's existing, load-bearing behaviour: a `--prio 9` entry added SECOND still lists FIRST, ahead of an unprioritized entry added first — `queue.list`'s current no-flag order is priority-descending, not insertion order and not date order.

MEASURED. `apps/cli/commands/queue_cmd.py`'s `_cmd_queue_list` builds its `rows` list from `list_entries_safe()` per project and performs no sorting itself in the CLI layer — the store already returns entries in priority order (confirmed by the passing, unmodified test above). This is a deliberate, meaningful, already-tested order — not the "arbitrary" order the Design section's sentence warns against presenting as if it were recency. Applying `apply_list_options`'s forced default (`sort or default_sort_field`, defaulting to `created_at` descending) unconditionally would silently override this order whenever `--sort` is not given, moving a newer low-priority entry ahead of an older high-priority one — the exact regression `test_priority_is_recorded_and_orders_the_listing` exists to catch, and a change to what "the queue" means operationally (highest-priority-next), not merely an additional capability.

CHOSEN. `queue.list` gains `--sort`/`--since`/`--until`/`--limit` support via `apply_list_options`, but with no flags at all it keeps its current, unmodified priority order exactly as `list_entries_safe` returns it. This is implemented by widening `apply_list_options`'s contract: `default_sort_field: str | None = None` — when `None` and `sort` is also `None`, the ordering step is skipped entirely (filtering and limiting still apply), so a caller with no natural default order forces one (as `job.list`/`memory.list` do, passing a real field name) while a caller with an EXISTING meaningful order opts OUT of forcing by passing `None` and keeps its own. `--sort priority`/`--sort created_at`/`--sort status` remain available as explicit, named, opt-in overrides — `--sort` still validates against a real field set and fails loudly on an unknown name, meeting Acceptance's "fails with the valid set named" clause unchanged.

ALTERNATIVE CONSIDERED AND REJECTED. Force `created_at` as `queue.list`'s default anyway, on the reading that T2_F262.md's Acceptance is unconditional ("newest-first... everywhere, without a flag"). Rejected: Acceptance's own DONE bar is "a specific run from the day before yesterday is findable by command in under ten seconds" and "every list uses the same words for the same flags" — both are satisfied by `--sort created_at` remaining available and spelled identically to every other list command; nothing in Acceptance requires discarding an existing, tested, operationally-meaningful order that a real user already relies on (queue processing order) to satisfy a demo scenario about finding a past run, which `queue.list` was never the primary command for in the first place (`job.list`/`patch.list`/etc. are). Silently changing queue semantics to satisfy a literal reading of one sentence, at the cost of breaking a passing, named, intentional test, is the "silent scope change" AGENTS.md's Commit Gate forbids, not an Acceptance-mandated change.

CONSEQUENCE. `packages/orchestration/list_options.py`'s `apply_list_options` gains `default_sort_field: str | None = None` (widened from a required `str`) and an early-exit from the sort step when both `sort` and `default_sort_field` are `None`; every existing caller (`job.list` from R13, `memory.list` this same round) is unaffected since both pass a real field name. `apps/cli/commands/queue_cmd.py`'s `_cmd_queue_list` wires `--sort`/`--since`/`--until`/`--limit` through `apply_list_options` with `default_sort_field=None`, preserving `test_priority_is_recorded_and_orders_the_listing` unchanged. `docs/roadmap/features/T2_F262.md` is not amended — this DECISION documents a scope boundary already implicit in "a store whose order is already meaningful is not the class of gap T003 targets," made explicit rather than silently assumed.

REVERSE by deleting this DECISION, reverting `default_sort_field` to a required `str` in `list_options.py`, and reverting `queue.list`'s wiring — which a fresh re-read of `test_priority_is_recorded_and_orders_the_listing` against a forced date-default would immediately re-discover broken.
<<<END DECISION_F262_D2>>>

Commit message: `F262 R14 C1: append GATE13 to live_review.md and DECISION F262 D2 to decisions.md - books round 13's PASS verdict`

──────────────────────────────────────────────────────────
C2 — production code + tests (one commit, three production rewrites, three test appends)
──────────────────────────────────────────────────────────

PAIR P1 (REWRITE) — `packages/orchestration/list_options.py`, `apply_list_options` widened so `default_sort_field` may be `None` (skip ordering entirely when neither `sort` nor `default_sort_field` is given). This is the WHOLE current function — re-read the file yourself first and confirm this FROM matches exactly before applying; if it does not match, STOP and report the mismatch rather than guessing.
FROM (exact):
<<<BEGIN PAIR_P1_FROM>>>
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
<<<END PAIR_P1_FROM>>>
TO:
<<<BEGIN PAIR_P1_TO>>>
def apply_list_options(
    rows: list[T],
    *,
    sort: str | None,
    desc: bool,
    since: str | None,
    until: str | None,
    limit: str | None,
    sort_fields: dict[str, Callable[[T], Any]],
    default_sort_field: str | None = None,
    date_getter: Callable[[T], str | None] | None = None,
) -> list[T]:
    """Filter by --since/--until, order by --sort/--desc (newest-first is
    the DEFAULT with no flags at all), then cap by --limit — in that
    order. `sort_fields` maps a valid --sort NAME to a key function over a
    row; an unknown name raises ListOptionError naming the valid set.
    `date_getter` extracts a row's own date string for --since/--until; a
    store with no timestamp concept passes None and --since/--until are
    accepted but filter nothing. `default_sort_field=None` means the
    caller's row order already has real meaning (e.g. queue priority):
    ordering is skipped entirely unless --sort is given explicitly."""
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

    if sort is not None or default_sort_field is not None:
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
<<<END PAIR_P1_TO>>>
Verify FROM occurs exactly once in the file before applying.

PAIR P2 (REWRITE) — `apps/cli/commands/queue_cmd.py`, `_cmd_queue_list` wired to `apply_list_options` with `default_sort_field=None` (per DECISION F262 D2). This is the WHOLE current function — re-read the file yourself first and confirm this FROM matches exactly before applying.
FROM (exact):
<<<BEGIN PAIR_P2_FROM>>>
def _cmd_queue_list(*, project: str | None = None, all_projects: bool = False,
                    json_output: bool = False) -> None:
    from packages.orchestration.job_queue import list_entries_safe

    if all_projects:
        project_ids = _project_ids_with_a_queue()
    else:
        project_ids = [_resolve_project_id(project)]

    rows: list[tuple[str, Any]] = []
    skipped_total = 0
    for project_id in project_ids:
        entries, _degraded, skipped = list_entries_safe(project_id)
        skipped_total += len(skipped)
        rows.extend((project_id, entry) for entry in entries)

    if json_output:
        import json as _json
        print(_json.dumps({
            "version": 1,
            "entry_count": len(rows),
            "entries": [{"id": entry.id, "status": entry.status, "priority": entry.priority,
                        "created_at": entry.created_at, "claimed_by": entry.claimed_by or "",
                        "goal": _goal_label(entry), "project_id": project_id}
                       for project_id, entry in rows],
        }, sort_keys=True))
        return

    if not rows:
        print("No queue entries found.")
    for project_id, entry in rows:
        owner = entry.claimed_by or "-"
        label = f"  (project: {project_id[:8]})" if all_projects else ""
        print(f"{entry.id[:12]}  {entry.status:<8}  prio {entry.priority:<4}  "
              f"{_age(entry.created_at):>4}  {owner:<24}  {_goal_label(entry)}{label}")
    if skipped_total:
        print(f"  ({skipped_total} unreadable queue file(s) skipped)", file=sys.stderr)
<<<END PAIR_P2_FROM>>>
TO:
<<<BEGIN PAIR_P2_TO>>>
def _cmd_queue_list(*, project: str | None = None, all_projects: bool = False,
                    json_output: bool = False, sort: str | None = None, desc: bool = False,
                    since: str | None = None, until: str | None = None,
                    limit: str | None = None) -> None:
    from packages.orchestration.job_queue import list_entries_safe
    from packages.orchestration.list_options import ListOptionError, apply_list_options

    if all_projects:
        project_ids = _project_ids_with_a_queue()
    else:
        project_ids = [_resolve_project_id(project)]

    rows: list[tuple[str, Any]] = []
    skipped_total = 0
    for project_id in project_ids:
        entries, _degraded, skipped = list_entries_safe(project_id)
        skipped_total += len(skipped)
        rows.extend((project_id, entry) for entry in entries)

    try:
        rows = apply_list_options(
            rows,
            sort=sort, desc=desc, since=since, until=until, limit=limit,
            sort_fields={
                "created_at": lambda pair: pair[1].created_at,
                "priority": lambda pair: pair[1].priority,
                "status": lambda pair: pair[1].status,
            },
            default_sort_field=None,
            date_getter=lambda pair: pair[1].created_at,
        )
    except ListOptionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if json_output:
        import json as _json
        print(_json.dumps({
            "version": 1,
            "entry_count": len(rows),
            "entries": [{"id": entry.id, "status": entry.status, "priority": entry.priority,
                        "created_at": entry.created_at, "claimed_by": entry.claimed_by or "",
                        "goal": _goal_label(entry), "project_id": project_id}
                       for project_id, entry in rows],
        }, sort_keys=True))
        return

    if not rows:
        print("No queue entries found.")
    for project_id, entry in rows:
        owner = entry.claimed_by or "-"
        label = f"  (project: {project_id[:8]})" if all_projects else ""
        print(f"{entry.id[:12]}  {entry.status:<8}  prio {entry.priority:<4}  "
              f"{_age(entry.created_at):>4}  {owner:<24}  {_goal_label(entry)}{label}")
    if skipped_total:
        print(f"  ({skipped_total} unreadable queue file(s) skipped)", file=sys.stderr)
<<<END PAIR_P2_TO>>>
Verify FROM occurs exactly once in the file before applying.

PAIR P3 (REWRITE) — `apps/cli/commands/queue_cmd.py`, the `queue.list` dispatch lambda.
FROM (exact):
<<<BEGIN PAIR_P3_FROM>>>
    "queue.list": lambda args: _cmd_queue_list(
        project=getattr(args, "project", None),
        all_projects=getattr(args, "all_projects", False),
        json_output=args.json,
    ),
<<<END PAIR_P3_FROM>>>
TO:
<<<BEGIN PAIR_P3_TO>>>
    "queue.list": lambda args: _cmd_queue_list(
        project=getattr(args, "project", None),
        all_projects=getattr(args, "all_projects", False),
        json_output=args.json,
        sort=getattr(args, "sort", None),
        desc=getattr(args, "desc", False),
        since=getattr(args, "since", None),
        until=getattr(args, "until", None),
        limit=getattr(args, "limit", None),
    ),
<<<END PAIR_P3_TO>>>
Verify FROM occurs exactly once in the file before applying.

PAIR P4 (REWRITE) — `apps/cli/commands/memory.py`, `_cmd_memory_list` wired to `apply_list_options` with `default_sort_field="created_at"` (its existing internal default already sorts this way — see BACKGROUND FACTS). This is the WHOLE current function — re-read the file yourself first and confirm this FROM matches exactly before applying.
FROM (exact):
<<<BEGIN PAIR_P4_FROM>>>
def _cmd_memory_list(
    *,
    project_id: str | None = None,
    job_id: str | None = None,
    json_output: bool = False,
) -> None:
    from packages.memory.local_gateway import list_memory

    entries = list_memory(project_id=project_id, job_id=job_id)

    if json_output:
        output = [
            {
                "id": str(e.id), "key": e.key, "value": e.value,
                "summary": e.summary, "tags": e.tags,
                "approved": e.approved, "source_type": e.source_type,
                "validity": e.validity, "review_status": e.review_status,
                "scope": e.scope, "evidence_refs": e.evidence_refs,
                "created_at": e.created_at,
                "updated_at": e.updated_at,
            }
            for e in entries
        ]
        print(_json.dumps({"version": 1, "entries": output, "count": len(output)}, sort_keys=True))
    else:
        if not entries:
            scope = f"project={project_id}" if project_id else (f"job={job_id}" if job_id else "global")
            print(f"No memory entries ({scope}).")
            return
        for e in entries:
            approved_mark = " [approved]" if e.approved else ""
            tags_str = f" tags={','.join(e.tags)}" if e.tags else ""
            print(f"  {e.key}: {e.value}{approved_mark}{tags_str}  (id={str(e.id)[:8]}, created={e.created_at}, updated={e.updated_at})")
<<<END PAIR_P4_FROM>>>
TO:
<<<BEGIN PAIR_P4_TO>>>
def _cmd_memory_list(
    *,
    project_id: str | None = None,
    job_id: str | None = None,
    json_output: bool = False,
    sort: str | None = None,
    desc: bool = False,
    since: str | None = None,
    until: str | None = None,
    limit: str | None = None,
) -> None:
    from packages.memory.local_gateway import list_memory
    from packages.orchestration.list_options import ListOptionError, apply_list_options

    entries = list_memory(project_id=project_id, job_id=job_id)

    try:
        entries = apply_list_options(
            entries,
            sort=sort, desc=desc, since=since, until=until, limit=limit,
            sort_fields={
                "created_at": lambda e: e.created_at,
                "key": lambda e: e.key,
            },
            default_sort_field="created_at",
            date_getter=lambda e: e.created_at,
        )
    except ListOptionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if json_output:
        output = [
            {
                "id": str(e.id), "key": e.key, "value": e.value,
                "summary": e.summary, "tags": e.tags,
                "approved": e.approved, "source_type": e.source_type,
                "validity": e.validity, "review_status": e.review_status,
                "scope": e.scope, "evidence_refs": e.evidence_refs,
                "created_at": e.created_at,
                "updated_at": e.updated_at,
            }
            for e in entries
        ]
        print(_json.dumps({"version": 1, "entries": output, "count": len(output)}, sort_keys=True))
    else:
        if not entries:
            scope = f"project={project_id}" if project_id else (f"job={job_id}" if job_id else "global")
            print(f"No memory entries ({scope}).")
            return
        for e in entries:
            approved_mark = " [approved]" if e.approved else ""
            tags_str = f" tags={','.join(e.tags)}" if e.tags else ""
            print(f"  {e.key}: {e.value}{approved_mark}{tags_str}  (id={str(e.id)[:8]}, created={e.created_at}, updated={e.updated_at})")
<<<END PAIR_P4_TO>>>
Verify FROM occurs exactly once in the file before applying.

PAIR P5 (REWRITE) — `apps/cli/commands/memory.py`, the `memory.list` dispatch lambda.
FROM (exact):
<<<BEGIN PAIR_P5_FROM>>>
    "memory.list": lambda args: _cmd_memory_list(
        project_id=getattr(args, "project", None),
        job_id=getattr(args, "job", None),
        json_output=getattr(args, "json", False),
    ),
<<<END PAIR_P5_FROM>>>
TO:
<<<BEGIN PAIR_P5_TO>>>
    "memory.list": lambda args: _cmd_memory_list(
        project_id=getattr(args, "project", None),
        job_id=getattr(args, "job", None),
        json_output=getattr(args, "json", False),
        sort=getattr(args, "sort", None),
        desc=getattr(args, "desc", False),
        since=getattr(args, "since", None),
        until=getattr(args, "until", None),
        limit=getattr(args, "limit", None),
    ),
<<<END PAIR_P5_TO>>>
Verify FROM occurs exactly once in the file before applying.

TEST T1 (APPEND) — `tests/orchestration/test_list_options.py`. Insert at the TRUE END of the file, immediately after `test_invalid_limit_raises` (the file's last function).
FROM (exact, the file's own last function, verify nothing follows it):
<<<BEGIN T1_FROM>>>
def test_invalid_limit_raises():
    rows = [{"id": "a", "created_at": "2026-01-01T00:00:00+00:00"}]
    with pytest.raises(ListOptionError):
        apply_list_options(
            rows, sort=None, desc=False, since=None, until=None, limit="not-a-number",
            sort_fields={"created_at": lambda r: r["created_at"]},
            default_sort_field="created_at",
            date_getter=lambda r: r["created_at"],
        )
<<<END T1_FROM>>>
TO:
<<<BEGIN T1_TO>>>
def test_invalid_limit_raises():
    rows = [{"id": "a", "created_at": "2026-01-01T00:00:00+00:00"}]
    with pytest.raises(ListOptionError):
        apply_list_options(
            rows, sort=None, desc=False, since=None, until=None, limit="not-a-number",
            sort_fields={"created_at": lambda r: r["created_at"]},
            default_sort_field="created_at",
            date_getter=lambda r: r["created_at"],
        )


def test_no_default_sort_field_keeps_original_order_when_sort_not_given():
    rows = [{"id": "c"}, {"id": "a"}, {"id": "b"}]
    out = apply_list_options(
        rows, sort=None, desc=False, since=None, until=None, limit=None,
        sort_fields={"id": lambda r: r["id"]},
        default_sort_field=None,
    )
    assert [r["id"] for r in out] == ["c", "a", "b"]


def test_no_default_sort_field_still_honours_explicit_sort():
    rows = [{"id": "c"}, {"id": "a"}, {"id": "b"}]
    out = apply_list_options(
        rows, sort="id", desc=False, since=None, until=None, limit=None,
        sort_fields={"id": lambda r: r["id"]},
        default_sort_field=None,
    )
    assert [r["id"] for r in out] == ["a", "b", "c"]
<<<END T1_TO>>>
Verify FROM occurs exactly once in the file before applying — it is the file's own last function.

TEST T2 (REWRITE) — `tests/cli/test_queue_cmd.py`, `TestList` class gains two new tests, inserted between `test_json_has_created_at_and_goal` and `class TestRm:`.
FROM (exact, including the two blank lines before the next class):
<<<BEGIN T2_FROM>>>
        assert data["entries"][0]["created_at"]
        assert data["entries"][0]["goal"] == "json goal"


class TestRm:
<<<END T2_FROM>>>
TO:
<<<BEGIN T2_TO>>>
        assert data["entries"][0]["created_at"]
        assert data["entries"][0]["goal"] == "json goal"

    def test_sort_created_at_overrides_the_priority_default(self, project):
        data_root, project_id = project
        _run(["queue", "add", "first goal", "--project", project_id], data_root)
        _run(["queue", "add", "second goal", "--prio", "9", "--project", project_id], data_root)

        lines = [ln for ln in _run(
            ["queue", "list", "--project", project_id, "--sort", "created_at"], data_root,
        ).stdout.splitlines() if ln.strip()]
        assert "first goal" in lines[0]
        assert "second goal" in lines[1]

    def test_unknown_sort_field_exits_nonzero_naming_valid_fields(self, project):
        data_root, project_id = project
        _run(["queue", "add", "a goal", "--project", project_id], data_root)

        proc = _run(["queue", "list", "--project", project_id, "--sort", "bogus"], data_root,
                    expect_ok=False)
        assert proc.returncode == 1
        assert "created_at" in proc.stderr


class TestRm:
<<<END T2_TO>>>
Verify FROM occurs exactly once in the file before applying (confirmed unique by the reviewer via the two anchor strings, but re-verify on current disk content per constraint 1).

TEST T3 (REWRITE) — `tests/test_grouped_cli.py`, `TestMemoryCLIContract` class gains two new tests, inserted between `test_approved_absent_is_false_in_argparse` and `class TestProjectListCLI:`.
FROM (exact, including the two blank lines before the next class):
<<<BEGIN T3_FROM>>>
    def test_approved_absent_is_false_in_argparse(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["memory", "store", "k", "v"])
        assert args.approved is False


class TestProjectListCLI:
<<<END T3_FROM>>>
TO:
<<<BEGIN T3_TO>>>
    def test_approved_absent_is_false_in_argparse(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["memory", "store", "k", "v"])
        assert args.approved is False

    def test_sort_by_key_orders_entries(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from apps.cli.commands.memory import _cmd_memory_list, _cmd_memory_store
        _cmd_memory_store("zeta", "v1")
        _cmd_memory_store("alpha", "v2")
        buf = StringIO()
        monkeypatch.setattr("sys.stdout", buf)
        _cmd_memory_list(json_output=True, sort="key")
        data = json.loads(buf.getvalue())
        assert [e["key"] for e in data["entries"]] == ["alpha", "zeta"]

    def test_unknown_sort_field_exits_nonzero(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from apps.cli.commands.memory import _cmd_memory_list, _cmd_memory_store
        _cmd_memory_store("key", "v")
        with pytest.raises(SystemExit) as exc:
            _cmd_memory_list(json_output=True, sort="bogus")
        assert exc.value.code == 1


class TestProjectListCLI:
<<<END T3_TO>>>
Verify FROM occurs exactly once in the file before applying. `StringIO`, `json`, `pytest` are already imported at module scope in this file — do not re-import them.

Apply PAIR P1-P5 and TEST T1-T3. Six files (3 production: `packages/orchestration/list_options.py`, `apps/cli/commands/queue_cmd.py`, `apps/cli/commands/memory.py`; 3 test: `tests/orchestration/test_list_options.py`, `tests/cli/test_queue_cmd.py`, `tests/test_grouped_cli.py`) in ONE commit.

Run `python3 -m py_compile packages/orchestration/list_options.py apps/cli/commands/queue_cmd.py apps/cli/commands/memory.py tests/orchestration/test_list_options.py tests/cli/test_queue_cmd.py tests/test_grouped_cli.py` and confirm exit 0. Then run `python3 -m pytest tests/orchestration/test_list_options.py tests/cli/test_queue_cmd.py tests/test_grouped_cli.py -q` and record the exact pass count verbatim — expected 562 (9+26+521=556 pre-existing, confirmed by the reviewer's own pre-round run of this exact combined command, plus 2+2+2=6 new). Commit message: `F262 R14 C2: T003 batch 2 - queue.list + memory.list wiring (DECISION F262 D2)`

──────────────────────────────────────────────────────────
C3 — replace .agent/plan.md with PLAN15
──────────────────────────────────────────────────────────
Replace the ENTIRE content of `.agent/plan.md` with exactly the text between the PLAN15 markers below (whole-file replace, byte-exact — verify with an actual byte-for-byte binary comparison, not `wc -l`/diffstat):

<<<BEGIN PLAN15>>>
# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 14, session 5 - T003 batch 2: `queue.list` and `memory.list` are
wired to `apply_list_options`. `queue.list` passes `default_sort_field=
None` (DECISION F262 D2) so its existing, tested PRIORITY default order
is preserved when no flags are given - `--sort created_at`/`priority`/
`status` are available as explicit overrides. `memory.list` passes
`default_sort_field="created_at"`, changing nothing about its no-flag
case (it already sorted newest-first internally) while adding `--sort
key`/`--since`/`--until`/`--limit`. `list_options.py`'s own contract
widened to make the priority-preserving case possible for any future
caller with a similar pre-existing order.

## Next Steps

- T003 batch 3+: wire the remaining commands - patch.list (approval_
  queue.py's format_intent_list table renderer needs its own look before
  wiring, since it isn't a plain per-row print like the commands done so
  far), loop.list (JSON rows and text rows are built from two DIFFERENT
  collections today - reconcile before wiring), then project.list,
  tournament.list, blocker.list, decision.list, review.list, propose.list,
  test.list, external-builder.submission-list, config.list. Re-check EACH
  one for a queue.list-shaped surprise (an existing meaningful non-date
  order) before assuming date-descending is safe, per DECISION F262 D2's
  precedent - grep its own tests for an order-asserting test FIRST.
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
- A command with its OWN meaningful non-date default order (queue.list's
  priority, DECISION F262 D2) opts out of the forced newest-first default
  via `default_sort_field=None` rather than losing that order - audit
  each remaining command for this shape before wiring it.
<<<END PLAN15>>>

Commit message: `F262 R14 C3: replace plan.md with PLAN15`

──────────────────────────────────────────────────────────
C4 — handback
──────────────────────────────────────────────────────────
Rewrite `.agent/handoff.md` (whole-file, per AGENTS.md's handback contract) with: Session (SESSION 5 of feature F262, round 14, rounds so far 14), a Range section stating this handback covers `3459e7a8..<C3 sha>` (C4/this handback commit is NOT part of the reviewed content range), an Item Status table (Preconditions, C0a, C0b, C1, C2, C3, C4, plus one row per gate you ran), a Commits table with every file changed per commit and its +/- line counts from `git show --numstat`, a Verification section with the REAL output of every command you ran (py_compile exit codes, the exact pytest pass count for C2's combined run, the canary suite run as ONE combined invocation: `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q`, expected 646 passed), a Deviations & assumptions section (state honestly anything that didn't go exactly as ordered, including the plan.md byte-equality check result, the DECISION F262 D2 append's byte math, and re-confirming `test_priority_is_recorded_and_orders_the_listing` still passes unmodified), and a Next section naming round 15's likely focus (T003 batch 3 against PLAN15's ordered list — your call which command(s), state your one-sentence reasoning; note patch.list and loop.list are flagged as needing extra investigation before wiring). Follow the exact structure of the R13 handback (commit 3459e7a8, already on disk — read it for the template).

After committing C4, run `git push -u origin feature/f262-list-commands-v2` and report the push result in your closing message.

Do NOT run any `gh pr` command. Do NOT merge anything. Do NOT touch `main`. This round ships no PR — the branch stays open for round 15.

═══════════════════════════════════════════════════════════════
CONSTRAINTS
═══════════════════════════════════════════════════════════════
1. Every FROM string in P1-P5 and T1-T3 must be verified to occur exactly once in its target file, using the file's CURRENT content on disk (re-read each file yourself before applying, do not trust cited context blindly). If a FROM does not match, STOP that pair, do not guess a fix, report the exact mismatch in Deviations instead.
2. Do not touch any file not named in this block. Do NOT wire any list command other than `queue.list`/`memory.list` this round.
3. Do not run `ruff` if it requires approval you don't have — note the refusal in Deviations if so, not a blocker.
4. If `.agent/STOP` appears at any point mid-round, finish the commit you are mid-way through (if any), then stop and hand off.
5. Keep C2 as ONE commit covering exactly the six named files.
6. Report every command's REAL exit code and REAL output. Never write "green"/"passed" without the actual number.
7. The C3 plan.md gate MUST be an actual byte-for-byte comparison (read both files in binary mode and compare with `==`), not a line-count or diffstat proxy.
8. The C1 append to `.agent/decisions.md` gets the SAME full byte-forensics treatment as the `.agent/live_review.md` append (base size + newline + slice length = post-commit size, tail-equality, negative-control byte-flip rejection) — `.agent/decisions.md` is named explicitly in the gate-budget rule's two-target list alongside `.agent/live_review.md`, and this is not a `.agent/` prose file that only gets a byte-equality check.
9. After applying PAIR P2/P3 and BEFORE running the combined pytest command, run `python3 -m pytest tests/cli/test_queue_cmd.py::TestList::test_priority_is_recorded_and_orders_the_listing -q` on its own and confirm it still passes unmodified — this is the regression DECISION F262 D2 exists to prevent, and it must be shown green, not merely assumed.

END OF BLOCK