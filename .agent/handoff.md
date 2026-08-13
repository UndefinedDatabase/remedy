# Handoff — F115 Prompt breakdown & cost report · Round 10

Branch `feature/f115-prompt-cost-report`, HEAD after C6. No PR created.
Deviations, declared: this file is over 60 lines (AGENTS.md DECISION D15).
The cause is the mandated content — the item-status table, the commit and
changed-files tables, nine gate results a-i measured individually, gate (d)'s
pasted hunk and gate (f)'s two probe results. No section is dropped.

## Item status
| Item | Status   | Reason |
|------|----------|--------|
| C1a  | done     | |
| C1b  | done     | |
| C2   | done     | |
| C3   | done     | one deviation inside (iv), below |
| C4   | deviated | placement split, below |
| C5   | done     | |
| C6   | done     | |

C3 (iv) deviation: the class's `_trace_entry` helper derives
`segment_manifest_chars` by summing the manifest's `chars`, which a
non-numeric value cannot survive (`TypeError` in the FIXTURE, not the code
under test). Rather than edit that shared helper, the test builds the entry
with a well-formed manifest and swaps the bad manifest in afterwards, so the
JSONL on disk still carries the bad values verbatim. The real
`segment_rows_from_trace_file` is still what reads the file.

C4 deviation: the block says "Place it directly after `merge_cost_reports`".
`query_segment_shares` IS directly after `merge_cost_reports`. The two
dataclasses sit with `CostRow`/`CostReport` in the file's dataclass region
instead, because that is where this module puts every result type and where a
reader searching for one lands. Declared rather than assumed.

## Commits
| SHA | Item | Subject | Insertions |
|-----|------|---------|-----------|
| 491c19ae | C1a | save the R10 authored step block | 322 |
| b2cab277 | C1b | mirror the R10 block into last_block | 270 (single-state-file rewrite) |
| a3e9eb61 | C2 | register R-0329 from the R9 gate | 37 |
| fa0a39bb | C3 | type-check manifest values before they become ledger rows | 61 |
| 2008a2cb | C4 | add the per-segment share aggregation query | 155 |
| 665432b3 | C5 | pin the segment share query, its order and its honesty | 178 |
| 5b1e0bea | C6 | refresh the plan and write the R10 handoff | 191 |
| (this one) | C6 | fill C6's own SHA into the table above | ~2 |

The last row is a SEVENTH commit, declared: C6's own SHA cannot exist inside
C6, and the block mandates real SHAs in this table. It touches only
`.agent/handoff.md`, a C6 path, and rewrites no history.

## Changed files
| Path | Items |
|------|-------|
| .agent/authored/f115-r10-1.md | C1a (new) |
| .agent/last_block.md | C1b |
| .agent/live_review.md | C2, C6 |
| packages/orchestration/token_ledger.py | C3, C4 |
| tests/orchestration/test_token_ledger.py | C3, C5 |
| .agent/plan.md | C6 |
| .agent/handoff.md | C6 |

Nothing else. No renderer, no CLI, no migration, no `cost_report.py`.

## Gates — every value measured, none derived
(a) `cmp .agent/authored/f115-r10-1.md .agent/last_block.md` exit **0**.
    sha256 of BOTH: `93a5a6347496a811cb9887d64f9d2312c42824537df592cd1ad6a846fc5f8731`.
    `wc -lc` authored: **322 20573**.
    Slice proofs — each slice cut out of the SAVED authored file and `cmp`ed
    against the region of the file it was applied to:
    TEXT-A → `.agent/live_review.md` exit **0**, 1 occurrence;
    TEXT-B → `token_ledger.py` exit **0**, 1 occurrence;
    TEXT-C → `token_ledger.py` exit **0**, 1 occurrence.
    Script: `.remedy-wt/f115_r10_gate_a.py` (gitignored).
(b) `.agent/live_review.md`: `^- R-0329` = **1** · `^- R-0` = **10** ·
    `^Done:` = **3** (unchanged) · `^## Steps` = **1**.
(c) `token_ledger.py`: `_MANIFEST_KEY_TYPES` = **4** · `_MANIFEST_KEYS` = **4** ·
    `class SegmentShareRow` = **1** · `class SegmentShareReport` = **1** ·
    `def query_segment_shares` = **1** · `_cost_filters` = **4** ·
    `_connect_readonly` = **3**. ruff over both files: **All checks passed!**,
    exit 0. `python3 -c "import packages.orchestration.token_ledger"` exit **0**.
