# Handback — F306 round 11: book round 10, the closure's evidence job and review package on the accepted head

## Session

SESSION 3 of feature F306 · round 11 · rounds so far 11

Context self-assessment: one records commit, three non-recording actions (the staging reclaim,
the evidence job, the review package) and the handback all read exactly as the block ordered, with
no `.agent/STOP`, no open pull request and no reflog or branch movement encountered; context held
comfortably throughout.

Fortschritt: ~97 % (everything but the closing round is done) — Schätzung

## Range

Review of `8911b1c1a`..`87d132b1d`

## Commits

### 87d132b1d F306 R11 C1: book round 10, bring the review-folder question up to date, the plan, save the block and the evidence script

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f306-r11.md` | +133/-0 | NEW FILE, byte copy of `block.md` (133 lines, sha256 `d7a6f047183c557404b6c1c46d1368cd8067bdecef7830c4b8d4ec20e351fb07`) |
| `.agent/authored/f306-r11-create_f306_evidence.py` | +244/-0 | NEW FILE, byte copy of `create_f306_evidence.py` |
| `.agent/live_review.md` | +2/-0 | round 10's PASS verdict appended, byte-identical to `append-live_review.txt` |
| `.agent/plan.md` | +4/-8 | replaced by `dry-plan.md` |
| `.agent/operator_questions.md` | +15/-10 | replaced by `operator_questions.md` (Q18 updated to say where the two folders are) |

### (this commit) F306 R11 C2: handback with the evidence and package readings

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | full rewrite per `docs/agents/handback_template.md` |

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`: confirmed no open
  pull request for this branch, before and after this round's work.
- Push after C1: `git -C /home/decodeux/Repos/remedy push -u origin feature/f306-findings-paydown-v8`
  — exit 0 on the first attempt (no HTTP 500, no retry needed):
  `8911b1c1a..87d132b1d  feature/f306-findings-paydown-v8 -> feature/f306-findings-paydown-v8`.
- No worktree added or removed. No `gh pr merge`, `gh pr edit` or `gh pr create`. No STATUS, README,
  ledger, queue or self-use action — none ordered for this round.
- Push after C2: `git -C /home/decodeux/Repos/remedy push origin feature/f306-findings-paydown-v8` —
  result and Gate 6's comparison are in the session's final reply, not in this file (the push had
  not yet happened when this file was written, per the write-once rule).

## Verification

Preconditions confirmed before C1: `git rev-parse HEAD` read
`8911b1c1ae2a14e9bc5d954b601c88152afbb5f6`, equal to
`git rev-parse origin/feature/f306-findings-paydown-v8`; `git status --porcelain` was empty;
`.agent/STOP` was absent; `git branch --show-current` read `feature/f306-findings-paydown-v8`.

Every prepared-file digest matched before use (all six files named in the prompt, each checked by a
Python sha256 reader before any read of its content for use): `block.md`
(`d7a6f047183c557404b6c1c46d1368cd8067bdecef7830c4b8d4ec20e351fb07`), `append-live_review.txt`,
`create_f306_evidence.py`, `dry-plan.md`, `operator_questions.md`, `verify.py` — all six `OK`.

`git branch --show-current` read `feature/f306-findings-paydown-v8` immediately before C1's commit
and again immediately before this handback commit, as ordered.

C1: a Python script under `.remedy-wt/f306-r11-worker/c1_prepare.py` wrote the five files by byte
copy/concatenation, then `git status --porcelain` before the commit showed exactly the five named
paths (two new, three modified) and nothing else. The saved block copy reads 133 lines, sha256
`d7a6f047183c557404b6c1c46d1368cd8067bdecef7830c4b8d4ec20e351fb07` — matching the digest given in
the task verbatim.

Gate 1: `git status --porcelain` → empty. Then `verify.py` →
```
C1 subject True
C1 parent is the base True
equal at C1 True .agent/live_review.md
equal at C1 True .agent/plan.md
equal at C1 True .agent/operator_questions.md
equal at C1 True .agent/authored/f306-r11.md
equal at C1 True .agent/authored/f306-r11-create_f306_evidence.py
C1 names exactly its paths True []
ALL True
```

