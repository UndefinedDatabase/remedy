# Handback — F060 round 1: F060 claimed, F141 round 11 booked, T001 the certificate profile landed

## Session

SESSION 1 of feature F060 · round 1 · rounds so far 1

Context self-assessment: this worker verified every prepared digest, made C1 by byte copy, wrote the profile and its tests itself, ran the one test run once, and wrote this handback with ample context margin left.

Fortschritt: ~20 % (claim, inventory and T001 landed · sources, verifier and commands open) — Schätzung

## Range

Review of `646c4b1d7`..`HEAD` on `feature/f060-long-run-certificate` (base: the merge commit of pull request 374 on `main`).

## Commits

### 840be0cbf F060 R1 C1: claim F060, book F141 R11, the inventory and DECISION F060 D1
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f060-r1.md` | 174/0 | this round's block, byte-saved for the authored-text proof |
| `.agent/f060_inventory.md` | 70/0 | the inventory of what F060 reuses and what it adds |
| `docs/roadmap/STATUS.md` | 1/1 | F060 claimed (`[ ]` to `[~]`) |
| `.agent/live_review.md` | 14/12 | re-headed; F141 round 11 booked |
| `.agent/decisions.md` | 17/0 | DECISION F060 D1 appended |
| `.agent/plan.md` | 16/13 | rewritten for F060 |
| `.agent/context.md` | 11/13 | rewritten for F060 |

### 14365874c F060 R1 C2: the job certificate profile, its manifest and its byte budget (T001)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/job_certificate.py` | 199/0 | new: constants, `CertificateSource`, `plan_certificate_members`, `render_certificate_manifest`, `build_job_certificate` |
| `tests/test_no_orphan_modules.py` | 2/0 | `ALLOWED_UNWIRED` entry for the new module |

### 6feff114c F060 R1 C3: goldens and the budget, overwrite and refusal tests of the certificate profile
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_job_certificate.py` | 249/0 | new: golden, determinism, budget, overwrite, 18 refusal cases, reopen problem, constants |

### C4 F060 R1 C4: handback (this commit)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | edited | this handback |

## External actions

- `git checkout -b feature/f060-long-run-certificate` on a clean `main` at `646c4b1d7`; the Open PR Gate had already run (no pull request open).
- `git push -u origin feature/f060-long-run-certificate` follows this commit; its outcome is reported in the session reply. No pull request was opened. No worktree was added or removed.

## Verification

Preconditions: `block.md` (174 lines, sha256 `1c801d47...ac1795`), `verify.py`, `run_selection.py`, `selection.txt` and `digests.txt` matched the prompt's sha256; all seven `c1-` files matched `digests.txt`. Start state: HEAD `646c4b1d` on `main`, `git status --porcelain` empty, no `.agent/STOP`. The saved block copy `.agent/authored/f060-r1.md` has 174 lines and sha256 `1c801d4735553277a3434deadb87836f04a4a2dea13e8dd4735576e1a5ac1795`, equal to `block.md`.

1. Gate 1: `git status --porcelain` empty; `python3 .remedy-wt/f060-r1/prep/verify.py .` — every line `True`, C4 `absent`, last line `ALL True`.
2. Gate 2: `python3 -m ruff check` over the three Python files C2 and C3 touched — `All checks passed!`
3. Gate 3: `python3 .remedy-wt/f060-r1/prep/run_selection.py . .remedy-wt/f060-r1-worker/selection-output.txt` — `paths 74`, `exit 0`, `3402 passed, 2 skipped in 27.08s`; no FAILED, ERROR or `process(es) behind` line; two SKIPPED lines (the D12 quarantine of the deleted reviewer agent file; install smoke is opt-in).
4. Gate 4: `python3 -m apps.cli.main integrity check --json` — exit 1, `fail_count` 1, only `high_blockers_open`: `12 open blocker/high: R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362`, the same twelve as before the round.
5. Gate 5: `open_finding_ids` over `.agent/live_review.md` — `88`.
6. Gate 6: `git diff --stat 646c4b1d7 HEAD -- packages/orchestration/review_zip.py` — no output.

## Authored-text proofs

C1: the seven prepared `c1-` files are byte copies, proven equal by sha256 at copy time and again by `verify.py`. C2 and C3 are the worker's own code and tests, not authored text.

## Deviations & assumptions

- The Session line carries the template's `rounds so far 1` suffix after the block's `SESSION 1 of feature F060 · round 1`.
- Gate 6 was run as `git -C . diff ...` from the primary checkout; gates 1, 3 and 5 ran from the checkout root with relative paths.
- Assumption: where the block leaves the wording open, the refusal for a missing parent folder reads `The folder for the certificate does not exist: <folder>`, and the other refusals name the offending value in a sentence of their own.
- No mutation red-proofs and no full-suite run, as the block orders.

## Next

1. Phase 1 rule 1: `.agent/STOP`.
2. Phase 1 rule 2: the Open PR Gate.
3. Book round 1's verdict in the next round's first commit.
4. Round 2: a finished job's sources and claims.

Operator questions open: 3.
Open findings: 88.

## For the operator, in plain sentences

Remedy has started a new piece of work: a certificate for a finished job. The certificate is a single archive that holds the files that show how the job ended, together with a list that names each file by its fingerprint and size and states what the job claims about itself. Large files such as a long diff or log are left out when the size budget would be exceeded, and the list then says where to fetch them and what fingerprint they must have. A certificate shows that its files are intact and agree with each other; it does not show who made it, and it says so in its own text. Remedy refuses to overwrite a certificate that already exists, and it reopens each new one and checks it before it appears. Nothing yet creates a certificate on its own; that comes in a later round. The whole test collection ran and passed, and the one known set of open serious findings is unchanged. Three questions still wait for you.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | branch created on `646c4b1d7` |
| C1 | done | `840be0cbf` |
| C2 | done | `14365874c` |
| C3 | done | `6feff114c` |
| C4 | done | this commit |
| Gate 1 | done | `ALL True` |
| Gate 2 | done | `All checks passed!` |
| Gate 3 | done | exit 0, 3402 passed, 2 skipped |
| Gate 4 | done | `fail_count` 1 (`high_blockers_open`, the same twelve) |
| Gate 5 | done | 88 |
| Gate 6 | done | no output |
