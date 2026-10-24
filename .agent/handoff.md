# Handoff — F152 round 5 (DECISION F152 D5: the kit's two added checks, the doctor's four isolation checks)

## Session

SESSION 1 of feature F152 · round 5 · rounds so far 5. This round booked round 4's FAIL, repaired
both findings it left open, and built T003's kit requirement and doctor checks; every commit
followed the block's ordered sequence with no split and no correction commit needed.

Fortschritt: ~75 % (T001 to T003 landed · the closure open) — Schätzung.

## Range

Review of `b55e7666a`..`08ff25679` (C1 through C4; C5 — this file plus the two `Landed:` lines
appended to `.agent/live_review.md` — is the commit that carries it, per the handback template's
self-reference exception).

## Commits

### b45228c34 F152 R5 C1: book round 4's FAIL, resolve R-1455 to R-1457, register R-1458 and R-1459, DECISION F152 D5
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f152-r5.md` | +140/-0 | NEW FILE — this round's block, the authored-text proof |
| `.agent/decisions.md` | +10/-0 | DECISION F152 D5 appended |
| `.agent/live_review.md` | +12/-0 | F152 round 4's FAIL verdict booked, R-1455/R-1456/R-1457 resolved, R-1458/R-1459 registered |
| `.agent/plan.md` | +6/-7 | rewritten: Current Step/Next Steps to round 5 |

### ba48920b1 F152 R5 C2: the A/B's isolated run never inherits, and the streamed call's own environment is read
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/worker_isolation.py` | +9/-5 | R-1458 — `run_isolation_ab`'s isolated run now takes `base_env` itself whenever `isolated_child_env` answers `None`; the function's own docstring states it in one sentence |
| `tests/orchestration/test_worker_adapter_slot.py` | +13/-7 | R-1459 — the stand-in `claude` appends one JSON line per run (argv + sorted environment names, never a value); the test reads the line whose argv carries `-p` |
| `tests/orchestration/test_worker_isolation.py` | +17/-0 | a red control: a `tool_flag` adapter declaring no allowlist now reads `marker_isolated` true, proving the leak R-1458 named now surfaces |

### d912f98cb F152 R5 C3: the kit refuses a missing record and a command line without its declared flags
| Path | +/- | Reason |
|---|---|---|
| `docs/system/worker-adapter-contract-v2.md` | +6/-0 | "## Worker isolation" gains two sentences on the kit's two new checks and the certification handshake |
| `packages/contracts/adapter_conformance_kit.py` | +25/-1 | `_check_isolation` gains D5 (1)'s two checks (record + status line; command line ends with declared `tool_args`, HTTP exempt), its own `_REPO_ROOT` resolved from the kit module's location |
| `tests/contracts/test_adapter_conformance_kit.py` | +88/-4 | the conforming CLI toy now ends its command line with its declared flag (and every CLI toy that overrides `build_invocation` is updated to match or given a flagless declaration); two new broken-case toys (missing record, dropped flag); four new isolation-dimension tests (ends-with-flag, no-status-line via `tmp_path`+monkeypatch, applies=False skips the flag check, HTTP skips it) |

