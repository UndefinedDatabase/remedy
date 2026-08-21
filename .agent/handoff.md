# Handback — F255 R21 · CLOSURE (last round of this branch)

## Range

Review of a4f0fafd..HEAD (HEAD = C4, the commit carrying this file).

## Commits

### 779a8318 chore(state): save the F255 R21 step block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f255-r21.md | 308/0 | C0a — the R21 block, byte-equal to `.remedy-wt/f255-r21.md` |

### 027537d1 chore(state): mirror the F255 R21 step block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | 240/333 | C0b — same file mirrored (break-rewrite reading 308/401) |

### 2df7eab5 chore(plan): advance the plan to F255 R21 closure
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | 17/24 | C1 — PLAN255R21, first substantive commit (break-rewrite 36/43) |

### 32401303 docs(review): record the R20 verdict
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | 2/0 | C2 — RECORDR20 appended after exactly one blank line |

### 7d601c94 docs(roadmap): close F255 teacher role and sync the README
| Path | +/- | Reason |
|------|-----|--------|
| docs/roadmap/STATUS.md | 1/1 | C3 — the `[x]` F255 line |
| README.md | 6/2 | C3 — count 52→53, Tier 5 Done 0→1, Tier 5 accepted list |
| .agent/candidates.md | 10/4 | C3 — carrier emptied; ONE commit with the two above |

C4 writes this file; its own cell belongs to the round report (R-0149).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |

## External actions

- `git push -u origin feature/f255-teacher-role` after C3 → exit 0, a4f0fafd..7d601c94.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → exit 0, `[]`.
- `gh pr create --base main --head feature/f255-teacher-role --title 'F255 — Teacher role (Tier 5)' --body-file .remedy-wt/f255-pr-body.md` → exit 0, **PR #208**, https://github.com/UndefinedDatabase/remedy/pull/208
- `gh pr view 208 --json state,mergeable,isDraft,autoMergeRequest` → OPEN, MERGEABLE, isDraft false, autoMergeRequest null.
- PR #208 was **NOT merged** and auto-merge was **NOT enabled**. No CI run was waited on.
- `git push` again after C4 → see round report; no worktree added or removed.

## Verification

- G1 STOP absent before C0a; branch feature/f255-teacher-role; `git status --porcelain` empty after every commit and now; `git worktree list` = primary checkout alone.
- G2 `.remedy-wt/f255-r21.md`, `.agent/authored/f255-r21.md` (C0a) and `.agent/last_block.md` (C0b) all sha256 a7d4a09cf30f997a78ca12409831f2f00ebba4b9995567e63ce407be6398afbb, 23516 B, 308 lines — all three EQUAL.
- G3 11 slices extracted from the committed C0a file by marker lines, count taken from that listing; newline-INCLUDED digests: PLAN255R21 b46418e7 2046B/36L, RECORDR20 0cab00fb 4132B/1L, STATUSFROM 09dba254 83B, STATUSTO 2c0c835f 396B, COUNTFROM 93c8221e 64B, COUNTTO b4eace4e 68B, TIERFROM 06f358c5 34B, TIERTO 1cc9fdd3 34B, ACCEPTEDFROM 2413c959 92B/3L, ACCEPTEDTO 4246b906 244B/7L, CANDIDATES c335c96a 1118B/19L.
- G4 `.agent/plan.md` at C1 = b46418e77d4a98e779d80d0ca76391832998c228c992f4a9d0a4216e7bc54215, 2046 B, 36 lines (<50), byte-equal to PLAN255R21; `## Goal`, `## Next Steps` and F255/F008 all present; C1 is the first commit after C0a/C0b.
- G5 base blob is a byte-exact PREFIX of C2; remainder 9a73713d, 4133 B, 2 lines, == `\n`+RECORDR20, byte after the leading newline is `G`. Independent blank-line split: 216 units, LAST unit 0cab00fb (nl-incl) / 92081cee (no-nl) — both equal RECORDR20. Constraint 5 re-measured: 0 interior blank lines. Negative control (one byte mutated) REJECTED by both readings.
- G6 sets 187/4/183/0 at a4f0fafd and 187/4/183/0 at C2 (registered `^- R-\d+ — `, resolved `^Done: R-\d+ — `). `Gate: R21 — the R20 entry.` 0x at base, 1x at C2, LAST of the 21 line-anchored `Gate: R` headers, all 21 keys distinct.
- G7 each FROM 1x at a4f0fafd; at C3 STATUS/COUNT/TIER/ACCEPTED all read FROM 0x, TO 1x. All four are REWRITES (TO contains FROM: false, measured) so none owes an append reading. STATUS.md at C3: one `^- \[x\] F255 — `, zero `^- \[~\] F255`.
- G8 STATUS `^- \[x\] F\d{3} — ` = 53; README N = 53; EQUAL. README Tier 5 Done cell = 1, equal to the 1 accepted id with a `T5_` feature file (F255).
- G9 `python3 -m pytest tests/docs/ -q -rf` exit 0, 295 passed. `python3 -m pytest tests/orchestration/test_roadmap_index.py -q -rf` exit 0, 30 passed. The two pins re-run alone: exit 0, 2 passed.
- G10 `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf` exit 0, 160 passed. `python3 -m pytest tests/cli/test_golden_path.py -q -rf` exit 0, 42 passed. Run serially, never two pytest processes at once.
- G11 PR #208 created after the push, OPEN, not a draft, autoMergeRequest null; not merged, auto-merge not enabled.
- G12 `git diff --name-only a4f0fafd..7d601c94` = the Change list minus `.agent/handoff.md`, no path on either side alone. T5_F255.md, .agent/decisions.md, teacher_model.py, teach_cmd.py all PRESENT at base and ABSENT from the range. Every commit has one parent; insertions 308, 240, 17, 2, 17 — all under 500. C3 is ONE commit: `git show --numstat 7d601c94` names exactly STATUS.md, README.md, candidates.md. Reflog measured at 7d601c94 with 5 commits made at that moment: 5 entries whose operation prefix is exactly `commit` — the two are equal; 0 entries containing amend/rebase/cherry; 0 reset entries.
- G13 marker lines (`<<<SLICE `/`<<<END ` prefixes) = 0 in plan.md@C1, live_review.md@C2, STATUS.md/README.md/candidates.md@C3 and this file@C4. Branch pushed after C3 BEFORE the PR was created, and again after C4.

