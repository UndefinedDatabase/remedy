── STEP T003 repair / R7 — F057 Rate-limit-aware scheduler ───────────
Round base — the SHA every range gate in this block measures from: 3ab9d964

Goal:  Persist the R6 verdict and its two findings, then close both. R-0372 is
       a missed call site; R-0373 is the one that matters — a bare rate-limit
       error never reaches the seam at all, so the feature is currently inert
       for exactly the signals it exists for.

Bundle — one commit each, in this order, pushed after EVERY commit:
  C0a  save this block verbatim  -> .agent/authored/f057-r7.md
  C0b  point last_block at it    -> .agent/last_block.md
  C1   R6 verdict, R-0372, R-0373 -> .agent/live_review.md   (FIRST, alone)
  C2   R-0372 fix: the third call site -> packages/orchestration/pingpong_loop.py
  C3   R-0373 fix: a rate limit is retryable AT THIS SEAM
       -> packages/orchestration/pingpong_loop.py
       + tests/orchestration/test_provider_retry.py
  C4   handback -> .agent/plan.md, .agent/handoff.md

C1 — .agent/live_review.md, APPEND ONLY at the end of the file
  Append the three slices below in this order, each separated from its
  neighbour by exactly one blank line. APPEND-shaped: nothing already on disk
  is edited, moved or deleted. Each slice is ONE physical line, matching the
  file's existing shape. Do NOT write a `Done:` paragraph of your own — `Done:`
  is reviewer-authored only (docs/agents/planner_reviewer_prompt.md §4 item 4).
  This commit lands BEFORE any code change, so nothing is lost if the session
  dies mid-round.

C2 — R-0372: pace the third call site
  `grep -n "_call_with_retry(" packages/orchestration/pingpong_loop.py` returns
  four hits: the def, and THREE call sites — the builder attempt, the reviewer
  attempt, and the reviewer PARSE-RETRY call. The R6 block said "BOTH call
  sites" and only two were wired; the parse-retry site is the one unpaced
  provider call left in the loop. Pass `rate_governor=_rate_governor` there
  too — the same single per-run instance, never a second one. That is the whole
  change: one keyword argument, no other line moves.

C3 — R-0373: make a rate limit retryable AT THIS SEAM, and only here
  The defect, proved by the reviewer at 3ab9d964:
      '429 Too Many Requests'  -> is_timeout=False, is_nonzero=False,
                                  should_retry=False, is_rate_limit_error=True
  `_call_with_retry` returns on `not should_retry(...)` BEFORE the retry body,
  and the retry body is where the governor's `observe` and `acquire` live. So a
  bare rate-limit error never reaches the governor, no cooldown is ever created,
  and the first-call pacing has nothing to pace. The R6 tests pass only because
  their fixture error also carries "exited 1", which `is_nonzero_exit_error`
  already accepts — the R6 test file says so in its own comment.

  The change, in `_call_with_retry` and NOWHERE else:
  - `is_rate_limit_error` is already exported by
    `packages.orchestration.rate_governor`; add it to the existing import.
  - Beside the existing `is_timeout` / `is_nonzero` / `is_reject` predicates,
    compute whether this error is a rate limit — but ONLY when the governor is
    active for this call, i.e. `rate_governor is not None and provider`. When
    it is not, the value is False and every pre-F057 caller keeps byte-identical
    behaviour, which is what the 294-test regression gate proves.
  - Change the retry DECISION so the call is retried when `should_retry(...)`
    says yes OR when it is a rate limit — except that a review reject
    (`is_reject`) is NEVER retried, exactly as today. `should_retry` already
    returns False for a reject, so state the reject exclusion explicitly rather
    than relying on it.
  - Do NOT touch `packages/orchestration/provider_timeouts.py`. The per-call
    retry policy is on the feature file's Do-not-touch list; this precedence
    rule belongs to the seam, and the comment above it says so in one line and
    names R-0373.
  - The retry stays bounded: `next_backoff(attempt)` still returns None past the
    last attempt and still returns `out`. A permanently rate-limited provider
    exhausts MAX_RETRIES and fails, it does not loop.

  Tests, added to the F057 section of tests/orchestration/test_provider_retry.py,
  each @pytest.mark.unit and named after the property:
   1. a BARE rate-limit error — use the literal `429 Too Many Requests`, which
      carries no "exited" and no timeout wording — is now retried when a
      governor and a provider are present: the call happens twice, one wait is
      recorded on `result.rate_limit_waits`, and the run succeeds;
   2. the same bare error with `rate_governor=None` is still NOT retried: one
      call, `retries_used == 0`, behaviour identical to before this round;
   3. a review reject is still never retried even when the governor is active —
      build the reject the way the existing tests in this file build one, and
      assert the call count stays 1.

