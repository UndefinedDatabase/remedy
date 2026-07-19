# Plan — Steps 14361-14560 — F012 Single-Publication & Complete Token-Truth Closure Round 34

Reviewed `remedy-review-20260719-230022-READY_FOR_REVIEW.zip` (SHA `d67895bb...c03cbc`, Evidence
`b95cde870e6863ad`, prior `453aab97e0fc3b01`, base `13cd5a5d`, HEAD `d822df9d`). Accepted and preserved:
direct-Python private-build→verify→atomic publication, fail-closed `git_tracked_status`, shared
producer/validator measurement-source enums, executable `create_manual_completion_bundle`, FV
reproducibility, total gate eval, root git-status snapshot, patchset identity, full package integration
termination, current manual zero-provider Evidence + token-truth equality. Exactly two error classes,
non-overlapping. No broadening.

## Scope 1 — one private-to-final publication; no public intermediate ZIP

The shell still built a PUBLIC `remedy-review-<STAMP>.zip`, ran `rm -f "$OUT"` on it, then re-published
to the status name — a foreign untracked file at the intermediate path was deleted, and the first
public ZIP was mutable between Python verification and final publication.

- `build_review_zip.py`: accept a final-name TEMPLATE containing `{package_status}`. Determine
  `package_status` from the verified in-memory manifest, derive the exact final path, build into a
  private same-directory `.part`, reopen+verify, then `publish_atomically(private_part, final_path)` —
  the SAME verified inode. `verify_source` binds the private source's lstat regular-file identity + the
  verified SHA-256 before publication; a symlink/non-regular/other-filesystem private source blocks.
  Print the exact final path + final SHA-256 in the JSON result. All possible status final names are
  declared as generated outputs so the dirty-subject disposition never self-blocks.
- `make_review_zip.sh`: no public temp ZIP name; no `rm -f "$OUT"`; no `mv "$OUT"`; no second
  `publish_atomically`; no `_refuse_tracked_output` on a ZIP. Passes the template, trusts only the JSON
  result, does READ-ONLY post-publication checks against the exact returned final path, never
  republishes. Git/publication decisions use `safe_publish` only.
- `safe_publish.publish_atomically(..., expected_sha256=...)`: bind the verified private source hash so
  a post-verification pathname swap cannot alter the published package.

Tests (real `make_review_zip.sh`, not only the primitive): foreign intermediate/final path byte-identical;
tracked temp-like/final path byte-identical; symlink/FIFO/dir at either public path untouched + blocks;
shell contains no `rm -f`/`mv`/second publish of a public ZIP (static regression); no public intermediate
exists at any time; two same-timestamp shell runs → exactly one publishes; direct Python vs shell same
final path → exactly one wins; published SHA-256 == private verified SHA-256; pathname swap after
verification cannot change the final package; failure before publication leaves no public ZIP and no
`.part`.

## Scope 2 — complete TokenTruthV1 input + output semantics

Round 33 unified enums but did not implement the promised state invariants: the producer clamped/coerced
malformed provider fields (negative cache tokens, `actual>provider`, `cost>actual`), and the validator
accepted `actual_model_verified` without a model, `cost_coverage_complete` with null cost, etc.

- One typed input contract: a strict normalizer for provider_evidence/token_accounting consumed fields
  (exact type, non-null/nullable, integer-not-boolean, nonnegative, finite cost, enum, cross-field
  actual≤provider / cost≤actual). Malformed evidence raises a bounded `TokenEvidenceError` — never
  `int()`-coerced or clamped — so `build_token_truth` raises, `regenerate_token_truth` returns
  `(None, reason)`, `token_truth_authority = PRODUCER_ERROR`, `package_status = BLOCKED_EVIDENCE`.
- `build_token_truth`: consume only normalized inputs; stop clamping; set `actual_model_verified` only
  with a real model identity; emit output that satisfies every invariant.
- `validate_token_truth`: closed TokenTruthV1 field set (unknown field blocks) + full state invariants
  (counts real nonnegative ints incl. cache; estimated/actual sum identities; actual≤provider;
  cost≤actual; coverage flags ↔ counts; confidence ↔ coverage; cost_coverage_complete ↔ finite non-null
  cost; total_cost ↔ cost_call_count>0; cost_coverage_reason null iff complete; model_verified ↔ model
  identity; missing_reason/actual_missing_reasons ↔ coverage; per_task closed/typed/agree with aggregate).

Tests: valid producer states (zero-provider manual, provider-without-usage, complete actuals+cost,
complete actuals+missing cost, mixed, verified model, cache usage); blocked states (negative cache,
bool/float counts, verified-without-model, model-without-evidence, cost-complete-null-cost,
cost-with-zero-cost-calls, cost>actual, actual>provider, coverage-flag-inconsistent, high-with-incomplete,
mixed-with-complete/none, unknown field, malformed per_task); meta-regression: every valid producer
fixture validates, every malformed input fails before a TokenTruthV1 is accepted.

## Scope 3 — truthful Round-34 docs + operator state

Direct-Python atomic publication (round 33) accepted; round 33 did NOT remove the public shell
intermediate; round 33 unified enums but did not complete TokenTruthV1 state validation; round 34 closes
only these two. Do not claim publication closure until the real shell has exactly one private-to-final
publication. F012 `[~]`, F017 `[ ]`.

## Constraints (unchanged)

Zero provider calls; manual only; no job-flow/job-run/db/network/docker/new deps. Small local commits,
never amend/squash. No push/PR/merge/main. Do not start F017. Fresh Evidence linked `b95cde870e6863ad`
through the real operator entry, VERIFIED_EQUAL, git OK, single private-to-final publication, no public
intermediate; one READY ZIP; then stop.
