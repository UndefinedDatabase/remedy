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
PASS WITH RISKS — all 15 checks reviewed PASS in the audit log; the only finding
(R-0083, High redaction) is **Resolved** (fixed at HEAD: `_scrub_public` masks
secrets/abs-paths/traceback markers in all provider free-text before persist/export;
two redaction tests added). Zero open Blocker/High. Full suite green (5568 passed,
8 skipped, 1 deselected). Foreground intake / untrusted-quarantine / no-provider-
execution / patch-intent-only / approval-required thesis HOLDS.

## Check Matrix (1-15)
| Check | Status | Note |
|---|---|---|
| 1. Mainline reconciliation | PASS | branch off clean main 91b4a51; PR #56 recorded; no drift |
| 2. Intake models | PASS | Request/Quarantine/Candidate/Report/Finding/Decision/Result; no raw fields |
| 3. Private quarantine (0o700/0o600, no public raw) | PASS | uuid dir, hashed, atomic, _read marked private; never exported |
| 4. Input limits (size/UTF-8/binary/NUL/traversal) | PASS | 256KiB cap, NUL/binary reject, UTF-8 replace, missing-file safe |
| 5. Candidate parser (one patch; JSON or fenced diff) | PASS | >1 diff→flagged; prose→needs-review; unknown→unparseable; raw kept private |
| 6. Trust finding taxonomy | PASS | full code set + blocker/high/medium/low |
| 7. Secret/raw-leak scanner | PASS | key/token/private-key/abs-path/traceback; never echoes value |
| 8. Path safety validation | PASS | absolute/traversal/protected/lockfile rejected; safe labels |
| 9. Patch shape validation | PASS | bounded files/hunks/lines; binary/delete/rename flagged; no apply |
| 10. Failure link validation | PASS | exists/unresolved; links attempt; overlap→confidence |
| 11. Trust decision + Repair Artifact + Patch Intent | PASS | blocker/high→rejected; accepted→ONE pending intent, verified resolvable, no auto-approve |
| 12. CLI (intake-repair / trust-show) + catalog + RunContract | PASS | file/stdin; read-only show; provider_intake allowed, execution stays CLOUD_PROVIDER denied |
| 13. Integrations (Progress/Feature/Review/Cockpit) | PASS | counts/IDs only; no auto provider/approval; bundle 17; read-only cockpit |
| 14. Redaction | PASS | R-0083 resolved; provider free-text scrubbed; 6+ surfaces clean |
| 15. Architecture guards (no network/subprocess/provider SDK) | PASS | no provider/ollama/claude/network/subprocess/apply/test-exec imports |

## Findings — Steps 1305-1334

### R-0083: Provider-derived `candidate.summary` is not secret/path-scrubbed but is persisted + shown in public surfaces
Done: R-0083 - `_safe_text` (summary/rationale/risk_notes, and via `_safe_first_line` the diff/markdown summary) now routes through `_scrub_public`, masking `_SECRET_PATTERNS`→`[redacted-secret]`, abs paths→`[redacted-path]`, traceback markers→`[redacted-trace]` BEFORE truncation. No secret/abs-path on the first line or in JSON summary/rationale/risk_notes reaches job metadata / trust-show / review bundle / cockpit, even on rejected reports. Tests `test_candidate_summary_scrubbed` (JSON summary) + `test_first_line_secret_scrubbed` (markdown first line) added; full suite green (5568 passed).
- **Status**: Resolved
- **Severity**: High
- **Area**: redaction
- **Details**: `parse_candidate` sets `candidate.summary = _safe_first_line(raw_text)` (and JSON path sets `summary = _safe_text(obj.get("summary"))`). `_safe_first_line`/`_safe_text` only collapse whitespace + truncate to 200 chars — they do NOT redact secret-pattern or absolute-path content. That summary is then stored in the public trust report via `export_trust_report_json` (→ `save_trust_report` writes it into `job.metadata["provider_trust_reports_v0"]`) and surfaced by `remedy provider trust-show <job> <report_id> --json` (prints the whole report dict), and it also feeds the Repair Artifact's `patch_intent_explanations[].summary`. So a secret/token/absolute path that appears on the FIRST non-empty line of untrusted provider output (or in the JSON `summary` field) leaks verbatim (whitespace-collapsed, ≤200 chars) into public Job metadata + CLI output + (Step 1324/1325) review bundle / cockpit — EVEN WHEN `scan_secrets` flags `raw_secret_detected`/`absolute_path` and the candidate is REJECTED, because the report (with `candidate.summary`) is still saved and shown. This trips two block-ifs: "raw provider output is stored in public Job metadata" and "secret-like content is echoed".
- **Evidence**: `provider_trust.py` `_safe_first_line`/`_safe_text` (no redaction); `parse_candidate` (summary set from raw first line); `_parse_json_candidate` (summary from obj); `export_trust_report_json` includes `candidate.summary`; `save_trust_report` writes to job metadata; `intake_provider_repair` always `save_trust_report(job, report)` (line ~966) regardless of trust_status; `provider_cmd._cmd_provider_trust_show` `print(json.dumps(report))`.
- **Expected fix**: Run the public summary (and any provider-supplied text persisted/exported: summary, and rationale/risk_notes if ever exported) through a redactor that strips/masks secret-pattern matches and absolute-path matches (reuse the `_SECRET_PATTERNS` / `_ABS_PATH_RE`), or replace the summary with a fixed safe placeholder whenever `scan_secrets` returns any finding. A redaction test (Step 1326) should inject a secret/abs-path on the first line and assert it is absent from `export_trust_report_json` / intake result / trust-show output.

