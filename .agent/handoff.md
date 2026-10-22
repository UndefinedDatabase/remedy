# Handback — F074 round 5: the closing round

## Session

SESSION 1 of feature F074 · round 5 · rounds so far 5

Context self-assessment: this worker checked the block's own digest and every prepared file's
digest against `manifest.tsv` before any write, byte-copied each C1/C2/C3 file with a disk-to-disk
equality proof, ran the rotation and all five gates once each with no overlap, and context stayed
ample throughout the round.

The session ends here because F074 is closed and the next feature starts in a fresh session.

Fortschritt: 100 % (F074 is accepted; its pull request waits for the next session's Open PR Gate) — Schätzung

## Range

Review of `6fc7c2c17`..`HEAD` on `feature/f074-estimate-calibration`.

## Commits

### 402c94d55 F074 R5 C1: book round 4, the Built State, save the round 5 block and the PR body
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f074-r5-pr_body.md` | +63/-0 | NEW FILE, this round's PR body, byte copy equal to the prepared file |
| `.agent/authored/f074-r5.md` | +131/-0 | NEW FILE, this round's block, byte copy equal to `block.md` (131 lines, sha256 `9e5a980e6b8c4232290ba275dc43dc493524d8c7f708d8c1fac6b4457fe58cd7`, equal to the prompt's) |
| `.agent/live_review.md` | +2/-0 | round 4's PASS verdict booked |
| `.agent/plan.md` | +5/-4 | rewritten for round 5 (the closing round) |
| `docs/roadmap/features/T3_F074.md` | +36/-0 | Built State section added |

`git show --shortstat`: 5 files changed, 237 insertions(+), 4 deletions(-).

### 8c83eb5e9 F074 R5 C2: rotate the finding ledger into its archive
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +0/-12 | 6 gate records and their resolved pairs moved out |
| `.agent/live_review_archive.md` | +12/-0 | receives the rotated records, byte-verbatim |

`git show --shortstat`: 2 files changed, 12 insertions(+), 12 deletions(-).

### (this commit) F074 R5 C3: accept F074 in STATUS with its README sync and the self-use queue
Grouped table (self-reference exception — this commit also writes the handoff that tables it):
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/STATUS.md` | +1/-1 | F074's `[~]` line becomes `[x]`, accepted, per `status_line.txt` |
| `README.md` | +12/-2 | `158 of 314`; Tier 3 row `16 \| 29`; F074's capability paragraph closes the Tier 3 list |
| `scripts/self_use_queue.json` | +1/-1 | SU-076's `consumed_by` becomes `F074` |
| `.agent/handoff.md` | n/a (self) | this handback — a handoff cannot table the commit that writes it |

C3's three files measured before the handoff joined them: `docs/roadmap/STATUS.md` 1/1,
`README.md` 12/2, `scripts/self_use_queue.json` 1/1 — matching `manifest.tsv` exactly.

## Item status

| Item | Status | Reason |
|---|---|---|
| Preconditions | done | HEAD `6fc7c2c17` equal to origin, `git status --porcelain` empty, no `.agent/STOP`, `gh pr list` open `[]`, branch as ordered |
| C1 | done | |
| C2 | done | rotation exit 0, output matched `sim-rotation.txt` line for line (bar the `written:` line), ledgers byte-equal to the C2 prepared files |
| C3 | done | three files byte-equal to the C3 prepared files before this commit |
| Gate 1 | done | `verify.py .` — every line `True`, `C3 committed` read `absent` (not yet committed at gate time), last line `ALL True` |
| Gate 2 | done | `status_line.txt` content occurs exactly once in `STATUS.md`; no `STATUS.md` line begins `- [~]` |
| Gate 3 | done | exit 0, `587 passed in 40.52s`, no FAILED/ERROR/SKIPPED line |
| Gate 4 | done | `integrity exit 0 6 pass; ... "fail_count": 0` |
| Gate 5 | done | open finding ids exactly `['R-1246', 'R-1281', 'R-1326', 'R-1351', 'R-1353', 'R-1418', 'R-1421']` |
| Push | pending | happens immediately after this commit, per the block's `THEN` step; outcome in the session reply |
| Pull request | pending | happens immediately after the push, per the block's `THEN` step; no number exists while this file is written; outcome in the session reply |

## External actions

None at commit time. `git push origin feature/f074-estimate-calibration`, `gh pr create`, and
`gh pr list` all run immediately after this commit, per the block's `THEN` step; their commands,
exit codes and outcomes are reported in this round's session reply rather than restated here,
since no PR number exists while this file is being written.

## Verification

Gate 1 — `python3 .remedy-wt/f074-r5/prep/verify.py .` (run from the primary checkout): every check line
`True` (parent-equality for both commits, one `Cn` subject per commit, branch, every C1/C2 path and
numstat and byte-equality, `C3 committed` → `absent`, then the three C3 working-tree byte-equality
checks `True`); last line `ALL True`.

Gate 2 — the content of `status_line.txt` without its trailing newline (the `- [x] F074 — Estimate
calibration (...)` line) occurs exactly once in `docs/roadmap/STATUS.md`; no line of `STATUS.md`
begins `- [~]`; count = 1, tilde-line count = 0.

Gate 3 — `python3 .remedy-wt/f074-r5/prep/gate3.py .` (run from the primary checkout), once:
```
exit 0
587 passed in 40.52s
```
No `FAILED`, `ERROR` or `SKIPPED` line printed.

Gate 4 — the same run's integrity line:
```
integrity exit 0 6 pass; ['{"check_count": 6, "checks": [{"message": "handlers=196", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}']
```

Gate 5 — `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`:
exit 0, `['R-1246', 'R-1281', 'R-1326', 'R-1351', 'R-1353', 'R-1418', 'R-1421']` — equal to the
block's expected list.

C2's rotation, whole output:
```
exit 0
gate records moved: 6
finding pairs moved: 0 (0 records)
resolved-text records moved: 0
old ledger size: 143641 bytes
new ledger size: 133734 bytes
old archive size: 7210272 bytes
new archive size: 7220179 bytes
open findings before: 7
open findings after: 7
gate headers matching neither known form (left in place): 1
```
(the `written:` line differed only in naming this real checkout's paths rather than the dry
worktree's, as the block anticipated). Ledger size before/after: 143641 → 133734 bytes; archive
before/after: 7210272 → 7220179 bytes.

## Authored-text proofs

C1, C2 and C3's prepared files were each copied by a Python byte copy and proven equal over bytes
at copy time, before staging; `verify.py` (gate 1) re-proved the C1/C2 committed blobs and the C3
working-tree files, all `True`.

STATUS line proof: `docs/roadmap/STATUS.md`'s F074 line is byte-identical to `status_line.txt`
without its trailing newline (occurrence count 1):
`- [x] F074 — Estimate calibration (T001–T003 complete; accepted 2026-10-22 · live review PASS —
ACCEPTED · Evidence job f074r4e1001 · package remedy-review-20261022-123801-READY_FOR_REVIEW.zip ·
SHA-256 d051c25a03f87697660083e4f7f4e8ca6a5c8c3ee2b6c099ab385cca29a7c920 · package path ~ · accepted
HEAD 15922d2be7f1079521572747018e9a9951056747)`

## Deviations & assumptions

None. The block's ordered sequence (preconditions, C1, C2, C3's three files, gates 1–5, the
handoff, then push and `gh pr create`) was followed exactly; no extra commit, no dropped commit, no
reordering.

## For the operator, in plain sentences

Once a kind of task has run often enough in this project, Remedy's cost estimates for it now come
from what those tasks really used, instead of a fixed guess per size. Every such estimate says how
many past tasks it rests on, and a kind of task measured too few times still keeps the fixed guess
and says so plainly. A new view shows the measurement and how old it is, and a stored plan now
shows a measured kind's typical size next to its size word. The paid run of Remedy on its own
backlog, which this closure consumes, stopped at its normal approval gate, the way every such run
does before anything it proposes is applied. The whole test collection passed on the code that
ships, and it used slightly less computer time than the previous closure did. The review package is
named `remedy-review-20261022-123801-READY_FOR_REVIEW.zip`, in the `zips` folder of the operator's
review-package history. A pull request is open and will be merged at the start of the next session
unless the operator merges it earlier.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. The Open PR Gate, which merges F074's pull request in the NEXT session and never in this one.
3. The booking of round 5's verdict, in the next feature's first commit.
4. Rule A5 (the next unchecked line in `docs/roadmap/STATUS.md`).

Operator questions open: 0. Open findings: 7 (R-1246, R-1281, R-1326, R-1351, R-1353, R-1418 and
R-1421, owned by F314).
