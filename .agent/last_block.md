── STEP T004 slice 2/2 — F105 R46 ────────────────────────────
Goal:        Give `remedy stats cache` the `--json` mode R45 deliberately left
             out, so the machine-readable document carries the same share, the
             same two absence words and the same per-role limit as the table.
Bundle:      C1a save block · C1b mirror · C2 the R45 gate, the R-0267
             resolution and the R46 step line · C3 the payload and the command ·
             C4 the catalog flag and its --json arg · C5 the tests ·
             C6 plan + SESSION-CLOSE handoff.
Change:      .agent/authored/f105-r46-1.md (new), .agent/last_block.md,
             .agent/live_review.md, apps/cli/commands/stats_ledger_cmd.py,
             apps/cli/command_catalog.py, tests/cli/test_stats_cost.py,
             .agent/plan.md, .agent/handoff.md. NOTHING else.
Constraints: AGENTS.md in full: self-review before every commit, one logical
             step per commit, plan.md current, clean tree, push at the end.
             Never `main`, never force-push, no PR, no merge. The human table
             must not change one byte — the R45 tests are the proof of that.
Done when:   every gate records a REAL exit code and the diff touches exactly
             the eight paths named above.
Handback:    completion report + rewrite .agent/handoff.md as a SESSION CLOSE
──────────────────────────────────────────────────────────────

C1a — write this ENTIRE block to `.agent/authored/f105-r46-1.md` byte for
  byte, commit it ALONE.
C1b — `cp` it over `.agent/last_block.md`, never retype, commit alone, then
  `cmp` the two: silent.

C2 — .agent/live_review.md. PAIR_LR is CONTAINS-FROM. The next free finding ID
  stays R-0268: this round registers nothing new.

<<<PAIR_LR_FROM>>>
  R-0267 with the error-path test the shared branch never had.
<<<END_PAIR_LR_FROM>>>

<<<PAIR_LR_TO>>>
  R-0267 with the error-path test the shared branch never had.
  Done: R-0267 — closed at R45 by the new
  `TestStatsCacheView::test_an_unreadable_ledger_exits_instead_of_reporting_zero`,
  which corrupts the ledger file on disk and asserts BOTH the exit code and the
  message on stderr, so the branch cannot regress into a confident zero without
  a red test. The reviewer re-ran the suite (39 passed) and read the test
  against the branch it covers rather than accepting the handback. RESOLVED.
- Reviewer gate on R45 (2026-08-10): PASS. Range `ae1756f8..c7510403` = eight
  commits, exactly the nine paths the block named. Insertions per commit 399,
  363, 47, 17, 109, 22, 54 and 98, each far under 500.
  Transport by the PRIMARY shape: `.remedy-wt/f105-r45-1.block.md`, the
  committed `.agent/authored/f105-r45-1.md` and `.agent/last_block.md` all
  three hash to
  `87f65221d35d613fdb70265fd670060ccc174c77c84fa4640eefa288a6058ad8`
  at 399 lines; both `cmp` runs silent.
  Stray reconcile over all FIVE authored commits: 47/0, 17/0, 109/0, 22/0 and
  54/0 added/stray — zero strays anywhere, and the single removal is the
  PAIR_ID FROM line its own REWRITE replaces.
  Gates re-run by THIS reviewer, none taken from the handback:
  `tests/cli/test_stats_cost.py` `39 passed in 0.39s` (33 + the 6 new); the
  catalog and spine suites `113 passed in 0.57s`; the canary
  `42 passed in 19.81s`; `py_compile` exit 0 on both production files;
  `.agent/plan.md` 45 lines with both mandated headings; `.agent/live_review.md`
  exactly one `## Steps` heading; the ID line reads R-0268; `^<<<` 0 in all
  seven touched files; `git status --porcelain` empty, primary worktree alone.
  The view was not accepted on its tests' word: the reviewer called
  `_render_cache_human` directly on a synthetic three-bucket report and read
  the output. A measured bucket printed `6.0%`, an unreported bucket printed
  `unmeasured` in all three figure columns, a bucket whose inputs were reported
  as zero printed `undefined`, and the role split printed the R-0266 limit
  line. The two words of DECISION D15 are therefore distinguishable in the
  rendered bytes, which is the only place the distinction matters.
  One reviewer-side lesson, not a finding, because the worker did nothing
  wrong: the block measured 399 lines against a cap of 400. One line is not a
  margin. Block budgets get counted before the prose is written, not after.
  `LAST_REVIEWED_SHA` advances ae1756f8 -> c7510403.
