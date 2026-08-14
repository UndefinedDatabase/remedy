── STEP T002/3 — F057 Rate-limit-aware scheduler · Round 4 ───────────────
Round base — the SHA every range gate in this block measures from: dae401e1

Goal: record the R3 verdict, register finding R-0368, and build T002 — the
per-provider governor: cooldown state fed by RateLimitSignal, acquire() with an
injected clock and a budget deadline, and stop-beats-wait ordering.

Bundle — seven commits, in this order, pushed after EVERY commit:
  C0a  .agent/authored/f057-r4.md                save this block verbatim
  C0b  .agent/last_block.md                      byte copy of the saved block
  C1   .agent/live_review.md                     append GATE-R3, FINDING-368
  C2   .agent/decisions.md                       append DECISION-D2
  C3   packages/orchestration/rate_governor.py   the governor
  C4   tests/orchestration/test_rate_governor.py the governor's tests
  C5   .agent/plan.md, .agent/context.md, .agent/handoff.md   handback

Change — C3, packages/orchestration/rate_governor.py
  EXTEND the existing module. Do not create a second module, do not move or
  rename any existing symbol, do not change any T001 behaviour. Add exactly:

  Constants
    RATE_LIMIT_COOLDOWN_BASE_S = 1.0   first cooldown when the provider gave no
                                       retry-after hint
    RATE_LIMIT_COOLDOWN_MAX_S = 60.0   the documented cap the exponential never
                                       exceeds
    RATE_GOVERNOR_POLL_SLICE_S = 0.05  wait granularity; the stop probe runs
                                       once per slice
    RATE_ACQUIRE_GRANTED = "granted"
    RATE_ACQUIRE_STOPPED = "stopped"
    RATE_ACQUIRE_DEADLINE_EXCEEDED = "deadline_exceeded"
    RATE_LIMIT_WAIT_VERSION = 1

  @dataclass(frozen=True) RateLimitWaitEvent
    provider: str · waited_s: float · reason: str ·
    rate_limit_wait_v: int = RATE_LIMIT_WAIT_VERSION
    to_json() -> dict[str, Any], JSON-safe, same discipline as
    RateLimitSignal.to_json.

  @dataclass(frozen=True) RateLimitAcquireResult
    outcome: str — one of the three RATE_ACQUIRE_* constants · provider: str ·
    waited_s: float · reason: str, "" when nothing was waited on.
    granted -> bool property: outcome == RATE_ACQUIRE_GRANTED.

  class ProviderRateGovernor
    __init__(self, *, monotonic_fn: Callable[[], float] = time.monotonic,
             sleep_fn: Callable[[float], None] = time.sleep,
             base_cooldown_s: float = RATE_LIMIT_COOLDOWN_BASE_S,
             max_cooldown_s: float = RATE_LIMIT_COOLDOWN_MAX_S,
             poll_slice_s: float = RATE_GOVERNOR_POLL_SLICE_S) -> None
      The clock and the sleep are INJECTED so a unit test never sleeps for real.

    observe(signal: RateLimitSignal) -> float
      Feed one signal into that provider's cooldown; return the cooldown
      seconds just applied.
        · signal.retry_after_s is used verbatim when it is not None;
        · when it is None the cooldown is
          min(base_cooldown_s * 2 ** (streak - 1), max_cooldown_s), streak being
          the count of consecutive signals observed for that provider;
        · a signal never SHORTENS a running cooldown: the new cooldown_until is
          max(existing, now + duration);
        · signal.reason becomes that provider's current wait reason.

    cooldown_remaining_s(provider: str) -> float
      max(0.0, cooldown_until - now); 0.0 for a provider never observed.

    acquire(self, provider: str, *, role: str = "",
            deadline_s: float | None = None,
            stop_check: Callable[[], Any] | None = None)
            -> RateLimitAcquireResult
      This ordering IS the acceptance criterion:
        1. Stop FIRST. If stop_check is not None and stop_check() is not None,
           return STOPPED immediately — before any cooldown is read, waited_s
           0.0, sleep_fn never called. Same "non-None means stopped" convention
           _call_with_retry already uses
           (packages/orchestration/pingpong_loop.py:2207).
        2. If cooldown_remaining_s(provider) <= 0.0: return GRANTED, waited_s
           0.0, NO wait event, and reset that provider's streak to 0 — the
           provider recovered.
        3. Otherwise wait in slices of at most poll_slice_s until the cooldown
           elapses, re-probing stop_check BEFORE every slice; a stop returns
           STOPPED with the seconds actually waited. deadline_s, when given, is
           an absolute value on the SAME monotonic scale as monotonic_fn: when
           the cooldown would run past it, wait only up to the deadline and
           return DEADLINE_EXCEEDED with the seconds actually waited.
        4. Every outcome that waited more than 0.0 seconds records exactly one
           RateLimitWaitEvent — granted, stopped and deadline alike — so a run
           stopped mid-wait still shows the wait it paid for.
      role is carried for the caller's evidence and does not affect pacing. Say
      that on its own line; do not leave a reader to infer it.

    wait_events() -> list[RateLimitWaitEvent]   a copy, never the live list
    total_waited_s() -> float                   the sum, for the T003 report line

  Documented deliberate absences, in the module docstring, in this repository's
  "Remedy deliberately does not X because Y" idiom (AGENTS.md, Code
  Discoverability Conventions):
    · v1 coordinates nothing ACROSS PROCESSES — two Remedy processes hold
      independent governors; cross-process pacing is the scheduler tier's
      problem, as the feature file states under Edge cases;
    · v1 does not queue or fairly order N concurrent acquirers inside one
      process either. acquire() is shaped so N callers CAN call it — no caller
      identity, no reservation, no handle to release — but the implementation is
      single-flight, per the feature file's "design the interface for N
      concurrent acquirers now, implement single-flight now";
    · nothing calls acquire() yet: the seam is T003.
  Update the module docstring's T002/T003 sentences to describe what the module
  now HAS rather than what it will have, and extend its Public API list. A
  docstring that describes a call graph the code does not have is finding
  R-0365's class, and this module has already spent a round on it.

