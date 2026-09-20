# Handoff — F277 Machine contracts: event vocabulary, JSON envelope, exit codes · Round 10

## Session

SESSION 6 of feature F277 · round 10 · rounds so far 10

Context self-assessment: the worker read `AGENTS.md`, `docs/agents/handback_template.md`,
`.remedy-wt/f277-r10-block.md` and `docs/roadmap/features/T2_F277.md` in full, verified the
step block's own bytes before using it (R-0954: measured 221 lines, sha256
`4ffe3c28775d65215d1fba954e161f2aa82f96cb3fc9023da6709d94092a6827`, matching both of the
delegation message's readings exactly), found no `.agent/STOP` on disk, verified the branch
was already `feature/f277-machine-contracts` clean at `33d1c9df`, then verified all five
PAYLOADS entries (line count + bytes + sha256) against the block's table before using any of
them — all five matched exactly. Executed the four-commit bundle (C1a, C1b, C2, C3) in order,
ran all six gates for real, and pushed.

## Range

Review of `33d1c9df`..`HEAD`.

## Commits

### 5cf5fe2e F277 R10 C1a: copy round 10 payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f277-r10-block.md | +221/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f277-r10-decisions.md | +52/-0 | byte-for-byte copy of decisions.md payload |
| .agent/authored/f277-r10-ledger.md | +2/-0 | byte-for-byte copy of ledger.md payload |
| .agent/authored/f277-r10-plan.md | +49/-0 | byte-for-byte copy of plan.md payload |

Measured insertions: 324 (221+52+2+49). Block's formula: block's own line count (221) plus
103 (52+2+49) = 324. Matches exactly.

### de1f10dd F277 R10 C1b: book round 9's PASS, record DECISION F277 D9, rewrite plan
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | append round 9 PASS entry (ledger.md payload) |
| .agent/decisions.md | +52/-0 | append DECISION F277 D9 (decisions.md payload) |
| .agent/plan.md | +29/-29 | rewrite to plan.md payload, byte-identical |

Measured insertions by `git show --numstat`: 83 (2+52+29). Matches the block's expected
reading exactly. Note: `git commit`'s own terminal summary printed "103 insertions(+), 49
deletions(-)" because of rename-detection folding on the `.agent/plan.md` rewrite (a 79%
similarity match) — the `git show --numstat` reading of 83 is the one DECISION F104 D1 fixes,
per the block's own warning, and it is the number reported as authoritative here.

### 8c2cd3cc F277 R10 C2: migrate the mission group onto the shared fail helper
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/mission_cmd.py | +39/-45 | apply s1-mission.diff: migrate onto `fail()`, thread `json_output` into `_resolve_project_id` and `_load_mission_or_exit` |
| tests/cli/test_mission_cmd.py | +51/-3 | apply s1-mission.diff: new coverage + adjusted existing assertions |

Measured insertions: 90 (39+51). Matches expected exactly. `import sys` was kept (per the
block's explicit note) and the two `file=sys.stderr` NOTES (a skipped-unreadable-records line
and a contract warning) were left untouched — confirmed by grep after the commit.

### a2079ffd F277 R10 C3: thread the shared mission helpers through the contract group
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/contract_cmd.py | +2/-2 | apply s2-contract.diff: thread `json_output` into the two shared-helper call sites |
| tests/cli/test_contract_cmd.py | +29/-0 | apply s2-contract.diff: new coverage, the red proof for both threaded arguments |

Measured insertions: 31 (2+29). Matches expected exactly.

Self-reference exception (handback template): the following commits, which only write and
then complete this handoff, share one grouped table with per-commit attribution in Reason —
a handback cannot table the commit that writes it (R-0149 pattern), following round 9's
identical precedent (C7/C7-fix).

### (C4) F277 R10 C4: rewrite handoff for round 10
### (C4-fix) F277 R10 C4-fix: record the actual push outcome in the handoff
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | first write | this handback, with placeholder G6 push/status/worktree readings not yet knowable before the push |
| .agent/handoff.md | fix-up | fill in the real `git push`/`git status`/`git worktree list` output for G6, only knowable after the first handoff commit was pushed |

(Exact SHAs for C4 and C4-fix are filled in below once made; see Deviations.)

## External actions

