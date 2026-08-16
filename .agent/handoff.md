# Handback — F085 R12 (record round: the R11 PASS, one resolution, two gate defects)

Feature T2_F085 Sandbox hardening (stage 1) · Round R12 · Branch feature/f085-sandbox-hardening
Fortschritt: ~40 % (F085 beansprucht · Amendment F085 D1 angewandt · T001 gebaut · R11 PASS · T002a Scrubbing-Hälfte gebaut und rot-kontrolliert · Migration der fünf Builder-Sites offen · T002b-d offen · T003 offen) — Schätzung
Open findings: 118 registered, 3 resolved, 0 `Landed:` → 115 open. Max R-0503, next free R-0504. The open count RISES by one this round (114 → 115), as the block declares: two registrations against one resolution.

## Range

Review of 0406ceba..HEAD

## Commits

### 1b104c9a docs(f085): save the R12 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r12.md | +264 -0 | C0a — the reviewer's `.remedy-wt/f085-r12.md` copied byte-for-byte with `shutil.copyfile`, digest verified before the commit |

### 4bbc4dbb docs(f085): mirror the R12 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +200 -336 | C0b — the COMMITTED C0a blob (`git show HEAD:.agent/authored/f085-r12.md`) copied whole |

### 17284ecb docs(review): record the R11 PASS, resolve R-0501, register two gate defects
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +123 -0 | C1 — pure APPEND of RECORD-R11, DONE-R0501, R-0502, R-0503 in that order, each preceded by exactly one blank line |

### b0d33e12 docs(f085): advance the plan to the R12 record round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +3 -4 | C2 — the PLAN pair over `## Current Step` only; `## Goal`, `## Next Steps` and `## Risks` byte-identical to 0406ceba |

### (this commit) docs(f085): rewrite the handback for R12
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | see note | C3 — a handback cannot table the commit that writes it (R-0149); its own numbers are ordered nowhere (R-0489) and the reviewer measures them at the next gate |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | this commit |

## External actions

`git push -u origin feature/f085-sandbox-hardening` after C2 → `0406ceba..b0d33e12`, success, upstream tracking set. A second push follows C3, then `gh pr list --state open --json number,headRefName,baseRefName,isDraft`; both are post-C3, so their outputs live in the round report (R-0494). No PR created, none merged. NO worktree was added, removed or pruned: this round orders no destructive check and needed none.

## Verification

