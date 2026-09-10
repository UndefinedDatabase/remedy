# Handback — F275 round 42

## Session

SESSION 18 of feature F275 · round 42 · rounds so far 42

Context self-assessment (amend0905-throughput): context is comfortable — this
round read AGENTS.md, the 280-line self-drive protocol, the 105-line handback
template, the 33858-byte block, and the three production seams it had to widen
(`data_paths.py` head, `pingpong_job.py` persistence block, `storage.py`'s
classic contract), and spent the rest of its cost on the ten gate runs rather
than on reading, so there is room for further rounds this session.

F275 stands at 42 rounds and 18 sessions against the operator's soft limit of 60
rounds and 20 sessions (amend0908-f275-finish rule 1), so no scope report is
owed.

## Range

Review of `77a7d840`..`HEAD` — C0a through C4. C4 is the commit that writes this
file, so every gate reading below is taken at C3 `c4cdc4ce` or earlier, and C4's
own numbers are not claimed here.

| Commit | SHA | Subject |
|---|---|---|
| C0a | `9c4f39c6` | save the round 42 step block verbatim |
| C0b | `bc90d257` | mirror the round 42 block into the last-block file |
| C1  | `6e885b61` | the round 42 plan |
| C2  | `03a3048e` | book the round 41 verdict, the flip-enumeration slip and DECISION F275 D23 |
| C3  | `c4cdc4ce` | widen the unified job store with a root override, corruption visibility and listing |
| C4  | this commit | the round 42 handback |

## Commits

### 9c4f39c6 F275 R42 C0a: save the round 42 step block verbatim.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r42.md` | +362/-0 | the block's bytes saved verbatim; 33858 bytes, final byte a newline, sha256 `da92b95ac2d0f35d4ed31f73d31468a5fafc0df2d1560bc55f944e739ef374ed` — the digest the block ordered |

### bc90d257 F275 R42 C0b: mirror the round 42 block into the last-block file.

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +333/-392 | written from `git cat-file blob 9c4f39c6:.agent/authored/f275-r42.md`, never retyped; the churn is the round 41 block it replaces |

### 6e885b61 F275 R42 C1: the round 42 plan.

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +18/-13 | whole-file replacement by the PLAN42 slice, extracted mechanically from the committed block; Current Step is now the widen, Next Steps 1 carries the enumeration gap the slip records |

### 03a3048e F275 R42 C2: book the round 41 verdict, the flip-enumeration slip and DECISION F275 D23.

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-0 | the RECORD42 append — the F275 R41 PASS verdict, booked by this round under amend0827 rule 1 |
| `.agent/prose_slips.md` | +2/-0 | the SLIPS42 append — roughly 1721 of the flip's 3771 declared lines have no committed per-site enumeration; a dated line, not an id |
| `.agent/decisions.md` | +14/-0 | the DECISION42 append — DECISION F275 D23, why the three capabilities are widened in before the flip |

### c4cdc4ce F275 R42 C3: widen the unified job store with a root override, corruption visibility and listing.

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/data_paths.py` | +20/-0 | S1: `job_record_paths(root=None) -> list[Path]`, placed directly above `job_evidence_dir` so it sits beside `job_record_path`; globs `*/job.json` under `jobs_dir(root)`, returns `[]` for an absent store, sorted by path. One WHY comment and one line added to the module's Public API block |
| `packages/orchestration/pingpong_job.py` | +75/-6 | S2: `root` threaded through `_persist_job`, `save_job_plan` and `load_job_plan` into `job_record_path(..., root)`, each unchanged when omitted. S3: `load_job_plan_safe`. S4: `list_job_plans_safe`, naming a skipped record by job id. S5: `list_job_plans`. No line of this module names `jobs_dir` or globs the store |
| `tests/orchestration/test_unified_store_parity.py` | +290/-0 | S6, new file: 18 tests covering (a)-(n) plus four discriminators (f2 the wrong-JSON-shape route, m2 the absent store, m3 the classic `<id>.json` shape, m4 the layout-ownership guard). Module docstring states W1/W2/W3 and DECISION F275 D23. Every test isolates through `tmp_path` |

### C4 (this commit) F275 R42 C4: the round 42 handback.

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file; a handback cannot table the commit that writes it (R-0149 pattern) |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach /home/decodeux/Repos/remedy/.agent-wt-r42 c4cdc4ce` | exit 0, then REMOVED immediately: the path sits inside the repo and is not gitignored, so primary `git status --porcelain` read `?? .agent-wt-r42/`. Declared below as a deviation |
| `git worktree remove --force /home/decodeux/Repos/remedy/.agent-wt-r42` + `git worktree prune` | exit 0 |
| `git worktree add --detach /home/decodeux/Repos/remedy-r42-wt c4cdc4ce` | exit 0; outside the repository, so primary porcelain stayed EMPTY for the whole of G6 |
| `git worktree remove --force /home/decodeux/Repos/remedy-r42-wt` + `git worktree prune` | exit 0; `git worktree list` then reads exactly ONE entry |
| `git push` | see Next; run after this commit |

