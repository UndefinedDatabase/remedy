# Handback — F037 R6

## Session
SESSION 2 of feature F037 · round 6 · rounds so far 6.
The 25-round / 7-session soft limit is not approached: 6 rounds, 2 sessions.

## Range
Review of 9deb942eda94ec82ba00badbeece4cde05138bed..HEAD
(plus the C4 handoff commit that writes this file).
Branch: `feature/f037-rendered-diff-viewer`. Round base: `9deb942e`.

## Commits

### e99c9840 docs(agent): save the F037 R6 step block verbatim
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f037-r6.md | +407 / -0 | C0a — the block saved verbatim, then worked from; every slice below was extracted from this COMMITTED blob in Python, never retyped |

### 7c73cba3 docs(agent): mirror the F037 R6 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +376 / -329 | C0b — `git cat-file blob HEAD:.agent/authored/f037-r6.md` written out; the paired-line numstat is the full-file-rewrite shape, not a partial copy |

### a597bad9 docs(agent): point the plan at the F037 R6 resolver round
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +19 / -16 | C1 — whole-file replacement, byte-equal to slice PLANF037R6; 48 lines, under the 50-line rule |

### daf03d1c docs(agent): book the R5 verdict, resolve R-0717 and R-0718, record four prose slips
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +4 / -2 | C2 — the DONE717 and DONE718 FROM/TO pairs, then the GATER5 EOF append |
| .agent/prose_slips.md | +25 / -0 | C2 — the SLIPR6 EOF append, four slips, no id |

### c30ec76d feat(diff-view): resolve evidence artifacts to the contract-v1 diff envelope
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/diff_view_source.py | +158 / -0 | C3 — the resolver, written from the SPEC; `ui_server.py` and `diff_parser.py` untouched |
| tests/orchestration/test_diff_view_source.py | +182 / -0 | C3 — nine tests, including the refusal test that pins that nothing was READ |

### C4 (this commit) docs(agent): hand back F037 R6
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | n/a | C4 — a handback cannot table the commit that writes it (R-0149 pattern) |

## External actions
- `git worktree add .remedy-wt/f037-r6-redproof c30ec76d` — created for G6.
- `git worktree remove .remedy-wt/f037-r6-redproof` then `git worktree prune` —
  removed; `git worktree list` back to 1 line, primary `git status --porcelain`
  0 lines.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` —
  returned `[]` verbatim. No PR created, nothing merged, as the block ordered.
- `git push origin feature/f037-rendered-diff-viewer` — ordered AFTER C4 and
  deliberately outside every gate, so its result is not named here; the reviewer
  reads the remote tip itself.

## Verification

**G1 hygiene — PASS.** `.agent/STOP` ABSENT before C0a and ABSENT again before
C4. `git rev-parse HEAD` before C0a = `9deb942eda94ec82ba00badbeece4cde05138bed`,
equal to the base SHA. `git branch --show-current` =
`feature/f037-rendered-diff-viewer`. `git status --porcelain` LINE COUNT after
C0a 0, after C0b 0, after C1 0, after C2 0, after C3 0.

**G2 transport, one digest comparison — PASS.** After C0a:
`.agent/authored/f037-r6.md` sha256
`0bf34beb051ea36b84b8e1cb1ed3fa3d5e7dfde97f1cd5f1665d5a8591e3d778`, 29657 bytes,
407 lines. After C0b: `git rev-parse HEAD:.agent/authored/f037-r6.md` =
`eff8007ac053110c3b94b2e10d648831c3d63e40` and
`git rev-parse HEAD:.agent/last_block.md` =
`eff8007ac053110c3b94b2e10d648831c3d63e40` — the SAME blob hash. Stated plainly:
this chain covers the saved copy, its mirror and the working copy, and claims
NOTHING about the bytes of any prompt.

**G3 extraction and caps — PASS.** All five slices extracted from the COMMITTED
C0a blob by their marker lines: PLANF037R6 48 lines, DONE717 1, DONE718 1,
GATER5 1, SLIPR6 24. TOTAL 407 (measured), CONTENT 75 (measured),
PROSE = 407 − 75 = 332 (measured). PROSE 332 ≤ 400 and TOTAL 407 ≤ 490.

**G4 the plan at C1 — PASS.** `.agent/plan.md` byte-equal to PLANF037R6 under
the newline-included convention: **True**. NEGATIVE CONTROL against the slice
minus its trailing newline: **False**. `^## Goal$` 1, `^## Next Steps$` 1,
`wc -l` 48, strictly under 50.

