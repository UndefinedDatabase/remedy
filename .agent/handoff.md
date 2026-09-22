# Handback — F278 Durable writes & loud failures · Round 6 · Book round 5, fail the secret detector closed, mark the first handler group

## Session

SESSION 1 of feature F278 · round 6 · rounds so far 6

This round booked round 5's PASS and DECISION F278 D5 into the durable
ledger files, then made `run_manifest._contains_secret` fail CLOSED — on any
exception from the redactor it reuses it now answers `True` (a detector that
failed cannot clear a value) instead of the old fail-open `False` — with a
test pinning the new answer and the old one still clear for an ordinary
value. It then marked every remaining blind `except Exception` handler in
`packages/orchestration/job_evidence.py` (29), `packages/orchestration/run_manifest.py`
(22, after the one behaviour-changing handler already carried its own reason
in C3) and `scripts/build_review_manifest.py` (27) with a
`# noqa: BLE001 — <reason>`, one file per commit, comment text only —
`marking_check.py` proved each marking commit changes no code, and its
negative control confirmed the fail-closed commit (which DOES change code)
correctly fails the same check. All five gates (G1–G5) ran clean and matched
the reviewer's dry-run readings exactly (transport, booking, product
bytes/BLE001/marking-check, tests, and the one red-proof mutation). Context
self-assessment: a comfortable majority of the working budget remains at
handback.

## Range

Review of `4353fb9e`..`HEAD`.

## Commits

### 8f405e71 F278 R6 C1a: copy round 6 block and bookkeeping payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f278-r6-block.md | +195/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f278-r6-decisions.md | +32/-0 | Bookkeeping copy of the decisions.md append payload |
| .agent/authored/f278-r6-ledger.md | +2/-0 | Bookkeeping copy of the live_review.md append payload |
| .agent/authored/f278-r6-plan.md | +29/-0 | Bookkeeping copy of the plan.md rewrite payload |

Measured insertions: 258 (block 195 + 63 payload lines), under the 500 cap;
matches the block's expected value exactly.

### 9fdca95e F278 R6 C1b: copy round 6 fail-closed payload, first marking diff and tools
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f278-r6-failclosed.diff | +41/-0 | Bookkeeping copy of the fail-closed detector diff |
| .agent/authored/f278-r6-mark_job_evidence.diff | +260/-0 | Bookkeeping copy of the job_evidence marking diff |
| .agent/authored/f278-r6-marking_check.py | +47/-0 | Bookkeeping copy of the G3 comment-only-proof tool |
| .agent/authored/f278-r6-mutations.py | +44/-0 | Bookkeeping copy of the G5 mutation-tool payload |

Measured insertions: 392 (41+260+47+44), matches the block's expected value
exactly.

### 21b5059d F278 R6 C1c: copy round 6 remaining marking diffs into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f278-r6-mark_run_manifest.diff | +199/-0 | Bookkeeping copy of the run_manifest marking diff |
| .agent/authored/f278-r6-mark_build_review_manifest.diff | +239/-0 | Bookkeeping copy of the review-manifest-builder marking diff |

Measured insertions: 438 (199+239), matches the block's expected value
exactly.

### 93c15092 F278 R6 C2: book round 5's PASS and DECISION F278 D5
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +32/-0 | `decisions.md` appended by byte concatenation |
| .agent/live_review.md | +2/-0 | `ledger.md` appended by byte concatenation |
| .agent/plan.md | +10/-10 | Rewritten to plan.md payload for round 6 |

Measured insertions: 44 (32+2+10), matches the block's expected value
exactly. Deletions: 10, all from the plan.md rewrite.

### 3b5ab6c8 F278 R6 C3: fail the manifest's secret detector closed when its redactor raises
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/run_manifest.py | +2/-2 | `_contains_secret`'s blind handler marked with a reason and its answer flipped `False`→`True`: a detector that failed cannot clear the value |
| tests/orchestration/test_run_manifest_security.py | +18/-0 | New `TestSecretDetectorFailsClosed` class: a failing redactor reports a secret, an ordinary value stays clear |

`git apply --check` real exit 0, `git apply` real exit 0. Measured
insertions: 20 (2+18), matches the block's expected value exactly.

### 38bbc406 F278 R6 C4: give each blind handler in job_evidence a reason
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/job_evidence.py | +29/-29 | Every one of the file's 29 blind `except Exception[:]` handlers gains `# noqa: BLE001 — <reason>`; comment text only, no code change (proved by marking_check.py) |

