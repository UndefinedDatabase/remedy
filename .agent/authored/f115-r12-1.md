── STEP T002-Goldens / R12 — F115 ─────────────────────────────────────────────
Goal:        Freeze the report's bytes against a ledger the REAL backfill
             wrote, so a change to the renderer has to be argued for instead of
             re-blessed — and close the guard hole R-0332 names before the
             goldens are blessed over that same module.

Bundle:      C1a save this block · C1b mirror it · C2 findings text (own commit,
             FIRST) · C3 R-0332 fix + its test · C4 the golden fixture and the
             golden pair on disk · C5 the golden-content tests · C6 plan +
             handoff.

Change:      Exactly these paths and nothing else:
             .agent/authored/f115-r12-1.md (new), .agent/last_block.md,
             .agent/live_review.md, packages/orchestration/cost_report.py,
             tests/orchestration/test_cost_report.py,
             tests/orchestration/fixtures/cost_report/golden/cost_report.md (new),
             tests/orchestration/fixtures/cost_report/golden/cost_report.json (new),
             .agent/plan.md, .agent/handoff.md.
             NO CLI, NO query change, NO schema change, NO token_ledger.py edit.

── C2 — .agent/live_review.md, OWN COMMIT, FIRST, before any code ─────────────
(i) REWRITE pair. Replace this ONE line, which is currently the last line of
the file, with the TO text below it. FROM appears exactly 1x today.

FROM:
Landed: R-0330 — a74e0668 rewrote the one docstring line to "READ-ONLY, and never raises on absence."; awaiting review.

TO:
Done: R-0330 — RESOLVED at the R11 gate. Verified against the disk and the behaviour, not the report: `grep -c 'READ-ONLY, never raises\.' packages/orchestration/token_ledger.py` prints 0, and the scoped sentence counts 2 — `query_cost`'s own at :1004 and `query_segment_shares`'s at :1098. Two is the CORRECT value, not a miscount: the fix makes the two docstrings agree, it does not make one of them unique. `git show --numstat a74e0668` changes exactly one line of one file. The claim is now true of the behaviour it describes — both functions still raise `ValueError` from `_resolve_ledger_path` when given neither `project_id` nor `path`, and neither raises on a ledger that is merely absent. The R11 round as a whole is PASS. The reviewer re-ran every gate itself: cmp exit 0 with sha256 431da8edba356a9521f58fec5be40f182cd7223addac54f1895a7799034dba74 over both copies, `wc -lc` 449 20234, ruff `All checks passed!`, the import exit 0, `10 passed` and `99 passed` and canary `42 passed` (151 in one run), `wc -l .agent/plan.md` 46, an empty porcelain, and 0/0 against origin. The authored C3 slice was compared DISK TO DISK against the applied file — 315 lines each, byte-identical — rather than against a reviewer retype, which is the R-0147 class this project has paid for before. Both mutation probes were RE-RUN INDEPENDENTLY in the reviewer's own disposable worktree rather than accepted from the handback: neutering `_same_question` fails exactly `test_a_mismatched_pair_is_refused_by_both_renderers` and nothing else, and changing `_figure`'s None branch to `return "0"` fails exactly `test_an_unmeasured_figure_prints_the_word_and_never_a_zero`; the worktree was removed and pruned with `git worktree list` left showing one line. The worker's fixture-design note was CHECKED rather than believed, and it is correct: rendering the DEFAULT pair under the second mutation still prints the word, from the "PARTLY UNMEASURED" sentence, so the fully-measured total in that one test is what makes the probe discriminating instead of decorative. That is a worker catch the block did not order, and it improved the round.

(ii) APPEND both of these to the END of the file, in this order, each separated
from its neighbour by one blank line:

- R-0331 — Low — reviewer block self-contradiction, self-registered. The R11
  block's "Change:" clause named SEVEN paths and said "nothing else", while its
  own "Constraints:" clause ordered a `Landed: R-0330` line into an EIGHTH,
  `.agent/live_review.md`. The two halves of one block disagreed about that
  block's own change set. The worker resolved it the right way: it wrote the
  line the constraint demanded and listed all eight paths in its handback,
  rather than dropping a mandated write to satisfy a file list. Sixth of the
  reviewer-arithmetic class after R-0282, R-0321, R-0323, R-0324 and R-0327,
  and the first whose two contradicting halves sat inside the SAME block — the
  earlier five were numbers the reviewer never re-derived from a list beside
  them, this one is a list the reviewer never re-derived from its own
  instructions four lines below. The standing checklist
  (`docs/agents/planner_reviewer_prompt.md`) sends the reviewer to the block's
  bytes, to the code it points at, to the file it writes into and to the tests
  that guard that file; it does not yet send the reviewer to the block's own
  other clause. No on-disk fix is possible — the block is committed verbatim by
  design and R11's verdict stands as PASS. Registered so the class stays
  countable rather than forgotten. OPEN.

