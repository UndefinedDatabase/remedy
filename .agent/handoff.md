# Handoff — F036, round 8 (the closure sequence's evidence round: book round 7, read the
self-use generator, build the evidence bundle and the review package at the accepted head)

## Session

SESSION 2 of feature F036 · round 8 · rounds so far 8. Context remaining at handback: a large
majority of the context budget is left — this round read AGENTS.md in full, the block, the three
payloads, and the handback template before writing anything; it applied the booking diff, rewrote
`.agent/plan.md`, ran the self-use generator's two calls, ran the evidence tool and the review
package script end to end (no summarizing, both to completion), and ran every gate (G1–G5) for
real before writing this handback.

## Range

Review of `6842325a2..HEAD` (`HEAD` is this handback's own commit, `F036 R8 C3`, on
`feature/f036-guided-result-tour`).

## Commits

### 1fdd2a3ca F036 R8 C1: copy round 8 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f036-r8-block.md | 158/0 | copy of the block, verified line count and sha256 |
| .agent/authored/f036-r8-booking.diff | 12/0 | copy of the reviewer's booking.diff payload |
| .agent/authored/f036-r8-create_f036_evidence.py | 164/0 | copy of the reviewer's evidence-tool payload |
| .agent/authored/f036-r8-plan.md | 27/0 | copy of the reviewer's plan.md payload |

361 insertions total, exactly the block's own C1 note (158-line block + 203).

### 153537dc8 F036 R8 C2: book round 7, resolve R-1090
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 4/0 | round 7's `Gate:` entry and the `Done: R-1090` resolution line, appended by booking.diff |
| .agent/plan.md | 6/9 | rewritten to the reviewer's plan.md payload |

Measured exactly the block's own C2 expected numstat: 4/0, 6/9. This commit's full sha,
`153537dc8e5a6bb7061f220cdeaffbc1829d3067`, is the round's ACCEPTED HEAD.

### <this commit> F036 R8 C3: rewrite handoff for round 8 with the evidence and package readings
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, per docs/agents/handback_template.md |

## External actions

- `git push -u origin feature/f036-guided-result-tour` immediately after C2, before A0 — outcome:
  `6842325a2..153537dc8 feature/f036-guided-result-tour -> feature/f036-guided-result-tour`,
  tracking set up.
- A0 (self-use reading, no commit): `packages.orchestration.self_use_generator.
  generate_and_append_if_empty()` then `packages.orchestration.self_use_queue.
  next_self_use_item()`, run from the repository root at C2. Outcome below (Verification).
- A1 (evidence job, no commit): `bash -c 'python3 .remedy-wt/f036-r8-payloads/
  create_f036_evidence.py > .remedy-wt/f036-r8-worker/evidence.log 2>&1; echo "REAL_EXIT=$?"'`.
  Outcome: `REAL_EXIT=0`. Full readings below.
- A2 (review package, no commit): `bash -c 'bash scripts/make_review_zip.sh --evidence-dir
  .remedy-wt/f036-r8-evidence > .remedy-wt/f036-r8-worker/zip.log 2>&1; echo "REAL_EXIT=$?"'`,
  `REMEDY_REVIEW_DIR` unset. Outcome: `REAL_EXIT=0`. Full readings below.
- `git push origin feature/f036-guided-result-tour` — run immediately after this commit per the
  bundle order. Its real outcome is reported in the round's reply (G6), not here, because this
  file is written before the push happens.
- No `gh pr create`, no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push,
  no `git stash`, no `git worktree add`/`remove` — none of these were run, per constraints 5 and 6.

## Verification

**G1 TRANSPORT** — PAYLOADS table readings (before use), all MATCH:
```
booking.diff:               12 lines, 5122 bytes, sha256 df52ceafeb4179852c3feda72d7fbd8cee1fc8e89ef4b2980b138091b51cd8a3
create_f036_evidence.py:   164 lines, 7969 bytes, sha256 2f33db1973c7c898d73976e30a2af98cbb2c89e23a6657c24141354d3b0e4b3a
plan.md:                    27 lines,  908 bytes, sha256 7165b60fd9e75258ee4c871c5589ed37c03c6cbd2cda3b137de3888a71c95c8a
```
Block self-check: 158 lines, sha256
`3a692d983f8c7b5cf46212f8053b98b9423b67a4d2c62246bd0f0c0a86dcfaad` — MATCH on both readings given
in the delegation message. `.agent/authored/f036-r8-*` copies vs. sources, read back via
`git show 1fdd2a3ca:<path>`, all byte-identical (sha256-verified):
```
f036-r8-block.md                  vs .remedy-wt/f036-r8/block.md                               MATCH
f036-r8-booking.diff              vs .remedy-wt/f036-r8-payloads/booking.diff                   MATCH
f036-r8-create_f036_evidence.py   vs .remedy-wt/f036-r8-payloads/create_f036_evidence.py        MATCH
f036-r8-plan.md                   vs .remedy-wt/f036-r8-payloads/plan.md                        MATCH
```
Insertions at C1: 361 (measured via `git diff --cached --stat` before commit), equal to the
block's 158 + 203, under the 500-line cap.

