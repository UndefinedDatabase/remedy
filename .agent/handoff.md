# Handoff — F162 round 6

## Session

SESSION 1 of feature F162 · round 6 · rounds so far 6. This session booked round 5's FAIL verdict,
resolved R-1465 and registered R-1466 by copying the prepared ledger and plan texts byte-for-byte,
repaired R-1466 exactly as its THE REPAIR clause states, then built T003's remaining half: the
`claude_cli.sandbox_profile` config key with its regenerated guide row, the tighten-only resolver
`effective_sandbox_profile` and its config-key helper, both slot functions reading through it
instead of parsing the bare declaration, and `worker doctor`'s new `sandbox_<provider_id>` check
wired in right after a worker's isolation checks; context self-assessment: every new behaviour was
proved against an exact field check or a dict-literal comparison written out in its own test, the
doctor's warning and refusal texts were hand-derived from the real built-in TOML values and the
enforcement functions' own branches before any test was written, and one drafting slip — an Edit
that briefly orphaned one assertion line of a pre-existing test while inserting a new test class
after it — was caught and fixed before any test ran green and before anything was staged, so it
never reached a commit.

Fortschritt: ~72 % (T001, T002 landed · T003 under way) — Schätzung.

## Range

Review of `e673cc738`..`477f39922` (C1 to C4; C5 — this file — is the commit that carries it, per
the handback template's self-reference exception).

## Commits

### 50446b91a F162 R6 C1: book round 5, resolve R-1465, register R-1466, DECISION F162 D6, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f162-r6.md` | +140/-0 | NEW FILE — this round's block, the authored-text proof, byte-copied from the prepared `c1-` file |
| `.agent/decisions.md` | +14/-0 | DECISION F162 D6 appended: the `claude_cli.sandbox_profile` key, the resolver, the calls' and evidence's use of it, the doctor check |
| `.agent/live_review.md` | +6/-0 | round 5's gate/verdict entry (VERDICT FAIL), R-1465's Done paragraph booked, R-1466 registered |
| `.agent/plan.md` | +7/-9 | rewritten: Current Step moves to round 6 under DECISION F162 D6 |
| `.agent/prose_slips.md` | +1/-0 | round 5's own prose slip (the `verify.py` reachability-sort false red) appended |

### 3b66e93cc F162 R6 C2: repair R-1466, the falsy-directory test runs where a stray write would land
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_sandbox_profiles.py` | +4/-1 | `test_writes_nothing_for_a_falsy_directory` now sets its working directory to `tmp_path` via `monkeypatch.chdir` before either call, per R-1466's THE REPAIR clause |

### b09b690ed F162 R6 C3: the claude_cli.sandbox_profile key and the tighten-only resolver
| Path | +/- | Reason |
|---|---|---|
| `docs/guides/environment.md` | +1/-0 | the new `REMEDY_CLAUDE_CLI_SANDBOX_PROFILE` row, regenerated from the registry by the command the guide's own header gives |
| `packages/orchestration/config_keys_claude.py` | +12/-0 | the `claude_cli.sandbox_profile` key, D6 (1), word for word |
| `packages/orchestration/sandbox_profiles.py` | +29/-0 | `sandbox_profile_config_key` and `effective_sandbox_profile`, D6 (2) |
| `packages/orchestration/worker_adapter_slot.py` | +10/-10 | `adapter_exec_policy` and `adapter_sandbox_record` now resolve through `effective_sandbox_profile` instead of parsing the bare declaration, D6 (3) |
| `tests/orchestration/test_sandbox_profiles.py` | +57/-0 | the resolver's own cases: the config key, an unset/blank value, `strict`, `net-local`'s refusal, `bogus`'s refusal, no-config reading the process config |
| `tests/orchestration/test_worker_adapter_slot.py` | +43/-0 | `adapter_exec_policy`/`adapter_sandbox_record` read the real `REMEDY_CLAUDE_CLI_SANDBOX_PROFILE` for `strict`'s tightened fields and `net-local`'s refusal |

### 477f39922 F162 R6 C4: worker doctor names each worker's sandbox profile and its unenforced dimensions
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/worker.py` | +6/-0 | `_cmd_worker_doctor` calls `sandbox_doctor_checks` right after a worker's isolation checks, inside the same condition |
| `docs/system/worker-adapter-contract-v2.md` | +7/-0 | the Sandbox default section's closing paragraph (DECISION F162 D6); a blank line added before round 5's own paragraph so it renders on its own |
| `packages/orchestration/sandbox_profiles.py` | +23/-0 | `sandbox_doctor_checks`, D6 (4) |
| `tests/cli/test_worker.py` | +48/-0 | `worker doctor --json` lists a passing `sandbox_claude_code` right after isolation's checks and stays ready; with `net-local` chosen it fails and is named among the blockers |
| `tests/orchestration/test_sandbox_profiles.py` | +75/-0 | `sandbox_doctor_checks`' own cases: the default's warning, `strict`'s warning outside the tool sandbox, `net-local`'s refusal, a double with every dimension enforced |

### (this commit) F162 R6 C5: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +1/-0 | the `Landed: R-1466` ledger line appended as the file's last line |
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
`python3 .remedy-wt/f162-r6/prep/verify.py .`:
```
True	50446b91a single parent equal to the commit before it
True	50446b91a subject carries a F162 R6 Cn tag: F162 R6 C1: book round 5, resolve R-1465, register R-1466, DECISION F1
True	50446b91a insertions 168 under 500 (or the handback)
True	3b66e93cc single parent equal to the commit before it
True	3b66e93cc subject carries a F162 R6 Cn tag: F162 R6 C2: repair R-1466, the falsy-directory test runs where a stray
True	3b66e93cc insertions 4 under 500 (or the handback)
True	b09b690ed single parent equal to the commit before it
True	b09b690ed subject carries a F162 R6 Cn tag: F162 R6 C3: the claude_cli.sandbox_profile key and the tighten-only re
True	b09b690ed insertions 152 under 500 (or the handback)
True	477f39922 single parent equal to the commit before it
True	477f39922 subject carries a F162 R6 Cn tag: F162 R6 C4: worker doctor names each worker's sandbox profile and its
True	477f39922 insertions 159 under 500 (or the handback)
True	on feature/f162-sandbox-profiles
True	C1 paths exactly [five paths]: [five paths] (exact match)
True	C1 .agent/authored/f162-r6.md equals c1-.agent__authored__f162-r6.md
True	C1 .agent/decisions.md equals c1-.agent__decisions.md
True	C1 .agent/live_review.md equals c1-.agent__live_review.md
True	C1 .agent/plan.md equals c1-.agent__plan.md
True	C1 .agent/prose_slips.md equals c1-.agent__prose_slips.md
True	C2 paths exactly [one path]: [one path] (exact match)
True	C2 3b66e93cc adds no machine path
True	C3 paths exactly [six paths]: [six paths] (exact match)
True	C3 b09b690ed adds no machine path
True	C4 paths exactly [five paths]: [five paths] (exact match)
True	C4 477f39922 adds no machine path
absent	C5
True	config.py untouched
True	C3 key declared
True	C3 guide row present
True	C3 resolver functions defined
True	C4 doctor check defined
True	C4 worker doctor calls it
True	the saved block equals block.md
ALL True
```
Every line `True`; `C5` correctly `absent` (not yet committed when this gate ran). Not re-run: it
was green on the first run.

**Gate 2.** `python3 .remedy-wt/f162-r6/prep/run_selection.py . .remedy-wt/f162-r6-worker/selection-output.txt`,
run once, after C4:
```
paths 110
exit 0
5134 passed, 2 skipped in 54.35s
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
```
`exit 0`, no `FAILED` or `ERROR` line, no line containing `process(es) behind`. Both `SKIPPED`
lines are the same two pre-existing, opt-in skips named by every prior round's own handoff; neither
is from this round's new tests. Not red, so no second run was needed.

**Gate 3.** `python3 -m ruff check packages/orchestration/sandbox_profiles.py packages/orchestration/worker_adapter_slot.py packages/orchestration/config_keys_claude.py apps/cli/commands/worker.py tests/orchestration tests/cli/test_worker.py`:
```
All checks passed!
```
Exit 0.

**Gate 4.** `python3 -m apps.cli.main integrity check --json`:
```
{"check_count": 6, "checks": [{"message": "handlers=201", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict FAIL", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
`fail_count` 0, all six checks `pass` (`live_review_verdict`'s message still reports round 5's own
FAIL verdict, now booked by this round's C1; the check itself reads `pass` because booking a FAIL
correctly is what it checks for). Then
`python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`:
`10`. Exactly the block's named count.

## Authored-text proofs

C1's five byte copies were each proved byte-equal to their prepared `c1-` file immediately after
copying, via a dedicated digest-verification script (every digest also independently re-confirmed
against `.remedy-wt/f162-r6/prep/digests.txt` before any prepared file was read). The authored
block's own proof: `.agent/authored/f162-r6.md` is 140 lines (`wc -l`) with sha256
`f51c55e4430c2a9145b07fcb13ec24a0fa7375448f805ead3f95012e8c8a0a53`, identical to `block.md`'s own
sha256 — the same digest `digests.txt` names for both prepared files. Gate 1's `verify.py` run
independently re-confirmed every `C1 ... equals c1-...` line `True`.

## Deviations & assumptions

1. While drafting C3's new tests, an `Edit` whose `old_string` ended one line short of the real end
   of the pre-existing `test_appends_one_sorted_key_line_per_call` test body left that test's last
   assertion (`assert all(p["provider"] == "claude-cli" and p["model"] == "m" for p in parsed)`)
   sitting after the inserted test classes instead of inside the test it belonged to. This was
   caught at once by the first `pytest` run on the file (`NameError: name 'parsed' is not defined`
   in the wrong test), before the file was staged or committed; it was fixed by moving the line back
   into the original test and the file was re-read and re-run clean before anything else happened.
   Nothing wrong ever reached a commit.
2. `sandbox_doctor_checks`' own detail text is pinned to Linux's enforcement branches (every
   `_enforcement_for_*` helper treats a non-Linux `sys.platform` as `unenforced, "not verified on
   <platform>"`), so three of the four new tests in `TestSandboxDoctorChecks` carry
   `@pytest.mark.skipif(not sys.platform.startswith("linux"), ...)`, matching the block's own
   parenthetical for the first case and extended here to the other platform-pinned ones on the same
   reasoning; the fourth, the `net-local` refusal, is platform-independent (the refusal text comes
   from `SandboxProfileLoosened`/`SandboxProfileError`, not from the enforcement table) and carries
   no skip. This host is Linux, so none of the three skips actually fired.
3. Several single-file `pytest` invocations covering each file touched this round, and several
   `ruff check` runs, were made during drafting to self-review each commit's diff before it was
   staged. None ran concurrently with another test command, none was the full suite, and none was a
   mutation red-proof; gate 2 and gate 3 themselves each ran exactly once, after C4, as the block
   requires.
4. A digest-verification script and a byte-copy script were run under
   `.remedy-wt/f162-r6-worker/` (created fresh this round); neither is committed and neither is a
   model or `claude`-binary call.

No other departure from the block's ordered commit sequence: no file touched outside the paths
named per commit, no mutation red-proof, no full suite run beyond gate 2's own selection, no
`REMEDY_TEST_MAX_WORKERS`, no two test commands run at once, no `claude` binary invoked, no worktree
of my own, and no `gh pr merge`, `git checkout`/`git switch` away from the feature branch, branch
creation, rebase, amend, force-push, or `--no-verify`.

## For the operator, in plain sentences

This session recorded the previous session's result and the two small corrections it ordered, then
let a project ask for a stricter safety profile than a worker's own built-in default and made every
place that reads the profile — the actual call, its written record, and the health check — agree on
the same answer. Asking for anything looser than the built-in default is refused before any call
runs, naming what the worker would have used instead. The health check now also says, for the one
worker type that has a safety profile today, which of its protections are honestly not being
enforced on this machine, and only turns that into a failure when the project's own choice was
refused outright. What still needs doing is the optional extra layer of protection that runs a
worker inside its own small throwaway container, which is this feature's last remaining piece.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | five files byte-equal to the prepared snapshots; numstat matched the manifest exactly |
| C2 | done | the falsy-directory test now runs with its working directory set to `tmp_path`; 4 insertions, 1 deletion |
| C3 | done | the `claude_cli.sandbox_profile` key, the regenerated guide row, the resolver, both slot functions reading through it; 152 insertions |
| C4 | done | `sandbox_doctor_checks`, its wiring into `worker doctor`, the contract page's new paragraph; 159 insertions |
| C5 | done | this handoff, committed alone per the self-reference exception, plus the one `Landed:` ledger line |
| R-1465 | done | RESOLVED at F162 R5 by C2, `75e6b81e2`; booked into the permanent ledger by this round's C1 |
| R-1466 | done | RESOLVED at F162 R6 by C2, `3b66e93cc` |
| Gate 1 | done | every line `True`, `C5` correctly `absent` |
| Gate 2 | done | exit 0, `5134 passed, 2 skipped`, no FAILED/ERROR/`process(es) behind`, both SKIPPED lines pre-existing |
| Gate 3 | done | `All checks passed!`, exit 0 |
| Gate 4 | done | `fail_count` 0; open id count `10`, matching the block exactly |
| Push | pending | runs immediately after this commit, per the block's push discipline; outcome reported in the reply |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work (absent as of this session).
2. Phase 1 rule 2: the Open PR Gate, before any new branch.
3. Book round 6's verdict in the next round's first commit.
4. T003: the optional container stage with its ADR, DECISION F162 D7.

Operator questions open: 3.
Open findings: 10 (R-1246, R-1281, R-1351, R-1353, R-1426, R-1428, R-1448, R-1450, R-1464 and
R-1466, owned by F316 and F162).
