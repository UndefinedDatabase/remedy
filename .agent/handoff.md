# Handback — F037 Rendered diff viewer, round 26 (EVIDENCE AND THE REVIEW ZIP)

## Session

SESSION 8 of feature F037 · round 26 · rounds so far 26

Rounds planned for this session: R25 (PASSED), R26 (this one), R27. R27 ends the
session and F037's closure sequence. This round is permitted past the 25-round
and seven-session soft limits of operator amendment amend0827-process-diet rule 6
by that amendment's rule 1, which names a feature's CLOSURE SEQUENCE as the one
exception to the ban on bookkeeping-only rounds.

SCOPE REPORT, carried because both soft limits are exceeded (rule 6):

- FINISHED. T001 the parser, T002 the source and the read endpoints, T003 the
  client row model, sidebar, hunk collapse, intraline emphasis and virtual
  scrolling — all built, all tested, all named with their test files in the
  Built State section this round appended to `docs/roadmap/features/T5_F037.md`.
  The integration gate PASSED at R25. The evidence bundle and the READY review
  package exist, named below.
- MISSING, and deliberately so per DECISION F037 D11 and amendment A6: the
  highlighting WIRING (the lazy language model ships complete, tested and
  UNWIRED), the 10k-line end-to-end perf measurement, and a ruling on the
  sidebar's visual treatment.
- PROPOSAL, unchanged from R24 and executed by no session: the split-off scope of
  A6 wants its own STATUS line immediately before F033. Rule 6 forbids a session
  executing a STATUS split on its own authority, so `docs/roadmap/STATUS.md` is
  untouched by this round.
- REMAINING WORK ON F037: the STATUS round only.

## Range

Review of `f676042c..HEAD`.

## Commits

### fb0ee4cb docs(agent): save the F037 R26 evidence-and-zip block

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f037-r26.md` | +490 / -0 | C0a — the block saved verbatim |

### 82cc2579 docs(agent): mirror the R26 block into last_block

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +416 / -272 | C0b — same bytes, one blob with C0a |

### 77cec858 docs(agent): point the plan at the F037 evidence-and-zip round

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +21 / -21 | C1 — the PLANF037R26 slice, rewritten not appended |

### 514e2991 docs(review): book the F037 R25 integration-gate verdict

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +12 / -0 | C2 — GATER25, appended |

### 5e557a1c docs(roadmap): record F037's Built State on the feature file

| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/features/T5_F037.md` | +49 / -0 | C3 — BUILTSTATE appended after A6; closure precondition 4. This is the ACCEPTED HEAD the package records. |

### C4 docs(agent): hand back F037 R26 with the closure package

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | (self-reference) | C4 — this file; a handback cannot table the commit that writes it (R-0149 pattern). Its insertion count belongs to the next round's ledger entry and was not gated here, as the block states. |

## External actions

| Command | Outcome |
|---------|---------|
| `gh pr list --state open --json number,headRefName,baseRefName,isDraft` | `[]` — no open PRs |
| `git worktree list` | One line: `/home/decodeux/Repos/remedy  5e557a1c [feature/f037-rendered-diff-viewer]` — the primary checkout alone; no worktree was added or removed this round |
| `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f037_closure_evidence/remedy-job-evidence-f037-closure` | exit 0; `PACKAGE_STATUS=READY_FOR_REVIEW` |
| `git push -u origin feature/f037-rendered-diff-viewer` | Runs immediately AFTER the commit that writes this file; see the note below |

No PR was created. No merge. No force-push, no history rewrite, no work on `main`.

THE PUSH OUTCOME IS NOT STATED HERE, deliberately. The push necessarily happens
after the commit that writes this file, so any outcome printed here would be a
value that could not exist when the text was written, and the write-once rule
forbids a second handoff commit to fill it in. The outcome is reported in this
round's session output instead, and the reviewer can measure it directly:
`git rev-parse HEAD` equals `git rev-parse origin/feature/f037-rendered-diff-viewer`
if and only if the push succeeded.

## The closure package — the four values R27 needs

