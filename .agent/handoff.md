# Handoff — F152 round 6 (R-1460 to R-1462 repaired: real flags only, one record check, no path printed)

## Session

SESSION 1 of feature F152 · round 6 · rounds so far 6. This round booked round 5's FAIL and
repaired all three findings it left open, each with its own red-proving test; every commit
followed the block's ordered sequence with no split and no correction commit needed.

Fortschritt: ~80 % (T001 to T003 landed · the closure open) — Schätzung.

## Range

Review of `d031acbbf`..`ee1575b7e` (C1 and C2; C3 — this file plus the three `Landed:` lines
appended to `.agent/live_review.md` — is the commit that carries it, per the handback template's
self-reference exception).

## Commits

### 71c3c276a F152 R6 C1: book round 5's FAIL, resolve R-1458 and R-1459, register R-1460 to R-1462
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f152-r6.md` | +89/-0 | NEW FILE — this round's block, the authored-text proof |
| `.agent/live_review.md` | +12/-0 | F152 round 5's FAIL verdict booked, R-1458/R-1459 already resolved from round 5, R-1460/R-1461/R-1462 registered |
| `.agent/plan.md` | +7/-6 | rewritten: Current Step/Next Steps to round 6 |
| `.agent/prose_slips.md` | +1/-0 | one prose-slip line for round 5's C4 Paths/text contradiction, the duplicate that is R-1461 |

### ee1575b7e F152 R6 C2: the doctor checks only real flags against the captured help, one record check, no path printed
| Path | +/- | Reason |
|---|---|---|
| `packages/contracts/adapter_conformance_kit.py` | +4/-13 | R-1461 — `_has_isolation_status_line` and the kit's own `_REPO_ROOT` are gone; `_check_isolation` imports and calls `has_isolation_record` from `worker_isolation.py` |
| `packages/orchestration/worker_isolation.py` | +13/-12 | R-1460 — the flags check now looks up only the `tool_args` members beginning with `--`; R-1462 — the home check's passing detail reads `HOME is a directory`, never a path; the `_REPO_ROOT`/`has_isolation_record` comments drop the round-5 deviation note, now the one true definition |
| `tests/cli/test_worker.py` | +9/-5 | the stand-in help-text constant is now `.agent/f302_claude_help.txt` lines 228 to 233 verbatim, with a comment naming the source |
| `tests/contracts/test_adapter_conformance_kit.py` | +4/-2 | `test_isolation_fails_for_a_record_with_no_status_line` patches `worker_isolation._REPO_ROOT` instead of the kit's, which no longer exists |
| `tests/orchestration/test_worker_isolation.py` | +14/-4 | the stand-in help-text constant is the same verbatim six lines; the reference-adapter pass test gains an `os.sep`-free assertion on the home detail (R-1462) |

### (this commit) F152 R6 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file — carried alone, per the handback template's self-reference exception (R-0149) |
| `.agent/live_review.md` | +6/-0 | three `Landed:` lines for R-1460, R-1461 and R-1462, per this round's own constraint (no `Done:` line written) |

## External actions

No `gh` command this round: the Open PR Gate runs at the next round's start (Next, below). No
worktree created or removed; no stash entry touched; no provider call; the real `claude` binary was
never invoked — every test whose doctor path reaches the help reader replaces `read_tool_help`
first, and the one test running a real executable (`test_read_tool_help_answers_none_for_an_executable_that_does_not_exist`)
runs one that does not exist. `git push origin feature/f152-worker-config-isolation` runs once,
immediately after this commit. The block orders no pull request.

## Verification

**Gate 1.** `git status --porcelain` → empty. Then `python3 .remedy-wt/f152-r6/prep/verify.py .`:

```
True	71c3c276a single parent equal to the commit before it
True	71c3c276a subject carries a F152 R6 Cn tag: F152 R6 C1: book round 5's FAIL, resolve R-1458 and R-1459, register R
True	71c3c276a insertions 109 under 500
True	71c3c276a adds no machine path
True	ee1575b7e single parent equal to the commit before it
True	ee1575b7e subject carries a F152 R6 Cn tag: F152 R6 C2: the doctor checks only real flags against the captured hel
True	ee1575b7e insertions 44 under 500
True	ee1575b7e adds no machine path
True	on feature/f152-worker-config-isolation
True	C1 at most one correction: 1 commit(s)
True	C1 paths ['.agent/authored/f152-r6.md', '.agent/live_review.md', '.agent/plan.md', '.agent/prose_slips.md']
True	C1 .agent/authored/f152-r6.md equals c1-.agent__authored__f152-r6.md
True	C1 .agent/live_review.md equals c1-.agent__live_review.md
True	C1 .agent/plan.md equals c1-.agent__plan.md
True	C1 .agent/prose_slips.md equals c1-.agent__prose_slips.md
True	C2 at most one correction: 1 commit(s)
True	C2 paths ['packages/contracts/adapter_conformance_kit.py', 'packages/orchestration/worker_isolation.py', 'tests/cli/test_worker.py', 'tests/contracts/test_adapter_conformance_kit.py', 'tests/orchestration/test_worker_isolation.py']
absent	C3
True	the kit keeps no copy of the check
True	the kit calls has_isolation_record
True	one definition of has_isolation_record
True	the saved block equals block.md
ALL True
```

Every line `True` (C3 correctly `absent` before this commit exists); the last line is `ALL True`.
Run before C3, as the block orders; this file is written and committed after.

**Gate 2.** `python3 .remedy-wt/f152-r6/prep/run_selection.py . .remedy-wt/f152-r6-worker/selection-output.txt`,
run once after C2:

```
paths 88
exit 0
3953 passed, 2 skipped in 30.52s
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
```

Exit 0, no `FAILED` or `ERROR` line, no "process(es) behind" line. Both `SKIPPED` lines are
pre-existing, documented skips unrelated to this round — identical to round 5's reading.

**Gate 3.** `python3 -m ruff check` over every Python file C2 touched (5 files:
`packages/orchestration/worker_isolation.py`, `packages/contracts/adapter_conformance_kit.py`,
`tests/orchestration/test_worker_isolation.py`, `tests/cli/test_worker.py`,
`tests/contracts/test_adapter_conformance_kit.py`):

```
All checks passed!
```

Exit 0.

**Gate 4.** `python3 -m apps.cli.main integrity check --json`, run once:

```
{"check_count": 6, "checks": [{"message": "handlers=201", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict FAIL", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```

`fail_count` 0, all six checks `pass`, `"ok": true`. `live_review_verdict` reads "last Gate verdict
FAIL" because round 5's own FAIL is the most recent Gate entry this check can see at this point in
the branch's own history; that is the round this handback books the repair for, not a defect of
this one.

**Gate 5.** `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` →
`11`, exit 0 — exactly the count the block names (the eight F316-owned ids plus R-1460, R-1461 and
R-1462, each still OPEN in the ledger text itself even though this round's own code repairs them;
three `Landed:` lines are appended in C3 rather than a `Done:` line, per this round's own
constraint, so the ledger entries stay open and the count is unchanged by that append).

## Authored-text proofs

C1's byte copy (`.remedy-wt/f152-r6-worker/c1_copy.py`) read `True` for all four targets
immediately after copying: `.agent/authored/f152-r6.md`, `.agent/live_review.md`,
`.agent/prose_slips.md`, `.agent/plan.md`. `.agent/authored/f152-r6.md`'s own line count and
sha256 — `89` lines, `13663acc54fe2d4db576a84abe85ec57464f47432dda1abd2fa4a0fc4cca0eb5` — were
independently confirmed equal to `block.md`'s own count and digest, computed directly on both
files. Gate 1's `verify.py` run independently re-confirmed every `C1 ... equals c1-...` line
`True` and the saved block equals `block.md`.

C2 carries no second reviewer-prepared text to compare against (no `c2-`/`c3-` files exist in the
prep bundle beyond `block.md`, `gate.md`, `run_selection.py`, `selection.txt` and `verify.py`,
specification/tooling files rather than per-commit authored proofs); its own content is this
round's worker-authored code and tests, checked by the gates above rather than a byte comparison.

## Deviations & assumptions

None. The one place the block anticipated a possible departure — "it may replace the kit's
`_REPO_ROOT`; if so, point it at the one remaining definition" — is exactly what C2 does in
`tests/contracts/test_adapter_conformance_kit.py`, so that is not a deviation from the block but
the block's own named branch, taken. Every commit followed the block's ordered sequence exactly:
no split (`C1a`/`C1b`, `C2a`/`C2b`), no correction commit, no file touched outside the paths named
per commit. No mutation red-proofs, no full suite, no `REMEDY_TEST_MAX_WORKERS`, no two test
commands run at once, no `claude` binary invoked by any test.

## For the operator, in plain sentences

This round closed the book on last round's check-up and repaired the three small gaps it found.
The day-to-day health check now reads a worker tool's real help text the way that text is actually
written, rather than expecting an exact phrase that never appears verbatim, so the check no longer
raises a false alarm on a real machine. The requirement that a worker tool's protection be backed
by a written research page is now checked by one single piece of code that both the certification
test and the health check call, instead of two separate copies that could quietly drift apart. And
the health check's own report about a worker's personal folder no longer prints the folder's actual
location, only whether one exists, matching this project's standing rule against printing machine
paths. Every other test this project runs, the project's own health check, and its open-findings
count all stayed exactly where they should. Nothing is pushed yet; that happens right after this
note is saved.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | four files byte-equal to the prepared snapshots |
| C2 | done | R-1460, R-1461 and R-1462 repaired, each with its own red-proving assertion |
| C3 | done | this handback |
| R-1460 | done | repaired in C2, `ee1575b7e` |
| R-1461 | done | repaired in C2, `ee1575b7e` |
| R-1462 | done | repaired in C2, `ee1575b7e` |
| Gate 1 | done | every line `True`, last line `ALL True` |
| Gate 2 | done | exit 0, `3953 passed, 2 skipped`, no FAILED/ERROR, no leftover process |
| Gate 3 | done | exit 0, all checks passed |
| Gate 4 | done | `fail_count` 0, all six checks pass |
| Gate 5 | done | open-id count 11, matches the block exactly |
| Push | pending | runs once immediately after this commit |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work.
2. Phase 1 rule 2: the Open PR Gate, before any new branch.
3. Book round 6's verdict in the next round's first commit.
4. The closure sequence.

Operator questions open: 3.
Open findings: 11.