No PR created, none edited, none merged. No force-push, no history rewrite, no
branch created or deleted. No `gh` command run. `remedy` never invoked (the
console script is sandbox-blocked); no CLI reading was needed, so neither
`remedy` nor `python3 -m apps.cli.grouped` was run.

## Verification

One line per gate, real exit codes, real numbers.

**G1 TRANSPORT, at C0b — PASS, REAL_EXIT=0.** `.agent/authored/f275-r42.md` and
`.agent/last_block.md` resolve at `bc90d257` to the SAME git blob
`ea23f07e55d4416410773f64a37d70aea681a428`; both read 33858 bytes at sha256
`da92b95ac2d0f35d4ed31f73d31468a5fafc0df2d1560bc55f944e739ef374ed`, which is the
digest the block ordered. `.agent/last_block.md` was produced by
`git cat-file blob 9c4f39c6:.agent/authored/f275-r42.md > .agent/last_block.md`
and not retyped. This covers the two committed artefacts only and claims nothing
about the bytes emitted into the worker's prompt (§3 item 37).

**G2 THE PLAN, at C1 — PASS, REAL_EXIT=0.** `git show 6e885b61:.agent/plan.md` is
2720 bytes at sha256
`e2f61c3629cd36886279a2da0dac458e9d2c8b1b5b45f6e4f19fdd64754b6b91`, BYTE-EQUAL to
the PLAN42 slice as extracted from the committed block (slice 2720 bytes,
`byte_equal True`). 47 lines against the AGENTS.md cap of 50. `^## Goal$` reads
1; `^## Next Steps$` reads 1.

**G3 THE RECORD, at C2 — PASS with a DECLARED FORM DISAGREEMENT, REAL_EXIT=0.**
All three appends read from committed blobs only — pre at `6e885b61`, post at
`03a3048e`.

| Append | pre bytes | slice bytes | post bytes | A true bytes | B true bytes (raw / normalized) | A control | B control (raw / normalized) |
|---|---|---|---|---|---|---|---|
| RECORD42 → `.agent/live_review.md` | 855619 | 4759 | 860378 | **True** | False / **True** (N=1) | **REJECTS** | REJECTS / REJECTS |
| SLIPS42 → `.agent/prose_slips.md` | 234601 | 892 | 235493 | **True** | False / **True** (N=1) | **REJECTS** | REJECTS / REJECTS |
| DECISION42 → `.agent/decisions.md` | 1055728 | 5890 | 1061618 | **True** | False / **True** (N=7) | **REJECTS** | REJECTS / REJECTS |

Reader A: `post == pre + slice` exactly, nothing between them, and
`len(pre)+len(slice) == len(post)` for all three. N was COUNTED from the slice
(1, 1, 7), not taken from the block. Negative controls flipped ONE byte inside
the FIRST appended paragraph at offsets 857998 (`2`→`3`), 235047 (space→`!`) and
1055827 (`i`→`h`), and BOTH readers rejected all three.