| Field | Value |
|-------|-------|
| Evidence job | `f037-closure` |
| package | `remedy-review-20260828-142213-READY_FOR_REVIEW.zip` |
| SHA-256 | `c3755b73a6cbaf21cd0547ce590aafee244d4143ace6ca1833bc93b50c87ef26` |
| package path | `/home/decodeux/Repos/remedy-history/zips` |
| accepted HEAD | `5e557a1c2b4f7f9187f5388b18a3712d4a5c3d7e` |

## Verification

**G1 HYGIENE — PASS.** `.agent/STOP` read from disk before C0a: `ls` reported
"No such file or directory" — ABSENT. Read again before C4, same command, same
answer — ABSENT. `git rev-parse HEAD` before C0a =
`f676042c550aeb9cb26ee54a34a10c0c2993776c`, equal to the BASE `f676042c`.
`git branch --show-current` = `feature/f037-rendered-diff-viewer`.
`git status --porcelain | wc -l` = 0 after C0a, after C0b, after C1, after C2,
after C3, and again after the zip build — six readings, all 0.

**G2 TRANSPORT — PASS.** sha256 of the committed `.agent/authored/f037-r26.md`
blob = `e784cecccecd0bf90632583400fa0086e55e027f5f11951d4ddbc39707cdf0da`
(31847 bytes, 490 lines). sha256 of the reviewer's own original at
`.remedy-wt/f037-r26-block.md` = the same digest, the same 31847 bytes. They are
EQUAL. That file existed before this worker did and was not written by it, so
this reading covers the EMISSION and not merely this worker's self-consistency.
No digest is stated here that was not computed here. At C0b,
`git rev-parse HEAD:.agent/authored/f037-r26.md` and
`git rev-parse HEAD:.agent/last_block.md` both print
`a6223fec105af40eb6c19c6b4a797978c82a7e0a` — ONE blob.

**G3 THE PLAN AT C1 — PASS.** PLANF037R26 was re-extracted from the COMMITTED
C0a blob via `git show fb0ee4cb:.agent/authored/f037-r26.md` and compared with
`.agent/plan.md` at `77cec858`: BYTE EQUAL including the trailing newline
(`True`). Negative control, the same comparison with the trailing newline
dropped: `False`. `wc -l` = 44, strictly under 50. Lines exactly `## Goal`: 1.
Lines exactly `## Next Steps`: 1.

**G4 THE RECORD AT C2, both readers — PASS.** (a) `f676042c` blob of
`.agent/live_review.md` + `\n` + GATER25 == the C2 blob → `True`. NEGATIVE
CONTROL: byte offset 10 of GATER25, which the script confirmed lies INSIDE the
FIRST appended paragraph, XORed with 0x01 and the equality recomputed → `False`.
REJECTED as required. (b) The C2 blob split on blank lines; N, counted by the
script from the slice itself, is **6**; the LAST 6 units of the file match those
6 paragraphs IN ORDER, unit by unit, all `True` (lengths 929, 945, 1404, 660,
1677, 1245). The pre-round blob is a byte PREFIX of the C2 blob: `True`, 1322142
bytes growing to 1329032. Every non-current revision was read with
`git show <sha>:<path>` into memory; no tracked file was written for a
measurement.

**G5 THE LEDGER — PASS.** Base figures re-measured by this worker at `f676042c`,
not inherited: registrations `^- R-\d+ — ` 292, all DISTINCT; `^Done: R-\d+ — `
43; `^Landed: R-` 11; `^Gate: F\d+ R\d+ — ` 95; OPEN SET as a set 251. Every one
equals the figure the block states. Over the C2 blob: registrations **292**,
UNMOVED, all 292 DISTINCT; `^Done: R-\d+ — ` **43**, UNMOVED; `^Landed: R-`
**11**, UNMOVED; `^Gate: F\d+ R\d+ — ` **96**, a rise of exactly ONE; OPEN SET
**251**, UNMOVED. `Gate: F037 R25` occurs exactly **1** time in the C2 blob.
`R-0714` is present as a registration and carries NO `Done:` line, so it is STILL
OPEN — the documented Medium risk F037 closes with.

