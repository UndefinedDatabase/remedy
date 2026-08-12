# Handoff — F105 R49 (R-0269 fixed, then the integration gate)

Branch: feature/f105-cache-optimal-prompt-ordering. Base 9c80cf59.
Commits: abab5427 (C1), 381b51c9 (C2), 7623d625 (C3), a8b6f66e (C4),
4064a6ed (C5), HEAD (C6).
No production code under `packages/` or `apps/` and no test module was edited:
a gate that repairs what it measures is not a gate. No PR was created, nothing
was merged, `main` was not touched, no force-push.

## Changed files
| Path | Commit | +/- |
|---|---|---|
| .agent/authored/f105-r49-1.md | C1 abab5427 | +209/-0 (new file) |
| .agent/last_block.md | C2 381b51c9 | +181/-163 |
| .agent/live_review.md | C3 7623d625 | +69/-1 |
| docs/system/cache-optimal-prompt-ordering-v1.md | C4 a8b6f66e | +14/-0 |
| .agent/live_review.md | C4 a8b6f66e | +1/-0 (the `Landed:` line) |
| .agent/gate_f105_r49/ (9 files) | C5 4064a6ed | +268/-0 (new dir) |
| .agent/plan.md | C6 HEAD | full rewrite, 49 lines |
| .agent/handoff.md | C6 HEAD | full rewrite (this file) |

## Item status
| Item | Status | Reason |
|---|---|---|
| C1 | done | block written to .agent/authored/f105-r49-1.md, committed alone |
| C2 | done | same bytes copied to .agent/last_block.md, separate commit |
| C3 | done | PAIR_ID rewrite (R-0269 -> R-0270) + PAIR_LR contains-from |
| C4 | done | one paragraph in the note + exactly one `Landed:` line, one commit |
| C5 | done | integration gate ran in full; evidence in .agent/gate_f105_r49/ |
| C6 | done | plan.md (49 lines) + this handoff, then push, no PR |

## Integration gate — real numbers (`.agent/gate_f105_r49/`)
Merge base cfda4245b106aa17f2a7d846629dd1ab806766c7.

| Side | Command | Exit | Result | Wall |
|---|---|---|---|---|
| branch | `python3 -m pytest -n auto -q` | 0 | 16462 passed, 19 skipped, 0 failed | 99 s |
| base | `REMEDY_UI_NO_AUTO_BUILD=1 python3 -m pytest -n auto -q` | 1 | 16298 passed, 19 skipped, 7 failed | 144 s |

The branch collects 157 more tests than the base — F105's own T001-T004 tests.
Both wall clocks are under the ~5 min budget, so no perf note is raised.

**BRANCH-ONLY (`comm -13`): 0 ids. The file is empty.** No blocker can exist:
the branch suite has zero failures, so step 4 has nothing to attribute on the
branch side, and the flake class attributes 0 — far under the 10 the block set
as the flake-debt alarm.