The declared disagreement, per G3's own "the operation wins" clause: constraint 2
puts the separating blank line INSIDE each slice, so the slice's first paragraph
carries a LEADING newline which in the post blob is consumed as the paragraph
SEPARATOR. The raw structural reader — split on a blank line, compare the last N
paragraphs verbatim — therefore reads **False on the TRUE bytes** for all three
appends, while Reader A, the ordered operation, reads True. Diagnosed directly:
the slice paragraph begins `b'\n2026-09-10 '` and the post paragraph begins
`b'2026-09-10 \xc2'`, and the two are equal after stripping boundary newlines.
The normalized reader (each paragraph stripped of leading/trailing newlines ONLY,
nothing else) reads True on the true bytes AND REJECTS all three controls, so the
normalization is not a zero-gate. (d): `^Gate: F275 R41 ` reads 0 at C1 and 1 at
C2; `^## DECISION F275 D23 ` reads 0 at C1 and 1 at C2.

**G4 THE OPEN SET, at C3 — PASS, REAL_EXIT=0.** By DISTINCT ID, read from
`git show <rev>:.agent/live_review.md` into memory, never over the tracked file.
At base `77a7d840`: 103 distinct registered − 17 distinct `Done:` = **86 open**.
At C3 `c4cdc4ce`: 103 − 17 = **86 open**. Registered this round: `[]`. Resolved
this round: `[]`. Highest id present is R-0874, so R-0875 is still free as the
block states.

**G5 THE WIDEN IS GREEN, at C3 — PASS, five readings.**

| Command | REAL_EXIT | Result |
|---|---|---|
| `python3 -m pytest tests/orchestration/test_unified_store_parity.py -q` | 0 | `18 passed in 0.27s` |
| `python3 -m pytest tests/test_data_paths.py tests/storage/test_persistence.py -q` | 0 | `65 passed in 0.64s` |
| `python3 -m pytest tests/cli/test_golden_path.py -q` | 0 | `42 passed in 18.89s` |
| `python3 -m ruff check <data_paths.py> <pingpong_job.py> <test_unified_store_parity.py>` | 0 | `All checks passed!` |
| the shipped-surface probe (one `python3 -c`) | 0 | transcript below |

The probe read the SHIPPED functions, not grep, and printed the import origin
first so no installed copy could be mistaken for the work tree:

```
data_paths   imported FROM: /home/decodeux/Repos/remedy/packages/orchestration/data_paths.py
pingpong_job imported FROM: /home/decodeux/Repos/remedy/packages/orchestration/pingpong_job.py
job_record_paths    (root: 'Path | None' = None) -> 'list[Path]'
save_job_plan       (job: 'JobPlan', root: 'Path | None' = None) -> 'Path'
load_job_plan       (job_id: 'str', root: 'Path | None' = None) -> 'JobPlan | None'
load_job_plan_safe  (job_id: 'str', root: 'Path | None' = None) -> 'tuple[JobPlan | None, bool]'
list_job_plans      (root: 'Path | None' = None) -> 'list[JobPlan]'
list_job_plans_safe (root: 'Path | None' = None) -> 'tuple[list[JobPlan], bool, list[str]]'
_persist_job        (job: 'JobPlan', root: 'Path | None' = None) -> 'Path'
```

All six ordered signatures are present with the exact shapes S1 to S5 fix, and
`_persist_job` carries the override too, as S2 requires.

**G6 THE WIDEN BITES — MUTATION RED PROOF, at C3 — PASS, all four mutations go
RED.** In a disposable worktree detached at `c4cdc4ce` at
`/home/decodeux/Repos/remedy-r42-wt`, never `cd`-ed into: every command ran as
`subprocess.run([...], cwd=<abs worktree>)`, every run under `python3 -B`, and
`__pycache__` purged before every run. Before believing any result the imported
module paths were printed and they resolve to the WORKTREE, not to an installed
copy:
`/home/decodeux/Repos/remedy-r42-wt/packages/orchestration/pingpong_job.py` and
`.../data_paths.py`. Pristine digests: `pingpong_job.py`
`fa0eb144dfec5c8fafbedd391709c6a79a7415952a36edafb228b3a728cd0d2e`,
`data_paths.py`
`0526e2a3197217d83b0e430fb19ff292cd444337377aa961cb0adc317c45f0ff`.

