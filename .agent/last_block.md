── STEP T003 batch7 — F262 List commands v2 ────────────────────────
Goal: Wire patch.list into the shared apply_list_options helper (T003), record DECISION F262 D3 documenting why loop.list is deferred to round 20, and book round 18's already-PASSED verdict into the ledger.

Bundle:
C0a. Save this entire step block, byte for byte, to a NEW file `.agent/authored/f262-r19.md`.
C0b. Whole-file replace `.agent/last_block.md` with the same bytes (mirror of C0a).
C1. Append GATE18 (below) to `.agent/live_review.md`.
C2. Append DECISION F262 D3 (below) to `.agent/decisions.md`.
C3. Production change: PAIR PA1 + PAIR PA2 in `apps/cli/commands/patch.py`, plus TEST T1 appended to `tests/test_patch_intent_approval.py`. ONE commit covering both files.
C4. Whole-file replace `.agent/plan.md` with PLAN20 (below).
C5. Rewrite `.agent/handoff.md` (handback) per docs/agents/handback_template.md; this is the round's LAST commit.

============================================================
GATE18 — append verbatim as a new line at the end of `.agent/live_review.md`. The current file ends with NO trailing newline. C1 must: read the current file, append exactly one `\n` character followed by the GATE18 text below (with no trailing newline after it either). Do this with Python (`pathlib.Path.write_bytes`), not a shell append.

GATE18 text (copy exactly, it is a single line with zero internal newlines, 2805 bytes UTF-8):
Gate: R18 — the F262 R18 entry. R18 SHIPPED T003 BATCH 6, `review.list`, `propose.list` and `external-builder.submission-list` wired to `apply_list_options`, all `default_sort_field="created_at"` — all three dispatch with `args` forwarded unchanged (no lambda extraction), so each needed ONLY ONE pair (the handler body), no dispatch-site pair; none had an order-asserting test; row shapes varied (dicts for review.list, ProposedTask pydantic models for propose.list needing `.isoformat()`, and dicts keyed `received_at` for external-builder.submission-list mapped to the shared `created_at` sort-field name) — AND THE REVIEWER RE-RAN EVERY GATE ITSELF. TRANSPORT HELD: `.agent/authored/f262-r18.md`/`.agent/last_block.md` share one sha256 digest, `58f130673d6c8a3eb626e4f4593d64676e07f0c53202c3a0342e3d8067a53559`, confirmed by the reviewer's own sha256sum of both committed files. THE DIFF WAS READ, NOT ONLY GATED: `git diff 25ef619839597ff4ec9fdd9d6c626e4597ec9ea5..f8ba752121e55af75231081f9a29490117ceea55` for `apps/cli/commands/review_cmd.py`, `apps/cli/commands/propose_cmd.py`, `apps/cli/commands/external_builder_cmd.py`, `tests/cli/test_review_cmd.py`, `tests/cli/test_propose_cli.py` and `tests/cli/test_external_builder_cli.py` shows exactly PAIR R1, PAIR PR1, PAIR E1, and the six new test functions across the three test files, every dispatch site (`review.list`, `propose.list`, `external-builder.submission-list`) confirmed UNTOUCHED (they already forward `args` unchanged), every other line in all six files untouched, confirmed by reading the full diff. `python3 -c "import py_compile; ..."` printed OK for all six touched files, run independently by the reviewer. THE GATE17 LEDGER APPEND (commit b3203e83) WAS RE-VERIFIED BYTE-EXACT: base 2465111 plus one newline plus GATE17 (2420 bytes, 0 internal newlines) equals 2467532, matching the file's own on-disk size measured immediately after the round. THE TESTS MOVED EXACTLY AS THE HANDBACK CLAIMED, reproduced independently: `python3 -m pytest tests/cli/test_review_cmd.py tests/cli/test_propose_cli.py tests/cli/test_external_builder_cli.py -q` read 46 passed (40 pre-existing plus 6 new). THE STATE READERS AND THE CANARY WERE UNMOVED, reproduced by the reviewer as ONE combined invocation: `tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py` read 646 passed, matching 515+52+21+16+42 exactly. HYGIENE HELD: `git status --porcelain` empty at HEAD `f8ba7521`, `git ls-files .remedy-wt` empty, `.agent/STOP` absent. THE PLAN HELD: `.agent/plan.md` measured 2352 bytes, matching the handback's own reported byte-for-byte comparison of the authored PLAN19 slice against the written file. THE VERDICT IS PASS.

Base file size immediately before C1 must read 2467532 (confirm with a fresh Python byte read before writing). Post-C1 size must read exactly 2470337 (2467532 + 1 + 2805). Verify both numbers yourself and report them.

