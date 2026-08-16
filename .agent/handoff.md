# Handback — F085 R7 (record the R6 PASS, register R-0498, fix R-0496)

Feature T2_F085 Sandbox hardening (stage 1) · Round R7 · Branch feature/f085-sandbox-hardening
Fortschritt: ~30 % (F085 beansprucht · Amendment F085 D1 angewandt · T001 gebaut · R6 PASS · R-0496 gefixt, R-0495 offen und T002 blockiert · T003 offen) — Schätzung
Open findings: 113 registered, 0 resolved, 113 open. Max R-0498, next free R-0499. R7 resolves NOTHING — `Landed: R-0496` is a worker note, not a resolution.

## Range

Review of ca5ff4f1756b38e7c176579abc753c0dcff06a22..HEAD

## Commits

### d0e597a3 docs(f085): save the R7 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r7.md | +253 -0 | C0a — the reviewer's block, copied byte-for-byte with `shutil.copyfile` |

### 779c3840 chore(agent): mirror the R7 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +156 -116 | C0b — the COMMITTED C0a blob read via `git show`, whole file |

### 11f03f47 docs(review): record the R6 PASS and register R-0498
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4 -0 | C1 — RECORD-R6 then R0498 appended verbatim, each preceded by one blank line |

### e77fa588 test(f085): compare cpu_seconds_used below the limit, not on it
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_exec_guard.py | +7 -1 | C2 — the CPU-ASSERT pair applied as a REWRITE; R-0496's boundary assertion |

### b6ef2a6e docs(review): note R-0496 landed in the R7 test fix
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 -0 | C3 — the LANDED-R0496 line, verbatim; the reviewer authors the resolution |

### 83c40b39 docs(f085): advance the plan to the R7 fix round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +12 -10 | C4 — whole file := the PLAN slice |

### (this commit) docs(f085): rewrite the handback for R7
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

`git push origin feature/f085-sandbox-hardening` after C4 → `ca5ff4f1..83c40b39`, success, origin at 83c40b39. A second push follows C5. `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`, exit 0. No PR created, no PR merged, no worktree added or removed.

## Verification

G1 `git status --porcelain` EMPTY immediately before C5 (only `.agent/handoff.md` in flight); `git worktree list` 1 line, `/home/decodeux/Repos/remedy 83c40b39 [feature/f085-sandbox-hardening]`; `.agent/STOP` absent, re-read from disk before the FIRST commit and again here. The post-C5 status reading is the R-0494 case and the reviewer measures it at the next gate.
G2 TRANSPORT `.remedy-wt/f085-r7.md`, committed `.agent/authored/f085-r7.md` and committed `.agent/last_block.md` all byte-EQUAL at sha256 f6fd67339f3c9745fb845b95a1fcb5649373c70c410a5852d97a3a7a027ca6af, 21267 B, 253 lines; one digest across all three.
G3 `.agent/plan.md` at HEAD byte-equals the PLAN slice; sha256 1a2b4a3ed34f4a4ade3ffef65f2d307aebe67b64e549c1439a26ba7434920a45, 2297 B, 40 lines; `## Goal` yes, `## Next Steps` yes, `F085` matched by `\bF\d{3}\b`, 40 < 50.
G4 pre-C1 225757 B (byte-identical to the blob at ca5ff4f1) is a byte-exact PREFIX of post-C1 231728 B; pre-C3 231728 B is a byte-exact PREFIX of post-C3 231994 B, which equals the HEAD blob. C1 tail 5971 B / 4 lines carries RECORD-R6 and R0498, each 1x in the tail and 1x in the WHOLE file; C3 tail 266 B / 2 lines carries LANDED-R0496, 1x in the tail and 1x in the WHOLE file. `git show --numstat 11f03f47 -- .agent/live_review.md` = `4 0`; `git show --numstat b6ef2a6e -- .agent/live_review.md` = `2 0`. Both deletion columns 0.
G5 regexes `^- R-\d+ — ` and `^Done: R-\d+ — `. Base ca5ff4f1: 112 registered, 0 resolved → 112 open. HEAD: 113 registered, 0 resolved → 113 open; 0 duplicate ids, 0 resolutions naming an unregistered id. Symmetric difference of HEAD-open against base-open plus R-0498: EMPTY. HEAD-open minus base-open = {R-0498}; base-open minus HEAD-open = {}. Resolutions added by R7: 0. Max R-0498, next free R-0499. LINE-START `^Landed: R-\d+` records at HEAD: exactly 1, naming R-0496.
G6 `.agent/live_review.md` still contains the substring `Steps`: yes, 21 occurrences.
G7 `git diff --name-only ca5ff4f1..HEAD` measured pre-C5, exit 0 = `.agent/authored/f085-r7.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `tests/orchestration/test_exec_guard.py` — the ordered set minus `.agent/handoff.md`, which is this commit. 0 paths under `packages/`, `docs/`, `apps/` or `scripts/`.
G8 UNCHANGED GUARD. `packages/orchestration/exec_guard.py` sha256 d9c77caec4ed9136868cef080bd2e2ae18c4216851507dc943d778d5c575114e, 12241 B, at ca5ff4f1 AND at HEAD — EQUAL. Constraint 4 held: no part of R-0495's fix landed here.
G9 PAIR SHAPE, a REWRITE. Over the WHOLE of `tests/orchestration/test_exec_guard.py` at HEAD the CPU-ASSERT-FROM text occurs 0 times and the line `    assert result.cpu_seconds_used >= 0.5` occurs exactly 1 time (exact full-line match). FROM occurred exactly 1 time before the edit. `git show --numstat e77fa588 -- tests/orchestration/test_exec_guard.py` = `7 1`.
G10 DETERMINISM, ten consecutive runs of `python3 -m pytest tests/orchestration/test_exec_guard.py -q` from the repository root at HEAD: run1 exit 0 `6 passed in 4.55s`; run2 exit 0 `6 passed in 4.56s`; run3 exit 0 `6 passed in 4.58s`; run4 exit 0 `6 passed in 4.57s`; run5 exit 0 `6 passed in 4.57s`; run6 exit 0 `6 passed in 4.56s`; run7 exit 0 `6 passed in 4.57s`; run8 exit 0 `6 passed in 4.57s`; run9 exit 0 `6 passed in 4.55s`; run10 exit 0 `6 passed in 4.55s`. ALL TEN exit 0, 10 green / 0 red. The coin flip R6 measured (worker 3 red of 7, reviewer 8 red of 12, always at `test_cpu_limit_kills_a_busy_loop_and_names_the_limit`) is gone.
G11 `python3 -m ruff check tests/orchestration/test_exec_guard.py` → exit 0, `All checks passed!`. Repository configuration, no `--isolated` (R-0463).
G12 `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, `42 passed in 20.50s`. Canary green, matching the reviewer's `42 passed` at ca5ff4f1.
G13 PROBE, the eight-file structural sweep run THREE times: run1 exit 0 `350 passed, 6 skipped in 15.38s`; run2 exit 0 `350 passed, 6 skipped in 15.22s`; run3 exit 0 `350 passed, 6 skipped in 15.34s`. No run was red, so no `-rf` FAILED node id exists to report.
G14 insertions (the `+` column): C0a 253, C0b 156, C1 4, C2 7, C3 2, C4 12 — none over 500. C5's own count is ordered nowhere (R-0494).
G15 `git log --format=%p ca5ff4f1..HEAD` → one parent per commit, linear: d0e597a3←ca5ff4f1, 779c3840←d0e597a3, 11f03f47←779c3840, e77fa588←11f03f47, b6ef2a6e←e77fa588, 83c40b39←b6ef2a6e. The reflog over THIS round is HEAD@{0}..HEAD@{5}, every entry `commit:`; HEAD@{6} and below are R6 and earlier. No amend, rebase, reset, branch switch or force-push.

