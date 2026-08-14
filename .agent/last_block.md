── STEP T003 part 1 of 2 / R6 — F057 Rate-limit-aware scheduler ──────
Round base — the SHA every range gate in this block measures from: 33fab24e

Goal:  Wire the governor into the ONE provider-call seam so a rate-limited
       provider makes the run WAIT instead of burning retries, and record every
       wait on PingPongResult. The report line, the JSON key and the
       limit-emitting fixture end-to-end are R7, deliberately NOT this round.

Bundle — one commit each, in this order, pushed after EVERY commit:
  C0a  save this block verbatim  -> .agent/authored/f057-r6.md
  C0b  point last_block at it    -> .agent/last_block.md
  C1   R5 verdict, R-0371, R-0370 resolution -> .agent/live_review.md
  C2   DECISIONS F057 D3, D4, D5 -> .agent/decisions.md
  C3   the seam                  -> packages/orchestration/pingpong_loop.py
  C4   seam tests                -> tests/orchestration/test_provider_retry.py
  C5   handback -> .agent/plan.md, .agent/context.md, .agent/handoff.md

C1 — .agent/live_review.md, APPEND ONLY at the end of the file
  Append the three slices below in this order, each separated from its
  neighbour by exactly one blank line. APPEND-shaped: nothing already in the
  file is edited, moved or deleted, and the existing `Landed: R-0370` line
  STAYS on disk with the authored `Done: R-0370` paragraph appended after it.
  Do NOT write a `Done:` paragraph of your own — the one below is
  reviewer-authored and is the only one
  (docs/agents/planner_reviewer_prompt.md section 4 item 4).
  Each slice is ONE physical line, matching the file's existing shape.

C2 — .agent/decisions.md, APPEND ONLY at the end of the file
  Append the DECISIONS slice below, preceded by one blank line. APPEND-shaped.

C3 — packages/orchestration/pingpong_loop.py, the seam
  This is production code. Read every function you touch in full first
  (AGENTS.md, File Editing Safety Rules). The seam inventory
  .agent/f057_t003_seam_inventory.md is the evidence for every line number
  below; it was written against 5de503c6 and no packages/ file has moved
  since, but RE-GREP each symbol before you edit and report any drift.

  (a) Import. Add to the module's existing top-level import block, after the
      `provider_timeouts` imports, in the order ruff I001 wants:
          from packages.orchestration.rate_governor import (
              RATE_SIGNAL_SOURCE_RETRY_REASON,
              ProviderRateGovernor,
              RateLimitAcquireResult,
              RateLimitWaitEvent,
              normalize_rate_limit_signal,
          )
      There is no import cycle: rate_governor imports stream_evidence, which
      imports prompt_trace and token_actuals and never pingpong_loop.

  (b) PingPongResult. Add ONE field directly below
      `    retry_reasons: list[str] = field(default_factory=list)`, with the
      one-line WHY above it (AGENTS.md, Code Discoverability):
          rate_limit_waits: list[dict[str, Any]] = field(default_factory=list)
      Every existing construction of PingPongResult uses keyword defaults, so
      a defaulted field breaks none of them.

  (c) One new module-level helper, directly above `def _call_with_retry(`:
      `_record_rate_limit_wait(result, acquired)` — takes the PingPongResult
      and a RateLimitAcquireResult, returns None, does nothing when
      `acquired.waited_s <= 0.0`, and otherwise appends
      `RateLimitWaitEvent(provider=..., waited_s=..., reason=...).to_json()`
      to `result.rate_limit_waits`. Build the dict THROUGH RateLimitWaitEvent,
      never by hand: one spelling per concept, and the report surface R7 adds
      must read the same shape the governor already emits.

  (d) `_call_with_retry` gains ONE new keyword parameter, defaulted so every
      existing caller is unaffected:
          rate_governor: ProviderRateGovernor | None = None,
      Extend the docstring with what the governor does at this seam and cite
      DECISION F057 D3 and D4 by name.

  (e) The FIRST-call pacing, inserted immediately BEFORE the existing
      `    if on_call is not None:` / `        on_call(1, False)` pair that
      precedes `    out = call_fn()`:
        - skip entirely when `rate_governor is None` or `not provider`
          (DECISION F057 D5);
        - otherwise `acquire(provider, role=role, stop_check=stop_check)` with
          NO deadline_s (DECISION F057 D4), pass the result to
          `_record_rate_limit_wait`, and then make the call REGARDLESS of the
          outcome (DECISION F057 D3 — this seam paces, it never terminates);
        - the comment above it states that in one line and names D3.

  (f) The RETRY pacing, inserted as one contiguous block immediately AFTER the
      existing stop probe
      `        if stop_check is not None and stop_check() is not None:` /
      `            return out`, and BEFORE `        result.retries_used += 1`:
        - skip entirely when `rate_governor is None` or `not provider`;
        - OBSERVE first: `normalize_rate_limit_signal(out.error,
          provider=provider, source=RATE_SIGNAL_SOURCE_RETRY_REASON)` and, when
          it is not None, `rate_governor.observe(signal)` — so the cooldown
          this failure announces is the one this retry waits out;
        - then `acquire(provider, role=role, stop_check=stop_check)`, pass the
          result to `_record_rate_limit_wait`, and `return out` when
          `not acquired.granted`.
      Placement is deliberate and load-bearing: BEFORE `result.retries_used`
      and the reason append, so a stop during the wait leaves the counters
      exactly where the existing stop path leaves them, and no evidence claims
      a retry that never happened.

  (g) `run_pingpong` gains ONE new keyword parameter
      `rate_governor: ProviderRateGovernor | None = None` and, when it is
      None, constructs a `ProviderRateGovernor()` with its own defaults ONCE
      per run in the same scope that already defines `_stopped`. Pass that one
      instance to BOTH `_call_with_retry` call sites — the builder site and
      the reviewer site — as `rate_governor=`. Do not create a second one.

  Nothing else in this file changes. Every insert is guarded by
  `rate_governor is None` or by a falsy provider, which is the default state
  for every existing caller.