**G5 the record at C2, full byte forensics — PASS.**
PAIRS. R-0717 FROM count before C2 1, after C2 0; TO count before 0, after 1.
R-0718 FROM count before C2 1, after C2 0; TO count before 0, after 1. The
containment readings were re-measured on disk: DONE717 `TO contains FROM: false`,
DONE718 `TO contains FROM: false` — both as the block states.
APPEND, live_review.md. Base 1156642 bytes. L (after the two pairs, before the
append) = 1159601. GATER5 byte length 2512. Post-append length 1162114 =
L + 1 + 2512 = 1162114 → **True**. Reader (a): the intermediate is a byte PREFIX
of the final → **True**. Reader (b), independent and structural: N, the number of
blank-line units in GATER5, measured by the script as **1**; the LAST 1 unit of
the final file equals the slice's 1 unit IN ORDER → **True**. NEGATIVE CONTROL:
one byte flipped inside the FIRST appended paragraph → reader (a) **False** and
reader (b) **False**.
APPEND, prose_slips.md. Base length before C2 measured at **6840** bytes, beside
the block's stated 6840 — they agree. SLIPR6 byte length 1583. Post-append length
8424 = 6840 + 1 + 1583 = 8424 → **True**. Reader (a) prefix → **True**. Reader
(b): Np = **4** blank-line units in SLIPR6; the LAST 4 units of the final file
equal the slice's 4 units IN ORDER → **True**. NEGATIVE CONTROL with the flipped
byte inside the FIRST appended bullet → reader (a) **False**, reader (b)
**False**.
COUNTS after C2, line-anchored, each MEASURED and each equal to the value the
block names: `^- R-\d+ — ` **279** (ordered 279, unchanged); `^Done: R-\d+ — `
**27** (ordered 27); `^Landed: R-` **1** (ordered 1); `^Gate: F\d+ R\d+ — `
**76** (ordered 76); `^Gate: R\d+ — ` **19** (ordered 19, unchanged).
Ids ADDED: **[]** (empty, as ordered). Ids newly RESOLVED: **R-0717, R-0718**
(exactly the two, as ordered). All ids DISTINCT: **True** (279 lines, 279
distinct). Maximum id: **R-0718**. Open set size: **252** — every registered id
minus every resolved id, 279 − 27, and two lower than the 254 GATER5 records for
the state before its own commit, which is the two resolutions this commit lands.

**G6 red-proofs — PASS, both mutations RED.** Run only inside the disposable
worktree `.remedy-wt/f037-r6-redproof` at the C3 tree, never in the primary
checkout; `__pycache__` purged and `python3 -B` used before EVERY run; the module
restored with `git checkout --` between mutations, each restore verified at
`git status --porcelain` 0 lines.

- UNMUTATED CONTROL:
  `python3 -B -m pytest tests/orchestration/test_diff_view_source.py -q` —
  real exit code **0**, verbatim summary `9 passed in 0.21s`.
