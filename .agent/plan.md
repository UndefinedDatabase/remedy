# Plan — F105 Cache-optimal prompt ordering (CLOSED)

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245.
Next free finding ID: R-0270.

## Goal
Every prompt composes from REGISTERED SEGMENTS ordered by stability — system
and conventions first, task and steering last — every call records a segment
manifest (name, rank, hash) into evidence, and `remedy stats cache` shows the
cache-read share per role from actuals. Prompt CONTENT does not change.
REACHED: T001, T002, T003 and T004 are ALL DONE.

## Current Step
F105 is CLOSED. `docs/roadmap/STATUS.md` carries the `[x] F105` line, accepted
2026-08-12 as PASS_WITH_RISKS — ACCEPTED, and README.md agrees with the ledger.

- Accepted HEAD: b928a0c691dc0a2b86c149a5e732ea07ac03176e
- Evidence job: f105-closure
- Package: remedy-review-20260812-092055-READY_FOR_REVIEW.zip
- SHA-256: 23b21bc171b0de493ca4db50c472ecb2797b58b5c870ff9aa5d9b5da71536840

The reviewer re-ran verification ITSELF rather than reading a handback: the
full suite returns 16462 passed, 19 skipped, 0 failed, and
`python3 -m apps.cli.grouped integrity check --json` returns `"passed": true`
with 5 of 5 checks.

Seven residual risks stay OPEN — the documented set F105 closes on: R-0221,
R-0239, R-0247, R-0262, R-0268 (Low); R-0265, R-0266 (Medium). No High finding
is open. R-0262/0265/0266/0268 are producer- or protocol-side, not F105's, and
R-0221 will cost any future gate the same phantom base-only failures.

One closure CANDIDATE is recorded in `.agent/candidates.md`: the review zip
packages the gitignored `.remedy-wt/` scratch tree. The next feature's first
reviewed round must register or resolve it.

DECISION D16 records why the AGENTS.md Open PR Gate does not block this
closure PR.

## Next Steps
1. The closure PR is UNMERGED BY DESIGN. It merges at the NEXT feature's start
   via the Open PR Gate; that gap is the operator's manual-review window. The
   operator may merge it manually at any time.
2. PR #189 (`docs/amend0810-clerical` -> `main`) remains the OPERATOR's: it is
   non-`feature/*`, therefore stop-and-report. Not merged, not commented on,
   not modified.
3. The next feature by Rule A5 is F107 — Context compiler v2.
