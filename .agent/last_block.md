═══════════════════════════════════════════════════════════════
STEP — F262 R15/? — T003 batch 3: tournament.list wiring
═══════════════════════════════════════════════════════════════

GOAL: Continue T003 with its third batch: wire `packages/orchestration/list_options.py` into `tournament.list`. Also book round 14's reviewer verdict into the ledger.

BACKGROUND FACTS (already verified by the reviewer — do not re-derive):
- `tournament.list`'s dispatch is `"tournament.list": _cmd_tournament_list` in `apps/cli/commands/tournament_cmd.py` — a DIRECT handler reference, not a lambda wrapper. `_cmd_tournament_list(args)` already receives the full `args` namespace, so wiring needs only ONE pair (the function body) — no separate dispatch-lambda pair, unlike `job.list`/`queue.list`/`memory.list`.
- `list_tournament_reports()` (`packages/orchestration/model_route_tournament.py:599`) builds its result by `sorted(root.iterdir())` — sorting by the ON-DISK DIRECTORY NAME (an internal tournament id), which is an ARBITRARY order with no operational meaning, unlike `queue.list`'s deliberate priority order (DECISION F262 D2). This is exactly the "arbitrary order presented as recency" case T2_F262.md's Design section warns against — `default_sort_field="created_at"` is the correct, unconditional choice here, with no D2-style opt-out needed.
- `reps` (the list `list_tournament_reports()` returns) is consumed by BOTH the `--json` branch (via `out["reports"]`, built FROM `reps`) and the text branch (iterating `reps` directly) — reassigning `reps` itself once, before either branch, updates both by construction, the same shape `job.list`'s R13 wiring used.
- `reps` entries are plain dicts with keys `tournament_id`, `status`, `winner_competitor_id`, `confidence` (always a populated string: `"low"`/`"medium"`/`"high"`, never `None`), `created_at`. `tests/cli/test_tournament_cli.py` has no test asserting a specific multi-report ORDER today — confirmed by the reviewer, so no D2-style regression risk exists here.

═══ COMMIT SEQUENCE (5 commits total) ═══

──────────────────────────────────────────────────────────
C0a — save this entire step block verbatim
──────────────────────────────────────────────────────────
Save the FULL literal text of this prompt message (everything between the "STEP —" header above and the final "END OF BLOCK" marker at the bottom) to `.agent/authored/f262-r15.md`, byte for byte, exactly as received. Commit message: `F262 R15 C0a: save block verbatim to .agent/authored/f262-r15.md`

──────────────────────────────────────────────────────────
C0b — mirror to .agent/last_block.md
──────────────────────────────────────────────────────────
Copy `.agent/authored/f262-r15.md` to `.agent/last_block.md`, whole-file replace. Verify `sha256sum` of both files matches after writing. Commit message: `F262 R15 C0b: mirror block to .agent/last_block.md`

──────────────────────────────────────────────────────────
C1 — append GATE14 to .agent/live_review.md
──────────────────────────────────────────────────────────
Append exactly the text between the GATE14 markers below to the END of `.agent/live_review.md`: one newline, then the GATE14 text verbatim (it is a SINGLE LINE — no internal newlines), nothing else added.

