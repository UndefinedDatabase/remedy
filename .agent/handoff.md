# Handback — F051 R2 (verdict persist + R-0157 + Built State + integration gate)

## Range
`34a32a1..HEAD` · feature/f051-escalate-instead-of-block · 5 commits this round
(R1's 9 are below it). PR **#165** updated, base `main`, **NOT merged**.
R2 verdict: **PENDING** — the gate verdict is the reviewer's; this carries records only.

## Item status
| Item | Status | Reason |
|---|---|---|
| 1 guard | done | block f051-r2 recorded in `.agent/last_block.md`, OUTCOME pending → executed |
| 2 authored texts | done | both sha256 matched first try, no rejoin |
| 3 persist commit | done | `d432a3f`; cmp 0 for both state files |
| 4 R-0157 fix + CLI test | done | `a96a8ce` + `6c4dae2`; slice gate 178 exit 0 |
| 5 Built State | done | `f59e88f` |
| 6 docs gate + canary | done | 292 exit 0 · 42 exit 0 |
| 7 integration gate | done | executed in full; **no branch-only failures**; STOP-ON-RED not triggered |
| 8 handback + push + PR update | done | this commit; PR #165 body updated; not merged |

## Authored-text verification — `sha256sum` output verbatim
    c3c89e2a8c698dd5cf57c6a475e2ee6775602d5d34d84e21673c0847d76b931b  .agent/authored/f051-r2-1.md
    63ac4c5a13a2910994135f4f77504634245c0e24f377d7ab3e528f0e367510d7  .agent/authored/f051-r2-2.md
Both equal their BEGIN-marker hashes; no transport fault in the authored bytes.
`cmp` live_review vs f051-r2-1 → **0**; `cmp` plan vs f051-r2-2 → **0**.
The only later edit to `live_review.md` is the single line the block dictated:
`  Done: R-0157 (commit a96a8ce).` appended at the end of the R-0157 bullet
(`6c4dae2`, diff = +1 line, nothing else touched).

## Commits
| Commit | Files | +/- | Note |
|---|---|---|---|
| `d432a3f` chore | `.agent/authored/f051-r2-{1,2}.md`, `.agent/{live_review,plan,last_block}.md` | +209/-163 | R1 PASS persisted, R-0157 registered |
| `a96a8ce` fix R-0157 | `apps/cli/command_catalog.py`, `apps/cli/commands/job.py`, `tests/orchestration/test_escalation.py` | +165/-2 | `--unattended` flag → `run_cycles(unattended=…)` + 7 CLI tests |
| `6c4dae2` chore | `.agent/live_review.md` | +1 | the dictated Done line |
| `f59e88f` docs | `docs/roadmap/features/T1_F051.md` | +62 | Built State, F050's shape |
| this commit | `.agent/handoff.md`, `.agent/last_block.md` | rewrite | handback, OUTCOME executed |

## R-0157 — what was built
`job run --unattended` (catalog `job.run`, `ArgDef(is_flag=True)`, additive) →
handler `unattended=getattr(args, "unattended", False)` →
`_cmd_job_run_cycles(unattended=…)` → `run_cycles(…, unattended=unattended)`.
Default OFF; attended behavior byte-unchanged. Help text names both halves:
safe defaults auto-apply into the escalation assumption log, a question with no
default still waits.
One thing the finding did not mention and I did not paper over: while the F046
rollout cap collapses a run to the single pass (`resolved.max_cycles <= 1`), the
loop never runs, so the flag cannot do what its help promises — the command now
prints a `Note: --unattended has no effect …` on stderr instead of accepting it
silently. Two tests pin that (present with the flag, absent without).
CLI-level tests (7, in `test_escalation.py::TestUnattendedRunLoopCliFlag`), all
driving the real `_cmd_job_run_cycles` with `CYCLE_SAFETY_CAP` lifted the way
the existing `job.run` multi-cycle test does: (a) with the flag the safe default
is auto-answered — `answer_source "default"`, no open decisions, terminal
`all_green`, every task COMPLETED; (b) without it the same fixture ends
`blocked`, exit 1, one open decision still carrying its `safe_default`; plus
catalog registration, handler passthrough, and an old namespace lacking the
attribute (defaults to False, no crash).

## Round gates — raw
    $ python3 -m pytest tests/orchestration/test_escalation.py \
        tests/orchestration/test_long_run_executor.py \
        tests/cli/test_open_decisions_view.py tests/cli/test_command_catalog.py -q
    178 passed in 0.99s          EXIT=0     (slice gate, item 4)

    $ python3 -m pytest tests/docs/ -q
    292 passed in 0.25s          EXIT=0

    $ python3 -m pytest tests/cli/test_golden_path.py -q
    42 passed in 19.07s          EXIT=0

`ruff check` clean on every file touched this round.

## Integration gate (docs/agents/integration_gate.md) — records
**Step 1 — branch run**, repo root, `python3 -m pytest -n auto -q`:

    14435 passed, 19 skipped in 144.80s (0:02:24)
    EXIT=0   WALL=145s
    grep '^FAILED' branch.log | sort > branch_failed.txt   ->  0 lines

**Step 2 — base run**, identical command, throwaway worktree at the merge base
`894375e40f2d88c3d2cd2859073423faa2b17120` (`git merge-base main HEAD`):

    20 failed, 14317 passed, 25 skipped in 161.50s (0:02:41)
    EXIT=1   WALL=162s
    base_failed.txt  ->  20 lines

Collection delta branch − base = 14454 − 14362 = **+92**, exactly this feature's
new tests (66 escalation + 26 open-decisions view). Nothing else appeared or
vanished.

**Step 3 — compare.**
`comm -13 base_failed.txt branch_failed.txt` (branch-only) → **EMPTY**.
The branch run has zero failures, so the branch-only set is empty by
construction, not by interpretation.
`comm -23` (base-only, 20 ids — failures the branch "fixed"):

    tests/cli/test_self_dogfood_execution_cli.py           2 ids
    tests/orchestration/test_test_runner.py                1 id   (vitest)
    tests/ui_server/test_dashboard_contract.py             1 id   (tsc)
    tests/ui_server/test_live_state.py                    16 ids
    (full id list: gate/base_failed.txt, reproduced in the PR body)

**Step 4 — attribution.** No branch-only ids exist, so there is nothing to
re-run serially and STOP-ON-RED cannot trigger. The 20 base-only ids are the
known R-0155 environment class, attributed by direct evidence rather than
assumption:
- worktree vs primary checkout: `node_modules` **ABSENT** in the worktree
  (present in primary), `apps/ui/dist` **ABSENT** (present in primary);
  `apps/ui/node_modules` and `.data` were present in both.
- raw causes from `base.log`: `AssertionError: vitest failed:` /
  `Cannot find package 'vitest'` / `AssertionError: tsc failed:` /
  `CompletedProcess(args=['npx', 'tsc', '--noEmit'], returncode=1)` — i.e. a
  missing root `node_modules`, and a UI server with no built `dist` to serve.
- scope grep: none of the four failing test FILES is in this branch's changed
  set (19 changed files, listed in the commit tables above) — zero coupling to
  feature code.
Refinement worth carrying into R-0155's eventual fix: the missing outputs here
are the **root `node_modules`** and **`apps/ui/dist`**, not `apps/ui/node_modules`
as the finding's text currently says.

**Worktree removal proof.**

    $ git worktree remove --force <scratch>/base-wt && git worktree prune
    $ git worktree list
    /home/decodeux/Repos/remedy  f59e88f [feature/f051-escalate-instead-of-block]
    directory gone: removed        primary tree: git status --porcelain empty

**Step 5 — budget.** Branch 2:24, base 2:41 — both under the ~5 min threshold;
no perf pass indicated. Verdict deliberately NOT issued here.

## Deviations
None. Every item executed as written; no stop-on-red condition arose.

## Observations (not deviations)
1. The `--unattended` no-effect note under the rollout cap (above) is behavior
   the block did not specify; silence seemed worse than a stderr line. Reviewer
   call.
2. `docs/roadmap/features/T1_F051.md` Built State claims only what tests pin;
   test counts are from `--collect-only` (66 + 26 = 92).
3. Gate logs kept at the session scratchpad (`gate/branch.log`, `base.log`,
   `branch_failed.txt`, `base_failed.txt`) — not committed, per the round's
   Change list.

## Open findings
**R-0155** (process, Low) and **R-0156** (process, Medium) remain open,
planning-routed. **R-0157** carries the dictated `Done:` line and awaits the
reviewer's Resolved. Next free ID: **R-0158**.

## Next expected action
Reviewer R2 verdict, including the integration-gate verdict on the records
above. Then closure per `docs/roadmap/STATUS_closure_protocol.md` — its own
round, never bundled; its zip was explicitly not part of R2.
