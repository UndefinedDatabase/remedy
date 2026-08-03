# Live Review — F071 Mission dossier (Tier 1)

Branch: feature/f071-mission-dossier
Scope: a maintained, hard-budgeted dossier (GOAL immutable ·
MILESTONES one line each · RISKS open-only · DECISIONS recent with
outcomes · NEXT single step) as the orchestrator's working memory —
rewritten by compression, never truncation. Budget from config
(dossier.max_tokens, default 3000) on the labeled estimate basis
(P6, decisions.md 2026-08-03). update() appends iteration facts;
over budget → ONE schema-validated compression call under explicit
rules; failed compression keeps the previous dossier plus raw facts
and FLAGS over-budget honestly. Versions dossier_v<N>.md; the
dossier is the stable PREFIX of the orchestrator prompt.

## Steps
- R1 (SPLIT, LARGE): claim + T001 + T002 — FAIL on R-0172, see
  Verdicts.
- R2 (SPLIT, LARGE repair+continue, current): persist findings →
  fix R-0172/R-0173/R-0174 → re-run the R1 gate (STOP if red) →
  T003 loop integration through the assemble_context dossier seam
  (prefix position asserted) + recall harness (seeded 10-fact
  fixture, reusable deliverable).
- R3: integration gate per docs/agents/integration_gate.md.
- R4: closure per docs/roadmap/STATUS_closure_protocol.md.

## Findings
- R-0172 (product, Medium) 2026-08-03: compression_rule_violation
  verifies "keep every open item" against the UNION of ids in
  answer.milestones + answer.risks, but _rebuild carries PER
  SECTION (carry() drops any id absent from that same section of
  the previous dossier). An open item returned under the wrong
  section passes the check and is silently dropped from the
  rebuilt dossier. Reviewer reproduced: open risk R002 returned
  inside "milestones" → status "compressed", open_items loses
  R002 (mission_dossier.py:491-521 vs :550-572). Silent open-item
  loss is the exact failure class the module exists to prevent.
  Fix: validate the REBUILT document — rebuilt =
  _rebuild(previous, answer); refuse unless {open ids of previous}
  ⊆ {ids of rebuilt.milestones + rebuilt.risks}; keep the
  invented-id and resolved-risk checks; compress_dossier returns
  the rebuilt dossier only after it passes. Pin with tests: open
  risk under "milestones" refused with "keep every open item" in
  the detail; open milestone under "risks" refused; a refused
  answer leaves the dossier untouched.
  Done: R-0172
- R-0173 (product, Low) 2026-08-03: write_dossier_version
  overwrites an existing dossier_v<N>.md silently (unconditional
  write_text) while the module doc and its own docstring promise
  versions are never overwritten;
  test_no_version_is_ever_overwritten writes two DIFFERENT
  versions, so the promise is untested. A same-version rewrite
  from a reused base dossier would destroy audit evidence. Fix: a
  byte-identical rewrite is a no-op returning the path; differing
  content raises ValueError naming path and version, original
  bytes intact. Pin both branches with tests.
- R-0174 (docs, Low) 2026-08-03: the IterationFacts docstring says
  "Decisions always append — they are a history", but append_facts
  routes decisions through _merge_by_id, so a restated decision id
  REPLACES its line. Behavior is correct (one home per fact); the
  sentence is wrong. Fix: the docstring states the merge-by-id
  semantics.
- Next free ID: R-0175.

## Verdicts
- R1: FAIL (SPLIT, LARGE, 2026-08-03). Range 097e4959..a2e06afc
  (7 commits, all tabled; plan-at-claim cmp 0). Reviewer re-ran:
  dossier 64, canary 42, config+loop 162, docs 293, ruff clean —
  all exit 0, matching the handback. Transport: cmp 0 against the
  reviewer's scratchpad originals for all four authored texts;
  applied state files cmp 0; STATUS claim FROM 1→0, TO 0→1.
  Deviations 1-7 accepted (split commits · one call/no retry ·
  goal rule as schema shape · estimate basis · lazy loop import ·
  one version per update · declared token-cap overrun). FAIL on
  R-0172 (Medium, reviewer-reproduced): section-crossing
  open-item loss through the compression rule check. R-0173 and
  R-0174 registered. LAST_REVIEWED_SHA stays 097e4959.
