── STEP T003c/4 — F115 Prompt breakdown & cost report · Round 17 ─────────────
Goal:        Put the report in a user's hands. `remedy stats report` renders
             the cost report and its prior-period comparison as markdown or
             json, over one project's ledger, from the pieces R15 and R16
             built.

Bundle:      This is the ONLY ordering statement in this block. Every later
             clause defers to it and none of them restates an order.
  C1  Findings first. Append the authored paragraph of SLICE A to
      `.agent/live_review.md`. OWN commit, and the FIRST commit of the round.
  C2  Save this whole block verbatim to `.agent/authored/f115-r17-1.md`.
  C3  Mirror the same bytes into `.agent/last_block.md`.
  C4  `apps/cli/command_catalog.py` — the `stats.report` entry.
  C5  `apps/cli/commands/stats_ledger_cmd.py` — the handler, the period-bound
      validator, and the `UNMEASURED` unification.
  C6  `tests/cli/test_stats_report.py` — new file, the round's tests.
  C7  Replace `.agent/plan.md` with SLICE B, then rewrite `.agent/handoff.md`.

Change:
  C4 — apps/cli/command_catalog.py
    * One new `CommandEntry`, placed directly after the `stats.cache` entry so
      the read-only stats views stay together:
      `command_id="stats.report"`, `group_id="stats"`, `subcommand="report"`,
      `action_class="read_only"`, `supports_json=True`,
      `related=("stats.cost", "stats.cache")`,
      `may_mutate_repo=False`, `may_execute_commands=False`.
    * Args: `--since`, `--until`, `--job`, `--by`, `--label`, the shared
      project-scope option, and the shared json option. In that order.
    * NO `--all-projects` flag, deliberately. Say why in the description:
      `merge_cost_reports` folds cost across projects but there is no
      cross-project merge for the segment breakdown, so an all-projects report
      would publish one project's breakdown under a multi-project total —
      exactly the mismatch `cost_report._same_question` exists to refuse.
      Write that as a short sentence in the entry's `description`, not only in
      a comment: the description is what `remedy <group> --help` prints.

  C5 — apps/cli/commands/stats_ledger_cmd.py
    * `UNMEASURED = COST_UNMEASURED_LABEL`, imported from
      `packages.orchestration.cost_report`, replacing the duplicated string
      literal. The NAME `UNMEASURED` stays exactly as it is — tests reach it as
      a module attribute — and the `#:` comment above it is updated to say the
      spelling now lives in one place. Follow this module's existing
      import style: it imports inside functions, so if a module-level import
      of `cost_report` creates a cycle or breaks a test, keep the constant
      module-level by importing `cost_report` at module scope only if that is
      clean, and otherwise state the obstacle in the handback rather than
      inventing a third spelling.
    * A period-bound validator used by the REPORT command only, leaving
      `stats cost` and `stats cache` untouched: it accepts an empty string,
      accepts an ISO-8601 timestamp (with `Z` read as `+00:00`), and on
      anything else prints an error NAMING THE FLAG THAT WAS WRONG and exits
      `EXIT_USAGE`. `--since` and `--until` must produce different messages;
      a validator that always says `--since` is a defect.
    * `_cmd_stats_report(*, since, until, job, by, label, project,
      json_output)`. It:
      - validates both bounds and `--by` (reuse `_validate_by`);
      - resolves EXACTLY ONE project's ledger — reuse `_one_project_ledger`
        with `all_projects=False` and `action="stats report"`;
      - runs `query_cost` and `query_segment_shares` over the same
        `since`/`until`/`job`;
      - calls `prior_report_period(since or None, until or None)`; when it is
        available, runs a SECOND `query_cost` over the prior window with
        `by=None` and the SAME `job` filter, and passes it as `prior`; when it
        is not, passes `no_comparison_reason=period.unavailable_reason` and no
        prior;
      - renders with `render_cost_report_markdown` or
        `cost_report_json_bytes` per `--json`, passing `--label` through, and
        prints the result;
      - handles `sqlite3.Error` the way `_load_ledger_reports` already does —
        a database error is not a zero.
      The prior query MUST carry the same `job` filter as the main one: a
      comparison against a differently-filtered window is the defect
      `_same_question` refuses one layer up, and the CLI must not be the thing
      that constructs it.
    * Register `"stats.report"` in `COMMAND_HANDLERS`, in the same
      `getattr(args, ...)` style as its neighbours.

  C6 — tests/cli/test_stats_report.py, a NEW file
    Build a fixture ledger the same way `tests/cli/test_stats_cost.py` already
    does — reuse its approach rather than inventing a second one; import from
    it if that is how this suite already shares fixtures, and otherwise say in
    the handback why a local copy was necessary. Cover, one property per test:
    * markdown output carries the cost table, the segment section and the
      comparison section;
    * `--json` output parses, and its `report_version` and `comparison` keys
      are present;
    * a `--since`/`--until` pair with data on both sides produces
      `comparison.available == true` and a prior window whose `until` is the
      `--since` string byte for byte;
    * an open-ended period (no `--until`) produces `available == false` with
      the open-ended reason, and NO zeros in the deltas — every delta null;
    * a bad `--until` exits `EXIT_USAGE` and the message names `--until`, not
      `--since`;
    * `--job` is applied to the prior query too: a job filter that excludes
      the prior window's calls yields an empty prior, and the output says the
      window was read and held nothing rather than printing zeros.