- R-0332 — Low — `_same_question` guards the filters but not the ledger, so the
  one thing it exists to prevent can still happen. `cost_report.py` refuses a
  pair whose `since` or `job_id` disagree, on the stated ground that publishing
  the breakdown of one period beside the total of another silently answers a
  question nobody asked. Two reports drawn from DIFFERENT LEDGERS with
  identical filters pass that check unexamined, and the result is the same
  defect in a better disguise: a share table from one project rendered under
  another project's total, with no filter mismatch anywhere to betray it. Both
  dataclasses already carry `ledger_path` and `ledger_exists`, so the evidence
  needed to catch it was in hand and simply not read. It is Low because no
  caller exists yet — nothing outside the tests renders a report until T003
  wires the CLI — and that is also precisely why it should close before that
  caller is written rather than after. Reviewer-authoring defect: the guard was
  authored in the R11 block, so this is the R11 slice's own gap, found at its
  own gate. Fixed in R12, which opens that module for the goldens anyway. OPEN.

── C3 — packages/orchestration/cost_report.py, the R-0332 fix ─────────────────
(i) REWRITE pair inside `_same_question`'s docstring. FROM appears 1x:

FROM:
    already refuses to do for its own ``by`` argument.
    """

TO:
    already refuses to do for its own ``by`` argument.

    THE LEDGER IS PART OF THE QUESTION, not only the filters. Two reports with
    identical filters drawn from two DIFFERENT ledgers describe two different
    sets of calls, and rendering them together would publish one project's
    breakdown under another's total with no filter mismatch to betray it — the
    same defect the paragraph above refuses, wearing a better disguise. A
    ``ledger_path`` of None on BOTH sides is the ``merge_cost_reports`` case, a
    cross-project total that belongs to no single file, and it compares equal
    to itself as it should.
    """

(ii) REWRITE pair in the body. FROM appears 1x:

FROM:
            f"match query_segment_shares(since={shares.since!r}, "
            f"job_id={shares.job_id!r})"
        )

TO:
            f"match query_segment_shares(since={shares.since!r}, "
            f"job_id={shares.job_id!r})"
        )
    if (cost.ledger_path, cost.ledger_exists) != (
        shares.ledger_path,
        shares.ledger_exists,
    ):
        raise ValueError(
            "a cost report needs one ledger, not two: query_cost read "
            f"{cost.ledger_path!r} (exists={cost.ledger_exists}) and "
            f"query_segment_shares read {shares.ledger_path!r} "
            f"(exists={shares.ledger_exists})"
        )

(iii) Add ONE test to tests/orchestration/test_cost_report.py, directly after
`test_a_mismatched_pair_is_refused_by_both_renderers`, named
`test_a_pair_from_two_different_ledgers_is_refused_by_both_renderers`: same
`since` and `job_id` on both halves, `ledger_path="/data/a/ledger.sqlite"` on
the cost report and `"/data/b/ledger.sqlite"` on the share report, then
`pytest.raises(ValueError)` around `render_cost_report_markdown` AND around
`cost_report_json_bytes`. Give it a one-line docstring saying that identical
filters over two different ledgers are still two questions.

── C4 — the golden fixture and the golden pair on disk ────────────────────────
Append to tests/orchestration/test_cost_report.py, after the existing tests, a
section under the comment banner
`# ── The golden pair, over a ledger the REAL backfill wrote ──────────────────`
containing exactly this fixture builder. Build it in THIS module rather than
importing the private helpers of `test_token_ledger.py`: a golden whose input a
reader cannot see in the same file is a golden that gets re-blessed instead of
argued with.

GOLDEN_DIR = Path(__file__).parent / "fixtures" / "cost_report" / "golden"
GOLDEN_LABEL = "f115-golden"
GOLDEN_MARKDOWN_NAME = "cost_report.md"
GOLDEN_JSON_NAME = "cost_report.json"

