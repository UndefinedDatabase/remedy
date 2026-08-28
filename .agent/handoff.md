# Handoff — F257 self-use track, round 5

## Session

SESSION 2 of feature F257 · round 5 · rounds so far 5

## Range

Review of `f594cf3b..HEAD` (HEAD = the C5 commit that writes this file).

## Commits

### 6f0555c8 chore(f257): save the round 5 step block verbatim — C0a

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f257-r5.md` | +465/-0 | the block saved verbatim by `shutil.copyfile` from `.remedy-wt/f257-r5-block.md` |

### 98f15a82 chore(f257): mirror the round 5 block to last_block — C0b

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +255/-174 | the same bytes mirrored from the COMMITTED blob; one blob id with the authored copy |

### 292aa618 docs(f257): advance the plan to the documentation round — C1

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +8/-6 | whole-file replacement by slice `PLANF257R5` |

### 86c6fcfd docs(f257): book the round 4 verdict and register R-0735 — C2

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +12/-0 | slices `GATEF257R4` then `FINDF257R5`, each appended under constraint 8 |
| `.agent/prose_slips.md` | +3/-0 | slice `SLIPSF257R4` appended under constraint 8 (two slip lines plus the one blank separator) |

### 059bc072 fix(f257): refuse a self-use id that is not one file name — C3

| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/self_use_job.py` | +31/-7 | S2/S3/S5: the single-component check ahead of the resolved containment check, the WHY comment stating the two different questions, the `Raises:` line and the Public API block |
| `tests/orchestration/test_self_use_job.py` | +65/-0 | S4: seven new tests in their own class, every destination under `tmp_path`; the eleven existing tests are untouched |

### 26c953ce docs(f257): document the self-use track and register it in the index — C4

| Path | +/- | Reason |
|------|-----|--------|
| `docs/system/self-use-track-v1.md` | +91/-0 | the NEW page, created whole from the `DOCPAGE` slice |
| `docs/README.md` | +2/-0 | PAIR A adds the quick-find row; PAIR B adds the System Documentation row in its alphabetical place |

### C5 — this handoff commit

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | the round handback; a handoff cannot table the commit that writes it (R-0149 pattern) |

Every `+/-` cell above was taken from `git diff --numstat` per commit and compared
cell by cell against the figures G8 reports; all six commits agree.

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`, REAL exit 0.
- `git worktree add .remedy-wt/f257-r5-g6 059bc072` → added detached at C3; used for G6 only.
- `git worktree remove --force /home/decodeux/Repos/remedy/.remedy-wt/f257-r5-g6` → removed BY EXACT PATH, never by glob; `git worktree list` then shows the primary alone.
- `git push origin feature/f257-self-use-track` → outcome recorded in the session output.
- No pull request was created. Nothing was merged. No force-push, no history rewrite.

## Verification

One line per gate, with the result actually measured.

- **G1 HYGIENE — PASS.** `.agent/STOP` read from disk with `os.path.exists` twice:
  before C0a `False`, before C3 `False`. Constraint 0: `gh pr list …` printed
  `[]` at REAL exit 0; `git rev-parse HEAD` printed
  `f594cf3b06b055190ba2d37402c08bc6a352f707`; `git branch --show-current` printed
  `feature/f257-self-use-track`. `git status --porcelain | wc -l` after each
  commit: C0a 0, C0b 0, C1 0, C2 0, C3 0, C4 0.
- **G2 TRANSPORT — PASS.** Committed blob `6f0555c8:.agent/authored/f257-r5.md`
  sha256 `9434d5f16f3406d3d404c52d8e461cc2383e9db53d4fa9e1401d0dccb13aa944`,
  29290 bytes; reviewer original `.remedy-wt/f257-r5-block.md` sha256
  `9434d5f16f3406d3d404c52d8e461cc2383e9db53d4fa9e1401d0dccb13aa944`, 29290
  bytes; **EQUAL True**. That original was written before this worker existed, so
  the reading covers more than self-consistency; and it covers no emission,
  because this workflow has none — the block was never retyped, only copied by
  `shutil.copyfile`. `git rev-parse 98f15a82:.agent/authored/f257-r5.md` and
  `git rev-parse 98f15a82:.agent/last_block.md` both print the single blob id
  `cfed21998b7dfb6a9ce370ab43af5444d84158df`.
- **G3 THE PLAN AT C1 — PASS.** `.agent/plan.md` at C1 equals `PLANF257R5`
  including the trailing newline: **True**, 1768 bytes on both sides. `wc -l`
  **37**, under 50 True. Lines exactly `## Goal`: **1**. Lines exactly
  `## Next Steps`: **1**.
