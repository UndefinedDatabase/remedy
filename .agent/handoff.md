# Handoff — F162 round 10

## Session

SESSION 2 of feature F162 · round 10 · rounds so far 10. Context stayed healthy throughout: every
digest, copy, launch and gate ran clean on its first and only attempt, so nothing needed a retry
that would have spent the round's budget twice.

Fortschritt: ~92 % (T001 to T003 landed; R-1470 repaired, the consolidation pass, the self-use run
and the one full suite done · the evidence, the package and the closing round remain) — Schätzung.

## Range

Review of `8a61ba724`..`b0ea97549` (C1 to C5; C6 — this file — is the commit that carries it, per
the handback template's self-reference exception).

## Commits

### 18ea2b563 F162 R10 C1: book round 9, R-1469 resolved, register R-1470, the plan, the block and the self-use script
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f162-r10.md` | +163/-0 | NEW FILE — this round's block, the authored-text proof, byte-copied from the prepared `c1-` file |
| `.agent/authored/f162-r10-selfuse.py` | +190/-0 | NEW FILE — the self-use script C4 runs, byte-copied from the prepared `c1-` file |
| `.agent/live_review.md` | +6/-0 | round 9's gate/verdict booked, R-1469 closed as a `Done:` paragraph, R-1470 registered OPEN |
| `.agent/plan.md` | +9/-7 | rewritten: Current Step moves to round 10's closure-sequence work, Next Steps point at round 11 and the closing round |

### 65367b3b3 F162 R10 C2: repair R-1470, the sandbox model's index row names its folder
| Path | +/- | Reason |
|---|---|---|
| `docs/README.md` | +1/-1 | repair R-1470: the sandbox-model Quick-Find row's type cell now reads `system`, so the documentation staleness check no longer reports it |

### 226015cb7 F162 R10 C3: the checklist's consolidation pass for F162
| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | +17/-0 | F162's one mandatory consolidation paragraph appended to the pre-emission checklist; nothing joined, no two items merged, the list stays at 34 items |

### 2fa84a217 F162 R10 C4: the closure's self-use item run to its approval gate, never applied
| Path | +/- | Reason |
|---|---|---|
| `scripts/self_use_queue.json` | +8/-0 | the generator's one appended entry, `SU-083`, `consumed_by` empty |
| `.agent/selfuse_f162/SU-083.md` | +11/-0 | NEW FILE — the generated job file for `SU-083` |
| `.agent/selfuse_f162/changed_paths.txt` | +1/-0 | NEW FILE — the one path the job's staged apply touched |
| `.agent/selfuse_f162/entry_and_job_file.txt` | +5/-0 | NEW FILE — the entry's id, title, provenance and job-file path |
| `.agent/selfuse_f162/execution_config.txt` | +43/-0 | NEW FILE — the run's execution configuration |
| `.agent/selfuse_f162/full_transcript.txt` | +14/-0 | NEW FILE — the job and task summary |
| `.agent/selfuse_f162/job_diff.txt` | +92/-0 | NEW FILE — the job branch's diff against `HEAD` |
| `.agent/selfuse_f162/result_state.txt` | +12/-0 | NEW FILE — the job and task state |
| `.agent/selfuse_f162/run_defects.txt` | +1/-0 | NEW FILE — `describe_self_use_run_defects` over the run's `JobPlan`: `NONE` |
| `.agent/selfuse_f162/staleness_after.txt` | +2/-0 | NEW FILE — the staleness catalog read from the job branch's workspace |
| `.agent/selfuse_f162/timing.txt` | +3/-0 | NEW FILE — start, finish and wall seconds |
| `.agent/selfuse_f162/worker_isolation.txt` | +2/-0 | NEW FILE — the run's `worker_isolation.jsonl` lines |
| `.agent/selfuse_f162/worker_sandbox.txt` | +2/-0 | NEW FILE — the run's `worker_sandbox.jsonl` lines (DECISION F162 D5) |

### b0ea97549 F162 R10 C5: the closure's one full suite and its CPU cost
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f162-closure-suite.txt` | +27/-0 | NEW FILE — the one full-suite transcript (`python3 -m pytest -n auto -q`) and the `closure_suite_cost.py` reading against F152's closure |

### (this commit) F162 R10 C6: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file — carried alone, per the handback template's self-reference exception (R-0149) |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft`, run before any write, as
the Open PR Gate: printed `[]` — no open PR for this branch, so no merge was due and a new branch
was not needed either (the feature branch was already current). No `gh pr create`, `gh pr merge`,
`git worktree add` or `git worktree remove` of my own this round: the self-use script's own
staleness read used the job's workspace directory (`plan.job_workspace_path`), not the job-branch
worktree fallback, so that branch of the script never ran `git worktree add`. No `claude` binary
invoked directly; the only provider calls this round are C4's self-use run's own two real calls
(builder then reviewer), inside their budget. `git push origin feature/f162-sandbox-profiles` runs
once, immediately after this commit, per the block's push discipline; its real outcome is reported
in the session reply, not in this file.

## Verification

**Gate 1.** `git status --porcelain` (empty), then `python3 .remedy-wt/f162-r10/prep/verify.py .`
(run from the repository root):
```
True	18ea2b563 single parent equal to the commit before it
True	18ea2b563 subject carries a F162 R10 Cn tag: F162 R10 C1: book round 9, R-1469 resolved, register R-1470, the plan,
True	18ea2b563 adds no machine path
True	65367b3b3 single parent equal to the commit before it
True	65367b3b3 subject carries a F162 R10 Cn tag: F162 R10 C2: repair R-1470, the sandbox model's index row names its fo
True	65367b3b3 adds no machine path
True	226015cb7 single parent equal to the commit before it
True	226015cb7 subject carries a F162 R10 Cn tag: F162 R10 C3: the checklist's consolidation pass for F162
True	226015cb7 adds no machine path
True	2fa84a217 single parent equal to the commit before it
True	2fa84a217 subject carries a F162 R10 Cn tag: F162 R10 C4: the closure's self-use item run to its approval gate, nev
True	2fa84a217 adds no machine path
True	b0ea97549 single parent equal to the commit before it
True	b0ea97549 subject carries a F162 R10 Cn tag: F162 R10 C5: the closure's one full suite and its CPU cost
True	b0ea97549 adds no machine path
True	on feature/f162-sandbox-profiles
True	C1 paths ['.agent/authored/f162-r10-selfuse.py', '.agent/authored/f162-r10.md', '.agent/live_review.md', '.agent/plan.md']
True	C1 .agent/authored/f162-r10-selfuse.py equals its c1- file
True	C1 .agent/authored/f162-r10.md equals its c1- file
True	C1 .agent/live_review.md equals its c1- file
True	C1 .agent/plan.md equals its c1- file
True	C2 the docs index alone
True	C2 index equals the prepared copy
True	C2 numstat ['1\t1\tdocs/README.md']
True	C2 no docs_index_type_column claim at HEAD: []
True	C3 the checklist page alone
True	C3 page equals the prepared copy
True	C3 numstat ['17\t0\tdocs/agents/planner_reviewer_prompt.md']
True	C4 paths: the queue and 12 file(s) under .agent/selfuse_f162/
True	C4 writes twelve self-use files: 12
True	C4 writes entry_and_job_file.txt
True	C4 writes execution_config.txt
True	C4 writes result_state.txt
True	C4 writes timing.txt
True	C4 writes changed_paths.txt
True	C4 writes full_transcript.txt
True	C4 writes worker_isolation.txt
True	C4 writes worker_sandbox.txt
True	C4 writes staleness_after.txt
True	C4 writes job_diff.txt
True	C4 writes run_defects.txt
True	C4 queue gains exactly one appended entry: SU-083
True	C4 the new entry is not consumed
True	C4 writes the entry's own job file
True	C5 the transcript alone
True	C5 transcript carries 'command:'
True	C5 transcript carries 'real exit code:'
True	C5 transcript carries 'wall time:'
True	C5 transcript carries 'summary line:'
True	C5 transcript carries 'bad node ids (failed + errors):'
True	C5 transcript carries 'leftover processes:'
True	C5 transcript carries 'tree it ran on:'
True	C5 transcript carries 'reflog unchanged during the run:'
True	C5 transcript carries 'cost exit code:'
absent	C6
True	the saved block equals block.md
ALL True
```
Every line `True`; `C6` correctly `absent` (not yet committed when this gate ran). Not re-run: it
was green on the first run.

**Gate 2.** The twelve files under `.agent/selfuse_f162/`, each non-empty (byte sizes, read-only,
one dedicated script):
```
entry_and_job_file.txt: 302 bytes
execution_config.txt: 1367 bytes
result_state.txt: 855 bytes
timing.txt: 104 bytes
changed_paths.txt: 44 bytes
full_transcript.txt: 1581 bytes
worker_isolation.txt: 861 bytes
worker_sandbox.txt: 1431 bytes
staleness_after.txt: 200 bytes
job_diff.txt: 3097 bytes
run_defects.txt: 5 bytes
SU-083.md: 886 bytes
```
All twelve non-empty.

**Gate 3.** The suite of C5, as the transcript records it: exit code `0`; summary line
`24116 passed, 11 skipped, 1 warning in 403.19s (0:06:43)`; bad node ids (failed + errors):
`NONE`.

**Gate 4.** `python3 -m apps.cli.main integrity check --json`:
```
{"check_count": 6, "checks": [{"message": "handlers=201", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
`fail_count` 0, all six checks `pass`. Then
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`:
`['R-1246', 'R-1281', 'R-1351', 'R-1353', 'R-1426', 'R-1428', 'R-1448', 'R-1450', 'R-1464', 'R-1467', 'R-1470']`
— exactly the eleven ids the block names, in the same order.

## Authored-text proofs

C1's four byte copies were each proved byte-equal to their prepared `c1-` file immediately after
copying, via a dedicated copy-and-hash script (every digest in `digests.txt`, and `digests.txt`'s
own sha256 against the one the session prompt named, independently confirmed with a Python sha256
reader before any prepared file was read). The authored block's own proof: `.agent/authored/f162-r10.md`
is 163 lines with sha256 `4353a05c555ba68b33f1a5840f076ab452330788da5c1bce08aa9258b2897136`,
identical to `block.md`'s own sha256 — the same digest `digests.txt` names for both prepared files.
C2 and C3's byte copies were each proved byte-equal to their prepared `c2-`/`c3-` file immediately
after copying, by the same method. Gate 1's `verify.py` run independently re-confirmed every
`C1`/`C2`/`C3 ... equals ...` line `True`.

## Self-use run

Entry `SU-083`, "Write the first tests for packages/orchestration/config_key_spec.py", job id
`0cdcfc43d6754774`. Builder: `claude-cli`, model `claude-sonnet-4-6`, effort `medium`. Reviewer:
`claude-cli`, model `claude-sonnet-4-6`, effort `medium` (both read from `execution_config.txt`).
Job state `completed`, stop reason empty, error empty. Task `T001`: status
`applied_to_job_workspace`, reviewer verdict `pass`, final status `staged_review_passed`, zero
repair rounds used (read from `result_state.txt`). Wall seconds `51.4` (read from `timing.txt`).

`changed_paths.txt` VERBATIM:
```
tests/orchestration/test_config_key_spec.py
```

`worker_isolation.txt` VERBATIM:
```
T001: {"adr_ref": "docs/adr/0002-claude-cli-worker-isolation.md", "applied": true, "env_digest": "7db0bffa706f498f7cee90e529f8df70bcee84653661ba0e35204967c1ff7ae5", "home": "operator", "method": "tool_flag", "model": "claude-sonnet-4-6", "names": ["HOME", "LANG", "LOGNAME", "PATH", "SHELL", "TERM", "USER"], "provider": "claude-cli", "role": "builder", "tool_args": ["--setting-sources", "project,local", "--strict-mcp-config"]}
T001: {"adr_ref": "docs/adr/0002-claude-cli-worker-isolation.md", "applied": true, "env_digest": "7db0bffa706f498f7cee90e529f8df70bcee84653661ba0e35204967c1ff7ae5", "home": "operator", "method": "tool_flag", "model": "claude-sonnet-4-6", "names": ["HOME", "LANG", "LOGNAME", "PATH", "SHELL", "TERM", "USER"], "provider": "claude-cli", "role": "reviewer", "tool_args": ["--setting-sources", "project,local", "--strict-mcp-config"]}
```

`worker_sandbox.txt` VERBATIM:
```
T001: {"dimensions": {"allowed_binaries": "enforced", "fs_scope": "unenforced", "net": "unenforced", "tmp_quota_mb": "enforced", "ulimits.cpu_s": "enforced", "ulimits.mem_mb": "enforced", "ulimits.nofile": "enforced"}, "model": "claude-sonnet-4-6", "profile": "claude-cli", "provider": "claude-cli", "reasons": {"allowed_binaries": "nothing to limit", "fs_scope": "no tool sandbox: only the working directory is pinned", "net": "the host network is shared and hosts are not filtered", "tmp_quota_mb": "nothing to limit", "ulimits.cpu_s": "nothing to limit", "ulimits.mem_mb": "nothing to limit", "ulimits.nofile": "RLIMIT_NOFILE on the process tree"}, "role": "builder", "runner": "process", "tool_sandbox": false}
T001: {"dimensions": {"allowed_binaries": "enforced", "fs_scope": "unenforced", "net": "unenforced", "tmp_quota_mb": "enforced", "ulimits.cpu_s": "enforced", "ulimits.mem_mb": "enforced", "ulimits.nofile": "enforced"}, "model": "claude-sonnet-4-6", "profile": "claude-cli", "provider": "claude-cli", "reasons": {"allowed_binaries": "nothing to limit", "fs_scope": "no tool sandbox: only the working directory is pinned", "net": "the host network is shared and hosts are not filtered", "tmp_quota_mb": "nothing to limit", "ulimits.cpu_s": "nothing to limit", "ulimits.mem_mb": "nothing to limit", "ulimits.nofile": "RLIMIT_NOFILE on the process tree"}, "role": "reviewer", "runner": "process", "tool_sandbox": false}
```

`job_diff.txt` VERBATIM:
```
$ git diff HEAD...remedy/job-0cdcfc43d6754774  (exit 0)
diff --git a/tests/orchestration/test_config_key_spec.py b/tests/orchestration/test_config_key_spec.py
new file mode 100644
index 000000000..69014a722
--- /dev/null
+++ b/tests/orchestration/test_config_key_spec.py
@@ -0,0 +1,85 @@
+import pytest
+from packages.orchestration.config_key_spec import ConfigKeySpec
+
+
+def test_minimal_construction():
+    spec = ConfigKeySpec(key="my_key", env_var="MY_KEY", description="A test key")
+    assert spec.key == "my_key"
+    assert spec.env_var == "MY_KEY"
+    assert spec.description == "A test key"
+
+
+def test_defaults():
+    spec = ConfigKeySpec(key="k", env_var="K", description="d")
+    assert spec.value_type is str
+    assert spec.entry_type is None
+    assert spec.default is None
+    assert spec.env_only is False
+    assert spec.secret is False
+    assert spec.fallback_key is None
+
+
+def test_value_type_int():
+    spec = ConfigKeySpec(key="timeout", env_var="TIMEOUT", description="timeout", value_type=int, default=30)
+    assert spec.value_type is int
+    assert spec.default == 30
+
+
+def test_value_type_bool():
+    spec = ConfigKeySpec(key="flag", env_var="FLAG", description="a bool flag", value_type=bool, default=False)
+    assert spec.value_type is bool
+    assert spec.default is False
+
+
+def test_value_type_list():
+    spec = ConfigKeySpec(key="items", env_var="ITEMS", description="a list", value_type=list)
+    assert spec.value_type is list
+
+
+def test_value_type_dict_with_entry_type():
+    spec = ConfigKeySpec(
+        key="table", env_var="TABLE", description="a dict", value_type=dict, entry_type=str
+    )
+    assert spec.value_type is dict
+    assert spec.entry_type is str
+
+
+def test_entry_type_dict_for_record_table():
+    spec = ConfigKeySpec(
+        key="records", env_var="RECORDS", description="record table", value_type=dict, entry_type=dict
+    )
+    assert spec.entry_type is dict
+
+
+def test_env_only_flag():
+    spec = ConfigKeySpec(key="token", env_var="TOKEN", description="token", env_only=True)
+    assert spec.env_only is True
+
+
+def test_secret_flag():
+    spec = ConfigKeySpec(key="api_key", env_var="API_KEY", description="secret", secret=True)
+    assert spec.secret is True
+
+
+def test_fallback_key():
+    spec = ConfigKeySpec(key="new_key", env_var="NEW_KEY", description="with fallback", fallback_key="old_key")
+    assert spec.fallback_key == "old_key"
+
+
+def test_frozen_immutability():
+    spec = ConfigKeySpec(key="k", env_var="K", description="d")
+    with pytest.raises((AttributeError, TypeError)):
+        spec.key = "changed"  # type: ignore[misc]
+
+
+def test_equality_and_hashing():
+    spec1 = ConfigKeySpec(key="k", env_var="K", description="d")
+    spec2 = ConfigKeySpec(key="k", env_var="K", description="d")
+    assert spec1 == spec2
+    assert hash(spec1) == hash(spec2)
+
+
+def test_inequality():
+    spec1 = ConfigKeySpec(key="a", env_var="A", description="d")
+    spec2 = ConfigKeySpec(key="b", env_var="B", description="d")
+    assert spec1 != spec2
```

`run_defects.txt` VERBATIM:
```
NONE
```

No finding is registered by this handback for the self-use run; `run_defects.txt` reads `NONE`, so
there is nothing for the next round's first commit to register.

## Closure suite

`.agent/authored/f162-closure-suite.txt`, whole and verbatim:
```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 404.1s (the launcher's reading); pytest's own reported wall time: 403.19s (0:06:43)
summary line: 24116 passed, 11 skipped, 1 warning in 403.19s (0:06:43)
bad node ids (failed + errors): NONE
leftover processes: NONE
tree it ran on: 2fa84a217 (F162 R10 C4: the closure's self-use item run to its approval gate, never applied)
tree note: C1 to C4 changed only .agent/ files, one docs index cell, the checklist page and the self-use queue
reflog before: 2fa84a217 HEAD@{2026-10-24 15:25:36 +0200}: commit: F162 R10 C4: the closure's self-use item run to its approval gate, never applied
reflog after: 2fa84a217 HEAD@{2026-10-24 15:25:36 +0200}: commit: F162 R10 C4: the closure's self-use item run to its approval gate, never applied
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F162 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1453.59 CPU seconds, 403.22 wall seconds, 24127 tests collected, exit status 0, recorded 2026-10-24T13:32:26Z
This closure's suite used 1453.59 CPU seconds, 4.8 percent less than F152's 1526.77, within the 10 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 0 percent.
The test modules whose CPU time rose most since F152's closure run:
  +9.67 s  tests/cli/test_do_sequence_cli.py (35.83 -> 45.50)
  +5.81 s  tests/orchestration/test_serve_daemon.py (23.31 -> 29.12)
  +4.54 s  tests/orchestration/test_run_manifest_task_lifecycle_binding.py (4.04 -> 8.58)
  +3.63 s  tests/runtimes/test_supervisor_portability.py (48.40 -> 52.03)
  +3.63 s  tests/orchestration/test_public_api_gate_paths.py (18.60 -> 22.23)
  +3.54 s  tests/orchestration/test_self_use_generator.py (7.57 -> 11.11)
  +2.83 s  tests/orchestration/test_subtree_rerun_prepare.py (17.09 -> 19.92)
  +2.69 s  tests/orchestration/test_event_name_coupling.py (14.93 -> 17.62)
  +2.58 s  tests/cli/test_quick_start.py (2.15 -> 4.73)
  +2.50 s  tests/cli/test_do_scale_matrix.py (38.22 -> 40.72)
```

## Deviations & assumptions

None. Every commit followed the block's ordered sequence C1 to C6; every path touched is exactly
the path set the block and `verify.py` name; the self-use run was launched once and waited for
once to completion on the first `wait.py` call (no second poll was needed); the suite ran once and
was waited for once to completion on the first `wait.py` call; the cost script ran exactly once.
No agent, fork, helper or subagent of any kind was started. No `cd`; every check or proof ran as a
single call, and every copy/hash/size script lives under `.remedy-wt/f162-r10-worker/`, each run
once. No command asked for an approval and none was refused. The `claude` binary was never run
directly. No `REMEDY_TEST_MAX_WORKERS`, no larger `-n`, no second test command, no worktree of my
own, no mutation. No production file was touched; the self-use job's own change stays on its
`remedy/job-0cdcfc43d6754774` branch, never applied.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | four files byte-equal to the prepared snapshots; `block.md` 163 lines, sha256 `4353a05c555ba68b33f1a5840f076ab452330788da5c1bce08aa9258b2897136` |
| C2 | done | the R-1470 repair; numstat `1 1` on `docs/README.md`, exactly as ordered |
| C3 | done | the consolidation paragraph; numstat `17 0` on the checklist page, exactly as ordered |
| C4 | done | self-use entry `SU-083` run to `completed`/`pass`/`staged_review_passed`, never applied; queue gained exactly one entry with empty `consumed_by`; twelve files written |
| C5 | done | the one full suite, `24116 passed, 11 skipped`, exit 0, no bad node ids; the cost script, exit 0, within the 10 percent limit |
| C6 | done | this handback |
| Gate 1 | done | every line `True`, `C6` correctly `absent` |
| Gate 2 | done | all twelve `.agent/selfuse_f162/` files non-empty |
| Gate 3 | done | exit 0, the summary line above, no bad node ids |
| Gate 4 | done | `fail_count` 0; open ids exactly the eleven the block names |
| Push | pending | runs immediately after this commit, per the block's push discipline; outcome reported in the reply |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work (absent as of this session).
2. Phase 1 rule 2: the Open PR Gate — no pull request is open for this branch yet.
3. The reviewer reviews round 10, books its verdict and R-1470, and registers every self-use run
   defect in the next round's first commit.
4. The evidence bundle and the review package, because this round's suite is green.
5. The closing round: the Built State, the rotation, the STATUS line, the README and the pull
   request.

Operator questions open: 2.
Open findings: 11 (R-1246, R-1281, R-1351, R-1353, R-1426, R-1428, R-1448, R-1450 and R-1464, owned
by F316; R-1467, owned by F246; R-1470, owned by F162, repaired this round by C2, pending its
`Done:` paragraph in the next round's first commit).

## For the operator, in plain sentences

Before this feature closes, Remedy ran one real piece of work on itself with a paid model: it was
asked to write the first tests for a small configuration-key helper that had none, and that work
finished cleanly and passed its own review without needing a single repair. The sandbox record the
run's worker calls wrote shows the same profile every claude-cli call on this machine uses today:
it limits what binaries, memory, CPU time and open files a call may use, but it does not fence off
the filesystem or the network, which is the honest, long-standing shape of this worker and not
something this round changed. Remedy's whole test collection then ran once on exactly the code that
will ship: 24,116 tests passed, 11 were skipped on purpose, and none failed. That run took a little
under seven minutes, and the computer time it used was about five percent less than the previous
feature's closure run, comfortably inside the usual run-to-run variation.
