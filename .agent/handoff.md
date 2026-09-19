# Handoff — F273 Findings paydown v1 · Round 21

## Session

SESSION 3 of feature F273 · round 21 · rounds so far 21

Context self-assessment: the worker read the block, AGENTS.md, the closure protocol's preconditions, the integration-gate procedure, amendment amend0917-throughput, the handback template and F271's closure transcript as its shape, and held all of it without loss; every figure below comes from a command run in this round.

## Range

Review of c8b91d87..HEAD — branch `feature/f273-findings-paydown-v1`.

## Summary

Round 21 is the integration-gate round. It books round 20's verdict and three resolutions, appends the feature file's Built State, and ran the feature's one full suite.
- C1 books Gate F273 R20 (VERDICT PASS) and the `Done:` lines of R-0994, R-0995 and R-0996; rewrites the plan; saves the four payload copies.
- C2 appends `## Built State (F273, 2026-09-19)` to `docs/roadmap/features/T2_F273.md`.
- C3 commits the closure suite's transcript. **The run is RED: 1 failed, 17516 passed, 20 skipped.** The one bad node is `tests/orchestration/test_job_plan_state_reads.py::TestNoRetiredJobPlanStateReads::test_the_scan_reaches_a_real_corpus` (`AssertionError: corpus collapsed to 299 files`, `assert 299 > 300`). Per the block nothing was repaired and the suite was not run a second time; the red run is the next round's input.
- C4 is this handoff.

## Commits

### f3571e8b F273 R21 C1: bookkeeping — round 20's PASS verdict and the resolutions of R-0994, R-0995 and R-0996 booked, the round 21 plan and the reviewer's payloads saved
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f273-r21-block.md` | +75 / -0 | Byte copy of the block |
| `.agent/authored/f273-r21-built_state.md` | +34 / -0 | Byte copy of built_state.md |
| `.agent/authored/f273-r21-ledger.md` | +8 / -0 | Byte copy of ledger.md |
| `.agent/authored/f273-r21-plan.md` | +30 / -0 | Byte copy of plan.md |
| `.agent/live_review.md` | +8 / -0 | `c8b91d87` bytes + ledger.md (Gate F273 R20, three `Done:` lines) |
| `.agent/plan.md` | +5 / -6 | := plan.md |

160 insertions, 6 deletions (`git show --numstat`).

### d2fc05b8 F273 R21 C2: the feature file gains its Built State — the open set by round, the product changes by the DECISIONs D1 to D20 that ruled them, and the ids the closure carries
| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/features/T2_F273.md` | +34 / -0 | `c8b91d87` bytes + built_state.md (an append) |

34 insertions, 0 deletions.