**BASE-ONLY (`comm -23`): 7 ids, all attributed, none genuine.** All seven are
`tests/ui_server/test_live_state.py::TestUIServerIntegration::` —
`test_api_invalid_token_403`, `test_api_missing_job_404`,
`test_app_shell_served_without_token`, `test_brain_endpoint`,
`test_dashboard_no_raw_leaks`, `test_put_rejected`,
`test_server_starts_and_writes_info`. Every one: ENVIRONMENT, the known R-0221
mtime class — expected, not a discovery. Three kinds of direct evidence, per
id: (a) each fails with "Server did not start in time" and stderr "ERROR: React
UI not built."; (b) `_frontend_is_stale()` (ui_server.py:2748) compares mtimes,
and in the base worktree dist was 08:54:33 against newest src 08:55:15 — stale
by construction, because `cp -a` preserves dist's mtime while `git worktree
add` stamps src with checkout time; in the primary, dist 08:54:33 against
newest src 2026-06-29, never stale; (c) each of the seven PASSES on a serial
re-run at the merge base (0.17-0.28 s each) once R-0221's own test has rebuilt
dist there. F104 R7 saw six ids of this class; membership differs because xdist
scheduling decides which ids run before that mid-run rebuild — all the methods
involved exist at base (lines 178, 188, 290).

**Dist parity, verified by CONTENT not by the env var.** Aggregate sha256 of
every file under `apps/ui/dist`:
`fb68a7293502c79b8ece61d154f5752100a16da1a08a481a7a4c1d79a5a503c0` — the SAME
value in all four readings (base before, base after, primary before, primary
after). The parity claim holds and nothing wrote through into the primary.
`node_modules` and `dist` were COPIED, never symlinked, and both were verified
to be real directories.

## Gates — real exit codes
| Gate | Command | Exit | Result |
|---|---|---|---|
| A | sha256sum block/authored/last_block | 0 | all three `2a191709a351799e814c69fb3754d8206660e08cb26c36d922903859336efba4` |
| A | cmp block vs authored; cmp block vs last_block | 0, 0 | both silent |
| B | wc -l .agent/authored/f105-r49-1.md | 0 | 209 vs the D5 cap of 400 |
| C | PAIR_ID shape, MEASURED | 0 | FROM 1->0, TO 0->1 (rewrite) |
| C | PAIR_LR shape, MEASURED | 0 | FROM 1->1, TO 0->1 (contains-from) |
| C | each TO-only line 1x among C3's added lines | 0 | 69 lines, all exactly 1x |
| D | stray reconcile, C3 live_review.md | 0 | 69 added, 1 removed, 0 stray |
| E | grep -c '^<<<' over the four named files | 1 x4 | counts 0, 0, 0, 0 |
| F | python3 -m pytest tests/docs/ -q | 0 | 294 passed in 0.30s |
| G | integration gate, branch run | 0 | 16462 passed, 19 skipped, 99 s |
| G | integration gate, base run | 1 | 7 failed, 16298 passed, 144 s, all 7 attributed |
| H | canary, pytest tests/cli/test_golden_path.py -q | 0 | 42 passed in 19.51s |
| I | git worktree list / git branch --list 'tmp/\*' | 0 | primary ALONE; tmp branch list EMPTY |
| I | git status --porcelain | 0 | empty |
| J | insertions per commit | 0 | 209, 181, 69, 15, 268 — all < 500 |
| J | git diff --name-only 9c80cf59..HEAD | 0 | exactly the 15 paths named by the block |

Gate E note: `grep -c` exits 1 when the pattern is absent, and absence IS the
pass condition; the recorded numbers are the counts, all zero. Gate E was run
only over `live_review.md`, `plan.md`, `handoff.md` and the note, as the block
scoped it — the captured pytest output in the gate dir may legitimately contain
such a sequence. Gate G's base exit code of 1 is the REAL exit code and is not
a red gate: seven attributed environment failures at the merge base are what
step 3 of the procedure exists to handle.

## Transport proof
`.remedy-wt/f105-r49-1.block.md`, `.agent/authored/f105-r49-1.md` and
`.agent/last_block.md` all three hash to
`2a191709a351799e814c69fb3754d8206660e08cb26c36d922903859336efba4`, 209 lines,
13469 bytes, no trailing whitespace, no tabs, no CR. Both `cmp` runs silent,
exit 0. The PAIR bodies were SLICED from the COMMITTED authored file by
`.remedy-wt/r49_apply.py`, which refuses any marker not present exactly once,
asserts TO startswith FROM for the declared CONTAINS-FROM shape, and refuses to
write unless the pre- and post-counts match the declared shapes. Nothing was
retyped. All scratch lives in the gitignored `.remedy-wt/`; the full run logs
(244 and 685 lines) were written there WHILE each suite ran and only trimmed
tails were copied into the evidence dir afterwards (R-0176).

## Base worktree
Created as `git worktree add -b tmp/base-gate .remedy-wt/base-gate cfda4245...`
— on a throwaway BRANCH, never detached (DECISION D3). Removed with `--force`
(it carried the copied untracked node_modules and dist), pruned, and the branch
deleted; all three exit 0. `git worktree list` now shows the primary alone and
`git branch --list 'tmp/*'` prints nothing. Proof in `worktree_cleanup.txt`.

## Open findings: 8
R-0221, R-0239, R-0247, R-0262, R-0265, R-0266, R-0268 carried, plus R-0269
registered this round by C3. R-0269 is the only one with a fix LANDED (C4);
it stays OPEN until the reviewer authors its `Done:` text. No `Done:` paragraph
was written by this worker. Next free ID: R-0270.

## PR #189 — untouched, stop-and-report
`docs/amend0810-clerical` -> `main`, open, NOT from a `feature/*` branch, so the
AGENTS.md Open PR Gate makes it stop-and-report rather than merge. This round
did not merge, comment on, or modify it. The operator must resolve it BEFORE
F105's closure PR is cut.

## Next expected action
Reviewer gates R49 over `9c80cf59..HEAD` and issues the INTEGRATION GATE
verdict — step 5 of the procedure reserves that verdict for the reviewer, so
this handoff records what was measured and claims no verdict. Then closure per
`docs/roadmap/STATUS_closure_protocol.md`, with PR #189 resolved first.

Deviations, declared: ONE, and it is a naming limit rather than a scope change.
C4's mandated `Landed:` line must name "which commit", but it is committed
TOGETHER with the doc change, so the SHA cannot exist when the line is written.
Rather than add a second commit or leave a placeholder, the line names "this
round C4 commit"; C4 is a8b6f66e per the table above. Nothing else deviates:
the diff touches exactly the paths the block named, and no gate outcome changes.

Deviations, declared (DECISION D15): this handoff is 154 lines against the
60-line cap. The cause is mandated content only — the 16-row gate table with
its real exit codes, the changed-files table, the item-status table, the
transport proof, and above all the block's explicit requirement that this file
carry the integration gate's real numbers: branch and base pass/fail counts,
the branch-only list, the base-only list, the attribution of EVERY differing id,
both wall clocks and the dist-hash parity proof. No section was dropped and no
prose was added to reach that length.
