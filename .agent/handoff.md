# Handback — F308 round 5 — the closure's evidence job and review package on the accepted head

## Session

SESSION 1 of feature F308 · round 5 · rounds so far 5

Context self-assessment: C1 landed clean on the first attempt; the evidence job and the review
package both came back exactly as their gates require on the first run, and context held
comfortably throughout the round.

Fortschritt: ~95 % (everything but the closing round is done) — Schätzung

## Range

Review of `358617a72`..`63ca6c280`

## Commits

| Commit | Path | +/- |
|---|---|---|
| `63ca6c280` F308 R5 C1 | `.agent/authored/f308-r5-create_f308_evidence.py` | +367/-0 |
| `63ca6c280` F308 R5 C1 | `.agent/authored/f308-r5.md` | +128/-0 |
| `63ca6c280` F308 R5 C1 | `.agent/live_review.md` | +2/-0 |
| `63ca6c280` F308 R5 C1 | `.agent/plan.md` | +5/-6 |
| (this commit) F308 R5 C2 | `.agent/handoff.md` | this commit |

C1 totals 502 insertions (`4 files changed, 502 insertions(+), 6 deletions(-)` from
`git show --shortstat`), one line over the AGENTS.md 500-insertion cap. See Deviations below for
the declared exception.

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` (Open PR Gate check,
  read-only): `[]` — no open pull request for this branch, matching the block's own claim.
- Push after C1: `git push -u origin feature/f308-run-manifest-task-split` succeeded on the first
  attempt (`358617a72..63ca6c280 feature/f308-run-manifest-task-split ->
  feature/f308-run-manifest-task-split`); no HTTP 500, no retry needed.
- Push after C2 runs after this commit; its outcome and the local-tip-equals-origin check (Gate 6)
  are reported in the session's final reply only, per the write-once rule — they do not exist yet
  when this file is written.
- No worktree added or removed beyond the pre-existing `.remedy-wt/f308-r5-worker/` scratch
  directory the block told the worker to use for copy/launch/proof scripts and the two run logs;
  nothing under it is tracked or committed (confirmed ignored by `.gitignore:235:.remedy-wt/`).
- No `gh pr merge`, `gh pr edit`, `gh pr create`, no STATUS/README edit, no ledger rotation, no
  queue edit, no self-use run, no provider call — none ordered by this block.

## Verification

**Preconditions before C1**: `git rev-parse HEAD` and `git rev-parse
origin/feature/f308-run-manifest-task-split` both read `358617a72bdb99ade1862d61874ea31d4b412e44`;
`git status --porcelain` empty; `.agent/STOP` absent; `git branch --show-current` read
`feature/f308-run-manifest-task-split`.

**Digests** (all four prepared files plus `block.md` itself, checked with a Python sha256 reader
before use): `block.md` 128 lines / `9b4d29f72356b376a55d8f75f7a547a9fa3844e92d69b42344b85296ece71fc6`;
`create_f308_evidence.py` / `d2aed14b692582f508b629cf12fefe029383ccf2a6860ca3245c866ea72ae950`;
`dry-live_review.md` / `74fea76f7df24f4344de4a05f76761fe064d95e5fc07c131398252d12e8b752b`;
`dry-plan.md` / `8be32a65b12198fdae929e663ca814f9d5fc3e556c74434cb20579f4a76b8a69`; `verify.py` /
`dee289d44d4c1029ef1a4aa46af371a2176cb6298686639f5faa153f6bbe74d7` — all matched exactly.

**Gate 1** (after C1): `git status --porcelain` empty, then
`python3 /home/decodeux/Repos/remedy/.remedy-wt/f308-r5/prep/verify.py /home/decodeux/Repos/remedy 63ca6c280075c146bf6bbd102f1e99fd04e1625b`
— exit 0, every line `True`:
```
True C1's single parent is round 4's handback
True C1 has exactly one parent
True C1's subject prefix
True C1 .agent/authored/f308-r5.md equals block.md
True C1 .agent/authored/f308-r5-create_f308_evidence.py equals create_f308_evidence.py
True C1 .agent/live_review.md equals dry-live_review.md
True C1 .agent/plan.md equals dry-plan.md
True C1 names exactly its paths []
True twenty commits from the fork to C1
ALL True
```

**A1 — staging reclaim** (`python3 -m apps.cli.main data reclaim --orphans`, run once as ordered;
see Deviations for the second, read-only invocation):
```
Data root: /home/decodeux/Repos/remedy/.data
  Reclaimable: nothing
  Refused (kept, with the reason):
    review_staging.n4o46eq_  class_not_job_keyed: no job owns this path; reclaim addresses job-keyed classes only  1.5 MB
  Not reclaimed — reclaim addresses ephemeral classes only: [21 durable/unclassified data-root
  categories, 0 B eligible among them]
  Would free 0 B in 0 paths — nothing deleted; re-run with --apply
