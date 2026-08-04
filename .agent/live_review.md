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
silent success. The harness adds no product code paths; product
fixes found by the campaign go through normal orders (T003).

## Steps
- R1 (SPLIT, LARGE): Open PR Gate (PR #178 merged) + claim + T001
  evaluator/matrix/dry-run proof + T002 the frozen ten-order set —
  PASS, see Verdicts.
- R2 (SPLIT, LARGE, current): persist the R1 verdict + fix R-0178
  + T003a live runner (isolated data root per run, real-root hash
  before/after, injection driver, evidence in the recorded
  schema) + campaign attempt 1: the full gauntlet from ONE
  invocation, matrix recorded honestly — a result below 10/10 is
  campaign data, not a round failure.
- R3+: campaign iterations — targeted fix orders + full reruns —
  until 10/10 stands from one invocation; then the integration
  gate per docs/agents/integration_gate.md.
- Closure per docs/roadmap/STATUS_closure_protocol.md; a passing
  10/10 emits a prepared-but-not-applied config diff + ADR — a
  human applies it, never the harness.

## Findings
- R-0178 (product, Low) 2026-08-04, reviewer's R1 read:
  gauntlet_evidence._as_number promises "a malformed number is a
  load error, never a silent zero" but returns the default
  silently — a run.json with a non-numeric wall_seconds or tokens
  value renders as 0 in the matrix, understating cost in the very
  report a human reads before flipping defaults. Fix: a
  non-numeric wall_seconds/tokens value becomes a load_error
  (malformed evidence, run not flawless), so the docstring stands
  as written; one falsification test per field.
  Fixed in this round's R-0178 commit: a non-numeric wall_seconds or
  tokens value — and a non-object tokens — becomes a load_error, so
  the run is not flawless and no criterion is reported green. Honest
  edges kept: an absent field still defaults (absence is not
  malformation), a bool is not a number, a numeric string is a type
  error rather than a value to coerce. Falsification per field plus
  one test that the run loses its pass; both golden matrices
  unchanged.
  Done: R-0178
- Next free ID: R-0179.

## Verdicts
- R1: PASS (SPLIT, LARGE, 2026-08-04). Range 563b15b4..740ff133
  (13 commits, all tabled). Transport: all four authored files cmp
  0 against the reviewer's scratchpad originals; applied files
  hash-identical to their authored copies. Reviewer re-ran both
  slice gates (evaluator 63, orders 34), siblings 44, canary 42,
  docs 293 — all exit 0 — and independently reproduced BOTH golden
  matrices byte-exact via the CLI over the recorded set (exit 1,
  5/9 flawless, exactly as recorded). Frozen set verified: ten
  orders, two of each kind, all four injection classes exercised,
  distinct risks in prose; the era mapping covers all seven R-ids
  the operator named. No existing product module touched — the
  range adds new files only. Deviations 1–5 accepted (module
  split: the seam is real and both slice gates ran as ordered).
  R-0178 registered from the reviewer's own read. Worktree
  hygiene: primary checkout only, porcelain empty at verdict.
  LAST_REVIEWED_SHA = 740ff133.
