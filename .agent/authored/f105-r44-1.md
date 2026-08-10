── STEP T004 slice 0/2 — F105 R44 ────────────────────────────
Goal:        Persist the R43 gate, then extract the ledger-reading half of
             `stats cost` into one helper, with no behaviour change, so the
             cache view in R45 reads through that helper instead of a copy.
Bundle:      C1a save this block verbatim · C1b mirror it into last_block ·
             C2 the R43 gate record and the R44 step line · C3 the extraction
             (production code, own commit) · C4 plan + handoff.
Change:      .agent/authored/f105-r44-1.md (new), .agent/last_block.md,
             .agent/live_review.md, apps/cli/commands/stats_ledger_cmd.py,
             .agent/plan.md, .agent/handoff.md. NOTHING else — no catalog
             entry, no new command, no new test module, no docs/ this round.
Constraints: AGENTS.md in full: self-review before every commit, one logical
             step per commit, plan.md current, clean tree, push at the end.
             Never `main`, never force-push, no PR this round. Do not touch
             packages/orchestration/**, tests/**, docs/**. The extraction must
             not change one byte of what `stats cost` prints — the existing
             suite is the proof of that, not your reading of the diff.
             Apply every pair below BYTE FOR BYTE. If a FROM is not found
             exactly once, STOP and report; do not retype it from memory.
Done when:   every gate below records a REAL exit code, and the diff touches
             exactly the six paths named above.
Handback:    completion report + rewrite .agent/handoff.md
──────────────────────────────────────────────────────────────

C1a — save this block verbatim
  Write this ENTIRE block, from the STEP header line to the last line of this
  block, to `.agent/authored/f105-r44-1.md` byte for byte. Commit it ALONE.

C1b — mirror
  `cp` that exact file over `.agent/last_block.md` — never retype it — and
  commit it alone. `cmp` the two afterwards: silent.

C2 — the R43 gate record and the R44 step line (.agent/live_review.md)
  PAIR_LR is CONTAINS-FROM: the TO repeats the FROM verbatim and adds lines
  after it. The FROM must be found exactly 1x before the write.

<<<PAIR_LR_FROM>>>
  T004 unstarted but fully scoped; the next session opens with T004 slice 1.
<<<END_PAIR_LR_FROM>>>

<<<PAIR_LR_TO>>>
  T004 unstarted but fully scoped; the next session opens with T004 slice 1.
- Reviewer gate on R43 (2026-08-10, by the session that resumed the branch):
  PASS. Range `1fc4c62c..b0b2d12f` = five commits, six paths, every one under
  `.agent/`; nothing under `packages/`, `apps/`, `tests/` or `docs/`.
  Insertions per commit 297, 208, 64, 44 and 94, each far under 500.
  Transport by the PRIMARY shape: `.remedy-wt/f105-r43-1.block.md`, the
  committed `.agent/authored/f105-r43-1.md` and `.agent/last_block.md` all
  three hash to
  `2c19254ead411e32b8247e54d7917aa1f411b63d2838b95f52e8f820881f71ad`
  at 297 lines against D5's cap of 400; both `cmp` runs silent.
  Reconciled by machine rather than by eye: every line C2 and C3 ADD appears
  in the committed authored file — 64 added and 44 added, 0 strays each — and
  of C4's 94 added lines the 14 in `.agent/plan.md` are 0-stray while the 80
  in `.agent/handoff.md` are worker-authored by design. `cmp` of the applied
  `.agent/plan.md` against the PAIR_P_PLAN slice is silent at 42 lines.
  Gates re-run by THIS reviewer, none taken from the handback: `tests/docs/`
  `294 passed in 0.26s`; `test_dashboard_contract.py` `70 passed in 3.96s`;
  the canary `42 passed in 19.85s`; `^<<<` 0 in all four touched text files;
  `.agent/plan.md` 42 lines against the cap of 50 and keeping `## Goal` and a
  `Steps` substring; `.agent/live_review.md` exactly one `## Steps` heading;
  `git status --porcelain` empty and the primary worktree alone.
  Spot-checks of the REVIEWER's choosing, not ordered by the block: the three
  source pointers under R-0265 and R-0266 were opened independently —
  `token_actuals.py:110` is the `or 0` collapse, `pingpong_loop.py:3970` is
  the hardcoded builder role constant, and `token_ledger.py:1017` is the
  `role=_first_string(accounting, ("role",))` line. All three read as
  registered, so neither finding rests on the inventory's word.
  Gate J, the deliberately absent R43 gate record, was the correct call and is
  closed by this entry: R43 ended a SESSION and not the BRANCH, so §4.13's
  terminator never applied and the round stayed gateable — the R-0264 reading,
  applied correctly for the first time by the round that produced it.
  The declared handoff overage (120 lines, DECISION D15 line present) is
  ACCEPTED: the mandated tables account for it and no section was dropped.
  `LAST_REVIEWED_SHA` advances 1fc4c62c -> b0b2d12f.
- R44: SPLIT round — persist the R43 gate and extract the ledger-reading half
  of `stats cost` into `_load_ledger_reports`, with no behaviour change, so a
  second view has one code path to read the ledger through rather than a copy
  of one. Production code, so the round is SPLIT by §3.
<<<END_PAIR_LR_TO>>>

C3 — extract the ledger read (apps/cli/commands/stats_ledger_cmd.py)
  PAIR_COST is a REWRITE: after the write its FROM is found 0x and its TO 1x.
  Count the FROM as the WHOLE contiguous text, never by its first line — the
  `def _cmd_stats_cost` signature legitimately survives inside the TO.

<<<PAIR_COST_FROM>>>
def _cmd_stats_cost(*, since: str = "", job: str = "", by: str | None = None,
                    project: str | None = None,
                    all_projects: bool = False,
                    json_output: bool = False) -> None:
    import sqlite3

    from apps.cli.commands.failure_stats_cmd import _validate_since
    from packages.orchestration.token_ledger import merge_cost_reports, query_cost

    # One spelling of "what is a valid --since", shared with `stats failures`.
    since = _validate_since(since)
    by = _validate_by(by)
    ledgers, scope_label = _ledger_paths_for_scope(project, all_projects)

    try:
        reports = [
            query_cost(path=path, since=since or None, job_id=job or None, by=by)
            for path in ledgers
        ]
    except sqlite3.Error as exc:
        # An unreadable ledger is not "zero cost". Saying so would be the exact
        # lie the basis labeling exists to prevent.
        if json_output:
            print(_json.dumps({"ok": False, "error": str(exc)}, indent=2))
        else:
            print(f"Error: cannot read the token ledger: {exc}", file=sys.stderr)
        raise SystemExit(EXIT_ERROR) from None

    report = reports[0] if len(reports) == 1 else merge_cost_reports(reports)
    # What was actually READ, not what was looked for: a project whose ledger does
    # not exist yet contributes no file and no figure.
    ledgers_read = [r.ledger_path for r in reports if r.ledger_exists and r.ledger_path]
    if json_output:
        print(_json.dumps(_cost_payload(
            report, ledgers_read=ledgers_read, scope_label=scope_label), indent=2))
    else:
        print(_render_cost_human(
            report, ledgers_read=ledgers_read, scope_label=scope_label))
<<<END_PAIR_COST_FROM>>>

<<<PAIR_COST_TO>>>
# Every read a ledger VIEW needs, in one place, so renderers stay renderers.
def _load_ledger_reports(*, since: str, job: str, by: str | None,
                         project: str | None, all_projects: bool,
                         json_output: bool):
    """Validate the filters, query every ledger in scope, and merge the answers.

    Views over this ledger ask it the SAME question and differ only in what they
    render from the answer, so the reading lives here once. Returns the merged
    report, the ledger paths actually READ, and the scope label, in that order.

    An unreadable ledger EXITS here instead of returning an empty report: a
    database error does not mean zero, and rendering it as zero would be the
    exact lie the basis labeling exists to prevent.
    """
    import sqlite3

    from apps.cli.commands.failure_stats_cmd import _validate_since
    from packages.orchestration.token_ledger import merge_cost_reports, query_cost

    # One spelling of "what is a valid --since", shared with `stats failures`.
    since = _validate_since(since)
    by = _validate_by(by)
    ledgers, scope_label = _ledger_paths_for_scope(project, all_projects)

    try:
        reports = [
            query_cost(path=path, since=since or None, job_id=job or None, by=by)
            for path in ledgers
        ]
    except sqlite3.Error as exc:
        if json_output:
            print(_json.dumps({"ok": False, "error": str(exc)}, indent=2))
        else:
            print(f"Error: cannot read the token ledger: {exc}", file=sys.stderr)
        raise SystemExit(EXIT_ERROR) from None

    report = reports[0] if len(reports) == 1 else merge_cost_reports(reports)
    # What was actually READ, not what was looked for: a project whose ledger does
    # not exist yet contributes no file and no figure.
    ledgers_read = [r.ledger_path for r in reports if r.ledger_exists and r.ledger_path]
    return report, ledgers_read, scope_label


def _cmd_stats_cost(*, since: str = "", job: str = "", by: str | None = None,
                    project: str | None = None,
                    all_projects: bool = False,
                    json_output: bool = False) -> None:
    report, ledgers_read, scope_label = _load_ledger_reports(
        since=since, job=job, by=by, project=project,
        all_projects=all_projects, json_output=json_output)
    if json_output:
        print(_json.dumps(_cost_payload(
            report, ledgers_read=ledgers_read, scope_label=scope_label), indent=2))
    else:
        print(_render_cost_human(
            report, ledgers_read=ledgers_read, scope_label=scope_label))
<<<END_PAIR_COST_TO>>>

C4 — plan and handoff
  Rewrite `.agent/plan.md` yourself to the post-round state: UNDER 50 lines,
  keeping a `## Goal` heading and a `## Next Steps` heading, naming R44 as
  gated-pending, the six open findings, and R45 — the `stats cache` command,
  its catalog entry and its test module — as the next step. This file is NOT
  reviewer-authored this round; the block budget went to the pairs. Write it
  against the current disk state, which AGENTS.md requires it to reflect.
  Then rewrite `.agent/handoff.md`: feature and round, branch, commit SHAs,
  changed-files table, item-status table, every gate below with its REAL exit
  code, open-findings count, next expected action. Under 60 lines, or over it
  with a DECISION D15 "Deviations, declared" line naming the actual count and
  the mandated content that caused it.
  Commit C4, then push the branch. Create NO pull request.

Gates — run every one, record its REAL exit code, never the word "green"
  A  sha256sum + cmp across the block file, `.agent/authored/f105-r44-1.md`
     and `.agent/last_block.md`: all three equal, both `cmp` runs silent.
  B  wc -l `.agent/authored/f105-r44-1.md`, reported against D5's cap of 400.
  C  Pair shapes MEASURED, not asserted: PAIR_LR FROM 1x before and 1x after,
     its TO 1x after; PAIR_COST FROM 1x before and 0x after, its TO 1x after.
  D  Stray reconcile for C2 and C3 — `git show -U0 <sha> -- <path>`, then
     check that every ADDED line appears in `.agent/authored/f105-r44-1.md`.
     Report both added counts and both stray counts.
  E  grep -c '^<<<' over live_review.md, plan.md, handoff.md and
     stats_ledger_cmd.py — all four 0. `grep -c` exits 1 when the pattern is
     absent, and that is the PASS condition here; record the counts.
  F  python3 -m pytest tests/cli/test_stats_cost.py -q — the extraction's own
     gate: this suite drives `stats cost` end to end, so it is what proves the
     behaviour did not move.
  G  python3 -m pytest tests/test_command_catalog.py tests/cli/test_command_catalog.py -q
  H  Canary: python3 -m pytest tests/cli/test_golden_path.py -q
  I  PROBE, not a colour, and ONLY inside a DISPOSABLE `git worktree` at HEAD,
     never the primary checkout: replace the body of `_load_ledger_reports`
     with `raise RuntimeError("probe")` and run tests/cli/test_stats_cost.py.
     REPORT HOW MANY TESTS FAIL. Do not assert a colour — if the number is 0
     the extraction is unreached, which is a finding about the code and not a
     failure of yours. Remove the worktree and `git worktree prune` before the
     handback, so the primary checkout is alone again at verdict time.
  J  git status --porcelain EMPTY; git worktree list shows the primary ALONE;
     insertions per commit from `git show --numstat`, each under 500.
  K  git diff --name-only b0b2d12f..HEAD — exactly the six paths named above.

Do not: touch `main`, force-push, create `.agent/STOP`, merge anything, widen
the change set, or fix R-0221, R-0239, R-0247, R-0262, R-0265 or R-0266 — all
six stay OPEN by design. Write no `Done:` paragraph of your own: a landed but
ungated fix is marked `Landed: R-XXXX` and nothing else, because only
reviewer-authored text sets a resolution (planner_reviewer_prompt.md §4.4).
