# Handback — F055 round 1 — claim, the catalog step, and T001 (the mode, its refusals, guarantees)

## Session

SESSION 1 of feature F055 · round 1 · rounds so far 1

Context self-assessment: C1 to C3 landed clean on the first attempt; C4 needed amendment 1
(the reviewer's own slip, not mine) to add the generated client-interface page and fix the
rehearsal's loop shape, both applied cleanly once read; C5's ten tests passed on the first
run; all six gates passed on the first run; context held comfortably throughout the round.

Fortschritt: ~35 % (claim, the catalog step and T001 landed · T002 and T003 open) — Schätzung

## Range

Review of `eea4f5cfe`..`75d2a814f` (then this commit).

## Commits

### `980fb1348` F055 R1 C1: claim F055, book F308 R6, re-head the ledger, DECISION F055 D1
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f055-r1.md` | +223/-0 | byte copy of `block.md` |
| `.agent/context.md` | +8/-11 | byte copy of `dry-context.md` |
| `.agent/decisions.md` | +12/-0 | byte copy of `dry-decisions.md` (DECISION F055 D1 appended) |
| `.agent/live_review.md` | +21/-21 | byte copy of `dry-live_review.md` (re-head + F308 R6 booked) |
| `.agent/plan.md` | +13/-9 | byte copy of `dry-plan.md` |
| `docs/roadmap/STATUS.md` | +1/-1 | byte copy of `dry-STATUS.md` (F055 `[ ]` → `[~]`) |

### `0d112fbef` F055 R1 C2: the catalog's do group moves to command_catalog_do.py (structure step)
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/command_catalog.py` | +2/-50 | the `do` group replaced by `*DO_COMMANDS,` + import |
| `apps/cli/command_catalog_do.py` | +65/-0 | NEW: `DO_COMMANDS`, the moved block unchanged |
| `docs/system/structure-ledger-v1.md` | +3/-2 | row 2460→2412; step (5) sentence |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | `apps.cli.command_catalog_do` |
| `tests/test_structure_ratchet.py` | +1/-1 | `MAX_FILE_LINES` 73649→73601 |

### `0792744c6` F055 R1 C3: the boundaries of _cmd_do_order and _cmd_do (structure page)
| Path | +/- | Reason |
|---|---|---|
| `docs/system/structure-ledger-v1.md` | +12/-0 | `src-boundaries.md` inserted verbatim |

### `0a6fb693a` F055 R1 C4: remedy do --rehearse stops before any job runs, with its refusals
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f055-r1-amend1.md` | +19/-0 | byte copy of `amend1.md` (amendment 1) |
| `apps/cli/command_catalog_do.py` | +1/-0 | `--rehearse` `ArgDef` after `--plan-only` |
| `apps/cli/commands/do_cmd.py` | +11/-11 | `rehearse` param + call, line-neutral (see Verification) |
| `apps/cli/commands/do_rehearsal_refusals.py` | +37/-0 | NEW: `refuse_rehearsal_conflicts` |
| `docs/guides/do-run-v1.md` | +13/-0 | `src-guide.md` inserted before `## JSON output` |
| `docs/system/machine-client-contract-v1.md` | +1/-0 | amendment 1: regenerated, one new `--rehearse` row |
| `packages/orchestration/do_context.py` | +2/-0 | `DoContext.rehearse` + comment |
| `packages/orchestration/do_rehearsal.py` | +26/-0 | NEW: `stop_walk_for_rehearsal` (single loop, amendment 1) |
| `packages/orchestration/do_sequence.py` | +4/-0 | `ctx.rehearse` branch, import, docstring sentence |
| `tests/orchestration/import_reachability_allowlist.txt` | +2/-0 | the two new modules, sorted |

### `75d2a814f` F055 R1 C5: the run's side-effect counters and the rehearsal's guarantees
| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_rehearsal.py` | +227/-0 | NEW: scenarios (a) to (e) of C5 |
| `tests/run_side_effect_counters.py` | +94/-0 | NEW: the four reusable counters |

### (this commit) F055 R1 C6: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | — |

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` (Open PR Gate check,
  read-only), run before C0: `[]` — no open pull request, matching the block's own claim.
- `git checkout -b feature/f055-rehearsal` from `main` at `eea4f5cfe` (C0).
- Push after C6 follows this commit: `git push -u origin feature/f055-rehearsal`; its outcome is
  reported in the session's final reply only, per the write-once rule — it does not exist yet
  when this file is written.
- No worktree added or removed beyond the pre-existing `.remedy-wt/f055-r1-worker/` scratch
  directory the block named for copy/hash/measure scripts; nothing under it is tracked.
- No `gh pr merge`, `gh pr edit`, `gh pr create`, no STATUS edit beyond C1's claim line, no ledger
  rotation, no self-use run, no provider call beyond the fake providers C5's tests drive — none
  ordered by this block.

## Verification

**Block verified before anything else**: `block.md` 223 lines /
`d346a4c7dd24b964db03428b34e3a536bb71cab89cb35fe7f6224da4122de013` — matched the prompt exactly.
`verify.py` (original) `be7605cfd8bfd8d83bfa4af30980c6fbe2cee082e241ed5dd2199432329c66a8`,
`run_selection.py` `aca3c3bba1921d12b1d6d57e9d7b518daa64c3d0ec98428c70da8e09b770f389`,
`selection.txt` `3d1266cb8bbd9936df04d768225e6f06101aeb1b8f3d66f70579f4fed4d6e99e`,
`src-boundaries.md` `383731f46aa67ce80eaf997b4ca34987294f9843a1d45747eea49cdde04d4d0a`,
`src-guide.md` `24cc8d2f1a0bcf88a78ae02878e324b11485335db0332685c43ef8a0d2b94c65`,
`dry-STATUS.md` `47b3986238547247ba847004ca491ccae1fe43e31756e13866d44516f0745fe8`,
`dry-live_review.md` `82c622885d7dd9e39a894dff6f66809d39b23b0d77c66cf0a1bca21979569716`,
`dry-decisions.md` `5caf999f7d4092cdc166d45448edc3e12d93e6668e42845fc1784ff84e01ebe8`,
`dry-plan.md` `8ad9518139905b1a948f9209526ba798971a51bc5922879ea63102f7dd6cb9fd`,
`dry-context.md` `103f937289c0871d639c74df79f5633344098dd5a3aa63bd336d5ee6bcc9e110` — all matched.
**Amendment 1**, read mid-round: `amend1.md` 19 lines /
`5e326ea59220e313034bbc71da89ce897fb0dab73d00a767e452525658c2f544` — matched. Replacement
`verify.py` 145 lines / `22d207aae31b17afedb83f3d960be1b2c8b852e352007c8049ddbc67a65ca57f` —
matched.

**C4's line-neutral edit of `do_cmd.py`**, measured with
`packages.orchestration.structure_measure.measure_repository` (not `wc -l`) after the edit:
`_cmd_do` 110 lines, `_cmd_do_order` 190 lines, the file 1024 lines — all three equal their
ledger rows, confirmed again after amendment 1's rewording of `do_rehearsal.py`'s docstring
(which does not touch `do_cmd.py`).

**Gate 1** — `git status --porcelain` empty, then
`python3 /home/decodeux/Repos/remedy/.remedy-wt/f055-r1/prep/verify.py /home/decodeux/Repos/remedy`:
```
True 980fb1348 has the single parent eea4f5cfe
True 980fb1348 subject begins 'F055 R1 C<n>:' (F055 R1 C1: claim F055, book F308 R6, re)
True 0d112fbef has the single parent 980fb1348
True 0d112fbef subject begins 'F055 R1 C<n>:' (F055 R1 C2: the catalog's do group moves)
True 0792744c6 has the single parent 0d112fbef
True 0792744c6 subject begins 'F055 R1 C<n>:' (F055 R1 C3: the boundaries of _cmd_do_or)
True 0a6fb693a has the single parent 0792744c6
True 0a6fb693a subject begins 'F055 R1 C<n>:' (F055 R1 C4: remedy do --rehearse stops b)
True 75d2a814f has the single parent 0a6fb693a
True 75d2a814f subject begins 'F055 R1 C<n>:' (F055 R1 C5: the run's side-effect counte)
True the commit C1 exists
True the commit C2 exists
True the commit C3 exists
True the commit C4 exists
True the commit C5 exists
[... 6 C1-path-equality lines, all True, plus the C1/C2/C3/C4/C5 path-set and content checks ...]
ALL True
```
(34 checks total, every one `True`; the full transcript is reproducible from the command above.)

**Gate 2** — `python3 -m ruff check` over every Python file C2, C4 and C5 touched (10 files:
`command_catalog.py`, `command_catalog_do.py`, `do_cmd.py`, `do_rehearsal_refusals.py`,
`do_context.py`, `do_rehearsal.py`, `do_sequence.py`, `run_side_effect_counters.py`,
`test_rehearsal.py`, `test_structure_ratchet.py`): `All checks passed!`

**Gate 3** (run exactly once, after C5) —
`python3 /home/decodeux/Repos/remedy/.remedy-wt/f055-r1/prep/run_selection.py /home/decodeux/Repos/remedy /home/decodeux/Repos/remedy/.remedy-wt/f055-r1-worker/selection-output.txt`:
```
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) — pre-existing, unrelated
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in (REMEDY_INSTALL_SMOKE=1)
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
91 paths
4394 passed, 3 skipped in 89.44s (0:01:29)
exit 0
```
No FAILED or ERROR line, no line naming a process left behind.

**Gate 4** — `python3 -m apps.cli.main integrity check --json`:
```
{"check_count": 6, "checks": [{"message": "handlers=188", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```

**Gate 5** —
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`:
```
['R-1246', 'R-1276', 'R-1277', ..., 'R-1313']
```
39 ids: `R-1246` then `R-1276` to `R-1313` in order, as required.

**Gate 6** — `python3 -m apps.cli.main do "rehearsal refusal probe" --rehearse --yes --json`:
```
exit 2
{"error": "invalid_argument", "message": "--rehearse leaves the plan's approval open for you to answer, and --yes would approve it unattended. Nothing was run.", "ok": false, "schema_version": 1}
```
`git status --porcelain` empty immediately after — the refusal wrote nothing.

## Authored-text proofs

`.agent/authored/f055-r1.md` against `block.md`: byte-identical, sha256
`d346a4c7dd24b964db03428b34e3a536bb71cab89cb35fe7f6224da4122de013`, confirmed twice — once by my
own copy script and again independently by `verify.py`'s Gate 1 (`git show <C1>:<path>` compared
to the prep file's bytes). `.agent/authored/f055-r1-amend1.md` against `amend1.md`: byte-identical,
sha256 `5e326ea59220e313034bbc71da89ce897fb0dab73d00a767e452525658c2f544`, same double
confirmation. The five `dry-*.md` copies applied in C1 (`STATUS.md`, `live_review.md`,
`decisions.md`, `plan.md`, `context.md`) were each confirmed byte-equal by sha256 at copy time and
again by Gate 1's per-path check. No other reviewer-authored text was applied this round.

## Deviations & assumptions

1. **An edit drafted on `main` before C0.** While working out the exact line-neutral join
   arithmetic for `do_cmd.py`'s C4 edit, I wrote and measured it directly in the checkout while
   still on `main`, before running C0. Caught via `git status --porcelain` before any commit:
   `main` was still clean at `eea4f5cfe` (confirmed with `git rev-parse HEAD`), so I stashed the
   change (`git stash push -u`), ran C0 for real, then popped the stash onto the new branch before
   any commit existed. No commit was ever made on `main`, and the stashed content is exactly what
   later became part of C4. Corrected before it could affect anything.
2. **Amendment 1, mid-round.** Before committing C4 I ran most of `selection.txt` as a precaution
   (not a formal gate) and found two failures in `tests/cli/test_client_interface.py`: the
   generated page `docs/system/machine-client-contract-v1.md` goes stale the moment `--rehearse`
   is added to the catalog, and the original `verify.py`'s C4 path check (extra paths must start
   with `tests/`) made it impossible to add that page to C4 without failing Gate 1 — a genuine
   contradiction between the block and the code. I stopped before committing C4 and reported it.
   The coordinator sent amendment 1 (`amend1.md`, verified 19 lines /
   `5e326ea59220e313034bbc71da89ce897fb0dab73d00a767e452525658c2f544`) adding the page and
   `.agent/authored/f055-r1-amend1.md` to C4's paths, replacing `verify.py` (verified 145 lines /
   `22d207aae31b17afedb83f3d960be1b2c8b852e352007c8049ddbc67a65ca57f`), and fixing
   `stop_walk_for_rehearsal` to a single loop. I applied all three changes, regenerated the page
   with exactly the named command, reran the diagnostic sweep clean, and committed C4.
3. **`do_rehearsal.py`'s module docstring rewritten once more**, after amendment 1 but before
   committing: my first wording, `` `remedy do --rehearse` plans an order... ``, tripped
   `tests/cli/test_advertised_commands.py::test_every_group_only_advertisement_reaches_a_command`
   (it reads as an unrunnable group-only CLI invocation — `do` with nothing but a flag — because
   the scanner does not parse markdown). Reworded to `` `remedy do`'s `--rehearse` flag plans an
   order... ``, same meaning, same line count, scanner-safe; confirmed with the full
   `test_advertised_commands.py` file (14 passed) before folding it into C4.
4. **C5, test (b): `count_applicator_calls` is not asserted.** A bare `remedy do "<order>"`
   without `--apply` never reaches the apply step (`apply_job`), the patch-hunk path
   (`apply_patch_intent`, only reachable through `remedy patch apply`), or the non-worktree
   copy-mode fallback (`_strict_apply_to_workspace`; the fixture's job takes the worktree path,
   `_verify_in_place_apply`, instead). All three stay at zero for a real run too, correctly, so
   that counter is left out of the "moves" assertions in test (b) with this reason, exactly as
   the block allowed; `count_role_provider_builds` and `count_worktree_creations` are asserted
   instead, plus the snapshot differing overall.
5. **The block's own text names `apps.cli.main.main([...])`** as what C5's tests should drive,
   but then says "as `tests/cli/test_do_sequence_cli.py` does" — that file drives
   `apps.cli.grouped.main([...])` (`apps.cli.main.main` takes no `argv` parameter at all; it reads
   `sys.argv`). I followed the working precedent file and used `apps.cli.grouped.main`, noting
   the mismatch here rather than silently resolving it.

No other departure from the block's ordered sequence.

## For the operator, in plain sentences

This round claimed the rehearsal feature, moved one group of the command catalog into its own
file as a structural step, wrote down two function boundaries the structure page was missing,
and built the first slice of the rehearsal mode: a flag that plans an order and stops before any
job runs, its refusals when combined with a flag that would approve, apply, commit or push, and
test utilities proving a rehearsal truly builds nothing, applies nothing and creates no worktree
while a real run does. One blocker came up mid-round — a generated reference page the original
instructions forgot to list — and the coordinator sent a short fix for it, which is now applied
and verified. All six checks the round requires came back clean. Two more rounds remain before
this feature closes: the rehearsal's own rendered report, then reusing a rehearsed plan for a
real run.

## Next

1. Phase 1 rule 1: `.agent/STOP` — absent at this handoff.
2. Rule 2, the Open PR Gate: no pull request is open for this branch yet.
3. Book round 1's verdict in the next round's first commit.
4. T002, under DECISION F055 D2.

Operator questions open: 0.
Open findings: 39 (R-1246 and R-1276 to R-1313, all owned by F307).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | branch created at `eea4f5cfe`, confirmed before any write |
| C1 | done | Gate 1 `ALL True`; 278 insertions |
| C2 | done | structure ratchet green; 72 insertions |
| C3 | done | boundaries inserted exactly; 12 insertions |
| C4 | done | amendment 1 applied; line-neutral confirmed; 116 insertions |
| C5 | done | 10/10 tests pass; 321 insertions |
| C6 | done | this commit |
| Gate 1 | done | `ALL True` |
| Gate 2 | done | `All checks passed!` |
| Gate 3 | done | 4394 passed, 3 skipped, exit 0, run once |
| Gate 4 | done | `fail_count` 0 |
| Gate 5 | done | 39 ids, in order |
| Gate 6 | done | exit 2, `invalid_argument`, sentence A |
