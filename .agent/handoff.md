# Handback — F055 round 8 — book round 7, repair R-1320, the one full suite again, the evidence job and the review package

## Session

SESSION 1 of feature F055 · round 8 · rounds so far 8

Context self-assessment: every step landed on the first attempt — the digest checks, C1's
bookkeeping copy, C2's repair and its two deterministic tests (confirmed red at `ae3acace0` and
green at the prepared file by a temporary swap, never committed), C3's one full suite (green,
exit 0), A1's evidence job (exit 0, a clean bundle) and A2's review package (`READY_FOR_REVIEW`)
all read exactly as the block described, so the round closes with the package built and nothing
left for the operator to repair.

Fortschritt: ~95 % (everything but the closing round is done) — Schätzung

## Range

Review of `ae3acace0`..`c3c6ae7bf958d712b77656e60a6ee9e9c33efe2a` (then this commit).

## Commits

### `53aea0e0b75b2798236a8036c7282b2e30e10d4a` F055 R8 C1: book round 7, R-1320 read again, DECISION F055 D4
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f055-r8.md` | +151/-0 | NEW: byte copy of `block.md` |
| `.agent/decisions.md` | +12/-0 | byte copy of `dry-decisions.md` (DECISION F055 D4) |
| `.agent/live_review.md` | +4/-0 | byte copy of `dry-live_review.md` (books round 7's verdict, re-reads R-1320) |
| `.agent/plan.md` | +7/-7 | byte copy of `dry-plan.md` |

### `c13b99e155cbc50ae468302e4273d32b86a80e10` F055 R8 C2: a runtime-flow check whose own application died never passes (R-1320)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/dod_runners.py` | +9/-0 | byte copy of `dry-dod_runners.py`: two checks of the process the check itself started |
| `tests/orchestration/test_dod_runners.py` | +79/-0 | two new deterministic tests in `TestRuntimeFlowRunner`, proven red at `ae3acace0`, green here |

### `c3c6ae7bf958d712b77656e60a6ee9e9c33efe2a` F055 R8 C3: the closure's one full suite on the repaired tree
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f055-closure-suite.txt` | +18/-18 | rewritten with the new suite run on the repaired tree |

C3 is the closure's ACCEPTED HEAD: full sha `c3c6ae7bf958d712b77656e60a6ee9e9c33efe2a`.

### (this commit) F055 R8 C4: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | full rewrite with the suite, evidence and package readings |

## External actions

- Preconditions checked before any write: `git rev-parse HEAD` and
  `origin/feature/f055-rehearsal` both read `ae3acace01f60c2f1c12818f3c3e3a12c7239b6c`;
  `git status --porcelain` was empty; `.agent/STOP` absent. `git branch --show-current` read
  `feature/f055-rehearsal` immediately before every commit.
- Push after C3: `git push -u origin feature/f055-rehearsal` — exit 0 on the first attempt (no
  HTTP 500, no retry needed): `ae3acace0..c3c6ae7bf  feature/f055-rehearsal -> feature/f055-rehearsal`.
- A1, the evidence job: `git reflog -n 3 --date=iso` recorded (quoted in Verification below), then
  `launch_evidence.py` started the evidence script detached (`python3
  .agent/authored/f055-r5-create_f055_evidence.py .remedy-wt/f055-r8-evidence`, cwd
  `/home/decodeux/Repos/remedy`), and `wait.py evidence <log dir> 50` was run, and ONLY that,
  while it ran — no other command touched the repo for the full ~20-minute run. Result: **exit
  0**, a clean bundle, package readiness confirmed next by A2.
- A2, the review package: a Python wrapper ran
  `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f055-r8-evidence` with `cwd` pinned
  to `/home/decodeux/Repos/remedy`, `REMEDY_REVIEW_DIR` unset, output captured to
  `.remedy-wt/f055-r8-worker/zip.log`. Result: exit 0, `PACKAGE_STATUS=READY_FOR_REVIEW`.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` was not run this round
  (no PR work ordered); the Next section below still names the Open PR Gate as a precondition of
  the next session.
- No `gh pr create/merge/edit`, no STATUS/README edit, no ledger rotation, no queue edit, no
  self-use run, no other provider call, no staging reclaim (not ordered by this block).
- Push after C4 follows this commit; its outcome is reported in the session's final reply, since
  it does not exist yet when this file is written.

## Verification

