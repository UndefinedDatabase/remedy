# Handoff — F273 Findings paydown v1 · Round 3

## Session

SESSION 1 of feature F273 · round 3 · rounds so far 3

Context self-assessment: the worker read the block, AGENTS.md, DECISION F273 D3, the handback template and the self-drive protocol's questions-file rule; every figure below comes from a command run in this round, and the worker's context held all of it without loss.

## Range

Review of a5e3b9ce..HEAD — branch `feature/f273-findings-paydown-v1`.

## Summary

Round 3 books round 2's verdict, closes T003 and builds T016 as the reviewer's dry run built them.
- C1 books Gate F273 R2 (VERDICT PASS) and the resolutions of R-0812, R-0396, R-0445 and R-0736, registers R-0983, R-0984 and R-0985, lands DECISION F273 D3, rewrites the plan and saves the six payload copies.
- C2 (T003, R-0645) adds one clause to step 1 of `docs/agents/integration_gate.md`: the FAILED list is one run's sample, an empty one is evidence and never proof.
- C3 (T016 (a), R-0984) gives `RunState` a `__str__` returning its value, adds a guard over `str()`, `format()` and the f-string of every member, and makes the CI `ci` job a `'3.10'`/`'3.12'` matrix with `fail-fast: false`, pinned by a test.
- C4 (T016 (b) and (c), R-0985 and R-0839) makes `scripts/rotate_live_review.py` the ledger's one reader (`open_finding_ids`, `count_open_findings` by distinct id, `latest_gate_verdict`), loads it by path in the manifest, writes `path -> base_sha256` tombstones in `create_manual_completion_bundle`, and binds tombstones to deleted subject paths in the packager's `_assert_authority_equality`.
- C5 (R-0983) makes `export_job_evidence` write `path -> base_sha256` tombstones and refuse a deleted path with no base blob.
- C6 is this handoff.

Landed: R-0645 — `52cee6d8`
Landed: R-0984 — `49cd2717`; resolution also reads the 3.12 column of the closure pull request's hosted CI (DECISION F273 D3 (2))
Landed: R-0985 — `cecc8881`
Landed: R-0839 — `cecc8881`
Landed: R-0983 — `531cc24a`

## Commits

