── STEP R8/n — F115 Prompt breakdown & cost report · Round 8 ─────────
Goal:        Decide T001's persistence SHAPE from the R7 inventory and land it as
             SCHEMA ONLY: a per-call `call_segments` table added as migration
             step 2, with `calls`, `CallRecord` and `_CALL_COLUMNS` untouched, so
             pre-F115 rows stay unattributed by construction and no existing row
             can read as ledger drift.
Bundle:      C1a save block · C1b mirror · C2 resolve R-0325 + R-0326 ·
             C3 DECISION F115 D4 into decisions.md · C4 D4 into the feature file ·
             C5 the migration itself · C6 its tests · C7 plan + handback
Change:      EXACTLY these paths, nothing else:
               .remedy-wt/f115-r8-1.md                    (source, gitignored, NOT committed)
               .agent/authored/f115-r8-1.md               (new, C1a)
               .agent/last_block.md                       (rewrite, C1b)
               .agent/live_review.md                      (C2: append)
               .agent/decisions.md                        (C3: append)
               docs/roadmap/features/T2_F115.md           (C4: append)
               packages/orchestration/token_ledger.py     (C5)
               tests/orchestration/test_token_ledger.py   (C6: append)
               .agent/plan.md                             (C7: full replace)
               .agent/handoff.md                          (C7: rewrite)
Constraints:
  - TEXT-A … TEXT-F are AUTHORED text: apply byte for byte, no rewording, no
    rewrapping, no re-punctuation, no slots to substitute. C6's tests are the one
    item you author yourself, to the exact assertions specified.
  - Do NOT write a `Done:` paragraph of your own and do NOT mark anything
    resolved (docs/agents/planner_reviewer_prompt.md §4.4). TEXT-A IS the
    reviewer's resolution text; applying it is C2. If a later fix lands with no
    authored resolution, the only permitted line is
    `Landed: R-XXXX — <one line: what changed, which commit>`.
  - Do NOT fix R-0320, R-0322, R-0323 or R-0324. The first two predate this
    branch; the last two are reviewer-arithmetic records with no on-disk fix.
  - Do NOT touch `calls`, `CallRecord`, `_CALL_COLUMNS`, `record_call`,
    `call_record_from_evidence`, `verify_ledger`, `query_cost` or ANY existing
    migration statement. Migration step 1 is never rewritten — that is the whole
    point of the numbered-step mechanism (`token_ledger.py:166-168`).
  - Nothing WRITES to `call_segments` this round. The table is inert until the
    next round's writer. Do not add a writer, a dataclass, a reader or a CLI flag.
  - Do NOT touch `pingpong_evidence.py`, `prompt_trace.py`, `prompt_segments.py`,
    `pingpong_loop.py`, `apps/cli/**`, or any test beyond the one C6 names.
  - Never force-push. Never commit on main. Push after EVERY commit (R-0289).
  - Do NOT create a pull request this round.
  - The primary checkout must satisfy `git status --porcelain` == empty at
    handback. The gate (g) red-proof runs ONLY inside a disposable git worktree
    under `.remedy-wt/`, which you remove and prune before the handback.

C2 — append TEXT-A to `.agent/live_review.md`, as two paragraphs separated by a
blank line, after the last existing line. Its own commit, FIRST after C1b.

===== TEXT-A BEGIN =====
Done: R-0325 — RESOLVED at the R7 gate. Verified against the disk, not the report: `python3 -m ruff check tests/test_llm_planner.py` prints `All checks passed!` with exit 0 at f20f172a, and `git show dd7feebd` shows the fix is exactly one moved line — the `planner_models` import now sits ABOVE the `prompt_segments` block, one insertion and one deletion in that file and no other file touched. `python3 -m pytest tests/test_llm_planner.py -q` prints `38 passed`, the R6 baseline unmoved, so the reorder changed no behaviour. The four-file ruff sweep the block also ordered prints `All checks passed!` with exit 0.

