# Handback — F055 round 3 — book round 2, resolve R-1316, register and repair R-1317, land T003

## Session

SESSION 1 of feature F055 · round 3 · rounds so far 3

Context self-assessment: C1 to C5 landed clean on the first attempt; gate 1's first run (before
the amendment) came back red on two path-allowlist gaps and a source-contiguity check the
original `verify.py` missed, I stopped before C6 and reported it rather than routing around it,
the coordinator sent amendment 1, and after it widened the allowlist and fixed the check every
gate came back green on the one run that counts.

Fortschritt: ~80 % (T001 to T003 landed · the closure open) — Schätzung

## Range

Review of `20630636b`..`93c397422` (then this commit).

## Commits

### `47eb42d3e` F055 R3 C1: book round 2, resolve R-1316, register R-1317, DECISION F055 D3
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f055-r3.md` | +167/-0 | NEW: byte copy of `block.md` |
| `.agent/decisions.md` | +12/-0 | byte copy of `dry-decisions.md` (DECISION F055 D3 appended) |
| `.agent/live_review.md` | +6/-0 | byte copy of `dry-live_review.md` (round 2 booked, R-1316 resolved, R-1317 registered) |
| `.agent/plan.md` | +6/-7 | byte copy of `dry-plan.md` |
| `.agent/prose_slips.md` | +1/-0 | byte copy of `dry-prose_slips.md` |

### `aa105b063` F055 R3 C2: the boundaries of _cmd_job_run and _cmd_status (structure page)
| Path | +/- | Reason |
|---|---|---|
| `docs/system/structure-ledger-v1.md` | +14/-0 | `src-boundaries.md` inserted after the `_cmd_do` bullet |

### `f1b4a0310` F055 R3 C3: remedy job run refuses a plan that is not approved (R-1317)
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/job_run_refusals.py` | +29/-0 | NEW: `refuse_unapproved_job_run` — exit 3, `plan_awaiting_approval` or `plan_rejected` |
| `apps/cli/commands/do_cmd.py` | +6/-6 | `_cmd_job_run` calls the refusal after the cancelled-job refusal; line-neutral (205) via joining `_resolve_cli_role_configs`'s kwargs |
| `apps/cli/command_catalog.py` | +1/-1 | `job.run` gains `exit_codes=(0, 1, 2, 3),` on the `may_execute_commands=True,` line |
| `apps/cli/client_interface.py` | +2/-1 | **amendment 1**: `OPERATION_REFUSAL_TOKENS["job.run"]` gains `plan_awaiting_approval`, `plan_rejected` — required by `test_declared_tokens_equal_the_tokens_the_handler_reaches[job.run]` once the catalog declares exit 3 |
| `docs/guides/exit-codes.md` | +1/-0 | **amendment 1**: `remedy job run` row added to the above-the-floor table — required by `test_guide_tables_equal_the_module_and_the_catalog` |
| `docs/system/machine-client-contract-v1.md` | +2/-2 | regenerated via `write_client_interface_page()` |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | `apps.cli.commands.job_run_refusals` added, alphabetically placed — `test_import_reachability.py` asked |

### `ff7f04e12` F055 R3 C4: a moved repository warns at the approval and the run, and status labels a waiting rehearsal
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/do_rehearsal.py` | +27/-1 | NEW: `rehearsal_staleness_warning`, `job_waits_after_rehearsal`; module docstring gains DECISION F055 D3 |
| `apps/cli/commands/decision.py` | +7/-1 | `_consume_plan_approval` prints the staleness warning (when any) to stderr before consuming the approval |
| `apps/cli/commands/do_cmd.py` | +6/-6 | `_cmd_job_run` prints the warning directly after C3's refusal; line-neutral (205) via joining `resolve_job_budgets`'s and `run_job`'s kwargs |
| `apps/cli/commands/status_cmd.py` | +6/-6 | each `by_state` job entry gains `"rehearsed"`; both text lines append `  (rehearsed)`; line-neutral (179) via joining the dict's keys |
| `docs/guides/do-run-v1.md` | +12/-0 | `src-guide.md` inserted before `## JSON output` |
| `apps/cli/client_interface.py` | +1/-1 | **amendment 1**: `ANSWER_KEY_TREES["status.run"]`'s per-job tree gains `"rehearsed": {}` — required by `test_a_real_runs_answers_return_only_keys_the_interface_names` |
| `docs/system/machine-client-contract-v1.md` | +1/-1 | regenerated via `write_client_interface_page()` |