- **G4 THE RECORD APPENDS AT C2 — PASS.** `.agent/live_review.md` reconstructed
  from the `f594cf3b` blob plus `GATEF257R4` plus `FINDF257R5`, applied IN THAT
  ORDER each under constraint 8: **True**; base 1388216 bytes, rebuilt 1393448,
  C2 blob 1393448. NEGATIVE CONTROL: byte at absolute offset 1388317 — the script
  asserted it lies inside the FIRST appended paragraph, which spans
  1388217..1391489 — XORed with 0x01; reconstruction then **False**. The
  pre-round blob is a byte PREFIX of the C2 blob: **True** (1388216 → 1393448).
  The C2 blob ends in exactly ONE newline: **True**. Separately,
  `.agent/prose_slips.md` at C2 reconstructs from its `f594cf3b` blob plus
  `SLIPSF257R4` under constraint 8: **True** (16258 → 16759 bytes), and
  `SLIPSF257R4` contributes exactly **TWO** lines.
- **G5 THE LEDGER AT C2 — PASS, counted by DISTINCT ID per constraint 9.**
  At `f594cf3b` / at C2 — lines matching `^- R-\d+ — `: **295 / 296**, all
  DISTINCT True / True; lines matching `^Done: R-\d+ — `: **44 / 44** with
  DISTINCT ids among them **42 / 42** (the two numbers differ exactly as
  constraint 9 anticipates), both UNMOVED; `^Landed: R-`: **11 / 11**, UNMOVED;
  `^Gate: F\d+ R\d+ — `: **109 / 110**, a rise of exactly one. OPEN SET
  `len(set(registered) - set(resolved))`: **253 → 254**, exactly the one id this
  round registers. `^Gate: F257 R4 — ` at C2: **1**. `^- R-0735 — ` at C2: **1**.
- **G6 THE RED-PROOF AT C3 — PASS**, run only inside
  `.remedy-wt/f257-r5-g6` (worktree added detached at `059bc072`), never in the
  primary. Command each time:
  `python3 -B -m pytest tests/orchestration/test_self_use_job.py -q -p no:cacheprovider`,
  with `__pycache__` purged before every run. Pristine module sha256
  `1edd7b4533f90fc844ccddd3c7618e0cd5b6afe9f251af680508f6bc45c2106d`.
  - CONTROL FIRST, unmutated: REAL exit **0**, `18 passed in 0.24s`.
  - MUTATION (i), the NEW single-component check DELETED so only the `f594cf3b`
    guard remains — the R-0735 regression: REAL exit **1**,
    `4 failed, 14 passed in 0.29s`. The four are
    `test_a_self_normalising_id_raises_the_modules_own_error`,
    `test_a_self_normalising_id_does_not_leak_a_file_not_found_error`,
    `test_a_single_dot_id_is_refused` and `test_a_double_dot_id_is_refused`.
    Reverted before the next.
  - MUTATION (ii), the resolved containment check DELETED, the new
    single-component check kept: REAL exit **1**, `1 failed, 17 passed in 0.25s`,
    the one being `test_a_symlinked_destination_is_still_refused_by_containment`.
    Reverted.
  - MUTATION (iii), the verbatim-bytes rule broken — `write_self_use_job_file`
    appends a trailing line instead of writing `entry.job_markdown` verbatim:
    REAL exit **1**, `2 failed, 16 passed in 0.25s`
    (`test_rendered_bytes_equal_the_curated_bytes` and
    `test_an_ordinary_id_still_writes`). Reverted.
  - CONTROL AGAIN, module restored byte-clean (byte equality against the pristine
    bytes: **True**, sha256
    `1edd7b4533f90fc844ccddd3c7618e0cd5b6afe9f251af680508f6bc45c2106d`): REAL
    exit **0**, `18 passed in 0.23s`.
  - The whole sequence ran TWICE with identical exit codes and counts, so the
    colours are not one-shot readings.
  - After `git worktree remove --force /home/decodeux/Repos/remedy/.remedy-wt/f257-r5-g6`
    (exact path, never a glob): `git worktree list` shows
    `/home/decodeux/Repos/remedy  059bc072 [feature/f257-self-use-track]` alone,
    and `git status --porcelain | wc -l` in the primary is **0**.