| Run | anchor count before | REAL_EXIT | summary | FAILED node ids (read from the `FAILED ` lines, token after the FIRST space) |
|---|---|---|---|---|
| control 0 | — | 0 | `18 passed in 0.28s` | none |
| M1 `load_job_plan` drops `root` | 1 | 1 | `2 failed, 16 passed` | `…::TestTheJobsRootOverride::test_b_a_record_written_under_a_root_loads_back_through_the_same_root`, `…::TestTheJobsRootOverride::test_c_a_record_under_one_root_is_invisible_under_another_root` |
| control after M1 | — | 0 | `18 passed in 0.28s` | none |
| M2 `load_job_plan_safe` except returns `(None, False)` | 1 | 1 | `3 failed, 15 passed` | `…::TestCorruptionVisibilityOfOneRecord::test_f_an_unreadable_record_reads_as_not_found_and_degraded`, `…::test_f2_a_record_whose_json_parses_into_the_wrong_shape_is_degraded_not_raised`, `…::test_h_the_plain_reader_cannot_tell_missing_from_unreadable_and_the_safe_one_can` |
| control after M2 | — | 0 | `18 passed in 0.28s` | none |
| M3 `list_job_plans_safe` sort line deleted | 1 | 1 | `1 failed, 17 passed` | `…::TestListingTheUnifiedStore::test_j_every_persisted_record_is_listed_newest_first` |
| control after M3 | — | 0 | `18 passed in 0.28s` | none |
| M4 `job_record_paths` glob `*/job.json`→`*.json` | 1 | 1 | `6 failed, 12 passed` | `…::TestListingTheUnifiedStore::test_j_…newest_first`, `…::test_k_an_unreadable_record_is_skipped_and_named_by_its_job_id`, `…::test_l_the_plain_listing_hides_the_degraded_flag`, `…::TestOnlyDataPathsSpellsTheStoreShape::test_m_the_accessor_returns_the_records_sorted_by_path`, `…::test_m3_the_classic_file_per_job_shape_is_not_what_the_accessor_finds`, `…::TestRecordsWrittenBeforeThisRoundStillLoad::test_n_a_record_carrying_none_of_the_new_keys_still_loads` |
| control after M4 | — | 0 | `18 passed in 0.28s` | none |

No mutation stayed green, so nothing has to be declared unreached. Every anchor
counted exactly 1 before it was applied. Every revert was byte-exact:
`pingpong_job.py` read back `fa0eb144…` after each of M1, M2 and M3, and
`data_paths.py` read back `0526e2a3…` after M4 — and after the LAST revert BOTH
touched files equal their pristine digests (`pristine_match=True` for both).
`git status --porcelain` in the PRIMARY checkout was read in the SAME command
sequence as each mutation, before its result was read, and was EMPTY (`''`) every
time. One honest reading to record rather than dress up: the cache purge removed
**0** directories on every run, because the worktree was freshly created and
`python3 -B` writes none — the purge ran and found nothing, which is the correct
outcome, not a skipped step.

**G7 THE LAYOUT GUARD, at C3 — PASS, REAL_EXIT=0.**
`python3 -m pytest tests/test_data_paths.py -q` reads `50 passed in 0.60s`. An
`ast` reading of `packages/orchestration/pingpong_job.py` at C3 — counting
`ast.Name` with `id == "jobs_dir"`, `ast.Attribute` with `attr == "jobs_dir"`,
and any `ImportFrom` naming or aliasing it — reports **0** references, `[]`. The
same reading finds `job_record_paths` once, at line 516, which is the listing
reaching the layout only through S1's accessor. This re-measures the guard the
block quotes as having gone red on the first draft rather than assuming it.

**G8 NOTHING ELSE MOVED, at C3 — PASS.** `.agent/STOP` read FROM DISK is ABSENT
(`ls: cannot access '/home/decodeux/Repos/remedy/.agent/STOP': No such file or
directory`) — read once before the first commit and again before C3, as
constraint 10 orders. `git status --porcelain` is EMPTY. `git worktree list`
reads exactly ONE entry, the primary checkout.
`git diff --name-only 77a7d840..c4cdc4ce` returns 9 paths and is an EXACT SET
MATCH against the Change list minus `.agent/handoff.md`: **MISSING `[]`, EXTRA
`[]`**. Paths under `apps/`, `docs/` or `scripts/`: **0**, `[]`.