### `93c397422` F055 R3 C5: the rehearsal's real run, its warning, its label and the approval refusal, proved
| Path | +/- | Reason |
|---|---|---|
| `tests/run_side_effect_counters.py` | +25/-0 | NEW: `count_planning_calls`, wrapping `intake.make_structured_call_fn`, `intake.make_provider_call_fn`, `job_plan.plan_job_llm`, `mission_compiler.plan_mission` in place |
| `tests/cli/test_rehearsal.py` | +175/-0 | NEW: scenarios (m) to (q) — approve+run with no second planning call, `--force-mission` on two deliverables, the staleness warning (moved vs. unmoved), R-1317's two refusals, `remedy status`'s label appearing and disappearing |
| `tests/orchestration/test_do_rehearsal.py` | +75/-0 | NEW: unit tests of `rehearsal_staleness_warning` (no record, no recorded head, equal heads, unreadable head, moved head) and `job_waits_after_rehearsal` |

### (this commit) F055 R3 C6: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | rewritten |
| `.agent/authored/f055-r3-amend1.md` | +17/-0 | NEW: byte copy of `amend1.md` |

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` (read-only, checked
  before writing this handback): `[]` — no open pull request.
- No branch created this round: C0 found `feature/f055-rehearsal` already at `20630636b`, matching
  origin, clean, no `.agent/STOP`.
- Push after C6 follows this commit: `git push -u origin feature/f055-rehearsal`; its outcome is
  reported in the session's final reply only — it does not exist yet when this file is written.
- No worktree added or removed beyond the pre-existing `.remedy-wt/f055-r3-worker/` scratch
  directory the block named for copy/hash/measure scripts; nothing under it is tracked.
- No `gh pr merge`, `gh pr edit`, `gh pr create`, no STATUS edit, no ledger rotation, no self-use
  run, no live provider call — none ordered by this block or its amendment. `tests/cli/test_rehearsal.py`
  scenarios (m), (p) and (q) are the real `job run` invocations this round made, through the fake
  builder/reviewer providers the fixture already wires, exactly as the round's other scenarios do.

## Verification

**Block verified before anything else**: `block.md` 167 lines /
`5ecd65e44b895ddf19374cff1cb577395f1edf660657aa2b2d565e4bf5473375` — matched. `verify.py`
(original) `1337645ee58949a7c97ac7e2ac7db6e0a20c7f25487869bf2f2afbb7f7b2fd25`, `run_selection.py`
`aca3c3bba1921d12b1d6d57e9d7b518daa64c3d0ec98428c70da8e09b770f389`, `selection.txt`
`220772443e247923144ff8b8b1b6cbeed7a5e418acb9ca4913f8624ff1ad671e`, `src-boundaries.md`
`ef246e8bf7d98fa8a2eddd9b26005e46e975c7a7d072b7381183738fc73fe7d6`, `src-guide.md`
`826084dd6a09cb2aa365d1ce5faaeee4a29311d52eaaf98cf39fcda65ed80fcf`, `dry-live_review.md`
`a86a03bb0b4b8d7fb0fdce4f5ba992d0c551f1a670f5be1a532ebf338331d832`, `dry-prose_slips.md`
`4301beaf77e77216c673998a48bec489f3a88654dbc48629fe9104c90555b495`, `dry-decisions.md`
`39201560ca657e8ca8211ba8147706d7f55cac0162ce2d4fa0ab86de7607e1fc`, `dry-plan.md`
`1b7670f9c2f4028fd50994ef1a316db98819464fcbe6b8c3af43b9db0bccd8e1` — all matched.
**Amendment 1**, read after gate 1's first (red) run: `amend1.md` 17 lines /
`048396ca226a920f579c1ed704b30f6ff42c1b8619208dd5b8862d3afecea389` — matched. Replacement
`verify.py` 113 lines / `091f47666b4a8d2adcb9e24ac883b62b17190dc9b8269f22f770b4728da879e4` —
matched.

**Gate 1** — `git status --porcelain` empty, then
`python3 /home/decodeux/Repos/remedy/.remedy-wt/f055-r3/prep/verify.py /home/decodeux/Repos/remedy`:
- First run, after C5, with the ORIGINAL `verify.py`, before the amendment — RED:
  ```
  False C3 names its paths; missing [], unexpected ['apps/cli/client_interface.py', 'docs/guides/exit-codes.md']
  False C4 names its paths; missing [], unexpected ['apps/cli/client_interface.py']
  False the warning is authored
  ALL False
  ```
  Every other line (33 of 36) read `True`. Root cause of the first two: declaring `job.run`'s
  exit 3 in the catalog, which the block's own C3 step 3 explicitly orders, forces
  `apps/cli/client_interface.py`'s `OPERATION_REFUSAL_TOKENS` and `docs/guides/exit-codes.md`'s
  table into sync too (both asserted by name-tests the block's own bundle lists), and the
  original `verify.py`'s `ALLOWED` sets for C3/C4 did not name either file. Root cause of the
  third: C4's committed `rehearsal_staleness_warning` wrapped the warning sentence across three
  adjacent string-literal lines (the rendered runtime string was correct and every unit test
  passed), but the original `verify.py` read the source as one contiguous span. Per my standing
  instructions I stopped before C6, pushed nothing, and reported the exact reading (reproduced
  above) rather than routing around it. The coordinator's amendment 1 widened `ALLOWED["C3"]` and
  `ALLOWED["C4"]` to include both files, and changed the warning check to read adjacent string
  literals as one (`re.sub(r'"\s*\n\s*f?"', "", code)`), declaring C1 to C5 as committed and the
  `do_rehearsal.py` wrapping unchanged.
- Second run, after `git checkout -- packages/orchestration/do_rehearsal.py` (discarding my local,
  now-unneeded reformatting) and with the replacement `verify.py` — the one amendment 1 counts —
  GREEN:
  ```
  True 47eb42d3e has the single parent 20630636b
  True 47eb42d3e subject begins 'F055 R3 C<n>:'
  True aa105b063 has the single parent 47eb42d3e
  True aa105b063 subject begins 'F055 R3 C<n>:'
  True f1b4a0310 has the single parent aa105b063
  True f1b4a0310 subject begins 'F055 R3 C<n>:'
  True ff7f04e12 has the single parent f1b4a0310
  True ff7f04e12 subject begins 'F055 R3 C<n>:'
  True 93c397422 has the single parent ff7f04e12
  True 93c397422 subject begins 'F055 R3 C<n>:'
  [... 5 C1-path-equality lines, 5 path-set checks (C2 to C5), C2's page-insertion check, C3's
  pending/rejected/no-BLE001 checks, C4's warning/no-BLE001/status-label/guide-insertion checks —
  all True ...]
  ALL True
  ```
  (36 checks total, every one `True`; the C6-amendment-copy check does not run yet — C6 did not
  exist when this gate ran, exactly as the block's "once each, after C5 and before C6" orders.)

**Gate 2** — `python3 -m ruff check` over every Python file C3, C4 and C5 touched
(`job_run_refusals.py`, `do_cmd.py`, `command_catalog.py`, `client_interface.py`,
`do_rehearsal.py`, `decision.py`, `status_cmd.py`, `run_side_effect_counters.py`,
`test_rehearsal.py`, `test_do_rehearsal.py`): `All checks passed!`, run once after C5.

**Gate 3** — `python3 /home/decodeux/Repos/remedy/.remedy-wt/f055-r3/prep/run_selection.py
/home/decodeux/Repos/remedy <output file>`, run ONCE, after C5 and the amendment:
```
SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252)
SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252)
SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252)
SKIPPED [1] tests/regression/test_named_bugs.py:385: D3 quarantine (F252)
SKIPPED [1] tests/regression/test_named_bugs.py:394: D3 quarantine (F252)
SKIPPED [1] tests/regression/test_named_bugs.py:401: D3 quarantine (F252)
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252)
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252)
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252)
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252)
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252)
124 paths
5857 passed, 13 skipped in 73.93s (0:01:13)
exit 0
```
No FAILED or ERROR line, no line naming a process left behind. Every SKIPPED is a pre-existing
quarantine, none of them in a file this round touched.

**Gate 4** — `python3 -m apps.cli.main integrity check --json`:
```
{"check_count": 6, "checks": [{"message": "handlers=188", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```

**Gate 5** —
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`:
```
['R-1246', 'R-1276', 'R-1277', 'R-1278', 'R-1279', 'R-1280', 'R-1281', 'R-1282', 'R-1283', 'R-1284', 'R-1285', 'R-1286', 'R-1287', 'R-1288', 'R-1289', 'R-1290', 'R-1291', 'R-1292', 'R-1293', 'R-1294', 'R-1295', 'R-1296', 'R-1297', 'R-1298', 'R-1299', 'R-1300', 'R-1301', 'R-1302', 'R-1303', 'R-1304', 'R-1305', 'R-1306', 'R-1307', 'R-1308', 'R-1309', 'R-1310', 'R-1311', 'R-1312', 'R-1313', 'R-1317']
```
40 ids: `R-1246`, then `R-1276` to `R-1313`, then `R-1317`, in order, as required.

**Gate 6** — `git show --stat` for C3 and C4:
```
f1b4a0310 F055 R3 C3: remedy job run refuses a plan that is not approved (R-1317)
 apps/cli/client_interface.py                       |  3 ++-
 apps/cli/command_catalog.py                        |  2 +-
 apps/cli/commands/do_cmd.py                        | 12 ++++-----
 apps/cli/commands/job_run_refusals.py              | 29 ++++++++++++++++++++++
 docs/guides/exit-codes.md                          |  1 +
 docs/system/machine-client-contract-v1.md          |  4 +--
 tests/orchestration/import_reachability_allowlist.txt |  1 +
 7 files changed, 42 insertions(+), 10 deletions(-)

ff7f04e12 F055 R3 C4: a moved repository warns at the approval and the run, and status labels a waiting rehearsal
 apps/cli/client_interface.py              |  2 +-
 apps/cli/commands/decision.py             |  8 +++++++-
 apps/cli/commands/do_cmd.py               | 12 ++++++------
 apps/cli/commands/status_cmd.py           | 12 ++++++------
 docs/guides/do-run-v1.md                  | 12 ++++++++++++
 docs/system/machine-client-contract-v1.md |  2 +-
 packages/orchestration/do_rehearsal.py    | 28 +++++++++++++++++++++++++++-
 7 files changed, 60 insertions(+), 16 deletions(-)
```
Measures, read with the ratchet's own scoped measure at C5 (HEAD): `_cmd_job_run` 205,
`_cmd_status` 179, `apps/cli/commands/do_cmd.py` 1024 — all three exact; `tests/test_structure_ratchet.py`
(5 tests) green.

## Authored-text proofs

`.agent/authored/f055-r3.md` against `block.md`: byte-identical, sha256
`5ecd65e44b895ddf19374cff1cb577395f1edf660657aa2b2d565e4bf5473375`, confirmed twice — once by my
own copy script and again independently by `verify.py`'s Gate 1 (`git show <C1>:<path>` compared
to the prep file's bytes). `.agent/authored/f055-r3-amend1.md` against `amend1.md`: byte-identical,
sha256 `048396ca226a920f579c1ed704b30f6ff42c1b8619208dd5b8862d3afecea389`, confirmed by my own copy
script at write time (the replacement `verify.py`'s own `C6`-amendment-copy check was not run as
part of this round's "once each" gate pass, since C6 did not exist yet when gates ran — see Gate 1
above). The four `dry-*.md` copies applied in C1 (`live_review.md`, `prose_slips.md`,
`decisions.md`, `plan.md`) were each confirmed byte-equal by sha256 at copy time and again by
Gate 1's per-path check. No other reviewer-authored text was applied this round.

## Deviations & assumptions

1. **Amendment 1** (`.agent/authored/f055-r3-amend1.md`), sent after gate 1's first run this
   round (reproduced in Verification above): the original `verify.py`'s `ALLOWED` sets for C3 and
   C4 did not name `apps/cli/client_interface.py` (either commit) or `docs/guides/exit-codes.md`
   (C3), although the block's own C3 step 3 ordered the catalog change that forces both into sync;
   and its warning check read the source as one line, where C4's committed code wrapped the
   sentence across three string-literal lines. Both are named in the amendment as the reviewer's
   slips, not mine. Per my standing instructions I stopped before C6 on the first (red) reading,
   pushed nothing, and reported it precisely rather than routing around it. The amendment widened
   `ALLOWED["C3"]` and `ALLOWED["C4"]`, changed the warning check to read adjacent string literals
   as one, declared C1 to C5 as committed with no code change needed, and ordered: discard my
   local (uncommitted, now-superseded) reformatting of the warning string, run gates 1 to 6 once
   each including gate 3, then C6 and the push. All of that is done; gate 1's second (and only
   counted) run is green, reproduced above.
2. **`apps/cli/client_interface.py` and `docs/guides/exit-codes.md` touched in C3, and
   `apps/cli/client_interface.py` touched again in C4** — beyond the block's originally named
   paths for those commits, now accepted by amendment 1 (deviation 1 above) and bounded to exactly
   what `tests/cli/test_exit_codes.py` and `tests/cli/test_client_interface.py` asked for: the new
   refusal tokens, the new exit code, and the new `status.run` answer key.

No other departure from the block's or the amendment's ordered commit sequence.

## For the operator, in plain sentences

This round booked round 2's verdict, closed the finding it opened, and registered the new one
this round repairs, then landed the real-run half of the rehearsal feature: running a rehearsed,
approved job no longer plans it again; a job whose plan still waits for approval, or was turned
down, is refused with the same words and exit code every other job command already uses; a
repository that moved since a rehearsal warns at the approval and at the run, without stopping
either; and the status overview marks a waiting rehearsed job, and stops marking it once it runs
for real. One round came back from the reviewer with an amendment: the gate that checks a
commit's files against the block's list was itself narrower than the round actually needed, over
two small, necessary consequences of a change the block had already ordered, plus one gate check
that misread a wrapped sentence as broken when it was not. Nothing about the feature's behaviour
changed because of it. All six checks the round requires came back clean on the run that counts.
The feature's three task slices are now all landed; what remains is the closure sequence.

## Next

1. Phase 1 rule 1: `.agent/STOP` — absent at this handoff.
2. Rule 2, the Open PR Gate: no pull request is open for this branch yet.
3. Book round 3's verdict in the next round's first commit.
4. The closure sequence.

Operator questions open: 0.
Open findings: 40 (R-1317 owned by F055, R-1246 and R-1276 to R-1313 by F307).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | preconditions held: HEAD and origin both `20630636b`, clean, no STOP |
| C1 | done | Gate 1 all five path-equality checks `True`; 192 insertions |
| C2 | done | the anchor was unique, C2's page equals C1's with the two boundaries inserted; 14 insertions |
| C3 | done | R-1317's refusal authored and proven; 42 insertions (amendment 1 widened its allowed paths) |
| C4 | done | the warning and the label landed; 60 insertions (amendment 1 widened its allowed paths and fixed the gate's own read of the warning) |
| C5 | done | 17 passed in `test_rehearsal.py` (12 existing + 5 new), 17 passed in `test_do_rehearsal.py` (11 existing + 6 new); 275 insertions |
| C6 | done | this commit |
| Gate 1 | done | first run RED (two allowlist gaps, one contiguity misread — all three the gate's own, per amendment 1); second run, after the amendment, `ALL True` |
| Gate 2 | done | `All checks passed!` |
| Gate 3 | done | run once, after C5 and the amendment — 5857 passed, 13 skipped (pre-existing quarantines), exit 0 |
| Gate 4 | done | `fail_count` 0 |
| Gate 5 | done | 40 ids, in order |
| Gate 6 | done | `git show --stat` for C3/C4 and the three measures reported above |
| R-1317 | done | `tests/cli/test_rehearsal.py` scenario (p): `job run` on a rehearsed job's pending then rejected plan exits 3 with `plan_awaiting_approval` then `plan_rejected`, under `--json`, the job staying `planned` with no provider built |
