# Handback — F314 "Findings paydown v10," round 2

## Session

SESSION 1 of feature F314 · round 2 · rounds so far 2

Context self-assessment: this session booked round 1's FAIL verdict and the two findings it
raised, repaired both mechanically, wrote `run_order`'s structure-ledger boundary, then carried out
T003's seam change and its new test, reading every touched file whole before editing it and running
every gate exactly once, after the last commit.

State block:
Feature F314 (claimed `[~]`), branch `feature/f314-findings-paydown-v10`, base `b50f09647`.
Fortschritt: ~25 % (T001 to T003 landed · T004 to T008 open) — Schätzung

## Range

Review of `b50f09647`..HEAD.

## Commits

### dfe686be9 F314 R2 C1: book F314 R1, register R-1443 and R-1444, DECISION F314 D3
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f314-r2.md` | +139/-0 | NEW FILE; byte copy of this round's block, `block.md` |
| `.agent/decisions.md` | +10/-0 | DECISION F314 D3 appended |
| `.agent/live_review.md` | +6/-0 | F314 round 1's FAIL gate entry and R-1443/R-1444 appended |
| `.agent/plan.md` | +8/-8 | rewritten for F314 round 2 |
| `.agent/prose_slips.md` | +1/-0 | one prose-slip line appended |

All five paths are byte copies of the reviewer's prepared `c1-*` files; gate 1's `verify.py` and a
direct sha256 comparison (see Authored-text proofs) confirm each equality.

### f29df1e00 F314 R2 C2: the debt-word test reads a whole word, and the order tier leaves the runner's prose (R-1443, R-1444)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/self_use_runner.py` | +2/-2 | R-1444: `parse_order_budget`'s docstring no longer names "the order tier"; it says a queue item may itself be a multi-task order |
| `tests/orchestration/test_self_use_generator.py` | +1/-1 | R-1443: the handler fixture's exception name becomes `except Exception as debt:`, a whole word before the mark |
| `tests/orchestration/test_self_use_runner.py` | +4/-7 | R-1444: the two-line standing-order comment removed; the Tier-0 half of a second comment removed; `TestAnExcusedHandlerItemRunsToTheApprovalGate`'s docstring drops its Tier 0 clause, "tiers 0 to 3" becomes "tiers 1 to 3" |