Change — C4, tests/orchestration/test_rate_governor.py
  EXTEND the file; all 46 existing tests keep passing unchanged. The opening
  docstring says "Pure logic: no clock, no sleep, no network, no filesystem" —
  that becomes false this round, so rewrite that sentence to say the clock and
  the sleep are injected fakes and that no test sleeps for real.
  Add a fake-clock helper local to this file — a small class holding a float
  now, whose sleep advances it — and cover at least:
    1. observe() with a retry_after_s hint applies exactly those seconds.
    2. observe() without a hint escalates 1x, 2x, 4x ... across consecutive
       signals for one provider and never exceeds RATE_LIMIT_COOLDOWN_MAX_S,
       proven by observing enough consecutive signals to pass the cap.
    3. Two providers hold independent cooldowns.
    4. acquire() on an unobserved provider is GRANTED, waited_s 0.0, no wait
       event.
    5. acquire() during a cooldown waits and is GRANTED, waited_s equal to the
       cooldown, with exactly one RateLimitWaitEvent carrying the provider, the
       waited seconds and the signal's reason.
    6. Stop beats wait, already stopped: a stop_check returning non-None makes
       acquire return STOPPED with waited_s 0.0, and the fake sleep is never
       called even once.
    7. Stop beats wait, stopped mid-wait: a stop_check that turns non-None after
       the first slice returns STOPPED with waited_s strictly LESS than the
       cooldown, and the fake clock proves acquire did not sleep the cooldown
       out.
    8. A deadline expiring mid-wait returns DEADLINE_EXCEEDED with waited_s
       equal to deadline minus start, and the partial wait recorded as an event.
    9. A granted acquire that waited nothing resets the streak, so the next
       hint-less signal starts again at RATE_LIMIT_COOLDOWN_BASE_S.
   10. RateLimitWaitEvent.to_json() survives json.dumps/loads unchanged, and the
       event is frozen — assert dataclasses.FrozenInstanceError, never a bare
       Exception (finding R-0366).
   11. total_waited_s() sums the round's waits.
  Mark them @pytest.mark.unit like the existing tests. No test may call
  time.sleep and none may assert on wall-clock duration.

Constraints
  · AGENTS.md in full: self-review loop before EVERY commit, one logical step
    per commit, under 500 INSERTIONS per commit, .agent/plan.md current, clean
    tree, push after every commit.
  · Do not touch packages/orchestration/provider_timeouts.py,
    packages/orchestration/pingpong_loop.py or
    packages/orchestration/stream_evidence.py — the feature file's Do-not-touch
    list. The T003 seam stays unwired: nothing outside rate_governor.py and its
    test may import the governor.
  · Never work on main, never force-push, never merge, never create a PR. There
    is no open PR for this branch and none is created before closure.
  · Any destructive check runs ONLY inside a disposable git worktree under
    .remedy-wt/ (gitignored), removed and pruned before the handback.
  · If .agent/STOP appears at any point: finish the commit in flight, write the
    handoff, stop.
  · Apply every authored slice below DISK TO DISK — extract it from the
    COMMITTED .agent/authored/f057-r4.md between its markers and write those
    bytes to the target. Never retype one. Assert the re-read bytes equal the
    extracted bytes and report the sha256 of each extracted slice.

