# Live Review — F053 Final & interim report (Tier 1)

Branch: feature/f053-run-report
Scope: one human-readable account per run — the final report writes
automatically at every terminal state, `remedy job report <id>
--interim` renders a labeled snapshot of a running job, and every
number names its basis (P6); a pure RENDERER over existing
structured sources, a missing source renders "not recorded", never
an invented value (docs/roadmap/features/T1_F053.md).

## Steps
- R1: claim + state reset + inspect report + T001 (renderer +
  next-action rule table + three golden terminal fixtures). Done.
- R2 (LARGE): persist R1 verdict + register R-0160 + DECISION D2 +
  feature-file amendment; T002 complete — STATUS-mirror producer,
  terminal-state hook (one report per terminal, regenerated),
  interim against a running fake job, CLI job report + --json,
  tests. Done.
- R3: persist R2 verdict + register R-0161 + DECISION D3; fix
  R-0161 (--final guard) + capability cap (A9); then the
  integration gate per docs/agents/integration_gate.md.
  In progress.

## Findings
- Open: R-0160 (process, Low, registered 2026-07-31): the R1
  red-proof mutation ran in the PRIMARY checkout (reverted, tree
  clean after, honestly declared — not a worker fault). The
  worktree-only rule for mutation checks binds only the reviewer
  (planner_reviewer_prompt.md §4 item 10); no doc binds the worker.
  Risk: a crash between mutate and revert leaves a dirty primary
  tree mid-feature. Fix: codify agent-wide worktree-only red-proofs
  — routed to the next paydown micro-round, not this feature.
  Documented risk until then.
- DECISION D2 (2026-07-31, §4.7, reviewer): the STATUS-mirror
  producer the feature file presumes exists does not (R1 inspect
  evidence, confirmed by the reviewer). T002 ADDS it: a read-only
  parser (packages/orchestration/status_mirror.py) that builds
  run_report.StatusMirror when docs/roadmap/STATUS.md exists in the
  target repo, else None ("not recorded" — non-self runs have no
  milestone). The next-action rule table gains a stopped-by-operator
  rule ranked between open-decision and blocked-failed. Alternatives
  considered: render "not recorded" forever (rejected: the Design
  line demands a computed distance, never hand-maintained); a
  separate feature (rejected: two sections of THIS feature's report
  depend on it). Reversal: any later relay may split the producer
  out; the ReportSources.status_mirror seam is unchanged either way.
- Open: R-0161 (product, Low, registered 2026-07-31): `remedy job
  report <id> --final` on a job that is NOT at a reported terminal
  renders a report with no INTERIM banner — the exact
  mislabeled-snapshot risk the banner exists to prevent, one typo
  away. Fix (R3): refuse --final unless the job's
  cycle_terminal_status is in REPORTED_TERMINALS; clean error (also
  as JSON under --json) naming the state and pointing to --interim;
  never auto-render. Plus the CALL-2 ruling attached here:
  accepted-capability lines cap via _capped with an honest "and N
  more" line (A9 — the report is a summary; 28 lines today, ~250 at
  roadmap end).
- DECISION D3 (2026-07-31, reviewer, practice-requires-pointer §2):
  integration_gate.md step 2 gains the base-worktree-on-a-BRANCH
  sentence — the dogfood branch guard refuses a detached HEAD by
  design, so a detached base worktree fails the guard-dependent ids
  for a new named cause (paydown-0731 negative-control evidence).
  Until now that lived only in session memory — exactly the A1
  class the §2 rule exists to catch. Reversal: revert the doc line.
- Next free ID: R-0162.

## Verdicts
- R1: PASS (reviewer, 2026-07-31). Range 15105dbe..840d2b7
  (content through 551b6ec6; handback 0ea37fb + block-executed mark
  after). Both authored texts cmp 0 disk-to-disk against the
  reviewer originals (primary proof, scratchpad alive;
  planner_reviewer_prompt.md §4 item 9). STATUS claim: line 39
  only, old 1→0 new 1. Reviewer's own runs: test_run_report 44,
  tests/docs 293, canary 42, ruff clean, strict-marker run clean —
  all exit 0. Diff read fully bottom-up: render_report_from_sources
  is genuinely pure (no clock/disk/randomness; the interim clock
  lives only in the impure render_report wrapper), the P6
  not-recorded rule is enforced by negative tests (invented-zero
  red-proof reproduced by the worker, 3 tests bite), P1 capability
  split pinned, A9 caps honest, 4-way commit split at real seams —
  no oversize commit. Inspect FINDING confirmed by own search: no
  production reader of docs/roadmap/STATUS.md exists → DECISION D2
  routes the producer to T002 (feature-file amendment authored this
  round). Worker red-proof ran in the PRIMARY checkout (reverted,
  tree clean, honestly declared) → R-0160 registered: the
  worktree-only mutation rule binds only the reviewer today (§4
  item 10). LAST_REVIEWED_SHA = 840d2b7.
- R2: PASS (reviewer, 2026-07-31). Range 840d2b7..1a5af0d (content
  through 4e5713ab; handback 1a5af0d after). All 4 authored texts
  cmp 0 disk-to-disk against the reviewer originals (primary proof;
  planner_reviewer_prompt.md §4 item 9); each applied region occurs
  exactly once (reviewer's own count proof). Reviewer's own runs:
  run_report + hook + CLI 106, self_healing_cycles 50 (executor
  regression clean), tests/docs 293, canary 42, ruff clean — all
  exit 0. Diff read fully bottom-up: status_mirror.py is genuinely
  read-only and None-on-doubt; live spot-check against the real
  ledger agrees with the reviewer's own hand count (F075,
  remaining 8, accepted 28, in-progress F053 only). Terminal hook
  verified: single seam _apply_terminal, REPORTED_TERMINALS pinned
  to exactly five, max_cycles_reached excluded with its own test,
  regenerate-never-append pinned, a write failure never kills the
  run, and the real-loop test reaches the hook through run_cycles.
  Worker red-proofs ran in a disposable worktree — R-0160 honored.
  RULING deviation 1 ACCEPTED: --final/--interim on the existing
  job.report command (F047 one-command precedent; bare view pinned
  unchanged by a test). RULING deviation 2 NOT accepted as-is:
  28 un-capped "Can now" lines violate the report-is-a-summary
  rule (A9) — cap ordered in R3. R-0161 registered: --final on a
  still-running job renders an unbannered report.
  LAST_REVIEWED_SHA = 1a5af0d.