Done: R-0326 — RESOLVED at the R7 gate. Verified against the RENDERED docstring rather than the source line, because the source line was never the defect: `compose_planner_prompt.__doc__` now contains no backslash-n sequence at all and its sentence reads intact, naming `PROMPT_SEGMENT_DELIMITER` as "the same blank-line separator this module concatenated by hand". `git show cbe38b90` confines the change to that docstring, four insertions and three deletions in `packages/orchestration/llm_planner.py`. The R7 round as a whole is PASS: the reviewer re-ran gates (a) through (i) and every value matched the handback — cmp exit 0 with sha256 c6ab0e7d25c42144af766401daf7a90309dae3736c6c0ba8285a0a6b9942ea00 over both copies, the five live-review counts 1/1/7/1/1, ruff clean over all four files, `38 passed`, the inventory's 1/6/6, canary `42 passed`, `wc -l .agent/plan.md` = 38, an empty `git status --porcelain`, and 24 changed paths with no `.remedy-wt/**` among them. The R7 diff touched only the eight paths its block declared, and the C5 inventory's load-bearing claims were spot-checked against source: thirteen `calls` columns with exactly three NOT NULL and no DEFAULT clause, `grep -rn "ALTER TABLE" --include=*.py .` zero matches, `grep -rn "unattributed" --include=*.py .` zero matches.
===== TEXT-A END =====

C3 — append TEXT-B to `.agent/decisions.md`, after the last existing line,
separated from it by one blank line. Its own commit.

===== TEXT-B BEGIN =====
## DECISION F115 D4 — the manifest gets its own table, not a ledger column (2026-08-13)

Context, from `.agent/f115_inventory.md` section "## T001 persistence inventory
(R7)", every citation re-read by the reviewer at the R8 gate: a `calls` row is
ONE FINALIZED TASK RUN keyed `"<job_id>:<task_id>"` (`token_ledger.py:178-192`,
DECISION F103 D16), while a segment manifest belongs to ONE PROVIDER CALL
(`prompt_trace.py:74-83`). The mapping is one-to-many. Three constraints then
decide the shape rather than merely colour it:

1. `verify_ledger` compares a stored row against a record re-derived from
   evidence by WHOLE-DATACLASS EQUALITY (`token_ledger.py:688-701`), so any
   column added to `_CALL_COLUMNS` must be reproducible by
   `call_record_from_evidence` — or every row reads as drift.
2. The live ledger hook fires BEFORE `prompt_trace.jsonl` is copied into
   `task_runs/<task_id>/`: `_record_finalized_call_in_ledger` at
   `pingpong_evidence.py:517-525`, the copy at `:527-536`. A later backfill
   reads that same tree WITH the file present. An evidence-derived manifest
   column would therefore be NULL live and non-NULL on backfill, which is
   constraint 1 firing on every row the feature cares about.
3. `record_call` writes `INSERT OR IGNORE` (`token_ledger.py:425-428`), which
   never UPDATEs, so a manifest cannot be attached to an existing row later.

Chosen: a NEW table `call_segments`, added as migration step 2, with
`SCHEMA_VERSION` bumped to 2. One row per segment of one composed prompt, its
value columns mirroring `ComposedPrompt.manifest_as_dicts()` one for one
(`prompt_segments.py:107-121` — name, rank, sha256, chars, tokens_estimated),
keyed by the ledger row's `call_id` plus `trace_seq`, the zero-based position of
the trace line within that task run's entries. `calls`, `CallRecord` and
`_CALL_COLUMNS` are not touched, so constraint 1 cannot fire and no existing
row's verify result moves. Backfill tolerance is STRUCTURAL rather than coded: a
pre-F115 row simply has no `call_segments` rows, and "no rows" is what the
report renders as unattributed — never guessed, and never a fabricated zero.

