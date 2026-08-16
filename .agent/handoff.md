# Handback — F085 R10 (record the R9 PASS, resolve R-0500, register R-0501)

Feature T2_F085 Sandbox hardening (stage 1) · Round R10 · Branch feature/f085-sandbox-hardening
Fortschritt: ~35 % (F085 beansprucht · Amendment F085 D1 angewandt · T001 gebaut · R9 PASS · R-0495, R-0496 und R-0500 erledigt · T002a Scrubbing-Hälfte für R11 vorbereitet und trocken geprüft · T002 offen · T003 offen) — Schätzung
Open findings: 116 registered, 2 resolved → 114 open, 0 `Landed:` records. Max R-0501, next free R-0502. R10 resolves R-0500 and registers R-0501; no code, no tests, no behaviour.

## Range

Review of 02043452794972c1f1b87cfe75fad7d3180eedcb..HEAD

## Commits

### e88fb800 docs(f085): save the R10 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r10.md | +298 -0 | C0a — the reviewer's block, copied byte-for-byte with `shutil.copyfile`, digest verified before the commit |

### 44869ecc docs(f085): mirror the R10 block into the last-block state file
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +238 -203 | C0b — the COMMITTED C0a file copied whole with `shutil.copyfile` |

### 960ba03a docs(review): record the R9 PASS, resolve R-0500 and register R-0501
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +89 -1 | C1 — DONE-R0500 REPLACES the file's last line LANDED-R0500 (that is the single deletion), then RECORD-R9 and then R0501 appended, each preceded by exactly one blank line |

### f1afe3b6 docs(f085): advance the plan to the R10 record round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +19 -14 | C2 — whole file := the PLAN slice |

### (this commit) docs(f085): rewrite the handback for R10
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

`git push -u origin feature/f085-sandbox-hardening` after C2 → `02043452..f1afe3b6`, success, origin at f1afe3b6, upstream tracking set. A second push follows C3, and `gh pr list --state open --json number,headRefName,baseRefName,isDraft` runs after that push exactly as the bundle orders; both are post-C3, so their outputs live in the round report and the reviewer measures them at the next gate (R-0494). No PR created, none merged. NO worktree was added, removed or pruned this round: the bundle orders none and none was needed.

## Verification

