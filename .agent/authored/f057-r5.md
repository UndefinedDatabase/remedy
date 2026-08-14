── STEP T003-prep — F057 Rate-limit-aware scheduler · Round 5 ─────────────
Round base — the SHA every range gate in this block measures from: 5de503c6

Goal: record the R4 verdict, register findings R-0369 and R-0370, close the
coverage gap R-0370 names, and CONFIRM the T003 seam on disk without touching
it — the feature file's own instruction, "Gate T003 on the seam being
confirmed". No production code changes this round.

Bundle — six commits, in this order, pushed after EVERY commit:
  C0a  .agent/authored/f057-r5.md                 save this block verbatim
  C0b  .agent/last_block.md                       byte copy of the saved block
  C1   .agent/live_review.md                      append GATE-R4, FINDING-369,
                                                  FINDING-370
  C2   tests/orchestration/test_rate_governor.py  the R-0370 fix, one test
  C3   .agent/f057_t003_seam_inventory.md         the T003 seam inventory (new)
  C4   .agent/plan.md, .agent/context.md, .agent/handoff.md   handback

Change — C2, tests/orchestration/test_rate_governor.py
  Add exactly ONE test, next to the other governor tests, on the same FakeClock
  helper: a signal never SHORTENS a cooldown already running. The invariant is
  implemented in observe() as
  `self._cooldown_until[provider] = max(self._cooldown_until.get(provider, 0.0),
  now + duration)` and nothing asserts it today, which is finding R-0370.
  Shape: observe a long hint (say 30.0), then observe a short one (say 1.0) for
  the SAME provider without advancing the clock, and assert
  cooldown_remaining_s stayed at the longer value. Mark it @pytest.mark.unit.
  Name it after the property, not after the method.
  Then append to .agent/live_review.md, as the LAST line of that file, a single
  line of your own of exactly this shape, with your real commit SHA:
    Landed: R-0370 — <one line: what changed, which commit>
  Do NOT write a `Done:` paragraph. `Done:` is reserved for reviewer-authored
  text (docs/agents/planner_reviewer_prompt.md §4 item 4); a surviving
  `Landed:` line is exactly what an unreviewed fix should look like on disk.
  That live_review.md edit belongs to C2, the same commit as the test.

Change — C3, .agent/f057_t003_seam_inventory.md (NEW file)
  READ-ONLY analysis of the T003 seam, committed as evidence so the next
  session starts T003 with the seam confirmed instead of re-deriving it. This
  commit touches NO file under packages/ or apps/. Do not create it under
  docs/ — it is round state, not built-system documentation
  (AGENTS.md, Documentation Structure), so it needs no docs/README.md entry.
  Note the neighbouring `.agent/t003_inventory.md` belongs to a DIFFERENT
  feature; this file's name is deliberately distinct.
  Answer each question below from the code, citing the SYMBOL plus its
  distinguishing text and the file:line where you read it. Every citation must
  resolve at 5de503c6 — re-grep each one before committing it. Where the code
  does not answer a question, write that it does not; a stated gap is the
  useful answer and an invented one costs the next round.
   1. The call site. `_call_with_retry` in
      packages/orchestration/pingpong_loop.py — quote the exact line where a
      provider call actually starts, and the line where `stop_check` is
      already consulted. Name what sits between them.
   2. Ordering. The feature file requires stop check, THEN budget check, THEN
      governor acquire. Which of those three exist at the seam today, in which
      order, and at which lines? Name precisely what T003 must insert and
      where.
   3. The deadline. `acquire(deadline_s=...)` wants an ABSOLUTE value on the
      same monotonic scale as the governor's clock. Find what the loop already
      knows about budgets and wall-clock deadlines — the symbol, the file:line,
      and the unit and epoch it is expressed in. If nothing there is already an
      absolute monotonic deadline, say so and name the nearest thing that is,
      because that conversion is T003's real work.
   4. Where the signals come from. The governor is fed by
      `read_run_event_signals` and `read_retry_reason_signals`. At the seam,
      which of the two shapes is reachable, and from which variable? Cite the
      `retry_reasons` append at packages/orchestration/pingpong_loop.py:2211
      and confirm it still reads as the module docstring of
      packages/orchestration/rate_governor.py claims.
   5. The provider identity. `acquire(provider=...)` needs a provider string.
      What does the seam already have in hand — the parameter, its type, and
      whether it can be empty? An empty provider key would put every provider
      in one cooldown bucket, so say what the seam must do about it.
   6. The evidence and report surfaces. Where would a wait event be recorded
      (the cycle-evidence structure the seam already writes to), and where
      would the run report line "waited Ns on provider rate limits this run" be
      emitted? Cite both, or state that one has no obvious home yet.
   7. The regression risk. Name the tests that already cover `_call_with_retry`
      and would have to stay green when T003 lands — file paths, and how many
      tests each holds. Do not run the full suite; scope it to those files and
      report what you ran.

