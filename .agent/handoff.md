# Handoff — F162 round 8

## Session

SESSION 1 of feature F162 · round 8 · rounds so far 8. Every new behaviour this round was proved
against a mocked `run_guarded` call for the repair, the container runtime already on this host for
the generator's cross-check against the committed document, or a real spawned child for the
end-to-end, so nothing here rests on an assumed outcome.

Fortschritt: ~88 % (T001 to T003 landed · the closure open) — Schätzung.

## Range

Review of `98b1e4e18`..`282c7aa2a` (C1 to C4; C5 — this file — is the commit that carries it, per
the handback template's self-reference exception).

## Commits

### 38221d0dc F162 R8 C1: book round 7, register R-1468, DECISION F162 D8, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f162-r8.md` | +120/-0 | NEW FILE — this round's block, the authored-text proof, byte-copied from the prepared `c1-` file |
| `.agent/decisions.md` | +16/-0 | DECISION F162 D8 appended: the generator, the document, the proof map, the walk, the end-to-end and the index rows |
| `.agent/live_review.md` | +4/-0 | round 7's gate/verdict entry booked, R-1468 registered OPEN (the repair R-1468's own text orders) |
| `.agent/plan.md` | +7/-7 | rewritten: Current Step moves to round 8 under DECISION F162 D8 |
| `.agent/prose_slips.md` | +1/-0 | one prose-slip line appended, per the prepared file |

### c7285033a F162 R8 C2: repair R-1468, the real workspace path, the environment and the cleanup rule
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/sandbox_container.py` | +3/-0 | `container_run_argv` resolves `workspace` with `os.path.realpath` before building the `-v` bind and the `-w` argument, so a symlinked workspace is bound and entered at its real path |
| `tests/orchestration/test_sandbox_container.py` | +63/-0 | three new tests: a symlinked workspace's bind and `-w` both name the real path; the base policy's `env` reaches the argv as one `-e` pair per item (`run_guarded` and the image check replaced so nothing runs); an `ok`, a `failed` and a `resource_limit` result each make no further call |

### e6578a0b3 F162 R8 C3: the generated honesty document and its row-to-test walk
| Path | +/- | Reason |
|---|---|---|
| `scripts/render_sandbox_model.py` | +179/-0 | NEW FILE — `render_sandbox_model()`, `write_sandbox_model()` and a `__main__`; the Proof-map constant per (runner, key), the per-profile table builder, and the claude-cli default's own profile built from the installed adapter's declaration |
| `docs/system/sandbox-model.md` | +65/-0 | NEW FILE — GENERATED: one table per profile (strict, standard, net-local, claude-cli default), one row per `SANDBOX_ENFORCEMENT_KEYS` entry, each cell's state and reason read from the real enforcement records |
| `tests/docs/test_sandbox_model_doc.py` | +132/-0 | NEW FILE — the three-assertion walk (byte equality, every Proof node id resolves, every fixture-process test of both runner files is named by a row) plus one red control per direction, built in `tmp_path` |
| `docs/README.md` | +2/-0 | the quick-find row and the System Documentation table row for `sandbox-model.md`, marked generated |
| `tests/test_no_orphan_modules.py` | +3/-2 | `scripts/render_sandbox_model.py` added to `ALLOWED_UNWIRED` (run by hand); `packages/orchestration/sandbox_container.py`'s own entry REMOVED, because the generator's import of `container_sandbox_enforcement` now reaches it — the module is no longer an orphan, so the stale entry would have failed `test_every_allowed_unwired_entry_is_a_live_orphan` |

### 282c7aa2a F162 R8 C4: the end-to-end, the claude-cli default reaches a real spawned child
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_claude_cli_exec_guard.py` | +59/-0 | one test: this process's own `RLIMIT_NOFILE` raised to its hard limit for the duration (skip under 2100); a control run of a stand-in script through `run_guarded` with a bare `ExecGuardPolicy()` opens all 2000 files; the same script through `_guarded_cli_run` stops with errno 24 (EMFILE) having opened fewer than 1024 |

### (this commit) F162 R8 C5: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file — carried alone, per the handback template's self-reference exception (R-0149) |
| `.agent/live_review.md` | +1/-0 | one `Landed: R-1468 — RESOLVED at F162 R8 by C2, c7285033a. ...` line appended as the file's last line |

## External actions

