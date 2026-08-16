# Handback — F085 R5 (record + T001 build round)

Feature T2_F085 Sandbox hardening (stage 1) · Round R5 · Branch feature/f085-sandbox-hardening
Fortschritt: ~25 % (F085 beansprucht · Seam-Inventar abgenommen · Amendment F085 D1 angewandt · T001 gebaut, ungenutzt · T002/T003 offen) — Schätzung
Open findings: 109 registered, 0 resolved, 109 open. Max R-0494, next free R-0495.

## Range

Review of 382ed7fa2055d38bc6ff94164c8cb993f28ce9fb..HEAD

## Commits

### 06379298 chore(agent): save the F085 R5 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r5.md | +341 -0 | C0a — the reviewer's block, copied byte-for-byte |

### 4bbcab4c chore(agent): mirror the R5 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +250 -227 | C0b — the COMMITTED C0a file, whole |

### c15e236a docs(review): record the R4 PASS and register R-0494
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4 -0 | C1 — RECORD-R4 then R0494, appended verbatim, first commit of the round |

### f51b2309 docs(f085): advance the plan to the R5 build round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +16 -16 | C2 — whole file := the PLAN slice |

### e0d4d880 feat(orchestration): add exec_guard with rlimit, wall-timeout and output-cap mechanics
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/exec_guard.py | +314 -0 | C3 — T001, worker-authored, NO callers |

### 0268d7a8 test(orchestration): cover exec_guard with the four runaway fixtures
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_exec_guard.py | +170 -0 | C4 — worker-authored, 6 tests, all `subprocess`-marked |

### (this commit) docs(f085): rewrite the handback for R5
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | see note | C5 — a handback cannot table the commit that writes it (R-0149); under R-0494 its own numbers are ordered nowhere and the reviewer measures them at the next gate |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit |

## External actions

`git push origin feature/f085-sandbox-hardening` after C4 → `382ed7fa..0268d7a8`, success. A second push follows C5. No PR created, no merge, no other `gh` command, no worktree added or removed this round.

## Verification

G1 `git status --porcelain` EMPTY immediately before C5 (only `.agent/handoff.md` in flight); `git worktree list` 1 line; `.agent/STOP` absent, re-read from disk before the first commit and again here.
G2 TRANSPORT `.remedy-wt/f085-r5.md`, committed `.agent/authored/f085-r5.md` and committed `.agent/last_block.md` all byte-EQUAL at sha256 4d1188a70d2f8d1ff23f6a5801c212b4406a738c7d6c59d77bb1877047ab9220, 26997 B, 341 lines.
G3 `.agent/plan.md` at HEAD byte-equals the PLAN slice; sha256 cbc8ee8a0b3b7196ae4dd9832abb66b009ccbe959ae0706f06f2ec2f266547a8, 41 lines, 2255 B; `## Goal` yes, `## Next Steps` yes, F085 matched, under 50 lines.
G4 pre-C1 208910 B is a byte-exact PREFIX of post-C1 214867 B; 5957-byte, 4-line tail; RECORD-R4 1x and R0494 1x in the whole file, both inside the tail; `git show --numstat c15e236a -- .agent/live_review.md` = `4 0`, deletion column 0. 0 marker lines reached the file.
G5 regexes `^- R-\d+ — ` and `^Done: R-\d+ — `. Base 382ed7fa: 108 registered, 0 resolved → 108 open. HEAD: 109 registered, 0 resolved → 109 open; 0 duplicate ids, 0 resolutions naming an unregistered id. Symmetric difference of HEAD-open against base-open plus R-0494: EMPTY. Newly resolved by R5: none. Max R-0494, next free R-0495. LINE-START `^Landed: R-\d+` records at HEAD: 0.
G6 `.agent/live_review.md` still contains the substring `Steps`: yes.
G7 `git diff --name-only 382ed7fa..HEAD` measured pre-C5 = `.agent/authored/f085-r5.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `packages/orchestration/exec_guard.py`, `tests/orchestration/test_exec_guard.py` — the ordered set minus `.agent/handoff.md`, which is this commit. 0 paths under `docs/`, `apps/` or `scripts/`. The post-C5 reading is the R-0494 case: the reviewer measures it at the next gate.
G8 `grep -rn "exec_guard" packages/ apps/ scripts/ tests/` → 2 lines, BOTH in `tests/orchestration/test_exec_guard.py` (its docstring and its import). NO third file, so T002 did not start here. Difference from the gate's wording, flagged not edited: `packages/orchestration/exec_guard.py` does not match because grep reads CONTENT and the module does not name its own path; the file was not edited to make it match.
G9 `python3 -m ruff check packages/orchestration/exec_guard.py tests/orchestration/test_exec_guard.py` → exit 0, `All checks passed!`. Run from the repository root against the repo `pyproject.toml`, never `--isolated`.
G10 the eight-file sweep → exit 0, `350 passed, 6 skipped in 15.19s` — the same count the reviewer measured at 382ed7fa, so the new orchestration module trips none of those guards.
G11 `python3 -m pytest tests/orchestration/test_exec_guard.py -q` → exit 0, `6 passed in 4.59s`.
G12 NO ORPHANS, immediately after G11: `pgrep -af REMEDY_EXEC_GUARD_FIXTURE` → exit 1, stdout EMPTY, 0 lines after excluding pgrep's own.
G13 `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, `42 passed in 20.68s`.
G14 insertions: C0a 341, C0b 250, C1 4, C2 16, C3 314, C4 170 — none over 500. C5's own count is ordered nowhere (R-0494).
G15 `git log --format=%p 382ed7fa..HEAD` → one parent per commit, linear. The reflog over THIS round is HEAD@{0}..HEAD@{5}, every entry `commit:`; HEAD@{6} and below are R4. No amend, rebase, reset, branch switch or force-push.
G16 MEMORY PROBE, tight arm of test (e), `address_space_bytes` 67108864 (64 MiB) against a 200 MiB allocation: `returncode` 1, NO term_signal (WIFEXITED true, WIFSIGNALED false), stderr last line `MemoryError`, `ru_maxrss` 25544 KiB = 26157056 B, BELOW the limit. This CONFIRMS the reviewer's stated reason rather than contradicting it: `wait4` holds nothing that separates this death from any other exit 1, so stage 1 cannot attribute it. R6 rules on whether a second evidence source can.
G17 NO OVERCLAIM: checked in the module docstring (`packages/orchestration/exec_guard.py` lines 9-15, the "Deliberate absences" block: NO CALLER, no env scrubbing, no network posture), in the test-file docstring (lines 7-8), and by scanning both files for `guarded|sandbox|protect|secure|hardened` — every hit is the API name `run_guarded` or a run performed BY this module, never a claim about an existing seam. Nothing calls `run_guarded`; G8 is the measurement.

