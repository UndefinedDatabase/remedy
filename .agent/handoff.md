# Handoff — F105 R48 (T004's before/after comparison note)

Branch: feature/f105-cache-optimal-prompt-ordering. Base 5e55669d.
Commits: f8664f38 (C1), fd48d5fa (C2), dd5881da (C3), 54396c6b (C4),
b817a117 (C5), c0e8ff2b (C6), HEAD (C7).
No production code under `packages/` or `apps/` was edited: this round MEASURES
what T001–T003 built. No frozen golden constant was touched. No PR was created,
nothing was merged, `main` was not touched, no force-push. T004 is now COMPLETE.

## Changed files
| Path | Commit | +/- |
|---|---|---|
| .agent/authored/f105-r48-1.md | C1 f8664f38 | +191/-0 (new file) |
| .agent/last_block.md | C2 fd48d5fa | +172/-121 |
| .agent/live_review.md | C3 dd5881da | +38/-0 |
| tests/orchestration/test_prompt_cache_prefix.py | C4 54396c6b | +322/-0 (new) |
| docs/system/cache-optimal-prompt-ordering-v1.md | C5 b817a117 | +175/-0 (new) |
| docs/README.md | C5 b817a117 | +2/-0 |
| docs/roadmap/features/T2_F105.md | C6 c0e8ff2b | +43/-0 |
| .agent/plan.md | C7 HEAD | full rewrite, 45 lines |
| .agent/handoff.md | C7 HEAD | full rewrite (this file) |

## Item status
| Item | Status | Reason |
|---|---|---|
| C1 | done | block written to .agent/authored/f105-r48-1.md, committed alone |
| C2 | done | same bytes copied to .agent/last_block.md, separate commit |
| C3 | done | PAIR_LR contains-from: R47 gate record + R48 step line; no ID advance |
| C4 | done | measurement module, 16 tests, `measure_cacheable_prefixes()` |
| C5 | done | ist-doc + BOTH docs/README.md rows in the same commit |
| C6 | done | `## Built State` appended to T2_F105.md, no numbers restated |
| C7 | done | plan.md (45 lines) + this handoff, then push, no PR |

## Measured before/after cacheable prefix — characters
Command, from the repo root: `python3 -m tests.orchestration.test_prompt_cache_prefix`

| Role | before_prefix | after_prefix | before_total | after_total |
|---|---|---|---|---|
| intake | 115 | 672 | 681 | 681 |
| plan | 227 | 1463 | 1548 | 1548 |
| mission | 207 | 1478 | 1576 | 1576 |
| builder | 458 | 620 | 1460 | 1460 |
| reviewer | 241 | 1134 | 1987 | 1987 |
| orchestrator | 3872 | 3872 | 3916 | 3916 |

`before_total == after_total` in every row: the composed prompt is a permutation
of the pre-migration one. `orchestrator` does not move because its pre-migration
order was ALREADY rank order — an honest zero-delta, not a gap.

## Gates — real exit codes
| Gate | Command | Exit | Result |
|---|---|---|---|
| A | sha256sum block/authored/last_block | 0 | all three EQUAL (digest below) |
| A | cmp block vs authored; cmp block vs last_block | 0, 0 | both silent |
| B | wc -l .agent/authored/f105-r48-1.md | 0 | 191 vs D5 cap 400 |
| C | PAIR_LR shape, MEASURED | 0 | FROM 1->1, TO 0->1; 38 TO-only lines each 1x |
| D | stray reconcile, C3 live_review.md | 0 | 38 added, 0 removed, 0 strays |
| E | grep -c '^<<<' over the six written files | 1 x6 | counts 0,0,0,0,0,0 |
| F | python3 -m pytest tests/docs/ -q | 0 | 294 passed in 0.30s |
| G | pytest tests/orchestration/test_prompt_cache_prefix.py -q | 0 | 16 passed in 0.20s |
| H | pytest tests/orchestration/ -q -k "prompt_golden or ..." | 0 | 109 passed, 10431 deselected in 2.57s |
| I | pytest tests/cli/test_golden_path.py -q (canary) | 0 | 42 passed in 19.81s |
| J | probe in a disposable worktree | 0 / 1 | see below — the block's mutation stayed GREEN |
| J | git worktree list after removal + prune | 0 | primary ALONE |
| K | insertions per commit | 0 | 191, 172, 38, 322, 177, 43 — all < 500 |
| K | git diff --name-only 5e55669d..HEAD | 0 | exactly the 9 named paths |

