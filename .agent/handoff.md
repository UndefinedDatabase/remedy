# Handback — F085 R14 (record the R13 PASS, register R-0505 and R-0506) — HALTED BY `.agent/STOP`

Feature T2_F085 Sandbox hardening (stage 1) · Round R14 · Branch feature/f085-sandbox-hardening
Fortschritt: ~50 % (T001 gebaut · R13 PASS aktenkundig · T002a: erste von fünf Builder-Sites migriert · vier Sites, T002b-d, T003 offen) — Schätzung
Open findings: 121 registered, 3 resolved, 0 `Landed:` → 118 open. Max R-0506, next free R-0507. The open set rose by exactly two, as the block declares: two registrations, no resolution.
THE ROUND WAS HALTED. `.agent/STOP` did not exist when this worker read it before C0a; it appeared during the round and was first seen in `git status --porcelain` immediately after C1 committed. Per self-drive protocol G6 and block constraint 4 the bundle ended there: C2 was NOT started. See deviation 1.

## Range

Review of ee8e7ba1..HEAD

## Commits

### 028a5e40 docs(f085): save the R14 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r14.md | +214 -0 | C0a — the reviewer's `.remedy-wt/f085-r14.md` copied byte-for-byte with `shutil.copyfile`; digest verified against the dispatch before the copy |

### 5cbc4ee0 docs(f085): mirror the R14 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +150 -336 | C0b — the COMMITTED C0a blob (`git cat-file blob HEAD:.agent/authored/f085-r14.md`) written whole, never the scratch file |

### b12e8b9e docs(review): record the R13 PASS and register two measured findings
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +80 -0 | C1 — pure APPEND of RECORD1, then FIND1 (R-0505), then FIND2 (R-0506), each preceded by exactly one blank line |

### (this commit) docs(f085): rewrite the handback for R14
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | see note | C3 — a handback cannot table the commit that writes it (R-0149); G8 orders its own count nowhere |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | skipped | `.agent/STOP` appeared after C1. Protocol G6 ("finish the commit in flight, hand off and end") and block constraint 4 forbid starting it. `.agent/plan.md` is UNTOUCHED and still describes R13; the PLANF→PLANT pair is unapplied and owed to the next round |
| C3 | done | this commit — the handback the STOP path itself mandates |

## External actions

`git push -u origin feature/f085-sandbox-hardening` after C1 → `ee8e7ba1..b12e8b9e`, rc 0, upstream tracking set. A second push follows C3, then `gh pr list --state open --json number,headRefName,baseRefName,isDraft`; both are post-C3, so their outputs live in the round report (R-0494). No PR created, none merged. NO worktree was added, removed or pruned. `.agent/STOP` was NOT deleted, NOT modified and NOT committed.

## Verification

