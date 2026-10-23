# Handback — F314 "Findings paydown v10," round 3

## Session

SESSION 1 of feature F314 · round 3 · rounds so far 3

Context self-assessment: this session booked round 2's FAIL verdict, resolved R-1443, registered
R-1445 and DECISION F314 D4, repaired R-1445 with a new gauntlet test and the rest of R-1444 by
renaming two fixture strings, then built T004's first half — a project's `[roles]` table, read for
the builder and the reviewer below an explicit option or a continued job's own persisted record —
reading every touched file whole before editing it and running every gate exactly once, after the
last commit.

State block:
Feature F314 (claimed `[~]`), branch `feature/f314-findings-paydown-v10`, base `68ce5e1ed`.
Fortschritt: ~35 % (T001 to T003 landed, T004 half · T005 to T008 open) — Schätzung

## Range

Review of `68ce5e1ed`..HEAD.

## Commits

### fb2ae3316 F314 R3 C1: book F314 R2, resolve R-1443, register R-1445, DECISION F314 D4
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f314-r3.md` | +146/-0 | NEW FILE; byte copy of this round's block, `block.md` |
| `.agent/decisions.md` | +10/-0 | DECISION F314 D4 appended |
| `.agent/live_review.md` | +8/-0 | F314 round 2's FAIL gate entry, R-1443's resolution, R-1444's recurrence note and R-1445 appended |
| `.agent/plan.md` | +7/-7 | rewritten for F314 round 3 |

All four paths are byte copies of the reviewer's prepared `c1-*` files; gate 1's `verify.py` and a
direct sha256 comparison (see Authored-text proofs) confirm each equality.

### ecfa045ce F314 R3 C2: the gauntlet test sees what run_order hands the order seam, and the runner's fixture names no tier (R-1445, R-1444)
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_gauntlet_runner.py` | +15/-0 | R-1445: `Recorder` gains `seen_accept_order`, its `_accept_order` records `(project_id, workspace, goal)` into it, and a new test asserts that tuple equals `("p-1", seen_repo_path, order.goal)` for one run through `run_order`, with `seen_repo_path` not `None` |
| `tests/orchestration/test_self_use_runner.py` | +2/-2 | R-1444's rest: `_order_item`'s `why` and `provenance` no longer name the deleted order tier |

