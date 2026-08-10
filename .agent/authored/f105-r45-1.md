── STEP T004 slice 1/2 — F105 R45 ────────────────────────────
Goal:        Add `remedy stats cache`: the cache-read share per bucket over the
             ledger rows that already exist, with `unmeasured` never rendered
             as a zero, and with the per-role limit named in the output.
Bundle:      C1a save block · C1b mirror · C2 R44 gate + R-0267 + R45 step ·
             C3 DECISION F105 D15 · C4 the view and its handler · C5 the
             catalog entry · C6 the tests · C7 plan + handoff.
Change:      .agent/authored/f105-r45-1.md (new), .agent/last_block.md,
             .agent/live_review.md, .agent/decisions.md,
             apps/cli/commands/stats_ledger_cmd.py, apps/cli/command_catalog.py,
             tests/cli/test_stats_cost.py, .agent/plan.md, .agent/handoff.md.
             NOTHING else. No new test module, no docs/, no packages/.
Constraints: AGENTS.md in full: self-review before every commit, one logical
             step per commit, plan.md current, clean tree, push at the end.
             Never `main`, never force-push, no PR. `--json` is deliberately
             NOT part of this round: the command ships human-rendered only and
             the catalog entry therefore declares supports_json=False and
             offers no --json arg, so no flag ever exists that does nothing.
Done when:   every gate records a REAL exit code and the diff touches exactly
             the nine paths named above.
Handback:    completion report + rewrite .agent/handoff.md
──────────────────────────────────────────────────────────────

C1a — write this ENTIRE block to `.agent/authored/f105-r45-1.md` byte for
  byte and commit it ALONE.
C1b — `cp` that file over `.agent/last_block.md`, never retype, commit alone,
  then `cmp` the two: silent.

C2 — .agent/live_review.md. PAIR_ID is a REWRITE (FROM 0x after, TO 1x after).
  PAIR_LR is CONTAINS-FROM: its TO repeats its FROM verbatim and adds after it.

<<<PAIR_ID_FROM>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0267.
<<<END_PAIR_ID_FROM>>>

<<<PAIR_ID_TO>>>
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0268.
<<<END_PAIR_ID_TO>>>

<<<PAIR_LR_FROM>>>
  of one. Production code, so the round is SPLIT by §3.
<<<END_PAIR_LR_FROM>>>

<<<PAIR_LR_TO>>>
  of one. Production code, so the round is SPLIT by §3.
- R-0267 (Low, F105 R44, pre-existing, registered AND fixed in R45): the
  `sqlite3.Error` branch that turns an unreadable ledger into a usage error
  has no test. `grep -rn 'cannot read the token ledger' tests/` returns
  nothing, so the one path that stops a database fault from being rendered as
  "zero cost" was never exercised. It is pre-existing — R44 moved it verbatim
  out of `_cmd_stats_cost` — but R44 also widened its blast radius, because
  the branch now sits in `_load_ledger_reports` and every view built on that
  helper inherits it. A silent regression there would print a confident zero
  over a corrupt file, which is the exact P6 failure the basis vocabulary
  exists to prevent. Cheap to close while a test class is being written
  anyway, so R45 closes it rather than carrying it.
