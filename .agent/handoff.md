# Handback — F263 Human-change absorption (absorb) · Round 2 · Book round 1, land T001's evidence path — BLOCKED at G4

## Session

SESSION 1 of feature F263 · round 2 · rounds so far 2

This round booked round 1's PASS and DECISION F263 D2 into the ledger
(C2), then applied the reviewer's three diffs and new test file to land
T001's second half — the job's evidence export copies every human change
record into the bundle and verifies each copy into
`human_change_integrity.json`, blocking the final verifier and the review
package's READY gate when a copy does not verify (C3). G1 through G3
passed with every reading exactly matching the block. G4's `ruff check`
read real exit 1 on a reviewer-payload file (`F401` unused import in
`tests/orchestration/test_human_change_evidence.py`, copied verbatim in
C3); per the block's constraint 4 and AGENTS.md "If Blocked" the round
stopped there — no payload was edited, G5 did not run. Context
self-assessment: roughly half the session's working context budget
remained at handback.

## Range

Review of `a34cc4b0`..`HEAD`.

## Commits

### 63099a30 F263 R2 C1a: copy round 2 block and bookkeeping payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f263-r2-block.md | +215/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f263-r2-ledger.md | +2/-0 | Payload copy |
| .agent/authored/f263-r2-decisions.md | +43/-0 | Payload copy |
| .agent/authored/f263-r2-plan.md | +31/-0 | Payload copy |

Measured insertions by `git show --numstat 63099a30`: 291 (215 + 2 + 43 +
31), matching the block's stated formula "this block's line count plus
76" (215 + 76 = 291) exactly. Under the 500 cap.

### 37d86231 F263 R2 C1b: copy round 2 product payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f263-r2-product.diff | +173/-0 | Payload copy |
| .agent/authored/f263-r2-fixtures.diff | +35/-0 | Payload copy |
| .agent/authored/f263-r2-docs.diff | +14/-0 | Payload copy |
| .agent/authored/f263-r2-test_human_change_evidence.py | +155/-0 | Payload copy |
| .agent/authored/f263-r2-mutations.py | +81/-0 | Payload copy (G5 tool) |

Measured insertions by `git show --numstat 37d86231`: 458 (173 + 35 + 14
+ 155 + 81), matching the block's expected 458 exactly.

### 75e7097b F263 R2 C2: book round 1's PASS and DECISION F263 D2

| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +43/-0 | Append of decisions.md payload |
| .agent/live_review.md | +2/-0 | Append of ledger.md payload |
| .agent/plan.md | +8/-11 | Rewritten to the round-2 `plan.md` payload |

Measured insertions by `git show --numstat 75e7097b`: `43 0
.agent/decisions.md`, `2 0 .agent/live_review.md`, `8 11 .agent/plan.md`
— matching the block's expected 43, 2, 8 exactly.

### e9df6f53 F263 R2 C3: carry human change records into the evidence package and block on a broken one

| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS_closure_protocol.md | +2/-1 | `git apply` of docs.diff |
| packages/orchestration/final_verifier.py | +9/-0 | `git apply` of product.diff — reads `human_change_integrity.json`, blocks on failure |
| packages/orchestration/human_change.py | +38/-0 | `git apply` of product.diff — `export_human_change_records`, `INTEGRITY_FILE` |
| packages/orchestration/job_evidence.py | +8/-0 | `git apply` of product.diff — calls the export into the bundle |
| packages/orchestration/manual_attestation.py | +3/-0 | `git apply` of product.diff — writes an intact-empty gate |
| scripts/build_review_manifest.py | +9/-2 | `git apply` of product.diff — closed-schema READY gate for the new file |
| tests/orchestration/test_human_change_evidence.py | +155/-0 | New test file, copied whole then `git add`ed |
| tests/orchestration/test_review_authoritative_e2e.py | +3/-1 | `git apply` of fixtures.diff |
| tests/orchestration/test_review_package_status.py | +2/-0 | `git apply` of fixtures.diff |

Measured insertions by `git show --numstat e9df6f53`: 2, 9, 38, 8, 3, 9,
155, 3, 2 in the same order — matching the block's expected 2, 9, 38, 8,
3, 9, 155, 3, 2 exactly. `git apply --check` then `git apply` for
product.diff, fixtures.diff, docs.diff: real exit 0, 0 for each (6
commands, 6 zeros).

### (this commit) F263 R2 C4: rewrite handoff for round 2

| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per `docs/agents/handback_template.md` — a handback cannot table the commit that writes it (R-0149 self-reference exception) |
| .agent/plan.md | rewritten | AGENTS.md "If Blocked" step 2 — records the exact G4 blocker in the Current Step, so a reader of `plan.md` alone sees the round stopped and why, without needing this handback. Bundled into C4 rather than the block's plain "handoff.md, its own commit" because both are single-state-file rewrites under the same commit-cap exemption and both exist to record the identical blocked state; declared here as a deviation from the block's literal C4 description. |

## External actions

- No `gh pr create`, no merge, no branch deletion — none ordered, none
  taken.