C4 — handback
  Apply the PLAN slice as the COMPLETE new .agent/plan.md, then rewrite
  .agent/handoff.md per docs/agents/handback_template.md.

Constraints
  - Never work on main; never force-push; no PR this round.
  - Do-not-touch: packages/orchestration/provider_timeouts.py and
    packages/orchestration/stream_evidence.py stay byte-identical.
    pingpong_loop.py is the only production file that may move.
  - Repository-wide `ruff check` is RED at base with 26 pre-existing errors and
    is NOT a gate; ruff is gated SCOPED to the files this round touches, where
    the reviewer measured `All checks passed!`, exit 0, at 3ab9d964.
  - No gate below asserts a predicted insertion/deletion pair (R-0367), and no
    text this block orders written into a file contains a value that does not
    yet exist when it is written (R-0371): every SHA and every numstat belongs
    in the HANDBACK, never in a committed line.
  - Count gates state their anchoring (R-0369) and are reported in both
    readings where both are named.
  - If `.agent/STOP` appears at any point, finish the commit in flight, write
    the handoff, and stop.

Done when — every command below was executed by the reviewer at 3ab9d964
before this block was emitted (R-0364), and the baseline it produced is stated
inline so no gate asks for an unreachable condition.
  1. `git status --porcelain` -> empty. Baseline: empty.
  2. `git worktree list` -> exactly one line. Baseline: one line.
  3. `git branch --show-current` -> feature/f057-rate-limit-scheduler.
  4. `cmp .agent/authored/f057-r7.md .agent/last_block.md` -> exit 0. Report the
     shared sha256 and the line count.
  5. In .agent/live_review.md, LINE-ANCHORED (`^` at line start):
     `^Gate: R6 — PASS` = 1, `^- R-0372 — ` = 1, `^- R-0373 — ` = 1,
     `^## Steps` = 1. Also report the whole-file SUBSTRING count of `## Steps`
     and whether it changed from 6, the value the reviewer measured at 3ab9d964.
     A change is not a failure; an unreported change is.
  6. `git show --numstat <the C1 sha> -- .agent/live_review.md` -> report both
     numbers. The only ordered property is that the deletion column is 0.
  7. `python3 -m pytest tests/orchestration/test_provider_retry.py -q` -> 0
     failed. Baseline at 3ab9d964: `26 passed`. Report the new total; it grows
     by C3 and the reviewer re-measures it, so do not predict it.
  8. `python3 -m pytest tests/orchestration/test_rate_governor.py -q` -> 0
     failed. Baseline: `59 passed`. This file is not touched; report any change
     to the total as a finding candidate.
  9. The four regression files, run together:
        python3 -m pytest tests/orchestration/test_job_budgets.py \
          tests/orchestration/test_stream_evidence_integration.py \
          tests/orchestration/test_failure_wiring.py \
          tests/orchestration/test_budget_stop_integration.py -q
     -> `294 passed`, exit 0. The reviewer measured exactly that at 3ab9d964, so
     any other number is C3 changing behaviour it must not change. This is the
     gate that proves the pre-F057 path is untouched.
 10. `python3 -m ruff check packages/orchestration/pingpong_loop.py
     tests/orchestration/test_provider_retry.py` -> `All checks passed!`,
     exit 0. Baseline: both already clean.
 11. Canary `python3 -m pytest tests/cli/test_golden_path.py -q` -> 0 failed.
     Baseline: `42 passed`.
 12. `python3 -m pytest tests/ui_server/test_dashboard_contract.py
     tests/regression/test_resource_safety.py
     tests/orchestration/test_test_runner.py -q` -> `142 passed`, exit 0.
     Baseline measured by the reviewer at 3ab9d964.
 13. `wc -l < .agent/plan.md` -> under 50 (AGENTS.md).
 14. `grep -n "_call_with_retry(" packages/orchestration/pingpong_loop.py` ->
     report every hit and, for each of the three CALL sites, whether it now
     passes `rate_governor=`. All three must.
 15. `git diff --name-only 3ab9d964..HEAD` -> report the real list. Every path
     on it must be one this block named: .agent/authored/f057-r7.md,
     .agent/last_block.md, .agent/live_review.md,
     packages/orchestration/pingpong_loop.py,
     tests/orchestration/test_provider_retry.py, .agent/plan.md,
     .agent/handoff.md. Any other path is a finding.
 16. Do-not-touch: `git diff --stat 21c8148e..HEAD --
     packages/orchestration/provider_timeouts.py
     packages/orchestration/stream_evidence.py` -> EMPTY output.
 17. RED-PROOF, in a disposable worktree under .remedy-wt/ and NEVER in the
     primary checkout. Prove the import path resolves INSIDE the worktree
     before trusting any colour — note that a bare `python3` there may import
     the PRIMARY checkout through the editable install, which nearly bit R6;
     run under pytest from inside the worktree and confirm. Run these as
     PROBES, reporting which tests fail and the exact assertion rather than
     confirming a colour this block predicts:
       (i)   revert the C3 retry decision to plain `should_retry(...)`;
       (ii)  drop the `rate_governor is not None and provider` guard from the
             C3 predicate, so a rate limit is retried even with no governor;
       (iii) remove `rate_governor=` from the C2 parse-retry site.
     If (iii) kills no test, say so plainly — an untested wiring change is a
     real gap and the reviewer wants to know, not to be reassured.
     Remove and prune the worktree afterwards; gate 2 is the proof it is gone.

