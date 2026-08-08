# Handback — F103 R5, the integration gate

Feature **T2_F103 — Token ledger (SQLite)**, round **R5** (the canonical gate,
docs/agents/integration_gate.md). Branch **`feature/f103-token-ledger`**, entered
at `e984bbab` — not re-cut, no PR, no merge, no force-push, `main` untouched.
`.agent/STOP` absent, re-checked before every commit. **NO production code and no
test file was changed this round**; the diff is `.agent/` only.

## Range
Review of `e984bbab..HEAD`. Three evidence commits; this file is the fourth.

## Commits
### 7fd00b80 chore(f103): record the R5 branch-side gate run
| Path | +/- | Reason |
|---|---|---|
| .agent/gate_f103_r5/branch_run.txt | +53/-0 | header, trimmed tail, grep counts over the FULL log |
| .agent/gate_f103_r5/branch_failed.txt | +0/-0 | empty on purpose — an empty file is evidence |

### b52a698e chore(f103): record the R5 base run, parity check and comparison
| Path | +/- | Reason |
|---|---|---|
| .agent/gate_f103_r5/base_run.txt | +61/-0 | same shape + the COMPLETE FAILED section |
| .agent/gate_f103_r5/base_failed.txt | +8/-0 | untrimmed sorted id list |
| .agent/gate_f103_r5/base_serial_rerun.txt | +170/-0 | serial re-runs, passes 1-4 incl. the negative control |
| .agent/gate_f103_r5/comm_branch_only_failures.txt | +0/-0 | `comm -13`, empty |
| .agent/gate_f103_r5/comm_base_only_failures.txt | +8/-0 | `comm -23` |
| .agent/gate_f103_r5/dist_hashes.txt | +56/-0 | parity + the before/after hash verdict |
| .agent/gate_f103_r5/worktree_cleanup.txt | +17/-0 | remove/prune/branch -D + `git worktree list` |

### 3178bfb5 chore(f103): attribute every gate id and measure the ledger seam
| Path | +/- | Reason |
|---|---|---|
| .agent/gate_f103_r5/attribution.txt | +134/-0 | sections 1-5, every id both directions |
| .agent/gate_f103_r5/r0218_seam_timing.txt | +90/-0 | R-0218's number |

### (this commit) chore(f103): rewrite handoff for the R5 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback — cannot table its own SHA |

Staged by exact path; `git add -A` never used. `.agent/plan.md` deliberately
UNTOUCHED: it was already synced to R5 and the gate produced no blocker, so
nothing in it changed.

## Verification (real commands, real exit codes)
| Command | Exit | Tail |
|---|---|---|
| `REMEDY_UI_NO_AUTO_BUILD=1 python3 -m pytest -n auto -q` (branch, repo root) | **0** | `16121 passed, 19 skipped in 123.68s (0:02:03)` |
| `REMEDY_UI_NO_AUTO_BUILD=1 python3 -m pytest -n auto -q` (base worktree root) | **1** | `8 failed, 16008 passed, 19 skipped in 155.11s (0:02:35)` |
| `python3 -m pytest tests/cli/test_golden_path.py -q` (canary) | **0** | `42 passed in 19.54s` |
| `git status --porcelain` | **0** | no output — clean tree |
| `git worktree list` | **0** | primary checkout only; `tmp/base-gate-f103` deleted |
| R-0218 harness (throwaway, uncommitted) | **0** | `median +1.386 ms (+236.2%)` |
Repo-wide sweep for `*.sqlite`, `*-wal`, `*-shm` incl. `.data/`: **0 hits**.

## Gate result (inputs only — the verdict is Window 1's)
Branch-only ids (`comm -13`): **0**. Base-only ids (`comm -23`): **8**, all
attributed by direct evidence — 1 xdist port race (`Errno 98`, serial-pass 4/4)
and 7 sharing one cause: `_frontend_is_stale` compares MTIMES, a fresh worktree
checkout is newer than a `cp -a`'d dist, so the server refuses to build and
exits 1. Proved by a negative control: moving the dist mtimes back reproduces
all 7 without changing a byte; restoring them makes them pass. No branch-only
failure coupled to F103 code, so nothing blocks under step 4.