C4 — tests/orchestration/test_provider_retry.py, the seam tests
  This file already owns `_call_with_retry` (it calls it at line 112), which is
  why the seam tests live here rather than in the feature file's suggested
  tests/orchestration/test_rate_governor.py: AGENTS.md's Code Discoverability
  rule names test files after the source they cover, and the source here is
  pingpong_loop.py, not rate_governor.py. Say so in one comment at the top of
  the new section so the next reader does not re-litigate it.

  Every governor in these tests is constructed with an INJECTED `monotonic_fn`
  and `sleep_fn` (its __init__ takes both keyword-only). A real sleep in a unit
  test is a finding — the feature file's orchestrator brief rejects them.

  Add these five tests, each named after the property and marked
  @pytest.mark.unit:
   1. a retry whose error carries a rate-limit wording makes the seam wait, and
      `result.rate_limit_waits` gains exactly one entry carrying that provider
      and the classified reason;
   2. a stop that arrives during that wait ends the logical call — assert the
      call_fn invocation COUNT does not grow after the stop, and that
      `result.retries_used` and `result.retry_reasons` are untouched;
   3. an EMPTY provider skips the governor entirely — no wait, no event, and
      the governor's `total_waited_s()` stays 0.0;
   4. `rate_governor=None` (the default) leaves behaviour identical — a
      failing-then-succeeding call retries exactly as it does today;
   5. the FIRST call is paced too: observe a cooldown on the governor, then
      call `_call_with_retry` with a call_fn that succeeds, and assert the call
      still happened AND one wait was recorded.

  If any of the five turns out not to discriminate its property, say so in the
  handback rather than weakening the assertion.

C5 — handback
  Apply the PLAN slice as the COMPLETE new .agent/plan.md, apply the two
  CONTEXT pairs to .agent/context.md, then rewrite .agent/handoff.md per
  docs/agents/handback_template.md.