- `git push origin feature/f263-human-change-absorption` after C4 — real
  outcome reported in the worker's final reply (G6 readings cannot live
  in this committed file per the block).
- G5's worktree (`.remedy-wt/f263-r2-mut`) was never created — the round
  stopped at G4 before reaching G5.

## Verification

**G1 — transport**: every payload's lines/bytes/sha256 measured against
the block's PAYLOADS table: all eight rows matched exactly (ledger.md
2/2337, decisions.md 43/3200, plan.md 31/1272, product.diff 173/9741,
fixtures.diff 35/2637, docs.diff 14/807, test_human_change_evidence.py
155/6925, mutations.py 81/3178 — sha256 digests all equal to the table).
Every committed `.agent/authored/f263-r2-*` blob read with `git show
<commit>:<path>` compared byte-for-byte against its `.remedy-wt/` source:
all nine pairs (the block plus the eight payloads) byte-identical = True.

**G2 — the booking**: concatenation checks — `git show a34cc4b0:.agent/live_review.md`
+ ledger.md payload == `git show 75e7097b:.agent/live_review.md`: True.
`git show a34cc4b0:.agent/decisions.md` + decisions.md payload == `git
show 75e7097b:.agent/decisions.md`: True. plan.md payload == `git show
75e7097b:.agent/plan.md`: True. sha256 at C2: `.agent/live_review.md`
373452 bytes `1ed2113b5de484068134735d52690072871b06d0b2364c1f3271e62e6efd70c7`;
`.agent/decisions.md` 1881309 bytes
`b1ce8ec76905935c5572d0722588e3a54c4d62ca4b7280f7d49d850c2c3c8894`;
`.agent/plan.md` 1272 bytes
`dc323c4f92daeefe6710069fcc88f9b971df6f54636e2178b624518b92587790` — all
three matching the block's reviewer-simulated table exactly. Open finding
ids via `scripts/rotate_live_review.py`'s `open_finding_ids` over the
file TEXT: 28 at `a34cc4b0`, 28 at C2, `base - c2 = []`, `c2 - base = []`
— both differences empty, matching the reviewer's reading of 28 and 28.

**G3 — the product bytes**: at C3, `git show e9df6f53:<path>` sha256 for
all nine G3-table paths matched the block's table exactly:
`human_change.py` 11553 bytes `e6c99c569a46728c94f4bc44f7e3665194069b1c9f77fd4bab3dc36b0caad3a1`;
`job_evidence.py` 137619 bytes `a0f8f792e72c70825253945f299a2ef4e839d50b96d06b119c2455ade420817f`;
`final_verifier.py` 45021 bytes `098f313906c57335760dffbb1697eb14bad44216edc96693dd814a3fc6eb4eea`;
`manual_attestation.py` 16334 bytes `11cc966952dd572d5217d82a7d99cc6b6ed41868602ff27e3fb501dd7c1888e3`;
`build_review_manifest.py` 180741 bytes `3ef54bb3fa9e8aa0280702d5edf7630c74374126f2f41c5eb426520b40a66d6f`;
`test_review_authoritative_e2e.py` 20641 bytes `2c58f0ad10e2f91e84b01cefeed522aebf49f09cc4a2144113ee7f04c003b45b`;
`test_review_package_status.py` 37968 bytes `d7cafa28e2debcbda059debbfea2f39279a22171ffcb199f224667979658a841`;
`STATUS_closure_protocol.md` 20232 bytes `689ab1f11cba0565023b1557f4b9f8b391655172cacefa45d3fa84dfe173c344`;
`test_human_change_evidence.py` 6925 bytes `abeb56888b1a7da7eb16aa24484333330a98dbc7073e7032ef001cb18249a512`.

**G4 — the tests, RED**: in the primary checkout at C3, SERIALLY:
`python3 -m pytest -q -p no:cacheprovider` over the block's exact
22-file selection (including `tests/cli/test_golden_path.py`, which the
command orders and the reviewer's own dry run excluded) →
`1918 passed in 316.72s`, real exit 0. The reviewer's disposable-worktree
run without the golden path read `1874 passed, 2 skipped`; the delta is
explained by the golden path's own tests and by this checkout's toolchain
differing from a fresh worktree (consistent with the round-1 handback's
same observation) — no failures, no unexpected skips either way. Then
`python3 -m ruff check` over the G3 table's Python paths (docs file
excluded): **real exit 1** —
```
F401 [*] `packages.orchestration.data_paths.job_evidence_dir` imported but unused
  --> tests/orchestration/test_human_change_evidence.py:16:47
Found 1 error.
[*] 1 fixable with the `--fix` option.
```
`job_evidence_dir` is imported at line 16 of the reviewer's payload and
never referenced anywhere else in the file (confirmed by `grep -n
job_evidence_dir tests/orchestration/test_human_change_evidence.py`,
one hit — the import line itself). This contradicts the block's stated
expectation of real exit 0 for this command. The worker does not edit or
retype a payload (block rule + constraint 1), so the file was left as
committed and the gate is reported RED rather than silently fixed.
`python3 -m apps.cli.main integrity check --json` was still run for a
complete record (read-only, no repair): all five checks (`handler_import`,
`live_review_verdict`, `plan_consistency`, `relevant_untracked`,
`high_blockers_open`) `pass`, `fail_count: 0`, `ok: true`, `passed: true`,
real exit 0.

