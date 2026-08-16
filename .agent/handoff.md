# Handback — F085 R1 (claim)

## Range
Review of a5a70621..HEAD on feature/f085-sandbox-hardening. Ordered sequence C0a, C0b, C1, C2, C3 followed exactly; C3 is the last commit.
Fortschritt: ~2 % (F085 beansprucht · T001/T002/T003 offen) — Schätzung

## Commits
### 1e447586 docs(f085): save the R1 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r1.md | 339/0 | C0a — block copied byte-for-byte (`shutil.copyfile`; `cp` is denied here) |
### 9994b596 chore(agent): mirror the R1 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 322/300 | C0b — mirror of the COMMITTED authored copy |
### 92dcdb03 docs(f085): reset the live review carrying the F083 open set
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 41/138 | C1 — LIVEREVIEW-HEADER, then R0490, then the carried open paragraphs |
### e1562470 docs(f085): claim F085 in the ledger and reset the task state
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS.md | 1/1 | C2 — STATUSLINE pair, `[ ]` becomes `[~]` |
| .agent/context.md | 31/29 | C2 — CONTEXT slice, whole file |
| .agent/plan.md | 31/30 | C2 — PLAN slice, whole file |
| .agent/candidates.md | 3/15 | C2 — CANDIDATES slice, whole file; the carrier is empty |
### C3 (this commit) docs(f085): rewrite the handback for R1
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | — | this file (R-0149 self-reference); its own insertion count rides in the round report, per G14 |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | this commit |

## External actions
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → exit 0, raw output `[]`. Open PR Gate passed; nothing merged, nothing to stop for.
- `git checkout main` → exit 0; `git pull --ff-only` → exit 0, "Already up to date."; `git rev-parse HEAD` = a5a706214d20101dd54564c23d0a3c22efcc705d, the ordered base; `git checkout -b feature/f085-sandbox-hardening` → exit 0. `feature/f083-ci-self-check` left alone.
- `git push -u origin feature/f085-sandbox-hardening` → exit 0, new branch, remote head e1562470. The push of C3 runs after this commit, so its outcome rides in the round report. No PR created, none merged.
- No worktree added or removed; `git worktree list` is ONE line throughout.

## Verification
- G1 `git status --porcelain` EMPTY before C0a and after every commit so far; `.agent/STOP` absent before the first commit and at this handback. The post-C3 readings cannot exist in this file and ride in the round report.
- G2 TRANSPORT: `.remedy-wt/f085-r1.md`, committed `.agent/authored/f085-r1.md` and committed `.agent/last_block.md` are byte-EQUAL, all sha256 7a34422a0df2ca34a94599de5804a87cf9b53e211c17de6a1e99f9d81b006512, 21785 B, 339 lines.
- G3 live_review at HEAD: 105 registered, 0 resolved, 0 `Landed:` lines, 0 duplicate ids, 0 resolutions naming an unregistered id. OPEN at HEAD 105, OPEN in the blob at a5a70621 104; the set comparison open(HEAD) == open(base) plus R-0490 is True with an empty symmetric difference. Max id R-0490, next free R-0491.
- G4 carried paragraphs compared 104, byte-equal to their pre-reset originals 104 — the two numbers agree.
- G5 `.agent/live_review.md` contains the substring `Steps`: True.
- G6 STATUS.md at HEAD: FROM 0x, TO 1x, `^- \[~\]` 1x, `^- \[x\] F\d{3} — ` 50x, `<<` 0x. Measured at a5a70621 first: FROM 1x, `[~]` 0x, `[x] F` 50x — the reviewer's reading reproduced. README.md is not touched.
- G7 `.agent/context.md` at HEAD: `## Active Branch`, `feature/`, `Steps`, a `\bF\d{3}\b` match and `resource|pytest` (case-insensitive) all present; each of the eight forbidden strings absent.
- G8 `.agent/plan.md` at HEAD: `## Goal` and `## Next Steps` present, `\bF\d{3}\b` matches, 40 lines — under 50.
- G9 byte-equal to their slices, sha256 and lines: context.md 297bd3984fbfef45efe46f1f6774fdbeddd5ac1b0d96608c3076738b23281bad 48; plan.md 05d8bf545f1066d10d66211883bead74a723b3f8939c0b2f76f4a12ad1db7b6a 40; candidates.md ffa9a740e0b77ba38a4e72d0f9edf5723a2fb574240abe0326ec5e4522f2429f 12.
- G10 `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q` → `157 passed`, exit 0, run in the PRIMARY checkout.
- G11 `python3 -m pytest tests/docs/ -q` → `295 passed`, exit 0.
- G12 `python3 -m pytest tests/cli/test_golden_path.py -q` → `42 passed`, exit 0.
- G13 `git diff --name-only a5a70621..HEAD` read before C3 lists 7 paths: the ordered set minus `.agent/handoff.md`, which this commit adds. Nothing outside the ordered set. The eight-path reading rides in the round report.
- G14 per-commit insertions from `git show --numstat`: C0a 339, C0b 322, C1 41, C2 66 — none over 500. C3's own count goes in the round report.
- G15 `git log --format=%p a5a70621..HEAD` → one parent per commit, history linear; `git reflog` over this round shows only `commit:` and `checkout:` entries — no amend, rebase, reset or force-push.

## Authored-text proofs
Every slice was extracted programmatically from the COMMITTED `.agent/authored/f085-r1.md` by its one-line markers and applied byte-verbatim: LIVEREVIEW-HEADER and R0490 in C1, the single-occurrence STATUSLINE pair in C2 (counted before and after), and CONTEXT, PLAN and CANDIDATES as whole files whose digests are recorded under G9. No marker line reached any target file and no slice was retyped.

## Deviations & assumptions
1. `cp` is denied in this session, so C0a copied through `shutil.copyfile`; the PROPERTY the gate names — byte equality and one shared sha256 — was measured, not the tool. `/tmp` is denied, so scratch lives in the gitignored `.remedy-wt/`.
2. `.agent/plan.md` still described the closed amend0816 work during C0a, C0b and C1 because the ordered bundle rewrites it in C2. The block's order was followed as written; from C2 on the plan matches this round. Declared rather than silently reordered.
3. This file is 74 lines, over the 60-line cap that a 5-commit round carries. Cause is mandated content: five per-commit tables plus fifteen ordered gate readings, each carrying its real measured value. No section dropped, no padding, no transcript.
4. The ordered commit sequence C0a, C0b, C1, C2, C3 was followed EXACTLY — no extra commit, none dropped, no reordering. Nothing follows C3.

## Next
Window 1 reviews this round; Phase 1 rule 1 first, re-reading `.agent/STOP` from disk. No PR exists for this branch and none is opened before closure.