Gate 2 (A1 — the staging reclaim preview): `python3 -m apps.cli.main data reclaim --orphans` → exit
0:
```
Data root: /home/decodeux/Repos/remedy/.data
  Reclaimable: nothing
  Refused (kept, with the reason):
    review_staging.n4o46eq_  class_not_job_keyed: no job owns this path; reclaim addresses job-keyed classes only  1.5 MB
  Not reclaimed — reclaim addresses ephemeral classes only:
    api (durable)  2.1 MB
    control (durable)  2.1 KB
    evidence (unclassified)  4.1 MB
    evidence_exports (durable)  32.8 MB
    job_evidence_index (durable)  141.6 KB
    job_logs (durable)  17.1 MB
    job_promotions (unclassified)  237.7 KB
    jobs (durable)  160.7 MB
    memory (durable)  17.2 KB
    missions (durable)  106.8 KB
    pingpong_runs (unclassified)  165.5 MB
    projects (durable)  124.8 KB
    proposed_tasks (durable)  1.8 KB
    queue (unclassified)  364 B
    remedy-job-evidence-f013_job_intake_closure (unclassified)  338.1 KB
    roadmap (durable)  166.7 KB
    runs (durable)  140.4 MB
    serve (durable)  26.9 KB
    smoke (durable)  225 B
    task_jobs (unclassified)  44.9 MB
    ui (durable)  1.7 KB
    workspaces (durable)  37.7 MB
  Would free 0 B in 0 paths — nothing deleted; re-run with --apply
```
Reclaimable list is empty, so `--apply` was SKIPPED per the block; the one refused path is
`review_staging.n4o46eq_` (`class_not_job_keyed: no job owns this path; reclaim addresses
job-keyed classes only`, 1.5 MB).

Gate 3 (A2 — the evidence job): reflog before (`git reflog -n 3 --date=iso`) read
`87d132b1d HEAD@{2026-10-14 00:31:20 +0200}: commit: F306 R11 C1: book round 10, bring the
review-folder question up to date, the plan, save the block and the evidence script` at the top;
branch read `feature/f306-findings-paydown-v8`. Launched detached via
`.remedy-wt/f306-r11-worker/launch_evidence.py` (a Python wrapper, `cwd=/home/decodeux/Repos/remedy`,
`start_new_session=True`), polled by this session until the exit file appeared (about 17 minutes
wall). `.remedy-wt/f306-r11-worker/evidence.log`, quoted whole:
```
head 87d132b1d8d35cebcc24df9651043380b56441d2
ancestry-path count 38
plain count 38
collected node ids 4946, deselected 33
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 4939, 'failed': 0, 'skipped': 7}, output_hash 8c43babee15e554984e0c343bc3ead8b7d05098d26a425b2ff20920187814575
validate_verification_tests problems [] passed 4939
is_valid_current_run True
validation_errors []
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
{
  "job_id": "f306r11e1001",
  "head_commit": "87d132b1d8d35cebcc24df9651043380b56441d2",
  "authority_count": 27,
  "partition": {"T001": 9, "T002": 9, "T003": 9},
  "commit_count": 38,
  "verdict": "PASS_WITH_RISKS",
  "manual_completion": true,
  "operator_attested_tasks": ["T001", "T002", "T003"],
  "total_passed": 4939
}
```
Script exit code (from `evidence.exit`): `0`. Expected-vs-actual: head equals C1's full sha;
ancestry-path count and plain count both 38 (37 commits before C1 plus C1); collected node ids 4946
(below 4961), deselected 33 (above 18); red control `unsafe among the real ids 0`; planted id reads
"a local absolute path"; pytest exit 0 with 4939 passed, 0 failed, 7 skipped; `validate_verification_tests
problems []`; `is_valid_current_run True`; `validation_errors []`. Reflog and branch read again after
the run: identical to before (same top line, same branch) — neither moved. No evidence file was
edited by hand.

