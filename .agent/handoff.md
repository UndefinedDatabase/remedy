# Handback — F085 R6 (record-only round, NO fix)

Feature T2_F085 Sandbox hardening (stage 1) · Round R6 · Branch feature/f085-sandbox-hardening
Fortschritt: ~25 % (F085 beansprucht · Amendment F085 D1 angewandt · T001 gebaut, R5 FAIL — 3 Findings offen · T002/T003 offen) — Schätzung
Open findings: 112 registered, 0 resolved, 112 open. Max R-0497, next free R-0498.

## Range

Review of 16506c0b5410faa6d452da9cef482ee279d6cd0d..HEAD

## Commits

### bb22b2dd docs(f085): save the R6 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r6.md | +213 -0 | C0a — the reviewer's block, copied byte-for-byte |

### 4cc753b6 chore(agent): mirror the R6 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +106 -234 | C0b — the COMMITTED C0a blob, whole file |

### 07255ccd docs(review): record the R5 FAIL and register R-0495, R-0496, R-0497
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +8 -0 | C1 — RECORD-R5, R0495, R0496, R0497 appended in that order, verbatim |

### 93fcf6ff docs(f085): advance the plan to the R6 record round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +14 -17 | C2 — whole file := the PLAN slice |

### (this commit) docs(f085): rewrite the handback for R6
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | see note | C3 — a handback cannot table the commit that writes it (R-0149); under R-0494 its own numbers are ordered nowhere and the reviewer measures them at the next gate |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | this commit |

## External actions

`git push origin feature/f085-sandbox-hardening` after C2 → `16506c0b..93fcf6ff`, success, origin at 93fcf6ff. A second push follows C3. No PR created, no PR merged, no other `gh` command, no worktree added or removed.

## Verification

