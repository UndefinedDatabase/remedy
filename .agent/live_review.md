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
  R-0161 (--final guard) + capability cap (A9); integration gate
  RED: one branch-only state-file id (R-0162); all six comm -23
  ids attributed + empirically confirmed. Done (gate outcome
  carried to R4).
- R4: persist R3 verdict + register R-0162; context.md repair 1 —
  fixed the "Steps" reader, tripped the resource-safety reader
  (reviewer-authored text, incomplete reader list); gate stopped
  at step 3 per the stop rule. Done (outcome carried to R5).
- R5: persist R4 verdict; apply the CORRECTED context.md (full
  reader list, validated against all 13 assertions) + the §4
  item 11 grep-every-reader rewrite; re-run gate steps 3-5 (full
  suite + docs + canary) — green required, else STOP. In progress.

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
- Resolved: R-0161 (product, Low) 2026-07-31: --final is refused
  unless the job's cycle_terminal_status is in REPORTED_TERMINALS
  (clean text + JSON error naming the state, --interim hint, never
  auto-renders); capability lines cap at 10 via _capped with the
  honest count line (CALL-2 ruling).
  Done: R-0161 (commit c2d9f790 — guard + tests; cap 9e0b4035).
- Open: R-0162 (process, Low, registered 2026-07-31; AMENDED after
  R4): the R1 context.md rewrite dropped the "Steps" token; the R4
  repair (reviewer-authored) fixed that reader and tripped a second
  one — test_context_mentions_resource_safety asserts "resource" or
  "pytest" in the same file; context.md's real-file readers span 4
  test files with 13 assertions. Fix (R5): corrected authored
  replacement validated against the FULL reader list before
  emission, plus the §4 item 11 rewrite adding the
  grep-every-reader rule. Not feature-code coupled.
- Next free ID: R-0163.

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
- R3: FAIL — INTEGRATION GATE RED (reviewer, 2026-07-31). Range
  1a5af0d..875a199 (content through 9e0b403). Commits A/B/C are
  sound: all 4 authored texts cmp 0 disk-to-disk (primary proof;
  planner_reviewer_prompt.md §4 item 9), applied regions exactly
  once; --final guard and capability cap verified by the reviewer's
  own runs (98 CLI + renderer tests), tests/docs 293, canary 42,
  ruff clean — all exit 0. Gate: branch 1 failed / 14609 passed
  (126s); base in a worktree ON a branch 6 failed / 14484 passed
  (107s); totals reconcile exactly (+120 = the F053 test files).
  comm -23 = 6, all UI-artifact environment class, attributed per
  id AND confirmed empirically (parity + no-auto-build → 17 passed
  at base). comm -13 = 1: test_context_md_no_stale_steps —
  serial-reproducible, reproduced by the reviewer's own run;
  state-file contract, NOT feature code. The worker's refusal to
  fix inside the gate round was CORRECT (the block forbade it);
  the failure is real, so the gate cannot PASS. R-0162 registered;
  the R4 full-suite re-run is the gate confirmation. The declared
  symlink side effect is accepted as benign (gitignored artifact,
  tree clean, ui_server suite green) and the gate doc now orders
  COPY, never symlink. LAST_REVIEWED_SHA stays 1a5af0d.
- R4: FAIL — GATE STILL RED, REVIEWER FAULT (reviewer,
  2026-07-31). Range 875a199..1ae0c42. Worker execution flawless:
  all 6 authored texts cmp 0 (saved copy AND applied region), the
  stop rule honored exactly, and the handback enumerated every
  reader of context.md — that enumeration became the fix's map.
  The red id moved because the R4 context.md text the REVIEWER
  authored satisfied the dashboard contract but not
  test_context_mentions_resource_safety ("resource"/"pytest" in
  the same file) — an incomplete-reader-list error on the
  authoring side. Reviewer's own verification: the new red id
  reproduced serially (1 failed, 0.03s); gate-1/2 greens accepted
  from raw transcripts; counts reconcile (14609 + 1 = 14610); the
  reviewer then enumerated ALL real-file context.md readers
  itself (4 test files, 13 assertions) and validated the R5
  replacement against every one BEFORE authoring it into the
  block. R-0162 stays Open for R5; the grep-every-reader rule is
  codified in the §4 item 11 rewrite. LAST_REVIEWED_SHA stays
  1a5af0d.