Helpers (write them with these exact names and shapes):
  * `_write_json(path, payload)` — `json.dumps(payload, indent=2) + "\n"`,
    utf-8, parents created.
  * `_manifest_entry(name, rank, sha256, chars, tokens_estimated)` — the five
    keys of one `ComposedPrompt.manifest_as_dicts()` row, in that order.
  * `_trace_entry(job_id, task_id, manifest)` — a real prompt-trace object:
    `run_id="run-golden"`, the given `job_id` and `task_id`, `round=1`,
    `role="builder"`, `provider="fake"`, `prompt_kind="initial"`,
    `prompt_sha256="0" * 64`, `prompt_chars=1234`,
    `prompt_tokens_estimated=308`, `segment_manifest=list(manifest)`,
    `segment_manifest_chars=sum(m["chars"] for m in manifest)`,
    `created_at="2026-08-08T09:00:00+00:00"`.
  * `_evidence_tree(root, job_id, runs)` — writes `manifest.json`
    (`{"bundle_type": "job_evidence", "job_id": job_id}`) and, per run tuple
    `(task_id, ts_utc, manifest, extra)`, a `task_runs/<task_id>/` holding
    `provider_evidence.json` built from this base dict updated with `extra` —
    `schema_version="1.0.0"`, `task_id`, `execution_mode="provider_backed"`,
    `provider_call_count=1`, `actual_call_count=1`, `cost_call_count=1`,
    `actual_prompt_tokens=1000`, `actual_completion_tokens=200`, `ts_utc` —
    plus `token_accounting.json` = `{"role": "builder"}`, plus, when `manifest`
    is not None, a real one-line JSONL `prompt_trace.jsonl`.
  * fixture `golden_ledger(tmp_path)` — three manifest entries,
    `task_brief` rank 10 sha `"a"*64` chars 120 tokens 30, `diff` rank 20 sha
    `"b"*64` chars 400 tokens 100, `schema_tail` rank 30 sha `"c"*64` chars 60
    tokens 100. Job `"job-traced"`: T001 at `2026-08-01T10:00:00+00:00` with
    `[task_brief, diff]`, T002 at `2026-08-05T10:00:00+00:00` with
    `[schema_tail]`. Job `"job-bare"`: T001 at `2026-08-09T10:00:00+00:00` with
    manifest None and no extra, T002 at `2026-08-09T11:00:00+00:00` with
    manifest None and extra `{"total_cost_usd": 0.25,
    "actual_cache_read_tokens": 64, "actual_cache_creation_tokens": 32,
    "actual_model_verified": True, "builder_actual_model": "claude-opus-5"}`.
    Backfill BOTH trees into one `tmp_path / "ledger.sqlite"` with the real
    `backfill_ledger(tree, path=ledger)`; assert each returns `recorded == 2`.
    Return the ledger path.
  * `_golden_pair(ledger)` — returns
    `(query_cost(path=ledger, by="day"), query_segment_shares(path=ledger))`.

Then WRITE the two golden files from that pair with
`label=GOLDEN_LABEL`, once, by hand or by a throwaway script — they are DATA,
committed as files, not generated at test time. Their content must be exactly
what `render_cost_report_markdown` and `cost_report_json_bytes` produce for
that pair.

The fixture ledger's expected values, MEASURED BY THE REVIEWER against a real
backfill before this block was written. Compute them independently; if any of
yours differs, report BOTH numbers and do not adjust anything to match:
  * cost total: calls 4, tokens_in 4000, tokens_out 800, cache_read 64,
    cache_write 32, cost_usd 0.25, measured_calls 1, unmeasured_calls 3,
    fully_measured False — so the PARTLY UNMEASURED sentence fires.
  * cost buckets, by="day", three of them: `2026-08-01` 1 call 1000/200 with
    every other figure None and 0 measured; `2026-08-05` 1 call 1000/200
    likewise; `2026-08-09` 2 calls 2000/400, cache 64/32, cost 0.25, 1 measured.
  * shares, in the pinned order: `diff` 1 call 1 segment 400 chars 100 tokens;
    `schema_tail` 1/1/60/100; `task_brief` 1/1/120/30.
  * attributed_calls 2, unattributed_calls 2; totals 3 segments, 580 chars,
    230 tokens_estimated.
  * therefore the share cells are 43.5%, 43.5%, 13.0% and the TOTAL row 100.0%,
    and `cost_usd` renders as `0.2500`.

── C5 — the golden-content tests ──────────────────────────────────────────────
Four tests, these names, appended after the fixture section:
 1. test_the_golden_markdown_matches_the_fixture_ledger
    Byte-for-byte: `render_cost_report_markdown(*_golden_pair(golden_ledger),
    label=GOLDEN_LABEL)` equals `(GOLDEN_DIR / GOLDEN_MARKDOWN_NAME).read_text(
    encoding="utf-8")`. Docstring: a golden re-blessed on every change checks
    nothing.
 2. test_the_golden_json_matches_the_fixture_ledger
    The same, for `cost_report_json_bytes` and `GOLDEN_JSON_NAME`.
 3. test_the_golden_files_state_the_numbers_the_ledger_holds
    Reads the two FILES, not the renderer, and asserts the measured values
    above independently: the json's total is calls 4, tokens_in 4000,
    tokens_out 800, cache_read 64, cache_write 32, cost_usd 0.25,
    measured_calls 1, unmeasured_calls 3; its bucket list is exactly
    `["2026-08-01", "2026-08-05", "2026-08-09"]`; its segment rows are exactly
    `["diff", "schema_tail", "task_brief"]` with
    total_tokens_estimated 230, attributed_calls 2, unattributed_calls 2. The
    markdown contains `PARTLY UNMEASURED`, `unmeasured`, `0.2500`, `43.5%` and
    `13.0%`. This test is what stops the pair from being a snapshot of whatever
    the renderer happened to emit.
 4. test_the_golden_json_agrees_with_the_golden_markdown
    Both files read from disk; every segment name in the json appears in the
    markdown, and the json's `total_tokens_estimated` appears in it as a cell.

