# Handback — F256 Diff viewer completion, round 9 (THE INTEGRATION GATE AND THE PACKAGE)

## Session

SESSION 2 of feature F256 · round 9 · rounds so far 9

## Range

Review of f69bff0d..HEAD (branch `feature/f256-diff-viewer-completion`).

## Commits

### c46042a9 chore(f256): save the round 9 block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f256-r9.md` | +409 / -0 | C0a: the block copied byte for byte from `.remedy-wt/f256-r9-block.md` |

### 1adc10d2 chore(f256): mirror the round 9 block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +337 / -250 | C0b: written from the COMMITTED C0a blob, so the two are one blob id |

### c47ad2ea docs(f256): advance the plan to the closure package round
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +15 / -14 | C1: whole-file replacement by the `PLANF256R9` slice |

### c6775b3c docs(f256): book the round 8 verdict
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +12 / -0 | C2: append of the `GATEF256R8` slice. THIS COMMIT IS THE ACCEPTED HEAD |

### C3 (this commit) chore(f256): hand back round 9
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | C3: this handback; a handoff cannot table the commit that writes it |

Every `+/-` cell above was taken from `git diff --numstat <sha>^ <sha>` and agrees
cell for cell with the figures G1 reports below. Nothing was committed between C2
and the zip build.

## VALUES FOR THE CLOSURE STATUS LINE (next round reads these)

| Field | Value |
|---|---|
| Evidence job | `f256-closure` |
| package | `remedy-review-20260828-233819-READY_FOR_REVIEW.zip` |
| SHA-256 | `5f18d7acdeab790b0f79181c7179023535b389ce0b76ec427f2765b20cda4ad5` |
| package path | `/home/decodeux/Repos/remedy-history/zips` |
| accepted HEAD | `c6775b3c41f1d1fa4b0f4bb7907307573855a61b` |

The SHA-256 was computed by the worker over the file on disk in the archived
directory; it agrees with the `final_sha256` the packaging pipeline printed. The
evidence directory is NOT committed, so this table is the durable carrier of these
five values.

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`
  (constraint 0, before anything), and `[]` again after the archive (G8). No PR
  created, none merged, nothing force-pushed, rebased or amended.
- `bash scripts/make_review_zip.sh --evidence-dir <evidence dir>` → exit 0,
  `PACKAGE_STATUS=READY_FOR_REVIEW`. Raw log
  `.remedy-wt/f256-r9-zip-build.txt`.
- `git push -u origin feature/f256-diff-viewer-completion` after C3 — outcome
  recorded in the round report.
- No `git worktree add` and no `git worktree remove`; every gate ran in the
  primary checkout.

## Verification

STOP sentinel, both ordered reads with `os.path.exists`:
`/home/decodeux/Repos/remedy/.agent/STOP` — before C0a: `False`; before C3: `False`.

`git rev-parse HEAD` before C0a = `f69bff0d417e90f1a1e8ae78760a807825297cce`, the
ordered base `f69bff0d`. `git branch --show-current` =
`feature/f256-diff-viewer-completion`. `git status --porcelain | wc -l` = 0 after
each of C0a, C0b, C1, C2 and again after the package was archived.

G1 HYGIENE AND STRUCTURE — PASS. `git diff --name-only f69bff0d..c6775b3c` lists
exactly four paths: `.agent/authored/f256-r9.md`, `.agent/last_block.md`,
`.agent/live_review.md`, `.agent/plan.md`. With `.agent/handoff.md` set aside both
residues are empty, printed in both directions: actual−expected `[]`,
expected−actual `[]`. `git diff --stat f69bff0d..c6775b3c` restricted to `apps/`,
to `packages/`, to `tests/` and to `docs/` prints NOTHING in all four cases.
Insertions per commit, each under 500 and each single-parent: C0a 409, C0b 337,
C1 15, C2 12. Marker sweep at C2, lines beginning `<<<SLICE ` / `<<<END `:
`.agent/plan.md` 0/0 and `.agent/live_review.md` 0/0, against the non-zero control
`.agent/authored/f256-r9.md` 3/3. Tracked build outputs across every `.gitignore`
glob — `*.zip`, `*.log`, `dist`, `build`, `node_modules`, `sdist`, `packages.zip`,
`remedy-job-evidence-*` — TOTAL 0. `git ls-files .remedy-wt | wc -l` = 0.

G2 TRANSPORT — PASS. `git show c46042a9:.agent/authored/f256-r9.md` is 23804 bytes,
sha256 `8237c1e4fdcde6ab70e6a0a2a3abc79c559ee3e8d7f5e75d206f819f73d559db`; the
reviewer's own original `.remedy-wt/f256-r9-block.md` is 23804 bytes with the same
digest; EQUAL `True`. That original predates this worker and was not written by it,
so the reading covers the reviewer-to-disk transport and not merely this worker's
self-consistency. At C0b, `.agent/authored/f256-r9.md` and `.agent/last_block.md`
are ONE blob id: `ae975426794bfd4e53f8fc51bca78973f13e5b5f` for both.

G3 THE PLAN AT C1 — PASS. `.agent/plan.md` at `c47ad2ea` equals `PLANF256R9`
including the trailing newline: `True` (1536 bytes on both sides). `wc -l` 34,
under 50. Lines exactly `## Goal`: 1. Lines exactly `## Next Steps`: 1.