## Authored-text proofs

PLAN, RECORD-R4 and R0494 were extracted programmatically from the COMMITTED `.agent/authored/f085-r5.md` by their one-line `<<<SLICE …>>>`/`<<<END …>>>` markers and applied byte-verbatim; none was retyped. Disk-to-disk equality is proved by G3 (whole file equals the slice) and G4 (prefix preserved, each slice exactly once, inside the appended tail). No marker LINE reached a target file: 0 in `.agent/plan.md`, 0 in `.agent/live_review.md`. The single `<<<` occurrence in `.agent/live_review.md` is authored prose inside the RECORD-R4 paragraph, not a transport marker.

## Deviations & assumptions

1. The ordered sequence C0a, C0b, C1, C2, C3, C4, C5 was followed exactly — seven commits, none added, none dropped, no reordering.
2. `cp` and the `remedy` CLI are denied in this session. C0a used `shutil.copyfile`; C0b wrote the bytes of the COMMITTED C0a blob. G2 proves the byte property the gate names.
3. `packages/orchestration/exec_guard.py` and `tests/orchestration/test_exec_guard.py` are WORKER-authored from the block's contract, as Change items 5 and 6 require. The reviewer authored no byte of either.
4. Contract choices the block left open, so the reviewer can reject them cheaply: `returncode` is the exit status when the child exited normally and `None` when it died on a signal, which is what makes `term_signal` non-redundant; `limits_enforced` also carries the guard-side `wall_timeout` and `output_bytes`, so `tripped_limit` is always a member of it; requested rlimits are clamped DOWN to the inherited hard limit, since an unprivileged process may lower a limit and never raise one; an output cap does NOT end the child, because the cap bounds memory while `wall_timeout_seconds` and `cpu_seconds` bound runtime. Each is stated in the module docstring.
5. Exit detection uses `os.waitid(..., WNOWAIT)` before `os.wait4`. WHY: observing the exit without reaping keeps the zombie in its process group, so the group kill on the normal-exit path cannot reach a recycled pid.
6. G8 differs from its wording and was NOT repaired by editing the file it measures; the difference and its cause are in the Verification block.
7. Commit Gate at C0a and C0b: `.agent/plan.md` still described R4, because C2 is the bundle's fourth commit. That is R-0491, which this bundle carries unchanged.
8. `.agent/context.md` and `.agent/decisions.md` were NOT updated: Constraint 3 limits the change set to the seven ordered paths.
9. `.remedy-wt/` gained gate scratch (three probe scripts, one pre-C1 blob): the already-registered R-0403 mechanism. The directory is gitignored; `git status --porcelain` is EMPTY.
10. Stated-cause overage (DECISION D15): this file is 106 lines, over the >5-commit cap of 100 and over the 60-line base cap. Cause is mandated content only — seven per-commit tables, the item-status table and the seventeen-gate verification block. No section was dropped and no transcript was padded.

## Next

- R6 is the next round: the seam migration begins with T002a (builder, 5 sites), and it too is a SPLIT round.
- `exec_guard.py` has NO callers yet, so nothing in Remedy is guarded by it and no containment claim may be made for the running system.
- There is NO open PR for this branch and none is opened before closure.
- The R5 verdict is written by the NEXT round's record commit.