## Authored-text proofs

All eleven slices were extracted from the COMMITTED `.agent/authored/f255-r21.md` by their marker lines and applied byte for byte; nothing was retyped. `.agent/plan.md`@C1 and `.agent/candidates.md`@C3 are byte-equal to PLAN255R21 (b46418e7) and CANDIDATES (c335c96a). The C2 remainder equals `\n`+RECORDR20 exactly. Each of the four FROMs matched exactly once and was replaced exactly once.

## Deviations & assumptions

- No departure from the ordered sequence C0a, C0b, C1, C2, C3, PR, C4. No extra, dropped or reordered commit. No slice was edited.
- NEWLINE CONVENTION, stated not assumed: slice bodies were applied with the marker block's trailing newline STRIPPED. This is forced by the ACCEPTED pair — `ACCEPTEDFROM` ends mid-line at `Full per-feature state:`, which is followed in README.md by ` [\`docs/roadmap/STATUS.md\`](…)`, so newline-INCLUDED it matches 0x. Newline-EXCLUDED all four FROMs match exactly 1x. Not a deviation, but the convention a re-measurer needs.
- OBSERVATION, not a deviation (same as R20): C0b reads 240/333 under plain `git diff --numstat` and 308/401 under break-rewrite detection; C1 reads 17/24 and 36/43. Both readings are under the cap and both are stated.
- OBSERVATION: the review package contains `.remedy-wt/` scratch — already-registered R-0403, not a new condition of this closure.
- R21 IS THE LAST ROUND OF THIS BRANCH, so its own verdict has no on-disk gate entry BY CONSTRUCTION (planner_reviewer_prompt.md §4 item 13, the terminator). It lives in this handback and in PR #208, and is not a missing gate.

## Next

F255 is CLOSED: the STATUS `[x]` line landed at C3 (7d601c94) together with the README sync. R20 PASSED and its verdict is ON DISK at C2 (32401303). R-0607, R-0608, R-0609 and R-0611 remain OPEN — none a code defect — and route to a paydown branch.

The next session's FIRST action is Phase 1 rule 1, the `.agent/STOP` re-read. Its SECOND is the OPEN PR GATE, which merges PR #208 before any new branch is cut. Rule A5 then selects F008 — SSE event stream — the first `[ ]` in STATUS order.

Fortschritt: 100 % (T001 through T004 COMPLETE and REVIEWED · the integration gate PASSED with 0 branch-only failures · evidence job and READY_FOR_REVIEW package built and re-verified · STATUS `[x]`, README sync and the pull request landed at this round · F255 CLOSED, the PR merges at the next feature's Open PR Gate) — Schätzung