- MUTATION (a), defeat S5(b) — the task-run branch accepts ANY `task_id` without
  testing membership in `list_task_run_ids`, so the path is built from the
  argument directly. FROM (occurrences counted at exactly 1 before the edit):

      if task_id is not None and task_id not in task_run_ids:
          view["reason"] = DIFF_REASON_UNKNOWN_TASK_RUN
          return view

  TO: the three lines deleted entirely.
  Real exit code **1**, verbatim summary `2 failed, 7 passed in 0.23s`. Failing
  node ids in full:
  `tests/orchestration/test_diff_view_source.py::test_unknown_task_run_is_refused_and_reports_the_real_runs`
  and
  `tests/orchestration/test_diff_view_source.py::test_traversal_task_ids_are_refused_without_reading_anything`.
- MUTATION (b), defeat S5(d) — the missing-artifact branch reports `available`
  True with `reason` None. FROM (occurrences counted at exactly 1 before the
  edit):

      if diff_text is None:
          view["reason"] = DIFF_REASON_ARTIFACT_MISSING
          return view

  TO:

      if diff_text is None:
          view["available"] = True
          view["reason"] = None
          return view

  Real exit code **1**, verbatim summary `1 failed, 8 passed in 0.23s`. Failing
  node id in full:
  `tests/orchestration/test_diff_view_source.py::test_missing_job_artifact_still_names_the_path_it_looked_for`.
- Worktree removed and pruned. `git worktree list` LINE COUNT **1**; primary
  `git status --porcelain` LINE COUNT **0**.

**G7 suite, lint and canary at C3 — PASS.** One pytest process at a time, never
two in parallel.

- `python3 -m pytest tests/orchestration/test_diff_view_source.py
  tests/orchestration/test_diff_parser.py -q` — real exit code **0**, verbatim
  summary `37 passed in 0.26s`, `^FAILED` line count **0**.
- EXTRACTOR-BLINDNESS CONTROL: the SAME `^FAILED` counter run over a control
  string containing
  `FAILED tests/orchestration/test_diff_view_source.py::test_control_string`
  returns **1**. The 0 above is therefore a measurement, not a blind spot.
- NODE-ID INVENTORY from
  `python3 -m pytest tests/orchestration/test_diff_view_source.py --collect-only -q`
  — **9 tests collected**, never derived from `-v` output:
  `::test_job_scope_reads_the_workspace_diff`,
  `::test_task_run_scope_reads_that_runs_safe_diff`,
  `::test_version_is_the_parsers_imported_contract_version`,
  `::test_absent_evidence_dir_is_named_rather_than_raised`,
  `::test_missing_job_artifact_still_names_the_path_it_looked_for`,
  `::test_unknown_task_run_is_refused_and_reports_the_real_runs`,
  `::test_traversal_task_ids_are_refused_without_reading_anything`,
  `::test_list_task_run_ids_sorts_and_filters_the_listing`,
  `::test_an_empty_diff_artifact_is_available_with_no_files`, each prefixed
  `tests/orchestration/test_diff_view_source.py`.
- `python3 -m ruff check packages/orchestration/diff_view_source.py
  tests/orchestration/test_diff_view_source.py` with the repository's own
  configuration and NO `--isolated` — real exit code **0**, verbatim output
  `All checks passed!`, stderr empty.
- CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — real exit code
  **0**, verbatim summary `42 passed in 20.80s`.

**G8 structure, artifacts and the Open PR Gate at C3 — PASS.**

- `git diff --name-only 9deb942e..c30ec76d` returns exactly:
  `.agent/authored/f037-r6.md`, `.agent/last_block.md`, `.agent/live_review.md`,
  `.agent/plan.md`, `.agent/prose_slips.md`,
  `packages/orchestration/diff_view_source.py`,
  `tests/orchestration/test_diff_view_source.py`. Residue ACTUAL minus EXPECTED
  **[]**; residue EXPECTED minus ACTUAL **[]**.
- Restricted `git diff --stat`: `apps/` **EMPTY**; `docs/` **EMPTY**;
  `packages/` holds only `packages/orchestration/diff_view_source.py`
  (158 insertions); `tests/` holds only
  `tests/orchestration/test_diff_view_source.py` (182 insertions).