- Reviewer gate on R44 (2026-08-10): PASS. Range `b0b2d12f..ae1756f8` = five
  commits, exactly the six paths the block named; one production file, nothing
  under `packages/`, `tests/` or `docs/`. Insertions per commit 233, 226, 37,
  24 and 94, each far under 500.
  Transport by the PRIMARY shape: `.remedy-wt/f105-r44-1.block.md`, the
  committed `.agent/authored/f105-r44-1.md` and `.agent/last_block.md` all
  three hash to
  `8944f6e563a74b11d104dc671b702b46ef49397f2b29227cf5fec48b6b987c24`
  at 233 lines against D5's cap of 400; both `cmp` runs silent, and the head
  and tail of the committed file are the reviewer's own emitted bytes.
  Reconciled by machine: C2 37 added / 0 stray / 0 removed; C3 24 added / 0
  stray / 6 removed, and all six removals are FROM text. `.agent/plan.md`
  carries 17 stray lines, which is NOT a finding — this block made that file
  worker-authored for the round and said so in its C4.
  Gates re-run by THIS reviewer, none taken from the handback:
  `tests/cli/test_stats_cost.py` `33 passed in 0.34s`; the two catalog suites
  `41 passed in 0.49s`; the canary `42 passed in 19.60s`; `py_compile` exit 0;
  `.agent/plan.md` 48 lines against the cap of 50 with `## Goal` and a `Steps`
  substring; `.agent/live_review.md` exactly one `## Steps` heading; `^<<<` 0
  in all four touched text files; `git status --porcelain` empty and the
  primary worktree alone.
  The C3 diff was read line by line against the authored TO and is
  byte-identical to it, including the two comment lines it deletes because the
  new docstring absorbed them. `query_cost(path=path` now appears exactly 1x
  in the module: one read path, which is what the extraction was for.
  The worker's ordered PROBE reported 19 of 33 tests failing when the helper's
  body raises — a number, not a colour, and it proves the helper is reached.
  The declared handoff overage (114 lines, DECISION D15 line present) is
  ACCEPTED. R-0267 above comes from a reviewer spot-check the block did not
  order and is the only thing this round leaves behind.
  `LAST_REVIEWED_SHA` advances b0b2d12f -> ae1756f8.
- R45: SPLIT round — add `remedy stats cache` over the helper R44 extracted,
  render the share with two distinct words for its two distinct absences
  (DECISION F105 D15), name the R-0266 per-role limit in the output, and close
  R-0267 with the error-path test the shared branch never had.
<<<END_PAIR_LR_TO>>>

C3 — .agent/decisions.md. PAIR_DEC is CONTAINS-FROM, appended at the END.

<<<PAIR_DEC_FROM>>>
producer fix, with R-0266 closed in the same round.
<<<END_PAIR_DEC_FROM>>>

<<<PAIR_DEC_TO>>>
producer fix, with R-0266 closed in the same round.

D15 — a cache-read share needs TWO words for "no number here", not one.
DECISION D14 Q5 ruled that a figure nobody reported prints the existing word
`unmeasured`, and that stands. But a SHARE has a second way to have no value:
a bucket whose inputs WERE reported and are both zero divides 0 by 0. Printing
`unmeasured` there would blame a provider for a figure it did in fact report —
the P6 lie pointing the other way — and printing `0.0%` would invent a
measurement. That case prints `undefined`, defined beside `UNMEASURED` in
`apps/cli/commands/stats_ledger_cmd.py` with the reason above it.

The alternative considered and rejected: one word for both, on the "one
spelling per concept" rule (AGENTS.md). Rejected because they are two
concepts, not one spelling of one — "nobody measured this" and "this measured
to nothing" differ exactly where a reader's next action differs.

Reverse this decision by deleting `UNDEFINED_SHARE` and returning `UNMEASURED`
for the zero-denominator case, with the test that pins the two words dropped.
<<<END_PAIR_DEC_TO>>>

C4 — apps/cli/commands/stats_ledger_cmd.py. Two CONTAINS-FROM pairs, ONE
  commit. PAIR_VIEW appends the view after `_cmd_stats_cost`; PAIR_HANDLER
  inserts the handler entry before the backfill-ledger one.

<<<PAIR_VIEW_FROM>>>
    else:
        print(_render_cost_human(
            report, ledgers_read=ledgers_read, scope_label=scope_label))
<<<END_PAIR_VIEW_FROM>>>

<<<PAIR_VIEW_TO>>>
    else:
        print(_render_cost_human(
            report, ledgers_read=ledgers_read, scope_label=scope_label))


#: What a share prints when its inputs WERE reported and are both zero. That is
#: NOT "nobody reported it": it is a real bucket that read nothing at all, and a
#: share of nothing has no value. Calling that `unmeasured` would blame a
#: provider for a figure it did report, and `0.0%` would invent a measurement.
UNDEFINED_SHARE = "undefined"