| Commit | insertions | cap 500 |
|---|---|---|
| C0a `9c4f39c6` | 362 | under |
| C0b `bc90d257` | 333 | under |
| C1 `6e885b61` | 18 | under |
| C2 `03a3048e` | 18 | under |
| C3 `c4cdc4ce` | 379 | under |

No commit is oversize, so F275's one permitted declared-oversize commit is still
unspent and remains available to the flip.

**Constraint 9 — the block's own measurement, taken from the committed
`.agent/authored/f275-r42.md` blob at C3.** TOTAL = **362** lines against the cap
of 490. Slice content lines: PLAN42 47, RECORD42 2, SLIPS42 2, DECISION42 14,
summed **65**. PROSE = 362 − 65 = **297** against the cap of 400. Marker lines
counted as prose. NEITHER CAP IS EXCEEDED.

**Self-review additions beyond the ordered gates** (AGENTS.md Mandatory
Self-Review Loop, "what could break"): `python3 -m pytest
tests/orchestration/test_import_reachability.py -q` reads `3 passed in 1.06s`
(REAL_EXIT=0), and `python3 -m pytest tests/orchestration -q -p no:randomly -k
"pingpong or job_admin or job_record or data_paths or persist"` reads
`539 passed, 11319 deselected in 64.56s`. Both were run before C3 was committed.

## Authored-text proofs

| Authored text | Target | Proof |
|---|---|---|
| the whole block | `.agent/authored/f275-r42.md` | 33858 bytes, 362 lines, final byte a newline, sha256 `da92b95ac2d0f35d4ed31f73d31468a5fafc0df2d1560bc55f944e739ef374ed` — matches the digest the block ordered, verified on disk BEFORE C0a was committed and again from the committed blob at G1 |
| PLAN42 | `.agent/plan.md` | extracted by `BEGIN-`/`END-` marker index from the COMMITTED blob via `git cat-file blob` and written with `pathlib.write_bytes`; never retyped. Committed blob byte-equal to the extracted slice, 2720 bytes, sha256 `e2f61c3629cd36886279a2da0dac458e9d2c8b1b5b45f6e4f19fdd64754b6b91` |
| RECORD42 | `.agent/live_review.md` | same mechanical extraction; applied as `old_bytes + slice_bytes`, nothing inserted. Reader A identical; 855619 + 4759 = 860378 |
| SLIPS42 | `.agent/prose_slips.md` | same; 234601 + 892 = 235493 |
| DECISION42 | `.agent/decisions.md` | same; 1055728 + 5890 = 1061618 |

S1 to S6 were DESCRIBED, not sliced (constraint 3), so there is no authored-text
proof for any production line and none is claimed. No slice was retyped,
reflowed or edited.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |
| S1 `data_paths.job_record_paths` | done | placed directly above `job_evidence_dir`; globs `*/job.json`, `[]` for an absent store, sorted by path, one WHY comment carrying the DECISION F260 D1 fact |
| S2 `root` threaded through three functions | done | `_persist_job`, `save_job_plan`, `load_job_plan`; each passes `root` to `job_record_path(..., root)`; `jobs_dir` reference count in the module is 0 (G7) |
| S3 `load_job_plan_safe` | done | three answers; catches `OSError`, `_json.JSONDecodeError`, `KeyError`, `ValueError`, `TypeError` |
| S4 `list_job_plans_safe` | done | skips by job id (directory name), `degraded` true on any skip, sorted by `created_at` descending |
| S5 `list_job_plans` | done | returns S4's first element, discards the other two |
| S6 `tests/orchestration/test_unified_store_parity.py` | deviated | every ordered property (a)-(n) is covered and each test name says what it pins, but the file ships **18** tests, not 14: four discriminators were added beyond the minimum the block set. Reason below |
| G1-G8 | done | all eight run for real; G3 declares a form disagreement, G6 declares a 0-directory cache purge |

## Deviations & assumptions