G4 THE RECORD AT C2 — PASS. (a) The `f69bff0d` blob of `.agent/live_review.md`
(1365713 bytes) plus a newline plus `GATEF256R8` (3655 bytes) equals the C2 blob
(1369369 bytes): `True`. The pre-round blob is a byte PREFIX: `True`. NEGATIVE
CONTROL: one byte flipped at offset 1365754, which the script confirms lies inside
the first appended paragraph spanning [1365714, 1365998) — context
`b' MEASUREMENT round, '` — and the equality became `False`.
(b) N was COUNTED BY THE SCRIPT from the slice, not taken from the block: N = 6.
The last 6 blank-line units of the file match those paragraphs IN ORDER: `True`,
both stripped and raw.

G5 THE LEDGER AT C2 — PASS, and it moved exactly as a round that registers and
resolves nothing should. Base `f69bff0d` → C2 `c6775b3c`: `^- R-\d+ — ` 293 → 293,
all DISTINCT in both; `^Done: R-\d+ — ` 43 → 43; `^Landed: R-` 11 → 11; the OPEN
SET as a set 252 → 252; `^Gate: F\d+ R\d+ — ` 104 → 105, a rise of exactly ONE.
`Gate: F256 R8` occurs exactly 1 time. `.agent/candidates.md` at C2 carries no
candidate entry — its body is the header block quote plus the paragraph beginning
`EMPTY.`.

G6 THE INTEGRATION GATE, closure precondition 2 — PASS, run at C2 from the
repository root in the primary checkout, one pytest process.

`apps/ui/dist` was checked FIRST and is NOT stale: newest mtime under
`apps/ui/src` is 1787951094.49 (`src/api/diffViewModel.test.ts`), newest under
`apps/ui/dist` is 1787951206.16 (`dist/index.html`), so dist is the newer of the
two and no `npx vite build` warm-up was needed or run.

    ["python3", "-B", "-m", "pytest", "-n", "auto", "-q"]   → REAL exit code 0

Final summary line, verbatim: `18150 passed, 20 skipped in 145.57s (0:02:25)`.
Wall clock measured by the wrapper: 146.1 s. The FULL raw output is saved at
`.remedy-wt/f256-r9-integration-gate.txt`. The reviewer measured 18150 passed and
20 skipped at `f69bff0d`; the re-measurement at C2 is IDENTICAL in both counts.
The wall clock differs — 145.57 s here against the reviewer's 104.3 s — and is
reported rather than explained away; the counts, which are the gate, agree exactly.
The gate was not red, so no failure list is reproduced.

G7 THE EVIDENCE JOB AND THE INTEGRITY CHECK — PASS.