Constraints
  · AGENTS.md in full: self-review loop before EVERY commit, one logical step
    per commit, under 500 INSERTIONS per commit, .agent/plan.md current, clean
    tree, push after every commit.
  · This round touches NO file under packages/ or apps/. The Do-not-touch list
    stands: packages/orchestration/provider_timeouts.py,
    packages/orchestration/pingpong_loop.py,
    packages/orchestration/stream_evidence.py. C3 READS pingpong_loop.py and
    must not modify one byte of it.
  · Never work on main, never force-push, never merge, never create a PR. There
    is no open PR for this branch and none is created before closure.
  · Any destructive check runs ONLY inside a disposable git worktree under
    .remedy-wt/ (gitignored), removed and pruned before the handback.
  · Apply every authored slice DISK TO DISK from the COMMITTED
    .agent/authored/f057-r5.md. Never retype one. Assert the re-read bytes
    equal the extracted bytes and report each slice's sha256.

Done when — every gate below is EXECUTED and its real exit code and real output
recorded in the handback. "Green" as a word is a finding. No gate here asserts a
predicted line count or a predicted numstat pair; where a number matters the
round REPORTS it (finding R-0367).
   1. git status --porcelain → empty at the handback.
   2. git worktree list → exactly one line.
   3. git branch --show-current → feature/f057-rate-limit-scheduler.
   4. cmp .agent/authored/f057-r5.md .agent/last_block.md → exit 0. Report the
      sha256 both files share and the block's line count, which must be ≤ 400.
      Checkpoint: over 400 stops the round after C0b.
   5. In .agent/live_review.md after C1, counted LINE-ANCHORED — a regex match
      at the START of a line, not a substring count anywhere in the file. This
      anchoring is finding R-0369's counter-measure and is not optional: the
      GATE-R4 slice quotes several of these strings inside its own prose, so a
      whole-file substring count of any of them is 2 by construction and
      measuring it that way would order an unreachable number.
        ^Gate: R4 — PASS   → 1
        ^- R-0369 —        → 1
        ^- R-0370 —        → 1
        ^## Steps          → 1
      Report both the line-anchored and the substring count for each, so the
      difference is on the record rather than hidden by the anchoring.
      Also: the line beginning "- R-0361 " still has sha256
      70a8c9fb1a6ddebd2a1592b467cf9cb7e18f43ad0449c245d110bc0f1f056a7b, taken
      over the line INCLUDING its trailing newline — the convention every
      earlier round used, stated here so it is not re-derived.
   6. C1 is a pure APPEND: git show --numstat <C1> -- .agent/live_review.md
      shows 0 deletions. Report the insertion count; do not predict it.
   7. python3 -m pytest tests/orchestration/test_rate_governor.py -q → exit 0.
      Report the passed count. All 58 tests present at 5de503c6 still pass;
      0 failed.
   8. python3 -m ruff check packages/orchestration/rate_governor.py
      tests/orchestration/test_rate_governor.py → "All checks passed!", exit 0.
      The reviewer executed this at 5de503c6 and it passed there.
   9. Canary: python3 -m pytest tests/cli/test_golden_path.py -q → exit 0.
      Report the passed count.
  10. Do-not-touch: git diff --stat 21c8148e..HEAD over the three files named
      under Constraints → EMPTY output. Separately, git diff --name-only
      5de503c6..HEAD must contain no path under packages/ or apps/ at all.
  11. Change set: git diff --name-only 5de503c6..HEAD → exactly the EIGHT paths
      this bundle names, no ninth.
  12. wc -l < .agent/plan.md → under 50. Report the number.
  13. In .agent/live_review.md: exactly one line matching ^Landed: R-0370 —
      and 0 lines matching ^Done: R-0370. Report both counts.
  14. RED-PROOF for the C2 test, inside a disposable worktree under
      .remedy-wt/ and never in the primary checkout, printing the imported
      module's __file__ FIRST to prove the mutated copy is under test: in
      observe(), replace the max(...) guard with the bare `now + duration`, so
      a later short hint can shorten a running cooldown. Report the failing
      test ids and the pass/fail counts. At least one test must fail, and it
      must be the C2 test — if the suite stays green the new test does not
      discriminate the invariant, and THAT is the finding to report, not a
      number to reach. Remove and prune the worktree afterwards; gate 2 proves
      it.
  15. Inventory citations: every file:line in
      .agent/f057_t003_seam_inventory.md is re-checked at 5de503c6 and the
      cited symbol or text is really there. Report the count checked and any
      that failed. A citation that does not resolve is finding R-0353's class
      and must be corrected before the commit, not declared afterwards.