#: What a role split cannot tell a reader yet, printed in the output instead of
#: buried in a docstring. Every ledger row a live run writes carries one
#: hardcoded role, so a role split of production data has exactly one bucket;
#: further buckets come from hand-written accounting files. Remedy names the
#: limit rather than presenting one bucket as a breakdown.
_ROLE_LIMIT_NOTE = (
    "Per-role limit: every row a live run writes carries one hardcoded role "
    "today, so a role split of production data shows a single bucket. Any "
    "further bucket here came from a hand-written accounting file, not from "
    "the orchestrator."
)


def _cache_read_share(row) -> float | str:
    """The bucket's cache-read share, or the word saying why it has none.

    The share is ``cache_read / (tokens_in + cache_read)``: of everything fed
    into the model, how much came from cache. BOTH inputs must be measured — an
    unmeasured input makes the share unmeasured too, because substituting a 0
    for a figure nobody reported is the same lie one layer up.
    """
    cache_read, tokens_in = row.cache_read, row.tokens_in
    if cache_read is None or tokens_in is None:
        return UNMEASURED
    total_input = tokens_in + cache_read
    if total_input == 0:
        return UNDEFINED_SHARE
    return cache_read / total_input


def _share_text(share) -> str:
    """One share as a table cell: a percentage, or the word standing in for it."""
    return share if isinstance(share, str) else f"{share * 100:.1f}%"


def _render_cache_human(report, *, ledgers_read: list[str], scope_label: str) -> str:
    """A share table in which no missing share can be mistaken for 0 %."""
    lines = [f"Cache-read share from the token ledger — {scope_label}, "
             f"{len(ledgers_read)} ledger(s) read"]
    lines.append("Filters: " + "  ".join(f"{name}={value}" for name, value in (
        ("since", report.since or "-"),
        ("job", report.job_id or "-"),
        ("by", report.by or "-"),
    )))

    if not report.ledger_exists:
        lines.append("")
        lines.append("No ledger on disk for this scope — nothing has been recorded yet.")
        lines.append("Run 'remedy stats backfill-ledger <evidence-dir>' to mirror "
                     "existing evidence.")
        return "\n".join(lines)

    headers = ["Bucket", "Calls", "Tokens in", "Cache read", "Cache share", "Basis"]
    labelled = [(row.bucket if row.bucket is not None else "(unnamed)", row)
                for row in report.rows] + [("TOTAL", report.total)]
    body = [
        [
            label,
            str(row.calls),
            _figure(row.tokens_in),
            _figure(row.cache_read),
            _share_text(_cache_read_share(row)),
            f"{_row_basis(row)} ({row.measured_calls}/{row.calls})",
        ]
        for label, row in labelled
    ]
    widths = [max(len(headers[i]), *(len(r[i]) for r in body)) for i in range(len(headers))]
    lines.append("")
    lines.append("  ".join(h.ljust(w) for h, w in zip(headers, widths)).rstrip())
    for row in body:
        lines.append("  ".join(cell.ljust(w) for cell, w in zip(row, widths)).rstrip())

    total = report.total
    lines.append("")
    lines.append("Share = cache_read / (tokens_in + cache_read).")
    lines.append(f"'{UNMEASURED}' means nobody reported the inputs; "
                 f"'{UNDEFINED_SHARE}' means they were reported and were zero.")
    lines.append(
        f"Basis: {total.measured_calls} of {total.calls} call(s) reported usage "
        f"(provider_reported); {total.unmeasured_calls} reported none (unknown)."
    )
    if report.by == "role":
        lines.append(_ROLE_LIMIT_NOTE)
    return "\n".join(lines)


def _cmd_stats_cache(*, since: str = "", job: str = "", by: str | None = None,
                     project: str | None = None,
                     all_projects: bool = False) -> None:
    report, ledgers_read, scope_label = _load_ledger_reports(
        since=since, job=job, by=by, project=project,
        all_projects=all_projects, json_output=False)
    print(_render_cache_human(
        report, ledgers_read=ledgers_read, scope_label=scope_label))
