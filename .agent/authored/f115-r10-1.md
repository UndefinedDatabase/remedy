── STEP R10/n — F115 Prompt breakdown & cost report · Round 10 ───────
Goal:        T002 part one — the aggregation query that joins `calls` to
             `call_segments` and reports per-segment shares with attributed and
             unattributed calls counted separately, plus the type guard that
             keeps an unpublishable manifest value out of the sums it would
             otherwise become a silent zero in.
Bundle:      C1a save block · C1b mirror · C2 register R-0329 ·
             C3 the manifest type guard and its test · C4 the aggregation query ·
             C5 tests · C6 plan + handback
Change:      EXACTLY these paths, nothing else:
               .agent/authored/f115-r10-1.md              (new, C1a)
               .agent/last_block.md                       (rewrite, C1b)
               .agent/live_review.md                      (C2: append)
               packages/orchestration/token_ledger.py     (C3, C4)
               tests/orchestration/test_token_ledger.py   (C3, C5: append)
               .agent/plan.md                             (C6: full replace)
               .agent/handoff.md                          (C6: rewrite)
Constraints:
  - TEXT-A and TEXT-B are AUTHORED text: apply byte for byte, sliced out of the
    saved `.agent/authored/f115-r10-1.md`. Everything else in C3-C5 you author
    yourself to the contracts below, in the file's existing idiom.
  - Do NOT write a `Done:` paragraph and do NOT mark anything resolved
    (docs/agents/planner_reviewer_prompt.md §4.4). TEXT-A registers ONE open
    finding. When you have fixed R-0329 in C3, the only permitted line is
    `Landed: R-0329 — <one line: what changed, which commit>`, appended in C6.
  - Do NOT fix R-0320, R-0322, R-0323, R-0324, R-0327 or R-0328.
  - Do NOT touch `calls`, `CallRecord`, `_CALL_COLUMNS`, `record_call`,
    `call_record_from_evidence`, `backfill_ledger`, `verify_ledger`,
    `query_cost`, `merge_cost_reports`, `CostRow`, `CostReport`,
    `SCHEMA_VERSION`, `_MIGRATIONS` or ANY existing migration statement. The
    schema is FINAL this round: no migration step is added, edited or bumped.
  - Do NOT touch `segment_rows_from_trace_file`, `record_call_segments` or the
    `CallSegmentRow` field set. C3 opens `_call_segment_row` and the
    `_MANIFEST_KEYS` definition and NOTHING else in the reader.
  - NO RENDERER and NO CLI this round. Markdown, json, goldens and
    `remedy stats report` are R11 and T003. Do not create
    `packages/orchestration/cost_report.py`.
  - REUSE the module's existing query plumbing; do not write a second one.
    `_resolve_ledger_path`, `_connect_readonly` and `_cost_filters` already
    exist and the new query uses all three. `_cost_filters` emits UNQUALIFIED
    `ts_utc >= ?` and `job_id = ?`; both columns live only on `calls` and the
    only column name the two tables share is `call_id`, which `_cost_filters`
    never names — so it is safe verbatim inside the join, and you must not
    fork, qualify or duplicate it.
  - NEVER RAISE and NEVER CREATE. The new query, like `query_cost`, opens
    read-only, returns an EMPTY report for a ledger file that does not exist,
    and must never bring a database into being or migrate one.
  - Push after EVERY commit. Do NOT create a pull request.
  - The primary checkout satisfies `git status --porcelain` == empty at
    handback. The gate (f) probes run ONLY inside a disposable git worktree
    under `.remedy-wt/`, which you remove and prune before the handback.

C2 — append TEXT-A to `.agent/live_review.md`, one paragraph, after the last
existing line. Its own commit, FIRST after C1b.