Handback: completion report + rewrite .agent/handoff.md (AGENTS.md: rewritten,
never appended; ≤60 lines, or a "Deviations, declared" line naming the actual
count and the mandated content that caused the overage — DECISION D15). It
carries the per-commit changed-files table, an item-status table covering C0a,
C0b, C1, C2, C3 and C4 exactly once each, the real verification output for all
15 gates, each extracted slice's sha256, and the open-findings count. Open
findings after C1: EIGHT — R-0361, R-0362, R-0363, R-0364, R-0367, R-0368,
R-0369, R-0370. Next free id: R-0371. R-0370 stays OPEN with a Landed: line;
only the reviewer's authored text may close it.
This is the session's LAST round under its declared round cap, so the handoff's
"Next" section names, in order: Phase 0 of docs/agents/self_drive_protocol.md,
then Phase 1 rule 1 — re-read .agent/STOP from disk — BEFORE rule 2, then T003
itself with the inventory from C3 as its starting evidence.

The five authored slices follow. Each marker is alone on its line.

>>> GATE-R4 >>>
Gate: R4 — PASS. Verification tier: round gate plus canary. Every value was re-measured by the reviewer against the disk, never read out of the handback: `tests/orchestration/test_rate_governor.py` → `58 passed`, the 46 that existed at `dae401e1` plus 12 new, 0 failed; `python3 -m ruff check` scoped to the two feature files → `All checks passed!`, exit 0; the canary `tests/cli/test_golden_path.py` → `42 passed`; the four `.agent` contract readers together (`tests/ui_server/test_dashboard_contract.py`, `tests/regression/test_resource_safety.py`, `tests/orchestration/test_test_runner.py`) → `142 passed`, and `tests/docs/` → `295 passed`, so the appended verdict text broke no state-file contract; `wc -l < .agent/plan.md` → 31; `.agent/handoff.md` → 90 lines carrying its DECISION D15 stated-cause line, with every mandated section present — per-commit table, item-status table, slice hashes, all 15 gates; `cmp .agent/authored/f057-r4.md .agent/last_block.md` → byte-equal, both sha256 `ee03a6e0647678d584e778653554ca68577a4c1ee5dd27d5c78c2c4bc48c6254`, 340 lines, inside the 400-line cap. The change set is exactly the nine paths the R4 block named — `git diff --name-only dae401e1..HEAD` lists no tenth — the Do-not-touch diff over `provider_timeouts.py`, `pingpong_loop.py` and `stream_evidence.py` at `21c8148e..HEAD` is EMPTY, and `grep -rn` for the module and the class across `packages/` and `apps/` outside the module itself returns nothing, so T002 is correctly unwired and the docstring's "nothing calls acquire() yet" is true rather than aspirational. C1 measures `4 0` — insertions only, so nothing above the appended text moved — and the carried R-0361 line still hashes to `70a8c9fb1a6ddebd2a1592b467cf9cb7e18f43ad0449c245d110bc0f1f056a7b` after a fourth append. Both authored live_review slices arrived byte-exact. TRANSPORT held disk to disk under a denied `cp`: the worker read the COMMITTED authored blob and wrote the slices with Python, re-reading and hashing each, which is the same proof the ritual asks for by a permitted route. The RED-PROOFS were reproduced by the reviewer in its OWN disposable worktree at `5de503c6`, import path printed first and confirmed inside it (`/home/decodeux/Repos/remedy/.remedy-wt/rev_r4_red/packages/orchestration/rate_governor.py`): deleting the per-slice stop probe gives `1 failed, 57 passed` on `test_stop_beats_wait_when_the_stop_arrives_mid_wait` asserting `'granted' == 'stopped'`, and uncapping the exponential gives `1 failed, 57 passed` on `test_observe_without_a_hint_escalates_and_never_passes_the_cap` asserting `64.0 == 60.0` — the same two tests and the same two assertions the worker reported. The worker's totals read `1 failed, 58 passed` because its runs carried one extra witness test that printed the import path, which it declared; the reviewer printed the path outside the suite instead, so the totals differ by exactly that one test and neither is wrong. The worktree was removed and pruned; `git worktree list` is one line and `git status --porcelain` is empty at this verdict. Stop-beats-wait is therefore proven by a failing mutant and not by a comment, which was this feature's stated risk. No block condition was hit: no fabricated value, no false live indicator, no missing changed-files table, no unverified completion claim, no silent scope change. Two defects found, both in the reviewer's own block and neither charged to the round — R-0369, a gate that counted a string the block's own slice writes into the same file, and R-0370, an implemented invariant the block never ordered a test for. One further observation is deliberately NOT registered as a finding: `2.0 ** (streak - 1)` in `observe` would raise `OverflowError` past streak 1025, which is unreachable because `acquire` resets the streak on every grant that waits nothing, so a run reaches it only by taking 1025 limit signals with no clean call between them; it is recorded here so the next reader does not re-open it.
<<< GATE-R4 <<<

