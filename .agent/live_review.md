# Live Review — Steps 14161-14360 — F012 Final Publication & Token-Contract Repair Round 33

## Verdict (reviewer-owned)
**PENDING** — F1/F2/F3/F4 closed this round; every accepted Round-32 authority contract
(final-verifier reproducibility, total gate eval, git-status snapshot, patchset identity, integration
termination, manual token-truth regeneration/equality) preserved. Not externally accepted.

## Process inspection (mandated first action)
`ps -eo pid,pgid,etime,args` filtered for `make_review_zip`, `build_review_zip`, `build_review_manifest`,
`build_r3?_evidence`, `pytest`, `remedy`: **no review-owned processes running**. Nothing obsolete to
terminate; no process group killed (no broad Python/Bash/Remedy kill performed).

## Builder Handoff

Operator-built by hand: no Builder, no Reviewer, no provider GENERATION call (0), no Fable, no
subagents, no Evidence `job-flow`/`job-run`, no Docker, no new dependency, **no database**, **no
LLM rerun**, no network. Every accepted Round-32 contract preserved.

External review of `remedy-review-20260719-215803-READY_FOR_REVIEW.zip` (SHA `3149a10e...7b64`,
Evidence `453aab97e0fc3b01`, prior `2d1e749dcff40512`, base `fbbd584`, HEAD `13cd5a5d`) accepted the
authority block and returned four bounded findings.

### Closed this round
- **F1** — `safe_publish.publish_atomically` is the ONE publication primitive and is really used:
  `build_review_zip.py` builds into a private `.remedy_zip_*.part` temp, verifies, then links it into
  place; `make_review_zip.sh` publishes the status-bearing name through the same primitive (no `mv -n`).
  `os.link` fails `FileExistsError` if the destination exists → exactly one of N concurrent publishers
  wins, losers raise `PublishCollisionError`, published bytes preserved; the builder no longer unlinks
  `out_path`. (F1 and F2 share the `safe_publish` primitive and were committed together — 24e6f66.)
- **F2** — `git_tracked_status` runs `git ls-files --error-unmatch -z --` and returns typed
  {TRACKED|UNTRACKED|GIT_FAILED|GIT_UNAVAILABLE|GIT_TIMED_OUT}; only UNTRACKED proceeds. A git exit 128
  (non-repo), missing binary, or timeout blocks — never silently "untracked".
- **F3** — `token_truth` exposes the canonical schema constants; `token_authority` imports them and the
  supported `measurement_source` enum is exactly what `build_token_truth` emits
  (`character_heuristic`/`provider_actuals`/`mixed_provider_actuals_and_heuristic`), plus the
  confidence↔source coherence pairing (67bcff3). A parallel per-task drift (`repair_attest`
  token_accounting missing `provider_call_count: 0`, pre-existing since round 32) was fixed the same
  way (50c2098).
- **F4** — `job_evidence.create_manual_completion_bundle` is the real operator entry that builds a
  complete manual bundle end-to-end THROUGH `write_manual_completion_evidence`; the source-inspection
  test is replaced by an execution test in a temporary git repository (fc030c2).

## Verification

- New/affected suites pass: test_review_atomic_publish, test_review_no_clobber_publish,
  test_review_manual_completion_shapes, test_manual_completion_bundle, test_token_producer_validator_compat,
  test_token_authority, test_review_token_truth_authority, test_repair_attest,
  test_review_authoritative_e2e, test_review_package_full_integration, test_do_job_flow, and the docs
  pins (TestF012Round33IsPinned). The full acceptance matrix is re-run before packaging; counts recorded
  in verification_tests.json.

## Status

F012 `[~]` — not externally accepted. F017 `[ ]` not started. Branch locally committed, unpushed,
unmerged. Authority: staged Evidence bytes → real producers → regenerated final verifier + token truth
→ gates → archive plan → immutable atomically-published ZIP; a supplied final-verifier/token-status
JSON is never authority.