- Per-commit INSERTION count from `git diff --numstat`, every commit
  single-parent (parents = 1) and every count under 500: C0a `e99c9840` **407**;
  C0b `7c73cba3` **376**; C1 `a597bad9` **19**; C2 `daf03d1c` **29**;
  C3 `c30ec76d` **340**. C4 is deliberately not counted — its own count cannot
  exist while its text is being written.
- Line-anchored `^<<<SLICE ` plus `^<<<END ` sweep: `.agent/plan.md` at C1
  **0**; `.agent/live_review.md` at C2 **0**; `.agent/prose_slips.md` at C2
  **0**. The SAME counter over the C0a blob measures **10**, greater than zero,
  so the sweep is shown not to be blind.
- `git ls-files .remedy-wt` LINE COUNT **0**.
- Open PR Gate, verbatim:
  `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
  returned `[]`.

## Authored-text proofs
Five slices, all extracted in Python from the COMMITTED C0a blob by their marker
LINES and applied byte for byte; none was retyped and none was edited.
- PLANF037R6 → `.agent/plan.md`: whole-file replacement, byte-equality **True**,
  negative control **False** (G4).
- DONE717 → `.agent/live_review.md`: FROM 1→0, TO 0→1 (G5).
- DONE718 → `.agent/live_review.md`: FROM 1→0, TO 0→1 (G5).
- GATER5 → `.agent/live_review.md`: prefix reader **True**, unit reader **True**,
  negative control **False**/**False** (G5).
- SLIPR6 → `.agent/prose_slips.md`: prefix reader **True**, unit reader **True**,
  negative control **False**/**False** (G5).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block verbatim | done | `e99c9840`, 407 lines |
| C0b mirror the C0a blob | done | `7c73cba3`, same blob hash `eff8007a` |
| C1 the plan | done | `a597bad9`, byte-equal to PLANF037R6 |
| C2 the record | done | `daf03d1c`, both pairs plus both appends in one commit |
| C3 the module and its tests | done | `c30ec76d`, written from the SPEC |
| C4 the handback | done | this commit |
| Constraint 1 slices from the committed blob | done | extracted by marker LINES in Python |
| Constraint 2 plan whole-file | done | G4 True |
| Constraint 3 both pairs are rewrites | done | G5 FROM 1→0, TO 0→1 for each |
| Constraint 4 appends after the pairs, same commit | done | single separator newline, file's own convention |
| Constraint 5 no id minted | done | ids ADDED [] |
| Constraint 6 `Landed: R-0711` untouched | done | `^Landed: R-` reads 1, exactly that line |
| Constraint 7 production code written from the SPEC | done | module docstring, one-line WHY above each definition, type hints, `from packages.orchestration...` import style |
| Constraint 8 `ui_server.py` untouched | done | not in the name-only list; no `tests/ui_server/` file touched |
| Constraint 9 `diff_parser.py` untouched | done | not in the name-only list; imported only |
| Constraint 10 no interactive constructs | done | `python3 -m pytest tests/test_no_interactive_guard.py -q` exit 0, `6 passed in 1.13s` |
| Constraint 11 report disagreements | done | none arose; every named value was met on measurement |
| S1 module docstring states the WHY | done | names the split from `diff_parser.py`, the no-HTTP boundary and the named-absence contract |
| S2 the public names | done | all eleven present with the ordered values, including `SAFE_TASK_RUN_ID_RE` |
| S3 `list_task_run_ids` | done | sorted, `SAFE_TASK_RUN_ID_RE.fullmatch`, `[]` on all three absences; re-declaration reason stated |
| S4 the nine envelope keys | done | exactly those keys, `version` IMPORTED, no second version literal |
| S5(a) no evidence dir | done | reason `evidence_dir_unavailable`, source None, files [], task_run_ids [] |
| S5(b) unknown task run | done | membership in the REAL listing; WHY comment names the deliberate absence of `path_utils.sanitize_path_component` |
| S5(c) artifact path and early `source` | done | `source` set before the read |
| S5(d) unreadable artifact | done | `OSError`/`UnicodeDecodeError`, `source` kept, mutation (b) RED |
| S5(e) parse, and EMPTY is AVAILABLE | done | WHY comment says it; pinned by `test_an_empty_diff_artifact_is_available_with_no_files` |
| S6 never raises | done | the path coercion is guarded too, so a non-path argument becomes a named absence rather than a `TypeError` |
| S7 trees under `tmp_path` | done | one helper, real unified-diff text, nothing under the repository |
| S8 job happy path | done | `test_job_scope_reads_the_workspace_diff` |
| S9 task-run happy path | done | asserts `packages/orchestration/task_only.py`, a path ONLY the task diff holds |
| S10 version by IMPORT | done | `test_version_is_the_parsers_imported_contract_version`, no transcribed integer |
| S11 one test per absence reason | done | three tests, each with reason, `available is False`, `files == []`, plus the ordered extra assertions |
| S12 the refusal test | done | all five hostile ids; marker planted OUTSIDE the evidence dir absent from every `repr()` |
| S13 sorts and filters | done | `["T001", "T002", "T010"]` exactly, with `nope` and the FILE `T999` excluded |
| S14 empty artifact | done | available True, `files == []` |
| G1 hygiene | done | STOP ABSENT twice, HEAD = base, five status readings all 0 |
| G2 transport | done | one digest comparison, blob hashes identical |
| G3 extraction and caps | done | PROSE 332 ≤ 400, TOTAL 407 ≤ 490 |
| G4 the plan | done | True / False / 1 / 1 / 48 |
| G5 the record | done | every count met, both negative controls False |
| G6 red-proofs | done | control green, both mutations RED, worktree removed |
| G7 suite, lint, canary | done | 37 passed, blindness control 1, 9 node ids, ruff 0, canary 42 passed |
| G8 structure and Open PR Gate | done | both residues empty, marker sweep 0/0/0 against a control of 10, `[]` |

## Deviations & assumptions
None. Every value the block named was met on measurement: `^- R-\d+ — ` 279,
`^Done: R-\d+ — ` 27, `^Landed: R-` 1, `^Gate: F\d+ R\d+ — ` 76,
`^Gate: R\d+ — ` 19, and the `.agent/prose_slips.md` base length 6840. The
ordered commit sequence C0a, C0b, C1, C2, C3, C4 was followed exactly — no extra
commit, none dropped, none reordered.

Two assumptions worth naming, neither of which changed what was built:
1. `evidence_dir` is typed `Path | None`. The block's SPEC gives no annotation
   for it, and `Path` is what every caller in `packages/orchestration/` already
   holds; the coercion `Path(evidence_dir)` also accepts a `str`, so an
   endpoint layer passing a string still works.
2. S5(d) is implemented as ONE absence flag rather than two branches, so
   "the path is not a file" and "the bytes would not decode" reach a single
   place that sets `DIFF_REASON_ARTIFACT_MISSING`. That is what makes mutation
   (b) a single-site edit; the observable behaviour is exactly as S5(d) states.

## Next
The first action of the next round is to re-read `.agent/STOP` from disk
(self-drive Phase 1 rule 1), and only then the Open PR Gate
(`gh pr list --state open --json number,headRefName,baseRefName,isDraft`).

After that, R7 is the second half of T001: the two GET routes onto
`build_diff_view` — the job scope as a handler-dict key and the task-run scope as
a structural route — with the route walk in
`tests/ui_server/test_command_channel.py` MEASURED at the base before the edit,
since `packages/orchestration/ui_server.py` was deliberately left untouched this
round. `build_diff_view` currently has no caller anywhere in the tree; R7 gives
it one.
