# Handoff — F162 round 5

## Session

SESSION 1 of feature F162 · round 5 · rounds so far 5. This session booked round 4's FAIL verdict
and R-1465, appended DECISION F162 D5 and the plan rewrite in its first commit, repaired R-1465
exactly as its THE REPAIR clause states, then built the rest of T003's first half: the compiler's
`tool_sandbox` keyword, the slot's two new functions, the sandbox evidence record and its writer,
the generated reachability list's one line, both claude-cli spawn policies compiled through the
slot, the factory's second evidence line, and the contract page's closing paragraph; context
self-assessment: every new behaviour was proved against a dict literal or an exact field check
written out in its own test rather than trusted by inspection, the claude-cli default's exec policy
and evidence record were hand-verified against the block's own field-by-field description before
any test was written, and one gate-1 false red — a pre-existing, pre-this-round disorder in the
generated reachability list's full ordering, outside the one line this round added — is declared
below rather than silently chased with a reorder the block forbids.

Fortschritt: ~65 % (T001, T002 landed · T003 under way) — Schätzung.

## Range

Review of `62b2bb2bf`..`204dd5824` (C1 to C4; C5 — this file — is the commit that carries it, per
the handback template's self-reference exception).

## Commits

### eb5edad53 F162 R5 C1: book round 4 and R-1465, DECISION F162 D5, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f162-r5.md` | +139/-0 | NEW FILE — this round's block, the authored-text proof, byte-copied from the prepared `c1-` file |
| `.agent/decisions.md` | +15/-0 | DECISION F162 D5 appended: the compiler's keyword, the slot's two functions, the evidence record and writer, both claude-cli policies, the generated list's line |
| `.agent/live_review.md` | +4/-0 | round 4's gate/verdict entry (VERDICT FAIL) and R-1465 booked |
| `.agent/plan.md` | +5/-5 | rewritten: Current Step moves to round 5 under DECISION F162 D5 |
| `.agent/prose_slips.md` | +1/-0 | round 4's own prose slip (the two forwarding methods and the raw-text comment search) appended |

### 75e6b81e2 F162 R5 C2: repair R-1465, the page names the right decision and two needless methods go
| Path | +/- | Reason |
|---|---|---|
| `docs/system/worker-adapter-contract-v2.md` | +1/-1 | `DECISION F152 D3 (4)` corrected to `DECISION F162 D3 (4)` in the Sandbox default section |
| `tests/orchestration/test_worker_adapter_slot.py` | +0/-6 | `_ThrowawayAdapter`'s forwarding `sandbox_default()` method and its false comment deleted |
| `tests/orchestration/test_worker_isolation.py` | +0/-6 | `_ThrowawayHomeAdapter`'s forwarding `sandbox_default()` method and its false comment deleted |

### 13b7bf122 F162 R5 C3: the slot compiles an adapter's default profile, and the sandbox record
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/sandbox_profiles.py` | +51/-3 | D5 (1)'s `tool_sandbox` keyword on the compiler; D5 (4)'s `WORKER_SANDBOX_FILENAME`, `worker_sandbox_record`, `record_worker_sandbox` |
| `packages/orchestration/worker_adapter_slot.py` | +40/-0 | D5 (2)'s `adapter_exec_policy` and `adapter_sandbox_record` |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | D5 (5)'s one generated line, `packages.orchestration.sandbox_profiles`, in its local sorted place |
| `tests/orchestration/test_sandbox_profiles.py` | +82/-0 | the compiler's `tool_sandbox=False` cases, the `worker_sandbox_record` dict-literal case, `record_worker_sandbox`'s falsy/two-line cases |
| `tests/orchestration/test_worker_adapter_slot.py` | +81/-1 | `adapter_exec_policy`'s claude-cli case and its `tool_sandbox=True`/no-`cwd` cases, `adapter_sandbox_record`'s claude-cli dict-literal case |

### 204dd5824 F162 R5 C4: both claude-cli policies compile the default, and every build records it
| Path | +/- | Reason |
|---|---|---|
| `docs/system/worker-adapter-contract-v2.md` | +6/-0 | the Sandbox default section's closing paragraph: `adapter_exec_policy`, `worker_sandbox.jsonl`, `worker_isolation.jsonl` |
| `packages/orchestration/pingpong_provider.py` | +12/-12 | `_cli_exec_policy` and `_stream_exec_policy` now return `adapter_exec_policy("claude-cli", ...)`; the import swaps `adapter_child_env` for `adapter_exec_policy`; file stays at 1570 lines |
| `packages/orchestration/role_provider_factory.py` | +14/-3 | `_record_claude_cli_evidence` helper writes both the isolation and the sandbox line, keeping `create_role_provider` under the structure ratchet's 100-line limit |
| `tests/orchestration/test_capability_routes.py` | +7/-5 | the folder assertion now names both evidence files, sorted |
| `tests/orchestration/test_claude_cli_exec_guard.py` | +12/-0 | `TestStageOnePolicyAndShape` gains the three new field assertions for `_cli_exec_policy`, plus one new test for `_stream_exec_policy` |
| `tests/orchestration/test_role_provider_factory.py` | +29/-0 | `TestWorkerSandboxEvidence`: one claude-cli build writes exactly one sandbox line, one non-claude-cli build writes none |

### (this commit) F162 R5 C5: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +1/-0 | the `Landed: R-1465` ledger line appended as the file's last line |
| `.agent/handoff.md` | rewritten | this file — carried alone, per the handback template's self-reference exception (R-0149) |

## External actions

No `gh pr list`, `gh pr create`, `gh pr merge`, or `git worktree` command this round: this is a
continuation round on the already-open feature branch, not a new branch start, so the Open PR Gate
does not apply here (it is the next round's first duty, named in `## Next`). No `claude` binary
invoked; no model/provider call of any kind; no container image pulled or run. `git push origin
feature/f162-sandbox-profiles` runs once, immediately after this commit, per the block's push
discipline; its real outcome is reported in the session reply, not in this file.

## Verification

**Gate 1.** After C4, `git -C <repository root> status --porcelain`: empty output. Then
`python3 .remedy-wt/f162-r5/prep/verify.py .`:
```
True	eb5edad53 single parent equal to the commit before it
True	eb5edad53 subject carries a F162 R5 Cn tag: F162 R5 C1: book round 4 and R-1465, DECISION F162 D5, the plan
True	eb5edad53 insertions 164 under 500 (or the handback)
True	75e6b81e2 single parent equal to the commit before it
True	75e6b81e2 subject carries a F162 R5 Cn tag: F162 R5 C2: repair R-1465, the page names the right decision and two n
True	75e6b81e2 insertions 1 under 500 (or the handback)
True	13b7bf122 single parent equal to the commit before it
True	13b7bf122 subject carries a F162 R5 Cn tag: F162 R5 C3: the slot compiles an adapter's default profile, and the sa
True	13b7bf122 insertions 255 under 500 (or the handback)
True	204dd5824 single parent equal to the commit before it
True	204dd5824 subject carries a F162 R5 Cn tag: F162 R5 C4: both claude-cli policies compile the default, and every bu
True	204dd5824 insertions 80 under 500 (or the handback)
True	on feature/f162-sandbox-profiles
True	C1 paths exactly [five paths]: [five paths] (exact match)
True	C1 .agent/authored/f162-r5.md equals c1-.agent__authored__f162-r5.md
True	C1 .agent/decisions.md equals c1-.agent__decisions.md
True	C1 .agent/live_review.md equals c1-.agent__live_review.md
True	C1 .agent/plan.md equals c1-.agent__plan.md
True	C1 .agent/prose_slips.md equals c1-.agent__prose_slips.md
True	C2 paths exactly [three paths]: [three paths] (exact match)
True	C2 75e6b81e2 adds no machine path
True	C3 paths exactly [five paths]: [five paths] (exact match)
True	C3 13b7bf122 adds no machine path
True	C4 paths exactly [six paths]: [six paths] (exact match)
True	C4 204dd5824 adds no machine path
absent	C5
True	C2 page names F162 D3 (4)
True	C2 _ThrowawayHomeAdapter has no sandbox_default method
True	C2 _ThrowawayAdapter has no sandbox_default method
True	C3 reachability list holds sandbox_profiles
False	C3 reachability list stays sorted
True	C3 reachability list gains exactly the one line
True	C3 slot defines both functions
True	C4 pingpong_provider.py at 1570 lines, 1570 required
True	C4 pingpong imports adapter_exec_policy and not adapter_child_env: ['adapter_cli_argv', 'adapter_exec_policy', 'adapter_usage_actuals']
True	C4 page paragraph present
True	the saved block equals block.md
ALL False
```
Every line `True` except one (C5 correctly `absent`, not yet committed when this gate ran; the one
real `False` is declared below). Not re-run: the one red line is not a defect this round's own
paths can fix without breaking a different instruction of the same block (declared below), so a
second run would read the identical result.

**Gate 2.** `python3 .remedy-wt/f162-r5/prep/run_selection.py . .remedy-wt/f162-r5-worker/selection-output.txt`,
run once, after C4:
```
paths 105
exit 0
4939 passed, 2 skipped in 49.93s
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
```
`exit 0`, no `FAILED` or `ERROR` line, no line containing `process(es) behind`. Both `SKIPPED`
lines are the pre-existing two prior handoffs already named; neither is from this round's new
tests, so the gate is not red on that account. Not red, so no second run was needed.

**Gate 3.** `python3 -m ruff check packages/orchestration/sandbox_profiles.py packages/orchestration/worker_adapter_slot.py packages/orchestration/pingpong_provider.py packages/orchestration/role_provider_factory.py tests/orchestration`:
```
All checks passed!
```
Exit 0.

**Gate 4.** `python3 -m apps.cli.main integrity check --json`:
```
{"check_count": 6, "checks": [{"message": "handlers=201", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict FAIL", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
`fail_count` 0, all six checks `pass` (`live_review_verdict`'s message reports round 4's own FAIL
verdict, now booked; the check itself still reads `pass` because booking a FAIL is correct). Then
`python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`:
`10`. Exactly the block's named count.

## Authored-text proofs

C1's five byte copies were each proved byte-equal to their prepared `c1-` file immediately after
copying, via a dedicated digest-verification script. The authored block's own proof:
`.agent/authored/f162-r5.md` is 139 lines (`wc -l`) with sha256
`757b6b94fd98b41809f46960569c1c55411354be033e54b3d7caf38f686298b4`, identical to `block.md`'s own
sha256 — the same digest `digests.txt` names for both prepared files. Gate 1's `verify.py` run
independently re-confirmed every `C1 ... equals c1-...` line `True`.

## Deviations & assumptions

1. Gate 1's `verify.py` reads `False` on "C3 reachability list stays sorted," and this line was
   NOT fixed. Measured directly: `git show 62b2bb2bf:tests/orchestration/import_reachability_allowlist.txt`
   was already not in full alphabetical order before this round started (confirmed by comparing it
   against Python's own `sorted()` on its own content) — long-standing disorder around the
   `job_report`/`job_input_definition` region and the `serve_http_handler`/`side_role_*`/`tier_*`
   region, neither touched by this round. This round's own C3 commit added exactly one line,
   `packages.orchestration.sandbox_profiles`, in its correct LOCAL sorted place — immediately after
   `packages.orchestration.safe_points` and before `packages.orchestration.sandbox_relay`, which is
   the ascending order of all three — and `verify.py`'s own "C3 reachability list gains exactly the
   one line" check, which measures the real property the block orders ("add the one line in its
   sorted place, never reorder others"), reads `True`. Resorting the whole file to make the global
   check read `True` would reorder every one of those pre-existing out-of-place lines, which is the
   one thing this round's own block explicitly forbids ("never reorder others"); it would also be a
   far larger, unrelated diff than this round's own scope. This is declared as a gate-1 false red
   rather than silently chased, on the precedent of F162 R3's and R4's own declared `verify.py`
   measurement quirks; it is not added to `.agent/prose_slips.md` because this round's block names
   no commit permitted to touch that file again after C1.
2. Before the official gates ran, several single-file `pytest` invocations covering each file
   touched this round, and several `ruff check` runs, were made during drafting to self-review each
   commit's diff before it was staged. None ran concurrently with another test command, none was
   the full suite, and none was a mutation red-proof; gate 2 and gate 3 themselves each ran exactly
   once, after C4, as the block requires.
3. A digest-verification script, a byte-copy script, and several standalone read-only sanity checks
   (confirming `adapter_exec_policy`'s and `adapter_sandbox_record`'s field-by-field behaviour
   against the block's own prose before any test was written) were run under
   `.remedy-wt/f162-r5-worker/` (created fresh this round); none is committed and none is a model or
   `claude`-binary call.
4. `create_role_provider` in `packages/orchestration/role_provider_factory.py` grew to 102 lines
   when the sandbox-evidence call was first added inline, which `tests/test_structure_ratchet.py`
   caught as a new function above the 100-line limit with no ledger row. Rather than add a row to
   `docs/system/structure-ledger-v1.md` — scope this round's block never orders — the two evidence
   calls were folded into one small helper, `_record_claude_cli_evidence`, bringing the function
   back to 97 lines. This is a deviation in STYLE only: the block's own text, "The factory writes
   `record_worker_sandbox(...)` right after the isolation line," is satisfied exactly — both calls
   happen together, in order, for every claude-cli build — just inside the helper rather than
   written out twice in the outer function's own body.

No other departure from the block's ordered commit sequence beyond the two declared above: no file
touched outside the paths named per commit, no mutation red-proof, no full suite run beyond gate
2's own selection, no `REMEDY_TEST_MAX_WORKERS`, no two test commands run at once, no `claude`
binary invoked, no worktree of my own, and no `gh pr merge`, `git checkout`/`git switch` away from
the feature branch, branch creation, rebase, amend, force-push, or `--no-verify`.

## For the operator, in plain sentences

This session recorded the previous session's result, fixed the two small mistakes that session's
own verification caught, and finished connecting the new safety declaration to how a real worker
call actually runs. Every limit a backend declares for itself now actually reaches the process that
runs its calls, with the strongest protection skipped exactly where a backend says it must be, and
every such call now leaves behind a written record of which limits applied and which did not, right
beside the record already kept of how its environment was cleaned. One already-existing ordering
problem in a generated bookkeeping file, unrelated to anything touched this session, was found and
left alone rather than fixed by a change far outside this session's own boundary, because fixing it
correctly needs its own separate pass. What still needs doing is letting a project state its own
tighter choice, and telling the project's health check what to warn about when it cannot trust what
it is told.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | five files byte-equal to the prepared snapshots; numstat matched the manifest exactly |
| C2 | done | the page's decision reference corrected; both forwarding `sandbox_default()` methods and their false comments deleted; 1 insertion |
| C3 | done | the compiler's `tool_sandbox` keyword, the slot's two functions, the evidence record and writer, the generated list's one line; 255 insertions |
| C4 | done | both claude-cli policies compiled through the slot, the factory's second evidence line, the page's closing paragraph; 80 insertions |
| C5 | done | this handoff, committed alone per the self-reference exception, plus the one `Landed:` ledger line |
| R-1465 | done | RESOLVED at F162 R5 by C2, `75e6b81e2` |
| Gate 1 | deviated | one real `False` line declared above (pre-existing, unrelated disorder in a generated file); every other line `True` |
| Gate 2 | done | exit 0, `4939 passed, 2 skipped`, no FAILED/ERROR/`process(es) behind`, no SKIPPED from this round's new tests |
| Gate 3 | done | `All checks passed!`, exit 0 |
| Gate 4 | done | `fail_count` 0; open id count `10`, matching the block exactly |
| Push | pending | runs immediately after this commit, per the block's push discipline; outcome reported in the reply |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work (absent as of this session).
2. Phase 1 rule 2: the Open PR Gate, before any new branch.
3. Book round 5's verdict in the next round's first commit.
4. T003: a project's choice in `remedy.toml` and the doctor's warnings, DECISION F162 D6.

Operator questions open: 3.
Open findings: 10 (R-1246, R-1281, R-1351, R-1353, R-1426, R-1428, R-1448, R-1450, R-1464 and
R-1465, owned by F316 and F162).