1. **S6 ships 18 tests, not 14 — an ADDITION within the block's "at minimum"
   licence, declared because the count differs from the ordered list.** (a)-(n)
   are each their own test with a name stating its property. The four extra are
   discriminators, added because without them a mutation the block orders would
   not have been reachable: `test_f2` (valid JSON of the wrong TYPE, which
   decodes fine and fails inside `_import_job`) is what makes the widened
   `ValueError`/`TypeError` clause in S3 load-bearing rather than decorative;
   `test_m2` pins `[]` for an absent store, which (m) names but (m)'s
   sorted-by-path assertion cannot see; `test_m3` pins that the CLASSIC
   `<id>.json` shape is NOT what the accessor finds, and it is one of the six
   tests M4 turns red — without it a store holding only unified records has no
   top-level `*.json` file, so widening the glob would have left every other
   listing test green; `test_m4` keeps the layout-ownership reason beside the
   code that would otherwise move the glob back into `pingpong_job`.

2. **S6 (d) isolates through `tmp_path` by POINTING the process data root at it,
   not by bypassing resolution.** "Omitting the override resolves where it
   resolved before" cannot be measured without exercising the default
   resolution, so `test_d` monkeypatches `REMEDY_DATA_DIR` to
   `tmp_path / "remedy_data"` and asserts the save lands at
   `<that>/jobs/<job_id>/job.json`. The block's binding clause — "no test can
   write into the repository's own `.data`" — holds: the write goes under
   `tmp_path`. This is the idiom
   `tests/orchestration/test_job_administrative_fields.py` already uses for the
   same purpose. Declared because the sentence also says "never through the
   process data root", and this test does reach that mechanism, pointed
   elsewhere.

3. **The G6 worktree was created twice.** The first `git worktree add` used
   `/home/decodeux/Repos/remedy/.agent-wt-r42`, INSIDE the repository and not
   covered by `.gitignore`, so primary `git status --porcelain` immediately read
   `?? .agent-wt-r42/`. It was removed and pruned before any mutation ran, and
   the proof was taken in `/home/decodeux/Repos/remedy-r42-wt`, outside the
   repository, where primary porcelain stayed EMPTY for the whole of G6. No
   mutation, run or reading was taken in the first worktree. Declared as an
   extra pair of external actions against the block's ordered sequence.

4. **G3's raw structural reader reads FALSE on the TRUE bytes for all three
   appends.** This is the form disagreement G3 anticipates and it is declared
   rather than routed around: constraint 2 puts the separating blank line inside
   the slice, so the slice's first paragraph owns a leading newline that the post
   blob spends as a paragraph separator. The ordered operation (Reader A, pure
   concatenation) is True for all three; the normalized Reader B is True for all
   three; all six control readings reject. Nothing was edited to make this agree
   — per constraint 1 a slice is never edited even where it looks wrong, and
   nothing about the slices IS wrong here, only the naive reader's form.

5. **`_persist_job` took the override too, which S2 orders explicitly.** An `ast`
   reading of `pingpong_job.py` at C3 counts **31** internal `_persist_job(...)`
   call sites, of which exactly **1** passes a second argument — `save_job_plan`'s
   own `_persist_job(job, root)`, added this round. The other 30 are unchanged and
   keep resolving through the process data root. No consumer moved anywhere in
   this round, which is what "green by construction" means here.

6. **Ruff's `B014`-style objection to the redundant exception tuple does not
   arise.** S3 and S4 list `_json.JSONDecodeError` beside `ValueError` although
   the former subclasses the latter. `[tool.ruff.lint] select` is
   `["E", "F", "W", "I", "UP"]` with no `B`, so the spec was followed literally
   and `ruff check` reads `All checks passed!`. Recorded so a later bugbear
   enablement finds the reason rather than a surprise.

No other deviation. No finding registered, none resolved, no id minted; R-0875
remains free. No path under `apps/`, `docs/` or `scripts/` was touched.

## Open findings

**86 open by distinct id**, unchanged from this round's base `77a7d840` — 103
distinct registrations against 17 distinct resolutions at both readings. Four are
High: R-0803, R-0804, R-0806 and R-0807, all F273's, per DECISION F272 D12.

## Next

Review `77a7d840..HEAD` and issue the round 42 verdict. The next production round
is THE FLIP itself — now that its target API exists — as F275's one
declared-oversize commit, with the inseparability reason and the real size stated
in the handback BEFORE review, and with either a per-site enumeration of the
`Job` and `Task` type sites or an explicit declaration that they were applied
from a measurement taken in that round's own worktree (the gap the SLIPS42 line
records). Phase 1 rule 1 first: read `.agent/STOP` from disk.
