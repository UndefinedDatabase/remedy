# Handback — F085 R8 (record the R7 PASS, resolve R-0496, fix R-0495)

Feature T2_F085 Sandbox hardening (stage 1) · Round R8 · Branch feature/f085-sandbox-hardening
Fortschritt: ~35 % (F085 beansprucht · Amendment F085 D1 angewandt · T001 gebaut · R7 PASS · R-0495 und R-0496 gefixt · T002 entsperrt, offen · T003 offen) — Schätzung
Open findings: 114 registered, 1 resolved, 113 open. Max R-0499, next free R-0500. R8 resolves R-0496 and registers R-0499.

## Range

Review of d37d1a1eba7ffdc7e332e8a7ab4c9c9eedf368bf..HEAD

## Commits

### 988869c6 docs(f085): save the R8 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r8.md | +393 -0 | C0a — the reviewer's block, copied byte-for-byte with `shutil.copyfile` |

### a69acc07 chore(agent): mirror the R8 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +268 -128 | C0b — the COMMITTED C0a file copied whole with `shutil.copyfile` |

### 1a0cc0ae docs(review): record the R7 PASS, resolve R-0496 and register R-0499
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +5 -1 | C1 — LANDED-R0496 (the file's last line) replaced by DONE-R0496, then RECORD-R7 and R0499 appended, each after one blank line |

### 73ff1b40 fix(orchestration): bound the guard's own drain so an escaped descendant cannot hang it
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/exec_guard.py | +32 -5 | C2 — all seven GUARD pairs; the R-0495 fix: one drain deadline for both pumps, `streams_complete` on the result |

### ded2dbb1 test(f085): hold the call bound when a descendant escapes the process group
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_exec_guard.py | +35 -0 | C3 — the NEW-TEST slice appended at EOF after one blank line; the setsid-escapee property |

### 66ce3b9e docs(f085): advance the plan to the R8 drain-bound round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +12 -13 | C4 — whole file := the PLAN slice |

### (this commit) docs(f085): rewrite the handback for R8
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

`git push origin feature/f085-sandbox-hardening` after C4 → `d37d1a1e..66ce3b9e`, success, origin at 66ce3b9e. A second push follows C5. `git worktree add --detach .remedy-wt/g12-red HEAD` → success, detached at 66ce3b9e (G12 only); `git worktree remove --force .remedy-wt/g12-red` then `git worktree prune` → success, list back to one line. `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`, exit 0. No PR created, none merged.

## Verification

G1 `git status --porcelain` EMPTY immediately before C5 (only `.agent/handoff.md` in flight) and EMPTY throughout G12; `git worktree list` 1 line, `/home/decodeux/Repos/remedy 66ce3b9e [feature/f085-sandbox-hardening]`; `.agent/STOP` absent, re-read from disk before the FIRST commit and again here. The post-C5 status reading is the R-0494 case and the reviewer measures it at the next gate.
G2 TRANSPORT `.remedy-wt/f085-r8.md`, committed `.agent/authored/f085-r8.md` and committed `.agent/last_block.md` all byte-EQUAL at sha256 b89466df0a7caa60971c727be97ae1ab0de7478476fc7be391a0bdb63163dfde, 27927 B, 393 lines; one digest across all three.
G3 `.agent/plan.md` at HEAD byte-equals the PLAN slice; sha256 a0bd751ab5087eea336976f65cc2aa62f79dddf74fbecbc672d6bf92ab2db1a5, 2235 B, 39 lines; `## Goal` yes, `## Next Steps` yes, `F085` matched by `\bF\d{3}\b`, 39 < 50.
G4 pre-C1 blob 231994 B ends with the LANDED-R0496 line; stripping that line leaves 231729 B, which is a byte-exact PREFIX of the post-C1 231729+6700 = 238429 B file. The 6700 B remainder after that prefix equals DONE-R0496 + one blank line + RECORD-R7 + one blank line + R0499, byte for byte. `git show --numstat 1a0cc0ae -- .agent/live_review.md` = `5 1`; the single deletion is the retired `Landed:` line.
G5 regexes `^- R-\d+ — ` and `^Done: R-\d+ — `. Base d37d1a1e: 113 registered, 0 resolved → 113 open. HEAD: 114 registered, 1 resolved → 113 open; 0 duplicate ids, 0 resolutions naming an unregistered id. REGISTERED symmetric difference HEAD vs base = {R-0499}; base minus HEAD = {} (nothing lost); HEAD registered == base registered ∪ {R-0499} is True. RESOLVED symmetric difference = {R-0496}; HEAD resolved == {R-0496} is True against an empty base. Max R-0499, next free R-0500. LINE-START `^Landed: R-\d+` records: 1 at d37d1a1e, 0 at HEAD — C1 retired it.
G6 `.agent/live_review.md` still contains the substring `Steps`: yes, 23 occurrences on 17 lines.
G7 `git diff --name-only d37d1a1e..HEAD` measured pre-C5, exit 0 = `.agent/authored/f085-r8.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `packages/orchestration/exec_guard.py`, `tests/orchestration/test_exec_guard.py` — the ordered set minus `.agent/handoff.md`, which is this commit. 0 paths under `docs/`, `apps/` or `scripts/`.
G8 PAIR PROOF over the WHOLE of `packages/orchestration/exec_guard.py` at HEAD. REWRITES: GUARD5 FROM 0x / TO 1x; GUARD6 FROM 0x / TO 1x. APPENDS: GUARD1 TO 1x, GUARD2 TO 1x, GUARD3 TO 1x, GUARD4 TO 1x, GUARD7 TO 1x. Every FROM occurred exactly 1x before its edit, verified pre-C2. `git show --numstat 73ff1b40 -- packages/orchestration/exec_guard.py` = `32 5`.
G9 NO CALLER. `grep -rn "exec_guard" packages/ apps/ scripts/ tests/` names exactly one file: `tests/orchestration/test_exec_guard.py`. The module does not write its own name inside itself (R-0497), so constraint 4 holds and no call site was migrated.
G10 `python3 -m ruff check packages/orchestration/exec_guard.py tests/orchestration/test_exec_guard.py` → exit 0, `All checks passed!`. Repository configuration, no `--isolated` (R-0463).
G11 DETERMINISM, ten consecutive runs of `python3 -m pytest tests/orchestration/test_exec_guard.py -q` from the repository root at HEAD: run1 exit 0 `7 passed in 7.66s`; run2 exit 0 `7 passed in 7.64s`; run3 exit 0 `7 passed in 7.63s`; run4 exit 0 `7 passed in 7.61s`; run5 exit 0 `7 passed in 7.63s`; run6 exit 0 `7 passed in 7.63s`; run7 exit 0 `7 passed in 7.59s`; run8 exit 0 `7 passed in 7.62s`; run9 exit 0 `7 passed in 7.63s`; run10 exit 0 `7 passed in 7.60s`. ALL TEN exit 0, ALL TEN `7 passed`; 10 green / 0 red.
G12 RED CONTROL in the disposable worktree only. The line `            pump.join(max(drain_deadline - time.monotonic(), 0.0))` occurred exactly 1x in the worktree copy and was replaced by `            pump.join()` there. `python3 -m pytest tests/orchestration/test_exec_guard.py -q -rf` in that worktree → exit 1, `1 failed, 6 passed in 24.72s`. The only `-rf` FAILED node id: `FAILED tests/orchestration/test_exec_guard.py::test_wall_timeout_bounds_the_call_when_a_descendant_escapes_the_group`. Decisive line: `assert result.streams_complete is False` / `E AssertionError: assert True is False` — the unbounded join waited out the escapee, so the drain completed and the property the fix asserts disappeared. Matches the reviewer's measurement exactly. Worktree removed and pruned; the primary checkout was never modified.
G13 `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, `42 passed in 20.50s`. Canary green, matching the reviewer's `42 passed` at d37d1a1e.
G14 PROBE, the eight-file structural sweep with `-rf`, run THREE times: run1 exit 0 `350 passed, 6 skipped in 15.24s`; run2 exit 0 `350 passed, 6 skipped in 15.37s`; run3 exit 0 `350 passed, 6 skipped in 15.37s`. No run was red, so no `-rf` FAILED node id exists to report and R-0499 gains no new observation.
G15 insertions (the `+` column): C0a 393, C0b 268, C1 5, C2 32, C3 35, C4 12 — none over 500. C5's own count is ordered nowhere (R-0494). `git log --format=%p d37d1a1e..HEAD` → one parent per commit, linear: 988869c6←d37d1a1e, a69acc07←988869c6, 1a0cc0ae←a69acc07, 73ff1b40←1a0cc0ae, ded2dbb1←73ff1b40, 66ce3b9e←ded2dbb1. The reflog over THIS round is HEAD@{0}..HEAD@{5}, every entry `commit:`; HEAD@{6} and below are R7 and earlier. No amend, rebase, reset, branch switch or force-push.

## Authored-text proofs

All twenty slices — PLAN, RECORD-R7, R0499, LANDED-R0496, DONE-R0496, NEW-TEST and the fourteen GUARD1..GUARD7 FROM/TO texts — were extracted programmatically from `.remedy-wt/f085-r8.md` by their one-line `<<<SLICE …>>>`/`<<<END …>>>` markers, never by substring split, and applied byte-verbatim; none was retyped. G2 proves that file byte-equal to the COMMITTED `.agent/authored/f085-r8.md` and to `.agent/last_block.md` on disk (not a digest fallback), so the extraction source and the committed original are the same bytes. Disk-to-disk equality is proved by G3 (whole file equals the slice), G4 (prefix preserved, remainder equals the three slices with their blank lines) and G8 (FROM 0x / TO 1x per pair). No marker LINE reached a target file: 0 `<<<SLICE` and 0 `<<<END` in `.agent/plan.md`, `packages/orchestration/exec_guard.py` and `tests/orchestration/test_exec_guard.py`. The `<<<` occurrences inside the RECORD-R7 and R0499 prose are mid-line prose and were preserved as such.

## Deviations & assumptions

1. The ordered sequence C0a, C0b, C1, C2, C3, C4, C5 was followed exactly — seven commits, none added, none dropped, no reordering.
2. `cp` and the `remedy` CLI are denied in this session. C0a and C0b both used `shutil.copyfile`, as change item 1 orders. G2 proves the byte property the gate names.
3. Commit Gate at C0a–C3: `.agent/plan.md` still described R7, because C4 is the bundle's sixth commit. That is R-0491, which this bundle carries unchanged.
4. `.agent/context.md` and `.agent/decisions.md` were NOT updated: constraint 3 limits the change set to the ordered paths.
5. The NEW-TEST slice is preceded by ONE blank line, as change item 5 orders, so `@pytest.mark.subprocess` sits one line below the previous test rather than the two of PEP 8. G10 is exit 0 under the repository's own ruff configuration, so the convention this repository enforces is met; the bytes were not adjusted (constraint 2).
6. Gate scratch (the twenty extracted slices, the pre-C1 blob, five gate scripts, this draft) and the G12 worktree were written under the gitignored `.remedy-wt/`; nothing entered the change set and `git status --porcelain` is clean.
7. `python3 -m py_compile` and a single-file `ruff check` were run on `exec_guard.py` inside the C2 self-review loop, before the ordered G10. They are self-review, not gate readings; G10 is reported above as its own run of the exact ordered command.
8. Stated-cause overage (DECISION D15): this file is 104 lines, over the 60-line base cap of docs/agents/handback_template.md and over its 100-line >5-commit cap, and over that template's 800-token thrift cap; no byte or token figure is stated here because such a figure would change the text that states it. Cause is mandated content only — seven per-commit tables for a seven-commit bundle, the item-status table covering C0a..C5, and a FIFTEEN-gate verification block of which G11 alone must carry ten exit codes and ten summary lines because the gate orders exactly that. No section was dropped, no transcript was padded.

## Next

- T002a is UNBLOCKED by this round and is R9's work: the builder class, five call sites, the first seam migration;
- `_StreamPump` still returns `b""` for a stream whose pump never reached EOF, so partial output is LOST on an incomplete drain — honest, because `streams_complete` says so, and lossy; the `snapshot()` refinement is named in the plan and is not claimed here;
- a stream still blocked at the grace deadline leaks one pipe read end and one daemon thread, which the guard docstring states as the deliberate tradeoff;
- `exec_guard.py` still has NO callers, so no containment claim holds for the running system;
- there is NO open PR for this branch and none is opened before closure;
- the R8 verdict is written by the NEXT round's record commit.