## Authored-text proofs

PLAN, RECORD-R6, R0498, LANDED-R0496, CPU-ASSERT-FROM and CPU-ASSERT-TO were extracted programmatically from the COMMITTED `.agent/authored/f085-r7.md` by their one-line `<<<SLICE …>>>`/`<<<END …>>>` markers and applied byte-verbatim; none was retyped. G2 proves that file byte-equal to the reviewer's `.remedy-wt/f085-r7.md` on disk (not a digest fallback). Disk-to-disk equality is proved by G3 (whole file equals the slice), G4 (prefix preserved, each slice exactly once in the appended tail and once in the whole file) and G9 (FROM 0x, TO 1x). No marker LINE reached a target file: 0 `<<<SLICE` and 0 `<<<END` in `.agent/plan.md`, `.agent/live_review.md` and `tests/orchestration/test_exec_guard.py`. The single `<<<` occurrence in `.agent/live_review.md` is pre-existing authored prose, present identically at ca5ff4f1.

## Deviations & assumptions

1. The ordered sequence C0a, C0b, C1, C2, C3, C4, C5 was followed exactly — seven commits, none added, none dropped, no reordering.
2. `cp` and the `remedy` CLI are denied in this session. C0a used `shutil.copyfile`; C0b wrote the bytes of the COMMITTED C0a blob read via `git show`. G2 proves the byte property the gates name.
3. Commit Gate at C0a–C3: `.agent/plan.md` still described R6, because C4 is the bundle's sixth commit. That is R-0491, which this bundle carries unchanged.
4. `.agent/context.md` and `.agent/decisions.md` were NOT updated: constraint 3 limits the change set to the ordered paths.
5. One timing run of the G10 command preceded the ten (exit 0, `6 passed in 4.55s`) to size the gate's runtime. It is NOT counted in G10; the ten reported runs are ten fresh consecutive runs.
6. Gate scratch (slice pickle, pre-C1/pre-C3 blobs, four gate scripts, this draft) was written under the gitignored `.remedy-wt/`; nothing entered the change set and `git status --porcelain` is clean.
7. R-0495 was NOT touched, per constraint 4. G8 is its byte proof.
8. Stated-cause overage (DECISION D15): this file is 103 lines, over the 60-line base cap and over the 100-line >5-commit cap of docs/agents/handback_template.md, and over that template's 800-token thrift cap; no byte or token figure is stated here because such a figure would change the text that states it. Cause is mandated content only — seven per-commit tables for a seven-commit bundle, the item-status table covering C0a..C5, and a FIFTEEN-gate verification block of which G10 alone must carry ten exit codes and ten summary lines because the gate orders exactly that. No section was dropped, no transcript was padded.

## Next

- R8 is a REPAIR round and fixes R-0495, the wall timeout that does not bound `run_guarded`'s own return; it is the last thing blocking T002a;
- `tests/orchestration/test_exec_guard.py` is GREEN and DETERMINISTIC as of this round, measured over ten runs, and R-0495 is a defect the suite does not yet cover — a green suite is not evidence that the guard bounds runtime;
- `exec_guard.py` still has NO callers, so no containment claim holds for the running system;
- there is NO open PR for this branch and none is opened before closure;
- the R7 verdict is written by the NEXT round's record commit.