Constraints:
 - Do-not-touch (T2_F115.md): pricing tables, calibration, UI rendering,
   scheduled reporting. No CLI wiring this round.
 - packages/ never imports from apps/.
 - No edit to token_ledger.py, to any query, or to the schema.
 - The goldens are DATA on disk. No test regenerates or rewrites them; a test
   that would "bless" a golden on mismatch is a defect, not a convenience.
 - Open findings stay open: R-0320, R-0322, R-0323, R-0324, R-0327, R-0328 are
   NOT fixed here. Write no `Done:` paragraph of your own — C2's text is
   reviewer-authored and complete. If R-0332's fix lands before its review,
   mark it `Landed: R-0332 — <one line, which commit>` and nothing else.
 - C2 is its own commit and comes first.
 - Destructive checks only inside a disposable worktree under .remedy-wt/.

Done when — run every command and record its REAL output and exit code:
 (a) cmp .agent/authored/f115-r12-1.md .agent/last_block.md        → exit 0;
     report sha256sum of both and `wc -lc` of one.
 (b) In .agent/live_review.md after C2:
       grep -c '^Landed: R-0330'   → 0
       grep -c '^Done:'            → 5   (four before this round, plus R-0330)
       grep -c '^- R-0'            → 13  (eleven before, plus R-0331 and R-0332)
       grep -c '^## Steps'         → 1
     and, scoped to that commit's ADDED lines only
     (`git show <sha> -- .agent/live_review.md | grep '^+'`), each of
     `^+Done: R-0330`, `^+- R-0331`, `^+- R-0332` appears exactly 1x.
 (c) python3 -m ruff check packages/orchestration/cost_report.py tests/orchestration/test_cost_report.py
       → All checks passed!
 (d) python3 -c "import packages.orchestration.cost_report"          → exit 0
 (e) python3 -m pytest tests/orchestration/test_cost_report.py -q    → report
     the exact count; 15 tests are ordered (10 from R11, 1 from C3, 4 from C5).
 (f) python3 -m pytest tests/orchestration/test_token_ledger.py -q   → 99 passed
 (g) python3 -m pytest tests/cli/test_golden_path.py -q              → 42 passed
 (h) Determinism, run twice in one process or as two invocations: the golden
     markdown and json render identical bytes on a REBUILT fixture ledger under
     a different tmp_path. Report how you established it.
 (i) PROBE 1, disposable worktree at HEAD under .remedy-wt/: delete the whole
     `if (cost.ledger_path, cost.ledger_exists) != (...)` block added by C3.
     The C3 test asserts that raise directly, so it MUST fail. Report the exact
     failed/passed counts and ids you measured.
 (j) PROBE 2, same discipline: in `_share_percent`, change the format from
     `.1f` to `.2f`. Both golden byte-comparisons MUST fail. Report the exact
     counts and ids, and say which tests stayed green and why that is right.
     Remove and prune the worktrees; `git worktree list` must end at one line.
 (k) wc -l .agent/plan.md                                            → under 50
 (l) git status --porcelain                                          → empty
 (m) git rev-list --left-right --count origin/feature/f115-prompt-cost-report...HEAD
                                                                     → 0  0
 (n) git diff --name-only 0d6c97aa..HEAD | wc -l  → report the number, and
     confirm no `.remedy-wt/**` path is among them.

── C6 — state ─────────────────────────────────────────────────────────────────
Rewrite .agent/plan.md (under 50 lines; keep "## Goal" and "## Next Steps";
Next Steps 1 becomes T003 — the `remedy stats report` CLI, `--until`, the
prior-period comparison and the json schema). Rewrite .agent/handoff.md per
AGENTS.md with the mandated tables and real values; repeat this line verbatim:
`Fortschritt: 80 % (T001 ✅ · T002 ✅ · T003 offen) — Schätzung`

Handback:    completion report with the item-status table + rewrite
             .agent/handoff.md.
──────────────────────────────────────────────────────────────────────────────
