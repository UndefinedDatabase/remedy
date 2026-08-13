── STEP R9/n — F115 Prompt breakdown & cost report · Round 9 ─────────
Goal:        Fill the table R8 created: read the segment manifests out of the
             copied `prompt_trace.jsonl` and write them into `call_segments` on
             the backfill path — where the file demonstrably exists — without
             moving a single `BackfillResult` counter or touching `calls`.
Bundle:      C1a save block · C1b mirror · C2 register R-0327 + R-0328 ·
             C3 the pure trace reader · C4 the writer and its wiring ·
             C5 tests · C6 plan + handback (SESSION END)
Change:      EXACTLY these paths, nothing else:
               .remedy-wt/f115-r9-1.md                    (source, gitignored, NOT committed)
               .agent/authored/f115-r9-1.md               (new, C1a)
               .agent/last_block.md                       (rewrite, C1b)
               .agent/live_review.md                      (C2: append)
               packages/orchestration/token_ledger.py     (C3, C4)
               tests/orchestration/test_token_ledger.py   (C5: append)
               .agent/plan.md                             (C6: full replace)
               .agent/handoff.md                          (C6: rewrite)
Constraints:
  - TEXT-A and TEXT-B are AUTHORED text: apply byte for byte, no rewording, no
    rewrapping, no re-punctuation. Everything else in C3-C5 you author yourself
    to the contracts stated below, in the file's existing idiom.
  - Do NOT write a `Done:` paragraph and do NOT mark anything resolved
    (docs/agents/planner_reviewer_prompt.md §4.4). TEXT-A registers two OPEN
    findings; it resolves nothing. If a fix lands with no authored resolution,
    the only permitted line is `Landed: R-XXXX — <one line>`.
  - Do NOT fix R-0320, R-0322, R-0323, R-0324, R-0327 or R-0328. The first two
    predate or sit outside this branch; the other four are reviewer-arithmetic
    records with no on-disk fix.
  - Do NOT touch `calls`, `CallRecord`, `_CALL_COLUMNS`, `record_call`,
    `call_record_from_evidence`, `verify_ledger`, `query_cost`,
    `merge_cost_reports`, `SCHEMA_VERSION` or ANY existing migration statement.
  - Do NOT touch `pingpong_evidence.py`, `prompt_trace.py`, `prompt_segments.py`,
    `pingpong_loop.py`, `apps/cli/**`, or any test beyond the one C5 names. The
    LIVE hook is deliberately NOT wired this round: it fires before the trace
    file is copied (`pingpong_evidence.py:517-525` vs `:527-536`), so backfill is
    the only path where the file exists. Do not "improve" that.
  - `BackfillResult` is FROZEN BEHAVIOUR. `scanned`, `recorded`, `skipped` and
    `failed` must come out of `backfill_ledger` exactly as they do today for
    every input. A segment read or write that fails is logged and counted as a
    ledger miss and NOTHING else. If you find yourself changing a counter, stop
    and declare it instead.
  - Parse JSON with the file's existing spelling, `strict_loads` from
    `packages.common.strict_json` (already imported at `token_ledger.py:88`),
    not a bare `json.loads`. One spelling per concept (AGENTS.md, Code
    Discoverability Conventions).
  - Never force-push. Never commit on main. Push after EVERY commit (R-0289).
  - Do NOT create a pull request this round.
  - The primary checkout satisfies `git status --porcelain` == empty at
    handback. The gate (f) red-proof runs ONLY inside a disposable git worktree
    under `.remedy-wt/`, which you remove and prune before the handback.

C2 — append TEXT-A to `.agent/live_review.md`, two paragraphs separated by a
blank line, after the last existing line. Its own commit, FIRST after C1b.

===== TEXT-A BEGIN =====
- R-0327 — Low — reviewer gate arithmetic, fifth of its class. R8's gate (e)
  demanded `grep -c` of the literal `        2: (` with EIGHT leading spaces.
  `_MIGRATIONS` is a dict whose KEYS sit at FOUR spaces — `1: (` at
  `token_ledger.py:170` is the shape the reviewer had already read in that same
  session — and the block's own TEXT-E, authored by the reviewer, places `2: (`
  at four spaces too. Real values: the eight-space pattern counts 0, the
  four-space one counts 1, at `token_ledger.py:207`. The eight-space indent
  belongs to the STATEMENT lines INSIDE the tuple, not to the key that opens it.
  The worker measured both, reported the real numbers and changed nothing to
  meet the ordered one — the correct behaviour, and it cost the round nothing
  because the gate asked for real values. Nothing on disk is wrong, so there is
  no fix; it is registered so the class stays countable. After R-0282, R-0321,
  R-0323 and R-0324. The standing counter-measure is already on disk as
  checklist item 8 (`docs/agents/planner_reviewer_prompt.md`): compute a gate's
  expected value from the code that PRODUCES it. Here that code was the block's
  OWN authored replacement text, four lines below the gate that miscounted it —
  the shortest distance any instance of this class has yet had. OPEN.