## Item status — R5 bundle B1-B5
| Item | Status | Reason |
|---|---|---|
| B1 branch run + failed list | done | exit 0, zero FAILED |
| B2 base run, parity by COPY, dist hash verified | deviated | see Deviations 1 and 3 |
| B3 compare + attribute every id both directions | done | 0 / 8, all attributed |
| B4 R-0218 seam timing | done | +1.386 ms median, no verdict written |
| B5 commit, push, rewrite handoff | done | this commit, then push |

## Findings
Open findings: **1** — R-0218 (Low), still OPEN. It is now PAID WITH A NUMBER
and the reviewer closes it after reading that number, not before. Next free ID:
**R-0220**. Possible new finding for Window 1 to raise or drop:
`tests/ui_server/test_dashboard_contract.py:521`
`TestAutoBuildBehavior::test_auto_build_runs_by_default` pops
`REMEDY_UI_NO_AUTO_BUILD` and runs a real `npm` build in whatever checkout it
finds — the named cause of the R-0169 class recurring. No test was changed.

## Deviations, declared
1. **Scratchpad and base worktree live at `.remedy-wt/…` inside the repo
   DIRECTORY, not `/tmp`.** Not a choice: this session's permission policy
   refuses every write outside `/home/decodeux/Repos/remedy` (`mkdir
   /tmp/remedy-f103-r5` → blocked, twice, also with the sandbox override).
   R-0176's SUBSTANCE is preserved and checked: `.remedy-wt/` is gitignored
   (`.gitignore:235`), and the only untracked-file input to the worktree digest
   is `git ls-files --others --exclude-standard` (`run_manifest.py:500`), which
   returns **0** hits for `remedy-wt`. So nothing digest-visible grew during
   either run. Logs were still written to the scratchpad and copied into
   `.agent/gate_f103_r5/` only after each run exited. The scratchpad, incl. the
   harness and its sqlite work dir, was deleted before the sweep above. One
   unrelated gitignored leftover from an earlier halted attempt
   (`.remedy-wt/scratch_f103_r5/`, 11:44) was left alone as not mine to remove.
2. **Three evidence commits, not two.** The prescribed boundary (branch-side,
   then base-side + compare + attribution + timing) makes a 540-line second
   commit, over the 500-line cap. Split at 53 / 320 / 224. No oversize
   exception is claimed.
3. **The neutralization is NOT clean, and the round says so instead of
   claiming a pass.** The dist aggregate CONTENT hash is identical before and
   after the base run (`fb68a729…`), so the parity claim holds and no
   `comm -23` id may be blamed on differing dist bytes. But the dist MTIMES
   moved mid-run in BOTH checkouts, because the test named under Findings
   builds for real. Its output is byte-identical, which is why the hash never
   moved. Recorded in full in `dist_hashes.txt`.
4. **The base worktree already existed at round start** (leftover at
   `.remedy-wt/base-f103` on `tmp/base-gate-f103` from a halted attempt). It
   was destroyed and recreated from scratch, never reused, then removed again.
5. This file is 120 lines, over the 60-line cap, with NO section dropped.
   Cause, all mandated: four per-commit changed-files tables, the six-row
   verification table, the B1-B5 item-status table, and these deviations.
6. Commit 4's SHA and the push result are absent by self-reference
   impossibility, not omission; both are in the completion report.

## Next
Window 1 reviews `e984bbab..HEAD` and issues the GATE VERDICT (integration_gate
step 5) — this round issued none — and decides R-0218 against the measured
number. On PASS, R6 is closure per docs/roadmap/STATUS_closure_protocol.md.
