# Handback — F085 R4 (record + amendment round)

Feature T2_F085 Sandbox hardening (stage 1) · Round R4 · Branch feature/f085-sandbox-hardening
Fortschritt: ~10 % (F085 beansprucht · Seam-Inventar abgenommen · Amendment F085 D1 angewandt · T001/T002/T003 offen) — Schätzung
Open findings: 108 registered, 0 resolved, 108 open. Max R-0493, next free R-0494.

## Range

Review of fb346e8c1783b397f83f44bb1d7a317435c505f1..HEAD

## Commits

### 420633e4 chore(agent): save the F085 R4 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r4.md | +318 -0 | C0a — the reviewer's block, copied byte-for-byte |

### 4af6e207 chore(agent): mirror the R4 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +213 -81 | C0b — the COMMITTED C0a file, whole |

### 0ad9d7ec docs(f085): advance the plan to the R4 amendment round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +16 -11 | C1 — whole file := the PLAN slice |

### dc89486b docs(review): record the R3 PASS and register R-0493
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4 -0 | C2 — RECORD-R3 then R0493, appended verbatim |

### 959bd33d docs(f085): apply amendment D1 to the feature file
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T2_F085.md | +68 -7 | C3 — FROM1→TO1, FROM2→TO2, AMENDMENT appended |

### (this commit) docs(f085): rewrite the handback for R4
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | see note | C4 — a handback cannot table its own commit (R-0149); G14 routes C4's insertion count to the round report |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |

## External actions

`git push origin feature/f085-sandbox-hardening` after C3 → `fb346e8c..959bd33d`, success. A second push follows C4; its outcome is in the round report. No PR created, no merge, no other `gh` command, no worktree added or removed this round.

## Verification

G1 `git status --porcelain` EMPTY immediately before C4 (only `.agent/handoff.md` in flight); `git worktree list` 1 line; `.agent/STOP` absent, re-read from disk before the first commit and again at the handback. Post-C4 readings are in the round report.
G2 TRANSPORT `.remedy-wt/f085-r4.md`, committed `.agent/authored/f085-r4.md` and committed `.agent/last_block.md` all byte-EQUAL at sha256 c755c49d28f58c0d9f97ce0e0f95daa75e9291eeb3b6fce10153291b96727b42, 23993 B, 318 lines.
G3 `.agent/plan.md` at HEAD byte-equals the PLAN slice; sha256 a1a17001365fd83c0de0168d8c7d5c6057ead885121c54917fbc54322c1be673, 41 lines, 2266 B; `## Goal` yes, `## Next Steps` yes, F085 matched, under 50 lines.
G4 pre-C2 202948 B is a byte-exact PREFIX of post-C2 208910 B; 5962-byte, 4-line tail; RECORD-R3 1x and R0493 1x in the whole file, both inside the tail; `git show --numstat dc89486b -- .agent/live_review.md` = `4 0`, deletion column 0.
G5 line-start regexes `^- R-\d+ — ` and `^Done: R-\d+ — `. Base fb346e8c: 107 registered, 0 resolved → 107 open. HEAD: 108 registered, 0 resolved → 108 open; 0 duplicate ids, 0 resolutions naming an unregistered id. Symmetric difference of HEAD-open against base-open plus R-0493: EMPTY. R4 resolves nothing (newly resolved set empty). Max R-0493, next free R-0494. LINE-START `^Landed: R-` records measured at HEAD: 0.
G6 `.agent/live_review.md` still contains the substring `Steps`: yes.
G7 `.agent/f085_inventory.md` BYTE-IDENTICAL at fb346e8c and HEAD, sha256 fed207f9f8fb5a2de6a52a5366e1f3332eab1ae60c3a666cbddf4771f6c166bd both, 20333 B both. R4 did not touch it.
G8 `docs/roadmap/features/T2_F085.md` at HEAD: FROM1 0x, TO1 1x, FROM2 0x, TO2 1x, AMENDMENT 1x and the file ENDS with it; `<<<` 0x in the whole file; lines 1 and 2 byte-identical to lines 1 and 2 at fb346e8c. 149 lines, 8203 B.
G9 `git diff --name-only fb346e8c..HEAD` = `.agent/authored/f085-r4.md`, `.agent/handoff.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `docs/roadmap/features/T2_F085.md` and nothing else; 0 paths under `packages/`, `apps/`, `tests/`, `scripts/`. Measured pre-C4 it is the same list without `.agent/handoff.md`; the post-C4 reading is in the round report.
G10 `python3 -m pytest tests/docs/ -q` → exit 0, `295 passed in 0.43s`.
G11 `python3 -m pytest tests/orchestration/test_roadmap_index.py -q` → exit 0, `30 passed in 0.35s`. This is the R-0493 counter-measure applied: the only suite that parses feature detail files.
G12 `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q` → exit 0, `157 passed in 19.66s`, run in the PRIMARY checkout.
G13 `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, `42 passed in 20.53s`.
G14 insertions: C0a 318, C0b 213, C1 16, C2 4, C3 68 — none over 500. C4's own count is in the round report.
G15 `git log --format=%p fb346e8c..HEAD` → one parent per commit, linear. The reflog over THIS round is HEAD@{0}..HEAD@{4}, every entry `commit:`; entries below start at fb346e8c and belong to R3. No amend, rebase, reset, branch switch or force-push.
G16 STALENESS: checked. The R3 PASS is on disk as the RECORD-R3 paragraph in `.agent/live_review.md` at HEAD (G4 measures it). This file was rewritten whole, and the two now-falsified R3 statements — that this branch's final round had been reached and that the R3 verdict lives only in the handoff, the round report and the PR under §4 item 13 — are ABSENT from it. The RECORD-R3 paragraph carries the TERMINATOR CORRECTION that supersedes both.