(j) `.remedy-wt/f256_evidence.py`, extracted from the COMMITTED C0a blob and run
with `python3` from the repository root. Every `selected` equals its `node_ids`
length and every `files` count is 1:

    vr-0001 selected 43 node_ids 43 files 1 dur 2.3
    vr-0002 selected 15 node_ids 15 files 1 dur 0.26
    vr-0003 selected 13 node_ids 13 files 1 dur 0.22
    vr-0004 selected 16 node_ids 16 files 1 dur 0.2
    vr-0005 selected 8  node_ids 8  files 1 dur 0.18
    vr-0006 selected 8  node_ids 8  files 1 dur 0.2
    vr-0007 selected 25 node_ids 25 files 1 dur 0.21
    vr-0008 selected 14 node_ids 14 files 1 dur 0.2
    vr-0009 selected 8  node_ids 8  files 1 dur 2.63

`SCAN rejected strings: 0 []` with `SCAN red control: True`. The bundle result:
`job_id` `f256-closure`, `head_commit`
`c6775b3c41f1d1fa4b0f4bb7907307573855a61b` (= C2), `manual_completion` true,
`operator_attested_tasks` T001/T002/T003, `partition` 4/4/4, `authority_count` 12,
`commit_count` 55, `total_passed` 150, `verdict` `PASS_WITH_RISKS`. All nine
`OUTPUT_HASH` lines read `True`. The evidence directory is 113 files under
`.remedy-wt/f256_closure_evidence/remedy-job-evidence-f256-closure` and is
gitignored; it was left in place per step (m).

(k) Closure precondition 3, run through
`packages.orchestration.integrity_gate.run_integrity_checks` because the `remedy`
CLI is denied in this session. The return is an `IntegrityGateResult` object:
`.passed` `True`, `.fail_count` `0`, and all five checks PASS —
`handler_import` PASS, `live_review_verdict` PASS, `plan_consistency` PASS,
`relevant_untracked` PASS, `high_blockers_open` PASS.

G8 THE PACKAGE — PASS. Built from a CLEAN tree at C2
(`git status --porcelain` = 0) with
`bash scripts/make_review_zip.sh --evidence-dir /home/decodeux/Repos/remedy/.remedy-wt/f256_closure_evidence/remedy-job-evidence-f256-closure`.
The script's final output, verbatim:

    ============================================
    REVIEW_PACKAGE_CREATED=true
    PACKAGE_STATUS=READY_FOR_REVIEW
    PACKAGING_CWD=/home/decodeux/Repos/remedy
    EVIDENCE_DIR=/home/decodeux/Repos/remedy/.remedy-wt/f256_closure_evidence/remedy-job-evidence-f256-closure
    REVIEW_SUBJECT_ALIGNMENT=PASS
    EVIDENCE_AUTHORITATIVE=true
    REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
    ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260828-233819-READY_FOR_REVIEW.zip
    ============================================

    ZIP CREATED AND READY FOR FINAL REVIEW

    18M	/home/decodeux/Repos/remedy-history/zips/remedy-review-20260828-233819-READY_FOR_REVIEW.zip
    Included files: 3337
    Branch: feature/f256-diff-viewer-completion
    Commit: c6775b3c41f1d1fa4b0f4bb7907307573855a61b
    Evidence: evidence/current/

PACKAGE_STATUS WAS READ FROM THE MANIFEST INSIDE THE PACKAGE, NOT INFERRED FROM AN
EXIT CODE. The pipeline returns exit 0 for both READY_FOR_REVIEW and
BLOCKED_EVIDENCE, so the exit code alone proves nothing; the reading below opens
the zip and parses `.review_zip_manifest.json` (10825 bytes, sha256
`4f9ec25cfd730a88b798778da7daae1c2c889e7c155820fbe1508c0fcb33382a`):

- `package_status` = `READY_FOR_REVIEW`
- `current_evidence.evidence_freshness.evidence_authoritative` = `true`
- `committed_review_subject.base_commit` =
  `0e8ab5b4f780b5265a6aa604ee89067399046b1e` — equals the ordered base, `True`
