# Handback — F085 R11 (T002a first half: opt-in env allowlist in the exec guard)

Feature T2_F085 Sandbox hardening (stage 1) · Round R11 · Branch feature/f085-sandbox-hardening
Fortschritt: ~40 % (F085 beansprucht · Amendment F085 D1 angewandt · T001 gebaut · R10 PASS · R-0500 erledigt, R-0501 offen · T002a Scrubbing-Hälfte gebaut, Migration offen · T002b-d offen · T003 offen) — Schätzung
Open findings: 116 registered, 2 resolved → 114 open, 0 `Landed:` records. Max R-0501, next free R-0502. This round writes NO finding: `.agent/live_review.md` is byte-unchanged (`git diff --name-only 2587780d..HEAD -- .agent/live_review.md` is empty).

## Range

Review of 2587780d9aa0d67d710e63193b3186ea3fc56a1d..HEAD

## Commits

### a1726eb7 docs(f085): save the R11 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r11.md | +400 -0 | C0a — the reviewer's block copied byte-for-byte with `shutil.copyfile`, digest verified before the commit |

### e4e2abb1 chore(f085): mirror the R11 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +358 -256 | C0b — the COMMITTED C0a blob (`git show HEAD:…`) copied whole |

### 8d496479 feat(f085): add an opt-in env allowlist to the exec guard
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/exec_guard.py | +45 -5 | C1 — GUARD1..GUARD7 in order: `FORBIDDEN_ENV_KEYS`, `scrub_child_env`, the `env_allowlist` field, `child_env` at the Popen site, three docstring pairs |
| tests/orchestration/test_exec_guard.py | +100 -1 | C1 — TEST1 (import), TEST2 (`_ENV_DUMP`, `_INTERPRETER_ADDED_ENV_KEYS`, `_dumped`), then NEWTESTS appended after exactly two blank lines |

### 6ab5c777 docs(f085): advance the plan to the R11 scrubbing round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +7 -9 | C2 — the PLAN pair over `## Current Step` and `## Next Steps`; `## Goal` and `## Risks` byte-identical to 2587780d |

### (this commit) docs(f085): rewrite the handback for R11
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | see note | C3 — a handback cannot table the commit that writes it (R-0149); its own numbers are ordered nowhere (R-0489/R-0494) and the reviewer measures them at the next gate |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | this commit |

## External actions

`git push -u origin feature/f085-sandbox-hardening` after C2 → `2587780d..6ab5c777`, success, upstream tracking set. A second push follows C3, then `gh pr list --state open --json number,headRefName,baseRefName,isDraft`; both are post-C3, so their outputs live in the round report (R-0494). No PR created, none merged. NO worktree was added, removed or pruned: the bundle orders none and none was needed.

## Verification

