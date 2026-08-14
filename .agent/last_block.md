── STEP CLOSE-SESSION — F057 · ROUND 3 ───────────────────────────────

Goal:        Persist the R2 verdict, register R-0367, mark R-0365 and R-0366
             resolved with reviewer-authored `Done:` text, and write the
             session-closing handoff that hands T002 to the next session.

Bundle:      C0a save this block · C0b point last_block at it · C1 the R2
             verdict, R-0367 and the two resolutions · C2 handback.

Change:      Exactly these files:
             - `.agent/authored/f057-r3.md` (NEW, C0a)
             - `.agent/last_block.md` (C0b)
             - `.agent/live_review.md` (C1, APPEND only)
             - `.agent/plan.md` (C2)
             - `.agent/context.md` (C2)
             - `.agent/handoff.md` (C2)
             NO production code. NO test file. If you believe a code change is
             needed, STOP and report it instead.

Staging:     EXPLICIT PATHS ONLY. Never `git add -A`. Push after every commit.

── C0a / C0b ─────────────────────────────────────────────────────────
Save this ENTIRE block verbatim (from `── STEP CLOSE-SESSION` to the end of the
ROUND GATES list) to `.agent/authored/f057-r3.md`; commit alone.
  Subject: `chore(f057): save the R3 block verbatim`
Copy to `.agent/last_block.md`, byte-identical, `cmp` exit 0; commit alone.
  Subject: `chore(f057): point last_block at the R3 block`

Apply every authored text DISK TO DISK out of the committed
`.agent/authored/f057-r3.md`. Never retype one.

── C1 — verdict, finding, resolutions ─────────────────────────────────
File `.agent/live_review.md`. APPEND the block below at the very END, preceded
by exactly one blank line. Change nothing above it. Each `- R-XXXX — ` and each
`Done: R-XXXX — ` is ONE physical line; do not re-wrap.

REVIEWER-AUTHORED. Apply byte for byte. Do not write a `Done:` paragraph of
your own and do not edit these.

>>> GATE-R2 >>>
Gate: R2 — PASS. Verification tier: round gate plus canary. Re-measured by the reviewer against the disk, not read out of the handback: `tests/orchestration/test_rate_governor.py` → `46 passed`, unchanged by C3 because that commit changed an assertion and not a count; `tests/docs/` together with the canary `tests/cli/test_golden_path.py` → `337 passed`, which is the 295 and the 42 the reviewer measured separately at R1; `python3 -m ruff check` scoped to the two feature files → `All checks passed!`, exit 0; `wc -l < .agent/plan.md` → 36; `cmp .agent/authored/f057-r2.md .agent/last_block.md` → exit 0; the R2 block itself is 187 lines, inside the 400-line cap that R-0363 recorded the R1 block breaking. The change set is exactly the seven files the R2 block named, and the Do-not-touch diff over `provider_timeouts.py`, `pingpong_loop.py` and `stream_evidence.py` is still EMPTY at `21c8148e..HEAD`. TRANSPORT proved disk to disk by the reviewer: the GATE-R1 and FINDINGS-R1 slices extracted from the committed `.agent/authored/f057-r2.md` each occur exactly once in `.agent/live_review.md`, both rewrite pairs went FROM 0 occurrences and TO exactly 1, `import dataclasses` is present, and the carried R-0361 line still hashes to `70a8c9fb1a6ddebd2a1592b467cf9cb7e18f43ad0449c245d110bc0f1f056a7b` after two appends. The RED-PROOF was reproduced by the reviewer in its own disposable worktree at `c3222402`, import path printed first and confirmed inside it: removing `frozen=True` from `RateLimitSignal` gives `1 failed, 45 passed`, the single id being `test_signal_is_frozen` failing `DID NOT RAISE <class 'dataclasses.FrozenInstanceError'>` — identical to the worker's report, and proof that the R-0366 fix is load-bearing rather than decorative. No block condition was hit. The round's one red gate was the reviewer's own arithmetic and is recorded as R-0367 below; the worker measured the real value, declared it, and correctly refused to edit the file to reach an impossible number.
<<< GATE-R2 <<>>> FINDING-367 >>>
- R-0367 — Low — the R2 block ordered a numstat that no correct application of its own pair can produce. C2's gate demanded `git show --numstat HEAD -- packages/orchestration/rate_governor.py` → `8 4`. The authored R0365-FROM slice is 4 lines and R0365-TO is 8, and the reviewer derived `8 4` from those two counts. But the final line of both slices is byte-identical — `    counts as X" drift apart, and the drift is the bug.` — so git's diff renders it as CONTEXT rather than as a deletion plus an insertion, and the only reachable measurement is `7 3`, which is exactly what the worker measured and declared. This is pre-emission checklist item 8 (docs/agents/planner_reviewer_prompt.md §3): a done-when may not assert a number the thing that produces it makes impossible, and the expected value must be computed from that producer — here git's diff algorithm — rather than from what the number obviously ought to be. §4.9 sanctions `git show --numstat` as the MEASUREMENT a receipt reports; it does not license predicting the pair in advance. It is also the third reviewer-arithmetic defect of this session, after R-0364's unexecuted ruff gate and alongside R-0363's unmeasured block length, which together say something the individual findings do not: this reviewer's failures are concentrated entirely in numbers asserted about artifacts rather than in the review of the work itself. Counter-measure, binding from the next block on and additive to R-0364's: a block asserts the DATA property — FROM 0 occurrences, TO exactly 1, the changed-paths list, a sha256 over extracted bytes — and never a predicted insertion/deletion pair; where the arithmetic matters it is reported by the round, not ordered by the block. OPEN.
<<< FINDING-367 <<<

