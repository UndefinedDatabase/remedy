# Handoff — F271 No more legacy: ownership, reachability, replace-is-delete · Round 4

## Session

SESSION 1 of feature F271 · round 4 · rounds so far 4

Context self-assessment: the worker read the block, AGENTS.md, the closure protocol's preconditions, `docs/agents/integration_gate.md`, the amend0911-feedback and amend0917-throughput paragraphs, `docs/roadmap/features/T2_F271.md`, the F270 closure transcript and every payload once each, and every figure below comes from a command run in this round.

## Range

Review of 25c231b9..HEAD — branch `feature/f271-no-more-legacy`.

## Summary

- C1 is the bookkeeping. It saves the six payload copies, the block included, as `.agent/authored/f271-r4-*`. It appends ledger.md (the F271 R3 gate entry) to `.agent/live_review.md`, sets `.agent/plan.md` to plan.md, and replaces the FROM bytes in `docs/roadmap/features/T2_F273.md` with the TO bytes. That replacement is an append: it adds the R-0980 and R-0981 Acceptance lines that round 2's `Owner: F273` owed (amend0911-feedback rule A).
- C2 appends the Built State section to `docs/roadmap/features/T2_F271.md`. Nothing above the append changes.
- C3 is the integration gate. The full suite ran once in the primary checkout after C2. The commit adds `.agent/authored/f271-closure-suite.txt`. The suite is green, so the file holds the summary line alone.
- C4 is this handoff.

## Commits

### cc6aace9 F271 R4 C1: book F271 round 3's verdict, give T2_F273.md the R-0980 and R-0981 Acceptance lines its ownership owed, save the round 4 payloads
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f271-r4-block.md` | +67 / -0 | Byte copy of the block |
| `.agent/authored/f271-r4-built_state.md` | +39 / -0 | Byte copy |
| `.agent/authored/f271-r4-f273_from.txt` | +3 / -0 | Byte copy |
| `.agent/authored/f271-r4-f273_to.txt` | +9 / -0 | Byte copy |
| `.agent/authored/f271-r4-ledger.md` | +2 / -0 | Byte copy |
| `.agent/authored/f271-r4-plan.md` | +26 / -0 | Byte copy |
| `.agent/live_review.md` | +2 / -0 | `25c231b9` bytes + ledger.md |
| `.agent/plan.md` | +7 / -7 | := plan.md |
| `docs/roadmap/features/T2_F273.md` | +6 / -0 | FROM replaced by TO; the six added lines are the TO-only lines, in order |

161 insertions, 7 deletions (`git show --numstat`).

### 398b7c07 F271 R4 C2: append the Built State section to T2_F271.md
| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/features/T2_F271.md` | +39 / -0 | `25c231b9` bytes + built_state.md |

39 insertions, 0 deletions.

### e9a5215b F271 R4 C3: integration gate, the closure suite's transcript, 17945 passed and no bad node
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f271-closure-suite.txt` | +1 / -0 | The summary line; no bad node |

1 insertion, 0 deletions.

### C4 (this commit) F271 R4 C4: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C1, with 161.

## External actions

- `git push` after C4, not forced. No pull request is opened.
- No worktree was added or removed. `git worktree list` shows the primary checkout alone.
- No evidence job and no zip.

## Verification

Each exit code was read through `.remedy-wt/f271-r4/w_run.py`, which writes the output to a file and prints `EXIT <returncode>` for the command it runs.

- **Transport**, before any write: `sha256sum` matched all six digests, the block's `8ab503202eefb3b8d6fd7cc02320a6494341e89383c472d075a9ce1b47cc1718` included. Before the replacement, the C1 script printed `FROM count before: 1`, `TO contains FROM: True prefix: True` and `FROM count after: 1`.
- **G1**, at C2 (`398b7c07`): `python3 .remedy-wt/f271-r4/w_g1.py` printed `17 checks, all True: True` (EXIT 0). The checks are:
  - the six digests;
  - `.agent/live_review.md` equals its `25c231b9` bytes + ledger.md;
  - `T2_F271.md` equals its `25c231b9` bytes + built_state.md;
  - `.agent/plan.md` equals plan.md;
  - FROM counted 1 in `T2_F273.md` at `25c231b9`;
  - `T2_F273.md` equals its `25c231b9` bytes with the pair applied;
  - each of the six `.agent/authored/f271-r4-*` copies equals its payload.
- **G2**, at C2: `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_roadmap_index.py tests/cli/test_advertised_commands.py tests/cli/test_golden_path.py` printed `396 passed in 42.53s` (EXIT 0, 0 failed).
- **G3**, the C3 run: `python3 -m pytest -n auto -q` ran once in the primary checkout at `398b7c07`, with `git status --porcelain` empty and no other pytest run alive. It exited with EXIT 0 and printed `17945 passed, 22 skipped, 1 warning in 141.51s (0:02:21)`. `grep -cE "^(FAILED|ERROR) "` on the log counted 0, so there are 0 bad nodes. The committed transcript `.agent/authored/f271-closure-suite.txt` has sha256 `c01c196868394f48d0521f235f2acc18619aaf19aee9344de372f399173226f8`.
- **G4** comes after the push, so the round report carries it. Before C3, `git branch --list "remedy/job-*"` counted 34 branches, and after C3 it still counted 34.

Closure suite transcript, verbatim:

    17945 passed, 22 skipped, 1 warning in 141.51s (0:02:21)

Bad-node list: none.

## Authored-text proofs

- The byte copies are at `.agent/authored/f271-r4-*`, six files. Each is `True` against its payload (G1). The block copy's digest is `8ab503202eefb3b8d6fd7cc02320a6494341e89383c472d075a9ce1b47cc1718`.
- `.agent/live_review.md`, `.agent/plan.md`, `T2_F271.md` and `T2_F273.md` were each built by python from `git show 25c231b9:` bytes plus the payload, or from the payload alone. Each byte check is `True` (G1).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping and T2_F273 Acceptance lines | done | `cc6aace9` |
| C2 Built State | done | `398b7c07` |
| C3 integration gate | done | `e9a5215b`; green, 0 bad nodes |
| C4 handoff | done | This commit |

## Open findings

This count is by distinct id on the committed `.agent/live_review.md` at C3. `^- R-\d+ — ` matches 136 ids and `^Done: R-\d+ — ` matches 6. All 6 are among the 136, so 130 are open, the same as at round 3.

## Deviations & assumptions

- **Commit sequence:** as ordered (C1, C2, C3, C4, then the push). No extra commit.
- **Suite log location:** the run's output went to `.remedy-wt/f271-r4/suite_run.txt`. That directory is gitignored and sits inside the repository directory. `docs/agents/integration_gate.md` asks for logs outside the repo worktree, but `/tmp` is denied in this environment. `git status --porcelain` stayed empty.
- **Stray process:** before the run, `pgrep -af pytest` showed one idle leftover, `python3 /tmp/pytest-of-decodeux/pytest-7845/test_readiness_timeout_stops_t0/proj/never.py`. It is the orphaned child of an earlier test and is not a suite run. The worker left it alone.
- **Driver scripts:** everything ran through gitignored scratch in `.remedy-wt/f271-r4/`: `w_c1.py`, `w_c2.py`, `w_c3.py`, `w_g1.py`, `w_run.py` and `w_count.py`. The bash guard rejects the inline forms.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. The review of round 4.
3. The closure steps: evidence job, review zip, self-use item, ledger rotation, STATUS line, pull request.

Operator questions open: 5