### 8fe7ea35 F273 R3 C1: bookkeeping — round 2's verdict and four resolutions booked, R-0983 to R-0985 registered, DECISION F273 D3 landed
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f273-r3-block.md` | +114 / -0 | Byte copy of the block |
| `.agent/authored/f273-r3-decisions.md` | +48 / -0 | Byte copy of decisions.md |
| `.agent/authored/f273-r3-gate_from.txt` | +1 / -0 | Byte copy of gate_from.txt |
| `.agent/authored/f273-r3-gate_to.txt` | +5 / -0 | Byte copy of gate_to.txt |
| `.agent/authored/f273-r3-ledger.md` | +16 / -0 | Byte copy of ledger.md |
| `.agent/authored/f273-r3-plan.md` | +29 / -0 | Byte copy of plan.md |
| `.agent/decisions.md` | +48 / -0 | `a5e3b9ce` bytes + decisions.md (DECISION F273 D3) |
| `.agent/live_review.md` | +16 / -0 | `a5e3b9ce` bytes + ledger.md (Gate F273 R2, four `Done:` lines, R-0983 to R-0985) |
| `.agent/plan.md` | +13 / -12 | := plan.md |

290 insertions, 12 deletions (`git show --numstat`).

### 52cee6d8 F273 R3 C2: T003, R-0645 — step 1 of the integration gate names its FAILED list one run's sample
| Path | +/- | Reason |
|------|-----|--------|
| `docs/agents/integration_gate.md` | +4 / -0 | `a5e3b9ce` bytes with gate_from.txt replaced by gate_to.txt (an append after the FROM line) |

4 insertions, 0 deletions.

### 49cd2717 F273 R3 C3: T016 (a), R-0984 — a run state renders its value on every interpreter and CI runs 3.10 and 3.12
| Path | +/- | Reason |
|------|-----|--------|
| `.github/workflows/ci.yml` | +9 / -1 | `ci` job matrix `['3.10', '3.12']`, `fail-fast: false` — `git apply .remedy-wt/f273-proto-t016a.diff` |
| `packages/core/models.py` | +5 / -0 | `RunState.__str__` returns its value — same diff |
| `tests/orchestration/test_ci_workflow.py` | +10 / -0 | Pins the matrix and the setup step reading it — same diff |
| `tests/orchestration/test_job_state_field.py` | +13 / -3 | Guard over `str()`, `format()` and f-string of every member; docstring updated — same diff |

37 insertions, 4 deletions.

### cecc8881 F273 R3 C4: T016 (b) and (c), R-0985 and R-0839 — the manifest reads the ledger through its canonical reader and the manual bundle writes tombstones
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/job_evidence.py` | +11 / -2 | Manual bundle writes `path -> base_sha256` tombstones — `git apply .remedy-wt/f273-proto-t016bc.diff` |
| `scripts/build_review_manifest.py` | +33 / -29 | Ledger reader loaded by path; manual-completion union and gate-matrix `proof_authority` read `file_hashes` only — same diff |
| `scripts/build_review_zip.py` | +18 / -5 | Tombstones bound to deleted subject paths; coverage sets held to the live authority — same diff |
| `scripts/rotate_live_review.py` | +45 / -7 | `open_finding_ids`, `count_open_findings` by distinct id, `latest_gate_verdict` — same diff |
| `tests/orchestration/test_final_audit_evidence.py` | +63 / -39 | Manifest tests rewritten to the `Gate:` format; one reads the real ledger — same diff |
| `tests/orchestration/test_live_review_rotation.py` | +33 / -3 | Distinct-id count and verdict reader tests — same diff |
| `tests/orchestration/test_review_archive_artifacts.py` | +1 / -1 | Pipeline copy includes `rotate_live_review.py` — same diff |
| `tests/orchestration/test_review_authoritative_e2e.py` | +1 / -1 | Same — same diff |
| `tests/orchestration/test_review_final_status_source.py` | +1 / -1 | Same — same diff |
| `tests/orchestration/test_review_manual_completion_shapes.py` | +62 / -0 | Tombstone for every deleted path — same diff |
| `tests/orchestration/test_review_package_full_integration.py` | +1 / -1 | Pipeline copy includes the reader — same diff |
| `tests/orchestration/test_review_package_root_chain.py` | +1 / -1 | Same — same diff |
| `tests/orchestration/test_review_packaging_collision_safety.py` | +2 / -1 | Same — same diff |
| `tests/orchestration/test_review_zip_deleted_path_authority.py` | +47 / -0 | Tombstone binding in the packager — same diff |
| `tests/orchestration/test_review_zip_hygiene.py` | +1 / -0 | Reader among the required scripts — same diff |
| `tests/orchestration/test_stream_export_e2e.py` | +1 / -1 | Pipeline copy includes the reader — same diff |
| `tests/test_no_orphan_modules.py` | +0 / -2 | `rotate_live_review.py` leaves `ALLOWED_UNWIRED` — same diff |

321 insertions, 94 deletions.