- R-0328 — Low — the R8 red-proof under-predicted its own blast radius. Gate (g)
  stated "Tests 1, 2 and 3 assert the table exists, so they MUST fail". The real
  result, with migration step 2 deleted in a disposable worktree, was `8 failed,
  78 passed`: all FOUR new tests — the fourth,
  `test_a_pre_f115_call_owns_no_segment_rows`, on `sqlite3.OperationalError: no
  such table: call_segments`, because its assertion SELECTs from that very table
  and the same block authored that assertion — plus four pre-existing
  `TestOpenLedger` tests that pin the version constant against the last
  migration step. The ordered COLOUR was right and the round went red exactly as
  required; what was wrong was the COUNT. An under-counted red-proof invites a
  worker either to doubt a correct result or to trim the mutation until the
  prediction fits, and neither is a thing a gate should tempt anyone into.
  Checklist item 5 governs a red-proof's REACHABILITY; this is its arithmetic
  sibling and the first recorded instance. No on-disk fix: the round's evidence
  is correct and more complete than the gate that asked for it. A welcome
  by-product of the over-shoot: `test_schema_version_matches_the_last_migration_step`
  already pins `SCHEMA_VERSION` to the highest `_MIGRATIONS` key, so a version
  bump without its step, or a step without its bump, cannot pass today. OPEN.
===== TEXT-A END =====

C3 — `packages/orchestration/token_ledger.py`, the PURE reader. One commit.

  (i) Add `_PROMPT_TRACE_FILENAME = "prompt_trace.jsonl"` beside the existing
      filename constants at `token_ledger.py:118-120`, with a one-line WHY
      comment directly above it naming that this is the copy the evidence
      exporter places in the task-run directory (`pingpong_evidence.py:533`).

  (ii) Apply TEXT-B verbatim, placed immediately after the `CallRecord`
       dataclass and its helpers, before `BackfillResult`.

===== TEXT-B BEGIN =====
# Column order restated once, exactly as migration step 2 declares it, so the
# INSERT and every later SELECT are built from ONE source and cannot drift.
_CALL_SEGMENT_COLUMNS = (
    "call_id",
    "trace_seq",
    "segment_name",
    "segment_rank",
    "segment_sha256",
    "chars",
    "tokens_estimated",
)

# The manifest keys a trace entry publishes, in the order the columns above take
# them. Named once so a missing key is detected rather than defaulted to zero.
_MANIFEST_KEYS = ("name", "rank", "sha256", "chars", "tokens_estimated")


@dataclass(frozen=True)
class CallSegmentRow:
    """One segment of one composed prompt, as the ledger stores it.

    Mirrors ``ComposedPrompt.manifest_as_dicts()`` one field per key
    (``prompt_segments.py:107-121``) plus two identity columns: the ledger row's
    ``call_id``, and ``trace_seq`` — the zero-based position of the trace line
    among THAT TASK RUN's entries, which is what makes a re-read of the same
    static file produce the same keys and a repeat backfill a no-op.

    A trace entry whose ``segment_manifest`` is empty produces NO row at all.
    That absence is what the report renders as unattributed; it is never a zero,
    and no row is ever invented to stand in for it.
    """

    call_id: str
    trace_seq: int
    segment_name: str
    segment_rank: int
    segment_sha256: str
    chars: int
    tokens_estimated: int
===== TEXT-B END =====

  (iii) Add `segment_rows_from_trace_file(trace_path, *, call_id, task_id) ->
        list[CallSegmentRow]`. Contract, all of which C5 must pin:
        - PURE AND READ-ONLY: opens nothing but the given path, writes nothing,
          creates no database.
        - NEVER RAISES, for any input. A path that does not exist returns `[]`.
          A line that is not valid JSON (`StrictJsonError`) is skipped and the
          scan continues. A blank line is skipped and does NOT consume an index.
        - Keeps only entries whose `task_id` equals the `task_id` argument. The
          copied file is the WHOLE JOB's trace, not that task's
          (`prompt_trace.py:200-204`), so this filter is load-bearing, not
          defensive.
        - `trace_seq` is the zero-based index AMONG THE KEPT entries, assigned
          in file order. An entry with an empty or absent `segment_manifest`
          STILL CONSUMES its index — the number means "position among this task
          run's provider calls", so it stays stable when a later round makes
          more calls carry manifests.
        - Each dict in an entry's `segment_manifest` becomes one row, taking its
          five values from `_MANIFEST_KEYS` in that order. A manifest dict
          MISSING any of the five keys is SKIPPED — never defaulted to 0 or "".
        - A one-line WHY comment sits directly above the definition.