- **G7 THE SUITES AT C4 — PASS, all eight exit 0.** One pytest process at a time,
  from the repository root, in the PRIMARY checkout, each as
  `python3 -B -m pytest <path> -q -p no:cacheprovider`. All eight ordered paths
  were confirmed to resolve on disk FIRST — the missing list is **`[]`** — so no
  suite exited 4 silently.
  - `tests/orchestration/test_self_use_job.py` — REAL exit 0, `18 passed in 0.22s`
  - `tests/orchestration/test_self_use_queue.py` — REAL exit 0, `18 passed in 0.21s`
  - `tests/test_data_paths.py` — REAL exit 0, `23 passed in 0.25s`
  - `tests/test_path_utils.py` — REAL exit 0, `28 passed in 0.19s`
  - `tests/regression/test_named_bugs.py` — REAL exit 0, `64 passed, 6 skipped in 1.28s`
  - `tests/orchestration/test_development_artifact_boundary.py` — REAL exit 0, `18 passed in 1.39s`
  - `tests/docs/test_docs_consistency.py` — REAL exit 0, `295 passed in 0.43s`
  - `tests/cli/test_golden_path.py` — REAL exit 0, `42 passed in 20.65s`
- **G8 STRUCTURE — PASS**, over `f594cf3b..26c953ce`, the range that ends BEFORE
  the handback commit. Range paths (9): `.agent/authored/f257-r5.md`,
  `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
  `.agent/prose_slips.md`, `docs/README.md`,
  `docs/system/self-use-track-v1.md`, `packages/orchestration/self_use_job.py`,
  `tests/orchestration/test_self_use_job.py`. Changeset-minus-range residue,
  computed over the change set WITHOUT the excluded path — **the excluded path is
  `.agent/handoff.md`**, which C5 writes — is **empty**. Range-minus-changeset
  residue, computed against the FULL change set, is **empty**. Insertions and
  parents: C0a **465**, C0b **255**, C1 **8**, C2 **15**, C3 **96**, C4 **93** —
  each under 500, and each of the six is **single-parent**. Delimiter counts over
  each file's C4 content, lines beginning `<<<SLICE ` and `<<<END `:
  `.agent/plan.md` 0 and 0; `.agent/live_review.md` 0 and 0;
  `.agent/prose_slips.md` 0 and 0; `packages/orchestration/self_use_job.py` 0 and
  0; `tests/orchestration/test_self_use_job.py` 0 and 0;
  `docs/system/self-use-track-v1.md` 0 and 0; `docs/README.md` 0 and 0 — beside
  the non-zero CONTROL `.agent/authored/f257-r5.md` at **9 and 9**, which shows
  the counter can see delimiters when they are there.
  `git ls-files .remedy-wt | wc -l` = **0**.
  `git diff --numstat f594cf3b 26c953ce -- <path>` is EMPTY, i.e. **ABSENT**, for
  all three of `packages/orchestration/self_use_queue.py`,
  `scripts/self_use_queue.json` and `docs/roadmap/STATUS_closure_protocol.md`.
  THE DOC GATE, run by hand because `tests/docs/test_docs_consistency.py` covers
  only five primary docs and the new page is not among them: the C4 blob of
  `docs/system/self-use-track-v1.md` carries exactly one markdown link target,
  `../roadmap/STATUS_closure_protocol.md`, none of them `http://`, `https://` or
  `mailto:`, and it RESOLVES on disk — **True**. `docs/README.md` at C4 contains
  the string `system/self-use-track-v1.md` exactly **TWICE**.
  `git cat-file -e f594cf3b:docs/system/self-use-track-v1.md` exits **128**, so
  the page did NOT exist at the base.