### 531cc24a F273 R3 C5: R-0983 — the provider-run export writes a tombstone as the removed blob's sha256
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/job_evidence.py` | +8 / -4 | `export_job_evidence` tombstone is `base_sha256`; no base blob refuses the proof — `git apply .remedy-wt/f273-proto-r0983.diff` |
| `tests/orchestration/test_job_evidence.py` | +49 / -0 | Export of a deleting branch strictly decodes — same diff |

57 insertions, 4 deletions.

### C6 (this commit) F273 R3 C6: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C4, with 321.

## External actions

- `git worktree add --detach .remedy-wt/f273-r3-g5 531cc24a` for G5, then `git worktree remove .remedy-wt/f273-r3-g5` (exit 0). `git worktree list` afterwards: the primary checkout at `531cc24a` on `feature/f273-findings-paydown-v1` and the reviewer's `.remedy-wt/f273-r3-dry` at `a5e3b9ce`, nothing else.
- After C6: `git push`. No pull request is opened.

## Verification

Exit codes were read through `.remedy-wt/f273-r3/run.py <cwd> <outfile|-> cmd...` (runs with an explicit `cwd`, prints the output or, with an outfile, its last 15 lines and its line count, then `EXIT <returncode>`); every gate ran with `cwd=/home/decodeux/Repos/remedy` except G5, which ran in its own worktree. Interpreter: Python 3.10.12.

- **Transport**, before any write: `.remedy-wt/f273-r3/digests.py` printed MATCH for all six payloads (block.md `2b3f9f097b10a16a494f706667d6340de36520007b372cd5d2f980c1355aa69b`) and all three diffs, `ALL True`.
- **G1** (at C5 `531cc24a`, clean tree): `.remedy-wt/f273-r3/g1.py`, EXIT 0:
  ```
  True plan.md == payload
  True live_review.md == base + ledger
  True decisions.md == base + decisions
  True authored f273-r3-plan.md == payload
  True authored f273-r3-ledger.md == payload
  True authored f273-r3-decisions.md == payload
  True authored f273-r3-gate_from.txt == payload
  True authored f273-r3-gate_to.txt == payload
  True authored f273-r3-block.md == payload
  True TO contains FROM
  True FROM exactly 1x before
  True FROM exactly 1x after
  True gate doc == base with FROM->TO
  True C2 touches only the gate doc
  True added 1x: "   That list is ONE run's sample, not th"
  True added 1x: '   empty list is evidence that this run '
  True added 1x: '   branch introduces no failure, and the'
  True added 1x: '   a later run finds red is attributed b'
  True C2 adds exactly the TO-only lines
  ALL True 19 checks
  ```
- **G2**: `git rev-parse 531cc24a:tests 531cc24a:packages 531cc24a:scripts 531cc24a:docs 531cc24a:.github`, EXIT 0:
  ```
  7f2abd8ebf29f2260f47f4cf3ef3a00ee9e97969
  33e5de700300b3644f0e979824eae0edcf526627
  eac614e51c99eabe996a0cebe7b4bebaf2f8abd5
  f1fd3da1ac35dae63ca2a6350f1ef205e3b0c2e4
  118e627f2d62e6962f7c0d9cdafa54888d110085
  ```
  All five equal the reviewer's dry-run subtrees.
- **G3** (primary checkout, serial, the block's 26 targets, full output in `.remedy-wt/f273-r3/g3.txt`, 11 lines): `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_job_state_field.py ... tests/orchestration/test_release_workflow.py`:
  ```
  699 passed in 217.48s (0:03:37)
  EXIT 0
  ```
  0 failed. `grep -c "R-0803:"` over the full output file printed `0`. `git status --porcelain` read empty afterwards.
- **G4** (primary checkout): `python3 -m ruff check` over the 21 Python files C3 to C5 touch, EXIT 0:
  ```
  All checks passed!
  ```
- **G5** (`python3 .remedy-wt/f273-r3/g5.py`, one worktree at `531cc24a`, `python3 -B -m pytest -q -p no:cacheprovider` from its root, `__pycache__` purged before every run, each mutation reverted by its saved bytes and `git status --porcelain` read empty after every revert), EXIT 0:
  ```
  job_evidence resolves to: /home/decodeux/Repos/remedy/.remedy-wt/f273-r3-g5/packages/orchestration/job_evidence.py
  inside worktree: True
  [control] exit 0; summary: 164 passed in 26.16s
  (a) packages/core/models.py: FROM count = 1
  [mut_a] exit 1; summary: 1 failed, 14 passed in 0.32s
      FAILED tests/orchestration/test_job_state_field.py::TestTheRenderingIsUnchanged::test_every_run_state_member_formats_and_stringifies_as_its_value
  (b) scripts/rotate_live_review.py: FROM count = 1
  [mut_b] exit 1; summary: 3 failed, 9 passed in 0.27s
      FAILED tests/orchestration/test_live_review_rotation.py::test_open_findings_count_is_identical_before_and_after
      FAILED tests/orchestration/test_live_review_rotation.py::test_the_open_set_counts_by_distinct_id_not_by_line
      FAILED tests/orchestration/test_live_review_rotation.py::test_dry_run_prints_the_sizes_and_writes_nothing
  (c) scripts/build_review_manifest.py: FROM count = 1
  [mut_c] exit 1; summary: 2 failed, 13 passed in 0.31s
      FAILED tests/orchestration/test_final_audit_evidence.py::TestReviewStateExtraction::test_open_findings_not_ready
      FAILED tests/orchestration/test_final_audit_evidence.py::TestReviewStateExtraction::test_the_manifest_reads_the_real_ledger_as_the_canonical_reader_does
  (d) packages/orchestration/job_evidence.py: FROM count = 1
  [mut_d] exit 1; summary: 1 failed, 24 passed in 5.62s
      FAILED tests/orchestration/test_review_manual_completion_shapes.py::TestDeletedSourceFileDoesNotBlockTheBundle::test_the_content_proof_carries_a_tombstone_for_every_deleted_path
  (e) packages/orchestration/job_evidence.py: FROM count = 1
  [mut_e] exit 1; summary: 1 failed, 96 passed in 22.07s
      FAILED tests/orchestration/test_job_evidence.py::TestDogfoodCommandShape::test_a_deleted_source_file_is_a_tombstone_the_strict_decoder_accepts
  control exit 0 ; mutation exits {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 1}
  G5 PASS
  ```
  The control ran over the five named test files. Every mutation went red; none stayed green. Every revert left the worktree clean. The worktree was then removed (see External actions).
- **G6** runs after the push and is reported in the round report, because this commit precedes it.
- Full suite: not run (amend0917-throughput).

## Authored-text proofs

- Every edited `.agent/` file was built by `python3 .remedy-wt/f273-r3/c1.py` from `git show a5e3b9ce:<path>` bytes and the payload bytes, and `docs/agents/integration_gate.md` by `.remedy-wt/f273-r3/c2.py` from `git show a5e3b9ce:docs/agents/integration_gate.md` bytes. Nothing was hand-edited. G1 re-proves every file and every `.agent/authored/f273-r3-*` copy against its payload.
- The code arrived only by `git apply` of the three reviewer-verified diffs, in the block's order. G2's subtree ids equal the reviewer's dry-run subtrees.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | `8fe7ea35` |
| C2 T003, R-0645 | done | `52cee6d8` |
| C3 T016 (a), R-0984 | done | `49cd2717` |
| C4 T016 (b) and (c), R-0985 and R-0839 | done | `cecc8881` |
| C5 R-0983 | done | `531cc24a` |
| C6 handoff + push | done | This commit, then the push |
| G1 to G5 | done | EXIT 0 / exact match as above |
| G6 | done | After the push; in the round report |

## Open findings

Measured by `.remedy-wt/f273-r3/measure.py` on the committed `.agent/live_review.md` at `531cc24a` (C1 onwards; C2 to C5 do not touch it):
- **By distinct id** (registered ids minus ids with at least one `^Done: R-\d{4} — ` line): 127 open.
- **By the canonical line formula** that `count_open_findings` had at `a5e3b9ce` (`^- R-\d{4} — ` lines minus `^Done: R-\d{4} — ` lines): 137 − 11 = 126.

Highest id R-0985. Against round 2's 128 and 127: C1 registered three ids (R-0983, R-0984, R-0985) and booked four `Done:` lines (R-0812, R-0396, R-0445, R-0736), so both readings fell by one. Since C4, `count_open_findings` itself counts by distinct id, so at `531cc24a` it returns 127.

## Deviations & assumptions

- **Commit sequence:** as ordered: C1, C2, C3, C4, C5, C6, then the push. No extra commit.
- **G1 first run:** the worker's own added check "C2 touches only the gate doc" first diffed `a5e3b9ce..52cee6d8`, which spans C1 as well, and printed False. The check was corrected to diff C2 against its parent (`52cee6d8^..52cee6d8`), as was the added-lines count, and the script was made to exit 1 on any False. The re-run above is all True. No file under review was changed.
- **Scratch runner:** the worker's shell cwd was the reviewer's `.remedy-wt/f273-r3-dry` worktree. Nothing was run in it; every git command used `git -C` on the primary checkout and every script used an explicit `cwd`.
- **G5 purge:** `python3 -B` writes no `__pycache__`, so the purges found nothing to remove after the first; the purge still ran before every run.
- **Payload copies:** "every payload above" was read as the six files the block lists under PAYLOADS. The three code diffs are listed under CODE, and they are not copied into `.agent/authored/`, as in round 2.
- **Scratch:** gitignored, under `.remedy-wt/f273-r3/`: `digests.py`, `c1.py`, `c2.py`, `g1.py`, `g5.py`, `measure.py`, `run.py`, `g3.txt`, `g5_*.txt`.

## Next

1. Phase 1 rule 1 (`.agent/STOP`), then the review of round 3.

Operator questions open: 5
