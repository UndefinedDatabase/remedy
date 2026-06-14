# Plan — Steps 1305-1334: Provider Trust Gate + External Repair Intake v0

## Goal
Take UNTRUSTED external model/agent output (local file or stdin), quarantine it,
parse/normalize, validate trust, emit a safe ProviderTrustReport, and ONLY when
accepted create a Repair Artifact + pending Repair Patch Intent → approval_required
→ stop. No provider/API/Ollama execution, no model invocation, no auto-apply, no
auto-approval. Apply stays through `do continue`.

## Current Step
1306 — provider_trust.py models + quarantine + parser + validation

## Steps
- [x] 1305: Mainline reconciliation + clean branch (PR #56 merged; scope→1305-1334)
- [ ] 1306: Intake models (Request/QuarantineRecord/CandidateRepair/TrustReport/Finding/Decision/Result)
- [ ] 1307: Private quarantine storage (0o700/0o600, bounded, hashed, no public raw)
- [ ] 1308: Input size/encoding limits (bytes/UTF-8/binary/NUL/traversal)
- [ ] 1309: Candidate parser (JSON or single fenced unified diff; exactly one patch)
- [ ] 1310: Trust finding taxonomy (codes + severities)
- [ ] 1311: Secret/raw-leak scanner (keys/tokens/passwords/private keys/abs paths/tracebacks)
- [ ] 1312: Path safety validation (relative-only, protected paths reject)
- [ ] 1313: Patch shape validation (bounded files/hunks/lines; delete high-risk; no binary)
- [ ] 1314: Failure link validation (exists/unresolved; link RepairAttempt; overlap→confidence)
- [ ] 1315: Trust decision (blocker/high→rejected; medium→needs_human_review; low→accepted)
- [ ] 1316: Repair Artifact from accepted candidate (linked, no raw export)
- [ ] 1317: Repair Patch Intent (real, pending; linked; catalog approve next action)
- [ ] 1318: CLI provider intake-repair (file/stdin)
- [ ] 1319: CLI provider trust-show (read-only)
- [ ] 1320: Command catalog (intake-repair write_metadata; trust-show read_only)
- [ ] 1321: RunContract (provider_intake/provider_trust_review/create_provider_repair_intent)
- [ ] 1322: Progress Ledger integration
- [ ] 1323: Feature Planner integration (no auto provider/approval)
- [ ] 1324: Review Bundle provider_trust_summary.json
- [ ] 1325: Cockpit read-only provider trust counts
- [ ] 1326: Redaction tests
- [ ] 1327: CLI runtime tests
- [ ] 1328: Architecture guards (no network/subprocess/provider SDK/apply/test-exec imports)
- [ ] 1329: Documentation (provider-trust-gate-v0 + cross-links)
- [ ] 1330: Targeted tests + full pytest once
- [ ] 1331: Live review
- [ ] 1332: PR discipline
- [ ] 1333: Product readiness update
- [ ] 1334: Final handoff

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