C4 — `packages/orchestration/token_ledger.py`, the WRITER and its wiring. One
commit.

  (i) Add `record_call_segments(rows, *, project_id=None, path=None) -> bool`,
      modelled on `record_call`'s discipline (`token_ledger.py:395-458`):
      - `INSERT OR IGNORE INTO call_segments (...) VALUES (...)` built from
        `_CALL_SEGMENT_COLUMNS`, via one `executemany` and one commit.
      - Idempotent by the table's own primary key: a repeat inserts nothing and
        still returns True.
      - An EMPTY `rows` returns True WITHOUT opening the ledger, so a task run
        with no manifests never creates a database file.
      - NEVER RAISES. On any failure it logs at ERROR, increments the existing
        miss counter through `_count_ledger_miss()`, and returns False.
      - Closes its connection in a `finally`, as `record_call` does.

  (ii) Wire it into `backfill_ledger` (`token_ledger.py:610-657`): after
       `record_call(...)` has returned True and `result.recorded` has been
       incremented, read `task_dir / _PROMPT_TRACE_FILENAME` through
       `segment_rows_from_trace_file(..., call_id=record.call_id,
       task_id=task_dir.name)` and pass the rows to `record_call_segments` with
       the same `project_id` / `path`. Its return value is NOT branched on and
       NO `BackfillResult` counter moves either way. Add a short comment saying
       why backfill is the only wired path — the live hook runs before the copy.

  (iii) Add the three new public names to the `Public API::` block in the module
        docstring, in the file's existing style, beside `record_call`.

C5 — append SIX test functions to `tests/orchestration/test_token_ledger.py`, in
one new class, in the file's existing idiom (reuse its tmp-path ledger fixture;
never touch the user's data root). Exactly six functions, no `parametrize`.
Build the trace fixtures by WRITING REAL JSONL LINES whose shape you copy from
`packages/orchestration/prompt_trace.py` — do not import a private helper. What
each must prove:
  1. Rows come out of a real two-entry trace file in FILE ORDER, with
     `trace_seq` 0 then 1, and each row's five value fields equal to the
     manifest dict they came from. Assert the full list, not a length.
  2. An entry with an EMPTY `segment_manifest` yields no rows but STILL CONSUMES
     its index: a file whose first entry has no manifest and whose second has
     one produces rows carrying `trace_seq` 1, never 0.
  3. Entries belonging to a DIFFERENT `task_id` are ignored — the copied file is
     the whole job's trace.
  4. Robustness, in one test: a path that does not exist returns `[]`; a file
     containing one malformed line between two good ones yields the two good
     entries' rows; and a manifest dict missing one of the five keys is skipped
     while its siblings survive. Nothing raises.
  5. `record_call_segments` is IDEMPOTENT: writing the same rows twice leaves
     `SELECT COUNT(*) FROM call_segments` equal to the row count, and both calls
     return True. Also assert that an empty row list returns True and creates no
     ledger file at a path that does not yet exist.
  6. END TO END through `backfill_ledger`: an evidence tree with one task run
     that has BOTH `provider_evidence.json` and a `prompt_trace.jsonl` carrying a
     manifest ends with `call_segments` rows whose `call_id` equals the `calls`
     row's, AND `BackfillResult`'s four counters are exactly what the same tree
     produces with the trace file absent. Assert the counters as the frozen
     behaviour they are.
Each test's name says what it proves, in the file's naming idiom. Own commit.

C6 — rewrite `.agent/plan.md` in full and rewrite `.agent/handoff.md`. One
commit. `.agent/plan.md` keeps `## Goal` and `## Next Steps`, stays under 50
lines, and its Next Steps read: (1) T002 — aggregation queries over
`calls` joined to `call_segments` plus the pure renderer with markdown/json
goldens, following `gauntlet_matrix.py` and the fixture-ledger pattern at
`tests/cli/test_stats_cost.py:49-128`; (2) T003 — `remedy stats report` CLI,
prior-period comparison, json schema; (3) integration gate
(docs/agents/integration_gate.md); (4) closure per
docs/roadmap/STATUS_closure_protocol.md. Last reviewed SHA is 8615259b (R8
PASS). Next free finding ID: R-0329. Open findings: 6 — R-0320, R-0322, R-0323,
R-0324, R-0327, R-0328. The Fortschritt line, verbatim, as the file's last line:

Fortschritt: 58 % (T001-Schema ✅ · T001-Writer ✅ · T002 · T003 offen) — Schätzung