Every exit code below is the real `subprocess.returncode` of the gate's exact argv with `cwd=/home/decodeux/Repos/remedy`; this session's Bash tool rejects `$?`, loops and `$( )` by FORM, so no code was read with `echo $?`.
G1 `git status --porcelain` EMPTY (exit 0, no output) before C0a, C0b, C1 and C2, and again before C3 with only `.agent/handoff.md` in flight; `.agent/STOP` re-read from disk before the FIRST and again before the LAST commit — absent both times (`ls` exit 2, "No such file or directory"); `git worktree list` → ONE line, `/home/decodeux/Repos/remedy  b0d33e12 [feature/f085-sandbox-hardening]`.
G2 TRANSPORT: `.remedy-wt/f085-r12.md`, `git show HEAD:.agent/authored/f085-r12.md` and `git show HEAD:.agent/last_block.md` are all byte-EQUAL at sha256 0f66ffe7b9a96bdb9bf8f9cb130a21d7ec2b8a8102f9f02cf85fa1ff74e78678, 18334 B, 264 lines — one digest across all three, disk-to-disk, no fallback.
G3 `.agent/plan.md` at HEAD: sha256 f7c2fae17240f364b5f4f0503be2d86a8f4e294cdbdb0ae6f34484f86bed9cf3, 2366 B, 41 lines. `## Goal` yes, `## Next Steps` yes, `\bF\d{3}\b` matches `F085`, 41 < 50. Byte-identical to their text at 0406ceba: `## Goal` True, `## Next Steps` True, `## Risks` True.
G4 C1 SHAPE: the pre-C1 blob (`git show 4bbc4dbb:.agent/live_review.md`, 252754 B) is a byte-exact PREFIX of the post-C1 file (`git show 17284ecb:…`, 262529 B) → True; HEAD equals post-C1 → True. The 9775-byte / 123-line remainder is byte-equal to one blank line + RECORD-R11 + blank + DONE-R0501 + blank + R0502 + blank + R0503 → True. Each of the four slices occurs exactly ONCE in the WHOLE file at HEAD: RECORD-R11 1, DONE-R0501 1, R0502 1, R0503 1. READING, not an assertion: `git show --numstat --format= 17284ecb -- .agent/live_review.md` → `123	0	.agent/live_review.md`; the deletion column is 0 because C1 only appends.
G5 ARITHMETIC over `.agent/live_review.md`, regexes `^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-\d+`. Base 0406ceba: 116 registered, 2 resolved, 0 landed — reproducing the reviewer's reading. HEAD: 118 registered, 3 resolved, 0 landed → 115 open. REGISTERED symmetric difference HEAD vs base `['R-0502', 'R-0503']`, base minus HEAD `[]`. RESOLVED symmetric difference `['R-0501']`. Duplicate registered ids 0, duplicate resolved ids 0, resolutions naming an unregistered id `[]`. Max R-0503, next free R-0504. Open 114 → 115, a rise of exactly one, as ordered.
G6 substring `Steps` in `.agent/live_review.md` at HEAD: count 28 (27 at base; RECORD-R11 names `## Next Steps` once). REPORTED, not asserted — the gate orders a count, not a value.
G7 `git diff --name-only 0406ceba..HEAD` measured BEFORE C3 → exit 0, four paths: `.agent/authored/f085-r12.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`. Equals the constraint-3 set minus `.agent/handoff.md`: True. 0 paths fall outside `.agent/` — nothing under `packages/`, `tests/`, `docs/`, `apps/` or `scripts/`.
G8 UNCHANGED, the honesty gate. `packages/orchestration/exec_guard.py`: base and HEAD both sha256 57867bb2e038666c5ec2c7cbba769a5b818ab31ae7648042384f73429bace269 → EQUAL. `tests/orchestration/test_exec_guard.py`: base and HEAD both sha256 c5061aa92a21b237f4520cd594435ab6dd9ee6ab4f1ab85e59968d6a192b2522 → EQUAL. This round changes no code, so NO containment claim follows from it; `exec_guard` still has no tracked caller.
G9 `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, `42 passed in 20.52s`, matching the reviewer's `42 passed` at 0406ceba. `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -q` → exit 0, `157 passed in 19.59s`, matching the reviewer's `157 passed`.
G10 INSERTIONS (the `+` column of `git show --numstat`): C0a 264, C0b 200, C1 123, C2 3. None exceeds 500. C3's own count is ordered nowhere (R-0489).
G11 HISTORY `git log --format=%h %p 0406ceba..HEAD` → exit 0, ONE parent per commit, linear: 1b104c9a←0406ceba, 4bbc4dbb←1b104c9a, 17284ecb←4bbc4dbb, b0d33e12←17284ecb. `git reflog -n 12` → exit 0; HEAD@{0}..HEAD@{3} are this round's four commits, every entry prefixed `commit:`, HEAD@{4} is 0406ceba the R11 handback. No amend, rebase, reset, branch switch or force-push.

## Authored-text proofs

All six slices — RECORD-R11, DONE-R0501, R0502, R0503, PLANF, PLANT — were extracted from the COMMITTED `.agent/authored/f085-r12.md` by their one-line `<<<SLICE …>>>` / `<<<END …>>>` markers programmatically, never retyped and never by substring split, and applied byte-verbatim. The PLAN applier verified PLANF occurred exactly once immediately before replacing it (1 → 0) and PLANT exactly once after (0 → 1). G2 proves the extraction source byte-equal to the reviewer's `.remedy-wt/f085-r12.md` and to `.agent/last_block.md`, so this is a disk-to-disk proof, not a digest fallback; G3 and G4 prove the applications on disk at HEAD. No marker LINE reached a target file: `<<<SLICE` and `<<<END` occur 0 times in `.agent/plan.md` and 0 times in the C1 remainder appended to `.agent/live_review.md`. No slice was corrected, reformatted or interpreted — the regex-looking text and backticks inside R0502 and R0503 landed as prose.

## Deviations & assumptions

1. The ordered sequence C0a, C0b, C1, C2, C3 was followed exactly — five commits, none added, none dropped, no reordering, no commit outside it.
2. `cp` and the `remedy` CLI are denied in this session, so C0a and C0b used `shutil.copyfile`, which change item 1 explicitly permits; G2 proves the BYTE property the gate names rather than the tool. Gate scratch — the slice files, the committed-blob copy, the pre/remainder blobs and this draft — lives under the gitignored `.remedy-wt/`; nothing there entered the change set and `git status --porcelain` was empty at every commit.
3. Commit Gate at C0a–C1: `.agent/plan.md` still described R11, because C2 is the bundle's fourth commit — the known R-0491 shape, which this bundle carries unchanged. `.agent/context.md` and `.agent/decisions.md` were deliberately NOT updated, as constraint 3 orders: scope is unchanged. No mutation or red-proof check ran, so no worktree was needed.
4. G6 is reported as a count and not asserted, exactly as the gate words it; the value moved 27 → 28 because RECORD-R11 quotes `## Next Steps`. That is a reading, not a failure.
5. Stated-cause overage (DECISION D15): this file is 85 lines, over the 60-line base cap, and the bundle is five commits so the >5-commit allowance does not apply. Cause is mandated content only — five per-commit tables, the item-status table, and an ELEVEN-gate verification block in which G4 carries the prefix/remainder proof, G5 the full symmetric-difference arithmetic and G8 four digests. No section was dropped and no transcript was padded.

## Next

- FIRST, per Phase 1 rule 1 of docs/agents/self_drive_protocol.md, re-read `.agent/STOP` from disk: Phase 0 is one-shot while G6 binds at any point. It was absent when this round read it before its first and last commits, which says nothing about the next session;
- THEN the Open PR Gate (Phase 1 rule 2): the `gh pr list` output for this round is in the round report, post-C3 (R-0494); no PR was created and none merged;
- then T002a's MIGRATION half: the five builder sites of amendment F085 D1 — `managed_builder_execution.py`:1160, `pingpong_provider.py`:952, 1075, 1208 and `stream_evidence.py`:595 — move to `run_guarded` with a builder policy and behaviour-equality goldens. Until then `exec_guard.py` has NO caller and nothing in the running system is scrubbed;
- R-0502 and R-0503 bind the REVIEWER, not the code: a no-caller gate names the import statement over tracked files, and an "exactly once among the added lines" gate over a source file excludes blank lines and bare docstring delimiters. Both counter-measures' promotion into docs/agents/planner_reviewer_prompt.md §3 stays routed to the paydown branch, which DECISION D2 calls overdue;
- the R12 verdict is written by the NEXT round's record commit.