`git apply --check` real exit 0, `git apply` real exit 0. Measured
insertions: 29, matches the block's expected value exactly.

### 4e9d0d0b F278 R6 C5: give each blind handler in run_manifest a reason
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/run_manifest.py | +22/-22 | The remaining 22 blind handlers in the file (the 23rd, `_contains_secret`, was already marked in C3) gain `# noqa: BLE001 — <reason>`; comment text only |

`git apply --check` real exit 0, `git apply` real exit 0. Measured
insertions: 22, matches the block's expected value exactly.

### 2db5905b F278 R6 C6: give each blind handler in the review manifest builder a reason
| Path | +/- | Reason |
|---|---|---|
| scripts/build_review_manifest.py | +27/-27 | Every one of the file's 27 blind handlers gains `# noqa: BLE001 — <reason>`; two lines keep their `# pragma: no cover` after the noqa; comment text only |

`git apply --check` real exit 0, `git apply` real exit 0. Measured
insertions: 27, matches the block's expected value exactly.

### C7 (this commit) F278 R6 C7: rewrite handoff for round 6
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per docs/agents/handback_template.md |

## External actions

- `git worktree add --detach .remedy-wt/f278-r6-mut 2db5905b` — real exit 0.
- `python3 .remedy-wt/f278-r6-payloads/mutations.py .remedy-wt/f278-r6-mut` — real exit 0 (see Verification, G5).
- `git worktree remove --force .remedy-wt/f278-r6-mut` — real exit 0.
- `git worktree prune` — real exit 0.
- `git push origin feature/f278-durable-writes-loud-failures` — see Verification, G6, for the real outcome (reported separately since it runs after this commit).
- No `gh pr create`, no `gh pr merge`, no force-push, no `git stash`, no checkout of another branch: none run, per the block's constraints.

## Verification

BEFORE ANYTHING ELSE:
- `ls .agent/STOP` → `No such file or directory`, exit 2, absent (proceed).
- `git status --porcelain` → empty. `git branch --show-current` → `feature/f278-durable-writes-loud-failures`. `git log --oneline -1` → `4353fb9e F278 R5 C4: rewrite handoff for round 5`.
- Block bytes (R-0954): measured lines=195, sha256=`d6feee5d2f9293f34f1a5a42456cfcddce562d9eeb7d9419d4447c23a95cac2f`; matches both given readings exactly.
- `git worktree list` (before) → primary checkout + `.remedy-wt/job-129b3ad7206d4f8d` only.
- `git branch --list 'remedy/job-*' | wc -l` → 38.

PAYLOADS — all 9 measured and matched the block's table exactly (lines/bytes/sha256): decisions.md (32/2295), failclosed.diff (41/1871), ledger.md (2/2641), mark_build_review_manifest.diff (239/13801), mark_job_evidence.diff (260/14308), mark_run_manifest.diff (199/11098), marking_check.py (47/1875), mutations.py (44/1811), plan.md (29/1096). All sha256 readings matched the table verbatim.

G1 TRANSPORT — every `.agent/authored/f278-r6-*` copy read back with `git show <commit>:<path>` and compared byte-for-byte against its source: all 10 copies (block.md + 9 payloads) matched exactly (block.md against `.remedy-wt/f278-r6-block.md`, the other 9 against their `.remedy-wt/f278-r6-payloads/` originals).

G2 THE BOOKING — at C2 (`93c15092`), the byte counts matched `4353fb9e` bytes plus each payload's bytes by strict concatenation (live_review.md: 435949+2641=438590; decisions.md: 1849815+2295=1852110; plan.md rewritten to 1096), and the sha256 read with `git show 93c15092:<path>` matched the reviewer's dry-run reading for all three files:
- `.agent/live_review.md`: bytes=438590, sha256=`13baaf026006aea7a1f73f7bd57b49dc42a0b9879aeeab0f10fcd6778aedf588` — MATCH
- `.agent/decisions.md`: bytes=1852110, sha256=`b49d866c38d1d8a4b3aebadb1116cfbbb94eefd5be0ad1876499c476c943816b` — MATCH
- `.agent/plan.md`: bytes=1096, sha256=`db40aced6129afd6dd2f8a330bc88eb1306df09d1b65b70dc3a2daac461a4944` — MATCH