===== TEXT-A BEGIN =====
- R-0329 — Low — a manifest value of the wrong TYPE becomes a measured zero in
  the sums T002 is about to build, which is the exact outcome the helper's own
  docstring says it prevents. `_call_segment_row` (`token_ledger.py:1247-1276`)
  checks only that the five `_MANIFEST_KEYS` are PRESENT and then takes their
  values VERBATIM, so a trace line carrying `"chars": "not-a-number"` yields a
  `CallSegmentRow` whose `chars` is that string. SQLite then accepts it:
  `chars INTEGER NOT NULL` is an AFFINITY, not a constraint, so a string that
  does not look like a number is stored AS TEXT and the NOT NULL is satisfied.
  Measured by the reviewer at the R9 gate against a scratch in-memory database:
  `typeof(chars)` prints `text`, and `SUM(chars)` over that row plus one real
  row of 10 prints `10.0`. Both halves of that result matter. The bad row
  contributed 0, which is precisely the "unpublished figure must never become a
  measured zero (P6)" the docstring four lines above the defect forbids; and
  the sum came back a FLOAT, which would move the bytes of any markdown golden
  that renders the same figure as an integer everywhere else — so R11's goldens
  would be pinned to a shape one malformed input can change. It is NOT
  reachable from Remedy's own composer, which publishes real ints through
  `manifest_as_dicts()`; it is registered anyway because the reader's entire
  contract is that it survives ARBITRARY file content, and "our producer is
  well behaved" is not the guarantee that contract makes. Fixed in R10 rather
  than deferred: R10 is the slice that starts SUMming those two columns and is
  therefore the round with a legitimate reason to open that helper, so fixing
  it here mixes nothing that does not already belong to the change. The R9
  round as a whole is PASS. The reviewer re-ran gates (a) through (i) and every
  value matched the handback: cmp exit 0 with sha256
  c5c5bc40c103ce743a81156078a727231460fe321be65e87613e2dc0265244b6 over both
  copies, the five live-review counts 1/1/9/3/1, the six `token_ledger.py`
  counts 1/1/1/4/2/3, ruff `All checks passed!` and the import exit 0, zero
  changed lines assigning a `BackfillResult` counter and zero inside its class
  body, `92 passed` and `41 passed`, canary `42 passed`, `wc -l .agent/plan.md`
  38, an empty porcelain, 28 changed paths with no `.remedy-wt/**` among them,
  and 0/0 against origin. The red-proof was RE-RUN INDEPENDENTLY by the
  reviewer in its own disposable worktree rather than accepted from the report:
  mutating `segment_rows_from_trace_file` to `return []` reproduced `5 failed,
  87 passed` and the same five test ids the handback names, and the worktree
  was removed and pruned with `git worktree list` left showing one line. OPEN.
===== TEXT-A END =====

C3 — `packages/orchestration/token_ledger.py`, the type guard. One commit,
together with the ONE test named at the end of this item.

  (i) REWRITE pair. FROM, the three lines at `token_ledger.py:274-276`:

===== TEXT-B-FROM BEGIN =====
# The manifest keys a trace entry publishes, in the order the columns above take
# them. Named once so a missing key is detected rather than defaulted to zero.
_MANIFEST_KEYS = ("name", "rank", "sha256", "chars", "tokens_estimated")
===== TEXT-B-FROM END =====

      TO, applied byte for byte:

===== TEXT-B BEGIN =====
# The manifest keys a trace entry publishes, in the order the columns above take
# them, each mapped to the type it must ALREADY be. Presence was never enough:
# ``chars INTEGER NOT NULL`` is a SQLite AFFINITY rather than a constraint, so a
# string that does not look like a number is stored as TEXT, satisfies NOT NULL,
# and then counts as 0 in every SUM over that column — the measured zero this
# module exists to refuse (R-0329). ``bool`` is excluded from ``int`` explicitly
# because it is a subclass of it and no manifest ever publishes a flag as a size.
_MANIFEST_KEY_TYPES: dict[str, type] = {
    "name": str,
    "rank": int,
    "sha256": str,
    "chars": int,
    "tokens_estimated": int,
}

# Derived, never restated: one spelling of the key order for the whole module.
_MANIFEST_KEYS = tuple(_MANIFEST_KEY_TYPES)
===== TEXT-B END =====

  (ii) REWRITE pair inside `_call_segment_row`. FROM, the two lines at
       `token_ledger.py:1262-1263`:

===== TEXT-C-FROM BEGIN =====
    if any(key not in manifest_entry for key in _MANIFEST_KEYS):
        return None
===== TEXT-C-FROM END =====

       TO, applied byte for byte:

===== TEXT-C BEGIN =====
    for key, expected in _MANIFEST_KEY_TYPES.items():
        if key not in manifest_entry:
            return None
        value = manifest_entry[key]
        if expected is int and isinstance(value, bool):
            return None
        if not isinstance(value, expected):
            return None
===== TEXT-C END =====

  (iii) Extend that helper's docstring so it states the TYPE rule as well as the
        presence rule, in your own words and the file's idiom: a value of the
        wrong type is skipped exactly like a missing key, and nothing is ever
        coerced. Keep the existing P6 sentence. This is the only prose you
        author in C3.

  (iv) ONE test appended to the existing `TestCallSegmentsWriter` class in
       `tests/orchestration/test_token_ledger.py`: a manifest dict whose `chars`
       is the string `"not-a-number"` is SKIPPED while a well-formed sibling in
       the same manifest survives, and a dict whose `tokens_estimated` is `True`
       is skipped too. Drive the real `segment_rows_from_trace_file` over a real
       JSONL file, as the class's existing tests do. Nothing raises.

C4 — `packages/orchestration/token_ledger.py`, the aggregation query. One
commit. Place it directly after `merge_cost_reports` so the query surface stays
in one region of the file.

  (i) `@dataclass class SegmentShareRow` — one segment kind's share:
      `segment_name: str`, `calls: int`, `segments: int`, `chars: int`,
      `tokens_estimated: int`. Its docstring states WHY these are plain ints and
      not the nullable figures `CostRow` carries: every value column of
      `call_segments` is declared NOT NULL, so a row that EXISTS always has a
      real figure, and the absence this feature has to report is the absence of
      the ROW — which is what `unattributed_calls` counts. That is a different
      shape of honesty from `CostRow`'s, not a departure from it.

  (ii) `@dataclass class SegmentShareReport` — `rows: list[SegmentShareRow]`,
       `attributed_calls: int`, `unattributed_calls: int`, `total_segments: int`,
       `total_chars: int`, `total_tokens_estimated: int`, plus the same
       provenance echo `CostReport` carries: `since`, `job_id`, `project_id`,
       `ledger_path`, `ledger_exists`. All counters default to 0 and `rows` to
       an empty list.

  (iii) `query_segment_shares(*, project_id=None, path=None, since=None,
        job_id=None) -> SegmentShareReport`. Contract, all of which C5 pins:
        - READ-ONLY through `_connect_readonly`, target through
          `_resolve_ledger_path`, filters through `_cost_filters`. It never
          creates a database, never migrates one, and returns an empty report
          with `ledger_exists=False` when the file is absent.
        - TWO statements, both under the SAME `_cost_filters` clause and params.
          Statement one groups the join `calls` → `call_segments` on `call_id`
          by `segment_name`, selecting `COUNT(DISTINCT call_id)`, `COUNT(*)`,
          `SUM(chars)` and `SUM(tokens_estimated)`. Statement two counts
          attribution over `calls` LEFT JOINed to
          `(SELECT DISTINCT call_id FROM call_segments)`: `COUNT(*)` is every
          call in the period and `COUNT(<the joined call_id>)` is the attributed
          subset, because COUNT ignores NULLs. Use COUNT and not SUM for both,
          for the reason `_cost_bucket_rows`'s docstring already gives: a count
          of nothing IS 0, while a sum of nothing is NULL.
        - `unattributed_calls` is the difference of those two counts.
        - ROW ORDER IS DETERMINISTIC, because R11 pins golden bytes against it:
          `tokens_estimated` DESC, then `segment_name` ASC as the tie-break.
        - The three totals are computed IN PYTHON as sums over `rows`, not by a
          third statement. State the reason in the docstring: it makes the
          Acceptance property "segment shares sum to the attributed total" true
          BY CONSTRUCTION instead of by two statements that could drift.
        - A one-line WHY comment sits directly above the definition.

  (iv) Add the three new public names to the `Public API::` block in the module
       docstring, in the file's existing style, beside `query_cost`.