**G6 THE BUILT STATE AT C3, THE DOCS GATE AND THE CANARY — PASS.** The C2 blob of
`docs/roadmap/features/T5_F037.md` is **12982** bytes; the C3 blob is **15880**.
The C2 blob is a byte PREFIX of the C3 blob: `True`. That prefix plus BUILTSTATE
equals the C3 blob exactly: `True`. NEGATIVE CONTROL, one byte inside BUILTSTATE
(slice offset 40) XORed with 0x01 and the equality recomputed: `False` —
REJECTED. Lines starting `## Built State`: exactly **1**. Lines starting `**A6`:
still exactly **1**. Nothing above the appended section was edited, reordered or
deleted, which the byte-prefix reading proves directly. Then, one pytest process
at a time:

| Command | Exit | Result |
|---------|------|--------|
| `python3 -m pytest tests/orchestration/test_test_runner.py tests/docs/ -q` | 0 | `347 passed in 5.64s` |
| `python3 -m pytest tests/cli/test_golden_path.py -q` | 0 | `42 passed in 20.72s` |

Both equal the reviewer's readings at `38966bf3` — 347 and 42.

**G7 THE EVIDENCE JOB, THE INTEGRITY CHECK AND THE PACKAGE — PASS.** All of (j)
through (m) executed.

(j) `python3 .remedy-wt/f037_evidence.py` from the repository root, exit **0**.
Per-run lines, every `selected` equal to its `node_ids` length:

| run | selected | node_ids | files | duration |
|-----|----------|----------|-------|----------|
| vr-0001 `tests/orchestration/test_diff_parser.py` | 43 | 43 | 1 | 2.33s |
| vr-0002 `tests/orchestration/test_diff_view_source.py` | 15 | 15 | 1 | 0.26s |
| vr-0003 `tests/ui_contracts/test_diff_envelope_door.py` | 13 | 13 | 1 | 0.22s |
| vr-0004 `tests/ui_contracts/test_diff_file_sidebar.py` | 11 | 11 | 1 | 0.19s |
| vr-0005 `tests/ui_contracts/test_diff_surface_css.py` | 8 | 8 | 1 | 0.18s |
| vr-0006 `tests/ui_contracts/test_diff_view_model.py` | 8 | 8 | 1 | 0.20s |
| vr-0007 `tests/ui_contracts/test_diff_view_render.py` | 19 | 19 | 1 | 0.20s |
| vr-0008 `tests/ui_contracts/test_diff_viewer_mount.py` | 14 | 14 | 1 | 0.20s |
| vr-0009 `tests/ui_server/test_diff_endpoint.py` | 6 | 6 | 1 | 0.86s |

Nine runs, 137 tests, every one exit 0 with zero failed, zero skipped and zero
deselected — the script asserts each of those itself, so a changed count would
have been a red here. `SCAN rejected strings: 0` with the empty list `[]`
printed, against the red control `SCAN red control: True` — the scanner does
reject a local absolute path, so the 0 is a real reading and not a blind one. The
bundle result: `job_id f037-closure`, `head_commit
5e557a1c2b4f7f9187f5388b18a3712d4a5c3d7e`, `manual_completion true`,
`operator_attested_tasks T001/T002/T003`, `partition 8/8/8`, `authority_count
24`, `commit_count 198`, `total_passed 137`, `verdict PASS_WITH_RISKS`. All NINE
`OUTPUT_HASH` lines read **True** — every `output_hash` is sha256 of its
`stdout_summary` exactly.

(k) CLOSURE PRECONDITION 3, re-measured at C3 by
`run_integrity_checks()` from `packages.orchestration.integrity_gate` (the
`remedy` CLI is denied in this session). The return is an `IntegrityGateResult`
OBJECT, read by attribute: `.passed` = **True**, `.fail_count` = **0**, five
checks, every one PASS — `handler_import` PASS, `live_review_verdict` PASS,
`plan_consistency` PASS, `relevant_untracked` PASS, `high_blockers_open` PASS.
This matches the reviewer's reading at `f676042c`.