Note the arithmetic: 2467532 + 1 + 2805 = 2470338. If your own byte read of GATE18's text differs from 2805, STOP and report the discrepancy rather than adjusting silently — re-copy the text above exactly and re-measure.
============================================================

DECISION F262 D3 — append verbatim to `.agent/decisions.md`. The current file ends with NO trailing newline. C2 must: read the current file, append exactly one `\n` character followed by the DECISION text below (with no trailing newline after it either). Do this with Python (`pathlib.Path.write_bytes`).

DECISION text (copy exactly, byte length 3645 UTF-8, contains internal newlines as shown — this is a multi-paragraph block, unlike GATE18 above):
## DECISION F262 D3 (2026-09-05, F262 R19) — loop.list keeps its config-declaration order as the default (`default_sort_field=None`, D2 precedent); wiring is a real restructure deferred to round 20, not implemented this round

CONTEXT. Round 19 investigated `loop.list` (`apps/cli/commands/loop_cmd.py::_cmd_loop_list`) as the last unwired T003 target PLAN19 flagged as needing its own look, alongside `patch.list` (wired this same round, ordinary shape, no DECISION needed). `load_loop_specs()` returns loops in the order they are declared in `remedy.toml` — an operator-authored, load-bearing order (which loop the operator wrote first), not a store artifact with a meaningful timestamp of its own. No loop record carries `created_at`; the ONLY date-shaped value anywhere in the command is `last_run_created_at`, computed per-spec via `last_run_for_loop(spec.name)` — and today that lookup runs ONLY inside the `if json_output:` branch, so the TEXT branch (`_last_run_label`) performs an independent, duplicate lookup of the same data. A loop that has never run has `last_run_created_at = None`, so sorting by it is not equivalent to sorting by anything resembling creation order, and is undefined for the (common) case of zero runs.

CHOSEN. `loop.list` keeps `default_sort_field=None` — its declared config order stays the default with no flag, exactly like `queue.list`'s priority order under DECISION F262 D2 — because the order is real and operator-authored, not arbitrary. `--sort last_run_created_at` becomes available as an explicit opt-in for the one case where a date does exist. Implementing this requires restructuring `_cmd_loop_list` to build ONE row list of `(spec, last_run_created_at, last_run_state)` tuples UNCONDITIONALLY (moving the `last_run_for_loop` call out of the `json_output`-only branch), run `apply_list_options` once over that list, and have BOTH the text and json branches render from the same post-`apply_list_options` list — removing the text branch's separate `_last_run_label` call in favour of reading the tuple's own precomputed `last_run_created_at`/`last_run_state`, which also removes today's duplicate lookup. This is a materially larger change than every other T003 batch (a genuine control-flow restructure, not an insertion before the existing render branches), so it is deferred to round 20 as its own step rather than folded into round 19's patch.list batch, keeping round 19's bundle coherent per the planner_reviewer_prompt.md §3 step-sizing rule ("shrink steps... when the ground is unknown").

ALTERNATIVE CONSIDERED AND REJECTED. Force `last_run_created_at` as the default sort key anyway, reading T2_F262.md's Acceptance literally ("newest-first... everywhere"). Rejected for the same reason D2 rejected it for `queue.list`: Acceptance's DONE bar is about FINDING a past run by command, which `--sort last_run_created_at` already satisfies as an explicit opt-in, and forcibly reordering loops away from their operator-declared sequence — the one piece of information this store actually carries reliably — would be a silent, undesired behavior change for a command whose primary use is "what are my loops and did they run", not "what ran most recently".