Open-finding-id set via `open_finding_ids` (`scripts/rotate_live_review.py`) over `.agent/live_review.md` TEXT: at `4353fb9e` count=26; at C2 (`93c15092`) count=26; `base - c2` = `[]`; `c2 - base` = `[]` — both differences empty, matching the reviewer's 26/26.

G3 THE PRODUCT BYTES AND THE COMMENT-ONLY PROOF — at C6 (`2db5905b`), sha256 of each file read with `git show 2db5905b:<path>`, all four MATCH:
- `packages/orchestration/job_evidence.py`: bytes=137163, sha256=`5167debd2143cfd0e7f3b1db35211d54f422f493b2e448449aaba0db56640347`
- `packages/orchestration/run_manifest.py`: bytes=338975, sha256=`85ae5b97395af295bcfffec67d045263e1616c969834ddf9a2d6a70032bff284`
- `scripts/build_review_manifest.py`: bytes=180325, sha256=`59744d2e5801c60ce1aec0917cb6c2d1e5cb19ad2682b294832b30cc6c246b53`
- `tests/orchestration/test_run_manifest_security.py`: bytes=8734, sha256=`94c56e4208ce70642bf2b53ac7d8ff92bafffecf76db46b3fa504c53da365a5a`

`python3 .remedy-wt/f278-r6-payloads/marking_check.py . 38bbc406 4e9d0d0b 2db5905b` → `38bbc406 OK pairs=29`, `4e9d0d0b OK pairs=22`, `2db5905b OK pairs=27`, real exit 0 — matches the block's expected pairs 29/22/27 exactly. The negative control, `python3 .remedy-wt/f278-r6-payloads/marking_check.py . 3b5ab6c8`, read `3b5ab6c8 VIOLATION pairs=20` with reasons `2 lines removed but 20 added`, `code changed: 'return False' -> 'return True'`, `no reasoned noqa: 'return True'`, real exit 1 — VIOLATION as the block requires, since C3 legitimately changes code (the fail-closed behaviour change) and is not a pure marking commit.

`python3 -m ruff check --select BLE001 packages/orchestration/job_evidence.py packages/orchestration/run_manifest.py scripts/build_review_manifest.py` → `All checks passed!`, real exit 0.

G4 THE TESTS — command (the block's own, in the primary checkout at C6, WITH `tests/cli/test_golden_path.py` as the block's own command lists it):
```
python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_run_manifest_security.py tests/orchestration/test_run_manifest.py tests/orchestration/test_job_evidence.py tests/orchestration/test_review_zip_hygiene.py tests/orchestration/test_run_manifest_standard_json.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py
```
Result: `344 passed in 220.31s (0:03:40)`, real exit 0 (`${PIPESTATUS[0]}`). The reviewer's own run, WITHOUT the golden path, in a disposable worktree carrying C2 to C6, read `301 passed, 1 skipped` at exit 0; this run's command includes `tests/cli/test_golden_path.py` as the block states it, giving a higher pass count and no reported skip — consistent with the block's own framing ("report what you read").

`python3 -m ruff check` over all four paths of the G3 table → `All checks passed!`, real exit 0.

`python3 -m apps.cli.main integrity check --json` → `fail_count: 0`, `ok: true`, `passed: true`, all 5 checks `pass` (`handler_import` handlers=145, `live_review_verdict`, `plan_consistency` with `unchecked=0, context_complete=False`, `relevant_untracked` with `untracked=0, relevant=0`, `high_blockers_open` — no open blocker/high findings). Real exit 0.

G5 THE RED PROOF — `git worktree add --detach .remedy-wt/f278-r6-mut 2db5905b` real exit 0. `python3 .remedy-wt/f278-r6-payloads/mutations.py .remedy-wt/f278-r6-mut` real exit 0, full output:
```
control_before REAL_EXIT=0
2 passed in 0.28s
m1_detector_fails_open_again FROM count in file: 1
m1_detector_fails_open_again REAL_EXIT=1
FAILED tests/orchestration/test_run_manifest_security.py::TestSecretDetectorFailsClosed::test_a_failing_redactor_reports_a_secret
1 failed, 1 passed in 0.26s
m1_detector_fails_open_again restored byte-identical: True
control_after REAL_EXIT=0
2 passed in 0.25s
```
Every reading matches the reviewer's stated expectations exactly: control_before `2 passed`/exit 0; m1 `1 failed, 1 passed`/exit 1 at `test_a_failing_redactor_reports_a_secret`; control_after `2 passed`/exit 0; the restore `True`.