Push: `git push origin feature/f257-self-use-track` — outcome recorded in the
session output; no PR was created and nothing was merged.

## Authored-text proofs

- `PLANF257R5`, `GATEF257R4`, `FINDF257R5`, `SLIPSF257R4`, `DOCPAGE`,
  `PAIRAFROM`, `PAIRATO`, `PAIRBFROM` and `PAIRBTO` were all extracted from the
  COMMITTED blob `git show 6f0555c8:.agent/authored/f257-r5.md` (constraint 3),
  never from the prompt text, by `.remedy-wt/r5_extract.py`; the delimiter lines
  were dropped as transport (constraint 2) and reach no target file, which G8's
  delimiter counts confirm at 0 in all seven targets against a 9/9 control.
- Disk-to-disk: the committed authored file and the reviewer's original
  `.remedy-wt/f257-r5-block.md` are byte-identical, sha256
  `9434d5f1…13aa944`, 29290 bytes each — G2.
- `.agent/last_block.md` shares ONE blob id with the authored copy at C0b:
  `cfed21998b7dfb6a9ce370ab43af5444d84158df`.
- Constraint 10: before replacing, `PAIRAFROM` was counted in `docs/README.md` at
  **exactly 1** occurrence and `PAIRBFROM` at **exactly 1**. Each FROM was
  replaced by its TO and nothing else in the file changed — the C4 diff to that
  file is +2/-0 and touches only those two regions.
- Constraint 11: `docs/system/self-use-track-v1.md` and both `docs/README.md`
  registrations land in the SAME commit, `26c953ce`.

## Deviations & assumptions

1. **THE SPEC'S S2 IS FACTUALLY WRONG ABOUT `..`, AND THE ORDERED BEHAVIOUR WON.**
   S2 states that `Path(entry.id).name == entry.id` refuses "both `.` and `..` —
   for `.` and `..` `Path(...).name` is the empty string". Measured here on this
   Python 3.10: `Path(".").name` is `''`, but **`Path("..").name` is `'..'`**, so
   the comparison ACCEPTS `..`. Implementing S2's mechanism literally left
   `test_a_double_dot_id_is_refused` red at `1 failed, 17 passed`, REAL exit 1 —
   the observation is a measurement, not a reading. S4 orders that `.` and `..`
   are refused, so the ordered BEHAVIOUR binds and the check ships as
   `if Path(entry.id).name != entry.id or entry.id in (".", ".."):`, with the WHY
   comment naming the `..` case outright. No character-class regex and no length
   constant were introduced, so constraint 7's reservation to `path_utils.py`
   holds. This is production code, which the block DESCRIBES rather than slices,
   so constraint 1's byte-for-byte rule does not reach it; recorded here because
   the mechanism differs from the sentence that ordered it.
2. **ONE TEST BEYOND S4's LIST, AND WITHOUT IT G6's MUTATION (ii) WOULD HAVE GONE
   GREEN.** S4 orders tests for `x/../SU-001`, `.` and `..`. Once the
   single-component check exists it refuses all four ids the R-0733 class already
   covered (`../../escaped`, the absolute id, `sub/dir`, `../escaped`), so
   deleting the resolved containment check no longer reddens anything those
   tests can see. G6 requires mutation (ii) to redden. The added test
   `test_a_symlinked_destination_is_still_refused_by_containment` makes
   `dest_dir/SU-042.md` a symlink into a sibling directory — an id that IS one
   file name, so only the resolved comparison can refuse it — which is exactly
   the symlink backstop S3 says the containment check exists for. Measured:
   mutation (ii) reddens on that test alone. Also added, for the same
   discriminating reason, `test_an_ordinary_id_still_writes`, so a mutation that
   refuses EVERY id cannot pass.