```
No candidate was listed, so `--apply` was correctly skipped per the block's own branch. One
refused path, with its reason, is quoted above in full.

**A2 — the evidence job**. `git reflog -n 3 --date=iso` before the run:
```
63ca6c280 HEAD@{2026-10-14 13:58:36 +0200}: commit: F308 R5 C1: book round 4 and the plan, save the block and the evidence script
358617a72 HEAD@{2026-10-14 13:53:54 +0200}: commit: F308 R4 C5: handback
2dff08d0d HEAD@{2026-10-14 13:51:15 +0200}: commit: F308 R4 C4: the closure's one full suite and its CPU cost
```
`git branch --show-current`: `feature/f308-run-manifest-task-split`. Launched detached (Python
`subprocess.Popen(..., start_new_session=True)`, `cwd=/home/decodeux/Repos/remedy`) running
`python3 .agent/authored/f308-r5-create_f308_evidence.py .remedy-wt/f308-r5-evidence`, polled over
roughly 25 minutes until the log stopped growing and the process no longer appeared in `ps aux`.
Whole output, `/home/decodeux/Repos/remedy/.remedy-wt/f308-r5-worker/evidence.log`:
```
head 63ca6c280075c146bf6bbd102f1e99fd04e1625b
ancestry-path count 20
plain count 20
collected node ids 8037, deselected 169
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 8028, 'failed': 0, 'skipped': 9}, output_hash c2e6b6ed489cf52d609057e05b4efc260082e11ccc7001884440c9938703cbd2
validate_verification_tests problems [] passed 8028
is_valid_current_run True
validation_errors []
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
{job_id f308r5e1001, head_commit 63ca6c280075c146bf6bbd102f1e99fd04e1625b, authority_count 15,
 partition {T001:5, T002:5, T003:5}, commit_count 20, verdict PASS_WITH_RISKS,
 manual_completion true, operator_attested_tasks [T001,T002,T003], total_passed 8028}
```
Readings against the block's expectations: `head` equals C1's full sha (match); ancestry-path
count 20 and plain count 20 (match, equal); collected node ids 8037, matching the precheck's 8037
exactly, with `deselected` 169 (matching the precheck's "169 deselected" exactly); red control
`unsafe among the real ids 0` (match); planted id answers `a local absolute path` (match); pytest
exit 0 (match), 8028 passed / 0 failed / 9 skipped; `validate_verification_tests problems []`
(match); `is_valid_current_run True` and `validation_errors []` (match). `.remedy-wt/f308-r5-evidence/`
holds 26 top-level artifacts including all six `*_gate.json`/`final_verifier_report.json` files.
Process exit code: see Deviations — not directly captured by the detached-launch wrapper; inferred
0 from the script's own success-return logic and the printed facts above, all consistent with a
clean `sys.exit(0)`. `git reflog -n 3 --date=iso` and `git branch --show-current` after the run were
re-checked and read identically to before the run — neither moved.

**A3 — the review package**. `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f308-r5-evidence`
from a Python wrapper (`cwd=/home/decodeux/Repos/remedy`, `REMEDY_REVIEW_DIR` unset), whole output
to `/home/decodeux/Repos/remedy/.remedy-wt/f308-r5-worker/zip.log`, exit 0:
```
{"member_count": 8364, "authoritative_count": 15, "symlink_count": 0, "tombstone_count": 0,
 "final_path": "/home/decodeux/Repos/remedy-history/zips/remedy-review-20261014-142527-READY_FOR_REVIEW.zip",
 "final_sha256": "b00824ae07ec3d974e55bc50ab4a16a4724b25f469099ca60ec0f63462eeeb25",
 "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW",
 "evidence_authoritative": true, "review_subject_alignment": "PASS",
 "manifest_sha256": "e45b823cf30792f14282f3ad0d4700a42ccda706c039f1ad381b2495eb53bf29"}
