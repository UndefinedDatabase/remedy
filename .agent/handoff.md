# Handoff — F112 Prompt budget per task class, round 25 (fix R-0791 + rebuild evidence/zip)

## Session

Session continuing F112 (same numbering as round 24's handoff used) ·
round 25 · rounds so far 25.

This round booked round 24's PASS verdict (RECORD24 — R-0790's fix
independently re-verified, one owed finding R-0791) into
`.agent/live_review.md` (C1), registering `R-0791` in the same append;
applied PLAN25 to `.agent/plan.md` (C2); FIXED `R-0791` — a
whitespace-only defect (double blank line at an append seam, missing
trailing newline) — in `tests/orchestration/test_failure_postmortem.py`
(C3); then, as an EXTERNAL ACTION (no commit of its own), re-ran the
evidence job and the mandatory review zip against the new head.

**THE ZIP DID NOT FULLY SUCCEED.** It built (exit 0, a real 22MB archive
at a real path with a verified SHA-256), so R-0790's fix IS confirmed
sufficient for the specific defect it targeted (the commit-subject
`ReviewSubjectError` crash that blocked round 23 is gone). But the
package is `PACKAGE_STATUS=BLOCKED_EVIDENCE` / `EVIDENCE_AUTHORITATIVE=false`
— a NEW, DIFFERENT blocker, unrelated to R-0790/R-0791, in the
verification-run recording shape that `job_evidence._run_verifications`
itself produces. Full detail in "The new blocker" below. Per constraint
6e this is declared, not papered over; no fix was attempted (it would
require touching `packages/orchestration/job_evidence.py` and/or
`scripts/build_review_manifest.py`, both outside this round's locked
change set).

## Range

`6dfdff5d..a06e8430` (base is F112 R24's handback commit; this handoff
itself lands as commit C4 on top of `a06e8430`).

## Commits

### 43f84b79 F112 R25 C0a: save round 25 step block verbatim to .agent/authored/f112-r25.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f112-r25.md` | 324/0 | Transport-proof source of truth for this round's block, saved verbatim (new file). |

### bad3101f F112 R25 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 324/288 | Byte-identical mirror of the authored file (whole-file overwrite; diff algorithm reports 324/288 due to partial line overlap with the prior round's block, not a size mismatch). Confirmed with `git rev-parse HEAD:.agent/authored/f112-r25.md` and `git rev-parse HEAD:.agent/last_block.md` printing the SAME blob id, `5b252687735a527c01a73367b1462450e4d5e3f0`. |

### 0972376d F112 R25 C1: append RECORD24 to live_review.md (books R24 PASS, registers R-0791)
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 4/1 | Appended RECORD24 via `content_bytes + b"\n" + RECORD24_bytes` (one-newline formula), extracted programmatically from the committed authored file. RECORD24 itself carries one internal `\n\n` (Gate paragraph / finding paragraph), preserved exactly. |

### ad3e4207 F112 R25 C2: apply PLAN25 to plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 14/18 | Whole-file replacement with PLAN25, extracted programmatically from the committed authored file, not retyped. No trailing newline. |

### a06e8430 F112 R25 C3: fix R-0791 - collapse double blank line and add trailing newline
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_failure_postmortem.py` | 1/2 | Single literal-string replacement (PAIR25_FROM → PAIR25_TO), extracted programmatically from the committed authored file, verified to occur exactly once before applying. Net byte count unchanged (50148 both sides): removes one blank line (-1 byte), adds a trailing newline (+1 byte). |

5 commits, 668 insertions total across C0a-C3 (largest single commit
324, under the 500 cap; no oversize declaration needed). This handback
is commit C4 — its own diff is the `.agent/handoff.md` rewrite only,
exempt from the churn reading as a single-state-file save.

## Verification

**G1 TRANSPORT** — sha256 of the committed `.agent/authored/f112-r25.md`:
`9dc6e3b9ba66fbe0d70713df6c1e3033f067349f060bcbb13bd98bfbe8606d4e`, length
**23028 bytes**. `git rev-parse HEAD:.agent/authored/f112-r25.md` and
`git rev-parse HEAD:.agent/last_block.md` BOTH print
`5b252687735a527c01a73367b1462450e4d5e3f0` — ONE blob id. PASS.

**G2 THE PLAN** — PLAN25 extracted by delimiter from the committed
authored file (1794 bytes) compared byte-for-byte against the written
`.agent/plan.md` at C2: **equal, 1794 bytes**. `wc -l .agent/plan.md` =
**40** (under 50). File ends WITHOUT a trailing newline. `## Goal`
count = **1**. `## Next Steps` count = **1**. PASS.

