# Live Review — F075 MILESTONE GATE: 10 flawless self-runs (Tier 1)

Branch: feature/f075-self-run-gauntlet
Scope: a gauntlet HARNESS — evaluator + matrix report + a frozen,
versioned set of ten mission orders — that earns autonomy with
data. Flawless per run = start command only + terminal green + all
blocking DoD checks green + zero unknown postmortems + zero open
decisions + host data root byte-untouched (before/after hash). The
evaluator names the F070 era-fixture classes (R-0141/R-0143/R-0144/
R-0145/R-0146/R-0147/R-0148) and the harness-failure injection
classes (provider API error mid-move, truncated model response,
harness death mid-dispatch and mid-write) — each degrades to a
LEDGERED failure, retry within budget, or escalation, never a
silent success. This round the scope gains ONE reviewed product
change: the run_mission exception boundary (DECISION 2026-08-04 in
the R2 verdict) — the loop's own docstring contract ("every
iteration leaves a ledger entry") made true under a raise.

## Steps
- R1 (SPLIT, LARGE): claim + T001 evaluator/matrix/dry-run proof +
  T002 frozen ten-order set — PASS, see Verdicts.
- R2 (SPLIT, LARGE): R1 PASS persisted + R-0178 fixed + T003a
  runner/injection driver/--live CLI; campaign attempt REFUSED at
  preflight on the missing run_mission exception boundary —
  compliant STOP, PASS, see Verdicts.
- R3 (SPLIT, LARGE, current): persist R2 verdict + fix R-0179 and
  R-0180 + the run_mission exception boundary (product change, own
  tests) + unblock the three raise-class injections + campaign
  attempt 1 from ONE invocation, matrix recorded honestly — below
  10/10 is campaign data, not a round failure.
- R4+: campaign iterations until 10/10 stands from one invocation;
  then the integration gate per docs/agents/integration_gate.md.
- Closure per docs/roadmap/STATUS_closure_protocol.md; a passing
  10/10 emits a prepared-but-not-applied config diff + ADR — a
  human applies it, never the harness.

## Findings
- R-0178 (product, Low): non-numeric evidence numbers were silent
  zeros. Fixed a11e089e, reviewer-verified in the diff and by
  rerunning the evidence/evaluator/matrix gates; goldens unchanged.
  Done: R-0178
- R-0179 (product, Low) 2026-08-04, reviewer's R2 read: an
  injection that NEVER FIRED settles as disposition
  ledgered_failure — an ACCEPTED class — so a run that never
  exercised its declared injection can still count flawless while
  its evidence claims a failure-handling that never happened
  (test_gauntlet_injection.py pins this at line 92). Benign today
  only because INJECT_ON_MOVE=1 and reaching `achieved` needs at
  least one move. Fix: a never-fired injection settles to its own
  REJECTED disposition (e.g. injection_never_fired) so the
  evaluator fails the run honestly; update the pinning test and
  the evaluator's REJECTED_DISPOSITIONS; record in decisions.md
  that this tightens the closed set BEFORE any campaign has run
  (pre-freeze, so no ADR needed — T1_F075.md freezes the
  definition at campaign time).
  Fixed in this round's R-0179 commit: DISPOSITION_NEVER_FIRED
  ("injection_never_fired") added to REJECTED_DISPOSITIONS;
  TruncatedResponseInjector.settle uses it; the pinning test now
  asserts the rejected class AND an end-to-end evaluator verdict
  that the run is not flawless. Pre-campaign, so no ADR.
  Done: R-0179
- R-0180 (product, Low) 2026-08-04, reviewer's R2 read:
  run_campaign's docstring promises "a run that dies takes only
  itself down" but its loop has no boundary — only run_mission
  raises are absorbed (inside run_order). A raise from run_order's
  own crash path (evidence write, the re-entered collectors) kills
  the rest of the campaign; in that path `body` can also be
  unbound at the hash-after line (NameError masks the original
  error). Fix: per-order boundary in run_campaign recording a
  synthetic crashed OrderOutcome; initialize body before the try
  or nest the crash path's fallback; one test where the crash
  path itself raises.
- Next free ID: R-0181.

## Verdicts
- R1: PASS (SPLIT, LARGE, 2026-08-04). Range 563b15b4..740ff133.
  Full text in this file's git history (55f706db).
  LAST_REVIEWED_SHA was 740ff133.
- R2: PASS (SPLIT, LARGE, 2026-08-04). Range 740ff133..ef23e274
  (7 commits, all tabled). Transport: r2-1/2/3 cmp 0 against the
  reviewer's scratchpad originals; live_review at the apply commit
  byte-equals the authored text (worker's later append is the
  permitted Done-mark only). Reviewer re-ran every gate: P2 111,
  slice 205, canary 42 — all exit 0 — and re-reproduced the golden
  matrix byte-exact through the CLI. R-0178 fix verified in the
  real diff. The STOP is COMPLIANT and TRUE: reviewer reproduced
  the escape independently (AST: zero try-blocks in run_mission
  698-885 and execute_move; a raising call_fn escaped
  run_structured_call at structured_outputs.py:158 in a live
  probe), so three injection classes are honestly undriveable and
  the preflight refusal spent zero tokens. R-0179/R-0180
  registered from the reviewer's read. DECISION 2026-08-04 (§4.7):
  the missing run_mission exception boundary is built IN THIS
  BRANCH as reviewed SPLIT work with its own tests — alternatives
  considered: a separate feature first (slower, breaks campaign
  momentum for a change this feature's acceptance explicitly
  demands) and a harness-side except (rejected: grades the
  harness's crutch, decisions.md 2026-08-04); reversal = any later
  relay. Worktree hygiene: primary only, porcelain empty.
  LAST_REVIEWED_SHA = ef23e274.