Done when: every command RUN for real, its TRUE output recorded — a guessed,
           expected or remembered value is a finding. Record exit codes.
  a. `cmp .agent/authored/f115-r9-1.md .agent/last_block.md` exits 0; record
     `sha256sum` of both and `wc -lc` of the authored file.
  b. After C2, over `.agent/live_review.md`: `grep -c '^- R-0327'` = 1 ·
     `grep -c '^- R-0328'` = 1 · `grep -c '^- R-0'` = 9 (was 7) ·
     `grep -c '^Done:'` = 3 (UNCHANGED) · `grep -c '^## Steps'` = 1.
  c. After C3 and C4, over `packages/orchestration/token_ledger.py`:
     `grep -c 'class CallSegmentRow'` = 1 ·
     `grep -c 'def segment_rows_from_trace_file'` = 1 ·
     `grep -c 'def record_call_segments'` = 1 ·
     `grep -c '_CALL_SEGMENT_COLUMNS'` — report the REAL number; it is at least
     2 (the definition plus the INSERT) · `grep -c '_PROMPT_TRACE_FILENAME'` —
     REAL number, at least 2 (the constant plus its use in `backfill_ledger`) ·
     `grep -c 'record_call_segments'` — REAL number, at least 3 (the definition,
     the docstring API line, the call in `backfill_ledger`). Then
     `python3 -m ruff check packages/orchestration/token_ledger.py` prints
     `All checks passed!` exit 0, and
     `python3 -c "import packages.orchestration.token_ledger"` exits 0.
  d. Prove `BackfillResult` did not move, against the code and not by assertion:
     `git diff 8615259b..HEAD -- packages/orchestration/token_ledger.py` must
     show NO changed line inside the `class BackfillResult` body and no changed
     line that assigns `result.scanned`, `result.recorded`, `result.skipped` or
     `result.failed`. Paste the `backfill_ledger` hunk into the handoff so the
     reviewer reads the seam rather than a claim about it.
  e. After C5: `python3 -m pytest tests/orchestration/test_token_ledger.py -q`.
     The measured R8 baseline is `86 passed in 6.15s`; six added functions make
     `92 passed` the expected line. Then
     `python3 -m pytest tests/cli/test_stats_cost.py -q` — measured baseline
     `41 passed in 0.48s`, and this round adds no test there, so 41 must not
     move. If either real number differs, report the REAL number with the full
     failure output and change nothing to meet a number.
  f. RED-PROOF, in a DISPOSABLE WORKTREE ONLY, after C5 is committed and pushed:
     `git worktree add .remedy-wt/r9-redproof HEAD --detach`, and inside that
     worktree ONLY, replace the body of `segment_rows_from_trace_file` with a
     bare `return []`, then run
     `python3 -m pytest tests/orchestration/test_token_ledger.py -q` there.
     This is a PROBE, not a prediction: record exactly which test ids failed and
     how many, whatever the number is. Do NOT adjust the mutation to reach a
     count. Then `git worktree remove --force .remedy-wt/r9-redproof` and
     `git worktree prune`, and record `git worktree list` afterwards. The
     primary checkout is never mutated for this.
  g. Canary `python3 -m pytest tests/cli/test_golden_path.py -q` — the measured
     baseline is `42 passed`; it must not move.
  h. `wc -l .agent/plan.md` prints a number BELOW 50 — record the real one.
  i. `git status --porcelain` empty ·
     `git diff --name-only 0d6c97aa..HEAD | wc -l` — the TWENTY-SEVEN paths
     present after R8 plus ONE new one (`.agent/authored/f115-r9-1.md`); every
     other path this round touches is already among the 27, so 28 is expected.
     If it is not 28, report the real number and the actual list and change
     nothing. No `.remedy-wt/**` path may appear. Finally
     `git rev-list --left-right --count origin/feature/f115-prompt-cost-report...HEAD`
     prints 0 and 0.
Handback:  completion report + rewrite `.agent/handoff.md`: item-status table
           (C1a, C1b, C2, C3, C4, C5, C6 — each exactly once, status done /
           skipped / deviated with a reason), commit table with real SHAs and
           real insertion counts, changed-files table, every result a-i as a
           REAL measured value including gate (d)'s pasted hunk, the
           open-findings count, the next expected action, and the Fortschritt
           line verbatim. Over 60 lines ⇒ add a "Deviations, declared" line
           naming the real count and the mandated content that caused it
           (AGENTS.md DECISION D15). Declare any command rewritten for the `$`
           restriction.

           THIS IS THE LAST ROUND OF THE SESSION. The handoff is the only return
           channel: whoever resumes reads it and nothing else from this session.
           Its "Resume here" section names T002 as the next work, points at the
           fixture-ledger and golden patterns `.agent/f115_inventory.md` section
           "## Q7" already lists, and states plainly that no PR exists yet and
           that closure has not started.
──────────────────────────────────────────────────────────────