Gate 4 (A3 — the review package): `bash scripts/make_review_zip.sh --evidence-dir
.remedy-wt/f306-r11-evidence`, launched via `.remedy-wt/f306-r11-worker/launch_zip.py` (Python
wrapper, `cwd=/home/decodeux/Repos/remedy`, detached, `REMEDY_REVIEW_DIR` unset), from the clean,
pushed tree at C1. `.remedy-wt/f306-r11-worker/zip.log`, quoted whole:
```
UNCHANGED: runtime_integration_gate.json — rebuilt from source; identical to existing
Evidence refresh completed for staged copy.
Observability index generated from staged bytes: evidence/current/self_run_observability_index.json
{"member_count": 8355, "authoritative_count": 27, "symlink_count": 0, "tombstone_count": 0, "final_path": "/home/decodeux/Repos/remedy-history/zips/remedy-review-20261014-005334-READY_FOR_REVIEW.zip", "final_sha256": "bfeb7cd3e0c6771d65f60195d1e6b495a034bd5333e56b35059c0244d5943608", "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW", "evidence_authoritative": true, "review_subject_alignment": "PASS", "manifest_sha256": "513a59b3ec701042345baca04b3ac8acf147bb14c9aea083393445769d1b78c5"}

============================================
REVIEW_PACKAGE_CREATED=true
PACKAGE_STATUS=READY_FOR_REVIEW
PACKAGING_CWD=/home/decodeux/Repos/remedy
EVIDENCE_DIR=.remedy-wt/f306-r11-evidence
REVIEW_SUBJECT_ALIGNMENT=PASS
EVIDENCE_AUTHORITATIVE=true
REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20261014-005334-READY_FOR_REVIEW.zip
============================================

ZIP CREATED AND READY FOR FINAL REVIEW

38M	/home/decodeux/Repos/remedy-history/zips/remedy-review-20261014-005334-READY_FOR_REVIEW.zip
Included files: 8355
Branch: feature/f306-findings-paydown-v8
Commit: 87d132b1d8d35cebcc24df9651043380b56441d2
Evidence: evidence/current/
```
Script exit code (from `zip.exit`): `0`. `PACKAGE_STATUS=READY_FOR_REVIEW`,
`REVIEW_SUBJECT_ALIGNMENT=PASS`, `EVIDENCE_AUTHORITATIVE=true`. Independent check via
`.remedy-wt/f306-r11-worker/verify_zip.py` (recomputed sha256, `zipfile.is_zipfile`, `testzip()`,
and the manifest read INSIDE the package): `SHA-256
bfeb7cd3e0c6771d65f60195d1e6b495a034bd5333e56b35059c0244d5943608` (matches the build log's
`final_sha256`); `is_zipfile True`; `testzip() None`; `.review_zip_manifest.json`'s
`committed_review_subject` → `"base_commit": "f51232ee2fd1e2367d8fad5045aa7d1a0805a3d4"` (matches
the expected base), `"head_commit": "87d132b1d8d35cebcc24df9651043380b56441d2"` (equals C1's full
sha). Directory the package ended up in:
`/home/decodeux/Repos/remedy-history/zips`.