Done when — every gate below is EXECUTED and its real exit code and real output
recorded in the handback. "Green" as a word is a finding. No gate here asserts a
predicted line count or a predicted numstat pair; where a number matters the
round REPORTS it (finding R-0367).
   1. git status --porcelain → empty at the handback.
   2. git worktree list → exactly one line.
   3. git branch --show-current → feature/f057-rate-limit-scheduler.
   4. cmp .agent/authored/f057-r4.md .agent/last_block.md → exit 0. Report the
      sha256 both files share and the block's line count, which must be ≤ 400.
      This gate is a CHECKPOINT: over 400 stops the round after C0b.
   5. In .agent/live_review.md after C1: "Gate: R3 — PASS" occurs exactly 1x,
      "- R-0368 — " exactly 1x, "## Steps" still exactly 1x, and the line
      beginning "- R-0361 " still has sha256
      70a8c9fb1a6ddebd2a1592b467cf9cb7e18f43ad0449c245d110bc0f1f056a7b.
   6. C1 is a pure APPEND: git show --numstat <C1> -- .agent/live_review.md
      shows 0 deletions. Report the insertion count; do not predict it.
   7. In .agent/decisions.md after C2: "## DECISION F057 D2 (2026-08-14)" occurs
      exactly 1x, and that commit's numstat for the file shows 0 deletions.
   8. python3 -m pytest tests/orchestration/test_rate_governor.py -q → exit 0.
      Report the passed count. All 46 tests present at dae401e1 still pass;
      0 failed.
   9. python3 -m ruff check packages/orchestration/rate_governor.py
      tests/orchestration/test_rate_governor.py → "All checks passed!", exit 0.
      The reviewer executed this at dae401e1 and it passed there.
  10. Canary: python3 -m pytest tests/cli/test_golden_path.py -q → exit 0.
      Report the passed count.
  11. Do-not-touch: git diff --stat 21c8148e..HEAD over the three files named
      under Constraints → EMPTY output.
  12. Change set: git diff --name-only dae401e1..HEAD → exactly the NINE paths
      this bundle names, no tenth.
  13. wc -l < .agent/plan.md → under 50. Report the number.
  14. No real sleeps: "time.sleep" occurs 0x in
      tests/orchestration/test_rate_governor.py. Report the count.
  15. RED-PROOF, inside a disposable worktree under .remedy-wt/ and never in the
      primary checkout, printing the imported module's __file__ FIRST to prove
      the mutated copy is the one under test. Two mutations, run separately:
        (a) delete the stop_check probe from acquire()'s per-slice loop, so a
            stop can only be seen before the wait starts;
        (b) replace the cooldown cap min(..., max_cooldown_s) with the uncapped
            product.
      For each: report the failing test ids and the pass/fail counts. At least
      one test must fail in each case — a mutation that leaves the suite green
      means the tests do not discriminate the property, and THAT is the finding
      to report, not a number to reach. Remove and prune the worktree
      afterwards; gate 2 proves it.

Handback: completion report + rewrite .agent/handoff.md (AGENTS.md: rewritten,
never appended; ≤60 lines, or a "Deviations, declared" line naming the actual
count and the mandated content that caused the overage — DECISION D15). It
carries the per-commit changed-files table, an item-status table covering C0a,
C0b, C1, C2, C3, C4 and C5 exactly once each, the real verification output for
all 15 gates, the sha256 of every extracted slice, and the open-findings count.
Open findings after C1: SIX — R-0361, R-0362, R-0363, R-0364, R-0367, R-0368.
Next free id: R-0369.

The five authored slices follow. Each marker is alone on its line.