(d) Established MECHANICALLY, not by assertion (`.remedy-wt/f115_r10_gate_d.py`):
    the script parses `git diff 22f3e716..HEAD --unified=0` with line numbers,
    maps every `-` line to its BASE line number and every `+` line to its HEAD
    line number, computes each frozen definition's top-level span in the version
    it belongs to, and intersects. Frozen spans (base → head): `query_cost`
    924-985 → 996-1057 · `record_call` 470-533 → 542-605 · `backfill_ledger`
    782-847 → 854-919 · `segment_rows_from_trace_file` 659-717 → 731-789 ·
    `record_call_segments` 721-778 → 793-850 · `_MIGRATIONS` 181-229 → 184-232.
    Changed base lines: **5** — 275, 276, 1253, 1262, 1263. Changed head lines:
    **189**. **VIOLATIONS: none.** The `_call_segment_row` hunk, verbatim:

        -    """One manifest dict as a row, or None when it does not carry all five keys.
        +    """One manifest dict as a row, or None unless all five keys are there AND typed.

             A dict missing a key is SKIPPED rather than completed with 0 or "": the
             values are taken verbatim from ``_MANIFEST_KEYS`` and nothing here invents,
             coerces or defaults one. An unpublished figure must never become a measured
             zero (P6), and a partial manifest row would be exactly that.
        +
        +    A value of the WRONG TYPE is skipped by exactly the same rule, because it
        +    reaches the same end by a longer route: ``chars INTEGER NOT NULL`` is a
        +    SQLite affinity rather than a constraint, so a non-numeric string is stored
        +    as TEXT, satisfies NOT NULL, and then counts as 0 in every SUM over that
        +    column. ``_MANIFEST_KEY_TYPES`` names the type each key must ALREADY be, and
        +    a value that is not it makes the whole dict a skip. Nothing is cast on the
        +    way past: a figure this module cannot verify is one it declines to store,
        +    not one it repairs.
             """
             if not isinstance(manifest_entry, dict):
                 return None
        -    if any(key not in manifest_entry for key in _MANIFEST_KEYS):
        -        return None
        +    for key, expected in _MANIFEST_KEY_TYPES.items():
        +        if key not in manifest_entry:
        +            return None
        +        value = manifest_entry[key]
        +        if expected is int and isinstance(value, bool):
        +            return None
        +        if not isinstance(value, expected):
        +            return None
             name, rank, sha256, chars, tokens_estimated = (
                 manifest_entry[key] for key in _MANIFEST_KEYS
             )

(e) `pytest tests/orchestration/test_token_ledger.py -q` → **99 passed**
    (R9 baseline 92 + 1 from C3 + 6 from C5; the derived expectation was met, and
    the number above is the one the run printed).
    `pytest tests/cli/test_stats_cost.py -q` → **41 passed**, unmoved.
(f) Two probes, disposable worktree `.remedy-wt/r10-probe` at 665432b3, primary
    checkout never mutated.
    Probe 1 — C3 guard reverted to the TEXT-C-FROM presence-only check:
    **1 failed, 98 passed**. The one id:
    `TestCallSegmentsWriter::test_a_wrongly_typed_manifest_value_is_skipped_like_a_missing_key`.
    Probe 2 — after `git checkout --` undid probe 1 (porcelain empty), the body
    of `query_segment_shares` replaced by `return SegmentShareReport()`:
    **4 failed, 95 passed**. The four ids, all in `TestQuerySegmentShares`:
    `test_shares_group_by_segment_name_in_the_pinned_row_order`,
    `test_a_call_without_segment_rows_is_unattributed_and_in_no_share_row`,
    `test_the_shares_sum_to_the_totals_and_the_calls_match_query_cost`,
    `test_since_and_job_id_narrow_the_rows_and_both_attribution_counts`.
    Reported as measured: the OTHER TWO of the six stayed GREEN under that
    mutation, and honestly so — `test_a_missing_ledger_...` asserts an empty
    report and no file created, and `test_the_report_changes_no_byte_...`
    asserts nothing was written, and a stub satisfies both by doing nothing.
    They pin absence guarantees, which a do-nothing body cannot violate. No
    mutation was adjusted to reach a count.
    Cleanup: `git worktree remove --force` + `git worktree prune`;
    `git worktree list` afterwards is ONE line — `/home/decodeux/Repos/remedy
    665432b3 [feature/f115-prompt-cost-report]`.
(g) Canary `pytest tests/cli/test_golden_path.py -q` → **42 passed**, unmoved.
(h) `wc -l .agent/plan.md` → **41** (below 50).
(i) `git status --porcelain` → **NOT empty**: one line, `?? .agent/STOP`.
    Real output, not routed around. That file — 0 bytes, mtime 09:09 — appeared
    DURING this round; the porcelain was empty at C1a and at every commit
    through C5, and no command of this round creates it. It is the operator's
    G6 stop signal (docs/agents/self_drive_protocol.md:104), so the round did
    what G6 says: finished the commit already half-written (C6) and handed off.
    It was NOT deleted (an operator's signal is not the worker's to clear) and
    NOT committed (it is not among the block's permitted paths). Every path this
    round wrote is committed; the working tree is otherwise clean.
    `git diff --name-only 0d6c97aa..HEAD | wc -l` → **29**, exactly the 28 after
    R9 plus `.agent/authored/f115-r10-1.md`. No `.remedy-wt/**` path among them.
    `git rev-list --left-right --count origin/...HEAD` → **0  0**.

Shell rewrites, declared: this environment's bash refused three command forms —
a chained `cmd ; echo "exit=$?"`, a `cat <<'PY'` heredoc containing an f-string
brace, and a `sed -n '/re/,/re/p'` range. The `cmp`/`grep` gates were therefore
run one command per invocation with the exit code read from the tool result, and
gates (a) and (d) were run from the two named scripts under gitignored
`.remedy-wt/`. No gate was weakened, skipped or substituted.

Open findings: **6** — R-0320, R-0322, R-0323, R-0324, R-0327, R-0328.
R-0329 is landed (fa0a39bb) and awaits this round's gate; no `Done:` paragraph
was written and nothing was marked resolved.

Next expected action: the R10 gate, then R11 — the pure renderer over
`query_segment_shares` and `query_cost` with its markdown/json golden pair.
Before R11 the operator's `.agent/STOP` has to be cleared or acknowledged; the
round ended at it rather than through it.

Fortschritt: 66 % (T001 ✅ · T002-Query ✅ · T002-Renderer · T003 offen) — Schätzung
