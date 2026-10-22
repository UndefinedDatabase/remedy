# Handback — F296 round 6: the closure's evidence round — book round 5 with R-1421, the evidence job and the review package

## Session

SESSION 1 of feature F296 · round 6 · rounds so far 6

Context self-assessment: this worker verified both prepared digests and every listed digest before any write, copied each named file by a script with a byte-for-byte proof, ran its self-review over each commit's staged diff before committing, ran the evidence job and the zip build each exactly once through the block's launch/wait scripts without ending its turn while either was alive, ran every gate once, and context stayed ample throughout.

Fortschritt: ~95 % (everything but the closing round is done) — Schätzung

## Range

Review of `a80252cde`..`HEAD` on `feature/f296-tier-escalation`.

## Commits

### 218933a46 F296 R6 C1: book round 5 and register R-1421, owned by F314, the plan, the block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f296-r6.md` | +118/-0 | NEW FILE, this round's block, byte copy, equal to `block.md` by line count (118) and sha256 (`138d8b8f...0dc8`) |
| `.agent/live_review.md` | +4/-0 | round 5's verdict booked and R-1421 registered (amend0827-process-diet rule 1) |
| `.agent/plan.md` | +5/-9 | rewritten for round 6's scope |
| `docs/roadmap/features/T2_F314.md` | +3/-0 | R-1421's Acceptance line added, owned by F314 per amend0911-feedback rule A |

### 0143b9e17 F296 R6 C2: the evidence script
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f296-r6-create_f296_evidence.py` | +292/-0 | NEW FILE, the reviewer-authored evidence script for this round, byte copy, run unedited in A2 |

### (this commit) F296 R6 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | C3: this handback (a handoff cannot table the commit that writes it) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 (preconditions) | done | branch `feature/f296-tier-escalation` at `a80252cde`, HEAD equal to `origin/feature/f296-tier-escalation`, `git status --porcelain` empty, `.agent/STOP` absent — all confirmed before any write |
| C1 | done | commit `218933a46`; all four paths byte-proved equal to their `c1-` source; `block.md` read 118 lines, sha256 `138d8b8f707ce5697596c91c6aaf942f45adbaf37af712aca58ef7fca3c30dc8`, matching the prompt's own digest |
| C2 | done | commit `0143b9e17`; byte-proved equal to its `c2-` source; pushed after the commit, first attempt succeeded (no HTTP 500) |
| A1 | done | preview read "Reclaimable: nothing", "Would free 0 B in 0 paths"; no candidate listed, so `--apply` was skipped per the block |
| A2 | done | job `f296r6e1001`; `launch.py`/`wait.py` each run once; exit 0 on the first `wait.py` call, wall 1594.5s |
| A3 | done | `launch.py`/`wait.py` each run once; exit 0 on the first `wait.py` call, wall 16.8s; `PACKAGE_STATUS=READY_FOR_REVIEW` |
| C3 | done | this commit, the handback |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` printed `True` on every check, `absent` for C3 (not yet committed when run), last line `ALL True` |
| Gate 2 | done | A2's and A3's readings both matched the block's expected shape exactly; exit codes 0 and 0 from the `.exit` files |
| Gate 3 | done | `integrity check --json` exit 0, `"fail_count": 0`; open-finding-id lookup printed the required seven ids |
| Push | done | reported below |

## External actions

No `gh pr list` call was made this round — the block's own Open PR Gate line states no pull request is open for this branch yet, and no PR step is asked of this round. `git push -u origin feature/f296-tier-escalation` ran once after C2 and succeeded on the first attempt (no HTTP 500, no retry needed); its result is reported below. A second push runs after this commit. No fetch, pull, merge, `gh pr create` or worktree add/remove. The scratch folder `.remedy-wt/f296-r6-worker/` holds the digest checker, the precondition checker, the copy-and-verify scripts, the A1/gate-3 wrapper scripts, and the commit-message files; the evidence job's own logs (`evidence.log`, `evidence.exit`) and the zip build's (`zip.log`, `zip.exit`) also live there, written by the block's own `launch.py`.

## Verification