Constraints
  - Never work on main; never force-push; no PR this round.
  - Do-not-touch (feature file): the per-call retry policy in
    packages/orchestration/provider_timeouts.py, parallelism itself, and the
    provider adapters' internals. packages/orchestration/stream_evidence.py
    also stays byte-identical. pingpong_loop.py is OPENED this round — that is
    what T003 is — and it is the only production file that may move.
  - Repository-wide `ruff check` is RED at base with 26 pre-existing errors and
    is NOT a gate. ruff is gated SCOPED to the files this round touches, where
    the reviewer measured `All checks passed!`, exit 0, at 33fab24e.
  - Every count gate below states its anchoring (R-0369). Report BOTH the
    line-anchored and the whole-file substring count where both are named.
  - No gate below asserts a predicted insertion/deletion pair (R-0367): where a
    number matters, MEASURE it and report it.
  - If `.agent/STOP` appears at any point, finish the commit in flight, write
    the handoff, and stop.

Done when — every command below was executed by the reviewer at 33fab24e
before this block was emitted (R-0364); the baseline each one produced is
stated inline so no gate asks for an unreachable condition.
  1. `git status --porcelain` -> empty. Baseline at 33fab24e: empty.
  2. `git worktree list` -> exactly one line. Baseline: one line.
  3. `git branch --show-current` -> feature/f057-rate-limit-scheduler.
  4. `cmp .agent/authored/f057-r6.md .agent/last_block.md` -> exit 0. Report
     the shared sha256 and the line count.
  5. In .agent/live_review.md, LINE-ANCHORED counts (`^` at line start):
     `^Gate: R5 — PASS` = 1, `^- R-0371 — ` = 1, `^Done: R-0370 — ` = 1,
     `^Landed: R-0370 —` = 1 (it STAYS), `^## Steps` = 1. Also report the
     whole-file SUBSTRING count of `## Steps` and state whether it changed from
     5, which is what the reviewer measured at 33fab24e. A change is not a
     failure; an unreported change is.
  6. `git show --numstat <the C1 sha> -- .agent/live_review.md` -> report the
     two numbers. The only ordered property is that the deletion column is 0,
     because C1 is an append.
  7. `python3 -m pytest tests/orchestration/test_rate_governor.py -q` -> 0
     failed. Baseline at 33fab24e: `59 passed`. This file is not touched this
     round, so report any change to the total as a finding candidate.
  8. `python3 -m pytest tests/orchestration/test_provider_retry.py -q` -> 0
     failed. Baseline at 33fab24e: `21 passed`. Report the new total; it grows
     by C4 and the reviewer re-measures it, so do not predict it.
  9. The four regression files the seam inventory names that C4 does NOT touch,
     run together:
        python3 -m pytest tests/orchestration/test_job_budgets.py \
          tests/orchestration/test_stream_evidence_integration.py \
          tests/orchestration/test_failure_wiring.py \
          tests/orchestration/test_budget_stop_integration.py -q
     -> `294 passed`, exit 0. The reviewer measured exactly that at 33fab24e,
     so any other number is the seam changing behaviour it must not change.
 10. `python3 -m ruff check packages/orchestration/pingpong_loop.py
     packages/orchestration/rate_governor.py
     tests/orchestration/test_provider_retry.py` -> `All checks passed!`, exit
     0. Baseline at 33fab24e: all three already clean.
 11. Canary `python3 -m pytest tests/cli/test_golden_path.py -q` -> 0 failed.
     Baseline: `42 passed`.
 12. The three .agent contract readers, together:
        python3 -m pytest tests/ui_server/test_dashboard_contract.py \
          tests/regression/test_resource_safety.py \
          tests/orchestration/test_test_runner.py -q
     -> `142 passed`, exit 0. Baseline measured by the reviewer at 33fab24e.
 13. `wc -l < .agent/plan.md` -> under 50 (AGENTS.md).
 14. `git diff --name-only 33fab24e..HEAD` -> report the real list. The ordered
     property is that every path on it is one this block named:
     .agent/authored/f057-r6.md, .agent/last_block.md, .agent/live_review.md,
     .agent/decisions.md, packages/orchestration/pingpong_loop.py,
     tests/orchestration/test_provider_retry.py, .agent/plan.md,
     .agent/context.md, .agent/handoff.md. Any path beyond those is a finding.
 15. Do-not-touch: `git diff --stat 21c8148e..HEAD --
     packages/orchestration/provider_timeouts.py
     packages/orchestration/stream_evidence.py` -> EMPTY output.
 16. RED-PROOF, in a disposable worktree under .remedy-wt/ and NEVER in the
     primary checkout. Print the imported module's __file__ FIRST and confirm
     it resolves INSIDE the worktree before trusting any colour. Run these two
     mutations as PROBES — report which tests fail and the exact assertion,
     rather than confirming a colour this block predicts:
       (i)  delete the `acquire(...)` call in the RETRY path (f) and its
            `return out` guard;
       (ii) delete the `observe(...)` call in the RETRY path (f).
     Remove and prune the worktree afterwards; gate 2 is the proof it is gone.