Handback: a completion report plus a rewritten .agent/handoff.md carrying the
  per-commit changed-files table, the item-status table (C0a, C0b, C1, C2, C3,
  C4 — each exactly once, done / skipped / deviated), the slice sha256 table,
  the REAL output of all 17 gates, the open-findings count and the next
  expected action. If the handoff exceeds 60 lines, carry the DECISION D15
  stated-cause line naming its real length and the mandated content that caused
  it, and drop no section. This is the session's LAST round under its declared
  cap, so the handoff is the only return channel: name Phase 1 rule 1 of
  docs/agents/self_drive_protocol.md — re-read `.agent/STOP` from disk — as the
  next session's first action, BEFORE rule 2, the Open PR Gate.

--- BEGIN SLICE GATE-R6 ---
Gate: R6 — PASS. Verification tier: round gate plus canary. Every value was re-measured by the reviewer against the disk, never read out of the handback: `tests/orchestration/test_provider_retry.py` and `tests/orchestration/test_rate_governor.py` together → `85 passed`, which is the 26 and the 59 the worker reported separately, 0 failed; the four regression files the seam must not disturb → `294 passed in 38.96s`, exit 0, unchanged from the baseline the reviewer measured at 33fab24e before the block was emitted; `python3 -m ruff check` over `pingpong_loop.py`, `rate_governor.py` and `test_provider_retry.py` → `All checks passed!`, exit 0; the canary together with the three `.agent` contract readers → `184 passed`, which is 42 plus 142; `cmp .agent/authored/f057-r6.md .agent/last_block.md` → exit 0, shared sha256 `c5dfac96f25f5a995d2ef118631d17a6123cdbb59bad5702a4fe26b0e4d7f6be`, 385 lines, inside the 400-line cap; `wc -l` → `.agent/plan.md` 35, `.agent/handoff.md` 137 with its DECISION D15 stated-cause line and no section dropped. C1 measures `6 0`, insertions only. Line-anchored counts in `.agent/live_review.md`: `^Gate: R5 — PASS` 1, `^- R-0371 — ` 1, `^Done: R-0370 — ` 1, `^Landed: R-0370 —` 1, `^## Steps` 1. The whole-file substring `## Steps` moved from 5 to 6 because the GATE-R5 slice reports its own line-anchored count and therefore contains the literal; the worker measured that, reported it, and named the cause — which is precisely what R-0369's counter-measure was written to produce, so the counter-measure worked and no finding is registered for it. The change set is exactly the nine paths the R6 block named — `git diff --name-only 33fab24e..HEAD` lists no tenth — and the Do-not-touch diff over `provider_timeouts.py` and `stream_evidence.py` at `21c8148e..HEAD` is EMPTY. The RED-PROOF was reproduced by the reviewer in its own disposable worktree at `3ab9d964`, with a NARROWER mutation than the worker's on purpose: deleting only `if not _acquired.granted: return out` and keeping the acquire gives `1 failed, 25 passed`, the single id being `test_stop_during_the_wait_ends_the_call_without_counting_a_retry` asserting `2 == 1` on the call count. That the mutated behaviour appeared at all is itself the import-path proof the R-0337 class asks for: an import that had resolved to the primary checkout would have passed. The worktree was removed and pruned; `git worktree list` is one line and `git status --porcelain` is empty at this verdict. The seam itself was read line by line rather than inferred from the tests: the first-call acquire records and never branches, the retry block observes before it acquires and sits BEFORE `result.retries_used`, so a stop during a wait leaves the counters exactly where the pre-existing stop probe leaves them, and every insert is guarded by `rate_governor is None` or a falsy provider, which is why the 294 regression tests cannot move. No block condition was hit: no fabricated value, no false live indicator, no missing changed-files table, no unverified completion claim, and no silent scope change — the one scope deviation was declared before review, in the handback, with its reason. Two findings, both registered below and neither charged to the round: R-0372, the reviewer's own miscount of the call sites, which the worker caught by reading the code instead of the block; and R-0373, which the worker's own test comment states as a fact and which no gate in the R6 block could have caught, because every gate in it was green for the right reasons.
--- END SLICE GATE-R6 ---