**Digests verified before anything else**, each with a Python sha256 reader (run as
`python3 -I <absolute path>`): `block.md` 151 lines /
`69675b935e09d85ef0c88de1210f05cdaf728eadc7aebaf9ae14d45d2783705f` — matched. All ten other
prepared files' sha256 (`dry-live_review.md`, `dry-decisions.md`, `dry-plan.md`,
`dry-dod_runners.py`, `launch_suite.py`, `launch_evidence.py`, `wait.py`, `load_record.py`,
`lastfailed.py`, `verify.py`) matched the digests given in the prompt — all `OK`.

**C2's two new tests, proven red/green before committing** (the one test-file run the block
permits "while you write it"): with the prepared `dry-dod_runners.py` in place, both
`test_an_app_already_exited_when_port_ownership_is_checked_does_not_pass` and
`test_an_app_that_exits_during_the_steps_does_not_pass` pass (`2 passed`). The repaired file was
then temporarily swapped for a copy of `ae3acace0`'s own `dod_runners.py` (never committed, never
part of any diff) and the same two tests were re-run: both fail
(`assert 'passed' == 'failed'`, i.e. the check wrongly reported `STATUS_PASSED`) — confirming
red at the base commit. The prepared file was copied back immediately afterward (byte-equality
re-checked, `True`) before any commit. The whole file, `tests/orchestration/test_dod_runners.py`,
was then run once more: `60 passed`.

**Gate 2** — `python3 -m ruff check packages/orchestration/dod_runners.py
tests/orchestration/test_dod_runners.py` (after C2): `All checks passed!`

**Gate 1** — `git status --porcelain` empty, then
`python3 /home/decodeux/Repos/remedy/.remedy-wt/f055-r8/prep/verify.py /home/decodeux/Repos/remedy c3c6ae7bf958d712b77656e60a6ee9e9c33efe2a`:
```
True C1's single parent is ae3acace0
True C1 has a single parent
True C1's subject begins 'F055 R8 C1:'
True C2 has a single parent
True C2's subject begins 'F055 R8 C2:'
True C3 has a single parent
True C3's subject begins 'F055 R8 C3:'
True C1 .agent/authored/f055-r8.md equals block.md
True C1 .agent/live_review.md equals dry-live_review.md
True C1 .agent/decisions.md equals dry-decisions.md
True C1 .agent/plan.md equals dry-plan.md
True C1 names exactly its paths []
True C2 names exactly its paths []
True C2's dod_runners.py equals dry-dod_runners.py
True C3 names only the transcript ['.agent/authored/f055-closure-suite.txt']
True fork..C3 ancestry 33 plain 33, both 33
True at most one commit after C3 (0)
ALL True
```
One run, green.

## Closure suite

