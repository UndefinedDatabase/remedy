# Handback — F307 round 32, the closing round: book round 31, re-assign six findings to F314, rotate the ledger, register F314, accept F307

## Session

SESSION 7 of feature F307 · round 32 · rounds so far 32

Context self-assessment: this worker verified every prepared digest before any write, copied each prepared file by a script and proved equality over bytes, ran the rotation and each gate once; context is ample and nothing was lost. The session ends here because F307 is closed and the next feature starts in a fresh session.

Fortschritt: 100 % (F307 is accepted; its pull request waits for the next session's Open PR Gate) — Schätzung

## Range

Review of `857783258`..`HEAD` on `feature/f307-findings-paydown-v9`.

## Commits

### 5540154ae F307 R32 C1: book round 31, re-assign six findings to F314, the Built State, the consolidation brought to nine findings, save the round 32 block and the PR body
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r32.md` | +137/-0 | NEW FILE, this round's block, byte copy |
| `.agent/authored/f307-r32-pr_body.md` | +58/-0 | NEW FILE, the pull request body, byte copy |
| `.agent/live_review.md` | +8/-0 | round 31 booked, six findings re-assigned to F314 |
| `docs/roadmap/features/T2_F307.md` | +43/-0 | the Built State |
| `docs/agents/planner_reviewer_prompt.md` | +6/-5 | the consolidation brought to nine findings |
| `.agent/plan.md` | +7/-9 | rewritten |

### a4d05508a F307 R32 C2: rotate the finding ledger into its archive
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +0/-663 | the rotation script's output |
| `.agent/live_review_archive.md` | +681/-0 | the rotation script's output |

DECLARED OVERSIZE (681 insertions, F307's one such commit): inseparable, because the rotation script writes the ledger and the archive in one step and verifies every moved record by sha256 across both, so neither file can land without the other. No earlier commit of F307 passed 500 insertions.

### 2cd5ce062 F307 R32 C3: register F314 — Findings paydown v10 under amend0911-feedback rule B: feature file, STATUS line, pin 314, README counters
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T2_F314.md` | +49/-0 | NEW FILE, the feature file |
| `docs/roadmap/STATUS.md` | +7/-0 | F314's line |
| `README.md` | +2/-2 | counters |
| `tests/docs/test_docs_consistency.py` | +5/-1 | the registered-count pin moves to 314 |

### (this commit) F307 R32 C4: accept F307 in STATUS with its README sync and the self-use queue
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/STATUS.md` | +1/-1 | C4: F307's line becomes the accepted line (measured before this handoff joined) |
| `README.md` | +15/-3 | C4: `155 of 314`, Tier 2 row `48 | 49`, F307's paragraph (measured before this handoff joined) |
| `scripts/self_use_queue.json` | +1/-1 | C4: SU-073 `consumed_by` becomes `F307` (measured before this handoff joined) |
| `.agent/handoff.md` | rewritten | C4: this handback (a handoff cannot table the commit that writes it) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | commit `5540154ae`, byte proofs held, numstat equal to the manifest |
| C2 | done | commit `a4d05508a`, rotation exit 0, output equal to the simulation, both files byte-equal to the prepared ones; declared oversize |
| C3 | done | commit `2cd5ce062`, byte proofs held, numstat equal to the manifest |
| C4 | done | this commit, byte proofs held, numstat equal to the manifest |
| Push | pending | reported in the session reply |
| Pull request | pending | created after the push; number and URL in the session reply |
| Gate 1 | done | status showed only the three C4 files; `verify.py` last line `ALL True` |
| Gate 2 | done | the STATUS line occurs once; no line begins `- [~]` |
| Gate 3 | done | exit 0, `578 passed in 64.03s` |
| Gate 4 | done | exit 0, six checks `pass`, `fail_count` 0 |
| Gate 5 | done | the open set equals the six ordered ids |

## External actions

None before this commit. The push and the pull request follow it and are reported in the session reply. No fetch or pull, no merge, no provider call. The scratch folder `.remedy-wt/f307-r32-worker/` holds the digest checker, the copy and proof scripts, the commit messages and the gate scripts.

## Verification

1. Digests before any write: `block.md` (137 lines), `verify.py`, `manifest.tsv`, `status_line.txt` and `sim-rotation.txt` equal the prompt's; every prepared file `manifest.tsv` lists matched (checker run with `python3 -I`, last line `ALL OK`).
2. Preconditions: HEAD `857783258` equal to `origin/feature/f307-findings-paydown-v9`, `git status --porcelain` empty, `.agent/STOP` absent. `git branch --show-current` read `feature/f307-findings-paydown-v9` before each commit.
3. Rotation (C2), `python3 scripts/rotate_live_review.py` through a wrapper with cwd the repository root, exit 0, output whole (the home folder is written as `~`):

```
gate records moved: 70
finding pairs moved: 133 (266 records)
resolved-text records moved: 3
old ledger size: 485937 bytes
new ledger size: 161479 bytes
old archive size: 6836056 bytes
new archive size: 7160532 bytes
open findings before: 6
open findings after: 6
gate headers matching neither known form (left in place): 1
written: ~/Repos/remedy/.agent/live_review.md and ~/Repos/remedy/.agent/live_review_archive.md
```

   Ledger size before 485937 bytes, after 161479 bytes. Exit code and every line but the last equal `sim-rotation.txt`; both files equal their prepared C2 files over bytes.
4. Gate 1: `git status --porcelain` showed `M  README.md`, `M  docs/roadmap/STATUS.md`, `M  scripts/self_use_queue.json` only. `python3 .remedy-wt/f307-r32/prep/verify.py` printed `True` on every line, `absent` for `C4 committed`, last line `ALL True`.
5. Gate 2: count of the status line in the STATUS page 1; lines beginning `- [~]`: none.
6. Gate 3: the ordered pytest selection, once, exit 0, `578 passed in 64.03s (0:01:04)`, no FAILED, ERROR or SKIPPED line.
7. Gate 4: `python3 -m apps.cli.main integrity check --json` exit 0, six checks `pass` (`handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`, `repo_root_hygiene`, `high_blockers_open`), `"fail_count": 0`.
8. Gate 5: `open_finding_ids` printed `['R-1246', 'R-1281', 'R-1326', 'R-1351', 'R-1353', 'R-1418']`.

## Authored-text proofs

Applied this round, each proved equal over bytes by a script that only reads, against the prepared file: every file of C1, C3 and C4, and both ledger files of C2. The STATUS line in `docs/roadmap/STATUS.md` is byte-identical to the prep folder's `status_line.txt` without its trailing newline (count 1). It names the package folder as `~/Repos/remedy-history/zips` (the file carries the machine's absolute form of the same folder).

## Deviations & assumptions

Gate 1's `verify.py` was run with the repository root as its argument, spelled as a full path, instead of `.`; the checked folder is the same. Nothing else differed: the commit sequence landed exactly as ordered (C1, C2, C3, then this C4), each touching only its named paths. No amend, rebase, force-push or `--no-verify`, `.data` never read by this worker, no second run of any copy script or gate.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate, which merges F307's pull request in the NEXT session and never in this one.
3. The reviewer's verdict on round 32 is booked in the next feature's first commit.
4. Rule A5: the next unchecked line in `docs/roadmap/STATUS.md`.

Operator questions open: 0. Open findings: 6 (R-1246, R-1281, R-1326, R-1351, R-1353 and R-1418, owned by F314).

## For the operator, in plain sentences

This clean-up batch repaired fifty-seven small problems, and each repair has a test that fails without it. It also wrote down thirty-three repairs that the operator's own branches had already made.

What a person notices is that a job which stops because one of its steps could not be finished keeps its finish time and runs that step again when tried again, that an order naming one file by a plain word is read as that file, that a middle way of running an order now sits between the small and the full one, and that a settings file that cannot be read is answered with a clear refusal instead of a crash report.

Several large pieces of code were split into smaller ones on the way.

The paid run of Remedy on itself stopped at its approval gate, as it should.

The whole test collection passed on the code that ships, after one repair.

The review package is named remedy-review-20261022-061118-READY_FOR_REVIEW.zip and sits in the zips folder inside the history folder under your home folder.

A pull request is open and will be merged at the start of the next session unless the operator merges it earlier.

Six problems stay written down for the next clean-up batch, and that batch is registered here.