**G3 THE RECORD APPEND** — RECORD24 extracted from the committed
authored file measured **5824 bytes**, matching the block's own pinned
figure exactly (Gate paragraph 3816 bytes + `\n\n` separator 2 bytes +
finding paragraph 2006 bytes = 5824, confirmed by splitting on the first
`\n\n`). `.agent/live_review.md` measured **2310824 bytes** immediately
before the append (matches the block's pinned pre-C1 figure exactly).
Arithmetic: `2310824 + 1 + 5824 = 2316649` — matches the real
post-append size exactly, confirmed directly, and matches the block's
own predicted total exactly. Old-file-is-prefix check: **True**.
Post-append file still ends WITHOUT a trailing newline: **True**. The
seam itself reads `...it.\nGate: F112 R24...` — exactly one newline
between the old tail and the new record, no extra blank line. HEADER
SHAPE: lines matching `^Gate: F\d+ R\d+ — ` — before C1 **271**, after
**272**. Lines matching `^Gate: F112 R24 — ` — before **0**, after
**1**. Lines matching `^- R-0791 — ` — before **0**, after **1**. OPEN
SET recomputed mechanically directly against `.agent/live_review.md`:
registered (unique `^- R-\d{4} — ` ids) — before **351**, after
**352**. `Done:` (unique `^Done: R-\d{4}` ids) — before **72**, after
**72**. Open total (registered minus done) — before **279**, after
**280**. MOVED exactly as the block predicted. PASS, no deviation.

**G4 PAIR25** — `.count()` of PAIR25_FROM's exact bytes (911 bytes) in
`tests/orchestration/test_failure_postmortem.py` before C3: **1**. File
byte size: **50148** before AND after C3 (unchanged, as predicted).
`wc -l`: **1098** before AND after C3 (unchanged). File now ends WITH a
trailing newline (confirmed `True`, was `False` before). Exactly ONE
blank line now separates `is True` from `@pytest.mark.parametrize`
(confirmed by regex: one match of `is True\n\n    @pytest.mark.parametrize`,
zero matches of the old double-blank pattern). `python3 -m ruff check
tests/orchestration/test_failure_postmortem.py` → **`All checks
passed!`**, exit 0 — the one `W292` finding present before C3 is gone.
PASS.

**G5 THE EVIDENCE + ZIP REBUILD** — see "The new blocker" section below
for full detail; summary line: merge-base reconfirmed unchanged
(`5c28c6741db2d9073fc75cd159d91037e0757fb0`); all three scoped
verification commands exit 0 (24, 2, 42 passed respectively, 68 total, 0
failed); `create_manual_completion_bundle` did NOT raise — it returned a
summary dict (`verdict: PASS_WITH_RISKS`, `authority_count: 21`,
`partition: T001/T002/T003 = 7/7/7`, `total_passed: 68`); the zip script
exited **0** and produced a real archive, but
`PACKAGE_STATUS=BLOCKED_EVIDENCE` / `EVIDENCE_AUTHORITATIVE=false`. **THE
ZIP DOES NOT NOW FULLY SUCCEED** — R-0790's own specific defect is
confirmed fixed (no more `ReviewSubjectError` crash on the commit
subject), but a second, different, previously-undiscovered defect in the
verification-run recording shape blocks the package from being
authoritative. Declared as a new blocker, not fixed (outside this
round's change set). PARTIAL — zip built, but not to a
commit-ready/authoritative state.

**G6 THE TREE AND THE COMMITS** — `git status --porcelain` and `git
status --porcelain --ignored=no` immediately before staging C4: **both
empty** (confirmed after the evidence/zip external action too — neither
the evidence directory nor the zip file is tracked or shown, both being
gitignored scratch). `git diff --stat 6dfdff5d..a06e8430 -- packages/
apps/ tests/ docs/`: **exactly one file**,
`tests/orchestration/test_failure_postmortem.py | 3 +-` — excluding that
file from consideration leaves an empty diff, exactly the declared
change set. PER-COMMIT INSERTIONS (the `+` column): C0a `43f84b79`
**324**, C0b `bad3101f` **324** (238 net-new content lines re-diffed
against the prior block; well under 500 regardless), C1 `0972376d` **4**,
C2 `ad3e4207` **14**, C3 `a06e8430` **1** — every one confirmed under
500; no oversize commit to declare. PASS.

## The new blocker (G5 detail — full text, not summarized)

After C3, the evidence + zip rebuild was run as an external action using
a driver script. **First attempt** placed the driver at the repo root
(`.remedy_r25_evidence_driver.py`, untracked) and hit
`ValueError: T001: safe-diff path set does not match the task
partition` inside `create_manual_completion_bundle` — root-caused by
direct inspection: `resolve_review_subject` merges the committed
base..head delta with the CURRENT WORKING TREE'S DIRTY STATE
(`_dirty_records`), so the untracked driver script itself was being
swept into the "attestable authority" file set, while `git diff
base..head` naturally had no history for an untracked file — a
self-inflicted mismatch, not a codebase defect. Fixed by relocating the
driver to the gitignored `.remedy-wt/` scratch location (per this
repo's own established convention for exactly this class of problem)
and re-running from a clean `git status --porcelain`; the second run's
authority count came out to 21 (7+7+7), matching the partition, and this
error did not recur.

**Second attempt** (from `.remedy-wt/r25_evidence_driver.py`, tree
clean) got past that point cleanly:

- `git merge-base main HEAD` → `5c28c6741db2d9073fc75cd159d91037e0757fb0` — UNCHANGED, matches the pinned base.
- Stale `remedy-job-evidence-f112-closure/` from round 23 confirmed gitignored via `git check-ignore -v` (`.gitignore:226:remedy-job-evidence-*/`), then removed.
- All three scoped verification commands, exit 0 each:
  - `python3 -m pytest tests/orchestration/test_class_prompt_budget.py` → 24 passed, 0 failed.
  - `python3 -m pytest tests/orchestration/test_context_compiler.py -k "test_an_oversized_context_fits_under_its_class_cap_with_the_demotion_recorded or test_an_unfittable_context_reports_cannot_fit_with_the_tier1_arithmetic"` → 2 passed, 0 failed.
  - `python3 -m pytest tests/cli/test_golden_path.py` → 42 passed, 0 failed.
- `create_manual_completion_bundle(...)` did NOT raise. Returned summary:
  ```
  {
    "job_id": "cee206d7881e4699",
    "head_commit": "a06e8430a632e00d88224417208b86ea7e0b7c68",
    "authority_count": 21,
    "partition": {"T001": 7, "T002": 7, "T003": 7},
    "commit_count": 165,
    "verdict": "PASS_WITH_RISKS",
    "manual_completion": true,
    "operator_attested_tasks": ["T001", "T002", "T003"],
    "total_passed": 68
  }
  ```
- `bash scripts/make_review_zip.sh --evidence-dir remedy-job-evidence-f112-closure` exited **0** and printed:
  ```
  UNCHANGED: runtime_integration_gate.json — rebuilt from source; identical to existing
  Evidence refresh completed for staged copy.
  Observability index generated from staged bytes: evidence/current/self_run_observability_index.json
  WARNING: Evidence validation failed (is_valid_current_run=false).
  Zip will be built anyway — reviewer will see validation status in manifest.
  {"member_count": 3862, "authoritative_count": 21, "symlink_count": 0, "tombstone_count": 0, "final_path": "/home/decodeux/Repos/remedy-history/zips/remedy-review-20260904-034254-BLOCKED_EVIDENCE.zip", "final_sha256": "bb52ab1106a77d706fa3e1a25e4bdc80510645194e9b303d46f3e6c03a59e96d", "publication_capability": "SUPPORTED", "package_status": "BLOCKED_EVIDENCE", "evidence_authoritative": false, "review_subject_alignment": "PASS", "manifest_sha256": "e08d5b466e8af7fc322dc0fa77d2ab8a928a6d73a16b3699a103726aac9d797e"}

  ============================================
  REVIEW_PACKAGE_CREATED=true
  PACKAGE_STATUS=BLOCKED_EVIDENCE
  PACKAGING_CWD=/home/decodeux/Repos/remedy
  EVIDENCE_DIR=remedy-job-evidence-f112-closure
  REVIEW_SUBJECT_ALIGNMENT=PASS
  EVIDENCE_AUTHORITATIVE=false
  REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
  ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260904-034254-BLOCKED_EVIDENCE.zip
  DO_NOT_COMMIT=true
  ============================================

  *** ZIP CREATED, BUT THIS PACKAGE IS NOT COMMIT-READY ***
  ```
- Independently confirmed the printed SHA-256 with a fresh, separate `hashlib.sha256` read of the produced file: `bb52ab1106a77d706fa3e1a25e4bdc80510645194e9b303d46f3e6c03a59e96d` — **MATCHES**. File size 22202607 bytes.
- Archiving: the zip script itself already writes directly to `/home/decodeux/Repos/remedy-history/zips/remedy-review-20260904-034254-BLOCKED_EVIDENCE.zip` (its `REVIEW_PACKAGE_DIR`); no separate copy step was needed or performed. Archived path: `/home/decodeux/Repos/remedy-history/zips/remedy-review-20260904-034254-BLOCKED_EVIDENCE.zip`.

**Root cause of `is_valid_current_run=false`**, found by calling
`scripts/build_review_manifest.validate_evidence_candidate('remedy-job-evidence-f112-closure')`
directly (read-only diagnostic, no file written):

```
{
  "is_valid_current_run": false,
  "validation_errors": [
    "verification_tests.json field verification_tests.runs[1].stdout_summary carries a local absolute path",
    "verification_tests.json runs[0] output_hash does not match sha256(stdout_summary)",
    "verification_tests.json runs[1] output_hash does not match sha256(stdout_summary)",
    "verification_tests.json runs[2] output_hash does not match sha256(stdout_summary)"
  ]
}
```

Two distinct, independently-confirmed sub-causes, BOTH inside
`packages/orchestration/job_evidence.py`'s `_run_verifications` /
`_default_verification_runner` machinery — NEITHER touched by this
round's commits (which are whitespace-in-a-test-file and `.agent/`
bookkeeping only):

1. **`output_hash` vs `stdout_summary` mismatch, all three runs.**
   `_run_verifications` stores `stdout_summary` truncated to its last
   2000 characters, but `output_hash` (when the runner supplies its own,
   as `_default_verification_runner` does) is computed over the FULL,
   untruncated output. Confirmed directly: `hashlib.sha256(stdout_summary
   .encode())` != the recorded `output_hash` for all three runs (any
   output over 2000 chars reproduces this). This is a structural property
   of the verification-recording code, not something this round's
   pytest commands did unusually.
2. **A local absolute path in run[1]'s `stdout_summary`.** The offending
   line, found by scanning `stdout_summary` line-by-line with
   `packages.orchestration.run_manifest._contains_local_path`:
   `'platform linux -- Python 3.10.12, pytest-9.0.3, pluggy-1.6.0 -- /usr/bin/python3'`
   — pytest's own standard verbose header line, which names the
   interpreter binary path. `_contains_local_path` flags `/usr/bin/python3`
   as an unsafe local path even though it is a stock system binary path
   that reveals nothing about this machine or this repo — the same
   defect FAMILY as R-0206/R-0790 (over-eager local-path detection
   producing false positives on ordinary, harmless text), but a
   DIFFERENT call site (`run_manifest._contains_local_path` scanning
   captured verification stdout, not `path_redaction.ABS_PATH_RE`
   scanning a commit subject) and a different triggering string. Only
   run[1] shows it in this bundle because its output is short enough
   that the header line survives the last-2000-char truncation window;
   run[0] and run[2] likely carry the same header line but it falls
   outside their truncated windows.

Neither sub-cause is fixable within this round's locked change set
(`.agent/authored/f112-r25.md`, `.agent/last_block.md`,
`.agent/live_review.md`, `.agent/plan.md`,
`tests/orchestration/test_failure_postmortem.py`, `.agent/handoff.md`)
— both live in `packages/orchestration/job_evidence.py` and/or
`packages/orchestration/run_manifest.py` / `scripts/build_review_manifest.py`,
none of which this round is authorized to touch. Per constraint 6e, this
is declared as the round's central, load-bearing result rather than
patched over: **the zip built (exit 0, real file, verified hash), but is
NOT commit-ready** — `PACKAGE_STATUS=BLOCKED_EVIDENCE`,
`EVIDENCE_AUTHORITATIVE=false`.

## Deviations & assumptions

1. **The driver script's first placement (repo root, untracked) caused a
   self-inflicted `ValueError` inside `create_manual_completion_bundle`**,
   traced to `resolve_review_subject` including dirty/untracked
   working-tree files in its authority scan. No production code was
   touched to work around this — the fix was purely procedural
   (relocate the driver into the gitignored `.remedy-wt/` scratch
   location and re-run from a clean tree), matching this repo's own
   established convention for exactly this class of problem. Not a
   registered finding (nothing on disk was ever wrong; the mistake was
   this round's own transient scratch-file placement, corrected before
   any commit).
2. **The zip's `BLOCKED_EVIDENCE` status is a NEW blocker, not a
   continuation of R-0790 or R-0791.** Both of this round's own fixes
   (booking RECORD24/registering R-0791, then fixing R-0791) are
   confirmed correct and complete by G1-G4 above; the block's own
   prediction that "the zip should now succeed" is only PARTIALLY borne
   out — R-0790's specific crash is gone, but a second, previously
   undiscovered defect (detailed above) now blocks authoritativeness.
   This is exactly the scenario constraint 6e names as its own new
   finding rather than something to paper over — no id is minted here by
   the worker (that is the reviewer's call per the findings-ledger
   rules), but the full, unsummarized evidence is captured above for the
   reviewer to register and design a round around.
3. **`.remedy-wt/r25_evidence_driver.py`** (the corrected, working driver
   script) and **`remedy-job-evidence-f112-closure/`** (the rebuilt
   evidence directory, job_id `cee206d7881e4699`) are both left on disk,
   gitignored, untracked, uncommitted — confirmed by G6's clean `git
   status --porcelain` (both plain and `--ignored=no`). Left in place
   intentionally so the reviewer can inspect the full evidence bundle
   directly rather than only this handback's excerpts.
4. **`.agent/decisions.md`, `.agent/candidates.md`, `.agent/prose_slips.md`,
   `docs/roadmap/features/T3_F112.md` were NOT touched**, per constraint
   8. **`scripts/self_use_queue.json` was NOT touched**, per the
   change-set note.
5. **`packages/common/path_redaction.py` was NOT touched**, per
   constraint 5 — this round's only code-adjacent change is the
   whitespace normalization in the test file (C3).
6. **`git push` outcome is not recorded in this file** (write-once rule)
   — see the completion report for the real result.

## Item-Status Table

| Item | Status | Reason |
|---|---|---|
| C0a save block | done | |
| C0b mirror block | done | blob-id-identical to C0a |
| C1 append RECORD24 (books R24, registers R-0791) | done | byte length matched pinned figure exactly (5824); arithmetic, prefix, header/open-set counts all match pinned figures; open set correctly MOVED (279→280) |
| C2 apply PLAN25 | done | byte-equal, 40 lines (under 50), no trailing newline, headings present exactly once each |
| C3 fix R-0791 (PAIR25) | done | count 1 before, byte size unchanged (50148), line count unchanged (1098), file now ends with trailing newline, one blank line at seam, `ruff` clean |
| G1 transport | done | blob ids match, sha256 + length reported |
| G2 the plan | done | byte-equal, headings present exactly once each |
| G3 the record append | done | arithmetic matches; open set correctly MOVED |
| G4 PAIR25 | done | count, byte sizes, line counts, trailing newline, blank-line seam, ruff all exactly as expected |
| G5 evidence + zip rebuild | deviated | zip built (exit 0, verified hash, archived) but package is BLOCKED_EVIDENCE/not authoritative — a new, different, fully-diagnosed blocker unrelated to R-0790/R-0791, declared in full above |
| G6 the tree and the commits | done | no protected-path diff outside the declared file, all commits under 500 insertions, tree clean including ignored scan |
| RECORD24 booked | done | applied verbatim at C1 |
| R-0791 registered | done | applied verbatim at C1, as part of RECORD24's own text |
| R-0791 fixed | done | PAIR25 applied at C3, ruff-confirmed clean |
| PLAN25 applied | done | applied verbatim at C2 |

## Next

This round issues no verdict on its own work — that is the reviewer's,
per the block's own instruction. No `Done: R-0790` or `Done: R-0791`
line is written here; per the block's own Handback instruction, those
lines are authored by the reviewer next round, once the reviewer accepts
this round's own verdict.

**Next expected action: this is a BLOCKER, not a closure handoff.** The
zip is not commit-ready. The reviewer needs to design the next round
around the two sub-causes named above in "The new blocker" — most
likely a fix to `_run_verifications`'s `output_hash`/`stdout_summary`
pairing (compute the hash over the same truncated text it stores, or
store the full text) and a narrowing fix to
`run_manifest._contains_local_path` (or its allow-list) so a bare stock
interpreter path like `/usr/bin/python3` in captured tool output is not
treated the same as a real local filesystem path worth redacting —
mirroring the same lesson R-0790 already taught about `ABS_PATH_RE`,
now needed at a second call site. Both changes would be to files outside
this round's locked scope, so no fix was attempted here. Do NOT retry
the zip build again without a code change — the two sub-causes are
deterministic and will reproduce identically.

Open findings count: **280** (352 registered, 72 `Done:`) — MOVED from
279 by this round's C1 append (G3 above), because this round both books
RECORD24's PASS verdict and registers `R-0791` in the same commit. This
handback's own new blocker (the `output_hash`/`stdout_summary` mismatch
and the `/usr/bin/python3` false positive) is NOT YET a registered
`R-` id — that registration is the reviewer's call for the next round.

Before starting the next round: re-check `.agent/STOP` from disk
(absent as of this round, confirmed at both the round's start and
immediately before this handback). Phase 0's state probe (git status,
branch, log, `gh pr list`) should be re-run fresh at that round's own
start, per `docs/agents/self_drive_protocol.md` — not assumed carried
over from this handoff.