--- BEGIN SLICE FINDING-372 ---
- R-0372 — Low — a block ordered a change at "BOTH" call sites of a function that has three. The R6 block's item (g) told the worker to pass the run's single governor "to BOTH `_call_with_retry` call sites — the builder site and the reviewer site". `grep -n "_call_with_retry(" packages/orchestration/pingpong_loop.py` returns four hits at `3ab9d964`: the definition, the builder attempt, the reviewer attempt, and the reviewer PARSE-RETRY call. The worker wired the two the block named, refused to wire the third because the same block said "Nothing else in this file changes", declared the deviation in its handback before review, and pointed at the evidence — `.agent/f057_t003_seam_inventory.md` names all three call sites itself, in its section 3, which is the very document the block cited as the round's evidence base. So the reviewer had the correct count in front of it, in its own ordered artifact, and wrote a smaller number anyway. The consequence on disk is real but small: the parse-retry provider call is the one call in the loop that is not paced, so a run that is being throttled can still fire an unpaced parse retry at the provider it is currently waiting out. This is not the R-0364 family — the block's gates were all reachable and all ran green — it is a reading defect, and its counter-measure is different in kind: when a block orders a change at "every" or "both" call sites of a symbol, the reviewer runs the grep that enumerates them and writes the resulting COUNT into the block, so the worker can check the reviewer's arithmetic instead of inheriting it. Fixed in this round's C2. OPEN until that fix is verified.
--- END SLICE FINDING-372 ---

