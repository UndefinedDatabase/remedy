# Handback — F085 R9 (record the R8 PASS, register R-0500, fix it)

Feature T2_F085 Sandbox hardening (stage 1) · Round R9 · Branch feature/f085-sandbox-hardening
Fortschritt: ~35 % (F085 beansprucht · Amendment F085 D1 angewandt · T001 gebaut · R8 PASS · R-0495 und R-0496 erledigt · T002 entsperrt, offen · T003 offen) — Schätzung
Open findings: 115 registered, 1 resolved, 114 open. Max R-0500, next free R-0501. R9 registers R-0500 and resolves nothing — a `Landed:` line is not a resolution.

## Range

Review of b868401f6341946337f31c4eae593ef27133dbe7..HEAD

## Commits

### 831a2b0c docs(f085): save the R9 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r9.md | +263 -0 | C0a — the reviewer's block, copied byte-for-byte with `shutil.copyfile` |

### 611323a3 docs(f085): mirror the R9 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +124 -254 | C0b — the COMMITTED C0a file copied whole with `shutil.copyfile` |

### 5a0bb7e1 docs(review): record the R8 PASS and register R-0500
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4 -0 | C1 — RECORD-R8 then R0500 appended, each after exactly one blank line; pure append |

### 76f53036 test(f085): separate the new test by two blank lines
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_exec_guard.py | +1 -0 | C2 — the SEPARATOR pair, a rewrite; the R-0500 fix, one newline byte, no code |

### 4e1bf9c2 docs(review): note R-0500 landed in the R9 separator fix
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 -0 | C3 — the LANDED-R0500 line appended after exactly one blank line |

### 28af756c docs(f085): advance the plan to the R9 record round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +6 -6 | C4 — whole file := the PLAN slice |

### (this commit) docs(f085): rewrite the handback for R9
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

`git push origin feature/f085-sandbox-hardening` after C4 → `b868401f..28af756c`, success, origin at 28af756c. A second push follows C5. `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`, exit 0. No PR created, none merged. NO worktree was added, removed or pruned this round: the bundle orders none and none was needed.

## Verification

G1 `git status --porcelain` EMPTY immediately before C5 (only `.agent/handoff.md` in flight); `git worktree list` 1 line, `/home/decodeux/Repos/remedy 28af756c [feature/f085-sandbox-hardening]`; `.agent/STOP` absent, re-read from disk before the FIRST commit and again here. The post-C5 status reading is the R-0494 case and the reviewer measures it at the next gate.
G2 TRANSPORT `.remedy-wt/f085-r9.md`, committed `.agent/authored/f085-r9.md` and committed `.agent/last_block.md` all byte-EQUAL at sha256 e8011bbab7c5e3cd1817c1566e1112fde16ec47975b65e5cb05a358ff6d6f42d, 23297 B, 263 lines; one digest across all three.
G3 `.agent/plan.md` at HEAD byte-equals the PLAN slice; sha256 83b4a6777d941144520af17a34a3731a16ab650bbc962822f1f17d356971eedb, 2217 B, 39 lines; `## Goal` yes, `## Next Steps` yes, `\bF\d{3}\b` matches F083 and F085, 39 < 50.
G4 pre-C1 blob 238429 B is a byte-exact PREFIX of the post-C1 245959 B file, and the 7530 B remainder equals one newline + RECORD-R8 + one newline + R0500, byte for byte. pre-C3 blob 245959 B (identical to the post-C1 blob) is a byte-exact PREFIX of the post-C3 246209 B file, and the 250 B remainder equals one newline + LANDED-R0500. Each of the three slices occurs exactly once in the WHOLE file at HEAD. `git show --numstat` for `.agent/live_review.md`: C1 = `4 0`, C3 = `2 0` — both deletion columns 0.
G5 regexes `^- R-\d+ — ` and `^Done: R-\d+ — `. Base b868401f: 114 registered, 1 resolved. HEAD: 115 registered, 1 resolved → 114 open; 0 duplicate ids, 0 resolutions naming an unregistered id. REGISTERED symmetric difference HEAD vs base = {R-0500}; base minus HEAD = {} (nothing lost). RESOLVED symmetric difference = {} — UNCHANGED at exactly {R-0496}, because R9 resolves nothing. Max R-0500, next free R-0501. LINE-START `^Landed: R-\d+` records at HEAD: exactly 1, naming R-0500.
G6 `.agent/live_review.md` still contains the substring `Steps`: yes, 25 occurrences.
G7 `git diff --name-only b868401f..HEAD` measured pre-C5 = `.agent/authored/f085-r9.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `tests/orchestration/test_exec_guard.py` — the ordered set minus `.agent/handoff.md`, which is this commit and which the reviewer measures at the next gate. 0 paths under `packages/`, `docs/`, `apps/` or `scripts/`.
G8 UNCHANGED GUARD `packages/orchestration/exec_guard.py` sha256 at b868401f and at HEAD are both 7dde71c84992af985b28c72d9b460280238721dae474938806f28f9b421b3b67 — equal, so this round added nothing to the file R8 fixed.
G9 PAIR SHAPE, a rewrite, over the WHOLE of `tests/orchestration/test_exec_guard.py` at HEAD: SEPARATOR-FROM 0 times, SEPARATOR-TO exactly 1 time. FROM occurred exactly 1x before the edit, verified pre-C2. `git show --numstat 76f53036` = `1 0`. File size 8134 B at b868401f → 8135 B at HEAD, difference exactly ONE byte.
G10 SEPARATOR MEASUREMENT, `[len(m.group(0)) for m in re.finditer(r"\n+(?=@pytest\.mark\.subprocess)", text)]` over the whole file. At b868401f: `[3, 3, 3, 3, 3, 3, 2]` — the trailing 2 is the defect. At HEAD: `[3, 3, 3, 3, 3, 3, 3]` — every decorated test now has two blank lines before it. Reported as a comparison, not an assertion.
G11 DETERMINISM, ten consecutive runs of `python3 -m pytest tests/orchestration/test_exec_guard.py -q` from the repository root at HEAD: run1 exit 0 `7 passed in 7.68s`; run2 exit 0 `7 passed in 7.66s`; run3 exit 0 `7 passed in 7.65s`; run4 exit 0 `7 passed in 7.65s`; run5 exit 0 `7 passed in 7.64s`; run6 exit 0 `7 passed in 7.64s`; run7 exit 0 `7 passed in 7.63s`; run8 exit 0 `7 passed in 7.60s`; run9 exit 0 `7 passed in 7.62s`; run10 exit 0 `7 passed in 7.62s`. ALL TEN exit 0, ALL TEN `7 passed`; 10 green / 0 red.
G12 `python3 -m ruff check tests/orchestration/test_exec_guard.py` → exit 0, `All checks passed!`, repository configuration, no `--isolated` (R-0463). As R-0500 records, this command was ALSO exit 0 before the fix, so this green says nothing about the separator; G10 is what measures it.
G13 `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, `42 passed in 20.62s`. Canary green, matching the reviewer's `42 passed` at b868401f.
G14 PROBE, the eight-file structural sweep with `-rf`, run THREE times: run1 exit 0 `350 passed, 6 skipped in 15.32s`; run2 exit 0 `350 passed, 6 skipped in 15.33s`; run3 exit 0 `350 passed, 6 skipped in 15.39s`. No run was red, so no `-rf` FAILED node id exists to report and R-0499 gains no new observation.
G15 insertions (the `+` column): C0a 263, C0b 124, C1 4, C2 1, C3 2, C4 6 — none over 500. C5's own count is ordered nowhere (R-0494). `git log --format=%p b868401f..HEAD` → one parent per commit, linear: 831a2b0c←b868401f, 611323a3←831a2b0c, 5a0bb7e1←611323a3, 76f53036←5a0bb7e1, 4e1bf9c2←76f53036, 28af756c←4e1bf9c2. The reflog over THIS round is HEAD@{0}..HEAD@{5}, every entry `commit:`; HEAD@{6} and below are R8 and earlier. No amend, rebase, reset, branch switch or force-push.

