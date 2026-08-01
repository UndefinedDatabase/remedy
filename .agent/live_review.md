# Live Review — F062 Product smoke as the closing gate (Tier 1)

Branch: feature/f062-product-smoke
Scope: a standard DoD block proving a runnable app STARTS, its core
paths RESPOND, and the console stream is clean, before a job may end
green; not-applicable (no runtime) reported honestly, never silently
green; fixtures are real mini-apps in the test tree. v1 is
HTTP-level — no browser dependency (reject any diff adding one).

## Steps
- R1 (SPLIT): claim + T001 — standard-block registration +
  app_starts + not-applicable path + fixture apps (green-tests/
  broken-start job held open with a concrete probe reason).
- R2 (LARGE, operator LARGE-mode 2026-08-01): T002
  core_paths_respond + path extraction hand-off + fixtures (ok,
  wrong status, missing marker); THEN T003 clean_console +
  documented pattern list + teardown-always (no zombie processes
  even on red) + the smoke config table; THEN the integration gate
  per docs/agents/integration_gate.md — per-slice verification,
  stop-on-red.
- R3: repair — R-0167 (a disabled smoke must not start the app) +
  scoped re-verification.
- R4: closure per docs/roadmap/STATUS_closure_protocol.md.

## Findings
- R-0166 (process, Low) 2026-08-01: handback form, two defects:
  (a) branch not pushed at handback (split_workflow.md single-writer
  rule: hand back only with a clean, committed, PUSHED branch;
  AGENTS.md Push Discipline); (b) the handoff commit (30177869) is
  absent from the handoff's Commits section and Range names HEAD
  1e3e58b0 while the branch head is the handoff commit — the R-0149
  exception allows a grouped self-reference table, not an omission.
  Fix: push as the FIRST action of R2; every later handback follows
  a push and tables ALL commits (grouped self-reference allowed).
  Done: R-0166 (pushed; this handback tables all commits).
- R-0167 (behavior, Low) 2026-08-01: `smoke.enabled = false` does not
  stop execution. The block contributes the honest "disabled by
  config" row (compile-time, pinned by test), but its spec is an
  ordinary `app_starts`, so `_run_product_smoke` still STARTS the
  app at run time — the off switch reports correctly yet still costs
  a full start-probe-stop cycle. Fix: the runner consults
  `smoke_config()["enabled"]` and refuses EARLY (no process started,
  mirroring the not-applicable path) with a distinct reason and the
  "disabled by config" text; pin with a test that a disabled run
  starts nothing (argv empty, duration 0, marker file untouched) and
  is not green. Compile-time contribution stays as is.
  Done: R-0167 (commit b6efe456).
- Next free ID: R-0168.

## Verdicts
- R1: PASS (SPLIT round, 2026-08-01). Range b836d364..1e3e58b0 plus
  handoff commit 30177869 (handoff+last_block only, verified).
  Reviewer re-ran: smoke 27, dod suites+schemas 200, docs 293,
  canary 42 — all exit 0, matching the handback transcripts.
  Transport cmp 0 disk-to-disk against scratchpad originals (both
  texts); STATUS claim FROM 1→0 / TO 0→1. Spot-checks: primary
  worktree only, no registration-by-import (fresh-process providers
  empty), no leaked runtime configs, 7 commits in range as tabled.
  Deviations 1–5 accepted: new check kind product_smoke; kind-set
  pin 5→6; additive StandardCheckContext.worktree_root;
  not-applicable = non-blocking red in reported_red (P6);
  _run_app_once extraction sharing the process discipline, harness
  semantics untouched. R-0166 registered (handback form, Low).
  LAST_REVIEWED_SHA = 30177869.
- R2: PASS — INTEGRATION GATE PASS (LARGE round, 2026-08-01). Range
  30177869..4d78cd12 (10 commits, all tabled). Reviewer re-ran:
  scoped 237 + canary 42, exit 0; OWN full suite at HEAD 14969
  passed / 19 skipped, exit 0 — matching the branch evidence in
  .agent/gate_f062_r2/; base 14900/19 exit 0 (worker raw, count
  delta +69 = exactly test_product_smoke.py); both comm directions
  EMPTY, nothing to attribute, flake debt 0. Transport cmp 0
  disk-to-disk (three texts, scratchpad originals); the worker's
  stray-blank-line application fumble was reverted pre-commit and
  disclosed. R-0166 verified fixed (pushed head = branch head, all
  commits tabled) — Done stands. Deviations 1–4 accepted:
  not-applicable/disabled contribute ONE honest row; path and
  console failures are never retried; clean_console judged before
  any pass; paths REPLACE while error_patterns only ADD. R-0167
  registered (disabled smoke still starts the app, Low). Only this
  round carries the full-suite claim: FULL SUITE GREEN.
  LAST_REVIEWED_SHA = 4d78cd12.
- R3: PASS (repair round, 2026-08-01). Range 4d78cd12..b2c17ea1
  (4 commits, all tabled). Reviewer re-ran: scoped 244 + canary 42,
  exit 0. Fix verified in situ: REASON_SMOKE_DISABLED refusal sits
  AFTER not-applicable and BEFORE any start; DISABLED_MESSAGE one
  shared constant; compile-time row unchanged; 7 pinned tests incl.
  the marker-file process fact; red-proof in a throwaway worktree
  (refusal deleted → 5 failed, marker file present) accepted.
  Transport: cmp 0 disk-to-disk all three texts (scratchpad
  originals); the r3-3 END-marker strip was recovered correctly by
  the hash gate — the transport fault was the relay's, the recovery
  was per protocol. Deviations 1–4 accepted (shared constant; order
  after not-applicable; all kinds refuse; gating untouched).
  R-0167 verified fixed and Done (commit b6efe456). Open findings 0.
  LAST_REVIEWED_SHA = b2c17ea1.
