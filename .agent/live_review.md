# Live Review — Steps 1305-1334: Provider Trust Gate + External Repair Intake v0

Reviewer: parallel reviewer
Scope: Provider Trust Gate + External Repair Intake v0 — treat external model/agent
output as UNTRUSTED: quarantine private, parse, validate trust, emit safe report,
and ONLY when accepted create a pending Repair Patch Intent. Must NOT: invoke any
provider/Ollama/Claude API, make network/subprocess calls, auto-apply/approve,
expose raw provider output/diff/source/secrets/tracebacks/abs paths. Patch Intent
creation only; apply stays via `do continue`.
Timestamp: 2026-06-14

## Verdict
PENDING — block in progress. Builder constructing provider_trust.py + CLI on top of
main 91b4a51 (PR #56 merged). Hard completion criteria (Step 1334) gate the verdict.

## Check Matrix (1-15) — to fill
| Check | Status | Note |
|---|---|---|
| 1. Mainline reconciliation | PENDING | branch off clean main 91b4a51; PR #56 recorded |
| 2. Intake models | PENDING | |
| 3. Private quarantine (0o700/0o600, no public raw) | PENDING | |
| 4. Input limits (size/UTF-8/binary/NUL/traversal) | PENDING | |
| 5. Candidate parser (one patch; JSON or fenced diff) | PENDING | |
| 6. Trust finding taxonomy | PENDING | |
| 7. Secret/raw-leak scanner | PENDING | |
| 8. Path safety validation | PENDING | |
| 9. Patch shape validation | PENDING | |
| 10. Failure link validation | PENDING | |
| 11. Trust decision + Repair Artifact + Patch Intent | PENDING | |
| 12. CLI (intake-repair / trust-show) + catalog + RunContract | PENDING | |
| 13. Integrations (Progress/Feature/Review/Cockpit) | PENDING | |
| 14. Redaction | PENDING | |
| 15. Architecture guards (no network/subprocess/provider SDK) | PENDING | |

## Findings — Steps 1305-1334
(none yet)
