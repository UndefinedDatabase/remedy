# Handoff — F115 Prompt breakdown & cost report · Round 9 (SESSION END)

Branch: feature/f115-prompt-cost-report · HEAD after C6 pushed · no PR exists.
Last reviewed SHA: 8615259b (R8 PASS). Open findings: 6 — R-0320, R-0322,
R-0323, R-0324, R-0327, R-0328. Next free finding ID: R-0329.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1a  | done   | |
| C1b  | done   | |
| C2   | done   | TEXT-A appended byte for byte, sliced out of the saved block |
| C3   | done   | constant + TEXT-B verbatim + reader + its private row builder |
| C4   | done   | writer, backfill wiring, three Public API lines |
| C5   | done   | six tests in one new class, plus four module-level helpers |
| C6   | done   | |

## Commits

| SHA | Subject | Insertions |
|-----|---------|-----------|
| 701e0f3b | chore(f115): save the R9 step block as authored text | 308 |
| e071c79a | chore(f115): mirror the R9 block into last_block | 262 |
| e2f73262 | docs(f115): register R-0327 and R-0328 from the R8 gate | 37 |
| 6b8305e6 | feat(f115): read segment manifests out of the copied prompt trace | 139 |
| 8632bb16 | feat(f115): write call_segments rows on the backfill path | 83 |
| 35ca075f | test(f115): pin the segment reader, writer and backfill seam | 240 |
| C6       | chore(f115): refresh the plan and write the R9 handoff | see git |

## Changed files

| Path | Change |
|------|--------|
| .agent/authored/f115-r9-1.md | new, 308 lines |
| .agent/last_block.md | rewritten, identical bytes |
| .agent/live_review.md | +37, two OPEN findings |
| packages/orchestration/token_ledger.py | +222 / -1 over C3+C4 |
| tests/orchestration/test_token_ledger.py | +240 |
| .agent/plan.md | full replace, 38 lines |
| .agent/handoff.md | rewritten (this file) |

`.remedy-wt/f115-r9-1.md` is the gitignored source and is NOT committed
(`git check-ignore` confirms `.gitignore:235`).

## Results, all measured

a. `cmp` exits 0 (CMP_EXIT_0 printed). sha256 of BOTH copies:
   `c5c5bc40c103ce743a81156078a727231460fe321be65e87613e2dc0265244b6`.
   `wc -lc .agent/authored/f115-r9-1.md` = `308 19369`. No trailing whitespace
   on any line (checked mechanically, 0 offending lines).
b. `.agent/live_review.md`: `^- R-0327` = 1 · `^- R-0328` = 1 · `^- R-0` = 9 ·
   `^Done:` = 3 (unchanged) · `^## Steps` = 1. All five as ordered.
c. `token_ledger.py`: `class CallSegmentRow` = 1 · `def
   segment_rows_from_trace_file` = 1 · `def record_call_segments` = 1 ·
   `_CALL_SEGMENT_COLUMNS` = 4 (definition, two uses in the INSERT builder, one
   in the row tuple comprehension) · `_PROMPT_TRACE_FILENAME` = 2 (constant +
   backfill use) · `record_call_segments` = 3 (definition, docstring API line,
   backfill call). `ruff check` printed `All checks passed!` exit 0;
   `python3 -c "import packages.orchestration.token_ledger"` exit 0.
d. `git diff 8615259b..HEAD -- packages/orchestration/token_ledger.py`: 223
   changed lines, of which lines assigning `result.scanned` / `result.recorded`
   / `result.skipped` / `result.failed` = 0, and changed lines inside the
   `class BackfillResult` body = 0. The only changed lines naming
   `BackfillResult` are the Public API line and a comment. The seam hunk:

```
@@ -645,6 +817,24 @@ def backfill_ledger(
                 continue
             if record_call(record, project_id=project_id, path=path):
                 result.recorded += 1
+                # BACKFILL IS THE ONLY WIRED PATH, deliberately: the live hook
+                # at the actuals seam fires BEFORE the exporter copies
+                # prompt_trace.jsonl into the task-run directory
+                # (``pingpong_evidence.py:517-525`` vs ``:527-536``), so this is
+                # the only place the file demonstrably exists. NO BackfillResult
+                # COUNTER MOVES either way — the return value is deliberately
+                # not branched on, because a segment read or write that fails is
+                # a counted ledger miss and nothing else, and `calls` mirroring
+                # must stay exactly as measurable as it was before F115.
+                record_call_segments(
+                    segment_rows_from_trace_file(
+                        task_dir / _PROMPT_TRACE_FILENAME,
+                        call_id=record.call_id,
+                        task_id=task_dir.name,
+                    ),
+                    project_id=project_id,
+                    path=path,
+                )
             else:
                 result.failed += 1
         except Exception:  # pragma: no cover - defence in depth; nothing below raises
```

e. `pytest tests/orchestration/test_token_ledger.py -q` → `92 passed in 6.35s`
   (R8 baseline 86, six added). `pytest tests/cli/test_stats_cost.py -q` →
   `41 passed in 0.46s`, unmoved.
f. RED-PROOF, disposable worktree `.remedy-wt/r9-redproof` at 35ca075f detached,
   body of `segment_rows_from_trace_file` replaced by `return []` (diff: 1
   insertion, 31 deletions, that function only). Result: **5 failed, 87 passed
   in 6.81s**. The five ids, all in `TestCallSegmentsWriter`:
   `test_two_entries_yield_their_rows_in_file_order`,
   `test_an_empty_manifest_yields_no_row_but_still_consumes_its_index`,
   `test_another_task_runs_entries_are_ignored`,
   `test_absent_malformed_and_partial_inputs_never_raise`,
   `test_backfill_writes_the_segment_rows_and_moves_no_counter`. The sixth new
   test, `test_recording_the_same_segments_twice_leaves_one_row_each`, passes by
   design: it drives `record_call_segments` directly and never calls the reader.
   Mutation not adjusted. Worktree removed and pruned; `git worktree list`
   afterwards shows exactly one line, the primary checkout at 35ca075f.
g. Canary `pytest tests/cli/test_golden_path.py -q` → `42 passed in 19.62s`,
   unmoved.
h. `wc -l .agent/plan.md` = 38 (below 50).
i. `git status --porcelain` empty · `git diff --name-only 0d6c97aa..HEAD | wc -l`
   = 28, exactly the 27 from R8 plus `.agent/authored/f115-r9-1.md`; no
   `.remedy-wt/**` path among them ·
   `git rev-list --left-right --count origin/...HEAD` → see the closing line
   below, re-measured after the C6 push.

## Shell rewrites declared

The sandboxed shell refuses any command containing `$`. Rewritten: exit-code
capture (`echo CMP_EXIT_0` on success instead of `echo "$?"`), the five
`grep -c` counts (five separate greps instead of a `for p in ... "$p"` loop),
and the trailing-whitespace / diff-scanning checks (`python3` heredocs instead
of `grep ' $'`). Every gate value above is a real measured output.

## Resume here

Next work is **T002**: aggregation queries over `calls` joined to
`call_segments`, plus the pure renderer emitting markdown and json. Follow
`packages/orchestration/gauntlet_matrix.py` with its golden PAIR at
`tests/orchestration/fixtures/gauntlet/golden/matrix.{json,md}`, and the
fixture-ledger pattern at `tests/cli/test_stats_cost.py:49-128` — both already
inventoried in `.agent/f115_inventory.md` section "## Q7". The ledger is now
readable end to end: a backfilled tree carries the segment rows.

NO PR EXISTS on this branch and CLOSURE HAS NOT STARTED. Do not assume either.
The live hook remains deliberately unwired (it fires before the trace copy);
that is a design decision, not an omission.

Deviations, declared: this handoff is over 60 lines because AGENTS.md DECISION
D15's mandated content does not fit — the item-status table, the commit table,
the changed-files table, nine measured gate results including gate (d)'s pasted
`backfill_ledger` hunk and gate (f)'s five failing test ids, the shell-rewrite
declaration, and the session-end "Resume here" section.

Fortschritt: 58 % (T001-Schema ✅ · T001-Writer ✅ · T002 · T003 offen) — Schätzung