>>> FINDING-369 >>>
- R-0369 — Low — a done-when counted a string that the same block's own slice writes into the same file. Gate 5 of the R4 block ordered `## Steps` to occur exactly 1x in `.agent/live_review.md`, and the block's own GATE-R3 slice ends with the sentence "…and `## Steps` still occurs exactly once", which the same round appends to that same file. The whole-file substring count after C1 is therefore 2 and cannot be 1; the same is true of `Gate: R2 — PASS`, quoted in the same sentence. The worker reported 1, which is the LINE-ANCHORED count and the measurement the contract actually cares about — `docs/agents/planner_reviewer_prompt.md` §4 item 11 requires the `## Steps` SECTION to exist, and `tests/ui_server/test_dashboard_contract.py` asserts the substring's presence, which two occurrences satisfy — so nothing on disk is wrong and the reviewer re-ran all four contract readers at `5de503c6` for `142 passed` to confirm it. The defect is the gate, not the file: it was ambiguous between two measurements that give different numbers, and it went unnoticed only because the worker silently picked the right one. This is the sixth recurrence of the class pre-emission checklist item 2 exists for — "a 'must be 0' done-when may not count a string that any TO slice in the same block writes into that same file" — and item 6's rule that such counts are read against the TARGET's existing content. The check is on disk, was not run, and that is the whole story. Counter-measure, binding from R5 on: every count gate over a file this block also writes states its ANCHORING explicitly, is expressed line-anchored whenever the string is a heading or a record's opening token, and is checked against the block's own slice bytes before emission — and the round reports both the anchored and the substring count so the difference stays visible rather than being absorbed by whichever reading happens to fit. OPEN.
<<< FINDING-369 <<<