Authored to the specification under C2, not byte copies — no `c2-*` prepared files exist to compare
against (the block's own header marks C2 as text the worker writes).

### 1519d51fd F314 R3 C3: a project's roles table chooses the builder and the reviewer below an explicit option (R-1326)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/project_roles.py` | +93/-0 | NEW FILE: `PROJECT_ROLES_KEYS`, `ProjectRolesError` and `read_project_roles`, reading `[roles]` of `.remedy/config.toml` with `tomllib`/`tomli`, answering `{}` for no repository, file or table, and refusing a bad key, a bad value, an unknown provider, a non-writing builder or an unknown planner |
| `tests/orchestration/test_project_roles.py` | +89/-0 | NEW FILE: one test per answer (absent file, no table, all three keys) and per refusal (unreadable TOML, `roles` not a table, unknown key, non-string/empty value, unknown builder, unknown reviewer, non-writing builder, unknown planner) |
| `packages/orchestration/execution_config.py` | +34/-7 | `_resolve_role_provider` added beside `_resolve_cfg` (DECISION F314 D4 WHY comment); `resolve_job_execution_config` gains `repo_path`, reads `read_project_roles(repo_path)`, and the builder's and the reviewer's provider resolve through the new helper: explicit > persisted > injected object > table (`roles`) > product default; docstring updated |
| `packages/orchestration/run_manifest.py` | +1/-1 | `_VALID_SOURCES` gains `"roles"` |
| `packages/orchestration/pingpong_job.py` | +1/-1 | `run_job`'s call to `resolve_job_execution_config` gains `repo_path=job.repo_path` on the existing `max_tasks=max_tasks,` line; the function's own line count is unchanged |
| `tests/orchestration/test_execution_config.py` | +52/-0 | `TestTheProjectRolesTable`: the table answers both roles with source `roles`; an explicit name, a persisted record and an injected provider object each beat the table; no table leaves the answer and source unchanged; a definition whose builder source is `roles` validates |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | `packages.orchestration.project_roles`, which `test_import_reachability.py` asked for |
| `docs/guides/do-run-v1.md` | +14/-0 | one paragraph beside the provider flags naming the `[roles]` table, its precedence and its refusals, with a three-line TOML example |

`run_job` stays at its prior line count — the one-line change replaces `max_tasks=max_tasks,` with
`max_tasks=max_tasks, repo_path=job.repo_path,` in place, and gate 1's ratchet reading confirms it.
285 insertions, under the 500-line cap, so no split into C3a/C3b was needed.

### this commit — F314 R3 C4: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | n/a (self-reference; R-0149 pattern) | this handback, rewritten per `docs/agents/handback_template.md` |

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `fb2ae3316`, four paths, each byte-equal to its prepared `c1-*` file |
| C2 | done | `ecfa045ce`, exactly the two named paths, authored to spec |
| C3 | done | `1519d51fd`, exactly the eight named paths; `run_job` unchanged in line count |
| C4 | done | this commit, `.agent/handoff.md` only |
| Gate 1 (`verify.py`) | done | every line `True`, `C4` read `absent`, last line `ALL True` |
| Gate 2 (`ruff check .`) | done | `All checks passed!` |
| Gate 3 (pytest selection) | done | exit 0, `4171 passed, 2 skipped in 32.01s`, no FAILED/ERROR/`process(es) behind` line |
| Gate 4 (integrity) | done | `"fail_count": 0` |
| Gate 5 (open finding ids) | done | `14` |
| Push | done | see External actions / the reply after this handback |

## External actions

- `git push origin feature/f314-findings-paydown-v10` — to run immediately after this commit,
  carrying `fb2ae3316`, `ecfa045ce`, `1519d51fd` and this handback's own commit; see the reply for
  the push's own result. The branch already tracks `origin/feature/f314-findings-paydown-v10`.
- No PR created, edited or merged by this session (none is ordered by this round's block; no open
  PR exists on this branch). No `gh` command run. No `git worktree add`/`remove` run.
- One scratch directory used, `.remedy-wt/f314-r3-worker/`, holding only two Python helper scripts
  (`c1_copy.py`, the digest-verification-and-byte-copy helper for C1, and `probe_project_roles.py`,
  used only to exercise `read_project_roles`'s answers and refusals while writing it) and gate 3's
  raw output file; `.remedy-wt/f314-r3/` (the reviewer's prepared tree) was only read, never
  written.

## Verification

Gate order per the block, run once each, after C3 and before this handoff.

1. `git status --porcelain` → empty.
   `python3 .remedy-wt/f314-r3/prep/verify.py .` →
   ```
   True	fb2ae3316 single parent equal to the commit before it
   True	fb2ae3316 carries a F314 R3 Cn subject
   True	fb2ae3316 insertions 171 under 500
   True	ecfa045ce single parent equal to the commit before it
   True	ecfa045ce carries a F314 R3 Cn subject
   True	ecfa045ce insertions 17 under 500
   True	1519d51fd single parent equal to the commit before it
   True	1519d51fd carries a F314 R3 Cn subject
   True	1519d51fd insertions 285 under 500
   True	the commits come in block order: ['C1', 'C2', 'C3']
   True	one commit per tag, C3 may be two
   True	C3 is at most two commits
   True	on feature/f314-findings-paydown-v10
   True	C1 paths [...] within [...]
   True	C1 .agent/authored/f314-r3.md equals c1-.agent__authored__f314-r3.md
   True	C1 .agent/decisions.md equals c1-.agent__decisions.md
   True	C1 .agent/live_review.md equals c1-.agent__live_review.md
   True	C1 .agent/plan.md equals c1-.agent__plan.md
   True	C2 paths [...] within [...]
   True	C3 paths [...] within [...]
   True	pingpong_job.py changes exactly the one line
   absent	C4
   True	the saved block equals block.md
   ALL True
   ```

2. `python3 -m ruff check .` → exit 0, `All checks passed!`.

3. `python3 .remedy-wt/f314-r3/prep/run_selection.py . .remedy-wt/f314-r3-worker/selection-output.txt` →
   ```
   paths 94
   exit 0
   4171 passed, 2 skipped in 32.01s
   SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): ...
   SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
   ```
   Exit 0; no FAILED, ERROR or `process(es) behind` line. Both skips are pre-existing and unrelated
   to this round's files (one a documented quarantine, one an opt-in network smoke test) — the same
   two round 2's handback recorded.

4. `python3 -m apps.cli.main integrity check --json` →
   `{"check_count": 6, ..., "fail_count": 0, "ok": true, "passed": true, ...}` — `fail_count: 0`.

5. `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` →
   `14`.

## Authored-text proofs

- `.agent/authored/f314-r3.md`: `wc -l` 146, matching `block.md`'s 146; sha256
  `f3a9a10dbac1ce5d32b257e87311dcdd6acdbea87a82e3c48066165076f8cd9a` on both. Byte-identical.
- `.agent/decisions.md` against `.remedy-wt/f314-r3/prep/c1-.agent__decisions.md`: sha256
  `42f3c1f2ccc0959a21a3751e5eaf77ec1b66aad4650a366e7c620de1b8f631f9` on both. Byte-identical.
- `.agent/live_review.md` against `.remedy-wt/f314-r3/prep/c1-.agent__live_review.md`: sha256
  `9f502ea6d9dd8ff569f7bd675cc1636619076dc63c9dd296b5f4033dc1fd9428` on both. Byte-identical.
- `.agent/plan.md` against `.remedy-wt/f314-r3/prep/c1-.agent__plan.md`: sha256
  `d24362093a211bb546f89ae3940c7a19368770df55c7f2d483314dc271a68fbe` on both. Byte-identical.

Before using any prepared file, `.remedy-wt/f314-r3/prep/digests.txt` was checked against its own
stated sha256 (`3a20abf371c61dc3093893e98af04e623cc893578decd056e2cf49d5c2018e07`, matched), then
every one of its eight listed entries was recomputed and matched, before any prepared file was
copied, run or read. C2 and C3 have no `c*-` prepared files — both are authored text per the
block's own instructions, not byte copies.

## Deviations & assumptions

1. `project_roles.py`'s three name-set imports (`ROLE_PROVIDER_NAMES`, `PLANNER_PROVIDERS`,
   `non_writing_provider_refusal`) are imported inside `read_project_roles`'s body unconditionally,
   rather than first attempting a module-level import and falling back only if it proved circular.
   This matches `execution_config.py`'s own existing convention for the same kind of import
   (`role_config`, `provider_timeouts`, `config`, `claude_cli_command` are all imported inside their
   functions "on purpose"), and a probe import of the module showed no cycle either way, so the
   choice costs nothing and removes any risk.
2. C3 item 5's instruction to build a roles-sourced definition "the way that file's existing source
   test builds one, if it has one; otherwise read `run_manifest.py` for the smallest valid
   definition" found no existing test in `test_execution_config.py` that builds a definition with a
   non-default source word. `test_a_roles_sourced_builder_validates` instead reuses that file's own
   `_Job`/`ecm.ExecutionConfig()` helper already used by `TestValidationOfTheFourKeys`, with
   `builder_source="roles"` substituted by `dataclasses.replace` — the same shape, not a hand-built
   dict copied from `run_manifest.py`'s field constants, since the existing helper already produces
   a complete, valid definition.
3. `execution_config.py`'s module docstring still lists only `default_role_provider_name` and
   `_resolve_cfg` as "the two field resolvers," not the new `_resolve_role_provider`. The block's
   item 2 ordered the docstring of `resolve_job_execution_config` updated (done), not the module
   docstring; left as ordered rather than widened.

C1 through C3 landed in the block's order, with no added, dropped or reordered commit; every
`c1-*` prepared byte was copied verbatim and proved equal by direct byte comparison before being
staged; every gate ran exactly once, after C3 and before this handoff, with no retry needed;
`tests/orchestration/import_reachability_allowlist.txt` needed one line, which C3 added, as the
block allowed.

## For the operator, in plain sentences

This session closed out last round's review: it fixed a test that could not actually see one of
the gauntlet's own internal handoffs, and renamed two leftover sentences that still described a
practice no longer in the code. It then opened a piece of the next capability: a project can now
name its own preferred builder and reviewer once, in a small settings file at the project's root,
instead of a person or another program having to repeat that choice on every single request. A
setting made this way still loses to an explicit choice on the command line or to a request that is
already underway with its own choice recorded, and a settings file naming a provider that does not
exist, or a builder that cannot actually make changes, is refused with a plain explanation rather
than silently ignored. Every required check came back clean, and the branch is about to be pushed
so the next session can continue with the remaining open work — starting with teaching the planning
step to read the same settings file.

## Next

1. Phase 1 rule 1: if `.agent/STOP` exists, the next session finishes whatever commit is in hand,
   writes the handoff, pushes, and stops, before anything else.
2. Rule 2, the Open PR Gate: check for open pull requests before starting any new unrelated work.
3. Book this round's verdict in the next round's first commit.
4. T004's second half: the planner reads `[roles]`.

Operator questions open: 1. Open findings: 14.
