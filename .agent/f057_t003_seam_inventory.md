# F057 T003 — the seam, confirmed on disk

Round state, not built-system documentation (AGENTS.md, Documentation Structure),
so this file is deliberately NOT under `docs/` and needs no `docs/README.md`
entry. The neighbouring `.agent/t003_inventory.md` belongs to a DIFFERENT
feature; this file's name is deliberately distinct.

READ-ONLY. Produced at R5, which changed no file under `packages/` or `apps/`.
Every citation below was re-read out of `5de503c6` — the round base — and is the
evidence T003 starts from instead of re-deriving it. The feature file's
orchestrator brief says "Gate T003 on the seam being confirmed"
(`docs/roadmap/features/T2_F057.md:65-66`); this is that confirmation.

## 1. The call site

`_call_with_retry` is defined at `packages/orchestration/pingpong_loop.py:2142`
(`def _call_with_retry(`). It starts a provider call in exactly TWO places, and
they are not symmetric:

- the FIRST call, `packages/orchestration/pingpong_loop.py:2172` —
  `    out = call_fn()` — preceded only by the optional prompt-trace hook
  `on_call(1, False)` at `packages/orchestration/pingpong_loop.py:2171`.
- the RETRY call, inside `for attempt in range(MAX_RETRIES):`
  (`packages/orchestration/pingpong_loop.py:2179`), at
  `packages/orchestration/pingpong_loop.py:2221` — `        out = call_fn()`.

`stop_check` is consulted ONCE, at
`packages/orchestration/pingpong_loop.py:2207` —
`        if stop_check is not None and stop_check() is not None:` — under the
comment `        # F018: check budget before spending another transport call`
at `packages/orchestration/pingpong_loop.py:2206`.

Between that probe and the retry call at 2221 sit, in order:

| Line | What |
|---|---|
| 2210 | `        result.retries_used += 1` |
| 2211 | `        _reason = f"{role}:attempt{attempt + 1}:{out.error[:120]}"` |
| 2212 | `        result.retry_reasons.append(_reason)` — its own comment: "the run-global summary, unchanged" |
| 2213-2217 | the `call_reasons` append — THIS logical call's evidence |
| 2218 | `        _time.sleep(backoff)` — the transport backoff |
| 2219-2220 | `on_call(attempt + 2, True)` — the prompt-trace hook |

`_time` is `import time as _time` at
`packages/orchestration/pingpong_loop.py:25`. Note that 2218 is the ONLY sleep
in the helper today, and it is the per-call backoff, not pacing: F057's wait is
a second, longer-horizon wait that the governor owns
(`docs/roadmap/features/T2_F057.md:14-16`).

## 2. Ordering — what exists, what T003 must insert

The feature file requires "order: stop check, budget check, THEN governor
acquire, so stops beat waits" (`docs/roadmap/features/T2_F057.md:31-32`).

What exists at the seam today:

1. **stop check — YES, but fused with the budget check and only before
   RETRIES.** There is ONE probe, `stop_check()` at
   `packages/orchestration/pingpong_loop.py:2207`. Its docstring says so
   explicitly at `packages/orchestration/pingpong_loop.py:2160`:
   "``stop_check`` (F018) is evaluated before each transport retry. A budget".
   The callable the loop passes is `_stopped`, defined at
   `packages/orchestration/pingpong_loop.py:2713`, wired in at
   `packages/orchestration/pingpong_loop.py:2860` (builder) and
   `packages/orchestration/pingpong_loop.py:3077` (reviewer); `_stopped`
   delegates to `run_pingpong`'s own `stop_check` parameter
   (`packages/orchestration/pingpong_loop.py:2452`), which the job layer binds
   to `_stop_check` at `packages/orchestration/pingpong_job.py:1968` and passes
   at `packages/orchestration/pingpong_job.py:2261`.
2. **budget check — YES, but it IS the stop check.** `_stop_check` calls
   `_should_stop(... budgets=_job_budgets, counters=counters ...)` at
   `packages/orchestration/pingpong_job.py:1970-1975`, so the operator stop and the
   budget evaluation return through one callable and one non-None value. The
   seam therefore CANNOT distinguish "operator stopped" from "budget exhausted"
   without inspecting the returned object. This is a real constraint on T003,
   not a nuance.
3. **governor acquire — NO.** Nothing in `packages/` or `apps/` imports
   `rate_governor`; the module docstring states that deliberately at
   `packages/orchestration/rate_governor.py:26`.

What T003 must insert, precisely:

- an `acquire(...)` call AFTER the existing `stop_check()` at
  `packages/orchestration/pingpong_loop.py:2207` and BEFORE
  `        _time.sleep(backoff)` at
  `packages/orchestration/pingpong_loop.py:2218` — that window is the only
  place in the retry path where the ordering the feature file demands already
  holds by construction.
- a second, NEW stop-then-acquire pair before the FIRST call at
  `packages/orchestration/pingpong_loop.py:2172`, because there is no probe of
  any kind before it today. Without this the governor paces retries only, and a
  run whose first call hits a limited provider is not paced at all. T003 must
  decide whether adding a stop probe before the first call is in scope — it
  changes existing F011/F018 behaviour and is the one place this seam work can
  regress something unrelated.