Gate 5: `python3 -m apps.cli.main integrity check --json` →
```
{"check_count": 6, "checks": [{"message": "handlers=188", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
exit 0; and
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
→ `['R-1235', 'R-1246', 'R-1252']` (exit 0, matches expectation); `git status --porcelain` → empty.

Gate 6: runs after this commit's push; its command, exit code and comparison are in the session's
final reply, not in this file (per the write-once rule).

## Authored-text proofs

- `.agent/authored/f306-r11.md` against `block.md`: byte-equal, 133 lines, sha256
  `d7a6f047183c557404b6c1c46d1368cd8067bdecef7830c4b8d4ec20e351fb07` (Gate 1's `names exactly its
  paths True []` plus C1's own write and `verify.py`'s equality print).
- `.agent/authored/f306-r11-create_f306_evidence.py` against `create_f306_evidence.py`: byte-equal
  (`verify.py`'s equality print).
- `.agent/live_review.md` against the base plus `append-live_review.txt`: byte-equal (`verify.py`'s
  equality print).
- `.agent/plan.md` against `dry-plan.md`: byte-equal (`verify.py`'s equality print).
- `.agent/operator_questions.md` against `operator_questions.md`: byte-equal (`verify.py`'s equality
  print).

## Deviations & assumptions

1. **A2 and A3's detached launch went through a one-line `bash -c` wrapper inside the Python
   launcher, not a bare `subprocess.Popen` of the pytest/zip command itself.** The block asks for "a
   Python wrapper with `cwd=...`, launched detached and polled", with the whole output written to a
   named log and the exit code captured. `launch_evidence.py` and `launch_zip.py` are Python
   scripts that set `cwd=REPO` and `start_new_session=True` on a `Popen` of `["bash", "-c",
   script]`, where `script` itself also `cd`s to the repo, runs the named command with `>` and `2>&1`
   into the named log file, and appends `echo $? > <exit file>` — the only way to persist a
   detached child's exit code past the point where the launching Python process itself returns.
   The named command, its cwd, its log path and its exit-code capture are exactly as ordered; the
   `bash -c` layer is the mechanism that makes the exit code survive the detach, not a substitution
   of a different command.
2. **No other deviation.** C1 ran exactly the five byte copies the block named, in the order given.
   A1 found no reclaim candidate and skipped `--apply`, as the block's own branching instruction
   says to. A2 and A3 ran once each, exactly as specified, and read every value the block predicted.
   Gates 1, 2, 3 and 5 ran exactly as named; Gate 4's zip-manifest keys are `base_commit`/
   `head_commit` rather than bare `base`/`head` as the block's prose shorthand put it — the values
   read are the ones the block names, under the package's own key names.

## For the operator, in plain sentences

The review package for this feature was built: a file named
`remedy-review-20261014-005334-READY_FOR_REVIEW.zip`, about 38 MB, sitting in the folder
`/home/decodeux/Repos/remedy-history/zips`. A check of unused scratch copies found nothing worth
clearing out this round — the one thing it flagged is a staging copy no job currently owns, which
the tool itself keeps rather than freeing, so no space was freed. The question about the two old
review folders now says where they are and that it is safe to leave them there or move them
yourself. Nothing new waits for you to decide.

## Next

1. Phase 1 rule 1: `.agent/STOP` — absent at this handoff.
2. Phase 1 rule 2: the Open PR Gate — no pull request is open for this branch yet.
3. The reviewer reviews round 11 and books its verdict in the next round's first commit.
4. The closing round: the Built State, R-1235's resolution, R-1246 and R-1252 re-assigned to the
   next paydown, the rotation, the next findings paydown registered, the self-use entry SU-062's
   `consumed_by`, the STATUS flip with the README sync, and the pull request, left unmerged.

Operator questions open: 1.
Open findings: 3 (R-1235, R-1246 and R-1252), all owned by F306.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| A1 | done | no reclaim candidate; `--apply` skipped per the block |
| A2 | done | exit 0; all predicted readings matched |
| A3 | done | `READY_FOR_REVIEW`, alignment `PASS`, authoritative `true` |
| C2 | done | this handback |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` `ALL True` |
| Gate 2 | done | reclaim preview read, empty candidate list, `--apply` skipped |
| Gate 3 | done | evidence job exit 0; every predicted reading matched |
| Gate 4 | done | package `READY_FOR_REVIEW`; manifest base/head match; `is_zipfile` True; `testzip()` None |
| Gate 5 | done | `fail_count` 0; open set `['R-1235', 'R-1246', 'R-1252']`; tree clean |
| Gate 6 | pending | runs after the push; reported in the session's final reply only |