Every exit code is the real `subprocess.returncode` of the gate's exact argv with `cwd=/home/decodeux/Repos/remedy`; this session's Bash tool rejects `$?`, loops and `$( )` by FORM, so no code was read with `echo $?`.
G1 HYGIENE, PARTLY RED BY THE SENTINEL. `git status --porcelain` was EMPTY before C0a, C0b and C1 (rc 0, no output). Before C3 it is NOT empty: it prints exactly `?? .agent/STOP`. The sentinel is untracked, outside the five-path change set, and deleting it is forbidden, so an empty tree and a live STOP file cannot both hold — reported, not repaired. `.agent/STOP` re-read from disk before the FIRST commit: ABSENT. Re-read before the LAST: PRESENT, 0 bytes, mtime 2026-08-16 18:25:36. `git worktree list` → rc 0, ONE line, `/home/decodeux/Repos/remedy  b12e8b9e [feature/f085-sandbox-hardening]`.
G2 TRANSPORT, disk-to-disk, no digest fallback. `.remedy-wt/f085-r14.md`, `git cat-file blob HEAD:.agent/authored/f085-r14.md` and `.agent/last_block.md` are all byte-EQUAL at sha256 77447503b8bc9e86e2f8f905172874568777ae8d25b074c0d3662b912b10d32e, 15023 B, 214 lines — one digest across all three, matching the dispatched digest exactly.
G3 C1 SHAPE. The pre-C1 blob (266306 B) is a byte-exact PREFIX of the post-C1 file (273602 B) → True; the HEAD blob equals the file on disk → True; the 7296-byte remainder is byte-equal to blank + RECORD1 + blank + FIND1 + blank + FIND2 in that order → True; each slice occurs exactly 1× in the WHOLE file at HEAD (RECORD1 1, FIND1 1, FIND2 1). READING, not a prediction: `git show --numstat --format= b12e8b9e` → `80	0	.agent/live_review.md`; the deletion column is 0 because C1 only appends.
G4 ARITHMETIC over `.agent/live_review.md`, regexes `^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-\d+` (all `re.M`). Base ee8e7ba1: 119 / 3 / 0 → 116 open, reproducing the block's reading. HEAD: 121 / 3 / 0 → 118 open. REGISTERED symmetric difference `['R-0505', 'R-0506']`; RESOLUTION symmetric difference `[]`. Duplicate registered ids `[]`; resolutions naming an unregistered id `[]`. Max R-0506, next free R-0507. A rise of exactly two, as ordered.
G5 PLAN PAIR — RED, AND RED BY THE STOP, NOT BY A MISAPPLICATION. The block orders PLANF 0× and PLANT 1× at HEAD. MEASURED at HEAD: PLANF occurs 1×, PLANT 0×, because C2 was never started. `.agent/plan.md` is byte-IDENTICAL to base — sha256 8dae6b41813aff162aeb1c5a877ab667be909c723c30bbb4dc5b3fce42f65f6d, 2437 B, 42 lines (< 50) — so `## Goal` and `## Risks` are identical to base as ordered, but `## Current Step` and `## Next Steps` are ALSO identical, where the block requires them to differ. Nothing was edited to make this number come out. PLANF was verified to occur EXACTLY once in `.agent/plan.md`, so the pair is still cleanly applicable by the next round.
G6 THE HONESTY GATE. This round changed no code, and no containment claim follows from it. Byte-IDENTICAL between ee8e7ba1 and HEAD, each reported at both ends: `packages/orchestration/exec_guard.py` 57867bb2e038666c5ec2c7cbba769a5b818ab31ae7648042384f73429bace269; `packages/orchestration/managed_builder_execution.py` 023c9d72186eaa3357e814f82aa234e02b15911f1dcf970454da8933a0bcb685; `tests/orchestration/test_managed_builder_execution.py` 4c9367fb931f71dc5d69f4b436ae7d4057a2b56906c37d102e830692be4fc13f. All three True.
G7 STATE READERS `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -q` → rc 0, `157 passed in 19.69s` at base and rc 0, `157 passed in 19.62s` at HEAD. CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` → rc 0, `42 passed in 20.56s` at base and rc 0, `42 passed in 20.50s` at HEAD. Both match base.
G8 COMMIT HYGIENE, three readings. `git diff --name-only ee8e7ba1..HEAD` measured BEFORE C3 → rc 0, THREE paths: `.agent/authored/f085-r14.md`, `.agent/last_block.md`, `.agent/live_review.md`. The block orders the five declared paths minus `.agent/handoff.md`, i.e. four; the set is short by `.agent/plan.md` alone, which is C2 — the skipped commit, deviation 1. 0 paths OUTSIDE the declared five. INSERTIONS (`+` column of `git show --numstat`): C0a 214, C0b 150, C1 80 — none exceeds 500; C3's own count is ordered nowhere. `git log --format=%h %p ee8e7ba1..HEAD` → ONE parent per commit, linear ee8e7ba1 ← 028a5e40 ← 5cbc4ee0 ← b12e8b9e. `git reflog` → HEAD@{0}..HEAD@{2} are this round's three commits, every entry prefixed `commit:`, HEAD@{3} is ee8e7ba1 the R13 handback; no amend, rebase, reset, branch switch or force-push.

## Authored-text proofs

All five slices — RECORD1, FIND1, FIND2, PLANF, PLANT — were extracted by their one-line `<<<SLICE …>>>` / `<<<END …>>>` markers programmatically from the COMMITTED `.agent/last_block.md` (byte-equal to `.agent/authored/f085-r14.md` and to the reviewer's `.remedy-wt/f085-r14.md` by G2, so this is a disk-to-disk proof, not a digest fallback), cross-checked byte-for-byte against an independent extraction from the reviewer's own file, and never retyped, split by substring, reformatted or reworded. The three applied slices measure RECORD1 3773 B / 40 lines, FIND1 1712 B / 18 lines, FIND2 1808 B / 19 lines, none carrying trailing whitespace; their regex-looking text and backticks landed as prose. No marker LINE reached any target file: the C1 remainder contains 0 `<<<SLICE` and 0 `<<<END`. (`.agent/live_review.md` holds one of each, both PRE-EXISTING at base inside an earlier round's record prose, unchanged by this round.) PLANF and PLANT were extracted and verified — PLANF occurs exactly 1× in `.agent/plan.md` — but NOT applied, because C2 was cancelled by the STOP.

## Deviations & assumptions

1. THE ORDERED COMMIT SEQUENCE WAS NOT COMPLETED. The block orders C0a, C0b, C1, C2, C3. C0a, C0b and C1 ran in order; C2 (`.agent/plan.md`, the PLANF→PLANT rewrite) was SKIPPED and C3 follows C1 directly. Reason: `.agent/STOP` was absent when re-read before C0a and appeared mid-round — first observed in `git status --porcelain` immediately after C1 was committed, mtime 18:25:36. Block constraint 4 and protocol G6 both say: finish the commit in flight, write the handback, end. C1 was finished; C2 was therefore never started. C3 is not a violation of that halt — it IS the handback the halt mandates. AGENTS.md's ambiguity rule (preserve safety, prefer smaller changes) was applied to choose the halt over completing an in-scope bookkeeping commit. Nothing was reordered and no commit outside the block was made.
2. `.agent/plan.md` IS STALE and was deliberately left so. It still reads "R13, this round: record the R12 PASS…". AGENTS.md's If-Blocked rule asks that the plan carry the blocker; that would mean authoring plan text this worker is not the author of — the reviewer authors, the worker applies — so the blocker is recorded HERE instead, in the handback the protocol names as the only return channel. The unapplied PLANF→PLANT pair is owed to the next round and is still cleanly applicable.
3. G1 CANNOT BE FULLY GREEN AND WAS NOT MADE SO. `git status --porcelain` prints `?? .agent/STOP` before C3. The sentinel is untracked, sits outside the five-path change set, and must never be deleted (R-0347); committing it would widen the change set. It was left exactly as found and the red half of G1 is reported rather than repaired.
4. `cp` and the `remedy` CLI are denied in this session, so C0a used `shutil.copyfile` and C0b `git cat-file blob`, which constraint 1 explicitly permits; G2 proves the BYTE property the gate names — one sha256, length and line count across all three artifacts — rather than the tool. Gate scratch (slice extractors, the pre-C1 and remainder blobs, this draft) lives under the gitignored `.remedy-wt/`; nothing there entered the change set.
5. Commit Gate at C0a and C0b: `.agent/plan.md` still described R13, because C2 is the bundle's fourth commit — the known R-0491 shape. At C1 and C3 it is stale for the stronger reason in deviation 2.
6. TRANSIENT UNTRACKED FILES, observed and reported, not repaired. During the G7 base run `git status --porcelain` briefly showed `?? tests/regression/test_wrapper_pass_2434876_akuvb1_t.py` and `?? tests/regression/test_wrapper_slow_2434876__xwxdq14.py`. Both are fixtures the state-reader suite writes and removes; they were gone before the next commit and no commit was made while they existed. Named because a reviewer re-running G7 concurrently with a commit could see a non-empty tree that is nobody's mistake.
7. Stated-cause overage (DECISION D15): this file is 79 lines / 12978 B against the 60-line base cap, and over the template's 800-token thrift cap as every handback in this feature has been. Cause is mandated content only — four per-commit tables, the item-status table, an EIGHT-gate verification block in which G3 carries the prefix/remainder proof, G4 the full symmetric-difference arithmetic and G8 three readings, plus the STOP incident, which the template requires in External actions, Item status and Deviations alike. No section was dropped and no transcript was padded.

## Next

- FIRST, per Phase 1 rule 1 of docs/agents/self_drive_protocol.md, re-read `.agent/STOP` from disk. It EXISTS at this handback, 0 bytes, and this worker neither created nor removed it. Until the operator clears it, rule 1 ends the session before any other rule is reached;
- THEN, once it is cleared, the Open PR Gate (Phase 1 rule 2): the `gh pr list` output for this round is in the round report, post-C3 (R-0494); no PR was created and none merged;
- the OWED work, in this order: C2's PLANF→PLANT rewrite of `.agent/plan.md`, which is unapplied and still exactly applicable, and then the R15 migration round — T002a's four remaining builder sites (`pingpong_provider.py`:952, 1075, 1208 and `stream_evidence.py`:595) onto `run_guarded`, carrying R-0506's fix for the stale absence claims in `exec_guard.py` and `managed_builder_execution.py`;
- the R14 verdict is written by the NEXT round's record commit.