(l) THE PACKAGE, built from a CLEAN tree at C3 with
`bash scripts/make_review_zip.sh --evidence-dir <EVIDENCE_DIR>`. The script's
final output verbatim:

    ============================================
    REVIEW_PACKAGE_CREATED=true
    PACKAGE_STATUS=READY_FOR_REVIEW
    PACKAGING_CWD=/home/decodeux/Repos/remedy
    EVIDENCE_DIR=/home/decodeux/Repos/remedy/.remedy-wt/f037_closure_evidence/remedy-job-evidence-f037-closure
    REVIEW_SUBJECT_ALIGNMENT=PASS
    EVIDENCE_AUTHORITATIVE=true
    REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
    ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260828-142213-READY_FOR_REVIEW.zip
    ============================================

    ZIP CREATED AND READY FOR FINAL REVIEW

    19M	/home/decodeux/Repos/remedy-history/zips/remedy-review-20260828-142213-READY_FOR_REVIEW.zip
    Included files: 3465
    Branch: feature/f037-rendered-diff-viewer
    Commit: 5e557a1c2b4f7f9187f5388b18a3712d4a5c3d7e
    Evidence: evidence/current/

READ FROM THE MANIFEST INSIDE THE PACKAGE — member `.review_zip_manifest.json`,
opened with `zipfile` from the archived file on disk, never from the staging
tree: `package_status` = **READY_FOR_REVIEW**;
`current_evidence.evidence_freshness.evidence_authoritative` = **True** (that is
where the manifest carries the flag the script prints as
`EVIDENCE_AUTHORITATIVE`; there is no top-level key of that name, and the two
readings agree); `packaged_evidence_job_id` = `f037-closure`;
`review_package_created` = True. `committed_review_subject`:

- `base_commit` = `9dde54956afbe5f432bfd429bf4ba0bb272f6d07` — equal to the
  required base `9dde5495…`
- `head_commit` = `5e557a1c2b4f7f9187f5388b18a3712d4a5c3d7e` — EQUAL TO C3
- `base_is_ancestor` true, `commit_count` 198, `file_count` 68, `tombstones` []

PACKAGE_STATUS IS THE READING, NEVER THE EXIT CODE. The pipeline returns exit 0
for both READY_FOR_REVIEW and BLOCKED_EVIDENCE, so the exit 0 recorded above
proves nothing on its own; the status stated here is the string read out of the
manifest inside the package, and it is READY_FOR_REVIEW.

- package FILENAME: `remedy-review-20260828-142213-READY_FOR_REVIEW.zip`
- SHA-256 computed by this worker over the file on disk, streamed in 1 MiB
  chunks: `c3755b73a6cbaf21cd0547ce590aafee244d4143ace6ca1833bc93b50c87ef26`
  (19342216 bytes). It equals the `final_sha256` the pipeline printed, and the
  two were computed independently.

(m) ARCHIVED. `/home/decodeux/Repos/remedy-history/zips` — measured as an
existing writable directory now holding 20 packages, with this one present at
that absolute path. NO MOVE WAS PERFORMED because none was needed: the script's
own `REVIEW_PACKAGE_DIR` already IS the archive directory, so the package was
written there directly. The `package path` value DECISION amend0827 D1 requires
is therefore `/home/decodeux/Repos/remedy-history/zips`, and it is not
`NOT ARCHIVED`. `.remedy-wt/f037_evidence.py` was then deleted BY THAT EXACT
PATH with `os.remove` — never by a glob — and confirmed gone; the evidence
directory was left in place, 27 files under
`.remedy-wt/f037_closure_evidence/remedy-job-evidence-f037-closure`.

**G8 STRUCTURE AND THE OPEN PR GATE, measured at C3 (`5e557a1c`) — PASS.**
`git diff --name-only f676042c..5e557a1c` returns **5** paths; the change set
minus `.agent/handoff.md` is the same **5** paths. RESIDUE measured-minus-
changeset: `[]`. RESIDUE changeset-minus-measured: `[]`. Both printed, both
EMPTY. `git diff --stat f676042c..5e557a1c -- <dir>` prints the empty string
`''` for `apps/`, for `packages/` and for `tests/` — all three cases print
NOTHING. Every commit C0a through C3 is single-parent (parent count 1, five
times); insertions from `git diff --numstat`, each under 500 and each equal to
the corresponding `## Commits` cell above:

| Commit | Insertions | Under 500 |
|--------|-----------|-----------|
| `fb0ee4cb` | 490 | yes |
| `82cc2579` | 416 | yes |
| `77cec858` | 21 | yes |
| `514e2991` | 12 | yes |
| `5e557a1c` | 49 | yes |

