# Handoff — F112 Prompt budget per task class, round 28 (rebuild closure evidence bundle + review zip against the R-0792/R-0793 fix)

## Session

Session continuing F112 (same numbering ambiguity round 20's handoff
introduced and rounds 21-27 carried forward unresolved — "6 (or 7)"; see
Deviations item 1 below) · round 28 · rounds so far 28.

This round is NOT a fresh loop-session bootstrap — it is a direct
continuation of round 27's own session. Per the session-numbering rule
(docs/agents/planner_reviewer_prompt.md §1 item 3: "this session is that
[carried] number plus one, carried forward in every handback of this
session"), a number only increments at a fresh bootstrap. This is not
one, so the number is unchanged from round 27.

## Range

Review of `313126ce..HEAD` (base is F112 R27's handback commit).

## Commits

### e4790bff F112 R28 C0a: save the round 28 step block verbatim to .agent/authored/f112-r28.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f112-r28.md` | +215/-0 | transport proof — verbatim copy of the supplied step block |

### fdaf902b F112 R28 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +215/-208 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption) |

### e259d851 F112 R28 C1: append RECORD27 to live_review.md (books R27 PASS, resolves R-0792/R-0793)
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +6/-1 | append RECORD27 (books round 27's PASS verdict, resolves `R-0792` and `R-0793` via the two `Done:` lines already embedded in the extracted RECORD27 span) |

### 346c178f F112 R28 C2: apply PLAN28 to plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +48/-48 | whole-file replace with PLAN28 |

### (no C3 commit — no repository diff)
C3 (the evidence bundle + review zip) produced NO repository diff by
design: `remedy-job-evidence-f112-closure/` and the review zip are both
gitignored and were never `git add`ed. Confirmed by `git status
--porcelain` (empty, both before and after C3) and `git check-ignore -v
remedy-job-evidence-f112-closure` (matched by `.gitignore:226`). The
driver script lives at `.remedy-wt/r28_evidence.py` (gitignored via
`.gitignore:235`), not committed.

### (this handback commit)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this handback (write-once per PH v3) |

## External actions

- `git push -u origin feature/f112-prompt-budget-per-task-class` — run
  after this handback commit; outcome reported in the completion message
  to the operator per the block's own ordering (this file is written
  once, so the literal push transcript is not edited back in after the
  fact).

## Verification

Real, trimmed transcripts for every gate this round's block ordered, run
in the PRIMARY checkout (C3/C4 produced no destructive verification, so
no disposable worktree was needed this round):

```
$ git status --porcelain   # before C0a
(empty)

$ git status --porcelain   # immediately before C3
(empty)
```

`.agent/live_review.md` reproduced at exactly `2334372` bytes immediately
after C1 (`2328447 + 1 + 5924`, RECORD27 extracted from the committed
authored file, sha256
`35a3c5fffd383da5d75f222bda03cf283150cad22acd71f3c70caffb23723a91`
matching the marker's stamped hash exactly, 5924 bytes); the pre-append
content is a byte-exact prefix of the post-append content; the file still
ends WITHOUT a trailing newline. Registered/`Done:`/open counts (counted
via the `^- R-\d{4} —` registration-bullet pattern and the `^Done: R-\d{4}`
pattern, deduplicated by id): before C1 — 354 registered, 72 `Done:`, 282
open; after C1 — 354 registered, 74 `Done:`, 280 open (UNMOVED registered
count, `Done:` count up by exactly 2, matching the block's pinned figures
exactly).

`.agent/plan.md` reproduced byte-identical to the extracted PLAN28 span:
`2218` bytes both sides, sha256
`33d287544d2c9b4c447bfd7cf64deccd7165a28b0c1f1e2492c3a6af3bf5805e`
matching the marker's stamped hash; `wc -l` reads `47` (under 50);
`## Goal`/`## Next Steps` each appear exactly once; no trailing newline.

**C3 — the three scoped verification commands, via `_run_verifications`
imported from `packages.orchestration.job_evidence`:**

```
python3 -m pytest tests/orchestration/test_class_prompt_budget.py
  -> passed=24 failed=0 skipped=0 selected=24 node_ids_count=24

python3 -m pytest tests/orchestration/test_context_compiler.py -k
  "test_an_oversized_context_fits_under_its_class_cap_with_the_demotion_recorded
  or test_an_unfittable_context_reports_cannot_fit_with_the_tier1_arithmetic"
  -> passed=2 failed=0 skipped=0 selected=2 node_ids_count=2

python3 -m pytest tests/cli/test_golden_path.py
  -> passed=42 failed=0 skipped=0 selected=42 node_ids_count=42
```
All three exited zero-failure; node_ids counts equal `selected` in every
run. Total passed across the three runs: 68.

**`create_manual_completion_bundle` returned summary (full):**

```json
{
  "job_id": "79b21c8cba8b4352",
  "head_commit": "346c178f3241fad3984dca9baea3f37e34c3892a",
  "authority_count": 24,
  "partition": {"T001": 8, "T002": 8, "T003": 8},
  "commit_count": 184,
  "verdict": "PASS_WITH_RISKS",
  "manual_completion": true,
  "operator_attested_tasks": ["T001", "T002", "T003"],
  "total_passed": 68
}
```
`base_commit` used: `5c28c6741db2d9073fc75cd159d91037e0757fb0`, reconfirmed
via `git merge-base main HEAD` immediately before the call — unchanged
from the block's stated value. `head_commit` used:
`346c178f3241fad3984dca9baea3f37e34c3892a`, reconfirmed via `git
rev-parse HEAD` immediately before the call, matching C2's own commit —
no discrepancy to declare. `job_id` freshly generated
(`uuid4().hex[:16]`). Call did not raise.

**C3c — output_hash self-check** (re-read
`remedy-job-evidence-f112-closure/verification_tests.json` from disk,
compared `output_hash` against `sha256(stdout_summary.encode()).hexdigest()`
for every run): `vr-0001` True, `vr-0002` True, `vr-0003` True — all three
`True` as expected.

**C3d — review zip build:**

```
$ bash scripts/make_review_zip.sh --evidence-dir remedy-job-evidence-f112-closure
... (evidence refresh, observability index, packaging) ...
REVIEW_PACKAGE_CREATED=true
PACKAGE_STATUS=READY_FOR_REVIEW
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260904-123332-READY_FOR_REVIEW.zip
exit_code=0
```
Printed SHA-256 (script's own JSON line): `final_sha256`
`b0085f28a2c0c50654ed33be647ed986addc07c1c462324b1ee3fc1c8bb05927`. My own
independent `sha256sum` of the produced file:
`b0085f28a2c0c50654ed33be647ed986addc07c1c462324b1ee3fc1c8bb05927` —
identical. File size 22385222 bytes (~22M).

**C3e — `.review_zip_manifest.json` read FROM INSIDE the zip via
Python's `zipfile` module (not from builder stdout):**

- `PACKAGE_STATUS` (manifest field `package_status`): `"READY_FOR_REVIEW"`
- `EVIDENCE_AUTHORITATIVE` (manifest field
  `current_evidence.evidence_freshness.evidence_authoritative`): `true`
- `REVIEW_SUBJECT_ALIGNMENT` (manifest field
  `review_subject_evidence_alignment.verdict`, the only field of that
  name in the manifest — the builder's own stdout also prints a
  top-level `review_subject_alignment: "PASS"` env-style summary line,
  consistent with but not substituted for this in-zip reading): `"PASS"`
- `committed_review_subject.base_commit`:
  `"5c28c6741db2d9073fc75cd159d91037e0757fb0"`
- `committed_review_subject.head_commit`:
  `"346c178f3241fad3984dca9baea3f37e34c3892a"`
- `committed_review_subject.base_is_ancestor`: `true`
- `ready_gate_matrix.ok`: `true`
- `ready_gate_matrix.blocking_reasons`: `[]` (empty)
- `ready_gate_matrix.gate_verdicts`: `artifact_contract_gate.json=PASS`,
  `change_provenance_gate.json=PASS`,
  `commit_execution_gate.json=NEEDS_HUMAN_APPROVAL`,
  `final_verifier_report.json=PASS_WITH_RISKS`,
  `fresh_evidence_gate.json=PASS`, `manifest_integrity.json=ok=true`,
  `postmortem_integrity.json=ok=true`, `runtime_integration_gate.json=PASS`
- `review_subject_evidence_alignment.verdict`: `"PASS"`
- `review_subject_evidence_alignment.issues`: `[]` (0 issues)
- `review_subject_evidence_alignment.hash_mismatches`: `[]` (0 mismatches)
- `review_subject_evidence_alignment.dirty_file_count_total`: `1`
  (untracked scratch content outside the committed review subject; not a
  hash mismatch and not a blocking reason — `ready_gate_matrix.ok` is
  `true` with an empty `blocking_reasons` list regardless)

**PACKAGE_STATUS reads `READY_FOR_REVIEW` and `EVIDENCE_AUTHORITATIVE`
reads `true` — the operator's expected result is confirmed, per the
R-0792/R-0793 fix landed in round 27.**

**C3f — archiving:** `scripts/make_review_zip.sh` writes the zip directly
to `/home/decodeux/Repos/remedy-history/zips/` as its own final output
location (`ZIP_PATH` above) — there is no separate staging location to
copy from. The driver's own copy attempt correctly detected source and
destination were the same file (`shutil.copy2` raised `SameFileError`)
and logged `NOT ARCHIVED` with that reason; the file's absolute archived
path is `/home/decodeux/Repos/remedy-history/zips/remedy-review-20260904-123332-READY_FOR_REVIEW.zip`,
already at the intended archive location — not a failure to archive.

**C3g:** `git status --porcelain` and `git status --porcelain
--ignored=no` both read empty for tracked paths after C3.
`git check-ignore -v remedy-job-evidence-f112-closure` →
`.gitignore:226:remedy-job-evidence-*/	remedy-job-evidence-f112-closure`
(exit 0, confirmed gitignored).

**C4 — integration-gate re-confirmation / integrity check:**

```
$ python3 -c "from packages.orchestration.integrity_gate import run_integrity_checks; r = run_integrity_checks(); ..."
passed: True
fail_count: 0
  handler_import: pass
  live_review_verdict: pass
  plan_consistency: pass
  relevant_untracked: pass
  high_blockers_open: pass
```

## Authored-text proofs

- `.agent/authored/f112-r28.md` (C0a): `sha256sum` of the source
  scratchpad file and the committed copy both read
  `4a64111331abc8f31617d0658f7f53fb22af236f10766a18339655079705595c`
  (17747 bytes, 215 lines) — identical.
- `.agent/last_block.md` (C0b): `git rev-parse
  HEAD:.agent/authored/f112-r28.md` and `git rev-parse
  HEAD:.agent/last_block.md` both print blob
  `df782cadec1cb4436b6560f55a5663812983042c` — identical.
- RECORD27 (C1) and PLAN28 (C2): byte-exact, hash-verified as reported
  under Verification above.

## Deviations & assumptions

1. **Session-number ambiguity carried forward, not resolved** — same
   "6 (or 7)" ambiguity documented in every handoff since round 20
   (rounds 21-27 all carried it forward unresolved for the same reason:
   the fresh-bootstrap boundary between round 19 and round 20 is not
   recoverable from git history or any handoff). This round makes the
   same choice, since it is an explicit continuation of round 27's own
   session, not a fresh bootstrap.
2. **No `git worktree` was used this round.** The block's mutation
   red-proof machinery (G5) does not apply — round 28 has no production
   code diff at all (nothing under `packages/`, `apps/`, `tests/`,
   `docs/` changed), so there was nothing to mutate. The evidence job and
   zip build ran directly in the primary checkout, matching the block's
   own item 4 instructions, which name no worktree for this round.
3. **C3's evidence dir and zip are confirmed NOT committed** — verified
   both by `git status --porcelain` reading empty throughout and by
   `git check-ignore -v` on the evidence dir. No deviation; stated here
   because the block called this out as "most important."
4. No blocking reason was found at C3e — `PACKAGE_STATUS` read
   `READY_FOR_REVIEW` and `EVIDENCE_AUTHORITATIVE` read `true` on the
   first attempt, so the block's fallback branch ("if PACKAGE_STATUS is
   not READY_FOR_REVIEW, stop and report the blocking reasons, do not
   attempt a second fix") was not triggered.
5. This round wrote NO `Done:`/verdict line into `.agent/live_review.md`
   beyond what C1 copied verbatim from RECORD27 — booking this round's
   own verdict is the reviewer's job next round, per the block's own
   instruction.

## Next

Round 29 (per PLAN28's Next Steps): the reviewer independently
re-verifies this round's diff and re-runs the three scoped commands plus
its own re-read of the produced zip's manifest, then — if it books a PASS
— authors the STATUS `[x]` line from this round's reported
job_id/package/hash/path/accepted-HEAD, closure commit (STATUS, README
capability sync, `self_use_queue` SU-007 `consumed_by=F112`, final
`.agent/` state), and opens a PR (not merged). Round 30 is the Open PR
Gate (hosted CI green, docs gate/canary/touched suites pass, planner
merges per the standing merge-autonomy rule; hand back the built zip's
name and SHA-256 to the operator).