--- BEGIN SLICE FINDING-373 ---
- R-0373 — Medium — the seam this feature exists for is unreachable for the signals it exists for. `_call_with_retry` returns early on `not should_retry(...)`, and the retry body BELOW that return is where R6 put the governor's `observe` and `acquire`. The reviewer measured the predicates directly at `3ab9d964`: for `'429 Too Many Requests'`, `is_timeout_error` is False, `is_nonzero_exit_error` is False and therefore `should_retry` is False, while `is_rate_limit_error` is True and `classify_rate_limit_reason` returns `rate_limited`; the same holds for `'rate_limit exceeded for this key'` and for `'overloaded_error: server is overloaded'`. So a provider that answers with a plain rate limit is not retried, the governor never observes it, no cooldown is ever created, and the first-call pacing has nothing to pace — the whole T003 seam is inert unless the provider's wording happens ALSO to carry a nonzero-exit or timeout marker. The R6 tests are green for a real reason and not a false one: their fixture error is `provider_error: RuntimeError: claude CLI exited 1: rate_limit exceeded for this key`, which `is_nonzero_exit_error` accepts, and the R6 test file states the constraint in its own comment above that constant — "A bare rate-limit wording never reaches the retry path at all, because should_retry declines it before the governor is consulted". The worker therefore documented the gap accurately and built exactly what the block ordered; the gap is the block's, which never named the precedence question even though the round's own `.agent/plan.md` text raised it and then dismissed it with the words "nothing is contradicted today" — true, and beside the point, because the failure mode is not contradiction but unreachability. Against the feature file this is a DONE-condition miss, not a nicety: the Acceptance section requires a limit-emitting fixture to produce zero failed tasks with waits in evidence, and a fixture emitting a bare 429 today produces a failed task and no waits. Fix in this round's C3: at THIS seam and not in the transport policy, a rate-limit error is retryable unless it is a review reject, guarded so that the pre-F057 path — no governor, or no provider — keeps byte-identical behaviour. That guard is what makes the fix provable: the 294-test regression gate cannot move. OPEN until that fix is verified.
--- END SLICE FINDING-373 ---

--- BEGIN SLICE PLAN ---
# Plan — F057 Rate-limit-aware scheduler

Branch: feature/f057-rate-limit-scheduler, cut from main at 21c8148e. Next free
finding id: R-0374. Open findings: R-0361, R-0362, R-0363, R-0364, R-0367,
R-0368, R-0369, R-0371, R-0372, R-0373 — R-0365, R-0366 and R-0370 are resolved.
R-0372 and R-0373 are fixed on disk this round and stay OPEN until a reviewer
verdict closes them; only reviewer-authored text may.

## Goal
Provider rate limits stop looking like failures. A per-provider governor reads
normalized limit signals out of call evidence and makes a run WAIT visibly —
with a reason and an expected retry — instead of burning retries or failing the
task. Providers that emit no limit signal behave exactly as today.

## Current Step
T003 repair. The governor is wired at all THREE `_call_with_retry` call sites,
and a rate-limit error is retryable at that seam so the governor is actually
reached — without touching the transport policy in provider_timeouts.py, which
the feature file forbids.

## Next Steps
1. T003 part 2, the report surfaces: `rate_limit_waits` in
   `export_pingpong_json`, the "waited Ns on provider rate limits this run"
   line in `summarize_pingpong` from `total_waited_s`, and the limit-emitting
   fixture end-to-end the feature's Acceptance section requires — the fixture
   should emit a BARE rate limit, which is what R-0373 made reachable.
2. Integration gate per docs/agents/integration_gate.md, then closure per
   docs/roadmap/STATUS_closure_protocol.md.

## Risks
- The seam now decides retryability for one error class. The 294-test
  regression gate is what proves the pre-F057 path did not move; run it on
  every round that touches `_call_with_retry`.
- A permanently rate-limited provider now consumes MAX_RETRIES instead of
  failing at once. That is the intended trade, and `next_backoff` still bounds
  it, but the report line in part 2 is what makes the cost visible.
--- END SLICE PLAN ---
──────────────────────────────────────────────────────────────────────