Handback: a completion report plus a rewritten .agent/handoff.md carrying the
  per-commit changed-files table, the item-status table (C0a, C0b, C1, C2, C3,
  C4, C5 — every one appears exactly once with done / skipped / deviated), the
  slice sha256 table, the REAL output of all 16 gates, the open-findings count
  and the next expected action. If the handoff exceeds 60 lines, carry the
  DECISION D15 stated-cause line naming its real length and the mandated
  content that caused it, and drop no section.

--- BEGIN SLICE GATE-R5 ---
Gate: R5 — PASS. Verification tier: round gate plus canary. Every value below was re-measured by the reviewer against the disk, never read out of the handback: `tests/orchestration/test_rate_governor.py` → `59 passed`, the 58 present at `5de503c6` plus the C2 test, 0 failed; `python3 -m ruff check` over `packages/orchestration/rate_governor.py` and `tests/orchestration/test_rate_governor.py` → `All checks passed!`, exit 0; the canary `tests/cli/test_golden_path.py` → `42 passed`; the three `.agent` contract readers together (`tests/ui_server/test_dashboard_contract.py`, `tests/regression/test_resource_safety.py`, `tests/orchestration/test_test_runner.py`) → `142 passed` — the R5 handback did not run these although C1, C2 and C4 all rewrote files those tests read, so the reviewer ran them rather than assuming them; `wc -l` → `.agent/plan.md` 35, `.agent/handoff.md` 112 carrying its DECISION D15 stated-cause line with every mandated section present; `cmp .agent/authored/f057-r5.md .agent/last_block.md` → exit 0, both sha256 `1e4e6b6acfc31fae30322b1b32d7e73d3c003a07893eaad444cbcdda6cad6561`, 268 lines, inside the 400-line cap. The change set is exactly the eight paths the R5 block named — `git diff --name-only 5de503c6..HEAD` lists no ninth — and the Do-not-touch diff over `provider_timeouts.py`, `pingpong_loop.py` and `stream_evidence.py` at `21c8148e..HEAD` is EMPTY, so the round that INVENTORIED the seam did not open it. C1 measures `6 0` and C2's live_review edit `2 0`, insertions only, so nothing above the appended text moved. Counts in `.agent/live_review.md` are reported in BOTH readings, per R-0369's own counter-measure: line-anchored `^Gate: R4 — PASS` 1, `^- R-0369 — ` 1, `^- R-0370 — ` 1, `^Landed: R-0370 —` 1, `^Done: R-0370` 0, `^## Steps` 1; whole-file substring 1, 1, 1, 1, 0 and 5 — the four extra `Steps` hits sit inside R-0369's and R-0370's own prose, which is exactly the difference that counter-measure exists to keep visible. The RED-PROOF was reproduced by the reviewer in its own disposable worktree at `33fab24e`, import path printed first and confirmed inside it (`.remedy-wt/rev_r5_red/./packages/orchestration/rate_governor.py`, with `inspect.getsource` confirming the guard gone in that copy): replacing `max(self._cooldown_until.get(provider, 0.0), now + duration)` with `now + duration` gives `1 failed, 58 passed`, the single id being `test_a_later_signal_never_shortens_a_cooldown_already_running` asserting `1.0 == 30.0` — the same test and the same assertion the worker reported, so the C2 test discriminates the invariant rather than decorating it. The worktree was removed and pruned; `git worktree list` is one line and `git status --porcelain` is empty at this verdict. The C3 seam inventory was audited citation by citation rather than accepted: the reviewer re-read every cited line of `pingpong_loop.py`, `rate_governor.py`, `budget_guard.py`, `models.py`, `failure_postmortem.py`, `stream_evidence.py`, `test_provider_retry.py` and `test_budget_stop_integration.py` out of the working tree, which is byte-identical to `5de503c6` for all of them, and each printed line supports the claim it is cited for; the three greps the inventory rests on were re-run independently — `rate_governor` outside its own module across `packages/` and `apps/` returns nothing, `monotonic` in `pingpong_loop.py` returns nothing, and `_record_attempt(` returns 2119, 2175 and 2222 exactly as claimed; the five-file regression run was re-executed and gives `315 passed in 39.16s`, exit 0, the stated sum; and the inventory's load-bearing section 6 claim was verified beyond its own citation — `_record_call_failure` is guarded by `if builder_out.error:` at 2869, so a paced-then-successful run really does write no `CallRetryEvidence` and the wait needs a new home on `PingPongResult`. No block condition was hit: no fabricated value, no false live indicator, no missing changed-files table, no unverified completion claim, no silent scope change. The round's one deviation was the reviewer's own defect and is not charged to it: the R5 block ordered a `Landed:` line to carry its own commit's SHA while living in that same commit, which is unreachable by construction — registered below as R-0371, where the worker did the only honest thing available and named the commit by its role instead of fabricating a hash.
--- END SLICE GATE-R5 ---

