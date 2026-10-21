## F060 — Long-run certificate

### What changed
- `remedy job certificate <job-id>` writes one small ZIP for a job that has ended (blocked,
  cancelled, completed, failed or stopped): its final report, cost record, Definition of Done
  result, the evidence export's token truth, verifier report and ownership record, the run manifest,
  and, while the size budget allows, its diff and run logs. A `manifest.json` names every member by
  sha256 and size and states six claims; a member the budget leaves out is referenced by its hash,
  size and where to fetch it. An existing file is never overwritten, and each certificate of a job
  gets the next issue number.
- `remedy verify <bundle>` checks a certificate on any machine, with no data folder and no
  checkout: the manifest's shape, every member against its hash and size, the budget, then every
  claim against the member it is derived from, so a report or cost changed together with its hash
  is still caught. Its verdict says first how the run ended, then whether the certificate is
  intact, and names the member of every problem. It exits 0 when intact and 1 when not.
- New modules: `packages/orchestration/job_certificate.py` (the profile),
  `job_certificate_sources.py` (a finished job's members and claims),
  `job_certificate_claims.py` (the claims from a member's bytes) and `job_certificate_verify.py`
  (the verifier); `apps/cli/command_catalog_certificate.py` and
  `apps/cli/commands/certificate_cmd.py` (the two commands). The page
  `docs/system/job-certificate-v1.md` says what a certificate is and is not.

### Why
The roadmap's F060: a finished run should be able to prove itself to someone who was not there,
with integrity proven and claims cross-checked, and honesty about failed runs included.

### Key decisions (`.agent/decisions.md`)
- D1: the review package's own packer and reopen check, `build_review_zip_from_snapshot` and
  `verify_review_zip`, are reused unchanged; a profile parameter on the shell driver was not taken,
  because it needs a checkout.
- D2: five terminal states; the report is rendered in memory when the saved one is missing or
  stale; the budget is 8 MiB or `--max-bytes`, not a configuration key, because `config.py` is at
  its structure-ledger limit.
- D3: the claims are derived from member bytes by one set of functions shared by builder and
  verifier; integrity is checked before claims.
- D4: `verify` is a hidden group whose bare form takes the bundle; the catalog entries live in their
  own module, and `command_catalog.py` keeps its 2314 lines.
- D5: the ledger rotation is skipped for the reason of DECISION F310 D8.

### How to review and test
- `python3 -m pytest -q tests/orchestration/test_job_certificate.py tests/orchestration/test_job_certificate_sources.py tests/orchestration/test_job_certificate_claims.py tests/orchestration/test_job_certificate_verify.py tests/cli/test_certificate_cmd.py`
- The tamper matrix is `tests/orchestration/test_job_certificate_verify.py`; the standalone check
  (a fresh folder, a data folder that does not exist) is in `tests/cli/test_certificate_cmd.py`.

### Verification (local; hosted CI is manual under operator amendment amend1011-manual-hosted-ci)
- The one full suite on `3b0db49b0`: `python3 -m pytest -n auto -q`, Python 3.10, exit 0,
  `22947 passed, 11 skipped, 1 warning in 337.96s` (`.agent/authored/f060-closure-suite.txt`).
- The evidence job `f060r6e1001` at `c9b3cbc4b82312d9c3c2b5180ced6dbb45673a08`: 10969 passed, 0 failed,
  6 skipped; package `remedy-review-20261021-150936-READY_FOR_REVIEW.zip`, SHA-256
  `97f5c525bc0d5a06a9935df49fbc999ea26913d8789c047561ac86aff4569cec`.
- Latest verdict: PASS (round 6); live review PASS_WITH_RISKS — the integrity check fails only on
  twelve High findings other features own (DECISION F310 D7).
- Findings: R-1404, R-1405 and R-1406 raised and resolved inside the feature; open findings 88.

### Runtime actuals
- One session, seven delegated rounds; reviewer on Claude Opus 5.5, workers on Claude Sonnet 5.
- The closure's self-use run SU-071: 2 provider calls, 57.5 seconds, never applied.
- Session token totals: not measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