Constraints:
  * AGENTS.md is the highest authority; nothing here weakens it.
  * Every commit is pushed before the next one begins (finding R-0289).
  * Each commit stays under the 500-insertion cap (`+` column only). If C6
    approaches it, split it by test group and say so in the handback.
  * Commit subjects carry no leading-slash token, no absolute path, no
    secret-like string. In particular the subject must not contain
    `/stats` or any other leading-slash token.
  * Do NOT touch: `docs/`, `docs/roadmap/`, `packages/orchestration/cost_report.py`,
    `packages/orchestration/token_ledger.py`, the goldens, pricing, calibration.
    This round consumes R15's and R16's work; it does not revise it. If you
    find a real defect in either, STOP and report it rather than fixing it
    here.
  * `stats cost` and `stats cache` keep their exact current behaviour and
    output. The only change to them is that `UNMEASURED` is now an imported
    spelling of the same word.
  * SLICE A appends to the end of `.agent/live_review.md`. SLICE B fully
    replaces `.agent/plan.md`. Both are applied BYTE FOR BYTE — no rewording,
    rewrapping or trimming. If a slice cannot be applied as given, apply
    nothing and report the exact obstacle.
  * Destructive verification runs ONLY inside a disposable `git worktree`
    under the gitignored `.remedy-wt/`, under a path name unique to this round.
    `.remedy-wt/` holds other sessions' scratch — create only your own
    directory and delete only your own. Remove and prune before the handback.
  * `git status --porcelain` is empty at handback.

Done when: every value below is REAL and recorded in the handback with the
command that produced it. "Green" as a word is not a result. Do NOT predict or
target any count — MEASURE the baseline BEFORE your first code commit, report
it, then report the value after.
  (a) `.agent/authored/f115-r17-1.md` and `.agent/last_block.md` are byte
      identical. Report the method, the sha256 of BOTH, and
      `wc -lc .agent/last_block.md`.
  (b) Scoped to the ADDED lines of C1's own commit:
      `git show <C1> -- .agent/live_review.md` shows `^+Done: R-0336` exactly
      once, and `git show --numstat <C1>` reports ZERO deleted lines.
      Whole-file after C1: `^Done:` 10, `^- R-0` 17, `^## Steps` 1,
      `^Landed:` 0.
  (c) `git log --oneline aa7ad8df..HEAD` lists C1 LAST — the oldest.
  (d) `python3 -m ruff check` over every file this round touches prints
      `All checks passed!` and exits 0.
  (e) `python3 -m pytest tests/cli/test_stats_report.py -q` — report the real
      number.
  (f) `python3 -m pytest tests/cli/test_stats_cost.py -q` — measure the
      baseline BEFORE C5 and report BOTH numbers. The `UNMEASURED`
      unification must move neither the count nor any assertion.
  (g) `python3 -m pytest tests/test_command_catalog.py tests/test_grouped_cli.py -q`
      — measure the baseline BEFORE C4 and report BOTH numbers. A new catalog
      entry is exactly what these contract tests exist to check, so if a count
      legitimately rises, say which test and why.
  (h) Canary: `python3 -m pytest tests/cli/test_golden_path.py -q` — baseline
      42. Report the real number.
  (i) `python3 -m pytest tests/orchestration/test_cost_report.py
      tests/orchestration/test_token_ledger.py -q` — baseline 134, and this
      round touches neither module. Report the real number.
  (j) ONE probe, in your disposable worktree: make the prior `query_cost` drop
      the `job` filter — pass `job_id=None` where it currently passes the
      report's job. Run `tests/cli/test_stats_report.py` and report the NAMES
      of every test that fails. Report names, not counts, and do not predict
      either. Then remove and prune the worktree and show `git worktree list`.
  (k) `remedy stats report --help` may be UNAVAILABLE to you: the `remedy`
      binary is refused in this session's sandbox. Do not fabricate its
      output. Instead prove the wiring the way the suite does — show that the
      catalog entry is discoverable and the handler key resolves — and state
      in the handback that the binary itself was not invoked and why.
  (l) `wc -l .agent/plan.md` under 50; `git status --porcelain` empty;
      `git rev-list --left-right --count origin/feature/f115-prompt-cost-report...HEAD`
      is `0  0`; `git diff --name-only 0d6c97aa..HEAD` contains no path
      matching `remedy-wt`.

═══ SLICE A — APPEND to .agent/live_review.md ═══════════════════════════════

