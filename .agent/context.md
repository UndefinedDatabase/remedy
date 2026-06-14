# Context

## Active Branch
feature/steps-1305-1334-provider-trust-gate-v0 (forked from clean main at 91b4a51
after PR #56 merged Bounded Overnight Executor v0). No drift.

## Mainline reconciliation (Step 1305)
- PR #56 MERGED → main. Current main commit: 91b4a51.
- Bounded Overnight Executor v0 landed: overnight_executor.py + `remedy overnight run`
  (foreground; one-cycle; explicit --allow-one-cycle + action flag; no daemon/
  scheduler/background/repeat; no provider/Ollama; no subprocess/generic runner;
  no double-apply/test/propose on retry). Progress/Feature/Review(16 sections)/
  Cockpit integrated. Full suite 5518 passed, 8 skipped, 1 deselected.

## Scope
Steps 1305-1334: Provider Trust Gate + External Repair Intake v0. Turn UNTRUSTED
external model/agent output (file/stdin) into a quarantined, validated, trust-
reported, optional Repair Artifact + pending Repair Patch Intent. NO provider
execution. Input is a local file/stdin; intake → quarantine → parse → trust
validation → ProviderTrustReport → optional artifact+intent → approval_required.

## Carried residual risks
- Provider-backed source repair NOT built (this block only INTAKES external output;
  next block: Provider-backed Repair Builder v0 wires real builders behind this gate).
- Fixture repair builder is docs-only by design (limited).
- Bounded overnight executor is single-cycle, foreground only (no loop/scheduler).
- UI `npm run lint` pre-existing TS parser/dependency blocker (no deps allowed).
- Pre-existing deselected `test_project_brain.py::...::test_full_chain_order`
  (always `-k "not test_full_chain_order"`).

## Provider Trust Gate constraints (block 1305-1334)
- NO direct provider/Ollama/Claude API integration, NO model invocation, NO network,
  NO subprocess, NO shell=True. Input is a local file or stdin only.
- External output is UNTRUSTED → quarantine privately (0o700 dir / 0o600 file,
  bounded size, content hash, no overwrite). Raw input NEVER exported publicly.
- No raw provider output/source/diff/stdout/stderr/artifact-body/secrets/tracebacks/
  abs paths in any public surface (CLI/trust-show/events/Progress/Feature/Review/Cockpit).
- Patch Intent creation ONLY; approval_required; apply remains via `do continue`.
- Accepted ≠ applied ≠ approved ≠ verified. No auto-apply/approval/revert/loop.
- blocker/high finding → rejected; medium → needs_human_review; unparseable → needs_human_review.
- Protected/abs/traversal paths rejected; secret-bearing rejected; exactly one patch.
- Every next safe action catalog-backed; no fake intent IDs.

## Resource safety (standing)
- No background pytest. Use `scripts/remedy_pytest.sh` (flock-serialized) for
  Remedy's own tests; full suite once at block end. No shell=True, no subprocess.

## Foundation reused
- approval_queue: patch intents are explanation entries on an Artifact's metadata
  `patch_intent_explanations` keyed by make_intent_id(artifact.id, idx);
  list_patch_intents / get_patch_intent / set_approval_state.
- repair_loop build_fixture_repair pattern (Artifact + patch_intent_explanations).
- run_contract: ContractAction (ALL_KNOWN_ACTIONS auto-derived from class vars),
  _DEFAULT_ALLOWED_ACTIONS, evaluate_run_action; CLOUD_PROVIDER denied via no_cloud.
- Review Bundle REQUIRED_SECTIONS currently 16; add provider_trust_summary.json → 17.

## Product readiness — Bounded Overnight Executor v0 (prior block)
Foreground one-step executor; report-only default; explicit flags; no provider/loop.

## Product readiness — Provider Trust Gate v0 (Step 1333)
CAN: ingest UNTRUSTED external model/agent output (local file or stdin) safely —
quarantine raw bytes privately (0o700/0o600, hashed, never public), parse a
conservative v0 candidate (JSON or one fenced unified diff), trust-validate (secret
scan, path safety, patch shape, failure link), emit a safe ProviderTrustReport, and
ONLY when accepted create a Repair Artifact + ONE pending Repair Patch Intent.
Surfaced in Progress/Feature/Review Bundle (provider_trust_summary.json)/Cockpit.
CANNOT (by design): NO provider/Ollama/Claude API execution, NO model invocation,
NO network, NO subprocess. Accepted ≠ applied ≠ approved ≠ verified — apply still
requires `remedy patch approve` + `do continue`. No raw output/diff/source/secrets/
tracebacks/abs paths on any public surface.
Next block can wire a real (local-first, gated) provider builder BEHIND this gate —
the gate stays the trust boundary; the builder just produces the candidate.

## Next block
Provider-backed Repair Builder v0.
