# Context — operator order fix1022-review-findings

## Active Branch
`feature/fix1022-review-findings`, from `main` after the Open PR Gate merged pull request 380
(F074).

## Scope
The four findings of the orchestrator's review of F310 to F074, as the operator order
fix1022-review-findings states them: R-1422 to R-1425. Nothing else.

## Do not touch
`pingpong_loop.py`, `pingpong_provider.py`, `role_provider_factory.py`, `do_sequence.py` and
`pingpong_provider_fake.py` for typing (their mypy errors are F314's, R-1425).

## Active assumptions
- Every behaviour change lands with a test committed red first.
- mypy repairs change no behaviour.

## Constraints
- Under 500 insertions per commit; commit subjects carry no leading-slash tokens.
- No ratchet or ceiling raised by hand; no assertion weakened.