`git worktree remove --force .remedy-wt/f278-r6-mut` real exit 0. `git worktree prune` real exit 0. `git worktree list` afterward → primary checkout (`feature/f278-durable-writes-loud-failures`) and `.remedy-wt/job-129b3ad7206d4f8d` only — the mutation worktree is gone.

G6 TREE AND PUSH — reported in the session's final reply, not this file, since it runs after this commit (C7). The handback cannot contain readings that postdate its own write.

## Authored-text proofs

Fidelity protocol (docs/agents/split_workflow.md, R-0147/R-0144/R-0148): byte-identity proof = mechanical disk-to-disk comparison of the applied location against the `.agent/authored/` copy.

- `decisions.md` (append): `.agent/decisions.md` at C2 sha256 `b49d866...c943816b` == payload sha256 concatenated onto the `4353fb9e` bytes (G2). MATCH.
- `ledger.md` (append): `.agent/live_review.md` at C2 sha256 `13baaf0...78aedf588` == payload sha256 concatenated onto the `4353fb9e` bytes (G2). MATCH.
- `plan.md` (rewrite): `.agent/plan.md` at C2 sha256 `db40ace...2daac461a4944` == payload sha256 exactly (G2). MATCH.
- `failclosed.diff` (applied): `.agent/authored/f278-r6-failclosed.diff` at C1b byte-identical to the payload (G1); `git apply --check` and `git apply` both real exit 0 at C3; resulting `run_manifest.py`/test bytes are part of the C6 sha256 table (G3, since run_manifest.py is touched again in C5). MATCH.
- `mark_job_evidence.diff` (applied): `.agent/authored/f278-r6-mark_job_evidence.diff` at C1b byte-identical to the payload (G1); `git apply --check` and `git apply` both real exit 0 at C4; resulting file's sha256 at C6 matches the G3 table. MATCH.
- `mark_run_manifest.diff` (applied): `.agent/authored/f278-r6-mark_run_manifest.diff` at C1c byte-identical to the payload (G1); `git apply --check` and `git apply` both real exit 0 at C5; resulting file's sha256 at C6 matches the G3 table. MATCH.
- `mark_build_review_manifest.diff` (applied): `.agent/authored/f278-r6-mark_build_review_manifest.diff` at C1c byte-identical to the payload (G1); `git apply --check` and `git apply` both real exit 0 at C6; resulting file's sha256 at C6 matches the G3 table. MATCH.
- `marking_check.py`: a TOOL run against the primary checkout at C4/C5/C6 and the negative control at C3, never applied to a tracked file. `.agent/authored/f278-r6-marking_check.py` at C1b verified byte-identical to the payload (G1). N/A for an "applied location" comparison by design.
- `mutations.py`: a TOOL run against the disposable mutation worktree, never applied to a tracked file. `.agent/authored/f278-r6-mutations.py` at C1b verified byte-identical to the payload (G1). N/A for an "applied location" comparison by design.
- This block (`f278-r6-block.md`): `.agent/authored/f278-r6-block.md` at C1a verified byte-identical to `.remedy-wt/f278-r6-block.md` (G1) and to the two readings given in the delegation message.

## Item-Status Table

| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C1c | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | |
| C7 | done | |
| G1 TRANSPORT | done | |
| G2 THE BOOKING | done | |
| G3 THE PRODUCT BYTES AND THE COMMENT-ONLY PROOF | done | |
| G4 THE TESTS | done | |
| G5 THE RED PROOF | done | |
| G6 TREE AND PUSH | done | runs after C7; real readings reported in the session's final chat reply, not this file |

## Deviations & assumptions

The round followed the block's ordered commit sequence (C1a, C1b, C1c, C2,
C3, C4, C5, C6, C7) exactly, touched exactly the tracked path set the block
names (verified via `git diff --name-only 4353fb9e HEAD` before C7), ran no
full suite, and left `.remedy-wt/job-129b3ad7206d4f8d`, its branch, and every
existing stash untouched. No other deviation.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 6,
then T003's next marking group: the job, pingpong, apply, runtime and
snapshot modules, each handler narrowed or given a reason. Open findings: 26.
Operator questions: 0.