TRANSPORT-MARKER SWEEP, counted affirmatively over each `HEAD:<path>` blob rather
than inferred from a silent `git grep`: `^<<<SLICE ` and `^<<<END ` are **0 and
0** in `.agent/plan.md`, **0 and 0** in `.agent/live_review.md` and **0 and 0**
in `docs/roadmap/features/T5_F037.md`, against the non-zero control
`.agent/authored/f037-r26.md`, which reports **4 and 4** — one pair per slice.
BUILD-OUTPUT GLOB SWEEP, re-measured rather than inherited, the fix clause
`R-0677` binds on a change set carrying an evidence path — `git ls-files` over
each `.gitignore` build-output glob: `*.zip` 0, `*.log` 0, `*.egg` 0,
`*.egg-info` 0, `build` 0, `*/build/*` 0, `dist` 0, `*/dist/*` 0, `node_modules`
0, `*/node_modules/*` 0, `sdist` 0, `packages.zip` 0, `remedy-job-evidence-*` 0.
TOTAL **0** — EMPTY. `git ls-files .remedy-wt | wc -l` = **0**: neither the
evidence directory nor the zip nor the scratch script ever entered the index, and
`git status --porcelain` stayed 0 after the build, so nothing showed up as
untracked either. `gh pr list --state open --json
number,headRefName,baseRefName,isDraft` → `[]`, no open PRs, so the Open PR Gate
is clear and nothing was merged.

## Authored-text proofs

Four reviewer-authored slices were applied this round. Every one was re-extracted
from the COMMITTED `.agent/authored/f037-r26.md` blob — not from the session's
copy of the block — and compared on disk.

| Slice | Target | Result |
|-------|--------|--------|
| PLANF037R26 | `.agent/plan.md` at `77cec858` | BYTE EQUAL including trailing newline (`True`); negative control dropping that newline `False` |
| GATER25 | `.agent/live_review.md` at `514e2991` | Reader (a) equality `True`, negative control inside its first paragraph `False`; reader (b) all 6 tail paragraphs match in order |
| BUILTSTATE | `docs/roadmap/features/T5_F037.md` at `5e557a1c` | Prefix + slice equality `True`, negative control inside the slice `False`; its leading blank line came from the slice, no newline was added by hand |
| EVIDENCESCRIPT | `.remedy-wt/f037_evidence.py` (untracked scratch, then deleted) | Written byte for byte, 5762 bytes, sha256 `96fbcce2b534d5cdba83ede0ec68dd7bd0d374132b49ba7e78b4e2daa6d4fbb7`; executed unmodified from the repository root |

No slice was reflowed, reworded, retitled, corrected or shortened. The delimiter
lines never reached a target file — G8's marker sweep measures 0 in all three
tracked targets.

## Deviations & assumptions

1. **The ordered commit sequence C0a, C0b, C1, C2, C3, C4 was followed exactly.**
   No extra commit, no dropped commit, no reordering. Nothing was committed
   between C3 and the zip build, as constraint 6 requires.
2. **Shell-guard re-expressions (constraint 9).** Two command FORMS were rejected
   by this session's guard and were re-expressed rather than weakened or skipped;
   no gate lost coverage. (a) A `python3 - <<'PY'` heredoc whose pattern table was
   a BRACE LITERAL CONTAINING QUOTES (`pats = { "name": r"regex" }`) was rejected;
   the identical measurement was re-expressed with a list of tuples built by
   `pats.append((...))`, with no `{` or `}` in the source, and produced the G5
   figures reported above. (b) `python3 -m pytest … | tail -12 ; echo
   "${PIPESTATUS[0]}"` was rejected for the INDEXED EXPANSION; both G6 suites were
   re-expressed as `subprocess.run(cmd, cwd=R, capture_output=True)` with
   `p.returncode` printed, which yields the REAL exit code of pytest itself rather
   than of a pipeline — a stronger reading than the rejected form, not a weaker
   one.