Authored to the specification under C2, not byte copies — no `c2-*` prepared files exist to compare
against (the block's own header marks C2 as text the worker writes).

### e134d814d F314 R2 C3: the structure ledger writes run_order's boundary
| Path | +/- | Reason |
|---|---|---|
| `docs/system/structure-ledger-v1.md` | +7/-0 | `run_order`'s boundary and two-step plan added to the Functions list (DECISION F314 D3) |

Byte copy of the reviewer's prepared `c3-*` file; gate 1's `verify.py` and a direct sha256
comparison (see Authored-text proofs) confirm equality.

### ee12f8083 F314 R2 C4: the gauntlet opens its order in the workspace's repository mission (R-1281)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/gauntlet_runner.py` | +13/-7 | R-1281, DECISION F314 D3: `_default_accept_order` added beside `_default_make_project`; `RunnerDeps.create_mission` replaced by `accept_order`, defaulting to it; the `create_mission` branch of `__post_init__` removed; `run_order`'s mission line now calls `deps.accept_order(project_id, workspace, order.goal)`; the module docstring names `accept_order` |
| `packages/orchestration/mission_state.py` | +2/-2 | `create_mission`'s docstring drops the clause naming the gauntlet as a caller; no code changed |
| `tests/orchestration/test_bench_model_context.py` | +1/-1 | the `create_mission` double becomes an `accept_order` double taking `(project_id, workspace, goal)` |
| `tests/orchestration/test_bench_run.py` | +3/-3 | the module docstring, the `deps()` wiring and the double itself renamed from `create_mission`/`_create_mission` to `accept_order`/`_accept_order` |
| `tests/orchestration/test_gauntlet_runner.py` | +30/-4 | the `Recorder` double and `test_the_defaults_are_the_production_verbs` renamed to `accept_order`/`_default_accept_order`; new test `test_the_default_order_seam_opens_the_workspace_repository_mission` added, proving the default seam leaves exactly one mission of the right repository, goal and newest order-batch text |

`run_order` stays at 125 lines — both gate 1's ratchet reading and running
`tests/test_structure_ratchet.py` directly confirm it. `tests/orchestration/import_reachability_allowlist.txt`
needed no new line: `repo_mission` and `mission_record` were already reachable and allowlisted
before this commit, and `test_import_reachability.py` passed unmodified.

### this commit — F314 R2 C5: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | n/a (self-reference; R-0149 pattern) | this handback, rewritten per `docs/agents/handback_template.md` |

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `dfe686be9`, five paths, each byte-equal to its prepared `c1-*` file |
| C2 | done | `f29df1e00`, exactly the three named paths, authored to spec |
| C3 | done | `e134d814d`, `docs/system/structure-ledger-v1.md` only, byte-equal to its prepared `c3-*` file |
| C4 | done | `ee12f8083`, exactly the five named paths; `run_order` stays at 125 lines; the allowlist needed no line |
| C5 | done | this commit, `.agent/handoff.md` only |
| Gate 1 (`verify.py`) | done | every line `True`, `C5` read `absent`, last line `ALL True` |
| Gate 2 (`ruff check .`) | done | `All checks passed!` |
| Gate 3 (pytest selection) | done | exit 0, `4144 passed, 2 skipped in 39.99s`, no FAILED/ERROR/`process(es) behind` line |
| Gate 4 (integrity) | done | `"fail_count": 0` |
| Gate 5 (open finding ids) | done | `14` |
| Push | done | see External actions / the reply after this handback |

## External actions

- `git push origin feature/f314-findings-paydown-v10` — to run immediately after this commit,
  carrying `dfe686be9`, `f29df1e00`, `e134d814d`, `ee12f8083` and this handback's own commit; see
  the reply for the push's own result. The branch already tracks `origin/feature/f314-findings-paydown-v10`.
- No PR created, edited or merged by this session (none is ordered by this round's block; no open
  PR exists on this branch). No `gh` command run. No `git worktree add`/`remove` run.
- One scratch directory used, `.remedy-wt/f314-r2-worker/`, holding only three Python helper
  scripts (`check_digests.py`, `c1_copy.py`, `c3_copy.py` — the digest-verification and
  byte-copy-with-hash-check helpers) and gate 3's raw output file; `.remedy-wt/f314-r2/` (the
  reviewer's prepared tree) was only read, never written.

## Verification

Gate order per the block, run once each, after C4 and before this handoff.

1. `git status --porcelain` → empty.
   `python3 .remedy-wt/f314-r2/prep/verify.py .` →
   ```
   True	dfe686be9 single parent equal to the commit before it
   True	dfe686be9 insertions 164 under 500
   True	f29df1e00 single parent equal to the commit before it
   True	f29df1e00 insertions 7 under 500
   True	e134d814d single parent equal to the commit before it
   True	e134d814d insertions 7 under 500
   True	ee12f8083 single parent equal to the commit before it
   True	ee12f8083 insertions 49 under 500
   True	every commit carries a F314 R2 Cn subject: 4 of 4
   True	the commits come in block order: ['C1', 'C2', 'C3', 'C4']
   True	on feature/f314-findings-paydown-v10
   True	C1 paths [...] within [...]
   True	C1 .agent/authored/f314-r2.md equals c1-.agent__authored__f314-r2.md
   True	C1 .agent/decisions.md equals c1-.agent__decisions.md
   True	C1 .agent/live_review.md equals c1-.agent__live_review.md
   True	C1 .agent/plan.md equals c1-.agent__plan.md
   True	C1 .agent/prose_slips.md equals c1-.agent__prose_slips.md
   True	C2 paths [...] within [...]
   True	C3 paths [...] within [...]
   True	C3 docs/system/structure-ledger-v1.md equals c3-docs__system__structure-ledger-v1.md
   True	C4 paths [...] within [...]
   absent	C5
   True	run_order no longer calls create_mission
   True	the saved block equals block.md
   ALL True
   ```

2. `python3 -m ruff check .` → exit 0, `All checks passed!`.

3. `python3 .remedy-wt/f314-r2/prep/run_selection.py . .remedy-wt/f314-r2-worker/selection-output.txt` →
   ```
   paths 96
   exit 0
   4144 passed, 2 skipped in 39.99s
   SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): ...
   SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
   ```
   Exit 0; no FAILED, ERROR or `process(es) behind` line. Both skips are pre-existing and unrelated
   to this round's files (one a documented quarantine, one an opt-in network smoke test).

4. `python3 -m apps.cli.main integrity check --json` →
   `{"check_count": 6, ..., "fail_count": 0, "ok": true, "passed": true, ...}` — `fail_count: 0`.

5. `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` →
   `14`.

## Authored-text proofs

- `.agent/authored/f314-r2.md`: `wc -l` 139, matching `block.md`'s 139; sha256
  `c39132f962740c6de7852f7f3eeb3d1f07c30dc68861fac2abbadbbff87609a8` on both. Byte-identical.
- `.agent/decisions.md` against `.remedy-wt/f314-r2/prep/c1-.agent__decisions.md`: sha256
  `6b122a4abe60ecd0684771a8a76ae2c32f8ff3d61c7c60a3838e40cdafe4a2c8` on both. Byte-identical.
- `.agent/live_review.md` against `.remedy-wt/f314-r2/prep/c1-.agent__live_review.md`: sha256
  `431d3ce944f53367cbf2ae88d4fcfa8656c605c31e2ee57c2a9aa8624273e681` on both. Byte-identical.
- `.agent/plan.md` against `.remedy-wt/f314-r2/prep/c1-.agent__plan.md`: sha256
  `baebb6246a16473c2f11dfccf7a47861770c943d6c406f744389a15775ffcecf` on both. Byte-identical.
- `.agent/prose_slips.md` against `.remedy-wt/f314-r2/prep/c1-.agent__prose_slips.md`: sha256
  `2d22ac20ddd3cd1565cee9a42fe0bfc5b382e9f977f64b9a80f6c17fb908aa71` on both. Byte-identical.
- `docs/system/structure-ledger-v1.md` against
  `.remedy-wt/f314-r2/prep/c3-docs__system__structure-ledger-v1.md`: sha256
  `6d4fe55b160813855abd8dc3089a3a5b3878ada1f97bff9f53cd637e3053cd11` on both. Byte-identical.

Before using any prepared file, `.remedy-wt/f314-r2/prep/digests.txt` was checked against its own
stated sha256 (`c41fe6a8183bbbf39dd8da573b2607cf4ef186799d8e87a9f7ae382d32baf197`, matched), then
every one of its ten listed entries was recomputed and matched, before any prepared file was
copied, run or read. C2 and C4 have no `c*-` prepared files — both are authored text per the
block's own instructions, not byte copies.

## Deviations & assumptions

None. C1 through C4 landed in the block's order, with no added, dropped or reordered commit; every
`c1-*` and `c3-*` prepared byte was copied verbatim and proved equal by direct byte comparison
before being staged; every gate ran exactly once, after C4 and before this handoff, with no retry
needed; `tests/orchestration/import_reachability_allowlist.txt` was checked and needed no line, as
the block allowed.

## For the operator, in plain sentences

This session closed out last round's review, fixing the two small gaps it found: a handler test
that could not actually tell debt code from clean code, and a few leftover sentences describing a
practice source that no longer exists. It then moved the one remaining piece of last round's larger
change. An automated challenge that exercises Remedy's own build loop used to open a separate,
throwaway piece of work for the model to act on; now it opens that work the same way a person's own
request would, inside the one ongoing record a repository already keeps for its real work. That
brings the automated challenge closer to testing the real path a person's request takes, rather
than a shortcut built only for testing. Every required check came back clean, and the branch is
about to be pushed so the next session can continue with the remaining open work.

## Next

1. Phase 1 rule 1: if `.agent/STOP` exists, the next session finishes whatever commit is in hand,
   writes the handoff, pushes, and stops, before anything else.
2. Rule 2, the Open PR Gate: check for open pull requests before starting any new unrelated work.
3. Book this round's verdict in the next round's first commit.
4. T004: R-1326, the `[roles]` table.

Operator questions open: 1. Open findings: 14.