<<<END_PAIR_VIEW_TO>>>

<<<PAIR_HANDLER_FROM>>>
    "stats.backfill-ledger": lambda args: _cmd_stats_backfill_ledger(
<<<END_PAIR_HANDLER_FROM>>>

<<<PAIR_HANDLER_TO>>>
    "stats.cache": lambda args: _cmd_stats_cache(
        since=getattr(args, "since", "") or "",
        job=getattr(args, "job", "") or "",
        by=getattr(args, "by", None),
        project=getattr(args, "project", None),
        all_projects=getattr(args, "all_projects", False),
    ),
    "stats.backfill-ledger": lambda args: _cmd_stats_backfill_ledger(
<<<END_PAIR_HANDLER_TO>>>

C5 — apps/cli/command_catalog.py. PAIR_CAT is CONTAINS-FROM: the new entry is
  inserted before the backfill-ledger entry.

<<<PAIR_CAT_FROM>>>
    CommandEntry(
        command_id="stats.backfill-ledger",
<<<END_PAIR_CAT_FROM>>>

<<<PAIR_CAT_TO>>>
    CommandEntry(
        command_id="stats.cache",
        group_id="stats",
        subcommand="cache",
        description=(
            "Cache-read share per bucket from the ledger. A share nobody could "
            "measure prints a word, never 0 %, and a role split names the limit "
            "it cannot show (read-only)."
        ),
        action_class="read_only",
        supports_json=False,
        related=("stats.cost", "stats.backfill-ledger"),
        args=(
            ArgDef("--since", "Only calls at or after this ISO-8601 timestamp", required=False, is_option=True),
            ArgDef("--job", "Only this job's calls", required=False, is_option=True),
            ArgDef("--by", "Group the shares by role, model or day (default: grand total only)", required=False, is_option=True),
            _PROJECT_SCOPE_OPT,
            _ALL_PROJECTS_FLAG,
        ),
        may_mutate_repo=False,
        may_execute_commands=False,
    ),
    CommandEntry(
        command_id="stats.backfill-ledger",
<<<END_PAIR_CAT_TO>>>

C6 — tests/cli/test_stats_cost.py. Two CONTAINS-FROM pairs, ONE commit.

<<<PAIR_TDOC_FROM>>>
  * `backfill-ledger` is idempotent: a second invocation adds no row.
<<<END_PAIR_TDOC_FROM>>>

<<<PAIR_TDOC_TO>>>
  * `backfill-ledger` is idempotent: a second invocation adds no row.
  * `stats cache` renders the cache-read share over the SAME rows, with two
    distinct words for its two distinct absences, and refuses to answer at all
    when the ledger cannot be read.
<<<END_PAIR_TDOC_TO>>>

<<<PAIR_TEST_FROM>>>
        assert sorted(p.name for p in filled_ledger.parent.iterdir()) == before
<<<END_PAIR_TEST_FROM>>>

<<<PAIR_TEST_TO>>>
        assert sorted(p.name for p in filled_ledger.parent.iterdir()) == before


class TestStatsCacheView:
    """`remedy stats cache` — the share view over the same ledger rows."""

    def test_the_command_is_in_the_catalog_and_has_a_handler(self):
        entry = get_command("stats.cache")

        assert entry is not None
        assert entry.action_class == "read_only"
        assert "stats.cache" in collect_all_handlers()

    def test_a_measured_bucket_renders_a_percentage(self, filled_ledger,
                                                    project_id, capsys):
        CMD._cmd_stats_cache(project=project_id, by="role")

        assert _table_row(capsys.readouterr().out, "builder")[2:5] == [
            "1000", "64", "6.0%"]

    def test_a_bucket_nobody_reported_says_so_instead_of_showing_zero(
        self, filled_ledger, project_id, capsys
    ):
        CMD._cmd_stats_cache(project=project_id, by="role")
        out = capsys.readouterr().out

        assert _table_row(out, "reviewer")[2:5] == ["unmeasured"] * 3
        assert "0.0%" not in out

    def test_a_role_split_names_the_limit_it_cannot_show(self, filled_ledger,
                                                         project_id, capsys):
        CMD._cmd_stats_cache(project=project_id, by="role")

        assert "Per-role limit" in capsys.readouterr().out

    def test_reported_zeros_are_undefined_and_not_unmeasured(self):
        from packages.orchestration.token_ledger import CostRow

        assert CMD._cache_read_share(
            CostRow(calls=1, tokens_in=0, cache_read=0)) == "undefined"
        assert CMD._cache_read_share(CostRow(calls=1)) == "unmeasured"

    def test_an_unreadable_ledger_exits_instead_of_reporting_zero(
        self, filled_ledger, project_id, capsys
    ):
        filled_ledger.write_bytes(b"this is not a database")

        with pytest.raises(SystemExit) as exc:
            CMD._cmd_stats_cache(project=project_id)

        assert exc.value.code == CMD.EXIT_ERROR
        assert "cannot read the token ledger" in capsys.readouterr().err
<<<END_PAIR_TEST_TO>>>

C7 — plan and handoff. Rewrite `.agent/plan.md` yourself: UNDER 50 lines, a
  `## Goal` heading and a `## Next Steps` heading, R45 gated-pending, the
  findings still open, and R46 (the `--json` mode for `stats cache` plus the
  before/after comparison note) as the next step. Then rewrite
  `.agent/handoff.md`: feature and round, branch, commit SHAs, changed-files
  table, item-status table, every gate with its REAL exit code, open-findings
  count, next expected action. Under 60 lines, or over it with a DECISION D15
  "Deviations, declared" line naming the count and its mandated causes.
  Commit C7, push the branch, create NO pull request.

Gates — run every one, record its REAL exit code, never the word "green"
  A  sha256sum + cmp across block file, authored file and last_block: all
     three equal, both `cmp` runs silent. B  wc -l the authored file vs cap 400.
  C  Pair shapes MEASURED: PAIR_ID FROM 1x before / 0x after, TO 1x after.
     PAIR_LR, PAIR_DEC, PAIR_VIEW, PAIR_HANDLER, PAIR_CAT, PAIR_TDOC and
     PAIR_TEST are all CONTAINS-FROM: FROM 1x before and 1x after, TO 1x after.
  D  Stray reconcile for C2, C3, C4, C5 and C6: `git show -U0 <sha> -- <path>`,
     then check every ADDED line appears in the authored file. Report added and
     stray counts for each.
  E  grep -c '^<<<' over all seven touched text files — every count 0.
  F  python3 -m pytest tests/cli/test_stats_cost.py -q — must include the six
     new tests. Report the total.
  G  python3 -m pytest tests/test_command_catalog.py tests/cli/test_command_catalog.py tests/cli/test_product_spine.py -q
  H  Canary: python3 -m pytest tests/cli/test_golden_path.py -q
  I  python3 -m py_compile on both changed production files.
  J  git status --porcelain EMPTY; git worktree list shows the primary ALONE;
     insertions per commit from `git show --numstat`, each under 500.
  K  git diff --name-only ae1756f8..HEAD — exactly the nine paths named above.

If gate F or G comes back RED, do NOT improvise a fix that leaves this change
set. Report the exact failure output and stop: a reviewer mistake in an
authored slice is mine to repair, and a round that halts honestly costs less
than one that invents its way past a red gate.

Do not: touch `main`, force-push, create `.agent/STOP`, merge anything, widen
the change set, or fix R-0221, R-0239, R-0247, R-0262, R-0265 or R-0266 — all
six stay OPEN by design. Write no `Done:` paragraph of your own: a landed but
ungated fix is marked `Landed: R-XXXX` and nothing else, because only
reviewer-authored text sets a resolution (planner_reviewer_prompt.md §4.4).