### 309afcaf F273 R21 C3: the closure suite's transcript — one run of the full suite in the primary checkout read 1 failed, 17516 passed, 20 skipped; the one bad node is listed and no R-0803 line was printed
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f273-closure-suite.txt` | +3 / -0 | Summary line, the one bad node id, `R-0803 lines: 0` |

3 insertions, 0 deletions.

### C4 (this commit) F273 R21 C4: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C1, with 160.

## External actions

- No worktree was added or removed; no branch was created or deleted.
- The branch `remedy/job-81ec65896729405c` still exists in this repository. A research helper's probe created it before round 16; nobody may delete it without the operator. `git branch --list 'remedy/job-*'` read 37 branches before C3 and 37 after the run.
- After C4: `git push`. No pull request is opened.

## Verification

Every script ran with an explicit `cwd=` of the primary checkout through `.remedy-wt/f273-r21/wk_run.py`, whose child `env=` drops `REMEDY_OLLAMA_HOST` and `OLLAMA_HOST` and which prints the child's real exit code.

- **Transport**, before any write: `sha256sum` of `block.md`, `ledger.md`, `plan.md`, `built_state.md` and `next.md` each equalled the block's digest; the block read 75 lines.
- **Block copy**, before C1 (`python3 .remedy-wt/f273-r21/wk_build.py c1`):
  ```
  saved block sha256 65615d5fc7ad1bcf8845679a4c362ed01352b76b728aa9a734b2d6899197968b lines 75
  ok c1
  ```
  Both equal the given block's digest and line count.
- **G1** (`python3 .remedy-wt/f273-r21/wk_g1.py` at C2 `d2fc05b8`):
  ```
  docs tree 6f24191f3f591dc5acf1a2f5c88f057d83514371
  digest ledger.md True
  digest plan.md True
  digest built_state.md True
  digest next.md True
  digest block.md True
  live_review True
  T2_F273 True
  plan True
  authored ledger.md True
  authored plan.md True
  authored built_state.md True
  authored block.md True
  docs tree True
  True
  EXIT CODE: 0  WALL: 0.1s
  ```
- **G2** (`python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_roadmap_index.py tests/cli/test_golden_path.py` at `d2fc05b8`):
  ```
  386 passed in 132.50s (0:02:12)
  EXIT CODE: 0  WALL: 215.4s
  ```
- **G3 = C3** (`python3 -m pytest -n auto -q`, once, primary checkout, at `d2fc05b8`, nothing else running; output logged to the gitignored `.remedy-wt/f273-r21/wk_suite_log.txt`, 271 lines):
  ```
  =================================== FAILURES ===================================
  ______ TestNoRetiredJobPlanStateReads.test_the_scan_reaches_a_real_corpus ______
  [gw13] linux -- Python 3.10.12 /usr/bin/python3
      def test_the_scan_reaches_a_real_corpus(self) -> None:
          """Anti-blindness: a scan over nothing would pass for the wrong reason."""
          files = _tracked_production_python_files()
  >       assert len(files) > 300, f"corpus collapsed to {len(files)} files"
  E       AssertionError: corpus collapsed to 299 files
  E       assert 299 > 300
  tests/orchestration/test_job_plan_state_reads.py:137: AssertionError
  =========================== short test summary info ============================
  FAILED tests/orchestration/test_job_plan_state_reads.py::TestNoRetiredJobPlanStateReads::test_the_scan_reaches_a_real_corpus
  1 failed, 17516 passed, 20 skipped, 1 warning in 207.79s (0:03:27)
  EXIT CODE: 1  WALL: 291.5s
  ```
  Exit code 1; bad nodes 1; `R-0803:` lines 0; the one warning is the `UserWarning` of `test_model_routing.py`'s undeclared-role test. Transcript `.agent/authored/f273-closure-suite.txt`, sha256 `a838b03a97eecc1fa49241d9a0a3e968e5bd3a1d2b0f207976c6f7afe318737f`, built by `.remedy-wt/f273-r21/wk_transcript.py` from the log, verbatim:
  ```
  1 failed, 17516 passed, 20 skipped, 1 warning in 207.79s (0:03:27)
  tests/orchestration/test_job_plan_state_reads.py::TestNoRetiredJobPlanStateReads::test_the_scan_reaches_a_real_corpus
  R-0803 lines: 0
  ```
- **G4** runs after the push and is reported in the round report, because this commit comes before it.

## Authored-text proofs

- Every C1 and C2 file was built by `python3 .remedy-wt/f273-r21/wk_build.py` from `git show c8b91d87:<path>` bytes and the digest-checked payload bytes, with no hand edit; G1 re-proves each against its payload at `d2fc05b8`.
- The `## Next` body below is `next.md` byte for byte, appended by `.remedy-wt/f273-r21/wk_c4.py`, which checks the payload digest first.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping (Gate F273 R20, `Done:` R-0994, R-0995, R-0996, plan, payload copies) | done | `f3571e8b` |
| C2 Built State append | done | `d2fc05b8` |
| G1 | done | True, exit 0 |
| G2 | done | 386 passed, exit 0 |
| C3 closure suite run + transcript commit | done | `309afcaf`; the run is red (1 failed), committed as ordered, not repaired |
| C4 handoff + push | done | This commit, then the push |
| G4 | done | After the push; in the round report |

## Open findings

Measured by `.remedy-wt/f273-r21/wk_count.py`, which loads `scripts/rotate_live_review.py` by path and calls `count_open_findings` (by distinct id) on the committed `.agent/live_review.md`:
- at `f3571e8b` (C1; C2 and C3 do not touch it): **13 open** — R-0499, R-0622, R-0662, R-0803, R-0807, R-0819, R-0820, R-0829, R-0866, R-0880, R-0892, R-0950, R-0984;
- at `c8b91d87`: 16 open.

C1's three `Done:` lines close three distinct ids: 16 - 3 = 13.

## Deviations & assumptions

- **Commit sequence:** as ordered: C1 to C4, then the push. No extra commit.
- **Red closure suite:** one bad node. The block orders no repair and no second run, so none was made; no attribution (serial re-run, main's hosted CI record) was attempted either, as that too lies outside the block. The assertion is a floor on the count of tracked production Python files (`> 300`), and the run counted 299.
- **Run log location:** `docs/agents/integration_gate.md` step 2 asks for run logs outside the repo worktree; `/tmp` is denied to this session, so the log went to the gitignored scratch directory `.remedy-wt/f273-r21/`, which the block names for scratch. Nothing from it is committed but the transcript.
- **Transcript blank lines:** the transcript has the summary line, the one bad node, and `R-0803 lines: 0`, one per line with no blank lines between, matching F271's transcript shape.
- **Operator questions:** the count below is the number of `### Q<n>` headings in `.agent/operator_questions.md` (Q1, Q2, Q4, Q5, Q7), unchanged this round.
- **Scratch:** gitignored under `.remedy-wt/f273-r21/`: `wk_run.py`, `wk_build.py`, `wk_g1.py`, `wk_transcript.py`, `wk_count.py`, `wk_c4.py`, `wk_suite_log.txt`, `handoff_head.md`.

## Next

1. Phase 1 rule 1 (`.agent/STOP`), then the review of round 21 over `c8b91d87`..the round 21
   handoff commit, booked as `Gate: F273 R21` in the next round's first commit, with the closure
   suite's transcript read from `.agent/authored/f273-closure-suite.txt`.
2. A red transcript: the repair rounds of amend0917-throughput. A green one: closure round A (the
   self-use item, the integrity check, the evidence job and the review zip), then closure round B.

Operator questions open: 5