--- BEGIN SLICE FINDING-371 ---
- R-0371 — Low — a block ordered a value that cannot exist at the moment the text carrying it is written. The R5 block told the worker to append to `.agent/live_review.md` "a single line of your own of exactly this shape, with your real commit SHA: `Landed: R-0370 — <one line: what changed, which commit>`" and, six lines later, that "that live_review.md edit belongs to C2, the same commit as the test". A commit's SHA is a hash over a tree that already contains every byte of that commit, so a line inside C2 can never name C2. No correct application of the bundle could satisfy both clauses. The worker was right to declare the deviation, name the commit by its role — "R5's C2, the same commit as this line, whose SHA the handback reports" — and let the handback carry the real value `a01e8a9712aead26eb88888db352d0bb72492cb9`; nothing was fabricated and nothing was edited toward a number. This is the seventh reviewer-gate defect of this feature, after R-0363's unmeasured block length, R-0364's unexecuted ruff gate, R-0367's unreachable numstat, R-0368's wrong-base range gate and R-0369's self-counting string gate, and it is a class none of their counter-measures reach: R-0364 makes the reviewer EXECUTE every gate it orders, but a self-referential SHA is not a gate at all — it is appliable CONTENT whose required value the act of applying it destroys, so there is nothing for the reviewer to execute in advance. `docs/agents/planner_reviewer_prompt.md` §4 item 4 supplies the template verbatim, including the words "which commit", and the template is fine; the defect is pairing it with "your real commit SHA" and "the same commit as the test". Counter-measure, binding from R6 on and additive to all of the above: before ordering any text to be written into a file, the reviewer checks that every value that text must contain already exists at the moment of writing. Commit SHAs, `git show --numstat` outputs and every other post-hoc measurement are ordered into the HANDBACK, which is written after the commits exist, and never into the committed text itself; where a committed line must identify its own commit it names it by its ROLE in the bundle. OPEN.
--- END SLICE FINDING-371 ---

--- BEGIN SLICE DONE-370 ---
Done: R-0370 — Fixed at `a01e8a9712aead26eb88888db352d0bb72492cb9`, verified by the reviewer at `33fab24e`. `tests/orchestration/test_rate_governor.py` now carries `test_a_later_signal_never_shortens_a_cooldown_already_running`, which observes a 30.0s hint, asserts the cooldown is 30.0, observes a 1.0s hint for the SAME provider without advancing the FakeClock, asserts `observe` returned 1.0 for that second signal, and asserts the remaining cooldown is still 30.0 — so the test fails if and only if the stored deadline moved DOWN. The reviewer did not take the fix on trust: it re-ran the mutation itself, in its own disposable worktree and never in the primary checkout, printing the imported module's `__file__` first and confirming with `inspect.getsource` that the guard was gone inside that copy. With `self._cooldown_until[provider] = max(self._cooldown_until.get(provider, 0.0), now + duration)` replaced by `self._cooldown_until[provider] = now + duration` the file goes to `1 failed, 58 passed`, the single failure being this test with `AssertionError: assert 1.0 == 30.0` — that test and no other, so the invariant is pinned exactly as narrowly as it should be, the same way stop-beats-wait and the cooldown cap already are. The worktree was removed and pruned. The `Landed:` line the worker wrote stays on disk above this paragraph, which is what §4 item 4 asks for: it records that the fix landed before any reviewer had seen it, and this paragraph is that review.
--- END SLICE DONE-370 ---

