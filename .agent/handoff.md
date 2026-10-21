# Handback — F060 round 3: round 2 booked, R-1405 repaired, the certificate verifier and its tamper fixtures landed

## Session

SESSION 1 of feature F060 · round 3 · rounds so far 3

Context self-assessment: this worker verified every prepared digest, made C1 by byte copy, wrote the claims module, the verifier and all their tests itself, ran the chosen tests once per gate, and wrote this handback with ample context margin left.

Fortschritt: ~60 % (T001, the sources and T002 landed · the commands open) — Schätzung

## Range

Review of `8b5a06680`..`HEAD` on `feature/f060-long-run-certificate`.

## Commits

### a43bed5aa F060 R3 C1: book round 2, resolve R-1404, register R-1405, DECISION F060 D3 and the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f060-r3.md` | 219/0 | this round's block, byte-saved for the authored-text proof |
| `.agent/live_review.md` | 6/0 | round 2 booked, R-1404 resolved, R-1405 registered |
| `.agent/decisions.md` | 10/0 | DECISION F060 D3 appended |
| `.agent/plan.md` | 6/7 | rewritten |
| `.agent/prose_slips.md` | 2/0 | two lines appended |

### a4edfe946 F060 R3 C2: the certificate's claims derived from its members' bytes (R-1405)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/job_certificate_claims.py` | 64/0 | new: the three pure derivations of a claim from a member's bytes |
| `packages/orchestration/job_certificate_sources.py` | 15/43 | claims now derived from the members built; `load_gate_result` and the three private helpers removed |
| `tests/orchestration/test_job_certificate_claims.py` | 93/0 | new: None, good and malformed cases of each function |
| `tests/orchestration/test_job_certificate_sources.py` | 2/2 | R-1405: the fixture's checks are three, two passed |

### ae89a7639 F060 R3 C3: the certificate verifier and its verdict (T002)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/job_certificate_verify.py` | 289/0 | new: `CertificateVerification`, `verify_job_certificate`, `render_certificate_verdict` |
| `tests/test_no_orphan_modules.py` | 2/2 | the sources module's unwired entry replaced by the verifier's |

### b2f069785 F060 R3 C4: the tamper matrix and the claim checks of the certificate verifier
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_job_certificate_verify.py` | 420/0 | new: fixture of seven classes, tamper matrix, doctored report and cost, claim rewrites, manifest refusals, verdicts |

### C5 F060 R3 C5: handback (this commit)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | edited | this handback |

## External actions

- `git push origin feature/f060-long-run-certificate` follows this commit; its outcome is reported in the session reply. No pull request was opened. No worktree was added or removed.

## Verification

Preconditions: `block.md`, `verify.py`, `run_selection.py`, `selection.txt` and `digests.txt` matched the digests in the prompt; all five `c1-` files matched `digests.txt`. The saved block copy has 219 lines and sha256 `afb90ecc6818ae8aaef7737e9cd48e3e23767b447fbeed1d20067939bafada25`, equal to `block.md`.

1. Gate 1: `git status --porcelain` empty; `python3 .remedy-wt/f060-r3/prep/verify.py .` — every line `True`, C5 `absent`, last line `ALL True`.
2. Gate 2: `python3 -m ruff check` over the seven Python files C2, C3 and C4 touched — `All checks passed!`
3. Gate 3: `python3 .remedy-wt/f060-r3/prep/run_selection.py . .remedy-wt/f060-r3-worker/selection-output.txt` — `paths 78`, `exit 0`, `3497 passed, 2 skipped in 20.03s`; no FAILED, ERROR or `process(es) behind` line; two SKIPPED lines (the D12 quarantine of the deleted reviewer agent file; install smoke is opt-in).
4. Gate 4: `python3 -m apps.cli.main integrity check --json` — exit 1, `fail_count` 1, only `high_blockers_open`: `12 open blocker/high: R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362`.
5. Gate 5: `open_finding_ids` over `.agent/live_review.md` — `89`.
6. Gate 6: `git diff --stat 646c4b1d7 HEAD -- packages/orchestration/review_zip.py` — no output.

## Authored-text proofs

C1: the five prepared `c1-` files are byte copies, proven equal by sha256 at copy time and again by `verify.py`. C2 to C4 are the worker's own code and tests.

## Deviations & assumptions

- The verifier reports a bundle that is a ZIP by its header but fails to open or read (a damaged archive) as `<path> could not be read as a ZIP archive: <reason>`, instead of raising; the block names no sentence for it.
- A manifest larger than the cap is refused with `manifest.json holds <n> bytes, more than the <cap> bytes a manifest may hold; it is not read.`; the block names no sentence for it.
- A manifest value check (`bundle_v`, `kind`) runs only when the key is present, so an absent key yields the single "lacks the key" sentence and not a second one. `bundle_v` must be a real int, so `true` is refused.
- A `members` or `referenced` field that is not a list is reported as `<field> entry 0 is malformed.`
- `cost_claims_from_member` passes `first_running_at` to the decoder only when it is a string.
- In the tamper matrix the "manifest" case rewrites one member's hash in the manifest while the member stays, since the manifest's own bytes are hashed from the file read and cannot disagree with themselves.
- The claim check runs only when the manifest and integrity checks found nothing, per DECISION F060 D3, so a `terminal_state` of `running` yields two sentences (not a terminal state; the report does not name it).
- No mutation red-proofs and no full-suite run, as the block orders.

## Next

1. Phase 1 rule 1: `.agent/STOP`.
2. Phase 1 rule 2: the Open PR Gate.
3. Book round 3's verdict in the next round's first commit.
4. Round 4: the two commands, the standalone check and the page.

Operator questions open: 3.
Open findings: 89.

## For the operator, in plain sentences

The certificate work can now check a certificate. Given a certificate file, Remedy first confirms that every member inside is exactly what the certificate says it is, and that nothing was added or taken away. Only then does it check that the statements the certificate makes agree with the members they come from: how the run ended, what it cost, how many checks passed and the regression status. A report or a cost figure that was edited together with its fingerprint is still caught, because the statement no longer matches the member. The result is a short plain verdict that says first how the run ended and second whether the certificate is intact, and it always repeats that a certificate proves integrity and not who made it. An earlier finding about a test that did not hold the right numbers was repaired. Nothing yet lets you run this from the command line; that comes in the next round. The tests chosen for this round ran and passed, and the one known set of open serious findings is unchanged. Three questions still wait for you.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `a43bed5aa` |
| C2 | done | `a4edfe946` |
| C3 | done | `ae89a7639` |
| C4 | done | `b2f069785` |
| C5 | done | this commit |
| Gate 1 | done | `ALL True` |
| Gate 2 | done | `All checks passed!` |
| Gate 3 | done | exit 0, 3497 passed, 2 skipped |
| Gate 4 | done | `fail_count` 1 (`high_blockers_open`, twelve findings) |
| Gate 5 | done | 89 |
| Gate 6 | done | no output |
