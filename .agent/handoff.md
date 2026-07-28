# Handback — F251 R2: verdict, R-0151/R-0152, S3 flake fixes, churn gate

## Range
Review of `13783ed..HEAD` — `feature/f251-suite-stabilization`, pushed, no PR;
6280cb0..13783ed were accepted by the R2 verdict and are not re-tabled.

## Commits
### f0ee3e1 R2 verdict · a8b3337 reviewer flake appendix
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f251-r2-1.md, .agent/live_review.md | +55, +67 −23 | verdict text sha256 111efa9b…, applied cmp 0 |
| .agent/authored/f251-r2-2.md, .agent/f251_baseline/reviewer_flake_extras.txt | +20, +20 | appendix sha256 45eb4a22…, copied cmp 0 |

### 7f67d03 R-0151 · af67046 · de17a00 · 13572dd global-state leaks
| Path | +/- | Reason |
|---|---|---|
| tests/docs/test_docs_consistency.py | +3 −1 | 7f67d03 — TOTAL_FEATURES 250→251 |
| tests/test_data_paths.py | +21 | af67046 — config-cache isolation (F-C) |
| tests/conftest.py | +29, +23 | de17a00 config-cache reset (F-B, F-E); 13572dd cwd restore |

### 1c95dec test(f251): per-worker runtime ports (F-A, F-D)
| Path | +/- | Reason |
|---|---|---|
| tests/ports.py | +39 | new: worker_port(), base 15173 |
| 6 runtime test modules | +36 −13 | dynamic default port (test_runtime_cmd, test_dev_server, test_runtime_{cli_process_boundary,lifecycle_safety,state_machine}, test_supervisor_portability) |

### 487c553 + this commit (self-reference, R-0149 grouped table)
| Path | +/- | Reason |
|---|---|---|
| .agent/f251_baseline/churn_gate_run1..3 + timings | +503 | 487c553 gate evidence |
| .agent/handoff.md | rewrite | this commit — 100 lines (`wc -l`) |

## Item status
| Item | Status | Reason |
|---|---|---|
| 1 persist R2 verdict, own commit, first | done | f0ee3e1, sha256 + cmp 0 |
| 2 reviewer flake appendix | done | a8b3337, sha256 + cmp 0 |
| 3 R-0151 fix | done | 7f67d03, 4 FeatureLedger tests green |
| 4 R-0152 fix (handback ≤100) | done | 100 lines, measured |
| 5 S3 per class | partial | F-A/F-D residue stopped, below |
| 6 churn gate ×3 | **NOT PASSED** | 1 id in run1 only |
| 7 canary | done | 42 passed |

### Per-class outcome
| Class | ids | Outcome |
|---|---|---|
| F-C data_paths | 1 | **fixed** — id 20× serial, module -n auto 3× + serial |
| F-B grouped_cli / F-E job_rerun_manifest | 5 | **fixed** — one root cause (config cache) |
| F-A/F-D runtimes+probe | 13 | **fixed** except 2 — union across 3 runs 10 → 2 |
| appendix repo-scan | 7 | **fixed** — cwd fixture; all 7 gone in gate 2 |
| F-A residue: Vite probe + supervisor guard | 2 | **stopped** — need product change |
| new: test_run_manifest TestCoverage | 1 | **open** — seen once, not reproduced |

## External actions
A push per commit (f0ee3e1, a8b3337, 7f67d03, af67046, de17a00, 1c95dec, 13572dd,
487c553, this one). No PR — reviewer-gated. No merges this round.

## Verification
    R-0151  -k FeatureLedger → 4 passed; file → 13 failed (README drift), 279 passed
    F-C     id ×20 serial → 0 failures; module -n auto ×3 + serial → 23 passed
    F-B/F-E poisoner + TestGroupedExecution ×3 → 9 passed (was 4 failed); 4 ids
            -n auto ×3 → 4 passed; module → 479 passed; 19-id flake set serial →
            19 passed; 18-id reproducer → 18 passed (was 4 failed)
    F-A/F-D 22-id set -n auto ×3 → union 10 → 2; serial 22 passed; 4 modules 127
    GATE 1  154 / 155+2err / 158+2err — core 154, 7 new churners (cwd leak)
    GATE 2  155 (2m54.885s) / 154 (3m4.077s) / 154 (3m4.346s); run2 == run3
            byte-identical AND each == the expected 154 exactly (comm empty BOTH
            ways vs serial_deterministic minus TestFeatureLedger); run1 had ONE
            extra id → gate not passed
    canary  test_golden_path.py -q → 42 passed; git status --porcelain → empty

## Authored-text proofs
sha256 matched BEFORE committing: f251-r2-1 `111efa9b…`, f251-r2-2 `45eb4a22…`;
`cmp` exit 0 for live_review←f251-r2-1 and reviewer_flake_extras←f251-r2-2.
**f251-r2-2 arrived line-wrapped**: three ids split mid-token. As-displayed bytes
hash to `3d148f40…`; joining the wrapped pairs gives `45eb4a22…` = the stated
hash, so the joined form was applied — R-0148 class, caught by the guard before
any commit, reported rather than silently "corrected".

## Deviations & assumptions
- **Gate not passed — stop-on-red.** Churn fell from 14 ids to 1 and the stable
  core is exactly the catalogued 154, but the bar is three identical sets and run1
  missed by one: `test_run_manifest.py::TestCoverage::
  test_check_candidate_is_incomplete_and_never_same`, `assert diff["same_inputs"]
  is None` → `False` (line 473). Not reproduced in 8 attempts (id 5/5, module
  3/3), so it is neither fixed nor quarantined.
- **Two F-A ids stopped, not quarantined** ("product change ⇒ STOP"): the
  real-Vite probe binds the product's apps/ui port; the supervisor_portability
  residue is a file-scoped teardown guard whose fix reaches the product
  stop/ownership path, and quarantining a test cannot silence a file-scoped guard.
- **0 quarantines.** Every flake closed was closed by a hermetic fix.
- `tests/conftest.py` now resets config and cwd for all 14314 tests; blast radius
  covered by 6 full-suite runs across the two gate attempts.
- A scripted edit put the new import inside embedded server-script strings in 5
  files; caught before running, reverted, redone via AST. None reached a commit.

## Next
Operator ruling open on the 13 D-classes (154 standing red) and the `.agent`-coupled
D4 tests; then the 3 open flake ids above.
**full suite: 0 quarantined, 1 churning (1 of 3 runs), 154 standing red (catalogued)**