3. **The package needed no move, so (m)'s move step was a no-op.** The block
   orders the package moved to `/home/decodeux/Repos/remedy-history/zips`;
   `make_review_zip.sh` writes its output to that directory itself
   (`REVIEW_PACKAGE_DIR`), so the package was already at the archived path when
   the script finished. Presence at the absolute path was verified rather than
   assumed. Nothing was moved, nothing was copied, and the recorded `package path`
   is the real directory the file is in.
4. **The push outcome is not written into this file.** Recording it here would
   require a value that cannot exist when the text is written, and the write-once
   rule forbids a second handoff commit. It is reported in the session output and
   is independently measurable by comparing `git rev-parse HEAD` with
   `git rev-parse origin/feature/f037-rendered-diff-viewer`.
5. **The Session section carries the rule-6 scope report.** Both soft limits — 25
   rounds and 7 sessions — are exceeded at round 26 of session 8, and
   `docs/agents/handback_template.md` makes the scope report mandatory in that
   state. The block ordered the Session line and its roster; the report is the
   template's own obligation on top of it, not new work, and it restates R24's
   D11/A6 ruling rather than re-opening it.
6. **No assumption was carried from the block's numbers.** Every base figure the
   block states — the 292/43/11/95/251 ledger readings, the 347 and 42 suite
   readings, the integrity result, the archive directory's existence and
   writability, the nine per-suite expected counts — was independently
   re-measured here, and each matched.
7. **No test was edited, added, deleted or skipped, and nothing under `apps/`,
   `packages/` or `tests/` was touched.** G8's three restricted stats print
   nothing, which proves it rather than asserting it.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block | done | `fb0ee4cb` |
| C0b mirror the block | done | `82cc2579` |
| C1 the plan | done | `77cec858` |
| C2 the R25 verdict | done | `514e2991` |
| C3 the Built State section | done | `5e557a1c` — the accepted HEAD |
| the evidence job and the review zip | done | run from the clean tree at C3, nothing committed in between |
| C4 the handback | done | this commit, then the push |
| G1 hygiene | done | STOP absent twice, base SHA equal, branch correct, 6×0 porcelain |
| G2 transport | done | digests EQUAL against the pre-existing original; one blob `a6223fec` |
| G3 the plan at C1 | done | byte equal, control False, 44 lines, 1 and 1 |
| G4 the record at C2 | done | reader (a) True with control False; reader (b) N=6 in order; prefix True |
| G5 the ledger | done | 292 / 43 / 11 / 96 / open 251; `Gate: F037 R25` once; `R-0714` still open |
| G6 built state, docs gate, canary | done | prefix+slice True with control False; 1 and 1; 347 and 42, both exit 0 |
| G7 evidence, integrity, package | done | 9 runs 137 passed; scan 0 with red control True; 9 OUTPUT_HASH True; integrity passed=True fail_count=0, 5 PASS; READY_FOR_REVIEW; head equals C3 |
| G8 structure and Open PR Gate | done | residue empty both ways; 3 restricted stats empty; 5 single-parent commits; markers 0/0/0 vs control 4; glob sweep 0; `gh pr list` `[]` |

## Open findings

**251** open, computed AS A SET over the C2 blob — 292 distinct registered ids
minus 43 distinct `Done:` ids — UNMOVED from `f676042c`, because this round
registered nothing and resolved nothing. F037 carries no open finding of its own.
`R-0714` remains open and is carried into closure as a DOCUMENTED MEDIUM RISK: it
is a defect in a `tests/ui_server/` test that F037 does not own, its
counter-measure is recorded in the finding itself, and repairing it here would be
scope drift.

## Next

The STATUS round — F037's last. In ONE commit: the `[x]` line for F037 in
`docs/roadmap/STATUS.md`, the README capability paragraph, the README accepted
count with its `Next:` clause, and the README tier row. The STATUS line's
closure segments come from this handback and have no other source: `Evidence job
f037-closure · package remedy-review-20260828-142213-READY_FOR_REVIEW.zip ·
SHA-256 c3755b73a6cbaf21cd0547ce590aafee244d4143ace6ca1833bc93b50c87ef26 ·
package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD
5e557a1c2b4f7f9187f5388b18a3712d4a5c3d7e`. Then the closure PR, which that round
creates and does NOT merge.

The next session applies Phase 1 rule 1 (read `.agent/STOP`) BEFORE rule 2 (the
Open PR Gate), in that order.
