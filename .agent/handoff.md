# Handoff — F158 round 8

## Session

SESSION 2 of feature F158 · round 8 · rounds so far 8. This session verified the prepared digest
and every file's sha256 before touching anything, applied the two ordered commits exactly as the
block specified, and found all three gates green on the first and only run of each, with comfortable
context headroom throughout.

Fortschritt: ~95 % (everything but the closing round is done) — Schätzung.

## Range

Review of `f78132441`..`18af758db` (C1 to C2; C3 — this file — is the commit that carries it, per
the handback template's self-reference exception).

## Commits

### 2c2306ee6 F158 R8 C1: book round 7, R-1471 resolved, register R-1472, the plan, the block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f158-r8.md` | +128/-0 | NEW FILE — this round's block, the authored-text proof, byte-copied from the prepared `c1-` file |
| `.agent/live_review.md` | +6/-0 | round 7's verdict booked, R-1471 resolved and R-1472 registered, byte-copied |
| `.agent/plan.md` | +7/-8 | rewritten: Current Step/Next Steps moved to round 8, byte-copied |

### 18af758db F158 R8 C2: the evidence script
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f158-r8-create_f158_evidence.py` | +317/-0 | NEW FILE — the evidence script, byte-copied |

### (this commit) F158 R8 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file — carried alone, per the handback template's self-reference exception (R-0149) |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` run once before any write
→ `[]` (Open PR Gate). No other `gh` command run. No `git worktree` command run by me. No stash
entry touched. No `claude` or `codex` binary invoked by me. No web fetch by me.
`git push origin feature/f158-cost-normalization` ran once immediately after C2 → fast-forwarded
`f78132441..18af758db` on the first attempt (no HTTP 500, no retry needed). It runs once more
immediately after this commit; that outcome is reported in the session reply, not in this file.

## Verification

**Gate 1.** `git -C <repo> status --porcelain` → empty (exit 0). Then
`python3 .remedy-wt/f158-r8/prep/verify.py <repo>`, run once from the primary checkout:
```
True	2c2306ee6 single parent
True	2c2306ee6 subject carries a F158 R8 Cn tag: F158 R8 C1: book round 7, R-1471 resolved, register R-1472, the plan,
True	2c2306ee6 adds no machine path
True	18af758db single parent
True	18af758db subject carries a F158 R8 Cn tag: F158 R8 C2: the evidence script
True	18af758db adds no machine path
True	on feature/f158-cost-normalization
True	C1 paths ['.agent/authored/f158-r8.md', '.agent/live_review.md', '.agent/plan.md']
True	C1 .agent/authored/f158-r8.md equals c1-.agent__authored__f158-r8.md
True	C1 .agent/live_review.md equals c1-.agent__live_review.md
True	C1 .agent/plan.md equals c1-.agent__plan.md
True	C2 paths ['.agent/authored/f158-r8-create_f158_evidence.py']
True	C2 .agent/authored/f158-r8-create_f158_evidence.py equals c2-.agent__authored__f158-r8-create_f158_evidence.py
absent	C3
True	the saved block equals block.md
ALL True
```
Exit 0. Every line `True` (C3 correctly `absent`, since C3 had not committed yet when this gate
ran); last line `ALL True`.

**Gate 2.** A2, the evidence job (`python3 .agent/authored/f158-r8-create_f158_evidence.py` via
`launch.py`/`wait.py`), ran once, exit 0, wall 1941.0 s:
```
exit 0 wall 1941.0
head 18af758dbe3e6b569083215ead8ceb5f25fed4cb
ancestry-path count 35
plain count 35
collected node ids 13227, deselected 253
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 13221, 'failed': 0, 'skipped': 6}, output_hash b0f40d249fe819031eb25c5e82880cc08fbe56ec867c40ccc37ff77ad95eb5bc, duration 1910.269s
validate_verification_tests problems [] passed 13221
is_valid_current_run True
validation_errors []
```
`head` equals C2's full sha; ancestry-path and plain counts both 35; collected 13227 and
deselected 253, matching the round 7 (`f78132441`) precheck exactly; red control unsafe count 0
with the planted id correctly flagged "a local absolute path"; pytest exit 0, 0 failed, duration
1910.269 s (above zero); `validate_verification_tests` problems `[]`; `is_valid_current_run` `True`;
`validation_errors` `[]`.

A3, the review package (`bash scripts/make_review_zip.sh --evidence-dir
.remedy-wt/f158-r8-evidence` via `launch.py`/`wait.py`), ran once, exit 0, wall 19.9 s:
```
{"member_count": 2144, "authoritative_count": 31, "symlink_count": 0, "tombstone_count": 0, "final_path": "~/Repos/remedy-history/zips/remedy-review-20261024-192309-READY_FOR_REVIEW.zip", "final_sha256": "f095df6c9db88fc7ac379572cf9a0d783f4eb187cdfa68b5123917814fa6451a", "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW", "evidence_authoritative": true, "review_subject_alignment": "PASS", "manifest_sha256": "5da3c49cd6b54599efe50179f7a7137084c24a17195a21629fd9c86d9c2ef45a"}
PACKAGE_STATUS=READY_FOR_REVIEW
REVIEW_SUBJECT_ALIGNMENT=PASS
EVIDENCE_AUTHORITATIVE=true
ZIP_PATH=~/Repos/remedy-history/zips/remedy-review-20261024-192309-READY_FOR_REVIEW.zip
```
A Python sha256 over the file reproduced `f095df6c9...` exactly; `zipfile.is_zipfile` `True`,
`testzip()` `None`. `.review_zip_manifest.json` inside the package: `committed_review_subject.base`
`407536a9b1d25fb7867808c35129d27df30aa661`, `.head` `18af758dbe3e6b569083215ead8ceb5f25fed4cb` —
base matches round 7's accepted head and head matches C2's full sha exactly. No second attempt was
needed; the sandbox wrote its default directory on the first try.

**Gate 3.** `python3 -m apps.cli.main integrity check --json`, run once from the primary checkout:
```
{"check_count": 6, "checks": [{"message": "handlers=204", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
Exit 0, `fail_count` 0, all six checks `pass`. Then
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`:
```
['R-1246', 'R-1281', 'R-1351', 'R-1353', 'R-1426', 'R-1428', 'R-1448', 'R-1450', 'R-1464', 'R-1467', 'R-1472']
```
Exit 0, the eleven ids named by the block, in that order. `git status --porcelain` → empty.

## Authored-text proofs

C1's byte copy and its disk-to-disk proof read `EQUAL`/`True` for all three targets immediately
after copying, before staging. The mandated proof, `.agent/authored/f158-r8.md` against `block.md`:
byte-identical, 128 lines, sha256 `dd1500c626d21ec619d894abe44bb4c4828c1f40bacab7f9d97d11e14faeb6ea`
for both files — the exact digest `digests.txt` stated for `block.md`. Gate 1's independent
`verify.py` run re-confirmed every `C1 ... equals c1-...` and `C2 ... equals c2-...` line `True`
and the final `the saved block equals block.md` line `True`. `None applied` beyond these — C2's
file is a prepared script byte copy proved the same way, not reviewer-authored findings or verdict
prose under the fidelity protocol.

## Evidence and package

- Evidence job id: `f158r8e1001` (from A2's final JSON: `"job_id": "f158r8e1001"`).
- A2's lines are quoted in full under Gate 2 above.
- Package file name: `remedy-review-20261024-192309-READY_FOR_REVIEW.zip`.
- Package SHA-256: `f095df6c9db88fc7ac379572cf9a0d783f4eb187cdfa68b5123917814fa6451a`.
- Directory: `~/Repos/remedy-history/zips`.
- Accepted head: `18af758dbe3e6b569083215ead8ceb5f25fed4cb` (C2's full sha; matches
  `.review_zip_manifest.json`'s `committed_review_subject.head`).

## Staging reclaim

A1's preview, `python3 -m apps.cli.main data reclaim --orphans`, run once: "Would free 0 B in 0
paths — nothing deleted; re-run with --apply". Every listed class (`api`, `autonomy`, `control`,
`crash`, `evidence_exports`, `job_apply_records`, `job_evidence_index`, `job_logs`, `jobs`, `logs`,
`memory`, `missions`, `projects`, `review_reports`, `roadmap`, `runs`, `serve`) was reported
"durable" and "not reclaimed — reclaim addresses ephemeral classes only," not refused for any other
reason. The preview listed no candidate, so the `--apply` step was skipped per the block; the
reading is the empty one above.

## Deviations & assumptions

None. Every commit matched the block's ordered sequence and paths exactly; every digest in
`digests.txt` matched before any file was used; A2 and A3 each ran exactly once and both exited 0
on the first attempt, with no retry needed for either push; the preview found nothing to reclaim so
no `--apply` ran; no file outside the paths named per commit was touched; no
`REMEDY_TEST_MAX_WORKERS` or extra `-n`; no second test command; no worktree of my own; no
agent/fork/helper of any kind started; no `gh pr create/merge`, `git checkout`/`git switch`, branch
creation/move/deletion or force-push; no `--no-verify`; no `claude`/`codex` binary invoked by me.

## For the operator, in plain sentences

This feature's evidence was collected fresh and checked: the full evidence job ran once, matched
the commit it was supposed to cover, and every one of its validation checks came back clean. The
review package was then built from that same clean, pushed state and is ready for review, saved
outside the repository on this machine. Separately, the paid trial run from the round before this
one — where Remedy wrote the first tests for one of its own untested modules — was reviewed and
approved by its own reviewer, but that change was deliberately left sitting on its own branch and
was never merged into the project. That trial's two model calls were never recorded in the cost
bookkeeping this feature cares about, because no existing ledger on this machine had a place for
them; that gap is now written down so a future clean-up feature can close it.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | three files byte-equal to prepared copies; round 7's verdict booked, R-1471 resolved, R-1472 registered, plan advanced |
| C2 | done | one file byte-equal; the evidence script committed alone; pushed on the first attempt |
| A1 | done | preview found nothing reclaimable (0 B, 0 paths), every class durable; `--apply` correctly skipped |
| A2 | done | evidence job `f158r8e1001` exit 0; head, ancestry counts, collected/deselected, red control, pytest, and validation readings all matched the block's expectations exactly |
| A3 | done | `PACKAGE_STATUS=READY_FOR_REVIEW`, `REVIEW_SUBJECT_ALIGNMENT=PASS`, `EVIDENCE_AUTHORITATIVE=true`; manifest base/head matched; no second attempt needed |
| C3 | done | this handoff, committed alone per the self-reference exception |
| Gate 1 | done | every line `True`, last line `ALL True` (C3 correctly `absent`) |
| Gate 2 | done | A2 and A3 readings both matched the block's expectations exactly |
| Gate 3 | done | exit 0, `fail_count` 0, all six checks pass; eleven open ids match the block exactly; tree clean |
| Push | done | after C2, fast-forward, first attempt; after C3 runs next, outcome in the reply |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work.
2. Phase 1 rule 2 — the Open PR Gate: no pull request is open for this branch yet, so the next
   session checks for open pull requests before starting anything new.
3. The reviewer reviews round 8 and books its verdict in the next round's first commit.
4. The closing round: the Built State, the rotation, SU-084's `consumed_by`, the STATUS flip with
   the README sync, and the pull request, left unmerged.

Operator questions open: 3.
Open findings: 11 (`R-1246`, `R-1281`, `R-1351`, `R-1353`, `R-1426`, `R-1428`, `R-1448`, `R-1450`,
`R-1464`, `R-1467`, `R-1472`).