Gate E note: `grep -c` exits 1 when the pattern is absent, and absence IS the
pass condition; the recorded numbers are the counts, all zero. Extra check run
beyond the block: `ruff check` on the new module, exit 0, "All checks passed!".

## Transport proof
`.remedy-wt/f105-r48-1.block.md`, `.agent/authored/f105-r48-1.md` and
`.agent/last_block.md` all three hash to
`c6c7d4549d10470888aa7806f92790038060b735a60cff2ea48b97c00ecb4fae`,
191 lines, no trailing whitespace, no tabs, no CR. Both `cmp` runs silent,
exit 0. The PAIR_LR body was SLICED from the COMMITTED authored file by
`.remedy-wt/r48_apply.py`, which refuses any marker not present exactly once,
refuses to write unless FROM == 1, additionally asserts TO startswith FROM
(the declared CONTAINS-FROM shape), and asserts TO == pre_TO + 1 afterwards.
Nothing was retyped. Scratch lives in the gitignored `.remedy-wt/`.

## Gate J — the probe outcome, in words
Ran at HEAD in a disposable worktree, twice, then removed and pruned.

**The block's own suggested mutation — give every registered segment the same
rank — left gate G GREEN: 16 passed.** That is the REAL outcome and it is a
result worth having. Reason, measured rather than guessed: five of the six sites
register their segments in an order that ALREADY equals rank order, so forcing
one rank is a no-op there. Only `plan` moved, and it collapsed to exactly its
pre-migration figure (`after_prefix` 1463 -> 227, equal to `before_prefix` 227),
which a `>=` assertion cannot catch. So the directional assertion does NOT prove
that composition sorts; it proves composition never sorts WORSE than the old
hand-written order.

**A second, stronger mutation — reverse the sort key in
`compose_prompt_segments` — turned gate G RED: 5 failed, 11 passed**, e.g.
`orchestrator: after_prefix 37 < before_prefix 3872`. intake, plan, mission,
builder and orchestrator all failed; `reviewer` alone stayed green because
reversing puts its many rank-5 segments first and its shared prefix happens to
grow (241 -> 860). So the module is NOT vacuous — it bites on a real defeat of
the ordering — but its sensitivity is bounded, and the honest statement is the
one above: it is a REGRESSION guard on the ordering's value, not a proof that
the registry sorts at all. The T003 goldens' `test_manifest_names_and_ranks` and
`test_manifest_ranks_are_non_decreasing` are what prove the sort.

Both mutations were reverted with `git checkout --` inside the worktree, the
worktree was removed with `--force` and pruned; `git worktree list` then shows
the primary ALONE and `git status --porcelain` is empty.

## Open findings: 7
R-0221, R-0239, R-0247, R-0262, R-0265, R-0266, R-0268 — all OPEN, none fixed
and none touched this round. No finding was registered, so the next free ID
stays R-0269 and no `Landed:` line was written.

## PR #189 — untouched, stop-and-report
`docs/amend0810-clerical` -> `main`, open, NOT from a `feature/*` branch, so the
AGENTS.md Open PR Gate makes it stop-and-report rather than merge. This round did
not merge, comment on, or modify it. The operator must resolve it BEFORE F105's
closure PR is cut.

## Next expected action
Reviewer gates R48 over `5e55669d..HEAD`. Then, per `.agent/plan.md`: the
integration gate (`docs/agents/integration_gate.md`), then closure
(`docs/roadmap/STATUS_closure_protocol.md`), with PR #189 resolved first.

Deviations, declared: ONE, and it is a reporting limit rather than a scope
change. Gate K's "insertions per commit" row cannot carry C7's own count,
because C7 is the commit that writes this file. Rather than add a second commit
(the R47 C3b shape) or leave a placeholder, the row lists the six countable
commits and the reviewer reads C7's own count from `git show --stat HEAD`; both
its paths are full rewrites of single `.agent/**` state files, which DECISION
F104 D1 exempts from the cap by construction. Nothing else deviates: the diff
touches exactly the nine paths the block named, and no gate outcome changes.

Deviations, declared (DECISION D15): this handoff is 143 lines against the
60-line cap. The cause is mandated content only — the 14-row gate table with its
real exit codes, the changed-files table, the item-status table, the transport
proof, the block-mandated measured before/after table with its command, and the
block-mandated gate-J probe outcome in words (which reports two mutations
because the first came back green and hiding that would be the finding), plus
the finding state, PR #189 and the next action. No section was dropped and no
prose was added to reach that length.