- R46: SPLIT round — add the `--json` mode for `stats cache`, so the machine
  document carries the same share, the same two absence words and the same
  per-role limit the table already states. Closes the flag R45 deliberately
  withheld rather than shipping one that did nothing. LAST round of the
  session; the branch continues.
<<<END_PAIR_LR_TO>>>

C3 — apps/cli/commands/stats_ledger_cmd.py. Three pairs, ONE commit.
  PAIR_PAYLOAD is CONTAINS-FROM, PAIR_CMD is a REWRITE, PAIR_H is
  CONTAINS-FROM.

<<<PAIR_PAYLOAD_FROM>>>
def _share_text(share) -> str:
    """One share as a table cell: a percentage, or the word standing in for it."""
    return share if isinstance(share, str) else f"{share * 100:.1f}%"
<<<END_PAIR_PAYLOAD_FROM>>>

<<<PAIR_PAYLOAD_TO>>>
def _share_text(share) -> str:
    """One share as a table cell: a percentage, or the word standing in for it."""
    return share if isinstance(share, str) else f"{share * 100:.1f}%"


def _cache_row_payload(row) -> dict:
    """One cache row as JSON: the share is a number, or null carrying its reason.

    A consumer that only reads ``cache_read_share`` sees ``null`` and knows the
    figure is absent; one that needs to know WHY reads ``share_basis``, which
    carries the same word the table prints. The two absences never collapse
    into one, and neither ever becomes a 0.
    """
    share = _cache_read_share(row)
    return {
        "bucket": row.bucket,
        "calls": row.calls,
        "tokens_in": row.tokens_in,
        "cache_read": row.cache_read,
        "cache_read_share": None if isinstance(share, str) else round(share, 6),
        "share_basis": share if isinstance(share, str) else "measured",
        "measured_calls": row.measured_calls,
        "unmeasured_calls": row.unmeasured_calls,
        "basis": _row_basis(row),
    }


def _cache_payload(report, *, ledgers_read: list[str], scope_label: str) -> dict:
    """The `--json` document for the cache view, carrying its own limits."""
    return {
        "version": COST_OUTPUT_VERSION,
        "scope": scope_label,
        "ledgers_read": ledgers_read,
        "filters": {"since": report.since or "", "job": report.job_id or "",
                    "by": report.by},
        "share_formula": "cache_read / (tokens_in + cache_read)",
        "note": ("a null share was never measurable and is not a zero share; "
                 "share_basis names which of the two reasons applies"),
        "role_limit": _ROLE_LIMIT_NOTE,
        "total": _cache_row_payload(report.total),
        "rows": [_cache_row_payload(row) for row in report.rows],
    }
<<<END_PAIR_PAYLOAD_TO>>>

<<<PAIR_CMD_FROM>>>
def _cmd_stats_cache(*, since: str = "", job: str = "", by: str | None = None,
                     project: str | None = None,
                     all_projects: bool = False) -> None:
    report, ledgers_read, scope_label = _load_ledger_reports(
        since=since, job=job, by=by, project=project,
        all_projects=all_projects, json_output=False)
    print(_render_cache_human(
        report, ledgers_read=ledgers_read, scope_label=scope_label))
<<<END_PAIR_CMD_FROM>>>