--- BEGIN SLICE DECISIONS ---
## DECISION F057 D3 (2026-08-14) — the seam PACES the first call, it never terminates it

CONTEXT. T003 inserts `acquire()` into `_call_with_retry`. The retry path already
has a stop probe that returns the last `out`; the FIRST call has no probe of any
kind, so a terminating one there changes F011/F018 behaviour rather than adding
to it (`.agent/f057_t003_seam_inventory.md` section 2).

CHOSEN. Before the first call the seam WAITS out a running cooldown and then
makes the call regardless of the acquire outcome. Before a RETRY it waits and
returns the existing `out` when the outcome is not granted, joining the terminal
path the stop probe already owns. `_call_with_retry` cannot say "no call was
made" without fabricating a provider output, and the loop above already owns
termination; the wait is interruptible, so a stop during a first-call wait ends
that wait immediately, which is the acceptance criterion the feature file states.

ALTERNATIVES CONSIDERED. Aborting the first call on a stopped acquire: the only
available return value is a fabricated `out`, which is worse than a stop honoured
one call later. Skipping the first call outright while a cooldown runs: an
unpaced run by another name.

HOW TO REVERSE. Delete the first-call acquire; the retry-path acquire stands on
its own and the C4 tests name the two paths separately.

## DECISION F057 D4 (2026-08-14) — deadline_s stays None at the seam in v1; the budget is enforced through stop_check

CONTEXT. `acquire(deadline_s=...)` wants an absolute value on the injected
monotonic scale. `grep -n monotonic packages/orchestration/pingpong_loop.py`
returns nothing, and neither `JobBudgets` nor `BudgetCounters` is reachable from
`_call_with_retry`, whose only budget-shaped input is the opaque `stop_check`;
the two epochs are unrelated (inventory section 3).

CHOSEN. Pass no deadline. The budget is already enforced through the same
`stop_check` that `acquire` re-probes before every wait slice: the job's
`_stop_check` rebuilds its counters on every call and `evaluate_budget`
recomputes `now` and `elapsed` from `started_at` on every evaluation
(`packages/orchestration/budget_guard.py`), so a wall-clock or deadline breach
arising DURING a wait is seen at the next slice boundary. The governor's own
cooldown cap bounds the wait on top of that.

ALTERNATIVES CONSIDERED. Threading `JobBudgets` down as a new parameter: the
larger change, buying no behaviour `stop_check` does not already deliver.
Passing a POSIX timestamp into a monotonic parameter: inventing a scale, exactly
what the inventory warns against.

HOW TO REVERSE. Thread the deadline in and pass it. `acquire` already implements
DEADLINE_EXCEEDED and its tests already pin it, so reversing is wiring.

## DECISION F057 D5 (2026-08-14) — an empty provider skips the governor entirely

CONTEXT. `_call_with_retry` takes `provider: str = ""` and the loop itself writes
`provider=builder_name or ""`, so a falsy provider is reachable. The governor
keys its cooldowns, streaks and reasons on the raw string, so an empty key would
put every unnamed provider into ONE shared bucket.

CHOSEN. When `provider` is falsy the seam does not call the governor at all — no
observe, no acquire, no wait event. That keeps the feature's "providers without
limit signals behave exactly as today" promise trivially true for unnamed
providers, and makes the shared-bucket bug unreachable rather than unlikely.

ALTERNATIVES CONSIDERED. A sentinel key such as "unknown": it merges genuinely
different providers under one cooldown — the same bug, only harder to see.

HOW TO REVERSE. Delete the falsy-provider guard at both seam sites; the C4 test
named for it fails immediately, which is the point.
--- END SLICE DECISIONS ---