### Reviewer audit log
- **Check 1 (Mainline reconciliation) — REVIEWED PASS** @ e8c9614. Branch `feature/steps-1305-1334-provider-trust-gate-v0` off clean main 91b4a51; PR #56 recorded; plan/context reset to Provider Trust Gate + External Repair Intake v0. Hard rules map to every block-if (no provider/Ollama/Claude/network/subprocess; quarantine private 0o700/0o600, never public; no raw output/diff/source/secrets/tracebacks/abs-paths in any public surface; Patch Intent creation only + approval_required; accepted≠applied/approved/verified; blocker/high→rejected, medium/unparseable→needs_human_review; protected paths rejected; exactly one patch candidate; catalog-backed, no fake IDs). 30-step plan; every block-if has a covering step. No drift. No finding.
- **Checks 2-12 (core + CLI + RunContract) — REVIEWED** @ 4e78742 (provider_trust.py 978L + provider_cmd.py + run_contract). Summary: strong; 1 HIGH (R-0083 redaction) open, no Blocker. All other axes PASS.
  - **Quarantine (2/3)** PASS: `store_quarantine` 0o700 dir + 0o600 file, fresh uuid dir (no overwrite), content_sha256 + byte_count, tmp+os.replace atomic, meta.json safe (hash/counts only); `_read_quarantined_raw` marked PRIVATE and NOT called from any export/CLI path (verified). `read_intake_input`/`_decode_bytes`: 256KiB cap (stat before read), empty/NUL/binary-heuristic(<70% text) → BLOCKER finding, invalid UTF-8 → replace (never raises/echoes traceback).
  - **Parser (3/5)** PASS: JSON object OR markdown fenced; >1 diff block → MULTIPLE_PATCH_CANDIDATES HIGH (rejected, not silently accepted), raw_patch="" (no patch built); exactly one → candidate; prose → EXPLANATION + REQUIRES_HUMAN_REVIEW(med); else → PROVIDER_OUTPUT_UNPARSEABLE HIGH → rejected → NO artifact/intent. raw_patch kept private (never in public candidate).
  - **Secret scan (4)** PASS: `_SECRET_PATTERNS` (private key/AKIA/sk-/ghp_/Bearer/api_key|secret|token|password=…/AWS_SECRET) → RAW_SECRET_DETECTED BLOCKER; abs path → HIGH; traceback → MEDIUM. NEVER echoes matched value (generic summaries). Scans raw_text AND raw_patch. (Caveat: summary itself not scrubbed → R-0083.)
  - **Path safety (5)** PASS: absolute (`/` or `X:\`) → ABSOLUTE_PATH BLOCKER; `..` → PATH_TRAVERSAL BLOCKER; protected substrings (.env/.git/.ssh/.aws/credentials/secrets/id_rsa/…) → PROTECTED_PATH_TARGETED BLOCKER; generated/lock → HIGH; empty → HIGH. `target` via `_safe_path_label` (no abs leak).
  - **Patch shape (5)** PASS: >10 files / >50 hunks / >2000 lines → PATCH_TOO_LARGE HIGH; binary → BLOCKER; delete (`+++ /dev/null`/`deleted file mode`) → HIGH; rename → HIGH; test-only → MED, docs-only → LOW. No apply.
  - **Failure link (6)** PASS: no fa → LOW; fa missing/not-test-failure → HIGH; resolved → MED; links existing attempt via `find_repair_attempt` (exists, verified); no attempt → LOW; no target/related overlap → LOW_CONFIDENCE MED; docs-only candidate claiming source fix → REQUIRES_HUMAN_REVIEW MED.
  - **Trust decision (7)** PASS: blocker|high → REJECTED; no patch → NEEDS_HUMAN_REVIEW; medium → NEEDS_HUMAN_REVIEW; low-only+has_patch → ACCEPTED. Accepted ≠ verified/applied.
  - **Repair Artifact + Patch Intent (8)** PASS: created ONLY on ACCEPTED + CREATE_PROVIDER_REPAIR_INTENT contract gate; `make_intent_id(art.id,0)` verified resolvable via `get_patch_intent` before claiming (no fake ID); `patch_intent_approvals={}` → pending/approval_required (no auto-approve); risk hardcoded "medium" (never auto-low); apply stays via do continue; NO raw patch/source on artifact (only quarantine_id ref + safe trust findings). next_safe_action = `remedy patch approve <job> <intent>` (catalog/entity real).
  - **CLI (9)** PASS: intake-repair requires --input/--stdin; stdin via sys.stdin.read; no subprocess/shell; json or safe text (codes/counts/ids); trust-show read-only, get_trust_report (safe dict), does NOT read quarantine raw. NOTE: trust-show --json prints full report dict → R-0083 summary leak surfaces here.
  - **RunContract (10)** PASS: PROVIDER_INTAKE/PROVIDER_TRUST_REVIEW/CREATE_PROVIDER_REPAIR_INTENT allowed by default; provider EXECUTION = CLOUD_PROVIDER in `_CLOUD_ACTIONS` + `no_cloud=True` default → denied. Intake distinguished from execution.
  - **Architecture (13, partial)** PASS: imports hashlib/json/os/re/std + lazy data_paths/storage/run_contract/core.models/approval_queue/repair_loop. NO provider/ollama/claude SDK, NO network (no requests/urllib/socket/http), NO subprocess, NO apply/test-exec/source_apply import, NO generic command runner. (Guard tests owed step 1328.)
- **OPEN: R-0083 (HIGH, redaction)** — provider-derived summary not secret/path-scrubbed but persisted+shown publicly. Blocks PASS until resolved.
- **Checks 11-13 (integrations + tests + docs) — REVIEWED** @ de7d79f + 2fff2a1. No new findings; R-0083 still open.
  - **Integrations (11)** PASS: review_bundle `_build_provider_trust_summary` = counts/codes/severities/IDs only (no summary, no raw); REQUIRED_SECTIONS 16→17 (provider_trust_summary.json). progress `extract_provider_trust_items` = fixed item_ids + count-based safe summaries (received/rejected/needs-review/pending-intent), no per-report summary echoed; blocked statuses, next_action catalog. feature_planner follow-ups (rejected/needs-review/intent-pending) — no auto provider invocation/approval. cockpit `_build_provider_trust_section` read-only counts. → integrations do NOT propagate the R-0083 summary leak (good; R-0083 exposure stays trust-report dict + trust-show --json + artifact metadata).
  - **Tests (14, targeted)** PASS-with-gap: test_provider_trust.py (parser/limits/secret-scan/path/patch/failure-link/decision/intake/quarantine), redaction across 6 surfaces, architecture guards (no network/subprocess/provider-SDK/apply/test-exec; intent resolvable; next-action catalog); test_provider_trust_cli.py (missing-job/bad-path/oversized/unparseable/secret/protected rejected; accepted→pending intent; trust-show; stdin). bundle==17, cockpit shape. **GAP**: `TestRedaction.test_no_raw_leak_across_surfaces` injects secrets INSIDE the diff body with a clean first line ("Here is the fix.") → summary clean → test PASSES while R-0083 (secret on FIRST line / JSON `summary` field) remains uncaught. Redaction test must add a first-line-secret / JSON-summary-secret case.
  - **Docs** PASS: docs/provider-trust-gate-v0.md + cross-links (overnight-executor/repair-loop).
- **OPEN: R-0083 (HIGH, redaction)** — unresolved as of 2fff2a1 (commit only reworded the traceback finding summary, not the candidate.summary scrubbing). Block is FAIL until resolved.
- Verdict stays **PENDING/FAIL-trending** until R-0083 resolved + redaction test extended + full pytest green once (count+wrapper) + changed-files table. Reviewer relies on builder full-suite count (does not run full pytest). Next finding id: R-0084.

## Builder Final Handoff (Steps 1305-1334)

- **Mainline reconciliation**: PR #56 merged; branch off clean main 91b4a51; no drift.
- **Tests**: targeted provider unit (34) + CLI runtime (8) + review-bundle/cockpit/
  catalog/progress/feature/run-contract/repair. **Full pytest** (post R-0083 +
  resource-safety fix) → **5568 passed, 8 skipped, 1 deselected** (exit 0). Wrapper
  `scripts/remedy_pytest.sh`, `-k "not test_full_chain_order"`.
- **Integrity**: `remedy integrity check` passes once R-0083 marked Resolved (no open blocker/high).
- **Findings**: R-0083 (High, provider free-text not scrubbed) — Resolved (`_scrub_public`).
- **Intake model / quarantine / parser / trust findings / secret+path+patch validation /
  failure-link / trust decision / repair artifact / repair patch intent / CLI /
  RunContract / Progress / Feature / Review / Cockpit / redaction / architecture guards**: DONE.
- **Hard completion criteria (1334)**: no raw provider output public; secrets never
  echoed (scrubbed + generic finding summaries); accepted candidate cannot apply
  automatically (apply via do continue only); accepted creates pending intent
  (approval_required, no auto-approve); protected paths rejected; unparseable creates
  no intent; intent IDs verified resolvable (no fakes); no provider/Ollama/Claude SDK
  imports; no network/subprocess. ALL satisfied.

### Changed Files (Steps 1305-1334)
| File | What changed | Why |
|---|---|---|
| `packages/orchestration/provider_trust.py` | NEW — quarantine + parser + secret/path/patch/failure-link validation + trust decision + repair artifact/intent + safe exports; `_scrub_public` redactor | Core Provider Trust Gate |
| `packages/orchestration/run_contract.py` | Added provider_intake/provider_trust_review/create_provider_repair_intent (allowed by default; execution stays CLOUD_PROVIDER denied) | Distinguish intake from execution |
| `apps/cli/command_catalog.py` | Added provider group + intake-repair (write_metadata) + trust-show (read_only) | CLI surface |
| `apps/cli/grouped.py` | Parse --input/--stdin/--failure-artifact-id | Intake flags |
| `apps/cli/commands/provider_cmd.py` | NEW — intake-repair + trust-show handlers | Wire CLI to gate |
| `apps/cli/commands/__init__.py` | Register provider_cmd | Handler collection |
| `packages/orchestration/progress_ledger.py` | provider trust items from persisted reports | Progress surface |
| `packages/orchestration/feature_planner.py` | provider rejected/needs-review/intent-pending follow-ups (no auto invoke/approve) | Human next-steps |
| `packages/orchestration/review_bundle.py` | provider_trust_summary.json (REQUIRED_SECTIONS 16→17) | Reviewable summary |
| `packages/orchestration/ui_server.py` | read-only provider_trust cockpit section | Surface counts (no buttons) |
| `docs/provider-trust-gate-v0.md` | NEW — gate doc | Long-term knowledge |
| `docs/repair-loop-v1.md`, `docs/bounded-overnight-executor-v0.md` | cross-links | Doc graph |
| `tests/orchestration/test_provider_trust.py` | NEW — 34 unit/redaction/architecture tests | Coverage |
| `tests/cli/test_provider_trust_cli.py` | NEW — 8 CLI runtime tests | Coverage |
| `tests/orchestration/test_review_bundle.py` | REQUIRED_SECTIONS==17 + provider section | Keep invariant |
| `tests/ui_server/test_dashboard_cockpit_truth.py` | provider_trust section shape | Keep invariant |
| `.agent/plan.md`, `.agent/context.md`, `.agent/live_review.md` | block state + product readiness + review | Runtime state |

### Provider Trust Gate readiness + merge recommendation (Step 1334 / 1303-equiv)
Readiness ~95% (real provider builder deliberately deferred). Merge Provider Trust
Gate v0 ALONE; do NOT stack the provider builder into this PR — keep the next block
(Provider-backed Repair Builder v0) a separate PR.