3. **Two comment lines beside the fix were made consistent with it.** The
   `SelfUseJobError` class docstring said "Two refusals wear this one error" and
   the containment comment said "its one other failure"; with a third refusal in
   the module both were stale on arrival, so they read "Three refusals" and "its
   other failures". S5 orders the `Raises:` line and the Public API block, which
   were updated as ordered; these two are the same edit carried to the two other
   sentences in the file that counted the refusals. Nothing else in the module's
   prose changed.
4. **Guard re-expressions (constraint 6), every one reported as required.** This
   session's guard rejects several ordinary shell forms BY FORM, so each was
   re-expressed rather than skipped or weakened:
   - `cp` is rejected outright → the C0a transport copy used
     `python3 -c "import shutil; shutil.copyfile(...)"`, and C0b was written from
     the COMMITTED blob through `git show` inside Python.
   - Loops, `$( )` inside a compound, `${arr[0]}`, process substitution and
     multi-operation one-liners are rejected → every gate that needed iteration
     (G4's reconstruction and negative control, G5's two-revision ledger count,
     G6's mutate/run/revert cycle with its `__pycache__` purges, G7's eight
     serial suites, G8's per-commit walk, delimiter sweep and link extraction)
     was moved into a scratch script under the gitignored `.remedy-wt/`:
     `r5_extract.py`, `r5_g4.py`, `r5_g5.py`, `r5_g6.py`, `r5_g6_nodes.py`,
     `r5_g7.py`, `r5_g8.py`. None is tracked — G8 reports
     `git ls-files .remedy-wt` = 0.
   - Brace literals containing quotes are rejected → the scratch scripts were
     created with the file-writing tool rather than typed into a heredoc.
   - All three env-var forms (`VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`)
     are rejected → the data-root isolation the job planner needs is set
     in-process by `monkeypatch.setenv` inside the existing `isolate_data_root`
     fixture; no new environment assignment was needed this round.
   - `cd X && git ...` is rejected → `git -C <path>` throughout, and `cwd=` on
     `subprocess.run` for every pytest invocation, including the worktree runs.
   - Python 3.10 forbids a backslash inside an f-string expression → every regex
     in `r5_g5.py` and `r5_g8.py` is hoisted into a named module-level constant
     and never interpolated.
   - The tool does not surface non-zero exits → every command was wrapped as
     `bash -c '<cmd>; echo "REAL_EXIT=$?"'` or run through `subprocess` and its
     `returncode` printed. No gate result is reported that was not actually seen.
5. **Constraint 8 versus the gate formulas: ONE wording disagreement, resolved in
   constraint 8's favour as it instructs.** Read literally, constraint 8's
   sentence "the bytes written are one newline, then the slice, then one newline"
   would end each target in TWO newlines, contradicting the same constraint's
   "the file ends with exactly one trailing newline". Every slice already carries
   its own terminating newline, so the bytes appended were **one newline, then
   the slice** — which yields exactly one blank-line separator and exactly one
   trailing newline, satisfying both governing clauses. G4 confirms the result
   reconstructs byte-exactly and that both targets end in one newline. Declared
   because constraint 8 asks for any disagreement to be named.
6. **Applied as written where I would have written it differently.** Constraint 1
   binds and no authored slice was corrected. One observation, for the record
   only: `PLANF257R5` marks "refuse an id that is not one file name" and
   "document the format where a reader looks" as `done` in the plan applied at
   C1, two and three commits before C3 and C4 made them true — the same pattern
   the round 4 slip records. A second, on the `DOCPAGE` slice: it was authored
   before this round's fix and so describes the loader's `^SU-\d{3}$` rule
   without mentioning the renderer's new single-file-name refusal. Neither was
   changed; both are the block author's to repair by a later append.
7. **No departure from the block's ordered commit sequence.** C0a, C0b, C1, C2,
   C3, C4, C5 were committed in exactly that order, one logical step each; no
   commit was added, dropped or reordered. This round registers R-0735 and
   resolves nothing, and no `Done:` or `Gate:` paragraph of my own was written
   anywhere — `GATEF257R4` and `FINDF257R5` are reviewer-authored text applied
   verbatim.
8. **Two extra checks beyond the block, both non-destructive.** Before C3 was
   committed, the shipped `write_self_use_job_file` was called at the base commit
   with the id `x/../SU-001` inside a scratch directory under `.remedy-wt/`, and
   it leaked `FileNotFoundError: [Errno 2] No such file or directory:
   '<scratch>/jobs/x/../SU-001.md'` — R-0735 reproduced exactly as measured, so
   the fix is aimed at the real defect. And `python3 -m ruff check` was run over
   the two C3 files (`All checks passed!`, REAL exit 0). Both are read-only and
   ordered by no gate, reported here so the record is complete.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block to `.agent/authored/f257-r5.md` | done | `6f0555c8`, byte-identical to the reviewer's original |
| C0b mirror the same bytes to `.agent/last_block.md` | done | `98f15a82`, one blob id with the authored copy |
| C1 advance `.agent/plan.md` | done | `292aa618`, whole-file `PLANF257R5` |
| C2 book the F257 R4 verdict, register R-0735, append two prose slips | done | `86c6fcfd`, all three appends under constraint 8 |
| C3 the R-0735 single-component fix and its tests | done | `059bc072`, +31/-7 and +65/-0, 18 tests green |
| C4 the documentation page and its two index registrations | done | `26c953ce`, one commit as constraint 11 requires; each FROM counted at exactly 1 first |
| C5 rewrite `.agent/handoff.md` | done | this commit |
| G1 hygiene | done | STOP False at both readings; three constraint-0 readings correct; clean tree after all six commits |
| G2 transport | done | digests EQUAL at 29290 bytes; one blob id at C0b |
| G3 the plan at C1 | done | equal including trailing newline at 1768 bytes; 37 lines; 1 and 1 |
| G4 the record appends at C2 | done | reconstruction True, negative control False, prefix holds, one trailing newline; slips file reconstructs and contributes exactly two lines |
| G5 the ledger at C2 | done | registered 295→296, `Done:` 44/42 and `Landed:` 11 unmoved, `Gate:` 109→110, open set 253→254, both single counts 1 |
| G6 the red-proof at C3 | done | control 0 at 18 passed; mutation (i) exit 1 at 4 failed; (ii) exit 1 at 1 failed; (iii) exit 1 at 2 failed; restored control 0 byte-clean; worktree removed by exact path, primary clean |
| G7 the suites at C4 | done | all eight paths resolved, all eight REAL exit 0 |
| G8 structure | done | both residues empty; six single-parent commits under 500; delimiters 0 in seven targets against a 9/9 control; `.remedy-wt` untracked; all three untouched paths absent; the new page's one link resolves; `system/self-use-track-v1.md` twice in the index; the page absent at base |

## Open findings

**254 open**, counted by DISTINCT ID per constraint 9 (`len(set(registered) -
set(resolved))`), risen from 253 at `f594cf3b` by exactly the one id this round
registers, R-0735. R-0735 is repaired in C3 but NOT resolved here — the record
carries no `Done:` line for it, because a resolution is the reviewer's to author.

## Next

Run the integration gate — the full suite under `pytest -n auto` with raw
output — and build the closure package, then close F257 through
`docs/roadmap/STATUS_closure_protocol.md`, whose new precondition 6 this feature
must itself satisfy.
