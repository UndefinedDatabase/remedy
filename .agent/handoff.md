# Handoff — F260 One world: mission → job → run, end of session 1

## Session

`SESSION 1 of feature F260 · rounds 1–4 delegated and reviewed · rounds so far 4`

Well inside the 25-round / 7-session soft limit, so no scope report is owed.

Context self-assessment: the reviewer's context was comfortable through four
rounds of authoring plus four independent re-verifications, and the session ends
with room to spare rather than exhausted — but the next round is a cross-module
production refactor (four minting call sites in `pingpong_job.py` and
`pingpong_loop.py`) whose pre-emission work needs a fresh reading of both
modules' import guards, which is the "round that explicitly needs a fresh
session" reason of docs/agents/self_drive_protocol.md G7 rather than a context
one.

## State block

`~25 % (T001 ✅ · Minting-Funktionen ✅ · Resolver + T002–T005 offen) — Schätzung`

Branch: `feature/f260-one-world`, cut from `main` at `b5cd6c20` (the merge commit
of pull request 240, F259). Branch tip and LAST REVIEWED commit: `fc36ab21`.
27 commits over four rounds. NO pull request exists for this branch yet — it is
opened in the closure sequence, not now.

Open findings: **295** (299 `^- R-\d{4} — ` registrations minus 4
`^Done: R-\d{4} — ` lines). Maximum id in use: **R-0814**, so the next id this
feature mints is R-0815.

## What this session did

The Open PR Gate merged F259's pull request 240 at merge commit `b5cd6c20` after
its CI run 33997545989 completed with conclusion `success`; `main` was pulled and
`gh pr list --state open` is empty. F259's round-10 closure round was reviewed
first — every gate re-run and reproduced — and its verdict is on the record as
the `Gate: R10` entry.

| Round | Range | Verdict | What it did |
|---|---|---|---|
| 1 | `b5cd6c20..4b704705` | FAIL (reviewer-caused) | Claimed the branch, re-headed the record, booked F259 R10. Stopped at gate G2, correctly: two defects in the reviewer's own block. Its four commits are byte-correct and were KEPT, not reverted. |
| 2 | `4b704705..bd42e0bc` | PASS | Repaired the one record byte, booked round 1's verdict and the two reviewer slips, claimed F260 in STATUS, and wrote `.agent/f260_inventory.md`. |
| 3 | `bd42e0bc..599b3df0` | PASS | Ruled DECISION F260 D1 and D2 from the inventory; registered R-0814. |
| 4 | `599b3df0..fc36ab21` | PASS | First production-code round: the three id-minting functions and their tests, with a mutation red-proof. |

## Changed files across the session

`git diff --numstat b5cd6c20..fc36ab21`:

| Path | +/- |
|---|---|
| .agent/authored/f260-r1.md | +457 / -0 |
| .agent/authored/f260-r2.md | +384 / -0 |
| .agent/authored/f260-r3.md | +345 / -0 |
| .agent/authored/f260-r4.md | +308 / -0 |
| .agent/context.md | +24 / -26 |
| .agent/f260_inventory.md | +239 / -0 |
| .agent/handoff.md | +220 / -241 |
| .agent/last_block.md | +296 / -288 |
| .agent/live_review.md | +28 / -18 |
| .agent/plan.md | +32 / -27 |
| .agent/prose_slips.md | +7 / -1 |
| docs/roadmap/STATUS.md | +1 / -1 |
| docs/roadmap/features/T2_F260.md | +134 / -8 |
| packages/orchestration/data_paths.py | +28 / -1 |
| tests/test_data_paths.py | +50 / -0 |

## THE ROUND 4 VERDICT — PASS, and it is owed to the record

This paragraph is the durable carrier operator amendment amend0827-process-diet
rule 1 provides for a verdict the reviewer's session cannot book itself. THE
FIRST COMMIT OF THE NEXT ROUND THAT IS HAPPENING ANYWAY MUST BOOK IT into
`.agent/live_review.md` as a `Gate: R4 — the F260 R4 entry.` paragraph, joining
the existing series; the round-5 block is expected to carry that slice.