>>> DONE-365 >>>
Done: R-0365 — Fixed at `47575d5f`, verified by the reviewer at `c3222402`. The docstring of `is_rate_limit_error` in `packages/orchestration/rate_governor.py` no longer claims that the readers call it. It now says what is true and what the reviewer confirmed by mutation: the predicate is the emptiness test of `classify_rate_limit_reason`, that function owns the single wording table, and the module's readers reach the table through `normalize_rate_limit_signal`. The anti-drift argument it borrows from `is_timeout_error` survives the rewrite, now attached to the function that actually carries the property. Transport was proved disk to disk rather than by retype — the R0365-FROM slice extracted from the committed `.agent/authored/f057-r2.md` occurs 0 times in the module and the R0365-TO slice exactly once. The commit's real numstat is `7 3`, not the `8 4` the block ordered, for the reason recorded as R-0367; the diff touches that one docstring paragraph and nothing else, and `tests/orchestration/test_rate_governor.py` still gives `46 passed` with `ruff check` clean on the file. No code path changed, which is the point: the defect was a false statement about the code, and only the statement moved.
<<< DONE-365 <<<

>>> DONE-366 >>>
Done: R-0366 — Fixed at `08810088`, verified by the reviewer at `c3222402`. `tests/orchestration/test_rate_governor.py::test_signal_is_frozen` now asserts `dataclasses.FrozenInstanceError` instead of a bare `Exception`, with `import dataclasses` added to the stdlib group so ruff's I001 stays satisfied — the reviewer re-ran `ruff check` on the file and got `All checks passed!`, exit 0. `pytest.raises(Exception)` occurs 0 times in the file. The reviewer did not take the fix on trust: it re-ran the RED-PROOF itself, in its own disposable worktree at `c3222402` and never in the primary checkout, proving the import path first (`MODULE /home/decodeux/Repos/remedy/.remedy-wt/rev_r2_red/packages/orchestration/rate_governor.py`, inside the worktree) and then removing `frozen=True` from the `RateLimitSignal` decorator. The suite went to `1 failed, 45 passed`, the single failure being `test_signal_is_frozen` with `Failed: DID NOT RAISE <class 'dataclasses.FrozenInstanceError'>` — so the assertion now fails for the specific reason it exists to catch, rather than for any reason at all. The worktree was removed and pruned and `git worktree list` returned to one line.
<<< DONE-366 <<<

Commit C1 ALONE.
  Subject: `docs(f057): record the R2 verdict and resolve R-0365 and R-0366`
Gates: `Gate: R2 — PASS` → exactly 1 · `- R-0367 — ` → exactly 1 ·
       `Done: R-0365 — ` → exactly 1 · `Done: R-0366 — ` → exactly 1 ·
       `## Steps` → exactly 1 · R-0361 sha256 unchanged

── C2 — handback and session close ────────────────────────────────────
Three files, ONE commit.

(a) `.agent/plan.md` — REPLACE THE WHOLE FILE:

>>> PLAN >>>
# Plan — F057 Rate-limit-aware scheduler

Branch: feature/f057-rate-limit-scheduler, cut from main at 21c8148e. Next free
finding id: R-0368. Open findings: R-0361, R-0362, R-0363, R-0364, R-0367 —
R-0365 and R-0366 are RESOLVED by reviewer-authored `Done:` text at R3.

## Goal
Provider rate limits stop looking like failures. A per-provider governor reads
normalized limit signals out of call evidence and makes a run WAIT visibly —
with a reason and an expected retry — instead of burning retries or failing the
task. Providers that emit no limit signal behave exactly as they do today.

## Current Step
T001 is DONE, reviewed and PASSed over rounds R1-R3: signal normalization lives
in `packages/orchestration/rate_governor.py` with 46 unit tests, an inventory of
the five real evidence shapes, and no wiring into any caller. The session closed
here at its own capacity limit, not at a blocker.

## Next Steps
1. T002 — the governor: per-provider cooldown state fed by `RateLimitSignal`,
   `acquire(provider, role)` with a deadline taken from budgets, an INJECTED
   clock (no real sleeps in unit tests), exponential cooldown with a documented
   cap when the provider gave no `retry_after_s`, and a wait event
   {provider, waited_s, reason}. Stop must beat wait: a stop request during a
   wait interrupts it immediately, so acquire polls in slices rather than
   sleeping once. Design the interface for N concurrent acquirers; implement
   single-flight. Multi-process runs share nothing in v1 — document it.