Alternatives considered. (a) An aggregate manifest column on `calls` — rejected
by constraints 1 and 2, and it would squash a one-to-many relation into a single
value, losing exactly the per-segment detail the feature exists to show. (b) A
reference to the trace file — rejected because the row ALREADY carries one:
`evidence_ref` is `"task_runs/<task_id>"` (`token_ledger.py:547-549`), which is
exactly the directory the trace file is copied into (`pingpong_evidence.py:533`),
so the option adds no information the row lacks; and a JSONL path cannot be
aggregated in SQL, which is precisely what T002's queries need.

Scope: this decision lands SCHEMA ONLY. Nothing writes to `call_segments` yet —
the writer is the next round. An inert table is what makes this a separately
reviewable commit rather than a schema change smuggled in beside its consumer.

Reverse by deleting the `2:` entry from `_MIGRATIONS`, restoring the version
constant to 1, and dropping the docstring bullet that names the table. A ledger
already migrated keeps an empty unused table, which no code reads.
===== TEXT-B END =====

C4 — append TEXT-C to `docs/roadmap/features/T2_F115.md`, after the last
existing line, separated by one blank line. Its own commit.

===== TEXT-C BEGIN =====
## T001 persistence shape — DECISION F115 D4 (2026-08-13)

T001's "persist the manifest reference (or the compact manifest itself)
alongside the ledger row" is settled as a SEPARATE TABLE, not a column on
`calls`. A ledger row is one finalized task run; a manifest is one provider
call, so the relation is one-to-many, and `verify_ledger`'s whole-dataclass
equality plus the hook's ordering against the trace-file copy make an
evidence-derived column read as drift on every row. Full reasoning, citations
and the reversal recipe: `.agent/decisions.md`, "DECISION F115 D4".

Consequence for this file's Design section: "Ledger extension (additive
column/table)" resolves to the TABLE reading. The backfill tolerance the same
bullet asks for is structural — a pre-F115 row owns no `call_segments` rows,
and the report renders that absence as unattributed rather than guessing.
===== TEXT-C END =====

C5 — `packages/orchestration/token_ledger.py`. Three authored pairs, ONE commit.
Apply each by locating the FROM bytes exactly once and replacing them with the
TO bytes. Before committing, re-read the whole file and confirm it still parses
(`python3 -c "import packages.orchestration.token_ledger"`).

PAIR 1 — REWRITE (the TO does not contain the FROM).
===== TEXT-D FROM BEGIN =====
SCHEMA_VERSION = 1
===== TEXT-D FROM END =====
===== TEXT-D TO BEGIN =====
SCHEMA_VERSION = 2
===== TEXT-D TO END =====

PAIR 2 — REWRITE (the TO does not contain the FROM: `}` no longer follows
`    ),` directly).
===== TEXT-E FROM BEGIN =====
        "CREATE INDEX IF NOT EXISTS idx_calls_role_model ON calls (role, model)",
    ),
}
===== TEXT-E FROM END =====
===== TEXT-E TO BEGIN =====
        "CREATE INDEX IF NOT EXISTS idx_calls_role_model ON calls (role, model)",
    ),
    # F115 D4: the segment manifest is per PROVIDER CALL while a `calls` row is
    # one finalized TASK RUN, so it gets its own table instead of a column. The
    # value columns mirror ComposedPrompt.manifest_as_dicts() one for one, so a
    # writer never has to invent or rename a field.
    2: (
        """
        CREATE TABLE IF NOT EXISTS call_segments (
            call_id          TEXT NOT NULL,
            trace_seq        INTEGER NOT NULL,
            segment_name     TEXT NOT NULL,
            segment_rank     INTEGER NOT NULL,
            segment_sha256   TEXT NOT NULL,
            chars            INTEGER NOT NULL,
            tokens_estimated INTEGER NOT NULL,
            PRIMARY KEY (call_id, trace_seq, segment_name)
        )
        """,
        "CREATE INDEX IF NOT EXISTS idx_call_segments_call_id ON call_segments (call_id)",
    ),
}
===== TEXT-E TO END =====

