# Handback — F074 round 4: book round 3, the evidence job and the review package

## Session

SESSION 1 of feature F074 · round 4 · rounds so far 4

Context self-assessment: this worker verified the block and digest list's own digests, then every
prepared file's digest, before any write; byte-copied each C1/C2 file with a disk-to-disk equality
proof; ran the evidence job and the package build through the launch/wait helpers, once each, with
no overlap; and context stayed ample throughout.

Fortschritt: ~95 % (everything but the closing round is done) — Schätzung

## Range

Review of `61e743187`..`HEAD` on `feature/f074-estimate-calibration`.

## Commits

### 4932b0109 F074 R4 C1: book round 3, the plan, the block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f074-r4.md` | +116/-0 | NEW FILE, this round's block, byte copy equal to `block.md` (116 lines, sha256 `c2b3f045...8f3c27`, equal to the prompt's) |
| `.agent/live_review.md` | +2/-0 | round 3's PASS verdict booked |
| `.agent/plan.md` | +4/-5 | rewritten for round 4 |

`git show --shortstat`: 3 files changed, 122 insertions(+), 5 deletions(-).

### 15922d2be F074 R4 C2: the evidence script
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f074-r4-create_f074_evidence.py` | +300/-0 | NEW FILE, byte copy of its prepared file |

`git show --shortstat`: 1 file changed, 300 insertions(+).

### (this commit) F074 R4 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback (a handoff cannot table the commit that writes it) |

## Item status

| Item | Status | Reason |
|---|---|---|
| Preconditions | done | HEAD `61e743187` equal to origin, status empty, no `.agent/STOP`, open PR list `[]`, branch as ordered |
| C1 | done | |
| C2 | done | pushed to origin (`61e743187..15922d2be`) |
| A1 | done | preview listed nothing; apply skipped |
| A2 | done | evidence job exit 0 |
| A3 | done | READY_FOR_REVIEW |
| C3 | done | this commit |
| Gate 1 | done | |
| Gate 2 | done | |
| Gate 3 | done | |

## External actions

- `git push origin feature/f074-estimate-calibration` after C2: `61e743187..15922d2be`, no retry needed (no HTTP 500).
- `python3 .remedy-wt/f074-r4/prep/launch.py evidence .remedy-wt/f074-r4-worker` (via a cwd-bound
  wrapper under `.remedy-wt/f074-r4-worker/`) and `wait.py evidence ... 50`: exit 0, wall 1594.0 s
  (one wait call).
- `python3 .remedy-wt/f074-r4/prep/launch.py zip .remedy-wt/f074-r4-worker` (same wrapper pattern)
  and `wait.py zip ... 50`: exit 0, wall 8.1 s.
- `git push origin feature/f074-estimate-calibration` after this commit (outcome in the worker's
  reply).
- No pull request created, no `gh` write beyond the read-only Open PR Gate check.

## Verification

Gate 1: `git status --porcelain` printed nothing; `python3 .remedy-wt/f074-r4/prep/verify.py .`
exit 0, every line `True` (C3 `absent` at that moment), last line `ALL True`.

Gate 2: evidence `.exit` file `exit 0 wall 1594.0`; zip `.exit` file `exit 0 wall 8.1`; readings
below under "Evidence and package".

Gate 3: `python3 -m apps.cli.main integrity check --json` exit 0, `"fail_count": 0`, all six checks
pass (`handler_import` handlers=196; `live_review_verdict` last Gate verdict PASS;
`plan_consistency` unchecked=0, context_complete=False; `relevant_untracked` untracked=0,
relevant=0; `repo_root_hygiene` pass; `high_blockers_open` no open blocker/high findings). The
open-finding-ids check printed `['R-1246', 'R-1281', 'R-1326', 'R-1351', 'R-1353', 'R-1418',
'R-1421']` (7 open findings), matching the block's expected list exactly. `git status --porcelain`
empty before this commit.

## Evidence and package

Evidence job id: `f074r4e1001`. A2's lines, verbatim:

```
head 15922d2be7f1079521572747018e9a9951056747
ancestry-path count 18
plain count 18
collected node ids 12034, deselected 251
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 12028, 'failed': 0, 'skipped': 6}, output_hash dad4f9e49a91ec2e38d3000ed0aee55c5831048c3135b8a3052f9032c3317758
validate_verification_tests problems [] passed 12028
is_valid_current_run True
validation_errors []
```

Its closing report: verdict `PASS_WITH_RISKS`, `manual_completion` true, 29 authority files, 18
commits, total passed 12028.

Package (the build's own lines):

```
PACKAGE_STATUS=READY_FOR_REVIEW
REVIEW_SUBJECT_ALIGNMENT=PASS
EVIDENCE_AUTHORITATIVE=true
ZIP_PATH=~/Repos/remedy-history/zips/remedy-review-20261022-123801-READY_FOR_REVIEW.zip
final_sha256 d051c25a03f87697660083e4f7f4e8ca6a5c8c3ee2b6c099ab385cca29a7c920
```

- Name: `remedy-review-20261022-123801-READY_FOR_REVIEW.zip`; directory
  `~/Repos/remedy-history/zips`; 8.2M, 2060 members.
- A Python sha256 over the file: `d051c25a03f87697660083e4f7f4e8ca6a5c8c3ee2b6c099ab385cca29a7c920`
  (equal to the build's own reading).
- `zipfile.is_zipfile` True, `testzip()` None.
- `.review_zip_manifest.json` inside the package, `committed_review_subject`: base
  `148a1c38672f3fa6547fa30c7348592641d55a67` (equal to the prompt's expected base), head
  `15922d2be7f1079521572747018e9a9951056747` (equal to C2's full sha), commit_count 18, file_count
  52.
- The default directory was writable; the fallback directory was not needed.

## Staging reclaim

`python3 -m apps.cli.main data reclaim --orphans` (preview): `Reclaimable: nothing`, `Would free 0
B in 0 paths`; no path refused — only durable classes (api, autonomy, control, crash,
evidence_exports, job_apply_records, job_evidence_index, job_logs, jobs, logs, memory, missions,
projects, review_reports, roadmap, runs, serve) listed as not reclaimed. No candidate, so the
`--apply` run was skipped.

## Authored-text proofs

The prepared files of C1 and C2 were copied by a Python byte copy and proven equal over bytes at
copy time (`c1_copy.py`, `c2_copy.py` under `.remedy-wt/f074-r4-worker/`); `verify.py` re-proved
each against the commit (gate 1, all `True`). `block.md` equals the saved `.agent/authored/f074-r4.md`
(116 lines, sha256 `c2b3f0452dcd29187b6e91f534e641c452b2f87a3fab8da311a2ba46f88f3c27`, equal to both
the prompt's digest and `digests.txt`'s own line for `block.md`).

## Deviations & assumptions

One: the first A1 preview run was executed as `cd <repo> && python3 -m apps.cli.main data reclaim
--orphans` in a single Bash call, which breaks the block's "never cd" constraint even though the
sandbox did not refuse it and the command was read-only (preview only, nothing deleted, no state
changed). This worker caught it immediately, re-ran the same preview through a cwd-bound Python
wrapper under `.remedy-wt/f074-r4-worker/run_cli.py` (no shell `cd`), got an identical reading, and
used that second, compliant run as the reading recorded above. Every other command this round used
either `git -C <repo>` or a cwd-bound wrapper script under `.remedy-wt/f074-r4-worker/`. No other
deviation: the block's ordered commit/action sequence (C1, C2, A1, A2, A3, gates 1-3, C3, push) was
followed exactly; no extra commit, no dropped commit, no reordering.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. Rule 2 (Open PR Gate); no pull request is open for this branch yet.
3. The reviewer reviews round 4 and books its verdict in the next round's first commit.
4. The closing round: the Built State, the rotation, SU-076's consumed_by, the STATUS flip with the
   README sync, and the pull request, left unmerged.

Operator questions open: 0. Open findings (gate 3): `['R-1246', 'R-1281', 'R-1326', 'R-1351',
'R-1353', 'R-1418', 'R-1421']`.

## For the operator, in plain sentences

The evidence for this feature was collected and checked: the test selection ran once on the final
code, nothing failed, and the checks on the record all read valid. The review package was built,
passed its own alignment and integrity checks, and is ready for review. It sits in the history
folder under the home folder, in the zips subfolder, as the newest review file.