**G2 THE BOOKING** — at C2 (`153537dc8`), `git show <C2>:<path>`:
```
.agent/live_review.md   341971 bytes  sha256 233d6cc5e3ee36457ed1a1222beef4035d9077df886e99554de6d27129d6eb4d
.agent/plan.md             908 bytes  sha256 7165b60fd9e75258ee4c871c5589ed37c03c6cbd2cda3b137de3888a71c95c8a
```
Both MATCH the block's G2 table exactly. `open_finding_ids` (`scripts.rotate_live_review`) over
`.agent/live_review.md` at C2 read `[]`, matching the reviewer's simulation.
```
python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_golden_path.py
369 passed in 37.82s
REAL_EXIT=0
```
Matches the reviewer's simulation reading (369 passed, exit 0) exactly.

**G3 THE BUNDLE** — A1, `create_f036_evidence.py`'s printed log, in full up to the summary:
```
head 153537dc8e5a6bb7061f220cdeaffbc1829d3067
ancestry-path count 53
plain count 53
collected node ids 1258, deselected 7
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 1255, 'failed': 0, 'skipped': 3}, output_hash c4da699c7a42c328dbb1005033310b6b6737006bc2ac4c4b4511977a8d49ff66
validate_verification_tests problems [] passed 1255
is_valid_current_run True
validation_errors []
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
```
REAL_EXIT=0. Ancestry-path count and plain count are EQUAL at 53 — two more than the reviewer's
dry-run reading of 51, matching the block's note "At C2 both ancestry counts read two more."
Collected node ids 1258 with 7 deselected, none unsafe among the real ids, the planted id answers
"a local absolute path" — all matching the reviewer's dry run exactly. Pytest exit 0 with 1255
passed and 3 skipped — matching the reviewer's dry run exactly.
`validate_verification_tests` problem list: EMPTY (`[]`), passed count 1255.
`is_valid_current_run`: `True`, `validation_errors`: `[]`.
Gate files the evidence directory holds, confirmed on disk under
`.remedy-wt/f036-r8-evidence/`: `artifact_contract_gate.json`, `change_provenance_gate.json`,
`commit_execution_gate.json`, `fresh_evidence_gate.json`, `runtime_integration_gate.json`,
`final_verifier_report.json`, plus `manifest.json`, `review_subject.json`, `job_report.json`,
`verification_tests.json`, `workspace.diff` and 53 files under `review_commit_patches/`, among
others (full directory listing captured in `.remedy-wt/f036-r8-worker/evidence.log` and the
worker's directory listing). Job id `f036r8e1001`, matching the block.

**G4 THE PACKAGE** — A2, `make_review_zip.sh`'s printed summary:
```
UNCHANGED: runtime_integration_gate.json — rebuilt from source; identical to existing
Evidence refresh completed for staged copy.
Observability index generated from staged bytes: evidence/current/self_run_observability_index.json
{"member_count": 6661, "authoritative_count": 32, "symlink_count": 0, "tombstone_count": 0, "final_path": "/home/decodeux/Repos/remedy-history/zips/remedy-review-20260928-094901-READY_FOR_REVIEW.zip", "final_sha256": "e2bd771b3f1c1a52fcc7e73cdae50c4fd4a837107ee5e46b76d79d8b8dffc2f4", "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW", "evidence_authoritative": true, "review_subject_alignment": "PASS", "manifest_sha256": "d048cba7a2205e83e0471e7e3169cda4addd53fd1ec384bc4c37f7a415a91b87"}

============================================
REVIEW_PACKAGE_CREATED=true
PACKAGE_STATUS=READY_FOR_REVIEW
PACKAGING_CWD=/home/decodeux/Repos/remedy
EVIDENCE_DIR=.remedy-wt/f036-r8-evidence
REVIEW_SUBJECT_ALIGNMENT=PASS
EVIDENCE_AUTHORITATIVE=true
REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260928-094901-READY_FOR_REVIEW.zip
============================================

ZIP CREATED AND READY FOR FINAL REVIEW

32M	/home/decodeux/Repos/remedy-history/zips/remedy-review-20260928-094901-READY_FOR_REVIEW.zip
Included files: 6661
Branch: feature/f036-guided-result-tour
Commit: 153537dc8e5a6bb7061f220cdeaffbc1829d3067
```
REAL_EXIT=0. `PACKAGE_STATUS=READY_FOR_REVIEW` (the reading, not the exit code).
`EVIDENCE_AUTHORITATIVE=true`. Package filename
`remedy-review-20260928-094901-READY_FOR_REVIEW.zip`, independently re-hashed:
```
sha256sum /home/decodeux/Repos/remedy-history/zips/remedy-review-20260928-094901-READY_FOR_REVIEW.zip
e2bd771b3f1c1a52fcc7e73cdae50c4fd4a837107ee5e46b76d79d8b8dffc2f4
```
— matches the tool's own `final_sha256` exactly. Archived directory:
`/home/decodeux/Repos/remedy-history/zips` (absolute). `.review_zip_manifest.json` read from
inside the package via `zipfile`:
```
committed_review_subject:
  base_commit: 9dc2f2a796d48a47119252c1ec8634230b00bf90
  head_commit: 153537dc8e5a6bb7061f220cdeaffbc1829d3067
  base_is_ancestor: true
  commit_count: 53
```
`head_commit` equals C2's full sha exactly; `base_commit` equals the fork point
`9dc2f2a796d48a47119252c1ec8634230b00bf90` the block states. `zipfile.is_zipfile(...)` read
`True`; `ZipFile(...).testzip()` read `None`.

**G5 THE TREE** — after A2:
```
python3 -m apps.cli.main integrity check --json
```
Six checks, all `pass`, `fail_count` 0, `ok` true: `handler_import` (handlers=167),
`live_review_verdict` (last Gate verdict PASS), `plan_consistency` (unchecked=0), `relevant_
untracked` (untracked=0, relevant=0), `repo_root_hygiene` (no reviewer scratch, evidence dir or
archive at the root), `high_blockers_open` (no open blocker/high findings).
`git status --porcelain` empty. `git worktree list | wc -l` = 62 (unchanged — no worktree
created or removed this round).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| A0 | done | both calls read `None`; `git status --porcelain` empty, nothing to restore |
| A1 | done | evidence bundle built at `.remedy-wt/f036-r8-evidence/`, exit 0, all readings match |
| A2 | done | package `READY_FOR_REVIEW`, `EVIDENCE_AUTHORITATIVE=true`, exit 0 |
| C3 | done | this handback |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | |
| G5 | done | |

## Authored-text proofs

`booking.diff` was applied via `git apply --check` (exit 0) then `git apply` (exit 0) — never
edited, never retyped. All three payloads (`booking.diff`, `create_f036_evidence.py`, `plan.md`)
were verified line count/byte count/sha256 against the PAYLOADS table before use, and the
committed `.agent/authored/f036-r8-*` copies read back byte-identical to their sources via
`git show` (G1, above). `.agent/plan.md` was REWRITTEN to the payload file by `shutil.copyfile`,
never hand-edited; its post-write bytes/sha256 equal the payload table's own row and C2's
resulting file hash matched the reviewer's G2 table exactly. `create_f036_evidence.py` was run
unedited, directly from `.remedy-wt/f036-r8-payloads/`, as the block specifies for A1 — it was
never copied into the working tree as an executable, only into `.agent/authored/` for the
transport record (C1), and that copy was never the one executed.

## Deviations & assumptions

None. The round's commit sequence (C1, C2), actions (A0, A1, A2) and this handback (C3) followed
the block's ordered bundle exactly, with no split commit, no extra commit, and no reordering.
Every gate ran for real, to completion, with no summarized "green": A1's evidence tool and A2's
package script were each run to their own natural completion under the 30-minute timeout budget
the block allows, and both finished well inside it.

## Next

Per the block's `## Next` order: (1) Phase 1 rule 1 — read `.agent/STOP` from disk at session
start. (2) The review of round 8. (3) The closing round: the booking of round 8, the ledger
rotation, the STATUS line with the README counters in the same commit, and the pull request.
Open-findings count: 0, as `open_finding_ids` reads at C2. Operator questions open: 1.