Every exit code below is the real `subprocess.returncode` of the gate's exact argv with `cwd=/home/decodeux/Repos/remedy`; this session's Bash tool rejects `$?`, loops and `$( )` by FORM, so no code was read with `echo $?`.
G1 `git status --porcelain` EMPTY (exit 0, no output) before C0a, C0b, C1 and C2, and EMPTY again before C3 with only `.agent/handoff.md` in flight; `git worktree list` → ONE line, `/home/decodeux/Repos/remedy  6ab5c777 [feature/f085-sandbox-hardening]`; `.agent/STOP` re-read from disk before the FIRST and again before the LAST commit — absent both times (`ls` exit 2, "No such file or directory").
G2 TRANSPORT: `.remedy-wt/f085-r11.md`, `git show HEAD:.agent/authored/f085-r11.md` and `git show HEAD:.agent/last_block.md` are all byte-EQUAL at sha256 0ac925d29a4c537683a695d732ed4d4af62e600ed7486d7d0d762514715a469b, 19176 B, 400 lines — one digest across all three, disk-to-disk, no fallback.
G3 `.agent/plan.md` at HEAD: sha256 699172bfed0791f5ab282384ef8f669c26249c6418ddc4fdd7a8c1688edd361a, 2446 B, 42 lines. `## Goal` yes, `## Next Steps` yes, feature-id regex matches `F085`, 42 < 50. `## Goal` byte-identical to 2587780d (729 B): True. `## Risks` byte-identical (472 B): True.
G4 PAIR SHAPES over the WHOLE target file at HEAD. REWRITES, FROM 0 / TO 1: PLAN 0/1, GUARD1 0/1, GUARD2 0/1, GUARD4 0/1, GUARD6 0/1, TEST1 0/1. APPENDS, FROM exactly 1 at HEAD and TO-contains-FROM True for all four: GUARD3 1/True, GUARD5 1/True, GUARD7 1/True, TEST2 1/True. Per-line count over C1's ADDED lines (`git show --format= --unified=0 8d496479 -- <path>`): every TO-ONLY line carrying content occurs exactly once — GUARD3 18/18, GUARD5 1/1, GUARD7 5/5, TEST2 16/16, zero content strays. The lines counted more than once are structural tokens only, reported not hidden: the empty line (6× in the exec_guard diff, 23× in the test diff) and the bare `"""` docstring closer (2× in the test diff), which repeat by construction and cannot be made unique — see the deviation note. NEWTESTS occurs exactly 1× in the test file and the file ENDS with it: True. READINGS, not assertions: C1 `45	5	packages/orchestration/exec_guard.py` + `100	1	tests/orchestration/test_exec_guard.py`; C2 `7	9	.agent/plan.md`.
G5 `git diff --name-only 2587780d HEAD` measured BEFORE C3 → exit 0: `.agent/authored/f085-r11.md`, `.agent/last_block.md`, `.agent/plan.md`, `packages/orchestration/exec_guard.py`, `tests/orchestration/test_exec_guard.py`. Equals the constraint-3 set minus `.agent/handoff.md`: True. Nothing under `docs/`, `apps/` or `scripts/`.
G6 IMPORT PATH, run from the repository root → exit 0: `/home/decodeux/Repos/remedy/packages/orchestration/exec_guard.py True`. The suite below measures THIS checkout and `scrub_child_env` exists on it.
G7 DETERMINISM: `python3 -m pytest tests/orchestration/test_exec_guard.py -q` TEN consecutive times at HEAD → exit codes [0,0,0,0,0,0,0,0,0,0]; summaries `12 passed in 7.79s / 7.70 / 7.76 / 7.78 / 7.76 / 7.79 / 7.78 / 7.74 / 7.80 / 7.72`. OBSERVED count 12 (7 at base + 5 new), not an expected one.
G8 SEPARATORS over the whole test file, compared not asserted. Base 2587780d: marker gaps [3,3,3,3,3,3,3], `def test_` gaps [1,1,1,1,1,1,1]. HEAD: marker gaps [3,3,3,3,3,3,3,3,3,3,3] (11 = 7 + 4 new marked tests, every one a 3), `def test_` gaps [1,1,1,1,1,1,1,1,1,1,1,3] — the trailing 3 is the unmarked `test_scrub_child_env_drops_a_key_the_source_never_defined`, whose two blank lines precede the `def` itself rather than a decorator; every other `def test_` still follows its decorator by one newline. No gap of 2 appears anywhere, so R-0500's one-blank-line shape did not recur.
G9 `python3 -m ruff check packages/orchestration/exec_guard.py tests/orchestration/test_exec_guard.py` under the repo's OWN configuration (not `--isolated`) → exit 0, `All checks passed!`. I ran the identical command at base 2587780d before touching either file: exit 0 there too, so this is unchanged, not newly green.
G10 `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, `42 passed in 20.50s`, matching the reviewer's `42 passed` at 2587780d. `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -q` → exit 0, `157 passed in 19.66s`, matching the reviewer's `157 passed`.
G11 NO CALLER — the gate's literal expectation is UNATTAINABLE and is reported as measured, not repaired. `grep -rln exec_guard packages apps scripts tests` → exit 0, four paths: `tests/orchestration/test_exec_guard.py` plus three gitignored `__pycache__/*.pyc` artifacts this session's own test runs produced. `packages/orchestration/exec_guard.py` does NOT appear because `grep -l` matches file CONTENT and the module's source contains no occurrence of the string `exec_guard` — true at 2587780d as well as at HEAD, so the gate's expected two-path set could not have been produced before this round either. The property the gate exists to prove HOLDS: intersecting the hits with `git ls-files`, the only TRACKED file naming `exec_guard` is the test file; no third tracked file exists, so no call site was migrated and constraint 3c is intact.
G12 INSERTIONS (the `+` column, `git show --numstat`): C0a 400, C0b 358, C1 145, C2 7. None exceeds 500. C3's own count is ordered nowhere (R-0489).
G13 HISTORY `git log --format=%h %p 2587780d..HEAD` → exit 0, ONE parent per commit, linear: a1726eb7←2587780d, e4e2abb1←a1726eb7, 8d496479←e4e2abb1, 6ab5c777←8d496479. `git reflog -n 12` → exit 0; HEAD@{0}..HEAD@{3} are this round's four commits, every entry prefixed `commit:`, and HEAD@{4} is 2587780d, the R10 handback. No amend, rebase, reset, branch switch or force-push.

## Authored-text proofs

All 21 slices were extracted from the COMMITTED `.agent/authored/f085-r11.md` by their one-line `<<<SLICE …>>>` / `<<<END …>>>` markers programmatically — never retyped, never by substring split. Each TO half was applied byte-verbatim after its FROM was verified to occur exactly once immediately before that replacement; the applier aborts rather than edit if a declared shape does not hold. G2 proves the extraction source byte-equal to the reviewer's `.remedy-wt/f085-r11.md` and to `.agent/last_block.md`, so this is a disk-to-disk proof, not a digest fallback. G3 and G4 prove the applications on disk at HEAD. No marker LINE reached a target file: `<<<SLICE` and `<<<END` occur 0 times in `.agent/plan.md`, `packages/orchestration/exec_guard.py` and `tests/orchestration/test_exec_guard.py` at HEAD.

## Deviations & assumptions

1. The ordered sequence C0a, C0b, C1, C2, C3 was followed exactly — five commits, none added, none dropped, no reordering, no commit outside it.
2. G11 is reported with its expectation unmet BY CONSTRUCTION, not repaired: the gate names a two-path set that `grep -l` cannot produce, because the module's own source never contains the string `exec_guard`, at base as much as at HEAD. Nothing was changed to make the gate green; the tracked-file reading that carries the gate's actual property is recorded above.
3. G4's "each TO-ONLY added line exactly once" is unattainable for blank lines and for the bare `"""` docstring closer, which repeat within one commit's added lines by construction. Every TO-ONLY line carrying content counts exactly once; the structural repeats are enumerated in G4 rather than filtered away silently. The prose was NOT altered to make the count come out (§4 item 9: the rule bends, never the text).
4. `cp` and the `remedy` CLI are denied in this session, so C0a and C0b used `shutil.copyfile`, which change item 1 explicitly permits; G2 proves the BYTE property the gate names rather than the tool. Gate scratch — the applier, five gate scripts, the committed-blob copy and this draft — lives under the gitignored `.remedy-wt/`; nothing there entered the change set and `git status --porcelain` was empty at every commit. One gate script initially passed the literal string `"C1"` where a SHA belonged and reported four false FAILs; the SCRIPT was fixed and re-run, no repository file was touched by that repair.
5. Commit Gate at C0a–C1: `.agent/plan.md` still described R10, because C2 is the bundle's fourth commit — the known R-0491 shape, which this bundle carries unchanged. `.agent/context.md` and `.agent/decisions.md` were deliberately NOT updated, as constraint 3 orders: scope and constraints are unchanged. No mutation or red-proof check ran, so no worktree was needed.
6. Stated-cause overage (DECISION D15): this file is 90 lines, over the 60-line base cap, and the bundle is five commits so the >5-commit allowance does not apply. Cause is mandated content only — five per-commit tables, the item-status table, and a THIRTEEN-gate verification block in which G4 carries per-line diff readings, G8 two list pairs and G11 a gate-defect explanation the reviewer would otherwise have to reconstruct. No section was dropped and no transcript was padded.

## Next

- FIRST, per Phase 1 rule 1 of docs/agents/self_drive_protocol.md, re-read `.agent/STOP` from disk: Phase 0 is one-shot while G6 binds at any point. It was absent when this round read it before its first and last commits, which says nothing about the next session;
- THEN the Open PR Gate (Phase 1 rule 2): the `gh pr list` output for this round is in the round report, post-C3 (R-0494); no PR was created and none merged;
- then T002a's MIGRATION half: the five builder sites of amendment F085 D1 move to `run_guarded` with a builder policy and behaviour-equality goldens. Until then `exec_guard.py` still has NO callers, so nothing in the running system is scrubbed and no containment claim follows from this round;
- an allowlist bounds what the PARENT hands over only: a CPython child still sets `LC_CTYPE` itself under PEP 538, which the module docstring now states and the tests subtract rather than credit to the guard;
- `_StreamPump` still returns `b""` for a stream whose pump never reached EOF, so partial output is LOST on an incomplete drain; `snapshot()` remains open in the plan;
- the R11 verdict is written by the NEXT round's record commit.