G1 `git status --porcelain` EMPTY immediately before C3 (only `.agent/handoff.md` in flight); `git worktree list` 1 line; `.agent/STOP` absent, re-read from disk before the first commit and again here.
G2 TRANSPORT `.remedy-wt/f085-r6.md`, committed `.agent/authored/f085-r6.md` and committed `.agent/last_block.md` all byte-EQUAL at sha256 fc4752a4ac333290e30d11145beaf519b9b6eb46d3b01099f95869fff5956d03, 22488 B, 213 lines.
G3 `.agent/plan.md` at HEAD byte-equals the PLAN slice; sha256 8b4398f8616dcdb71cf72d254e22c09937f87052350e22bd2721cb69ab1ef5ad, 38 lines, 2136 B; `## Goal` yes, `## Next Steps` yes, `F085` matched, under 50 lines.
G4 pre-C1 214867 B is a byte-exact PREFIX of post-C1 225757 B; appended tail 10890 B, 8 lines; RECORD-R5, R0495, R0496 and R0497 each occur exactly 1x in the WHOLE file and each 1x inside the tail; `git show --numstat 07255ccd -- .agent/live_review.md` = `8 0`, deletion column 0.
G5 regexes `^- R-\d+ — ` and `^Done: R-\d+ — `. Base 16506c0b: 109 registered, 0 resolved → 109 open. HEAD: 112 registered, 0 resolved → 112 open; 0 duplicate ids, 0 resolutions naming an unregistered id. Symmetric difference of HEAD-open against base-open plus R-0495, R-0496, R-0497: EMPTY. Newly open: exactly those three. Resolved by R6: NONE. Max R-0497, next free R-0498. LINE-START `^Landed: R-\d+` records at HEAD: 0.
G6 `.agent/live_review.md` still contains the substring `Steps`: yes, 19 occurrences.
G7 `git diff --name-only 16506c0b..HEAD` measured pre-C3 = `.agent/authored/f085-r6.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md` — the ordered set minus `.agent/handoff.md`, which is this commit. 0 paths under `packages/`, `tests/`, `docs/`, `apps/` or `scripts/`. The post-C3 reading is the R-0494 case: the reviewer measures it at the next gate.
G8 UNCHANGED CODE. `packages/orchestration/exec_guard.py` sha256 d9c77caec4ed9136868cef080bd2e2ae18c4216851507dc943d778d5c575114e, 12241 B, at 16506c0b AND at HEAD. `tests/orchestration/test_exec_guard.py` sha256 9301bc652ecf555b983e0cf85dc7c5da52071ef20de741b9cd3f1476188bad53, 6211 B, at 16506c0b AND at HEAD. Both pairs equal: constraint 4 held, nothing was repaired.
G9 RED — DOES NOT REPRODUCE AS ORDERED, and NOT repaired. `python3 -m pytest tests/orchestration/test_exec_guard.py -q` was run SEVEN times at HEAD from the repository root. Exit 1 on 3 runs, `1 failed, 5 passed in 4.58s`/`4.59s`; exit 0 on 4 runs, `6 passed in 4.55s`–`4.59s`. Ordered sequence: run1 exit 0, run2 exit 1, run3 exit 0, run4 exit 0, run5 exit 1, run6 exit 0, run7 exit 1. The gate passes only when the command FAILS, so it is satisfied on 3 of 7 runs and unsatisfied on 4 — it is a coin flip here, not the 5-of-5 red the reviewer measured. When it fails it fails EXACTLY as described: `test_cpu_limit_kills_a_busy_loop_and_names_the_limit`, `E AssertionError: assert 0.9997739999999999 >= 1.0`, the same value to six figures as the reviewer's 0.999776. Nothing was fixed, skipped or xfailed; G8 is the byte proof. This non-determinism is the substance of R-0496 rather than a contradiction of it: an assertion sitting ON the boundary is a coin flip, which is what R-0496 says.
G10 `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, `42 passed in 20.54s`. Canary green.
G11 insertions: C0a 213, C0b 106, C1 8, C2 14 — none over 500. C3's own count is ordered nowhere (R-0494).
G12 `git log --format=%p 16506c0b..HEAD` → one parent per commit, linear: bb22b2dd←16506c0b, 4cc753b6←bb22b2dd, 07255ccd←4cc753b6, 93fcf6ff←07255ccd. The reflog over THIS round is HEAD@{0}..HEAD@{3}, every entry `commit:`; HEAD@{4} and below are R5. No amend, rebase, reset, branch switch or force-push.

## Authored-text proofs

PLAN, RECORD-R5, R0495, R0496 and R0497 were extracted programmatically from `.remedy-wt/f085-r6.md`, which G2 proves byte-equal to the COMMITTED `.agent/authored/f085-r6.md`, by their one-line `<<<SLICE …>>>`/`<<<END …>>>` markers, and applied byte-verbatim; none was retyped. Disk-to-disk equality is proved by G3 (whole file equals the slice) and G4 (prefix preserved, each slice exactly once, inside the appended tail). No marker LINE reached a target file: 0 in `.agent/plan.md`, 0 in the appended tail of `.agent/live_review.md`. The single `<<<` occurrence in `.agent/live_review.md` is authored prose inside the pre-existing RECORD-R4 paragraph, not a transport marker.

## Deviations & assumptions

1. The ordered sequence C0a, C0b, C1, C2, C3 was followed exactly — five commits, none added, none dropped, no reordering.
2. DEVIATION, declared: G9 does not reproduce. The block states the reviewer measured `1 failed, 5 passed`, exit 1, five times out of five at 16506c0b; at this worker's hand the same command at HEAD is non-deterministic, 3 red and 4 green out of 7 runs. Constraint 7 was followed: the real command, exit codes and summary lines are recorded above and NOTHING that the gate measures was edited. Consequence for R7: `test_cpu_limit_kills_a_busy_loop_and_names_the_limit` is FLAKY, not reliably red, so a green run of this file proves nothing until R-0496 is fixed.
3. `cp` and the `remedy` CLI are denied in this session. C0a used `shutil.copyfile`; C0b wrote the bytes of the COMMITTED C0a blob read via `git show`. G2 proves the byte property the gate names.
4. Commit Gate at C0a and C0b: `.agent/plan.md` still described R5, because C2 is the bundle's fourth commit. That is R-0491, which this bundle carries unchanged.
5. `.agent/context.md` and `.agent/decisions.md` were NOT updated: constraint 3 limits the change set to the ordered paths.
6. No scratch file was written this round — every gate ran through a `python3` heredoc — so `.remedy-wt/` gained nothing beyond the reviewer's own block file. It is gitignored and `git status --porcelain` is EMPTY.
7. Stated-cause overage (DECISION D15): this file is 87 lines, over the 60-line base cap and under the 100-line >5-commit cap. Cause is mandated content only — five per-commit tables, the item-status table and the twelve-gate verification block, of which G9 needs its full transcript because it is the round's declared deviation. No section was dropped and no transcript was padded.

## Next

- R7 is a REPAIR round and fixes R-0495 and R-0496 in that order; R-0497 is a reviewer-side gate defect and is fixed by the reviewer's next block, not by a worker edit.
- `tests/orchestration/test_exec_guard.py` is RED at HEAD on `test_cpu_limit_kills_a_busy_loop_and_names_the_limit`, deliberately left red, and no round may claim this branch is green until R-0496 is resolved. G9 above records that it is in fact FLAKY rather than reliably red, which strengthens rather than weakens that rule.
- `exec_guard.py` still has NO callers, so no containment claim holds for the running system.
- There is NO open PR for this branch and none is opened before closure.
- The R6 verdict is written by the NEXT round's record commit.