No `gh pr list`, `gh pr create`, `gh pr merge`, or `git worktree` command this round: this is a
continuation round on the already-open feature branch, not a new branch start, so the Open PR Gate
does not apply here (it is the next round's first duty, named in `## Next`). No `claude` binary
invoked; no model/provider call of any kind. No container image pulled, built or pushed at any
point this round: podman/docker and the local `python:3.12-slim` image were already present on
this host, and gate 2's container-runner tests ran `--pull never` through `run_guarded`, same as
every prior round. `git push origin feature/f162-sandbox-profiles` runs once, immediately after
this commit, per the block's push discipline; its real outcome is reported in the session reply,
not in this file.

## Verification

**Gate 1.** After C4, `git -C <repository root> status --porcelain`: empty output. Then
`python3 .remedy-wt/f162-r8/prep/verify.py .`:
```
True	38221d0dc single parent equal to the commit before it
True	38221d0dc subject carries a F162 R8 Cn tag: F162 R8 C1: book round 7, register R-1468, DECISION F162 D8, the plan
True	38221d0dc insertions 148 under 500 (or the handback)
True	c7285033a single parent equal to the commit before it
True	c7285033a subject carries a F162 R8 Cn tag: F162 R8 C2: repair R-1468, the real workspace path, the environment an
True	c7285033a insertions 66 under 500 (or the handback)
True	e6578a0b3 single parent equal to the commit before it
True	e6578a0b3 subject carries a F162 R8 Cn tag: F162 R8 C3: the generated honesty document and its row-to-test walk
True	e6578a0b3 insertions 381 under 500 (or the handback)
True	282c7aa2a single parent equal to the commit before it
True	282c7aa2a subject carries a F162 R8 Cn tag: F162 R8 C4: the end-to-end, the claude-cli default reaches a real spaw
True	282c7aa2a insertions 59 under 500 (or the handback)
True	on feature/f162-sandbox-profiles
True	C1 paths exactly [five paths]: [five paths] (exact match)
True	C1 .agent/authored/f162-r8.md equals c1-.agent__authored__f162-r8.md
True	C1 .agent/decisions.md equals c1-.agent__decisions.md
True	C1 .agent/live_review.md equals c1-.agent__live_review.md
True	C1 .agent/plan.md equals c1-.agent__plan.md
True	C1 .agent/prose_slips.md equals c1-.agent__prose_slips.md
True	C2 paths exactly [two paths]: [two paths] (exact match)
True	C2 c7285033a adds no machine path
True	C3 holds the required paths, extras only guards under tests/: ['tests/test_no_orphan_modules.py']
True	C3 e6578a0b3 adds no machine path
True	C4 paths exactly [one path]: [one path] (exact match)
True	C4 282c7aa2a adds no machine path
absent	C5
True	C2 module resolves the workspace's real path
True	C3 README quick-find and table rows
True	C3 generator functions defined
True	C3 document has the four profiles
True	pingpong_provider.py untouched
True	the saved block equals block.md
ALL True
```
Every line `True`; `C5` correctly `absent` (not yet committed when this gate ran). Not re-run: it
was green on the first run.

**Gate 2.** `python3 .remedy-wt/f162-r8/prep/run_selection.py . .remedy-wt/f162-r8-worker/selection-output.txt`,
run once, after C4:
```
paths 111
exit 0
5170 passed, 2 skipped in 54.12s
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
```
`exit 0`, no `FAILED` or `ERROR` line, no line containing `process(es) behind`. Both `SKIPPED`
lines are the same two pre-existing, opt-in skips every prior round's own handoff names; neither
is from the container fixtures or the end-to-end, which this gate makes a red condition — all
container-runner tests and the new end-to-end test passed outright. Not red, so no second run was
needed.

**Gate 3.** `python3 -m ruff check scripts/render_sandbox_model.py packages/orchestration/sandbox_container.py tests/orchestration tests/docs/test_sandbox_model_doc.py`:
```
All checks passed!
```
Exit 0.

**Gate 4.** `python3 -m apps.cli.main integrity check --json`:
```
{"check_count": 6, "checks": [{"message": "handlers=201", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict FAIL", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
`fail_count` 0, all six checks `pass`. Then
`python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`:
`11`. Exactly the block's named count (this ran BEFORE C5's `Landed:` append; `Landed:` is not a
`Done:` line, so the count is unchanged by this handback and stays `11` until the next round's
first commit books a proper `Done:` paragraph).

## Authored-text proofs

C1's five byte copies were each proved byte-equal to their prepared `c1-` file immediately after
copying, via a dedicated copy-and-hash script (every digest in `digests.txt`, and `digests.txt`'s
own sha256 against the one the session prompt named, independently confirmed before any prepared
file was read). The authored block's own proof: `.agent/authored/f162-r8.md` is 120 lines (`wc -l`)
with sha256 `4fb410592ebb240cbedef8a01e83b7195f7d9bc16513c1c8c3f07f71b5db9e89`, identical to
`block.md`'s own sha256 — the same digest `digests.txt` names for both prepared files. Gate 1's
`verify.py` run independently re-confirmed every `C1 ... equals c1-...` line `True`.

## Deviations & assumptions

1. DECISION F162 D8 (3) states the proof map as "one constant" per "(runner, key) pair", without a
   third axis for the row's own state. This round builds exactly that: ONE node id per (runner,
   key), reused identically across all four profile tables for that key, rather than a separate id
   per (profile, state). Consequence, stated plainly rather than left implicit: for a dimension
   whose only direct fixture proves a REAL limit (the cpu, memory and nofile fixtures), a row whose
   own state is the vacuous "nothing to limit" case (for example the claude-cli default's
   `ulimits.cpu_s`, which is `None`) still cites that same fixture's node id, because no fixture
   proves the vacuous case directly and the DECISION text does not provide a second column for it.
   The two mechanical checks the walk runs — every node id resolves to a defined test, and every
   fixture-process test is named by some row — both hold regardless; what this assumption trades
   away is a tighter, per-state link the DECISION's prose does not itself require.
2. Building the document's generator (`scripts/render_sandbox_model.py`) gave
   `packages/orchestration/sandbox_container.py` its first non-test importer, which makes its
   `ALLOWED_UNWIRED` entry in `tests/test_no_orphan_modules.py` stale (that guard's own second test
   asserts the list only shrinks). The entry is removed in this round's C3, and the fact that the
   module's first real-code reacher is this round's documentation generator rather than F246's gate
   plugin run (R-1467, still open and still owned by F246) is recorded here rather than left for a
   later round to rediscover.
3. The literal argv tests in `tests/orchestration/test_sandbox_container.py` were left unchanged,
   as the block's conditional instructs: on this host `tmp_path` is already its own real path (the
   prefix and the `os.path.realpath` of it are byte-identical), confirmed before editing anything,
   so C2's `os.path.realpath` call changes no existing test's expected value.
4. No file outside the paths named per commit; no mutation red-proof; no full suite run beyond
   gate 2's own selection; no `REMEDY_TEST_MAX_WORKERS`; no two test commands run at once; no
   `claude` binary invoked; no container image pulled, built or pushed, and no container started
   outside the test runs; no worktree of my own; no `gh pr merge`, branch switch, rebase, amend,
   force-push or `--no-verify`; no agent, fork or subagent of any kind — every command this round
   is one call, run alone.

## For the operator, in plain sentences

This session recorded the previous session's passing result, then closed the one small gap the
previous review found in the container runner's workspace handling, its environment passthrough
and its cleanup rule. It then built the one piece this feature's plan has been pointing at since
it started: a single page that lists, for every safety profile this feature ships, exactly what
each of the two ways of running a worker does and does not protect against, with every line tied
to the real test that proves it, and regenerated automatically so the page can never drift from
the code behind it. Finally, it proved with a real child process that the one worker type already
using this safety net really does have its open-files limit enforced, not merely declared. What
remains for this feature is a short closing sequence that a fresh session will run: a self-check
of the feature's own build process, one full pass of every test together, and the packaging of the
evidence that both succeeded.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | five files byte-equal to the prepared snapshots; numstat matched the manifest exactly |
| C2 | done | the real-path repair plus three new tests; 66 insertions |
| C3 | done | the generator, the generated document, the walk, the README rows and the orphan-list repair; 381 insertions |
| C4 | done | the end-to-end test proving the adapter's declared `nofile` reaches a real spawned child; 59 insertions |
| C5 | done | this handoff plus the ledger's one `Landed:` line |
| R-1468 | done | RESOLVED at F162 R8 by C2, `c7285033a`; booked here as `Landed:`, to become a `Done:` paragraph in the next round's first commit |
| Gate 1 | done | every line `True`, `C5` correctly `absent` |
| Gate 2 | done | exit 0, `5170 passed, 2 skipped`, no FAILED/ERROR/`process(es) behind`, neither skip from the container fixtures or the end-to-end |
| Gate 3 | done | `All checks passed!`, exit 0 |
| Gate 4 | done | `fail_count` 0; open id count `11`, matching the block exactly |
| Push | pending | runs immediately after this commit, per the block's push discipline; outcome reported in the reply |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work (absent as of this session).
2. Phase 1 rule 2: the Open PR Gate — no PR is open for F162 yet.
3. Book round 8's verdict in the next round's first commit.
4. The closure sequence per `docs/roadmap/STATUS_closure_protocol.md`: the self-use run, the
   integration gate, the evidence package.

Operator questions open: 3.
Open findings: 11 (R-1246, R-1281, R-1351, R-1353, R-1426, R-1428, R-1448, R-1450 and R-1464, owned
by F316; R-1467, owned by F246; R-1468, owned by F162 and landed this round, pending its `Done:`
paragraph).