Done: R-0336 — REGISTERED, not resolved, and it stays OPEN by construction: the block that carried the wrong prediction is committed verbatim by design, so there is nothing on disk to correct. Its counter-measure, however, was applied immediately rather than deferred, and it worked: R16's gate (d) predicted no line count at all and ordered a structural proof instead, the worker returned real numstats of `14 1` and `4 0` together with a key-by-key comparison, and the reviewer re-ran that comparison independently — `buckets`, `segments`, `total`, `label`, `filters`, `ledger_exists` and `note` all equal, added keys exactly `['comparison']`, removed none, changed exactly `['report_version']` 2 to 3. No figure, bucket or segment row moved. The R16 round as a whole is PASS. The reviewer re-ran every gate itself: `cmp .agent/authored/f115-r16-1.md .agent/last_block.md` exit 0 — again the reviewer's sandbox allows `cmp` where the worker's refuses it, so the worker's sha256-plus-byte-compare substitute was corroborated by the primary proof rather than accepted — with sha256 `24984348f53494604bcbf924b9b91238a9d0c53b33faadf53f71d724ce7b009b` over both copies, `wc -lc` 298 23248, the live-review counts 9 / 17 / 1 / 0, `git show --numstat aa1a6cfb` 4 insertions and ZERO deletions, C1 the oldest commit of `6752841a..HEAD`, ruff `All checks passed!` over all four files, 134 passed against a 119 baseline, 83 passed over the canary and the untouched CLI cost tests, `wc -l .agent/plan.md` 43, an empty porcelain, 0 0 against origin, and 39 changed paths with no `remedy-wt` among them. Both authored slices were compared DISK TO DISK against the committed `.agent/authored/f115-r16-1.md` — 43 of 43 plan lines and 44 decision lines, byte-identical. The C5 deviation is ACCEPTED and is an improvement the block did not ask for: a comparison that does not name its own baseline is a number the reader cannot check against anything, so the `Previous period: since=… until=… · N call(s).` provenance line belongs there. A PROBE of the reviewer's own choosing settled what the two ordered probes could not. P1 removed the subtraction, which only proves the window is displaced; neither probe touched the load-bearing claim of DECISION F115 D6 — that the prior window's `until` is the caller's own `since` STRING and never a re-serialisation of it. Replacing `until=since` with `until=parsed_since.isoformat()` in a disposable worktree fails exactly `TestPriorReportPeriod::test_the_prior_window_of_a_bare_date_pair` and `TestPriorReportPeriod::test_the_prior_until_is_the_original_since_string_byte_for_byte`, and nothing else, so the byte-reuse rule is pinned by a test named for it rather than merely described in a docstring. The worktree was removed and pruned; `git worktree list` shows one line. One inaccuracy is recorded here WITHOUT being registered as a finding, because it moved no evidence: the R16 handback attributed the json golden's single deleted line to a trailing comma gained by the `buckets` array, when the diff shows that line unchanged and the deletion is simply the `report_version` line being rewritten. The number reported was correct, the structural proof was correct and independently reproduced, and the wrong aside sits in a handback sentence rather than in a gate value — registering it would cost a round more than the error costs the record.

═══ SLICE B — FULL REPLACEMENT of .agent/plan.md ════════════════════════════

# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged. Last reviewed SHA: aa7ad8df (R16 PASS). Next free finding
ID: R-0337. Open findings: 10 — R-0320, R-0322, R-0323, R-0324, R-0327,
R-0328, R-0331, R-0333, R-0334, R-0336. No PR exists and closure has not
started.

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
T003 is wired to a user. `remedy stats report` resolves one project's
ledger, runs the cost and share queries over `[since, until)`, places the
prior window with `prior_report_period` and queries it under the SAME job
filter, then renders markdown or json. `--all-projects` is deliberately
absent: there is no cross-project merge for the segment breakdown, so an
all-projects report would publish one project's breakdown under a
multi-project total. `stats_ledger_cmd.UNMEASURED` is now an import of
`COST_UNMEASURED_LABEL`, so the word has one spelling.

## Next Steps
1. T003d — the docs page the new user-visible behaviour needs, registered
   in the `docs/README.md` index in the same PR.
2. Integration gate (docs/agents/integration_gate.md).
3. Closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Per-role has one bucket until `role` stops being hardcoded, and
  per-task-class has no source at all: report "no data", never a bucket.
- R-0322 will meet F115's integration gate as five pre-existing reds.
- The goldens are DATA: no test may regenerate them. A renderer change
  that moves the bytes must move the files in the same, argued commit.
- The `remedy` binary is refused in this session's sandbox, so CLI wiring
  is proven through the suite and never through a pasted `--help`.

Fortschritt: 93 % (T001 ✅ · T002 ✅ · T003 fast fertig) — Schätzung

═════════════════════════════════════════════════════════════════════════════

Handback:    A completion report plus a rewritten `.agent/handoff.md`, carrying
             feature and round, branch, the per-commit table, the changed-files
             table, the item-status table over C1..C7 with `done`/`skipped`/
             `deviated` and a reason for anything not `done`, every gate value
             (a)..(l) as a real measured value with its baseline where one was
             ordered, the open-findings count, and the next expected action. It
             repeats the Fortschritt line of SLICE B verbatim. Cap is 60 lines;
             exceed it only with a DECISION D15 "Deviations, declared" line
             naming the real line count and the mandated content that caused
             the overage. Never drop a section to meet the cap.
─────────────────────────────────────────────────────────────────────────────
