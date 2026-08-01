# Live Review — F061 Definition-of-Done compiler (Tier 1)

Branch: feature/f061-dod-compiler
Scope: user intent + Flight Plan compile into a machine-checkable DoD
(versioned schema; checks with blocking flags); runners execute checks
with per-check evidence; the job-end gate (T004) holds a job open on a
red blocking check. Compiler is an LLM step with intake/plan
discipline: schema-enforced, parse-retried, honest deterministic
fallback labeled compiled=false.

## Steps
- R1 (LARGE): T001 schema + compiler + deterministic fallback + three
  fixture missions with golden DoDs + acceptance-traceability rule,
  then T002 runners (pytest/lint/build/custom_cmd) with per-check
  evidence, each kind proven red and green — PASS.
- R2 (LARGE): persist + fix R-0164, then T003 runtime_flow runner on
  the runtime harness + fixture app flow, then T004 job-end gate +
  report matrix + CLI matrix view + end-to-end — awaiting handback.
- Later: integration gate; closure is its own round.

## Findings
- Open: R-0164 (hardening, Low) 2026-08-01: validate_check_spec
  accepts flag-shaped first tokens — a pytest selector like "-x" (or
  a lint/build tool, or custom_cmd argv[0], like "--version") passes
  compile-time validation; a flag-shaped selector then lands in the
  pytest argv as an option and silently changes what runs. The
  feature file orders detectable nonsense refused at compile time.
  Fix: refuse values starting with "-" for pytest selector, lint/build
  tool, and custom_cmd argv[0] in validate_check_spec; one negative
  test per field.
  Done: R-0164 (commit af5c39d7).
- Next free ID: R-0165.

## Verdicts
- R1: PASS (SPLIT round, 2026-08-01). Range 1869d89a..785f8cbd.
  Reviewer re-ran at HEAD: scoped 89 passed, tests/docs 293 passed,
  canary 42 passed — all exit 0; tree porcelain-empty; `git worktree
  list` = primary only. Transport: all four authored texts cmp 0
  disk-to-disk against the reviewer scratchpad originals (primary
  proof); applied live_review/plan/context each cmp 0 against their
  authored files; STATUS TO-line occurs exactly once, FROM-line zero
  times. The worker's declared A9 deviations 1–10 ACCEPTED, notably:
  SCHEMA_REGISTRY registration deferred (registry has no production
  consumer; one-line follow-up), provider answers in DoDDraft so it
  cannot label provenance or claim compiled, acceptance checks group
  by selector (rule asks coverage, not duplicate processes),
  executable allowlist shared with test_runner, F017 fences enforced
  as execution location, runners return evidence not verdicts (gate
  is T004). Phase-0 deviation (last_block.md checkout collision,
  recovered, no content lost, net effect exactly the gate's order)
  ACCEPTED. Round tier: scoped gates + canary + docs gate. R-0164
  registered (Low); fix ordered in R2. No mutation checks ran.
  LAST_REVIEWED_SHA = 785f8cbd.