VERDICT PASS on range `599b3df0..fc36ab21`, seven commits, all single-parent,
largest insertion count 308, well under the AGENTS.md 500-insertion cap. The
reviewer re-ran every gate itself rather than reading the handback for it.

- TRANSPORT: one digest
  `ab4c1b77b317bd7dc6a4bcb6ad45c68cb3eecb48ea5362a1803b0105c7d06ca0` across the
  scratch original, the saved copy and the mirror. Per §3 item 37 that is a COPY
  chain over three of the worker's own artefacts and is not a claim about bytes
  emitted into a prompt.
- THE RECORD: `.agent/live_review.md` 873291 → 877435 bytes, growth 4144 equal to
  the appended length exactly; the pre-image is a byte-exact PREFIX and the
  remainder is `"\n" + GATE_R3 + "\n"`; registrations stay 299 and `Done:` stays
  4, which is right because round 4 registered and resolved nothing; thirteen
  `Gate:` headers, all distinct.
- THE SHIPPED CODE WAS RUN, NOT READ. In a disposable worktree at `fc36ab21` the
  reviewer imported the three functions and called each 1000 times: returned
  lengths are exactly `{16}`, 1000/1000 values distinct per function, every
  character across all 3000 values is lowercase hex, every value matches
  `data_paths._SHORT_HEX_RE`, and `uuid.UUID(mint_job_id())` raises
  `ValueError: badly formed hexadecimal UUID string` — the probe D2 rests on.
  The three names are three DISTINCT function objects with distinct
  `__qualname__`s, so DECISION F260 D2's "one shape is not one function" clause
  is satisfied by the objects and not merely by the source. `resolve_job_id` and
  `resolve_any_job_id` both still import and are unchanged, which is what T004
  needs to still be true.
- NO INSTALL SHADOWS THE WORKTREE: the imported module resolved from
  `.remedy-wt/rev-r4/packages/orchestration/data_paths.py`, so the readings above
  and the red-proof below describe the branch's own bytes.
- THE MUTATION RED-PROOF REPRODUCES INDEPENDENTLY. In that worktree the
  unmutated control is exit 0 at 28 passed. Changing `[:16]` to `[:32]` inside
  the body of `mint_job_id` ONLY — verified by grep, the other two bodies
  untouched — gives exit 1 at 2 failed and 26 passed, at node ids
  `tests/test_data_paths.py::TestMintIds::test_each_mints_sixteen_lowercase_hex_chars`
  and `::TestMintIds::test_a_minted_job_id_is_not_a_uuid`. The second failure is
  the valuable one: widening to 32 hex makes the value a VALID UUID hex, so
  `UUID()` accepts it and the test that pins D2's premise fires. The worktree was
  discarded with `git worktree remove --force`, never reverted, and the primary
  checkout is `git status --porcelain` empty.
- THE SUITES, re-run by the reviewer serially, all exit 0:
  `tests/test_data_paths.py` 28 (23 before, plus exactly the 5 tests the new
  class adds), `tests/docs/` 303, `test_roadmap_index.py` 30, `tests/ui_server/`
  515, `test_test_runner.py` 52, `test_resource_safety.py` 21,
  `test_integrity_gate.py` 16, `tests/cli/test_golden_path.py` 42.
- THE CODE IS IDIOMATIC AND SCOPED: three separate `def`s between `control_dir`
  and `_SHORT_HEX_RE`, one D2 rationale comment above the group, a first-line
  docstring per function naming WHAT KIND of thing the id names, `uuid4` added to
  the existing `from uuid import UUID` line with `UUID` retained, and the module
  docstring's `Public API::` block extended. Nothing else in the file moved.