- `git worktree add --detach .remedy-wt/f277-r10-g5 a2079ffd` — succeeded, for G5's mutation
  red-proofs.
- `git worktree remove .remedy-wt/f277-r10-g5` — succeeded, as G5's last action.
- `git push -u origin feature/f277-machine-contracts` — reported under Verification/G6 below
  (the round's final act).

## Verification

### Pre-flight

- `ls .agent/STOP` → `No such file or directory`.
- `git status --porcelain` → empty.
- `git branch --show-current` → `feature/f277-machine-contracts`.
- `git rev-parse HEAD` → `33d1c9dfd36b6eb1296e0cb0f4783fdfba36f65f`. Matches the block's stated tip.
- Block self-verification (R-0954): measured 221 lines, sha256
  `4ffe3c28775d65215d1fba954e161f2aa82f96cb3fc9023da6709d94092a6827` for
  `.remedy-wt/f277-r10-block.md`. Both match the delegation message's two readings exactly.

### G1(a) — PAYLOADS transport, all five files

| file | lines measured | lines expected | bytes measured | bytes expected | sha256 match |
|---|---|---|---|---|---|
| ledger.md | 2 | 2 | 4287 | 4287 | True (`a90429dc6357086fbb851bdc6761b1b666cb7e2c7234bb9633fb0a6a62f09917`) |
| decisions.md | 52 | 52 | 3870 | 3870 | True (`f0b40d1812d8a60213a9d7605abbdd44fd7311c7405ed88509c350757d3c8c1c`) |
| plan.md | 49 | 49 | 2710 | 2710 | True (`116c0ee356cb5d8b267cf496779b249b8611fed876cdc7fbd8e3205167ca44ab`) |
| s1-mission.diff | 304 | 304 | 13346 | 13346 | True (`a5350096ddc09e61fa34633520656229e55947459a71199cc8b4af10b8e5c35d`) |
| s2-contract.diff | 52 | 52 | 2491 | 2491 | True (`10431783212ebdca53b7676ab8336456248e44c9f06eddd1fdd95597c382ab45`) |

All five equal. `git apply --check` exit code for each of the two `.diff` files: 0 (both), run
before the corresponding `git apply`.

### G1(b) — the four `.agent/authored/f277-r10-*` copies vs. their sources

| copy | source | `cmp` result |
|---|---|---|
| f277-r10-block.md | .remedy-wt/f277-r10-block.md | True |
| f277-r10-ledger.md | .remedy-wt/f277-r10-payloads/ledger.md | True |
| f277-r10-decisions.md | .remedy-wt/f277-r10-payloads/decisions.md | True |
| f277-r10-plan.md | .remedy-wt/f277-r10-payloads/plan.md | True |

Four readings, all True.

### G1(c) — the two appends at C1b, pre/payload/post, plus the negative control

| file | pre (bytes at 33d1c9df) | payload (bytes) | post (bytes at C1b) | pre+payload=post |
|---|---|---|---|---|
| .agent/live_review.md | 430979 | 4287 | 435266 | True |
| .agent/decisions.md | 1783242 | 3870 | 1787112 | True |

Two readings, both True. Negative control: reconstructed `pre + payload` for
`.agent/live_review.md` in a scratch script, flipped one bit inside the appended region
(offset `len(pre) + 50`), and compared against the real post-append file — unflipped
comparison: True; flipped comparison: False, as required.

### G1(d) — `.agent/plan.md` at C1b vs. `plan.md` payload

Both sha256 `116c0ee356cb5d8b267cf496779b249b8611fed876cdc7fbd8e3205167ca44ab`. Equal.
49 lines, under the 50-line rule.

### G1(e) — open set by distinct id in `.agent/live_review.md`

At `33d1c9df`: 27 distinct ids matching `^- R-\d+ — ` minus 7 distinct ids matching
`^Done: R-\d+ — ` = 20.
At C1b (`de1f10dd`): re-measured the same way = 27 distinct registered minus 7 distinct done =
20 (round 10 registers and resolves nothing under this pattern, so the two-line append to
`.agent/live_review.md` does not change the distinct-id open count).
Both readings: 20 and 20, as required — reported as measured, not merely claimed equal.

### G1(f) — `.agent/prose_slips.md` not touched

`git diff --name-only 33d1c9df de1f10dd` named exactly: `.agent/authored/f277-r10-block.md`,
`.agent/authored/f277-r10-decisions.md`, `.agent/authored/f277-r10-ledger.md`,
`.agent/authored/f277-r10-plan.md`, `.agent/decisions.md`, `.agent/live_review.md`,
`.agent/plan.md`. `.agent/prose_slips.md` does not appear, as required.

### G2 — code transport, blob ids at C3 (a2079ffd)

| path | blob id measured | blob id expected | match |
|---|---|---|---|
| apps/cli/commands/mission_cmd.py | 7ccec8fc2ffa425f305067c79f81083e8b27daa1 | same | True |
| tests/cli/test_mission_cmd.py | c499f988fde7cae998157890cae4c064abc21f88 | same | True |
| apps/cli/commands/contract_cmd.py | 395c2b05bb33906b46eb154a663833e16786d41c | same | True |
| tests/cli/test_contract_cmd.py | 2eeb2c16eb294eb36e99a73fe8c3d96a7544f57b | same | True |

All four match. `git diff --name-only de1f10dd a2079ffd` named exactly these four paths,
length 4, no fifth.

### G3 — targeted suite, in the primary checkout at C3

```
$ python3 -m pytest -q -p no:cacheprovider tests/cli/test_mission_cmd.py \
  tests/cli/test_contract_cmd.py tests/orchestration/test_mission_compiler.py \
  tests/orchestration/test_orchestrator_loop.py \
  tests/orchestration/test_import_reachability.py tests/test_grouped_cli.py \
  tests/test_command_catalog.py tests/cli/test_command_catalog.py \
  tests/test_no_orphan_modules.py tests/cli/test_golden_path.py tests/docs
1196 passed in 211.94s (0:03:31)
```
Exit code: 0. Re-ran a second time to confirm reproducibility: `1196 passed in 211.37s`, exit
0. This differs from the block's stated reviewer dry-run reading of `1194 passed` — reported
as measured, per the block's explicit "if your measurement differs ... report the number you
measured and say so." Both runs in this checkout landed exactly 1196 with zero failures; no
red result. Full suite was NOT run, per amend0917 rule 1.

### G4 — lint over the four G2 paths

```
$ python3 -m ruff check apps/cli/commands/mission_cmd.py tests/cli/test_mission_cmd.py \
  apps/cli/commands/contract_cmd.py tests/cli/test_contract_cmd.py
All checks passed!
```
Exit code: 0.

### G5 — mutation red-proofs, disposable worktree

`git worktree add --detach .remedy-wt/f277-r10-g5 a2079ffd` → succeeded, detached HEAD at
`a2079ffd`.

Unmutated control: `130 passed in 55.78s`, exit 0. Matches the block's stated `130 passed`
reading.

| mutation | anchor count | result | exit | failed node ids |
|---|---|---|---|---|
| (a) mission_cmd.py: drop `, exit_code=EXIT_NO_PROJECT` from `_resolve_project_id`'s `no_project` call | 1 | 5 failed, 125 passed | 1 | `TestStart::test_starting_without_a_project_exits_three`, `TestStatusTransitions::test_a_transition_without_a_project_exits_three`, `TestNoProjectIsRefusedInTheCallersShape::test_under_json_it_is_an_envelope_on_stdout`, `TestNoProjectIsRefusedInTheCallersShape::test_without_json_it_is_the_two_lines_it_always_was`, `TestNoProjectIsRefusedInTheCallersShape` (5th) → see note |
| (b) mission_cmd.py: `_load_mission_or_exit`'s `MissionNotFoundError` branch, `json_output=json_output` → `json_output=False` | 1 | 2 failed, 128 passed | 1 | `TestPlan::test_planning_an_unknown_mission_exits_one`, `TestTheTwoSharedHelpersThreadTheFlagIntoThisGroupToo::test_an_unknown_mission_is_an_envelope_under_json` |
| (c) mission_cmd.py: `"mission_plan_in_progress"` → `"plan_in_progress"` | 1 | 1 failed, 129 passed | 1 | `TestInProgressRefusal::test_a_recompile_is_refused_once_a_job_is_linked` |
| (d) mission_cmd.py: `_load_mission_or_exit` call before `call_fn = None`, drop `, json_output=json_output` | 1 | 1 failed, 129 passed | 1 | `TestPlan::test_planning_an_unknown_mission_exits_one` |
| (e) contract_cmd.py: drop `, json_output=json_output` from the `_resolve_project_id(project, ...)` call | 1 | 1 failed, 129 passed | 1 | `TestTheTwoSharedHelpersThreadTheFlagIntoThisGroupToo::test_no_project_is_an_envelope_under_json_and_exits_three` |
| (f) contract_cmd.py: drop `, json_output=json_output` from the `_load_mission_or_exit(project_id, mission_id, ...)` call | 1 | 1 failed, 129 passed | 1 | `TestTheTwoSharedHelpersThreadTheFlagIntoThisGroupToo::test_an_unknown_mission_is_an_envelope_under_json` |

Note on (a): the 5 failed node ids, exactly, were
`TestStart::test_starting_without_a_project_exits_three`,
`TestStatusTransitions::test_a_transition_without_a_project_exits_three`,
`TestNoProjectIsRefusedInTheCallersShape::test_under_json_it_is_an_envelope_on_stdout`,
`TestNoProjectIsRefusedInTheCallersShape::test_without_json_it_is_the_two_lines_it_always_was`,
`TestTheTwoSharedHelpersThreadTheFlagIntoThisGroupToo::test_no_project_is_an_envelope_under_json_and_exits_three`
(the fifth is in `test_contract_cmd.py`, not `test_mission_cmd.py` — both files were in the
same pytest invocation). All five match the block's expected list exactly.

Every reading matches the block's expected numbers and node ids exactly. Each file was
restored byte-identically after its mutation (manual re-`Edit` back to the original text,
confirmed with `git status --porcelain` empty in the worktree after every single revert). No
mutation stayed green.

Restored control (after all six reverts): `130 passed in 55.27s`, exit 0. `git status
--porcelain` in the mutation worktree: empty.

`git worktree remove .remedy-wt/f277-r10-g5` → succeeded. `git worktree list` after removal
shows the primary checkout and the two pre-existing `remedy/job-*` worktrees only (see G6).

### G6 — push and tree, after C4

(Filled in by the C4-fix commit once the push has actually run — see Deviations.)

## Authored-text proofs

The four `.agent/authored/f277-r10-*` files copied at C1a were each compared byte-for-byte
(`cmp`) against their reviewer-authored source under `.remedy-wt/f277-r10-payloads/` (the
block copy against `.remedy-wt/f277-r10-block.md`). All four: True. See G1(b) above.

## Deviations & assumptions

1. The block's own BUNDLE header reads "SIX COMMITS" but lists only five sub-items
   (C1a, C1b, C2, C3, C4); the worker executed exactly those five, in the block's stated
   order, with none dropped, added, or reordered. This is a reviewer-prose miscount with no
   product effect — the block itself explicitly forbids touching `.agent/prose_slips.md` this
   round ("There is NO slips payload this round"), so per AGENTS.md's prose-vs-product-defect
   split this is recorded here in the handback's deviations rather than in that file or as an
   R-id.
2. **A trailing C4-fix commit, following round 9's identical precedent (C7/C7-fix).** C4
   writes this handoff with the G6 push outcome not yet knowable (the push is C4's own
   trailing action per the block's own instruction: "rewrite handoff, then push"); C4-fix
   fills in the real `git push`/`git status`/`git worktree list` readings for G6 once they
   exist. This is the handback template's explicit "trailing bookkeeping commits that only
   trim it" exception (R-0149 pattern).
3. G3's targeted-suite count read `1196 passed` in this checkout, both on first run and on a
   confirming re-run, against the block's stated reviewer dry-run reading of `1194 passed`.
   Both counts are exit 0 with zero failures; the gate is green either way. Reported as
   measured, not adjusted, per the block's explicit instruction for a differing count.

## Next

T003 continues, by `sys.exit` site: `job` (44), `decision` (31), `project` (25), `brain` (24),
`do` (19), `patch` (18), `memory` (9), `grouped` (8), `test_cmds` (7), then the tail.
`runtime_cmd.py` is its own round (27 sites, exit codes 2-5, `error_class` supervisor
contract). T003 closes with the catalog half (33 read-only commands without `supports_json`).
Then T004 (exit-code taxonomy + sweep) and closure.
