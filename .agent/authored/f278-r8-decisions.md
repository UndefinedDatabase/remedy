
DECISION F278 D7 (2026-09-23, round 8) — BLE001 IS ON: WHAT IT COVERS, WHAT IT EXCUSES, AND THE
RATCHET THAT HOLDS THE EXCUSES.

CONTEXT. After rounds 5 to 7, 82 blind handlers remained under `packages/`, `apps/` and
`scripts/`, measured at `2537a4ae` with `ruff check --select BLE001`, and `tests/` held 13 more.
DECISION amend0911-feedback D7 requires `ruff check .` to report zero findings at every commit.

CHOSEN. (1) R-1037 and R-1038 are repaired first, each in its own commit with its test: a
plan's budgets or fences that fail to validate now refuse the order through a new
`do_sequence.order_job_limits`, and `review_subject._metadata_is_safe` answers False when its
scanners raise. (2) One handler is NARROWED rather than excused:
`hunk_decision_record._parsed_decision_stamp` wraps `datetime.fromisoformat` alone, and its own
docstring names `TypeError` and `ValueError` as the two failures it means. (3) The rest are
marked in two comment-only commits; the three marks that carried no reason gain one, and two
older marks that wrote their reason after a hyphen are rewritten with the em dash the ratchet
reads. (4) THE ENABLEMENT COMMIT adds `BLE001` to `select` in `pyproject.toml` and to the
`tests/**` per-file ignores — a test may catch anything in order to assert on it — and adds
`tests/test_ble001_ratchet.py`, which requires a reason after ` — ` on every
`noqa: BLE001` under `packages/`, `apps/` and `scripts/`, requires `BLE001` to stay selected, and
holds the count of excused handlers EQUAL to `MAX_EXCUSED`, 290 at this commit: a new excuse fails
it, and so does a removed one until the number is lowered in the same commit. With the rule on,
`ruff check .` over the whole tree reports zero, which CI's budgets stage and D7 require.

ALTERNATIVES. Turn the rule on for `tests/` too — rejected: a test that catches everything to
assert on the exception is the one place a blind handler is the point. Hold the count with `<=`
only — rejected: a count that may silently fall is a ceiling that drifts upward the next time a
mark is added back.

REVERSE by deleting this paragraph, removing `BLE001` from `select` and from the `tests/**` line,
and deleting `tests/test_ble001_ratchet.py`; the marks are inert without the rule.
