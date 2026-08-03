# Live Review — F071 Mission dossier (Tier 1)

Branch: feature/f071-mission-dossier
Scope: a maintained, hard-budgeted dossier (GOAL immutable ·
MILESTONES one line each · RISKS open-only · DECISIONS recent with
outcomes · NEXT single step) as the orchestrator's working memory —
rewritten by compression, never truncation. Budget from config
(dossier.max_tokens, default 3000) on the labeled estimate basis.
Live state dossier_state.json; versions dossier_v<N>.md, never
overwritten (R-0173); the maintained document is the loop's prompt
prefix through the assemble_context dossier seam; recall harness
published as a reusable deliverable (F079 reuses it).

## Steps
- R1 (SPLIT, LARGE): claim + T001 + T002 — FAIL on R-0172, see
  Verdicts.
- R2 (SPLIT, LARGE repair+continue): R-0172/0173/0174 fixed + T003
  loop integration + recall harness — FAIL on R-0175, see Verdicts.
- R3 (SPLIT, LARGE repair+gate, current): persist R-0175 → fix →
  re-run the R2 gate (STOP if red) → integration gate per
  docs/agents/integration_gate.md.
- R4: closure per docs/roadmap/STATUS_closure_protocol.md.

## Findings
- R-0172 (product, Medium) 2026-08-03: section-crossing open-item
  loss — rule check judged the answer's raw id lists while
  _rebuild carried per section. Fixed 90141a5d: _check_rules
  judges the REBUILT document and compress_dossier returns that
  same object; cross-section answers refused, pinned by tests.
  Reviewer re-ran the R1 reproduction against the fix: refused
  with "keep every open item: open item(s) R002 were dropped",
  dossier untouched.
  Done: R-0172
- R-0173 (product, Low) 2026-08-03: silent same-version overwrite.
  Fixed e3575f71: byte-identical rewrite is a no-op; differing
  content raises ValueError, original intact; both branches
  pinned.
  Done: R-0173
- R-0174 (docs, Low) 2026-08-03: IterationFacts docstring vs
  merge-by-id behavior. Fixed 55139dab; a restated decision
  replaces its line, pinned.
  Done: R-0174
- R-0175 (product, Medium) 2026-08-03: refresh_mission_dossier
  writes dossier_v<N>.md THEN dossier_state.json, and run_mission
  calls refresh unguarded (orchestrator_loop.py:811). A death
  between the two writes — exactly the F075 harness-death-
  mid-write class (T1_F075.md, operator addition 2026-08-03) —
  leaves the version archive one ahead of the live state. As soon
  as any fact drifts (one new ledger entry suffices), every later
  refresh recomputes the SAME version number with different bytes
  and the R-0173 guard raises ValueError. Reviewer reproduced in
  a scratch root: stale state + one ledger entry → refresh
  raises, and raises again on every retry — the mission is
  permanently wedged until a human edits evidence files. The
  module's own "degraded but never a dead loop" stance
  (load_dossier_state) is broken by its sibling. Fix: reconcile
  before writing — latest = latest_dossier_version(...); if the
  updated dossier's version <= latest, fast-forward to
  latest + 1 via replace(); the archive stays append-only, the
  never-overwrite guard stays intact, and a torn write self-heals
  on the next refresh. Record the fast-forward as the explicit
  exception to the one-update-one-version decision in
  decisions.md. Pin with tests: state one version behind the
  archive plus differing facts → refresh succeeds at latest+1
  with prior files untouched; the following refresh continues
  normally.
  Done: R-0175
- Next free ID: R-0176.

## Verdicts
- R1: FAIL (SPLIT, LARGE, 2026-08-03). Range 097e4959..a2e06afc.
  FAIL on R-0172 (Medium, reviewer-reproduced); R-0173/0174
  registered. Details in git history of this file.
- R2: FAIL (SPLIT, LARGE repair+continue, 2026-08-03). Range
  097e4959..9698306e (16 commits; R1's seven re-tabled grouped,
  accepted). Findings-persist commit 06a37117 cmp 0 against the
  reviewer's scratchpad original; Done-marks appended in the
  fixing commits. Reviewer re-ran: dossier 97, loop 106, canary
  42, docs 293, ruff clean — all exit 0, matching the handback;
  R1's reproduction now refused with the correct detail and an
  untouched dossier. R-0172/0173/0174 fixes verified in the real
  diff. T003 delivered: state/facts/refresh helpers, loop prefix
  wiring through the existing seam, recall harness with negative
  control (the survived-then-killed mutation reported honestly).
  Deviations 1-8 accepted. FAIL on R-0175 (Medium,
  reviewer-reproduced): torn-write wedge from the
  version-then-state write order under the R-0173 guard.
  LAST_REVIEWED_SHA stays 097e4959.