**G5 — NOT RUN.** Per the block's constraint 4 ("If a gate goes red,
STOP... Do not repair the reviewer's payloads") the round stopped at
G4's ruff failure. No `.remedy-wt/f263-r2-mut` worktree was created; no
mutation was applied or reverted.

## Authored-text proofs

- `.agent/authored/f263-r2-block.md` (C1a) == `.remedy-wt/f263-r2-block.md`: byte-identical True.
- `.agent/authored/f263-r2-ledger.md` (C1a) == `.remedy-wt/f263-r2-payloads/ledger.md`: byte-identical True.
- `.agent/authored/f263-r2-decisions.md` (C1a) == `.remedy-wt/f263-r2-payloads/decisions.md`: byte-identical True.
- `.agent/authored/f263-r2-plan.md` (C1a) == `.remedy-wt/f263-r2-payloads/plan.md`: byte-identical True.
- `.agent/authored/f263-r2-product.diff` (C1b) == `.remedy-wt/f263-r2-payloads/product.diff`: byte-identical True.
- `.agent/authored/f263-r2-fixtures.diff` (C1b) == `.remedy-wt/f263-r2-payloads/fixtures.diff`: byte-identical True.
- `.agent/authored/f263-r2-docs.diff` (C1b) == `.remedy-wt/f263-r2-payloads/docs.diff`: byte-identical True.
- `.agent/authored/f263-r2-test_human_change_evidence.py` (C1b) == `.remedy-wt/f263-r2-payloads/test_human_change_evidence.py`: byte-identical True.
- `.agent/authored/f263-r2-mutations.py` (C1b) == `.remedy-wt/f263-r2-payloads/mutations.py`: byte-identical True.
- APPLIED text: `product.diff`, `fixtures.diff`, `docs.diff` were each
  `git apply --check`ed (exit 0) then `git apply`ed (exit 0) unedited,
  never retyped; G3's post-apply sha256 matches against the reviewer's
  table are the disk-to-disk proof that the applied bytes equal the
  payload's bytes.
- APPLIED text: `tests/orchestration/test_human_change_evidence.py` as
  committed at C3 (`git show e9df6f53:tests/orchestration/test_human_change_evidence.py`)
  compared byte-for-byte to the committed
  `.agent/authored/f263-r2-test_human_change_evidence.py` blob and to the
  source payload: sha256
  `abeb56888b1a7da7eb16aa24484333330a98dbc7073e7032ef001cb18249a512`
  all three, equal — the file that fails ruff is confirmed to be the
  reviewer's own unmodified text, not a transcription error.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 291 insertions, matches block formula (215+76) |
| C1b | done | 458 insertions, matches block exactly |
| C2 | done | 43/2/8 insertions, matches block exactly; G2 fully passed |
| C3 | done | 2/9/38/8/3/9/155/3/2 insertions, matches block exactly; G3 fully passed |
| C4 | done | this handback, bundled with plan.md per declared deviation |
| G1 | done | all readings match |
| G2 | done | all readings match |
| G3 | done | all readings match |
| G4 | blocked | pytest 1918 passed exit 0; ruff real exit 1 (F401 in reviewer payload `test_human_change_evidence.py`); integrity check all-pass exit 0 |
| G5 | skipped | not run — round stopped at G4 per constraint 4, before creating the mutation worktree |
| T001 (evidence path) | deviated | code and tests landed in C3 byte-identical to the reviewer's payload, but not certified done: the payload's own test file fails ruff, blocking the round's DONE-WHEN before G5's red-proofs could run |

## Deviations & assumptions

1. G4's `ruff check` read real exit 1, not the block's expected 0: an
   unused import (`job_evidence_dir`, F401) in the reviewer's payload
   `tests/orchestration/test_human_change_evidence.py`, applied verbatim
   in C3. Per the block's constraint 4 and AGENTS.md "If Blocked", the
   worker did not edit the payload and stopped the round here. G5 did not
   run as a result.
2. C4 bundles `.agent/handoff.md` and `.agent/plan.md` into one commit
   instead of the block's literal "handoff.md, rewritten, its own
   commit" — both are single-state-file rewrites (exempt from the
   insertion cap) recording the identical blocked state, and AGENTS.md
   "If Blocked" step 2 requires the plan.md update; splitting them into
   two commits would not change what either says.
3. G4's pytest command (run exactly as the block specifies, including
   `tests/cli/test_golden_path.py`) read `1918 passed` where the
   reviewer's own dry run — which explicitly excluded the golden path —
   read `1874 passed, 2 skipped`. Both are real exit 0 with zero
   failures; the count difference is explained by the golden path's own
   tests plus this checkout's toolchain (not a fresh disposable
   worktree), consistent with the same observation in round 1's handback.
   Not a gate failure.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round
2, then T002 — `remedy absorb`, the explicit command over the same
`absorb` path. Open findings count: 28. Operator-questions count: 0.
