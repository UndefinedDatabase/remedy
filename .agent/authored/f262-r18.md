── STEP T003 batch6 — F262 List commands v2 ────────────────────────
Goal: Wire review.list, propose.list and external-builder.submission-list into the shared apply_list_options helper (T003, closing out the plain single-collection list batch), and book round 17's already-PASSED verdict into the ledger.

Bundle:
C0a. Save this entire step block, byte for byte, to a NEW file `.agent/authored/f262-r18.md`.
C0b. Whole-file replace `.agent/last_block.md` with the same bytes (mirror of C0a).
C1. Append GATE17 (below) to `.agent/live_review.md`.
C2. Production change: PAIR R1 in `apps/cli/commands/review_cmd.py`, PAIR PR1 in `apps/cli/commands/propose_cmd.py`, PAIR E1 in `apps/cli/commands/external_builder_cmd.py`, plus TEST T1 appended to `tests/cli/test_review_cmd.py`, TEST T2 appended to `tests/cli/test_propose_cli.py`, TEST T3 appended to `tests/cli/test_external_builder_cli.py`. ONE commit covering all six files.
C3. Whole-file replace `.agent/plan.md` with PLAN19 (below).
C4. Rewrite `.agent/handoff.md` (handback) per docs/agents/handback_template.md; this is the round's LAST commit.

============================================================
GATE17 — append verbatim as a new line at the end of `.agent/live_review.md`. The current file ends with NO trailing newline. C1 must: read the current file, append exactly one `\n` character followed by the GATE17 text below (with no trailing newline after it either). Do this with Python (`pathlib.Path.write_bytes`), not a shell append.

GATE17 text (copy exactly, it is a single line with zero internal newlines, 2420 bytes UTF-8):
Gate: R17 — the F262 R17 entry. R17 SHIPPED T003 BATCH 5, `blocker.list` and `decision.list` wired to `apply_list_options`, both `default_sort_field="created_at"` — both job-scoped, both return typed rows (StopReason/HumanDecision) whose `created_at` is already a plain string, both dispatch via lambda so each needed two pairs (handler + dispatch), and neither store's order was meaningful or test-guarded so neither needed a D2-style opt-out — AND THE REVIEWER RE-RAN EVERY GATE ITSELF. TRANSPORT HELD: `.agent/authored/f262-r17.md`/`.agent/last_block.md` share one sha256 digest, `1cc828a4f4b3e0a792406ae032bc30ca4c2847e0ef808ebd25dddec5031eb90b`, confirmed by the reviewer's own sha256sum of both committed files. THE DIFF WAS READ, NOT ONLY GATED: `git diff 94eb67c91cb9c1f28c7f1285d4d6411a475c23e4..25ef619839597ff4ec9fdd9d6c626e4597ec9ea5` for `apps/cli/commands/blocker.py`, `apps/cli/commands/decision.py`, `tests/cli/test_blocker_cmd.py` and `tests/cli/test_decision_cmd.py` shows exactly PAIR B1/B2, PAIR D1/D2, and the two new test classes (`TestBlockerListOptions`, `TestDecisionListOptions`) plus their `import pytest` additions, every other line in all four files untouched, confirmed by reading the full diff. `python3 -c "import py_compile; ..."` printed OK for all four touched files, run independently by the reviewer. THE GATE16 LEDGER APPEND (commit c43293f3) WAS RE-VERIFIED BYTE-EXACT: base 2462543 plus one newline plus GATE16 (2567 bytes, 0 internal newlines) equals 2465111, matching the file's own on-disk size measured immediately after the round. THE TESTS MOVED EXACTLY AS THE HANDBACK CLAIMED, reproduced independently: `python3 -m pytest tests/cli/test_blocker_cmd.py tests/cli/test_decision_cmd.py -q` read 8 passed (4 pre-existing plus 4 new). THE STATE READERS AND THE CANARY WERE UNMOVED, reproduced by the reviewer as ONE combined invocation: `tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py` read 646 passed, matching 515+52+21+16+42 exactly. HYGIENE HELD: `git status --porcelain` empty at HEAD `25ef6198`, `git ls-files .remedy-wt` empty, `.agent/STOP` absent. THE PLAN HELD: `.agent/plan.md` measured 2159 bytes, matching the handback's own reported byte-for-byte comparison of the authored PLAN18 slice against the written file. THE VERDICT IS PASS.

