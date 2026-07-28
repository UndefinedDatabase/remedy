# Handback — F251 R3: R3 verdict, F-F root cause, churn gate PASSED

## Range
Review of `6c45717..HEAD` — `feature/f251-suite-stabilization`, pushed, no PR.

## Commits
### 2a93e31 chore(f251): persist the R3 PASS verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f251-r3-1.md | +54 | verdict text, sha256 aec772a5… verified |
| .agent/live_review.md | +85 −43 | full replace from f251-r3-1 (cmp 0) |

### 5abfd3c test(f251): freeze Remedy's worktree identity per test (F-F)
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_run_manifest.py | +28 | autouse identity freeze |
| tests/cli/test_job_rerun_manifest.py | +28 | autouse identity freeze |
| .agent/plan.md | +38 −45 | worker rewrite (authored r3-2 unverified) |

### 6c3f072 + this commit (self-reference, R-0149 grouped table)
| Path | +/- | Reason |
|---|---|---|
| .agent/f251_baseline/churn_gate2_run1..3 + timings | +491 | 6c3f072 — gate evidence |
| .agent/handoff.md | rewrite | this commit — 100 lines (`wc -l`) |

## Item status
| Item | Status | Reason |
|---|---|---|
| 1a persist R3 verdict (f251-r3-1) | done | 2a93e31, sha256 + cmp 0 |
| 1b apply authored plan (f251-r3-2) | **BLOCKED** | sha256 mismatch — see below |
| 2 F-F root cause + fix | done | 5abfd3c, hermetic, reproducer-proven |
| 3 churn gate ×3 | **PASSED** | three identical sets == expected 154 |
| 4 canary | done | 42 passed in 15.63s |
| R-0153 | **open** | needs the authored plan text re-sent |

## BLOCKER — f251-r3-2 failed its hash, not committed
Received 37 lines / 1686 bytes hashing to
`c30e6828d9b061a6c2b15964cc930d014b1c65266046cb8ff3cedc5b11588cd0`;
stated `8ac81a9afde5921b68eb792135905528989aecb3f83337c55a0076fa4e1d873d`.
Recovery attempted per the R2 protocol, all failed: every adjacent-line join
(with/without space, continuation stripped and unstripped), every combination of
the unicode variants present (`…` `–` `×` `→` `—`), and trailing-newline / CRLF
variants. Unverified authored bytes are not committed, so `.agent/plan.md` carries
a worker rewrite that says so at the top. **R-0153 stays open** until f251-r3-2 is
re-sent. `f251-r3-1` verified byte-exact, so the verdict was persisted rather than
lost — step 1's single ordered commit is now two; flagged, not silent.

## F-F — root-caused, hermetically fixed
A run manifest records Remedy's OWN worktree identity (HEAD, content hash,
dirty), and **any untracked entry sets dirty** (`run_manifest.py`: `dirty = True
# any untracked entry means dirty`). The reference manifest is written when the
job runs; the candidate is built moments later. Under `-n auto` all 24 workers
share this one repo tree, so a neighbouring test creating or removing a repo file
between those moments yields a blocking drift, and `same_inputs` becomes `False`
where the tests require `None`.

**Not a product bug.** Detecting that Remedy's own checkout changed between the
recorded run and the current one is the intended F012 behaviour. The defect is
test hermeticity: these tests assert about JOB inputs while running in a tree
other tests mutate. The modules already carry this seam deliberately
(`_patch_remedy_identity`); these three ids did not use it. The fix freezes the
identity to the value seen at test start — the real value, not a forced
"complete" — so the assertions keep their meaning.

## External actions
A push per commit (2a93e31, 5abfd3c, 6c3f072, this one). No PR — reviewer-gated,
no merges.

## Verification
    F-F repro    untracked repo-root file churned: coverage id 5/5 RED; quiet tree 3/3 green
    F-F fixed    all 3 ids under the same churn → 5/5 passed
                 both modules serial → 75 passed; -n auto ×3 → 75 passed
                 load-generator loop (4 parallel pytest jobs) 20/20 clean —
                 generic load never reproduced it, tree mutation always did
    GATE retry   run1 154 failed / 2m55.453s
                 run2 154 failed / 3m0.927s
                 run3 154 failed / 3m8.946s
                 three id sets IDENTICAL (diff -q clean, both pairs), 0 errors
                 each == expected 154 exactly (comm empty BOTH directions vs
                 serial_deterministic minus TestFeatureLedger)
    canary       test_golden_path.py -q → 42 passed; porcelain empty

## D4 ids — actual state, as ordered
Both `test_live_review_has_steps_section` ids (test_test_runner.py,
test_dashboard_contract.py) are PRESENT and RED in all three gate runs. They
passed in the reviewer's R2 runs because `.agent/live_review.md` then held a text
with a "Steps" section; this round's live_review (f251-r3-1) has none, so they are
red — but stably red, which is why the sets are identical. Still D4: coupled to
live `.agent` state, not to the code under test.

## Deviations & assumptions
- Step 1's single ordered commit became two (verdict in, plan not): only one of
  the two texts verified. See BLOCKER.
- 0 quarantines, unchanged. Every flake closed was closed by a hermetic fix.
- 2 F-A ids stay stopped (real-Vite port, file-scoped supervisor guard): both need product change, untouched; neither appeared in any gate run.
- No D-class edits; the 154 standing red is unchanged and still catalogued.

## Next
Re-send f251-r3-2 to close R-0153. Operator ruling open on the 13 D-classes (154 standing red) and the 2 stopped F-A ids.
**full suite: 0 quarantined, 0 churning, 154 standing red (catalogued)**