- The worker's deviation 2 is upheld and is a fair criticism of the block: gate
  G4 ordered the mutation into the body of `mint_job_id`, which forced three
  literal function bodies and foreclosed the shared private helper the block's
  own C4 text had permitted. The outcome is correct and D2's intent is met, but
  the gate constrained the implementation rather than measuring it, and a later
  block ordering a red-proof should name the PROPERTY to break, not the line.

## Verification at the branch tip

- `git status --porcelain` — empty.
- `git ls-files .remedy-wt` — empty; the scratch is untracked.
- `python3 -m apps.cli.grouped integrity check --json` — `"passed": true`,
  `"fail_count": 0`, 5 checks, handlers=342.
- `git worktree list` — the eleven `remedy/job-*` worktrees predate this session;
  no worktree this session created survives.

## Item status

| Item | Status | Reason |
|---|---|---|
| Open PR Gate — merge F259's PR 240 | done | merged at `b5cd6c20` after CI success; `main` pulled; no open PRs |
| Review F259 round 10 | done | PASS; booked as the `Gate: R10` entry |
| Claim F260 | done | STATUS `[~] F260`; `[x]` count unchanged at 73 |
| T001 the inventory | done | `.agent/f260_inventory.md`, 98 distinct citations, all resolving |
| T001 DECISION F260 D1 | done | one record, three areas; names R-0814's fix |
| T001 DECISION F260 D2 | done | 16-hex, one minting function per kind |
| T001 the minting functions | done | shipped, tested, red-proved |
| T001 the one resolver | NOT STARTED | needs T002's store; see Next |
| Book the round 4 verdict | owed | carried in this file; the next round's first commit books it |
| Open a pull request | not due | the closure sequence opens it, not this session |

## Next — the expected first actions of the next session

1. Read `.agent/STOP` from disk (Phase 1 rule 1), THEN run the Open PR Gate
   (rule 2). There is no open pull request, so the gate passes with nothing to
   merge and no branch is created — this session's branch is resumed.
2. Book the round 4 verdict above into `.agent/live_review.md` as
   `Gate: R4 — the F260 R4 entry.`, in the FIRST commit of round 5, which is a
   round happening anyway. A round whose whole change set is that booking is
   FORBIDDEN (amend0827 rule 1).
3. Round 5's work, already scoped by the reviewer at `fc36ab21`: move the four
   inline minting call sites onto the new functions —
   `pingpong_job.py:290` (`JobPlan.job_id`) → `mint_job_id`,
   `pingpong_loop.py:122` (`PingPongResult.run_id`) → `mint_run_id`, and
   `pingpong_job.py:2268` and `:2291` (`active_episode_id`) → `mint_episode_id`.
   Scope this precisely: many other `uuid4().hex[:16]` sites exist under
   `packages/orchestration/` and they name other kinds of thing (promotion,
   package, session, plan, quarantine), which DECISION F260 D2 does not reach.
   Before ordering it, read both modules for import guards and for an import
   cycle — `data_paths` imports nothing from either, so none is expected, but
   §3 items 7 and 34 require it to be read rather than assumed.
4. Then T002: the extended Mission record, the unified Job record under
   `jobs/<16hex>/` with its evidence beside it, and `runs/<run_id>/` keyed by run
   id. This is where finding R-0814 is fixed, because that layout is what removes
   the split storage root.

## Open risks carried forward

- DECISION F260 D1 changes what `<data_root>/runs/` is keyed by, from job id to
  run id. Every reader of the old shape must move in the same commit as its
  writer, or a run log is unreadable between two commits.
- The feature file's original "rename `task_jobs/` to `runs/`" order is NOT
  performed; DECISION F260 D0 records why, measured. Anyone reading the Goal &
  Done section alone will still find the retired sentence — D0 sits below it and
  supersedes it.
- The T005 prototype-cluster deletion is large and reversible in one direction
  only. It runs last, behind a reachability test that is green BEFORE the first
  `git rm`.