G1 `git status --porcelain` EMPTY before each of C0a, C0b, C1 and C2 (exit 0, output ``), and EMPTY again immediately before C3 with only `.agent/handoff.md` in flight; `git worktree list` exit 0, ONE line, `/home/decodeux/Repos/remedy  f1afe3b6 [feature/f085-sandbox-hardening]`; `.agent/STOP` re-read from disk before the FIRST commit and again before this LAST one — absent both times. The post-C3 status reading is the R-0494 case.
G2 TRANSPORT `.remedy-wt/f085-r10.md`, the committed `.agent/authored/f085-r10.md` and the committed `.agent/last_block.md` are all byte-EQUAL at sha256 9c88a94078a3b094875ba04efd9baebe34f3a4d430fef0a4d632521278262289, 19029 B, 298 lines — one digest across all three, computed over `git show HEAD:<path>` for the two committed files.
G3 `.agent/plan.md` at HEAD byte-equals the PLAN slice: True. sha256 13346b879a781bf38a9c20d97f3dd90a86c0cb5cc4cf6c65353ecdfadf0ca680, 2581 B, 44 lines. `## Goal` yes, `## Next Steps` yes, `\bF\d{3}\b` matches F085, F083, F085; 44 < 50.
G4 C1 SHAPE. The pre-C1 blob is 246209 B and ends with the LANDED-R0500 slice (occurring exactly once); with that final line stripped, the remaining 245960 B are a byte-exact PREFIX of the post-C1 file: True. The 6794 B remainder equals DONE-R0500 + one blank line + RECORD-R9 + one blank line + R0501, byte for byte: True. READING beside it, not an assertion: `git show --numstat --format= 960ba03a -- .agent/live_review.md` → exit 0, `89	1	.agent/live_review.md`. Over the WHOLE file at HEAD: LANDED-R0500 0 times, DONE-R0500 1, RECORD-R9 1, R0501 1.
G5 ARITHMETIC over `.agent/live_review.md`, regexes `^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-\d+`. Base 02043452: 115 registered, 1 resolved, 1 landed. HEAD: 116 registered, 2 resolved, 0 landed → 114 open. REGISTERED symmetric difference HEAD vs base = {R-0501}, base minus HEAD = {} (nothing lost). RESOLVED symmetric difference = {R-0500}. 0 duplicate ids; 0 resolutions naming an unregistered id. Max R-0501, next free R-0502. Every value matches the block's prediction.
G6 `.agent/live_review.md` still contains the substring `Steps`: yes, 27 occurrences at HEAD (reported, not asserted).
G7 `git diff --name-only 02043452..HEAD` → exit 0, measured BEFORE C3: `.agent/authored/f085-r10.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md` — equal to the constraint-3 set minus `.agent/handoff.md`: True. 0 paths outside `.agent/`, hence 0 under `packages/`, `tests/`, `docs/`, `apps/` or `scripts/`.
G8 UNCHANGED, the honesty gate. `packages/orchestration/exec_guard.py` sha256 at 02043452 and at HEAD are both 7dde71c84992af985b28c72d9b460280238721dae474938806f28f9b421b3b67 — EQUAL, matching the reviewer's measurement. `tests/orchestration/test_exec_guard.py` at both is e4576b64852660fbd627c85523f15479f813aeb17ab9e3a41c3e2be1ab5bcc0a — EQUAL. This round changes no code, so no containment claim follows.
G9 `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, `42 passed in 20.55s`. Canary green, matching the reviewer's `42 passed` at 02043452.
G10 `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -q` → exit 0, `157 passed in 19.73s`, matching the reviewer's `157 passed` at 02043452.
G11 INSERTIONS (the `+` column) from `git show --numstat`: C0a 298 (`298	0	.agent/authored/f085-r10.md`), C0b 238 (`238	203	.agent/last_block.md`), C1 89 (`89	1	.agent/live_review.md`), C2 19 (`19	14	.agent/plan.md`). None exceeds 500. C3's own count is ordered nowhere (R-0489/R-0494).
G12 HISTORY `git log --format=%h %p 02043452..HEAD` → exit 0, ONE parent per commit, linear: e88fb800←02043452, 44869ecc←e88fb800, 960ba03a←44869ecc, f1afe3b6←960ba03a. The reflog over THIS round is HEAD@{0}..HEAD@{3}, every entry `commit:` and matching those four subjects; HEAD@{4} is 02043452, the R9 handback. No amend, rebase, reset, branch switch or force-push.

## Authored-text proofs

All five slices — PLAN, LANDED-R0500, DONE-R0500, RECORD-R9 and R0501 — were extracted programmatically from `.remedy-wt/f085-r10.md` by their one-line `<<<SLICE …>>>` / `<<<END …>>>` markers, never by substring split and never retyped, and applied byte-verbatim. G2 proves that source file byte-equal to the COMMITTED `.agent/authored/f085-r10.md` and to `.agent/last_block.md` on disk, so the extraction source and the committed original are the same bytes — disk-to-disk, not a digest fallback. Disk-to-disk equality of the applications is proved by G3 (`.agent/plan.md` whole file equals the PLAN slice) and G4 (prefix preserved after the LANDED-R0500 line is stripped; the remainder equals DONE-R0500 + blank + RECORD-R9 + blank + R0501 byte for byte, and each of the three occurs exactly once in the whole file while LANDED-R0500 occurs zero times). No marker LINE reached a target file: 0 `<<<SLICE` and 0 `<<<END` occur in `.agent/plan.md` or in the appended region of `.agent/live_review.md`; the `<<<` inside the block's own prose is mid-line prose and was preserved as such in the C0a/C0b copies.

## Deviations & assumptions

1. The ordered sequence C0a, C0b, C1, C2, C3 was followed exactly — five commits, none added, none dropped, no reordering.
2. `cp` and the `remedy` CLI are denied in this session, so C0a and C0b both used `shutil.copyfile`, which change item 1 explicitly permits; G2 proves the BYTE property the gate names rather than the tool. Gate scratch (the five extracted slices, the pre-C1 blob, the two gate scripts and this draft) went under the gitignored `.remedy-wt/`; nothing there entered the change set and `git status --porcelain` was empty at every commit.
3. Commit Gate at C0a–C1: `.agent/plan.md` still described R9, because C2 is the bundle's fourth commit — that is R-0491, which this bundle carries unchanged. `.agent/context.md` and `.agent/decisions.md` were deliberately NOT updated, as constraint 3 orders: scope and constraints are unchanged.
4. This session's Bash tool rejects `$?`, shell loops and `$( )` by FORM, so no exit code above was read with `echo $?`. Every exit code is the real `subprocess.returncode` of the gate's exact argv, run with `cwd` at the repository root.
5. Stated-cause overage (DECISION D15): this file is 86 lines, over the 60-line base cap of docs/agents/handback_template.md, and this bundle is five commits, so the ≤100 >5-commit allowance does not apply and the overage is declared here instead. Cause is mandated content only — five per-commit tables, the item-status table covering C0a..C3, and a TWELVE-gate verification block in which G4, G5 and G12 each carry byte-level or set-level readings the gate orders explicitly. No section was dropped and no transcript was padded; no token figure is stated, because stating one would change the text that states it.

## Next

- FIRST, per Phase 1 rule 1 of docs/agents/self_drive_protocol.md, re-read `.agent/STOP` from disk: Phase 0 is one-shot while G6 binds at any point. It was absent when this round read it before its first and last commits, which says nothing about the next session;
- THEN the Open PR Gate (Phase 1 rule 2): there was NO open PR for this branch when this round pushed, and none is opened before closure;
- then R11 builds the first half of T002a — environment scrubbing behind an opt-in `env_allowlist` with a `FORBIDDEN_ENV_KEYS` floor — whose block is drafted and dry-run but NOT started here;
- `exec_guard.py` is UNCHANGED by this round and still has NO callers, so no containment claim holds for the running system;
- `_StreamPump` still returns `b""` for a stream whose pump never reached EOF, so partial output is LOST on an incomplete drain; the `snapshot()` refinement is named in the plan and is not claimed here;
- the R10 verdict is written by the NEXT round's record commit.
