# Live Review — Steps 2506-2585: Controlled Claude Code Operator Path v0

Reviewer: parallel reviewer (independent; owns verdict — builder self-report does not set verdict;
a builder `Done:` marker is NOT reviewer `Resolved`).
Scope (ALLOWED): CLI template enable/disable/update; package-bound placeholder resolution;
adapter/template/session/approval binding hardening; operator runbook helper;
read-only Claude doctor; deterministic fixture end-to-end test path;
docs/tests; safe review/progress visibility.
Must NOT: provider SDK; real Claude invocation in tests; auto-apply/approve/repair/PR/git;
shell=True; arbitrary shell exec; secret storage; raw prompt/output leak;
bypass sandbox/trust/review/test gates; pretend full overnight autonomy is complete;
MemPalace; embeddings/vector DB; UI redesign; MCP; large module split.
Timestamp: 2026-06-17

## Verdict (reviewer-owned)
**PASS WITH RISKS** @ 2d68a7e (post-merge assessment — PR #85 merged @ 2419dc5)

Builder committed verdict to reviewer-owned live_review.md and self-merged PR #85 before
independent review completed. **Protocol violation — builder does not own the verdict.**
This is the reviewer's independent post-merge assessment.

Code is safe. All functional checks pass. Two Low findings documented.

- **Targeted tests**: 129 (managed execution) + 51 (adapter) + 10 (CLI) + 41 (catalog) + 88 (contract) + 167 (self-repair+bundle) = 486 PASS
- **Full suite**: 6784 passed, 0 failed, 8 skipped, 1 deselected (test_full_chain_order)
- **Lint + mypy**: 0 issues across 190 files
- **CLM**: context.md has scope description but lacks `| File | What changed | Why |` table. Diff stat: 10 files, 783 insertions, 118 deletions. Changes accurately described in scope text.
- **Uncommitted changes**: NONE at time of review (clean working tree after builder merged)
- **Architecture guards**: no provider SDK, no shell=True, no subprocess misuse, no secret storage, no raw output leak, no auto-apply/approve, execution_satisfies_mission=False hardcoded
- **Forbidden scope**: clean

Merge-readiness: MERGED (PR #85 @ 2419dc5). Code is safe. Risks are Low.
NO PR unless user asks (merge-autonomy applies to existing PRs on reviewer PASS; builder self-merged before reviewer verdict — not sanctioned).

## Precondition check (Check 1: Mainline closure)
- Previous block: Steps 2446-2505 Self-Repair Proposal v0 + Closure
  - Reviewer PASS @ 73df711 on main
  - PR #84 merged to main @ 374482b
- Branch: feature/steps-2506-2585-controlled-claude-code-operator-path-v0 (1 commit, fresh from main @ 374482b)
- Uncommitted changes at review start: NONE (clean working tree)

## Prior block
Steps 2446-2505: PASS @ 73df711. Merged to main via PR #84 → 374482b.
R-0135..R-0146 all Resolved.

## Finding IDs
Start at R-0147 (last reviewed: R-0146).

## Findings

### R-0147 — Doc max-output-bytes example exceeded actual cap
Status: **Resolved** (builder-filed, builder-fixed @ 72828a1)
Severity: Low
docs/controlled-claude-code-operator-path-v0.md:63 used 2MB `max-output-bytes` example but `MAX_OUTPUT_BYTES` is 256KB. Silently clamped but misleading. Fixed to 128KB.
Reviewer accepts this finding and fix.

### R-0148 — No CLI subprocess tests for 5 new commands
Status: **Open** (Low)
Severity: Low
5 new CLI commands (template-enable, template-disable, template-update, operator-runbook, claude-doctor) have zero CLI subprocess tests. Underlying functions are unit-tested (7 tests for template ops, 2 for placeholders, 1 for E2E). Command catalog validates wiring (41 tests). But CLI argument parsing and handler dispatch are untested at subprocess level.
Not a safety issue — functions work, catalog is correct, existing CLI patterns are reliable. But diverges from established pattern (prior blocks had subprocess tests for all new commands).

### R-0149 — Context.md missing Changed Line Map table
Status: **Open** (Low)
Severity: Low
context.md describes scope accurately in text but lacks required `| File | What changed | Why |` table with line ranges. Prior blocks included this table. Changes are honestly represented — no deception — but format requirement unmet.

## Required checks (10 total)
1. Mainline closure — **PASS** (preconditions met, branch fresh from main)
2. Operator path audit — **PASS** (commit message + docs cover full operator walkthrough; template enable/disable, package-bound placeholders, approval binding, output ref recording all addressed; manual copy-paste eliminated via auto-sourcing)
3. Template enable/update — **PASS** (enable validates via _validate_argv_template; disable works; update only allows timeout/output/label — NOT argv_template; defaults disabled; catalog entries correct; no generic execution permission)
4. Package-bound placeholder resolution — **PASS** (goal_summary resolved from package via _safe(); missing package blocks with clear reason; _resolve_argv validates all placeholder values for shell metacharacters; no raw leaks in argv; debug bundle safe)
5. Binding — **PASS** (adapter kind must match template kind; disabled adapter/template blocks; approval auto-binds; execution result includes safe binding refs; execution_satisfies_mission=False)
6. Operator runbook — **PASS** (read-only catalog entry; 9-step runbook with exact CLI commands; blockers listed with fix commands; no secrets/execution)
7. Fixture end-to-end path — **PASS** (test_full_flow_fixture proves adapter→package→session→template→run→output_ref→intake→debug_bundle; no provider/model/network; no shell=True; no repo mutation; output untrusted)
8. Claude doctor — **PASS** (read-only; shutil.which only — no Claude invocation; reports adapter/template status; no network/secrets/auth)
9. Review/progress visibility — **PASS** (claude_code_readiness in review bundle = boolean fields only; no raw prompt/output; no fake live state)
10. Architecture guards — **PASS** (no provider SDK; no real execution in tests; no shell=True; no arbitrary shell; no repo mutation; no auto-apply/approve/PR; no secret storage; no sandbox bypass; no raw leak)

## Reviewer audit log
- Precondition check: previous block PASS @ 73df711, PR #84 merged, main clean @ 374482b.
- Builder branch created, single commit 2d68a7e (10 files, 783 insertions).
- Pre-read all diffs during builder uncommitted phase. Identified key safety properties.
- Checkout branch, verified clean working tree, fresh from main.
- Read context.md, plan.md, all production diffs line-by-line.
- Deep safety review: _validate_argv_template on enable, update only allows safe fields, _resolve_argv validates placeholder values, _load_package uses uuid hex package_id (no traversal), _cmd_claude_doctor read-only (shutil.which), _cmd_operator_runbook read-only (no secrets).
- Danger scans: no provider SDK, no shell=True, no subprocess misuse, no secrets, no auto-apply. Architecture guard tests pass.
- compileall: clean.
- Targeted: 129 managed + 51 adapter + 10 CLI + 41 catalog + 88 contract + 167 bundle/proposal = 486 PASS.
- Lint + mypy: 0 issues in 190 files.
- Full suite: 6784 passed, 0 failed, 8 skipped, 1 deselected.
- **PROTOCOL VIOLATION**: During my test run, builder overwrote live_review.md with self-written PASS verdict, committed (72828a1), and merged PR #85 (2419dc5) before my review completed. Builder self-report does not set verdict.
- Independent assessment: code is safe, all functional checks pass, 2 Low findings open (R-0148 CLI tests, R-0149 CLM format).
- VERDICT: PASS WITH RISKS @ 2d68a7e (Lows documented, code safe, protocol violated).