### 08ff25679 F152 R5 C4: worker doctor checks every worker's isolation
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/worker.py` | +11/-0 | `_cmd_worker_doctor` adds the four isolation checks for every `available` spec naming an adapter, right after its executable check and only once that executable is found; existing checks, order and wording unchanged |
| `docs/system/worker-adapter-contract-v2.md` | +4/-1 | "## Worker isolation" gains one sentence on the doctor's four checks |
| `packages/orchestration/worker_isolation.py` | +105/-0 | `has_isolation_record`, `read_tool_help`, `isolation_doctor_checks` (D5 (2)); see Deviations for why `has_isolation_record` is a second definition rather than a shared import |
| `tests/cli/test_worker.py` | +62/-0 | every `TestWorkerDoctor` test that makes `claude` found now also replaces `read_tool_help`; two new tests (the four `isolation_claude_code_*` checks appear and pass; a help reader omitting a flag fails `isolation_claude_code_flags` and blocks readiness) |
| `tests/orchestration/test_worker_isolation.py` | +117/-0 | `TestIsolationDoctorChecks` — all four pass for the reference adapter; the flags check names the rejected flag; the home check fails when `HOME` is unset and, for a throwaway-home adapter, when the temp folder cannot hold a directory; the record check fails for a missing record; a declaration that does not apply answers one passing check; the declaration check fails for an adapter with no `isolation()`; `read_tool_help` answers `None` for a missing executable |

### (this commit) F152 R5 C5: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file — carried alone, per the handback template's self-reference exception (R-0149) |
| `.agent/live_review.md` | +4/-0 | two `Landed:` lines for R-1458 and R-1459, per this round's own constraint (no `Done:` line written) |

## External actions

No `gh` command this round: the Open PR Gate runs at the next round's start (Next, below). No
worktree created or removed; no stash entry touched; no provider call; the real `claude` binary was
never invoked — every test whose doctor path reaches the help reader replaces `read_tool_help`
first. `git push origin feature/f152-worker-config-isolation` runs once, immediately after this
commit. The block orders no pull request.

## Verification

**Gate 1.** `git status --porcelain` → empty. Then `python3 .remedy-wt/f152-r5/prep/verify.py .`:

```
True	b45228c34 single parent equal to the commit before it
True	b45228c34 subject carries a F152 R5 Cn tag: F152 R5 C1: book round 4's FAIL, resolve R-1455 to R-1457, register R-
True	b45228c34 insertions 168 under 500
True	b45228c34 adds no machine path
True	ba48920b1 single parent equal to the commit before it
True	ba48920b1 subject carries a F152 R5 Cn tag: F152 R5 C2: the A/B's isolated run never inherits, and the streamed ca
True	ba48920b1 insertions 39 under 500
True	ba48920b1 adds no machine path
True	d912f98cb single parent equal to the commit before it
True	d912f98cb subject carries a F152 R5 Cn tag: F152 R5 C3: the kit refuses a missing record and a command line withou
True	d912f98cb insertions 119 under 500
True	d912f98cb adds no machine path
True	08ff25679 single parent equal to the commit before it
True	08ff25679 subject carries a F152 R5 Cn tag: F152 R5 C4: worker doctor checks every worker's isolation
True	08ff25679 insertions 299 under 500
True	08ff25679 adds no machine path
True	on feature/f152-worker-config-isolation
True	C1 at most one split or correction: 1 commit(s)
True	C1 paths ['.agent/authored/f152-r5.md', '.agent/decisions.md', '.agent/live_review.md', '.agent/plan.md']
True	C1 .agent/authored/f152-r5.md equals c1-.agent__authored__f152-r5.md
True	C1 .agent/decisions.md equals c1-.agent__decisions.md
True	C1 .agent/live_review.md equals c1-.agent__live_review.md
True	C1 .agent/plan.md equals c1-.agent__plan.md
True	C2 at most one split or correction: 1 commit(s)
True	C2 paths ['packages/orchestration/worker_isolation.py', 'tests/orchestration/test_worker_adapter_slot.py', 'tests/orchestration/test_worker_isolation.py']
True	C3 at most one split or correction: 1 commit(s)
True	C3 paths ['docs/system/worker-adapter-contract-v2.md', 'packages/contracts/adapter_conformance_kit.py', 'tests/contracts/test_adapter_conformance_kit.py']
True	C4 at most one split or correction: 1 commit(s)
True	C4 paths ['apps/cli/commands/worker.py', 'docs/system/worker-adapter-contract-v2.md', 'packages/orchestration/worker_isolation.py', 'tests/cli/test_worker.py', 'tests/orchestration/test_worker_isolation.py']
absent	C5
True	the saved block equals block.md
ALL True
```

Every line `True` (C5 correctly `absent` before this commit exists); the last line is `ALL True`.
Run before C5, as the block orders; this file is written and committed after.

**Gate 2.** `python3 .remedy-wt/f152-r5/prep/run_selection.py . .remedy-wt/f152-r5-worker/selection-output.txt`,
run once after C4:

```
paths 88
exit 0
3953 passed, 2 skipped in 30.60s
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
```

Exit 0, no `FAILED` or `ERROR` line, no "process(es) behind" line. Both `SKIPPED` lines are
pre-existing, documented skips unrelated to this round — identical to round 4's reading.

**Gate 3.** `python3 -m ruff check` over every Python file C2 to C4 touched (7 files:
`packages/orchestration/worker_isolation.py`, `tests/orchestration/test_worker_isolation.py`,
`tests/orchestration/test_worker_adapter_slot.py`, `packages/contracts/adapter_conformance_kit.py`,
`tests/contracts/test_adapter_conformance_kit.py`, `apps/cli/commands/worker.py`,
`tests/cli/test_worker.py`):

```
All checks passed!
```

Exit 0.

**Gate 4.** `python3 -m apps.cli.main integrity check --json`, run once:

```
{"check_count": 6, "checks": [{"message": "handlers=201", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict FAIL", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```

`fail_count` 0, all six checks `pass`, `"ok": true`. `live_review_verdict` reads "last Gate verdict
FAIL" because round 4's own FAIL is the most recent Gate entry this check can see at this point in
the branch's own history; that is the round this handback books the repair for, not a defect of
this one.

**Gate 5.** `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` →
`10`, exit 0 — exactly the count the block names (the eight F316-owned ids plus R-1458 and R-1459,
each still OPEN in the ledger text itself even though this round's own code repairs them; two
`Landed:` lines are appended in C5 rather than a `Done:` line, per this round's own constraint, so
the ledger entries stay open and the count is unchanged by that append).

## Authored-text proofs

C1's byte copy (`.remedy-wt/f152-r5-worker/copy_c1.py`) read `equal` for all four targets
immediately after copying: `.agent/authored/f152-r5.md`, `.agent/live_review.md`,
`.agent/decisions.md`, `.agent/plan.md`. `.agent/authored/f152-r5.md`'s own line count and
sha256 — `140` lines, `ecb16ce82a6ded28914e3460c568636e18c756d0d29587fb4fa88a2605a1200d` — were
independently confirmed equal to `block.md`'s own count and digest by `wc -l` and `sha256sum` run
directly on both files. Gate 1's `verify.py` run independently re-confirmed every `C1 ...
equals c1-...` line `True` and the saved block equals `block.md`.

C2 to C4 carry no second reviewer-prepared text to compare against (no `c2-`/`c3-`/`c4-` files
exist in the prep bundle beyond `d5.md`, `gate.md`, `run_selection.py`, `selection.txt` and
`verify.py`, which are specification/tooling files rather than per-commit authored proofs); their
own content is this round's worker-authored code and tests, checked by the gates above rather than
a byte comparison.

## Deviations & assumptions

One deviation, declared as the block's own D5 (2) escape clause invites: D5 (2) asks the doctor's
record check to call "the same function the kit's record check uses", naming a move of that
function into `worker_isolation.py` with the kit importing it. C4's own Paths list, however, names
only `packages/orchestration/worker_isolation.py`, `apps/cli/commands/worker.py`,
`tests/orchestration/test_worker_isolation.py`, `tests/cli/test_worker.py` and
`docs/system/worker-adapter-contract-v2.md` — it does not list
`packages/contracts/adapter_conformance_kit.py`. Editing the kit module to import a new function
would be a file outside the paths named per commit (AGENTS.md's Commit Gate), so this round keeps
C3's already-committed kit definition (`_has_isolation_status_line` and the kit's own `_REPO_ROOT`)
untouched, and `worker_isolation.py` instead carries its own `has_isolation_record`, checking the
identical property (a file under the repository root holding a line beginning `> **Status:`) by a
second, independent definition. This is declared inline in `worker_isolation.py`'s own comment
above `has_isolation_record` and `_REPO_ROOT`, not only here.

Two judgment calls worth stating explicitly rather than leaving implicit, since the block's own
prose did not spell out every detail: first, `isolation_doctor_checks`'s single "does not apply"
answer is named `isolation_<provider_id>` with no suffix, distinct from the four per-check names
(`_declaration`, `_record`, `_home`, `_flags`), so a reader cannot mistake it for one of the four
and the block's "one passing check" wording is met literally rather than by omitting three of the
four. Second, the flags check always calls `read_tool_help` while the declaration applies, even
for a declaration naming no `tool_args` at all (unlike the kit's own flag check, which the block
explicitly gates on "and names `tool_args`"): an empty `tool_args` trivially passes (nothing is
missing from the help text), so the behaviour is the same either way and no test depends on the
difference, but the doctor's own wording in D5 (2) omits that extra gate where the kit's does not,
so the code follows the doctor's own sentence literally.

Every commit otherwise followed the block's ordered sequence exactly: no split (`C2a`/`C2b`,
`C3a`/`C3b` or `C4a`/`C4b`), no correction commit, no file touched outside the paths named per
commit (beyond the one declared exception above, which touched no file outside its OWN commit's
scope — it kept a file within C4's Paths from reaching into another commit's). No mutation
red-proofs, no full suite, no `REMEDY_TEST_MAX_WORKERS`, no two test commands run at once, no
`claude` binary invoked by any test.

## For the operator, in plain sentences

This round closed the book on the two small gaps last round's check-up found in the practice proof
that shows a worker tool's protection really works, and then built the two remaining pieces of the
isolation work this feature set out to do. A worker tool's own certification test now refuses to
pass it unless its protection is backed by a real written research page and unless its actual
command line still carries every protective flag it claims to use, so a tool cannot be approved
on paperwork alone. And the day-to-day health check this project runs before trusting a tool now
looks at that same protection directly: it confirms the tool's research page exists and is
complete, that its personal-folder handling is sound, and that its protective flags are still
accepted by the tool's own help text, all without ever placing a real paid call. Every other test
this project runs, the project's own health check, and its open-findings count all stayed exactly
where they should. Nothing is pushed yet; that happens right after this note is saved.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | four files byte-equal to the prepared snapshots |
| C2 | done | R-1458 and R-1459 repaired, with a red control proving each |
| C3 | done | the kit's two new isolation checks, the new broken-case toys, the new positive tests, the contract page |
| C4 | done | the doctor's four isolation checks, wired into `worker doctor`, with full test coverage |
| C5 | done | this handback |
| R-1458 | done | repaired in C2, `ba48920b1` |
| R-1459 | done | repaired in C2, `ba48920b1` |
| Gate 1 | done | every line `True`, last line `ALL True` |
| Gate 2 | done | exit 0, `3953 passed, 2 skipped`, no FAILED/ERROR, no leftover process |
| Gate 3 | done | exit 0, all checks passed |
| Gate 4 | done | `fail_count` 0, all six checks pass |
| Gate 5 | done | open-id count 10, matches the block exactly |
| Push | pending | runs once immediately after this commit |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work.
2. Phase 1 rule 2: the Open PR Gate, before any new branch.
3. Book round 5's verdict in the next round's first commit.
4. The closure sequence: the integration gate.

Operator questions open: 3.
Open findings: 10.
