# T1_F251 — Full-suite stabilization (flake-debt paydown)
**Tier 1 · Registered work item (operator decision 2026-07-27) · Executes
before F050 · Blocks/used by: gate discriminability, the F075 baseline**

## Goal & Done (operator scope ruling 2026-07-27)
The full suite on main churns at ~150–215 failures per `-n auto` run, in
both directions between runs; gate discriminability must be restored
before the self-run phase. DONE when three consecutive full-suite runs
(`python3 -m pytest -n auto -q`) on the result branch produce identical
failure sets, and that set is empty except for explicitly quarantined
tests.

## Rules (operator scope ruling 2026-07-27)
- Quarantine = visible, tracked mechanism: marker/skip with reason string
  + backlog reference per test; follow an existing repo convention or
  create a minimal one. Never deletion, never blanket directory skips,
  never weakened assertions.
- Each standing failure class gets an explicit per-class decision
  (root-cause fix or quarantine-with-reason), named one by one in the
  handback: the ~14 catalog/discovery failures, the 3 .agent contract
  failures, the supervisor/probe xdist classes, the integrity-check
  live_review_verdict matcher gap.
- Root-cause fixes preferred where cheap; typical xdist suspects to check
  first: shared tmp/data paths, port collisions, test-order dependencies,
  global process/env state. Hermetic fix beats quarantine.
- Record full-suite wall time before/after. A flaky test exposing a REAL
  product bug is a finding per normal rules.

## Out of scope
New product features, CLI work, executor changes beyond what a
hermetic-test fix strictly requires.

## Deliverable
The handback's final line: "full suite on main: N quarantined,
0 churning" — the baseline F075's gauntlet inherits.

## Relation to F135/F052
Neither feature carries this repo-suite stabilization scope: F135
(Tier 7 flaky detector) productizes history-based detection inside
Remedy's verify evidence and depends on unbuilt F061; F052 consumes
verify failures of Remedy-run cycles at runtime. Both stay in place;
this registered work item pays the debt directly. The quarantine
convention created here should anticipate the F135 marker convention
(explicit reviewed marker change; quarantined tests stay visible in
reports).
