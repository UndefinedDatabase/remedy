# Plan — Steps 1305-1334: Provider Trust Gate + External Repair Intake v0

## Goal
Take UNTRUSTED external model/agent output (local file or stdin), quarantine it,
parse/normalize, validate trust, emit a safe ProviderTrustReport, and ONLY when
accepted create a Repair Artifact + pending Repair Patch Intent → approval_required
→ stop. No provider/API/Ollama execution, no model invocation, no auto-apply, no
auto-approval. Apply stays through `do continue`.

## Current Step
DONE — full suite 5568 passed; verdict PASS WITH RISKS; ready to merge alone

## Steps
- [x] 1305: Mainline reconciliation + clean branch (PR #56 merged; scope→1305-1334)
- [x] 1306: Intake models (Request/QuarantineRecord/CandidateRepair/TrustReport/Finding/Decision/Result)
- [x] 1307: Private quarantine storage (0o700/0o600, bounded, hashed, no public raw)
- [x] 1308: Input size/encoding limits (bytes/UTF-8/binary/NUL/traversal)
- [x] 1309: Candidate parser (JSON or single fenced unified diff; exactly one patch)
- [x] 1310: Trust finding taxonomy (codes + severities)
- [x] 1311: Secret/raw-leak scanner (keys/tokens/passwords/private keys/abs paths/tracebacks)
- [x] 1312: Path safety validation (relative-only, protected paths reject)
- [x] 1313: Patch shape validation (bounded files/hunks/lines; delete high-risk; no binary)
- [x] 1314: Failure link validation (exists/unresolved; link RepairAttempt; overlap→confidence)
- [x] 1315: Trust decision (blocker/high→rejected; medium→needs_human_review; low→accepted)
- [x] 1316: Repair Artifact from accepted candidate (linked, no raw export)
- [x] 1317: Repair Patch Intent (real, pending; linked; catalog approve next action)
- [x] 1318: CLI provider intake-repair (file/stdin)
- [x] 1319: CLI provider trust-show (read-only)
- [x] 1320: Command catalog (intake-repair write_metadata; trust-show read_only)
- [x] 1321: RunContract (provider_intake/provider_trust_review/create_provider_repair_intent)
- [x] 1322: Progress Ledger integration
- [x] 1323: Feature Planner integration (no auto provider/approval)
- [x] 1324: Review Bundle provider_trust_summary.json
- [x] 1325: Cockpit read-only provider trust counts
- [x] 1326: Redaction tests
- [x] 1327: CLI runtime tests
- [x] 1328: Architecture guards (no network/subprocess/provider SDK/apply/test-exec imports)
- [x] 1329: Documentation (provider-trust-gate-v0 + cross-links)
- [x] 1330: Targeted + full pytest once (R-0083 + resource-safety fixed)
- [x] 1331: Live review
- [x] 1332: PR discipline
- [x] 1333: Product readiness update
- [x] 1334: Final handoff

## Hard rules
- NO provider/Ollama/Claude API execution, NO model invocation, NO network, NO subprocess.
- External output is UNTRUSTED → quarantine private (0o700/0o600), never public.
- No raw provider output/source/diff/stdout/stderr/artifact-body/secrets/tracebacks/
  abs paths in ANY public surface (CLI/trust-show/events/Progress/Feature/Review/Cockpit).
- Patch Intent creation ONLY; approval_required; apply stays via `do continue`.
- Accepted ≠ applied, ≠ approved, ≠ verified.
- blocker/high finding → rejected; medium → needs_human_review; unparseable → needs_human_review.
- Protected paths rejected; secret-bearing rejected; exactly one patch candidate.
- Every next safe action catalog-backed; no fake intent IDs.

## Next block
Provider-backed Repair Builder v0.