Base file size immediately before C1 must read 2465111 (confirm with a fresh Python byte read before writing). Post-C1 size must read exactly 2467532 (2465111 + 1 + 2420). Verify both numbers yourself and report them.
============================================================

PAIR R1 — apps/cli/commands/review_cmd.py — REWRITE. Before applying, re-read the CURRENT file and confirm this FROM text occurs exactly 1 time:

FROM:
    from packages.orchestration.reviewer import list_recommendations
    from packages.orchestration.storage import load_job

    job = load_job(UUID(args.job_id))
    recs = list_recommendations(job)

    if getattr(args, "json", False):
        print(json.dumps({
            "version": 1,
            "job_id": str(job.id),
            "recommendations": recs,

Replace it with this TO text:
    from packages.orchestration.list_options import ListOptionError, apply_list_options
    from packages.orchestration.reviewer import list_recommendations
    from packages.orchestration.storage import load_job

    job = load_job(UUID(args.job_id))
    recs = list_recommendations(job)
    try:
        recs = apply_list_options(
            recs,
            sort=getattr(args, "sort", None), desc=getattr(args, "desc", False),
            since=getattr(args, "since", None), until=getattr(args, "until", None),
            limit=getattr(args, "limit", None),
            sort_fields={
                "created_at": lambda r: r.get("created_at", ""),
                "status": lambda r: r.get("status", ""),
            },
            default_sort_field="created_at",
            date_getter=lambda r: r.get("created_at") or None,
        )
    except ListOptionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if getattr(args, "json", False):
        print(json.dumps({
            "version": 1,
            "job_id": str(job.id),
            "recommendations": recs,

Note: `sys` and `json` are already imported at module scope in review_cmd.py (lines 9-10) — do not add duplicate imports. `_cmd_review_list`'s dispatch site already forwards `args` unchanged (`"review.list": lambda args: _cmd_review_list(args),`) — do NOT touch the dispatch site, it needs no change since the function reads sort/desc/since/until/limit via getattr on the same args object it always received.

PAIR PR1 — apps/cli/commands/propose_cmd.py — REWRITE. Before applying, re-read the CURRENT file and confirm this FROM text occurs exactly 1 time:

FROM:
        print(f"Proposed task store is unreadable: {exc}", file=sys.stderr)
        sys.exit(1)

    if getattr(args, "json", False):
        print(json.dumps({
            "version": 1,
            "job_id": job_id,
            "count": len(tasks),

Replace it with this TO text:
        print(f"Proposed task store is unreadable: {exc}", file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.list_options import ListOptionError, apply_list_options
    try:
        tasks = apply_list_options(
            tasks,
            sort=getattr(args, "sort", None), desc=getattr(args, "desc", False),
            since=getattr(args, "since", None), until=getattr(args, "until", None),
            limit=getattr(args, "limit", None),
            sort_fields={
                "created_at": lambda t: t.created_at,
                "status": lambda t: t.status.value if hasattr(t.status, "value") else str(t.status),
                "priority": lambda t: t.priority,
            },
            default_sort_field="created_at",
            date_getter=lambda t: t.created_at.isoformat(),
        )
    except ListOptionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if getattr(args, "json", False):
        print(json.dumps({
            "version": 1,
            "job_id": job_id,
            "count": len(tasks),

Note: `sys` and `json` are already imported at module scope in propose_cmd.py — do not add duplicate imports. `_cmd_propose_list`'s dispatch site already forwards `args` unchanged (`"propose.list": lambda args: _cmd_propose_list(args),`) — do NOT touch the dispatch site.

PAIR E1 — apps/cli/commands/external_builder_cmd.py — REWRITE. Before applying, re-read the CURRENT file and confirm this FROM text occurs exactly 1 time:

FROM:
def _cmd_external_builder_submission_list(args: Any) -> None:
    from packages.orchestration.external_builder_sandbox import load_external_submissions
    subs = load_external_submissions(job_id=str(args.job_id))
    out = {"job_id": str(args.job_id), "submission_count": len(subs),

Replace it with this TO text:
def _cmd_external_builder_submission_list(args: Any) -> None:
    from packages.orchestration.external_builder_sandbox import load_external_submissions
    from packages.orchestration.list_options import ListOptionError, apply_list_options
    subs = load_external_submissions(job_id=str(args.job_id))
    try:
        subs = apply_list_options(
            subs,
            sort=getattr(args, "sort", None), desc=getattr(args, "desc", False),
            since=getattr(args, "since", None), until=getattr(args, "until", None),
            limit=getattr(args, "limit", None),
            sort_fields={
                "created_at": lambda s: s.get("received_at", ""),
                "state": lambda s: s.get("state", ""),
            },
            default_sort_field="created_at",
            date_getter=lambda s: s.get("received_at") or None,
        )
    except ListOptionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    out = {"job_id": str(args.job_id), "submission_count": len(subs),

Note: `sys` and `json` are already imported at module scope in external_builder_cmd.py — do not add duplicate imports. `"external-builder.submission-list": _cmd_external_builder_submission_list,` in COMMAND_HANDLERS is a DIRECT function reference (no lambda at all) — do NOT touch the dispatch site.

TEST T1 — tests/cli/test_review_cmd.py — append two new test functions at the END of the file (the file currently ends with `assert data["recommendations"][0]["created_at"] == "2026-09-04T00:00:00+00:00"` as its last line). Before applying, re-read the CURRENT file to confirm your insertion point is genuinely the end of the file.

Append this new content (two blank lines before it, matching the file's existing spacing between its two top-level functions):

def test_limit_caps_returned_recommendations(capsys):
    from apps.cli.commands.review_cmd import _cmd_review_list

    job_stub = SimpleNamespace(id=uuid4())
    recs = [
        {"id": "rec1", "title": "A", "status": "pending", "created_at": "2026-09-01T00:00:00+00:00"},
        {"id": "rec2", "title": "B", "status": "pending", "created_at": "2026-09-02T00:00:00+00:00"},
        {"id": "rec3", "title": "C", "status": "pending", "created_at": "2026-09-03T00:00:00+00:00"},
    ]
    args = Namespace(job_id=str(job_stub.id), json=True, limit="2")
    with patch("packages.orchestration.storage.load_job", return_value=job_stub), \
         patch("packages.orchestration.reviewer.list_recommendations", return_value=recs):
        _cmd_review_list(args)

    data = json.loads(capsys.readouterr().out)
    assert len(data["recommendations"]) == 2


def test_unknown_sort_field_exits_nonzero():
    from apps.cli.commands.review_cmd import _cmd_review_list

    job_stub = SimpleNamespace(id=uuid4())
    args = Namespace(job_id=str(job_stub.id), json=True, sort="bogus")
    with patch("packages.orchestration.storage.load_job", return_value=job_stub), \
         patch("packages.orchestration.reviewer.list_recommendations", return_value=_recs()):
        with pytest.raises(SystemExit) as exc:
            _cmd_review_list(args)
    assert exc.value.code == 1

This test file does not currently import `pytest` at module scope — add `import pytest` to its existing import block (it currently imports `json`, `Namespace`, `SimpleNamespace`, `patch`, `uuid4`) as part of this same commit, since `pytest.raises` is used by the new test.

TEST T2 — tests/cli/test_propose_cli.py — insert two new test methods into class `TestProposeListHandler`, at the end of that class (immediately after its `test_list_invalid_status` method, which is currently the class's and the file's last method). Before applying, re-read the CURRENT file to confirm this FROM anchor occurs exactly 1 time:

FROM:
    def test_list_invalid_status(self, tmp_store):
        handlers = collect_all_handlers()
        args = SimpleNamespace(job_id=JOB_ID, status="bogus", json=False)
        with pytest.raises(SystemExit):
            handlers["propose.list"](args)

Replace it with this TO text (note it contains the FROM text as its head, followed by two new test methods):
    def test_list_invalid_status(self, tmp_store):
        handlers = collect_all_handlers()
        args = SimpleNamespace(job_id=JOB_ID, status="bogus", json=False)
        with pytest.raises(SystemExit):
            handlers["propose.list"](args)

    def test_limit_caps_returned_tasks(self, tmp_store, capsys):
        add_proposed_task(JOB_ID, ProposedTask(title="A"))
        add_proposed_task(JOB_ID, ProposedTask(title="B"))
        add_proposed_task(JOB_ID, ProposedTask(title="C"))
        handlers = collect_all_handlers()
        args = SimpleNamespace(job_id=JOB_ID, status=None, json=True, limit="2")
        handlers["propose.list"](args)
        data = json.loads(capsys.readouterr().out)
        assert data["count"] == 2

    def test_unknown_sort_field_exits_nonzero_for_list(self, tmp_store):
        add_proposed_task(JOB_ID, ProposedTask(title="A"))
        handlers = collect_all_handlers()
        args = SimpleNamespace(job_id=JOB_ID, status=None, json=True, sort="bogus")
        with pytest.raises(SystemExit):
            handlers["propose.list"](args)

TEST T3 — tests/cli/test_external_builder_cli.py — append two new test functions at the END of the file (the file currently ends with `assert "received=" in r2.stdout` as its last line). Before applying, re-read the CURRENT file to confirm your insertion point is genuinely the end of the file.

Append this new content (two blank lines before it, matching the file's existing spacing between its top-level functions):

def test_submission_list_limit_caps_count(env):
    job_id = _job(env)
    pkg = json.loads(run_grouped_cli(["external-builder", "package-create", job_id, "--json"], env).stdout)
    for label in ("claude", "gpt", "gemini"):
        cf = env / f"resp-{label}.md"; cf.write_text(_SAFE_CAND)
        run_grouped_cli(["external-builder", "submit", pkg["package_id"],
                         "--candidate-file", str(cf), "--source-label", label, "--json"], env)
    r = run_grouped_cli(["external-builder", "submission-list", job_id, "--json", "--limit", "2"], env)
    d = json.loads(r.stdout)
    assert d["submission_count"] == 2


def test_submission_list_unknown_sort_field_exits_nonzero(env):
    job_id = _job(env)
    pkg = json.loads(run_grouped_cli(["external-builder", "package-create", job_id, "--json"], env).stdout)
    cf = env / "resp.md"; cf.write_text(_SAFE_CAND)
    run_grouped_cli(["external-builder", "submit", pkg["package_id"],
                     "--candidate-file", str(cf), "--source-label", "claude", "--json"], env)
    r = run_grouped_cli(["external-builder", "submission-list", job_id, "--sort", "bogus"], env)
    assert r.returncode == 1
    assert "created_at" in r.stderr

Commit C2 covers all six files (three production pairs, three test appends) as ONE commit.

============================================================
PLAN19 — whole-file replace of `.agent/plan.md`. Byte length must be exactly 2352 (UTF-8), confirm with a binary-mode byte comparison after writing.

PLAN19 text (copy exactly):
# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 18, session 6 - T003 batch 6: `review.list`, `propose.list` and
`external-builder.submission-list` wired to `apply_list_options`, all
`default_sort_field="created_at"`. All three dispatch with `args`
passed straight through (no lambda extraction), so each needed ONLY
ONE pair (the handler body) - no dispatch-site pair, unlike
project/blocker/decision. None had an order-asserting test. Row
shapes vary: review.list's rows are dicts, propose.list's are
ProposedTask pydantic models (`created_at.isoformat()`), and
external-builder.submission-list's are dicts keyed `received_at`
mapped to the shared `created_at` sort-field name for flag
consistency, per Design's "same words for same flags".

## Next Steps

- T003 is now done for every plain single-collection list command.
  Remaining: patch.list (approval_queue.py's table renderer) and
  loop.list (rows built from two different collections) still need
  their own look before wiring - neither is a plain single-collection
  list. config.list/worker.list/execution.list stay excused per Risks.
- change.list's event-log CREATED date stays open, UNRELATED to D1:
  do_run.py's event stays dead, job.py's real event carries no
  intent_id to join on - see DECISION F262 D1's Alternative section.
- Once patch.list/loop.list are wired (or excused), add an
  integration-level smoke test proving the ten-second demo in
  Acceptance: a named run findable by one command with --since/--sort.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix.
- A command with its OWN meaningful non-date default order (queue.list's
  priority, DECISION F262 D2) opts out via `default_sort_field=None` -
  audit patch.list/loop.list for this shape before wiring them.

============================================================
CONSTRAINTS:
1. Do not touch any list command other than review.list/propose.list/external-builder.submission-list this round.
2. Do not widen or change `apply_list_options` itself (packages/orchestration/list_options.py) — it is unchanged this round.
3. No file besides these may be written: `apps/cli/commands/review_cmd.py`, `apps/cli/commands/propose_cmd.py`, `apps/cli/commands/external_builder_cmd.py`, `tests/cli/test_review_cmd.py`, `tests/cli/test_propose_cli.py`, `tests/cli/test_external_builder_cli.py`, `.agent/authored/f262-r18.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`.
4. Re-confirm each FROM string's exact occurrence count (must be 1) against the file's CURRENT on-disk content immediately before applying — not against the copy quoted in this prompt.
5. Commit order is exactly C0a, C0b, C1, C2, C3, C4, each its own commit.
6. Run `git status --porcelain` after every commit; it must be empty before proceeding.
7. `.agent/STOP` must be absent before C0a and re-checked before C4. If it appears, stop immediately, finish only a half-written commit, and write the handoff reporting the STOP instead of continuing.
8. Capture REAL exit codes for every command — do not report "green" as a bare word.
9. Do NOT touch any dispatch/COMMAND_HANDLERS lambda for these three commands — all three already forward `args` unchanged and need no dispatch-site pair, unlike prior rounds' project/blocker/decision.
10. Known sandbox quirks in this repo (from prior rounds): `python3 -m py_compile <files>` as a literal multi-arg command has sometimes been denied by the Bash sandbox — if denied, substitute `python3 -c "import py_compile; py_compile.compile('path/a.py', doraise=True); ...; print('OK')"` and declare the substitution. `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`, and `cp` are denied outright — use `monkeypatch`/`python3 -c "import shutil; shutil.copyfile(a,b)"` if ever needed. Never use a sandbox-override flag to route around a denial.

DONE WHEN (run every one of these EXACTLY as written and record the REAL, complete output of each in your handback — quote actual pytest/py_compile output, do not summarize as "passed"):
G1. `python3 -c "import py_compile; py_compile.compile('apps/cli/commands/review_cmd.py', doraise=True); py_compile.compile('apps/cli/commands/propose_cmd.py', doraise=True); py_compile.compile('apps/cli/commands/external_builder_cmd.py', doraise=True); py_compile.compile('tests/cli/test_review_cmd.py', doraise=True); py_compile.compile('tests/cli/test_propose_cli.py', doraise=True); py_compile.compile('tests/cli/test_external_builder_cli.py', doraise=True); print('OK')"` → must print OK.
G2. `python3 -m pytest tests/cli/test_review_cmd.py tests/cli/test_propose_cli.py tests/cli/test_external_builder_cli.py -q` → expect 46 passed (2+29+9=40 pre-existing + 6 new). Report the exact number.
G3. `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q` → expect 646 passed (515+52+21+16+42), unmoved. Report the exact number.
G4. `sha256sum .agent/authored/f262-r18.md .agent/last_block.md` → must print one identical digest for both files. Report both digests.
G5. Byte-read `.agent/live_review.md` immediately before C1 and immediately after C1 (Python, binary mode) → before must be 2465111, after must be 2467532. Report both numbers.
G6. Byte-read `.agent/plan.md` immediately after C3, binary mode → must be exactly 2352 bytes, byte-for-byte equal to the PLAN19 text above. Report the byte count and whether it matched exactly.
G7. `git status --porcelain` → empty, checked before C0a and immediately before C4. Report both checks.
G8. `git ls-files .remedy-wt` → empty. Report the output (should be nothing).

HANDBACK: write a full completion report and rewrite `.agent/handoff.md` per docs/agents/handback_template.md and AGENTS.md's "### handoff.md" section — include the changed-files table (path, +/-, reason) for every commit, an item-status table (Item | Status | Reason) covering every bundle item (C0a..C4, and each gate G1..G8), the real verification results for every gate above, the SESSION NUMBER (this is SESSION 6 of feature F262, round 18), and the next expected action (round 19: investigate patch.list and loop.list's own shapes before deciding how/whether to wire them into T003, per PLAN19's Next Steps — this is the LAST of the currently-known T003 batches, so round 19 may lead into T003 closure). After the handoff commit (C4), run `git push -u origin feature/f262-list-commands-v2` and report the push result. Do NOT create a PR. Do NOT merge anything. Do NOT touch `main`.
──────────────────────────────────────────────────────────────