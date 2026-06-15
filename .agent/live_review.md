# Live Review — Steps 1681-1716: External Builder Sandbox v0

Reviewer: parallel reviewer (independent; owns verdict — builder self-report does not set verdict, protocol §5)
Scope: INGRESS sandbox for EXTERNAL builder candidates — safe request-package export, quarantined
external candidate submission, bridge into the EXISTING Trust Gate → Verification → Materialization
seams, candidate quality evaluation for external submissions, READ-ONLY routing feedback, safe
progress/review/cockpit summaries, docs/tests/integrity. Sandbox is INGRESS, NOT execution. Must NOT:
execute external providers, call Claude/Pi/OpenAI/Ollama, use network/browser/subprocess/MCP, auto
apply/approve/test/repair, automate git commit/branch/PR, or build a model/route tournament.
NO PR unless user asks (Step 1716).
Timestamp: 2026-06-15

## Verdict (reviewer-owned)
PENDING — block just started. New branch `feature/steps-1681-1716-external-builder-sandbox-v0` off
clean merged main `7cec21c` (PR #67 merged Candidate Quality Evaluation v1; reviewer verdict PASS
@ 7729b89). Zero block commits (`git log main..HEAD` empty). No code to verdict yet. Merge-ready
CANNOT be claimed while this verdict is PENDING.

## Check Matrix (1-14)
| Check | Status | Note |
|---|---|---|
| 1. Mainline closure (Candidate Quality v1 PASS respected; no scope before closure) | PASS | branch off 7cec21c (merged main); 0 drift commits |
| 2. Scope boundary (sandbox is ingress, not execution) | PENDING | |
| 3. Request package safety (safe context only; no raw/protected leaks) | PENDING | |
| 4. Storage/quarantine (raw/private separated from public summaries) | PENDING | |
| 5. Submission intake (bounded; protected; no traversal/symlink/binary unsafe) | PENDING | |
| 6. Trust/verification bridge (external candidate stays untrusted until verified) | PENDING | |
| 7. Candidate Quality (evidence-only; ceilings preserved) | PENDING | |
| 8. Routing feedback (read-only confidence only; no auto generation) | PENDING | |
| 9. Progress/Feature/Review/Cockpit (safe summaries; no fake live state) | PENDING | |
| 10. CLI/catalog/run contract (catalog-valid; non-executable classifications) | PENDING | |
| 11. Redaction (no raw/secret/path/log/diff/traceback public) | PENDING | |
| 12. Architecture guards (no forbidden imports/calls) | PENDING | |
| 13. Tests (targeted + full suite reported) | PENDING | |
| 14. Handoff (changed-files table, risks, non-goals, next block) | PENDING | |

## Negative-test checklist (reviewer must verify)
| # | Case | Status |
|---|---|---|
| 1 | Candidate fake "tests passed" claim → no proof promotion | PENDING |
| 2 | Candidate secret-looking token → not public | PENDING |
| 3 | Candidate absolute path → not public | PENDING |
| 4 | Candidate `diff --git` → not public | PENDING |
| 5 | Candidate oversized → rejected safely | PENDING |
| 6 | Candidate symlink / path traversal / protected path → rejected safely | PENDING |
| 7 | Rejected candidate → low score / no intent | PENDING |
| 8 | Pending approval → not completed | PENDING |
| 9 | Routing poor history → human-review recommendation only | PENDING |
| 10 | Routing recommendation creates/runs/generates nothing | PENDING |

## Findings — Steps 1681-1716
(none yet)

Next id: R-0091.

## Reviewer audit log
- PR #67 merged Candidate Quality Evaluation v1 (1645-1680) to main → `7cec21c`; reviewer verdict
  PASS @ `7729b89`. New branch `feature/steps-1681-1716-external-builder-sandbox-v0` off `7cec21c`
  (clean merged main). `git log main..HEAD` empty → no drift, no block code yet. Check 1 PASS.
- WATCH: sandbox is INGRESS only — external candidate text is UNTRUSTED and must flow through the
  EXISTING quarantine → Trust Gate → Verification → Materialization pipeline (no direct parse-to-
  intent, no pre-trust materialization, no trusting external candidate). Quality eval must reuse the
  evidence-only ceilings (no model confidence / self-claim / "tests passed" / raw text). Routing
  feedback read-only (no auto generation / no worker exec). Intake must reject traversal/symlink/
  protected/binary/oversized safely. NO provider/network/subprocess/browser/MCP/git/apply/approve/
  test/PR. Public surfaces = codes/IDs/counts only. Idempotent. next actions catalog-valid (R-0088).