C5 — append SIX test functions to `tests/orchestration/test_token_ledger.py` in
ONE new class, in the file's existing idiom, reusing its tmp-path ledger and
evidence fixtures; never touch the user's data root. Exactly six functions, no
`parametrize`. Build ledger state by running the REAL `backfill_ledger` over a
real evidence tree wherever a call row is needed — do not hand-write ledger rows
with raw SQL. What each must prove:
  1. Shares group by `segment_name` over a ledger holding more than one segment
     kind, in the ordered sequence (`tokens_estimated` DESC, `segment_name`
     ASC), with each row's four figures equal to the values the fixture
     published. Assert the full list of rows, not a length.
  2. A call that owns NO segment rows — the pre-F115 shape — is counted in
     `unattributed_calls` and contributes nothing to any share row, while a call
     that owns them is counted in `attributed_calls`.
  3. INTERNAL CONSISTENCY, the feature's own Acceptance line: the sums of
     `segments`, `chars` and `tokens_estimated` across `rows` equal the report's
     three totals, AND `attributed_calls + unattributed_calls` equals
     `query_cost(...).total.calls` over the SAME filters.
  4. `since` and `job_id` narrow the share rows AND the two attribution counts
     together — a call filtered out of the period is in neither.
  5. A ledger file that does not exist yields `ledger_exists` False, empty
     `rows`, zero counters, and NO file is created at that path.
  6. READ-ONLY, the Acceptance's "report generation touches nothing": capture
     the ledger file's bytes before the call and assert they are identical
     after, and assert that no `-wal` or `-shm` file is left beside it.
Each test's name says what it proves, in the file's naming idiom. Own commit.

C6 — rewrite `.agent/plan.md` in full and rewrite `.agent/handoff.md`, and
append the `Landed: R-0329` line to `.agent/live_review.md`. One commit.
`.agent/plan.md` keeps `## Goal` and `## Next Steps`, stays under 50 lines, and
its Next Steps read: (1) R11 — the pure renderer over `query_segment_shares` and
`query_cost`, markdown and json, with the golden PAIR on disk following
`packages/orchestration/gauntlet_matrix.py`; (2) T003 — `remedy stats report`
CLI, `--until`, prior-period comparison, json schema, and the docs page the new
user-visible behaviour will need; (3) integration gate
(docs/agents/integration_gate.md); (4) closure per
docs/roadmap/STATUS_closure_protocol.md. Last reviewed SHA is 22f3e716 (R9
PASS). Next free finding ID: R-0330. Open findings: 6 — R-0320, R-0322, R-0323,
R-0324, R-0327, R-0328, with R-0329 landed and awaiting the R10 gate. The
Fortschritt line, verbatim, as the file's last line:

Fortschritt: 66 % (T001 ✅ · T002-Query ✅ · T002-Renderer · T003 offen) — Schätzung