>>> GATE-R3 >>>
Gate: R3 — PASS. Verification tier: round gate plus canary. Every value below was re-measured by the reviewer against the disk rather than read out of the handback: `tests/orchestration/test_rate_governor.py` → `46 passed`; `tests/docs/` → `295 passed`; the canary `tests/cli/test_golden_path.py` → `42 passed`; `python3 -m ruff check` scoped to the two feature files → `All checks passed!`, exit 0; `wc -l < .agent/plan.md` → 38; `.agent/handoff.md` → 133 lines, carrying the DECISION D15 stated-cause line that length requires; the saved block is 200 lines, inside the 400-line cap R-0363 recorded the R1 block breaking; `cmp .agent/authored/f057-r3.md .agent/last_block.md` → byte-equal, both sha256 `c39feb138de6f36d57cad97aa99a7ca770e47a719d7a455d277e03e09db7c999`. The change set is exactly the six files the R3 block named — `git diff --name-only c3222402..HEAD` lists no seventh — and no `.py` file moved at all, which the EMPTY Do-not-touch diff over `provider_timeouts.py`, `pingpong_loop.py` and `stream_evidence.py` at `21c8148e..HEAD` confirms independently. C1's application to `.agent/live_review.md` measures `8 0`: insertions only, so nothing above the appended text moved, and the carried R-0361 line still hashes to `70a8c9fb1a6ddebd2a1592b467cf9cb7e18f43ad0449c245d110bc0f1f056a7b` after a third append. `Gate: R2 — PASS`, `- R-0367 — `, `Done: R-0365 — ` and `Done: R-0366 — ` each occur exactly once and `## Steps` still occurs exactly once, so the `.agent` contract readers stay satisfied. `git worktree list` is one line and `git status --porcelain` is empty at this verdict. No block condition was hit: no fabricated value, no false live indicator, no missing changed-files table, no unverified completion claim, no silent scope change. This entry exists although the R3 handback invoked §4 item 13: that item exempts the last round of a BRANCH, whose verdict lives in the handoff and the PR, and R3 was the last round of a SESSION on a branch that continues at T002 — so its verdict is recorded here in the normal cadence, where R2 recorded R1 and R3 recorded R2. No repair round was opened for it, exactly as item 13 requires. The round's one red gate was the reviewer's own defect and is recorded below as R-0368, not charged to the round: the worker measured the real value, proved the reachable form over the round's actual base, and edited nothing to reach an unreachable one.
<<< GATE-R3 <<<

>>> FINDING-368 >>>
- R-0368 — Low — a round gate named a base ref belonging to a different round. Gate 14 of the R3 block ordered `git diff --name-only 36b745bd..HEAD` and expected exactly the six files that block names. `36b745bd` is the R1 handback — the base of ROUND 2, not of round 3, whose base is `c3222402` — so the ordered range necessarily spans both rounds and lists the two Python files R2 legitimately changed. The real output at `944f01cc` was eight paths, and no correct application of the R3 bundle could have made it six. The worker measured it, declared it, computed the reachable form (`git diff --name-only c3222402..HEAD` → exactly the six named files) and edited nothing to reach the ordered one; the reviewer re-measured that reachable form at `dae401e1` and confirms it. This is the fifth reviewer-arithmetic defect of this feature, after R-0363's unmeasured block length, R-0364's unexecuted ruff gate and R-0367's unreachable numstat, and it is precisely the one their counter-measures do not reach: R-0364 makes the reviewer EXECUTE every gate it orders, and R-0367 bars predicted numbers, but a range gate executed at the wrong base runs cleanly at emission time and only becomes unmeetable once the round's own commits exist. Counter-measure, binding from R4 on and additive to both: every gate taking a commit range states its base as the SHA of the handback the round starts from — re-read from `git log` at emission, never carried over from the previous block — and the block prints that SHA once in its bundle header, so the range and the round agree by construction rather than by the reviewer's memory. OPEN.
<<< FINDING-368 <<<

>>> DECISION-D2 >>>

## DECISION F057 D2 (2026-08-14) — the governor's acquire() contract: stop is read before cooldown, and every wait is evidence

CONTEXT. T002 builds `ProviderRateGovernor.acquire()` in
`packages/orchestration/rate_governor.py`. Three of its choices are not
derivable from the feature file and would otherwise be re-litigated at T003,
when the seam in `_call_with_retry` starts calling it.

CHOSEN. (1) `acquire()` probes `stop_check` BEFORE it reads any cooldown, and
again before every wait slice, so a stop request can never be delayed by a
pacing decision. The feature file's acceptance criterion is "a stop request
during a wait interrupts the wait immediately"; reading the cooldown first
would satisfy the words while adding a slice of latency to every stop.
(2) A wait that ends in a stop or in a deadline still records its
`RateLimitWaitEvent`. Time was really spent, and evidence that omitted it would
make a paced-then-stopped run look like a run that never waited.
(3) `retry_after_s` is honoured verbatim when the provider sends one, and the
exponential is used only in its absence — a provider that states its own
recovery time knows better than a backoff curve, and `parse_retry_after_seconds`
already rejects negatives and anything over `MAX_RETRY_AFTER_S`, so the verbatim
path cannot be fed an absurd number.