<<<BEGIN GATE14>>>
Gate: R14 — the F262 R14 entry. R14 continued T003 (batch 2): `queue.list` and `memory.list` wired to `apply_list_options` — `queue.list` with `default_sort_field=None` per DECISION F262 D2 (preserving its existing, load-bearing PRIORITY default order), `memory.list` with `default_sort_field="created_at"` (unchanged no-flag behaviour, new capability layered on top); `list_options.py`'s `apply_list_options` widened to accept `default_sort_field: str | None = None` with an early-exit from the sort step when both `sort` and `default_sort_field` are `None` — AND THE REVIEWER RE-RAN EVERY GATE ITSELF. TRANSPORT HELD: `.agent/authored/f262-r14.md`/`.agent/last_block.md` share one sha256 digest, `394dc28973984bb8d7803197196f575e0ec72d0893c78180574f2b619c95f51b`, confirmed by the reviewer's own sha256sum of both committed files. THE DIFF WAS READ, NOT ONLY GATED: `git diff 3459e7a8..c65f8342` shows exactly PAIR P1 (`list_options.py`'s widened signature and guarded sort block), PAIR P2/P3 (`queue_cmd.py`'s `_cmd_queue_list` body and dispatch lambda), PAIR P4/P5 (`memory.py`'s `_cmd_memory_list` body and dispatch lambda), and the three test appends (`tests/orchestration/test_list_options.py`, `tests/cli/test_queue_cmd.py`, `tests/test_grouped_cli.py`), every diff re-read in full, nothing else touched. `python3 -m py_compile` exited 0 on all six touched files, run together by the reviewer. THE CONSTRAINT-9 REGRESSION CHECK WAS RE-RUN BY THE REVIEWER: `tests/cli/test_queue_cmd.py::TestAdd::test_priority_is_recorded_and_orders_the_listing` read 1 passed, unmodified — DECISION F262 D2's own regression proof held. THE GATE13 LEDGER APPEND AND THE DECISION F262 D2 APPEND (both commit 06f35c1e) WERE BOTH RE-VERIFIED BYTE-EXACT: live_review.md base 2455026 plus one newline plus GATE13 (2386 bytes, 0 internal newlines) equals 2457413; decisions.md base 797530 plus one newline plus the 4891-byte DECISION equals 802422 — both exact. THE TESTS MOVED EXACTLY AS THE HANDBACK CLAIMED, reproduced independently: `tests/orchestration/test_list_options.py tests/cli/test_queue_cmd.py tests/test_grouped_cli.py` read 562 passed (556 pre-existing plus 6 new). THE STATE READERS AND THE CANARY WERE UNMOVED, reproduced by the reviewer as ONE combined invocation: `tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py` read 646 passed, matching 515+52+21+16+42 exactly. HYGIENE HELD: `git status --porcelain` empty at HEAD `60fe2ed1`, `git ls-files .remedy-wt` empty, `.agent/STOP` absent. THE PLAN HELD: `.agent/plan.md` measured 2880 bytes, matching the handback's own reported byte-for-byte comparison of the authored PLAN15 slice against the written file. THE VERDICT IS PASS.
<<<END GATE14>>>

Commit message: `F262 R15 C1: append GATE14 to live_review.md - books round 14's PASS verdict`

──────────────────────────────────────────────────────────
C2 — production code + tests (one commit, one production rewrite, one test append)
──────────────────────────────────────────────────────────

PAIR P1 (REWRITE) — `apps/cli/commands/tournament_cmd.py`, `_cmd_tournament_list` wired to `apply_list_options` with `default_sort_field="created_at"`. This is the WHOLE current function — re-read the file yourself first and confirm this FROM matches exactly before applying; if it does not match, STOP and report the mismatch rather than guessing.
FROM (exact):
<<<BEGIN PAIR_P1_FROM>>>
def _cmd_tournament_list(args: Any) -> None:
    from packages.orchestration.model_route_tournament import list_tournament_reports
    reps = list_tournament_reports(job_id=str(args.job_id))
    out = {"job_id": str(args.job_id), "report_count": len(reps),
           "reports": [{"tournament_id": r.get("tournament_id"), "status": r.get("status"),
                        "winner_competitor_id": r.get("winner_competitor_id", ""),
                        "confidence": r.get("confidence"),
                        "created_at": r.get("created_at", "")} for r in reps]}
    if getattr(args, "json", False):
        print(json.dumps(out, indent=2))
        return
    print(f"Tournament reports for {str(args.job_id)[:8]}: {len(reps)}")
    for r in reps:
        winner = r.get("winner_competitor_id") or "(none)"
        print(f"  {r.get('tournament_id')}: {r.get('status')}  winner={winner}"
              f"  confidence={r.get('confidence')}  (created={r.get('created_at', '')})")
<<<END PAIR_P1_FROM>>>
TO:
<<<BEGIN PAIR_P1_TO>>>
def _cmd_tournament_list(args: Any) -> None:
    from packages.orchestration.list_options import ListOptionError, apply_list_options
    from packages.orchestration.model_route_tournament import list_tournament_reports
    reps = list_tournament_reports(job_id=str(args.job_id))
    try:
        reps = apply_list_options(
            reps,
            sort=getattr(args, "sort", None), desc=getattr(args, "desc", False),
            since=getattr(args, "since", None), until=getattr(args, "until", None),
            limit=getattr(args, "limit", None),
            sort_fields={
                "created_at": lambda r: r.get("created_at", ""),
                "status": lambda r: r.get("status", ""),
                "confidence": lambda r: r.get("confidence", ""),
            },
            default_sort_field="created_at",
            date_getter=lambda r: r.get("created_at") or None,
        )
    except ListOptionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    out = {"job_id": str(args.job_id), "report_count": len(reps),
           "reports": [{"tournament_id": r.get("tournament_id"), "status": r.get("status"),
                        "winner_competitor_id": r.get("winner_competitor_id", ""),
                        "confidence": r.get("confidence"),
                        "created_at": r.get("created_at", "")} for r in reps]}
    if getattr(args, "json", False):
        print(json.dumps(out, indent=2))
        return
    print(f"Tournament reports for {str(args.job_id)[:8]}: {len(reps)}")
    for r in reps:
        winner = r.get("winner_competitor_id") or "(none)"
        print(f"  {r.get('tournament_id')}: {r.get('status')}  winner={winner}"
              f"  confidence={r.get('confidence')}  (created={r.get('created_at', '')})")
<<<END PAIR_P1_TO>>>
Verify FROM occurs exactly once in the file before applying. `sys` is already imported at module scope in this file — do not re-import it. Do NOT touch `_cmd_tournament_report`, `_cmd_tournament_show`, or `_cmd_tournament_integrity` — none of those are part of this round's change set.

TEST T1 (APPEND) — `tests/cli/test_tournament_cli.py`. Insert at the TRUE END of the file, immediately after `test_list_text_shows_per_row` (the file's last function).
FROM (exact, the file's own last function, verify nothing follows it):
<<<BEGIN T1_FROM>>>
def test_list_text_shows_per_row(env):
    r = run_grouped_cli(["tournament", "report", "job-7", "--json"], env)
    tid = json.loads(r.stdout)["tournament_id"]
    r2 = run_grouped_cli(["tournament", "list", "job-7"], env)
    assert r2.returncode == 0
    assert tid in r2.stdout
    assert "created=" in r2.stdout
<<<END T1_FROM>>>
TO:
<<<BEGIN T1_TO>>>
def test_list_text_shows_per_row(env):
    r = run_grouped_cli(["tournament", "report", "job-7", "--json"], env)
    tid = json.loads(r.stdout)["tournament_id"]
    r2 = run_grouped_cli(["tournament", "list", "job-7"], env)
    assert r2.returncode == 0
    assert tid in r2.stdout
    assert "created=" in r2.stdout


def test_limit_caps_the_report_count(env):
    run_grouped_cli(["tournament", "report", "job-8", "--json"], env)
    run_grouped_cli(["tournament", "report", "job-8", "--json"], env)
    run_grouped_cli(["tournament", "report", "job-8", "--json"], env)
    r = run_grouped_cli(["tournament", "list", "job-8", "--json", "--limit", "2"], env)
    d = json.loads(r.stdout)
    assert d["report_count"] == 2


def test_unknown_sort_field_exits_nonzero(env):
    run_grouped_cli(["tournament", "report", "job-9", "--json"], env)
    r = run_grouped_cli(["tournament", "list", "job-9", "--sort", "bogus"], env)
    assert r.returncode == 1
    assert "created_at" in r.stderr
<<<END T1_TO>>>
Verify FROM occurs exactly once in the file before applying — it is the file's own last function. `run_grouped_cli` and `json` are already imported at module scope in this file — do not re-import them.

Apply PAIR P1 and TEST T1. Two files (1 production: `apps/cli/commands/tournament_cmd.py`; 1 test: `tests/cli/test_tournament_cli.py`) in ONE commit.

Run `python3 -m py_compile apps/cli/commands/tournament_cmd.py tests/cli/test_tournament_cli.py` and confirm exit 0. Then run `python3 -m pytest tests/cli/test_tournament_cli.py -q` and record the exact pass count verbatim — expected 10 (8 pre-existing + 2 new). Commit message: `F262 R15 C2: T003 batch 3 - tournament.list wiring`

──────────────────────────────────────────────────────────
C3 — replace .agent/plan.md with PLAN16
──────────────────────────────────────────────────────────
Replace the ENTIRE content of `.agent/plan.md` with exactly the text between the PLAN16 markers below (whole-file replace, byte-exact — verify with an actual byte-for-byte binary comparison, not `wc -l`/diffstat):

<<<BEGIN PLAN16>>>
# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 15, session 5 - T003 batch 3: `tournament.list` wired to
`apply_list_options` with `default_sort_field="created_at"` -
`list_tournament_reports()`'s own order was `sorted(root.iterdir())`
(an arbitrary on-disk directory-name order, not a meaningful one like
queue.list's priority), so forcing newest-first is the correct,
unconditional choice here, no D2-style opt-out needed. Single pair -
`tournament.list`'s dispatch is a direct handler reference, not a
lambda, so no separate dispatch-site edit was needed.

## Next Steps

- T003 batch 4+: wire the remaining commands - project.list, blocker.list,
  decision.list, review.list, propose.list, external-builder.submission-list
  are all shaped like tournament.list (plain dict rows, single collection
  feeding both --json and text). patch.list (approval_queue.py's
  format_intent_list table renderer) and loop.list (JSON/text rows built
  from two different collections) still need their own look before wiring.
  config.list/worker.list/execution.list stay excused per Risks.
  Re-check EACH remaining command's OWN tests for an order-asserting test
  FIRST, per DECISION F262 D2's precedent, before assuming date-descending
  is safe to force.
- change.list's event-log CREATED date stays open, UNRELATED to D1:
  do_run.py's event stays dead, job.py's real event carries no
  intent_id to join on - see DECISION F262 D1's Alternative section.
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
<<<END PLAN16>>>

Commit message: `F262 R15 C3: replace plan.md with PLAN16`

──────────────────────────────────────────────────────────
C4 — handback
──────────────────────────────────────────────────────────
Rewrite `.agent/handoff.md` (whole-file, per AGENTS.md's handback contract) with: Session (SESSION 5 of feature F262, round 15, rounds so far 15), a Range section stating this handback covers `60fe2ed1..<C3 sha>` (C4/this handback commit is NOT part of the reviewed content range), an Item Status table (Preconditions, C0a, C0b, C1, C2, C3, C4, plus one row per gate you ran), a Commits table with every file changed per commit and its +/- line counts from `git show --numstat`, a Verification section with the REAL output of every command you ran (py_compile exit codes, the exact pytest pass count for C2's run, the canary suite run as ONE combined invocation: `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q`, expected 646 passed), a Deviations & assumptions section (state honestly anything that didn't go exactly as ordered, including the plan.md byte-equality check result), and a Next section. This is SESSION 5's fifth round (the upper end of the self-drive protocol's default four-to-five-round session target) — state plainly in the Next section that session 5 has reached its default round target and the next session should open fresh per the protocol's own judgment, naming round 16's likely focus (T003 batch 4 against PLAN16's ordered list) as what that next session should pick up, WITHOUT starting it. Follow the exact structure of the R14 handback (commit 60fe2ed1, already on disk — read it for the template).

After committing C4, run `git push -u origin feature/f262-list-commands-v2` and report the push result in your closing message.

Do NOT run any `gh pr` command. Do NOT merge anything. Do NOT touch `main`. This round ships no PR — the branch stays open for round 16.

═══════════════════════════════════════════════════════════════
CONSTRAINTS
═══════════════════════════════════════════════════════════════
1. Every FROM string in P1 and T1 must be verified to occur exactly once in its target file, using the file's CURRENT content on disk (re-read each file yourself before applying, do not trust cited context blindly). If a FROM does not match, STOP that pair, do not guess a fix, report the exact mismatch in Deviations instead.
2. Do not touch any file not named in this block. Do NOT wire any list command other than `tournament.list` this round.
3. Do not run `ruff` if it requires approval you don't have — note the refusal in Deviations if so, not a blocker.
4. If `.agent/STOP` appears at any point mid-round, finish the commit you are mid-way through (if any), then stop and hand off.
5. Keep C2 as ONE commit covering exactly the two named files.
6. Report every command's REAL exit code and REAL output. Never write "green"/"passed" without the actual number.
7. The C3 plan.md gate MUST be an actual byte-for-byte comparison (read both files in binary mode and compare with `==`), not a line-count or diffstat proxy.

END OF BLOCK