Done when: every command RUN for real, its TRUE output recorded — a guessed,
           expected or remembered value is a finding. Record exit codes.
  a. `cmp .agent/authored/f115-r10-1.md .agent/last_block.md` exits 0; record
     `sha256sum` of both and `wc -lc` of the authored file. Then prove the three
     authored slices were applied and not retyped: for TEXT-A, TEXT-B and
     TEXT-C, extract the slice from the SAVED authored file and `cmp` it against
     the corresponding region of the file it was applied to. Record each exit
     code. A proof computed against a retyped copy is a false verification claim.
  b. After C2, over `.agent/live_review.md`: `grep -c '^- R-0329'` = 1 ·
     `grep -c '^- R-0'` = 10 (was 9) · `grep -c '^Done:'` = 3 (UNCHANGED) ·
     `grep -c '^## Steps'` = 1.
  c. After C3 and C4, over `packages/orchestration/token_ledger.py`, report the
     REAL number for each: `grep -c '_MANIFEST_KEY_TYPES'` (at least 3 — the
     definition, the derived tuple, the loop) · `grep -c '_MANIFEST_KEYS'`
     (at least 3 — the derived definition and its two uses) ·
     `grep -c 'class SegmentShareRow'` = 1 · `grep -c 'class SegmentShareReport'`
     = 1 · `grep -c 'def query_segment_shares'` = 1 ·
     `grep -c '_cost_filters'` (at least 3 — the definition and one use in each
     query) · `grep -c '_connect_readonly'` (at least 3). Then
     `python3 -m ruff check packages/orchestration/token_ledger.py
     tests/orchestration/test_token_ledger.py` prints `All checks passed!` exit
     0, and `python3 -c "import packages.orchestration.token_ledger"` exits 0.
  d. Prove the frozen surface did not move, against the code and not by
     assertion: in `git diff 22f3e716..HEAD -- packages/orchestration/token_ledger.py`
     there is NO changed line inside `def query_cost`, `def record_call`,
     `def backfill_ledger`, `def segment_rows_from_trace_file`,
     `def record_call_segments` or the `_MIGRATIONS` literal. Report how you
     established that, and paste the `_call_segment_row` hunk into the handoff
     so the reviewer reads the guard rather than a claim about it.
  e. `python3 -m pytest tests/orchestration/test_token_ledger.py -q` — the
     measured R9 baseline is `92 passed`; C3 adds one function and C5 adds six,
     so `99 passed` is the derived expectation. Report the REAL number. Then
     `python3 -m pytest tests/cli/test_stats_cost.py -q` — measured baseline
     `41 passed`, and this round adds no test there, so 41 must not move. If
     either real number differs, report the REAL number with the full failure
     output and change nothing to meet a number.
  f. TWO PROBES, in a DISPOSABLE WORKTREE ONLY, after C5 is committed and
     pushed: `git worktree add .remedy-wt/r10-probe HEAD --detach`, and inside
     that worktree ONLY. Probe 1: revert the C3 guard to a presence-only check
     (the TEXT-C-FROM two lines). Probe 2, after undoing probe 1: replace the
     body of `query_segment_shares` with `return SegmentShareReport()`. Run
     `python3 -m pytest tests/orchestration/test_token_ledger.py -q` after each
     and record exactly WHICH test ids failed and HOW MANY, whatever the numbers
     are. These are PROBES, not predictions: do NOT adjust a mutation to reach a
     count, and report a green probe as green — that is a real result about the
     tests, not a failure of the round. Then
     `git worktree remove --force .remedy-wt/r10-probe` and `git worktree
     prune`, and record `git worktree list` afterwards. The primary checkout is
     never mutated for this.
  g. Canary `python3 -m pytest tests/cli/test_golden_path.py -q` — the measured
     baseline is `42 passed`; it must not move.
  h. `wc -l .agent/plan.md` prints a number BELOW 50 — record the real one.
  i. `git status --porcelain` empty ·
     `git diff --name-only 0d6c97aa..HEAD | wc -l` — the TWENTY-EIGHT paths
     present after R9 plus ONE new one (`.agent/authored/f115-r10-1.md`); every
     other path this round touches is already among the 28, so 29 is expected.
     If it is not 29, report the real number and the actual list and change
     nothing. No `.remedy-wt/**` path may appear. Finally
     `git rev-list --left-right --count origin/feature/f115-prompt-cost-report...HEAD`
     prints 0 and 0.
Handback:  completion report + rewrite `.agent/handoff.md`: item-status table
           (C1a, C1b, C2, C3, C4, C5, C6 — each exactly once, status done /
           skipped / deviated with a reason), commit table with real SHAs and
           real insertion counts, changed-files table, every result a-i as a
           REAL measured value including gate (d)'s pasted hunk and gate (f)'s
           two probe results, the open-findings count, the next expected action,
           and the Fortschritt line verbatim. Over 60 lines ⇒ add a
           "Deviations, declared" line naming the real count and the mandated
           content that caused it (AGENTS.md DECISION D15). Declare any command
           you had to rewrite for a shell restriction.
──────────────────────────────────────────────────────────────