PAIR 3 — APPEND-shaped (the TO CONTAINS the FROM verbatim as its opening bytes).
===== TEXT-F FROM BEGIN =====
  finest record the actuals feature puts on disk, and a per-request row would
  have to invent ids, timestamps and a usage split no file records.
===== TEXT-F FROM END =====
===== TEXT-F TO BEGIN =====
  finest record the actuals feature puts on disk, and a per-request row would
  have to invent ids, timestamps and a usage split no file records. F115 D4 adds
  ``call_segments`` BESIDE it rather than widening it — one row per segment of
  one composed prompt, keyed by the row's ``call_id`` plus the trace line's
  position — so the per-call breakdown lives in its own table and ``calls``
  keeps its one-row-per-task-run identity untouched.
===== TEXT-F END =====

C6 — append FOUR test functions to `tests/orchestration/test_token_ledger.py`,
in the file's existing style (follow the surrounding class/fixture conventions
and reuse whatever tmp-path ledger fixture the file already has; do NOT touch
the user's data root). Exactly four functions, no `parametrize`. Their required
assertions, which you must satisfy without weakening:

  1. A FRESH ledger carries the table: `open_ledger` on a tmp path, then
     `SELECT name FROM sqlite_master WHERE type='table' AND name='call_segments'`
     returns a row, and the `meta` row for `SCHEMA_VERSION_KEY` reads `"2"`.
  2. A v1 ledger UPGRADES IN PLACE: open a ledger, then in the same file
     `DROP TABLE call_segments` and set the `meta` `schema_version` value back to
     `"1"`, commit and close; reopen with `open_ledger`; assert the table is
     present again AND the stored version reads `"2"`. This is the test that
     proves the numbered-step mechanism works past step 1 — it has never run
     before in this repository.
  3. The COLUMNS mirror the manifest: `PRAGMA table_info(call_segments)` yields
     exactly the seven names, in this order: `call_id`, `trace_seq`,
     `segment_name`, `segment_rank`, `segment_sha256`, `chars`,
     `tokens_estimated`. Assert the list equality, not a membership check.
  4. BACKFILL TOLERANCE is structural: record one ordinary call through the
     existing `record_call` path into a tmp ledger, then
     `SELECT COUNT(*) FROM call_segments WHERE call_id = ?` for that row's id
     returns 0, while the row itself is present in `calls`. Its docstring states
     in one line that no-rows is what the report renders as unattributed.

Each test's name says what it proves, in the file's existing naming idiom. Its
own commit.

C7 — rewrite `.agent/plan.md` in full and rewrite `.agent/handoff.md`. One
commit. `.agent/plan.md` keeps `## Goal` and `## Next Steps` headings, stays
under 50 lines, and its Next Steps read: (1) the `call_segments` WRITER —
populate from the copied `prompt_trace.jsonl` on the backfill path, where the
file exists, since the live hook runs before the copy; (2) T002 aggregation
queries plus the pure renderer with goldens; (3) T003 CLI, period comparison and
json schema; (4) integration gate, then closure. Last reviewed SHA is f20f172a
(R7 PASS). Next free finding ID: R-0327. Open findings: 4 — R-0320, R-0322,
R-0323, R-0324 (R-0325 and R-0326 are resolved by TEXT-A this round). The
Fortschritt line, verbatim, as the file's last line:

Fortschritt: 50 % (R1 ✅ · T001a ✅ · alle drei Call-Sites ✅ · T001-Shape-Inventar ✅ · T001-Persistenz läuft · T002 · T003 offen) — Schätzung

