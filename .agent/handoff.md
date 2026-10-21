# Handback — F060 round 2: round 1 booked, R-1404 repaired, a finished job's sources and claims landed

## Session

SESSION 1 of feature F060 · round 2 · rounds so far 2

Context self-assessment: this worker verified every prepared digest, made C1 by byte copy, wrote the repair tests, the sources module and their tests itself, ran the chosen tests once per gate, and wrote this handback with ample context margin left.

Fortschritt: ~40 % (T001 and the sources landed · verifier and commands open) — Schätzung

## Range

Review of `2dd431430`..`HEAD` on `feature/f060-long-run-certificate`.

## Commits

### d480036a5 F060 R2 C1: book round 1, register R-1404, DECISION F060 D2 and the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f060-r2.md` | 191/0 | this round's block, byte-saved for the authored-text proof |
| `.agent/live_review.md` | 4/0 | round 1 booked, R-1404 registered |
| `.agent/decisions.md` | 10/0 | DECISION F060 D2 appended |
| `.agent/plan.md` | 7/8 | rewritten |
| `.agent/prose_slips.md` | 1/0 | one line appended |

### 53c761fa4 F060 R2 C2: two tests hold the exact-fit budget and the refusal before writing (R-1404)
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_job_certificate.py` | 21/0 | two tests added: exact-fit budget embeds the diff; an existing out path is refused before the packer is called |

### 92b83077d F060 R2 C3: a finished job's certificate sources, claims and issue record
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/job_certificate_sources.py` | 214/0 | new: `collect_certificate_inputs`, the issue record, the not-ready error |
| `packages/orchestration/job_certificate.py` | 2/0 | `CERTIFICATE_DEFAULT_MAX_BYTES` |
| `tests/test_no_orphan_modules.py` | 2/2 | the profile's unwired entry replaced by the sources module's entry |

### ae3224092 F060 R2 C4: tests of a finished job's certificate sources and claims
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_job_certificate_sources.py` | 222/0 | new: 17 test cases over members, claims, states, report choice, actuals, issue record, symlink |

### C5 F060 R2 C5: handback (this commit)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | edited | this handback |

## External actions

- `git push origin feature/f060-long-run-certificate` follows this commit; its outcome is reported in the session reply. No pull request was opened. No worktree was added or removed.

## Verification

Preconditions: `block.md`, `verify.py` (first digest `489d07b4...`, then the reviewer's updated `3df70ff6433c...`, checked before gate 1), `run_selection.py`, `selection.txt` and `digests.txt` matched; all five `c1-` files matched `digests.txt`. The saved block copy has 191 lines and sha256 `d26a5a21414121414d741e7554c0ec7f7a8635d058d8bc00fd95436497d2c830`, equal to `block.md`.

1. Gate 1: `git status --porcelain` empty; `python3 .remedy-wt/f060-r2/prep/verify.py .` — every line `True`, C5 `absent`, last line `ALL True`.
2. Gate 2: `python3 -m ruff check` over the five Python files C2, C3 and C4 touched — `All checks passed!`
3. Gate 3: `python3 .remedy-wt/f060-r2/prep/run_selection.py . .remedy-wt/f060-r2-worker/selection-output.txt` — `paths 76`, `exit 0`, `3435 passed, 2 skipped in 29.76s`; no FAILED, ERROR or `process(es) behind` line; two SKIPPED lines (the D12 quarantine of the deleted reviewer agent file; install smoke is opt-in).
4. Gate 4: `python3 -m apps.cli.main integrity check --json` — exit 1, `fail_count` 1, only `high_blockers_open`: `12 open blocker/high: R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362`, the same twelve as before the round.
5. Gate 5: `open_finding_ids` over `.agent/live_review.md` — `89`.
6. Gate 6: `git diff --stat 646c4b1d7 HEAD -- packages/orchestration/review_zip.py` — no output.

## Authored-text proofs

C1: the five prepared `c1-` files are byte copies, proven equal by sha256 at copy time and again by `verify.py`. C2 to C4 are the worker's own code and tests.

## Deviations & assumptions

- C3's orphan-list edit replaces the profile's entry instead of adding beside it, by the reviewer's ruling, because the new module reaches the profile. The worker stopped before committing C3 and resumed after the ruling; `verify.py` was updated by the reviewer and its new digest checked.
- The test fixture job carries `metadata={"target_repo": ...}`. Without it the decision queue derives one open "no target repository" decision for every job, so the block's expected `decisions_count` 0 for a record-only job would not hold. The module itself counts `list_decisions(plan, [])` as specified.
- Test (a) also writes the two run-manifest files, so every mapped file is present, not only the export's three.
- A persisted report is accepted when the whole line `- State: <state>` is among its lines; a symlinked or unreadable member file raises `CertificateError` naming the path.
- No mutation red-proofs and no full-suite run, as the block orders.

## Next

1. Phase 1 rule 1: `.agent/STOP`.
2. Phase 1 rule 2: the Open PR Gate.
3. Book round 2's verdict in the next round's first commit.
4. Round 3: the verifier and its tamper fixtures.

Operator questions open: 3.
Open findings: 89.

## For the operator, in plain sentences

The certificate work now knows how to gather what a finished job leaves behind. For a job that has ended, in any of five ways, Remedy reads its report, its cost record, its checks, its ownership record, its run manifest, its diff and its run logs, and works out the claims the certificate will state. A job that is still going, or that does not exist, is refused with a plain sentence. When the saved report describes an earlier state of the job, Remedy writes a fresh one in memory and changes nothing on disk. Each job also keeps a small record of the certificates issued for it, so a later certificate gets a higher number. A previous finding about two missing tests was repaired. Nothing yet creates a certificate on its own; that comes in a later round. The tests chosen for this round ran and passed, and the one known set of open serious findings is unchanged. Three questions still wait for you.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `d480036a5` |
| C2 | done | `53c761fa4` |
| C3 | deviated | `92b83077d`; orphan-list entry replaced, by the reviewer's ruling |
| C4 | done | `ae3224092`; fixture carries a target repository |
| C5 | done | this commit |
| Gate 1 | done | `ALL True` |
| Gate 2 | done | `All checks passed!` |
| Gate 3 | done | exit 0, 3435 passed, 2 skipped |
| Gate 4 | done | `fail_count` 1 (`high_blockers_open`, the same twelve) |
| Gate 5 | done | 89 |
| Gate 6 | done | no output |