## Authored-text proofs

All six slices — PLAN, RECORD-R8, R0500, LANDED-R0500 and the SEPARATOR-FROM/SEPARATOR-TO pair — were extracted programmatically from `.remedy-wt/f085-r9.md` by their one-line `<<<SLICE …>>>`/`<<<END …>>>` markers, never by substring split, and applied byte-verbatim; none was retyped. G2 proves that file byte-equal to the COMMITTED `.agent/authored/f085-r9.md` and to `.agent/last_block.md` on disk, not by digest fallback, so the extraction source and the committed original are the same bytes. Disk-to-disk equality is proved by G3 (whole file equals the slice), G4 (prefix preserved, remainder equals the appended slices with their blank lines) and G9 (FROM 0x / TO 1x). The extracted FROM is 175 B and the TO is 176 B — the one-newline difference the pair exists for, preserved because neither was stripped or retyped. No marker LINE reached a target file: 0 `<<<SLICE` and 0 `<<<END` in `.agent/plan.md` and `tests/orchestration/test_exec_guard.py`; the `<<<` inside the RECORD-R8 and R0500 prose is mid-line prose and was preserved as such.

## Deviations & assumptions

1. The ordered sequence C0a, C0b, C1, C2, C3, C4, C5 was followed exactly — seven commits, none added, none dropped, no reordering.
2. `cp` and the `remedy` CLI are denied in this session, so C0a and C0b both used `shutil.copyfile` as change item 1 orders and G2 proves the byte property the gate names; gate scratch (the six extracted slices, the pre-C1 and pre-C3 blobs, this draft) went under the gitignored `.remedy-wt/`, nothing entered the change set and `git status --porcelain` is clean.
3. Commit Gate at C0a–C3: `.agent/plan.md` still described R8, because C4 is the bundle's sixth commit — that is R-0491, which this bundle carries unchanged. `.agent/context.md` and `.agent/decisions.md` were NOT updated: constraint 3 limits the change set to the ordered paths.
4. This session's Bash tool rejects `$?` by FORM, so no gate's exit code could be read with `echo $?`. Every exit code above is the real `subprocess.returncode` of the gate's exact argv run with `cwd` at the repository root — the ordered command, a different reader. G12's transcript is that run, not a self-review run.
5. Stated-cause overage (DECISION D15): this file is 100 lines, over the 60-line base cap of docs/agents/handback_template.md and over that template's 800-token thrift cap, but at its 100-line >5-commit cap; no token figure is stated because such a figure would change the text that states it. Cause is mandated content only — seven per-commit tables for a seven-commit bundle, the item-status table covering C0a..C5, and a FIFTEEN-gate verification block of which G11 alone must carry ten exit codes and ten summary lines because the gate orders exactly that. No section was dropped, no transcript was padded.

## Next

- R10 starts T002a — the builder class, five call sites, the first seam migration — and needs its own block; nothing of it is started here;
- `exec_guard.py` is UNCHANGED by this round and still has NO callers, so no containment claim holds for the running system;
- `_StreamPump` still returns `b""` for a stream whose pump never reached EOF, so partial output is LOST on an incomplete drain; the `snapshot()` refinement is named in the plan and is not claimed here;
- there is NO open PR for this branch and none is opened before closure;
- the R9 verdict is written by the NEXT round's record commit.
