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
- R3: closure per docs/roadmap/STATUS_closure_protocol.md.

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
- Next free ID: R-0167.

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