1. Digests before any write: `block.md` (118 lines, sha256 `138d8b8f707ce5697596c91c6aaf942f45adbaf37af712aca58ef7fca3c30dc8`) and `digests.txt` (sha256 `6223df3cd445f24ffec98f868b2f5f2540a37063dd74853501caa4c43a99d0d7`) matched the two hashes given in the prompt; every one of the nine entries listed in `digests.txt` matched its sha256 (checked with a script, last line `ALL_OK: True`).
2. Preconditions: `git rev-parse --short=9 HEAD` read `a80252cde`, `git rev-parse HEAD` equalled `git rev-parse origin/feature/f296-tier-escalation` (`a80252cde7399ab25e52a4c392bf88669035fda8`), `git status --porcelain` printed nothing, `git branch --show-current` read `feature/f296-tier-escalation`, `.agent/STOP` did not exist — all before any write.
3. C1: all four named paths copied by a script, then compared byte-for-byte against the prepared source; `git status --porcelain` afterward showed exactly the four named paths (one new, three modified), matching the block's path list; `git branch --show-current` read `feature/f296-tier-escalation` immediately before the commit.
4. C2: the one named path copied the same way and byte-proved; `git status --porcelain` showed exactly that one new path; `git branch --show-current` read `feature/f296-tier-escalation` immediately before the commit. Pushed once, succeeded on the first attempt.
5. Gate 1: `git status --porcelain` printed nothing; `python3 .remedy-wt/f296-r6/prep/verify.py .` (run with `cwd=` set to the repository root) printed `True` on every check for C1 and C2, `absent` for C3 (not yet committed when the gate ran), and `ALL True` last.
6. A1: `python3 -m apps.cli.main data reclaim --orphans` (preview) exit 0: "Reclaimable: nothing", every other class listed "(durable)" with its size, "Would free 0 B in 0 paths — nothing deleted; re-run with --apply". No candidate listed, so `--apply` was not run, per the block's own rule for an empty preview.
7. A2: `git reflog -n 3 --date=iso` read (before the job started) `0143b9e17 ... commit: F296 R6 C2: the evidence script`, `218933a46 ... commit: F296 R6 C1: ...`, `a80252cde ... commit: F296 R5 C5: handback`. `python3 .remedy-wt/f296-r6/prep/launch.py evidence .remedy-wt/f296-r6-worker` started the run (pid 3553006); `python3 .remedy-wt/f296-r6/prep/wait.py evidence .remedy-wt/f296-r6-worker 50` returned on the first call. Verbatim lines: `exit 0 wall 1594.5`, `head 0143b9e17e05e2626602830340b25fef55479b04`, `ancestry-path count 22`, `plain count 22`, `collected node ids 11592, deselected 251`, `red control: unsafe among the real ids 0 []`, `red control: planted id -> a local absolute path`, `pytest exit 0, {'passed': 11586, 'failed': 0, 'skipped': 6}, output_hash 5780a21d94ef59efa43c7060eec224c495289d747b430dc105e219d11f25bf0f`, `validate_verification_tests problems [] passed 11586`, `is_valid_current_run True`, `validation_errors []`. The summary JSON reported `"verdict": "PASS_WITH_RISKS"`, `"total_passed": 11586`, `"commit_count": 22`.
8. A3: from the clean, pushed tree at C2, `python3 .remedy-wt/f296-r6/prep/launch.py zip .remedy-wt/f296-r6-worker` started the build (pid 3852120); `python3 .remedy-wt/f296-r6/prep/wait.py zip .remedy-wt/f296-r6-worker 50` returned on the first call with `exit 0 wall 16.8`. The log's verbatim summary line (this machine's home folder written as `~`): `{"member_count": 2045, "authoritative_count": 23, "symlink_count": 0, "tombstone_count": 0, "final_path": "~/Repos/remedy-history/zips/remedy-review-20261022-085320-READY_FOR_REVIEW.zip", "final_sha256": "cc616314ffef4d468e3dcfa497b55011ec6b129005fead9927778f05f410fbe5", "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW", "evidence_authoritative": true, "review_subject_alignment": "PASS", "manifest_sha256": "07f965497283ea4544c115a4316f2762983aac9afbb858280e9ba73d87f564ed"}`. A second Python script then read the package: a sha256 over the file read `cc616314ffef4d468e3dcfa497b55011ec6b129005fead9927778f05f410fbe5` (matching the build's own reading); `zipfile.is_zipfile` returned `True`; `testzip()` returned `None`; `.review_zip_manifest.json` inside the package carried `committed_review_subject.base_commit = eb7aa432b15331cc8e777b34306bcb144fb5a8fe` and `committed_review_subject.head_commit = 0143b9e17e05e2626602830340b25fef55479b04`, matching the block's expected base and C2's full sha. No zip refusal occurred, so the second-attempt alternative path was not needed.
9. Gate 3: `python3 -m apps.cli.main integrity check --json` exit 0, six checks all `pass` (handler_import, live_review_verdict, plan_consistency, relevant_untracked, repo_root_hygiene, high_blockers_open), `"fail_count": 0`. `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"` printed `['R-1246', 'R-1281', 'R-1326', 'R-1351', 'R-1353', 'R-1418', 'R-1421']`, matching the block's required list exactly. `git status --porcelain` printed nothing.

## Authored-text proofs

Applied this round, each proved equal over bytes by a script that only reads, against the prepared file: all four paths of C1 (plus `.agent/authored/f296-r6.md` additionally proved equal to the prompt's own `block.md` by line count and sha256), the one path of C2. A1, A2 and A3 are the worker's own run outputs, not reviewer-authored text, and carry no such proof; A2's script itself (`.agent/authored/f296-r6-create_f296_evidence.py`) is reviewer-authored and was proved byte-equal in C2, then run unedited.

## Evidence and package

Evidence job id `f296r6e1001`. A2's lines, quoting the launcher's own tool output verbatim: `exit 0 wall 1594.5`; `head 0143b9e17e05e2626602830340b25fef55479b04`; `ancestry-path count 22`; `plain count 22`; `collected node ids 11592, deselected 251`; `red control: unsafe among the real ids 0 []`; `red control: planted id -> a local absolute path`; `pytest exit 0, {'passed': 11586, 'failed': 0, 'skipped': 6}`; `validate_verification_tests problems [] passed 11586`; `is_valid_current_run True`; `validation_errors []`.

Package `remedy-review-20261022-085320-READY_FOR_REVIEW.zip`, SHA-256 `cc616314ffef4d468e3dcfa497b55011ec6b129005fead9927778f05f410fbe5` (quoting the build tool's own `final_sha256` field, re-derived independently by a Python sha256 over the file and found equal), directory `~/Repos/remedy-history/zips` (quoting the build tool's own `REVIEW_PACKAGE_DIR`), accepted head `0143b9e17e05e2626602830340b25fef55479b04` (quoting `.review_zip_manifest.json`'s own `committed_review_subject.head_commit`, equal to C2's full sha).

## Staging reclaim

Preview (`python3 -m apps.cli.main data reclaim --orphans`), quoting the tool's own output: "Reclaimable: nothing"; every other class is listed "(durable)" with its size (api 7.3 MB, autonomy 457 B, control 1.9 KB, crash 1.0 KB, evidence_exports 2.4 MB, job_apply_records 27.2 KB, job_evidence_index 9.3 KB, job_logs 299.8 KB, jobs 2.2 MB, logs 83.2 KB, memory 3.5 KB, missions 273.4 KB, projects 60.3 KB, review_reports 84.1 KB, roadmap 175.3 KB, runs 1.6 MB, serve 151.3 KB) — each refused because reclaim addresses ephemeral classes only and every one of these is durable; "Would free 0 B in 0 paths — nothing deleted; re-run with --apply". No candidate was listed, so `--apply` was not run; the empty reading is recorded here per the block's own rule.

## Deviations & assumptions

None. The commit sequence landed exactly as ordered (C1, C2, then this C3), each commit touching only its named paths. The evidence job and the zip build each ran exactly once through the block's own `launch.py`/`wait.py`, with this worker's shell tool using its longest timeout and `wait.py` returning on the first call for each. No amend, rebase, force-push or `--no-verify` was used. `REMEDY_TEST_MAX_WORKERS` was never set, no `-n` of this worker's own was passed, no mutation ran, and no worktree of this worker's own was created. `.data` was never read directly by this worker (only by the tools it ran, as the block permits). This worker never changed its own working directory; every command needing the repository root as cwd ran through a small `python3` script under `.remedy-wt/f296-r6-worker/` that passes `cwd=`. Both pushes (after C2, and the one following this commit) ran on the first attempt with no HTTP 500, so the retry path was never exercised.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate — no pull request is open for this branch yet.
3. The reviewer reviews round 6 and books its verdict in the next round's first commit.
4. The closing round: the Built State, the rotation, SU-074's consumed_by, the STATUS flip with the README sync, and the pull request, left unmerged.

Operator questions open: 0. Open findings: `['R-1246', 'R-1281', 'R-1326', 'R-1351', 'R-1353', 'R-1418', 'R-1421']` (7).

## For the operator, in plain sentences

This session collected and checked the closing evidence for the tier-escalation feature: all 11,586 selected automated tests passed, none failed, and the six skipped tests were intentional. The review package that a human or another tool will inspect before this feature closes was built successfully and is ready for review. It is stored outside this repository's working copy, on this machine, in the user's review archive folder.