## 3. The deadline — the conversion is T003's real work

`ProviderRateGovernor.acquire(deadline_s=...)` wants an ABSOLUTE value on the
same monotonic scale as the injected clock; the docstring says so at
`packages/orchestration/rate_governor.py:469`, and the default clock is
`time.monotonic` (`packages/orchestration/rate_governor.py:404`).

**Nothing in the loop is an absolute monotonic deadline.** `grep -n monotonic
packages/orchestration/pingpong_loop.py` returns NOTHING at `5de503c6` — the
loop never reads a monotonic clock at all. The nearest things that exist:

| Symbol | Where | Unit and epoch |
|---|---|---|
| `JobBudgets.deadline` | `packages/core/models.py:145` | `datetime \| None`, timezone-aware, coerced to UTC at `packages/core/models.py:181`. Absolute, but WALL-CLOCK UTC, not monotonic. |
| `JobBudgets.max_wall_clock_minutes` | `packages/core/models.py:141` | integer MINUTES, a duration, no epoch. |
| `BudgetCounters.elapsed_seconds` | `packages/orchestration/budget_guard.py:52` | seconds elapsed, a duration measured from `started_at`. |
| `BudgetCounters.started_at` | `packages/orchestration/budget_guard.py:54` | `datetime \| None`, wall-clock UTC. |

`evaluate_budget` compares them as wall-clock: `if now >= budgets.deadline:` at
`packages/orchestration/budget_guard.py:336`, and
`if elapsed >= limit_secs:` at `packages/orchestration/budget_guard.py:331`
where `limit_secs = budgets.max_wall_clock_minutes * 60`
(`packages/orchestration/budget_guard.py:329`).

So T003 must CONVERT, and the conversion is the work: it has a UTC datetime and
a monotonic-scale API, and the two epochs are unrelated. The honest shape is to
read both clocks once at the seam and carry the offset —
`deadline_s = monotonic_now + (budgets.deadline - utc_now).total_seconds()` —
never to pass a POSIX timestamp into a monotonic parameter. Neither
`JobBudgets` nor `BudgetCounters` is reachable from `_call_with_retry` today:
the helper's only budget-shaped input is the opaque `stop_check` callable, so
either the deadline is threaded in as a new parameter or it is derived at the
call sites (2849, 3061, 3117) where the loop's own scope is in reach. T003 must
not invent a scale, and must not silently treat "no deadline" as zero —
`acquire` already documents `deadline_s=None` as "no deadline".

## 4. Where the signals come from

Of the two readers, only ONE is reachable at the seam without a disk read.

- `read_retry_reason_signals` (`packages/orchestration/rate_governor.py:296`) —
  REACHABLE, from two variables in `_call_with_retry`'s own scope:
  `result.retry_reasons` (the run-global list, declared at
  `packages/orchestration/pingpong_loop.py:187`) and the per-call
  `call_reasons` list (parameter at
  `packages/orchestration/pingpong_loop.py:2151`). The single entry appended to
  both is built at `packages/orchestration/pingpong_loop.py:2211` as
  `        _reason = f"{role}:attempt{attempt + 1}:{out.error[:120]}"`. That is
  EXACTLY what the governor's module docstring claims at
  `packages/orchestration/rate_governor.py:40` and what
  `read_retry_reason_signals`' own docstring restates at
  `packages/orchestration/rate_governor.py:303`
  (``Each entry is ``"{role}:attempt{n}:{error}"`` (pingpong_loop.py:2211)``).
  Re-checked at `5de503c6`: the claim still reads true, byte for byte.
  Simpler still, `out.error` itself is in hand at
  `packages/orchestration/pingpong_loop.py:2180`, so the seam can normalize the
  raw provider text without waiting for a reason string to be formatted.
- `read_run_event_signals` (`packages/orchestration/rate_governor.py:266`) —
  NOT reachable at the seam. Normalized run events are written to a file, not
  returned: `normalize_stream_object` is called only inside
  `capture_stream_evidence` at `packages/orchestration/stream_evidence.py:484`,
  and the reader that returns them as a list is `read_run_events` at
  `packages/orchestration/stream_evidence.py:817`, which
  `packages/orchestration/pingpong_loop.py` never calls. What the loop holds
  after a call is `stream_call_id` and `stream_artifact_refs`
  (`packages/orchestration/pingpong_loop.py:2137-2138`) — paths, not events.
  Feeding shape 1/2 into the governor therefore costs a disk read per call,
  which is a design decision T003 owns and should probably decline for v1.

## 5. The provider identity

`_call_with_retry` already takes `    provider: str = "",` at
`packages/orchestration/pingpong_loop.py:2147` — a plain `str` with an EMPTY
default, used today only for attribution in `_record_attempt`
(`packages/orchestration/pingpong_loop.py:2119`, called at 2175 and 2222).

It CAN be empty, in two different ways:

- the parameter defaults to `""` and existing callers omit it — e.g.
  `tests/orchestration/test_provider_retry.py:112` calls
  `_call_with_retry(lambda: out, result=result, role="builder")` with no
  provider at all.
- the loop's own values are `builder_name` /`reviewer_name`, parameters of
  `run_pingpong` at `packages/orchestration/pingpong_loop.py:2424` and
  `packages/orchestration/pingpong_loop.py:2425`, passed at
  `packages/orchestration/pingpong_loop.py:2857` and
  `packages/orchestration/pingpong_loop.py:3069`. They default to `"fake"`, but
  the loop itself does not trust them: it writes `provider=builder_name or ""`
  at `packages/orchestration/pingpong_loop.py:2835`, which only makes sense if
  a falsy value is reachable.

An empty key would put every provider into ONE cooldown bucket — the governor
keys `_cooldown_until`, `_streaks` and `_reasons` on the raw string
(`packages/orchestration/rate_governor.py:415-417`) — so the seam must NOT pass
an empty provider through. The two honest options are to SKIP the governor
entirely when `provider` is falsy (no identity, no pacing, current behaviour
preserved) or to pass an explicit sentinel; skipping is the smaller change and
keeps the feature's "providers without limit signals behave exactly as today"
promise (`docs/roadmap/features/T2_F057.md:10-11`) trivially true for unnamed
providers. This must be a decision in `.agent/decisions.md`, not an accident.

## 6. Evidence and report surfaces

- **Wait event — a home exists, and it is per-logical-call.** The structure the
  seam already writes to is the `call_reasons` list
  (`packages/orchestration/pingpong_loop.py:2151`), which the loop allocates
  per logical call at `packages/orchestration/pingpong_loop.py:2848` and
  `packages/orchestration/pingpong_loop.py:3060` and which is consumed into
  `CallRetryEvidence.of(list(call_reasons or []))` at
  `packages/orchestration/pingpong_loop.py:2339`, whose constructor is
  `packages/orchestration/failure_postmortem.py:233`. But `CallRetryEvidence`
  holds only `retries_used` and `retry_reasons`
  (`packages/orchestration/failure_postmortem.py:228-229`) and is written ONLY on a
  call that finally FAILED — `_record_call_failure`
  (`packages/orchestration/pingpong_loop.py:2281`) is called at terminal exits
  only, by its own docstring. A paced-then-SUCCESSFUL run is exactly the run
  F057 must show waits for, and that run writes no post-mortem. So: there IS a
  cycle-evidence structure at the seam, and it is the WRONG one. The reachable
  home for a wait is a new field on `PingPongResult` beside
  `    retry_reasons: list[str] = field(default_factory=list)`
  (`packages/orchestration/pingpong_loop.py:187`), which is what
  `RateLimitWaitEvent.to_json` (`packages/orchestration/rate_governor.py:364`)
  is already shaped for.
- **Report line — two homes, both obvious.** The JSON surface is
  `export_pingpong_json` at `packages/orchestration/pingpong_loop.py:4229`,
  which already emits `        "retries_used": result.retries_used,` at
  `packages/orchestration/pingpong_loop.py:4326` and `"retry_reasons"` at 4327;
  a `rate_limit_waits` key belongs beside them. The human line "waited 84s on
  provider rate limits this run" (`docs/roadmap/features/T2_F057.md:33`) belongs
  in `summarize_pingpong` at `packages/orchestration/pingpong_loop.py:4364`,
  next to the existing conditional lines such as the reviewer-parse block at
  `packages/orchestration/pingpong_loop.py:4389-4393`. The number it prints is
  `ProviderRateGovernor.total_waited_s`
  (`packages/orchestration/rate_governor.py:513`), which exists for exactly
  this and says so.

## 7. Regression risk — what must stay green

Tests that import or exercise `_call_with_retry` directly, found by
`grep -rn "_call_with_retry" tests/`:

| File | Tests | First reference |
|---|---|---|
| `tests/orchestration/test_job_budgets.py` | 135 | line 766 |
| `tests/orchestration/test_stream_evidence_integration.py` | 62 | line 259 |
| `tests/orchestration/test_failure_wiring.py` | 58 | line 19 |
| `tests/orchestration/test_budget_stop_integration.py` | 39 | line 425 |
| `tests/orchestration/test_provider_retry.py` | 21 | line 112 |

Counts are `pytest --collect-only -q` per file at `5de503c6`. What was RUN this
round, scoped to those five files and nothing wider:

    python3 -m pytest tests/orchestration/test_provider_retry.py \
      tests/orchestration/test_failure_wiring.py \
      tests/orchestration/test_budget_stop_integration.py \
      tests/orchestration/test_job_budgets.py \
      tests/orchestration/test_stream_evidence_integration.py -q
    → 315 passed in 39.25s, exit 0

315 is the sum of the five counts, so nothing was skipped or deselected. The
full suite was NOT run; that is the integration gate's job, not this
inventory's. The sharpest of these for T003 is
`tests/orchestration/test_budget_stop_integration.py:425`
(`"""_call_with_retry checks stop_check before transport retries."""`), which
pins the very ordering the governor must be inserted after.