>>> FINDING-370 >>>
- R-0370 — Low — an implemented invariant of the governor has no test. `ProviderRateGovernor.observe` in `packages/orchestration/rate_governor.py` sets `self._cooldown_until[provider] = max(self._cooldown_until.get(provider, 0.0), now + duration)`, and its docstring states the property that `max` carries: "A signal never SHORTENS a running cooldown: the stored deadline moves to the later of the two, so a late 1-second hint cannot cancel a 30-second wait already under way." That is load-bearing — a provider that answers a 30-second throttle with a stray 1-second hint would otherwise have the long wait erased and be hammered immediately — and it is exactly the shape of behaviour a later refactor drops without noticing, because every other test passes with the `max` removed. The R4 block's test list ordered eleven properties and this was not among them, so the gap is the reviewer's, not the round's: the worker built and documented the invariant it was told to build. The R4 red-proofs demonstrate the cost precisely — the two mutations that WERE ordered each killed a test, while removing this guard kills nothing. Fix: one test on the existing FakeClock that observes a long hint, then a short one for the same provider without advancing the clock, and asserts the remaining cooldown is still the long one; plus the matching mutation red-proof, so the invariant is pinned the same way stop-beats-wait and the cooldown cap already are. OPEN.
<<< FINDING-370 <<<

>>> PLAN >>>
# Plan — F057 Rate-limit-aware scheduler

Branch: feature/f057-rate-limit-scheduler, cut from main at 21c8148e. Next free
finding id: R-0371. Open findings: R-0361, R-0362, R-0363, R-0364, R-0367,
R-0368, R-0369, R-0370 — R-0365 and R-0366 were resolved at R3. R-0370 carries a
`Landed:` line this round; only reviewer-authored text may close it.

## Goal
Provider rate limits stop looking like failures. A per-provider governor reads
normalized limit signals out of call evidence and makes a run WAIT visibly —
with a reason and an expected retry — instead of burning retries or failing the
task. Providers that emit no limit signal behave exactly as today.

## Current Step
T001 and T002 are built and PASSed. This round records the R4 verdict, registers
R-0369 and R-0370, closes R-0370's coverage gap with one test, and confirms the
T003 seam on disk in `.agent/f057_t003_seam_inventory.md` without touching
`packages/orchestration/pingpong_loop.py`. No production code changed.

## Next Steps
1. T003 — seam integration in `_call_with_retry`
   (`packages/orchestration/pingpong_loop.py`, which already carries
   `stop_check`), ordered stop, then budget, then acquire; wait evidence; the
   report line; the limit-emitting fixture end-to-end. Start from the C3
   inventory: it names the call site, the ordering gap, the deadline conversion
   and the regression tests that must stay green.
2. Integration gate, then closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- The deadline conversion is T003's real work: `acquire` wants an absolute
  monotonic value and the loop's budgets are unlikely to be in that form. The
  inventory names what exists; T003 must not invent a scale.
- Wiring the governor makes `is_rate_limit_error` live for the first time, and
  it still has no precedence rule against the existing transport predicates.
  T003 decides it with evidence.
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
the one claimed STATUS line. T001 and T002 are built and gated; T003, the seam
in `packages/orchestration/pingpong_loop.py`, is all that remains.

Out: the per-call retry policy in `packages/orchestration/provider_timeouts.py`,
parallelism itself, and the provider adapters' internals — the feature file's
Do-not-touch list, verified byte-identical at every round so far.
`packages/orchestration/pingpong_loop.py` is READ this round for the seam
inventory and stays byte-identical until T003 opens it.

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
- Count gates over a file the same block writes state their anchoring and are
  line-anchored for headings and record-opening tokens (R-0369).
- A round pushes after EVERY commit, not once at its last step.

## Steps
R1 claim and T001 ✅ → R2 findings and two fixes ✅ → R3 verdict and session
close ✅ → R4 T002 governor ✅ → R5 R4 verdict, R-0369, R-0370 and the T003 seam
inventory → T003 seam → integration gate → closure.
<<< CONTEXT <<<
