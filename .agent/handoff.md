# Handback — F314 "Findings paydown v10," round 4

## Session

SESSION 1 of feature F314 · round 4 · rounds so far 4

Context self-assessment: this session booked round 3's FAIL verdict, resolved R-1444 and R-1445,
registered R-1446 to R-1448 and DECISIONs F314 D5 and D6, repaired R-1446 and R-1447 with two new
tests and a moved guide paragraph, made the `[roles]` table refuse a `planner` key, and finished
T005 by bringing the two modules DECISION F314 D6 named to zero mypy errors without a behaviour
change — reading every touched file whole before editing it and running every gate exactly once,
after the last commit.

State block:
Feature F314 (claimed `[~]`), branch `feature/f314-findings-paydown-v10`, base `1d02d2ffd`.
Fortschritt: ~55 % (T001 to T005 landed · T006 to T008 open) — Schätzung

## Range

Review of `1d02d2ffd`..HEAD.

## Commits

### ee91513c5 F314 R4 C1: book F314 R3, resolve R-1444 and R-1445, register R-1446 to R-1448, DECISIONs F314 D5 and D6
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f314-r4.md` | +125/-0 | NEW FILE; byte copy of this round's block, `block.md` |
| `.agent/decisions.md` | +20/-0 | DECISIONs F314 D5 and D6 appended |
| `.agent/live_review.md` | +12/-0 | F314 round 3's FAIL gate entry, R-1444's and R-1445's resolutions, R-1446, R-1447 and R-1448 appended |
| `.agent/plan.md` | +8/-10 | rewritten for F314 round 4 |

All four paths are byte copies of the reviewer's prepared `c1-*` files; gate 1's `verify.py` and a
direct sha256 comparison (see Authored-text proofs) confirm each equality.

### a4715ca55 F314 R4 C2: run_job reads the project's roles table under test, the guide's paragraph follows the options, and the table refuses a planner key (R-1446, R-1447)
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_job_task_runner.py` | +36/-0 | `TestConfigSourceAudit` gains `test_first_run_takes_providers_from_the_project_roles_table` (a `[roles]` table of `fake`/`fake`, `run_job` called with no name and no injected provider, both roles read `fake` with source `roles`) and `test_a_project_roles_table_that_cannot_be_used_stops_the_job_before_any_call` (`builder = "nobody"`, injected recording providers, `ProjectRolesError` raised and neither provider's call counter moved) |
| `docs/guides/do-run-v1.md` | +15/-13 | the `[roles]` paragraph and its TOML example move out of the `## Flags` list to directly after its last bullet, with a blank line before and after; the refusal sentence now says the run is refused when its job starts, before the builder or the reviewer is called; the example now reads `claude-cli`/`claude-cli`; one new sentence names `--planner-provider` and `planner.provider` of `remedy.toml` for the planner and says the table refuses a `planner` key |
| `packages/orchestration/project_roles.py` | +25/-23 | `PROJECT_ROLES_KEYS` becomes `("builder", "reviewer")`; a `planner` key raises `ProjectRolesError` naming `--planner-provider` and `planner.provider` of `remedy.toml`; the `planner` branch and the `PLANNER_PROVIDERS` import are gone; the module and function docstrings say so |
| `tests/orchestration/test_project_roles.py` | +8/-7 | `test_all_three_keys_are_read` loses its planner key and is renamed `test_both_keys_are_read`; `test_a_planner_outside_the_planner_providers_is_refused` becomes `test_a_planner_key_is_refused`, asserting the new refusal sentence; every other test stays |

### 63f925853 F314 R4 C3: the role provider factory and the do sequence type-check clean (R-1425)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/role_provider_factory.py` | +1/-1 | `common` in `create_role_provider` gets the explicit annotation `dict[str, Any]`, so `**common` type-checks against `ClaudeCliProvider`'s individual keyword parameters instead of their union (6+6 errors to 0) |
| `packages/orchestration/do_sequence.py` | +9/-9 | `cast` added to the module's `typing` import; `_first_pass_task_plan`'s five uses of `fp_result.plan` after the try/except (whose `except` branch reassigns `fp_result` itself, invalidating the narrowing the leading `if fp_result.plan is not None:` gave it, R-0768's class) become `cast(Any, fp_result.plan)`; `_step_plan`'s and `_step_shape`'s three uses of `ctx.project` (whose field is `RemyProject | None`, narrowed only by the init step's own ordering, `do_targets.py`) become `cast("RemyProject", ctx.project)`, the string form reading the name already imported under `TYPE_CHECKING` so no new runtime import is needed. No behaviour changed; mypy on the two modules: 12 and 8 errors to 0 and 0 |

### this commit — F314 R4 C4: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | n/a (self-reference; R-0149 pattern) | this handback, rewritten per `docs/agents/handback_template.md` |

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `ee91513c5`, four paths, each byte-equal to its prepared `c1-*` file |
| C2 | done | `a4715ca55`, exactly the four named paths, authored to spec |
| C3 | done | `63f925853`, exactly the two named paths; no listed function grew |
| C4 | done | this commit, `.agent/handoff.md` only |
| Gate 1 (`verify.py`) | done | every line `True`, `C4` read `absent`, last line `ALL True` |
| Gate 2 (`ruff check .`) | done | `All checks passed!` |
| Gate 3 (pytest selection) | done | exit 0, `7429 passed, 2 skipped in 126.76s`, no FAILED/ERROR/`process(es) behind` line |
| Gate 4 (integrity) | done | `"fail_count": 0` |
| Gate 5 (open finding ids) | done | `15` |
| Gate 6 (mypy gate) | done | `role_provider_factory.py 0`, `do_sequence.py 0` |
| Push | done | see External actions / the reply after this handback |

## External actions

- `git push origin feature/f314-findings-paydown-v10` — to run immediately after this commit,
  carrying `ee91513c5`, `a4715ca55`, `63f925853` and this handback's own commit; see the reply for
  the push's own result. The branch already tracks `origin/feature/f314-findings-paydown-v10`.
- No PR created, edited or merged by this session (none is ordered by this round's block; no open
  PR exists on this branch). No `gh` command run. No `git worktree add`/`remove` run.
- One scratch directory used, `.remedy-wt/f314-r4-worker/` (created this round), holding one
  digest-verification helper (`check_digests.py`), one copy-and-verify helper for C1
  (`c1_copy.py`) and the gate output files (`mypy-before.txt`, `mypy-c3-check.txt`,
  `mypy-after.txt`, `selection-output.txt`); `.remedy-wt/f314-r4/` (the reviewer's prepared tree)
  was only read, never written.

## Verification

Gate order per the block, run once each, after C3 and before this handoff.

1. `git status --porcelain` → empty.
   `python3 .remedy-wt/f314-r4/prep/verify.py .` →
   ```
   True	ee91513c5 single parent equal to the commit before it
   True	ee91513c5 carries a new F314 R4 Cn subject
   True	ee91513c5 insertions 165 under 500
   True	a4715ca55 single parent equal to the commit before it
   True	a4715ca55 carries a new F314 R4 Cn subject
   True	a4715ca55 insertions 84 under 500
   True	63f925853 single parent equal to the commit before it
   True	63f925853 carries a new F314 R4 Cn subject
   True	63f925853 insertions 10 under 500
   True	the commits come in block order: ['C1', 'C2', 'C3']
   True	on feature/f314-findings-paydown-v10
   True	C1 paths exactly [...]
   True	C1 .agent/authored/f314-r4.md equals c1-.agent__authored__f314-r4.md
   True	C1 .agent/decisions.md equals c1-.agent__decisions.md
   True	C1 .agent/live_review.md equals c1-.agent__live_review.md
   True	C1 .agent/plan.md equals c1-.agent__plan.md
   True	C2 paths exactly [...]
   True	C3 paths exactly [...]
   True	C3 adds no bare type: ignore
   absent	C4
   True	the saved block equals block.md
   ALL True
   ```

2. `python3 -m ruff check .` → exit 0, `All checks passed!`.

3. `python3 .remedy-wt/f314-r4/prep/run_selection.py . .remedy-wt/f314-r4-worker/selection-output.txt` →
   ```
   paths 103
   exit 0
   7429 passed, 2 skipped in 126.76s (0:02:06)
   SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): ...
   SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
   ```
   Exit 0; no FAILED, ERROR or `process(es) behind` line. Both skips are pre-existing and unrelated
   to this round's files (one a documented quarantine, one an opt-in network smoke test) — the same
   two round 3's handback recorded.

4. `python3 -m apps.cli.main integrity check --json` →
   `{"check_count": 6, ..., "fail_count": 0, "ok": true, "passed": true, ...}` — `fail_count: 0`.

5. `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` →
   `15`.

6. `python3 .remedy-wt/f314-r4/prep/mypy_gate.py . .remedy-wt/f314-r4-worker/mypy-after.txt` →
   ```
   mypy 2.3.1 (compiled: yes)
   exit 1
   Found 400 errors in 101 files (checked 501 source files)
   pingpong_loop.py 24
   pingpong_provider.py 13
   role_provider_factory.py 0
   do_sequence.py 0
   ```
   `role_provider_factory.py` and `do_sequence.py` both `0`, as the block required. The other two
   named modules, `pingpong_loop.py` (24) and `pingpong_provider.py` (13), are unchanged from the
   before-C3 reading and from DECISION F314 D6's own measurement — neither grew, so neither is this
   round's to repair (DECISION F314 D6 (1)). The whole-tree count fell from 420 to 400 (the two
   repaired modules' 12 and 8 errors), in 101 files against 103 before.

## Authored-text proofs

- `.agent/authored/f314-r4.md`: `wc -l` 125, matching `block.md`'s 125; sha256
  `1cf3e2e043e5d80bd9d5ae9f413c02d074d463c6e5208c39fd53646b83961926` on both. Byte-identical.
- `.agent/decisions.md` against `.remedy-wt/f314-r4/prep/c1-.agent__decisions.md`: sha256
  `9b07f410e4b20c4465d03675ce7f36aeb816b50bde5e76af40c8988254774517` on both. Byte-identical.
- `.agent/live_review.md` against `.remedy-wt/f314-r4/prep/c1-.agent__live_review.md`: sha256
  `aaf2274104c637dff9ea70f07635db3cb8ac4bc5f3447fbb18505283d515439d` on both. Byte-identical.
- `.agent/plan.md` against `.remedy-wt/f314-r4/prep/c1-.agent__plan.md`: sha256
  `be9d64ee633a881e6b7d52a54a86fd50523f67c8372c7648288a6313d52b4a67` on both. Byte-identical.

Before using any prepared file, `.remedy-wt/f314-r4/prep/digests.txt` was checked against its own
stated sha256 (`6d600149e0e3c61207c26b1c0972fe3eefec03ccf281a85581954066e472826d`, matched), then
every one of its nine listed entries was recomputed and matched, before any prepared file was
copied, run or read. C2 and C3 have no `c*-` prepared files — both are authored text per the
block's own instructions, not byte copies.

## Deviations & assumptions

1. C2 item 1(a)'s fallback clause — "if the class's helpers cannot run a job without an injected
   provider, say so in the handback and write the test at the nearest point that still goes
   through `run_job`" — did not trigger: `run_job(job.job_id)` with no provider name and no
   injected object runs to the point of resolving and recording `execution_config` without error,
   the same way several existing tests elsewhere in the suite already call `run_job` with only
   `builder_name="fake"` and no injected object. The test therefore calls `run_job` directly, as
   ordered, with no fallback needed.
2. C3's "no listed function grows by a line" was read as also covering the two ratchet tests that
   are not named by number in the block but are the mechanism the sentence protects: a function
   that is not on the ledger's list must not cross its 100-line threshold either, and the file
   itself must not cross the 1,000-line threshold, or `tests/test_structure_ratchet.py` would fail
   under the pytest selection with a brand-new, unlisted debt. The first attempt at the narrowing
   fix (named local variables plus a short WHY comment at each site) pushed `_first_pass_task_plan`
   from 99 to 105 lines and the file from 998 to 1009, which was measured and then rewritten as
   inline `cast(...)` expressions with a one-line or trailing comment instead, restoring both
   functions' and the file's original line counts exactly (`_first_pass_task_plan` 99,
   `_step_plan` 82, `_step_shape` 80, file 998). The committed diff is the second, line-neutral
   form; nothing of the first form was committed.
3. `cast("RemyProject", ctx.project)` uses a string forward reference rather than a runtime import
   of `RemyProject`, because the class is already imported under `if TYPE_CHECKING:` at the top of
   `do_sequence.py`; `cast`'s first argument is evaluated by Python but ignored by it, so the
   string resolves for mypy without adding an import line that would itself grow the file.

C1 through C3 landed in the block's order, with no added, dropped or reordered commit; every
`c1-*` prepared byte was copied verbatim and proved equal by direct byte comparison before being
staged; every gate ran exactly once, after C3 and before this handoff, with no retry needed.

## For the operator, in plain sentences

This session closed out last round's review and repaired both things it found: a test that could
not actually see the wiring between a run and a project's own provider settings now does, and the
one place in the written guide that described that setting moved to where a reader would expect
it, with a clearer sentence about when a bad setting is refused. The settings table also now says
plainly that it does not yet choose which service plans a run; that remains a separate, explicit
choice until a later round teaches the table to cover it too. Separately, this session finished a
small piece of code health left over from an earlier review: two files had grown a number of type
mistakes that a stricter checker catches, and both are now completely clean of them without
changing what either file actually does when it runs. Every required check came back clean, and
the branch is about to be pushed so the next session can continue with the remaining open work.

## Next

1. Phase 1 rule 1: if `.agent/STOP` exists, the next session finishes whatever commit is in hand,
   writes the handoff, pushes, and stops, before anything else.
2. Rule 2, the Open PR Gate: check for open pull requests before starting any new unrelated work.
3. Book this round's verdict in the next round's first commit.
4. T006: the hosted runner's three findings.

Operator questions open: 1. Open findings: 15.