Done when: every command RUN for real, its TRUE output recorded — a guessed,
           expected or remembered value is a finding. Record exit codes.
  a. `cmp .agent/authored/f115-r8-1.md .agent/last_block.md` exits 0; record
     `sha256sum` of both and `wc -lc` of the authored file.
  b. After C2, over `.agent/live_review.md`: `grep -c '^Done:'` = 3 (was 1) ·
     `grep -c '^- R-0'` = 7 (UNCHANGED — TEXT-A registers no new finding) ·
     `grep -c '^## Steps'` = 1.
  c. After C3: `grep -c '^## DECISION F115 D4' .agent/decisions.md` = 1.
  d. After C4: `grep -c '^## T001 persistence shape' docs/roadmap/features/T2_F115.md`
     = 1.
  e. After C5, over `packages/orchestration/token_ledger.py`:
     `grep -c '^SCHEMA_VERSION = 2'` = 1 · `grep -c '^SCHEMA_VERSION = 1'` = 0 ·
     `grep -c 'CREATE TABLE IF NOT EXISTS call_segments'` = 1 ·
     `grep -c 'idx_call_segments_call_id'` = 1 · `grep -c '        2: ('` = 1.
     Then `python3 -m ruff check packages/orchestration/token_ledger.py` prints
     `All checks passed!` with exit 0, and
     `python3 -c "import packages.orchestration.token_ledger"` exits 0.
  f. After C6: `python3 -m pytest tests/orchestration/test_token_ledger.py -q`.
     The measured R7 baseline is `82 passed in 6.12s`; four added functions make
     `86 passed` the expected line. If the real number differs, report the REAL
     number and the full failure output and change nothing to meet the number.
  g. RED-PROOF, in a DISPOSABLE WORKTREE ONLY. After C6 is committed and pushed:
     `git worktree add .remedy-wt/r8-redproof HEAD`, and inside that worktree
     ONLY, delete the whole `2: (...)` entry from `_MIGRATIONS`, then run
     `python3 -m pytest tests/orchestration/test_token_ledger.py -q` there and
     record the real output. Tests 1, 2 and 3 assert the table exists, so they
     MUST fail; record which ids failed and how many. Then
     `git worktree remove --force .remedy-wt/r8-redproof` and
     `git worktree prune`, and record `git worktree list` afterwards. The
     primary checkout is never mutated for this.
  h. DOCS-ROUND GATE (this round's change set includes docs/roadmap/**):
     `python3 -m pytest tests/docs/ -q` — record the real line and exit code.
  i. Canary `python3 -m pytest tests/cli/test_golden_path.py -q` — the measured
     baseline is `42 passed`; it must not move.
  j. `wc -l .agent/plan.md` prints a number BELOW 50 — record the real one.
  k. `git status --porcelain` empty ·
     `git diff --name-only 0d6c97aa..HEAD | wc -l` — the TWENTY-FOUR paths
     present after R7 plus THREE new ones (`.agent/authored/f115-r8-1.md`,
     `packages/orchestration/token_ledger.py`,
     `tests/orchestration/test_token_ledger.py`); every other path this round
     touches is already among the 24, so 27 is expected. If it is not 27, report
     the real number and the actual list and change nothing. No `.remedy-wt/**`
     path may appear. Finally
     `git rev-list --left-right --count origin/feature/f115-prompt-cost-report...HEAD`
     prints 0 and 0.
Handback:  completion report + rewrite `.agent/handoff.md`: item-status table
           (C1a, C1b, C2, C3, C4, C5, C6, C7 — each exactly once, status done /
           skipped / deviated with a reason), commit table with real SHAs and
           real insertion counts, changed-files table, every result a-k as a
           REAL measured value, the open-findings count, the next expected
           action, and the Fortschritt line verbatim. Over 60 lines ⇒ add a
           "Deviations, declared" line naming the real count and the mandated
           content that caused it (AGENTS.md DECISION D15). Declare any command
           you had to rewrite for the `$` restriction.
──────────────────────────────────────────────────────────────