Reflog before the run: `c13b99e15 HEAD@{2026-10-14 19:32:21 +0200}: commit: F055 R8 C2: a
runtime-flow check whose own application died never passes (R-1320)`. The reflog line read
identically after the run (reported in the transcript's own "reflog after" line below), so the
tree did not move during the run.

The new `.agent/authored/f055-closure-suite.txt`, quoted whole:
```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 353.1s (the launcher's reading); pytest's own reported wall time: 352.31s (0:05:52)
summary line: 23069 passed, 22 skipped, 1 warning in 352.31s (0:05:52)
bad node ids (failed + errors):
  NONE
leftover processes: NONE
tree it ran on: c13b99e15 (F055 R8 C2: a runtime-flow check whose own application died never passes (R-1320))
tree note: the run the operator amendment amend0921-operator-feedback rule 1 orders on the repaired tree; it replaces the run on 71305a2c7
reflog before: c13b99e15 HEAD@{2026-10-14 19:32:21 +0200}: commit: F055 R8 C2: a runtime-flow check whose own application died never passes (R-1320)
reflog after: c13b99e15 HEAD@{2026-10-14 19:32:21 +0200}: commit: F055 R8 C2: a runtime-flow check whose own application died never passes (R-1320)
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F055 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1279.63 CPU seconds, 352.32 wall seconds, 23091 tests collected, exit status 0, recorded 2026-10-14T17:38:33Z
This closure's suite used 1279.63 CPU seconds, 9.4 percent more than F308's 1170.14, within the 14.1 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 14.1 percent.
The test modules whose CPU time rose most since F308's closure run:
  +11.67 s  tests/runtimes/test_supervisor_portability.py (35.60 -> 47.27)
  +7.46 s  tests/orchestration/test_review_zip_hygiene.py (31.38 -> 38.84)
  +7.11 s  tests/ui_server/test_multi_project_live.py (14.81 -> 21.92)
  +5.29 s  tests/cli/test_rehearsal.py (0.00 -> 5.29)
  +4.85 s  tests/orchestration/test_subtree_rerun_prepare.py (10.27 -> 15.12)
  +4.31 s  tests/orchestration/test_self_use_runner.py (3.59 -> 7.90)
  +4.12 s  tests/orchestration/test_review_package_full_integration.py (3.39 -> 7.51)
  +3.88 s  tests/orchestration/test_job_worktree_integration.py (6.64 -> 10.52)
  +3.77 s  tests/orchestration/test_run_manifest.py (4.47 -> 8.24)
  +2.93 s  tests/cli/test_serve_client_parity.py (6.55 -> 9.48)
```
Suite GREEN (exit 0, no bad node ids), within the cost ceiling (exit 0 on the cost script, 9.4
percent against a 14.1 percent limit) — so A1 and A2 proceeded.

**A1, the evidence job** — `wait.py`'s whole printed output, verbatim:
```
head c3c6ae7bf958d712b77656e60a6ee9e9c33efe2a
ancestry-path count 33
plain count 33
collected node ids 8339, deselected 169
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 8330, 'failed': 0, 'skipped': 9}, output_hash aa866e0d30c0a69915880a9dc05a0ba8fdfcd74520de7af565f7574b86f24e5c
validate_verification_tests problems [] passed 8330
is_valid_current_run True
validation_errors []
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
{
  "job_id": "f055r5e1001",
  "head_commit": "c3c6ae7bf958d712b77656e60a6ee9e9c33efe2a",
  "authority_count": 26,
  "partition": {
    "T001": 9,
    "T002": 9,
    "T003": 8
  },
  "commit_count": 33,
  "verdict": "PASS_WITH_RISKS",
  "manual_completion": true,
  "operator_attested_tasks": [
    "T001",
    "T002",
    "T003"
  ],
  "total_passed": 8330
}
exit 0 wall 1203.1
```
Every reading matches the block's expectation exactly: `head` equals C3's full sha; both counts
33; `collected node ids` 8339 (the precheck's 8337 plus C2's two new tests) with `deselected`
169; red control 0 with the planted id answering "a local absolute path"; pytest exit 0 with
`failed` 0; `validate_verification_tests problems []`; `is_valid_current_run True`;
`validation_errors []`; exit 0. Evidence job id (from the script's own summary line, quoted
above): `f055r5e1001`.

**A2, the review package** — the wrapper's captured `zip.log`, decisive lines:
```
{"member_count": 8412, "authoritative_count": 26, "symlink_count": 0, "tombstone_count": 0, "final_path": "/home/decodeux/Repos/remedy-history/zips/remedy-review-20261014-200011-READY_FOR_REVIEW.zip", "final_sha256": "7be134c461b533e26dab8ca02d1f28de90a750c6a18197a9fd549f87529611aa", "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW", "evidence_authoritative": true, "review_subject_alignment": "PASS", "manifest_sha256": "01d8670c6f1e61c6a9e8d8d793928f3936df5761ff2c61e5cab0eb2b5fe5ee1d"}
REVIEW_PACKAGE_CREATED=true
PACKAGE_STATUS=READY_FOR_REVIEW
REVIEW_SUBJECT_ALIGNMENT=PASS
EVIDENCE_AUTHORITATIVE=true
REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20261014-200011-READY_FOR_REVIEW.zip
```
Package: `remedy-review-20261014-200011-READY_FOR_REVIEW.zip`, SHA-256 (independently recomputed
with a Python sha256 reader over the file on disk, matching the tool's own `final_sha256`):
`7be134c461b533e26dab8ca02d1f28de90a750c6a18197a9fd549f87529611aa`. Directory (the absolute path
the package ended up in): `/home/decodeux/Repos/remedy-history/zips`. `committed_review_subject`
read from `.review_zip_manifest.json` inside the zip: base `eea4f5cfe51c434eb2ab2bb0fb0246069cfa7bca`,
head `c3c6ae7bf958d712b77656e60a6ee9e9c33efe2a` (= C3's full sha, the accepted HEAD) — both match
the block's expectation exactly. `zipfile.is_zipfile(path)` → `True`; `ZipFile.testzip()` → `None`.

**Gate 6** — after A2, before C4: `python3 -m apps.cli.main integrity check --json`:
```
{"check_count": 6, "checks": [{"message": "handlers=188", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
`fail_count` 0. Open ids, via `scripts.rotate_live_review.open_finding_ids` over
`.agent/live_review.md` (41 ids, in order): `R-1246`, `R-1276` to `R-1313`, `R-1319`, `R-1320` —
exactly the set the block names. `git status --porcelain` empty.

## Authored-text proofs

`.agent/authored/f055-r8.md` against `block.md`: byte-identical, sha256
`69675b935e09d85ef0c88de1210f05cdaf728eadc7aebaf9ae14d45d2783705f`, confirmed by my own copy
script at write time and again independently by `verify.py`'s Gate 1 check. `.agent/live_review.md`
against `dry-live_review.md`, `.agent/decisions.md` against `dry-decisions.md`, and `.agent/plan.md`
against `dry-plan.md` (all C1): each confirmed byte-equal by a Python equality check at copy time
and again by Gate 1's per-path check. `packages/orchestration/dod_runners.py` against
`dry-dod_runners.py` (C2): confirmed byte-equal at copy time and again by Gate 1's
`C2's dod_runners.py equals dry-dod_runners.py` check. No other reviewer-authored text was
applied this round (the test file's two new tests and the handback are worker-authored, not
reviewer-authored pastes).

## Deviations & assumptions

None. Every step ran exactly as the block ordered: the digest checks all matched; C1, C2 and C3
landed in the ordered sequence with Gate 1 and Gate 2 both green; the suite ran once, green,
within the cost ceiling; the reflog did not move during the suite run; A1's evidence job exited 0
with a clean bundle on the first and only attempt; A2's package read `READY_FOR_REVIEW` on the
first and only attempt; Gate 6 read `fail_count` 0 with exactly the 41 open ids the block names.
R-1320's repair is recorded in the item-status table below, not as a `Landed:` or `Done:` line.

## For the operator, in plain sentences

A check Remedy runs on an application — starting it, waiting for it to answer, then running a
small flow of requests against it — could, in a race, pass on a DIFFERENT application that
happened to be listening on the same network port while the check's own application had already
died. That is now repaired and proven with two new deterministic tests: the check now fails,
with a clear reason, whenever its own application was already dead when ownership of the port
was checked, or died partway through the check's steps. The whole test collection (over 23,000
tests) ran again on the repaired code, once, and it passed cleanly with nothing broken and no
leftover processes. The review package was built successfully and is ready for review; its
location is recorded above. Nothing waits for you right now.

## Next

1. Phase 1 rule 1: `.agent/STOP` — absent at this handoff.
2. Rule 2, the Open PR Gate: no pull request is open for this branch yet.
3. The reviewer reviews round 8 and books its verdict in the next round's first commit.
4. The closing round: the Built State, the resolutions of R-1320 and the earlier fixes, the
   rotation, SU-064's `consumed_by`, the STATUS flip with the README sync, and the pull request,
   left unmerged.

Operator questions open: 0.
Open findings: 41 (R-1320 owned by F055; R-1246, R-1276 to R-1313 and R-1319 by F307).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | Gate 1's checks `True`; books round 7 and R-1320's re-reading, DECISION F055 D4 |
| C2 | done | the repair plus its two deterministic tests, red at `ae3acace0`, green here; ruff clean |
| C3 | done | the one full suite, green, exit 0; full sha `c3c6ae7bf958d712b77656e60a6ee9e9c33efe2a` is the accepted head |
| A1 | done | evidence job exit 0, clean bundle, `job_id f055r5e1001` |
| A2 | done | review package `READY_FOR_REVIEW`, base/head match, zip valid |
| C4 | done | this commit |
| R-1320 | done | repaired by C2, proven by its two new tests and the green full suite in C3 |
| Gate 1 | done | `ALL True`, one run |
| Gate 2 | done | `All checks passed!` |
| Gate 3 (C3 suite) | done | exit 0, `23069 passed, 22 skipped`, no bad node ids |
| Gate 4 (A1) | done | every reading matched the block's expectation exactly |
| Gate 5 (A2) | done | `PACKAGE_STATUS=READY_FOR_REVIEW`, base/head match, zip valid |
| Gate 6 | done | `fail_count` 0, 41 open ids exactly as required, `git status --porcelain` empty |