--- BEGIN SLICE PLAN ---
# Plan — F057 Rate-limit-aware scheduler

Branch: feature/f057-rate-limit-scheduler, cut from main at 21c8148e. Next free
finding id: R-0372. Open findings: R-0361, R-0362, R-0363, R-0364, R-0367,
R-0368, R-0369, R-0371 — R-0365, R-0366 and R-0370 are resolved.

## Goal
Provider rate limits stop looking like failures. A per-provider governor reads
normalized limit signals out of call evidence and makes a run WAIT visibly —
with a reason and an expected retry — instead of burning retries or failing the
task. Providers that emit no limit signal behave exactly as today.

## Current Step
T003 part 1: the governor is wired into `_call_with_retry` in
`packages/orchestration/pingpong_loop.py` — observe on a failed call, acquire
before the first call and before every retry, waits recorded on
`PingPongResult.rate_limit_waits` — with the seam tests in
`tests/orchestration/test_provider_retry.py`. DECISIONS F057 D3, D4 and D5
record the three choices the feature file left open.

## Next Steps
1. T003 part 2: the report surfaces — `rate_limit_waits` in
   `export_pingpong_json`, the "waited Ns on provider rate limits this run"
   line in `summarize_pingpong` from `total_waited_s`, and the limit-emitting
   fixture end-to-end that the feature's Acceptance section requires.
2. Integration gate per docs/agents/integration_gate.md, then closure per
   docs/roadmap/STATUS_closure_protocol.md.

## Risks
- The seam now runs on every provider call. Its whole cost when no governor is
  passed and when the provider is falsy must stay zero, which is what the
  294-test regression gate exists to prove.
- `is_rate_limit_error` and the transport predicates still have no precedence
  rule against each other. The seam observes AFTER `should_retry` has already
  decided, so nothing is contradicted today, but F049 will need one.
--- END SLICE PLAN ---

CONTEXT pair 1 — REWRITE (FROM and TO are disjoint).
--- BEGIN SLICE CONTEXT1-FROM ---
the one claimed STATUS line. T001 and T002 are built and gated; T003, the seam
in `packages/orchestration/pingpong_loop.py`, is all that remains.

Out: the per-call retry policy in `packages/orchestration/provider_timeouts.py`,
parallelism itself, and the provider adapters' internals — the feature file's
Do-not-touch list, verified byte-identical at every round so far.
`packages/orchestration/pingpong_loop.py` is READ this round for the seam
inventory and stays byte-identical until T003 opens it.
--- END SLICE CONTEXT1-FROM ---
--- BEGIN SLICE CONTEXT1-TO ---
the one claimed STATUS line. T001 and T002 are built and gated; T003 opened
`packages/orchestration/pingpong_loop.py` at R6 and now owns the seam there and
its tests in `tests/orchestration/test_provider_retry.py`.

Out: the per-call retry policy in `packages/orchestration/provider_timeouts.py`,
parallelism itself, and the provider adapters' internals — the feature file's
Do-not-touch list, verified byte-identical at every round so far.
`packages/orchestration/stream_evidence.py` is out too and stays byte-identical.
--- END SLICE CONTEXT1-TO ---

CONTEXT pair 2 — REWRITE (FROM and TO are disjoint).
--- BEGIN SLICE CONTEXT2-FROM ---
R1 claim and T001 ✅ → R2 findings and two fixes ✅ → R3 verdict and session
close ✅ → R4 T002 governor ✅ → R5 R4 verdict, R-0369, R-0370 and the T003 seam
inventory → T003 seam → integration gate → closure.
--- END SLICE CONTEXT2-FROM ---
--- BEGIN SLICE CONTEXT2-TO ---
R1 claim and T001 ✅ → R2 findings and two fixes ✅ → R3 verdict and session
close ✅ → R4 T002 governor ✅ → R5 R5 verdict, R-0369, R-0370 and the T003 seam
inventory ✅ → R6 R5 verdict, R-0371 and the T003 seam itself → R7 the report
surfaces and the limit-emitting fixture → integration gate → closure.
--- END SLICE CONTEXT2-TO ---
──────────────────────────────────────────────────────────────────────