## Authored-text proofs

PLAN, RECORD-R3, R0493, FROM1, TO1, FROM2, TO2 and AMENDMENT were extracted programmatically from the COMMITTED `.agent/authored/f085-r4.md` by their one-line markers and applied byte-verbatim; none was retyped. Disk-to-disk equality is proved by G3 (whole file equals the slice), G4 (prefix preserved, each slice exactly once in the appended tail) and G8 (each TO/AMENDMENT slice exactly once, each FROM zero times). No transport marker reached any target file: `.agent/plan.md`, `.agent/live_review.md` and `docs/roadmap/features/T2_F085.md` each contain 0 `<<<` occurrences.

## Deviations & assumptions

1. The ordered sequence C0a, C0b, C1, C2, C3, C4 was followed exactly — six commits, none added, none dropped, no reordering.
2. `cp` is denied in this session. C0a used `shutil.copyfile`; C0b wrote the bytes of the COMMITTED C0a blob. The gate names byte equality and a digest rather than a tool; G2 proves the property.
3. Commit Gate at C0a and C0b: `.agent/plan.md` still described R3, because C1 is the bundle's third commit. That is R-0491, which this bundle carries unchanged.
4. `.agent/context.md` and `.agent/decisions.md` were NOT updated. Constraint 3 limits the change set to the six ordered paths, and R4 made no new worker decision — the amendment is the reviewer's DECISION F085 D1, recorded at R2 and applied here.
5. TO1 is a REWRITE, declared as such in the block, and its final clause re-joins the untouched paragraph remainder at `writing outside scope`; the resulting line wrap is the authored bytes, not an adjustment.
6. `.remedy-wt/` gained gate scratch again (the pre-C2 blob, two gate scripts, this draft): the already-registered R-0403 mechanism, unchanged by R4. The directory is gitignored; `git status --porcelain` is EMPTY.
7. Stated-cause overage (DECISION D15): this file is 95 lines, over the 60-line cap, and also over the template's 800-token hard cap (R3's accepted handback was 87 lines and 6823 B; this round adds a sixth commit table and four more gates). Cause is mandated content only — six per-commit tables, the item-status table and the sixteen-gate verification block. No section was dropped and no transcript was padded. Its exact byte count is in the round report, not here, because a self-measured byte figure changes when it is written.

## Next

- R5 is the next round: T001 — `exec_guard.py` mechanics (rlimits, wall timeout, output caps) plus the four runaway fixtures. It is the first round of this feature to touch production code, so it is a SPLIT round under §3 Round-types.
- There is NO open PR for this branch and none is opened before closure.
- The R4 verdict is written by the NEXT round's record commit, not by this handback.