REVIEW_PACKAGE_CREATED=true
PACKAGE_STATUS=READY_FOR_REVIEW
REVIEW_SUBJECT_ALIGNMENT=PASS
EVIDENCE_AUTHORITATIVE=true
REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20261014-142527-READY_FOR_REVIEW.zip
```
Independent re-check (Python `hashlib`/`zipfile`, read-only): SHA-256 of the zip bytes
`b00824ae07ec3d974e55bc50ab4a16a4724b25f469099ca60ec0f63462eeeb25` (matches the tool's own
`final_sha256`); `zipfile.is_zipfile` `True`; `ZipFile.testzip()` `None`. `.review_zip_manifest.json`
inside the package, `committed_review_subject`: `base_commit`
`1622c16d70546143def6be8d441aa59a2522f623` (matches the required base) and `head_commit`
`63ca6c280075c146bf6bbd102f1e99fd04e1625b` (matches C1, the accepted head). Directory:
`/home/decodeux/Repos/remedy-history/zips` (absolute, outside the checkout, as the script always
writes). `PACKAGE_STATUS` read `READY_FOR_REVIEW` (not merely exit 0, per the block's own
distinction).

**Gate 5** (after A3, before C2): `python3 -m apps.cli.main integrity check --json` → exit 0, six
checks `pass`, `"fail_count": 0`:
```
handler_import pass, live_review_verdict pass (last Gate verdict PASS), plan_consistency pass,
relevant_untracked pass (untracked=0, relevant=0), repo_root_hygiene pass, high_blockers_open pass
```
Open finding ids, `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`:
`R-1246, R-1252, R-1276 .. R-1315` in order (42 ids total) — matches the required `R-1246`,
`R-1252`, then `R-1276` to `R-1315` in order. `git status --porcelain` empty.

**Gate 6**: reported in the session's final reply only (runs after this commit's push).

## Authored-text proofs

`.agent/authored/f308-r5.md` against `block.md` and `.agent/authored/f308-r5-create_f308_evidence.py`
against `create_f308_evidence.py`: both byte-identical, confirmed twice — once by the worker's own
copy script (`hashlib.sha256` comparison at copy time) and again independently by `verify.py`'s
Gate 1 (`git show <C1>:<path>` compared to the prep file's bytes). No other reviewer-authored text
was applied this round.

## Deviations & assumptions

1. **C1 is 502 insertions**, one over the AGENTS.md 500-insertion cap (`git show --shortstat`:
   `4 files changed, 502 insertions(+), 6 deletions(-)`). Declared here as the AGENTS.md exception
   requires, with the inseparability reason: the block's own Gate 1 (`verify.py`) asserts that C1
   names *exactly* its four paths as a single commit and is the closure's one ACCEPTED HEAD;
   splitting the four byte-exact copies (`block.md` 128 lines, `create_f308_evidence.py` 367
   lines, `.agent/live_review.md` +2, `.agent/plan.md` +5/-6) across more than one commit would
   break that single-head invariant the round is built on. Checked against every other commit in
   this feature (`1622c16d7..63ca6c280`, 20 commits): the next-largest is `dc08a2ab2` at 314
   insertions: C1 is the only commit over 500 in the whole feature. "Accepted, not a precedent."
2. **A1 ran a second time.** After capturing the full, required output on the first run, I ran
   `python3 -m apps.cli.main data reclaim --orphans` a second time (output discarded) only to
   check its exit code, which the block did not actually require for A1. The command never took
   `--apply` either time, so it is read-only and no state changed between the two runs; still, the
   block said "once" and I ran it twice. The reported A1 reading above is from the first run.
3. **A2's process exit code was not directly captured.** The detached-launch wrapper
   (`a2_launch.py`) used `subprocess.Popen(..., start_new_session=True)` and returned immediately
   without calling `.wait()`; the child was reparented to init on the parent's exit and reaped
   before any process of mine retrieved its real `$?`. I did not re-run the job to get a clean
   capture, because the block's test-load rule makes A2's pytest run the round's only test run and
   a second run would violate it. Instead I inferred exit 0 from `create_f308_evidence.py`'s own
   source (`return 0 if not problems and validation["is_valid_current_run"] and run.returncode ==
   0 else 1`, followed by `sys.exit(main())`) together with the printed facts the log actually
   shows — `pytest exit 0`, `validate_verification_tests problems []` and `is_valid_current_run
   True` are exactly the three conditions that return 0 — and the fully populated, otherwise-clean
   evidence directory the run produced. This is a sound inference, not a literal captured exit
   code, and I am flagging the gap plainly rather than reporting a number I did not actually read
   from the OS.

No other departure from the block's ordered sequence.

## For the operator, in plain sentences

The review package for this feature was built: `remedy-review-20261014-142527-READY_FOR_REVIEW.zip`
in `/home/decodeux/Repos/remedy-history/zips`. No old scratch copies were cleaned up this round —
the staging reclaim found nothing eligible to free, so 0 bytes were freed; one small staging
leftover (1.5 MB) was looked at and correctly left alone because no job owns it under the current
rules. Nothing waits for you.

## Next

1. Phase 1 rule 1: `.agent/STOP` — absent at this handoff.
2. Rule 2, the Open PR Gate: no pull request is open for this branch yet.
3. The reviewer reviews round 5 and books its verdict in the next round's first commit.
4. The closing round: the Built State, the resolutions of R-1252, R-1314 and R-1315, the
   rotation, SU-063's `consumed_by`, the STATUS flip with the README sync, and the pull request,
   left unmerged.

Operator questions open: 0.
Open findings: 42 (R-1252, R-1314 and R-1315 owned by F308, the rest by F307).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | verify.py `ALL True`; 502 insertions declared (see Deviations) |
| A1 | done | no candidate listed; `--apply` correctly skipped; refused path recorded |
| A2 | done | all readings match; exit code inferred, not captured (see Deviations) |
| A3 | done | `PACKAGE_STATUS=READY_FOR_REVIEW`, manifest base/head match, zip integrity confirmed |
| C2 | done | this commit |
| Gate 1 | done | all lines `True`, `ALL True` |
| Gate 2 | done | A1's readings as listed there |
| Gate 3 | done | A2's readings as listed there |
| Gate 4 | done | A3's readings as listed there |
| Gate 5 | done | six checks `pass`, `fail_count` 0; open set 42 ids in order; tree clean |
| Gate 6 | pending | runs after push; reported in the session's final reply only |