<<<PAIR_CMD_TO>>>
def _cmd_stats_cache(*, since: str = "", job: str = "", by: str | None = None,
                     project: str | None = None,
                     all_projects: bool = False,
                     json_output: bool = False) -> None:
    report, ledgers_read, scope_label = _load_ledger_reports(
        since=since, job=job, by=by, project=project,
        all_projects=all_projects, json_output=json_output)
    if json_output:
        print(_json.dumps(_cache_payload(
            report, ledgers_read=ledgers_read, scope_label=scope_label), indent=2))
    else:
        print(_render_cache_human(
            report, ledgers_read=ledgers_read, scope_label=scope_label))
<<<END_PAIR_CMD_TO>>>

<<<PAIR_H_FROM>>>
        all_projects=getattr(args, "all_projects", False),
    ),
    "stats.backfill-ledger": lambda args: _cmd_stats_backfill_ledger(
<<<END_PAIR_H_FROM>>>

<<<PAIR_H_TO>>>
        all_projects=getattr(args, "all_projects", False),
        json_output=getattr(args, "json", False),
    ),
    "stats.backfill-ledger": lambda args: _cmd_stats_backfill_ledger(
<<<END_PAIR_H_TO>>>

C4 — apps/cli/command_catalog.py. Two pairs, ONE commit. PAIR_FLAG is a
  REWRITE; PAIR_ARG is CONTAINS-FROM.

<<<PAIR_FLAG_FROM>>>
        action_class="read_only",
        supports_json=False,
        related=("stats.cost", "stats.backfill-ledger"),
<<<END_PAIR_FLAG_FROM>>>

<<<PAIR_FLAG_TO>>>
        action_class="read_only",
        supports_json=True,
        related=("stats.cost", "stats.backfill-ledger"),
<<<END_PAIR_FLAG_TO>>>

<<<PAIR_ARG_FROM>>>
            _PROJECT_SCOPE_OPT,
            _ALL_PROJECTS_FLAG,
        ),
        may_mutate_repo=False,
        may_execute_commands=False,
    ),
    CommandEntry(
        command_id="stats.backfill-ledger",
<<<END_PAIR_ARG_FROM>>>

<<<PAIR_ARG_TO>>>
            _PROJECT_SCOPE_OPT,
            _ALL_PROJECTS_FLAG,
            _JSON_OPT,
        ),
        may_mutate_repo=False,
        may_execute_commands=False,
    ),
    CommandEntry(
        command_id="stats.backfill-ledger",
<<<END_PAIR_ARG_TO>>>

C5 — tests/cli/test_stats_cost.py. PAIR_TEST is CONTAINS-FROM, appended to the
  END of the TestStatsCacheView class.

<<<PAIR_TEST_FROM>>>
        assert exc.value.code == CMD.EXIT_ERROR
        assert "cannot read the token ledger" in capsys.readouterr().err
<<<END_PAIR_TEST_FROM>>>

<<<PAIR_TEST_TO>>>
        assert exc.value.code == CMD.EXIT_ERROR
        assert "cannot read the token ledger" in capsys.readouterr().err

    def test_the_json_share_carries_its_reason_and_never_a_zero(
        self, filled_ledger, project_id, capsys
    ):
        CMD._cmd_stats_cache(project=project_id, by="role", json_output=True)
        rows = {row["bucket"]: row
                for row in json.loads(capsys.readouterr().out)["rows"]}

        assert rows["builder"]["cache_read_share"] == pytest.approx(0.0601, abs=1e-4)
        assert rows["builder"]["share_basis"] == "measured"
        assert rows["reviewer"]["cache_read_share"] is None
        assert rows["reviewer"]["share_basis"] == "unmeasured"

    def test_the_json_document_states_the_role_limit(self, filled_ledger,
                                                     project_id, capsys):
        CMD._cmd_stats_cache(project=project_id, json_output=True)
        payload = json.loads(capsys.readouterr().out)

        assert "hardcoded role" in payload["role_limit"]
        assert payload["share_formula"] == "cache_read / (tokens_in + cache_read)"
<<<END_PAIR_TEST_TO>>>

C6 — plan and SESSION-CLOSE handoff
  Rewrite `.agent/plan.md`: UNDER 50 lines, a `## Goal` heading and a
  `## Next Steps` heading, the session recorded as CLOSED at R46 and NOT
  against a `.agent/STOP` file, `LAST_REVIEWED_SHA` c7510403, the open
  findings, and the three things left in this feature as the next steps —
  (1) the T004 before/after comparison note in the feature's evidence with
  honest numbers whatever they are, (2) the integration gate per
  docs/agents/integration_gate.md, (3) closure per
  docs/roadmap/STATUS_closure_protocol.md.
  Then rewrite `.agent/handoff.md` as a SESSION CLOSE: feature and round,
  branch, commit SHAs, changed-files table, item-status table, every gate with
  its REAL exit code, open-findings count, next expected action. Under 60
  lines, or over it with a DECISION D15 "Deviations, declared" line naming the
  count and its mandated causes.
  The handoff MUST state, in its own section, that `.agent/live_review.md`
  carries the R46 step line but NO R46 gate record, deliberately: R46 ends a
  SESSION and not the BRANCH, so planner_reviewer_prompt.md §4.13's terminator
  does NOT apply — that is the R-0264 distinction — and the NEXT session gates
  R46 as an ordinary handback from base c7510403. It must also state that
  PR #189 (`docs/amend0810-clerical` -> `main`) was left untouched because it
  does not originate from a `feature/*` branch, which makes the Open PR Gate
  stop-and-report, and that it must be resolved by the operator before F105's
  closure PR is cut.
  Commit C6, push the branch, create NO pull request.

Gates — run every one, record its REAL exit code, never the word "green"
  A  sha256sum + cmp across block file, authored file and last_block: all three
     equal, both `cmp` silent.  B  wc -l the authored file against cap 400.
  C  Pair shapes MEASURED: PAIR_CMD and PAIR_FLAG are REWRITEs (FROM 1x before,
     0x after; TO 1x after). PAIR_LR, PAIR_PAYLOAD, PAIR_H, PAIR_ARG and
     PAIR_TEST are CONTAINS-FROM (FROM 1x before and 1x after; TO 1x after).
  D  Stray reconcile for C2, C3, C4 and C5: `git show -U0 <sha> -- <path>`,
     then check every ADDED line appears in the authored file. Report added,
     removed and stray counts for each.
  E  grep -c '^<<<' over all six touched text files — every count 0.
  F  python3 -m pytest tests/cli/test_stats_cost.py -q — expect the 39 from R45
     plus the 2 new. Report the total.
  G  python3 -m pytest tests/test_command_catalog.py tests/cli/test_command_catalog.py tests/cli/test_product_spine.py -q
  H  Canary: python3 -m pytest tests/cli/test_golden_path.py -q
  I  python3 -m py_compile on both changed production files.
  J  The human table did not move: confirm the four R45 rendering tests still
     pass by name in gate F's run, and say so with their names.
  K  git status --porcelain EMPTY; git worktree list shows the primary ALONE;
     insertions per commit under 500; git diff --name-only c7510403..HEAD is
     exactly the eight paths named above.

If gate F or G comes back RED, do NOT improvise a fix that leaves this change
set. Report the exact failure output and stop: a mistake in an authored slice
is mine to repair, and a round that halts honestly costs less than one that
invents its way past a red gate.

Do not: touch `main`, force-push, create `.agent/STOP`, merge anything, create
a PR, widen the change set, or fix R-0221, R-0239, R-0247, R-0262, R-0265 or
R-0266 — all six stay OPEN by design. Write no `Done:` paragraph of your own:
only reviewer-authored text sets a resolution (planner_reviewer_prompt.md §4.4).
