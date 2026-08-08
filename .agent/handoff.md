# Handoff — F103 Token ledger (SQLite), R6 (SPLIT, production code)

Branch `feature/f103-token-ledger` @ `eb8f5b99` (from `af91d57b`), pushed.
No verdict issued: split round with production code never self-certifies.

## Commits
| SHA | Subject | Files | Size |
|-----|---------|-------|------|
| `37a444d1` | persist the R5 PASS verdict and findings R-0220, R-0221 | `.agent/live_review.md`, `.agent/authored/f103-r6-1.md`, `.agent/authored/f103-r6-2.md` | +284/-7 |
| `087acd78` | register R-0221 as a closure candidate | `.agent/candidates.md` | +1/-3 |
| `8391f755` | arm the live token ledger at the task-run evidence seam | `packages/orchestration/job_evidence.py`, `tests/orchestration/test_token_ledger.py` | +410/-5 |
| `eb8f5b99` | sync the plan to the R6 live-mirror round | `.agent/plan.md` | +23/-23 |

No commit over 500 lines. Path set held exactly; nothing outside it was touched.

## How the project is resolved at the seam
`export_job_evidence` calls the new private `_resolve_job_ledger_project_id(job)`
ONCE per export and threads the registry UUID plus `job.job_id` into
`_write_task_run_evidence` (new keyword-only params, `None` defaults, so the
three existing positional callers stay inert). Resolution is
`project_registry.resolve_project(job.repo_path)` — persisted job state, the
registry's read-only resolver, registry UUID; the ledger path comes from
`token_ledger_path_for` → `data_paths.projects_dir`, so `REMEDY_DATA_DIR` is
honoured. Deliberately NOT `project_scope.resolve_scope`: it consults
`REMEDY_PROJECT` and the CWD, which exist to read a human's intent and would
file one project's spend under another. An empty/absent `repo_path` returns
None rather than letting `Path("")` become the CWD — this repository is itself
a registered project (`83cdfe8b-…`), so that fallback would have written into
the real `.data/`. Resolution is wrapped: it cannot raise. `pingpong_evidence.py`
is BYTE-UNCHANGED — a caller was added, not a parameter.

## Verification (run by me, real exit codes)
| Command | Result | Exit |
|---------|--------|------|
| `pytest tests/orchestration/test_token_ledger.py -q` | 82 passed (68 + 14 new) | 0 |
| `pytest tests/orchestration/test_evidence_bundle.py tests/orchestration/test_job_evidence.py -q` | 161 passed | 0 |
| `pytest tests/cli/test_stats_cost.py -q` | 33 passed | 0 |
| `pytest tests/cli/test_golden_path.py -q` (canary) | 42 passed | 0 |
| `pytest tests/orchestration -q` | 10210 passed, 7 skipped, 649s | 0 |
| `git status --porcelain` | empty | 0 |
| `rglob` scan for `*.sqlite`/`-wal`/`-shm` incl. `.data/` | NONE | — |
| `ruff check` on both changed files | All checks passed | 0 |

MUTATION RED-PROOF, run by me and reverted: (1) dropping the `ledger_*`
arguments from the `write_evidence_bundle` call turned **6 of the 6
production-path tests RED** while the 4 inertness tests stayed green — the new
tests genuinely depend on the wiring, not on a hand-passed target; (2) making
the resolver fall back to `"."` on an empty `repo_path` turned
`test_an_empty_repo_path_never_falls_back_to_the_process_cwd` RED, and it
failed by resolving the REAL project UUID `83cdfe8b-…`, which is precisely the
data-root escape constraint 3 forbids.

## Transport proofs
Receipt 1 → `.agent/live_review.md`. FROM counts BEFORE any edit: PAIR 1 1x,
PAIR 2 1x, PAIR 3 1x, PAIR 4 1x. AFTER: PAIR 1 FROM 0x / TO 1x; PAIR 2 FROM 0x /
TO 1x; PAIR 3 FROM 0x / TO 1x; PAIR 4 (append-shaped) FROM 1x / TO-only line
`- D17 (…` 1x. All four TO blocks verified present byte-verbatim exactly once.
CORRECTION, declared: the step block labels PAIR 3 append-shaped, but its TO
does not contain its FROM — `- R5: pending review.` becomes
`- R6: pending review.`. It is a REWRITE, so FROM 0x is the attainable and
honest count; reporting 1x would have been false. PAIR 4 is genuinely
append-shaped and reports FROM 1x as instructed.
Receipt 2 → `.agent/plan.md` by `cp`; `cmp` **exit 0**. Both receipts: no
trailing whitespace on any line, exactly one closing newline.

## Item status
| Item | Status | Reason |
|------|--------|--------|
| B1 receipts saved first | done | |
| B2 receipt 1 → live_review, commit 1 first action | done | |
| B3 R-0221 → candidates.md | done | replaced the stale "(empty — …)" |
| B4 wire the mirror at the seam | done | |
| B5 production-path + inertness tests | done | 14 tests, both mutations red-proofed |
| B6 verification | done | table above, all exit 0 |
| B7 plan receipt, commit, push, handoff | done | |

## Open findings & deviations
Open findings: **1** — R-0220 (Medium), fixed here, closes on reviewer
confirmation. R-0218/R-0219 closed; R-0221 carried in `.agent/candidates.md`.
Deviations, declared: (a) the PAIR 3 shape correction above; (b)
`tests/orchestration/test_job_evidence.py` exists, so the middle command needed
no adjustment; (c) the new tests live in `test_token_ledger.py` — the honest
home, since the behaviour under test is F103's ledger, not the bundle writer;
(d) the resolver adds one `git rev-parse` per EXPORT (not per task run), so the
R5-measured +1.386 ms per finalized task run is unmoved; (e) plan.md was synced
at B7 as the bundle ordered, so commits 1-3 carried the R5-era plan, matching
this feature's own R5 pattern.

## Next expected action
Reviewer reads `af91d57b..eb8f5b99`, re-runs the table, and rules on R-0220.
On PASS, R7 is closure per docs/roadmap/STATUS_closure_protocol.md.