2. T003 — seam integration in `_call_with_retry`
   (`packages/orchestration/pingpong_loop.py:2142`, which already carries
   `stop_check`), ordered stop, then budget, then acquire; wait evidence; the
   report line; the limit-emitting fixture end-to-end.
3. Integration gate, then closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- The stop-beats-wait ordering is the acceptance criterion most likely to be
  faked by a comment. It needs its own test with an injected clock.
- `is_rate_limit_error` still has no precedence rule against the existing
  transport predicates. T003 decides it with evidence; nothing depends on it yet.
<<< PLAN <<<

(b) `.agent/context.md` — REPLACE THE WHOLE FILE:

>>> CONTEXT >>>
# Context — F057 Rate-limit-aware scheduler

## Active Branch
feature/f057-rate-limit-scheduler, cut from main at 21c8148e. F057 is claimed
`[~]` in docs/roadmap/STATUS.md and stays claimed until closure. No PR exists
for this branch yet; one is created at closure, not before.

## Scope
In: `packages/orchestration/rate_governor.py` and
`tests/orchestration/test_rate_governor.py`, plus `.agent/**` round state and
the one claimed STATUS line. T001 is complete and reviewed; T002 (the governor)
and T003 (the seam) remain.

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
- Unit tests use an injected clock. A real sleep in a unit test is a finding.
- A round pushes after EVERY commit, not once at its last step.

## Steps
R1 claim and T001 ✅ → R2 findings and two fixes ✅ → R3 verdict and session
close ✅ → next session: T002 governor → T003 seam → integration gate → closure.
<<< CONTEXT <<<

(c) `.agent/handoff.md` — rewrite (never append) per AGENTS.md and
docs/agents/handback_template.md. It is the session's ONLY return channel, so
it must carry: feature and round; branch; the commit SHAs of THIS round;
a changed-files table; REAL verification results with real exit codes; the
open-findings count; and the next expected action. Under 60 lines, or carry a
"Deviations, declared" line naming the real count and the mandated content that
caused it (DECISION D15). Include the item-status table with C0a, C0b, C1, C2
each exactly once.

The handoff MUST state, under "Next", in this order:
  1. The next session's first action is Phase 0 of
     docs/agents/self_drive_protocol.md, then Phase 1 rule 1 — re-read
     `.agent/STOP` from disk — BEFORE rule 2.
  2. There is NO open PR for this branch and none should be created until
     closure; the Open PR Gate therefore has nothing to merge.
  3. The work resumes at T002 as specified in `.agent/plan.md`.
  4. This session ended at its own capacity limit with every round reviewed and
     PASSed, not at a blocker — a clean stop, not an interruption.
It must also record that R3 is the session's LAST round and therefore has no
on-disk gate entry of its own, by construction
(docs/agents/planner_reviewer_prompt.md §4 item 13): its verdict lives in this
handoff. That absence is the terminator, not a missing gate — do not let a
later reader open a repair round to close it.

Commit C2 ALONE.
  Subject: `chore(f057): handback R3 and close the session`

── ROUND GATES — run every one, record the REAL exit code ─────────────
 1. `git status --porcelain` → empty
 2. `git worktree list` → exactly one line
 3. `git branch --show-current` → `feature/f057-rate-limit-scheduler`
 4. `Gate: R2 — PASS` in `.agent/live_review.md` → exactly 1
 5. `- R-0367 — ` → exactly 1
 6. `Done: R-0365 — ` → exactly 1 · `Done: R-0366 — ` → exactly 1
 7. `## Steps` in `.agent/live_review.md` → exactly 1
 8. the R-0361 line's sha256 → `70a8c9fb1a6ddebd2a1592b467cf9cb7e18f43ad0449c245d110bc0f1f056a7b`
 9. `wc -l < .agent/plan.md` → under 50
10. `cmp .agent/authored/f057-r3.md .agent/last_block.md` → exit 0
11. `python3 -m pytest tests/orchestration/test_rate_governor.py -q` → exit 0
12. `python3 -m pytest tests/docs/ -q` → exit 0
13. `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0 (canary)
14. `git diff --name-only 36b745bd..HEAD` → only the six files this block names
15. `git diff --stat 21c8148e..HEAD -- packages/orchestration/provider_timeouts.py packages/orchestration/pingpong_loop.py packages/orchestration/stream_evidence.py` → EMPTY

KNOWN-RED BASELINE, per R-0364's counter-measure: repository-wide
`python3 -m ruff check` exits 1 with 26 pre-existing errors at base `21c8148e`.
It is NOT a gate this round, and this round changes no Python file at all.

No numstat is ordered anywhere in this block, per R-0367's counter-measure.

Report every gate with its real output. If a gate goes red, STOP and report the
exact output rather than adjusting a file to satisfy it.