ALTERNATIVES CONSIDERED. Returning a bare bool from `acquire()`: rejected
because "did not wait" and "was stopped mid-wait" are different facts to the
caller and to the report line, and a bool erases the difference. Holding a lock
across the wait so N acquirers queue fairly: rejected as v1 scope — the feature
file says implement single-flight now, and a lock held across a wait serializes
callers a later tier will want concurrent.

HOW TO REVERSE. Delete this decision and change the three behaviours in
`acquire()`; the tests named in the R4 block pin each one, so reversing means
deleting those tests deliberately rather than discovering the change later.
<<< DECISION-D2 <<<

>>> PLAN >>>
# Plan — F057 Rate-limit-aware scheduler

Branch: feature/f057-rate-limit-scheduler, cut from main at 21c8148e. Next free
finding id: R-0369. Open findings: R-0361, R-0362, R-0363, R-0364, R-0367,
R-0368 — R-0365 and R-0366 were resolved at R3.

## Goal
Provider rate limits stop looking like failures. A per-provider governor reads
normalized limit signals out of call evidence and makes a run WAIT visibly —
with a reason and an expected retry — instead of burning retries or failing the
task. Providers that emit no limit signal behave exactly as today.

## Current Step
T002 — the governor itself, built this round in
`packages/orchestration/rate_governor.py`: per-provider cooldown state fed by
`RateLimitSignal`, `acquire()` with an injected clock and a budget deadline,
stop-beats-wait ordering, and wait events. Nothing calls it yet; the seam is
T003. Awaiting the reviewer's gate.

## Next Steps
1. T003 — seam integration in `_call_with_retry`
   (`packages/orchestration/pingpong_loop.py:2142`, which already carries
   `stop_check`), ordered stop, then budget, then acquire; wait evidence; the
   report line; the limit-emitting fixture end-to-end.
2. Integration gate, then closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Stop-beats-wait is the acceptance criterion most likely to be faked by a
  comment. It is pinned by two tests and a mutation red-proof this round.
- `is_rate_limit_error` still has no precedence rule against the existing
  transport predicates. T003 decides it with evidence; nothing depends on it yet.
<<< PLAN <<<

>>> CONTEXT >>>
# Context — F057 Rate-limit-aware scheduler

## Active Branch
feature/f057-rate-limit-scheduler, cut from main at 21c8148e. F057 is claimed
`[~]` in docs/roadmap/STATUS.md and stays claimed until closure. No PR exists
for this branch yet; one is created at closure, not before.

## Scope
In: `packages/orchestration/rate_governor.py` and
`tests/orchestration/test_rate_governor.py`, plus `.agent/**` round state and
the one claimed STATUS line. T001 and T002 are built; T003, the seam, remains.

Out: the per-call retry policy in `packages/orchestration/provider_timeouts.py`,
parallelism itself, and the provider adapters' internals — the feature file's
Do-not-touch list, verified byte-identical at every round so far.
`packages/orchestration/pingpong_loop.py` holds the T003 seam and stays
untouched until then.

## Constraints
- The main session writes nothing in the work tree; a delegated worker subagent
  makes every commit (docs/agents/self_drive_protocol.md).
- Merges only at the Open PR Gate; never force-push; never work on main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/** also gates
  tests/docs/. Destructive and red-proof checks run only inside a disposable
  git worktree under .remedy-wt/, so resource safety stays intact and no
  background pytest process is ever left running.
- Repository-wide `ruff check` is RED at base 21c8148e with 26 pre-existing
  errors (20 I001, 4 F401, 1 F821, 1 UP035). It is NOT a round gate; ruff is
  gated scoped to the files this feature owns. Repairing it is a paydown
  branch's job, not this one's (R-0364).
- The governor's clock and sleep are injected. A real sleep in a unit test is a
  finding.
- A round pushes after EVERY commit, not once at its last step.

## Steps
R1 claim and T001 ✅ → R2 findings and two fixes ✅ → R3 verdict and session
close ✅ → R4 R3 verdict, R-0368 and T002 governor → T003 seam → integration
gate → closure.
<<< CONTEXT <<<