- `committed_review_subject.head_commit` =
  `c6775b3c41f1d1fa4b0f4bb7907307573855a61b` — equals C2, `True`
- `ready_gate_matrix.ok` = `true`, `blocking_reasons` `[]`,
  `packaging_warnings` `[]`, `external_paths_detected` `[]`,
  `git_status_snapshot.status` = `OK`

Package FILENAME `remedy-review-20260828-233819-READY_FOR_REVIEW.zip`, 18076792
bytes, SHA-256 computed by the worker over the file on disk
`5f18d7acdeab790b0f79181c7179023535b389ce0b76ec427f2765b20cda4ad5`, which agrees
with the `final_sha256` the pipeline printed. ABSOLUTE ARCHIVED DIRECTORY:
`/home/decodeux/Repos/remedy-history/zips` (existing, writable, 21 entries
including this package). `gh pr list --state open` after the archive: `[]`.

## Authored-text proofs

Three reviewer-authored slices were carried this round, every one extracted from
the COMMITTED blob `git show c46042a9:.agent/authored/f256-r9.md` per constraint 3
and never from the prompt text. That blob is byte-equal to the reviewer's original
`.remedy-wt/f256-r9-block.md` at 23804 bytes, sha256
`8237c1e4fdcde6ab70e6a0a2a3abc79c559ee3e8d7f5e75d206f819f73d559db` (G2).

| Slice | Target | Disk-to-disk result |
|---|---|---|
| `PLANF256R9` | `.agent/plan.md` | whole-file equality including trailing newline, `True` (G3) |
| `GATEF256R8` | `.agent/live_review.md` | base + `\n` + slice equals the C2 blob, `True`; prefix `True`; negative control `False` (G4) |
| `EVIDENCESCRIPT` | `.remedy-wt/f256_evidence.py` (untracked, gitignored) | written from the committed blob, run, then deleted by exact path at step (m); applied to no tracked file |

The `<<<SLICE` / `<<<END` delimiters reached no target file: G1's marker sweep
reads 0/0 in both tracked targets, against 3/3 in the authored control.

## Deviations & assumptions

The ordered commit sequence was followed exactly — C0a, C0b, C1, C2, C3, in that
order, with no extra commit, no dropped commit and no reordering. Nothing was
committed between C2 and the zip build. No slice was reflowed, reworded, shortened
or corrected.

1. GUARD RE-EXPRESSION (constraint 6). `ls -la /home/decodeux/Repos/remedy-history/zips`
   chained with a `find` was refused by this session's command guard
   ("requires approval"), and a `... | xxd` tail chain was refused likewise. Both
   were RE-EXPRESSED, not weakened, as script files under `.remedy-wt/`
   (`r9_archive.py`, and the byte-level checks folded into `r9_g2345.py`) which
   read the same facts through Python `os`/`glob` and byte slicing. No check was
   skipped and none was made cheaper.
2. GUARD RE-EXPRESSION (constraint 6). Every multi-step computation this round ran
   from a script file under the gitignored `.remedy-wt/` — `r9_c0a.py`,
   `r9_c0b.py`, `r9_extract.py`, `r9_c2.py`, `r9_g1.py`, `r9_g2345.py`,
   `r9_dist.py`, `r9_g6.py`, `r9_integrity.py`, `r9_zip.py`, `r9_manifest.py`,
   `r9_manifest2.py`, `r9_manifest3.py`, `r9_manifest4.py`, `r9_list.py`,
   `r9_list2.py`, `r9_archive.py`, `r9_stop.py` — because this session's guard
   rejects `for`/`while` loops, `$( )` substitution and `python3 - <<'PY'`
   heredocs by FORM, and /tmp is denied. `git ls-files .remedy-wt` is 0, so none
   of them entered the commit range.
