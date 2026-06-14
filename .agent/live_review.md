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

### R-0083: Provider-derived `candidate.summary` is not secret/path-scrubbed but is persisted + shown in public surfaces
Done: R-0083 - `_safe_text` (summary/rationale/risk_notes, and via `_safe_first_line` the diff/markdown summary) now routes through `_scrub_public`, masking `_SECRET_PATTERNS`→`[redacted-secret]`, abs paths→`[redacted-path]`, traceback markers→`[redacted-trace]` BEFORE truncation. No secret/abs-path on the first line or in JSON summary/rationale/risk_notes reaches job metadata / trust-show / review bundle / cockpit, even on rejected reports. Test `test_candidate_summary_scrubbed` added.
- **Status**: Open
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
