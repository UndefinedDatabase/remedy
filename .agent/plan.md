# Plan — Steps 2446-2505 Final Closure: R-0141..R-0146

## Goal
Fix 6 findings from reviewer FAIL verdict on R-0135..R-0140 closure.

## Steps
- [x] R-0141: Redact title/next_action/safe_summary in export_progress_ledger_json via shared _SECRET_RE; reword plan.md
- [x] R-0142: Extend _SECRET_RE in self_repair_proposal.py for token/credential with quoted/unquoted; case-insensitive
- [x] R-0143: convert_self_repair_proposal_to_worker_prompt revalidates acceptance_criteria and required_tests
- [x] R-0144: CLI test file passes as full file run (12 tests, no hangs, 1.93s)
- [x] R-0145: Remove duplicate evidence_refs.append in anomaly/blocking loops; single append after
- [x] R-0146: Simple-language handoff in commit/PR
- [x] Tests: 77 proposal + 12 CLI + 90 bundle + 31 ledger = 210 targeted; 6768 full suite (0 failures, 8 skipped)
- [ ] Commit + push

## Hard rules
No provider execution; no auto-apply/approve/PR/git; no shell=True; no secret storage;
no raw log/prompt/transcript leaks; no MemPalace/embeddings.