CONSEQUENCE. No code changes to `loop_cmd.py` or `list_options.py` land in this round (R19); this DECISION is the specification round 20 implements against. `docs/roadmap/features/T2_F262.md` is not amended — this DECISION documents a scope boundary already implicit in "a store whose order is already meaningful is not the class of gap T003 targets" (D2's own words), extended to a second command of the same shape.

Base file size immediately before C2 must read 802422 (confirm with a fresh Python byte read before writing). Post-C2 size must read exactly 806068 (802422 + 1 + 3645). Verify both numbers yourself and report them.
============================================================

PAIR PA1 — apps/cli/commands/patch.py — REWRITE. Before applying, re-read the CURRENT file and confirm this FROM text occurs exactly 1 time:

FROM:
def _cmd_list_patch_intents(job_id_str: str, *, json_output: bool = False) -> None:
    job_id = resolve_job_id(job_id_str)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.approval_queue import format_intent_list, list_patch_intents
    intents = list_patch_intents(job)
    if json_output:

Replace it with this TO text:
def _cmd_list_patch_intents(
    job_id_str: str,
    *,
    json_output: bool = False,
    sort: str | None = None,
    desc: bool = False,
    since: str | None = None,
    until: str | None = None,
    limit: str | None = None,
) -> None:
    job_id = resolve_job_id(job_id_str)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.approval_queue import format_intent_list, list_patch_intents
    from packages.orchestration.list_options import ListOptionError, apply_list_options
    intents = list_patch_intents(job)
    try:
        intents = apply_list_options(
            intents,
            sort=sort, desc=desc, since=since, until=until, limit=limit,
            sort_fields={
                "created_at": lambda i: i.get("created_at") or "",
                "state": lambda i: i.get("state", ""),
                "risk": lambda i: i.get("risk", ""),
            },
            default_sort_field="created_at",
            date_getter=lambda i: i.get("created_at") or None,
        )
    except ListOptionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    if json_output:

Note: `sys` is already imported at module scope in patch.py (line 6, `import sys`) — do not add a duplicate import.

PAIR PA2 — apps/cli/commands/patch.py — REWRITE. Before applying, re-read the CURRENT file and confirm this FROM text occurs exactly 1 time:

FROM:
    "patch.list": lambda args: _cmd_list_patch_intents(args.job_id, json_output=args.json),

Replace it with this TO text:
    "patch.list": lambda args: _cmd_list_patch_intents(
        args.job_id,
        json_output=args.json,
        sort=getattr(args, "sort", None),
        desc=getattr(args, "desc", False),
        since=getattr(args, "since", None),
        until=getattr(args, "until", None),
        limit=getattr(args, "limit", None),
    ),

TEST T1 — tests/test_patch_intent_approval.py — append two new test methods into class `TestCmdListPatchIntents`, at the end of that class. Before applying, re-read the CURRENT file and confirm this FROM anchor occurs exactly 1 time:

FROM:
    def test_json_output_has_created_at_key(self, tmp_path, monkeypatch, capsys):
        job = self._save(tmp_path, monkeypatch)
        _add_patch_artifact(job)
        save_job(job)
        from apps.cli.commands.patch import _cmd_list_patch_intents
        _cmd_list_patch_intents(str(job.id), json_output=True)
        data = json.loads(capsys.readouterr().out)
        assert "created_at" in data["intents"][0]

Replace it with this TO text (note it contains the FROM text as its head, followed by two new test methods):
    def test_json_output_has_created_at_key(self, tmp_path, monkeypatch, capsys):
        job = self._save(tmp_path, monkeypatch)
        _add_patch_artifact(job)
        save_job(job)
        from apps.cli.commands.patch import _cmd_list_patch_intents
        _cmd_list_patch_intents(str(job.id), json_output=True)
        data = json.loads(capsys.readouterr().out)
        assert "created_at" in data["intents"][0]

    def test_limit_caps_returned_intents(self, tmp_path, monkeypatch, capsys):
        job = self._save(tmp_path, monkeypatch)
        _add_patch_artifact(job, intent_count=3)
        save_job(job)
        from apps.cli.commands.patch import _cmd_list_patch_intents
        _cmd_list_patch_intents(str(job.id), json_output=True, limit="2")
        data = json.loads(capsys.readouterr().out)
        assert data["intent_count"] == 2

    def test_unknown_sort_field_exits_nonzero(self, tmp_path, monkeypatch):
        job = self._save(tmp_path, monkeypatch)
        _add_patch_artifact(job)
        save_job(job)
        from apps.cli.commands.patch import _cmd_list_patch_intents
        with pytest.raises(SystemExit) as exc_info:
            _cmd_list_patch_intents(str(job.id), json_output=True, sort="bogus")
        assert exc_info.value.code == 1

Note: `pytest` and `json` are already imported at module scope in tests/test_patch_intent_approval.py (used elsewhere in the same class) — do not add duplicate imports. `_add_patch_artifact(job, intent_count=3)` is a pre-existing helper in this file that adds 3 intents in one call — do not reimplement it.

Commit C3 covers both files (patch.py's two pairs, and the test file's append) as ONE commit.

============================================================
PLAN20 — whole-file replace of `.agent/plan.md`. Byte length must be exactly 2180 (UTF-8), confirm with a binary-mode byte comparison after writing.

PLAN20 text (copy exactly):
# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 19, session 6 - T003 batch 7: `patch.list` wired to
`apply_list_options` with `default_sort_field="created_at"` (ordinary
shape, dict rows, dispatch lambda needed both pairs, no order test).
`loop.list` was investigated but NOT wired this round - DECISION F262
D3 keeps its config-declaration order as default (D2 precedent) and
specifies a real restructure (unify text/json into one row list before
sorting) that round 20 implements, since it does not fit the
insert-before-render shape every other T003 batch used.

## Next Steps

- Round 20: implement DECISION F262 D3 - restructure `_cmd_loop_list`
  to build `(spec, last_run_created_at, last_run_state)` rows
  unconditionally, apply_list_options with `default_sort_field=None`,
  render both text and json from the same post-option list.
- After loop.list, T003 is done for every list command in scope.
  config.list/worker.list/execution.list stay excused per Risks.
- change.list's event-log CREATED date stays open, UNRELATED to D1:
  do_run.py's event stays dead, job.py's real event carries no
  intent_id to join on - see DECISION F262 D1's Alternative section.
- Once loop.list lands, add an integration-level smoke test proving
  the ten-second demo in Acceptance: a named run findable by one
  command with --since/--sort.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix.
- A command with its OWN meaningful non-date default order (queue.list's
  priority D2, loop.list's config order D3) opts out via
  `default_sort_field=None` rather than losing that order.

============================================================
CONSTRAINTS:
1. Do not touch `loop_cmd.py` or `list_options.py` this round — DECISION D3 defers that to round 20.
2. Do not touch any list command other than patch.list this round.
3. No file besides these may be written: `apps/cli/commands/patch.py`, `tests/test_patch_intent_approval.py`, `.agent/authored/f262-r19.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/handoff.md`.
4. Re-confirm each FROM string's exact occurrence count (must be 1) against the file's CURRENT on-disk content immediately before applying — not against the copy quoted in this prompt.
5. Commit order is exactly C0a, C0b, C1, C2, C3, C4, C5, each its own commit.
6. Run `git status --porcelain` after every commit; it must be empty before proceeding.
7. `.agent/STOP` must be absent before C0a and re-checked before C5. If it appears, stop immediately, finish only a half-written commit, and write the handoff reporting the STOP instead of continuing.
8. Capture REAL exit codes for every command — do not report "green" as a bare word.
9. Known sandbox quirks in this repo (from prior rounds): `python3 -m py_compile <files>` as a literal multi-arg command has sometimes been denied by the Bash sandbox — if denied, substitute `python3 -c "import py_compile; py_compile.compile('path/a.py', doraise=True); ...; print('OK')"` and declare the substitution. `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`, and `cp` are denied outright — use `monkeypatch`/`python3 -c "import shutil; shutil.copyfile(a,b)"` if ever needed. Never use a sandbox-override flag to route around a denial.

DONE WHEN (run every one of these EXACTLY as written and record the REAL, complete output of each in your handback — quote actual pytest/py_compile output, do not summarize as "passed"):
G1. `python3 -c "import py_compile; py_compile.compile('apps/cli/commands/patch.py', doraise=True); py_compile.compile('tests/test_patch_intent_approval.py', doraise=True); print('OK')"` → must print OK.
G2. `python3 -m pytest tests/test_patch_intent_approval.py -q` → expect 70 passed (68 pre-existing + 2 new). Report the exact number.
G3. `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q` → expect 646 passed (515+52+21+16+42), unmoved. Report the exact number.
G4. `sha256sum .agent/authored/f262-r19.md .agent/last_block.md` → must print one identical digest for both files. Report both digests.
G5. Byte-read `.agent/live_review.md` immediately before C1 and immediately after C1 AND `.agent/decisions.md` immediately before C2 and immediately after C2 (Python, binary mode) → live_review.md before must be 2467532, after must be 2470338; decisions.md before must be 802422, after must be 806068. Report all four numbers.
G6. Byte-read `.agent/plan.md` immediately after C4, binary mode → must be exactly 2180 bytes, byte-for-byte equal to the PLAN20 text above. Report the byte count and whether it matched exactly.
G7. `git status --porcelain` → empty, checked before C0a and immediately before C5. Report both checks.
G8. `git ls-files .remedy-wt` → empty. Report the output (should be nothing).

HANDBACK: write a full completion report and rewrite `.agent/handoff.md` per docs/agents/handback_template.md and AGENTS.md's "### handoff.md" section — include the changed-files table (path, +/-, reason) for every commit, an item-status table (Item | Status | Reason) covering every bundle item (C0a..C5, and each gate G1..G8), the real verification results for every gate above, the SESSION NUMBER (this is SESSION 6 of feature F262, round 19), and the next expected action (round 20: implement DECISION F262 D3's loop.list restructure per PLAN20's Next Steps — this is expected to be the LAST T003 batch). After the handoff commit (C5), run `git push -u origin feature/f262-list-commands-v2` and report the push result. Do NOT create a PR. Do NOT merge anything. Do NOT touch `main`.
──────────────────────────────────────────────────────────────