3. DEVIATION FROM STEP (m), and it is a no-op in the worker's favour. Step (m)
   ordered the package MOVED to `/home/decodeux/Repos/remedy-history/zips`. The
   packaging pipeline WRITES there directly — `REVIEW_PACKAGE_DIR` and `ZIP_PATH`
   in its own output both name that directory — so the package was already at the
   archive destination and NO move was performed. The recorded `package path` is
   the same absolute directory the block named, and the file was verified present
   there at 18076792 bytes with the reported SHA-256. Nothing was left inside the
   repository by this round.
4. DECLARED, per constraint 1 — a slice applied as written that the worker
   believes overstates the disk at the moment it lands. `PLANF256R9` marks "the
   integration gate | done" and "the evidence bundle and the package | done" in
   the item table, and C1 commits that text BEFORE G6, G7 and G8 have run; the
   block's own bundle order puts the plan commit ahead of the pipeline. The slice
   was applied byte for byte and unchanged, as constraint 1 requires. Both claims
   were true by the end of the round: the gate passed and the package is
   READY_FOR_REVIEW.
5. READING, not a defect (G8). The manifest carries no TOP-LEVEL key
   `evidence_authoritative` and no top-level `review_subject_alignment`; the block
   names both as things to report from the manifest. `evidence_authoritative` was
   read at `current_evidence.evidence_freshness.evidence_authoritative` = `true`,
   which agrees with the `EVIDENCE_AUTHORITATIVE=true` line the pipeline printed,
   and `REVIEW_SUBJECT_ALIGNMENT=PASS` is likewise a pipeline stdout field. Both
   readings are reported with their real locations rather than as top-level keys.
6. NOTED, not this round's artifact. A stale package from an earlier session,
   `/home/decodeux/Repos/remedy/remedy-review-20260823-135731-READY_FOR_REVIEW.zip`,
   sits gitignored in the repository root. It was NOT created, moved or deleted by
   this round — the change set does not name it and deleting another round's
   artifact is not this round's business. It is tracked by nothing: G1's
   `git ls-files *.zip` is 0 and `git status --porcelain` is 0.
7. NOTED, an internal manifest figure. `review_subject_evidence_alignment`
   reports `dirty_file_count_total: 1` while `dirty_source_test_files` is `[]`,
   `git_status_snapshot.status` is `OK` and the worker's own
   `git status --porcelain` was 0 at the build. Reported because it is a number a
   reviewer will meet in the manifest; it did not block the package and the
   `ready_gate_matrix` is `ok: true` with no blocking reasons.
8. `.agent/context.md` and `.agent/decisions.md` were NOT touched: the change set
   names neither, this round makes no new technical decision of its own, and the
   scope and constraints of the branch are unchanged from round 8.
9. NO pull request was created and nothing was merged, per constraint 0 and the
   block's closing line. `docs/roadmap/STATUS.md` and `README.md` were not touched
   by a byte — G1's restricted `git diff --stat` over `docs/` prints nothing.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | `c46042a9` |
| C0b mirror the block | done | `1adc10d2` |
| C1 advance the plan | done | `c47ad2ea` |
| C2 book the round 8 verdict | done | `c6775b3c` — the ACCEPTED HEAD |
| C3 rewrite the handback | done | this commit |
| G1 hygiene and structure | done | PASS |
| G2 transport | done | PASS |
| G3 the plan at C1 | done | PASS |
| G4 the record at C2 | done | PASS |
| G5 the ledger at C2 | done | PASS |
| G6 the integration gate | done | PASS — exit 0, 18150 passed, 20 skipped |
| G7 the evidence job and the integrity check | done | PASS — bundle written, `passed=True`, `fail_count=0` |
| G8 the package | done | PASS — READY_FOR_REVIEW, archived |

## Next

The closure commit: apply the reviewer-authored STATUS `[x]` line for F256 —
built from the evidence job id, package filename, SHA-256, package path and
accepted HEAD in the table above — together with the README capability sync in ONE
commit, then open the closure PR per the AGENTS.md workflow. The PR is NOT merged
this session; the gap is the operator's manual-review window.
