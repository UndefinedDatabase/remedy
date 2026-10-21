## F141 — Permission matrix per autonomy level

### What changed
- **The matrix and its one check (T001).** `packages/orchestration/permission_matrix.py` holds the
  eight actions (`read`, `write_worktree`, `commit`, `push`, `dependency_change`, `destructive`,
  `expensive`, `external_call`), the thirty-two cells of `PERMISSION_MATRIX` over F078's levels
  `L2` to `L5`, and `require_permission` / `require_permissions`. A `deny` raises
  `PermissionRefusedError`; an `ask` without an approval of the instance answers `ask` naming the
  level that would allow it; every satisfied `ask` appends one line to
  `<data root>/autonomy/permission_grants.jsonl`; every answer cites its cell as
  `(action, level) = cell`. `autonomy.allow_push`, true by default and refused from the
  environment, turns every `push` cell into `deny`. A job pins its level at its first check.
- **The seams (T002).** `read` at `build_builder_context` (moved out of `run_pingpong`);
  `write_worktree`, `commit` and `push` at the apply's own refusals through
  `packages/orchestration/apply_permissions.py`, approved by the operator's flags; `remedy do run`'s
  push by `--push` or `apply.push_after_mission`; `dependency_change` and `destructive` at the apply,
  approved through a decision raised on the job; `expensive` at the cost prompt; `external_call` at
  every child process that keeps the network.
- **The page, the guards and the Orb (T003).** `docs/system/permission-matrix-v1.md` is rendered
  whole from the constants and a docs test fails on any drift; a guard reads every module's syntax
  tree for a bypass-shaped parameter and holds that each seam imports the matrix; `remedy status
  --json` answers `autonomy.push_allowed` and `autonomy.permissions` (contract 1.24);
  `tests/orchestration/test_permission_levels.py` drives the real seams at each level.
- **Structure.** `run_pingpong` fell from 1314 to 1274 lines and `pingpong_loop.py` from 5231 to
  5192, rows and pins lowered.

### Why
F078 gated who may START work; this gates what running work may DO, as one reviewable table with
no bypass flag and an audited approval per instance (`docs/roadmap/features/T7_F141.md`).

### Key decisions
DECISIONs F141 D1 to D8 in `.agent/decisions.md`. D1: the table and the reality it encodes
(`destructive` asks instead of denying at `L2`, so a branch merge keeps working; push asks at every
level, because Remedy does push on the operator's flag). D2: a job keeps the level of its first
context. D3: the apply's write, commit and push ask through the refusals they already have. D4: a
dependency change or a deletion asks through a decision on the job. D5: the cost prompt and a
networked child. D6: the rendered page, the two guards, and `permissions.py` staying a layer below.
D7: contract 1.24 and the fixture per level. D8: no ledger rotation in this closure (R-1376, owned
by F307). Operator question Q23 records the table, already executed with the session's
recommendation.

### How to review and test
Read `docs/roadmap/features/T7_F141.md` (Built State), `docs/system/permission-matrix-v1.md` and the
round entries in `.agent/live_review.md`. Every production change was red-proven by the reviewer,
by mutations in a disposable worktree or, for R-1402, by its guard's red run on the old bytes. The closure's one full suite: `python3 -m pytest -n auto -q` →
`22803 passed, 11 skipped` on `22bd1250c` (`.agent/authored/f141-closure-suite.txt`), 3.7 percent
less CPU time than F078's.

### Evidence
- Evidence job `f141r10e1001` (10825 passed, 0 failed); package
  `remedy-review-20261021-131628-READY_FOR_REVIEW.zip`, SHA-256
  `c8f302dbefe31863d6d3509858eb3d6fff2abe56c0648b3d78b03cd005611d26`, in
  `~/Repos/remedy-history/zips`; accepted head `23e8f8244bc15db7df28c0b1f28086c289a46fcb`.
- Self-use item SU-070, made from finding R-1401, ran to its approval gate through the `self_use`
  role's provider and was never applied; it changed no file, because R-1401 had already been
  repaired, which is registered as R-1403 for the findings paydown.

### Verdict and findings
Live review PASS_WITH_RISKS: the integrity check fails only on twelve High findings F141 does not
own (DECISION F310 D7). Resolved inside the feature: R-1395 to R-1402. Open: 88 findings by the
ledger's reader; F141 owns none (R-1403 is owned by F307).

### Runtime actuals
Two sessions on 2026-10-21: nine delegated rounds, then two; reviewer Claude Opus 5.5, workers
Claude Sonnet; tokens and cost of the sessions: not-measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
